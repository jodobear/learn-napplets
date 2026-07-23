# Learn Napplets — Codex Build Pack

**Version:** 3  
**Prepared:** 2026-07-23  
**Project type:** independent learning product and repository

This pack specifies **Learn Napplets**: an interactive course, architecture laboratory, example-napplet collection, and structured ecosystem map for developers and LLMs.

The project is independent from `napplet/web`, `napplet/naps`, NIP repositories, runtimes, and Learn FIPS. Those projects are read-only upstream sources or optional released dependencies.

## Product outputs

One repository may produce several explicitly different artifacts:

| Artifact | Runtime role | v1 status |
|---|---|---:|
| **Public learning website** | Ordinary web application and declared teaching host | Required |
| **Real lab napplets** | Focused untrusted applications used by lessons | At least three required |
| **Workbench napplet** | Portable untrusted architecture/tooling application | ADR-gated |
| **Full-course napplet** | Portable untrusted course build using the current napplet artifact contract | ADR-gated |

The host and guest roles must remain separate:

- The **public-site build** may create sandboxed lab napplets, inject deterministic capabilities, record envelopes, and run selected conformance checks.
- A **napplet build** is an untrusted guest. It may present simulations or ask the external runtime to open sibling napplets through the current composition mechanism. It must not impersonate a shell or describe privately nested frames as runtime composition.

Prefer separate compile-time entry points and dependency boundaries over runtime authority detection.

## Delivery cut lines

### Content MVP

- homepage;
- why napplets;
- sandbox boundary;
- one real request journey;
- capabilities;
- glossary and source/status pages;
- one real note-tool napplet hosted by the teaching host, preferably a composer when its selected current domain is usable.

### v1 minimum

- the complete thirteen-lesson course;
- the public site and declared teaching-host profiles;
- at least three real lab napplets: one composer and two interchangeable viewers;
- core architecture, capability, identity, composition, and conformance labs;
- source provenance and drift pages;
- page Markdown, structured knowledge JSON, `llms.txt`, and `llms-full.txt`.

A Workbench or full-course napplet must not block v1 unless Phase 0 explicitly recommends it.

## Document precedence

When instructions conflict, use this order:

1. `AGENTS.md`;
2. accepted ADRs and current Phase 0 research outputs;
3. canonical project documents under `docs/`;
4. the currently authorized phase prompt;
5. templates and examples.

A project document never overrides an upstream protocol source. Flag conflicts rather than silently choosing.

## Start here

1. Create an empty repository, provisionally `learn-napplets`.
2. Extract the **contents** of this pack into the repository root.
3. Run `python scripts/validate-pack.py`.
4. Initialize Git and commit the documentation baseline.
5. Give Codex only [`prompts/00-PHASE-0-RESEARCH.md`](prompts/00-PHASE-0-RESEARCH.md).
6. Review the Phase 0 research and ADR recommendations.
7. Continue one authorized phase at a time.

Long-lived rules:

- [`AGENTS.md`](AGENTS.md)
- [`CODEX-MASTER-PROMPT.md`](CODEX-MASTER-PROMPT.md)
- [`AUDIT-REPORT.md`](AUDIT-REPORT.md)

## Document map

| Document | Purpose |
|---|---|
| [`docs/01-PROJECT-CHARTER.md`](docs/01-PROJECT-CHARTER.md) | Mission, audiences, outcomes, non-goals, and v1 cut line |
| [`docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`](docs/02-UPSTREAM-TRUTH-AND-DRIFT.md) | Source authority, claim provenance, drift, and freshness |
| [`docs/03-DELIVERY-MODES.md`](docs/03-DELIVERY-MODES.md) | Website, teaching host, lab napplets, Workbench, and course napplet |
| [`docs/04-RESEARCH-PLAN.md`](docs/04-RESEARCH-PLAN.md) | Prioritized Phase 0 work and feasibility gates |
| [`docs/05-CURRICULUM-AND-EXPERIENCE.md`](docs/05-CURRICULUM-AND-EXPERIENCE.md) | Course, interactions, diagrams, and learner paths |
| [`docs/06-TECHNICAL-ARCHITECTURE.md`](docs/06-TECHNICAL-ARCHITECTURE.md) | Independent repository architecture and host/guest boundaries |
| [`docs/07-CONTENT-AND-KNOWLEDGE-MODEL.md`](docs/07-CONTENT-AND-KNOWLEDGE-MODEL.md) | Shared human/LLM source model |
| [`docs/08-PHASED-IMPLEMENTATION-PLAN.md`](docs/08-PHASED-IMPLEMENTATION-PLAN.md) | Phase scope, dependencies, and exit gates |
| [`docs/09-QUALITY-SECURITY-ACCESSIBILITY.md`](docs/09-QUALITY-SECURITY-ACCESSIBILITY.md) | Accuracy, security, accessibility, browser, and performance requirements |
| [`docs/10-DECISIONS-AND-ADRS.md`](docs/10-DECISIONS-AND-ADRS.md) | Fixed product decisions and ADR queue |
