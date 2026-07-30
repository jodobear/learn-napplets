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
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

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


class _NoRedirect(HTTPRedirectHandler):
    """Refuse redirect expansion outside the reviewed public-read boundary."""

    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Request:
        raise ValueError(f"redirect refused for bounded collection: {newurl}")


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
        self._opener = build_opener(_NoRedirect())

    def _read(self, url: str) -> bytes:
        if reject_unallowlisted(url):
            raise ValueError(f"source URL is not allowlisted: {url}")
        request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "learn-napplets-phase1"})
        with self._opener.open(request, timeout=self.timeout_seconds) as response:  # nosec B310 - exact HTTPS allowlist above
            if response.geturl() != url:
                raise ValueError("redirect refused for bounded collection")
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

    def tree(self, tree_sha: str) -> Mapping[str, Any]:
        return self._json(f"https://api.github.com/repos/{self.repository}/git/trees/{tree_sha}?recursive=1")

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


REVIEWED_COLLECTION_TARGETS: tuple[dict[str, Any], ...] = (
    {
        "id": "CAND-SRC-NAPPLET-WEB-PR184-20260728", "repository": "napplet/web", "repositoryId": 1197078677,
        "defaultBranch": "main", "commitSha": "4916777862ababd09fa13cf155f4b4079c8e8cb1",
        "treeSha": "11d4c67a47fd399f801bf0339885dc3dda9780aa", "path": "packages/cli/src/manifest.ts",
        "blobSha": "c9c0ceff963da1e2c5c71f97ddc69afff08d3c57", "evidenceClass": "observed-implementation",
        "affectedClaims": ["DRF-IDENTITY-001"], "affectedDrift": ["DRF-IDENTITY-001"],
        "affectedQuestions": ["OQ-UPSTREAM-BASELINE-001"], "refreshTrigger": "NIP-5A/NIP-5D, web release, or default-branch change.",
    },
    {
        "id": "CAND-SRC-NAPPLET-WEB-PR186-20260728", "repository": "napplet/web", "repositoryId": 1197078677,
        "defaultBranch": "main", "commitSha": "dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b",
        "treeSha": "33edc8387973f31687dfb20181a40fe936286824", "path": "packages/nap/src/convention-uri.ts",
        "blobSha": "1a8db0c46d517edf2374b5e5022b429d8b18191b", "evidenceClass": "observed-implementation",
        "affectedClaims": ["DRF-INTENT-001", "DRF-MANIFEST-001", "DRF-METADATA-001", "DRF-IDENTITY-001"],
        "affectedDrift": ["DRF-INTENT-001", "DRF-MANIFEST-001", "DRF-METADATA-001", "DRF-IDENTITY-001"],
        "affectedQuestions": ["OQ-UPSTREAM-BASELINE-001", "OQ-VERIFIED-LOADER-IDENTITY-001", "OQ-VERIFIED-LOADER-MANIFEST-001"],
        "refreshTrigger": "Linked NAP status/revision, web release/default-branch change, or Phase 2 contract review.",
    },
    {
        "id": "CAND-SRC-NAPPLET-WEB-PR188-20260728", "repository": "napplet/web", "repositoryId": 1197078677,
        "defaultBranch": "main", "commitSha": "60889f1c2476e063500c7ab6624af6abe0dbcbe5",
        "treeSha": "d1bd6d78bb357506e6f4244537fecd54262f9a55", "path": "packages/nap/package.json",
        "blobSha": "d125a4a5ae6d1a8b7409b94be0cb51a6899c2a62", "evidenceClass": "release-metadata",
        "affectedClaims": ["CLM-CMP-PACKAGE-001"], "affectedDrift": ["DRF-ARTIFACT-001"],
        "affectedQuestions": ["OQ-PUBLIC-PACKAGE-BASELINE-001"], "refreshTrigger": "Registry/release/integrity/export change or package admission review.",
    },
    {
        "id": "CAND-SRC-KEHTO-WEB-PR204-20260728", "repository": "kehto/web", "repositoryId": 1204025151,
        "defaultBranch": "main", "commitSha": "b85db51db838866de753b275b9d34ec908785bd2",
        "treeSha": "6ba4a4f6cdd52c2231d80f1ff913f7727720c8a3", "path": "RUNTIME-SPEC.md",
        "blobSha": "d90cab7dcad177c6eacb6f0780b434b5ecffccab", "evidenceClass": "observed-implementation",
        "affectedClaims": ["DRF-HANDSHAKE-001", "DRF-EGRESS-001", "DRF-CONFORMANCE-001"],
        "affectedDrift": ["DRF-HANDSHAKE-001", "DRF-EGRESS-001", "DRF-CONFORMANCE-001"],
        "affectedQuestions": ["OQ-VERIFIED-LOADER-IDENTITY-001", "OQ-VERIFIED-LOADER-MANIFEST-001", "OQ-VERIFIED-LOADER-VERIFIER-001"],
        "refreshTrigger": "Listed runtime source-path or default-branch change.",
    },
    {
        "id": "CAND-SRC-KEHTO-WEB-PR209-20260728", "repository": "kehto/web", "repositoryId": 1204025151,
        "defaultBranch": "main", "commitSha": "4eafa058d18cf245b23d49b23bc29dda0b7d7651",
        "treeSha": "24563d1aa55989c09f6134a15b4492c4c66fc8c6", "path": "packages/runtime/package.json",
        "blobSha": "fc6447a2cd05edccd4bd324b29340abcfee2e935", "evidenceClass": "release-metadata",
        "affectedClaims": ["CLM-CMP-PACKAGE-001"], "affectedDrift": ["DRF-ARTIFACT-001"],
        "affectedQuestions": ["OQ-PUBLIC-PACKAGE-BASELINE-001"], "refreshTrigger": "Registry integrity/current runtime manifest change.",
    },
    {
        "id": "CAND-SRC-KEHTO-WEB-PR211-20260728", "repository": "kehto/web", "repositoryId": 1204025151,
        "defaultBranch": "main", "commitSha": "54ef2ead03ee0c37727468b8658b6dc224137",
        "treeSha": "4e88d775afb6e27ffeef1e143a2477bbe7dd28b6", "path": "scripts/audit-gateway-artifacts.mjs",
        "blobSha": "afc424858b74b8917a0529e8065bc6afaaa2e3cc", "evidenceClass": "observed-implementation",
        "affectedClaims": ["DRF-ARTIFACT-001"], "affectedDrift": ["DRF-ARTIFACT-001"],
        "affectedQuestions": ["OQ-VERIFIED-LOADER-VERIFIER-001"], "refreshTrigger": "Loader/audit path or default-branch change.",
    },
    {
        "id": "CAND-SRC-NAPS-WINDOW-20260728", "repository": "napplet/naps", "repositoryId": 1202279733,
        "defaultBranch": "master", "checkpointCommit": "5ac0490461ca6fec2f0d2e45b4835cf9bc08de24",
        "evidenceClass": "repository-history-observation", "affectedClaims": ["CLM-UPSTREAM-BASELINE-001"],
        "affectedDrift": ["DRF-DISCOVERY-001"], "affectedQuestions": ["OQ-UPSTREAM-BASELINE-001"],
        "refreshTrigger": "Next bounded rolling-window review; this is not an authority or content source.",
    },
)
REVIEWED_COLLECTION_PARSER_VERSION = "reviewed-refresh-v1"


