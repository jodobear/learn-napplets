---
phase: 1
reviewers: [codex]
reviewed_at: 2026-07-23T18:07:52Z
plans_reviewed:
  - 01-01-PLAN.md
  - 01-02-PLAN.md
  - 01-03-PLAN.md
  - 01-04-PLAN.md
  - 01-05-PLAN.md
  - 01-06-PLAN.md
  - 01-07-PLAN.md
  - 01-08-PLAN.md
  - 01-09-PLAN.md
  - 01-10-PLAN.md
  - 01-11-PLAN.md
  - 01-12-PLAN.md
  - 01-13-PLAN.md
  - 01-14-PLAN.md
  - 01-15-PLAN.md
  - 01-16-PLAN.md
  - 01-17-PLAN.md
  - 01-18-PLAN.md
  - 01-19-PLAN.md
  - 01-20-PLAN.md
  - 01-21-PLAN.md
  - 01-22-PLAN.md
  - 01-23-PLAN.md
  - 01-24-PLAN.md
  - 01-25-PLAN.md
  - 01-26-PLAN.md
  - 01-27-PLAN.md
  - 01-28-PLAN.md
source_grounding: true
source_grounding_authority: grep
effective_drift_guard: .planning/governance/evidence-policy.md
---

# Cross-AI Plan Review — Phase 1

## Codex Review

Codex was invoked with the canonical project, roadmap, requirements, Phase 1 context and research, and all 28 plans. It did not return a review. The recorded output contains the submitted review packet followed by repeated authentication-refresh and transport failures, including HTTP 401 / expired-token errors at `/tmp/gsd-review-KgKBTI/gsd-review-codex.md:5415-5462`. It contains no reviewer-authored findings, strengths, severity labels, plan citations, or proposed edits.

This is one failed reviewer lane, not approval and not evidence of plan-content defects. Re-authenticate Codex and rerun `gsd-review --phase 1 --codex` before treating the deep review-convergence gate as satisfied. No PLAN change follows from the failed lane itself.

## Source-grounding Review

### Authority and method

The effective drift guard is `.planning/governance/evidence-policy.md`. It is the live enforcement policy; the preserved source pack is integrity-pinned at `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0` but remains tier-4 archive/planning guidance rather than protocol authority. Precedence and preservation are documented in `.planning/traceability/pack-v3-import.md:14-22`.

All declared new artifacts, report outputs, schemas, fixtures, IDs, and planned validators were excluded from absence findings. The current tree intentionally has no canonical research `source-registry.yaml`, claims registry, or compatibility matrix, so no upstream-facing plan reference can yet resolve through an immutable `SRC-*` record. The plans have no direct external URL citations; they cite generic symbols, discovery categories, and future records.

## Verification coverage

