# Research Schema Migration Notes

## Contract status

All current research schemas are **schema version 1**. Version 1 is the baseline and has no predecessor migration. A schema's version is its `schemaVersion` constant, and a change that alters a valid record's interpretation is breaking.

## Breaking-change procedure

Before a breaking schema version is accepted, add a dated migration entry that includes all of the following:

1. the affected schema filename and old/new version;
2. the record fields whose meaning changed;
3. a deterministic migration command or checked-in migration script reference;
4. before/after fixture paths and expected SHA-256 outputs;
5. compatibility and rollback notes; and
6. a concise change note explaining why the break is necessary.

The common validator rejects a migration record that omits the version change, deterministic command/reference, digest-backed fixture, or change note. Migration automation may transform records, but it cannot grant human approval or change a proposed ADR to accepted.

## Version 1 inventory

| Schema | Version | Migration |
| --- | --- | --- |
| `spike.schema.json` | 1 | Baseline — no predecessor |
| `environment.schema.json` | 1 | Baseline — no predecessor |
| `phase-governance.schema.json` | 1 | Baseline — no predecessor |
| `spike-impact-fragment.schema.json` | 1 | Baseline — no predecessor |

## Entry template

```text
Schema: <filename>
Version: <old> -> <new>
Deterministic migration: <tools/phase1-python command or checked-in script>
Fixtures: <before path sha256> -> <after path sha256>
Change notes: <meaning and compatibility impact>
Rollback: <safe reversal or restore procedure>
```
