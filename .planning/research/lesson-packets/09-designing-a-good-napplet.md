# Lesson Research Packet — Designing a Good Napplet

- **Lesson ID:** LES-009
- **Primary audience:** General web/application developers, product-minded developers, and runtime implementers.
- **Prerequisites:** LES-004 through LES-008; understand that a focused-app design heuristic is not an upstream or runtime mandate.
- **Last researched:** 2026-07-24

## Learner question

How can a learner evaluate a proposed focused napplet design while authority boundaries, identity, manifest, archetype, convention, and runtime behavior remain evidence-limited?

## Intended outcome

Learners can use an explicitly project-policy design checklist to ask whether a concern is focused, whether authority remains host-owned, and what evidence is missing, while avoiding claims that a selected napplet format, manifest, identity model, capability API, or composition convention already exists.

## Current terminology

- **Good napplet** is a project learning phrase for a focused application design discussion; it is not an upstream quality criterion or an implementation certification.
- **Focused concern** means a proposed narrow application responsibility, not a proof that a real napplet boundary or runtime capability exists.
- **Host-owned authority** is a project policy direction: sensitive or repetitive authority stays with the trusted host while the guest receives only declared mediated capabilities.
- **Manifest** remains an unresolved source/resolver question linked to `CLM-DRF-MANIFEST-NORMATIVE`, `SRC-POLICY-002`, and `OQ-VERIFIED-LOADER-MANIFEST-001`.
- **`dTag` identity** remains an unresolved identity question linked to `CLM-DRF-IDENTITY-NORMATIVE`, `SRC-POLICY-002`, and `OQ-VERIFIED-LOADER-IDENTITY-001`; it must not be used as a bare design requirement.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-POLICY-001` | project-policy | accepted | `SRC-POLICY-002`, Required fields and verification rule | `provisional`: project evidence and design-process rule, not a napplet specification. |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: no official immutable napplet design/rule baseline is reviewed. |
| `CLM-DRF-METADATA-NORMATIVE` | project-policy | accepted | `SRC-POLICY-002`, Freshness | `provisional`: metadata meaning needs immutable registry evidence. |
| `CLM-DRF-IDENTITY-NORMATIVE` | project-policy | accepted | `SRC-POLICY-002`, Freshness | `provisional`: identity evidence is required before `dTag` behavior is concluded. |
| `CLM-DRF-MANIFEST-NORMATIVE` | project-policy | accepted | `SRC-POLICY-002`, Freshness | `provisional`: manifest evidence is required before kind/resolution behavior is concluded. |

## Implementation and runtime evidence

`CMP-BASELINE-001` is **blocked**, `ARC-CANDIDATE-001` is **blocked**, and `HOST-PROFILE-001` is **not selected**. Therefore, the useful near-term design output is a static, evidence-rich heuristic: name the focused concern, list proposed host-owned authority, name proposed mediated requests, label the instrument provenance, and state unresolved evidence. This is project policy and inference for Phase 2/initial static-site planning; it does not select a runtime, package, manifest, verifier, identity scheme, portability target, or editor capability.

## Drift and open questions

- `DRF-METADATA-001` is **blocked**: archetype/convention metadata cannot be settled without immutable registry or projection evidence.
- `DRF-IDENTITY-001` is **blocked**: identity and `dTag` behavior cannot be concluded without immutable identity evidence.
- `DRF-MANIFEST-001` is **blocked**: current manifest-kind and resolution sources are absent.
- `DRF-INTENT-001` is **blocked**: handler/catalog assumptions cannot determine a design integration seam.
- `OQ-UPSTREAM-BASELINE-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, and `OQ-VERIFIED-LOADER-MANIFEST-001` state the dated source/review work required before those design questions become teachable facts.

## Misconceptions to address

- “Small” or “focused” does not prove an application is a real napplet, compatible, secure, or portable.
- A design checklist does not establish manifest, `dTag`, registry, handler, or runtime requirements.
- A policy that host authority should remain explicit does not prove a particular host has enforced it.

## Story representation

**Conceptual simulation:** A learner gives a fictional note-tool card a narrow concern, proposed host-owned concerns, and missing-evidence badges. The outcome is an inspectable rationale, not an executable design, installed package, manifest, identity, signer, key, relay, wallet, device, upload, or external service action.

