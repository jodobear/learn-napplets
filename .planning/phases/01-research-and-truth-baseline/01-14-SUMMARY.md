---
phase: 01-research-and-truth-baseline
plan: 14
subsystem: research-spike
tags: [spk-f, portable-workbench, astro, vitepress, evidence, adr-0007]
requires:
  - phase: 01-10
    provides: approved static-framework package provenance and SPK-B accessibility evidence
  - phase: 01-11
    provides: direct-browser runner baseline and Firefox attachment blocker
  - phase: 01-13
    provides: shared-content parity fixture pattern
provides:
  - guest-only two-lesson SPK-F feasibility contract and package approval record
  - five-run Astro and VitePress disposable build evidence
  - blocked ADR-0007 input preserving cross-browser and VitePress accessibility blockers
affects: [ADR-0007, Phase 02 product contract, portable target, public-site sequence]
tech-stack:
  added: []
  patterns: [per-package human gate, ignored disposable experiment tree, digest-pinned measurement record]
key-files:
  created:
    - .planning/spikes/spk-f-course-workbench/metadata.yaml
    - .planning/spikes/spk-f-course-workbench/recipe.md
    - .planning/spikes/spk-f-course-workbench/fixture.md
    - .planning/spikes/spk-f-course-workbench/environment.json
    - .planning/spikes/spk-f-course-workbench/measurements.yaml
    - .planning/spikes/spk-f-course-workbench/report.md
  modified:
    - .gitignore
key-decisions:
  - "Astro 7.1.3 and VitePress 1.6.4 were installed only after dated SPK-F-specific human approval."
  - "SPK-F is a blocked ADR-0007 evidence result because Firefox exited before Playwright attachment; no portable outcome is selected."
  - "SPK-B's VitePress reduced-motion/static-equivalent blocker remains independent and unresolved."
patterns-established:
  - "Guest-only spikes use ignored .planning/spikes/*/.experiment/ storage and remove it after digest capture."
requirements-completed: [EVID-04]
coverage:
  - id: D1
    description: "Guest-only SPK-F contract with exact human-approved package gates"
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-f-course-workbench --contract"
        status: pass
    human_judgment: true
    rationale: "Package legitimacy approval is intentionally a blocking human trust decision."
  - id: D2
    description: "Five-run portable feasibility evidence and blocked ADR-0007 recommendation"
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-f-course-workbench --complete"
        status: pass
      - kind: integration
        ref: "tools/phase1-python tools/validate-planning.py"
        status: pass
    human_judgment: true
    rationale: "Firefox runtime compatibility remains blocked and ADR-0007 acceptance requires separate human roles."
metrics:
  duration: 6h 18m 46s
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 14: SPK-F Portable Feasibility Summary

**Guest-only Astro and VitePress two-lesson prototype evidence with human-gated installs, deterministic five-run builds, and a blocked cross-browser ADR-0007 input.**

## Performance

- **Duration:** 6h 18m 46s
- **Started:** 2026-07-24T02:13:28Z
- **Completed:** 2026-07-24T08:32:14Z
- **Tasks:** 3/3
- **Files modified:** 7

## Accomplishments

- Created a non-production SPK-F contract and representative two-lesson fixture that labels all UI as guest-only simulation and prohibits host imports and private-frame composition claims.
- Recorded dated human approval for exactly `astro@7.1.3` and `vitepress@1.6.4`, then installed each only in an ignored disposable SPK-F path with lifecycle scripts disabled.
- Captured five deterministic static builds, artifact sizes, build timing, memory, Chromium behavior, capability degradation, and a Firefox attachment blocker; removed the disposable experiment afterward.
- Produced a blocked, proposed ADR-0007 evidence result without selecting a delivery outcome or affecting public-site sequencing.

## Task Commits

1. **Task 1: Define SPK-F portable feasibility candidates and fixture** — `289d4ab` (feat)
2. **Task 2: Approve or block exact SPK-F prototype package installs** — `828e0c0` (docs)
3. **Task 3: Run SPK-F and document an ADR 0007 recommendation or blocker** — `9d488bc` (feat)

## Files Created/Modified

