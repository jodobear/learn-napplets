# ADR 0003 — Deployment/publication

- **Status:** proposed
- **Date:** 2026-07-24
- **Owners:** Release owner (responsible); research-owner supplies evidence context.
- **Required approver:** Product owner; consult Security reviewer and Technical owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 03 independent repository foundation; 11 quality, launch, and maintenance.
- **Source refs:** SRC-POLICY-001, SRC-POLICY-002; CLM-UPSTREAM-BASELINE-001; CMP-BASELINE-001; DRF-METADATA-001; OQ-UPSTREAM-BASELINE-001.
- **Evidence IDs:** SPK-K-DEPLOYMENT; CMP-BASELINE-001; CLM-CMP-PACKAGE-001; DRF-METADATA-001; OQ-UPSTREAM-BASELINE-001; SPK-K-BLOCKED-EXTERNAL-AUTHORIZATION-MISSING.
- **Impacts:** Requirements EVID-03, EVID-04, OPER-03; phases 01, 02, 03, and 11.
- **Governance:** Status: proposed. No external deployment, publication, release, account operation, credential use, or provider choice is authorized by this record.

## Context

The project will eventually need separately accountable public-site, lab-artifact, and optional portable-output delivery paths, with artifact integrity and rollback evidence. Phase 1 is restricted to local, disposable evidence. Its outcome must not be mislabeled as an externally reachable preview, publication, or release.

## Upstream facts

No current immutable upstream deployment, runtime, public package/export, manifest, identity, verifier, or portable-target baseline supports a delivery choice. `CLM-UPSTREAM-BASELINE-001` and `OQ-UPSTREAM-BASELINE-001` retain that absence as blocked review work. `CMP-BASELINE-001` remains blocked, including public package evidence (`CLM-CMP-PACKAGE-001`).

`DRF-METADATA-001` is blocked because an immutable registry/projection baseline is absent; it cannot establish artifact metadata or publication behavior. `SRC-POLICY-001` is a revision-pinned planning archive and `SRC-POLICY-002` is revision-pinned project policy. Both specify evidence discipline but are not upstream hosting or publication authority.

## Local decision boundary

Whether to assemble local artifacts, use a named provider, publish a public site, issue a lab artifact, or release a portable build is a Learn Napplets operational decision. Until an external action is explicitly authorized, the project may retain local artifact evidence only. This ADR does not choose a provider, target, domain, account, credential, production CSP, host profile, or release identity.

## Options

**Alternatives:** Option A, Option B, and Option C below remain reviewable; none is accepted by this record.

### Option A — Retain local-only artifact evidence as the proposed baseline

Keep three distinct static fixture categories—public-site, lab artifact, and optional portable output—digest-pinned, inspected locally, isolated in the disposable spike directory, and rolled back. Use this only as future delivery-design input.

### Option B — Defer all delivery-path recommendations

Retain no candidate direction until an authorized named disposable-sandbox probe and immutable public delivery evidence are collected. This avoids provisional operational direction but prevents later reviewers from using the observed local integrity/rollback discipline.

### Option C — Authorize a future named sandbox probe only through a new approval

After explicit authorization, conduct a bounded external probe with a named target, exact command, cleanup/retention plan, credential handling, owner, dated security and release sign-offs, and result-digest policy. This is not authorized now and must not be implied by this ADR.

## Evidence

**Canonical evidence and provenance.** The Plan 01-28 consolidation audit records SPK-K as explanatory `no-impact-fragment` context: report SHA-256 `923d3085c176dbdb83603d283f4f4ddaf0128eab90244ccbd8e20fefd42dd594`, metadata SHA-256 `2bfba0fc63e9a775fb7d36b86037f9f5b679cba75a23e267aec25f6ce998b26c`, and measurements SHA-256 `8b0f2c8f997427e9677c989c80a78586cf45f0b4d4c8a06b7f740bb6cb1a2b70`. The consolidation rerun input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`; it expressly does not turn report prose into upstream fact.

**Observed local implementation behavior.** SPK-K recorded a project-operator `local-only` decision on 2026-07-24. Its replay performed zero external operations, account/credential access, target lookup, listener start, deployment, publication, or writes outside its disposable output directory. It assembled, SHA-256-verified, path-isolation-checked, and rolled back three fixtures (452 aggregate payload bytes); its post-verification replay digest was `f9d777acf32478dfe5e4ca69b96280e89b0cc045d6c97b9db603f42635033aaa`. This is local artifact-integrity observation only.

**Project policy.** `SRC-POLICY-002` / `CLM-POLICY-001` require reviewed evidence before verification. Existing policy prohibits an external write without explicit authorization. `CLM-UPSTREAM-BASELINE-001` blocks claims about upstream/runtime delivery behavior until a current immutable source is reviewed.

**Inference.** The local evidence supports keeping the three categories distinct and requiring digest, isolation, and rollback checks in a later delivery design. It cannot support provider, public reachability, deployment, publication, release, or portable compatibility claims.

## Decision

**Proposed recommendation only:** retain Option A as the minimum local delivery-evidence baseline and preserve Option C as a gated future evidence-collection path. Do not execute external actions, configure deployment infrastructure, create an account, use credentials, or change ADR status. Product-owner approval and separately dated security/release authorization are required before any external probe.

## Host/guest implications

The public site, host-backed lab artifact, and optional portable guest output must remain separate categories if later delivery work begins. This local fixture does not prove a trusted host, guest sandbox, browser containment, mediator, deployment CSP, runtime compatibility, or portable target. Firefox Playwright attachment remains blocked; package/public-export, manifest, identity, and verifier gaps remain blocked; no delivery evidence resolves them.

## Human/LLM implications

A future public delivery path must surface artifact/source/status evidence to human readers and machine outputs from the accepted common structured source. The local SPK-K fixture neither creates a content pipeline nor demonstrates public artifact discoverability, LLM retrieval, or that a generated file is suitable for release.

## Consequences

- Preserves a traceable local integrity, isolation, and rollback pattern without inventing external delivery evidence.
- Makes external authorization, target naming, security/release review, cleanup, and credential policy explicit prerequisites.
- Prevents the optional portable target from becoming a public-site dependency.
- Defers provider configuration and release identity until evidence and approval exist.

## Risks

- Local static files could be mistaken for a hosted preview or an authorized publication.
- A future external probe without named-target, cleanup, retention, credential, security, and release controls could create avoidable operational exposure.
- Unresolved package/manifest/identity/verifier and portable-target evidence can invalidate any delivery assumption beyond local artifact handling.

## Uncertainty

**Uncertainty:** Material.

**Material.** The SPK-K local-only replay cannot establish provider behavior, public reachability, hosting configuration, runtime compatibility, a real lab artifact, portable compatibility, or release identity. `CMP-BASELINE-001`, `DRF-METADATA-001`, and `OQ-UPSTREAM-BASELINE-001` remain blocked. External deployment has not been tested.

## Revisit triggers

- **Revisit trigger:** a product owner explicitly authorizes a named disposable external target with dated security and release sign-offs, exact command, cleanup/retention, credential, and digest policies.
- Immutable public hosting, package/export, runtime, identity, manifest, verifier, or portable-target evidence is collected and reviewed.
- The Phase 2 contract changes delivery categories, deterministic-path requirements, or the public-site/guest separation.
