---
phase: 01-research-and-truth-baseline
plan: 48
subsystem: static learning site
tags: [static-site, accessibility, evidence-labels, python-stdlib, chromium]

requires:
  - phase: 01-46
    provides: evidence-safety and recovery controls
  - phase: 01-47
    provides: immutable truth-refresh records for the public content contract
provides:
  - dependency-free generated learning pages and shared knowledge JSON
  - evidence/status labels and a static authority-boundary transcript
  - local Chromium coverage of the complete learning path
  - reproducible loopback preview instructions
affects: [phase-01-verification, phase-02-product-content-contract, accessibility, knowledge-outputs]

tech-stack:
  added: [Python standard library static generator, authored CSS, local progressive JavaScript, approved Chromium Playwright]
  patterns: [structured-content-to-static-output, local-only assets, static-first progressive enhancement, evidence-labeled records]

key-files:
  created:
    - site/content/site.json
    - site/assets/styles.css
    - site/assets/site.js
    - site/README.md
    - tests/site/test_site_browser.py
  modified:
    - tools/build-site.py
    - site/templates/page.html
    - site/dist/index.html
    - site/dist/learn/index.html
    - site/dist/architecture/index.html
    - site/dist/sources/index.html
    - tests/site/test_static_site.py

key-decisions:
  - "Generate human HTML, knowledge JSON, and local static assets from a single stdlib-only build path."
  - "Keep the authority model, transcript, table, source IDs, and blockers in static HTML; JavaScript only adds an optional resettable reading trace."
  - "Use an ink-and-paper editorial field-guide system with explicit host, guest, blocked, and evidence treatments instead of dashboard cards or external design dependencies."
  - "Treat retained Phase 1 PRE118 and source-registry failures as deferred evidence-system gaps, not as static-site defects."

patterns-established:
  - "Static equivalent first: every essential interaction is rendered in HTML before optional JavaScript runs."
  - "Local-only verification: generated pages use relative local assets and browser request observation rejects required external dependencies."

requirements-completed: [EVID-01, EVID-02, EVID-03, OPER-03]

coverage:
  - id: D1
    description: "One structured content contract generates four evidence-labeled HTML pages and shared knowledge JSON."
    requirement: EVID-01
    verification:
      - kind: integration
        ref: "python3 -m unittest discover -s tests/site -p 'test_static_site.py' -v"
        status: pass
    human_judgment: false
  - id: D2
    description: "Responsive editorial learning interface keeps static transcript, table, source labels, focus treatment, print output, forced-color support, and reduced-motion safeguards."
    requirement: OPER-03
    verification:
      - kind: automated_ui
        ref: "tests/site/test_site_browser.py"
        status: pass
    human_judgment: true
    rationale: "Automated checks prove semantic, keyboard, responsive, no-script, and reduced-motion contracts; a reviewer should still judge visual reading rhythm and information hierarchy."
  - id: D3
    description: "The local start-to-learn-to-architecture-to-sources path runs in approved Chromium without a required external request."
    requirement: EVID-03
    verification:
      - kind: e2e
        ref: "approved Chromium observation at http://127.0.0.1:8766/"
        status: pass
    human_judgment: false

metrics:
  duration: 17min
  completed: 2026-07-31
  status: complete
---

# Phase 01 Plan 48: Static Evidence Learning Site Summary

**A dependency-free editorial field guide turns one evidence-labeled record into a responsive authority-boundary learning path, machine-readable knowledge, and locally verified browser experience.**

## Performance

- **Duration:** 17 min
- **Started:** 2026-07-31T03:50:29Z
- **Completed:** 2026-07-31T04:07:38Z
- **Tasks:** 3 completed
- **Files modified:** 16 (including required tracking)

## Accomplishments

- Built the four-page `/ → /learn/ → /architecture/ → /sources/` learning path and `knowledge.json` from a single versioned content record, preserving fact, term, relationship, source, status, and blocker IDs.
- Added a distinctive ink-and-paper field-guide visual system with trust-zone composition, evidence/status typography, responsive rhythm, visible focus, forced-color, reduced-motion, and print contracts.
- Kept all essential meaning in static HTML; the small local script only adds an optional, resettable/replayable architecture reading trace.
- Added stdlib loopback preview instructions and approved Chromium checks for routes, keyboard traversal, local-only requests, narrow no-script rendering, reduced motion, transcript/table/source equivalents, and optional trace controls.

## Task Commits

Each task was committed atomically through its TDD gates:

1. **Task 1: Generate a coherent static learning surface from one structured source** — `cf7e278` (test), `72d6529` (feat)
2. **Task 2: Deliver distinctive accessible interaction and visual design** — `04552ea` (test), `1200e3c` (feat)
3. **Task 3: Exercise the built site in a real browser** — `9205048` (test), `80632ae` (docs)

**Plan metadata:** pending this summary commit.

