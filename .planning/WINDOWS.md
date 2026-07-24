---
schema_version: 1
open_count: 10
waived_count: 0
fixed_count: 1
total_count: 11
last_updated: 2026-07-24T10:36:13.437Z
---

# Broken Windows Ledger

> Cross-phase defect register. `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | deviation | requirements-phase1-tools.txt |  | Removed inline pip hashes because they forced unapproved resolver pins; artifact hashes remain in approval and environment records. | fixed |  | 2026-07-23T21:36:10.803Z | 2026-07-23T21:36:41.912Z |
| 2 | 01 | unrun-verify | tools/phase1-python |  | Python unittest discovery found no test modules and exited 5 after SPK-B validation. | open |  | 2026-07-24T01:07:30.289Z |  |
| 3 | 01 | unrun-verify | .planning/spikes/spk-c-boundary-harness/runner.py |  | Firefox 152.0.4 could not launch under approved Playwright 1.61.0; SPK-C cross-browser replay remains blocked | open |  | 2026-07-24T01:36:37.590Z |  |
| 4 | 01 | deviation | .planning/spikes/spk-d-verified-loader/measurements.yaml |  | Recorded five actual fixture-integrity replays before retaining five raw measurement values. | open |  | 2026-07-24T01:58:26.617Z |  |
| 5 | 01 | deviation | .planning/spikes/spk-d-verified-loader/metadata.yaml |  | Added the validator-required --root .planning argument to the SPK-D impact-fragment command. | open |  | 2026-07-24T01:58:26.678Z |  |
| 6 | 01 | stub | .planning/spikes/spk-k-deployment/fixture.md | 33 | Intentional lab-artifact placeholder prevents a teaching-host deployment claim pending evidence and ADR approval. | open |  | 2026-07-24T10:04:33.212Z |  |
| 7 | 01 | stub | .planning/spikes/spk-k-deployment/fixture.md | 36 | Intentional portable-output placeholder prevents a portability claim while ADR-0007 remains unresolved. | open |  | 2026-07-24T10:04:33.290Z |  |
| 8 | 01 | deviation | .planning/spikes/spk-h-browser-egress/fixture.html |  | Parent CSP inheritance initially blocked the declared local script measurement. | open |  | 2026-07-24T10:36:13.234Z |  |
| 9 | 01 | deviation | .planning/spikes/spk-h-browser-egress/fixture.html |  | Opaque-origin worker probe was bounded to a blob worker and documented as non-loader evidence. | open |  | 2026-07-24T10:36:13.304Z |  |
| 10 | 01 | deviation | .planning/spikes/spk-h-browser-egress/runner.py |  | Referrer-mode receipt grouping initially produced a false failed matrix result. | open |  | 2026-07-24T10:36:13.369Z |  |
| 11 | 01 | deviation | .planning/research/schemas/spike-impact-fragment.schema.json |  | SPK-H needed a typed security-egress finding proposal schema field for required approval metadata. | open |  | 2026-07-24T10:36:13.437Z |  |

````json
[
  {
    "id": 1,
    "kind": "deviation",
    "phase": "01",
    "file": "requirements-phase1-tools.txt",
    "line": null,
    "description": "Removed inline pip hashes because they forced unapproved resolver pins; artifact hashes remain in approval and environment records.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-07-23T21:36:10.803Z",
    "resolved_at": "2026-07-23T21:36:41.912Z"
  },
  {
    "id": 2,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "tools/phase1-python",
    "line": null,
    "description": "Python unittest discovery found no test modules and exited 5 after SPK-B validation.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T01:07:30.289Z",
    "resolved_at": null
  },
  {
    "id": 3,
    "kind": "unrun-verify",
    "phase": "01",
    "file": ".planning/spikes/spk-c-boundary-harness/runner.py",
    "line": null,
    "description": "Firefox 152.0.4 could not launch under approved Playwright 1.61.0; SPK-C cross-browser replay remains blocked",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T01:36:37.590Z",
    "resolved_at": null
  },
  {
    "id": 4,
    "kind": "deviation",
    "phase": "01",
    "file": ".planning/spikes/spk-d-verified-loader/measurements.yaml",
    "line": null,
    "description": "Recorded five actual fixture-integrity replays before retaining five raw measurement values.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T01:58:26.617Z",
    "resolved_at": null
  },
  {
    "id": 5,
    "kind": "deviation",
    "phase": "01",
    "file": ".planning/spikes/spk-d-verified-loader/metadata.yaml",
    "line": null,
    "description": "Added the validator-required --root .planning argument to the SPK-D impact-fragment command.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T01:58:26.678Z",
    "resolved_at": null
  },
  {
    "id": 6,
    "kind": "stub",
    "phase": "01",
    "file": ".planning/spikes/spk-k-deployment/fixture.md",
    "line": 33,
    "description": "Intentional lab-artifact placeholder prevents a teaching-host deployment claim pending evidence and ADR approval.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T10:04:33.212Z",
    "resolved_at": null
  },
  {
    "id": 7,
    "kind": "stub",
    "phase": "01",
    "file": ".planning/spikes/spk-k-deployment/fixture.md",
    "line": 36,
    "description": "Intentional portable-output placeholder prevents a portability claim while ADR-0007 remains unresolved.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T10:04:33.290Z",
    "resolved_at": null
  },
  {
    "id": 8,
    "kind": "deviation",
    "phase": "01",
    "file": ".planning/spikes/spk-h-browser-egress/fixture.html",
    "line": null,
    "description": "Parent CSP inheritance initially blocked the declared local script measurement.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T10:36:13.234Z",
    "resolved_at": null
  },
  {
    "id": 9,
    "kind": "deviation",
    "phase": "01",
    "file": ".planning/spikes/spk-h-browser-egress/fixture.html",
    "line": null,
    "description": "Opaque-origin worker probe was bounded to a blob worker and documented as non-loader evidence.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T10:36:13.304Z",
    "resolved_at": null
  },
  {
    "id": 10,
    "kind": "deviation",
    "phase": "01",
    "file": ".planning/spikes/spk-h-browser-egress/runner.py",
    "line": null,
    "description": "Referrer-mode receipt grouping initially produced a false failed matrix result.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T10:36:13.369Z",
    "resolved_at": null
  },
  {
    "id": 11,
    "kind": "deviation",
    "phase": "01",
    "file": ".planning/research/schemas/spike-impact-fragment.schema.json",
    "line": null,
    "description": "SPK-H needed a typed security-egress finding proposal schema field for required approval metadata.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-07-24T10:36:13.437Z",
    "resolved_at": null
  }
]
````
