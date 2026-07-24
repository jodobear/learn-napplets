import copy
import json
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
        comparison = [changed, {'id': 'SRC-POLICY-002', 'outcome': 'unavailable'}, {'id': 'SRC-POLICY-001', 'outcome': 'ambiguous'}]
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


if __name__ == '__main__':
    unittest.main()
