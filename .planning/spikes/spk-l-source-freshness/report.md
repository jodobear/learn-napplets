# SPK-L Source Freshness Evidence

SPK ID: SPK-L-SOURCE-FRESHNESS
Metadata path: metadata.yaml

## Research question

Can a deterministic local comparison route source identity drift to human review without rewriting accepted evidence?

## Sources and immutable revisions

 and  are read-only canonical inputs pinned in the source registry; this replay fetched and changed no live source.

## Observations

All seven fixture scenarios replayed locally. Unchanged and repeated runs exited 0 with identical report digest and no review work. Changed digest and moved path emitted stable review-required output retaining old pointer/digest. Unavailable and ambiguous emitted blocked review work. A held report lock made concurrent refresh exit 1 with a visible lock-busy error. Canonical registry, claims, drift, and question bytes stayed unchanged.

## Conflicts

Non-unchanged outcomes are mechanical identity conflicts, not semantic conclusions. They retain old identity and affected IDs for a human reviewer.

## Inference

The fixture supports an ADR 0011 proposal: changed/moved evidence requires stale review, while unavailable/ambiguous evidence remains blocked. It does not establish upstream fact or accept an ADR.

## Prototype or measurement

 ran local fixture inputs;  records exit codes and every report SHA-256. This is a deterministic local measurement, not a network or browser probe.

## Recommendation

Use stable source IDs, old identity retention, and deterministic review-work IDs for targeted D-36 research. Keep ADR 0011 proposed pending human protocol-technical approval.

## Uncertainty

The fixture proves tool routing only. It cannot determine changed upstream meaning, choose a cadence, rewrite accepted evidence, or make unavailable evidence fresh.

## Affected phases and requirements

Affected requirements: EVID-02, EVID-04, OPER-01. Affected phase: 01. Impacted ADR: ADR-0011, proposed and blocked for acceptance.

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical human review and content-learning review if teaching impact changes. Automation cannot rewrite claims, classifications, approvals, or ADR status.
