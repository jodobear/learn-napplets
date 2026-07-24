---
phase: 01-research-and-truth-baseline
reviewed: 2026-07-24T00:00:00Z
depth: standard
files_reviewed: 15
files_reviewed_list:
  - .gitignore
  - requirements-phase1-tools.txt
  - tests/phase1/test_compatibility.py
  - tests/phase1/test_drift.py
  - tests/phase1/test_evidence.py
  - tests/phase1/test_governance.py
  - tests/phase1/test_lesson_evidence.py
  - tests/phase1/test_preflight.py
  - tests/phase1/test_spike_consolidation.py
  - tests/phase1/test_spikes.py
  - tools/acquire-sources.py
  - tools/phase1-python
  - tools/refresh-sources.py
  - tools/validate-planning.py
  - tools/validate-research.py
findings:
  critical: 9
  blocker: 9
  warning: 3
  info: 0
  total: 12
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-07-24T00:00:00Z  
**Depth:** standard  
**Files Reviewed:** 15  
**Status:** issues_found

## Summary

The Phase 1 evidence tools contain multiple fail-open paths that can authorize work without complete immutable provenance, execute an untrusted replay command, bypass the approved toolchain, or leave canonical evidence only partly published after a crash. The completed-spike validation and several corresponding tests also accept declared evidence that does not exist. These defects must be fixed before Phase 1 closeout is trusted.

## Critical Issues

### CR-01: Claim-citation provenance gate is disabled by an incorrectly escaped regex

**File:** `/workspace/projects/learn-napplets/tools/validate-planning.py:144`  
**Issue:** The raw regex ends in `\\b`, which matches a literal backslash followed by `b`, not a word boundary. Normal `CLM-*` citations in lesson packets, ADRs, and catalogs are never found, so `GATE016`–`GATE018` cannot enforce claim-to-immutable-source provenance during Phase 1 completion.  
**Impact:** The completion gate can pass citation-bearing material whose claims are unknown, have no source relations, or resolve to incomplete immutable source records.  
**Fix:** Use a real word-boundary expression and add a regression test with a dangling claim citation:
```python
re.findall(r"(?<![A-Z0-9-])(CLM-[A-Z0-9][A-Z0-9-]*)\b", text)
```

### CR-02: Execution preflight can authorize a non-converged review and unresolved HIGH findings

**File:** `/workspace/projects/learn-napplets/tools/validate-planning.py:46-81`  
**Issue:** A reviewer line is accepted whenever it is non-empty and lacks a few failure keywords; it does not require a verified convergence disposition such as `CONVERGED; HIGH=0; actionable=0`. Also, any occurrence of `none` in the Current HIGH section suppresses HIGH processing, including text such as `None resolved; HIGH-001 remains open.`  
**Impact:** Phase 1 execution can be authorized despite missing deep-review convergence or unresolved HIGH findings.  
**Fix:** Parse bounded sections strictly. Require the expected successful-disposition format, accept `None.` only as the entire normalized Current HIGH body, and parse each finding/disposition row from the dedicated dispositions table.

### CR-03: Phase-completion validation bypasses the approved isolated toolchain

**File:** `/workspace/projects/learn-napplets/tools/validate-planning.py:96-102,211-218`  
**Issue:** Gate subcommands and the lesson-evidence suite execute with `sys.executable`, rather than `tools/phase1-python`. This bypasses the approved interpreter, executable-digest verification, and isolated-environment policy during the command that certifies Phase 1 completion.  
**Impact:** Ambient packages can alter validation behavior or execute import-time code while the completion gate still reports success.  
**Fix:** Invoke all Phase 1 Python validators through the approved wrapper, including the subprocess test suite:
```python
command = [
    str(ROOT / "tools" / "phase1-python"),
    str(ROOT / "tools" / "validate-research.py"),
    *args,
]
```
Add a test proving the completion gate rejects an unapproved interpreter/environment.

### CR-04: Completed spikes accept unverifiable raw evidence and replay output digests

**File:** `/workspace/projects/learn-napplets/tools/validate-research.py:264-303`  
**Issue:** `validate_spike(..., "complete")` only checks that `rawOutputDigests` and `evidenceLinks` are non-empty. It never resolves their paths, verifies SHA-256 values, or connects `replayResult.outputDigest` to retained output.  
**Impact:** A completed spike can certify invented, altered, or missing raw evidence, defeating the immutable-provenance requirement.  
**Fix:** Require each local evidence path to be safely confined to the spike directory, exist, and match its declared digest. Require the replay-result digest to resolve to one of the validated retained outputs.

### CR-05: Impact fragments can bind canonical evidence to arbitrary files outside `.planning`

**File:** `/workspace/projects/learn-napplets/tools/validate-research.py:475-515,532-534`  
**Issue:** Fragment paths are constructed with `planning_root / supplied_path`, but absolute paths override `planning_root` and `..` segments are not rejected. Metadata, report, source, measurement, and evidence links can reference arbitrary local files. Further, `sourceLinks.path` only needs to hash-match any file; it is not required to be the canonical source-registry artifact for the declared `sourceId`.  
**Impact:** An untrusted fragment can pass using externally controlled evidence rather than retained Phase 1 evidence, corrupting consolidation provenance.  
**Fix:** Centralize safe path resolution: reject absolute paths and traversal, resolve candidates, and require `candidate.is_relative_to(planning_root.resolve())`. Enforce expected canonical locations for each link kind and verify each source link against the registered source record rather than merely any file with a supplied digest.

