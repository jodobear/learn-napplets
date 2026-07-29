---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
current_phase: 01
current_phase_name: research-and-truth-baseline
status: blocked
stopped_at: Exact-commit review 341884f found 2 HIGH source-grounding defects; targeted snapshot repair/replan required before Plan 01-29 Task 1
last_updated: "2026-07-29T02:03:02Z"
last_activity: 2026-07-29
last_activity_desc: external review bound commit f8adcf6 and aggregate 24e34efc, passed all prior regressions, and found two absent committed-input defects
progress:
  total_phases: 1
  completed_phases: 0
  total_plans: 45
  completed_plans: 28
---

# Project State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-07-23)

**Core value:** Learners can accurately understand and exercise the boundary where focused, untrusted napplet code delegates dangerous or repetitive authority to a trusted host.
**Current focus:** Phase 01 — research-and-truth-baseline

## Current Position

Phase: 1 (research-and-truth-baseline) — BLOCKED ON 2 HIGH EXACT-COMMIT REVIEW FINDINGS
Plan: 28 of 45 executed; Plan 01-29 Task 1 remains unexecuted
Status: Prior reader/wheel/digest/receipt regressions pass, but active plans depend on canonical context/project and four upstream-refresh reports absent from reviewed commit
Last activity: 2026-07-29 — external Codex review reproduced all 45 plan hashes and found 2 HIGH/actionable committed-input defects

Progress: [██████░░░░] 62%

## Performance Metrics

**Velocity:**

- Total plans completed: 0
- Average duration: N/A
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| - | 0 | 0 | N/A |

**Recent Trend:**

- Last 5 plans: None
- Trend: N/A

**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 01 P01 | 45m | 3 tasks | 7 files |
| Phase 01 P02 | 25m | 2 tasks | 8 files |
| Phase 01 P03 | 8m | 2 tasks | 6 files |
| Phase 01 P04 | 14m | 2 tasks | 10 files |
| Phase 01 P05 | 289 | 2 tasks | 10 files |
| Phase 01 P06 | 10m | 2 tasks | 12 files |
| Phase 01 P07 | 8m | 1 tasks | 5 files |
| Phase 01 P20 | 12m | 2 tasks | 6 files |
| Phase 01 P26 | 175s | 2 tasks | 5 files |
| Phase 01 P08 | 309s | 1 tasks | 7 files |
| Phase 01 P09 | 20m | 2 tasks | 6 files |
| Phase 01 P10 | 748s | 3 tasks | 4 files |
| Phase 01 P11 | 888s | 2 tasks | 11 files |
| Phase 01 P12 | 880s | 2 tasks | 7 files |
| Phase 01 P13 | 634s | 2 tasks | 7 files |
| Phase 01 P14 | 6h 18m 46s | 3 tasks | 7 files |
| Phase 01-research-and-truth-baseline P15 | 710s | 3 tasks | 7 files |
| Phase 01 P17 | 1201s | 2 tasks | 7 files |
| Phase 01-research-and-truth-baseline P18 | 1224s | 3 tasks | 8 files |
| Phase 01 P19 | 13m | 3 tasks | 8 files |
| Phase 01 P16 | 18m 30s | 2 tasks | 10 files |
| Phase 01 P28 | 37m | 2 tasks | 8 files |
| Phase 01 P21 | 256s | 2 tasks | 4 files |
| Phase 01 P22 | 145s | 2 tasks | 4 files |
| Phase 01 P27 | 386s | 2 tasks | 7 files |
| Phase 01 P23 | 347s | 2 tasks | 6 files |
| Phase 01 P25 | 434s | 2 tasks | 15 files |
| Phase 01 P24 | 15m | 3 tasks | 5 files |

## Accumulated Context

### Decisions

Decisions are logged in `PROJECT.md` Key Decisions table. Current planning constraints:

- Source Phases 0–10 map in order to GSD Phases 1–11.
- No source-stage research evidence exists, no ADR is accepted, and no production application scaffold is authorized.
- Phase 1 requires deep plan-review convergence before research execution.
- ADR 0007 controls whether Phase 9 is executed, narrowed, or skipped; it cannot block the public-site sequence.
- [Phase ?]: Phase 1 research tooling uses project-operator-approved PyYAML 6.0.3, jsonschema 4.26.0, and Playwright 1.61.0 only in .research/phase1-tools.
- [Phase ?]: Phase 1 browser runner uses direct installed Google Chrome 150.0.7871.124 and Firefox 152.0.4; Playwright-managed browser downloads are not requested.
- [Phase ?]: Phase 1 verification and replay commands must use tools/phase1-python, which checks the recorded isolated interpreter version and SHA-256.
- [Phase ?]: Preserved source-pack records remain provisional collection seeds and cannot serve as current upstream proof.
- [Phase ?]: Evidence validation may prepare review work but cannot automatically verify a claim without dated reviewer approval.
- [Phase ?]: Conflicts retain parallel pinned normative and observed DRF sides rather than a forced winner.
- [Phase ?]: Compatibility baseline pins must match referenced source commit, path, and content digest.
- [Phase ?]: Pre-run spike contracts omit observations; completed spikes require measured, digest-pinned replay evidence.
- [Phase ?]: Automated validation prepares evidence but cannot replace dated human approval or accept an ADR.
- [Phase ?]: Spike impact fragments pin metadata, reports, sources, and measurements with SHA-256 before consolidation.
- [Phase ?]: Discovery pointers remain blocked until official immutable source records are collected.
- [Phase ?]: Project policy controls evidence handling but does not prove upstream protocol behavior.
- [Phase ?]: All mandatory drift checks remain blocked until official immutable upstream baselines are collected; archived planning questions never become protocol facts.
- [Phase ?]: Refresh comparison emits stable review work and preserves canonical evidence records for human interpretation.
- [Phase ?]: Unpinned ecosystem candidates remain blocked catalog records, not inferred protocol or implementation facts.
- [Phase ?]: napplet/web requires distinct public release and repository/public-export evidence before a consume, wrap, or avoid decision.
- [Phase ?]: Runtime dimensions are a source-acquisition checklist, not a selected teaching-host architecture.
- [Phase ?]: SPK-L uses deterministic local refresh fixtures to route stable review work while retaining canonical evidence history.
- [Phase ?]: All six audiences retain source, claim, drift, and open-question IDs rather than settling protocol behavior.
- [Phase ?]: Learn FIPS, MDN Learning, and The Odin Project are excluded until complete immutable comparator records exist.
- [Phase ?]: The first real-lab operation and teaching-host profile are blocked with a deterministic static fallback.
- [Phase ?]: Lesson index fixes all thirteen IDs and descriptive filenames while staged validation requires files only for present entries.
- [Phase ?]: LES-001 through LES-004 remain conceptual/static research packets until immutable evidence and human review support any runtime or protocol claim.
- [Phase ?]: SPK-A retains Candidate A as a proposed public-site-first workspace boundary model; ADR-0001 remains pending human review.
- [Phase ?]: Astro 7.1.3 is proposed ADR-0002 evidence only after five passing isolated fixture replays.
- [Phase ?]: VitePress 1.6.4 is blocked from a positive ADR-0002 recommendation until a reviewed accessibility/static-equivalent fixture resolves its repeated assertion failure.
- [Phase ?]: SPK-C remains blocked overall: Chromium passed five isolated samples, but direct-installed Firefox 152.0.4 could not launch under approved Playwright 1.61.0.
- [Phase ?]: SPK-C source bindings remain blocked policy inputs; browser fixture observations do not establish upstream protocol behavior.
- [Phase ?]: SPK-D records verified-loader feasibility as blocked until current immutable manifest/identity sources and reviewed verifier provenance exist; no cryptography is hand-rolled.
- [Phase ?]: Exact-byte and one-byte mutation replay is local fixture-integrity evidence only; it does not resolve protocol behavior or the Plan 01-11 Firefox blocker.
- [Phase ?]: SPK-E keeps one bounded fixture as the content-fact source and validates six representation outputs for exact provenance/status parity.
- [Phase ?]: SPK-E preserves exact canonical vocabulary values where canonical records provide no separate terminology, maturity, uncertainty, or status IDs.
- [Phase ?]: SPK-E retains generated outputs only in /tmp and commits digest-based replay evidence as proposed ADR-0004 input.
- [Phase ?]: Astro 7.1.3 and VitePress 1.6.4 were installed only after dated SPK-F-specific human approval.
- [Phase ?]: SPK-F is a blocked ADR-0007 evidence result because Firefox exited before Playwright attachment; no portable outcome is selected.
- [Phase ?]: SPK-B VitePress reduced-motion/static-equivalent evidence remains independently unresolved.
- [Phase ?]: SPK-G blocks CAND-NAPPLET-WEB-PACKAGE until an exact public release, root export, provenance, integrity, and immutable release/implementation baseline are collected and approved.
- [Phase ?]: SPK-G zero-operation replays are supply-chain blocker evidence only, never package conformance or protocol authority.
- [Phase ?]: SPK-I retains data-driven semantic SVG as a proposed static-first ADR-0006 baseline; no visual dependency or dynamic state controller was added.
- [Phase ?]: SPK-I remains blocked for cross-browser recommendation because direct-installed Firefox exited before Playwright attached; no launcher or configuration workaround was used.
- [Phase ?]: SPK-J proposes fixed tested variants as the default and controlled native textarea only for the declared bounded edit; no arbitrary learner code executes in trusted context.
- [Phase ?]: SPK-J does not select CodeMirror despite bounded Chromium success; CodeJar and cross-browser ADR-0009 evidence remain blocked.
- [Phase ?]: SPK-K Task 2 selected local-only on 2026-07-24; external deployment/publication remains scoped blocked evidence.
- [Phase ?]: SPK-K local replay uses digest-pinned static inspection and rollback with no listener, external command, target, account, or credential access.
- [Phase ?]: SPK-H retains SPK-C's opaque-origin srcdoc guest and sandbox=allow-scripts-only loading model.
- [Phase ?]: Chrome egress outcomes are fixture-specific observations; Firefox exits before Playwright attachment and blocks cross-browser recommendation without a workaround.
- [Phase ?]: A restrictive public-site CSP is proposed project policy only; OQ-EGRESS-NIP-001 and DRF-EGRESS-001 remain open pending immutable upstream evidence and review.
- [Phase ?]: All SPK-A through SPK-L reports are explicit no-impact or consolidated canonical evidence; raw report prose is not canonical authority.
- [Phase ?]: SPK-C/D/G/H outcomes remain blocked or materially uncertain; incompatible fragment stable IDs publish deterministic OQ-CONSOLIDATION review work instead of overwriting evidence.
- [Phase ?]: ADR 0001 carries the narrow public-site-first workspace boundary as a proposed review direction while retaining the broader alternative.
- [Phase ?]: ADR 0002 carries Astro 7.1.3 only as a proposed fixture-supported candidate and retains the VitePress reduced-motion/static-equivalent blocker.
- [Phase ?]: ADR 0003 treats local artifact assembly as non-production evidence and keeps any external deployment or publication behind new authorization.
- [Phase ?]: ADR 0004 proposes common structured-source parity as a Phase 2 contract constraint without authorizing a production renderer.
- [Phase ?]: ADR 0005–0008 remain proposed-only; the public static learning path is independent of optional portable and advanced capabilities.
- [Phase ?]: Semantic SVG is only a proposed later baseline; static diagram, transcript, and table remain the minimum safe path.
- [Phase ?]: Future protocol fixtures must traverse CLM-* to complete immutable SRC-* records and use explicit deterministic fakes.
- [Phase ?]: LES-005 through LES-009 remain deterministic conceptual simulations because no first real-lab operation or teaching-host profile is selected.
- [Phase ?]: Manifest and dTag identity terms remain linked to provisional policy claims and blocked canonical questions, not teaching rules.
- [Phase ?]: Host-mediated sibling composition has no observed canonical result and remains a conceptual comparison topic.
- [Phase ?]: ADR-0009 retains fixed variants and bounded native text editing as a proposed least-authority direction; CodeMirror is unselected and CodeJar remains blocked.
- [Phase ?]: ADR-0010 keeps public-package admission and updates blocked until release, root-export, provenance, integrity, implementation, compatibility, and review evidence are complete.
- [Phase ?]: ADR-0011 proposes targeted D-20/D-36 source-refresh review work that retains old identity and never auto-changes claims, ADRs, or approvals.
- [Phase ?]: The static public-site path remains a proposed post-Phase-2 direction; host, package, portable, external-delivery, and complex interactive capabilities remain deferred.
- [Phase ?]: The lesson index is a complete, ordered thirteen-entry contract rather than a directory convention.
- [Phase ?]: Build, runtime, package, deployment, and contribution content remains deterministic conceptual research until canonical evidence and human review resolve its blockers.
- [Phase ?]: Phase 1 verification is `gaps_found` (1/5 must-haves verified); focused gap closure, Nyquist validation, security review, and fresh passing verification are required before Phase 2.
- [Phase ?]: All six dated scoped role approvals retain Firefox, VitePress, package, manifest/identity/verifier, delivery, portable, editor, dynamic-diagram, and freshness blockers or deferrals.
- [Phase ?]: ADR 0001–0011 remain proposed; no residual risk, CSP behavior, teaching-host architecture, deployment, release, publication, or external action is accepted.
- [Phase ?]: Plan 01-29 execution requires exactly one independent authorization record plus a sorted one-to-one SHA-256 map for every active plan file; aggregate-only binding and stale fixed plan counts are insufficient.
- [Phase ?]: Exact-commit review `ea45866` of `fbaa886` found 3 HIGH and 1 MEDIUM actionable defects: installed-wheel provenance, mixed-generation canonical reads, terminal digest self-reference, and package receipt overwrite/revalidation.
- [Phase ?]: Review-mode replanning incorporated all four defects, split toolchain/source-ingress scope across Plans 01-29/01-44/01-45, and propagated transactional-reader contracts through Plans 01-36/01-42/01-43.
- [Phase ?]: Independent GSD plan verification passed all 45 revised plans, 92 executable tasks, all six Phase 1 requirement IDs, the dependency DAG, and all 39 tracked context decisions; this does not replace fresh external review binding.
- [Phase ?]: The revised 45-plan snapshot totals 609276 bytes with aggregate SHA-256 `122c58add51ebb1030cb9e3544c9915c386cb8a408aee7adb2bfd7112b50ccd5` using lexical basename + NUL + file bytes + NUL.
- [Phase ?]: Exact-commit review of `7c151cc` independently reproduced that binding, confirmed the wheelhouse provenance, terminal digest, receipt preservation, and Plan 01-29/01-44/01-45 split repairs, and found one remaining HIGH Plan 01-35 transactional-reader propagation defect.
- [Phase ?]: Plan 01-35 must depend on Plan 01-42, consume only the registered in-memory canonical snapshot/index without reopening live paths, carry an overlap/open-instrumentation regression, and be included in Plan 01-42 future-reader propagation.
- [Phase ?]: Targeted replanning now enforces that contract across Plans 01-35 and 01-42; independent GSD verification passed with no blocker or warning.
- [Phase ?]: The corrected 45-plan snapshot totals 616221 bytes with aggregate SHA-256 `24e34efc006adc9b547d46e6e1406ba4ed042b071fdeeba5e2f658bd50e6d136` using lexical basename + NUL + file bytes + NUL.
- [Phase ?]: Exact-commit external review `341884f` binds plan commit `f8adcf6` and independently reproduces 45/45 file hashes, 616221 bytes, and aggregate `24e34efc006adc9b547d46e6e1406ba4ed042b071fdeeba5e2f658bd50e6d136`.
- [Phase ?]: All prior wheelhouse, transactional-reader, terminal-digest, receipt-preservation, and Plan 01-29/01-44/01-45 ownership regressions pass.
- [Phase ?]: Review found 2 HIGH/actionable source-grounding defects: Plan 01-45 depends on four upstream-refresh reports absent from the reviewed commit, and active gap plans require canonical `01-CONTEXT.md`/`.planning/PROJECT.md` absent from that commit.
- [Phase ?]: OpenCode returned no assistant text, Ollama produced an ungrounded simulated-execution response, and llama.cpp rejected the full prompt for context overflow; only Codex contributes authorization weight.

