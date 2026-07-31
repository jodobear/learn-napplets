---
phase: 01-research-and-truth-baseline
plan: 47
subsystem: evidence-integrity
tags: [immutable-provenance, source-refresh, evidence-labeling, yaml, python, static-content-handoff]

requires:
  - phase: 01-research-and-truth-baseline
    provides: "Plan 01-46 repository-confined source acquisition, atomic canonical publication, and observed-local drift safety"
provides:
  - "Four digest-verified 2026-07-31 immutable source records with separate draft, implementation, and native-reference authority labels"
  - "Source-linked claims, terminology, compatibility, drift, and open-question records that retain package, runtime, browser, and protocol blockers"
  - "Website-ready truth handoff with stable source/claim/term IDs, status labels, safe explanatory statements, and narrow refresh triggers"
  - "Git-reachable historical source-registry validation for retained completed-spike evidence"
affects: [01-48, static-site-content, source-status-display, compatibility-review, evidence-refresh]

tech-stack:
  added: []
  patterns: [immutable revision-path-digest provenance, authority-evidence-maturity separation, Git-reachable historical evidence binding, structured static-content handoff]

key-files:
  created: []
  modified:
    - .planning/research/source-registry.yaml
    - .planning/research/claims.yaml
    - .planning/research/compatibility-matrix.yaml
    - .planning/research/drift-register.yaml
    - .planning/research/decision-summary.md
    - .planning/research/executive-summary.md
    - .planning/phases/01-research-and-truth-baseline/01-TRUTH-REFRESH.md
    - .planning/phases/01-research-and-truth-baseline/01-RESEARCH.md
    - tools/validate-research.py
    - tests/phase1/test_compatibility.py
    - tests/phase1/test_spikes.py

key-decisions:
  - "Render Plan 01-48 explanatory content only from stable source, claim, term, and blocker IDs with separate authority, evidence class, maturity, state, uncertainty, and refresh labels."
  - "Keep OWS-004 mutable pull-request direction and the pre-existing 2026-07-28 PR snapshot separate from the four immutable 2026-07-31 source records."
  - "Treat a completed spike's source-registry digest as valid only when it matches the current regular file or exact bytes in a Git-reachable historical registry revision."
  - "Keep direct NIP-5D, package, runtime, browser, conformance, teaching-host, portability, ADR, and Phase 2 outcomes blocked or proposed."

patterns-established:
  - "Static explanatory facts must carry their canonical IDs and status dimensions rather than a flattened support label."
  - "A later canonical source refresh must preserve prior evidence identity through a reachable exact historical snapshot, not rewrite retained spike evidence to the new current digest."

requirements-completed: []
requirements-addressed: [EVID-01, EVID-02, EVID-03, OPER-01]
coverage:
  - id: D1
    description: "Four 2026-07-31 upstream blobs are pinned to exact commit/path/digest provenance with authority, evidence, maturity, uncertainty, impact, and refresh metadata."
    requirement: EVID-01
    verification:
      - kind: integration
        ref: "tools/phase1-python provenance digest check for SRC-*-20260731"
        status: pass
      - kind: other
        ref: "isolated tools/validate-research.py validate --root <temporary research copy>"
        status: pass
    human_judgment: false
  - id: D2
    description: "Claims, terminology, compatibility, drift, and questions visibly preserve draft/implementation/reference distinctions and blocked dimensions."
    requirement: EVID-02
    verification:
      - kind: unit
        ref: "tests/phase1/test_compatibility.py and tests/phase1/test_drift.py"
        status: pass
      - kind: other
        ref: "isolated tools/validate-research.py validate --root <temporary research copy>"
        status: pass
    human_judgment: false
  - id: D3
    description: "A structured truth handoff supplies safe statements, stable IDs, required display labels, blocked topics, and refresh triggers for the dependency-free static site."
    requirement: OPER-01
    verification:
      - kind: integration
        ref: "tools/validate-research.py validate-reports --root .planning"
        status: pass
      - kind: other
        ref: "tools/validate-planning.py"
        status: pass
    human_judgment: false
  - id: D4
    description: "Retained completed-spike source-registry links accept only current or Git-reachable exact historical bytes after a legitimate truth refresh."
    requirement: EVID-03
    verification:
      - kind: unit
        ref: "tests/phase1/test_spikes.py#SpikeValidationTests.test_completed_spike_accepts_reachable_historical_registry_digest_only"
        status: pass
    human_judgment: false

metrics:
  duration: 22m 31s
  completed: 2026-07-31
status: complete
---

# Phase 01 Plan 47: Immutable Truth Refresh Summary

**Four dated upstream source blobs now feed source-linked claims, explicit compatibility/drift blockers, and a static-site-safe truth handoff without presenting draft or implementation behavior as settled protocol authority.**

## Performance

- **Duration:** 22m 31s
- **Started:** 2026-07-31T03:14:55Z
- **Completed:** 2026-07-31T03:37:26Z
- **Tasks:** 3/3
- **Files modified:** 16 task artifacts

