#!/usr/bin/env python3
"""Prove SPK-H source-link semantic negatives fail before consolidation."""

from __future__ import annotations

import copy
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
SPIKE = Path(__file__).resolve().parent
FRAGMENT = SPIKE / "impact-fragment.yaml"
OUTPUT = Path("/tmp/spk-h-negative-fragments")


def write_fixture(name: str, value: dict) -> Path:
    path = OUTPUT / f"{name}.yaml"
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
    return path


def require_rejection(name: str, value: dict, expected_error: str) -> None:
    path = write_fixture(name, value)
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/validate-research.py"),
            "validate-impact-fragment",
            str(path),
            "--root",
            str(ROOT / ".planning"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode == 0 or expected_error not in completed.stdout:
        raise SystemExit(
            f"{name} was not rejected as expected; returncode={completed.returncode}; output={completed.stdout!r}"
        )
    print(f"PASS: {name} rejected with {expected_error}")


def main() -> int:
    fragment = yaml.safe_load(FRAGMENT.read_text(encoding="utf-8"))
    if not isinstance(fragment, dict):
        raise SystemExit("SPK-H fragment must be a mapping")
    shutil.rmtree(OUTPUT, ignore_errors=True)
    OUTPUT.mkdir(parents=True)

    missing = copy.deepcopy(fragment)
    missing["sourceLinks"] = []
    require_rejection("missing-source-link", missing, "ERROR IMP")

    altered = copy.deepcopy(fragment)
    altered["sourceLinks"][0]["sourceId"] = "SRC-NONEXISTENT-001"
    require_rejection("altered-source-id", altered, "ERROR IMP010")

    mismatched = copy.deepcopy(fragment)
    mismatched["sourceLinks"][0]["sha256"] = "0" * 64
    require_rejection("mismatched-source-digest", mismatched, "ERROR IMP011")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
