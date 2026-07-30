---
phase: 01-research-and-truth-baseline
plan: 41
subsystem: research-evidence
tags: [package-evidence, registry-receipts, provenance, spk-g, testing]
requires:
  - phase: 01-31
    provides: authority-gated research baseline and blocked package policy records
provides:
  - immutable, separately attributable fixture and live-or-blocker registry receipt histories
  - deterministic package evidence history and SPK-G blocked-admission routing
  - a dated package current-work snapshot that preserves OWS-001 history
  - regression coverage for receipt revalidation and package blocker routing
affects: [package-admission, SPK-G, ADR-0010, phase-02, phase-03, phase-05, phase-11]
tech-stack:
  added: []
  patterns: [exclusive-create-receipts, exact-byte-sha256-revalidation, append-only-evidence-history, impact-scoped-blockers]
key-files:
  created:
    - tools/collect-registry-evidence.py
    - .planning/research/reports/package-registry-fixture-receipt-20260728.yaml
    - .planning/research/reports/package-registry-live-or-blocker-receipt-20260728.yaml
  modified:
    - .planning/research/package-evidence.yaml
    - .planning/research/package-map.md
    - .planning/research/ecosystem-inventory.yaml
    - .planning/research/open-work-snapshot.json
    - tests/phase1/test_compatibility.py
    - tests/phase1/fixtures/registry-response.json
key-decisions:
  - "Fixture collection proves only collector and exact-byte receipt mechanics; it never establishes a published-package fact or approval."
  - "The live-or-blocker collection retains its own immutable attribution and routes incomplete eligibility to a scoped SPK-G blocker."
  - "OWS-001 and all historic unavailable records remain intact while OWS-002 appends the package-registry blocker snapshot."
patterns-established:
  - "Package evidence retains every receipt path, attempt ID, digest, transport, outcome, and classification instead of using a latest-wins pointer."
  - "SPK-G remains blocked until complete public artifact evidence and a separate package-admission approval exist."
requirements-completed: [EVID-03, EVID-04, OPER-01]
coverage:
  - id: D1
    description: "Fixture and live-or-blocker registry receipts remain distinct, immutable, exact-byte-revalidated histories."
    requirement: EVID-03
    verification:
      - kind: unit
        ref: "tests/phase1/test_compatibility.py#registry collector receipt tests"
        status: pass
      - kind: other
        ref: "tools/phase1-python tools/collect-registry-evidence.py validate-receipt"
        status: pass
    human_judgment: false
  - id: D2
    description: "Incomplete package evidence retains a deterministic, impact-scoped SPK-G blocked-admission route."
    requirement: EVID-04
    verification:
      - kind: unit
        ref: "tests/phase1/test_compatibility.py#test_package_metadata_preserves_history_and_blocker_routing"
        status: pass
      - kind: other
        ref: "tools/phase1-python tools/validate-research.py validate --root .planning/research"
        status: pass
    human_judgment: false
  - id: D3
    description: "Package evidence collection remains credential-free and never executes package code."
    requirement: OPER-01
    verification:
      - kind: unit
        ref: "tests/phase1/test_compatibility.py#test_registry_live_unavailable_routes_impact_scoped_blocker"
        status: pass
    human_judgment: false
duration: 56m
completed: 2026-07-30
status: complete
---

# Phase 01 Plan 41: Package Registry Evidence History Summary

**Immutable fixture and live-or-blocker registry receipts now retain exact-byte provenance and route incomplete package evidence into a deterministic SPK-G admission blocker.**

## Performance

- **Duration:** 56 min
- **Started:** 2026-07-30T15:34:44Z
- **Completed:** 2026-07-30T16:30:44Z
- **Tasks:** 2/2
- **Files modified:** 9

## Accomplishments

