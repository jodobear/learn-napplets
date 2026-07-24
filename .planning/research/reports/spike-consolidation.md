# Spike Consolidation Audit

This deterministic audit records immutable inputs and serialized outcomes; it does not accept an ADR or promote a local observation into an upstream fact.

## Immutable input snapshot

| Spike | Report | Metadata | Measurement | Fragment |
| --- | --- | --- | --- | --- |
| SPK-A | `spikes/spk-a-workspace/report.md` SHA-256 `5a3d445a81ceb49c1335abbd6ee5abb33b6027b6327763d20fba273608e90e4b` | `spikes/spk-a-workspace/metadata.yaml` SHA-256 `f93a8a6f9f4e219967a5cb12aca222da352c58054797cb47dffb0ef46cc44573` | `spikes/spk-a-workspace/measurements.yaml` SHA-256 `aa24ff4fec4f52c4bcdb7e28c62b0357e386472b36fdc581425e5a546af2a44e` | no-impact-fragment |
| SPK-B | `spikes/spk-b-static-framework/report.md` SHA-256 `3c47d39388afb79f96bbf893eaf5e414cd2267ab8d466ac1428d03a2133e1c10` | `spikes/spk-b-static-framework/metadata.yaml` SHA-256 `7d2b688cf0b163d6bceac2aef405441abe9ffd625aa6556ea9d39a9c9b423809` | `spikes/spk-b-static-framework/measurements.yaml` SHA-256 `12019091bb5221bea64909f828e89e371626cbb9a4ced8aedf034d8d74725275` | no-impact-fragment |
| SPK-C | `spikes/spk-c-boundary-harness/report.md` SHA-256 `ad21b749834d8d4df9382a1b80eb9526f952da1d1c7132fb603561427a31738e` | `spikes/spk-c-boundary-harness/metadata.yaml` SHA-256 `39c876306da5d086ffdaa28114e648b092b5e242f858a02ceb8d7c9e2ed09c11` | `spikes/spk-c-boundary-harness/measurements.yaml` SHA-256 `743d2a9f369312c2dd410d4d77a30a658f0ef21204b8f609cb2b8bc4cb5777d3` | `spikes/spk-c-boundary-harness/impact-fragment.yaml` SHA-256 `36e268fd57f36b44b779954758f4b7990e588e9c60b87bc5fa5a3c737c8e2ac4` |
| SPK-D | `spikes/spk-d-verified-loader/report.md` SHA-256 `1eb9c8634698a9487078d0a01131f597473a5966e93f679dca30bf8bf5a60b50` | `spikes/spk-d-verified-loader/metadata.yaml` SHA-256 `d4b83bb4d3eb6d49b5ed2ae804170bd1acba19332ec02a05e9f1c1f3a80a5781` | `spikes/spk-d-verified-loader/measurements.yaml` SHA-256 `3ddb0748c92d44204647cea6f5261392b239de95c97de1473853dae7644c9143` | `spikes/spk-d-verified-loader/impact-fragment.yaml` SHA-256 `ea1f91f0737b22c8df9655ca2fe56c40c5391c19b40d8d9b2977cfdb1728c893` |
| SPK-E | `spikes/spk-e-content-rendering/report.md` SHA-256 `26503edcec77a0a65b44dfbd5c2a75a987390be3530a2bc18d7fc54e8a425588` | `spikes/spk-e-content-rendering/metadata.yaml` SHA-256 `623490c15e47fc73478147c4d1a7cddf86fe055de8fa0cf2c33b81da4e1c6d3c` | `spikes/spk-e-content-rendering/measurements.yaml` SHA-256 `ced41b4a399597f131d7a3368bc1122e9bca052c81c1f7e796a267d6314c2cb8` | no-impact-fragment |
| SPK-F | `spikes/spk-f-course-workbench/report.md` SHA-256 `06db24dc5fdb3ab863a80f85c4c85648181c4589a923c99ee1ae3a15a8fd96ef` | `spikes/spk-f-course-workbench/metadata.yaml` SHA-256 `2bf5d338c11276ac16b42dc1982cb4bf3ad91bef84449fd7daade27c781bf4fd` | `spikes/spk-f-course-workbench/measurements.yaml` SHA-256 `d235ca07db2a8cde1444277c5e1689e63086421d1cbc95e6a9cd15e2435f1ce6` | no-impact-fragment |
| SPK-G | `spikes/spk-g-package-conformance/report.md` SHA-256 `5f1993cbff951b4ae68508806f7b48f841198b31e9fa91b7c4c575c546963e86` | `spikes/spk-g-package-conformance/metadata.yaml` SHA-256 `8a0a91e7a70a77466aa3942cdc2e6c59a5350df98a59606ecd68a3d315f8195c` | `spikes/spk-g-package-conformance/measurements.yaml` SHA-256 `aba6aa72bfcdf68498c90108314e2464a0e195086412bb090e91917255fed59b` | `spikes/spk-g-package-conformance/impact-fragment.yaml` SHA-256 `0814880f4d58a28a7702f40931841b5e151d19aa8a959d779701019e3b19cae1` |
| SPK-H | `spikes/spk-h-browser-egress/report.md` SHA-256 `715589b73dea61bb8e620c9ef5a54a066c2bbe8b4d4317450188e7a185c0cfb6` | `spikes/spk-h-browser-egress/metadata.yaml` SHA-256 `1f6e42f81ce9f1ae765d9166eb9b09676f67c366e410feb744626127ba84fbfb` | `spikes/spk-h-browser-egress/measurements.yaml` SHA-256 `5d91d92ea90c98e62d51119da6c5be3aae483501b4d9b6aa604bcb79298680d8` | `spikes/spk-h-browser-egress/impact-fragment.yaml` SHA-256 `40d7f7bfacffd2630bc9884ba717da0d263ef5b092de5abee69fb86d094b8042` |
| SPK-I | `spikes/spk-i-diagram-motion/report.md` SHA-256 `eb08fd60641fdbd8e588e212f60b0267f33357c49db04080656ff19336b0dec3` | `spikes/spk-i-diagram-motion/metadata.yaml` SHA-256 `7815b5b83a07ff3e648db6b00b25fbb9626cd8043692d429967b377edc66b7d4` | `spikes/spk-i-diagram-motion/measurements.yaml` SHA-256 `a7955dda9f692d794dd4f07040f6aa3a3f28c10777bb19b699cb675bfd108f61` | no-impact-fragment |
| SPK-J | `spikes/spk-j-code-editing/report.md` SHA-256 `48ceace6a76927b2cb4fd7881235bff926a7524621885e1aa98a1c4cf03e3321` | `spikes/spk-j-code-editing/metadata.yaml` SHA-256 `05a510beee8e88e8a68113d3abe95a21ae74efdeac355daea39512b27bfca1c5` | `spikes/spk-j-code-editing/measurements.yaml` SHA-256 `2407701d1128ad1ac076a9c050f4f7b6bb3e0d0b0658ccc4a52de7114d3b6b1b` | no-impact-fragment |
| SPK-K | `spikes/spk-k-deployment/report.md` SHA-256 `923d3085c176dbdb83603d283f4f4ddaf0128eab90244ccbd8e20fefd42dd594` | `spikes/spk-k-deployment/metadata.yaml` SHA-256 `2bfba0fc63e9a775fb7d36b86037f9f5b679cba75a23e267aec25f6ce998b26c` | `spikes/spk-k-deployment/measurements.yaml` SHA-256 `8b0f2c8f997427e9677c989c80a78586cf45f0b4d4c8a06b7f740bb6cb1a2b70` | no-impact-fragment |
| SPK-L | `spikes/spk-l-source-freshness/report.md` SHA-256 `452c5f824c15df942deb8630b5eea4cadde27f32598d9bf8a53dfee92f47bd2d` | `spikes/spk-l-source-freshness/metadata.yaml` SHA-256 `96814da6ab39d241639b2c7ce69f08056cb757dddf3ffe950a82a3a9ffd9df9a` | `spikes/spk-l-source-freshness/measurements.yaml` SHA-256 `ce7b85a04c9833b197a1e2d6c0c2b2b0f55e4e4e8ebeecb11c57187c82d7588d` | no-impact-fragment |

