---
phase: 01-research-and-truth-baseline
reviewed: 2026-07-31T00:00:00Z
depth: standard
files_reviewed: 24
files_reviewed_list:
  - tests/phase1/fixtures/registry-response.json
  - tests/phase1/test_compatibility.py
  - tests/phase1/test_consolidation_recovery.py
  - tests/phase1/test_drift.py
  - tests/phase1/test_evidence.py
  - tests/phase1/test_gap_closeout.py
  - tests/phase1/test_governance.py
  - tests/phase1/test_lesson_evidence.py
  - tests/phase1/test_preflight.py
  - tests/phase1/test_security_review.py
  - tests/phase1/test_spike_consolidation.py
  - tests/phase1/test_spikes.py
  - tools/acquire-sources.py
  - tools/canonical-recovery.py
  - tools/collect-registry-evidence.py
  - tools/measure-package-conformance.py
  - tools/migrate-phase1-records.py
  - tools/phase1-bootstrap.py
  - tools/refresh-sources.py
  - tools/run-spk-g-sandbox.py
  - tools/validate-phase1-security.py
  - tools/validate-planning.py
  - tools/validate-research.py
  - tools/verify-phase1-toolchain.py
findings:
  critical: 7
  warning: 3
  info: 0
  total: 10
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-07-31T00:00:00Z  
**Depth:** standard  
**Files Reviewed:** 24  
**Status:** issues_found

## Summary

The reviewed Phase 1 evidence tooling has seven blocking correctness or security defects in its cache confinement, durable publication, canonical recovery, and future SPK-G execution paths. The full scoped suite passed 140 tests, but it does not exercise these failure modes. Three additional warnings leave regression coverage incomplete or make evidence tooling unavailable after failures.

## Narrative Findings (AI reviewer)

The submitted implementation generally intends to fail closed, but several code paths contradict that boundary: multi-file evidence records are replaced independently, unexpected transaction artifacts can hang readers indefinitely, and the future package operation bypasses the declared sandbox. These are substantive failures, not deliberate blocked-evidence policy choices.

## Critical Issues

### CR-01: Acquisition cache can escape the repository

**File:** `/workspace/projects/learn-napplets/tools/acquire-sources.py:190-194,251-267`  
**Issue:** `_confined_cache_root()` accepts any resolved path whose final components are `.research/upstreams`, including `/tmp/.research/upstreams`. `collect_immutable_candidate()` subsequently writes fetched upstream bytes there. This contradicts the tool's repository-confined ignored-cache contract and permits collection output outside the checkout.

**Fix:** Require the resolved cache root to equal `CACHE_ROOT.resolve()` (or at minimum be below `ROOT.resolve()` and within `.research/upstreams`), reject symlinked roots, and add a regression test that `collect_immutable_candidate()` rejects `/tmp/.research/upstreams`.

### CR-02: Consolidation publishes canonical files one at a time without durable recovery

**File:** `/workspace/projects/learn-napplets/tools/validate-research.py:1529-1542`  
**Issue:** Consolidation performs sequential `os.replace()` calls for six canonical targets. A kill, crash, or power failure after any replacement permanently leaves a mixed generation. The rollback handles only caught `OSError` and is itself non-atomic, so it cannot recover from interruption.

**Fix:** Publish the complete target map with the journaled `publish_generation()` primitive from `tools/canonical-recovery.py`, or an equivalent durable generation transaction. Add interruption tests at every replacement point and verify that readers see either the entire old generation or the entire new generation.

### CR-03: Newly synthesized drift records are invalid and collapse local observations into upstream sides

**File:** `/workspace/projects/learn-napplets/tools/validate-research.py:1139-1168`  
**Issue:** `new_drift_record()` assigns the same source-derived `side` to both `normative` and `observed`. `validate_drift()` explicitly rejects identical side identities at lines 558-560. Consolidation only schema-validates staged records, so it can publish data that the normal semantic validator subsequently rejects. It also represents a local spike observation as normative evidence.

**Fix:** Use the blocked `observed-local` shape with `normative: null` and retained report/measurement provenance for local spike results, or require genuinely distinct pinned normative and observed sources. Run semantic `validate_drift()` against staged data before publication.

