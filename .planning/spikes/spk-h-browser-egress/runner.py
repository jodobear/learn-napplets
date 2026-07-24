#!/usr/bin/env python3
"""Measure the disposable SPK-H local egress fixture with approved browsers only.

The runner starts an ephemeral loopback-only server, serves fixed fixture assets, and
records bounded request receipts. It never uses a public target, credential, browser
configuration, managed browser download, or production host surface.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.metadata
import json
import shutil
import socket
import struct
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Browser, BrowserType, sync_playwright

EXPECTED_PLAYWRIGHT = "1.61.0"
SAMPLES = 5
BROWSERS = (
    ("Chromium", "Google Chrome", "/opt/google/chrome/google-chrome", "150.0.7871.124"),
    ("Firefox", "Mozilla Firefox", "/usr/bin/firefox", "152.0.4"),
)
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL4jQAAAABJRU5ErkJggg==")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def tone_wav() -> bytes:
    """Return a fixed 100 ms PCM WAV sufficient for a metadata-load observation."""
    sample_rate = 8000
    samples = bytes([128] * (sample_rate // 10))
    header = b"RIFF" + struct.pack("<I", 36 + len(samples)) + b"WAVEfmt "
    header += struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate, 1, 8)
    return header + b"data" + struct.pack("<I", len(samples)) + samples


class LocalEgressServer(ThreadingHTTPServer):
    allow_reuse_address = True

    def __init__(self, fixture: Path) -> None:
        super().__init__(("127.0.0.1", 0), LocalEgressHandler)
        self.fixture = fixture
        self.receipts: list[dict[str, str | None]] = []
        self.receipt_lock = threading.Lock()

    @property
    def origin(self) -> str:
        return f"http://127.0.0.1:{self.server_port}"

    def record(self, handler: BaseHTTPRequestHandler) -> None:
        parsed = urlparse(handler.path)
        case = parse_qs(parsed.query).get("case", [None])[0]
        receipt = {
            "method": handler.command,
            "path": parsed.path,
            "case": case,
            "origin": handler.headers.get("Origin"),
            "referer": handler.headers.get("Referer"),
            "secFetchDest": handler.headers.get("Sec-Fetch-Dest"),
        }
        with self.receipt_lock:
            self.receipts.append(receipt)

    def matching_receipts(self, case: str) -> list[dict[str, str | None]]:
        with self.receipt_lock:
            return [receipt.copy() for receipt in self.receipts if receipt["case"] == case]


class LocalEgressHandler(BaseHTTPRequestHandler):
    server: LocalEgressServer

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "null")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_bytes(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, value: dict[str, Any]) -> None:
        self.send_bytes(200, "application/json; charset=utf-8", json.dumps(value, sort_keys=True).encode("utf-8"))

    def do_GET(self) -> None:
        self.server.record(self)
        parsed = urlparse(self.path)
        if parsed.path == "/fixture.html":
            self.send_bytes(200, "text/html; charset=utf-8", self.server.fixture.read_bytes())
        elif parsed.path == "/fetch":
            self.send_json({"ok": True, "endpoint": "local-fetch"})
        elif parsed.path == "/headers":
            self.send_json({
                "origin": self.headers.get("Origin"),
                "referer": self.headers.get("Referer"),
                "secFetchDest": self.headers.get("Sec-Fetch-Dest"),
            })
        elif parsed.path == "/pixel.png":
            self.send_bytes(200, "image/png", PNG)
        elif parsed.path == "/tone.wav":
            self.send_bytes(200, "audio/wav", tone_wav())
        elif parsed.path == "/classic.js":
            self.send_bytes(200, "text/javascript; charset=utf-8", b"window.__spkHClassicLoaded='local-classic-script';\n")
        elif parsed.path == "/module.js":
            self.send_bytes(200, "text/javascript; charset=utf-8", b"window.__spkHModuleLoaded='local-module-script'; export const spkHModule = true;\n")
        elif parsed.path == "/worker.js":
            self.send_bytes(200, "text/javascript; charset=utf-8", b"self.postMessage('local-worker-ok');\n")
        elif parsed.path == "/events":
            body = b"data: local-event-source-ok\n\n"
            self.send_bytes(200, "text/event-stream; charset=utf-8", body)
        elif parsed.path == "/socket" and self.headers.get("Upgrade", "").lower() == "websocket":
            self.websocket_reply()
        elif parsed.path == "/navigation":
            self.send_bytes(200, "text/plain; charset=utf-8", b"unexpected navigation receipt")
        else:
            self.send_bytes(404, "text/plain; charset=utf-8", b"not found")

    def do_POST(self) -> None:
        self.server.record(self)
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        if length:
            self.rfile.read(length)
        if parsed.path == "/form":
            self.send_bytes(204, "text/plain; charset=utf-8", b"")
        else:
            self.send_bytes(404, "text/plain; charset=utf-8", b"not found")

    def websocket_reply(self) -> None:
        key = self.headers.get("Sec-WebSocket-Key")
        if not key:
            self.send_bytes(400, "text/plain; charset=utf-8", b"missing websocket key")
            return
        accept = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()).decode("ascii")
        self.send_response(101, "Switching Protocols")
        self.send_header("Upgrade", "websocket")
        self.send_header("Connection", "Upgrade")
        self.send_header("Sec-WebSocket-Accept", accept)
        self.end_headers()
        self.connection.settimeout(2)
        try:
            header = self.connection.recv(2)
            if len(header) == 2:
                size = header[1] & 0x7F
                masked = bool(header[1] & 0x80)
                if size == 126:
                    size = struct.unpack("!H", self.connection.recv(2))[0]
                elif size == 127:
                    size = struct.unpack("!Q", self.connection.recv(8))[0]
                mask = self.connection.recv(4) if masked else b""
                payload = self.connection.recv(size) if size else b""
                if masked and len(mask) == 4:
                    _ = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
            response = b"local-websocket-ok"
            self.connection.sendall(bytes([0x81, len(response)]) + response)
        except (OSError, socket.timeout):
            return


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def channel_map(channels: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(channel.get("name")): channel for channel in channels}


def expect(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = condition
    if not condition:
        raise AssertionError(label)


def run_sample(browser: Browser, server: LocalEgressServer, family: str, sample: int) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    errors: list[str] = []
    context = browser.new_context()
    try:
        page = context.new_page()
        page.on("console", lambda message: errors.append(f"{message.type}:{message.text[:180]}"))
        case = f"{family.lower()}-{sample}"
        started = time.perf_counter()
        page.goto(f"{server.origin}/fixture.html?origin={server.origin}&sample={case}", wait_until="load")
        result = page.evaluate("() => window.runSpkHEgress()")
        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
        measurement = result["measurement"]
        negative = result["negativeCsp"]
        channels = channel_map(measurement["channels"])
        negative_channels = channel_map(negative["channels"])
        receipts = server.matching_receipts(case)
        negative_receipts = server.matching_receipts(f"{case}-negative")
        receipt_paths = {receipt["path"] for receipt in receipts}

        expect(measurement["sourceMapped"] is True and negative["sourceMapped"] is True, "top-level-source-maps-to-exact-iframe-window", checks)
        expect(channels.get("fetch", {}).get("status") == "fulfilled", "fetch-local-loopback-fulfilled", checks)
        expect(channels["fetch"]["value"]["status"] == 200 and channels["fetch"]["value"]["body"].get("ok") is True, "fetch-fixed-json-response", checks)
        expect(channels.get("images-media", {}).get("status") == "fulfilled", "image-and-media-local-load", checks)
        expect(channels["images-media"]["value"] == {"image": "loaded", "media": "loadedmetadata"}, "image-and-media-fixed-results", checks)
        expect(channels.get("classic-module-scripts", {}).get("status") == "fulfilled", "classic-and-module-scripts-loaded", checks)
        expect(channels["classic-module-scripts"]["value"] == {"classic": "local-classic-script", "module": "local-module-script"}, "classic-and-module-fixed-markers", checks)
        expect(channels.get("websocket", {}).get("value") == "local-websocket-ok", "websocket-fixed-roundtrip", checks)
        expect(channels.get("eventsource", {}).get("value") == "local-event-source-ok", "eventsource-fixed-message", checks)
        expect(channels.get("worker", {}).get("value") == "local-worker-ok", "worker-fixed-message", checks)
        expect(channels.get("referrer-origin", {}).get("status") == "fulfilled", "referrer-origin-endpoint-results-recorded", checks)
        expect(set((channels["referrer-origin"]["value"] or {}).keys()) == {"defaultHeaders", "noReferrerHeaders"}, "both-referrer-modes-recorded", checks)
        expect(channels.get("form-navigation", {}).get("status") == "observed", "form-navigation-attempt-recorded", checks)
        expect("/form" not in receipt_paths and "/navigation" not in receipt_paths, "sandbox-without-form-or-top-navigation-token-prevented-receipt", checks)
        expect({"/fetch", "/pixel.png", "/tone.wav", "/classic.js", "/module.js", "/socket", "/events", "/worker.js", "/headers"}.issubset(receipt_paths), "all-loopback-channel-endpoints-received", checks)
        expect(negative_channels.get("negative-fetch", {}).get("status") == "rejected", "semantic-negative-csp-rejects-fetch", checks)
        expect(negative_channels.get("negative-image", {}).get("status") == "rejected", "semantic-negative-csp-rejects-image", checks)
        expect(not negative_receipts, "semantic-negative-csp-prevents-local-endpoint-receipts", checks)
        expect(all(receipt["path"] != "/form" and receipt["path"] != "/navigation" for receipt in receipts), "no-form-or-navigation-receipt", checks)
        return {
            "sample": sample,
            "outcome": "passed",
            "elapsedMilliseconds": elapsed_ms,
            "fixtureResult": result,
            "endpointReceipts": receipts,
            "checks": checks,
            "console": errors,
        }
    except Exception as error:
        return {
            "sample": sample,
            "outcome": "failed",
            "error": f"{type(error).__name__}: {error}",
            "checks": checks,
            "console": errors,
        }
    finally:
        context.close()


def run_browser(launcher: BrowserType, family: str, vendor: str, executable: str, expected_version: str, server: LocalEgressServer) -> dict[str, Any]:
    try:
        browser = launcher.launch(executable_path=executable, headless=True)
    except Exception as error:
        return {
            "browser": family,
            "vendor": vendor,
            "executable": executable,
            "expectedVersion": expected_version,
            "outcome": "blocked",
            "attemptedSamples": list(range(1, SAMPLES + 1)),
            "affectedChannelGroups": ["fetch", "images-media", "classic-module-scripts", "websocket", "eventsource", "worker", "form-navigation", "referrer-origin"],
            "errorClass": "BrowserType.launch",
            "error": f"{type(error).__name__}: {error}",
            "observedBehavior": "No fixture behavior was observed because the direct-installed browser exited before Playwright attached to a clean context.",
            "workaroundApplied": "none",
        }
    try:
        samples = [run_sample(browser, server, family, sample) for sample in range(1, SAMPLES + 1)]
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
    output = args.out.resolve()
    if not fixture.is_file():
        raise SystemExit(f"fixture does not exist: {fixture}")
    if output == output.parent or not str(output).startswith("/tmp/"):
        raise SystemExit("output directory must be an isolated /tmp path")
    shutil.rmtree(output, ignore_errors=True)
    output.mkdir(parents=True, exist_ok=True)
    server = LocalEgressServer(fixture)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser_runs = []
            for family, vendor, executable, expected_version in BROWSERS:
                launcher = playwright.chromium if family == "Chromium" else playwright.firefox
                browser_runs.append(run_browser(launcher, family, vendor, executable, expected_version, server))
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
    outcomes = {run["browser"]: run["outcome"] for run in browser_runs}
    overall = "failed" if "failed" in outcomes.values() else "blocked" if "blocked" in outcomes.values() else "passed"
    browser_results = {
        "spikeId": "SPK-H-BROWSER-EGRESS",
        "classification": "observed browser behavior from an exact local sandbox/iframe fixture",
        "nonProduction": True,
        "playwrightVersion": EXPECTED_PLAYWRIGHT,
        "fixture": {"path": str(fixture), "sha256": sha256_file(fixture), "bytes": fixture.stat().st_size},
        "loopback": {"bindAddress": "127.0.0.1", "ephemeralPort": True, "publicProbe": False, "usedSecrets": False},
        "browserRuns": browser_runs,
        "result": overall,
    }
    results_path = output / "browser-results.json"
    write_json(results_path, browser_results)
    manifest = {
        "spikeId": "SPK-H-BROWSER-EGRESS",
        "fixtureSha256": sha256_file(fixture),
        "runnerSha256": sha256_file(Path(__file__).resolve()),
        "browserResults": {"path": str(results_path), "sha256": sha256_file(results_path)},
        "result": overall,
        "retainedArtifacts": "raw browser results remain only in /tmp/spk-h-browser-egress",
    }
    write_json(output / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 1 if overall == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
