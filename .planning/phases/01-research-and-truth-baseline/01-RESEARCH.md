# Phase 1: Research and Truth Baseline - Research

**Researched:** 2026-07-23  
**Domain:** Revision-pinned evidence operations, structured research records, reproducible browser spikes, and governance traceability  
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

## Implementation Decisions

### Source acquisition
- **D-01:** Use blocking-first acquisition: deeply acquire sources needed for Phase 1 decisions and first-lab selection; catalog other known sources without exhaustive cloning.
- **D-02:** Stop acquisition when every blocking claim, ADR recommendation, and spike has primary evidence or an explicit impact-scoped blocker; source-count and ecosystem exhaustiveness are not completion criteria.
- **D-03:** Discover additional sources through bounded snowballing: follow authoritative references, imports, and manifests one hop; go deeper only when a blocking decision requires it.
- **D-04:** Pin canonical evidence with official host/repository identity, ref/commit SHA, path/locator, retrieval time, and content digest. Record signed tag/commit status when available, but do not require signatures universally.
- **D-05:** Record both latest relevant published/released state and current default-branch/open-work state when they differ. Published packages are tested; repository HEAD is compared for unreleased drift.
- **D-06:** Treat issues, PRs, discussions, and draft proposals as directional evidence and revisit triggers, never sole proof of shipped behavior.
- **D-07:** Use generated docs as discovery/corroboration; verify blocking behavior against pinned source, schemas, tests, or measurements.
- **D-08:** Inspect targeted history around blocking claims and changed interfaces. Inspect transitive dependencies only when they affect protocol shape, security boundaries, browser viability, build identity, or licensing.
- **D-09:** Keep clones/downloads in ignored cache. Commit manifests, digests, failure/retry records, and minimal license-aware cited excerpts—not full upstream trees, build output, or transport logs.
- **D-10:** Public read-only network access is allowed without per-source confirmation. Authentication, posting, issue/PR creation, or other external writes require explicit approval.
- **D-11:** Missing sources block only dependent claims/decisions. A corroborated mirror/archive may be a temporary fallback; authenticity uncertainty keeps affected claims blocked.
- **D-12:** Represent conflicts as parallel truth records by authority, maturity, normative statement, observed behavior, and affected scope. Do not silently force a winner.
- **D-13:** When a source moves/disappears, replace the canonical pointer but retain old ID, digest, locator, affected decisions, and replacement history in the audit log.

### Evidence acceptance
- **D-14:** A blocking claim requires a pinned primary source plus independent corroboration from schema/test/implementation evidence or reproducible measurement where behavior matters.
- **D-15:** Research owner prepares evidence; protocol/technical role approves blocking claims; content role reviews teaching impact. Agents may review/recommend but cannot supply human approval.
- **D-16:** Keep normative requirements and observed implementation behavior separate when they disagree.
- **D-17:** Inference may guide research and recommendations but never verifies a blocking claim by itself.
- **D-18:** Use structured states—`verified`, `disputed`, `provisional`, `blocked`, `stale`—with explicit reasons. Do not use numeric confidence scores.
- **D-19:** Credible unresolved conflicts become `disputed` and block only dependent decisions/content. Clearly labeled comparison teaching remains possible when useful.
- **D-20:** Phase 1 measures volatility and recommends source-specific freshness tiers. Expired evidence becomes `stale`, remains in history, and blocks new dependent approvals/publication until refreshed or explicitly deferred.

### Spike boundaries
- **D-21:** Run each mandatory spike in an isolated disposable directory/worktree or temporary environment; never inside a future production scaffold.
- **D-22:** Define hypothesis, variables, environment, measurements, success threshold, failure outcome, and blocked outcome before execution.
- **D-23:** Commit reproducible recipe/config/fixtures, summarized measurements, all decision-relevant values, key raw output/digests, and conclusions. Exclude caches, clones, dependency trees, builds, and bulky logs.
- **D-24:** Live public probes are allowed only when essential, read-only, and sandboxed. Capture inputs and provide deterministic local replay; no real secrets, keys, or destructive state.

### Decision closure
- **D-25:** Phase 1 recommends ADR outcomes only. Phase 2/project-owner review accepts, rejects, or defers them.
- **D-26:** Phase 1 may pass with unresolved upstream blockers only when each blocker is impact-scoped, affected claims/phases are mapped, and a safe fallback/defer path is approved.
- **D-27:** User currently fills product, protocol/technical, security, accessibility, content/learning, and release roles.
- **D-28:** High-risk decisions still require distinct dated per-role sign-offs even when one user fills every role; one generic approval cannot implicitly satisfy all roles.

### Record schemas
- **D-29:** Use stable semantic type-prefixed IDs such as `SRC-`, `CLM-`, `SPK-`, `ADR-`, and `LES-`. IDs never encode mutable titles, paths, status, or revisions. — **Reversibility:** costly — changing published IDs requires cross-record and downstream artifact migration.
- **D-30:** Canonical structured records use human-editable YAML validated by versioned JSON Schema; generated JSON is allowed for tools/exports. — **Reversibility:** costly — changing canonical formats requires record and validator migration.
- **D-31:** Cross-record links use stable IDs plus validated relation types such as `supports`, `contradicts`, `measures`, `affects`, `recommends`, and `supersedes`; dangling IDs fail validation. — **Reversibility:** costly — relation vocabulary changes affect all records, queries, and graph exports.
- **D-32:** Breaking schema changes increment schema version, provide deterministic migration, and retain change notes. Do not silently edit record meaning in place.

### Exit mechanics
- **D-33:** Overall Phase 1 result is `passed` or `blocked`; no broad “pass with warnings.”
- **D-34:** Reviewed research tracks may become accepted/reusable evidence while overall phase remains blocked on unrelated dependencies.
- **D-35:** Applicable mandatory gates cannot be waived as passed. A gate may be explicitly `not-applicable` or deferred only with impact mapping and approval.
- **D-36:** Relevant source/package/runtime change, stale blocking evidence, failed downstream assumption, or ADR revisit trigger opens targeted research work rather than rerunning all Phase 1 work.

### Reproduction matrix
- **D-37:** Phase 1 spike baseline is Linux with Chromium and Firefox. WebKit and wider OS coverage are not required for this phase unless a specific blocking decision later proves dependent on them.
- **D-38:** Every spike records exact OS/container, browser versions, Node/runtime/package-manager versions, dependencies, commands, environment flags, and hashes.
- **D-39:** For nondeterministic measurements, run five samples, retain every value, and report range plus median. The median is the decision summary value.

