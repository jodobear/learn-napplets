#!/usr/bin/env python3
"""Bounded, read-only helper for revision-pinned Phase 1 source collection.

The command never performs network writes. It accepts only Tier 1 hosts and can
resolve a local Git clone's mutable ref to a commit and exact revision:path blob
before calculating an evidence digest. Cache paths are deliberately confined to
ignored .research/upstreams/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = ROOT / ".research" / "upstreams"
ALLOWED_HOSTS = {
    "github.com",
    "api.github.com",
    "raw.githubusercontent.com",
    "www.npmjs.com",
    "npmjs.com",
    "developer.mozilla.org",
    "www.theodinproject.com",
    "theodinproject.com",
    "learnfips.com",
    "www.learnfips.com",
}


def reject_unallowlisted(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.hostname.lower() not in ALLOWED_HOSTS:
        return f"source URL is not allowlisted: {url}"
    return None


def cache_path(value: str) -> Path:
    requested = Path(value).expanduser().resolve()
    try:
        requested.relative_to(CACHE_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"cache root must remain under {CACHE_ROOT}") from exc
    return requested


def git_output(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args], text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "git resolution failed")
    return result.stdout.strip()


def resolve_blob(repository: Path, ref: str, path: str) -> dict[str, str]:
    """Resolve ref -> commit -> exact blob and digest its immutable bytes."""
    commit = git_output(repository, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")
    blob = git_output(repository, "rev-parse", "--verify", "--end-of-options", f"{commit}:{path}^{{blob}}")
    result = subprocess.run(
        ["git", "-C", str(repository), "cat-file", "blob", blob], capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "cannot read resolved blob")
    return {
        "commitSha": commit,
        "blobSha": blob,
        "path": path,
        "contentSha256": hashlib.sha256(result.stdout).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and pin bounded Tier 1 source inputs without network writes.")
    parser.add_argument("--validate-url", help="validate one candidate URL against the Tier 1 HTTPS allowlist")
    parser.add_argument("--cache-root", default=str(CACHE_ROOT), help="ignored cache path; must remain under .research/upstreams/")
    parser.add_argument("--repository-dir", type=Path, help="existing local clone to inspect; this command does not clone")
    parser.add_argument("--ref", help="mutable discovery ref to resolve")
    parser.add_argument("--path", help="repository-relative source path to resolve")
    args = parser.parse_args()

    if args.validate_url:
        error = reject_unallowlisted(args.validate_url)
        if error:
            print(error, file=sys.stderr)
            return 2
        print("allowlisted")
        return 0

    try:
        cache_path(args.cache_root)
        if not (args.repository_dir and args.ref and args.path):
            parser.error("supply --validate-url or --repository-dir, --ref, and --path")
        repository = args.repository_dir.resolve()
        if not (repository / ".git").exists():
            raise ValueError("repository-dir must be an existing local Git clone")
        print(json.dumps(resolve_blob(repository, args.ref, args.path), sort_keys=True))
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
