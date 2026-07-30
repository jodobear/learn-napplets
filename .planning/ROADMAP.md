# Roadmap: Learn Napplets

## Overview

This standard, source-ordered horizontal roadmap preserves the intent and order of the accepted source implementation plan: source Phases 0–10 map directly to GSD Phases 1–11. It begins with revision-pinned research and decision evidence, then defines the product contract before any production scaffold, and proceeds through the public learning experience, real napplet labs, knowledge outputs, and release maintenance. The source plan is `docs/learn-napplets-codex-pack-v3/docs/08-PHASED-IMPLEMENTATION-PLAN.md`.

**Roadmap mode:** Standard / horizontal, source-plan ordered

**Current gate:** Phase 1 terminal attestation has been published after human terminal verification and project-owner recheck. This records Phase 1 closeout only; ADR 0001–0011 remain proposed, and no production application scaffold, deployment/release, external action, residual-risk acceptance, package admission, or Phase 2 transition is authorized.

**Ownership rule:** Each v1 requirement has one owning phase only. Later phases may support or enforce an owned requirement but do not acquire duplicate ownership.

## Phases

**Phase Numbering:**

- Integer phases are planned work.
- Decimal phases are reserved for explicitly approved inserted work only.

- [x] **Phase 1: Research and Truth Baseline** - Source Phase 0 research, spikes, and recommendations establish an evidence-backed decision baseline.
- [ ] **Phase 2: Product and Content Contract** - Source Phase 1 turns accepted research and decisions into a buildable learning contract.
- [ ] **Phase 3: Independent Repository Foundation** - Source Phase 2 creates the static-first workspace and enforceable host/guest boundary.
- [ ] **Phase 4: Visual and Content Primitives** - Source Phase 3 supplies accessible, data-driven learning and diagram primitives.
- [ ] **Phase 5: Real End-to-End Vertical Slice** - Source Phase 4 proves the learning model through a real, deterministic boundary-harness lab.
- [ ] **Phase 6: Core Course and Workbench Expansion** - Source Phase 5 completes foundational lessons and extends the teaching host.
- [ ] **Phase 7: Composition, Patterns, and Application Design** - Source Phase 6 teaches focused apps and runtime-mediated composition with real napplets.
- [ ] **Phase 8: Build, Runtime, and Protocol Contribution** - Source Phase 7 connects application building, runtime behavior, and contribution seams.
- [ ] **Phase 9: Optional Portable Napplet Target** - Source Phase 8 conditionally publishes the ADR-approved portable artifact without blocking the public site.
- [ ] **Phase 10: Knowledge and LLM Hardening** - Source Phase 9 makes the ecosystem map retrievable through versioned, common-source outputs.
- [ ] **Phase 11: Quality, Launch, and Maintenance** - Source Phase 10 completes release gates and establishes sustainable truth maintenance.

## Phase Details

### Phase 1: Research and Truth Baseline

**Source phase crosswalk**: Source Phase 0 — Research and Truth Baseline

**Goal**: Decision makers and maintainers can rely on a dated, immutable-source evidence baseline to choose the first safe teaching scope and architecture without presenting unsettled upstream behavior as fact.

**Depends on**: Nothing (first phase)

**Requirements**: EVID-01, EVID-02, EVID-03, EVID-04, OPER-01, OPER-03

**Success Criteria** (what must be TRUE):

  1. A maintainer can trace every blocking protocol-sensitive claim to its immutable upstream revision, path or locator, digest, retrieval date, authority tier, evidence class, and maturity label.
  2. A maintainer can inspect each volatile claim's conflicts, uncertainty, drift status, affected requirement or phase, and refresh trigger instead of treating disagreement as settled.
  3. A decision maker can review a compatibility matrix spanning the selected protocol sources, packages, runtimes, examples, and current upstream work before architecture is proposed.
  4. A decision maker can inspect reproducible measurements from each mandatory spike before repository, framework, deployment, content, teaching-host, fixture, and portable-target recommendations are considered.
  5. The project owner can review a source-backed recommendation for the first lab domain and teaching-host profile, or an explicit blocker, while confirming that no production application scaffold was created.

