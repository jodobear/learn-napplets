---
phase: 01-research-and-truth-baseline
plan: 44
subsystem: supply-chain-security
tags: [python, pip, wheelhouse, sha256, offline-install, record-integrity]
requires:
  - phase: 01-research-and-truth-baseline
    provides: Plan 01-29 recorded-interpreter bootstrap and review authorization gate
provides:
  - Complete exact hash-locked Python dependency closure in a verified offline wheelhouse
  - Fresh certified target with installer-report, archive, and installed-RECORD provenance binding
  - Bootstrap-first wrapper that rejects unverified forwarding
  - Standard-library verifier for lock, policy, wheel, inventory, report, attestation, and RECORD checks
affects: [01-45, Phase 1 source collection, evidence tooling]
tech-stack:
  added: [PyYAML 6.0.3, jsonschema 4.26.0, Playwright 1.61.0, verified transitive wheel closure]
  patterns: [offline hash-required installation, archive-to-report provenance, wheel-to-installed-RECORD integrity]
key-files:
  created:
    - .planning/research/toolchain-wheelhouse-manifest.json
    - .planning/research/toolchain-install-attestation.json
    - tools/verify-phase1-toolchain.py
  modified:
    - requirements-phase1-tools.txt
    - .planning/research/toolchain-approval.yaml
    - tools/phase1-python
    - tests/phase1/test_evidence.py
key-decisions:
  - "The prior human approval remains limited to the three approved top-level pins; exact resolver-selected dependencies are derived in scope and policy checked."
  - "The forwarding wrapper executes only the fresh certified target after bootstrap and complete verifier success."
  - "Wheel .data header paths are translated to pip's installed RECORD spelling before integrity comparison."
patterns-established:
  - "Require every wheelhouse archive to match one lock entry, manifest record, installer-report URL, and installed distribution."
  - "Bind target forwarding to both interpreter/venv identity and installed file hashes rather than package metadata alone."
requirements-completed: [EVID-01, OPER-03]
coverage:
  - id: D1
    description: Fresh Phase 1 target is built offline from the complete hash-required wheel closure and attested through installer report and RECORD comparisons.
    requirement: EVID-01
    verification:
      - kind: integration
        ref: tools/phase1-python --verify-toolchain
        status: pass
      - kind: unit
        ref: tests/phase1/test_evidence.py#SourceEvidenceTests.test_toolchain_certification_binds_fresh_install_to_verified_wheels
        status: pass
      - kind: integration
        ref: tests/phase1/test_evidence.py#SourceEvidenceTests.test_toolchain_certification_survives_checkout_relocation_and_rejects_stale_paths
        status: pass
    human_judgment: false
  - id: D2
    description: Wrapper forwarding fails closed for altered archives, lock/policy/report/attestation inputs, target inventory, and installed RECORDs.
    requirement: OPER-03
    verification:
      - kind: unit
        ref: tests/phase1/test_evidence.py#SourceEvidenceTests.test_toolchain_integrity_blocks_untrusted_forwarding
        status: pass
      - kind: unit
        ref: tests/phase1/test_evidence.py#SourceEvidenceTests.test_toolchain_scope_or_policy_failure_requires_escalation
        status: pass
    human_judgment: false
metrics:
  duration: 35min
  completed: 2026-07-30
status: complete
---

# Phase 01 Plan 44: Fresh Offline Toolchain Certification Summary

**A complete hash-locked Python wheel closure now produces a checkout-relocatable fresh Phase 1 target whose wrapper forwarding is blocked unless archive, policy, installer report, inventory, attestation-path, and RECORD checks all pass.**

## Performance

- **Duration:** 35 min
- **Completed:** 2026-07-30
- **Tasks:** 1/1
- **Files modified:** 8 task artifacts plus this summary

## Accomplishments

- Replaced the three top-level-only requirements list with the complete ten-distribution, exact SHA-256 closure while retaining the dated human top-level approval boundary.
- Downloaded one approved compatible binary wheel per closure member into the ignored offline wheelhouse and generated a sorted tracked manifest for all archive hashes and policy outcomes.
- Built a new isolated certification target from `--require-hashes --no-index --find-links --no-deps --only-binary=:all:`, then bound every installed distribution to its `file://` installer-report wheel filename/hash and wheel/installed RECORD hashes without retaining a stale worktree path.
- Added a standard-library verifier and made `tools/phase1-python` bootstrap first, verify all certification inputs, and only then forward argv to the fresh target.

## Task Commits

1. **Task 1: Certify one fresh hash-locked environment from its verified wheel archives** - `d4e9d23` (test RED), `5b35ee7` (feat GREEN)

## Files Created/Modified

