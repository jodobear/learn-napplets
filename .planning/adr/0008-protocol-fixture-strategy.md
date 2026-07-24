# ADR 0008 — Protocol fixture strategy

- **Status:** proposed (`Status: proposed`)
- **Date:** 2026-07-24
- **Owners:** Test owner (responsible); research owner supplies evidence context.
- **Required approver:** Protocol/technical owner; consult Security reviewer, Technical owner, Content/learning owner, Accessibility reviewer, and Product owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 05 core course and workbench expansion.
- **Source refs:** `SRC-POLICY-001`, `SRC-POLICY-002`; `CLM-UPSTREAM-BASELINE-001`, `CLM-POLICY-001`, `CLM-CMP-FIXTURE-001`, `CLM-CMP-PACKAGE-001`; `CMP-BASELINE-001`; `DRF-MANIFEST-001`, `DRF-IDENTITY-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`, `DRF-EGRESS-001`; `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-VERIFIER-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`, `OQ-EGRESS-NIP-001`, `OQ-UPSTREAM-BASELINE-001`.
- **Evidence IDs:** `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`; `CMP-BASELINE-001`; Plan 01-28 spike-consolidation audit and replay-manifest digest `679be644f14a77b6c40528a74aea29e530837ef2db731a24ac13f8d4d4177d93`.
- **Impacts:** Requirements `EVID-03`, `EVID-04`, `OPER-03`; phases 01, 02, and 05.
- **Governance:** Status remains proposed. This record authorizes no protocol fixture, verifier, package, network adapter, public conformance claim, or production loader.

## Context

Deterministic lessons and later labs need testable examples without live relays, wallets, signers, accounts, devices, or external services. The fixture strategy must preserve source provenance, keep simulations visibly bounded, and avoid inferring protocol truth from synthetic bytes. Canonical SPK-D and SPK-G evidence show that loader, package, public fixture, and conformance evidence remain blocked; this ADR proposes a safety-first strategy for future review.

## Upstream facts

No current immutable upstream manifest, identity mapping, signature/blob/aggregate verifier, loader implementation, public package release/export, conformance target, or fixture baseline has been collected and reviewed. `CLM-CMP-FIXTURE-001` and `CLM-CMP-PACKAGE-001` are blocked claims, each linked through complete immutable source records to describe absence and required evidence, not to establish protocol behavior.

`DRF-MANIFEST-001`, `DRF-IDENTITY-001`, `DRF-ARTIFACT-001`, and `DRF-CONFORMANCE-001` remain blocked. `DRF-EGRESS-001` remains a separate blocked browser-egress question. No fixture may convert project policy, planning archive context, a digest match, or a local fake into a normative protocol statement.

## Local decision boundary

A future Learn Napplets fixture strategy is project test/content policy. It may require deterministic local fake external systems, schema validation, compatibility records, replayability, static alternatives, and explicit source/status labels. It must not define upstream message, identity, manifest, signature, blob, aggregate, loading, egress, package, or conformance semantics.

All fixture claims must be classified as one of: revision-pinned upstream fact, proposal/draft, observed local implementation behavior, project policy, or inference. Lessons must disclose where a fake replaces a live external system and must not make the fake a hidden authority source.

## Options

**Alternatives:** all options remain reviewable; none is accepted by this record.

### Option A — Propose a pinned, deterministic fixture baseline

For future approved lessons, use only fixtures whose source revision/path/locator/digest/retrieval/authority/evidence-class/maturity record is complete; validate the fixture's own schema; pin its bytes and measurements; record compatibility separately; and replace external systems with deterministic fakes carrying explicit simulation labels. Treat any unsupported protocol-sensitive field as blocked.

### Option B — Defer all protocol-shaped fixtures

Use only general static content until official immutable protocol and verification sources exist. This minimizes interpretation risk but provides no reusable deterministic lab/fixture direction for later review.

### Option C — Use synthetic bytes or a package as a verified-loader/conformance substitute

Promote supplied-byte hashing, local fake behavior, package compilation, or a private/deep package path into loader or conformance evidence. This is blocked by `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, `CLM-CMP-FIXTURE-001`, and `CLM-CMP-PACKAGE-001`. No cryptography may be hand-rolled; no package, verifier, resolver, key, blob, aggregate, manifest, identity tuple, or private path may be substituted.

## Evidence

**Canonical consolidation evidence.** `SPK-D-IMPACT-001` and `SPK-G-IMPACT-001` are Plan 01-28's consolidation-issued decision-evidence IDs. They pin report, metadata, measurement, source-registry, and digest links. The consolidation audit's rerun-input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`; its replay manifest preserves reproducibility inventory and does not accept an ADR or upgrade fixture behavior to upstream fact.

