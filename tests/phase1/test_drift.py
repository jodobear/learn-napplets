import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
DRIFT = ROOT / '.planning/research/schemas/drift.schema.json'
QUESTION = ROOT / '.planning/research/schemas/open-question.schema.json'
REGISTER = ROOT / '.planning/research/drift-register.yaml'
QUESTIONS = ROOT / '.planning/research/open-questions.yaml'
SOURCES = ROOT / '.planning/research/source-registry.yaml'
CLAIMS = ROOT / '.planning/research/claims.yaml'
SHA = 'a' * 64
COMMIT = '0' * 40
SIDE = {'claimId':'CLM-POLICY-001','sourceId':'SRC-POLICY-001','commitSha':COMMIT,'path':'policy.md','locator':'L1','contentSha256':SHA,'statement':'Recorded statement.','authorityTier':'project-policy','maturity':'accepted','evidenceClass':'project-policy'}
DRIFT_RECORD = {'id':'DRF-POLICY-001','kind':'drift','topic':'Policy conflict','status':'disputed','statusReason':'Parallel evidence needs review.','normative':SIDE,'observed':copy.deepcopy(SIDE),'impacts':{'content':['LES-001'],'code':['tool'],'knowledge':['map'],'requirements':['EVID-02'],'phases':['01']},'uncertainty':{'state':'material','reason':'Unresolved.'},'history':[{'at':'2026-07-24T00:00:00Z','state':'disputed','reason':'Recorded.'}],'review':{'owner':'owner','status':'pending','requiredRoles':['protocol']}}
QUESTION_RECORD = {'id':'OQ-POLICY-001','kind':'open-question','question':'What resolves the conflict?','status':'blocked','sourceRefs':['SRC-POLICY-001'],'impacts':{'requirements':['EVID-02'],'phases':['01']},'blockedDecisions':['ADR-0001'],'resolutionCriteria':['Pin and review source.'],'owner':'owner','review':{'status':'pending','requiredRoles':['protocol']},'history':[{'at':'2026-07-24T00:00:00Z','status':'blocked','reason':'Source missing.'}]}

MANDATORY_TOPICS = {
    'discovery model',
    'NAP-SHELL handshake',
    'manifest kinds',
    'dTag identity',
    'archetype/convention metadata',
    'NAP-INTENT handler/catalog assumptions',
    'unknown message/source behavior',
    'exact artifact versus build output',
    'browser egress versus mediated access',
    'conformance/private-or-retired behavior',
}
MANDATORY_DRIFT_IDS = {
    'DRF-ARTIFACT-001',
    'DRF-CONFORMANCE-001',
    'DRF-DISCOVERY-001',
    'DRF-EGRESS-001',
    'DRF-HANDSHAKE-001',
    'DRF-IDENTITY-001',
    'DRF-INTENT-001',
    'DRF-MANIFEST-001',
    'DRF-METADATA-001',
    'DRF-UNKNOWN-MESSAGES-001',
}


