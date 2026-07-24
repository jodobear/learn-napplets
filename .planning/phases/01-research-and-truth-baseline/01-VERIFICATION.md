---
phase: 01-research-and-truth-baseline
verified: 2026-07-24T12:59:24Z
status: gaps_found
score: 1/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
next_action: "Create and execute a focused Phase 1 gap-closure plan, then re-run verification; do not transition to Phase 2 or authorize production work."
next_command: "/gsd-plan-phase 1 --gaps"
gaps:
  - truth: "Blocking protocol-sensitive claim citations are fail-closed and resolve only to complete immutable source provenance."
    status: failed
    reason: "The claim-citation regex uses literal \\b, so GATE016–GATE018 silently skip ordinary CLM-* citations."
    artifacts:
      - path: tools/validate-planning.py
        issue: "Line 144 cannot match a normal word-boundary citation."
    missing:
      - "Correct the regex and add dangling/incomplete citation regression tests."
  - truth: "Completion and execution gates reject non-converged review, unresolved HIGH findings, or use of an unapproved validation environment."
    status: failed
    reason: "Preflight accepts arbitrary non-error reviewer text and treats any occurrence of 'none' as no HIGH; completion invokes validators and lesson tests through sys.executable."
    artifacts:
      - path: tools/validate-planning.py
        issue: "Lines 46–81 and 96–102/211–218 are fail-open and bypass tools/phase1-python."
    missing:
      - "Strict bounded convergence/HIGH parsing and mandatory wrapper invocation for every Phase 1 subprocess."
  - truth: "Each mandatory spike has reproducible retained raw evidence and an allowlisted replay that cannot execute arbitrary local commands."
    status: failed
    reason: "Complete-spike validation only requires nonempty declarations; replay executes manifest-provided command strings without an allowlist."
    artifacts:
      - path: tools/validate-research.py
        issue: "Lines 264–303 do not resolve evidence paths/digests; lines 905–965 execute arbitrary replayCommand values."
    missing:
      - "Safely resolve and hash every retained evidence file, bind outputDigest to it, and derive or strict-allowlist replay commands."
  - truth: "Consolidation preserves canonical evidence integrity and separates normative upstream evidence from local observation."
    status: failed
    reason: "Impact-fragment links accept absolute/traversing paths and noncanonical sources; consolidation publishes six targets sequentially and copies a local observation to both normative and observed sides."
    artifacts:
      - path: tools/validate-research.py
        issue: "Lines 463–544 lack path confinement/canonical-source binding; lines 660–688 conflate evidence classes; lines 1022–1035 are not crash-atomic."
    missing:
      - "Constrained canonical path resolution, distinct observed-local evidence model, and durable single-pointer or journaled atomic publication."
  - truth: "Refresh and approved-toolchain evidence are dependency-integrity protected and deterministic per source."
    status: failed
    reason: "The wrapper hashes only the interpreter, requirements are not hash locked, and duplicate contradictory refresh observations produce multiple results."
    artifacts:
      - path: tools/phase1-python
        issue: "Only executable version/hash are checked."
      - path: requirements-phase1-tools.txt
        issue: "Top-level pins have neither hashes nor transitive closure."
      - path: tools/refresh-sources.py
        issue: "Lines 155–157 process duplicate source observations independently."
    missing:
      - "Fully hash-locked dependency closure with verification and one-source/one-observation conflict handling."
  - truth: "The mandatory Phase 1 validation contract has completed and records current evidence rather than a pending Wave 0 template."
    status: failed
    reason: "01-VALIDATION.md still declares status draft, nyquist_compliant false, wave_0_complete false, every task pending, and Approval pending despite claimed closeout."
    artifacts:
      - path: .planning/phases/01-research-and-truth-baseline/01-VALIDATION.md
        issue: "Current validation artifact contradicts completion readiness."
    missing:
      - "Complete or explicitly reconcile the validation contract only after integrity fixes and fresh evidence."
---

# Phase 01: Research and Truth Baseline Verification Report

**Phase Goal:** Decision makers and maintainers can rely on a dated, immutable-source evidence baseline to choose the first safe teaching scope and architecture without presenting unsettled upstream behavior as fact.

