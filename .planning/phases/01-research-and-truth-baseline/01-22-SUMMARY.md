---
phase: 01-research-and-truth-baseline
plan: 22
subsystem: architecture-decision-records
tags: [adr, evidence, provenance, accessibility, portable-target, fixtures]
requires:
  - phase: 01-28
    provides: "Canonical spike-consolidation audit, compatibility/drift/open-question records, and immutable impact fragments"
provides:
  - "Four proposed-only, source-traceable ADRs for teaching host, diagram/motion, portable target, and protocol fixtures"
  - "A public-site fast path explicitly separated from optional portable and advanced capability blockers"
affects: [phase-2-product-contract, phase-4-visual-primitives, phase-5-teaching-host, phase-8-portable-target]
tech-stack:
  added: []
  patterns:
    - "ADRs consume consolidation-issued canonical IDs; raw no-impact reports remain explanatory context only"
    - "Blocked browser, verifier, package, identity, manifest, and accessibility evidence remains explicit in proposed recommendations"
key-files:
  created:
    - .planning/adr/0005-teaching-host.md
    - .planning/adr/0006-diagram-motion.md
    - .planning/adr/0007-portable-napplet-target.md
    - .planning/adr/0008-protocol-fixture-strategy.md
  modified: []
key-decisions:
  - "Keep the public static learning path independent of optional teaching-host and portable-target work."
  - "Treat semantic SVG as a proposed smallest later baseline only; retain static diagram/transcript/table as the immediate safe path."
  - "Require future protocol fixtures to bind every technical claim through CLM-* to complete immutable SRC-* records and use explicit deterministic fakes."
patterns-established:
  - "Proposed ADRs preserve option sets, owner/approver roles, uncertainty, risk, and concrete source/measurement revisit triggers."
requirements-completed: [EVID-03, EVID-04, OPER-03]
coverage:
  - id: D1
    description: "Proposed ADR 0005 and ADR 0006 preserve host/guest, Firefox, static-accessibility, and canonical-evidence boundaries."
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-adr .planning/adr/0005-teaching-host.md && .../0006-diagram-motion.md"
        status: pass
    human_judgment: false
  - id: D2
    description: "Proposed ADR 0007 and ADR 0008 keep portable scope non-blocking and fixtures source-pinned/deterministic."
    requirement: EVID-03
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-adr .planning/adr/0007-portable-napplet-target.md && .../0008-protocol-fixture-strategy.md"
        status: pass
    human_judgment: false
metrics:
  duration: 2m 25s
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 22: Proposed Architecture ADRs Summary

**Four evidence-scoped proposed ADRs preserve the static public-site fast path while exposing unresolved host, browser, portable-target, package, and fixture constraints for human review.**

## Performance

- **Duration:** 2m 25s
- **Started:** 2026-07-24T11:45:03Z
- **Completed:** 2026-07-24T11:47:28Z
- **Tasks:** 2/2
- **Files modified:** 4

## Accomplishments

- Drafted ADR 0005 with a profile-scoped teaching-host proposal that distinguishes missing upstream behavior, local browser observation, future architecture, project CSP policy, and blocked external adapters.
- Drafted ADR 0006 with a static-first diagram direction, preserving transcript/table/keyboard/reduced-motion/reset equivalents and the Firefox pre-attachment block.
- Drafted ADR 0007 with the exact `GO-V1`, `GO-LATER`, `WORKBENCH-ONLY`, and `NO-GO` choices while making the optional portable target unable to block the public-site roadmap.
- Drafted ADR 0008 with a proposed immutable-source, schema-validation, deterministic-fake, compatibility-record, and explicit-limitation strategy; no verifier or package behavior was promoted.

## Task Commits

Each task was committed atomically:

1. **Task 1: Write proposed teaching-host and diagram/motion ADRs** - `8660f41` (docs)
2. **Task 2: Write proposed portable-target and protocol-fixture ADRs** - `3c23075` (docs)

## Files Created/Modified

- `.planning/adr/0005-teaching-host.md` - Proposed profile-scoped teaching-host boundary with canonical SPK-C/D/G/H evidence, static fallback, and explicit blockers.
- `.planning/adr/0006-diagram-motion.md` - Proposed static-first diagram/motion direction with no-impact evidence handling and accessibility constraints.
- `.planning/adr/0007-portable-napplet-target.md` - Proposed portable outcome set that preserves a non-blocking public-site fast path.
- `.planning/adr/0008-protocol-fixture-strategy.md` - Proposed deterministic fixture policy bound to canonical SPK-D/G provenance and verifier/package limits.

## Decisions Made

- Retained all ADRs as `proposed`; no human approval, production scaffold, runtime, UI, package, verifier, or portable artifact was authorized.
- Treated Plan 01-28's canonical impact IDs and audit as decision evidence. SPK-F and SPK-I raw reports remain explanatory because the audit marked them `no-impact-fragment`.
- Kept Firefox 152.0.4's pre-attachment outcome across SPK-C/F/H/I/J as a blocker, without a cross-browser claim, launcher workaround, browser configuration change, or browser download.
- Identified the minimum static learning site as independently reviewable after Phase 2 approval; optional portable/advanced paths remain defer/narrow/skip candidates.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Matched the semantic ADR validator's literal field contract**
- **Found during:** Task 1
- **Issue:** The template-style bold labels did not contain the validator's required literal `Status: proposed` and `Revisit trigger:` strings, so both ADR validations failed despite semantically complete sections.
- **Fix:** Preserved the plan-required bold status marker while adding the validator-compatible literal status/revisit labels to ADR 0005 and ADR 0006.
- **Files modified:** `.planning/adr/0005-teaching-host.md`, `.planning/adr/0006-diagram-motion.md`
- **Verification:** `tools/phase1-python tools/validate-research.py validate-adr` passed for both files.
- **Committed in:** `8660f41`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug).
**Impact on plan:** The change is documentation-contract compatibility only; it adds no product scope and leaves all evidence classifications and blockers unchanged.

## Issues Encountered

- The full research validator writes the pre-existing dirty `.planning/research/reports/validation.md`; it was intentionally not run so that protected file was neither modified nor committed. Per-ADR semantic validation passed for all four records.

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 2 can review a minimum static public learning-site direction without waiting on optional portable work.
- ADR acceptance remains a human gate. Firefox attached-context evidence, current immutable manifest/identity/verifier provenance, public package/root-export/conformance evidence, SPK-B's VitePress accessibility failure, and upstream egress evidence remain unresolved.
- Later production work must retain host/guest separation, deterministic fake-system limits, explicit real-versus-simulated labels, and structured evidence parity.

## Self-Check: PASSED

- Verified all four ADR files and this summary exist.
- Verified task commits `8660f41cf8383b71f0313278652a1aa32b23f58f` and `3c2307586524a4ed4b59d81c602573755901cff6` resolve to commit objects.
- Verified all four semantic ADR validations pass; no stub patterns were found.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
