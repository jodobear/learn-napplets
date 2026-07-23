---
phase: 01-research-and-truth-baseline
plan: "04"
subsystem: research-evidence-validation
tags: [python, json-schema, yaml, spike, governance, provenance, validation]

requires:
  - phase: 01-02
    provides: "Safe YAML, Draft 2020-12 validation, and immutable source/claim semantics"
provides:
  - "Versioned disposable SPK and reproducibility-environment contracts"
  - "Canonical report, governance, lesson-index, ADR, migration, and impact-fragment validation"
  - "Explicit separation of automated verification from required human approval"
affects: [phase-1-spikes, phase-1-consolidation, phase-governance, ADR-recommendations]

tech-stack:
  added: []
  patterns: [pre-run-versus-complete-validation, safe-local-YAML-validation, immutable-digest-links, approval-separation]

key-files:
  created:
    - .planning/research/schemas/spike.schema.json
    - .planning/research/schemas/environment.schema.json
    - .planning/research/schemas/report-contract.yaml
    - .planning/research/schemas/phase-governance.schema.json
    - .planning/research/schemas/migration-notes.md
    - .planning/research/schemas/spike-impact-fragment.schema.json
    - tests/phase1/test_spikes.py
    - tests/phase1/test_governance.py
    - tests/phase1/test_spike_consolidation.py
  modified:
    - tools/validate-research.py

key-decisions:
  - "Pre-run spike contracts intentionally omit observations, while completion requires replayable environment, measured output, digests, and local replay evidence."
  - "The evidence policy's ten ordered H2 headings are the canonical report authority; the preserved template is structural aid only."
  - "A passing validator result prepares evidence for review but cannot create human approval or convert an ADR from proposed to accepted."
  - "Impact fragments pin metadata, reports, source links, and measurements with SHA-256 digests before consolidation."

patterns-established:
  - "Validate a record's strict schema before resolving its local paths, stable IDs, and immutable content digests."
  - "Treat a blocked spike as complete evidence only when its inputs, impacts, and local blocked replay result remain attributable."

requirements-completed: [EVID-04, OPER-03]
coverage:
  - id: D1
    description: "SPK envelopes distinguish measurement-free pre-run contracts from completed evidence and require five-sample browser or nondeterministic measurements."
    requirement: EVID-04
    verification:
      - kind: unit
        ref: "tests/phase1/test_spikes.py via tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_spikes.py'"
        status: pass
    human_judgment: false
  - id: D2
    description: "Governance, reports, lesson indices, ADR proposals, schema migrations, and immutable spike impact fragments fail closed through the common CLI."
    requirement: OPER-03
    verification:
      - kind: integration
        ref: "tests/phase1/test_governance.py, tests/phase1/test_spike_consolidation.py, and tools/validate-research.py validate"
        status: pass
    human_judgment: false

duration: 14m
completed: 2026-07-23
status: complete
---

# Phase 01 Plan 04: Reproducible Spike and Governance Contracts Summary

**Versioned SPK evidence envelopes, reproducibility manifests, report/governance conventions, and digest-pinned impact fragments now make disposable Phase 1 experiments replayable without allowing automation to stand in for human approval.**

## Performance

- **Duration:** 14m
- **Started:** 2026-07-23T22:46:38Z
- **Completed:** 2026-07-23T23:00:46Z
- **Tasks:** 2/2
- **Files modified:** 10

## Accomplishments

- Added strict SPK and environment schemas plus `validate-spike --contract|--complete`, including isolated non-production paths, safety declarations, local replay, raw-output digests, and five-sample range/median rules.
- Added the canonical ten-heading report contract, phase governance contract, lesson-index and proposed-ADR validation, plus migration-note enforcement for breaking schema changes.
- Added immutable spike impact-fragment validation for metadata, report, source, and measurement paths with SHA-256 checks, typed proposed impacts, and the SPK-H security/egress extension.
- Added focused negative fixtures for each contract and passed the complete available Phase 1 test and validator suite.

## Task Commits

1. **Task 1: Define the validated SPK envelope and reproducibility environment** - `8822364` (test), `4348301` (feat)
2. **Task 2: Add report, governance, lesson-index, and schema-evolution validation to the common CLI** - `6ddfe43` (test), `b61efb3` (feat)

## Files Created/Modified

