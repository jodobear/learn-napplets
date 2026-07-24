# SPK-C — Sandboxed Browser Boundary Harness Report

SPK ID: SPK-C-BOUNDARY-HARNESS

Metadata path: metadata.yaml

## Research question

Can a local, `sandbox="allow-scripts"` iframe fixture prove the declared pre-script injection, bounded `postMessage` exchange, `MessageEvent.source` mapping, declared-domain removal error, envelope capture, and deterministic response in both separately pinned installed browsers without creating a trusted host or asserting upstream napplet behavior?

## Sources and immutable revisions

- **Pinned upstream statement:** none. `metadata.yaml.sourceBindings` resolves every primitive to `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001`, whose immutable archive pin is commit `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`, locator `Source and claim record model`, SHA-256 `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`, retrieved `2026-07-24T00:00:00Z`, authority `planning-archive`, evidence class `project-policy`, maturity `accepted`. The linked claim is blocked and is not a source of browser or protocol behavior.
- **Fixture evidence:** `fixture.html` SHA-256 `acc7a1655bac027301185de1fd16c8dc8b6056443ff77e2c0f92b0970d9211df`; isolated runner `runner.py` SHA-256 `a50cf27b80770d27a96168fa5ea1fe7daf3ef49b4455d7da3ab326def0059125`; completed `metadata.yaml` SHA-256 `39c876306da5d086ffdaa28114e648b092b5e242f858a02ceb8d7c9e2ed09c11`.
- **Execution environment:** `environment.json` SHA-256 `c21cb7cf5ed85c496b1e97facb0d69389d772f23c142e8112b57cb31f9f3e695` records approved `playwright==1.61.0`, Google Chrome `150.0.7871.124` at the pinned installed executable, Firefox `152.0.4` at `/usr/bin/firefox`, headless mode, and no requested managed browser download.

## Observations

These are **observed browser/tooling results**, not upstream protocol facts.

| Browser | Five clean-context samples | Actual observed fixture result | Classification |
| --- | --- | --- | --- |
| Chromium / Google Chrome 150.0.7871.124 | 5/5 passed | Each sample acknowledged `pre-guest-script`, mapped `MessageEvent.source` to the iframe window, returned `local-service-ok` with the declared domain, and returned `declared-domain-missing` after removal. Elapsed range: 29.556–39.305 ms; median: 33.352 ms. | observed browser behavior |
| Firefox 152.0.4 | 0/5 fixture samples observed | The installed process exited with code 0 during `BrowserType.launch` before Playwright 1.61.0 attached to a clean context. No injection, source mapping, envelope, or response behavior was observed. | blocked execution outcome |

`measurements.yaml` SHA-256 `743d2a9f369312c2dd410d4d77a30a658f0ef21204b8f609cb2b8bc4cb5777d3` preserves every Chromium elapsed value, every Chromium result envelope, all five Firefox launch attempts, and the explicit unavailable timing sentinel. No network target, credential, relay, wallet, upload, external state, or top-level guest execution was used.

## Conflicts

There is no pinned upstream browser or napplet statement to compare against, so this measurement cannot resolve an upstream conflict. The required cross-browser observation is incomplete: Chromium passed the isolated fixture while Firefox never reached fixture execution. That is a direct tooling/runtime block, not evidence that Firefox supports or rejects the declared boundary model.

## Inference

The narrow supported inference is that this exact disposable fixture behaved as specified in the recorded Chromium environment. It does not select a teaching-host profile, prove `document.domain` behavior, establish a napplet wire protocol, or generalize to Firefox. The absence of a Firefox fixture observation keeps the overall SPK-C result blocked.

## Prototype or measurement

Replay only with the approved isolated toolchain and direct installed browsers:

```text
tools/phase1-python .planning/spikes/spk-c-boundary-harness/runner.py
tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-c-boundary-harness --complete
```

The runner creates a fresh Playwright context for every sample, uses only `/opt/google/chrome/google-chrome` and `/usr/bin/firefox`, and writes no artifact. It deliberately exits nonzero while the Firefox row is blocked. Do not run `playwright install`, download a managed browser, or replace the failed Firefox surface.

## Recommendation

**Proposed host policy, not accepted architecture:** retain the fixture and its bounded top-level observer pattern as candidate ADR-0005 evidence only. Do not treat the fixture as a production host, and do not select it for Phase 2 or Phase 5 while the Firefox evidence is blocked and the upstream source bindings remain blocked.

## Uncertainty

Material uncertainty remains. The source records are project-policy/archive inputs, not current upstream proof; the local fixture omits real authority, services, and protocol domains by design; and the direct-installed Firefox/Playwright mismatch prevents a cross-browser conclusion. Human protocol-technical, security, accessibility, content-learning, and product review remains required before any ADR acceptance.

## Affected phases and requirements

- **EVID-04 / Phase 01:** SPK-C produces a truthful blocked cross-browser result with reproducible Chromium evidence and a Firefox execution blocker.
- **ADR-0005:** receives proposed evidence only; it cannot be accepted from this report.
- **Phases 02 and 05:** must retain a static/deferred fallback and cannot treat the fixture as a selected real teaching-host profile.

## Owner and required approval

Owner: research owner. Required approval: separate dated human protocol-technical, security, accessibility, content-learning, and product review as applicable. This report and its validators record evidence structure only; they do not approve a claim, accept ADR-0005, or authorize a production host.
