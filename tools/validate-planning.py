#!/usr/bin/env python3
"""Validate canonical GSD planning and preserved source-pack integrity."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import unicodedata
from pathlib import Path
from types import MappingProxyType

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


REQUIRED_PHASE1_SOURCE_INPUTS = (
    ".planning/PROJECT.md",
    ".planning/phases/01-research-and-truth-baseline/01-CONTEXT.md",
    ".planning/research/reports/upstream-refresh-kehto-web-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-napplet-naps-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-napplet-web-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-synthesis-2026-07-28.md",
)


def _frontmatter(text: str) -> str:
    match = re.match(r"\A---\n([\s\S]*?)\n---\n", text)
    if not match:
        raise ValueError("PRE100: review record lacks a bounded frontmatter manifest")
    return match.group(1)


def _single_frontmatter_value(frontmatter: str, name: str) -> str:
    values = re.findall(rf"^{re.escape(name)}:\s*(\S.*?)\s*$", frontmatter, re.MULTILINE)
    if len(values) != 1:
        raise ValueError(f"PRE101: expected exactly one {name} field")
    return values[0].strip().strip('"')


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise ValueError(f"PRE102: git {' '.join(args)} failed: {detail}")
    return completed.stdout


def _blob_at(root: Path, revision: str, path: str) -> tuple[str, bytes]:
    listing = _git(root, "ls-tree", revision, "--", path).strip()
    match = re.fullmatch(r"100644 blob ([0-9a-f]{40})\t(.+)", listing)
    if not match or match.group(2) != path:
        raise ValueError(f"PRE103: {path} is not a regular 100644 blob at {revision}")
    return match.group(1), _git(root, "show", f"{revision}:{path}").encode()


def _parse_review_manifest(review_text: str) -> tuple[str, str, dict[str, str], dict[str, tuple[str, str, str]], bool]:
    frontmatter = _frontmatter(review_text)
    reviewed_commit = _single_frontmatter_value(frontmatter, "reviewed_commit")
    identity_block = re.search(r'^reviewer_identity:\n((?:  [^\n]+\n)+)', frontmatter, re.MULTILINE)
    reviewer = re.search(r'^  [^\s:#]+:\s*"?([^"\n]+?)"?\s*$', identity_block.group(1), re.MULTILINE) if identity_block else None
    if not reviewer or not reviewer.group(1).strip():
        raise ValueError("PRE104: missing independent reviewer identity")
    reviewer_identity = reviewer.group(1).strip()
    verdict_match = re.search(r'^  verdict:\s*"?([^"\n]+?)"?\s*$', frontmatter, re.MULTILINE)
    if not verdict_match or verdict_match.group(1).strip() != "CONVERGED; HIGH=0; actionable=0":
        raise ValueError("PRE105: convergence verdict must equal CONVERGED; HIGH=0; actionable=0")
    if _single_frontmatter_value(frontmatter, "current_high") != "0" or _single_frontmatter_value(frontmatter, "current_actionable") != "0":
        raise ValueError("PRE106: review record has unresolved HIGH or actionable findings")
    superseded_rows = re.findall(r'^  superseded:\s*(true|false)\s*$', frontmatter, re.MULTILINE | re.IGNORECASE)
    if len(superseded_rows) != 1:
        raise ValueError("PRE107: superseded state must be explicit exactly once")
    superseded = superseded_rows[0].lower()

    plan_block = re.search(r'^plan_file_sha256:\n([\s\S]*?)(?=^reviewed_source_inputs:)', frontmatter, re.MULTILINE)
    if not plan_block:
        raise ValueError("PRE108: missing active-plan manifest")
    plan_text = plan_block.group(1).split("\nplan_snapshot:", 1)[0]
    plans: dict[str, str] = {}
    plan_rows = re.findall(r'^\s{0,2}([^\s:]+):\s*([0-9a-f]{64})\s*$', plan_text, re.MULTILINE)
    if not plan_rows or len(plan_rows) != len(plan_text.strip().splitlines()):
        raise ValueError("PRE109: malformed active-plan manifest entry")
    for name, digest in plan_rows:
        if name in plans:
            raise ValueError(f"PRE110: duplicate active-plan manifest entry: {name}")
        plans[name] = digest

    source_block = re.search(r'^reviewed_source_inputs:\n[\s\S]*?^  paths:\n([\s\S]*)\Z', frontmatter, re.MULTILINE)
    if not source_block:
        raise ValueError("PRE111: missing reviewed source-input manifest")
    source_rows = re.findall(
        r'^    - path: ([^\n]+)\n      mode: "?(\d+)"?\n      git_blob: ([0-9a-f]{40})\n      sha256: ([0-9a-f]{64})\s*$',
        source_block.group(1),
        re.MULTILINE,
    )
    if len(source_rows) != len(source_block.group(1).strip().split("\n    - path: ")):
        raise ValueError("PRE112: malformed source-input manifest entry")
    sources: dict[str, tuple[str, str, str]] = {}
    for path, mode, blob, digest in source_rows:
        if path in sources:
            raise ValueError(f"PRE113: duplicate source-input manifest entry: {path}")
        sources[path] = (mode, blob, digest)
    for heading in ("Execution authorization", "Convergence"):
        if len(re.findall(rf'^##\s+{re.escape(heading)}\s*$', review_text, re.MULTILINE)) > 1:
            raise ValueError(f"PRE114: duplicate bounded {heading} section")
    return reviewed_commit, reviewer_identity, plans, sources, superseded == "true"


def review_manifest_errors(review_text: str, *, root: Path = ROOT, executor_identity: str | None = None) -> list[str]:
    """Validate current bytes against the independent content-addressed review record."""
    try:
        reviewed_commit, reviewer, plans, sources, superseded = _parse_review_manifest(review_text)
        if superseded:
            raise ValueError("PRE115: review record is explicitly superseded")
        if not executor_identity:
            raise ValueError("PRE116: missing nonempty executor identity")
        if executor_identity == reviewer:
            raise ValueError("PRE117: executor identity must differ from reviewer identity")
        _git(root, "rev-parse", "--verify", f"{reviewed_commit}^{{commit}}")
        active = sorted(path.name for path in (root / ".planning/phases/01-research-and-truth-baseline").glob("01-*-PLAN.md"))
        if sorted(plans) != active:
            raise ValueError("PRE118: review plan manifest is not the exact active plan set")
        for name in active:
            path = ".planning/phases/01-research-and-truth-baseline/" + name
            current = (root / path).read_bytes()
            expected = plans[name]
            if hashlib.sha256(current).hexdigest() != expected:
                raise ValueError(f"PRE119: active plan digest differs: {name}")
            _, reviewed_bytes = _blob_at(root, reviewed_commit, path)
            if hashlib.sha256(reviewed_bytes).hexdigest() != expected:
                raise ValueError(f"PRE120: reviewed commit plan differs: {name}")
        if tuple(sorted(sources)) != REQUIRED_PHASE1_SOURCE_INPUTS:
            raise ValueError("PRE121: source-input manifest is not the closed sorted six-path set")
        for path in REQUIRED_PHASE1_SOURCE_INPUTS:
            mode, declared_blob, declared_digest = sources[path]
            if mode != "100644":
                raise ValueError(f"PRE122: source input mode is not 100644: {path}")
            blob, reviewed_bytes = _blob_at(root, reviewed_commit, path)
            if blob != declared_blob or hashlib.sha256(reviewed_bytes).hexdigest() != declared_digest:
                raise ValueError(f"PRE123: reviewed source blob differs: {path}")
            head_blob, head_bytes = _blob_at(root, "HEAD", path)
            if head_blob != declared_blob or head_bytes != reviewed_bytes:
                raise ValueError(f"PRE124: HEAD source blob differs: {path}")
            working = root / path
            if working.is_symlink() or not working.is_file() or not stat.S_ISREG(working.stat().st_mode):
                raise ValueError(f"PRE125: working source input is not a tracked regular file: {path}")
            _git(root, "ls-files", "--error-unmatch", "--", path)
            if working.read_bytes() != reviewed_bytes or hashlib.sha256(working.read_bytes()).hexdigest() != declared_digest:
                raise ValueError(f"PRE126: working source input bytes differ: {path}")
    except (OSError, ValueError) as exc:
        return [str(exc)]
    return []


def phase1_execution_preflight_errors(review_text: str, *, root: Path = ROOT, executor_identity: str | None = None) -> list[str]:
    return review_manifest_errors(review_text, root=root, executor_identity=executor_identity)


def load_reviewed_phase1_source_snapshot(review_path: Path, *, root: Path = ROOT, executor_identity: str) -> MappingProxyType:
    """Return immutable bytes sourced only from exact reviewed Git blobs."""
    text = review_path.read_text(encoding="utf-8")
    errors = review_manifest_errors(text, root=root, executor_identity=executor_identity)
    if errors:
        raise ValueError("; ".join(errors))
    reviewed_commit, _, _, sources, _ = _parse_review_manifest(text)
    snapshot = {path: _blob_at(root, reviewed_commit, path)[1] for path in REQUIRED_PHASE1_SOURCE_INPUTS}
    if any(hashlib.sha256(snapshot[path]).hexdigest() != sources[path][2] for path in snapshot):
        raise ValueError("PRE127: reviewed source snapshot digest changed during loading")
    return MappingProxyType(snapshot)


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise ValueError("cannot read YAML without the certified Phase 1 environment") from exc
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


_CLAIM_CITATION = re.compile(r"(?<![A-Za-z0-9-])(CLM-[A-Z0-9]+(?:-[A-Z0-9]+)*)\b")


def _citation_claim_ids(text: str) -> set[str]:
    """Extract exact ASCII CLM tokens without Unicode normalization."""
    citations: set[str] = set()
    for match in _CLAIM_CITATION.finditer(text):
        before = text[match.start() - 1] if match.start() else ""
        after = text[match.end()] if match.end() < len(text) else ""
        if (
            any(character and unicodedata.category(character).startswith("M") for character in (before, after))
            or after in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-"
        ):
            continue
        citations.add(match.group(1))
    return citations


def phase1_citation_and_inventory_errors(*, root: Path = ROOT) -> list[str]:
    """Validate citation provenance and inventory coverage without mutating evidence."""
    errors: list[str] = []
    research = root / ".planning/research"
    planning = root / ".planning"
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
    citation_paths = sorted([
        *research.glob("*catalog*.yaml"),
        *(research / "lesson-packets").glob("*.md"),
        *(planning / "adr").glob("*.md"),
    ])
    for path in citation_paths:
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"GATE015: cannot read citation-bearing artifact {path.relative_to(root)}: {exc}")
            continue
        for claim_id in sorted(_citation_claim_ids(text)):
            claim = claims.get(claim_id)
            if not isinstance(claim, dict):
                errors.append(f"GATE016: {path.relative_to(root)} cites unknown claim {claim_id}")
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
        "research/adr-handoff.yaml",
        "research/lesson-packets/index.yaml",
        "research/reports/phase-gate.md",
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
    phase_gate = PLANNING / "research/reports/phase-gate.md"
    errors.extend(phase1_command_errors("validate-report", str(phase_gate)))
    handoff_path = PLANNING / "research/adr-handoff.yaml"
    try:
        handoff = load_yaml(handoff_path)
        entry = handoff.get("phase2Entry")
        handoff_adrs = handoff.get("adrs")
        expected_adrs = {f"ADR-{number:04d}" for number in range(1, 12)}
        indexed_adrs = {item.get("id"): item for item in handoff_adrs if isinstance(item, dict)} if isinstance(handoff_adrs, list) else {}
        if not isinstance(entry, dict) or not entry.get("interimRestriction"):
            errors.append("GATE010: ADR handoff lacks the Phase 2 interim no-scaffold restriction")
        if set(indexed_adrs) != expected_adrs:
            errors.append("GATE011: ADR handoff must account for ADR-0001 through ADR-0011 exactly")
        for adr_id, record in indexed_adrs.items():
            missing = [field for field in ("owner", "approver", "evidenceIds", "status", "acceptanceDeadline", "affectedRequirements", "affectedPhases") if not record.get(field)]
            if record.get("status") != "proposed" or missing:
                errors.append(f"GATE012: ADR handoff {adr_id} lacks complete proposed handoff fields")
    except ValueError as exc:
        errors.append(f"GATE013: {exc}")
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
    parser.add_argument(
        "--verify-phase1-source-inputs",
        action="store_true",
        help="Read-only verification of the closed reviewed Phase 1 source-input map.",
    )
    parser.add_argument("--review", type=Path, help="Review record for --verify-phase1-source-inputs.")
    parser.add_argument("--executor-identity", help="Nonempty identity that must match GSD_EXECUTOR_ID.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    def error(code: str, message: str) -> None:
        errors.append(f"{code}: {message}")

    def warn(code: str, message: str) -> None:
        warnings.append(f"{code}: {message}")

    execution_gate_requested = args.phase_1_execution_preflight or args.phase_1_complete
    if execution_gate_requested:
        environment_identity = os.environ.get("GSD_EXECUTOR_ID", "")
        if not args.executor_identity or not environment_identity or args.executor_identity != environment_identity:
            error("PRE116", "missing or mismatched --executor-identity and GSD_EXECUTOR_ID")
        else:
            review_path = PLANNING / "phases/01-research-and-truth-baseline/01-REVIEWS.md"
            if not review_path.is_file():
                error("PRE000", f"missing Phase 1 review record: {review_path.relative_to(ROOT)}")
            else:
                errors.extend(
                    phase1_execution_preflight_errors(
                        review_path.read_text(encoding="utf-8"), executor_identity=args.executor_identity
                    )
                )
        if errors:
            for message in errors:
                print(f"ERROR {message}")
            print(f"Planning validation failed: {len(errors)} error(s), 0 warning(s).")
            return 1

    if args.verify_phase1_source_inputs:
        if not args.review:
            error("PRE128", "--verify-phase1-source-inputs requires --review")
        elif not args.review.is_file():
            error("PRE129", f"review record is unavailable: {args.review}")
        else:
            review_text = args.review.read_text(encoding="utf-8")
            verification_identity = args.executor_identity or "source-input-verifier"
            errors.extend(review_manifest_errors(review_text, executor_identity=verification_identity))
            if not errors:
                reviewed_commit, _, _, sources, _ = _parse_review_manifest(review_text)
                print(f"reviewed_commit={reviewed_commit}")
                for path in REQUIRED_PHASE1_SOURCE_INPUTS:
                    print(f"{path} {sources[path][2]}")
        if errors:
            for message in errors:
                print(f"ERROR {message}")
            print(f"Planning validation failed: {len(errors)} error(s), 0 warning(s).")
            return 1
        return 0

    if args.phase_1_execution_preflight and not args.phase_1_complete:
        print("Phase 1 execution preflight passed")
        return 0

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
