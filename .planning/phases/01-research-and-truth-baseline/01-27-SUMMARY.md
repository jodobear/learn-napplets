---
phase: 01-research-and-truth-baseline
plan: 27
subsystem: lesson-research-evidence
tags: [markdown, yaml, unittest, evidence, lesson-packets, accessibility]
requires:
  - phase: 01-08
    provides: "Fixed thirteen-packet index and LES-001 through LES-004 packet conventions"
  - phase: 01-28
    provides: "Canonical compatibility, drift, open-question, and consolidation-audit evidence state"
provides:
  - "Five uncertainty-bounded lesson research packets for request, capability, identity, composition, and focused-application design"
  - "Nine-present staged fixed lesson inventory without changing the remaining planned entries"
  - "Canonical-ID validation for CMP, DRF, and OQ citations plus both required unsettled-evidence sections"
affects: [01-25, 01-24, phase-2-product-contract, phase-3-static-site]
tech-stack:
  added: []
  patterns:
    - "Research packets cite post-consolidation canonical IDs and keep blocked evidence in both uncertainty sections"
    - "Later interactive instruments remain deterministic conceptual simulations with keyboard, reduced-motion, transcript, state-inspection, reset/replay, and static-equivalent requirements"
key-files:
  created:
    - .planning/research/lesson-packets/05-one-request-across-boundary.md
    - .planning/research/lesson-packets/06-capabilities-not-ambient-authority.md
    - .planning/research/lesson-packets/07-identity-and-distribution.md
    - .planning/research/lesson-packets/08-apps-that-cooperate.md
    - .planning/research/lesson-packets/09-designing-a-good-napplet.md
    - tests/phase1/test_lesson_evidence.py
  modified:
    - .planning/research/lesson-packets/index.yaml
key-decisions:
  - "LES-005 through LES-009 use only conceptual simulations and deterministic future fixtures because no first real-lab operation or teaching-host profile is selected."
  - "Manifest and dTag identity terms remain explicitly linked to provisional policy claims and blocked canonical questions rather than becoming teaching rules."
  - "Host-mediated sibling composition has no observed canonical result and remains a conceptual comparison topic."
patterns-established:
  - "Canonical CMP, DRF, and OQ citations must resolve to Plan 01-28 collections and appear with state, reason, and impact in both uncertainty sections when unsettled."
requirements-completed: [EVID-01, EVID-02, EVID-03]
coverage:
  - id: D1
    description: "LES-005 through LES-009 retain all packet-template sections, fixed IDs, and deterministic conceptual-instrument constraints."
    requirement: EVID-01
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-lessons --index .planning/research/lesson-packets/index.yaml --required-present 9"
        status: pass
    human_judgment: false
  - id: D2
    description: "Every CMP, DRF, and OQ citation in LES-005 through LES-009 resolves to canonical records and unsettled citations are bounded in both required sections."
    requirement: EVID-02
    verification:
      - kind: unit
        ref: "tests/phase1/test_lesson_evidence.py"
        status: pass
    human_judgment: false
  - id: D3
    description: "The canonical research collections remain structurally and semantically valid after staged lesson packet publication."
    requirement: EVID-03
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/learn-napplets-validation-XXXXXX.md"
        status: pass
    human_judgment: false
metrics:
  duration: 6m 26s
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 27: Lesson Research Packets Summary

**Five evidence-bounded research packets stage a nine-lesson inventory for request, least-authority capability, identity/distribution, composition, and focused napplet design without presenting blocked protocol or runtime behavior as fact.**

## Performance

- **Duration:** 6m 26s
- **Started:** 2026-07-24T11:50:33Z
- **Completed:** 2026-07-24T11:56:59Z
- **Tasks:** 2/2
- **Files modified:** 7

## Accomplishments

