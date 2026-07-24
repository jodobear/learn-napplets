---
phase: 01-research-and-truth-baseline
plan: 10
subsystem: research-spikes
tags: [spike, static-framework, reproducibility, adr-0002, evidence]
requires:
  - 01-07 ecosystem catalog
  - 01-20 source-freshness evidence
  - 01-26 teaching scope
provides:
  - package-approved static-framework comparison evidence for ADR-0002 review
  - five-repeat, digest-pinned framework measurements
  - explicit VitePress accessibility-fixture blocker
affects: [ADR-0002, EVID-04, phase-2-framework-decision]
tech-stack:
  added: []
  patterns: [isolated npm installs, five-repeat deterministic replay, digest-pinned evidence]
key-files:
  created:
    - .planning/spikes/spk-b-static-framework/environment.json
    - .planning/spikes/spk-b-static-framework/measurements.yaml
    - .planning/spikes/spk-b-static-framework/report.md
  modified:
    - .planning/spikes/spk-b-static-framework/metadata.yaml
decisions:
  - Astro 7.1.3 is proposed ADR-0002 evidence only after five passing isolated fixture replays.
  - VitePress 1.6.4 is blocked from a positive ADR-0002 recommendation until a reviewed accessibility/static-equivalent fixture resolves its repeated assertion failure.
metrics:
  duration: 12m 28s
  completed: 2026-07-24
  tasks_completed: 3
  files_changed: 4
status: complete
---

# Phase 01 Plan 10: SPK-B Static Framework Evidence Summary

SPK-B now provides package-approved, five-repeat static-framework evidence for ADR-0002 without creating a production scaffold.

## Tasks Completed

| Task | Description | Commit |
| --- | --- | --- |
| 1 | Defined approved candidates, isolated experiment contract, and fixture | `406accb` |
| 2 | Recorded the operator's exact package approvals | `1419477` |
| 3 | Installed approved releases, measured five replays, and preserved evidence | `53c5b12` |

## Evidence Produced

- `environment.json` records actual Node, npm, Python, browser, package, executable, and command-digest facts.
- `measurements.yaml` preserves all five elapsed values, output digests, criteria, failures, and replay commands.
- `report.md` separates source inputs, observed behavior, inference, uncertainty, proposed recommendation, and required ADR approval.
- Astro `7.1.3` passed all five fixture replays with stable static-output digest `ec7e951d45a25fdcf0648263164a81e6709ade51ae8d9e3723bf3130b69eec94`.
- VitePress `1.6.4` produced stable output but failed its required reduced-motion accessibility assertion in all five replays; it remains blocked from a positive recommendation.

## Verification

Passed:

- `tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-b-static-framework --contract`
- `tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-b-static-framework --complete`
- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/learn-napplets-phase1-research-validation.json`
- `tools/phase1-python tools/validate-planning.py` (0 errors; expected pending Phase 1 warning)

`tools/phase1-python -m unittest discover` found no test modules and exited 5 (`NO TESTS RAN`). This repository has no Python test suite to execute; the plan's required spike and planning validators passed.

## Decisions Made

1. Treat the passing Astro result as **proposed evidence only** for ADR-0002; it does not authorize a framework or production scaffold.
2. Retain VitePress as an exact approved candidate but block a positive recommendation until a separately reviewed fixture proves the required accessibility/static-equivalent path.

## Deviations from Plan

### Auto-fixed Issues

1. **[Rule 1 - Bug] Corrected disposable fixture harness paths and SSR-safe lab script**
   - **Found during:** Task 3 measurement setup.
   - **Issue:** The initial disposable harness resolved VitePress output at the wrong path and ran its raw lab script during static rendering.
   - **Fix:** Corrected the SPK-B-local harness before the final five-repeat measurement; it was deleted with the disposable experiment after evidence capture.
   - **Commit:** Not committed; only the final measured evidence is retained.

2. **[Rule 1 - Bug] Added machine-readable report identity declarations**
   - **Found during:** Full Phase 1 research validation.
   - **Issue:** The report initially omitted the validator-required plain `SPK ID` and `Metadata path` declarations.
   - **Fix:** Added both declarations and re-ran the complete research validator successfully.
   - **Commit:** `53c5b12`

## Known Stubs

None.

## Threat Surface Scan

No new network endpoint, authentication path, file-access trust boundary, schema trust boundary, or production framework scaffold was introduced. Approved package code existed only in the deleted SPK-B-local disposable experiment.

## Self-Check: PASSED

All four SPK-B evidence files exist, and commits `406accb`, `1419477`, and `53c5b12` are present in the repository history.
