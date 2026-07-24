#!/usr/bin/env python3
"""Measure the approved SPK-J fixture and CodeMirror candidate locally.

The runner serves only the SPK-J fixture and its ignored local node_modules tree on
loopback. It never evaluates learner text: fixture tests submit text only to native
textareas whose implementation uses exact comparison and textContent, while the
CodeMirror harness receives only a fixed synthetic document.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from playwright.sync_api import Browser, BrowserType, Page, sync_playwright

EXPECTED_PLAYWRIGHT = "1.61.0"
SAMPLES = 5
STARTER = 'const greeting = "Hello";'
ALTERNATE = 'const greeting = "Hi";'
HOSTILE = '<script>window.__spkJTrustedHostSentinel = "changed"</script>'
SENTINEL = "spk-j-trusted-context-sentinel-v1"
BROWSERS = (
    ("Chromium", "Google Chrome", "/opt/google/chrome/google-chrome"),
    ("Firefox", "Mozilla Firefox", "/usr/bin/firefox"),
)
DIRECT_PACKAGES = (
    "@codemirror/state",
    "@codemirror/view",
    "@codemirror/commands",
    "@codemirror/lang-javascript",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def expect(condition: bool, name: str, checks: dict[str, bool]) -> None:
    checks[name] = condition
    if not condition:
        raise AssertionError(name)


def tree_size(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def local_fixture_safety(fixture: Path) -> dict[str, Any]:
    """Inspect source text without interpreting learner-controlled values."""
    text = fixture.read_text(encoding="utf-8")
    forbidden = (
        "eval(",
        "new Function",
        "innerHTML",
        "createElement('script')",
        "fetch(",
        "localStorage",
        "sessionStorage",
        "postMessage(",
        "srcdoc",
        "Worker(",
    )
    return {
        "fixtureContainsOnlyTrustedScript": text.count("<script>") == 1,
        "forbiddenFixtureTokens": [token for token in forbidden if token in text],
        "usesTextContent": text.count("textContent"),
        "hasTrustedSentinel": "__spkJTrustedHostSentinel" in text,
        "hasExactVariantComparison": "value === starter" in text and "value === alternate" in text,
        "hostileInputTest": "runner supplies one fixed hostile literal to the native textarea; fixture source does not embed learner-controlled markup",
    }


def package_entry(package_dir: Path) -> str | None:
    package = json.loads((package_dir / "package.json").read_text(encoding="utf-8"))
    exports = package.get("exports")
    if isinstance(exports, str):
        return exports
    if isinstance(exports, dict):
        root = exports.get(".")
        if isinstance(root, str):
            return root
        if isinstance(root, dict):
            candidate = root.get("import") or root.get("default")
            if isinstance(candidate, str):
                return candidate
        candidate = exports.get("import") or exports.get("default")
        if isinstance(candidate, str):
            return candidate
    for key in ("module", "main"):
        if isinstance(package.get(key), str):
            return package[key]
    return None


def package_directories(node_modules: Path) -> list[Path]:
    directories: list[Path] = []
    for child in sorted(node_modules.iterdir()):
        if child.name.startswith("."):
            continue
        if child.name.startswith("@"):
            directories.extend(path for path in sorted(child.iterdir()) if (path / "package.json").is_file())
        elif (child / "package.json").is_file():
            directories.append(child)
    return directories


def module_map(node_modules: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    imports: dict[str, str] = {}
    inventory: list[dict[str, str]] = []
    for directory in package_directories(node_modules):
        package_path = directory / "package.json"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        name = package.get("name")
        entry = package_entry(directory)
        if not isinstance(name, str) or entry is None:
            continue
        relative_dir = directory.relative_to(node_modules).as_posix()
        imports[name] = f"/modules/{relative_dir}/{entry.removeprefix('./')}"
        inventory.append(
            {
                "name": name,
                "version": str(package.get("version")),
                "packageJsonSha256": sha256_file(package_path),
                "entry": entry,
            }
        )
    return imports, inventory


def harness_html(imports: dict[str, str]) -> str:
    import_map = json.dumps({"imports": imports}, sort_keys=True)
    return f"""<!doctype html>
