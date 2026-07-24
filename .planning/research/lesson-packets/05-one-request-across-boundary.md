# Lesson Research Packet — One Request Across a Boundary

- **Lesson ID:** LES-005
- **Primary audience:** General web/application developers and developers new to Nostr.
- **Prerequisites:** LES-001 through LES-004, especially the difference between a conceptual boundary and a measured runtime boundary.
- **Last researched:** 2026-07-24

## Learner question

How can a learner reason about one request crossing a proposed guest-to-host boundary without mistaking a diagram or local fixture for a protocol trace?

## Intended outcome

Learners can label a request as proposed, identify the authority decision that must remain with a trusted host, and explain why no current request envelope, host profile, or first real-lab operation is established.

## Current terminology

- **Request across a boundary** is a project learning scenario, not a validated NAP, NIP, browser, or runtime message sequence.
- **Trusted host** and **guest napplet** are project boundary terms: sensitive or repetitive authority is assigned to the proposed host while a guest receives only declared mediated capabilities.
- **Envelope** and **response** are explanatory labels only. No current immutable record defines their fields, sender identity, transport, lifecycle, or error semantics.
- **First real-lab operation** is `OP-FIRST-REAL-LAB-001`, explicitly not selected in `TSCOPE-001`.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-POLICY-001` | project-policy | accepted | `SRC-POLICY-002`, Required fields and verification rule | `provisional`: governs evidence handling, not a request protocol. |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: no official immutable request, transport, or runtime baseline is reviewed. |
| `CLM-CMP-RUNTIME-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, freshness | `blocked`: no runtime compatibility evidence selects host behavior. |

## Implementation and runtime evidence

`CMP-BASELINE-001` is **blocked**: it is a canonical record of missing public compatibility baselines, not a successful interoperability result. `TSCOPE-001` records both the first real-lab operation and teaching-host profile as **not selected**. A later deterministic host fixture may model a proposed request/result only after it labels itself as a fixture and does not claim a protocol envelope, real host, signer, relay, wallet, device, upload, external service, or live network result.

## Drift and open questions

- `DRF-HANDSHAKE-001` is **blocked**: no immutable bootstrap source or observed runtime baseline establishes a request handshake.
- `DRF-EGRESS-001` is **blocked**: a browser egress observation cannot be treated as mediated-access or transport behavior.
- `OQ-UPSTREAM-BASELINE-001` records the official-source collection and review needed before request behavior can be taught as fact.
- `OQ-EGRESS-NIP-001` records the unresolved upstream and measurement scope for channel constraints or mediation.

## Misconceptions to address

- An arrow from guest to host does not prove a `postMessage`, request envelope, sender check, or response rule.
- A host-shaped actor in a lesson does not have a selected signing, relay, storage, or policy authority.
- A deterministic fixture can demonstrate a stated local simulation without becoming a real first lab or protocol conformance result.

## Story representation

**Conceptual simulation:** A note-tool-shaped guest asks a host-shaped decision point for a named, hypothetical operation. The transcript exposes `request proposed`, `authority unresolved`, and `result not executed`; it never depicts a real secret, signer, key, relay, wallet, device, upload, or external service.

## System representation

**Conceptual simulation:** `guest concern → proposed request → proposed host decision → static result explanation`. The diagram identifies the authority question but intentionally has no guaranteed browser mechanism, origin rule, transport, receiver, lifecycle, or error path.

## Wire representation

No current validated request/response envelope is available. The static equivalent is an inspectable blank-envelope anatomy card marked `to be evidenced`, with `CLM-UPSTREAM-BASELINE-001`, `DRF-HANDSHAKE-001`, and `OQ-UPSTREAM-BASELINE-001` visible; it must not use plausible wire fields as if they were established.

## Code representation

No executable host or guest API is available. A data-only ownership matrix may state `proposed requester`, `proposed authority decision`, `evidence state`, and `no real operation`; it must contain no runtime imports, real secret, signing call, network request, or implementation-specific API.

## Candidate instrument

- **Conceptual simulation:** Envelope Journey, driven by deterministic local transcript data.
- **Provenance:** conceptual simulation; neither a real napplet nor a deterministic host fixture or implementation observation.
- **Safety boundary:** no live relay, signer, wallet, key, device, upload, external service, or real capability grant.

## Required fixtures and tests

- Derive any later transcript and state table from common structured packet data so human and machine outputs expose the same evidence IDs and labels.
- Provide keyboard traversal, reduced-motion behavior with unchanged meaning, state inspection, reset/replay, and a static-equivalent transcript/table for every later interaction.
- Test that the instrument retains its conceptual-simulation provenance, deterministic inputs, and blocked request/host evidence state.

## Do not teach as settled

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** public release/current-work compatibility baselines are absent. **Impact:** no request/result behavior, host profile, or interoperability outcome may be taught as established.
- `DRF-HANDSHAKE-001` — **state: blocked**. **Reason:** immutable bootstrap and runtime evidence is absent. **Impact:** handshake, envelope, and lifecycle teaching remain conceptual only.
- `DRF-EGRESS-001` — **state: blocked**. **Reason:** browser egress versus mediated access lacks required source and measurement evidence. **Impact:** no channel or mediation guarantee may be claimed.
- `OQ-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** relevant official immutable sources have not been recorded and reviewed. **Impact:** dependent request, runtime, and protocol claims remain blocked.
- `OQ-EGRESS-NIP-001` — **state: blocked**. **Reason:** no immutable upstream statement resolves the measured channels. **Impact:** local browser observations cannot become request-transport or policy facts.

## Follow-up research

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** public compatibility inputs are not pinned. **Impact:** collect separate public package, runtime, example, fixture, release, and current-work baselines before any compatibility lesson conclusion.
- `DRF-HANDSHAKE-001` and `DRF-EGRESS-001` — **state: blocked**. **Reason:** source and measurement evidence remain incomplete. **Impact:** retain parallel normative and observed records under D-12 and D-16 instead of selecting a mechanism.
- `OQ-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** official immutable protocol and runtime records are missing. **Impact:** resolve identity, revision, locator, digest, authority, maturity, and review state before promoting request content.
- `OQ-EGRESS-NIP-001` — **state: blocked**. **Reason:** its official-source search and attached-context measurement work remains unresolved. **Impact:** revisit the lesson only after that dated, impact-scoped question is resolved and reviewed.
