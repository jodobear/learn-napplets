#!/usr/bin/env python3
"""Compare immutable source observations and emit human review work only.

This command never changes source, claim, drift, question, or ADR records.  It writes a
review report whose stable work IDs let a reviewer compare repeated refreshes safely.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import stat
import time
from pathlib import Path
from typing import Any, Mapping

import yaml


REQUIRED_HEADINGS = (
    "Research question",
    "Sources and immutable revisions",
    "Observations",
    "Conflicts",
    "Inference",
    "Prototype or measurement",
    "Recommendation",
    "Uncertainty",
    "Affected phases and requirements",
    "Owner and required approval",
)
PIN_FIELDS = ("commitSha", "path", "contentSha256")
OUTCOMES = {"unchanged", "changed", "unavailable", "ambiguous"}
ROOT = Path(__file__).resolve().parents[1]


def _canonical_source_snapshot() -> Mapping[str, bytes]:
    spec = importlib.util.spec_from_file_location("canonical_recovery", ROOT / "tools" / "canonical-recovery.py")
    if spec is None or spec.loader is None:
        raise ValueError("canonical recovery module is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.read_canonical_snapshot(
        "source-acquisition",
        ("research/source-registry.yaml", "research/claims.yaml", "research/drift-register.yaml", "research/open-questions.yaml"),
        root=ROOT / ".planning",
    )


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def load_comparison(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError("comparison input must be a JSON array of objects")
    return [normalize_observation(item) for item in value]


def normalize_observation(observation: dict[str, Any]) -> dict[str, Any]:
    """Reject unsupported comparison fields and return canonical input bytes."""
    allowed = {"id", "outcome", *PIN_FIELDS}
    unknown = sorted(set(observation) - allowed)
    if unknown:
        raise ValueError(f"comparison observation has unsupported fields: {', '.join(unknown)}")
    source_id = observation.get("id")
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("comparison observation requires a source id")
    normalized: dict[str, Any] = {"id": source_id}
    requested = observation.get("outcome")
    if requested is not None:
        if not isinstance(requested, str) or requested not in OUTCOMES - {"unchanged", "changed"}:
            raise ValueError(f"unsupported explicit comparison outcome: {requested}")
        normalized["outcome"] = requested
    for field in PIN_FIELDS:
        value = observation.get(field)
        if value is not None:
            if not isinstance(value, str) or not value:
                raise ValueError(f"comparison observation {field} must be a nonempty string when supplied")
            normalized[field] = value
    if requested is None and any(field not in normalized for field in PIN_FIELDS):
        raise ValueError("comparison observation without an explicit outcome requires every immutable pin field")
    return normalized


def normalized_observation_bytes(observation: dict[str, Any]) -> bytes:
    return json.dumps(observation, sort_keys=True, separators=(",", ":")).encode("utf-8")


def reduce_observations(observations: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Produce exactly one deterministic review result for each source ID."""
    grouped: dict[str, dict[bytes, dict[str, Any]]] = {}
    for observation in observations:
        grouped.setdefault(observation["id"], {})[normalized_observation_bytes(observation)] = observation
    results: list[dict[str, Any]] = []
    for source_id in sorted(grouped):
        distinct = grouped[source_id]
        if len(distinct) == 1:
            results.append(compare(next(iter(distinct.values())), sources))
            continue
        observation_bytes = sorted(distinct)
        digests = [hashlib.sha256(value).hexdigest() for value in observation_bytes]
        source = sources.get(source_id, {})
        results.append(
            {
                "sourceId": source_id,
                "outcome": "ambiguous",
                "old": {field: source.get(field) for field in PIN_FIELDS},
                "observed": {"normalizedObservationDigests": digests},
                "normalizedObservationDigests": digests,
            }
        )
    return results


def related_ids(source_id: str, claims: list[dict[str, Any]], drift: list[dict[str, Any]], questions: list[dict[str, Any]]) -> list[str]:
    result: set[str] = set()
    for claim in claims:
        if any(link.get("sourceId") == source_id for link in claim.get("sourceRelations", []) if isinstance(link, dict)):
            result.add(str(claim.get("id")))
    for record in drift:
        sides = (record.get("normative"), record.get("observed"))
        if any(isinstance(side, dict) and side.get("sourceId") == source_id for side in sides):
            result.add(str(record.get("id")))
    for question in questions:
        if source_id in question.get("sourceRefs", []):
            result.add(str(question.get("id")))
    return sorted(item for item in result if item and item != "None")