### Claude's Discretion
- Internal file layout below the required `.planning/research/`, `.planning/spikes/`, schema, and cache boundaries.
- Exact names for validated relation enums beyond the locked core set.
- Exact tooling used to create deterministic migrations and environment manifests, subject to plan review.

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EVID-01 | Maintainers can trace every blocking protocol-sensitive claim to an immutable upstream revision, path/locator, digest, retrieval date, authority tier, evidence class, and maturity label. | Source/claim schemas, a pinned-acquisition recipe, validation rules, and the source-to-claim link policy. [VERIFIED: .planning/REQUIREMENTS.md; .planning/governance/evidence-policy.md] |
| EVID-02 | Maintainers can see conflicts, uncertainty, known drift, affected requirements/phases, and refresh triggers for each volatile claim. | Parallel claim/conflict records, drift/open-question registers, freshness state machine, and impact-link validation. [VERIFIED: .planning/REQUIREMENTS.md; .planning/governance/evidence-policy.md] |
| EVID-03 | Maintainers can review compatibility across selected protocol sources, packages, runtimes, examples, and current work before architecture is accepted. | Compatibility record schema plus acquisition of released state and default-branch/open-work snapshots. [VERIFIED: 01-CONTEXT.md D-05; .planning/REQUIREMENTS.md] |
| EVID-04 | Decision makers can review measurable mandatory-spike evidence before accepting repository, framework, deployment, content, teaching-host, fixture, or portable-target recommendations. | Uniform spike contract, isolated disposable experiments, measured result reports, and proposed ADR packets. [VERIFIED: 01-CONTEXT.md D-21–D-24; .planning/REQUIREMENTS.md] |
| OPER-01 | Maintainers can detect upstream source/package/runtime drift, map impact, and create review work without silently rewriting accepted claims. | Read-only refresh collector, immutable comparison, impact graph, stale state, and explicit review-work output. [VERIFIED: .planning/REQUIREMENTS.md; .planning/governance/evidence-policy.md] |
| OPER-03 | Every phase has explicit owner/approver roles, measurable exit evidence, GSD verification status, and traceability to requirements. | Versioned phase-evidence/approval convention, a gate manifest, and validation of owner, approver, requirement, and verification fields. [VERIFIED: .planning/REQUIREMENTS.md; .planning/governance/approval-matrix.md] |
</phase_requirements>

## Summary

Phase 1 is a research-operations delivery, not a product implementation phase: it must establish canonical, revision-pinned YAML records; validate their relationships; run disposable evidence-producing spikes; and leave every architecture conclusion as a **proposed** ADR for human review. The current project already supplies the output inventory, approval boundaries, and an initial structural validator, while explicitly prohibiting production markers (`package.json`, `src/`, `apps/`, and `packages`) before Phase 3. [VERIFIED: .planning/validation/phase-gates.yaml; tools/validate-planning.py; CLAUDE.md]

Plan the work in dependency order, rather than by document type: first establish the schemas, IDs, validation command, ignored acquisition cache, and report templates; then acquire Tier-1 sources and derive source/claim/drift/compatibility records; then run the twelve isolated spikes using the same reproducibility envelope; then assemble thirteen lesson packets, catalogues, ADR recommendations, and the phase gate report. A protocol statement remains `blocked`, `provisional`, `disputed`, or `stale` unless its prescribed evidence and human approval are present; agents cannot make it `verified`. [VERIFIED: 01-CONTEXT.md D-14–D-20, D-33–D-36; .planning/governance/evidence-policy.md]

The primary implementation risk is confusing the preserved source pack with current upstream proof. The source pack provides the research questions and acceptance shape, but its own hierarchy says current revision-pinned upstream evidence outranks it; do not invent any protocol conclusion while planning. [VERIFIED: .planning/traceability/pack-v3-import.md; CLAUDE.md]

**Primary recommendation:** Create a small, Python-driven evidence toolchain around canonical YAML + JSON Schema before any acquisition or browser spike; make every later artifact, test, and ADR recommendation consume those validated records. [VERIFIED: 01-CONTEXT.md D-29–D-32; .planning/validation/phase-gates.yaml]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Revision-pinned source capture, digesting, and refresh comparison | API / Backend (local CLI) | Database / Storage | A deterministic local collector owns network retrieval, SHA/digest calculation, retry logs, and derived status; canonical results persist as version-controlled records. [VERIFIED: .planning/governance/evidence-policy.md; 01-CONTEXT.md D-04, D-09] |
| Canonical evidence, claim, conflict, compatibility, and gate records | Database / Storage | API / Backend (local CLI) | YAML is the canonical human-editable store, while the local validator enforces schemas and stable references before records become inputs to reports or ADRs. [VERIFIED: 01-CONTEXT.md D-29–D-32; .planning/validation/phase-gates.yaml] |
| Browser-boundary and egress observations | Browser / Client | API / Backend (local CLI) | Iframe sandbox, injection, `postMessage`, source-window, and egress behavior must be measured by real browser primitives; the runner only orchestrates and records them. [VERIFIED: docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md §9C, §9H; 01-CONTEXT.md D-37–D-39] |
| Teaching-host and framework conclusions | API / Backend (local disposable harness) | Browser / Client | The harness records host-policy and protocol observations, while browser behavior is evidence; neither is production host code in Phase 1. [VERIFIED: .planning/ROADMAP.md §Phase 1; CLAUDE.md] |
| Human approval and ADR acceptance | Database / Storage (approval records) | — | The workflow records owners, required approvals, evidence IDs, and exit status; a project owner supplies acceptance outside automation. [VERIFIED: .planning/governance/approval-matrix.md; 01-CONTEXT.md D-15, D-25, D-28] |

## Project Constraints (from CLAUDE.md)

- `.planning/STATE.md` is the sole live project-status source; `.planning/PROJECT.md`, `REQUIREMENTS.md`, and `ROADMAP.md` define scope.
- Preserve `docs/learn-napplets-codex-pack-v3/`; do not edit it during normal project work.
- Stop and record any conflict between canonical planning and current revision-pinned upstream protocol evidence; never silently override upstream facts.
- Do not create production app/framework scaffolding before Phase 1 research/spikes, required ADR recommendations and approval, and the Phase 2 contract pass; mark disposable spikes as non-production.
- For protocol-sensitive claims, record immutable revision, locator, digest, retrieval date, authority/evidence/maturity classifications, uncertainty, affected requirements/phases, and refresh trigger.
- Keep upstream fact, proposal/draft, observed behavior, project policy, and inference separate.
- Use GSD lifecycle and retain human stops at ADR acceptance, external actions, UAT, failed verification, security blockers, phase transition approval, and release.
- Required learning paths are deterministic; trusted hosts own sensitive/repetitive authority; guest napplets receive only declared mediated capabilities.
- Essential interactions require keyboard operation, reduced motion, transcript/state inspection, reset/replay, and static equivalents.
- Human and LLM essential facts derive from common structured sources; Graphify is navigation/indexing, never evidence authority.

