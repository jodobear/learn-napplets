---
phase: 01-research-and-truth-baseline
plan: 19
subsystem: research-governance
tags: [spike, deployment, publication, local-only, sha256, evidence]
requires:
  - phase: 01-07
    provides: delivery-mode recommendation and blocked compatibility baseline
  - phase: 01-20
    provides: Phase 1 source and claim policy records
  - phase: 01-26
    provides: isolated Phase 1 Python toolchain
provides:
  - Explicit local-only deployment/publication evidence gate for SPK-K
  - Digest-pinned local artifact assembly, inspection, and rollback replay
  - Scoped blocker for external deployment/publication evidence
  - Auditable named-sandbox authorization contract for any future external probe
affects: [ADR-0003, EVID-04, delivery, portability, release]
tech-stack:
  added: [standard-library Python local fixture runner]
  patterns: [local-only artifact replay, explicit external-write authorization, digest-pinned rollback evidence]
key-files:
  created:
    - .planning/spikes/spk-k-deployment/metadata.yaml
    - .planning/spikes/spk-k-deployment/recipe.md
    - .planning/spikes/spk-k-deployment/fixture.md
    - .planning/spikes/spk-k-deployment/runner.py
    - .planning/spikes/spk-k-deployment/environment.json
    - .planning/spikes/spk-k-deployment/measurements.yaml
    - .planning/spikes/spk-k-deployment/report.md
  modified:
    - .planning/research/schemas/spike.schema.json
key-decisions:
  - "Task 2 selected local-only on 2026-07-24; external deployment/publication remains blocked."
  - "Local static inspection replaces a listener or provider preview; no network command or external target is used."
  - "Any future sandbox probe requires a named disposable target plus exact command, cleanup, retention, owner, security/release sign-offs, credential handling, and result-digest policy."
patterns-established:
  - "External write gate: not-authorized/local-only/sandbox-probe states are schema-validated and sandbox probes require complete auditable authorization fields."
  - "Local artifact evidence: generate under the spike .experiment directory, record payload/manifest digests, then verify and delete the output."
requirements-completed: [EVID-04]
coverage:
  - id: D1
    description: "SPK-K local artifact contract and complete local-only evidence record"
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-k-deployment --complete"
        status: pass
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-k-deployment/report.md"
        status: pass
    human_judgment: false
  - id: D2
    description: "Planning boundary remains valid after local-only evidence recording"
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-planning.py"
        status: pass
    human_judgment: false
duration: 13m
completed: 2026-07-24
status: complete
---

# Phase 01 Plan 19: Local Deployment Evidence Summary

**Digest-pinned local static artifact replay with explicit local-only deployment blocking and no external target, credential, command, publication, or release.**

## Performance

- **Duration:** 13m
- **Started:** 2026-07-24T09:50:30Z
- **Completed:** 2026-07-24T10:03:09Z
- **Tasks:** 3/3
- **Files modified:** 8

## Accomplishments

- Defined SPK-K as a non-production local artifact experiment with three separate, digest-pinned output categories and a deterministic `SPK-K-BLOCKED-EXTERNAL-AUTHORIZATION-MISSING` external outcome.
- Recorded the dated Task 2 `local-only` decision, preventing account/credential access, target lookup, remote configuration, deployment, publication, external commands, and external writes.
- Replayed static local artifact assembly, digest verification, isolation inspection, and rollback using `tools/phase1-python`; all generated files were removed after verification.
- Produced a proposed, impact-scoped ADR-0003 evidence record that does not claim external hosting, public reachability, portable compatibility, or production release.

## Task Commits

Each task was committed atomically:

1. **Task 1: Define local artifact and optional external deployment evidence** — `cd84c42` (`feat`)
2. **Task 2: Decide whether SPK-K may perform an external sandbox deployment probe** — `423ddcc` (`docs`)
3. **Task 3: Execute local SPK-K evidence and any authorized sandbox probe** — `fbebc97` (`feat`)

## Files Created/Modified