class DriftSchemas(unittest.TestCase):
    def validate(self, path, record):
        return list(Draft202012Validator(json.loads(path.read_text())).iter_errors(record))

    def test_parallel_conflict_requires_two_complete_sides_and_impacts(self):
        self.assertFalse(self.validate(DRIFT, DRIFT_RECORD))
        bad=copy.deepcopy(DRIFT_RECORD); del bad['observed']; self.assertTrue(self.validate(DRIFT,bad))
        bad=copy.deepcopy(DRIFT_RECORD); bad['impacts']['content']=[]; self.assertTrue(self.validate(DRIFT,bad))

    def test_open_question_requires_blocker_routing_and_resolution(self):
        self.assertFalse(self.validate(QUESTION, QUESTION_RECORD))
        for key in ('sourceRefs','blockedDecisions','resolutionCriteria','owner'):
            bad=copy.deepcopy(QUESTION_RECORD); del bad[key]; self.assertTrue(self.validate(QUESTION,bad))

    def test_mandatory_drift_register_keeps_parallel_pinned_evidence(self):
        register = yaml.safe_load(REGISTER.read_text())
        sources = {record['id']: record for record in yaml.safe_load(SOURCES.read_text())['sources']}
        claims = {record['id']: record for record in yaml.safe_load(CLAIMS.read_text())['claims']}
        records = register['drift']
        records_by_id = {record['id']: record for record in records}
        self.assertEqual(len(records_by_id), len(records))
        self.assertTrue(MANDATORY_DRIFT_IDS <= records_by_id.keys())
        self.assertEqual(
            {records_by_id[record_id]['topic'] for record_id in MANDATORY_DRIFT_IDS},
            MANDATORY_TOPICS,
        )
        for record in records:
            self.assertTrue(record['id'].startswith('DRF-'))
            self.assertFalse(self.validate(DRIFT, record))
            if record['normative'] is None:
                self.assertEqual(record['observed']['classification'], 'observed-local')
                self.assertTrue(record['observed']['id'].startswith('OBS-'))
                self.assertNotIn('claimId', record['observed'])
            else:
                if record['id'] in MANDATORY_DRIFT_IDS:
                    self.assertNotEqual(record['normative']['claimId'], record['observed']['claimId'])
                for side_name in ('normative', 'observed'):
                    side = record[side_name]
                    self.assertIn(side['claimId'], claims)
                    self.assertIn(side['sourceId'], sources)
                    source = sources[side['sourceId']]
                    self.assertEqual(
                        {key: side[key] for key in ('commitSha', 'path', 'contentSha256')},
                        {key: source[key] for key in ('commitSha', 'path', 'contentSha256')},
                    )
            self.assertIn('dependentDecisionDisposition', record)
        for record_id, record in records_by_id.items():
            if record_id not in MANDATORY_DRIFT_IDS:
                self.assertTrue(any(
                    isinstance(item, dict) and 'Consolidated SPK-' in item.get('reason', '')
                    for item in record.get('history', [])
                ))

    def test_open_questions_route_unresolved_dependent_decisions(self):
        questions = yaml.safe_load(QUESTIONS.read_text())['questions']
        self.assertGreaterEqual(len(questions), 1)
        for question in questions:
            self.assertFalse(self.validate(QUESTION, question))
            self.assertEqual(question['status'], 'blocked')
            self.assertTrue(question['blockedDecisions'])

    def test_drift_v1_to_v2_migration(self):
        script = ROOT / 'tools' / 'migrate-phase1-records.py'
        legacy = ROOT / '.planning/research/schemas/fixtures/drift-v1-legacy.yaml'
        expected = ROOT / '.planning/research/schemas/fixtures/drift-v2-current.yaml'
        with __import__('tempfile').TemporaryDirectory() as temporary:
            root = Path(temporary)
            malformed = root / 'malformed-v1.yaml'
            malformed.write_text('schemaVersion: 1\ndrift: not-a-list\n')
            malformed_output = root / 'malformed-v2.yaml'
            malformed_result = __import__('subprocess').run(
                [__import__('sys').executable, str(script), 'migrate-drift', '--input', str(malformed), '--output', str(malformed_output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(malformed_result.returncode, 0)
            self.assertFalse(malformed_output.exists())
            output = root / 'drift-v2.yaml'
            first = __import__('subprocess').run(
                [__import__('sys').executable, str(script), 'migrate-drift', '--input', str(legacy), '--output', str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
            self.assertEqual(output.read_bytes(), expected.read_bytes())
            first_bytes = output.read_bytes()
            second = __import__('subprocess').run(
                [__import__('sys').executable, str(script), 'migrate-drift', '--input', str(output), '--output', str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
            self.assertEqual(output.read_bytes(), first_bytes)
            old = yaml.safe_load(legacy.read_text())
            current = yaml.safe_load(output.read_text())
            self.assertEqual(
                sorted(item['id'] for item in old['drift']),
                sorted(item['id'] for item in current['drift']),
            )
            for before, after in zip(sorted(old['drift'], key=lambda item: item['id']), current['drift']):
                self.assertEqual(sorted(before['history'], key=lambda item: (item['at'], item['state'], item['reason'])), after['history'])
                self.assertEqual(before['normative']['claimId'], after['normative']['claimId'])
                self.assertEqual(before['observed']['claimId'], after['observed']['claimId'])

    def test_drift_records_sort_ids_observations_impacts_and_history(self):
        script = ROOT / 'tools' / 'migrate-phase1-records.py'
        legacy = {
            'schemaVersion': 1,
            'drift': [
                copy.deepcopy(DRIFT_RECORD) | {'id': 'DRF-Z-001', 'impacts': {'content': ['Z', 'A'], 'code': ['z', 'A'], 'knowledge': ['z', 'A'], 'requirements': ['EVID-04', 'EVID-01'], 'phases': ['10', '01']}, 'history': [{'at': '2026-07-25T00:00:00Z', 'state': 'blocked', 'reason': 'z'}, {'at': '2026-07-24T00:00:00Z', 'state': 'verified', 'reason': 'b'}, {'at': '2026-07-24T00:00:00Z', 'state': 'verified', 'reason': 'a'}, {'at': '2026-07-24T00:00:00Z', 'state': 'verified', 'reason': 'a'}]},
                copy.deepcopy(DRIFT_RECORD) | {'id': 'DRF-A-001'},
            ],
            'observedLocal': [
                {'id': 'OBS-Z-001', 'class': 'observed-local'},
                {'id': 'OBS-A-001', 'class': 'observed-local'},
            ],
        }
        with __import__('tempfile').TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'legacy.yaml'
            output = root / 'current.yaml'
            source.write_text(yaml.safe_dump(legacy, sort_keys=False))
            result = __import__('subprocess').run(
                [__import__('sys').executable, str(script), 'migrate-drift', '--input', str(source), '--output', str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            current = yaml.safe_load(output.read_text())
            self.assertEqual([item['id'] for item in current['drift']], ['DRF-A-001', 'DRF-Z-001'])
            self.assertEqual([item['id'] for item in current['observedLocal']], ['OBS-A-001', 'OBS-Z-001'])
            record = current['drift'][1]
            self.assertEqual(record['impacts'], {'content': ['A', 'Z'], 'code': ['A', 'z'], 'knowledge': ['A', 'z'], 'requirements': ['EVID-01', 'EVID-04'], 'phases': ['01', '10']})
            self.assertEqual(record['history'], [{'at': '2026-07-24T00:00:00Z', 'state': 'verified', 'reason': 'a'}, {'at': '2026-07-24T00:00:00Z', 'state': 'verified', 'reason': 'a'}, {'at': '2026-07-24T00:00:00Z', 'state': 'verified', 'reason': 'b'}, {'at': '2026-07-25T00:00:00Z', 'state': 'blocked', 'reason': 'z'}])

    def test_drift_rejects_empty_null_and_single_sides(self):
        local = {
            'id': 'OBS-LOCAL-001',
            'classification': 'observed-local',
            'reportPath': 'spikes/spk-c-boundary-harness/report.md',
            'reportSha256': SHA,
            'measurementPath': 'spikes/spk-c-boundary-harness/measurements.yaml',
            'measurementSha256': SHA,
            'statement': 'A bounded local fixture did not produce an attached Firefox context.',
            'fallback': 'Keep the deterministic static fallback.',
        }
        record = copy.deepcopy(DRIFT_RECORD)
        record['status'] = 'blocked'
        record['normative'] = None
        record['observed'] = local
        self.assertFalse(self.validate(DRIFT, record))
        for mutation in (
            lambda value: value.pop('normative'),
            lambda value: value.update({'normative': None, 'observed': copy.deepcopy(SIDE)}),
            lambda value: value['observed'].update({'id': 'CLM-NOT-OBS-001'}),
            lambda value: value['observed'].pop('measurementSha256'),
            lambda value: value['observed'].update({'claimId': 'CLM-SYNTHETIC-001'}),
        ):
            bad = copy.deepcopy(record)
            mutation(bad)
            self.assertTrue(self.validate(DRIFT, bad))
        register = yaml.safe_load(REGISTER.read_text())
        local_records = [item for item in register['drift'] if item.get('normative') is None]
        self.assertTrue(local_records)
        for item in local_records:
            self.assertEqual(item['status'], 'blocked')
            self.assertTrue(item['observed']['id'].startswith('OBS-'))
            self.assertEqual(item['observed']['classification'], 'observed-local')
            self.assertTrue(item['review']['owner'])
            self.assertTrue(item['dependentDecisionDisposition']['safeFallback'])

    def test_parallel_sides_are_distinct_and_adjacent(self):
        spec = importlib.util.spec_from_file_location('phase1_validate_research', ROOT / 'tools/validate-research.py')
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        parallel = copy.deepcopy(DRIFT_RECORD)
        parallel['observed']['claimId'] = 'CLM-UPSTREAM-BASELINE-001'
        parallel['observed']['sourceId'] = 'SRC-POLICY-001'
        parallel['observed']['commitSha'] = 'c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0'
        parallel['observed']['path'] = 'docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md'
        parallel['observed']['contentSha256'] = 'df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb'
        self.assertFalse(module.validate_drift([parallel], {'SRC-POLICY-001'}, {'CLM-POLICY-001', 'CLM-UPSTREAM-BASELINE-001'}))
        collapsed = copy.deepcopy(parallel)
        collapsed['observed'] = copy.deepcopy(collapsed['normative'])
        self.assertTrue(module.validate_drift([collapsed], {'SRC-POLICY-001'}, {'CLM-POLICY-001', 'CLM-UPSTREAM-BASELINE-001'}))
        local = copy.deepcopy(parallel)
        local['status'] = 'blocked'
        local['normative'] = None
        local['observed'] = {'id': 'OBS-LOCAL-001', 'classification': 'observed-local', 'reportPath': 'report.md', 'reportSha256': SHA, 'measurementPath': 'measurements.yaml', 'measurementSha256': SHA, 'statement': 'Local observation.', 'fallback': 'Use the static fallback.'}
        self.assertFalse(module.validate_drift([local], {'SRC-POLICY-001'}, {'CLM-POLICY-001', 'CLM-UPSTREAM-BASELINE-001'}))

    def test_consolidated_local_observation_retains_non_normative_provenance(self):
        spec = importlib.util.spec_from_file_location('phase1_validate_research', ROOT / 'tools/validate-research.py')
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        fragment = {
            'fragmentId': 'SPK-LOCAL-IMPACT-001',
            'spikeId': 'SPK-LOCAL-001',
            'reportPath': 'spikes/spk-local-001/report.md',
            'reportSha256': SHA,
            'measurementLinks': [{'path': 'spikes/spk-local-001/measurements.yaml', 'sha256': SHA}],
            'uncertainty': {'state': 'material', 'reason': 'Only a local fixture observation is available.'},
            'affectedRequirements': ['EVID-02'],
            'affectedPhases': ['01'],
            'proposedImpacts': [{'type': 'adr', 'id': 'ADR-0005'}],
            '_digest': SHA,
        }
        record = module.new_drift_record(fragment, 'DRF-LOCAL-001', {}, {})
        self.assertIsNone(record['normative'])
        self.assertEqual(record['observed']['classification'], 'observed-local')
        self.assertEqual(record['observed']['reportSha256'], SHA)
        self.assertEqual(record['observed']['measurementSha256'], SHA)
        self.assertEqual(record['uncertainty'], fragment['uncertainty'])
        self.assertEqual(record['impacts']['requirements'], ['EVID-02'])
        self.assertTrue(record['dependentDecisionDisposition']['revisitTrigger'])
        self.assertFalse(self.validate(DRIFT, record))
        self.assertEqual(module.validate_drift([record], {'SRC-POLICY-001'}, {'CLM-POLICY-001'}), [])


class RefreshComparisonTests(unittest.TestCase):
    script = ROOT / 'tools' / 'refresh-sources.py'

    def run_refresh(self, comparison, report):
        comparison_path = report.parent / 'comparison.json'
        comparison_path.write_text(json.dumps(comparison))
        return __import__('subprocess').run(
            [
                __import__('sys').executable, str(self.script),
                '--registry', str(SOURCES), '--claims', str(CLAIMS), '--drift', str(REGISTER),
                '--questions', str(QUESTIONS), '--comparison', str(comparison_path), '--report', str(report),
            ],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )

    def test_unchanged_refresh_is_idempotent_and_does_not_mutate_claims(self):
        source = yaml.safe_load(SOURCES.read_text())['sources'][0]
        comparison = [{key: source[key] for key in ('id', 'commitSha', 'path', 'contentSha256')}]
        before = CLAIMS.read_bytes()
        with __import__('tempfile').TemporaryDirectory() as temporary:
            report = Path(temporary) / 'refresh-review-work.md'
            first = self.run_refresh(comparison, report)
            self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
            first_report = report.read_bytes()
            second = self.run_refresh(comparison, report)
            self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
            self.assertEqual(report.read_bytes(), first_report)
            self.assertIn('unchanged', report.read_text())
        self.assertEqual(CLAIMS.read_bytes(), before)

    def test_changed_unavailable_and_ambiguous_sources_create_scoped_review_work(self):
        source = yaml.safe_load(SOURCES.read_text())['sources'][0]
        changed = {key: source[key] for key in ('id', 'commitSha', 'path', 'contentSha256')}
        changed['contentSha256'] = 'f' * 64
        comparison = [changed, {'id': 'SRC-POLICY-002', 'outcome': 'unavailable'}, {'id': 'SRC-UNKNOWN-001', 'outcome': 'ambiguous'}]
        with __import__('tempfile').TemporaryDirectory() as temporary:
            report = Path(temporary) / 'refresh-review-work.md'
            result = self.run_refresh(comparison, report)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            text = report.read_text()
            for expected in ('changed', 'unavailable', 'ambiguous', 'old pointer/digest', 'review-required'):
                self.assertIn(expected, text)
            headings = [line[3:] for line in text.splitlines() if line.startswith('## ')]
            self.assertEqual(headings, [
                'Research question', 'Sources and immutable revisions', 'Observations', 'Conflicts',
                'Inference', 'Prototype or measurement', 'Recommendation', 'Uncertainty',
                'Affected phases and requirements', 'Owner and required approval',
            ])

    def test_duplicate_refresh_observations_are_idempotent(self):
        source = yaml.safe_load(SOURCES.read_text())['sources'][0]
        observation = {key: source[key] for key in ('id', 'commitSha', 'path', 'contentSha256')}
        with __import__('tempfile').TemporaryDirectory() as temporary:
            root = Path(temporary)
            one = root / 'one.md'
            duplicate = root / 'duplicate.md'
            self.assertEqual(self.run_refresh([observation], one).returncode, 0)
            result = self.run_refresh([observation, dict(observation)], duplicate)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(duplicate.read_bytes(), one.read_bytes())
            self.assertEqual(duplicate.read_text().count(f'`{source["id"]}`: outcome'), 1)

    def test_conflicting_refresh_observations_are_one_ambiguous_result(self):
        source = yaml.safe_load(SOURCES.read_text())['sources'][0]
        first = {key: source[key] for key in ('id', 'commitSha', 'path', 'contentSha256')}
        second = dict(first)
        second['contentSha256'] = 'f' * 64
        expected_digests = sorted(
            hashlib.sha256(json.dumps(item, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
            for item in (first, second)
        )
        with __import__('tempfile').TemporaryDirectory() as temporary:
            root = Path(temporary)
            forward = root / 'forward.md'
            reverse = root / 'reverse.md'
            result = self.run_refresh([first, second], forward)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            reverse_result = self.run_refresh([second, first], reverse)
            self.assertEqual(reverse_result.returncode, 0, reverse_result.stderr + reverse_result.stdout)
            text = forward.read_text()
            self.assertEqual(forward.read_bytes(), reverse.read_bytes())
            self.assertIn('outcome `ambiguous`', text)
            self.assertEqual(len(set(re.findall(r'RFW-[A-F0-9]+', text))), 1)
            for digest in expected_digests:
                self.assertIn(digest, text)

    def test_refresh_lock_serializes_and_process_termination_releases_it(self):
        source = yaml.safe_load(SOURCES.read_text())['sources'][0]
        comparison = [{key: source[key] for key in ('id', 'commitSha', 'path', 'contentSha256')}]
        holder_code = """
import importlib.util
import sys
import time
from pathlib import Path

spec = importlib.util.spec_from_file_location('phase1_refresh_lock_holder', Path(sys.argv[1]))
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
handle = module.acquire_lock(Path(sys.argv[2]), timeout_seconds=2)
Path(sys.argv[3]).write_text('ready', encoding='utf-8')
time.sleep(30)
"""
        with __import__('tempfile').TemporaryDirectory() as temporary:
            root = Path(temporary)
            report = root / 'refresh-review-work.md'
            ready = root / 'lock-holder-ready'
            holder = subprocess.Popen([sys.executable, '-c', holder_code, str(self.script), str(report), str(ready)], cwd=ROOT)
            try:
                deadline = time.monotonic() + 2
                while not ready.exists() and holder.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(ready.exists(), 'lock holder did not acquire the refresh lock')
                blocked = self.run_refresh(comparison, report)
                self.assertNotEqual(blocked.returncode, 0)
                self.assertIn('lock is busy', blocked.stdout)
            finally:
                holder.terminate()
                holder.wait(timeout=2)
            recovered = self.run_refresh(comparison, report)
            self.assertEqual(recovered.returncode, 0, recovered.stderr + recovered.stdout)


if __name__ == '__main__':
    unittest.main()