**Verified:** 2026-07-24T12:59:24Z  
**Status:** gaps_found  
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Every blocking protocol-sensitive claim is traceable through a fail-closed immutable-source provenance gate. | FAILED | `validate-planning.py:144` uses `\\b` in a raw regex. Targeted reproduction found zero matches for `CLM-POLICY-001`; the same expression with `\b` found the claim. GATE016–GATE018 therefore do not run for normal citations. |
| 2 | Volatile claims preserve conflicts, uncertainty, impact, and refresh state without presenting local observations as settled/normative fact. | FAILED | Canonical records exist, but `new_drift_record` (`validate-research.py:660–688`) copies a local observation into both `normative` and `observed`. `drift-register.yaml:270–299` contains the resulting identical sides with planning-archive/project-policy classification. |
| 3 | A compatibility matrix enables review across selected protocol sources, packages, runtimes, examples, and current work before architecture is proposed. | FAILED | `compatibility-matrix.yaml` has category fields, but its only source baseline is `SRC-POLICY-001/002` (planning archive/project policy), not selected immutable protocol/package/runtime evidence. Its integrity gate is also bypassable through the citation and consolidation defects. |
| 4 | Each mandatory spike has reproducible retained measurements before its recommendation is considered. | FAILED | Full validation passed, but completed spikes need only nonempty `rawOutputDigests`/`evidenceLinks` (`validate-research.py:264–303). The passing fixture in `test_spikes.py:144–164` declares a nonexistent `raw.txt`. Replay accepts manifest commands without an executable/argument allowlist. |
| 5 | The owner can inspect an explicit safe-scope blocker/fallback while all ADRs remain proposed and no production scaffold exists. | VERIFIED | `adr-handoff.yaml:5–9` limits use to Phase 2 contract definition and forbids production scaffolding; all 11 handoff ADRs are `proposed`; no `package.json`, `pnpm-workspace.yaml`, `src/`, `apps/`, or `packages/` production marker was found. This narrow fact does not cure the integrity failures above. |

**Score:** 1/5 truths verified (0 present, behavior-unverified)

## Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `.planning/research/source-registry.yaml`, `claims.yaml`, catalogs, lesson packets | Source/claim baseline and teaching evidence | PRESENT BUT NOT TRUSTWORTHY | Files are substantive and referenced by validators, but citation traversal can silently skip claims. |
| `.planning/research/compatibility-matrix.yaml`, `drift-register.yaml`, `open-questions.yaml` | Explicit compatibility, uncertainty, and conflict records | PRESENT BUT NOT TRUSTWORTHY | Records exist; fragment ingestion permits external evidence and synthesized drift makes local observations normative. |
| `.planning/spikes/*/{metadata,measurements,report}` and `replay-manifest.yaml` | Retained, reproducible mandatory-spike evidence | PRESENT BUT NOT TRUSTWORTHY | Reports and metadata exist, yet raw evidence/output digest resolution and replay command allowlisting are absent. |
| `tools/validate-planning.py`, `tools/validate-research.py`, `tools/phase1-python` | Fail-closed evidence and closeout enforcement | STUB AT SECURITY BOUNDARY | Substantive code is wired into closeout, but the reviewed paths are fail-open or bypass the approved wrapper. |
| `.planning/research/phase-governance.yaml` | Owner/approver/exit-evidence/governance record | PARTIAL | Fields and scoped signoffs exist, but `verification.gsdState: passed` relies on unsound completion checks. |
| `01-VALIDATION.md` | Current Nyquist validation contract | STALE / INCOMPLETE | Frontmatter remains `draft`, `nyquist_compliant: false`, `wave_0_complete: false`; all task rows remain pending. |

## Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| Citation-bearing catalogs, lessons, ADRs | `claims.yaml` → `source-registry.yaml` | `phase1_citation_and_inventory_errors()` | NOT WIRED SAFELY | Enumeration is broken by the escaped word-boundary regex. |
| Completion gate | approved toolchain | `phase1_command_errors()` and lesson test subprocess | NOT WIRED | Uses `sys.executable`, not `tools/phase1-python`; wrapper hash/environment enforcement is bypassed. |
| Spike metadata | retained raw output and replay output | `validate_spike(..., complete)` | NOT WIRED | Declarations are only checked for truthiness; neither file resolution nor hash binding occurs. |
| Replay manifest | validated spike command | `replay_spikes()` | UNSAFE | Manifest `replayCommand` is passed to `shlex.split` and `subprocess.run` without an allowlist. |
| Impact fragment | canonical `.planning` inputs / source registry | `validate_impact_fragment()` | NOT WIRED SAFELY | Absolute paths override `planning_root`, traversal is allowed, and source links are not tied to the declared source's canonical record. |
| Consolidation staging | canonical evidence generation | `consolidate_spike_impacts()` | PARTIAL | Staging and lock exist, but six independent `os.replace` operations leave a mixed generation after process crash. |

## Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces real data | Status |
|---|---|---|---|---|
| Citation gate | `claim_id` matches | Catalog/lesson/ADR text | No — ordinary citations are omitted by regex | DISCONNECTED |
| Complete-spike gate | `rawOutputDigests`, `evidenceLinks`, `replayResult.outputDigest` | Metadata declarations | No — no retained-file/digest resolution | HOLLOW |
| Replay runner | `replayCommand` | YAML manifest | Yes, but untrusted arbitrary command | UNSAFE |
| Consolidated drift | `normative` / `observed` | Impact fragment plus source record | Misclassified — one local observation is copied to both | MISCLASSIFIED |

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Full Phase 1 deterministic suite and completion gate | `tools/phase1-python -m unittest discover -s tests/phase1 && tools/phase1-python tools/validate-planning.py --phase-1-complete` | 46 tests passed; completion reported 0 errors/0 warnings | PASS, but insufficient: tests encode several defects below. |
| Execution preflight rejects nonconverged review/HIGH | Targeted `phase1_execution_preflight_errors()` with arbitrary reviewer and `None resolved; HIGH-001 remains open.` | Returned `[]` | FAIL (CR-02 confirmed) |
| Citation gate enumerates normal claim citation | Targeted regex comparison in approved wrapper | Flawed regex found `[]`; correct boundary found `['CLM-POLICY-001']` | FAIL (CR-01 confirmed) |
| Replay rejects arbitrary executable | Targeted temporary 12-entry manifest, each `replayCommand: /usr/bin/true` | `replay_spikes()` returned `[]` and executed the command | FAIL (CR-06 confirmed) |
| Refresh canonicalizes duplicate source observation | Targeted `refresh_souces.compare()` twice for `SRC-1` with contradictory pins | Two independent `changed` results returned | FAIL (WR-03 confirmed) |

## Probe Execution

| Probe | Command | Result | Status |
|---|---|---|---|
| Phase replay manifest | Invoked by `tools/phase1-python tools/validate-planning.py --phase-1-complete` | Exit 0 | EXECUTED, NOT TRUSTWORTHY — replay validator allows arbitrary command strings and does not prove retained raw-output binding. |

## Requirements Coverage

| Requirement | Source Plans | Description | Status | Evidence |
|---|---|---|---|---|
| EVID-01 | 01-02, 01-05, 01-08, 01-24, 01-25, 01-27 | Immutable source-to-claim traceability | BLOCKED | CR-01 and CR-05 make source/claim provenance bypassable; only archive/project-policy baseline records are present. |
| EVID-02 | 01-03, 01-05, 01-06, 01-08, 01-20, 01-23, 01-24, 01-25, 01-26, 01-27 | Conflict, uncertainty, drift, impact, and refresh visibility | BLOCKED | Drift/open-question files exist, but CR-08 collapses normative and observed classification; WR-03 permits contradictory refresh records. |
| EVID-03 | 01-03, 01-06, 01-07, 01-21–01-24, 01-26–01-28 | Compatibility review across source/package/runtime/example/current work | BLOCKED | Matrix exists but no qualified current upstream baseline exists, and CR-05 permits noncanonical external evidence. |
| EVID-04 | 01-01, 01-04, 01-09–01-20, 01-24, 01-28 | Reviewable reproducible mandatory-spike evidence | BLOCKED | CR-04, CR-06, CR-07, and WR-01 invalidate retained-evidence, replay safety, and publication-integrity assurance. |
| OPER-01 | 01-03, 01-04, 01-06, 01-20, 01-23, 01-24, 01-26, 01-28 | Detect drift and create review work without silent rewrite | BLOCKED | Refresh does not rewrite claim prose, but WR-03 makes one-source/one-observation review routing nondeterministic. |
| OPER-03 | 01-01–01-04, 01-21–01-28 and others | Owner/approver, exit evidence, GSD verification, and requirement traceability | BLOCKED | Governance/ADR handoff records exist, but the recorded passed validation state rests on bypassable gates; current `01-VALIDATION.md` remains draft. |

All six specified Phase 1 requirement IDs appear in PLAN frontmatter. No orphaned Phase 1 requirement was found in `REQUIREMENTS.md`.

## Review-Finding Adjudication

| Finding | Verdict | Concrete evidence |
|---|---|---|
| CR-01 | CONFIRMED | Regex and targeted match reproduction above. |
| CR-02 | CONFIRMED | Targeted nonconverged/HIGH input returned no errors; parser requires neither `CONVERGED; HIGH=0; actionable=0` nor exact `None.`. |
| CR-03 | CONFIRMED | `validate-planning.py:97,213` use `sys.executable`; wrapper is not in the completion subprocess path. |
| CR-04 | CONFIRMED | `validate_spike` checks only nonempty fields; `test_spikes.py:144–164` passes without creating declared `raw.txt`. |
| CR-05 | CONFIRMED | `planning_root / supplied_path` at lines 475, 476, 501, 511, 532 accepts absolute paths; no resolved-root confinement or canonical source-record path equality is checked. |
| CR-06 | CONFIRMED | Targeted `/usr/bin/true` manifest completed; `subprocess.run(shlex.split(command))` executes manifest input. |
| CR-07 | CONFIRMED | Lines 1022–1035 replace six targets serially. In-process rollback cannot survive crash/kill/power loss between replacements. |
| CR-08 | CONFIRMED | `new_drift_record` assigns `normative: side` and `observed: side.copy()`; canonical `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` exhibits it. |
| CR-09 | CONFIRMED | Wrapper validates only interpreter path/version/SHA; requirements have no distribution hashes or dependency closure. |
| WR-01 | CONFIRMED | Passing fixture declares `raw.txt` with placeholder digest but does not create it. |
| WR-02 | CONFIRMED | `test_evidence.py:94–99` writes `.planning/research/reports/validation.md` in the canonical working tree. |
| WR-03 | CONFIRMED | Two conflicting source observations yield two review results rather than a rejected/canonical ambiguous result. |

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `tools/validate-planning.py` | 144 | Incorrect escaped regex disables provenance checks | BLOCKER | Citation evidence can evade source validation. |
| `tools/validate-planning.py` | 97, 213 | Ambient interpreter subprocesses | BLOCKER | Approved toolchain gate is bypassed during certification. |
| `tools/validate-research.py` | 952–958 | Manifest-controlled executable invocation | BLOCKER | Arbitrary local command execution. |
| `tools/validate-research.py` | 1024–1033 | Sequential multi-file publication | BLOCKER | Crash can permanently mix canonical generations. |
| `tests/phase1/test_evidence.py` | 94–99 | Test mutates canonical output | WARNING | Dirty/racy canonical planning evidence. |
| `.planning/phases/01-research-and-truth-baseline/01-VALIDATION.md` | 5–8, 42–85 | Stale draft/pending validation contract | WARNING | Contradicts claimed completed validation. |

No unreferenced `TBD`, `FIXME`, or `XXX` debt marker was found in the reviewed Phase 1 tools/tests.

## Security and Human Follow-Up

`workflow.security_enforcement` is enabled, but `.planning/phases/01-research-and-truth-baseline/01-SECURITY.md` does not exist. It is not listed as a required Phase 1 artifact in the current plan/gate inventory, so absence alone is not an independently specified artifact failure. It is nonetheless a required follow-up before any transition because CR-05, CR-06, CR-07, and CR-09 are security-relevant and no dedicated security assessment records their resolution or residual-risk decision. It cannot be used to accept or waive these defects.

After automated gap closure, a project owner/security reviewer must re-check that the repaired closeout: (1) only executes fixed allowlisted replay commands, (2) rejects missing/altered raw evidence and path escapes, (3) cannot publish a mixed generation after forced interruption/recovery, (4) reports every cited CLM provenance failure, and (5) retains the scoped human closeout only for Phase 2 contract readiness. ADRs must remain proposed; no production scaffold, deployment, release, external action, residual-risk acceptance, or transition is authorized by this report.

## Gaps Summary

The visible evidence records, proposed ADR handoff, scoped no-scaffold restriction, and test suite are substantive. They do not establish the phase goal because the mechanisms that certify immutable provenance, reproducibility, trusted execution, canonical publication, and evidence classification are demonstrably bypassable. The green 46-test suite and zero-error completion command are not sufficient evidence: the review findings are reproduced against the actual implementation, and two tests explicitly encode the unsafe behavior.

No later roadmap phase specifically commits to repairing Phase 1 evidence-validator, replay, consolidation, or dependency-integrity defects. These are not deferred items. They are Phase 1 closure gaps.

---

_Verified: 2026-07-24T12:59:24Z_  
_Verifier: Claude (gsd-verifier)_
