---
phase: 01-research-and-truth-baseline
plan: 11
subsystem: research-spike
tags: [playwright-1.61.0, chromium, firefox, iframe-sandbox, postmessage, provenance]
requires:
  - phase: 01-07
    provides: blocked teaching scope and source/claim baseline
  - phase: 01-20
    provides: approved isolated Phase 1 toolchain
  - phase: 01-26
    provides: teaching-host scope constraints
provides:
  - isolated SPK-C iframe fixture and direct-installed browser replay runner
  - provenance-bound browser evidence with an immutable impact fragment
  - truthful cross-browser blocker for ADR-0005 review
affects: [01-16, 01-22, 01-28, phase-02, phase-05]
tech-stack:
  added: [Playwright 1.61.0 runner usage only; no packages installed]
  patterns: [sandboxed srcdoc guest, bounded envelope capture, source/claim provenance validation, blocked browser evidence]
key-files:
  created:
    - .planning/spikes/spk-c-boundary-harness/fixture.html
    - .planning/spikes/spk-c-boundary-harness/runner.py
    - .planning/spikes/spk-c-boundary-harness/impact-fragment.yaml
  modified:
    - .planning/research/schemas/spike.schema.json
    - .planning/research/schemas/spike-impact-fragment.schema.json
    - tools/validate-research.py
key-decisions:
  - "SPK-C remains blocked overall: Chromium passed five isolated samples, but Firefox 152.0.4 exited before approved Playwright 1.61.0 attached."
  - "Browser observations remain fixture-specific; all upstream-sensitive source bindings are explicitly blocked project-policy inputs."
patterns-established:
  - "Direct-installed browser runner: use tools/phase1-python with Playwright 1.61.0 and never request managed browser downloads."
  - "Impact hand-off: bind report, metadata, measurements, source registry, proposed open question, drift record, and phase impacts by SHA-256."
requirements-completed: []
coverage:
  - id: D1
    description: "Safe local sandboxed iframe contract with bounded postMessage envelopes and provenance-bound source bindings"
    requirement: EVID-04
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-c-boundary-harness --contract"
        status: pass
    human_judgment: false
  - id: D2
    description: "Cross-browser SPK-C boundary evidence for the first teaching-host profile"
    requirement: EVID-04
    verification:
      - kind: automated_ui
        ref: "tools/phase1-python .planning/spikes/spk-c-boundary-harness/runner.py"
        status: fail
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-c-boundary-harness --complete"
        status: pass
    human_judgment: true
    rationale: "Firefox did not reach fixture execution, and a human must review the blocked direct-installed browser surface before any host-profile decision."
duration: 15m
completed: 2026-07-24
status: complete
---

# Phase 01 Plan 11: Sandboxed Browser Boundary Harness Summary

**A sandboxed local iframe fixture recorded five successful Chromium boundary exchanges and a reproducible Firefox/Playwright launch blocker without asserting upstream protocol behavior.**

## Performance

- **Duration:** 15m
- **Started:** 2026-07-24T01:23:25Z
- **Completed:** 2026-07-24T01:38:22Z
- **Tasks:** 2/2 completed
- **Files modified:** 11

## Accomplishments

- Defined SPK-C's non-production `sandbox="allow-scripts"` iframe contract, fixed envelope, deterministic local service, declared-domain removal path, and separately pinned installed browser surfaces.
- Replayed five clean Chromium contexts through approved Playwright 1.61.0; each observed pre-script injection, `MessageEvent.source` mapping, deterministic success, and deterministic declared-domain-missing response.
- Preserved the Firefox launch failure as a blocked outcome, including the environment, raw values, report, proposed open question/drift record, and SHA-bound impact fragment for Plan 01-28.

## Task Commits

Each task was committed atomically:

1. **Task 1: Specify the sandboxed real-browser boundary experiment** - `f3a8941` (feat)
2. **Task 2: Run SPK-C in clean browser contexts and preserve its evidence-impact fragment** - `07584ca` (feat)

## Files Created/Modified

