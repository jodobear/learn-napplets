#!/usr/bin/env python3
"""Verify and certify the Phase 1 offline wheelhouse using only the standard library."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile
from email.parser import BytesParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
APPROVED_TOP_LEVEL = {"pyyaml": "6.0.3", "jsonschema": "4.26.0", "playwright": "1.61.0"}


def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def json_digest(value: Any) -> str:
    return digest_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def fail(message: str) -> None:
    raise ValueError(f"toolchain: {message}")


def repository_relative(path: Path) -> str:
    """Return a non-escaping repo-relative reference, never a host path."""
    root = ROOT.absolute()
    candidate = path.absolute()
    if root not in (candidate, *candidate.parents):
        fail(f"path escapes repository root: {path}")
    return candidate.relative_to(root).as_posix()


def resolve_repository_relative(value: object, label: str) -> Path:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a nonempty repo-relative path")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(f"{label} must be repo-relative and non-escaping")
    resolved = (ROOT / candidate).absolute()
    root = ROOT.absolute()
    if root not in (resolved, *resolved.parents):
        fail(f"{label} escapes repository root")
    return resolved


def file_url_wheel_filename(value: object) -> str:
    """Accept a historical file URL but bind it to the current wheelhouse bytes."""
    if not isinstance(value, str):
        fail("installer report must identify a file:// wheelhouse archive")
    parsed = urlparse(value)
    if parsed.scheme != "file" or parsed.netloc or parsed.query or parsed.fragment:
        fail("installer report must identify a plain file:// wheelhouse archive")
    decoded = unquote(parsed.path)
    filename = Path(decoded).name
    if not filename or filename in {".", ".."}:
        fail("installer report archive lacks a wheel filename")
    return filename


def parse_lock(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        fail(f"missing lock file: {path}")
    entries: dict[str, dict[str, str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("--"):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s]+)\s+--hash=sha256:([0-9a-f]{64})", line)
        if not match:
            fail(f"lock entry is not exact and hash-required: {line}")
        name, version, archive_hash = match.groups()
        key = normalized(name)
        if key in entries:
            fail(f"duplicate lock distribution: {name}")
        entries[key] = {"name": key, "version": version, "sha256": archive_hash}
    if not entries:
        fail("lock contains no distributions")
    return entries


def wheel_info(path: Path) -> dict[str, Any]:
    if path.suffix != ".whl":
        fail(f"source distribution or non-wheel archive present: {path.name}")
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
            record_names = [name for name in names if name.endswith(".dist-info/RECORD")]
            wheel_names = [name for name in names if name.endswith(".dist-info/WHEEL")]
            if len(metadata_names) != 1 or len(record_names) != 1 or len(wheel_names) != 1:
                fail(f"wheel metadata is incomplete or ambiguous: {path.name}")
            metadata = BytesParser().parsebytes(archive.read(metadata_names[0]))
            name = metadata.get("Name")
            version = metadata.get("Version")
            if not name or not version:
                fail(f"wheel metadata lacks Name or Version: {path.name}")
            wheel = archive.read(wheel_names[0]).decode("utf-8", errors="strict")
            tags = [line.split(":", 1)[1].strip() for line in wheel.splitlines() if line.startswith("Tag:")]
            if not tags or not any(tag == "py3-none-any" or (tag.startswith("py3-none-") and "x86_64" in tag and "linux" in tag) or ("cp314" in tag and "x86_64" in tag and "linux" in tag) for tag in tags):
                fail(f"wheel is foreign-platform or incompatible: {path.name}")
            records: dict[str, str] = {}
            for row in csv.reader(archive.read(record_names[0]).decode("utf-8", errors="strict").splitlines()):
                if len(row) != 3:
                    fail(f"wheel RECORD row is malformed: {path.name}")
                entry, checksum, _size = row
                if entry in records:
                    fail(f"wheel RECORD has duplicate path: {path.name}")
                records[entry] = checksum
            return {
                "normalizedName": normalized(name),
                "version": version,
                "filename": path.name,
                "sha256": digest_file(path),
                "metadataSha256": digest_bytes(archive.read(metadata_names[0])),
                "wheelSha256": digest_bytes(archive.read(wheel_names[0])),
                "record": records,
            }
    except zipfile.BadZipFile as exc:
        raise ValueError(f"toolchain: invalid wheel archive: {path.name}") from exc


def policy_scope(path: Path, lock: dict[str, dict[str, str]]) -> dict[str, str]:
    if not path.is_file():
        fail(f"missing approval policy: {path}")
    text = path.read_text(encoding="utf-8")
    for name, version in APPROVED_TOP_LEVEL.items():
        display = {"pyyaml": "PyYAML", "jsonschema": "jsonschema", "playwright": "playwright"}[name]
        if not re.search(rf"- name: {re.escape(display)}\n\s+version: {re.escape(version)}\n\s+status: approved", text):
            fail(f"top-level approval is missing or changed for {display}=={version}")
    for marker in ("identifier: MIT\n      decision: approved", "identifier: Apache-2.0\n      decision: approved"):
        if marker not in text:
            fail("license policy is missing an approved top-level license decision")
    unexpected = set(APPROVED_TOP_LEVEL).difference(lock)
    if unexpected:
        fail("approved top-level scope is missing from the derived closure")
    result: dict[str, str] = {}
    for name, entry in lock.items():
        if name in APPROVED_TOP_LEVEL:
            if entry["version"] != APPROVED_TOP_LEVEL[name]:
                fail(f"top-level scope change requires escalation: {name}=={entry['version']}")
            result[name] = "approved-top-level"
        else:
            result[name] = "derived-in-scope"
    return result


def inspect_wheelhouse(wheelhouse: Path, lock: dict[str, dict[str, str]], policy: dict[str, str]) -> list[dict[str, Any]]:
    if not wheelhouse.is_dir():
        fail(f"missing wheelhouse: {wheelhouse}")
    archives = sorted(path for path in wheelhouse.iterdir() if path.is_file())
    if not archives:
        fail("wheelhouse is empty")
    observed: dict[str, dict[str, Any]] = {}
    for archive in archives:
        info = wheel_info(archive)
        name = info["normalizedName"]
        if name in observed:
            fail(f"duplicate wheel archive for distribution: {name}")
        observed[name] = info
    if set(observed) != set(lock):
        missing = sorted(set(lock).difference(observed))
        surplus = sorted(set(observed).difference(lock))
        fail(f"wheelhouse closure mismatch; missing={missing}; surplus={surplus}")
    records: list[dict[str, Any]] = []
    for name in sorted(lock):
        expected = lock[name]
        actual = observed[name]
        if actual["version"] != expected["version"]:
            fail(f"wheel version differs from lock: {actual['filename']}")
        if actual["sha256"] != expected["sha256"]:
            fail(f"wheel archive hash differs from lock: {actual['filename']}")
        actual["policy"] = policy[name]
        records.append(actual)
    return records


def manifest_for(lock_path: Path, policy_path: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "lockSha256": digest_file(lock_path),
        "policySha256": digest_file(policy_path),
        "wheels": [{key: value for key, value in record.items() if key != "record"} for record in records],
    }


def verify_manifest(path: Path, expected: dict[str, Any]) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing wheelhouse manifest: {path}")
    try:
        actual = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("toolchain: wheelhouse manifest is invalid JSON") from exc
    if actual != expected:
        fail("wheelhouse manifest does not bind the verified lock, policy, and archives")
    return actual


def verify_report(report_path: Path, wheelhouse: Path, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not report_path.is_file():
        fail(f"missing installer report: {report_path}")
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        installed = report["install"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError("toolchain: installer report is malformed") from exc
    expected = {record["normalizedName"]: record for record in records}
    mapping: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in installed:
        metadata = item.get("metadata", {})
        name = normalized(str(metadata.get("name", "")))
        version = str(metadata.get("version", ""))
        filename = file_url_wheel_filename(item.get("download_info", {}).get("url"))
        source = wheelhouse / filename
        if name not in expected or name in seen:
            fail("installer report has undeclared or duplicate distribution")
        wheel = expected[name]
        if not source.is_file() or version != wheel["version"] or filename != wheel["filename"] or digest_file(source) != wheel["sha256"]:
            fail("installer report does not bind distribution to its verified archive")
        seen.add(name)
        mapping.append({"normalizedName": name, "version": version, "wheel": source.name, "sha256": wheel["sha256"]})
    if seen != set(expected):
        fail("installer report omits a declared distribution")
    return sorted(mapping, key=lambda item: item["normalizedName"])


def installed_record_relative(wheel_relative: str, distribution: str = "") -> str:
    """Translate wheel .data RECORD paths into pip's installed RECORD spelling."""
    parts = wheel_relative.split("/")
    if len(parts) >= 3 and parts[0].endswith(".data"):
        scheme, remainder = parts[1], "/".join(parts[2:])
        if scheme in {"purelib", "platlib"}:
            return remainder
        if scheme == "headers":
            if not distribution:
                fail("wheel header RECORD mapping requires a distribution name")
            return f"../../../include/site/python{sys.version_info.major}.{sys.version_info.minor}/{distribution}/{remainder}"
        if scheme == "scripts":
            return f"../../../bin/{remainder}"
        fail(f"wheel RECORD uses unsupported installation scheme: {scheme}")
    return wheel_relative


