---
phase: 01-research-and-truth-baseline
plan: 21
subsystem: architecture-decision-records
tags: [adr, evidence, provenance, governance, static-first]
requires:
  - phase: 01-28
    provides: "Canonical spike-consolidation audit, compatibility/drift/open-question records, and digest-pinned evidence inventory"
provides:
  - "Four proposed-only, evidence-scoped ADR records for workspace, framework, deployment, and common-source content"
  - "Explicit preservation of browser, accessibility, delivery, package, identity, verifier, and portable-target blockers"
affects: [01-22, 01-23, 01-24, phase-2-product-contract, phase-3-independent-repository-foundation]
tech-stack:
  added: []
  patterns:
    - "ADR evidence cites canonical source/claim/compatibility/drift/open-question IDs and consolidation audit digests"
    - "Local spike observations remain distinct from upstream facts, project policy, inference, and proposed decisions"
key-files:
  created:
    - .planning/adr/0001-repository-workspace.md
    - .planning/adr/0002-site-framework.md
    - .planning/adr/0003-deployment-publication.md
    - .planning/adr/0004-content-source-model.md
  modified: []
decisions:
  - "ADR 0001 carries the narrow public-site-first workspace boundary as a proposed review direction while retaining the broader alternative."
  - "ADR 0002 carries Astro 7.1.3 only as a proposed fixture-supported candidate and retains the VitePress reduced-motion/static-equivalent blocker."
  - "ADR 0003 treats local artifact assembly as non-production evidence and keeps any external deployment or publication behind new authorization."
  - "ADR 0004 proposes common structured-source parity as a Phase 2 contract constraint without authorizing a production renderer."
metrics:
  duration: 256s
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 21: Proposed Architecture ADRs Summary

**Four digest-traceable, proposed-only ADRs preserve a smallest static-first review direction while keeping all source, browser, accessibility, deployment, package, identity, verifier, and portable-target uncertainty explicit.**

## Performance

- **Duration:** 4m 16s
- **Started:** 2026-07-24T11:34:56Z
- **Completed:** 2026-07-24
- **Tasks:** 2/2
- **Files created:** 4

## Accomplishments

- Drafted ADR 0001 with a narrow public-site-first workspace-boundary proposal, a broader alternative, and blocked official runtime/package/deployment evidence.
- Drafted ADR 0002 from the disposable static-framework comparison: Astro 7.1.3 is a review candidate only, while VitePress 1.6.4 remains blocked by its repeated reduced-motion/static-equivalent assertion failure.
- Drafted ADR 0003 so SPK-K local artifact integrity, isolation, and rollback measurements cannot be mistaken for hosting, publication, release, or external authorization.
- Drafted ADR 0004 so the SPK-E bounded parity observation can inform a future common structured-source contract without creating a schema, renderer, route, or guest integration.
- Cited Plan 01-28 consolidation-issued compatibility, drift, open-question, source, claim, audit, and digest records; raw spike reports appear only as explicitly limited local-observation context.

## Task Commits

1. **Task 1: Write proposed ADR 0001 and ADR 0002 from SPK-A/SPK-B evidence** — `eb4218a` (`docs`)
2. **Task 2: Write proposed ADR 0003 and ADR 0004 from SPK-K/SPK-E evidence** — `2520cb8` (`docs`)

## Files Created

- `.planning/adr/0001-repository-workspace.md` — proposed workspace-boundary alternatives, evidence traceability, approval boundary, and revisit conditions.
- `.planning/adr/0002-site-framework.md` — proposed static-framework review direction, fixture limits, and retained VitePress accessibility blocker.
- `.planning/adr/0003-deployment-publication.md` — proposed local-only delivery-evidence baseline and external-action authorization boundary.
- `.planning/adr/0004-content-source-model.md` — proposed common structured-source/parity constraint for later content-contract review.

## Validations

- Passed `tools/phase1-python tools/validate-research.py validate-adr` for all four ADRs with no validation output.
- Passed the Plan 01-21 proposed-status assertions for ADRs 0001–0004.
- Passed all required template-heading checks for the four ADRs.
- Passed `tools/phase1-python -m unittest tests/phase1/test_governance.py` — 6 tests.
- Passed `git diff --check HEAD~2..HEAD -- .planning/adr`.

## Decisions Made

- ADR 0001–0004 remain `proposed`; no Phase 1 automation accepted, rejected, or implemented any recommendation.
- The smallest evidence-supported static-first direction is reserved only for future Phase 2/3 review and does not overcome or omit blocked evidence.
- Local SPK-A, SPK-B, SPK-E, and SPK-K reports are digest-pinned explanatory evidence because consolidation records them as `no-impact-fragment`; they do not supply unsupported upstream or canonical compatibility claims.

## Blockers Preserved

- Direct-installed Firefox 152.0.4 exited before Playwright 1.61.0 attached; it does not supply cross-browser evidence.
- VitePress 1.6.4 remains blocked as positive framework evidence pending reviewed reduced-motion/static-equivalent fixture evidence.
- External deployment/publication was not tested; local artifact evidence is not a hosted preview, publication, or release.
- Public package/export, manifest, identity, verifier, and conformance baselines remain blocked.
- Portable-target feasibility remains uncertain and optional; it cannot block the public-site sequence.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added validator-required semantic labels to ADR 0001 and ADR 0002**
- **Found during:** Task 1 validation
- **Issue:** The first drafts used the template headings but omitted the exact `Alternatives:` and `Uncertainty:` semantic labels required by `validate-adr`.
- **Fix:** Added explicit labels while retaining the template sections and proposed-only decision boundary.
- **Files modified:** `.planning/adr/0001-repository-workspace.md`, `.planning/adr/0002-site-framework.md`
- **Commit:** `eb4218a`

**Total deviations:** 1 auto-fixed Rule 1 validation defect.

## Known Stubs

None.

## Threat Flags

None. The plan introduced decision documentation only; it created no endpoint, auth path, file-access behavior, schema change, or other new trust-boundary implementation surface.

## Next Phase Readiness

- Later Phase 2/product-owner review can accept, reject, or request evidence for the four records; no ADR has been accepted here.
- Phase 3 remains prohibited from creating a production workspace or framework scaffold until the Phase 1 and Phase 2 gates are satisfied.
- Plans 01-22 through 01-24 can consume these proposed-only ADR records and their preserved blockers.

## Self-Check: PASSED

- Verified four ADR records and this summary exist on disk.
- Verified task commits `eb4218a` and `2520cb8` resolve to commit objects.
