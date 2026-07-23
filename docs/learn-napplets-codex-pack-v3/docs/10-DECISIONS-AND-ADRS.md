# Decisions and ADR Queue

## 1. Fixed product decisions

These are Learn Napplets product decisions, not protocol claims.

### D1 — Independent repository

The project is independently developed, governed, and deployed.

### D2 — Upstreams are read-only inputs

Normal project work does not modify upstream repositories.

### D3 — Public site is canonical

Stable lessons, citations, source pages, accessibility, and discovery live on the open web.

### D4 — Real lab napplets are required for v1

At least one composer and two interchangeable viewers demonstrate actual application behavior.

### D5 — Host and guest roles are separate

The public teaching host and portable napplet builds cannot share ambiguous authority.

### D6 — Teaching-host claims are profile-scoped

The project claims only the boundary, loader, domain, and composition behavior it has implemented and tested.

### D7 — Portable Workbench/course builds are feasibility-gated

They must not block the public-site v1 unless ADR 0007 explicitly says otherwise.

### D8 — One source model feeds humans and LLMs

No independently authored AI documentation.

### D9 — Deterministic fixtures are default

Required learning does not use real secrets, public relays, wallets, devices, or uploads.

### D10 — The site is non-authoritative

Current upstream sources remain protocol authority.

## 2. Required ADRs

### ADR 0001 — Repository/workspace

Select the smallest workspace supporting site, shared packages, host-only code, and multiple napplet builds.

### ADR 0002 — Site framework

Select based on static output, labs, content, entries, tests, accessibility, and maintenance.

### ADR 0003 — Deployment and publication

Define public-site hosting plus separate example-napplet publication.

### ADR 0004 — Content source model

Choose structured Markdown, typed records, or hybrid.

### ADR 0005 — Teaching-host architecture

Define profile scope, public package reuse, local adapters, and conformance claims.

### ADR 0006 — Diagram and motion system

Choose data-driven SVG and minimal state/motion dependencies.

### ADR 0007 — Portable napplet target

Decide `GO-V1`, `GO-LATER`, `WORKBENCH-ONLY`, or `NO-GO`.

### ADR 0008 — Protocol fixture strategy

Define source revision, schema validation, fake cryptography/external systems, and compatibility records.

### ADR 0009 — Code editing

Select variants, textarea, lightweight editor, or CodeMirror.

### ADR 0010 — Package versioning

Define pin/update policy for public `@napplet/*` dependencies.

### ADR 0011 — Source freshness

Define cadence, thresholds, stale behavior, and impact mapping.

### ADR 0012 — Content and example license

Define original content, diagram, and code licenses.

### ADR 0013 — Lab publication identity

Define manifest identity, release signing, versioning, and rollback for public labs.

### ADR 0014 — Public-site security policy

Define CSP, editable-code isolation, external links, and differences from current protocol requirements.

## 3. ADR standard

Every ADR includes:

- context;
- upstream facts versus local decisions;
- alternatives;
- evidence and measurements;
- host/guest implications;
- human/LLM implications;
- consequences and risks;
- revisit triggers.

## 4. Default hypotheses

These are research starting points, not decisions:

- a small pnpm-style monorepo is likely appropriate;
- a static-first component framework is likely appropriate;
- data-driven SVG is likely preferable to a heavy graph library;
- public site plus real lab napplets is the strongest v1;
- a focused Workbench napplet is likely more valuable initially than forcing the entire public site into one guest artifact;
- the full course is likely `GO-LATER`;
- the first production host profile should be boundary harness, followed by verified loader.

Codex must reject a hypothesis when evidence warrants it.
