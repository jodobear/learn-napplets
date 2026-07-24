# SPK-C — Sandboxed Real-Browser Boundary Harness Recipe

SPK-C is an isolated, disposable, **non-production** browser fixture. It does not create a trusted host, production entry point, package manifest, relay, wallet, upload, external-state connection, or secret. The only guest code runs in the `fixture.html` iframe with `sandbox="allow-scripts"`; observer diagnostics remain in the top-level local harness and are not part of the claimed guest response.

## Source and claim boundary

`SRC-POLICY-001` and `CLM-UPSTREAM-BASELINE-001` are immutable project-policy / archive records, not upstream browser or napplet proof. Each required primitive is therefore marked `blocked` in `metadata.yaml.sourceBindings`. The fixture measurements below are **observed browser behavior** only. Any host boundary recommendation is **proposed project policy** pending ADR-0005 review.

## Fixed local fixture contract

- **Current source-model fixture:** A local top-level page creates one sandboxed `srcdoc` iframe. Its first guest document script stores the declared domain value and injection phase before the second guest script handles messages.
- **Sandbox:** `allow-scripts` only. No `allow-same-origin`, forms, downloads, popups, top navigation, modals, pointer lock, storage access, or network operation is granted.
- **Pre-script injection:** The fixture injects the fixed string `lesson.example.invalid` into `window.__spkCDeclaredDomain` before the guest script starts. The removed-domain case injects no value; it intentionally does not call or make a claim about the deprecated `document.domain` API.
- **Allowed envelope:** Only plain objects with `kind`, `nonce`, `scenario`, and fixed request/result fields are accepted. The fixed nonce is `spk-c-local-nonce-v1`; browser-origin data is diagnostic only because a sandboxed `srcdoc` iframe has an opaque origin.
- **Source mapping:** The top-level harness checks that the request event's `source` is exactly `iframe.contentWindow` before emitting a response.
- **Deterministic service:** A valid `boundary-request` receives `{ kind: "boundary-response", ok: true, result: "local-service-ok" }`. The removed-domain scenario receives `{ kind: "boundary-response", ok: false, error: "declared-domain-missing" }`.
- **Capture:** `window.__spkCTranscript` retains bounded envelopes and booleans only; it has no network or persistent storage sink.

## Replay

1. Verify that the only runner is `tools/phase1-python` and its approved `playwright==1.61.0` dependency.
2. Use only the separately pinned installed browser executables in `metadata.yaml`: Google Chrome 150.0.7871.124 and Firefox 152.0.4. Never run `playwright install`, use managed browser binaries, or download a browser.
3. For each browser, launch five fresh contexts, open the local `file://` fixture, call `runBoundaryHarness()`, and retain the two scenario result envelopes, `MessageEvent.source` mapping, injection acknowledgement, and execution time.
4. A sample passes only when the declared-domain scenario acknowledges `pre-guest-script`, maps the source, and returns `local-service-ok`, while the removed-domain scenario maps the source and returns `declared-domain-missing`.
5. Record every raw elapsed value plus range and median. Any fixture/browser discrepancy is an observed result, not a protocol fact.
6. Run `validate-spike --complete`, `validate-report`, `validate-impact-fragment`, and `validate-planning`. Do not call the result a production host or a selected protocol profile.

## Failure and blocked handling

A timeout, missing source mapping, unexpected envelope, unexpected response, browser launch failure, or absent approved runner is a failed or blocked measurement according to `metadata.yaml`. Preserve the bounded local evidence, include the affected EVID-04 / ADR-0005 impact, and do not substitute another browser, package, execution context, or external service.
