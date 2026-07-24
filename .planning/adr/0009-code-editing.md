# ADR 0009 — Code editing

- **Status:** proposed
- **Date:** 2026-07-24
- **Owners:** UI/technical owner (responsible); research owner supplies evidence context.
- **Required approver:** Accessibility reviewer; consult Security reviewer, Content/learning owner, Product owner, and Technical owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 03 public static site; 05 core course and workbench expansion.
- **Source refs:** `SRC-POLICY-001`, `SRC-POLICY-002`; `CLM-POLICY-001`, `CLM-UPSTREAM-BASELINE-001`; `CMP-BASELINE-001`; `DRF-CONFORMANCE-001`, `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`; `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `OQ-UPSTREAM-BASELINE-001`.
- **Evidence IDs:** Plan 01-28 spike-consolidation audit (SPK-J disposition: `no-impact-fragment`); `CLM-POLICY-001`; `CMP-BASELINE-001`; `DRF-CONFORMANCE-001`; `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`.
- **Impacts:** Requirements `EVID-04`, `OPER-03`; phases 01, 02, 03, and 05.
- **Governance:** Status: proposed. This record neither accepts an editor choice nor authorizes a production editor, package installation, arbitrary learner-code execution, browser workaround, or production scaffold.

## Context

A later lesson may require a learner to make one declared text change while preserving keyboard access, visible and announced state, reset/replay, static equivalence, and host isolation. The decision is costly to reverse once lessons, authoring conventions, and accessibility tests depend on an editing model. The Phase 1 fast path must nevertheless remain a static learning site that does not require an editor.

SPK-J is accounted for in the Plan 01-28 audit as `no-impact-fragment`. Its raw report is explanatory context only: it cannot serve as canonical authority for a browser, package, accessibility, or production-editor conclusion.

## Upstream facts

No current immutable upstream source establishes an editor requirement, code-execution model, package choice, browser support, or host/guest editing contract. `SRC-POLICY-001` is a revision-pinned planning archive and `SRC-POLICY-002` is a revision-pinned project-policy record; both resolve through complete source records but are not upstream editor or protocol facts.

`CLM-UPSTREAM-BASELINE-001`, `CMP-BASELINE-001`, and `DRF-CONFORMANCE-001` retain missing public runtime/package/conformance evidence as blocked work. `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` and `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` retain the observed pre-attachment Firefox toolchain block; they do not establish Firefox support or rejection for any editor.

## Local decision boundary

Choosing the smallest editing affordance for a bounded Learn Napplets exercise is project and accessibility policy. It must not imply upstream protocol behavior, a selected host profile, a package approval, or permission to execute learner text. A trusted future host retains sensitive/repetitive authority; an untrusted future guest receives no arbitrary execution authority merely because a lesson contains editable text.

## Options

**Alternatives:** all options remain reviewable; none is accepted by this record.

### Option A — Fixed tested variants by default, with a controlled native textarea only for one declared edit

Propose fixed, keyboard-reachable variants as the default. Permit a native textarea only when a lesson explicitly needs one small, fixed comparison against declared alternate text, with visible/announced result, reset, static fallback, and no execution.

### Option B — Defer editing interactions

Use static explanations, code samples, transcripts, and reasoning prompts until Phase 2/5 specifies a measured editing need and the required accessibility/security review is complete.

### Option C — Select a full package editor or arbitrary code execution

Use CodeMirror, CodeJar, or another package editor as the default, or execute learner-authored code. This is not supported. CodeMirror's bounded Chrome observation remains raw explanatory context and does not select it; CodeJar remains blocked because its recorded release/source version identities conflict. Any arbitrary execution requirement needs a separate trusted-host/sandbox architecture and security review.

## Evidence

**Canonical evidence and provenance.** Plan 01-28's immutable audit records SPK-J as `no-impact-fragment`, with report SHA-256 `48ceace6a76927b2cb4fd7881235bff926a7524621885e1aa98a1c4cf03e3321`, metadata SHA-256 `05a510beee8e88e8a68113d3abe95a21ae74efdeac355daea39512b27bfca1c5`, and measurement SHA-256 `2407701d1128ad1ac076a9c050f4f7b6bb3e0d0b0658ccc4a52de7114d3b6b1b`. The audit's rerun-input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`. This provenance accounts for SPK-J without upgrading its prose into canonical decision evidence.

