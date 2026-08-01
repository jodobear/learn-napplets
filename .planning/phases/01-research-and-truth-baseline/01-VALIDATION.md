---
phase: 01
slug: research-and-truth-baseline
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-07-23
updated: 2026-07-30T18:49:39Z
---

# Phase 1 — Validation Strategy

This contract records executable Phase 1 evidence checks. It classifies evidence and produces review work; it does not approve an ADR, recommendation, residual risk, source authority, package admission, architecture, or phase transition.

## Current Status

The fourteen direct evidence-production attempts below closed successfully at `2026-07-30T18:49:39Z`. The retained post-closure full suite and identity-bound completion gate both passed, so Nyquist compliance and Wave 0 completion are true without reopening the canonical ledger.

## Prerequisite Gate Evidence

Plan 01-37 executed the following wrapper-only sequence with executor identity `claude-code/gpt-5.6-sol:gsd-executor`, distinct from the recorded independent reviewer. These prerequisite gate runs are not canonical probe attempts.

| Stage | Exact command | Result |
| --- | --- | --- |
| bound-review-preflight | `GSD_EXECUTOR_ID="claude-code/gpt-5.6-sol:gsd-executor" tools/phase1-python tools/validate-planning.py --phase-1-execution-preflight --executor-identity "claude-code/gpt-5.6-sol:gsd-executor"` | exit 0 — passed |
| toolchain-verification | `tools/phase1-python --verify-toolchain` | exit 0 — passed |
| full-phase1-tests | `tools/phase1-python -m unittest discover -s tests/phase1` | exit 0 — 121 tests passed |
| research-validation | `tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/phase1-final-validation.md` | exit 0 — passed |
| report-validation | `tools/phase1-python tools/validate-research.py validate-reports --root .planning` | exit 0 — passed |
| canonical-recovery | `tools/phase1-python tools/validate-research.py recover-consolidation --research .planning/research` | exit 0 — passed |
| spike-replay | `tools/phase1-python tools/validate-research.py replay-spikes --manifest .planning/spikes/replay-manifest.yaml --check` | exit 0 — passed |
| phase-completion | `GSD_EXECUTOR_ID="claude-code/gpt-5.6-sol:gsd-executor" tools/phase1-python tools/validate-planning.py --phase-1-complete --executor-identity "claude-code/gpt-5.6-sol:gsd-executor"` | exit 0 — 0 errors, 0 warnings |

## Canonical Direct-Attempt Ledger

