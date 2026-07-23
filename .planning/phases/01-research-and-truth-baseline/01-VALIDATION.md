---
phase: 1
slug: research-and-truth-baseline
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-23
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for evidence records, mandatory spikes, refresh behavior, and governance outputs.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` plus repository structural validators |
| **Config file** | none — Wave 0 establishes `tests/phase1/` and schema-validation entry point |
| **Quick run command** | `tools/phase1-python tools/validate-planning.py` |
| **Full suite command** | `tools/phase1-python -m unittest discover -s tests/phase1 && tools/phase1-python tools/validate-planning.py --phase-1-complete` |
| **Estimated runtime** | Target: <60 seconds excluding browser/deployment spike replay |

---

## Sampling Rate

- **After every task commit:** Run `tools/phase1-python tools/validate-planning.py` plus narrow `tools/phase1-python -m unittest` module for changed requirement.
- **After every plan wave:** Run `tools/phase1-python -m unittest discover -s tests/phase1 && tools/phase1-python tools/validate-planning.py`.
- **Before `/gsd-verify-work`:** Full suite and all available deterministic spike replay commands must be green.
- **Max feedback latency:** 60 seconds for non-browser checks; long-running spike commands report measured duration separately.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-W0-EVID-01 | TBD | 0 | EVID-01 | T-01 evidence tampering | Missing immutable identity, locator, digest, authority, evidence, maturity, or source relation is rejected. | schema + semantic unit | `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_evidence*.py'` | ❌ W0 | ⬜ pending |
| 01-W0-EVID-02 | TBD | 0 | EVID-02 | T-02 silent drift | Volatile claims require conflicts, uncertainty, impact, refresh trigger, and append-only state history. | unit + fixture | `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_drift*.py'` | ❌ W0 | ⬜ pending |
| 01-W0-EVID-03 | TBD | 0 | EVID-03 | T-03 mixed baselines | Compatibility rows cannot reference unknown IDs or combine incompatible source baselines. | semantic unit | `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_compatibility*.py'` | ❌ W0 | ⬜ pending |
| 01-W0-EVID-04 | TBD | 0 | EVID-04 | T-04 unsafe/unreproducible spike | Spike envelopes record inputs, environment, commands, observations, limitations, digests, and replay result without secrets. | unit + integration | `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_spikes*.py'` | ❌ W0 | ⬜ pending |
| 01-W0-OPER-01 | TBD | 0 | OPER-01 | T-05 unauthorized rewrite | Refresh comparison emits review work and never auto-rewrites accepted claim prose or state. | integration fixture | `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_refresh*.py'` | ❌ W0 | ⬜ pending |
| 01-W0-OPER-03 | TBD | 0 | OPER-03 | T-06 bypassed governance | Phase records require owners, approvers, requirement links, exit evidence, and GSD verification status. | schema + semantic unit | `tools/phase1-python -m unittest discover -s tests/phase1 -p 'test_governance*.py'` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `.planning/research/schemas/` — Draft 2020-12 schemas for source, claim, drift, compatibility, open-question, spike, and phase-governance records.
- [ ] `tools/validate-research.py` or scoped extension to `tools/validate-planning.py` — safe YAML parsing, schema checks, semantic relation checks, and compact diagnostics.
- [ ] `tests/phase1/` — deterministic fixtures and tests for evidence, drift, compatibility, spike envelopes, refresh behavior, and governance.
- [ ] Human-approved pinned YAML/schema/browser toolchain — no package install before package-legitimacy checkpoint.
- [ ] `.gitignore` coverage for `.research/` plus bulky spike outputs and caches.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Approve proposed parser, schema validator, browser runner, and binaries before installation. | EVID-04 | Package legitimacy and environment changes require human approval. | Review package names, official sources, pinned versions, licenses, hashes where available, and requested install commands; record approval or blocker. |
| Review protocol-sensitive claims that remain conflicting, low-confidence, stale, or blocked. | EVID-01, EVID-02 | Automated checks can prove metadata completeness, not settle upstream meaning. | Inspect source registry, claim records, conflict links, uncertainty, drift state, affected requirements/phases, and refresh triggers; approve only source-backed wording. |
| Review mandatory spike observations before architecture recommendations. | EVID-04 | Browser, deployment, CSP, package-consumption, and portable-target observations require environment-aware judgment. | Replay documented command where available; inspect captured environment, inputs, outputs, limitations, and digests; record accepted evidence or explicit blocker. |
| Confirm ADRs remain proposals and no production app/framework scaffold exists. | OPER-03 | Phase boundary and ADR acceptance are project-owner gates. | Inspect ADR status fields and repository diff; reject accepted ADR status or production scaffold creation during Phase 1. |

---

## Validation Sign-Off

- [ ] Every plan task has automated verification or explicit Wave 0 dependency.
- [ ] Sampling continuity: no three consecutive tasks lack automated checks.
- [ ] Wave 0 covers every missing validator/test reference above.
- [ ] No watch-mode flags appear in verification commands.
- [ ] Non-browser feedback latency remains below 60 seconds.
- [ ] Mandatory spike replay commands and environment metadata are recorded.
- [ ] Human approval checkpoints are preserved for package installs, ADR acceptance, external actions, and Phase 1 closeout.
- [ ] `nyquist_compliant: true` set only after `/gsd-validate-phase` confirms coverage.

**Approval:** pending
