---
phase: 01-research-and-truth-baseline
plan: 05
subsystem: evidence-acquisition
status: complete
tags: [evidence, provenance, source-acquisition, claims]
requires: [01-03, 01-04]
provides:
  - Bounded read-only source collector with HTTPS allowlist and Git blob pinning
  - Candidate authority manifest, acquisition log, and ecosystem dispositions
  - Source-linked policy claims and an explicitly blocked protocol map
affects: [01-06, phase-1-compatibility, phase-1-spikes]
tech-stack:
  added: [Python standard library collector]
  patterns: [immutable revision:path pinning, blocked-not-inferred evidence state]
key-files:
  created:
    - tools/acquire-sources.py
    - .planning/research/acquisition-log.yaml
    - .planning/research/candidate-source-manifest.yaml
    - .planning/research/ecosystem-inventory.yaml
    - .planning/research/protocol-map.md
    - .planning/research/terminology-map.yaml
  modified:
    - .planning/research/source-registry.yaml
    - .planning/research/claims.yaml
    - tests/phase1/test_evidence.py
decisions:
  - No mutable discovery pointer is treated as protocol evidence; incomplete candidates remain impact-scoped blocked.
  - Local project policy is recorded separately from upstream facts and cannot verify a protocol conclusion.
metrics:
  tasks_completed: 2
  commits: 3
  completed: 2026-07-24
---

# Phase 01 Plan 05: Bounded Tier 1 Evidence Baseline Summary

A read-only, allowlisted collector and reproducible candidate manifest now retain only immutable evidence records or explicit impact-scoped blockers, with no inferred NIP/NAP protocol claims.

## Tasks Completed

1. **Acquire bounded Tier 1 sources as immutable evidence records**
   - Added `tools/acquire-sources.py`, which rejects non-allowlisted HTTPS inputs without cache writes and resolves a local Git ref to a commit, exact blob, and SHA-256 digest.
   - Added a bounded candidate manifest, acquisition/failure log, and ecosystem inventory; all unresolved upstream candidates are explicitly blocked or deferred rather than filled from memory.
   - Updated source registry with two immutable project-policy records only.
   - Commits: `b534103`, `0d18f9e`.

2. **Derive claim, terminology, and protocol maps from the pinned registry**
   - Added a source-linked policy claim and an impact-scoped blocked baseline claim.
   - Added protocol and terminology maps that distinguish policy from upstream evidence and leave NIP/NAP behavior and first-lab selection blocked.
   - Commit: `82f4db4`.

## Verification

Passed:

- `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_evidence.py'` — 8 tests.
- `tools/phase1-python -m unittest discover -s tests/phase1` — 29 tests.
- `tools/phase1-python tools/acquire-sources.py --help`.
- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md`.
- `tools/phase1-python tools/validate-planning.py` — passed with the expected Phase 1 pending-deliverables warning.

`tools/phase1-python tools/validate-planning.py --phase-1-complete` correctly remains unavailable: later plans have not yet created required Phase 1 artifacts (compatibility, drift, executive/decision summaries, security findings, and lesson packets). This is not a Plan 01-05 failure and was not treated as a phase pass.

## Decisions Made

- Discovery URLs are cataloguing inputs, not immutable evidence.
- Acquisition failure blocks only dependent protocol/compatibility/first-lab work and records a safe defer path.
- Project policy records may govern evidence handling but cannot establish an upstream protocol fact.

## Deviations from Plan

### Auto-fixed Issues

1. **[Rule 3 - Blocking issue] Corrected the RED-test command shell variable**
   - **Found during:** Task 1 RED run.
   - **Issue:** `status` is read-only in the active zsh shell, preventing the intended post-test commit sequence.
   - **Fix:** Re-ran the already-failing RED test and committed it without using the reserved shell variable.
   - **Files modified:** None.
   - **Commit:** `b534103`.

## Known Stubs

None. Blocked source candidates are deliberate evidence states with impact, fallback, approver, and refresh information; they do not substitute for missing data.

## Self-Check: PASSED

- Found collector, candidate manifest, acquisition log, source registry, claims, protocol map, and terminology map.
- Found task commits `b534103`, `0d18f9e`, and `82f4db4`.
