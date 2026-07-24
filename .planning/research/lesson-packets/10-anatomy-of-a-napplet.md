# Lesson Research Packet — Anatomy of a Napplet

- **Lesson ID:** LES-010
- **Primary audience:** General web/application developers and developers preparing to assess a future napplet build surface.
- **Prerequisites:** LES-007 and LES-009; understand that identity, distribution, and focused-design terms are evidence-limited.
- **Last researched:** 2026-07-24

## Learner question

Which build-surface questions can be inspected now without presenting a package layout, manifest, export, or verifier as a current napplet requirement?

## Intended outcome

Learners can distinguish an annotated, evidence-led project explorer from a real napplet source tree, identify the separate public-package and identity evidence that a build lesson would require, and retain a deterministic static fallback until those sources are reviewed.

## Current terminology

- **Anatomy of a napplet** is a lesson-research label, not a verified project-layout specification.
- **Public package**, **root export**, **manifest**, **identity**, and **verifier** name separate research surfaces; this packet does not define their fields, file names, or loading semantics.
- **Annotated project explorer** is a proposed static instrument that can show evidence gaps without containing an importable project or package command.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-CMP-PACKAGE-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, package compatibility evidence | **state: blocked**; no immutable public release or export baseline is available. |

## Implementation and runtime evidence

`CMP-BASELINE-001` is a **blocked** compatibility record, not a package, implementation, browser-support, or import result. No released `napplet/web` version, integrity value, documented root export, public implementation revision, or verified build command has been collected. `SPK-G-IMPACT-001` remains a materially uncertain local no-candidate outcome; it does not authorize an install, a private-monorepo path, or a source-tree diagram as public-package evidence.

## Drift and open questions

- `DRF-ARTIFACT-001` remains **blocked**: a build output cannot be equated with an exact released artifact.
- `DRF-CONFORMANCE-001` remains **blocked**: no public fixture or conformance target supports a layout or validator claim.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` and `OQ-PUBLIC-CONFORMANCE-001` route the separate release/export/provenance and conformance acquisition work.

## Misconceptions to address

- A plausible `src/` tree, manifest file, or import statement is not evidence of a real napplet format.
- A private source path, local build, or digest does not prove a public package, root export, or release artifact.
- A local fixture observation does not establish verifier, identity, manifest, or browser behavior.

## Story representation

**Conceptual simulation:** A learner opens an artifact-evidence card and asks which evidence would justify showing source, build, package, identity, and verifier details. Each proposed detail stays labelled `not collected` or `blocked`; no code is built, installed, imported, or executed.

## System representation

**Conceptual simulation:** `proposed source surface → public release/export evidence question → identity/manifest evidence question → conformance evidence question`. The arrows represent research dependencies, not a selected build pipeline, resolver, or runtime.

## Wire representation

No manifest, identity tuple, artifact descriptor, or verifier envelope is validated. The static equivalent is an evidence-link table naming the blocked records, not pseudo-fields that resemble a package schema.

## Code representation

No package command, build configuration, source tree, verifier, resolver, or runtime import belongs in this packet. A data-only card may show `candidate surface`, `evidence needed`, and `safe static fallback`; it must not contain a package name presented as installable, a public URL, a secret, a key, or executable build instructions.

## Candidate instrument

- **Conceptual simulation:** Annotated Project Explorer with deterministic local evidence cards and a static table.
- **Provenance:** conceptual simulation; neither a real napplet project, package, verified loader, nor observed implementation.
- **Safety boundary:** no package install, build, import, manifest resolution, verifier execution, public publication, credentials, browser run, or external service.

## Required fixtures and tests

- Derive future explorer cards and the static table from common structured source/status records so human and machine outputs expose the same IDs and states.
- Provide keyboard traversal, reduced-motion equivalence, state inspection, reset/replay, and a static equivalent for every later explorer interaction.
- Test that any future project-layout detail remains labelled illustrative until public package, identity, manifest, verifier, and conformance evidence is complete and reviewed.

## Do not teach as settled

- `CLM-CMP-PACKAGE-001` — **state: blocked**. **Reason:** the public package candidate remains an unpinned discovery pointer with no immutable release or export record. **Impact:** do not teach a package layout, import, version, root export, or browser-support claim.
- `CMP-BASELINE-001` — **state: blocked**. **Reason:** the compatibility baseline has only project-policy source records and no qualified public package/runtime/example/fixture inputs. **Impact:** do not select a build surface or represent compatibility as successful.
- `DRF-ARTIFACT-001` — **state: blocked**. **Reason:** no public package release or exact build-output evidence is pinned. **Impact:** no local build or artifact anatomy can become a release rule.
- `DRF-CONFORMANCE-001` — **state: blocked**. **Reason:** no public conformance fixture or immutable package/runtime observation exists. **Impact:** no validator, test command, or conformance repair path may be taught as current.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` — **state: blocked**. **Reason:** exact public release, provenance, integrity, root export, and independent implementation records are uncollected. **Impact:** retain a static evidence explorer rather than a real package exercise.
- `OQ-PUBLIC-CONFORMANCE-001` — **state: blocked**. **Reason:** a public conformance target and immutable baseline are unknown. **Impact:** do not infer conformance from a private path, compile result, or unpublished build.

## Follow-up research

- `CLM-CMP-PACKAGE-001` — **state: blocked**. **Reason:** the public package candidate remains an unpinned discovery pointer with no immutable release or export record. **Impact:** collect separately pinned release and repository/public-export sources before selecting package content.
- `CMP-BASELINE-001` — **state: blocked**. **Reason:** the compatibility baseline has only project-policy source records and no qualified public package/runtime/example/fixture inputs. **Impact:** keep the static explorer until a reviewed compatibility comparison can support a teaching path.
- `DRF-ARTIFACT-001` — **state: blocked**. **Reason:** no public package release or exact build-output evidence is pinned. **Impact:** compare released artifacts and source/build outputs without overwriting the blocked record.
- `DRF-CONFORMANCE-001` — **state: blocked**. **Reason:** no public conformance fixture or immutable package/runtime observation exists. **Impact:** acquire a public target before proposing a conformance lab or repair exercise.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` — **state: blocked**. **Reason:** exact public release, provenance, integrity, root export, and independent implementation records are uncollected. **Impact:** route package acquisition and review through this dated question before any install or import.
- `OQ-PUBLIC-CONFORMANCE-001` — **state: blocked**. **Reason:** a public conformance target and immutable baseline are unknown. **Impact:** route conformance research separately; do not promote a local example into a public result.
