# Phase 1 Research Risks

## Research question

What unresolved risks could invalidate or constrain the proposed static-public-site direction, and who must review each risk before a dependent decision proceeds?

This is a risk synthesis from common canonical records. It does not accept an ADR, convert a local observation into upstream fact, or authorize a production capability.

## Sources and immutable revisions

- `SRC-POLICY-001`: immutable planning-archive/project-policy record, commit `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, digest `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`; material uncertainty.
- `SRC-POLICY-002`: immutable project-policy record, commit `b534103068be8c07e6869bfb7290fb60fdd87c8c`, digest `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`; limited uncertainty.
- Canonical risk inputs: `CMP-BASELINE-001`; `SPK-C-IMPACT-001`, `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, `SPK-H-IMPACT-001`; `DRF-*`; `OQ-*`; `TSCOPE-001`; proposed ADR-0001 through ADR-0011.
- The Plan 01-28 audit remains the authority boundary for spike evidence. Report-only SPK-A/B/E/F/I/J/K/L records are explanatory context, not separate fact sources.

## Observations

| Risk group | State and canonical evidence | Impact | Mitigation or blocked disposition | Owner / required approval | Revisit trigger |
| --- | --- | --- | --- | --- | --- |
| Unresolved upstream source | Blocked: `CLM-UPSTREAM-BASELINE-001`, `OQ-UPSTREAM-BASELINE-001` | Can invalidate terminology, host, runtime, composition, and lesson claims. | Keep protocol-sensitive claims blocked; teach only labeled concepts/simulations. | Research owner / Protocol-technical and content-learning review | Official immutable source identity, revision, locator, digest, retrieval, authority, and claim review arrives or changes. |
| Supply chain / public package | Blocked: `SPK-G-IMPACT-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001` | Unsafe package admission, false conformance, license/integrity exposure. | No install, private/deep/substitute path, or inferred compatibility; static fallback. | Technical owner / Release, security, protocol-technical review | Public release/export/provenance/integrity/license/implementation/conformance bundle or vulnerability/update event. |
| Manifest, identity, verifier | Blocked: `SPK-D-IMPACT-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-VERIFIER-001` | False security assurance, unsafe loader/identity teaching, hand-rolled cryptography risk. | Do not implement or teach verified loading; preserve deterministic fake/static path. | Technical owner / Security and protocol-technical review | Reviewed immutable manifest/identity/verifier provenance and concrete design review. |
| Browser/security/egress | Material/block: `SPK-C-IMPACT-001`, `SPK-H-IMPACT-001`, `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `OQ-EGRESS-NIP-001` | Cross-browser/accessibility and CSP/host claims could be false. | Retain Firefox blocker; no launcher/config/download workaround; proposed CSP remains policy only. | Technical owner / Security, protocol-technical, accessibility review | Separately reviewed attached-context Firefox evidence; immutable egress source; CSP/capability review. |
| Accessibility and editing | Material: ADR-0006/0009 proposed; SPK-J/SPK-I audit context | UI may exclude keyboard, reduced-motion, transcript/table, screen-reader, or static-path users. | Minimum static diagram/transcript/table path; fixed variants before controlled textarea; no editor selection. | UI/technical owner / Accessibility reviewer | Phase 2 criteria, actual assistive-technology observation, approved editor need, or reviewed cross-browser evidence. |
| Delivery and external action | Blocked beyond local: ADR-0003 proposed | Publication/account/credential/target or release claims could bypass review. | Keep local artifacts as evidence only; no deployment/publication/account/credential/network action. | Release owner / Product owner and security review | Explicit named-target authorization with cleanup, retention, credential, security, and release controls. |
| Operational freshness | Material: ADR-0011 proposed, `CLM-POLICY-001` | Stale/ambiguous source could silently affect claims, summaries, or release material. | D-20/D-36 targeted review; preserve old identity; changed/moved/unavailable/ambiguous stays review-required or blocked. | Research owner / Protocol-technical owner | Source revision/path/digest/status change or targeted refresh review work. |
| Product scope / portability | Unselected: `TSCOPE-001`, ADR-0005/0007 proposed | Optional host/portable work could delay or overtake the public static learning path. | Do not select host/operation/portable outcome; static public content remains independently useful. | Product owner / Product, security, accessibility, content-learning review | Phase 2 contract and credible source/browser/value evidence; product chooses a portable outcome. |

## Conflicts

- A product need for interactive authority-boundary teaching conflicts with no selected real operation or host profile; the static simulation fallback resolves scope, not technical truth.
- Bounded Chromium checks exist while Firefox produced no attached context. This is an evidence gap, not a browser result.
- The project can propose a fast static site while package, deploy, and portable capabilities remain blocked; the fast path must not hide their residual risk.
- SPK-J preserves a CodeMirror non-selection and CodeJar blocker only as raw explanatory context. Plan 01-28 prohibits treating that context as a canonical positive package or editor result.

## Inference

The risk register supports a **risk-contained fast path**: a deterministic, static, source-status-rich learning site after Phase 2 approval. It is lower risk because it avoids live external dependencies, package consumption, host authority, external publication, arbitrary learner execution, and optional portability. It is not risk-free: source truth, browser/accessibility, content contract, and human approval still gate it.

## Prototype or measurement

The evidence includes deterministic local fixture and consolidation measurements only:

- `SPK-C-IMPACT-001` / `SPK-H-IMPACT-001`: bounded Chromium observations, Firefox pre-attachment block.
- `SPK-D-IMPACT-001`: byte-integrity observation, no verifier conclusion.
- `SPK-G-IMPACT-001`: zero-operation public-package gate, no package conclusion.
- Plan 01-28: lock-protected deterministic audit/replay inventory.

No measurement establishes an external deployment, live protocol system, public package conformance, cross-browser host profile, portable artifact, or production accessibility outcome.

## Recommendation

- Accept no ADR through this risk document.
- Keep the proposed static public-site path narrow: common structured sources, deterministic explanations/simulations, static/transcript/table equivalents, and visible source/status/uncertainty.
- Treat all optional/complex capabilities as explicit deferrals: host/guest runtime, real operation, manifest/identity/verifier, package, full editor, arbitrary code execution, dynamic controller, portable target, and external deployment.
- Require the listed owner and human approval before a blocked disposition changes. Automation may prepare evidence and targeted refresh review work but must not resolve semantics, accept an ADR, or grant a security exception.

## Uncertainty

**Material.** The common source registry has no current official upstream protocol/package/runtime records. Source volatility is unknown; Firefox has no attached fixture result; actual assistive-technology speech has not been observed; package/export/conformance, manifest/identity/verifier, egress, external deployment, and portable value remain unresolved. The proposed static path is therefore a controlled product recommendation, not a verified implementation or release claim.

## Affected phases and requirements

- **Requirements:** `EVID-02`, `EVID-03`, `EVID-04`, `OPER-01`, `OPER-03`.
- **Phases:** 01 evidence baseline; 02 contract approval; 03 static-site foundation; 05 host/course expansion; optional 08 portability; 11 maintenance/release.
- **Blocked or proposed decisions:** ADR-0003, ADR-0005, ADR-0007, ADR-0008, ADR-0009, ADR-0010, and ADR-0011 remain proposed. The risk ledger does not change their status.

## Owner and required approval

Research owner owns source/drift coordination; technical owner owns package/host implementation proposals; UI/technical owner owns editing scope; accessibility reviewer owns learner-facing accessibility approval; security reviewer owns authority/egress/exception review; release owner owns package and external-delivery review; product owner owns product/portable decisions; protocol/technical owner owns upstream-sensitive source review. Missing approval keeps the corresponding evidence or ADR proposed/blocked.
