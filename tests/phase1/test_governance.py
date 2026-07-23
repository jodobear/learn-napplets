"""Report, governance, lesson-index, and ADR contract tests."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-research.py"
HEADINGS = [
    "Research question", "Sources and immutable revisions", "Observations", "Conflicts", "Inference",
    "Prototype or measurement", "Recommendation", "Uncertainty", "Affected phases and requirements",
    "Owner and required approval",
]
GOVERNANCE = {
    "schemaVersion": 1,
    "id": "PGV-PHASE-001",
    "kind": "phase-governance",
    "phase": "01",
    "owner": "research-owner",
    "requiredApprover": "protocol-technical-owner",
    "requirements": ["OPER-03"],
    "exitEvidence": [{"id": "SPK-TEST-001", "measure": "replay result", "expected": "blocked", "actual": "blocked", "path": "spikes/spk-test-001/report.md"}],
    "verification": {"gsdState": "passed", "validatedAt": "2026-07-24T00:00:00Z", "validator": "validate-research"},
    "approval": {"status": "pending"},
    "phaseResult": "blocked",
}


def report_text(spike_id: str | None = None) -> str:
    sections = [f"## {heading}\n\nEvidence for {heading}." for heading in HEADINGS]
    if spike_id:
        sections[-1] += f"\n\nSPK ID: {spike_id}\nMetadata path: metadata.yaml"
    return "# Report\n\n" + "\n\n".join(sections) + "\n"


class GovernanceValidationTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(VALIDATOR), *args], cwd=ROOT, text=True, capture_output=True, check=False)

    def test_governance_requires_roles_requirements_exit_evidence_and_validation_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "governance.yaml"
            path.write_text(yaml.safe_dump(GOVERNANCE), encoding="utf-8")
            self.assertEqual(self.run_cli("validate-governance", str(path)).returncode, 0)
            for key in ("owner", "requiredApprover", "requirements", "exitEvidence", "verification"):
                with self.subTest(key=key):
                    record = copy.deepcopy(GOVERNANCE)
                    del record[key]
                    path.write_text(yaml.safe_dump(record), encoding="utf-8")
                    result = self.run_cli("validate-governance", str(path))
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(key, result.stdout)

    def test_report_requires_each_canonical_h2_heading_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "research-report.md"
            path.write_text(report_text(), encoding="utf-8")
            self.assertEqual(self.run_cli("validate-report", str(path)).returncode, 0)
            for heading in HEADINGS:
                with self.subTest(heading=heading):
                    path.write_text(report_text().replace(f"## {heading}", "# Removed heading"), encoding="utf-8")
                    result = self.run_cli("validate-report", str(path))
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(heading, result.stdout)

    def test_spike_report_rejects_mismatched_declared_and_metadata_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "spk-test-001"
            directory.mkdir()
            (directory / "metadata.yaml").write_text("id: SPK-OTHER-001\n", encoding="utf-8")
            report = directory / "report.md"
            report.write_text(report_text("SPK-TEST-001"), encoding="utf-8")
            result = self.run_cli("validate-report", str(report))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ERROR RPT005", result.stdout)

    def test_lesson_index_rejects_duplicate_ids_filename_mismatch_and_bad_required_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            packets = root / "packets"
            packets.mkdir()
            (packets / "LES-001.md").write_text("# Lesson 1\n", encoding="utf-8")
            index = root / "index.yaml"
            index.write_text(yaml.safe_dump({"lessons": [{"id": "LES-001", "filename": "LES-001.md"}]}), encoding="utf-8")
            self.assertEqual(self.run_cli("validate-lessons", "--index", str(index), "--required-present", "1").returncode, 0)
            index.write_text(yaml.safe_dump({"lessons": [{"id": "LES-001", "filename": "LES-001.md"}, {"id": "LES-001", "filename": "wrong.md"}]}), encoding="utf-8")
            result = self.run_cli("validate-lessons", "--index", str(index), "--required-present", "1")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate", result.stdout)
            index.write_text(yaml.safe_dump({"lessons": [{"id": "LES-001", "filename": "wrong.md"}]}), encoding="utf-8")
            result = self.run_cli("validate-lessons", "--index", str(index), "--required-present", "2")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("filename", result.stdout)

    def test_breaking_schema_change_requires_versioned_deterministic_migration_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "migration.md"
            path.write_text("Schema: spike.schema.json\nVersion: 1 -> 2\n", encoding="utf-8")
            result = self.run_cli("validate-migration", str(path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Deterministic migration", result.stdout)

    def test_adr_requires_proposed_status_and_resolvable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "ADR-0001.md"
            path.write_text("# ADR 0001\n\nStatus: accepted\n", encoding="utf-8")
            result = self.run_cli("validate-adr", str(path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Status: proposed", result.stdout)


if __name__ == "__main__":
    unittest.main()
