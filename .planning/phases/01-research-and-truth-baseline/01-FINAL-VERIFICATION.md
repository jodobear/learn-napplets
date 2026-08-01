---
phase: 01-research-and-truth-baseline
verified: 2026-07-31T04:28:53Z
status: gaps_found
score: "3/5 roadmap success criteria verified; 4/6 direct requirement capabilities verified"
behavior_unverified: 0
overrides_applied: 0
next_action: "Create focused gap-closure work for public source-identity validation, historical source-registry binding of retained impact fragments, the stale collector fixture, and reduced-motion replay behavior; then independently re-run the affected tests. Preserve the authorized PRE118 and broader deferred boundaries."
next_command: "/gsd-plan-phase 1 --gaps"
re_verification:
  previous_status: gaps_found
  previous_score: "0/6 specified requirements verified"
  gaps_closed:
    - "Repository cache confinement now rejects external and symlink-mediated roots before transport or writes."
    - "Canonical recovery now refuses malformed transaction residue, and local drift synthesis uses observed-local with normative null."
    - "Refresh uses a process-lifetime advisory lock that releases after process death."
  gaps_remaining:
    - "Public static-site source identity validation accepts mutable GitHub branch URLs."
    - "All retained impact fragments still bind an obsolete source-registry digest, preventing consolidation after the truth refresh."
    - "The retained collector tracer test uses a now-forbidden temporary cache root and errors before its assertions."
    - "Reduced-motion replay still explicitly requests smooth scrolling."
  regressions:
    - "The retained full Phase 1 suite is red: 151 tests, 17 failures, and 8 errors."
requirements:
  EVID-01:
    status: failed
    reason: "The live static-site builder accepts a mutable /blob/main/ URL as an immutable source identity and does not cross-check sourceIdentity, commit, path, digest, or timestamp. The public source ledger is therefore not a reliable immutable-evidence boundary."
  EVID-02:
    status: verified
    reason: "Current drift, claim, source, compatibility, and site records retain separate authority/evidence/maturity/state/uncertainty labels and explicit blocked conflict routing; the full suite's drift tests pass."
  EVID-03:
    status: verified
    reason: "CMP-BASELINE-001 spans protocol, observed implementation, package, runtime, example/fixture, current-work, and conformance dimensions, explicitly blocks all unqualified dimensions, and does not accept an architecture. The stale collector tracer regression remains an active test-maintenance gap but does not make the current matrix misstate compatibility."
  EVID-04:
    status: failed
    reason: "The current source-registry digest is b53cd402... while all four impact fragments declare f32d576...; consolidation rejects them with IMP011/IMP016 before semantic validation or journaled publication. Mandatory-spike evidence is not currently revalidatable/reconsolidatable after the truth refresh."
  OPER-01:
    status: verified
    reason: "Focused and full-suite refresh tests pass for ambiguity reduction, idempotence, no silent claim rewrite, and advisory-lock release after process death."
  OPER-03:
    status: verified
    reason: "Governance, role, requirement, exit-evidence, and current gaps_found status records are present and direct governance tests pass. The historical PRE118 exact-plan-set binding remains an explicitly authorized deferred terminal-review mechanism, not evidence of a passed phase."
