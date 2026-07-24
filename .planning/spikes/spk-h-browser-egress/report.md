# SPK-H — Browser egress and CSP findings

SPK ID: SPK-H-BROWSER-EGRESS

Metadata path: metadata.yaml

## Research question

Under the exact SPK-C selected loading model—a top-level observer with an opaque-origin `srcdoc` guest in `sandbox="allow-scripts"` only—what do the named installed browsers observe for fetch, images/media, classic/module scripts, WebSocket, EventSource, workers, form/navigation, and referrer/origin when every network target is deterministic local loopback? Which facts remain separate from a future public-site CSP policy and from an upstream NIP statement?

## Sources and immutable revisions

- **Current upstream statement:** none was collected. The only source binding for a current NIP egress assertion is the complete blocked pair `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001`: archive commit `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`, locator `Source and claim record model`, SHA-256 `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`, retrieved `2026-07-24T00:00:00Z`, authority `planning-archive`, evidence class `project-policy`, maturity `accepted`. It is not browser or protocol proof.
- **Project-policy statement:** `SRC-POLICY-002` / `CLM-POLICY-001` pins commit `b534103068be8c07e6869bfb7290fb60fdd87c8c`, `.planning/governance/evidence-policy.md`, locator `Required fields and verification rule`, SHA-256 `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`, retrieved `2026-07-24T00:00:00Z`, authority/evidence class `project-policy`, maturity `accepted`. It requires this report to keep observation, policy, and inference separate.
- **Selected model input:** SPK-C metadata SHA-256 `39c876306da5d086ffdaa28114e648b092b5e242f858a02ceb8d7c9e2ed09c11`; SPK-C report SHA-256 `ad21b749834d8d4df9382a1b80eb9526f952da1d1c7132fb603561427a31738e`. Their pinned model is an opaque-origin `srcdoc` guest, `sandbox="allow-scripts"` only, and a top-level source-window observer.
- **Fixture evidence:** `fixture.html` SHA-256 `51bd5b65fb89ede010391b64e6db8222b4d91ec9e8ed499835375b3cb0f6811e`; runner `runner.py` SHA-256 `4da4d9a494d6605609f8b18d44a4e6781cb44012adaa60f0394426dc114afaa3`; environment `environment.json` SHA-256 `6e090da8b019135ff3991b472b352b2558c3176b3f29f0c315057e651de96633`; measurements `measurements.yaml` SHA-256 `5d91d92ea90c98e62d51119da6c5be3aae483501b4d9b6aa604bcb79298680d8`.

## Observations

**Observed browser behavior only.** These rows describe the fixture, browsers, versions, sandbox, CSP input, and local receipts. They do not establish a NIP or production-host rule.

| Browser | Five fresh-context samples | Eight declared channel groups | CSP-negative guest | Result |
| --- | --- | --- | --- | --- |
| Chromium / Google Chrome 150.0.7871.124 | 5/5 passed; elapsed 327.803–405.229 ms, median 333.707 ms | Fetch returned fixed local JSON; image/audio loaded; classic/module markers appeared; WebSocket and EventSource returned fixed values; fixed `blob:` worker returned `local-worker-ok`; form receipt was absent without `allow-forms`; top navigation raised `SecurityError`; `/headers` retained `Origin: null` and absent `Referer` for both recorded referrer modes. | `connect-src 'none'` rejected fetch and `img-src 'none'` rejected image before an endpoint receipt. | observed browser behavior for this fixture |
| Firefox 152.0.4 | 0/5 fixture samples observed | All eight groups blocked before execution | Not observed | The direct-installed process exited with code 0 during `BrowserType.launch` before Playwright 1.61.0 attached to a clean context. No browser-channel result exists. |

Chrome's local measurement CSP was `default-src 'none'; script-src 'unsafe-inline' LOOPBACK; connect-src LOOPBACK WS_LOOPBACK; img-src LOOPBACK; media-src LOOPBACK; worker-src blob: LOOPBACK; form-action LOOPBACK; base-uri 'none'; frame-src 'none'`. The loopback endpoint was ephemeral `127.0.0.1`, never a public target. The top-level observer source-mapped each guest result to the exact iframe window. No credential, account, upload, persistence, relay, wallet, external request, browser download, or explicit browser launch flag was used.

## Conflicts

There is no current immutable upstream NIP browser-egress statement to compare against, so no upstream conflict is resolved here. `DRF-EGRESS-001` remains blocked: a local Chrome observation and an unavailable Firefox run cannot settle mediated-access or browser-network protocol behavior. The repeated Firefox launcher outcome is a tooling execution block, not evidence that Firefox allows or denies any channel.

## Inference

The narrow supported inference is that this exact disposable fixture can observe all eight declared channel groups in the named Chrome environment while a semantic-negative child CSP rejects the two bounded regression attempts before local endpoint contact. The sandbox-only form and top-navigation outcomes are fixture observations under the recorded tokens; they do not generalize to an iframe with different sandbox tokens, CSP, origin, browser version, or host code.

## Prototype or measurement

Replay only with the project-approved isolated interpreter and direct-installed binaries:

```text
tools/phase1-python .planning/spikes/spk-h-browser-egress/runner.py \
  --fixture .planning/spikes/spk-h-browser-egress/fixture.html \
  --out /tmp/spk-h-browser-egress
```

The runner starts an ephemeral `127.0.0.1` server and removes only its own `/tmp` output directory. It creates one fresh context per sample, records every result and bounded endpoint receipt under `/tmp/spk-h-browser-egress`, and closes the server. Raw output digest: `b5a25132b43de628d1c20c28eb09cfd8e47ecb497b51ffbbdc23e5baf18d827c`.

## Recommendation

**Proposed project policy, not a protocol requirement or accepted ADR:** any future public teaching site should start from a restrictive CSP and allow only reviewable, build-specific sources required by its chosen static content and mediated capabilities. Do not use this proposal to claim that a NIP requires the CSP, that sandboxing alone blocks every channel, or that Chrome's fixture outcome is cross-browser evidence.

Retain this package as proposed blocked evidence for ADR-0005 and ADR-0014. A security owner must review any concrete production CSP separately; Phase 1 automation cannot accept an ADR or approve a security exception.

## Uncertainty

Material uncertainty remains. The only source bindings are project policy/archive records, not current upstream proof; Chrome covers one local fixture rather than a public-site configuration; the referrer/origin values are recorded rather than interpreted; the fixed `blob:` worker does not make a same-origin worker-loader claim; and Firefox supplied no attached-context result. `OQ-EGRESS-NIP-001` remains open: collect an immutable current NIP statement, a complete source/claim binding, and human protocol-technical review before teaching any upstream browser-egress rule.

## Affected phases and requirements

- **EVID-04 / Phase 01:** SPK-H supplies reproducible Chrome observation and an explicit Firefox blocker; the cross-browser mandatory spike result remains blocked.
- **ADR-0005 and ADR-0014:** receive a local, proposed security/egress input only; neither decision is accepted or selected by this report.
- **Phases 02 and 05:** retain a static/deferred fallback and must not turn this fixture or proposed CSP into a selected production host profile.
- **DRF-EGRESS-001:** remains blocked pending immutable upstream evidence and review.

## Owner and required approval

Owner: research owner. Required approval: dated human protocol-technical and security review, with accessibility, content-learning, product, and release review as applicable. Plan 01-28 owns canonical evidence consolidation and final security/egress synthesis; this local fragment is only a typed, immutable hand-off proposal.
