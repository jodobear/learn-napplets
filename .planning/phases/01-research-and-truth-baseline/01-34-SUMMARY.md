---
phase: 01-research-and-truth-baseline
plan: 34
subsystem: research-evidence-validation
tags: [python, yaml, json-schema, provenance, migration, trust-boundary]
requires:
  - phase: 01-33
    provides: current canonical research registry and consolidated spike records
provides:
  - deterministic v1-to-v2 drift-register migration with retained fixtures and lineage
  - canonical impact-fragment path/source confinement
  - explicit observed-local drift evidence without normative authority
  - refreshed digest bindings for canonical registry provenance
affects: [01-35, 01-36, 01-42, research-validation, spike-consolidation]
tech-stack:
  added: []
  patterns:
    - deterministic YAML contract migration with preserved legacy fixtures
    - canonical path resolution below an explicit planning root
    - exclusive upstream-comparison and observed-local drift forms
key-files:
  created:
    - tools/migrate-phase1-records.py
    - .planning/research/schemas/legacy/drift.schema.v1.json
    - .planning/research/schemas/fixtures/drift-v1-legacy.yaml
    - .planning/research/schemas/fixtures/drift-v2-current.yaml
  modified:
    - tools/validate-research.py
    - .planning/research/schemas/drift.schema.json
    - .planning/research/drift-register.yaml
    - tests/phase1/test_drift.py
    - tests/phase1/test_spike_consolidation.py
key-decisions:
  - "Version 2 preserves v1 DRF/SRC/CLM lineage while sorting records, impacts, and history deterministically without deduplicating history."
  - "Local browser observations use a null normative side and OBS-prefixed observed-local provenance; they cannot carry source or claim authority fields."
  - "Impact-fragment source links must name the exact canonical registry file and validate its file digest independently of source-record content digests."
patterns-established:
  - "Migration commands validate input before atomically replacing output, keeping malformed legacy input from creating a partial result."
  - "Canonical planning links reject absolute paths, normalization components, symlink traversal, nonregular files, and non-spike-local evidence."
requirements-completed: [EVID-01, EVID-02, EVID-04, OPER-01]
coverage:
  - id: D1
    description: Deterministic retained v1-to-v2 drift migration
    requirement: EVID-01
    verification:
      - kind: unit
        ref: tests/phase1/test_drift.py#test_drift_v1_to_v2_migration
        status: pass
      - kind: other
        ref: tools/phase1-python tools/migrate-phase1-records.py migrate-drift --input .planning/research/schemas/fixtures/drift-v1-legacy.yaml --output /tmp/drift-v2.yaml
        status: pass
    human_judgment: false
  - id: D2
    description: Canonical fragment confinement and complete source binding
    requirement: EVID-02
    verification:
      - kind: unit
        ref: tests/phase1/test_spike_consolidation.py#test_fragment_rejects_noncanonical_path_or_source_substitution
        status: pass
      - kind: other
        ref: tools/phase1-python tools/validate-research.py validate-impact-fragment .planning/spikes/spk-c-boundary-harness/impact-fragment.yaml --root .planning
        status: pass
    human_judgment: false
  - id: D3
    description: Explicit observed-local drift classification without a normative authority side
    requirement: EVID-04
    verification:
      - kind: unit
        ref: tests/phase1/test_drift.py#test_drift_rejects_empty_null_and_single_sides; tests/phase1/test_drift.py#test_parallel_sides_are_distinct_and_adjacent
        status: pass
      - kind: other
        ref: tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/phase1-drift-v2.md
        status: pass
    human_judgment: false
metrics:
  duration: 14m
  completed: 2026-07-30
  tasks: 2
  files: 14
status: complete
---

# Phase 01 Plan 34: Evidence-safe drift migration and provenance confinement Summary

**Deterministic v2 drift evidence preserves v1 lineage while confining impact links and separating local browser measurements from normative upstream authority.**

## Performance

- **Duration:** 14m
- **Started:** 2026-07-30T14:40:56Z
- **Completed:** 2026-07-30T14:55:00Z
- **Tasks:** 2/2
- **Files modified:** 14

