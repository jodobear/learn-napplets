# Phase 0 — Research and Truth Baseline

## 1. Objective

Produce a dated, source-linked baseline that answers:

- what the current napplet model is;
- which terms the course should use;
- where current upstream sources disagree;
- which protocol surfaces the first real labs can safely exercise;
- which public packages and runtime implementations match which source revisions;
- how the independent site and optional napplet builds should be structured.

Phase 0 is a decision phase, not a documentation scavenger hunt. Inventory broadly; deep-read only material that affects the MVP, a known drift item, or an architectural decision.

## 2. Research workspace

Use an ignored directory:

```text
.research/upstreams/
├── nips/
├── naps/
├── napplet-web/
├── runtimes/
└── learning-products/
```

Never edit these clones.

Record exact commit SHAs and file digests. If cloning is unavailable, use current raw/API sources and document the limitation.

## 3. Priority tiers

### Tier 1 — Blocking truth baseline

Complete before any production architecture decision:

- current NIP-5D text and PR state;
- current NAP registry/projection terminology;
- manifest and identity model;
- capability discovery/bootstrap model;
- current composition/archetype/convention model;
- browser sandbox and outbound-network behavior;
- core MVP domain proposals;
- package/runtime compatibility for the first lab;
- teaching-host feasibility;
- independent repository/framework/content architecture.

### Tier 2 — Required ecosystem inventory

Inventory every current NAP, archetype, convention, issue, PR, and implementation by metadata. Deep-read only entries that:

- affect the first thirteen lessons;
- are used by an example;
- conflict with a higher-authority source;
- are active enough to change a near-term decision;
- demonstrate an important protocol boundary.

### Tier 3 — Deferred discovery

Record, but do not let these block the baseline unless they affect v1:

- advanced value/device/media domains;
- speculative native/WASM projections;
- live-relay course mode;
- generalized AI tutor;
- full production runtime architecture.

## 4. Protocol audit

### 4.1 NIP-5D

Document:

- current title/status/revision;
- philosophy and scope;
- terminology;
- sandbox and loading;
- message carrier and envelope;
- source-window authentication;
- namespace injection and domain availability;
- exact-code identity;
- manifest kinds/tags/artifact shape;
- required-capability behavior;
- signing/encryption boundary;
- guarantees and non-guarantees;
- unresolved review concerns.

Do not use the PR’s original description when it conflicts with the current file.

### 4.2 NAP registry and taxonomy

Document:

- capability seam;
- domain naming;
- projection-neutral contract versus web binding;
- request/result/push conventions;
- archetype registry;
- app-to-app convention model;
- NAP governance and implementation requirement;
- current active/draft/deferred/legacy entries.

### 4.3 Blocking drift checklist

Create a separate finding for each:

1. object-presence discovery versus `shell.supports()`;
2. NAP-SHELL/handshake assumptions;
3. NIP-5D-specific manifest kinds versus NIP-5A kind `35128` descriptions;
4. identity use of `dTag` when some current manifest kinds may have no `d` tag;
5. whether current manifests define/permit archetype and convention metadata;
6. NAP-INTENT’s handler/catalog/dTag assumptions under the current manifest model;
7. current unknown-message and unknown-source behavior;
8. exact artifact rule versus current build-tool output;
9. current browser-network restrictions versus the stated mediated-access model;
10. any conformance/build checks enforcing private or retired behavior.

A blocking item may remain unresolved upstream. The project response is then to label it and avoid pretending it is settled.

### 4.4 Core MVP domain deep reads

Confirm the current candidate set before deep-reading it. Expected candidates include the domains needed for:

- identity display;
- draft/progress storage;
- note publication/query;
- resources/source links;
- composition/default handlers.

Select a first real lab operation using this order:

1. preferred: an operation that advances the note journey, such as draft storage or note publication, when its current proposal and implementation are sufficiently coherent;
2. fallback: a simpler current domain operation, such as read-only identity or scoped storage, when publication is too unstable;
3. blocked: no real-domain Phase 4 lab until the gap is documented. Never invent a teaching-only protocol domain.

For each selected proposal, extract:

- domain and maturity;
- operations;
- wire messages;
- error/lifecycle behavior;
- shell obligations;
- security boundary;
- implementation links;
- conflicts with NIP-5D or templates;
- suitability for a first real lab.

## 5. Implementation audit

### 5.1 `napplet/web`

Map public, supported surfaces only:

- core/envelope types;
- domain contracts;
- shim;
- SDK;
- build plugin;
- CLI/starter;
- conformance engine and browser exports;
- examples/skills;
- current open issues and PRs affecting v1.

For each useful surface, record:

- package/version/commit;
- public export;
- browser compatibility;
- source revision it appears to implement;
- known drift;
- whether to consume, wrap, or avoid.

### 5.2 Runtime implementations

For each credible runtime, map:

- loader/verifier;
- browser shell adapter;
- session/source mapping;
- policy/ACL;
- dispatch;
- domain services;
- storage scoping;
- signer/relay adapters;
- composition/catalog behavior;
- conformance and known drift.

Classify each block:

- required current behavior;
- possible architecture;
- host policy;
- external adapter.

## 6. Ecosystem examples and current-work audit

Identify current public napplets, demos, starter applications, runtime galleries, and published examples. For each useful example record:

- repository or manifest pointer;
- exact revision;
- user job;
- domains/archetypes/conventions used;
- runtime tested;
- conformance evidence;
- screenshot/demo availability;
- license and whether it may be adapted or only linked;
- lesson or inspiration-gallery relevance.

Do not assume an app is protocol-faithful because it is labeled a napplet.

Then snapshot:

- NIP-5D PR state and current head;
- open `napplet/web` issues/PRs;
- open NAP PRs and labels;
- relevant discussions;
- linked/recent branches that materially affect v1;
- package/runtime releases.

Do not deep-read every branch. Branch names and recent activity are weak signals unless tied to a PR, issue, or source change.

For each item classify impact:

- terminology;
- lesson content;
- lab behavior;
- package integration;
- runtime example;
- contribution case study;
- no v1 impact.

## 7. Pedagogy and audience audit

Study Learn FIPS and at least two other strong technical learning products.

Extract:

- lesson sequencing;
- recurring scenario;
- simulation/lab placement;
- playground and glossary patterns;
- assessment style;
- progress and accessibility;
- content/data separation;
- testing;
- patterns to reuse/adapt/avoid.

Create persona/jobs records for:

- new-to-Nostr developer;
- Nostr developer;
- general application developer;
- runtime implementer;
- protocol contributor;
- LLM/coding agent.

For each define prerequisite, goal, misconception, useful analogy, analogy failure, preferred representation, and assessment task.

## 8. Lesson research packets

Create one research packet for each planned lesson before Phase 1 writes final curriculum copy.

Each packet contains:

- learner question and prerequisite;
- current terminology;
- source-linked claim candidates;
- implementation/runtime evidence;
- known drift and open questions;
- likely misconceptions;
- candidate Story/System/Wire/Code representations;
- candidate lab and whether it should be real or simulated;
- code/wire fixtures needed;
- facts that must not yet be taught as settled;
- follow-up research needed.

Store them under:

```text
.planning/research/lesson-packets/
├── 01-why-napplets.md
├── 02-mental-model.md
├── ...
└── 13-evolving-the-protocol.md
```

Also produce machine-readable ecosystem catalogs:

```text
.planning/research/domain-catalog.yaml
.planning/research/archetype-convention-catalog.yaml
```

Catalog every current entry by identifier, maturity, source revision, implementation evidence, and v1 relevance.

## 9. Mandatory technical spikes

### A — Independent workspace

Compare the smallest workspace structures that support a public site, shared content, host-only code, and multiple napplet builds.

### B — Static-first site framework

Compare plausible current options against prerendering, interactive labs, Markdown/content, multiple entries, testing, bundle isolation, and static deployment.

### C — Real boundary harness

Prove with actual browser primitives:

- current iframe sandbox;
- current pre-script domain injection;
- `postMessage`;
- `MessageEvent.source` mapping;
- domain removal;
- envelope recording;
- deterministic service response.

### D — Verified-loader feasibility

Prove or identify blockers for current manifest resolution, signature/blob/aggregate verification, exact-byte loading, and identity mapping.

