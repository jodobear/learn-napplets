# SPK-H — Browser egress and CSP evidence recipe

SPK-H is an isolated, disposable, **non-production** local browser experiment. It
creates no production host, route, framework, package, public site, account, secret,
upload, external request, or persistent browser state. Its only server binds loopback
`127.0.0.1` on an ephemeral port for the duration of the measurement and accepts only
fixture-defined paths.

## Selected model and evidence boundary

The fixture uses the selected SPK-C model without changing its trust shape:

- a top-level local observer creates an iframe;
- the iframe is `sandbox="allow-scripts"`, with no `allow-same-origin`, forms,
  popups, downloads, top navigation, storage access, or other capability token;
- the guest is an opaque-origin `srcdoc` document;
- the top-level observer receives a bounded `postMessage` result and checks
  `MessageEvent.source === iframe.contentWindow` before recording it.

The selected SPK-C metadata digest and report digest are pinned in `metadata.yaml`.
Rerun SPK-H only if that loading/sandbox model changes; a result from another iframe,
origin, browser, or CSP model is not substitutable evidence.

There is **no current immutable upstream NIP statement** in this spike. The complete
`SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` binding records that blocker, and
`SRC-POLICY-002` / `CLM-POLICY-001` records the project requirement to separate
facts, observations, policy, and inference. Any statement about a current NIP becomes
`OQ-EGRESS-NIP-001` until a complete immutable `SRC-*` / `CLM-*` pair is collected.
The preserved source-pack section 9H is planning context only, not current upstream
proof.

## Exact CSP inputs

The runtime replaces `LOOPBACK` with the bound `http://127.0.0.1:<ephemeral-port>`
and `WS_LOOPBACK` with its `ws://` counterpart **inside the guest template before it
is assigned to `srcdoc`**. The template itself is committed and digest-pinned.

| Mode | Exact guest CSP | Purpose | Classification |
| --- | --- | --- | --- |
| `local-channel-measurement` | `default-src 'none'; script-src 'unsafe-inline' LOOPBACK; connect-src LOOPBACK WS_LOOPBACK; img-src LOOPBACK; media-src LOOPBACK; worker-src blob: LOOPBACK; form-action LOOPBACK; base-uri 'none'; frame-src 'none'` | Permit only the deterministic local endpoints required to observe the declared channels. | observed-browser-behavior input, not a public policy recommendation |
| `semantic-negative-csp` | `default-src 'none'; script-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; media-src 'none'; worker-src 'none'; form-action 'none'; base-uri 'none'; frame-src 'none'` | Require the bounded local fetch and image attempts to reject before external endpoint contact. | observed-browser-behavior input, not an upstream requirement |

The top-level document has its own constrained CSP: `default-src 'none'; script-src
'unsafe-inline' http://127.0.0.1:*; style-src 'unsafe-inline'; connect-src
http://127.0.0.1:* ws://127.0.0.1:*; img-src http://127.0.0.1:*; media-src
http://127.0.0.1:*; worker-src blob: http://127.0.0.1:*; form-action
http://127.0.0.1:*; base-uri 'none'; frame-src 'none'`. It creates no network
channel itself; the inherited source list permits the opaque-origin guest's exact
local measurement CSP to be tested instead of silently blocking it at the parent.

## Predeclared clean-context matrix

Every sample uses one fresh Playwright context and one named direct-installed browser
without explicit browser CLI flags, profile, preference, or browser download.

