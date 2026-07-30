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


    def load_spk_g_runner(self):
        runner = ROOT / "tools" / "measure-package-conformance.py"
        spec = importlib.util.spec_from_file_location("measure_package_conformance", runner)
        self.assertIsNotNone(spec, "SPK-G runner must be importable")
        module = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader, "SPK-G runner must have a loader")
        spec.loader.exec_module(module)
        return module

    def spk_g_snapshot(self, module, *, qualified: bool = False) -> dict[str, bytes]:
        dimensions = [
            {"name": name, "status": "qualified" if qualified else "blocked"}
            for name in module.COMPATIBILITY_DIMENSIONS
        ]
        compatibility = {
            "compatibility": [{
                "id": "CMP-BASELINE-001",
                "dimensions": dimensions,
                "baselineEligibility": {
                    "status": "eligible" if qualified else "blocked",
                    "approval": "approved" if qualified else "not-approved",
                    "reviewRecordId": "APR-PACKAGE-001" if qualified else None,
                },
            }],
        }
        artifact = {
            "status": "qualified" if qualified else "blocked",
            "packageName": "example-package" if qualified else None,
            "version": "1.2.3" if qualified else None,
            "tarballIntegrity": "sha512-example" if qualified else None,
            "provenance": "https://registry.example.invalid/example-package" if qualified else None,
            "license": "MIT" if qualified else None,
            "rootExport": "example-package" if qualified else None,
            "releasedSourceId": "SRC-RELEASE-001" if qualified else None,
            "implementationSourceId": "SRC-IMPLEMENTATION-001" if qualified else None,
            "runtimeInput": "runtime-fixture" if qualified else None,
            "exampleInput": "example-fixture" if qualified else None,
            "fixtureInput": "root-export-fixture" if qualified else None,
            "conformanceInput": "root-export-conformance" if qualified else None,
        }
        sources = {
            "sources": [
                {"id": source_id, "collectionStatus": "collected", "review": {"status": "approved"}, "freshness": {"state": "current"}}
                for source_id in ("SRC-RELEASE-001", "SRC-IMPLEMENTATION-001")
            ],
        }
        package = {
            "artifactEvidence": artifact,
            "approval": "approved" if qualified else "not-approved",
            "packageDecision": {
                "status": "approved" if qualified else "blocked",
                "reviewedAt": "2026-07-30" if qualified else None,
            },
        }
        documents = {
            "research/compatibility-matrix.yaml": compatibility,
            "research/package-evidence.yaml": package,
            "research/source-registry.yaml": sources,
            "research/claims.yaml": {"claims": []},
            "research/drift-register.yaml": {"drift": []},
            "research/open-questions.yaml": {"questions": []},
        }
        return {name: yaml.safe_dump(documents[name], sort_keys=False).encode("utf-8") for name in module.SPK_G_SNAPSHOT_TARGETS}

    def test_spk_g_measurement_requires_qualified_eligibility_and_approval(self) -> None:
        module = self.load_spk_g_runner()
        attempted: list[list[str]] = []
        blocked = module.run_spk_g(
            self.spk_g_snapshot(module),
            sandbox_probe=lambda: module.SandboxContract.unavailable("NO_SANDBOX"),
            operation_runner=lambda argv, workspace: attempted.append(argv),
        )
        self.assertEqual(blocked["status"], "SPK-G-BLOCKED-ELIGIBILITY")
        self.assertIn("DIMENSION_NORMATIVE_PROTOCOL_BLOCKED", blocked["reasons"])
        self.assertEqual(attempted, [])

        missing_artifact = self.spk_g_snapshot(module, qualified=True)
        package = yaml.safe_load(missing_artifact["research/package-evidence.yaml"])
        package["artifactEvidence"].pop("license")
        missing_artifact["research/package-evidence.yaml"] = yaml.safe_dump(package, sort_keys=False).encode("utf-8")
        result = module.run_spk_g(missing_artifact, sandbox_probe=lambda: module.SandboxContract.unavailable("NO_SANDBOX"))
        self.assertEqual(result["status"], "SPK-G-BLOCKED-ELIGIBILITY")
        self.assertIn("PACKAGE_LICENSE_MISSING", result["reasons"])

    def test_spk_g_sandbox_blocks_unavailable_or_escape_prone_execution(self) -> None:
        module = self.load_spk_g_runner()
        attempted: list[list[str]] = []
        for reason in ("NO_USER_NAMESPACE", "NETWORK_REACHABLE", "REPOSITORY_WRITABLE", "SECRET_ENVIRONMENT", "RESOURCE_LIMITS_MISSING"):
            with self.subTest(reason=reason):
                result = module.run_spk_g(
                    self.spk_g_snapshot(module, qualified=True),
                    sandbox_probe=lambda reason=reason: module.SandboxContract.unavailable(reason),
                    operation_runner=lambda argv, workspace: attempted.append(argv),
                )
                self.assertEqual(result["status"], "SPK-G-BLOCKED-SANDBOX-UNAVAILABLE")
                self.assertEqual(result["reasons"], [reason])
        self.assertEqual(attempted, [])

    def test_spk_g_reader_reads_one_transactional_snapshot_or_refuses(self) -> None:
        module = self.load_spk_g_runner()
        parsed = 0
        attempted: list[list[str]] = []

        def refusing_reader():
            raise module.SnapshotRefused("CANONICAL_LOCK_CONFLICT")

        refused = module.run_spk_g(
            snapshot_reader=refusing_reader,
            parser_observer=lambda: self.fail("canonical parsing occurred after snapshot refusal"),
            operation_runner=lambda argv, workspace: attempted.append(argv),
        )
        self.assertEqual(refused["status"], "SPK-G-BLOCKED-CANONICAL-SNAPSHOT-REFUSED")
        self.assertEqual(attempted, [])

        recovery_spec = importlib.util.spec_from_file_location("canonical_recovery_for_spk_g", ROOT / "tools" / "canonical-recovery.py")
        self.assertIsNotNone(recovery_spec)
        recovery = importlib.util.module_from_spec(recovery_spec)
        self.assertIsNotNone(recovery_spec.loader)
        recovery_spec.loader.exec_module(recovery)
        old = self.spk_g_snapshot(module)
        new = dict(old)
        new["research/package-evidence.yaml"] = new["research/package-evidence.yaml"].replace(b"not-approved", b"approved")
        with tempfile.TemporaryDirectory() as temporary:
            planning = Path(temporary)
            for target, content in old.items():
                path = planning / target
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            recovery.register_canonical_reader("spk-g-mixed-journal-fixture", module.SPK_G_SNAPSHOT_TARGETS)
            with self.assertRaises(recovery.PublishInterrupted):
                recovery.publish_generation(planning, new, interrupt_after=0)

            def observed_parser():
                nonlocal parsed
                parsed += 1

            complete = module.run_spk_g(
                snapshot_reader=lambda: recovery.read_canonical_snapshot("spk-g-mixed-journal-fixture", module.SPK_G_SNAPSHOT_TARGETS, root=planning),
                parser_observer=observed_parser,
                sandbox_probe=lambda: module.SandboxContract.unavailable("NO_SANDBOX"),
            )
        self.assertEqual(parsed, 1)
        self.assertEqual(complete["status"], "SPK-G-BLOCKED-ELIGIBILITY")
        self.assertEqual(attempted, [])

    def test_spk_g_retains_evidence_only_after_complete_result_validation(self) -> None:
        module = self.load_spk_g_runner()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            targets = {name: root / name for name in ("measurements.yaml", "report.md", "impact-fragment.yaml")}
            original = {name: f"old-{name}\n".encode("utf-8") for name in targets}
            for name, path in targets.items():
                path.write_bytes(original[name])
            candidate = {name: f"new-{name}\n".encode("utf-8") for name in targets}
            workspace = root / "candidate"
            workspace.mkdir()
            for name, value in candidate.items():
                (workspace / name).write_bytes(value)
            with self.assertRaises(module.ReceiptValidationError):
                module.retain_validated_bundle(workspace, targets, validator=lambda _: ["receipt invalid"])
            self.assertFalse(workspace.exists())
            self.assertEqual({name: path.read_bytes() for name, path in targets.items()}, original)


if __name__ == "__main__":
    unittest.main()
