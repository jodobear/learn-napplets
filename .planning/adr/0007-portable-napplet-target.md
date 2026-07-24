# ADR 0007 — Portable napplet target

- **Status:** proposed (`Status: proposed`)
- **Date:** 2026-07-24
- **Owners:** Product owner (responsible); research owner supplies evidence context.
- **Required approver:** Product owner; consult Technical owner, Content/learning owner, Accessibility reviewer, Security reviewer, and Release owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 05 core course and workbench expansion; 08 optional portable napplet target.
- **Source refs:** `SRC-POLICY-001`, `SRC-POLICY-002`; `CLM-UPSTREAM-BASELINE-001`, `CLM-POLICY-001`; `CMP-BASELINE-001`; `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`; `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `OQ-UPSTREAM-BASELINE-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`.
- **Evidence IDs:** Plan 01-28 all-spike consolidation audit (`SPK-F` disposition: `no-impact-fragment`); `CMP-BASELINE-001`; `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`.
- **Impacts:** Requirements `EVID-03`, `EVID-04`, `OPER-03`; phases 01, 02, 05, and optional 08.
- **Governance:** Status remains proposed. This record selects no outcome, creates no portable artifact, grants no guest authority, and does not delay the public-site sequence.

## Context

The project may later offer an optional portable course/workbench napplet, but its public static learning site must not wait for that work. SPK-F measured a disposable guest-only static simulation under limited conditions and preserved a cross-browser blocker. Plan 01-28 classified SPK-F as `no-impact-fragment`; its raw report is explanatory context only, never canonical decision evidence. This ADR lists the required outcome choices so product review can decide later without implying that Phase 1 selected one.

## Upstream facts

No current immutable upstream source establishes a portable napplet artifact, loading, storage, resource, link, composition, package-export, host-capability, or browser-compatibility contract. `CLM-UPSTREAM-BASELINE-001` and `CMP-BASELINE-001` preserve missing source/compatibility evidence. `SRC-POLICY-001` and `SRC-POLICY-002` are revision-pinned planning/project-policy records; they do not prove portable runtime behavior.

`DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` records a tooling result, not browser support or rejection: Firefox `152.0.4` exited before Playwright `1.61.0` attached. `DRF-ARTIFACT-001` and `DRF-CONFORMANCE-001` remain blocked. `CLM-CMP-PACKAGE-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, and `OQ-PUBLIC-CONFORMANCE-001` prohibit deriving a portable target from a private, substitute, unpublished, deep, workspace, `src/`, or `dist/` package path.

## Local decision boundary

Whether to ship an optional portable guest-only learning target is a Learn Napplets product roadmap decision. It must remain separate from the faster public-site path. Any portable artifact would be a guest, not a host: it cannot own sensitive/repetitive authority, signing material, wallet, relay, secrets, arbitrary learner code execution, or unreviewed external adapters.

A simulated course/workbench must visibly label synthetic/deterministic behavior. It must not present a local static simulation as real napplet composition, mediated capability, current artifact behavior, or cross-browser support.

## Options

**Alternatives:** all four outcome states are exact review choices; none is selected by this record.

### Option A — `GO-V1`

Include a portable target in the public v1 scope only after reviewed immutable upstream source/package/runtime evidence, accessible cross-browser measurements, a Phase 2 product/content contract, and product approval establish that it has sufficient learning value without weakening the host/guest boundary. This is not supported by current evidence.

### Option B — `GO-LATER`

Keep a portable target as a planned later capability after the public static site. This retains option value while allowing source acquisition, Firefox attached-context evidence, package/export provenance, and product value review to mature. It is not an authorization to build now.

### Option C — `WORKBENCH-ONLY`

Permit a bounded, clearly simulated, guest-only workbench after separate review, without presenting it as a portable public target or making it a required learning path. It must retain deterministic static equivalents and cannot provide host authority. This option remains unselected.

### Option D — `NO-GO`

Skip the portable target for this milestone if value, safety, accessibility, compatibility, or maintenance evidence remains insufficient. The public site continues; this option is not a failure of the public learning product.

## Evidence

**Canonical consolidation status.** Plan 01-28's all-spike audit records SPK-F as `no-impact-fragment`. Its report, metadata, and measurement digests are pinned in the audit, but no `SPK-F-IMPACT-*` canonical target exists. Therefore the raw SPK-F report can explain its fixture conditions and outcome vocabulary but cannot support an ADR fact, selected option, or portable-runtime conclusion.

