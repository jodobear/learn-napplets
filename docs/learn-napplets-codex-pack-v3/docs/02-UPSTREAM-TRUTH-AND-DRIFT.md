# Upstream Truth, Provenance, and Drift Policy

## 1. Purpose

The ecosystem is experimental and changes quickly. Learn Napplets must remain accurate without presenting itself as the protocol.

## 2. Source classes

| Authority | Examples | Permitted use |
|---|---|---|
| **Current NIP draft** | living NIP-5D file | Web loading, sandbox, transport, sender identity, manifest, and security claims within scope |
| **Current NAP proposal** | one current domain file | Domain operations, messages, errors, and trust boundary |
| **Registry/governance** | projection, archetype, convention, templates | Taxonomy and process, subject to drift against higher-authority files |
| **Referenced protocol** | adopted NIP-5A portions | Only behavior actually adopted by the current source |
| **Implementation observation** | `napplet/web`, public packages, tests | Evidence and tested examples, never protocol authority |
| **Runtime observation** | Kehto or another runtime | One possible architecture and policy |
| **Pedagogy inspiration** | Learn FIPS | Teaching and interaction patterns |
| **Project decision** | accepted ADR | This repository's product/technical choices only |

Scope resolves conflicts as well as authority: NIP-5D controls the web projection, while an individual NAP controls its domain operations and semantics. Stale web-binding text inside a NAP/template does not override current NIP-5D; current NIP-5D does not define the domain's operation set.

## 3. Known high-risk drift to re-verify

Phase 0 must explicitly check:

1. current NIP-5D domain-object presence versus registry/projection `shell.supports()` text;
2. current NIP-5D manifest kinds/profile versus NIP-5A kind `35128` language elsewhere;
3. NAP-SHELL/handshake assumptions versus current NIP-5D bootstrap behavior;
4. the `(dTag, aggregateHash)` identity tuple when current manifest kinds may omit a `d` tag;
5. whether archetype and convention manifest tags are defined for the current NIP-5D profile;
6. NAP-INTENT handler identity/catalog assumptions under the current manifest model;
7. browser outbound-network behavior versus mediated-access claims;
8. package/conformance behavior that still enforces retired or private conventions.

These are research questions, not project-level resolutions.

## 4. Source registry

Store source metadata in:

```text
.planning/research/source-registry.yaml
```

Required fields:

```yaml
id:
title:
authority:
maturity:
repository:
path:
livingUrl:
immutableUrl:
ref:
commitSha:
contentSha256:
pullRequest:
observedAt:
lastCheckedAt:
scope:
notes:
```

For a pull-request ref, record the actual head commit SHA. Do not rely only on a mutable raw PR URL.

Do not vendor full upstream specifications. Metadata, short source-linked claims, and fixture excerpts are sufficient.

## 5. Claim inventory

Every load-bearing claim has a stable ID:

```yaml
id: claim.nip5d.shell-trusted
statement: "The current NIP-5D security model treats napplets as untrusted and the shell as trusted."
evidenceClass: current-nip-draft
maturity: draft
concepts:
  - concept.napplet
  - concept.shell
  - concept.trust-boundary
sources:
  - sourceId: nip-5d
    path: 5D.md
    section: Security Considerations
    excerptSha256: ...
lastVerified: 2026-07-23
affectedContent:
  - lesson.sandbox-boundary
affectedCode:
  - lab.threat-lens
```

Claims are concise original explanations, not copied specifications.

## 6. Compatibility matrix

Maintain:

```text
.planning/research/compatibility-matrix.yaml
```

It maps:

- source revision;
- package version/commit;
- runtime version/commit;
- supported domains;
- known drift;
- tested examples;
- conformance result.

This prevents a current lesson from combining wire text from one revision with SDK behavior from another.

## 7. Drift register

Each conflict includes:

```yaml
id:
topic:
claims:
  - sourceRef:
    statement:
impact:
  content: []
  code: []
  knowledge: []
decision:
status:
owner:
verifiedAt:
resolutionEvidence:
```

Valid statuses:

- `open`;
- `teaching-higher-authority-with-warning`;
- `blocked`;
- `resolved-upstream`;
- `legacy-retired`.

## 8. Evidence classes and public labels

| Evidence class | Public label |
|---|---|
| `conceptual-model` | CONCEPTUAL MODEL |
| `current-nip-draft` | CURRENT NIP DRAFT |
| `current-nap-proposal` | CURRENT NAP PROPOSAL |
| `registry-governance` | REGISTRY / GOVERNANCE |
| `implementation-observation` | IMPLEMENTATION OBSERVATION |
| `runtime-observation` | RUNTIME EXAMPLE |
| `project-decision` | LEARN NAPPLETS DECISION |
| `open-question` | OPEN QUESTION |
| `legacy-superseded` | LEGACY / SUPERSEDED |

Maturity is displayed separately: draft, implemented, active, deferred, superseded, disputed, or unknown.

## 9. Volatility

| Volatility | Examples | Rule |
|---|---|---|
| **High** | open PRs, issues, proposal status, living draft files | refresh in every phase that uses them |
| **Medium** | package APIs, runtime behavior, deployment tooling | refresh before code/tutorial changes |
| **Low** | conceptual models and historical context | periodic review |

An active branch is not evidence of intended future behavior unless connected to a PR, issue, or relevant source commit.

## 10. Citation placement

Load-bearing claims need nearby citations containing:

- source title;
- authority;
- section/path;
- immutable revision;
- last verified date;
- dispute indicator where relevant.

A generic sources footer is not enough.

## 11. Source refresh automation

The project should:

1. fetch source metadata;
2. detect changed paths/content digests;
3. map changes to claim, lesson, lab, and knowledge IDs;
4. create a report or maintenance issue;
5. never auto-rewrite explanatory prose or change classifications.

Automation detects change. Review determines meaning.

## 12. Network/source failure

When current sources cannot be reached:

- retain the last verified record;
- mark it stale;
- record the fetch failure;
- block new protocol conclusions;
- do not replace verification with model memory or old summaries.

## 13. Research completion standard

No protocol-sensitive lesson reaches final prose until:

- its source pack is complete;
- claims are inventoried;
- drift is classified;
- package/runtime compatibility is recorded;
- terminology matches current sources;
- examples validate or are visibly illustrative.
