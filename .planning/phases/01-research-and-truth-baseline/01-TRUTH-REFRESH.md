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
