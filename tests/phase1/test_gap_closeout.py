"""Executable Nyquist edge probes for Phase 1 closeout evidence."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
PLANNING = ROOT / ".planning"
VALIDATOR = ROOT / "tools" / "validate-research.py"
DIMENSIONS = (
    "normativeProtocol",
    "observedImplementation",
    "publishedPackage",
    "runtime",
    "exampleFixture",
    "currentWork",
    "conformance",
)


def load_research_validator():
    spec = importlib.util.spec_from_file_location("phase1_gap_closeout_validator", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def complete_governance() -> dict:
    signoffs = {
        name: {"status": "pending"}
        for name in ("product", "protocolTechnical", "security", "accessibility", "contentLearning", "release")
    }
    return {
        "schemaVersion": 1,
        "id": "PGV-GAP-CLOSEOUT-001",
        "kind": "phase-governance",
        "phase": "01",
        "owner": "research-owner",
        "requiredApprover": "protocol-technical-owner",
        "requirements": ["OPER-03", "EVID-03"],
        "exitEvidence": [
            {
                "id": "SPK-GAP-CLOSEOUT-001",
                "measure": "retained local fixture",
                "expected": "blocked or complete evidence",
                "actual": "fixture retained",
                "path": ".planning/spikes/spk-a-workspace/report.md",
            }
        ],
        "verification": {
            "gsdState": "blocked",
            "validatedAt": "2026-07-31T00:00:00Z",
            "validator": "tools/validate-research.py validate-governance",
        },
        "approval": {"status": "pending"},
        "signoffs": signoffs,
        "authorityDeterminations": [
            {
                "scopeId": "CAND-GAP-CLOSEOUT-001",
                "candidateId": "CAND-GAP-CLOSEOUT-001",
                "authorityArtifactPath": ".planning/research/authority-determinations.yaml",
                "authorityArtifactSha256": "a" * 64,
                "acquisitionReceiptPath": ".planning/research/reports/upstream-acquisition-20260728.md",
                "acquisitionReceiptSha256": "b" * 64,
                "determinationIds": [
                    "AUTH-GAP-PRODUCT",
                    "AUTH-GAP-PROTOCOL",
                    "AUTH-GAP-SECURITY",
                    "AUTH-GAP-ACCESSIBILITY",
                    "AUTH-GAP-CONTENT",
                    "AUTH-GAP-RELEASE",
                ],
                "reviewedSourceInputBinding": {"parserVersion": "fixture-v1"},
            }
        ],
        "blockers": [],
        "phaseResult": "blocked",
    }


class GapCloseoutTests(unittest.TestCase):
    def compatibility_snapshot(self, validator) -> dict[str, bytes]:
        return {
            relative: (PLANNING / relative).read_bytes()
            for relative in validator.COMPATIBILITY_SNAPSHOT_TARGETS
        }

    def qualified_compatibility_snapshot(self, validator) -> dict[str, bytes]:
        snapshot = self.compatibility_snapshot(validator)
        registry = yaml.safe_load(snapshot["research/source-registry.yaml"])
        matrix = yaml.safe_load(snapshot["research/compatibility-matrix.yaml"])
        sources = registry["sources"]
        dimension_sources = {
            "normativeProtocol": ("SRC-NORMATIVE-QUALIFIED", "normative-protocol", "official-normative"),
            "observedImplementation": ("SRC-OBSERVED-QUALIFIED", "observed-implementation", "official-repository-observation"),
            "runtime": ("SRC-RUNTIME-QUALIFIED", "runtime-measurement", "independent-runtime-measurement"),
            "exampleFixture": ("SRC-FIXTURE-QUALIFIED", "example-fixture", "reproducible-fixture"),
            "currentWork": ("SRC-CURRENT-WORK-QUALIFIED", "observed-implementation", "official-repository-observation"),
        }
        for source_id, raw_origin, authority_tier in dimension_sources.values():
            sources.append(
                {
                    "id": source_id,
                    "collectionStatus": "collected",
                    "rawOrigin": raw_origin,
                    "authorityTier": authority_tier,
                    "review": {"status": "approved"},
                    "freshness": {"state": "current"},
                }
            )
        baseline = next(record for record in matrix["compatibility"] if record["id"] == "CMP-BASELINE-001")
        for dimension in baseline["dimensions"]:
            dimension["status"] = "qualified"
            if dimension["name"] in dimension_sources:
                dimension["references"] = [{"id": dimension_sources[dimension["name"]][0]}]
            elif dimension["name"] == "publishedPackage":
                dimension["references"] = [{"id": "SRC-NORMATIVE-QUALIFIED"}]
            elif dimension["name"] == "conformance":
                dimension["references"] = [{"id": "SRC-OBSERVED-QUALIFIED"}]
        baseline["baselineEligibility"] = {
            "status": "eligible",
            "approval": "approved",
            "reviewRecordId": "APR-GAP-CLOSEOUT-001",
        }
        package = yaml.safe_load(snapshot["research/package-evidence.yaml"])
        package["approval"] = "approved"
        package["artifactEvidence"] = {"status": "qualified"}
        metadata = yaml.safe_load(snapshot["spikes/spk-g-package-conformance/metadata.yaml"])
        metadata["status"] = "complete"
        snapshot["research/source-registry.yaml"] = yaml.safe_dump(registry, sort_keys=False).encode("utf-8")
        snapshot["research/compatibility-matrix.yaml"] = yaml.safe_dump(matrix, sort_keys=False).encode("utf-8")
        snapshot["research/package-evidence.yaml"] = yaml.safe_dump(package, sort_keys=False).encode("utf-8")
        snapshot["spikes/spk-g-package-conformance/metadata.yaml"] = yaml.safe_dump(metadata, sort_keys=False).encode("utf-8")
        snapshot["spikes/spk-g-package-conformance/report.md"] = b"# Conformance fixture\n"
        return snapshot

    def test_compatibility_completeness_requires_qualified_dimensions_without_approval(self) -> None:
        validator = load_research_validator()
        complete = self.qualified_compatibility_snapshot(validator)
        qualified = validator.evaluate_compatibility_baseline(
            validator.build_compatibility_snapshot_index(complete)
        )
        self.assertEqual(qualified["status"], "eligible")
        self.assertEqual(qualified["approval"], "approved")
        self.assertFalse(qualified["architectureApproved"])

        for dimension_name in DIMENSIONS:
            with self.subTest(dimension=dimension_name):
                mutated = dict(complete)
                matrix = yaml.safe_load(mutated["research/compatibility-matrix.yaml"])
                baseline = matrix["compatibility"][0]
                dimension = next(item for item in baseline["dimensions"] if item["name"] == dimension_name)
                if dimension_name == "publishedPackage":
                    package = yaml.safe_load(mutated["research/package-evidence.yaml"])
                    package["artifactEvidence"] = {"status": "blocked"}
                    mutated["research/package-evidence.yaml"] = yaml.safe_dump(package, sort_keys=False).encode("utf-8")
                elif dimension_name == "conformance":
                    metadata = yaml.safe_load(mutated["spikes/spk-g-package-conformance/metadata.yaml"])
                    metadata["status"] = "blocked"
                    mutated["spikes/spk-g-package-conformance/metadata.yaml"] = yaml.safe_dump(metadata, sort_keys=False).encode("utf-8")
                else:
                    dimension["references"] = []
                mutated["research/compatibility-matrix.yaml"] = yaml.safe_dump(matrix, sort_keys=False).encode("utf-8")
                result = validator.evaluate_compatibility_baseline(
                    validator.build_compatibility_snapshot_index(mutated)
                )
                token = validator.dimension_reason_token(dimension_name)
                self.assertEqual(result["status"], "blocked")
                self.assertEqual(result["approval"], "not-approved")
                self.assertFalse(result["architectureApproved"])
                self.assertTrue(
                    any(reason.startswith(f"DIMENSION_{token}_") for reason in result["reasons"]),
                    result,
                )

    def test_mandatory_spike_completeness_requires_retained_evidence_without_approval(self) -> None:
        validator = load_research_validator()
        manifest = yaml.safe_load((PLANNING / "spikes/replay-manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual([entry["spikeId"] for entry in manifest["entries"]], [f"SPK-{letter}" for letter in "ABCDEFGHIJKL"])
        with tempfile.TemporaryDirectory() as temporary:
            copied_planning = Path(temporary) / ".planning"
            copied_spikes = copied_planning / "spikes"
            copied_spikes.mkdir(parents=True)
            copied_manifest = copied_spikes / "replay-manifest.yaml"
            copied_manifest.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
            for entry in manifest["entries"]:
                source_directory = PLANNING / entry["report"]["path"]
                source_directory = source_directory.parent
                shutil.copytree(source_directory, copied_spikes / source_directory.name)
                for evidence_name in ("report", "metadata", "measurement"):
                    evidence = entry[evidence_name]
                    retained = copied_planning / evidence["path"]
                    self.assertTrue(retained.is_file(), evidence)
                metadata = yaml.safe_load((copied_spikes / source_directory.name / "metadata.yaml").read_text(encoding="utf-8"))
                self.assertTrue(metadata.get("rawOutputDigests"), entry["spikeId"])
                self.assertTrue(metadata.get("evidenceLinks"), entry["spikeId"])
                self.assertTrue(metadata.get("replayResult", {}).get("outputDigest"), entry["spikeId"])
                self.assertEqual(
                    validator.validate_spike(copied_spikes / source_directory.name, "complete"),
                    [],
                    entry["spikeId"],
                )
            self.assertEqual(validator.validate_replay_manifest(copied_manifest, copied_planning), [])
            mutated = yaml.safe_load(copied_manifest.read_text(encoding="utf-8"))
            mutated["entries"][0]["report"]["sha256"] = "0" * 64
            copied_manifest.write_text(yaml.safe_dump(mutated, sort_keys=False), encoding="utf-8")
            errors = validator.validate_replay_manifest(copied_manifest, copied_planning)
            self.assertEqual(len(errors), 2, errors)
            self.assertTrue(errors[0].startswith("ERROR RPL005: SPK-A report"), errors)
            self.assertTrue(errors[1].startswith("ERROR RPL007: SPK-A fixture evidence"), errors)
            self.assertNotIn("approved", " ".join(errors).lower())

    def test_governance_role_adjacency_requires_independence(self) -> None:
        validator = load_research_validator()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "governance.yaml"
            independent = complete_governance()
            path.write_text(yaml.safe_dump(independent, sort_keys=False), encoding="utf-8")
            self.assertEqual(validator.validate_governance(path), [])
            aliased = copy.deepcopy(independent)
            aliased["requiredApprover"] = aliased["owner"]
            path.write_text(yaml.safe_dump(aliased, sort_keys=False), encoding="utf-8")
            self.assertEqual(
                validator.validate_governance(path),
                ["ERROR GOV003: responsible owner and required approver must be separate roles"],
            )

    def test_governance_empty_null_single_required_fields_fail(self) -> None:
        validator = load_research_validator()
        cases = {
            "empty-owner": lambda record: record.__setitem__("owner", ""),
            "null-approver": lambda record: record.__setitem__("requiredApprover", None),
            "empty-requirements": lambda record: record.__setitem__("requirements", []),
            "null-exit-evidence": lambda record: record.__setitem__("exitEvidence", None),
            "single-signoff": lambda record: record.__setitem__("signoffs", {"product": {"status": "pending"}}),
            "single-exit-field": lambda record: record.__setitem__("exitEvidence", [{"id": "SPK-GAP-CLOSEOUT-001"}]),
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "governance.yaml"
            for name, mutate in cases.items():
                with self.subTest(name=name):
                    record = complete_governance()
                    mutate(record)
                    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
                    errors = validator.validate_governance(path)
                    self.assertTrue(errors, name)
                    self.assertTrue(all(error.startswith("ERROR ") for error in errors), errors)

    def test_governance_ordering_is_stable(self) -> None:
        validator = load_research_validator()
        expected = ["ERROR GOV003: responsible owner and required approver must be separate roles"]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "governance.yaml"
            for requirements in (("EVID-03", "OPER-03"), ("OPER-03", "EVID-03")):
                for signoff_names in (
                    ("product", "protocolTechnical", "security", "accessibility", "contentLearning", "release"),
                    ("release", "contentLearning", "accessibility", "security", "protocolTechnical", "product"),
                ):
                    record = complete_governance()
                    record["requirements"] = list(requirements)
                    record["signoffs"] = {name: {"status": "pending"} for name in signoff_names}
                    record["requiredApprover"] = record["owner"]
                    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
                    self.assertEqual(validator.validate_governance(path), expected)


if __name__ == "__main__":
    unittest.main()
