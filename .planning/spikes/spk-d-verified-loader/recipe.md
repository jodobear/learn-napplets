# SPK-D — Verified-loader feasibility recipe

Non-production disposable research spike. This recipe records feasibility limits; it does not create a loader, perform signature/blob/aggregate verification, or establish a protocol fact.

## Scope and question

Can the repository currently replay a source-backed, reviewed verification path for manifest resolution, identity mapping, signature verification, blob verification, aggregate verification, and exact-byte loading?

The answer is initially **blocked**. The only available source record is policy/archive evidence that explicitly states that no current upstream conclusion is established until official immutable records are collected and reviewed. The fixture therefore verifies only the integrity of explicitly supplied local bytes; it never represents a manifest, signature, blob, aggregate, identity, or successful verifier output.

## Immutable binding matrix

Every row uses the same available blocked baseline, `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001`:

- immutable revision: `c626d4c9d6e8e325672b71eb4d93dbe0753fe8f0`
- path: `docs/learn-napplets-codex-pack-v3/docs/02-UPSTREAM-TRUTH-AND-DRIFT.md`
- locator: `Source and claim record model`
- content SHA-256: `df04218b808e3b5925dde0ea2041660f4304d3e92af399a273e34a1c25f4b9bb`
- retrieval time: `2026-07-24T00:00:00Z`
- authority/evidence/maturity: `planning-archive` / `project-policy` / `accepted`

| Primitive | SRC/CLM binding | Expected classification | Expected outcome |
| --- | --- | --- | --- |
| Manifest resolution | `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` | blocked | No resolver or current immutable manifest record is invoked. |
| Identity mapping | `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` | blocked | No `d` tag, aggregate identity tuple, or mapping rule is invented. |
| Exact artifact-byte loading | `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` | blocked | Local byte decoding/digest comparison is replayed; loader behavior remains unproven. |
| Signature verification | `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` | blocked | No signature value, key, or verifier is supplied or simulated. |
| Blob verification | `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` | blocked | No blob contract or verifier is supplied or simulated. |
| Aggregate verification | `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` | blocked | No aggregate value, algorithm, or verifier is supplied or simulated. |
| Reused verifier provenance | `SRC-POLICY-001` / `CLM-UPSTREAM-BASELINE-001` | blocked | No reviewed verifier implementation exists to reuse. |

`SRC-POLICY-001` is a project-policy/archive seed, not current upstream protocol authority. Its use preserves the blocker; it does not fill the missing verification surface.

## Exact fixture

`fixture.json` pins the synthetic local input:

- encoding: hex
- bytes: `53504b2d44206c6f63616c20666978747572652062797465732076310a`
- byte length: `29`
- SHA-256: `b83079843b0410559ad4e275557c4103d3a3b86026fc0bc9eccf62fe42e9607c`

The deterministic mutation is one byte only:

- ID: `one-byte-xor-offset-0`
- offset: `0`
- original byte: `0x53`
- mutated byte: `0x52`
- mutated bytes: `52504b2d44206c6f63616c20666978747572652062797465732076310a`
- byte length: `29`
- SHA-256: `34e7f0624caefa1b9e3257946df0eed0d37c0b6253c41d0a7d3975a622e39d9d`

Both cases have expected verification state `blocked`. A different local digest establishes only that the provided bytes changed; it does not make any unavailable signature, blob, aggregate, manifest, identity, or loader surface succeed or fail.

## Approved deterministic replay

Use only the project-approved Phase 1 Python wrapper and Python standard library. Do not install, fetch, substitute, or invoke another package, service, signing key, or verifier.

```bash
tools/phase1-python -c "import hashlib,json; f=json.load(open('.planning/spikes/spk-d-verified-loader/fixture.json')); b=bytes.fromhex(f['artifact']['exactBytesHex']); m=bytes([b[0]^1])+b[1:]; assert len(b)==f['artifact']['byteLength']==len(m); assert hashlib.sha256(b).hexdigest()==f['artifact']['sha256']; assert sum(x!=y for x,y in zip(b,m))==1; assert hashlib.sha256(m).hexdigest()==f['mutationCase']['sha256']; assert all(s['status']=='blocked' for s in f['verificationSurfaces'])"
```

The command is an integrity replay only. It uses `hashlib` to compare the exact fixture digest already recorded in the fixture; it does not implement a signature, blob, aggregate, manifest, identity, or loader algorithm.

Then run:

```bash
tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-d-verified-loader --complete
tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-d-verified-loader/report.md
tools/phase1-python tools/validate-research.py validate-impact-fragment --root .planning .planning/spikes/spk-d-verified-loader/impact-fragment.yaml
```

## Outcome thresholds

- **Success:** only a later current immutable source baseline and publicly reviewed verifier can validate every declared surface for the unchanged fixture and reject the mutation. This plan does not assert that threshold.
- **Failure:** a later reviewed verification surface produces a recorded mismatch for an otherwise supported primitive. Preserve the error and make no positive recommendation.
- **Blocked:** the current result. Missing immutable manifest/identity sources and reviewed verifier provenance prevent every protocol-sensitive primitive from being executed. Preserve exact-byte observations and the impact-scoped blocker without substitution.

## Safety boundary

- No secrets, keys, live network access, destructive state, dependency installation, or browser execution are used.
- No custom cryptography, aggregate calculation, signature construction, or verifier implementation is permitted.
- No conclusion is promoted beyond a local fixture-integrity observation; Plan 01-28 alone may validate and serially merge proposed impacts.
