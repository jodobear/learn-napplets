# Lesson Research Packet — A Nostr Client, Taken Apart

- **Lesson ID:** LES-001
- **Primary audience:** Developers new to Nostr and general web/application developers.
- **Prerequisites:** Basic web application concepts; no assumed Nostr, protocol, runtime, or signing knowledge.
- **Last researched:** 2026-07-24

## Learner question

Why examine a focused napplet-shaped application instead of assuming one interface should own every client concern?

## Intended outcome

Learners can distinguish a proposed focused application concern from shared authority in a conceptual model, identify the missing evidence needed to select a real host or domain, and decline to infer protocol behavior from the model.

## Current terminology

- **Nost r client:** a lesson-title and discovery term only; no current immutable upstream definition is in the canonical registry.
- **Focused application / napplet:** a project learning label, not evidence that a selected implementation or protocol surface exists.
- **Shared authority:** a project-policy framing for sensitive or repetitive host responsibilities; the actual host boundary remains unresolved.
- **Immutable source record:** a provisional project-policy term defined by `SRC-POLICY-001` and `SRC-POLICY-002`.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-POLICY-001` | project-policy | accepted | `SRC-POLICY-002`, Required fields and verification rule | `provisional`: governs research handling, not an upstream fact. |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: no official immutable NAP/NIP/package/runtime baseline has been reviewed. |
| `CLM-CMP-RUNTIME-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, research completion and freshness | `blocked`: no immutable credible runtime baseline is available. |

## Implementation and runtime evidence

No implementation or runtime has been selected or observed. `CLM-CMP-RUNTIME-001` is an explicit blocked disposition, not evidence that a particular host mediates signing, storage, relays, uploads, or policy. The recurring note journey is a conceptual project scenario and must not be rendered as an observed request trace.

## Drift and open questions

- `DRF-DISCOVERY-001` is **blocked** because no immutable official discovery/registry baseline is collected.
- `DRF-HANDSHAKE-001` is **blocked** because neither immutable bootstrap nor runtime evidence exists.
- `OQ-UPSTREAM-BASELINE-001` records the official-source acquisition and review work needed before real host, runtime, or protocol teaching can begin.

## Misconceptions to address

- A focused interface does not prove that it is a real napplet or that a particular runtime supports it.
- Separating an application concern in a diagram does not establish where signing, storage, relay, upload, or policy authority actually resides.
- A preserved planning diagram is not current upstream proof.

## Story representation

**Conceptual simulation:** A composer has a note-shaped draft and asks a proposed trusted boundary for help. The representation says only that the learning model separates a request from the authority decision; it does not claim that any protocol message, signing action, or network operation occurs.

## System representation

**Conceptual simulation:** `focused application → proposed mediated boundary → unresolved external concerns`. The boundary, concern names, and arrows are labels for questions to investigate, not a selected host architecture or execution sequence.

## Wire representation

No current validated envelope is available. Use an inspectable static card stating `blocked: CLM-UPSTREAM-BASELINE-001`; do not invent a request, response, event, or relay wire format.

## Code representation

No current tested package or global example is available. A static pseudo-ownership table may show `application concern`, `unresolved authority`, and `evidence needed`, but it must contain no executable protocol or runtime API example.

## Candidate instrument

- **Conceptual simulation:** a static Monolith Splitter ownership exercise with visible evidence-state badges.
- **Provenance:** conceptual simulation; not a real napplet, deterministic host fixture, or implementation observation.
- **Safety boundary:** no real keys, signing, uploads, relay calls, package imports, or live external dependency.

## Required fixtures and tests

- A deterministic JSON or Markdown ownership transcript whose labels are derived from this packet and cite `CLM-UPSTREAM-BASELINE-001`.
- A static-equivalent table and keyboard-operable selection exercise when implemented later.
- A validation assertion that the instrument keeps its conceptual-simulation label and exposes the blocked source baseline.

## Do not teach as settled

- `CLM-UPSTREAM-BASELINE-001` is **blocked**: official immutable protocol, implementation, and first-lab evidence is absent; impacted requirements include `EVID-01` and `EVID-02`.
- `CLM-CMP-RUNTIME-001` is **blocked**: no runtime compatibility baseline exists, so no concrete host behavior may be claimed.
- `DRF-DISCOVERY-001` and `DRF-HANDSHAKE-001` are **blocked**: discovery and bootstrap behavior require official immutable evidence and human review.

## Follow-up research

- Resolve `OQ-UPSTREAM-BASELINE-001` by recording official identity, revision, locator, digest, authority, evidence class, maturity, and review state for relevant sources.
- Revisit `DRF-DISCOVERY-001` and `DRF-HANDSHAKE-001` after the required immutable sources and independent implementation or measurement evidence are collected.
- Promote no candidate instrument beyond a conceptual simulation unless its claimed behavior is linked to reviewed canonical evidence.