## Serialized outcomes

| Stable ID | Disposition |
| --- | --- |
| SPK-C-IMPACT-001 | merged |
| SPK-D-IMPACT-001 | merged |
| SPK-G-IMPACT-001 | merged |
| SPK-H-IMPACT-001 | merged |

## Blocked and uncertain outcomes

- `SPK-C-IMPACT-001`: uncertainty `material` — The only source bindings are blocked project-policy records, and the Firefox execution surface supplied no fixture observation; SPK-C cannot select or prove a cross-browser teaching-host profile. Open questions: OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001.
- `SPK-D-IMPACT-001`: uncertainty `material` — The fixture proves only its supplied byte-digest and one-byte mutation observations. Current immutable manifest/identity sources and reviewed signature/blob/aggregate/loader provenance are absent, so no protocol or compatibility behavior is established. Open questions: OQ-VERIFIED-LOADER-MANIFEST-001, OQ-VERIFIED-LOADER-IDENTITY-001, OQ-VERIFIED-LOADER-VERIFIER-001.
- `SPK-G-IMPACT-001`: uncertainty `material` — The human block and local replay establish only that no qualified candidate was available or executed. Package identity, public exports, license, integrity, browser support, source revision, drift, and conformance remain unresolved. Open questions: OQ-PUBLIC-PACKAGE-BASELINE-001, OQ-PUBLIC-CONFORMANCE-001.
- `SPK-H-IMPACT-001`: uncertainty `material` — The only source bindings are project policy/archive inputs; Chrome measures one disposable local fixture, Firefox has no attached-context result, and neither result establishes upstream protocol behavior or a production CSP. Open questions: OQ-EGRESS-NIP-001, OQ-FIREFOX-PLAYWRIGHT-LAUNCH-001.

## Transaction

- Exclusive `fcntl.flock` lock acquired before immutable snapshot and staging.
- Canonical targets: compatibility-matrix.yaml, drift-register.yaml, open-questions.yaml, security-egress-findings.md, replay-manifest.yaml.
- Blocked and uncertain dispositions remain blocked; no report prose becomes an asserted upstream fact.
- Replay manifest SHA-256: `679be644f14a77b6c40528a74aea29e530837ef2db731a24ac13f8d4d4177d93`.
- Rerun input digest: `17fb823be4794eebcd5a52cf6b8753063b28a68cf5b6b8e9d85871dbc7e97d85`; identical validated inputs produce byte-identical staged outputs.
