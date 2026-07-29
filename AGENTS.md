# Learn Napplets — Agent Instructions

## Canonical project state

- `.planning/STATE.md` is sole live project-status source.
- `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, and `.planning/ROADMAP.md` define current scope.
- `docs/learn-napplets-codex-pack-v3/` is preserved source/archive. Do not edit it during normal project work.
- Graph artifacts are navigation aids, never evidence authority.

## Phase gates

Current GSD Phase 1 is Research and Truth Baseline. Do not create production app or framework scaffolding before Phase 1 evidence/spikes and Phase 2 product/content contract pass their human gates.

Trusted host owns sensitive or repetitive authority. Guest napplets receive only declared mediated capabilities. Required learning paths must stay deterministic and cannot depend on live external systems.

## Evidence rules

Separate upstream fact, proposal, observed implementation behavior, project policy, and inference. Protocol-sensitive claims require immutable revision/path/digest evidence plus dated authority, maturity, uncertainty, impact, and refresh metadata.

## Code Review Rules

- Review repository evidence, not plan prose alone. Cite concrete `path:line` evidence and mechanism.
- Phase 1 execution remains blocked until exact-commit plan review records `HIGH=0` and `ACTIONABLE=0`.
- Recompute and verify every active Phase 1 plan SHA-256, total bytes, and lexical `basename + NUL + bytes + NUL` aggregate when review binding changes.
- Verify six mandatory source inputs are regular Git blobs from same reviewed commit and byte-match checkout: `.planning/PROJECT.md`, Phase 1 `01-CONTEXT.md`, and four `upstream-refresh-*-2026-07-28.md` reports.
- Treat elapsed calendar age as audit context only. Unchanged exact bindings expire only through changed plan/source bytes, changed reviewed commit, or explicit supersession.
- Probe-suite reruns are allowed. Require exactly one canonical evidence row per fixed probe ID from designated direct invocation, with all discovery/rerun attempts retained separately.
- Flag correctness, security, evidence-integrity, dependency, ownership, missing-input, testability, and phase-goal defects. Mark severity and whether plan changes are actionable.
- Never accept ADRs, residual risk, external actions, phase transitions, or releases through automated review.
