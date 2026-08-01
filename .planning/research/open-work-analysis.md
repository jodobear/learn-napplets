# Current Work Analysis

## Research question

Which immutable NAP, `napplet/web`, Kehto/Paja, and Nampplets observations can support an evidence-labeled static explanation, and which compatibility or architecture questions must remain blocked?

## Sources and immutable revisions

- `SRC-NAPS-NAP-INTENT-20260731` pins `napplet/naps@5ac0490461ca6fec2f0d2e45b4835cf9bc08de24:naps/NAP-INTENT.md` with SHA-256 `d6a533ea9c132f0196057c177e87452a7c9edda452fea4b89368afc202b709f0`. It is a repository-local NAP draft source, distinct from unresolved NIP-5D authority.
- `SRC-NAPPLET-WEB-20260731` pins the `napplet/web@03ad65b66413e5798536ef48695ffc4c2508f2c3` README with SHA-256 `f21e5bc41a990e40b72124ca68109b63df40b9850758c4346f151ec328ba7dae` as observed alpha implementation evidence.
- `SRC-KEHTO-WEB-PAJA-20260731` pins `kehto/web@d42b3c3da7e0ad3cea233b34458997b09b11960d:packages/paja/README.md` with SHA-256 `dcf02f032bafd87be94297a1995025069df7ff44444b9087d6e1e580ef7e4c33` as observed implementation evidence.
- `SRC-NAMPLETS-NATIVE-20260731` pins `pablof7z/nampplets@1094f1db23292f966fd65757132678406f7ca28c:README.md` with SHA-256 `3d1a5165f97bfdb50d3155bbf04044be6bbe63df91385f8e56f1865de2b8874b` as optional native-reference behavior only.
- `OWS-004` retains separate retrieval-response digests for mutable `napplet/web` #186/#192/#194 and `kehto/web` #217 direction metadata; those records are not source records and do not establish normative behavior.

## Observations

The four admitted blobs provide enough provenance to display a static source/status explanation: a repository-local draft NAP text, alpha web implementation context, Paja local-authoring context, and an explicitly optional native reference. The web and Kehto records are observed implementation, and the Nampplets record is a native reference; none gains NAP/NIP authority by appearing beside the NAP draft.

## Conflicts

`NAP-INTENT.md` itself names a NIP-5D web binding while direct NIP-5D authority remains unresolved. `napplet/web` direction includes merged migration and INTENT-alignment work, while `kehto/web` documents a different implementation environment. The records preserve those parallel sides; no compatibility winner, teaching host, or runtime contract is selected.

`napplet/web` #194 is a package-version merge containing filesystem-named changesets. It is retained as release-direction metadata only; it does not prove a published artifact, root export, package integrity, or filesystem behavior.

## Inference

A static page may truthfully explain the evidence classes and unresolved boundaries if every source and statement retains its ID, maturity, source status, and uncertainty label. It must not teach implementation conventions as protocol law or imply that an implementation/release snapshot is package-qualified.

## Prototype or measurement

None. This work pinned source bytes and recorded bounded direction metadata; it did not install packages, execute a runtime, contact relays, run a browser lab, or test portability.

## Recommendation

Keep `CMP-BASELINE-001` and all package, native qualification, runtime, Firefox, teaching-host, and portability dimensions blocked. Use only the four stable source IDs and the `OWS-004` directional labels in the static site. A future review must directly acquire the missing NIP-5D source and independently qualify package/runtime evidence before changing those states.

## Uncertainty

Material. The NAP source is a draft with unresolved web projection; the other sources are implementation/reference observations. Pull-request direction metadata is mutable and is retained only to explain why a review may be needed.

## Affected phases and requirements

- Phase: `01`
- Requirements: `EVID-01`, `EVID-02`, `EVID-03`, `OPER-01`
- Drift records: `DRF-DISCOVERY-001`, `DRF-INTENT-001`, `DRF-MANIFEST-001`, `DRF-METADATA-001`, `DRF-HANDSHAKE-001`, `DRF-EGRESS-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical and content-learning human review, with security review for implementation boundary claims. Automation may prepare status-labeled static content but cannot accept an ADR, a residual risk, a package, or a runtime direction.
