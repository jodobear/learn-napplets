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


if __name__ == "__main__":
    unittest.main()