## System representation

**Conceptual simulation:** `focused concern → proposed mediated request → proposed host-owned authority → evidence/status check`. The model includes explicit unknown nodes for manifest, identity, archetype, convention, and runtime; it must not draw these as completed integrations.

## Wire representation

No current manifest, identity, intent, or capability wire format is validated. The static equivalent is a source-status checklist that exposes relevant `DRF-*` and `OQ-*` IDs rather than a sample package descriptor, message, signature, or resolver record.

## Code representation

No scaffold, package, runtime API, manifest, or real napplet code belongs in this research packet. A non-executable data-only design brief may hold `focus`, `proposed authority`, `simulation provenance`, and `evidence gap`; it must have no runtime import, secret, key, cryptographic routine, package command, live endpoint, or external dependency.

## Candidate instrument

- **Conceptual simulation:** Architecture Clinic design brief with deterministic local data, a visible evidence-status checklist, and static rationale output.
- **Provenance:** conceptual simulation; neither a production design tool, real napplet, deterministic host fixture, nor implementation observation.
- **Safety boundary:** no production scaffold, user-code execution, package install, signer, secret, key, wallet, relay, device, upload, browser run, or external service.

## Required fixtures and tests

- Derive a later checklist, rationale transcript, and accessible static table from common structured sources so human and machine outputs expose the same facts and IDs.
- Provide keyboard operation, reduced-motion equivalence, state inspection, reset/replay, and static-equivalent output for any later interactive design exercise.
- Test that unresolved manifest and `dTag` identity references retain their canonical IDs and cannot become unstructured requirements or settled labels.

## Do not teach as settled

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** public compatibility evidence is absent. **Impact:** no real napplet format, runtime, package, or portable design conclusion is selected.
- `DRF-METADATA-001` — **state: blocked**. **Reason:** metadata has no immutable registry/projection baseline. **Impact:** archetype/convention design guidance remains a comparison topic only.
- `DRF-IDENTITY-001` — **state: blocked**. **Reason:** immutable identity evidence is unavailable. **Impact:** `dTag` identity behavior cannot be a design rule.
- `DRF-MANIFEST-001` — **state: blocked**. **Reason:** current manifest sources are absent. **Impact:** manifest structure and resolution cannot be prescribed.
- `DRF-INTENT-001` — **state: blocked**. **Reason:** handler/catalog assumptions are unpinned. **Impact:** integration, routing, and delegation seams remain unresolved.
- `OQ-UPSTREAM-BASELINE-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, and `OQ-VERIFIED-LOADER-MANIFEST-001` — **state: blocked**. **Reason:** official-source, identity, and manifest/resolver review work is incomplete. **Impact:** evidence gaps stay visible in the design brief rather than becoming requirements.

- `CLM-DRF-MANIFEST-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-DRF-IDENTITY-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-POLICY-001` — **state: provisional**. **Reason:** Policy is structurally validated; it does not itself approve a protocol-sensitive claim. **Impact:** requirements EVID-01, OPER-03; phases 01.
- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
- `CLM-DRF-METADATA-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
## Follow-up research

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** no independently pinned public compatibility inputs exist. **Impact:** use the static first-site design brief only until a reviewed baseline supports a selected host/runtime/package path.
- `DRF-METADATA-001`, `DRF-IDENTITY-001`, `DRF-MANIFEST-001`, and `DRF-INTENT-001` — **state: blocked**. **Reason:** immutable sources and observed behavior remain distinct or absent. **Impact:** retain D-12/D-16 parallel records and D-18 states rather than converting a heuristic into an upstream fact.
- `OQ-UPSTREAM-BASELINE-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, and `OQ-VERIFIED-LOADER-MANIFEST-001` — **state: blocked**. **Reason:** each records a dated official-source search, unresolved reason, scope, and review criterion. **Impact:** resolve those questions before a manifest, `dTag`, identity, or integration rule is promoted beyond a clearly labelled proposal.
- `CLM-DRF-MANIFEST-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-DRF-IDENTITY-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-POLICY-001` — **state: provisional**. **Reason:** Policy is structurally validated; it does not itself approve a protocol-sensitive claim. **Impact:** requirements EVID-01, OPER-03; phases 01.
- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
- `CLM-DRF-METADATA-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
