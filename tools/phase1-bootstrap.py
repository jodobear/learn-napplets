#!/usr/bin/env python3
"""Run the recorded Phase 1 interpreter before any site-enabled tooling."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTUP_HOOK_NAMES = ("sitecustomize.py", "usercustomize.py")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repository_relative_path(value: object) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("bootstrap: isolatedInterpreter must be a nonempty relative path")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("bootstrap: isolatedInterpreter must remain below repository root")
    candidate_path = ROOT / candidate
    # The manifest records a repository-contained symlink whose approved target may
    # live outside the repository.  Constrain the link location, not its target.
    absolute_candidate = candidate_path.absolute()
    if ROOT.resolve() not in (absolute_candidate, *absolute_candidate.parents):
        raise ValueError("bootstrap: isolatedInterpreter escapes repository root")
    return candidate_path.resolve()


def load_environment(path: Path) -> dict[str, object]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"bootstrap: cannot read environment record: {exc}") from exc
    if not isinstance(document, dict) or not isinstance(document.get("python"), dict):
        raise ValueError("bootstrap: environment record lacks python details")
    return document


def assert_recorded_interpreter(environment: dict[str, object]) -> Path:
    python = environment["python"]
    assert isinstance(python, dict)
    expected = repository_relative_path(python.get("isolatedInterpreter"))
    resolved_expected = Path(str(python.get("resolvedExecutable", ""))).resolve()
    if expected != resolved_expected:
        raise ValueError("bootstrap: recorded interpreter does not resolve to resolvedExecutable")
    actual = Path(sys.executable).resolve()
    if actual != resolved_expected:
        raise ValueError("bootstrap: invocation did not use the recorded interpreter")
    if sys.version.split()[0] != python.get("version"):
        raise ValueError("bootstrap: interpreter version differs from environment record")
    if digest(actual) != python.get("executableSha256"):
        raise ValueError("bootstrap: interpreter SHA-256 differs from environment record")
    return actual


def startup_inventory_errors(directory: Path) -> list[str]:
    errors: list[str] = []
    if not directory.is_dir():
        return [f"bootstrap: startup inventory is not a directory: {directory}"]
    for candidate in directory.rglob("*"):
        if not candidate.is_file() or candidate.is_symlink():
            continue
        if candidate.name in STARTUP_HOOK_NAMES or candidate.suffix == ".pth":
            errors.append(f"bootstrap: unsafe startup hook inventory entry: {candidate.name}")
    return errors


def run_self_test(interpreter: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="phase1-bootstrap-") as temporary:
        fixture = Path(temporary)
        payload = fixture / "startup-payload-ran"
        (fixture / "malicious.pth").write_text(
            f"import pathlib; pathlib.Path({str(payload)!r}).write_text('ran')\n", encoding="utf-8"
        )
        for name in STARTUP_HOOK_NAMES:
            (fixture / name).write_text(
                f"import pathlib; pathlib.Path({str(payload)!r}).write_text('ran')\n", encoding="utf-8"
            )
        completed = subprocess.run(
            [str(interpreter), "-I", "-S", "-c", "import sys; assert 'site' not in sys.modules"],
            cwd=fixture,
            text=True,
            capture_output=True,
            check=False,
            env={"PATH": os.environ.get("PATH", ""), "PYTHONPATH": str(fixture)},
        )
        if completed.returncode:
            raise ValueError(f"bootstrap: isolated fixture command failed: {completed.stderr.strip()}")
        if payload.exists():
            raise ValueError("bootstrap: malicious startup fixture executed under -I -S")
        if not startup_inventory_errors(fixture):
            raise ValueError("bootstrap: unsafe startup fixture inventory was accepted")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", type=Path, default=ROOT / ".planning/spikes/_shared/toolchain-environment.json")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--startup-inventory", type=Path)
    args = parser.parse_args()
    try:
        environment = load_environment(args.environment)
        interpreter = assert_recorded_interpreter(environment)
        if args.startup_inventory:
            errors = startup_inventory_errors(args.startup_inventory)
            if errors:
                raise ValueError("\n".join(errors))
        if args.self_test:
            run_self_test(interpreter)
            print("bootstrap self-test passed")
        else:
            print("bootstrap verification passed")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
