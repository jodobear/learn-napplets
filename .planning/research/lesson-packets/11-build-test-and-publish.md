# Lesson Research Packet — Build, Test, and Publish

- **Lesson ID:** LES-011
- **Primary audience:** Developers considering future napplet build, test, release, or publication work.
- **Prerequisites:** LES-007 and LES-010; understand that an artifact, public package, and conformance target require distinct evidence.
- **Last researched:** 2026-07-24

## Learner question

How can source become a verified runnable artifact without confusing a local build, deterministic fixture, or archive suggestion with a current public build, test, or publication workflow?

## Intended outcome

Learners can separate illustrative commands from tested commands, distinguish local fixture integrity from public artifact provenance, and identify why publication and external deployment remain deferred rather than a required lesson exercise.

## Current terminology

- **Build**, **test**, and **publish** are topic labels; no current command surface is verified for a napplet package.
- **Verified runnable artifact** requires public release, integrity, export, implementation, compatibility, and review evidence; no such artifact is available here.
- **Dry-run publication** is a future bounded teaching possibility, not authorization to publish, deploy, access an account, or use credentials.

## Candidate claims

| Claim ID | Evidence class | Maturity | Source/section | Confidence |
| --- | --- | --- | --- | --- |
| `CLM-CMP-PACKAGE-001` | project-policy | unknown | `SRC-POLICY-001` / `SRC-POLICY-002`, package compatibility evidence | **state: blocked**; no public package surface supports a command tutorial. |

## Implementation and runtime evidence

No package was installed, imported, built, tested, or published for this lesson. `CMP-BASELINE-001` is **blocked** and `SPK-G-IMPACT-001` is a materially uncertain no-candidate result, so neither can establish a package command or conformance outcome. `SPK-K` selected local-only static inspection and rollback evidence; its outcome is not external deployment, publication, account access, or a public release workflow.

## Drift and open questions

- `DRF-ARTIFACT-001` retains the difference between a build output and a public artifact.
- `DRF-CONFORMANCE-001` retains the missing public conformance fixture and target.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` and `OQ-PUBLIC-CONFORMANCE-001` separate the required public-source and public-target research before any tutorial is promoted.

## Misconceptions to address

- A build that succeeds locally is not automatically a verified public artifact.
- A digest check on a supplied fixture is not a package integrity or provenance result.
- A documented command is illustrative until it executes against a reviewed, immutable, public surface; it is not an invitation to deploy or publish.

## Story representation

**Conceptual simulation:** A learner routes a fictional source card through `command evidence needed`, `artifact evidence needed`, `conformance evidence needed`, and `external action deferred`. The transcript has no command execution, package manager, listener, account, credential, network target, or publication action.

## System representation

**Conceptual simulation:** `illustrative source → blocked public artifact evidence → blocked conformance evidence → external publication deferred`. This is a research dependency map, not a CI pipeline, package registry workflow, or deployment architecture.

## Wire representation

No public manifest, artifact metadata, release descriptor, publication request, or conformance response is validated. Use an inspectable status table rather than a plausible release payload or registry API example.

## Code representation

No executable build, test, publish, deployment, package-manager, registry, or credential command is appropriate. If a later lesson displays a command, it must label it `illustrative` until a reviewed public source and CI-compatible deterministic replay prove it; this packet provides no such command.

## Candidate instrument

- **Conceptual simulation:** Build Evidence Workbench with deterministic status cards and a static dry-run explanation.
- **Provenance:** conceptual simulation; neither a build system, package test runner, registry client, deployment action, nor publication result.
- **Safety boundary:** no package install, arbitrary command execution, listener, external target, account, credential, release, public deployment, or publication.

## Required fixtures and tests

- Derive command-status cards and static explanations from common structured evidence records rather than command literals or visual-only state.
- Provide keyboard operation, reduced-motion equivalence, state inspection, reset/replay, and a static table for every later workbench interaction.
- Test that an illustrative command, local fixture digest, local rollback, and external publication boundary retain distinct labels and cannot be represented as a public release result.

## Do not teach as settled

- `CLM-CMP-PACKAGE-001` — **state: blocked**. **Reason:** no immutable public release or export baseline is available. **Impact:** no package install, build, test, or publication command may be taught as current.
- `CMP-BASELINE-001` — **state: blocked**. **Reason:** public package, runtime, example, and fixture compatibility inputs are absent. **Impact:** do not claim that a runnable artifact is compatible, verified, or publicly consumable.
- `DRF-ARTIFACT-001` — **state: blocked**. **Reason:** exact artifact versus build-output evidence is missing. **Impact:** a local compilation or digest cannot become a release or provenance conclusion.
- `DRF-CONFORMANCE-001` — **state: blocked**. **Reason:** no public conformance fixture or immutable package/runtime observation is collected. **Impact:** do not teach a validator, repair loop, or test suite as a current conformance workflow.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` — **state: blocked**. **Reason:** release, provenance, integrity, root-export, and implementation evidence is incomplete. **Impact:** external package actions remain deferred.
- `OQ-PUBLIC-CONFORMANCE-001` — **state: blocked**. **Reason:** the public target and immutable baseline are unknown. **Impact:** local fixtures and builds cannot supply a conformance claim.

## Follow-up research

- `CLM-CMP-PACKAGE-001` — **state: blocked**. **Reason:** no immutable public release or export baseline is available. **Impact:** refresh the package evidence before drafting a real tutorial.
- `CMP-BASELINE-001` — **state: blocked**. **Reason:** public package, runtime, example, and fixture compatibility inputs are absent. **Impact:** retain the static workbench until a reviewed compatibility row exists.
- `DRF-ARTIFACT-001` — **state: blocked**. **Reason:** exact artifact versus build-output evidence is missing. **Impact:** collect separately pinned artifact and build data without treating either as the other.
- `DRF-CONFORMANCE-001` — **state: blocked**. **Reason:** no public conformance fixture or immutable package/runtime observation is collected. **Impact:** identify a public target before introducing a repair exercise.
- `OQ-PUBLIC-PACKAGE-BASELINE-001` — **state: blocked**. **Reason:** release, provenance, integrity, root-export, and implementation evidence is incomplete. **Impact:** resolve this dated question before any package command, release, or publication exercise.
- `OQ-PUBLIC-CONFORMANCE-001` — **state: blocked**. **Reason:** the public target and immutable baseline are unknown. **Impact:** resolve this separately before a command is presented as conformance work.
