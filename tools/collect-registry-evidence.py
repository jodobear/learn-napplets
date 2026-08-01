#!/usr/bin/env python3
"""Collect bounded registry evidence without installing or importing packages.

Fixture collection proves receipt mechanics only. Live collection is a separate,
operator-gated read-only attempt; unavailable or non-permitted collection writes
an impact-scoped blocker instead of promoting fixture material to artifact fact.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote, urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_HOST = "registry.npmjs.org"
CANONICAL_PACKAGE = "@napplet/web"
CANONICAL_URL = f"https://{REGISTRY_HOST}/{quote(CANONICAL_PACKAGE, safe='')}"
MAX_RESPONSE_BYTES = 65_536
CONNECT_TIMEOUT_SECONDS = 5
READ_TIMEOUT_SECONDS = 5
TOTAL_TIMEOUT_SECONDS = 10
_ATTEMPT_RE = re.compile(r"^REG-(?:FIXTURE|LIVE|BLOCKER)-[A-Z0-9-]{3,80}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ReceiptError(ValueError):
    """Raised when an evidence receipt violates its fixed bounded contract."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _require_timestamp(value: Any) -> str:
    if not isinstance(value, str):
        raise ReceiptError("retrieval timestamp must be an RFC3339 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReceiptError("retrieval timestamp must be RFC3339") from exc
    if parsed.tzinfo is None:
        raise ReceiptError("retrieval timestamp must include a timezone")
    return value


def _relative_regular_file(path: Path, *, must_exist: bool) -> Path:
    """Return a confined regular path without traversing symlinks."""
    raw = path.expanduser()
    candidate = raw if raw.is_absolute() else ROOT / raw
    try:
        relative = candidate.relative_to(ROOT)
    except ValueError as exc:
        raise ReceiptError("path must remain inside the repository") from exc
    current = ROOT
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ReceiptError("path must not traverse a symlink")
    if must_exist:
        try:
            mode = candidate.stat(follow_symlinks=False).st_mode
        except OSError as exc:
            raise ReceiptError("required input path is missing") from exc
        if not candidate.is_file() or candidate.is_symlink() or not stat.S_ISREG(mode):
            raise ReceiptError("input must be a regular file")
    return candidate


def _receipt_target(path: Path) -> Path:
    target = _relative_regular_file(path, must_exist=False)
    if target.exists() or target.is_symlink():
        raise ReceiptError("receipt path already exists; immutable history cannot be overwritten")
    if not target.parent.is_dir():
        raise ReceiptError("receipt parent directory must already exist")
    return target


def _request_record() -> dict[str, str]:
    return {
        "method": "GET",
        "canonicalUrl": CANONICAL_URL,
        "allowedHost": REGISTRY_HOST,
        "redirectPolicy": "refuse",
    }


def _limits_record() -> dict[str, int]:
    return {
        "connectTimeoutSeconds": CONNECT_TIMEOUT_SECONDS,
        "readTimeoutSeconds": READ_TIMEOUT_SECONDS,
        "timeoutSeconds": TOTAL_TIMEOUT_SECONDS,
        "maxResponseBytes": MAX_RESPONSE_BYTES,
    }


def _fixture_receipt(attempt_id: str, retrieved_at: str, response: bytes) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "registry-collection-receipt",
        "attemptId": attempt_id,
        "transport": "fixture",
        "outcome": "fixture-mechanism-only",
        "retrievedAt": retrieved_at,
        "request": _request_record(),
        "limits": _limits_record(),
        "response": {
            "status": 200,
            "headers": {"content-type": "application/json"},
            "byteCount": len(response),
            "sha256": hashlib.sha256(response).hexdigest(),
            "capturedBytes": response.hex(),
        },
        "authority": {
            "classification": "fixture-mechanism-only",
            "statement": "This retained fixture proves collector and exact-byte receipt mechanics only; it is not a published-package fact or admission approval.",
        },
    }


