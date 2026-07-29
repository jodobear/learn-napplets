# Kehto/web upstream refresh — 2026-07-28

## Scope and outcome

- **Window (UTC):** `2026-07-25T09:29:46Z` through `2026-07-28T09:29:46Z` (inclusive search bounds).
- **Retrieved:** `2026-07-28T09:34:19Z` via authenticated public read-only GitHub REST API (`gh api`); no upstream or Learn Napplets artifact was modified except this report.
- **Result:** **5 merged pull requests** were returned. The GitHub Search API reported `total_count: 5` and returned 5 results at `per_page=100`; pagination was enabled, so the result set was not silently capped.
- **Decision:** this is a review trigger, not a protocol-authority update. The window contains substantial merged implementation and a package-version release PR, but no independently inspected normative `napplet/naps` source. Existing blocked Learn Napplets upstream claims remain blocked.

## Repository identity and retrieval anchor

| Repository | GitHub ID | URL | Default branch | Private | Archived | Default HEAD | Default HEAD tree | HEAD commit time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kehto/web | 1204025151 | https://github.com/kehto/web | main | false | false | 54ef2ead03ee0c37783727468b8658b6dc224137 | 4e88d775afb6e27ffeef1e143a2477bbe7dd28b6 | 2026-07-27T19:42:01Z |

