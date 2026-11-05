#!/usr/bin/env python3
"""Serves the built page on localhost for development.

    tools/serve.py [--site build/debug/site] [--data ~/Games/Battlespire] [--port 8000]

With --data, the install is also served under /dev-data/ (with a manifest.json listing it), for the
page's ?dev mode: http://localhost:8000/?dev loads it without the folder picker, ?dev&cd with the CD
image, ?dev&args=--level,l1.bs6 passes options. Only ever on 127.0.0.1: this is not for hosting.
"""
import argparse
import functools
import http.server
import json
import os
import pathlib
import urllib.parse


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".wasm": "application/wasm"}

    def __init__(self, *args, data=None, **kwargs):
        self.data = data
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def translate_path(self, path):
        url = urllib.parse.urlparse(path).path
        if self.data and url.startswith("/dev-data/"):
            rel = urllib.parse.unquote(url[len("/dev-data/"):])
            return str((self.data / rel).resolve())
        return super().translate_path(path)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path).path
        if self.data and url.startswith("/dev-data/") and not pathlib.Path(self.translate_path(self.path)).is_relative_to(self.data):
            self.send_error(404)  # outside the install
            return
        if self.data and url == "/dev-data/manifest.json":
            files = []
            for root, _, names in os.walk(self.data):
                for name in names:
                    p = pathlib.Path(root, name)
                    files.append({"rel": p.relative_to(self.data).as_posix(), "size": p.stat().st_size})
            body = json.dumps(files).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", type=pathlib.Path, default=root / "build" / "debug" / "site")
    ap.add_argument("--data", type=pathlib.Path, default=os.environ.get("BS_DATA_DIR"))
    ap.add_argument("--port", type=int, default=8000)
    a = ap.parse_args()
    data = a.data.expanduser().resolve() if a.data else None
    handler = functools.partial(Handler, directory=str(a.site), data=data)
    with http.server.ThreadingHTTPServer(("127.0.0.1", a.port), handler) as server:
        print(f"http://localhost:{a.port}/" + (f"?dev  (install: {data})" if data else ""))
        server.serve_forever()


if __name__ == "__main__":
    main()
