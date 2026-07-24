# ADR 0004 — Content source model

- **Status:** proposed
- **Date:** 2026-07-24
- **Owners:** Content/technical owner (responsible); research-owner supplies evidence context.
- **Required approver:** Product owner; consult Content/learning owner, Accessibility reviewer, Security reviewer, and Technical owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 03 independent repository foundation; 10 knowledge and LLM hardening.
- **Source refs:** SRC-POLICY-001, SRC-POLICY-002; CLM-POLICY-001; CLM-UPSTREAM-BASELINE-001; CMP-BASELINE-001; DRF-INTENT-001; DRF-UNKNOWN-MESSAGES-001; OQ-UPSTREAM-BASELINE-001.
- **Evidence IDs:** SPK-E-CONTENT-RENDERING; CLM-POLICY-001; CMP-BASELINE-001; CLM-CMP-EXAMPLE-001; DRF-INTENT-001; DRF-UNKNOWN-MESSAGES-001; OQ-UPSTREAM-BASELINE-001.
- **Impacts:** Requirements EVID-03, EVID-04, OPER-03; phases 01, 02, 03, and 10.
- **Governance:** Status: proposed. This is not authorization to create a production renderer, source schema, route, guest integration, or second authoring source.

## Context

Learners and LLMs need essential facts from common structured sources rather than visuals, component literals, or disconnected AI-only documents. A future content contract must preserve provenance, claim, terminology, maturity, uncertainty, and status across human-readable and machine-readable representations. Phase 1 can test parity with one bounded local record but cannot select a production schema or renderer.

## Upstream facts

No current immutable upstream protocol, content, runtime, package, or example baseline defines the content model. `CLM-UPSTREAM-BASELINE-001` and `OQ-UPSTREAM-BASELINE-001` preserve that state as blocked review work. `CMP-BASELINE-001` and `CLM-CMP-EXAMPLE-001` are blocked; they do not establish example, guest, or protocol compatibility.

`DRF-INTENT-001` and `DRF-UNKNOWN-MESSAGES-001` remain blocked because no immutable catalog or message-behavior source has been collected. `SRC-POLICY-002` and `CLM-POLICY-001` are project-policy evidence requiring immutable identity and human review; they govern handling of content facts but do not prove an upstream semantic model. `SRC-POLICY-001` remains planning archive context only.

## Local decision boundary

The choice to require a common structured content record and field-level representation parity is a Learn Napplets product/content decision. The precise source schema, renderer, routes, guest content integration, authoring workflow, LLM retrieval format, and accessibility implementation remain for the Phase 2 product/content contract and later human approval.

## Options

**Alternatives:** Option A, Option B, and Option C below remain reviewable; none is accepted by this record.

### Option A — Propose one structured content source with required parity fields

Carry forward a content-model constraint: essential human-facing and machine-facing outputs should derive from one structured record and preserve source ID, claim ID, terminology, maturity, uncertainty, and status with target-level parity validation.

### Option B — Defer common-source requirements until Phase 2

Retain the evidence but make no content-model proposal until a complete curriculum, source-status, and LLM strategy are approved. This avoids early contract direction but risks later surfaces diverging before parity expectations are specified.

### Option C — Permit representation-specific authoring

Allow each static page, guest content object, transcript, glossary, and knowledge artifact to become a separate source of truth. This is rejected as a proposed direction because it conflicts with the project boundary requiring essential human and LLM facts from common structured sources; it remains documented as an alternative for review rather than silently excluded.

## Evidence