- `.planning/research/schemas/spike.schema.json` - Versioned pre-run and completed SPK evidence-envelope contract.
- `.planning/research/schemas/environment.schema.json` - Exact OS, browser, runtime, dependency, flag, and command-hash manifest contract.
- `.planning/research/schemas/report-contract.yaml` - Canonical report heading order, discovery rules, and spike metadata-link convention.
- `.planning/research/schemas/phase-governance.schema.json` - Owner, approver, exit-evidence, verification, approval, and final-result contract.
- `.planning/research/schemas/migration-notes.md` - Deterministic migration and breaking-change procedure.
- `.planning/research/schemas/spike-impact-fragment.schema.json` - Digest-pinned typed fragment contract for later spike consolidation.
- `tools/validate-research.py` - Common CLI commands for spike, report, governance, lesson, ADR, migration, and fragment validation.
- `tests/phase1/test_spikes.py` - Pre-run/post-run spike-envelope fixtures.
- `tests/phase1/test_governance.py` - Report, governance, lesson-index, ADR, and migration failure fixtures.
- `tests/phase1/test_spike_consolidation.py` - Fragment identity, digest, dangling-link, and SPK-H extension fixtures.

## Decisions Made

- Pre-run envelope validation proves declared experiment safety and replay inputs without falsely demanding observations; completed validation adds post-run evidence requirements.
- The project evidence policy is the canonical report-heading authority; the preserved source-pack report template remains non-authoritative structural guidance.
- Human approval remains a separate governance state: no green validation or applicable-gate waiver can produce a passed phase result by itself.
- Consolidation must consume typed impact fragments that resolve each referenced local artifact and SHA-256 digest before use.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical Functionality] Added spike CLI support during Task 1**
- **Found during:** Task 1
- **Issue:** The Task 1 behavior requires `validate-spike --contract|--complete`, but its bounded file list omitted the common CLI that must expose the feature.
- **Fix:** Added the minimal `validate-spike` command path to the declared common enforcement boundary, preserving Task 2 for the broader report/governance/fragment extensions.
- **Files modified:** `tools/validate-research.py`
- **Verification:** `tests/phase1/test_spikes.py` passes.
- **Committed in:** `4348301`

**2. [Rule 1 - Bug] Repaired contract parsing and isolated-fixture compatibility**
- **Found during:** Task 2
- **Issue:** Initial raw-string patterns double-escaped report and stable-ID expressions, and root validation incorrectly required migration notes in temporary source/claim test roots.
- **Fix:** Corrected the regexes and made migration-note enforcement conditional on an existing optional schema artifact in isolated roots.
- **Files modified:** `tools/validate-research.py`
- **Verification:** All 28 Phase 1 tests and both validators pass.
- **Committed in:** `b61efb3`

**3. [Rule 2 - Missing Critical Functionality] Pinned metadata and report bytes in impact fragments**
- **Found during:** Task 2
- **Issue:** The initial fragment shape carried SHA-256 values for sources and measurements but not the report and metadata paths required by the task's immutable-link contract.
- **Fix:** Required `metadataSha256` and `reportSha256` and validated both against the referenced local files.
- **Files modified:** `.planning/research/schemas/spike-impact-fragment.schema.json`, `tools/validate-research.py`, `tests/phase1/test_spike_consolidation.py`
- **Verification:** Fragment digest, dangling-link, semantic-mismatch, and SPK-H fixtures pass.
- **Committed in:** `b61efb3`

---

**Total deviations:** 3 auto-fixed (1 Rule 1 bug, 2 Rule 2 missing-critical-functionality fixes)
**Impact on plan:** All fixes are contained in the plan's declared contract and enforcement files; no production scaffold, archive change, or approval automation was introduced.

## Issues Encountered

None remaining. The task's initially conflicting bounded-file list and required spike CLI behavior were resolved by a minimal, contract-required extension to the declared common validator.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Later Phase 1 spikes can create disposable `SPK-*` directories with pre-run declarations, complete evidence, immutable impact fragments, and report links that share one enforcement boundary.
- The remaining research, spike, lesson, and ADR plans must continue to retain human review and proposed-only ADR states.

## Self-Check: PASSED

All ten plan artifacts exist; task commits `8822364`, `4348301`, `6ddfe43`, and `b61efb3` resolve; the stub scan found no known stubs; and `tools/phase1-python -m unittest discover -s tests/phase1`, `tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md`, `tools/phase1-python tools/validate-planning.py`, and `git diff --check` passed.
