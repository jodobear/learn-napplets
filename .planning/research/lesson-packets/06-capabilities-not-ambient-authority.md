# Lesson Research Packet — Capabilities, Not Ambient Authority

- **Lesson ID:** LES-006
- **Primary audience:** General web/application developers, security-minded learners, and runtime implementers.
- **Prerequisites:** LES-004 and LES-005; understand that a conceptual host/guest boundary is not proof of a selected capability mechanism.
- **Last researched:** 2026-07-24

## Learner question

Why should a proposed guest receive only named, mediated authority rather than an assumption of direct access, even when the implementation mechanism is unresolved?

## Intended outcome

Learners can distinguish the project least-authority policy from an upstream or browser fact, identify a proposed capability as an explicit request for host mediation, and avoid claiming that a grant, denial, or fallback mechanism already exists.

## Current terminology

- **Declared mediated capability** is a project boundary policy: a future guest receives only authority explicitly mediated by the host.
- **Ambient authority** means an assumed direct ability to reach a sensitive or repetitive resource; this packet does not claim a current runtime prevents it by a particular mechanism.
- **Capability grant**, **capability removal**, and **graceful degradation** are future host-profile and fixture questions, not current protocol semantics.
- **Host-only authority** is a learning label for concerns such as keys, signers, relays, wallets, devices, uploads, and policy; it is not evidence that a named runtime implements those categories.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-POLICY-001` | project-policy | accepted | `SRC-POLICY-002`, Required fields and verification rule | `provisional`: evidence handling and boundary policy, not a capability API. |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: no protocol conclusion defines capability behavior. |
| `CLM-CMP-RUNTIME-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, freshness | `blocked`: no credible runtime baseline selects a grant model. |

## Implementation and runtime evidence

`CMP-BASELINE-001` is **blocked** and cannot establish a real capability surface. `HOST-PROFILE-001` is **not selected** in `TSCOPE-001`; its safe fallback is static public content with source-status-rich conceptual simulations. A future deterministic fixture may show a deliberately modeled allow/deny branch, but it must label that branch as a local teaching model rather than evidence of an upstream capability, browser isolation rule, or runtime authorization result.

## Drift and open questions

- `DRF-HANDSHAKE-001` is **blocked**: no bootstrap semantics establish how a guest asks for authority.
- `DRF-EGRESS-001` is **blocked**: local browser egress evidence does not establish direct-versus-mediated resource access.
- `DRF-UNKNOWN-MESSAGES-001` is **blocked**: unknown request/source behavior has no immutable protocol or runtime definition.
- `OQ-UPSTREAM-BASELINE-001` and `OQ-EGRESS-NIP-001` retain the official-source and browser-measurement work required before mechanism claims.

## Misconceptions to address

- A capability label does not prove that a guest has an API, a permission prompt, a sandbox token, or access to a host resource.
- “No ambient authority” is a project least-authority direction, not evidence of a current runtime security guarantee.
- A modeled denial is not a measured graceful-degradation path unless a future selected host profile and fixture support it.

## Story representation

**Conceptual simulation:** A guest selects one proposed operation card while host-only concern cards remain visibly unavailable. The transcript says `request proposed`, `grant not implemented`, and `no real authority granted`; no card invokes a signer, wallet, key, relay, device, upload, or external service.

## System representation

**Conceptual simulation:** `guest concern → named proposed request → unresolved host policy decision → static explanation`. The diagram does not assert a capability namespace, injection path, permission model, sandbox attribute, or security boundary behavior.

## Wire representation

No validated capability request, grant, denial, or error envelope exists. Use a static table of proposed fields and evidence states, not an executable or plausible protocol message; surface `DRF-HANDSHAKE-001` and `DRF-UNKNOWN-MESSAGES-001` beside the table.

## Code representation

No current API should be taught. A non-executable policy matrix can distinguish `proposed mediated`, `not granted by this packet`, and `evidence needed`; it must not use imports, globals, mock secrets, real keys, signer calls, or live service endpoints.

## Candidate instrument

- **Conceptual simulation:** Capability Lab card sorter with a deterministic local state transcript.
- **Provenance:** conceptual simulation, not a selected teaching-host fixture, browser observation, or real napplet.
- **Safety boundary:** no user code execution, live service, relay, wallet, signer, secret, key, device, upload, or real capability grant.

## Required fixtures and tests

- Derive all later capability names, states, denials, and evidence badges from common structured packet data for human/LLM parity.
- Support keyboard operation, reduced-motion equivalence, transcript/state inspection, reset/replay, and an accessible static table without changing the conceptual result.
- Test that a simulated deny path remains labelled conceptual and never reports an unmeasured runtime or protocol guarantee.

## Do not teach as settled

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** immutable compatibility inputs are not available. **Impact:** no capability surface, runtime behavior, or conformance result is established.
- `DRF-HANDSHAKE-001` — **state: blocked**. **Reason:** bootstrap behavior lacks immutable source and runtime evidence. **Impact:** request/grant lifecycle and authority-transfer semantics cannot be taught as fact.
- `DRF-EGRESS-001` — **state: blocked**. **Reason:** browser egress versus mediation is unresolved. **Impact:** the lesson cannot claim that direct resource access is technically prevented.
- `DRF-UNKNOWN-MESSAGES-001` — **state: blocked**. **Reason:** no current source defines unknown request/source handling. **Impact:** errors, rejection, and fallback mechanics remain unspecified.
- `OQ-UPSTREAM-BASELINE-001` and `OQ-EGRESS-NIP-001` — **state: blocked**. **Reason:** official source collection and measured-browser work are incomplete. **Impact:** mechanism-dependent teaching stays bounded to a conceptual simulation.

- `CLM-POLICY-001` — **state: provisional**. **Reason:** Policy is structurally validated; it does not itself approve a protocol-sensitive claim. **Impact:** requirements EVID-01, OPER-03; phases 01.
- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
- `CLM-CMP-RUNTIME-001` — **state: blocked**. **Reason:** Runtime candidates remain unpinned discovery pointers. **Impact:** requirements EVID-02, EVID-03; phases 01.
## Follow-up research

- `CMP-BASELINE-001` — **state: blocked**. **Reason:** no public package/runtime/example/fixture comparison exists. **Impact:** retain the static conceptual fallback until a reviewed compatibility baseline can support a selected host profile.
- `DRF-HANDSHAKE-001`, `DRF-EGRESS-001`, and `DRF-UNKNOWN-MESSAGES-001` — **state: blocked**. **Reason:** no immutable definition or adequate measurement resolves the separate questions. **Impact:** preserve distinct normative, observed, policy, and inference records under D-12, D-16, and D-18.
- `OQ-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** official immutable source records and review are absent. **Impact:** use it to collect the source/claim path for any later capability claim.
- `OQ-EGRESS-NIP-001` — **state: blocked**. **Reason:** its official-source scope and attached-context measurement have not been completed. **Impact:** revisit browser/mediation statements only after the dated question and required review resolve.
- `CLM-POLICY-001` — **state: provisional**. **Reason:** Policy is structurally validated; it does not itself approve a protocol-sensitive claim. **Impact:** requirements EVID-01, OPER-03; phases 01.
- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
- `CLM-CMP-RUNTIME-001` — **state: blocked**. **Reason:** Runtime candidates remain unpinned discovery pointers. **Impact:** requirements EVID-02, EVID-03; phases 01.
