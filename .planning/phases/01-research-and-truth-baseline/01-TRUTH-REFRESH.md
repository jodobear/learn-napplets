# Phase 01 Truth Refresh — 2026-07-31

## Scope and evidence boundary

This refresh admits four exact immutable source blobs for static explanatory/source-status use. It does not accept an ADR, qualify a package, select a teaching host, prove runtime/browser compatibility, or turn repository behavior or pull-request metadata into NAP/NIP protocol authority.

| Source ID | Immutable identity and locator | Authority / evidence / maturity | Retrieved / SHA-256 | Unresolved impact |
| --- | --- | --- | --- | --- |
| `SRC-NAPS-NAP-INTENT-20260731` | `napplet/naps@5ac0490461ca6fec2f0d2e45b4835cf9bc08de24:naps/NAP-INTENT.md` (blob `3bddd41697d02d825d45191d0122292f7bcaaac6`) | Repository-local NAP specification; `specification`; `draft` | `2026-07-31T03:08:39Z`; `d6a533ea9c132f0196057c177e87452a7c9edda452fea4b89368afc202b709f0` | Its stated NIP-5D web binding does not resolve NIP-5D authority, projection, runtime, or browser gaps. |
| `SRC-NAPPLET-WEB-20260731` | `napplet/web@03ad65b66413e5798536ef48695ffc4c2508f2c3:README.md` (blob `04781fbff0067492f7e1835726c97871983b4036`) | Official repository observation; `implementation`; `implementation-specific` | `2026-07-31T03:08:39Z`; `f21e5bc41a990e40b72124ca68109b63df40b9850758c4346f151ec328ba7dae` | Alpha implementation descriptions, migration direction, and release statements are not normative authority, package qualification, or compatibility proof. |
| `SRC-KEHTO-WEB-PAJA-20260731` | `kehto/web@d42b3c3da7e0ad3cea233b34458997b09b11960d:packages/paja/README.md` (blob `1908af0edbb6695950d8a0e7172374c7d68cf513`) | Official repository observation; `implementation`; `implementation-specific` | `2026-07-31T03:08:39Z`; `dcf02f032bafd87be94297a1995025069df7ff44444b9087d6e1e580ef7e4c33` | Paja's local-authoring and live-relay defaults cannot select the teaching host or establish runtime, Firefox, portability, or package support. |
| `SRC-NAMPLETS-NATIVE-20260731` | `pablof7z/nampplets@1094f1db23292f966fd65757132678406f7ca28c:README.md` (blob `22981ba1fb54a41286c2b186a37a1ab51d9d4561`) | Optional native reference observation; `implementation`; `implementation-specific` | `2026-07-31T03:08:39Z`; `3d1a5165f97bfdb50d3155bbf04044be6bbe63df91385f8e56f1865de2b8874b` | Native-reference behavior is never NAP/NIP authority or a web/portable-target qualification. |

## Directional work kept separate

Pull-request API metadata is mutable directional evidence, not immutable source content. The dated `OWS-004` snapshot records its retrieval-response digests and keeps the records separate from the four source IDs:

- `napplet/web` #186 and #192 are retained as merged implementation migration/INTENT-alignment direction, not protocol facts.
- `napplet/web` #194 is retained as release metadata carrying filesystem-named changesets, not a package-admission or behavior proof.
- `kehto/web` #217 is retained as merged Paja social-cache direction, not runtime qualification.

## Refresh rule

Do not repeat broad discovery. Re-fetch only if a cited upstream head changes after 2026-07-31, a pinned blob becomes unavailable, or a reviewer requires a different source scope. All records remain pending the required human technical/content/security review.

## Site-content handoff

Plan 01-48 may consume only the stable IDs and bounded statements below from common structured records. Each public rendering must retain source, authority/evidence class, maturity, claim state, uncertainty, and blocker labels beside protocol-sensitive material.

### Stable source and claim IDs

