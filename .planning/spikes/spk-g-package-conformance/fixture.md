# SPK-G disposable public-export consumer fixture

**Fixture status:** recovery-guarded blocked contract. No package is installed,
imported, compiled, or executed in the current evidence state.

## Current consumer declaration

| Field | Value |
| --- | --- |
| Selected package/version | none — no released public package version is cataloged |
| Public export locator | none — no documented package-root export is cataloged |
| Conformance target | none — no public conformance fixture is cataloged |
| Snapshot reader | Plan 01-42 `spk-g-package-evidence` fixed target registration |
| Current outcome | `SPK-G-BLOCKED-ELIGIBILITY` with operation count `0` |
| Safe fallback | dependency-free deterministic static learning path |

A reader refusal is `SPK-G-BLOCKED-CANONICAL-SNAPSHOT-REFUSED` and occurs before
canonical evidence parsing, sandbox argv construction, or a package operation.
A qualified candidate without verified OS sandbox controls is
`SPK-G-BLOCKED-SANDBOX-UNAVAILABLE` with operation count `0`.

## Future root-export fixture contract

A future fixture can run only after it records and passes all of these exact
values from the recovered snapshot:

1. package name and exact released version;
2. tarball integrity, official registry/project provenance, license, and
   documented package-root export equal to the package name;
3. distinct approved released-package and implementation `SRC-*` records plus
   their `CLM-*` relation;
4. runtime, example, local fixture, and public-conformance inputs;
5. a separately dated approved package decision; and
6. an audited OS sandbox contract with no network, a read-only repository, an
   isolated writable workspace, empty/minimal inherited environment, and resource
   limits.

The operation may exercise the documented package-root export only. It must reject
all deep subpaths, `dist/`, `src/`, internal implementation files, relative
upstream checkouts, workspace aliases, private packages, unpublished builds,
substitute packages, and browser execution.

Five retained outputs must classify a result as bounded observed implementation
behavior. A successful import or compile is never protocol authority,
architecture approval, or independent cross-runtime conformance. Firefox remains
blocked before Playwright attachment and the static fallback remains available.
