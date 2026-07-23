# Learn Napplets Plan Audit

**Audited:** 2026-07-23  
**Input:** Codex Build Pack v2  
**Output:** Codex Build Pack v3

## Verdict

The v2 framing was fundamentally correct:

- the learning product is an independent repository;
- the public website may act as a teaching host;
- selected lessons should use real napplets;
- a Workbench or full-course napplet is a separate untrusted guest build;
- upstream NIP/NAP documents remain authoritative;
- human and LLM outputs should derive from one content model.

The plan was not yet tight enough to hand to Codex unchanged. The main issues were avoidable implementation rework, an over-broad first research phase, ambiguous evidence/status labels, and several protocol-sensitive questions that needed to be made explicit blockers.

## Findings and corrections

| Severity | Finding | Correction in v3 |
|---|---|---|
| High | Phase 4 allowed simulated boundary behavior and Phase 5 then replaced it with a real teaching shell. | Phase 4 now delivers the first real end-to-end vertical slice with a minimal production teaching shell and actual lab napplet. Phase 5 expands it rather than replacing it. |
| High | `NORMATIVE DRAFT` mixed source authority with ecosystem maturity and could imply a draft proposal is settled. | Claims now use separate `evidenceClass` and `maturity` axes. Public labels distinguish current NIP draft, current NAP proposal, implementation observation, project decision, and open question. |
| High | Current composition/manifest drift was generally acknowledged but not listed as a blocking research checklist. | Phase 0 now explicitly investigates capability discovery, NAP-SHELL, NIP-5D versus NIP-5A manifest framing, `dTag` identity for manifest kinds without a `d` tag, archetype/convention tags, and NAP-INTENT handler identity. |
| High | The plan did not require an empirical outbound-network and CSP analysis, despite the security model depending on mediated access. | Added a mandatory browser-egress/security spike and a clear separation between NIP assertions, browser behavior, and the public site's own CSP policy. |
| Medium | Phase 0 asked Codex to deeply inspect too many proposals, branches, and technical options at once. | Research is now tiered. Codex inventories the whole ecosystem but deep-reads only sources that affect the MVP, unresolved drift, or active implementation decisions. |
| Medium | The public teaching shell could be mistaken for a complete conformant runtime. | Added declared teaching-host profiles: boundary harness, verified loader, selected-domain host, and composition host. The site may claim only the profile it has implemented and tested. |
| Medium | The pack hard-coded “single-file” in product-level descriptions outside a source-verification context. | Product language now says “current-compatible napplet artifact.” The current artifact shape is verified and pinned during Phase 0 before build rules are implemented. |
| Medium | Document precedence was implicit, increasing the risk that duplicate wording would diverge. | Added an explicit precedence order: `AGENTS.md`, accepted ADRs/research, canonical project docs, phase prompt, templates/examples. Conflicts must be flagged. |
| Medium | The v1 cut line was not exact. | v3 defines a content MVP, an interactive MVP, and a v1 minimum. The v1 minimum includes the public site, declared teaching host, at least three real lab napplets, the thirteen-lesson course, core labs, source/status pages, and machine outputs. |
| Medium | Upstream reproducibility relied on commit SHA alone. | Source records now include path, immutable URL, content digest, observed time, and section locator. A compatibility matrix ties source revisions to package/runtime revisions. |
| Medium | A new empty repository and unavailable upstream network were not handled explicitly. | Codex must initialize the documentation baseline when needed and must stop protocol conclusions when current sources cannot be fetched; memory is not an acceptable substitute. |
| Low | “Shell” and “runtime” were used loosely. | The course must teach shell as the NIP-5D web host and runtime as the broader projection-neutral host concept, while marking internal runtime decomposition as implementation-specific. |
| Low | Knowledge outputs lacked a schema/version migration rule. | Added `schemaVersion`, stable-ID deprecation/alias rules, and versioned knowledge endpoints. |

## Current protocol-sensitive reasons for the stronger research gate

The living NIP-5D file currently defines domain availability through the presence of `window.napplet.<domain>`, NIP-5D-specific manifest kinds, verified `srcdoc` loading, and an `allow-scripts` opaque-origin iframe. Parts of the current NAP registry and web-projection text still describe `shell.supports()`, NAP-SHELL, and NIP-5A kind `35128`. Current NAP-INTENT and archetype documents also build on those registry assumptions. These are upstream drift items, not decisions the learning project should resolve by invention.

## Tightened execution sequence

```text
0  Research and truth baseline
1  Product and content contract
2  Independent repository foundation
3  Visual/content primitives
4  Real end-to-end vertical slice
5  Core course and Workbench expansion
6  Composition, patterns, and app design
7  Build, runtime, and contribution chapters
8  Optional portable napplet artifact
9  Knowledge and LLM hardening
10 Quality, launch, and maintenance
```

## Recommended handoff

Give Codex only `prompts/00-PHASE-0-RESEARCH.md` first. Review the source registry, drift register, compatibility matrix, security findings, teaching-host profile, and ADR 0007 delivery-mode decision before authorizing implementation.

## Sources checked for this audit

- Living NIP-5D file: `https://raw.githubusercontent.com/nostr-protocol/nips/refs/pull/2303/head/5D.md`
- NIP-5D pull request: `https://github.com/nostr-protocol/nips/pull/2303`
- Current NAP registry: `https://raw.githubusercontent.com/napplet/naps/master/README.md`
- Current web projection: `https://raw.githubusercontent.com/napplet/naps/master/projections/web.md`
- Current archetype registry: `https://raw.githubusercontent.com/napplet/naps/master/ARCHETYPES.md`
- Current NAP-INTENT proposal: `https://raw.githubusercontent.com/napplet/naps/master/naps/NAP-INTENT.md`