## Files Created/Modified

- `site/content/site.json` — versioned source records for the human and machine outputs.
- `tools/build-site.py` — reproducible stdlib generator with validation, escaping, atomic writes, and local asset publication.
- `site/templates/page.html` — semantic page frame with local asset links, skip link, landmarks, and navigation.
- `site/assets/styles.css` — editorial evidence-led design system with responsive, focus, motion, print, and forced-color rules.
- `site/assets/site.js` — defensive optional reading trace with replay and reset controls.
- `site/dist/` — generated pages, knowledge JSON, and local assets.
- `tests/site/test_static_site.py` — content parity, reproducibility, local-asset, and static accessibility contract coverage.
- `tests/site/test_site_browser.py` — approved Chromium path, keyboard, no-script, narrow layout, reduced-motion, and egress coverage.
- `site/README.md` — local build, loopback preview, and verification instructions.

## Verification

- `python3 tools/build-site.py --check` — passed.
- `python3 -m unittest discover -s tests/site -p 'test_static_site.py' -v` — 5 passed.
- `tools/phase1-python -m unittest discover -s tests/site -p 'test_site_browser.py' -v` — 4 passed in approved direct-installed Google Chrome.
- End-to-end browser observation on `http://127.0.0.1:8766/` — passed: the skip link received first keyboard focus; clicking through the learning path produced **A note journey, read in order** → **The host keeps authority** → **Evidence, with its limits attached**; replay/reset worked; reduced-motion computed to `scroll-behavior: auto`; all 12 observed page requests stayed local. A 320px no-script architecture visit retained one transcript, one table, seven source links, no optional trace, and no document overflow.
- `tools/phase1-python -m unittest discover -s tests/phase1 -v` — ran but did not pass: 151 tests ended with 17 failures and 8 errors from pre-existing `PRE118` review-manifest refusal and `IMP011`/`IMP016` source-registry digest failures. These do not exercise or alter the static-site surface and are recorded in `deferred-items.md` for a separately scoped gap plan.

## Decisions Made

- Generated source CSS and JavaScript into `site/dist/assets/` so every required browser asset is relative, checked into the reproducible output, and observable as local-only.
- Used the architecture page's existing static ordered steps, transcript, and comparison table as the complete no-script model; the enhanced trace cannot become a source of essential facts.
- Kept direct-installed Firefox outside this plan's Chromium-only test target. Its existing Phase 1 launch blocker remains a deferred cross-browser evidence issue; no launcher/configuration workaround was attempted.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Used an available loopback port for end-to-end observation**
- **Found during:** Task 3 verification
- **Issue:** The requested loopback preview port `8765` was already in use.
- **Fix:** Started the identical stdlib static server on `127.0.0.1:8766`, exercised the full browser flow, captured a screenshot, then stopped only that exact preview process.
- **Files modified:** None
- **Verification:** The approved browser flow and all local-only request checks passed on the alternate port.
- **Committed in:** N/A (verification environment only)

**2. [Rule 1 - Tracking bug] Retained the Phase 1 verification gate after plan-progress recalculation**
- **Found during:** Final tracking update
- **Issue:** Progress recalculation inferred one completed phase solely because all 48 plan summaries existed, despite the roadmap still reporting Phase 1 as in progress and the active `gaps_found` verification gate.
- **Fix:** Kept the plan count at 48 but restored `completed_phases: 0` and updated the current position to await phase verification/UAT.
- **Files modified:** `.planning/STATE.md`
- **Verification:** `STATE.md` remains `status: executing`; the roadmap update reports `In Progress` and `complete: false`.
- **Committed in:** pending metadata commit

---

**Total deviations:** 2 auto-fixed (1 blocking verification-environment issue, 1 tracking bug)
**Impact on plan:** No product scope, dependency, network, runtime, or evidence claim changed; the tracking correction preserves the explicit phase gate.

## Issues Encountered

- The retained Phase 1 suite has unrelated pre-existing evidence/terminal binding failures. They are recorded in `.planning/phases/01-research-and-truth-baseline/deferred-items.md`; this plan intentionally did not change canonical evidence, review binding, or source-registry records.

## Known Stubs

None. Essential source labels, status records, transcript, table, and blocker content are structured and rendered in static output; the optional trace is explicitly nonessential.

## User Setup Required

None — local preview uses Python's standard-library HTTP server and no external service configuration.

## Next Phase Readiness

- The static learning site is ready for phase verification/UAT review, including the remaining human visual judgment of the editorial reading experience.
- Phase 01 remains `gaps_found` / not complete: PRE118, source-registry digest, cross-browser Firefox, and other deferred Phase 1 evidence blockers retain their own scope and ownership.

## Self-Check: PASSED

Confirmed all listed site/test/source files exist and every Task 1–3 TDD commit resolves to a commit object.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-31*
