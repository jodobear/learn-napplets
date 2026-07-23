import copy
import json
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
RECORD={'id':'CMP-POLICY-001','kind':'compatibility','sourceBaseline':[PIN],'packages':['PKG-POLICY-001'],'runtimes':['RUN-POLICY-001'],'examples':['EXM-POLICY-001'],'fixtures':['FIX-POLICY-001'],'knownDrift':['DRF-POLICY-001'],'testEvidence':['TST-POLICY-001'],'observedAt':'2026-07-24T00:00:00Z','releaseState':PIN,'currentWork':copy.deepcopy(PIN)}


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


if __name__=='__main__':
    unittest.main()
