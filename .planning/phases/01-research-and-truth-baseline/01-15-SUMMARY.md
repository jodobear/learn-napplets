--
phase: 01-research-and-truth-baseline
plan: 15
subsystem: research-evidence
tags: [supply-chain, package-conformance, immutable-evidence, blocker]
requires:
  - phase: 01
    provides: package map, CLM blocker, immutable policy baselines, and approved Phase 1 toolchain
provides:
  - Dated human block for unqualified package discovery pointer
  - Reproducible dependency-free SPK-G blocker evidence and immutable impact fragment
affects: [01-28-consolidation, phase-02-product-content-contract, ADR-0005, ADR-0008, ADR-0010]
tech-stack:
  added: []
  patterns: [public-root-export-only, exact-package-human-gate, dependency-free-blocker-replay]
key-files:
  created:
    - .planning/spikes/spk-g-package-conformance/recipe.md
    - .planning/spikes/spk-g-package-conformance/fixture.md
    - .planning/spikes/spk-g-package-conformance/environment.json
    - .planning/spikes/spk-g-package-conformance/measurements.yaml
    - .planning/spikes/spk-g-package-conformance/report.md
    - .planning/spikes/spk-g-package-conformance/impact-fragment.yaml
  modified:
    - .planning/spikes/spk-g-package-conformance/metadata.yaml
key-decisions:
  - Preserve CAND-NAPPLET-WEB-PACKAGE as blocked because no qualifying public release/export/source baseline is cataloged.
  - Treat zero package operations as dependency-free blocker evidence, not compatibility evidence.
patterns-established:
  - Public package consumption requires exact release, root export, provenance, license, integrity, immutable release and implementation baselines, and dated human approval.
  - Private, deep, workspace, source, distribution, and monorepo imports are rejected before fixture execution.
requirements-completed: [EVID-03, EVID-04]
coverage:
  - id: D1
    description: SPK-G public package gate and blocked consumer contract
    requirement: EVID-03
    verification:
      - kind: integration
        ref: tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-g-package-conformance --complete
        status: pass
    human_judgment: false
  - id: D2
    description: Immutable blocked package/conformance evidence hand-off
    requirement: EVID-04
    verification:
      - kind: integration
        ref: tools/phase1-python tools/validate-research.py validate-impact-fragment --root .planning .planning/spikes/spk-g-package-conformance/impact-fragment.yaml
        status: pass
    human_judgment: false
duration: 12min
completed: 2026-07-24
status: complete
--

# Phase 01 Plan 15: Public Package Conformance Summary

**Blocked public-package consumption contract with a dated supply-chain decision, five dependency-free replays, and a digest-pinned SPK-G impact hand-off.**

## Performance

- **Duration:** 12 min
- **Started:** 2026-07-24T08:36:59Z
- **Completed:** 2026-07-24T08:48:49Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Defined a disposable public-root-export-only fixture that rejects private and deep upstream paths.
- Recorded the dated human block for `CAND-NAPPLET-WEB-PACKAGE`; no package, package manager, registry, browser, or network operation ran.
- Preserved five zero-operation blocker replays, complete environment/measurement evidence, a canonical report, and `SPK-G-IMPACT-001` for Plan 01-28 consolidation.

## Task Commits

Each task was committed atomically:

1. **Task 1: Define exact public-export package/conformance consumers** - `d55e863` (feat)
2. **Task 2: Approve or block exact SPK-G package installation and conformance commands** - `90ddddb` (chore)
3. **Task 3: Execute SPK-G against approved public releases and preserve compatibility impacts** - `cb76bc5` (feat)

## Files Created/Modified

- `.planning/spikes/spk-g-package-conformance/metadata.yaml` - package gate, dated block, and completed replay evidence.
- `.planning/spikes/spk-g-package-conformance/recipe.md` - public release eligibility and no-substitution rules.
- `.planning/spikes/spk-g-package-conformance/fixture.md` - zero-import disposable consumer contract.
- `.planning/spikes/spk-g-package-conformance/environment.json` - reproducibility environment and command hashes.
- `.planning/spikes/spk-g-package-conformance/measurements.yaml` - five dependency-free blocked replays.
- `.planning/spikes/spk-g-package-conformance/report.md` - canonical blocked evidence report.
- `.planning/spikes/spk-g-package-conformance/impact-fragment.yaml` - immutable compatibility, drift, open-question, and ADR hand-off.

## Decisions Made

- Blocked `CAND-NAPPLET-WEB-PACKAGE` because the catalog lacks an exact public release/version, documented root export, provenance, license, integrity, and distinct immutable released-package and implemented-source baselines.
- Retained a dependency-free static fallback. Zero package operations show gate compliance only and do not constitute protocol or conformance evidence.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Completed metadata evidence fields required for validation**
- **Found during:** Task 3
- **Issue:** The Task 3 file list omitted `metadata.yaml`, but `validate-spike --complete` requires environment facts, measurements, output digests, replay result, evidence links, and a blocked record in that file.
- **Fix:** Added the required completed-state evidence fields while preserving the human package block and no-install outcome.
- **Files modified:** `.planning/spikes/spk-g-package-conformance/metadata.yaml`
- **Verification:** `validate-spike --complete` passed.
- **Committed in:** `cb76bc5`

---

**Total deviations:** 1 auto-fixed (Rule 3 blocking validation requirement).
**Impact on plan:** Required for the declared complete-spike validator; no scope expansion, package installation, or substitution occurred.

## Issues Encountered

- No cataloged public package release/export met the immutable CLM/SRC eligibility gate. This is the intended blocked outcome, preserved with dated human review rather than bypassed.

## Known Stubs

None. The zero-import fixture and unavailable package fields are intentional blocker evidence, not UI or runtime stubs.

## User Setup Required

None - no external service configuration or package installation is authorized.

## Next Phase Readiness

- Plan 01-28 can validate `SPK-G-IMPACT-001` and either consolidate its proposed open questions and drift records or retain them as explicit blockers.
- Phase 02 must not add a napplet package dependency unless a future collection supplies the complete public release/export evidence and a new dated human approval.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*

## Self-Check: PASSED
