# SPK-E — Shared-source content rendering replay

This is a disposable, non-production local experiment. It does not create an application route, framework scaffold, public artifact, or a second authoring source.

## Single source boundary

`fixture.yaml` is the only content-fact input. `render.py` contains format templates only and reads the record plus `canonicalFieldValues` from that fixture. It must not define a replacement source, claim, terminology, maturity, uncertainty, or status value.

The fixture deliberately uses the canonical source ID `SRC-POLICY-002`, claim ID `CLM-POLICY-001`, term `immutable source record`, maturity `accepted`, uncertainty state `limited`, and status `provisional`. The last four are exact canonical controlled values; the current canonical records do not define separate stable IDs for those vocabularies.

## Procedure

1. Validate the pre-execution envelope:

   ```text
   tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-e-content-rendering --contract
   ```

2. Remove only the isolated local output directory, then render the six target representations:

   ```text
   rm -rf /tmp/spk-e-content-rendering
   tools/phase1-python .planning/spikes/spk-e-content-rendering/render.py --fixture .planning/spikes/spk-e-content-rendering/fixture.yaml --out /tmp/spk-e-content-rendering
   ```

3. Read `/tmp/spk-e-content-rendering/manifest.json`. It contains SHA-256 output digests and a field-level equality result for exactly these six generated files: `static.html`, `guest-content.json`, `content.md`, `glossary.md`, `transcript.txt`, and `knowledge.json`.

4. Replay step 2 into a fresh `/tmp` directory and compare manifests byte-for-byte. Any different digest or any mismatch in `sourceId`, `claimId`, `terminology`, `maturity`, `uncertaintyState`, or `status` is a failure.

5. Record the actual command, environment, fixture digest, per-output digests, parity result, and replay result in `environment.json`, `measurements.yaml`, and `report.md`. Keep generated output local to `/tmp` unless a mismatch requires retained decision evidence.

## Outcome handling

- **Passed:** all six representations were generated from the one fixture and preserve every required canonical field exactly. This is proposed ADR-0004 evidence only.
- **Failed:** retain the failed local output and its digest, describe the specific divergent field, and make no positive renderer recommendation. Never repair a target by hand or create another fact source.
- **Blocked:** record the approved-toolchain blocker and its impact on ADR-0004/Phase 02. Do not install a package, introduce a framework, or create an application route to work around it.

No observation from this replay establishes upstream protocol behavior or accepts an ADR.
