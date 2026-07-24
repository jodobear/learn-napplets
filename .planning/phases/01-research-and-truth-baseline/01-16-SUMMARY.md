---
phase: 01-research-and-truth-baseline
plan: 16
subsystem: research-security
status: complete
tags: [browser-egress, csp, iframe-sandbox, playwright, chrome, firefox, evidence]
requires:
  - phase: 01-11
    provides: SPK-C selected opaque-origin srcdoc iframe model and Firefox launch blocker
  - phase: 01-07
    provides: immutable evidence and impact-fragment validation patterns
provides:
  - Reproducible SPK-H local-loopback browser egress matrix for eight channel groups
  - Chrome observations, Firefox pre-attachment blocker evidence, and typed security/egress hand-off
  - Semantic source-link negative tests for pre-consolidation fragment validation
affects: [01-28 security-egress synthesis, ADR-0005, ADR-0014, EVID-04, phases-02-and-05]
tech-stack:
  added: []
  patterns:
    - Exact SPK-C sandbox/loading model with deterministic loopback-only channel endpoints
    - Browser observations, project policy, and upstream questions recorded as separate evidence categories
    - Schema-validated security/egress finding proposal with source-link negative cases
key-files:
  created:
    - .planning/spikes/spk-h-browser-egress/environment.json
    - .planning/spikes/spk-h-browser-egress/measurements.yaml
    - .planning/spikes/spk-h-browser-egress/report.md
    - .planning/spikes/spk-h-browser-egress/impact-fragment.yaml
    - .planning/spikes/spk-h-browser-egress/negative-fragment-tests.py
  modified:
    - .planning/spikes/spk-h-browser-egress/metadata.yaml
    - .planning/spikes/spk-h-browser-egress/recipe.md
    - .planning/spikes/spk-h-browser-egress/fixture.html
    - .planning/spikes/spk-h-browser-egress/runner.py
    - .planning/research/schemas/spike-impact-fragment.schema.json
key-decisions:
  - SPK-H preserves SPK-C's opaque-origin srcdoc guest and sandbox=allow-scripts-only loading model.
  - Chrome-only egress results remain browser observations; Firefox's pre-attachment exit blocks cross-browser recommendations.
  - A restrictive public-site CSP is proposed project policy only, never an inferred upstream NIP requirement.
requirements-completed: [EVID-04]
coverage:
  - id: D1
    description: Eight-channel deterministic local-loopback egress matrix under the selected sandbox/loading model.
    requirement: EVID-04
    verification:
      - kind: integration
        ref: tools/phase1-python .planning/spikes/spk-h-browser-egress/runner.py --fixture .planning/spikes/spk-h-browser-egress/fixture.html --out /tmp/spk-h-browser-egress
        status: pass
      - kind: integration
        ref: tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-h-browser-egress --complete
        status: pass
    human_judgment: false
  - id: D2
    description: Typed SPK-H security/egress impact fragment and source-binding regression cases.
    requirement: EVID-04
    verification:
      - kind: integration
        ref: tools/phase1-python tools/validate-research.py validate-impact-fragment .planning/spikes/spk-h-browser-egress/impact-fragment.yaml --root .planning
        status: pass
      - kind: integration
        ref: tools/phase1-python .planning/spikes/spk-h-browser-egress/negative-fragment-tests.py
        status: pass
    human_judgment: false
  - id: D3
    description: Proposed CSP policy and unresolved upstream egress question remain correctly categorized.
    requirement: EVID-04
    verification:
      - kind: integration
        ref: tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-h-browser-egress/report.md
        status: pass
    human_judgment: false
metrics:
  duration: 18m 30s
  completed: 2026-07-24
---

# Phase 01 Plan 16: Browser Egress and CSP Evidence Summary

**Deterministic local-loopback evidence for eight sandboxed browser egress channel groups, with five Chrome observations and an explicit Firefox pre-attachment blocker.**

## Performance

- **Duration:** 18m 30s
- **Started:** 2026-07-24T10:15:30Z
- **Completed:** 2026-07-24T10:34:00Z
- **Tasks:** 2/2
- **Files modified:** 10

## Accomplishments

- Defined and replayed SPK-H against the exact SPK-C opaque-origin `srcdoc` / `sandbox="allow-scripts"` model using only deterministic `127.0.0.1` endpoints and no credentials or external probes.
- Recorded five Chrome samples covering fetch, images/media, classic/module scripts, WebSocket, EventSource, workers, form/navigation, and referrer/origin, plus a semantic-negative CSP probe.
- Preserved Firefox 152.0.4's exit-before-attachment result as an all-channel execution block; no browser launcher flag, profile, preference, download, or workaround was added.
- Produced a schema-validated SPK-H impact fragment with source/observation/policy/question separation, a proposed security finding requiring human approval, and source-link negative tests.

## Task Commits

Each task was committed atomically:

1. **Task 1: Specify the selected-model egress fixture and test matrix** — `abc515f` (feat)
2. **Task 2: Run SPK-H and preserve the security/egress consolidation input** — `9e74ff5` (feat)