## Accomplishments

- Added an idempotent `migrate-drift` CLI, retained v1 schema/fixture artifacts, and canonical v2 fixture with stable-ID, impact, and history ordering.
- Added a v2 drift schema that makes complete parallel upstream sides exclusive from a null-normative, digest-pinned observed-local form.
- Confined fragment links to regular canonical files below the supplied planning root, including exact registry paths, complete source records, and independent file-digest checks.
- Reclassified the retained egress and Firefox launcher observations as blocked observed-local records with static fallbacks.

## Task Commits

1. **Task 1: Migrate drift v1 to v2 with deterministic ordering and retained lineage**
   - `c12f532` — `test(01-34): add failing drift migration regressions`
   - `97555fc` — `feat(01-34): migrate drift evidence to v2`
2. **Task 2: Close CR-05 confinement and CR-08 observed-local classification on migrated records**
   - `78a810f` — `test(01-34): add confinement and local evidence regressions`
   - `b8096de` — `feat(01-34): confine impact provenance and local drift evidence`

## Files Created/Modified

- `tools/migrate-phase1-records.py` — validates and atomically writes canonical v2 drift documents.
- `.planning/research/schemas/drift.schema.json` — defines mutually exclusive upstream-side and observed-local shapes.
- `.planning/research/drift-register.yaml` — holds v2 records and explicit local browser observations.
- `tools/validate-research.py` — resolves confined files and enforces source/provenance and local-evidence boundaries.
- `tests/phase1/test_drift.py` — covers migration, canonical ordering, local form, and distinct upstream sides.
- `tests/phase1/test_spike_consolidation.py` — covers path escape, substitution, and source-record rejection cases.
- `.planning/research/schemas/{legacy/drift.schema.v1.json,fixtures/drift-v1-legacy.yaml,fixtures/drift-v2-current.yaml,migration-notes.md}` — retained contract lineage and migration audit evidence.

## Decisions Made

- Preserve original v1 contract bytes as immutable migration input; use canonical ordering only in v2 output.
- Keep local fixture results blocked and self-describing through `OBS-*` records rather than constructing a normative counterpart.
- Treat source-registry artifact digests and individual source-record content digests as distinct trust assertions.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Repaired stale fixed-fragment provenance digests**
- **Found during:** Task 2 (confinement enforcement)
- **Issue:** Four consolidated impact fragments carried stale source-registry or metadata file digests, so strict canonical validation would reject the fixed fragments and all consolidation regressions.
- **Fix:** Refreshed only the affected canonical registry and metadata digest bindings in SPK-C, SPK-D, SPK-G, and SPK-H fragments; source IDs, source-record content digests, reports, measurements, statuses, and authority classifications remain unchanged.
- **Files modified:** `.planning/spikes/spk-c-boundary-harness/impact-fragment.yaml`, `.planning/spikes/spk-d-verified-loader/impact-fragment.yaml`, `.planning/spikes/spk-g-package-conformance/impact-fragment.yaml`, `.planning/spikes/spk-h-browser-egress/impact-fragment.yaml`
- **Verification:** Each fragment validates with the confined resolver; all eight spike-consolidation tests pass.
- **Committed in:** `b8096de`

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** The repair is required for the planned exact-digest validation and changes no source authority or ADR state.

## Issues Encountered

- The full Phase 1 unittest discovery was run once and had three pre-existing governance failures because this isolated worktree lacks `.planning/validation/required-artifacts.json`; this support artifact is outside this plan and was not edited. Task-owned `test_drift` and `test_spike_consolidation` modules, all specified regressions, deterministic migration, canonical research validation, and the fixed SPK-C fragment validation pass.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plans consuming drift records can rely on a current-format-only document, retained v1 audit trail, and explicit local provenance.
- Consolidation and publication work can use `resolve_canonical_file` for constrained planning-root evidence links.
- The isolated-worktree governance support artifact remains an external harness concern; no STATE.md or ROADMAP.md was changed.

## Self-Check: PASSED

Verified all created artifacts and all four TDD task commits (`c12f532`, `97555fc`, `78a810f`, `b8096de`) from the active worktree branch.
