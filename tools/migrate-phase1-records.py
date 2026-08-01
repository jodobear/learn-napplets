#!/usr/bin/env python3
"""Deterministically migrate Phase 1 drift and compatibility records."""

from __future__ import annotations

import argparse
import copy
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml


IMPACT_KEYS = ("content", "code", "knowledge", "requirements", "phases")
COMPATIBILITY_DIMENSIONS = (
    ("normativeProtocol", "sourceBaseline", "normative protocol evidence", "official normative authority", "No qualified immutable normative protocol source is retained."),
    ("observedImplementation", "sourceBaseline", "observed implementation evidence", "official repository observation", "No qualified observed implementation source is retained."),
    ("publishedPackage", "packages", "published registry artifact evidence", "independent package registry authority", "No independently retrieved published package artifact is retained."),
    ("runtime", "runtimes", "runtime behavior evidence", "independent runtime measurement authority", "No independent runtime evidence is retained."),
    ("exampleFixture", "examples", "example and fixture evidence", "reproducible fixture authority", "No independent example or fixture evidence is retained."),
    ("currentWork", "currentWork", "current-work source evidence", "official repository observation", "No qualified current-work source is retained."),
    ("conformance", "testEvidence", "conformance measurement evidence", "reproducible conformance authority", "No independent conformance evidence is retained."),
)


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _canonical_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("drift entries must be objects")
    _require_string(record.get("id"), "drift id")
    impacts = record.get("impacts")
    if not isinstance(impacts, dict):
        raise ValueError("drift impacts must be an object")
    for key in IMPACT_KEYS:
        values = impacts.get(key)
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise ValueError(f"drift impacts.{key} must be a string list")
        impacts[key] = sorted(values)
    history = record.get("history")
    if not isinstance(history, list) or not all(isinstance(item, dict) for item in history):
        raise ValueError("drift history must be an object list")
    for entry in history:
        for key in ("at", "state", "reason"):
            _require_string(entry.get(key), f"drift history.{key}")
    record["history"] = sorted(history, key=lambda entry: (entry["at"], entry["state"], entry["reason"]))
    return record


def _canonical_observation(observation: Any) -> dict[str, Any]:
    if not isinstance(observation, dict):
        raise ValueError("observedLocal entries must be objects")
    observation_id = _require_string(observation.get("id"), "observedLocal id")
    if not observation_id.startswith("OBS-"):
        raise ValueError("observedLocal ids must use the OBS- prefix")
    return observation


def migrate_drift_v1_to_v2(document: Any) -> dict[str, Any]:
    """Return a canonical v2 copy of a valid v1 or v2 drift document."""
    if not isinstance(document, dict):
        raise ValueError("drift document root must be an object")
    version = document.get("schemaVersion")
    if version not in (1, 2):
        raise ValueError("drift document schemaVersion must be 1 or 2")
    drift = document.get("drift")
    if not isinstance(drift, list):
        raise ValueError("drift document drift must be a list")
    migrated = dict(document)
    migrated["schemaVersion"] = 2
    migrated["drift"] = sorted((_canonical_record(dict(record)) for record in drift), key=lambda record: record["id"])
    if "observedLocal" in migrated:
        observations = migrated["observedLocal"]
        if not isinstance(observations, list):
            raise ValueError("observedLocal must be a list")
        migrated["observedLocal"] = sorted((_canonical_observation(dict(item)) for item in observations), key=lambda item: item["id"])
    return migrated


def _compatibility_pin(record: dict[str, Any]) -> dict[str, str]:
    pins = record.get("sourceBaseline")
    if not isinstance(pins, list) or not pins or not isinstance(pins[0], dict):
        raise ValueError("compatibility sourceBaseline must contain a pinned source")
    pin = pins[0]
    for key in ("sourceId", "commitSha", "path", "contentSha256"):
        _require_string(pin.get(key), f"compatibility sourceBaseline.{key}")
    return {key: pin[key] for key in ("sourceId", "commitSha", "path", "contentSha256")}


def _compatibility_references(record: dict[str, Any], field: str) -> None:
    value = record.get(field)
    if field in {"sourceBaseline", "currentWork"}:
        if field == "sourceBaseline":
            if not isinstance(value, list) or not value:
                raise ValueError("compatibility sourceBaseline must be a nonempty list")
        elif not isinstance(value, dict):
            raise ValueError("compatibility currentWork must be a pinned source")
        return
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"compatibility {field} must be a nonempty stable reference list")


