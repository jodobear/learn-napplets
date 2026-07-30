---
phase: 01-research-and-truth-baseline
verified: 2026-07-30T23:28:50Z
status: gaps_found
score: "0/6 specified requirements verified"
next_action: "Create focused Phase 1 gap-closure plans for the current evidence-tooling trust-boundary failures, execute them, then independently re-verify. Do not transition to Phase 2."
next_command: "/gsd-plan-phase 1 --gaps"
requirements:
  EVID-01:
    status: failed
    reason: "Repository-confinement validation accepts an external .research/upstreams root, so source collection cannot be relied on as checkout-confined evidence handling."
  EVID-02:
    status: failed
    reason: "New drift synthesis can collapse a local observation into identical normative and observed sides, contrary to the semantic drift contract."
  EVID-03:
    status: failed
    reason: "The compatibility baseline is blocked in all seven substantive dimensions and has no qualified protocol/package/runtime/example/current-work baseline."
  EVID-04:
    status: failed
    reason: "Spike evidence publication/retention paths are not crash-atomic and one retained-bundle path follows predictable temporary-file symlinks."
  OPER-01:
    status: failed
    reason: "Unexpected transaction artifacts can make canonical readers retry indefinitely; refresh locks can remain permanently stale after abnormal termination."
  OPER-03:
    status: failed
    reason: "Although plan/role/traceability artifacts exist, the recorded passed verification state relies on tooling with unremediated trust-boundary defects."
gaps:
  - truth: "Maintainers can rely on repository-confined immutable source acquisition."
    status: failed
    reason: "The cache-root validator accepts /tmp/.research/upstreams and collection subsequently writes fetched bytes under that external root."
    artifacts:
      - path: "tools/acquire-sources.py"
        issue: "_confined_cache_root validates only the last two path components."
    missing:
      - "Require the resolved cache root to equal the repository CACHE_ROOT or be constrained below the repository root; reject symlinked/external roots."
  - truth: "Canonical evidence is always published and read as one durable generation."
    status: failed
    reason: "Consolidation replaces six canonical files sequentially; malformed transaction artifacts cause canonical readers to retry forever."
    artifacts:
      - path: "tools/validate-research.py"
        issue: "consolidate_spike_impacts uses sequential os.replace calls instead of the journaled publisher."
      - path: "tools/canonical-recovery.py"
        issue: "_recover_locked ignores unexpected transaction entries that read_canonical_snapshot then retries indefinitely."
    missing:
      - "Route consolidation through journaled generation publication and fail closed on every unexpected transaction-directory entry."
  - truth: "Volatile local observations remain distinct from normative upstream evidence."
    status: failed
    reason: "new_drift_record duplicates the same source-derived side as normative and observed even though validate_drift rejects identical identities."
    artifacts:
      - path: "tools/validate-research.py"
        issue: "new_drift_record assigns normative: side and observed: side.copy()."
    missing:
      - "Emit the blocked observed-local shape with null normative side, or require two genuinely distinct pinned upstream sides before publication."
  - truth: "A verified SPK-G operation is sandboxed, accepts the declared scoped package, and retains evidence safely."
    status: failed
    reason: "The operation runner receives bare npm argv, @napplet/web is rejected by slash filtering, and retained output uses predictable temporary paths plus sequential replacement."
    artifacts:
      - path: "tools/measure-package-conformance.py"
        issue: "run_spk_g does not construct the declared sandbox argv; fixed_operation rejects scoped names; retain_validated_bundle follows temporary symlinks and is non-atomic."
    missing:
      - "Pass only a constructed sandbox command to the runner, validate scoped npm names safely, and use private no-follow staging plus journaled multi-file publication."
  - truth: "Drift/refresh maintenance remains available and deterministic after abnormal conditions."
    status: failed
    reason: "A stale O_EXCL refresh lock blocks all subsequent refreshes; migration also mutates caller-owned nested input structures."
    artifacts:
      - path: "tools/refresh-sources.py"
        issue: "Persistent lock has no liveness or stale-lock recovery."
      - path: "tools/migrate-phase1-records.py"
        issue: "Shallow copy leaves nested impacts lists caller-owned and sorted in place."
    missing:
      - "Use process-lifetime advisory locking or safe stale-lock reclamation, and deep-copy migration input before canonicalization."
retained_boundary:
  phase_2_transition: not_authorized
  production_scaffold: prohibited
  adr_acceptance: not_authorized
  package_admission: not_authorized
  release_or_external_action: not_authorized
---

# Phase 01: Research and Truth Baseline — Final Verification

**Phase Goal:** Maintainers can rely on dated immutable-source evidence to choose safe teaching scope and architecture without presenting unsettled behavior as fact.

**Verified:** 2026-07-30T23:28:50Z  
**Status:** `gaps_found`  
**Score:** 0/6 specified requirements verified  
**Historical initial verification:** Preserved byte-for-byte at `/workspace/projects/learn-napplets/.planning/phases/01-research-and-truth-baseline/01-VERIFICATION.md` (SHA-256 `ecc85cc7b0cefd958ea6f30c44f6f5f5f4915ba51d650978eab5498aeabf4b8f`).

