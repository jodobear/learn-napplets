#!/usr/bin/env python3
"""Run the isolated SPK-C fixture with approved Playwright and installed browsers."""

from __future__ import annotations

import importlib.metadata
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

FIXTURE = (Path(__file__).resolve().parent / "fixture.html").as_uri()
BROWSERS = (
    ("Chromium", "Google Chrome", "/opt/google/chrome/google-chrome"),
    ("Firefox", "Mozilla Firefox", "/usr/bin/firefox"),
)


def valid(result: dict) -> bool:
    scenarios = {item["scenario"]: item for item in result["scenarios"]}
    present = scenarios.get("declared-domain-present", {})
    removed = scenarios.get("declared-domain-removed", {})
    return (
        present.get("ready", {}).get("injectionPhase") == "pre-guest-script"
        and present.get("ready", {}).get("declaredDomainPresent") is True
        and present.get("sourceMapped") is True
        and present.get("response", {}).get("ok") is True
        and present.get("response", {}).get("result") == "local-service-ok"
        and removed.get("ready", {}).get("injectionPhase") == "pre-guest-script"
        and removed.get("ready", {}).get("declaredDomainPresent") is False
        and removed.get("sourceMapped") is True
        and removed.get("response", {}).get("ok") is False
        and removed.get("response", {}).get("error") == "declared-domain-missing"
    )


def main() -> int:
    if importlib.metadata.version("playwright") != "1.61.0":
        raise SystemExit("approved Playwright 1.61.0 is unavailable")

    runs = []
    with sync_playwright() as playwright:
        for family, vendor, executable in BROWSERS:
            launcher = playwright.chromium if family == "Chromium" else playwright.firefox
            try:
                browser = launcher.launch(executable_path=executable, headless=True)
            except Exception as error:
                runs.extend(
                    {
                        "browser": family,
                        "vendor": vendor,
                        "browserVersion": "launch-unavailable",
                        "sample": sample,
                        "elapsedMilliseconds": 0.0,
                        "outcome": "blocked",
                        "error": f"{type(error).__name__}: {error}",
                    }
                    for sample in range(1, 6)
                )
                continue
            try:
                for sample in range(1, 6):
                    context = browser.new_context()
                    page = context.new_page()
                    started = time.perf_counter()
                    try:
                        page.goto(FIXTURE, wait_until="load")
                        result = page.evaluate("() => window.runBoundaryHarness()")
                        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
                        runs.append(
                            {
                                "browser": family,
                                "vendor": vendor,
                                "browserVersion": browser.version,
                                "sample": sample,
                                "elapsedMilliseconds": elapsed_ms,
                                "outcome": "passed" if valid(result) else "failed",
                                "result": result,
                            }
                        )
                    except Exception as error:
                        runs.append(
                            {
                                "browser": family,
                                "vendor": vendor,
                                "browserVersion": browser.version,
                                "sample": sample,
                                "elapsedMilliseconds": round((time.perf_counter() - started) * 1000, 3),
                                "outcome": "failed",
                                "error": f"{type(error).__name__}: {error}",
                            }
                        )
                    finally:
                        context.close()
            finally:
                browser.close()

    print(json.dumps({"playwrightVersion": importlib.metadata.version("playwright"), "fixture": FIXTURE, "runs": runs}, indent=2))
    return 0 if all(run["outcome"] == "passed" for run in runs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
