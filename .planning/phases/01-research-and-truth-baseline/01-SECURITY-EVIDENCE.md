# Phase 1 ASVS L1 Remediation-Evidence Dossier
#
# Automation-prepared evidence only. This document contains no security verdict,
# approval, waiver, accepted residual risk, or phase-transition determination.
# A non-executor human auditor and rechecker must independently inspect this dossier.

dossier_kind: phase1-asvs-l1-remediation-evidence
prepared_at: "2026-07-31T00:00:00Z"
prepared_by_executor: "claude-code/gpt-5.6-sol:gsd-executor"
independent_plan_review_identity: "codex-cli/0.146.0:gpt-5.6-sol:external-read-only"
reviewed_commit: 5c137af5c79e1ddecbd019c5f80c2ecdfcfc291a
active_plan_review_path: .planning/phases/01-research-and-truth-baseline/01-REVIEWS.md
active_plan_manifest_sha256: 8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95
asvs_reference_path: .planning/research/reports/asvs-reference-20260728.md
asvs_reference_sha256: 9569150eabab77b98a0536dd675361838d06735d5b24c14dcdf89535a19c855b
evidence_manifest_algorithm: "SHA-256 of canonical YAML mapping with evidence_manifest_sha256 omitted"
evidence_manifest_sha256: 3f229313a95c4875291e87edea437304ed51789007781f98dadb2c1edd39494c
verification_batch:
  executor_identity: "claude-code/gpt-5.6-sol:gsd-executor"
  commands:
    - command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_security_review.py'"
      result: "exit 0; 5 tests passed"
    - command: "tools/phase1-python -m unittest discover -s tests/phase1"
      result: "exit 0; 133 tests passed"
    - command: "GSD_EXECUTOR_ID=claude-code/gpt-5.6-sol:gsd-executor tools/phase1-python tools/validate-planning.py --phase-1-complete --executor-identity claude-code/gpt-5.6-sol:gsd-executor"
      result: "exit 0; 0 errors, 0 warnings"