```json
{"ledgerId":"P1-38-NYQUIST-DIRECT-14","executorIdentity":"claude-code/gpt-5.6-sol:gsd-executor","closureBoundary":"after fourteen direct rows and before post-closure verification","attempts":[{"attemptId":"P1-38-DIRECT-P-EVID01-ADJ","role":"direct","probeId":"P-EVID01-ADJ","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_ascii_adjacency_extracts_exact_token"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-adj"},{"attemptId":"P1-38-DIRECT-P-EVID01-EMPTY","role":"direct","probeId":"P-EVID01-EMPTY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_empty_inventory_has_no_diagnostic"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-empty"},{"attemptId":"P1-38-DIRECT-P-EVID01-ENCODING","role":"direct","probeId":"P-EVID01-ENCODING","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_tokens_are_ascii_decoded_codepoints_without_unicode_normalization"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-encoding"},{"attemptId":"P1-38-DIRECT-P-EVID01-ORDER","role":"direct","probeId":"P-EVID01-ORDER","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_diagnostics_stable_path_then_id"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-order"},{"attemptId":"P1-38-DIRECT-P-EVID02-ADJ","role":"direct","probeId":"P-EVID02-ADJ","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid02-adj"},{"attemptId":"P1-38-DIRECT-P-EVID02-EMPTY","role":"direct","probeId":"P-EVID02-EMPTY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.DriftSchemas.test_drift_rejects_empty_null_and_single_sides"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid02-empty"},{"attemptId":"P1-38-DIRECT-P-EVID02-ORDER","role":"direct","probeId":"P-EVID02-ORDER","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.DriftSchemas.test_drift_records_sort_ids_observations_impacts_and_history"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid02-order"},{"attemptId":"P1-38-DIRECT-P-EVID03-MANUAL","role":"direct","probeId":"P-EVID03-MANUAL","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_compatibility_completeness_requires_qualified_dimensions_without_approval"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid03-manual"},{"attemptId":"P1-38-DIRECT-P-EVID04-MANUAL","role":"direct","probeId":"P-EVID04-MANUAL","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_mandatory_spike_completeness_requires_retained_evidence_without_approval"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid04-manual"},{"attemptId":"P1-38-DIRECT-P-OPER01-IDEMPOTENCY","role":"direct","probeId":"P-OPER01-IDEMPOTENCY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper01-idempotency"},{"attemptId":"P1-38-DIRECT-P-OPER01-CONCURRENCY","role":"direct","probeId":"P-OPER01-CONCURRENCY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_spike_consolidation.SpikeConsolidationTests.test_recovery_after_each_publish_interruption_is_coherent"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper01-concurrency"},{"attemptId":"P1-38-DIRECT-P-OPER03-ADJ","role":"direct","probeId":"P-OPER03-ADJ","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_governance_role_adjacency_requires_independence"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper03-adj"},{"attemptId":"P1-38-DIRECT-P-OPER03-EMPTY","role":"direct","probeId":"P-OPER03-EMPTY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_governance_empty_null_single_required_fields_fail"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper03-empty"},{"attemptId":"P1-38-DIRECT-P-OPER03-ORDER","role":"direct","probeId":"P-OPER03-ORDER","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_governance_ordering_is_stable"],"exit":0,"compactResult":"Ran 1 test; OK","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper03-order"}]}
```

## Direct Attempt Evidence

<a id="direct-attempt-p1-38-direct-p-evid01-adj"></a>`P1-38-DIRECT-P-EVID01-ADJ`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-evid01-empty"></a>`P1-38-DIRECT-P-EVID01-EMPTY`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-evid01-encoding"></a>`P1-38-DIRECT-P-EVID01-ENCODING`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-evid01-order"></a>`P1-38-DIRECT-P-EVID01-ORDER`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-evid02-adj"></a>`P1-38-DIRECT-P-EVID02-ADJ`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-evid02-empty"></a>`P1-38-DIRECT-P-EVID02-EMPTY`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-evid02-order"></a>`P1-38-DIRECT-P-EVID02-ORDER`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-evid03-manual"></a>`P1-38-DIRECT-P-EVID03-MANUAL`: wrapper probe executed; compatibility result stayed blocked/non-approving under each missing dimension.

<a id="direct-attempt-p1-38-direct-p-evid04-manual"></a>`P1-38-DIRECT-P-EVID04-MANUAL`: wrapper probe executed; all twelve retained spike bundles validated and a digest mutation produced a concrete gap.

<a id="direct-attempt-p1-38-direct-p-oper01-idempotency"></a>`P1-38-DIRECT-P-OPER01-IDEMPOTENCY`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-oper01-concurrency"></a>`P1-38-DIRECT-P-OPER01-CONCURRENCY`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-oper03-adj"></a>`P1-38-DIRECT-P-OPER03-ADJ`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-oper03-empty"></a>`P1-38-DIRECT-P-OPER03-EMPTY`: wrapper probe executed; 1 test passed.

<a id="direct-attempt-p1-38-direct-p-oper03-order"></a>`P1-38-DIRECT-P-OPER03-ORDER`: wrapper probe executed; 1 test passed.

## Canonical Probe Matrix

