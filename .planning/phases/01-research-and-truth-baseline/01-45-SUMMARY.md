---
phase: 01-research-and-truth-baseline
plan: 45
subsystem: evidence-acquisition
tags: [python, github-api, immutable-content, sha256, reviewed-git-blobs]

requires:
  - phase: 01-research-and-truth-baseline
    provides: Plan 01-29 Git-blob review binding and Plan 01-44 certified Phase 1 wrapper
provides:
  - bounded public GitHub collection for five immutable observed implementation/release targets
  - review-bound queue and receipt containing seven complete bounded observations
  - additive acquisition and candidate history with a retained failed-locator record
affects: [01-30, 01-31, 01-32, 01-33, 01-35, 01-43]

tech-stack:
  added: []
  patterns: [no-redirect HTTPS transport, immutable commit-tree-blob validation, review-bound receipt validation, non-normative observed evidence]

key-files:
  created:
    - .planning/research/upstream-acquisition-queue.yaml
    - .planning/research/reports/upstream-acquisition-20260728.md
  modified:
    - tools/acquire-sources.py
    - tests/phase1/test_evidence.py
    - .planning/research/acquisition-log.yaml
    - .planning/research/candidate-source-manifest.yaml

key-decisions:
  - "Bind both queue and receipt to the exact Plan 01-29 reviewed commit, four report digests, parser version, and parsed-record digest before downstream consumption."
  - "Retain the approved malformed PR211 locator as a scoped failed outcome rather than substitute the different 40-hex commit in the reviewed report."
  - "Keep implementation and release bytes observed-only, with no canonical source insertion, protocol authority decision, package admission, or ADR acceptance."

patterns-established:
  - "Public collection validates repository identity, immutable commit/tree/blob metadata, exact raw-byte SHA-256, and cache confinement before retaining an observed outcome."
  - "A bounded source discrepancy is appended as failure history and never becomes permission to crawl, correct the locator, or replace a candidate."

requirements-completed: [EVID-01, EVID-03, OPER-03]
coverage:
  - id: D1
    description: Fixture-backed immutable source collector and seven-dimension blocked compatibility classifier
    requirement: EVID-03
    verification:
      - kind: unit
        ref: tests/phase1/test_evidence.py#BoundedCollectorTests.test_candidate_acquisition_tracer_blocks_incomplete_dimensions
        status: pass
      - kind: unit
        ref: tests/phase1/test_evidence.py#BoundedCollectorTests.test_acquisition_queue_uses_only_reviewed_git_blob_refresh_inputs
        status: pass
    human_judgment: false
  - id: D2
    description: Bounded public acquisition queue, receipt, and reviewed-source binding validator
    requirement: EVID-01
    verification:
      - kind: integration
        ref: tools/phase1-python tools/acquire-sources.py validate-reviewed-acquisition --queue .planning/research/upstream-acquisition-queue.yaml --receipt .planning/research/reports/upstream-acquisition-20260728.md --review .planning/phases/01-research-and-truth-baseline/01-REVIEWS.md
        status: pass
      - kind: integration
        ref: tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/phase1-acquisition-validation.md
        status: pass
    human_judgment: false
  - id: D3
    description: Exact approved public-read scope records observed source bytes while retaining the invalid PR211 locator as blocked failure evidence
    requirement: OPER-03
    verification:
      - kind: integration
        ref: tools/phase1-python tools/acquire-sources.py collect --queue .planning/research/upstream-acquisition-queue.yaml --receipt .planning/research/reports/upstream-acquisition-20260728.md --cache-root .research/upstreams
        status: pass
    human_judgment: true
    rationale: Human authority review remains required before observed implementation/release material can be accepted as canonical or normative evidence.

metrics:
  duration: continuation session
  completed: 2026-07-30
status: complete
---

# Phase 01 Plan 45: Bounded Public Acquisition History Summary

**A review-bound, cache-confined GitHub collector retained five immutable observed implementation/release byte captures, a napplet/naps zero-result checkpoint, and one exact-scope failed locator without promoting any material to protocol or canonical authority.**

## Performance

- **Duration:** Continuation session
- **Completed:** 2026-07-30
- **Tasks:** 2/2
- **Files modified:** 7 task artifacts

## Accomplishments

