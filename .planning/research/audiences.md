# Audience Synthesis

Status: **provisional**. This is an evidence-scoped research synthesis, not accepted curriculum copy or a protocol claim. Shared evidence: `SRC-POLICY-001`, `SRC-POLICY-002`, `CLM-UPSTREAM-BASELINE-001`, `CMP-BASELINE-001`, and `OQ-UPSTREAM-BASELINE-001`.

| Audience | Need and prerequisite | Misconception to test | Representation and assessment | Evidence state |
| --- | --- | --- | --- | --- |
| Developers new to Nostr | Need the note journey and host/guest ownership model; basic web concepts only. | A napplet owns signing, relays, storage, and policy. | Story/System ownership table; choose an owner and denied direct-authority path. | `DRF-DISCOVERY-001`, `DRF-HANDSHAKE-001`; blocked upstream baseline. |
| Existing Nostr developers | Need to compare familiar client concerns with mediated authority; know events, relays, signers. | Existing client conventions establish napplet domains. | Source-status comparison; mark proposal as evidenced, blocked, or stale. | `DRF-MANIFEST-001`, `DRF-EGRESS-001`; blocked. |
| General web/application developers | Need browser-boundary reasoning; know browser messaging and deployment. | An iframe or simulation proves protocol behavior. | Trust Map and static transcript; separate browser observation, policy, and protocol statement. | `DRF-EGRESS-001`, `DRF-UNKNOWN-MESSAGES-001`; blocked. |
| Runtime implementers | Need an evidence checklist for host responsibilities; know loaders and policy. | Archive diagrams select required runtime architecture. | Runtime X-ray; classify component and name missing pin/measurement. | `CLM-CMP-RUNTIME-001`, `DRF-HANDSHAKE-001`, `DRF-INTENT-001`; blocked. |
| Protocol contributors | Need an honest routing model; know specs/proposals/implementations. | A proposal or observation settles a normative behavior. | Specification Map; identify an invented assumption and route an open question. | `DRF-DISCOVERY-001`, `DRF-METADATA-001`, `DRF-INTENT-001`; blocked. |
| LLMs and coding agents | Need structured provenance behavior; can retrieve records. | A plausible synthesis or Graphify edge is evidence. | ID-backed source-status table; answer with IDs, uncertainty, and fallback. | `CLM-POLICY-001`, `DRF-CONFORMANCE-001`; blocked where upstream proof is required. |

## Teaching safeguards

- Analogies in `jobs-to-be-done.yaml` are conceptual and include their limitations; they never establish host, domain, runtime, or protocol behavior.
- Wire and Code representations are unavailable until an immutable source and compatible measurement support them. A static explanation remains the safe fallback.
- Each audience assessment is a reasoning task, not acronym recall. It must preserve source, claim, drift, and open-question IDs.
- Required approvals remain protocol-technical and content-learning human review. D-14, D-16, D-18, and D-19 apply: no inferred conclusion becomes verified, normative and observed records remain separate, and material conflict blocks only dependent teaching work.