```json
[{"probeId":"P-EVID01-ADJ","namedTest":"test_preflight.Phase1ExecutionPreflightTests.test_citation_ascii_adjacency_extracts_exact_token","directAttemptId":"P1-38-DIRECT-P-EVID01-ADJ","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-adj"},{"probeId":"P-EVID01-EMPTY","namedTest":"test_preflight.Phase1ExecutionPreflightTests.test_citation_empty_inventory_has_no_diagnostic","directAttemptId":"P1-38-DIRECT-P-EVID01-EMPTY","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-empty"},{"probeId":"P-EVID01-ENCODING","namedTest":"test_preflight.Phase1ExecutionPreflightTests.test_citation_tokens_are_ascii_decoded_codepoints_without_unicode_normalization","directAttemptId":"P1-38-DIRECT-P-EVID01-ENCODING","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-encoding"},{"probeId":"P-EVID01-ORDER","namedTest":"test_preflight.Phase1ExecutionPreflightTests.test_citation_diagnostics_stable_path_then_id","directAttemptId":"P1-38-DIRECT-P-EVID01-ORDER","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-order"},{"probeId":"P-EVID02-ADJ","namedTest":"test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent","directAttemptId":"P1-38-DIRECT-P-EVID02-ADJ","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid02-adj"},{"probeId":"P-EVID02-EMPTY","namedTest":"test_drift.DriftSchemas.test_drift_rejects_empty_null_and_single_sides","directAttemptId":"P1-38-DIRECT-P-EVID02-EMPTY","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid02-empty"},{"probeId":"P-EVID02-ORDER","namedTest":"test_drift.DriftSchemas.test_drift_records_sort_ids_observations_impacts_and_history","directAttemptId":"P1-38-DIRECT-P-EVID02-ORDER","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid02-order"},{"probeId":"P-EVID03-MANUAL","namedTest":"test_gap_closeout.GapCloseoutTests.test_compatibility_completeness_requires_qualified_dimensions_without_approval","directAttemptId":"P1-38-DIRECT-P-EVID03-MANUAL","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid03-manual"},{"probeId":"P-EVID04-MANUAL","namedTest":"test_gap_closeout.GapCloseoutTests.test_mandatory_spike_completeness_requires_retained_evidence_without_approval","directAttemptId":"P1-38-DIRECT-P-EVID04-MANUAL","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid04-manual"},{"probeId":"P-OPER01-IDEMPOTENCY","namedTest":"test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent","directAttemptId":"P1-38-DIRECT-P-OPER01-IDEMPOTENCY","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper01-idempotency"},{"probeId":"P-OPER01-CONCURRENCY","namedTest":"test_spike_consolidation.SpikeConsolidationTests.test_recovery_after_each_publish_interruption_is_coherent","directAttemptId":"P1-38-DIRECT-P-OPER01-CONCURRENCY","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper01-concurrency"},{"probeId":"P-OPER03-ADJ","namedTest":"test_gap_closeout.GapCloseoutTests.test_governance_role_adjacency_requires_independence","directAttemptId":"P1-38-DIRECT-P-OPER03-ADJ","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper03-adj"},{"probeId":"P-OPER03-EMPTY","namedTest":"test_gap_closeout.GapCloseoutTests.test_governance_empty_null_single_required_fields_fail","directAttemptId":"P1-38-DIRECT-P-OPER03-EMPTY","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper03-empty"},{"probeId":"P-OPER03-ORDER","namedTest":"test_gap_closeout.GapCloseoutTests.test_governance_ordering_is_stable","directAttemptId":"P1-38-DIRECT-P-OPER03-ORDER","evidenceLocator":"01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper03-order"}]
```

## Ledger Closure

```json
{"ledgerId":"P1-38-NYQUIST-DIRECT-14","closedAt":"2026-07-30T18:49:39Z","preClosureLedgerSha256":"04290f43c56fd77f05fb8676bf07c76ed93222ee303e5d8e7cf9c25a42203d93"}
```

The SHA-256 is calculated over the UTF-8 canonical JSON serialization of the ledger ID, closure boundary, and lexically ordered fourteen-row direct-attempt payload, excluding the digest field. The closed ledger cannot gain, replace, or invalidate rows. Validator, security, terminal, regression, and full-gate reruns occur only after this boundary and may be retained in independent post-closure batches.

## Manual Evidence-Completeness Boundaries

Compatibility and mandatory-spike classifications identify evidence completeness and concrete gaps for human review. They cannot accept an ADR, recommendation, residual risk, source authority, package admission, architecture, or phase transition. The `architectureApproved: false` result is invariant even for a qualified fixture; the current canonical baseline remains blocked by its retained evidence state.
