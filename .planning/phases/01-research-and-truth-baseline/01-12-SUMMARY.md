---
phase: 01-research-and-truth-baseline
plan: "12"
subsystem: research-evidence
tags: [phase-1, evidence, verified-loader, immutable-fixture, blocked]

requires:
  - phase: 01-07
    provides: bounded source and claim catalog inputs
  - phase: 01-20
    provides: source-freshness evidence conventions
  - phase: 01-26
    provides: first teaching-scope and fallback constraints
provides:
  - source-bound blocked SPK-D verified-loader feasibility envelope
  - exact-byte fixture with a deterministic one-byte mutation case
  - digest-pinned replay evidence and immutable impact hand-off for serial consolidation
affects: [01-28, ADR-0005, ADR-0008, phase-02-product-contract]

tech-stack:
  added: []
  patterns:
    - Per-primitive immutable SRC/CLM bindings with blocked classification when reviewed verification evidence is absent
    - Five-sample deterministic byte-integrity replay that never substitutes for cryptographic verification

key-files:
  created:
    - .planning/spikes/spk-d-verified-loader/fixture.json
    - .planning/spikes/spk-d-verified-loader/environment.json
    - .planning/spikes/spk-d-verified-loader/measurements.yaml
    - .planning/spikes/spk-d-verified-loader/report.md
    - .planning/spikes/spk-d-verified-loader/impact-fragment.yaml
  modified:
    - .planning/spikes/spk-d-verified-loader/metadata.yaml
    - .planning/spikes/spk-d-verified-loader/recipe.md

key-decisions:
  - "Record verified-loader feasibility as blocked because neither current immutable protocol evidence nor reviewed verifier provenance exists; do not hand-roll or simulate cryptography."
  - "Treat exact-byte digest and one-byte mutation replay as a local integrity observation only, preserve all protocol-sensitive surfaces as blocked, and leave the SPK-C Firefox blocker unchanged."

patterns-established:
  - "Evidence-bound blocker: give each requested primitive its own immutable SRC/CLM row and retain blocked disposition when a reviewed surface is unavailable."
  - "Fixture integrity is not verifier evidence: pin input and mutation digests, record five actual replay samples, and label the scope explicitly."

requirements-completed: [EVID-04]

coverage:
  - id: D1
    description: "SPK-D source-bound exact-byte fixture and blocked feasibility envelope"
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-d-verified-loader --complete"
        status: pass
    human_judgment: false
  - id: D2
    description: "Digest-pinned SPK-D report and immutable impact proposal for ADR review"
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-d-verified-loader/report.md; validate-impact-fragment --root .planning"
        status: pass
    human_judgment: true
    rationale: "Automated validation proves structure and digest links, but human protocol-technical and ADR review must assess missing upstream evidence."

metrics:
  duration: 880s
  completed: 2026-07-24
  tasks: 2
  files: 7
status: complete
---

# Phase 01 Plan 12: Verified-loader feasibility evidence Summary

**Pinned local byte-integrity evidence records that verified-loader feasibility is blocked until immutable manifest/identity sources and reviewed verification provenance exist.**

## Performance

- **Duration:** 14m 40s
- **Started:** 2026-07-24T01:41:16Z
- **Completed:** 2026-07-24T01:55:56Z
- **Tasks:** 2/2
- **Files modified:** 7

## Accomplishments

- Defined a non-production SPK-D envelope with individual immutable `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` bindings for manifest, identity, artifact bytes, signature, blob, aggregate, and verifier provenance.
- Pinned a 29-byte local fixture and its exact one-byte mutation, replayed its integrity assertions five times through `tools/phase1-python`, and retained every unavailable protocol-sensitive surface as `blocked`.
- Preserved environment, measurement, report, and impact-fragment digests for Plan 01-28 to validate and serially consolidate; no loader, cryptographic primitive, package, network operation, or production scaffold was added.

## Task Commits

Each task was committed atomically:

1. **Task 1: Define a pinned verified-loader feasibility fixture** — `8fc23ec` (`feat`)
2. **Task 2: Execute SPK-D and preserve its identity/verification impact fragment** — `3ac0a12` (`feat`)

## Files Created/Modified

