# Phase 1 Closeout Gate

## Research question

Does the complete Phase 1 evidence baseline satisfy its deterministic artifact, provenance, replay, lesson, governance, and no-scaffold contracts sufficiently to present a human closeout decision without converting proposed architecture or blocked upstream evidence into acceptance?

## Sources and immutable revisions

- Canonical source baseline: `SRC-POLICY-001` at commit `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, path `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`, SHA-256 `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`, retrieved `2026-07-24T00:00:00Z`; planning-archive/project-policy evidence, not current upstream protocol proof.
- Canonical policy baseline: `SRC-POLICY-002` at commit `b534103068be8c07e6869bfb7290fb60fdd87c8c`, path `.planning/governance/evidence-policy.md`, SHA-256 `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`, retrieved `2026-07-24T00:00:00Z`; project-policy evidence, not upstream protocol proof.
- Canonical claim, compatibility, drift, open-question, candidate-source, and ecosystem-disposition records were validated from `.planning/research/`. Every cited `CLM-*` in catalogs, lesson packets, and ADRs resolved to a complete immutable `SRC-*` path or remained an explicitly impact-scoped blocked record.
- The consolidated spike audit records the exact report, metadata, measurement, fragment, and replay-manifest digests for all SPK-A through SPK-L. Its current replay-manifest digest is `679be644f14a77b6c40528a74aea29e530837ef2db731a24ac13f8d4d4177d93` and rerun-input digest is `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`.

## Observations

Automated closeout commands completed successfully on the recorded isolated Python toolchain:

| Check | Actual result |
| --- | --- |
| `unittest discover -s tests/phase1` | Passed: 46 tests |
| Full `test_lesson_evidence.py` contract | Passed: 6 tests across LES-001 through LES-013 |
| `replay-spikes --manifest … --check` | Passed after validating pinned inputs and executing all 12 declared local replay commands |
| `validate-planning.py --phase-1-complete` | Passed: 0 errors, 0 warnings |
| `validate-research.py validate-reports --root .planning` | Passed canonical report and SPK metadata checks |
| `validate-research.py validate --root .planning/research --report …/validation.md` | Valid deterministic structural and semantic output; no human approval granted |

The required artifact inventory is present: executive/decision/risk/security syntheses; source, claim, compatibility, drift, open-question, current-work, catalog, teaching-scope, and pedagogy records; 13 lesson packets; SPK-A–SPK-L reports and replay manifest; proposed ADR 0001–0011; consolidation audit; governance record; candidate-source and ecosystem inventories. No forbidden production marker (`package.json`, `pnpm-workspace.yaml`, `src`, `apps`, or `packages`) exists.

| Spike | Metadata / replay disposition | Recorded measurement summary | Replay reference |
| --- | --- | --- | --- |
| SPK-A | planned / passed local replay | 7, 0 | `spk-a-workspace/metadata.yaml` |
| SPK-B | passed / passed | 584.662, 1471.271 | `spk-b-static-framework/metadata.yaml` |
| SPK-C | blocked / blocked | 33.352, 0.0 | `spk-c-boundary-harness/metadata.yaml` |
| SPK-D | blocked / blocked | 0, 1, 0 | `spk-d-verified-loader/metadata.yaml` |
| SPK-E | passed / passed | 0, 6, 6, 1 | `spk-e-content-rendering/metadata.yaml` |
| SPK-F | blocked / blocked | 593.762, 240084, 1508.372, 304388, 2, 0 | `spk-f-course-workbench/metadata.yaml` |
| SPK-G | blocked / blocked | 0, 0, 0, 0, 0 | `spk-g-package-conformance/metadata.yaml` |
| SPK-H | blocked / blocked | 333.707, 19, 8, 0.0 | `spk-h-browser-egress/metadata.yaml` |
| SPK-I | blocked / blocked | 11.235, 8625, 27, 1, 0.0 | `spk-i-diagram-motion/metadata.yaml` |
| SPK-J | blocked / blocked | 26.53, 74.381, 7955, 5174566, 24, 1, 1, 0.0 | `spk-j-code-editing/metadata.yaml` |
| SPK-K | blocked / blocked | 452, 3, 3, 1, 0 | `spk-k-deployment/metadata.yaml` |
| SPK-L | planned / passed local replay | 0 | `spk-l-source-freshness/metadata.yaml` |

The Phase 1 governance record has distinct pending slots for product, protocol/technical, security, accessibility, content/learning, and release; it intentionally records `phaseResult: blocked` pending human closeout.

## Conflicts

- Chromium fixture observations coexist with no attached Firefox result. `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` and `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` retain the failure before Playwright attachment; no browser download, launcher workaround, substitute browser, or configuration workaround was used.
- `SPK-D-IMPACT-001` preserves local byte-digest and mutation evidence only. `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, and `OQ-VERIFIED-LOADER-VERIFIER-001` block manifest, identity, signature/blob/aggregate, and verifier conclusions.
- `SPK-G-IMPACT-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, and `OQ-PUBLIC-CONFORMANCE-001` preserve the absent public release, root export, provenance, integrity, implementation, and conformance baseline; zero-operation replay is not package evidence.
- `SPK-H-IMPACT-001`, `DRF-EGRESS-001`, and `OQ-EGRESS-NIP-001` preserve local egress observations separately from upstream semantics. The restrictive CSP is proposed project policy only.
- VitePress reduced-motion/static-equivalent evidence remains independently unresolved; local deployment remains external-action-free; portable outcome remains unselected; editor evidence remains bounded and does not select CodeMirror or clear the CodeJar conflict.

## Inference

The deterministic evidence system is mechanically complete and reproducible, but it does not establish current upstream protocol, runtime, package, manifest/identity/verifier, cross-browser, production accessibility, public deployment, or portable-target truth. The only safe candidate direction is a **minimum static, deterministic, source-status-visible learning site after Phase 2 contract approval**.

This is a project-scope inference, not an ADR decision, protocol conclusion, residual-risk acceptance, Phase 1 pass, Phase 2 authorization, or permission to create production scaffolding.

## Prototype or measurement

The all-packet canonical-evidence test verified the complete ordered lesson inventory: `LES-001`, `LES-002`, `LES-003`, `LES-004`, `LES-005`, `LES-006`, `LES-007`, `LES-008`, `LES-009`, `LES-010`, `LES-011`, `LES-012`, and `LES-013`. It checked their canonical IDs, source/claim provenance, compatibility/drift/open-question targets, consolidation mappings, and uncertainty-boundary text.

The SPK-A–SPK-L table above records the actual metadata/replay status and each metadata measurement sequence. The replay runner did not treat the manifest as narrative: it checked input digests, required every stable SPK ID exactly once, and executed each local `validate-spike --complete` replay. Blocked results are successful preservation of the declared blocker state, not positive technical outcomes.

The closeout validator also checked deterministic typed-ID ordering, complete source fields, catalog/lesson/ADR claim-to-source traversal, candidate-source-manifest coverage by ecosystem-inventory disposition, all 12 report/metadata links, all 11 ADRs with `Status: proposed`, and absence of the forbidden production scaffold markers.

## Recommendation

**Candidate closeout recommendation: blocked pending human review.** The automation gate is green, but `PGV-PHASE-001` remains `blocked` until the project owner supplies itemized, dated role outcomes and one explicit result.

**Minimum website-unlocking decisions for Phase 2 / later static site:**

1. Record the Phase 1 human closeout result and per-role review status.
2. Keep ADR-0001 (public-site-first boundary), ADR-0002 (static-site candidate), and ADR-0004 (common structured source) as evidence-backed proposals for the Phase 2 product/content contract; do not convert them to accepted automatically.
3. Preserve static lessons, transcript/table/static equivalents, deterministic conceptual simulations, and source/status/uncertainty visibility as the safe scope boundary.
4. Keep production framework/application scaffolding prohibited until the required owner ADR decision and Phase 2 contract approval are recorded.

**Complexity safe to defer:** teaching host and real lab operation (ADR-0005/0008); portable target (ADR-0007); package admission/versioning (ADR-0010); editor and dynamic diagram capability (ADR-0006/0009); external deployment/publication (ADR-0003); and freshness cadence automation (ADR-0011). Deferral does not erase their blockers or required reviews.

## Uncertainty

- **EVID-03:** equality semantics for future compatibility dimensions remains an explicit versioned-schema-extension question; current known IDs and baselines validate, but a new dimension requires migration review.
- **EVID-04:** unlike spike measurement units remain unaggregated; raw values and their evidence remain linked without a fabricated universal score.
- **Residual blocker set:** `OQ-UPSTREAM-BASELINE-001`, `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001`, `OQ-EGRESS-NIP-001`, `OQ-PUBLIC-PACKAGE-BASELINE-001`, `OQ-PUBLIC-CONFORMANCE-001`, `OQ-VERIFIED-LOADER-MANIFEST-001`, `OQ-VERIFIED-LOADER-IDENTITY-001`, and `OQ-VERIFIED-LOADER-VERIFIER-001` remain blocked with mapped impacts.
- **Security exceptions:** none accepted. Public CSP, host/guest boundary, package, verifier, real external service, credentials, deployment, and browser workaround actions remain prohibited pending their named reviews.

## Affected phases and requirements

| Requirement | Traceability / result | Affected phases |
| --- | --- | --- |
| EVID-01 | Immutable source/claim identity, digest, locator, and deterministic index gate passed | 01, 02–11 |
| EVID-02 | Parallel drift/conflict, uncertainty, impact, and refresh records validated | 01, 02–11 |
| EVID-03 | Compatibility evidence is structurally complete but upstream baseline remains blocked | 01, 02, 03, 05, 11 |
| EVID-04 | Twelve spike reports/replays and raw measurements accounted for; positive recommendations remain scoped | 01, 02, 03, 04, 05, 08, 11 |
| OPER-01 | Targeted refresh/review-work and replay determinism validated; no automatic claim rewrite | 01, 02, 11 |
| OPER-03 | Governance role, exit-evidence, verification, requirement, and human-closeout fields validated | 01, 02–11 |

The Phase 2 entry gate requires a human-recorded passed Phase 1 baseline plus the evidence-backed proposed ADR 0001–0011 handoff. It permits product/content-contract definition only; human ADR disposition and Phase 2 contract approval remain separate production-scaffold gates.

## Owner and required approval

Research owner prepared the validated evidence package. Required human closeout entries are separate dated statuses for product, protocol/technical, security, accessibility, content/learning, and release roles, plus the project owner’s exact `passed` or `blocked` result. Protocol/technical review is required for upstream-sensitive evidence; security review for egress/authority/exceptions; accessibility review for learner-facing equivalents; content/learning review for teaching scope; release review for package and external delivery; product review for scope and portability.

All ADR 0001–0011 remain `proposed`. The evidence handoff at `.planning/research/adr-handoff.yaml` identifies each owner, approver, evidence IDs, deadline, impacts, and interim no-scaffold restriction. No approval is implied by this report or any automated command.
