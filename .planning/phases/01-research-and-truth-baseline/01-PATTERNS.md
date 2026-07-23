# Phase 1: Research and Truth Baseline - Pattern Map

**Mapped:** 2026-07-23  
**Files classified:** 50 path groups (including 13 lesson packets, 12 disposable spike directories, and ADR recommendation series)  
**Analogs found:** 35 / 50 path groups

## Scope and authority note

Phase 1 has no production application code, so there are no controller/component/service analogs to copy. Its implementation is a local, Python-driven planning/evidence toolchain plus canonical YAML/Markdown/JSON records. `docs/learn-napplets-codex-pack-v3/` supplies preserved **structure-only** analogs; it is immutable and must not be edited. Canonical policy and current state under `.planning/` override source-pack instructions that conflict with them. In particular, do **not** create `.planning/STATUS.md`; `.planning/STATE.md` is the sole live state source.

## File Classification

| New/Modified File(s) | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `.gitignore` | config | file-I/O | existing `.gitignore` | role-match |
| `requirements-phase1-tools.txt` (or approved isolated-environment manifest) | config | batch | none | none |
| `tools/validate-planning.py` (extend) and/or `tools/validate-research.py` | utility / validator CLI | batch, file-I/O, transform | `tools/validate-planning.py` | exact |
| `.planning/research/schemas/{source,claim,drift,compatibility,open-question,spike,phase-governance}.schema.json` and migration fixtures/notes | config / model | transform | `templates/{source-registry,claim,drift,compatibility-matrix,open-question}.example.yaml` | partial |
| `tests/phase1/test_{evidence,drift,compatibility,spikes,refresh,governance}.py` and deterministic fixtures | test | batch, file-I/O | none (no test suite exists) | none |
| `.planning/research/source-registry.yaml` | model / canonical record | CRUD, file-I/O | `templates/source-registry.example.yaml` | exact structure |
| `.planning/research/claims.yaml` | model / canonical record | CRUD, file-I/O | `templates/claim.example.yaml` | exact structure |
| `.planning/research/{compatibility-matrix,drift-register,open-questions}.yaml` | model / canonical record | CRUD, transform | corresponding `templates/*.example.yaml` | exact structure |
| `.planning/research/{terminology-map,teaching-scope,domain-catalog,archetype-convention-catalog,example-napplet-catalog,jobs-to-be-done}.yaml` | model / catalog record | CRUD, transform | `templates/lesson.example.yaml` and the record examples above | role-match |
| `.planning/research/{executive-summary,decision-summary,protocol-map,open-work-analysis,package-map,runtime-comparison,pedagogy-review,audiences,delivery-mode-recommendation,security-egress-findings,risks}.md` | report / documentation | transform | `templates/RESEARCH-REPORT-TEMPLATE.md` | role-match |
| `.planning/research/open-work-snapshot.json` | data snapshot | file-I/O, transform | `.planning/traceability/pack-v3-file-manifest.json` | role-match |
| `.planning/research/lesson-packets/{01...13}-*.md` | documentation / lesson research record | transform | `templates/LESSON-RESEARCH-PACKET-TEMPLATE.md` | exact |
| `.planning/spikes/_shared/{environment schema,replay helpers}` | utility / config | file-I/O, batch | `tools/validate-planning.py` | partial |
| `.planning/spikes/{spk-a-workspace,spk-b-static-framework,spk-c-boundary-harness,spk-d-verified-loader,spk-e-content-rendering,spk-f-course-workbench,spk-g-package-conformance,spk-h-browser-egress,spk-i-diagram-motion,spk-j-code-editing,spk-k-deployment,spk-l-source-freshness}/` recipes, fixtures, manifests, measurements, reports | disposable spike / test harness | event-driven, file-I/O, batch | `templates/lab.example.yaml` plus `templates/RESEARCH-REPORT-TEMPLATE.md` | role-match |
| `.planning/adr/{0001...0011}-*.md` proposed ADR recommendations | documentation / decision record | transform | `templates/ADR-TEMPLATE.md` | exact |
| `.planning/research/reports/{validation,refresh}*.md` and review-work output | report / event record | event-driven, transform | `templates/RESEARCH-REPORT-TEMPLATE.md` | role-match |

## Pattern Assignments

### `tools/validate-planning.py` extension and/or `tools/validate-research.py` (utility / validator CLI, batch + file-I/O)

**Analog:** `tools/validate-planning.py`

Use the existing standard-library CLI shape; either extend it with a clearly isolated Phase 1 command path or introduce `tools/validate-research.py` with the same conventions. The validator must perform two ordered gates: per-record Draft 2020-12 validation, then cross-record semantic/link validation. It should emit compact `ERROR CODE: message` diagnostics and return non-zero on any error. Do not replace the existing baseline validator or bypass its archive/scaffold protections.

