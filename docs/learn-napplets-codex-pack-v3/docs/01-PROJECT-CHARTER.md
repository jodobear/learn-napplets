# Project Charter

## 1. Product

**Learn Napplets** is an independent interactive learning product for the napplet ecosystem.

It is:

- a progressive course;
- an architecture explorer;
- a deterministic browser laboratory;
- a collection of real example napplets;
- a developer onboarding path;
- a runtime and protocol contribution guide;
- a structured knowledge source for LLMs.

It is not a canonical specification, a complete Nostr course, or a package API reference.

## 2. Core proposition

> Build one focused part of a Nostr client. Let the trusted host handle the dangerous and repetitive parts.

Suggested public headline:

> Build a Nostr app without becoming a Nostr client.

## 3. Questions the product answers

In order:

1. Why do napplets exist?
2. What is a napplet?
3. What belongs to the napplet, shell, runtime, service, relay, and Blossom layers?
4. What crosses the web boundary?
5. How does the host mediate authority?
6. How is exact application code identified, distributed, and verified?
7. How do focused applications cooperate?
8. How does a developer build, test, and publish one?
9. What must a runtime implement?
10. Where does a missing feature or protocol change belong?

## 4. Audiences

### New to Nostr

Needs only the Nostr concepts required by later lessons:

- keys;
- signed events;
- kinds and tags;
- relays and filters;
- NIPs;
- Blossom.

No unexplained kind numbers or acronyms.

### Existing Nostr developer

Needs comparison with conventional Nostr clients, NIP-07-style authority, relay pools, routing, NIP-51 mutations, uploads, storage, and signing.

### General application/web developer

Needs comparisons with operating-system processes, browser sandboxes, extensions, microfrontends, mini-apps, and capability security. Every analogy states where it breaks.

### Runtime implementer

Needs loader and verification behavior, source-window mapping, sessions, policy, dispatch, service adapters, projection boundaries, and conformance.

### Protocol contributor

Needs current taxonomy, boundary tests, proposal venues, implementation evidence, lifecycle/error design, and anti-patterns.

### LLM or coding agent

Needs stable terms, aliases, explicit ownership, typed relationships, dated sources, maturity labels, and text equivalents for every visual.

## 5. Terminology principle

The course must distinguish:

- **shell:** the NIP-5D web host;
- **runtime:** the broader projection-neutral host concept;
- **runtime internals:** one implementation's policy, dispatch, services, and adapters.

It must also keep capability, projection, archetype, and app-to-app convention as separate axes. Phase 0 resolves the current exact terminology before final content is written.

## 6. Learning outcomes

A learner completing v1 can:

- explain why a napplet is not merely an iframe microfrontend;
- identify trusted and untrusted actors;
- distinguish web projection from capability contracts;
- trace one actual request and result;
- select the narrowest appropriate domain;
- degrade gracefully when a domain is absent;
- explain exact-build identity and its update implications;
- explain runtime-mediated application selection;
- scope a focused napplet;
- build and test a simple example;
- classify a proposed change as protocol, SDK, runtime, content, or application work.

## 7. Product principles

### One recurring scenario

Use the **journey of one note**:

```text
open composer → write → save → identify → request publish
→ policy → sign → route → open → resolve viewer → render
```

### Show, manipulate, inspect

For each major concept:

1. show the system;
2. let the learner change it;
3. let the learner break it;
4. expose the state and wire;
5. connect it to current sources;
6. apply it in a design exercise.

### Real napplets where educational

Use an actual napplet when the lesson depends on:

- sandboxing;
- injected domains;
- `postMessage`;
- source-window identity;
- feature gating;
- exact packaging;
- runtime-mediated composition;
- conformance.

Use ordinary web components for navigation, glossary, static diagrams, and other material where a napplet adds no explanatory value.

### Honest status

Every protocol-sensitive explanation shows:

- evidence class;
- upstream maturity;
- exact source revision;
- last verification date;
- known drift.

## 8. Delivery cut lines

### Content MVP

- homepage;
- why napplets;
- sandbox boundary;
- one request;
- capabilities;
- glossary and source/status pages;
- minimal real teaching host;
- one real note-tool napplet, preferably the composer when its selected current domain is usable.

### Interactive MVP

- verified loader or explicitly limited boundary profile;
- envelope inspector;
- capability toggles;
- deterministic services;
- first in-browser conformance path.

### v1 minimum

- all thirteen lessons;
- at least three real lab napplets: one composer and two viewers;
- architecture, capability, identity, composition, and conformance labs;
- declared teaching-host profiles;
- source/drift pages;
- human and machine content outputs.

### Post-v1 candidates

- portable Workbench napplet;
- full-course napplet;
- live Nostr mode;
- advanced device/value/media labs;
- generalized AI tutor.

## 9. Non-goals

- replacing upstream specifications;
- teaching all of Nostr;
- documenting every package export;
- requiring public relays for lesson completion;
- exposing real signing keys;
- building a production wallet or signer;
- presenting one runtime as mandated architecture;
- turning every component into a napplet;
- hiding drift;
- allowing an optional course napplet to block the public-site v1.

## 10. Success criteria

### Human

A learner can draw the trust boundary, trace one request, explain why the key stays in the host, select an appropriate capability, and route a proposed change.

### Developer

A developer can run, modify, test, and understand the example napplets without relying on undocumented host behavior.

### LLM

Using only generated project artifacts, an LLM can answer a fixed evaluation set about definitions, ownership, request flow, composition, protocol versus implementation, and current status while returning the relevant concept and source IDs.

## 11. Relationship to upstream projects

The project may:

- link to and verify upstream sources;
- consume suitable released `@napplet/*` packages;
- use public conformance APIs;
- publish example napplets;
- identify protocol gaps.

It does not become the authority over those projects.