**Required reviews / human approvals**: Deep plan-review convergence is required before any Phase 1 execution. After research, the project owner reviews the evidence baseline, spike results, unresolved upstream questions, and ADR recommendations; ADRs remain unaccepted until Phase 2.

**Expected outputs**:

- Dated source registry, claims, terminology, protocol map, compatibility matrix, drift register, open-question register, and current-work snapshot under `.planning/research/`.
- Domain, archetype/convention, and example-napplet catalogs plus thirteen lesson research packets.
- Mandatory spike evidence for workspace, site framework, boundary harness, verified loader, shared content, portable target, package consumption, egress/CSP, diagrams, code editing, deployment, and source freshness.
- Evidence-backed ADR recommendations and a research executive/decision summary; all recommendations remain proposals.
- Phase governance and traceability convention for the remaining roadmap.

**Plans**: 45/45 plans executed

Gap Closure Plans:

**Wave 1**

- [x] 01-29-PLAN.md — Establish the stdlib-only bootstrap and content-addressed independent review authorization.

**Wave 2** *(blocked on Plan 01-29)*

- [x] 01-44-PLAN.md — Build and certify a complete hash-locked fresh environment from verified wheel artifacts.

**Wave 3** *(blocked on Plan 01-44)*

- [x] 01-45-PLAN.md — Trace bounded immutable public-source acquisition and retain complete acquisition history.

**Wave 4** *(blocked on Plan 01-45)*

- [x] 01-30-PLAN.md — Obtain human authority classifications before source ingestion.
- [x] 01-32-PLAN.md — Repair citation provenance, strict review parsing, and wrapper invocation.
- [x] 01-33-PLAN.md — Bind retained spike evidence and remove manifest command authority.

**Wave 5**

- [x] 01-31-PLAN.md — Ingest reviewed source/normative evidence or impact-scoped blockers.
- [x] 01-34-PLAN.md — Close CR-05 path/source confinement and CR-08 observed-local versus normative classification.

**Wave 6**

- [x] 01-41-PLAN.md — Independently intake package registry evidence and retain scoped package blockers.
- [x] 01-42-PLAN.md — Close CR-07 durable crash-atomic canonical publication, transactional reads, and recovery.

**Wave 7** *(blocked on Plans 01-34, 01-41, and 01-42)*

- [x] 01-35-PLAN.md — Migrate and evaluate substantive compatibility eligibility from one registered transactional snapshot.

**Wave 8**

- [x] 01-36-PLAN.md — Run approval-gated package/conformance measurement or retain a precise blocker.

**Wave 9** *(blocked on Plan 01-36)*

- [x] 01-43-PLAN.md — Append observed upstream refresh records and retain blocker routing.

**Wave 10** *(blocked on all upstream gap plans, including Plan 01-43)*

- [x] 01-37-PLAN.md — Execute the complete repaired Phase 1 gate sequence.

**Wave 11**

- [x] 01-38-PLAN.md — Complete Nyquist probes and reconcile validation evidence.

**Wave 12**

- [x] 01-39-PLAN.md — Record ASVS L1 security remediation review.

**Wave 13**

- [x] 01-40-PLAN.md — Freshly verify Phase 1 and synchronize factual status/accounting after human terminal verification and project-owner recheck.

Plans:
**Wave 1**

- [x] 01-01-PLAN.md — Approve and isolate the Phase 1 research toolchain.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-02-PLAN.md — Prove the source-record to validation-review tracer and claim contract.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 01-03-PLAN.md — Define drift, open-question, and compatibility contracts.
- [x] 01-04-PLAN.md — Define reproducible spike and phase-governance contracts.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 01-05-PLAN.md — Acquire bounded immutable sources and derive source-linked claims.

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 01-06-PLAN.md — Record drift, compatibility, current work, and refresh review work.

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 01-07-PLAN.md — Build ecosystem/domain/archetype/example catalogs.

