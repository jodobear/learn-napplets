"""Contract tests for the complete Phase 1 wrapper-only closeout pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Callable
import unittest


WRAPPER = "tools/phase1-python"


@dataclass(frozen=True)
class CloseoutStage:
    """One ordered, wrapper-bound command in the Phase 1 closeout contract."""

    identifier: str
    argv: list[str]


@dataclass(frozen=True)
class CloseoutResult:
    """The only closeout outcome: all stages pass or one named stage blocks."""

    succeeded: bool
    failed_stage: str | None
    completed_stages: tuple[str, ...]


def build_supported_closeout_stages(executor_identity: str, reviewer_identity: str) -> tuple[CloseoutStage, ...]:
    """Return the exact supported argv sequence without shell interpolation."""
    if not executor_identity:
        raise ValueError("executor identity must be nonempty")
    if not reviewer_identity or executor_identity == reviewer_identity:
        raise ValueError("executor identity must differ from the independent reviewer")
    return (
        CloseoutStage(
            "bound-review-preflight",
            [
                WRAPPER,
                "tools/validate-planning.py",
                "--phase-1-execution-preflight",
                "--executor-identity",
                executor_identity,
            ],
        ),
        CloseoutStage("toolchain-verification", [WRAPPER, "--verify-toolchain"]),
        CloseoutStage("full-phase1-tests", [WRAPPER, "-m", "unittest", "discover", "-s", "tests/phase1"]),
        CloseoutStage(
            "research-validation",
            [
                WRAPPER,
                "tools/validate-research.py",
                "validate",
                "--root",
                ".planning/research",
                "--report",
                "/tmp/phase1-final-validation.md",
            ],
        ),
        CloseoutStage(
            "report-validation",
            [WRAPPER, "tools/validate-research.py", "validate-reports", "--root", ".planning"],
        ),
        CloseoutStage(
            "canonical-recovery",
            [WRAPPER, "tools/validate-research.py", "recover-consolidation", "--research", ".planning/research"],
        ),
        CloseoutStage(
            "spike-replay",
            [
                WRAPPER,
                "tools/validate-research.py",
                "replay-spikes",
                "--manifest",
                ".planning/spikes/replay-manifest.yaml",
                "--check",
            ],
        ),
        CloseoutStage(
            "phase-completion",
            [WRAPPER, "tools/validate-planning.py", "--phase-1-complete", "--executor-identity", executor_identity],
        ),
    )


def run_closeout_stages(
    stages: tuple[CloseoutStage, ...],
    subprocess_runner: Callable[[CloseoutStage], object],
) -> CloseoutResult:
    """Run injected subprocess calls in order and stop at the first nonzero result."""
    completed: list[str] = []
    for stage in stages:
        result = subprocess_runner(stage)
        if getattr(result, "returncode", 1) != 0:
            return CloseoutResult(False, stage.identifier, tuple(completed))
        completed.append(stage.identifier)
    return CloseoutResult(True, None, tuple(completed))


class Phase1CloseoutCommandTests(unittest.TestCase):
    def test_supported_closeout_sequence_uses_approved_wrapper(self) -> None:
        executor_identity = "phase1-closeout-executor"
        reviewer_identity = "codex-cli/0.146.0:gpt-5.6-sol:external-read-only"
        stages = build_supported_closeout_stages(executor_identity, reviewer_identity)

        expected = [
            (
                "bound-review-preflight",
                [
                    "tools/phase1-python",
                    "tools/validate-planning.py",
                    "--phase-1-execution-preflight",
                    "--executor-identity",
                    executor_identity,
                ],
            ),
            ("toolchain-verification", ["tools/phase1-python", "--verify-toolchain"]),
            (
                "full-phase1-tests",
                ["tools/phase1-python", "-m", "unittest", "discover", "-s", "tests/phase1"],
            ),
            (
                "research-validation",
                [
                    "tools/phase1-python",
                    "tools/validate-research.py",
                    "validate",
                    "--root",
                    ".planning/research",
                    "--report",
                    "/tmp/phase1-final-validation.md",
                ],
            ),
            (
                "report-validation",
                [
                    "tools/phase1-python",
                    "tools/validate-research.py",
                    "validate-reports",
                    "--root",
                    ".planning",
                ],
            ),
            (
                "canonical-recovery",
                [
                    "tools/phase1-python",
                    "tools/validate-research.py",
                    "recover-consolidation",
                    "--research",
                    ".planning/research",
                ],
            ),
            (
                "spike-replay",
                [
                    "tools/phase1-python",
                    "tools/validate-research.py",
                    "replay-spikes",
                    "--manifest",
                    ".planning/spikes/replay-manifest.yaml",
                    "--check",
                ],
            ),
            (
                "phase-completion",
                [
                    "tools/phase1-python",
                    "tools/validate-planning.py",
                    "--phase-1-complete",
                    "--executor-identity",
                    executor_identity,
                ],
            ),
        ]
        self.assertEqual([(stage.identifier, stage.argv) for stage in stages], expected)
        self.assertTrue(all(stage.argv[0] == "tools/phase1-python" for stage in stages))
        self.assertNotEqual(executor_identity, reviewer_identity)
        self.assertTrue(executor_identity)

        seen: list[tuple[str, list[str]]] = []

        def successful_runner(stage):
            seen.append((stage.identifier, stage.argv))
            return SimpleNamespace(returncode=0, stdout=f"{stage.identifier} passed", stderr="")

        result = run_closeout_stages(stages, successful_runner)
        self.assertTrue(result.succeeded)
        self.assertIsNone(result.failed_stage)
        self.assertEqual(seen, expected)

    def test_closeout_sequence_stops_on_nonzero_stage(self) -> None:
        stages = build_supported_closeout_stages(
            "phase1-closeout-executor",
            "codex-cli/0.146.0:gpt-5.6-sol:external-read-only",
        )
        seen: list[str] = []

        for review_diagnostic in (
            "PRE119: active plan digest differs",
            "PRE117: executor identity must differ from reviewer identity",
        ):
            with self.subTest(review_diagnostic=review_diagnostic):
                seen.clear()

                def rejected_review_runner(stage, diagnostic=review_diagnostic):
                    seen.append(stage.identifier)
                    return SimpleNamespace(
                        returncode=1 if stage.identifier == "bound-review-preflight" else 0,
                        stdout=diagnostic,
                        stderr="",
                    )

                rejected_review = run_closeout_stages(stages, rejected_review_runner)
                self.assertFalse(rejected_review.succeeded)
                self.assertEqual(rejected_review.failed_stage, "bound-review-preflight")
                self.assertEqual(seen, ["bound-review-preflight"])
                self.assertNotIn("phase-completion", rejected_review.completed_stages)

        seen.clear()

        def failing_runner(stage):
            seen.append(stage.identifier)
            return SimpleNamespace(
                returncode=1 if stage.identifier == "report-validation" else 0,
                stdout=f"{stage.identifier} result",
                stderr="",
            )

        failure = run_closeout_stages(stages, failing_runner)
        self.assertFalse(failure.succeeded)
        self.assertEqual(failure.failed_stage, "report-validation")
        self.assertEqual(
            seen,
            [
                "bound-review-preflight",
                "toolchain-verification",
                "full-phase1-tests",
                "research-validation",
                "report-validation",
            ],
        )
        self.assertNotIn("canonical-recovery", failure.completed_stages)
        self.assertNotIn("spike-replay", failure.completed_stages)
        self.assertNotIn("phase-completion", failure.completed_stages)


from pathlib import Path
import hashlib
import importlib.util
import json
import re
import shutil
import tempfile


TERMINAL_ROOT = Path(__file__).resolve().parents[2]
TERMINAL_CANDIDATE = TERMINAL_ROOT / ".planning/phases/01-research-and-truth-baseline/01-VERIFICATION-CANDIDATE.md"
TERMINAL_CONTRACT = TERMINAL_ROOT / ".planning/phases/01-research-and-truth-baseline/01-VALIDATION.md"
TERMINAL_AUDIT = TERMINAL_ROOT / ".planning/phases/01-research-and-truth-baseline/01-POST-CLOSURE-VERIFICATION.md"
TERMINAL_SECURITY = TERMINAL_ROOT / ".planning/phases/01-research-and-truth-baseline/01-SECURITY.md"
TERMINAL_VALIDATOR = TERMINAL_ROOT / "tools/validate-phase1-terminal.py"


def load_terminal_validator():
    spec = importlib.util.spec_from_file_location("phase1_terminal_validator", TERMINAL_VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("terminal validator module is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reviewed_source_table(text: str) -> str:
    match = re.search(
        r"^## Reviewed Source-Grounding Authorization\n.*?(\| Path \|.*?)(?=\n\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError("candidate is missing source-grounding table")
    return match.group(1).strip()


class VerificationAdjudicationTests(unittest.TestCase):
    def test_fresh_verification_has_exact_review_finding_adjudication(self) -> None:
        terminal = load_terminal_validator()
        terminal.validate_candidate_evidence(
            candidate=TERMINAL_CANDIDATE,
            validation_contract=TERMINAL_CONTRACT,
            post_closure_audit=TERMINAL_AUDIT,
            security=TERMINAL_SECURITY,
        )
        with tempfile.TemporaryDirectory() as temporary:
            malformed = Path(temporary) / "candidate.md"
            text = TERMINAL_CANDIDATE.read_text(encoding="utf-8")
            malformed.write_text(
                text.replace(
                    "| CR-08 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent`",
                    "| CR-08 | `tools/not-the-certified-wrapper.py`",
                ),
                encoding="utf-8",
            )
            with self.assertRaises(terminal.ValidationError):
                terminal.validate_candidate_evidence(
                    candidate=malformed,
                    validation_contract=TERMINAL_CONTRACT,
                    post_closure_audit=TERMINAL_AUDIT,
                    security=TERMINAL_SECURITY,
                )


class TerminalPublicationTests(unittest.TestCase):
    executor_identity = "claude-code/gpt-5.6-sol:gsd-executor"

    def setUp(self) -> None:
        self.terminal = load_terminal_validator()
        self.temporary = tempfile.TemporaryDirectory()
        self.staged_root = Path(self.temporary.name) / "phase-01"
        self.staged_root.mkdir()
        self.attestation = self.staged_root / "terminal-validation-attestation.json"
        self.live_state = (TERMINAL_ROOT / ".planning/STATE.md").read_bytes()
        self.live_roadmap = (TERMINAL_ROOT / ".planning/ROADMAP.md").read_bytes()
        self._write_complete_targets()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_complete_targets(self) -> None:
        candidate_digest = hashlib.sha256(TERMINAL_CANDIDATE.read_bytes()).hexdigest()
        security_digest = hashlib.sha256(TERMINAL_SECURITY.read_bytes()).hexdigest()
        source_table = reviewed_source_table(TERMINAL_CANDIDATE.read_text(encoding="utf-8"))
        reverify = f'''---
reviewed_commit: 1a9449be4d74aa1ceed235d949802266846cf63b
candidate_sha256: {candidate_digest}
security_sha256: {security_digest}
plan_review_sha256: 8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95
terminalVerifier:
  role: terminalVerifier
  principal: independent-human
  timestamp: "2026-07-30T22:00:00Z"
  reviewed_commit: 1a9449be4d74aa1ceed235d949802266846cf63b
  plan_review_sha256: 8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95
  evidence_sha256: {candidate_digest}
  security_sha256: {security_digest}
  determination: blocked
  rationale: Evidence remains intentionally blocked pending human scope determination.
projectOwnerRechecker:
  role: projectOwnerRechecker
  principal: independent-human
  timestamp: "2026-07-30T22:01:00Z"
  reviewed_commit: 1a9449be4d74aa1ceed235d949802266846cf63b
  plan_review_sha256: 8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95
  evidence_sha256: {candidate_digest}
  security_sha256: {security_digest}
  determination: blocked
  rationale: Independently rechecked the retained compatibility blocker.
---

# Phase 1 Re-verification

## Reviewed Source-Grounding Authorization

{source_table}
'''
        (self.staged_root / "01-REVERIFICATION.md").write_text(reverify, encoding="utf-8")
        (self.staged_root / "STATE.md").write_text("staged state; no transition\n", encoding="utf-8")
        (self.staged_root / "ROADMAP.md").write_text("staged roadmap; no transition\n", encoding="utf-8")

    def _validate_staged(self) -> dict[str, object]:
        return self.terminal.validate_staged_terminal(
            staged_root=self.staged_root,
            candidate=TERMINAL_CANDIDATE,
            security=TERMINAL_SECURITY,
            reviewed_commit="1a9449be4d74aa1ceed235d949802266846cf63b",
            post_closure_audit=TERMINAL_AUDIT,
            executor_identity=self.executor_identity,
            attestation=self.attestation,
        )

    def test_terminal_validator_binds_staged_three_file_set_before_publication(self) -> None:
        result = self._validate_staged()
        self.assertEqual(set(result["targetMap"]), {"01-REVERIFICATION.md", "STATE.md", "ROADMAP.md"})
        self.assertEqual((TERMINAL_ROOT / ".planning/STATE.md").read_bytes(), self.live_state)
        self.assertEqual((TERMINAL_ROOT / ".planning/ROADMAP.md").read_bytes(), self.live_roadmap)
        (self.staged_root / "unexpected.md").write_text("extra", encoding="utf-8")
        with self.assertRaises(self.terminal.ValidationError):
            self._validate_staged()

    def test_terminal_validator_uses_external_target_only_aggregate_without_self_reference(self) -> None:
        result = self._validate_staged()
        self.assertTrue(self.attestation.is_file())
        self.assertNotIn("terminal-validation-attestation.json", result["targetMap"])
        payload = json.loads(self.attestation.read_text(encoding="utf-8"))
        self.assertEqual(payload["generationSha256"], result["generationSha256"])
        (self.staged_root / "STATE.md").write_text("tampered staged state\n", encoding="utf-8")
        with self.assertRaises(self.terminal.ValidationError):
            self.terminal.validate_existing_attestation(self.staged_root, self.attestation)

    def test_terminal_validator_requires_separate_role_bound_records_but_allows_one_principal(self) -> None:
        self._validate_staged()
        reverify = self.staged_root / "01-REVERIFICATION.md"
        text = reverify.read_text(encoding="utf-8")
        reverify.write_text(text.replace("projectOwnerRechecker:", "missingRole:"), encoding="utf-8")
        with self.assertRaises(self.terminal.ValidationError):
            self._validate_staged()
        self._write_complete_targets()
        reverify.write_text(
            reverify.read_text(encoding="utf-8").replace("principal: independent-human", f"principal: {self.executor_identity}", 1),
            encoding="utf-8",
        )
        with self.assertRaises(self.terminal.ValidationError):
            self._validate_staged()

    def test_terminal_validator_requires_exact_reviewed_source_input_binding(self) -> None:
        self.terminal.validate_candidate_evidence(
            candidate=TERMINAL_CANDIDATE,
            validation_contract=TERMINAL_CONTRACT,
            post_closure_audit=TERMINAL_AUDIT,
            security=TERMINAL_SECURITY,
        )
        with tempfile.TemporaryDirectory() as temporary:
            malformed = Path(temporary) / "candidate.md"
            text = TERMINAL_CANDIDATE.read_text(encoding="utf-8")
            marker = "| `.planning/PROJECT.md` |"
            malformed.write_text(text.replace(marker, marker + "\n" + marker, 1), encoding="utf-8")
            with self.assertRaises(self.terminal.ValidationError):
                self.terminal.validate_candidate_evidence(
                    candidate=malformed,
                    validation_contract=TERMINAL_CONTRACT,
                    post_closure_audit=TERMINAL_AUDIT,
                    security=TERMINAL_SECURITY,
                )

    def test_terminal_validator_requires_canonical_probe_attempt_ledger(self) -> None:
        self.terminal.validate_candidate_evidence(
            candidate=TERMINAL_CANDIDATE,
            validation_contract=TERMINAL_CONTRACT,
            post_closure_audit=TERMINAL_AUDIT,
            security=TERMINAL_SECURITY,
        )
        with tempfile.TemporaryDirectory() as temporary:
            malformed = Path(temporary) / "candidate.md"
            text = TERMINAL_CANDIDATE.read_text(encoding="utf-8")
            malformed.write_text(text.replace('"role":"direct"', '"role":"post-closure"', 1), encoding="utf-8")
            with self.assertRaises(self.terminal.ValidationError):
                self.terminal.validate_candidate_evidence(
                    candidate=malformed,
                    validation_contract=TERMINAL_CONTRACT,
                    post_closure_audit=TERMINAL_AUDIT,
                    security=TERMINAL_SECURITY,
                )

    def test_terminal_validator_preserves_closed_ledger_through_post_closure_verification(self) -> None:
        self.terminal.validate_candidate_evidence(
            candidate=TERMINAL_CANDIDATE,
            validation_contract=TERMINAL_CONTRACT,
            post_closure_audit=TERMINAL_AUDIT,
            security=TERMINAL_SECURITY,
        )
        with tempfile.TemporaryDirectory() as temporary:
            malformed = Path(temporary) / "audit.md"
            text = TERMINAL_AUDIT.read_text(encoding="utf-8")
            malformed.write_text(text.replace('"preClosureLedgerSha256":"a530368', '"preClosureLedgerSha256":"b530368', 1), encoding="utf-8")
            with self.assertRaises(self.terminal.ValidationError):
                self.terminal.validate_candidate_evidence(
                    candidate=TERMINAL_CANDIDATE,
                    validation_contract=TERMINAL_CONTRACT,
                    post_closure_audit=malformed,
                    security=TERMINAL_SECURITY,
                )


if __name__ == "__main__":
    unittest.main()
