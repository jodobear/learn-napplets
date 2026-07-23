# Quality, Security, Accessibility, and Testing

## 1. Accuracy gates

Fail a phase/release when:

- a protocol-sensitive claim lacks a current source;
- evidence class and maturity are conflated;
- a current-status page lacks a verification date;
- a wire example fails current validation;
- a package example fails to compile against its recorded version;
- a fixture/source compatibility record is missing;
- a runtime example is presented as mandated architecture;
- an open question is stated as settled;
- a stale alias appears without mapping;
- a lab teaches behavior no current source defines.

## 2. Test matrix

| Layer | Tests |
|---|---|
| Content | schema, source IDs, evidence/maturity, glossary links, stale terminology |
| Code examples | TypeScript compile, current public imports, build |
| Knowledge | JSON schema/version, Markdown generation, stable IDs, parity |
| Diagrams | node/edge integrity, transcript/table parity, keyboard state |
| Labs | deterministic transitions, reset, failures, static fallback |
| Teaching host | profile declaration, iframe lifecycle, injection, messages, source mapping |
| Verified loader | signature/blob/aggregate/artifact fixtures where implemented |
| Napplet artifacts | current build shape, feature gating, applicable conformance |
| Routes | prerender, base path, 404, no-JavaScript |
| Accessibility | automated checks plus manual keyboard/screen-reader review |
| Browser | Chromium, Firefox, WebKit |
| Visual | selected deterministic screenshots |
| Performance | route/lab bundles, startup, optional course artifact |
| Deployment | artifact assembly and production smoke tests |
| Freshness | upstream SHA/digest change and impact mapping |

## 3. Accessibility

- semantic headings and landmarks;
- full keyboard operation;
- visible focus;
- no hover-only information;
- no color-only meaning;
- accessible SVG titles/descriptions;
- transcript and table fallback;
- reduced-motion support;
- play/pause/step/reset;
- zoom-safe layout;
- responsive code;
- no-JavaScript reading;
- print-friendly lessons.

## 4. Motion

Complex motion does not auto-loop.

Every stateful animation has named deterministic steps that tests can render directly.

## 5. Teaching-host security

The teaching host must:

- declare its profile and source baseline;
- use the current verified sandbox/loading behavior for the profile;
- validate inbound messages;
- bind messages through the current sender mechanism;
- keep fixtures fake;
- avoid real secrets and automatic external publication;
- isolate editable learner code;
- sanitize deep links and fixture selection;
- avoid `eval` unless a separately reviewed sandbox design requires it;
- expose observer diagnostics out-of-band rather than as invented wire responses.

## 6. Browser egress and CSP

Test actual browser behavior under the selected current loading model.

The public site’s CSP is a **project security policy**, not automatically a NIP requirement. Document:

- what the current NIP states;
- what each supported browser permits;
- what the teaching site blocks;
- which behavior remains an upstream question.

Do not claim that iframe sandboxing alone blocks channels that browser tests show remain available.

## 7. Editable-code safety

Preferred order:

1. fixed tested variants;
2. controlled small edits;
3. isolated bundling worker;
4. full editor only when justified.

Never execute arbitrary learner code in the top-level site context.

## 8. Deterministic data

Use fixed fake:

- keys;
- events;
- timestamps;
- relay names;
- response timing;
- publication outcomes;
- manifests;
- failures.

Compute actual hashes/signature verification where the lesson claims to demonstrate those mechanisms, but never use production credentials.

## 9. Live mode

Any live mode is:

- opt-in;
- separately labeled;
- unnecessary for lesson completion;
- reviewed for keys, signing, relays, uploads, privacy, and abuse;
- disabled in tests;
- outside initial v1 unless explicitly approved.

## 10. Privacy

Default:

- no account;
- local/session progress only;
- no behavioral analytics;
- no remote execution of learner code;
- no upload of learner content.

Future analytics require an explicit data and retention policy.

## 11. Performance

- static content before hydration;
- lazy-load labs;
- no global heavy motion library;
- SVG before canvas;
- no WebGL without measured need;
- no heavyweight editor in the default bundle;
- separate host/workbench chunks;
- separate budgets for public site and portable napplet.

Set numeric budgets after Phase 0 measurements.

## 12. Browser matrix

At minimum:

- current Chromium desktop/mobile;
- current Firefox desktop;
- current WebKit/Safari-equivalent;
- touch;
- narrow viewport;
- high zoom;
- reduced motion.

Run real browser integration tests for iframe, module, source-window, and egress behavior.

## 13. Supply chain and licensing

Before release:

- verify licenses for adapted code/content;
- record upstream provenance;
- avoid copied specification text;
- generate a dependency/license report;
- pin or lock build dependencies;
- review public example-napplet publication identity and signing process.

## 14. Learning validation

Prepare task-based walkthrough scripts for each primary audience. Measure whether a participant can explain ownership, trace a request, select a domain, and route a contribution without prompting.

Do not fabricate user-testing results. When participants are unavailable, ship the scripts and record the validation as pending. LLM evaluation is not a substitute for human comprehension testing.

## 15. Release checklist

- source registry current;
- compatibility and drift reviewed;
- examples compile;
- lab napplets build;
- applicable conformance passes;
- teaching-host profile passes its tests;
- human/machine parity passes;
- accessibility review complete;
- browser/security/egress review complete;
- performance budgets pass;
- deployment/publication smoke tests pass;
- maintenance workflow enabled.
