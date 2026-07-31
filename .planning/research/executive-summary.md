# Phase 1 Research Executive Summary

## Research question

What can a learner and maintainer responsibly understand today about napplets, sources, authority boundaries, and unresolved implementation work from a single dated evidence baseline?

**Answer:** Learn Napplets now has four immutable 2026-07-31 source records suitable for a status-labeled static explanation. They establish a limited evidence map: one repository-local NAP **draft**, two **observed implementations**, and one optional **native reference**. They do not establish a reviewed NIP-5D protocol baseline, package/runtime/browser compatibility, a teaching host, a portable outcome, or an accepted ADR.

## Sources and immutable revisions

| Source ID | Exact identity | Class / maturity | Safe use |
| --- | --- | --- | --- |
| `SRC-NAPS-NAP-INTENT-20260731` | `napplet/naps@5ac0490461ca6fec2f0d2e45b4835cf9bc08de24:naps/NAP-INTENT.md`; SHA-256 `d6a533ea9c132f0196057c177e87452a7c9edda452fea4b89368afc202b709f0` | Repository-local NAP specification / draft | Explain that a draft names NAP-INTENT and a NIP-5D web binding; do not treat it as direct NIP-5D authority. |
| `SRC-NAPPLET-WEB-20260731` | `napplet/web@03ad65b66413e5798536ef48695ffc4c2508f2c3:README.md`; SHA-256 `f21e5bc41a990e40b72124ca68109b63df40b9850758c4346f151ec328ba7dae` | Official repository observation / implementation-specific | Explain alpha implementation context only. |
| `SRC-KEHTO-WEB-PAJA-20260731` | `kehto/web@d42b3c3da7e0ad3cea233b34458997b09b11960d:packages/paja/README.md`; SHA-256 `dcf02f032bafd87be94297a1995025069df7ff44444b9087d6e1e580ef7e4c33` | Official repository observation / implementation-specific | Explain Paja local authoring/testing and its explicit fixture mode only. |
| `SRC-NAMPLETS-NATIVE-20260731` | `pablof7z/nampplets@1094f1db23292f966fd65757132678406f7ca28c:README.md`; SHA-256 `3d1a5165f97bfdb50d3155bbf04044be6bbe63df91385f8e56f1865de2b8874b` | Optional native-reference observation / implementation-specific | Explain native-reference scope and unratified compatibility state only. |

`SRC-POLICY-001` and `SRC-POLICY-002` remain project-policy/archive records. `OWS-004` keeps mutable PR direction separate from immutable source content.

## Observations

1. **Evidence is the first lesson.** `CLM-NAP-INTENT-20260731`, `CLM-NAPPLET-WEB-20260731`, `CLM-KEHTO-WEB-PAJA-20260731`, and `CLM-NAMPLETS-NATIVE-20260731` are provisional claims with source IDs, maturity, uncertainty, and pending review.
2. **Draft is not final authority.** The NAP-INTENT draft can be described precisely, but its NIP-5D binding does not settle NIP-5D protocol meaning, projection, runtime, or browser behavior.
3. **Implementation is not protocol.** napplet/web and Paja describe implementation contexts. The static site can show those labels and limitations, not turn their README text or mutable PR direction into NAP/NIP law.
4. **Native reference is not a qualification.** Nampplets remains an optional native reference; its unratified compatibility lock cannot prove web/portable/package/conformance support.
5. **The project policy mental model remains safe explanatory content.** A future trusted host owns sensitive/repetitive authority and a future untrusted napplet receives only declared mediated capabilities. This is visible project-policy/conceptual teaching, not a claim that a current runtime is selected or verified.

## Conflicts

- `DRF-INTENT-001` keeps the NAP-INTENT draft and alpha napplet/web implementation sides distinct. The NIP-5D dependency and mutable migration/INTENT PR direction are unresolved.
- `DRF-HANDSHAKE-001` keeps Paja's mandatory shell handshake as an implementation observation; it does not establish a protocol requirement.
- `DRF-ARTIFACT-001` keeps #194 filesystem-named release metadata from becoming package/artifact evidence.
- `DRF-CONFORMANCE-001` keeps the native unratified compatibility state from becoming public conformance proof.
- `CMP-BASELINE-001` keeps protocol, implementation, package, runtime, fixture, current-work, and conformance eligibility visibly blocked.

## Inference

The owner-authorized exception may now deliver a dependency-free static public learning surface in Plan 01-48. It should make the source/status boundary legible, use deterministic static explanations, and derive essential human and machine-readable facts from one structured content source.

The exception is narrow. It does not authorize a framework, package manager, runtime, host/guest execution, package consumption, live service, signer, wallet, deployment, portable artifact, ADR acceptance, or Phase 2 transition.

## Prototype or measurement

No runtime or product prototype is claimed here. The refresh verified four stored immutable blobs and records bounded PR-direction metadata. It ran no package, guest, browser, relay, wallet, signer, or compatibility/conformance operation.

## Recommendation

1. **Build static, labeled learning pages now.** Plan 01-48 may render source IDs, claims, terms, status labels, uncertainty, and blockers from common structured content.
2. **Teach a cautious mental model.** Make the host/guest authority boundary explicitly project-policy/conceptual and pair it with source/status disclosure rather than asserting selected runtime behavior.
3. **Show unresolved work rather than hiding it.** NIP-5D, registry/projection, packages, public artifacts/exports, runtime/browser support, conformance, host selection, portability, and ADRs remain blocked or proposed.
4. **Keep the site deterministic.** Required paths must not depend on a package, framework, external source request, relay, wallet, signer, browser lab, or runtime.
5. **Refresh narrowly.** Re-fetch only when a cited head changes after 2026-07-31, a pinned blob becomes unavailable, or a reviewer asks for a different source scope.

## Uncertainty

**Material.** A draft NAP record, alpha web implementation, Paja implementation, native reference, and mutable PR direction cannot establish a comprehensive protocol/compatibility conclusion. All output must show source/evidence class, maturity, state, uncertainty, and blocker status adjacent to essential protocol-sensitive statements.

## Affected phases and requirements

- **Requirements:** `EVID-01`, `EVID-02`, `EVID-03`, `OPER-01`.
- **Phase 01:** provides the dated source/claim/drift/compatibility baseline and a static-site-safe handoff.
- **Plan 01-48:** may consume the stable source, claim, term, and blocker IDs for a deterministic local static site.
- **Later phases:** retain ownership of product contract, accessibility release criteria, runtime/host behavior, package admission, portability, knowledge hardening, deployment, and release.

## Owner and required approval

Research owner coordinates evidence maintenance. Protocol-technical and content-learning reviewers decide protocol-sensitive meaning; security review is required for authority-boundary claims; product owner owns Phase 2 contract approval; release owner owns package and external delivery decisions. ADRs remain proposed and no automated process may authorize the next phase.
