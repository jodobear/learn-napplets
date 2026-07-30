#!/usr/bin/env python3
"""Fail-closed validation for the Phase 1 staged terminal publication boundary.

The terminal attestation deliberately lives outside the three staged target bytes.  This
avoids a self-referential digest while keeping publication consumers able to prove the
exact generation they are about to publish.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE_PATHS = (
    ".planning/PROJECT.md",
    ".planning/phases/01-research-and-truth-baseline/01-CONTEXT.md",
    ".planning/research/reports/upstream-refresh-kehto-web-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-napplet-naps-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-napplet-web-2026-07-28.md",
    ".planning/research/reports/upstream-refresh-synthesis-2026-07-28.md",
)
EXPECTED_PROBES = {
    "P-EVID01-ADJ": "test_preflight.Phase1ExecutionPreflightTests.test_citation_ascii_adjacency_extracts_exact_token",
    "P-EVID01-EMPTY": "test_preflight.Phase1ExecutionPreflightTests.test_citation_empty_inventory_has_no_diagnostic",
    "P-EVID01-ENCODING": "test_preflight.Phase1ExecutionPreflightTests.test_citation_tokens_are_ascii_decoded_codepoints_without_unicode_normalization",
    "P-EVID01-ORDER": "test_preflight.Phase1ExecutionPreflightTests.test_citation_diagnostics_stable_path_then_id",
    "P-EVID02-ADJ": "test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent",
    "P-EVID02-EMPTY": "test_drift.DriftSchemas.test_drift_rejects_empty_null_and_single_sides",
    "P-EVID02-ORDER": "test_drift.DriftSchemas.test_drift_records_sort_ids_observations_impacts_and_history",
    "P-EVID03-MANUAL": "test_gap_closeout.GapCloseoutTests.test_compatibility_completeness_requires_qualified_dimensions_without_approval",
    "P-EVID04-MANUAL": "test_gap_closeout.GapCloseoutTests.test_mandatory_spike_completeness_requires_retained_evidence_without_approval",
    "P-OPER01-IDEMPOTENCY": "test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent",
    "P-OPER01-CONCURRENCY": "test_spike_consolidation.SpikeConsolidationTests.test_recovery_after_each_publish_interruption_is_coherent",
    "P-OPER03-ADJ": "test_gap_closeout.GapCloseoutTests.test_governance_role_adjacency_requires_independence",
    "P-OPER03-EMPTY": "test_gap_closeout.GapCloseoutTests.test_governance_empty_null_single_required_fields_fail",
    "P-OPER03-ORDER": "test_gap_closeout.GapCloseoutTests.test_governance_ordering_is_stable",
}
EXPECTED_FINDINGS = tuple([f"CR-{number:02d}" for number in range(1, 10)] + [f"WR-{number:02d}" for number in range(1, 4)])
TARGET_NAMES = ("01-REVERIFICATION.md", "ROADMAP.md", "STATE.md")
AGGREGATE_ALGORITHM = "sha256:lexical-logical-path-utf8-nul-bytes-nul"


class ValidationError(RuntimeError):
    """A terminal evidence or staged-publication invariant did not hold."""


def _sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _regular(path: Path) -> Path:
    try:
        mode = path.stat(follow_symlinks=False).st_mode
    except OSError as exc:
        raise ValidationError(f"required regular file is unavailable: {path}") from exc
    if path.is_symlink() or not stat.S_ISREG(mode):
        raise ValidationError(f"required path must be a regular non-symlink file: {path}")
    return path


def _read(path: Path) -> str:
    try:
        return _regular(path).read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"required text file is not UTF-8: {path}") from exc


def _frontmatter(text: str, label: str) -> dict[str, Any]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise ValidationError(f"{label} has no YAML frontmatter")
    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValidationError(f"{label} has malformed YAML frontmatter") from exc
    if not isinstance(parsed, dict):
        raise ValidationError(f"{label} frontmatter must be a mapping")
    return parsed


def _one_section(text: str, heading: str, label: str) -> str:
    matches = list(re.finditer(rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL))
    if len(matches) != 1:
        raise ValidationError(f"{label} must contain exactly one {heading!r} section")
    return matches[0].group(1).strip()


def _table(section: str, header: tuple[str, ...], label: str) -> list[list[str]]:
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        raise ValidationError(f"{label} is not a complete Markdown table")

    def cells(line: str) -> list[str]:
        return [item.strip() for item in line.strip().strip("|").split("|")]

    if cells(lines[0]) != list(header):
        raise ValidationError(f"{label} has an unexpected header")
    if not all(re.fullmatch(r":?-{3,}:?", value.replace(" ", "")) for value in cells(lines[1])):
        raise ValidationError(f"{label} has no valid separator")
    rows = [cells(line) for line in lines[2:]]
    if any(len(row) != len(header) or any(not cell for cell in row) for row in rows):
        raise ValidationError(f"{label} has empty or malformed cells")
    return rows


def _strip_code(value: str) -> str:
    return value.strip().strip("`")


def _json_blocks(text: str, label: str) -> list[dict[str, Any] | list[Any]]:
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.DOTALL)
    parsed: list[dict[str, Any] | list[Any]] = []
    for block in blocks:
        try:
            value = json.loads(block)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{label} has malformed JSON evidence") from exc
        if not isinstance(value, (dict, list)):
            raise ValidationError(f"{label} JSON evidence must be an object or array")
        parsed.append(value)
    return parsed


def _canonical_json_sha(value: Mapping[str, Any]) -> str:
    return _sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _expected_argv(named_test: str) -> list[str]:
    return ["tools/phase1-python", "-m", "unittest", named_test]


def _ledger_payload(ledger: Mapping[str, Any]) -> dict[str, Any]:
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise ValidationError("canonical ledger attempts must be a list")
    return {
        "ledgerId": ledger.get("ledgerId"),
        "closureBoundary": ledger.get("closureBoundary"),
        "attempts": sorted(attempts, key=lambda row: row.get("attemptId", "") if isinstance(row, dict) else ""),
    }


def _ledger_by_id(text: str, ledger_id: str, label: str) -> dict[str, Any]:
    candidates = [
        value for value in _json_blocks(text, label)
        if isinstance(value, dict) and value.get("ledgerId") == ledger_id and "attempts" in value
    ]
    if len(candidates) != 1:
        raise ValidationError(f"{label} must contain exactly one direct-attempt ledger {ledger_id}")
    return candidates[0]


def _validate_ledger(ledger: Mapping[str, Any], ledger_id: str, declared_digest: str, label: str) -> dict[str, dict[str, Any]]:
    if ledger.get("ledgerId") != ledger_id or not isinstance(ledger.get("closureBoundary"), str) or not ledger["closureBoundary"]:
        raise ValidationError(f"{label} ledger identity or closure boundary is invalid")
    if not isinstance(declared_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", declared_digest):
        raise ValidationError(f"{label} ledger digest is absent or malformed")
    if _canonical_json_sha(_ledger_payload(ledger)) != declared_digest:
        raise ValidationError(f"{label} closed ledger payload digest does not match")
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != len(EXPECTED_PROBES):
        raise ValidationError(f"{label} ledger must contain exactly fourteen direct attempts")
    by_probe: dict[str, dict[str, Any]] = {}
    attempt_ids: set[str] = set()
    for attempt in attempts:
        if not isinstance(attempt, dict):
            raise ValidationError(f"{label} ledger attempt is not an object")
        probe = attempt.get("probeId")
        attempt_id = attempt.get("attemptId")
        if probe not in EXPECTED_PROBES or not isinstance(attempt_id, str):
            raise ValidationError(f"{label} ledger has an unknown probe or invalid attempt ID")
        expected_id = f"{ledger_id.replace('TERMINAL-DIRECT-14', 'DIRECT').replace('NYQUIST-DIRECT-14', 'DIRECT')}-{probe}"
        if attempt_id != expected_id or attempt_id in attempt_ids or probe in by_probe:
            raise ValidationError(f"{label} ledger direct attempt IDs are not unique designated IDs")
        if attempt.get("role") != "direct" or attempt.get("exit") != 0:
            raise ValidationError(f"{label} canonical attempt must be a successful direct attempt")
        if attempt.get("argv") != _expected_argv(EXPECTED_PROBES[probe]):
            raise ValidationError(f"{label} canonical attempt command differs from designated wrapper")
        locator = attempt.get("evidenceLocator")
        if not isinstance(locator, str) or not locator:
            raise ValidationError(f"{label} canonical attempt lacks an evidence locator")
        attempt_ids.add(attempt_id)
        by_probe[probe] = attempt
    if set(by_probe) != set(EXPECTED_PROBES):
        raise ValidationError(f"{label} ledger probe set is incomplete or has extras")
    return by_probe


def _validate_contract_ledger(validation_contract: Path) -> None:
    text = _read(validation_contract)
    ledger = _ledger_by_id(text, "P1-38-NYQUIST-DIRECT-14", "validation contract")
    closure = [
        value for value in _json_blocks(text, "validation contract")
        if isinstance(value, dict) and value.get("ledgerId") == "P1-38-NYQUIST-DIRECT-14" and "preClosureLedgerSha256" in value
    ]
    if len(closure) != 1:
        raise ValidationError("validation contract has no unique ledger closure record")
    attempts = _validate_ledger(ledger, "P1-38-NYQUIST-DIRECT-14", closure[0].get("preClosureLedgerSha256"), "validation contract")
    matrices = [value for value in _json_blocks(text, "validation contract") if isinstance(value, list) and len(value) == len(EXPECTED_PROBES)]
    if len(matrices) != 1:
        raise ValidationError("validation contract must contain one canonical probe matrix")
    _validate_matrix(matrices[0], attempts, "validation contract")


def _validate_matrix(rows: list[Any], attempts: Mapping[str, Mapping[str, Any]], label: str) -> None:
    if len(rows) != len(EXPECTED_PROBES):
        raise ValidationError(f"{label} canonical matrix must contain fourteen rows")
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValidationError(f"{label} canonical matrix row is invalid")
        probe = row.get("probeId")
        if probe not in EXPECTED_PROBES or probe in seen:
            raise ValidationError(f"{label} canonical matrix has duplicate or unknown probe")
        attempt = attempts.get(probe)
        if attempt is None or row.get("directAttemptId") != attempt.get("attemptId"):
            raise ValidationError(f"{label} canonical row does not select its designated direct attempt")
        named = row.get("namedTest")
        if not isinstance(named, str) or not named.endswith(EXPECTED_PROBES[probe].split(".")[-1]):
            raise ValidationError(f"{label} canonical row has a mismatched named test")
        row_locator = row.get("evidenceLocator")
        attempt_locator = attempt.get("evidenceLocator")
        if isinstance(row_locator, str) and row_locator.startswith("#") and isinstance(attempt_locator, str) and "#" in attempt_locator:
            row_locator = attempt_locator.split("#", 1)[0] + row_locator
        if row_locator != attempt_locator:
            raise ValidationError(f"{label} canonical row has a mismatched evidence locator")
        seen.add(probe)
    if seen != set(EXPECTED_PROBES):
        raise ValidationError(f"{label} canonical matrix probe IDs differ from the contract")


def _candidate_matrix(text: str) -> list[dict[str, Any]]:
    section = _one_section(text, "Probe Execution", "candidate")
    rows = _table(section, ("Probe ID", "Named test", "Direct attempt", "Exit", "Evidence locator"), "candidate probe matrix")
    output: list[dict[str, Any]] = []
    for probe, named, attempt, exit_code, locator in rows:
        if exit_code != "0":
            raise ValidationError("candidate canonical probe matrix contains a nonzero exit")
        output.append({
            "probeId": _strip_code(probe),
            "namedTest": _strip_code(named),
            "directAttemptId": _strip_code(attempt),
            "evidenceLocator": _strip_code(locator),
        })
    return output


def _source_binding_from_verifier() -> tuple[str, dict[str, dict[str, str]]]:
    command = [
        str(ROOT / "tools/phase1-python"),
        str(ROOT / "tools/validate-planning.py"),
        "--verify-phase1-source-inputs",
        "--review",
        str(ROOT / ".planning/phases/01-research-and-truth-baseline/01-REVIEWS.md"),
    ]
    result = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise ValidationError("Plan 01-29 source-input verifier refused terminal evidence")
    reviewed_commit: str | None = None
    digests: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if line.startswith("reviewed_commit="):
            reviewed_commit = line.split("=", 1)[1].strip()
        elif line.startswith(".planning/"):
            path, digest = line.split(maxsplit=1)
            digests[path] = digest.strip()
    if reviewed_commit is None or tuple(digests) != EXPECTED_SOURCE_PATHS:
        raise ValidationError("source-input verifier did not produce the exact six-path binding")
    rows: dict[str, dict[str, str]] = {}
    for path in EXPECTED_SOURCE_PATHS:
        listing = subprocess.run(["git", "ls-tree", reviewed_commit, "--", path], cwd=ROOT, check=False, capture_output=True, text=True)
        parts = listing.stdout.strip().split(maxsplit=3)
        if len(parts) != 4 or parts[0] != "100644" or parts[1] != "blob" or parts[3] != path:
            raise ValidationError(f"reviewed source input has no expected regular Git blob: {path}")
        current = ROOT / path
        if _sha(_regular(current).read_bytes()) != digests[path]:
            raise ValidationError(f"working source input differs from reviewed digest: {path}")
        rows[path] = {"mode": parts[0], "blob": parts[2], "sha": digests[path], "commit": reviewed_commit}
    return reviewed_commit, rows


def _source_table(text: str, label: str) -> dict[str, dict[str, str]]:
    section = _one_section(text, "Reviewed Source-Grounding Authorization", label)
    rows = _table(section, ("Path", "Git mode", "Git blob", "SHA-256", "Reviewed commit"), f"{label} source authorization")
    parsed: dict[str, dict[str, str]] = {}
    for path, mode, blob, digest, commit in rows:
        normalized = _strip_code(path)
        if normalized in parsed:
            raise ValidationError(f"{label} source authorization has duplicate path")
        parsed[normalized] = {
            "mode": _strip_code(mode), "blob": _strip_code(blob), "sha": _strip_code(digest), "commit": _strip_code(commit),
        }
    if tuple(parsed) != EXPECTED_SOURCE_PATHS:
        raise ValidationError(f"{label} source authorization does not contain the exact six paths")
    return parsed


def _validate_source_table(text: str, label: str) -> tuple[str, dict[str, dict[str, str]]]:
    actual_commit, expected = _source_binding_from_verifier()
    observed = _source_table(text, label)
    if observed != expected:
        raise ValidationError(f"{label} source authorization differs from the Plan 01-29 verifier")
    return actual_commit, observed


def _security_findings(security: Path) -> tuple[dict[str, Any], dict[str, dict[str, str]]]:
    meta = _frontmatter(_read(security), "security review")
    findings = meta.get("findings")
    if meta.get("status") != "passed" or meta.get("open_high_count") != 0 or not isinstance(findings, list):
        raise ValidationError("security review is not a passing ASVS L1 evidence record")
    result: dict[str, dict[str, str]] = {}
    for item in findings:
        if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in ("id", "command", "source_path")):
            raise ValidationError("security finding register is malformed")
        finding_id = item["id"]
        if finding_id in result:
            raise ValidationError("security finding register has a duplicate finding")
        result[finding_id] = {"command": item["command"], "source": item["source_path"]}
    if tuple(result) != EXPECTED_FINDINGS:
        raise ValidationError("security finding register does not have the exact CR/WR finding set")
    return meta, result


def _validate_adjudication(text: str, security: Path) -> dict[str, Any]:
    section = _one_section(text, "Review Finding Adjudication", "candidate")
    rows = _table(section, ("Finding ID", "Approved wrapper command", "Fresh result/evidence locator", "Repaired source path", "Verdict"), "candidate adjudication")
    metadata, expected = _security_findings(security)
    observed: dict[str, tuple[str, str]] = {}
    for finding, command, evidence, source, verdict in rows:
        command = _strip_code(command)
        source = _strip_code(source)
        if finding in observed or not evidence.strip() or "tools/phase1-python" not in command or not verdict.strip():
            raise ValidationError("candidate adjudication has duplicate, stale, or non-wrapper evidence")
        observed[finding] = (command, source)
    if set(observed) != set(expected):
        raise ValidationError("candidate adjudication finding IDs are not exact")
    for finding, value in expected.items():
        if observed[finding] != (value["command"], value["source"]):
            raise ValidationError(f"candidate adjudication mapping differs for {finding}")
    return metadata


def _audit_batch(text: str, candidate_meta: Mapping[str, Any], ledger_digest: str) -> None:
    batches_objects = [value for value in _json_blocks(text, "post-closure audit") if isinstance(value, dict) and "batches" in value]
    if len(batches_objects) != 1 or not isinstance(batches_objects[0].get("batches"), list):
        raise ValidationError("post-closure audit must contain exactly one batch registry")
    batches = batches_objects[0]["batches"]
    ids: set[str] = set()
    selected_id = candidate_meta.get("selected_post_closure_batch_id")
    selected_digest = candidate_meta.get("selected_post_closure_batch_sha256")
    selected: Mapping[str, Any] | None = None
    for batch in batches:
        if not isinstance(batch, dict) or not isinstance(batch.get("batchId"), str) or batch["batchId"] in ids:
            raise ValidationError("post-closure audit has an invalid or duplicate batch ID")
        ids.add(batch["batchId"])
        if batch.get("ledgerId") != "P1-40-TERMINAL-DIRECT-14" or batch.get("preClosureLedgerSha256") != ledger_digest:
            continue
        payload = {key: value for key, value in batch.items() if key != "batchPayloadSha256"}
        if _canonical_json_sha(payload) != batch.get("batchPayloadSha256"):
            raise ValidationError("post-closure batch payload digest does not match")
        runs = batch.get("runs")
        if not isinstance(runs, list) or not runs or any(not isinstance(run, dict) or run.get("exit") != 0 for run in runs):
            raise ValidationError("post-closure batch runs are malformed")
        if batch["batchId"] == selected_id:
            selected = batch
    if selected is None or selected.get("batchPayloadSha256") != selected_digest:
        raise ValidationError("candidate selected audit batch is missing or does not bind its digest")


def validate_candidate_evidence(*, candidate: Path, validation_contract: Path, post_closure_audit: Path, security: Path) -> dict[str, Any]:
    """Validate immutable candidate evidence without writing live or staged state."""
    text = _read(candidate)
    meta = _frontmatter(text, "candidate")
    if meta.get("re_verification") is not True or meta.get("terminal_verdict") != "pending_human_recheck":
        raise ValidationError("candidate must remain a non-terminal pending-human-recheck dossier")
    historical = ROOT / ".planning/phases/01-research-and-truth-baseline/01-VERIFICATION.md"
    if meta.get("historical_verification_sha256") != _sha(_regular(historical).read_bytes()):
        raise ValidationError("candidate does not bind the unchanged historical verification record")
    _, sources = _validate_source_table(text, "candidate")
    security_meta = _validate_adjudication(text, security)
    if meta.get("security_review_sha256") != _sha(_regular(security).read_bytes()):
        raise ValidationError("candidate does not bind the security review digest")
    if meta.get("active_plan_review_manifest_sha256") != security_meta.get("reviewed_plan_manifest_sha256"):
        raise ValidationError("candidate plan-review digest differs from the security review")
    _validate_contract_ledger(validation_contract)
    ledger = _ledger_by_id(text, "P1-40-TERMINAL-DIRECT-14", "candidate")
    attempts = _validate_ledger(ledger, "P1-40-TERMINAL-DIRECT-14", meta.get("canonical_ledger_sha256"), "candidate")
    _validate_matrix(_candidate_matrix(text), attempts, "candidate")
    _audit_batch(_read(post_closure_audit), meta, meta["canonical_ledger_sha256"])
    return {"metadata": meta, "sourceBinding": sources, "ledgerDigest": meta["canonical_ledger_sha256"]}


def generation_sha256(targets: Mapping[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(targets):
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(targets[name])
        digest.update(b"\0")
    return digest.hexdigest()


def _roles(meta: Mapping[str, Any], candidate_digest: str, security_digest: str, plan_digest: str, reviewed_commit: str, executor_identity: str) -> None:
    for field, role in (("terminalVerifier", "terminalVerifier"), ("projectOwnerRechecker", "projectOwnerRechecker")):
        record = meta.get(field)
        if not isinstance(record, dict):
            raise ValidationError(f"staged re-verification lacks {field} role record")
        prohibited = {key for key in record if "target" in key.lower() or "aggregate" in key.lower()}
        if prohibited:
            raise ValidationError("role records must not contain target map, hash, or aggregate data")
        required = {
            "role": role,
            "principal": None,
            "timestamp": None,
            "reviewed_commit": reviewed_commit,
            "plan_review_sha256": plan_digest,
            "evidence_sha256": candidate_digest,
            "security_sha256": security_digest,
            "determination": None,
            "rationale": None,
        }
        for key, expected in required.items():
            value = record.get(key)
            if expected is None:
                if not isinstance(value, str) or not value.strip():
                    raise ValidationError(f"{field} role record has an empty {key}")
            elif value != expected:
                raise ValidationError(f"{field} role record has mismatched {key}")
        if record["principal"] == executor_identity or record["determination"] not in {"passed", "blocked"}:
            raise ValidationError(f"{field} role record is not an eligible non-executor terminal determination")


def _staged_targets(staged_root: Path, attestation: Path) -> dict[str, bytes]:
    try:
        mode = staged_root.stat(follow_symlinks=False).st_mode
    except OSError as exc:
        raise ValidationError("staged root is unavailable") from exc
    if staged_root.is_symlink() or not stat.S_ISDIR(mode):
        raise ValidationError("staged root must be a regular directory")
    names = sorted(item.name for item in staged_root.iterdir() if item.name != attestation.name)
    if tuple(names) != TARGET_NAMES:
        raise ValidationError("staged root must contain the exact three target files and no extras")
    return {name: _regular(staged_root / name).read_bytes() for name in TARGET_NAMES}


def validate_existing_attestation(staged_root: Path, attestation: Path) -> dict[str, Any]:
    """Recheck that an external attestation still binds the current staged target bytes."""
    targets = _staged_targets(staged_root, attestation)
    try:
        payload = json.loads(_read(attestation))
    except json.JSONDecodeError as exc:
        raise ValidationError("terminal attestation is malformed") from exc
    if not isinstance(payload, dict) or payload.get("aggregateAlgorithm") != AGGREGATE_ALGORITHM:
        raise ValidationError("terminal attestation algorithm is invalid")
    expected_map = {name: _sha(content) for name, content in targets.items()}
    if payload.get("profile") != "terminal" or payload.get("targetMap") != expected_map or payload.get("generationSha256") != generation_sha256(targets):
        raise ValidationError("terminal attestation does not bind the exact staged target-only generation")
    return payload


def validate_staged_terminal(*, staged_root: Path, candidate: Path, security: Path, reviewed_commit: str, post_closure_audit: Path, executor_identity: str, attestation: Path) -> dict[str, Any]:
    """Validate three staged targets then write one external non-self-referential attestation."""
    if not executor_identity:
        raise ValidationError("executor identity is required for terminal role separation")
    if attestation.exists() or attestation.is_symlink():
        if attestation.is_symlink() or not attestation.is_file():
            raise ValidationError("existing terminal attestation path is unsafe")
        attestation.unlink()
    candidate_evidence = validate_candidate_evidence(
        candidate=candidate,
        validation_contract=ROOT / ".planning/phases/01-research-and-truth-baseline/01-VALIDATION.md",
        post_closure_audit=post_closure_audit,
        security=security,
    )
    targets = _staged_targets(staged_root, attestation)
    reverify_text = targets["01-REVERIFICATION.md"].decode("utf-8")
    reverify_meta = _frontmatter(reverify_text, "staged re-verification")
    candidate_digest = _sha(_regular(candidate).read_bytes())
    security_digest = _sha(_regular(security).read_bytes())
    plan_digest = candidate_evidence["metadata"].get("active_plan_review_manifest_sha256")
    if reverify_meta.get("reviewed_commit") != reviewed_commit:
        raise ValidationError("staged re-verification reviewed commit does not match invocation")
    if reverify_meta.get("candidate_sha256") != candidate_digest or reverify_meta.get("security_sha256") != security_digest or reverify_meta.get("plan_review_sha256") != plan_digest:
        raise ValidationError("staged re-verification artifact digests do not bind candidate and security evidence")
    _, candidate_sources = _validate_source_table(_read(candidate), "candidate")
    if _source_table(reverify_text, "staged re-verification") != candidate_sources:
        raise ValidationError("staged re-verification source authorization differs from candidate")
    _roles(reverify_meta, candidate_digest, security_digest, plan_digest, reviewed_commit, executor_identity)
    target_map = {name: _sha(content) for name, content in targets.items()}
    payload = {
        "aggregateAlgorithm": AGGREGATE_ALGORITHM,
        "candidateSha256": candidate_digest,
        "generationSha256": generation_sha256(targets),
        "planReviewSha256": plan_digest,
        "profile": "terminal",
        "reviewedCommit": reviewed_commit,
        "securitySha256": security_digest,
        "targetMap": target_map,
        "validationResult": "passed",
    }
    temporary = attestation.with_name(f".{attestation.name}.tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    os.replace(temporary, attestation)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Phase 1 terminal evidence and staged targets")
    parser.add_argument("--validate-candidate-evidence", action="store_true")
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--validation-contract", type=Path)
    parser.add_argument("--post-closure-audit", type=Path, required=True)
    parser.add_argument("--security", type=Path, default=ROOT / ".planning/phases/01-research-and-truth-baseline/01-SECURITY.md")
    parser.add_argument("--staged-root", type=Path)
    parser.add_argument("--reviewed-commit")
    parser.add_argument("--attestation", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.validate_candidate_evidence:
            if args.validation_contract is None or args.staged_root is not None or args.attestation is not None:
                raise ValidationError("candidate-only validation requires a validation contract and no staged publication arguments")
            validate_candidate_evidence(
                candidate=args.candidate,
                validation_contract=args.validation_contract,
                post_closure_audit=args.post_closure_audit,
                security=args.security,
            )
        else:
            if args.staged_root is None or args.reviewed_commit is None or args.attestation is None:
                raise ValidationError("staged validation requires staged root, reviewed commit, and attestation")
            validate_staged_terminal(
                staged_root=args.staged_root,
                candidate=args.candidate,
                security=args.security,
                reviewed_commit=args.reviewed_commit,
                post_closure_audit=args.post_closure_audit,
                executor_identity=os.environ.get("GSD_EXECUTOR_ID", ""),
                attestation=args.attestation,
            )
    except ValidationError as exc:
        print(f"TERMINAL_VALIDATION_REFUSED: {exc}", file=sys.stderr)
        return 1
    print("terminal validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
