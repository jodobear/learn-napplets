# SPK-F — Guest-only Portable Workbench/Course Feasibility Report

SPK ID: SPK-F-COURSE-WORKBENCH

Metadata path: metadata.yaml

## Research question

Can exact human-approved static-content releases build the declared disposable two-lesson, guest-only Workbench/course simulation while retaining artifact, startup, memory, accessibility, navigation, capability-degradation, identity, and build-complexity evidence without claiming host authority or real napplet composition?

## Sources and immutable revisions

- **Project-policy source:** `SRC-POLICY-001`, immutable revision `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`, `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`, digest `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`, retrieved 2026-07-24. Authority/evidence/maturity: planning archive/project policy/accepted. It is not current upstream protocol proof.
- **Project-policy source:** `SRC-POLICY-002`, immutable revision `b534103068be8c07e6869bfb7290fb60fdd87c8c`, `.planning/governance/evidence-policy.md`, digest `9d3f9697cc7058b8edcb5b2a346ff9de677ca10b5b163d1ba1b7f40d7d01c4b2`, retrieved 2026-07-24. Authority/evidence/maturity: project policy/project policy/accepted.
- **Approved registry releases:** `astro@7.1.3` (`https://registry.npmjs.org/astro/7.1.3`, MIT, registry integrity `sha512-4dhPyAAXthf3xLEYnG8SeL7yr/nTPPABfY7e9YF0yuO+vK9Xp+8Q5j4xzsmL3GueukQv4oNwGNTBepLOiDGeJA==`, installed manifest SHA-256 `bf3ff78baf8ec066d56d5ca414fa38ff2fecefa21c2aa69b5891bc03740aa41a`) and `vitepress@1.6.4` (`https://registry.npmjs.org/vitepress/1.6.4`, MIT, registry integrity `sha512-+2ym1/+0VVrbhNyRoFFesVvBvHAVMZMK0rw60E3X/5349M1GuVdKeazuksqopEdvkKwKGs21Q729jX81/bkBJg==`, installed manifest SHA-256 `da038b347065c4543eb794a52f552140451974804800d99e20f6d6e624200ac4`) are package provenance, not proof of upstream napplet behavior.
- **Local fixture evidence:** `fixture.md` SHA-256 `f7f490d6dcc198b2358682e906979b9c366eed24174e846eb42531c750fcb690`; `environment.json` records the approved direct browser inventory and exact local toolchain.

## Observations

| Candidate | Five-build output digest | Artifact bytes | Build median | Build-memory median | Chromium | Firefox |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `astro@7.1.3` | `6b09b1f03f901de0e32a6ab36fe2fbf8b92e760489c2298afc248ed8bd0da86b` | 3,710 | 593.762 ms | 240,084 KiB | passed fixture interaction | blocked before Playwright attachment |
| `vitepress@1.6.4` | `ba7313c36bb704e99b349691bc72f9cad48c637cbc49877a315a97bc0eb2b42c` | 924,910 | 1,508.372 ms | 304,388 KiB | passed static fixture inspection | blocked before Playwright attachment |

Both candidates built the two representative lessons, architecture transcript, code example, assessment, source metadata, lesson navigation controls, reduced-motion marker, update identity marker, and no-private-frame output deterministically over five runs. Chromium exercised Astro's present-capability toggle and reset-to-absent behavior. VitePress rendered the declared present/absent static-equivalent transcript without claiming mediated capability. No source/lab was opened and no external state was written.

## Conflicts

`SPK-C` already records that Firefox 152.0.4 exits before approved Playwright 1.61.0 attaches. The same direct-browser observation occurred here; this is a preserved, impact-scoped runtime-compatibility blocker, not a new browser configuration attempt.

`SPK-B` independently recorded a VitePress reduced-motion/static-equivalent fixture assertion failure. The SPK-F VitePress output contains the local marker and rendered under Chromium, but that distinct result neither resolves nor supersedes the SPK-B failure.

## Inference

The measured local result supports only a narrow inference: both approved releases can deterministically produce this guest-only static simulation under the recorded Linux/Node environment, and Chromium can render the declared interaction/static-equivalent paths. It does not establish a current napplet artifact contract, host authority, optional mediated capability, Firefox compatibility, sibling composition, or a portable delivery commitment.

## Prototype or measurement

After the Task 2 package gate, only the exact approved commands in `metadata.yaml` installed releases below `.planning/spikes/spk-f-course-workbench/.experiment/` with `--ignore-scripts --package-lock=false`. Five offline measurement replays used:

```text
CI=1 NO_COLOR=1 node .planning/spikes/spk-f-course-workbench/.experiment/run-spk-f.mjs
```

Direct-installed Chrome and Firefox were then attempted through approved `tools/phase1-python` Playwright. Chrome passed the bounded checks; Firefox exited before attachment. The disposable dependency tree, generated sources, outputs, raw logs, and browser observations are removed after this report captures their digests. No repository-root package manifest, host, app, production artifact, external request, secret, or ADR acceptance was created.

## Recommendation

**Blocked evidence result; no ADR outcome selected.** Do not choose `GO-V1`, `GO-LATER`, `WORKBENCH-ONLY`, or `NO-GO` from this measurement alone. Preserve the public-site-first sequence and retain the Phase 1 portable target as blocked for cross-browser runtime evidence. This report is proposed ADR-0007 input only.

## Uncertainty

Material. The prototype has one local guest-only simulation and static source metadata. It does not prove current upstream package exports, artifact/loading/storage/resource/link/composition rules, real external lab opening, Firefox behavior, browser conformance, host/guest authority, or production accessibility. Refresh when current immutable upstream runtime/package evidence or a reproducible Firefox launcher result becomes available.

## Affected phases and requirements

- **`EVID-04` / Phase 01:** records reproducible package-gated feasibility evidence and a cross-browser blocker.
- **`ADR-0007`:** receives a proposed blocked-evidence input; no decision is accepted.
- **Phase 02 and later portable work:** remain conditional on Phase 1 review, source acquisition, browser evidence, and the Phase 2 product/content contract.
- **Public-site work:** remains independent and must not wait for SPK-F.

## Owner and required approval

Owner: research owner. Required approval: separate dated product, protocol-technical, security, accessibility, and content-learning review as applicable. Only those reviewers may accept, reject, defer, or request more ADR-0007 evidence; this report cannot accept the ADR.
