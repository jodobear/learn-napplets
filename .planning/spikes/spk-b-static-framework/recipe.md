# SPK-B — Static-First Framework Comparison Recipe

SPK-B is disposable, **non-production** research. It must not create `package.json`, `src`, `apps`, `packages`, or another production marker at repository root.

## Candidate gate

The only candidates are `astro@7.1.3` and `vitepress@1.6.4`, recorded in `metadata.yaml`. Before any install, the reviewer must record an approve or block decision for each exact package/version after inspecting the official registry/project provenance, MIT license, registry integrity, source decision, and isolated command. A blocked candidate is never substituted.

## Criteria

For each approved candidate, record prerendering, Markdown/structured-content handling, interactive-lab integration boundary, multiple entries, test support, bundle/authority isolation, accessibility support/evidence, static deployment output, elapsed fixture measurement, failure, and blocker. The measurement threshold is five identical local replays with no repository-root production marker; otherwise record the declared failure or blocker.

## Isolation and replay

All dependencies and generated output remain below `.planning/spikes/spk-b-static-framework/.experiment/`, an ignored disposable path. After approval, run only the candidate's exact command from `metadata.yaml`, perform the same local fixture comparison five times through `tools/phase1-python`, capture command/output digests and environment facts, then remove or retain only the committed text evidence. No package command, browser acquisition, live probe, or production framework initialization is permitted before approval.