def _dimension_reference(pin: dict[str, str]) -> dict[str, str]:
    return {
        "id": pin["sourceId"],
        "relation": "candidate",
        "locator": f"commit:{pin['commitSha']} path:{pin['path']}",
        "contentSha256": pin["contentSha256"],
    }


def _migrated_dimensions(record: dict[str, Any]) -> list[dict[str, Any]]:
    pin = _compatibility_pin(record)
    dimensions: list[dict[str, Any]] = []
    for name, source_field, evidence_expectation, authority_expectation, missing_reason in COMPATIBILITY_DIMENSIONS:
        _compatibility_references(record, source_field)
        dimensions.append({
            "name": name,
            "status": "blocked",
            "evidenceClassExpectation": evidence_expectation,
            "authorityExpectation": authority_expectation,
            "references": [_dimension_reference(pin)],
            "missingReason": missing_reason,
        })
    return dimensions


def migrate_compatibility_v1_to_v2(document: Any) -> dict[str, Any]:
    """Return a deterministic v2 compatibility document without evaluating eligibility.

    v1 records are copied losslessly before seven closed, blocked, not-reviewed
    dimension records are added. v2 documents are validated sufficiently to reject
    malformed input and then canonicalized without assigning eligibility or approval.
    """
    if not isinstance(document, dict):
        raise ValueError("compatibility document root must be an object")
    version = document.get("schemaVersion")
    if version not in (1, 2):
        raise ValueError("compatibility document schemaVersion must be 1 or 2")
    records = document.get("compatibility")
    if not isinstance(records, list) or not records or not all(isinstance(record, dict) for record in records):
        raise ValueError("compatibility document compatibility must be a nonempty object list")
    migrated = copy.deepcopy(document)
    migrated["schemaVersion"] = 2
    canonical: list[dict[str, Any]] = []
    for original in migrated["compatibility"]:
        record = dict(original)
        _require_string(record.get("id"), "compatibility id")
        _require_string(record.get("kind"), "compatibility kind")
        if record["kind"] != "compatibility":
            raise ValueError("compatibility kind must equal compatibility")
        if version == 1:
            record["dimensions"] = _migrated_dimensions(record)
        else:
            dimensions = record.get("dimensions")
            if not isinstance(dimensions, list) or [item.get("name") for item in dimensions if isinstance(item, dict)] != [item[0] for item in COMPATIBILITY_DIMENSIONS]:
                raise ValueError("compatibility v2 dimensions must be the closed ordered dimension set")
        canonical.append(record)
    migrated["compatibility"] = sorted(canonical, key=lambda record: record["id"])
    return migrated


def yaml_bytes(document: dict[str, Any]) -> bytes:
    return yaml.safe_dump(document, sort_keys=False, allow_unicode=True).encode("utf-8")


def compatibility_yaml_bytes(document: dict[str, Any]) -> bytes:
    return yaml_bytes(document)


def _load_document(source: Path) -> Any:
    try:
        return yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load input: {exc}") from exc


def _write_atomic(output: Path, content: bytes) -> None:
    output_parent = output.parent
    if not output_parent.is_dir():
        raise ValueError(f"output directory does not exist: {output_parent}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output_parent)
    try:
        with os.fdopen(descriptor, "wb") as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, output)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def migrate_file(source: Path, output: Path) -> None:
    _write_atomic(output, yaml_bytes(migrate_drift_v1_to_v2(_load_document(source))))


def migrate_compatibility_file(source: Path, output: Path) -> None:
    _write_atomic(output, compatibility_yaml_bytes(migrate_compatibility_v1_to_v2(_load_document(source))))


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    migrate_drift = commands.add_parser("migrate-drift")
    migrate_drift.add_argument("--input", type=Path, required=True)
    migrate_drift.add_argument("--output", type=Path, required=True)
    migrate_compatibility = commands.add_parser("migrate-compatibility")
    migrate_compatibility.add_argument("--input", type=Path, required=True)
    migrate_compatibility.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "migrate-drift":
            migrate_file(args.input, args.output)
        else:
            migrate_compatibility_file(args.input, args.output)
    except ValueError as exc:
        print(f"ERROR MIGRATE: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