- `.planning/spikes/spk-c-boundary-harness/fixture.html` - Local sandboxed guest fixture with bounded postMessage scenarios.
- `.planning/spikes/spk-c-boundary-harness/runner.py` - Direct-installed browser runner using approved Playwright 1.61.0 only.
- `.planning/spikes/spk-c-boundary-harness/{environment.json,measurements.yaml,report.md}` - Reproducible environment and truthful browser evidence.
- `.planning/spikes/spk-c-boundary-harness/impact-fragment.yaml` - Immutable proposed compatibility, drift, open-question, and impact hand-off.
- `.planning/research/schemas/{spike.schema.json,spike-impact-fragment.schema.json}` - Contract support for provenance-rich bindings and SPK-C fragment fields.
- `tools/validate-research.py` - Semantic validation of enriched source/claim immutable bindings.

## Decisions Made

- SPK-C is **blocked**, not passed: Chrome evidence is reproducible, but no Firefox fixture behavior was observed after the installed Firefox process exited during Playwright launch.
- The static/deferred fallback remains required for the prospective teaching-host profile; neither the fixture nor any upstream protocol behavior is selected.
- `SPK-C-IMPACT-001` retains the Firefox execution issue for serial canonical consolidation rather than modifying canonical compatibility, drift, or open-question records directly.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Extended strict evidence schemas for the plan-required provenance fields**
- **Found during:** Task 1 and Task 2
- **Issue:** The strict spike and impact-fragment schemas could not represent the task-required source/claim immutable binding, separate browser execution surfaces, fragment ID, typed proposed impact lists, or measurement path/digest.
- **Fix:** Added backwards-compatible optional fields and SPK-C-specific required checks; added semantic validation that enriched bindings match source-registry pins and blocked claims.
- **Files modified:** `.planning/research/schemas/spike.schema.json`, `.planning/research/schemas/spike-impact-fragment.schema.json`, `tools/validate-research.py`
- **Verification:** Contract, complete-spike, impact-fragment, common-research, and planning validation passed.
- **Committed in:** `f3a8941`, `07584ca`

**2. [Rule 1 - Bug] Corrected the generated guest script terminator**
- **Found during:** Task 2 browser replay
- **Issue:** The generated `srcdoc` retained an extra slash escape, preventing Chromium from receiving its first boundary message and producing timeouts.
- **Fix:** Emitted the inner `</script>` terminator correctly while keeping the outer fixture parser safe.
- **Files modified:** `.planning/spikes/spk-c-boundary-harness/fixture.html`
- **Verification:** All five Chromium samples then passed the declared injection, source mapping, and two-envelope assertions.
- **Committed in:** `07584ca`

**3. [Rule 2 - Missing Critical] Added a checked-in isolated replay runner**
- **Found during:** Task 2 evidence capture
- **Issue:** A disposable browser command without a committed runner would not preserve the required clean-context replay mechanics or ensure use of only approved installed browsers.
- **Fix:** Added a non-production `runner.py` that verifies Playwright 1.61.0, uses only the two pinned installed executables, creates fresh contexts, captures bounded results, and exits nonzero for blocked or failed evidence.
- **Files modified:** `.planning/spikes/spk-c-boundary-harness/runner.py`, `.planning/spikes/spk-c-boundary-harness/recipe.md`, `.planning/spikes/spk-c-boundary-harness/metadata.yaml`
- **Verification:** Runner produced five Chromium passes and five faithfully recorded Firefox launch blocks without downloads or external state.
- **Committed in:** `07584ca`

---

**Total deviations:** 3 auto-fixed (1 Rule 1 bug, 1 Rule 2 missing critical functionality, 1 Rule 3 blocking issue)
**Impact on plan:** All changes are constrained to the disposable SPK-C evidence path and validation contracts; no production scaffold, secret, external state, or browser download was introduced.

## Issues Encountered

- The approved direct-installed Firefox 152.0.4 executable exited with code 0 before Playwright 1.61.0 attached. The runner therefore exited nonzero, SPK-C was recorded as blocked, and no positive cross-browser claim was made. The open defect is registered in `.planning/WINDOWS.md`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 01-28 can validate and consolidate `SPK-C-IMPACT-001` as a blocked local evidence hand-off.
- Plans 01-16, 01-22, and later host-profile work must preserve the Firefox execution blocker and static/deferred fallback.
- A human must decide how to obtain an approved, reproducible Firefox execution surface before any cross-browser host-profile conclusion or ADR-0005 acceptance.

---
## Self-Check: PASSED

- Confirmed all SPK-C fixture, runner, evidence, fragment, and summary files exist.
- Confirmed task commits `f3a8941` and `07584ca` exist in git history.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
