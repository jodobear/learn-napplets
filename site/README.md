# Learn Napplets static evidence edition

This directory is a dependency-free, local-only learning surface. It is generated from `site/content/site.json`; it does not start a host, execute a guest napplet, contact a relay, use a wallet or signer, or qualify a runtime or package.

## Build

From the repository root, rebuild the checked-in site with Python's standard library only:

```sh
python3 tools/build-site.py
python3 tools/build-site.py --check
```

The build writes the public output to `site/dist/`. Do not edit generated HTML, `knowledge.json`, or copied local assets directly. Edit the structured content, template, or authored local assets, then rebuild.

## Local preview

Build first, then serve only the generated directory on loopback:

```sh
python3 tools/build-site.py
cd site/dist
python3 -m http.server 8000 --bind 127.0.0.1
```

Open the deterministic learning path in a browser:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/learn/
- http://127.0.0.1:8000/architecture/
- http://127.0.0.1:8000/sources/

All essential content is static HTML. JavaScript only adds an optional, page-local reading trace beside the architecture transcript; disabling it leaves the path, transcript, table, source labels, and blockers complete. The site makes no required external requests. The source-ledger links are inspectable immutable identities and are not fetched as part of the learning path.

## Verification

```sh
python3 tools/build-site.py --check
python3 -m unittest discover -s tests/site -p 'test_static_site.py' -v
tools/phase1-python -m unittest discover -s tests/site -p 'test_site_browser.py' -v
```

The browser checks use the already-approved local Chromium environment. They do not download a browser, add a dependency, or use a live service.