- Added a bounded GET-only collector with exclusive receipt creation, exact captured-byte SHA-256 validation, fixture-mechanism classification, and separate policy-gated live-or-blocker history.
- Recorded both receipt bindings in package evidence and documented the separation between repository identity, release commit, registry artifact, and collection receipts.
- Preserved `OWS-001` and its unavailable records while appending `OWS-002`; linked incomplete package eligibility to an impact-scoped SPK-G blocker with EVID/ADR/OQ/DRF impact IDs, fallback, and refresh trigger.
- Added deterministic regressions for retained receipt attribution, current-work history preservation, and SPK-G routing.

## Verification

Passed the full plan-level automated sequence:

- Three registry collector/receipt boundary tests, including fixture rehashing, distinct immutable receipt paths, overwrite refusal, receipt revalidation, and unavailable-live blocker routing.
- `test_published_package_metadata_requires_independent_registry_artifact`.
- `test_package_metadata_preserves_history_and_blocker_routing`.
- Both committed receipt files through `tools/collect-registry-evidence.py validate-receipt`.
- Canonical research validation via `tools/validate-research.py validate --root .planning/research --report /tmp/phase1-package-intake.md`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Collect immutable fixture and live-or-blocker registry receipts without overwriting either history** — `d35b6fa` (test), `dd6b0f1` (feat)
2. **Task 2: Preserve package history and package-to-SPK-G blocker routing** — `f659e54` (test), `38b26c6` (feat)

## Files Created/Modified

- `tools/collect-registry-evidence.py` — bounded, non-executing registry receipt collector and validator.
- `.planning/research/reports/package-registry-fixture-receipt-20260728.yaml` — immutable fixture-mechanism receipt.
- `.planning/research/reports/package-registry-live-or-blocker-receipt-20260728.yaml` — distinct impact-scoped live collection blocker receipt.
- `.planning/research/package-evidence.yaml` — retained two-receipt attribution and blocked package admission.
- `.planning/research/package-map.md` — explicit repository/release/artifact/receipt distinction and SPK-G routing.
- `.planning/research/ecosystem-inventory.yaml` — structured receipt history, eligibility checklist, and blocked routing.
- `.planning/research/open-work-snapshot.json` — appended OWS-002 package-registry snapshot while retaining OWS-001.
- `tests/phase1/test_compatibility.py` — receipt and package history regression coverage.
- `tests/phase1/fixtures/registry-response.json` — deterministic bounded registry transport fixture.

## Decisions Made

- Fixture evidence remains `fixture-mechanism-only` and cannot be promoted to a published-package fact or admission approval.
- The live collection's `impact-scoped-blocker` stays separately attributable, preserving fixture bytes and history.
- Package admission remains blocked until every SPK-G eligibility item is complete and a separate approval is recorded; the deterministic static path remains the fallback.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected the final JSON receipt-history regression assertion**
- **Found during:** Task 2: Preserve package history and package-to-SPK-G blocker routing
- **Issue:** The initial assertion compared Python tuples to JSON arrays, which cannot compare equal after JSON parsing even when the retained receipt fields match.
- **Fix:** Compared the explicit path, attempt ID, receipt digest, transport, outcome, and classification fields after parsing.
- **Files modified:** `tests/phase1/test_compatibility.py`
- **Verification:** `test_package_metadata_preserves_history_and_blocker_routing` passes.
- **Committed in:** `38b26c6` (part of the Task 2 feature commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** The test correction preserves the intended deterministic receipt-history contract without broadening scope.

## Issues Encountered

None beyond the corrected JSON assertion shape.

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Future package work can consume the retained receipt history without treating fixture output or repository data as artifact evidence.
- SPK-G remains intentionally blocked until a qualifying public artifact and separate package-admission approval resolve every listed eligibility item.
- No package installation, import, or execution was performed.

## Self-Check: PASSED

- Confirmed all nine task artifacts and this summary exist.
- Confirmed Task 1 commits `d35b6fa` and `dd6b0f1`, plus Task 2 commits `f659e54` and `38b26c6`, exist in the complete Git log.
- Confirmed no diff in `.planning/STATE.md` or `.planning/ROADMAP.md` and no support symlink change.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-30*
