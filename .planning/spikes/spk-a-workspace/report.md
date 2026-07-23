# SPK-A Workspace Evidence

SPK ID: SPK-A-WORKSPACE
Metadata path: metadata.yaml

## Research question

Can repository/workspace boundary candidates be compared reproducibly without initializing a production workspace?

## Sources and immutable revisions

SRC-POLICY-001 and SRC-POLICY-002 are the project-policy bindings declared in metadata.yaml. TSCOPE-001 and CMP-BASELINE-001 are local, blocked research inputs. This replay fetched no live source and establishes no upstream protocol fact.

## Observations

Five local fixture assertions each exited 0 and emitted fixture-contract-ok. Candidate A and Candidate C each score 7/7 on the predeclared boundary matrix; Candidate B scores 0/7. No root path listed in productionMarkersBlockedBeforePhase3 was created.

## Conflicts

Candidate A and Candidate C tie in conceptual boundary coverage. Candidate C describes a broader future workspace, while Candidate A is the narrowest public-site-first model. Neither comparison selects a package manager, framework, bundler, runtime, or deployment system.

## Inference

The local fixture supports a proposed repository boundary recommendation, not an accepted architecture. Its static reasoning is compatible with the blocked teaching scope and compatibility baseline; it cannot resolve their external-evidence blockers.

## Prototype or measurement

measurements.yaml records all five samples, candidate scores, input digest, output digest, and median-replay summary. environment.json records the actual approved Phase 1 runner, browser binaries, dependencies, flags, and command hashes. The comparison ran only local text assertions; it did not materialize candidate layouts, install dependencies, or contact a network service.

## Recommendation

Proposed ADR-0001 disposition: retain Candidate A as the narrowest future public-site-first repository/workspace boundary model, with separately named structured content, trusted host, and multiple guest entries. Keep Candidate C as an equivalent broader alternative for later Phase 3 workspace design. This recommendation remains proposed and requires project-owner review; no production workspace is authorized.

## Uncertainty

This is a text-only structural comparison, not a framework, bundle, package, browser, or deployment measurement. The tied score does not prove implementation feasibility. Selected runtime, host profile, operation, and public export evidence remain blocked.

## Affected phases and requirements

Affected requirement: EVID-04. Affected phases: 01, 02, and 03. Affected decision: ADR-0001, proposed only. Refresh trigger: when immutable runtime/package/deployment evidence or the Phase 3 scaffold gate changes.

## Owner and required approval

Owner: research-owner. Required approval: dated project-owner ADR-0001 review, with protocol-technical, security, accessibility, content-learning, and release review as applicable. Automation cannot accept the ADR or promote this disposable spike into a production scaffold.
