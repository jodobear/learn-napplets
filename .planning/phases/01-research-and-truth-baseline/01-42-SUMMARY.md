---
phase: 01-research-and-truth-baseline
plan: 42
subsystem: canonical-evidence-recovery
tags: [python, fcntl, fsync, sha256, atomic-publication, transactional-reader]
requires:
  - phase: 01-34
    provides: valid v2 canonical research records and confined evidence paths
provides:
  - durable digest-bound journal recovery for complete canonical generations
  - registered shared-lock in-memory canonical snapshots for multi-file readers
  - fixed terminal and observed-refresh profile publication guarded by attestations
affects: [01-35, 01-36, 01-40, 01-43, research-validation, planning-preflight]
tech-stack:
  added: []
  patterns:
    - writer-exclusive and reader-shared flock protocol
    - same-filesystem staged/backed-up journal transaction with fsync boundaries
    - fixed profile target maps with target-only SHA-256 aggregates
key-files:
  created:
    - tools/canonical-recovery.py
  modified:
    - tools/validate-research.py
    - tools/validate-planning.py
    - tools/refresh-sources.py
    - tests/phase1/test_spike_consolidation.py
    - .gitignore
key-decisions:
  - "Canonical readers must register an exact named target set and parse only the returned immutable byte mapping."
  - "Publish profiles accept only fixed logical target maps and attestations binding each target plus a target-only aggregate."
patterns-established:
  - "Prepared or publishing journals recover only to verified old bytes; committed journals must verify the complete new bytes."
  - "Runtime transaction lock files are ignored, never committed evidence artifacts."
requirements-completed: [EVID-01, EVID-02, EVID-04, OPER-01]
coverage:
  - id: D1
    description: Durable interrupted-generation recovery and tampered-journal refusal
    requirement: OPER-01
    verification:
      - kind: unit
        ref: tests/phase1/test_spike_consolidation.py#SpikeConsolidationTests.test_recovery_after_each_publish_interruption_is_coherent
        status: pass
      - kind: unit
        ref: tests/phase1/test_spike_consolidation.py#SpikeConsolidationTests.test_recovery_rejects_tampered_or_incomplete_journal_before_reader_entry
        status: pass
    human_judgment: false
  - id: D2
    description: Registered shared-lock canonical snapshots and fixed attested profile publisher
    requirement: EVID-02
    verification:
      - kind: unit
        ref: tests/phase1/test_spike_consolidation.py#SpikeConsolidationTests.test_transactional_multi_file_reader_never_observes_mixed_generation_during_successful_publish
        status: pass
      - kind: other
        ref: tools/phase1-python tools/canonical-recovery.py publish-validated-canonical-set --help
        status: pass
    human_judgment: false
metrics:
  duration: 20m
  completed: 2026-07-30
  tasks: 1
  files: 6
status: complete
---

# Phase 01 Plan 42: Durable canonical publication and snapshot recovery Summary

**A fsynced journaled publisher and shared-lock snapshot API now prevent canonical multi-file readers from consuming interrupted or mixed evidence generations.**

## Performance

- **Duration:** 20m
- **Started:** 2026-07-30T16:24:00Z
- **Completed:** 2026-07-30T16:44:48Z
- **Tasks:** 1/1
- **Files modified:** 6

## Accomplishments

- Added `tools/canonical-recovery.py` with durable staging, backup, prepared/publishing/committed journals, digest validation, deterministic recovery, and lock contention refusal.
- Added exact reader and publisher registries: registered readers receive immutable in-memory snapshots while terminal and observed-refresh profiles accept only fixed target maps and exact attestations.
- Routed planning and source-refresh entrypoints through recovery/snapshot checks and added a recovery command to research validation.
- Added copied-root interruption, tampered-journal, reader registration, snapshot, attestation, and CLI-contract regressions.

## Task Commits

1. **Task 1: Recover interrupted generations and return each reader one lock-held canonical snapshot**
   - `9772a04` — `test(01-42): add failing recovery transaction regressions`
   - `b3dc4ea` — `feat(01-42): add journaled canonical recovery`
   - `e5bb533` — `chore(01-42): ignore canonical recovery locks`

## Files Created/Modified

- `tools/canonical-recovery.py` — durable publisher, recovery primitive, registration contract, shared-lock reader, and validated-profile CLI.
- `tools/validate-research.py` — exposes recovery through `recover-consolidation` and provides snapshot integration helpers.
- `tools/validate-planning.py` — refuses a canonical journal failure before multi-file planning preflight proceeds.
- `tools/refresh-sources.py` — reads the canonical source family from one registered snapshot for the standard refresh route.
- `tests/phase1/test_spike_consolidation.py` — recovery and transactional-reader regression coverage at the public test path.
- `.gitignore` — excludes generated canonical lock files.

## Decisions Made

- Preserve unfinished evidence transaction material until recovery proves a complete old generation or verifies the complete committed new generation.
- Keep attestation files outside the target-only aggregate domain to avoid self-referential terminal validation.
- Use closed profile and reader registries rather than caller-supplied path collections.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Ignored runtime canonical lock files**
- **Found during:** Task 1 verification
- **Issue:** The writer/reader lock protocol creates root and planning lock files that otherwise remain untracked after verification.
- **Fix:** Added exact lock-file rules to `.gitignore`.
- **Files modified:** `.gitignore`
- **Verification:** `git status --short` no longer reports generated canonical lock files.
- **Committed in:** `e5bb533`

---

**Total deviations:** 1 auto-fixed (1 Rule 2 missing critical)
**Impact on plan:** Required runtime-artifact hygiene only; canonical evidence history and planning records remain unchanged.

## Issues Encountered

- The baseline Plan 01-42 test names were required on `SpikeConsolidationTests`; copied-root transaction fixtures are delegated through that established public class path while remaining isolated from legacy consolidation setup.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 01-35 can register and consume the `compatibility-baseline` snapshot without reopening canonical paths.
- Plan 01-36 can use the reserved SPK-G snapshot profile before any package operation.
- Plan 01-40 and Plan 01-43 can use the terminal and observed-refresh publisher profiles, respectively, after their task-owned staged validation creates the external attestations.

## Self-Check: PASSED

Verified `tools/canonical-recovery.py` and the recovery regressions exist; confirmed task commits `9772a04`, `b3dc4ea`, and `e5bb533` are present on the active worktree branch. The complete Plan 01-42 automated verification sequence passed.