def compare(observation: dict[str, Any], sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source_id = observation.get("id")
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("comparison observation requires a source id")
    requested = observation.get("outcome")
    if requested is not None:
        if requested not in OUTCOMES - {"unchanged", "changed"}:
            raise ValueError(f"unsupported explicit comparison outcome: {requested}")
        outcome = requested
    elif source_id not in sources:
        outcome = "ambiguous"
    else:
        source = sources[source_id]
        outcome = "unchanged" if all(observation.get(field) == source.get(field) for field in PIN_FIELDS) else "changed"
    source = sources.get(source_id, {})
    old_pin = {field: source.get(field) for field in PIN_FIELDS}
    new_pin = {field: observation.get(field) for field in PIN_FIELDS}
    return {"sourceId": source_id, "outcome": outcome, "old": old_pin, "observed": new_pin}


def work_id(result: dict[str, Any]) -> str:
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "RFW-" + hashlib.sha256(payload).hexdigest()[:16].upper()


def acquire_lock(report: Path, timeout_seconds: float = 0.5) -> int:
    """Acquire an advisory lock that the operating system releases on process death."""
    lock = report.with_name(f".{report.name}.lock")
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    except OSError as exc:
        raise RuntimeError(f"cannot open refresh report lock: {lock}: {exc}") from exc
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise RuntimeError(f"refresh report lock must be a regular file: {lock}")
        deadline = time.monotonic() + timeout_seconds
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return descriptor
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise RuntimeError(f"refresh report lock is busy: {lock}")
                time.sleep(0.05)
    except Exception:
        os.close(descriptor)
        raise


def render(results: list[dict[str, Any]], impact_map: dict[str, list[str]]) -> str:
    lines = ["# Source Refresh Review Work", ""]
    content: dict[str, list[str]] = {heading: [] for heading in REQUIRED_HEADINGS}
    content["Research question"].append("Which immutable source observations changed, became unavailable, or are ambiguous, and which stable records require human review?")
    for result in results:
        source_id = result["sourceId"]
        outcome = result["outcome"]
        old = result["old"]
        observed = result["observed"]
        old_description = f"`{old['commitSha']}:{old['path']}` / `{old['contentSha256']}`"
        if "normalizedObservationDigests" in result:
            observed_description = "conflicting normalized-observation digests " + ", ".join(
                f"`{digest}`" for digest in result["normalizedObservationDigests"]
            )
        else:
            observed_description = f"`{observed['commitSha']}:{observed['path']}` / `{observed['contentSha256']}`"
        content["Sources and immutable revisions"].append(
            f"- `{source_id}`: outcome `{outcome}`; old pointer/digest {old_description}; observed {observed_description}."
        )
        if outcome == "unchanged":
            content["Observations"].append(f"- `{source_id}` is unchanged; no review work is opened.")
        else:
            review_id = work_id(result)
            impacted = impact_map[source_id]
            content["Observations"].append(f"- `{review_id}`: `{source_id}` is `{outcome}`; review-required impacts: {', '.join(f'`{item}`' for item in impacted) or 'none mapped'}.")
            content["Conflicts"].append(f"- `{review_id}` preserves the old pointer/digest and does not resolve the meaning of a `{outcome}` result.")
    if not content["Conflicts"]:
        content["Conflicts"].append("- None detected by this unchanged comparison; semantic interpretation remains a human task.")
    content["Inference"].append("- Comparison outcomes are mechanical evidence only; they do not rewrite claim prose, classification, maturity, approval, or ADR status.")
    content["Prototype or measurement"].append("- None. This command compares recorded identifiers and bytes; it does not execute a package, runtime, browser, or protocol measurement.")
    content["Recommendation"].append("- Human reviewers should inspect each review-required work item, retain history, and decide whether linked evidence should become stale or blocked. Unchanged sources need no duplicate work.")
    content["Uncertainty"].append("- Changed, unavailable, and ambiguous comparisons leave upstream meaning unresolved until a reviewer evaluates new immutable evidence.")
    affected = sorted({item for ids in impact_map.values() for item in ids})
    content["Affected phases and requirements"].append(f"- Stable IDs mapped for review: {', '.join(f'`{item}`' for item in affected) or 'none'}.")
    content["Owner and required approval"].append("- Owner: research-owner. Required approval: protocol-technical human review; content-learning review when teaching impact changes. Automation has no approval authority.")
    for heading in REQUIRED_HEADINGS:
        lines.extend((f"## {heading}", "", *content[heading], ""))
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare immutable source observations and create review work without mutating canonical evidence.")
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--drift", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--comparison", type=Path, required=True, help="JSON array of observed immutable source pins or explicit unavailable/ambiguous outcomes")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        expected = {
            "registry": ROOT / ".planning/research/source-registry.yaml",
            "claims": ROOT / ".planning/research/claims.yaml",
            "drift": ROOT / ".planning/research/drift-register.yaml",
            "questions": ROOT / ".planning/research/open-questions.yaml",
        }
        if all(getattr(args, key).resolve() == path for key, path in expected.items()):
            snapshot = _canonical_source_snapshot()
            registry = yaml.safe_load(snapshot["research/source-registry.yaml"])
            claims = yaml.safe_load(snapshot["research/claims.yaml"]).get("claims", [])
            drift = yaml.safe_load(snapshot["research/drift-register.yaml"]).get("drift", [])
            questions = yaml.safe_load(snapshot["research/open-questions.yaml"]).get("questions", [])
        else:
            registry = load_yaml(args.registry)
            claims = load_yaml(args.claims).get("claims", [])
            drift = load_yaml(args.drift).get("drift", [])
            questions = load_yaml(args.questions).get("questions", [])
        sources = {record["id"]: record for record in registry.get("sources", []) if isinstance(record, dict) and isinstance(record.get("id"), str)}
        if not all(isinstance(records, list) for records in (claims, drift, questions)):
            raise ValueError("claims, drift, and questions records must be lists")
        results = reduce_observations(load_comparison(args.comparison), sources)
        impact_map = {item["sourceId"]: related_ids(item["sourceId"], claims, drift, questions) for item in results}
        report = render(results, impact_map)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        lock_descriptor = acquire_lock(args.report)
        try:
            temporary = args.report.with_name(f".{args.report.name}.tmp-{os.getpid()}")
            temporary.write_text(report, encoding="utf-8")
            os.replace(temporary, args.report)
        finally:
            fcntl.flock(lock_descriptor, fcntl.LOCK_UN)
            os.close(lock_descriptor)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
