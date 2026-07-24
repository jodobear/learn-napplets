---
phase: 01-research-and-truth-baseline
plan: 23
subsystem: research-decision-synthesis
tags: [evidence, adr, source-freshness, package-versioning, code-editing, risk]
requires:
  - phase: 01-28
    provides: "Canonical all-spike consolidation audit, impact records, replay manifest, and blocked/uncertain evidence state"
provides:
  - "Proposed ADRs for least-authority editing, public-package versioning, and source freshness review"
  - "Executive, decision, and risk synthesis grounded in shared canonical evidence"
  - "A proposed static-public-site fast path with explicit optional-capability deferrals"
affects: [phase-02-product-content-contract, phase-03-static-site-foundation, phase-05-teaching-host, phase-08-portable-target, phase-11-maintenance]
tech-stack:
  added: []
  patterns:
    - "Consume consolidation-issued canonical IDs for ADR facts; retain no-impact spike reports as explanatory context"
    - "Classify source facts, observations, project policy, proposals, inference, blockers, and uncertainty separately"
key-files:
  created:
    - .planning/adr/0009-code-editing.md
    - .planning/adr/0010-package-versioning.md
    - .planning/adr/0011-source-freshness.md
    - .planning/research/executive-summary.md
    - .planning/research/decision-summary.md
    - .planning/research/risks.md
  modified: []
key-decisions:
  - "Fixed tested variants and a narrowly controlled native textarea remain proposed least-authority editing direction; CodeMirror is not selected and CodeJar remains blocked."
  - "No napplet package/version is admitted until public release, root export, provenance, integrity, implementation baseline, compatibility, and review evidence is complete."
  - "Source freshness uses targeted D-20/D-36 review work that retains old identity and never auto-changes claims, ADRs, or approvals."
  - "The minimal static public-site path is a proposed post-Phase-2 direction that defers host, package, portable, external-delivery, and complex interactive capability."
patterns-established:
  - "Decision summaries expose a smallest evidence-supported path alongside unresolved risks and required approvals."
  - "Every conclusion links evidence category/state, stable IDs, impacts, ownership, and revisit triggers."
requirements-completed: [EVID-02, EVID-03, EVID-04, OPER-01, OPER-03]
coverage:
  - id: D1
    description: "Three proposed ADRs preserve evidence provenance, alternatives, uncertainty, impacts, approvers, and revisit triggers."
    requirement: EVID-02
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-adr .planning/adr/0009-code-editing.md (and 0010/0011)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Executive, decision, and risk summaries use ordered research headings and validate against canonical research records."
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "Static-site fast path and optional-capability deferrals remain proposed decisions requiring human approval."
    requirement: OPER-03
    verification:
      - kind: other
        ref: "Manual review of proposed ADR status and decision-summary.md"
        status: pass
    human_judgment: true
    rationale: "Only the required human approvers may accept ADRs or authorize the Phase 2/3 transition."
metrics:
  duration: 347s
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 23: Research Decision Synthesis Summary

**Proposed code-editing, package-versioning, and source-freshness ADRs plus evidence-grounded executive, decision, and risk summaries that preserve the static-site fast path and every material blocker.**

## Performance

- **Duration:** 5m 47s
- **Started:** 2026-07-24T12:02:26Z
- **Completed:** 2026-07-24T12:08:13Z
- **Tasks:** 2/2
- **Files modified:** 6

## Accomplishments

- Added proposed-only ADR-0009, ADR-0010, and ADR-0011 with alternatives, evidence states, owner/approver roles, impacts, uncertainty, and concrete revisit triggers.
- Synthesized canonical source, claim, compatibility, drift, open-question, teaching-scope, delivery, ADR, and consolidation evidence into executive, decision, and risk outputs.
- Made the smallest post-Phase-2 static public-learning-site direction visible while explicitly deferring host/guest runtime, public package, portable, external deployment, full editor, arbitrary execution, and live-system capabilities.

## Task Commits

Each task was committed atomically:

1. **Task 1: Write proposed ADR 0009 through ADR 0011** — `108b525` (docs)
2. **Task 2: Synthesize executive, decision, and risk outputs from common records** — `183ac22` (docs)

## Files Created/Modified

- `.planning/adr/0009-code-editing.md` — Proposed least-authority editing direction that retains fixed variants, controlled textarea scope, CodeMirror non-selection, CodeJar blocker, and Firefox uncertainty.
- `.planning/adr/0010-package-versioning.md` — Proposed public-evidence gate for future package admission and updates; preserves the public-package/conformance blocker.
- `.planning/adr/0011-source-freshness.md` — Proposed D-20/D-36 targeted source-review policy that retains old identity and forbids automatic evidence mutation.
- `.planning/research/executive-summary.md` — Eight decision-question answers with source categories, states, uncertainty, blockers, impacts, owners, and refresh triggers.
- `.planning/research/decision-summary.md` — Decision-maker fast path, evidence/status table, explicit deferrals, approval routing, and revisit index.
- `.planning/research/risks.md` — Grouped upstream, supply-chain, browser/security, accessibility, delivery, operational, and scope risks with owner, impact, mitigation/blocker, and trigger.

## Decisions Made

- The canonical Phase 1 recommendation series now extends through ADR-0011, but every ADR remains proposed and unaccepted.
- Canonical consolidation IDs and record states are the decision-evidence layer; raw report-only spike material is explanatory context only.
- Fixed variants are the proposed editing default, controlled textarea is bounded, CodeMirror is unselected, and CodeJar remains blocked.
- The static public-site path is a proposed product direction after Phase 2 approval, not a substitute for unresolved host, package, portability, or delivery evidence.

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

The prescribed canonical validator writes the pre-existing dirty `.planning/research/reports/validation.md`. Verification preserved and restored that file byte-for-byte, so it was not committed or changed by this plan.

## Known Stubs

None.

## User Setup Required

None — no external service configuration, package installation, browser run/download, network action, deployment, publication, account, or credential access occurred.

## Next Phase Readiness

- Phase 2 can consume the proposed ADR series and common structured decision summaries without treating any recommendation as accepted.
- The proposed fast path is a deterministic static learning site with common structured sources and explicit status/uncertainty; its implementation remains gated by Phase 2 approval.
- Firefox, package/public-export/conformance, manifest/identity/verifier, egress, VitePress accessibility, CodeJar, external-deployment, and optional-portable blockers remain visible for later review.

---
## Self-Check: PASSED

- Verified all six ADR/summary artifacts and this summary file exist.
- Verified task commits `108b525` and `183ac22` resolve to commit objects.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
