from __future__ import annotations

import os
import subprocess
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "playwright"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def _start_server(port: int = 8001) -> ThreadingHTTPServer:
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("", port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def _pwcli() -> str:
    codex_home = os.environ.get("CODEX_HOME") or str(Path.home() / ".codex")
    return str(Path(codex_home) / "skills" / "playwright" / "scripts" / "playwright_cli.sh")


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    server = _start_server()
    try:
        pwcli = _pwcli()
        base = "http://localhost:8001"
        _run([pwcli, "open", f"{base}/outputs/trace_swimlane.html", "--headed"])
        _run([pwcli, "screenshot", "--filename", str(OUT_DIR / "trace_swimlane.png"), "--full-page"])
        _run([pwcli, "goto", f"{base}/outputs/trace_timeline.html"])
        _run([pwcli, "screenshot", "--filename", str(OUT_DIR / "trace_timeline.png"), "--full-page"])
        _run([pwcli, "goto", f"{base}/outputs/trace.html"])
        _run([pwcli, "screenshot", "--filename", str(OUT_DIR / "trace_table.png"), "--full-page"])
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