<html lang=\"en\"><meta charset=\"utf-8\"><title>SPK-J CodeMirror local harness</title>
<style>
  body {{ font: 16px system-ui, sans-serif; margin: 1rem; }}
  #cm-shell {{ border: 2px solid currentColor; padding: .5rem; }}
  #cm-shell:focus-within {{ outline: 3px solid Highlight; outline-offset: 3px; }}
  pre {{ white-space: pre-wrap; }}
</style>
<main>
  <h1>SPK-J CodeMirror local harness</h1>
  <p id=\"fallback\">Static fallback: {STARTER}</p>
  <p>This harness imports approved local packages only and passes a fixture constant to the editor. It never accepts or executes learner code.</p>
  <div id=\"cm-shell\" aria-label=\"Approved CodeMirror synthetic editor\"></div>
  <output id=\"cm-status\" aria-live=\"polite\">Loading approved local package candidate.</output>
</main>
<script type=\"importmap\">{import_map}</script>
<script type=\"module\">
  import {{EditorState}} from \"@codemirror/state\";
  import {{EditorView, keymap}} from \"@codemirror/view\";
  import {{defaultKeymap}} from \"@codemirror/commands\";
  import {{javascript}} from \"@codemirror/lang-javascript\";
  const starter = {json.dumps(STARTER)};
  const sentinel = {json.dumps(SENTINEL)};
  window.__spkJTrustedHostSentinel = sentinel;
  const state = EditorState.create({{doc: starter, extensions: [keymap.of(defaultKeymap), javascript()]}});
  const view = new EditorView({{state, parent: document.getElementById('cm-shell')}});
  document.getElementById('cm-status').textContent = `Approved package candidate rendered ${{view.state.doc.length}} fixed characters.`;
  window.__spkJCodeMirrorObservation = {{
    fixedDocument: view.state.doc.toString(),
    contentEditable: view.contentDOM.getAttribute('contenteditable'),
    sentinelIntact: window.__spkJTrustedHostSentinel === sentinel
  }};
