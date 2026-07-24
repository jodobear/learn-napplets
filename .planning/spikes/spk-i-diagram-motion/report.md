# SPK-I — Accessible deterministic diagram/motion report

SPK ID: SPK-I-DIAGRAM-MOTION

Metadata path: metadata.yaml

## Research question

Can a bounded data-driven semantic SVG carry the complete synthetic teaching meaning of a three-step trusted-host boundary flow with keyboard operation, visible focus, static transcript/table equivalents, deterministic reset/replay and screenshots, reduced-motion parity, and hostile-input containment—without a visual dependency or dynamic learner-code surface?

## Sources and immutable revisions

- **Project-policy source:** `SRC-POLICY-002`, `.planning/governance/evidence-policy.md`, commit `b534103068be8c07e6869bfb7290fb60fdd87c8c`, locator `Required fields and verification rule`, SHA-256 `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`, retrieved `2026-07-24T00:00:00Z`, authority/evidence class `project-policy`, maturity `accepted`. It governs local evidence handling; it is not upstream protocol authority.
- **Local synthetic fixture:** `fixture.svg`, SHA-256 `abe83d1fc388235625862f0281ea838665b7be747052a15a2029047e3159e8f3`, 8,625 bytes. It contains synthetic labels plus `SRC-POLICY-002` / `CLM-POLICY-001` status identifiers only.
- **Measurement runner:** `runner.py`, SHA-256 `be8b88ad99054ae84039aea8457ee92052d33473bfaaa80322dcc0bce2fb27f2`, run with approved `tools/phase1-python` and Playwright `1.61.0` against direct-installed Chrome `150.0.7871.124` and Firefox `152.0.4`. No package was installed, substituted, or downloaded.
- **Reproducibility evidence:** `environment.json` SHA-256 `fdbb3e8d986dbc35b83093f7d31524388c9f5ddd8a8f3a70411eddec664898b3`; `measurements.yaml` SHA-256 `a7955dda9f692d794dd4f07040f6aa3a3f28c10777bb19b699cb675bfd108f61`; `/tmp/spk-i-diagram-motion/browser-results.json` SHA-256 `8c01d8f814d2a8f2e6ad77292b7dd43dd54fced02818cea716bb608325ed7db5`; `/tmp/spk-i-diagram-motion/manifest.json` SHA-256 `cfa271c9b61c304160d0ee7afcb0658e7864b127dac4c54640d044be30b0e1b7`.

## Observations

**Chromium:** all five clean Google Chrome contexts passed all 27 declared local checks. Native Tab reached each of the three SVG links and Enter selected `step-compose`, `step-host`, and `step-result`. Each focus state had a stable visible-focus screenshot digest. The visual flow, transcript region, and ARIA table all contained `Compose`, `Host sentinel`, and `Static result`.

The initial reduced-motion screenshot, no-preference screenshot, and reset/replay screenshot were byte-identical in all five Chrome samples: `a5e00e4e82453a94263c8f1be4a68771fd4d3fa0d23bd01562badab25f87b0cb`. Fixture-load values were `9.108`, `16.832`, `8.382`, `11.235`, and `12.139` milliseconds (range `8.382`–`16.832`; median `11.235`). The fixture used zero JavaScript bytes.

The runner found zero script elements, inline event attributes, and unsafe hrefs in static XML and Chrome DOM. The hostile input remained escaped literal text, and the static trusted-host sentinel remained `trusted-host-only-static` in every Chrome sample.

**Firefox:** direct-installed Firefox `152.0.4` launched through approved Playwright `1.61.0` but exited with code `0` before a clean automation context attached. No fixture, screenshot, keyboard, reduced-motion, transcript/table, or sentinel result was observed. This reproduces the existing Firefox launch blocker. No browser download, added launch argument, profile, preference, or launcher/configuration workaround was attempted.

Candidate A (semantic static SVG) passed all measured Chromium checks but has a blocked cross-browser result. Candidate B (minimal executable state/motion controller) was intentionally not introduced because SPK-I must not create a dynamic learner-code or script-injection surface. Candidate C (visual-library dependency) remains blocked: no approved measured need exists and no visual dependency was installed.

## Conflicts

Chrome supports the bounded local SVG contract, while Firefox supplied no contrary fixture observation because automation could not attach. This is an incomplete browser matrix, not evidence that Firefox rejects the SVG or that Chrome behavior generalizes to a production teaching host. No upstream protocol source was evaluated or resolved.

## Inference

**Inference:** the Chrome result makes a data-driven semantic SVG with static transcript/table parity a credible lowest-complexity **proposed** baseline for a later accessible diagram primitive. Its zero JavaScript and 8,625-byte fixture cost are enough local evidence not to assume a state/motion library is necessary.

This does not select a production visual system, prove screen-reader speech, establish upstream behavior, or resolve Firefox. Essential meaning must remain available in static, keyboard, transcript, table, reduced-motion, and reset/replay representations before later work can add optional motion.

## Prototype or measurement

The prototype is limited to the disposable `SPK-I` fixture and runner under `.planning/spikes/spk-i-diagram-motion/`. It uses named static SVG anchor targets, five isolated Chrome contexts, `reduce` and `no-preference` motion contexts, fixed viewport screenshots, and immutable fixture URI reset/replay. Generated screenshots and raw results remain only in `/tmp/spk-i-diagram-motion`.

No application route, framework scaffold, production component, visual dependency, network target, secret, executable learner input, or script injection was created. Semantic DOM exposure was tested; actual assistive-technology speech was not simulated or claimed.

## Recommendation

**Project recommendation, not an accepted ADR:** retain Candidate A as a non-production, partially measured proposed ADR-0006 input. A later implementation may use a static-first data-driven semantic SVG only if it preserves the tested equivalents and obtains required approval. Do not add a heavy visual dependency or motion/state controller without a new approved measurement that demonstrates need and passes the same boundary checks.

ADR-0006 remains **blocked for a cross-browser positive recommendation** until the approved direct-installed Firefox/Playwright launcher mismatch is resolved through a separately reviewed environment change. The safe Phase 04 fallback is a static diagram, transcript, and table with no essential motion.

## Uncertainty

Uncertainty is material. This synthetic local fixture does not establish protocol facts, production accessibility, runtime isolation, or actual assistive-technology behavior. Firefox supplied no fixture result. Chrome's five deterministic screenshots apply only to this fixed Linux/browser configuration and are not a production bundle budget or general performance claim.

## Affected phases and requirements

- **EVID-04 / Phase 01:** measurable non-production diagram/motion evidence with incomplete browser scope recorded honestly.
- **ADR-0006:** proposed, blocked-for-cross-browser input; Candidate A is locally promising in Chrome, no visual dependency is selected, and Firefox remains unresolved.
- **Phase 04 / A11Y-01 support:** preserve static SVG, keyboard, transcript, table, reduced-motion, and reset/replay equivalents; animation cannot carry essential authority or protocol meaning.
- **Phase 05 teaching-host work:** may use the hostile-input/sentinel test shape as a local fixture-boundary pattern but must not treat it as runtime-boundary proof.

## Owner and required approval

Owner: research owner. Required approval: separate dated human accessibility, security, content-learning, protocol-technical, and product review as applicable before accepting ADR-0006 or authorizing a production visual system. This report records local observations and a proposal only; it does not verify an upstream claim, accept an ADR, or authorize production scaffolding.
