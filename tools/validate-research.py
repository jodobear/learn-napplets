#!/usr/bin/env python3
"""Validate Phase 1 canonical evidence records without changing review state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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
    try:
        fragment = load_yaml(path)
    except ValueError as exc:
        return [f"ERROR IMP001: {exc}"]
    errors = [error.replace("ERROR SCH", "ERROR IMP") for error in schema_errors(ROOT / ".planning/research/schemas/spike-impact-fragment.schema.json", [fragment])]
    spike_id = fragment.get("spikeId")
    expected_directory = str(spike_id).lower()
    metadata_path = fragment.get("metadataPath")
    report_path = fragment.get("reportPath")
    if not isinstance(metadata_path, str) or not isinstance(report_path, str):
        return errors + ["ERROR IMP002: fragment requires metadata and report paths"]
    metadata_file = planning_root / metadata_path
    report_file = planning_root / report_path
    if metadata_file.parent.name != expected_directory or report_file.parent.name != expected_directory:
        errors.append("ERROR IMP003: fragment identity must match the SPK metadata and report directory")
    try:
        metadata = load_yaml(metadata_file)
        if metadata.get("id") != spike_id:
            errors.append("ERROR IMP004: fragment spikeId does not match metadata ID")
    except ValueError as exc:
        errors.append(f"ERROR IMP005: metadata link does not resolve: {exc}")
    if metadata_file.is_file() and fragment.get("metadataSha256") != hashlib.sha256(metadata_file.read_bytes()).hexdigest():
        errors.append("ERROR IMP006: metadata path has an altered SHA-256")
    if not report_file.is_file():
        errors.append("ERROR IMP007: report link does not resolve")
    elif fragment.get("reportSha256") != hashlib.sha256(report_file.read_bytes()).hexdigest():
        errors.append("ERROR IMP008: report path has an altered SHA-256")
    source_registry = planning_root / "research/source-registry.yaml"
    try:
        source_document = load_yaml(source_registry)
        source_ids = {item.get("id") for item in source_document.get("sources", []) if isinstance(item, dict)}
    except ValueError as exc:
        source_ids = set()
        errors.append(f"ERROR IMP009: source registry does not resolve: {exc}")
    for link in fragment.get("sourceLinks", []):
        if not isinstance(link, dict):
            continue
        source_file = planning_root / str(link.get("path", ""))
        if link.get("sourceId") not in source_ids:
            errors.append(f"ERROR IMP010: dangling source link {link.get('sourceId')}")
        if not source_file.is_file():
            errors.append("ERROR IMP011: source path is missing or has an altered SHA-256")
        elif link.get("sha256") != hashlib.sha256(source_file.read_bytes()).hexdigest():
            errors.append("ERROR IMP011: source path is missing or has an altered SHA-256")
    for link in fragment.get("measurementLinks", []):
        if not isinstance(link, dict):
            continue
        measurement_file = planning_root / str(link.get("path", ""))
        if not measurement_file.is_file():
            errors.append("ERROR IMP012: measurement path is missing or has an altered SHA-256")
        elif link.get("sha256") != hashlib.sha256(measurement_file.read_bytes()).hexdigest():
            errors.append("ERROR IMP012: measurement path is missing or has an altered SHA-256")
    expected_patterns = {"requirement": r"^[A-Z][A-Z0-9]{3,4}-\d{2}$", "adr": r"^ADR-\d{4}$", "phase": r"^\d{2}$", "lesson": r"^LES-\d{3}$"}
    for impact in fragment.get("proposedImpacts", []):
        if isinstance(impact, dict) and not re.fullmatch(expected_patterns.get(impact.get("type"), r"$^"), str(impact.get("id", ""))):
            errors.append("ERROR IMP013: proposed impact type and canonical ID do not match")
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
