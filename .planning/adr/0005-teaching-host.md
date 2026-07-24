# ADR 0005 — Teaching-host architecture

- **Status:** proposed (`Status: proposed`)
- **Date:** 2026-07-24
- **Owners:** Technical owner (responsible); research owner supplies evidence context.
- **Required approver:** Security reviewer; consult Protocol/technical owner, Accessibility reviewer, Content/learning owner, and Product owner.
- **Related phases:** 01 research baseline; 02 product/content contract; 05 core course and workbench expansion.
- **Source refs:** `SRC-POLICY-001`, `SRC-POLICY-002`; `CLM-UPSTREAM-BASELINE-001`, `CLM-POLICY-001`; `CMP-BASELINE-001`; `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `DRF-EGRESS-001`, `DRF-MANIFEST-001`, `DRF-IDENTITY-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`; `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `OQ-EGRESS-NIP-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-VERIFIER-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`.
- **Evidence IDs:** `SPK-C-IMPACT-001`, `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, `SPK-H-IMPACT-001`; `CMP-BASELINE-001`.
- **Impacts:** Requirements `EVID-03`, `EVID-04`, `OPER-03`; phases 01, 02, and 05.
- **Governance:** Status remains proposed. This record neither selects a runtime nor authorizes a production host, loader, browser workaround, package dependency, CSP exception, or guest implementation.

## Context

Later learning material may need to demonstrate the authority boundary between a public teaching host and an untrusted guest. Phase 1 recorded narrow local fixtures, but every protocol-sensitive host, manifest, identity, verifier, package, and cross-browser conclusion remains blocked. This ADR therefore proposes a review boundary, not a runtime architecture.

## Upstream facts

No current immutable upstream fact establishes a teaching-host profile, guest capability set, manifest/identity rule, verified-loader behavior, package export, browser egress rule, or portable runtime contract. `CLM-UPSTREAM-BASELINE-001` is blocked and resolves to the complete immutable project-policy/archive sources `SRC-POLICY-001` and `SRC-POLICY-002`; it records the missing upstream baseline rather than supplying protocol truth.

`CMP-BASELINE-001` is blocked for public package, runtime, example, and fixture compatibility. Its claim links include `CLM-CMP-PACKAGE-001`, which forbids inferring behavior from private/deep paths or unpublished builds. `DRF-MANIFEST-001`, `DRF-IDENTITY-001`, `DRF-ARTIFACT-001`, and `DRF-CONFORMANCE-001` remain blocked; no manifest, identity, signature/blob/aggregate verifier, release artifact, or conformance behavior is settled.

## Local decision boundary

The separation of sensitive/repetitive authority into a future trusted teaching host and the confinement of any future guest to declared mediated capabilities is Learn Napplets project policy. A future host profile must be scoped to reviewed measurements and product requirements; it must not imply that an upstream protocol mandates a particular iframe, loader, CSP, message envelope, identity model, or browser capability.

The terms below remain distinct:

- **Required source behavior:** absent and blocked pending immutable reviewed upstream sources.
- **Observed browser behavior:** exact local Chromium fixture observations only, recorded by canonical `SPK-C-IMPACT-001` and `SPK-H-IMPACT-001`; Firefox supplied no attached-context observation.
- **Possible architecture:** a later, separately reviewed top-level observer plus opaque-origin, `sandbox="allow-scripts"` guest may remain a bounded fixture-shaped candidate only.
- **Host policy:** a restrictive, reviewable public-site CSP is proposed project policy only (`SEF-BROWSER-EGRESS-001`); it is neither upstream requirement nor accepted security decision.
- **External adapter:** any manifest resolver, identity mapper, package, signature/blob/aggregate verifier, relay, signer, wallet, or remote service is out of scope until exact public provenance and approval exist.

## Options

**Alternatives:** all options remain reviewable; none is accepted by this record.

### Option A — Propose a static-first, profile-scoped teaching boundary

Carry forward the smallest future direction: public static learning content remains independently useful; any optional guest demonstration receives only explicitly declared, mediated capabilities from a separately reviewed trusted host. Preserve the static/transcript/state-inspection/reset/replay fallback whenever the optional guest path is unavailable.

### Option B — Defer any host-profile recommendation

Retain only the evidence registry and do not propose even a bounded host profile until immutable source, browser, package, identity, and verifier evidence is reviewed. This minimizes architectural direction but leaves Phase 2/5 without an explicit authority boundary for review.

### Option C — Propose a verified-loader or reusable package host

Treat manifest/identity/verifier and package integration as the primary future profile. This is blocked: `SPK-D-IMPACT-001` confirms only supplied-byte digest integrity, while `SPK-G-IMPACT-001` confirms no qualified public package was available or executed. No hand-rolled cryptography, substitute package, private path, or deep import is permitted.

## Evidence

**Canonical consolidation evidence.** Plan 01-28 records `SPK-C-IMPACT-001`, `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, and `SPK-H-IMPACT-001` as the decision-evidence IDs. Each fragment pins its report, metadata, measurement, source-registry, and SHA-256 records. The consolidation audit has rerun-input digest `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85` and expressly prevents raw report prose from becoming upstream fact.

