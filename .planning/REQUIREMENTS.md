# Requirements: Learn Napplets

**Defined:** 2026-07-23  
**Core Value:** Learners can accurately understand and exercise the trusted-host/untrusted-napplet authority boundary.

## v1 Requirements

### Research and Evidence Integrity

- [ ] **EVID-01**: Maintainers can trace every blocking protocol-sensitive claim to an immutable upstream revision, path/locator, digest, retrieval date, authority tier, evidence class, and maturity label.
- [ ] **EVID-02**: Maintainers can see conflicts, uncertainty, known drift, affected requirements/phases, and refresh triggers for each volatile claim.
- [ ] **EVID-03**: Maintainers can review compatibility across selected protocol sources, packages, runtimes, examples, and current work before architecture is accepted.
- [x] **EVID-04**: Decision makers can review measurable mandatory-spike evidence before accepting repository, framework, deployment, content, teaching-host, fixture, or portable-target recommendations.

### Learning and Content Contract

- [ ] **LEARN-01**: Each v1 lesson has audience, objective, prerequisites, source pack, misconceptions, implementation level, static equivalent, and acceptance evidence.
- [ ] **LEARN-02**: Learners can distinguish shell, runtime, runtime internals, capability, projection, archetype, and app-to-app convention using current terminology.
- [ ] **LEARN-03**: Learners can identify trusted and untrusted actors, trace one real request/result, and explain why key authority remains with the host.
- [ ] **LEARN-04**: Learners can select the narrowest appropriate capability/domain and explain graceful degradation when it is absent.
- [ ] **LEARN-05**: Learners can classify proposed changes as protocol, SDK, runtime, content, or application work.
- [ ] **LEARN-06**: Human learning validation uses declared personas, sample strategy, observable tasks, scoring rubric, pass thresholds, and explicit handling when participants are unavailable.

### Host, Guest, and Security

- [ ] **SECU-01**: Developers can run a teaching host where guest napplets cannot access host-only keys, signers, relay pools, wallets, devices, uploads, or policy except through declared mediated capabilities.
- [ ] **SECU-02**: Developers can verify source-window/session identity, request/response envelopes, capability gating, lifecycle, errors, and deterministic service behavior in browser tests.
- [ ] **SECU-03**: Public delivery enforces reviewed CSP, editable-code isolation, external-link policy, artifact identity/versioning, rollback, and dependency pin/update policy.
- [ ] **SECU-04**: Required labs use fake or deterministic external systems and never expose real signing keys.

### Accessible Learning Experience

- [ ] **A11Y-01**: Every essential interactive diagram or lab has keyboard operation, deterministic reset/replay, transcript/state inspection, static explanation, and reduced-motion behavior.
- [ ] **A11Y-02**: Course routes, glossary, source/status pages, labs, and examples meet the accepted accessibility contract and automated/manual checks.
- [ ] **A11Y-03**: Content remains usable without live network access for all required learning paths.

### Labs and Examples

- [ ] **LABS-01**: Developers can run, modify, test, and understand at least three real v1 lab napplets without undocumented host behavior.
- [ ] **LABS-02**: Learners can use deterministic architecture, capability, identity, composition, and conformance labs tied to current evidence.
- [ ] **LABS-03**: Each published example declares teaching-host profile, required capabilities, source identity, compatibility, limitations, and real-versus-simulated behavior.

### Knowledge and Operations

- [ ] **KNOW-01**: Human pages and machine-readable artifacts derive essential definitions, ownership, relationships, status, and source IDs from common structured content.
- [ ] **KNOW-02**: An LLM can answer the fixed evaluation set using generated artifacts and return relevant concept/source IDs.
- [ ] **OPER-01**: Maintainers can detect upstream source/package/runtime drift, map impact, and create review work without silently rewriting accepted claims.
- [ ] **OPER-02**: Release is blocked when required browser, performance, security, accessibility, content, artifact, source-freshness, learning, or verification gates fail.
- [x] **OPER-03**: Every phase has explicit owner/approver roles, measurable exit evidence, GSD verification status, and traceability to requirements.

