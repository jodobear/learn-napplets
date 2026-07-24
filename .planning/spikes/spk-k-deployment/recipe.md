# SPK-K — Local artifact and optional external-probe recipe

SPK-K is a disposable, **non-production** deployment/publication experiment.
It does not create a product site, teaching host, guest napplet, framework
scaffold, account, credential, remote configuration, preview URL, published
artifact, or production release.

## Research question

Can the project create separately identifiable local static public-site, lab
artifact, and optional portable-output fixtures while maintaining a clear,
auditable boundary between local evidence and an external deployment or
publication claim?

The preserved source-pack plan asks to test independent public-site deployment,
lab napplet build/publication, and optional course napplet output. This spike
uses that as archived planning context only. Current project evidence remains
blocked for runtime, package, host, and portable-target behavior; local output
therefore cannot establish those external or upstream facts.

## Local-only artifact plan

Task 3 may assemble only the following local artifacts below
`.planning/spikes/spk-k-deployment/.experiment/local-artifacts/`:

| Artifact | Identity and required digest | Bounded purpose | Preview and isolation criterion | Rollback criterion |
| --- | --- | --- | --- | --- |
| `public-site-static` | directory manifest, sorted file list, byte count, and SHA-256 | Static source-status-rich lesson placeholder; no live domain or host assertion | Serve only on loopback for local inspection; contains no external URL, credential, network request, or provider configuration | Delete its local artifact directory and verify the parent contains no artifact files |
| `lab-artifact-placeholder` | directory manifest, sorted file list, byte count, and SHA-256 | Explicitly blocked placeholder for a future trusted teaching-host lab; no guest runtime, capability, or authority | Inspect as static text only; it must declare that no lab is deployed or previewed | Delete its local artifact directory and verify no host/guest output remains |
| `portable-output-placeholder` | directory manifest, sorted file list, byte count, and SHA-256 | Explicitly conditional placeholder for an optional course/portable artifact; no portability claim | Inspect as static text only; it must state that ADR-0007 remains separate and unresolved | Delete its local artifact directory and verify no course/portable output remains |

The identity record for each artifact must name its fixture input, deterministic
file list, byte count, SHA-256, local preview status, isolation result, and
rollback result. A local preview is not hosting, publication, or deployment.

## Permitted local commands

Before Task 2, the only executable command is the contract validation command:

```text
tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-k-deployment --contract
```

After Task 2, whether its selection is `local-only` or `sandbox-probe`, Task 3
may perform the local-only assembly described in `fixture.md`, calculate SHA-256
artifact identities, inspect static content without a listener, and remove those
local artifacts as the declared rollback check. The exact local commands are:

```text
tools/phase1-python .planning/spikes/spk-k-deployment/runner.py --fixture .planning/spikes/spk-k-deployment/fixture.md --out .planning/spikes/spk-k-deployment/.experiment/local-artifacts
tools/phase1-python .planning/spikes/spk-k-deployment/runner.py --fixture .planning/spikes/spk-k-deployment/fixture.md --out .planning/spikes/spk-k-deployment/.experiment/local-artifacts --rollback
```

Every local command must use `tools/phase1-python`; all generated files must
remain below `.planning/spikes/spk-k-deployment/.experiment/`. The runner does
not open a listener or make a network request.

No package installation, remote configuration, account lookup, credential
access, provider CLI command, external probe, publication, or deployment command
is an executable command in this recipe.

## External-probe gate

`metadata.yaml` starts with `externalProbeAuthorization.status:
not-authorized`. That state permits no external action and requires the
following deterministic blocked result:

```text
SPK-K-BLOCKED-EXTERNAL-AUTHORIZATION-MISSING
```

Task 2 has exactly two choices:

1. **`local-only`** — retain local artifact evidence and record external
   deployment/publication as a scoped blocker. No target is named, no credential
   is inspected, and no external command is added or run.
2. **`sandbox-probe`** — only after an explicit human authorization names the
   target may metadata contain an external command. The target must be classified
   as `disposable-sandbox`, not production, not shared staging, and not an
   unspecified provider environment.

A `sandbox-probe` authorization is incomplete and must remain blocked unless
metadata records all of the following before any command is eligible:

| Required authorization field | Required value or control |
| --- | --- |
| Named target | A human-provided unique sandbox name; do not invent one |
| Target classification | `disposable-sandbox` |
| Exact command | The human-approved write command, including its named target; no variable or default target |
| Cleanup procedure | Concrete removal/verification procedure for the named sandbox artifact/configuration |
| Retention period | Human-approved finite retention period or immediate cleanup |
| Owner | Named accountable owner or role supplied with the authorization |
| Security sign-off | Dated security reviewer authorization for this sandbox write |
| Release sign-off | Dated release owner authorization for this sandbox write; not release acceptance |
| Credential handling | Credentials stay outside version control and command output; never echo, log, or commit them |
| Result-digest policy | SHA-256 of the exact local artifact and redacted result record; never digest or store credentials |

A sandbox probe remains a non-production observation. It cannot accept ADR-0003,
claim public release, or authorize later deployment targets.

## Outcomes and ADR impact

- **Local pass:** all three local fixture artifacts are deterministic,
  digest-pinned, locally previewed/inspected as declared, isolated beneath
  SPK-K, and deleted by the local rollback check. This is local assembly
  evidence only.
- **Local failure:** retain the failed identity or command result; make no
  deployment or portability recommendation.
- **External authorization blocked:** preserve the deterministic blocked result,
  map it to `EVID-04`, `ADR-0003`, Phase 01, and later delivery/release work.
- **Authorized sandbox observation:** record target, exact command, cleanup,
  retention, owner, dated security/release sign-offs, redacted credential
  handling, and result-digest policy. Label it as disposable-sandbox observation,
  never as a production deployment or publication.

SPK-K can inform only a proposed ADR-0003 recommendation. The approval matrix
still requires technical responsibility, product approval, and consultation with
security and release roles for repository/framework/deployment ADRs.
