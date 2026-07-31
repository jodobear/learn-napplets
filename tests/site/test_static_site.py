"""Observable contract tests for the dependency-free static learning site."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "tools" / "build-site.py"
CONTENT = ROOT / "site" / "content" / "site.json"


class StaticSiteBuildTests(unittest.TestCase):
    maxDiff = None

    def build(self, content: Path, output: Path, check: bool = False) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(BUILDER),
            "--content",
            str(content),
            "--output",
            str(output),
        ]
        if check:
            command.append("--check")
        return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)

    def test_build_emits_the_complete_four_page_learning_path_and_knowledge(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "dist"
            result = self.build(CONTENT, output)
            self.assertEqual(result.returncode, 0, result.stderr)

            expected = {
                "index.html",
                "learn/index.html",
                "architecture/index.html",
                "sources/index.html",
                "knowledge.json",
            }
            self.assertEqual(
                {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()},
                expected,
            )
            architecture = (output / "architecture" / "index.html").read_text(encoding="utf-8")
            sources = (output / "sources" / "index.html").read_text(encoding="utf-8")
            self.assertIn('id="architecture-transcript"', architecture)
            self.assertIn("Request → mediated capability → result", architecture)
            self.assertIn("SRC-NAPS-NAP-INTENT-20260731", sources)
            self.assertIn("material", sources)

    def test_essential_fact_changes_propagate_to_human_and_machine_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            content = temporary_path / "site.json"
            output = temporary_path / "dist"
            shutil.copyfile(CONTENT, content)
            payload = json.loads(content.read_text(encoding="utf-8"))
            payload["facts"]["FACT-HOST-BOUNDARY-001"]["statement"] = (
                "Authority stays with the host; the guest receives only declared mediated capabilities."
            )
            content.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            result = self.build(content, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            rendered = (output / "architecture" / "index.html").read_text(encoding="utf-8")
            knowledge = (output / "knowledge.json").read_text(encoding="utf-8")
            expected = payload["facts"]["FACT-HOST-BOUNDARY-001"]["statement"]
            self.assertIn(expected, rendered)
            self.assertIn(expected, knowledge)
            self.assertIn("FACT-HOST-BOUNDARY-001", rendered)
            self.assertIn("FACT-HOST-BOUNDARY-001", knowledge)

    def test_build_is_byte_reproducible_and_check_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "dist"
            first = self.build(CONTENT, output)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = {
                file.relative_to(output).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest()
                for file in output.rglob("*")
                if file.is_file()
            }
            second = self.build(CONTENT, output, check=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            after = {
                file.relative_to(output).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest()
                for file in output.rglob("*")
                if file.is_file()
            }
            self.assertEqual(before, after)
            (output / "index.html").write_text("drift", encoding="utf-8")
            drift = self.build(CONTENT, output, check=True)
            self.assertNotEqual(drift.returncode, 0)
            self.assertIn("out of date", drift.stderr)

    def test_builder_rejects_unsafe_content_and_unknown_references(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            content = temporary_path / "site.json"
            output = temporary_path / "dist"
            shutil.copyfile(CONTENT, content)
            payload = json.loads(content.read_text(encoding="utf-8"))
            payload["facts"]["FACT-HOST-BOUNDARY-001"]["statement"] = "<script>unsafe</script>"
            content.write_text(json.dumps(payload), encoding="utf-8")
            unsafe = self.build(content, output)
            self.assertNotEqual(unsafe.returncode, 0)
            self.assertIn("unsafe markup", unsafe.stderr)

            payload["facts"]["FACT-HOST-BOUNDARY-001"]["statement"] = "Safe sentence."
            payload["pages"]["home"]["factIds"].append("FACT-UNKNOWN-999")
            content.write_text(json.dumps(payload), encoding="utf-8")
            unknown = self.build(content, output)
            self.assertNotEqual(unknown.returncode, 0)
            self.assertIn("unknown fact ID", unknown.stderr)


if __name__ == "__main__":
    unittest.main()
