# Upstream Merge Refresh Synthesis — 2026-07-28

**Scope:** Fully enumerated merged pull requests in the inclusive UTC window `2026-07-25T09:29:46Z`–`2026-07-28T09:29:46Z`: `kehto/web` **5**, `napplet/web` **3**, and `napplet/naps` **0**; total **8**. [VERIFIED: upstream refresh reports]

## Decision Boundary

This is a research-only, implementation-ready refresh map. It records candidate evidence and review work; it does **not** ingest source records, change claim/ADR/matrix/drift/question states, accept an authority claim, or alter Phase 1 gates. GitHub repository identity, merge commits, `commit:path` locators, trees, Git blob IDs, and report diff digests are candidate evidence pending schema ingestion and human review. [VERIFIED: CLAUDE.md; 01-CONTEXT.md D-04, D-06, D-14–D-20]

## Executive Conclusion

The verified public repositories resolve the narrow prior **mutable discovery-pointer identity gap** for the two implementation/release candidates: `napplet/web` (repository ID `1197078677`, `main`) and `kehto/web` (repository ID `1204025151`, `main`) now have public repository identities and immutable implementation anchors. They do **not** resolve the separate authority gap for NAP/NIP protocol specifications, registry/projection/governance semantics, package-registry artifact integrity, root exports, license/provenance, executed runtime behavior, cross-runtime conformance, or human approval. [VERIFIED: upstream refresh reports]

Accordingly, **EVID-03 remains blocked**. The refresh materially improves the acquisition queue from “unverified mutable pointer only” to “public identity plus candidate immutable repository evidence,” but `CMP-BASELINE-001` still lacks a qualified protocol baseline and independently pinned released-package/runtime/example/conformance evidence. **EVID-04 also remains blocked**: source inspection and merged tests are not reproducible local spike evidence, and existing Phase 1 validator/replay/publication integrity defects remain independently unresolved. [VERIFIED: 01-VERIFICATION.md; upstream refresh reports]

## Classified Findings

| Classification | Finding | Planning meaning |
|---|---|---|
| Repository identity fact | Public `napplet/web`, `kehto/web`, and `napplet/naps` identities/default branches were retrieved from GitHub. | Authorize bounded identity/authenticity review; do not equate public GitHub identity with protocol authority. |
| Merged implementation observation | `napplet/web` #184/#186/#188 and `kehto/web` #204/#209/#211 changed CLI/URI/intent/manifest/loader/package/test/doc surfaces. | Preserve as observed-source candidates, parallel to blocked normative records. |
| PR intent/proposal | PR narratives assert protocol drafts, conventions, and reasons for implementation decisions. | Retain as directional evidence only; directly acquire normative NIP/NAP sources before any protocol claim. |
| Protocol authority | No independently reviewed immutable NIP-5A, NIP-5D, NAP registry/projection/governance source was ingested. | No protocol claim, first-lab selection, or architecture decision advances. |
| Project policy | Current policy still requires immutable records, separated truth classes, review, and no automatic rewrite. | All refresh actions are review-gated and additive. |
| Inference | Changed implementation surfaces identify likely affected research areas. | Create targeted review work, not accepted conclusions. |

## Immutable Candidate Evidence Register

