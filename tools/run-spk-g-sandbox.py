#!/usr/bin/env python3
"""Fail-closed OS sandbox contract for a future qualified SPK-G operation.

This module never selects, installs, imports, or executes a package by itself.  A caller
may construct an OS-sandboxed command only after a recovered eligibility receipt says
that a specifically approved public artifact is qualified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class SandboxContract:
    status: str
    reasons: tuple[str, ...]
    network_disabled: bool = False
    repository_read_only: bool = False
    isolated_workspace: bool = False
    minimal_environment: bool = False
    resource_limits: bool = False
    mechanism: str = "none"

    @classmethod
    def unavailable(cls, *reasons: str) -> "SandboxContract":
        return cls(status="unavailable", reasons=tuple(reasons) or ("SANDBOX_UNAVAILABLE",))

    @classmethod
    def verified(cls, mechanism: str) -> "SandboxContract":
        return cls(
            status="verified",
            reasons=(),
            network_disabled=True,
            repository_read_only=True,
            isolated_workspace=True,
            minimal_environment=True,
            resource_limits=True,
            mechanism=mechanism,
        )

    def digest(self) -> str:
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def probe_sandbox() -> SandboxContract:
    """Report an auditable capability decision without starting a sandbox.

    Capability discovery is intentionally conservative: an executable alone is not
    proof that its user namespace, no-network, readonly bind, or rlimit policy is
    enforceable in this process.  A future approved runner must provide an attested
    mechanism-specific probe before this returns ``verified``.
    """
    if shutil.which("bwrap") is None:
        return SandboxContract.unavailable("NO_ROOTLESS_SANDBOX_MECHANISM")
    # Environment variables are not evidence that OS isolation is actually enforced.
    # A verified result must come from a future qualified operation's attested runtime
    # probe, not from an operator-supplied toggle in this unqualified baseline.
    return SandboxContract.unavailable("SANDBOX_PROBE_REQUIRES_QUALIFIED_OPERATION")


def construct_sandbox_argv(contract: SandboxContract, repository: Path, workspace: Path, package_argv: Sequence[str]) -> list[str]:
    """Build the fixed bwrap boundary only from an already approved package argv."""
    if contract.status != "verified" or not all((contract.network_disabled, contract.repository_read_only, contract.isolated_workspace, contract.minimal_environment, contract.resource_limits)):
        raise ValueError("SPK-G sandbox contract is not verified")
    if contract.mechanism != "bubblewrap-rootless-v1" or shutil.which("bwrap") is None:
        raise ValueError("SPK-G sandbox mechanism is unavailable")
    repository = repository.resolve(strict=True)
    workspace = workspace.resolve(strict=True)
    if repository == workspace or repository in workspace.parents:
        raise ValueError("SPK-G workspace must be isolated from the readonly repository")
    # No caller-controlled flags precede this boundary.  The fixed policy unshares the
    # network, exposes the repository readonly, uses an empty HOME, and bounds the
    # process via bwrap's pid namespace; the caller applies wall/CPU/memory/file limits
    # before exec in its dedicated approved runtime wrapper.
    return [
        "bwrap", "--unshare-user", "--unshare-pid", "--unshare-net", "--die-with-parent",
        "--ro-bind", str(repository), "/repository", "--bind", str(workspace), "/workspace",
        "--tmpfs", "/tmp", "--dir", "/home/sandbox", "--setenv", "HOME", "/home/sandbox",
        "--setenv", "PATH", "/usr/bin:/bin", "--chdir", "/workspace", "--",
        *package_argv,
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect the SPK-G no-network sandbox contract")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("only --check is supported; this tool never executes a package directly")
    contract = probe_sandbox()
    print(json.dumps({**asdict(contract), "digest": contract.digest()}, sort_keys=True))
    return 0 if contract.status == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
