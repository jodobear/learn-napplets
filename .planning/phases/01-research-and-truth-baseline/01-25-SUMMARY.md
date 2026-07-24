---
phase: 01-research-and-truth-baseline
plan: 25
subsystem: research-evidence
tags: [lesson-packets, canonical-evidence, uncertainty-boundaries, unittest, yaml]
requires:
  - phase: 01-27
    provides: LES-005 through LES-009 packets and their initial evidence contract
  - phase: 01-28
    provides: canonical compatibility, drift, open-question, claim, source, and consolidation records
provides:
  - Complete fixed LES-001 through LES-013 packet inventory
  - Evidence-bounded research packets for anatomy, build/publication, runtime, and contribution lessons
  - Full-inventory canonical citation, immutable-source, and uncertainty-section validation
affects: [01-24-phase-gate, phase-2-content-contract, phase-3-static-site]
tech-stack:
  added: []
  patterns:
    - Fixed lesson-index inventory with exact ID-to-filename validation
    - Canonical family citation resolution and uncertainty-boundary checks
key-files:
  created:
    - .planning/research/lesson-packets/10-anatomy-of-a-napplet.md
    - .planning/research/lesson-packets/11-build-test-and-publish.md
    - .planning/research/lesson-packets/12-inside-a-runtime.md
    - .planning/research/lesson-packets/13-evolving-the-protocol.md
  modified:
    - .planning/research/lesson-packets/index.yaml
    - tests/phase1/test_lesson_evidence.py
key-decisions:
  - "The lesson index is a complete, ordered thirteen-entry contract rather than a directory convention."
  - "Build, runtime, package, deployment, and contribution content remains deterministic conceptual research until canonical evidence and human review resolve its blockers."
patterns-established:
  - "Every cited unsettled CLM, CMP, DRF, or OQ record must appear in both uncertainty sections with canonical state, reason, and impact."
  - "CLM citations must traverse typed source relations to complete immutable SRC records; compatibility scope is the canonical boundary when a compatibility row has no separate impacts field."
requirements-completed: [EVID-01, EVID-02, EVID-03]
coverage:
  - id: D1
    description: "Complete fixed LES-001 through LES-013 research-packet inventory."
    requirement: EVID-01
    verification:
      - kind: integration
        ref: "tools/validate-research.py validate-lessons --index .planning/research/lesson-packets/index.yaml --required-present 13"
        status: pass
      - kind: unit
        ref: "tests/phase1/test_lesson_evidence.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "Canonical citation, source-transitivity, consolidation-target, and uncertainty-boundary validation across all packets."
    requirement: EVID-02
    verification:
      - kind: unit
        ref: "tests/phase1/test_lesson_evidence.py"
        status: pass
      - kind: integration
        ref: "tools/validate-research.py validate --root .planning/research --report /tmp/01-25-validation.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "Evidence-bounded build, publication, runtime, and contribution research packets that defer unresolved complex work."
    requirement: EVID-03
    verification:
      - kind: unit
        ref: "tests/phase1/test_lesson_evidence.py"
        status: pass
    human_judgment: false
metrics:
  duration: 7m 14s
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 25: Complete Lesson Research Inventory Summary

**Thirteen fixed lesson-research packets now trace canonical evidence and keep unresolved build, runtime, publication, and contribution work visibly deferred.**

## Performance

- **Duration:** 7m 14s
- **Started:** 2026-07-24T12:11:37Z
- **Completed:** 2026-07-24T12:18:51Z
- **Tasks:** 2/2
- **Files modified:** 15 task files

## Accomplishments

- Added LES-010 through LES-013 at their stable, index-declared filenames for anatomy, build/test/publish, runtime, and protocol-evolution research.
- Completed the ordered LES-001 through LES-013 inventory and verified exactly thirteen indexed Markdown packets.
- Expanded shared validation to resolve CLM/CMP/DRF/OQ citations, audit targets, immutable claim-source relations, and both uncertainty sections across the complete inventory.
- Kept public-package, manifest/identity/verifier, Firefox, external publication/deployment, runtime-profile, source-freshness, and contribution boundaries as explicit blockers or follow-up work.

## Verification

Passed:

- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/01-25-validation.md`
- `tools/phase1-python tools/validate-research.py validate-lessons --index .planning/research/lesson-packets/index.yaml --required-present 13`
- `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_lesson_evidence.py'` — 6 tests
- Exact filesystem inventory assertion — 13 packet Markdown files

The planned validation report path was already dirty before execution and was intentionally not staged or committed; validation used `/tmp/01-25-validation.md` instead.

## Task Commits

1. **Task 1: Research the build, runtime, and contribution lessons with full canonical-evidence coverage**
   - `1f923e3` — `test(01-25): add full lesson evidence inventory coverage` (TDD RED)
   - `8389a62` — `feat(01-25): complete thirteen lesson research packets` (TDD GREEN)
2. **Task 2: Verify the final shared lesson index, evidence links, and exact packet inventory** — verification-only; no content change was required after Task 1.

## Files Created/Modified

- `.planning/research/lesson-packets/10-anatomy-of-a-napplet.md` — package/build-surface research with static-only explorer boundary.
- `.planning/research/lesson-packets/11-build-test-and-publish.md` — artifact, conformance, and external-publication research boundary.
- `.planning/research/lesson-packets/12-inside-a-runtime.md` — required-behavior, possible-architecture, host-policy, and adapter classification.
- `.planning/research/lesson-packets/13-evolving-the-protocol.md` — deterministic contribution-routing and dated open-question research.
- `.planning/research/lesson-packets/index.yaml` — complete stable thirteen-packet inventory.
- `tests/phase1/test_lesson_evidence.py` — all-packet canonical citation and immutable-source validation.
- `.planning/research/lesson-packets/01-nostr-client-taken-apart.md` through `09-designing-a-good-napplet.md` — complete uncertainty entries for every cited unsettled canonical record.

## Decisions Made

- Kept the fixed LES identifiers and filenames unchanged; completion is controlled only by the shared ordered index.
- Treated compatibility `scope` as its canonical reason/impact boundary where that canonical record type does not carry separate `stateReason` or `impacts` fields.
- Kept all complex exercises as explicitly labelled conceptual simulations; no package install, browser run, external action, network access, deployment, publication, or credentials were used.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Test contract bug] Handle compatibility rows with canonical scope rather than unavailable generic reason/impact fields**
- **Found during:** Task 1
- **Issue:** The full-inventory test assumed every canonical record exposed `stateReason` and `impacts`; `CMP-BASELINE-001` instead exposes its canonical boundary through `scope`.
- **Fix:** Used `scope` as the explicit canonical reason/impact fallback while retaining strict validation for every cited record.
- **Files modified:** `tests/phase1/test_lesson_evidence.py`
- **Verification:** Full six-test lesson-evidence suite passed.
- **Committed in:** `8389a62`

**2. [Rule 2 - Missing critical transparency] Normalize uncertainty entries for the existing LES-001 through LES-009 packets**
- **Found during:** Task 1
- **Issue:** Earlier packets cited unsettled CLM-family records but did not consistently include each cited ID's canonical state, reason, and impact in both mandatory uncertainty sections.
- **Fix:** Added structured canonical uncertainty entries across the existing packets so the shared full-inventory contract can prevent unsettled evidence becoming settled instruction.
- **Files modified:** `.planning/research/lesson-packets/01-nostr-client-taken-apart.md` through `09-designing-a-good-napplet.md`
- **Verification:** Full lesson-evidence suite and exact thirteen-packet validation passed.
- **Committed in:** `8389a62`

**Total deviations:** 2 auto-fixed (1 Rule 1, 1 Rule 2).

## Issues Encountered

- The TDD RED run correctly failed for the four absent packets, staged index state, and incomplete cross-inventory uncertainty coverage.
- `.planning/research/reports/validation.md` was pre-existing dirty content; per execution constraints it was neither edited intentionally nor staged. The common validator wrote its verification output under `/tmp`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 01-24 can consume a mechanically verified exact packet inventory and canonical evidence boundaries for Phase 1 closeout.
- Human review and approval are still required for ADR acceptance, Phase 1 gate transition, and any later runtime/package/deployment/contribution implementation work.

## Self-Check: PASSED

- Verified all four created packet files, the completed index, and the all-inventory test file exist.
- Verified TDD RED commit `1f923e3` and GREEN commit `8389a62` exist as commit objects.