**Imports and roots pattern** (lines 3-15):
```python
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / ".planning"
```

**Defensive parser and diagnostic accumulator pattern** (lines 17-27, 38-45):
```python
def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON: {exc}") from exc

errors: list[str] = []
warnings: list[str] = []

def error(code: str, message: str) -> None:
    errors.append(f"{code}: {message}")

def warn(code: str, message: str) -> None:
    warnings.append(f"{code}: {message}")
```

**Validation/exit pattern** (lines 152-166):
```python
for message in warnings:
    print(f"WARN {message}")
for message in errors:
    print(f"ERROR {message}")

if errors:
    print(f"Planning validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1

print(f"Planning validation passed: 0 errors, {len(warnings)} warning(s).")
return 0
```

**Required research-specific addition:** safely parse YAML only after the human package checkpoint; validate schemas and instances separately; then build one in-memory ID index and reject dangling IDs, invalid relations, baseline mismatches, and invalid status transitions. Never auto-rewrite accepted claim prose, maturity, approval, or ADR status.

---

### `.planning/research/schemas/*.schema.json` and record validators (config/model, transform)

**Analogs:**
- `docs/learn-napplets-codex-pack-v3/templates/source-registry.example.yaml`
- `docs/learn-napplets-codex-pack-v3/templates/claim.example.yaml`
- `docs/learn-napplets-codex-pack-v3/templates/drift.example.yaml`
- `docs/learn-napplets-codex-pack-v3/templates/compatibility-matrix.example.yaml`
- `docs/learn-napplets-codex-pack-v3/templates/open-question.example.yaml`

These examples establish record *shape*, not proof of upstream facts. Put a versioned `$schema` and schema version in each new JSON Schema. Define stable typed IDs and closed/strict required fields where the policy requires an auditable field. Store relations by ID; do not duplicate mutable source content inside claims.

**Immutable source identity pattern** — `source-registry.example.yaml` lines 1-23:
```yaml
sources:
  - id: nip-5d
    authority: current-nip-draft
    maturity: draft
    repository: nostr-protocol/nips
    path: 5D.md
    livingUrl: https://github.com/nostr-protocol/nips/pull/2303
    immutableUrl: REPLACE_DURING_RESEARCH
    ref: refs/pull/2303/head
    commitSha: REPLACE_DURING_RESEARCH
    contentSha256: REPLACE_DURING_RESEARCH
    observedAt: REPLACE_DURING_RESEARCH
    lastCheckedAt: REPLACE_DURING_RESEARCH
```

**Claim-to-source link pattern** — `claim.example.yaml` lines 1-18:
```yaml
claims:
  - id: claim.example
    statement: Replace with one concise source-linked claim.
    evidenceClass: current-nip-draft
    maturity: draft
    sources:
      - sourceId: nip-5d
        path: 5D.md
        section: Replace with section
        excerptSha256: REPLACE_DURING_RESEARCH
    affectedContent:
      - lesson.example
    affectedCode:
      - lab.example
    lastVerified: REPLACE_DURING_RESEARCH
```

**Parallel conflict record pattern** — `drift.example.yaml` lines 1-17:
```yaml
items:
  - id: drift.example
    topic: Replace with drift topic
    claims:
      - sourceRef: source-a
        statement: ""
      - sourceRef: source-b
        statement: ""
    impact:
      content: []
      code: []
      knowledge: []
    status: open
    resolutionEvidence: []
```

**Compatibility baseline pattern** — `compatibility-matrix.example.yaml` lines 1-17:
```yaml
records:
  - id: compatibility.example
    sourceBaseline:
      nip5dCommit: REPLACE_DURING_RESEARCH
      napsCommit: REPLACE_DURING_RESEARCH
    packages:
      - name: "@napplet/example"
        version: REPLACE_DURING_RESEARCH
        publicExports: []
    runtimes: []
    domains: []
    fixtures: []
    knownDrift: []
    tests: []
```

**Blocker/impact pattern** — `open-question.example.yaml` lines 1-12:
```yaml
questions:
  - id: question.example
    question: ""
    whyItMatters: ""
    sourceRefs: []
    affectedConcepts: []
    affectedLessons: []
    blockedDecisions: []
    currentEvidence: []
    resolutionCriteria: []
    status: open
```

---

### `.planning/research/*.md`, research reports, and `.planning/research/lesson-packets/*.md` (documentation, transform)