- `.planning/spikes/spk-d-verified-loader/metadata.yaml` — completed blocked spike envelope, immutable per-primitive bindings, replay facts, and output digests.
- `.planning/spikes/spk-d-verified-loader/recipe.md` — non-production replay procedure and explicit no-cryptography/no-package boundary.
- `.planning/spikes/spk-d-verified-loader/fixture.json` — exact 29-byte fixture, SHA-256 pins, and one-byte mutation case.
- `.planning/spikes/spk-d-verified-loader/environment.json` — approved toolchain, installed-browser inventory, no-execution flags, and command hashes.
- `.planning/spikes/spk-d-verified-loader/measurements.yaml` — five actual fixture-integrity samples, blocked surfaces, and no-egress result.
- `.planning/spikes/spk-d-verified-loader/report.md` — canonical feasibility report separating upstream fact, observation, inference, recommendation, and uncertainty.
- `.planning/spikes/spk-d-verified-loader/impact-fragment.yaml` — immutable local proposal for `EVID-04`, `ADR-0005`, `ADR-0008`, and Plan 01-28 consolidation.

## Decisions Made

- No current immutable manifest/identity source or reviewed public verifier was available, so every protocol-sensitive primitive remains a source-bound blocker instead of a simulated success or failure.
- The only observed result is deterministic local byte integrity; it must not be promoted to a verified-loader profile, compatibility conclusion, or settled identity behavior.
- SPK-D does not execute a browser and does not alter the existing Plan 01-11 Firefox/Playwright blocker.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical data integrity] Replayed all five recorded fixture samples**
- **Found during:** Task 2: Execute SPK-D and preserve its identity/verification impact fragment
- **Issue:** The completed environment contract retains browser inventory, which requires five raw measurement values; recording repeated values without corresponding executions would misrepresent evidence.
- **Fix:** Ran the approved fixture-integrity assertion five actual times and recorded all exit, mutation, and blocked-surface observations.
- **Files modified:** `.planning/spikes/spk-d-verified-loader/metadata.yaml`, `.planning/spikes/spk-d-verified-loader/measurements.yaml`, `.planning/spikes/spk-d-verified-loader/report.md`
- **Verification:** `validate-spike --complete` and research-root validation pass.
- **Committed in:** `3ac0a12` (part of Task 2 commit)

**2. [Rule 3 - Blocking issue] Supplied the validator's required planning root**
- **Found during:** Task 2: Execute SPK-D and preserve its identity/verification impact fragment
- **Issue:** `validate-impact-fragment` requires `--root`; the initially declared replay command omitted that required argument.
- **Fix:** Updated the SPK-D metadata and recipe to use `validate-impact-fragment --root .planning` and reran the validator.
- **Files modified:** `.planning/spikes/spk-d-verified-loader/metadata.yaml`, `.planning/spikes/spk-d-verified-loader/recipe.md`
- **Verification:** `tools/phase1-python tools/validate-research.py validate-impact-fragment --root .planning .planning/spikes/spk-d-verified-loader/impact-fragment.yaml` passes.
- **Committed in:** `3ac0a12` (part of Task 2 commit)

---

**Total deviations:** 2 auto-fixed (1 Rule 2 data-integrity correction, 1 Rule 3 validation-command correction).
**Impact on plan:** Both corrections preserve reproducibility and truthful evidence without adding scope, packages, cryptography, or production behavior.

## Issues Encountered

- A first local wrapper attempt used zsh's read-only `status` special parameter while capturing the research-root validator exit code. The validator was rerun with a neutral `code` variable and passed. No project artifact was changed by the failed wrapper attempt.

## User Setup Required

None — no external service, account, package, secret, or manual configuration is required.

## Next Phase Readiness

- Plan 01-28 can validate the digest-pinned SPK-D impact fragment before any canonical consolidation.
- SPK-D remains blocked for `EVID-04`, `ADR-0005`, and `ADR-0008` until current immutable manifest/identity evidence and reviewed verifier provenance are collected and human-reviewed.
- Preserve the Plan 01-11 Firefox 152.0.4 / Playwright 1.61.0 blocker; SPK-D made no browser claim and does not resolve it.

## Self-Check: PASSED

All seven SPK-D artifacts and both atomic task commits exist at their recorded paths and hashes.