## Accomplishments

- Verified Task 1 commit `67e7593` and retained four exact 2026-07-31 immutable source blobs: a repository-local NAP draft, alpha napplet/web observation, Kehto/Paja observation, and optional Nampplets native reference.
- Added stable source-linked claims and terminology, then refreshed the compatibility matrix, drift records, open question, and protocol map without turning absence, README prose, or mutable pull-request direction into support.
- Published a common-record truth handoff for Plan 01-48 with safe source/claim/term IDs, mandatory status labels, prohibited topics, and narrow refresh triggers.
- Safely integrated the pre-existing `01-RESEARCH.md` working-tree addition by retaining its 2026-07-28 PR-derived snapshot as historical candidate context and explicitly separating it from the 2026-07-31 canonical blobs.
- Repaired retained spike validation so a legitimate current source-registry refresh does not falsely invalidate a completed spike whose exact prior registry bytes are Git-reachable.

## Task Commits

Each task was committed atomically:

1. **Task 1: Bind refreshed sources to immutable provenance** — `67e7593` (`feat`)
2. **Task 2: Refresh claims, terminology, protocol map, drift, and compatibility** — `2494446` (`feat`)
3. **Task 3: Publish one website-ready truth summary** — `7c3b962` (`feat`)

## Files Created/Modified

- `.planning/research/source-registry.yaml` — retains the four dated source identities, revisions, locators, digests, classifications, impacts, and refresh triggers.
- `.planning/research/claims.yaml`, `terminology-map.yaml`, and `protocol-map.md` — provide site-safe stable IDs and preserve the distinctions between draft specification, observed implementation, native reference, policy, and blocker.
- `.planning/research/compatibility-matrix.yaml`, `drift-register.yaml`, and `open-questions.yaml` — retain all substantive compatibility dimensions and unresolved conflicts as blocked.
- `.planning/research/open-work-snapshot.json` and `open-work-analysis.md` — retain mutable PR direction separately as `OWS-004` context.
- `.planning/research/decision-summary.md` and `executive-summary.md` — derive the current decision/readiness reading from canonical records rather than stale prose.
- `.planning/phases/01-research-and-truth-baseline/01-TRUTH-REFRESH.md` — supplies the compact Plan 01-48 source/status content handoff.
- `.planning/phases/01-research-and-truth-baseline/01-RESEARCH.md` — preserves and explicitly qualifies the pre-existing 2026-07-28 candidate refresh alongside the new canonical refresh.
- `tools/validate-research.py` and `tests/phase1/test_spikes.py` — validate current or Git-reachable historical source-registry digests for retained completed-spike evidence.
- `tests/phase1/test_compatibility.py` — covers the appended `OWS-004` immutable truth-refresh snapshot.

## Verification

Passed:

- `tools/phase1-python --verify-toolchain`.
- Four exact source-cache SHA-256 checks for `SRC-NAPS-NAP-INTENT-20260731`, `SRC-NAPPLET-WEB-20260731`, `SRC-KEHTO-WEB-PAJA-20260731`, and `SRC-NAMPLETS-NATIVE-20260731`.
- Isolated canonical schema/semantic validation using `tools/validate-research.py validate --root <temporary research copy>`.
- `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_compatibility test_drift test_spikes.SpikeValidationTests.test_completed_spike_accepts_reachable_historical_registry_digest_only` — 26 tests passed.
- `tools/phase1-python tools/validate-research.py validate-reports --root .planning`.
- `tools/phase1-python tools/validate-planning.py` — 0 errors, 0 warnings.
- `git diff --check`.

Known historical boundary:

- The canonical-root form of `tools/validate-research.py validate --root .planning/research` still stops before semantic validation with `PRE118: review plan manifest is not the exact active plan set`. This was run and confirmed; it is the pre-existing historical exact-active-plan binding failure explicitly deferred outside the owner-authorized recovery scope. This plan does not alter, waive, or claim to repair PRE118. The isolated semantic route above validates the changed record set without bypassing the canonical preflight for any claim of terminal Phase 1 completion.

## Decisions Made

- The static site may state only the bounded descriptions in `01-TRUTH-REFRESH.md`; every protocol-sensitive display must expose source ID, authority/evidence class, maturity, state, uncertainty, and refresh trigger.
- The 2026-07-28 PR-derived material stays as historical candidate/directional context. `OWS-004` keeps mutable PR metadata separate from immutable blob-backed sources.
- Completed spike metadata keeps its historical source-registry digest. Validation now verifies that it maps to a regular current registry or Git-reachable exact historical registry bytes, rather than falsely re-binding it to the latest registry.
- Plan 01-47 addresses EVID-01, EVID-02, EVID-03, and OPER-01 but does not mark a Phase 1 requirement or the phase complete: direct NIP-5D, package, runtime/browser, conformance, approval, and PRE118 constraints remain open.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated snapshot regression coverage for the new truth-refresh history entry**
- **Found during:** Task 2 verification.
- **Issue:** `test_package_metadata_preserves_history_and_blocker_routing` asserted that `open-work-snapshot.json` ended at `OWS-003`, so Task 1's intentional `OWS-004` append made the focused compatibility test fail.
- **Fix:** Extended the regression to assert the immutable 2026-07-31 snapshot's parent, retrieval time, source IDs, and separate mutable-direction statuses.
- **Files modified:** `tests/phase1/test_compatibility.py`.
- **Verification:** Focused compatibility/drift suite passed.
- **Committed in:** `2494446`.

