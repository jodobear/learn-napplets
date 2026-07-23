# AGENTS.md — Learn Napplets

These are the durable operating rules for coding agents working in the **independent Learn Napplets repository**.

## 1. Mission

Build an accurate, interactive, accessible learning product that teaches:

- why napplets exist;
- the napplet frame of mind;
- the trusted host and untrusted application boundary;
- NIP-5D’s web projection;
- the NAP capability seam;
- current archetype and app-to-app convention models;
- exact-code distribution and identity;
- focused application design;
- runtime responsibilities;
- build, conformance, publication, and protocol contribution paths.

The same structured source must also form a precise map for LLMs.

## 2. Instruction precedence

When repository instructions conflict, use this order:

1. this `AGENTS.md`;
2. accepted ADRs and current research outputs under `.planning/`;
3. canonical project documents under `docs/`;
4. the currently authorized phase prompt;
5. templates and examples.

No project instruction overrides a current upstream protocol source. Record conflicts instead of choosing silently.

## 3. Independent-repository boundary

This repository is not `napplet/web`, `napplet/naps`, a NIP repository, a runtime repository, or Learn FIPS.

Treat upstream projects as read-only unless the user creates a separate explicit upstream-contribution task.

Do not:

- modify disposable upstream clones;
- open upstream PRs as a side effect of building the course;
- import unpublished source paths or private package internals;
- couple deployment to an upstream monorepo;
- present one SDK or runtime as the protocol definition.

Put disposable clones under an ignored path such as:

```text
.research/upstreams/
```

Record repository, path, ref, immutable commit SHA, file digest, retrieval time, and authority for every source used.

## 4. Canonical source hierarchy

For protocol-sensitive claims, use this priority order:

1. the current NIP-5D proposal text for web loading, sandbox, transport, sender identity, manifest profile, and security boundary;
2. the current individual NAP proposal/specification for one runtime capability domain;
3. the current NAP registry, web projection, archetype registry, convention files, governance files, and templates for taxonomy and process;
4. referenced NIPs for only the portions adopted by the current design;
5. `napplet/web` packages, tests, examples, docs, and conformance tooling as implementation evidence;
6. Kehto or another runtime as a non-authoritative implementation example;
7. Learn FIPS and other learning products as pedagogical inspiration only.

Read the current source. Do not answer protocol questions from memory. A NAP owns its domain semantics; NIP-5D owns the web projection. When a NAP file or template contains stale web-binding text that conflicts with the current NIP-5D file, preserve the domain contract but follow and cite NIP-5D for browser loading, discovery, transport, and identity.

If current upstream sources cannot be fetched, record a blocker and stop protocol conclusions. Cached knowledge is not a replacement for current verification.

## 5. Protocol fidelity

Never invent protocol surface.

Do not fabricate or silently assume:

- message types or fields;
- bootstrap handshakes;
- capability names;
- manifest kinds, tags, or artifact rules;
- sandbox tokens or CSP rules;
- capability-discovery behavior;
- version negotiation;
- app-to-app conventions;
- archetype tags;
- signing or encryption methods;
- runtime obligations.

A missing behavior is a research finding or protocol gap.

Every protocol-sensitive code path, wire example, or teaching assertion must cite a current source revision. Every package example must also record the package/runtime revision it was tested against.

## 6. Evidence class and maturity are separate

Do not use one `status` field to mean both “where this claim comes from” and “how mature the upstream work is.”

### Evidence classes

- `conceptual-model`
- `current-nip-draft`
- `current-nap-proposal`
- `registry-governance`
- `implementation-observation`
- `runtime-observation`
- `project-decision`
- `open-question`
- `legacy-superseded`

### Maturity values

- `draft`
- `active`
- `implemented`
- `deferred`
- `superseded`
- `disputed`
- `unknown`

Public labels should make both dimensions understandable. A current draft is the source this project follows for interoperability work, but it is not a finalized standard.

## 7. Drift handling

When sources disagree:

1. record both claims and exact revisions;
2. identify the authority and maturity of each source;
3. identify affected lessons, labs, code, and generated knowledge;
4. teach the higher-authority current source only when the hierarchy resolves the issue;
5. label unresolved behavior `OPEN QUESTION`;
6. never invent a compatibility compromise.

Active branches are leads, not authority. Deep-read a branch only when it is linked to an open PR, a current source change, or a material implementation decision.