**Traceable policy and blocker paths.** `CLM-POLICY-001` resolves to the complete immutable `SRC-POLICY-002` record and governs separation of observation, policy, inference, provenance, uncertainty, and human review. `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` and `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` retain the browser automation gap as canonical blocked evidence. `CMP-BASELINE-001` resolves through blocked package/runtime/example/fixture claims to immutable source records; it makes absent evidence visible rather than upgrading it to compatibility.

**Explanatory local context only.** The raw SPK-F report describes one guest-only static two-lesson simulation, deterministic static outputs in an approved disposable environment, bounded Chromium checks, and Firefox pre-attachment exit. It explicitly states no `GO-V1`, `GO-LATER`, `WORKBENCH-ONLY`, or `NO-GO` outcome was selected. The report also preserves SPK-B's independent VitePress reduced-motion/static-equivalent assertion failure; SPK-F output does not resolve or supersede that failure. These statements are context, not canonical portable-target evidence.

**Approved versus blocked dependencies.** The SPK-F fixture used dated human-approved disposable `astro@7.1.3` and `vitepress@1.6.4` releases only within its deleted experiment; that approval did not authorize production packages or a portable target. The napplet package candidate remains blocked under `CLM-CMP-PACKAGE-001` and canonical `SPK-G-IMPACT-001`: no exact public release, root export, provenance, integrity, or distinct implementation baseline is available.

**Inference.** The public static learning site can move through Phase 2 approval without a portable result. Deferring, narrowing, or skipping the optional target is safer than making a blocked guest-only simulation a public-site dependency.

## Decision

**Proposed recommendation only:** preserve all four outcome states for product-owner review and explicitly decouple them from the public-site fast path. Phase 2 may progress toward a minimum static learning site after its own approval even if ADR 0007 remains proposed, deferred, narrowed, or results in `NO-GO`. Do not choose an outcome, create a portable artifact, or turn a simulation into a required path during Phase 1.

## Host/guest implications

If later authorized, a portable target is guest-only and receives only declared mediated capabilities from a separately reviewed trusted host. It must not become a host, claim real signing/identity/loader authority, or substitute a local mock for an external system. Required learning remains deterministic and works with static/transcript/state-inspection/reset/replay/reduced-motion/keyboard equivalents even when the portable target is unavailable.

## Human/LLM implications

Course pages and knowledge outputs must label real behavior, deterministic simulation, proposal, blocked evidence, and inference separately. The public static site must expose essential facts from common structured records rather than relying on the optional portable artifact. Any future workbench must preserve the same provenance, uncertainty, and status labels in human and machine-readable views.

## Consequences

- Keeps public-site v1 fast while source, browser, accessibility, package, and portable evidence stays unresolved.
- Gives product review four explicit, reversible outcome states rather than an implicit binary commitment.
- Prevents guest-only simulations from being misrepresented as real portable napplet or host behavior.
- Defers a costly portable artifact contract until evidence and product value warrant it.

## Risks

- A local disposable build could be confused with real artifact, composition, or browser conformance.
- The Firefox pre-attachment blocker could be hidden by Chromium-only output or a launcher/configuration workaround.
- The independently unresolved VitePress accessibility/static-equivalent failure could be misrepresented as resolved.
- A package substitute/private/deep path could bypass public-package provenance and supply-chain review.

## Uncertainty

**Uncertainty:** Material.

No canonical SPK-F impact record supports a positive portable target conclusion. Firefox has no attached-context result; SPK-B's VitePress accessibility failure remains unresolved; package, runtime, artifact, composition, host authority, and public conformance baselines remain blocked. No outcome state may be upgraded without product-owner approval and new reviewed evidence.

## Revisit triggers

- Revisit trigger: Phase 2 establishes the learning-value, deterministic-path, guest-authority, accessibility, and public-site success contract for any optional portable target.
- A consolidation-issued canonical portable feasibility impact record links immutable sources, package/export provenance, cross-browser measurements, and required reviewer approvals.
- Firefox attached-context measurements become available under a separately reviewed environment change; no launcher workaround, browser configuration change, download, or substitute browser may erase the blocker.
- SPK-B's VitePress reduced-motion/static-equivalent failure is independently resolved or remains a reviewed blocker, and any approved package release/provenance/digest changes.
