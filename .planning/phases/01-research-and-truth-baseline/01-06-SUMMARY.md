---
phase: 01-research-and-truth-baseline
plan: 06
subsystem: evidence-drift-and-refresh
status: complete
tags: [evidence, drift, compatibility, provenance, refresh, python]
requires: [01-05]
provides:
  - Ten separately traceable, blocked DRF outcomes with parallel immutable policy/archival baselines
  - A compatibility matrix and directional current-work snapshot that preserve blocked upstream status
  - Deterministic, comparison-only source refresh review work
  - Scoped open-question routing for dependent ADR decisions
affects: [01-07, phase-1-spikes, phase-1-adrs, source-freshness]
tech-stack:
  added: [Python standard-library refresh CLI]
  patterns: [parallel conflict records, immutable pin comparison, deterministic review-work identity, no-automatic-claim-revision]
key-files:
  created:
    - .planning/research/drift-register.yaml
    - .planning/research/compatibility-matrix.yaml
    - .planning/research/open-work-snapshot.json
    - .planning/research/open-work-analysis.md
    - .planning/research/open-questions.yaml
    - tools/refresh-sources.py
    - .planning/research/reports/refresh-review-work.md
  modified:
    - .planning/research/claims.yaml
    - .planning/research/schemas/drift.schema.json
    - .planning/research/schemas/compatibility.schema.json
    - tests/phase1/test_drift.py
    - tests/phase1/test_compatibility.py
key-decisions:
  - "All mandatory drift checks remain blocked until official immutable upstream baselines are collected; archived planning questions never become protocol facts."
  - "Current-work metadata is directional evidence and a revisit trigger, never sole proof of released or shipped behavior."
  - "Refresh comparison emits stable review work and preserves canonical evidence records for human interpretation."
patterns-established:
  - "DRF records preserve separate normative and observed statements, source pins, uncertainty, impact, and dependent-decision disposition."
  - "Refresh output is atomically replaced under a bounded lock; concurrent callers fail explicitly rather than interleave report writes."
requirements-completed: [EVID-02, EVID-03, OPER-01]
coverage:
  - id: D1
    description: "Ten mandatory drift outcomes retain complete parallel source and claim links plus unresolved decision routing."
    requirement: EVID-02
    verification:
      - kind: unit
        ref: "tests/phase1/test_drift.py#test_mandatory_drift_register_keeps_parallel_pinned_evidence"
        status: pass
      - kind: other
        ref: "tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md"
        status: pass
    human_judgment: false
  - id: D2
    description: "Blocked compatibility and directional current-work records preserve immutable-baseline distinctions without asserting unavailable package or runtime behavior."
    requirement: EVID-03
    verification:
      - kind: unit
        ref: "tests/phase1/test_compatibility.py#test_matrix_covers_blocked_public_surfaces_without_mixing_baselines"
        status: pass
    human_judgment: false
  - id: D3
    description: "Source refresh comparisons are idempotent for unchanged pins and create stable review work for changed, unavailable, or ambiguous inputs without claim mutation."
    requirement: OPER-01
    verification:
      - kind: integration
        ref: "tests/phase1/test_drift.py#RefreshComparisonTests"
        status: pass
      - kind: other
        ref: "tools/phase1-python tools/refresh-sources.py --help"
        status: pass
    human_judgment: false
metrics:
  duration: 10m
  tasks_completed: 2
  files_modified: 12
  completed: 2026-07-23
---

# Phase 01 Plan 06: Drift, Compatibility, and Refresh Review Summary

**A blocked-but-auditable compatibility baseline now preserves ten unresolved protocol-drift questions and routes immutable source changes to deterministic human review work.**

## Performance

- **Duration:** 10 min
- **Started:** 2026-07-23T23:10:20Z
- **Completed:** 2026-07-23T23:19:55Z
- **Tasks:** 2
- **Files modified:** 12

## Accomplishments

