# Phase 1: Research and Truth Baseline - Context

**Gathered:** 2026-07-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 1 produces revision-pinned source records, claim/conflict/drift records, compatibility analysis, reproducible technical spikes, thirteen lesson research packets, and evidence-backed ADR recommendations. It does not accept ADRs or create production application/framework scaffolding.

</domain>

<decisions>
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

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Canonical GSD scope and gates
- `.planning/PROJECT.md` — product value, constraints, source authority, and no-production gate.
- `.planning/REQUIREMENTS.md` — Phase 1-owned evidence and governance requirements.
- `.planning/ROADMAP.md` §Phase 1 — phase goal, success criteria, outputs, and approval boundary.
- `.planning/STATE.md` — current status and blockers.
- `.planning/validation/phase-gates.yaml` — mandatory Phase 1 artifacts and evidence classes.
- `.planning/validation/required-artifacts.json` — canonical planning integrity contract.

### Governance and traceability
- `.planning/governance/evidence-policy.md` — required evidence fields, verification, freshness, and precedence.
- `.planning/governance/approval-matrix.md` — review/approval roles and exception rules.
- `.planning/governance/decision-register.md` — ADR queue, evidence minimums, owners, and revisit triggers.
- `.planning/traceability/requirement-source-map.yaml` — requirement-to-source-pack mapping.
- `.planning/traceability/phase-crosswalk.md` — GSD/source phase mapping.
- `.planning/traceability/pack-v3-import.md` — source-pack preservation and authority model.

### Preserved source-pack requirements
- `docs/learn-napplets-codex-pack-v3/AGENTS.md` — long-lived research, host/guest, and phase-authorization constraints.
- `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md` — source, claim, drift, and change-impact model.
- `docs/learn-napplets-codex-pack-v3/docs/04-RESEARCH-PLAN.md` — required research tracks, artifacts, report standard, and exit criteria.
- `docs/learn-napplets-codex-pack-v3/docs/06-TECHNICAL-ARCHITECTURE.md` — provisional architecture hypotheses requiring evidence.
- `docs/learn-napplets-codex-pack-v3/docs/08-PHASED-IMPLEMENTATION-PLAN.md` §Phase 0 — source phase outcome and gate.
- `docs/learn-napplets-codex-pack-v3/docs/09-QUALITY-SECURITY-ACCESSIBILITY.md` — spike, browser, security, accessibility, and quality expectations.
- `docs/learn-napplets-codex-pack-v3/docs/10-DECISIONS-AND-ADRS.md` — ADR topics and minimum ADR content.
- `docs/learn-napplets-codex-pack-v3/prompts/00-PHASE-0-RESEARCH.md` — authorized source-phase prompt.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/validate-planning.py`: baseline structural, traceability, archive-integrity, and premature-scaffold checks; extend rather than replace.
- `.planning/validation/phase-gates.yaml`: machine-readable Phase 1 gate seed.
- `.planning/traceability/pack-v3-file-manifest.json`: established digest-manifest pattern.
- `.planning/graphs/graph.json`: navigation index for requirements, phases, ADRs, and source docs; never evidence authority.

### Established Patterns
- Canonical live state lives under `.planning/`; preserved v3 pack remains immutable source/archive.
- Planning records are version-controlled; bulky clones/caches/generated dependencies are not.
- GSD uses discuss → research/plan → convergence → execute → verify, with human gates retained.

### Integration Points
- Phase planning writes plans under `.planning/phases/01-research-and-truth-baseline/`.
- Research outputs belong under `.planning/research/`; spike recipes/results under `.planning/spikes/`; schemas under `.planning/validation/` or a dedicated schema subtree chosen by planner.
- Planning validator and Graphify consume canonical records after creation.
- No application/runtime code exists. No production integration point is authorized in this phase.

</code_context>

<specifics>
## Specific Ideas

- Use Linux, Chromium, and Firefox for Phase 1 reproducibility coverage.
- Report five-run median plus full value range for nondeterministic measurements.
- User fills all approval roles for now, but signs high-risk role decisions separately.
- Canonical source pointers may be replaced when moved, but prior identity and history remain auditable.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 1-research-and-truth-baseline*
*Context gathered: 2026-07-23*