def _checked_output_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError("collection output path must remain inside the repository") from exc
    return resolved


def _write_json(path: Path, document: Mapping[str, Any]) -> None:
    checked = _checked_output_path(path)
    checked.parent.mkdir(parents=True, exist_ok=True)
    checked.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _require_exact_target_set(binding: Mapping[str, Any]) -> None:
    parsed_ids = {candidate["id"] for candidate in binding["candidates"]}
    expected_ids = {target["id"] for target in REVIEWED_COLLECTION_TARGETS}
    if parsed_ids != expected_ids:
        raise ValueError("reviewed refresh parser did not emit the complete bounded observation set")


def _validate_expected_identity(identity: Mapping[str, Any], target: Mapping[str, Any]) -> None:
    if identity.get("id") != target["repositoryId"] or identity.get("default_branch") != target["defaultBranch"]:
        raise ValueError("official repository identity/default branch differs from the reviewed bounded target")


def _validate_tree_target(transport: HttpsTransport, target: Mapping[str, Any]) -> None:
    commit = transport.commit(str(target["commitSha"]))
    tree = commit.get("tree")
    if not isinstance(tree, Mapping) or tree.get("sha") != target["treeSha"]:
        raise ValueError("immutable commit tree differs from the reviewed bounded target")
    tree_document = transport.tree(str(target["treeSha"]))
    if tree_document.get("truncated") is True or not isinstance(tree_document.get("tree"), list):
        raise ValueError("immutable tree response is truncated or malformed")
    for entry in tree_document["tree"]:
        if isinstance(entry, Mapping) and entry.get("path") == target["path"]:
            if entry.get("type") != "blob" or entry.get("sha") != target["blobSha"]:
                raise ValueError("immutable tree blob differs from the reviewed bounded target")
            return
    raise ValueError("reviewed immutable commit:path is missing from the immutable tree")


