#!/usr/bin/env python3
"""Validate Phase 1 canonical evidence records without changing review state."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = {"supports", "contradicts", "measures", "affects", "recommends", "supersedes"}


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


def load_optional_records(root: Path, filename: str, key: str, schema: str) -> tuple[list[dict[str, Any]], list[str]]:
    path = root / filename
    if not path.exists():
        return [], []
    document = load_yaml(path)
    records = document.get(key, [])
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        return [], [f"ERROR IO002: {filename} {key} must be a list of records"]
    return records, schema_errors(root / "schemas" / schema, records)


def validate_drift(records: list[dict[str, Any]], source_ids: set[str], claim_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for record in records:
        record_id = record.get("id", "<unknown>")
        for side in (record.get("normative", {}), record.get("observed", {})):
            if not isinstance(side, dict):
                continue
            if side.get("sourceId") not in source_ids:
                errors.append(f"ERROR SEM008: {record_id} references unknown source {side.get('sourceId')}")
            if side.get("claimId") not in claim_ids:
                errors.append(f"ERROR SEM009: {record_id} references unknown claim {side.get('claimId')}")
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
    if mode == "contract":
        return errors

    required_complete = ("environmentFacts", "measurements", "rawOutputDigests", "replayResult", "evidenceLinks")
    for field in required_complete:
        if not metadata.get(field):
            errors.append(f"ERROR SPK003: completed spike requires {field}")
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
    args = parser.parse_args()

    if args.command == "validate-spike":
        errors = validate_spike(args.directory.resolve(), "contract" if args.contract else "complete")[:100]
        for error in errors:
            print(error)
        return 1 if errors else 0

    root = args.root
    errors: list[str] = []
    sources: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    try:
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
        drift, drift_errors = load_optional_records(root, "drift-register.yaml", "drift", "drift.schema.json")
        questions, question_errors = load_optional_records(root, "open-questions.yaml", "questions", "open-question.schema.json")
        compatibility, compatibility_errors = load_optional_records(root, "compatibility-matrix.yaml", "compatibility", "compatibility.schema.json")
        errors.extend(drift_errors + question_errors + compatibility_errors)
        claim_ids, claim_id_errors = record_ids(claims, "CLM-")
        drift_ids, drift_id_errors = record_ids(drift, "DRF-")
        question_ids, question_id_errors = record_ids(questions, "OQ-")
        compatibility_ids, compatibility_id_errors = record_ids(compatibility, "CMP-")
        errors.extend(claim_id_errors + drift_id_errors + question_id_errors + compatibility_id_errors)
        errors.extend(validate_drift(drift, source_ids, claim_ids))
        known_ids = source_ids | claim_ids | drift_ids | question_ids | compatibility_ids
        errors.extend(validate_compatibility(compatibility, source_index, known_ids))
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
