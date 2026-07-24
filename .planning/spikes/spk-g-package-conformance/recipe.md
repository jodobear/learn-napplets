# SPK-G — Public package and conformance consumption recipe

SPK-G is a disposable, **non-production** research contract. It has no
qualified package operation at this time. It does not install a package,
contact a registry, or infer package behavior from an archive, a private
monorepo path, an unpublished workspace, or a guessed package name.

## Scope and question

Can a cataloged released public package export be consumed in an isolated
fixture against its recorded released-package and implemented-source baselines?

**Current answer: blocked.** `package-map.md` records only
`CAND-NAPPLET-WEB-PACKAGE` and `CAND-NAPPLET-WEB-REPOSITORY` as discovery
pointers. `CLM-CMP-PACKAGE-001` is blocked because no immutable public
`napplet/web` release or export baseline is available. `CMP-BASELINE-001`,
`DRF-ARTIFACT-001`, and `DRF-CONFORMANCE-001` retain the corresponding
compatibility and drift scope.

## Immutable blocking bindings

| Scope | Source / claim | Immutable locator | Classification | Result |
| --- | --- | --- | --- | --- |
| Package release/export eligibility | `SRC-POLICY-001` / `CLM-CMP-PACKAGE-001` | `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0:docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md` at `Source and claim record model`; SHA-256 `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb` | planning archive / project policy / accepted | blocked; archive is not package proof |
| Supply-chain and source gate | `SRC-POLICY-002` / `CLM-CMP-PACKAGE-001` | `b534103068be8c07e6869bfb7290fb60fdd87c8c:.planning/governance/evidence-policy.md` at `Required fields and verification rule`; SHA-256 `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2` | project policy / project policy / accepted | blocked; no qualifying release baseline |

Both source records are complete immutable policy records. Neither is an
immutable official released-package record or a distinct implemented
public-export source record; neither can qualify a package candidate.

## Candidate inventory and human gate

There are **zero installable candidates**. The sole catalog entry below is a
blocked discovery pointer retained for acquisition tracking, not a selected
package release.

| Catalog entry | Exact public package / version | Public export locator | Official registry / project provenance | License | Release integrity / source baseline | Browser support | Isolated install command | Conformance command | Eligibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CAND-NAPPLET-WEB-PACKAGE` | unavailable; no released version cataloged | unavailable; no documented public export cataloged | unavailable; no official registry or project release URL cataloged | unavailable | unavailable; no tarball integrity, released-package `SRC-*`, or implemented-source `SRC-*` cataloged | unknown | none — blocked, do not invoke a package manager | none — blocked, do not import or compile | blocked by `CLM-CMP-PACKAGE-001` |

The human approval field in `metadata.yaml` deliberately remains
`pending-human-review` with no reviewer or date. It does not authorize an
install. At Task 2, the reviewer must record an explicit block unless new,
fully cataloged evidence supplies every unavailable field; Task 2 must not
substitute a different package.

## Public-surface and fixture rules

- The consumer may use only a documented package-root public export recorded
  in the reviewed candidate row. It must never use a deep import, file path,
  `src/`, `packages/`, workspace alias, `dist/` file, relative upstream path,
  git checkout path, or private monorepo path.
- A candidate is eligible only if all of these are recorded before approval:
  exact package name and released version; documented root export locator;
  official registry and project/repository provenance; license; tarball
  integrity/hash source; browser support claim; distinct complete immutable
  released-package and implemented-source `SRC-*` records; and a valid `CLM-*`
  relation.
- A compile or import result is an **observed implementation behavior**, never
  upstream protocol authority. Bind it to the source baseline and preserve
  actual errors without treating a successful import as conformance.
- Dependencies, locks, logs, generated output, and any temporary fixture
  state belong only below
  `.planning/spikes/spk-g-package-conformance/.experiment/`, which remains
  disposable and ignored.

## Predeclared measurements and thresholds

| Measurement | Replay input and operation | Expected result | Success | Failure | Blocked threshold |
| --- | --- | --- | --- | --- | --- |
| qualified exact public releases | candidate inventory + `metadata.yaml` | `0` now | every selected row has every eligibility field and human approval | a qualified approved command returns a recorded import/compile/conformance error | `0` qualifying rows or any missing field; do not run an install |
| public exports exercised | reviewed fixture import declaration | `0` now | only documented package-root exports are exercised in five replays | an exercised public export mismatches the recorded baseline or command output | no recorded public export locator |
| import/compile/conformance results | exact approved isolated commands | no command / no output now | five replayable observations bound to source IDs and output digests | preserve exact error and use no substitute | no exact command may exist or run |
| forbidden import count | `fixture.md` import-policy inspection | `0` | zero deep/private/source/workspace imports | one forbidden path is attempted or declared | N/A; the contract remains blocked without imports |

## Deterministic local replay before approval

Run only the contract validator with the approved wrapper:

```bash
tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-g-package-conformance --contract
```

The expected result is a successful structural validation of a **blocked
candidate inventory**. It does not retrieve, install, import, compile, or test
any external package.

## Future operation shape — not an authorized command

No exact install or conformance command can be proposed while the required
package/version/export fields are unavailable. After a future evidence
collection and a Task 2 human approval, the record must name the exact
isolated command in this form, with every placeholder replaced by the reviewed
catalog value:

```text
npm --prefix .planning/spikes/spk-g-package-conformance/.experiment/<exact-package>-<exact-version> install --ignore-scripts --package-lock=false <exact-package>@<exact-version>
node <approved-local-fixture-using-only-the-documented-root-export>
```

This is an operation shape, not a command to run. It must not be completed
with a guessed name, version, export, registry URL, or a private/deep import.

## Dispositions and impacts

- **Current disposition:** blocked; there is no consume, wrap, or avoid result
  based on an implementation experiment.
- **Compatibility:** retain `CMP-BASELINE-001` as blocked.
- **Drift:** retain `DRF-ARTIFACT-001` and `DRF-CONFORMANCE-001` as blocked.
- **ADR impacts:** retain proposed blocked input for `ADR-0005`, `ADR-0008`,
  and `ADR-0010`; no ADR is accepted or selected by this spike.
- **Fallback:** do not add an upstream dependency. Preserve the static,
  deterministic research path until a public immutable release/export baseline
  is collected and approved.

## Safety boundary

No secrets, private sources, registry write, external mutation, production
scaffold, package install, browser execution, or live probe is permitted by
this task. Plan 01-28 alone may validate and consolidate later SPK-G impact
records.
