---
review_date: "2026-07-30"
scope: "Phase 1 ASVS L1 remediation review"
asvs_level: L1
blocking_threshold: high
reviewed_commits:
  - 5c137af5c79e1ddecbd019c5f80c2ecdfcfc291a
reviewed_plan_manifest_sha256: 8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95
reviewed_evidence_manifest_sha256: 3f229313a95c4875291e87edea437304ed51789007781f98dadb2c1edd39494c
status: passed
open_high_count: 0
securityAuditor:
  role: securityAuditor
  principal: jo
  timestamp: "2026-07-30T21:10:03Z"
  reviewed_commit: 5c137af5c79e1ddecbd019c5f80c2ecdfcfc291a
  reviewed_plan_manifest_sha256: 8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95
  reviewed_evidence_manifest_sha256: 3f229313a95c4875291e87edea437304ed51789007781f98dadb2c1edd39494c
  asvs_reference_sha256: 9569150eabab77b98a0536dd675361838d06735d5b24c14dcdf89535a19c855b
  determination: Passed
  rationale: "reviewed the bound dossier and independently reran CR-01, CR-05, CR-07, CR-09, and the ASVS security regression suite; all five sampled checks passed; no new SEC finding was observed."
securityRechecker:
  role: securityRechecker
  principal: jo
  timestamp: "2026-07-30T21:15:38Z"
  reviewed_commit: 5c137af5c79e1ddecbd019c5f80c2ecdfcfc291a
  reviewed_plan_manifest_sha256: 8d7a03fd1948e74e3dcca6b3be8ee2cd3f4f09e5e092470f9898193d1a0b9f95
  reviewed_evidence_manifest_sha256: 3f229313a95c4875291e87edea437304ed51789007781f98dadb2c1edd39494c
  asvs_reference_sha256: 9569150eabab77b98a0536dd675361838d06735d5b24c14dcdf89535a19c855b
  determination: Confirmed
  rationale: "independently confirmed the audit determination against sampled results and bound artifacts; required CR/WR dispositions remain mitigated; no unresolved HIGH or new SEC finding was reported."
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
  - id: CR-02
    threat: elevation-of-privilege
    severity: high
    primary_coverage: review convergence and HIGH parsing
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_preflight.Phase1ExecutionPreflightTests.test_preflight_requires_exact_convergence_and_high_disposition"
    result: "exit 0; non-converged review and unresolved HIGH dispositions are rejected"
    source_path: tools/validate-planning.py
    applicable_asvs_ids: [v5.0.0-2.2.2, v5.0.0-2.3.1]
  - id: CR-03
    threat: elevation-of-privilege
    severity: high
    primary_coverage: certified-wrapper subprocess execution
    disposition: mitigated
    command: "GSD_EXECUTOR_ID=claude-code/gpt-5.6-sol:gsd-executor tools/phase1-python tools/validate-planning.py --phase-1-complete --executor-identity claude-code/gpt-5.6-sol:gsd-executor"
    result: "exit 0; completion gate ran through tools/phase1-python"
    source_path: tools/validate-planning.py
    applicable_asvs_ids: [v5.0.0-2.2.2]
  - id: CR-04
    threat: tampering
    severity: high
    primary_coverage: retained output digest binding
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest"
    result: "exit 0; missing or mismatched retained output is rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-2.2.1]
  - id: CR-05
    threat: tampering
    severity: high
    primary_coverage: confined canonical fragment paths
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spike_consolidation.SpikeConsolidationTests.test_fragment_rejects_noncanonical_path_or_source_substitution"
    result: "exit 0; escaping and substituted fragment paths are rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-5.3.2]
  - id: CR-06
    threat: elevation-of-privilege
    severity: high
    primary_coverage: fixed replay command mapping
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_replay_mapping_rejects_manifest_command_substitution"
    result: "exit 0; manifest command substitution is rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-1.3.2]
  - id: CR-07
    threat: denial-of-service
    severity: high
    primary_coverage: publish interruption recovery
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_consolidation_recovery.ObservedRefreshPublicationTests.test_observed_refresh_five_file_generation_recovers_after_each_replacement"
    result: "exit 0; interrupted publication recovers a coherent generation"
    source_path: tools/canonical-recovery.py
    applicable_asvs_ids: [v5.0.0-2.3.1]
  - id: CR-08
    threat: tampering
    severity: high
    primary_coverage: distinct parallel drift sides
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.DriftSchemas.test_parallel_sides_are_distinct_and_adjacent"
    result: "exit 0; duplicate or collapsed drift sides are rejected"
    source_path: tools/validate-research.py
    applicable_asvs_ids: [v5.0.0-2.2.2, v5.0.0-2.3.1]
  - id: CR-09
    threat: elevation-of-privilege
    severity: high
    primary_coverage: certified toolchain integrity
    disposition: mitigated
    command: "tools/phase1-python --verify-toolchain"
    result: "exit 0; certified interpreter, wheelhouse, and installed-record integrity verified"
    source_path: tools/verify-phase1-toolchain.py
    applicable_asvs_ids: [v5.0.0-11.4.1, v5.0.0-15.1.1, v5.0.0-15.2.1]
  - id: WR-01
    threat: tampering
    severity: medium
    primary_coverage: retained-output fixture integrity
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_spikes.SpikeValidationTests.test_complete_spike_requires_retained_output_and_bound_replay_digest"
    result: "exit 0; fixture requires retained output before a complete result"
    source_path: tests/phase1/test_spikes.py
    applicable_asvs_ids: [v5.0.0-2.2.1]
  - id: WR-02
    threat: tampering
    severity: medium
    primary_coverage: temporary report isolation
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_evidence.SourceEvidenceTests.test_evidence_validation_uses_temporary_report_without_canonical_mutation"
    result: "exit 0; validation report stays outside canonical planning state"
    source_path: tests/phase1/test_evidence.py
    applicable_asvs_ids: [v5.0.0-5.3.2]
  - id: WR-03
    threat: tampering
    severity: medium
    primary_coverage: ambiguous refresh reduction
    disposition: mitigated
    command: "PYTHONPATH=tests/phase1 tools/phase1-python -m unittest test_drift.RefreshComparisonTests.test_duplicate_refresh_observations_are_idempotent"
    result: "exit 0; duplicate observations reduce deterministically without contradictory routing"
    source_path: tools/refresh-sources.py
    applicable_asvs_ids: [v5.0.0-2.1.1, v5.0.0-15.1.1]
