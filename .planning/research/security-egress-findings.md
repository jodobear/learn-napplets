# Security and egress synthesis

## Research question

What does the validated SPK-H local fixture support without converting local browser behavior or project policy into an upstream protocol conclusion?

## Sources and immutable revisions

- Fragment: `SPK-H-IMPACT-001` SHA-256 `40d7f7bfacffd2630bc9884ba717da0d263ef5b092de5abee69fb86d094b8042`.
- Report: `spikes/spk-h-browser-egress/report.md` SHA-256 `715589b73dea61bb8e620c9ef5a54a066c2bbe8b4d4317450188e7a185c0cfb6`.
- Metadata: `spikes/spk-h-browser-egress/metadata.yaml` SHA-256 `1f6e42f81ce9f1ae765d9166eb9b09676f67c366e410feb744626127ba84fbfb`.
- Measurement: `spikes/spk-h-browser-egress/measurements.yaml` SHA-256 `5d91d92ea90c98e62d51119da6c5be3aae483501b4d9b6aa604bcb79298680d8`.
- Canonical source and claim provenance: `SRC-POLICY-001`, `SRC-POLICY-002`, `CLM-UPSTREAM-BASELINE-001`, and `CLM-POLICY-001`.

## Observations

No current immutable upstream egress statement was collected. The source and claim records document that absence as blocked project evidence, not upstream browser or protocol proof.

**Browser observations:** the exact opaque-origin `srcdoc` guest with `sandbox=allow-scripts` only produced five bounded Chromium local-loopback observations. Firefox exited before Playwright attached, so no Firefox channel or CSP behavior was observed. These are fixture observations only.

## Conflicts

`DRF-EGRESS-001` and `DRF-FIREFOX-PLAYWRIGHT-LAUNCH-001` retain the distinct local observation, missing Firefox attachment, and unresolved upstream question. No conflict is silently resolved by this synthesis.

## Inference

The supported inference is limited to the named local fixture, browser version, sandbox tokens, CSP inputs, and loopback endpoints. It does not select a production host profile or establish upstream egress behavior.

## Prototype or measurement

SPK-H records five bounded Chromium measurements plus an explicit Firefox pre-attachment blocked result. The local replay validates the referenced digest-pinned report, metadata, and measurement only; it does not test an external endpoint or production CSP.

## Recommendation

**Proposed project policy:** `SEF-BROWSER-EGRESS-001` proposes a restrictive, reviewable public-site CSP only after named security and protocol review. It is not an upstream NIP requirement or cross-browser conclusion.

## Uncertainty

**Unresolved questions:** `OQ-EGRESS-NIP-001` and `OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001` remain blocked pending immutable upstream evidence and, for Firefox, attached-context measurements under the approved toolchain. The only source bindings are project policy/archive inputs; neither the Chrome fixture nor the unavailable Firefox result establishes a production CSP.

## Affected phases and requirements

- Requirements: `EVID-04`, `OPER-03`.
- Phases: 01 evidence baseline, 02 product/content contract, 03 static-site foundation, and 05 teaching-host work.
- Impact: do not authorize a host profile, external egress, or browser-support conclusion; preserve deterministic static fallback and the Firefox blocker.

## Owner and required approval

Owner: `research-owner`. Required approval: dated security and protocol-technical review before ADR-0014 or any production CSP decision. Revisit trigger: collect a current immutable upstream egress statement and obtain Firefox attached-context measurements under the approved toolchain.
