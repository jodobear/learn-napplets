# Phased Implementation Plan

Each phase is independently authorized, reviewable, and stoppable. Accuracy, accessibility, source provenance, and human/LLM parity are continuous requirements rather than final-phase cleanup.

## Phase 0 — Research and Truth Baseline

### Outcome

Verified protocol/taxonomy map, terminology, drift, compatibility matrix, security findings, technical spikes, and ADR recommendations.

### Work

Follow `docs/04-RESEARCH-PLAN.md`.

### Exit gate

- blocking source questions are documented;
- first-lab domain and host profile are selected or explicitly blocked;
- repository/framework/content recommendations have evidence;
- no production application was scaffolded outside disposable spikes.

---

## Phase 1 — Product and Content Contract

### Outcome

A buildable product specification derived from Phase 0.

### Work

- reconcile this brief with research;
- finalize MVP, v1, and future scope;
- finalize route/lesson graph;
- finalize learner paths;
- finalize source/evidence/maturity policy;
- finalize schemas;
- finalize lab inventory and implementation levels;
- accept or reject ADRs;
- identify blockers that remain upstream.

### Deliverables

```text
.planning/product/
├── PRODUCT.md
├── IA.md
├── CURRICULUM.md
├── CONTENT-CONTRACT.md
├── INTERACTION-INVENTORY.md
├── SOURCE-STATUS-POLICY.md
├── LLM-STRATEGY.md
└── MVP.md
```

### Exit gate

Every v1 route/lab has audience, objective, prerequisite, source pack, implementation level, static equivalent, and acceptance test.

---

## Phase 2 — Independent Repository Foundation

### Outcome

A static-first production workspace with explicit host/guest boundaries.

### Work

- initialize accepted workspace/framework;
- create public-site shell;
- create guest build boundary;
- implement content/source schemas;
- implement route generation, metadata, sitemap, and a static search index;
- implement source/status and glossary primitives;
- generate initial Markdown/knowledge artifacts;
- add test/deployment preview;
- enforce forbidden host imports.

### Exit gate

- site prerenders meaningful skeleton pages;
- schemas validate;
- machine outputs generate;
- host/guest architecture test passes;
- selected deployment preview works.

---

## Phase 3 — Visual and Content Primitives

### Outcome

Accessible data-driven components used by the first real vertical slice.

### Work

- design tokens and responsive layout;
- evidence/maturity/source badges;
- trust zones and capability ports;
- Story/System/Wire/Code view;
- trust, execution, composition, and specification diagrams;
- deterministic stepper;
- transcripts/tables/reduced motion;
- lesson and lab frames.

### Exit gate

Every canonical diagram renders as SVG, transcript, accessible table, and knowledge JSON. Components contain no hard-coded private protocol facts.

---

## Phase 4 — Real End-to-End Vertical Slice

### Outcome

The content MVP proves the learning model with actual napplet mechanics rather than throwaway simulations.

### Pages

- homepage;
- why napplets;
- sandbox boundary;
- one request;
- capabilities;
- glossary essentials;
- source/status baseline.

### Real implementation

- minimal production boundary-harness teaching host;
- one focused note-tool lab napplet, preferably the composer when Phase 0 approves its required domain;
- actual current sandbox/loading subset selected in Phase 0;
- actual namespace injection;
- actual `postMessage` and source-window mapping;
- deterministic selected-domain service;
- envelope/timeline inspector;
- capability removal and failure path.

### Instruments

- Monolith Splitter;
- Threat Lens;
- Envelope Journey driven by real messages;
- Capability Lab driven by the real napplet.

### Exit gate

A new learner can explain why the model exists, identify the trust boundary, trace an actual request, explain why signing authority stays in the host, and show graceful capability degradation.

The vertical slice passes browser, accessibility, content-source, and architecture tests.

---

## Phase 5 — Core Course and Workbench Expansion

### Outcome

