# Codex Master Prompt — Build Learn Napplets

You are building **Learn Napplets**, an independent learning product and repository.

Read and obey `AGENTS.md`. Use accepted ADRs and current `.planning/` research as the operational source for project decisions. Use the documents under `docs/` as the product contract.

## Mission

Create a static-first, interactive course that enables people and LLMs to understand the napplet mental model, protocol boundaries, ecosystem, development workflow, runtime responsibilities, and contribution seams accurately.

The project serves:

1. developers new to Nostr;
2. existing Nostr developers;
3. general application/web developers;
4. runtime implementers;
5. protocol contributors;
6. coding agents and LLMs.

## Independent-project boundary

Treat NIP repositories, `napplet/naps`, `napplet/web`, runtime repositories, and Learn FIPS as read-only upstream sources. Consume only suitable public released APIs. Do not modify upstreams unless the user opens a separate explicit contribution task.

## Product outputs

The repository may build:

1. a canonical public learning website and declared teaching host;
2. focused real lab napplets;
3. an optional Workbench napplet;
4. an optional course napplet compatible with the current verified napplet artifact contract.

The public host and napplet guest roles are separate. Guest builds must never import host-only code or impersonate the runtime.

## v1 minimum

- complete thirteen-lesson course;
- public static-first site;
- declared teaching-host profiles;
- at least three real lab napplets: one composer and two interchangeable viewers;
- architecture, capability, identity, composition, and conformance labs;
- source/status and drift pages;
- page Markdown, versioned knowledge JSON, `llms.txt`, and `llms-full.txt`.

A Workbench or full-course napplet is delivered only if the accepted ADR approves it.

## Research-first rule

Do not build the production site before Phase 0 and Phase 1 pass.

Phase 0 must establish:

- current protocol and taxonomy;
- source revisions and claim inventory;
- explicit drift and open questions;
- package/runtime compatibility matrix;
- browser security/egress findings;
- teaching-host feasibility and profile;
- delivery-mode recommendation;
- workspace, framework, content, deployment, and motion ADR evidence.

Never invent protocol behavior to unblock implementation.

## Product principles

- Reuse one scenario: the journey of one note.
- Begin with authority and boundaries, not package installation.
- Support Story, System, Wire, and Code views.
- Use real napplets when the lesson depends on real napplet mechanics.
- Use ordinary web components when packaging them as napplets adds no teaching value.
- Keep essential lessons readable without JavaScript.
- Use deterministic fixtures.
- distinguish current NIP draft, NAP proposal, implementation observation, project decision, and open question.
- Generate human and LLM outputs from one source model.
- Make animation inspectable, controllable, and accessible.

## Curriculum

1. A Nostr client, taken apart
2. The cast and mental model
3. Nostr underneath
4. The sandbox boundary
5. One request across the boundary
6. Capabilities, not ambient authority
7. Identity and distribution
8. Composition
9. Designing a good napplet
10. Anatomy of a napplet
11. Build, test, and publish
12. Inside a runtime
13. Evolving the protocol

## Protocol fidelity

Use current upstream sources. Do not invent handshakes, capabilities, messages, manifest fields, artifact rules, sandbox behavior, archetype metadata, conventions, signing methods, or runtime obligations.

Every protocol-sensitive claim needs a current source. Every package/runtime example needs a tested revision. Current upstream drift must remain visible.

## Phase order

Execute only the phase explicitly authorized by the user:

0. Research and Truth Baseline
1. Product and Content Contract
2. Independent Repository Foundation
3. Visual and Content Primitives
4. Real End-to-End Vertical Slice
5. Core Course and Workbench Expansion
6. Composition, Patterns, and Application Design
7. Build, Runtime, and Protocol Contribution
8. Optional Portable Napplet Target
9. Knowledge and LLM Hardening
10. Quality, Launch, and Maintenance

Do not silently continue into the next phase.

## Required behavior per phase

1. orient in Git;
2. read current planning artifacts;
3. refresh volatile upstream sources used by the phase;
4. state the phase plan and exit gate;
5. implement only that phase;
6. add tests and content checks;
7. update sources, ADRs, compatibility records, and status;
8. report unresolved drift;
9. commit atomically;
10. produce a PR or PR-ready report.

## First action

Execute only `prompts/00-PHASE-0-RESEARCH.md`.

Do not scaffold the production application during the first run.
