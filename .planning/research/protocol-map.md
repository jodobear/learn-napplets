# Protocol and Taxonomy Evidence Map

## Research question

What do current authoritative sources establish about NIP-5D/NIP-5A scope, loading, sandboxing, transport, sender, manifest, identity, registry/projection taxonomy, capability bootstrap, domains, archetypes, conventions, and a first-lab candidate?

## Sources and immutable revisions

- `SRC-POLICY-001` and `SRC-POLICY-002` are immutable project-policy records, not current upstream protocol evidence.
- No `SRC-*` current upstream protocol record was collected in this bounded run. Candidate names and mutable discovery pointers are retained in `candidate-source-manifest.yaml` but are not evidence.

## Observations

- The candidate manifest identifies the required authority surfaces and records every one as blocked or deferred rather than converting a discovery pointer into a fact.
- `CLM-UPSTREAM-BASELINE-001` records the resulting project-policy gate.

## Conflicts

No credible upstream conflict can be compared until at least two pinned authoritative/observed records exist. No winner is selected.

## Inference

None. A missing immutable record cannot support inference about protocol behavior.

## Prototype or measurement

None. No protocol/browser/runtime observation is claimed by this map.

## Recommendation

Use `tools/acquire-sources.py` only with allowlisted official HTTPS candidates and read-only local Git resolution; collect a complete `SRC-*` record before creating any upstream-fact, proposal, or observed-implementation claim. Keep first-lab selection blocked.

## Uncertainty

Material. Current NIP/NAP meaning, runtime behavior, package identity, domains, archetypes/conventions, and pedagogical first-lab suitability remain blocked. Refresh when an official repository/path/ref is confirmed.

## Affected phases and requirements

- Requirements: `EVID-01`, `EVID-02`
- Phase: `01`
- Downstream work: compatibility assessment, mandatory protocol-related spikes, and first-lab recommendation.

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical and content-learning human review. Automation must not mark this evidence verified.