| Public ID | Type and state | Source linkage | Site-safe explanatory statement |
| --- | --- | --- | --- |
| `SRC-NAPS-NAP-INTENT-20260731` / `CLM-NAP-INTENT-20260731` | Repository-local NAP draft / provisional claim | `napplet/naps@5ac0490461ca6fec2f0d2e45b4835cf9bc08de24:naps/NAP-INTENT.md` | A draft names NAP-INTENT, an archetype intent dispatcher, and a NIP-5D web binding. It does not resolve direct NIP-5D authority or compatibility. |
| `SRC-NAPPLET-WEB-20260731` / `CLM-NAPPLET-WEB-20260731` | Alpha observed implementation / provisional claim | `napplet/web@03ad65b66413e5798536ef48695ffc4c2508f2c3:README.md` | napplet/web describes its own alpha SDK/shell model. It is not NAP/NIP authority, a package qualification, or runtime/browser proof. |
| `SRC-KEHTO-WEB-PAJA-20260731` / `CLM-KEHTO-WEB-PAJA-20260731` | Observed implementation / provisional claim | `kehto/web@d42b3c3da7e0ad3cea233b34458997b09b11960d:packages/paja/README.md` | Paja documents local authoring/testing, live-relay defaults, and a memory fixture mode. This does not select a teaching host or qualify a runtime. |
| `SRC-NAMPLETS-NATIVE-20260731` / `CLM-NAMPLETS-NATIVE-20260731` | Optional native reference / provisional claim | `pablof7z/nampplets@1094f1db23292f966fd65757132678406f7ca28c:README.md` | Nampplets is an in-progress native reference with an unratified compatibility lock. It does not qualify web, portable, package, or NAP/NIP behavior. |
| `CLM-UPSTREAM-BASELINE-001` / `OQ-UPSTREAM-BASELINE-001` | Project-policy blocker / blocked | Four source IDs above plus policy records and `DRF-*` records | The four sources improve traceability but do not establish a reviewed comprehensive NAP/NIP protocol conclusion or first-lab recommendation. |

### Stable term IDs and labels

- `NAP-INTENT` is a **draft NAP specification term** sourced from `SRC-NAPS-NAP-INTENT-20260731` and must display `provisional` plus `material uncertainty`.
- `napplet/web` and `Paja` are **observed implementation terms** sourced from their respective `SRC-*` IDs and must display `implementation-specific`, `provisional`, and `material uncertainty`.
- `Nampplets native reference` is an **optional native-reference term** sourced from `SRC-NAMPLETS-NATIVE-20260731` and must display `implementation-specific`, `provisional`, and `material uncertainty`.
- `NIP-5D`, `NIP-5A`, `NAP registry`, and `NAP projection` remain **blocked unresolved-upstream terms**. Do not supply a definition beyond that status boundary.

### Topics that remain blocked

| Topic | Record(s) | Required public treatment |
| --- | --- | --- |
| Direct NIP-5D authority, NAP registry, and projection | `CLM-UPSTREAM-BASELINE-001`, `OQ-UPSTREAM-BASELINE-001` | Mark blocked; do not state a protocol rule or selected architecture. |
| INTENT disagreement and migration direction | `DRF-INTENT-001`, `OWS-004` | Show draft versus observed implementation labels; keep PR #192 as mutable direction only. |
| Package/public-artifact qualification | `CLM-CMP-PACKAGE-001`, `DRF-ARTIFACT-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001` | Mark blocked; do not install, link as supported, or claim an export/integrity result. |
| Runtime, browser, and teaching host | `CMP-BASELINE-001`, `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `CLM-CMP-RUNTIME-001` | Mark blocked; do not imply Paja or another implementation is selected or supported. |
| Conformance and native qualification | `DRF-CONFORMANCE-001`, `OQ-PUBLIC-CONFORMANCE-001` | Mark blocked; do not infer conformance from native-reference text or README tooling descriptions. |
| Portability, live services, wallets, signers, and deployment | ADR-0003/0005/0007/0008/0010 proposed plus existing blockers | Exclude from required site behavior and label any mention as deferred/proposed. |

### Required status-label contract

Every static page that renders an essential fact must expose the matching stable ID and these separate fields: **authority tier**, **evidence class**, **maturity**, **claim/record state**, **uncertainty**, **source identity**, and **refresh trigger**. Use `draft`, `observed implementation`, `optional native reference`, `project policy`, `provisional`, and `blocked` literally where applicable. Never flatten these into a single "supported" label.

### Refresh triggers

- Re-fetch a source only when its cited upstream head changes after 2026-07-31, its pinned blob becomes unavailable, or a reviewer requires a different source scope.
- Treat a changed revision, path, digest, authority/evidence/maturity label, package artifact, runtime observation, or review outcome as targeted review work, not an automatic text rewrite.
- Preserve `OWS-004` PR metadata as mutable directional context and retain prior source identity/history when a later refresh is admitted.

### Plan 01-48 consumption boundary

The static site may explain the evidence model and project-policy authority boundary with deterministic HTML, transcript/table equivalents, source/status displays, and no external dependency. It may not turn these records into a runtime, package, host, guest, relay, wallet, signer, browser-compatibility, portable-target, deployment, ADR-acceptance, or Phase 2 claim.