| Recommended new candidate ID | Purpose / classification | Immutable revision, path, and digest/blob | Affects / refresh trigger |
|---|---|---|---|
| `CAND-SRC-NAPPLET-WEB-PR184-20260728` | Observed CLI identity/manifest implementation, not protocol authority. | `4916777862ababd09fa13cf155f4b4079c8e8cb1`; `packages/cli/src/manifest.ts` blob `c9c0ceff963da1e2c5c71f97ddc69afff08d3c57`; test blob `d459150eb898f1c18ebe4b967f18b3d55d1685cd`. | EVID-02/EVID-03, `DRF-IDENTITY-001`; refresh on NIP-5A/NIP-5D or web release/HEAD change. |
| `CAND-SRC-NAPPLET-WEB-PR186-20260728` | Observed queryless URI, intent, manifest, sender/delivery, reference-shell implementation. | `dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b`; `packages/nap/src/convention-uri.ts` blob `1a8db0c46d517edf2374b5e5022b429d8b18191b`; `packages/nap/src/intent/shim.ts` `8fd94fa71a16865f90fb8438a09867ff81954c54`; `packages/core/src/types/intent.ts` `930e8c246d3…`; reference shell `05a3145501642fc3772da749b2f76e3f91056559`. | EVID-02/EVID-03; identity/metadata/manifest/intent/security review; refresh on linked NAP status, web HEAD/release, or before Phase 2. |
| `CAND-SRC-NAPPLET-WEB-PR188-20260728` | Committed release/version metadata candidate, not registry artifact proof. | `60889f1c2476e063500c7ab6624af6abe0dbcbe5`; `packages/nap/package.json` blob `d125a4a5ae6d1a8b7409b94be0cb51a6899c2a62`; `packages/core/package.json` `b50f3760749b80e09d517402e3edb96d0e335868`; tree `d1bd6d78bb357506e6f4244537fecd54262f9a55`. | EVID-03/EVID-04, `CLM-CMP-PACKAGE-001`, SPK-G, ADR-0010; refresh on registry/release/integrity/export change. |
| `CAND-SRC-KEHTO-WEB-PR204-20260728` | Observed runtime/host/security/reference implementation, not NAP/NIP authority. | `b85db51db838866de753b275b9d34ec908785bd2`; diff SHA-256 `87688bba7f4f62b98f7a3dd83c7fe4e250e13fc049c95a0b4a9f9ee5ec44fb8d`; `RUNTIME-SPEC.md` blob `d90cab7dcad177c6eacb6f0780b434b5ecffccab`; frame loader `49976f4c8868f6f31e16a9ffeb33080646cdb3b4`. | EVID-03; loader/identity/handshake/intent/manifest/egress/unknown-message/conformance review; refresh on listed source-path or default-HEAD change. |
| `CAND-SRC-KEHTO-WEB-PR209-20260728` | Release/version/package-manifest history candidate. | `4eafa058d18cf245b23d49b23bc29dda0b7d7651`; diff SHA-256 `4b0d22e05ed2718784396052b56b35c0eb2d19bc171b75e6d6643069ff1c1f57`; e.g. runtime manifest blob `fc6447a2cd05edccd4bd324b29340abcfee2e935`. | EVID-03/EVID-04, package/release review; refresh on registry integrity/current manifest change. |
| `CAND-SRC-KEHTO-WEB-PR211-20260728` | Observed loader-audit ownership/CI regression evidence. | `54ef2ead03ee0c37727468b8658b6dc224137`; diff SHA-256 `0c5d272b9ed2c77f1d95f31cc98235bdaba594cc82e3ca205f1205f70443420f`; gateway audit blob `afc424858b74b8917a0529e8065bc6afaaa2e3cc`. | EVID-03; verified-loader identity/manifest/verifier review; refresh when loader/audit paths change. |
| `CAND-SRC-NAPS-WINDOW-20260728` | Bounded zero-merge repository-history observation only. | `napplet/naps` `master` checkpoint `5ac0490461ca6fec2f0d2e45b4835cf9bc08de24`; API snapshot SHA-256 `8ac19d279a8ccd9bc86c3ed952b79ba2c36a46937034268965d702a4c49965df`. | EVID-01–EVID-04/OPER-01/OPER-03; refresh at next rolling-window review. |

**ID note:** These are recommended IDs only. Create them only through the canonical schema/validator after identity/authenticity and content-byte review; retain existing `SRC-POLICY-*` unchanged. The abbreviated `930e8c246d3…` denotes the full blob listed in the source report and must be copied losslessly during ingestion. [VERIFIED: source-registry.yaml; upstream refresh reports]

## Change Classification by PR

| Change class | Merged PRs | Candidate effect |
|---|---|---|
| Package exports/versioning | `napplet/web` #188; `kehto/web` #204/#209; #184 has CLI patch changeset. | Separate source commit version evidence from registry/tarball/integrity/export evidence; no install. |
| Runtime/security boundary | `napplet/web` #186; `kehto/web` #204/#211. | Review sender attestation, loader ownership, handshake, sandbox/active-surface assertions as observed implementation only. |
| Protocol/spec semantics | `napplet/web` #184/#186; `kehto/web` #204. | Acquire authoritative NIP/NAP revisions first; do not teach queryless URI, d-tag, manifest, intent, delivery, or NAP-INC semantics as protocol law. |
| Examples/tests/docs | `napplet/web` #184/#186/#188; `kehto/web` #204/#208/#210/#211. | Tests and docs corroborate repository intent/behavior at the revision but do not establish cross-runtime conformance. |
| Compatibility assumptions | #186/#188 and #204/#209 notably affect identity, metadata, manifests, intent, package/release, fixture, and loader assumptions. | Add only parallel observed evidence after review; leave matrix blocked. |

## Implementation-Ready Refresh Map