## 8. Shell and runtime terminology

Teach these carefully:

- **Shell:** the NIP-5D web host that creates and communicates with napplet iframes.
- **Runtime:** the broader projection-neutral host concept used by the NAP ecosystem.
- In the web projection, the shell is the browser-facing host. A runtime may internally contain shell adapters, policy, dispatch, services, and external integrations, but that decomposition is implementation-specific.

Do not casually treat shell and runtime as either perfect synonyms or mandatory separate processes.

## 9. Runtime-role separation

The project may produce several builds with different authority.

### Public-site build

The public site may act as a **declared teaching host**. It may:

- create sandboxed lab napplet iframes;
- inject selected deterministic domains;
- authenticate source windows;
- record actual messages;
- implement selected manifest verification;
- run selected conformance checks.

It must declare which teaching-host profile it implements. It must not claim to be a complete conformant runtime merely because some labs work.

### Napplet builds

A Workbench, course, or lab build running as a napplet:

- is an untrusted guest;
- must not import host-only teaching-shell code;
- must not claim shell authority;
- must feature-gate optional domains;
- must not depend on direct storage, relay, signer, or device access unless the current protocol explicitly permits it;
- may show simulations;
- may ask the external runtime to open sibling napplets through the current canonical mechanism;
- must not describe privately nested frames as runtime composition.

Prefer separate compile-time entry points and dependency rules. Do not infer authority from iframe nesting, URL shape, `window.parent`, or unrelated browser APIs.

## 10. Teaching-host profiles

Use these declared profiles:

1. **Boundary harness:** current sandbox, injection, `postMessage`, source-window mapping, and envelope observation.
2. **Verified loader:** boundary harness plus current manifest/signature/blob/aggregate verification and exact-byte loading.
3. **Selected-domain host:** verified loader plus explicitly named NAP-domain services.
4. **Composition host:** selected-domain host plus the current role/handler/catalog mechanism.

A lesson or lab must display the profile it relies on. A profile may be renamed after Phase 0, but the distinction must remain.

## 11. Research-first gate

Do not scaffold the production course, write final protocol-sensitive prose, or implement a production host before Phases 0 and 1 pass.

Throwaway spikes belong under:

```text
.planning/spikes/
```

Every spike records hypothesis, source revisions, result, measurements, recommendation, and disposition.

## 12. Human and LLM parity

The same source records must generate:

- static HTML;
- page Markdown;
- glossary entries;
- diagram transcripts;
- structured knowledge JSON;
- source/status data;
- `llms.txt`;
- `llms-full.txt`.

No essential fact may exist only in an image, animation, hover state, canvas, or interactive branch.

Use stable concept IDs, explicit aliases, schema versions, and deprecation mappings. Use explicit actor names when authority matters.

## 13. Interaction and accessibility

Use animation only to show causality, sequence, authority, policy, identity change, composition, failure, or recovery.

Every significant animation requires:

- play/pause;
- previous/next;
- reset;
- keyboard control;
- reduced-motion behavior;
- text transcript.

Every real lab also requires a static explanation and deterministic replay.

## 14. Safety and determinism

Required lessons must not depend on:

- a real private key;
- a production signer;
- public relay availability;
- a wallet;
- device access;
- external uploads;
- learner accounts.

Use fixed fake keys, events, manifests, relays, timing, and outcomes. Compute real hashes when teaching hashing.

Any future live mode is separate, opt-in, and independently reviewed.

## 15. Engineering workflow

Before edits:

```bash
git status
git branch --show-current
git log --oneline -5
```

If the repository has no commits, initialize the documentation baseline first, then create the Phase 0 branch. Do not pretend a default branch exists when it does not.

Work on one descriptive branch per phase. Keep commits atomic and stage explicit paths.

At the end of each phase:

- update `.planning/STATUS.md`;
- update affected ADRs;
- refresh relevant source records;
- run the phase checks;
- commit the work;
- push/open a PR when remote access and credentials exist;
- otherwise leave a clean branch with a PR-ready report.

Never claim a source fetch, test, push, PR, publication, or deployment that did not occur.

## 16. Definition of done

A phase is complete only when:

- its required artifacts exist;
- its exit criteria pass;
- protocol claims have current sources;
- code and wire examples validate;
- interactive material has static equivalents;
- tests pass;
- unresolved drift and out-of-scope work are listed;
- the phase did not silently advance into the next phase.