def _append_history(path: Path, outcomes: list[Mapping[str, Any]], retrieved_at: str) -> None:
    checked = _checked_output_path(path)
    existing = checked.read_text(encoding="utf-8") if checked.exists() else "schemaVersion: 1\nretrievals:\nfailures:\n"
    if "ACQ-FAIL-001" not in existing:
        raise ValueError("acquisition history is missing required ACQ-FAIL-001")
    lines = [existing.rstrip(), "", "# Additive Plan 01-45 bounded collection history.", "outcomes:"]
    for outcome in outcomes:
        result = str(outcome["result"])
        lines.extend((
            f"  - id: ACQ-01-45-{outcome['candidateId']}",
            f"    date: {retrieved_at[:10]}",
            "    action: bounded-public-https-read",
            f"    sourceIds: [{outcome['candidateId']}]",
            f"    result: {result}",
            f"    scope: {outcome['repository']} reviewed immutable observation only; non-normative pending human authority review.",
            f"    retry: {outcome['refreshTrigger']}",
        ))
        if result == "failed":
            lines.append(f"    reason: {json.dumps(outcome['reason'])}")
    checked.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _append_observed_candidates(path: Path, outcomes: list[Mapping[str, Any]]) -> None:
    checked = _checked_output_path(path)
    existing = checked.read_text(encoding="utf-8")
    if "blockedDisposition:" not in existing or "observedCandidates:" in existing:
        raise ValueError("candidate manifest cannot safely receive additive observed candidates")
    lines = ["observedCandidates:"]
    for outcome in outcomes:
        lines.extend((
            f"  - id: {outcome['candidateId']}",
            f"    repository: {outcome['repository']}",
            f"    collectionResult: {outcome['result']}",
            f"    evidenceClass: {outcome['evidenceClass']}",
            "    authority: observed-only-not-normative",
            f"    immutableLocator: {json.dumps(outcome.get('immutableLocator', 'repository identity/default-branch checkpoint only'))}",
            f"    refreshTrigger: {json.dumps(outcome['refreshTrigger'])}",
        ))
    checked.write_text(existing.replace("blockedDisposition:", "\n".join(lines) + "\nblockedDisposition:", 1), encoding="utf-8")


