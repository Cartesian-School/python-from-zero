#!/usr/bin/env python3
"""Static file server for local testing that mirrors vercel.json's
site-wide Cross-Origin-Opener-Policy / Cross-Origin-Embedder-Policy headers,
so SharedArrayBuffer (needed by the input() bridge) is available locally
exactly as it is in production. Must be site-wide, not just /practice/**:
Chromium requires a Worker's own script response to carry a compatible
COEP header too whenever the page that spawns it has one set, and the
shared worker script lives under /assets/js/, not /practice/.

Usage: python3 scripts/dev_server.py <port> [directory]
"""
import http.server
import sys


class CrossOriginIsolatedHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    directory = sys.argv[2] if len(sys.argv) > 2 else "."
    handler = lambda *args, **kwargs: CrossOriginIsolatedHandler(*args, directory=directory, **kwargs)
    http.server.ThreadingHTTPServer(("", port), handler).serve_forever()
