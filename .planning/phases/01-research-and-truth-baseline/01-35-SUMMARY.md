---
phase: 01-research-and-truth-baseline
plan: 35
subsystem: compatibility-evidence
status: complete
tags: [python, yaml, json-schema, compatibility, immutable-snapshot, evidence-provenance]
requires:
  - phase: 01-29
    provides: reviewed source-input binding and immutable Git-blob evidence boundary
  - phase: 01-42
    provides: registered shared-lock canonical snapshot reader
  - phase: 01-45
    provides: reviewed acquisition queue and receipt binding
provides:
  - deterministic compatibility v1-to-v2 migration with retained immutable fixtures
  - seven-dimension substantive eligibility result with ordered blocked reasons
  - immutable registered compatibility snapshot index with no post-acquisition canonical reads
affects: [01-36, package-conformance, phase-1-validation]
tech-stack:
  added: []
  patterns:
    - closed compatibility dimension records with evidence and authority expectations
    - receipt validation before a registered immutable snapshot is acquired
    - typed in-memory indexes as the sole evaluator input
key-files:
  created:
    - .planning/research/schemas/legacy/compatibility.schema.v1.json
    - .planning/research/schemas/fixtures/compatibility-v1-legacy.yaml
    - .planning/research/schemas/fixtures/compatibility-v2-current.yaml
  modified:
    - tools/migrate-phase1-records.py
    - tools/validate-research.py
    - tools/acquire-sources.py
    - .planning/research/schemas/compatibility.schema.json
    - .planning/research/compatibility-matrix.yaml
    - tests/phase1/test_compatibility.py
key-decisions:
  - "Compatibility eligibility consumes only CompatibilitySnapshotIndex data parsed from Plan 01-42's registered reader."
  - "Eligibility remains blocked until every substantive dimension and a separate reviewed approval are qualified; it never approves architecture."
  - "A standalone read-only receipt validation uses a fixed non-reviewer identity while collection still requires an explicit executor identity."
patterns-established:
  - "Snapshot-only evaluators do not receive roots or paths, preventing lazy canonical-file reopening."
  - "Compatibility evidence reports blocked reasons in the fixed seven-dimension order followed by approval state."
requirements-completed: [EVID-01, EVID-02, EVID-03, OPER-01]
coverage:
  - id: D1
    description: Deterministic migration retains v1 references and produces exactly the closed v2 dimension contract.
    requirement: EVID-03
    verification:
      - kind: unit
        ref: tests/phase1/test_compatibility.py#CompatibilitySchema.test_compatibility_v1_to_v2_migration
        status: pass
    human_judgment: false
  - id: D2
    description: Compatibility baseline evaluates substantive dimensions and receipt-bound provenance from one immutable registered snapshot.
    requirement: EVID-03
    verification:
      - kind: unit
        ref: tests/phase1/test_compatibility.py#CompatibilitySchema.test_baseline_eligibility_requires_all_substantive_dimensions_without_approval
        status: pass
      - kind: unit
        ref: tests/phase1/test_compatibility.py#CompatibilitySchema.test_compatibility_evaluation_rejects_unbound_reviewed_acquisition_provenance
        status: pass
      - kind: integration
        ref: tests/phase1/test_compatibility.py#CompatibilitySchema.test_compatibility_evaluation_uses_one_registered_snapshot_during_successful_publish
        status: pass
    human_judgment: false
metrics:
  duration: 14m
  completed: 2026-07-30
  tasks: 2
  files: 10
---

# Phase 01 Plan 35: Substantive compatibility baseline Summary

**Versioned compatibility evidence now evaluates seven authority-aware dimensions from one immutable canonical snapshot and preserves a deterministic blocked v1-to-v2 migration path.**

## Performance

- **Duration:** 14 min
- **Started:** 2026-07-30T16:50:06Z
- **Completed:** 2026-07-30T17:03:45Z
- **Tasks:** 2/2
- **Files modified:** 10

## Accomplishments

- Added a schema-v2 compatibility contract with closed normative-protocol, observed-implementation, published-package, runtime, example/fixture, current-work, and conformance dimensions.
- Retained a legacy v1 schema plus paired fixture inputs, deterministic migration CLI, checksums, and explicit rollback/change notes without synthesizing eligibility or approval.
- Added receipt-bound snapshot indexing and semantic blocked-or-eligible evaluation that resolves source, claim, package, spike, drift, and open-question families only from registered in-memory bytes.
- Proved concurrent canonical publication leaves compatibility results wholly on the old snapshot, and instrumented post-acquisition evaluation to reject all canonical filesystem opens.

