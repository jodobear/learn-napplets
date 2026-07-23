# Content and Knowledge Model

## 1. Principle

Maintain one authoritative educational source model and render it into human and machine forms.

Do not maintain separate drifting versions of:

- the human course;
- an AI summary;
- the glossary;
- diagram prose;
- protocol status.

Generated artifacts are derived views. Structured lesson/claim/source records are the project content source; upstream specifications remain protocol authority.

## 2. Core entities

- **Source:** upstream/project source with immutable revision metadata.
- **Claim:** one concise statement with evidence class, maturity, and source locator.
- **Concept:** stable mental-model entity.
- **Relationship:** typed edge between concepts.
- **Lesson:** objectives, prerequisites, claims, labs, and assessments.
- **Lab:** deterministic or real interaction with states and transcript.
- **Pattern:** reusable application design shape.
- **Assessment:** reasoning task and expected concepts/facts.
- **Open question:** unresolved issue with impact and sources.
- **Compatibility record:** source/package/runtime/fixture relationship.

## 3. Stable IDs and versions

Examples:

```text
concept.napplet
concept.shell
concept.runtime
concept.web-projection
concept.capability-seam
concept.domain
concept.exact-build-identity
concept.manifest
concept.intent
concept.archetype
concept.convention
concept.teaching-host

lesson.why-napplets
lesson.sandbox-boundary
lesson.one-request
lesson.composition

lab.monolith-splitter
lab.envelope-journey
lab.capability-lab
lab.manifest-identity
```

Display labels may change; IDs do not.

When an ID must be retired:

- keep an alias/deprecation record;
- identify the replacement;
- preserve old URLs where practical;
- increment knowledge schema version only for structural breaking changes.

## 4. Evidence and maturity

Use separate fields:

```ts
type EvidenceClass =
  | 'conceptual-model'
  | 'current-nip-draft'
  | 'current-nap-proposal'
  | 'registry-governance'
  | 'implementation-observation'
  | 'runtime-observation'
  | 'project-decision'
  | 'open-question'
  | 'legacy-superseded';

type Maturity =
  | 'draft'
  | 'active'
  | 'implemented'
  | 'deferred'
  | 'superseded'
  | 'disputed'
  | 'unknown';
```

## 5. Source schema

```yaml
id: nip-5d
title: NIP-5D — Nostr Web Applets
authority: current-nip-draft
maturity: draft
repository: nostr-protocol/nips
path: 5D.md
livingUrl: ...
immutableUrl: ...
ref: refs/pull/2303/head
commitSha: ...
contentSha256: ...
observedAt: 2026-07-23T00:00:00Z
lastCheckedAt: 2026-07-23T00:00:00Z
scope:
  - web projection
  - sandbox
  - transport
```

## 6. Claim schema

```yaml
id: claim.nip5d.shell-trusted
statement: "The current NIP-5D security model treats napplets as untrusted and the shell as trusted."
evidenceClass: current-nip-draft
maturity: draft
concepts:
  - concept.napplet
  - concept.shell
sources:
  - sourceId: nip-5d
    path: 5D.md
    section: Security Considerations
    excerptSha256: ...
affectedContent:
  - lesson.sandbox-boundary
affectedCode:
  - lab.threat-lens
lastVerified: 2026-07-23
```

## 7. Concept schema

```yaml
id: concept.napplet
label: Napplet
aliases:
  - Nostr web applet
oneSentence: "A focused Nostr application that runs with mediated authority."
definition: ...
owns:
  - user interface
  - focused application logic
doesNotOwn:
  - signing keys
  - shell-wide storage
  - relay pool
trustZone: untrusted
layer: application
oftenConfusedWith:
  - concept.iframe-microfrontend
whereAnalogyBreaks:
  - ...
related:
  - concept.shell
  - concept.web-projection
evidenceClass: current-nip-draft
maturity: draft
sourceRefs:
  - nip-5d
lastVerified: 2026-07-23
```

## 8. Lesson schema

```yaml
id: lesson.one-request
slug: one-request
title: One request across the boundary
chapter: boundary
order: 5
summary: ...
audiences:
  - new-to-nostr
  - nostr-developer
  - runtime-developer
prerequisites:
  - lesson.sandbox-boundary
learningObjectives:
  - objective.trace-request
concepts:
  - concept.web-projection
  - concept.capability-seam
claims:
  - claim.nip5d.domain-action-envelope
labs:
  - lab.envelope-journey
assessments:
  - assessment.trace-publish
sourceRefs:
  - nip-5d
lastVerified: 2026-07-23
```

## 9. Relationship vocabulary

Keep the graph small:

- `isA`;
- `owns`;
- `doesNotOwn`;
- `mediates`;
- `provides`;
- `requests`;
- `mapsTo`;
- `runsInside`;
- `identifies`;
- `composes`;
- `opensByRole`;
- `definedBy`;
- `implementedBy`;
- `confusedWith`;
- `dependsOn`;
- `supersedes`.

Example:

```yaml
- subject: concept.shell
  predicate: mediates
  object: concept.signing

- subject: concept.web-projection
  predicate: mapsTo
  object: concept.postmessage
```

## 10. Diagram model

Every diagram record includes:

- question answered;
- nodes and edges;
- deterministic steps;
- narration;
- transcript;
- accessible table;
- source refs;
- evidence/maturity;
- reduced-motion behavior.

No essential meaning may exist only in coordinates or color.

## 11. Lab model

```yaml
id: lab.envelope-journey
title: Envelope Journey
lesson: lesson.one-request
implementation: real-boundary-harness
hostProfile: boundary-harness
objective: "Trace one request and result."
states:
  - id: request
    narration: ...
  - id: source-authentication
    narration: ...
  - id: policy
    narration: ...
  - id: service
    narration: ...
  - id: result
    narration: ...
failureModes:
  - unknown-source
  - missing-domain
  - invalid-payload
sourceRefs:
  - nip-5d
transcript: ...
staticFallback: ...
```

## 12. Human outputs

Generate:

- lesson HTML;
- lesson Markdown;
- glossary;
- architecture atlas;
- pattern gallery;
- source/drift/status pages;
- printable lessons;
- static transcripts.

## 13. Machine outputs

Generate:

```text
/llms.txt
/llms-full.txt
/knowledge/v1/index.json
/knowledge/v1/concepts.json
/knowledge/v1/relationships.json
/knowledge/v1/claims.json
/knowledge/v1/lessons.json
/knowledge/v1/labs.json
/knowledge/v1/sources.json
/knowledge/v1/status.json
/knowledge/v1/open-questions.json
/knowledge/v1/compatibility.json
/<route>.md
```

Each JSON file contains:

```json
{
  "schemaVersion": "1.0.0",
  "generatedAt": "...",
  "sourceBaseline": "baseline-..."
}
```

Compute `sourceBaseline` deterministically from the canonicalized source IDs, commit SHAs, and content digests used for the build. This allows humans and tools to tell whether two generated artifacts describe the same upstream snapshot.

Treat `llms.txt` as a proposed convention, not a formal protocol requirement.

## 14. `llms.txt`

Keep it concise:

- product definition;
- canonical course entry points;
- core concept list;
- source/status page;
- machine endpoint list;
- experimental-status warning.

## 15. `llms-full.txt`

Include:

- complete glossary;
- lesson summaries;
- ownership tables;
- architecture transcripts;
- current protocol versus implementation distinctions;
- source baseline;
- open-question summaries.

Do not reproduce full upstream specifications.

## 16. LLM writing rules

- define terms before use;
- list aliases explicitly;
- use precise actor names;
- distinguish shell, runtime concept, runtime internals, service, and external system;
- distinguish capability from transport;
- distinguish archetype from payload convention;
- state evidence and maturity near claims;
- include source IDs;
- state analogy limitations;
- explain negative boundaries;
- avoid ambiguous pronouns when several actors are present.

## 17. Evaluation set

Create fixed questions covering:

- definition;
- ownership;
- trust;
- request flow;
- capability selection;
- composition;
- distribution;
- protocol contribution;
- implementation drift;
- open-question recognition.

Example:

```json
{
  "question": "Does a napplet receive the user's signing key?",
  "expectedConcepts": [
    "concept.napplet",
    "concept.shell",
    "concept.signing"
  ],
  "expectedFacts": [
    "The trusted host retains signing authority.",
    "The napplet sends an application-level request through a capability."
  ],
  "requiredSourceRefs": ["nip-5d"],
  "forbiddenMisconceptions": [
    "The SDK gives the napplet a private key."
  ]
}
```

## 18. Validation

Fail CI when:

- a concept/claim/source ID is unresolved;
- a claim lacks evidence or source;
- authority and maturity are conflated;
- a diagram lacks transcript/table data;
- a lab lacks static fallback;
- a source revision/digest is absent;
- a legacy alias lacks mapping;
- an open question is rendered as settled;
- a lesson lacks Markdown output;
- human and machine titles diverge;
- a code example fails to compile;
- a fixture revision conflicts with its compatibility record.

## 19. Freshness

Every volatile entity includes source ref, last verified date, maturity, and affected IDs.

Display a warning when current-status material exceeds the configured freshness threshold.