| Channel group | Local endpoint / action | Expected bounded result | Failure / block meaning |
| --- | --- | --- | --- |
| Fetch | `GET /fetch` with CORS response | Fulfilled local JSON response and endpoint receipt | A rejection or missing receipt is a fixture/browser failure, not a protocol conclusion. |
| Images/media | `GET /pixel.png` and `GET /tone.wav` | Image load and audio `loadedmetadata`, with endpoint receipts | A failed resource result is a local observation only. |
| Classic/module scripts | `GET /classic.js` and `GET /module.js` | Both fixed markers become visible before channel run | Script outcome is not a browser security generalization. |
| WebSocket | Local HTTP upgrade at `/socket` | Fixed `local-websocket-ok` response after one fixed message | No public WebSocket target exists. |
| EventSource | `GET /events` | Fixed `local-event-source-ok` message, then client close | No public stream exists. |
| Workers | Fixed `blob:` worker created in the opaque-origin guest | Dedicated worker returns `local-worker-ok` without a network request | Worker runs only fixed fixture code; this records worker execution, not a same-origin worker-loader claim. |
| Form/navigation | `POST /form` attempt and `top.location` assignment to `/navigation` | Without sandbox tokens, no endpoint receipt; bounded sandbox failure is recorded | It does not prove a protocol or future host policy. |
| Referrer/origin | `GET /headers` with default and `referrerPolicy: 'no-referrer'` | Endpoint preserves received `Origin` and `Referer` values without interpretation | Values are recorded, not normalized into a claim. |

For each browser that reaches the fixture, all eight groups run five times. Every
nondeterministic elapsed measurement keeps all five values, range, and median. The
semantic-negative CSP runs fetch and image attempts as a regression guard. A browser
that exits before Playwright attachment records all channels as `blocked` with no
fixture observation.

## Replay

1. Validate the planned envelope.

   ```text
   tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-h-browser-egress --contract
   ```

2. Run the fixture only through the recorded isolated interpreter. The runner makes
   its temporary browser result files under `/tmp`; it starts and closes its own
   loopback server and does not leave a listener running.

   ```text
   tools/phase1-python .planning/spikes/spk-h-browser-egress/runner.py \
     --fixture .planning/spikes/spk-h-browser-egress/fixture.html \
     --out /tmp/spk-h-browser-egress
   ```

3. Use only `/opt/google/chrome/google-chrome` version `150.0.7871.124` and
   `/usr/bin/firefox` version `152.0.4` via Playwright `1.61.0`. Do **not** run
   `playwright install`, download a browser, add launcher flags, use a profile, add a
   preference, or work around Firefox if it exits before attachment.

4. Preserve `browser-results.json` and `manifest.json` only under `/tmp`; commit the
   bounded environment, measurements, report, and impact fragment. The runner exits
   successfully for an explicit browser `blocked` outcome and nonzero only for a
   fixture failure in a browser that attached.

5. Run complete validation and the semantic negative-fragment regression test:

   ```text
   tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-h-browser-egress --complete
   tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-h-browser-egress/report.md
   tools/phase1-python .planning/spikes/spk-h-browser-egress/negative-fragment-tests.py
   tools/phase1-python tools/validate-research.py validate-impact-fragment .planning/spikes/spk-h-browser-egress/impact-fragment.yaml --root .planning
   ```

## Reporting schema and outcome rules

The report must use the canonical ordered headings:

1. Research question
2. Sources and immutable revisions
3. Observations
4. Conflicts
5. Inference
6. Prototype or measurement
7. Recommendation
8. Uncertainty
9. Affected phases and requirements
10. Owner and required approval

Within each relevant heading, label one of four categories explicitly:

- **Current upstream statement:** none observed; preserve the blocked source binding
  and the dated `OQ-EGRESS-NIP-001` instead of inventing a NIP rule.
- **Observed browser behavior:** only the named browser/version, fixture digest,
  sandbox/CSP input, endpoint receipt, and raw result.
- **Proposed project policy:** a non-binding public-site CSP direction subject to
  separate security approval; it is not an upstream requirement.
- **Open upstream question:** evidence needed, affected decision, and refresh trigger.

A fixture failure, missing endpoint receipt, unexpected source-window mapping,
non-loopback request, secret, browser mismatch, or Firefox launch failure is retained
as failed/blocked evidence. It never authorizes a production host, CSP deployment,
ADR acceptance, or a claim that sandboxing/CSP universally blocks a channel.
