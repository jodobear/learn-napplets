"""Executable Nyquist edge probes for Phase 1 closeout evidence."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
PLANNING = ROOT / ".planning"
VALIDATOR = ROOT / "tools" / "validate-research.py"
DIMENSIONS = (
    "normativeProtocol",
    "observedImplementation",
    "publishedPackage",
    "runtime",
    "exampleFixture",
    "currentWork",
    "conformance",
)


def load_research_validator():
    spec = importlib.util.spec_from_file_location("phase1_gap_closeout_validator", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def complete_governance() -> dict:
    signoffs = {
        name: {"status": "pending"}
        for name in ("product", "protocolTechnical", "security", "accessibility", "contentLearning", "release")
    }
    return {
        "schemaVersion": 1,
        "id": "PGV-GAP-CLOSEOUT-001",
        "kind": "phase-governance",
        "phase": "01",
        "owner": "research-owner",
        "requiredApprover": "protocol-technical-owner",
        "requirements": ["OPER-03", "EVID-03"],
        "exitEvidence": [
            {
                "id": "SPK-GAP-CLOSEOUT-001",
                "measure": "retained local fixture",
                "expected": "blocked or complete evidence",
                "actual": "fixture retained",
                "path": ".planning/spikes/spk-a-workspace/report.md",
            }
        ],
        "verification": {
            "gsdState": "blocked",
            "validatedAt": "2026-07-31T00:00:00Z",
            "validator": "tools/validate-research.py validate-governance",
        },
        "approval": {"status": "pending"},
        "signoffs": signoffs,
        "authorityDeterminations": [
            {
                "scopeId": "CAND-GAP-CLOSEOUT-001",
                "candidateId": "CAND-GAP-CLOSEOUT-001",
                "authorityArtifactPath": ".planning/research/authority-determinations.yaml",
                "authorityArtifactSha256": "a" * 64,
                "acquisitionReceiptPath": ".planning/research/reports/upstream-acquisition-20260728.md",
                "acquisitionReceiptSha256": "b" * 64,
                "determinationIds": [
                    "AUTH-GAP-PRODUCT",
                    "AUTH-GAP-PROTOCOL",
                    "AUTH-GAP-SECURITY",
                    "AUTH-GAP-ACCESSIBILITY",
                    "AUTH-GAP-CONTENT",
                    "AUTH-GAP-RELEASE",
                ],
                "reviewedSourceInputBinding": {"parserVersion": "fixture-v1"},
            }
        ],
        "blockers": [],
        "phaseResult": "blocked",
    }


class GapCloseoutTests(unittest.TestCase):
    def compatibility_snapshot(self, validator) -> dict[str, bytes]:
        return {
            relative: (PLANNING / relative).read_bytes()
            for relative in validator.COMPATIBILITY_SNAPSHOT_TARGETS
        }

    def qualified_compatibility_snapshot(self, validator) -> dict[str, bytes]:
        snapshot = self.compatibility_snapshot(validator)
        registry = yaml.safe_load(snapshot["research/source-registry.yaml"])
        matrix = yaml.safe_load(snapshot["research/compatibility-matrix.yaml"])
        sources = registry["sources"]
        dimension_sources = {
            "normativeProtocol": ("SRC-NORMATIVE-QUALIFIED", "normative-protocol", "official-normative"),
            "observedImplementation": ("SRC-OBSERVED-QUALIFIED", "observed-implementation", "official-repository-observation"),
            "runtime": ("SRC-RUNTIME-QUALIFIED", "runtime-measurement", "independent-runtime-measurement"),
            "exampleFixture": ("SRC-FIXTURE-QUALIFIED", "example-fixture", "reproducible-fixture"),
            "currentWork": ("SRC-CURRENT-WORK-QUALIFIED", "observed-implementation", "official-repository-observation"),
        }
        for source_id, raw_origin, authority_tier in dimension_sources.values():
            sources.append(
                {
                    "id": source_id,
                    "collectionStatus": "collected",
                    "rawOrigin": raw_origin,
                    "authorityTier": authority_tier,
                    "review": {"status": "approved"},
                    "freshness": {"state": "current"},
                }
            )
        baseline = next(record for record in matrix["compatibility"] if record["id"] == "CMP-BASELINE-001")
        for dimension in baseline["dimensions"]:
            dimension["status"] = "qualified"
            if dimension["name"] in dimension_sources:
                dimension["references"] = [{"id": dimension_sources[dimension["name"]][0]}]
            elif dimension["name"] == "publishedPackage":
                dimension["references"] = [{"id": "SRC-NORMATIVE-QUALIFIED"}]
            elif dimension["name"] == "conformance":
                dimension["references"] = [{"id": "SRC-OBSERVED-QUALIFIED"}]
        baseline["baselineEligibility"] = {
            "status": "eligible",
            "approval": "approved",
            "reviewRecordId": "APR-GAP-CLOSEOUT-001",
        }
        package = yaml.safe_load(snapshot["research/package-evidence.yaml"])
        package["approval"] = "approved"
        package["artifactEvidence"] = {"status": "qualified"}
        metadata = yaml.safe_load(snapshot["spikes/spk-g-package-conformance/metadata.yaml"])
        metadata["status"] = "complete"
        snapshot["research/source-registry.yaml"] = yaml.safe_dump(registry, sort_keys=False).encode("utf-8")
        snapshot["research/compatibility-matrix.yaml"] = yaml.safe_dump(matrix, sort_keys=False).encode("utf-8")
        snapshot["research/package-evidence.yaml"] = yaml.safe_dump(package, sort_keys=False).encode("utf-8")
        snapshot["spikes/spk-g-package-conformance/metadata.yaml"] = yaml.safe_dump(metadata, sort_keys=False).encode("utf-8")
        snapshot["spikes/spk-g-package-conformance/report.md"] = b"# Conformance fixture\n"
        return snapshot

    def test_compatibility_completeness_requires_qualified_dimensions_without_approval(self) -> None:
        validator = load_research_validator()
        complete = self.qualified_compatibility_snapshot(validator)
        qualified = validator.evaluate_compatibility_baseline(
            validator.build_compatibility_snapshot_index(complete)
        )
        self.assertEqual(qualified["status"], "eligible")
        self.assertEqual(qualified["approval"], "approved")
        self.assertFalse(qualified["architectureApproved"])

        for dimension_name in DIMENSIONS:
            with self.subTest(dimension=dimension_name):
                mutated = dict(complete)
                matrix = yaml.safe_load(mutated["research/compatibility-matrix.yaml"])
                baseline = matrix["compatibility"][0]
                dimension = next(item for item in baseline["dimensions"] if item["name"] == dimension_name)
                if dimension_name == "publishedPackage":
                    package = yaml.safe_load(mutated["research/package-evidence.yaml"])
                    package["artifactEvidence"] = {"status": "blocked"}
                    mutated["research/package-evidence.yaml"] = yaml.safe_dump(package, sort_keys=False).encode("utf-8")
                elif dimension_name == "conformance":
                    metadata = yaml.safe_load(mutated["spikes/spk-g-package-conformance/metadata.yaml"])
                    metadata["status"] = "blocked"
                    mutated["spikes/spk-g-package-conformance/metadata.yaml"] = yaml.safe_dump(metadata, sort_keys=False).encode("utf-8")
                else:
                    dimension["references"] = []
                mutated["research/compatibility-matrix.yaml"] = yaml.safe_dump(matrix, sort_keys=False).encode("utf-8")
                result = validator.evaluate_compatibility_baseline(
                    validator.build_compatibility_snapshot_index(mutated)
                )
                token = validator.dimension_reason_token(dimension_name)
                self.assertEqual(result["status"], "blocked")
                self.assertEqual(result["approval"], "not-approved")
                self.assertFalse(result["architectureApproved"])
                self.assertTrue(
                    any(reason.startswith(f"DIMENSION_{token}_") for reason in result["reasons"]),
                    result,
                )

    def test_mandatory_spike_completeness_requires_retained_evidence_without_approval(self) -> None:
        validator = load_research_validator()
        manifest = yaml.safe_load((PLANNING / "spikes/replay-manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual([entry["spikeId"] for entry in manifest["entries"]], [f"SPK-{letter}" for letter in "ABCDEFGHIJKL"])
        with tempfile.TemporaryDirectory() as temporary:
            copied_planning = Path(temporary) / ".planning"
            copied_spikes = copied_planning / "spikes"
            copied_spikes.mkdir(parents=True)
            copied_manifest = copied_spikes / "replay-manifest.yaml"
            copied_manifest.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
            for entry in manifest["entries"]:
                source_directory = PLANNING / entry["report"]["path"]
                source_directory = source_directory.parent
                shutil.copytree(source_directory, copied_spikes / source_directory.name)
                for evidence_name in ("report", "metadata", "measurement"):
                    evidence = entry[evidence_name]
                    retained = copied_planning / evidence["path"]
                    self.assertTrue(retained.is_file(), evidence)
                metadata = yaml.safe_load((copied_spikes / source_directory.name / "metadata.yaml").read_text(encoding="utf-8"))
                self.assertTrue(metadata.get("rawOutputDigests"), entry["spikeId"])
                self.assertTrue(metadata.get("evidenceLinks"), entry["spikeId"])
                self.assertTrue(metadata.get("replayResult", {}).get("outputDigest"), entry["spikeId"])
                self.assertEqual(
                    validator.validate_spike(copied_spikes / source_directory.name, "complete"),
                    [],
                    entry["spikeId"],
                )
            self.assertEqual(validator.validate_replay_manifest(copied_manifest, copied_planning), [])
            mutated = yaml.safe_load(copied_manifest.read_text(encoding="utf-8"))
            mutated["entries"][0]["report"]["sha256"] = "0" * 64
            copied_manifest.write_text(yaml.safe_dump(mutated, sort_keys=False), encoding="utf-8")
            errors = validator.validate_replay_manifest(copied_manifest, copied_planning)
            self.assertEqual(len(errors), 2, errors)
            self.assertTrue(errors[0].startswith("ERROR RPL005: SPK-A report"), errors)
            self.assertTrue(errors[1].startswith("ERROR RPL007: SPK-A fixture evidence"), errors)
            self.assertNotIn("approved", " ".join(errors).lower())

    def test_governance_role_adjacency_requires_independence(self) -> None:
        validator = load_research_validator()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "governance.yaml"
            independent = complete_governance()
            path.write_text(yaml.safe_dump(independent, sort_keys=False), encoding="utf-8")
            self.assertEqual(validator.validate_governance(path), [])
            aliased = copy.deepcopy(independent)
            aliased["requiredApprover"] = aliased["owner"]
            path.write_text(yaml.safe_dump(aliased, sort_keys=False), encoding="utf-8")
            self.assertEqual(
                validator.validate_governance(path),
                ["ERROR GOV003: responsible owner and required approver must be separate roles"],
            )

    def test_governance_empty_null_single_required_fields_fail(self) -> None:
        validator = load_research_validator()
        cases = {
            "empty-owner": lambda record: record.__setitem__("owner", ""),
            "null-approver": lambda record: record.__setitem__("requiredApprover", None),
            "empty-requirements": lambda record: record.__setitem__("requirements", []),
            "null-exit-evidence": lambda record: record.__setitem__("exitEvidence", None),
            "single-signoff": lambda record: record.__setitem__("signoffs", {"product": {"status": "pending"}}),
            "single-exit-field": lambda record: record.__setitem__("exitEvidence", [{"id": "SPK-GAP-CLOSEOUT-001"}]),
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "governance.yaml"
            for name, mutate in cases.items():
                with self.subTest(name=name):
                    record = complete_governance()
                    mutate(record)
                    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
                    errors = validator.validate_governance(path)
                    self.assertTrue(errors, name)
                    self.assertTrue(all(error.startswith("ERROR ") for error in errors), errors)

    def test_governance_ordering_is_stable(self) -> None:
        validator = load_research_validator()
        expected = ["ERROR GOV003: responsible owner and required approver must be separate roles"]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "governance.yaml"
            for requirements in (("EVID-03", "OPER-03"), ("OPER-03", "EVID-03")):
                for signoff_names in (
                    ("product", "protocolTechnical", "security", "accessibility", "contentLearning", "release"),
                    ("release", "contentLearning", "accessibility", "security", "protocolTechnical", "product"),
                ):
                    record = complete_governance()
                    record["requirements"] = list(requirements)
                    record["signoffs"] = {name: {"status": "pending"} for name in signoff_names}
                    record["requiredApprover"] = record["owner"]
                    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
                    self.assertEqual(validator.validate_governance(path), expected)


CANONICAL_PROBES = {
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


def json_section(markdown: str, heading: str) -> object:
    marker = f"## {heading}\n\n```json\n"
    start = markdown.find(marker)
    if start < 0:
        raise ValueError(f"missing JSON section: {heading}")
    payload_start = start + len(marker)
    payload_end = markdown.find("\n```", payload_start)
    if payload_end < 0:
        raise ValueError(f"unterminated JSON section: {heading}")
    return json.loads(markdown[payload_start:payload_end])


def normalized_payload(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def replace_json_section(markdown: str, heading: str, value: object) -> str:
    marker = f"## {heading}\n\n```json\n"
    start = markdown.index(marker) + len(marker)
    end = markdown.index("\n```", start)
    return markdown[:start] + normalized_payload(value) + markdown[end:]


def direct_payload(ledger: dict) -> dict:
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise ValueError("DIR001: canonical ledger attempts must be a list")
    return {
        "ledgerId": ledger.get("ledgerId"),
        "closureBoundary": ledger.get("closureBoundary"),
        "attempts": sorted(attempts, key=lambda item: item.get("attemptId", "")),
    }


def direct_digest(ledger: dict) -> str:
    import hashlib

    return hashlib.sha256(normalized_payload(direct_payload(ledger)).encode("utf-8")).hexdigest()


def post_closure_digest(batch: dict) -> str:
    import hashlib

    payload = {
        "batchId": batch.get("batchId"),
        "ledgerId": batch.get("ledgerId"),
        "preClosureLedgerSha256": batch.get("preClosureLedgerSha256"),
        "timestamp": batch.get("timestamp"),
        "runs": sorted(batch.get("runs", []), key=lambda item: item.get("runId", "")),
    }
    return hashlib.sha256(normalized_payload(payload).encode("utf-8")).hexdigest()


def validation_contract_errors(validation_text: str, post_closure_text: str) -> list[str]:
    errors: list[str] = []
    try:
        ledger = json_section(validation_text, "Canonical Direct-Attempt Ledger")
        matrix = json_section(validation_text, "Canonical Probe Matrix")
        closure = json_section(validation_text, "Ledger Closure")
        post_closure = json_section(post_closure_text, "Retained Post-Closure Batches")
    except (ValueError, json.JSONDecodeError) as exc:
        return [f"DOC001: {exc}"]
    if not isinstance(ledger, dict) or ledger.get("ledgerId") != "P1-38-NYQUIST-DIRECT-14":
        errors.append("DIR002: canonical ledger ID must be P1-38-NYQUIST-DIRECT-14")
        return errors
    if ledger.get("closureBoundary") != "after fourteen direct rows and before post-closure verification":
        errors.append("DIR003: canonical ledger closure boundary is missing or changed")
    if not isinstance(ledger.get("executorIdentity"), str) or not ledger["executorIdentity"]:
        errors.append("DIR004: canonical ledger requires nonempty executor identity")
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        return [*errors, "DIR005: canonical ledger attempts are missing"]
    if len(attempts) != 14:
        errors.append("DIR006: canonical ledger must contain exactly fourteen direct attempts")
    attempt_ids = [item.get("attemptId") for item in attempts if isinstance(item, dict)]
    probe_ids = [item.get("probeId") for item in attempts if isinstance(item, dict)]
    if len(attempt_ids) != len(set(attempt_ids)):
        errors.append("DIR007: canonical direct attempt IDs must be unique")
    if set(probe_ids) != set(CANONICAL_PROBES):
        errors.append("DIR008: canonical direct attempts must cover each required probe exactly once")
    attempts_by_probe = {item.get("probeId"): item for item in attempts if isinstance(item, dict)}
    for probe_id, expected_test in CANONICAL_PROBES.items():
        attempt = attempts_by_probe.get(probe_id)
        if not isinstance(attempt, dict):
            continue
        if attempt.get("attemptId") != f"P1-38-DIRECT-{probe_id}":
            errors.append(f"DIR009: {probe_id} has an invalid direct attempt ID")
        if attempt.get("role") != "direct":
            errors.append(f"DIR010: {probe_id} canonical evidence must use a direct attempt")
        expected_argv = ["tools/phase1-python", "-m", "unittest", expected_test]
        if attempt.get("argv") != expected_argv or attempt.get("environment") != {"PYTHONPATH": "tests/phase1"}:
            errors.append(f"DIR011: {probe_id} direct attempt argv is not designated wrapper argv")
        if attempt.get("exit") != 0:
            errors.append(f"DIR012: {probe_id} canonical direct attempt did not exit zero")
        if not isinstance(attempt.get("compactResult"), str) or not attempt["compactResult"]:
            errors.append(f"DIR013: {probe_id} canonical direct attempt lacks compact result evidence")
        expected_locator = f"01-VALIDATION.md#direct-attempt-p1-38-direct-{probe_id.lower()}"
        if attempt.get("evidenceLocator") != expected_locator:
            errors.append(f"DIR014: {probe_id} direct attempt evidence locator is invalid")
    if not isinstance(matrix, list) or len(matrix) != 14:
        errors.append("MAT001: canonical probe matrix must contain exactly fourteen rows")
    else:
        matrix_probe_ids = [item.get("probeId") for item in matrix if isinstance(item, dict)]
        if set(matrix_probe_ids) != set(CANONICAL_PROBES) or len(matrix_probe_ids) != len(set(matrix_probe_ids)):
            errors.append("MAT002: canonical probe matrix must select every required probe exactly once")
        for row in matrix:
            if not isinstance(row, dict):
                errors.append("MAT003: canonical probe matrix row must be an object")
                continue
            probe_id = row.get("probeId")
            attempt = attempts_by_probe.get(probe_id)
            if not isinstance(attempt, dict) or row.get("directAttemptId") != attempt.get("attemptId"):
                errors.append(f"MAT004: {probe_id} matrix row does not select its direct attempt")
            elif row.get("evidenceLocator") != attempt.get("evidenceLocator"):
                errors.append(f"MAT005: {probe_id} matrix evidence locator differs from its direct attempt")
            elif row.get("namedTest") != CANONICAL_PROBES.get(probe_id):
                errors.append(f"MAT006: {probe_id} matrix named test is not designated")
    if not isinstance(closure, dict) or closure.get("ledgerId") != ledger.get("ledgerId") or not closure.get("closedAt"):
        errors.append("CLS001: canonical ledger closure marker is missing")
    elif closure.get("preClosureLedgerSha256") != direct_digest(ledger):
        errors.append("CLS002: closed direct-attempt payload digest differs")
    if not isinstance(post_closure, dict) or not isinstance(post_closure.get("batches"), list) or not post_closure["batches"]:
        errors.append("POST001: post-closure verification requires retained batches")
    else:
        batch_ids: set[str] = set()
        for batch in post_closure["batches"]:
            if not isinstance(batch, dict):
                errors.append("POST002: retained batch must be an object")
                continue
            batch_id = batch.get("batchId")
            if not isinstance(batch_id, str) or not batch_id or batch_id in batch_ids:
                errors.append("POST003: retained post-closure batches require unique IDs")
            batch_ids.add(batch_id)
            if batch.get("ledgerId") != ledger.get("ledgerId") or batch.get("preClosureLedgerSha256") != closure.get("preClosureLedgerSha256"):
                errors.append("POST004: post-closure batch is not bound to the closed ledger digest")
            if batch.get("batchPayloadSha256") != post_closure_digest(batch):
                errors.append("POST005: retained post-closure batch payload digest differs")
            runs = batch.get("runs")
            if not isinstance(runs, list) or not runs:
                errors.append("POST006: retained post-closure batch requires identified runs")
            elif any(
                not isinstance(run, dict)
                or not isinstance(run.get("runId"), str)
                or run.get("argv", [None])[0] != "tools/phase1-python"
                or run.get("exit") != 0
                or not run.get("resultDigest")
                or not run.get("evidenceLocator")
                for run in runs
            ):
                errors.append("POST007: retained post-closure run is incomplete or not wrapper-bound")
            if "canonicalProbeMatrix" in batch or "attempts" in batch:
                errors.append("POST008: post-closure verification must not change the closed canonical matrix")
    return errors


class ValidationLedgerTests(unittest.TestCase):
    def test_validation_probe_attempt_ledger_is_canonical_and_complete(self) -> None:
        validation = PLANNING / "phases/01-research-and-truth-baseline/01-VALIDATION.md"
        post_closure = PLANNING / "phases/01-research-and-truth-baseline/01-POST-CLOSURE-VERIFICATION.md"
        errors = validation_contract_errors(validation.read_text(encoding="utf-8"), post_closure.read_text(encoding="utf-8"))
        self.assertEqual(errors, [], errors)

        canonical = json_section(validation.read_text(encoding="utf-8"), "Canonical Direct-Attempt Ledger")
        for mutation, diagnostic in (
            (lambda ledger: ledger["attempts"].pop(), "DIR006"),
            (lambda ledger: ledger["attempts"].append(copy.deepcopy(ledger["attempts"][0])), "DIR006"),
            (lambda ledger: ledger["attempts"][0].__setitem__("role", "post-closure"), "DIR010"),
            (lambda ledger: ledger["attempts"][0].__setitem__("argv", ["python", "-m", "unittest"]), "DIR011"),
            (lambda ledger: ledger["attempts"][0].__setitem__("exit", 1), "DIR012"),
        ):
            with self.subTest(diagnostic=diagnostic):
                changed = copy.deepcopy(canonical)
                mutation(changed)
                document = replace_json_section(
                    validation.read_text(encoding="utf-8"), "Canonical Direct-Attempt Ledger", changed
                )
                errors = validation_contract_errors(document, post_closure.read_text(encoding="utf-8"))
                self.assertTrue(any(error.startswith(diagnostic) for error in errors), errors)

    def test_validation_probe_attempt_ledger_is_closed_before_post_closure_verification(self) -> None:
        validation = PLANNING / "phases/01-research-and-truth-baseline/01-VALIDATION.md"
        post_closure = PLANNING / "phases/01-research-and-truth-baseline/01-POST-CLOSURE-VERIFICATION.md"
        validation_text = validation.read_text(encoding="utf-8")
        post_text = post_closure.read_text(encoding="utf-8")
        self.assertEqual(validation_contract_errors(validation_text, post_text), [])

        closure = json_section(validation_text, "Ledger Closure")
        changed_closure = copy.deepcopy(closure)
        changed_closure["preClosureLedgerSha256"] = "0" * 64
        malformed_closure = replace_json_section(validation_text, "Ledger Closure", changed_closure)
        self.assertTrue(any(error.startswith("CLS002") for error in validation_contract_errors(malformed_closure, post_text)))

        batches = json_section(post_text, "Retained Post-Closure Batches")
        changed_batches = copy.deepcopy(batches)
        changed_batches["batches"][0]["preClosureLedgerSha256"] = "0" * 64
        changed_batches["batches"][0]["batchPayloadSha256"] = post_closure_digest(changed_batches["batches"][0])
        malformed_binding = replace_json_section(post_text, "Retained Post-Closure Batches", changed_batches)
        self.assertTrue(any(error.startswith("POST004") for error in validation_contract_errors(validation_text, malformed_binding)))

        changed_matrix = copy.deepcopy(batches)
        changed_matrix["batches"][0]["canonicalProbeMatrix"] = []
        changed_matrix["batches"][0]["batchPayloadSha256"] = post_closure_digest(changed_matrix["batches"][0])
        malformed_matrix = replace_json_section(post_text, "Retained Post-Closure Batches", changed_matrix)
        self.assertTrue(any(error.startswith("POST008") for error in validation_contract_errors(validation_text, malformed_matrix)))

        repeated = copy.deepcopy(batches)
        second = copy.deepcopy(repeated["batches"][0])
        second["batchId"] = "P1-38-POST-REPLAY"
        second["timestamp"] = "2026-07-31T00:00:01Z"
        second["runs"][0]["runId"] = "P1-38-POST-REPLAY-RUN-01"
        second["batchPayloadSha256"] = post_closure_digest(second)
        repeated["batches"].append(second)
        repeated_text = replace_json_section(post_text, "Retained Post-Closure Batches", repeated)
        self.assertEqual(validation_contract_errors(validation_text, repeated_text), [])


if __name__ == "__main__":
    unittest.main()
