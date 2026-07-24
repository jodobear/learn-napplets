# SPK-G — Public package and conformance consumption report

SPK ID: SPK-G-PACKAGE-CONFORMANCE

Metadata path: metadata.yaml

## Research question

Can a cataloged released public package export be consumed in an isolated fixture against recorded public release and implemented-source baselines without importing private upstream internals?

## Sources and immutable revisions

- **Upstream fact:** none is established. The catalog contains no official released `napplet/web` package/version, documented public export, release integrity, or distinct implemented public-export source baseline.
- **Blocked package claim:** `CLM-CMP-PACKAGE-001` binds the absence to `SRC-POLICY-001`, commit `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, path `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`, locator `Source and claim record model`, SHA-256 `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`, and `SRC-POLICY-002`, commit `b534103068be8c07e6869bfb7290fb60fdd87c8c`, path `.planning/governance/evidence-policy.md`, locator `Required fields and verification rule`, SHA-256 `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`. Both were retrieved `2026-07-24T00:00:00Z`.
- **Authority boundary:** these are planning-archive/project-policy and project-policy records. They preserve missing evidence; neither is official package provenance or protocol authority.
- **Local evidence:** `fixture.md` SHA-256 `2481ad99caed14b4e72af36ec87cf19f0ca62aa7e2e7498016582917d192172b`; `environment.json` SHA-256 `381e7c5c192eeac3cf23eefc3b669c6d2c3710b0ec3d0cb1bdecd68727726f1f`; `measurements.yaml` SHA-256 `aba6aa72bfcdf68498c90108314e2464a0e195086412bb090e91917255fed59b`; `source-registry.yaml` SHA-256 `59a3146c13939aa900f92cabb5156faf6b2d8612d711a57a35495e9a7d5cacc5`.

## Observations

**Observed implementation behavior:** five dependency-free local gate replays exited `0`. All found `CAND-NAPPLET-WEB-PACKAGE` blocked by the dated human decision, an unavailable exact version, no authorized install command, and no `.experiment/` directory.

Every replay observed zero qualifying releases, install attempts, public-export imports, conformance targets, and forbidden private/deep imports. No registry, package manager, browser, package code, secret, external state, or network target was used.

## Conflicts

The preserved materials name `napplet/web` only as a discovery pointer, while the catalog has no immutable released-package or public-export implementation side to compare. This does not resolve a package conflict. `DRF-ARTIFACT-001` and `DRF-CONFORMANCE-001` remain blocked.

## Inference

**Inference:** the repeatable gate proves only that the recorded catalog state and human decision disallow package execution. It cannot establish package availability, protocol behavior, browser behavior, imports, compilation, or conformance. Zero install attempts are supply-chain compliance, not compatibility success.

## Prototype or measurement

No external package, consumer implementation, production scaffold, or conformance target was created. Five replays inspected the blocked metadata through `tools/phase1-python`; the structural contract validator also passed.

```text
tools/phase1-python -c spk-g-blocked-package-gate
tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-g-package-conformance --contract
```

The declared not-run error is `SPK-G-BLOCKED-NO-PUBLIC-RELEASE-BASELINE`, not an error emitted by an installed library.

## Recommendation

**Project recommendation, not an accepted ADR:** preserve `CAND-NAPPLET-WEB-PACKAGE` as blocked. Install nothing, substitute no package, and do not use private, workspace, deep, `src/`, `dist/`, or monorepo paths. Collect exact official release/version, package-root export, provenance, license, integrity, browser claim, and distinct immutable release and implementation source baselines before another human review.

## Uncertainty

Material uncertainty remains for package identity, version, public exports, licensing, registry integrity, source revision, browser support, release/current-work divergence, and public conformance. Policy records make the absence auditable but cannot answer package questions.

## Affected phases and requirements

- **EVID-03 / EVID-04 / Phase 01:** SPK-G supplies replayable dependency-free blocked evidence tied to `CLM-CMP-PACKAGE-001`.
- **`CMP-BASELINE-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`:** remain blocked; no compatibility or release artifact result was produced.
- **ADR-0005, ADR-0008, ADR-0010:** receive proposed blocked input only.
- **Phase 02:** must retain a static/deferred path and must not add a napplet package dependency from this record.

## Owner and required approval

Owner: research owner. The 2026-07-24 Task 2 human checkpoint blocked `CAND-NAPPLET-WEB-PACKAGE` and authorizes no package operation. A retry needs complete public evidence plus dated human protocol-technical, security/supply-chain, content-learning, accessibility, and product review as applicable. This report records local evidence only; it does not approve a claim, accept an ADR, or authorize production scaffolding.