- `requirements-phase1-tools.txt` - Complete ten-wheel exact-hash offline lock.
- `.planning/research/toolchain-approval.yaml` - Distinguishes approved top-level scope from derived in-scope closure members.
- `.planning/research/toolchain-wheelhouse-manifest.json` - Sorted archive hash, metadata, and policy binding.
- `.planning/research/toolchain-install-attestation.json` - Fresh-target, installer-report, archive mapping, and RECORD attestation.
- `tools/verify-phase1-toolchain.py` - Standard-library certification and forwarding verifier.
- `tools/phase1-python` - Bootstrap-first verified forwarding wrapper.
- `tests/phase1/test_evidence.py` - Four named toolchain certification regressions.

## Decisions Made

- The approved PyYAML, jsonschema, and Playwright pins remain the sole human-authorized top-level scope; resolver-selected closure members need no new sign-off when their exact binary archive and policy checks pass.
- A fresh certification target, rather than the bootstrap interpreter or a prior target, is the only wrapper forwarding destination.
- The attestation stores wheelhouse, report, target, and interpreter references as non-escaping repo-relative paths, then binds the current checkout's venv configuration, interpreter digest, installer report, and installed RECORD digests.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected wheel `.data/headers` RECORD translation**
- **Found during:** Task 1 certification.
- **Issue:** Pip installs the greenlet header under the target include tree while its wheel RECORD uses a `.data/headers` path, so a direct path comparison rejected a valid fresh installation.
- **Fix:** Translate standard wheel installation schemes to pip's installed RECORD paths before comparing hashes.
- **Files modified:** `tools/verify-phase1-toolchain.py`
- **Verification:** Fresh offline certification and `tools/phase1-python --verify-toolchain` pass.
- **Committed in:** `5b35ee7`

**2. [Rule 1 - Bug] Restored the plan-specified test class path**
- **Found during:** Task 1 focused verification.
- **Issue:** The four RED tests initially lived on a separate class, while the plan invokes them through `test_evidence.SourceEvidenceTests`.
- **Fix:** Preserved existing source-validation tests under a distinct class and exposed the four certification tests on the required class path.
- **Files modified:** `tests/phase1/test_evidence.py`
- **Verification:** All four exact focused unittest invocations pass through the certified wrapper.
- **Committed in:** `5b35ee7`

**3. [Rule 2 - Missing Critical] Bound the fresh target's venv identity in the attestation**
- **Found during:** Task 1 target-forwarding review.
- **Issue:** Archive and installed-file checks alone did not bind the wrapper's target location and venv configuration.
- **Fix:** Added target-root, target-interpreter-path, and `pyvenv.cfg` digest checks to the attestation verifier.
- **Files modified:** `tools/verify-phase1-toolchain.py`, `.planning/research/toolchain-install-attestation.json`
- **Verification:** Fresh certification, standalone verifier, and wrapper verifier all pass.
- **Committed in:** `5b35ee7`

**4. [Rule 1 - Bug] Made attestation and installer-report provenance checkout-relocatable**
- **Found during:** Post-run merge portability review.
- **Issue:** The tracked attestation serialized durable-worktree absolute paths, and report verification required those original paths, so moving identical ignored runtime assets into the merged checkout would fail.
- **Fix:** Store and validate only non-escaping repo-relative wheelhouse, report, target, and interpreter references. Treat report `file://` locations as historical provenance while binding their exact declared filename, distribution, and hash to the current verified wheelhouse.
- **Files modified:** `tools/verify-phase1-toolchain.py`, `.planning/research/toolchain-install-attestation.json`, `tests/phase1/test_evidence.py`
- **Verification:** A copied identical certification asset set verifies under a distinct checkout root; every absolute attestation reference is rejected.
- **Committed in:** portability correction commit after this summary update.

**Total deviations:** 4 auto-fixed (3 Rule 1 bugs, 1 Rule 2 critical integrity binding).

## Issues Encountered

- The four Plan 01-44 focused certification tests pass in the durable worktree. The full `tests/phase1/test_evidence.py` integration run depends on the orchestrator checkout's traceability fixture and is post-merge orchestration work, not a durable-worktree deferral.
- The first two isolated certification targets discovered RECORD translation and attestation-binding defects. They are intentionally retained as ignored runtime assets per durable-worktree instruction; the final verified target is `.research/phase1-certified-tools-4`.

## Known Stubs

None.

## Next Phase Readiness

- Plan 01-45 can invoke `tools/phase1-python` only after its bootstrap and certification gates pass.
- The orchestrator must preserve the ignored runtime assets listed in the executor completion message before cleaning this durable worktree.

## Self-Check: PASSED

- Confirmed `tools/verify-phase1-toolchain.py`, the tracked wheelhouse manifest, and the tracked installation attestation exist.
- Confirmed TDD RED commit `d4e9d23` and GREEN commit `5b35ee7` exist on the worktree branch.
- Confirmed no tracked-file deletion was introduced and no Known Stubs were found in task artifacts.
- Confirmed copied identical runtime assets verify from a distinct checkout root while stale absolute attestation paths are rejected.
