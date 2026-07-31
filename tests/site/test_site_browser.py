"""Bounded local Chromium checks for the generated static learning site."""

from __future__ import annotations

import contextlib
import http.server
import shutil
import subprocess
import sys
import threading
import unittest
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import Browser, Page, Playwright, sync_playwright


ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "site" / "dist"
BUILDER = ROOT / "tools" / "build-site.py"
README = ROOT / "site" / "README.md"


class QuietStaticHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class SiteBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        built = subprocess.run(
            [sys.executable, str(BUILDER)], cwd=ROOT, text=True, capture_output=True, check=False
        )
        if built.returncode:
            raise RuntimeError(f"site build failed before browser checks:\n{built.stderr}")

        handler = lambda *args, **kwargs: QuietStaticHandler(*args, directory=str(DIST), **kwargs)
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = f"http://127.0.0.1:{cls.server.server_port}"

        chrome = shutil.which("google-chrome")
        if not chrome:
            raise RuntimeError("approved Google Chrome executable is unavailable")
        cls.playwright: Playwright = sync_playwright().start()
        cls.browser: Browser = cls.playwright.chromium.launch(headless=True, executable_path=chrome)

    @classmethod
    def tearDownClass(cls) -> None:
        with contextlib.suppress(Exception):
            cls.browser.close()
        with contextlib.suppress(Exception):
            cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def page(self, *, width: int, javascript_enabled: bool = True, reduced_motion: str = "no-preference") -> tuple[object, Page]:
        context = self.browser.new_context(
            viewport={"width": width, "height": 900},
            java_script_enabled=javascript_enabled,
            reduced_motion=reduced_motion,
        )
        return context, context.new_page()

    def assert_local_requests(self, requested: list[str]) -> None:
        for request_url in requested:
            parsed = urlparse(request_url)
            if parsed.scheme in {"data", "about"}:
                continue
            self.assertEqual(parsed.netloc, urlparse(self.origin).netloc, request_url)

    def test_desktop_learning_path_has_local_routes_and_keyboard_order(self) -> None:
        context, page = self.page(width=1440)
        try:
            requested: list[str] = []
            page.on("request", lambda request: requested.append(request.url))
            for route in ("/", "/learn/", "/architecture/", "/sources/"):
                response = page.goto(f"{self.origin}{route}", wait_until="networkidle")
                self.assertIsNotNone(response)
                self.assertEqual(response.status, 200, route)

            page.goto(f"{self.origin}/", wait_until="networkidle")
            focused: list[str] = []
            for _ in range(10):
                page.keyboard.press("Tab")
                focused.append(page.evaluate("document.activeElement && document.activeElement.href"))
            self.assertEqual(focused[0], f"{self.origin}/#main-content")
            self.assertIn(f"{self.origin}/learn/", focused)
            self.assertIn(f"{self.origin}/sources/", focused)
            self.assertGreater(page.locator("main").count(), 0)
            self.assertGreater(page.locator("nav[aria-label='Primary navigation']").count(), 0)
            self.assert_local_requests(requested)
        finally:
            context.close()

    def test_mobile_no_script_architecture_keeps_transcript_table_and_source_links(self) -> None:
        context, page = self.page(width=320, javascript_enabled=False)
        try:
            response = page.goto(f"{self.origin}/architecture/", wait_until="networkidle")
            self.assertIsNotNone(response)
            self.assertEqual(response.status, 200)
            self.assertEqual(
                page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"), True
            )
            self.assertGreater(page.locator(".authority-diagram").count(), 0)
            self.assertGreater(page.locator("#architecture-transcript").count(), 0)
            self.assertGreater(page.locator("table").count(), 0)
            self.assertGreater(page.locator(".relationship-steps li").count(), 3)
            self.assertGreater(page.locator("a[href*='sources/index.html#source-']").count(), 0)
            self.assertEqual(page.locator("[data-reading-trace]").count(), 0)
        finally:
            context.close()

    def test_reduced_motion_and_optional_trace_controls_are_operable(self) -> None:
        context, page = self.page(width=1024, reduced_motion="reduce")
        try:
            page.goto(f"{self.origin}/architecture/", wait_until="networkidle")
            self.assertEqual(page.evaluate("getComputedStyle(document.documentElement).scrollBehavior"), "auto")
            self.assertEqual(page.locator("[data-reading-trace]").count(), 1)
            page.locator("[data-trace-replay]").click()
            self.assertTrue(page.locator(".transcript").evaluate("element => element.open"))
            page.locator("[data-trace-reset]").click()
            self.assertIn("Trace reset", page.locator("#trace-status").inner_text())
        finally:
            context.close()

    def test_readme_documents_the_stdlib_local_preview_contract(self) -> None:
        instructions = README.read_text(encoding="utf-8")
        self.assertIn("python3 -m http.server", instructions)
        self.assertIn("python3 tools/build-site.py", instructions)
        self.assertIn("http://127.0.0.1:", instructions)
        self.assertNotIn("npm", instructions.lower())


if __name__ == "__main__":
    unittest.main()
