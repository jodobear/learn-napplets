# Delivery Mode Recommendation

## Research question

How should public site, teaching-host labs, Workbench, and course artifact roles be proposed without selecting an architecture or accepting ADR 0007?

## Sources and immutable revisions

`SRC-POLICY-001` and `SRC-POLICY-002` are immutable project-policy records. `CMP-BASELINE-001`, `CLM-CMP-RUNTIME-001`, `CLM-CMP-PACKAGE-001`, `CLM-CMP-EXAMPLE-001`, `DRF-EGRESS-001`, and `OQ-UPSTREAM-BASELINE-001` establish the blocked implementation baseline. The preserved delivery-mode document is archive planning context only, not current upstream proof.

## Observations

The project boundary requires deterministic required paths and a trusted host that mediates authority. The archive proposes: a public site for stable/static learning, a teaching host for declared lab behavior, untrusted focused lab guests, an ADR-gated Workbench, and an ADR-gated course artifact. No current runtime, package, domain, or artifact evidence validates implementation of any host profile.

## Conflicts

Runtime, package, artifact, and egress behavior are blocked. Selecting a boundary harness, verified loader, selected-domain host, composition host, browser integration, or portable build would impersonate an unresolved technical decision.

## Inference

The least-commitment delivery proposal is public-site-first with static, source-status-rich explanations as the safe fallback. A future teaching-host lab may be considered only after evidence and ADR approval. Workbench and course artifacts remain conditional options, not delivery commitments.

## Prototype or measurement

None. No delivery implementation, guest build, or host capability has been exercised.

## Recommendation

Propose these roles only: (1) public site—canonical static lessons and source/status artifacts; (2) teaching-host lab—future trusted, explicitly declared profile; (3) Workbench—optional focused portable architecture tool; (4) course artifact—optional separate guest build. Preserve ADR 0007 options `GO-V1`, `GO-LATER`, `WORKBENCH-ONLY`, and `NO-GO`; do not select one. Safe fallback: static public content plus labeled conceptual simulations and transcripts, with no real domain, host, or guest assertion.

## Uncertainty

Material. Browser viability, host policy, source mapping, domains, artifact shape, package exports, and portable capability degradation remain blocked. Affected decisions require later approved evidence and separate role sign-offs.

## Affected phases and requirements

Phase `01`; Phase 2 product contract; later teaching-host/lab and optional portable work. Requirements: `EVID-03`, `EVID-04`. Decisions: `ADR-0005`, `ADR-0007`, `ADR-0008`. Links: `CMP-BASELINE-001`, `CLM-UPSTREAM-BASELINE-001`, `DRF-EGRESS-001`, `OQ-UPSTREAM-BASELINE-001`.

## Owner and required approval

Owner: research-owner. Required approval: product, protocol-technical, security, accessibility, and content-learning roles as applicable. These are D-25 through D-28 proposals, not accepted ADR outcomes.
