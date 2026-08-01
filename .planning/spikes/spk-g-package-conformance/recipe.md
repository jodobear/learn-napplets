# SPK-G — Public package and conformance consumption recipe

SPK-G is a disposable, **non-production** measurement boundary. The runner does
not install, import, compile, or execute any package unless one immutable,
registered canonical snapshot proves a complete public-artifact candidate, a
separately dated decision approves that exact candidate, and the OS sandbox
contract is verified before any package-manager argv exists.

## Current outcome: deterministic no-operation blocker

`CAND-NAPPLET-WEB-PACKAGE` has no exact released version, tarball integrity,
provenance, license, documented package-root export, distinct released and
implementation source baselines, runtime/example/fixture/conformance inputs, or
approved dated decision. `CMP-BASELINE-001` is blocked across all seven required
dimensions. The only valid current outcome is a receipt with
`SPK-G-BLOCKED-ELIGIBILITY` and operation count zero.

The receipt is based on the Plan 01-42 registered
`spk-g-package-evidence` reader. It returns a single complete old or new mapping,
or refuses before YAML parsing, sandbox argument construction, or any package
operation. The runner must not reopen a canonical file after that mapping is
acquired.

## Bounded future operation contract

A future operation is permissible only when all checks below pass in order:

1. The registered snapshot returns the exact complete target set.
2. Every compatibility dimension is `qualified`; baseline eligibility is
   `eligible`, approved, and has a review record.
3. The artifact records the exact package name/version, tarball integrity,
   registry/project provenance, license, documented package-root export, distinct
   approved and current released/implementation `SRC-*` records, and the required
   runtime, example, fixture, and conformance inputs.
4. A separate package decision is `approved` with a non-empty dated review value.
5. An OS-level rootless sandbox contract proves no network, read-only repository,
   isolated writable workspace, empty/minimal environment, and wall-clock, CPU,
   memory, process-count, and file-size limits.

Only then may a fixed `npm install --ignore-scripts --package-lock=false
<exact-name>@<exact-version>` argv be constructed inside the sandboxed workspace.
The fixture may import only the recorded package-root export. A package operation
is observed implementation behavior only: it cannot establish protocol authority,
architecture approval, cross-runtime conformance, or remove the existing Firefox
pre-attachment blocker.

## Prohibited surfaces and deterministic fallback

The runner rejects deep/package-file imports, `src/`, `dist/`, relative upstream
paths, workspace aliases, private packages, unpublished output, guessed names,
substitute packages, browser execution, registry access, and external writes.

If any required evidence, approval, recovery result, or sandbox control is absent,
the runner retains a specific `SPK-G-BLOCKED-*` receipt with operation count zero.
It preserves the dependency-free static learning path and the Firefox blocker.

## Replays

The following commands are deterministic local checks; current canonical evidence
causes neither command to invoke a package manager:

```bash
tools/phase1-python tools/measure-package-conformance.py --spike .planning/spikes/spk-g-package-conformance --check
tools/phase1-python tools/measure-package-conformance.py --spike .planning/spikes/spk-g-package-conformance --run-five
```

A five-run result is retained only after its complete receipt bundle validates.
Any failure removes candidate workspace material and leaves the prior measurements,
report, and impact fragment byte-identical.
