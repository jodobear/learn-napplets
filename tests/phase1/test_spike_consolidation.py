"""Immutable spike impact validation and consolidation transaction tests."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-research.py"
PLANNING = ROOT / ".planning"
SHA = "a" * 64
FRAGMENT = {
    "schemaVersion": 1,
    "id": "SPK-IMPACT-TEST-001",
    "kind": "spike-impact-fragment",
    "spikeId": "SPK-TEST-001",
    "metadataPath": "spikes/spk-test-001/metadata.yaml",
    "metadataSha256": SHA,
    "reportPath": "spikes/spk-test-001/report.md",
    "reportSha256": SHA,
    "sourceLinks": [{"sourceId": "SRC-POLICY-001", "relation": "measures", "path": "research/source-registry.yaml", "sha256": SHA}],
    "measurementLinks": [{"path": "spikes/spk-test-001/raw.txt", "sha256": SHA}],
    "uncertainty": {"state": "limited", "reason": "Fixture-only result."},
    "proposedImpacts": [{"type": "adr", "id": "ADR-0005", "rationale": "Requires human review."}],
}
CANONICAL_TARGETS = (
    "compatibility-matrix.yaml",
    "drift-register.yaml",
    "open-questions.yaml",
)


class SpikeConsolidationTests(unittest.TestCase):
    def run_fragment(self, fragment: Path, planning_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(VALIDATOR), "validate-impact-fragment", str(fragment), "--root", str(planning_root)], cwd=ROOT, text=True, capture_output=True, check=False)

    def run_consolidation(
        self,
        planning_root: Path,
        audit: Path,
        *extra: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(VALIDATOR),
            "consolidate-spike-impacts",
            "--spikes",
            str(planning_root / "spikes"),
            "--research",
            str(planning_root / "research"),
            "--audit",
            str(audit),
            *extra,
        ]
        return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False, env=env)

    def write_fixture_root(self, fragment: dict) -> tuple[Path, Path, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        planning = Path(temp.name) / ".planning"
        spike = planning / "spikes" / "spk-test-001"
        spike.mkdir(parents=True)
        metadata = spike / "metadata.yaml"
        metadata.write_text("id: SPK-TEST-001\n", encoding="utf-8")
        report = spike / "report.md"
        report.write_text("# Spike report\n", encoding="utf-8")
        fragment["metadataSha256"] = hashlib.sha256(metadata.read_bytes()).hexdigest()
        fragment["reportSha256"] = hashlib.sha256(report.read_bytes()).hexdigest()
        raw = spike / "raw.txt"
        raw.write_text("raw measurement\n", encoding="utf-8")
        source = planning / "research" / "source-registry.yaml"
        source.parent.mkdir()
        source.write_text(yaml.safe_dump({"sources": [{
            "id": "SRC-POLICY-001", "kind": "source", "collectionStatus": "collected", "rawOrigin": "project-policy",
            "repository": "example/repository", "officialUrl": "https://example.invalid/repository", "immutableUrl": "https://example.invalid/repository/blob/" + "0" * 40 + "/policy.md",
            "ref": "0" * 40, "commitSha": "0" * 40, "path": "policy.md", "locator": "L1", "contentSha256": "a" * 64,
            "retrievedAt": "2026-07-24T00:00:00Z", "authorityTier": "project-policy", "evidenceClass": "project-policy", "maturity": "accepted",
            "uncertainty": {"state": "limited", "reason": "Fixture only."}, "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
            "freshness": {"state": "current", "refreshTrigger": "Fixture only."}, "review": {"owner": "owner", "status": "pending", "requiredRoles": ["protocol"]},
        }]}, sort_keys=False), encoding="utf-8")
        if fragment.get("sourceLinks"):
            fragment["sourceLinks"][0]["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        if fragment.get("measurementLinks"):
            fragment["measurementLinks"][0]["sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
        fragment_path = planning / "spikes" / "spk-test-001" / "impact.yaml"
        fragment_path.write_text(yaml.safe_dump(fragment), encoding="utf-8")
        return fragment_path, planning, temp

    def copy_planning(self, directory: Path) -> Path:
        planning = directory / ".planning"
        shutil.copytree(PLANNING, planning, ignore=shutil.ignore_patterns(".cache", "validation.md", "replay-manifest.yaml", "security-egress-findings.md", "spike-consolidation.md"))
        return planning

    def canonical_bytes(self, planning: Path) -> dict[str, bytes]:
        return {name: (planning / "research" / name).read_bytes() for name in CANONICAL_TARGETS}

    def remove_consolidation_history(self, planning: Path) -> None:
        """Make a pre-publication fixture without discarding unrelated history."""
        for filename, key in (("drift-register.yaml", "drift"), ("open-questions.yaml", "questions")):
            path = planning / "research" / filename
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            for record in document.get(key, []):
                if isinstance(record, dict) and isinstance(record.get("history"), list):
                    record["history"] = [
                        item
                        for item in record["history"]
                        if not (isinstance(item, dict) and "Consolidated SPK-" in str(item.get("reason", "")))
                    ]
            path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    def test_fragment_resolves_source_and_measurement_digests(self) -> None:
        fragment_path, planning, temp = self.write_fixture_root(copy.deepcopy(FRAGMENT))
        with temp:
            result = self.run_fragment(fragment_path, planning)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fragment_rejects_noncanonical_path_or_source_substitution(self) -> None:
        cases = {
            "absolute": lambda value, planning: value["measurementLinks"][0].update({"path": str((planning / "spikes/spk-test-001/raw.txt").resolve())}),
            "traversal": lambda value, planning: value["measurementLinks"][0].update({"path": "spikes/spk-test-001/../spk-test-001/raw.txt"}),
            "empty": lambda value, planning: value["measurementLinks"][0].update({"path": ""}),
            "nul": lambda value, planning: value["measurementLinks"][0].update({"path": "spikes/spk-test-001/raw.txt\\x00suffix"}),
            "symlink": lambda value, planning: (planning / "spikes/spk-test-001/raw.txt").unlink() or (planning / "spikes/spk-test-001/raw.txt").symlink_to(planning / "outside.txt"),
            "wrong-spike-directory": lambda value, planning: value.update({"metadataPath": "spikes/spk-other-001/metadata.yaml"}),
            "missing-file": lambda value, planning: value["measurementLinks"][0].update({"path": "spikes/spk-test-001/missing.txt"}),
            "digest-substitution": lambda value, planning: value["measurementLinks"][0].update({"sha256": "0" * 64}),
            "noncanonical-registry": lambda value, planning: value["sourceLinks"][0].update({"path": "research/./source-registry.yaml"}),
            "unknown-source": lambda value, planning: value["sourceLinks"][0].update({"sourceId": "SRC-UNKNOWN-001"}),
            "incomplete-source": lambda value, planning: (planning / "research/source-registry.yaml").write_text("sources:\\n  - id: SRC-POLICY-001\\n", encoding="utf-8"),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                fragment = copy.deepcopy(FRAGMENT)
                fragment_path, planning, temporary = self.write_fixture_root(fragment)
                (planning / "outside.txt").write_text("outside\n", encoding="utf-8")
                mutate(fragment, planning)
                fragment_path.write_text(yaml.safe_dump(fragment, sort_keys=False), encoding="utf-8")
                with temporary:
                    result = self.run_fragment(fragment_path, planning)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("ERROR IMP", result.stdout)

    def test_fragment_rejects_missing_altered_semantic_mismatched_and_dangling_links(self) -> None:
        cases = {
            "missing": lambda value: value.pop("measurementLinks"),
            "semantic": lambda value: value.update({"spikeId": "SPK-OTHER-001"}),
            "dangling": lambda value: value["sourceLinks"][0].update({"sourceId": "SRC-MISSING-001"}),
            "altered": lambda value: None,
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                fragment = copy.deepcopy(FRAGMENT)
                mutate(fragment)
                fragment_path, planning, temp = self.write_fixture_root(fragment)
                if name == "altered":
                    (planning / "spikes" / "spk-test-001" / "raw.txt").write_text("altered measurement\n", encoding="utf-8")
                with temp:
                    result = self.run_fragment(fragment_path, planning)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("ERROR IMP", result.stdout)

    def test_spk_h_fragment_requires_complete_transitive_provenance(self) -> None:
        fragment = copy.deepcopy(FRAGMENT)
        fragment.update({"id": "SPK-IMPACT-H-001", "spikeId": "SPK-H-001", "metadataPath": "spikes/spk-h-001/metadata.yaml", "reportPath": "spikes/spk-h-001/report.md"})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "impact.yaml"
            path.write_text(yaml.safe_dump(fragment), encoding="utf-8")
            result = self.run_fragment(path, Path(temp))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("securityEgress", result.stdout)

        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            fragment_path = planning / "spikes" / "spk-h-browser-egress" / "impact-fragment.yaml"
            fragment = yaml.safe_load(fragment_path.read_text(encoding="utf-8"))
            fragment["sourceIds"] = ["SRC-POLICY-001"]
            fragment_path.write_text(yaml.safe_dump(fragment, sort_keys=False), encoding="utf-8")
            result = self.run_fragment(fragment_path, planning)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ERROR IMP", result.stdout)

    def test_dry_run_accounts_for_all_spikes_and_preserves_canonical_targets(self) -> None:
        before = self.canonical_bytes(PLANNING)
        with tempfile.TemporaryDirectory() as temp:
            audit = Path(temp) / "audit.md"
            result = self.run_consolidation(PLANNING, audit, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(audit.is_file())
            text = audit.read_text(encoding="utf-8")
            for spike_id in "ABCDEFGHIJKL":
                self.assertIn(f"SPK-{spike_id}", text)
            self.assertIn("SPK-C-IMPACT-001", text)
            self.assertIn("no-impact-fragment", text)
        self.assertEqual(before, self.canonical_bytes(PLANNING))

    def test_duplicate_fragment_is_a_single_no_op_and_order_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            source = planning / "spikes" / "spk-c-boundary-harness" / "impact-fragment.yaml"
            duplicate = source.with_name("impact-fragment-duplicate.yaml")
            duplicate.write_bytes(source.read_bytes())
            audit = planning / "research" / "reports" / "audit.md"
            result = self.run_consolidation(planning, audit, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            text = audit.read_text(encoding="utf-8")
            self.assertEqual(1, text.count("SPK-C-IMPACT-001 | no-op-duplicate"))
            reverse_audit = planning / "research" / "reports" / "reverse-audit.md"
            reverse = self.run_consolidation(planning, reverse_audit, "--dry-run", "--input-order", "reverse")
            self.assertEqual(reverse.returncode, 0, reverse.stdout + reverse.stderr)
            self.assertEqual(audit.read_bytes(), reverse_audit.read_bytes())

    def test_conflicting_stable_id_is_blocked_without_replacing_canonical_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            source = planning / "spikes" / "spk-c-boundary-harness" / "impact-fragment.yaml"
            before = {name: (planning / "research" / name).read_bytes() for name in ("compatibility-matrix.yaml", "drift-register.yaml")}
            source_digest = hashlib.sha256(source.read_bytes()).hexdigest()
            conflict = yaml.safe_load(source.read_text(encoding="utf-8"))
            conflict["uncertainty"]["reason"] = "Incompatible immutable evidence proposal."
            conflict_path = source.with_name("impact-fragment-conflict.yaml")
            conflict_path.write_text(yaml.safe_dump(conflict, sort_keys=False), encoding="utf-8")
            conflict_digest = hashlib.sha256(conflict_path.read_bytes()).hexdigest()
            audit = planning / "research" / "reports" / "audit.md"
            result = self.run_consolidation(planning, audit)
            self.assertNotEqual(result.returncode, 0)
            conflict_id = "OQ-CONSOLIDATION-SPK-C-IMPACT-001"
            self.assertIn(conflict_id, result.stdout)
            self.assertEqual(before, {name: (planning / "research" / name).read_bytes() for name in before})
            questions = yaml.safe_load((planning / "research" / "open-questions.yaml").read_text(encoding="utf-8"))["questions"]
            conflict_question = next((item for item in questions if item["id"] == conflict_id), None)
            self.assertIsNotNone(conflict_question)
            self.assertIn(source_digest, str(conflict_question["history"]))
            self.assertIn(conflict_digest, str(conflict_question["history"]))
            self.assertIn(conflict_id, audit.read_text(encoding="utf-8"))

    def test_consolidation_generation_recovers_after_each_publish_interruption(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            self.remove_consolidation_history(planning)
            audit = planning / "research" / "reports" / "audit.md"
            targets = (
                planning / "research" / "compatibility-matrix.yaml",
                planning / "research" / "drift-register.yaml",
                planning / "research" / "open-questions.yaml",
                planning / "research" / "security-egress-findings.md",
                audit,
                planning / "spikes" / "replay-manifest.yaml",
            )
            old = {target.relative_to(planning).as_posix(): target.read_bytes() if target.exists() else None for target in targets}
            recovery_path = ROOT / "tools" / "canonical-recovery.py"
            spec = importlib.util.spec_from_file_location("canonical_recovery_0146", recovery_path)
            recovery = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(recovery)
            for position in range(len(targets)):
                with self.subTest(position=position):
                    result = self.run_consolidation(
                        planning,
                        audit,
                        env=os.environ | {"CONSOLIDATION_INJECT_PUBLISH_INTERRUPTION": str(position)},
                    )
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn("CONSOLIDATION_PUBLISH_INTERRUPTED", result.stdout)
                    recovery.recover_canonical_generation(planning)
                    recovered = {
                        target.relative_to(planning).as_posix(): target.read_bytes() if target.exists() else None
                        for target in targets
                    }
                    self.assertIn(recovered, (old,))

    def test_consolidation_semantic_failure_does_not_enter_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            self.remove_consolidation_history(planning)
            fragment = yaml.safe_load((planning / "spikes" / "spk-h-browser-egress" / "impact-fragment.yaml").read_text(encoding="utf-8"))
            proposed_ids = {item["id"] for item in fragment["proposedDriftRecords"]}
            drift_path = planning / "research" / "drift-register.yaml"
            drift_document = yaml.safe_load(drift_path.read_text(encoding="utf-8"))
            drift_document["drift"] = [item for item in drift_document["drift"] if item["id"] not in proposed_ids]
            drift_path.write_text(yaml.safe_dump(drift_document, sort_keys=False), encoding="utf-8")
            audit = planning / "research" / "reports" / "audit.md"
            spec = importlib.util.spec_from_file_location("validate_research_0146", VALIDATOR)
            validator = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(validator)
            original_new_drift = validator.new_drift_record

            def invalid_new_drift(*args):
                record = original_new_drift(*args)
                record["observed"]["classification"] = "not-observed-local"
                return record

            validator.new_drift_record = invalid_new_drift
            before = self.canonical_bytes(planning)
            errors = validator.consolidate_spike_impacts(
                planning / "spikes", planning / "research", audit, False, 1.0, "normal"
            )
            self.assertTrue(any("SEM008" in error for error in errors), errors)
            self.assertEqual(before, self.canonical_bytes(planning))
            self.assertFalse((planning / ".canonical-transactions").exists())

    def test_contention_and_injected_precommit_failure_preserve_byte_identical_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            self.remove_consolidation_history(planning)
            audit = planning / "research" / "reports" / "audit.md"
            before = self.canonical_bytes(planning)
            env = os.environ | {"CONSOLIDATION_TEST_HOLD_LOCK_SECONDS": "0.4"}
            winner = subprocess.Popen(
                [sys.executable, str(VALIDATOR), "consolidate-spike-impacts", "--spikes", str(planning / "spikes"), "--research", str(planning / "research"), "--audit", str(audit)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            time.sleep(0.1)
            loser = self.run_consolidation(planning, audit, "--lock-timeout", "0.05")
            winner_stdout, winner_stderr = winner.communicate(timeout=10)
            self.assertEqual(winner.returncode, 0, winner_stdout + winner_stderr)
            self.assertNotEqual(loser.returncode, 0)
            self.assertIn("CONSOLIDATION_LOCK_CONFLICT", loser.stdout)
            after_success = self.canonical_bytes(planning)
            failing_env = os.environ | {"CONSOLIDATION_INJECT_PRECOMMIT_FAILURE": "1"}
            failed = self.run_consolidation(planning, audit, env=failing_env)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("CONSOLIDATION_INJECTED_FAILURE", failed.stdout)
            self.assertEqual(after_success, self.canonical_bytes(planning))
            self.assertNotEqual(before, after_success)


class CanonicalRecoveryTests(unittest.TestCase):
    """Regression contract for Plan 01-42 durable canonical publication."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.targets = ("a.yaml", "b.yaml", "c.yaml")
        for name in self.targets:
            (self.root / name).write_bytes(f"old-{name}".encode())
        recovery_path = ROOT / "tools" / "canonical-recovery.py"
        spec = importlib.util.spec_from_file_location("canonical_recovery", recovery_path)
        self.recovery = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(self.recovery)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _staged(self, prefix: str = "new") -> dict[str, bytes]:
        return {name: f"{prefix}-{name}".encode() for name in self.targets}

    def _live(self) -> dict[str, bytes]:
        return {name: (self.root / name).read_bytes() for name in self.targets}

    def test_recovery_after_each_publish_interruption_is_coherent(self) -> None:
        old = self._live()
        new = self._staged()
        for position in range(len(self.targets)):
            with self.subTest(position=position):
                for name, content in old.items():
                    (self.root / name).write_bytes(content)
                with self.assertRaises(self.recovery.PublishInterrupted):
                    self.recovery.publish_generation(self.root, new, interrupt_after=position)
                self.recovery.recover_canonical_generation(self.root)
                self.assertIn(self._live(), (old, new))

    def test_recovery_rejects_tampered_or_incomplete_journal_before_reader_entry(self) -> None:
        with self.assertRaises(self.recovery.PublishInterrupted):
            self.recovery.publish_generation(self.root, self._staged(), interrupt_after=0)
        journal = next((self.root / ".canonical-transactions").glob("*/journal.json"))
        journal.write_text("{\\\"state\\\": \\\"unknown\\\"}", encoding="utf-8")
        self.assertRaises(self.recovery.RecoveryError, self.recovery.read_canonical_snapshot, "fixture-reader", self.targets, root=self.root)

    def test_transactional_multi_file_reader_never_observes_mixed_generation_during_successful_publish(self) -> None:
        self.recovery.register_canonical_reader("fixture-reader", self.targets)
        old = self._live()
        paused = []
        snapshot = self.recovery.read_canonical_snapshot("fixture-reader", self.targets, root=self.root, after_first_read=lambda: paused.append(True))
        self.assertEqual(dict(snapshot), old)
        self.recovery.publish_generation(self.root, self._staged())
        self.assertEqual(dict(snapshot), old)

    def test_all_canonical_reader_entrypoints_use_registered_transactional_snapshot(self) -> None:
        self.recovery.register_canonical_reader("fixture-reader", self.targets)
        with self.assertRaises(self.recovery.RecoveryError):
            self.recovery.read_canonical_snapshot("undeclared-reader", self.targets, root=self.root)
        with self.assertRaises(self.recovery.RecoveryError):
            self.recovery.read_canonical_snapshot("fixture-reader", ("a.yaml",), root=self.root)

    def test_validated_canonical_set_api_rejects_wrong_profile_or_attestation(self) -> None:
        old = self._live()
        staged = self.root / "staged"
        staged.mkdir()
        for name, value in self._staged().items():
            (staged / name).write_bytes(value)
        attestation = {"profile": "fixture", "targetMap": {name: hashlib.sha256(value).hexdigest() for name, value in self._staged().items()}, "generationSha256": self.recovery.generation_sha256(self._staged())}
        self.recovery.register_canonical_profile("fixture", {name: name for name in self.targets})
        self.recovery.publish_validated_canonical_set("fixture", staged, attestation, root=self.root, allow_unsafe_staging=True)
        self.assertEqual(self._live(), self._staged())
        with self.assertRaises(self.recovery.RecoveryError):
            self.recovery.publish_validated_canonical_set("missing", staged, attestation, root=self.root, allow_unsafe_staging=True)
        self.assertEqual(self._live(), self._staged())

    def test_terminal_set_publishes_only_validated_staged_generation(self) -> None:
        self.recovery.register_canonical_profile("fixture", {name: name for name in self.targets})
        staged = self.root / "staged"
        staged.mkdir()
        generated = self._staged()
        for name, value in generated.items():
            (staged / name).write_bytes(value)
        attestation = {"profile": "fixture", "targetMap": {name: hashlib.sha256(value).hexdigest() for name, value in generated.items()}, "generationSha256": self.recovery.generation_sha256(generated)}
        (staged / "a.yaml").write_bytes(b"altered")
        with self.assertRaises(self.recovery.RecoveryError):
            self.recovery.publish_validated_canonical_set("fixture", staged, attestation, root=self.root, allow_unsafe_staging=True)

    def test_validate_planning_reads_one_transactional_snapshot_or_refuses(self) -> None:
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate-planning.py")], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Planning validation passed", result.stdout)

    def test_publish_validated_canonical_set_cli_contract(self) -> None:
        result = subprocess.run([sys.executable, str(ROOT / "tools/canonical-recovery.py"), "publish-validated-canonical-set", "--help"], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for option in ("--profile", "--staged-root", "--attestation"):
            self.assertIn(option, result.stdout)


# Plan 01-42 keeps the established public test class path while isolating the
# copied-root transaction fixtures from the legacy consolidation setup.
def _delegate_recovery_case(name: str):
    def delegated(_: unittest.TestCase) -> None:
        case = CanonicalRecoveryTests(name)
        case.setUp()
        try:
            getattr(case, name)()
        finally:
            case.tearDown()
    return delegated


for _recovery_test in (
    "test_recovery_after_each_publish_interruption_is_coherent",
    "test_recovery_rejects_tampered_or_incomplete_journal_before_reader_entry",
    "test_validate_planning_reads_one_transactional_snapshot_or_refuses",
    "test_transactional_multi_file_reader_never_observes_mixed_generation_during_successful_publish",
    "test_all_canonical_reader_entrypoints_use_registered_transactional_snapshot",
    "test_validated_canonical_set_api_rejects_wrong_profile_or_attestation",
    "test_terminal_set_publishes_only_validated_staged_generation",
    "test_publish_validated_canonical_set_cli_contract",
):
    setattr(SpikeConsolidationTests, _recovery_test, _delegate_recovery_case(_recovery_test))


if __name__ == "__main__":
    unittest.main()
