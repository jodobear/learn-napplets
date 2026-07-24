# SPK-J — Least-authority code-editing report

SPK ID: SPK-J-CODE-EDITING

Metadata path: metadata.yaml

## Research question

Which least-authority editing approach lets a learner complete the bounded synthetic task—change `const greeting = "Hello";` to the one declared alternate—while preserving keyboard use, semantic status, static fallback, deterministic reset/replay, and trusted-context isolation without executing arbitrary learner code?

## Sources and immutable revisions

- **Project-policy source:** `SRC-POLICY-002`, `.planning/governance/evidence-policy.md`, commit `b534103068be8c07e6869bfb7290fb60fdd87c8c`, locator `Required fields and verification rule`, SHA-256 `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`, retrieved `2026-07-24T00:00:00Z`, authority/evidence class `project-policy`, maturity `accepted`. It governs evidence handling and package review; it is not upstream protocol authority.
- **Local synthetic fixture:** `fixture.html`, SHA-256 `f0a2e97578be8abc9c685ee753c20ab4155e8b7f08aa18b52b38687d45d0a3dd`, 7,955 bytes. It contains only two declared text variants, native controls, exact string comparison, and a test sentinel.
- **Measurement runner:** `runner.py`, SHA-256 `30e5c053a96d7527962c4a69f7af7a6c73ad3d09c32157f04278d568b992c83e`, run through approved `tools/phase1-python` with Playwright `1.61.0` against direct-installed Chrome `150.0.7871.124` and Firefox `152.0.4`.
- **Approved direct CodeMirror releases:** `@codemirror/state@6.5.2`, `@codemirror/view@6.38.6`, `@codemirror/commands@6.8.1`, and `@codemirror/lang-javascript@6.2.3`. Exact registry integrity, MIT license evidence, immutable release commits, and public root exports are recorded in `metadata.yaml`. Human approval dated `2026-07-24` explicitly accepted incomplete transitive dependency-lock review for this isolated non-production experiment only.
- **Blocked lightweight release:** `codejar@4.3.0` was not installed because its registry release points to a git revision whose immutable `package.json` reports version `4.2.0`.
- **Reproducibility evidence:** `environment.json` SHA-256 `b1f5908976032e02398e90f524e4f80f3c21f22138d564aa952ff1c0f78d7d00`; `measurements.yaml` SHA-256 `2407701d1128ad1ac076a9c050f4f7b6bb3e0d0b0658ccc4a52de7114d3b6b1b`; `/tmp/spk-j-code-editing/browser-results.json` SHA-256 `e15afaed4626cb924fc44a558eafbba7de4583ea413ab0ee41ee97e45e0ce87e`; `/tmp/spk-j-code-editing/manifest.json` SHA-256 `beed1b3e7fb26c7f91f15f6ad3254ec2d94e9a02a611fa9dd9e83443368c3189`.

## Observations

**Chromium:** all five clean Google Chrome contexts passed all 24 declared checks. Fixed variants were keyboard reachable, had visible focus, and updated an announced status. The controlled textarea accepted only the exact alternate string; the fixed hostile literal remained unrecognized text, created no extra script element, and left the trusted-host sentinel unchanged. Reset restored the starter text deterministically. The native lightweight shell exposed its label and status and added no dependency or evaluator.

Native fixture load values were `30.920`, `22.921`, `22.290`, `37.275`, and `26.530` milliseconds (range `22.290`–`37.275`; median `26.530`). Its reset screenshot had one digest across all five samples. Native package cost was zero bytes beyond the 7,955-byte fixture.

The approved CodeMirror direct set resolved to 15 local packages totaling 5,174,566 bytes; the four direct published packages totaled 1,925,436 unpacked bytes. The loopback harness received only the fixed starter document. It exposed a contenteditable surface, keyboard focus, harness-visible focus, announced status, static no-JavaScript fallback, and unchanged sentinel. Load values were `74.381`, `79.477`, `78.325`, `56.455`, and `56.311` milliseconds (range `56.311`–`79.477`; median `74.381`). Its initial screenshot had one digest across all five samples. All 16 resource requests were local loopback fixture/module requests.

Actual assistive-technology speech was not observed. The experiment checked semantic labels, `aria-live` status, DOM exposure, keyboard focus, static fallback, and visible focus only.