- Added LES-005 through LES-007 for one proposed request, mediated capabilities, and identity/distribution questions, with no selected real host, operation, manifest, or identity rule.
- Added LES-008 and LES-009 for conceptual app cooperation and focused napplet design, explicitly distinguishing absent observed composition from a future implementation observation.
- Staged the fixed thirteen-entry index at exactly nine present packets and added canonical citation tests that require every cited CMP, DRF, and OQ record to resolve and every unsettled citation to have state, reason, and impact in both required sections.

## Task Commits

Each task was committed atomically:

1. **Task 1: Research request, capability, and identity packets** - `0857fde` (feat)
2. **Task 2: Research composition and design packets and stage nine-packet validation** - `6c97c0a` (feat)

## Files Created/Modified

- `.planning/research/lesson-packets/index.yaml` - Preserves the fixed ordered inventory and marks LES-005 through LES-009 present.
- `.planning/research/lesson-packets/05-one-request-across-boundary.md` - Bounds a request-boundary model to a conceptual simulation.
- `.planning/research/lesson-packets/06-capabilities-not-ambient-authority.md` - Separates least-authority project policy from unestablished capability mechanics.
- `.planning/research/lesson-packets/07-identity-and-distribution.md` - Keeps manifest, dTag, verifier, artifact, and public-package questions explicitly blocked.
- `.planning/research/lesson-packets/08-apps-that-cooperate.md` - Keeps cooperation and sibling composition as evidence-limited comparison work.
- `.planning/research/lesson-packets/09-designing-a-good-napplet.md` - Supplies a static-first focused-design heuristic without selecting a runtime or manifest model.
- `tests/phase1/test_lesson_evidence.py` - Resolves packet citations against current canonical collections and checks the unsettled-teaching boundary.

## Decisions Made

- Keep all five packet instruments as labelled conceptual simulations; no live relay, wallet, signer, external service, secret, key, package install, browser run, or production scaffold is authorized.
- Use common structured packet data as the future source for human and machine representations, with keyboard, reduced-motion, transcript/state inspection, reset/replay, and static equivalents required before UI implementation.
- Preserve manifest, dTag identity, verifier, package, runtime, archetype, convention, and composition uncertainty through canonical IDs and dated follow-up work.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Excluded claim-family substrings from canonical citation matching**
- **Found during:** Task 2: Research composition and design packets and stage nine-packet validation.
- **Issue:** The initial citation matcher treated the `CMP-*` substring inside claim IDs such as `CLM-CMP-RUNTIME-001` as a compatibility citation, producing a false missing-record failure. The audit assertion also required a truncated canonical-target sentence rather than the authoritative full audit line.
- **Fix:** Tightened the matcher to require a standalone evidence-family ID and asserted the audit target names individually.
- **Files modified:** `tests/phase1/test_lesson_evidence.py`
- **Verification:** `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_lesson_evidence.py'`
- **Committed in:** `6c97c0a`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug).
**Impact on plan:** The correction makes canonical-ID validation accurately distinguish claim references from compatibility records; no scope or evidence state changed.

## Issues Encountered

- The common research validator requires an explicit `--report` target. Verification used a temporary file under `/tmp`, preserving the pre-existing dirty `.planning/research/reports/validation.md` unchanged and uncommitted.

## Known Stubs

None. The phrase “not available” in LES-006 describes the canonical blocked evidence state; it is not a UI placeholder or an unmet packet dependency.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 01-25 can extend the citation test to the remaining LES-010 through LES-013 packets and perform the thirteen-packet closeout.
- The initial Phase 2 product/content contract and Phase 3 static-site planning can consume all five packets as research inputs, not final lesson copy.
- Canonical blockers for manifest, dTag identity, verifier, package/public-export, runtime, browser, archetype, convention, and composition behavior remain explicit and require immutable evidence plus human review before promotion.

## Self-Check: PASSED

- Verified LES-005 through LES-009, the staged index, the evidence test, and this summary exist.
- Verified task commits `0857fde` and `6c97c0a` resolve to commit objects.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
