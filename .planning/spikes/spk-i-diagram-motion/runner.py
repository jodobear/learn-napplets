#!/usr/bin/env python3
"""Measure the isolated SPK-I SVG with approved Playwright and installed browsers.

The fixture itself stays inert: this runner never evaluates learner content, injects a
script, or modifies browser launch configuration. It observes semantic DOM structure,
native keyboard navigation, static screenshots, and a static trusted-host sentinel.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import shutil
import time
import xml.etree.ElementTree as element_tree
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, BrowserType, Page, sync_playwright

EXPECTED_PLAYWRIGHT = "1.61.0"
EXPECTED_SENTINEL = "trusted-host-only-static"
SAMPLES = 5
BROWSERS = (
    ("Chromium", "Google Chrome", "/opt/google/chrome/google-chrome"),
    ("Firefox", "Mozilla Firefox", "/usr/bin/firefox"),
)
STEP_LINKS = (
    ("#step-compose", "step-compose"),
    ("#step-host", "step-host"),
    ("#step-result", "step-result"),
)
PARITY_LABELS = ("Compose", "Host sentinel", "Static result")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def static_fixture_safety(fixture: Path) -> dict[str, Any]:
    """Inspect the local XML fixture without interpreting any fixture-provided code."""
    root = element_tree.fromstring(fixture.read_bytes())
    script_elements: list[str] = []
    event_attributes: list[str] = []
    unsafe_links: list[str] = []
    for element in root.iter():
        local_name = element.tag.rsplit("}", 1)[-1]
        if local_name.lower() == "script":
            script_elements.append(local_name)
        for name, value in element.attrib.items():
            local_attribute = name.rsplit("}", 1)[-1]
            if local_attribute.lower().startswith("on"):
                event_attributes.append(local_attribute)
            if local_attribute == "href" and not value.startswith("#"):
                unsafe_links.append(value)
    return {
        "xmlParses": True,
        "scriptElementCount": len(script_elements),
        "eventAttributes": event_attributes,
        "unsafeHrefs": unsafe_links,
        "rootSentinel": root.attrib.get("data-trusted-host-sentinel"),
        "hostileInputIsEscapedText": "&lt;script&gt;window.__learnerInjection = true&lt;/script&gt;" in fixture.read_text(encoding="utf-8"),
    }


def expect(condition: bool, message: str, checks: dict[str, Any]) -> None:
    checks[message] = condition
    if not condition:
        raise AssertionError(message)


def screenshot(page: Page, path: Path) -> str:
    # The inert fixture has no animation elements; asking Playwright to disable animations
    # on a standalone SVG waits for an animation lifecycle that never fires in Chrome.
    # The viewport fully contains the fixed 1040×760 fixture. Avoid standalone-SVG
    # full-page capture, which Chrome cannot complete deterministically in this harness.
    image = page.screenshot(path=path, full_page=False, caret="hide", scale="css")
    return sha256_bytes(image)


def run_sample(
    browser: Browser,
    fixture_uri: str,
    output_dir: Path,
    family: str,
    sample: int,
    static_safety: dict[str, Any],
) -> dict[str, Any]:
    """Run one clean context with static and reduced-motion representations."""
    checks: dict[str, Any] = {}
    sample_dir = output_dir / family.lower() / f"sample-{sample}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        viewport={"width": 1100, "height": 820},
        color_scheme="light",
        reduced_motion="reduce",
        service_workers="block",
    )
    no_preference_context = None
    try:
        page = context.new_page()
        started = time.perf_counter()
        page.goto(fixture_uri, wait_until="load")
        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)

        root = page.locator("svg")
        expect(root.count() == 1, "one-svg-root", checks)
        expect(page.locator("title#fixture-title").count() == 1, "semantic-title-present", checks)
        expect(page.locator("desc#fixture-description").count() == 1, "semantic-description-present", checks)
        expect(root.get_attribute("data-trusted-host-sentinel") == EXPECTED_SENTINEL, "trusted-host-sentinel-unchanged", checks)
        expect(page.locator("script").count() == 0, "browser-dom-has-no-script-element", checks)
        expect(static_safety["scriptElementCount"] == 0, "xml-has-no-script-element", checks)
        expect(not static_safety["eventAttributes"], "xml-has-no-inline-event-handler", checks)
        expect(not static_safety["unsafeHrefs"], "xml-has-no-unsafe-href", checks)
        expect(static_safety["hostileInputIsEscapedText"], "hostile-input-remains-escaped-text", checks)
        expect(static_safety["rootSentinel"] == EXPECTED_SENTINEL, "static-sentinel-is-recorded", checks)

        transcript = page.locator("#transcript").text_content() or ""
        table = page.locator("#state-table").text_content() or ""
        visual = page.locator("#visual-flow").text_content() or ""
        expect(page.locator('#transcript[role="region"]').count() == 1, "transcript-region-exposed", checks)
        expect(page.locator('#state-table[role="table"]').count() == 1, "state-table-exposed", checks)
        for label in PARITY_LABELS:
            expect(label in visual and label in transcript and label in table, f"parity-{label.lower().replace(' ', '-')}", checks)

        initial_digest = screenshot(page, sample_dir / "initial-reduced-motion.png")
        keyboard_links: list[dict[str, str]] = []
        focus_digests: list[str] = []
        for index, (expected_href, expected_id) in enumerate(STEP_LINKS, start=1):
            page.goto(fixture_uri, wait_until="load")
            for _ in range(index):
                page.keyboard.press("Tab")
            focused = page.locator(":focus")
            actual_href = focused.get_attribute("href")
            expect(actual_href == expected_href, f"keyboard-tab-reaches-{expected_id}", checks)
            focus_digest = screenshot(page, sample_dir / f"focus-{index}.png")
            expect(focus_digest != initial_digest, f"visible-focus-{expected_id}", checks)
            page.keyboard.press("Enter")
            expect(page.url.endswith(expected_href), f"keyboard-enter-selects-{expected_id}", checks)
            keyboard_links.append({"href": actual_href or "", "target": expected_id})
            focus_digests.append(focus_digest)

        page.goto(fixture_uri, wait_until="load")
        reset_digest = screenshot(page, sample_dir / "reset-replay.png")
        expect(reset_digest == initial_digest, "reset-replay-matches-initial", checks)

        no_preference_context = browser.new_context(
            viewport={"width": 1100, "height": 820},
            color_scheme="light",
            reduced_motion="no-preference",
            service_workers="block",
        )
        no_preference_page = no_preference_context.new_page()
        no_preference_page.goto(fixture_uri, wait_until="load")
        no_preference_digest = screenshot(no_preference_page, sample_dir / "initial-no-preference.png")
        expect(no_preference_digest == initial_digest, "reduced-motion-static-equivalent", checks)
        expect(root.get_attribute("data-motion-policy") == "no-auto-loop; named-static-steps-only", "no-auto-loop-motion-policy", checks)

        return {
            "sample": sample,
            "outcome": "passed",
            "elapsedMilliseconds": elapsed_ms,
            "fixtureBytes": len(Path(fixture_uri.removeprefix("file://")).read_bytes()),
            "semanticExposure": {
                "title": True,
                "description": True,
                "transcriptRegion": True,
                "stateTable": True,
                "screenReaderSpeech": "not-observed; semantic DOM contract only",
            },
            "keyboardLinks": keyboard_links,
            "checks": checks,
            "screenshotDigests": {
                "initialReducedMotion": initial_digest,
                "focus": focus_digests,
                "resetReplay": reset_digest,
                "initialNoPreference": no_preference_digest,
            },
        }
    except Exception as error:
        return {
            "sample": sample,
            "outcome": "failed",
            "error": f"{type(error).__name__}: {error}",
            "checks": checks,
        }
    finally:
        if no_preference_context is not None:
            no_preference_context.close()
        context.close()


def run_browser(
    launcher: BrowserType,
    family: str,
    vendor: str,
    executable: str,
    fixture_uri: str,
    output_dir: Path,
    static_safety: dict[str, Any],
) -> dict[str, Any]:
    """Launch exactly the approved installed binary; do not add settings or retries."""
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
            "observedBehavior": "No fixture behavior was observed because the direct-installed browser did not retain a Playwright context.",
            "workaroundApplied": "none",
        }
    try:
        samples = [run_sample(browser, fixture_uri, output_dir, family, sample, static_safety) for sample in range(1, SAMPLES + 1)]
        return {
            "browser": family,
            "vendor": vendor,
            "executable": executable,
            "version": browser.version,
            "outcome": "passed" if all(sample["outcome"] == "passed" for sample in samples) else "failed",
            "samples": samples,
        }
    finally:
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if importlib.metadata.version("playwright") != EXPECTED_PLAYWRIGHT:
        raise SystemExit(f"approved Playwright {EXPECTED_PLAYWRIGHT} is unavailable")
    fixture = args.fixture.resolve()
    if not fixture.is_file():
        raise SystemExit(f"fixture does not exist: {fixture}")
    output_dir = args.out.resolve()
    if output_dir == output_dir.parent or not str(output_dir).startswith("/tmp/"):
        raise SystemExit("output directory must be an isolated /tmp path")
    shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    static_safety = static_fixture_safety(fixture)
    with sync_playwright() as playwright:
        results = []
        for family, vendor, executable in BROWSERS:
            launcher = playwright.chromium if family == "Chromium" else playwright.firefox
            results.append(run_browser(launcher, family, vendor, executable, fixture.as_uri(), output_dir, static_safety))

    outcomes = {result["browser"]: result["outcome"] for result in results}
    overall = "failed" if "failed" in outcomes.values() else "blocked" if "blocked" in outcomes.values() else "passed"
    browser_results = {
        "spikeId": "SPK-I-DIAGRAM-MOTION",
        "classification": "observed browser behavior from synthetic local fixture",
        "nonProduction": True,
        "playwrightVersion": EXPECTED_PLAYWRIGHT,
        "fixture": {"path": str(fixture), "sha256": sha256_file(fixture), "bytes": fixture.stat().st_size},
        "staticSafety": static_safety,
        "browserRuns": results,
        "result": overall,
    }
    results_path = output_dir / "browser-results.json"
    write_json(results_path, browser_results)
    manifest = {
        "spikeId": "SPK-I-DIAGRAM-MOTION",
        "fixtureSha256": sha256_file(fixture),
        "browserResults": {"path": str(results_path), "sha256": sha256_file(results_path)},
        "result": overall,
        "retainedArtifacts": "generated browser screenshots and raw results remain only in /tmp",
    }
    write_json(output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 1 if overall == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
