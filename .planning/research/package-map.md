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

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical and content-learning human review. Any package installation remains a spike-local human checkpoint.
