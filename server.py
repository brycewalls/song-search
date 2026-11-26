#!/usr/bin/env python3
"""Tiny local server for the Song Search player.

Serves the files in this folder and saves marks to progress.json, so the
marks survive closing the browser and Claude can read them later.
Listens on this computer only (127.0.0.1).
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRESS = os.path.join(HERE, "progress.json")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8797


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def _send_json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/progress":
            try:
                with open(PROGRESS, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (OSError, ValueError):
                data = {}
            return self._send_json(200, data)
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/progress":
            return self._send_json(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2_000_000:
                return self._send_json(413, {"error": "too large"})
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("progress must be an object")
        except (ValueError, UnicodeDecodeError) as exc:
            return self._send_json(400, {"error": str(exc)})
        tmp = PROGRESS + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=0)
        os.replace(tmp, PROGRESS)
        return self._send_json(200, {"saved": len(data)})

    def end_headers(self):
        if self.path.endswith((".html", ".json", "/")):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Song Search player running at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
