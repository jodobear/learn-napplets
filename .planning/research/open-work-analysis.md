# Current Work Analysis

## Research question

Which current NIP-5D, NAP, `napplet/web`, and runtime issue/PR/discussion signals require a compatibility or architecture revisit?

## Sources and immutable revisions

- `SRC-POLICY-001` pins the preserved research-question seed; it is project-policy evidence, not an upstream protocol source.
- `SRC-POLICY-002` pins the project evidence policy that classifies unresolved retrieval as blocked.
- `open-work-snapshot.json` records the dated candidate metadata results. No current-work item has an immutable upstream revision in this snapshot.

## Observations

The bounded candidate inventory retains NIP-5D, NAP registry/projection, `napplet/web`, and credible runtime surfaces. The snapshot records each as unavailable for immutable issue/PR/discussion metadata collection and maps the affected `DRF-*` records.

## Conflicts

No normative upstream side and observed implementation side are available to compare. The absence of an immutable current-work reference is a blocker, not evidence that an archived question or private implementation remains current.

## Inference

Directional work can identify what to revisit, but cannot be sole proof of released package, runtime, or protocol behavior under D-06.

## Prototype or measurement

None. This analysis records metadata provenance only; no implementation, package, runtime, or browser behavior was measured.

## Recommendation

Keep the compatibility row and dependent ADRs blocked. Re-run bounded official-source acquisition when a public immutable source, release, issue, PR, or discussion revision is available, then create a new dated snapshot instead of overwriting this one.

## Uncertainty

Material. The exact current status, scope, and behavior of all named surfaces remains unknown without immutable retrieval. Snapshot items are directional evidence and revisit triggers only.

## Affected phases and requirements

- Phase: `01`
- Requirements: `EVID-02`, `EVID-03`, `OPER-01`
- Drift records: `DRF-DISCOVERY-001`, `DRF-HANDSHAKE-001`, `DRF-MANIFEST-001`, `DRF-IDENTITY-001`, `DRF-METADATA-001`, `DRF-INTENT-001`, `DRF-UNKNOWN-MESSAGES-001`, `DRF-ARTIFACT-001`, `DRF-EGRESS-001`, `DRF-CONFORMANCE-001`

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical and content-learning human review. Automation may open targeted review work but must not interpret this directional snapshot as accepted behavior.
