---
phase: 1
reviewers: [codex]
successful_reviewers: [codex]
reviewed_at: 2026-07-29T12:38:04Z
reviewed_commit: 9b5794f6043da001053404861ff2a888347f9be7
reviewed_head: 9b5794f6043da001053404861ff2a888347f9be7
review_binding_status: exact-current-head-plan-snapshot-not-converged
supersedes_reviewed_commit: 243e72f58a71bc9476f7a5d97f0b5fd47cb0667b
previous_review_record_commit: 341884f
reviewer_identity:
  codex: "codex-cli/0.146.0:external-read-only"
reviewer_access:
  codex: "read-only review of current HEAD with repository source access"
review_context: "current committed HEAD plan snapshot; external Codex CLI; no Phase 1 plan execution"
current_high: 0
current_medium: 1
current_low: 0
current_actionable: 1
current_actionable_non_high: 1
authorization:
  verdict: "NOT CONVERGED; HIGH=0; actionable=1"
  superseded: false
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
  - 01-29-PLAN.md
  - 01-30-PLAN.md
  - 01-31-PLAN.md
  - 01-32-PLAN.md
  - 01-33-PLAN.md
  - 01-34-PLAN.md
  - 01-35-PLAN.md
  - 01-36-PLAN.md
  - 01-37-PLAN.md
  - 01-38-PLAN.md
  - 01-39-PLAN.md
  - 01-40-PLAN.md
  - 01-41-PLAN.md
  - 01-42-PLAN.md
  - 01-43-PLAN.md
  - 01-44-PLAN.md
  - 01-45-PLAN.md
plan_snapshot:
  count: 45
  total_bytes: 659132
  aggregate_sha256: f5f924b6347e74311e2c3e0567241d3232adbe1550a122f6990eb35f56f7e24e
  algorithm: "lexically ordered basename + NUL + exact bytes + NUL"
reviewed_source_inputs:
  status: "6/6 regular blobs, digests and worktree bytes verified by Codex"
  paths:
    - .planning/PROJECT.md
    - .planning/phases/01-research-and-truth-baseline/01-CONTEXT.md
    - .planning/research/reports/upstream-refresh-kehto-web-2026-07-28.md
    - .planning/research/reports/upstream-refresh-napplet-web-2026-07-28.md
    - .planning/research/reports/upstream-refresh-napplet-naps-2026-07-28.md
    - .planning/research/reports/upstream-refresh-synthesis-2026-07-28.md
---

# Cross-AI Plan Review — Phase 1

## Review Scope and Binding

Codex independently reviewed committed `HEAD` `9b5794f6043da001053404861ff2a888347f9be7` through installed `codex-cli 0.146.0` in read-only mode. It reviewed all 45 Phase 1 plans, reproduced the plan binding, and did not edit files or execute a Phase 1 plan.

Binding reproduced: 45 regular `100644` Git blobs with worktree-byte equality; 659,132 plan bytes; aggregate SHA-256 `f5f924b6347e74311e2c3e0567241d3232adbe1550a122f6990eb35f56f7e24e`; six mandatory source inputs as regular blobs with matching digests and worktree bytes; zero dependency-DAG cycles/missing/same-or-later-wave dependencies; requirement union exactly `EVID-01` through `EVID-04`, `OPER-01`, and `OPER-03`; and all 39 context decisions covered.

This record supersedes the `243e72f` review. Its two former MEDIUM findings were checked against the revised plans: the content-addressed review-validity ambiguity is resolved, and global exactly-once probe execution was replaced by canonical evidence-row uniqueness. A new MEDIUM remains, so execution remains prohibited.

## Codex Review

### Summary

Plan 01-32’s freshness ambiguity is resolved. Plan 01-40 no longer demands globally single probe execution. The replacement command-attempt ledger, however, has one self-recording contradiction. **Verdict: NOT CONVERGED.**

### Strengths

- Plan 01-32 now makes review validity unambiguously content-addressed: audit time must be syntactically valid, but unchanged bound bytes cannot expire solely by calendar age (`01-32-PLAN.md:86`). That agrees with Plan 01-29’s byte/commit/supersession validity rules (`01-29-PLAN.md:90`).
- Plan 01-40 now requires exactly one canonical evidence row per probe while permitting discovery and reruns as separate execution attempts (`01-40-PLAN.md:21`, `01-40-PLAN.md:125`).
- Source grounding remains strong: six-path review binding, regular Git-blob verification, worktree equality, and Git-blob-only loading are explicitly required (`01-29-PLAN.md:94`, `01-45-PLAN.md:96`).
- Repository merges remain observed implementation/release evidence rather than normative protocol authority; EVID-03 and EVID-04 remain blocked until qualified inputs and measurements exist (`.planning/research/reports/upstream-refresh-synthesis-2026-07-28.md:13`, `01-RESEARCH.md:614`).
- Human authority, proposed-only ADRs, transactional publication, wrapper enforcement, and no-production-scaffold boundaries remain fail-closed.

