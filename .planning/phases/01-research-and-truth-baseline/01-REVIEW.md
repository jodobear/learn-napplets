---
phase: 01-research-and-truth-baseline
reviewed: 2026-07-31T04:17:27Z
depth: standard
files_reviewed: 36
files_reviewed_list:
  - site/README.md
  - site/assets/site.js
  - site/assets/styles.css
  - site/content/site.json
  - site/dist/architecture/index.html
  - site/dist/index.html
  - site/dist/learn/index.html
  - site/dist/sources/index.html
  - site/templates/page.html
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
  - tests/site/test_site_browser.py
  - tests/site/test_static_site.py
  - tools/acquire-sources.py
  - tools/build-site.py
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
  critical: 1
  warning: 1
  info: 0
  total: 2
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-07-31T04:17:27Z
**Depth:** standard
**Files Reviewed:** 36
**Status:** issues_found

## Summary

This re-review covers the owner-authorized evidence-boundary recovery and static-site scope. The six targeted baseline items are fixed, while the four explicitly excluded package/migration items remain deferred. Two newly actionable defects remain: the static-site builder accepts mutable source URLs while labeling them immutable, and a retained collector regression is incompatible with the repaired exact-cache policy.

Verification performed: `python3 tools/build-site.py --check` and all five `tests/site/test_static_site.py` tests passed. The targeted collector regression `test_evidence.BoundedCollectorTests.test_candidate_acquisition_tracer_blocks_incomplete_dimensions` fails with the stale temporary cache root described in WR-04. `git diff --check` passed.

## Narrative Findings (AI reviewer)

The static site correctly renders the currently checked-in evidence labels, but the source-content validator does not enforce the immutable-evidence contract that the rendered ledger promises. The retained Phase 1 test suite also contains a regression that now fails because it still expects the pre-recovery cache-root behavior.

## Historical Baseline Outcomes

| Finding | Outcome | Re-review disposition |
| --- | --- | --- |
| CR-01 | fixed | Exact repository cache-root confinement is now enforced before transport or writes. |
| CR-02 | fixed | Consolidation routes its complete target map through journaled canonical publication. |
| CR-03 | fixed | Synthesized local drift is `observed-local` with `normative: null`. |
| CR-04 | fixed | Canonical recovery refuses malformed or unexpected transaction residue. |
| CR-05 | deferred | SPK-G sandbox execution is outside the owner-authorized static-site recovery scope. |
| CR-06 | deferred | Scoped npm package-name operation remains outside the recovery scope. |
| CR-07 | deferred | SPK-G retained-bundle publication remains outside the recovery scope. |
| WR-01 | fixed | The formerly overwritten source-ingress test is discoverable. |
| WR-02 | deferred | Migration input mutation is explicitly outside the recovery scope. |
| WR-03 | fixed | Refresh coordination now uses process-lifetime advisory locking. |

### Preserved baseline finding history

#### CR-01: Acquisition cache can escape the repository

**Historical file:** `/workspace/projects/learn-napplets/tools/acquire-sources.py:190-194,251-267`
**Historical issue:** `_confined_cache_root()` accepted any resolved path whose final components were `.research/upstreams`, including `/tmp/.research/upstreams`. `collect_immutable_candidate()` subsequently wrote fetched upstream bytes there. This contradicted the tool's repository-confined ignored-cache contract and permitted collection output outside the checkout.
**Historical fix:** Require the resolved cache root to equal `CACHE_ROOT.resolve()` (or at minimum be below `ROOT.resolve()` and within `.research/upstreams`), reject symlinked roots, and add a regression test that `collect_immutable_candidate()` rejects `/tmp/.research/upstreams`.

#### CR-02: Consolidation publishes canonical files one at a time without durable recovery