### Pending Todos

- Targeted repair: commit/digest-bind canonical `01-CONTEXT.md`, `.planning/PROJECT.md`, and the four upstream-refresh reports, or revise every affected read-first/source-selection contract to committed authoritative replacements.
- Rerun independent plan checking, commit revised snapshot, then rerun exact-commit external review against the new sorted 45-entry SHA-256 map.
- Resume `/gsd-execute-phase 1` only after the bound review records 0 HIGH / 0 actionable.
- Complete Nyquist validation, security review, and fresh independent re-verification after execution.

### Blockers/Concerns

- Exact-review record `341884f` binds plan commit `f8adcf6` and aggregate `24e34efc006adc9b547d46e6e1406ba4ed042b071fdeeba5e2f658bd50e6d136`, but records 2 HIGH / 2 actionable findings and does not authorize execution.
- Plan 01-45's four upstream-refresh report inputs and active gap plans' canonical `01-CONTEXT.md`/`.planning/PROJECT.md` inputs are absent from the reviewed commit; similarly named mutable working-tree files cannot satisfy exact-commit source grounding.
- Execution is blocked before Plan 01-29 Task 1 until targeted repair and a fresh independent exact-commit review bind all active plans and record 0 HIGH / 0 actionable.
- Prior ownership/publication corrections remain resolved: receipt CLI ownership, shared publisher CLI ownership, real five-file observed-refresh publication, and Plan 01-36→01-43→01-37 ordering remain explicit in the revised dependency graph.
- Plans otherwise preserve automated dependency locking, task-local boundary regressions, direct receipt validation, validator ownership, staged atomic publication, extensible ASVS findings, and one-user/multi-role sign-offs.
- Phase 1 verification remains `gaps_found` with 1/5 must-haves verified; see `01-VERIFICATION.md` and `01-REVIEW.md`.
- Evidence validation remains fail-open at trust-critical boundaries including citation matching, preflight parsing, replay execution, path confinement, canonical publication, evidence classification, dependency integrity, and duplicate refresh handling.
- `01-VALIDATION.md` remains draft/noncompliant, and no Phase 1 security review artifact exists.
- Upstream-sensitive terms and protocol behavior must remain labeled as uncertain until immutable-source evidence is reviewed.
- Do not create a production scaffold before Phase 1 and Phase 2 gates pass.
- SPK-C Firefox 152.0.4 exited before approved Playwright 1.61.0 attached; no cross-browser fixture evidence exists for ADR-0005.
- SPK-D verified-loader feasibility is blocked: immutable current manifest/identity source records and reviewed signature/blob/aggregate/loader verifier provenance are unavailable; ADR-0005 and ADR-0008 receive proposed blocked evidence only.
- SPK-F cross-browser feasibility is blocked: direct-installed Firefox 152.0.4 exited before approved Playwright 1.61.0 attached; preserve SPK-B VitePress accessibility evidence.
- SPK-I: Direct-installed Firefox 152.0.4 exits before approved Playwright 1.61.0 attaches; Chrome passed five static SVG samples, but ADR-0006 cannot receive a positive cross-browser recommendation.

## Deferred Items

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| Optional portable target | Execute only if ADR 0007 authorizes it | Conditional | 2026-07-23 |

## Session Continuity

Last session: 2026-07-29
Stopped at: Exact-commit review `341884f` found 2 HIGH/actionable absent committed-input defects
Resume file: `.planning/phases/01-research-and-truth-baseline/01-REVIEWS.md` — run targeted `/gsd-plan-phase 1 --reviews` repair before another exact review
