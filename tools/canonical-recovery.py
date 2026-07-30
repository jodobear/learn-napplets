#!/usr/bin/env python3
"""Fail-closed, journaled publication and canonical snapshot primitives.

Canonical consumers register a fixed target set once, acquire all bytes under a shared
lock, and parse only the returned immutable mapping.  Writers take the same lock
exclusively and leave a durable, digest-bound journal until a complete generation is
verified.  Recovery never guesses which generation is usable.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
TRANSACTION_DIRECTORY = ".canonical-transactions"
LOCK_NAME = ".canonical-recovery.lock"

# Logical staged names map to fixed live repository locations.  Callers cannot supply
# target paths, which prevents a valid attestation being redirected at another file.
registeredCanonicalProfiles: dict[str, dict[str, str]] = {
    "terminal": {
        "01-REVERIFICATION.md": ".planning/phases/01-research-and-truth-baseline/01-REVERIFICATION.md",
        "STATE.md": ".planning/STATE.md",
        "ROADMAP.md": ".planning/ROADMAP.md",
    },
    "observed-refresh": {
        "claims.yaml": ".planning/research/claims.yaml",
        "drift-register.yaml": ".planning/research/drift-register.yaml",
        "open-questions.yaml": ".planning/research/open-questions.yaml",
        "package-map.md": ".planning/research/package-map.md",
        "open-work-snapshot.json": ".planning/research/open-work-snapshot.json",
    },
}

# These registrations cover every current route and reserve fixed contracts for the
# later compatibility, SPK-G, and observed-refresh readers.  Routes may only add a
# new named fixed set through register_canonical_reader().
registeredCanonicalReaders: dict[str, tuple[str, ...]] = {
    "research-validation": (
        "research/source-registry.yaml", "research/claims.yaml", "research/compatibility-matrix.yaml",
        "research/drift-register.yaml", "research/open-questions.yaml",
    ),
    "consolidation": (
        "research/compatibility-matrix.yaml", "research/drift-register.yaml", "research/open-questions.yaml",
        "spikes/replay-manifest.yaml",
    ),
    "planning-preflight": ("PROJECT.md", "STATE.md", "ROADMAP.md"),
    "source-acquisition": ("research/source-registry.yaml", "research/claims.yaml", "research/drift-register.yaml", "research/open-questions.yaml"),
    "compatibility-baseline": (
        "research/source-registry.yaml", "research/claims.yaml", "research/compatibility-matrix.yaml",
        "research/drift-register.yaml", "research/open-questions.yaml", "research/package-evidence.yaml",
        "research/package-map.md", "research/upstream-acquisition-queue.yaml",
        "research/reports/upstream-acquisition-20260728.md", "spikes/spk-g-package-conformance/metadata.yaml",
        "spikes/spk-g-package-conformance/report.md",
    ),
    "spk-g-package-evidence": (
        "research/compatibility-matrix.yaml", "research/package-evidence.yaml", "research/source-registry.yaml",
        "research/claims.yaml", "research/drift-register.yaml", "research/open-questions.yaml",
    ),
    "observed-refresh-validation": (
        "research/claims.yaml", "research/drift-register.yaml", "research/open-questions.yaml",
        "research/package-map.md", "research/open-work-snapshot.json",
    ),
}


class RecoveryError(RuntimeError):
    """A journal, lock, target, or attestation cannot prove a full generation."""


class PublishInterrupted(RuntimeError):
    """Deterministic test-only interruption after a replacement position."""


def _sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def generation_sha256(targets: Mapping[str, bytes]) -> str:
    """Hash logical path bytes and target bytes; attestations are intentionally absent."""
    digest = hashlib.sha256()
    for logical in sorted(targets):
        digest.update(logical.encode("utf-8"))
        digest.update(b"\0")
        digest.update(targets[logical])
        digest.update(b"\0")
    return digest.hexdigest()


def _normal_relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\0" in value or "\\" in value:
        raise RecoveryError("canonical path must be a nonempty POSIX relative path")
    candidate = Path(value)
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise RecoveryError("canonical path is unsafe")
    return candidate.as_posix()


def _regular(root: Path, relative: str, *, must_exist: bool = True) -> Path:
    relative = _normal_relative(relative)
    root = root.resolve(strict=True)
    target = root / relative
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise RecoveryError("canonical path traverses a symlink")
    if must_exist:
        try:
            mode = target.stat(follow_symlinks=False).st_mode
        except OSError as exc:
            raise RecoveryError(f"canonical target is unavailable: {relative}") from exc
        if not stat.S_ISREG(mode):
            raise RecoveryError("canonical target must be a regular file")
    elif target.exists() or target.is_symlink():
        raise RecoveryError("transaction path already exists")
    return target


def _fsync_file(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_durable(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
    finally:
        os.close(descriptor)
    _fsync_directory(path.parent)


def _journal_bytes(value: Mapping[str, object]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _store_journal(transaction: Path, journal: Mapping[str, object]) -> None:
    payload = _journal_bytes(journal)
    _write_durable(transaction / "journal.json", payload)
    # The companion digest detects corruption/tampering before any reader receives
    # canonical bytes. It is written after the journal and independently fsynced.
    _write_durable(transaction / "journal.sha256", (_sha(payload) + "\n").encode("ascii"))


def _load_journal(transaction: Path) -> dict[str, object]:
    journal_path, digest_path = transaction / "journal.json", transaction / "journal.sha256"
    try:
        if not journal_path.is_file() or journal_path.is_symlink() or not digest_path.is_file() or digest_path.is_symlink():
            raise RecoveryError("transaction journal is incomplete")
        payload = journal_path.read_bytes()
        declared = digest_path.read_text(encoding="ascii").strip()
        if declared != _sha(payload):
            raise RecoveryError("transaction journal digest mismatch")
        value = json.loads(payload)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RecoveryError("transaction journal is malformed") from exc
    if not isinstance(value, dict):
        raise RecoveryError("transaction journal must be an object")
    required = {"id", "state", "targets"}
    if set(value) != required or not isinstance(value["id"], str) or value["state"] not in {"prepared", "publishing", "committed"}:
        raise RecoveryError("transaction journal has an unknown state")
    if not isinstance(value["targets"], list) or not value["targets"]:
        raise RecoveryError("transaction journal target list is invalid")
    return value


@contextmanager
def _lock(root: Path, mode: int, timeout: float = 2.0):
    root = root.resolve(strict=True)
    handle = open(root / LOCK_NAME, "a+", encoding="utf-8")
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(handle.fileno(), mode | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise RecoveryError("CANONICAL_LOCK_CONFLICT: timed out waiting for canonical transaction lock")
                time.sleep(0.01)
        yield
    finally:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def register_canonical_reader(reader_id: str, target_paths: Iterable[str]) -> None:
    paths = tuple(_normal_relative(item) for item in target_paths)
    if not reader_id or reader_id in registeredCanonicalReaders or not paths or len(set(paths)) != len(paths):
        raise RecoveryError("canonical reader registration must have one unique ID and fixed unique targets")
    registeredCanonicalReaders[reader_id] = paths


def register_canonical_profile(profile: str, targets: Mapping[str, str]) -> None:
    if not profile or profile in registeredCanonicalProfiles or not targets:
        raise RecoveryError("canonical profile already exists or is empty")
    logical = tuple(_normal_relative(name) for name in targets)
    live = tuple(_normal_relative(path) for path in targets.values())
    if len(set(logical)) != len(logical) or len(set(live)) != len(live):
        raise RecoveryError("canonical profile targets must be unique")
    registeredCanonicalProfiles[profile] = dict(zip(logical, live, strict=True))


def _recover_locked(root: Path) -> None:
    transactions = root / TRANSACTION_DIRECTORY
    if not transactions.exists():
        return
    if transactions.is_symlink() or not transactions.is_dir():
        raise RecoveryError("transaction directory is unsafe")
    journals = sorted(path for path in transactions.iterdir() if path.is_dir() and not path.is_symlink())
    if len(journals) > 1:
        raise RecoveryError("multiple unfinished canonical transactions")
    if not journals:
        return
    transaction = journals[0]
    journal = _load_journal(transaction)
    targets = journal["targets"]
    if not isinstance(targets, list):
        raise RecoveryError("transaction targets invalid")
    entries: list[dict[str, str]] = []
    for item in targets:
        if not isinstance(item, dict) or set(item) != {"target", "old", "new", "backup"}:
            raise RecoveryError("transaction target entry is invalid")
        if not all(isinstance(item[field], str) for field in item):
            raise RecoveryError("transaction target entry has invalid values")
        entries.append(item)
    if journal["state"] in {"prepared", "publishing"}:
        for entry in entries:
            target = _regular(root, entry["target"])
            backup = transaction / entry["backup"]
            if not backup.is_file() or backup.is_symlink() or _sha(backup.read_bytes()) != entry["old"]:
                raise RecoveryError("transaction backup is missing or digest-mismatched")
            replacement = transaction / (entry["backup"] + ".restore")
            shutil.copyfile(backup, replacement)
            _fsync_file(replacement)
            os.replace(replacement, target)
            _fsync_file(target)
            _fsync_directory(target.parent)
        if any(_sha(_regular(root, entry["target"]).read_bytes()) != entry["old"] for entry in entries):
            raise RecoveryError("recovery could not verify the complete old generation")
    else:
        if any(_sha(_regular(root, entry["target"]).read_bytes()) != entry["new"] for entry in entries):
            raise RecoveryError("committed transaction does not verify as a complete new generation")
    shutil.rmtree(transaction)
    _fsync_directory(transactions)


def recover_canonical_generation(root: Path = ROOT, *, timeout: float = 2.0) -> None:
    with _lock(root, fcntl.LOCK_EX, timeout):
        _recover_locked(root.resolve(strict=True))


def read_canonical_snapshot(
    reader_id: str,
    target_paths: Iterable[str],
    *,
    root: Path = ROOT / ".planning",
    timeout: float = 2.0,
    after_first_read: Callable[[], None] | None = None,
) -> Mapping[str, bytes]:
    """Return one immutable complete generation; never return target bytes on refusal."""
    declared = registeredCanonicalReaders.get(reader_id)
    requested = tuple(_normal_relative(item) for item in target_paths)
    if declared is None or requested != declared:
        raise RecoveryError("canonical reader is not registered for this exact target set")
    root = root.resolve(strict=True)
    while True:
        retry_recovery = False
        with _lock(root, fcntl.LOCK_SH, timeout):
            transactions = root / TRANSACTION_DIRECTORY
            if transactions.exists() and any(transactions.iterdir()):
                retry_recovery = True
            else:
                snapshot: dict[str, bytes] = {}
                for index, relative in enumerate(requested):
                    snapshot[relative] = _regular(root, relative).read_bytes()
                    if index == 0 and after_first_read is not None:
                        after_first_read()
                return MappingProxyType(snapshot)
        if retry_recovery:
            recover_canonical_generation(root, timeout=timeout)


def publish_generation(
    root: Path,
    staged_targets: Mapping[str, bytes],
    *,
    timeout: float = 2.0,
    interrupt_after: int | None = None,
) -> None:
    """Publish named bytes atomically or retain enough material to recover the old set."""
    root = root.resolve(strict=True)
    ordered = { _normal_relative(name): content for name, content in sorted(staged_targets.items()) }
    if not ordered or not all(isinstance(value, bytes) for value in ordered.values()):
        raise RecoveryError("publication requires a nonempty map of byte targets")
    with _lock(root, fcntl.LOCK_EX, timeout):
        _recover_locked(root)
        transactions = root / TRANSACTION_DIRECTORY
        transactions.mkdir(exist_ok=True)
        _fsync_directory(root)
        transaction = transactions / uuid.uuid4().hex
        transaction.mkdir()
        backups = transaction / "backup"
        staged = transaction / "staged"
        backups.mkdir(); staged.mkdir()
        entries: list[dict[str, str]] = []
        try:
            for index, (target_name, content) in enumerate(ordered.items()):
                target = _regular(root, target_name)
                old = target.read_bytes()
                backup_relative = f"backup/{index:04d}"
                staged_relative = f"staged/{index:04d}"
                _write_durable(transaction / backup_relative, old)
                _write_durable(transaction / staged_relative, content)
                entries.append({"target": target_name, "old": _sha(old), "new": _sha(content), "backup": backup_relative})
            _fsync_directory(backups); _fsync_directory(staged); _fsync_directory(transaction)
            journal: dict[str, object] = {"id": transaction.name, "state": "prepared", "targets": entries}
            _store_journal(transaction, journal)
            journal["state"] = "publishing"
            _store_journal(transaction, journal)
            for index, entry in enumerate(entries):
                source = transaction / f"staged/{index:04d}"
                target = _regular(root, entry["target"])
                os.replace(source, target)
                _fsync_file(target); _fsync_directory(target.parent)
                if interrupt_after == index:
                    raise PublishInterrupted(f"injected interruption after replacement {index}")
            if any(_sha(_regular(root, entry["target"]).read_bytes()) != entry["new"] for entry in entries):
                raise RecoveryError("published generation digest verification failed")
            journal["state"] = "committed"
            _store_journal(transaction, journal)
            shutil.rmtree(transaction)
            _fsync_directory(transactions)
        except PublishInterrupted:
            raise
        except Exception:
            # Keep a valid prepared/publishing journal and backups for recovery. If
            # journal creation itself failed, fail closed rather than deleting evidence.
            raise


def _safe_staged_root(root: Path, staged_root: Path, profile: str, allow_unsafe: bool) -> Path:
    staged = staged_root.resolve(strict=True)
    if staged.is_symlink() or not staged.is_dir():
        raise RecoveryError("staged root must be a regular directory")
    if allow_unsafe:
        return staged
    required_parent = root / ".planning" / (".terminal-staging" if profile == "terminal" else ".observed-refresh-staging")
    try:
        staged.relative_to(required_parent.resolve(strict=True))
    except ValueError as exc:
        raise RecoveryError("staged root is outside the approved profile staging directory") from exc
    return staged


def _attested_targets(attestation: Mapping[str, object], profile: str, content: Mapping[str, bytes]) -> None:
    target_map = attestation.get("targetMap")
    if attestation.get("profile") != profile or not isinstance(target_map, dict):
        raise RecoveryError("attestation profile or target map is invalid")
    expected = {name: _sha(value) for name, value in content.items()}
    if target_map != expected:
        raise RecoveryError("attestation target map does not bind exact staged bytes")
    if attestation.get("generationSha256") != generation_sha256(content):
        raise RecoveryError("attestation generation aggregate does not bind exact staged bytes")


def publish_validated_canonical_set(
    profile: str,
    staged_root: Path,
    attestation: Mapping[str, object] | Path,
    *,
    root: Path = ROOT,
    timeout: float = 2.0,
    allow_unsafe_staging: bool = False,
) -> None:
    profile_targets = registeredCanonicalProfiles.get(profile)
    if profile_targets is None:
        raise RecoveryError("unknown canonical profile")
    root = root.resolve(strict=True)
    staged = _safe_staged_root(root, staged_root, profile, allow_unsafe_staging)
    if isinstance(attestation, Path):
        try:
            if attestation.is_symlink() or not attestation.is_file():
                raise RecoveryError("attestation must be a regular file")
            parsed = json.loads(attestation.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RecoveryError("attestation is malformed") from exc
    else:
        parsed = dict(attestation)
    if not isinstance(parsed, dict):
        raise RecoveryError("attestation must be an object")
    names = tuple(sorted(profile_targets))
    observed_names = tuple(sorted(path.name for path in staged.iterdir() if path.name != (attestation.name if isinstance(attestation, Path) else "")))
    if observed_names != names:
        raise RecoveryError("staged root does not contain the exact fixed profile target set")
    content: dict[str, bytes] = {}
    for logical in names:
        candidate = staged / logical
        if candidate.is_symlink() or not candidate.is_file() or not stat.S_ISREG(candidate.stat(follow_symlinks=False).st_mode):
            raise RecoveryError("staged target must be a regular non-symlink file")
        content[logical] = candidate.read_bytes()
    _attested_targets(parsed, profile, content)
    # Convert fixed logical targets to root-relative live targets only after every
    # staged byte and aggregate are independently rechecked.
    publish_generation(root, {profile_targets[name]: content[name] for name in names}, timeout=timeout)
    if any(_sha(_regular(root, profile_targets[name]).read_bytes()) != _sha(content[name]) for name in names):
        raise RecoveryError("published live generation does not match attestation")


def main() -> int:
    parser = argparse.ArgumentParser(description="Journaled canonical generation recovery and publication")
    subcommands = parser.add_subparsers(dest="command", required=True)
    publish = subcommands.add_parser("publish-validated-canonical-set")
    publish.add_argument("--profile", choices=("terminal", "observed-refresh"), required=True)
    publish.add_argument("--staged-root", type=Path, required=True)
    publish.add_argument("--attestation", type=Path, required=True)
    recover = subcommands.add_parser("recover")
    recover.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        if args.command == "publish-validated-canonical-set":
            publish_validated_canonical_set(args.profile, args.staged_root, args.attestation)
        else:
            recover_canonical_generation(args.root)
    except RecoveryError as exc:
        print(f"CANONICAL_PUBLICATION_REFUSED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
