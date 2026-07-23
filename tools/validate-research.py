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


def main() -> int:
    parser = argparse.ArgumentParser()
    command = parser.add_subparsers(dest="command", required=True)
    validate = command.add_parser("validate")
    validate.add_argument("--root", type=Path, required=True)
    validate.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
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
