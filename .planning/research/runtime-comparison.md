# Runtime Comparison

## Research question

Which credible runtime surfaces demonstrate required behavior, possible architecture, host policy, or external adapters for later teaching work?

## Sources and immutable revisions

- `SRC-POLICY-001` and `SRC-POLICY-002` are immutable project-policy records only; their revisions and digests are recorded in the source registry.
- `CAND-RUNTIME-IMPLEMENTATION` is a discovery candidate with no immutable official runtime record.
- `CMP-BASELINE-001` and `CLM-CMP-RUNTIME-001` establish the current blocked compatibility disposition.

## Observations

No credible runtime has a validated immutable source revision, browser-shell evidence, or public conformance record. The catalog therefore records no runtime as a selected implementation or teaching-host profile.

The comparison dimensions remain required for later evidence collection:

| Dimension | Classification now | Evidence state |
| --- | --- | --- |
| Loader/verifier | Required behavior to investigate | Blocked |
| Browser shell | Possible architecture | Blocked |
| Source mapping | Required behavior to investigate | Blocked |
| Policy | Host policy | Blocked |
| Dispatch | Required behavior to investigate | Blocked |
| Domains | Required behavior to investigate | Blocked |
| Storage | Possible architecture | Blocked |
| Signer/relay adapters | External adapters | Blocked |
| Composition | Possible architecture | Blocked |
| Conformance | Required behavior to investigate | Blocked |

## Conflicts

No normative protocol side and no observed runtime side are available for comparison. `DRF-HANDSHAKE-001`, `DRF-INTENT-001`, `DRF-UNKNOWN-MESSAGES-001`, `DRF-EGRESS-001`, and `DRF-CONFORMANCE-001` preserve the relevant unresolved differences without selecting a winner.

## Inference

Runtime architecture cannot be inferred from the archived plan or a discovery pointer. The dimensions are a research checklist, not a default host design.

## Prototype or measurement

None. No runtime, browser shell, adapter, or host has been executed. No production scaffold has been created.

## Recommendation

Keep all runtime candidates blocked for teaching-host and delivery decisions. Acquire targeted public immutable records only where they affect protocol shape, security boundaries, browser viability, build identity, or licensing (D-08); compare released state with default-branch/open work separately (D-05). A later ADR may recommend an evidence-backed profile but cannot be accepted here.

## Uncertainty

Material. Runtime semantics, interoperability, browser viability, host policy, composition behavior, and adapter boundaries remain unknown.

## Affected phases and requirements

- Phase: `01`; later teaching-scope, browser, loader, conformance, and ADR work.
- Requirements: `EVID-03`, `EVID-04`.
- Compatibility: `CMP-BASELINE-001`.
- Claim: `CLM-CMP-RUNTIME-001`.
- Open question: `OQ-UPSTREAM-BASELINE-001`.

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical and content-learning human review. Architecture and teaching-host selection remain explicit human-approved ADR decisions.