- Recorded all ten mandatory `DRF-*` checks as distinct, blocked parallel records with immutable source pins, separate claims, uncertainty, impact mapping, and safe dependent-decision dispositions.
- Added an explicit blocked compatibility row, dated directional current-work snapshot, ordered current-work analysis, and an `OQ-*` route for all decisions that remain dependent on official upstream evidence.
- Implemented `tools/refresh-sources.py` to compare immutable pins and emit a heading-contract-compliant review report without rewriting source, claim, drift, question, approval, or ADR records.
- Added TDD coverage for the artifact graph and for unchanged, changed, unavailable, and ambiguous refresh results; the full Phase 1 suite now has 34 passing tests.

## Task Commits

Each TDD task was committed as a RED/Green pair:

1. **Task 1: Record mandatory drift outcomes, compatibility, and current work** — `328685f` (test), `e49a530` (feat)
2. **Task 2: Implement drift refresh as comparison and review-work generation only** — `79fc60f` (test), `041a757` (feat)

## Files Created/Modified

- `.planning/research/drift-register.yaml` — ten blocked `DRF-*` outcomes with parallel source-pinned sides.
- `.planning/research/compatibility-matrix.yaml` — honest compatibility baseline that records blocked public package/runtime/example/fixture evidence.
- `.planning/research/open-work-snapshot.json` and `open-work-analysis.md` — dated, directional current-work evidence and impact analysis.
- `.planning/research/open-questions.yaml` — stable unresolved-decision routing criteria.
- `tools/refresh-sources.py` — atomic, comparison-only review-work generator with a bounded lock.
- `.planning/research/reports/refresh-review-work.md` — initial deterministic unchanged comparison report.
- `tests/phase1/test_drift.py` and `tests/phase1/test_compatibility.py` — artifact and refresh behavior checks.

## Verification

Passed:

- `tools/phase1-python -m unittest discover -s tests/phase1` — 34 tests.
- `tools/phase1-python tools/refresh-sources.py --help`.
- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md`.
- `tools/phase1-python tools/validate-planning.py` — passed with the expected Phase 1 pending-deliverables warning.

## Decisions Made

- Preserve the upstream-evidence blocker instead of inventing outcomes for the ten required comparison questions.
- Treat candidate issue/PR/discussion metadata as directional only and retain immutable-record collection as the refresh trigger.
- Make refresh generation append-free and idempotent: the report is derived from comparison input and atomic output replacement, while reviewers decide semantic state changes.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] Extended closed record schemas for required traceability metadata**
- **Found during:** Task 1.
- **Issue:** The closed drift and compatibility schemas rejected the plan-required dependent-decision disposition and per-row status/scope metadata.
- **Fix:** Added validated optional fields to retain these mandatory details without weakening the existing immutable-pin constraints.
- **Files modified:** `.planning/research/schemas/drift.schema.json`, `.planning/research/schemas/compatibility.schema.json`.
- **Verification:** Focused schema tests and research-root validation pass.
- **Committed in:** `e49a530`.

---

**Total deviations:** 1 auto-fixed (1 blocking issue).
**Impact on plan:** The schema extension was required to store plan-mandated traceability data; no upstream or accepted claim meaning was changed.

## Known Stubs

None. `blocked`, `unavailable`, and null immutable-reference values are deliberate evidence states with scoped impacts and refresh triggers; they do not stand in for source data.

## Issues Encountered

- The initial schema extension introduced malformed JSON; the focused RED/Green validation immediately exposed it and the schema was rewritten as valid JSON before the task Green commit.

## Self-Check: PASSED

- Found all seven planned artifacts and the plan summary at their declared paths.
- Verified TDD and implementation commits `328685f`, `e49a530`, `79fc60f`, and `041a757` resolve in Git.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 01-07 can consume the stable `DRF-*`, `CMP-*`, and `OQ-*` IDs and must preserve the current blocked upstream-evidence status.
- Official immutable NIP/NAP/package/runtime acquisition remains the explicit prerequisite for semantic compatibility or architecture conclusions.
