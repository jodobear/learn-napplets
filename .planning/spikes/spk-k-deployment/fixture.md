# SPK-K local artifact fixture

## Fixture status

**Status:** planned local-only fixture.

This fixture intentionally contains no source application, host implementation,
napplet, package, build framework, provider configuration, account identifier,
credential, remote URL, or deployment command. It defines the minimum static
payloads that Task 3 may assemble locally after Task 2 records its decision.

## Source and package baseline

| Baseline | Classification | Bound used by this fixture |
| --- | --- | --- |
| `SRC-POLICY-001` — preserved source-pack deployment planning | archived planning context, not current upstream proof | Defines the three assessment categories: independent public site, lab artifact, and optional course output |
| `SRC-POLICY-002` — project evidence policy | project policy | Requires immutable identity, digest, scoped uncertainty, and human approval boundaries |
| `CMP-BASELINE-001` | blocked compatibility baseline | No runtime, package, export, domain, or portable-target implementation is selected or inferred |
| `TSCOPE-001` | blocked teaching scope | The safe fallback is static public content; no real lab operation or teaching-host profile is claimed |

No package is selected or installed. A package/framework baseline would require
separate immutable evidence and approval; SPK-K does not infer one from local
file creation.

## Declared local payloads

Task 3 may create exactly these bounded static outputs beneath
`.planning/spikes/spk-k-deployment/.experiment/local-artifacts/`:

1. `public-site-static/index.html` — static text stating that it is a local
   SPK-K fixture, containing no script, external asset, form, telemetry,
   credential, provider setting, host assertion, or runtime claim.
2. `lab-artifact-placeholder/README.md` — static text stating that a teaching
   host/lab artifact is blocked and has not been built, hosted, previewed, or
   published.
3. `portable-output-placeholder/README.md` — static text stating that optional
   portability remains conditional on separate ADR-0007 evidence and has not
   been packaged, hosted, or published.
4. One `artifact-manifest.json` per output, with artifact ID, sorted relative
   file list, byte count, SHA-256, fixture input digest, local preview status,
   isolation result, and rollback result.

The payload content is deliberately minimal because the local measurement is
artifact identity and separation, not framework selection or production-site
functionality.

## Required local checks

For each declared artifact, Task 3 must record:

- SHA-256 of each payload and its manifest;
- sorted file list and aggregate byte count;
- that the output path remains beneath the SPK-K `.experiment/` directory;
- `public-site-static` loopback-only local preview result, with no claim of
  public reachability;
- static inspection result for the two placeholders;
- rollback result after removing the local artifact directories; and
- deterministic replay result from this fixture and the assembled manifests.

A local output is not an external publication, preview deployment, or artifact
release. It may not supply a provider URL, target, account, credential, or
external result.

## External-probe fixture boundary

The external-probe target is intentionally absent. Under the default
`not-authorized` state, the expected external result is
`SPK-K-BLOCKED-EXTERNAL-AUTHORIZATION-MISSING`.

If and only if Task 2 chooses `sandbox-probe`, the human authorization must add
the named disposable-sandbox target and the exact write command to metadata
before Task 3 may act. The authorization must also supply cleanup, retention,
owner, security/release sign-offs, credential handling, and result-digest policy
as defined in `recipe.md`. An unavailable name or target is a blocker, not a
reason to guess a provider or inspect local credentials.