## Final Verdict

**Phase goal not achieved.** Phase 1 has substantive structured artifacts and intentionally retains unresolved upstream behavior as blocked. However, maintainers cannot safely *rely* on the baseline: current source-acquisition, canonical-publication/recovery, drift-synthesis, and future SPK-G evidence paths contain reproduced trust-boundary failures.

The 2026-07-31 code review's seven critical findings remain current defects. Earlier passing validation, security, and terminal-attestation records do not resolve them: they predate the current review and exercise the older CR/WR remediation register rather than these newly found paths. The identifier reuse between the old security CR/WR register and the current review's `CR-*` findings makes that distinction especially important.

## Goal-Backward Assessment

| Observable truth | Status | Evidence |
|---|---|---|
| Blocking protocol-sensitive claims can be relied on as immutable-source evidence. | FAILED | `tools/acquire-sources.py:190-194` accepts an external cache root; source registry has only 3 records (2 project-policy, 1 observed implementation) and no verified claim. |
| Volatile claims preserve uncertainty and do not promote local observations to settled/normative fact. | FAILED | `tools/validate-research.py:1139-1168` builds identical normative/observed records; direct reproduction returned `identical_sides=True`. |
| Compatibility can be reviewed across protocol, package, runtime, examples, and current work before architecture is proposed. | FAILED | `.planning/research/compatibility-matrix.yaml` has all seven substantive dimensions blocked and `baselineEligibility.status: blocked`; its source baseline is project-policy/archive material. |
| Mandatory spike evidence is durably reproducible before recommendations are considered. | FAILED | `consolidate_spike_impacts()` uses sequential canonical replacement; SPK-G retained evidence replacement is non-atomic and follows predictable temporary symlinks. |
| Drift can be detected and review work created without silently corrupting or indefinitely blocking the evidence baseline. | FAILED | Canonical reader loops on unexpected transaction artifacts; refresh locks have no stale-lock recovery. |
| Phase roles, exit evidence, verification state, and requirement traceability accurately represent the phase. | FAILED | All 45 plans/summaries declare completion and the governance record says passed, but current unremediated trust-boundary defects invalidate that verification state. |

## Requirement Accounting

| Requirement | Status | Evidence |
|---|---|---|
| EVID-01 | FAILED | Direct wrapper reproduction: `_confined_cache_root(Path('/tmp/.research/upstreams'))` returned `/tmp/.research/upstreams`. `collect_immutable_candidate()` then writes under that root. |
| EVID-02 | FAILED | Direct reproduction of `new_drift_record()` emitted equal normative and observed sides, while `validate_drift()` at `tools/validate-research.py:558-560` explicitly rejects identical source identities. |
| EVID-03 | FAILED | Compatibility matrix is structurally present but blocked in every substantive dimension; no qualified normative protocol, package artifact, runtime, example/fixture, current-work, or conformance evidence is available. |
| EVID-04 | FAILED | All 12 spike artifact groups and replay manifest entries exist, but their consolidation/retention mechanisms cannot guarantee durable coherent evidence under interruption or hostile temporary paths. |
| OPER-01 | FAILED | An isolated malformed-transaction reproduction made `read_canonical_snapshot()` spin until `timeout` returned exit 124. Refresh's persistent `O_EXCL` lock can remain stale indefinitely. |
| OPER-03 | FAILED | Requirement IDs appear across all 45 plan frontmatters and governance artifacts exist, but a terminal passed state cannot be trusted while its evidence mechanics have current critical defects. |

All six specified requirement IDs are claimed by Phase 1 plans. No orphaned Phase 1 requirement was found in `/workspace/projects/learn-napplets/.planning/REQUIREMENTS.md`. No later roadmap phase specifically owns repair of these Phase 1 evidence-validator and publication defects; none are deferred.

## Reproduced Critical Defects

1. **External source-acquisition cache root — BLOCKER**  
   `/workspace/projects/learn-napplets/tools/acquire-sources.py:190-194` accepts any resolved path ending in `.research/upstreams`. Direct reproduction accepted `/tmp/.research/upstreams`.

2. **Non-atomic canonical consolidation — BLOCKER**  
   `/workspace/projects/learn-napplets/tools/validate-research.py:1529-1542` replaces six canonical targets serially rather than using the journaled publisher. A crash/kill between replacements leaves a mixed generation.

3. **Local drift observation copied into normative side — BLOCKER**  
   `/workspace/projects/learn-napplets/tools/validate-research.py:1139-1168` assigns `normative: side` and `observed: side.copy()`. Direct reproduction yielded identical sides even though the semantic validator forbids them.

4. **Canonical reader retry denial of service — BLOCKER**  
   `/workspace/projects/learn-napplets/tools/canonical-recovery.py:233-324` ignores unexpected transaction-directory files during recovery but considers them during reads. An isolated reproduction required timeout termination: `timeout_exit=124`.

