# SPK-L — Deterministic Source-Freshness Replay

This is a disposable, non-production local fixture. It does not fetch, modify, or replace upstream sources or canonical evidence.

## Inputs

- `fixture.yaml` defines all local comparison scenarios and expected review routing.
- Canonical records are read-only inputs: source registry, claims, drift register, and open questions.
- `tools/refresh-sources.py` writes a scenario-local report only.

## Procedure

1. Copy the fixture comparison JSON for one named scenario into an isolated temporary directory.
2. Record SHA-256 digests of the canonical claims, registry, drift, question, and ADR records before replay.
3. Run `tools/phase1-python tools/refresh-sources.py` with the canonical inputs and a temporary report path.
4. For `repeated-run`, run the exact command twice and compare report bytes.
5. For `concurrent-refresh`, hold the report lock, run the command, and record its bounded lock-busy result; release the lock and rerun normally.
6. Compare canonical-record digests after every scenario. A mismatch is failure: no canonical claim text, evidence class, maturity, review/approval, or ADR outcome may be automatically changed.
7. Record each result, stable review-work ID, old identity/replacement history, affected IDs, and report digest in `measurements.yaml`.

## Expected routing

| Scenario | Outcome | Review routing | Canonical effect |
| --- | --- | --- | --- |
| unchanged / repeated run | unchanged | none; no duplicate | retain identity and state |
| changed digest / moved path | changed | stable review work with affected IDs | retain old pointer/digest and mark review-required |
| unavailable / ambiguous | unavailable / ambiguous | stable blocked review work | retain history; do not claim freshness |
| concurrent refresh | bounded lock conflict | visible retryable conflict | no interleaved report or canonical write |

All non-unchanged results are targeted research triggers under D-36. They are ADR 0011 proposal inputs only and require human protocol-technical review; they never accept an ADR.