**Traceable evidence paths.** Both impact fragments cite `SRC-POLICY-001` and `SRC-POLICY-002`, which resolve through `CLM-UPSTREAM-BASELINE-001`, `CLM-POLICY-001`, `CLM-CMP-FIXTURE-001`, and `CLM-CMP-PACKAGE-001` to records containing immutable URL, repository, commit, path, locator, digest, retrieval date, authority, evidence class, maturity, uncertainty, impacts, and review state. These paths establish provenance and present blockers; they do not validate a protocol fixture.

**Observed local implementation behavior.** `SPK-D-IMPACT-001` retains five deterministic local byte-integrity observations: supplied bytes matched their pinned digest and a one-byte mutation matched a different pinned digest. It explicitly retains all manifest resolution, identity mapping, signature verification, blob verification, aggregate verification, and exact-byte loader surfaces as `not-run`/blocked. Digest equality is not cryptographic verification.

`SPK-G-IMPACT-001` retains a dependency-free gate outcome: zero qualifying public releases, installs, imports, conformance targets, or private/deep imports were attempted. This is supply-chain blocker evidence only; it is not package availability, compatibility, or conformance success.

**Inference.** Option A is the narrowest project strategy that can support deterministic teaching artifacts without claiming unavailable protocol semantics: pin sources and local fixture artifacts, validate structure, use explicit deterministic fakes, preserve compatibility blockers, and omit unsupported claims. It does not authorize a fixture implementation before review.

## Decision

**Proposed recommendation only:** carry Option A into Phase 2/5 review as a fixture-policy constraint. A later approved fixture must: (1) trace every technical fact, adapter, package, and lesson citation through `CLM-*` to a complete immutable `SRC-*` record; (2) validate its own schema and preserve source/fixture/measurement digests; (3) use deterministic, visibly simulated fakes for external systems; (4) record compatibility and drift independently; and (5) leave unresolved inputs explicitly blocked. Do not create a fixture, verifier, loader, package integration, or protocol implementation in Phase 1.

## Host/guest implications

A future deterministic fixture may emulate a narrowly declared external response for educational replay, but it cannot grant a guest host-only authority or impersonate a real signer, wallet, relay, loader, identity service, or package. The trusted host remains responsible for any later mediated capability. Required paths must remain deterministic and usable through static/transcript/state-inspection/reset/replay/keyboard/reduced-motion equivalents when an optional lab is unavailable.

## Human/LLM implications

Fixture-driven lessons and machine-readable knowledge must expose a common structured record for source ID, claim ID, source class, maturity, uncertainty, simulation status, expected input/output, fixture digest, and compatibility state. Human readers and LLMs must be able to distinguish a pinned upstream fact from a local fake and a blocked claim. A rendered success marker cannot conceal unavailable verifier/package/protocol evidence.

## Consequences

- Establishes a reviewable path for deterministic fake systems without live external dependencies.
- Makes fixture provenance, schema validation, compatibility records, and limitations explicit and testable.
- Prevents byte hashes, package gates, or local outputs from being misrepresented as cryptographic, loader, or conformance proof.
- Defers actual verifier, adapter, package, and protocol fixture implementation until immutable source and approval gates are met.

## Risks

- A deterministic fake may be mistaken for a real protocol, service, signer, wallet, or runtime interaction.
- An incomplete claim-to-source path could leave a lesson citation dangling or hide a stale source.
- Hand-rolled cryptography or an unreviewed verifier could create a security-critical false assurance.
- A substitute/private/deep package path could bypass public release, root-export, provenance, integrity, and supply-chain review.
- A fixture could become an accidental host authority surface if simulated guest/host roles are not explicit.

## Uncertainty

**Uncertainty:** Material.

`SPK-D-IMPACT-001` and `SPK-G-IMPACT-001` retain blocked manifest, identity, verifier, package, fixture, and conformance conclusions. No public conformance fixture or qualified package was executed. Current source records govern evidence handling but do not establish protocol behavior. Any fixture behavior beyond its declared deterministic local simulation requires new source evidence, compatibility records, and human review.

## Revisit triggers

- Revisit trigger: official immutable manifest, identity, verifier, package-root-export, release artifact, and public conformance fixture records are collected, linked through reviewed `CLM-*` claims, or any referenced revision/path/locator/digest changes.
- A schema-validation, provenance, replay, compatibility, or human/LLM parity check finds a missing field, nondeterministic fake, mislabeled simulation, or dangling citation.
- Protocol/technical and security reviewers accept, reject, or request changes to a concrete fixture/adapter design; no automated ADR acceptance is permitted.
- Phase 2 changes deterministic-learning, content-source, accessibility, or lab requirements, or a later host/guest capability introduces a new trust boundary.