**Project policy.** `CLM-POLICY-001` resolves to complete immutable `SRC-POLICY-002` provenance and requires source identity, classification, and human review. The project boundary requires deterministic required paths and static, transcript/state-inspection, keyboard, reduced-motion, reset, and replay equivalents.

**Observed/explanatory context.** SPK-J's raw report records bounded Chrome fixture checks of fixed variants, a controlled native textarea, and a fixed-document CodeMirror harness; it also records zero attached Firefox fixture results and no observed assistive-technology speech. Those local observations are not canonical facts, cross-browser evidence, production accessibility evidence, or a package-selection basis.

**Inference.** Given the bounded learning objective and absent canonical positive editor evidence, fixed variants are the smallest evidence-aware proposal; a controlled native textarea is narrower than a package editor. This is a proposal, not acceptance.

## Decision

**Proposed recommendation only:** carry Option A into Phase 2/5 review as the least-authority editing constraint. The minimum Phase 3 static learning site may use Option B and does not depend on an editor. Do not select CodeMirror, remove the CodeJar blocker, install an editor package, execute learner text, or change ADR status in Phase 1.

## Host/guest implications

A future host must not execute learner-entered text or hand host authority to a guest editor. Any optional bounded text input must compare against declared constants, keep status and reset inspectable, and preserve static alternatives. It does not establish a guest sandbox, package integration, browser containment, or a real runtime path.

## Human/LLM implications

Lessons and knowledge outputs must label the fixed variant, controlled edit, simulation status, source/claim IDs, uncertainty, and blocked package/browser evidence from common structured records. An editor UI, rendered success marker, or code literal cannot become a second source of truth or conceal the absence of protocol/package evidence.

## Consequences

- Keeps the minimum static learning site independent of an editor dependency and optional complex capability.
- Provides a narrowly reviewable route for a declared textual edit without arbitrary code execution.
- Retains CodeMirror as unselected contextual evidence and CodeJar as blocked, rather than silently substituting another package.
- Defers a costly editor, sandbox, package-maintenance, and accessibility contract until a real lesson need is approved.

## Risks

- Treating SPK-J raw fixture output as canonical production, browser, or accessibility evidence would violate the consolidation boundary.
- The Firefox pre-attachment blocker and absent assistive-technology observation could be obscured by Chromium-only output.
- A package editor could expand dependency, bundle, maintenance, and execution surface without an approved need.
- A future request for arbitrary learner execution could breach host/guest authority unless separately designed and reviewed.

## Uncertainty

**Uncertainty:** Material for browser coverage, assistive technology, production bundle/isolation, package maintenance, and any execution model; limited only to the raw disposable fixture context.

`CMP-BASELINE-001`, `DRF-CONFORMANCE-001`, `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`, and the linked open questions remain blocked. No consolidation-issued SPK-J impact record provides positive editor-selection evidence.

## Revisit triggers

- **Revisit trigger:** Phase 2/5 approves a concrete learning objective that cannot be met by fixed variants or a controlled native textarea.
- A consolidation-issued successor provides complete immutable source/package provenance, accessibility and cross-browser measurements, and the required accessibility/security/content review.
- The approved Firefox attached-context route changes under separate review; do not use a launcher workaround, browser configuration, managed download, or substitute browser to erase the blocker.
- A CodeMirror/CodeJar release, root export, source identity, dependency review, or measurement changes; CodeJar's identity conflict remains blocked until independently resolved.
