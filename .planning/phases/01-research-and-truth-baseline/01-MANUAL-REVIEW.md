---
phase: 01-research-and-truth-baseline
review_source: 01-REVIEWS.md
authority: human-plan-review
status: in_progress
started: 2026-07-28
completed_items: 5
total_items: 8
---

# Phase 1 Manual Convergence Review

Review each current external finding separately before targeted replanning.

| Item | Severity | Scope | Decision | Rationale | Plan change required |
|---|---|---|---|---|---|
| 1 | HIGH | Plan 01-29 bootstrap ordering | Accept correction | A trust gate cannot safely invoke `tools/phase1-python` before a stdlib-only pre-site bootstrap proves startup hooks and site processing cannot execute first. | Move creation/direct verification of `tools/phase1-bootstrap.py` into Task 1; run recorded interpreter with `-I -S` and malicious-`.pth` regression before wrapper authorization; retain full lock/RECORD work in Task 2. |
| 2 | HIGH | Plans 01-39/01-40 validator ownership | Add explicit tasks | Trust-policy validators must be defined, tested, and reviewed before a human checkpoint relies on them; checkpoint-time implementation would bypass plan review. | Add dedicated pre-checkpoint TDD tasks for `tools/validate-phase1-security.py` and `tools/validate-phase1-terminal.py`, including focused negative regressions, `files_modified`, artifact lists, and exact verify commands. |
| 3 | HIGH | Plan 01-40 terminal publication ordering | Stage, validate, publish | Writing live terminal artifacts before validation can expose a contradictory or mixed authoritative generation after failure or interruption. | Human authors staged `REVERIFICATION`/`STATE`/`ROADMAP`; terminal validator checks the bound staged set; Plan 01-42 journal/recovery atomically publishes all three only after pass; add interruption coverage. |
| 4 | HIGH | Plan 01-39 ASVS finding extensibility | Allow SEC findings | A complete ASVS review must represent new issues it discovers; an exact-CR/WR-only global set can omit or misclassify a newly discovered HIGH issue. | Keep CR-01..CR-09 and WR-01..WR-03 as exact required subset; add stable optional `SEC-*` findings linked to applicable ASVS controls; require evidence/results; count unresolved HIGH across both sets and block pass. |
| 5 | HIGH | Plans 01-39/01-40 identity policy | Role-bound same person | Locked D-27/D-28 permits one user across roles while requiring separate dated per-role determinations; distinct-person requirements would make legitimate completion impossible and invite fabricated identities. | Allow repeated human principal across roles; require separate role, timestamp, commit/artifact digests, determination, and rationale records; forbid generic approval reuse and automation/executor human sign-off. |

## Pending

6. Task-local boundary regressions.
7. Direct registry receipt validation.
8. Toolchain freshness and transitive-lock approval authority.