## Task Commits

1. **Task 1: Migrate compatibility v1 to v2 without evaluating eligibility**
   - `2624b1a` — `test(01-35): add failing compatibility migration regression`
   - `26c9ce8` — `feat(01-35): migrate compatibility records to v2`
2. **Task 2: Evaluate seven substantive dimensions to ordered eligible-or-blocked truth**
   - `7a854f3` — `test(01-35): add failing compatibility snapshot regressions`
   - `a8b5f93` — `feat(01-35): evaluate compatibility from registered snapshots`

## Files Created/Modified

- `tools/migrate-phase1-records.py` — deterministic compatibility migration API and CLI alongside the retained drift migration.
- `tools/validate-research.py` — immutable `CompatibilitySnapshotIndex`, ordered semantic evaluator, and snapshot-only validation route.
- `tools/acquire-sources.py` — standalone reviewed-acquisition revalidation identity fallback for the documented read-only command.
- `.planning/research/schemas/compatibility.schema.json` — v2 seven-dimension contract.
- `.planning/research/compatibility-matrix.yaml` — blocked baseline with ordered substantive result reasons.
- `tests/phase1/test_compatibility.py` — migration, provenance, publication-overlap, and post-snapshot-open regressions.

## Verification

Passed the complete automated Plan 01-35 verification sequence:

- `tools/phase1-python tools/acquire-sources.py validate-reviewed-acquisition --queue .planning/research/upstream-acquisition-queue.yaml --receipt .planning/research/reports/upstream-acquisition-20260728.md --review .planning/phases/01-research-and-truth-baseline/01-REVIEWS.md`
- `test_compatibility.CompatibilitySchema.test_compatibility_v1_to_v2_migration`
- `test_compatibility.CompatibilitySchema.test_baseline_eligibility_requires_all_substantive_dimensions_without_approval`
- `test_compatibility.CompatibilitySchema.test_compatibility_evaluation_rejects_unbound_reviewed_acquisition_provenance`
- `test_compatibility.CompatibilitySchema.test_compatibility_evaluation_uses_one_registered_snapshot_during_successful_publish`
- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/phase1-substantive-compatibility.md`
- Full `test_compatibility` module: 11 tests passed.

## Decisions Made

- Stored migration dimensions as blocked/not-reviewed evidence records so v2 migration remains independent of semantic eligibility policy.
- Kept eligibility and approval distinct: even a structurally complete record remains blocked without a separate reviewed approval, and no result expresses architecture approval.
- Validated receipt/queue provenance before registered snapshot acquisition; after acquisition, evaluator helpers receive no canonical root or path capability.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Made the documented read-only provenance command self-contained**
- **Found during:** Task 2 verification
- **Issue:** The exact planned `validate-reviewed-acquisition` command failed outside an orchestration environment because `GSD_EXECUTOR_ID` was unset.
- **Fix:** Added a fixed non-reviewer identity solely for standalone read-only revalidation; bounded collection continues to require an explicit executor identity.
- **Files modified:** `tools/acquire-sources.py`
- **Verification:** The exact command and the snapshot-only `validate --root` route pass without an exported executor variable.
- **Committed in:** `a8b5f93`

---

**Total deviations:** 1 auto-fixed (1 Rule 3 blocking)
**Impact on plan:** Required verification usability only; reviewed source binding, blocked evidence classifications, approval boundaries, and collection authentication semantics remain unchanged.

## Issues Encountered

- Dynamically loaded validator modules cannot use dataclass registration safely unless inserted into `sys.modules`; the immutable compatibility index therefore uses `NamedTuple`, preserving typed immutability without hidden loader state.

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 01-36 can consume the ordered blocked compatibility result before constructing any package operation.
- The current baseline deliberately remains blocked on qualified normative, package, runtime, example, current-work, conformance, and reviewed-approval evidence.

## Self-Check: PASSED

- Confirmed all ten planned implementation, schema, fixture, and test artifacts plus this summary exist.
- Confirmed task TDD commits `2624b1a`, `26c9ce8`, `7a854f3`, and `a8b5f93` are present in Git history.
- Confirmed Plan 01-35 introduced no tracked-file deletions and did not modify `STATE.md` or `ROADMAP.md`.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-30*