Complete the foundational chapters and extend the teaching host without replacing Phase 4 work.

### Pages

- cast and mental model;
- optional Nostr primer;
- identity and distribution.

### Work

- Architecture Atlas;
- verified-loader profile or a clearly documented blocker;
- Manifest Identity Lab;
- real hashing/verification fixtures;
- expanded Workbench panes;
- first browser-safe conformance path;
- compatibility/source display in labs;
- broader deterministic fault injection.

### Exit gate

The host declares and passes its implemented profile. The identity lesson does not present unresolved manifest questions as settled. The first example passes applicable conformance checks.

---

## Phase 6 — Composition, Patterns, and Application Design

### Outcome

Learners can reason about focused apps and current runtime-mediated composition.

### Work

- refresh current composition sources;
- implement two viewer napplets;
- implement only the resolved composition-host subset;
- Composition Lab;
- pattern gallery;
- anti-pattern catalog;
- Architecture Clinic;
- independent-runtime interoperability attempt.

### Exit gate

- three real lab napplets exist;
- handler replacement is demonstrable where current sources permit it;
- unresolved archetype/convention/manifest behavior is visible;
- patterns are machine-readable.

---

## Phase 7 — Build, Runtime, and Protocol Contribution

### Outcome

A learner can build an app, understand a host, and locate the correct contribution seam.

### Work

- anatomy-of-a-napplet explorer;
- tested current build/conformance/publication tutorial;
- Conformance Lab;
- Runtime X-ray;
- contribution router;
- protocol design clinic;
- dated open-question map;
- source/package refresh.

### Exit gate

Commands execute in CI or are visibly illustrative. Runtime diagrams separate required behavior, possible architecture, host policy, and external adapters. Contribution cases route correctly.

---

## Phase 8 — Optional Portable Napplet Target

### Outcome

Publish the Workbench, selected-course, or full-course napplet approved by ADR 0007.

### Work

- implement separate guest entry;
- embed approved content/tools;
- map optional progress/link/composition capabilities;
- enforce no host imports;
- validate current artifact;
- test startup/bundle/accessibility;
- test in a compatible runtime;
- document and publish the artifact if approved.

### Exit gate

The artifact uses only current declared capabilities, contains no host authority, labels simulations, passes parity tests, and works under the tested runtime/source baseline.

Skip this phase when ADR 0007 is `NO-GO`.

---

## Phase 9 — Knowledge and LLM Hardening

### Outcome

The ecosystem map is retrievable without visual context.

### Work

- complete stable concepts/claims/relationships;
- versioned knowledge outputs;
- page Markdown;
- `llms.txt` and `llms-full.txt`;
- evaluation fixtures;
- human/machine parity checks;
- alias/deprecation rules;
- stale-source and stale-term checks.

### Exit gate

No essential fact exists only in an image or interaction. All knowledge outputs share the same source baseline and schema version.

---

## Phase 10 — Quality, Launch, and Maintenance

### Outcome

Production release with sustainable truth maintenance.

### Work

- audience-specific content reviews;
- final source/drift audit;
- accessibility and browser testing;
- performance tuning;
- teaching-host security review;
- public-site CSP review as project policy;
- deployment/publication;
- production smoke tests;
- source-freshness workflow;
- maintenance runbook;
- release notes and backlog.

### Exit gate

- all v1 requirements pass;
- production site and machine outputs are verified;
- example napplets are versioned;
- source-refresh workflow is enabled;
- unresolved upstream questions are visible.

## PR strategy

Suggested branches:

```text
research/truth-baseline
docs/product-contract
feat/repository-foundation
feat/visual-content-primitives
feat/real-vertical-slice
feat/core-course-workbench
feat/composition-patterns
feat/build-runtime-contribute
feat/portable-napplet
feat/knowledge-surface
chore/launch
```

Each PR includes objective, source revisions, decisions, implementation, screenshots/transcripts, tests, drift, out-of-scope work, and next-phase blockers.