def _blocker_receipt(attempt_id: str, retrieved_at: str, reason: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "registry-collection-receipt",
        "attemptId": attempt_id,
        "transport": "live-or-blocker",
        "outcome": "impact-scoped-blocker",
        "retrievedAt": retrieved_at,
        "request": _request_record(),
        "limits": _limits_record(),
        "blocker": {
            "reason": reason,
            "affectedRequirements": ["EVID-03", "EVID-04", "OPER-01"],
            "affectedPhases": ["01"],
            "affectedAdrs": ["ADR-0005", "ADR-0008", "ADR-0010"],
            "affectedQuestions": ["OQ-PUBLIC-PACKAGE-BASELINE-001", "OQ-PUBLIC-CONFORMANCE-001"],
            "affectedDrift": ["DRF-ARTIFACT-001", "DRF-CONFORMANCE-001"],
            "safeFallback": "Keep the deterministic static path dependency-free and retain SPK-G package admission as blocked.",
            "refreshTrigger": "Collect a public read-only registry response only after the exact package scope is essential, sandboxed, credential-free, and separately approved; then revalidate every receipt and eligibility field.",
        },
        "authority": {
            "classification": "impact-scoped-blocker",
            "statement": "No live registry observation was made, and no fixture response may be promoted to a published-package fact.",
        },
    }


def _live_receipt(attempt_id: str, retrieved_at: str, status: int, headers: Mapping[str, str], response: bytes) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "registry-collection-receipt",
        "attemptId": attempt_id,
        "transport": "live-or-blocker",
        "outcome": "observed-live",
        "retrievedAt": retrieved_at,
        "request": _request_record(),
        "limits": _limits_record(),
        "response": {
            "status": status,
            "headers": {"content-type": headers.get("content-type", "")},
            "byteCount": len(response),
            "sha256": hashlib.sha256(response).hexdigest(),
            "capturedBytes": response.hex(),
        },
        "authority": {
            "classification": "observed-registry-metadata",
            "statement": "This is an observed registry response only. It does not install, import, approve, or prove package conformance or protocol behavior.",
        },
    }


