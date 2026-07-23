# Curriculum and Experience Specification

## 1. Teaching model

Learn Napplets is a course with instruments. It is not a marketing page with animations and not a prose mirror of upstream specifications.

Use one recurring scenario: **the journey of one note**.

```text
write → save → identify → request publish → authorize → sign → route
→ open → resolve handler → render
```

Each lesson reveals another layer of the same journey.

## 2. Four synchronized detail modes

### Story

Plain-language actor intent.

> The composer asks the shell to publish an unsigned note.

### System

Architecture or sequence view.

```text
Napplet → web boundary → policy → domain service → relays
```

### Wire

A current validated envelope, manifest fragment, or explicit illustrative fixture.

### Code

A current tested package/global example tied to a compatibility record.

Selecting one step highlights its equivalent in all four views.

## 3. Representation provenance

Every instrument is labeled as one of:

- **REAL NAPPLET / REAL BROWSER BOUNDARY**;
- **DETERMINISTIC HOST FIXTURE**;
- **CONCEPTUAL SIMULATION**;
- **IMPLEMENTATION OBSERVATION**.

Never let a visual simulation imply that a protocol operation actually occurred.

Every protocol-sensitive block also displays evidence class, maturity, source revision, and last verification date.

## 4. Course structure

### Chapter I — The shift

#### 1. A Nostr client, taken apart

Question:

> Why not build another complete Nostr client?

Instrument:

- Monolith Splitter.

Outcome:

- focused application logic separates from shared authority;
- the host mediates signing, storage, relays, uploads, and policy;
- compromise of one UI does not automatically grant all authority.

#### 2. The cast and mental model

Question:

> What are napplet, shell, runtime, projection, capability domain, convention, and archetype?

Instrument:

- Architecture Atlas;
- owns / does-not-own / communicates-with cards;
- analogy and “where it breaks” comparisons.

Required distinction:

- shell is the NIP-5D web host;
- runtime is the broader host concept;
- internal runtime layering is an implementation choice.

#### 3. Nostr underneath

Question:

> What minimum Nostr knowledge is required?

Instrument:

- optional event, relay, and Blossom journey.

Experienced Nostr developers may collapse this lesson.

### Chapter II — The boundary

#### 4. The sandbox boundary

Question:

> Who is trusted, what authority exists, and what is not guaranteed?

Instrument:

- Trust Map;
- Threat Lens;
- Who Owns What;
- Who Sees What.

Teach both guarantees and non-guarantees. Include the difference between current specification claims and observed browser behavior.

#### 5. One request across the boundary

Question:

> What happens when a napplet calls a domain operation?

Instrument:

- synchronized Story/System/Wire/Code sequence;
- actual message recorder in the teaching host.

#### 6. Capabilities, not ambient authority

Question:

> How does a napplet ask for functionality without receiving broad authority?

Instrument:

- capability tray;
- real feature-gating example;
- “choose the narrowest capability” exercise.

Every example uses a current selected domain proposal and displays its draft/maturity status.

#### 7. Identity and distribution

Question:

> How does the host know which exact code it is running?

Instrument:

- verified-loader journey;
- manifest/hash laboratory;
- one-byte mutation.

Do not teach unresolved `dTag` or manifest metadata behavior as settled.

### Chapter III — Composition

#### 8. Apps that cooperate

Question:

> How are role, handler selection, lifecycle, and payload meaning separated?

Instrument:

- Composition Lab with multiple viewers and user defaults.

Refresh current intent/archetype/convention sources immediately before implementation. If current sources conflict, teach the conflict and limit real behavior to the resolved subset.

#### 9. Designing a good napplet

Question:

> Where should one app end and another begin?

Instrument:

- Architecture Clinic;
- pattern gallery;
- anti-pattern review.

### Chapter IV — Build

#### 10. Anatomy of a napplet

Question:

> Which files and tools produce a real napplet?

Instrument:

- annotated project explorer tied to current public tooling or a clearly labeled minimal implementation.

#### 11. Build, test, and publish

Question:

> How does source become a verified runnable artifact?

Instrument:

- developer Workbench;
- conformance repair;
- manifest inspection;
- dry-run publication.

### Chapter V — Runtime and protocol

#### 12. Inside a runtime

Question:

> What must a host do, and what is only one implementation architecture?

Instrument:

- Runtime X-ray with labels:
  - current required behavior;
  - possible architecture;
  - host policy;
  - external adapter.

#### 13. Evolving the protocol

