# Upstream refresh — `napplet/naps` — 2026-07-28

## Scope and result

**Authorized activity:** public, read-only GitHub API research via `gh`; no upstream or planning artifact was changed.

**Rolling window (inclusive):** `2026-07-25T09:29:46Z` through `2026-07-28T09:29:46Z`.

**Result:** **0 merged pull requests** in the window. Consequently there are no in-scope PR diffs, changed-file records, merge commits, linked issues/discussions, or per-PR protocol/runtime/package classifications to record. This is a negative observation about GitHub merge metadata in the stated window, not evidence that the protocol is stable, normative, released, or suitable for teaching.

## Repository identity and retrieval checkpoint

| Field | Value |
|---|---|
| Repository requested / verified | [`napplet/naps`](https://github.com/napplet/naps), public, not archived |
| GitHub repository ID / node ID | `1202279733` / `R_kgDOR6lVNQ` |
| Default branch | `master` |
| Retrieval interval | `2026-07-28T09:31:48Z`–`2026-07-28T09:32:15Z` UTC |
| Latest default-branch ref at retrieval | `refs/heads/master` → commit `5ac0490461ca6fec2f0d2e45b4835cf9bc08de24` |
| Latest default-branch tree | `c2db1eb8f9f6512ad51e001b1636cc71e8d2f0fb` |
| Latest default-branch commit timestamp | `2026-07-24T10:01:21Z` (before the rolling window) |
| Default-branch commits in window | `0` |

The current default-branch head is a retrieval checkpoint only. Its commit message identifies it as PR #90, merged before the window; this refresh did **not** fetch or classify that out-of-window PR’s diff. It must not be treated as a new in-window protocol or implementation finding.

## Enumeration method and completeness

1. Verified identity/default branch with `GET /repos/napplet/naps`.
2. Enumerated every closed PR using `GET /repos/napplet/naps/pulls?state=closed&sort=updated&direction=desc&per_page=100` with `gh api --paginate --slurp`; pagination returned one page containing **59** closed PR records, of which **43** have a non-null `merged_at`.
3. Applied the requested inclusive UTC timestamp predicate to every returned non-null `merged_at`: `start <= merged_at <= end`. Result: **0** records.
4. Ran a corroborating GitHub Search query for merged PRs dated `2026-07-25..2026-07-28`; it returned `total_count: 0`. The fully paginated pulls enumeration, not Search’s date syntax, is the completeness basis.
5. Queried `GET /repos/napplet/naps/commits?sha=master&since=2026-07-25T09:29:46Z&until=2026-07-28T09:29:46Z&per_page=100`; it returned zero default-branch commits.

This did not silently cap results: the closed-PR endpoint was paginated to exhaustion, and all 59 records were examined. The nearest merged PRs precede the window: #90 at `2026-07-24T10:01:21Z`, #89 at `2026-07-24T10:00:07Z`, and #92 at `2026-07-24T09:59:52Z`.

## In-window merged PR register

| PR | Title / URL | Author | Created / merged | Base / head | Merge commit / tree | Files / labels | Relevance and evidence classification |
|---|---|---|---|---|---|---|---|
| _None_ | _No merged PR timestamp fell in the inclusive window._ | — | — | — | — | — | No PR proposal, merged implementation behavior, or inference was created. |

### Diff, issue, and discussion inspection disposition

There is no PR record to inspect. Therefore:

- no PR diff was fetched;
- no changed-file status, additions, deletions, blob SHA, immutable `commit:path` locator, base/head ref, label, or merge tree exists for this window;
- no linked issue or discussion exists to inspect for an in-window PR;
- protocol, runtime, API, package export/versioning, security-boundary, examples/docs/tests, and compatibility classifications are **not applicable**, rather than “unchanged by proof.”

## Evidence metadata and immutable locators

The window has no merged source-content snapshot to hash. The following are SHA-256 digests of exact GitHub API response snapshots captured during retrieval; they establish the query result and checkpoint, not a protocol source’s normative content.

| Evidence ID | Immutable revision / locator | Snapshot SHA-256 | Retrieved | Authority / evidence class / maturity | Uncertainty and refresh trigger |
|---|---|---|---|---|---|
| `GH-NAPS-REPO-20260728` | `GET https://api.github.com/repos/napplet/naps`; repo ID `1202279733`, default ref `master` | `49bf5669b825004902ce782e53baf9271819969470ba8f0de0b982175d9d955c` | `2026-07-28T09:31:48Z` | GitHub’s repository metadata for the named public repository; **upstream-hosted repository identity**, observed metadata; not protocol authority | Mutable service response. Refresh for a later source-review run, repository transfer/rename, or any candidate-identity decision. |
| `GH-NAPS-CLOSED-PRS-20260728` | `GET /repos/napplet/naps/pulls?state=closed&sort=updated&direction=desc&per_page=100`, fully Link-paginated; 59 records | `8ac19d279a8ccd9bc86c3ed952b79ba2c36a46937034268965d702a4c49965df` | `2026-07-28T09:32:15Z` | GitHub PR merge metadata; **observed implementation/workflow history**, complete for this endpoint retrieval; not normative protocol evidence | Captures current API history only. Refresh at the next rolling-window review or when a PR merge is reported. |
| `GH-NAPS-SEARCH-20260728` | `GET /search/issues?q=repo:napplet/naps+is:pr+is:merged+merged:2026-07-25..2026-07-28&per_page=100`; `total_count: 0` | `c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0` | `2026-07-28T09:31:48Z` | Corroborating GitHub search metadata; observed discovery evidence | Search uses day-level syntax and is not the sole completeness mechanism. Refresh with the main enumeration. |
| `GH-NAPS-DEFAULT-REF-20260728` | `GET /repos/napplet/naps/git/ref/heads/master` → `5ac0490461ca6fec2f0d2e45b4835cf9bc08de24` | `c0b0c7fb8120223f3acb76fbdd9f1f541895368a0d3fb119bfc6fb94d9ea808f` | `2026-07-28T09:31:48Z` | Git object ref observation; immutable commit identifier once captured, but mutable branch-ref endpoint | Refresh before using the head as a compatibility baseline. Ref observation does not establish content semantics. |
| `GH-NAPS-DEFAULT-COMMIT-20260728` | `GET /repos/napplet/naps/git/commits/5ac0490461ca6fec2f0d2e45b4835cf9bc08de24`; tree `c2db1eb8f9f6512ad51e001b1636cc71e8d2f0fb` | `e15fd31d35d6fea9e9ca2ebff7168e89fbd73d9f8fd344c4640e59c49ae474d5` | `2026-07-28T09:31:48Z` | Immutable Git commit/tree metadata; upstream repository implementation metadata, but outside this refresh window and not content-reviewed | A commit/tree hash alone is not a reviewed protocol source. Fetch exact paths/blobs and obtain review before any claim. |
| `GH-NAPS-MASTER-WINDOW-COMMITS-20260728` | `GET /repos/napplet/naps/commits?sha=master&since=2026-07-25T09:29:46Z&until=2026-07-28T09:29:46Z&per_page=100`; `[]` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `2026-07-28T09:32:15Z` | Default-branch activity corroboration; observed metadata | Does not cover non-default branches, releases, discussions, or external channels. Refresh with each window. |

**Affected requirements/phases:** The evidence is relevant to Phase 1 / source Phase 0 requirements `EVID-01`, `EVID-02`, `EVID-03`, `EVID-04`, `OPER-01`, and `OPER-03`. It supports neither a Phase 1 gate change nor a later-phase architecture/content assertion. It remains indirectly relevant to all later phases that consume accepted Phase 1 evidence.

## Fact / proposal / behavior / inference separation

| Classification | Finding |
|---|---|
| Upstream fact (GitHub metadata) | The verified public repository is `napplet/naps`; `master` was its default branch at retrieval; the fully enumerated closed-PR response contains no merge timestamp in the requested window. |
| PR proposal | None in scope; no in-window PR exists from which to extract intent. |
| Merged implementation behavior | None in scope; no in-window merged diff or changed file was inspected. |
| Project policy | Preserve identity, do not auto-rewrite claims/ADRs/approvals, and require immutable source + review before teaching protocol behavior. |
| Inference | No in-window GitHub PR merge was found. It is unsafe to infer protocol stability, lack of direct pushes, absence of release/package changes, or normative authority from that absence. |

## Comparison with active Learn Napplets research

No active artifact was modified. The absence of a merged PR in this window produces **no content-level refresh** for an existing source record, because the active registry still has no immutable upstream `napplet/naps` source record. It instead confirms that the existing baseline remains blocked and that source acquisition/review is still required independently of this rolling-window result.

### Exact records and refresh disposition

| Artifact / ID | Current active state | In-window effect and required disposition |
|---|---|---|
| `OWS-001`, `OW-NAP-001` — [`open-work-snapshot.json`](../open-work-snapshot.json#L2-L46) | Blocked; `OW-NAP-001` points to `CAND-NAP-REGISTRY`, with `immutableReference: null` and `retrievalOutcome: unavailable`. | **No PR-triggered refresh.** Retain blocked. A confirmed official repository/path/ref must still start bounded source acquisition. |
| `CAND-NAP-REGISTRY`, `CAND-NAP-PROJECTION`, `CAND-NAP-GOVERNANCE`; also `CAND-NAPPLET-WEB-REPOSITORY`, `CAND-NAPPLET-WEB-PACKAGE`, `CAND-RUNTIME-IMPLEMENTATION` — [`candidate-source-manifest.yaml`](../candidate-source-manifest.yaml#L2-L99) | All blocked candidates; refresh trigger is confirmed official repository/path/ref. | **No candidate is promoted or refreshed by this zero-PR result.** The verified repository identity may be a discovery lead for `CAND-NAP-*`, but it is not an approved identity/path/authority determination. |
| `SRC-POLICY-001`, `SRC-POLICY-002` — [`source-registry.yaml`](../source-registry.yaml#L2-L60) | Local immutable planning/project-policy records only; explicitly not upstream protocol/package proof. | **No refresh.** Do not convert GitHub metadata into a source-registry protocol record without an approved immutable `revision:path` or blob source capture. |
| `ACQ-FAIL-001` — [`acquisition-log.yaml`](../acquisition-log.yaml#L10-L21) | Upstream protocol/registry/package/runtime acquisition blocked by missing official identity, commit, locator, digest, and authenticity review. | **Still open.** This report supplies repository discovery metadata only; it does not satisfy the failure’s missing evidence. |
| `CLM-UPSTREAM-BASELINE-001` — [`claims.yaml`](../claims.yaml#L29-L65) | No current NAP/NIP conclusion or first-lab recommendation without official immutable source + review. | **No claim refresh.** Preserve safe fallback: no asserted protocol behavior. |
| `CMP-BASELINE-001`, `CLM-CMP-PACKAGE-001`, `CLM-CMP-RUNTIME-001`, `CLM-CMP-EXAMPLE-001`, `CLM-CMP-FIXTURE-001` — [`compatibility-matrix.yaml`](../compatibility-matrix.yaml#L2-L50) | Blocked; release/current-work slots contain planning-policy inputs, not upstream evidence. | **No matrix row refresh.** A future immutable source/release/current-work comparison needs human review; this no-merge result is not compatibility evidence. |
| `DRF-DISCOVERY-001`, `DRF-METADATA-001`, `DRF-INTENT-001` — [`drift-register.yaml`](../drift-register.yaml#L142, #L595, #L467) | NAP/discovery/metadata/intent drift remains blocked. | **No drift state change.** Preserve all as blocked; do not label fresh. |
| `DRF-HANDSHAKE-001`, `DRF-MANIFEST-001`, `DRF-IDENTITY-001`, `DRF-EGRESS-001` — [`drift-register.yaml`](../drift-register.yaml#L339, #L529, #L401, #L203) | Bootstrap/host drift remains blocked. | **No refresh.** No in-window implementation evidence can resolve these. |
| `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`, `DRF-UNKNOWN-MESSAGES-001` — [`drift-register.yaml`](../drift-register.yaml#L3, #L75, #L656) | Runtime/package drift remains blocked. | **No refresh.** The report does not establish package release, exports, runtime behavior, or conformance. |
| `OQ-UPSTREAM-BASELINE-001` — [`open-questions.yaml`](../open-questions.yaml#L154-L207) | Requires identity, commit, locator, digest, retrieval metadata, release-vs-current comparison, drift, and review. | **Still open.** This report resolves only a narrow GitHub PR-window query, not the required evidence package. |
| `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`, `OQ-EGRESS-NIP-001` — [`open-questions.yaml`](../open-questions.yaml#L114-L153, #L77-L113, #L3-L39) | Public package, conformance, and egress questions unresolved. | **No refresh.** Retain as open; no installation, export, runtime, or egress claim is supported. |
| `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, `OQ-VERIFIED-LOADER-VERIFIER-001` — [`open-questions.yaml`](../open-questions.yaml#L208-L313) | Blocked pending upstream evidence. | **No refresh.** No source content was collected. |

### Catalogs and lesson packets

| Item | Required status after this refresh |
|---|---|
| `ARC-CANDIDATE-001` — [`archetype-convention-catalog.yaml`](../archetype-convention-catalog.yaml#L4-L28) | Remains blocked; do not select archetype, convention, composition behavior, or capability mapping. |
| `DOM-CANDIDATE-001` — [`domain-catalog.yaml`](../domain-catalog.yaml#L4-L28) | Remains blocked; do not select a real domain, teaching-host profile, or first lab. |
| `EXAMPLE-CANDIDATE-001` — [`example-napplet-catalog.yaml`](../example-napplet-catalog.yaml#L4-L39) | Remains blocked; no executable/adaptable/conformant v1 example is established. |
| `napplet/web` package map — [`package-map.md`](../package-map.md#L3-L47) | Retain **avoid as dependency**. No version, integrity, root export, implementation revision, browser claim, or install instruction was established. |
| `LES-009` — [`09-designing-a-good-napplet.md`](../lesson-packets/09-designing-a-good-napplet.md#L24-L66) | Keep manifest/identity/metadata/intent conceptual only. |
| `LES-010` — [`10-anatomy-of-a-napplet.md`](../lesson-packets/10-anatomy-of-a-napplet.md#L22-L79) | Do not teach package layout/import/version/root export as settled. |
| `LES-011` — [`11-build-test-and-publish.md`](../lesson-packets/11-build-test-and-publish.md#L22-L79) | Do not add a current package/build/test/publish tutorial. |
| `LES-012` — [`12-inside-a-runtime.md`](../lesson-packets/12-inside-a-runtime.md#L23-L79) | Keep runtime dimensions a research checklist, not a selected architecture. |
| `LES-013` — [`13-evolving-the-protocol.md`](../lesson-packets/13-evolving-the-protocol.md#L23-L65) | Preserve the rule that PR/issue/discussion signals route research; they do not establish protocol fact. |

### ADR and spike impact

| Item | Required status after this refresh |
|---|---|
| `ADR-0011` — [`0011-source-freshness.md`](../../adr/0011-source-freshness.md#L19-L29) | Remains proposed. The result follows its intended direction: identity-pinned review, preserve old identity, and no automatic mutation of claims/ADRs/approvals. |
| `ADR-0010` — [`0010-package-versioning.md`](../../adr/0010-package-versioning.md#L17-L25) | Remains proposed and blocked: release/version, integrity, provenance, license, root export, implementation baseline, compatibility, and review remain absent. |
| `ADR-0001`–`ADR-0005`, `ADR-0008` — [`adr-handoff.yaml`](../adr-handoff.yaml#L10-L98), [`0005-teaching-host.md`](../../adr/0005-teaching-host.md#L17-L33), [`0008-protocol-fixture-strategy.md`](../../adr/0008-protocol-fixture-strategy.md#L17-L27) | No update or acceptance basis. The zero-PR result does not resolve discovery/workspace, framework, publication, content, host, loader, manifest, identity, or verifier questions. |
| `SPK-G-PACKAGE-CONFORMANCE` — [`metadata.yaml`](../../spikes/spk-g-package-conformance/metadata.yaml#L5-L12) | Remains blocked; zero package installs/imports/conformance runs remain valid blocker evidence only. |
| `SPK-D-VERIFIED-LOADER` — [`metadata.yaml`](../../spikes/spk-d-verified-loader/metadata.yaml#L129-L163) | Remains local digest/mutation evidence only; it does not establish verifier behavior. |
| `SPK-C` and `SPK-H` — [`spk-c metadata`](../../spikes/spk-c-boundary-harness/metadata.yaml#L182-L189), [`spk-h metadata`](../../spikes/spk-h-browser-egress/metadata.yaml#L180-L187) | Retain fixture-specific Chromium observations and Firefox limitation; no upstream/cross-browser conclusion is added. |
| `SPK-L-SOURCE-FRESHNESS` — [`metadata.yaml`](../../spikes/spk-l-source-freshness/metadata.yaml#L2-L35) | Remains a deterministic local review-routing fixture, not live upstream volatility evidence. |

## Refresh work created or avoided

### No automatic updates

The following actions are intentionally **not** taken from this report: no source-record creation, claim rewrite, drift-status change, matrix update, lesson instruction change, package admission, ADR acceptance, spike conclusion update, or Phase 1 gate change.

### Manual follow-up candidates

1. **Identity/authenticity review:** Determine whether the verified GitHub repository is an official authority for each `CAND-NAP-*` purpose rather than assuming ownership from its name.
2. **Immutable content acquisition:** If authorized and identity-confirmed, capture exact official `commit:path` or Git blob locators; record exact bytes/digests, retrieval dates, authority/evidence/maturity, and release-versus-current separation.
3. **Targeted comparison:** Route any content change to the relevant `DRF-*`, `CMP-BASELINE-001`, and `OQ-*` records; retain prior evidence identities and request human review.
4. **Future rolling review:** Re-run the fully paginated timestamp filter for the next requested window and separately examine releases, package registries, direct default-branch commits, issues/discussions, and official specification sources only when scoped and authorized.

## Uncertainty and conclusion

This refresh establishes a bounded, reproducible observation: no merged GitHub PR in `napplet/naps` has a `merged_at` timestamp inside the requested interval. It does not prove absence of unmerged work, direct pushes outside the queried history, releases, non-default branches, package publication, changed documentation, off-GitHub discussion, or protocol evolution.

Most importantly, a merged implementation—even if one had appeared—would be observed repository behavior or a PR proposal, not automatically normative protocol authority. Current Learn Napplets records correctly remain blocked pending official immutable source material and human review.
