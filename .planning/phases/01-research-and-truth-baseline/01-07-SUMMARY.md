---
phase: 01-research-and-truth-baseline
plan: 07
subsystem: ecosystem-catalogs
status: complete
tags: [evidence, catalogs, domains, examples, packages, runtimes]
requires: [01-06]
provides:
  - Evidence-linked blocked dispositions for domain, archetype/convention, and public-example candidates
  - Package and runtime acquisition criteria for later scope synthesis and spikes
affects: [01-20, 01-26, phase-1-spikes, phase-1-adrs]
tech-stack:
  added: []
  patterns: [candidate-to-evidence linkage, impact-scoped blocked disposition, separate release-and-current-work analysis]
key-files:
  created:
    - .planning/research/domain-catalog.yaml
    - .planning/research/archetype-convention-catalog.yaml
    - .planning/research/example-napplet-catalog.yaml
    - .planning/research/package-map.md
    - .planning/research/runtime-comparison.md
  modified: []
decisions:
  - "Unpinned ecosystem candidates remain blocked catalog records, not inferred protocol or implementation facts."
  - "napplet/web requires distinct public release and repository/public-export evidence before a consume, wrap, or avoid decision."
  - "Runtime dimensions are a source-acquisition checklist, not a selected teaching-host architecture."
metrics:
  tasks_completed: 1
  files_modified: 5
  completed: 2026-07-24
---

# Phase 01 Plan 07: Ecosystem Catalogs Summary

**Evidence-linked catalogs now route all known ecosystem candidates to explicit blocked states rather than allowing archive seeds or discovery pointers to become teaching-scope claims.**

## Accomplishments

- Added domain and archetype/convention records that state the blocked dependency on official immutable registry and projection evidence.
- Added a public-example catalog record with explicit provenance, license, adaptation, conformance, and lesson-use blockers.
- Added package and runtime analyses with the required ordered evidence headings, public-surface requirements, release/current-work distinction, and no-private-import policy.
- Preserved catalog inputs for Wave 7 teaching-scope and freshness work without selecting a domain, runtime, package, or teaching-host profile.

## Task Commits

1. **Task 1: Catalog protocol surfaces, implementation options, and examples** — `949e720` (`feat`)

## Verification

Passed:

- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md`
- Catalog existence assertion from the plan.
- `tools/phase1-python -m unittest discover -s tests/phase1` — 34 tests.
- `tools/phase1-python tools/validate-planning.py` — passed with expected pending-deliverables warning.

## Decisions Made

- Preserve each candidate as evidence-linked blocked research input until immutable official evidence and required human review exist.
- Require a released-package source record and a distinct repository/public-export source record before evaluating `napplet/web` consumption.
- Keep runtime dimensions classified as required behavior, possible architecture, host policy, or external adapter instead of treating any as settled architecture.

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None. Empty example/runtime fields are intentional blocked evidence states with a named source candidate, impact, open question, and refresh trigger; they are not UI or implementation placeholders.

## Threat Flags

None. This plan added only local evidence records and analysis; it introduced no endpoint, auth, file-access, or schema trust-boundary surface.

## Self-Check: PASSED

- Found all five catalog/map artifacts and this summary at their declared paths.
- Verified task commit `949e720` resolves in Git.
