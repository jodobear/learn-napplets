"""Evidence-record validation tests for the Phase 1 source tracer."""

from __future__ import annotations

import copy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-research.py"
SOURCE_SCHEMA = ROOT / ".planning" / "research" / "schemas" / "source.schema.json"
CLAIM_SCHEMA = ROOT / ".planning" / "research" / "schemas" / "claim.schema.json"

VALID_SOURCE = {
    "id": "SRC-POLICY-001",
    "kind": "source",
    "collectionStatus": "seed",
    "rawOrigin": "project-policy",
    "repository": "learn-napplets",
    "officialUrl": "https://example.invalid/learn-napplets",
    "immutableUrl": "https://example.invalid/learn-napplets/blob/0123456789abcdef0123456789abcdef01234567/.planning/governance/evidence-policy.md",
    "ref": "0123456789abcdef0123456789abcdef01234567",
    "commitSha": "0123456789abcdef0123456789abcdef01234567",
    "path": ".planning/governance/evidence-policy.md",
    "locator": "Required fields",
    "contentSha256": "a" * 64,
    "retrievedAt": "2026-07-24T00:00:00Z",
    "authorityTier": "project-policy",
    "evidenceClass": "project-policy",
    "maturity": "accepted",
    "uncertainty": {"state": "limited", "reason": "Collection seed; not upstream proof."},
    "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
    "freshness": {"state": "provisional", "refreshTrigger": "Policy revision or digest change"},
    "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]},
}


class SourceEvidenceTests(unittest.TestCase):
    def run_validator(self, research_root: Path, report: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "validate", "--root", str(research_root), "--report", str(report)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_root(self, record: dict, duplicate: bool = False) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "research"
        (root / "schemas").mkdir(parents=True)
        shutil.copy2(SOURCE_SCHEMA, root / "schemas" / "source.schema.json")
        records = [record, copy.deepcopy(record)] if duplicate else [record]
        if duplicate:
            records[1]["id"] = record["id"]
        (root / "source-registry.yaml").write_text(
            "schemaVersion: 1\nsources:\n" + "".join(
                "  - " + "\n    ".join(f"{key}: {value}" for key, value in item.items()) + "\n"
                for item in records
            )
        )
        return root, temp

    def test_complete_source_record_produces_deterministic_review_report(self) -> None:
        root, temp = self.write_root(copy.deepcopy(VALID_SOURCE))
        with temp:
            report = root / "reports" / "validation.md"
            result = self.run_validator(root, report)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("SRC-POLICY-001", report.read_text())
            self.assertIn("valid", report.read_text())

    def test_incomplete_source_record_is_rejected(self) -> None:
        record = copy.deepcopy(VALID_SOURCE)
        del record["commitSha"]
        root, temp = self.write_root(record)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("commitSha", result.stdout)

    def test_duplicate_stable_ids_are_rejected(self) -> None:
        root, temp = self.write_root(copy.deepcopy(VALID_SOURCE), duplicate=True)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ERROR SEM001: duplicate record ID SRC-POLICY-001", result.stdout)

    def test_traceability_mappings_resolve_to_pinned_archive_files(self) -> None:
        report = ROOT / ".planning" / "research" / "reports" / "validation.md"
        result = self.run_validator(ROOT / ".planning" / "research", report)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("Traceability mappings: valid", report.read_text())

    def write_claim_root(self, claim: dict) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
        root, temp = self.write_root(copy.deepcopy(VALID_SOURCE))
        shutil.copy2(CLAIM_SCHEMA, root / "schemas" / "claim.schema.json")
        (root / "claims.yaml").write_text("schemaVersion: 1\nclaims:\n  - " + "\n    ".join(
            f"{key}: {value}" for key, value in claim.items()
        ) + "\n")
        return root, temp

    def test_valid_source_linked_provisional_claim_passes(self) -> None:
        claim = {
            "id": "CLM-POLICY-001", "kind": "claim", "statement": "A project-policy seed requires review.",
            "rawOrigin": "project-policy", "assertionKind": "project-policy", "evidenceClass": "project-policy",
            "maturity": "accepted", "state": "provisional", "stateReason": "Awaiting technical review.",
            "uncertainty": {"state": "limited", "reason": "Policy seed."},
            "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
            "sourceRelations": [{"sourceId": "SRC-POLICY-001", "relation": "supports", "role": "primary", "locator": "Required fields", "excerptSha256": "b" * 64}],
            "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]}, "blocking": False,
        }
        root, temp = self.write_claim_root(claim)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_blocking_claim_requires_distinct_corroboration(self) -> None:
        claim = {
            "id": "CLM-POLICY-003", "kind": "claim", "statement": "Blocking evidence requires independent corroboration.",
            "rawOrigin": "project-policy", "assertionKind": "project-policy", "evidenceClass": "project-policy",
            "maturity": "accepted", "state": "blocked", "stateReason": "Corroboration is unavailable.",
            "uncertainty": {"state": "material", "reason": "One source only."}, "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
            "sourceRelations": [
                {"sourceId": "SRC-POLICY-001", "relation": "supports", "role": "primary", "locator": "Required fields", "excerptSha256": "b" * 64},
                {"sourceId": "SRC-POLICY-001", "relation": "supports", "role": "independent-corroboration", "locator": "Required fields", "excerptSha256": "b" * 64},
            ],
            "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]}, "blocking": True,
            "blockedDetails": {"scope": "This claim only.", "safeFallback": "Defer it.", "approver": "project-owner", "date": "2026-07-24", "revisitCriterion": "A distinct source is available."},
        }
        root, temp = self.write_claim_root(claim)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires distinct primary and independent corroborating sources", result.stdout)

    def test_claim_semantic_failures_are_rejected(self) -> None:
        claim = {
            "id": "CLM-POLICY-002", "kind": "claim", "statement": "An invalid claim must be rejected.",
            "rawOrigin": "inference", "assertionKind": "inference", "evidenceClass": "inference", "maturity": "unknown",
            "state": "verified", "stateReason": "Automation-only transition.",
            "uncertainty": {"state": "material", "reason": "No review."}, "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
            "sourceRelations": [{"sourceId": "SRC-MISSING-001", "relation": "invented", "role": "primary", "locator": "none", "excerptSha256": "b" * 64}],
            "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]}, "blocking": False,
        }
        root, temp = self.write_claim_root(claim)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("references unknown source SRC-MISSING-001", result.stdout)
            self.assertIn("cannot be verified without reviewer approval evidence", result.stdout)


if __name__ == "__main__":
    unittest.main()
