"""Contract tests for the complete Phase 1 wrapper-only closeout pipeline."""

from __future__ import annotations

from types import SimpleNamespace
import unittest


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

        def stale_review_runner(stage):
            seen.append(stage.identifier)
            if stage.identifier == "bound-review-preflight":
                return SimpleNamespace(returncode=1, stdout="PRE119: active plan digest differs", stderr="")
            return SimpleNamespace(returncode=0, stdout=f"{stage.identifier} passed", stderr="")

        stale_review = run_closeout_stages(stages, stale_review_runner)
        self.assertFalse(stale_review.succeeded)
        self.assertEqual(stale_review.failed_stage, "bound-review-preflight")
        self.assertEqual(seen, ["bound-review-preflight"])
        self.assertNotIn("phase-completion", stale_review.completed_stages)

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
