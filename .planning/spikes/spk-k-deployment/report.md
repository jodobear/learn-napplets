# SPK-K Deployment/publication evidence

SPK ID: SPK-K-DEPLOYMENT
Metadata path: metadata.yaml

## Research question

Can bounded local static artifact assembly provide auditable evidence for the public-site, lab-artifact, and optional portable-output categories without claiming external hosting, publication, deployment, or release?

## Sources and immutable revisions

`SRC-POLICY-001` is the preserved deployment-planning context; it is not current upstream proof. `SRC-POLICY-002` is the project evidence policy. `CMP-BASELINE-001` and `TSCOPE-001` remain blocked inputs: neither supplies a selected runtime, package, host profile, domain operation, or portable target. The local fixture digest is `1f30bb1a2c4c63715b94ce85d1f95a68f5eefc8eaf749e86e4008b0ecddebfe0`; the local runner digest is `17b661472935df263603ec6efde06973c4c5a0e765adf170432b7e4c84aef793`.

## Observations

Task 2 selected `local-only` on 2026-07-24. The replay executed zero external operations. It did not access an account or credential, look up a target, configure a remote, start a listener, deploy, publish, or write outside the local disposable SPK-K output directory. The replay assembled three static artifacts below `.planning/spikes/spk-k-deployment/.experiment/local-artifacts/`, verified each payload and manifest SHA-256, passed static inspection and path-isolation checks for all three artifacts, and removed the output directory successfully.

The local artifact payload byte counts were 247 for `public-site-static`, 101 for `lab-artifact-placeholder`, and 104 for `portable-output-placeholder`. The deterministic replay digest after digest verification was `f9d777acf32478dfe5e4ca69b96280e89b0cc045d6c97b9db603f42635033aaa`.

## Conflicts

The preserved plan calls for deployment/publication assessment, while present project policy prohibits an external write without explicit authorization. Local assembly and static inspection are not externally hosted preview or publication evidence. No conflict is resolved by treating local files as public deployment.

## Inference

The local fixture demonstrates only that three artifact categories can be kept distinct, digest-pinned, inspected without a network listener, confined below the disposable spike directory, and rolled back. It does not demonstrate provider behavior, public reachability, a hosting configuration, runtime compatibility, a lab host, package output, portable compatibility, publication, or release.

## Prototype or measurement

`tools/phase1-python` ran the committed local `runner.py` once to assemble the fixture and once with `--rollback` to re-verify payload digests and remove the artifacts. `measurements.yaml` retains the three artifact identities, aggregate 452 payload bytes, three successful static-inspection checks, three successful isolation checks, one successful rollback, zero external operations, and the replay digest. No network or browser command ran.

## Recommendation

For ADR-0003, retain local artifact evidence as proposed, non-production evidence only. Record deployment and publication as `SPK-K-BLOCKED-EXTERNAL-AUTHORIZATION-MISSING` until a future separately authorized named disposable-sandbox probe is approved with target, exact command, cleanup, retention, owner, security/release sign-offs, credential handling, and result-digest policy. This report does not recommend a provider, target, production release, or ADR acceptance.

## Uncertainty

Material. The local-only replay cannot establish external hosting, public delivery, release identity, a real lab artifact, optional portable output, or current upstream behavior. The static artifact payloads are measurement fixtures, not product implementations.

## Affected phases and requirements

Affected requirement: `EVID-04`. Affected phase: `01`; downstream delivery, teaching-host, portability, and release work remain impacted. Affected ADR: `ADR-0003`, proposed only. External deployment/publication is impact-scoped blocked evidence, not a passed Phase 1 gate.

## Owner and required approval

Owner: research-owner. Task 2 decision recorded by the project operator as `local-only` on 2026-07-24. Any future external write requires a new explicit named-target authorization and dated security and release sign-offs before an external command becomes eligible. Product/technical ADR review remains separate; automation cannot accept ADR-0003 or release an artifact.
