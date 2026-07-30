#!/usr/bin/env python3
"""Deterministically migrate Phase 1 drift registers from v1 to v2."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml


IMPACT_KEYS = ("content", "code", "knowledge", "requirements", "phases")


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
    """Return a canonical v2 copy of a valid v1 or v2 drift document.

    The migration preserves every record, stable identifier, impact element, and
    history entry. Sorting is deliberately stable, so duplicate history entries
    remain duplicated and re-running the migration is byte deterministic.
    """
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


def yaml_bytes(document: dict[str, Any]) -> bytes:
    return yaml.safe_dump(document, sort_keys=False, allow_unicode=True).encode("utf-8")


def migrate_file(source: Path, output: Path) -> None:
    try:
        loaded = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load input: {exc}") from exc
    migrated = migrate_drift_v1_to_v2(loaded)
    content = yaml_bytes(migrated)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    migrate = commands.add_parser("migrate-drift")
    migrate.add_argument("--input", type=Path, required=True)
    migrate.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        migrate_file(args.input, args.output)
    except ValueError as exc:
        print(f"ERROR MIGRATE: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
