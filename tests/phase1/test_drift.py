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
        self.assertEqual(len(records), 10)
        self.assertEqual({record['topic'] for record in records}, MANDATORY_TOPICS)
        for record in records:
            self.assertTrue(record['id'].startswith('DRF-'))
            self.assertFalse(self.validate(DRIFT, record))
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

    def test_open_questions_route_unresolved_dependent_decisions(self):
        questions = yaml.safe_load(QUESTIONS.read_text())['questions']
        self.assertGreaterEqual(len(questions), 1)
        for question in questions:
            self.assertFalse(self.validate(QUESTION, question))
            self.assertEqual(question['status'], 'blocked')
            self.assertTrue(question['blockedDecisions'])


if __name__ == '__main__':
    unittest.main()
