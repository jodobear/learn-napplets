#!/usr/bin/env python3
"""Validate Phase 1 canonical evidence records without changing review state."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, NamedTuple

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = {"supports", "contradicts", "measures", "affects", "recommends", "supersedes"}


def canonical_recovery_module() -> Any:
    """Load the Plan 01-42 ownership boundary without reopening canonical paths."""
    spec = importlib.util.spec_from_file_location("canonical_recovery", ROOT / "tools" / "canonical-recovery.py")
    if spec is None or spec.loader is None:
        raise ValueError("canonical recovery module is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_registered_snapshot(reader_id: str, targets: tuple[str, ...], planning_root: Path) -> Mapping[str, bytes]:
    """Acquire a complete in-memory generation before a multi-file route parses it."""
    try:
        return canonical_recovery_module().read_canonical_snapshot(reader_id, targets, root=planning_root)
    except Exception as exc:
        raise ValueError(f"canonical snapshot refused for {reader_id}: {exc}") from exc


COMPATIBILITY_SNAPSHOT_TARGETS = (
    "research/source-registry.yaml",
    "research/claims.yaml",
    "research/compatibility-matrix.yaml",
    "research/drift-register.yaml",
    "research/open-questions.yaml",
    "research/package-evidence.yaml",
    "research/package-map.md",
    "research/upstream-acquisition-queue.yaml",
    "research/reports/upstream-acquisition-20260728.md",
    "spikes/spk-g-package-conformance/metadata.yaml",
    "spikes/spk-g-package-conformance/report.md",
)
COMPATIBILITY_DIMENSION_ORDER = (
    "normativeProtocol",
    "observedImplementation",
    "publishedPackage",
    "runtime",
    "exampleFixture",
    "currentWork",
    "conformance",
)


def dimension_reason_token(name: str) -> str:
    """Return the stable ordered diagnostic token for a closed dimension name."""
    return re.sub(r"(?<!^)([A-Z])", r"_\1", name).upper()


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _snapshot_yaml(snapshot: Mapping[str, bytes], target: str) -> Mapping[str, Any]:
    try:
        value = normalize_yaml(yaml.safe_load(snapshot[target].decode("utf-8")))
    except (KeyError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"compatibility snapshot target is unavailable or malformed: {target}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"compatibility snapshot target must be an object: {target}")
    return value


def _snapshot_json(snapshot: Mapping[str, bytes], target: str) -> Mapping[str, Any]:
    try:
        value = json.loads(snapshot[target].decode("utf-8"))
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"compatibility snapshot target is unavailable or malformed: {target}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"compatibility snapshot target must be an object: {target}")
    return value


def _family_digest(snapshot: Mapping[str, bytes], prefix: str) -> str:
    digest = hashlib.sha256()
    for target in sorted(item for item in snapshot if item.startswith(prefix)):
        digest.update(target.encode("utf-8")); digest.update(b"\0")
        digest.update(snapshot[target]); digest.update(b"\0")
    return digest.hexdigest()


class CompatibilitySnapshotIndex(NamedTuple):
    """The sole dependency of compatibility eligibility evaluation.

    Every family is parsed from bytes returned by the registered Plan 01-42 reader.
    This type intentionally carries no root or path attribute, preventing helpers
    from reopening mutable canonical records after the snapshot is acquired.
    """

    sources: Mapping[str, Mapping[str, Any]]
    claims: Mapping[str, Mapping[str, Any]]
    compatibility: tuple[Mapping[str, Any], ...]
    drift: Mapping[str, Mapping[str, Any]]
    questions: Mapping[str, Mapping[str, Any]]
    package_evidence: Mapping[str, Any]
    package_map: str
    acquisition_queue: Mapping[str, Any]
    acquisition_receipt: Mapping[str, Any]
    spk_g_metadata: Mapping[str, Any]
    spk_g_report: str
    family_digests: Mapping[str, str]
    provenance_reasons: tuple[str, ...]


def build_compatibility_snapshot_index(snapshot: Mapping[str, bytes]) -> CompatibilitySnapshotIndex:
    """Parse the exact registered snapshot into immutable source-family indexes."""
    if tuple(snapshot) != COMPATIBILITY_SNAPSHOT_TARGETS:
        raise ValueError("compatibility snapshot target set is incomplete or unordered")
    source_document = _snapshot_yaml(snapshot, "research/source-registry.yaml")
    claim_document = _snapshot_yaml(snapshot, "research/claims.yaml")
    matrix_document = _snapshot_yaml(snapshot, "research/compatibility-matrix.yaml")
    drift_document = _snapshot_yaml(snapshot, "research/drift-register.yaml")
    question_document = _snapshot_yaml(snapshot, "research/open-questions.yaml")
    package_evidence = _snapshot_yaml(snapshot, "research/package-evidence.yaml")
    if matrix_document.get("schemaVersion") != 2:
        raise ValueError("compatibility-matrix.yaml must use schemaVersion 2; migrate legacy records first")
    queue = _snapshot_json(snapshot, "research/upstream-acquisition-queue.yaml")
    receipt = _snapshot_json(snapshot, "research/reports/upstream-acquisition-20260728.md")
    metadata = _snapshot_yaml(snapshot, "spikes/spk-g-package-conformance/metadata.yaml")
    try:
        sources = source_document["sources"]
        claims = claim_document["claims"]
        compatibility = matrix_document["compatibility"]
        drift = drift_document["drift"]
        questions = question_document["questions"]
    except KeyError as exc:
        raise ValueError("compatibility snapshot family lacks its required record list") from exc
    families = (sources, claims, compatibility, drift, questions)
    if any(not isinstance(family, list) or not all(isinstance(item, dict) for item in family) for family in families):
        raise ValueError("compatibility snapshot family contains malformed records")
    provenance_reasons: list[str] = []
    try:
        acquisition = canonical_acquisition_module()
        acquisition.validate_reviewed_acquisition_documents(queue, receipt)
    except Exception:
        provenance_reasons.append("PROVENANCE_REVIEWED_ACQUISITION_INVALID")
    return CompatibilitySnapshotIndex(
        sources=_freeze({item["id"]: item for item in sources if isinstance(item.get("id"), str)}),
        claims=_freeze({item["id"]: item for item in claims if isinstance(item.get("id"), str)}),
        compatibility=tuple(_freeze(item) for item in compatibility),
        drift=_freeze({item["id"]: item for item in drift if isinstance(item.get("id"), str)}),
        questions=_freeze({item["id"]: item for item in questions if isinstance(item.get("id"), str)}),
        package_evidence=_freeze(package_evidence),
        package_map=snapshot["research/package-map.md"].decode("utf-8"),
        acquisition_queue=_freeze(queue),
        acquisition_receipt=_freeze(receipt),
        spk_g_metadata=_freeze(metadata),
        spk_g_report=snapshot["spikes/spk-g-package-conformance/report.md"].decode("utf-8"),
        family_digests=_freeze({
            "SRC": _family_digest(snapshot, "research/source-registry.yaml"),
            "CLM": _family_digest(snapshot, "research/claims.yaml"),
            "CMP": _family_digest(snapshot, "research/compatibility-matrix.yaml"),
            "DRF": _family_digest(snapshot, "research/drift-register.yaml"),
            "OQ": _family_digest(snapshot, "research/open-questions.yaml"),
            "package": _family_digest(snapshot, "research/package-evidence.yaml") + _family_digest(snapshot, "research/package-map.md"),
            "SPK": _family_digest(snapshot, "spikes/spk-g-package-conformance/"),
        }),
        provenance_reasons=tuple(provenance_reasons),
    )


def canonical_acquisition_module() -> Any:
    spec = importlib.util.spec_from_file_location("phase1_acquire_sources", ROOT / "tools" / "acquire-sources.py")
    if spec is None or spec.loader is None:
        raise ValueError("reviewed acquisition validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compatibility_family_digests(index: CompatibilitySnapshotIndex) -> dict[str, str]:
    return dict(index.family_digests)


def _record_by_id(records: Mapping[str, Mapping[str, Any]], reference_id: Any) -> Mapping[str, Any] | None:
    return records.get(reference_id) if isinstance(reference_id, str) else None


def _qualified_source(source: Mapping[str, Any] | None, *, raw_origin: set[str], authority: set[str]) -> bool:
    if source is None:
        return False
    review = source.get("review")
    freshness = source.get("freshness")
    return (
        source.get("collectionStatus") == "collected"
        and source.get("rawOrigin") in raw_origin
        and source.get("authorityTier") in authority
        and isinstance(review, Mapping) and review.get("status") == "approved"
        and isinstance(freshness, Mapping) and freshness.get("state") != "stale"
    )


def _dimension_semantic_reason(name: str, dimension: Mapping[str, Any], index: CompatibilitySnapshotIndex) -> str | None:
    references = dimension.get("references")
    if not isinstance(references, tuple) or not references:
        return "MISSING_REFERENCE"
    ids = [reference.get("id") for reference in references if isinstance(reference, Mapping)]
    if len(ids) != len(references) or len(set(ids)) != len(ids):
        return "DUPLICATE_REFERENCE"
    known = set(index.sources) | set(index.claims) | set(index.drift) | set(index.questions)
    if any(reference_id not in known for reference_id in ids):
        return "UNKNOWN_REFERENCE"
    sources = [_record_by_id(index.sources, reference_id) for reference_id in ids]
    if any(source is not None and source.get("freshness", {}).get("state") == "stale" for source in sources):
        return "STALE_EVIDENCE"
    if name == "normativeProtocol":
        if not any(_qualified_source(source, raw_origin={"normative-protocol"}, authority={"official-normative", "official-protocol"}) for source in sources):
            return "WRONG_AUTHORITY"
    elif name in {"observedImplementation", "currentWork"}:
        if not any(_qualified_source(source, raw_origin={"observed-implementation"}, authority={"official-repository-observation"}) for source in sources):
            return "WRONG_AUTHORITY"
    elif name == "publishedPackage":
        artifact = index.package_evidence.get("artifactEvidence")
        if not isinstance(artifact, Mapping) or artifact.get("status") != "qualified" or index.package_evidence.get("approval") != "approved":
            return "SOURCE_RELEASE_ONLY"
    elif name == "runtime":
        if not any(_qualified_source(source, raw_origin={"runtime-measurement"}, authority={"independent-runtime-measurement"}) for source in sources):
            return "MISSING_INDEPENDENT_EVIDENCE"
    elif name == "exampleFixture":
        if not any(_qualified_source(source, raw_origin={"example-fixture"}, authority={"reproducible-fixture"}) for source in sources):
            return "MISSING_INDEPENDENT_EVIDENCE"
    elif name == "conformance":
        if index.spk_g_metadata.get("status") != "complete" or "conformance" not in index.spk_g_report.lower():
            return "MISSING_INDEPENDENT_EVIDENCE"
    return None


def evaluate_compatibility_baseline(snapshot_index: CompatibilitySnapshotIndex) -> dict[str, Any]:
    """Return deterministic substantive eligibility from an immutable snapshot only."""
    if not isinstance(snapshot_index, CompatibilitySnapshotIndex):
        raise TypeError("evaluate_compatibility_baseline requires CompatibilitySnapshotIndex")
    if snapshot_index.provenance_reasons:
        return {
            "status": "blocked", "approval": "not-approved", "architectureApproved": False,
            "reasons": list(snapshot_index.provenance_reasons), "familyDigests": compatibility_family_digests(snapshot_index),
        }
    baseline = next((record for record in snapshot_index.compatibility if record.get("id") == "CMP-BASELINE-001"), None)
    if baseline is None:
        return {"status": "blocked", "approval": "not-approved", "architectureApproved": False, "reasons": ["BASELINE_MISSING"], "familyDigests": compatibility_family_digests(snapshot_index)}
    dimensions = baseline.get("dimensions")
    by_name = {item.get("name"): item for item in dimensions if isinstance(item, Mapping)} if isinstance(dimensions, tuple) else {}
    reasons: list[str] = []
    for name in COMPATIBILITY_DIMENSION_ORDER:
        token = dimension_reason_token(name)
        dimension = by_name.get(name)
        if dimension is None:
            reasons.append(f"DIMENSION_{token}_MISSING")
            continue
        status = dimension.get("status")
        if status != "qualified":
            reasons.append(f"DIMENSION_{token}_{str(status or 'missing').upper().replace('-', '_')}")
            continue
        semantic = _dimension_semantic_reason(name, dimension, snapshot_index)
        if semantic is not None:
            reasons.append(f"DIMENSION_{token}_{semantic}")
    eligibility = baseline.get("baselineEligibility")
    approval = eligibility.get("approval") if isinstance(eligibility, Mapping) else "not-approved"
    reviewed = (
        isinstance(eligibility, Mapping)
        and approval == "approved"
        and eligibility.get("status") == "eligible"
        and isinstance(eligibility.get("reviewRecordId"), str)
        and bool(eligibility.get("reviewRecordId"))
    )
    if not reviewed:
        reasons.append("APPROVAL_NOT_GRANTED")
    return {
        "status": "eligible" if not reasons else "blocked",
        "approval": approval if reviewed else "not-approved",
        "architectureApproved": False,
        "reasons": reasons,
        "familyDigests": compatibility_family_digests(snapshot_index),
    }


def evaluate_registered_compatibility(planning_root: Path, *, after_snapshot: Any = None) -> dict[str, Any]:
    """Acquire the registered reader once, then evaluate only its frozen index."""
    snapshot = read_registered_snapshot("compatibility-baseline", COMPATIBILITY_SNAPSHOT_TARGETS, planning_root)
    index = build_compatibility_snapshot_index(snapshot)
    if after_snapshot is not None:
        after_snapshot()
    return evaluate_compatibility_baseline(index)


def validated_compatibility_snapshot_index(research_root: Path) -> CompatibilitySnapshotIndex:
    """Verify Plan 01-45's receipt against Plan 01-29 before snapshot acquisition."""
    planning_root = research_root.resolve(strict=True).parent
    review = planning_root / "phases/01-research-and-truth-baseline/01-REVIEWS.md"
    command = [
        sys.executable, str(ROOT / "tools/acquire-sources.py"), "validate-reviewed-acquisition",
        "--queue", str(planning_root / "research/upstream-acquisition-queue.yaml"),
        "--receipt", str(planning_root / "research/reports/upstream-acquisition-20260728.md"),
        "--review", str(review),
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip().replace("\n", " | ")
        raise ValueError(f"reviewed acquisition provenance refused before compatibility snapshot: {detail or 'non-zero exit'}")
    snapshot = read_registered_snapshot("compatibility-baseline", COMPATIBILITY_SNAPSHOT_TARGETS, planning_root)
    return build_compatibility_snapshot_index(snapshot)


def normalize_yaml(value: Any) -> Any:
    """Keep YAML timestamps compatible with the canonical string contract."""
    if isinstance(value, (datetime, date)):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, list):
        return [normalize_yaml(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_yaml(item) for key, item in value.items()}
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = normalize_yaml(yaml.safe_load(path.read_text(encoding="utf-8")))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read YAML {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def resolve_canonical_file(
    planning_root: Path,
    supplied_path: Any,
    expected_relative_path: str | None = None,
) -> Path:
    """Resolve one confined, canonical regular file below a planning root."""
    if not isinstance(supplied_path, str) or not supplied_path or "\x00" in supplied_path:
        raise ValueError("path must be a nonempty string without NUL")
    if Path(supplied_path).is_absolute() or "\\" in supplied_path:
        raise ValueError("path must be a relative POSIX path")
    parts = supplied_path.split("/")
    if any(part in {"", ".", ".."} for part in parts) or "/".join(parts) != supplied_path:
        raise ValueError("path must not contain normalization components")
    if expected_relative_path is not None and supplied_path != expected_relative_path:
        raise ValueError(f"path must equal canonical path {expected_relative_path}")
    try:
        root = planning_root.resolve(strict=True)
    except OSError as exc:
        raise ValueError(f"planning root cannot be resolved: {exc}") from exc
    candidate = planning_root.joinpath(*parts)
    current = planning_root
    try:
        for part in parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("path must not traverse a symlink")
        resolved = candidate.resolve(strict=True)
        mode = candidate.stat(follow_symlinks=False).st_mode
    except OSError as exc:
        raise ValueError(f"path cannot be resolved: {exc}") from exc
    if not resolved.is_relative_to(root) or not stat.S_ISREG(mode):
        raise ValueError("path must resolve to a confined regular file")
    return candidate


def schema_errors(schema_path: Path, records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    try:
        schema = load_json(schema_path)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
    except (ValueError, SchemaError) as exc:
        return [f"ERROR SCH001: invalid schema {schema_path.name}: {exc}"]
    for index, record in enumerate(records, start=1):
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
            location = ".".join(str(item) for item in error.absolute_path) or "record"
            errors.append(f"ERROR SCH002: {schema_path.name} record {index} {location}: {error.message}")
    return errors


def record_ids(records: list[dict[str, Any]], prefix: str) -> tuple[set[str], list[str]]:
    ids: set[str] = set()
    errors: list[str] = []
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id.startswith(prefix):
            errors.append(f"ERROR SEM002: expected {prefix} stable ID")
            continue
        if record_id in ids:
            errors.append(f"ERROR SEM001: duplicate record ID {record_id}")
        ids.add(record_id)
    return ids, errors


def validate_traceability() -> list[str]:
    errors: list[str] = []
    map_path = ROOT / ".planning/traceability/requirement-source-map.yaml"
    manifest_path = ROOT / ".planning/traceability/pack-v3-file-manifest.json"
    try:
        source_map = load_yaml(map_path)
        manifest = load_json(manifest_path)
    except ValueError as exc:
        return [f"ERROR TRC001: {exc}"]
    source_path = source_map.get("sourcePack")
    entries = {entry.get("path"): entry.get("sha256") for entry in manifest.get("files", []) if isinstance(entry, dict)}
    if not isinstance(source_path, str):
        return ["ERROR TRC002: requirement source map lacks sourcePack"]
    requirements = source_map.get("requirements")
    if not isinstance(requirements, dict):
        return ["ERROR TRC003: requirement source map lacks requirements"]
    for requirement_id, paths in requirements.items():
        if not isinstance(paths, list):
            errors.append(f"ERROR TRC004: {requirement_id} mapping must be a list")
            continue
        for relative_path in paths:
            if not isinstance(relative_path, str):
                errors.append(f"ERROR TRC005: {requirement_id} has non-string source path")
                continue
            manifest_path_key = f"{source_path}/{relative_path}"
            expected_digest = entries.get(manifest_path_key)
            target = ROOT / manifest_path_key
            if expected_digest is None or not target.is_file():
                errors.append(f"ERROR TRC006: {requirement_id} does not resolve to manifest-pinned archive path {relative_path}")
                continue
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest != expected_digest:
                errors.append(f"ERROR TRC007: {requirement_id} archive digest mismatch {relative_path}")
    return errors


def validate_claims(claims: list[dict[str, Any]], source_ids: set[str], sources: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    _, id_errors = record_ids(claims, "CLM-")
    errors.extend(id_errors)
    for claim in claims:
        claim_id = claim.get("id", "<unknown>")
        links = claim.get("sourceRelations", [])
        if not isinstance(links, list):
            continue
        primary_ids: set[str] = set()
        independent_ids: set[str] = set()
        for link in links:
            if not isinstance(link, dict):
                continue
            source_id = link.get("sourceId")
            relation = link.get("relation")
            if source_id not in source_ids:
                errors.append(f"ERROR SEM003: {claim_id} references unknown source {source_id}")
                continue
            if relation not in RELATIONS:
                errors.append(f"ERROR SEM004: {claim_id} uses unsupported relation {relation}")
            source = sources[source_id]
            required_source = ("officialUrl", "repository", "commitSha", "path", "locator", "retrievedAt", "contentSha256", "authorityTier", "maturity")
            if any(not source.get(field) for field in required_source):
                errors.append(f"ERROR SEM005: {claim_id} references incomplete immutable source {source_id}")
            if link.get("role") == "primary":
                primary_ids.add(source_id)
            if link.get("role") == "independent-corroboration":
                independent_ids.add(source_id)
        if claim.get("state") == "verified":
            review = claim.get("review", {})
            if not isinstance(review, dict) or not review.get("approvedBy") or not review.get("approvedAt"):
                errors.append(f"ERROR SEM006: {claim_id} cannot be verified without reviewer approval evidence")
        if claim.get("blocking") is True:
            if not primary_ids or not independent_ids or primary_ids & independent_ids:
                errors.append(f"ERROR SEM007: blocking {claim_id} requires distinct primary and independent corroborating sources")
    return errors


def load_optional_records(
    root: Path,
    filename: str,
    key: str,
    schema: str,
    expected_schema_version: int | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    path = root / filename
    if not path.exists():
        return [], []
    document = load_yaml(path)
    errors: list[str] = []
    if expected_schema_version is not None and document.get("schemaVersion") != expected_schema_version:
        errors.append(f"ERROR MIG004: {filename} must use schemaVersion {expected_schema_version}; migrate legacy records first")
    records = document.get(key, [])
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        return [], [*errors, f"ERROR IO002: {filename} {key} must be a list of records"]
    return records, [*errors, *schema_errors(root / "schemas" / schema, records)]


def validate_drift(records: list[dict[str, Any]], source_ids: set[str], claim_ids: set[str]) -> list[str]:
    """Keep upstream comparison sides separate from observed-local records."""
    errors: list[str] = []
    for record in records:
        record_id = record.get("id", "<unknown>")
        normative = record.get("normative")
        observed = record.get("observed")
        if normative is None:
            if record.get("status") != "blocked" or not isinstance(observed, dict) or observed.get("classification") != "observed-local":
                errors.append(f"ERROR SEM008: {record_id} local evidence requires blocked observed-local form")
                continue
            prohibited_authority = {"claimId", "sourceId", "commitSha", "path", "locator", "contentSha256", "authorityTier", "maturity", "evidenceClass"}
            if prohibited_authority & observed.keys():
                errors.append(f"ERROR SEM009: {record_id} observed-local evidence must not carry normative authority fields")
            continue
        if not isinstance(normative, dict) or not isinstance(observed, dict):
            errors.append(f"ERROR SEM008: {record_id} requires two complete upstream sides or observed-local form")
            continue
        for side in (normative, observed):
            if side.get("sourceId") not in source_ids:
                errors.append(f"ERROR SEM008: {record_id} references unknown source {side.get('sourceId')}")
            if side.get("claimId") not in claim_ids:
                errors.append(f"ERROR SEM009: {record_id} references unknown claim {side.get('claimId')}")
        identity_fields = ("claimId", "sourceId", "commitSha", "path", "contentSha256")
        if all(normative.get(field) == observed.get(field) for field in identity_fields):
            errors.append(f"ERROR SEM010: {record_id} upstream normative and observed sides must be distinct")
    return errors


def validate_compatibility(records: list[dict[str, Any]], source_index: dict[str, dict[str, Any]], known_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for record in records:
        record_id = record.get("id", "<unknown>")
        for field in ("packages", "runtimes", "examples", "fixtures", "knownDrift", "testEvidence"):
            for reference in record.get(field, []):
                if reference not in known_ids:
                    errors.append(f"ERROR SEM010: {record_id} references unknown {field} ID {reference}")
        for pin in [*record.get("sourceBaseline", []), record.get("releaseState", {}), record.get("currentWork", {})]:
            if not isinstance(pin, dict):
                continue
            source = source_index.get(pin.get("sourceId"))
            if source is None:
                errors.append(f"ERROR SEM011: {record_id} references unknown baseline source {pin.get('sourceId')}")
            elif any(pin.get(key) != source.get(key) for key in ("commitSha", "path", "contentSha256")):
                errors.append(f"ERROR SEM012: {record_id} baseline conflicts with source {pin.get('sourceId')} commitSha/path/contentSha256")
    return errors


def report_text(source_records: list[dict[str, Any]], claim_records: list[dict[str, Any]], errors: list[str]) -> str:
    lines = ["# Research Validation Report", "", "This deterministic report records structural and semantic checks; it does not grant human approval.", "", "## Result", "", f"- Status: {'invalid' if errors else 'valid'}", "- Traceability mappings: " + ("invalid" if any(error.startswith("ERROR TRC") for error in errors) else "valid"), "", "## Source records", ""]
    for record in sorted(source_records, key=lambda item: item.get("id", "")):
        lines.append(f"- {record.get('id', '<missing>')}: {'valid' if not errors else 'review required'}")
    lines.extend(["", "## Claim records", ""])
    for record in sorted(claim_records, key=lambda item: item.get("id", "")):
        lines.append(f"- {record.get('id', '<missing>')}: {record.get('state', 'unknown')}")
    if errors:
        lines.extend(["", "## Diagnostics", "", *[f"- {error}" for error in errors]])
    return "\n".join(lines) + "\n"


def validate_spike(directory: Path, mode: str) -> list[str]:
    """Validate one disposable SPK envelope without executing its command."""
    errors: list[str] = []
    try:
        metadata = load_yaml(directory / "metadata.yaml")
    except ValueError as exc:
        return [f"ERROR SPK001: {exc}"]

    errors.extend(schema_errors(ROOT / ".planning/research/schemas/spike.schema.json", [metadata]))
    expected_directory = str(metadata.get("id", "")).lower()
    if directory.name != expected_directory or directory.parent.name != "spikes" or directory.parent.parent.name != ".planning":
        errors.append("ERROR SPK002: spike directory must be .planning/spikes/spk-*/ and match its SPK ID")

    bindings = metadata.get("sourceBindings", [])
    enriched_bindings = [binding for binding in bindings if isinstance(binding, dict) and any(key in binding for key in ("claimId", "primitive", "expectedClassification", "immutable"))]
    if enriched_bindings:
        try:
            source_document = load_yaml(ROOT / ".planning/research/source-registry.yaml")
            claim_document = load_yaml(ROOT / ".planning/research/claims.yaml")
            sources = {record.get("id"): record for record in source_document.get("sources", []) if isinstance(record, dict)}
            claims = {record.get("id"): record for record in claim_document.get("claims", []) if isinstance(record, dict)}
        except ValueError as exc:
            errors.append(f"ERROR SPK011: cannot resolve enriched source bindings: {exc}")
            sources, claims = {}, {}
        immutable_fields = ("commitSha", "path", "locator", "contentSha256", "retrievedAt", "authorityTier", "evidenceClass", "maturity")
        for binding in enriched_bindings:
            primitive = binding.get("primitive", "<unknown>")
            source_id = binding.get("sourceId")
            claim_id = binding.get("claimId")
            source = sources.get(source_id)
            if source is None:
                errors.append(f"ERROR SPK012: {primitive} references unknown source {source_id}")
                continue
            if claim_id not in claims:
                errors.append(f"ERROR SPK013: {primitive} references unknown claim {claim_id}")
            immutable = binding.get("immutable")
            if not isinstance(immutable, dict) or any(immutable.get(field) != source.get(field) for field in immutable_fields):
                errors.append(f"ERROR SPK014: {primitive} immutable binding does not match source {source_id}")
            if binding.get("expectedClassification") == "blocked" and claims.get(claim_id, {}).get("state") != "blocked":
                errors.append(f"ERROR SPK015: {primitive} marked blocked must resolve to a blocked claim")
    if mode == "contract":
        return errors

    required_complete = ("environmentFacts", "measurements", "rawOutputDigests", "replayResult", "evidenceLinks")
    for field in required_complete:
        if not metadata.get(field):
            errors.append(f"ERROR SPK003: completed spike requires {field}")
    errors.extend(validate_complete_spike_evidence(metadata, directory))
    manifest_name = metadata.get("environmentManifest")
    environment: dict[str, Any] = {}
    if isinstance(manifest_name, str):
        try:
            environment = load_json(directory / manifest_name)
            errors.extend(schema_errors(ROOT / ".planning/research/schemas/environment.schema.json", [environment]))
        except ValueError as exc:
            errors.append(f"ERROR SPK004: completed spike requires valid environment facts: {exc}")

    browser_run = bool(environment.get("browsers")) or "browser" in metadata.get("environmentFacts", {})
    for measurement in metadata.get("measurements", []):
        if not isinstance(measurement, dict):
            continue
        values = measurement.get("rawValues", [])
        if measurement.get("nondeterministic") is True or browser_run:
            if not isinstance(values, list) or len(values) != 5:
                errors.append("ERROR SPK005: browser or nondeterministic measurement requires exactly five rawValues")
                continue
            if not all(isinstance(value, (int, float)) for value in values):
                errors.append("ERROR SPK006: rawValues must be numeric")
                continue
            observed_range = measurement.get("range")
            if observed_range != {"min": min(values), "max": max(values)}:
                errors.append("ERROR SPK007: measurement range must equal the rawValues minimum and maximum")
            ordered = sorted(values)
            observed_median = (ordered[2] if len(ordered) % 2 else (ordered[len(ordered) // 2 - 1] + ordered[len(ordered) // 2]) / 2)
            if measurement.get("median") != observed_median:
                errors.append("ERROR SPK008: measurement median must equal the rawValues median")
    if metadata.get("status") == "blocked":
        blocked = metadata.get("blocked")
        if not isinstance(blocked, dict) or not blocked.get("reason") or not blocked.get("affectedRequirements") or not blocked.get("affectedAdrs"):
            errors.append("ERROR SPK009: blocked spike retains reason, affected requirements, and affected ADRs")
        result = metadata.get("replayResult")
        if isinstance(result, dict) and result.get("status") != "blocked":
            errors.append("ERROR SPK010: blocked spike requires a blocked local replay result")
    return errors


REPORT_CONTRACT = ROOT / ".planning/research/schemas/report-contract.yaml"


def report_contract() -> dict[str, Any]:
    return load_yaml(REPORT_CONTRACT)


def validate_report(path: Path, planning_root: Path | None = None) -> list[str]:
    """Check only H2 headings and, for spikes, the declared metadata identity."""
    errors: list[str] = []
    try:
        contract = report_contract()
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        return [f"ERROR RPT001: cannot read report contract or report: {exc}"]
    headings = re.findall(r"^## (.+?)\s*$", text, flags=re.MULTILINE)
    required = contract.get("canonicalHeadings", [])
    if headings != required:
        for index, heading in enumerate(required):
            if index >= len(headings) or headings[index] != heading:
                errors.append(f"ERROR RPT002: required H2 heading {heading!r} is missing, duplicated, or out of order")
                break
        if len(headings) > len(required):
            errors.append("ERROR RPT003: report has non-canonical or duplicate H2 headings")
    if path.name == "report.md" and path.parent.name.startswith("spk-"):
        match = re.search(r"^SPK ID:\s*(SPK-[A-Z0-9][A-Z0-9-]*)\s*$", text, flags=re.MULTILINE)
        metadata_path = re.search(r"^Metadata path:\s*(.+?)\s*$", text, flags=re.MULTILINE)
        if match is None or metadata_path is None or metadata_path.group(1) != "metadata.yaml":
            errors.append("ERROR RPT004: spike report requires SPK ID and Metadata path: metadata.yaml declarations")
        else:
            try:
                metadata = load_yaml(path.parent / metadata_path.group(1))
                if metadata.get("id") != match.group(1) or path.parent.name != match.group(1).lower():
                    errors.append("ERROR RPT005: spike report SPK ID, metadata ID, and directory must match")
                errors.extend(validate_spike(path.parent, "complete"))
            except ValueError as exc:
                errors.append(f"ERROR RPT006: spike metadata does not resolve: {exc}")
    return errors


def validate_reports(planning_root: Path) -> list[str]:
    try:
        contract = report_contract()
    except ValueError as exc:
        return [f"ERROR RPT007: cannot load report contract: {exc}"]
    errors: list[str] = []
    discovery = contract.get("reportDiscovery", {})
    for pattern in discovery.get("researchPatterns", []):
        for path in sorted(planning_root.glob(pattern)):
            errors.extend(validate_report(path, planning_root))
    spike_pattern = discovery.get("spikePattern")
    if isinstance(spike_pattern, str):
        for path in sorted(planning_root.glob(spike_pattern)):
            errors.extend(validate_report(path, planning_root))
    return errors


def validate_governance(path: Path) -> list[str]:
    try:
        record = load_yaml(path)
    except ValueError as exc:
        return [f"ERROR GOV001: {exc}"]
    errors = schema_errors(ROOT / ".planning/research/schemas/phase-governance.schema.json", [record])
    approval = record.get("approval", {})
    if record.get("phaseResult") == "passed" and isinstance(approval, dict) and approval.get("status") != "approved":
        errors.append("ERROR GOV002: a passed phase result requires separate dated human approval; validation alone is insufficient")
    if record.get("owner") == record.get("requiredApprover"):
        errors.append("ERROR GOV003: responsible owner and required approver must be separate roles")
    return errors


def validate_lessons(index: Path, required_present: int) -> list[str]:
    try:
        document = load_yaml(index)
    except ValueError as exc:
        return [f"ERROR LES001: {exc}"]
    lessons = document.get("lessons")
    if not isinstance(lessons, list) or not all(isinstance(item, dict) for item in lessons):
        return ["ERROR LES002: lesson index requires a lessons record list"]
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_filenames: set[str] = set()
    present = 0
    for lesson in lessons:
        lesson_id = lesson.get("id")
        filename = lesson.get("filename")
        status = lesson.get("status", "present")
        if not isinstance(lesson_id, str) or not re.fullmatch(r"LES-\d{3}", lesson_id):
            errors.append("ERROR LES003: lesson index requires canonical LES-* ID")
            continue
        if lesson_id in seen_ids:
            errors.append(f"ERROR LES004: duplicate lesson ID {lesson_id}")
        seen_ids.add(lesson_id)
        if not isinstance(filename, str) or Path(filename).name != filename or not filename.endswith(".md"):
            errors.append(f"ERROR LES005: filename for {lesson_id} must be a local Markdown filename")
            continue
        if filename in seen_filenames:
            errors.append(f"ERROR LES005: duplicate lesson filename {filename}")
        seen_filenames.add(filename)
        if status not in {"present", "planned"}:
            errors.append(f"ERROR LES006: lesson {lesson_id} status must be present or planned")
            continue
        if status == "present":
            present += 1
            if not (index.parent / "packets" / filename).is_file() and not (index.parent / filename).is_file():
                errors.append(f"ERROR LES007: present lesson file is missing: {filename}")
    if present != required_present:
        errors.append(f"ERROR LES008: required-present {required_present} does not equal {present} indexed present packets")
    return errors


def validate_migration(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"ERROR MIG001: cannot read migration notes: {exc}"]
    changes = re.findall(r"^Version:\s*(\d+)\s*->\s*(\d+)\s*$", text, flags=re.MULTILINE)
    if not changes:
        return []
    errors: list[str] = []
    for old, new in changes:
        if int(new) <= int(old):
            errors.append("ERROR MIG002: breaking schema evolution requires an incremented version")
    for label in ("Schema:", "Deterministic migration:", "Fixtures:", "Change notes:", "Rollback:"):
        if label not in text:
            errors.append(f"ERROR MIG003: breaking schema evolution requires {label}")
    return errors


def validate_adr(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"ERROR ADR001: cannot read ADR: {exc}"]
    errors: list[str] = []
    required_labels = ("Status: proposed", "Evidence IDs:", "Uncertainty:", "Impacts:", "Alternatives:", "Required approver:", "Revisit trigger:")
    for label in required_labels:
        if label not in text:
            errors.append(f"ERROR ADR002: ADR requires {label}")
    evidence = re.findall(r"SRC-[A-Z0-9][A-Z0-9-]*", text)
    if not evidence:
        errors.append("ERROR ADR003: ADR requires at least one canonical immutable source ID")
        return errors
    try:
        registry = load_yaml(ROOT / ".planning/research/source-registry.yaml")
        sources = {item.get("id"): item for item in registry.get("sources", []) if isinstance(item, dict)}
        for source_id in evidence:
            source = sources.get(source_id)
            if not isinstance(source, dict):
                errors.append(f"ERROR ADR004: ADR evidence ID does not resolve: {source_id}")
            elif any(not source.get(field) for field in ("commitSha", "path", "contentSha256", "immutableUrl")):
                errors.append(f"ERROR ADR005: ADR evidence ID lacks immutable source fields: {source_id}")
    except ValueError as exc:
        errors.append(f"ERROR ADR006: immutable source registry cannot be resolved: {exc}")
    return errors


def validate_impact_fragment(path: Path, planning_root: Path) -> list[str]:
    """Validate immutable spike links through canonical planning-root paths only."""
    try:
        fragment = load_yaml(path)
    except ValueError as exc:
        return [f"ERROR IMP001: {exc}"]
    errors = [error.replace("ERROR SCH", "ERROR IMP") for error in schema_errors(ROOT / ".planning/research/schemas/spike-impact-fragment.schema.json", [fragment])]
    spike_id = fragment.get("spikeId")
    expected_directory = str(spike_id).lower()
    spike_prefix = f"spikes/{expected_directory}/"

    def resolve_link(value: Any, label: str, expected: str | None = None, spike_local: bool = False) -> Path | None:
        try:
            candidate = resolve_canonical_file(planning_root, value, expected)
        except ValueError as exc:
            errors.append(f"ERROR IMP002: {label} is not canonical: {exc}")
            return None
        if spike_local and not isinstance(value, str):
            errors.append(f"ERROR IMP003: {label} must be spike-local")
            return None
        if spike_local and not value.startswith(spike_prefix):
            errors.append("ERROR IMP003: fragment identity must match the SPK metadata and report directory")
            return None
        return candidate

    metadata_file = resolve_link(fragment.get("metadataPath"), "metadata path", f"{spike_prefix}metadata.yaml")
    report_file = resolve_link(fragment.get("reportPath"), "report path", f"{spike_prefix}report.md")
    if metadata_file is not None:
        try:
            metadata = load_yaml(metadata_file)
            if metadata.get("id") != spike_id:
                errors.append("ERROR IMP004: fragment spikeId does not match metadata ID")
        except ValueError as exc:
            errors.append(f"ERROR IMP005: metadata link does not resolve: {exc}")
        if fragment.get("metadataSha256") != hashlib.sha256(metadata_file.read_bytes()).hexdigest():
            errors.append("ERROR IMP006: metadata path has an altered SHA-256")
    if report_file is not None and fragment.get("reportSha256") != hashlib.sha256(report_file.read_bytes()).hexdigest():
        errors.append("ERROR IMP008: report path has an altered SHA-256")

    registry_relative = "research/source-registry.yaml"
    source_registry = resolve_link(registry_relative, "source registry", registry_relative)
    source_index: dict[str, dict[str, Any]] = {}
    registry_digest = ""
    if source_registry is not None:
        registry_digest = hashlib.sha256(source_registry.read_bytes()).hexdigest()
        try:
            source_document = load_yaml(source_registry)
            source_index = {item.get("id"): item for item in source_document.get("sources", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
        except ValueError as exc:
            errors.append(f"ERROR IMP009: source registry does not resolve: {exc}")
    immutable_source_fields = ("id", "kind", "collectionStatus", "rawOrigin", "repository", "officialUrl", "immutableUrl", "ref", "commitSha", "path", "locator", "contentSha256", "retrievedAt", "authorityTier", "evidenceClass", "maturity", "uncertainty", "impacts", "freshness", "review")
    for link in fragment.get("sourceLinks", []):
        if not isinstance(link, dict):
            continue
        source_file = resolve_link(link.get("path"), "source link", registry_relative)
        source_id = link.get("sourceId")
        source = source_index.get(source_id)
        if source is None:
            errors.append(f"ERROR IMP010: dangling source link {source_id}")
        elif any(not source.get(field) for field in immutable_source_fields):
            errors.append(f"ERROR IMP010: incomplete immutable source record {source_id}")
        if source_file is not None and link.get("sha256") != registry_digest:
            errors.append("ERROR IMP011: source registry digest does not match declared link digest")

    for link in fragment.get("measurementLinks", []):
        if not isinstance(link, dict):
            continue
        measurement_file = resolve_link(link.get("path"), "measurement link", spike_local=True)
        if measurement_file is not None and link.get("sha256") != hashlib.sha256(measurement_file.read_bytes()).hexdigest():
            errors.append("ERROR IMP012: measurement path has an altered SHA-256")
    expected_patterns = {"requirement": r"^[A-Z][A-Z0-9]{3,4}-\d{2}$", "adr": r"^ADR-\d{4}$", "phase": r"^\d{2}$", "lesson": r"^LES-\d{3}$"}
    for impact in fragment.get("proposedImpacts", []):
        if isinstance(impact, dict) and not re.fullmatch(expected_patterns.get(impact.get("type"), r"$^"), str(impact.get("id", ""))):
            errors.append("ERROR IMP013: proposed impact type and canonical ID do not match")

    declared_source_ids = set(fragment.get("sourceIds", []))
    linked_source_ids = {link.get("sourceId") for link in fragment.get("sourceLinks", []) if isinstance(link, dict)}
    if fragment.get("fragmentId"):
        if declared_source_ids != linked_source_ids:
            errors.append("ERROR IMP014: sourceIds must exactly match typed sourceLinks")
        evidence_kinds = {link.get("kind") for link in fragment.get("evidenceLinks", []) if isinstance(link, dict)}
        if any(kind not in evidence_kinds for kind in ("source", "metadata", "measurement", "report")):
            errors.append("ERROR IMP015: evidenceLinks must include source, metadata, measurement, and report provenance")
        expected_evidence = {"source": registry_relative, "metadata": f"{spike_prefix}metadata.yaml", "measurement": fragment.get("measurementPath"), "report": f"{spike_prefix}report.md"}
        for link in fragment.get("evidenceLinks", []):
            if not isinstance(link, dict):
                continue
            kind = link.get("kind")
            expected = expected_evidence.get(kind)
            evidence_file = resolve_link(link.get("path"), "evidence link", expected, spike_local=kind in {"metadata", "measurement", "report"})
            if evidence_file is not None and link.get("sha256") != hashlib.sha256(evidence_file.read_bytes()).hexdigest():
                errors.append("ERROR IMP016: evidence link path has an altered SHA-256")
        try:
            claims_document = load_yaml(resolve_canonical_file(planning_root, "research/claims.yaml", "research/claims.yaml"))
            claims = {item.get("id"): item for item in claims_document.get("claims", []) if isinstance(item, dict)}
        except ValueError as exc:
            claims = {}
            errors.append(f"ERROR IMP017: claims registry does not resolve: {exc}")
        for source_id in declared_source_ids:
            if not any(isinstance(claim, dict) and any(isinstance(relation, dict) and relation.get("sourceId") == source_id for relation in claim.get("sourceRelations", [])) for claim in claims.values()):
                errors.append(f"ERROR IMP018: source {source_id} has no canonical claim provenance")
    if str(spike_id).startswith("SPK-H-"):
        proposal = fragment.get("securityEgressFindingProposal")
        if not isinstance(proposal, dict) or not proposal.get("id") or not proposal.get("owner") or not proposal.get("requiredApproval"):
            errors.append("ERROR IMP020: SPK-H requires securityEgress and complete output provenance")
    return errors


SPIKE_REPORTS = {
    "SPK-A": "spk-a-workspace",
    "SPK-B": "spk-b-static-framework",
    "SPK-C": "spk-c-boundary-harness",
    "SPK-D": "spk-d-verified-loader",
    "SPK-E": "spk-e-content-rendering",
    "SPK-F": "spk-f-course-workbench",
    "SPK-G": "spk-g-package-conformance",
    "SPK-H": "spk-h-browser-egress",
    "SPK-I": "spk-i-diagram-motion",
    "SPK-J": "spk-j-code-editing",
    "SPK-K": "spk-k-deployment",
    "SPK-L": "spk-l-source-freshness",
}
CONSOLIDATION_AT = "2026-07-24T00:00:00Z"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_retained_evidence(spike_directory: Path, relative_path: Any, expected_digest: Any) -> tuple[bytes, str]:
    """Resolve one declared retained output without allowing path authority."""
    if not isinstance(relative_path, str) or not relative_path or "\x00" in relative_path:
        raise ValueError("retained evidence path must be a nonempty string without NUL")
    if not isinstance(expected_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_digest):
        raise ValueError("retained evidence digest must be an exact lowercase SHA-256")
    if relative_path.startswith("/") or "\\" in relative_path:
        raise ValueError("retained evidence path must use a relative POSIX path")
    parts = relative_path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("retained evidence path must be normalized and remain below the spike directory")
    base = spike_directory.resolve(strict=True)
    candidate = spike_directory.joinpath(*parts)
    current = spike_directory
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("retained evidence must not traverse a symlink")
    try:
        resolved = candidate.resolve(strict=True)
        mode = candidate.stat(follow_symlinks=False).st_mode
    except OSError as exc:
        raise ValueError(f"retained evidence path cannot be resolved: {exc}") from exc
    if not resolved.is_relative_to(base) or not stat.S_ISREG(mode):
        raise ValueError("retained evidence must be a confined regular file")
    content = candidate.read_bytes()
    observed_digest = hashlib.sha256(content).hexdigest()
    if observed_digest != expected_digest:
        raise ValueError("retained evidence SHA-256 does not match declared digest")
    return content, observed_digest


def validate_complete_spike_evidence(metadata: dict[str, Any], spike_directory: Path) -> list[str]:
    """Bind completed-spike evidence and replay output to retained local bytes."""
    errors: list[str] = []
    outputs = metadata.get("rawOutputDigests")
    if not isinstance(outputs, list) or not outputs:
        return ["ERROR SPK016: completed spike requires retained raw output declarations"]
    resolved_outputs: dict[str, str] = {}
    for output in outputs:
        if not isinstance(output, dict):
            errors.append("ERROR SPK017: retained output declaration must be an object")
            continue
        path = output.get("path")
        digest = output.get("sha256")
        if path in resolved_outputs:
            errors.append("ERROR SPK018: duplicate normalized retained output path")
            continue
        try:
            _, observed_digest = resolve_retained_evidence(spike_directory, path, digest)
        except ValueError as exc:
            errors.append(f"ERROR SPK019: {exc}")
            continue
        resolved_outputs[path] = observed_digest

    links = metadata.get("evidenceLinks")
    if not isinstance(links, list) or not links:
        errors.append("ERROR SPK020: completed spike requires typed evidence links")
    else:
        for link in links:
            if not isinstance(link, dict):
                errors.append("ERROR SPK021: typed evidence link must be an object")
                continue
            path = link.get("path")
            digest = link.get("sha256")
            kind = link.get("kind")
            if kind == "source" and path == "../../research/source-registry.yaml":
                # This is a canonical source-binding reference, not a retained spike output.
                source_registry = ROOT / ".planning/research/source-registry.yaml"
                if not source_registry.is_file() or source_registry.is_symlink() or sha256(source_registry) != digest:
                    errors.append("ERROR SPK022: canonical source evidence does not match its declared digest")
                continue
            try:
                _, observed_digest = resolve_retained_evidence(spike_directory, path, digest)
            except ValueError as exc:
                errors.append(f"ERROR SPK023: typed evidence link is invalid: {exc}")
                continue

    replay = metadata.get("replayResult")
    output_digest = replay.get("outputDigest") if isinstance(replay, dict) else None
    if output_digest not in set(resolved_outputs.values()):
        errors.append("ERROR SPK025: replay result digest must bind one validated retained output")
    return errors


def normalized_fragment(fragment: dict[str, Any]) -> str:
    return json.dumps(normalize_yaml(fragment), sort_keys=True, separators=(",", ":"))


def yaml_bytes(document: dict[str, Any]) -> bytes:
    return yaml.safe_dump(document, sort_keys=False, allow_unicode=True).encode("utf-8")


def acquire_consolidation_lock(research: Path, timeout: float) -> tuple[Any | None, str | None]:
    lock_name = hashlib.sha256(str(research.resolve()).encode("utf-8")).hexdigest()[:20]
    handle = open(Path(tempfile.gettempdir()) / f"learn-napplets-consolidation-{lock_name}.lock", "a+", encoding="utf-8")
    deadline = time.monotonic() + timeout
    while True:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return handle, None
        except BlockingIOError:
            if time.monotonic() >= deadline:
                handle.close()
                return None, "CONSOLIDATION_LOCK_CONFLICT: timed out waiting for the exclusive consolidation lock"
            time.sleep(0.01)


def release_consolidation_lock(handle: Any) -> None:
    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    handle.close()


def fragment_source_claim_errors(fragment: dict[str, Any], planning_root: Path) -> list[str]:
    """Validate that every fragment source has a metadata claim-to-source path."""
    errors: list[str] = []
    metadata_path = planning_root / str(fragment["metadataPath"])
    metadata = load_yaml(metadata_path)
    claims = load_yaml(planning_root / "research/claims.yaml").get("claims", [])
    claim_index = {item.get("id"): item for item in claims if isinstance(item, dict)}
    for source_id in fragment.get("sourceIds", []):
        bindings = [item for item in metadata.get("sourceBindings", []) if isinstance(item, dict) and item.get("sourceId") == source_id]
        bound_claims = [claim_index.get(binding.get("claimId")) for binding in bindings]
        canonical_claims = [claim for claim in claim_index.values() if isinstance(claim, dict) and any(isinstance(link, dict) and link.get("sourceId") == source_id for link in claim.get("sourceRelations", []))]
        if not canonical_claims:
            errors.append(f"ERROR IMP018: source {source_id} has no canonical claim provenance")
        if bound_claims and not any(isinstance(claim, dict) and any(isinstance(link, dict) and link.get("sourceId") == source_id for link in claim.get("sourceRelations", [])) for claim in bound_claims):
            errors.append(f"ERROR IMP019: metadata claim provenance does not transitively resolve {source_id}")
    return errors


def discover_consolidation_inputs(spikes: Path, planning_root: Path, input_order: str) -> tuple[list[tuple[Path, dict[str, Any]]], list[str], list[tuple[str, Path, str]]]:
    errors: list[str] = []
    reports: list[tuple[str, Path, str]] = []
    for short_id, directory in SPIKE_REPORTS.items():
        report = spikes / directory / "report.md"
        if not report.is_file():
            errors.append(f"ERROR CONS001: missing required {short_id} report at {report}")
        else:
            reports.append((short_id, report, sha256(report)))
    paths = sorted(spikes.glob("spk-*/impact-fragment*.yaml"))
    if input_order == "reverse":
        paths.reverse()
    fragments: list[tuple[Path, dict[str, Any]]] = []
    for path in paths:
        fragment_errors = validate_impact_fragment(path, planning_root)
        try:
            fragment = load_yaml(path)
        except ValueError as exc:
            errors.append(f"ERROR CONS002: {exc}")
            continue
        errors.extend(fragment_errors)
        errors.extend(fragment_source_claim_errors(fragment, planning_root))
        fragments.append((path, fragment))
    return fragments, sorted(set(errors)), reports


def merge_fragment_history(document: dict[str, Any], key: str, fragment: dict[str, Any], prefix: str) -> None:
    marker = f"{fragment['fragmentId']} fragment SHA-256 {fragment['_digest']}"
    proposals = [item for item in fragment.get(prefix, []) if isinstance(item, dict)]
    proposal_ids = {item.get("id") for item in proposals}
    for record in document.get(key, []):
        if not isinstance(record, dict) or record.get("id") not in proposal_ids:
            continue
        history = record.get("history", [])
        if any(isinstance(item, dict) and marker in str(item.get("reason", "")) for item in history):
            continue
        rationale = next((item.get("rationale", "") for item in proposals if item.get("id") == record.get("id")), "")
        history.append({"at": CONSOLIDATION_AT, "state": record.get("status", "blocked"), "reason": f"Consolidated {marker}; {rationale}"})
        record["history"] = history


def new_drift_record(fragment: dict[str, Any], drift_id: str, claims: dict[str, dict[str, Any]], sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source_id = fragment["sourceIds"][0]
    source = sources[source_id]
    claim_id = next((item.get("id") for item in claims.values() if isinstance(item, dict) and any(isinstance(link, dict) and link.get("sourceId") == source_id for link in item.get("sourceRelations", []))), "CLM-UPSTREAM-BASELINE-001")
    side = {
        "claimId": claim_id,
        "sourceId": source_id,
        "commitSha": source["commitSha"],
        "path": source["path"],
        "locator": source["locator"],
        "contentSha256": source["contentSha256"],
        "statement": "Consolidated local spike observation is retained as a blocked project-evidence hand-off, not an upstream fact.",
        "authorityTier": source["authorityTier"],
        "maturity": source["maturity"],
        "evidenceClass": source["evidenceClass"],
    }
    return {
        "id": drift_id,
        "kind": "drift",
        "topic": drift_id.removeprefix("DRF-").lower().replace("-", " "),
        "status": "blocked",
        "statusReason": f"Consolidated {fragment['fragmentId']} retains a local blocked or uncertain observation without asserting upstream behavior.",
        "normative": side,
        "observed": side.copy(),
        "impacts": {"content": ["LES-001"], "code": [fragment["spikeId"]], "knowledge": ["spike-consolidation"], "requirements": sorted(fragment["affectedRequirements"]), "phases": sorted(fragment["affectedPhases"])},
        "uncertainty": fragment["uncertainty"],
        "history": [{"at": CONSOLIDATION_AT, "state": "blocked", "reason": f"Consolidated {fragment['fragmentId']} fragment SHA-256 {fragment['_digest']}."}],
        "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical", "security"]},
        "dependentDecisionDisposition": {"decisionIds": sorted(item["id"] for item in fragment["proposedImpacts"] if item.get("type") == "adr") or ["ADR-0005"], "disposition": "blocked", "safeFallback": "Keep the deterministic static fallback.", "revisitTrigger": "Collect immutable source evidence and obtain required review."},
    }


def merge_fragments(research: Path, fragments: list[tuple[Path, dict[str, Any]]]) -> tuple[dict[str, dict[str, Any]], list[tuple[str, str]], list[str]]:
    documents = {name: load_yaml(research / name) for name in ("compatibility-matrix.yaml", "drift-register.yaml", "open-questions.yaml")}
    sources = {item.get("id"): item for item in load_yaml(research / "source-registry.yaml").get("sources", []) if isinstance(item, dict)}
    claims = {item.get("id"): item for item in load_yaml(research / "claims.yaml").get("claims", []) if isinstance(item, dict)}
    outcomes: list[tuple[str, str]] = []
    conflicts: list[str] = []
    seen: dict[str, str] = {}
    accepted: list[dict[str, Any]] = []
    for path, fragment in sorted(fragments, key=lambda item: (item[1].get("fragmentId", ""), str(item[0]))):
        digest = sha256(path)
        fragment = copy_fragment = dict(fragment)
        copy_fragment["_digest"] = digest
        stable_id = str(fragment.get("fragmentId", fragment.get("id")))
        payload = normalized_fragment(fragment)
        previous = seen.get(stable_id)
        if previous is not None:
            if previous != payload:
                conflicts.append(f"OQ-CONSOLIDATION-{stable_id}")
                outcomes.append((stable_id, "blocked-conflict"))
            else:
                outcomes.append((stable_id, "no-op-duplicate"))
            continue
        seen[stable_id] = payload
        accepted.append(copy_fragment)
        outcomes.append((stable_id, "merged"))
    if conflicts:
        return documents, outcomes, sorted(set(conflicts))
    drift_records = documents["drift-register.yaml"].setdefault("drift", [])
    drift_index = {record.get("id"): record for record in drift_records if isinstance(record, dict)}
    questions = documents["open-questions.yaml"].setdefault("questions", [])
    question_index = {record.get("id"): record for record in questions if isinstance(record, dict)}
    compatibility = documents["compatibility-matrix.yaml"].get("compatibility", [])
    for fragment in accepted:
        for drift_proposal in fragment.get("proposedDriftRecords", []):
            if not isinstance(drift_proposal, dict):
                continue
            drift_id = drift_proposal["id"]
            if drift_id not in drift_index:
                record = new_drift_record(fragment, drift_id, claims, sources)
                drift_records.append(record)
                drift_index[drift_id] = record
        merge_fragment_history(documents["drift-register.yaml"], "drift", fragment, "proposedDriftRecords")
        for question in fragment.get("proposedOpenQuestions", []):
            question_id = question["id"]
            marker = f"{fragment['fragmentId']} fragment SHA-256 {fragment['_digest']}"
            if question_id in question_index:
                history = question_index[question_id].setdefault("history", [])
                if not any(marker in str(item.get("reason", "")) for item in history if isinstance(item, dict)):
                    history.append({"at": CONSOLIDATION_AT, "status": "blocked", "reason": f"Consolidated {marker}; {question['rationale']}"})
                continue
            linked_drift = sorted(item["id"] for item in fragment.get("proposedDriftRecords", []) if isinstance(item, dict))
            question_index[question_id] = {
                "id": question_id,
                "kind": "open-question",
                "question": question["rationale"],
                "status": "blocked",
                "sourceRefs": sorted(set(fragment["sourceIds"] + linked_drift)),
                "impacts": {"requirements": sorted(fragment["affectedRequirements"]), "phases": sorted(fragment["affectedPhases"])},
                "blockedDecisions": sorted(item["id"] for item in fragment["proposedImpacts"] if item.get("type") == "adr") or ["ADR-0005"],
                "resolutionCriteria": ["Collect complete immutable source and claim provenance, then obtain the required review."],
                "owner": "research-owner",
                "review": {"status": "pending", "requiredRoles": ["protocol-technical", "security"]},
                "history": [{"at": CONSOLIDATION_AT, "status": "blocked", "reason": f"Consolidated {marker}; {question['rationale']}"}],
            }
            questions.append(question_index[question_id])
        for record in compatibility:
            if not isinstance(record, dict):
                continue
            known_drift = record.setdefault("knownDrift", [])
            for drift_proposal in fragment.get("proposedDriftRecords", []):
                if not isinstance(drift_proposal, dict):
                    continue
                drift_id = drift_proposal["id"]
                if drift_id not in known_drift:
                    known_drift.append(drift_id)
            record["knownDrift"] = sorted(known_drift)
    drift_records.sort(key=lambda item: item.get("id", ""))
    questions.sort(key=lambda item: item.get("id", ""))
    return documents, outcomes, []


def record_conflict_questions(
    documents: dict[str, dict[str, Any]],
    fragments: list[tuple[Path, dict[str, Any]]],
    conflicts: list[str],
) -> None:
    """Publish deterministic review work while leaving incompatible targets untouched."""
    questions = documents["open-questions.yaml"].setdefault("questions", [])
    question_index = {record.get("id"): record for record in questions if isinstance(record, dict)}
    for conflict_id in conflicts:
        fragment_id = conflict_id.removeprefix("OQ-CONSOLIDATION-")
        candidates = sorted(
            ((path, fragment) for path, fragment in fragments if fragment.get("fragmentId", fragment.get("id")) == fragment_id),
            key=lambda item: (sha256(item[0]), str(item[0])),
        )
        digests = [sha256(path) for path, _ in candidates]
        source_refs = sorted(
            {
                reference
                for _, fragment in candidates
                for reference in [*fragment.get("sourceIds", []), *(item.get("id") for item in fragment.get("proposedDriftRecords", []) if isinstance(item, dict))]
            }
        )
        requirements = sorted({item for _, fragment in candidates for item in fragment.get("affectedRequirements", [])})
        phases = sorted({item for _, fragment in candidates for item in fragment.get("affectedPhases", [])})
        decisions = sorted(
            {
                item.get("id")
                for _, fragment in candidates
                for item in fragment.get("proposedImpacts", [])
                if isinstance(item, dict) and item.get("type") == "adr"
            }
        )
        history = [
            {
                "at": CONSOLIDATION_AT,
                "status": "blocked",
                "reason": f"Incompatible {fragment_id} immutable proposal SHA-256 {digest}; retain both payloads for human review.",
            }
            for digest in digests
        ]
        existing = question_index.get(conflict_id)
        if isinstance(existing, dict):
            existing_history = existing.setdefault("history", [])
            for entry in history:
                if not any(isinstance(item, dict) and entry["reason"] == item.get("reason") for item in existing_history):
                    existing_history.append(entry)
            continue
        record = {
            "id": conflict_id,
            "kind": "open-question",
            "question": f"Which immutable {fragment_id} payload, if any, may be consolidated after review of the incompatible evidence?",
            "status": "blocked",
            "sourceRefs": source_refs,
            "impacts": {"requirements": requirements, "phases": phases},
            "blockedDecisions": decisions or ["ADR-0005"],
            "resolutionCriteria": ["Compare both retained immutable fragment SHA-256 values with their report, metadata, measurement, source, and claim provenance; then obtain the required review."],
            "owner": "research-owner",
            "review": {"status": "pending", "requiredRoles": ["protocol-technical", "security"]},
            "history": history,
        }
        questions.append(record)
        question_index[conflict_id] = record
    questions.sort(key=lambda item: item.get("id", ""))


def input_snapshot_digest(reports: list[tuple[str, Path, str]], fragments: list[tuple[Path, dict[str, Any]]]) -> str:
    """Return the deterministic rerun key for every immutable consolidation input."""
    inputs: list[tuple[str, str]] = []
    for _, report, digest in reports:
        directory = report.parent
        inputs.extend(
            (
                (str(report), digest),
                (str(directory / "metadata.yaml"), sha256(directory / "metadata.yaml")),
                (str(directory / "measurements.yaml"), sha256(directory / "measurements.yaml")),
            )
        )
    inputs.extend((str(path), sha256(path)) for path, _ in fragments)
    return hashlib.sha256(json.dumps(sorted(inputs), separators=(",", ":")).encode("utf-8")).hexdigest()


def security_egress_synthesis(fragment: dict[str, Any]) -> str:
    digest = fragment["_digest"]
    source_ids = ", ".join(fragment["sourceIds"])
    questions = "; ".join(item["id"] for item in fragment["proposedOpenQuestions"])
    proposal = fragment["securityEgressFindingProposal"]
    return f"""# Security and egress synthesis\n\n## Research question\n\nWhat does the validated SPK-H local fixture support without converting local browser behavior or project policy into an upstream protocol conclusion?\n\n## Sources and immutable revisions\n\n- Fragment: `{fragment['fragmentId']}` SHA-256 `{digest}`.\n- Report: `{fragment['reportPath']}` SHA-256 `{fragment['reportSha256']}`.\n- Metadata: `{fragment['metadataPath']}` SHA-256 `{fragment['metadataSha256']}`.\n- Measurement: `{fragment['measurementPath']}` SHA-256 `{fragment['measurementSha256']}`.\n- Canonical source and claim provenance: {source_ids}; `CLM-UPSTREAM-BASELINE-001` and `CLM-POLICY-001`.\n\n## Observations\n\nNo current immutable upstream egress statement was collected. The source and claim records document that absence as blocked project evidence, not upstream browser or protocol proof.\n\n**Browser observations:** the exact opaque-origin `srcdoc` guest with `sandbox=allow-scripts` only produced five bounded Chromium local-loopback observations. Firefox exited before Playwright attached, so no Firefox channel or CSP behavior was observed. These are fixture observations only.\n\n## Conflicts\n\n`DRF-EGRESS-001` and `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` retain the distinct local observation, missing Firefox attachment, and unresolved upstream question. No conflict is silently resolved by this synthesis.\n\n## Inference\n\nThe supported inference is limited to the named local fixture, browser version, sandbox tokens, CSP inputs, and loopback endpoints. It does not select a production host profile or establish upstream egress behavior.\n\n## Prototype or measurement\n\nSPK-H records five bounded Chromium measurements plus an explicit Firefox pre-attachment blocked result. The local replay validates the referenced digest-pinned report, metadata, and measurement only; it does not test an external endpoint or production CSP.\n\n## Recommendation\n\n**Proposed project policy:** `{proposal['id']}` proposes a restrictive, reviewable public-site CSP only after named security and protocol review. It is not an upstream NIP requirement or cross-browser conclusion.\n\n## Uncertainty\n\n**Unresolved questions:** {questions} remain blocked pending immutable upstream evidence and, for Firefox, attached-context measurements under the approved toolchain. {fragment['uncertainty']['reason']}\n\n## Affected phases and requirements\n\n- Requirements: `EVID-04`, `OPER-03`.\n- Phases: 01 evidence baseline, 02 product/content contract, 03 static-site foundation, and 05 teaching-host work.\n- Impact: do not authorize a host profile, external egress, or browser-support conclusion; preserve deterministic static fallback and the Firefox blocker.\n\n## Owner and required approval\n\nOwner: `{proposal['owner']}`. Required approval: {proposal['requiredApproval']} Revisit trigger: {proposal.get('revisitTrigger', 'Collect immutable evidence and review it.')}\n"""


def replay_manifest(spikes: Path, reports: list[tuple[str, Path, str]]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for short_id, report, report_digest in reports:
        directory = report.parent
        metadata = directory / "metadata.yaml"
        measurement = directory / "measurements.yaml"
        evidence = [{"path": str(report.relative_to(spikes.parent)), "sha256": report_digest}, {"path": str(metadata.relative_to(spikes.parent)), "sha256": sha256(metadata)}]
        if measurement.is_file():
            evidence.append({"path": str(measurement.relative_to(spikes.parent)), "sha256": sha256(measurement)})
        entries.append({"spikeId": short_id, "report": evidence[0], "metadata": evidence[1], "measurement": evidence[2] if len(evidence) == 3 else None, "fixtureEvidence": evidence, "replayCommand": f"tools/phase1-python tools/validate-research.py validate-spike .planning/{str(directory.relative_to(spikes.parent))} --complete", "applicability": "local-only; retain blocked result when declared browser or upstream baseline is unavailable", "freshnessThreshold": "recheck when any pinned input digest changes", "requiredOutcome": "validated complete spike or explicit blocked disposition"})
    return {"schemaVersion": 1, "kind": "spike-replay-manifest", "entries": entries}


def consolidation_audit(reports: list[tuple[str, Path, str]], fragments: list[tuple[Path, dict[str, Any]]], outcomes: list[tuple[str, str]], conflicts: list[str], manifest_digest: str) -> str:
    rerun_digest = input_snapshot_digest(reports, fragments)
    lines = ["# Spike Consolidation Audit", "", "This deterministic audit records immutable inputs and serialized outcomes; it does not accept an ADR or promote a local observation into an upstream fact.", "", "## Immutable input snapshot", "", "| Spike | Report | Metadata | Measurement | Fragment |", "| --- | --- | --- | --- | --- |"]
    for short_id, report, digest in reports:
        directory = report.parent
        metadata = directory / "metadata.yaml"
        measurement = directory / "measurements.yaml"
        local_fragments = sorted(
            ((path, value) for path, value in fragments if value.get("spikeId", "").startswith(short_id + "-")),
            key=lambda item: (item[1].get("fragmentId", item[1].get("id", "")), str(item[0])),
        )
        fragment_text = ", ".join(f"`{path.relative_to(report.parents[2])}` SHA-256 `{sha256(path)}`" for path, _ in local_fragments) or "no-impact-fragment"
        lines.append(
            f"| {short_id} | `{report.relative_to(report.parents[2])}` SHA-256 `{digest}` | "
            f"`{metadata.relative_to(report.parents[2])}` SHA-256 `{sha256(metadata)}` | "
            f"`{measurement.relative_to(report.parents[2])}` SHA-256 `{sha256(measurement)}` | {fragment_text} |"
        )
    lines.extend(["", "## Serialized outcomes", "", "| Stable ID | Disposition |", "| --- | --- |"])
    for stable_id, outcome in sorted(outcomes):
        lines.append(f"| {stable_id} | {outcome} |")
    for conflict in conflicts:
        lines.append(f"| {conflict} | blocked-conflict; deterministic review work retains both immutable fragment payloads |")
    lines.extend(["", "## Blocked and uncertain outcomes", ""])
    for _, fragment in sorted(fragments, key=lambda item: item[1].get("fragmentId", item[1].get("id", ""))):
        proposed_questions = ", ".join(item["id"] for item in fragment.get("proposedOpenQuestions", []) if isinstance(item, dict)) or "none"
        lines.append(f"- `{fragment.get('fragmentId', fragment.get('id'))}`: uncertainty `{fragment['uncertainty']['state']}` — {fragment['uncertainty']['reason']} Open questions: {proposed_questions}.")
    lines.extend(["", "## Transaction", "", "- Exclusive `fcntl.flock` lock acquired before immutable snapshot and staging.", "- Canonical targets: compatibility-matrix.yaml, drift-register.yaml, open-questions.yaml, security-egress-findings.md, replay-manifest.yaml.", "- Blocked and uncertain dispositions remain blocked; no report prose becomes an asserted upstream fact.", f"- Replay manifest SHA-256: `{manifest_digest}`.", f"- Rerun input digest: `{rerun_digest}`; identical validated inputs produce byte-identical staged outputs.", ""])
    return "\n".join(lines)


def expected_replay_argv(spike_id: str, planning_root: Path) -> list[str]:
    """Return the only approved replay argv for a stable spike ID."""
    try:
        directory = SPIKE_REPORTS[spike_id]
    except KeyError as exc:
        raise ValueError(f"unknown replay spike ID {spike_id}") from exc
    # The wrapper runs from repository root; YAML supplies no executable or arguments.
    return ["tools/phase1-python", "tools/validate-research.py", "validate-spike", f".planning/spikes/{directory}", "--complete"]


def validate_replay_manifest(path: Path, planning_root: Path) -> list[str]:
    try:
        manifest = load_yaml(path)
    except ValueError as exc:
        return [f"ERROR RPL001: {exc}"]
    entries = manifest.get("entries", [])
    if not isinstance(entries, list) or len(entries) != len(SPIKE_REPORTS):
        return ["ERROR RPL002: manifest must account for SPK-A through SPK-L"]
    errors: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("spikeId"), str) or entry["spikeId"] in seen:
            errors.append("ERROR RPL003: entries require unique stable spike IDs")
            continue
        spike_id = entry["spikeId"]
        seen.add(spike_id)
        directory = SPIKE_REPORTS.get(spike_id)
        if directory is None:
            errors.append("ERROR RPL006: manifest IDs must be SPK-A through SPK-L")
            continue
        expected_paths = {
            "report": f"spikes/{directory}/report.md",
            "metadata": f"spikes/{directory}/metadata.yaml",
            "measurement": f"spikes/{directory}/measurements.yaml",
        }
        expected_evidence: list[tuple[str, str]] = []
        for label, expected_path in expected_paths.items():
            evidence = entry.get(label)
            if not isinstance(evidence, dict) or evidence.get("path") != expected_path:
                errors.append(f"ERROR RPL004: {spike_id} {label} must use its mapped retained path")
                continue
            try:
                _, digest = resolve_retained_evidence(planning_root, evidence.get("path"), evidence.get("sha256"))
            except ValueError as exc:
                errors.append(f"ERROR RPL005: {spike_id} {label} is invalid: {exc}")
                continue
            expected_evidence.append((expected_path, digest))
        fixture_evidence = entry.get("fixtureEvidence")
        actual_evidence = [(item.get("path"), item.get("sha256")) for item in fixture_evidence] if isinstance(fixture_evidence, list) and all(isinstance(item, dict) for item in fixture_evidence) else []
        if actual_evidence != expected_evidence:
            errors.append(f"ERROR RPL007: {spike_id} fixture evidence must exactly bind mapped retained files")
        legacy_command = entry.get("replayCommand")
        if legacy_command is not None and legacy_command != " ".join(expected_replay_argv(spike_id, planning_root)):
            errors.append(f"ERROR RPL008: {spike_id} manifest command text is not the fixed rendered argv")
    if seen != set(SPIKE_REPORTS):
        errors.append("ERROR RPL006: manifest IDs must be SPK-A through SPK-L")
    return errors


def replay_spikes(manifest_path: Path, planning_root: Path) -> list[str]:
    """Validate retained replay inputs and execute only stable-ID-derived argv."""
    errors = validate_replay_manifest(manifest_path, planning_root)
    if errors:
        return errors
    try:
        manifest = load_yaml(manifest_path)
    except ValueError as exc:
        return [f"ERROR RPL001: {exc}"]
    entries = manifest.get("entries", [])
    for entry in sorted(entries, key=lambda item: str(item.get("spikeId", "")) if isinstance(item, dict) else ""):
        if not isinstance(entry, dict):
            errors.append("ERROR RPL009: replay manifest entry must be an object")
            continue
        spike_id = entry.get("spikeId")
        try:
            argv = expected_replay_argv(spike_id, planning_root)
            result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, check=False)
        except (OSError, ValueError) as exc:
            errors.append(f"ERROR RPL010: {spike_id} replay could not start: {exc}")
            continue
        if result.returncode:
            detail = (result.stdout or result.stderr).strip().replace("\n", " | ")
            errors.append(f"ERROR RPL011: {spike_id} replay failed: {detail or 'non-zero exit'}")
    return errors


def consolidate_spike_impacts(spikes: Path, research: Path, audit: Path, dry_run: bool, timeout: float, input_order: str) -> list[str]:
    planning_root = spikes.parent
    lock, lock_error = acquire_consolidation_lock(research, timeout)
    if lock_error:
        return [lock_error]
    try:
        hold_seconds = float(os.environ.get("CONSOLIDATION_TEST_HOLD_LOCK_SECONDS", "0"))
        if hold_seconds > 0:
            time.sleep(hold_seconds)
        fragments, errors, reports = discover_consolidation_inputs(spikes, planning_root, input_order)
        if errors:
            return errors
        documents, outcomes, conflicts = merge_fragments(research, fragments)
        if conflicts:
            record_conflict_questions(documents, fragments, conflicts)
        h_fragment = next((fragment for _, fragment in fragments if fragment.get("spikeId") == "SPK-H-BROWSER-EGRESS"), None)
        if h_fragment is None:
            return ["ERROR CONS004: SPK-H fragment is required before security/egress synthesis"]
        h_fragment = dict(h_fragment)
        h_fragment["_digest"] = sha256(next(path for path, fragment in fragments if fragment.get("spikeId") == "SPK-H-BROWSER-EGRESS"))
        security = security_egress_synthesis(h_fragment)
        manifest = replay_manifest(spikes, reports)
        manifest_bytes = yaml_bytes(manifest)
        audit_text = consolidation_audit(reports, fragments, outcomes, conflicts, hashlib.sha256(manifest_bytes).hexdigest())
        conflict_errors = [f"ERROR CONS003: incompatible stable fragment proposal requires {item}" for item in conflicts]
        if dry_run:
            audit.parent.mkdir(parents=True, exist_ok=True)
            audit.write_text(audit_text, encoding="utf-8")
            return conflict_errors
        stage = Path(tempfile.mkdtemp(prefix=".spike-consolidation-", dir=research))
        targets = {
            research / "compatibility-matrix.yaml": yaml_bytes(documents["compatibility-matrix.yaml"]),
            research / "drift-register.yaml": yaml_bytes(documents["drift-register.yaml"]),
            research / "open-questions.yaml": yaml_bytes(documents["open-questions.yaml"]),
            research / "security-egress-findings.md": security.encode("utf-8"),
            audit: audit_text.encode("utf-8"),
            spikes / "replay-manifest.yaml": manifest_bytes,
        }
        staged: dict[Path, Path] = {}
        for index, (target, content) in enumerate(targets.items()):
            staged_path = stage / f"{index:02d}-{target.name}"
            staged_path.write_bytes(content)
            staged[target] = staged_path
        staged_documents = {name: load_yaml(staged[research / name]) for name in ("compatibility-matrix.yaml", "drift-register.yaml", "open-questions.yaml")}
        validation_errors = schema_errors(research / "schemas/compatibility.schema.json", staged_documents["compatibility-matrix.yaml"].get("compatibility", []))
        validation_errors += schema_errors(research / "schemas/drift.schema.json", staged_documents["drift-register.yaml"].get("drift", []))
        validation_errors += schema_errors(research / "schemas/open-question.schema.json", staged_documents["open-questions.yaml"].get("questions", []))
        validation_errors += validate_replay_manifest(staged[spikes / "replay-manifest.yaml"], planning_root)
        if validation_errors:
            shutil.rmtree(stage, ignore_errors=True)
            return validation_errors
        if conflicts:
            # Conflict review writes only its open-question record; compatibility and
            # drift documents were not merged and must retain their exact bytes.
            for target in (research / "compatibility-matrix.yaml", research / "drift-register.yaml"):
                staged.pop(target)
        if os.environ.get("CONSOLIDATION_INJECT_PRECOMMIT_FAILURE") == "1":
            shutil.rmtree(stage, ignore_errors=True)
            return ["CONSOLIDATION_INJECTED_FAILURE: staged transaction rolled back before publication"]
        originals = {target: target.read_bytes() if target.exists() else None for target in staged}
        try:
            for target, staged_path in staged.items():
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(staged_path, target)
        except OSError as exc:
            for target, original in originals.items():
                if original is None:
                    target.unlink(missing_ok=True)
                else:
                    target.write_bytes(original)
            return [f"ERROR CONS005: publication failed and prior canonical state was restored: {exc}"]
        finally:
            shutil.rmtree(stage, ignore_errors=True)
        return conflict_errors
    finally:
        release_consolidation_lock(lock)


def main() -> int:
    parser = argparse.ArgumentParser()
    command = parser.add_subparsers(dest="command", required=True)
    validate = command.add_parser("validate")
    validate.add_argument("--root", type=Path, required=True)
    validate.add_argument("--report", type=Path, required=True)
    spike = command.add_parser("validate-spike")
    spike.add_argument("directory", type=Path)
    spike_mode = spike.add_mutually_exclusive_group(required=True)
    spike_mode.add_argument("--contract", action="store_true")
    spike_mode.add_argument("--complete", action="store_true")
    governance = command.add_parser("validate-governance")
    governance.add_argument("path", type=Path)
    report = command.add_parser("validate-report")
    report.add_argument("path", type=Path)
    reports = command.add_parser("validate-reports")
    reports.add_argument("--root", type=Path, required=True)
    lessons = command.add_parser("validate-lessons")
    lessons.add_argument("--index", type=Path, required=True)
    lessons.add_argument("--required-present", type=int, required=True)
    adr = command.add_parser("validate-adr")
    adr.add_argument("path", type=Path)
    migration = command.add_parser("validate-migration")
    migration.add_argument("path", type=Path)
    fragment = command.add_parser("validate-impact-fragment")
    fragment.add_argument("path", type=Path)
    fragment.add_argument("--root", type=Path, required=True)
    consolidate = command.add_parser("consolidate-spike-impacts")
    consolidate.add_argument("--spikes", type=Path, required=True)
    consolidate.add_argument("--research", type=Path, required=True)
    consolidate.add_argument("--audit", type=Path, required=True)
    consolidate.add_argument("--dry-run", action="store_true")
    consolidate.add_argument("--lock-timeout", type=float, default=2.0)
    consolidate.add_argument("--input-order", choices=("normal", "reverse"), default="normal")
    replay = command.add_parser("replay-spikes")
    replay.add_argument("--manifest", type=Path, required=True)
    replay.add_argument("--check", action="store_true")
    recovery = command.add_parser("recover-consolidation")
    recovery.add_argument("--research", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "validate-spike":
        errors = validate_spike(args.directory.resolve(), "contract" if args.contract else "complete")[:100]
    elif args.command == "validate-governance":
        errors = validate_governance(args.path)[:100]
    elif args.command == "validate-report":
        errors = validate_report(args.path)[:100]
    elif args.command == "validate-reports":
        errors = validate_reports(args.root)[:100]
    elif args.command == "validate-lessons":
        errors = validate_lessons(args.index, args.required_present)[:100]
    elif args.command == "validate-adr":
        errors = validate_adr(args.path)[:100]
    elif args.command == "validate-migration":
        errors = validate_migration(args.path)[:100]
    elif args.command == "validate-impact-fragment":
        errors = validate_impact_fragment(args.path, args.root)[:100]
    elif args.command == "consolidate-spike-impacts":
        errors = consolidate_spike_impacts(args.spikes, args.research, args.audit, args.dry_run, args.lock_timeout, args.input_order)[:100]
    elif args.command == "replay-spikes":
        errors = replay_spikes(args.manifest, args.manifest.parents[1])[:100] if args.check else []
    elif args.command == "recover-consolidation":
        try:
            canonical_recovery_module().recover_canonical_generation(args.research.resolve().parents[1])
            errors = []
        except Exception as exc:
            errors = [f"ERROR REC001: canonical recovery refused: {exc}"]
    else:
        errors = []
    if args.command != "validate":
        for error in errors:
            print(error)
        return 1 if errors else 0

    root = args.root
    errors: list[str] = []
    sources: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    try:
        if root.resolve() == (ROOT / ".planning/research").resolve():
            # The reviewed-acquisition check happens before the Plan 01-42 reader. From
            # this point onward compatibility families are consumed exclusively from one
            # registered immutable mapping; eligibility receives only its typed index.
            compatibility_index = validated_compatibility_snapshot_index(root)
            sources = [_thaw(record) for record in compatibility_index.sources.values()]
            claims = [_thaw(record) for record in compatibility_index.claims.values()]
            drift = [_thaw(record) for record in compatibility_index.drift.values()]
            questions = [_thaw(record) for record in compatibility_index.questions.values()]
            compatibility = [_thaw(record) for record in compatibility_index.compatibility]
            errors.extend(schema_errors(root / "schemas/source.schema.json", sources))
            source_ids, source_id_errors = record_ids(sources, "SRC-")
            errors.extend(source_id_errors)
            source_index = {record.get("id"): record for record in sources if isinstance(record.get("id"), str)}
            errors.extend(schema_errors(root / "schemas/claim.schema.json", claims))
            errors.extend(validate_claims(claims, source_ids, source_index))
            errors.extend(schema_errors(root / "schemas/drift.schema.json", drift))
            errors.extend(schema_errors(root / "schemas/open-question.schema.json", questions))
            errors.extend(schema_errors(root / "schemas/compatibility.schema.json", compatibility))
            claim_ids, claim_id_errors = record_ids(claims, "CLM-")
            drift_ids, drift_id_errors = record_ids(drift, "DRF-")
            question_ids, question_id_errors = record_ids(questions, "OQ-")
            compatibility_ids, compatibility_id_errors = record_ids(compatibility, "CMP-")
            errors.extend(claim_id_errors + drift_id_errors + question_id_errors + compatibility_id_errors)
            errors.extend(validate_drift(drift, source_ids, claim_ids))
            known_ids = source_ids | claim_ids | drift_ids | question_ids | compatibility_ids
            errors.extend(validate_compatibility(compatibility, source_index, known_ids))
            # A blocked substantive result is valid evidence; no approval or ADR state is
            # synthesized by validation. The returned ordered reasons remain in matrix data.
            evaluate_compatibility_baseline(compatibility_index)
        else:
            # Isolated source/claim fixtures predate the complete canonical snapshot
            # contract. They validate only their supplied records and never invoke the
            # repository-confined reviewed-acquisition preflight.
            source_document = load_yaml(root / "source-registry.yaml")
            sources = source_document.get("sources", [])
            if not isinstance(sources, list) or not all(isinstance(item, dict) for item in sources):
                raise ValueError("source-registry.yaml sources must be a list of records")
            errors.extend(schema_errors(root / "schemas/source.schema.json", sources))
            source_ids, source_id_errors = record_ids(sources, "SRC-")
            errors.extend(source_id_errors)
            source_index = {record.get("id"): record for record in sources if isinstance(record.get("id"), str)}
            claims_path = root / "claims.yaml"
            if claims_path.exists():
                claims_document = load_yaml(claims_path)
                claims = claims_document.get("claims", [])
                if not isinstance(claims, list) or not all(isinstance(item, dict) for item in claims):
                    raise ValueError("claims.yaml claims must be a list of records")
                errors.extend(schema_errors(root / "schemas/claim.schema.json", claims))
                errors.extend(validate_claims(claims, source_ids, source_index))
            drift, drift_errors = load_optional_records(root, "drift-register.yaml", "drift", "drift.schema.json", expected_schema_version=2)
            questions, question_errors = load_optional_records(root, "open-questions.yaml", "questions", "open-question.schema.json")
            compatibility, compatibility_errors = load_optional_records(root, "compatibility-matrix.yaml", "compatibility", "compatibility.schema.json", expected_schema_version=2)
            errors.extend(drift_errors + question_errors + compatibility_errors)
            claim_ids, claim_id_errors = record_ids(claims, "CLM-")
            drift_ids, drift_id_errors = record_ids(drift, "DRF-")
            question_ids, question_id_errors = record_ids(questions, "OQ-")
            compatibility_ids, compatibility_id_errors = record_ids(compatibility, "CMP-")
            errors.extend(claim_id_errors + drift_id_errors + question_id_errors + compatibility_id_errors)
            errors.extend(validate_drift(drift, source_ids, claim_ids))
            known_ids = source_ids | claim_ids | drift_ids | question_ids | compatibility_ids
            errors.extend(validate_compatibility(compatibility, source_index, known_ids))
        errors.extend(validate_reports(root.parent))
        migration_notes = root / "schemas/migration-notes.md"
        if migration_notes.exists():
            errors.extend(validate_migration(migration_notes))
        errors.extend(validate_traceability())
    except ValueError as exc:
        errors.append(f"ERROR IO001: {exc}")
    errors = errors[:100]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report_text(sources, claims, errors), encoding="utf-8")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
