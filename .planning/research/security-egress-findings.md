# Security and egress synthesis

## Research question

What does the validated SPK-H local fixture support without converting local browser behavior or project policy into an upstream protocol conclusion?

## Sources and immutable revisions

- Fragment: `SPK-H-IMPACT-001` SHA-256 `40d7f7bfacffd2630bc9884ba717da0d263ef5b092de5abee69fb86d094b8042`.
- Report: `spikes/spk-h-browser-egress/report.md` SHA-256 `715589b73dea61bb8e620c9ef5a54a066c2bbe8b4d4317450188e7a185c0cfb6`.
- Metadata: `spikes/spk-h-browser-egress/metadata.yaml` SHA-256 `1f6e42f81ce9f1ae765d9166eb9b09676f67c366e410feb744626127ba84fbfb`.
- Measurement: `spikes/spk-h-browser-egress/measurements.yaml` SHA-256 `5d91d92ea90c98e62d51119da6c5be3aae483501b4d9b6aa604bcb79298680d8`.
- Canonical source and claim provenance: SRC-POLICY-001, SRC-POLICY-002; `CLM-UPSTREAM-BASELINE-001` and `CLM-POLICY-001`.

## Upstream-fact status

No current immutable upstream egress statement was collected. `SRC-POLICY-001` and `CLM-UPSTREAM-BASELINE-001` record that absence as blocked project evidence; they are not upstream browser or protocol proof.

## Browser observations

The exact opaque-origin `srcdoc` guest with `sandbox=allow-scripts` only produced five bounded Chromium local-loopback observations. Firefox exited before Playwright attached, so no Firefox channel or CSP behavior was observed. These are fixture observations only.

## Proposed project policy

`SEF-BROWSER-EGRESS-001` is a proposed project policy: use a restrictive, reviewable public-site CSP only after the named security and protocol review. It is not an upstream NIP requirement or cross-browser conclusion.

## Unresolved questions

OQ-EGRESS-NIP-001; OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001 remain blocked pending immutable upstream evidence and, for Firefox, attached-context measurements under the approved toolchain.

## Conflicts

`DRF-EGRESS-001` and the Firefox launcher blocker retain the distinct local observation and unresolved upstream question. No conflict is silently resolved by this synthesis.

## Inference

The supported inference is limited to the named local fixture, browser version, sandbox tokens, CSP inputs, and loopback endpoints. It does not select a production host profile.

## Uncertainty

The only source bindings are project policy/archive inputs; Chrome measures one disposable local fixture, Firefox has no attached-context result, and neither result establishes upstream protocol behavior or a production CSP.

## Owner and required approval

Owner: `research-owner`. Required approval: Dated security and protocol-technical review before ADR-0014 or any production CSP decision. Revisit trigger: Collect a current immutable upstream egress statement and obtain Firefox attached-context measurements under the approved toolchain.
