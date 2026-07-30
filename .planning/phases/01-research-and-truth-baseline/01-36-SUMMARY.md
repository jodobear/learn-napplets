---
phase: 01-research-and-truth-baseline
plan: 36
subsystem: package-evidence-safety
tags: [python, transactional-snapshot, sandbox-gate, package-evidence, sha256]
requires:
  - phase: 01-42
    provides: registered shared-lock canonical snapshots and recovery refusal
  - phase: 01-35
    provides: compatibility eligibility evaluation context
provides:
  - recovery-guarded SPK-G package measurement receipts
  - deterministic five-sample no-operation evidence for unqualified package input
  - digest-bound blocked impact hand-off retaining static and Firefox fallbacks
affects: [01-43, EVID-03, EVID-04, OPER-01, ADR-0010]
tech-stack:
  added: []
  patterns:
    - snapshot-before-parse-and-argv package safety gate
    - fail-closed no-network sandbox-contract receipt
    - all-or-nothing retained spike evidence bundle
key-files:
  created:
    - tools/measure-package-conformance.py
    - tools/run-spk-g-sandbox.py
  modified:
    - tests/phase1/test_spikes.py
    - .planning/spikes/spk-g-package-conformance/metadata.yaml
    - .planning/spikes/spk-g-package-conformance/measurements.yaml
    - .planning/spikes/spk-g-package-conformance/report.md
    - .planning/spikes/spk-g-package-conformance/impact-fragment.yaml
key-decisions:
  - "SPK-G remains a deterministic no-operation receipt until recovered evidence has a complete exact artifact and separately dated approval."
  - "Sandbox capability discovery fails closed; an environment toggle cannot attest that OS controls are enforced."
requirements-completed: [EVID-03, EVID-04, OPER-01]
coverage:
  - id: D1
    description: Recovery-guarded eligibility and sandbox gate refuses package work before argv construction.
    requirement: OPER-01
    verification:
      - kind: unit
        ref: tests/phase1/test_spikes.py#test_spk_g_reader_reads_one_transactional_snapshot_or_refuses
        status: pass
      - kind: unit
        ref: tests/phase1/test_spikes.py#test_spk_g_sandbox_blocks_unavailable_or_escape_prone_execution
        status: pass
    human_judgment: false
  - id: D2
    description: Five digest-bound SPK-G blocked receipts retain exact missing evidence and safe fallback.
    requirement: EVID-04
    verification:
      - kind: other
        ref: tools/phase1-python tools/measure-package-conformance.py --spike .planning/spikes/spk-g-package-conformance --run-five
        status: pass
      - kind: other
        ref: tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-g-package-conformance --complete
        status: pass
      - kind: other
        ref: tools/phase1-python tools/validate-research.py validate-impact-fragment .planning/spikes/spk-g-package-conformance/impact-fragment.yaml --root .planning
        status: pass
    human_judgment: false
metrics:
  duration: 12m 17s
  completed: 2026-07-30
  tasks: 2
  files: 9
status: complete
---

# Phase 01 Plan 36: SPK-G package conformance gate Summary

**Recovery-guarded SPK-G now retains five digest-bound, zero-operation package-evidence receipts when its exact public artifact, approval, and sandbox prerequisites are absent.**

## Performance

- **Duration:** 12m 17s
- **Started:** 2026-07-30T17:31:51Z
- **Completed:** 2026-07-30T17:44:08Z
- **Tasks:** 2/2
- **Files modified:** 9

## Accomplishments

- Added a Plan 01-42 snapshot-first SPK-G runner that refuses before canonical parsing, sandbox argv construction, or package operation when its recovered evidence is incomplete.
- Added a fail-closed sandbox contract and tests covering missing eligibility, dated approval, sandbox controls, interrupted journals, and evidence-retention rollback.
- Retained five zero-operation blocked receipts, exact missing-reason categories, digests, safe fallback, and a validated blocked impact fragment without changing package, ADR, compatibility, or Firefox status.

## Task Commits

1. **Task 1: Gate one SPK-G measurement on qualified evidence and dated approval**
   - `bf897d3` — `test(01-36): add failing SPK-G measurement boundary tests`
   - `ae1d293` — `feat(01-36): gate SPK-G package measurement`
2. **Task 2: Retain five-result measurement or blocked outcome in canonical SPK-G evidence**
   - `dc849df` — `docs(01-36): retain SPK-G blocked measurement evidence`

## Files Created/Modified

- `tools/measure-package-conformance.py` — reads one registered immutable snapshot, evaluates all evidence gates, and emits no-operation or observed-only receipts.
- `tools/run-spk-g-sandbox.py` — defines a fail-closed no-network/read-only/minimal-environment sandbox contract.
- `tests/phase1/test_spikes.py` — covers gate ordering, snapshot recovery/refusal, sandbox refusal, and rollback.
- `.planning/spikes/spk-g-package-conformance/{metadata.yaml,recipe.md,fixture.md}` — records the recovery, approval, root-export, sandbox, static-fallback, and Firefox constraints.
- `.planning/spikes/spk-g-package-conformance/{measurements.yaml,report.md,impact-fragment.yaml}` — retains five validated blocked outputs and the canonical downstream hand-off.

## Decisions Made

- Retain a specific `SPK-G-BLOCKED-ELIGIBILITY` result rather than construct or execute a package operation from incomplete evidence.
- Treat sandbox availability as unverified unless an enforceable runtime probe attests the controls; a process environment marker is not proof.
- Continue to classify any future successful bounded operation as observed implementation behavior only.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Registered-support module loading did not populate `sys.modules`**
- **Found during:** Task 1 verification
- **Issue:** Dynamically loaded `run-spk-g-sandbox.py` failed while `@dataclass` resolved postponed annotations outside `sys.modules`.
- **Fix:** Registered each dynamically loaded support module before execution.
- **Files modified:** `tools/measure-package-conformance.py`
- **Verification:** All four SPK-G gate regressions pass.
- **Committed in:** `ae1d293`

**2. [Rule 1 - Evidence integrity] Rebound retained metadata digests after evidence updates**
- **Found during:** Task 2 retention
- **Issue:** The Task 1 metadata contract pins fixture, measurement, and report bytes; retaining updated evidence would otherwise leave its complete-spike digest checks stale.
- **Fix:** Updated only the required digest references while retaining the validated Task 2 evidence bundle.
- **Files modified:** `.planning/spikes/spk-g-package-conformance/metadata.yaml`
- **Verification:** Complete spike, report, and impact-fragment validators pass.
- **Committed in:** `dc849df`

---

**Total deviations:** 2 auto-fixed (2 Rule 1 bugs)
**Impact on plan:** Both corrections preserve fail-closed execution and evidence integrity; no package operation, live request, external write, approval, or architecture change occurred.

## Issues Encountered

- Current canonical evidence is substantively ineligible, so the authorized deterministic outcome is a five-sample no-operation blocker rather than a package import or conformance result.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 01-43 can consume the validated SPK-G blocked impact fragment only as proposed blocked evidence.
- A future package measurement requires complete immutable public artifact/source records, a separately dated approval, and verified OS sandbox enforcement.
- The deterministic static fallback and existing Firefox pre-attachment blocker remain unchanged.

## Self-Check: PASSED

Verified all seven implementation/evidence paths exist, `bf897d3`, `ae1d293`, and `dc849df` resolve on the active worktree branch, and the complete SPK-G verification suite passes.