---

# Phase 1 ASVS L1 Security Review

## Human audit record

Human determinations were captured interactively. Automation only transcribed the supplied determinations and mechanically validated their bindings; it is not a human signatory.

The human auditor independently executed `/tmp/learn-napplets-01-39-human-audit.sh` and recorded the following sampled results in `/tmp/learn-napplets-01-39-human-audit-results.txt`:

| Sample | Human-observed result |
| --- | --- |
| CR-01 citation provenance | PASS |
| CR-05 canonical path confinement | PASS |
| CR-07 interrupted publication recovery | PASS |
| CR-09 certified toolchain integrity | PASS |
| ASVS security policy regressions | 5 tests PASS |
| Summary | PASS=5 FAIL=0 |

## Finding register binding

The frontmatter contains exactly CR-01 through CR-09 and WR-01 through WR-03. For each required finding, its command, result, source path, and applicable ASVS controls mechanically equal the bound remediation-evidence dossier.

## New security findings

No new `SEC-*` finding was reported by human review. This is a human audit observation; it does not assert that automation proved none exist.

## Research constraints outside remediation mapping

Immutable upstream source/authenticity evidence, published-package provenance and integrity evidence, and the retained Firefox probe blocker remain research constraints. This review neither accepts them as residual risk nor treats them as resolved.

## Authority boundary

This passed local ASVS L1 remediation review does not establish protocol behavior, accept an ADR, authorize a phase transition, or authorize production scaffolding.
