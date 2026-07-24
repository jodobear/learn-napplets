---
phase: 01-research-and-truth-baseline
plan: 18
subsystem: research-spike
tags: [code-editing, codemirror, accessibility, browser-isolation, supply-chain]
requires:
  - phase: 01-07
    provides: package and runtime candidate catalogs
  - phase: 01-20
    provides: approved isolated Phase 1 toolchain
  - phase: 01-26
    provides: bounded teaching scope
provides:
  - least-authority editing comparison with five Chromium replays
  - dated editor package decisions and isolated CodeMirror measurement
  - explicit Firefox and CodeJar blockers for ADR-0009 review
affects: [ADR-0009, EVID-04, phase-05-teaching-host]
tech-stack:
  added: []
  patterns: [exact-variant editing, no learner-code execution, local loopback package harness]
key-files:
  created:
    - .planning/spikes/spk-j-code-editing/fixture.html
    - .planning/spikes/spk-j-code-editing/runner.py
    - .planning/spikes/spk-j-code-editing/environment.json
    - .planning/spikes/spk-j-code-editing/measurements.yaml
    - .planning/spikes/spk-j-code-editing/report.md
  modified:
    - .planning/spikes/spk-j-code-editing/metadata.yaml
key-decisions:
  - Fixed tested variants are the proposed default; a controlled native textarea is justified only for the declared small edit.
  - CodeMirror is not selected despite passing bounded Chromium checks; CodeJar remains blocked and Firefox evidence is unavailable.
patterns-established:
  - Learner-editable text is compared to fixed constants and rendered as text; it is never evaluated in trusted context.
  - Package-editor measurement uses exact approved releases in ignored spike-local storage and fixed runner-owned input only.
requirements-completed: []
coverage:
  - id: D1
    description: Bounded native and package editing accessibility/isolation evidence
    requirement: EVID-04
    verification:
      - kind: automated_ui
        ref: tools/phase1-python .planning/spikes/spk-j-code-editing/runner.py --fixture .planning/spikes/spk-j-code-editing/fixture.html --experiment .planning/spikes/spk-j-code-editing/.experiment/codemirror-6-core --out /tmp/spk-j-code-editing
        status: partial
      - kind: integration
        ref: tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-j-code-editing --complete
        status: pass
    human_judgment: true
    rationale: Firefox did not attach, and ADR-0009 remains blocked for cross-browser acceptance.
duration: 20m
completed: 2026-07-24
status: complete
---

# Phase 01 Plan 18: Least-Authority Code-Editing Evidence Summary

SPK-J now compares fixed variants, controlled native editing, a native inspection shell, blocked CodeJar, and an approved isolated CodeMirror direct set without executing arbitrary learner code.

## Performance

- **Duration:** 20m
- **Started:** 2026-07-24T14:58:21+05:30
- **Completed:** 2026-07-24T15:18:45+05:30
- **Tasks:** 3/3
- **Files modified:** 8

## Accomplishments

- Defined a synthetic exact-match editing fixture with keyboard controls, semantic status, static fallback, deterministic reset, hostile-input containment, and a trusted-host sentinel.
- Recorded the dated package gate: CodeJar `4.3.0` blocked; four exact CodeMirror packages approved only for this ignored, non-production experiment with an explicit transitive-lock-review exception.
- Replayed five clean Chromium samples. All 24 declared checks passed for native and fixed-document CodeMirror paths; Firefox exited before Playwright attachment and remains blocked.
- Measured native median load at `26.530 ms`, CodeMirror median load at `74.381 ms`, and the resolved local CodeMirror tree at `5,174,566` bytes.

## Task Commits

1. **Task 1: Define least-authority editing candidates and isolated fixture** — `41e2863`
2. **Task 2: Approve or block exact SPK-J editor dependencies** — `0a2fc0d`
3. **Task 3: Execute SPK-J and report the smallest justified editing scope** — `6a8917e`

## Decisions Made

- Propose fixed tested variants as the default for the bounded objective.
- Use a controlled native textarea only when the learner must make the one declared textual change.
- Do not select CodeMirror as the default: measured need is absent, its local tree is much larger, Firefox evidence is missing, and the dependency-lock exception was experiment-only.
- Keep CodeJar blocked because its registry release and immutable source version identities conflict.

## Verification

Passed:

- `tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-j-code-editing --complete`
- `tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-j-code-editing/report.md`
- `tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/spk-j-research-validation.md`
- `tools/phase1-python tools/validate-planning.py` with the expected Phase 1 pending warning only

Chromium passed five samples. Firefox remained blocked before context attachment; no browser download or configuration workaround was used.

## Deviations from Plan

1. **[Rule 1 - Bug] Corrected browser-runner evaluation parameters.** The first harness run referenced page-level `arguments`; the runner was changed to pass an explicit evaluation parameter, then all five Chromium samples were rerun.
2. **[Rule 2 - Missing Critical] Added a checked-in isolated replay runner.** Task 3 required reproducible browser, package, hostile-input, fallback, screenshot, and sentinel measurements.
3. **[Execution Recovery] Main orchestrator completed the canonical report and metadata.** The executor environment rejected writing the required report artifact, so validated uncommitted measurements were completed without rerunning package acquisition or altering the evidence.

## Security and Boundary Result

No learner-controlled text was evaluated, compiled, imported, or passed to CodeMirror. The package harness received only fixed runner-owned input over loopback. No production route, framework scaffold, root package manifest, secret, upload, external request, telemetry, or persistent state was created.

## Next Phase Readiness

- ADR-0009 receives proposed least-authority evidence only; it remains blocked for cross-browser acceptance.
- Phase 05 must preserve fixed/static paths, keyboard/status/reset behavior, and trusted-host ownership.
- Any arbitrary learner-code execution path requires a separate sandbox design and security review.

## Self-Check: PASSED

All SPK-J contract, fixture, runner, environment, measurement, report, and summary files exist. Task commits `41e2863`, `0a2fc0d`, and `6a8917e` exist in repository history.
