---
phase: 01
plan: 40
re_verification: true
terminal_verdict: pending_human_recheck
prepared_at: "2026-07-30T21:30:00Z"
prepared_by_executor: "claude-code/gpt-5.6-sol:gsd-executor"
reviewed_commit: "77e6acfd753b478177e556b599111a02a0131bdc"
active_plan_review_manifest_sha256: "8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95"
security_review_sha256: "12b0d70e7a82e22b07d9322cf1ffa1acb7ceafba9f58b7abc01f9acd40f7f145"
security_evidence_sha256: "042812f6c7015cd61cf49939153d73b6033394a1080597cf0e625aefbb4343c9"
historical_verification_sha256: "ecc85cc7b0cefd958ea6f30c44f6f5f5f4915ba51d650978eab5498aeabf4b8f"
canonical_ledger_id: P1-40-TERMINAL-DIRECT-14
canonical_ledger_sha256: "a530368c494b05e0f999f3ddcfde445c6b9c38ea21c1247ff18da07eb4001159"
selected_post_closure_batch_id: P1-40-POST-001
selected_post_closure_batch_sha256: "229198f18c4a07f56dcf7151fc23a79a19a4bb05ba361010fd524119b514436b"
---

# Phase 1 Fresh Verification Candidate

This automation-prepared dossier is non-terminal. It preserves the historical initial verification record unchanged, binds fresh command evidence, and leaves terminal determination to separately dated human verifier and project-owner rechecker records.

## Historical Initial Verification Binding

`01-VERIFICATION.md` remains byte-for-byte unchanged. Its SHA-256 is `ecc85cc7b0cefd958ea6f30c44f6f5f5f4915ba51d650978eab5498aeabf4b8f`.

## Reviewed Source-Grounding Authorization

The source-input verifier passed against the active review record. This table is the single six-row authorization table in this candidate.

| Path | Git mode | Git blob | SHA-256 | Reviewed commit |
| --- | --- | --- | --- | --- |
| `.planning/PROJECT.md` | `100644` | `4e26ed80eaf03fcc56384b4be78c20ac9b856265` | `aa4507190c8971a229ea628b697ff1e91e8f0d8ff317380aefe3f992f079f499` | `1a9449be4d74aa1ceed235d949802266846cf63b` |
| `.planning/phases/01-research-and-truth-baseline/01-CONTEXT.md` | `100644` | `0b626d358e8d22fcd6fb2d0c42f01b45e0a1823c` | `fdfad3695d380d16436420f19a77f6740d798b398441e3da3d442ec2e52b26f8` | `1a9449be4d74aa1ceed235d949802266846cf63b` |
| `.planning/research/reports/upstream-refresh-kehto-web-2026-07-28.md` | `100644` | `8b0e6d97b647989aca17184d62b81d9037fbd142` | `959b6101e411e52ad64ce532477974382c15aa4062c2c544868491f944fa3a36` | `1a9449be4d74aa1ceed235d949802266846cf63b` |
| `.planning/research/reports/upstream-refresh-napplet-naps-2026-07-28.md` | `100644` | `0b30af640dc2d05763d53a04b71fd33d7aaaab53` | `94a49792c6fc0f8336803f03c2fb324371618092eccb0cc7a26cf57d319ed4d4` | `1a9449be4d74aa1ceed235d949802266846cf63b` |
| `.planning/research/reports/upstream-refresh-napplet-web-2026-07-28.md` | `100644` | `a9fc4a6612105b3ac7325ce1823c85a36c26d1eb` | `3219578c3b2eff1eb09f04a48ccc1587de9321ba615d87ffb1e163c5bf58cc28` | `1a9449be4d74aa1ceed235d949802266846cf63b` |
| `.planning/research/reports/upstream-refresh-synthesis-2026-07-28.md` | `100644` | `d059ba5a34f50656c94f87b62ee15852f311e5a2` | `eba5df04a8ddfa0b5a4d7b1ec60268f3d7bb733623e8ba1ac3482b2f371c6478` | `1a9449be4d74aa1ceed235d949802266846cf63b` |

## Prerequisite Verification

The supported wrapper-only gate passed before direct evidence production. The same full gate was retained after closure in `P1-40-POST-001`; it is noncanonical post-closure verification.