### E — Shared content, multiple renderers

Prove one source record can render to static HTML, guest content, Markdown, glossary, transcript, and knowledge JSON.

### F — Course/Workbench napplet feasibility

Build the two-lesson prototype from `03-DELIVERY-MODES.md` and return `GO-V1`, `GO-LATER`, `WORKBENCH-ONLY`, or `NO-GO`.

### G — Package/conformance consumption

Determine which released public exports can be consumed safely. Do not import private monorepo paths.

### H — Browser egress and public-site CSP

Empirically test, under the current iframe/loading model:

- `fetch`;
- images/media;
- classic/module scripts;
- WebSocket;
- EventSource;
- workers;
- form/navigation channels;
- referrer/origin behavior.

Separate:

- what the current NIP states;
- what browsers actually enforce;
- what the public teaching site should enforce as project policy;
- what remains an upstream protocol question.

Never turn the project’s CSP into a claimed NIP requirement.

### I — Diagram/motion stack

Compare data-driven SVG and minimal state/motion libraries for accessibility, reduced motion, deterministic screenshots, and bundle cost.

### J — Code-editing scope

Compare fixed variants, controlled textarea edits, lightweight editors, and CodeMirror. Select the least complex option that supports the learning objective.

### K — Deployment and publication

Test independent public-site deployment, lab napplet build/publication, and optional course napplet output.

### L — Source freshness

Prototype SHA/digest refresh, changed-path detection, impact mapping, and report generation.

## 10. Required artifacts

```text
.planning/
├── STATUS.md
├── research/
│   ├── executive-summary.md
│   ├── decision-summary.md
│   ├── protocol-map.md
│   ├── terminology-map.yaml
│   ├── source-registry.yaml
│   ├── claims.yaml
│   ├── compatibility-matrix.yaml
│   ├── teaching-scope.yaml
│   ├── domain-catalog.yaml
│   ├── archetype-convention-catalog.yaml
│   ├── example-napplet-catalog.yaml
│   ├── lesson-packets/
│   │   └── 01...13.md
│   ├── drift-register.yaml
│   ├── open-questions.yaml
│   ├── open-work-snapshot.json
│   ├── open-work-analysis.md
│   ├── package-map.md
│   ├── runtime-comparison.md
│   ├── pedagogy-review.md
│   ├── audiences.md
│   ├── jobs-to-be-done.yaml
│   ├── delivery-mode-recommendation.md
│   ├── security-egress-findings.md
│   └── risks.md
├── spikes/
│   └── ...
└── adr/
    ├── 0001-repository-workspace.md
    ├── 0002-site-framework.md
    ├── 0003-deployment-shape.md
    ├── 0004-content-source-model.md
    ├── 0005-teaching-host.md
    ├── 0006-diagram-motion-stack.md
    ├── 0007-portable-napplet-target.md
    └── 0008-protocol-fixture-strategy.md
```

## 11. Report standard

Every report separates:

- research question;
- sources and immutable revisions;
- observations;
- conflicts;
- inference;
- prototype/measurement;
- recommendation;
- uncertainty;
- affected phases.

## 12. Exit criteria

Phase 0 passes only when:

- every core concept has a source pack;
- all thirteen lesson research packets exist;
- domain, archetype/convention, and example-napplet catalogs exist;
- terminology is mapped;
- high-risk drift is registered;
- core MVP domains are selected or explicitly blocked;
- source/package/runtime compatibility is recorded;
- boundary-harness and content-rendering spikes pass;
- verified-loader feasibility is known;
- browser-egress findings exist;
- portable-napplet scope has an ADR recommendation;
- workspace/framework/deployment recommendations have evidence;
- no production framework was committed outside disposable spikes;
- the research branch is PR-ready.

## 13. Executive decision questions

The final summary answers:

1. What is the current mental model?
2. Which terms should the course use?
3. Which claims remain disputed?
4. Which domains and composition mechanisms can v1 demonstrate honestly?
5. Which public implementation surfaces can be consumed?
6. Which teaching-host profile should Phase 4 implement first?
7. Should v1 include a Workbench or course napplet?
8. Which repository architecture should Phase 2 implement?
9. What source change would invalidate each decision?
