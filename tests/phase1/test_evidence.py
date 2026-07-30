"""Evidence-record validation tests for the Phase 1 source tracer."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate-research.py"
SOURCE_SCHEMA = ROOT / ".planning" / "research" / "schemas" / "source.schema.json"
CLAIM_SCHEMA = ROOT / ".planning" / "research" / "schemas" / "claim.schema.json"

VALID_SOURCE = {
    "id": "SRC-POLICY-001",
    "kind": "source",
    "collectionStatus": "seed",
    "rawOrigin": "project-policy",
    "repository": "learn-napplets",
    "officialUrl": "https://example.invalid/learn-napplets",
    "immutableUrl": "https://example.invalid/learn-napplets/blob/0123456789abcdef0123456789abcdef01234567/.planning/governance/evidence-policy.md",
    "ref": "0123456789abcdef0123456789abcdef01234567",
    "commitSha": "0123456789abcdef0123456789abcdef01234567",
    "path": ".planning/governance/evidence-policy.md",
    "locator": "Required fields",
    "contentSha256": "a" * 64,
    "retrievedAt": "2026-07-24T00:00:00Z",
    "authorityTier": "project-policy",
    "evidenceClass": "project-policy",
    "maturity": "accepted",
    "uncertainty": {"state": "limited", "reason": "Collection seed; not upstream proof."},
    "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
    "freshness": {"state": "provisional", "refreshTrigger": "Policy revision or digest change"},
    "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]},
}


class SourceEvidenceValidationTests(unittest.TestCase):
    def run_validator(self, research_root: Path, report: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "validate", "--root", str(research_root), "--report", str(report)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_root(self, record: dict, duplicate: bool = False) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "research"
        (root / "schemas").mkdir(parents=True)
        shutil.copy2(SOURCE_SCHEMA, root / "schemas" / "source.schema.json")
        records = [record, copy.deepcopy(record)] if duplicate else [record]
        if duplicate:
            records[1]["id"] = record["id"]
        (root / "source-registry.yaml").write_text(
            "schemaVersion: 1\nsources:\n" + "".join(
                "  - " + "\n    ".join(f"{key}: {value}" for key, value in item.items()) + "\n"
                for item in records
            )
        )
        return root, temp

    def test_complete_source_record_produces_deterministic_review_report(self) -> None:
        root, temp = self.write_root(copy.deepcopy(VALID_SOURCE))
        with temp:
            report = root / "reports" / "validation.md"
            result = self.run_validator(root, report)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("SRC-POLICY-001", report.read_text())
            self.assertIn("valid", report.read_text())

    def test_incomplete_source_record_is_rejected(self) -> None:
        record = copy.deepcopy(VALID_SOURCE)
        del record["commitSha"]
        root, temp = self.write_root(record)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("commitSha", result.stdout)

    def test_duplicate_stable_ids_are_rejected(self) -> None:
        root, temp = self.write_root(copy.deepcopy(VALID_SOURCE), duplicate=True)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ERROR SEM001: duplicate record ID SRC-POLICY-001", result.stdout)

    def test_evidence_validation_uses_temporary_report_without_canonical_mutation(self) -> None:
        canonical_report = ROOT / ".planning" / "research" / "reports" / "validation.md"
        before = canonical_report.read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "validation.md"
            result = self.run_validator(ROOT / ".planning" / "research", report)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("Traceability mappings: valid", report.read_text())
        self.assertEqual(canonical_report.read_bytes(), before)

    def write_claim_root(self, claim: dict) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
        root, temp = self.write_root(copy.deepcopy(VALID_SOURCE))
        shutil.copy2(CLAIM_SCHEMA, root / "schemas" / "claim.schema.json")
        (root / "claims.yaml").write_text("schemaVersion: 1\nclaims:\n  - " + "\n    ".join(
            f"{key}: {value}" for key, value in claim.items()
        ) + "\n")
        return root, temp

    def test_valid_source_linked_provisional_claim_passes(self) -> None:
        claim = {
            "id": "CLM-POLICY-001", "kind": "claim", "statement": "A project-policy seed requires review.",
            "rawOrigin": "project-policy", "assertionKind": "project-policy", "evidenceClass": "project-policy",
            "maturity": "accepted", "state": "provisional", "stateReason": "Awaiting technical review.",
            "uncertainty": {"state": "limited", "reason": "Policy seed."},
            "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
            "sourceRelations": [{"sourceId": "SRC-POLICY-001", "relation": "supports", "role": "primary", "locator": "Required fields", "excerptSha256": "b" * 64}],
            "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]}, "blocking": False,
        }
        root, temp = self.write_claim_root(claim)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_blocking_claim_requires_distinct_corroboration(self) -> None:
        claim = {
            "id": "CLM-POLICY-003", "kind": "claim", "statement": "Blocking evidence requires independent corroboration.",
            "rawOrigin": "project-policy", "assertionKind": "project-policy", "evidenceClass": "project-policy",
            "maturity": "accepted", "state": "blocked", "stateReason": "Corroboration is unavailable.",
            "uncertainty": {"state": "material", "reason": "One source only."}, "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
            "sourceRelations": [
                {"sourceId": "SRC-POLICY-001", "relation": "supports", "role": "primary", "locator": "Required fields", "excerptSha256": "b" * 64},
                {"sourceId": "SRC-POLICY-001", "relation": "supports", "role": "independent-corroboration", "locator": "Required fields", "excerptSha256": "b" * 64},
            ],
            "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]}, "blocking": True,
            "blockedDetails": {"scope": "This claim only.", "safeFallback": "Defer it.", "approver": "project-owner", "date": "2026-07-24", "revisitCriterion": "A distinct source is available."},
        }
        root, temp = self.write_claim_root(claim)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires distinct primary and independent corroborating sources", result.stdout)

    def test_claim_semantic_failures_are_rejected(self) -> None:
        claim = {
            "id": "CLM-POLICY-002", "kind": "claim", "statement": "An invalid claim must be rejected.",
            "rawOrigin": "inference", "assertionKind": "inference", "evidenceClass": "inference", "maturity": "unknown",
            "state": "verified", "stateReason": "Automation-only transition.",
            "uncertainty": {"state": "material", "reason": "No review."}, "impacts": {"requirements": ["EVID-01"], "phases": ["01"]},
            "sourceRelations": [{"sourceId": "SRC-MISSING-001", "relation": "invented", "role": "primary", "locator": "none", "excerptSha256": "b" * 64}],
            "review": {"owner": "research-owner", "status": "pending", "requiredRoles": ["protocol-technical"]}, "blocking": False,
        }
        root, temp = self.write_claim_root(claim)
        with temp:
            result = self.run_validator(root, root / "report.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("references unknown source SRC-MISSING-001", result.stdout)
            self.assertIn("cannot be verified without reviewer approval evidence", result.stdout)


class BoundedCollectorTests(unittest.TestCase):
    def test_collector_rejects_non_allowlisted_url_without_writing(self) -> None:
        collector = ROOT / "tools" / "acquire-sources.py"
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary) / "cache"
            result = subprocess.run(
                [sys.executable, str(collector), "--validate-url", "https://example.invalid/not-allowed", "--cache-root", str(cache)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not allowlisted", result.stderr)
            self.assertFalse(cache.exists())


class BoundedCollectorTests(unittest.TestCase):
    """Exercise the fixture-only source-ingress boundary without live HTTPS."""

    COLLECTOR = ROOT / "tools" / "acquire-sources.py"
    REPORT_PATHS = (
        ".planning/research/reports/upstream-refresh-kehto-web-2026-07-28.md",
        ".planning/research/reports/upstream-refresh-napplet-web-2026-07-28.md",
        ".planning/research/reports/upstream-refresh-napplet-naps-2026-07-28.md",
        ".planning/research/reports/upstream-refresh-synthesis-2026-07-28.md",
    )

    @classmethod
    def collector(cls):
        import importlib.util

        spec = importlib.util.spec_from_file_location("phase1_acquire_sources", cls.COLLECTOR)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module

    def run_git(self, root: Path, *args: str) -> str:
        result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def reviewed_fixture(self) -> tuple[Path, Path, tempfile.TemporaryDirectory[str]]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "reviewed-source-fixture"
        root.mkdir()
        self.run_git(root, "init")
        self.run_git(root, "config", "user.email", "fixture@example.invalid")
        self.run_git(root, "config", "user.name", "Fixture")
        files = {
            ".planning/PROJECT.md": "# Fixture Project\n",
            ".planning/phases/01-research-and-truth-baseline/01-CONTEXT.md": "# Fixture Context\n",
            ".planning/phases/01-research-and-truth-baseline/01-01-PLAN.md": "# Fixture plan\n",
            self.REPORT_PATHS[0]: "# Kehto detail report without a candidate table\n",
            self.REPORT_PATHS[1]: "# Napplet detail report without a candidate table\n",
            self.REPORT_PATHS[2]: "# Naps zero-result detail report without a candidate table\n",
            self.REPORT_PATHS[3]: (
                "| CAND-KEHTO-WEB-PR204-20260728 | observed implementation |\n"
                "| CAND-NAPPLET-WEB-PR186-20260728 | observed implementation |\n"
                "| CAND-NAPS-WINDOW-20260728 | zero-result observation |\n"
                "| CAND-NAPPLET-WEB-PR188-20260728 | release metadata |\n"
            ),
        }
        for relative, content in files.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        self.run_git(root, "add", ".")
        self.run_git(root, "commit", "-m", "fixture source inputs")
        commit = self.run_git(root, "rev-parse", "HEAD")
        rows = []
        for relative in (
            ".planning/PROJECT.md",
            ".planning/phases/01-research-and-truth-baseline/01-CONTEXT.md",
            *self.REPORT_PATHS,
        ):
            blob = self.run_git(root, "rev-parse", f"HEAD:{relative}")
            digest = __import__("hashlib").sha256((root / relative).read_bytes()).hexdigest()
            rows.append(f"    - path: {relative}\n      mode: \"100644\"\n      git_blob: {blob}\n      sha256: {digest}")
        plan_digest = __import__("hashlib").sha256(
            (root / ".planning/phases/01-research-and-truth-baseline/01-01-PLAN.md").read_bytes()
        ).hexdigest()
        review = root / "review.md"
        review.write_text(
            "---\n"
            f"reviewed_commit: {commit}\n"
            "reviewer_identity:\n  fixture: fixture-reviewer\n"
            "current_high: 0\ncurrent_actionable: 0\n"
            "authorization:\n  verdict: \"CONVERGED; HIGH=0; actionable=0\"\n  superseded: false\n"
            f"plan_file_sha256:\n  01-01-PLAN.md: {plan_digest}\n"
            "reviewed_source_inputs:\n  status: fixture\n  paths:\n"
            + "\n".join(rows)
            + "\n---\n# Fixture review\n",
            encoding="utf-8",
        )
        return root, review, temp

    def test_candidate_acquisition_tracer_blocks_incomplete_dimensions(self) -> None:
        collector = self.collector()
        commit = "dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b"
        path = "packages/nap/src/convention-uri.ts"
        blob_bytes = b"export const observed = 'queryless';\n"
        transport = collector.FixtureTransport(
            identities={"https://api.github.com/repos/napplet/web": {"html_url": "https://github.com/napplet/web", "id": 1197078677, "private": False, "archived": False, "default_branch": "main"}},
            commits={commit: {"sha": commit, "tree": "33edc8387973f31687dfb20181a40fe936286824"}},
            blobs={(commit, path): blob_bytes},
            packages={"@napplet/nap": {"version": "0.29.0"}},
        )
        with tempfile.TemporaryDirectory() as temporary:
            cache_root = Path(temporary) / ".research" / "upstreams"
            record = collector.collect_immutable_candidate(
                transport=transport,
                identity_url="https://api.github.com/repos/napplet/web",
                repository="napplet/web",
                commit_sha=commit,
                path=path,
                cache_root=cache_root,
                retrieved_at="2026-07-30T00:00:00Z",
                source_id="SRC-NAPPLET-WEB-PR186-20260730",
                impacts=["EVID-03"],
            )
            self.assertEqual(record["rawOrigin"], "observed-implementation")
            self.assertEqual(record["evidenceClass"], "implementation")
            self.assertEqual(record["contentSha256"], __import__("hashlib").sha256(blob_bytes).hexdigest())
            self.assertNotIn("approved", record["review"])
            root, temp = SourceEvidenceValidationTests().write_root(record)
            with temp:
                result = subprocess.run(
                    [sys.executable, str(VALIDATOR), "validate", "--root", str(root), "--report", str(root / "report.md")],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

        classification = collector.classify_compatibility(
            {"observed-implementation": [record["id"]]}, ["EVID-03", "OPER-03"]
        )
        self.assertEqual(classification["status"], "blocked")
        self.assertEqual(
            classification["missingDimensions"],
            ["normative-protocol", "published-package", "runtime", "example-fixture", "current-work", "conformance"],
        )
        self.assertEqual(classification["affectedRequirements"], ["EVID-03", "OPER-03"])

        with self.assertRaisesRegex(ValueError, "allowlisted"):
            collector.collect_immutable_candidate(transport, "https://example.invalid/repo", "napplet/web", commit, path, cache_root, "2026-07-30T00:00:00Z", record["id"], ["EVID-03"])
        with self.assertRaisesRegex(ValueError, "immutable commit"):
            collector.collect_immutable_candidate(transport, "https://api.github.com/repos/napplet/web", "napplet/web", "main", path, cache_root, "2026-07-30T00:00:00Z", record["id"], ["EVID-03"])
        with self.assertRaisesRegex(ValueError, "cache root"):
            collector.cache_path("/tmp/escaping-cache")
        with self.assertRaisesRegex(ValueError, "normative"):
            collector.build_observed_source_record(record, raw_origin="upstream-fact")

    def test_acquisition_queue_uses_only_reviewed_git_blob_refresh_inputs(self) -> None:
        collector = self.collector()
        root, review, temp = self.reviewed_fixture()
        with temp:
            receipt = collector.load_reviewed_refresh_candidates(root, review, "fixture-executor")
            self.assertEqual(receipt["reviewedCommit"], subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip())
            self.assertEqual([item["id"] for item in receipt["candidates"]], [
                "CAND-KEHTO-WEB-PR204-20260728",
                "CAND-NAPPLET-WEB-PR186-20260728",
                "CAND-NAPS-WINDOW-20260728",
                "CAND-NAPPLET-WEB-PR188-20260728",
            ])
            altered = root / self.REPORT_PATHS[0]
            altered.write_text("| CAND-ALTERED-001 | mutable worktree only |\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "working source input bytes differ"):
                collector.load_reviewed_refresh_candidates(root, review, "fixture-executor")
            altered.unlink()
            with self.assertRaisesRegex(ValueError, "working source input|HEAD source blob differs"):
                collector.load_reviewed_refresh_candidates(root, review, "fixture-executor")

        root, review, temp = self.reviewed_fixture()
        with temp:
            receipt = collector.load_reviewed_refresh_candidates(root, review, "fixture-executor")
            bad_binding = copy.deepcopy(receipt)
            bad_binding["reportDigests"][self.REPORT_PATHS[0]] = "0" * 64
            with self.assertRaisesRegex(ValueError, "digest"):
                collector.validate_reviewed_refresh_binding(bad_binding)
            bad_binding = copy.deepcopy(receipt)
            bad_binding["reviewedCommit"] = "f" * 40
            with self.assertRaisesRegex(ValueError, "reviewed commit"):
                collector.validate_reviewed_refresh_binding(bad_binding)

    def test_reviewed_acquisition_validator_requires_identical_git_blob_binding(self) -> None:
        collector = self.collector()
        root, review, temp = self.reviewed_fixture()
        with temp:
            binding = collector.load_reviewed_refresh_candidates(root, review, "fixture-executor")
            binding["parserVersion"] = "reviewed-refresh-v1"
            queue = {"reviewedSourceInputBinding": binding, "entries": []}
            receipt = {"reviewedSourceInputBinding": copy.deepcopy(binding), "outcomes": []}
            collector.validate_reviewed_acquisition_documents(queue, receipt)

            receipt["reviewedSourceInputBinding"]["reportDigests"][self.REPORT_PATHS[0]] = "0" * 64
            with self.assertRaisesRegex(ValueError, "digest"):
                collector.validate_reviewed_acquisition_documents(queue, receipt)


class SourceEvidenceTests(unittest.TestCase):
    """Exercise the stdlib-only archive-to-target certification boundary."""

    VERIFIER = ROOT / "tools" / "verify-phase1-toolchain.py"

    def run_case(self, case: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.VERIFIER), "--self-test-case", case],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_toolchain_certification_rejects_unverified_wheelhouse_before_install(self) -> None:
        result = self.run_case("wheelhouse-rejection")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("wheelhouse rejection checks passed", result.stdout)

    def test_toolchain_certification_binds_fresh_install_to_verified_wheels(self) -> None:
        result = self.run_case("fresh-install-binding")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("fresh install binding checks passed", result.stdout)

    def test_toolchain_integrity_blocks_untrusted_forwarding(self) -> None:
        result = self.run_case("forwarding-integrity")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("forwarding integrity checks passed", result.stdout)

    def test_toolchain_scope_or_policy_failure_requires_escalation(self) -> None:
        result = self.run_case("scope-policy-escalation")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("scope and policy escalation checks passed", result.stdout)

    def test_toolchain_certification_survives_checkout_relocation_and_rejects_stale_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "relocated-checkout"
            (copied / "tools").mkdir(parents=True)
            (copied / ".planning/research").mkdir(parents=True)
            (copied / ".research").mkdir(parents=True)
            shutil.copy2(self.VERIFIER, copied / "tools" / "verify-phase1-toolchain.py")
            for name in ("requirements-phase1-tools.txt",):
                shutil.copy2(ROOT / name, copied / name)
            for name in ("toolchain-approval.yaml", "toolchain-wheelhouse-manifest.json", "toolchain-install-attestation.json"):
                shutil.copy2(ROOT / ".planning/research" / name, copied / ".planning/research" / name)
            shutil.copytree(ROOT / ".research/phase1-wheelhouse", copied / ".research/phase1-wheelhouse")
            shutil.copytree(ROOT / ".research/phase1-certified-tools-4", copied / ".research/phase1-certified-tools-4")
            shutil.copy2(ROOT / ".research/phase1-installer-report-4.json", copied / ".research/phase1-installer-report-4.json")
            command = [sys.executable, str(copied / "tools" / "verify-phase1-toolchain.py"), "--verify-toolchain"]
            relocated = subprocess.run(command, cwd=copied, text=True, capture_output=True, check=False)
            self.assertEqual(relocated.returncode, 0, relocated.stderr + relocated.stdout)
            attestation = copied / ".planning/research/toolchain-install-attestation.json"
            document = json.loads(attestation.read_text())
            for field in ("wheelhousePath", "installerReportPath", "targetRoot", "targetInterpreterPath", "targetInterpreter"):
                stale_document = copy.deepcopy(document)
                stale_document[field] = str((ROOT / stale_document[field]).absolute())
                attestation.write_text(json.dumps(stale_document), encoding="utf-8")
                stale = subprocess.run(command, cwd=copied, text=True, capture_output=True, check=False)
                self.assertNotEqual(stale.returncode, 0)
                self.assertIn("repo-relative", stale.stderr)
            attestation.write_text(json.dumps(document), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