| Plan(s) | Cited external/upstream surface | Resolution status | Drift-guard severity |
|---|---|---|---|
| `01-01` | PyYAML 6.0.3, jsonschema 4.26.0, Playwright 1.61.0; Chrome/Chromium/Firefox | Versions and mutable official-doc pointers occur in research; no artifact hash, browser revision, or canonical source record | MEDIUM |
| `01-02`–`01-04` | JSON Schema Draft 2020-12, `yaml.safe_load`, Git `revision:path` resolution | Identifiable dialect/docs, but no artifact-pinned package evidence | MEDIUM |
| `01-05`–`01-07` | NIP-5D/NIP-5A; NAP registry/web projection/archetypes/conventions/NAP-INTENT; `napplet/web`; runtime/domain/example candidates; Learn FIPS | Discovery/archive pointers only; no upstream commit, locator, or digest | HIGH |
| `01-08`–`01-10`, `01-13`–`01-14`, `01-17`, `01-19`–`01-21`, `01-24` | Preserved research, curriculum, delivery, ADR, and report-template references | Resolves to archive paths and digest manifest at `c626…`; correctly non-authoritative for protocol facts | Covered as archive guidance |
| `01-11` | Sandboxed iframe, injection, `postMessage`, `MessageEvent.source`, domain removal; browser/Playwright behavior | No web-platform/browser/runner source bindings; cached summaries are insufficient | HIGH |
| `01-12` | Manifest resolution, identity, artifact bytes, signature/blob/aggregate verification | Future source/claim links are generic; no per-field binding or verifier provenance | HIGH |
| `01-15` | Public packages, public exports, external adapters | No official registry/repository, immutable release/tag, export locator, or source record | HIGH |
| `01-16` | `fetch`, WebSocket, EventSource, workers, navigation/referrer/origin, CSP/current-NIP behavior | Browser measurements are observations, but claimed NIP semantics have no pinned source | HIGH |
| `01-18` | CodeMirror | Generic package family only; no concrete package, repository, version, integrity, license, or public-API locator | HIGH |
| `01-22`–`01-23` | Package/version/update claims; adapter behavior | “Pinned source” labels do not require transitive immutable-source resolution | HIGH |
| `01-25` | Package/import evidence, runtime behavior, external adapters | Lesson validation does not require technical claims to traverse to complete `SRC-*` records | HIGH |
| `01-26` | Learn FIPS and two technical-learning comparators | Learn FIPS has no official URL/version/revision/license provenance; two comparators are unnamed | HIGH |
| `01-27` | `manifest`, `dTag` | Bare unresolved symbols without source binding or open-question linkage | HIGH |
| `01-28` | Upstream/pinned-source facts; browser egress; CSP | Source IDs are required but not transitively validated; CSP must remain project policy unless sourced | HIGH |

### Current HIGH concerns

1. **No enforceable initial authority set for source acquisition.** `01-05-PLAN.md:85,100`, `01-06-PLAN.md:89`, and `01-07-PLAN.md:73` must seed immutable `SRC-*` entries for NIP-5D, NIP-5A, and the named napplet repositories; record official repository, commit SHA, path/locator, retrieval time, digest, authority, and maturity. They must also require a candidate-source manifest for each domain/runtime/package/example/pedagogy comparator, and make unresolved acquisitions impact-scoped `blocked` records. `01-06` must bind both sides of each `DRF-*` result to source IDs and immutable baseline fields; `01-07` must require a released-package record and a repository/public-export record per catalog item.

2. **Browser-boundary findings lack immutable source bindings.** `01-11-PLAN.md:73,83,85` must require `metadata.yaml.sourceBindings` for sandbox, injection, message carrier, `MessageEvent.source`, and domain removal, each resolving to a `SRC-*` locator/revision/path-or-section/digest/authority. Selected Chromium and Firefox execution surfaces must be separately pinned; absent bindings must be `blocked`, and remaining results must be labeled browser observations.

3. **Verification spike permits unbound cryptographic semantics.** `01-12-PLAN.md:73,83,85` must require per-field source-binding rows for manifest, identity, artifact bytes, signature, blob, and aggregate fields. Each row needs `SRC-*`, `CLM-*`, immutable revision/path/locator/digest, expected outcome, and normative/implementation-specific/blocked classification; reused verifier provenance must meet the same rule.

4. **Package, adapter, and lesson technical claims can remain generically sourced.** `01-15-PLAN.md:72,95`, `01-22-PLAN.md:77,87,115`, `01-23-PLAN.md:83,93`, `01-25-PLAN.md:98,100`, and `01-28-PLAN.md:117,119` must mandate transitive validation of every upstream fact, package, adapter, fixture, and lesson citation. In particular, Plan 01-25's `test_lesson_evidence.py` contract must traverse every cited `CLM-*` through its source links to complete immutable `SRC-*` records, and fail a packet on a missing, dangling, incomplete, or non-immutable source binding rather than merely validating `CMP-*`, `DRF-*`, and `OQ-*` family links. Each `SRC-*` must include official URL/repository, revision or package integrity, path/locator, retrieval time, digest, authority tier, and maturity; unresolved input is `blocked`.

