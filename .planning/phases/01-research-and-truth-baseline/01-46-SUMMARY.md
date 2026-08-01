---
phase: 01-research-and-truth-baseline
plan: 46
subsystem: evidence-integrity
tags: [python, filesystem-confinement, atomic-publication, advisory-locking, evidence-classification]

requires:
  - phase: 01-research-and-truth-baseline
    provides: Plan 01-42 journaled canonical publisher and Plan 01-45 bounded source acquisition
provides:
  - repository-confined immutable-source cache admission before transport or writes
  - bounded all-or-nothing canonical generation recovery with malformed-transaction refusal
  - non-normative observed-local drift synthesis and staged semantic validation
  - process-lifetime advisory refresh locking with focused retained-finding coverage
affects: [01-47, 01-48, evidence-refresh, canonical-publication]

tech-stack:
  added: []
  patterns: [exact cache-root confinement, journaled generation publication, observed-local/null-normative evidence, fcntl advisory locks]

key-files:
  created: []
  modified:
    - tools/acquire-sources.py
    - tools/canonical-recovery.py
    - tools/validate-research.py
    - tools/refresh-sources.py
    - tests/phase1/test_evidence.py
    - tests/phase1/test_spike_consolidation.py
    - tests/phase1/test_consolidation_recovery.py
    - tests/phase1/test_drift.py
    - tests/phase1/test_gap_closeout.py

key-decisions:
  - "Keep local spike observations blocked and observed-local with normative null; only genuinely distinct pinned sides may represent upstream drift."
  - "Hold an fcntl advisory lock descriptor for the refresh writer lifetime so abnormal process exit releases future refresh attempts."
  - "Do not alter historical terminal review-binding machinery while its PRE118 failure remains outside the owner-authorized recovery scope."

patterns-established:
  - "Evidence writer boundaries validate complete staged data before invoking canonical publication."
  - "A visible advisory-lock file may remain as a coordination inode, but it cannot permanently block refresh after its holder exits."

requirements-completed: [EVID-01, EVID-02, EVID-04, OPER-01, OPER-03]
coverage:
  - id: D1
    description: Repository-confined immutable source acquisition rejects external and symlink-mediated cache roots before side effects.
    requirement: EVID-01
    verification:
      - kind: unit
        ref: tests/phase1/test_evidence.py#BoundedCollectorTests.test_collector_rejects_external_or_symlink_cache_root_before_transport
        status: pass
      - kind: unit
        ref: tests/phase1/test_evidence.py#BoundedCollectorTests.test_unittest_discovery_includes_non_allowlisted_ingress_once
        status: pass
    human_judgment: false
  - id: D2
    description: Canonical consolidation publishes a complete old or new generation and refuses malformed transaction residue.
    requirement: EVID-04
    verification:
      - kind: integration
        ref: tests/phase1/test_spike_consolidation.py#SpikeConsolidationTests.test_consolidation_generation_recovers_after_each_publish_interruption
        status: pass
      - kind: unit
        ref: tests/phase1/test_consolidation_recovery.py#CanonicalRecoveryTests.test_unexpected_transaction_entries_refuse_within_timeout
        status: pass
    human_judgment: false
  - id: D3
    description: Local drift records retain non-normative provenance and refresh locks serialize writers while recovering after process death.
    requirement: OPER-01
    verification:
      - kind: unit
        ref: tests/phase1/test_drift.py#DriftSchemas.test_consolidated_local_observation_retains_non_normative_provenance
        status: pass
      - kind: integration
        ref: tests/phase1/test_drift.py#RefreshComparisonTests.test_refresh_lock_serializes_and_process_termination_releases_it
        status: pass
      - kind: unit
        ref: tests/phase1/test_gap_closeout.py#RecoveryScopeCompositionTests.test_focused_recovery_composition_covers_only_retained_findings
        status: pass
    human_judgment: false
  - id: D4
    description: Full Phase 1 suite confirmation after the six retained repair regressions.
    verification:
      - kind: integration
        ref: tools/phase1-python -m unittest discover -s tests/phase1 -v
        status: fail
    human_judgment: true
    rationale: Historical terminal-validator tests are blocked by PRE118 review-manifest binding and require separately scoped human-approved remediation.

metrics:
  duration: 5m 55s
  completed: 2026-07-31
status: complete
---

# Phase 01 Plan 46: Evidence Boundary Recovery Summary

**Repository-confined source ingress, journaled canonical evidence generations, observed-local drift semantics, and process-lifetime refresh locks now protect the retained evidence boundary repairs without promoting local observations to upstream fact.**

## Performance

- **Duration:** 5m 55s
- **Started:** 2026-07-31T02:53:24Z
- **Completed:** 2026-07-31T02:59:19Z
- **Tasks:** 3/3
- **Files modified:** 9 task artifacts