## v2 Requirements

- **FUTR-01**: Learners can use a portable Workbench napplet if ADR 0007 authorizes it.
- **FUTR-02**: Learners can opt into live Nostr mode without making it required for course completion.
- **FUTR-03**: Advanced device, value, and media labs extend the deterministic core.
- **FUTR-04**: A generalized AI tutor can use accepted structured knowledge outputs.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Canonical protocol specification | Upstream projects remain authoritative |
| Complete Nostr curriculum | Product teaches only prerequisite concepts |
| Exhaustive package API reference | Package docs remain source authority |
| Production wallet or signer | Unsafe and outside learning core |
| Mandatory live external services | Breaks deterministic learning/accessibility |
| Full-course napplet required for v1 | Optional target cannot block public site |

## Traceability

Each v1 requirement has exactly one owning phase. Supporting work in other phases is non-owning and does not duplicate this mapping.

| Requirement | Owning Phase | Status |
|-------------|--------------|--------|
| EVID-01 | Phase 1 | Pending |
| EVID-02 | Phase 1 | Pending |
| EVID-03 | Phase 1 | Pending |
| EVID-04 | Phase 1 | Complete |
| LEARN-01 | Phase 2 | Pending |
| LEARN-02 | Phase 6 | Pending |
| LEARN-03 | Phase 5 | Pending |
| LEARN-04 | Phase 6 | Pending |
| LEARN-05 | Phase 8 | Pending |
| LEARN-06 | Phase 11 | Pending |
| SECU-01 | Phase 5 | Pending |
| SECU-02 | Phase 5 | Pending |
| SECU-03 | Phase 11 | Pending |
| SECU-04 | Phase 5 | Pending |
| A11Y-01 | Phase 4 | Pending |
| A11Y-02 | Phase 11 | Pending |
| A11Y-03 | Phase 3 | Pending |
| LABS-01 | Phase 7 | Pending |
| LABS-02 | Phase 8 | Pending |
| LABS-03 | Phase 7 | Pending |
| KNOW-01 | Phase 10 | Pending |
| KNOW-02 | Phase 10 | Pending |
| OPER-01 | Phase 1 | Pending |
| OPER-02 | Phase 11 | Pending |
| OPER-03 | Phase 1 | Complete |

### Cross-Phase Support (Non-Owning)

| Owning Requirement | Supporting Phases | Support relationship |
|--------------------|-------------------|----------------------|
| EVID-01–EVID-04, OPER-01 | Phases 2–11 | Accepted evidence, source labels, drift triggers, and compatibility baselines govern later work. |
| OPER-03 | Phases 2–11 | Each phase records its own reviews, approval evidence, verification status, and outputs using the Phase 1 governance convention. |
| LEARN-01 | Phases 3–11 | The approved lesson/lab contract constrains implementation, validation, knowledge hardening, and release. |
| A11Y-01 | Phases 5–11 | The accessible primitive contract is applied to later labs, examples, and route additions. |
| A11Y-03 | Phases 5–11 | The static-first and deterministic foundation is preserved as required paths expand. |
| SECU-01, SECU-02, SECU-04 | Phases 6–11 | The Phase 5 teaching-host controls and deterministic-fixture constraints apply to later labs and release review. |
| LABS-01, LABS-03 | Phases 8, 11 | The three-lab set and example declarations are refreshed for contribution teaching and release validation. |
| KNOW-01, KNOW-02 | Phase 11 | Generated knowledge outputs are checked as release artifacts. |

**Coverage:**

- v1 requirements: 25
- Mapped to one owning phase: 25
- Unmapped: 0
- Duplicate ownership: 0

*Note: the prior aggregate count stated 24, but the enumerated v1 IDs total 25.*

## Definition of Done

A requirement is complete only when implementation or evidence exists, automated checks pass, required human checks pass, canonical verification records the result, and the owning approver accepts any residual risk.

---
*Requirements defined: 2026-07-23*  
*Last updated: 2026-07-23 after source-plan-aligned roadmap initialization*
