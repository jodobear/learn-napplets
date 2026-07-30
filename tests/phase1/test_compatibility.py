import builtins
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]
SCHEMA=ROOT/'.planning/research/schemas/compatibility.schema.json'
MATRIX=ROOT/'.planning/research/compatibility-matrix.yaml'
SNAPSHOT=ROOT/'.planning/research/open-work-snapshot.json'
SHA='a'*64; COMMIT='0'*40
PIN={'sourceId':'SRC-POLICY-001','commitSha':COMMIT,'path':'policy.md','contentSha256':SHA}
DIMENSIONS=[
    {'name': name, 'status': 'blocked', 'evidenceClassExpectation': 'test evidence', 'authorityExpectation': 'test authority', 'references': [{'id': 'SRC-POLICY-001', 'relation': 'candidate', 'locator': 'commit:test path:policy.md', 'contentSha256': SHA}], 'missingReason': 'test-only blocked dimension'}
    for name in ('normativeProtocol', 'observedImplementation', 'publishedPackage', 'runtime', 'exampleFixture', 'currentWork', 'conformance')
]
RECORD={'id':'CMP-POLICY-001','kind':'compatibility','sourceBaseline':[PIN],'packages':['PKG-POLICY-001'],'runtimes':['RUN-POLICY-001'],'examples':['EXM-POLICY-001'],'fixtures':['FIX-POLICY-001'],'knownDrift':['DRF-POLICY-001'],'testEvidence':['TST-POLICY-001'],'observedAt':'2026-07-24T00:00:00Z','releaseState':PIN,'currentWork':copy.deepcopy(PIN),'dimensions':DIMENSIONS}


