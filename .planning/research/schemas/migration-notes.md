# Research Schema Migration Notes

## Drift register v1 to v2

Schema: `drift.schema.json`
Version: 1 -> 2
Deterministic migration: `tools/phase1-python tools/migrate-phase1-records.py migrate-drift --input .planning/research/schemas/fixtures/drift-v1-legacy.yaml --output .planning/research/schemas/fixtures/drift-v2-current.yaml`
Fixtures: `fixtures/drift-v1-legacy.yaml` SHA-256 `bee238e63387f59573fc364843d01a56a3332607cbceca155b83e6be24577f85` -> `fixtures/drift-v2-current.yaml` SHA-256 `579ae805203993c39cea51915dee1b59d2b972d7547ec49e6889551dbd7faec2`
Change notes: Version 2 preserves every drift, source, claim, observation, impact, and history identifier while canonicalizing stable-ID records, scalar impact lists, and chronological history entries. It introduces mutually exclusive parallel upstream-side and observed-local alternatives, so a local measurement cannot be represented as an upstream normative side.
Compatibility: The retained `legacy/drift.schema.v1.json` and immutable v1 fixture remain audit inputs only. Ordinary research validation accepts the current v2 document after migration; migration is idempotent for v2 documents.
Rollback: Restore the v1 schema and register from the retained v1 fixture only as a documented contract rollback; do not remove either immutable fixture or rewrite stable IDs. Re-run the deterministic migration to return to v2.

## Other schema inventory

| Schema | Version | Migration |
| --- | --- | --- |
| `spike.schema.json` | 1 | Baseline — no predecessor |
| `environment.schema.json` | 1 | Baseline — no predecessor |
| `phase-governance.schema.json` | 1 | Baseline — no predecessor |
| `spike-impact-fragment.schema.json` | 1 | Baseline — no predecessor |
