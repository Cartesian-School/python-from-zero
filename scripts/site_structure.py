"""Walks the generated site/ tree and returns structured page records.

This is the single source of truth reused by build_seo_meta.py,
build_sitemap.py, and validate_navigation.py — so canonical URLs, sitemap
entries, and link-validation targets can never independently drift out of
sync with each other or with the actual generated HTML.

Only reads already-generated site/**/*.html — run the build_*.py page
generators first.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"

# Canonical production origin. Every canonical link, sitemap entry, and OG/
# JSON-LD url must be built from this — never a *.vercel.app preview host,
# the bare apex (cartesianschool.org), or localhost.
SITE_ORIGIN = "https://www.cartesianschool.org"

_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
_DESC_RE = re.compile(r'<meta\s+name="description"\s+content="(.*?)"\s*/?>', re.S)
_LANG_RE = re.compile(r'<html[^>]*\blang="([^"]*)"')


@dataclass
class PageRecord:
    path: Path  # absolute filesystem path under site/
    url_path: str  # site-root-relative path, e.g. "/chapters/glava-03/x.html"
    title: str | None
    description: str | None
    lang: str
    kind: str  # see _classify()

    @property
    def canonical_url(self) -> str:
        return SITE_ORIGIN + self.url_path


def _classify(url_path: str) -> str:
    if url_path == "/index.html":
        return "home"
    if url_path == "/predmetnyj-ukazatel.html":
        return "reference"
    if url_path.startswith("/front-matter/"):
        return "front-matter"
    if url_path.startswith("/practice/") and url_path.endswith("/index.html"):
        return "practice"
    if url_path.startswith("/practice/"):
        return "other"  # graders/, non-page assets under practice/
    if url_path.startswith("/chapters/") and url_path.endswith("/index.html"):
        return "chapter-opener"
    if url_path.startswith("/chapters/"):
        return "chapter-lesson"
    if url_path.startswith("/projects/") and url_path.endswith("/index.html"):
        return "project"
    if url_path.startswith("/projects/"):
        return "other"
    return "other"


def iter_pages() -> list[PageRecord]:
    records = []
    for path in sorted(SITE_DIR.rglob("*.html")):
        rel = path.relative_to(SITE_DIR)
        url_path = "/" + rel.as_posix()
        text = path.read_text(encoding="utf-8")
        title_m = _TITLE_RE.search(text)
        desc_m = _DESC_RE.search(text)
        lang_m = _LANG_RE.search(text)
        records.append(
            PageRecord(
                path=path,
                url_path=url_path,
                title=html.unescape(title_m.group(1)) if title_m else None,
                description=html.unescape(desc_m.group(1)) if desc_m else None,
                lang=lang_m.group(1) if lang_m else "ru",
                kind=_classify(url_path),
            )
        )
    return records