### CR-04: Unexpected transaction entries make canonical readers retry forever

**File:** `/workspace/projects/learn-napplets/tools/canonical-recovery.py:232-240,313-324`  
**Issue:** `_recover_locked()` ignores transaction-directory entries that are files or symlinks. `read_canonical_snapshot()` detects any entry, invokes recovery, then retries; because recovery left the ignored entry in place, this repeats indefinitely. A stray `.canonical-transactions/leftover` therefore hangs planning and evidence readers rather than failing closed.

**Fix:** Reject non-directory, symlinked, or otherwise unrecognized transaction-directory entries with `RecoveryError`; recovery must not return while the reader would still observe transaction content. Add a timeout-bound regression test.

### CR-05: A verified SPK-G operation is handed to the executor without the declared sandbox

**File:** `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:200-212`  
**Issue:** After accepting a `SandboxContract`, `run_spk_g()` passes a bare `npm install` argv to `operation_runner`. It never invokes `construct_sandbox_argv()` from `tools/run-spk-g-sandbox.py`. A future injected executor can consequently install a package with host network, repository write access, and ambient environment despite the receipt claiming a verified sandbox.

**Fix:** Construct and execute only the fixed sandbox argv after contract verification, bind the repository read-only and workspace separately, and enforce resource limits in that same boundary. Add a test proving that an operation runner never receives a bare `npm` argv.

### CR-06: SPK-G rejects the intended scoped package even after qualification

**File:** `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:171-176`  
**Issue:** `fixed_operation()` rejects every package name containing `/`. The canonical target is `@napplet/web`, so a fully eligible and sandboxed run raises `ReceiptValidationError` instead of performing the bounded measurement.

**Fix:** Use a strict npm package-name validator that accepts one scoped `@scope/name` separator while rejecting traversal, backslashes, and invalid names. Add a successful `@napplet/web` operation-construction test.

### CR-07: Retained SPK-G evidence replacement is not atomic

**File:** `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:215-237`  
**Issue:** `retain_validated_bundle()` replaces each target independently. A failure after the first replacement leaves a mixture of new and old evidence despite the function's atomicity claim. Its predictable temporary names also permit a pre-existing symlink at a temporary path to redirect writes.

**Fix:** Stage all evidence in a private verified directory and use a journaled multi-file publication path with recovery. Create temporary files exclusively with no-follow semantics, and add injected-failure tests after every replacement.

## Warnings

### WR-01: A source-ingress security test is silently excluded from discovery

**File:** `/workspace/projects/learn-napplets/tests/phase1/test_evidence.py:154-169,171-190`  
**Issue:** `BoundedCollectorTests` is declared twice. The second declaration overwrites the first at module scope, so `test_collector_rejects_non_allowlisted_url_without_writing()` is not discovered or run.

**Fix:** Merge the first test into the later class or rename one of the classes, then assert that unittest discovery includes the non-allowlisted URL test.

### WR-02: Drift migration mutates caller-owned input data

**File:** `/workspace/projects/learn-napplets/tools/migrate-phase1-records.py:65-83`  
**Issue:** `migrate_drift_v1_to_v2()` shallow-copies the document and each record. `_canonical_record()` then sorts nested `impacts` lists in place, mutating the input document despite the function promising a migrated copy.

**Fix:** Start the drift migration with `copy.deepcopy(document)` and ensure canonicalization only mutates owned structures. Add a test asserting the input object remains unchanged after migration.

### WR-03: Refresh report locks remain permanently stale after abnormal termination

**File:** `/workspace/projects/learn-napplets/tools/refresh-sources.py:162-174,249-256`  
**Issue:** The report lock is a persistent `O_EXCL` file without ownership, liveness, or stale-lock recovery. If a process exits after acquiring it but before `unlink()`, all later refreshes for that report fail indefinitely as busy.

**Fix:** Use an advisory `fcntl.flock` lock whose lifetime ends with the process, or record PID and timestamp and reclaim only demonstrably stale locks. Add a subprocess-termination regression test.

---

_Reviewed: 2026-07-31T00:00:00Z_  
_Reviewer: Claude (gsd-code-reviewer)_  
_Depth: standard_
