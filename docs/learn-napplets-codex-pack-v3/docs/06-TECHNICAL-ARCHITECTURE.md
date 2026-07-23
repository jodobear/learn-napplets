# Technical Architecture

## 1. Status

This is an architectural hypothesis for Phase 0 evaluation. Accepted ADRs replace hypotheses before production scaffolding.

## 2. Independent workspace hypothesis

A small monorepo is likely appropriate because the product has multiple build targets and shared content.

```text
learn-napplets/
├── apps/
│   ├── site/                    # canonical public site; host role
│   └── course-napplet/          # optional guest role
├── napplets/
│   ├── note-composer/
│   ├── note-viewer-minimal/
│   └── note-viewer-context/
├── packages/
│   ├── content/
│   ├── knowledge/
│   ├── ui/
│   ├── diagrams/
│   ├── teaching-host/           # host-only
│   ├── protocol-fixtures/
│   ├── assessments/
│   └── build-tools/
├── docs/
├── .planning/
├── scripts/
└── tests/
```

Final names and tooling depend on ADRs.

## 3. Dependency boundaries

```text
content ─────────────► site
   ├────────────────► course-napplet
   ├────────────────► knowledge generators
   └────────────────► diagrams

protocol-fixtures ──► teaching-host
protocol-fixtures ──► lab napplets
teaching-host ──────► site

teaching-host ─X────► course-napplet
teaching-host ─X────► lab napplets
```

Enforce forbidden edges in tests or lint rules.

## 4. Build targets

### Public site

- static-first/prerendered;
- route-level interactive loading;
- host-only teaching environment;
- no server requirement for core lessons;
- no-JavaScript reading;
- generated Markdown and knowledge outputs;
- metadata, sitemap, and static search index.

### Lab napplets

- focused purpose;
- current verified artifact contract;
- current source-defined domain/messages;
- feature gating;
- deterministic fixture mode;
- conformance and interoperability tests.

### Course/Workbench napplet

- separate guest entry;
- no host imports;
- current verified artifact contract;
- embedded core content;
- optional capability adapters;
- internal navigation;
- explicit limitations.

## 5. Host/guest separation

Do not use one runtime bundle that infers trust.

Prefer separate applications or entries:

```text
entries/site.ts
entries/course-napplet.ts
```

Add bundle tests proving guest artifacts do not contain host code.

## 6. Teaching-host architecture

```text
TeachingHost
├── HostProfileDeclaration
├── FixtureOrVerifiedLoader
├── IframeHost
├── SourceWindowRegistry
├── DomainRegistry
├── PolicyEngine
├── DomainDispatcher
├── DeterministicServices
├── EnvelopeRecorder
├── TimelineRecorder
└── FaultInjector
```

### Profile 1 — Boundary harness

Uses actual current browser primitives for sandboxing, injection, messaging, and source-window mapping. It may load a pre-verified local fixture and must say so.

### Profile 2 — Verified loader

Adds current manifest, signature, blob, aggregate, artifact, and exact-byte verification.

### Profile 3 — Selected-domain host

Adds explicitly named current domain services.

### Profile 4 — Composition host

Adds current handler/catalog/default resolution.

The host reports its profile and source revisions. It does not call itself a full runtime unless independent tests support that claim.

## 7. Real browser mechanics

For protocol-sensitive lessons, use:

- actual sandboxed iframe;
- actual `srcdoc`/loading mechanism required by the current source;
- actual injection before authored scripts;
- actual `postMessage`;
- actual `MessageEvent.source`;
- structured-clone-safe objects.

Use deterministic simulation only for external systems such as relays, signers, Blossom, or devices.

## 8. Deterministic services

Candidate services, confirmed during Phase 0:

- identity fixture;
- scoped storage fixture;
- publish/query fixture;
- resource/link fixture;
- composition fixture.

Each service declares:

- source revision;
- domain and maturity;
- implemented operations;
- policy;
- fake side effects;
- fault modes;
- conformance coverage.

