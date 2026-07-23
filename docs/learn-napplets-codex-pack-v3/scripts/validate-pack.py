#!/usr/bin/env python3
"""Validate the documentation pack before it becomes a project repository."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def validate_links() -> None:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                ERRORS.append(f"missing link: {path.relative_to(ROOT)} -> {target}")


def validate_manifest() -> None:
    pack_path = ROOT / "pack.json"
    try:
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        ERRORS.append(f"invalid pack.json: {exc}")
        return

    actual = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != "pack.json"
    )
    listed = sorted(pack.get("files", []))
    if actual != listed:
        missing = sorted(set(actual) - set(listed))
        extra = sorted(set(listed) - set(actual))
        ERRORS.append(f"pack.json mismatch; missing={missing}, extra={extra}")


def validate_phase_prompts() -> None:
    numbers: list[int] = []
    for path in (ROOT / "prompts").glob("*.md"):
        match = re.match(r"(\d{2})-PHASE-(\d+)-", path.name)
        if not match:
            ERRORS.append(f"unrecognized phase prompt name: {path.name}")
            continue
        prefix, phase = (int(match.group(1)), int(match.group(2)))
        if prefix != phase:
            ERRORS.append(f"phase prefix mismatch: {path.name}")
        numbers.append(phase)
    if sorted(numbers) != list(range(11)):
        ERRORS.append(f"expected phase prompts 0..10, found {sorted(numbers)}")


def validate_yaml_when_available() -> None:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        return
    for path in (ROOT / "templates").glob("*.yaml"):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            ERRORS.append(f"invalid YAML template {path.name}: {exc}")


def main() -> int:
    validate_links()
    validate_manifest()
    validate_phase_prompts()
    validate_yaml_when_available()
    if ERRORS:
        print("Pack validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("Pack validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
