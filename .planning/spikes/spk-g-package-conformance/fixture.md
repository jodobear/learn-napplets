# SPK-G Disposable public-export consumer fixture

**Fixture status:** blocked contract; no package is installed or imported.

## Consumer declaration

| Field | Value |
| --- | --- |
| Consumer imports | none — no exact reviewed public package/export exists |
| Selected package/version | none — `CAND-NAPPLET-WEB-PACKAGE` has no released version cataloged |
| Public export locator | none — no documented package-root export cataloged |
| Conformance target | none — no public conformance fixture or target cataloged |
| Fixture location if later eligible | `.planning/spikes/spk-g-package-conformance/.experiment/public-release-if-qualified/` |
| Current outcome | `SPK-G-BLOCKED-NO-PUBLIC-RELEASE-BASELINE` |

This absence is intentional: adding a guessed import would make the fixture
claim a package identity and public surface that the catalog does not contain.

## Import policy

A future consumer import is permitted only when it uses the reviewed package
root and the exact documented public export locator. All of the following are
explicitly rejected:

- deep/package-file imports such as package subpaths, `dist/`, `src/`, or
  internal implementation files;
- relative paths into an upstream checkout, cloned repository, or monorepo;
- workspace aliases, private packages, unpublished build outputs, and
  `packages/` paths;
- fallback packages, package-name guesses, or package versions not recorded in
  `metadata.yaml` after human approval.

No private monorepo import point exists in this fixture.

## Future conformance fixture contract

After every package eligibility field is cataloged and a human approves the
exact candidate, the fixture must declare:

1. package name and exact released version;
2. documented package-root public export locator;
3. released-package and implemented-source `SRC-*` IDs plus their `CLM-*`
   relation;
4. source-baseline digest, registry integrity, official provenance, license,
   browser-support claim, and known drift;
5. a bounded local input and an expected import/compile/conformance output or
   error; and
6. five replay observations and output digests, labeled implementation evidence
   rather than protocol authority.

Until then the deterministic replay input is this document plus
`metadata.yaml`; the expected result is the blocked outcome above. The only
allowed command is the non-installing contract validation command recorded in
`recipe.md`.