Identity metadata was retrieved at `2026-07-28T09:34:19Z` from `GET /repos/kehto/web`. Default-branch content is anchored to immutable commit [`54ef2ead03ee0c37783727468b8658b6dc224137`](https://github.com/kehto/web/commit/54ef2ead03ee0c37783727468b8658b6dc224137) and tree [`4e88d775afb6e27ffeef1e143a2477bbe7dd28b6`](https://api.github.com/repos/kehto/web/git/trees/4e88d775afb6e27ffeef1e143a2477bbe7dd28b6).

### Evidence metadata

- **Authority:** GitHub REST data and Git objects are authoritative for the public repository identity, branch ref, PR metadata, merge relation, commit/tree IDs, and listed blob IDs. They are **not** normative authority for the NAP/NIP protocol merely because a repository implementation references it.
- **Evidence class:** merged implementation behavior (commit/path/blob evidence); PR narrative/release proposal (PR body); repository-history fact (GitHub API); analyst inference (impact comparison below).
- **Maturity:** repository-history facts are high-confidence and immutable at the cited commits; behavior observations are high-confidence only for the cited implementation snapshot; normative protocol implications are unconfirmed.
- **Uncertainty:** PR #204’s body references external `napplet/naps` commit and open PRs #89–#92, but those external sources were not retrieved in this bounded `kehto/web` refresh. Their status/authority therefore remains unverified here.
- **Affected Learn Napplets scope:** Phase 1 / source-research gate and the dependent Phase 2 product/content-contract gate. No current production requirement, ADR acceptance, or implementation decision is changed by this report.
- **Refresh trigger:** any change to `kehto/web` default HEAD; a new merged PR touching `RUNTIME-SPEC.md`, `packages/**`, `apps/playground/**`, `tests/**`, security guards, package release metadata, or docs/examples; or acquisition of an immutable normative `napplet/naps` source.

## Enumerated merged pull requests

| # | Title | URL | Author | Created | Merged | Base | Head | Merge commit | Merge tree | Labels | Files / diffstat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 204 | chore: chase Napplet convention and runtime conformance | https://github.com/kehto/web/pull/204 | dskvr | 2026-07-23T22:35:09Z | 2026-07-27T18:48:09Z | kehto:main @ `dd79b04122c94ab63a08b856c377eb2e807f6644` | kehto:chore/napplet-scheme-conformance @ `59f56ce47e7eec2ec4438393f0c59b55f653cb04` | `b85db51db838866de753b275b9d34ec908785bd2` | `6ba4a4f6cdd52c2231d80f1ff913f7727720c8a3` | none | 389 / +40629 −4852 |
| 208 | docs: require dedicated Kehto worktree root | https://github.com/kehto/web/pull/208 | dskvr | 2026-07-26T10:47:00Z | 2026-07-26T11:20:06Z | kehto:main @ `738c3ce5aa398a413e50155ea505bd96bb6792e3` | kehto:chore/worktree-location-policy @ `c665bedc61109eed57d6a8e025446694a0002cfd` | `dd79b04122c94ab63a08b856c377eb2e807f6644` | `69370045e970c03bdb1effb77dd507cc16ccf916` | none | 6 / +68 −5 |
| 209 | Version Packages | https://github.com/kehto/web/pull/209 | github-actions[bot] | 2026-07-27T18:55:20Z | 2026-07-27T19:10:47Z | kehto:main @ `b85db51db838866de753b275b9d34ec908785bd2` | kehto:changeset-release/main @ `12eff5b7fe2114b6816ed870c36aa4ba5af0c569` | `4eafa058d18cf245b23d49b23bc29dda0b7d7651` | `24563d1aa55989c09f6134a15b4492c4c66fc8c6` | none | 35 / +279 −101 |
| 210 | docs: record Phase 106 closeout | https://github.com/kehto/web/pull/210 | dskvr | 2026-07-27T19:07:04Z | 2026-07-27T19:10:24Z | kehto:main @ `b85db51db838866de753b275b9d34ec908785bd2` | kehto:chore/phase-106-closeout @ `55da5e4f27d88ec7484098e02ea11a5b11ef7261` | `c3cc7f27ea4681e8b3334a5b109e228c97ff96a8` | `b70e8cfb8c381e57bbf81583277a7c8ab7bf9cec` | none | 7 / +308 −48 |
| 211 | fix(pages): follow extracted playground frame loader | https://github.com/kehto/web/pull/211 | dskvr | 2026-07-27T19:18:11Z | 2026-07-27T19:42:02Z | kehto:main @ `4eafa058d18cf245b23d49b23bc29dda0b7d7651` | kehto:fix/pages-deployment-30295407069 @ `1d08541dac0cadd3bb9a4f37d1d41ff444c0bba9` | `54ef2ead03ee0c37783727468b8658b6dc224137` | `4e88d775afb6e27ffeef1e143a2477bbe7dd28b6` | none | 16 / +267 −29 |

All five PRs target `main`; all were merged within the requested window. PR #204 was created before the window but merged within it, so it is included.

## PR-by-PR inspection and relevance

### PR #204 — chore: chase Napplet convention and runtime conformance

- **URL/author:** https://github.com/kehto/web/pull/204 — `dskvr`
- **Immutable implementation anchor:** merge commit [`b85db51db838866de753b275b9d34ec908785bd2`](https://github.com/kehto/web/commit/b85db51db838866de753b275b9d34ec908785bd2); tree `6ba4a4f6cdd52c2231d80f1ff913f7727720c8a3`; base `dd79b04122c94ab63a08b856c377eb2e807f6644`; head `59f56ce47e7eec2ec4438393f0c59b55f653cb04`.
- **Diff snapshot digest:** SHA-256 `87688bba7f4f62b98f7a3dd83c7fe4e250e13fc049c95a0b4a9f9ee5ec44fb8d`. PR #204 uses a locally generated binary diff of immutable base `dd79b04122c94ab63a08b856c377eb2e807f6644` to merge `b85db51db838866de753b275b9d34ec908785bd2` because GitHub’s PR diff endpoint returned HTTP 406 for its >300-file diff; other PRs use fetched GitHub diff representations. Exact changed blob IDs are in the manifest below.
- **Relevance classification:** Protocol, runtime, security boundary, packages, examples/docs/tests.

**Merged implementation behavior (observed):** a large conformance migration touches `RUNTIME-SPEC.md` (+70/−10), 110 `packages/**` files, 48 `apps/**` files, 44 test files, 14 docs files, and security/active-surface checks. At default HEAD, `RUNTIME-SPEC.md` describes `napplet:<archetype>/<intent>[...?params]`, NAP-INC exact topic identity, runtime-attested `(dTag, aggregateHash)` identity, content-addressed `iframe.srcdoc` loading, sandbox `allow-scripts`, and a one-time `shell.ready` → `shell.init` handshake. `apps/playground/src/playground-frame-loader.ts` registers the computed identity and environment before assigning `iframe.srcdoc`; `shell-host.ts` remains the shell/intent side. These are implementation observations at the cited default-head commit, not normative protocol conclusions.

**PR proposal/narrative:** the author states that NAP-SHELL is retained as host-owned because released core/shim omit it, labels NAP-INTENT PR #91 as open draft, and says NAP-RESOURCE has no standalone authority and NAP-DM is a gap. This is useful provenance but remains PR-authored narrative pending direct primary-source review.

**Impact:** high relevance to candidate runtime, identity, handshake, intent, manifest, unknown-message, and egress/security research. It must prompt targeted evidence acquisition, not unblock `CLM-UPSTREAM-BASELINE-001`.

**Linked issue/discussion review:** `GET /issues/{number}/comments` returned 0 comments for this PR; its issue timeline had no cross-referenced issue/discussion event. PR body references to external NAP PRs (principally #204/#209) are unverified narrative references, not linked authority evidence in this report.

<details><summary>Complete changed-file manifest (389 files; status, additions, deletions, immutable blob SHA)</summary>

| Status | Path | Additions | Deletions | Git blob SHA |
| --- | --- | --- | --- | --- |
| added | .changeset/phase-102-acl-inc.md | 5 | 0 | `e515c9bfcfa07f408fda126fc3757f20d2032366` |
| added | .changeset/phase-102-runtime-inc.md | 5 | 0 | `f7a738f511ab683766c9353185e8ca1027da9d0b` |
| added | .changeset/phase-102-services-inc.md | 5 | 0 | `bc95338674c62b76262941ac25ad35198f4af7f6` |
| added | .changeset/phase-102-shell-inc.md | 5 | 0 | `9feaca7bdb7c4a087313865e0d2dbdb26118b31c` |
| added | .changeset/phase-103-acl-identity-theme.md | 5 | 0 | `a330a44c569bdf5771cfeb296eaf51d942c18c74` |
| added | .changeset/phase-103-paja-identity-theme.md | 5 | 0 | `a431338f0cbb0629605f6479316cd74a086eca1c` |
| added | .changeset/phase-103-runtime-identity-theme.md | 5 | 0 | `b9eb4e1062ef998d9bbc0b958dadbbbb9d10313d` |
| added | .changeset/phase-103-services-identity-theme.md | 5 | 0 | `01a61c4400822612e406528450cb3e050104d93f` |
| added | .changeset/phase-103-shell-identity-theme.md | 5 | 0 | `01e3bcad0c46169f2eb4e034de993082285e1028` |
| added | .changeset/phase-105-published-package-line.md | 29 | 0 | `38abacef9320803d7280091bc7c7355258d2d3c4` |
| added | .planning/NAP-CONVENTIONS-6461E4B-DELTA-AUDIT.md | 325 | 0 | `8e7871c6ab93845853ea0100c572284f77edfc1c` |
| added | .planning/NAP-CONVENTIONS-DRAFT-PRS-89-90-91-92-AUDIT.md | 275 | 0 | `de6ae6baf48ae9ab073f89330140ab2b583f5b9d` |
| modified | .planning/PROJECT.md | 11 | 15 | `d51f099d340f5725123d86c95c4d6c66dd6afbbe` |
| modified | .planning/REQUIREMENTS.md | 415 | 26 | `5dab9451182c723035e93b098f6983ca8d265da0` |
| modified | .planning/ROADMAP.md | 362 | 2 | `68a8fa33a642c20bcc11cc5bb579e69b95965e07` |
| modified | .planning/STATE.md | 171 | 18 | `1544f208127aeb6b0426cee702b730a7c3b814bc` |
| added | .planning/WINDOWS.md | 373 | 0 | `c67bec90482313cd0cd3d2d7c4adb10a3465ffa3` |
| modified | .planning/config.json | 1 | 1 | `30827b623147dc8e6355ee1f9af654f5454a44fd` |
| added | .planning/milestones/v1.28-REQUIREMENTS.md | 51 | 0 | `be66590c9414a55f8045e61371e9efd103407eed` |
| added | .planning/phases/101-nap-shell-session-integrity/101-01-PLAN.md | 232 | 0 | `707a1a2eb7af87eac8730f740f65aa0320cb5cdc` |
| added | .planning/phases/101-nap-shell-session-integrity/101-01-SUMMARY.md | 106 | 0 | `4f2c1dcd73e280ca89da257fcdd730200f1cb537` |
| added | .planning/phases/101-nap-shell-session-integrity/101-02-PLAN.md | 243 | 0 | `472b6f5175acd4d87fee0d889d5fdec64ed9d55a` |
| added | .planning/phases/101-nap-shell-session-integrity/101-02-SUMMARY.md | 134 | 0 | `7bc4db1cc973f451340236f6209c18ad7647c04b` |
| added | .planning/phases/101-nap-shell-session-integrity/101-03-PLAN.md | 219 | 0 | `1bd6ae7b1b7eb0899bdeda90f6ed22ead299fb28` |
| added | .planning/phases/101-nap-shell-session-integrity/101-03-SUMMARY.md | 134 | 0 | `653631829b9c1a78c7f6941877dfa2b891fee57f` |
| added | .planning/phases/101-nap-shell-session-integrity/101-04-PLAN.md | 182 | 0 | `082029e18e7a4db1e3016b9453914bea50bd2552` |
| added | .planning/phases/101-nap-shell-session-integrity/101-04-SUMMARY.md | 111 | 0 | `45f0c4c588e810ed21313ee407799b8e300615e6` |
| added | .planning/phases/101-nap-shell-session-integrity/101-05-PLAN.md | 205 | 0 | `199fa49c8e1b6df0bbee05cbcb4fbd3e33afdb79` |
| added | .planning/phases/101-nap-shell-session-integrity/101-05-SUMMARY.md | 139 | 0 | `2b9c86941ebf150c284417f9b6b962cfcfe7f1dc` |
| added | .planning/phases/101-nap-shell-session-integrity/101-CONTEXT.md | 98 | 0 | `c14f57408b08875e4f47dd11da62e9bff124ff15` |
| added | .planning/phases/101-nap-shell-session-integrity/101-PATTERNS.md | 280 | 0 | `d5b0fddc86eebd04802b2c7428484b675670ff46` |
| added | .planning/phases/101-nap-shell-session-integrity/101-PR89-INC-TRANSPOSITION-RESEARCH.md | 108 | 0 | `8a55328cfba42b5b4bf3f70425e23f4bf4c83f97` |
| added | .planning/phases/101-nap-shell-session-integrity/101-RESEARCH.md | 393 | 0 | `2408988aea0e08c847f902041d5e0b4964b42f25` |
| added | .planning/phases/101-nap-shell-session-integrity/101-REVIEW-FIX.md | 36 | 0 | `b15db99fc0f26a978c6f8c19192ca12f0ec9f643` |
| added | .planning/phases/101-nap-shell-session-integrity/101-REVIEW.md | 73 | 0 | `30fa821a48220ce026574e7fd966801a61c5bda2` |
| added | .planning/phases/101-nap-shell-session-integrity/101-SECURITY.md | 85 | 0 | `1e2e6f751805b2c523e29d87ca07f62d7037b0e5` |
| added | .planning/phases/101-nap-shell-session-integrity/101-UPSTREAM-DELTA.md | 204 | 0 | `75cffbebc67b2f90adc16ee5f0b013462f5bc6f9` |
| added | .planning/phases/101-nap-shell-session-integrity/101-VALIDATION.md | 91 | 0 | `b2136e0de35cb7cabb4282afa1ae994c00488d30` |
| added | .planning/phases/101-nap-shell-session-integrity/101-VERIFICATION.md | 123 | 0 | `c1f19421620397c95ad16e37bd296b971cbd2e70` |
| added | .planning/phases/101-nap-shell-session-integrity/COVERAGE.md | 1 | 0 | `b5cc04b407313f6840291f0f0045c84d1bb0ee53` |
| added | .planning/phases/101-nap-shell-session-integrity/deferred-items.md | 5 | 0 | `9a5c737844db9dc3bee73f2f9a30dba07713e268` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-01-PLAN.md | 155 | 0 | `6554b6f15ec730b217ab9d3cdd3b7dde22b7becc` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-01-SUMMARY.md | 123 | 0 | `3f30e6538db85f40532218562a1293d98711bbc6` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-02-PLAN.md | 187 | 0 | `3f98dd9e2aec817eaa4ed8bacd9acfa099fd619e` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-02-SUMMARY.md | 126 | 0 | `7b527ffbfc31fc9addc22cc29221a6af471d75e4` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-03-PLAN.md | 182 | 0 | `feea0cfabf82a4e6fc92e9f95e227db25450ec74` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-03-SUMMARY.md | 119 | 0 | `4f90d181d7be88d7dbbe3b00312ec5d428b6a8a7` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-04-PLAN.md | 190 | 0 | `26b941f47b0dafaa9636a934f7e6fb5689c85c05` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-04-SUMMARY.md | 127 | 0 | `dd1b0a34e209230a42d89c06e0193aa1a0444f1d` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-05-PLAN.md | 157 | 0 | `1b791417173142dc7e5278abf914d7a3ad8924b9` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-05-SUMMARY.md | 143 | 0 | `73038b89796770dba2ba42c9dff1b5bc470aa298` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-06-PLAN.md | 161 | 0 | `545926451e16a11238ad6030733e52afc8c07e34` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-06-SUMMARY.md | 130 | 0 | `83f32ddfedd9284e296f8d4a1d5d45ec842fed8b` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-07-PLAN.md | 159 | 0 | `6a2f83b9d6a17ed95307070ce50c074f0191bc33` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-07-SUMMARY.md | 137 | 0 | `00d77f026c20263ad7d444535e04835f3afab535` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-08-PLAN.md | 149 | 0 | `21f52e4837c670abc9055c9a58cce65cee39f6eb` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-08-SUMMARY.md | 152 | 0 | `1a2f54d5b9f1c6c31b01823cb251775d0040dcdc` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-09-PLAN.md | 126 | 0 | `089676b94e97f85fd9c6fb8fd893b0db288a5512` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-09-SUMMARY.md | 118 | 0 | `93f5b06e4b0f7e1278a1d687d848d9891d481b94` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-10-PLAN.md | 170 | 0 | `f1d8584d6e82b1855b1e89794f6840a3e9cbbb2d` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-10-SUMMARY.md | 90 | 0 | `7d05a13155bde432973d164ad641e81184430311` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-11-PLAN.md | 134 | 0 | `2b4e91c8cfe1b8d2b455f3f88b3e8f468dc8bb15` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-11-SUMMARY.md | 176 | 0 | `100871894f8a92d18d2349cc085197a5d47c77b9` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-12-PLAN.md | 141 | 0 | `dd0444def0bbf53d2ed7cac5fe10114ceaeef532` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-12-SUMMARY.md | 118 | 0 | `52e9b50257fdbce901542b86d7437836c5dc29ce` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-13-PLAN.md | 166 | 0 | `26283ce4747be5f6ae1bf434768848596841e112` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-13-SUMMARY.md | 122 | 0 | `2c9410d7f524114cf1d22d152627a3ece9d8b014` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-14-PLAN.md | 254 | 0 | `2e7d95cb4f828c2e8442a777c4a24c9b7d9615ff` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-14-SUMMARY.md | 159 | 0 | `1c5078324dcd67c1b5593c9a5e2e8912ba2af58a` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-CONTEXT.md | 132 | 0 | `9ca287f65e5904733b313691bdcd8cf227d9429e` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-PATTERNS.md | 301 | 0 | `d231b9ec9590c1fcf61f5c56fd7cef3ab3f928ae` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-RESEARCH.md | 511 | 0 | `50da4aa017857663004ee2e4aa8963107672ab00` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-REVIEW-FIX.md | 55 | 0 | `7bc3bfb246403eb56b6e2a84282f13e5554382e2` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-REVIEW.md | 84 | 0 | `9981d96cdb1610d77a7fd37979bdb9cbee99fa55` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-SECURITY.md | 102 | 0 | `3e7f043f7a5a47d63776c9342ea33df4d21f944e` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-VALIDATION.md | 207 | 0 | `702bbfe00772459553b2bd573cf74b5b2091bd25` |
| added | .planning/phases/102-nap-inc-event-channel-parity/102-VERIFICATION.md | 143 | 0 | `01cf276d3e12a43e9cf1d019f552ed00126beb0c` |
| added | .planning/phases/102-nap-inc-event-channel-parity/deferred-items.md | 5 | 0 | `9ab53a38ab324db9e163c3b8600abf20ad4005bb` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-01-PLAN.md | 195 | 0 | `83f0b226b985454ce6bba93411f35adcdce55921` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-01-SUMMARY.md | 79 | 0 | `9b2266d5e306de66627f9c58ea966dc39d939b6b` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-02-PLAN.md | 271 | 0 | `447579ad8763d871ac13d9d0513d453a1e2ff70a` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-02-SUMMARY.md | 133 | 0 | `53dbc080d0a5463dfb5575f87e615cf726a4e961` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-03-PLAN.md | 199 | 0 | `111504425c73128fbaae1743914451030d231e62` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-03-SUMMARY.md | 143 | 0 | `a3b20cfc5341aa2b0a262e1e786cd058fa077ed0` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-04-PLAN.md | 194 | 0 | `b41d7596c912de60d52ae42f74fe1f2305387c84` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-04-SUMMARY.md | 150 | 0 | `5816ccc35770c69d187a322de562a208043c00f0` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-05-PLAN.md | 258 | 0 | `3abd32b8038564672cc2d5598b2a9b76d4480bd8` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-05-SUMMARY.md | 128 | 0 | `c11225bcacb6f0649f06303c35f913246fd8546e` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-06-PLAN.md | 217 | 0 | `7fbffbdfd9e993c33c0ba83852d25c7e62604817` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-06-SUMMARY.md | 149 | 0 | `4dd6f57311a45579b2ef2a99990d02dbda29e39d` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-07-PLAN.md | 292 | 0 | `3273e2695e1b8a21735dd0bc911632a3f8409364` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-07-SUMMARY.md | 149 | 0 | `4136e5fc4e35adccde8a7b12257214f895914a07` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-CONTEXT.md | 65 | 0 | `034f9b16bf826f37d8924e9763be5003f2557bc8` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-PATTERNS.md | 249 | 0 | `501fd6fde47616cc1b3d9445f2770bc6eb67aa74` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-PLAN-OUTLINE.md | 22 | 0 | `a5ffe5c5b655383da26be7ee8d3c730d73763989` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-RESEARCH.md | 310 | 0 | `ee772da9d516316811162f760ec4ba878e50fd9f` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-REVIEW.md | 82 | 0 | `c57c3d9af60daa3d136839972b39a96253137afd` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-SECURITY.md | 86 | 0 | `7d318a34f8b38df8f6afa4ef56aacc6078e55017` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-VALIDATION.md | 155 | 0 | `201f67662b9332013bfd59ba99b243faf9cbb7a8` |
| added | .planning/phases/103-identity-and-theme-wire-parity/103-VERIFICATION.md | 131 | 0 | `31681ee682b284dc2cad8ae73df802c0352972cf` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-01-PLAN.md | 226 | 0 | `9fce5f92f8c624be71290d60808d049e65504d40` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-01-SUMMARY.md | 149 | 0 | `f73538841274d133f3af3ac5c4ce123eceb3479c` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-02-PLAN.md | 224 | 0 | `cba0700eb2a3e75acd31c8366ab32b0b80ac3bce` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-02-SUMMARY.md | 177 | 0 | `1b38be80f7620ad1c8c1409bb8ee94b0add9c361` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-03-PLAN.md | 198 | 0 | `be92334dabd0ed7066a5deaafa9975cf14efda80` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-03-SUMMARY.md | 176 | 0 | `ecb3a28bc2eeb26689e355440ff2d8e4c0c727df` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-04-PLAN.md | 257 | 0 | `99dfea76646caf21af889cdce7f233150843bcfe` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-04-SUMMARY.md | 204 | 0 | `a562094e8cbf6195ca3d20b31fa9c627296e0877` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-05-PLAN.md | 250 | 0 | `0a80cf3e71958eb1bbd72fd5f9ce7af69a990fc9` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-05-SUMMARY.md | 221 | 0 | `5ec16708db4ab09a11f178779217db16b3cdf0ef` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-06-PLAN.md | 94 | 0 | `c92e87dfa57c42d118c1974ae1f6d27121e03028` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-06-SUMMARY.md | 122 | 0 | `db3552d7f06e4ac1fac3a1952f5681b92079bd0b` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-CONTEXT.md | 74 | 0 | `002ac3ce10eec3a1213fadc305caf7be60e48463` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-PATTERNS.md | 274 | 0 | `a7ffad35a2056f4fcdaefaf80cc6fc8774d333fe` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-PLAN-OUTLINE.md | 35 | 0 | `7ea52c59150c27646b64be6361ebeb2eeb6e54f5` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-RESEARCH.md | 491 | 0 | `e5075462376a422219f97fe5a9aa421b8065e94c` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-VALIDATION.md | 114 | 0 | `c95de7f05edbfcd8c84956100b2a7e33078782f3` |
| added | .planning/phases/104-nap-intent-and-manifest-contract-parity/104-VERIFICATION.md | 133 | 0 | `68dc64ada56132b0f526c101517ed580a4f99d27` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-01-PLAN.md | 139 | 0 | `f6b5004b62fb9f9ce282b5865e3ef437eadd5a64` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-01-SUMMARY.md | 138 | 0 | `cd6cab978b2b8e7f57e41cbd4cfe2f201df9d5f8` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-02-PLAN.md | 122 | 0 | `a1df9f189be95872f0b85d083f420f8f6ef1b564` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-02-SUMMARY.md | 131 | 0 | `672e9d9fa6559c9a101f84087f3aa06dd620b309` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-03-PLAN.md | 128 | 0 | `b240bc24b49654776853057a6831104e97d1dee9` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-03-SUMMARY.md | 111 | 0 | `4fa70b33096ae516c7925d06197daa7c8b42a76f` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-04-PLAN.md | 156 | 0 | `fe3246130526fe8da44da4f3cbe3b16d1f27a51a` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-04-SUMMARY.md | 133 | 0 | `d742e5bd85a783362127486fe994ea1fbd96140b` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-05-PLAN.md | 163 | 0 | `fc33ab2f478b316a454f7f684784ad0bf57e6226` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-05-SUMMARY.md | 156 | 0 | `88b51948d11ceb4543198c2f509109031c9ef875` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-06-PLAN.md | 161 | 0 | `7137b81e650f45157df5dd698c8011b9d32d7de2` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-06-SUMMARY.md | 118 | 0 | `2efd97cec22f88950f494ff5d5531cb11f5d817e` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-07-PLAN.md | 160 | 0 | `d3851c4e92e617c2d04ab9ab2e649f1f7134c035` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-07-SUMMARY.md | 134 | 0 | `642e78a6b4edc2892f53e6baab9d7275ec026b66` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-08-PLAN.md | 168 | 0 | `9eec9e887f762fb3d442dda2006c42df1897565a` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-08-SUMMARY.md | 168 | 0 | `c92d8f587341faa3ce4a190f4acef163b552e97c` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-09-PLAN.md | 187 | 0 | `5a7a2b53728ebf1e8426b8b5dd3bc899ee9ba70b` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-09-SUMMARY.md | 198 | 0 | `48d1c4143576a63e892b88d95e48a18ae16180b9` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-10-PLAN.md | 159 | 0 | `8b8372a445d5bb913d54beb737b9651a9d07d70e` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-10-SUMMARY.md | 138 | 0 | `dbd5bcaff7b6cc5e297158a10e26091e891bd052` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-11-PLAN.md | 171 | 0 | `218ae26027cdb252b185eb39ff2141f255b3c8b5` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-11-SUMMARY.md | 143 | 0 | `b406e8ab5634ddf459777e56ac6249b323e5e5cb` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-12-PLAN.md | 124 | 0 | `94b4a509adeb08a72a154604bfcbc80ffc26b360` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-12-SUMMARY.md | 130 | 0 | `c0b809f3a9175308acf77df8d13d84498302c11d` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-PATTERNS.md | 266 | 0 | `6eeee613627f2239fed4296fa67da52f7eba4fdf` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-RESEARCH.md | 346 | 0 | `b652fc8c2949f3bbb4b256284cbd99e09233d68c` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-REVIEW-FIX.md | 62 | 0 | `26386be1c80825dcc1cbe3a03ad5e2e4a2bfe779` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-REVIEW.md | 61 | 0 | `b02f14bb109b0f6ff89176492ed2a484f6b395fc` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-SECURITY.md | 95 | 0 | `6f88ba919bb261266ce3884a9c9219108ad0897a` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-UI-REVIEW.md | 102 | 0 | `f74d5e9736689723e6bd687d948420002fc2e8a1` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-VALIDATION.md | 134 | 0 | `c5332389694fd1d7c3b4bcf19aadf1993228c76b` |
| added | .planning/phases/105-published-convention-adoption-and-host-flows/105-VERIFICATION.md | 147 | 0 | `77b0a984e6ce687a8715b20ceea9f3fcf0577f38` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-01-PLAN.md | 271 | 0 | `948c974e6c9f97b4839c9ed90799cd71662a1c9b` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-01-SUMMARY.md | 89 | 0 | `b2dbc8654e52ff64faaf9d2bcf1a6d15f25eb445` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-02-PLAN.md | 178 | 0 | `93e88295095966b1d3a68876d4423e531a9dccce` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-02-SUMMARY.md | 119 | 0 | `337a545fa2a44d47853056089ef60dace3d6ed0d` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-03-PLAN.md | 222 | 0 | `ca51889f1da475f51b6e19fcfdfa77ea64fcb874` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-03-SUMMARY.md | 119 | 0 | `157e4110806c294c4d66618d1da20de84af9c362` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-AUTHORITY-REVALIDATION.md | 65 | 0 | `71290610f3d7f1c45928bb36de9b70cece02f02c` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-CONFORMANCE-MATRIX.md | 61 | 0 | `37859778204b6f68865c3869774cbc75583bc4fb` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-PATTERNS.md | 274 | 0 | `4b56402268dea1977f45a4585d001a0984f51514` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-RELEASE-CHECKLIST.md | 171 | 0 | `8dbb6ad151c9a960a90647ea612c162a4b35d727` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-RESEARCH.md | 346 | 0 | `22072f111456f7ec3a45874b7065b0df24701b4c` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-REVIEW-FIX.md | 39 | 0 | `d2079af965c00081cf4abb274217af4af8c12080` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-REVIEW.md | 38 | 0 | `c4e7dba5b3654044750f7535c33a2960ebc9e38b` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-VALIDATION.md | 84 | 0 | `fe766c8bf8c8e558b34549bdd7379d26a3cc98bc` |
| added | .planning/phases/106-active-surface-conformance-and-release/COVERAGE.md | 1 | 0 | `acffc1805e32319ef98358c55c7b3a34c181cd44` |
| modified | AGENTS.md | 11 | 0 | `b9b66df2eb9d383265150a083a07e63a610a5874` |
| modified | RUNTIME-SPEC.md | 70 | 10 | `d90cab7dcad177c6eacb6f0780b434b5ecffccab` |
| modified | apps/playground/README.md | 76 | 8 | `91304c184ed2aa79521af8ea25151e2b7a4bff5c` |
| modified | apps/playground/napplets/ble-demo/package.json | 3 | 3 | `49f5d762775b10b2f339a44ea19fe7929b3fb9b3` |
| modified | apps/playground/napplets/bot/package.json | 4 | 4 | `fc0b494d02a055ec6e8ffe52e4a370293feffb57` |
| modified | apps/playground/napplets/bot/src/main.ts | 8 | 21 | `db445889ca469432308250d95d36714fb33f82e3` |
| modified | apps/playground/napplets/chat/package.json | 5 | 5 | `f4d3d5ebc1b4e64de0ac81435cbd974104f877e7` |
| modified | apps/playground/napplets/chat/src/main.ts | 4 | 17 | `1fee11adbbd366500318532714906c248a332ec2` |
| modified | apps/playground/napplets/common-demo/package.json | 3 | 3 | `e8facf01dd8f9efa13d5cad71048c6b63df35a18` |
| modified | apps/playground/napplets/composer/package.json | 5 | 5 | `ad40d487bbd29f47706e2d9258c96318dcd6fe6f` |
| modified | apps/playground/napplets/cvm-relatr/package.json | 4 | 4 | `2c337c037e064d7be36577953e7a661849200a76` |
| modified | apps/playground/napplets/feed/package.json | 5 | 5 | `8e28b40dea26eb52cd202ebca473b7dfc664392f` |
| modified | apps/playground/napplets/feed/src/main.ts | 12 | 4 | `2831244265928040cf5940aa94dd4621edeb7d96` |
| added | apps/playground/napplets/feed/src/profile-media.ts | 88 | 0 | `aeeeb39197d19575ff0c3e6c8fd9199c59960244` |
| modified | apps/playground/napplets/feed/vite.config.ts | 1 | 1 | `d3186302c03fa1ec5de11e0850b79cd802fe2937` |
| added | apps/playground/napplets/inc-event.ts | 20 | 0 | `11a3efbf7a6316e8503e8f6c18a26bdfec415fb6` |
| modified | apps/playground/napplets/link-demo/package.json | 3 | 3 | `dc5ca3338794cca993d41715f7e5bf1656de0711` |
| modified | apps/playground/napplets/lists-demo/package.json | 3 | 3 | `b9349fe718e9847749ea0e680ae5c9c55303363d` |
| modified | apps/playground/napplets/preferences/package.json | 4 | 4 | `2f0bcd92894a56eab3a7c99bee84393cf2ad6da1` |
| modified | apps/playground/napplets/preferences/src/main.ts | 2 | 3 | `f37ae23cc71f865dacf20955960392d6ab9386a3` |
| modified | apps/playground/napplets/profile-viewer/index.html | 10 | 0 | `c1149ec1697c4fec04ec86d3ef2d535e59cf3935` |
| modified | apps/playground/napplets/profile-viewer/package.json | 4 | 4 | `7463baec69bfc69548a78f3602de66d11d425bf6` |
| modified | apps/playground/napplets/profile-viewer/src/main.ts | 83 | 63 | `e9d39db066e21bb83408f733f07c6cdaa925bb3c` |
| added | apps/playground/napplets/profile-viewer/src/profile-load-controller.ts | 82 | 0 | `6c5f9831a1fcd9c68cffc1b8ad1e8d380bdd9b5d` |
| added | apps/playground/napplets/profile-viewer/src/profile-media.ts | 88 | 0 | `7f46d13767899ca3ad725be96bb3072e33dfc647` |
| modified | apps/playground/napplets/profile-viewer/vite.config.ts | 1 | 1 | `9b1c2019115efbdcfc0512734fd9d8bc22c84f55` |
| modified | apps/playground/napplets/resource-demo/package.json | 4 | 4 | `d7547dba4ea4ce89d41feca8309972011e552fbf` |
| modified | apps/playground/napplets/resource-demo/src/main.ts | 1 | 1 | `828c50d47d8741a79f1efcc0fd84d27d87699510` |
| modified | apps/playground/napplets/serial-demo/package.json | 3 | 3 | `7f172e128ae78746e3eed2cb79c697c68309bcad` |
| modified | apps/playground/napplets/shared-vite-config.ts | 60 | 15 | `a6cdf33fcba1e0ea623ba18e1689dfdb7045558c` |
| modified | apps/playground/napplets/toaster/package.json | 4 | 4 | `9e80d13ae8d37a502417e0afe72cb7f3e8a818e6` |
| modified | apps/playground/napplets/webrtc-demo/package.json | 3 | 3 | `85740ec9d95709211be1b06d8e3f50a2ad0e63c0` |
| modified | apps/playground/package.json | 3 | 1 | `129bbfd68242b1db09c68afb7d0ef16e3b5ce7fc` |
| modified | apps/playground/src/acl-panel.ts | 7 | 0 | `d1195a73963c9ca6022d3f0b4245b9d980cfa3e0` |
| modified | apps/playground/src/demo-hooks.ts | 33 | 12 | `6d0ea224ae4c2bc4da756ee7dfd6f4d248689548` |
| modified | apps/playground/src/flow-animator.ts | 18 | 24 | `3d8e962bf949e3349868eec835c50ccd5be02227` |
| added | apps/playground/src/installed-napplet-catalog.ts | 178 | 0 | `c8885cb7ad7d49fbaee0e4f5de82412f0e2c21fd` |
| modified | apps/playground/src/main-notifications.ts | 12 | 12 | `e9cea5da74effb132de721ee6d5f81c38a7db7dc` |
| modified | apps/playground/src/main-preferences.ts | 14 | 14 | `220f9fa14cdd04041d83eb805e131fe2001bcd87` |
| modified | apps/playground/src/main-signer.ts | 27 | 9 | `a1d54a047d8b3176838e917bb09093ddfa7c131d` |
| modified | apps/playground/src/main.ts | 58 | 17 | `05b04f01af0023b210fa6acd28f4dcc8a1937088` |
| modified | apps/playground/src/message-tap.ts | 20 | 0 | `e70bb2cc62a5c4ae435f210100c721309e0c4b9d` |
| modified | apps/playground/src/napplet-resolver.ts | 4 | 4 | `d06f805863e05e64343d5e3bf1a4f9b65ac42fb1` |
| added | apps/playground/src/playground-access-controls.ts | 296 | 0 | `78a037a799e8c756af4bdeb728f9585349a200e7` |
| added | apps/playground/src/playground-frame-loader.ts | 158 | 0 | `49976f4c8868f6f31e16a9ffeb33080646cdb3b4` |
| modified | apps/playground/src/playground-intent-catalog.ts | 13 | 4 | `8c4ace5c0b0187954b821f71240ffff454527de2` |
| added | apps/playground/src/playground-intent-controller.ts | 162 | 0 | `58905c5f50bf2348221c84180025b1e3e9fa5f18` |
| modified | apps/playground/src/playground-relay-service.ts | 25 | 21 | `2fa812d7a2f3b66c2f40b2cdbca49358ff61baee` |
| modified | apps/playground/src/shell-host.ts | 358 | 370 | `3ce64f8ee2b08cf3909359c390453f627b181229` |
| modified | apps/playground/src/signer-modal.ts | 9 | 1 | `948ac018e375240d73a85573aa67b6fe3aaaa8b8` |
| modified | docs/how-tos/paja-getting-started.md | 21 | 0 | `c942b88114c0dfce2eccc9dbbc4ab84b9006d5b7` |
| modified | docs/how-tos/paja-local-authoring.md | 22 | 0 | `6bb9878cd42bcdc48545cd93d370fdb71d585564` |
| modified | docs/migrations/GAP-ANALYSIS.md | 2 | 2 | `b2bd6621adaf144a58f329111250fb667bff31d8` |
| modified | docs/migrations/RUNTIME-MIGRATION.md | 8 | 2 | `0c3acb8a31f0c146913f238e92c5f57ec1c433ff` |
| modified | docs/packages/acl.md | 2 | 2 | `1d124f806ff82fb7c4a7fecb6c92b2b82495f0e1` |
| modified | docs/packages/firewall.md | 1 | 1 | `e64438b115036ba7e20dc410227959749479587b` |
| modified | docs/packages/paja.md | 39 | 5 | `2f9d51a6fae7a4737ff0948b2d715282a34ff5e6` |
| modified | docs/packages/playground.md | 37 | 2 | `e84454507be7ab2f0f25ba41302f9fe6a9cafe67` |
| modified | docs/packages/runtime.md | 9 | 2 | `53435506d8fd8d5b268f1bbdc876088b2cccba99` |
| modified | docs/packages/services.md | 11 | 3 | `08156f850a86e19a90129864d172d9fa4d9a3e61` |
| modified | docs/packages/shell.md | 8 | 2 | `b3a58a012fad08bc39469199fdec1e8470ee2964` |
| modified | docs/policies/NIP-5D-CONFORMANCE.md | 105 | 2 | `9e976ce5b1f5285ade588a1734c09ff1c8dc516f` |
| modified | docs/policies/SHELL-RESOURCE-POLICY.md | 47 | 32 | `08024792868f483ee2f95a39e152bbdcd782a629` |
| modified | docs/superpowers/specs/2026-06-15-nap-intent-design.md | 5 | 0 | `d8b3a4e4f7b73ad8a4050ba221cf0811a59fff60` |
| modified | packages/acl/README.md | 5 | 0 | `62c9e5a60510a5ced67027b2e3858e55e3c6fa71` |
| modified | packages/acl/jsr.json | 2 | 2 | `fa8457e3083658d68d7fdf89c2021fea3ae936d7` |
| modified | packages/acl/package.json | 4 | 4 | `e777cc13eed9e4bb82c4ef1dadbede9941c4bd4c` |
| modified | packages/acl/src/resolve.test.ts | 27 | 72 | `68f95041e23a90ef31bd8645aeed160e37543dd5` |
| modified | packages/acl/src/resolve.ts | 43 | 22 | `7f00b1d841d52c721a47132c0d3bf0163b5c1fab` |
| modified | packages/cli/package.json | 4 | 4 | `4db0dbf6ac46152ad0c348bd374f76f3dc626a20` |
| modified | packages/firewall/README.md | 5 | 0 | `588ce0bff6d8a2618a8696a29593982bd05aa208` |
| modified | packages/firewall/jsr.json | 1 | 1 | `843b1c72447edefd15223ac54b173c7a5dd431ca` |
| modified | packages/firewall/package.json | 2 | 2 | `558999ccab67d679d9bd92cb7f1f69ebaa67ac1d` |
| modified | packages/firewall/src/evaluate.ts | 9 | 4 | `c263547a75da318df58cd3e3174aae06fcedbd64` |
| modified | packages/firewall/src/types.ts | 11 | 5 | `f34ef81ef4c950c4df38993664a86b1d2eddea66` |
| modified | packages/nip/README.md | 17 | 0 | `878e116afd0d283bce7c583b247e864110186788` |
| modified | packages/nip/src/5d/index.test.ts | 47 | 14 | `7d9b2e37ff22274041515dfd4942f96960f8d99f` |
| modified | packages/nip/src/5d/index.ts | 58 | 11 | `443470e8bfbee8ac0fb9dad06e2953e475977708` |
| modified | packages/paja/README.md | 38 | 2 | `8522581e3c0092f50ccb4cc6900d7d96b9902ef6` |
| modified | packages/paja/jsr.json | 2 | 2 | `929c29d8654aecab46101d1c3843327e5cdbbecc` |
| modified | packages/paja/package.json | 4 | 4 | `e1183a923a8ff2b2ae4d7c6be61fb006892bcfe0` |
| added | packages/paja/src/browser-adapter-intent.test.ts | 201 | 0 | `6ac835c4dbb0587768572070484969cd46a9fc9f` |
| modified | packages/paja/src/browser-adapter.ts | 68 | 46 | `273bf12128b617500ca0c418de2e818a6fa5c5ed` |
| added | packages/paja/src/browser-devtools.test.ts | 97 | 0 | `6f2992c0be1fdf27e4d5667128e7f0843a0b802c` |
| modified | packages/paja/src/browser-devtools.ts | 8 | 0 | `d3cb32f3d1d94ed30e948e245b678ed2bdaf27ca` |
| added | packages/paja/src/browser-host-runtime.ts | 26 | 0 | `0558bd0310fa488073794347719b061abaaab305` |
| added | packages/paja/src/browser-host-signer.ts | 94 | 0 | `25f74ce710e1b2ffd59e0fd7679a7896753b38b3` |
| modified | packages/paja/src/browser-host.test.ts | 180 | 10 | `9189e3de8a4fc12bef03a543efd7d45a3cbe6ead` |
| modified | packages/paja/src/browser-host.ts | 83 | 153 | `7a74a1ef4703b40850b616242b3e5168807d7d9e` |
| added | packages/paja/src/browser-intent-controller.test.ts | 120 | 0 | `f1080788395e74fd18d2affcfe89234ae5be829b` |
| added | packages/paja/src/browser-intent-controller.ts | 159 | 0 | `fee74cf25c0b514a681cd9f3897994e7e0bf34ce` |
| added | packages/paja/src/browser-intent-host.ts | 304 | 0 | `6f182d05c812d8ff9a346280a694c3947742e50e` |
| modified | packages/paja/src/browser-relay-runtime.test.ts | 133 | 2 | `9d51640ba3229338289ae2f143729745da9e41b8` |
| modified | packages/paja/src/browser-relay-runtime.ts | 35 | 19 | `7dafc346fce08fc3ff0ffa4f7b68cc0a87dcfc33` |
| modified | packages/paja/src/browser-runtime-tabs.test.ts | 6 | 0 | `ae6954c9e14134b51039289ec7ec01e13e11db69` |
| modified | packages/paja/src/browser-runtime-tabs.ts | 21 | 28 | `070f1969b9ba46e26a1c29c715e3815f4e54955d` |
| added | packages/paja/src/browser-target-diagnostics.ts | 36 | 0 | `127e29259ceef4a33bd29db93bafcbb97a217180` |
| modified | packages/paja/src/browser-target-frame.ts | 41 | 39 | `058c7154c030467619de5124f5a94ef061dd89e8` |
| modified | packages/paja/src/index.ts | 11 | 0 | `c619c3ea237055985462e60e5a6e7fd23b6ffacb` |
| added | packages/paja/src/installed-napplet-catalog.test.ts | 159 | 0 | `4bef9dec9cfa85cda0005eb62beafb555d2f9a66` |
| added | packages/paja/src/installed-napplet-catalog.ts | 170 | 0 | `83695f918571b80b812b5799094b82b54d097349` |
| modified | packages/paja/src/parity.test.ts | 84 | 6 | `ceb2f5189d624d9cdf29dfbf64e95ef2df8a2415` |
| modified | packages/paja/src/parity.ts | 20 | 0 | `e19f0dc301dc222873e76d6b4f34d4cb1b5f7204` |
| added | packages/paja/src/theme-broadcast.ts | 31 | 0 | `ba997a2b837add2b4d7d6bf22582bbea80544860` |
| modified | packages/runtime/README.md | 110 | 1 | `37145487fab374fc4bdf96e05f250e955f8a02e0` |
| modified | packages/runtime/jsr.json | 2 | 2 | `005d4ed50ced75a4e748818a91339766a282c78a` |
| modified | packages/runtime/package.json | 4 | 4 | `6ea436e53af691b5cabc2f0ec77104d8b78a82eb` |
| modified | packages/runtime/src/acl-state.test.ts | 15 | 0 | `432c9fdc0442d67c79d4af1cac23a7343c12c955` |
| modified | packages/runtime/src/acl-state.ts | 12 | 0 | `740b8d43eaf4fbbd23b02c0b508e165444f2dd34` |
| modified | packages/runtime/src/dispatch.test.ts | 616 | 55 | `0d52ebce9fe02bc6e0e2d42fb26c482db8efcbb3` |
| modified | packages/runtime/src/domain-handlers.ts | 11 | 12 | `a6b1931b173957a542758ade1f15cab5df9c6de9` |
| added | packages/runtime/src/domain-results.ts | 91 | 0 | `f4b2cb7397435b0b6559d9a2cf98210b33e8cc54` |
| modified | packages/runtime/src/firewall-dispatch.test.ts | 25 | 2 | `d5215c85632006379623afa394f6342973669a0e` |
| modified | packages/runtime/src/identity-handler.ts | 9 | 11 | `86865a5f19197d11b06aeb9e63884913336f347c` |
| modified | packages/runtime/src/inc-handler.ts | 104 | 29 | `a2cb7d2ccfcc0db3d58b95f04caa41aabf0305e5` |
| modified | packages/runtime/src/index.ts | 2 | 1 | `9f6fc48ee19c15e1a81fa7f4f1d9f024d4eb1391` |
| modified | packages/runtime/src/intent-dispatch.test.ts | 237 | 10 | `b028e6a3a85fe02f92c76e405064ed1441ca509a` |
| modified | packages/runtime/src/relay-handler.ts | 126 | 68 | `d47789b38061783fe441e27e18427cd325bab135` |
| modified | packages/runtime/src/replay.ts | 66 | 12 | `e602ab8c489578ac81a1be3a1981f5bcf5e43b78` |
| modified | packages/runtime/src/runtime.test.ts | 278 | 24 | `4cac1c0734f45e21547753394e8d5cc63b46834c` |
| modified | packages/runtime/src/runtime.ts | 151 | 13 | `263e8bd41bbfd9b5dc0523ac8cc9e5b8ce1dc220` |
| added | packages/runtime/src/service-dispatch.test.ts | 61 | 0 | `5a3008635835ad217dfaca9f68074d605373d293` |
| modified | packages/runtime/src/service-dispatch.ts | 7 | 17 | `e2a210b10dc208f542a93fa1b50c73bfa9cdba43` |
| modified | packages/runtime/src/session-registry.ts | 22 | 1 | `fb20f37203e959721c1c9697e8edcc28113d3d7f` |
| modified | packages/runtime/src/types.test.ts | 42 | 0 | `a2b35d0111a0669b7adb8acf66c9d34870dc8ebd` |
| modified | packages/runtime/src/types.ts | 64 | 4 | `059c8360fee49ce20ed2b9224dd7acdb73a69904` |
| modified | packages/services/README.md | 98 | 18 | `76604e6f8fa32e86e6d2ff05f01dceef10df86b7` |
| modified | packages/services/jsr.json | 2 | 2 | `db8b45929374241154edc45af1bebdcc190a9a1e` |
| modified | packages/services/package.json | 5 | 6 | `a8f78c776261bb1c86c1e5ca195af4511e06711d` |
| removed | packages/services/src/audio-service.ts | 0 | 126 | `12e7cc846e349881c9c2d8ec0487fe5027e2a220` |
| modified | packages/services/src/catalog-intent-resolver.test.ts | 399 | 78 | `60369f11a68b21c06e35c171defbcd9a4bf734c5` |
| modified | packages/services/src/catalog-intent-resolver.ts | 198 | 130 | `e447348cbfd7ac24f917b0a33afa1d0c56fab17e` |
| modified | packages/services/src/coordinated-relay.test.ts | 81 | 0 | `a7dc8e041567c3385856c985e30eefd7a49c9f41` |
| modified | packages/services/src/coordinated-relay.ts | 47 | 9 | `c7908c749b08cd36df833b7dfe4a67995b6ac22d` |
| modified | packages/services/src/identity-service.test.ts | 139 | 25 | `8b2964a480a5f21235a92df49668b48a292cf2dc` |
| modified | packages/services/src/identity-service.ts | 39 | 68 | `1f2f155952cff9fc79f6588a4d6463488606ec93` |
| modified | packages/services/src/index.ts | 15 | 13 | `50a3383c5e30fcdc1a906eeee49bb02d0e3565a8` |
| modified | packages/services/src/intent-service.test.ts | 392 | 121 | `aeefe841b9c1cd4d11c2fb0d30a15c8a544c3405` |
| modified | packages/services/src/intent-service.ts | 250 | 67 | `1128c582125f14bbc576939d98e1425d6b46cdfb` |
| added | packages/services/src/intent-types.test.ts | 135 | 0 | `28f44e8c4e76f81a73b95fc54a31e306838cce1a` |
| removed | packages/services/src/intent-types.ts | 0 | 97 | `b21d3adceb4df11550e2921f892279d8ef26cb63` |
| modified | packages/services/src/manifest-intent-catalog.test.ts | 62 | 28 | `df613225686d5a02c7d6200b94c72a5246e8ee33` |
| modified | packages/services/src/manifest-intent-catalog.ts | 42 | 16 | `d680cc32d534adb1a3707542c5b7253a2deb6b92` |
| modified | packages/services/src/manifest-intent-dispatch.test.ts | 531 | 55 | `7c24c5aa73b8a4e892023d2a3ffe9345fc8849cd` |
| modified | packages/services/src/media-service.ts | 2 | 5 | `f5d46dbcea3305da7b764d2c047328afe5fa8f23` |
| modified | packages/services/src/notification-service.test.ts | 108 | 193 | `fb41816441b6f5b757e3cf53c3ade8643b1cf5f8` |
| modified | packages/services/src/notification-service.ts | 28 | 75 | `d24a08b09b89aa5732883cb4bb7c4da1d94134c8` |
| modified | packages/services/src/notify-service.ts | 4 | 6 | `f92ccd2dad36ea20d421daef0899c681b302bc02` |
| modified | packages/services/src/relay-pool-service.test.ts | 63 | 0 | `2117d5183d823869cf62098120312cde92b3f770` |
| modified | packages/services/src/relay-pool-service.ts | 42 | 9 | `d7fd7125702d8856df1aa6d01910d6928d30cdb7` |
| modified | packages/services/src/theme-service.test.ts | 47 | 27 | `47c15a94a7e85fe2d0fde08f4f2230ff16e91f7e` |
| modified | packages/services/src/theme-service.ts | 15 | 8 | `b982959edef654d65edadda4b89d393b38a7d0f3` |
| modified | packages/services/src/types.ts | 0 | 42 | `11d8c73054f7f28337a14dec9ee04faf99454868` |
| modified | packages/shell/README.md | 96 | 9 | `b762dca85ce31d58dc9f212cc420d2fa59dcedc8` |
| modified | packages/shell/jsr.json | 2 | 2 | `4d41fd629c2674a60062b695f3092c15c04fb555` |
| modified | packages/shell/package.json | 5 | 5 | `4f6f6435cb714ff29432ef6d7ff2a0e137b36a77` |
| modified | packages/shell/src/hooks-adapter.ts | 3 | 3 | `b13e1b4faa5ff7b625845e5f0d88af486b97d3ef` |
| modified | packages/shell/src/identity-proxy.test.ts | 12 | 19 | `0231fc08fbff9354c39606b292ee81145c4aff51` |
| modified | packages/shell/src/identity-proxy.ts | 13 | 18 | `849f696fcd00c13e94531263d86e5508f08cffbf` |
| modified | packages/shell/src/index.ts | 2 | 1 | `3b69516afd1d786b5fe1435f0601491f780432ab` |
| modified | packages/shell/src/napplet-namespace.test.ts | 755 | 22 | `3ac0bb708fa87d684d3d22caf824b527be15506f` |
| modified | packages/shell/src/napplet-namespace.ts | 465 | 80 | `b6f03f0e092374a1ec1f13f5bea6d2f5aade870a` |
| modified | packages/shell/src/origin-registry.ts | 20 | 0 | `5ce2915cdddefa84e05b32a7c796c9d967336ed9` |
| modified | packages/shell/src/shell-bridge.test.ts | 416 | 47 | `159f785d06ccc1778e8d7bd002c4dadb8bca1a89` |
| modified | packages/shell/src/shell-bridge.ts | 28 | 23 | `dedb14b5deb52de590075c68e05098748cd6556a` |
| modified | packages/shell/src/shell-init.test.ts | 100 | 617 | `330d158e8f5d9f7eb5cafa21eba43edd370e06e0` |
| modified | packages/shell/src/shell-init.ts | 81 | 136 | `05323e5149c21bd73bb402b9281fbd62c7b19f66` |
| modified | packages/shell/src/shell-ready.ts | 62 | 64 | `7b9bb9b277494dd5815a4ce561ce86a42d035561` |
| modified | packages/shell/src/shell-supports-conformance.test.ts | 55 | 157 | `1a15a895ad011e0206e9248435fe556cbd4701bc` |
| added | packages/shell/src/theme-proxy.test.ts | 47 | 0 | `220af51aa5f35b0642290a98e7eac954a1411c81` |
| modified | packages/shell/src/theme-proxy.ts | 15 | 26 | `3d60ea52d2e7c185fd72723941cddfaed9e42d8e` |
| modified | packages/shell/src/types.ts | 41 | 63 | `51616c110b85076a96773124f30b9a7a5e9b7840` |
| modified | packages/shell/tests/no-window-nostr.test.ts | 8 | 11 | `0910a719cf4df946ec6ac81bc1db36b8ef68015e` |
| modified | packages/shell/tests/perm-namespace.test.ts | 32 | 125 | `8454565782f15a039e26869c3a6b8d1eb3ba87df` |
| modified | playwright.config.ts | 7 | 1 | `980c925ffe1f486ff56842e26af196484d6c0f73` |
| modified | pnpm-lock.yaml | 220 | 214 | `9b31e61a0d113b79c9461720fff29706ec045bc5` |
| added | scripts/verify-napplet-authorities.mjs | 182 | 0 | `d066a2ca99c75c4b043972cf1bc1038d783a1915` |
| added | scripts/verify-phase-106-conformance-matrix.mjs | 85 | 0 | `4122bef6f457a5f00320ace4f2b836f8b2073187` |
| modified | skills/add-service/SKILL.md | 43 | 128 | `4c6d55baf15d790476984a5af10062479e6de3a0` |
| modified | skills/integrate-shell/SKILL.md | 13 | 6 | `53f99767cf48b27bc03448e40da55bdd852eaa0b` |
| modified | tests/e2e/acl-revoke-relay-write.spec.ts | 3 | 3 | `ecdbdc78ccd04e041383b87b3cf6b0995d6c79a5` |
| modified | tests/e2e/demo-audit-correctness.spec.ts | 7 | 1 | `4b379610bdb2324909a77b3de6eb4e538861aefd` |
| modified | tests/e2e/demo-notification-service.spec.ts | 12 | 3 | `51389035959bca2e852d22771ae3b343671148b0` |
| modified | tests/e2e/demo-service-toggle.spec.ts | 87 | 0 | `3b9b2ff2fb27591e1da665e6bdfc59da272a0070` |
| modified | tests/e2e/gateway-artifact-parity.spec.ts | 13 | 4 | `45c5112a3bf3c096c1e62e6799626133649ddb90` |
| modified | tests/e2e/harness/harness.ts | 15 | 29 | `46f31a8bc0bb17a6445009956b7fa8230cb74093` |
| modified | tests/e2e/harness/vite.config.ts | 17 | 0 | `63e8b9e2f92289ab70b56bd3d03b9e83142a3f4c` |
| modified | tests/e2e/identity-flow.spec.ts | 13 | 6 | `2d2b1155e715c13e487c7cb63d2123e823c79b70` |
| modified | tests/e2e/inc-roundtrip.spec.ts | 2 | 2 | `701a1c0530bd56a14b17c40f1db9c2c0b0f96def` |
| modified | tests/e2e/nap-identity.spec.ts | 43 | 43 | `0b77c43c259262e6c657a65c3ce44ab34a076e7d` |
| added | tests/e2e/nap-inc-playground.spec.ts | 245 | 0 | `4ce99c9c23d7668ca13354702b491913ba2e77fe` |
| modified | tests/e2e/nap-theme.spec.ts | 30 | 63 | `0fcfcf0084414631080b092db16b2a09bcaf624c` |
| modified | tests/e2e/naps-path-conformance.spec.ts | 3 | 1 | `5b240b0ace9bd71c81d56664d17da5537b8f388f` |
| modified | tests/e2e/notify-lifecycle.spec.ts | 11 | 5 | `2ab49406735b4cbbe375dd037e07e741de3a09ae` |
| modified | tests/e2e/paja-runtime-pointer.spec.ts | 146 | 0 | `c3a8b3d1d20d5f46f4c35cb0c672dc1fa0a479b9` |
| modified | tests/e2e/paja-single-window.spec.ts | 184 | 10 | `d1b71736fe16daac017d8d0f4f16559ec3f8eed0` |
| added | tests/e2e/playground-profile-intent.spec.ts | 90 | 0 | `d83b9fb517b60251fe032fcc911aeefc4ee863cb` |
| modified | tests/e2e/profile-open.spec.ts | 16 | 28 | `1ef67cc44da5b588fbc41f0775ed4ec7c0dc70ac` |
| modified | tests/e2e/theme-broadcast.spec.ts | 88 | 5 | `c6b37ff98f955051da6a99409e015ee70051b0ce` |
| modified | tests/fixtures/napplets/nap-identity/package.json | 4 | 4 | `01aa99a29745435c3bf7c4da6dc9325e7f705173` |
| modified | tests/fixtures/napplets/nap-inc/package.json | 4 | 4 | `3476f558db0d18cb78e64cd6410794d736843010` |
| modified | tests/fixtures/napplets/nap-inc/src/main.ts | 12 | 2 | `61acf26c55f8b74ba97855271312ca659c948df7` |
| modified | tests/fixtures/napplets/nap-notify/package.json | 4 | 4 | `716e754596432e899ec7dee9ab577f5f444aed19` |
| modified | tests/fixtures/napplets/nap-relay/package.json | 5 | 5 | `4259ac7184909eac8be9abc927838292541c2bac` |
| modified | tests/fixtures/napplets/nap-storage/package.json | 4 | 4 | `46e59d3e7400b407aef691523633e3914b7bea90` |
| modified | tests/fixtures/napplets/nap-theme/package.json | 4 | 4 | `c766f299b86320fba8d5d42b85811342446107f1` |
| modified | tests/unit/demo-config-overrides.test.ts | 22 | 0 | `7d9a15de45c9fb12199265ece3ce0308ad017320` |
| added | tests/unit/flow-animator-path.test.ts | 89 | 0 | `6c7bb96ac8a8638b6852c3ff2274bf47be750b6a` |
| added | tests/unit/identity-theme-conformance-guard.test.ts | 99 | 0 | `e4c5fdaf577965d7aedc7ee1fdd70c9a7109a723` |
| added | tests/unit/main-signer-identity.test.ts | 37 | 0 | `678ef7e3fbf0c0d31886f6d28d415ed837f0a90b` |
| added | tests/unit/nap-inc-conformance.test.ts | 85 | 0 | `49b6170a113d6ceb7ca71634f8fa29f4fd3f5a38` |
| added | tests/unit/napplet-package-alignment.test.ts | 127 | 0 | `87f612847d535f619051080bccdca7089482bc14` |
| modified | tests/unit/nip5d-conformance-guard.test.ts | 379 | 4 | `605c5032b20d5bbaff9fc5d697533311d103a67b` |
| added | tests/unit/playground-capability-maps.test.ts | 25 | 0 | `143dc07ab70384a825883bf2aed1873bfdc7ab2e` |
| modified | tests/unit/playground-gateway-guard.test.ts | 357 | 41 | `e1ad12132555eb3777fa6e723056ecbe2d539556` |
| added | tests/unit/playground-installed-catalog.test.ts | 68 | 0 | `106cf50665a7ebad5f32569204c7e487542f80b6` |
| modified | tests/unit/playground-intent-catalog.test.ts | 34 | 5 | `10b95c8a8700e12a9ee63b2fe4b8a5122f17b99d` |
| added | tests/unit/playground-intent-controller.test.ts | 290 | 0 | `b66795abd7161f0b795a040b4db4804855b1c9ac` |
| modified | tests/unit/playground-relay-service.test.ts | 15 | 8 | `7654e8e500a21f3e450d415413876ea8097f8409` |
| added | tests/unit/playground-shell-host-proxy.test.ts | 121 | 0 | `94597553c2c2fc94ad380d2e9cfbde4cdd9c94a0` |
| added | tests/unit/profile-load-controller.test.ts | 55 | 0 | `bc845c10dd74e8ef2caefd04b2a3d03ba03da550` |
| added | tests/unit/profile-resource-media.test.ts | 105 | 0 | `db885eab83cbad40e1877c248c9d0ef6293e0434` |
| added | tests/unit/published-napplet-contract.test.ts | 148 | 0 | `6f635702b3eee84a6f8783f5bd2c3f2300eb6313` |
| modified | tests/unit/sdk-migration-guard.test.ts | 279 | 38 | `5d18f60a4479d8d7bc237a211d5e72e8bbe891bf` |

</details>

### PR #208 — docs: require dedicated Kehto worktree root

- **URL/author:** https://github.com/kehto/web/pull/208 — `dskvr`
- **Immutable implementation anchor:** merge commit [`dd79b04122c94ab63a08b856c377eb2e807f6644`](https://github.com/kehto/web/commit/dd79b04122c94ab63a08b856c377eb2e807f6644); tree `69370045e970c03bdb1effb77dd507cc16ccf916`; base `738c3ce5aa398a413e50155ea505bd96bb6792e3`; head `c665bedc61109eed57d6a8e025446694a0002cfd`.
- **Diff snapshot digest:** SHA-256 `d4a5efe74ef44646842735807f11186a4eb8e36befa1c7274e32166b0dc5ea71`. PR #204 uses a locally generated binary diff of immutable base `738c3ce5aa398a413e50155ea505bd96bb6792e3` to merge `dd79b04122c94ab63a08b856c377eb2e807f6644` because GitHub’s PR diff endpoint returned HTTP 406 for its >300-file diff; other PRs use fetched GitHub diff representations. Exact changed blob IDs are in the manifest below.
- **Relevance classification:** Documentation / worktree policy; package documentation version correction.

**Merged implementation behavior:** no runtime, protocol, package export, or production security-boundary implementation changed. The six files are planning/policy plus two package-doc version rows.

**PR proposal/narrative:** portable dedicated worktree policy and stale docs-version correction.

**Impact:** no change to Learn Napplets protocol baseline; note only as an upstream documentation/release-metadata hygiene signal.

**Linked issue/discussion review:** `GET /issues/{number}/comments` returned 0 comments for this PR; its issue timeline had no cross-referenced issue/discussion event. PR body references to external NAP PRs (principally #204/#209) are unverified narrative references, not linked authority evidence in this report.

<details><summary>Complete changed-file manifest (6 files; status, additions, deletions, immutable blob SHA)</summary>

| Status | Path | Additions | Deletions | Git blob SHA |
| --- | --- | --- | --- | --- |
| modified | .planning/STATE.md | 4 | 3 | `7a03114e70c1bf396f31d387137f17fa56c0601f` |
| added | .planning/quick/260726-g8r-update-agents-md-to-require-kehto-worktr/260726-g8r-PLAN.md | 14 | 0 | `82c77b7d7b8402cd644e574b6806c156139564a4` |
| added | .planning/quick/260726-g8r-update-agents-md-to-require-kehto-worktr/260726-g8r-SUMMARY.md | 39 | 0 | `8177c56c670d8f5d1c50c7dc808a3e55d44be32a` |
| modified | AGENTS.md | 9 | 0 | `ba3545b32dff0a283ec85e3383e6313561eee0d4` |
| modified | docs/packages/firewall.md | 1 | 1 | `122e120531054c24cd89a5d341734ec32bcacf75` |
| modified | docs/packages/paja.md | 1 | 1 | `b24cc217bbe5a6a4e179f92f94e65ba5633d5b10` |

</details>

### PR #209 — Version Packages

- **URL/author:** https://github.com/kehto/web/pull/209 — `github-actions[bot]`
- **Immutable implementation anchor:** merge commit [`4eafa058d18cf245b23d49b23bc29dda0b7d7651`](https://github.com/kehto/web/commit/4eafa058d18cf245b23d49b23bc29dda0b7d7651); tree `24563d1aa55989c09f6134a15b4492c4c66fc8c6`; base `b85db51db838866de753b275b9d34ec908785bd2`; head `12eff5b7fe2114b6816ed870c36aa4ba5af0c569`.
- **Diff snapshot digest:** SHA-256 `4b0d22e05ed2718784396052b56b35c0eb2d19bc171b75e6d6643069ff1c1f57`. PR #204 uses a locally generated binary diff of immutable base `b85db51db838866de753b275b9d34ec908785bd2` to merge `4eafa058d18cf245b23d49b23bc29dda0b7d7651` because GitHub’s PR diff endpoint returned HTTP 406 for its >300-file diff; other PRs use fetched GitHub diff representations. Exact changed blob IDs are in the manifest below.
- **Relevance classification:** Release / versioning / package metadata / changelogs.

**Merged implementation behavior:** Changesets removes ten changeset files and updates package manifests, JSR manifests, and changelogs for `@kehto/acl`, `cli`, `firewall`, `paja`, `runtime`, `services`, `shell`, playground, and E2E harness. This is the only window PR explicitly performing version/release metadata changes. At current default HEAD the observed package versions differ again in some cases (for example `@kehto/runtime` `0.19.0`, `@kehto/shell` `0.18.0`, `@kehto/acl` `0.16.0`), so this PR alone is not an adequate current release baseline.

**PR proposal/narrative:** generated Changesets release text references draft upstream NAP PRs. Treat those statements as release notes, not independently verified protocol authority.

**Impact:** directly refreshes the blocked `napplet/web` package/release/export candidate; requires a separately pinned current package manifest/export snapshot and registry integrity evidence.

**Linked issue/discussion review:** `GET /issues/{number}/comments` returned 0 comments for this PR; its issue timeline had no cross-referenced issue/discussion event. PR body references to external NAP PRs (principally #204/#209) are unverified narrative references, not linked authority evidence in this report.

<details><summary>Complete changed-file manifest (35 files; status, additions, deletions, immutable blob SHA)</summary>

| Status | Path | Additions | Deletions | Git blob SHA |
| --- | --- | --- | --- | --- |
| removed | .changeset/phase-102-acl-inc.md | 0 | 5 | `e515c9bfcfa07f408fda126fc3757f20d2032366` |
| removed | .changeset/phase-102-runtime-inc.md | 0 | 5 | `f7a738f511ab683766c9353185e8ca1027da9d0b` |
| removed | .changeset/phase-102-services-inc.md | 0 | 5 | `bc95338674c62b76262941ac25ad35198f4af7f6` |
| removed | .changeset/phase-102-shell-inc.md | 0 | 5 | `9feaca7bdb7c4a087313865e0d2dbdb26118b31c` |
| removed | .changeset/phase-103-acl-identity-theme.md | 0 | 5 | `a330a44c569bdf5771cfeb296eaf51d942c18c74` |
| removed | .changeset/phase-103-paja-identity-theme.md | 0 | 5 | `a431338f0cbb0629605f6479316cd74a086eca1c` |
| removed | .changeset/phase-103-runtime-identity-theme.md | 0 | 5 | `b9eb4e1062ef998d9bbc0b958dadbbbb9d10313d` |
| removed | .changeset/phase-103-services-identity-theme.md | 0 | 5 | `01a61c4400822612e406528450cb3e050104d93f` |
| removed | .changeset/phase-103-shell-identity-theme.md | 0 | 5 | `01e3bcad0c46169f2eb4e034de993082285e1028` |
| removed | .changeset/phase-105-published-package-line.md | 0 | 29 | `38abacef9320803d7280091bc7c7355258d2d3c4` |
| modified | apps/playground/CHANGELOG.md | 15 | 0 | `d04935af642a65d4a941eb4da60f6259430ef23e` |
| modified | apps/playground/package.json | 1 | 1 | `7202a237530d093db87976449b563c482392c7a8` |
| modified | packages/acl/CHANGELOG.md | 26 | 0 | `5258aef9298e27061200125a7d6bacbd34615f9e` |
| modified | packages/acl/jsr.json | 1 | 1 | `82cf377bae1f366823ddd4655164fd1119d951be` |
| modified | packages/acl/package.json | 1 | 1 | `4c7f412f475e49604e2af994aa3c0c26a3af795b` |
| modified | packages/cli/CHANGELOG.md | 30 | 0 | `a9717f6edda2e38bcaf3a7a992f064f8ba46e689` |
| modified | packages/cli/jsr.json | 2 | 2 | `2b2dc698a63923858baa82d8e984f428e63114eb` |
| modified | packages/cli/package.json | 1 | 1 | `724e25688f2927d08b3b82792bff48a0de93f131` |
| modified | packages/firewall/CHANGELOG.md | 24 | 0 | `9b830f6c0628c6014955fdf1fc721a709b05622b` |
| modified | packages/firewall/jsr.json | 1 | 1 | `513e5310a654de9f8973a9370b952beca2902287` |
| modified | packages/firewall/package.json | 1 | 1 | `0c6680fb418cd9342bb1c8ad598204267ff9d3dc` |
| modified | packages/paja/CHANGELOG.md | 42 | 0 | `4d924670b973835cfc1ebc25fbd9683af42d143f` |
| modified | packages/paja/jsr.json | 6 | 6 | `d7e80571cddebacf54452e33aeda6771dcb10445` |
| modified | packages/paja/package.json | 1 | 1 | `4ed8e93b70a46b87c3a3133a274cc86914e5516e` |
| modified | packages/runtime/CHANGELOG.md | 34 | 0 | `7301c319bc7a677542bf9e3899cd22346d00324e` |
| modified | packages/runtime/jsr.json | 3 | 3 | `ea5d23559bfd7fd8328a9cf52d12ce2e388cfc4d` |
| modified | packages/runtime/package.json | 1 | 1 | `fc6447a2cd05edccd4bd324b29340abcfee2e935` |
| modified | packages/services/CHANGELOG.md | 33 | 0 | `1b99f20bae8534c24babb1be34948fedd441c22f` |
| modified | packages/services/jsr.json | 2 | 2 | `44d66c28ff9eb9ae006518d4bf7799ead4459af0` |
| modified | packages/services/package.json | 1 | 1 | `e7bb95b48e693665c559a2b231f8d8a5150d9c67` |
| modified | packages/shell/CHANGELOG.md | 36 | 0 | `ec54899441a6efddca65752c3bf72a24093dda63` |
| modified | packages/shell/jsr.json | 3 | 3 | `3dc4955d76031b19715e4d8e70fd45a18230503b` |
| modified | packages/shell/package.json | 1 | 1 | `e431916d83384845d792791ec024029874edef4c` |
| modified | tests/e2e/harness/CHANGELOG.md | 12 | 0 | `4d25b264e5bd277d6f189ab2d42a6b0690a6a303` |
| modified | tests/e2e/harness/package.json | 1 | 1 | `62b803a1a1f69086d7955e742a2e4acc7f24db10` |

</details>

### PR #210 — docs: record Phase 106 closeout

- **URL/author:** https://github.com/kehto/web/pull/210 — `dskvr`
- **Immutable implementation anchor:** merge commit [`c3cc7f27ea4681e8b3334a5b109e228c97ff96a8`](https://github.com/kehto/web/commit/c3cc7f27ea4681e8b3334a5b109e228c97ff96a8); tree `b70e8cfb8c381e57bbf81583277a7c8ab7bf9cec`; base `b85db51db838866de753b275b9d34ec908785bd2`; head `55da5e4f27d88ec7484098e02ea11a5b11ef7261`.
- **Diff snapshot digest:** SHA-256 `5d3c8adfcd293e91173c08479243329cf3aab400850c735ee077ec676aea753f`. PR #204 uses a locally generated binary diff of immutable base `b85db51db838866de753b275b9d34ec908785bd2` to merge `c3cc7f27ea4681e8b3334a5b109e228c97ff96a8` because GitHub’s PR diff endpoint returned HTTP 406 for its >300-file diff; other PRs use fetched GitHub diff representations. Exact changed blob IDs are in the manifest below.
- **Relevance classification:** Planning closeout documentation.

**Merged implementation behavior:** only seven `.planning/**` files changed. It does not duplicate or alter the merged implementation, per its PR narrative.

**Impact:** documentation of Kehto’s own phase closeout is not external protocol authority and does not change Learn Napplets claims. It provides context for #204 only.

**Linked issue/discussion review:** `GET /issues/{number}/comments` returned 0 comments for this PR; its issue timeline had no cross-referenced issue/discussion event. PR body references to external NAP PRs (principally #204/#209) are unverified narrative references, not linked authority evidence in this report.

<details><summary>Complete changed-file manifest (7 files; status, additions, deletions, immutable blob SHA)</summary>

| Status | Path | Additions | Deletions | Git blob SHA |
| --- | --- | --- | --- | --- |
| modified | .planning/PROJECT.md | 7 | 3 | `bd8319232912b65365c8fddf27fe117c28173eb9` |
| modified | .planning/ROADMAP.md | 5 | 5 | `949d72cd697648befe6a2a23b824acb6f3934d73` |
| modified | .planning/STATE.md | 20 | 18 | `c7b335285b31507020ab91f4f6536e1eebe34785` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-SECURITY.md | 72 | 0 | `82c7c0d5f37bfecd2299b26631775c8dc1f5989f` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-UAT.md | 29 | 0 | `3ad7319d58eaff9a620220a829f024abef6d154a` |
| modified | .planning/phases/106-active-surface-conformance-and-release/106-VALIDATION.md | 34 | 22 | `b6fad5235a12cf1e296b4095af63c1831acbb57e` |
| added | .planning/phases/106-active-surface-conformance-and-release/106-VERIFICATION.md | 141 | 0 | `0fd3510d8ad4ae07b9cf566fe426e47adac58af2` |

</details>

### PR #211 — fix(pages): follow extracted playground frame loader

- **URL/author:** https://github.com/kehto/web/pull/211 — `dskvr`
- **Immutable implementation anchor:** merge commit [`54ef2ead03ee0c37783727468b8658b6dc224137`](https://github.com/kehto/web/commit/54ef2ead03ee0c37783727468b8658b6dc224137); tree `4e88d775afb6e27ffeef1e143a2477bbe7dd28b6`; base `4eafa058d18cf245b23d49b23bc29dda0b7d7651`; head `1d08541dac0cadd3bb9a4f37d1d41ff444c0bba9`.
- **Diff snapshot digest:** SHA-256 `0c5d272b9ed2c77f1d95f31cc98235bdaba594cc82e3ca205f1205f70443420f`. PR #204 uses a locally generated binary diff of immutable base `4eafa058d18cf245b23d49b23bc29dda0b7d7651` to merge `54ef2ead03ee0c37783727468b8658b6dc224137` because GitHub’s PR diff endpoint returned HTTP 406 for its >300-file diff; other PRs use fetched GitHub diff representations. Exact changed blob IDs are in the manifest below.
- **Relevance classification:** Runtime-adjacent loader audit, CI scripts, documentation, regression tests.

**Merged implementation behavior:** the PR moves the executable gateway audit’s loader-owned checks from `shell-host.ts` to `playground-frame-loader.ts`, adds loader-ownership and package-doc-version synchronizer regressions, and changes CI/release gate scripts and package documentation. It does **not** change `apps/playground/src/playground-frame-loader.ts` or `shell-host.ts` in this PR; it corrects the audit to follow the earlier extraction in #204.

**PR proposal/narrative:** the Pages failure was described as an audit-path failure while runtime behavior remained present. That conclusion is corroborated only to the narrow extent of the changed audit/test paths; no hosted-check log was independently retrieved here.

**Impact:** reinforces the need to use immutable commit+path behavior evidence rather than file-name assumptions for loader/identity research. It is relevant to `OQ-VERIFIED-LOADER-IDENTITY-001` and active-surface/security validation, but does not advance a protocol claim.

**Linked issue/discussion review:** `GET /issues/{number}/comments` returned 0 comments for this PR; its issue timeline had no cross-referenced issue/discussion event. PR body references to external NAP PRs (principally #204/#209) are unverified narrative references, not linked authority evidence in this report.

<details><summary>Complete changed-file manifest (16 files; status, additions, deletions, immutable blob SHA)</summary>

| Status | Path | Additions | Deletions | Git blob SHA |
| --- | --- | --- | --- | --- |
| modified | .github/workflows/ci.yml | 2 | 2 | `8e48b0add7fb74ee5d13dd8b07b8db5889d14f2d` |
| added | .planning/debug/resolved/pages-deployment-30295407069.md | 74 | 0 | `9de3ee050e7e79cf11368b6e4f560b5bfd7371a2` |
| modified | docs/packages/acl.md | 1 | 1 | `7bee6da0d25c539f740b3d005a40026f9ce84f5d` |
| modified | docs/packages/cli.md | 1 | 1 | `76c8c5ecc5f341bbce5e7db986ba52ee59720ad4` |
| modified | docs/packages/firewall.md | 1 | 1 | `f92d25d5c48e098b6158a0863011d82b26d9358b` |
| modified | docs/packages/paja.md | 1 | 1 | `39d1bbf781b707da8bba4fb0f77e48ef9aa26fa8` |
| modified | docs/packages/runtime.md | 1 | 1 | `4b9afd0342838fde3665febd006aab66d7ed88ca` |
| modified | docs/packages/services.md | 1 | 1 | `82bfeec5ef8b44168328bce5149819df53736bf9` |
| modified | docs/packages/shell.md | 1 | 1 | `f862b0e99292203bcfc4815ece21e49d2024b3d3` |
| modified | scripts/audit-gateway-artifacts.mjs | 20 | 13 | `afc424858b74b8917a0529e8065bc6afaaa2e3cc` |
| modified | scripts/select-e2e-tests.mjs | 1 | 1 | `9d80b9c54ce9f48ad82dad950c99a283a5c91d78` |
| modified | scripts/sync-jsr-versions.mjs | 15 | 4 | `5db7b09c8d47f6b7c03aa3a5e644a862a4be8dff` |
| added | scripts/sync-package-doc-versions.mjs | 72 | 0 | `d036d0811c7bb90a457f7eddf9d07bac586e2c69` |
| modified | tests/unit/ci-release-gate.test.ts | 2 | 2 | `f97c367a56e2b162a40649a3779c0d94fcb56320` |
| modified | tests/unit/playground-gateway-guard.test.ts | 16 | 0 | `fffbe998a97515c982ef0eca6efe60141211908e` |
| added | tests/unit/sync-package-doc-versions.test.ts | 58 | 0 | `a95bfca9968423a8f32d813b70b267c87f11c51a` |

</details>

## Cross-PR classification matrix

| PR | Protocol | Runtime/API | Package exports/versioning | Security boundary | Examples/docs/tests | Learn Napplets relevance |
| --- | --- | --- | --- | --- | --- | --- |
| 204 | Yes | Yes | Yes — 110 package files and changesets | Yes — active-surface/authority guards | Yes — playground examples, docs, 44 test files | High; merged code is implementation evidence only |
| 208 | No | No | Docs version rows only | No runtime boundary | Docs/policy only | Low |
| 209 | No direct protocol behavior | No direct runtime behavior | Yes — manifests/JSR/changelogs/version release | No direct boundary | Changelogs/tests | High for package-baseline acquisition |
| 210 | No | No | No | No | Planning docs only | Context only |
| 211 | No direct protocol semantics | Audit follows loader behavior; no loader implementation path changed | Package-doc synchronization only | Gateway audit/CI guard only | Docs/scripts/three tests | Medium for behavior locator/audit mapping |

## Comparison to active Learn Napplets research artifacts

### What remains unchanged

- No literal `kehto` source is currently registered under `.planning/research`; the active discovery labels are `napplet/web` and related NAP/NIP references.
- `SRC-POLICY-001` (planning archive) and `SRC-POLICY-002` (current project policy) are not upstream proof and must not be overwritten by this report.
- The global gate in `CLM-UPSTREAM-BASELINE-001` remains correct: no current upstream NAP/NIP conclusion or first-lab recommendation is established until an official immutable source is collected and reviewed.
- Merged implementation code does not establish normative protocol authority; in particular, #204’s upstream references need independent direct retrieval and authority classification.

### Exact current artifacts requiring targeted refresh review

| Artifact type | Exact ID / locator | Refresh action and preserved uncertainty |
| --- | --- | --- |
| Candidate sources | `CAND-NAPPLET-WEB-PACKAGE` (`candidate-source-manifest.yaml:49-55`) | Blocked public package candidate; now needs a separately pinned released package manifest, export map, version, integrity/provenance record; PR #209 is a trigger, not the package snapshot. |
| Candidate sources | `CAND-NAPPLET-WEB-REPOSITORY` (`candidate-source-manifest.yaml:56-62`) | Blocked repository candidate; now has verified identity and default-head anchor: `kehto/web`, `main` @ `54ef2ead…`, tree `4e88d775…`. Proposed new source record only; do not retroactively mark candidate acquired without review. |
| Inventory | `ECO-NAPPLET-WEB-PACKAGE` (`ecosystem-inventory.yaml:33-37`) | Refresh blocked package identity/release/export bytes and distinguish merged source from published artifact. |
| Inventory | `ECO-NAPPLET-WEB-REPOSITORY` (`ecosystem-inventory.yaml:38-42`) | Refresh with this public repo identity, immutable revision/path/blob evidence, license and authoritative scope review. |
| Claims | `CLM-UPSTREAM-BASELINE-001` (`claims.yaml:29-65`) | Remain blocked; attach this report only as a review input, not approval. |
| Claims | `CLM-CMP-PACKAGE-001` (`claims.yaml:167-196`) | Refresh package release/export comparison due #209; remains blocked until registries/package bytes are pinned. |
| Claims | `CLM-CMP-RUNTIME-001` (`claims.yaml:197-226`) | Refresh as observed implementation comparison using #204/#211 commit+path anchors; remains non-normative. |
| Claims | `CLM-CMP-EXAMPLE-001` (`claims.yaml:227-256`) | Refresh example/playground observation using #204; retain fixture/conformance uncertainty. |
| Claims | `CLM-CMP-FIXTURE-001` (`claims.yaml:257-286`) | Refresh test/fixture observation using #204/#211; not upstream proof. |
| Matrix | `CMP-BASELINE-001` (`compatibility-matrix.yaml:3-49`) | Keep `blocked`; add a review row/candidate evidence reference only after source-record review. |
| Open question | `OQ-UPSTREAM-BASELINE-001` (`open-questions.yaml:154-196`) | Primary refresh question: acquire immutable official records; compare released/current-work; retain parallel drift and human review. |
| Open question | `OQ-PUBLIC-PACKAGE-BASELINE-001` (`open-questions.yaml:114-151`) | Refresh from released package metadata, not source-only #209. |
| Open question | `OQ-VERIFIED-LOADER-IDENTITY-001` (`open-questions.yaml:208-241`) | Refresh with #204 loader and #211 audit-path evidence; current conclusion remains unresolved. |
| Open question | `OQ-VERIFIED-LOADER-MANIFEST-001` (`open-questions.yaml:244-277`) | #204’s content-addressed loading and manifest-related code is a review trigger only. |
| Open question | `OQ-VERIFIED-LOADER-VERIFIER-001` (`open-questions.yaml:279-...`) | Review active-surface/check evidence; retain absence of independent conformance verification. |

### Drift records and candidate issue mapping

- Preserve all existing drift records as **blocked**: `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`, `DRF-DISCOVERY-001`, `DRF-EGRESS-001`, `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `DRF-HANDSHAKE-001`, `DRF-IDENTITY-001`, `DRF-INTENT-001`, `DRF-MANIFEST-001`, `DRF-METADATA-001`, and `DRF-UNKNOWN-MESSAGES-001` (`drift-register.yaml:3-...`).
- Highest-priority review associations: #204 → handshake/identity/intent/manifest/unknown-message/egress/conformance; #209 → metadata/artifact; #211 → identity/manifest/conformance verifier path. These associations are **inferences from changed paths and observed code**, not resolved drift conclusions.
- `open-work-snapshot.json:28-34` (`OW-NAPPLET-WEB-001`) and `open-work-analysis.md:5-35` must receive a **new dated snapshot/review record** rather than replacement: their active status is blocked and the existing snapshot explicitly lacks immutable source reference. This report supplies repository-history evidence but does not establish a complete source record.

### Lessons, ADRs, spikes, and governance

| Type | Exact ID / locator | Refresh disposition |
| --- | --- | --- |
| Lesson | `LES-010` — `lesson-packets/10-anatomy-of-a-napplet.md:22-36` | Refresh candidate-claim/package treatment with source-vs-published-package distinction from #209. |
| Lesson | `LES-013` — `lesson-packets/13-evolving-the-protocol.md:25-87` | Apply its rule: this source refresh creates targeted review work and cannot auto-change claim, ADR, approval, or instruction. |
| ADR handoff | `ADR-0001` through `ADR-0011` — `adr-handoff.yaml:1-99` | No acceptance status changes. `ADR-0011` source-refresh blocker remains open. |
| Phase governance | `phase-governance.yaml:14-151` | Keep Phase 1 evidence-gate/Phase 2 dependency unchanged; source refresh and ADR-0011 remain unresolved. |
| Spike impacts | `SPK-C-IMPACT-001`, `SPK-D-IMPACT-001`, `SPK-G-IMPACT-001`, `SPK-H-IMPACT-001` — `reports/spike-consolidation.md:22-36` | Review only where #204 intersects runtime/security; no local spike is promoted to upstream fact. |
| Security/egress | `security-egress-findings.md:7-49` | No production CSP/host/upstream egress conclusion is created; #204 active-surface guards are repository implementation evidence only. |

## Recommended bounded follow-up

1. Create a proposed, separately reviewed source record for the public `kehto/web` repository using the identity/default-head data above. Its authority should be limited to repository implementation and release-history evidence; it must not be recorded as NAP/NIP protocol authority.
2. Acquire official immutable `napplet/naps` protocol sources and the actual package-registry artifacts independently. Verify references that PR #204/#209 merely assert, including stated revisions and draft/open status, before changing any protocol claim.
3. Compare a pinned released `@kehto/*` package/export snapshot to the current default-head package manifests. Treat PR #209 as release-history evidence, not proof that source-head version/export bytes are the published ones.
4. Add targeted review work for loader identity, handshake, manifest, intent, unknown-message, egress, and security-boundary drift. Preserve the exact commit/path/blob locators below and do not advance maturity without human review.
5. Retain the prior open-work snapshot; create a new dated snapshot as `open-work-analysis.md` prescribes. Do not overwrite claims, matrix status, ADR state, lessons, or spike results automatically.

## Method and reproducibility

- Repository identity: `GET /repos/kehto/web`; default ref: `GET /repos/kehto/web/git/ref/heads/main`; default commit/tree: `GET /repos/kehto/web/commits/{sha}`.
- Enumeration: `GET /search/issues?q=repo:kehto/web+is:pr+is:merged+merged:2026-07-25T09:29:46Z..2026-07-28T09:29:46Z&per_page=100` with pagination. Search count and returned count both equal 5.
- Per PR: `GET /pulls/{number}`, paginated `GET /pulls/{number}/files`, PR diff, `GET /issues/{number}/comments`, issue timeline, and `GET /git/commits/{merge_sha}`. Raw/fetched diff SHA-256 values and every listed Git blob SHA are recorded above.
- #204 GitHub diff endpoint returned HTTP 406 because the PR exceeded 300 files. Its digest therefore covers a locally produced `git diff --binary <base> <merge>` using immutable GitHub-fetched commits; file-level APIs returned all 389 changed-file records, so no file list was truncated.
- Local repository comparison is read-only. The only Learn Napplets write was this report. Retrieval timestamp is the UTC time recorded at the start of evidence synthesis.

## Conclusion

The window contains 5 merged PRs, including a large merged `napplet` convention/runtime conformance implementation (#204), a release-metadata PR (#209), and a loader-audit correction (#211). These are strong public repository-history and implementation observations, but insufficient to establish normative NAP/NIP authority or unblock Learn Napplets Phase 1 upstream claims. The appropriate outcome is a bounded, review-gated refresh of the enumerated candidates, claims, questions, and drift records.

