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
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse
from urllib.request import Request, urlopen

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


COMPATIBILITY_DIMENSIONS = (
    "normative-protocol",
    "observed-implementation",
    "published-package",
    "runtime",
    "example-fixture",
    "current-work",
    "conformance",
)
REVIEWED_REFRESH_REPORTS = (
    ".planning/research/reports/upstream-refresh-kehto-web-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-napplet-web-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-napplet-naps-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-synthesis-2026-07-28.md",
)
_COMMIT_RE = re.compile(r"^[0-9a-f]{40,64}$")
_CANDIDATE_ROW_RE = re.compile(r"^\|\s*`?(CAND-[A-Z0-9][A-Z0-9-]*)`?\s*\|", re.MULTILINE)


class HttpsTransport:
    """Read-only HTTPS transport for an already-approved bounded collection run.

    Instantiation makes no request. Every URL is allowlisted before it is opened,
    and callers still supply an immutable commit rather than a branch name.
    """

    def __init__(self, repository: str, *, timeout_seconds: int = 20) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("repository must be an owner/name GitHub identity")
        self.repository = repository
        self.timeout_seconds = timeout_seconds

    def _read(self, url: str) -> bytes:
        if reject_unallowlisted(url):
            raise ValueError(f"source URL is not allowlisted: {url}")
        request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "learn-napplets-phase1"})
        with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 - exact HTTPS allowlist above
            return response.read()

    def _json(self, url: str) -> Mapping[str, Any]:
        try:
            payload = json.loads(self._read(url).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("official HTTPS response is not valid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("official HTTPS response must be a JSON object")
        return payload

    def identity(self, url: str) -> Mapping[str, Any]:
        return self._json(url)

    def commit(self, sha: str) -> Mapping[str, Any]:
        return self._json(f"https://api.github.com/repos/{self.repository}/git/commits/{sha}")

    def blob(self, commit_sha: str, path: str) -> bytes:
        safe_path = _safe_repo_path(path).as_posix()
        return self._read(f"https://raw.githubusercontent.com/{self.repository}/{commit_sha}/{safe_path}")


class FixtureTransport:
    """In-process-only transport used by deterministic collector tracer tests."""

    def __init__(
        self,
        *,
        identities: Mapping[str, Mapping[str, Any]],
        commits: Mapping[str, Mapping[str, Any]],
        blobs: Mapping[tuple[str, str], bytes],
        packages: Mapping[str, Mapping[str, Any]],
    ) -> None:
        self.identities = identities
        self.commits = commits
        self.blobs = blobs
        self.packages = packages

    def identity(self, url: str) -> Mapping[str, Any]:
        try:
            return self.identities[url]
        except KeyError as exc:
            raise ValueError("repository identity response is missing") from exc

    def commit(self, sha: str) -> Mapping[str, Any]:
        try:
            return self.commits[sha]
        except KeyError as exc:
            raise ValueError("immutable commit is missing") from exc

    def blob(self, commit_sha: str, path: str) -> bytes:
        try:
            return self.blobs[(commit_sha, path)]
        except KeyError as exc:
            raise ValueError("immutable commit:path blob is missing") from exc


def _confined_cache_root(value: Path) -> Path:
    resolved = value.expanduser().resolve()
    if resolved.name != "upstreams" or resolved.parent.name != ".research":
        raise ValueError("cache root must be an ignored .research/upstreams directory")
    return resolved


def _safe_repo_path(path: str) -> Path:
    candidate = Path(path)
    if not path or candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("repository path must not escape the immutable commit tree")
    return candidate


def _validate_identity(identity: Mapping[str, Any], identity_url: str, repository: str) -> None:
    if reject_unallowlisted(identity_url):
        raise ValueError(f"repository identity URL is not allowlisted: {identity_url}")
    expected_url = f"https://github.com/{repository}"
    if identity.get("html_url") != expected_url:
        raise ValueError("repository identity response does not match the requested official repository")
    if not isinstance(identity.get("id"), int) or identity["id"] <= 0:
        raise ValueError("repository identity response lacks a stable repository ID")
    if identity.get("private") is not False or identity.get("archived") is not False:
        raise ValueError("repository identity response is not a public active repository")
    if not isinstance(identity.get("default_branch"), str) or not identity["default_branch"]:
        raise ValueError("repository identity response lacks a default branch")


def build_observed_source_record(record: Mapping[str, Any], *, raw_origin: str = "observed-implementation") -> dict[str, Any]:
    """Return a source record that cannot elevate observed code into normative authority."""
    if raw_origin != "observed-implementation":
        raise ValueError("observed implementation cannot be classified as normative authority")
    result = dict(record)
    result["rawOrigin"] = "observed-implementation"
    result["evidenceClass"] = "implementation"
    result["authorityTier"] = "official-repository-observation"
    result["maturity"] = "implementation-specific"
    result["review"] = {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]}
    return result


def collect_immutable_candidate(
    transport: FixtureTransport,
    identity_url: str,
    repository: str,
    commit_sha: str,
    path: str,
    cache_root: Path,
    retrieved_at: str,
    source_id: str,
    impacts: list[str],
) -> dict[str, Any]:
    """Collect one allowlisted immutable candidate through a transport boundary.

    The caller provides the exact commit and path; a branch name or a response that
    merely identifies a default branch cannot become a collection target.
    """
    if not _COMMIT_RE.fullmatch(commit_sha):
        raise ValueError("collector requires an immutable commit SHA, not a mutable-only identity")
    if reject_unallowlisted(identity_url):
        raise ValueError(f"repository identity URL is not allowlisted: {identity_url}")
    repo_path = _safe_repo_path(path)
    root = _confined_cache_root(cache_root)
    identity = transport.identity(identity_url)
    _validate_identity(identity, identity_url, repository)
    commit = transport.commit(commit_sha)
    if commit.get("sha") != commit_sha or not commit.get("tree"):
        raise ValueError("immutable commit response does not bind the requested SHA and tree")
    content = transport.blob(commit_sha, path)
    if not isinstance(content, bytes):
        raise ValueError("immutable commit:path blob is not exact bytes")
    target = (root / repository / commit_sha / repo_path).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("repository cache path escapes .research/upstreams") from exc
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()
    record = {
        "id": source_id,
        "kind": "source",
        "collectionStatus": "collected",
        "repository": repository,
        "officialUrl": f"https://github.com/{repository}",
        "immutableUrl": f"https://github.com/{repository}/blob/{commit_sha}/{path}",
        "ref": commit_sha,
        "commitSha": commit_sha,
        "path": path,
        "locator": f"commit:{commit_sha} path:{path}",
        "contentSha256": digest,
        "retrievedAt": retrieved_at,
        "uncertainty": {"state": "material", "reason": "Observed repository implementation is not normative protocol authority."},
        "impacts": {"requirements": impacts, "phases": ["01"]},
        "freshness": {"state": "provisional", "refreshTrigger": "Repository identity, commit, path, or digest changes."},
    }
    return build_observed_source_record(record)


def classify_compatibility(qualified_dimensions: Mapping[str, list[str]], affected_requirements: list[str]) -> dict[str, Any]:
    """Return reviewable compatibility status without treating observations as approval."""
    missing = [dimension for dimension in COMPATIBILITY_DIMENSIONS if not qualified_dimensions.get(dimension)]
    return {
        "status": "blocked" if missing else "review-required",
        "dimensions": list(COMPATIBILITY_DIMENSIONS),
        "missingDimensions": missing,
        "affectedRequirements": list(affected_requirements),
        "authority": "no automatic approval",
    }


def _load_planning_validator() -> Any:
    location = ROOT / "tools" / "validate-planning.py"
    spec = importlib.util.spec_from_file_location("phase1_validate_planning", location)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load Plan 01-29 source-input validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_reviewed_refresh_binding(binding: Mapping[str, Any]) -> None:
    report_digests = binding.get("reportDigests")
    source_digests = binding.get("sourceReportDigests")
    reviewed_commit = binding.get("reviewedCommit")
    if not isinstance(reviewed_commit, str) or not _COMMIT_RE.fullmatch(reviewed_commit):
        raise ValueError("reviewed commit must be an immutable SHA")
    if binding.get("sourceSnapshotCommit") != reviewed_commit:
        raise ValueError("reviewed commit differs from the Plan 01-29 source snapshot")
    if not isinstance(report_digests, Mapping) or not isinstance(source_digests, Mapping):
        raise ValueError("reviewed report digest binding is missing")
    if set(report_digests) != set(REVIEWED_REFRESH_REPORTS) or set(source_digests) != set(REVIEWED_REFRESH_REPORTS):
        raise ValueError("reviewed report binding must contain exactly four refresh reports")
    for report in REVIEWED_REFRESH_REPORTS:
        digest = report_digests[report]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or digest != source_digests[report]:
            raise ValueError("reviewed report digest does not match the immutable source snapshot")
    candidates = binding.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("reviewed report binding contains no candidate rows")
    ids = [candidate.get("id") for candidate in candidates if isinstance(candidate, Mapping)]
    if len(ids) != len(candidates) or len(set(ids)) != len(ids):
        raise ValueError("reviewed report candidate rows are unrecognized or duplicate")


def load_reviewed_refresh_candidates(root: Path, review_path: Path, executor_identity: str) -> dict[str, Any]:
    """Load candidate rows solely from Plan 01-29-reviewed Git blobs.

    Working-tree report text is never read. The Plan 01-29 loader first requires
    exact review binding, tracked regular files, current-HEAD equality, and digest
    equality, then returns immutable bytes from the reviewed commit.
    """
    validator = _load_planning_validator()
    snapshot = validator.load_reviewed_phase1_source_snapshot(
        review_path, root=root, executor_identity=executor_identity
    )
    reviewed_commit, _, _, sources, _ = validator._parse_review_manifest(review_path.read_text(encoding="utf-8"))
    report_digests = {report: sources[report][2] for report in REVIEWED_REFRESH_REPORTS}
    candidates: list[dict[str, str]] = []
    for report in REVIEWED_REFRESH_REPORTS:
        content = snapshot.get(report)
        if content is None or hashlib.sha256(content).hexdigest() != report_digests[report]:
            raise ValueError("reviewed report digest changed before candidate parsing")
        found = _CANDIDATE_ROW_RE.findall(content.decode("utf-8"))
        # Detail reports can be evidence-only (including a bounded zero-result
        # window); the synthesis owns the aggregate candidate table. Every blob
        # remains digest-bound before this parser permits that distinction.
        candidates.extend({"id": candidate_id, "reportPath": report} for candidate_id in found)
    if not candidates:
        raise ValueError("reviewed report set contains no recognized candidate rows")
    binding: dict[str, Any] = {
        "reviewedCommit": reviewed_commit,
        "sourceSnapshotCommit": reviewed_commit,
        "reportDigests": report_digests,
        "sourceReportDigests": dict(report_digests),
        "candidates": candidates,
    }
    binding["parsedRecordSha256"] = hashlib.sha256(
        json.dumps({"reportDigests": report_digests, "candidates": candidates}, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    validate_reviewed_refresh_binding(binding)
    return binding


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
