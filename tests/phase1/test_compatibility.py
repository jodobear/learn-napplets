import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
SCHEMA=ROOT/'.planning/research/schemas/compatibility.schema.json'
SHA='a'*64; COMMIT='0'*40
PIN={'sourceId':'SRC-POLICY-001','commitSha':COMMIT,'path':'policy.md','contentSha256':SHA}
RECORD={'id':'CMP-POLICY-001','kind':'compatibility','sourceBaseline':[PIN],'packages':['PKG-POLICY-001'],'runtimes':['RUN-POLICY-001'],'examples':['EXM-POLICY-001'],'fixtures':['FIX-POLICY-001'],'knownDrift':['DRF-POLICY-001'],'testEvidence':['TST-POLICY-001'],'observedAt':'2026-07-24T00:00:00Z','releaseState':PIN,'currentWork':copy.deepcopy(PIN)}
class CompatibilitySchema(unittest.TestCase):
 def test_requires_pinned_release_and_current_work_baselines(self):
  validator=Draft202012Validator(json.loads(SCHEMA.read_text()))
  self.assertFalse(list(validator.iter_errors(RECORD)))
  bad=copy.deepcopy(RECORD); bad['currentWork']['commitSha']=''; self.assertTrue(list(validator.iter_errors(bad)))
if __name__=='__main__': unittest.main()