## Standard Stack

### Core

| Library / Tool | Version | Purpose | Why Standard |
|----------------|---------|---------|--------------|
| Git CLI | 2.51.2 installed | Resolve commits and exact `revision:path` blobs; capture content by object ID. | Use `git rev-parse --verify --end-of-options "$REV^{commit}"` and resolve a verified blob before hashing/reading it; this is the project’s immutable-source backbone. [CITED: https://git-scm.com/docs/git-rev-parse] |
| YAML + JSON Schema Draft 2020-12 | Schema dialect, not a package | Canonical human-editable records plus versioned structural and relationship validation. | `$schema` identifies a schema’s dialect and meta-schema; validate the schema itself and the parsed YAML instance separately. [CITED: https://json-schema.org/draft/2020-12/json-schema-core] |
| Python | 3.14.3 installed | Deterministic local collectors, validation, report generation, fixture replay, and existing validator extension. | The repository already has a standard-library Python validator; extend it rather than replace it with an application framework. [VERIFIED: tools/validate-planning.py; environment audit 2026-07-23] |

### Supporting

| Library | Verified version / publish date | Purpose | When to Use |
|---------|---------------------------------|---------|-------------|
| `PyYAML` [WARNING: flagged as suspicious — verify before using.] | PyPI 6.0.3; published 2025-09-25 | Parse canonical YAML records using `yaml.safe_load`, then pass plain data to JSON Schema validation. [CITED: https://pyyaml.org/wiki/PyYAMLDocumentation] | Install only after the required human package-verification checkpoint. [VERIFIED: PyPI registry audit 2026-07-23] |
| `jsonschema` [WARNING: flagged as suspicious — verify before using.] | PyPI 4.26.0; published 2026-01-07 | Validate Draft 2020-12 record instances and schema documents in the local toolchain. [CITED: https://python-jsonschema.readthedocs.io/en/stable/] | Install only after the required human package-verification checkpoint. [VERIFIED: PyPI registry audit 2026-07-23] |
| `playwright` [WARNING: flagged as suspicious — verify before using.] | PyPI 1.61.0; published 2026-06-29 | Execute disposable, clean-slate Chromium/Firefox browser spikes and record repeatable observations. [CITED: https://playwright.dev/python/docs/library] | Install only after the required human package-verification checkpoint; use only in `.planning/spikes/`, never as a product framework. [VERIFIED: PyPI registry audit 2026-07-23] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| JSON Schema validator | Handwritten field/reference checks | Reject: nested schema semantics, reference integrity, and deterministic migration validation are core safety properties; keep only project-specific semantic checks outside the schema engine. [CITED: https://json-schema.org/draft/2020-12/json-schema-core] |
| Browser-runner automation | Manual Chrome/Firefox procedures | Reject for blocking spikes: manual procedures cannot reliably produce per-run environment manifests, reusable assertions, or five-sample evidence. Playwright contexts supply clean-slate isolation. [CITED: https://playwright.dev/docs/browser-contexts] |
| Git object retrieval | Mutable raw/default-branch URLs | Reject: a branch/PR URL can move. Capture the resolved commit and content/blob digest; mutable URLs remain discovery pointers only. [CITED: https://git-scm.com/docs/git-rev-parse] |

**Installation:**

```bash
# Human checkpoint required first: inspect package provenance and approve all three SUS verdicts.
python3 -m pip install "PyYAML==6.0.3" "jsonschema==4.26.0" "playwright==1.61.0"
python3 -m playwright install chromium firefox
```

The Phase 1 browser baseline is Chrome/Chromium plus Firefox; Playwright’s own compatible browser binaries should be recorded in each spike environment manifest rather than inferred from the host browser version. [CITED: https://playwright.dev/docs/browsers; VERIFIED: 01-CONTEXT.md D-37–D-38]

**Version verification:** `pip index versions PyYAML`, `pip index versions jsonschema`, and `pip index versions playwright` returned 6.0.3, 4.26.0, and 1.61.0 respectively on 2026-07-23. [VERIFIED: PyPI registry audit 2026-07-23]

## Package Legitimacy Audit

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| `PyYAML` | PyPI | published 2025-09-25 | not supplied by legitimacy seam | https://pyyaml.org/ | SUS — unknown downloads | Flagged — planner must add `checkpoint:human-verify` before install. [VERIFIED: package-legitimacy audit 2026-07-23] |
| `jsonschema` | PyPI | published 2026-01-07 | not supplied by legitimacy seam | https://github.com/python-jsonschema/jsonschema | SUS — unknown downloads | Flagged — planner must add `checkpoint:human-verify` before install. [VERIFIED: package-legitimacy audit 2026-07-23] |
| `playwright` | PyPI | published 2026-06-29 | not supplied by legitimacy seam | none reported by legitimacy seam | SUS — too new, unknown downloads, no repository | Flagged — planner must add `checkpoint:human-verify` before install. [VERIFIED: package-legitimacy audit 2026-07-23] |

**Packages removed due to [SLOP] verdict:** none. [VERIFIED: package-legitimacy audit 2026-07-23]  
**Packages flagged as suspicious [SUS]:** `PyYAML`, `jsonschema`, and `playwright`; no plan may install them before the human checkpoint records provenance, intended version, license, and locked hash/source decision. [VERIFIED: package-legitimacy audit 2026-07-23]

## Architecture Patterns

### System Architecture Diagram

```text
             public, read-only upstream hosts
                         |
                         | discovery pointer / API response (untrusted input)
                         v
      +---------------------------------------+
      | Local acquisition CLI                 |
      | allowlisted host -> resolve ref/SHA    |
      | capture path, locator, bytes, digest   |
      | retry/failure log; no external writes  |
      +--------------------+------------------+
                           |
                           v
      +---------------------------------------+
      | Canonical YAML records                |
      | SRC-* -> CLM-* -> DRF-* / CMP-*       |
      |       -> OQ-* / LES-* / ADR-*          |
      +--------------------+------------------+
                           |
              JSON Schema + semantic link validation
                           |
            +--------------+----------------+
            |                               |
            v                               v
 +------------------------+      +-----------------------------+
 | Research outputs       |      | Disposable spike runner     |
 | maps, catalogs,        |      | browser/package/framework   |
 | compatibility/current  |      | measurements + replay       |
 | work, lesson packets   |      +-------------+---------------+
 +------------+-----------+                    |
              |                                v
              +--------------->+-----------------------------+
                                | SPK-* report + measurement  |
                                | source / environment / hash |
                                +-------------+---------------+
                                              |
                                              v
                                +-----------------------------+
                                | Proposed ADR + phase gate    |
                                | owner/approver/requirements  |
                                +-------------+---------------+
                                              |
                                   human review; never automated acceptance
```

Every arrow between a network response and an accepted record must retain provenance and validation results; every arrow into an ADR is a recommendation, not acceptance. [VERIFIED: 01-CONTEXT.md D-04, D-14–D-20, D-25; .planning/governance/evidence-policy.md]

### Recommended Project Structure

```text
.planning/
├── research/                         # committed canonical evidence records and derived reports
│   ├── schemas/                       # versioned JSON Schemas + migration notes
│   ├── source-registry.yaml           # SRC-* records
│   ├── claims.yaml                    # CLM-* records and source links
│   ├── compatibility-matrix.yaml      # CMP-* source/package/runtime/example rows
│   ├── drift-register.yaml            # DRF-* parallel conflict records
│   ├── open-questions.yaml            # OQ-* blockers and impact mappings
│   ├── lesson-packets/                # exactly 13 LES-* packets
│   └── reports/                       # generated refresh/validation summaries
├── spikes/                            # disposable, non-production SPK-* recipes/results/fixtures
│   ├── _shared/                       # replay helpers and environment-manifest schema
│   └── spk-*/                         # isolated experiment, not application scaffolding
├── adr/                               # proposed ADR 0001–0011 recommendations and evidence links
├── validation/                        # validator extension, gate contract, schema tests
└── phases/01-research-and-truth-baseline/
    └── 01-RESEARCH.md                 # planning research only

.research/
└── upstreams/                         # ignored clones/downloads/cache; never committed
```

Add `.research/` to `.gitignore` before acquisition, because the repository’s current ignore file contains only `*.zip` while the locked decision requires clones/downloads in an ignored cache. [VERIFIED: .gitignore; 01-CONTEXT.md D-09]

### Pattern 1: Immutable source record before claim record

**What:** Create and validate `SRC-*` records first. A claim links only by stable source ID plus exact commit, path/locator, and source/excerpt digest; it does not embed mutable URLs as sufficient proof.

**When to use:** For every protocol-sensitive claim, package/runtime compatibility row, evidence-backed lesson statement, and ADR input.

**Example:**

```yaml
# Source: project-required record policy; fields are a planning pattern, not upstream protocol facts.
id: SRC-NIP5D-001
kind: source
repository: owner/repository
livingUrl: https://github.com/owner/repository/pull/123
immutableUrl: https://github.com/owner/repository/blob/<commit>/path/file.md
ref: refs/pull/123/head
commitSha: <40-or-64-hex-object-id>
path: path/file.md
locator: "§ Security considerations"
contentSha256: <sha256-of-exact-retrieved-content>
retrievedAt: 2026-07-23T00:00:00Z
authorityTier: upstream-nip-draft
evidenceClass: specification
maturity: draft
freshness:
  state: provisional
  refreshTrigger: "PR head SHA, path, or content digest changes"
```

The Git verification sequence must resolve the commit first, resolve that commit’s path to a blob second, then read/hash that blob; `rev:path` names the content at that revision rather than a moving branch tip. [CITED: https://git-scm.com/docs/git-rev-parse]

### Pattern 2: Schema validation plus semantic graph validation

**What:** Apply two gates. Gate 1 parses YAML safely and validates each record against its versioned Draft 2020-12 schema. Gate 2 builds an in-memory ID index and rejects dangling cross-record links, invalid relation types, inconsistent source revisions, and disallowed state transitions.

**When to use:** On every record change, generated report, spike result, and phase-gate run.

**Example:**

```python
# Source: JSON Schema requires schema/instance validation separation.
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

record = yaml.safe_load(Path(".planning/research/claims.yaml").read_text())
Draft202012Validator(claims_schema).validate(record)
validate_cross_record_links(record_index)  # project-specific semantic gate
```

Use `safe_load`; do not construct Python objects from untrusted YAML. Validate parsed data as an instance, and validate each schema against its declared Draft 2020-12 meta-schema during tooling tests. [CITED: https://pyyaml.org/wiki/PyYAMLDocumentation; https://json-schema.org/draft/2020-12/json-schema-core]

### Pattern 3: Evidence envelope for every spike

**What:** Put a machine-readable `SPK-*` metadata record beside a minimal recipe, local fixture, raw-value digest, and report. The record must include hypothesis, independent/dependent variables, exact environment, commands, success/failure/blocked thresholds, all five values when nondeterministic, range/median, sources, conclusion, uncertainty, and disposition.

**When to use:** For all twelve named Phase 1 spikes, including a result of `blocked`.

**Example:**

```yaml
id: SPK-EGRESS-001
status: planned                         # planned | passed | failed | blocked
hypothesis: "To be tested; no browser conclusion is pre-recorded."
environmentManifest: environment.json
samplesRequired: 5
measurements: []
successThreshold: "Defined before execution"
failureOutcome: "Reject the affected recommendation"
blockedOutcome: "Create OQ-* with requirement/ADR impact"
disposition: delete-spike
```

The result report must distinguish browser observation, upstream statement, and project CSP decision; a local CSP is never evidence of a protocol requirement. [VERIFIED: docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md §9H; docs/learn-napplets-codex-pack-v3/docs/09-QUALITY-SECURITY-ACCESSIBILITY.md §6]

### Pattern 4: Refresh detects and routes; reviewers interpret

**What:** The refresh CLI compares only canonical source identity, resolved commit, path/blob/content digest, and release/current-work markers. It emits `unchanged`, `changed`, `unavailable`, or `ambiguous`, marks affected records stale when necessary, and creates an explicit review-work record. It never changes claim prose, authority, maturity, or ADR status itself.

**When to use:** The source-freshness spike, each dependent phase planning event, and release review.

**Example:**

```text
resolve mutable pointer -> commit SHA -> revision:path blob -> SHA-256
       | unchanged                       | changed/unavailable
       v                                 v
  retain reviewed state          mark linked records stale/blocked
                                        -> emit OQ/refresh report
                                        -> human reviewer decides meaning
```

GitHub’s pull-request response exposes `head.sha`; rate-limit headers and bounded retry behavior must be captured in collector failures rather than hidden. [CITED: https://docs.github.com/en/rest/pulls/pulls; https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api]

### Anti-Patterns to Avoid

- **Source URL as proof:** A mutable branch or PR URL alone cannot satisfy immutable-source provenance; retain it only as a discovery pointer and record the resolved commit and content digest. [CITED: https://git-scm.com/docs/git-rev-parse]
- **One `status` field:** Do not merge provenance/evidence class, upstream maturity, review state, and freshness into one ambiguous value. [VERIFIED: CLAUDE.md; 01-CONTEXT.md D-16–D-20]
- **Conflict winner by convenience:** Do not overwrite a lower-authority source or a contradicting implementation observation; retain parallel records and map scope/impact. [VERIFIED: 01-CONTEXT.md D-12, D-16, D-19]
- **Spike as hidden scaffold:** Do not promote a framework or host experiment into `src/`, `apps/`, `packages/`, or a production lockfile. [VERIFIED: CLAUDE.md; tools/validate-planning.py]
- **Unbounded crawl:** Do not clone/deep-read the ecosystem until it is “complete”; stop when blocking claims, ADRs, and spikes have primary evidence or an impact-scoped blocker. [VERIFIED: 01-CONTEXT.md D-01–D-03]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| General JSON Schema evaluation | A custom recursive JSON Schema interpreter | A Draft 2020-12 validator behind a narrow local adapter | Schema dialect selection, meta-schema validity, references, and keyword semantics are established specifications; custom behavior would make evidence validation non-portable. [CITED: https://json-schema.org/draft/2020-12/json-schema-core] |
| YAML deserialization | Regex/split-based YAML parsing | `yaml.safe_load` followed by schema validation | YAML has nested collections, scalar typing, and unsafe constructors that a text parser will mishandle. [CITED: https://pyyaml.org/wiki/PyYAMLDocumentation] |
| Revision-pinned content resolution | String-concatenated raw GitHub URLs | Git object resolution (`rev-parse`) or an API-derived commit SHA followed by a local digest | A branch/PR reference can move, while verified commit/blob object IDs and captured digests are stable evidence inputs. [CITED: https://git-scm.com/docs/git-rev-parse; https://docs.github.com/en/rest/pulls/pulls] |
| Browser isolation/reproducibility | A shared browser profile or manually cleared state | A fresh browser context per test/spike sample | Clean-slate browser contexts remove state coupling and make failures reproducible. [CITED: https://playwright.dev/docs/browser-contexts] |
| Drift meaning resolution | An automatic text rewrite or inferred compatibility fix | Change report + impact mapping + human review | Automation can detect source movement, but only a reviewer can decide whether a semantic claim or recommendation changed. [VERIFIED: .planning/governance/evidence-policy.md; 01-CONTEXT.md D-36] |

**Key insight:** Phase 1’s product is an auditable decision trail. Reusable parsers, validators, Git object semantics, and browser isolation make the trail reproducible; project-specific policy remains in thin schemas and semantic validators. [VERIFIED: .planning/governance/evidence-policy.md; CITED: https://playwright.dev/docs/browser-contexts]

## Common Pitfalls

### Pitfall 1: Treating source-pack material as current upstream truth

**What goes wrong:** A preserved planning document is cited as proof of current protocol behavior.  
**Why it happens:** It is detailed, internally coherent, and easier to read than current upstream revisions.  
**How to avoid:** Use it only to enumerate research questions, then pin upstream source records before asserting a protocol fact; report any contradiction rather than editing around it. [VERIFIED: .planning/traceability/pack-v3-import.md; CLAUDE.md]  
**Warning signs:** A claim has a project-document source but no `SRC-*` revision/path/digest or uses phrases such as “the protocol requires” without an immutable upstream locator. [VERIFIED: .planning/governance/evidence-policy.md]

### Pitfall 2: Passing schema validation while links are broken

**What goes wrong:** Individually well-formed YAML references a missing source/claim/spike/ADR or an unapproved relationship.  
**Why it happens:** JSON Schema validates record shape, not the whole record graph.  
**How to avoid:** Run an ID-index and relation-vocabulary gate after per-file schema validation; make dangling IDs a hard failure. [VERIFIED: 01-CONTEXT.md D-31]  
**Warning signs:** A generated report omits evidence silently, or an affected requirement has no reverse links. [VERIFIED: .planning/governance/evidence-policy.md]

### Pitfall 3: Mutable PR state masquerading as a pin

**What goes wrong:** The registry stores only a PR number/ref or `main` URL, so replay fetches different content later.  
**Why it happens:** Git hosting UIs show friendly refs more readily than resolved object IDs.  
**How to avoid:** Store PR/ref as a discovery field but capture the observed `head.sha`, `revision:path`, and digest at acquisition time. [CITED: https://docs.github.com/en/rest/pulls/pulls; https://git-scm.com/docs/git-rev-parse]  
**Warning signs:** An immutable URL still contains a branch name, or rerunning a source digest produces a surprise change without a recorded event. [VERIFIED: 01-CONTEXT.md D-04, D-13]

### Pitfall 4: Measuring browser policy in the wrong context

**What goes wrong:** The runner tests egress or iframe behavior in a top-level page, a browser with retained state, or a different sandbox/loading setup than the selected source describes.  
**Why it happens:** Browser APIs work in both contexts, but security behavior can differ.  
**How to avoid:** Make the selected frame/sandbox/loading configuration a test fixture, capture browser version and flags, start a fresh context per test, and label observations as browser behavior rather than NIP requirements. [CITED: https://playwright.dev/docs/browser-contexts; VERIFIED: 01-CONTEXT.md D-37–D-39]  
**Warning signs:** Results cannot name iframe attributes, origin/referrer behavior, browser version, or whether browser behavior versus project CSP was measured. [VERIFIED: docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md §9H]

### Pitfall 5: Unreviewed automation silently changes evidence

**What goes wrong:** A collector sees a changed digest and updates an accepted claim/maturity/recommendation automatically.  
**Why it happens:** “Freshness” is misread as a content-regeneration task.  
**How to avoid:** Allow automation to mark linked work `stale` and create a review record only; require the designated human approval for a new verified claim or ADR state. [VERIFIED: .planning/governance/evidence-policy.md; .planning/governance/approval-matrix.md]  
**Warning signs:** Generated diffs alter explanatory prose or approval fields without a reviewer identifier and dated decision. [VERIFIED: 01-CONTEXT.md D-15, D-20]

### Pitfall 6: Package/tool installation bypasses the audit gate

**What goes wrong:** The plan installs a convenient parser or browser runner before provenance review.  
**Why it happens:** Registry existence is mistaken for supply-chain approval.  
**How to avoid:** Place explicit `checkpoint:human-verify` tasks before all flagged package installs, pin approved versions, and record install/browser-binary versions in each spike manifest. [VERIFIED: package-legitimacy audit 2026-07-23; 01-CONTEXT.md D-38]  
**Warning signs:** A plan has `pip install` without a preceding checkpoint or allows an unpinned package version. [VERIFIED: package-legitimacy audit 2026-07-23]

## Code Examples

Verified patterns from official sources:

### Resolve a commit and exact source blob

```bash
# Source: https://git-scm.com/docs/git-rev-parse
commit_oid=$(git rev-parse --quiet --verify --end-of-options "$REV^{commit}") || exit 1
blob_oid=$(git rev-parse --quiet --verify --end-of-options "$commit_oid:$PATH^{blob}") || exit 1
git cat-file blob "$blob_oid" > "$DESTINATION"
sha256sum "$DESTINATION"
```

The two-step resolution avoids reading a moving branch after `$REV` is reduced to a commit. [CITED: https://git-scm.com/docs/git-rev-parse]

### Use a fresh browser context for an evidence sample

```python
# Source: https://playwright.dev/docs/browser-contexts
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()  # fresh, non-persistent sample context
    page = context.new_page()
    page.goto(local_spike_url)
    # execute one asserted browser observation and serialize the result
    context.close()
    browser.close()
```

Run this sample through the same recipe five times for nondeterministic measurements, retaining each result and reporting range plus median. [CITED: https://playwright.dev/docs/browser-contexts; VERIFIED: 01-CONTEXT.md D-39]

### Validate a schema and a record as separate artifacts

```python
# Source: https://json-schema.org/draft/2020-12/json-schema-core
schema_validator = Draft202012Validator.check_schema(schema)
Draft202012Validator(schema).validate(record)
```

`check_schema` is the schema gate; `validate(record)` is the instance gate. A separate project semantic pass must still resolve cross-record IDs and relations. [CITED: https://json-schema.org/draft/2020-12/json-schema-core; VERIFIED: 01-CONTEXT.md D-31]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| One mutable “latest” source link and a prose summary | Resolve immutable commit/blob content, calculate a digest, preserve the mutable discovery URL separately, and map downstream impact before review | Required for this Phase 1 baseline | Enables replay and freshness checks without claiming that a branch URL is stable. [VERIFIED: 01-CONTEXT.md D-04, D-13; CITED: https://git-scm.com/docs/git-rev-parse] |
| A single confidence/status label | Separate authority/evidence class, maturity, review/verification state, freshness state, conflict state, and uncertainty | Locked by Phase 1 context | Prevents a draft/observation/policy/inference from being displayed as a verified protocol fact. [VERIFIED: 01-CONTEXT.md D-16–D-20; CLAUDE.md] |
| Manual one-off browser demonstrations | Isolated, version-manifested, locally replayable browser evidence with explicit success/failure/blocked outcomes | Required for Phase 1 spikes | Makes an ADR recommendation reviewable rather than anecdotal. [VERIFIED: 01-CONTEXT.md D-21–D-24, D-37–D-39; CITED: https://playwright.dev/docs/browser-contexts] |

**Deprecated/outdated:**
- Treating `docs/learn-napplets-codex-pack-v3/` as mutable execution state is prohibited; it is a preserved source/archive, while current state belongs in `.planning/STATE.md`. [VERIFIED: CLAUDE.md; .planning/traceability/pack-v3-import.md]
- Any source-plan instruction to update `.planning/STATUS.md` is superseded by the canonical migration to `.planning/STATE.md`. [VERIFIED: .planning/traceability/pack-v3-import.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The Python packages flagged `SUS` will be acceptable after human provenance/license review and can be used only for Phase 1 tooling. | Standard Stack; Package Legitimacy Audit | The plan must replace the toolchain or use a reviewed local environment; no install may proceed automatically. [ASSUMED] |
| A2 | A local Git checkout/clone is available for every source that requires `revision:path` blob resolution. | Architecture Patterns | API-only sources need an equivalent immutable-content retrieval adapter and a clearly recorded limitation. [ASSUMED] |
| A3 | The public upstream sources needed for Tier 1 research remain reachable read-only during execution. | Environment Availability | Affected claims must become blocked/stale and the phase may need an impact-scoped blocked result. [ASSUMED] |

## Open Questions (RESOLVED)

These are resolved planning dispositions, not accepted ADRs or settled upstream facts. The factual uncertainty stated below remains evidence work for Phase 1.

1. **Which exact source-record and relation-schema versioning layout should be canonical?**
   - What we know: YAML plus versioned JSON Schema, stable IDs, deterministic migrations, and the six core relation types are locked. [VERIFIED: 01-CONTEXT.md D-29–D-32]
   - What’s unclear: The file split, schema `$id` namespace, extension relation names, and migration-command interface are discretionary. [VERIFIED: 01-CONTEXT.md §Claude's Discretion]
   - Planning resolution: Plan 01-02 Tasks 1–2 owns one schema per record family and a central relation vocabulary; Plan 01-04 Task 2 owns deterministic migration fixtures and change notes. Validator or migration-fixture failure blocks dependent evidence records and reports; no all-purpose ontology is substituted.

2. **Which upstream documents/packages/runtimes meet Tier-1 proof needs?**
   - What we know: The scope requires current NIP-5D, NAP registry/projection, selected domain sources, `napplet/web`, credible runtimes, current work, and learning-product comparisons. [VERIFIED: docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md §§3–7]
   - What’s unclear: The current immutable revisions and whether any listed surface remains coherent enough for the first real lab.
   - Planning resolution: Plan 01-05 Tasks 1–2 performs bounded acquisition and claim triage; Plan 01-06 Task 1 records compatibility/current-work impacts. Only revision-pinned coherent sources enter Tier 1; unavailable or incoherent candidates become impact-scoped blockers under D-11, never training-knowledge substitutions.

3. **Can the three flagged packages be approved for this repository?**
   - What we know: Registry lookup found each package and the respective official documentation names them, but the legitimacy seam returned `SUS` for all three. [VERIFIED: package-legitimacy audit 2026-07-23; CITED: https://pyyaml.org/wiki/PyYAMLDocumentation; https://python-jsonschema.readthedocs.io/en/stable/; https://playwright.dev/python/docs/library]
   - What’s unclear: The project owner’s accepted supply-chain review standard and whether a preapproved tool environment is available.
   - Planning resolution: Plan 01-01 Task 1 is the blocking human approval checkpoint for PyYAML, jsonschema, Playwright, and its requested browser binaries; Plan 01-01 Task 2 installs only recorded approvals. A denial or unavailable reviewed environment blocks YAML/schema/browser-dependent tasks; no installation proceeds and no handwritten replacement is used.

4. **Do browser spikes need Playwright-managed binaries or can the installed Chrome/Firefox be driven directly?**
   - What we know: Google Chrome 150.0.7871.124 and Firefox 152.0.4 are installed; a `chromium` command is not installed. [VERIFIED: environment audit 2026-07-23]
   - What’s unclear: Disk/system-dependency availability for Playwright browser binaries and whether the source-sensitive behavior differs in installed Chrome versus the runner’s Chromium.
   - Planning resolution: Plan 01-01 Task 1 explicitly approves either reviewed installed Chrome/Firefox driving or approved Playwright-managed Chromium/Firefox binaries; Plan 01-01 Task 3 records the exact executable paths and versions. Browser-dependent spikes block if neither reviewed option passes the environment gate. WebKit is not required unless later evidence elevates it. [VERIFIED: 01-CONTEXT.md D-37–D-38]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Git | Revision-pinned source capture and preserved-pack integrity | ✓ | 2.51.2 | GitHub/API immutable commit/blob retrieval adapter when a clone is unavailable. [CITED: https://git-scm.com/docs/git-rev-parse] |
| Python | Existing validator and Phase 1 local tooling | ✓ | 3.14.3 | — [VERIFIED: environment audit 2026-07-23] |
| Node/npm | Candidate JavaScript-package/spike inspection and environment manifest | ✓ | Node 22.22.0; npm 10.9.4 | Do not make Node tooling a prerequisite for record validation. [VERIFIED: environment audit 2026-07-23] |
| Google Chrome | Browser observation baseline | ✓ | 150.0.7871.124 | Install a reviewed Playwright Chromium binary after human checkpoint. [VERIFIED: environment audit 2026-07-23; CITED: https://playwright.dev/docs/browsers] |
| Firefox | Browser observation baseline | ✓ | 152.0.4 | Install a reviewed Playwright Firefox binary after human checkpoint. [VERIFIED: environment audit 2026-07-23; CITED: https://playwright.dev/docs/browsers] |
| Playwright Python + binaries | Isolated, automated browser spikes | ✗ | — | Manual reconnaissance is non-gating only; a reviewed installation or equivalent isolated runner is required before calling browser-spike evidence reproducible. [CITED: https://playwright.dev/docs/browser-contexts] |
| PyYAML / `jsonschema` | Canonical YAML parsing and Draft 2020-12 validation | ✗ | — | Do not implement production validation manually; obtain human approval for the flagged packages or use an organization-approved equivalent. [CITED: https://pyyaml.org/wiki/PyYAMLDocumentation; https://json-schema.org/draft/2020-12/json-schema-core] |
| Docker | Optional pinned experiment container | ✓ | 29.6.1 | Record host OS/environment directly if a container would obscure browser behavior. [VERIFIED: environment audit 2026-07-23] |

**Missing dependencies with no fallback:**
- A human-approved schema-validation/YAML-parser toolchain and isolated browser runner are blocking for Phase 1’s machine-validated records and reproducible mandatory browser spikes. [VERIFIED: package-legitimacy audit 2026-07-23; .planning/validation/phase-gates.yaml]

**Missing dependencies with fallback:**
- The `chromium` command is absent, but installed Google Chrome and a reviewed Playwright Chromium binary are viable browser targets. [VERIFIED: environment audit 2026-07-23; CITED: https://playwright.dev/docs/browsers]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | None yet; only the existing Python structural validator is present. [VERIFIED: tools/validate-planning.py; repository scan 2026-07-23] |
| Config file | none — establish Phase 1 validation entry point in Wave 0. [VERIFIED: repository scan 2026-07-23] |
| Quick run command | `python3 tools/validate-planning.py` [VERIFIED: tools/validate-planning.py] |
| Full suite command | `python3 tools/validate-planning.py --phase-1-complete` plus new schema/semantic/spike replay tests. [VERIFIED: tools/validate-planning.py; .planning/validation/phase-gates.yaml] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EVID-01 | Reject source/claim records missing immutable identity, locator, digest, authority/evidence/maturity, or valid source link. | schema + semantic unit | `python3 -m unittest discover -s tests/phase1 -p 'test_evidence*.py'` | ❌ Wave 0 |
| EVID-02 | Reject volatile claims without conflicts/uncertainty/impact/refresh fields; verify transitions to stale/blocked preserve history. | unit + fixture | `python3 -m unittest discover -s tests/phase1 -p 'test_drift*.py'` | ❌ Wave 0 |
| EVID-03 | Reject compatibility rows with unknown source/package/runtime/example IDs or mixed source baselines. | semantic unit | `python3 -m unittest discover -s tests/phase1 -p 'test_compatibility*.py'` | ❌ Wave 0 |
| EVID-04 | Reject incomplete spike evidence envelopes and run deterministic local replay assertions where the tool/environment exists. | unit + integration | `python3 -m unittest discover -s tests/phase1 -p 'test_spikes*.py'` | ❌ Wave 0 |
| OPER-01 | Compare fixture source snapshots, emit a review-work record, and prove no accepted claim prose/state is auto-rewritten. | integration fixture | `python3 -m unittest discover -s tests/phase1 -p 'test_refresh*.py'` | ❌ Wave 0 |
| OPER-03 | Reject phase records without owners, approvers, requirement links, exit evidence, or GSD verification status. | schema + semantic unit | `python3 -m unittest discover -s tests/phase1 -p 'test_governance*.py'` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `python3 tools/validate-planning.py` plus the narrow `unittest` module touched by the task. [VERIFIED: tools/validate-planning.py]
- **Per wave merge:** `python3 -m unittest discover -s tests/phase1 && python3 tools/validate-planning.py`. [ASSUMED]
- **Phase gate:** Full suite green, `python3 tools/validate-planning.py --phase-1-complete`, required report/artifact count checks, and the required human review before `/gsd-verify-work`. [VERIFIED: .planning/validation/phase-gates.yaml; .planning/ROADMAP.md §Phase 1]

### Wave 0 Gaps

- [ ] `.planning/research/schemas/` — versioned Draft 2020-12 schemas for source, claim, drift, compatibility, open question, spike, and phase-governance records. [VERIFIED: 01-CONTEXT.md D-29–D-32]
- [ ] `tools/validate-research.py` or a clearly scoped extension to `tools/validate-planning.py` — YAML parsing, schema gate, semantic link gate, and compact diagnostics. [VERIFIED: 01-CONTEXT.md §Existing Code Insights]
- [ ] `tests/phase1/` — deterministic fixture-led schema, refresh, compatibility, governance, and spike-envelope tests. [ASSUMED]
- [ ] `requirements-phase1-tools.txt` or a human-approved isolated tool environment — all dependencies pinned after package checkpoint. [VERIFIED: package-legitimacy audit 2026-07-23]
- [ ] `.gitignore` entry for `.research/` and spike-local bulky outputs/caches. [VERIFIED: .gitignore; 01-CONTEXT.md D-09]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Phase 1 has no user-account authentication; authenticated upstream access, if ever needed, requires explicit approval and must not be a hidden prerequisite. [VERIFIED: 01-CONTEXT.md D-10] |
| V3 Session Management | yes — browser boundary spike only | Record and validate source-window/session mapping as an observed browser/protocol behavior; do not claim a production session design. [VERIFIED: docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md §9C] |
| V4 Access Control | yes | Keep host/guest authority and declared capability checks within disposable harnesses; no guest receives host-only authority. [VERIFIED: CLAUDE.md; .planning/PROJECT.md] |
| V5 Input Validation | yes | Treat all network data, cloned text, YAML, paths, and report inputs as untrusted; use safe parsing, Draft 2020-12 validation, strict stable-ID/relation checks, and allowlisted acquisition targets. [CITED: https://pyyaml.org/wiki/PyYAMLDocumentation; https://json-schema.org/draft/2020-12/json-schema-core] |
| V6 Cryptography | yes — source identity/verified-loader research | Use Git object IDs, SHA-256 digests, and the upstream/reviewed verification implementation; never hand-roll signatures, hashes, or aggregate verification. [CITED: https://git-scm.com/docs/git-rev-parse; VERIFIED: 01-CONTEXT.md D-24] |

### Known Threat Patterns for Phase 1 Tooling

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Mutable ref/PR changes after acquisition | Tampering | Resolve and record commit and blob/content digest; retain changes as drift and require review. [CITED: https://git-scm.com/docs/git-rev-parse; https://docs.github.com/en/rest/pulls/pulls] |
| Malicious YAML tags or schema-bypass fields | Tampering / Elevation of Privilege | `safe_load`, exact schema dialect, closed/strict record shapes where appropriate, and semantic-ID checks. [CITED: https://pyyaml.org/wiki/PyYAMLDocumentation; https://json-schema.org/draft/2020-12/json-schema-core] |
| Source collector rate-limit failure hidden as freshness | Denial of Service / Repudiation | Store attempt timestamp, HTTP/rate-limit data, bounded retry result, and `blocked`/`stale` impact rather than a false clean refresh. [CITED: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api] |
| Browser egress conclusion overgeneralized to protocol | Tampering / Information Disclosure | Test a named browser/frame/sandbox fixture; separately report upstream source statement, actual browser observation, and local CSP policy. [VERIFIED: docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md §9H; docs/learn-napplets-codex-pack-v3/docs/09-QUALITY-SECURITY-ACCESSIBILITY.md §6] |
| Learner/spike code obtaining host privileges | Elevation of Privilege | Run only disposable isolated spike code; never execute arbitrary code in a top-level host context and never use real secrets. [VERIFIED: CLAUDE.md; docs/learn-napplets-codex-pack-v3/docs/09-QUALITY-SECURITY-ACCESSIBILITY.md §7] |

## Sources

### Primary (HIGH confidence)

- `.planning/REQUIREMENTS.md` — Phase-owned requirement wording and ownership. [VERIFIED: repository source]
- `.planning/ROADMAP.md` §Phase 1 — output inventory, success criteria, review/approval boundary. [VERIFIED: repository source]
- `01-CONTEXT.md` — locked evidence, record, spike, governance, and reproduction decisions. [VERIFIED: repository source]
- `.planning/governance/evidence-policy.md`, `.planning/governance/approval-matrix.md`, `.planning/validation/phase-gates.yaml` — canonical policy/gate constraints for the plan. [VERIFIED: repository source]
- `CLAUDE.md` — enforced project constraints, no-production gate, and evidence separation. [VERIFIED: repository source]

### Secondary (MEDIUM confidence)

- https://git-scm.com/docs/git-rev-parse — revision and blob-object verification pattern. [CITED: https://git-scm.com/docs/git-rev-parse]
- https://json-schema.org/draft/2020-12/json-schema-core — `$schema`, dialect, meta-schema, and instance-validation semantics. [CITED: https://json-schema.org/draft/2020-12/json-schema-core]
- https://playwright.dev/docs/browser-contexts and https://playwright.dev/docs/browsers — isolated browser contexts and browser binaries. [CITED: https://playwright.dev/docs/browser-contexts; https://playwright.dev/docs/browsers]
- https://docs.github.com/en/rest/pulls/pulls and https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api — pull-request `head.sha` and collector rate-limit behavior. [CITED: https://docs.github.com/en/rest/pulls/pulls; https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api]
- https://pyyaml.org/wiki/PyYAMLDocumentation and https://python-jsonschema.readthedocs.io/en/stable/ — parser and validator package documentation. [CITED: https://pyyaml.org/wiki/PyYAMLDocumentation; https://python-jsonschema.readthedocs.io/en/stable/]

### Tertiary (LOW confidence)

- Documentation research was fetched through the WebFetch fallback because Context7 CLI/MCP was unavailable; the research confidence seam classified provider `webfetch` as LOW even when the URLs were official. These citations must be refreshed during execution if they influence a locked tooling decision. [VERIFIED: research tooling audit 2026-07-23]

## Metadata

**Confidence breakdown:**
- Standard stack: LOW — package/docs information came through the WebFetch fallback, the confidence seam classified it LOW, and all proposed packages are `SUS` until human verification. [VERIFIED: classify-confidence and package-legitimacy audits 2026-07-23]
- Architecture: HIGH — file locations, required outputs, gates, and locked decisions come from the canonical project context. [VERIFIED: .planning/ROADMAP.md; 01-CONTEXT.md; CLAUDE.md]
- Pitfalls: MEDIUM — project-specific pitfalls are grounded in locked policy; Git/JSON Schema/browser operational guidance is cited official documentation but retrieved through a LOW-confidence fallback. [VERIFIED: .planning/governance/evidence-policy.md; CITED: https://git-scm.com/docs/git-rev-parse]

**Research date:** 2026-07-23  
**Valid until:** Internal planning constraints: until changed. External tool/documentation findings: refresh at execution and within 7 days for package/browser decisions. [ASSUMED]
