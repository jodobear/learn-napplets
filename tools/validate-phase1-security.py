#!/usr/bin/env python3
"""Validate the Phase 1 human ASVS L1 security-review boundary.

This validator validates evidence bindings and review structure. It deliberately
cannot author, approve, or turn a human review into a security decision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FINDINGS = tuple([f"CR-{number:02d}" for number in range(1, 10)] + [f"WR-{number:02d}" for number in range(1, 4)])
BOUND_FINDING_FIELDS = (
    "id", "threat", "severity", "primary_coverage", "disposition", "command", "result", "source_path", "applicable_asvs_ids",
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ASVS_ID = re.compile(r"^v5\.0\.0-[A-Za-z0-9.-]+$")
SEC_ID = re.compile(r"^SEC-[1-9][0-9]{2,}$")


def error(errors: list[str], message: str) -> None:
    errors.append(f"ERROR SEC: {message}")


def required_string(value: Any, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        error(errors, f"{label} must be a nonempty string")
        return None
    return value


def digest(value: Any, label: str, errors: list[str]) -> str | None:
    text = required_string(value, label, errors)
    if text is None:
        return None
    if not SHA256.fullmatch(text):
        error(errors, f"{label} must be a lowercase SHA-256")
        return None
    return text


def timestamp(value: Any, label: str, errors: list[str]) -> None:
    text = required_string(value, label, errors)
    if text is None:
        return
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        error(errors, f"{label} must be an RFC3339 timestamp")
        return
    if parsed.tzinfo is None:
        error(errors, f"{label} must include a timezone")


def review_date(value: Any, errors: list[str]) -> None:
    text = required_string(value, "review_date", errors)
    if text is None:
        return
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        error(errors, "review_date must be an ISO calendar date")


def load_yaml(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        error(errors, f"cannot read {label}: {exc}")
        return None
    if not isinstance(document, dict):
        error(errors, f"{label} must be a YAML mapping")
        return None
    return document


def load_frontmatter(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        error(errors, f"cannot read security review: {exc}")
        return None
    match = re.match(r"\A---\n([\s\S]*?)\n---\n", text)
    if match is None:
        error(errors, "security review requires bounded YAML frontmatter")
        return None
    try:
        document = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        error(errors, f"security review frontmatter is invalid YAML: {exc}")
        return None
    if not isinstance(document, dict):
        error(errors, "security review frontmatter must be a YAML mapping")
        return None
    return document


def canonical_digest(value: Mapping[str, Any], omitted_key: str) -> str:
    """Digest a record without its self-referential manifest field."""
    payload = dict(value)
    payload.pop(omitted_key, None)
    return hashlib.sha256(
        yaml.safe_dump(payload, sort_keys=True, allow_unicode=True).encode("utf-8")
    ).hexdigest()


def validate_matrix(matrix: Mapping[str, Any], errors: list[str]) -> set[str]:
    if matrix.get("asvs_version") != "5.0.0":
        error(errors, "ASVS matrix must declare asvs_version 5.0.0")
    if matrix.get("level") != "L1":
        error(errors, "ASVS matrix must declare level L1")
    catalog = matrix.get("catalog_requirement_ids")
    controls = matrix.get("controls")
    if not isinstance(catalog, list) or not catalog or not all(isinstance(item, str) for item in catalog):
        error(errors, "ASVS matrix requires a nonempty catalog_requirement_ids string list")
        return set()
    if len(catalog) != len(set(catalog)) or any(ASVS_ID.fullmatch(item) is None for item in catalog):
        error(errors, "ASVS catalog requirement IDs must be unique v5.0.0 IDs")
    if not isinstance(controls, list):
        error(errors, "ASVS matrix controls must be a list")
        return set(catalog)
    control_ids = [item.get("id") for item in controls if isinstance(item, dict)]
    if len(control_ids) != len(controls) or control_ids != catalog:
        error(errors, "ASVS matrix controls must list each catalog requirement exactly once in catalog order")
    applicable: set[str] = set()
    for control in controls:
        if not isinstance(control, dict):
            continue
        control_id = control.get("id", "<unknown>")
        source = control.get("source")
        if not isinstance(source, dict):
            error(errors, f"{control_id} requires a source path and SHA-256")
        else:
            required_string(source.get("path"), f"{control_id} source path", errors)
            digest(source.get("sha256"), f"{control_id} source SHA-256", errors)
        applicability = control.get("applicability")
        if applicability not in {"applicable", "not-applicable", "blocked"}:
            error(errors, f"{control_id} has an invalid applicability")
        required_string(control.get("rationale"), f"{control_id} rationale", errors)
        if applicability == "applicable":
            applicable.add(str(control_id))
            for key in ("verification_status", "command_or_evidence", "observed_result"):
                required_string(control.get(key), f"{control_id} {key}", errors)
            linked = control.get("linked_references")
            if not isinstance(linked, list) or not linked or any(not isinstance(item, str) or not item for item in linked):
                error(errors, f"{control_id} requires nonempty linked_references")
    return applicable


def validate_finding(finding: Any, applicable_controls: set[str], errors: list[str]) -> str | None:
    if not isinstance(finding, dict):
        error(errors, "security finding must be a mapping")
        return None
    finding_id = required_string(finding.get("id"), "finding id", errors)
    if finding_id is None:
        return None
    for key in ("threat", "severity", "primary_coverage", "disposition", "command", "result", "source_path"):
        required_string(finding.get(key), f"{finding_id} {key}", errors)
    linked = finding.get("applicable_asvs_ids")
    if not isinstance(linked, list) or not linked or any(not isinstance(item, str) for item in linked):
        error(errors, f"{finding_id} requires applicable ASVS IDs")
    elif any(item not in applicable_controls for item in linked):
        error(errors, f"{finding_id} links a non-applicable or unknown ASVS control")
    return finding_id


def finding_map(findings: Any, applicable_controls: set[str], errors: list[str], label: str) -> dict[str, Mapping[str, Any]]:
    if not isinstance(findings, list):
        error(errors, f"{label} findings must be a list")
        return {}
    output: dict[str, Mapping[str, Any]] = {}
    for finding in findings:
        finding_id = validate_finding(finding, applicable_controls, errors)
        if finding_id is None:
            continue
        if finding_id in output:
            error(errors, f"{label} repeats finding {finding_id}")
            continue
        output[finding_id] = finding
    required = set(REQUIRED_FINDINGS)
    ids = set(output)
    if not required.issubset(ids):
        error(errors, f"{label} must include every required CR-01..CR-09 and WR-01..WR-03 finding")
    unexpected = ids - required
    malformed = sorted(item for item in unexpected if SEC_ID.fullmatch(item) is None)
    if malformed:
        error(errors, f"{label} has malformed optional finding IDs: {', '.join(malformed)}")
    return output


def validate_role(
    record: Any,
    role: str,
    review: Mapping[str, Any],
    evidence: Mapping[str, Any],
    reviewed_commit: str,
    executor: str,
    errors: list[str],
) -> Mapping[str, Any] | None:
    if not isinstance(record, dict):
        error(errors, f"{role} record must be a mapping")
        return None
    if record.get("role") != role:
        error(errors, f"{role} record must name its role")
    principal = required_string(record.get("principal"), f"{role} principal", errors)
    if principal == executor:
        error(errors, f"{role} principal must not be the automation executor")
    timestamp(record.get("timestamp"), f"{role} timestamp", errors)
    if record.get("reviewed_commit") != reviewed_commit:
        error(errors, f"{role} reviewed commit is not bound to the requested commit")
    for record_key, review_key, evidence_key in (
        ("reviewed_plan_manifest_sha256", "reviewed_plan_manifest_sha256", "active_plan_manifest_sha256"),
        ("reviewed_evidence_manifest_sha256", "reviewed_evidence_manifest_sha256", "evidence_manifest_sha256"),
        ("asvs_reference_sha256", "asvs_reference_sha256", "asvs_reference_sha256"),
    ):
        value = digest(record.get(record_key), f"{role} {record_key}", errors)
        if value is not None and (review.get(review_key) not in (None, value) or value != evidence.get(evidence_key)):
            error(errors, f"{role} {record_key} is not bound to the review and evidence")
    required_string(record.get("determination"), f"{role} determination", errors)
    required_string(record.get("rationale"), f"{role} rationale", errors)
    return record


def validate_real_bindings(
    security_path: Path,
    evidence_path: Path,
    evidence: Mapping[str, Any],
    reviewed_commit: str,
    errors: list[str],
) -> None:
    """Recompute local immutable bindings outside isolated fixture tests."""
    plan_path = ROOT / ".planning/phases/01-research-and-truth-baseline/01-REVIEWS.md"
    expected_plan_path = ".planning/phases/01-research-and-truth-baseline/01-REVIEWS.md"
    if evidence.get("active_plan_review_path") != expected_plan_path:
        error(errors, "evidence must bind the canonical active plan review path")
    elif not plan_path.is_file() or plan_path.is_symlink():
        error(errors, "canonical active plan review is unavailable as a regular file")
    elif evidence.get("active_plan_manifest_sha256") != hashlib.sha256(plan_path.read_bytes()).hexdigest():
        error(errors, "active plan manifest digest differs from current 01-REVIEWS.md")
    if evidence.get("evidence_manifest_sha256") != canonical_digest(evidence, "evidence_manifest_sha256"):
        error(errors, "evidence manifest digest does not match its canonical content")
    plan_file = ".planning/phases/01-research-and-truth-baseline/01-39-PLAN.md"
    current_plan = ROOT / plan_file
    try:
        reviewed_plan = subprocess.check_output(["git", "show", f"{reviewed_commit}:{plan_file}"], cwd=ROOT)
    except (OSError, subprocess.CalledProcessError):
        error(errors, "reviewed commit cannot supply the bound 01-39 plan bytes")
    else:
        if not current_plan.is_file() or reviewed_plan != current_plan.read_bytes():
            error(errors, "reviewed commit does not contain the current bound 01-39 plan bytes")
    if evidence.get("reviewed_commit") != reviewed_commit:
        error(errors, "evidence reviewed_commit differs from the requested reviewed commit")
    if not security_path.is_file() or not evidence_path.is_file():
        error(errors, "security and evidence artifacts must be regular files")


def validate(security_path: Path, evidence_path: Path, matrix_path: Path, reviewed_commit: str, fixture_mode: bool) -> list[str]:
    errors: list[str] = []
    if reviewed_commit == "HEAD":
        try:
            reviewed_commit = subprocess.check_output(
                ["git", "rev-parse", "--verify", "HEAD^{commit}"], cwd=ROOT, text=True
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            error(errors, "--reviewed-commit HEAD could not resolve to a Git commit")
            return errors
    if re.fullmatch(r"[0-9a-f]{40}", reviewed_commit) is None:
        error(errors, "--reviewed-commit must be HEAD or a 40-character Git commit")
        return errors
    executor = os.environ.get("GSD_EXECUTOR_ID", "")
    if not executor:
        error(errors, "GSD_EXECUTOR_ID is required")
        return errors
    review = load_frontmatter(security_path, errors)
    evidence = load_yaml(evidence_path, "security evidence", errors)
    matrix = load_yaml(matrix_path, "ASVS matrix", errors)
    if review is None or evidence is None or matrix is None:
        return errors
    applicable_controls = validate_matrix(matrix, errors)
    evidence_findings = finding_map(evidence.get("findings"), applicable_controls, errors, "evidence")
    review_findings = finding_map(review.get("findings"), applicable_controls, errors, "review")
    for key in ("reviewed_commit", "active_plan_manifest_sha256", "evidence_manifest_sha256", "asvs_reference_sha256"):
        value = evidence.get(key)
        if key == "reviewed_commit":
            required_string(value, f"evidence {key}", errors)
        else:
            digest(value, f"evidence {key}", errors)
    if evidence.get("reviewed_commit") != reviewed_commit:
        error(errors, "evidence reviewed_commit is not the requested reviewed commit")
    for finding_id in REQUIRED_FINDINGS:
        if finding_id in evidence_findings and finding_id in review_findings:
            evidence_binding = {key: evidence_findings[finding_id].get(key) for key in BOUND_FINDING_FIELDS}
            review_binding = {key: review_findings[finding_id].get(key) for key in BOUND_FINDING_FIELDS}
            if evidence_binding != review_binding:
                error(errors, f"{finding_id} review evidence does not exactly match the remediation dossier")
    if review.get("asvs_level") != "L1":
        error(errors, "security review must declare asvs_level L1")
    if review.get("blocking_threshold") != "high":
        error(errors, "security review must declare high blocking threshold")
    review_date(review.get("review_date"), errors)
    required_string(review.get("scope"), "scope", errors)
    commits = review.get("reviewed_commits")
    if not isinstance(commits, list) or reviewed_commit not in commits or any(not isinstance(item, str) for item in commits):
        error(errors, "reviewed_commits must include the requested reviewed commit")
    for key, evidence_key in (
        ("reviewed_plan_manifest_sha256", "active_plan_manifest_sha256"),
        ("reviewed_evidence_manifest_sha256", "evidence_manifest_sha256"),
    ):
        value = digest(review.get(key), key, errors)
        if value is not None and value != evidence.get(evidence_key):
            error(errors, f"{key} differs from the bound evidence")
    auditor = validate_role(review.get("securityAuditor"), "securityAuditor", review, evidence, reviewed_commit, executor, errors)
    rechecker = validate_role(review.get("securityRechecker"), "securityRechecker", review, evidence, reviewed_commit, executor, errors)
    if auditor is not None and rechecker is not None and json.dumps(auditor, sort_keys=True) == json.dumps(rechecker, sort_keys=True):
        error(errors, "securityAuditor and securityRechecker must be separate role-bound records")
    status = review.get("status")
    open_high_count = review.get("open_high_count")
    if not isinstance(open_high_count, int) or isinstance(open_high_count, bool) or open_high_count < 0:
        error(errors, "open_high_count must be a nonnegative integer")
    unresolved_high = [
        finding_id for finding_id, finding in review_findings.items()
        if str(finding.get("severity", "")).lower() == "high" and finding.get("disposition") != "mitigated"
    ]
    if status == "passed":
        if open_high_count != 0:
            error(errors, "passed review requires open_high_count: 0")
        if unresolved_high:
            error(errors, "passed review cannot retain unresolved HIGH findings")
        missing_mitigations = [
            finding_id for finding_id in REQUIRED_FINDINGS
            if review_findings.get(finding_id, {}).get("disposition") != "mitigated"
        ]
        if missing_mitigations:
            error(errors, "passed review requires every required CR/WR finding to be mitigated")
    if not fixture_mode:
        validate_real_bindings(security_path, evidence_path, evidence, reviewed_commit, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a human-authored Phase 1 ASVS L1 security review.")
    parser.add_argument("--security", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--asvs-matrix", type=Path, required=True)
    parser.add_argument("--reviewed-commit", required=True)
    parser.add_argument("--fixture-mode", action="store_true", help="Skip repository bindings for isolated unit fixtures.")
    args = parser.parse_args()
    errors = validate(args.security, args.evidence, args.asvs_matrix, args.reviewed_commit, args.fixture_mode)
    for message in errors:
        print(message)
    if errors:
        return 1
    print("Phase 1 security review validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