gaps:
  - truth: "Public source/status output can be relied on to identify only immutable evidence."
    status: failed
    reason: "CR-08 reproduced: tools/build-site.py accepts a mutable GitHub branch URL and labels the rendered record as an immutable source identity."
    artifacts:
      - path: tools/build-site.py
        issue: "SAFE_URL only accepts a generic github.com URL; it does not require a commit SHA, SHA-256 digest, RFC3339 retrieval time, or sourceIdentity-to-URL correspondence."
      - path: tests/site/test_static_site.py
        issue: "No negative tests reject branch/tag URLs, malformed source identity/digest/timestamp values, or mismatching URL identity fields."
    missing:
      - "Require immutable GitHub blob URLs with a 40–64 hex commit and validate sourceIdentity repository/commit/path against the URL."
      - "Validate 64-character lowercase SHA-256 digests and timezone-qualified retrieval timestamps, with negative regressions."
  - truth: "Mandatory spike evidence remains reproducibly validated and can be reconsolidated after a legitimate source refresh."
    status: failed
    reason: "All four retained impact fragments still declare historical source-registry digest f32d576e3..., while the current canonical registry is b53cd402...; current consolidation aborts with IMP011 and IMP016."
    artifacts:
      - path: tools/validate-research.py
        issue: "validate_impact_fragment() requires the current registry bytes even though completed-spike metadata has a Git-reachable historical-registry exception."
      - path: .planning/spikes/spk-c-boundary-harness/impact-fragment.yaml
        issue: "Declares the obsolete source-registry digest."
      - path: .planning/spikes/spk-d-verified-loader/impact-fragment.yaml
        issue: "Declares the obsolete source-registry digest."
      - path: .planning/spikes/spk-g-package-conformance/impact-fragment.yaml
        issue: "Declares the obsolete source-registry digest."
      - path: .planning/spikes/spk-h-browser-egress/impact-fragment.yaml
        issue: "Declares the obsolete source-registry digest."
    missing:
      - "Apply a safe Git-reachable historical-registry policy to retained impact-fragment provenance, or produce an explicitly authorized, coherently re-bound canonical generation."
      - "Restore passing consolidation interruption, semantic-failure, contention, dry-run, duplicate-fragment, and conflict regressions."
  - truth: "The retained source-acquisition/compatibility tracer is an executable regression for the exact cache policy."
    status: partial
    reason: "WR-04 reproduced: test_candidate_acquisition_tracer_blocks_incomplete_dimensions supplies a TemporaryDirectory cache root and errors at exact-root admission before its intended compatibility assertions."
    artifacts:
      - path: tests/phase1/test_evidence.py
        issue: "The test's temporary .research/upstreams fixture is incompatible with the repaired exact repository cache-root contract."
    missing:
      - "Use collector.CACHE_ROOT and clean only a unique child fixture; retain the strict production cache-root policy."
  - truth: "Optional replay controls fully honor reduced-motion preference."
    status: failed
    reason: "With prefers-reduced-motion: reduce active, clicking replay calls scrollIntoView({behavior: 'smooth', block: 'start'}). CSS cannot neutralize this explicit JavaScript option."
    artifacts:
      - path: site/assets/site.js
        issue: "Replay hard-codes smooth scrolling rather than selecting auto when reduced motion is requested."
      - path: tests/site/test_site_browser.py
        issue: "The test checks computed CSS scrollBehavior but does not observe the scrollIntoView options issued by replay."
    missing:
      - "Use behavior: 'auto' when matchMedia('(prefers-reduced-motion: reduce)').matches, and add a direct browser regression."
deferred:
  - truth: "Exact active-plan-set review binding and terminal-publication choreography pass."
    addressed_in: "Separately authorized future gap work; explicitly excluded from Plans 01-46 through 01-48."
    evidence: "PRE118 is reproduced because 01-REVIEWS.md binds the historical 45-plan set while 48 plans are active. deferred-items.md and ROADMAP.md explicitly retain this external review-byte-binding/terminal boundary."
  - truth: "SPK-G execution, scoped-package admission, and retained SPK-G bundle publication are repaired."
    addressed_in: "Future package-admission/SPK-G work."
    evidence: "Owner-authorized recovery defers CR-05 through CR-07/SPK-G; the static site neither executes nor admits a package."
  - truth: "Migration copy semantics are repaired."
    addressed_in: "Future migration work."
    evidence: "Owner-authorized recovery explicitly defers WR-02."
retained_boundaries:
  phase_2_transition: not_authorized
  production_scaffold: prohibited
  adr_acceptance: not_authorized
  package_admission: not_authorized
  runtime_or_guest_execution: not_authorized
  portable_target: not_authorized
  deployment_or_release: not_authorized
  live_service_wallet_or_signer: prohibited
---

# Phase 01: Research and Truth Baseline — Current Independent Verification

**Phase Goal:** Maintainers can rely on dated immutable-source evidence to choose safe teaching scope and architecture without presenting unsettled behavior as fact.

**Verified:** 2026-07-31T04:28:53Z
**Status:** `gaps_found`
**Re-verification:** Yes — after Plans 01-46, 01-47, and 01-48.

The preserved initial record remains untouched at `/workspace/projects/learn-napplets/.planning/phases/01-research-and-truth-baseline/01-VERIFICATION.md`. This report replaces the stale 2026-07-30 final verdict evidence, not that historical record.

