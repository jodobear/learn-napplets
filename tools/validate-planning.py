#!/usr/bin/env python3
"""Validate canonical GSD planning and preserved source-pack integrity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

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


def load_yaml(path: Path) -> dict:
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read valid YAML {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return document


def phase1_command_errors(*args: str) -> list[str]:
    command = [sys.executable, str(ROOT / "tools/validate-research.py"), *args]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode == 0:
        return []
    detail = (result.stdout or result.stderr).strip().replace("\n", " | ")
    return [f"GATE{args[0].upper()}: {detail or 'validator failed'}"]


def phase1_citation_and_inventory_errors() -> list[str]:
    """Validate Phase 1 citation provenance and candidate disposition coverage."""
    errors: list[str] = []
    research = PLANNING / "research"
    try:
        sources = {
            record.get("id"): record
            for record in load_yaml(research / "source-registry.yaml").get("sources", [])
            if isinstance(record, dict)
        }
        claims = {
            record.get("id"): record
            for record in load_yaml(research / "claims.yaml").get("claims", [])
            if isinstance(record, dict)
        }
        candidates = {
            record.get("id")
            for record in load_yaml(research / "candidate-source-manifest.yaml").get("candidates", [])
            if isinstance(record, dict)
        }
        inventory = load_yaml(research / "ecosystem-inventory.yaml").get("items", [])
    except ValueError as exc:
        return [f"GATE014: {exc}"]

    required_source_fields = {
        "officialUrl", "repository", "commitSha", "path", "locator", "contentSha256",
        "retrievedAt", "authorityTier", "evidenceClass", "maturity", "immutableUrl",
    }
    citation_paths = [
        *sorted(research.glob("*catalog*.yaml")),
        *sorted((research / "lesson-packets").glob("*.md")),
        *sorted((PLANNING / "adr").glob("*.md")),
    ]
    for path in citation_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"GATE015: cannot read citation-bearing artifact {path.relative_to(ROOT)}: {exc}")
            continue
        for claim_id in sorted(set(re.findall(r"(?<![A-Z0-9-])(CLM-[A-Z0-9][A-Z0-9-]*)\\b", text))):
            claim = claims.get(claim_id)
            if not isinstance(claim, dict):
                errors.append(f"GATE016: {path.relative_to(ROOT)} cites unknown claim {claim_id}")
                continue
            relations = claim.get("sourceRelations")
            if not isinstance(relations, list) or not relations:
                errors.append(f"GATE017: {claim_id} lacks canonical source relations")
                continue
            for relation in relations:
                source = sources.get(relation.get("sourceId")) if isinstance(relation, dict) else None
                if not isinstance(source, dict) or any(not source.get(field) for field in required_source_fields):
                    errors.append(f"GATE018: {claim_id} does not traverse to complete immutable SRC provenance")
                    break

    dispositions = {
        item.get("candidateId"): item
        for item in inventory
        if isinstance(item, dict) and isinstance(item.get("candidateId"), str)
    }
    for candidate_id in sorted(candidates):
        item = dispositions.get(candidate_id)
        if not isinstance(item, dict) or not item.get("disposition") or not item.get("reason"):
            errors.append(f"GATE019: candidate source {candidate_id} lacks an ecosystem-inventory disposition")
    return errors


def phase1_completion_errors() -> list[str]:
    """Fail closed for the complete Phase 1 research evidence baseline."""
    errors: list[str] = []
    gates_path = PLANNING / "validation/phase-gates.yaml"
    try:
        gates = load_yaml(gates_path)
        phase = gates.get("phases", {}).get(1) or gates.get("phases", {}).get("1")
        required_artifacts = phase.get("requiredArtifacts", []) if isinstance(phase, dict) else []
    except ValueError as exc:
        return [f"GATE002: {exc}"]
    if not required_artifacts:
        errors.append("GATE003: Phase 1 required-artifact inventory is empty")
    for relative_path in required_artifacts:
        path = PLANNING / str(relative_path)
        if not path.is_file():
            errors.append(f"GATE004: missing Phase 1 required artifact {path.relative_to(ROOT)}")

    required_paths = (
        "research/phase-governance.yaml",
        "research/lesson-packets/index.yaml",
        "research/reports/spike-consolidation.md",
        "spikes/replay-manifest.yaml",
        "research/candidate-source-manifest.yaml",
        "research/ecosystem-inventory.yaml",
    )
    for relative_path in required_paths:
        if not (PLANNING / relative_path).is_file():
            errors.append(f"GATE005: missing closeout artifact .planning/{relative_path}")

    expected_spikes = tuple(f"SPK-{letter}" for letter in "ABCDEFGHIJKL")
    for spike_id in expected_spikes:
        matches = list((PLANNING / "spikes").glob(f"{spike_id.lower()}-*/report.md"))
        if len(matches) != 1:
            errors.append(f"GATE006: expected one report for {spike_id}, found {len(matches)}")
        else:
            errors.extend(phase1_command_errors("validate-report", str(matches[0])))

    index = PLANNING / "research/lesson-packets/index.yaml"
    errors.extend(phase1_command_errors("validate-lessons", "--index", str(index), "--required-present", "13"))
    lesson_result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests/phase1", "-p", "test_lesson_evidence.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if lesson_result.returncode:
        detail = (lesson_result.stdout or lesson_result.stderr).strip().replace("\n", " | ")
        errors.append(f"GATE007: full thirteen-packet canonical-evidence suite failed: {detail}")

    for number in range(1, 12):
        matches = list((PLANNING / "adr").glob(f"{number:04d}-*.md"))
        if len(matches) != 1:
            errors.append(f"GATE008: expected one proposed ADR {number:04d}, found {len(matches)}")
        else:
            errors.extend(phase1_command_errors("validate-adr", str(matches[0])))

    security = PLANNING / "research/security-egress-findings.md"
    errors.extend(phase1_command_errors("validate-report", str(security)))
    security_text = security.read_text(encoding="utf-8") if security.is_file() else ""
    required_security_content = (
        "SPK-H-IMPACT-001", "Sources and immutable revisions", "Browser observations",
        "Proposed project policy", "Unresolved questions", "Uncertainty",
        "Affected phases and requirements", "Owner and required approval",
    )
    for marker in required_security_content:
        if marker not in security_text:
            errors.append(f"GATE009: security/egress synthesis lacks required field {marker!r}")

    governance = PLANNING / "research/phase-governance.yaml"
    errors.extend(phase1_command_errors("validate-governance", str(governance)))
    errors.extend(phase1_command_errors("replay-spikes", "--manifest", str(PLANNING / "spikes/replay-manifest.yaml"), "--check"))
    errors.extend(phase1_citation_and_inventory_errors())
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
        errors.extend(phase1_completion_errors())
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