## Files Created/Modified

- `.planning/spikes/spk-h-browser-egress/{metadata.yaml,recipe.md,fixture.html,runner.py}` — selected-model contract, exact CSP matrix, safe fixture, and direct-installed browser runner.
- `.planning/spikes/spk-h-browser-egress/{environment.json,measurements.yaml,report.md}` — pinned environment and browser observations.
- `.planning/spikes/spk-h-browser-egress/impact-fragment.yaml` — immutable typed hand-off for Plan 01-28.
- `.planning/spikes/spk-h-browser-egress/negative-fragment-tests.py` — rejected source-link removal, alteration, and digest-mismatch cases.
- `.planning/research/schemas/spike-impact-fragment.schema.json` — validates the required SPK-H security/egress finding proposal.

## Decisions Made

- Retained only the SPK-C selected model: top-level observer, opaque-origin `srcdoc` guest, and `sandbox="allow-scripts"` with no additional capability token.
- Treated Chrome results as fixture-specific observed browser behavior and Firefox's launcher exit as a blocker, not an egress conclusion.
- Kept `OQ-EGRESS-NIP-001` and `DRF-EGRESS-001` open; a restrictive CSP direction is proposed project policy pending dated security and protocol-technical approval.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected inherited parent CSP blocking the guest script matrix**
- **Found during:** Task 2
- **Issue:** The parent document's initial CSP was inherited by the `srcdoc` guest and blocked the fixture's local classic/module script observations before the declared guest CSP could be measured.
- **Fix:** Constrained the parent to loopback-only sources required by the local matrix and documented the inherited-policy interaction; the guest still owns the exact measurement and semantic-negative CSP inputs.
- **Files modified:** `fixture.html`, `recipe.md`
- **Verification:** Five Chrome samples completed every channel and semantic-negative CSP check.
- **Committed in:** `9e74ff5`

**2. [Rule 1 - Bug] Replaced an invalid opaque-origin worker URL probe with a bounded blob worker**
- **Found during:** Task 2
- **Issue:** An opaque-origin `srcdoc` guest could not complete a fixed external worker-script round trip, so the fixture conflated worker execution with a same-origin worker-loader claim.
- **Fix:** Measured a fixed `blob:` worker under an explicit `worker-src blob:` input and documented that it does not establish a same-origin worker-loader rule.
- **Files modified:** `fixture.html`, `runner.py`, `metadata.yaml`, `recipe.md`
- **Verification:** Every Chrome sample returned `local-worker-ok`.
- **Committed in:** `9e74ff5`

**3. [Rule 1 - Bug] Grouped referrer-mode endpoint receipts with their sample**
- **Found during:** Task 2
- **Issue:** The runner's receipt assertion omitted the deliberately suffixed default and no-referrer header requests, causing a false failed matrix result despite successful observations.
- **Fix:** Grouped both header receipt cases before asserting all required loopback endpoint types.
- **Files modified:** `runner.py`
- **Verification:** Five Chrome samples passed all 19 required checks.
- **Committed in:** `9e74ff5`

**4. [Rule 3 - Blocking] Added the missing typed security/egress fragment contract field**
- **Found during:** Task 2
- **Issue:** The plan requires a fragment-level security/egress finding proposal with owner and required approval, but the existing closed schema rejected that required field.
- **Fix:** Added a backward-compatible SPK-H conditional schema contract and the required `securityEgressFindingProposal` record.
- **Files modified:** `.planning/research/schemas/spike-impact-fragment.schema.json`, `impact-fragment.yaml`
- **Verification:** The valid fragment passes; three semantic negative source-link cases fail before consolidation.
- **Committed in:** `9e74ff5`

**Total deviations:** 4 auto-fixed (3 Rule 1 bugs, 1 Rule 3 blocking contract gap).

**Impact on plan:** All fixes were required for truthful, reproducible local evidence and did not add a production scaffold, browser workaround, external probe, dependency, or protocol claim.

## Issues Encountered

- Firefox 152.0.4 exited before Playwright 1.61.0 attachment on all five required attempts. This is preserved as a blocked execution outcome, not an unsupported browser-security claim.

## Known Stubs

None. The fixture has real deterministic local data sources for its bounded measurements; its intentionally unavailable Firefox observations are documented as a blocker rather than rendered placeholder data.

## Next Phase Readiness

- Plan 01-28 can consolidate SPK-H's immutable local fragment into the final security/egress synthesis while preserving the source, observation, policy, and open-question boundaries.
- ADR-0005 and ADR-0014 remain proposed and blocked for cross-browser recommendation. A dated security and protocol-technical review is still required before any production CSP or host decision.

## Self-Check: PASSED

- Confirmed all ten SPK-H/schema artifacts exist.
- Confirmed task commits `abc515f` and `9e74ff5` exist in git history.
- Re-ran completed-spike, report, impact-fragment, and semantic negative validation successfully.
