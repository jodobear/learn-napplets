"""Disposable SPK envelope validation tests."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
        raw_bytes = b"blocked fixture output\n"
        raw_digest = hashlib.sha256(raw_bytes).hexdigest()
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
                "rawOutputDigests": [{"path": "raw.txt", "sha256": raw_digest}],
                "replayResult": {"status": "blocked", "outputDigest": raw_digest},
                "evidenceLinks": [{"kind": "measurement", "path": "raw.txt", "sha256": raw_digest}],
            }
        )
        directory, temp = self.write_spike(metadata, VALID_ENVIRONMENT)
        with temp:
            (directory / "raw.txt").write_bytes(raw_bytes)
            result = self.run_spike(directory, "--complete")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_complete_spike_requires_retained_output_and_bound_replay_digest(self) -> None:
        raw_bytes = b"retained local evidence\n"
        raw_digest = hashlib.sha256(raw_bytes).hexdigest()

        def completed_metadata() -> dict:
            metadata = copy.deepcopy(BASE_SPIKE)
            metadata.update(
                {
                    "status": "passed",
                    "environmentFacts": {"browser": "Firefox 152", "runtime": "CPython 3.14"},
                    "measurements": [{"name": "fixture-result", "nondeterministic": True, "rawValues": [1, 1, 1, 1, 1], "range": {"min": 1, "max": 1}, "median": 1}],
                    "rawOutputDigests": [{"path": "raw.txt", "sha256": raw_digest}],
                    "replayResult": {"status": "passed", "outputDigest": raw_digest},
                    "evidenceLinks": [{"kind": "measurement", "path": "raw.txt", "sha256": raw_digest}],
                }
            )
            return metadata

        metadata = completed_metadata()
        directory, temp = self.write_spike(metadata, VALID_ENVIRONMENT)
        with temp:
            (directory / "raw.txt").write_bytes(raw_bytes)
            result = self.run_spike(directory, "--complete")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        cases = {
            "empty-declarations": lambda record: record.__setitem__("rawOutputDigests", []),
            "null-declaration": lambda record: record.__setitem__("rawOutputDigests", None),
            "absolute-path": lambda record: record["rawOutputDigests"][0].__setitem__("path", "/tmp/raw.txt"),
            "traversing-path": lambda record: record["rawOutputDigests"][0].__setitem__("path", "../raw.txt"),
            "nul-path": lambda record: record["rawOutputDigests"][0].__setitem__("path", "raw\\x00.txt"),
            "duplicate-normalized-path": lambda record: record["rawOutputDigests"].append({"path": "./raw.txt", "sha256": raw_digest}),
            "unbound-replay-digest": lambda record: record["replayResult"].__setitem__("outputDigest", "f" * 64),
            "unbound-evidence-link": lambda record: record["evidenceLinks"][0].__setitem__("sha256", "e" * 64),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                metadata = completed_metadata()
                mutate(metadata)
                directory, temp = self.write_spike(metadata, VALID_ENVIRONMENT)
                with temp:
                    (directory / "raw.txt").write_bytes(raw_bytes)
                    result = self.run_spike(directory, "--complete")
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

        for name, path in (("missing-file", "raw.txt"), ("directory", "output-dir"), ("symlink", "output-link"), ("altered-bytes", "raw.txt")):
            with self.subTest(name=name):
                metadata = completed_metadata()
                metadata["rawOutputDigests"][0]["path"] = path
                metadata["evidenceLinks"][0]["path"] = path
                directory, temp = self.write_spike(metadata, VALID_ENVIRONMENT)
                with temp:
                    if name == "directory":
                        (directory / path).mkdir()
                    elif name == "symlink":
                        (directory / "source.txt").write_bytes(raw_bytes)
                        (directory / path).symlink_to("source.txt")
                    elif name == "altered-bytes":
                        (directory / path).write_bytes(b"altered local evidence\n")
                    result = self.run_spike(directory, "--complete")
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_replay_mapping_rejects_manifest_command_substitution(self) -> None:
        spec = importlib.util.spec_from_file_location("validate_research_for_test", VALIDATOR)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(module)
        expected_prefix = ["tools/phase1-python", "tools/validate-research.py", "validate-spike"]
        for spike_id, directory in module.SPIKE_REPORTS.items():
            with self.subTest(spike_id=spike_id):
                self.assertEqual(
                    module.expected_replay_argv(spike_id, ROOT),
                    [*expected_prefix, f".planning/spikes/{directory}", "--complete"],
                )

        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = Path(temporary) / "replay-manifest.yaml"
            manifest_path.write_text(
                yaml.safe_dump({"entries": [{"spikeId": spike_id, "replayCommand": "python -c 'raise SystemExit(99)'"} for spike_id in module.SPIKE_REPORTS]}),
                encoding="utf-8",
            )
            completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
            with mock.patch.object(module, "validate_replay_manifest", return_value=[]), mock.patch.object(module.subprocess, "run", return_value=completed) as run:
                errors = module.replay_spikes(manifest_path, ROOT / ".planning")
            self.assertEqual(errors, [])
            self.assertEqual(
                [call.args[0] for call in run.call_args_list],
                [module.expected_replay_argv(spike_id, ROOT) for spike_id in module.SPIKE_REPORTS],
            )


if __name__ == "__main__":
    unittest.main()