- `.planning/spikes/spk-f-course-workbench/metadata.yaml` — contract, approval decisions, completed measurements, and blocked outcome.
- `.planning/spikes/spk-f-course-workbench/recipe.md` — guest-only isolation, package-gate, and replay procedure.
- `.planning/spikes/spk-f-course-workbench/fixture.md` — two lessons, transcript, code example, assessment, source metadata, and capability states.
- `.planning/spikes/spk-f-course-workbench/environment.json` — runtime, browser, package manifest, and command-digest facts.
- `.planning/spikes/spk-f-course-workbench/measurements.yaml` — five-run build, artifact, memory, browser, and boundary observations.
- `.planning/spikes/spk-f-course-workbench/report.md` — proposed blocked ADR-0007 evidence report.
- `.gitignore` — ignores all disposable Phase 1 spike experiment trees.

## Decisions Made

- Required a fresh SPK-F-specific dated human approval for both exact package versions, rather than treating earlier SPK-B approval as sufficient.
- Treated the direct-installed Firefox failure as a blocked result matching SPK-C, not as permission to change browser configuration or select an ADR outcome.
- Retained SPK-B's distinct VitePress accessibility assertion failure; SPK-F Chromium rendering does not supersede it.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected Astro fixture code literal parsing and capability-state evidence**
- **Found during:** Task 3
- **Issue:** The initial disposable Astro page embedded unescaped JavaScript object braces in template content, causing the first build to fail; its initial emitted output also did not expose the present-capability branch for the deterministic output check.
- **Fix:** Rendered the illustrative code as a template literal and made both declared capability states explicit in the disposable fixture output before repeating all five measurements.
- **Files modified:** ignored SPK-F `.experiment/` sources only; removed after evidence capture.
- **Verification:** Both five-run builds completed with stable output digests; Chromium exercised Astro's capability-present toggle and reset-to-absent behavior.
- **Committed in:** `9d488bc` (Task 3 evidence records)

**2. [Rule 1 - Bug] Supplied required five-sample browser measurement arrays**
- **Found during:** Task 3 complete-spike validation
- **Issue:** The completed-spike validator requires every metric to carry five raw values whenever browser execution is recorded.
- **Fix:** Recorded five identical bounded Chromium and Firefox attachment-count values with exact range and median, preserving the Firefox zero result.
- **Files modified:** `.planning/spikes/spk-f-course-workbench/metadata.yaml`
- **Verification:** `validate-spike --complete` passed.
- **Committed in:** `9d488bc` (Task 3)

**3. [Rule 3 - Blocking] Ignored disposable SPK-F installation storage**
- **Found during:** Task 3
- **Issue:** The declared `.experiment/` path was not covered by the repository ignore rules, so isolated package installation could leave untracked dependency trees.
- **Fix:** Added `.planning/spikes/*/.experiment/` to `.gitignore`, verified the path is ignored, and removed the full SPK-F experiment tree after digest capture.
- **Files modified:** `.gitignore`
- **Verification:** `git check-ignore` matched the path; no experiment tree remained after measurement.
- **Committed in:** `9d488bc` (Task 3)

**Total deviations:** 3 auto-fixed (2 Rule 1, 1 Rule 3).
**Impact on plan:** All changes were required to build the planned disposable fixture, accurately capture complete evidence, and preserve the no-untracked-dependency boundary. No production scaffold or substitute dependency was introduced.

## Issues Encountered

- The package-local VitePress `--help` invocation launched a process instead of completing as a help command; it was stopped without changing package configuration. Local package documentation was read instead.
- Firefox 152.0.4 exited before approved Playwright 1.61.0 attached. This matches the existing SPK-C blocker and leaves SPK-F blocked rather than creating a retry configuration or an ADR recommendation.

## Known Stubs

None. The fixture's capability-present and capability-absent paths are explicitly labeled simulations; they are intentional scope boundaries, not unwired product behavior.

## Next Phase Readiness

- SPK-F provides reproducible, human-gated portable-target feasibility evidence for ADR-0007 review.
- The portable target remains blocked on Firefox runtime evidence, current immutable upstream artifact/runtime sources, and separate human ADR approval.
- Public-site work remains independent of this optional portable experiment.

## Self-Check: PASSED

Verified all six SPK-F artifacts and task commits `289d4ab`, `828e0c0`, and `9d488bc` exist.