5. **Current-NIP claims are not separated from browser observations or proposed CSP.** `01-16-PLAN.md:71,81` must require a complete `SRC-*`/`CLM-*` pair for each current-NIP assertion, classify channel results as browser measurements unless independently supported, make unpinned assertions `OQ-*` or blocked, and retain CSP recommendations as project policy unless separately sourced.

6. **CodeMirror is not an identified, immutable candidate.** `01-18-PLAN.md:18,68,81` must require exact package name/version, official registry/repository, release/tag/commit or registry integrity, public API/export locator, license source, retrieval time, and source revision for each concrete candidate; otherwise it stays blocked.

7. **Pedagogy comparison is not reproducible.** `01-26-PLAN.md:75` must register Learn FIPS and two named comparators with official URL, immutable revision or captured version/date, locator, digest, license/use constraints, and selection rationale before comparison; unmatched comparators are excluded or blocked.

8. **`manifest` and `dTag` remain bare symbols.** `01-27-PLAN.md:71` must bind each question to a governing `SRC-*` or a dated `OQ-*` that records official-source search scope, unresolved reason, affected lessons, and refresh trigger.

9. **Deep plan-review convergence is neither encoded as an execution gate nor complete.** No Phase 1 plan carries a machine-checkable prerequisite that requires the committed review record, a successful reviewer response, and explicit convergence/sign-off before Phase 1 execution. The requested Codex reviewer also returned no assessment because of expired authentication. Add a final Plan 01-28 task or an execution preflight validator that fails closed unless the review record names a successful reviewer, all current HIGH concerns are incorporated or explicitly dispositioned, and an authorized convergence decision is recorded. Re-authenticate Codex and rerun before execution; Phase 1 remains stopped at the required convergence gate under `.planning/STATE.md:7-11,30-33,83-87`.

10. **Plan 01-28 does not prove concurrent consolidation is staged, locked, and atomically published.** `01-28-PLAN.md:105,119-121` sorts and reruns fragments, but does not require an exclusive lock, immutable input snapshot/staging directory, atomic replacement of all canonical outputs plus audit, or a failure-injection proof that a mid-merge error exposes neither partial canonical state nor a mismatched audit. Add those mechanics and a two-process contention test; the test must prove one process blocks or exits deterministically, a failed staged merge leaves every target byte-identical, and a successful merge publishes the full canonical set and audit together.

11. **Plan 01-08 declares a downstream lesson as its own required artifact.** `01-08-PLAN.md:22-29,80-87` declares `LES-09`, while `01-27-PLAN.md:7-14` is its later-wave producer. Remove it from Plan 01-08's own required artifacts or label it explicitly as `produced_by: 01-27`; add a lint that each declared artifact is locally created or explicitly external/deferred.

12. **Pre-execution spike validation can deadlock on evidence that exists only after execution.** `01-04-PLAN.md:85-92`, `01-15-PLAN.md:68-74,91-97`, and `01-17-PLAN.md:63-79` require measurement/raw-output completeness before the corresponding setup task creates it. Define `validate-spike --contract` for pre-run contracts and `validate-spike --complete` only after environment, output, digests, measurements, and replay evidence exist; change every setup task to use the contract mode.

13. **Phase 2 has a circular ADR admission condition.** `phase-gates.yaml:53-56`, `ROADMAP.md:146`, `01-21-PLAN.md:15-17`, and `01-24-PLAN.md:159-164` require accepted/deferred ADRs before Phase 2 even though acceptance belongs to Phase 2. Require a passed Phase 1 baseline plus evidence-backed proposed ADRs at entry, then make an approval checkpoint block production scaffolding; add an ADR handoff with owner, approver, evidence IDs, deadline, interim restriction, and impact.