- Completed the fixture-only immutable candidate tracer from Task 1, including the seven-dimension blocked compatibility result and Git-blob-only refresh-input regression.
- Added a read-only no-redirect collector that requires public repository identity, immutable commit/tree/blob agreement, exact raw-byte SHA-256, and ignored `.research/upstreams/` cache confinement.
- Collected five approved immutable `commit:path` byte targets, preserved the bounded `napplet/naps` zero-result identity/default-branch observation, and recorded every result as observed-only evidence.
- Generated a queue and receipt bound to reviewed commit `1a9449be4d74aa1ceed235d949802266846cf63b`, all four refresh-report SHA-256 values, parser version, and deterministic parsed-record digest.
- Preserved `ACQ-FAIL-001`, prior discovery pointers, and candidate history while adding all Task 2 outcomes additively.

## Task Commits

1. **Task 1: Trace one immutable public candidate to staged blocked compatibility evidence** — `37acf87` (RED), `ad5b038` (GREEN), `cc33d14` (parser correction)
2. **Task 2: Collect the bounded public window and retain additive review-ready history** — `312e4c7` (RED), `3c8cf36` (GREEN)

## Files Created/Modified

- `tools/acquire-sources.py` — bounded collector, no-redirect HTTPS transport, immutable tree/blob checks, review-binding validation, and additive history generation.
- `tests/phase1/test_evidence.py` — receipt/queue binding regression that rejects altered report digests.
- `.planning/research/upstream-acquisition-queue.yaml` — seven reviewed-source-bound bounded observations with immutable targets and impact/refresh metadata.
- `.planning/research/reports/upstream-acquisition-20260728.md` — retrieved bytes, SHA-256 values, repository identity fields, scoped failure, and observed-only classifications.
- `.planning/research/acquisition-log.yaml` — retained `ACQ-FAIL-001` plus dated additive collection outcomes.
- `.planning/research/candidate-source-manifest.yaml` — retained discovery pointers plus new separate observed candidates.

## Verification

Passed:

- `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_evidence` — 15 tests.
- Both Task 1 focused tracer/reviewed-input tests.
- Task 2 collection command under the certified wrapper.
- `validate-reviewed-acquisition` against the generated queue and receipt.
- `tools/validate-research.py validate --root .planning/research --report /tmp/phase1-acquisition-validation.md`.
- `tools/phase1-python --verify-toolchain` and Plan 01-29 `--verify-phase1-source-inputs` review-binding verification.
- `git diff --check` for the Task 2 commit.

## Decisions Made

- Implemented an explicit no-redirect handler so a public response cannot expand the approved host scope.
- Kept cached upstream bytes only below ignored `.research/upstreams/`; tracked artifacts retain only locators, metadata, and SHA-256 values.
- The receipt has no approval field and explicitly labels all collected code/release data as observed, non-normative material pending Plans 01-30 and 01-31 human gates.

## Deviations from Plan

None — the exact approval scope required the PR211 mismatch to remain a failed receipt outcome rather than a substitution.

## Issues Encountered

- The approved PR211 immutable commit string is 37 hexadecimal characters, while the exact reviewed report records a different 40-hex commit. The collector made no PR211 public request and retained an impact-scoped `failed` record stating that no substitute or scope expansion was attempted.

## Known Stubs

None.

## Threat Flags

None — the collector's public HTTPS, cache, source-classification, and history-retention surfaces are covered by Plan 01-45 threat mitigations T-45-01 through T-45-06.

## Next Phase Readiness

- Plans 01-30 and 01-31 can inspect a review-bound, non-normative receipt without rerunning the bounded read window.
- PR211 remains blocked on an explicitly approved, correctly formed immutable locator; a future correction requires a new human approval rather than automatic substitution.
- Required ignored assets for the merge handoff are `.research/phase1-wheelhouse/`, `.research/phase1-certified-tools-4/`, `.research/phase1-installer-report-4.json`, `.research/phase1-tools/`, and `.research/upstreams/`.

## Self-Check: PASSED

- Confirmed all seven Task 1/Task 2 artifacts and this summary exist in the durable worktree.
- Confirmed all three Task 1 commits and both Task 2 RED/GREEN commits are reachable.
- Confirmed no tracked-file deletions, stub markers, or whitespace errors in the Task 2 commit.
