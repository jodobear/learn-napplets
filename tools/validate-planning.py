#!/usr/bin/env python3
"""Validate canonical GSD planning and preserved source-pack integrity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / ".planning"


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON: {exc}") from exc


def requirement_ids(text: str) -> set[str]:
    v1_section = text.split("## v2 Requirements", 1)[0]
    return set(re.findall(r"\*\*([A-Z][A-Z0-9]{3,4}-\d{2})\*\*", v1_section))


def markdown_section(text: str, heading: str) -> str:
    """Return a review-record section body, or an empty string."""
    match = re.search(
        rf"^#{{2,6}}\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^#{{1,2}}\s|\Z)",
        text,
        re.MULTILINE,
    )
    return match.group(1) if match else ""


def phase1_execution_preflight_errors(review_text: str) -> list[str]:
    """Fail closed unless the Phase 1 convergence record authorizes execution."""
    errors: list[str] = []
    authorization = markdown_section(review_text, "Execution authorization")
    successful_reviewer = re.search(
        r"^-\s+Successful reviewer:\s+(.+?)\s*$", authorization, re.MULTILINE | re.IGNORECASE
    )
    reviewer_response = successful_reviewer.group(1) if successful_reviewer else ""
    if not reviewer_response or re.search(
        r"failed|expired|transport|authentication|error", reviewer_response, re.IGNORECASE
    ):
        errors.append("PRE001: missing successful reviewer response")

    current_high = markdown_section(review_text, "Current HIGH")
    if current_high and not re.search(r"\bnone\b", current_high, re.IGNORECASE):
        finding_ids = sorted(
            {f"HIGH-{number}" for number in re.findall(r"\bHIGH[- ]?(\d+)\b", current_high, re.IGNORECASE)}
        )
        if not finding_ids:
            errors.append("PRE002: current HIGH finding lacks disposition with rationale")
        for finding_id in finding_ids:
            disposition = re.search(
                rf"^\|[^\n|]*\b{re.escape(finding_id)}\b[^\n|]*\|\s*"
                r"(?:addressed|deferred|rejected)\s*\|\s*[^|\n\s][^|\n]*\|?\s*$",
                review_text,
                re.MULTILINE | re.IGNORECASE,
            )
            if not disposition:
                errors.append(
                    f"PRE002: current HIGH finding {finding_id} lacks disposition with rationale"
                )

    authorized = re.search(r"^-\s+Decision:\s+authorized\s*$", authorization, re.MULTILINE | re.IGNORECASE)
    dated = re.search(
        r"^-\s+Authorized date:\s+\d{4}-\d{2}-\d{2}\s*$",
        authorization,
        re.MULTILINE | re.IGNORECASE,
    )
    if not authorized or not dated:
        errors.append("PRE003: missing authorized dated convergence decision")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase-1-complete",
        action="store_true",
        help="Require Phase 1/source Phase 0 deliverables instead of baseline-pending state.",
    )
    parser.add_argument(
        "--phase-1-execution-preflight",
        action="store_true",
        help="Require the committed Phase 1 review convergence record to authorize execution.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    def error(code: str, message: str) -> None:
        errors.append(f"{code}: {message}")

    def warn(code: str, message: str) -> None:
        warnings.append(f"{code}: {message}")

    if args.phase_1_execution_preflight:
        review_path = PLANNING / "phases/01-research-and-truth-baseline/01-REVIEWS.md"
        if not review_path.is_file():
            error("PRE000", f"missing Phase 1 review record: {review_path.relative_to(ROOT)}")
        else:
            errors.extend(phase1_execution_preflight_errors(review_path.read_text()))

    contract_path = PLANNING / "validation/required-artifacts.json"
    if not contract_path.exists():
        error("PLAN001", f"missing {contract_path.relative_to(ROOT)}")
        contract = {}
    else:
        try:
            contract = load_json(contract_path)
        except ValueError as exc:
            error("PLAN002", str(exc))
            contract = {}

    for rel in contract.get("canonicalPlanning", []):
        if not (ROOT / rel).is_file():
            error("PLAN003", f"missing canonical artifact {rel}")

    parallel_state = ROOT / contract.get("forbiddenParallelState", ".planning/STATUS.md")
    if parallel_state.exists():
        error("STATE001", "STATUS.md exists; STATE.md must be sole live state source")

    config_path = PLANNING / "config.json"
    if config_path.exists():
        try:
            config = load_json(config_path)
            workflow = config.get("workflow", {})
            if workflow.get("auto_advance") is not False:
                error("AUTO001", "workflow.auto_advance must default to false")
            if workflow.get("plan_review_convergence") is not True:
                error("AUTO002", "workflow.plan_review_convergence must be true")
            if not workflow.get("security_enforcement"):
                error("AUTO003", "security enforcement must be enabled")
        except ValueError as exc:
            error("PLAN004", str(exc))

    manifest_path = PLANNING / "traceability/pack-v3-file-manifest.json"
    if manifest_path.exists():
        try:
            manifest = load_json(manifest_path)
            for entry in manifest.get("files", []):
                path = ROOT / entry["path"]
                if not path.is_file():
                    error("ARCH001", f"archived source missing: {entry['path']}")
                    continue
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest != entry["sha256"]:
                    error("ARCH002", f"archived source changed: {entry['path']}")
        except (ValueError, KeyError, TypeError) as exc:
            error("ARCH003", f"invalid source-pack manifest: {exc}")

    requirements_path = PLANNING / "REQUIREMENTS.md"
    roadmap_path = PLANNING / "ROADMAP.md"
    source_map_path = PLANNING / "traceability/requirement-source-map.yaml"
    if requirements_path.exists():
        req_ids = requirement_ids(requirements_path.read_text())
        if len(req_ids) != 25:
            error("REQ001", f"expected 25 v1 requirement IDs, found {len(req_ids)}")
        if source_map_path.exists():
            mapped = set(re.findall(r"^\s{2}([A-Z][A-Z0-9]{3,4}-\d{2}):", source_map_path.read_text(), re.M))
            missing = sorted(req_ids - mapped)
            if missing:
                error("REQ002", f"requirements missing source mappings: {', '.join(missing)}")
        if roadmap_path.exists():
            roadmap = roadmap_path.read_text()
            missing = sorted(req_id for req_id in req_ids if req_id not in roadmap)
            if missing:
                error("REQ003", f"requirements absent from roadmap: {', '.join(missing)}")

    crosswalk_path = PLANNING / "traceability/phase-crosswalk.md"
    if crosswalk_path.exists():
        rows = re.findall(r"^\|\s*(\d+)\s*\|.*?\|\s*(\d+)\s*\|", crosswalk_path.read_text(), re.M)
        if rows != [(str(i), str(i - 1)) for i in range(1, 12)]:
            error("ROAD001", "phase crosswalk must map GSD 1-11 to source 0-10")

    state_path = PLANNING / "STATE.md"
    if state_path.exists():
        state = state_path.read_text().lower()
        phase_one = re.search(r"\bphase\s*:?\s*0?1\b", state)
        source_zero = re.search(r"\bsource\s+(?:stage|phase)s?\s*0\b", state)
        if not phase_one or not source_zero:
            error("STATE002", "STATE.md must identify GSD Phase 1/source stage 0 as current")
        if "accepted" in state and "no" not in state:
            warn("STATE003", "review acceptance wording for accidental completion claims")

    blocked_markers = contract.get("productionMarkersBlockedBeforePhase3", [])
    present = [marker for marker in blocked_markers if (ROOT / marker).exists()]
    if present:
        error("GATE001", f"production scaffold present before authorization: {', '.join(present)}")

    phase1_required = [
        "research/executive-summary.md",
        "research/decision-summary.md",
        "research/source-registry.yaml",
        "research/claims.yaml",
        "research/compatibility-matrix.yaml",
        "research/drift-register.yaml",
        "research/security-egress-findings.md",
    ]
    missing_phase1 = [rel for rel in phase1_required if not (PLANNING / rel).is_file()]
    lesson_dir = PLANNING / "research/lesson-packets"
    lesson_count = len(list(lesson_dir.glob("*.md"))) if lesson_dir.exists() else 0
    if args.phase_1_complete:
        if missing_phase1:
            error("GATE002", f"Phase 1 artifacts missing: {', '.join(missing_phase1)}")
        if lesson_count != 13:
            error("GATE003", f"expected 13 lesson packets, found {lesson_count}")
    elif missing_phase1 or lesson_count != 13:
        warn("PENDING001", "Phase 1/source Phase 0 deliverables are pending as expected")

    for message in warnings:
        print(f"WARN {message}")
    for message in errors:
        print(f"ERROR {message}")

    if errors:
        print(f"Planning validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"Planning validation passed: 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