### Concerns

#### HIGH

None.

#### MEDIUM

##### 1. Command-attempt ledger cannot include its own later verification attempts

**Actionable: yes**

Plan 01-38 requires every plan-declared full-suite discovery to appear in the completed ledger (`01-38-PLAN.md:81`), then its automated verification runs two more discovery commands (`01-38-PLAN.md:82`). The same temporal conflict appears in Plan 01-40: Task 1 writes the candidate ledger after recording every plan-declared attempt (`01-40-PLAN.md:129`) and then runs another full discovery (`01-40-PLAN.md:130`); Task 2 finalizes and validates the candidate (`01-40-PLAN.md:149`) and then runs full discovery again (`01-40-PLAN.md:150`).

Mechanism: omitting those later plan-declared attempts makes the ledger incomplete. Appending them mutates ledger bytes after its evidence/digests have been recorded. The prior global exactly-once defect is fixed, but the replacement ledger contract lacks a finite closure boundary.

**Required plan change:** define the ledger as designated evidence-production attempts ending before ledger finalization, and explicitly classify subsequent validator/regression reruns as post-closure verification outside ledger completeness; or record post-closure verification in a separate digest-bound artifact.

#### LOW

None.

### Risk Assessment

No current HIGH-risk plan defect was found. Source-authority and phase-transition boundaries are strong. Residual execution risk is MEDIUM: command-attempt completeness can become unverifiable or force post-validation mutation. Upstream protocol, package, runtime, conformance, and reproducible-spike gaps remain intentionally blocked rather than accepted as truth.

### Exact Counts and Authorization

| Metric | Count |
|---|---:|
| HIGH | 0 |
| MEDIUM | 1 |
| LOW | 0 |
| ACTIONABLE | 1 |
| ACTIONABLE_NON_HIGH | 1 |
| Plans reviewed | 45 |
| Mandatory source inputs verified | 6 |
| DAG errors | 0 |

`NOT CONVERGED; HIGH=0; ACTIONABLE=1`

## Consensus Summary

Codex was the explicitly selected and successful external reviewer. No multi-reviewer weighted consensus exists; this source-grounded Codex result controls the current authorization.

### Verified Strengths

- The previous Plan 01-32 calendar-age ambiguity is fully addressed in executable plan text.
- The previous Plan 01-40 global exactly-once execution contradiction is fully addressed by changing the contract to canonical evidence-row uniqueness.
- Current committed bytes, six mandatory source inputs, dependency ordering, requirement coverage, and decision coverage were independently checked.
- Planning evidence, implementation observations, derived reports, and upstream authority remain explicitly separated.

### Current Blocking Concern

1. **MEDIUM/actionable — finite command-attempt ledger closure is unspecified.** Plans 01-38 and 01-40 require ledger completeness while scheduling later verification discoveries that cannot be represented without mutating finalized evidence. Incorporate an explicit designated-evidence closure boundary or a separate post-closure attestation before execution.

### Authorization

- HIGH=0
- MEDIUM=1
- LOW=0
- ACTIONABLE=1
- ACTIONABLE_NON_HIGH=1
- VERDICT=`NOT CONVERGED`

Required next action: targeted review-mode replan for Plans 01-38 and 01-40, then a new exact-commit Codex review. Do not execute Plan 01-29.

## Verification coverage

### Method, scope, and authority rule

This configured source-grounding pass resolved all cited existing paths and named symbols in current `01-01-PLAN.md` through `01-45-PLAN.md`, including the 28 already-executed historical plans and the 17 remaining plans. Repeated citations are collapsed only where they identify the same target. Newly produced artifacts/interfaces were excluded from resolution and are listed separately as unresolved planned outputs.

An existing Graphify graph was queried for navigation only; it produced no source claims used here. Graphify is not evidence authority.

Effective authority labels:

- **Planning evidence (P):** project/planning docs, ADRs, phase docs, and preserved source-pack docs. They establish project intent or state only, never upstream protocol authority.
- **Implementation/evidence (W):** current repository tools, schemas, fixtures, tests, and spike artifacts. They establish observed repository behavior/content only.
- **Derived output (D):** research records, reports, measurements, manifests, reviews, and generated artifacts. They are not upstream authority.
- **Upstream immutable authority (U):** none of the repository-local citations resolves to this class in the current tree. Refresh reports are observed/derived material, not normative upstream sources.

### Plans 01-01 through 01-28

| Plans | Existing cited paths and symbols resolved | Effective authority and verification result |
|---|---|---|
| 01-01–01-05 | `.planning/{PROJECT.md,ROADMAP.md,STATE.md}`; `01-CONTEXT.md:16-67`; `01-{RESEARCH,PATTERNS,VALIDATION,REVIEWS}.md`; governance `{approval-matrix,evidence-policy,decision-register}.md`; validation `{phase-gates.yaml,required-artifacts.json}`; preserved source-pack templates; research `{source-registry,claims,drift-register,compatibility-matrix,open-questions,acquisition-log,candidate-source-manifest,ecosystem-inventory}.yaml`; research schemas; `tools/{phase1-python,validate-planning.py,validate-research.py,acquire-sources.py}`; Phase 1 test modules; `requirements-phase1-tools.txt`; `toolchain-approval.yaml`; `toolchain-environment.json`. Named routes include `phase1_execution_preflight_errors`, `phase1_command_errors`, `phase1_completion_errors`, and `--phase-1-execution-preflight` in `validate-planning.py:42-296`. | P/W/D. All resolve as planning, current tooling, or local derived evidence; no upstream baseline is established. `CLM-UPSTREAM-BASELINE-001` remains blocked (`claims.yaml:29-65`). |
| 01-06–01-10 | Preserved research-plan/delivery/architecture docs; research `{source-registry,claims,acquisition-log,drift-register,compatibility-matrix,open-questions,open-work-snapshot,terminology-map,teaching-scope,package-map,runtime-comparison,domain-catalog,archetype-convention-catalog,example-napplet-catalog,toolchain-approval}.yaml`; drift/compatibility/spike schemas; `validate_research` validators and `refresh-sources.py`; lesson index and packets; SPK-A and SPK-B artifact sets. Named symbols include `validate_drift`, `validate_compatibility`, `validate_spike`, `validate_report`, `validate_lessons`, `SPK-A-WORKSPACE`, and package-gate entries. | P/W/D. Compatibility is explicitly `blocked` (`compatibility-matrix.yaml:3-50`); no public `napplet/web` package baseline exists (`package-map.md:13-35`). Existing lesson enforcement uses three-digit IDs (`validate-research.py:393-396`). |
| 01-11–01-15 | Planning docs and preserved source-pack docs; research `{source-registry,claims,compatibility-matrix,drift-register,teaching-scope,terminology-map,delivery-mode-recommendation,package-map,toolchain-approval}`; full SPK-C, D, E, F, and G artifact sets; `phase1-python`, `validate-research.py`, `validate-planning.py`. | P/W/D. Existing spike reports are observed local evidence, not protocol/package authority. SPK-C lacks Firefox evidence; SPK-D is not verified-loader evidence; SPK-F selected no portable target; SPK-G performed no package install/import/conformance target. |
| 01-16–01-20 | Context/governance inputs; research `{claims,drift-register,teaching-scope,pedagogy-review,package-map,delivery-mode-recommendation,compatibility-matrix,source-registry,open-questions}`; SPK-H, I, J, K, and L artifact sets; `refresh-sources.py:51-138`; `test_drift.py:48-155`. | P/W/D. SPK-H/I/J do not establish cross-browser success; Firefox is an execution blocker. SPK-K is local-only and does not establish deployment/publication. SPK-L report interpolation is malformed (`report.md:10-12,26-28`) and metadata remains planned (`metadata.yaml:5,49-51`). |
| 01-21–01-24 | Planning/governance docs; research records and consolidation report; ADRs `0001`–`0011`; spike reports; traceability `{requirement-source-map.yaml,pack-v3-import.md}`; research `{report-contract.yaml,phase-governance.schema.json,phase-governance.yaml,reports/phase-gate.md,reports/validation.md,adr-handoff.yaml}`; replay manifest; `validate-planning.py`, `validate-research.py`, `test_governance.py`, and `test_lesson_evidence.py`. Named functions include `replay_spikes`, `validate_impact_fragment`, `discover_consolidation_inputs`, and `consolidate_spike_impacts`. | P/W/D. ADRs are local decisions/proposals, not proof of upstream-sensitive premises. Historical `phaseResult: passed` and scoped gate passes are stale derived output; current authoritative state is blocked (`STATE.md:28-35`). |
| 01-25–01-28 | Lesson packet index (`LES-001`–`LES-013`) and named packets; packet template; `test_lesson_evidence.py` symbols `EXPECTED_INVENTORY`, `CANONICAL_HEADINGS`, `ID_PATTERN`, `AUDIT_TARGETS`, `LessonEvidenceTests`; pedagogy/delivery research; preserved delivery/curriculum docs; spike-consolidation report; research schemas; `validate-research.py:463-642,905-1038,1065-1099`; consolidation tests; all SPK report and cited impact-fragment files. | P/W/D. External pedagogy comparators remain blocked discovery pointers (`candidate-source-manifest.yaml:70-99`); no real-lab host profile is selected (`teaching-scope.yaml:2-33`). Consolidation only proves the local transaction/test surface, not upstream truth. |