findings:
  - id: CR-01
    threat: spoofing
    severity: high
    primary_coverage: citation provenance
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_preflight.Phase1ExecutionPreflightTests.test_citation_ascii_adjacency_extracts_exact_token"
    result: "exit 0; cited token adjacency is parsed exactly"
    source_path: tools/validate-planning.py
    applicable_asvs_ids: [v5.0.0-2.1.1, v5.0.0-2.2.1]
    evidence_locator: "tests/phase1/test_preflight.py::Phase1ExecutionPreflightTests.test_citation_ascii_adjacency_extracts_exact_token; 01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid01-adj"
  - id: CR-02
    threat: elevation-of-privilege
    severity: high
    primary_coverage: review convergence and HIGH parsing
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_preflight.Phase1ExecutionPreflightTests.test_preflight_requires_exact_convergence_and_high_disposition"
    result: "exit 0; non-converged review and unresolved HIGH dispositions are rejected"
    source_path: tools/validate-planning.py
    applicable_asvs_ids: [v5.0.0-2.2.2, v5.0.0-2.3.1]
    evidence_locator: "tests/phase1/test_preflight.py::Phase1ExecutionPreflightTests.test_preflight_requires_exact_convergence_and_high_disposition"
  - id: CR-03
    threat: elevation-of-privilege
    severity: high
    primary_coverage: certified-wrapper subprocess execution
    disposition: mitigated
    command: "GSD_EXECUTOR_ID=claude-code/gpt-5.6-sol:gsd-executor tools/phase1-python tools/validate-planning.py --phase-1-complete --executor-identity claude-code/gpt-5.6-sol:gsd-executor"
    result: "exit 0; completion gate ran through tools/phase1-python"
    source_path: tools/validate-planning.py
    applicable_asvs_ids: [v5.0.0-2.2.2]
    evidence_locator: "01-VALIDATION.md#prerequisite-gate-evidence; .planning/phases/01-research-and-truth-baseline/01-37-SUMMARY.md#closeout-evidence"
  - id: CR-04
    threat: tampering
    severity: high
    primary_coverage: retained output digest binding
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest"
    result: "exit 0; missing or mismatched retained output is rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-2.2.1]
    evidence_locator: "tests/phase1/test_spikes.py::SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest"
  - id: CR-05
    threat: tampering
    severity: high
    primary_coverage: confined canonical fragment paths
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spike_consolidation.SpikeConsolidationTests.test_fragment_rejects_noncanonical_path_or_source_substitution"
    result: "exit 0; escaping and substituted fragment paths are rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-5.3.2]
    evidence_locator: "tests/phase1/test_spike_consolidation.py::SpikeConsolidationTests.test_fragment_rejects_noncanonical_path_or_source_substitution"
  - id: CR-06
    threat: elevation-of-privilege
    severity: high
    primary_coverage: fixed replay command mapping
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_replay_mapping_rejects_manifest_command_substitution"
    result: "exit 0; manifest command substitution is rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-1.3.2]
    evidence_locator: "tests/phase1/test_spikes.py::SpikeValidationTests.test_replay_mapping_rejects_manifest_command_substitution"
  - id: CR-07
    threat: denial-of-service
    severity: high
    primary_coverage: publish interruption recovery
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_consolidation_recovery.ObservedRefreshPublicationTests.test_observed_refresh_five_file_generation_recovers_after_each_replacement"
    result: "exit 0; interrupted publication recovers a coherent generation"
    source_path: tools/canonical-recovery.py
    applicable_asvs_ids: [v5.0.0-2.3.1]
    evidence_locator: "tests/phase1/test_consolidation_recovery.py::ObservedRefreshPublicationTests.test_observed_refresh_five_file_generation_recovers_after_each_replacement"
  - id: CR-08
    threat: tampering
    severity: high
    primary_coverage: distinct parallel drift sides
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent"
    result: "exit 0; duplicate or collapsed drift sides are rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-2.2.2, v5.0.0-2.3.1]
    evidence_locator: "tests/phase1/test_drift.py::DriftSchemas.test_parallel_sides_are_distinct_and_adjacent; 01-VALIDATION.md#direct-attempt-p1-38-direct-p-evid02-adj"
  - id: CR-09
    threat: elevation-of-privilege
    severity: high
    primary_coverage: certified toolchain integrity
    disposition: mitigated
    command: "tools/phase1-python --verify-toolchain"
    result: "exit 0; certified interpreter, wheelhouse, and installed-record integrity verified"
    source_path: tools/verify-phase1-toolchain.py
    applicable_asvs_ids: [v5.0.0-11.4.1, v5.0.0-15.1.1, v5.0.0-15.2.1]
    evidence_locator: "tests/phase1/test_evidence.py::test_toolchain_integrity_blocks_untrusted_forwarding; .planning/phases/01-research-and-truth-baseline/01-37-SUMMARY.md#closeout-evidence"
  - id: WR-01
    threat: tampering
    severity: medium
    primary_coverage: retained-output fixture integrity
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest"
    result: "exit 0; fixture requires retained output before a complete result"
    source_path: tests/phase1/test_spikes.py
    applicable_asvs_ids: [v5.0.0-2.2.1]
    evidence_locator: "tests/phase1/test_spikes.py::SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest"
  - id: WR-02
    threat: tampering
    severity: medium
    primary_coverage: temporary report isolation
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_evidence.SourceEvidenceTests.test_evidence_validation_uses_temporary_report_without_canonical_mutation"
    result: "exit 0; validation report stays outside canonical planning state"
    source_path: tests/phase1/test_evidence.py
    applicable_asvs_ids: [v5.0.0-5.3.2]
    evidence_locator: "tests/phase1/test_evidence.py::SourceEvidenceTests.test_evidence_validation_uses_temporary_report_without_canonical_mutation"
  - id: WR-03
    threat: tampering
    severity: medium
    primary_coverage: ambiguous refresh reduction
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent"
    result: "exit 0; duplicate observations reduce deterministically without contradictory routing"
    source_path: tools/refresh-sources.py
    applicable_asvs_ids: [v5.0.0-2.1.1, v5.0.0-15.1.1]
    evidence_locator: "tests/phase1/test_drift.py::RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent; 01-VALIDATION.md#direct-attempt-p1-38-direct-p-oper01-idempotency"
research_constraints_outside_remediation_mapping:
  - "Immutable upstream source/authenticity evidence remains a research constraint; this dossier does not convert it to a mitigation, waiver, or accepted residual risk."
  - "Published-package provenance and integrity evidence remains blocked pending required source and review evidence; this dossier does not accept package risk."
  - "Firefox exited before approved Playwright attachment in retained probes; no Firefox result is solved or claimed by this dossier."
human_audit_boundary: "The security auditor must independently inspect the evidence, rerun selected wrapper commands, identify any stable SEC-* findings, and author a separate human review. Automation cannot certify a security status."
