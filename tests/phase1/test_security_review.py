"""ASVS L1 security-review policy and regression tests for Phase 1."""

from __future__ import annotations

import copy
import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / ".planning" / "config.json"
REFERENCE = ROOT / ".planning" / "research" / "reports" / "asvs-reference-20260728.md"
MATRIX = ROOT / ".planning" / "research" / "reports" / "asvs-5.0.0-l1-applicability.yaml"
VALIDATOR = ROOT / "tools" / "validate-phase1-security.py"
REQUIRED_FINDING_IDS = tuple([f"CR-{number:02d}" for number in range(1, 10)] + [f"WR-{number:02d}" for number in range(1, 4)])


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def base_matrix() -> dict:
    """Return a self-contained complete miniature matrix for validator rejection tests.

    Production data must list the complete official catalog; fixture controls model the
    required CR/WR mapping and are not ASVS authority.
    """
    controls = []
    for number, finding_id in enumerate(REQUIRED_FINDING_IDS, start=1):
        control_id = f"v5.0.0-TEST-L1-{number:02d}"
        controls.append(
            {
                "id": control_id,
                "source": {"path": "5.0/en/test.md", "sha256": "a" * 64},
                "applicability": "applicable",
                "rationale": "Fixture control bound to a required remediation finding.",
                "verification_status": "passed",
                "command_or_evidence": "fixture command",
                "observed_result": "fixture passed",
                "linked_references": [finding_id],
            }
        )
    return {
        "asvs_version": "5.0.0",
        "level": "L1",
        "catalog_requirement_ids": [item["id"] for item in controls],
        "controls": controls,
    }


def base_evidence() -> dict:
    return {
        "reviewed_commit": "b" * 40,
        "active_plan_manifest_sha256": "c" * 64,
        "evidence_manifest_sha256": "d" * 64,
        "asvs_reference_sha256": "e" * 64,
        "findings": [
            {
                "id": finding_id,
                "threat": "tampering",
                "severity": "high",
                "primary_coverage": "remediation",
                "disposition": "mitigated",
                "command": f"fixture verify {finding_id}",
                "result": "exit 0",
                "source_path": f"tools/{finding_id.lower()}.py",
                "applicable_asvs_ids": [f"v5.0.0-TEST-L1-{index:02d}"],
            }
            for index, finding_id in enumerate(REQUIRED_FINDING_IDS, start=1)
        ],
    }


def passing_review(evidence: dict) -> dict:
    common = {
        "principal": "independent-human@example.test",
        "reviewed_commit": evidence["reviewed_commit"],
        "reviewed_plan_manifest_sha256": evidence["active_plan_manifest_sha256"],
        "reviewed_evidence_manifest_sha256": evidence["evidence_manifest_sha256"],
        "asvs_reference_sha256": evidence["asvs_reference_sha256"],
        "determination": "passed",
        "rationale": "Independent fixture recheck confirms all listed remediations.",
    }
    return {
        "review_date": "2026-07-30",
        "scope": "Phase 1 ASVS L1 remediation review",
        "asvs_level": "L1",
        "blocking_threshold": "high",
        "reviewed_commits": [evidence["reviewed_commit"]],
        "reviewed_plan_manifest_sha256": evidence["active_plan_manifest_sha256"],
        "reviewed_evidence_manifest_sha256": evidence["evidence_manifest_sha256"],
        "status": "passed",
        "open_high_count": 0,
        "securityAuditor": {**common, "role": "securityAuditor", "timestamp": "2026-07-30T12:00:00Z"},
        "securityRechecker": {**common, "role": "securityRechecker", "timestamp": "2026-07-30T12:05:00Z"},
        "findings": copy.deepcopy(evidence["findings"]),
    }


