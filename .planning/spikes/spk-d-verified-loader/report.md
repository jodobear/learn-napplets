# SPK-D — Verified-loader feasibility report

SPK ID: SPK-D-VERIFIED-LOADER

Metadata path: metadata.yaml

## Research question

Can current, immutable, publicly reviewed evidence support a reproducible measurement of manifest resolution, identity mapping, signature/blob/aggregate verification, and exact-byte loading for a verified-loader profile?

## Sources and immutable revisions

- **Upstream fact:** none established. No current immutable upstream manifest, identity, signature, blob, aggregate, or reviewed loader implementation record exists in `source-registry.yaml`; this report does not infer one.
- **Blocked policy baseline:** every declared primitive in `metadata.yaml.sourceBindings` resolves to `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001`: commit `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`, locator `Source and claim record model`, content SHA-256 `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`, retrieved `2026-07-24T00:00:00Z`, authority `planning-archive`, evidence class `project-policy`, maturity `accepted`. It preserves the lack of current upstream proof and is not itself protocol authority.
- **Fixture and execution evidence:** `fixture.json` SHA-256 `7d5a04eb9b5684c147053ee913aae375fdd8a994ba7e15c9da309a3d1e944cc6`; exact artifact bytes SHA-256 `b83079843b0410559ad4e275557c4103d3a3b86026fc0bc9eccf62fe42e9607c`; one-byte mutation SHA-256 `34e7f0624caefa1b9e3257946df0eed0d37c0b6253c41d0a7d3975a622e39d9d`; `environment.json` SHA-256 `603fdef9b0d7948f52bfdb1c640b3f61c97debc549d2e7d9c054f188871bb6c1`; `measurements.yaml` SHA-256 `3ddb0748c92d44204647cea6f5261392b239de95c97de1473853dae7644c9143`; completed `metadata.yaml` SHA-256 `d4b83bb4d3eb6d49b5ed2ae804170bd1acba19332ec02a05e9f1c1f3a80a5781`.
- **Tooling:** the approved wrapper resolved to CPython `3.14.3`; `tools/phase1-python` SHA-256 `644981c1104123d43a8e2b4a9b5b0738ad790e6f80c2f712f185bfc76a5507e5`. The environment records only already approved Phase 1 dependencies. No package was installed or substituted.

## Observations

**Observed implementation behavior:** this was a local Python standard-library fixture-integrity observation, not a protocol implementation observation.

Five deterministic `tools/phase1-python` replays exited `0`. In every sample, the supplied 29-byte artifact decoded from its pinned hex form and matched SHA-256 `b83079843b0410559ad4e275557c4103d3a3b86026fc0bc9eccf62fe42e9607c`. The mutation changed only offset `0`, retained 29 bytes, and matched SHA-256 `34e7f0624caefa1b9e3257946df0eed0d37c0b6253c41d0a7d3975a622e39d9d`.

All six declared verification surfaces remained explicitly `blocked`: manifest resolution, identity mapping, signature verification, blob verification, aggregate verification, and exact-byte loader behavior. The relevant execution outcomes are `not-run`, not failures of an implemented verifier: immutable current source evidence and reviewed verifier provenance are absent. No signature, key, blob, aggregate, manifest, identity tuple, resolver, loader, network target, browser, credential, or external state was used.

## Conflicts

The archive identifies manifest and `(dTag, aggregateHash)` identity questions as high-risk drift topics, but it states that they are research questions rather than project-level resolutions. Because no current immutable upstream source is pinned, there is no normative statement against which this local fixture can be compared. The blocker is therefore retained rather than resolved by choosing a side.

## Inference

**Inference:** the exact local fixture can be replayed as a byte-integrity check, but that result cannot establish verified-loader feasibility. Digest equality for supplied bytes is not signature, blob, aggregate, manifest, identity, or loader verification. The absence of a reviewed surface prevents a successful or failed protocol-sensitive experiment.

## Prototype or measurement

No production prototype or loader was created. The bounded replay was run five times through the approved wrapper using the command declared in `metadata.yaml` and recorded in `measurements.yaml`:

```text
tools/phase1-python -c fixture-integrity-only
```

The full assertion decodes only the fixture's supplied hex bytes, compares their pinned SHA-256 values, confirms the one-byte mutation, and asserts that every unavailable surface remains blocked. It does not hand-roll or simulate cryptography. `environment.json` records direct installed browser inventory only; SPK-D did not execute a browser and does not alter the preserved SPK-C Firefox/Playwright blocker.

## Recommendation

**Project recommendation, not an accepted ADR:** retain SPK-D as a non-production blocked fixture and do not select a Profile 2 verified loader, teach manifest/identity behavior as settled, or treat byte-digest replay as cryptographic verification. Collect and review current immutable source records plus reviewed public verification provenance before attempting a supported feasibility measurement. No package addition or verifier substitution is authorized by this report.

## Uncertainty

Material uncertainty remains. The available bindings are project-policy/archive records, not current upstream proof. Every protocol-sensitive field remains blocked, including what the current manifest is, how identity maps, and what signature/blob/aggregate or exact-byte loading semantics should be verified. The local fixture contains synthetic bytes only by design; its behavior cannot resolve that uncertainty.

## Affected phases and requirements

- **EVID-04 / Phase 01:** SPK-D produces a reproducible, explicitly blocked feasibility result with pinned fixture, source, environment, and measurement evidence.
- **ADR-0005:** receives a proposed blocked input only; it cannot select a teaching-host/loader profile from this report.
- **ADR-0008:** receives a proposed blocked input only; no mediated verification or egress-adjacent authority conclusion is supported.
- **Phase 02:** must retain the current static/deferred fallback and must not create a verified-loader implementation from this fixture.

## Owner and required approval

Owner: research owner. Required approval: separate dated human protocol-technical, security, content-learning, accessibility, and product review as applicable. This report, its measurement, and validators preserve evidence structure only; they do not approve a claim, accept ADR-0005 or ADR-0008, authorize a dependency, or permit production scaffolding.