**Traceable evidence paths.** `SPK-C-IMPACT-001` and `SPK-H-IMPACT-001` link to `SRC-POLICY-001` (and SPK-H to `SRC-POLICY-002`), whose related claims are `CLM-UPSTREAM-BASELINE-001` and `CLM-POLICY-001`; `SPK-D-IMPACT-001` and `SPK-G-IMPACT-001` link to both sources and their blocked claims. These links reach immutable commit, path, locator, digest, retrieval, authority, evidence-class, and maturity fields in the source registry through the claims record. They establish evidence provenance and blocking status, not upstream host behavior.

**Observed implementation and browser behavior.** The canonical fragments retain five Chromium fixture samples for bounded source-window mapping, deterministic responses, and local egress checks. They also retain the Firefox `152.0.4` outcome: the direct-installed process exited before Playwright `1.61.0` attached, so zero Firefox fixture samples exist. This blocks a cross-browser success claim across SPK-C/H and must remain visible without launcher workaround, browser configuration change, download, or substitute browser result.

**Verified-loader and package limits.** `SPK-D-IMPACT-001` retains supplied-byte and one-byte-mutation digest observations only; current immutable manifest/identity source records and reviewed signature/blob/aggregate/loader provenance are absent. `SPK-G-IMPACT-001` retains the public-package gate: no exact public release, root export, provenance, integrity, or implementation baseline exists. The blocked records require no substitute/private/deep package path.

**Inference.** Option A is the narrowest project-policy direction consistent with the evidence: keep the public static site fast path independent of optional host/guest demonstrations. It is not a full runtime, a compatibility finding, or an accepted architecture.

## Decision

**Proposed recommendation only:** carry Option A to Phase 2 and later security/protocol review as a profile-scoped, static-first teaching boundary. The public learning site must be able to proceed without a guest host path. A future guest must have no host authority and may receive only declared mediated capabilities after its source, browser, security, and accessibility evidence is reviewed. Preserve Options B and C as explicit alternatives and leave all external adapters blocked.

## Host/guest implications

A future public host owns sensitive or repetitive authority; a future guest remains untrusted and guest-only. Required learning paths cannot depend on a live service, real signing key, wallet, relay, package, verifier, or portable runtime. Any local fixture must remain deterministic, disclose simulated versus real behavior, offer keyboard/reduced-motion/transcript/state-inspection/reset/replay/static equivalents, and never turn the teaching host into a full runtime.

`SPK-C-IMPACT-001` and `SPK-H-IMPACT-001` preserve an opaque-origin `srcdoc` guest with `sandbox=allow-scripts` and top-level observer as a measured fixture shape only. `SEF-BROWSER-EGRESS-001` remains proposed project policy; it cannot become a production CSP or upstream egress rule without required security and protocol review.

## Human/LLM implications

Human-facing lessons and machine-readable knowledge outputs must label upstream facts, local observations, project policy, proposals, and inferences separately. The static path must carry essential authority-boundary meaning without requiring the optional guest. Any future host/guest lesson, transcript, state inspection, or knowledge output must trace claims through common structured evidence records and retain source, claim, maturity, uncertainty, and status.

## Consequences

- Gives Phase 2/5 a narrowly reviewable authority boundary without selecting a runtime.
- Keeps the public-site fast path independent of verified-loader, package, portable, and cross-browser blockers.
- Preserves the Firefox pre-attachment block and all source/provenance gaps rather than masking them as compatibility.
- Defers costly host, adapter, fixture, and capability contracts until reviewers can inspect immutable evidence.

## Risks

- A local Chromium fixture could be mistaken for cross-browser, upstream, or production-host proof.
- Treating byte-digest replay as cryptographic verification would bypass the immutable manifest/identity/verifier provenance blocker.
- Treating the package gate as a compatibility success could invite an unsafe substitute or private/deep import.
- Treating proposed CSP policy as an upstream requirement or accepted security exception could overstate evidence.

## Uncertainty

**Uncertainty:** Material.

`SPK-C-IMPACT-001`, `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, and `SPK-H-IMPACT-001` are materially uncertain and/or blocked. Required reviewer roles remain pending. The Firefox `152.0.4` / Playwright `1.61.0` pre-attachment outcome leaves no Firefox fixture result. The static fallback is the safe path, not evidence that the unresolved host profile works.

## Revisit triggers

- Revisit trigger: collect and review official immutable host/runtime, manifest, identity, verifier, package-root-export, public conformance, and browser-egress evidence; reopen if a referenced commit, path, locator, or digest changes.
- **Measurement trigger:** obtain Firefox attached-context observations under a separately reviewed environment change; do not use a launcher workaround, browser configuration change, managed download, or substitute browser to erase the block.
- **Security trigger:** security and protocol-technical review approves or rejects a concrete CSP/capability boundary, with any exception recorded under the approval matrix.
- **Product trigger:** Phase 2 accepts or changes deterministic static-path, structured-content, and accessibility requirements; any request for live adapters or guest authority reopens this ADR.