def validate_reviewed_acquisition_documents(queue: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    queue_binding = queue.get("reviewedSourceInputBinding")
    receipt_binding = receipt.get("reviewedSourceInputBinding")
    if not isinstance(queue_binding, Mapping) or not isinstance(receipt_binding, Mapping):
        raise ValueError("queue and receipt require reviewed-source input bindings")
    if queue_binding.get("parserVersion") != REVIEWED_COLLECTION_PARSER_VERSION or receipt_binding.get("parserVersion") != REVIEWED_COLLECTION_PARSER_VERSION:
        raise ValueError("queue and receipt reviewed-source binding has an unexpected parser version")
    validate_reviewed_refresh_binding(queue_binding)
    validate_reviewed_refresh_binding(receipt_binding)
    if queue_binding != receipt_binding:
        raise ValueError("queue and receipt reviewed-source bindings differ")


def _revalidate_reviewed_binding(queue: Mapping[str, Any], receipt: Mapping[str, Any], review_path: Path) -> None:
    executor_identity = os.environ.get("GSD_EXECUTOR_ID")
    if not executor_identity:
        raise ValueError("GSD_EXECUTOR_ID is required to revalidate reviewed acquisition")
    expected = load_reviewed_refresh_candidates(ROOT, review_path, executor_identity)
    expected["parserVersion"] = REVIEWED_COLLECTION_PARSER_VERSION
    validate_reviewed_acquisition_documents(queue, receipt)
    if queue["reviewedSourceInputBinding"] != expected:
        raise ValueError("reviewed acquisition binding differs from the current Plan 01-29 Git-blob snapshot")


def collect_reviewed_public_window(queue_path: Path, receipt_path: Path, cache_root: Path, review_path: Path) -> int:
    executor_identity = os.environ.get("GSD_EXECUTOR_ID")
    if not executor_identity:
        raise ValueError("GSD_EXECUTOR_ID is required for bounded collection")
    preflight = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate-planning.py"), "--verify-phase1-source-inputs", "--review", str(review_path)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if preflight.returncode:
        raise ValueError(preflight.stderr.strip() or preflight.stdout.strip() or "reviewed source-input verification failed")
    binding = load_reviewed_refresh_candidates(ROOT, review_path, executor_identity)
    binding["parserVersion"] = REVIEWED_COLLECTION_PARSER_VERSION
    _require_exact_target_set(binding)
    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    outcomes: list[dict[str, Any]] = []
    for target in REVIEWED_COLLECTION_TARGETS:
        if "commitSha" in target and not _COMMIT_RE.fullmatch(str(target["commitSha"])):
            outcomes.append({**target, "candidateId": target["id"], "result": "failed", "retrievedAt": retrieved_at,
                "reason": "Approved immutable locator does not match a valid reviewed commit SHA; no substitute or public request was attempted.",
                "authority": "observed-only-not-normative",
                "uncertainty": "Bounded candidate failed before collection; no scope expansion was attempted."})
            continue
        transport = HttpsTransport(str(target["repository"]))
        identity_url = f"https://api.github.com/repos/{target['repository']}"
        try:
            identity = transport.identity(identity_url)
            _validate_identity(identity, identity_url, str(target["repository"]))
            _validate_expected_identity(identity, target)
            if target["id"] == "CAND-SRC-NAPS-WINDOW-20260728":
                outcomes.append({**target, "candidateId": target["id"], "result": "observed-zero-result", "retrievedAt": retrieved_at,
                    "repositoryIdentity": {"id": identity["id"], "defaultBranch": identity["default_branch"]},
                    "uncertainty": "Bounded zero-result/default-branch observation only; no content was read.", "authority": "observed-only-not-normative"})
                continue
            _validate_tree_target(transport, target)
            record = collect_immutable_candidate(transport, identity_url, str(target["repository"]), str(target["commitSha"]),
                str(target["path"]), cache_root, retrieved_at, f"SRC-{target['id'][9:]}", ["EVID-03"])
            outcomes.append({**target, "candidateId": target["id"], "result": "collected", "retrievedAt": retrieved_at,
                "repositoryIdentity": {"id": identity["id"], "defaultBranch": identity["default_branch"]},
                "immutableLocator": record["immutableUrl"], "contentSha256": record["contentSha256"], "sourceRecord": record,
                "uncertainty": "Observed implementation or release metadata only; no normative authority, package admission, or compatibility approval follows.",
                "authority": "observed-only-not-normative"})
        except Exception as exc:
            outcomes.append({**target, "candidateId": target["id"], "result": "failed", "retrievedAt": retrieved_at,
                "reason": str(exc), "authority": "observed-only-not-normative",
                "uncertainty": "Bounded candidate failed; no replacement or scope expansion was attempted."})
    queue = {"schemaVersion": 1, "kind": "bounded-reviewed-public-acquisition-queue", "reviewedSourceInputBinding": binding,
        "entries": [{key: value for key, value in target.items() if key != "checkpointCommit"} for target in REVIEWED_COLLECTION_TARGETS],
        "nonNormative": True, "humanAuthorityRequiredBy": ["01-30", "01-31"]}
    receipt = {"schemaVersion": 1, "kind": "bounded-reviewed-public-acquisition-receipt", "retrievedAt": retrieved_at,
        "reviewedSourceInputBinding": binding, "outcomes": outcomes,
        "conclusion": "All collected implementation and release bytes are observed, non-normative evidence pending human authority review; no canonical source record was created."}
    _write_json(queue_path, queue)
    _write_json(receipt_path, receipt)
    _append_history(ROOT / ".planning/research/acquisition-log.yaml", outcomes, retrieved_at)
    _append_observed_candidates(ROOT / ".planning/research/candidate-source-manifest.yaml", outcomes)
    # A retained, impact-scoped failed outcome is an expected bounded result. The
    # receipt remains consumable only through the validator and never substitutes a candidate.
    return 0


AUTHORITY_ROLES = (
    "product",
    "protocolTechnical",
    "security",
    "accessibility",
    "contentLearning",
    "release",
)


def _yaml_mapping(path: Path, label: str) -> Mapping[str, Any]:
    """Parse one reviewed YAML document without accepting executable YAML features."""
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - the certified wrapper supplies PyYAML
        raise ValueError("safe YAML support is unavailable in the approved Phase 1 toolchain") from exc
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"{label} is not valid YAML") from exc
    if not isinstance(document, Mapping):
        raise ValueError(f"{label} must be a YAML mapping")
    return document


