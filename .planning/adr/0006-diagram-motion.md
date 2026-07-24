# ADR 0006 — Diagram/motion system

- **Status:** proposed (`Status: proposed`)
- **Date:** 2026-07-24
- **Owners:** UI owner (responsible); research owner supplies evidence context.
- **Required approver:** Accessibility reviewer; consult Content/learning owner, Security reviewer, Protocol/technical owner, and Product owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 04 visual and content primitives; 05 core course and workbench expansion.
- **Source refs:** `SRC-POLICY-001`, `SRC-POLICY-002`; `CLM-POLICY-001`, `CLM-UPSTREAM-BASELINE-001`; `CMP-BASELINE-001`; `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`; `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `OQ-UPSTREAM-BASELINE-001`.
- **Evidence IDs:** Plan 01-28 all-spike consolidation audit (`SPK-I` disposition: `no-impact-fragment`); `CLM-POLICY-001`; `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`.
- **Impacts:** Requirements `EVID-04`, `OPER-03`; phases 01, 02, 04, and 05.
- **Governance:** Status remains proposed. This record does not select a production component, visual library, motion controller, browser-support claim, or accessibility exception.

## Context

Later lessons need diagrams that make essential meaning available without motion, scripting, or a visual dependency. The Phase 1 SPK-I fixture explored a bounded semantic SVG approach, but Plan 01-28 classified SPK-I as `no-impact-fragment`: its raw report may explain context, but it is not canonical decision evidence. This ADR therefore proposes the smallest static baseline as a review direction rather than an accepted visual architecture.

## Upstream facts

No current immutable upstream source defines a Learn Napplets diagram system, required motion behavior, screen-reader result, or browser support contract. `CLM-UPSTREAM-BASELINE-001` is a blocked project-policy claim, not a visual or protocol fact. `SRC-POLICY-001` and `SRC-POLICY-002` supply immutable evidence governance only.

`DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` and `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` preserve the observed tooling block: direct-installed Firefox `152.0.4` exited before approved Playwright `1.61.0` attached, so there is no Firefox fixture, keyboard, screenshot, reduced-motion, transcript/table, or assistive-technology observation to generalize.

## Local decision boundary

Requiring essential diagram meaning to remain available through keyboard navigation, visible focus, reduced-motion behavior, static transcript and table equivalents, state inspection, reset/replay, and a static representation is Learn Napplets product/accessibility policy. Choosing an SVG encoding, data shape, optional motion, component framework, or dependency belongs to later approved implementation work.

The project may propose a static semantic SVG as the smallest baseline, but must not present it as accepted architecture, a cross-browser conclusion, an upstream requirement, or proof of actual assistive-technology speech.

## Options

**Alternatives:** all options remain reviewable; none is accepted by this record.

### Option A — Propose static-first, data-driven semantic SVG with equivalent representations

Use a later data-driven semantic SVG only as the smallest baseline candidate, provided that static transcript/table equivalents, keyboard operation, visible focus, reduced-motion parity, deterministic reset/replay, state inspection, and hostile-input containment preserve all essential meaning. Optional motion may decorate, never carry, authority or required lesson facts.

### Option B — Use static diagram, transcript, and table without SVG interaction

Defer SVG interaction and use a simple static diagram plus transcript and table. This is the safest current fast path because it avoids claiming unresolved browser/accessibility behavior while still conveying essential learning content.

### Option C — Add an executable controller or visual-library dependency

Introduce a script-driven state/motion controller or visual library. This is not supported by canonical decision evidence and should remain deferred until a separately approved need measurement demonstrates that the static baseline cannot meet the Phase 2/4 contract and passes the same accessibility/security boundaries.

## Evidence

**Canonical consolidation status.** Plan 01-28's immutable audit identifies SPK-I as `no-impact-fragment`; its report, metadata, and measurement digests are accounted for in the audit, but no consolidation-issued impact ID exists. Under the downstream evidence rule, raw SPK-I prose is explanatory context only and cannot support an ADR fact or upgrade a recommendation.

**Traceable decision evidence.** `CLM-POLICY-001` resolves through `SRC-POLICY-002` to immutable commit `b534103068be8c07e6869bfb7290fb60fdd87c8c`, path `.planning/governance/evidence-policy.md`, locator, digest, retrieval date, authority/evidence class, and maturity. It requires immutable identity, separated evidence classes, and human review. `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` and `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` are canonical records of the attached-context absence, linked to the same complete project evidence chain. These records support constraints and uncertainty, not production UI behavior.

**Explanatory local context only.** The raw SPK-I report describes five passing Chrome samples of a synthetic zero-JavaScript semantic SVG fixture with keyboard links, visible focus, transcript/table parity, deterministic reset/replay, reduced-motion screenshot parity, and escaped hostile input. It also records the Firefox pre-attachment exit. Because SPK-I has no canonical impact fragment, none of those measurements is treated here as a source of decision fact, cross-browser success, production accessibility claim, or selected architecture.

**Inference.** Options A and B preserve the project requirement that essential meaning has static equivalents; Option B is immediately safe to defer less and lets a minimum static learning site proceed after Phase 2 approval. Option A remains a partially measured, non-production candidate for later review. Option C has no approved evidence of need.

## Decision

**Proposed recommendation only:** carry Option B as the minimum public-site fast path and Option A as the smallest optional later diagram candidate, subject to the Phase 2 contract and accessibility review. Do not add a motion library, state controller, production component, or browser-support claim in Phase 1. Preserve Option C as a deferred alternative, not a rejected or selected implementation.

## Host/guest implications

Diagrams describe a boundary but must not confer authority or become a guest execution surface. The public static site may render a non-executable diagram, transcript, and table independently of any optional napplet. If a later host/guest lesson includes motion or state inspection, it must preserve the static equivalents and label simulation versus real behavior; it must not use the diagram result as host, loader, protocol, or browser-boundary evidence.

## Human/LLM implications

The diagram, transcript, table, state inspection, and machine-readable knowledge outputs must derive essential labels and status from common structured records. Neither a visual-only literal nor a motion-only path may become a second source of truth. Any later SVG data model needs explicit provenance, maturity, uncertainty, and status fields so human and LLM outputs remain aligned.

## Consequences

- Keeps the minimum static learning site independent of optional diagram interaction and unresolved browser automation evidence.
- Makes transcript, table, keyboard, reduced-motion, reset/replay, and state-inspection requirements explicit before optional motion is considered.
- Avoids a visual dependency or dynamic learner-code surface without an approved measured need.
- Defers an expensive cross-phase visual contract until content, accessibility, and source evidence are reviewed.

## Risks

- Treating SPK-I's raw fixture report as canonical evidence would violate the Plan 01-28 consolidation boundary.
- Treating five Chrome samples as cross-browser or production accessibility proof would hide the Firefox pre-attachment blocker.
- Letting motion encode essential authority or protocol facts would exclude reduced-motion, keyboard, transcript, table, static, and machine-readable consumers.
- Adding a controller or dependency without a measured need could create unnecessary security, bundle, and maintenance surface.

## Uncertainty

**Uncertainty:** Material for production, cross-browser, and assistive-technology conclusions; limited only to the explanatory local fixture context.

No canonical SPK-I impact record supports a positive implementation choice. Firefox `152.0.4` remains blocked before Playwright attachment across SPK-C/F/H/I/J; no launcher workaround, browser configuration change, or download was used. Actual screen-reader speech, production bundle behavior, protocol meaning, and runtime isolation have not been measured or accepted.

## Revisit triggers

- Revisit trigger: a reviewed, consolidation-issued canonical SPK-I successor impact record provides immutable source/measurement provenance and passes the applicable semantic ADR contract.
- **Browser trigger:** a separately reviewed environment change produces attached-context Firefox measurements; do not use a launcher workaround, configuration change, managed browser download, or substitute browser.
- **Accessibility trigger:** Phase 2/4 defines or changes static/transcript/table, keyboard, focus, reduced-motion, reset/replay, state-inspection, and assistive-technology criteria.
- **Need trigger:** an approved measurement shows that static representations cannot meet a declared learning requirement and a proposed controller/dependency can meet the same accessibility and authority constraints.
