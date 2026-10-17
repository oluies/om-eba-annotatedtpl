"""A static server that speaks byte ranges and logs what each request pulled.

Python's SimpleHTTPRequestHandler does not do ranges, and the whole point of the spike
is to measure them, so this does the minimum: 206 with Content-Range, CORS for the
worker, and one log line per request with the byte count.
"""

import http.server
import re
import socketserver
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8099
SERVED: list[tuple[str, int]] = []


class Ranged(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _file(self) -> Path | None:
        target = (ROOT / self.path.lstrip("/").split("?")[0]).resolve()
        return target if target.is_file() and ROOT in target.parents else None

    TYPES = {
        ".html": "text/html; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json",
        ".parquet": "application/vnd.apache.parquet",
        ".wasm": "application/wasm",
    }

    def _type(self, target: Path) -> None:
        # A module script with no Content-Type is refused outright: "Expected a
        # JavaScript-or-Wasm module script but the server responded with a MIME type
        # of ''". GitHub Pages sets these; this test server has to as well.
        self.send_header("Content-Type", self.TYPES.get(target.suffix, "application/octet-stream"))

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Expose-Headers", "content-length, content-range, accept-ranges")
        self.send_header("Accept-Ranges", "bytes")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors()
        self.send_header("Access-Control-Allow-Headers", "range")
        self.end_headers()

    def do_HEAD(self) -> None:
        target = self._file()
        if not target:
            self.send_error(404)
            return
        self.send_response(200)
        self._cors()
        self._type(target)
        self.send_header("Content-Length", str(target.stat().st_size))
        self.end_headers()

    def do_GET(self) -> None:
        target = self._file()
        if not target:
            self.send_error(404)
            return
        size = target.stat().st_size
        found = re.match(r"bytes=(\d+)-(\d*)", self.headers.get("Range", ""))
        if found:
            start = int(found.group(1))
            end = int(found.group(2)) if found.group(2) else size - 1
            end = min(end, size - 1)
            body = target.read_bytes()[start : end + 1]
            self.send_response(206)
            self._cors()
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            body = target.read_bytes()
            self.send_response(200)
            self._cors()
        self._type(target)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        SERVED.append((target.name, len(body)))
        print(f"  {len(body):>9,} B  {target.name}  {self.headers.get('Range', 'whole file')}", file=sys.stderr)

    def log_message(self, format: str, *args: object) -> None:
        # The per-request line above is the log; the default one would double it.
        pass


with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Ranged) as httpd:
    httpd.allow_reuse_address = True
    print(f"serving {ROOT} on {PORT}", file=sys.stderr)
    httpd.serve_forever()