## Accomplishments

- Confined immutable-source collection to the exact repository-owned cache root and restored discovery coverage for rejected ingress.
- Routed complete consolidation targets through the shared journaled publisher, validating staged drift semantics before publication and failing closed on malformed transaction residue.
- Preserved local observations as blocked `observed-local` records with `normative: null`, and replaced persistent exclusive refresh locks with held advisory locks that release on process death.
- Added an exact six-finding composition test for CR-01 through CR-04, WR-01, and WR-03; it intentionally excludes deferred migration-copy and SPK-G/package work.

## Task Commits

1. **Task 1: Confine source ingress and restore its missing regression** — `725c0e5` (RED), `59ed63a` (GREEN)
2. **Task 2: Publish and recover canonical evidence as one bounded generation** — `a6d9265` (RED), `74cb1ea` (GREEN)
3. **Task 3: Preserve observed-local semantics and recover refresh availability** — `2266a94` (RED), `8929405` (GREEN)

## Files Created/Modified

- `tools/acquire-sources.py` — rejects non-canonical or symlink-mediated source-cache paths before transport or writes.
- `tools/canonical-recovery.py` — refuses unknown, malformed, symlinked, or ambiguous transaction residue within bounded recovery.
- `tools/validate-research.py` — publishes complete validated consolidation maps atomically and retains observed-local drift records without normative duplication.
- `tools/refresh-sources.py` — holds an `fcntl.flock` descriptor for the refresh writer lifetime and releases it on normal completion or process death.
- `tests/phase1/test_evidence.py` — covers cache ingress confinement and single discovery of non-allowlisted URLs.
- `tests/phase1/test_spike_consolidation.py` and `tests/phase1/test_consolidation_recovery.py` — cover interruption-safe generation recovery and fast malformed-transaction refusal.
- `tests/phase1/test_drift.py` and `tests/phase1/test_gap_closeout.py` — cover non-normative local provenance, lock-holder termination recovery, and the exact retained recovery composition.

## Verification

Passed:

- Task 1 focused source-ingress regression command from `01-46-PLAN.md`.
- Task 2 focused canonical-publication/recovery regression command from `01-46-PLAN.md`.
- `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift test_gap_closeout` — 22 tests passed.
- Task 3 RED/GREEN regression selection — 3 tests passed after the advisory-lock implementation.
- `tools/phase1-python --verify-toolchain` and `git diff --check`.

Deferred failure:

- `tools/phase1-python -m unittest discover -s tests/phase1 -v` ran the full suite but eight historical `test_closeout_commands` terminal-validator tests errored because the Plan 01-29 source-input verifier returned `PRE118: review plan manifest is not the exact active plan set`. This is outside the active repair scope and its resolution must not weaken the historical review binding or reintroduce deferred terminal-publication choreography. The item is retained in `deferred-items.md`.

## Decisions Made

- Local spike evidence remains a blocked observed-local hand-off with retained report and measurement digests; it cannot become normative merely by duplicating a source-derived side.
- Refresh locking uses a private regular lock inode plus a held `fcntl.flock` descriptor. The OS releases the lock when a process exits, while concurrent writers receive a bounded busy result.
- The focused composition test names only the six owner-authorized findings, making deferred CR-05 through CR-07, SPK-G, and WR-02 explicitly out of scope.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Imported the advisory-lock module required by the refresh implementation**
- **Found during:** Task 3 GREEN verification
- **Issue:** The first advisory-lock implementation referenced `fcntl` before importing it, causing the lock-holder subprocess to exit with `NameError`.
- **Fix:** Added the standard-library `fcntl` import and reran the regression selection successfully.
- **Files modified:** `tools/refresh-sources.py`
- **Verification:** The process-termination recovery regression passed after the import was added.
- **Committed in:** `8929405`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** The correction was required for the planned advisory-lock behavior and did not expand scope.

## Issues Encountered

- Full-suite terminal-validator coverage is presently blocked by the pre-existing `PRE118` exact-active-plan-manifest condition. It was recorded for a dedicated gap plan rather than changing review-binding or terminal machinery outside this recovery plan.

## Known Stubs

None.

## Next Phase Readiness

- Plan 01-47 can consume repository-confined acquisition and coherent canonical evidence generations for immutable upstream truth admission.
- The complete Phase 1 suite is not green until the separately deferred historical terminal review-binding failure is resolved under a scoped plan and approval boundary.

## Self-Check: PASSED

- Confirmed all nine task artifacts and this summary exist in the main worktree.
- Confirmed all six Task 1–3 RED/GREEN commits are reachable from `master`.
- Confirmed no tracked-file deletions or whitespace errors were introduced by Task 3.
