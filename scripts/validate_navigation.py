#!/usr/bin/env python3
"""Build-time navigation validator.

Walks every generated *.html page (in the built dist/ tree by default — the
actual deployed structure, since notebooks/book/projects are copied in as
siblings of site/'s own contents, not literally present under site/) and
fails the build if any href:

- points at a local file/page that does not exist,
- has a #fragment that does not match any id="..." on its target page,
- points at localhost, a *.vercel.app preview host, or the bare apex
  (cartesianschool.org instead of www.cartesianschool.org),
- (informational) duplicate ids within a single page, which make fragment
  navigation to that id ambiguous.

Usage: python3 scripts/validate_navigation.py [dist_dir]
Defaults to site/ (useful for a quick check without a full build).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

# Only match href inside a real <a ...> or <link ...> tag — not a bare
# `href="..."` substring anywhere in the text, which would also match escaped
# HTML-syntax examples in the book's own teaching prose
# (e.g. "<code>&lt;a href=&quot;...&quot;&gt;</code>" describing HTML to
# a student — that's not a real link, and &lt; means there's no literal "<"
# for this pattern to anchor on).
HREF_RE = re.compile(r'<(?:a|link)\s[^>]*?\bhref="([^"]*)"')

# Real id="..." attributes only — a lookbehind excludes "data-lesson-id=" and
# similar suffixed attributes, which a bare `id="` match would wrongly treat
# as a fragment target.
ID_RE = re.compile(r'(?<![\w-])id="([^"]*)"')

# Only the site's own generated pages are navigation to validate — not
# standalone example project source (e.g. projects/flask/*/templates/*.html
# are raw Jinja2 templates with {{ ... }} syntax, never rendered as real
# HTML, and not part of the site's own link graph).
EXCLUDED_DIRS = {"projects"}

DISALLOWED_HOSTS_SUFFIX = (".vercel.app",)
DISALLOWED_HOSTS_EXACT = {"localhost", "127.0.0.1", "cartesianschool.org"}
CANONICAL_HOST = "www.cartesianschool.org"

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:")


def _ids_in(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(ID_RE.findall(path.read_text(encoding="utf-8")))


def _resolve_internal(href_path: str, current_file: Path, base_dir: Path) -> Path:
    if href_path in ("", "/"):
        href_path = "/index.html"
    if href_path.startswith("/"):
        target = (base_dir / href_path.lstrip("/")).resolve()
    else:
        target = (current_file.parent / href_path).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target


def validate(base_dir: Path) -> list[str]:
    errors: list[str] = []
    html_files = [
        f
        for f in sorted(base_dir.rglob("*.html"))
        if f.relative_to(base_dir).parts[0] not in EXCLUDED_DIRS
    ]
    id_cache: dict[Path, set[str]] = {}

    def ids_of(path: Path) -> set[str]:
        if path not in id_cache:
            id_cache[path] = _ids_in(path)
        return id_cache[path]

    for file in html_files:
        rel = file.relative_to(base_dir)
        text = file.read_text(encoding="utf-8")

        # Duplicate ids within this one page.
        all_ids = ID_RE.findall(text)
        seen: set[str] = set()
        for i in all_ids:
            if i in seen:
                errors.append(f"{rel}: duplicate id=\"{i}\" on the same page (ambiguous fragment target)")
            seen.add(i)

        for href in HREF_RE.findall(text):
            if not href or href.startswith(SKIP_SCHEMES):
                continue
            if href == "#":
                continue

            if href.startswith("http://") or href.startswith("https://"):
                parsed = urlsplit(href)
                host = parsed.hostname or ""
                if host in DISALLOWED_HOSTS_EXACT or host.endswith(DISALLOWED_HOSTS_SUFFIX):
                    errors.append(f"{rel}: non-canonical/preview host in href: {href}")
                    continue
                if host != CANONICAL_HOST:
                    continue  # genuinely external link (fonts, docs, etc.) — not ours to validate
                # www.cartesianschool.org link — validate as internal below
                href_path = parsed.path or "/"
                fragment = parsed.fragment
            else:
                href_path, _, fragment = href.partition("#")

            # Percent-encoded paths (e.g. non-ASCII filenames like "готовая
            # книга.pdf") must be decoded before filesystem lookup — the URL
            # component is encoded, the file on disk is not.
            target = _resolve_internal(unquote(href_path), file, base_dir)
            if not target.exists():
                shown = target.relative_to(base_dir) if base_dir in target.parents else target
                errors.append(f'{rel}: href="{href}" -> missing file {shown}')
                continue

            if fragment and target.suffix == ".html":
                if fragment not in ids_of(target):
                    errors.append(f'{rel}: href="{href}" -> #{fragment} not found in {target.relative_to(base_dir)}')

    return errors


def main() -> None:
    base_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "site"
    if not base_dir.exists():
        print(f"Directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    errors = validate(base_dir)
    if errors:
        print(f"Navigation validation failed — {len(errors)} problem(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    html_count = len(
        [f for f in base_dir.rglob("*.html") if f.relative_to(base_dir).parts[0] not in EXCLUDED_DIRS]
    )
    print(f"Navigation OK: {html_count} pages checked against {base_dir}, no broken links or fragments.")


if __name__ == "__main__":
    main()