## Final Verdict

**Phase goal is not achieved.** Plans 01-46 and 01-47 repaired the previously reproduced cache-confinement, transaction-recovery, observed-local, and refresh-lock defects, and Plan 01-48 produced a substantive static site. However, the public source ledger's immutable-identity validation is bypassable, and the truth refresh rendered the retained impact-fragment provenance unverifiable by the current consolidation path. These are active trust defects, not the owner-authorized SPK-G/migration or terminal-binding deferrals.

The static surface itself is substantive and locally functional, but it cannot compensate for a builder that will call mutable or malformed source input immutable. It also has an independent reduced-motion replay defect.

## Goal Achievement

### Roadmap Success Criteria

| # | Observable truth | Status | Independent evidence |
|---|---|---|---|
| 1 | A maintainer can trace every blocking protocol-sensitive claim to immutable revision, locator, digest, retrieval date, authority tier, evidence class, and maturity. | FAILED | All four newly admitted cached source blobs match their registry SHA-256 and the current records are complete, but `tools/build-site.py` accepts a mutable `/blob/main/` value as `immutableUrl`. The public ledger therefore has no enforceable immutable-identity boundary. |
| 2 | A maintainer can inspect volatile claims' conflicts, uncertainty, drift, impacts, and refresh trigger rather than treating disagreement as settled. | VERIFIED | `drift-register.yaml`, `claims.yaml`, `compatibility-matrix.yaml`, and the generated source page expose blocked/provisional distinctions; all full-suite `test_drift` tests passed. |
| 3 | A decision maker can review compatibility across selected protocol sources, packages, runtimes, examples, and current work before architecture is proposed. | VERIFIED | `CMP-BASELINE-001` carries all seven dimensions and `baselineEligibility: blocked`; repository observations, draft authority, package, runtime, fixture, current-work, and conformance gaps remain explicit. No architecture is accepted. |
| 4 | A decision maker can inspect reproducible measurements from every mandatory spike before recommendations are considered. | FAILED | Four retained impact fragments bind obsolete registry bytes. Current consolidation refuses them with `IMP011`/`IMP016`, so the recovery tests cannot reach interruption, semantic, contention, or reconciliation behavior. |
| 5 | The owner can review a first-lab recommendation or explicit blocker while confirming no production application scaffold exists. | VERIFIED | `CLM-UPSTREAM-BASELINE-001`, `OQ-*`, and `CMP-BASELINE-001` give explicit blockers; all ADRs remain proposed; no root `package.json`, workspace manifest, `src/`, `apps/`, or `packages/` production marker exists. |

**Roadmap score:** 3/5 success criteria verified.
**Direct requirement capability score:** 4/6; EVID-01 and EVID-04 are blocked by active defects.

### Plan 01-48 Must-Haves

| Must-have | Status | Evidence |
|---|---|---|
| Deterministic static learning path explains the host/guest boundary. | VERIFIED | Four Chromium browser checks passed for `/`, `/learn/`, `/architecture/`, and `/sources/`; no-JS mobile transcript/table/source-link coverage passed. |
| Human pages and machine knowledge derive from one structured source. | VERIFIED | `site/content/site.json` equals generated `site/dist/knowledge.json`; a fact mutation test proves propagation to HTML and JSON. |
| Protocol-sensitive statements visibly distinguish evidence/status dimensions. | FAILED | Current generated output shows those labels, but CR-08 permits a mutable/malformed source record to be rendered as immutable. |
| The shipped site has no framework, package manager, runtime, package, or external-service dependency. | VERIFIED | The stdlib build and browser checks pass; generated required requests remain loopback/local and no production package/runtime marker exists. |
| Keyboard, no-JS/static-equivalent, responsive, reduced-motion, reset/replay controls work. | FAILED | Keyboard/no-JS/responsive/reset checks pass, but direct Chromium observation under reduced motion captured replay requesting explicit `behavior: 'smooth'`. |

