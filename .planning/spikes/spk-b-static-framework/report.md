# SPK-B — Static-First Framework Comparison Report

SPK ID: SPK-B-STATIC-FRAMEWORK

Metadata path: metadata.yaml

## Research question

Can the two exact, human-approved static-first package releases in `metadata.yaml` build the same disposable local fixture five times while preserving static output, separate public/lab entries, accessibility support paths, and no production framework scaffold?

## Sources and immutable revisions

- **Project policy / contract:** current committed `metadata.yaml`, `recipe.md` (`SHA-256 a6f6a912406c259dcbe4db43e73cb4d929a8f5b43002f82fd5cb5404cd283a60`), and `fixture.md` (`SHA-256 24ee064159a14de4f0c9e6c8d3f9684fad1ace76920cb899d8fc614a5a24e503`), retrieved/approved 2026-07-24. These are project-policy inputs, not upstream framework facts.
- **Approved release evidence:** `astro@7.1.3` from `https://registry.npmjs.org/astro/7.1.3`, integrity `sha512-4dhPyAAXthf3xLEYnG8SeL7yr/nTPPABfY7e9YF0yuO+vK9Xp+8Q5j4xzsmL3GueukQv4oNwGNTBepLOiDGeJA==`, shasum `f80d8459c10fff08b2c457e9171547f32761582c`, installed package-manifest SHA-256 `bf3ff78baf8ec066d56d5ca414fa38ff2fecefa21c2aa69b5891bc03740aa41a`.
- **Approved release evidence:** `vitepress@1.6.4` from `https://registry.npmjs.org/vitepress/1.6.4`, integrity `sha512-+2ym1/+0VVrbhNyRoFFesVvBvHAVMZMK0rw60E3X/5349M1GuVdKeazuksqopEdvkKwKGs21Q729jX81/bkBJg==`, shasum `1b6c68fede541a3f401a66263dce0c985e2d8d92`, installed package-manifest SHA-256 `da038b347065c4543eb794a52f552140451974804800d99e20f6d6e624200ac4`.
- **Environment:** `environment.json` records Node `v22.22.0`, npm `10.9.4`, the digest-pinned `tools/phase1-python`, and installed browser versions. No browser was downloaded or used.

## Observations

Observed implementation behavior, fully itemized in `measurements.yaml`:

| Candidate | Exact release | Five replay result | Stable static-output SHA-256 | Mean elapsed |
| --- | --- | --- | --- | ---: |
| Astro | `astro@7.1.3` | 5/5 passed | `ec7e951d45a25fdcf0648263164a81e6709ade51ae8d9e3723bf3130b69eec94` | 600.801 ms |
| VitePress | `vitepress@1.6.4` | 0/5 passed | `2948ebf6c8c59be0f82b95e945d7110c492d375d646cddb1cbde9cea49a69c26` | 1472.095 ms |

Astro passed all declared static HTML, structured content, bounded local lab, separate entry, deterministic assertion, boundary, accessibility-support-path, and static-deployment checks. VitePress emitted stable static public/lab pages, but every replay reported `accessibility assertion missing prefers-reduced-motion`.

The only installs were the two approved `npm --prefix ... install --ignore-scripts --package-lock=false` commands in `metadata.yaml`. The fixture and generated outputs stayed below `.planning/spikes/spk-b-static-framework/.experiment/`; that disposable tree was removed after evidence capture. No root `package.json`, lockfile, `src`, `apps`, or `packages` production marker was created.

## Conflicts

No upstream source fact conflicts with planning. A local measurement conflict remains: the VitePress fixture emitted stable static pages and intended content/lab structure, while its declared deterministic accessibility assertion did not find the reduced-motion marker in emitted HTML. This report retains that failure rather than inferring equivalence from source input.

## Inference

Only this narrow inference is supported: under the recorded environment, the exact Astro release satisfied the disposable fixture. The result does not select an architecture, prove browser interaction, establish a runtime authority model, or prove upstream protocol behavior. VitePress does not meet this fixture's complete measured-evidence threshold.

## Prototype or measurement

Replay after the same two approved installs:

```text
node .planning/spikes/spk-b-static-framework/.experiment/run-comparison.mjs
```

The command materializes the text-only fixture under the approved candidate paths, builds each candidate five times, records source/command/output digests and durations, then removes the disposable tree. No live probe, external runtime service, lifecycle script, or browser download was used.

## Recommendation

**Proposed, not accepted:** provide Astro `7.1.3` as reproducible, package-approved SPK-B input for ADR-0002 review. Do not initialize Astro or select it as project architecture in Phase 1.

**Blocked for this fixture:** do not use VitePress `1.6.4` as positive ADR-0002 evidence until a separately reviewed measurement resolves the repeated reduced-motion/static-equivalent assertion failure. Do not substitute an unapproved package.

## Uncertainty

This comparison covers a minimal static fixture, not the future app, trusted host, untrusted napplet containment, production deployment, keyboard browser automation, or current upstream protocol behavior. Command-output digests vary with logs; each candidate's static output digest was stable through five replays. ADR-0002 remains proposed and needs human acceptance.

## Affected phases and requirements

- **Phase 1 / `EVID-04`:** reproducible SPK-B evidence includes an explicit VitePress blocker.
- **ADR-0002:** receives proposed framework evidence only; no accepted architecture is created.
- **Phase 2 and later:** remain gated by Phase 1 review and the Phase 2 product/content contract.

## Owner and required approval

Owner: project operator and ADR-0002 reviewers. Required approval: human ADR-0002 review must accept, reject, or request additional evidence. This report cannot accept the ADR or authorize a production framework.
