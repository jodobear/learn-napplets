---
phase: 01-research-and-truth-baseline
review_source: 01-REVIEWS.md
authority: human-plan-review
status: in_progress
started: 2026-07-28
completed_items: 3
total_items: 8
---

# Phase 1 Manual Convergence Review

Review each current external finding separately before targeted replanning.

| Item | Severity | Scope | Decision | Rationale | Plan change required |
|---|---|---|---|---|---|
| 1 | HIGH | Plan 01-29 bootstrap ordering | Accept correction | A trust gate cannot safely invoke `tools/phase1-python` before a stdlib-only pre-site bootstrap proves startup hooks and site processing cannot execute first. | Move creation/direct verification of `tools/phase1-bootstrap.py` into Task 1; run recorded interpreter with `-I -S` and malicious-`.pth` regression before wrapper authorization; retain full lock/RECORD work in Task 2. |
| 2 | HIGH | Plans 01-39/01-40 validator ownership | Add explicit tasks | Trust-policy validators must be defined, tested, and reviewed before a human checkpoint relies on them; checkpoint-time implementation would bypass plan review. | Add dedicated pre-checkpoint TDD tasks for `tools/validate-phase1-security.py` and `tools/validate-phase1-terminal.py`, including focused negative regressions, `files_modified`, artifact lists, and exact verify commands. |
| 3 | HIGH | Plan 01-40 terminal publication ordering | Stage, validate, publish | Writing live terminal artifacts before validation can expose a contradictory or mixed authoritative generation after failure or interruption. | Human authors staged `REVERIFICATION`/`STATE`/`ROADMAP`; terminal validator checks the bound staged set; Plan 01-42 journal/recovery atomically publishes all three only after pass; add interruption coverage. |

## Pending

3. Validate-before-atomic-terminal-publication ordering.
4. ASVS extensible finding model.
5. Identity rules versus one-user multi-role governance.
6. Task-local boundary regressions.
7. Direct registry receipt validation.
8. Toolchain freshness and transitive-lock approval authority.