## 9. Internal learning-environment adapter

The project may define an internal UI abstraction:

```ts
type LearningEnvironment = {
  mode: 'public-site' | 'course-napplet';
  progress: {
    load(): Promise<ProgressState | null>;
    save(state: ProgressState): Promise<void>;
  };
  sources: {
    open(reference: SourceReference): Promise<'opened' | 'copied' | 'unavailable'>;
  };
  labs: {
    open(labId: string): Promise<'opened' | 'simulated' | 'unavailable'>;
  };
};
```

This is local application plumbing, not a NAP.

Possible mappings:

- public progress → privacy-reviewed browser persistence;
- guest progress → optional current storage domain, otherwise memory;
- public source → safe web link;
- guest source → optional link domain or copyable citation;
- public labs → teaching host;
- guest labs → external runtime composition or labeled simulation.

## 10. Content architecture

Use framework-independent structured Markdown plus typed data.

Content records reference stable IDs for claims, concepts, sources, labs, and diagrams. Interactive components do not encode protocol facts privately.

## 11. Protocol fixtures

Fixtures must be:

- tied to source revision;
- schema-validated where possible;
- human-readable;
- deterministic;
- reusable across site, lab napplets, and tests;
- clearly fake when representing signatures, relays, or publication.

Maintain a compatibility matrix between fixture revision, package version, and runtime version.

## 12. Diagram architecture

Diagrams are structured data:

```ts
type DiagramNode = {
  id: string;
  label: string;
  kind: string;
  trust: 'trusted' | 'untrusted' | 'external';
  evidenceClass: EvidenceClass;
  maturity: Maturity;
  description: string;
  sourceRefs: string[];
};

type DiagramEdge = {
  id: string;
  from: string;
  to: string;
  relation: string;
  style: 'request' | 'response' | 'policy' | 'distribution' | 'forbidden';
};

type DiagramStep = {
  id: string;
  narration: string;
  activeNodes: string[];
  activeEdges: string[];
};
```

The same data renders SVG, transcript, accessible table, and knowledge JSON.

## 13. Framework selection criteria

Evaluate:

- current ecosystem compatibility;
- prerendered output;
- interactive component ergonomics;
- Markdown/data pipeline;
- multiple entries;
- current napplet artifact build;
- accessibility;
- browser testing;
- bundle isolation;
- maintenance cost.

Do not choose a framework because another learning site uses it.

## 14. Package consumption

Consume only public released exports.

For each dependency record:

- version/commit;
- public export;
- browser support;
- source revision implemented;
- known drift;
- fallback/adapter strategy.

If a useful upstream helper is private, either implement a minimal source-faithful local adapter or create a separate upstream task. Do not import source internals.

## 15. Knowledge outputs

Generate versioned outputs:

```text
/knowledge/v1/index.json
/knowledge/v1/concepts.json
/knowledge/v1/relationships.json
/knowledge/v1/claims.json
/knowledge/v1/sources.json
/knowledge/v1/status.json
/llms.txt
/llms-full.txt
```

Every JSON document includes `schemaVersion`, `generatedAt`, and source-baseline metadata.

## 16. Deployment

The independent repository owns all releases.

Likely outputs:

```text
dist/site/
dist/napplets/<name>/
dist/course-napplet/        # optional
dist/knowledge/
```

Public-site deployment and napplet publication are separate release operations.

## 17. Observability

Development mode exposes:

- host profile;
- source baseline;
- iframe lifecycle;
- injected domains;
- actual envelopes;
- source-window mapping;
- policy decision;
- service action;
- conformance findings.

Observer explanations are out-of-band teaching UI, not invented protocol responses.

## 18. Architecture tests

- forbidden host imports in guest bundles;
- source/fixture revision consistency;
- content-renderer parity;
- source ID resolution;
- source-window mapping;
- domain-presence toggles;
- envelope validation;
- no-JavaScript routes;
- current artifact validation;
- deterministic replay;
- knowledge schema/version checks.
