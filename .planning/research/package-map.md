# Package Map

## Research question

What released public `napplet/web` package surface, public export, browser support, and implementation revision can later teaching work consume, wrap, or avoid?

## Sources and immutable revisions

- `SRC-POLICY-001` (`c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`, digest `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`) is a preserved planning-policy seed, not package proof.
- `SRC-POLICY-002` (`b534103068be8c07e6869bfb7290fb60fdd87c8c`, `.planning/governance/evidence-policy.md`, digest `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`) governs the blocked disposition.
- `CAND-NAPPLET-WEB-PACKAGE` and distinct `CAND-NAPPLET-WEB-REPOSITORY` are discovery pointers only. Neither has a released package version/integrity nor a repository/public-export `SRC-*` record.

## Observations

`CMP-BASELINE-001` and `CLM-CMP-PACKAGE-001` record this surface as blocked. Therefore the catalog has no exact package version, integrity, export locator, implemented-source revision, browser-support claim, or installation instruction. A private monorepo path is explicitly not package evidence.

## Conflicts

There is no immutable released-package side and no immutable repository/public-export side to compare. `DRF-ARTIFACT-001` and `DRF-CONFORMANCE-001` retain the unresolved artifact and public-conformance questions.

## Inference

No consume, wrap, or avoid conclusion is justified. The only safe present disposition is **avoid as an implementation dependency** while preserving the named public candidates for bounded acquisition.

## Prototype or measurement

None. No package was installed, imported, or executed; this is not a substitute for the package/conformance spike.

## Recommendation

Keep `napplet/web` blocked. Before any future consume/wrap/avoid recommendation, collect both: (1) a released-package `SRC-*` record with exact version or integrity and public export locator, and (2) a distinct repository/public-export `SRC-*` record with implemented source revision, browser evidence, known drift, and compatibility comparison. Do not plan a private-monorepo import.

## Uncertainty

Material. Package identity, exports, browser support, license, release/current-work divergence, and conformance status are all unknown.

## Affected phases and requirements

- Phase: `01`; later teaching-scope, package-consumption, and runtime work.
- Requirements: `EVID-03`, `EVID-04`.
- Compatibility: `CMP-BASELINE-001`.
- Claims/drift: `CLM-CMP-PACKAGE-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`.
- Open question: `OQ-UPSTREAM-BASELINE-001`.

## Package evidence history

The retained history below distinguishes collection mechanics, package/repository
identity, and package-admission evidence. Entries are listed in collection order;
the later live-or-blocker receipt does not replace the fixture receipt.

### Repository identity

- Candidate: `CAND-NAPPLET-WEB-REPOSITORY`.
- State: discovery pointer only. No immutable official repository identity,
  `revision:path` record, or documented public root export has been collected.
- Classification: repository identity is distinct from an observed release commit
  and from an independently retrieved registry artifact.

### Observed release commit

- State: unavailable. No release commit has been observed or is being inferred
  from PR data, a source head, fixture bytes, or a private monorepo path.
- Required future comparison: any released commit must remain distinct from the
  implemented-source head and record both immutable baselines before it informs
  compatibility or package admission.

### Independently retrieved registry artifact

- State: blocked. The two retained receipts do not contain a qualifying live
  artifact observation with version, tarball URL, SRI/integrity, exposed SHA-256,
  provenance or explicit absence, license, documented root exports, and
  released-commit versus source-head comparison.
- Repository release metadata remains `not-an-artifact-substitute`; fixture
  bytes are mechanism evidence only and do not become a published-package fact.

### Immutable collection receipts

| Collection order | Path | Attempt ID | Receipt SHA-256 | Transport / outcome | Classification |
| --- | --- | --- | --- | --- | --- |
| 1 | `reports/package-registry-fixture-receipt-20260728.yaml` | `REG-FIXTURE-20260728-001` | `4f35050e9ee18864aeec90f88053b27dc209b32301ee82d460755af16241fc80` | `fixture` / `fixture-mechanism-only` | `mechanism-only-not-published-package-fact` |
| 2 | `reports/package-registry-live-or-blocker-receipt-20260728.yaml` | `REG-BLOCKER-20260728-001` | `40ebd1c8f1e8b0bcde03f01e936affb815fe2ed375113cce2547020c9c286a26` | `live-or-blocker` / `impact-scoped-blocker` | `blocked-no-live-registry-observation` |

Both path/attempt/digest bindings are retained in `package-evidence.yaml`; neither
entry is a latest-wins pointer. The live-or-blocker receipt records that no live
observation was made and cannot alter fixture bytes or attribution.

### SPK-G admission routing

`CAND-NAPPLET-WEB-PACKAGE` remains **blocked** for SPK-G. Every eligibility item
(exact public release, registry artifact fields, provenance, license, documented
root export, distinct implemented-source baseline, compatibility comparison, and
separate package approval) must be complete before a zero-operation blocker can
be replaced. The blocked route affects `EVID-03`, `EVID-04`, `OPER-01`,
`ADR-0005`, `ADR-0008`, `ADR-0010`, `OQ-PUBLIC-PACKAGE-BASELINE-001`,
`OQ-PUBLIC-CONFORMANCE-001`, `DRF-ARTIFACT-001`, and `DRF-CONFORMANCE-001`.

Safe fallback: keep the deterministic static learning path dependency-free.
Refresh trigger: collect and review a qualifying official registry artifact with
all required fields, then obtain separate package-admission approval before
SPK-G work.

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical and content-learning human review. Any package installation remains a spike-local human checkpoint.
