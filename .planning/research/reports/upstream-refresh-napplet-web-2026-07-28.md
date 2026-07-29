# Upstream Refresh — `napplet/web` (rolling window ending 2026-07-28)

## Scope and outcome

**Authorized activity:** public, read-only GitHub API research for Learn Napplets Phase 1.  
**Window (inclusive, UTC):** `2026-07-25T09:29:46Z` through `2026-07-28T09:29:46Z`.  
**Retrieved:** `2026-07-28T09:36:09Z`.  
**Result:** **3 merged pull requests**. The enumeration query was `repo:napplet/web is:pr is:merged merged:2026-07-25T09:29:46Z..2026-07-28T09:29:46Z`, paginated with `per_page=100`; GitHub Search reported `total_count: 3`, so the result was not silently capped.

## Repository identity and retrieval baseline

| Field | Value |
|---|---|
| Repository | [`napplet/web`](https://github.com/napplet/web) |
| GitHub repository id / visibility | `1197078677` / `public` |
| Default branch | `main` |
| Default-branch HEAD at retrieval | [`60889f1c2476e063500c7ab6624af6abe0dbcbe5`](https://github.com/napplet/web/commit/60889f1c2476e063500c7ab6624af6abe0dbcbe5) |
| Repository state | public; `archived: false`; created `2026-03-31T10:01:23Z`; API `pushed_at` `2026-07-27T17:49:49Z` |

### Evidence method and authority boundary

Each PR, merge commit, and changed-file record below was fetched from GitHub REST. Immutable implementation locators are `https://github.com/napplet/web/blob/<merge-commit>/<path>` (or the Git blob SHA in the file inventory). Git blob SHA is the immutable content identifier recorded in preference to a separate raw-content SHA-256 snapshot; consequently, **no mutable raw snapshot is treated as evidence**. Retrieval time for all records is `2026-07-28T09:36:09Z`.

* **Authority:** `napplet/web` is an official-looking public implementation/release repository once its GitHub identity is verified, but this refresh did not establish it as protocol-specification authority.
* **Evidence class:** GitHub PR/commit/diff/file metadata and merged implementation behavior; PR prose is author proposal/rationale, not independently normative evidence.
* **Maturity:** merged code is mature only as an observed current implementation/release baseline. It does **not** automatically settle NIP/NAP rules, security guarantees, interoperability, or a Learn Napplets policy decision.
* **Refresh trigger:** default-branch movement, a new release/package registry record, upstream NIP/NAP governance change, or before Phase 2/product-contract acceptance. Re-fetch immutable revisions rather than relying on this report's mutable GitHub UI links.

## Enumeration and relevance summary

| PR | Merged UTC | Primary change | Protocol | Runtime/API/security boundary | Packages/releases | Docs/examples/tests |
|---|---:|---|---|---|---|---|
| [#184](https://github.com/napplet/web/pull/184) | 2026-07-26T10:15:32Z | removes CLI's 13-character `d`-tag ceiling | **Potential identity/manifest relevance; not normative** | CLI validation only; no runtime boundary change observed | `@napplet/cli` patch changeset, then released in #188 | CLI docs + regression test |
| [#186](https://github.com/napplet/web/pull/186) | 2026-07-26T10:34:42Z | adopts queryless convention and intent contracts | **High observed implementation relevance; draft/proposal provenance must remain separate** | public types, shims, reference shell, manifest tool, sender attestation, delivery semantics changed | minor changesets for seven packages; patch changesets for three | extensive docs, fixtures, conformance and unit tests |
| [#188](https://github.com/napplet/web/pull/188) | 2026-07-26T11:11:52Z | Versions Packages release PR | no independent protocol logic | publishes version metadata/changelogs only | releases the #184/#186 changeset set | changelogs only |

## Per-PR evidence and interpretation

### PR #184 — [`fix(cli): remove invented 13-char cap on napplet d tags`](https://github.com/napplet/web/pull/184)

| Field | Record |
|---|---|
| Author / lifecycle | `hzrd149`; created `2026-07-23T13:48:12Z`; merged `2026-07-26T10:15:32Z` |
| Base / head | `main` @ `b335c40c77f55547f23af81d6d999e2e4e3a3623`; `fix/cli-d-tag-length-limit` @ `ce0925be60c90042a4428cf7eab9e616046bcaea` |
| Merge commit / tree | [`4916777862ababd09fa13cf155f4b4079c8e8cb1`](https://github.com/napplet/web/commit/4916777862ababd09fa13cf155f4b4079c8e8cb1) / `11d4c67a47fd399f801bf0339885dc3dda9780aa` |
| Scope | 9 files; +127 / -6; 2 commits; labels: none; issue comments: 0; review comments: 0 |
| PR proposal/rationale | The author says the old `(1, 13)` limit was CLI-invented and says NIP-5D/NIP-5A do not constrain length. This is **PR proposal/rationale**, not a verified normative conclusion in this report. |
| Merged implementation behavior | `NAMED_SITE_D_TAG_PATTERN` changed from `^[a-z0-9-]{1,13}$` to `^[a-z0-9-]+$`; trailing `-` remains rejected. The CLI docs/error strings were aligned, and a test accepts `my-very-long-napplet-name`. |
| Relevance | identity/manifest/CLI behavior; no guest-host security boundary, runtime mechanism, or package export API change found. A CLI validation relaxation should not be taught as a protocol rule until NIP-5A/NIP-5D authority is pinned and reviewed. |

### PR #186 — [`feat: adopt queryless convention and intent contracts`](https://github.com/napplet/web/pull/186)

| Field | Record |
|---|---|
| Author / lifecycle | `dskvr`; created `2026-07-23T17:50:33Z`; merged `2026-07-26T10:34:42Z` |
| Base / head | `main` @ `4916777862ababd09fa13cf155f4b4079c8e8cb1`; `feat/ad-hoc-nap-schemes` @ `c34556572d906d5a55e2f40f98e056b79903cc15` |
| Merge commit / tree | [`dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b`](https://github.com/napplet/web/commit/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b) / `33edc8387973f31687dfb20181a40fe936286824` |
| Scope | 171 files; +12,034 / -1,248; 130 commits; labels: none; issue comments: 0; review comments: 0 |
| Linked proposal/discussion check | No linked `napplet/web` issue, discussion, timeline cross-reference, or comments were returned. PR prose cites `napplet/naps` PRs [#89](https://github.com/napplet/naps/pull/89), [#90](https://github.com/napplet/naps/pull/90), and [#91](https://github.com/napplet/naps/pull/91). At retrieval #89 and #90 were closed/merged on 2026-07-24; #91 remained open. The PR description's “draft and unmerged” wording is therefore stale at retrieval and cannot be used as current authority. |
| PR proposal | The author proposes exact queryless `napplet:<archetype>/<intent>` identities; query-to-shallow-text-payload transposition; runtime-attested sender; URI-authoritative invocation; immediate acceptance separate from eventual handling; source-independent no-ID target delivery; optional same-tag `kind:<number>` metadata; retirement of undocumented `napplet-*` HTML metadata. These are **proposed/adopted implementation contracts**, not automatically normative protocol facts. |
| Merged implementation behavior inspected | `packages/nap/src/convention-uri.ts` parses queryless identity and rejects fragments, malformed parameters, duplicate decoded names, and simultaneous query/explicit payload. `packages/nap/src/intent/shim.ts` refuses caller-supplied sender, normalizes URI input, uses `intent.deliver`, and exposes `onDelivery`. `packages/core/src/types/intent.ts` documents runtime-attested sender and opaque untrusted payload. The reference shell derives sender from endpoint `dTag` and emits delivery after acceptance. Vite manifest tooling validates queryless convention tags and optional same-tag nonnegative `kind:` metadata. These observations are pinned to the merge commit/tree and file blobs in the inventory. |
| Relevance | **Protocol/API:** high observed change to public conventions, intent types, manifest metadata and package exports. **Runtime/security:** changes a claimed security boundary (caller cannot set sender) and delivery lifecycle model, but does not prove a trusted host implementation outside this repository. **Compatibility:** high; published minor releases follow in #188. **Docs/examples/tests:** high, including docs, skills, fixtures, conformance, tests. |

### PR #188 — [`Version Packages`](https://github.com/napplet/web/pull/188)

| Field | Record |
|---|---|
| Author / lifecycle | `github-actions[bot]`; created `2026-07-26T10:16:28Z`; merged `2026-07-26T11:11:52Z` |
| Base / head | `main` @ `dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b`; `changeset-release/main` @ `3d36ed46e5cd862d81b3cc68d1df81a9ab62609a` |
| Merge commit / tree | [`60889f1c2476e063500c7ab6624af6abe0dbcbe5`](https://github.com/napplet/web/commit/60889f1c2476e063500c7ab6624af6abe0dbcbe5) / `d1bd6d78bb357506e6f4244537fecd54262f9a55` |
| Scope | 33 files; +172 / -63; 1 commit; labels: none; issue comments: 0; review comments: 0 |
| Merged implementation behavior | consumes the changesets from #184 and #186, removes the changeset files, and updates package/JSR metadata and changelogs. No source-runtime or protocol behavior changed independently in this PR. |
| Version records in committed package manifests | `@napplet/cli@0.3.0`, `@napplet/conformance@0.14.0`, `@napplet/core@0.29.0`, `@napplet/nap@0.29.0`, `@napplet/sdk@0.25.0`, `@napplet/shim@0.27.0`, `@napplet/vite-plugin@0.12.0`, `@napplet/boilerplate@0.3.1`, `@napplet/conformance-cli@0.2.16`, `@napplet/skills@0.2.11`, `@napplet/conformance-web@0.0.15`. |
| Uncertainty | A committed version is strong implementation/release metadata, but this refresh did not retrieve npm/JSR registry provenance, tarball integrity, package availability, license, root exports, or run any package/runtime. It therefore does not close package-admission or runtime questions. |

## Fact / proposal / observed behavior / inference separation

| Classification | Statement | Boundaries |
|---|---|---|
| Upstream fact | The verified public repository has default branch `main`; the three listed PRs merged in the stated window at the recorded immutable merge commits. | GitHub repository/PR/commit API fact. |
| PR proposal | #184's statement that no protocol length limit exists, and #186's contract narrative/release notes. | Must be checked against revision-pinned NIP/NAP sources; does not override them. |
| Merged implementation behavior | CLI accepts arbitrary non-empty lowercase/digit/hyphen `d` tags except trailing hyphen; #186 code implements queryless URI normalization, sender derivation/guarding, target delivery, and optional kind metadata. | Observed only at the listed source revisions. Not independently executed here. |
| Inference | Learn Napplets needs a focused refresh of identity, manifest, metadata, intent, package, fixture/conformance, and lesson material. | Requires protocol-technical/content/security review; does not unblock Phase 1 by itself. |

## Comparison with active Learn Napplets Phase 1 artifacts — refresh queue

No active artifact was modified. The following are **refresh candidates**, not assertions that their existing blocked status is wrong.

| Active artifact and exact ID/row | Why it needs review after this upstream window | Required disposition |
|---|---|---|
| `candidate-source-manifest.yaml`: `CAND-NAPPLET-WEB-REPOSITORY` (currently points to `https://github.com/nap-ecosystem`) | The verified public repository identity is `https://github.com/napplet/web`; current pointer differs. | Add/review an immutable implementation candidate with the three commits/trees; do not relabel it protocol authority. |
| `candidate-source-manifest.yaml`: `CAND-NAPPLET-WEB-PACKAGE` | #188 supplies committed versions but not registry integrity/provenance. | Keep blocked; add release-commit evidence as distinct from registry/tarball evidence. |
| `claims.yaml`: `CLM-CMP-PACKAGE-001` | Its absolute statement that no immutable public release/export baseline is available now has a partial counterexample: public committed version/export-source evidence exists. | Refresh wording/state only after registry/package review; retain blocker for install/admission because integrity, registry and public root export evidence are still absent. |
| `drift-register.yaml`: `DRF-IDENTITY-001`, `DRF-MANIFEST-001`, `DRF-METADATA-001`, `DRF-INTENT-001` | #184 touches `d`-tag validation; #186 supplies pinned observed implementation of identity, manifest tags, metadata, intent delivery and sender provenance. | Add parallel observed implementation evidence at `4916777`/`dd7b3a7`; retain normative side blocked until NIP/NAP source authority and review are recorded. |
| `compatibility-matrix.yaml`: `CMP-BASELINE-001` | Current work and release are no longer only policy placeholders: #186/#188 provide a source revision and package-manifest baseline. | Add a separate “source/release-commit observed” row, not a completed release/package/runtime compatibility result. |
| `open-questions.yaml`: `OQ-UPSTREAM-BASELINE-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-VERIFIER-001` | These questions explicitly require immutable current/released source, identity/manifest/resolver, package and verifier evidence. | Refresh their source refs and resolution subcriteria; do not close without official protocol, registry, and human review evidence. |
| `lesson-packets/03-nostr-underneath.md` (`LES-003`), `07-identity-and-distribution.md` (`LES-007`), `09-designing-a-good-napplet.md` (`LES-009`), `10-anatomy-of-a-napplet.md` (`LES-010`), `11-build-test-and-publish.md` (`LES-011`), `12-inside-a-runtime.md` (`LES-012`), `13-evolving-the-protocol.md` (`LES-013`) | They intentionally teach blocked identity/manifest/package/runtime/proposal distinctions. #184/#186/#188 provide material for an observed-vs-normative update, especially queryless contracts, `dTag`, package versions, runtime-attested sender, and future protocol evolution. | Keep essential facts sourced from structured evidence and retain explicit uncertainty; no lesson may present #186 as settled protocol law. |
| `adr-handoff.yaml`: `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0008`, `ADR-0010`, `ADR-0011` | Their evidence dependencies traverse discovery/metadata/intent/identity/manifest/package freshness questions. | Add this report as review input; no automatic ADR acceptance. `ADR-0011` should schedule another revision check on upstream release/governance change. |
| `reports/spike-consolidation.md` and `reports/phase-gate.md`: `SPK-C-IMPACT-001`, `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, `SPK-H-IMPACT-001` | #186 adds source-level conformance/reference-shell/fixture evidence; #188 adds version metadata. No browser, registry, package install, or external trusted-runtime measurement occurred. | Re-scope only source-inspection portions if desired. Keep material uncertainty and do not claim the spikes passed or replace their observed measurement limits. |

### Drift and open questions created by the refresh

1. **Repository identity drift:** `CAND-NAPPLET-WEB-REPOSITORY` identifies a different host path (`nap-ecosystem`) than the verified public repo (`napplet/web`). Confirm whether this is an archival/pointer convention or a stale candidate before editing canonical research.
2. **Protocol-versus-implementation drift:** #186 adopts a contract whose cited upstream status is mixed at retrieval (#89/#90 merged, #91 open). The implementation may be ahead of, selectively project, or differ from final normative sources.
3. **Release-versus-registry gap:** #188 documents committed package versions, not registry integrity/availability/export semantics. A repository release PR cannot substitute for an npm/JSR immutable tarball or package audit.
4. **Security-boundary gap:** source code's sender guard and endpoint-derived sender are observed implementation behavior. They are not evidence that every host prevents spoofing or that a Learn Napplets host should grant a capability.
5. **Compatibility gap:** repository tests and conformance/reference-shell changes establish only repository-maintained test intent and unexecuted source changes in this review; they do not establish cross-runtime compatibility.

## Required review path before a canonical refresh

1. Pin and review authoritative NIP-5A/NIP-5D and NAP/NAP-INTENT revisions, including the exact governance/status of cited `napplet/naps` #89–#91.
2. Record `napplet/web` as observed implementation evidence with the three merge commits, trees, and below blob inventory; retain authority class and uncertainty.
3. Independently retrieve registry/package integrity, provenance, license and public exports before changing package admission or SPK-G conclusions.
4. Have protocol-technical, content-learning, and security reviewers assess affected drift/ADR rows. Record any conflict instead of silently replacing current project policy.
5. Refresh when the default-branch HEAD changes from `60889f1c2476e063500c7ab6624af6abe0dbcbe5`, packages are published/retagged, or the linked NAP work changes status; immediately before Phase 2 contract approval.

## Complete changed-file inventory

Rows are complete GitHub `/pulls/{n}/files` API results. `blob SHA` is the exact Git blob object returned for the changed file at the PR result. For removed files it identifies the deleted preimage; use the merge commit plus path locator for the immutable post-merge tree state. Status/additions/deletions are GitHub diff metadata.

### PR #184 inventory (9 files)

| Path | Status | + | - | Blob SHA | Immutable locator |
|---|---:|---:|---:|---|---|
| `.changeset/cli-d-tag-length-limit.md` | added | 10 | 0 | `95a35ffc6e4ed3ca9622a8aea3d90dbfb6fd4d73` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/.changeset/cli-d-tag-length-limit.md) |
| `.planning/STATE.md` | modified | 1 | 0 | `b432395514324c1e0ce047a67c20011ae4df3a9a` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/.planning/STATE.md) |
| `.planning/quick/260723-kgz-remove-cli-d-tag-length-limit/PLAN.md` | added | 51 | 0 | `3715b2abd13502784ac7df15a9e1d825c3f2b799` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/.planning/quick/260723-kgz-remove-cli-d-tag-length-limit/PLAN.md) |
| `.planning/quick/260723-kgz-remove-cli-d-tag-length-limit/SUMMARY.md` | added | 45 | 0 | `d96e77a789bcbe960437e7eac6216f1f7de5138c` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/.planning/quick/260723-kgz-remove-cli-d-tag-length-limit/SUMMARY.md) |
| `packages/cli/README.md` | modified | 2 | 2 | `65e60a6728894248c99babb5080db867761f80dc` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/packages/cli/README.md) |
| `packages/cli/src/deploy-plan.ts` | modified | 1 | 1 | `ce8362e99101269d476b5b71ad903ba7721564e4` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/packages/cli/src/deploy-plan.ts) |
| `packages/cli/src/init-wizard.ts` | modified | 1 | 1 | `c9c6be58810f4c9aa3d5ecd9617444696bff395d` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/packages/cli/src/init-wizard.ts) |
| `packages/cli/src/manifest.ts` | modified | 2 | 2 | `c9c0ceff963da1e2c5c71f97ddc69afff08d3c57` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/packages/cli/src/manifest.ts) |
| `packages/cli/tests/manifest_test.ts` | modified | 14 | 0 | `d459150eb898f1c18ebe4b967f18b3d55d1685cd` | [commit:path](https://github.com/napplet/web/blob/4916777862ababd09fa13cf155f4b4079c8e8cb1/packages/cli/tests/manifest_test.ts) |

### PR #186 inventory (171 files)

| Path | Status | + | - | Blob SHA | Immutable locator |
|---|---:|---:|---:|---|---|
| `.changeset/ad-hoc-convention-contracts.md` | added | 16 | 0 | `655c96e1f5d268b60466d8fbbf0b8b654efef33d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.changeset/ad-hoc-convention-contracts.md) |
| `.changeset/ad-hoc-convention-guidance.md` | added | 10 | 0 | `0d5ef1c64b3b19855a9734284468b0a7a15ab948` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.changeset/ad-hoc-convention-guidance.md) |
| `.planning/REQUIREMENTS.md` | modified | 74 | 2 | `08620980b6d1e266dde4885c169a61df5ce79fe5` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/REQUIREMENTS.md) |
| `.planning/ROADMAP.md` | modified | 121 | 5 | `3ba2d468ee9282464ea1d39df0019541502836b1` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/ROADMAP.md) |
| `.planning/STATE.md` | modified | 75 | 15 | `334dff5087da8ba15a5a5bdc53c932c0567a4e6f` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/STATE.md) |
| `.planning/WINDOWS.md` | added | 100 | 0 | `d85aad89d7dbac396109a8dd04243543d167ef01` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/WINDOWS.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/.gitkeep` | added | 1 | 0 | `8b137891791fe96927ad78e64b0aad7bded08bdc` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/.gitkeep) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-01-PLAN.md` | added | 166 | 0 | `f3ec195eeb0ceb10e6f97809743dec6a7111be10` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-01-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-01-SUMMARY.md` | added | 128 | 0 | `b22691bc7e3d2f868166f0e7acc6d9161ba1a208` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-01-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-02-PLAN.md` | added | 149 | 0 | `cdf51f7418fa41f9618d4560de76e88528cbdfd0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-02-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-02-SUMMARY.md` | added | 92 | 0 | `7d8b8a42daa986cd579ef30dc97f0270ed498796` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-02-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-03-PLAN.md` | added | 125 | 0 | `acde234d00db1511b47db8b3de4473a67dda8a62` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-03-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-03-SUMMARY.md` | added | 76 | 0 | `c98e7e2529de5549d08265f9600afcae5d0d75d7` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-03-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-04-PLAN.md` | added | 172 | 0 | `5066306f86676db6c131afc470efc3139e6d64e5` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-04-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-04-SUMMARY.md` | added | 139 | 0 | `a1463ef9a3ebe6ea20209619ee498f39329f5317` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-04-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-05-PLAN.md` | added | 162 | 0 | `90f9c7313cd6cb278ad80d1735c9d69d40e63126` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-05-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-05-SUMMARY.md` | added | 129 | 0 | `465218db8948190411c00563e1396b8c56551d1a` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-05-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-06-PLAN.md` | added | 134 | 0 | `2e6ce5e345c26784f7f02aef61db6c57ccd43b69` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-06-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-06-SUMMARY.md` | added | 106 | 0 | `3eeae4fe2d52618c01fc3b66ea2614acadbd3429` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-06-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-07-PLAN.md` | added | 156 | 0 | `5eb80b86f0f02b76534a8baae684349a0c09be74` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-07-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-07-SUMMARY.md` | added | 136 | 0 | `f43b3111233901d59c284918f333895739f6ebb1` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-07-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-08-PLAN.md` | added | 133 | 0 | `14e02ac3a3c484e68dfec54f32d56495530adfa5` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-08-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-08-SUMMARY.md` | added | 132 | 0 | `b05bdc7c161362fb8e2f7dd07ef20cb538d889c5` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-08-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-09-PLAN.md` | added | 132 | 0 | `edc7c776d5c56606a1c9daef3797c9425d738719` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-09-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-09-SUMMARY.md` | added | 138 | 0 | `cf7bfc7943e3619aa2127c5d68f883c53ffad6f6` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-09-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-10-PLAN.md` | added | 193 | 0 | `d7114622fa9b9d4e7317d4af676dbc2f7729081a` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-10-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-10-SUMMARY.md` | added | 151 | 0 | `e4fc7af1c9c51222a1892d8d726c63a90bcf15e8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-10-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-11-PLAN.md` | added | 154 | 0 | `ae1a40ded9ac4fe12e1aa66154fb176c7d943e67` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-11-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-11-SUMMARY.md` | added | 142 | 0 | `c0811372ce961b54a58151bba1c1b32ab73e44a1` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-11-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-12-PLAN.md` | added | 137 | 0 | `e9dc5b60169746edc6eac6e488cda0b3016d52c6` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-12-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-12-SUMMARY.md` | added | 130 | 0 | `5ee1f61291c9ddc8c2417f63039e1e560898e62c` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-12-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-13-PLAN.md` | added | 169 | 0 | `7ce3ad0d3e2cdd72b14cc7d9103682e59bb98504` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-13-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-13-SUMMARY.md` | added | 150 | 0 | `bd78f04a6a31b324c66fcb29724b71db85d6a758` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-13-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-14-PLAN.md` | added | 181 | 0 | `de32550ec91f62bd65076a6342a560d549a9a3b1` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-14-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-14-SUMMARY.md` | added | 159 | 0 | `4e0b4ddd1be2ce4ef71b5ac518b8cf06868395e6` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-14-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-15-PLAN.md` | added | 91 | 0 | `fca4e2911b85eb7af5b62b473d8d7b3956fad1c3` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-15-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-15-SUMMARY.md` | added | 130 | 0 | `4cbc29d2221a20c818705e6cd96d639b22143067` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-15-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-16-PLAN.md` | added | 103 | 0 | `121e121ce99b244076fb4716ee6bc356a10607e8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-16-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-16-SUMMARY.md` | added | 123 | 0 | `d31dbc0bfaac097405b2c16f33df960f59b9a214` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-16-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-17-PLAN.md` | added | 107 | 0 | `68f5403aa6d78c0f674853e7e6a14d0757f09374` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-17-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-17-SUMMARY.md` | added | 133 | 0 | `46fac48e300d030fe7059698d565ca574ae60ebf` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-17-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-18-PLAN.md` | added | 85 | 0 | `260cbea24010b19707445e85bb793be30823f82d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-18-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-18-SUMMARY.md` | added | 48 | 0 | `7dfd2cdd2782ffd9545537e62c7461b9a75d65c7` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-18-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-19-PLAN.md` | added | 87 | 0 | `ffce614ae6ec371f530a8d8d8d561f503818db3d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-19-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-19-SUMMARY.md` | added | 117 | 0 | `70469998a91218974ae01fcda98363f677300532` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-19-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-20-PLAN.md` | added | 90 | 0 | `be0a818ce2576b8f144dd185c2cceee07e4c17b8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-20-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-20-SUMMARY.md` | added | 46 | 0 | `6d11eab3fe258c203fa5ddb38d228a00c290d044` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-20-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-21-PLAN.md` | added | 92 | 0 | `a3a59d6dff32c390319c0e6c6ce3bb9999ee4d29` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-21-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-21-SUMMARY.md` | added | 48 | 0 | `c93203dbf6444d8df43ca2efedf43a5d67fc6d77` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-21-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-22-PLAN.md` | added | 111 | 0 | `ce597830c64c94bc6cad84208f11c079a4236466` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-22-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-22-SUMMARY.md` | added | 81 | 0 | `06f1520ffc7235c3a34f4195faef102eed6ab204` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-22-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-23-PLAN.md` | added | 101 | 0 | `95df902c40e56817cc2a8ca38b780798c84c29cd` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-23-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-23-SUMMARY.md` | added | 116 | 0 | `e65047f3bed4bc6ed9d601417953b329a6dbada0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-23-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-24-PLAN.md` | added | 113 | 0 | `351fcd99479f474fe572d60be80596e6c31ff18c` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-24-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-24-SUMMARY.md` | added | 62 | 0 | `e37f968c8a06e8a675bf4469051e04ed135daa84` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-24-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-25-PLAN.md` | added | 92 | 0 | `740b039b4aec8052acecc3eda53e339d1fc2fa3e` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-25-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-25-SUMMARY.md` | added | 128 | 0 | `69dbc2b03f27bf9de69a405c7c1cf4f74ed4980b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-25-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-26-PLAN.md` | added | 90 | 0 | `8b60b5dae6649f519f24c438c803024885b128d8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-26-PLAN.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-26-SUMMARY.md` | added | 126 | 0 | `fb1f80e57124acce837ca587a47da1dabdcf60c9` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-26-SUMMARY.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-CONTEXT.md` | added | 140 | 0 | `6e4d4fc11c5feadc2dca27be86b92390f17bd2b0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-CONTEXT.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-PATTERNS.md` | added | 253 | 0 | `73a77eb423794e1776429713cf2281c7413d05ff` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-PATTERNS.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-PR89-91-DELTA.md` | added | 137 | 0 | `497efaae82d8d8f3e8349f4a187b1cc9a79b941d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-PR89-91-DELTA.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-RESEARCH.md` | added | 472 | 0 | `563cbe7498421e7e817e29e3b13e89c9713829c7` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-RESEARCH.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-REVIEW-2.md` | added | 138 | 0 | `4febd9cf83fb7b8b78084df6331e2eee66d26841` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-REVIEW-2.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-REVIEW-FIX.md` | added | 50 | 0 | `028c098b1fd645ec6b90ecdd3dd32249ad04f03a` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-REVIEW-FIX.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-REVIEW.md` | added | 148 | 0 | `a9e42322cb4b02e6a70499a9ef59edf0b51ac1d8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-REVIEW.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-VALIDATION.md` | added | 97 | 0 | `41c0bf146a67a73dc63de22e484f5c2e79e9c46d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-VALIDATION.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/161-VERIFICATION.md` | added | 137 | 0 | `e9c9680d4129d54f10195820589cd3ca69afd523` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/161-VERIFICATION.md) |
| `.planning/phases/161-ad-hoc-convention-package-contracts/deferred-items.md` | added | 25 | 0 | `2621b00f50af371582f094913feab214c1578bfb` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/phases/161-ad-hoc-convention-package-contracts/deferred-items.md) |
| `.planning/quick/260726-ft1-remove-hard-wrapped-prose-from-affected-/260726-ft1-PLAN.md` | added | 35 | 0 | `f7645445d15f9b29587c724e461dc994f95944bd` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/quick/260726-ft1-remove-hard-wrapped-prose-from-affected-/260726-ft1-PLAN.md) |
| `.planning/quick/260726-ft1-remove-hard-wrapped-prose-from-affected-/260726-ft1-SUMMARY.md` | added | 37 | 0 | `cddec51e40fb1de91e959013e70dd0de988c14cf` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/.planning/quick/260726-ft1-remove-hard-wrapped-prose-from-affected-/260726-ft1-SUMMARY.md) |
| `AGENTS.md` | modified | 1 | 0 | `040252d79b8abc31a5bb6370586014bc4e2836e8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/AGENTS.md) |
| `README.md` | modified | 28 | 20 | `d810ca4e59f51c45a3745531cc0a46466bd6a578` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/README.md) |
| `apps/docs/guide/build-note-drafts-napplet-from-boilerplate.md` | modified | 27 | 10 | `4344fb87f08cd0c634ba7ff28c98494184c8a8d6` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/guide/build-note-drafts-napplet-from-boilerplate.md) |
| `apps/docs/guide/build-note-drafts-napplet-with-ai-agent-and-skills.md` | modified | 31 | 11 | `dadf49826849e8b1928d5a1b32f33bcc635fb217` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/guide/build-note-drafts-napplet-with-ai-agent-and-skills.md) |
| `apps/docs/guide/build-note-drafts-napplet.md` | modified | 30 | 10 | `fc81f51914c0592941885fdf4c978bec72816777` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/guide/build-note-drafts-napplet.md) |
| `apps/docs/guide/concepts.md` | modified | 45 | 0 | `b7a8e7d261d11a951cd711c4b8d0c1cfd4a8aa88` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/guide/concepts.md) |
| `apps/docs/guide/getting-started.md` | modified | 30 | 6 | `4b689af707d9192588a00ece2757f31e4a61191e` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/guide/getting-started.md) |
| `apps/docs/guide/index.md` | modified | 18 | 0 | `ab7af6718b705dfa77d8c431aea21823bd98fa49` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/guide/index.md) |
| `apps/docs/guide/nip-5d.md` | modified | 36 | 0 | `dfaae73d55fcb9d5e3ec6ce781b9acfc797dee63` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/guide/nip-5d.md) |
| `apps/docs/naps/index.md` | modified | 51 | 10 | `4916935111755f56b981e1ed3d3933aeccd8790a` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/naps/index.md) |
| `apps/docs/packages/boilerplate.md` | modified | 28 | 0 | `6ba6ceb4427ec6ce2e63892012ebd32bb6a51847` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/packages/boilerplate.md) |
| `apps/docs/packages/cli.md` | modified | 47 | 2 | `8d213667424c0e0e392ba0bd632dae407941bc9d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/packages/cli.md) |
| `apps/docs/packages/core.md` | modified | 46 | 0 | `bf61194462a209b6df4d5544a9caa21474470894` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/packages/core.md) |
| `apps/docs/packages/nap.md` | modified | 71 | 0 | `5d107cf552a352266ca9a79edb8db0a11677fa31` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/packages/nap.md) |
| `apps/docs/packages/sdk.md` | modified | 72 | 3 | `7e43a2496d439df5682fea249052db7518100ef5` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/packages/sdk.md) |
| `apps/docs/packages/shim.md` | modified | 58 | 1 | `a4479b563be431fa88a68d8b0135a5842ff56c63` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/packages/shim.md) |
| `apps/docs/packages/vite-plugin.md` | modified | 6 | 16 | `4e1c1329ae6cca024e5d9a66484c5745f1f494f0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/docs/packages/vite-plugin.md) |
| `apps/web/src/lib/site.ts` | modified | 1 | 1 | `190cde68abbfe432b2b4fbe20cc889168bde2a7d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/apps/web/src/lib/site.ts) |
| `package.json` | modified | 1 | 0 | `d13e549713c16ca54a8ffad47ede7e021c25581a` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/package.json) |
| `packages/boilerplate/README.md` | modified | 13 | 16 | `520926843eead569163be94dd57ef5aa67b7ea62` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/boilerplate/README.md) |
| `packages/cli/README.md` | modified | 46 | 95 | `b0310e3d37cd65031afc66220551d0c6ecf82386` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/README.md) |
| `packages/cli/src/cli.ts` | modified | 3 | 3 | `455ccee47bd4eaa687e7380b7beb45110883145a` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/src/cli.ts) |
| `packages/cli/src/config.ts` | modified | 49 | 36 | `760550288fe03c94fb76b78999ddc91de9e86937` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/src/config.ts) |
| `packages/cli/src/init-wizard.ts` | modified | 7 | 7 | `f695aed3c0fec7ea3a3a4c72501a4dc7a28a3c1e` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/src/init-wizard.ts) |
| `packages/cli/src/manifest-metadata.ts` | modified | 18 | 11 | `a02ddfcbb4090370778219b515f77ac9d6ea9559` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/src/manifest-metadata.ts) |
| `packages/cli/src/mod.ts` | modified | 1 | 1 | `5328d51f33e5aea627674702800657d54d72a6d5` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/src/mod.ts) |
| `packages/cli/src/output.ts` | modified | 1 | 1 | `e30db68ebf74692079128dcad4d5ea6d014c160b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/src/output.ts) |
| `packages/cli/src/types.ts` | modified | 5 | 4 | `0365436cd59d7603eac246d869bb30ee3c4a732d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/src/types.ts) |
| `packages/cli/tests/config_test.ts` | modified | 80 | 13 | `fd259c20e9f5bdf74a271d03550f6c9541644e51` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/tests/config_test.ts) |
| `packages/cli/tests/init_wizard_test.ts` | modified | 4 | 4 | `78d36bf0c05b7ac663432b141d25dd384850fd84` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/tests/init_wizard_test.ts) |
| `packages/cli/tests/manifest_test.ts` | modified | 47 | 5 | `ce3c52a33830d3beecb3f90109bc3868acd4c81b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/cli/tests/manifest_test.ts) |
| `packages/conformance-cli/README.md` | modified | 9 | 20 | `b88759134b9687593a1068e95f4e9e4d1133bd80` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance-cli/README.md) |
| `packages/conformance-cli/src/cli.test.ts` | modified | 1 | 1 | `fc096c0f0d0602406c23c9a95267832698d135ed` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance-cli/src/cli.test.ts) |
| `packages/conformance-cli/src/ui-server.test.ts` | modified | 3 | 3 | `9189e763b44e63bb0dec484f35589aa6494b3518` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance-cli/src/ui-server.test.ts) |
| `packages/conformance/README.md` | modified | 12 | 24 | `0e881f052292c6157d93cb9b27e9ad47c2e55db1` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/README.md) |
| `packages/conformance/src/checks/catalog.test.ts` | modified | 16 | 0 | `43a1228a5e65d4e8ac8418bcda2aeda98dace8bb` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/src/checks/catalog.test.ts) |
| `packages/conformance/src/shell/reference-shell.test.ts` | modified | 137 | 0 | `c37183d3d5ba9512577d31352c607fe68720bb2f` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/src/shell/reference-shell.test.ts) |
| `packages/conformance/src/shell/reference-shell.ts` | modified | 129 | 27 | `05a3145501642fc3772da749b2f76e3f91056559` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/src/shell/reference-shell.ts) |
| `packages/conformance/src/validators/envelope.test.ts` | modified | 93 | 12 | `49d00e9e30c9125bf66efab9492b22f986df511b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/src/validators/envelope.test.ts) |
| `packages/conformance/src/validators/envelope.ts` | modified | 81 | 16 | `570d2106005014fb9d20cc02571a7a4770ce14a2` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/src/validators/envelope.ts) |
| `packages/conformance/src/validators/manifest.test.ts` | modified | 1 | 1 | `f373099e1776b17a01df431a4a53935966850fee` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/src/validators/manifest.test.ts) |
| `packages/conformance/src/validators/manifest.ts` | modified | 0 | 6 | `32f5b25945d86044dc09c8050ad470ba87e5ffe0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/conformance/src/validators/manifest.ts) |
| `packages/core/README.md` | modified | 32 | 15 | `ec2399ae7b732a382cdd26fa32293421e5ae1403` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/README.md) |
| `packages/core/src/index.ts` | modified | 4 | 0 | `40c8c59dfb33ba33356ec75c8525567ec8c3debe` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/index.ts) |
| `packages/core/src/intent-contract.test.ts` | added | 81 | 0 | `7269408bf47893354271a1f4a2a19d4a2b0fb1c4` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/intent-contract.test.ts) |
| `packages/core/src/topics.ts` | modified | 11 | 15 | `c46c4ba6d3eb634395e77fa317182e8a45eade5c` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/topics.ts) |
| `packages/core/src/types/global.ts` | modified | 6 | 17 | `b29bbfb010e1a3cc1df7995d841cfd61c53c8c40` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/types/global.ts) |
| `packages/core/src/types/global/nostr-api.ts` | modified | 6 | 6 | `b0e4a85b82f635548bc89b8d9ff5fc523faa8078` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/types/global/nostr-api.ts) |
| `packages/core/src/types/global/runtime-api.ts` | modified | 4 | 6 | `865a212195ac9203adf612005f3170769c9102e0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/types/global/runtime-api.ts) |
| `packages/core/src/types/global/service-api.ts` | modified | 45 | 23 | `88e481fed2ef773206123f1c21dc42050b354eb9` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/types/global/service-api.ts) |
| `packages/core/src/types/intent.ts` | modified | 49 | 18 | `930e8c2463d99de0ffe57dfd3ea8a3cee634dc2f` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/core/src/types/intent.ts) |
| `packages/nap/README.md` | modified | 49 | 28 | `a574bcbf9501156ae080f2a6922cb906eca38f11` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/README.md) |
| `packages/nap/src/boundary-smoke.test.ts` | modified | 65 | 2 | `bd8813d9204b76a79f623a8595bc9378df8569c1` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/boundary-smoke.test.ts) |
| `packages/nap/src/config/sdk.ts` | modified | 1 | 2 | `0da4006a1044f2e95eae301d878cb68e1227e3e3` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/config/sdk.ts) |
| `packages/nap/src/config/shim.test.ts` | added | 49 | 0 | `1e6a3dfdfbac004a1b5d36bb9fd20f4a33a5492b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/config/shim.test.ts) |
| `packages/nap/src/config/shim.ts` | modified | 5 | 31 | `d989b91477f97575f1ef4c40f8e99625f07fb02f` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/config/shim.ts) |
| `packages/nap/src/config/types.ts` | modified | 1 | 1 | `6ad300acc20554ffde1d9b9b47b0d6c52c840395` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/config/types.ts) |
| `packages/nap/src/convention-uri.test.ts` | added | 57 | 0 | `2c661c9749c2b81dabc8d0c19267b3830d078290` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/convention-uri.test.ts) |
| `packages/nap/src/convention-uri.ts` | added | 72 | 0 | `1a8db0c46d517edf2374b5e5022b429d8b18191b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/convention-uri.ts) |
| `packages/nap/src/inc-compat.test.ts` | modified | 166 | 1 | `44ddefcefe8a2c738a4c72666ae5a4b1608c94ec` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/inc-compat.test.ts) |
| `packages/nap/src/inc/sdk.ts` | modified | 7 | 8 | `8245b41dda7210018baad78b7933921e0c50626b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/inc/sdk.ts) |
| `packages/nap/src/inc/shim.ts` | modified | 63 | 25 | `25d5ffaebe647523fea363e5310a541e96a9f907` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/inc/shim.ts) |
| `packages/nap/src/inc/types.ts` | modified | 12 | 8 | `0c9111f54a0fe4db5e3fd6851340964f316d8335` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/inc/types.ts) |
| `packages/nap/src/intent/index.ts` | modified | 11 | 9 | `6bf1daf1606044a139452251ccee2bea67e5a32b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/intent/index.ts) |
| `packages/nap/src/intent/sdk.ts` | modified | 34 | 18 | `56df884c8c5dfe6b075a108a085b2fb2c05c86a8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/intent/sdk.ts) |
| `packages/nap/src/intent/shim.test.ts` | modified | 223 | 24 | `e20fb1f58194b4f174d4c05ee5deb88f6ac2f176` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/intent/shim.test.ts) |
| `packages/nap/src/intent/shim.ts` | modified | 139 | 37 | `8fd94fa71a16865f90fb8438a09867ff81954c54` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/intent/shim.ts) |
| `packages/nap/src/intent/types.ts` | modified | 43 | 89 | `c81cb8ff82a153b5f6e62b98a31d9a12af1edcb0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/nap/src/intent/types.ts) |
| `packages/sdk/README.md` | modified | 51 | 42 | `a382c2756369e90cd58512a039860a605b85ef7e` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/sdk/README.md) |
| `packages/sdk/src/config.ts` | modified | 3 | 5 | `aebdc8bce3937c813f14d572d3cf9165769473c8` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/sdk/src/config.ts) |
| `packages/sdk/src/cvm.ts` | modified | 31 | 23 | `177467b52aa402df48807be6530626111e80d999` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/sdk/src/cvm.ts) |
| `packages/sdk/src/nap-runtime.ts` | modified | 1 | 0 | `08af5a25d619638033e7da92037d835d515fb6dd` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/sdk/src/nap-runtime.ts) |
| `packages/sdk/src/nap-types.ts` | modified | 3 | 0 | `49d6fa1a746353e92cd4f04a9019034bdfb9fd1d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/sdk/src/nap-types.ts) |
| `packages/sdk/src/relay.ts` | modified | 8 | 9 | `8e8298f5ae3d7dd85b5fead222efb893e95c8480` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/sdk/src/relay.ts) |
| `packages/shim/README.md` | modified | 66 | 32 | `c40cb29712777393500b2fc54dd0ac74b741d781` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/shim/README.md) |
| `packages/shim/src/runtime-guard.test.ts` | modified | 4 | 2 | `5884b22135e10bfc5bea58aa49e3212a6ab3ded3` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/shim/src/runtime-guard.test.ts) |
| `packages/shim/src/runtime-guard.ts` | modified | 2 | 6 | `297c5826044b7b95c4f4cd9321b005586d5b467c` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/shim/src/runtime-guard.ts) |
| `packages/shim/src/runtime.ts` | modified | 2 | 0 | `953e17d17fc07b4a4048a3fa5209992459abc554` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/shim/src/runtime.ts) |
| `packages/shim/src/shell.test.ts` | modified | 44 | 8 | `1b66fb777d294453ca3c95d4b886b7e8c440a0d5` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/shim/src/shell.test.ts) |
| `packages/skills/README.md` | modified | 25 | 30 | `7afe28ae02f147f3154ddf27ebdd6f9a68963597` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/skills/README.md) |
| `packages/skills/skills/build-napplet/SKILL.md` | modified | 71 | 8 | `5e9c6e0c04516be2651a38eaf0037bee0ec8dbb1` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/skills/skills/build-napplet/SKILL.md) |
| `packages/skills/skills/design-napplet/SKILL.md` | modified | 45 | 0 | `a050aa631a7c108f9cae53cd855947eb70d8c7d6` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/skills/skills/design-napplet/SKILL.md) |
| `packages/skills/skills/make-napplet/SKILL.md` | modified | 37 | 1 | `02c689f6f15f0e255e40479b9d1cdceb7e77ac3b` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/skills/skills/make-napplet/SKILL.md) |
| `packages/skills/skills/test-napplet/SKILL.md` | modified | 4 | 2 | `a405e093961ef5cf7f88ebf6cd8622e983f1d58d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/skills/skills/test-napplet/SKILL.md) |
| `packages/skills/src/index.test.ts` | modified | 37 | 2 | `cabbe6335e685d2d8d985fdddb28e99f79d8b031` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/skills/src/index.test.ts) |
| `packages/vite-plugin/README.md` | modified | 39 | 85 | `6c17dc505023c1c318f267e9f22160c0d9a0613f` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/vite-plugin/README.md) |
| `packages/vite-plugin/package.json` | modified | 1 | 1 | `62bf666c56576b712bb8bb57fa8940bbcba895bc` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/vite-plugin/package.json) |
| `packages/vite-plugin/src/index.test.ts` | modified | 133 | 22 | `7fcfb127102c245158c247974d679711b08de2e0` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/vite-plugin/src/index.test.ts) |
| `packages/vite-plugin/src/index.ts` | modified | 9 | 11 | `4a6428a3b0fbd5da4c0b3fe9d0e6694cb48b6eb3` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/vite-plugin/src/index.ts) |
| `packages/vite-plugin/src/manifest.ts` | modified | 35 | 67 | `79aae5d2a56fc718a18fca4ff33df579e06fe42d` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/vite-plugin/src/manifest.ts) |
| `packages/vite-plugin/src/types.ts` | modified | 13 | 21 | `86ddae5771d161f51ce91b418f670a56b879f360` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/packages/vite-plugin/src/types.ts) |
| `pnpm-lock.yaml` | modified | 40 | 38 | `89af5b9a2a1c53b405dbabcfe8c4446b24c8a908` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/pnpm-lock.yaml) |
| `pnpm-workspace.yaml` | modified | 6 | 1 | `65a6bcd5b028f49428602ce80898b8f5643c17ba` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/pnpm-workspace.yaml) |
| `scripts/test-convention-contracts.mjs` | added | 213 | 0 | `cd97f8c3224888c0b4780e6d11f3341d5632d7ed` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/scripts/test-convention-contracts.mjs) |
| `scripts/test-convention-contracts.test.mjs` | added | 133 | 0 | `288975be455d4c165bb52bc1865ca51723570616` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/scripts/test-convention-contracts.test.mjs) |
| `scripts/test-tutorial.mjs` | modified | 2 | 21 | `09948aaa9d9fe90f3c15bc367bcaf6c09149addd` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/scripts/test-tutorial.mjs) |
| `tests/fixtures/napplets/broken/index.html` | modified | 0 | 3 | `296ca5550958d6d1f23d1a1df8207a0ff0dbca14` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/tests/fixtures/napplets/broken/index.html) |
| `tests/fixtures/napplets/conformant/index.html` | modified | 0 | 3 | `1afa739eb8b3c4bf6e72326cf6ce23166252899a` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/tests/fixtures/napplets/conformant/index.html) |
| `tests/fixtures/napplets/conformant/main.js` | modified | 1 | 1 | `72de4ecc0c70491c2964882de203024852c3b4c4` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/tests/fixtures/napplets/conformant/main.js) |
| `tests/fixtures/napplets/resource-data/index.html` | modified | 0 | 3 | `a2aeb7086842dd081f71d250cbd02ff1ad8c89ce` | [commit:path](https://github.com/napplet/web/blob/dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b/tests/fixtures/napplets/resource-data/index.html) |

### PR #188 inventory (33 files)

| Path | Status | + | - | Blob SHA | Immutable locator |
|---|---:|---:|---:|---|---|
| `.changeset/ad-hoc-convention-contracts.md` | removed | 0 | 16 | `655c96e1f5d268b60466d8fbbf0b8b654efef33d` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/.changeset/ad-hoc-convention-contracts.md) |
| `.changeset/ad-hoc-convention-guidance.md` | removed | 0 | 10 | `0d5ef1c64b3b19855a9734284468b0a7a15ab948` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/.changeset/ad-hoc-convention-guidance.md) |
| `.changeset/cli-d-tag-length-limit.md` | removed | 0 | 10 | `95a35ffc6e4ed3ca9622a8aea3d90dbfb6fd4d73` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/.changeset/cli-d-tag-length-limit.md) |
| `apps/conformance/CHANGELOG.md` | modified | 7 | 0 | `461194a49245aab06813a9b1726d1cb03da5b19f` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/apps/conformance/CHANGELOG.md) |
| `apps/conformance/package.json` | modified | 1 | 1 | `4090af1e940bd3db46a76eefda9beaaa59ad09a5` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/apps/conformance/package.json) |
| `packages/boilerplate/CHANGELOG.md` | modified | 9 | 0 | `7c5df1896ccb25993890735606f6914038b3b876` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/boilerplate/CHANGELOG.md) |
| `packages/boilerplate/package.json` | modified | 1 | 1 | `c09677644655836fedb7c31fae285c425d04e98a` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/boilerplate/package.json) |
| `packages/cli/CHANGELOG.md` | modified | 20 | 0 | `d0cc90613bd0c294457c29fb5cf6d5e8ecbe94d9` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/cli/CHANGELOG.md) |
| `packages/cli/deno.json` | modified | 1 | 1 | `c121e650242a0c332b5cc5da9d4dc66c1faf712e` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/cli/deno.json) |
| `packages/cli/package.json` | modified | 1 | 1 | `f357ccfaa08037d465ebfaa2d96ffe2e96ffab7f` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/cli/package.json) |
| `packages/conformance-cli/CHANGELOG.md` | modified | 11 | 0 | `17747abdb58a64de972d5da4c8be222d7eff271c` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/conformance-cli/CHANGELOG.md) |
| `packages/conformance-cli/package.json` | modified | 1 | 1 | `047bd46b3c4930a0094c9fc6493f6050ca556b82` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/conformance-cli/package.json) |
| `packages/conformance/CHANGELOG.md` | modified | 17 | 0 | `5d7fcef77ff32bb677b0842ddeeabcb74e48c398` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/conformance/CHANGELOG.md) |
| `packages/conformance/jsr.json` | modified | 3 | 3 | `44c3292f6142046fe6cedd890bde1b9d88ddf034` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/conformance/jsr.json) |
| `packages/conformance/package.json` | modified | 1 | 1 | `4afcb91e1df8e00955ac4e4b3549a053eeb9e6a4` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/conformance/package.json) |
| `packages/core/CHANGELOG.md` | modified | 11 | 0 | `6fb2bd268d58ba8442a4cddc0d1f8371a8d1007d` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/core/CHANGELOG.md) |
| `packages/core/jsr.json` | modified | 1 | 1 | `cbda4e81381214af82f3f3d29a566d9ac1ab5704` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/core/jsr.json) |
| `packages/core/package.json` | modified | 1 | 1 | `b50f3760749b80e09d517402e3edb96d0e335868` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/core/package.json) |
| `packages/nap/CHANGELOG.md` | modified | 16 | 0 | `a6bacf0ef3117938a08f9df83f1c215725064919` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/nap/CHANGELOG.md) |
| `packages/nap/jsr.json` | modified | 2 | 2 | `3850dae4b0c957be65fdb2dcc456c9932589061b` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/nap/jsr.json) |
| `packages/nap/package.json` | modified | 1 | 1 | `d125a4a5ae6d1a8b7409b94be0cb51a6899c2a62` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/nap/package.json) |
| `packages/sdk/CHANGELOG.md` | modified | 17 | 0 | `27432a029208de9e7274c3203ef809111e880a68` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/sdk/CHANGELOG.md) |
| `packages/sdk/jsr.json` | modified | 3 | 3 | `5fc54b574ac7bd676092ed5caab4785230966c49` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/sdk/jsr.json) |
| `packages/sdk/package.json` | modified | 1 | 1 | `1fb5d7f70aaf2a4166effe29315b5daea6d48960` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/sdk/package.json) |
| `packages/shim/CHANGELOG.md` | modified | 17 | 0 | `fe7c0e4365b870d47f20768c543db21d1e597150` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/shim/CHANGELOG.md) |
| `packages/shim/jsr.json` | modified | 3 | 3 | `246fe8ef3768aa591197d6665ab880ec9e640ee1` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/shim/jsr.json) |
| `packages/shim/package.json` | modified | 1 | 1 | `108051a52603853da37548e669b0c329d8fa5fdb` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/shim/package.json) |
| `packages/skills/CHANGELOG.md` | modified | 9 | 0 | `cdcaec8406882cdb1c8e6cf23b16512f69849d18` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/skills/CHANGELOG.md) |
| `packages/skills/jsr.json` | modified | 1 | 1 | `6bbff5e70675f292cc5e42b0013c50b99f0c5715` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/skills/jsr.json) |
| `packages/skills/package.json` | modified | 1 | 1 | `14c1f7229bcc35e84b0b901ef194f409615b3735` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/skills/package.json) |
| `packages/vite-plugin/CHANGELOG.md` | modified | 11 | 0 | `fea38f1c7d37e220176f3bb64a67692a09d0b88a` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/vite-plugin/CHANGELOG.md) |
| `packages/vite-plugin/jsr.json` | modified | 2 | 2 | `1a547e5c8879cc4ab1223e23ecb19a741aae781e` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/vite-plugin/jsr.json) |
| `packages/vite-plugin/package.json` | modified | 1 | 1 | `75cabba693b60483d472a8f84b09efd2e3cf5507` | [commit:path](https://github.com/napplet/web/blob/60889f1c2476e063500c7ab6624af6abe0dbcbe5/packages/vite-plugin/package.json) |

## Evidence metadata register

| Evidence ID | Immutable revision / locator | Digest | Retrieved | Authority / evidence / maturity | Uncertainty | Affected requirements/phases | Refresh trigger |
|---|---|---|---|---|---|---|---|
| `SRC-WEB-PR-184-20260728` | merge `4916777862ababd09fa13cf155f4b4079c8e8cb1`, tree `11d4c67a47fd399f801bf0339885dc3dda9780aa`; PR/diff and inventory locators above | exact Git blob SHAs per inventory | `2026-07-28T09:36:09Z` | implementation candidate / GitHub API and merged code / observed-current | material for protocol normativity and runtime generalization | EVID-02, EVID-03; Phase 01; identity/manifest lessons and ADR-0006 | NIP-5A/NIP-5D revision or CLI/release change |
| `SRC-WEB-PR-186-20260728` | merge `dd7b3a728eb9c838b7218fcec7bb7bb00e7cc88b`, tree `33edc8387973f31687dfb20181a40fe936286824`; PR/diff and inventory locators above | exact Git blob SHAs per inventory | `2026-07-28T09:36:09Z` | implementation candidate / merged code, PR prose, docs/tests / observed-current | material; #91 open and no independent execution or protocol authority review | EVID-02, EVID-03; Phase 01; DRF-INTENT/MANIFEST/METADATA/IDENTITY and ADR-0003/4/5/6/8 | linked NAP status/revision, web HEAD/release, or before Phase 2 |
| `SRC-WEB-PR-188-20260728` | merge `60889f1c2476e063500c7ab6624af6abe0dbcbe5`, tree `d1bd6d78bb357506e6f4244537fecd54262f9a55`; PR/diff and inventory locators above | exact Git blob SHAs per inventory | `2026-07-28T09:36:09Z` | implementation/release metadata candidate / package manifests + changelogs / observed-current | material; registry publication/integrity/export behavior unverified | EVID-03, EVID-04; Phase 01–02; CLM-CMP-PACKAGE-001, SPK-G, ADR-0010 | package registry/release record, artifact integrity change, or package admission decision |
| `SRC-WEB-HEAD-20260728` | `main` HEAD `60889f1c2476e063500c7ab6624af6abe0dbcbe5` | Git commit SHA | `2026-07-28T09:36:09Z` | repository identity / GitHub branch API / point-in-time | mutable branch pointer after retrieval | Phase 01 source freshness; ADR-0011 | any default-branch movement |

## Non-modification statement

This research created this report only. No candidate manifest, claims, drift rows, open questions, matrix, lessons, ADRs, spikes, application code, branch, or commit was changed.


## Supplement — exact active-artifact trace from targeted comparison

This supplement expands the refresh queue with every directly relevant active identifier located in the Phase 1 research corpus. No active artifact names PR #184, #186, #188 or literal `queryless`; the corpus correctly treats these matters as blocked research, so the mapping below is a refresh route rather than a claim of resolution.

### Canonical-state and candidate records

* `source-registry.yaml`: `SRC-POLICY-001` is preserved planning-policy context and `SRC-POLICY-002` is project evidence policy. Neither is upstream proof and neither should be replaced by this report.
* `candidate-source-manifest.yaml`: all candidates remain `acquisitionState: blocked`. Refresh candidates are `CAND-NIP-5D`, `CAND-NAPPLET-WEB-REPOSITORY` (#184); `CAND-NAP-REGISTRY`, `CAND-NAP-PROJECTION`, and `CAND-NAP-GOVERNANCE` (#186); and `CAND-NAPPLET-WEB-PACKAGE` plus `CAND-NAPPLET-WEB-REPOSITORY` (#188).
* `open-work-snapshot.json`: `OW-NIP5D-001` (identity), `OW-NAP-001` (registry/projection/governance), and `OW-NAPPLET-WEB-001` (repository/package) are directional records with `immutableReference: null`. Preserve their historic result, then attach a new dated immutable snapshot rather than overwriting the absence record.
* `ecosystem-inventory.yaml`: `ECO-NAPPLET-WEB-PACKAGE` and `ECO-NAPPLET-WEB-REPOSITORY` require refresh for their currently unpinned identity/release-byte assertions.
* `open-work-analysis.md` explicitly categorizes NIP-5D, NAP and `napplet/web` issue/PR/discussion signals as directional and calls for a dated immutable snapshot. Its conclusion remains applicable.

### PR #184 precise impact map

| Area | Exact active records needing review | Why |
|---|---|---|
| Claims/drift | `CLM-UPSTREAM-BASELINE-001`, `CLM-DRF-IDENTITY-NORMATIVE`, `CLM-DRF-IDENTITY-OBSERVED`, `DRF-IDENTITY-001` | The CLI `d`-tag relaxation is immutable observed implementation evidence, but it does not settle the identity/aggregate mapping or protocol rule. |
| Questions/matrix | `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-VERIFIER-001`, `CMP-BASELINE-001` | These require identity, manifest/resolver and verifier sources; #184 supplies a CLI source point only. |
| Lessons | `LES-003` (`03-nostr-underneath.md`), `LES-007` (`07-identity-and-distribution.md`), `LES-009` (`09-designing-a-good-napplet.md`) | Their terminology, drift, “do not teach as settled,” and follow-up sections explicitly prohibit treating `dTag` as a stable identity/design rule. |
| ADRs/spikes | `ADR-0006` directly via `DRF-IDENTITY-001`; `ADR-0005`/`ADR-0008` indirectly via the identity/manifest/verifier questions; `SPK-D-IMPACT-001` | Keep proposed/blocked: fixture bytes/mutations and a CLI diff do not establish loader, verifier, manifest, or aggregate identity semantics. |

### PR #186 precise impact map

| Area | Exact active records needing review | Why |
|---|---|---|
| Claims/drift | `CLM-DRF-INTENT-NORMATIVE`, `CLM-DRF-INTENT-OBSERVED`, `DRF-INTENT-001`; additionally `DRF-MANIFEST-001` and `DRF-METADATA-001` | #186 touches handler/catalog semantics, manifest tags, archetype/convention metadata, and observed sender/delivery behavior. |
| Questions/matrix | `OQ-UPSTREAM-BASELINE-001`, `CMP-BASELINE-001` | The question already requires distinct released-public and current/open-work evidence, conflict recording, and review. |
| Catalogs | `ARC-CANDIDATE-001` in `archetype-convention-catalog.yaml`; `DOM-CANDIDATE-001` in `domain-catalog.yaml` | Both name `DRF-INTENT-001` as known drift and forbid selecting conventions, composition/capability mappings, domains, host profiles, or first lab from unreviewed work. |
| Lessons | `LES-002` (`02-cast-and-mental-model.md`), `LES-008` (`08-apps-that-cooperate.md`), `LES-009`, `LES-013` (`13-evolving-the-protocol.md`) | Their handler/catalog, wire representation, routing/delegation/discovery/composition, and proposal-status sections require the observed-versus-normative distinction. |
| ADRs/spikes | `ADR-0004` directly via `DRF-INTENT-001`; no dedicated intent-contract spike outcome exists | Keep `ADR-0004` proposed. Do not claim a generic spike validates queryless, acceptance, source-independent delivery, or sender-attestation semantics. |

### PR #188 precise impact map

| Area | Exact active records needing review | Why |
|---|---|---|
| Claims/drift | `CLM-CMP-PACKAGE-001`, `CLM-DRF-ARTIFACT-NORMATIVE`, `CLM-DRF-ARTIFACT-OBSERVED`, `CLM-DRF-CONFORMANCE-NORMATIVE`, `CLM-DRF-CONFORMANCE-OBSERVED`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001` | Committed package manifests/changelogs are new version evidence, not registry artifact integrity, export, or runtime evidence. |
| Questions/matrix | `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`, `CMP-BASELINE-001` | They require registry/project provenance, license, integrity, root export, release/implementation separation and a public conformance target. |
| Package analysis | `package-map.md` and `phase-governance.yaml` | The former says exact version/integrity/export/revision/browser evidence is absent; the latter’s blocker `OQ-PUBLIC-PACKAGE-BASELINE-001` and blocked `ADR-0010` continue to prohibit package admission/updates/conformance claims. |
| Lessons | `LES-007`, `LES-010` (`10-anatomy-of-a-napplet.md`), `LES-011` (`11-build-test-and-publish.md`) | Their package/release workflow sections must distinguish the committed versions observed here from an installed/audited published package. |
| ADRs/spikes | `ADR-0010` direct; `ADR-0002` through artifact drift; `ADR-0009` through conformance drift; `ADR-0005`/`ADR-0008` through package/conformance questions; `SPK-G-IMPACT-001` | Keep the package spike materially uncertain: no qualified package was installed or executed in this research. |
