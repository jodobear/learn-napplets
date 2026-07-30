---
phase: 01-research-and-truth-baseline
plan: 33
subsystem: research-evidence-validation
tags: [python, unittest, sha256, deterministic-refresh, replay-safety]
requires:
  - phase: 01-45
    provides: bounded public acquisition history used by the research baseline
provides:
  - Digest-bound retained spike evidence with fixed wrapper replay arguments
  - One deterministic result per source observation set
  - Hermetic evidence-validation test output
affects: [phase-01-consolidation, evidence-review, source-refresh]
tech-stack:
  added: []
  patterns:
    - Normalize JSON observations before source-level reduction.
    - Use temporary report destinations for evidence validation tests.
key-files:
  created: []
  modified:
    - tools/validate-research.py
    - .planning/spikes/replay-manifest.yaml
    - tools/refresh-sources.py
    - tests/phase1/test_spikes.py
    - tests/phase1/test_drift.py
    - tests/phase1/test_evidence.py
key-decisions:
  - "Replay arguments derive only from stable SPIKE_REPORTS mappings."
  - "Duplicate observations collapse by normalized JSON bytes; conflicts become one ambiguous work item."
  - "Evidence validation tests write only temporary reports."
patterns-established:
  - "Retained output evidence is confined, regular-file-only, and SHA-256-bound."
  - "Refresh produces review work only and never source or claim authorization."
requirements-completed: [EVID-01, EVID-04, OPER-01, OPER-03]
coverage:
  - id: D1
    description: "Retained spike bytes and replay mapping are digest-bound and fixed-wrapper-only."
    requirement: EVID-01
    verification:
      - kind: unit
        ref: "tests/phase1/test_spikes.py and replay-spikes --check"
        status: pass
    human_judgment: false
  - id: D2
    description: "Refresh duplicates reduce to one stable source result and conflicts become one ambiguous digest-listed review item."
    requirement: OPER-01
    verification:
      - kind: unit
        ref: "tests/phase1/test_drift.py#RefreshComparisonTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "Evidence validation report output is temporary and canonical report bytes remain unchanged."
    requirement: EVID-04
    verification:
      - kind: unit
        ref: "tests/phase1/test_evidence.py#SourceEvidenceTests.test_evidence_validation_uses_temporary_report_without_canonical_mutation"
        status: pass
    human_judgment: false
duration: resumed execution; duration not reconstructed
completed: 2026-07-30
status: complete
---

# Phase 01 Plan 33: Deterministic Evidence Replay and Refresh Summary

**Digest-bound retained spike replay, fixed wrapper arguments, deterministic refresh review work, and canonical-report-safe evidence tests.**

## Performance

- **Duration:** Resumed execution; duration not reconstructed.
- **Tasks:** 2 completed through TDD RED and GREEN commits.
- **Files modified:** 15 plan-owned files.
- **Verification:** 30 Plan 01-33 tests plus replay manifest check passed.

## Accomplishments

- Bound completed spike declarations to confined retained bytes, exact SHA-256 values, and fixed stable-ID replay argv rather than YAML command text.
- Collapsed byte-identical refresh observations and reduced conflicting observations for one source to one stable ambiguous work item with sorted normalized-observation digests.
- Wrote evidence-validation reports to temporary destinations and proved canonical validation report bytes are unchanged.

## Task Commits

1. **Task 1 RED: retained evidence and replay regressions** - `171a032` (test)
2. **Task 1 GREEN: retained evidence and fixed replay binding** - `1e56c34` (feat)
3. **Task 2 RED: deterministic refresh regressions** - `937024b` (test)
4. **Task 2 GREEN: duplicate refresh reduction and evidence isolation** - `bd911c4` (feat)

## Files Created/Modified

- `tools/validate-research.py` - Resolves retained evidence safely and derives replay argv from stable mappings.
- `.planning/spikes/replay-manifest.yaml` - Stores digest-pinned replay metadata without executable authority.
- `.planning/spikes/spk-{a,b,e,f,h,i,j,k,l}-*/metadata.yaml` - Contains retained evidence repairs for nine spike records.
- `tools/refresh-sources.py` - Normalizes and reduces refresh observations before review-work rendering.
- `tests/phase1/test_spikes.py` - Covers retained output confinement, digest binding, and replay substitution rejection.
- `tests/phase1/test_drift.py` - Covers duplicate and conflicting refresh reduction.
- `tests/phase1/test_evidence.py` - Covers canonical report isolation in SourceEvidenceTests.

## Decisions Made

- Refresh preserves old pins and does not rewrite source, claim, drift, question, or ADR content.
- Conflicting observations become one explicit ambiguous result with sorted digests, not an automatic interpretation.
- Canonical evidence reports are read-only test inputs; test reports live under TemporaryDirectory paths.

## Deviations from Plan

### User-authorized Task 1 metadata deviation

- **Scope:** Nine spike metadata records: SPK-A, SPK-B, SPK-E, SPK-F, SPK-H, SPK-I, SPK-J, SPK-K, and SPK-L.
- **Reason:** Retained-evidence binding required concrete metadata repairs so declarations reference real retained output bytes and exact digests.
- **Outcome:** The records are plan-owned research evidence metadata covered by retained-output and replay regressions.
- **Commit:** `1e56c34`.

### Auto-fixed Issues

**1. [Rule 1 - Bug] Placed canonical-mutation isolation coverage in the named test class and made it self-contained.**
- **Found during:** Task 2 verification.
- **Issue:** The named Task 2 test referenced SourceEvidenceTests, but its method was initially on SourceEvidenceValidationTests; the named test could not be discovered and then lacked its helper after relocation.
- **Fix:** Located the test in SourceEvidenceTests and invoked the validator directly with existing subprocess and interpreter fixtures.
- **Files modified:** `tests/phase1/test_evidence.py`.
- **Verification:** All three named Task 2 tests pass.
- **Commit:** `bd911c4`.

---

**Total deviations:** 1 auto-fixed Rule 1 bug and 1 user-authorized Task 1 metadata deviation.
**Impact on plan:** Both changes enforce planned evidence and test-isolation behavior without expanding authority or product scope.

## Execution Environment

The primary checkout transferred missing canonical traceability and governance support inputs byte-for-byte into this stopped worktree before resumption. They were used only as uncommitted execution support inputs and were neither modified nor staged: `.planning/config.json`, `.planning/governance/`, `.planning/traceability/`, `.planning/validation/required-artifacts.json`, and `CLAUDE.md`. This transfer is not a product or plan change.

## Verification

Passed:

- `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent test_drift.RefreshComparisonTests.test_conflicting_refresh_observations_are_one_ambiguous_result test_evidence.SourceEvidenceTests.test_evidence_validation_uses_temporary_report_without_canonical_mutation`
- `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes test_drift test_evidence`
- `tools/phase1-python tools/validate-research.py replay-spikes --manifest .planning/spikes/replay-manifest.yaml --check`

## Known Stubs

None.

## Next Phase Readiness

Plan 01-33 provides deterministic, hermetic evidence replay and refresh behavior for later research consolidation. No external setup or network action occurred.

## Self-Check: PASSED

- All fifteen plan-owned modified files exist in the pinned worktree.
- Task commits `171a032`, `1e56c34`, `937024b`, and `bd911c4` exist.
- Only declared support inputs remain untracked; they were not staged.
