# Learn Napplets

## What This Is

Learn Napplets is an independent, interactive learning product for the napplet ecosystem. It combines a progressive course, architecture explorer, deterministic browser labs, real example napplets, developer onboarding, runtime/protocol contribution guidance, and structured knowledge outputs for LLMs.

It is not a canonical protocol specification, complete Nostr course, or exhaustive package API reference.

## Core Value

Learners can accurately understand and exercise the boundary where focused, untrusted napplet code delegates dangerous or repetitive authority to a trusted host.

## Requirements

### Validated

(None yet — source-pack import does not validate product or protocol requirements.)

### Active

- [ ] Establish a revision-pinned research and truth baseline before production implementation.
- [ ] Define a buildable product/content contract from accepted evidence and ADRs.
- [ ] Deliver static-first, accessible learning content with deterministic labs and real napplets where educational.
- [ ] Keep host/guest authority, protocol facts, project policy, and implementation details explicit.
- [ ] Generate human-readable and machine-readable knowledge from common structured sources.
- [ ] Verify quality, security, accessibility, browser compatibility, learning outcomes, and source freshness before release.

### Out of Scope

- Replacing upstream specifications — upstream projects remain authoritative.
- Teaching all of Nostr — include only concepts required by later lessons.
- Requiring live relays, wallets, signers, devices, or public services for required learning — core paths stay deterministic.
- Exposing real signing keys or building production wallets/signers — conflicts with teaching safety.
- Presenting one runtime implementation as mandated architecture — distinguish protocol from implementation.
- Turning every component into a napplet — use ordinary web components where boundary behavior is not educational.
- Allowing an optional course/workbench napplet to block public-site v1 — ADR 0007 controls portable scope.

## Context

The received v3 planning pack is preserved at `docs/learn-napplets-codex-pack-v3/`. It contains a coherent charter, research plan, 11 source phases (0–10), quality/security/accessibility expectations, prompts, templates, and an ADR queue. It has not executed Phase 0: no current upstream snapshots, accepted ADRs, source registry, compatibility matrix, mandatory spike evidence, or lesson research packets exist.

Canonical live planning resides in `.planning/`. Source-pack references to `.planning/STATUS.md` map to `.planning/STATE.md`; no second mutable status file is maintained.

Primary audiences:
- developers new to Nostr;
- existing Nostr developers;
- general web/application developers;
- runtime implementers;
- protocol contributors;
- LLMs and coding agents.

Recurring learning scenario: journey of one note — compose, save, identify, request publish, apply policy, sign, route, resolve viewer, render.

## Constraints

- **Upstream authority**: Protocol-sensitive claims require current, immutable source evidence; project docs never override upstream facts.
- **Research gate**: No production application scaffold before source Phase 0 and product-contract Phase 1 pass.
- **Trust boundary**: Public teaching host and guest napplet builds must remain separate authority domains.
- **Determinism**: Required learning paths cannot depend on live external systems.
- **Accessibility**: Interactive material needs keyboard, reduced-motion, transcript, and static equivalents.
- **Human/LLM parity**: Essential facts must come from common structured sources, not visuals or component literals alone.
- **Honest maturity**: Facts, proposals, implementation behavior, and project policy must be labeled separately.
- **State authority**: `.planning/STATE.md` is sole live GSD status source.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Preserve nested v3 pack unchanged | Keeps received baseline recoverable and auditable | — Pending validation |
| Use `.planning/` as canonical GSD workspace | Gives GSD one authoritative state model | — Pending validation |
| Map source phases 0–10 to GSD phases 1–11 | GSD uses positive sequential phase numbering | — Pending validation |
| Use guarded automation | Gain speed without crossing ADR, UAT, security, external-action, or release gates | — Pending validation |
| Deep-converge Phase 1/source Phase 0 plan | Research assumptions are high-risk and upstream-sensitive | — Pending review |
| Delay Graphify until canonical planning validates | Avoid indexing ambiguous/noncanonical state | — Pending validation |

## Evolution

This document evolves at phase transitions and milestone boundaries. Each transition reviews validated/active/out-of-scope requirements, key decisions, core value, and current context.

---
*Last updated: 2026-07-23 after canonical GSD initialization*