**Historical file:** `/workspace/projects/learn-napplets/tools/validate-research.py:1529-1542`
**Historical issue:** Consolidation performed sequential `os.replace()` calls for six canonical targets. A kill, crash, or power failure after any replacement permanently left a mixed generation. The rollback handled only caught `OSError` and was itself non-atomic, so it could not recover from interruption.
**Historical fix:** Publish the complete target map with the journaled `publish_generation()` primitive from `tools/canonical-recovery.py`, or an equivalent durable generation transaction. Add interruption tests at every replacement point and verify that readers see either the entire old generation or the entire new generation.

#### CR-03: Newly synthesized drift records are invalid and collapse local observations into upstream sides

**Historical file:** `/workspace/projects/learn-napplets/tools/validate-research.py:1139-1168`
**Historical issue:** `new_drift_record()` assigned the same source-derived `side` to both `normative` and `observed`. `validate_drift()` explicitly rejected identical side identities at lines 558-560. Consolidation only schema-validated staged records, so it could publish data that the normal semantic validator subsequently rejected. It also represented a local spike observation as normative evidence.
**Historical fix:** Use the blocked `observed-local` shape with `normative: null` and retained report/measurement provenance for local spike results, or require genuinely distinct pinned normative and observed sources. Run semantic `validate_drift()` against staged data before publication.

#### CR-04: Unexpected transaction entries make canonical readers retry forever

**Historical file:** `/workspace/projects/learn-napplets/tools/canonical-recovery.py:232-240,313-324`
**Historical issue:** `_recover_locked()` ignored transaction-directory entries that were files or symlinks. `read_canonical_snapshot()` detected any entry, invoked recovery, then retried; because recovery left the ignored entry in place, this repeated indefinitely. A stray `.canonical-transactions/leftover` therefore hung planning and evidence readers rather than failing closed.
**Historical fix:** Reject non-directory, symlinked, or otherwise unrecognized transaction-directory entries with `RecoveryError`; recovery must not return while the reader would still observe transaction content. Add a timeout-bound regression test.

#### CR-05: A verified SPK-G operation is handed to the executor without the declared sandbox

**Historical file:** `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:200-212`
**Historical issue:** After accepting a `SandboxContract`, `run_spk_g()` passed a bare `npm install` argv to `operation_runner`. It never invoked `construct_sandbox_argv()` from `tools/run-spk-g-sandbox.py`. A future injected executor could consequently install a package with host network, repository write access, and ambient environment despite the receipt claiming a verified sandbox.
**Historical fix:** Construct and execute only the fixed sandbox argv after contract verification, bind the repository read-only and workspace separately, and enforce resource limits in that same boundary. Add a test proving that an operation runner never receives a bare `npm` argv.

#### CR-06: SPK-G rejects the intended scoped package even after qualification

**Historical file:** `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:171-176`
**Historical issue:** `fixed_operation()` rejected every package name containing `/`. The canonical target is `@napplet/web`, so a fully eligible and sandboxed run raised `ReceiptValidationError` instead of performing the bounded measurement.
**Historical fix:** Use a strict npm package-name validator that accepts one scoped `@scope/name` separator while rejecting traversal, backslashes, and invalid names. Add a successful `@napplet/web` operation-construction test.

#### CR-07: Retained SPK-G evidence replacement is not atomic

**Historical file:** `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:215-237`
**Historical issue:** `retain_validated_bundle()` replaced each target independently. A failure after the first replacement left a mixture of new and old evidence despite the function's atomicity claim. Its predictable temporary names also permitted a pre-existing symlink at a temporary path to redirect writes.
**Historical fix:** Stage all evidence in a private verified directory and use a journaled multi-file publication path with recovery. Create temporary files exclusively with no-follow semantics, and add injected-failure tests after every replacement.

#### WR-01: A source-ingress security test is silently excluded from discovery