**2. [Rule 1 - Bug] Preserved historical source-registry bindings for completed spikes**
- **Found during:** Task 3 report validation.
- **Issue:** `validate-reports` rejected seven completed spike reports after the planned source-registry refresh because it required their historically pinned registry digest to equal the latest registry file.
- **Fix:** Restricted validation to the current regular registry file or exact bytes from a Git-reachable historical registry revision, with a regression that rejects an unknown digest.
- **Files modified:** `tools/validate-research.py`, `tests/phase1/test_spikes.py`.
- **Verification:** New regression, report validation, planning validation, and the focused suite passed.
- **Committed in:** `7c3b962`.

**3. [Rule 2 - Evidence tracking] Kept addressed Phase 1 requirements pending rather than marking them complete**
- **Found during:** Final tracking update.
- **Issue:** The plan links EVID-01, EVID-02, EVID-03, and OPER-01, but canonical records retain direct-authority, compatibility, human-approval, and PRE118 blockers. Marking them complete would violate the project Definition of Done and misstate live status.
- **Fix:** Recorded the requirements as addressed in this summary and retained their existing pending/gaps-found tracking state; no requirement checkbox was auto-completed.
- **Files modified:** `.planning/phases/01-research-and-truth-baseline/01-47-SUMMARY.md`, `.planning/STATE.md`.
- **Verification:** `CMP-BASELINE-001`, `OQ-UPSTREAM-BASELINE-001`, and the preserved PRE118 result remain visibly blocked.
- **Committed in:** Plan metadata commit.

**4. [Rule 3 - Blocking] Corrected the stale next-plan position after state advancement**
- **Found during:** Final state update.
- **Issue:** `state.advance-plan` incremented the legacy `Plan: 2 of 48` body field to `3 of 48` even though disk summaries and the roadmap correctly report 47 of 48 plans complete.
- **Fix:** Used the GSD state update handler to set the next executable position to `Plan: 48 of 48`, recorded the Plan 01-48 resume file, and reconciled stale metric/todo prose so completed recovery plans are not listed as pending.
- **Files modified:** `.planning/STATE.md`.
- **Verification:** STATE frontmatter records `completed_plans: 47`; ROADMAP records `47/48`; Current Position now reads `Plan: 48 of 48`; only Plan 01-48 remains in Pending Todos.
- **Committed in:** Plan metadata commit.

---

**Total deviations:** 4 auto-fixed (2 Rule 1 bugs, 1 Rule 2 evidence-tracking correction, 1 Rule 3 state-tracking repair)
**Impact on plan:** The corrections preserve exact historical evidence, run the planned focused verification, prevent false phase-requirement completion, and accurately route the next plan. Neither adds a runtime, package, external service, or architectural selection.

## Issues Encountered

- Canonical-root semantic validation remains blocked by the historical PRE118 exact-active-plan binding. The scope boundary was respected: no terminal-review, plan-binding, or PRE118 machinery was changed. The existing isolated validation route verified the updated records, while the known blocker remains visible for separately approved work.

## Known Stubs

None. The scan found only existing test mock fixtures using empty argv/stdout/stderr values; they are intentional subprocess test inputs and do not flow to a user-facing or evidence-rendering surface.

## Threat Flags

| Flag | File | Description |
| --- | --- | --- |
| `threat_flag: local-git-history-read` | `tools/validate-research.py` | Completed-spike validation now invokes fixed-argv, timeout-bounded local Git reads for one hard-coded registry path; it accepts only exact SHA-256 bytes from reachable history. |

## User Setup Required

None — no external service configuration or package installation was added.

## Next Phase Readiness

- Plan 01-48 can build the owner-authorized dependency-free static site from the stable `SRC-*`, `CLM-*`, terminology, drift, question, and truth-refresh handoff records.
- The site must keep all listed status labels and blockers visible; it cannot consume packages, run a host/guest runtime, contact live systems, or imply source-qualified support.
- Phase 1 remains `gaps_found` until separately authorized work resolves the deferred PRE118 and broader direct-authority/package/runtime/browser/conformance/approval requirements.

## Self-Check: PASSED

- Confirmed all key Task 1–3 artifacts and this summary exist in the main working tree.
- Confirmed commits `67e7593`, `2494446`, and `7c3b962` are reachable.
- Confirmed no tracked-file deletions or whitespace errors were introduced by the plan commits.
