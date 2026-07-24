# ADR 0010 — Package versioning

- **Status:** proposed
- **Date:** 2026-07-24
- **Owners:** Technical owner (responsible); research owner supplies evidence context.
- **Required approver:** Release owner; consult Protocol/technical owner, Security reviewer, Accessibility reviewer, Content/learning owner, and Product owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 03 public static site; 05 teaching-host work; 11 quality, launch, and maintenance.
- **Source refs:** `SRC-POLICY-001`, `SRC-POLICY-002`; `CLM-CMP-PACKAGE-001`, `CLM-UPSTREAM-BASELINE-001`; `CMP-BASELINE-001`; `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`; `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`.
- **Evidence IDs:** `SPK-G-IMPACT-001`; `CMP-BASELINE-001`; `CLM-CMP-PACKAGE-001`; `DRF-ARTIFACT-001`; `DRF-CONFORMANCE-001`; `OQ-PUBLIC-PACKAGE-BASELINE-001`; `OQ-PUBLIC-CONFORMANCE-001`.
- **Impacts:** Requirements `EVID-03`, `EVID-04`, `OPER-03`; phases 01, 02, 03, 05, and 11.
- **Governance:** Status: proposed. This record approves no package, version, package manager operation, dependency manifest, public export, private import, substitute package, or production scaffold.

## Context

Later work may need a repeatable package version/update policy, but the Phase 1 public-site fast path should not depend on a napplet package. Changing a package policy after authoring, build, security, and release workflows exist is costly because version, integrity, provenance, compatibility, and stale-state handling must move together.

## Upstream facts

No current immutable official public `napplet/web` release, exact version, registry integrity value, license, documented root export, implemented-source revision, browser claim, or public conformance target is recorded. `CLM-CMP-PACKAGE-001` is a blocked project-policy claim that makes that absence auditable; it is not a claim that a package is unavailable in general or that any substitute is safe.

`SPK-G-IMPACT-001` is consolidation-issued canonical evidence. It retains the dependency-free blocked gate and links through complete `SRC-POLICY-001` and `SRC-POLICY-002` records. `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, and `OQ-PUBLIC-CONFORMANCE-001` keep the release/public-export/conformance gaps open for review.

## Local decision boundary

How Learn Napplets admits, pins, updates, reviews, or removes a future dependency is project supply-chain and release policy. It cannot establish upstream package behavior or waive the need for exact public provenance. It also cannot turn a project-policy source, a private monorepo path, an unpublished build, a deep import, or a zero-operation gate into a package compatibility result.

## Options

**Alternatives:** all options remain reviewable; none is accepted by this record.

### Option A — Propose a public-evidence gate before package admission and every update

Before a future dependency is considered, require a complete public release/version, integrity and provenance, license, documented root export, distinct immutable implemented-source baseline, compatibility comparison, and required human review. Record version, digest, source locator, update impact, and rollback/revisit trigger together. If the evidence is incomplete, retain a dependency-free/static fallback.

### Option B — Defer package policy until a Phase 2/3 dependency is approved

Do not propose an admission/update policy until an accepted product/content contract identifies a concrete dependency need. This minimizes policy commitment but leaves later reviewers without a reusable evidence gate.

### Option C — Consume a private/deep/substitute path or infer conformance from installation/compilation

Use a private monorepo, workspace, `src/`, `dist/`, deep path, unpublished build, similarly named package, or compile result as a substitute. This is blocked by the canonical package/public-conformance records and is not an acceptable versioning route.

## Evidence

**Canonical evidence and provenance.** `SPK-G-IMPACT-001` pins report SHA-256 `5f1993cbff951b4ae68508806f7b48f841198b31e9fa91b7c4c575c546963e86`, metadata SHA-256 `8a0a91e7a70a77466aa3942cdc2e6c59a5350df98a59606ecd68a3d315f8195c`, and measurement SHA-256 `aba6aa72bfcdf68498c90108314e2464a0e195086412bb090e91917255fed59b`. Plan 01-28's rerun-input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`. Its source and claim links resolve to complete immutable project-policy records; they establish the blocked evidence path, not package functionality.

**Observed implementation behavior.** The canonical SPK-G hand-off retains five dependency-free local gate replays that performed zero releases, installs, imports, package executions, browser operations, or conformance runs. This observation proves only supply-chain restraint under the recorded gate; it is not package compatibility, availability, or conformance success.

**Project policy and inference.** `SRC-POLICY-002` and `CLM-POLICY-001` require immutable identity and human review. The safest proposed inference is Option A: package admission and update should remain blocked until the public evidence bundle is complete, and the smallest website path should remain dependency-free with respect to the blocked napplet package.

## Decision

**Proposed recommendation only:** carry Option A into Phase 2/3/11 release review. Do not select a public package version, run a package manager, create a manifest, approve CodeJar or another substitute, or accept this ADR in Phase 1. The minimal static site path may proceed after its own approvals without a napplet package; optional host/package work remains deferred.

## Host/guest implications

A future guest or host cannot acquire authority through an unreviewed dependency. Any later package-backed integration must remain distinct from host policy, declare capabilities, preserve deterministic static alternatives, and pass separate security, accessibility, and protocol review. This ADR does not select a loader, verifier, manifest/identity rule, runtime, or guest package export.

## Human/LLM implications

Human and machine-readable dependency records must expose the exact version, release integrity, source revision/path/locator, evidence class, compatibility state, uncertainty, approval, and update/replay status from common structured records. A README claim, rendered package name, or transient install output is not sufficient evidence.

## Consequences

- Keeps the Phase 3 static-site direction free of the blocked public-package surface.
- Makes supply-chain admission and update decisions attributable and reviewable rather than implicit package-manager actions.
- Preserves public-package, root-export, provenance, integrity, manifest, identity, verifier, and conformance gaps as blockers.
- Defers package-driven host/guest integration until complete evidence and approval make its maintenance cost justified.

## Risks

- A blocked zero-operation gate could be misread as package compatibility or a permanent ecosystem conclusion.
- A private/deep/substitute import could bypass public provenance, integrity, licensing, and review controls.
- Updating only a version string without synchronized source/compatibility/replay review could create stale or untraceable claims.
- Package use could obscure unresolved manifest, identity, verifier, browser, and public-conformance risks.

## Uncertainty

**Uncertainty:** Material.

Package identity, public export, version, integrity, provenance, license, implementation revision, browser support, release/current-work divergence, and conformance remain unresolved. `SPK-G-IMPACT-001`, `CMP-BASELINE-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`, and their blocked open questions do not supply a positive package-selection result.

## Revisit triggers

- **Revisit trigger:** a complete official public release/version, integrity, provenance, license, documented root export, and distinct immutable implementation baseline is collected and reviewed.
- A public conformance target/fixture and compatible browser/runtime evidence are recorded, or any referenced release, export, source revision, digest, or license changes.
- A vulnerability, revocation, deprecation, ownership/provenance change, dependency-closure review result, or update measurement invalidates the recorded package evidence.
- Phase 2/3/11 approves a concrete package need and a release owner plus the required security/protocol/accessibility reviewers approve the associated update and rollback plan.