## Artifact, Wiring, and Data-Flow Verification

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `.planning/research/source-registry.yaml` | Immutable dated source records | PRESENT, SUBSTANTIVE | The four 2026-07-31 records contain revision, path, locator/blob, SHA-256, retrieval time, authority/evidence/maturity, uncertainty, impacts, and refresh trigger. Exact cache bytes all hash-match. |
| `.planning/research/claims.yaml`, `drift-register.yaml`, `compatibility-matrix.yaml` | Labeled claims, conflicts, and compatibility blockers | PRESENT, WIRED | Claims reference source IDs; drift keeps `observed-local` with `normative: null` where appropriate; compatibility explicitly blocks all unqualified dimensions. |
| `tools/acquire-sources.py`, `tools/canonical-recovery.py`, `tools/refresh-sources.py` | Safe ingress, generation recovery, and refresh | VERIFIED FOR REPAIRED PATHS | Focused ingress, malformed-transaction, observed-local, and process-death lock tests pass. |
| `tools/validate-research.py` plus four `impact-fragment.yaml` files | Revalidatable/reconsolidatable spike evidence | HOLLOW AT REFRESH BOUNDARY | Completed-spike metadata permits a Git-reachable historic registry, but impact fragments require current bytes and fail pre-publication. |
| `site/content/site.json` → `site/dist/**/*.html`, `site/dist/knowledge.json` | Single structured site truth source | VERIFIED | Reproducible 5-test static suite passes; current knowledge JSON exactly equals content JSON and generated pages include required status labels. |
| `tools/build-site.py` | Validated public source/status generator | STUB AT TRUST BOUNDARY | Rendering and escaping are substantive, but source identity validation is insufficient for the immutable-source promise. |
| `site/assets/site.js` | Optional, nonessential reset/replay enhancement | PARTIAL | It does not contain essential facts and reset works, but replay violates reduced-motion preference. |

### Key Links and Data Flow

| From | To | Status | Evidence |
|---|---|---|---|
| Source registry → claims/drift/compatibility | WIRED | Current IDs and source relations resolve; relevant full-suite drift/compatibility tests pass. |
| Retained impact fragments → current consolidation | NOT WIRED | `validate_impact_fragment()` rejects all historical fragment registry links against current bytes (`IMP011`, `IMP016`). |
| `site/content/site.json` → HTML | WIRED/FLOWING | Build renders facts, terms, blockers, source records, labels, and source links from IDs in one input. |
| `site/content/site.json` → `knowledge.json` | WIRED/FLOWING | Generator serializes the same content object; exact current JSON parity was checked. |
| Browser replay control → reduced-motion contract | NOT WIRED SAFELY | CSS uses reduced-motion overrides, but JavaScript forces `scrollIntoView({ behavior: 'smooth' })`. |

## Requirement Coverage

| Requirement | Status | Evidence and limits |
|---|---|---|
| EVID-01 | FAILED | Current four source records and cache digests are valid, but the public builder can convert a mutable/malformed source record into an apparent immutable source ledger entry (CR-08). |
| EVID-02 | VERIFIED | Current records preserve authority/evidence/maturity/state/uncertainty/impact/refresh separation; drift tests pass. |
| EVID-03 | VERIFIED | The compatibility matrix is complete as a blocked review baseline. WR-04 is an active regression-fixture repair, not a false compatibility conclusion in current data. |
| EVID-04 | FAILED | The current truth refresh invalidated all four retained impact-fragment registry bindings for the current consolidation validator; 11 full-suite failures result. |
| OPER-01 | VERIFIED | Refresh reduction, ambiguity, no-auto-rewrite, and process-lifetime locking tests pass. |
| OPER-03 | VERIFIED | Required governance, role, traceability, and current `gaps_found` state artifacts exist and direct governance tests pass. PRE118 remains an authorized deferred terminal-review-binding limitation. |

All six owning IDs are represented in all 48 PLAN frontmatters: EVID-01 (24 plans), EVID-02 (22), EVID-03 (26), EVID-04 (33), OPER-01 (20), and OPER-03 (19). No Phase 1 owning requirement is orphaned in `REQUIREMENTS.md`. Plan 01-48's A11Y-03 and KNOW-01 references are non-owning support, as its plan declares.

## Behavioral Checks

