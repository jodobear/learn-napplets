---
phase: 01-research-and-truth-baseline
plan: "02"
subsystem: research-evidence-validation
tags: [python, pyyaml, jsonschema, draft-2020-12, provenance, traceability]

requires:
  - phase: 01-01
    provides: "Approved isolated Phase 1 Python validation toolchain"
provides:
  - "Strict Draft 2020-12 source and claim record contracts"
  - "Safe YAML, schema, semantic-link, and traceability validation CLI"
  - "Deterministic Markdown review work for canonical evidence records"
affects: [01-03, phase-1-acquisition, phase-1-spikes, evidence-governance]

tech-stack:
  added: []
  patterns: [safe YAML parsing, Draft 2020-12 schema gate, stable-ID semantic links, human-gated verification]

key-files:
  created:
    - .planning/research/schemas/source.schema.json
    - .planning/research/schemas/claim.schema.json
    - .planning/research/source-registry.yaml
    - .planning/research/claims.yaml
    - tools/validate-research.py
    - tests/phase1/test_evidence.py
  modified:
    - .planning/traceability/requirement-source-map.yaml
    - .planning/research/reports/validation.md

key-decisions:
  - "Preserved source-pack material is stored only as a draft collection seed, never as current upstream proof."
  - "Automation validates provenance and evidence links but cannot promote a claim to verified without dated reviewer approval."
  - "Traceability paths must resolve to the revision-pinned archive manifest and their recorded SHA-256 digests."

patterns-established:
  - "Validate schemas before records, then enforce duplicate-ID and graph semantics before rendering review work."
  - "Represent source origin, assertion kind, evidence class, maturity, review state, and freshness as separate fields."

requirements-completed: [EVID-01, OPER-03]
coverage:
  - id: D1
    description: "A source record is structurally validated for immutable identity, classification, uncertainty, impacts, freshness, and review fields."
    requirement: EVID-01
    verification:
      - kind: unit
        ref: "tests/phase1/test_evidence.py via tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_evidence.py'"
        status: pass
    human_judgment: false
  - id: D2
    description: "Source-linked claims reject dangling/unsupported evidence relations and automation-only verified transitions."
    requirement: EVID-01
    verification:
      - kind: integration
        ref: "tools/phase1-python tools/validate-research.py validate --root .planning/research --report .planning/research/reports/validation.md"
        status: pass
    human_judgment: false
  - id: D3
    description: "Canonical traceability mappings resolve only to archived paths with manifest-pinned SHA-256 digests."
    requirement: OPER-03
    verification:
      - kind: unit
        ref: "tests/phase1/test_evidence.py#test_traceability_mappings_resolve_to_pinned_archive_files"
        status: pass
    human_judgment: false

duration: 25m
completed: 2026-07-24
status: complete
---

# Phase 01 Plan 02: Source and Claim Evidence Tracer Summary

**A deterministic YAML-to-Draft-2020-12 evidence tracer now rejects incomplete or dangling provenance, preserves origin and maturity states, and emits review work without granting claim approval.**

## Performance

- **Duration:** 25m
- **Completed:** 2026-07-24
- **Tasks:** 2/2
- **Files modified:** 8

## Accomplishments

- Added strict, versioned source and claim schemas for immutable identity, classification, uncertainty, impacts, freshness, reviewer state, and the approved relation vocabulary.
- Implemented `validate-research.py validate` using `yaml.safe_load`, Draft 2020-12 schema validation, duplicate-ID checks, source/claim graph semantics, and deterministic Markdown review output.
- Repaired legacy requirement-source-map paths and verify every mapping against the preserved pack manifest and SHA-256 digest.
- Added deterministic fixtures covering complete/incomplete sources, duplicate IDs, valid provisional claims, dangling/unsupported evidence, automation-only verification, and insufficient blocking corroboration.

## Task Commits

1. **Task 1: Run one pinned source record through validation into review work** - `b1e6bdd` (test), `836576e` (feat)
2. **Task 2: Add the source-linked claim contract without conflating evidence states** - `26ba34d` (feat)

## Files Created/Modified

- `.planning/research/schemas/source.schema.json` - Strict immutable `SRC-*` record contract.
- `.planning/research/schemas/claim.schema.json` - Typed `CLM-*` contract with relations and review-gated states.
- `.planning/research/source-registry.yaml` - Draft archived-source collection seed, explicitly not upstream proof.
- `.planning/research/claims.yaml` - Provisional project-policy claim linked to its seed record.
- `tools/validate-research.py` - Safe parser, schema/semantic gates, traceability integrity checks, and deterministic report renderer.
- `tests/phase1/test_evidence.py` - Source and claim validation fixtures.
- `.planning/traceability/requirement-source-map.yaml` - Archive-valid requirement source paths.
- `.planning/research/reports/validation.md` - Current deterministic validation review work.

## Decisions Made

- Keep preserved-pack records visibly provisional/draft and never elevate them to immutable upstream proof.
- Enforce the core relation vocabulary (`supports`, `contradicts`, `measures`, `affects`, `recommends`, `supersedes`) in both schema and semantic validation.
- Treat automated validation as review preparation; dated reviewer evidence remains mandatory before a claim can be verified.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Normalized safely parsed YAML timestamp scalars before schema validation**
- **Found during:** Task 1
- **Issue:** PyYAML converts unquoted ISO timestamps to `datetime` values, while the JSON Schema correctly requires canonical timestamp strings.
- **Fix:** The safe YAML loader recursively serializes date/time scalars to ISO-8601 strings before Draft 2020-12 validation.
- **Files modified:** `tools/validate-research.py`
- **Verification:** All source and claim fixtures pass with deterministic report output.
- **Committed in:** `836576e`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** The normalization preserves safe parsing and canonical schema semantics without changing evidence meaning.

## Issues Encountered

- The original legacy map referenced a non-existent source-pack curriculum filename. It was repaired to the manifest-pinned `docs/05-CURRICULUM-AND-EXPERIENCE.md` path before semantic validation relied on it.

## User Setup Required

None - no external service configuration is required.

## Next Phase Readiness

- Plans 01-03 and later acquisition work can consume validated `SRC-*` and `CLM-*` records plus deterministic review output.
- Current source-pack seeds remain explicitly non-upstream evidence and must not be used to verify a protocol-sensitive claim.

## Self-Check: PASSED

All eight plan artifacts exist; Task commits `b1e6bdd`, `836576e`, and `26ba34d` resolve; no created or modified plan artifact contains an unintentional stub; and the full Phase 1 test suite, research validator, planning validator, and `git diff --check` passed.

---
*Phase: 01-research-and-truth-baseline*
*Completed: 2026-07-24*