| Stage | Result | Evidence digest |
| --- | --- | --- |
| bound review preflight | exit 0 | `da682ac91f90006fd49649b5d1ddbf581920ae9ba0d2763301717bae0fdc05ee` |
| source input verifier | exit 0 | `20daa6035b8a1120cd399c64d6b9c4e7ecb7b233b65adf421985a3d0bfebe08b` |
| certified toolchain | exit 0 | `f816b70850126ed457ff08db3255a52ef63498d64a2fa3cdbe4377858f5872e3` |
| full Phase 1 suite | exit 0 | `648e838b6a9d22f8efef0b993ff7e5446074bec0080bda48398cbd70797ae27f` |
| research validation | exit 0 | `f816b70850126ed457ff08db3255a52ef63498d64a2fa3cdbe4377858f5872e3` |
| report validation | exit 0 | `f816b70850126ed457ff08db3255a52ef63498d64a2fa3cdbe4377858f5872e3` |
| recovery validation | exit 0 | `f816b70850126ed457ff08db3255a52ef63498d64a2fa3cdbe4377858f5872e3` |
| spike replay | exit 0 | `f816b70850126ed457ff08db3255a52ef63498d64a2fa3cdbe4377858f5872e3` |
| identity-bound completion | exit 0 | `5345611cc529bf2b51245f3bfd9659942e2dd3be5d8a5b72ea8eb46e1101e28e` |

## Canonical Direct-Attempt Ledger

```json
{"ledgerId":"P1-40-TERMINAL-DIRECT-14","closureBoundary":"after fourteen direct rows and before post-closure verification","attempts":[{"attemptId":"P1-40-DIRECT-P-EVID01-ADJ","role":"direct","probeId":"P-EVID01-ADJ","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_ascii_adjacency_extracts_exact_token"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_preflight.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid01-adj"},{"attemptId":"P1-40-DIRECT-P-EVID01-EMPTY","role":"direct","probeId":"P-EVID01-EMPTY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_empty_inventory_has_no_diagnostic"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_preflight.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid01-empty"},{"attemptId":"P1-40-DIRECT-P-EVID01-ENCODING","role":"direct","probeId":"P-EVID01-ENCODING","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_tokens_are_ascii_decoded_codepoints_without_unicode_normalization"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_preflight.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid01-encoding"},{"attemptId":"P1-40-DIRECT-P-EVID01-ORDER","role":"direct","probeId":"P-EVID01-ORDER","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_preflight.Phase1ExecutionPreflightTests.test_citation_diagnostics_stable_path_then_id"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_preflight.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid01-order"},{"attemptId":"P1-40-DIRECT-P-EVID02-ADJ","role":"direct","probeId":"P-EVID02-ADJ","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_drift.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid02-adj"},{"attemptId":"P1-40-DIRECT-P-EVID02-EMPTY","role":"direct","probeId":"P-EVID02-EMPTY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.DriftSchemas.test_drift_rejects_empty_null_and_single_sides"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_drift.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid02-empty"},{"attemptId":"P1-40-DIRECT-P-EVID02-ORDER","role":"direct","probeId":"P-EVID02-ORDER","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.DriftSchemas.test_drift_records_sort_ids_observations_impacts_and_history"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_drift.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid02-order"},{"attemptId":"P1-40-DIRECT-P-EVID03-MANUAL","role":"direct","probeId":"P-EVID03-MANUAL","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_compatibility_completeness_requires_qualified_dimensions_without_approval"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_gap_closeout.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid03-manual"},{"attemptId":"P1-40-DIRECT-P-EVID04-MANUAL","role":"direct","probeId":"P-EVID04-MANUAL","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_mandatory_spike_completeness_requires_retained_evidence_without_approval"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_gap_closeout.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-evid04-manual"},{"attemptId":"P1-40-DIRECT-P-OPER01-CONCURRENCY","role":"direct","probeId":"P-OPER01-CONCURRENCY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_spike_consolidation.SpikeConsolidationTests.test_recovery_after_each_publish_interruption_is_coherent"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_spike_consolidation.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-oper01-concurrency"},{"attemptId":"P1-40-DIRECT-P-OPER01-IDEMPOTENCY","role":"direct","probeId":"P-OPER01-IDEMPOTENCY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_drift.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-oper01-idempotency"},{"attemptId":"P1-40-DIRECT-P-OPER03-ADJ","role":"direct","probeId":"P-OPER03-ADJ","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_governance_role_adjacency_requires_independence"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_gap_closeout.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-oper03-adj"},{"attemptId":"P1-40-DIRECT-P-OPER03-EMPTY","role":"direct","probeId":"P-OPER03-EMPTY","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_governance_empty_null_single_required_fields_fail"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_gap_closeout.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-oper03-empty"},{"attemptId":"P1-40-DIRECT-P-OPER03-ORDER","role":"direct","probeId":"P-OPER03-ORDER","environment":{"PYTHONPATH":"tests/phase1"},"argv":["tools/phase1-python","-m","unittest","test_gap_closeout.GapCloseoutTests.test_governance_ordering_is_stable"],"exit":0,"compactResult":"Ran 1 test; OK","fixtureOrMutation":"canonical regression fixture","sourcePath":"tests/phase1/test_gap_closeout.py","evidenceLocator":"01-VERIFICATION-CANDIDATE.md#direct-attempt-p1-40-direct-p-oper03-order"}]}
```