class CompatibilitySchema(unittest.TestCase):
    def test_requires_pinned_release_and_current_work_baselines(self):
        validator=Draft202012Validator(json.loads(SCHEMA.read_text()))
        self.assertFalse(list(validator.iter_errors(RECORD)))
        bad=copy.deepcopy(RECORD); bad['currentWork']['commitSha']=''; self.assertTrue(list(validator.iter_errors(bad)))

    def test_matrix_covers_blocked_public_surfaces_without_mixing_baselines(self):
        matrix = yaml.safe_load(MATRIX.read_text())['compatibility']
        snapshot = json.loads(SNAPSHOT.read_text())
        self.assertGreaterEqual(len(matrix), 1)
        self.assertEqual(snapshot['classification'], 'directional-evidence')
        self.assertEqual(snapshot['retrievedAt'], '2026-07-24T00:00:00Z')
        validator = Draft202012Validator(json.loads(SCHEMA.read_text()))
        for record in matrix:
            self.assertFalse(list(validator.iter_errors(record)))
            self.assertEqual(record['releaseState']['sourceId'], record['currentWork']['sourceId'])
            self.assertEqual(record['releaseState']['commitSha'], record['currentWork']['commitSha'])
            self.assertIn('public exports only', record['scope'])
            self.assertIn('status', record)

    def test_compatibility_v1_to_v2_migration(self):
        migration_path = ROOT / 'tools/migrate-phase1-records.py'
        spec = importlib.util.spec_from_file_location('phase1_migrate_records', migration_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        legacy = ROOT / '.planning/research/schemas/fixtures/compatibility-v1-legacy.yaml'
        expected = ROOT / '.planning/research/schemas/fixtures/compatibility-v2-current.yaml'
        migrated = module.migrate_compatibility_v1_to_v2(yaml.safe_load(legacy.read_text()))
        self.assertEqual(module.compatibility_yaml_bytes(migrated), expected.read_bytes())
        record = migrated['compatibility'][0]
        self.assertEqual(migrated['schemaVersion'], 2)
        self.assertEqual(
            [dimension['name'] for dimension in record['dimensions']],
            ['normativeProtocol', 'observedImplementation', 'publishedPackage', 'runtime', 'exampleFixture', 'currentWork', 'conformance'],
        )
        self.assertTrue(all(dimension['status'] == 'blocked' for dimension in record['dimensions']))
        self.assertNotIn('baselineEligibility', record)
        self.assertEqual(record['sourceBaseline'][0]['sourceId'], 'SRC-POLICY-001')
        self.assertEqual(record['packages'], ['CLM-CMP-PACKAGE-001'])
        self.assertEqual(record['knownDrift'], ['DRF-ARTIFACT-001', 'DRF-CONFORMANCE-001', 'DRF-DISCOVERY-001', 'DRF-EGRESS-001', 'DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001', 'DRF-HANDSHAKE-001', 'DRF-IDENTITY-001', 'DRF-INTENT-001', 'DRF-MANIFEST-001', 'DRF-METADATA-001', 'DRF-UNKNOWN-MESSAGES-001'])
        self.assertEqual(module.migrate_compatibility_v1_to_v2(migrated), migrated)
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            temporary_path = Path(temporary)
            output = temporary_path / 'compatibility.yaml'
            module.migrate_compatibility_file(legacy, output)
            self.assertEqual(output.read_bytes(), expected.read_bytes())
            malformed = temporary_path / 'malformed.yaml'
            malformed.write_text('schemaVersion: 1\ncompatibility: bad\n')
            rejected = subprocess.run(
                [str(ROOT / 'tools/phase1-python'), str(migration_path), 'migrate-compatibility', '--input', str(malformed), '--output', str(temporary_path / 'must-not-exist.yaml')],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertFalse((temporary_path / 'must-not-exist.yaml').exists())

    def _research_validator(self):
        spec = importlib.util.spec_from_file_location('phase1_research_validator', ROOT / 'tools/validate-research.py')
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _compatibility_snapshot(self, module, planning: Path = ROOT / '.planning'):
        return {
            relative: (planning / relative).read_bytes()
            for relative in module.COMPATIBILITY_SNAPSHOT_TARGETS
        }

    def test_baseline_eligibility_requires_all_substantive_dimensions_without_approval(self):
        module = self._research_validator()
        snapshot = self._compatibility_snapshot(module)
        index = module.build_compatibility_snapshot_index(snapshot)
        baseline = module.evaluate_compatibility_baseline(index)
        self.assertEqual(baseline['status'], 'blocked')
        self.assertEqual(baseline['approval'], 'not-approved')
        self.assertEqual(
            baseline['reasons'],
            ['DIMENSION_NORMATIVE_PROTOCOL_BLOCKED', 'DIMENSION_OBSERVED_IMPLEMENTATION_BLOCKED', 'DIMENSION_PUBLISHED_PACKAGE_BLOCKED', 'DIMENSION_RUNTIME_BLOCKED', 'DIMENSION_EXAMPLE_FIXTURE_BLOCKED', 'DIMENSION_CURRENT_WORK_BLOCKED', 'DIMENSION_CONFORMANCE_BLOCKED', 'APPROVAL_NOT_GRANTED'],
        )
        for dimension in ('normativeProtocol', 'observedImplementation', 'publishedPackage', 'runtime', 'exampleFixture', 'currentWork', 'conformance'):
            with self.subTest(dimension=dimension):
                mutated = dict(snapshot)
                matrix = yaml.safe_load(mutated['research/compatibility-matrix.yaml'])
                record = matrix['compatibility'][0]
                for item in record['dimensions']:
                    item['status'] = 'qualified'
                next(item for item in record['dimensions'] if item['name'] == dimension)['status'] = 'blocked'
                record['baselineEligibility'] = {'status': 'review-required', 'approval': 'not-approved', 'reasons': []}
                mutated['research/compatibility-matrix.yaml'] = yaml.safe_dump(matrix, sort_keys=False).encode()
                result = module.evaluate_compatibility_baseline(module.build_compatibility_snapshot_index(mutated))
                self.assertEqual(result['status'], 'blocked')
                self.assertIn(f"DIMENSION_{module.dimension_reason_token(dimension)}_BLOCKED", result['reasons'])
        complete = dict(snapshot)
        matrix = yaml.safe_load(complete['research/compatibility-matrix.yaml'])
        record = matrix['compatibility'][0]
        for item in record['dimensions']:
            item['status'] = 'qualified'
        record['baselineEligibility'] = {'status': 'eligible', 'approval': 'not-approved', 'reasons': []}
        complete['research/compatibility-matrix.yaml'] = yaml.safe_dump(matrix, sort_keys=False).encode()
        result = module.evaluate_compatibility_baseline(module.build_compatibility_snapshot_index(complete))
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['approval'], 'not-approved')
        self.assertIn('APPROVAL_NOT_GRANTED', result['reasons'])
        self.assertFalse(result['architectureApproved'])

    def test_compatibility_evaluation_rejects_unbound_reviewed_acquisition_provenance(self):
        module = self._research_validator()
        snapshot = self._compatibility_snapshot(module)
        queue = json.loads(snapshot['research/upstream-acquisition-queue.yaml'])
        queue['reviewedSourceInputBinding']['reviewedCommit'] = '0' * 40
        snapshot['research/upstream-acquisition-queue.yaml'] = json.dumps(queue).encode()
        result = module.evaluate_compatibility_baseline(module.build_compatibility_snapshot_index(snapshot))
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['reasons'], ['PROVENANCE_REVIEWED_ACQUISITION_INVALID'])

    def test_compatibility_evaluation_uses_one_registered_snapshot_during_successful_publish(self):
        module = self._research_validator()
        recovery = module.canonical_recovery_module()
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            planning = Path(temporary) / '.planning'
            shutil.copytree(ROOT / '.planning/research', planning / 'research')
            shutil.copytree(ROOT / '.planning/spikes/spk-g-package-conformance', planning / 'spikes/spk-g-package-conformance')
            old_snapshot = recovery.read_canonical_snapshot('compatibility-baseline', module.COMPATIBILITY_SNAPSHOT_TARGETS, root=planning)
            old_index = module.build_compatibility_snapshot_index(old_snapshot)
            old_result = module.evaluate_compatibility_baseline(old_index)
            staged = {relative: old_snapshot[relative] for relative in module.COMPATIBILITY_SNAPSHOT_TARGETS}
            staged['research/claims.yaml'] += b'\n# successful-publisher-generation\n'
            published = []
            def publish_after_first_index_access():
                recovery.publish_generation(planning, staged)
                published.append(True)
            self.assertEqual(
                module.evaluate_registered_compatibility(planning, after_snapshot=publish_after_first_index_access),
                old_result,
            )
            self.assertEqual(published, [True])
            self.assertEqual(module.evaluate_compatibility_baseline(old_index), old_result)
            self.assertEqual(old_result['familyDigests'], module.compatibility_family_digests(old_index))
            guarded = module.build_compatibility_snapshot_index(old_snapshot)
            original_open = builtins.open
            original_read_bytes = Path.read_bytes
            original_read_text = Path.read_text
            def refuse_canonical_open(*args, **kwargs):
                raise AssertionError('compatibility evaluator reopened a canonical path after snapshot acquisition')
            builtins.open = refuse_canonical_open
            Path.read_bytes = refuse_canonical_open
            Path.read_text = refuse_canonical_open
            try:
                self.assertEqual(module.evaluate_compatibility_baseline(guarded), old_result)
            finally:
                builtins.open = original_open
                Path.read_bytes = original_read_bytes
                Path.read_text = original_read_text

    def _registry_command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(ROOT / 'tools/phase1-python'), str(ROOT / 'tools/collect-registry-evidence.py'), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_registry_collector_fixture_receipt_rehashes_exact_response_bytes(self):
        fixture = ROOT / 'tests/phase1/fixtures/registry-response.json'
        fixture_bytes = fixture.read_bytes()
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            receipt = Path(temporary) / 'fixture-receipt.yaml'
            result = self._registry_command(
                'collect-fixture', '--fixture', str(fixture), '--receipt', str(receipt),
                '--attempt-id', 'REG-FIXTURE-TEST-001', '--retrieved-at', '2026-07-28T00:00:00Z',
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            document = yaml.safe_load(receipt.read_text())
            self.assertEqual(document['transport'], 'fixture')
            self.assertEqual(document['request']['method'], 'GET')
            self.assertEqual(document['response']['sha256'], hashlib.sha256(fixture_bytes).hexdigest())
            self.assertEqual(document['response']['capturedBytes'], fixture_bytes.hex())
            self.assertEqual(self._registry_command('validate-receipt', '--receipt', str(receipt)).returncode, 0)
            for field, value in (
                ('method', 'POST'), ('host', 'untrusted.example'), ('redirect', 'follow'),
                ('timeoutSeconds', 0), ('maxResponseBytes', 1),
            ):
                mutated = copy.deepcopy(document)
                if field == 'method':
                    mutated['request']['method'] = value
                elif field == 'host':
                    mutated['request']['allowedHost'] = value
                elif field == 'redirect':
                    mutated['request']['redirectPolicy'] = value
                else:
                    mutated['limits'][field] = value
                receipt.write_text(yaml.safe_dump(mutated, sort_keys=False))
                self.assertNotEqual(self._registry_command('validate-receipt', '--receipt', str(receipt)).returncode, 0, field)
            receipt.write_text(yaml.safe_dump(document, sort_keys=False))
            changed = copy.deepcopy(document)
            changed['response']['capturedBytes'] = (fixture_bytes + b'!').hex()
            receipt.write_text(yaml.safe_dump(changed, sort_keys=False))
            self.assertNotEqual(self._registry_command('validate-receipt', '--receipt', str(receipt)).returncode, 0)

    def test_registry_attempt_receipts_are_separate_immutable_and_revalidated(self):
        fixture = ROOT / 'tests/phase1/fixtures/registry-response.json'
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            fixture_receipt = Path(temporary) / 'fixture.yaml'
            live_receipt = Path(temporary) / 'live.yaml'
            first = self._registry_command(
                'collect-fixture', '--fixture', str(fixture), '--receipt', str(fixture_receipt),
                '--attempt-id', 'REG-FIXTURE-TEST-002', '--retrieved-at', '2026-07-28T00:00:00Z',
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            original_fixture = fixture_receipt.read_bytes()
            live = self._registry_command(
                'collect-live-or-blocker', '--live-if-permitted', '--receipt', str(live_receipt),
                '--attempt-id', 'REG-LIVE-TEST-001', '--retrieved-at', '2026-07-28T00:00:00Z',
            )
            self.assertEqual(live.returncode, 0, live.stderr)
            fixture_document = yaml.safe_load(original_fixture)
            live_document = yaml.safe_load(live_receipt.read_text())
            self.assertNotEqual(fixture_document['attemptId'], live_document['attemptId'])
            self.assertEqual(fixture_receipt.read_bytes(), original_fixture)
            self.assertEqual(self._registry_command('validate-receipt', '--receipt', str(fixture_receipt)).returncode, 0)
            self.assertEqual(self._registry_command('validate-receipt', '--receipt', str(live_receipt)).returncode, 0)
            overwrite = self._registry_command(
                'collect-live-or-blocker', '--live-if-permitted', '--receipt', str(live_receipt),
                '--attempt-id', 'REG-LIVE-TEST-002', '--retrieved-at', '2026-07-28T00:00:00Z',
            )
            self.assertNotEqual(overwrite.returncode, 0)
            self.assertEqual(fixture_receipt.read_bytes(), original_fixture)

    def test_registry_live_unavailable_routes_impact_scoped_blocker(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            receipt = Path(temporary) / 'live-blocker.yaml'
            result = self._registry_command(
                'collect-live-or-blocker', '--live-if-permitted', '--receipt', str(receipt),
                '--attempt-id', 'REG-LIVE-TEST-003', '--retrieved-at', '2026-07-28T00:00:00Z',
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            document = yaml.safe_load(receipt.read_text())
            self.assertEqual(document['transport'], 'live-or-blocker')
            self.assertEqual(document['outcome'], 'impact-scoped-blocker')
            blocker = document['blocker']
            self.assertEqual(blocker['affectedRequirements'], ['EVID-03', 'EVID-04', 'OPER-01'])
            self.assertIn('ADR-0010', blocker['affectedAdrs'])
            self.assertIn('OQ-PUBLIC-PACKAGE-BASELINE-001', blocker['affectedQuestions'])
            self.assertIn('DRF-ARTIFACT-001', blocker['affectedDrift'])
            self.assertTrue(blocker['safeFallback'])
            self.assertTrue(blocker['refreshTrigger'])
            self.assertEqual(self._registry_command('validate-receipt', '--receipt', str(receipt)).returncode, 0)

    def test_published_package_metadata_requires_independent_registry_artifact(self):
        evidence = yaml.safe_load((ROOT / '.planning/research/package-evidence.yaml').read_text())
        self.assertEqual(evidence['approval'], 'not-approved')
        self.assertEqual(evidence['artifactEvidence']['status'], 'blocked')
        self.assertEqual(evidence['artifactEvidence']['repositoryReleaseData'], 'not-an-artifact-substitute')
        self.assertEqual(len(evidence['receiptHistory']), 2)
        self.assertEqual({item['transport'] for item in evidence['receiptHistory']}, {'fixture', 'live-or-blocker'})

    def test_package_metadata_preserves_history_and_blocker_routing(self):
        evidence = yaml.safe_load((ROOT / '.planning/research/package-evidence.yaml').read_text())
        expected_receipts = [
            ('reports/package-registry-fixture-receipt-20260728.yaml', 'REG-FIXTURE-20260728-001',
             '4f35050e9ee18864aeec90f88053b27dc209b32301ee82d460755af16241fc80',
             'fixture', 'fixture-mechanism-only', 'mechanism-only-not-published-package-fact'),
            ('reports/package-registry-live-or-blocker-receipt-20260728.yaml', 'REG-BLOCKER-20260728-001',
             '40ebd1c8f1e8b0bcde03f01e936affb815fe2ed375113cce2547020c9c286a26',
             'live-or-blocker', 'impact-scoped-blocker', 'blocked-no-live-registry-observation'),
        ]
        self.assertEqual(
            [tuple(item[field] for field in ('path', 'attemptId', 'receiptSha256', 'transport', 'outcome', 'classification'))
             for item in evidence['receiptHistory']],
            expected_receipts,
        )
        blocker = evidence['blockedAdmission']
        self.assertEqual(blocker['disposition'], 'blocked')
        self.assertEqual(blocker['candidateId'], 'CAND-NAPPLET-WEB-PACKAGE')
        self.assertEqual(blocker['affectedRequirements'], ['EVID-03', 'EVID-04', 'OPER-01'])
        self.assertIn('ADR-0010', blocker['affectedAdrs'])
        self.assertIn('OQ-PUBLIC-PACKAGE-BASELINE-001', blocker['affectedQuestions'])
        self.assertIn('DRF-CONFORMANCE-001', blocker['affectedDrift'])
        self.assertTrue(blocker['safeFallback'])
        self.assertTrue(blocker['refreshTrigger'])

        inventory = yaml.safe_load((ROOT / '.planning/research/ecosystem-inventory.yaml').read_text())['items']
        package = next(item for item in inventory if item['id'] == 'ECO-NAPPLET-WEB-PACKAGE')
        history = package['packageEvidenceHistory']
        self.assertEqual([entry['attemptId'] for entry in history['receiptHistory']], [
            'REG-FIXTURE-20260728-001', 'REG-BLOCKER-20260728-001',
        ])
        self.assertEqual(history['repositoryIdentity']['candidateId'], 'CAND-NAPPLET-WEB-REPOSITORY')
        self.assertEqual(history['observedReleaseCommit']['status'], 'unavailable')
        self.assertEqual(history['independentlyRetrievedArtifact']['status'], 'blocked')
        routing = package['spkGBlockerRouting']
        self.assertEqual(routing['disposition'], 'blocked')
        self.assertEqual(routing['affectedRequirements'], blocker['affectedRequirements'])
        self.assertEqual(routing['affectedAdrs'], blocker['affectedAdrs'])
        self.assertEqual(routing['affectedQuestions'], blocker['affectedQuestions'])
        self.assertEqual(routing['affectedDrift'], blocker['affectedDrift'])
        self.assertTrue(routing['safeFallback'])
        self.assertTrue(routing['refreshTrigger'])
        self.assertEqual(routing['separateApproval'], 'required')
        self.assertTrue(all(item['status'] != 'complete' for item in routing['eligibility']))

        package_map = (ROOT / '.planning/research/package-map.md').read_text()
        for heading in ('## Package evidence history', '### Repository identity', '### Observed release commit',
                        '### Independently retrieved registry artifact', '### Immutable collection receipts'):
            self.assertIn(heading, package_map)

        snapshot = json.loads(SNAPSHOT.read_text())
        self.assertEqual(snapshot['id'], 'OWS-001')
        self.assertEqual(snapshot['retrievedAt'], '2026-07-24T00:00:00Z')
        self.assertEqual(
            [(item['id'], item['retrievalOutcome']) for item in snapshot['items']],
            [('OW-NIP5D-001', 'unavailable'), ('OW-NAP-001', 'unavailable'),
             ('OW-NAPPLET-WEB-001', 'unavailable'), ('OW-RUNTIME-001', 'unavailable')],
        )
        self.assertEqual([entry['id'] for entry in snapshot['snapshotHistory']], ['OWS-002'])
        current = snapshot['snapshotHistory'][0]
        self.assertEqual(current['parentSnapshotId'], 'OWS-001')
        self.assertEqual(current['retrievedAt'], '2026-07-28T00:00:00Z')
        self.assertEqual(
            [tuple(item[field] for field in ('path', 'attemptId', 'receiptSha256', 'transport', 'outcome', 'classification'))
             for item in current['items'][0]['receiptHistory']],
            expected_receipts,
        )
        self.assertEqual(current['items'][0]['spkGBlockerRouting'], routing)


if __name__=='__main__':
    unittest.main()