Question:

> Where does a missing behavior belong?

Instrument:

- contribution router;
- protocol design clinic;
- dated open-question map.

## 5. Standard lesson anatomy

Every lesson contains:

1. guiding question;
2. recurring note scenario;
3. thirty-second model;
4. interactive or inspectable instrument;
5. owns / does-not-own table;
6. source and protocol mapping;
7. implementation example;
8. failure or abuse case;
9. design exercise;
10. knowledge check;
11. evidence, maturity, and last-verified metadata;
12. next conceptual dependency.

## 6. Canonical diagrams

Use separate diagrams for separate questions.

### Trust map

Who is trusted and who owns authority?

### Execution stack

How does one request move through application, projection, policy, service, and external systems?

### Composition plane

How does the host resolve and open another focused application?

### Specification map

Which current upstream source owns which behavior?

Do not combine these into one misleading stack.

## 7. Core instruments

| Instrument | Purpose | Required implementation level |
|---|---|---|
| Monolith Splitter | separation of concerns | conceptual simulation |
| Architecture Atlas | ecosystem map | data-driven |
| Threat Lens | authority/visibility | data-driven plus source links |
| Envelope Journey | actual request flow | real boundary harness |
| Capability Lab | feature gating | real lab napplet and host toggle |
| Manifest Identity Lab | exact bytes and identity | verified-loader fixture |
| Composition Lab | handler/default resolution | composition-host fixture and real viewers |
| Boundary Game | ownership reasoning | deterministic exercise |
| Runtime X-ray | required versus possible internals | data-driven |
| Protocol Design Clinic | least authority and venue | scenario exercise |
| Conformance Lab | repair protocol/tooling violations | real validators where public |

## 8. Use of chat

Use chat as a synchronized actor transcript, not decoration.

```text
NAPPLET
Please publish this unsigned note.

TEACHING HOST
The selected domain is available. Policy permits the fixture operation.

DOMAIN SERVICE
Constructing the deterministic signed-event fixture and routing result.

RELAY FIXTURE
Accepted by three simulated relays.

TEACHING HOST
Returning the correlated result.
```

Selecting a message reveals actor, trust zone, exact object, source owner, and sequence step.

A generic AI tutor is outside v1.

## 9. Pattern gallery

Every pattern record includes:

- one user job;
- why it should be focused;
- current required/optional domains;
- archetype/role if current;
- what it intentionally does not own;
- graceful degradation;
- implementation links;
- evidence and maturity.

Initial patterns:

- viewer;
- composer;
- manager;
- lens;
- inspector;
- conversation pane;
- media desk;
- tool console;
- device controller;
- document explorer.

## 10. Learner paths

Use one content graph with suggested ordering.

- **New to Nostr:** Story/System first, Nostr primer enabled.
- **Nostr developer:** Wire/Code visible immediately, familiar comparisons.
- **Runtime developer:** boundary, loader, request flow, policy, conformance.
- **Protocol contributor:** specification map, drift, domain boundaries, design clinic.

## 11. Assessment design

Prefer reasoning tasks:

- choose the owner;
- select the narrowest current domain;
- identify an invented assumption;
- explain a failure;
- route a proposed change;
- repair a real example.

Avoid acronym-only recall.

## 12. Visual and motion character

The site should feel precise, instrument-like, composable, and explicit about uncertainty.

Motion is reserved for causality, sequencing, authority, identity change, composition, failure, and recovery.

## 13. Homepage

1. client separates into focused apps and host services;
2. thirty-second distinction;
3. mini capability lab;
4. trace one real request;
5. four architecture views;
6. learner paths;
7. napplet inspiration gallery;
8. build the sample;
9. contribution router;
10. current draft/source status.

## 14. Phase mapping

### Phase 4 vertical slice

- homepage;
- lessons 1, 4, 5, and 6;
- glossary/source essentials;
- Monolith Splitter, Threat Lens, Envelope Journey, Capability Lab;
- minimal real teaching host and the approved note-tool napplet, preferably the composer.

### Phase 5 expansion

- lessons 2, 3, and 7;
- Architecture Atlas;
- verified-loader/manifest lab;
- expanded Workbench and first conformance path.

Later phases add composition, build, runtime, and contribution chapters.

## 15. Portable course adaptation

A course-napplet build shares content and diagram data, but may use different navigation, persistence, source opening, and lab invocation.

Real sibling napplets are opened by the external host. Heavy host-only labs may be represented by static transcripts or opened separately.