def _write_receipt_exclusive(target: Path, document: Mapping[str, Any]) -> None:
    content = yaml.safe_dump(dict(document), sort_keys=False, allow_unicode=True).encode("utf-8")
    try:
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise ReceiptError("receipt path already exists; immutable history cannot be overwritten") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            target.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def _read_bounded_response(url: str) -> tuple[int, dict[str, str], bytes]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != REGISTRY_HOST or url != CANONICAL_URL:
        raise ReceiptError("live collection target is not the one allowlisted canonical registry URL")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPRedirectHandler())
    # HTTPRedirectHandler is overridden by the handler below so redirect expansion is never followed.
    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
            raise ReceiptError("redirect refused for bounded registry collection")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())
    request = urllib.request.Request(url, method="GET", headers={"Accept": "application/json", "User-Agent": "learn-napplets-phase1-registry-evidence"})
    with opener.open(request, timeout=TOTAL_TIMEOUT_SECONDS) as response:  # nosec B310: exact HTTPS host and URL are enforced above.
        if response.geturl() != url:
            raise ReceiptError("redirect refused for bounded registry collection")
        status = int(response.status)
        if status != 200:
            raise ReceiptError("registry response status is not an allowed success status")
        chunks: list[bytes] = []
        remaining = MAX_RESPONSE_BYTES + 1
        while remaining:
            chunk = response.read(min(8192, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > MAX_RESPONSE_BYTES:
            raise ReceiptError("registry response exceeds the fixed response-size cap")
        return status, {"content-type": response.headers.get("Content-Type", "")}, payload


def _validate_response(response: Any) -> None:
    if not isinstance(response, Mapping):
        raise ReceiptError("receipt response is missing")
    if response.get("status") != 200:
        raise ReceiptError("receipt response status must be 200")
    headers = response.get("headers")
    if not isinstance(headers, Mapping) or not isinstance(headers.get("content-type"), str):
        raise ReceiptError("receipt response headers are malformed")
    captured = response.get("capturedBytes")
    if not isinstance(captured, str) or len(captured) % 2:
        raise ReceiptError("receipt captured bytes must be hexadecimal")
    try:
        content = bytes.fromhex(captured)
    except ValueError as exc:
        raise ReceiptError("receipt captured bytes must be hexadecimal") from exc
    if response.get("byteCount") != len(content) or len(content) > MAX_RESPONSE_BYTES:
        raise ReceiptError("receipt response byte count is invalid")
    if response.get("sha256") != hashlib.sha256(content).hexdigest():
        raise ReceiptError("receipt response SHA-256 does not rehash exact captured bytes")


def validate_receipt(document: Any) -> None:
    if not isinstance(document, Mapping):
        raise ReceiptError("receipt must be a YAML mapping")
    if document.get("schemaVersion") != 1 or document.get("kind") != "registry-collection-receipt":
        raise ReceiptError("receipt schema identity is invalid")
    attempt_id = document.get("attemptId")
    if not isinstance(attempt_id, str) or not _ATTEMPT_RE.fullmatch(attempt_id):
        raise ReceiptError("receipt attempt ID is invalid")
    transport = document.get("transport")
    outcome = document.get("outcome")
    if transport not in {"fixture", "live-or-blocker"}:
        raise ReceiptError("receipt transport classification is invalid")
    if (transport, outcome) not in {("fixture", "fixture-mechanism-only"), ("live-or-blocker", "observed-live"), ("live-or-blocker", "impact-scoped-blocker")}:
        raise ReceiptError("receipt transport and outcome classifications conflict")
    _require_timestamp(document.get("retrievedAt"))
    request = document.get("request")
    if not isinstance(request, Mapping) or dict(request) != _request_record():
        raise ReceiptError("receipt request must retain the fixed GET, allowlist, canonical URL, and redirect policy")
    limits = document.get("limits")
    if not isinstance(limits, Mapping) or dict(limits) != _limits_record():
        raise ReceiptError("receipt limits must retain the fixed positive timeout and response-size bounds")
    authority = document.get("authority")
    if not isinstance(authority, Mapping) or not isinstance(authority.get("statement"), str) or not authority["statement"]:
        raise ReceiptError("receipt authority classification is malformed")
    if outcome == "impact-scoped-blocker":
        blocker = document.get("blocker")
        if not isinstance(blocker, Mapping):
            raise ReceiptError("blocked live collection requires an impact-scoped blocker")
        required_lists = {
            "affectedRequirements": ["EVID-03", "EVID-04", "OPER-01"],
            "affectedPhases": ["01"],
            "affectedAdrs": ["ADR-0005", "ADR-0008", "ADR-0010"],
            "affectedQuestions": ["OQ-PUBLIC-PACKAGE-BASELINE-001", "OQ-PUBLIC-CONFORMANCE-001"],
            "affectedDrift": ["DRF-ARTIFACT-001", "DRF-CONFORMANCE-001"],
        }
        for field, expected in required_lists.items():
            if blocker.get(field) != expected:
                raise ReceiptError(f"blocked live collection has invalid {field}")
        if not all(isinstance(blocker.get(field), str) and blocker[field] for field in ("reason", "safeFallback", "refreshTrigger")):
            raise ReceiptError("blocked live collection lacks reason, fallback, or refresh trigger")
        if "response" in document:
            raise ReceiptError("blocked live collection must not contain a fixture or observed response")
    else:
        _validate_response(document.get("response"))
        if "blocker" in document:
            raise ReceiptError("response receipt must not carry a blocker")
    expected_authority = "fixture-mechanism-only" if transport == "fixture" else ("impact-scoped-blocker" if outcome == "impact-scoped-blocker" else "observed-registry-metadata")
    if authority.get("classification") != expected_authority:
        raise ReceiptError("receipt authority classification conflicts with transport outcome")


def _load_receipt(path: Path) -> Mapping[str, Any]:
    candidate = _relative_regular_file(path, must_exist=True)
    try:
        document = yaml.safe_load(candidate.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReceiptError("receipt cannot be read as safe YAML") from exc
    if not isinstance(document, Mapping):
        raise ReceiptError("receipt must be a YAML mapping")
    return document


def _attempt_id(kind: str) -> str:
    return f"REG-{kind}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"


def collect_fixture(args: argparse.Namespace) -> int:
    fixture = _relative_regular_file(args.fixture, must_exist=True)
    target = _receipt_target(args.receipt)
    response = fixture.read_bytes()
    if len(response) > MAX_RESPONSE_BYTES:
        raise ReceiptError("fixture response exceeds the fixed response-size cap")
    document = _fixture_receipt(args.attempt_id or _attempt_id("FIXTURE"), args.retrieved_at or _utc_now(), response)
    validate_receipt(document)
    _write_receipt_exclusive(target, document)
    validate_receipt(_load_receipt(target))
    print(f"fixture receipt created: {target.relative_to(ROOT)}")
    return 0


def collect_live_or_blocker(args: argparse.Namespace) -> int:
    target = _receipt_target(args.receipt)
    attempt_id = args.attempt_id or _attempt_id("LIVE")
    retrieved_at = args.retrieved_at or _utc_now()
    if not (args.live_authorized and args.essential_sandboxed):
        document = _blocker_receipt(
            attempt_id if attempt_id.startswith("REG-BLOCKER-") else attempt_id.replace("REG-LIVE-", "REG-BLOCKER-"),
            retrieved_at,
            "Live registry collection was not run because the D-10 public-read and D-24 essential sandboxed credential-free predicates were not both explicitly declared; no package command or import was attempted.",
        )
    else:
        try:
            status, headers, response = _read_bounded_response(CANONICAL_URL)
            document = _live_receipt(attempt_id, retrieved_at, status, headers, response)
        except (ReceiptError, urllib.error.URLError, OSError) as exc:
            document = _blocker_receipt(
                attempt_id if attempt_id.startswith("REG-BLOCKER-") else attempt_id.replace("REG-LIVE-", "REG-BLOCKER-"),
                retrieved_at,
                f"Bounded live registry collection was unavailable: {exc}; no package command or import was attempted.",
            )
    validate_receipt(document)
    _write_receipt_exclusive(target, document)
    validate_receipt(_load_receipt(target))
    print(f"live-or-blocker receipt created: {target.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect bounded registry metadata without package execution.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    fixture = subcommands.add_parser("collect-fixture", help="capture a checked-in deterministic response fixture")
    fixture.add_argument("--fixture", type=Path, required=True)
    fixture.add_argument("--receipt", type=Path, required=True)
    fixture.add_argument("--attempt-id")
    fixture.add_argument("--retrieved-at")
    live = subcommands.add_parser("collect-live-or-blocker", help="record an observed live response or impact-scoped blocker")
    live.add_argument("--live-if-permitted", action="store_true", required=True)
    live.add_argument("--live-authorized", action="store_true", help="operator declaration for D-10 public read")
    live.add_argument("--essential-sandboxed", action="store_true", help="operator declaration for D-24 essential credential-free sandbox")
    live.add_argument("--receipt", type=Path, required=True)
    live.add_argument("--attempt-id")
    live.add_argument("--retrieved-at")
    validate = subcommands.add_parser("validate-receipt", help="rehash and validate one immutable receipt")
    validate.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "collect-fixture":
            return collect_fixture(args)
        if args.command == "collect-live-or-blocker":
            return collect_live_or_blocker(args)
        validate_receipt(_load_receipt(args.receipt))
        print("registry receipt validation passed")
        return 0
    except ReceiptError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
