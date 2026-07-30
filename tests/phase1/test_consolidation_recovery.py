"""Observed-refresh transactional publication regressions for Plan 01-43."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLANNING = ROOT / ".planning"
VALIDATOR = ROOT / "tools" / "validate-research.py"
RECOVERY = ROOT / "tools" / "canonical-recovery.py"
TARGETS = (
    "claims.yaml",
    "drift-register.yaml",
    "open-questions.yaml",
    "package-map.md",
    "open-work-snapshot.json",
)


def load_recovery():
    spec = importlib.util.spec_from_file_location("canonical_recovery_0143", RECOVERY)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ObservedRefreshPublicationTests(unittest.TestCase):
    def copy_planning(self, directory: Path) -> Path:
        planning = directory / ".planning"
        shutil.copytree(
            PLANNING,
            planning,
            ignore=shutil.ignore_patterns(".cache", ".canonical-transactions", ".canonical-recovery.lock", ".observed-refresh-staging"),
        )
        return planning

    def staged_root(self, planning: Path) -> Path:
        staged = planning / ".observed-refresh-staging" / "phase-01"
        staged.mkdir(parents=True)
        for name in TARGETS:
            source = planning / "research" / name
            content = source.read_bytes()
            suffix = b"\n<!-- observed refresh fixture -->\n" if name == "package-map.md" else b"\n"
            staged.joinpath(name).write_bytes(content + suffix)
        return staged

    def validator(self, planning: Path, staged: Path, attestation: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "validate-observed-refresh-staged", "--staged-root", str(staged), "--attestation", str(attestation)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def attestation_map(self, staged: Path) -> dict[str, str]:
        return {name: hashlib.sha256((staged / name).read_bytes()).hexdigest() for name in TARGETS}

    def test_observed_refresh_five_file_generation_recovers_after_each_replacement(self) -> None:
        recovery = load_recovery()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = {}
            new = {}
            for name in TARGETS:
                target = root / "research" / name
                target.parent.mkdir(parents=True, exist_ok=True)
                old[f"research/{name}"] = f"old-{name}".encode()
                new[f"research/{name}"] = f"new-{name}".encode()
                target.write_bytes(old[f"research/{name}"])
            for position in range(len(TARGETS)):
                for name, content in old.items():
                    (root / name).write_bytes(content)
                with self.assertRaises(recovery.PublishInterrupted):
                    recovery.publish_generation(root, new, interrupt_after=position)
                recovery.recover_canonical_generation(root)
                snapshot = recovery.read_canonical_snapshot(
                    "observed-refresh-validation",
                    tuple(f"research/{name}" for name in TARGETS),
                    root=root,
                )
                self.assertIn(dict(snapshot), (old, new))

    def test_observed_refresh_reader_snapshot_waits_out_successful_publish(self) -> None:
        recovery = load_recovery()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = {}
            new = {}
            for name in TARGETS:
                target = root / "research" / name
                target.parent.mkdir(parents=True, exist_ok=True)
                old[f"research/{name}"] = f"old-{name}".encode()
                new[f"research/{name}"] = f"new-{name}".encode()
                target.write_bytes(old[f"research/{name}"])
            entered, release, published = threading.Event(), threading.Event(), threading.Event()
            captured: list[dict[str, bytes]] = []

            def reader() -> None:
                snapshot = recovery.read_canonical_snapshot(
                    "observed-refresh-validation",
                    tuple(f"research/{name}" for name in TARGETS),
                    root=root,
                    after_first_read=lambda: (entered.set(), release.wait(2)),
                )
                captured.append(dict(snapshot))

            def writer() -> None:
                recovery.publish_generation(root, new, timeout=1.5)
                published.set()

            read_thread = threading.Thread(target=reader)
            read_thread.start()
            self.assertTrue(entered.wait(1))
            write_thread = threading.Thread(target=writer)
            write_thread.start()
            time.sleep(0.1)
            self.assertFalse(published.is_set())
            release.set()
            read_thread.join(2)
            write_thread.join(2)
            self.assertTrue(published.is_set())
            self.assertEqual(captured, [old])
            current = recovery.read_canonical_snapshot(
                "observed-refresh-validation", tuple(f"research/{name}" for name in TARGETS), root=root
            )
            self.assertEqual(dict(current), new)

    def test_observed_refresh_rejects_tampered_or_incomplete_attestation_before_reader_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            staged = self.staged_root(planning)
            attestation = staged / "observed-refresh-validation-attestation.json"
            result = self.validator(planning, staged, attestation)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            staged.joinpath("unexpected.txt").write_text("x\n", encoding="utf-8")
            rejected = self.validator(planning, staged, attestation)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertFalse(attestation.exists())

    def test_observed_refresh_staged_validation_binds_exact_five_target_digests(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            staged = self.staged_root(planning)
            attestation = staged / "observed-refresh-validation-attestation.json"
            result = self.validator(planning, staged, attestation)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            document = json.loads(attestation.read_text(encoding="utf-8"))
            self.assertEqual(document["profile"], "observed-refresh")
            self.assertEqual(document["targetMap"], self.attestation_map(staged))
            self.assertEqual(list(document["targetMap"]), sorted(TARGETS))
            self.assertIn("reviewedSourceInputBinding", document)
            self.assertIn("spkG", document)

    def test_observed_refresh_staged_validation_cli_contract(self) -> None:
        help_result = subprocess.run(
            [sys.executable, str(VALIDATOR), "validate-observed-refresh-staged", "--help"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(help_result.returncode, 0, help_result.stdout + help_result.stderr)
        self.assertIn("--staged-root", help_result.stdout)
        self.assertIn("--attestation", help_result.stdout)
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            staged = self.staged_root(planning)
            (staged / "claims.yaml").unlink()
            attestation = staged / "observed-refresh-validation-attestation.json"
            result = self.validator(planning, staged, attestation)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(attestation.exists())

    def test_live_observed_refresh_generation_matches_attestation(self) -> None:
        staged = PLANNING / ".observed-refresh-staging" / "phase-01"
        attestation = staged / "observed-refresh-validation-attestation.json"
        self.assertTrue(attestation.is_file())
        document = json.loads(attestation.read_text(encoding="utf-8"))
        observed = {
            name: hashlib.sha256((PLANNING / "research" / name).read_bytes()).hexdigest()
            for name in TARGETS
        }
        self.assertEqual(document["targetMap"], observed)

    def test_observed_refresh_rejects_unbound_reviewed_acquisition_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            planning = self.copy_planning(Path(temp))
            receipt = planning / "research" / "reports" / "upstream-acquisition-20260728.md"
            document = json.loads(receipt.read_text(encoding="utf-8"))
            document["reviewedSourceInputBinding"]["reviewedCommit"] = "0" * 40
            receipt.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            staged = self.staged_root(planning)
            attestation = staged / "observed-refresh-validation-attestation.json"
            result = self.validator(planning, staged, attestation)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(attestation.exists())


if __name__ == "__main__":
    unittest.main()
