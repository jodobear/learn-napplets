#!/usr/bin/env python3
"""Render one SPK-E fixture into six local, deterministic representations."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml


TARGETS = (
    ("static-html", "static.html"),
    ("guest-content", "guest-content.json"),
    ("markdown", "content.md"),
    ("glossary", "glossary.md"),
    ("transcript", "transcript.txt"),
    ("knowledge-json", "knowledge.json"),
)


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def render(fixture: dict[str, Any]) -> dict[str, str]:
    record = fixture["contentRecord"]
    fields = fixture["canonicalFieldValues"]
    parity = compact_json(fields)
    escaped_parity = html.escape(parity, quote=True)
    source = record["source"]
    claim = record["claim"]

    return {
        "static.html": "\n".join(
            (
                "<!doctype html>",
                '<html lang="en">',
                "<head><meta charset=\"utf-8\"><title>SPK-E static content</title></head>",
                "<body>",
                f'<article data-parity="{escaped_parity}">',
                f"<h1>{html.escape(record['title'])}</h1>",
                f"<p>{html.escape(record['summary'])}</p>",
                f"<p>{html.escape(record['statement'])}</p>",
                f"<dl><dt>Source</dt><dd>{html.escape(source['id'])}</dd><dt>Claim</dt><dd>{html.escape(claim['id'])}</dd></dl>",
                "</article>",
                "</body>",
                "</html>",
                "",
            )
        ),
        "guest-content.json": json.dumps(
            {
                "kind": "spk-e-guest-content",
                "canonicalFields": fields,
                "content": {"title": record["title"], "statement": record["statement"]},
                "nonProduction": True,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n",
        "content.md": "\n".join(
            (
                f"<!-- parity: {parity} -->",
                f"# {record['title']}",
                "",
                record["summary"],
                "",
                record["statement"],
                "",
                f"Source: `{source['id']}`. Claim: `{claim['id']}`.",
                "",
            )
        ),
        "glossary.md": "\n".join(
            (
                f"<!-- parity: {parity} -->",
                f"## {record['terminology']['term']}",
                "",
                record["glossaryDefinition"],
                "",
            )
        ),
        "transcript.txt": "\n".join(
            (
                f"PARITY {parity}",
                "SPK-E transcript",
                record["transcript"],
                f"Source {source['id']}; claim {claim['id']}.",
                "",
            )
        ),
        "knowledge.json": json.dumps(
            {
                "kind": "spk-e-knowledge-record",
                "canonicalFields": fields,
                "contentId": record["id"],
                "statement": record["statement"],
                "classification": record["classification"],
                "source": source,
                "claim": claim,
                "terminology": record["terminology"],
                "uncertainty": record["uncertainty"],
                "nonProduction": True,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n",
    }


def extract_parity(filename: str, content: str) -> dict[str, Any]:
    if filename == "static.html":
        match = re.search(r'data-parity="([^"]+)"', content)
        if not match:
            raise ValueError("static HTML lacks data-parity")
        return json.loads(html.unescape(match.group(1)))
    if filename in {"content.md", "glossary.md"}:
        match = re.match(r"<!-- parity: (.+) -->", content)
        if not match:
            raise ValueError(f"{filename} lacks parity comment")
        return json.loads(match.group(1))
    if filename == "transcript.txt":
        match = re.match(r"PARITY (.+)", content)
        if not match:
            raise ValueError("transcript lacks PARITY line")
        return json.loads(match.group(1))
    return json.loads(content)["canonicalFields"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    fixture = yaml.safe_load(args.fixture.read_text(encoding="utf-8"))
    if not isinstance(fixture, dict) or fixture.get("localOnly") is not True or fixture.get("nonProduction") is not True:
        raise ValueError("SPK-E fixture must be a local, non-production mapping")
    expected = fixture["canonicalFieldValues"]
    required = fixture["fieldParityContract"]["requiredFields"]
    if set(required) != set(expected):
        raise ValueError("field parity contract and canonical values differ")

    outputs = render(fixture)
    if tuple((target, filename) for target, filename in TARGETS) != tuple((entry["id"], entry["path"]) for entry in fixture["fieldParityContract"]["targetRepresentations"]):
        raise ValueError("fixture target declaration does not match renderer targets")

    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)
    digests: list[dict[str, str]] = []
    parity_results: list[dict[str, Any]] = []
    for target, filename in TARGETS:
        content = outputs[filename]
        actual = extract_parity(filename, content)
        if actual != expected:
            raise ValueError(f"{target} parity mismatch: {actual!r}")
        path = args.out / filename
        path.write_text(content, encoding="utf-8")
        digests.append({"target": target, "path": filename, "sha256": sha256_bytes(content.encode("utf-8"))})
        parity_results.append({"target": target, "result": "passed", "fields": actual})

    manifest = {
        "spikeId": fixture["spikeId"],
        "fixtureSha256": sha256_bytes(args.fixture.read_bytes()),
        "nonProduction": True,
        "outputDigests": digests,
        "fieldParity": parity_results,
        "result": "passed",
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