### CR-06: Replay manifests permit arbitrary local command execution

**File:** `/workspace/projects/learn-napplets/tools/validate-research.py:943-958`  
**Issue:** `replay_spikes` executes an arbitrary `replayCommand` from the manifest. `validate_replay_manifest` validates only fixture digests and does not constrain the executable, arguments, or relationship between command and spike. `shlex.split` prevents shell interpolation but does not prevent a tampered manifest from running arbitrary local programs.  
**Impact:** A modified manifest can execute arbitrary learner or host code, violating the explicit no-arbitrary-code-execution boundary.  
**Fix:** Do not execute manifest-provided command strings. Derive the replay invocation from a fixed spike-ID-to-directory mapping and run only the approved `tools/phase1-python ... validate-spike ... --complete` form. If commands remain declarative, parse and exact-match a strict allowlist before execution.

### CR-07: Transactional consolidation can leave permanently partial canonical state

**File:** `/workspace/projects/learn-napplets/tools/validate-research.py:1022-1033`  
**Issue:** Consolidation publishes six files through sequential `os.replace` calls. A process crash, kill, power loss, or exception between replacements leaves a mixed generation of canonical evidence, audit, security synthesis, and replay manifest. The in-process rollback only handles `OSError` after a failed replacement and is itself non-atomic.  
**Impact:** Subsequent gates can consume internally inconsistent canonical state despite the tool claiming serialized transactional publication.  
**Fix:** Use a durable journaled transaction with startup recovery, or publish immutable generation directories and atomically switch a single manifest/pointer file only after all staged artifacts are fsynced and validated.

### CR-08: Consolidation reclassifies local spike observations as both normative and observed evidence

**File:** `/workspace/projects/learn-napplets/tools/validate-research.py:660-688`  
**Issue:** `new_drift_record` creates one source-derived `side` and assigns it to both `normative` and `observed`. Its statement describes a local spike observation, while authority tier, maturity, and evidence class are copied from the referenced source.  
**Impact:** Local observations can appear to be source-authoritative normative evidence, violating the required separation of upstream fact, project policy, observation, and inference.  
**Fix:** Model retained local measurement evidence as its own explicitly classified observation with immutable local provenance. Do not synthesize a normative side from it; preserve the unresolved difference as an open question until independent normative evidence exists.

### CR-09: Toolchain wrapper verifies only the Python executable, not installed dependency integrity

**Files:** `/workspace/projects/learn-napplets/tools/phase1-python:35-39`; `/workspace/projects/learn-napplets/requirements-phase1-tools.txt:5-8`  
**Issue:** The wrapper hashes the interpreter but does not verify installed distributions, dependency closure, or wheel hashes. The requirements file pins only three top-level versions and supplies no hashes for those distributions or transitive packages.  
**Impact:** A changed or injected package inside the isolated environment passes the wrapper's interpreter check and can influence evidence validation.  
**Fix:** Use a fully resolved, hash-locked requirements artifact with `--require-hashes`; record distribution or wheel hashes in the toolchain manifest; verify them before executing Phase 1 tooling.

## Warnings

### WR-01: Tests explicitly certify completed spikes without retained raw-output files

**File:** `/workspace/projects/learn-napplets/tests/phase1/test_spikes.py:144-164`  
**Issue:** The passing completed-spike fixture declares `raw.txt` in `rawOutputDigests` and `evidenceLinks` but never creates it.  
**Impact:** The test suite encodes the raw-evidence integrity defect and cannot detect regressions that accept nonexistent or altered artifacts.  
**Fix:** Create `raw.txt`, compute its SHA-256, assert the valid case passes, and add missing-file and altered-content cases that must fail.

### WR-02: Evidence test writes into canonical repository planning state

**File:** `/workspace/projects/learn-napplets/tests/phase1/test_evidence.py:94-99`  
**Issue:** `test_traceability_mappings_resolve_to_pinned_archive_files` writes its report to `.planning/research/reports/validation.md` in the working tree.  
**Impact:** Test execution can dirty canonical planning artifacts and parallel test runs race on the same output path.  
**Fix:** Use a `TemporaryDirectory` report path while retaining the real research root as the validation input.

### WR-03: Refresh input accepts contradictory duplicate observations for one source

**File:** `/workspace/projects/learn-napplets/tools/refresh-sources.py:155-157`  
**Issue:** The comparison list is processed independently and permits multiple entries for the same source ID with conflicting outcomes or pins. It emits multiple review work items rather than failing closed or reducing them to one explicitly ambiguous source observation.  
**Impact:** Review routing is not a one-source/one-observation deterministic record and can present contradictory refresh state to reviewers.  
**Fix:** Group observations by `id` before comparison; reject non-identical duplicates, or emit one canonical `ambiguous` result containing all conflicting observations and their digests.

---

_Reviewed: 2026-07-24T00:00:00Z_  
_Reviewer: Claude (gsd-code-reviewer)_  
_Depth: standard_
