---
schema_version: 1
open_count: 4
waived_count: 0
fixed_count: 1
total_count: 5
last_updated: 2026-07-24T01:58:26.678Z
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
  }
]
````
