---
schema_version: 1
open_count: 0
waived_count: 0
fixed_count: 1
total_count: 1
last_updated: 2026-07-23T21:36:41.912Z
---

# Broken Windows Ledger

> Cross-phase defect register. `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | deviation | requirements-phase1-tools.txt |  | Removed inline pip hashes because they forced unapproved resolver pins; artifact hashes remain in approval and environment records. | fixed |  | 2026-07-23T21:36:10.803Z | 2026-07-23T21:36:41.912Z |

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
  }
]
````
