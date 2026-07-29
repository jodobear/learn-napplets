"""Deterministic regressions for the Phase 1 bootstrap and review boundary."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "tools" / "validate-planning.py"
spec = importlib.util.spec_from_file_location("validate_planning", VALIDATOR_PATH)
validate_planning = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validate_planning)


class Phase1ExecutionPreflightTests(unittest.TestCase):
    def _run_git(self, root: Path, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

    def _review_for(self, root: Path, commit: str, plan_paths: list[str], source_paths: list[str]) -> str:
        plan_rows = "\n".join(
            f"  {Path(path).name}: {hashlib.sha256((root / path).read_bytes()).hexdigest()}"
            for path in plan_paths
        )
        source_rows = []
        for path in source_paths:
            blob = self._run_git(root, "rev-parse", f"{commit}:{path}")
            digest = hashlib.sha256((root / path).read_bytes()).hexdigest()
            source_rows.extend(
                [
                    f"    - path: {path}",
                    '      mode: "100644"',
                    f"      git_blob: {blob}",
                    f"      sha256: {digest}",
                ]
            )
        return "\n".join(
            [
                "---",
                f"reviewed_commit: {commit}",
                "reviewer_identity:",
                '  codex: "independent-reviewer"',
                "current_high: 0",
                "current_actionable: 0",
                "authorization:",
                '  verdict: "CONVERGED; HIGH=0; actionable=0"',
                "  superseded: false",
                "plan_file_sha256:",
                plan_rows,
                "reviewed_source_inputs:",
                "  paths:",
                *source_rows,
                "---",
                "# Phase 1 Review",
            ]
        ) + "\n"

    def _temporary_review_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, list[str], list[str]]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        plan_path = ".planning/phases/01-research-and-truth-baseline/01-01-PLAN.md"
        source_paths = list(validate_planning.REQUIRED_PHASE1_SOURCE_INPUTS)
        contents = {
            plan_path: b"---\nphase: 01\n---\nplan bytes\n",
            ".planning/PROJECT.md": b"project\n",
            ".planning/phases/01-research-and-truth-baseline/01-CONTEXT.md": b"context\n",
            ".planning/research/reports/upstream-refresh-kehto-web-2026-07-28.md": b"kehto\n",
            ".planning/research/reports/upstream-refresh-napplet-web-2026-07-28.md": b"web\n",
            ".planning/research/reports/upstream-refresh-napplet-naps-2026-07-28.md": b"naps\n",
            ".planning/research/reports/upstream-refresh-synthesis-2026-07-28.md": b"synthesis\n",
        }
        for relative, content in contents.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        self._run_git(root, "init", "-q")
        self._run_git(root, "config", "user.email", "test@example.invalid")
        self._run_git(root, "config", "user.name", "Phase 1 Test")
        self._run_git(root, "add", ".")
        self._run_git(root, "commit", "-qm", "reviewed inputs")
        commit = self._run_git(root, "rev-parse", "HEAD")
        review = root / "review.md"
        review.write_text(self._review_for(root, commit, [plan_path], source_paths), encoding="utf-8")
        return temporary, root, review, [plan_path], source_paths

    def test_bootstrap_self_test_rejects_startup_hook_fixtures(self) -> None:
        manifest = ROOT / ".planning/spikes/_shared/toolchain-environment.json"
        interpreter = ROOT / ".research/phase1-tools/bin/python"
        result = subprocess.run(
            [str(interpreter), "-I", "-S", str(ROOT / "tools/phase1-bootstrap.py"), "--environment", str(manifest), "--self-test"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("bootstrap self-test passed", result.stdout)

    def test_preflight_rejects_review_not_bound_to_active_plan_manifest(self) -> None:
        temporary, root, review, plan_paths, _ = self._temporary_review_repo()
        with temporary:
            original = review.read_text(encoding="utf-8")
            cases = {
                "omitted": original.replace("  01-01-PLAN.md:", "  01-02-PLAN.md:"),
                "extra": original.replace("reviewed_source_inputs:", "  01-02-PLAN.md: " + "0" * 64 + "\nreviewed_source_inputs:"),
                "duplicate": original.replace("reviewed_source_inputs:", "  01-01-PLAN.md: " + "0" * 64 + "\nreviewed_source_inputs:"),
                "altered": original.replace(hashlib.sha256((root / plan_paths[0]).read_bytes()).hexdigest(), "f" * 64),
                "malformed": original.replace("  01-01-PLAN.md:", "  invalid plan name:"),
                "wrong-commit": original.replace("reviewed_commit:", "reviewed_commit: " + "0" * 40 + "\n# reviewed_commit:"),
            }
            for name, text in cases.items():
                with self.subTest(name=name):
                    errors = validate_planning.review_manifest_errors(text, root=root, executor_identity="executor")
                    self.assertTrue(errors, errors)

    def test_preflight_content_addressed_review_requires_bound_bytes_or_explicit_supersession(self) -> None:
        temporary, root, review, plan_paths, _ = self._temporary_review_repo()
        with temporary:
            text = review.read_text(encoding="utf-8")
            self.assertEqual(
                validate_planning.review_manifest_errors(text, root=root, executor_identity="executor"),
                [],
            )
            (root / plan_paths[0]).write_text("changed\n", encoding="utf-8")
            self.assertTrue(validate_planning.review_manifest_errors(text, root=root, executor_identity="executor"))
            (root / plan_paths[0]).write_text("---\nphase: 01\n---\nplan bytes\n", encoding="utf-8")
            self.assertTrue(
                validate_planning.review_manifest_errors(
                    text.replace("reviewed_commit:", "reviewed_commit: " + "f" * 40 + "\n# reviewed_commit:"),
                    root=root,
                    executor_identity="executor",
                )
            )
            self.assertTrue(
                validate_planning.review_manifest_errors(
                    text.replace("superseded: false", "superseded: true"),
                    root=root,
                    executor_identity="executor",
                )
            )

    def test_preflight_requires_exact_convergence_and_high_disposition(self) -> None:
        temporary, root, review, _, _ = self._temporary_review_repo()
        with temporary:
            text = review.read_text(encoding="utf-8")
            for name, altered in {
                "nonconverged": text.replace("CONVERGED; HIGH=0; actionable=0", "looks good"),
                "high": text.replace("current_high: 0", "current_high: 1"),
                "missing-reviewer": text.replace('  codex: "independent-reviewer"\n', ""),
            }.items():
                with self.subTest(name=name):
                    self.assertTrue(validate_planning.review_manifest_errors(altered, root=root, executor_identity="executor"))
            self.assertTrue(validate_planning.review_manifest_errors(text, root=root, executor_identity="independent-reviewer"))

    def test_preflight_rejects_duplicate_authorization_or_convergence_sections(self) -> None:
        temporary, root, review, _, _ = self._temporary_review_repo()
        with temporary:
            text = review.read_text(encoding="utf-8")
            for heading in ("Execution authorization", "Convergence"):
                with self.subTest(heading=heading):
                    duplicate = text + f"\n## {heading}\nfirst\n\n## {heading}\nsecond\n"
                    self.assertTrue(validate_planning.review_manifest_errors(duplicate, root=root, executor_identity="executor"))

    def test_phase1_complete_rejects_missing_executor_identity_before_success_output(self) -> None:
        environment = os.environ.copy()
        environment.pop("GSD_EXECUTOR_ID", None)
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--phase-1-complete"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Planning validation passed", result.stdout)

    def test_preflight_rejects_absent_untracked_or_byte_mismatched_required_source_input(self) -> None:
        temporary, root, review, _, source_paths = self._temporary_review_repo()
        with temporary:
            text = review.read_text(encoding="utf-8")
            self.assertEqual(validate_planning.review_manifest_errors(text, root=root, executor_identity="executor"), [])
            for name, mutate in {
                "missing": lambda path: path.unlink(),
                "untracked": lambda path: (path.unlink(), path.write_text("untracked\n", encoding="utf-8")),
                "byte-mismatched": lambda path: path.write_text("changed\n", encoding="utf-8"),
            }.items():
                with self.subTest(name=name):
                    target = root / source_paths[0]
                    original = b"project\n"
                    target.write_bytes(original)
                    if name == "untracked":
                        self._run_git(root, "rm", "--cached", "--", source_paths[0])
                    mutate(target)
                    errors = validate_planning.review_manifest_errors(text, root=root, executor_identity="executor")
                    self.assertTrue(errors, errors)
                    if name == "untracked":
                        self._run_git(root, "reset", "--", source_paths[0])

    def test_preflight_loads_only_reviewed_git_blob_source_snapshot(self) -> None:
        temporary, root, review, _, source_paths = self._temporary_review_repo()
        with temporary:
            snapshot = validate_planning.load_reviewed_phase1_source_snapshot(
                review, root=root, executor_identity="executor"
            )
            self.assertEqual(tuple(snapshot), tuple(source_paths))
            self.assertEqual(snapshot[".planning/PROJECT.md"], b"project\n")
            with self.assertRaises(TypeError):
                snapshot[".planning/PROJECT.md"] = b"replacement\n"
            (root / ".planning/PROJECT.md").write_text("mutable replacement\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_planning.load_reviewed_phase1_source_snapshot(
                    review, root=root, executor_identity="executor"
                )


if __name__ == "__main__":
    unittest.main()