**Wave 7** *(blocked on Wave 6 completion)*

- [x] 01-26-PLAN.md — Synthesize audience, pedagogy, delivery, and first teaching scope.
- [x] 01-20-PLAN.md — Run SPK-L source-freshness evidence.

**Wave 8** *(blocked on Wave 7 completion, including Plan 01-20 source-freshness evidence)*

- [x] 01-08-PLAN.md — Create the shared index and LES-01 through LES-04 packets.
- [x] 01-09-PLAN.md — Run SPK-A independent-workspace evidence.
- [x] 01-10-PLAN.md — Run SPK-B static-framework evidence behind package approval.
- [x] 01-11-PLAN.md — Run SPK-C browser evidence and preserve its immutable local impact fragment.
- [x] 01-12-PLAN.md — Run SPK-D verified-loader evidence and preserve its immutable local impact fragment.
- [x] 01-13-PLAN.md — Run SPK-E shared-content rendering evidence.
- [x] 01-14-PLAN.md — Run SPK-F portable Workbench/course feasibility evidence.
- [x] 01-15-PLAN.md — Run SPK-G package/conformance evidence and preserve its immutable local impact fragment.
- [x] 01-17-PLAN.md — Run SPK-I diagram/motion accessibility evidence.
- [x] 01-18-PLAN.md — Run SPK-J least-authority code-editing evidence.
- [x] 01-19-PLAN.md — Run SPK-K local/authorized deployment evidence.

