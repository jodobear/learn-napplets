# ADR 0011 — Source freshness

- **Status:** proposed
- **Date:** 2026-07-24
- **Owners:** Research owner (responsible); technical owner supplies implementation context.
- **Required approver:** Protocol/technical owner; consult Content/learning owner and Release owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 03 public static site; 05 teaching-host work; 11 quality, launch, and maintenance.
- **Source refs:** `SRC-POLICY-001`, `SRC-POLICY-002`; `CLM-POLICY-001`, `CLM-UPSTREAM-BASELINE-001`; `CMP-BASELINE-001`; `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`; `OQ-UPSTREAM-BASELINE-001`.
- **Evidence IDs:** Plan 01-28 spike-consolidation audit (SPK-L disposition: `no-impact-fragment`); `CLM-POLICY-001`; `CLM-UPSTREAM-BASELINE-001`; `CMP-BASELINE-001`; `DRF-ARTIFACT-001`; `DRF-CONFORMANCE-001`; `OQ-UPSTREAM-BASELINE-001`.
- **Impacts:** Requirements `EVID-02`, `EVID-04`, `OPER-01`, `OPER-03`; phases 01, 02, 03, 05, and 11.
- **Governance:** Status: proposed. This record sets no accepted refresh cadence, does not auto-change a claim or ADR, and does not authorize live-source retrieval, network probing, or a Phase 2 transition.

## Context

Protocol-sensitive learning content must remain traceable to a revision, locator, digest, retrieval date, authority, evidence class, maturity, uncertainty, and review state. Freshness policy is costly to change after citations, generated knowledge, compatibility records, and release checklists depend on it. A stale or ambiguous source must produce review work rather than silently rewriting evidence.

SPK-L is accounted for in the Plan 01-28 audit as `no-impact-fragment`; its raw local fixture report is explanatory context only. It cannot prove a live source changed, determine the meaning of a changed source, choose a global cadence, or accept an ADR.

## Upstream facts

No current immutable upstream protocol/package/runtime source is available to establish a domain-specific refresh interval or current protocol truth. `SRC-POLICY-001` and `SRC-POLICY-002` are complete immutable planning/project-policy records. `CLM-UPSTREAM-BASELINE-001` is a blocked policy claim that records the missing official baseline; it is not a claim about protocol behavior.

`CMP-BASELINE-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`, and `OQ-UPSTREAM-BASELINE-001` retain the unresolved immutable-source, public artifact, and conformance evidence. These records require review before dependent claims can move; they do not make unavailability equivalent to freshness.

## Local decision boundary

Recording source identity, comparing a candidate against retained identity, routing non-unchanged states to named review work, and assigning human approvers are Learn Napplets evidence-maintenance policy. This policy must distinguish a mechanical identity difference from semantic meaning and must never rewrite accepted evidence, claim classification, approval, or ADR status automatically.

The D-20/D-36 direction is targeted refresh: retain old identity, scope the affected source/claim/drift/ADR records, and create stable review-required work for changed, moved, unavailable, or ambiguous results. It is not a live-system dependency or an autonomous decision mechanism.

## Options

**Alternatives:** all options remain reviewable; none is accepted by this record.

### Option A — Propose identity-pinned, targeted refresh review

For every fact-bearing source, retain immutable identity and compare revision/path/digest on the applicable refresh trigger. Unchanged evidence remains unchanged; changed or moved identity creates targeted stale review; unavailable or ambiguous identity remains blocked. Reviewers determine meaning, update impacts, and approve any later claim/ADR change.

### Option B — Defer freshness policy until source acquisition completes

Keep only the current evidence register and wait for official source collection before proposing refresh behavior. This avoids a policy recommendation but leaves no repeatable way to expose stale state.

### Option C — Use time-based automatic refresh or overwrite accepted evidence

Treat a scheduled recheck, unavailable response, or changed digest as authority to replace records, verify claims, change approvals, or accept ADRs. This is prohibited because mechanical comparison cannot supply semantic review or upstream authority.

## Evidence