5. **SPK-G runner is given unsandboxed npm argv — BLOCKER**  
   `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:200-212` verifies a sandbox contract but sends bare `npm install` argv to an injected `operation_runner`, without constructing the declared sandbox command.

6. **SPK-G rejects its intended scoped target — BLOCKER**  
   `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:171-176` rejects all package names containing `/`. Direct invocation for `@napplet/web` raised `ReceiptValidationError`.

7. **SPK-G retained-bundle write is symlink-following and non-atomic — BLOCKER**  
   `/workspace/projects/learn-napplets/tools/measure-package-conformance.py:215-237` writes predictable `.<target>.spk-g.tmp` files, then replaces targets serially. An isolated symlink reproduction changed both the intended target and an external file to `b'new'`.

## Confirmed Warnings

| Finding | Evidence | Impact |
|---|---|---|
| Excluded ingress regression | `tests/phase1/test_evidence.py:154` and `:171` define `BoundedCollectorTests` twice. Verbose discovery did not list `test_collector_rejects_non_allowlisted_url_without_writing`. | A source-ingress rejection test is silently excluded. |
| Caller-owned migration input is mutated | Direct reproduction of `migrate_drift_v1_to_v2()` returned `input_mutated=True`; nested impacts were sorted in the input. | Migration violates copy semantics and can alter upstream caller state. |
| Refresh lock can become permanently stale | `tools/refresh-sources.py:162-174,250-256` uses a persistent `O_EXCL` lock removed only on normal process completion. | Abnormal exit can indefinitely block source refresh review work. |

## Behavioral and Integrity Checks

| Check | Result | Assessment |
|---|---|---|
| `tools/phase1-python -m unittest discover -s tests/phase1 -v` | 140 tests passed in 82.304 seconds. | PASS, but insufficient: the current critical failure paths are not covered. |
| `tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/independent-phase1-validation.md` | Exit 0. | PASS, but only verifies current structural/semantic inputs. |
| `tools/phase1-python tools/validate-research.py validate-reports --root .planning` | Exit 0. | PASS, but does not exercise unsafe future publication paths. |
| Identity-bound `tools/validate-planning.py --phase-1-complete` | `0 errors, 0 warning(s)`. | PASS, but cannot supersede direct reproductions against the current implementation. |
| Phase probe scripts | No `scripts/*/tests/probe-*.sh` discovered or declared. | No executable shell probes to run. |

## Artifact and Data-Flow Assessment

| Artifact group | Status | Details |
|---|---|---|
| Source registry and claims | PRESENT, NOT TRUSTWORTHY | Files are substantive and validate, but acquisition confinement is bypassable and the live registry contains no qualified upstream protocol source. |
| Compatibility, drift, and open-question records | PRESENT, NOT TRUSTWORTHY | Current files preserve blocked status and uncertainty, but synthesis can publish invalid drift and readers can hang on malformed transaction artifacts. |
| Twelve spike metadata/measurement/report groups and replay manifest | PRESENT, NOT TRUSTWORTHY | The 36 core spike artifacts exist. Their integrity depends on unsafe consolidation/retention paths. |
| Security and terminal verification records | PRESENT, OUTDATED FOR CURRENT DEFECTS | `01-SECURITY.md`, `01-REVERIFICATION.md`, and `01-POST-CLOSURE-VERIFICATION.md` are substantive, but their passed results do not adjudicate the later-discovered defects. |
| Governance and traceability records | PRESENT, PARTIAL | Roles, plans, requirement IDs, and exit records are present, but `gsdState: passed` is not supportable until the evidence mechanisms are repaired and independently rechecked. |

## No-Phase-2-Transition Boundary

The retained boundary remains mandatory:

- No production scaffold was found outside preserved archive material: no project `package.json`, workspace manifest, `src/`, `apps/`, or `packages/` tree was found.
- `/workspace/projects/learn-napplets/.planning/research/adr-handoff.yaml` keeps ADRs proposed and prohibits production application/framework scaffolding pending separate human decisions and Phase 2 contract approval.
- This verification does not authorize ADR acceptance, residual-risk acceptance, package admission, external action, deployment, release, production scaffolding, or a Phase 2 transition.

## Required Remediation Before Re-verification

1. Restrict source cache roots to the repository-owned cache and add an external-root rejection regression.
2. Use journaled all-or-nothing publication for every canonical multi-file writer, including consolidation and SPK-G evidence retention; reject unexpected transaction entries before retrying readers.
3. Emit valid `observed-local` drift records or require genuinely distinct pinned sides, and semantically validate staged drift before publication.
4. Bind any future SPK-G execution to the constructed sandbox command, accept safe scoped npm names, and use no-follow private staging for all retained files.
5. Repair the duplicate test class, deep-copy migration inputs, and implement stale refresh-lock recovery.
6. Re-run independent review, security review, validation, and terminal verification against the repaired implementation. Keep all ADRs proposed and the Phase 2 boundary closed until this re-verification passes.

---

_Verifier: Claude (independent Phase 1 verifier)_