14. **All-spike replay is claimed at closeout but not executable from the closeout verification.** `01-24-PLAN.md:145-151` requires replay but its verification command does not run any replay runner, contrary to `01-VALIDATION.md:29-34`. Have Plan 01-28 create a versioned `replay-manifest.yaml` for SPK-A–SPK-L and have Plan 01-24 run every applicable replay, failing on missing, stale, or threshold-failing evidence.

15. **SPK-J/K/L can influence ADRs without crossing the canonical evidence boundary.** `01-18-PLAN.md:99-102`, `01-19-PLAN.md:103-106`, `01-20-PLAN.md:92-95`, `01-28-PLAN.md:110-121`, and `01-21-PLAN.md:57-65` allow raw report consumption while consolidation records report-only inputs as no-impact. Require typed schema-validated decision-evidence fragments for SPK-J/K/L and require Plans 01-21 through 01-23 to consume consolidation-issued canonical IDs only.

16. **The canonical requirement-source map contains broken preserved-pack paths.** `.planning/traceability/requirement-source-map.yaml:8,10-12,18,22` references a nonexistent `03-LEARNING-AND-INTERACTION-DESIGN.md`, while the pinned pack manifest lists different files. Correct the mappings before execution and add a Plan 01-02 or Plan 01-24 traceability test that resolves every mapped immutable-pack path and digest.

17. **Core-concept and ecosystem-inventory exit criteria are not mechanically enforced.** The preserved requirements at `docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md:50-58,432-449` demand concept source packs and ecosystem dispositions, but `01-05-PLAN.md:77-85`, `01-25-PLAN.md:93-100`, and `01-24-PLAN.md:125-140` do not enforce them. Add a revision-pinned ecosystem inventory and core-concept map; require every concept to resolve to pinned `SRC-*`/`CLM-*` records and every discovered item to have an inventory disposition before closeout.

### Current actionable non-HIGH concerns

1. **Toolchain provenance is below the evidence floor.** `01-01-PLAN.md:73-77,85,95,97`, `01-02-PLAN.md:90`, and `01-05-PLAN.md:85` must require release-artifact URL plus SHA-256/integrity and license source for PyYAML/jsonschema/Playwright; browser vendor/version or Playwright browser-revision provenance; the explicit Draft 2020-12 `$schema` URI and parser/validator record IDs; and Git executable version, commit OID, blob OID, and `revision:path` for acquisition-log entries.

2. **Four plans ambiguously cite report headings.** `01-17-PLAN.md:75-77`, `01-18-PLAN.md:89-91`, `01-19-PLAN.md:93-95`, and `01-20-PLAN.md:77-84` must add `.planning/governance/evidence-policy.md` to `read_first`, identify its Reports section as the canonical ten-heading authority, and name `RESEARCH-REPORT-TEMPLATE.md` only as a non-authoritative structural aid.

3. **Plan 01-28 lacks an SPK-H output-provenance negative test.** `01-28-PLAN.md:105,117,119` validates SPK-H input provenance but does not prove that a generated `security-egress-findings.md` with a missing, altered, or mismatched upstream-fact/browser-observation/policy/question source binding is rejected. Add a failing fixture and acceptance criterion that validates every output claim's typed link back to the immutable SPK-H fragment, report, and canonical source/claim record, and fails before publication on a broken link.

4. **The stated Wave-7 barrier is missing from executable dependencies.** `ROADMAP.md:90-109`, `01-09-PLAN.md:3-6`, and `01-20-PLAN.md:3-6` describe Wave 8 as blocked on all Wave-7 work but omit Plan 01-20 from the dependencies. Add `01-20` to each Wave-8 plan or amend the roadmap to describe independent tracks and why source-freshness work need only precede consolidation.

