---
phase: 01-research-and-truth-baseline
plan: 20
subsystem: source-freshness
status: complete
tags: [evidence, freshness, drift, refresh, spk-l]
requires: [01-07]
provides: [deterministic-source-freshness-fixture, review-work-routing-evidence]
affects: [ADR-0011, OPER-01]
tech-stack:
  added: []
  patterns: [local-fixture-replay, immutable-identity-comparison, stable-review-work]
key-files:
  created:
    - .planning/spikes/spk-l-source-freshness/metadata.yaml
    - .planning/spikes/spk-l-source-freshness/fixture.yaml
    - .planning/spikes/spk-l-source-freshness/recipe.md
    - .planning/spikes/spk-l-source-freshness/environment.json
    - .planning/spikes/spk-l-source-freshness/measurements.yaml
    - .planning/spikes/spk-l-source-freshness/report.md
  modified: []
decisions:
  - Local refresh scenarios retain canonical identity and route non-unchanged results to human review.
metrics:
  tasks_completed: 2
  files_modified: 6
  completed: 2026-07-24
---

# Phase 01 Plan 20: Source Freshness Summary

**SPK-L provides deterministic, local evidence that refresh comparison retains historical identity and routes changed, unavailable, ambiguous, and concurrent outcomes to bounded human review work without canonical-claim rewrites.**

## Accomplishments

- Defined seven fixture scenarios covering unchanged, changed digest, moved replacement, unavailable, ambiguous, repeated, and concurrent refresh behavior.
- Replayed each scenario with the approved isolated Python runner and captured environment, outcome, and report-digest evidence.
- Proved unchanged reruns do not duplicate review work, non-unchanged cases retain old identity, and a held lock prevents interleaved report writes.

## Task Commits

1. **Task 1: Define deterministic source-freshness scenarios** —  ()
2. **Task 2: Run SPK-L and demonstrate change routing without rewrite** —  ()

## Verification

Passed:

-  — 6 tests.
- 
- 
- 
- WARN PENDING001: Phase 1/source Phase 0 deliverables are pending as expected
Planning validation passed: 0 errors, 1 warning(s). — passed with expected pending-deliverables warning.

## Decisions Made

- Preserve canonical source and claim records as read-only refresh inputs; automation emits review work rather than interpreting or rewriting evidence.
- Treat changed and moved identities as review-required stale inputs, unavailable and ambiguous identities as blocked inputs, and concurrent refresh as a visible bounded retry condition.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Aligned SPK ID with required directory identity**
- **Found during:** Task 1
- **Issue:** The initial  ID did not match the mandated  directory-validation rule.
- **Fix:** Used , matching the deterministic spike directory.
- **Files modified:** , 
- **Commit:** 

**2. [Rule 3 - Blocking issue] Supplied validator-required report path**
- **Found during:** Task 2 verification
- **Issue:** The research-root validator requires a report target although the plan command omitted its required  argument.
- **Fix:** Passed the existing validation report target without staging its unrelated generated change.
- **Commit:** 

## Known Stubs

None. Zero-digest environment fields denote non-browser local-fixture placeholders required by the environment schema, not data flowing to a product surface.

## Threat Flags

None. The plan uses local, read-only fixture inputs and introduces no network, auth, endpoint, or production trust-boundary surface.

## Self-Check: PASSED

- Found all six declared SPK-L artifacts.
- Verified task commits  and  resolve in Git.
