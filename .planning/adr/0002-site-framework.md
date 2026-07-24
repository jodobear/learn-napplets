# ADR 0002 — Site framework

- **Status:** proposed
- **Date:** 2026-07-24
- **Owners:** Technical owner (responsible); research-owner supplies evidence context.
- **Required approver:** Product owner; consult Security reviewer and Release owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 03 independent repository foundation.
- **Source refs:** SRC-POLICY-001, SRC-POLICY-002; CLM-UPSTREAM-BASELINE-001; CMP-BASELINE-001; DRF-ARTIFACT-001; OQ-UPSTREAM-BASELINE-001.
- **Evidence IDs:** SPK-B-STATIC-FRAMEWORK; CMP-BASELINE-001; CLM-CMP-PACKAGE-001; CLM-CMP-RUNTIME-001; DRF-ARTIFACT-001; OQ-UPSTREAM-BASELINE-001.
- **Impacts:** Requirements EVID-03, EVID-04, OPER-03; phases 01, 02, and 03.
- **Governance:** Status: proposed. This recommendation is not a framework selection, package approval for production, or authorization to scaffold.

## Context

The future public learning site needs a static-first path that can eventually render structured content, preserve public/lab separation, and meet accessibility and deterministic-learning constraints. Phase 1 compares only a disposable local fixture. The framework choice is costly to reverse after build interfaces and content integration exist, so the evidence and its limits must remain visible.

## Upstream facts

No current immutable upstream napplet/runtime/package compatibility baseline supports a production framework decision. `CMP-BASELINE-001` is blocked, including `CLM-CMP-PACKAGE-001` and `CLM-CMP-RUNTIME-001`; its project-policy facts say that public package and runtime evidence is missing, not that any framework is compatible or incompatible.

`DRF-ARTIFACT-001` is blocked because no public package release or exact build-output evidence has been pinned. `SRC-POLICY-001` is planning-archive context and `SRC-POLICY-002` is project policy. They are immutable project records, but neither is an upstream framework or protocol fact.

## Local decision boundary

Selecting a site framework is a Learn Napplets delivery decision. The project must preserve static-first output, deterministic required paths, accessibility support, content parity, and a future separation between public site, host authority, and guest entries. This ADR does not determine host/guest runtime behavior, protocol compatibility, deployment, or package public export.

## Options

**Alternatives:** Option A, Option B, and Option C below remain reviewable; none is accepted by this record.

### Option A — Carry Astro 7.1.3 as the proposed static-first candidate

Use the SPK-B package-approved local fixture result as evidence for later review of Astro `7.1.3`. The proposal is limited to the recorded disposable environment and does not initialize Astro or select it for the project.

### Option B — Defer framework selection

Keep both candidates unselected until the Phase 2 product/content contract, official compatibility sources, and any additional accessibility measurements are reviewed. This avoids commitment but delays a reviewable Phase 3 direction.

### Option C — Retain VitePress 1.6.4 as a blocked alternative

Do not use VitePress `1.6.4` as positive ADR evidence until a separately reviewed fixture resolves its repeated reduced-motion/static-equivalent assertion failure. Do not substitute an unapproved package or infer equivalence from its stable static pages.

## Evidence

**Canonical evidence and provenance.** The Plan 01-28 consolidation audit records SPK-B as explanatory `no-impact-fragment` context: report SHA-256 `3c47d39388afb79f96bbf893eaf5e414cd2267ab8d466ac1428d03a2133e1c10`, metadata SHA-256 `7d2b688cf0b163d6bceac2aef405441abe9ffd625aa6556ea9d39a9c9b423809`, and measurement SHA-256 `12019091bb5221bea64909f828e89e371626cbb9a4ced8aedf034d8d74725275`. The consolidation audit rerun input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`; it prohibits promoting report prose to an upstream fact.

**Observed local implementation behavior.** In the recorded Node `v22.22.0` / npm `10.9.4` disposable fixture, Astro `7.1.3` passed 5/5 replay samples with stable static-output SHA-256 `ec7e951d45a25fdcf0648263164a81e6709ade51ae8d9e3723bf3130b69eec94`. VitePress `1.6.4` built stable static pages but failed 5/5 because the declared accessibility assertion could not find `prefers-reduced-motion`. These observations do not establish browser interaction, production accessibility, protocol behavior, or framework suitability beyond the fixture.

**Project policy.** `SRC-POLICY-002` / `CLM-POLICY-001` require evidence identity and human review. `CLM-UPSTREAM-BASELINE-001`, `CMP-BASELINE-001`, and `DRF-ARTIFACT-001` require the project not to infer current public-package/runtime compatibility from local output.

**Inference.** The smallest evidence-supported direction is to offer Astro `7.1.3` for later static-first review while retaining VitePress as an unresolved accessibility blocker. This is a proposal, not a selection.

## Decision

**Proposed recommendation only:** carry Option A to later technical and product-owner review as the candidate framework direction for a smallest static-first public site. Preserve Option B and Option C explicitly. Do not initialize a framework, create a production manifest, install packages, or change ADR status in Phase 1.

## Host/guest implications

A static-first framework could later render public content and bounded local-lab entry points, but this fixture does not prove trusted-host/untrusted-guest containment, mediated capability behavior, browser interoperability, or portable guest support. The Firefox Playwright attachment block, VitePress accessibility evidence gap, package/manifest/identity/verifier gaps, and portable-target uncertainty remain untouched.

## Human/LLM implications

The recorded fixture included structured content support paths, but it does not establish a content schema or a human/LLM output pipeline. Any framework adopted later must render from the accepted common structured source and keep source, maturity, uncertainty, and status visible; ADR 0004 and Phase 2 supply that contract.

## Consequences

- Provides a reproducible local candidate instead of treating a framework decision as implicit.
- Keeps VitePress's repeated reduced-motion/static-equivalent failure visible rather than obscuring it with its static-output result.
- Avoids a production package manifest, scaffold, framework runtime, or deployment setup.
- Changing framework after Phase 3 would require coordinated migration of content, tests, build interfaces, and deployment integration.

## Risks

- The Astro fixture outcome could be mistaken for full accessibility, browser, or security evidence.
- The VitePress failure could be ignored rather than resolved by an independently reviewed measurement.
- Existing Firefox Playwright attachment, package/public-export, manifest, identity, verifier, and portable-target gaps could invalidate assumptions outside this narrow fixture.

## Uncertainty

**Uncertainty:** Material.

**Material.** The five replay samples measure only a local disposable fixture. `CMP-BASELINE-001`, `DRF-ARTIFACT-001`, and `OQ-UPSTREAM-BASELINE-001` are blocked; none supplies current official package/runtime compatibility. VitePress lacks the required accessibility/static-equivalent fixture evidence. No browser run occurred for SPK-B.

## Revisit triggers

- **Revisit trigger:** the approved package release, registry integrity/manifest digest, or recorded fixture environment changes.
- A separately reviewed VitePress reduced-motion/static-equivalent measurement passes or establishes a durable blocker.
- Official immutable runtime/package/public-export evidence is collected and reviewed, or `CMP-BASELINE-001` / `DRF-ARTIFACT-001` changes.
- The Phase 2 content contract changes required accessibility, content, host/guest, or deterministic-lab capabilities.
