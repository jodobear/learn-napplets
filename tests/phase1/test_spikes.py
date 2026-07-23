"""Disposable SPK envelope validation tests."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-research.py"


BASE_SPIKE = {
    "schemaVersion": 1,
    "id": "SPK-TEST-001",
    "kind": "spike",
    "nonProduction": True,
    "status": "planned",
    "hypothesis": "The isolated fixture can be replayed without external state.",
    "variables": {
        "independent": ["fixture-input"],
        "dependent": ["reported-result"],
        "controlled": ["isolated-directory"],
    },
    "commands": ["tools/phase1-python run.py --fixture fixture.json"],
    "environmentManifest": "environment.json",
    "sourceBindings": [
        {
            "sourceId": "SRC-POLICY-001",
            "relation": "measures",
            "plan": "Use the immutable policy seed only as a project-policy input.",
        }
    ],
    "successThreshold": "The local replay returns the expected fixture result.",
    "failureOutcome": "Reject the scoped recommendation.",
    "blockedOutcome": "Record an impact-scoped blocker for review.",
    "replay": {
        "input": "fixture.json",
        "command": "tools/phase1-python run.py --fixture fixture.json",
    },
    "safety": {
        "noSecrets": True,
        "noDestructiveState": True,
        "liveProbe": "not-used",
    },
    "uncertainty": {"state": "limited", "reason": "Fixture-only contract test."},
    "recommendation": "No architecture recommendation; this is a disposable validation fixture.",
    "disposition": "delete-spike",
}

VALID_ENVIRONMENT = {
    "schemaVersion": 1,
    "id": "ENV-TEST-001",
    "kind": "environment",
    "os": "Linux test fixture",
    "container": "not detected",
    "browsers": [{"family": "Firefox", "version": "152", "executableSha256": "c" * 64}],
    "runtimes": {"python": "3.14"},
    "packageManager": {"name": "pip", "version": "26"},
    "dependencies": [],
    "environmentFlags": [],
    "commandHashes": [{"command": "tools/phase1-python run.py --fixture fixture.json", "sha256": "d" * 64}],
}


class SpikeValidationTests(unittest.TestCase):
    def write_spike(self, metadata: dict, environment: dict | None = None) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        directory = Path(temp.name) / ".planning" / "spikes" / "spk-test-001"
        directory.mkdir(parents=True)
        (directory / "metadata.yaml").write_text(yaml.safe_dump(metadata, sort_keys=False), encoding="utf-8")
        if environment is not None:
            (directory / "environment.json").write_text(json.dumps(environment), encoding="utf-8")
        return directory, temp

    def run_spike(self, directory: Path, mode: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "validate-spike", str(directory), mode],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_contract_accepts_measurement_free_pre_run_envelope(self) -> None:
        directory, temp = self.write_spike(copy.deepcopy(BASE_SPIKE))
        with temp:
            result = self.run_spike(directory, "--contract")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_contract_rejects_each_required_pre_run_declaration(self) -> None:
        for key in ("hypothesis", "variables", "environmentManifest", "commands", "successThreshold", "replay", "sourceBindings"):
            with self.subTest(key=key):
                metadata = copy.deepcopy(BASE_SPIKE)
                del metadata[key]
                directory, temp = self.write_spike(metadata)
                with temp:
                    result = self.run_spike(directory, "--contract")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(key, result.stdout)

    def test_complete_rejects_missing_post_run_evidence(self) -> None:
        metadata = copy.deepcopy(BASE_SPIKE)
        metadata["status"] = "passed"
        directory, temp = self.write_spike(metadata)
        with temp:
            result = self.run_spike(directory, "--complete")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("measurements", result.stdout)

    def test_complete_requires_five_raw_values_range_and_median_for_browser_measurement(self) -> None:
        metadata = copy.deepcopy(BASE_SPIKE)
        metadata.update(
            {
                "status": "passed",
                "environmentFacts": {"browser": "Firefox 152", "runtime": "CPython 3.14"},
                "measurements": [
                    {
                        "name": "fixture-duration-ms",
                        "nondeterministic": True,
                        "rawValues": [10, 12, 11, 10],
                        "range": {"min": 10, "max": 12},
                        "median": 10.5,
                    }
                ],
                "rawOutputDigests": [{"path": "raw.txt", "sha256": "a" * 64}],
                "replayResult": {"status": "passed", "outputDigest": "b" * 64},
                "evidenceLinks": [{"kind": "measurement", "path": "raw.txt", "sha256": "a" * 64}],
            }
        )
        directory, temp = self.write_spike(metadata, VALID_ENVIRONMENT)
        with temp:
            result = self.run_spike(directory, "--complete")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("rawValues", result.stdout)

    def test_complete_accepts_blocked_spike_with_retained_inputs_and_local_replay_result(self) -> None:
        metadata = copy.deepcopy(BASE_SPIKE)
        metadata.update(
            {
                "status": "blocked",
                "blocked": {
                    "reason": "Required browser capability is unavailable in the fixture.",
                    "affectedRequirements": ["EVID-04"],
                    "affectedAdrs": ["ADR-0005"],
                },
                "environmentFacts": {"browser": "Chrome 150", "runtime": "CPython 3.14"},
                "measurements": [{"name": "fixture-result", "nondeterministic": True, "rawValues": [1, 1, 1, 1, 1], "range": {"min": 1, "max": 1}, "median": 1}],
                "rawOutputDigests": [{"path": "raw.txt", "sha256": "a" * 64}],
                "replayResult": {"status": "blocked", "outputDigest": "b" * 64},
                "evidenceLinks": [{"kind": "measurement", "path": "raw.txt", "sha256": "a" * 64}],
            }
        )
        directory, temp = self.write_spike(metadata, VALID_ENVIRONMENT)
        with temp:
            result = self.run_spike(directory, "--complete")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
