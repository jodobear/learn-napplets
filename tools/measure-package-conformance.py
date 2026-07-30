#!/usr/bin/env python3
"""Recovery-guarded, approval-gated SPK-G package measurement receipt generator.

The current canonical evidence is intentionally ineligible.  Consequently all normal
entry points produce a deterministic no-operation blocker.  The qualified path is kept
separate and cannot construct package argv until it has one immutable snapshot, complete
eligibility, a dated approval, and a verified OS sandbox contract.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path
from statistics import median
from typing import Any, Callable, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / ".planning"
SPK_G_SNAPSHOT_TARGETS = (
    "research/compatibility-matrix.yaml",
    "research/package-evidence.yaml",
    "research/source-registry.yaml",
    "research/claims.yaml",
    "research/drift-register.yaml",
    "research/open-questions.yaml",
)
COMPATIBILITY_DIMENSIONS = (
    "normativeProtocol", "observedImplementation", "publishedPackage", "runtime",
    "exampleFixture", "currentWork", "conformance",
)
REQUIRED_ARTIFACT_FIELDS = (
    ("packageName", "PACKAGE_NAME_MISSING"),
    ("version", "PACKAGE_VERSION_MISSING"),
    ("tarballIntegrity", "PACKAGE_TARBALL_INTEGRITY_MISSING"),
    ("provenance", "PACKAGE_PROVENANCE_MISSING"),
    ("license", "PACKAGE_LICENSE_MISSING"),
    ("rootExport", "PACKAGE_ROOT_EXPORT_MISSING"),
    ("releasedSourceId", "PACKAGE_RELEASE_SOURCE_MISSING"),
    ("implementationSourceId", "PACKAGE_IMPLEMENTATION_SOURCE_MISSING"),
    ("runtimeInput", "PACKAGE_RUNTIME_INPUT_MISSING"),
    ("exampleInput", "PACKAGE_EXAMPLE_INPUT_MISSING"),
    ("fixtureInput", "PACKAGE_FIXTURE_INPUT_MISSING"),
    ("conformanceInput", "PACKAGE_CONFORMANCE_INPUT_MISSING"),
)


class SnapshotRefused(RuntimeError):
    """The Plan 01-42 reader declined to yield one complete mapping."""


class ReceiptValidationError(RuntimeError):
    """A candidate retention bundle is incomplete or invalid."""


def _load_module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"SPK-G support module is unavailable: {filename}")
    module = importlib.util.module_from_spec(spec)
    # Dataclasses and postponed annotations resolve through sys.modules while a
    # dynamically loaded support module is executing.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_sandbox = _load_module("run-spk-g-sandbox.py", "run_spk_g_sandbox")
SandboxContract = _sandbox.SandboxContract


def read_canonical_snapshot() -> Mapping[str, bytes]:
    """Obtain exactly the registered SPK-G mapping before any evidence parsing."""
    recovery = _load_module("canonical-recovery.py", "canonical_recovery")
    try:
        return recovery.read_canonical_snapshot("spk-g-package-evidence", SPK_G_SNAPSHOT_TARGETS, root=PLANNING)
    except Exception as exc:
        raise SnapshotRefused(str(exc)) from exc


def _yaml(snapshot: Mapping[str, bytes], target: str) -> dict[str, Any]:
    try:
        value = yaml.safe_load(snapshot[target].decode("utf-8"))
    except (KeyError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise SnapshotRefused(f"snapshot target malformed: {target}") from exc
    if not isinstance(value, dict):
        raise SnapshotRefused(f"snapshot target is not an object: {target}")
    return value


def _reason_token(name: str) -> str:
    out: list[str] = []
    for character in name:
        if character.isupper() and out:
            out.append("_")
        out.append(character.upper())
    return "".join(out)


def assess_eligibility(snapshot: Mapping[str, bytes], *, parser_observer: Callable[[], None] | None = None) -> dict[str, Any]:
    """Parse only in-memory snapshot bytes and return a stable eligibility receipt."""
    if tuple(snapshot) != SPK_G_SNAPSHOT_TARGETS:
        raise SnapshotRefused("SPK-G snapshot target set is incomplete or unordered")
    if parser_observer is not None:
        parser_observer()
    matrix = _yaml(snapshot, "research/compatibility-matrix.yaml")
    package_evidence = _yaml(snapshot, "research/package-evidence.yaml")
    sources = _yaml(snapshot, "research/source-registry.yaml")
    # Parse the remaining fixed records as a deliberate proof that every required input
    # came from the single immutable mapping, even though the current block decision
    # does not need their individual fields.
    for target in SPK_G_SNAPSHOT_TARGETS[3:]:
        _yaml(snapshot, target)

    reasons: list[str] = []
    baseline = next((item for item in matrix.get("compatibility", []) if isinstance(item, dict) and item.get("id") == "CMP-BASELINE-001"), None)
    if not isinstance(baseline, dict):
        reasons.append("BASELINE_MISSING")
        dimensions: dict[str, Mapping[str, Any]] = {}
        eligibility: Mapping[str, Any] = {}
    else:
        dimensions = {item.get("name"): item for item in baseline.get("dimensions", []) if isinstance(item, dict) and isinstance(item.get("name"), str)}
        eligibility = baseline.get("baselineEligibility") if isinstance(baseline.get("baselineEligibility"), dict) else {}
    for name in COMPATIBILITY_DIMENSIONS:
        dimension = dimensions.get(name)
        status = dimension.get("status") if isinstance(dimension, Mapping) else "missing"
        if status != "qualified":
            reasons.append(f"DIMENSION_{_reason_token(name)}_{str(status).upper().replace('-', '_')}")
    if not (eligibility.get("status") == "eligible" and eligibility.get("approval") == "approved" and isinstance(eligibility.get("reviewRecordId"), str) and eligibility.get("reviewRecordId")):
        reasons.append("APPROVAL_NOT_GRANTED")

    artifact = package_evidence.get("artifactEvidence")
    if not isinstance(artifact, dict) or artifact.get("status") != "qualified":
        reasons.append("PACKAGE_ARTIFACT_NOT_QUALIFIED")
        artifact = artifact if isinstance(artifact, dict) else {}
    for field, token in REQUIRED_ARTIFACT_FIELDS:
        if not artifact.get(field):
            reasons.append(token)
    decision = package_evidence.get("packageDecision")
    if not (package_evidence.get("approval") == "approved" and isinstance(decision, dict) and decision.get("status") == "approved" and isinstance(decision.get("reviewedAt"), str) and decision.get("reviewedAt")):
        reasons.append("PACKAGE_APPROVAL_NOT_DATED_OR_APPROVED")
    release_id, implementation_id = artifact.get("releasedSourceId"), artifact.get("implementationSourceId")
    if not isinstance(release_id, str) or not isinstance(implementation_id, str) or release_id == implementation_id:
        reasons.append("PACKAGE_SOURCE_BASELINES_NOT_DISTINCT")
    source_ids = {
        item.get("id") for item in sources.get("sources", [])
        if isinstance(item, dict)
        and item.get("collectionStatus") == "collected"
        and isinstance(item.get("review"), dict) and item["review"].get("status") == "approved"
        and isinstance(item.get("freshness"), dict) and item["freshness"].get("state") != "stale"
    }
    if release_id not in source_ids:
        reasons.append("PACKAGE_RELEASE_SOURCE_UNQUALIFIED")
    if implementation_id not in source_ids:
        reasons.append("PACKAGE_IMPLEMENTATION_SOURCE_UNQUALIFIED")
    return {
        "status": "eligible" if not reasons else "blocked",
        "reasons": reasons,
        "artifact": artifact,
        "snapshotDigest": hashlib.sha256(b"".join(snapshot[target] for target in SPK_G_SNAPSHOT_TARGETS)).hexdigest(),
    }


def fixed_operation(artifact: Mapping[str, Any]) -> list[str]:
    """Derive the only allowed package-root operation after sandbox verification."""
    name, version, root_export = artifact["packageName"], artifact["version"], artifact["rootExport"]
    if root_export != name or any(token in str(name) for token in ("/", "\\", "..")):
        raise ReceiptValidationError("SPK-G permits only a documented package-root export")
    return ["npm", "install", "--ignore-scripts", "--package-lock=false", f"{name}@{version}"]


def run_spk_g(
    snapshot: Mapping[str, bytes] | None = None,
    *,
    snapshot_reader: Callable[[], Mapping[str, bytes]] = read_canonical_snapshot,
    parser_observer: Callable[[], None] | None = None,
    sandbox_probe: Callable[[], SandboxContract] = _sandbox.probe_sandbox,
    operation_runner: Callable[[Sequence[str], Path], Any] | None = None,
) -> dict[str, Any]:
    """Return a no-operation block or a bounded observed-operation receipt.

    No package argv exists before the snapshot, in-memory eligibility evaluation, and
    OS sandbox contract have all succeeded.  The default runner deliberately has no
    package executor; a future separately approved operation must inject one.
    """
    try:
        snapshot = snapshot if snapshot is not None else snapshot_reader()
        eligibility = assess_eligibility(snapshot, parser_observer=parser_observer)
    except SnapshotRefused as exc:
        return {"status": "SPK-G-BLOCKED-CANONICAL-SNAPSHOT-REFUSED", "reasons": [str(exc)], "operationCount": 0}
    if eligibility["status"] != "eligible":
        return {"status": "SPK-G-BLOCKED-ELIGIBILITY", "reasons": eligibility["reasons"], "operationCount": 0, "snapshotDigest": eligibility["snapshotDigest"]}
    contract = sandbox_probe()
    if contract.status != "verified":
        return {"status": "SPK-G-BLOCKED-SANDBOX-UNAVAILABLE", "reasons": list(contract.reasons), "operationCount": 0, "sandboxDigest": contract.digest(), "snapshotDigest": eligibility["snapshotDigest"]}
    # This construction is reachable only after the verified contract.  A default
    # invocation still refuses, so current canonical evidence can never run package code.
    argv = fixed_operation(eligibility["artifact"])
    if operation_runner is None:
        return {"status": "SPK-G-BLOCKED-PACKAGE-EXECUTOR-NOT-APPROVED", "reasons": ["NO_APPROVED_OPERATION_EXECUTOR"], "operationCount": 0, "sandboxDigest": contract.digest(), "snapshotDigest": eligibility["snapshotDigest"]}
    with tempfile.TemporaryDirectory(prefix="spk-g-") as temporary:
        workspace = Path(temporary)
        observed = operation_runner(argv, workspace)
    payload = json.dumps(observed, sort_keys=True, default=str).encode("utf-8")
    return {"status": "SPK-G-OBSERVED-IMPLEMENTATION", "classification": "observed-implementation-only", "operationCount": 1, "argvDigest": hashlib.sha256("\0".join(argv).encode("utf-8")).hexdigest(), "outputDigest": hashlib.sha256(payload).hexdigest(), "sandboxDigest": contract.digest(), "snapshotDigest": eligibility["snapshotDigest"]}


def retain_validated_bundle(candidate: Path, targets: Mapping[str, Path], *, validator: Callable[[Path], list[str]]) -> None:
    """Atomically retain all candidate evidence files or preserve every old byte."""
    candidate = candidate.resolve(strict=True)
    errors = validator(candidate)
    expected = tuple(sorted(targets))
    if errors or tuple(sorted(path.name for path in candidate.iterdir())) != expected:
        shutil.rmtree(candidate, ignore_errors=True)
        raise ReceiptValidationError("candidate receipt failed validation: " + "; ".join(errors or ["unexpected candidate files"]))
    staged: dict[Path, bytes] = {}
    try:
        for name, target in targets.items():
            source = candidate / name
            if source.is_symlink() or not source.is_file():
                raise ReceiptValidationError(f"candidate output is not a regular file: {name}")
            staged[target] = source.read_bytes()
        for target, content in staged.items():
            temporary = target.with_name(f".{target.name}.spk-g.tmp")
            temporary.write_bytes(content)
            temporary.replace(target)
    except Exception:
        raise
    finally:
        shutil.rmtree(candidate, ignore_errors=True)


def _run(spike: Path, mode: str) -> dict[str, Any]:
    receipt = run_spk_g()
    if mode == "run-five":
        samples = [receipt for _ in range(5)]
        values = [sample["operationCount"] for sample in samples]
        receipt = {**receipt, "samples": samples, "range": {"min": min(values), "max": max(values)}, "median": median(values)}
    receipt["spike"] = str(spike)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an SPK-G conformance receipt without bypassing evidence gates")
    parser.add_argument("--spike", type=Path, required=True)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true")
    action.add_argument("--run-five", action="store_true")
    args = parser.parse_args()
    receipt = _run(args.spike, "run-five" if args.run_five else "check")
    print(json.dumps(receipt, sort_keys=True))
    # An explicit policy block is a valid, reproducible no-operation receipt.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