</script>
</html>"""


class LocalOnlyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, fixture: Path, modules: Path, harness: Path, **kwargs: Any) -> None:
        self.fixture = fixture
        self.modules = modules
        self.harness = harness
        super().__init__(*args, directory="/", **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def translate_path(self, path: str) -> str:
        request = unquote(urlparse(path).path)
        if request == "/fixture.html":
            return str(self.fixture)
        if request == "/harness.html":
            return str(self.harness)
        if request.startswith("/modules/"):
            relative = Path(request.removeprefix("/modules/"))
            candidate = (self.modules / relative).resolve()
            if candidate == self.modules or self.modules in candidate.parents:
                return str(candidate)
        return str(self.harness.parent / "not-found")


def serve_local(fixture: Path, modules: Path, harness: Path) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    handler = lambda *args, **kwargs: LocalOnlyHandler(*args, fixture=fixture, modules=modules, harness=harness, **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{server.server_port}"


def screenshot_digest(page: Page, path: Path) -> str:
    image = page.screenshot(path=path, full_page=True, caret="hide", scale="css")
    return sha256_bytes(image)


def fixture_checks(page: Page, checks: dict[str, bool]) -> dict[str, Any]:
    expect(page.locator("h1").count() == 1, "fixture-main-heading", checks)
    expect(page.locator("label[for='controlled-edit']").count() == 1, "controlled-textarea-label", checks)
    expect(page.locator("#controlled-edit").count() == 1, "controlled-textarea-present", checks)
    expect(page.locator("#controlled-status[aria-live='polite']").count() == 1, "controlled-status-announced", checks)
    expect(page.locator("button[data-fixed]").count() == 2, "fixed-variant-buttons", checks)

    page.locator("body").press("Tab")
    expect(page.evaluate("(value) => document.activeElement && document.activeElement.dataset.fixed === value", STARTER), "keyboard-tab-reaches-fixed-variant", checks)
    page.keyboard.press("Enter")
    expect("starter variant recognized" in (page.locator("#fixed-output").text_content() or ""), "keyboard-enter-selects-fixed-variant", checks)
    focus_outline = page.evaluate("getComputedStyle(document.activeElement).outlineStyle")
    expect(focus_outline != "none", "native-visible-focus", checks)

    controlled = page.locator("#controlled-edit")
    controlled.fill(ALTERNATE)
    expect("alternate variant recognized" in (page.locator("#controlled-status").text_content() or ""), "controlled-exact-alternate-recognized", checks)
    controlled.fill(HOSTILE)
    expect("unrecognized literal text" in (page.locator("#controlled-status").text_content() or ""), "hostile-text-remains-unrecognized", checks)
    expect(page.locator("script").count() == 1, "hostile-text-creates-no-script", checks)
    expect(page.evaluate("window.__spkJTrustedHostSentinel") == SENTINEL, "trusted-context-sentinel-unchanged", checks)
    page.locator("#controlled-reset").click()
    expect(controlled.input_value() == STARTER, "controlled-reset-restores-starter", checks)

    lightweight = page.locator("#lightweight-edit")
    lightweight.fill(ALTERNATE)
    expect("1 line(s)" in (page.locator("#lightweight-status").text_content() or ""), "lightweight-inspection-reports-lines", checks)
    page.locator("#lightweight-reset").click()
    expect(lightweight.input_value() == STARTER, "lightweight-reset-restores-starter", checks)
    return {"screenReaderSpeech": "not-observed; labels and aria-live semantic DOM contract checked"}


def harness_checks(page: Page, checks: dict[str, bool]) -> None:
    page.wait_for_function("window.__spkJCodeMirrorObservation !== undefined")
    observation = page.evaluate("window.__spkJCodeMirrorObservation")
    expect(observation["fixedDocument"] == STARTER, "codemirror-receives-fixed-document-only", checks)
    expect(observation["contentEditable"] == "true", "codemirror-contenteditable-exposed", checks)
    expect(observation["sentinelIntact"] is True, "codemirror-sentinel-unchanged", checks)
    content = page.locator(".cm-content")
    content.focus()
    expect(page.evaluate("document.activeElement.classList.contains('cm-content')"), "codemirror-keyboard-focusable", checks)
    outline = page.evaluate("getComputedStyle(document.getElementById('cm-shell')).outlineStyle")
    expect(outline != "none", "codemirror-harness-visible-focus", checks)
    expect("fixed characters" in (page.locator("#cm-status").text_content() or ""), "codemirror-status-announced", checks)


def static_fallback_check(browser: Browser, base_url: str) -> dict[str, bool]:
    context = browser.new_context(java_script_enabled=False, service_workers="block")
    try:
        page = context.new_page()
        page.goto(f"{base_url}/fixture.html", wait_until="load")
        fixture_readable = STARTER in (page.locator("body").text_content() or "") and ALTERNATE in (page.locator("body").text_content() or "")
        page.goto(f"{base_url}/harness.html", wait_until="load")
        harness_readable = STARTER in (page.locator("#fallback").text_content() or "")
        return {"fixtureStaticEquivalent": fixture_readable, "codeMirrorStaticFallback": harness_readable}
    finally:
        context.close()


def run_sample(browser: Browser, base_url: str, output: Path, family: str, sample: int) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    requests: list[str] = []
    sample_dir = output / family.lower() / f"sample-{sample}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        viewport={"width": 1100, "height": 900},
        color_scheme="light",
        reduced_motion="reduce",
        service_workers="block",
    )
    try:
        page = context.new_page()
        page.on("request", lambda request: requests.append(request.url))
        started = time.perf_counter()
        page.goto(f"{base_url}/fixture.html", wait_until="load")
        fixture_load_ms = round((time.perf_counter() - started) * 1000, 3)
        fixture_semantics = fixture_checks(page, checks)
        fixture_screenshot = screenshot_digest(page, sample_dir / "fixture-after-reset.png")

        started = time.perf_counter()
        page.goto(f"{base_url}/harness.html", wait_until="load")
        code_mirror_load_ms = round((time.perf_counter() - started) * 1000, 3)
        harness_checks(page, checks)
        code_mirror_screenshot = screenshot_digest(page, sample_dir / "codemirror-initial.png")
        fallback = static_fallback_check(browser, base_url)
        for name, passed in fallback.items():
            expect(passed, name, checks)
        expect(all(url.startswith(base_url) for url in requests), "all-browser-requests-loopback-only", checks)
        return {
            "sample": sample,
            "outcome": "passed",
            "fixtureLoadMilliseconds": fixture_load_ms,
            "codeMirrorLoadMilliseconds": code_mirror_load_ms,
            "checks": checks,
            "semanticExposure": fixture_semantics,
            "loopbackRequests": sorted(set(requests)),
            "screenshotDigests": {"fixtureAfterReset": fixture_screenshot, "codeMirrorInitial": code_mirror_screenshot},
        }
    except Exception as error:
        return {"sample": sample, "outcome": "failed", "error": f"{type(error).__name__}: {error}", "checks": checks}
    finally:
        context.close()


def run_browser(launcher: BrowserType, family: str, vendor: str, executable: str, base_url: str, output: Path) -> dict[str, Any]:
    try:
        browser = launcher.launch(executable_path=executable, headless=True)
    except Exception as error:
        return {
            "browser": family,
            "vendor": vendor,
            "executable": executable,
            "expectedVersion": "150.0.7871.124" if family == "Chromium" else "152.0.4",
            "outcome": "blocked",
            "attemptedSamples": list(range(1, SAMPLES + 1)),
            "errorClass": "BrowserType.launch",
            "error": f"{type(error).__name__}: {error}",
            "workaroundApplied": "none",
        }
    try:
        samples = [run_sample(browser, base_url, output, family, sample) for sample in range(1, SAMPLES + 1)]
        return {"browser": family, "vendor": vendor, "executable": executable, "version": browser.version, "outcome": "passed" if all(sample["outcome"] == "passed" for sample in samples) else "failed", "samples": samples}
    finally:
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if importlib.metadata.version("playwright") != EXPECTED_PLAYWRIGHT:
        raise SystemExit(f"approved Playwright {EXPECTED_PLAYWRIGHT} is unavailable")
    fixture = args.fixture.resolve()
    experiment = args.experiment.resolve()
    node_modules = experiment / "node_modules"
    output = args.out.resolve()
    if not fixture.is_file() or not node_modules.is_dir():
        raise SystemExit("fixture and approved isolated node_modules are required")
    if output == output.parent or not str(output).startswith("/tmp/"):
        raise SystemExit("output directory must be isolated below /tmp")
    shutil.rmtree(output, ignore_errors=True)
    output.mkdir(parents=True, exist_ok=True)

    safety = local_fixture_safety(fixture)
    if safety["forbiddenFixtureTokens"] or not safety["fixtureContainsOnlyTrustedScript"] or not safety["hasExactVariantComparison"]:
        raise SystemExit(f"fixture safety contract failed: {safety}")
    imports, inventory = module_map(node_modules)
    missing = [package for package in DIRECT_PACKAGES if package not in imports]
    if missing:
        raise SystemExit(f"approved package root exports unavailable: {missing}")
    harness = output / "harness.html"
    harness.write_text(harness_html(imports), encoding="utf-8")
    server, thread, base_url = serve_local(fixture, node_modules, harness)
    try:
        with sync_playwright() as playwright:
            browser_runs = []
            for family, vendor, executable in BROWSERS:
                launcher = playwright.chromium if family == "Chromium" else playwright.firefox
                browser_runs.append(run_browser(launcher, family, vendor, executable, base_url, output))
    finally:
        server.shutdown()
        thread.join()
        server.server_close()

    outcomes = {run["browser"]: run["outcome"] for run in browser_runs}
    overall = "failed" if "failed" in outcomes.values() else "blocked" if "blocked" in outcomes.values() else "passed"
    results = {
        "spikeId": "SPK-J-CODE-EDITING",
        "classification": "observed browser behavior from synthetic local fixture and approved local package candidate",
        "nonProduction": True,
        "playwrightVersion": EXPECTED_PLAYWRIGHT,
        "fixture": {"path": str(fixture), "sha256": sha256_file(fixture), "bytes": fixture.stat().st_size},
        "runner": {"path": str(Path(__file__).resolve()), "sha256": sha256_file(Path(__file__).resolve())},
        "packageExperiment": {"path": str(experiment), "bytes": tree_size(experiment), "directPackages": list(DIRECT_PACKAGES), "inventory": inventory},
        "fixtureSafety": safety,
        "browserRuns": browser_runs,
        "result": overall,
    }
    results_path = output / "browser-results.json"
    write_json(results_path, results)
    manifest = {
        "spikeId": "SPK-J-CODE-EDITING",
        "fixtureSha256": sha256_file(fixture),
        "runnerSha256": sha256_file(Path(__file__).resolve()),
        "browserResults": {"path": str(results_path), "sha256": sha256_file(results_path)},
        "result": overall,
        "retainedArtifacts": "browser screenshots, temporary local harness, and raw results remain only in /tmp/spk-j-code-editing",
    }
    write_json(output / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 1 if overall == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
