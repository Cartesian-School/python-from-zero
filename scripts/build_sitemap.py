#!/usr/bin/env python3
"""Generates site/sitemap.xml from the actual generated site structure
(site_structure.py) — not a hand-maintained URL list, so it can't drift out
of sync with the real pages.

Practice pages are intentionally excluded: they are thin application shells
around notebook content already represented on their parent theory page (see
build_seo_meta.py, which also marks them noindex,follow) — including them
would just add near-duplicate, low-value URLs to the index.
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_structure import SITE_DIR, SITE_ORIGIN, iter_pages
from localization import Routes

EXCLUDED_KINDS = {"practice", "other"}
OUT_PATH = SITE_DIR / "sitemap.xml"


def main() -> None:
    routes = Routes()
    pages = [p for p in iter_pages()
             if p.kind not in EXCLUDED_KINDS and routes.publishable_path(p.url_path)]
    bilingual = any(routes.alternates(p.url_path) for p in pages)
    namespace = ' xmlns:xhtml="http://www.w3.org/1999/xhtml"' if bilingual else ""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"{namespace}>',
    ]
    for p in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(p.canonical_url)}</loc>")
        for locale, path in routes.alternates(p.url_path).items():
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{locale}" href="{escape(SITE_ORIGIN + path)}" />')
        lines.append("  </url>")
    lines.append("</urlset>")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"sitemap.xml: {len(pages)} URL(ов) записано в {OUT_PATH.relative_to(SITE_DIR.parent)}")


if __name__ == "__main__":
    main()
