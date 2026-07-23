---
phase: 01-research-and-truth-baseline
plan: "01"
subsystem: research-infrastructure
tags: [python, pyyaml, jsonschema, playwright, reproducibility, supply-chain]

requires: []
provides:
  - "Fail-closed Phase 1 execution-convergence preflight with deterministic tests"
  - "Human-approved, pinned research-only Python toolchain and direct installed-browser route"
  - "Checked isolated interpreter wrapper and reproducibility environment manifest"
affects: [01-02, phase-1-spikes, phase-1-validation]

tech-stack:
  added: [PyYAML 6.0.3, jsonschema 4.26.0, Playwright 1.61.0]
  patterns: [blocking supply-chain approval before install, ignored research environment, manifest-checked interpreter wrapper]

key-files:
  created:
    - requirements-phase1-tools.txt
    - .planning/research/toolchain-approval.yaml
    - .planning/spikes/_shared/toolchain-environment.json
    - tools/phase1-python
    - tests/phase1/test_preflight.py
  modified:
    - .gitignore
    - tools/validate-planning.py

key-decisions:
  - "Use direct-installed-browsers: Google Chrome 150.0.7871.124 and Firefox 152.0.4; do not acquire Playwright-managed browser binaries."
  - "Keep the exact three approved top-level Python pins in a Phase 1-only requirements file and record selected artifact SHA-256 values in the approval record."
  - "Require all later Phase 1 verification and replay commands to use tools/phase1-python."

patterns-established:
  - "Research dependencies live only below ignored .research/phase1-tools and never in a production manifest."
  - "The wrapper validates the isolated interpreter version and resolved executable SHA-256 against the committed environment manifest before forwarding arguments."

requirements-completed: [EVID-04, OPER-03]
coverage:
  - id: D1
    description: "Fail-closed execution-convergence preflight rejects missing successful review, HIGH-finding dispositions, and dated authorization."
    requirement: EVID-04
    verification:
      - kind: unit
        ref: "tests/phase1/test_preflight.py via tools/phase1-python -m unittest discover -s tests/phase1"
        status: pass
    human_judgment: false
  - id: D2
    description: "Approved isolated research toolchain records provenance, hashes, direct installed browsers, and a checked interpreter wrapper."
    requirement: OPER-03
    verification:
      - kind: integration
        ref: "tools/phase1-python manifest/package integrity assertions"
        status: pass
      - kind: manual_procedural
        ref: ".planning/research/toolchain-approval.yaml (Phase 1 blocking-human checkpoint)"
        status: pass
    human_judgment: false

duration: 45m
completed: 2026-07-24
status: complete
---

# Phase 01 Plan 01: Research Toolchain Approval and Isolation Summary

**A fail-closed review gate, operator-approved pinned Python tooling, and a manifest-checked isolated interpreter establish reproducible Phase 1 research without browser downloads or production scaffolding.**

## Performance

- **Duration:** 45m
- **Started:** 2026-07-24T20:55:19Z
- **Completed:** 2026-07-24
- **Tasks:** 3/3
- **Files modified:** 7

## Accomplishments

- Added deterministic preflight tests and a fail-closed `--phase-1-execution-preflight` validator that requires a successful reviewer response, complete HIGH-finding dispositions, and dated authorization.
- Recorded the project operator's approval for `PyYAML==6.0.3`, `jsonschema==4.26.0`, and `playwright==1.61.0`, including official registry/artifact URLs, selected SHA-256 values, and license decisions.
- Selected and recorded the final `direct-installed-browsers` route: `/usr/bin/google-chrome` 150.0.7871.124 and `/usr/bin/firefox` 152.0.4; Playwright-managed Chromium and Firefox downloads are explicitly `not-requested`.
- Created the ignored `.research/phase1-tools/` environment, `tools/phase1-python` checked wrapper, and reproducibility manifest with OS, Python, package, Git, Node/npm, browser, provenance, and five-sample median policy data.

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement the fail-closed Phase 1 execution-convergence preflight** - `b2886a7` (test), `a69cb02` (feat)
2. **Task 2: Approve the Phase 1 research-only package and browser toolchain** - `a5724e6` (docs)
3. **Task 3: Install the approved research toolchain, pin its wrapper, and capture the reproducibility baseline** - `85d855e` (feat)

## Files Created/Modified

- `tools/validate-planning.py` - Adds the committed-review convergence preflight command and stable diagnostics.
- `tests/phase1/test_preflight.py` - Proves preflight rejection and success cases with deterministic fixtures.
- `.planning/research/toolchain-approval.yaml` - Stores final operator approvals, release artifacts, hashes, licenses, browser route, and no-download decisions.
- `requirements-phase1-tools.txt` - Contains only the three approved Phase 1 research-tool pins.
- `.planning/spikes/_shared/toolchain-environment.json` - Captures installed distribution inventory, executable provenance, and reproducibility baseline.
- `tools/phase1-python` - Refuses ambient interpreters and verifies the approved interpreter version and SHA-256 before execution.
- `.gitignore` - Ignores the Phase 1 research environment and generated Python bytecode while preserving the archive rule.

## Decisions Made

- The project operator's final checkpoint decision is authoritative: use direct-installed Chrome and Firefox, not managed Playwright browser binaries. No `playwright install` command was run.
- Root package artifacts are pinned and their selected wheel SHA-256 values are recorded before installation. The environment manifest additionally records the resolver's actual installed distributions and artifact hashes.
- Phase 1 replay and verification must call `tools/phase1-python`, which binds every invocation to the recorded isolated interpreter rather than an ambient Python installation.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed inline package hashes that inadvertently enabled pip's global hash-required mode**
- **Found during:** Task 3 (approved isolated toolchain installation)
- **Issue:** Supplying root-package `--hash` values in the requirements file caused pip to require pins and hashes for every resolver dependency, preventing installation even though the approved three top-level pins were available.
- **Fix:** Retained the exact selected artifact SHA-256 values in the committed approval record, removed only the inline pip hash tokens, and captured every resolved distribution's artifact URL and SHA-256 in the environment manifest.
- **Files modified:** `requirements-phase1-tools.txt`, `.planning/spikes/_shared/toolchain-environment.json`
- **Verification:** The isolated environment installed the approved pins; the manifest integrity assertions and full Phase 1 test suite passed.
- **Committed in:** `85d855e` (Task 3)

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** The correction preserved the approved top-level pins, pre-install root artifact evidence, isolated boundary, and complete post-install provenance without adding a package or downloading a browser binary.

## Issues Encountered

- An exploratory package-version assertion used the absent `playwright.__version__` attribute. Replacing it with `importlib.metadata.version()` confirmed the installed distribution version without changing project artifacts.

## User Setup Required

None - no external service configuration is required. The approved system browser executables must remain available at the recorded paths for browser spike replay.

## Next Phase Readiness

- Plan 01-02 can use `tools/phase1-python` for its YAML, JSON Schema, and browser-dependent research tooling.
- The reproducibility baseline is specific to the recorded Fedora/Linux host and installed browser executables; a changed interpreter, browser binary, or package artifact requires a refreshed approval/environment record before dependent evidence is treated as comparable.

## Self-Check: PASSED

All seven plan artifacts exist; Task 1 through Task 3 commits (`b2886a7`, `a69cb02`, `a5724e6`, `85d855e`) resolve; the tracked implementation files contain no stub patterns; and `git diff --check` passed.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
