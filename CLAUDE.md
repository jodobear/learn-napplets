# Learn Napplets — Project Instructions

## Canonical state

- `.planning/STATE.md` is sole live project status source.
- `.planning/PROJECT.md`, `REQUIREMENTS.md`, and `ROADMAP.md` define current scope.
- `docs/learn-napplets-codex-pack-v3/` is preserved source/archive; do not edit it during normal project work.
- If canonical planning conflicts with current revision-pinned upstream protocol evidence, stop and record conflict. Never silently override upstream facts.

## Phase gate

Current GSD Phase 1 maps to source-pack Phase 0 (Research and Truth Baseline).

Production frameworks, trusted-host/runtime code, guest execution, package integration, live-service dependencies, and portable artifacts remain blocked before:
1. Phase 1 research outputs and applicable safety gates pass;
2. required ADR recommendations have evidence and approval;
3. Phase 2 product/content contract passes.

Owner-authorized exception: after Plans 01-46 and 01-47 pass, Plan 01-48 may create a dependency-free static informational/learning site from structured, evidence-labeled records. This exception does not authorize a framework or package manager, host/guest runtime, signing or wallet authority, live relays, package conformance, deployment/publication, ADR acceptance, or Phase 2 transition.

Disposable spikes must be isolated and clearly marked non-production.

## Evidence

Protocol-sensitive claims require immutable source revision, path/locator, digest, retrieval date, authority/evidence/maturity classification, uncertainty, affected requirements/phases, and refresh trigger.

Separate:
- upstream fact;
- proposal/draft;
- observed implementation behavior;
- project policy;
- inference.

## GSD workflow

Use GSD lifecycle:

```text
discuss → plan → plan review/convergence → execute → review → verify/UAT → transition
```

- Prefer `/gsd-progress --next` for routing.
- `workflow.auto_advance` remains off by default.
- Never use `--force` routinely.
- Automation stops at ADR acceptance, external actions, human UAT, failed verification, security exceptions/blockers, phase transition approval, and release.
- Use gap plans after verification failures instead of replanning whole phase.
- The original Phase 1 research plan received deep review convergence. The owner-authorized 01-46 through 01-48 recovery set receives exactly one focused plan-checker pass; do not restart external plan-binding or terminal-review choreography.

## Product boundaries

- Trusted host owns sensitive/repetitive authority; guest napplets receive only declared mediated capabilities.
- Required learning paths are deterministic and cannot depend on live external systems.
- Essential interactions need keyboard, reduced-motion, transcript/state inspection, reset/replay, and static equivalents.
- Human and LLM outputs derive essential facts from common structured sources.
- Graphify is navigation/indexing, never evidence authority.
