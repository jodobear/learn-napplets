# Lesson Research Packet — Identity and Distribution

- **Lesson ID:** LES-007
- **Primary audience:** Developers new to Nostr, runtime implementers, and security-minded learners.
- **Prerequisites:** LES-002 through LES-005; understand that terminology and a note-shaped fixture do not establish an identity or distribution rule.
- **Last researched:** 2026-07-24

## Learner question

What can learners say about identity and distribution questions while manifest, `dTag`, artifact, verifier, and runtime evidence remain unresolved?

## Intended outcome

Learners can identify identity and distribution as separate evidence questions, trace each unresolved term to a canonical drift/open-question record, and refuse to infer identity, package, manifest, or publication behavior from archive prose, a local digest, or an illustrative fixture.

## Current terminology

- **Identity** is a research topic, not a current mapping rule in this packet.
- **`dTag` identity** is an unresolved term governed by `CLM-DRF-IDENTITY-NORMATIVE` with source `SRC-POLICY-002`; its unresolved official-source search and impact are recorded by `OQ-VERIFIED-LOADER-IDENTITY-001`.
- **Manifest** is an unresolved source/resolver question governed by `CLM-DRF-MANIFEST-NORMATIVE` with source `SRC-POLICY-002` and `OQ-VERIFIED-LOADER-MANIFEST-001`.
- **Distribution** is a learning label for public artifact, package, or runtime provenance questions; it does not identify a published package, registry, export, or release behavior.
- **Exact-byte local digest** is fixture-integrity evidence only, not proof of signature, blob, aggregate, loader, identity, or artifact conformance behavior.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-POLICY-001` | project-policy | accepted | `SRC-POLICY-002`, Required fields and verification rule | `provisional`: governs source and review handling, not identity semantics. |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: no official immutable identity, manifest, package, or runtime conclusion is reviewed. |
| `CLM-DRF-IDENTITY-NORMATIVE` | project-policy | accepted | `SRC-POLICY-002`, Freshness | `provisional`: requires immutable identity evidence before `dTag` behavior is concluded. |
| `CLM-DRF-MANIFEST-NORMATIVE` | project-policy | accepted | `SRC-POLICY-002`, Freshness | `provisional`: requires immutable manifest evidence before kind or resolution behavior is concluded. |

## Implementation and runtime evidence

`CMP-BASELINE-001` is **blocked**. The Plan 01-28 consolidation audit records `SPK-D-IMPACT-001` as materially uncertain: exact-byte and one-byte mutation work proves only the supplied local fixture observations, not a manifest, identity tuple, verifier, or loader rule. It records `SPK-G-IMPACT-001` as materially uncertain: no qualified public package candidate was available or executed. These consolidated outcomes are explanatory boundaries, not upstream facts or a substitute for immutable sources.

## Drift and open questions

- `DRF-IDENTITY-001` is **blocked** because no immutable manifest or aggregate-identity source has been collected.
- `DRF-MANIFEST-001` is **blocked** because current manifest-kind sources are absent from the immutable registry.
- `DRF-ARTIFACT-001` and `DRF-CONFORMANCE-001` are **blocked** because public release/build-output and conformance baselines are unavailable.
- `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, and `OQ-VERIFIED-LOADER-VERIFIER-001` record the separate provenance and review work needed before any identity, manifest, or verifier lesson assertion.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` and `OQ-PUBLIC-CONFORMANCE-001` record the separate public release, export, provenance, integrity, and conformance work needed before distribution claims.

## Misconceptions to address

- A `dTag` token in a diagram, archive, or fixture does not establish an identity tuple or mapping rule.
- A manifest-looking object does not prove manifest kind, resolver, package, or loader behavior.
- A package name, build output, local digest, or compile result does not prove a public distribution artifact or conformance.

## Story representation

**Conceptual simulation:** A learner follows a fictional artifact card through four question cards: identity source, manifest source, verifier provenance, and public-distribution evidence. Every card states `blocked` or `needs immutable source`; it does not create a key, sign content, resolve a manifest, install a package, contact a registry, or publish an artifact.

## System representation

**Conceptual simulation:** `illustrative artifact → unresolved identity evidence → unresolved manifest/verifier evidence → unresolved public-distribution evidence`. The model separates questions rather than depicting a stable identity, aggregate, resolver, installer, runtime, or release pipeline.

## Wire representation

No current identity tuple, manifest envelope, signature/blob/aggregate format, or package metadata record is validated. The static equivalent is an evidence-link table that cites `DRF-IDENTITY-001`, `DRF-MANIFEST-001`, and their dated `OQ-*` records; it must not present pseudo-fields as a protocol schema.

## Code representation

No verifier, resolver, manifest parser, package install, or runtime import is appropriate. A non-executable record may show `illustrative artifact`, `fixture digest only`, `public provenance missing`, and `review needed`; it contains no real key, secret, signature routine, cryptographic implementation, package command, registry access, or external service call.

## Candidate instrument

- **Conceptual simulation:** Identity and Distribution Evidence Trail with deterministic local cards and an inspectable transcript.
- **Provenance:** conceptual simulation; no real napplet, verified loader, public package, distribution system, or implementation observation.
- **Safety boundary:** no real keys, secrets, signer, package install, registry access, verifier execution, manifest resolution, live service, or publication.

## Required fixtures and tests

- Derive later cards, transcript, and static table from common structured sources so human and machine outputs carry identical canonical IDs and uncertainty labels.
- Provide keyboard navigation, reduced-motion equivalence, state inspection, reset/replay, and a static equivalent for every later interactive view.
- Test that any illustrative `dTag`, manifest, or artifact text links to its canonical record and cannot be shown as a verified identity, resolver, distribution, or conformance outcome.

## Do not teach as settled

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** no public immutable package/runtime/example/fixture compatibility baseline exists. **Impact:** no distribution or runtime compatibility conclusion is available.
- `DRF-IDENTITY-001` — **state: blocked**. **Reason:** immutable manifest and aggregate-identity sources are missing. **Impact:** `dTag` identity behavior cannot be asserted.
- `DRF-MANIFEST-001` — **state: blocked**. **Reason:** manifest-kind sources are absent. **Impact:** manifest kind and resolution behavior cannot be taught.
- `DRF-ARTIFACT-001` and `DRF-CONFORMANCE-001` — **state: blocked**. **Reason:** public artifact/build-output and conformance baselines are not pinned. **Impact:** package, release, output, and conformance claims remain unavailable.
- `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, and `OQ-VERIFIED-LOADER-VERIFIER-001` — **state: blocked**. **Reason:** identity mapping, manifest source/resolver, and verifier provenance lack required immutable evidence. **Impact:** do not present or implement those behaviors.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` and `OQ-PUBLIC-CONFORMANCE-001` — **state: blocked**. **Reason:** public release/export/integrity and conformance targets are uncollected. **Impact:** do not claim an artifact is distributable, compatible, or conformant.

- `CLM-DRF-IDENTITY-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-DRF-MANIFEST-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-POLICY-001` — **state: provisional**. **Reason:** Policy is structurally validated; it does not itself approve a protocol-sensitive claim. **Impact:** requirements EVID-01, OPER-03; phases 01.
- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
## Follow-up research

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** qualified public compatibility inputs are missing. **Impact:** collect independently pinned package, runtime, example, fixture, release, and current-work evidence before selecting an identity/distribution teaching path.
- `DRF-IDENTITY-001`, `DRF-MANIFEST-001`, `DRF-ARTIFACT-001`, and `DRF-CONFORMANCE-001` — **state: blocked**. **Reason:** their normative and observed evidence remains distinct and incomplete. **Impact:** retain parallel authority/maturity records under D-12 and D-16 rather than inventing a rule.
- `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, and `OQ-VERIFIED-LOADER-VERIFIER-001` — **state: blocked**. **Reason:** each has a separately scoped official-source/provenance search and review criterion. **Impact:** resolve all three before promoting a loader-related identity or manifest conclusion.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` and `OQ-PUBLIC-CONFORMANCE-001` — **state: blocked**. **Reason:** public release, integrity, export, and target evidence is absent. **Impact:** revisit distribution teaching only after the dated questions resolve and required technical/security review occurs.
- `CLM-DRF-IDENTITY-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-DRF-MANIFEST-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-POLICY-001` — **state: provisional**. **Reason:** Policy is structurally validated; it does not itself approve a protocol-sensitive claim. **Impact:** requirements EVID-01, OPER-03; phases 01.
- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