5. **SPK-H may not test SPK-C's selected boundary model.** `01-16-PLAN.md:68-83` and `01-11-PLAN.md:69-85` run concurrently although H claims the selected iframe/loading model. Make Plan 01-16 depend on Plan 01-11, establish an earlier shared versioned loading-model contract, or rerun SPK-H under the model selected by SPK-C.

6. **Verification commands can escape the approved isolated research toolchain.** `01-01-PLAN.md:81-98`, `01-02-PLAN.md:91,107`, `01-24-PLAN.md:139,149,162`, and `01-VALIDATION.md:23-32` create an isolated environment but later use ambient `python3`. Emit a stable approved interpreter wrapper and require it in every verification/replay command with recorded version/hash.

7. **Evidence and maturity vocabularies lack a validated lossless mapping.** `evidence-policy.md:9-18`, `AGENTS.md:94-120`, `01-02-PLAN.md:81-108`, and `01-05-PLAN.md:95-102` can collapse upstream proposal or implementation observation into a generic fact. Preserve raw source labels and validate mappings to canonical `assertionKind`, `evidenceClass`, and `maturity`; render both source origin and maturity.

8. **ADR, lesson-packet, and teaching-scope checks remain mostly structural.** `01-21-PLAN.md:75-87`, `01-22-PLAN.md:77-89`, `01-23-PLAN.md:79-85`, `01-25-PLAN.md:92-100`, and `01-26-PLAN.md:63-77` need validated contracts and negative fixtures for required semantic fields, canonical IDs, uncertainty, impacts, alternatives, approvals, revisit triggers, audience coverage, and safe fallback.

9. **Impact-fragment semantic validation arrives after fragments are produced.** `01-15-PLAN.md:91-98`, `01-16-PLAN.md:77-84`, and `01-28-PLAN.md:96-107` use early string-presence checks. Move the fragment schema, parser, cross-record/digest validator, and negative fixtures to Plan 01-04 or another prerequisite before the parallel spike wave.

10. **Blocking-claim corroboration and fallback policy are not machine-verifiable.** `01-CONTEXT.md:31-38,47-50`, `01-02-PLAN.md:101-108`, and `01-24-PLAN.md:130-151` must require typed primary and independent corroboration links; every unresolved blocker accepted in a passed outcome must contain approved safe fallback/defer path, scope, approver, date, and revisit criterion.

11. **SPK-I/J omit required cross-browser and adversarial coverage.** `01-CONTEXT.md:64-67`, `01-17-PLAN.md:64-79`, and `01-18-PLAN.md:65-70,87-93` must add candidate × Chromium × Firefox evidence, keyboard/reduced-motion/screen-reader/static-equivalence checks, and hostile-input tests proving learner content cannot reach dynamic execution, script injection, or a trusted-host sentinel.

12. **The final lesson count is directory-wide rather than index-defined.** `01-25-PLAN.md:93-110` should treat indexed LES filenames as the only authoritative inventory and constrain or remove raw `*.md` counting. (LOW)

13. **Phase/source terminology is easy to misread during approvals.** `phase-crosswalk.md:3-17` and `01-01-PLAN.md:2-5` should add `gsd_phase: 1`, `source_phase: 0`, and `adr_status_limit: proposed` to every Phase 1 plan frontmatter. (LOW)

14. **SPK-K needs an explicit sandbox-write exception decision.** `01-19-PLAN.md:74-98` conflicts with the read-only live-probe preference in `01-CONTEXT.md:25-27,40-44`; make it dry-run/local only or record named target, classification, cleanup, retention, and sign-off controls. (LOW)

## Consensus Summary

Only the requested Codex lane was selected, and it failed before producing review content; therefore no cross-AI agreement can be claimed. The source-grounding pass and independent all-plan audit verify the listed evidence-provenance, lifecycle, dependency, replay, consolidation, and gate defects against canonical planning and the effective drift guard. The Phase 1 baseline validator passes with the expected pending-deliverables warning, but that does not resolve any concern above or authorize execution.
