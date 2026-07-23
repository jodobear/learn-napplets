# SPK-A — Isolated Workspace Comparison Recipe

SPK-A is a disposable, **non-production** research fixture. It creates no workspace, dependency manifest, source tree, application, package, build output, or deployment artifact.

## Inputs and criteria

- Teaching scope: `TSCOPE-001` is blocked and selects neither a real operation nor a teaching-host profile.
- Compatibility baseline: `CMP-BASELINE-001` requires public exports only and has no selected runtime/package.
- Source bindings: `SRC-POLICY-001` and `SRC-POLICY-002` are project-policy inputs, not upstream proof.
- Blocked markers: `package.json`, `pnpm-workspace.yaml`, `src`, `apps`, and `packages` from `required-artifacts.json`.

Evaluate every candidate for seven binary criteria: public-site boundary, shared-content boundary, host-only isolation, multiple guest entries, deterministic testability, bundle isolation, and deployment compatibility. A criterion is `1` only when its boundary is explicit in the candidate text; otherwise it is `0` and the reason is recorded.

## Replay

1. Confirm no path listed in `productionMarkersBlockedBeforePhase3` exists at repository root.
2. Run the metadata assertion in `metadata.yaml` five times using `tools/phase1-python`; retain every result and SHA-256 digest.
3. Score the candidate matrix in `fixture.md` by summing the seven declared binary criteria.
4. Run `validate-spike --complete` and `validate-planning`.
5. Treat the highest qualifying candidate as a **proposed** ADR-0001 recommendation only. A tie, missing boundary, marker detection, or unavailable toolchain produces the declared failure or blocked outcome.

## Isolation rule

All layouts below are text in `fixture.md`. No replay step may materialize a layout or create any blocked marker in the repository root. Temporary output is limited to process stdout; no dependency installation, network probe, or production initialization is permitted.
