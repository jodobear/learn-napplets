# Research Schema Migration Notes

## Drift register v1 to v2

Schema: `drift.schema.json`
Version: 1 -> 2
Deterministic migration: `tools/phase1-python tools/migrate-phase1-records.py migrate-drift --input .planning/research/schemas/fixtures/drift-v1-legacy.yaml --output .planning/research/schemas/fixtures/drift-v2-current.yaml`
Fixtures: `fixtures/drift-v1-legacy.yaml` SHA-256 `bee238e63387f59573fc364843d01a56a3332607cbceca155b83e6be24577f85` -> `fixtures/drift-v2-current.yaml` SHA-256 `579ae805203993c39cea51915dee1b59d2b972d7547ec49e6889551dbd7faec2`
Change notes: Version 2 preserves every drift, source, claim, observation, impact, and history identifier while canonicalizing stable-ID records, scalar impact lists, and chronological history entries. It introduces mutually exclusive parallel upstream-side and observed-local alternatives, so a local measurement cannot be represented as an upstream normative side.
Compatibility: The retained `legacy/drift.schema.v1.json` and immutable v1 fixture remain audit inputs only. Ordinary research validation accepts the current v2 document after migration; migration is idempotent for v2 documents.
Rollback: Restore the v1 schema and register from the retained v1 fixture only as a documented contract rollback; do not remove either immutable fixture or rewrite stable IDs. Re-run the deterministic migration to return to v2.

## Compatibility matrix v1 to v2

Schema: `compatibility.schema.json`
Version: 1 -> 2
Deterministic migration: `tools/phase1-python tools/migrate-phase1-records.py migrate-compatibility --input .planning/research/schemas/fixtures/compatibility-v1-legacy.yaml --output .planning/research/schemas/fixtures/compatibility-v2-current.yaml`
Fixtures: `fixtures/compatibility-v1-legacy.yaml` SHA-256 `94ee3eb480cc616a998411ab3f01ad3f8fb99d779ad723ef3c301406ca348f0a` -> `fixtures/compatibility-v2-current.yaml` SHA-256 `aaf1de4cfc1c7d15fb161ac8fff1bf99626bc929713c89d9578c774e4dafceb2`
Change notes: Version 2 preserves every CMP/SRC/CLM/DRF/OQ reference and historical observation while adding exactly seven closed dimension records: `normativeProtocol`, `observedImplementation`, `publishedPackage`, `runtime`, `exampleFixture`, `currentWork`, and `conformance`. Each has a stable candidate reference, locator/digest relationship, evidence-class expectation, authority expectation, blocked/not-reviewed status, and explicit missing reason. Migration does not resolve evidence, judge authority, decide eligibility, grant a review, or accept an ADR.
Compatibility: The retained `legacy/compatibility.schema.v1.json` and immutable v1 fixture are audit inputs only. Ordinary research validation accepts only schema version 2 after migration; migration is deterministic and idempotent for a correctly closed v2 document.
Rollback: Restore the v1 schema and compatibility register only as a documented contract rollback from the retained immutable v1 fixture; do not remove legacy/current fixtures or rewrite stable IDs and historical observations. Re-run the deterministic migration to return to v2.

## Other schema inventory

| Schema | Version | Migration |
| --- | --- | --- |
| `spike.schema.json` | 1 | Baseline — no predecessor |
| `environment.schema.json` | 1 | Baseline — no predecessor |
| `phase-governance.schema.json` | 1 | Baseline — no predecessor |
| `spike-impact-fragment.schema.json` | 1 | Baseline — no predecessor |