**Firefox:** direct-installed Firefox `152.0.4` exited with code `0` before Playwright `1.61.0` attached. No fixture, editor, keyboard, fallback, screenshot, hostile-input, or sentinel behavior was observed. No browser download, launcher argument, profile, preference, or configuration workaround was attempted.

## Conflicts

Chrome supplied complete local evidence for the bounded synthetic fixture and fixed-document CodeMirror harness, while Firefox supplied no contrary fixture result because automation could not attach. This is an incomplete browser matrix, not evidence that Firefox rejects any candidate or that Chrome behavior generalizes to production.

CodeMirror passed the bounded Chrome checks, but its resolved local tree is materially larger than the dependency-free candidates and the learning task did not require arbitrary editing or execution. The approval exception also left the transitive dependency lock incompletely reviewed. CodeJar remained blocked because its registry and immutable source version identities conflict.

## Inference

**Inference:** fixed tested variants are sufficient and lowest-authority for the declared learning objective. A controlled native textarea is justified only when the learner must make the one bounded textual change. The native inspection shell remains a possible dependency-free extension for line/character feedback.

The CodeMirror observation demonstrates only that the exact approved direct set can render a fixed synthetic document in this Chrome environment. It does not justify making a full editor the default, authorizing arbitrary learner-code execution, accepting its incomplete dependency closure for production, or establishing upstream/runtime behavior.

## Prototype or measurement

After the dated package gate, the exact CodeMirror direct set was installed only below ignored `.planning/spikes/spk-j-code-editing/.experiment/codemirror-6-core/` with `--ignore-scripts --package-lock=false`. The runner served only the SPK-J fixture, temporary harness, and local package modules over `127.0.0.1`; generated screenshots and raw results remained under `/tmp/spk-j-code-editing`.

The fixture never calls `eval`, `Function`, dynamic script creation, `innerHTML`, networking, storage, `postMessage`, `srcdoc`, or workers. Learner-editable text is compared to fixed constants and displayed through `textContent`. The CodeMirror harness receives only a fixed runner-owned starter string; no learner text is passed to the package editor or executed.

No application route, production component, framework scaffold, root package manifest, secret, upload, telemetry event, external request, or persistent learner record was created.

## Recommendation

**Project recommendation, not an accepted ADR:** use fixed tested variants as the default for this bounded objective. Use a controlled native textarea only for the declared small edit, preserving exact classification, visible/announced status, reset, static fallback, and no execution. Do not select CodeMirror as the default: measured need is absent, the local tree is substantially larger, Firefox evidence is unavailable, and the transitive dependency-lock review exception was scoped only to this disposable experiment. Keep CodeJar blocked.

ADR-0009 remains **blocked for a cross-browser positive recommendation**. Any future requirement for arbitrary learner-code execution needs a separate trusted-host/sandbox design and security review; SPK-J does not authorize that capability.

## Uncertainty

Uncertainty is material. Results apply only to synthetic text, one Linux environment, one Chrome build, the recorded direct package versions, and fixed local checks. Firefox supplied no fixture result. Actual screen-reader speech, learner comprehension, production bundle behavior, production isolation, package maintenance suitability, and upstream protocol behavior were not established.

Refresh this evidence when the approved Firefox execution route changes, when editor versions or exports change, when complete transitive dependency review is required, or when a real learning objective demands capability beyond fixed variants or controlled text.

## Affected phases and requirements

- **EVID-04 / Phase 01:** records bounded editing, accessibility, isolation, package, cost, and browser evidence with an explicit Firefox blocker.
- **ADR-0009:** proposed least-authority input only; fixed variants are locally preferred, controlled textarea is narrowly justified, CodeMirror is not selected, and CodeJar remains blocked.
- **Phase 05:** must preserve trusted-host ownership, static fallback, keyboard/status/reset behavior, and prohibition on arbitrary top-level learner-code execution.
- **Later production/package work:** requires fresh package approval, complete dependency review, cross-browser evidence, and separate security/accessibility approval.

## Owner and required approval

Owner: research owner. Required approval: separate dated security, accessibility, content-learning, protocol-technical, and product review as applicable before accepting ADR-0009 or authorizing a production editor or learner-code execution path. This report records local observations and a proposal only; it does not accept an ADR, verify upstream protocol behavior, or authorize production scaffolding.