| Check | Result | Status |
|---|---|---|
| `tools/phase1-python --verify-toolchain` | Passed. | PASS |
| `tools/phase1-python tools/build-site.py --check` and static suite | Build check plus 5 static tests passed. | PASS |
| Direct Chromium browser suite | 4 tests passed: routes, keyboard order, local-only assets, no-JS mobile equivalents, reset/replay, and computed reduced-motion CSS. | PASS, INCOMPLETE |
| Direct CR-08 mutation | A copied content record with `https://github.com/.../blob/main/...` was accepted: `CR08_REPRODUCED=mutable_blob_main_accepted`. | FAIL |
| Direct WR-04 tracer | The named test errors at exact cache-root admission before its intended assertions. | FAIL |
| Direct reduced-motion replay observation | With reduced motion active, replay invoked `scrollIntoView({'behavior': 'smooth', 'block': 'start'})`. | FAIL |
| Focused recovery set | Ingress, malformed transaction, observed-local, lock, historical completed-spike, and composition tests passed; the two consolidation tests fail first on IMP011/IMP016. | FAIL |
| `validate-research.py validate --root .planning/research` | Refused with `PRE118` before canonical semantic validation. | DEFERRED LIMIT |
| `validate-research.py validate-reports --root .planning` | Passed. | PASS |
| Base `validate-planning.py` | Passed with 0 errors and 0 warnings. | PASS |
| Phase-complete validation with matched independent identity | Refused with `PRE118: review plan manifest is not the exact active plan set`. | DEFERRED LIMIT |
| Full Phase 1 suite | 151 tests: 17 failures, 8 errors. Seven terminal-validator errors and six validation-path failures stem from PRE118; eleven consolidation failures stem from IMP011/IMP016; one error is WR-04. | FAIL |

No declared or conventional `scripts/*/tests/probe-*.sh` probe was found for Plans 01-46 through 01-48.

## Findings Classification

| Finding | Classification | Impact |
|---|---|---|
| CR-08 mutable/malformed public immutable-source acceptance | BLOCKER | EVID-01 and the public evidence-label truth are not reliable. |
| Stale impact-fragment registry digest after Plan 01-47 refresh | BLOCKER | EVID-04 cannot be revalidated/reconsolidated; the atomic-publication path is not reached. |
| WR-04 stale temporary-root tracer | WARNING | The retained suite is red and the intended compatibility classification assertions are not exercised. |
| Forced smooth replay under reduced motion | BLOCKER | Active Plan 01-48 reduced-motion must-have is violated despite nonessential/static alternatives. |
| PRE118 exact historical 45-plan review binding | DEFERRED, NOT PASSED | Explicitly outside the recovery set; it prevents terminal validation but does not authorize a Phase 1 pass or transition. |

No unreferenced `TBD`, `FIXME`, or `XXX` debt marker was found in the active recovery tool, test, or site files. The only `placeholder` hit is the builder's legitimate unknown-template-token rejection, not a rendered placeholder.

## Human Verification After Gap Closure

After the blockers are repaired and automated checks are green, a reviewer should inspect the site at narrow and wide widths for editorial reading hierarchy, focus visibility, and whether the source/status labels remain understandable without treating draft or implementation observations as support. This is visual-quality judgment; it cannot make the current automated blockers acceptable.

## Retained Boundaries

- No production framework, package manager, trusted host, guest execution, package admission, live relay, wallet, signer, portable target, deployment, release, ADR acceptance, or Phase 2 transition is authorized.
- CR-05 through CR-07/SPK-G execution, WR-02 migration semantics, and PRE118 external review/terminal binding remain explicitly deferred; this report neither waives nor accepts them.
- The current site remains a local, dependency-free informational/learning surface. Its static boundary is not a runtime or a protocol/compatibility qualification.

## Gaps Summary

The recovery work materially improved the evidence tooling and produced a real accessible static site, but the phase cannot be closed. The two material trust failures are coupled to the truth-refresh handoff: the public renderer validates an insufficient source identity, and the refresh leaves historic spike-fragment provenance unusable by the current canonical consolidation path. Fix those without weakening cache confinement, historic evidence immutability, or journaled publication. Repair WR-04 against the strict cache policy and change replay to honor reduced motion. Re-run focused regressions, the site browser checks, canonical validation, and the full suite; preserve PRE118 and the other owner-authorized deferrals as non-passing boundaries.

---

_Verifier: Claude (independent Phase 1 verifier)_
