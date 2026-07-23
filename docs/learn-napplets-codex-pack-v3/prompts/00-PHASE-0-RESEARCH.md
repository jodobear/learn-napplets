# Codex Prompt — Phase 0: Research and Truth Baseline

Work in the new independent **Learn Napplets** repository.

Read and obey:

- `AGENTS.md`;
- `CODEX-MASTER-PROMPT.md`;
- `docs/04-RESEARCH-PLAN.md`;
- the other project documents as referenced;
- templates under `templates/`.

Execute only Phase 0. Do not scaffold the production course.

## Git orientation

Run:

```bash
git status
git branch --show-current
git log --oneline -5
```

If the repository has no commits, commit the supplied documentation baseline first. Then create a descriptive Phase 0 branch.

## Current-source requirement

Treat upstream repositories as read-only.

Fetch current source from:

- the living NIP-5D PR/file and adopted NIP material;
- `napplet/naps` registry, projection, current core proposals, archetypes, conventions, governance, issues, PRs, and relevant discussions;
- `napplet/web` public packages, conformance, examples, tooling, issues, PRs, and relevant branches;
- credible current runtime implementations;
- Learn FIPS and selected comparison learning products.

Record exact commit SHAs, paths, immutable links, content digests, and observed times.

If current sources cannot be fetched, record a blocker and stop protocol conclusions. Do not substitute model memory.

## Scope discipline

Inventory the entire ecosystem by metadata, but deep-read only sources that:

- affect the MVP;
- are part of a known drift item;
- are used by the first real lab;
- materially affect a technical ADR;
- illustrate an important boundary.

Do not deep-read every active branch merely because it exists.

## Required work

Complete all Tier 1 and Tier 2 work and every mandatory spike in `docs/04-RESEARCH-PLAN.md`.

Pay particular attention to:

- current domain availability/bootstrap behavior;
- current manifest kinds, artifact, and exact identity;
- `dTag` behavior for manifest kinds without a `d` tag;
- archetype/convention metadata under the current manifest model;
- NAP-INTENT handler identity/catalog assumptions;
- browser network egress and public-site CSP separation;
- package/conformance drift;
- host versus guest build boundaries.

## Delivery-mode research

Evaluate:

1. public learning site;
2. real lab napplets hosted by a teaching host;
3. portable Workbench napplet;
4. selected/full-course napplet.

Build disposable spikes only. Do not treat a privately nested frame inside a course napplet as proof of runtime composition.

Return a delivery recommendation and ADR 0007 outcome.

## Required outputs

Create the complete `.planning/` artifact set from the research plan, including:

- source registry;
- claim inventory;
- thirteen lesson research packets;
- domain, archetype/convention, and public example-napplet catalogs;
- compatibility matrix;
- terminology map;
- drift/open-question registers;
- security/egress findings;
- current-work snapshot;
- package/runtime maps;
- pedagogy and audience analysis;
- teaching-scope decision;
- all ADR recommendations.

Every spike report includes hypothesis, sources, implementation, measurements, result, recommendation, uncertainty, and disposition.

## Verification and finish

Run all checks available in the independent repository.

Update `.planning/STATUS.md`.

Commit Phase 0 atomically. Push/open a research PR when remote access and credentials exist; otherwise leave a clean PR-ready branch and report.

Stop after Phase 0.