- `.planning/spikes/spk-k-deployment/metadata.yaml` — complete SPK-K envelope, local-only decision, digests, replay result, and scoped blocker.
- `.planning/spikes/spk-k-deployment/recipe.md` — local-only artifact rules, exact replay commands, and named-sandbox authorization contract.
- `.planning/spikes/spk-k-deployment/fixture.md` — bounded static payload and source/package baseline declaration.
- `.planning/spikes/spk-k-deployment/runner.py` — standard-library local artifact assembly, digest verification, containment, and rollback runner.
- `.planning/spikes/spk-k-deployment/environment.json` — isolated local toolchain and no-network/no-external-command manifest.
- `.planning/spikes/spk-k-deployment/measurements.yaml` — artifact identities, five-value validation-compatible measurements, zero external operations, and replay digest.
- `.planning/spikes/spk-k-deployment/report.md` — ADR-0003 local-only evidence report with canonical research headings.
- `.planning/research/schemas/spike.schema.json` — schema-validated external probe authorization states and audit fields.

## Decisions Made

- Task 2 selected `local-only` on 2026-07-24. This preserves local evidence and records external deployment/publication as scoped blocked evidence.
- No named target was supplied or invented. A sandbox probe remains ineligible until a future explicit authorization supplies all required target, command, cleanup, retention, ownership, security/release, credential, and digest controls.
- The replay uses static inspection rather than an HTTP listener, so the local test establishes artifact identity and containment only.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Made external-action authorization machine-validatable**
- **Found during:** Task 1 and Task 2
- **Issue:** The canonical spike schema rejected an authorization field due to `additionalProperties: false`; it therefore could not validate the plan-required default-deny state or the audit controls required for a future sandbox exception.
- **Fix:** Added a backward-compatible `externalProbeAuthorization` schema contract, including enforced decision date/approver for `local-only` and full named-target controls for `sandbox-probe`.
- **Files modified:** `.planning/research/schemas/spike.schema.json`, `.planning/spikes/spk-k-deployment/metadata.yaml`
- **Verification:** `validate-spike --contract` and `validate-spike --complete` passed.
- **Committed in:** `cd84c42`, `423ddcc`

**2. [Rule 2 - Missing Critical] Added a deterministic local replay runner**
- **Found during:** Task 3
- **Issue:** The planned local artifact measurement needed a committed exact command and a safe path-containment/rollback implementation; an inline trial was not a durable replay artifact.
- **Fix:** Added a standard-library `runner.py` constrained to the spike `.experiment` directory. It performs no network or provider operation, verifies digests, and removes only its own generated local artifacts.
- **Files modified:** `.planning/spikes/spk-k-deployment/runner.py`, `.planning/spikes/spk-k-deployment/recipe.md`, `.planning/spikes/spk-k-deployment/metadata.yaml`
- **Verification:** Assembly and rollback replay passed; the output directory was absent after rollback; complete spike, report, and planning validators passed.
- **Committed in:** `fbebc97`

---

**Total deviations:** 2 auto-fixed (2 Rule 2 missing-critical fixes).
**Impact on plan:** Both fixes enforce the plan's default-deny external-action boundary and deterministic replay requirements without adding a provider, package, credential, network listener, or external command.

## Issues Encountered

- The first local inline assembly invocation had a Python quoting syntax error before it performed any write. It was replaced by the committed deterministic runner, then assembly and rollback were replayed successfully.
- `tools/validate-planning.py` passed with its pre-existing expected `PENDING001` Phase 1 warning. No unrelated dirty planning files were staged or modified by this plan.

## Known Stubs

| Stub | File | Line | Reason and resolution boundary |
| --- | --- | --- | --- |
| `lab-artifact-placeholder` static payload | `.planning/spikes/spk-k-deployment/fixture.md` | 33 | Intentional Phase 1 safe fallback; it explicitly prevents a claim that a teaching host/lab artifact was built or deployed. Resolve only after immutable evidence and ADR approval. |
| `portable-output-placeholder` static payload | `.planning/spikes/spk-k-deployment/fixture.md` | 36 | Intentional Phase 1 safe fallback; it explicitly prevents a portability claim while ADR-0007 remains unresolved. Resolve only in separately authorized downstream work. |

## Next Phase Readiness

- ADR-0003 has local assembly, digest, isolation, and rollback evidence, but external deployment/publication remains impact-scoped blocked.
- Future external evidence requires a new explicit named disposable-sandbox authorization; local-only does not authorize a target, account, credential use, provider command, or release.
- The intentional blocked placeholders preserve the Phase 1 boundary and must not be promoted to a real lab or portable artifact without later evidence and approvals.

## Self-Check: PASSED

- Confirmed the seven SPK-K artifact files and this summary exist on disk.
- Confirmed Task 1 `cd84c42`, Task 2 `423ddcc`, and Task 3 `fbebc97` exist as commit objects.
- Confirmed the generated `.experiment/local-artifacts` directory was removed after rollback.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