def verify_installed_records(target: Path, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    site = target / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    if not site.is_dir():
        fail("fresh target site-packages is unavailable")
    expected = {record["normalizedName"]: record for record in records}
    installed: dict[str, Path] = {}
    for dist_info in site.glob("*.dist-info"):
        metadata_path = dist_info / "METADATA"
        if not metadata_path.is_file():
            fail("installed distribution lacks METADATA")
        metadata = BytesParser().parsebytes(metadata_path.read_bytes())
        name = normalized(str(metadata.get("Name", "")))
        version = str(metadata.get("Version", ""))
        if name in installed or name not in expected or version != expected[name]["version"]:
            fail("target inventory has undeclared, duplicate, or wrong-version distribution")
        installed[name] = dist_info
    if set(installed) != set(expected):
        fail("target inventory does not match closure")
    results: list[dict[str, Any]] = []
    for name, wheel in sorted(expected.items()):
        actual_records: dict[str, str] = {}
        record_path = installed[name] / "RECORD"
        if not record_path.is_file():
            fail("installed distribution lacks RECORD")
        for row in csv.reader(record_path.read_text(encoding="utf-8").splitlines()):
            if len(row) != 3 or row[0] in actual_records:
                fail("installed RECORD is malformed")
            actual_records[row[0]] = row[1]
        for relative, expected_hash in wheel["record"].items():
            if not expected_hash:
                continue
            installed_relative = installed_record_relative(relative, name)
            installed_path = (site / installed_relative).resolve()
            if target.resolve() not in (installed_path, *installed_path.parents) or not installed_path.is_file():
                fail("installed RECORD path is missing or escapes the target")
            encoded = base64.urlsafe_b64encode(hashlib.sha256(installed_path.read_bytes()).digest()).decode("ascii").rstrip("=")
            actual_hash = actual_records.get(installed_relative)
            if expected_hash != f"sha256={encoded}" or actual_hash != expected_hash:
                fail("installed file fails wheel and installed RECORD comparison")
        results.append({"normalizedName": name, "recordVerified": True, "installedRecordSha256": digest_file(record_path)})
    return results


def verify_all(lock: Path, policy: Path, wheelhouse: Path, manifest: Path, report: Path, target: Path, attestation: Path) -> dict[str, Any]:
    # All runtime inputs remain below the checkout. This prevents a copied
    # attestation from silently selecting a prior worktree or ambient target.
    repository_relative(wheelhouse)
    repository_relative(report)
    repository_relative(target)
    lock_entries = parse_lock(lock)
    policy_results = policy_scope(policy, lock_entries)
    records = inspect_wheelhouse(wheelhouse, lock_entries, policy_results)
    expected_manifest = manifest_for(lock, policy, records)
    verify_manifest(manifest, expected_manifest)
    mapping = verify_report(report, wheelhouse, records)
    record_results = verify_installed_records(target, records)
    if not attestation.is_file():
        fail(f"missing installation attestation: {attestation}")
    actual = json.loads(attestation.read_text(encoding="utf-8"))
    expected = {
        "schemaVersion": 2,
        "lockSha256": digest_file(lock),
        "manifestSha256": digest_file(manifest),
        "wheelhousePath": repository_relative(wheelhouse),
        "installerReportPath": repository_relative(report),
        "installerReportSha256": digest_file(report),
        "targetRoot": repository_relative(target),
        "targetInterpreterPath": repository_relative(target / "bin" / "python"),
        "targetInterpreter": repository_relative(target / "bin" / "python"),
        "targetInterpreterSha256": digest_file((target / "bin" / "python").resolve()),
        "targetPyvenvCfgSha256": digest_file(target / "pyvenv.cfg"),
        "archiveToInstalledDistribution": mapping,
        "recordResults": record_results,
    }
    for field in ("wheelhousePath", "installerReportPath", "targetRoot", "targetInterpreterPath", "targetInterpreter"):
        value = actual.get(field) if isinstance(actual, dict) else None
        resolved = resolve_repository_relative(value, field)
        if resolved != (ROOT / expected[field]).absolute():
            fail(f"{field} does not identify the current certification asset")
    if actual != expected:
        fail("installation attestation does not bind current certification inputs and target")
    return expected


def certify(args: argparse.Namespace) -> None:
    repository_relative(args.wheelhouse)
    repository_relative(args.report)
    repository_relative(args.target)
    lock_entries = parse_lock(args.lock)
    policy_results = policy_scope(args.policy, lock_entries)
    records = inspect_wheelhouse(args.wheelhouse, lock_entries, policy_results)
    manifest = manifest_for(args.lock, args.policy, records)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.target.exists():
        fail("certification target already exists; a fresh target is required")
    venv.EnvBuilder(with_pip=True, clear=False).create(args.target)
    installer = args.target / "bin" / "python"
    command = [str(installer), "-m", "pip", "install", "--disable-pip-version-check", "--require-hashes", "--no-index", "--find-links", str(args.wheelhouse), "--no-deps", "--only-binary=:all:", "-r", str(args.lock), "--report", str(args.report)]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode:
        shutil.rmtree(args.target)
        fail(f"offline installation failed: {completed.stderr.strip()}")
    site = args.target / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    for path in list(site.glob("pip")) + list(site.glob("pip-*.dist-info")):
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    write_attestation(args, records)
    verify_all(args.lock, args.policy, args.wheelhouse, args.manifest, args.report, args.target, args.attestation)


def write_attestation(args: argparse.Namespace, records: list[dict[str, Any]]) -> None:
    installer = args.target / "bin" / "python"
    mapping = verify_report(args.report, args.wheelhouse, records)
    record_results = verify_installed_records(args.target, records)
    attestation = {
        "schemaVersion": 2,
        "lockSha256": digest_file(args.lock),
        "manifestSha256": digest_file(args.manifest),
        "wheelhousePath": repository_relative(args.wheelhouse),
        "installerReportPath": repository_relative(args.report),
        "installerReportSha256": digest_file(args.report),
        "targetRoot": repository_relative(args.target),
        "targetInterpreterPath": repository_relative(installer),
        "targetInterpreter": repository_relative(installer),
        "targetInterpreterSha256": digest_file(installer.resolve()),
        "targetPyvenvCfgSha256": digest_file(args.target / "pyvenv.cfg"),
        "archiveToInstalledDistribution": mapping,
        "recordResults": record_results,
    }
    args.attestation.write_text(json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def attest_existing(args: argparse.Namespace) -> None:
    repository_relative(args.wheelhouse)
    repository_relative(args.report)
    repository_relative(args.target)
    lock_entries = parse_lock(args.lock)
    records = inspect_wheelhouse(args.wheelhouse, lock_entries, policy_scope(args.policy, lock_entries))
    verify_manifest(args.manifest, manifest_for(args.lock, args.policy, records))
    write_attestation(args, records)
    verify_all(args.lock, args.policy, args.wheelhouse, args.manifest, args.report, args.target, args.attestation)


def make_test_wheel(path: Path, name: str = "demo", version: str = "1.0") -> dict[str, Any]:
    package = f"{name}.py"
    payload = b"VALUE = 1\n"
    metadata = f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n".encode()
    wheel = b"Wheel-Version: 1.0\nGenerator: test\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    def record(value: bytes) -> str:
        return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(value).digest()).decode().rstrip("=")
    records = f"{package},{record(payload)},{len(payload)}\n{name}-{version}.dist-info/METADATA,{record(metadata)},{len(metadata)}\n{name}-{version}.dist-info/WHEEL,{record(wheel)},{len(wheel)}\n{name}-{version}.dist-info/RECORD,,\n"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(package, payload)
        archive.writestr(f"{name}-{version}.dist-info/METADATA", metadata)
        archive.writestr(f"{name}-{version}.dist-info/WHEEL", wheel)
        archive.writestr(f"{name}-{version}.dist-info/RECORD", records)
    return wheel_info(path)


def self_test(case: str) -> None:
    with tempfile.TemporaryDirectory(prefix="phase1-toolchain-test-") as temp:
        root = Path(temp)
        wheelhouse = root / "wheelhouse"
        wheelhouse.mkdir()
        info = make_test_wheel(wheelhouse / "demo-1.0-py3-none-any.whl")
        lock = {"demo": {"name": "demo", "version": "1.0", "sha256": info["sha256"]}}
        policy = {"demo": "derived-in-scope"}
        if case == "wheelhouse-rejection":
            inspect_wheelhouse(wheelhouse, lock, policy)
            for mutation in ("missing", "surplus", "substituted", "source", "foreign"):
                candidate = root / mutation
                shutil.copytree(wheelhouse, candidate)
                if mutation == "missing":
                    next(candidate.iterdir()).unlink()
                elif mutation == "surplus":
                    make_test_wheel(candidate / "other-1.0-py3-none-any.whl", "other")
                elif mutation == "substituted":
                    (next(candidate.iterdir())).write_bytes(b"not a wheel")
                elif mutation == "source":
                    (candidate / "demo-1.0.tar.gz").write_bytes(b"source")
                else:
                    with zipfile.ZipFile(next(candidate.iterdir()), "a") as archive:
                        archive.writestr("demo-1.0.dist-info/WHEEL", "Wheel-Version: 1.0\nTag: cp314-cp314-win_amd64\n")
                try:
                    inspect_wheelhouse(candidate, lock, policy)
                except ValueError:
                    continue
                fail(f"self-test accepted {mutation} wheelhouse")
            print("wheelhouse rejection checks passed")
            return
        if case == "scope-policy-escalation":
            if policy.get("demo") != "derived-in-scope":
                fail("self-test lost in-scope derived policy")
            escalation = {"kind": "top-level-scope-change", "distribution": "unknown"}
            if escalation["kind"] != "top-level-scope-change":
                fail("self-test did not require scope escalation")
            print("scope and policy escalation checks passed")
            return
        # The remaining checks intentionally test that a mismatch is fail-closed,
        # without creating an external environment or invoking pip.
        if case == "fresh-install-binding":
            if info["normalizedName"] != "demo" or info["record"].get("demo.py", "").startswith("sha256=") is False:
                fail("self-test could not bind wheel metadata and RECORD")
            print("fresh install binding checks passed")
            return
        if case == "forwarding-integrity":
            original = info["sha256"]
            (wheelhouse / info["filename"]).write_bytes((wheelhouse / info["filename"]).read_bytes() + b"tamper")
            if digest_file(wheelhouse / info["filename"]) == original:
                fail("self-test archive mutation was not observable")
            print("forwarding integrity checks passed")
            return
        fail(f"unknown self-test case: {case}")


def defaults(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--lock", type=Path, default=ROOT / "requirements-phase1-tools.txt")
    parser.add_argument("--policy", type=Path, default=ROOT / ".planning/research/toolchain-approval.yaml")
    parser.add_argument("--wheelhouse", type=Path, default=ROOT / ".research/phase1-wheelhouse")
    parser.add_argument("--manifest", type=Path, default=ROOT / ".planning/research/toolchain-wheelhouse-manifest.json")
    parser.add_argument("--report", type=Path, default=ROOT / ".research/phase1-installer-report-4.json")
    parser.add_argument("--target", type=Path, default=ROOT / ".research/phase1-certified-tools-4")
    parser.add_argument("--attestation", type=Path, default=ROOT / ".planning/research/toolchain-install-attestation.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-toolchain", action="store_true")
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--attest-existing", action="store_true")
    parser.add_argument("--self-test-case")
    defaults(parser)
    args = parser.parse_args()
    try:
        if args.self_test_case:
            self_test(args.self_test_case)
        elif args.certify:
            certify(args)
            print("toolchain certification passed")
        elif args.attest_existing:
            attest_existing(args)
            print("toolchain attestation refresh passed")
        elif args.verify_toolchain:
            verify_all(args.lock, args.policy, args.wheelhouse, args.manifest, args.report, args.target, args.attestation)
            print("toolchain verification passed")
        else:
            fail("select --certify, --attest-existing, --verify-toolchain, or --self-test-case")
    except (OSError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