def _required_string(value: Any, diagnostic: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(diagnostic)
    return value


def _rfc3339(value: Any, diagnostic: str) -> datetime:
    text = _required_string(value, diagnostic)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(diagnostic) from exc
    if parsed.tzinfo is None:
        raise ValueError(diagnostic)
    return parsed.astimezone(timezone.utc)


def _sha256(value: Any, diagnostic: str) -> str:
    text = _required_string(value, diagnostic)
    if not re.fullmatch(r"[0-9a-f]{64}", text):
        raise ValueError(diagnostic)
    return text


def _string_list(value: Any, diagnostic: str) -> list[str]:
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(diagnostic)
    return list(value)


def validate_authority_determinations(
    determinations: Mapping[str, Any],
    receipt: Mapping[str, Any],
    authority_digest: str,
    acquisition_digest: str,
    acquisition_retrieved_at: str | None = None,
) -> dict[str, Mapping[str, Any]]:
    """Validate the immutable, human-authored six-role decision boundary.

    This deliberately validates record shape and byte bindings only. It never
    turns an approved intake determination into a verified claim, ADR decision,
    package permission, or protocol fact.
    """
    if determinations.get("kind") != "human-authority-determinations":
        raise ValueError("authority determinations kind is invalid")
    if receipt.get("kind") != "authority-determinations-receipt":
        raise ValueError("authority receipt kind is invalid")
    if receipt.get("authorityArtifactPath") != ".planning/research/authority-determinations.yaml":
        raise ValueError("authority receipt path is invalid")
    if _sha256(receipt.get("authorityArtifactSha256"), "authority receipt artifact digest is invalid") != authority_digest:
        raise ValueError("authority receipt artifact digest does not match determination bytes")
    bound_acquisition_digest = _sha256(receipt.get("acquisitionReceiptSha256"), "authority receipt acquisition digest is invalid")
    if bound_acquisition_digest != acquisition_digest:
        raise ValueError("authority receipt acquisition digest does not match the bound acquisition receipt")
    if _required_string(receipt.get("reviewerIdentity"), "authority receipt reviewer identity is missing") != _required_string(
        determinations.get("reviewerIdentity"), "authority reviewer identity is missing"
    ):
        raise ValueError("authority receipt reviewer identity differs from determination record")
    if determinations.get("acquisitionReceiptPath") != receipt.get("acquisitionReceiptPath"):
        raise ValueError("authority determination acquisition receipt path differs from receipt")
    if _sha256(determinations.get("acquisitionReceiptSha256"), "authority determination acquisition digest is invalid") != bound_acquisition_digest:
        raise ValueError("authority determination acquisition digest differs from receipt")

    scope_ids = _string_list(determinations.get("scopeIds"), "authority scope IDs are missing")
    receipt_scope_ids = _string_list(receipt.get("scopeIds"), "authority receipt scope IDs are missing")
    if scope_ids != sorted(scope_ids) or receipt_scope_ids != scope_ids:
        raise ValueError("authority scope IDs are not the exact sorted receipt scope set")
    records = determinations.get("authorityDeterminations")
    if not isinstance(records, list) or len(records) != len(scope_ids):
        raise ValueError("authority determinations do not cover the exact scope set")

    freshness_floor = _rfc3339(acquisition_retrieved_at, "bound acquisition receipt retrieval time is invalid") if acquisition_retrieved_at else None
    by_scope: dict[str, Mapping[str, Any]] = {}
    determination_ids: set[str] = set()
    for scope in records:
        if not isinstance(scope, Mapping):
            raise ValueError("authority determination scope must be a mapping")
        scope_id = _required_string(scope.get("scopeId"), "authority scope ID is missing")
        if scope_id in by_scope:
            raise ValueError("duplicate authority scope ID")
        if scope_id not in scope_ids or scope.get("candidateId") != scope_id:
            raise ValueError("authority scope does not match the receipt-bound candidate")
        _required_string(scope.get("sourcePurpose"), "authority source purpose is missing")
        _required_string(scope.get("authorityClass"), "authority class is missing")
        _required_string(scope.get("evidenceClass"), "authority evidence class is missing")
        if _sha256(scope.get("acquisitionReceiptSha256"), "authority scope acquisition digest is invalid") != bound_acquisition_digest:
            raise ValueError("authority scope acquisition digest differs from receipt")
        queue_impact = scope.get("queueImpact")
        if not isinstance(queue_impact, Mapping):
            raise ValueError("authority scope queue impact is missing")
        for key in ("affectedClaims", "affectedDrift", "affectedQuestions"):
            _string_list(queue_impact.get(key), f"authority scope {key} is missing")

        decisions = scope.get("determinations")
        if not isinstance(decisions, list) or len(decisions) != len(AUTHORITY_ROLES):
            raise ValueError("authority scope requires exactly six role determinations")
        roles: set[str] = set()
        rationales: set[str] = set()
        role_effects: set[str] = set()
        for decision in decisions:
            if not isinstance(decision, Mapping):
                raise ValueError("authority role determination must be a mapping")
            decision_id = _required_string(decision.get("id"), "authority determination ID is missing")
            if decision_id in determination_ids:
                raise ValueError("duplicate authority determination ID")
            determination_ids.add(decision_id)
            role = _required_string(decision.get("role"), "authority role is missing")
            if role not in AUTHORITY_ROLES:
                raise ValueError("authority role is unrecognized")
            if role in roles:
                raise ValueError("duplicate authority role determination")
            roles.add(role)
            if decision.get("decision") not in {"approved", "blocked", "rejected", "not-applicable"}:
                raise ValueError("authority role decision is invalid")
            _required_string(decision.get("determinedBy"), "authority determination actor is missing")
            _rfc3339(decision.get("determinedAt"), "authority determination timestamp is invalid")
            freshness = _rfc3339(decision.get("freshnessCheckedAt"), "authority determination freshness timestamp is invalid")
            if freshness_floor is not None and freshness < freshness_floor:
                raise ValueError("authority determination is stale relative to the bound acquisition receipt")
            rationale = _required_string(decision.get("rationale"), "authority determination rationale is missing")
            if rationale in rationales:
                raise ValueError("authority scope has generic/shared rationale text")
            rationales.add(rationale)
            references = decision.get("evidenceReferences")
            if decision.get("decision") == "not-applicable":
                _required_string(decision.get("notApplicableRationale"), "not-applicable authority role lacks a bounded dated rationale")
            elif not isinstance(references, list) or not references:
                raise ValueError("authority role evidence references are missing")
            if isinstance(references, list):
                for reference in references:
                    if not isinstance(reference, Mapping):
                        raise ValueError("authority evidence reference is malformed")
                    _required_string(reference.get("id"), "authority evidence reference ID is missing")
                    _required_string(reference.get("locator"), "authority evidence reference locator is missing")
                    _required_string(reference.get("relevance"), "authority evidence reference relevance is missing")
            impact = decision.get("impactMap")
            if not isinstance(impact, Mapping):
                raise ValueError("authority role impact map is missing")
            for key in ("affectedRequirements", "affectedPhases", "affectedAdrs", "affectedLessons"):
                _string_list(impact.get(key), f"authority role {key} impact is missing")
            role_effect = _required_string(impact.get("roleEffect"), "authority role effect is missing")
            if role_effect in role_effects:
                raise ValueError("authority scope has generic/shared role effect text")
            role_effects.add(role_effect)
        if roles != set(AUTHORITY_ROLES):
            raise ValueError("authority scope requires exactly six unique roles")
        by_scope[scope_id] = scope
    if set(by_scope) != set(scope_ids):
        raise ValueError("authority determinations do not match the declared scope IDs")
    return by_scope


def require_current_authority_determinations(
    determinations: Mapping[str, Any],
    receipt: Mapping[str, Any],
    authority_digest: str,
    acquisition_digest: str,
    scope_id: str,
    acquisition_retrieved_at: str | None = None,
) -> Mapping[str, Any]:
    """Return one current complete intake scope, otherwise reject before intake."""
    scopes = validate_authority_determinations(
        determinations, receipt, authority_digest, acquisition_digest, acquisition_retrieved_at
    )
    try:
        return scopes[scope_id]
    except KeyError as exc:
        raise ValueError("authority determination scope is absent or scope-mismatched") from exc


def _validate_scope_against_outcome(scope: Mapping[str, Any], outcome: Mapping[str, Any]) -> None:
    candidate_id = _required_string(outcome.get("candidateId"), "reviewed outcome candidate ID is missing")
    if scope.get("scopeId") != candidate_id or scope.get("candidateId") != candidate_id:
        raise ValueError("authority determination scope does not match the reviewed outcome")
    queue_impact = scope.get("queueImpact")
    if not isinstance(queue_impact, Mapping):
        raise ValueError("authority scope queue impact is missing")
    for scope_key, outcome_key in (("affectedClaims", "affectedClaims"), ("affectedDrift", "affectedDrift"), ("affectedQuestions", "affectedQuestions")):
        if queue_impact.get(scope_key) != outcome.get(outcome_key):
            raise ValueError("authority determination impact scope differs from reviewed outcome")


def _validate_reviewed_source_input_binding(binding: Any) -> Mapping[str, Any]:
    if not isinstance(binding, Mapping):
        raise ValueError("reviewed-source input binding is missing")
    try:
        validate_reviewed_refresh_binding(binding)
    except ValueError as exc:
        raise ValueError(f"reviewed-source input binding is invalid: {exc}") from exc
    return binding


def prepare_authority_gated_intake(
    outcome: Mapping[str, Any],
    scope: Mapping[str, Any],
    acquisition_digest: str,
    *,
    reviewed_source_input_binding: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create either a limited observed record or deterministic blocked attempt.

    The caller must validate the whole determinations document before selecting a
    scope. This function still checks the selected scope and receipt-bound input
    relationship so an altered, unbound, or mismatched row cannot mutate a
    canonical record.
    """
    binding = _validate_reviewed_source_input_binding(reviewed_source_input_binding)
    if _sha256(scope.get("acquisitionReceiptSha256"), "authority scope acquisition digest is invalid") != acquisition_digest:
        raise ValueError("authority scope acquisition digest differs from reviewed acquisition receipt")
    _validate_scope_against_outcome(scope, outcome)
    decisions = scope.get("determinations")
    if not isinstance(decisions, list) or {decision.get("role") for decision in decisions if isinstance(decision, Mapping)} != set(AUTHORITY_ROLES):
        raise ValueError("authority scope requires exactly six unique role determinations")
    statuses = {decision.get("decision") for decision in decisions if isinstance(decision, Mapping)}
    candidate_id = _required_string(outcome.get("candidateId"), "reviewed outcome candidate ID is missing")
    blocked = outcome.get("result") != "collected" or statuses & {"blocked", "rejected"}
    if blocked:
        return {
            "status": "blocked",
            "blockedAttempt": {
                "id": f"ACQ-01-31-BLOCKED-{candidate_id}",
                "candidateId": candidate_id,
                "sourceIds": [candidate_id],
                "result": "blocked",
                "reason": "Receipt-bound authority scope is unavailable, incomplete, or intentionally blocked; no substitute evidence was accepted.",
                "affectedClaims": list(outcome.get("affectedClaims", [])),
                "affectedDrift": list(outcome.get("affectedDrift", [])),
                "affectedQuestions": list(outcome.get("affectedQuestions", [])),
                "safeFallback": "Preserve the affected evidence as blocked and do not infer a normative claim, ADR acceptance, or production permission.",
                "refreshTrigger": _required_string(outcome.get("refreshTrigger"), "reviewed outcome refresh trigger is missing"),
                "reviewedSourceInputBinding": dict(binding),
            },
        }
    if scope.get("authorityClass") not in {"observed-implementation", "observed-release-metadata"}:
        raise ValueError("approved authority scope cannot elevate unqualified material into a normative source")
    required = ("repository", "commitSha", "path", "contentSha256", "retrievedAt")
    for key in required:
        _required_string(outcome.get(key), f"reviewed collected outcome {key} is missing")
    record = {
        "id": f"SRC-{candidate_id.removeprefix('CAND-SRC-')}",
        "kind": "source",
        "collectionStatus": "collected",
        "rawOrigin": "observed-implementation",
        "repository": outcome["repository"],
        "officialUrl": f"https://github.com/{outcome['repository']}",
        "immutableUrl": outcome.get("immutableLocator") or f"https://github.com/{outcome['repository']}/blob/{outcome['commitSha']}/{outcome['path']}",
        "ref": outcome["commitSha"],
        "commitSha": outcome["commitSha"],
        "path": outcome["path"],
        "locator": f"commit:{outcome['commitSha']} path:{outcome['path']}",
        "contentSha256": outcome["contentSha256"],
        "retrievedAt": outcome["retrievedAt"],
        "authorityTier": "official-repository-observation",
        "evidenceClass": "implementation",
        "maturity": "implementation-specific",
        "uncertainty": {"state": "material", "reason": "Receipt-bound repository bytes are observed implementation evidence, not normative protocol authority."},
        "impacts": {"requirements": ["EVID-03"], "phases": ["01"]},
        "freshness": {"state": "provisional", "refreshTrigger": outcome["refreshTrigger"]},
        "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]},
    }
    return {"status": "ready", "record": record}


def validate_authority_receipt_files(determinations_path: Path, receipt_path: Path) -> dict[str, Mapping[str, Any]]:
    """Validate exact artifact bytes against its receipt and bound acquisition receipt."""
    determinations = _yaml_mapping(determinations_path, "authority determinations")
    receipt = _yaml_mapping(receipt_path, "authority receipt")
    acquisition_path_text = _required_string(receipt.get("acquisitionReceiptPath"), "authority receipt acquisition path is missing")
    acquisition_path = (ROOT / acquisition_path_text).resolve()
    try:
        acquisition_path.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError("authority receipt acquisition path escapes the repository") from exc
    try:
        acquisition_bytes = acquisition_path.read_bytes()
    except OSError as exc:
        raise ValueError("bound acquisition receipt is missing") from exc
    try:
        acquisition = json.loads(acquisition_bytes)
    except json.JSONDecodeError as exc:
        raise ValueError("bound acquisition receipt is not valid JSON") from exc
    if not isinstance(acquisition, Mapping):
        raise ValueError("bound acquisition receipt must be a mapping")
    retrieved_at = acquisition.get("retrievedAt")
    return validate_authority_determinations(
        determinations,
        receipt,
        hashlib.sha256(determinations_path.read_bytes()).hexdigest(),
        hashlib.sha256(acquisition_bytes).hexdigest(),
        retrieved_at if isinstance(retrieved_at, str) else None,
    )


def intake_receipt_bound_outcome(
    outcome: Mapping[str, Any],
    determinations_path: Path,
    receipt_path: Path,
    *,
    reviewed_source_input_binding: Mapping[str, Any],
) -> dict[str, Any]:
    """Authority-gate one receipt row before a caller persists any canonical result."""
    scopes = validate_authority_receipt_files(determinations_path, receipt_path)
    receipt = _yaml_mapping(receipt_path, "authority receipt")
    scope = require_current_authority_determinations(
        _yaml_mapping(determinations_path, "authority determinations"),
        receipt,
        hashlib.sha256(determinations_path.read_bytes()).hexdigest(),
        _sha256(receipt.get("acquisitionReceiptSha256"), "authority receipt acquisition digest is invalid"),
        _required_string(outcome.get("candidateId"), "reviewed outcome candidate ID is missing"),
    )
    # Keep the call above explicit: no record construction happens until the
    # full immutable artifact and the exact requested scope have passed.
    if scope["scopeId"] not in scopes:
        raise ValueError("authority scope lookup is not stable")
    return prepare_authority_gated_intake(
        outcome,
        scope,
        _sha256(receipt.get("acquisitionReceiptSha256"), "authority receipt acquisition digest is invalid"),
        reviewed_source_input_binding=reviewed_source_input_binding,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and pin bounded Tier 1 source inputs without network writes.")
    subparsers = parser.add_subparsers(dest="command")
    collect_parser = subparsers.add_parser("collect", help="collect only the reviewed, bounded public GitHub observation window")
    collect_parser.add_argument("--queue", type=Path, required=True)
    collect_parser.add_argument("--receipt", type=Path, required=True)
    collect_parser.add_argument("--cache-root", type=Path, required=True)
    validate_parser = subparsers.add_parser("validate-reviewed-acquisition", help="revalidate queue/receipt Git-blob input bindings")
    validate_parser.add_argument("--queue", type=Path, required=True)
    validate_parser.add_argument("--receipt", type=Path, required=True)
    validate_parser.add_argument("--review", type=Path, required=True)
    authority_receipt_parser = subparsers.add_parser("validate-authority-receipt", help="validate exact human authority determination and acquisition receipt bindings")
    authority_receipt_parser.add_argument("--determinations", type=Path, required=True, help="Path to the human-authored authority determinations YAML")
    authority_receipt_parser.add_argument("--receipt", type=Path, required=True, help="Path to the digest-bound authority receipt YAML")
    parser.add_argument("--validate-url", help="validate one candidate URL against the Tier 1 HTTPS allowlist")
    parser.add_argument("--cache-root", default=str(CACHE_ROOT), help="ignored cache path; must remain under .research/upstreams/")
    parser.add_argument("--repository-dir", type=Path, help="existing local clone to inspect; this command does not clone")
    parser.add_argument("--ref", help="mutable discovery ref to resolve")
    parser.add_argument("--path", help="repository-relative source path to resolve")
    args = parser.parse_args()

    try:
        if args.command == "collect":
            return collect_reviewed_public_window(
                args.queue, args.receipt, _confined_cache_root(args.cache_root),
                ROOT / ".planning/phases/01-research-and-truth-baseline/01-REVIEWS.md",
            )
        if args.command == "validate-reviewed-acquisition":
            queue = json.loads(_checked_output_path(args.queue).read_text(encoding="utf-8"))
            receipt = json.loads(_checked_output_path(args.receipt).read_text(encoding="utf-8"))
            _revalidate_reviewed_binding(queue, receipt, _checked_output_path(args.review))
            print("reviewed acquisition binding passed")
            return 0
        if args.command == "validate-authority-receipt":
            validate_authority_receipt_files(args.determinations, args.receipt)
            print("authority receipt binding passed")
            return 0
        if args.validate_url:
            error = reject_unallowlisted(args.validate_url)
            if error:
                print(error, file=sys.stderr)
                return 2
            print("allowlisted")
            return 0
        cache_path(args.cache_root)
        if not (args.repository_dir and args.ref and args.path):
            parser.error("supply collect, validate-reviewed-acquisition, --validate-url, or --repository-dir, --ref, and --path")
        repository = args.repository_dir.resolve()
        if not (repository / ".git").exists():
            raise ValueError("repository-dir must be an existing local Git clone")
        print(json.dumps(resolve_blob(repository, args.ref, args.path), sort_keys=True))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
