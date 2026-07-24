# Lesson Research Packet — The Cast and Mental Model

- **Lesson ID:** LES-002
- **Primary audience:** Developers new to Nostr, runtime implementers, and LLMs/coding agents consuming structured records.
- **Prerequisites:** LES-001 conceptual ownership model or equivalent understanding that evidence state limits teaching claims.
- **Last researched:** 2026-07-24

## Learner question

Which terms describe a proposed napplet ecosystem mental model, and which distinctions remain unresolved until authoritative sources are pinned?

## Intended outcome

Learners can classify terms as project policy, unresolved upstream terminology, or implementation-specific language; they can avoid treating a shell, runtime, projection, capability domain, convention, or archetype as settled protocol vocabulary.

## Current terminology

- **NIP-5D**, **NIP-5A**, **NAP registry**, and **NAP projection** are `blocked` unresolved-upstream terms in `terminology-map.yaml`.
- **Capability bootstrap** is a project-policy label with `blocked` protocol meaning.
- **Shell** and **runtime** are useful teaching labels from preserved planning context, but their protocol scope, relationship, and internal layering have no current immutable official baseline.
- **Archetype** and **convention** remain candidate catalog categories; they are not selected or verified current behavior.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-UPSTREAM-BASELINE-001` | project-policy | accepted | `SRC-POLICY-001` / `SRC-POLICY-002`, source and verification rules | `blocked`: upstream terminology cannot be concluded. |
| `CLM-CMP-RUNTIME-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, research completion and freshness | `blocked`: no credible runtime baseline is available. |
| `CLM-DRF-METADATA-NORMATIVE` | project-policy | accepted | `SRC-POLICY-002`, Freshness | `provisional`: requires immutable registry evidence before metadata meaning is concluded. |

## Implementation and runtime evidence

There is no selected runtime, shell, projection, package, or example napplet evidence. The only current implementation disposition is that runtime compatibility is blocked. Any diagram that assigns ownership or communication paths is a conceptual taxonomy, not an implementation observation.

## Drift and open questions

- `DRF-HANDSHAKE-001` is **blocked**: bootstrap behavior lacks immutable protocol and runtime evidence.
- `DRF-METADATA-001` is **blocked**: registry/projection metadata has no immutable baseline.
- `DRF-INTENT-001` is **blocked**: handler/catalog assumptions are unpinned.
- `OQ-UPSTREAM-BASELINE-001` is the dated, impact-scoped path for resolving these terms.

## Misconceptions to address

- A labeled architecture atlas does not define protocol vocabulary.
- A runtime's internal layering, if later observed, is not automatically a required host architecture.
- A capability/domain/convention label should not be used as evidence that a request is authorized or interoperable.

## Story representation

**Conceptual simulation:** A learner receives term cards and sorts them into `project policy`, `unresolved upstream term`, `possible implementation observation`, and `needs immutable source`. Cards display their stable evidence IDs rather than implied definitions.

## System representation

**Conceptual simulation:** An ownership map may depict a proposed application, boundary, host, runtime, projection, domain, convention, and archetype as separate questions. It must not draw a guaranteed handshake, injection path, or authority assignment.

## Wire representation

No validated handshake, manifest, or message envelope is available. The static alternative is an evidence-state transcript naming `DRF-HANDSHAKE-001`, `DRF-METADATA-001`, and `DRF-INTENT-001` as blocked.

## Code representation

No current package/global API can be shown. Present a non-executable vocabulary data record with term classifications and source IDs rather than class names, imports, or host APIs.

## Candidate instrument

- **Conceptual simulation:** Architecture Atlas term-card sorter with a static table and state-inspection transcript.
- **Provenance:** conceptual simulation; it must never identify itself as a real runtime or browser boundary.
- **Safety boundary:** no dynamic imports, untrusted code, capabilities, or external service calls.

## Required fixtures and tests

- Deterministic term-card fixture populated only from `terminology-map.yaml` classifications and this packet's citations.
- Keyboard and static-table equivalents; reduced-motion does not change meaning.
- Validator/test coverage that blocked terms retain an explicit source or open-question ID and are not displayed as verified definitions.

## Do not teach as settled

- `CLM-UPSTREAM-BASELINE-001` and `CLM-CMP-RUNTIME-001` are **blocked**; no shell/runtime scope or behavior is established.
- `DRF-HANDSHAKE-001`, `DRF-METADATA-001`, and `DRF-INTENT-001` are **blocked**; bootstrap, metadata, and handler meanings are unresolved.
- `CLM-DRF-METADATA-NORMATIVE` is **provisional** project policy, not evidence of an upstream registry rule.

- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
- `CLM-DRF-METADATA-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `OQ-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** All relevant candidates remain discovery pointers without immutable current evidence. **Impact:** requirements EVID-02, EVID-03, OPER-01; phases 01.
- `CLM-CMP-RUNTIME-001` — **state: blocked**. **Reason:** Runtime candidates remain unpinned discovery pointers. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `DRF-HANDSHAKE-001` — **state: blocked**. **Reason:** No immutable NIP-5D bootstrap baseline or observed runtime baseline has been collected. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `DRF-METADATA-001` — **state: blocked**. **Reason:** No immutable registry or projection baseline has been collected. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `DRF-INTENT-001` — **state: blocked**. **Reason:** Handler and catalog sources lack immutable released and current-work baselines. **Impact:** requirements EVID-02, EVID-03; phases 01.
## Follow-up research

- Use `OQ-UPSTREAM-BASELINE-001` to acquire and review official NIP-5D/NIP-5A, registry, projection, runtime, and current-work records.
- Compare normative sources and observed implementations as parallel records under D-12 and D-16; do not collapse them into an atlas fact.
- Replace only the affected conceptual cards once the relevant claim has immutable evidence and required human review.
- `CLM-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** Candidate discovery pointers lack a complete official identity, resolved revision:path blob, digest, and human technical review. **Impact:** requirements EVID-01, EVID-02; phases 01.
- `CLM-CMP-RUNTIME-001` — **state: blocked**. **Reason:** Runtime candidates remain unpinned discovery pointers. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `CLM-DRF-METADATA-NORMATIVE` — **state: provisional**. **Reason:** This is a governing evidence rule, not an upstream protocol conclusion. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `DRF-HANDSHAKE-001` — **state: blocked**. **Reason:** No immutable NIP-5D bootstrap baseline or observed runtime baseline has been collected. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `DRF-METADATA-001` — **state: blocked**. **Reason:** No immutable registry or projection baseline has been collected. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `DRF-INTENT-001` — **state: blocked**. **Reason:** Handler and catalog sources lack immutable released and current-work baselines. **Impact:** requirements EVID-02, EVID-03; phases 01.
- `OQ-UPSTREAM-BASELINE-001` — **state: blocked**. **Reason:** All relevant candidates remain discovery pointers without immutable current evidence. **Impact:** requirements EVID-02, EVID-03, OPER-01; phases 01.
