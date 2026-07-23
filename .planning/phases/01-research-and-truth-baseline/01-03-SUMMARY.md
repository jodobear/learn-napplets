---
phase: 01-research-and-truth-baseline
plan: "03"
subsystem: research-evidence-validation
tags: [json-schema, draft-2020-12, provenance, drift, compatibility]
requires:
  - phase: 01-02
    provides: "Source and claim schemas plus safe semantic validation"
provides:
  - "Strict DRF and OQ contracts for parallel conflicts and impact-scoped blockers"
  - "CMP immutable-baseline contract with semantic dangling-link and baseline checks"
affects: [phase-1-acquisition, phase-1-spikes, evidence-governance]
tech-stack:
  added: []
  patterns: [parallel conflict records, impact-scoped blockers, immutable baseline comparison]
key-files:
  created:
    - .planning/research/schemas/drift.schema.json
    - .planning/research/schemas/open-question.schema.json
    - .planning/research/schemas/compatibility.schema.json
    - tests/phase1/test_drift.py
    - tests/phase1/test_compatibility.py
  modified:
    - tools/validate-research.py
key-decisions:
  - "Conflicting normative and observed statements remain parallel DRF sides with independently pinned source fields."
  - "Compatibility pins must equal their referenced immutable source commit, path, and content digest."
patterns-established:
  - "Schema shape gates precede semantic ID and immutable-baseline checks."
requirements-completed: [EVID-02, EVID-03, OPER-01]
coverage:
  - id: D1
    description: "Parallel drift and open-question records reject flattened conflicts and incomplete blocker routing."
    requirement: EVID-02
    verification:
      - kind: unit
        ref: "tests/phase1/test_drift.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "Compatibility records require immutable release and current-work source pins."
    requirement: EVID-03
    verification:
      - kind: unit
        ref: "tests/phase1/test_compatibility.py"
        status: pass
    human_judgment: false
duration: 8m
completed: 2026-07-24
status: complete
---

# Phase 01 Plan 03: Conflict and Compatibility Contracts Summary

**Draft 2020-12 contracts now preserve conflicting evidence as parallel records, route open blockers by impact, and constrain compatibility to immutable source baselines.**

## Performance

- **Duration:** 8m
- **Tasks:** 2/2
- **Files modified:** 6

## Accomplishments

- Added closed DRF and OQ schemas that require complete parallel evidence sides, uncertainty, impact mapping, history, owners, review routing, and resolution criteria.
- Added CMP schema and semantic validator checks for unknown stable IDs and source-pin commit/path/digest mismatches.
- Added focused negative fixture coverage and passed the complete available Phase 1 suite and validators.

## Task Commits

1. **Task 1: Model parallel conflicts and impact-scoped open questions** - `8d6a82c` (feat)
2. **Task 2: Constrain compatibility to one known immutable evidence baseline** - `787600b` (test), `dcaadb9` (feat)

## Files Created/Modified

- `.planning/research/schemas/drift.schema.json` - Parallel conflict record contract.
- `.planning/research/schemas/open-question.schema.json` - Blocker and resolution-routing contract.
- `.planning/research/schemas/compatibility.schema.json` - Immutable compatibility baseline contract.
- `tools/validate-research.py` - Optional record-family schema and semantic validation.
- `tests/phase1/test_drift.py` - Drift/open-question negative fixtures.
- `tests/phase1/test_compatibility.py` - Compatibility pin fixture.

## Decisions Made

- Keep conflicting normative and observed evidence visible rather than selecting a protocol winner.
- Require a compatibility pin to match its known source record exactly, preserving released and current-work evidence as distinct pins.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Repaired malformed compatibility schema JSON**
- **Found during:** Task 2
- **Issue:** The initial compact schema serialization was invalid JSON.
- **Fix:** Rewrote the schema in valid structured JSON before committing.
- **Files modified:** `.planning/research/schemas/compatibility.schema.json`
- **Verification:** Draft 2020-12 fixture test and complete Phase 1 suite pass.
- **Committed in:** `dcaadb9`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** Required for schema validation; no scope expansion.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Acquisition and refresh work can store uncertainty, source conflict, blocked work, and source-pinned compatibility without converting unknowns into settled facts.

## Self-Check: PASSED

All six plan artifacts exist; task commits `8d6a82c`, `787600b`, and `dcaadb9` resolve; no plan artifact has an intentional stub; `tools/phase1-python -m unittest discover -s tests/phase1`, `tools/phase1-python tools/validate-research.py validate --root .planning/research`, `tools/phase1-python tools/validate-planning.py`, and `git diff --check` passed.
