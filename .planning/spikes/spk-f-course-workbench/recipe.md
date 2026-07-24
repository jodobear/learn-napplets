# SPK-F — Guest-only Portable Workbench/Course Feasibility Recipe

SPK-F is a disposable, non-production experiment. It evaluates a portable
**guest-only simulation**, not a teaching host, production course artifact, or
current napplet runtime implementation.

## Candidate package gate

The only candidate packages are `astro@7.1.3` and `vitepress@1.6.4`, exactly as
recorded in `metadata.yaml`. Before any package command, a human reviewer must
record a dated **approved** or **blocked** decision for each exact version after
reviewing its official registry/project provenance, MIT license, release
integrity, source/hash decision, and isolated command.

No candidate is installed by this contract. An approval from another spike is
context only; SPK-F requires its own auditable Task 2 decision. If any candidate
is blocked or not approved, do not substitute a package. Run only dependency-free
contract evidence and record the portable conclusion as blocked.

## Fixture boundary

`fixture.md` supplies two representative lessons, an architecture diagram and
transcript, a code example, an assessment, source-status metadata, optional
progress, and optional external source/lab opening. Its simulated capabilities
are labeled and inspectable:

- **Capability present:** keep progress in the fixture's guest-memory model and
  render a source/lab-open request as a copyable, non-executing transcript.
- **Capability absent:** reset progress on replay and replace source/lab opening
  with a copyable citation and an explanation that no external request occurred.

The fixture imports no host code, holds no secret, performs no external write,
uses no direct browser storage/relay/service worker, and must not contain a
private child frame. It must never claim that an embedded visual is a real
runtime-composed sibling napplet. Any real sibling creation or focus would belong
to an external host after current-source verification and ADR approval.

## Measurements and decision boundary

After every exact candidate is approved, capture five runs for artifact shape and
size, startup, memory, keyboard/reduced-motion accessibility, lesson navigation,
Chromium and Firefox compatibility, optional-capability degradation, update and
identity implications, and build complexity. Record all samples, range, and
median in the eventual SPK-F measurement record with command and output digests.

The only proposed ADR-0007 vocabulary is `GO-V1`, `GO-LATER`,
`WORKBENCH-ONLY`, `NO-GO`, or a blocked-evidence result. SPK-F cannot accept ADR
0007, publish an artifact, write external state, establish upstream behavior, or
block public-site work.

## Isolation and replay

All dependencies, generated files, and browser work must remain below
`.planning/spikes/spk-f-course-workbench/.experiment/`, which is disposable and
ignored. After approval, run only the exact command attached to that candidate in
`metadata.yaml`; use `--ignore-scripts` and do not create a repository-root
`package.json`, lockfile, app, host, or production scaffold.

Run the fixture in both declared capability states five times through
`tools/phase1-python`, retain environment and digest evidence, then validate the
completed spike and overall planning boundary. Before approval, the only allowed
command is:

```text
tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-f-course-workbench --contract
```
