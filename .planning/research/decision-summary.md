# Phase 1 Decision Summary

## Research question

Which decision-maker actions are supported by common Phase 1 evidence, what remains blocked, and what is the smallest path that preserves a deterministic public learning product without converting a proposal into acceptance?

**Decision state:** every ADR remains **proposed**. The evidence supports a reviewable fast-track direction, not an approved implementation: after Phase 2 product/content-contract approval, build a static public learning site from common structured sources and defer optional/complex capabilities that need source, browser, supply-chain, security, accessibility, or product evidence.

## Sources and immutable revisions

The decision summary uses only canonical structured records and previously proposed ADRs:

- `SRC-POLICY-001` (`c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, archive path and digest `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`) is planning-archive/project-policy context, not upstream proof.
- `SRC-POLICY-002` (`b534103068be8c07e6869bfb7290fb60fdd87c8c`, evidence-policy path and digest `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`) is project policy, not upstream proof.
- Claims, compatibility, drift, open questions, `TSCOPE-001`, delivery-mode recommendation, and Plan 01-28 audit/replay data are the shared record layer. Cited `CLM-*` records resolve to complete immutable `SRC-*` records; blocked claims are rendered as blockers, never as inferred facts.
- Consolidation-issued records are `SPK-C-IMPACT-001`, `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, and `SPK-H-IMPACT-001`. Their audit rerun-input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`.

## Observations

| Decision area | Evidence category/state | Canonical record(s) | Decision-maker reading |
| --- | --- | --- | --- |
| Mental model and terms | Project policy; upstream behavior blocked | `CLM-POLICY-001`, `CLM-UPSTREAM-BASELINE-001` | Teach explicit authority-boundary and evidence labels as project/simulation concepts; do not state protocol behavior. |
| Disputes and source status | Blocked conflict/review work | `CMP-BASELINE-001`, `DRF-*`, `OQ-UPSTREAM-BASELINE-001` | Preserve parallel records and uncertainty; do not collapse differences into a technical winner. |
| First real operation / host | Not selected | `TSCOPE-001`, ADR-0005 proposed | Use static conceptual simulations; no real domain operation or host profile is selected. |
| Public surfaces / package | Supply-chain blocker | `SPK-G-IMPACT-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001` | No package version/export is consumable; no private/deep/substitute path. |
| Browser / security | Local observation plus blocker | `SPK-C-IMPACT-001`, `SPK-H-IMPACT-001`, `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` | Chromium fixture observations are local only; Firefox remains blocked; no production CSP or host conclusion. |
| Portability | Product outcome unselected | ADR-0007 proposed | Keep `GO-V1`, `GO-LATER`, `WORKBENCH-ONLY`, and `NO-GO` open; do not block the public site. |
| Editing | Explanatory local context; canonical browser blocker | Plan 01-28 SPK-J no-impact entry; `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` | Fixed variants/controlled textarea are proposed least-authority direction; CodeMirror is not selected and CodeJar remains blocked. |
| Freshness | Project-policy proposal; live semantics unknown | ADR-0011 proposed, `CLM-POLICY-001`, `OQ-UPSTREAM-BASELINE-001` | Use targeted review work, retain old identity, and require human meaning review; do not auto-change records. |

## Conflicts

- The desired public learning experience includes authority-boundary concepts, but source evidence does not select a runtime, host profile, composition model, manifest/identity mapping, or verifier.
- Chrome-only fixture observations conflict with the requirement for cross-browser confidence because Firefox never attached; no workaround is evidence.
- A public static site can be proposed independently of package/portable/deployment evidence; treating the static direction as a substitute for those proofs would be incorrect.
- Raw report observations can explain recommendations but Plan 01-28 allows only the four consolidation-issued fragments to provide canonical spike impact evidence.

## Inference

**Smallest evidence-supported path to a Phase 3 working static learning site:**

1. Obtain the separate Phase 2 product/content-contract approval.
2. Use a public-site-first repository direction and a static-first site candidate only as proposed ADR inputs; do not scaffold before authorization.
3. Render essential facts from one structured record with source/claim/status/maturity/uncertainty parity for human and LLM outputs.
4. Deliver deterministic static lessons, source-status-rich conceptual simulations, transcript/table/static equivalents, and accessible reasoning interactions.
5. Keep all required learning paths independent of live sources, relays, wallets, signers, packages, verifiers, guests, and external deployment.

This inference exposes a fast path while preserving residual risk. It does not accept ADR-0001 through ADR-0011, select Astro, select a host, accept an editor, authorize a package, or approve a Phase 2 transition.

## Prototype or measurement

- The consolidation transaction verified evidence accounting and byte-stable reruns; it did not validate an application.
- `SPK-G-IMPACT-001` observed a zero-operation dependency-free blocker, not package conformance.
- `SPK-D-IMPACT-001` observed fixture byte integrity, not verifier/loader correctness.
- `SPK-C-IMPACT-001` and `SPK-H-IMPACT-001` preserve local fixture conditions and Firefox absence, not browser compatibility.
- Report-only spikes remain explanatory context. In particular, SPK-J preserves fixed-variant/CodeMirror/CodeJar context, and SPK-L preserves local refresh-routing context, without canonical positive targets.

## Recommendation

| Proposed direction | Evidence/state | Owner / required approval | Explicit deferral and revisit trigger |
| --- | --- | --- | --- |
| Minimal static public site | ADR-0001/0002/0004/0006 proposed; `TSCOPE-001` safe fallback | Product owner approves Phase 2 contract; technical/content/accessibility review | Defer scaffold/framework selection until approval; reopen for contract, source, accessibility, or static-equivalence changes. |
| Structured human/LLM parity | ADR-0004 proposed; `CLM-POLICY-001` | Content/technical owner; Product owner | Defer renderer/schema implementation; reopen for missing parity field, second source, or source-record change. |
| Bounded editing only | ADR-0009 proposed; SPK-J audit context; Firefox blocker | UI/technical owner; Accessibility reviewer | Defer CodeMirror, CodeJar, arbitrary execution; reopen for approved learning need and reviewed cross-browser/accessibility/package evidence. |
| Public package/version policy | ADR-0010 proposed; `SPK-G-IMPACT-001` blocked | Technical owner; Release owner | Defer all package consumption; reopen only with official release/export/provenance/integrity/conformance evidence or a security/update event. |
| Targeted source freshness review | ADR-0011 proposed; `CLM-POLICY-001` | Research owner; Protocol/technical owner | Defer cadence and automatic mutation; reopen for source identity/state change or review-work result. |
| Optional host/guest, portable, external delivery | ADR-0003/0005/0007/0008 proposed; canonical blockers | Respective technical/product/release/security roles | Defer implementation; reopen only with approved source/browser/security/accessibility/product evidence. |

## Uncertainty

**Material and decision-relevant.** No official immutable upstream baseline establishes protocol/runtime/package/host behavior. The following remain visible blockers: Firefox attachment, public package/export/conformance, manifest, identity, verifier provenance, browser egress semantics, VitePress reduced-motion/static-equivalent evidence, CodeJar identity conflict, external deployment limit, actual assistive-technology observation, and portable outcome. A static site direction is a scope-control proposal, not evidence that later capabilities are unnecessary or impossible.

## Affected phases and requirements

- **Requirements:** `EVID-02`, `EVID-03`, `EVID-04`, `OPER-01`, `OPER-03`.
- **Phase 01:** preserves canonical evidence, proposed ADRs, and review work.
- **Phase 02:** must define and receive approval for the product/content contract before the fast path begins.
- **Phase 03:** may be the earliest future static-site foundation only after the applicable gates; no current scaffold is authorized.
- **Phase 05 / optional 08 / Phase 11:** retain host, package, portability, freshness, and release work as conditional/deferred.

## Owner and required approval

Research owner owns canonical evidence maintenance. Product owner owns product-contract and portable outcome approval; protocol/technical owner owns protocol-sensitive source review; accessibility reviewer owns learner-facing accessibility review; security reviewer owns authority/CSP/exception review; release owner owns package/update and external-delivery review. All ADRs remain proposed until the named human approver accepts a concrete decision; automation must not make that transition.