**Analogs:**
- `docs/learn-napplets-codex-pack-v3/templates/RESEARCH-REPORT-TEMPLATE.md`
- `docs/learn-napplets-codex-pack-v3/templates/LESSON-RESEARCH-PACKET-TEMPLATE.md`

Every claim-bearing report must retain the policy’s separation between upstream facts, observations, conflicts, inference, project recommendation, and uncertainty. Do not present a source-pack statement or project CSP choice as current protocol fact.

**Research report section order** — `RESEARCH-REPORT-TEMPLATE.md` lines 1-35:
```markdown
# Research Report — Question

## Research question
## Why it matters
## Sources
## Observations
## Conflicts and drift
## Inferences
## Prototype or measurement
## Recommendation
## Uncertainty
## Affected phases/content/code
## Disposition
```

**Lesson packet pattern** — `LESSON-RESEARCH-PACKET-TEMPLATE.md` lines 1-44:
```markdown
# Lesson Research Packet — Title

- **Lesson ID:**
- **Primary audience:**
- **Prerequisites:**
- **Last researched:**

## Learner question
## Intended outcome
## Current terminology
## Candidate claims
## Implementation and runtime evidence
## Drift and open questions
## Misconceptions to address
## Story representation
## System representation
## Wire representation
## Code representation
## Candidate instrument
## Required fixtures and tests
## Do not teach as settled
## Follow-up research
```

Use exactly thirteen independently reviewable `LES-*` packets. Candidate claims must cite existing record IDs and their true evidence state; disputed/provisional/blocked/stale items belong in the explicit “Do not teach as settled” and follow-up sections.

---

### `.planning/spikes/_shared/*` and `.planning/spikes/spk-*/{recipe,metadata,fixture,environment,measurements,report}` (disposable spike/test harness, event-driven + file-I/O)

**Analogs:**
- `docs/learn-napplets-codex-pack-v3/templates/lab.example.yaml`
- `docs/learn-napplets-codex-pack-v3/templates/RESEARCH-REPORT-TEMPLATE.md`

The source pack specifies twelve mandatory spike directories: A workspace, B static framework, C boundary harness, D verified loader, E content rendering, F course/workbench, G package/conformance, H browser egress, I diagram/motion, J code editing, K deployment, and L source freshness. These are isolated non-production experiments, not an app scaffold. Each must include a machine-readable `SPK-*` envelope, deterministic local replay input, environment manifest, measurement values, raw-output digest where applicable, and a report.

**Lab accessibility/traceability fields** — `lab.example.yaml` lines 1-14:
```yaml
id: lab.example
lesson: lesson.example
implementation: conceptual-simulation
hostProfile: none
objective: ""
states: []
failureModes: []
sourceRefs: []
transcript: ""
staticFallback: ""
reducedMotion: ""
compatibilityRef:
```

**Required report disposition vocabulary** — `RESEARCH-REPORT-TEMPLATE.md` lines 22-35:
```markdown
## Prototype or measurement
## Recommendation
## Uncertainty
## Affected phases/content/code
## Disposition

- delete spike;
- retain as fixture;
- promote later;
- blocked.
```

For every spike define the hypothesis, variables, exact environment, commands, success/failure/blocked thresholds before execution. For nondeterministic results, retain all five values and report range plus median. Browser reports must separately identify upstream statement, observed browser behavior, and proposed project policy.

---

### `.planning/adr/0001-*.md` through `.planning/adr/0011-*.md` (documentation/decision record, transform)

**Analog:** `docs/learn-napplets-codex-pack-v3/templates/ADR-TEMPLATE.md`

Create recommendations only: each ADR remains `proposed` until the required human review. The source pack lists 0001–0008, while current Phase 1 research also requires recommendations through 0011; preserve the same template structure for all current ADR records rather than treating a source-pack inventory as an upper bound.

**Metadata and evidence boundary** — `ADR-TEMPLATE.md` lines 1-19:
```markdown
# ADR NNNN — Title

- **Status:** proposed | accepted | rejected | superseded
- **Date:**
- **Owners:**
- **Related phases:**
- **Source refs:**

## Context
## Upstream facts

List current source-linked facts. These are not local choices.

## Local decision boundary

Which parts are Learn Napplets product/implementation decisions?
```

**Human-review/revisit pattern** — `ADR-TEMPLATE.md` lines 29-53:
```markdown
## Evidence
## Decision
## Host/guest implications
## Human/LLM implications
## Consequences
## Risks
## Revisit triggers

Which source change or measurement should reopen this ADR?
```

---

### `.gitignore`, acquisition cache, and `open-work-snapshot.json` (config/data snapshot, file-I/O)

**Analogs:** `.gitignore`; `.planning/traceability/pack-v3-file-manifest.json`

