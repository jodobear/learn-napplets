# Lesson Research Packet — The Sandbox Boundary

- **Lesson ID:** LES-004
- **Primary audience:** General web/application developers, runtime implementers, and security-minded learners.
- **Prerequisites:** LES-001 through LES-003; basic understanding that a conceptual boundary does not establish browser, protocol, or runtime guarantees.
- **Last researched:** 2026-07-24

## Learner question

Who might be trusted in a future teaching boundary, what authority should remain explicit, and which guarantees cannot yet be claimed?

## Intended outcome

Learners can identify the difference between proposed host/guest authority, observed browser behavior, and upstream protocol requirements; they can use a static trust map without assuming an iframe, capability mechanism, or message boundary is already verified.

## Current terminology

- **Trusted host** and **untrusted guest napplet** are project boundary terms: the product constraint assigns sensitive/repetitive authority to a host and declared mediated capabilities to a guest, but it does not prove a selected protocol/runtime mechanism.
- **Sandbox boundary**, **capability**, and **mediated access** are unresolved implementation/protocol questions unless linked to a future pinned source and measurement.
- **Browser observation** is distinct from an upstream requirement and from local host policy under D-16.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-POLICY-001` | project-policy | accepted | `SRC-POLICY-002`, Required fields and verification rule | `provisional`: process and labeling rule, not a browser or protocol guarantee. |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: current boundary behavior is unresolved. |
| `CLM-CMP-RUNTIME-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, research completion and freshness | `blocked`: no runtime baseline supports a chosen host profile. |

## Implementation and runtime evidence

No browser-boundary spike, runtime implementation observation, selected host profile, or real request/result exists. `teaching-scope.yaml` records `HOST-PROFILE-001` as not selected and requires a deterministic static fallback. The current evidence supports a proposal for least-authority teaching, not a claim that an iframe, sandbox, origin check, capability gate, or message receiver has specific behavior.

## Drift and open questions

- `DRF-HANDSHAKE-001` is **blocked**: bootstrap behavior lacks immutable source and observed runtime evidence.
- `DRF-EGRESS-001` is **blocked**: browser egress versus mediated access lacks a named measurement and immutable source.
- `DRF-UNKNOWN-MESSAGES-001` is **blocked**: unknown message/source behavior is not defined by the current records.
- `OQ-UPSTREAM-BASELINE-001` maps the required official source collection, comparison, and human review.

## Misconceptions to address

- A drawn sandbox boundary is not evidence that guest code cannot reach a specific resource.
- A browser feature, if later observed, is not by itself a protocol mandate or a sufficient project security policy.
- “Capability” does not mean a guest has been granted ambient authority; the actual mechanism is not yet selected.

## Story representation

**Conceptual simulation:** A guest asks a host-shaped actor for a labeled operation. The transcript distinguishes `request proposed`, `policy unresolved`, `browser behavior unmeasured`, and `no real authority granted`.

## System representation

**Conceptual simulation:** A trust map separates proposed guest code, a proposed host decision point, and host-only concern categories. It shows authority questions, not confirmed iframe attributes, origin boundaries, source-window identity, or network pathways.

## Wire representation

No validated request/response envelope is available. The static equivalent is a blank-envelope anatomy card whose fields are marked `to be evidenced`; it must not use a plausible `postMessage` payload as if it were a protocol or runtime trace.

## Code representation

No executable host/guest code is safe to present as current behavior. Use a non-executable policy matrix stating that key, signer, relay, wallet, device, upload, and policy access are not granted by this research packet and require future declared, measured controls.

## Candidate instrument

- **Conceptual simulation:** Trust Map and Threat Lens with a static owns/does-not-own table.
- **Provenance:** conceptual simulation; it is not a real browser boundary, deterministic host fixture, or implementation observation.
- **Safety boundary:** deterministic local data only; no user code execution, real secrets, signing, wallets, devices, uploads, or external services.

## Required fixtures and tests

- A deterministic trust-map data fixture that exposes actor, proposed authority category, denied direct access, evidence state, and static transcript.
- Keyboard traversal, reduced-motion behavior, reset/replay, and an accessible table for every later interactive rendering.
- Tests that retain conceptual-simulation provenance and prevent the display of unmeasured browser or protocol behavior as a guarantee.

## Do not teach as settled

- `CLM-UPSTREAM-BASELINE-001` and `CLM-CMP-RUNTIME-001` are **blocked**: no official protocol/runtime record selects a host profile or boundary behavior.
- `DRF-HANDSHAKE-001`, `DRF-EGRESS-001`, and `DRF-UNKNOWN-MESSAGES-001` are **blocked**: bootstrap, egress, and unknown-message behavior require current source/measurement evidence.
- `HOST-PROFILE-001` is **not selected** in `TSCOPE-001`; the safe fallback is a labeled static conceptual simulation.

## Follow-up research

- Resolve `OQ-UPSTREAM-BASELINE-001` with official immutable protocol, package, runtime, and browser-boundary records before claiming a mechanism.
- Run the planned browser and boundary spikes with a deterministic local fixture; record browser observation, upstream statement, and project policy separately.
- Revisit `DRF-HANDSHAKE-001`, `DRF-EGRESS-001`, and `DRF-UNKNOWN-MESSAGES-001` only after their source, measurement, impact, and review requirements are met.