**Canonical evidence and provenance.** Plan 01-28's audit records SPK-L as `no-impact-fragment`, with report SHA-256 `452c5f824c15df942deb8630b5eea4cadde27f32598d9bf8a53dfee92f47bd2d`, metadata SHA-256 `96814da6ab39d241639b2c7ce69f08056cb757dddf3ffe950a82a3a9ffd9df9a`, and measurement SHA-256 `ce7b85a04c9833b197a1e2d6c0c2b2b0f55e4e4e8ebeecb11c57187c82d7588d`. The Plan 01-28 rerun-input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`. This accounts for SPK-L without making raw report prose a canonical freshness fact.

**Observed/explanatory context.** SPK-L's raw fixture report describes deterministic local unchanged/repeated, changed-digest, moved-path, unavailable, ambiguous, and lock-contention scenarios. It reports that canonical bytes were not rewritten. This is local tool-routing context, not an upstream observation, cadence measurement, or semantic review.

**Project policy and inference.** `CLM-POLICY-001` and `SRC-POLICY-002` require immutable identity and human review. The evidence-supported local-policy proposal is Option A: use source identity plus targeted, stable review work so stale state remains visible and provenance history is preserved. The proposal remains pending protocol/technical approval.

## Decision

**Proposed recommendation only:** carry Option A into Phase 2/3/11 evidence-maintenance review. Retain D-20/D-36 targeted refresh behavior and a source-refresh review requirement, but do not set a mandatory cadence, fetch sources, rewrite claims, accept an ADR, or mark an unavailable source fresh. The minimum static learning site may proceed only with approved, visibly labeled evidence; it cannot rely on live external systems for required learning paths.

## Host/guest implications

Freshness maintenance does not give a host, guest, package, verifier, or external adapter any authority. A later lab must use pinned deterministic inputs and label their source status; a live source check cannot become a required learner interaction. Any optional host/guest content affected by stale evidence must retain its static/transcript/replay fallback until review resolves the impact.

## Human/LLM implications

Human-facing citations and machine-readable knowledge must derive source identity, state, uncertainty, impacted claims, and review status from common structured records. A regenerated page or model output cannot silently normalize a stale, moved, ambiguous, or blocked source. Review work must reveal the old identity, proposed new identity, scope, owner, and required approval.

## Consequences

- Makes stale-state handling attributable without declaring a changed source semantically understood.
- Preserves the static deterministic teaching path when external sources are unavailable.
- Keeps package/public-export, manifest, identity, verifier, browser, and protocol gaps visible instead of treating a refresh process as evidence resolution.
- Requires coordinated evidence and release review when an accepted source change affects content, compatibility, or decisions.

## Risks

- A digest/path change may be mistaken for semantic equivalence or a protocol conclusion.
- A fixed cadence could miss high-risk changes or produce noise; source volatility remains unknown.
- Automated mutation of claims, ADR status, or approvals would bypass the approval matrix and conceal stale evidence.
- Unavailable/ambiguous sources could be accidentally rendered as current if the blocked disposition is not preserved.

## Uncertainty

**Uncertainty:** Material.

The SPK-L fixture demonstrates local routing only. It does not establish live-source volatility, a sufficient cadence, semantic equivalence, upstream truth, or fresh status for unavailable evidence. `CLM-UPSTREAM-BASELINE-001`, `CMP-BASELINE-001`, the artifact/conformance drift records, and `OQ-UPSTREAM-BASELINE-001` remain blocked.

## Revisit triggers

- **Revisit trigger:** any fact-bearing source revision, path, locator, digest, authority/evidence class, maturity, retrieval record, package release/export, or compatibility measurement changes.
- A targeted refresh emits changed, moved, unavailable, ambiguous, or lock-conflict review work; retain old identity and require the named protocol/technical review before updating dependent claims or ADRs.
- A reviewer measures actual source volatility or identifies a content/release impact that warrants a specific cadence or escalation policy.
- Phase 2/3/11 changes the structured-source, citation, deterministic-learning, release, or risk-acceptance contract.