| Existing artifact / IDs | Recommended action after human review | Status now |
|---|---|---|
| `candidate-source-manifest.yaml`: `CAND-NAPPLET-WEB-REPOSITORY`, `CAND-NAPPLET-WEB-PACKAGE`, `CAND-RUNTIME-IMPLEMENTATION`, `CAND-NAP-*` | Add separate candidate records/pointers for `napplet/web`, `kehto/web`, and `napplet/naps`; authenticate official authority by purpose and capture exact source bytes/digests. Do not replace old discovery history. | No mutation; blocked. |
| `source-registry.yaml` / `acquisition-log.yaml` | Ingest only reviewed `SRC-*` records for selected exact `commit:path` blobs; record the retrieval and authority/evidence/maturity fields. | No mutation; only policy records exist. |
| `claims.yaml`: `CLM-UPSTREAM-BASELINE-001`, `CLM-CMP-PACKAGE-001`, `CLM-CMP-RUNTIME-001`, `CLM-CMP-EXAMPLE-001`, `CLM-CMP-FIXTURE-001` | Preserve blocked states. Add candidate observed-source relations after review; revise the absolute “no public release/export baseline” wording only if registry/root-export evidence is independently pinned. | No claim is resolved. |
| `drift-register.yaml`: `DRF-IDENTITY-001`, `DRF-MANIFEST-001`, `DRF-METADATA-001`, `DRF-INTENT-001`, `DRF-HANDSHAKE-001`, `DRF-EGRESS-001`, `DRF-UNKNOWN-MESSAGES-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001` | Append parallel observed implementation sides/history with exact candidate locators; retain blocked normative sides and material uncertainty. | No drift is resolved. |
| `open-questions.yaml`: `OQ-UPSTREAM-BASELINE-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`, `OQ-VERIFIED-LOADER-{IDENTITY,MANIFEST,VERIFIER}-001`, `OQ-EGRESS-NIP-001` | Update resolution criteria/source references with missing protocol, registry, execution, and approval steps; keep open. | No question closes. |
| `compatibility-matrix.yaml`: `CMP-BASELINE-001` | Add an explicitly `observed-source/release-commit` candidate row only after canonical source review. Keep baseline `blocked` until qualified protocol/package/runtime/example/fixture inputs exist. | EVID-03 remains blocked. |
| `open-work-snapshot.json`: `OW-NAP-001`, `OW-NAPPLET-WEB-001`, `OW-RUNTIME-001` | Preserve historical `immutableReference: null`; create a new dated snapshot/review record rather than overwriting it. | Existing snapshot remains valid history. |
| `ecosystem-inventory.yaml`: `ECO-NAPPLET-WEB-{PACKAGE,REPOSITORY}`, `ECO-RUNTIME` | Refresh candidates with the now-known repository identities; distinguish repository source from published package. | Still blocked/deferred. |
| `package-map.md`, `LES-010`, `ADR-0010`, `SPK-G` report | Add only an observed-commit-versus-published-package distinction, with explicit non-admission. Do not add import instructions, version recommendation, root-export assertion, or conformance claim. | Remain blocked/proposed/materially uncertain. |

## Required Human Review Points

1. **Identity/authenticity:** Is `napplet/web`, `kehto/web`, or `napplet/naps` official for the particular repository/protocol/package purpose claimed?
2. **Protocol technical:** Directly pin NIP-5A/NIP-5D and NAP registry/projection/governance sources; adjudicate conflicts with observed implementation without overwriting either side.
3. **Security:** Review sender-derivation/attestation, iframe loader/sandbox, handshake, egress, and active-surface claims as implementation evidence; no host capability follows automatically.
4. **Release/supply chain:** Pin registry artifacts, integrity, provenance, license, documented root exports, and release-versus-source divergence before package admission or SPK-G retry.
5. **Content learning:** Confirm every lesson continues to distinguish observation/proposal from protocol fact and preserves static deterministic fallbacks.
6. **Phase gate:** Repair and re-verify known fail-open provenance/replay/consolidation/toolchain defects before treating any candidate ingestion as EVID-03/EVID-04 closure. [VERIFIED: 01-VERIFICATION.md; 01-REVIEW.md]

## Remaining Blocking Gaps and Triggers

- **Normative protocol source gap:** official immutable NIP/NAP source paths, content digests, authority/maturity, and human review remain missing. Trigger: authoritative governance/specification revision, or source acquisition approval.
- **Package artifact gap:** registry availability, integrity, provenance, license, documented root export, and release/current source comparison remain missing. Trigger: new registry/release/integrity/export record or a concrete Phase 2 package decision.
- **Runtime/conformance gap:** no independently executed trusted-host/runtime/cross-runtime conformance measurement follows from merged source/tests. Trigger: source review plus reproducible isolated measurement.
- **EVID-04 integrity gap:** validators currently fail open in citation traversal, replay execution, retained-evidence checking, publication atomicity, and dependency integrity. Trigger: focused Phase 1 gap closure and fresh verification.
- **`napplet/naps` window:** zero merged PRs proves only the bounded merge-history result, not protocol stability or authority. Trigger: next rolling window, direct commits/releases, or scoped normative-source review.

## Sources

- `upstream-refresh-kehto-web-2026-07-28.md` — five fully enumerated merged PRs, immutable merge/tree/blob/diff metadata. [VERIFIED: local research report]
- `upstream-refresh-napplet-web-2026-07-28.md` — three fully enumerated merged PRs and repository identity/release observations. [VERIFIED: local research report]
- `upstream-refresh-napplet-naps-2026-07-28.md` — fully enumerated zero-merge window and repository checkpoint. [VERIFIED: local research report]
- `01-VERIFICATION.md`, `01-REVIEW.md` — unresolved Phase 1 evidence-integrity and closeout gaps. [VERIFIED: local phase reports]
