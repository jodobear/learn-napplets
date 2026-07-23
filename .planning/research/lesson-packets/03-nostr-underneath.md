# Lesson Research Packet — Nostr Underneath

- **Lesson ID:** LES-003
- **Primary audience:** Developers new to Nostr and general web/application developers; experienced Nostr developers may use this as an evidence-status check.
- **Prerequisites:** LES-001 and LES-002, including the distinction between a teaching scenario and a verified protocol fact.
- **Last researched:** 2026-07-24

## Learner question

What minimum Nostr context can be introduced without pretending that an event, relay, identity, or publication flow has been established by the current evidence baseline?

## Intended outcome

Learners can identify the recurring note journey as a proposed explanatory frame, distinguish it from an event or relay protocol trace, and name the source work required before any concrete Nostr behavior becomes lesson fact.

## Current terminology

- **Note journey** is a project scenario: compose, save, identify, request publish, apply policy, sign, route, resolve, and render are learning prompts, not an observed or normative sequence.
- **Nostr event**, **relay**, **signing**, and **publish** are discovery vocabulary in this packet; no current immutable Nostr source record defines their required behavior here.
- **Identity** and **manifest** questions remain unresolved and must be connected to canonical evidence IDs rather than free-form assumptions.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-POLICY-001` | project-policy | accepted | `SRC-POLICY-002`, Required fields and verification rule | `provisional`: the evidence process is defined, not Nostr behavior. |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: no immutable protocol conclusion may be taught. |
| `CLM-DRF-IDENTITY-NORMATIVE` | project-policy | accepted | `SRC-POLICY-002`, Freshness | `provisional`: requires immutable identity evidence before dTag behavior is concluded. |

## Implementation and runtime evidence

No event fixture, relay trace, signer, package, or runtime observation has been collected for this lesson. A later deterministic fixture may model a note-shaped object solely as illustrative data, but it cannot claim validity, publishability, identity semantics, routing, or rendering behavior.

## Drift and open questions

- `DRF-IDENTITY-001` is **blocked**: neither manifest nor aggregate-identity evidence has been acquired.
- `DRF-MANIFEST-001` is **blocked**: current manifest-kind sources are absent.
- `DRF-EGRESS-001` is **blocked**: browser egress and mediated access lack source and measurement evidence.
- `OQ-UPSTREAM-BASELINE-001` identifies the authoritative source and review work before event, relay, identity, or publication claims can be settled.

## Misconceptions to address

- A note-shaped JSON fixture is not a valid event, signed content, or a real network publication.
- A linear journey diagram does not prove that all clients, hosts, or runtimes use that order.
- An identity label or dTag-like token without pinned evidence is not a stable identity rule.

## Story representation

**Conceptual simulation:** A learner follows a fictional draft note through an explicitly hypothetical sequence of questions: who would identify it, who would authorize action, and what evidence would be needed to render it. Each step is marked `illustrative` or `blocked`.

## System representation

**Conceptual simulation:** `draft → unresolved identity question → proposed request question → unresolved external system question → display question`. The representation purposefully omits a protocol actor, guaranteed relay, signer, or runtime.

## Wire representation

No current validated event, relay message, or manifest fragment is available. Use a static field inventory labeled `not a protocol envelope` and link the unavailability to `CLM-UPSTREAM-BASELINE-001` and `DRF-MANIFEST-001`.

## Code representation

No current tested code example is available. A data-only, non-executable fixture may support a reasoning exercise if it has deterministic local values, no secret material, and a visible statement that it does not encode protocol validity.

## Candidate instrument

- **Conceptual simulation:** an optional Nostr-underneath journey with a static step transcript and evidence-state labels.
- **Provenance:** conceptual simulation, not an implementation observation or real browser boundary.
- **Safety boundary:** no relay connection, signer, key, identity, upload, or live publication path.

## Required fixtures and tests

- Deterministic local note-shaped fixture with an explicit `illustrative-only` label and no real credentials or endpoints.
- Static explanation, keyboard sequence navigation, reset/replay, and state-inspection transcript for any later interaction.
- Test that the instrument never labels its fixture an event, signed payload, or successful publication and retains the cited blocked IDs.

## Do not teach as settled

- `CLM-UPSTREAM-BASELINE-001` is **blocked**: no current immutable protocol conclusion supports a real event/relay/publication lesson.
- `DRF-IDENTITY-001` and `DRF-MANIFEST-001` are **blocked**: identity and manifest behavior, including dTag questions, cannot be asserted.
- `DRF-EGRESS-001` is **blocked**: browser-versus-mediated external access is unmeasured and unresolved.
- `CLM-DRF-IDENTITY-NORMATIVE` is **provisional** project policy, not a protocol identity definition.

## Follow-up research

- Fulfil `OQ-UPSTREAM-BASELINE-001` with official immutable Nostr and napplet-related sources before promoting any event, relay, identity, or publication statement.
- Acquire separate source and measurement evidence for `DRF-IDENTITY-001`, `DRF-MANIFEST-001`, and `DRF-EGRESS-001`; retain normative and observed sides separately.
- Replace the conceptual wire/code placeholders only with validated source-linked fixtures and the required human review.
