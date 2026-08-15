#!/usr/bin/env python3
"""Build-time SEO validator.

Checks, across the built dist/ tree (or site/ for a quick local check):

- every page has exactly one <title>,
- every page has a <meta name="description">,
- every page has exactly one canonical link, using https://www.cartesianschool.org,
- every page has the core Open Graph fields,
- every <script type="application/ld+json"> block parses as valid JSON,
- sitemap.xml contains only https://www.cartesianschool.org URLs,
- robots.txt references the canonical sitemap URL.

Usage: python3 scripts/validate_seo.py [dist_dir]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL_ORIGIN = "https://www.cartesianschool.org"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="(.*?)"\s*/?>', re.S)
CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"\s*/?>')
OG_RE = {
    "og:type": re.compile(r'<meta\s+property="og:type"'),
    "og:site_name": re.compile(r'<meta\s+property="og:site_name"'),
    "og:title": re.compile(r'<meta\s+property="og:title"'),
    "og:description": re.compile(r'<meta\s+property="og:description"'),
    "og:url": re.compile(r'<meta\s+property="og:url"'),
    "og:image": re.compile(r'<meta\s+property="og:image"'),
}
JSON_LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

# projects/ contains standalone example project source (including raw Jinja2
# templates with a .html extension) — not real generated site pages, so they
# carry none of this metadata and shouldn't be validated as if they did.
EXCLUDED_DIRS = {"projects"}


def validate_page(file: Path, base_dir: Path) -> list[str]:
    rel = file.relative_to(base_dir)
    text = file.read_text(encoding="utf-8")
    errors = []

    titles = TITLE_RE.findall(text)
    if len(titles) != 1:
        errors.append(f"{rel}: expected exactly 1 <title>, found {len(titles)}")

    if not DESC_RE.search(text):
        errors.append(f"{rel}: missing <meta name=\"description\">")

    canonicals = CANONICAL_RE.findall(text)
    if len(canonicals) != 1:
        errors.append(f"{rel}: expected exactly 1 canonical link, found {len(canonicals)}")
    else:
        canonical = canonicals[0]
        if not canonical.startswith(CANONICAL_ORIGIN + "/"):
            errors.append(f"{rel}: canonical does not use {CANONICAL_ORIGIN}: {canonical}")

    for field, pattern in OG_RE.items():
        if not pattern.search(text):
            errors.append(f"{rel}: missing {field}")

    for block in JSON_LD_RE.findall(text):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON-LD ({exc})")

    return errors


def validate_sitemap(base_dir: Path) -> list[str]:
    errors = []
    sitemap = base_dir / "sitemap.xml"
    if not sitemap.exists():
        return [f"sitemap.xml missing at {sitemap}"]
    text = sitemap.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>(.*?)</loc>", text)
    if not locs:
        errors.append("sitemap.xml contains no <loc> entries")
    for loc in locs:
        if not loc.startswith(CANONICAL_ORIGIN + "/"):
            errors.append(f"sitemap.xml: non-canonical URL: {loc}")
    return errors


def validate_robots(base_dir: Path) -> list[str]:
    errors = []
    robots = base_dir / "robots.txt"
    if not robots.exists():
        return [f"robots.txt missing at {robots}"]
    text = robots.read_text(encoding="utf-8")
    expected = f"Sitemap: {CANONICAL_ORIGIN}/sitemap.xml"
    if expected not in text:
        errors.append(f'robots.txt does not reference "{expected}"')
    return errors


def main() -> None:
    base_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "site"
    if not base_dir.exists():
        print(f"Directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    errors: list[str] = []
    pages = [
        f
        for f in sorted(base_dir.rglob("*.html"))
        if f.relative_to(base_dir).parts[0] not in EXCLUDED_DIRS
    ]
    for page in pages:
        errors += validate_page(page, base_dir)
    errors += validate_sitemap(base_dir)
    errors += validate_robots(base_dir)

    if errors:
        print(f"SEO validation failed — {len(errors)} problem(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"SEO OK: {len(pages)} pages, sitemap.xml, and robots.txt all valid.")


if __name__ == "__main__":
    main()
