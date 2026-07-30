"""Report, governance, lesson-index, and ADR contract tests."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-research.py"
EXECUTOR_ID = "claude-code/gpt-5.6-sol:phase1-orchestrated-executor"
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
    "signoffs": {
        "product": {"status": "pending"},
        "protocolTechnical": {"status": "pending"},
        "security": {"status": "pending"},
        "accessibility": {"status": "pending"},
        "contentLearning": {"status": "pending"},
        "release": {"status": "pending"},
    },
    "blockers": [],
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

    def run_planning_gate(self) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, "GSD_EXECUTOR_ID": EXECUTOR_ID}
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate-planning.py"),
                "--phase-1-complete",
                "--executor-identity",
                EXECUTOR_ID,
            ],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_phase_one_closeout_requires_governance_and_complete_evidence_contract(self) -> None:
        governance = ROOT / ".planning/research/phase-governance.yaml"
        self.assertTrue(governance.is_file(), "Phase closeout needs a governance record")
        result = self.run_planning_gate()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_phase_one_governance_requires_all_distinct_role_signoff_slots(self) -> None:
        record = copy.deepcopy(GOVERNANCE)
        record["signoffs"] = {
            "product": {"status": "pending"},
            "protocolTechnical": {"status": "pending"},
            "security": {"status": "pending"},
            "accessibility": {"status": "pending"},
            "contentLearning": {"status": "pending"},
            "release": {"status": "pending"},
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "governance.yaml"
            path.write_text(yaml.safe_dump(record), encoding="utf-8")
            self.assertEqual(self.run_cli("validate-governance", str(path)).returncode, 0)
            for role in tuple(record["signoffs"]):
                with self.subTest(role=role):
                    incomplete = copy.deepcopy(record)
                    del incomplete["signoffs"][role]
                    path.write_text(yaml.safe_dump(incomplete), encoding="utf-8")
                    result = self.run_cli("validate-governance", str(path))
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("signoffs", result.stdout)

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

    def test_lesson_index_validates_staged_inventory_and_present_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            packets = root / "packets"
            packets.mkdir()
            (packets / "01-nostr-client-taken-apart.md").write_text("# Lesson 1\n", encoding="utf-8")
            index = root / "index.yaml"
            index.write_text(yaml.safe_dump({"lessons": [
                {"id": "LES-001", "filename": "01-nostr-client-taken-apart.md", "status": "present"},
                {"id": "LES-002", "filename": "02-cast-and-mental-model.md", "status": "planned"},
            ]}), encoding="utf-8")
            self.assertEqual(self.run_cli("validate-lessons", "--index", str(index), "--required-present", "1").returncode, 0)
            index.write_text(yaml.safe_dump({"lessons": [{"id": "LES-001", "filename": "01-nostr-client-taken-apart.md"}, {"id": "LES-001", "filename": "wrong.md"}]}), encoding="utf-8")
            result = self.run_cli("validate-lessons", "--index", str(index), "--required-present", "1")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate", result.stdout)
            index.write_text(yaml.safe_dump({"lessons": [{"id": "LES-001", "filename": "wrong.md", "status": "unknown"}]}), encoding="utf-8")
            result = self.run_cli("validate-lessons", "--index", str(index), "--required-present", "2")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("status", result.stdout)

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


    def test_authority_determination_requires_current_complete_scope(self) -> None:
        import importlib.util

        collector_path = ROOT / "tools" / "acquire-sources.py"
        spec = importlib.util.spec_from_file_location("phase1_governance_collector", collector_path)
        collector = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(collector)
        determinations_path = ROOT / ".planning/research/authority-determinations.yaml"
        receipt_path = ROOT / ".planning/research/authority-determinations.receipt.yaml"
        acquisition_path = ROOT / ".planning/research/reports/upstream-acquisition-20260728.md"
        determinations = yaml.safe_load(determinations_path.read_text(encoding="utf-8"))
        receipt = yaml.safe_load(receipt_path.read_text(encoding="utf-8"))
        acquisition_digest = hashlib.sha256(acquisition_path.read_bytes()).hexdigest()
        scope_id = determinations["scopeIds"][0]

        accepted = collector.require_current_authority_determinations(
            determinations,
            receipt,
            hashlib.sha256(determinations_path.read_bytes()).hexdigest(),
            acquisition_digest,
            scope_id,
        )
        self.assertEqual(accepted["scopeId"], scope_id)

        for mutation, diagnostic in (
            (lambda document: document["authorityDeterminations"][0]["determinations"].pop(), "exactly six"),
            (lambda document: document["authorityDeterminations"][0]["determinations"].__setitem__(1, copy.deepcopy(document["authorityDeterminations"][0]["determinations"][0])), "duplicate"),
            (lambda document: document["authorityDeterminations"][0].__setitem__("scopeId", "CAND-OTHER-SCOPE"), "scope"),
        ):
            with self.subTest(diagnostic=diagnostic):
                malformed = copy.deepcopy(determinations)
                mutation(malformed)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    collector.require_current_authority_determinations(
                        malformed,
                        receipt,
                        hashlib.sha256(determinations_path.read_bytes()).hexdigest(),
                        acquisition_digest,
                        scope_id,
                    )

    def test_validate_governance_receipt_binding(self) -> None:
        collector = ROOT / "tools" / "acquire-sources.py"
        determinations = ROOT / ".planning/research/authority-determinations.yaml"
        receipt = ROOT / ".planning/research/authority-determinations.receipt.yaml"
        command = [sys.executable, str(collector), "validate-authority-receipt", "--determinations", str(determinations), "--receipt"]
        accepted = subprocess.run(command + [str(receipt)], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(accepted.returncode, 0, accepted.stderr + accepted.stdout)
        self.assertIn("authority receipt binding passed", accepted.stdout)

        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            copied_determinations = directory / "authority-determinations.yaml"
            copied_receipt = directory / "authority-determinations.receipt.yaml"
            copied_determinations.write_bytes(determinations.read_bytes())
            copied_receipt.write_bytes(receipt.read_bytes())
            missing = subprocess.run(command[:5] + [str(copied_determinations), "--receipt", str(directory / "missing.yaml")], cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertNotEqual(missing.returncode, 0)
            copied_receipt.write_text("not: [valid", encoding="utf-8")
            malformed = subprocess.run(command[:5] + [str(copied_determinations), "--receipt", str(copied_receipt)], cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertNotEqual(malformed.returncode, 0)
            copied_receipt.write_bytes(receipt.read_bytes())
            copied_determinations.write_text(copied_determinations.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            altered = subprocess.run(command[:5] + [str(copied_determinations), "--receipt", str(copied_receipt)], cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertNotEqual(altered.returncode, 0)
            copied_determinations.write_bytes(determinations.read_bytes())
            copied_receipt.write_text(copied_receipt.read_text(encoding="utf-8").replace("acquisitionReceiptSha256: 9b4c", "acquisitionReceiptSha256: 0b4c"), encoding="utf-8")
            changed_digest = subprocess.run(command[:5] + [str(copied_determinations), "--receipt", str(copied_receipt)], cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertNotEqual(changed_digest.returncode, 0)
            copied_receipt.write_text(receipt.read_text(encoding="utf-8").replace("CAND-SRC-KEHTO-WEB-PR204-20260728", "CAND-SRC-OTHER-001", 1), encoding="utf-8")
            scope_mismatch = subprocess.run(command[:5] + [str(copied_determinations), "--receipt", str(copied_receipt)], cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertNotEqual(scope_mismatch.returncode, 0)


if __name__ == "__main__":
    unittest.main()
