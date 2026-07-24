# Lesson Research Packet — Inside a Runtime

- **Lesson ID:** LES-012
- **Primary audience:** Runtime implementers, general web/application developers, and learners comparing host responsibility with implementation architecture.
- **Prerequisites:** LES-004 through LES-006 and LES-008; understand that a proposed host/guest boundary does not select a runtime.
- **Last researched:** 2026-07-24

## Learner question

What must a future host investigate, and what remains only a possible runtime architecture, host policy, or external adapter while current runtime evidence is blocked?

## Intended outcome

Learners can classify a runtime dimension as required behavior to investigate, possible architecture, host policy, or external adapter; they can avoid treating that classification as a selected host profile, browser guarantee, or protocol mandate.

## Current terminology

- **Runtime** is a research surface, not a selected implementation, shell, or teaching-host profile.
- **Required behavior to investigate** is a collection priority, not evidence that a behavior is currently mandated.
- **Possible architecture**, **host policy**, and **external adapter** are categories for separating claims; none names an approved architecture or integration.
- **Runtime X-ray** is a proposed data-driven static instrument, not an execution trace or runtime inspection tool.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-CMP-RUNTIME-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, runtime compatibility evidence | **state: blocked**; credible runtime candidates remain unpinned. |

## Implementation and runtime evidence

`CMP-BASELINE-001` is **blocked** and no credible runtime has an immutable source revision, browser-shell evidence, public conformance record, or selected teaching-host profile. The runtime comparison classifies loader/verifier, source mapping, dispatch, domains, and conformance as required behavior to investigate; browser shell, storage, and composition as possible architecture; policy as host policy; and signer/relay integrations as external adapters. These classifications are an acquisition checklist, not a protocol rule or default implementation. Firefox evidence remains blocked because Firefox exited before Playwright attached; that fixture-specific observation does not establish a runtime or browser requirement.

## Drift and open questions

- `DRF-HANDSHAKE-001` and `DRF-UNKNOWN-MESSAGES-001` remain blocked: bootstrap and error/source handling lack immutable protocol and observed runtime evidence.
- `DRF-EGRESS-001` remains blocked: a local browser egress observation does not establish mediated-access behavior.
- `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` and `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` retain the missing Firefox fixture result without selecting a workaround.
- `OQ-UPSTREAM-BASELINE-001` is the dated source-and-review route before selecting runtime behavior or a teaching-host profile.

## Misconceptions to address

- A runtime diagram does not prove a loader, verifier, dispatch, policy, storage, or adapter architecture.
- A browser result is an observation with its own scope; it is not an upstream requirement, a host-policy decision, or cross-browser support.
- A host-policy label does not imply that a particular runtime enforces it.

## Story representation

**Conceptual simulation:** A learner sorts proposed runtime responsibilities into four visible categories and receives a transcript saying `classification only`, `runtime not selected`, and `no operation executed`. No guest code, host API, signer, relay, storage, external adapter, or browser boundary runs.

## System representation

**Conceptual simulation:** `evidence question → required behavior to investigate | possible architecture | host policy | external adapter`. The branches express categorization, not a prescribed execution stack, capability mechanism, or selected host profile.

## Wire representation

No runtime bootstrap, request, response, dispatch, error, or adapter envelope is validated. The static equivalent is a category table citing the blocked evidence records; it must not use plausible messages or protocol fields.

## Code representation

No runtime, loader, verifier, browser-shell, adapter, or host API may be shown as current. A non-executable classification record can list dimensions and evidence states, but it cannot import a runtime, execute untrusted code, perform a browser run, access a secret, or contact an external adapter.

## Candidate instrument

- **Conceptual simulation:** Runtime X-ray classification table with deterministic source-status cards and an inspectable transcript.
- **Provenance:** conceptual simulation; neither a selected runtime, teaching-host fixture, browser test, nor observed implementation behavior.
- **Safety boundary:** no runtime import, guest execution, host authority, signer, key, relay, storage, browser launch, external adapter, credential, or network access.

## Required fixtures and tests

- Derive every category, status badge, and transcript row from common structured evidence records for human/LLM parity.
- Provide keyboard operation, reduced-motion equivalence, state inspection, reset/replay, and an accessible static table for any later X-ray interaction.
- Test that categories remain distinct and that fixture-specific Chrome or Firefox evidence cannot become a runtime recommendation or protocol requirement.

## Do not teach as settled

- `CLM-CMP-RUNTIME-001` — **state: blocked**. **Reason:** runtime candidates remain unpinned discovery pointers. **Impact:** no runtime architecture, host profile, browser shell, or adapter behavior is selected.
- `CMP-BASELINE-001` — **state: blocked**. **Reason:** public compatibility inputs do not provide a credible runtime baseline. **Impact:** runtime dimensions stay a research checklist rather than an implementation decision.
- `DRF-HANDSHAKE-001` — **state: blocked**. **Reason:** immutable bootstrap and observed runtime evidence are absent. **Impact:** do not teach startup, request, lifecycle, or response semantics as a host requirement.
- `DRF-UNKNOWN-MESSAGES-001` — **state: blocked**. **Reason:** no immutable protocol or runtime record defines unknown request/source behavior. **Impact:** error, rejection, and fallback handling remain unspecified.
- `DRF-EGRESS-001` — **state: blocked**. **Reason:** browser egress and mediated access lack the required source and measurement baseline. **Impact:** do not claim a channel, isolation, or mediation guarantee.
- `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` — **state: blocked**. **Reason:** Firefox exited before approved Playwright attachment and produced no fixture observation. **Impact:** no cross-browser runtime or host conclusion is available.
- `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` — **state: blocked**. **Reason:** the Firefox fixture behavior required for boundary assessment is absent. **Impact:** retain the static fallback and do not adopt a launcher workaround as a result.
- `OQ-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** official immutable protocol, runtime, and current-work records are not collected and reviewed. **Impact:** route future runtime claims through source acquisition and human review.

## Follow-up research

- `CLM-CMP-RUNTIME-001` — **state: blocked**. **Reason:** runtime candidates remain unpinned discovery pointers. **Impact:** acquire public immutable runtime evidence before comparing implementations.
- `CMP-BASELINE-001` — **state: blocked**. **Reason:** public compatibility inputs do not provide a credible runtime baseline. **Impact:** preserve separate required-behavior, architecture, policy, and adapter categories during future comparison.
- `DRF-HANDSHAKE-001` — **state: blocked**. **Reason:** immutable bootstrap and observed runtime evidence are absent. **Impact:** collect normative and observed records separately rather than selecting an envelope.
- `DRF-UNKNOWN-MESSAGES-001` — **state: blocked**. **Reason:** no immutable protocol or runtime record defines unknown request/source behavior. **Impact:** investigate error behavior without inventing rejection or fallback semantics.
- `DRF-EGRESS-001` — **state: blocked**. **Reason:** browser egress and mediated access lack the required source and measurement baseline. **Impact:** retain the difference between browser observation and host-policy design.
- `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` — **state: blocked**. **Reason:** Firefox exited before approved Playwright attachment and produced no fixture observation. **Impact:** resolve the evidence gap before treating cross-browser behavior as measured.
- `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` — **state: blocked**. **Reason:** the Firefox fixture behavior required for boundary assessment is absent. **Impact:** use the dated question to route compatible measurement work without a workaround.
- `OQ-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** official immutable protocol, runtime, and current-work records are not collected and reviewed. **Impact:** obtain the required sources and approval before promoting any category to a runtime conclusion.