Append narrowly scoped cache/output ignores without removing the existing `*.zip` rule. `.research/upstreams/` (and spike-local caches/build outputs, if used) must remain untracked. Commit manifests, failure/retry records, source digests, cited excerpts, and replay inputs—not clones, package trees, browser binaries, builds, or transport logs.

**Versioned manifest pattern** — `pack-v3-file-manifest.json` lines 1-9:
```json
{
  "schemaVersion": 1,
  "sourcePack": "learn-napplets-codex-pack-v3",
  "sourcePath": "docs/learn-napplets-codex-pack-v3",
  "sourceCommit": "c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0",
  "validatedOn": "2026-07-23",
  "validator": "docs/learn-napplets-codex-pack-v3/scripts/validate-pack.py",
  "validatorResult": "passed",
  "files": []
}
```

Use a similar versioned, explicitly dated structure for generated snapshots, while source records remain canonical YAML.

## Shared Patterns

### Canonical planning and archive integrity

**Sources:** `tools/validate-planning.py` lines 47-64, 80-93, 127-130; `.planning/validation/required-artifacts.json` lines 18-27.

All new work belongs under `.planning/`, except ignored acquisition cache. Retain the existing validator’s canonical-artifact checks and SHA-256 archive verification. The pre-Phase-3 block on `package.json`, `pnpm-workspace.yaml`, `src`, `apps`, and `packages` remains active for every implementation plan.

### Evidence required fields and verification state

**Source:** `.planning/governance/evidence-policy.md` lines 7-30.

Every source/claim/spike/ADR-facing record must preserve stable IDs, immutable source identity, locator, retrieval/digest, authority/evidence/maturity classification, explicit uncertainty and impacts, ownership/review state, freshness, and revisit trigger. Only human-approved, complete, locator-supported claims are `verified`; changed source identity marks linked records `stale`, unavailable sources are `blocked`.

### Human approval boundary

**Source:** `.planning/governance/approval-matrix.md` lines 5-24.

Automation may collect evidence, validate shape/links, and issue review work. It cannot accept ADRs, verify claims on a human’s behalf, approve exceptions, or move through approval-bearing phase transitions. Preserve the responsible/required-approver distinction and dated, role-specific sign-offs for high-risk work.

### Error, blocker, and retry handling

**Sources:** `tools/validate-planning.py` lines 17-22 and 152-162; `.planning/governance/evidence-policy.md` lines 24-30.

Convert unreadable/invalid local inputs into deterministic diagnostics. Convert acquisition/rate-limit/source-availability failures into retained records and scoped `blocked`/`stale` impacts, never a false clean refresh or silently altered claim. A refresh collector emits comparison/review output only.

### Dependency checkpoint

**Source:** `01-RESEARCH.md` lines 160-169, 493-507.

`PyYAML`, `jsonschema`, and `playwright` are all flagged `SUS`. Put an explicit human-verification checkpoint before installation, then pin approved versions and provenance/hash/license decisions in the tools environment record. Until then, do not implement a hand-rolled YAML parser or JSON Schema engine; a missing approved toolchain is a legitimate scoped blocker.

## No Analog Found

| File(s) | Role | Data Flow | Reason and safest pattern |
|---|---|---|---|
| `requirements-phase1-tools.txt` / isolated environment manifest | config | batch | Repository has no dependency manifest. Add only after human verification; pin exact approved versions and provenance. Do not add a production package manifest. |
| `tests/phase1/*.py` | test | batch, file-I/O | No existing test suite. Use standard-library `unittest`, deterministic checked-in fixtures, temporary directories, and the six test groups specified in `01-RESEARCH.md` lines 523-532. |
| JSON Schema documents and deterministic migration code | config / utility | transform | No schema engine or migration precedent exists. Adopt Draft 2020-12 through the reviewed library behind the narrow validator CLI, with schema/instance/semantic tests. |
| Browser runner/replay helpers | disposable test harness | event-driven, file-I/O | No browser automation precedent exists. Confine to `.planning/spikes/`; use clean contexts, local fixtures, environment manifests, and five-sample handling. |
| Source acquisition and refresh collector | utility | request-response, file-I/O, transform | No network utility precedent exists. Make it local/read-only, allowlisted and bounded; resolve immutable Git commit/blob before digesting; produce failure/review records without mutating accepted evidence. |

## Metadata

**Analog search scope:** repository root; `tools/`; `.planning/validation/`; `.planning/governance/`; `.planning/traceability/`; preserved `docs/learn-napplets-codex-pack-v3/templates/` and Phase 0 research plan.  
**Files scanned/read:** 24 direct files plus Graphify navigation query.  
**Pattern extraction date:** 2026-07-23
