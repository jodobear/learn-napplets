# ADR 0001 — Repository/workspace

- **Status:** proposed
- **Date:** 2026-07-24
- **Owners:** Technical owner (responsible); research-owner supplies evidence context.
- **Required approver:** Product owner; consult Security reviewer and Release owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 03 independent repository foundation.
- **Source refs:** SRC-POLICY-001, SRC-POLICY-002; CLM-UPSTREAM-BASELINE-001; CMP-BASELINE-001; DRF-DISCOVERY-001; OQ-UPSTREAM-BASELINE-001.
- **Evidence IDs:** SPK-A-WORKSPACE; CMP-BASELINE-001; CLM-UPSTREAM-BASELINE-001; DRF-DISCOVERY-001; OQ-UPSTREAM-BASELINE-001.
- **Impacts:** Requirements EVID-03, EVID-04, OPER-03; phases 01, 02, and 03.
- **Governance:** Status: proposed. This record is a recommendation for later human review, not an acceptance, rejection, or authorization to create a workspace.

## Context

Phase 3 will need repository boundaries that keep a public teaching site, structured content, trusted host-only authority, and guest napplet entries distinct. Phase 1 may compare candidates but cannot create a production workspace or select an implementation before the product/content contract and required approval.

## Upstream facts

No current immutable upstream repository, runtime, package, or protocol fact supports a workspace selection. `CLM-UPSTREAM-BASELINE-001` records that the absence of reviewed official immutable sources blocks such a conclusion. `SRC-POLICY-001` is a revision-pinned planning archive and `SRC-POLICY-002` is a revision-pinned project evidence policy; both are project-policy evidence, not upstream protocol authority.

`CMP-BASELINE-001` is explicitly blocked: its package, runtime, example, and fixture inputs remain unresolved. `DRF-DISCOVERY-001` and `OQ-UPSTREAM-BASELINE-001` preserve the missing official discovery/runtime/package baseline as review work rather than a fact about how napplet systems behave.

## Local decision boundary

Whether later Learn Napplets work uses distinct public-site, structured-content, trusted-host, and guest-entry boundaries is a project architecture choice. Naming those boundaries does not select a package manager, framework, bundler, deployment provider, runtime profile, or protocol behavior. Any implementation is deferred until ADR review, the Phase 2 contract, and Phase 3 authorization.

## Options

**Alternatives:** Option A, Option B, and Option C below remain reviewable; none is accepted by this record.

### Option A — Narrow public-site-first boundary model

Propose a smallest future workspace with separately named public-site, structured-content, trusted-host, and multiple guest-entry boundaries. This is the SPK-A candidate that tied for the highest local structural score while minimizing immediate workspace breadth.

### Option B — Defer all workspace shape

Retain only the research evidence and wait for immutable runtime/package/deployment evidence before proposing any boundary model. This minimizes early commitment but leaves Phase 2 without a concrete reviewable direction.

### Option C — Broader future-workspace model

Keep SPK-A Candidate C as an equally scored alternative that anticipates a broader later workspace. It remains an alternative, not a selected architecture, and should be reconsidered if Phase 3 scope requires boundaries beyond the static-first public site.

## Evidence

**Canonical evidence and provenance.** The Plan 01-28 consolidation audit records SPK-A as an explanatory `no-impact-fragment` input, with report SHA-256 `5a3d445a81ceb49c1335abbd6ee5abb33b6027b6327763d20fba273608e90e4b`, metadata SHA-256 `f93a8a6f9f4e219967a5cb12aca222da352c58054797cb47dffb0ef46cc44573`, and measurements SHA-256 `aa24ff4fec4f52c4bcdb7e28c62b0357e386472b36fdc581425e5a546af2a44e`. The consolidation rerun input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`. Its audit expressly says report prose is not an asserted upstream fact.

**Observed local implementation behavior.** The disposable SPK-A text-fixture comparison produced five passing local assertions; Candidates A and C each scored 7/7 and Candidate B scored 0/7. No production marker was created. This is a bounded local structural observation, not upstream behavior or an implementation feasibility result.

**Project policy.** `SRC-POLICY-002` and `CLM-POLICY-001` require immutable source identity and human review before a claim is verified. `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` require deferral of upstream-sensitive conclusions pending reviewed immutable sources.

**Inference.** Subject to those limits, Candidate A is the smallest evidence-supported direction for future public-site-first review. That inference does not prove a runtime, compatibility, package, or deployment choice.

## Decision

**Proposed recommendation only:** carry Option A into Phase 2/3 review as the narrowest public-site-first workspace boundary model; preserve Option C as a costly-to-reverse alternative. Do not materialize directories, install packages, select a framework, or alter ADR status in Phase 1. Product-owner acceptance remains required.

## Host/guest implications

If later approved, the boundary model gives the public teaching host a named location separate from untrusted guest entries and makes structured content shareable without granting guest code host authority. It does not establish a host profile, guest sandbox behavior, mediated capability, portable target, package export, or browser compatibility. Those remain blocked by the canonical baseline and related open questions.

## Human/LLM implications

A separately named structured-content boundary supports the project goal that essential facts derive from common records for human and machine outputs. It does not authorize a renderer, source schema, LLM export, or a second authoring source; ADR 0004 and the Phase 2 content contract govern those decisions.

## Consequences

- Gives later reviewers a narrow, evidence-labeled boundary proposal rather than an implied scaffold.
- Preserves the broader Candidate C alternative without presenting its breadth as required.
- Keeps architecture, runtime, package, deployment, protocol, and teaching-host conclusions outside this ADR's evidence.
- Revising the boundary after Phase 3 is costly because later build and import interfaces would need coordinated migration.

## Risks

- Treating a local text comparison as compatibility or upstream proof would misrepresent the evidence.
- Treating this proposal as approval could bypass the product-owner and Phase 2 gates.
- The unresolved package, manifest, identity, verifier, portable-target, and official-baseline gaps may require a different later boundary.

## Uncertainty

**Uncertainty:** Material.

**Material.** `CMP-BASELINE-001`, `DRF-DISCOVERY-001`, and `OQ-UPSTREAM-BASELINE-001` remain blocked. SPK-A has no canonical impact fragment, so its measurements are digest-pinned explanatory context only. No current immutable upstream runtime/package/deployment evidence establishes feasibility.

## Revisit triggers

- **Revisit trigger:** an immutable runtime, package, deployment, or official discovery baseline is collected and reviewed, or its revision/path/digest changes.
- Phase 2 changes the accepted product/content contract or Phase 3 changes the workspace/scaffold boundary.
- A reviewed measurement demonstrates that Candidate A cannot maintain public/host/guest/content separation, or that Candidate C is required.