## Ledger Closure

`P1-40-TERMINAL-DIRECT-14` closed at `2026-07-30T21:30:00Z`, after its fourteen direct rows and before retained post-closure verification. Its normalized lexical direct-row payload SHA-256 is `a530368c494b05e0f999f3ddcfde445c6b9c38ea21c1247ff18da07eb4001159`. Later batches cannot replace or add canonical rows.

## Probe Execution

| Probe ID | Named test | Direct attempt | Exit | Evidence locator |
| --- | --- | --- | --- | --- |
| P-EVID01-ADJ | `test_citation_ascii_adjacency_extracts_exact_token` | `P1-40-DIRECT-P-EVID01-ADJ` | 0 | `#direct-attempt-p1-40-direct-p-evid01-adj` |
| P-EVID01-EMPTY | `test_citation_empty_inventory_has_no_diagnostic` | `P1-40-DIRECT-P-EVID01-EMPTY` | 0 | `#direct-attempt-p1-40-direct-p-evid01-empty` |
| P-EVID01-ENCODING | `test_citation_tokens_are_ascii_decoded_codepoints_without_unicode_normalization` | `P1-40-DIRECT-P-EVID01-ENCODING` | 0 | `#direct-attempt-p1-40-direct-p-evid01-encoding` |
| P-EVID01-ORDER | `test_citation_diagnostics_stable_path_then_id` | `P1-40-DIRECT-P-EVID01-ORDER` | 0 | `#direct-attempt-p1-40-direct-p-evid01-order` |
| P-EVID02-ADJ | `test_parallel_sides_are_distinct_and_adjacent` | `P1-40-DIRECT-P-EVID02-ADJ` | 0 | `#direct-attempt-p1-40-direct-p-evid02-adj` |
| P-EVID02-EMPTY | `test_drift_rejects_empty_null_and_single_sides` | `P1-40-DIRECT-P-EVID02-EMPTY` | 0 | `#direct-attempt-p1-40-direct-p-evid02-empty` |
| P-EVID02-ORDER | `test_drift_records_sort_ids_observations_impacts_and_history` | `P1-40-DIRECT-P-EVID02-ORDER` | 0 | `#direct-attempt-p1-40-direct-p-evid02-order` |
| P-EVID03-MANUAL | `test_compatibility_completeness_requires_qualified_dimensions_without_approval` | `P1-40-DIRECT-P-EVID03-MANUAL` | 0 | `#direct-attempt-p1-40-direct-p-evid03-manual` |
| P-EVID04-MANUAL | `test_mandatory_spike_completeness_requires_retained_evidence_without_approval` | `P1-40-DIRECT-P-EVID04-MANUAL` | 0 | `#direct-attempt-p1-40-direct-p-evid04-manual` |
| P-OPER01-IDEMPOTENCY | `test_duplicate_refresh_observations_are_idempotent` | `P1-40-DIRECT-P-OPER01-IDEMPOTENCY` | 0 | `#direct-attempt-p1-40-direct-p-oper01-idempotency` |
| P-OPER01-CONCURRENCY | `test_recovery_after_each_publish_interruption_is_coherent` | `P1-40-DIRECT-P-OPER01-CONCURRENCY` | 0 | `#direct-attempt-p1-40-direct-p-oper01-concurrency` |
| P-OPER03-ADJ | `test_governance_role_adjacency_requires_independence` | `P1-40-DIRECT-P-OPER03-ADJ` | 0 | `#direct-attempt-p1-40-direct-p-oper03-adj` |
| P-OPER03-EMPTY | `test_governance_empty_null_single_required_fields_fail` | `P1-40-DIRECT-P-OPER03-EMPTY` | 0 | `#direct-attempt-p1-40-direct-p-oper03-empty` |
| P-OPER03-ORDER | `test_governance_ordering_is_stable` | `P1-40-DIRECT-P-OPER03-ORDER` | 0 | `#direct-attempt-p1-40-direct-p-oper03-order` |