### Plans 01-29 through 01-45

| Plan | Existing cited paths/symbols resolved | Effective authority and verification result |
|---|---|---|
| 01-29 | `tools/{phase1-python,validate-planning.py,acquire-sources.py}`; `tests/phase1/{test_preflight.py,test_evidence.py}`; planning `{PROJECT.md,STATE.md,01-CONTEXT.md,01-RESEARCH.md,01-REVIEW.md,01-VERIFICATION.md,01-REVIEWS.md}`; four upstream-refresh reports; `toolchain-approval.yaml`; `toolchain-environment.json`. Named fields: `python.isolatedInterpreter`, `python.resolvedExecutable`, `python.executableSha256`; review fields `reviewed_commit`, `reviewer_identity`, `plan_file_sha256`, `reviewed_source_inputs`. | P/W/D. Current tooling and binding evidence only; refresh reports are derived observations, not U. |
| 01-30 | `source-registry.yaml`, `candidate-source-manifest.yaml`, `claims.yaml`, `compatibility-matrix.yaml`, ADR `0010`, `acquire-sources.py`, `validate-planning.py`, governance role/schema fields. | P/W/D. Candidate records are blocked discovery evidence, not acquired sources or authority receipts. |
| 01-31 | Research `{source-registry,phase-governance,candidate-source-manifest,acquisition-log,claims,compatibility-matrix,open-work-snapshot}.yaml`; `acquire-sources.py`; `validate-planning.py`; governance/evidence tests. `SRC-POLICY-001/002` and blocked `CLM-UPSTREAM-BASELINE-001` resolve. | P/W/D. Existing policy roles are generic phase signoff slots, not per-scope authority determinations. |
| 01-32 | `validate-planning.py`, `phase1-python`, `test_preflight.py`, `test_lesson_evidence.py`, phase/research inputs. `phase1_citation_and_inventory_errors()` and `GATE016`–`GATE018` resolve at `validate-planning.py:105-168,147,152,156`; current review fields are YAML `current_high` and `authorization.verdict`. | P/W. Existing validator behavior is local implementation; it is not upstream authority. The current literal `\\b` regex at `validate-planning.py:144` does not itself prove the proposed stronger citation behavior. |
| 01-33 | `validate-research.py`, `refresh-sources.py`, replay manifest, spike/drift/evidence tests, SPK-G metadata, `spike.schema.json`; `SPIKE_REPORTS`; `validate-spike`, `replay-spikes`, and `validate` routes. | P/W/D. `replayCommand` is manifest data executed through `shlex.split()` (`validate-research.py:946-958`), not authority. |
| 01-34 | `validate-research.py`; drift schema/register; spike-impact schema; source/claim/compatibility/question records; SPK-C/H impact fragments; drift/consolidation tests. | P/W/D. Current drift remains schema version 1 and is not the planned v2 source-class/migration contract. |
| 01-35 | Compatibility schema/matrix; source/claim/drift/question/open-work/package records; `test_compatibility.py`; SPK-G files; ADR `0010`. `CMP-BASELINE-001` is blocked. | P/W/D. Existing compatibility schema is v1-style (`compatibility.schema.json:7-22`), not the planned seven-dimension v2 contract. |
| 01-36 | `test_spikes.py`; full SPK-G artifact set; `validate-research.py`. Existing retained blocker `SPK-G-BLOCKED-NO-PUBLIC-RELEASE-BASELINE` resolves at `measurements.yaml:23-29`. | P/W/D. It is a retained blocked/no-operation baseline, not package or release authority. |
| 01-37 | `phase1-python`, `validate-planning.py`, `validate-research.py`; current Phase 1 test modules; compatibility matrix; replay manifest; phase review/verification docs. Existing routes include `--phase-1-execution-preflight`, `--phase-1-complete`, `validate`, `validate-reports`, and `replay-spikes`. | P/W/D. Current command support does not establish proposed closeout evidence. |
| 01-38 | `01-VALIDATION.md`; state/review/verification docs; current Phase 1 tests; research records; replay manifest; tool trio. `nyquist_compliant` and `wave_0_complete` resolve as `false` at `01-VALIDATION.md:6-7`. | P/W/D. Existing validation is pending/draft, not terminal canonical-probe evidence. |
| 01-39 | `STATE.md`, `.planning/config.json:48-49`, phase review/verification/validation/research docs, tool trio, tests/research records. `security_asvs_level: 1` and `security_block_on: high` resolve. | P/W/D. The cited pinned OWASP ASVS source is absent locally, so no U authority is locally verified. |
| 01-40 | `{STATE,ROADMAP,PROJECT,REQUIREMENTS}.md`; phase context/research/review/validation/verification docs; current tests/research/tools. Historical `## Review Finding Adjudication` resolves only in `01-VERIFICATION.md:147`. | P/W/D. No terminal candidate/staging evidence currently exists; the ledger-closure MEDIUM above remains actionable. |
| 01-41 | `package-map.md`, `ecosystem-inventory.yaml`, `open-work-snapshot.json`, `test_compatibility.py`, SPK-G metadata, ADR. `OWS-001` resolves at `open-work-snapshot.json:3`. | P/W/D. The package map explicitly says no published-package proof exists (`package-map.md:11-15`). |
| 01-42 | `validate-research.py`, `validate-planning.py`, `refresh-sources.py`, spike/preflight tests, canonical research records, replay manifest. | P/W/D. Current tools lack the planned transactional snapshot/recovery interface. |
| 01-43 | `validate-research.py`; live `claims.yaml`, `drift-register.yaml`, `open-questions.yaml`, `package-map.md`, `open-work-snapshot.json`; source/compatibility records; SPK-G files; ADR. | P/W/D. Observed-refresh staging targets and attestation are absent. |
| 01-44 | `requirements-phase1-tools.txt`; `toolchain-approval.yaml`; `phase1-python`; `test_evidence.py`; toolchain environment manifest. The approved PyYAML/jsonschema/Playwright scope and matching pins resolve. | P/W/D. Wrapper forwarding does not certify a wheelhouse or installation. |
| 01-45 | `acquire-sources.py`; `test_evidence.py`; research `{acquisition-log,candidate-source-manifest,source-registry}.yaml` and source/compatibility schemas; `validate-research.py`; refresh reports. `BoundedCollectorTests`, `ACQ-FAIL-001`, `ALLOWED_HOSTS`, `reject_unallowlisted`, `CACHE_ROOT`, and `cache_path` resolve. | P/W/D. Refresh reports self-classify as observed repository-history evidence, not normative upstream authority. |

### Excluded newly produced artifacts and unresolved plan assertions

The following are intentionally not counted as existing authority because they are planned outputs/interfaces absent from the current tree: `tools/phase1-bootstrap.py`; `01-29-SUMMARY.md` through `01-45-SUMMARY.md`; authority determinations/receipts; upstream acquisition queue/report; `validate-reviewed-acquisition`; `validate-authority-receipt`; `migrate-phase1-records.py`; v2 migration/schema fixtures and APIs; canonical recovery, package-conformance, and sandbox-run tools; snapshot/reader/recovery/publication APIs; closeout/terminal/security/registry/wheelhouse collectors and their tests; ASVS reference/applicability artifacts; reviewed-source loader/binding; seven-dimension classifier; and `.planning/research/upstreams/` cache.

Their absence is expected before authorized execution but makes the corresponding plan claims unresolved rather than verified. Existing repository-local items do not silently upgrade to immutable upstream protocol or published-package authority. Execution remains blocked until the current MEDIUM is incorporated into executable plan text or explicitly deferred/rejected, the resulting plan snapshot is reviewed, and the review converges.
