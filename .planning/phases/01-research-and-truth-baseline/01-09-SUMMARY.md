---
phase: 01-research-and-truth-baseline
plan: 09
subsystem: workspace-research-spike
status: complete
tags: [spk-a, workspace, evidence, adr-0001, non-production]
requires: [01-07, 01-20, 01-26]
provides: [reproducible workspace comparison, proposed ADR-0001 evidence]
affects: [phase-2-content-contract, phase-3-workspace-design]
tech-stack:
  added: []
  patterns: [text-only isolated fixture, five-sample replay, digest-pinned measurement]
key-files:
  created:
    - .planning/spikes/spk-a-workspace/metadata.yaml
    - .planning/spikes/spk-a-workspace/recipe.md
    - .planning/spikes/spk-a-workspace/fixture.md
    - .planning/spikes/spk-a-workspace/environment.json
    - .planning/spikes/spk-a-workspace/measurements.yaml
    - .planning/spikes/spk-a-workspace/report.md
  modified: []
decisions:
  - Candidate A is the narrowest proposed public-site-first repository boundary model; ADR-0001 remains proposed.
  - The text-only comparison cannot select a framework, package manager, runtime, bundle, or deployment system.
metrics:
  tasks_completed: 2
  files_modified: 6
  completed: 2026-07-24
---

# Phase 01 Plan 09: Isolated Workspace Comparison Summary

**SPK-A supplies digest-pinned, five-sample evidence for a proposed public-site-first workspace boundary model without creating any production workspace marker.**

## Accomplishments

- Defined a non-production SPK-A contract with explicit variables, criteria, success/failure/blocked outcomes, source bindings, and replay controls.
- Compared three text-only candidate layouts against public-site, shared-content, host-only, guest-entry, testability, bundle, and deployment boundaries.
- Replayed the local assertion five times, recorded environment and input/output digests, and retained Candidate A as a proposed ADR-0001 input.

## Task Commits

1. **Task 1: Specify and fixture the isolated workspace comparison** — `25d6ca9` (`feat`)
2. **Task 2: Execute SPK-A and report a recommendation or blocker** — `332e03b` (`feat`)

## Verification

Passed:

- `tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-a-workspace --contract`
- `tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-a-workspace --complete`
- `tools/phase1-python tools/validate-planning.py` — passed with expected `PENDING001` warning.
- `tools/phase1-python -m unittest discover -s tests/phase1` — 34 tests passed.

## Decisions Made

- Retain Candidate A as the narrowest public-site-first conceptual boundary model for proposed ADR-0001 review.
- Keep Candidate C as a broader equivalent hypothesis and Candidate B as the negative control.
- Do not promote the comparison into a production workspace, dependency manifest, source tree, or deployment configuration.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Repaired report contract declarations**
- **Found during:** Task 2 full-suite verification
- **Issue:** The first report rendering lost required literal SPK ID and metadata-path declarations during shell interpolation, causing `RPT004`.
- **Fix:** Rewrote the local report with literal `SPK ID: SPK-A-WORKSPACE` and `Metadata path: metadata.yaml` declarations, then refreshed its digest reference.
- **Files modified:** `.planning/spikes/spk-a-workspace/report.md`, `.planning/spikes/spk-a-workspace/metadata.yaml`
- **Commit:** `332e03b`

**2. [Rule 2 - Missing critical functionality] Added completed-evidence metadata fields**
- **Found during:** Task 2 completion design
- **Issue:** The complete spike validator requires environment facts, five-sample measurements, raw output digests, replay result, and evidence links in the SPK envelope.
- **Fix:** Added those required, digest-pinned fields to the Task 1 metadata contract when recording Task 2 results.
- **Files modified:** `.planning/spikes/spk-a-workspace/metadata.yaml`
- **Commit:** `332e03b`

## Known Stubs

None. Candidate layouts are intentionally text-only research fixtures and do not flow to a product runtime.

## Threat Flags

None. The spike adds only local evidence artifacts, has no network or authentication surface, and validates the production-marker boundary.

## Self-Check: PASSED

- Found all six declared SPK-A artifacts at their expected paths.
- Verified task commits `25d6ca9` and `332e03b` resolve in Git.
