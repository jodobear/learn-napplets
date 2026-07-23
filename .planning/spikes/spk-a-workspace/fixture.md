# SPK-A Text-Only Candidate Fixture

`productionMarkersBlockedBeforePhase3`: `package.json`, `pnpm-workspace.yaml`, `src`, `apps`, `packages`.

These are comparison diagrams, not filesystem instructions. Do not create any displayed path.

| Criterion | Candidate A — public-site root + isolated content/host/guests | Candidate B — single mixed site tree | Candidate C — future workspace layout |
| --- | --- | --- | --- |
| public-site boundary | 1: public-site artifact is separately named | 0: site and host concerns are mixed | 1: public site is separately named |
| shared-content boundary | 1: common structured content is separately named | 0: content is implicit in site | 1: shared content is separately named |
| host-only isolation | 1: trusted host is separately named | 0: host privileges are mixed | 1: host is separately named |
| multiple guest entries | 1: guests are named as independent entries | 0: one mixed entry | 1: guest entries are separately named |
| deterministic testability | 1: each boundary has static fixture inputs | 0: one coupled fixture | 1: each boundary has fixture inputs |
| bundle isolation | 1: public, host, and guest outputs are distinct concepts | 0: one undifferentiated bundle | 1: separate output concepts |
| deployment compatibility | 1: public static deployment can stay independent | 0: deployment is coupled | 1: static site remains independently deployable |

## Candidate A

```text
public-site/        # static public delivery boundary
content-records/    # common structured source boundary
trusted-host/       # host-only authority boundary
guest-entry-one/    # independent guest boundary
guest-entry-two/    # independent guest boundary
```

## Candidate B

```text
single-site-and-host-and-guests/  # intentionally mixed comparison baseline
```

## Candidate C

```text
future-public-site/
future-shared-content/
future-trusted-host/
future-guest-entries/
```

Candidate A is the narrowest text model that makes all seven required boundaries explicit without implying a selected framework or package manager. Candidate C has equivalent conceptual separation but is a broader future-workspace hypothesis. Candidate B is retained as the negative control. All candidate names are fixture labels only; none may be materialized before the Phase 3 marker gate opens.
