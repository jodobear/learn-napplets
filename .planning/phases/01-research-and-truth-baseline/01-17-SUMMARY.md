---
phase: 01-research-and-truth-baseline
plan: 17
subsystem: research-spike
tags: [spk-i, svg, accessibility, playwright, chromium, firefox, adr-0006]

requires:
  - phase: 01-07
    provides: approved isolated Phase 1 browser/toolchain baseline
  - phase: 01-20
    provides: evidence-policy and planning integrity conventions
  - phase: 01-26
    provides: deterministic local replay evidence conventions
provides:
  - non-production semantic SVG fixture with static transcript/table parity
  - reproducible installed-browser accessibility and determinism measurement runner
  - proposed ADR-0006 evidence that records the Firefox blocker without workaround
affects: [ADR-0006, Phase 04, Phase 05, A11Y-01]

tech-stack:
  added: []
  patterns:
    - direct-installed browser-only Playwright replay through tools/phase1-python
    - static-first SVG parity with keyboard, transcript, table, reduced-motion, and reset/replay checks

key-files:
  created:
    - .planning/spikes/spk-i-diagram-motion/fixture.svg
    - .planning/spikes/spk-i-diagram-motion/runner.py
    - .planning/spikes/spk-i-diagram-motion/environment.json
    - .planning/spikes/spk-i-diagram-motion/measurements.yaml
    - .planning/spikes/spk-i-diagram-motion/report.md
  modified:
    - .planning/spikes/spk-i-diagram-motion/metadata.yaml
    - .planning/spikes/spk-i-diagram-motion/recipe.md

key-decisions:
  - "Retain a data-driven semantic SVG as a proposed static-first ADR-0006 baseline; do not add a visual dependency or executable state controller."
  - "Keep ADR-0006 cross-browser evidence blocked because direct-installed Firefox exited before Playwright attached; use no launcher or configuration workaround."

patterns-established:
  - "Static-first visual evidence: every essential synthetic state appears in SVG, keyboard navigation, transcript, and ARIA table representations."
  - "Browser-blocker preservation: record exact installed-browser failure evidence and a safe static fallback instead of altering the approved environment."

requirements-completed: [EVID-04]

coverage:
  - id: D1
    description: "Non-production semantic SVG fixture with keyboard, transcript, table, reduced-motion, reset/replay, hostile-input, and sentinel contracts."
    requirement: EVID-04
    verification:
      - kind: automated_ui
        ref: "tools/phase1-python .planning/spikes/spk-i-diagram-motion/runner.py --fixture .planning/spikes/spk-i-diagram-motion/fixture.svg --out /tmp/spk-i-diagram-motion (Chrome five-sample result)"
        status: pass
      - kind: other
        ref: "tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-i-diagram-motion --complete"
        status: pass
    human_judgment: true
    rationale: "Semantic DOM coverage passed in Chrome, but actual assistive-technology speech and a Firefox fixture run remain unavailable."
  - id: D2
    description: "ADR-0006 measurement report with fixture, environment, output digests, candidate comparison, and the direct-installed Firefox block."
    requirement: EVID-04
    verification:
      - kind: other
        ref: "tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-i-diagram-motion/report.md"
        status: pass
      - kind: other
        ref: "tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/spk-i-research-validation.md"
        status: pass
    human_judgment: true
    rationale: "The report is valid evidence, but ADR acceptance and cross-browser sufficiency require human review."

metrics:
  duration: 20m 1s
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 17: Accessible Diagram/Motion Evidence Summary

**A zero-JavaScript semantic SVG passed five deterministic Chrome accessibility-equivalence samples, while the direct-installed Firefox launch blocker correctly leaves ADR-0006 cross-browser evidence proposed and blocked.**

## Performance

- **Duration:** 20m 1s
- **Started:** 2026-07-24T08:53:55Z
- **Completed:** 2026-07-24T09:13:56Z
- **Tasks:** 2/2
- **Files modified:** 7

## Accomplishments

- Created a non-production, synthetic, data-driven SVG fixture with semantic title/description, visible keyboard focus, transcript/table parity, static reduced-motion equivalence, and deterministic reset/replay targets.
- Added a reproducible local runner using only `tools/phase1-python`, approved Playwright 1.61.0, and direct-installed Chrome/Firefox; it neither installs browsers nor executes learner input.
- Recorded five passing Chrome samples, exact fixture/output digests, zero-JavaScript byte cost, hostile-input containment, trusted-host sentinel integrity, and the reproduced Firefox launch block for ADR-0006 review.

## Browser Outcomes

| Browser | Version | Outcome | Evidence |
| --- | --- | --- | --- |
| Google Chrome | 150.0.7871.124 | Passed | Five clean contexts passed 27 checks; initial, reduced-motion, and reset/replay screenshot digest was stable. |
| Firefox | 152.0.4 | Blocked | Exited with code 0 before Playwright attached; no fixture result was observed and no launcher/config workaround was applied. |

## Verification

Passed:

- `tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-i-diagram-motion --contract`
- `tools/phase1-python .planning/spikes/spk-i-diagram-motion/runner.py --fixture .planning/spikes/spk-i-diagram-motion/fixture.svg --out /tmp/spk-i-diagram-motion`
- `tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-i-diagram-motion --complete`
- `tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-i-diagram-motion/report.md`
- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/spk-i-research-validation.md`
- `git diff --check`

The runner returned a valid blocked evidence envelope: Chrome passed all declared local checks; Firefox remained blocked before context attachment.

## Task Commits

Each task was committed atomically:

1. **Task 1: Define the accessible deterministic diagram/motion comparison** — `59617f2` (`feat`)
2. **Task 2: Run SPK-I and report the accessibility/cost tradeoff** — `9eb79db` (`feat`)

## Files Created/Modified

- `.planning/spikes/spk-i-diagram-motion/metadata.yaml` — schema-valid planned/completed contract, hashes, measurements, and scope-limited blocker.
- `.planning/spikes/spk-i-diagram-motion/recipe.md` — candidate matrix, static-equivalence procedure, and safe failure/blocker handling.
- `.planning/spikes/spk-i-diagram-motion/fixture.svg` — synthetic accessible static diagram, keyboard links, transcript, table, and hostile-input sentinel material.
- `.planning/spikes/spk-i-diagram-motion/runner.py` — installed-browser-only five-sample measurement runner with no input execution or script injection.
- `.planning/spikes/spk-i-diagram-motion/environment.json` — reproducibility inventory and command hashes.
- `.planning/spikes/spk-i-diagram-motion/measurements.yaml` — candidate cost/accessibility measurements and browser outcomes.
- `.planning/spikes/spk-i-diagram-motion/report.md` — canonical ADR-0006 evidence report with proposed/blocked conclusion.

## Decisions Made

- Retained the static semantic SVG as the lowest-complexity proposed baseline because it passed Chrome's keyboard, parity, reset/replay, reduced-motion, deterministic screenshot, hostile-input, and sentinel checks without JavaScript or a visual dependency.
- Kept the overall ADR-0006 recommendation blocked for cross-browser acceptance: Firefox's direct-installed launch exited before automation attached, so no Firefox visual or accessibility conclusion is claimed.
- Did not install a visual dependency, create app components, add a dynamic state controller, or alter browser configuration.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed standalone-SVG screenshot capture timeout**
- **Found during:** Task 2 — browser measurement
- **Issue:** Playwright's full-page screenshot path timed out against the standalone fixed-size SVG, preventing valid Chrome evidence collection.
- **Fix:** Captured the fully visible fixed 1040×760 viewport instead; the inert SVG has no animation elements, and the resulting screenshots were byte-identical across all five samples.
- **Files modified:** `.planning/spikes/spk-i-diagram-motion/runner.py`
- **Verification:** Five Chrome samples passed and shared one initial/reduced-motion/reset screenshot digest.
- **Committed in:** `9eb79db` (part of Task 2)

**2. [Rule 2 - Missing Critical Functionality] Added an isolated reproducible browser runner**
- **Found during:** Task 2 — measurement setup
- **Issue:** The plan required five clean Chrome/Firefox accessibility and determinism measurements but did not declare the runnable harness needed to reproduce them.
- **Fix:** Added `runner.py` inside the disposable spike only. It uses approved Playwright and direct-installed browsers, retains generated artifacts in `/tmp`, and statically rejects executable fixture surfaces.
- **Files modified:** `.planning/spikes/spk-i-diagram-motion/runner.py`, `.planning/spikes/spk-i-diagram-motion/fixture.svg`
- **Verification:** Runner produced the digest-pinned Chrome pass and Firefox blocked envelope; completed spike validation passed.
- **Committed in:** `9eb79db` (part of Task 2)

---

**Total deviations:** 2 auto-fixed (1 Rule 1 bug, 1 Rule 2 critical reproducibility addition).
**Impact on plan:** Both changes are confined to SPK-I and necessary for valid, reproducible evidence. No production scope or unapproved dependency was added.

## Issues Encountered

- Direct-installed Firefox `152.0.4` again exited before Playwright `1.61.0` attached to a clean context. This is recorded as an evidence blocker, not auto-fixed, and no download, flag, profile, preference, or launcher workaround was used.
- Existing dirty generated `.planning/research/reports/validation.md` remained preserved at its prior `25` added lines; common research validation wrote only `/tmp/spk-i-research-validation.md`.

## User Setup Required

None — no external service, secret, browser download, or manual configuration is required.

## Next Phase Readiness

- ADR-0006 now has deterministic Chrome evidence for the static-first SVG candidate and an explicit static Phase 04 fallback.
- Human accessibility/security/content/product review is still required before ADR acceptance.
- The direct-installed Firefox/Playwright launcher mismatch remains a blocker for a positive cross-browser recommendation; preserve it until a separately approved environment change is available.

## Self-Check: PASSED

All seven SPK-I artifacts exist, and task commits `59617f2` and `9eb79db` resolve to commit objects on the current branch.
