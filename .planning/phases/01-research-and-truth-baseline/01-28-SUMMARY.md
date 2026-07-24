---
phase: 01-research-and-truth-baseline
plan: 28
subsystem: research-evidence-consolidation
tags: [python, yaml, jsonschema, evidence, provenance, transaction, replay]
requires:
  - phase: 01-09-through-01-20
    provides: "Completed SPK-A through SPK-L reports plus immutable impact fragments for SPK-C, SPK-D, SPK-G, and SPK-H"
provides:
  - "One lock-protected, deterministic canonical consolidation path for all Phase 1 spike evidence"
  - "History-preserving compatibility, drift, and open-question updates with blocked conflict review records"
  - "SPK-H security/egress synthesis, all-spike audit, and digest-pinned replay inventory"
affects: [01-21, 01-22, 01-23, 01-24, phase-2-product-contract]
tech-stack:
  added: []
  patterns:
    - "Exclusive fcntl.flock transaction with same-filesystem staging and byte-stable reruns"
    - "Stable-ID evidence merge that preserves history and routes incompatible inputs to blocked OQ review work"
    - "Digest-pinned replay manifest generated from report, metadata, measurement, and fixture inputs"
key-files:
  created:
    - .planning/research/reports/spike-consolidation.md
    - .planning/research/security-egress-findings.md
    - .planning/spikes/replay-manifest.yaml
  modified:
    - tools/validate-research.py
    - tests/phase1/test_spike_consolidation.py
    - .planning/research/compatibility-matrix.yaml
    - .planning/research/drift-register.yaml
    - .planning/research/open-questions.yaml
key-decisions:
  - "All SPK-A through SPK-L reports are accounted for; reports without a machine-readable impact fragment remain explicit no-impact-fragment context rather than inferred canonical facts."
  - "SPK-C, SPK-D, SPK-G, and SPK-H remain blocked or materially uncertain evidence; consolidation records attributable history but accepts no ADR or upstream conclusion."
  - "An incompatible stable fragment ID publishes a deterministic OQ-CONSOLIDATION review record containing both immutable evidence digests while preserving compatibility and drift targets."
patterns-established:
  - "Downstream ADR and closeout work consumes consolidation-issued canonical IDs and audit records, not raw spike prose as authority."
  - "Security/egress documentation separates source status, fixture observation, proposed project policy, unresolved questions, inference, uncertainty, and approval ownership."
requirements-completed: [EVID-02, EVID-03, EVID-04, OPER-01]
coverage:
  - id: D1
    description: "Serialized all-spike canonical merge preserves history, handles contention/failure, and routes incompatible stable IDs to blocked review work."
    requirement: EVID-02
    verification:
      - kind: unit
        ref: "tests/phase1/test_spike_consolidation.py"
        status: pass
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py consolidate-spike-impacts ... (two byte-compared runs)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Complete Phase 1 canonical evidence and all registered reports validate after transactional consolidation."
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md"
        status: pass
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-reports --root .planning"
        status: pass
    human_judgment: false
  - id: D3
    description: "Digest-pinned SPK-A through SPK-L replay inventory and SPK-H security/egress synthesis retain blocked cross-browser and upstream-evidence boundaries."
    requirement: OPER-01
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py replay-spikes --manifest .planning/spikes/replay-manifest.yaml --check"
        status: pass
    human_judgment: false
metrics:
  duration: 37m
  completed: 2026-07-24
status: complete
---

# Phase 01 Plan 28: Spike Evidence Consolidation Summary

**Locked, digest-pinned consolidation turns all twelve spike reports into one history-preserving canonical evidence state while retaining blocked browser, package, verifier, identity, manifest, and upstream-source uncertainty.**

## Performance

- **Duration:** 37 min
- **Started:** 2026-07-24T10:48:46Z
- **Completed:** 2026-07-24T11:26:02Z
- **Tasks:** 2/2
- **Files modified:** 8

## Accomplishments

- Verified the approved tracer commits and executed the real lock-protected consolidation for every SPK-A through SPK-L report, preserving six no-impact-fragment dispositions and serially merging the four validated impact fragments.
- Published canonical compatibility, drift, and open-question history; emitted a complete path/digest inventory, a replay manifest, and a deterministic all-spike audit with rerun input and replay-manifest digests.
- Generated the SPK-H security/egress synthesis with upstream-source status, local browser observations, proposed CSP policy, unresolved Firefox and upstream questions, inference, uncertainty, owner, and required approval kept distinct.
- Extended conflict handling so an incompatible stable fragment produces a deterministic blocked `OQ-CONSOLIDATION-*` review record containing both immutable fragment digests without replacing compatibility or drift evidence.

## Task Commits