**Wave 9** *(blocked on SPK-C's selected boundary model)*

- [x] 01-16-PLAN.md — Run SPK-H browser egress/CSP evidence using the selected SPK-C model.

**Wave 10** *(blocked on all spike evidence, including SPK-H)*

- [x] 01-28-PLAN.md — Serially consolidate all spike reports and impact fragments into canonical evidence.

**Wave 11** *(blocked on consolidation)*

- [x] 01-21-PLAN.md — Draft proposed ADR 0001–0004 from consolidated evidence.
- [x] 01-22-PLAN.md — Draft proposed ADR 0005–0008 from consolidated evidence.
- [x] 01-27-PLAN.md — Create LES-05 through LES-09 packets.

**Wave 12** *(blocked on the Wave 11 proposal and lesson inputs)*

- [x] 01-25-PLAN.md — Complete LES-10 through LES-13 and the exact inventory.
- [x] 01-23-PLAN.md — Draft proposed ADR 0009–0011 and decision summaries from consolidated evidence.

**Wave 13** *(blocked on the completed evidence baseline)*

- [x] 01-24-PLAN.md — Enforce the Phase 1 gate after consolidation and stop for human closeout.

### Phase 2: Product and Content Contract

**Source phase crosswalk**: Source Phase 1 — Product and Content Contract

**Goal**: The project owner can approve a buildable, evidence-derived product and learning contract before production implementation begins.

**Depends on**: a human-recorded passed Phase 1 evidence baseline plus the evidence-backed, still-proposed ADR 0001–0011 handoff.

**Entry boundary**: Phase 2 may define the product/content contract from the proposed ADR evidence. Human ADR acceptance, rejection, or explicit deferral and Phase 2 contract approval remain separate prerequisites for any production application/framework scaffolding.

**Requirements**: LEARN-01

**Success Criteria** (what must be TRUE):

  1. A curriculum reviewer can inspect every v1 lesson and lab to find its audience, objective, prerequisites, source pack, misconceptions, implementation level, static equivalent, and acceptance evidence.
  2. A project owner can see a coherent route and learner-path graph that connects the recurring note journey to each lesson, representation, and assessment.
  3. A content author can distinguish committed scope, conditionally gated work, future work, and upstream blockers without inventing settled protocol facts.
  4. A build planner can use the accepted content, interaction, source-status, and machine-output contracts to determine what each later phase must deliver.

**Required reviews / human approvals**: The project owner approves the product contract, route and curriculum graph, source/evidence/maturity policy, and accepted or rejected ADRs. Production scaffolding remains prohibited until this approval is recorded.

**Expected outputs**:

- `.planning/product/PRODUCT.md`, `IA.md`, `CURRICULUM.md`, `CONTENT-CONTRACT.md`, `INTERACTION-INVENTORY.md`, `SOURCE-STATUS-POLICY.md`, and `LLM-STRATEGY.md`.
- Finalized v1, conditional, and future scope; route/lesson graph; learner paths; lab inventory; implementation levels; and acceptance tests.
- ADR decisions or explicitly retained upstream blockers derived from Phase 1 evidence.

**Plans**: TBD

### Phase 3: Independent Repository Foundation

**Source phase crosswalk**: Source Phase 2 — Independent Repository Foundation

**Goal**: Developers can build and preview a static-first public learning workspace whose content, guest builds, and host-only authority are structurally separated.

**Depends on**: Phase 2

**Requirements**: A11Y-03

**Success Criteria** (what must be TRUE):

  1. A learner can open the required foundation learning path without a live relay, wallet, signer, device, or other external service being needed.
  2. A developer can prerender meaningful skeleton routes, metadata, sitemap, search index, source/status data, and initial human and machine-readable artifacts from the accepted content contract.
  3. A maintainer can validate content and source schemas before publishing a route or generated knowledge artifact.
  4. An architecture reviewer can verify through automated checks that public-site and guest-build code cannot import host-only authority.

**Required reviews / human approvals**: The project owner reviews the production workspace against accepted ADR 0001–0005 and deployment evidence. An architecture/security review approves the host/guest boundary before real lab authority is added.

**Expected outputs**:

- Accepted workspace and static-first site foundation with separate public-site, shared-content, host-only, and guest-build boundaries.
- Content/source schemas; route generation; metadata, sitemap, static search, glossary, source/status primitives; and initial Markdown/knowledge generation.
- Preview deployment path, test baseline, and forbidden-host-import enforcement.

**Plans**: TBD

### Phase 4: Visual and Content Primitives

**Source phase crosswalk**: Source Phase 3 — Visual and Content Primitives

**Goal**: Learners can use accessible, data-driven visual representations and lesson/lab frames that explain authority boundaries without embedding private protocol assertions in components.

**Depends on**: Phase 3

**Requirements**: A11Y-01

**Success Criteria** (what must be TRUE):

  1. A learner can operate every shipped canonical diagram or stepper with a keyboard, reset and replay it deterministically, and use reduced-motion behavior.
  2. A learner can obtain the same essential diagram or interaction meaning through a transcript, state inspection, static explanation, and accessible table rather than relying on animation alone.
  3. A content author can render trust, execution, composition, and specification views from structured records while keeping source, maturity, and policy status visible.
  4. A reviewer can confirm that canonical diagrams provide SVG, transcript, accessible-table, and knowledge-JSON representations with no hard-coded private protocol facts.

**Required reviews / human approvals**: A human accessibility review validates keyboard, transcript, static-equivalent, and reduced-motion behavior. The project owner approves the visual/content primitive set for the first vertical slice.

**Expected outputs**:

- Design tokens, responsive lesson/lab layout, evidence and maturity badges, trust zones, capability ports, and Story/System/Wire/Code views.
- Data-driven trust, execution, composition, and specification diagrams with transcript/table/reduced-motion variants.
- Deterministic stepper plus reusable lesson and lab frames.

**Plans**: TBD
**UI hint**: yes

### Phase 5: Real End-to-End Vertical Slice

**Source phase crosswalk**: Source Phase 4 — Real End-to-End Vertical Slice

**Goal**: A new learner can safely understand and exercise one actual napplet request across the trusted-host/untrusted-guest boundary using a deterministic, evidence-scoped teaching host.

**Depends on**: Phase 4

**Requirements**: LEARN-03, SECU-01, SECU-02, SECU-04

**Success Criteria** (what must be TRUE):

  1. A learner can identify the trusted host and untrusted napplet, trace an actual request/result through the envelope timeline, and explain why signing authority stays in the host.
  2. A developer can run the teaching host knowing a guest napplet cannot directly access host-only keys, signers, relay pools, wallets, devices, uploads, or policy outside declared mediated capabilities.
  3. A developer can run browser tests that verify source-window/session identity, request/response envelopes, capability gating, lifecycle, errors, and deterministic service responses.
  4. A learner can remove a declared capability, observe a deterministic failure path and graceful degradation, and complete the required lab without real keys or live external systems.
  5. A new learner can use the homepage, why-napplets, sandbox-boundary, one-request, capabilities, glossary-essentials, and source/status content to explain why the model exists.

**Required reviews / human approvals**: The project owner approves the selected real domain and teaching-host profile against Phase 1 evidence. Human security, accessibility, browser-compatibility, content-source, and architecture reviews must pass before the slice is accepted.

**Expected outputs**:

- Minimal production boundary-harness teaching host and one focused real note-tool lab napplet using the Phase 1-approved current subset.
- Actual sandbox/loading subset, namespace injection, `postMessage`, source-window mapping, deterministic domain service, envelope/timeline inspector, and capability removal path.
- First public content vertical slice and its Monolith Splitter, Threat Lens, Envelope Journey, and Capability Lab instruments.

**Plans**: TBD
**UI hint**: yes

### Phase 6: Core Course and Workbench Expansion

**Source phase crosswalk**: Source Phase 5 — Core Course and Workbench Expansion

**Goal**: Learners can apply the foundational mental model across terminology, identity, distribution, and narrower capability choices while the teaching host declares its implemented profile.

**Depends on**: Phase 5

**Requirements**: LEARN-02, LEARN-04

**Success Criteria** (what must be TRUE):

  1. A learner can distinguish shell, runtime, runtime internals, capability, projection, archetype, and app-to-app convention using the current terminology and visible maturity labels.
  2. A learner can select the narrowest appropriate capability or domain for a learning task and explain what graceful degradation looks like when it is absent.
  3. A developer can inspect the declared teaching-host profile, its compatibility/source display, and the first browser-safe conformance result instead of inferring undocumented host behavior.
  4. A learner can follow the cast-and-mental-model, optional Nostr-primer, identity, and distribution chapters without being told unresolved manifest questions are settled.

**Required reviews / human approvals**: The project owner approves the foundational chapter expansion and declared host profile. Human review confirms terminology, identity claims, and verification fixtures match the current evidence baseline.

**Expected outputs**:

- Core foundational chapters, Architecture Atlas, Manifest Identity Lab, real hashing/verification fixtures, and expanded Workbench panes.
- Declared and tested host profile, verified-loader result or explicit blocker, first browser-safe conformance path, compatibility/source displays, and broader deterministic fault injection.

**Plans**: TBD
**UI hint**: yes

### Phase 7: Composition, Patterns, and Application Design

**Source phase crosswalk**: Source Phase 6 — Composition, Patterns, and Application Design

**Goal**: Developers can run and reason about a small set of focused, real napplets and the current evidence-scoped composition patterns that connect them.

**Depends on**: Phase 6

**Requirements**: LABS-01, LABS-03

**Success Criteria** (what must be TRUE):

  1. A developer can run, modify, test, and understand at least three real v1 lab napplets without relying on undocumented teaching-host behavior.
  2. A learner can observe the supported composition behavior, including handler replacement where current sources permit it, and see unresolved archetype, convention, or manifest behavior labeled rather than hidden.
  3. A user of each published example can inspect its teaching-host profile, required capabilities, source identity, compatibility, limitations, and real-versus-simulated behavior.
  4. A developer can use the Composition Lab, pattern gallery, anti-pattern catalog, and Architecture Clinic to compare focused application designs and an independent-runtime interoperability attempt.

**Required reviews / human approvals**: The project owner approves the three-lab set and the resolved composition-host subset. Human architecture and source-evidence review confirms examples make only supportable interoperability claims.

**Expected outputs**:

- Two additional real viewer napplets alongside the original focused note-tool lab.
- Evidence-scoped composition-host subset, Composition Lab, pattern gallery, anti-pattern catalog, Architecture Clinic, and interoperability-attempt record.
- Machine-readable patterns and complete example declarations.

**Plans**: TBD
**UI hint**: yes

### Phase 8: Build, Runtime, and Protocol Contribution

**Source phase crosswalk**: Source Phase 7 — Build, Runtime, and Protocol Contribution

**Goal**: Learners can build an application, distinguish runtime behavior from project policy, and route a proposed change to the correct contribution seam.

**Depends on**: Phase 7

**Requirements**: LEARN-05, LABS-02

**Success Criteria** (what must be TRUE):

  1. A learner can classify a proposed change as protocol, SDK, runtime, content, or application work and use the contribution router to find the appropriate next step.
  2. A learner can use deterministic architecture, capability, identity, composition, and conformance labs that cite the current evidence baseline.
  3. A developer can follow a current build, conformance, and publication tutorial whose commands execute in CI or are plainly labeled as illustrative.
  4. A learner can inspect Runtime X-ray views and protocol-design cases that separate required behavior, possible architecture, host policy, and external adapters.

**Required reviews / human approvals**: The project owner approves the contribution-routing and tutorial scope. Human technical review validates current commands, source/package refresh evidence, and the separation between protocol requirements and project policy.

**Expected outputs**:

- Anatomy-of-a-napplet explorer, Conformance Lab, Runtime X-ray, contribution router, protocol design clinic, and dated open-question map.
- Tested build/conformance/publication tutorial, refreshed source/package references, and deterministic lab coverage for the full v1 teaching set.

**Plans**: TBD
**UI hint**: yes

### Phase 9: Optional Portable Napplet Target

**Source phase crosswalk**: Source Phase 8 — Optional Portable Napplet Target

**Goal**: If ADR 0007 authorizes it, users can run an independently packaged Workbench, selected-course, or full-course napplet that never acquires public teaching-host authority.

**Depends on**: Phase 8

**Requirements**: FUTR-01 (conditional v2; excluded from v1 requirement coverage)

**Success Criteria** (what must be TRUE):

  1. When ADR 0007 is `GO-V1`, a user can start the approved portable artifact in a compatible runtime using only its declared current capabilities.
  2. A reviewer can verify that the portable artifact has a separate guest entry, no host-only imports or authority, and parity-tested accessibility and startup behavior.
  3. A user can see simulations labeled as simulations and can inspect the artifact's tested runtime/source baseline, compatibility, bundle, and capability limits.
  4. When ADR 0007 is `GO-LATER`, `WORKBENCH-ONLY`, or `NO-GO`, the project owner can see a documented skip or narrowed scope that does not block the public-site sequence.

**Required reviews / human approvals**: The project owner must explicitly confirm ADR 0007's status before work begins. If it is not `GO-V1`, record the skip or narrowed scope and advance to Phase 10 without treating this phase as a v1 blocker.

**Expected outputs**:

- Conditional separate guest entry and approved portable artifact, or a documented ADR-directed skip/narrowing decision.
- Capability map, no-host-import enforcement, startup/bundle/accessibility tests, compatible-runtime test record, and publication documentation when approved.

**Plans**: TBD
**UI hint**: yes

### Phase 10: Knowledge and LLM Hardening

**Source phase crosswalk**: Source Phase 9 — Knowledge and LLM Hardening

**Goal**: Learners, maintainers, and LLMs can retrieve essential ecosystem knowledge without relying on visual context or separately authored AI-only documentation.

**Depends on**: Phase 9 completed or formally skipped

**Requirements**: KNOW-01, KNOW-02

**Success Criteria** (what must be TRUE):

  1. A reader can retrieve essential definitions, ownership, relationships, maturity/status, and source IDs from human pages and generated machine-readable artifacts derived from common structured content.
  2. An LLM can answer the fixed evaluation set from generated artifacts and return relevant concept and source IDs.
  3. A maintainer can verify that no essential fact appears only in an image or interactive surface and that page Markdown, knowledge JSON, and LLM files use one schema version and source baseline.
  4. A maintainer can apply alias, deprecation, stale-source, and stale-term rules to generated outputs without silently replacing accepted evidence.

**Required reviews / human approvals**: The project owner approves the fixed LLM evaluation set and acceptable retrieval behavior. Human content/evidence review verifies human and machine parity before release hardening begins.

**Expected outputs**:

- Completed versioned concepts, claims, relationships, source-linked page Markdown, knowledge JSON, `llms.txt`, and `llms-full.txt`.
- Evaluation fixtures, parity reports, alias/deprecation rules, and stale-source/stale-term checks.

**Plans**: TBD
**UI hint**: yes

### Phase 11: Quality, Launch, and Maintenance

**Source phase crosswalk**: Source Phase 10 — Quality, Launch, and Maintenance

**Goal**: The public learning product can be released only after its learning, accessibility, security, source-freshness, artifact, and operational evidence passes, with a maintainable process for future truth changes.

**Depends on**: Phase 10

**Requirements**: LEARN-06, SECU-03, A11Y-02, OPER-02

**Success Criteria** (what must be TRUE):

  1. A release reviewer can see that course routes, glossary, source/status pages, labs, and examples meet the accepted accessibility contract through automated and manual evidence.
  2. A release reviewer can verify reviewed public-delivery protections for CSP, editable-code isolation, external-link policy, artifact identity/versioning, rollback, and dependency pin/update policy.
  3. A maintainer can run the release gate and see publication blocked whenever required browser, performance, security, accessibility, content, artifact, source-freshness, learning, or verification evidence fails.
  4. A project owner can review human learning validation with declared personas, sample strategy, observable tasks, scoring rubric, pass thresholds, and an explicit fallback when participants are unavailable.
  5. A maintainer can follow the source-refresh workflow and maintenance runbook while unresolved upstream questions remain visible rather than silently rewritten.

**Required reviews / human approvals**: The project owner gives final release approval after audience-specific content review, source/drift audit, accessibility/browser review, performance review, teaching-host security review, public-site security-policy review, and learning-outcome review all pass or have accepted residual risk.

**Expected outputs**:

- Final quality evidence for accessibility, browsers, performance, security, content, examples, machine outputs, source freshness, and learning outcomes.
- Production deployment/publication, smoke-test record, versioned example napplets, release notes, visible open-question/backlog record, source-refresh workflow, and maintenance runbook.

**Plans**: TBD
**UI hint**: yes

## Progress

**Execution order:** Phases execute in numeric order. Phase 9 is conditional on ADR 0007 and may be formally skipped without blocking Phase 10.

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Research and Truth Baseline | 45/45 | In Progress|  |
| 2. Product and Content Contract | 0/TBD | Not started | - |
| 3. Independent Repository Foundation | 0/TBD | Not started | - |
| 4. Visual and Content Primitives | 0/TBD | Not started | - |
| 5. Real End-to-End Vertical Slice | 0/TBD | Not started | - |
| 6. Core Course and Workbench Expansion | 0/TBD | Not started | - |
| 7. Composition, Patterns, and Application Design | 0/TBD | Not started | - |
| 8. Build, Runtime, and Protocol Contribution | 0/TBD | Not started | - |
| 9. Optional Portable Napplet Target | 0/TBD | Not started — conditional on ADR 0007 | - |
| 10. Knowledge and LLM Hardening | 0/TBD | Not started | - |
| 11. Quality, Launch, and Maintenance | 0/TBD | Not started | - |
