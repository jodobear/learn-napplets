# Protocol and Taxonomy Evidence Map

## Research question

What can the dated immutable source set say about NAP-INTENT, NIP-5D, alpha web implementation behavior, Paja, and a native reference without presenting implementation or draft material as settled protocol law?

## Sources and immutable revisions

- `SRC-NAPS-NAP-INTENT-20260731` pins `napplet/naps@5ac0490461ca6fec2f0d2e45b4835cf9bc08de24:naps/NAP-INTENT.md` (SHA-256 `d6a533ea9c132f0196057c177e87452a7c9edda452fea4b89368afc202b709f0`) as a repository-local NAP **draft** specification. It identifies NAP-INTENT and a NIP-5D web binding, but it is not the missing direct NIP-5D authority.
- `SRC-NAPPLET-WEB-20260731` pins `napplet/web@03ad65b66413e5798536ef48695ffc4c2508f2c3:README.md` (SHA-256 `f21e5bc41a990e40b72124ca68109b63df40b9850758c4346f151ec328ba7dae`) as an **observed alpha implementation** source.
- `SRC-KEHTO-WEB-PAJA-20260731` pins `kehto/web@d42b3c3da7e0ad3cea233b34458997b09b11960d:packages/paja/README.md` (SHA-256 `dcf02f032bafd87be94297a1995025069df7ff44444b9087d6e1e580ef7e4c33`) as an **observed implementation** source.
- `SRC-NAMPLETS-NATIVE-20260731` pins `pablof7z/nampplets@1094f1db23292f966fd65757132678406f7ca28c:README.md` (SHA-256 `3d1a5165f97bfdb50d3155bbf04044be6bbe63df91385f8e56f1865de2b8874b`) as an optional **native-reference observation**.
- `SRC-POLICY-001` and `SRC-POLICY-002` remain project-policy/archive context, not upstream protocol evidence. Mutable pull-request direction remains separately retained in `OWS-004`, never as a canonical source record.

## Observations

- **Draft specification:** `CLM-NAP-INTENT-20260731` can explain that the NAP-INTENT draft describes an archetype intent dispatcher and labels a NIP-5D web binding. It remains provisional and cannot settle NIP-5D meaning, projection, runtime, or browser behavior.
- **Observed web implementation:** `CLM-NAPPLET-WEB-20260731` can display that its own README calls the project alpha and describes an implementation-specific SDK/shell model. It cannot qualify a package, a runtime, a browser, or a protocol conclusion.
- **Observed Paja implementation:** `CLM-KEHTO-WEB-PAJA-20260731` can explain that Paja documents local authoring/testing, live-relay defaults, and an explicit memory fixture mode. These are Kehto behavior observations, not a selected teaching host or a portable/runtime result.
- **Native reference:** `CLM-NAMPLETS-NATIVE-20260731` can explain that Nampplets is an in-progress native Rust/macOS reference with an unratified compatibility lock. It is neither NAP/NIP authority nor evidence for web compatibility.

## Conflicts

- The NAP-INTENT draft names a NIP-5D web binding, while direct NIP-5D authority remains unavailable. `DRF-INTENT-001` preserves the draft and observed alpha implementation sides without selecting a protocol winner.
- `OWS-004` separately preserves mutable `napplet/web` migration/INTENT direction (#186 and #192), filesystem-named release metadata (#194), and Paja social-cache direction (#217). These objects explain review triggers only; they are not immutable source content, behavior proof, or package evidence.
- Paja's documented local environment and Nampplets' native environment are different observed contexts. They do not select a teaching host, resolve Firefox/browser gaps, establish portability, or prove a common runtime contract.
- Package qualification, public artifact integrity/root export, measured conformance, direct NIP-5D authority, and browser/runtime evidence remain blocked in `CMP-BASELINE-001`, `DRF-ARTIFACT-001`, `DRF-CONFORMANCE-001`, and the relevant `OQ-*` records.

## Inference

A static public explanation may present the source IDs, classes, maturity, uncertainty, and explicit blockers together. The only safe inference is about the evidence boundary: a draft source, an implementation observation, and a native reference must stay visibly distinct. It must not teach their implementation conventions as protocol requirements or imply package/runtime support.

## Prototype or measurement

None. This map records immutable source bytes and bounded directional metadata only. It did not install packages, execute a guest/runtime, contact relays, run a browser lab, test a conformance target, or qualify a portable artifact.

## Recommendation

Use the four stable source IDs and their matching `CLM-*` IDs only for status-labeled, deterministic static explanation. Keep NIP-5D, NAP registry/projection, package admission, runtime/browser support, first teaching-host selection, and portable-target outcomes blocked. Refresh only if a cited upstream head changes after 2026-07-31, a cited blob becomes unavailable, or review requires a different source scope.

## Uncertainty

Material. The NAP source is a repository-local draft with an unresolved NIP-5D dependency; napplet/web and Paja are implementation observations; Nampplets is native-reference behavior; mutable pull-request metadata is directional only. No human technical, content, or security review has converted these observations into accepted facts.

## Affected phases and requirements

- Requirements: `EVID-01`, `EVID-02`, `EVID-03`, `OPER-01`.
- Phase: `01` research baseline.
- Downstream work: static source/status presentation; compatibility assessment; mandatory protocol-related spikes; teaching-host, package, browser, and runtime decisions.

## Owner and required approval

Owner: research-owner. Required approval: protocol-technical and content-learning human review, with security review for authority-boundary implications. Automation must not mark this evidence verified, accept an ADR, authorize a package, select a host, or transition the project to Phase 2.
