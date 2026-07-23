"""Immutable spike impact-fragment validation tests."""

from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-research.py"
SHA = "a" * 64
FRAGMENT = {
    "schemaVersion": 1,
    "id": "SPK-IMPACT-TEST-001",
    "kind": "spike-impact-fragment",
    "spikeId": "SPK-TEST-001",
    "metadataPath": "spikes/spk-test-001/metadata.yaml",
    "reportPath": "spikes/spk-test-001/report.md",
    "sourceLinks": [{"sourceId": "SRC-POLICY-001", "relation": "measures", "path": "research/source-registry.yaml", "sha256": SHA}],
    "measurementLinks": [{"path": "spikes/spk-test-001/raw.txt", "sha256": SHA}],
    "uncertainty": {"state": "limited", "reason": "Fixture-only result."},
    "proposedImpacts": [{"type": "adr", "id": "ADR-0005", "rationale": "Requires human review."}],
}


class SpikeConsolidationTests(unittest.TestCase):
    def run_fragment(self, fragment: Path, planning_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(VALIDATOR), "validate-impact-fragment", str(fragment), "--root", str(planning_root)], cwd=ROOT, text=True, capture_output=True, check=False)

    def write_fixture_root(self, fragment: dict) -> tuple[Path, Path, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        planning = Path(temp.name) / ".planning"
        spike = planning / "spikes" / "spk-test-001"
        spike.mkdir(parents=True)
        metadata = spike / "metadata.yaml"
        metadata.write_text("id: SPK-TEST-001\n", encoding="utf-8")
        report = spike / "report.md"
        report.write_text("# Spike report\n", encoding="utf-8")
        raw = spike / "raw.txt"
        raw.write_text("raw measurement\n", encoding="utf-8")
        source = planning / "research" / "source-registry.yaml"
        source.parent.mkdir()
        source.write_text("sources:\n  - id: SRC-POLICY-001\n", encoding="utf-8")
        fragment["sourceLinks"][0]["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        fragment["measurementLinks"][0]["sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
        fragment_path = planning / "spikes" / "spk-test-001" / "impact.yaml"
        fragment_path.write_text(yaml.safe_dump(fragment), encoding="utf-8")
        return fragment_path, planning, temp

    def test_fragment_resolves_source_and_measurement_digests(self) -> None:
        fragment_path, planning, temp = self.write_fixture_root(copy.deepcopy(FRAGMENT))
        with temp:
            result = self.run_fragment(fragment_path, planning)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fragment_rejects_missing_altered_semantic_mismatched_and_dangling_links(self) -> None:
        cases = {
            "missing": lambda value: value.pop("measurementLinks"),
            "semantic": lambda value: value.update({"spikeId": "SPK-OTHER-001"}),
            "dangling": lambda value: value["sourceLinks"][0].update({"sourceId": "SRC-MISSING-001"}),
            "altered": lambda value: value["measurementLinks"][0].update({"sha256": "b" * 64}),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                fragment = copy.deepcopy(FRAGMENT)
                mutate(fragment)
                fragment_path, planning, temp = self.write_fixture_root(fragment)
                with temp:
                    result = self.run_fragment(fragment_path, planning)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("ERROR IMP", result.stdout)

    def test_spk_h_fragment_requires_security_egress_extension(self) -> None:
        fragment = copy.deepcopy(FRAGMENT)
        fragment.update({"id": "SPK-IMPACT-H-001", "spikeId": "SPK-H-001", "metadataPath": "spikes/spk-h-001/metadata.yaml", "reportPath": "spikes/spk-h-001/report.md"})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "impact.yaml"
            path.write_text(yaml.safe_dump(fragment), encoding="utf-8")
            result = self.run_fragment(path, Path(temp))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("securityEgress", result.stdout)


if __name__ == "__main__":
    unittest.main()
