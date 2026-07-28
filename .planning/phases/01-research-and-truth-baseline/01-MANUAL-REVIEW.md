---
phase: 01-research-and-truth-baseline
review_source: 01-REVIEWS.md
authority: human-plan-review
status: completed
started: 2026-07-28
completed_items: 8
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
| 6 | MEDIUM | Plans 01-29/01-36/01-42 task-local regressions | Require task-local tests | A task cannot claim its core boundary behavior when its own completion command never executes the named regression; aggregate closeout is later defense, not primary evidence. | Add exact wrapper-routed test addresses for duplicate authorization sections, sandbox escape/unavailability, direct validate-planning recovery, and all-reader recovery to owning task verify blocks; missing method must fail. |
| 7 | MEDIUM | Plan 01-41 direct registry receipt validation | Require direct validation | A schema unit test can pass while the collector never runs, the receipt is absent, or its digest does not match the exact response bytes. Fixture evidence proves collector mechanics but cannot establish a live published-package fact. | Make Task 1 own the collector and receipt; always execute bounded fixture mode; recompute and validate the receipt SHA-256 from captured response bytes; run bounded live mode only when D-10/D-24 permit it, otherwise retain an impact-scoped blocker. |
| 8 | MEDIUM | Plan 01-29 review freshness and transitive lock authority | Digest + automation | Exact plan digests and reviewed commit already invalidate stale review content when plan bytes change; arbitrary elapsed-time expiry adds delay without protecting unchanged plans. Resolver-selected dependencies need reproducible integrity controls, not per-package human ceremony. | Remove time-based review expiry; invalidate review on any bound plan/commit change or explicit supersession. Human approval covers top-level research-tool scope; automation derives the full closure, locks versions and artifact hashes, and runs license/integrity/security gates. Escalate only policy failures or scope changes. |

## Review Complete

All eight current findings have human decisions. Apply targeted plan corrections, rerun external convergence, and execute only after zero HIGH and zero actionable findings.
