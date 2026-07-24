#!/usr/bin/env python3
"""Assemble and roll back the bounded local-only SPK-K fixture artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

SPIKE_ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = SPIKE_ROOT / ".experiment" / "local-artifacts"
FORBIDDEN_TOKENS = (
    "http://",
    "https://",
    "<script",
    "<form",
    "fetch(",
    "telemetry",
    "credential",
    "provider",
)
PAYLOADS = {
    "public-site-static": (
        "index.html",
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        "<title>SPK-K local-only fixture</title></head>"
        "<body><main><h1>Local static evidence only</h1>"
        "<p>This is not hosted, deployed, published, or a production release.</p>"
        "</main></body></html>\n",
    ),
    "lab-artifact-placeholder": (
        "README.md",
        "# Blocked lab artifact\n\n"
        "No teaching host, guest runtime, preview, deployment, or publication exists.\n",
    ),
    "portable-output-placeholder": (
        "README.md",
        "# Conditional portable output\n\n"
        "ADR-0007 remains unresolved; this is not packaged, hosted, or published.\n",
    ),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def safe_output_path(path: Path) -> Path:
    resolved = path.resolve()
    experiment_root = (SPIKE_ROOT / ".experiment").resolve()
    if resolved == experiment_root or experiment_root not in resolved.parents:
        raise ValueError("output path must remain below the SPK-K .experiment directory")
    return resolved


def assemble(fixture: Path, output: Path) -> dict[str, Any]:
    if not fixture.is_file():
        raise ValueError(f"fixture does not exist: {fixture}")

    shutil.rmtree(output, ignore_errors=True)
    output.mkdir(parents=True)
    fixture_digest = sha256_bytes(fixture.read_bytes())
    observations: list[dict[str, Any]] = []

    for artifact_id, (relative_name, content) in PAYLOADS.items():
        artifact_root = output / artifact_id
        artifact_root.mkdir()
        payload = artifact_root / relative_name
        payload.write_text(content, encoding="utf-8")
        payload_bytes = payload.read_bytes()
        payload_digest = sha256_bytes(payload_bytes)
        inspection_passed = all(token not in content.lower() for token in FORBIDDEN_TOKENS)
        isolation_passed = artifact_root.resolve().is_relative_to(output.resolve())
        manifest = {
            "artifactId": artifact_id,
            "files": [relative_name],
            "byteCount": len(payload_bytes),
            "payloadSha256": payload_digest,
            "fixtureSha256": fixture_digest,
            "localPreview": "not-hosted; static inspection only; no listener started",
            "isolation": isolation_passed,
            "rollback": "pending",
        }
        manifest_path = artifact_root / "artifact-manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        observations.append(
            {
                "artifactId": artifact_id,
                "payload": relative_name,
                "payloadBytes": len(payload_bytes),
                "payloadSha256": payload_digest,
                "manifestSha256": sha256_bytes(manifest_path.read_bytes()),
                "staticInspectionPassed": inspection_passed,
                "isolationPassed": isolation_passed,
                "localPreview": manifest["localPreview"],
            }
        )

    if not all(
        item["staticInspectionPassed"] and item["isolationPassed"]
        for item in observations
    ):
        raise ValueError("local static inspection or isolation check failed")
    return {"fixtureSha256": fixture_digest, "observations": observations}


def rollback(output: Path) -> dict[str, Any]:
    if not output.is_dir():
        raise ValueError(f"local artifact directory does not exist: {output}")

    records: list[dict[str, Any]] = []
    for artifact_root in sorted(path for path in output.iterdir() if path.is_dir()):
        manifest_path = artifact_root / "artifact-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        payload_path = artifact_root / manifest["files"][0]
        if sha256_bytes(payload_path.read_bytes()) != manifest["payloadSha256"]:
            raise ValueError(f"payload digest mismatch: {artifact_root.name}")
        records.append(
            {
                "artifactId": manifest["artifactId"],
                "payloadSha256": manifest["payloadSha256"],
                "manifestSha256": sha256_bytes(manifest_path.read_bytes()),
                "byteCount": manifest["byteCount"],
                "staticInspection": "passed",
                "isolation": "passed",
                "localPreview": manifest["localPreview"],
            }
        )

    replay_digest = sha256_bytes(
        json.dumps(records, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    shutil.rmtree(output)
    rollback_passed = not output.exists()
    if not rollback_passed:
        raise ValueError("local artifact rollback did not remove the output directory")
    return {
        "records": records,
        "replayDigest": replay_digest,
        "rollbackPassed": rollback_passed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()

    output = safe_output_path(args.out)
    result = rollback(output) if args.rollback else assemble(args.fixture.resolve(), output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
