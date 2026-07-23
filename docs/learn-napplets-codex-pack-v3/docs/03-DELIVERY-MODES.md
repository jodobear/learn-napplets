# Delivery Modes: Website, Teaching Host, and Napplet Builds

## 1. One project, explicit runtime roles

Learn Napplets may produce several artifacts from shared content, but each artifact has a different authority and purpose.

| Artifact | Execution role | Purpose | v1 |
|---|---|---|---:|
| **Public site** | ordinary web app; declared teaching host | canonical lessons, stable links, source pages, labs | Required |
| **Lab napplets** | untrusted napplets | prove actual sandbox, domains, messages, identity, and composition | At least three required |
| **Workbench napplet** | untrusted napplet | portable architecture tools and simulations | ADR-gated |
| **Course napplet** | untrusted napplet | portable selected/full course using current artifact rules | ADR-gated |

## 2. Public-site mode

The public site provides:

- prerendered lessons;
- stable URLs and anchors;
- search;
- source/drift pages;
- diagram transcripts;
- machine-readable knowledge;
- a deterministic teaching host;
- embedded real lab napplets.

The site may perform host behavior because this build creates and owns the lab iframes. It must declare its implemented teaching-host profile.

## 3. Teaching-host profiles

### Boundary harness

Implements the current sandbox, namespace injection, `postMessage`, source-window mapping, and envelope observation.

### Verified loader

Adds current manifest resolution/signature/blob/aggregate verification and exact-byte loading.

### Selected-domain host

Adds explicitly named current NAP-domain services with deterministic fixtures.

### Composition host

Adds the current installed-handler/catalog/default-resolution mechanism.

A profile is a teaching capability declaration, not a claim that the site is a full production runtime.

## 4. Real lab napplets

Initial required set:

1. focused note composer;
2. minimal note viewer;
3. contextual note viewer.

Additional candidates:

- capability-degradation demo;
- storage-scope demo;
- invalid-envelope repair demo;
- manifest/identity demo;
- conformance repair exercise.

Each lab:

- performs one focused user job;
- uses only current source-defined domains/messages;
- feature-gates optional domains;
- builds to the artifact contract verified in Phase 0;
- runs in the teaching host;
- is tested in an independent runtime where feasible;
- passes applicable conformance checks;
- has a static transcript and explanation.

## 5. Workbench napplet

A Workbench napplet is a focused portable tool, not automatically the full course. Its single user job is to inspect and practice the napplet architecture; it must not become a disguised general-purpose client merely because it contains several related instruments.

Possible tools:

- architecture atlas;
- responsibility game;
- envelope decoder;
- capability selector;
- manifest identity calculator;
- contribution router;
- source/glossary lookup.

Candidate optional capabilities, subject to Phase 0 verification:

- storage for saved progress/scenarios;
- link opening for canonical sources;
- intent/composition for sibling example napplets.

Without an optional capability, it must degrade to memory, copyable citations, or a labeled simulation.

## 6. Course napplet

A course napplet is a separate guest build of shared course content. It is not the canonical public deployment.

Phase 0 must verify the current artifact, loading, storage, resource, link, and composition rules before implementation.

Likely constraints to test:

- self-contained/current-compatible artifact size;
- internal navigation without public-web route assumptions;
- optional mediated progress storage;
- optional source-link opening;
- embedded static core content;
- external runtime invocation of real sibling labs;
- startup, memory, accessibility, and update identity.

It must not depend on direct browser storage, direct relay access, a generic signer, a service worker, or privately nested “composed” napplets unless current upstream sources explicitly permit those behaviors.

## 7. Composition rule

A napplet may render a visual simulation of several actors. That is ordinary UI.

A napplet must not claim that private child frames are runtime-composed napplets. Real sibling napplets are created/focused by the external host through the current source-defined composition mechanism.

## 8. Separate entry points

Preferred shape, subject to ADR:

```text
apps/site/                  # host/public entry
apps/course-napplet/        # optional guest entry
napplets/*/                 # focused guests
packages/content/           # shared
packages/knowledge/         # shared
packages/ui/                # shared presentation
packages/diagrams/          # shared data/state
packages/teaching-host/     # host-only
```

Architecture tests must prevent host-only imports in guest artifacts.

## 9. Feature parity

Public site and portable napplet builds should share:

- lesson records;
- concept IDs;
- glossary;
- diagram data;
- assessments;
- source/status metadata.

They do not require identical navigation, persistence, routing, source-opening behavior, or lab hosting.

## 10. Course-napplet feasibility gate

Build a disposable prototype containing:

- two representative lessons;
- one architecture diagram and transcript;
- one code example;
- one assessment;
- source metadata;
- optional progress;
- optional external lab/source opening.

Measure:

- artifact shape and size;
- startup and memory;
- accessibility;
- navigation;
- runtime compatibility;
- capability degradation;
- update/identity implications;
- build complexity.

ADR outcomes:

- `GO-V1`;
- `GO-LATER`;
- `WORKBENCH-ONLY`;
- `NO-GO`.

Default hypothesis: `GO-LATER`.

## 11. Acceptance tests

### Public site

- works without a napplet runtime;
- exposes stable routes and static content;
- hosts at least one real lab napplet;
- declares host profile and limitations.

### Lab napplet

- boots under current sandbox/loading rules;
- uses only exposed domains;
- handles missing optional domains;
- emits validated messages;
- remains focused.

### Workbench/course napplet

- contains no host-only imports;
- uses the current artifact contract;
- avoids direct privileged browser assumptions;
- labels simulations;
- uses the external host for real sibling composition.