Each task was committed atomically; TDD tasks retain their red and green commits.

1. **Task 1: Prove one immutable fragment-to-canonical merge path before full consolidation** - `072f439` (test), `b82740a` (feat)
2. **Task 2: Consolidate all spike reports and fragments into history-preserving canonical evidence** - `e4dd411` (test), `a1e8d90` (feat)

## Files Created/Modified

- `tools/validate-research.py` - Validates immutable fragment provenance, serializes lock-protected merge transactions, publishes blocked conflict work, and generates audit/manifest outputs.
- `tests/phase1/test_spike_consolidation.py` - Exercises contention, pre-commit rollback, stable reruns, and publication of deterministic incompatible-fragment review records.
- `.planning/research/compatibility-matrix.yaml` - Retains canonical compatibility history linked to consolidated drift evidence.
- `.planning/research/drift-register.yaml` - Adds SPK-C and SPK-H attributable blocked-observation history without asserting browser or protocol facts.
- `.planning/research/open-questions.yaml` - Adds source-linked blocked questions for Firefox, verified-loader, package, conformance, and egress evidence.
- `.planning/research/security-egress-findings.md` - Provides the constrained SPK-H security/egress synthesis.
- `.planning/research/reports/spike-consolidation.md` - Audits all twelve immutable inputs, dispositions, uncertainty, transaction behavior, and rerun identity.
- `.planning/spikes/replay-manifest.yaml` - Pins report, metadata, measurement, fixture paths, digests, replay commands, and freshness criteria for SPK-A through SPK-L.

## Decisions Made

- All report-only spikes are explicit `no-impact-fragment` audit entries; their report prose is explanatory context, not a source for inferred canonical claims.
- Canonical records retain blocked and uncertain observations as appended attributable history; no consolidation result accepts an ADR or promotes a fixture observation to upstream fact.
- Incompatible stable IDs are review work, not overwrite candidates: both immutable payload digests and combined impacts remain in deterministic `OQ-CONSOLIDATION-*` records.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Made the transaction success test independent of already-consolidated source fixtures**
- **Found during:** Task 2
- **Issue:** The contention test assumed the repository copy had no previously consolidated history, so it failed once the real Task 2 publication made the source fixture legitimately idempotent.
- **Fix:** The temporary test fixture now removes only consolidation-attributable history before testing a new successful transaction, preserving all unrelated history.
- **Files modified:** `tests/phase1/test_spike_consolidation.py`
- **Verification:** `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_spike_consolidation.py'`
- **Committed in:** `e4dd411`

**2. [Rule 2 - Missing Critical Functionality] Published conflict review records and complete transaction inventory**
- **Found during:** Task 2
- **Issue:** The tracer rejected incompatible fragments but did not publish the required deterministic `OQ-CONSOLIDATION-*` record with both digests; its audit also lacked metadata/measurement snapshot paths and digests plus a rerun input digest.
- **Fix:** Added deterministic conflict-record publication, stable input ordering, full input snapshot inventory, blocked/uncertain outcome accounting, replay-manifest digest, and rerun input digest.
- **Files modified:** `tools/validate-research.py`, `tests/phase1/test_spike_consolidation.py`, `.planning/research/reports/spike-consolidation.md`
- **Verification:** Consolidation unit suite, two byte-compared real consolidation runs, canonical validation, report validation, and replay-manifest check all pass.
- **Committed in:** `e4dd411`, `a1e8d90`

---

**Total deviations:** 2 auto-fixed (1 Rule 1 bug, 1 Rule 2 missing critical functionality).
**Impact on plan:** Both fixes enforce the explicit transaction, provenance, conflict-retention, and reproducibility requirements without expanding product scope.

## Issues Encountered

- The plan's historical tracer invocation omitted the required `--root .planning` argument for `validate-impact-fragment`; its committed unit suite remained the authoritative successful tracer verification, and Task 2 used the full consolidation command with explicit roots.
- The required canonical validator writes the pre-existing dirty `validation.md` report. It was backed up for verification and restored byte-identically, so it was neither altered in final state nor committed.

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plans 01-21 through 01-24 can consume the canonical compatibility, drift, open-question, security/egress, replay-manifest, and consolidation-audit records.
- Firefox launcher, manifest, identity, verifier, package/public-export, portable-target, and editor-related blockers remain explicit; no optional blocked capability was solved or selected.
- ADR acceptance, security exceptions, Phase 1 closeout, Phase 2 product/content contract approval, and any production scaffold remain human gates.

## Self-Check: PASSED

- Verified published audit, security synthesis, replay manifest, and summary file exist.
- Verified task commits `072f439`, `b82740a`, `e4dd411`, and `a1e8d90` resolve to commit objects.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
