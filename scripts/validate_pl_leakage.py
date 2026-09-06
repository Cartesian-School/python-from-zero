#!/usr/bin/env python3
"""Fail closed on Cyrillic text in any approved PL page's visible content,
accessibility attributes, or runtime-visible <script> literals (practice
config titles, manual-completion UI strings, JSON-LD SEO payloads). Also
checks PL notebook Markdown prose and code-comment lines. Zero exceptions in
this milestone: the allowlist (manifest/i18n/pl_leakage_allowlist.json, if
present) must stay empty.

<script> content is intentionally NOT exempted like <code>/<pre>: this
codebase never embeds a protected Cyrillic literal in executable JS (config
values, identifiers, and enum-like strings are all ASCII by construction —
see build_polish_course.py's TranslationMemory), so any Cyrillic inside a
<script> block on an approved PL page is leaked human-facing text, not a
protected payload. An earlier version of this validator decomposed <script>
tags before scanning, which produced a false PASS on real leakage (config
chapterTitle/lessonTitle, manual-completion status/button/confirm text) —
see the regression tests in tests/test_pl_shell.py.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bs4 import BeautifulSoup
from localization import MANIFEST_DIR, PUBLISHABLE_STATES, ROOT, Routes, read_json

CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]+")
LEAKY_ATTRS = ("aria-label", "aria-description", "title", "alt", "placeholder")
ALLOWLIST_PATH = MANIFEST_DIR / "pl_leakage_allowlist.json"
PRACTICE_MANIFEST = ROOT / "manifest/practice_manifest.json"

# Executable code samples are protected payloads: an inline/block code
# example may legitimately show Cyrillic as expected program output. They
# are in scope for the M02-I05 linguistic audit, not this leakage gate.
_PROTECTED_TAGS = ("style", "code", "pre")

_MD_PROTECTED = re.compile(r"(`+[^`]*`+|https?://[^\s)>]+)")
_CODE_COMMENT = re.compile(r"^(\s*#\s*)(.*)$")
_CODE_COMMENT_EXEMPT = re.compile(r"noqa|type:\s*ignore|pragma|doctest")


def _allowlist() -> set[str]:
    if not ALLOWLIST_PATH.is_file():
        return set()
    return set(read_json(ALLOWLIST_PATH).get("allowed_strings", []))


def find_leaks(html: str, allowlist: set[str]) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    # BeautifulSoup's get_text() already excludes <script>/<style> content
    # regardless of decompose(); scan script bodies explicitly below so
    # runtime-visible literals (practice config titles, manual-completion
    # UI text, JSON-LD SEO payloads) can't hide from this check the way an
    # earlier version of this validator let them.
    scripts = [tag.string or tag.get_text() for tag in soup.find_all("script")]
    for tag in soup(list(_PROTECTED_TAGS)):
        tag.decompose()

    hits: list[str] = []
    for match in CYRILLIC_RE.finditer(soup.get_text()):
        if match.group(0) not in allowlist:
            hits.append(match.group(0))
    for script_text in scripts:
        for match in CYRILLIC_RE.finditer(script_text or ""):
            if match.group(0) not in allowlist:
                hits.append(f"<script>: {match.group(0)!r}")
    for tag in soup.find_all(True):
        for attr in LEAKY_ATTRS:
            value = tag.get(attr)
            if not value:
                continue
            for match in CYRILLIC_RE.finditer(value):
                if match.group(0) not in allowlist:
                    hits.append(f"{attr}={match.group(0)!r}")
    return hits


def find_notebook_leaks(notebook: dict, allowlist: set[str]) -> list[str]:
    hits: list[str] = []
    for cell in notebook.get("cells", []):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "markdown":
            fenced = False
            for line in source.splitlines():
                if line.lstrip().startswith("```"):
                    fenced = not fenced
                    continue
                if fenced:
                    continue
                for piece in _MD_PROTECTED.split(line)[::2]:
                    for match in CYRILLIC_RE.finditer(piece):
                        if match.group(0) not in allowlist:
                            hits.append(f"markdown: {match.group(0)!r}")
        elif cell.get("cell_type") == "code":
            for line in source.splitlines():
                match = _CODE_COMMENT.match(line)
                if match and not _CODE_COMMENT_EXEMPT.search(line):
                    for cm in CYRILLIC_RE.finditer(match.group(2)):
                        if cm.group(0) not in allowlist:
                            hits.append(f"code-comment: {cm.group(0)!r}")
    return hits


def validate() -> int:
    allowlist = _allowlist()
    routes = Routes()
    checked = 0
    failures: list[str] = []

    for page_id, page in routes.pages.items():
        variant = page["variants"].get("pl")
        if not variant or variant["status"] not in PUBLISHABLE_STATES:
            continue
        path = ROOT / "site" / variant["path"].lstrip("/")
        if not path.is_file():
            continue
        hits = find_leaks(path.read_text(encoding="utf-8"), allowlist)
        checked += 1
        if hits:
            failures.append(f"{variant['path']}: {hits}")

    practice_manifest = read_json(PRACTICE_MANIFEST) if PRACTICE_MANIFEST.is_file() else {}
    for practice_id, entry in sorted(practice_manifest.items()):
        notebook_path = ROOT / "site/pl/notebooks" / entry["notebook"]
        if not notebook_path.is_file():
            continue
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        hits = find_notebook_leaks(notebook, allowlist)
        checked += 1
        if hits:
            failures.append(f"pl/notebooks/{entry['notebook']}: {hits}")

    if failures:
        for failure in failures:
            print(f"LEAK: {failure}")
        raise AssertionError(f"Russian leakage found on {len(failures)} approved PL page(s)")

    print(f"PASS: zero Cyrillic leakage across {checked} approved PL page(s)")
    return checked


if __name__ == "__main__":
    validate()