class SecurityReviewTests(unittest.TestCase):
    maxDiff = None

    def run_validator(self, security: dict, evidence: dict, matrix: dict, *, executor: str = "automation@example.test") -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            security_path = workspace / "security.md"
            evidence_path = workspace / "evidence.yaml"
            matrix_path = workspace / "matrix.yaml"
            security_path.write_text("---\n" + yaml.safe_dump(security, sort_keys=False) + "---\n# Fixture security review\n", encoding="utf-8")
            evidence_path.write_text(yaml.safe_dump(evidence, sort_keys=False), encoding="utf-8")
            matrix_path.write_text(yaml.safe_dump(matrix, sort_keys=False), encoding="utf-8")
            environment = {**os.environ, "GSD_EXECUTOR_ID": executor}
            return subprocess.run(
                [
                    str(ROOT / "tools" / "phase1-python"),
                    str(VALIDATOR),
                    "--security", str(security_path),
                    "--evidence", str(evidence_path),
                    "--asvs-matrix", str(matrix_path),
                    "--reviewed-commit", evidence["reviewed_commit"],
                    "--fixture-mode",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )

    def test_asvs_scope_uses_config_and_pinned_official_reference(self) -> None:
        import json

        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(config["workflow"]["security_asvs_level"], 1)
        self.assertEqual(config["workflow"]["security_block_on"], "high")
        reference = REFERENCE.read_text(encoding="utf-8")
        required = {
            "repository: OWASP/ASVS",
            "tag: v5.0.0_release",
            "commit: 5cf9b032440be53ce345ab3c130fda46ba1ce7a2",
            "path: 5.0/en/0x03-What-is-the-ASVS.md",
            "authority: standards-reference",
            "evidence_class:",
            "maturity:",
            "uncertainty:",
            "refresh_trigger:",
            "retrieved_at:",
            "sha256:",
        }
        self.assertTrue(all(token in reference for token in required), reference)

    def test_asvs_l1_applicability_matrix_is_complete_and_finding_bound(self) -> None:
        matrix = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
        self.assertEqual(matrix["asvs_version"], "5.0.0")
        self.assertEqual(matrix["level"], "L1")
        catalog_ids = matrix["catalog_requirement_ids"]
        controls = matrix["controls"]
        self.assertTrue(catalog_ids)
        self.assertEqual(len(catalog_ids), len(set(catalog_ids)))
        self.assertEqual([item["id"] for item in controls], catalog_ids)
        for control in controls:
            self.assertRegex(control["id"], r"^v5\.0\.0-")
            self.assertIn(control["applicability"], {"applicable", "not-applicable", "blocked"})
            self.assertTrue(control["rationale"])
            if control["applicability"] == "applicable":
                for field in ("verification_status", "command_or_evidence", "observed_result", "linked_references"):
                    self.assertTrue(control[field], (control["id"], field))
        mapped = {reference for item in controls for reference in item.get("linked_references", [])}
        self.assertTrue(set(REQUIRED_FINDING_IDS).issubset(mapped))

    def test_asvs_l1_register_requires_required_cr_wr_and_allows_sec_findings(self) -> None:
        evidence = base_evidence()
        matrix = base_matrix()
        review = passing_review(evidence)
        self.assertEqual(self.run_validator(review, evidence, matrix).returncode, 0)
        cases = {
            "missing-required": lambda target: target["findings"].pop(),
            "duplicate-required": lambda target: target["findings"].append(copy.deepcopy(target["findings"][0])),
            "malformed-sec": lambda target: target["findings"].append({**copy.deepcopy(target["findings"][0]), "id": "SEC-invalid"}),
            "blank-finding-cell": lambda target: target["findings"][0].__setitem__("threat", ""),
            "unlinked-sec": lambda target: target["findings"].append({**copy.deepcopy(target["findings"][0]), "id": "SEC-001", "applicable_asvs_ids": []}),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                candidate = copy.deepcopy(review)
                mutate(candidate)
                self.assertNotEqual(self.run_validator(candidate, evidence, matrix).returncode, 0)

    def test_passed_security_review_rejects_unmitigated_high_dispositions(self) -> None:
        evidence = base_evidence()
        matrix = base_matrix()
        review = passing_review(evidence)
        self.assertEqual(self.run_validator(review, evidence, matrix).returncode, 0)
        for mutate in (
            lambda target: target.__setitem__("open_high_count", 1),
            lambda target: target["findings"][0].__setitem__("disposition", "open"),
            lambda target: target["findings"].append({**copy.deepcopy(target["findings"][0]), "id": "SEC-001", "disposition": "open"}),
        ):
            with self.subTest(mutation=mutate):
                candidate = copy.deepcopy(review)
                mutate(candidate)
                self.assertNotEqual(self.run_validator(candidate, evidence, matrix).returncode, 0)

    def test_security_validator_rejects_generic_or_executor_role_reuse(self) -> None:
        evidence = base_evidence()
        matrix = base_matrix()
        review = passing_review(evidence)
        cases = {
            "generic-reuse": lambda target: target.__setitem__("securityRechecker", target["securityAuditor"]),
            "missing-rationale": lambda target: target["securityAuditor"].pop("rationale"),
            "executor-signoff": lambda target: target["securityAuditor"].__setitem__("principal", "executor@example.test"),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                candidate = copy.deepcopy(review)
                mutate(candidate)
                self.assertNotEqual(
                    self.run_validator(candidate, evidence, matrix, executor="executor@example.test").returncode,
                    0,
                )


if __name__ == "__main__":
    unittest.main()