## Post-Closure Audit Snapshot

The selected audit batch is `P1-40-POST-001`, bound to `P1-40-TERMINAL-DIRECT-14` and its ledger digest. Its normalized payload SHA-256 is `229198f18c4a07f56dcf7151fc23a79a19a4bb05ba361010fd524119b514436b`. It retains the full prerequisite gate as noncanonical verification only.

## Review Finding Adjudication

| Finding ID | Approved wrapper command | Fresh result/evidence locator | Repaired source path | Verdict |
| --- | --- | --- | --- | --- |
| CR-01 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_preflight.Phase1ExecutionPreflightTests.test_citation_ascii_adjacency_extracts_exact_token` | `P1-40-DIRECT-P-EVID01-ADJ; #direct-attempt-p1-40-direct-p-evid01-adj` | `tools/validate-planning.py` | passed |
| CR-02 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_preflight.Phase1ExecutionPreflightTests.test_preflight_requires_exact_convergence_and_high_disposition` | `full suite; P1-40-POST-001-RUN-04` | `tools/validate-planning.py` | passed |
| CR-03 | `GSD_EXECUTOR_ID=claude-code/gpt-5.6-sol:gsd-executor tools/phase1-python tools/validate-planning.py --phase-1-complete --executor-identity claude-code/gpt-5.6-sol:gsd-executor` | `P1-40-POST-001-RUN-09` | `tools/validate-planning.py` | passed |
| CR-04 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest` | `full suite; P1-40-POST-001-RUN-04` | `tools/validate-research.py` | passed |
| CR-05 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spike_consolidation.SpikeConsolidationTests.test_fragment_rejects_noncanonical_path_or_source_substitution` | `full suite; P1-40-POST-001-RUN-04` | `tools/validate-research.py` | passed |
| CR-06 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_replay_mapping_rejects_manifest_command_substitution` | `full suite; P1-40-POST-001-RUN-04` | `tools/validate-research.py` | passed |
| CR-07 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_consolidation_recovery.ObservedRefreshPublicationTests.test_observed_refresh_five_file_generation_recovers_after_each_replacement` | `full suite; P1-40-POST-001-RUN-04` | `tools/canonical-recovery.py` | passed |
| CR-08 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent` | `P1-40-DIRECT-P-EVID02-ADJ; #direct-attempt-p1-40-direct-p-evid02-adj` | `tools/validate-research.py` | passed |
| CR-09 | `tools/phase1-python --verify-toolchain` | `P1-40-POST-001-RUN-03` | `tools/verify-phase1-toolchain.py` | passed |
| WR-01 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest` | `full suite; P1-40-POST-001-RUN-04` | `tests/phase1/test_spikes.py` | passed |
| WR-02 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_evidence.SourceEvidenceTests.test_evidence_validation_uses_temporary_report_without_canonical_mutation` | `full suite; P1-40-POST-001-RUN-04` | `tests/phase1/test_evidence.py` | passed |
| WR-03 | `PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent` | `P1-40-DIRECT-P-OPER01-IDEMPOTENCY; #direct-attempt-p1-40-direct-p-oper01-idempotency` | `tools/refresh-sources.py` | passed |

## Truth and Blocker Analysis

- EVID-01, EVID-02, EVID-04, OPER-01, and OPER-03 direct regressions passed with fresh canonical evidence.
- EVID-03 remains terminally unresolved pending human evaluation of the substantive compatibility baseline or a D-26 impact-scoped safe fallback/defer determination. This candidate does not relabel blocked normative, package, runtime, example, fixture, or conformance evidence as verified.
- The ASVS L1 review passed with `open_high_count: 0`; its review and evidence digests are bound in the frontmatter.
- Firefox attachment, package provenance, immutable upstream-source/authenticity, and other retained research constraints remain visible; this dossier neither accepts risk nor authorizes ADR acceptance, external action, production scaffolding, release, Phase 2, or a phase transition.

## Terminal Boundary

No terminal result is declared here. Only a separately human-authored staged re-verification with two valid non-executor role records may determine `passed` or `blocked`; the three live terminal files remain unchanged by this task.