**Historical file:** `/workspace/projects/learn-napplets/tests/phase1/test_evidence.py:154-169,171-190`
**Historical issue:** `BoundedCollectorTests` was declared twice. The second declaration overwrote the first at module scope, so `test_collector_rejects_non_allowlisted_url_without_writing()` was not discovered or run.
**Historical fix:** Merge the first test into the later class or rename one of the classes, then assert that unittest discovery includes the non-allowlisted URL test.

#### WR-02: Drift migration mutates caller-owned input data

**Historical file:** `/workspace/projects/learn-napplets/tools/migrate-phase1-records.py:65-83`
**Historical issue:** `migrate_drift_v1_to_v2()` shallow-copied the document and each record. `_canonical_record()` then sorted nested `impacts` lists in place, mutating the input document despite the function promising a migrated copy.
**Historical fix:** Start the drift migration with `copy.deepcopy(document)` and ensure canonicalization only mutates owned structures. Add a test asserting the input object remains unchanged after migration.

#### WR-03: Refresh report locks remain permanently stale after abnormal termination

**Historical file:** `/workspace/projects/learn-napplets/tools/refresh-sources.py:162-174,249-256`
**Historical issue:** The report lock was a persistent `O_EXCL` file without ownership, liveness, or stale-lock recovery. If a process exited after acquiring it but before `unlink()`, all later refreshes for that report failed indefinitely as busy.
**Historical fix:** Use an advisory `fcntl.flock` lock whose lifetime ends with the process, or record PID and timestamp and reclaim only demonstrably stale locks. Add a subprocess-termination regression test.

## Critical Issues

### CR-08: Static-site builder accepts mutable sources as immutable evidence

**File:** `/workspace/projects/learn-napplets/tools/build-site.py:33,96-103`
**Issue:** `SAFE_URL` only checks that an `immutableUrl` looks like a GitHub URL. It accepts mutable branch and tag references such as `https://github.com/jodobear/learn-napplets/blob/main/.planning/governance/evidence-policy.md`. The builder also only requires nonempty `sourceIdentity`, `digest`, and `retrievedAt` strings. It can therefore generate a source ledger that calls a mutable or malformed record an “immutable source identity,” violating the evidence contract for the learning surface.

A temporary content copy with the `SRC-POLICY-002` URL changed to the mutable `/blob/main/` form completed successfully with `returncode=0`.

**Fix:** Require and cross-check immutable source fields before rendering:

```python
IMMUTABLE_GITHUB_URL = re.compile(
    r"^https://github\.com/(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/blob/"
    r"(?P<commit>[0-9a-f]{40,64})/(?P<path>[A-Za-z0-9._/-]+)$"
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
```

Parse `retrievedAt` as a timezone-qualified RFC3339 timestamp, require the digest to match `SHA256`, and require `sourceIdentity` to identify the same repository, commit, and path as the immutable URL. Add negative tests for branch/tag URLs, malformed digests/timestamps, and mismatched identity fields.

## Warnings

### WR-04: Retained collector regression still expects the unsafe cache-root policy

**File:** `/workspace/projects/learn-napplets/tests/phase1/test_evidence.py:332-369`
**Issue:** `test_candidate_acquisition_tracer_blocks_incomplete_dimensions` creates a temporary `.research/upstreams` directory and supplies it to `collect_immutable_candidate()`. The repaired collector intentionally admits only the exact repository-owned `collector.CACHE_ROOT`, so the test now errors at `tools/acquire-sources.py:197` before exercising its intended assertions:

```text
ValueError: cache root must be the exact repository-owned .research/upstreams directory
```

This is a stale regression fixture rather than the preserved PRE118 or source-registry deferred failures. It leaves the retained suite red and masks the intended compatibility classification assertions.

**Fix:** Pass `collector.CACHE_ROOT` to this fixture and remove only its unique `fixture/collector` child after the assertion, following the nearby exact-cache-root test. Do not relax `_confined_cache_root()` to restore acceptance of temporary external paths.

---

_Reviewed: 2026-07-31T04:17:27Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