**Canonical evidence and provenance.** The Plan 01-28 consolidation audit records SPK-E as explanatory `no-impact-fragment` context: report SHA-256 `26503edcec77a0a65b44dfbd5c2a75a987390be3530a2bc18d7fc54e8a425588`, metadata SHA-256 `623490c15e47fc73478147c4d1a7cddf86fe055de8fa0cf2c33b81da4e1c6d3c`, and measurements SHA-256 `ced41b4a399597f131d7a3368bc1122e9bca052c81c1f7e796a267d6314c2cb8`. The consolidation rerun input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`; it does not elevate report prose to upstream authority.

**Observed local implementation behavior.** Five deterministic local SPK-E replays generated six representations—static HTML, guest content JSON, Markdown, glossary entry, transcript, and knowledge JSON—from one bounded project-policy fixture. Each retained `sourceId=SRC-POLICY-002`, `claimId=CLM-POLICY-001`, terminology `immutable source record`, maturity `accepted`, `uncertaintyState=limited`, and `status=provisional`; each target was parsed back and checked for exact field parity. Every replay had the same manifest SHA-256 `c54ce3b7997783f2407fb45af0fe5f7c46685888f0a57faab8abd3f4e2c1796b`. The outputs remained isolated under `/tmp`, were not committed as content assets, and are not a production renderer.

**Project policy.** `CLM-POLICY-001` requires immutable source identity and human review before verification. The project boundary requires essential human and LLM facts to derive from common structured sources. `CLM-UPSTREAM-BASELINE-001` prohibits treating this local record as a protocol conclusion.

**Inference.** Option A is a plausible future content-contract constraint because it preserved the specified field values across six formats. It does not establish semantic completeness, real-interface accessibility, LLM response quality, guest protocol behavior, security, framework viability, or production renderer selection.

## Decision

**Proposed recommendation only:** carry Option A into Phase 2 as a content-contract constraint: one structured source of essential facts, explicit provenance/status fields, and representation-level parity validation. Keep Option B and Option C visible for review. Do not add a production schema, renderer, content route, guest integration, or authoring system in Phase 1; product-owner acceptance remains required.

## Host/guest implications

A shared structured source could later supply public-site and guest-facing content without granting guest code host-only authority. It does not define guest loading, sandboxing, host capability mediation, package export, or protocol semantics. Firefox Playwright attachment is still blocked; manifest, identity, verifier, package/public-export, browser egress, and portable-target uncertainty remain separate unresolved evidence.

## Human/LLM implications

Option A directly supports human/LLM parity: a public page, glossary, transcript, and knowledge artifact would trace essential facts to the same structured record and visibly preserve source/status fields. The local parity experiment does not prove that an LLM retrieves or reasons correctly, that all content is accessible, or that any representation may suppress required context. Phase 2 must define schema completeness, authoring governance, accessibility, and retrieval evaluation.

## Consequences

- Gives Phase 2 a small, evidence-scoped common-source constraint without creating a renderer.
- Makes provenance, maturity, uncertainty, and status parity testable rather than relying on visual or prose-only consistency.
- Preserves exact canonical controlled values where no separate terminology/maturity/uncertainty/status IDs exist; it does not invent a parallel ID system.
- Requires future content, accessibility, and knowledge work to coordinate schema and validation changes.

## Risks

- The bounded fixture could be overgeneralized into a complete content or LLM-quality solution.
- A future schema that omits status/provenance fields can silently undermine human/LLM parity.
- Copying content into per-surface literals can create a second source of truth.
- Unresolved upstream semantic, package, manifest, identity, verifier, browser, and portable-target gaps must not be hidden by a content-model decision.

## Uncertainty

**Uncertainty:** Material for production and protocol conclusions; limited for the bounded local parity observation.

The fixture demonstrates deterministic parity for one synthetic/project-policy record only. `CMP-BASELINE-001`, `DRF-INTENT-001`, `DRF-UNKNOWN-MESSAGES-001`, and `OQ-UPSTREAM-BASELINE-001` remain blocked. No production renderer, framework, guest runtime, browser accessibility result, security boundary, or LLM-quality evaluation was tested.

## Revisit triggers

- **Revisit trigger:** Phase 2 approves or changes the content/source-status/LLM contract, including required field vocabulary or representation set.
- A parity measurement discovers a missing field, target encoding mismatch, inaccessible representation, or a second source of truth.
- Immutable upstream source, runtime, example, catalog, or message-behavior evidence is collected and reviewed, or the referenced claim/source digests change.
