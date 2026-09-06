#!/usr/bin/env python3
"""Fail closed on Cyrillic text in any approved PL page's visible content or
accessibility attributes. Zero exceptions in this milestone: the allowlist
(manifest/i18n/pl_leakage_allowlist.json, if present) must stay empty.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bs4 import BeautifulSoup
from localization import MANIFEST_DIR, ROOT, Routes, read_json

CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]+")
LEAKY_ATTRS = ("aria-label", "title", "alt", "placeholder")
ALLOWLIST_PATH = MANIFEST_DIR / "pl_leakage_allowlist.json"


def _allowlist() -> set[str]:
    if not ALLOWLIST_PATH.is_file():
        return set()
    return set(read_json(ALLOWLIST_PATH).get("allowed_strings", []))


def find_leaks(html: str, allowlist: set[str]) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    hits: list[str] = []
    for match in CYRILLIC_RE.finditer(soup.get_text()):
        if match.group(0) not in allowlist:
            hits.append(match.group(0))
    for tag in soup.find_all(True):
        for attr in LEAKY_ATTRS:
            value = tag.get(attr)
            if not value:
                continue
            for match in CYRILLIC_RE.finditer(value):
                if match.group(0) not in allowlist:
                    hits.append(f"{attr}={match.group(0)!r}")
    return hits


def validate() -> int:
    allowlist = _allowlist()
    routes = Routes()
    checked = 0
    failures: list[str] = []

    for page_id, page in routes.pages.items():
        variant = page["variants"].get("pl")
        if not variant or variant["status"] != "approved":
            continue
        path = ROOT / "site" / variant["path"].lstrip("/")
        if not path.is_file():
            continue
        hits = find_leaks(path.read_text(encoding="utf-8"), allowlist)
        checked += 1
        if hits:
            failures.append(f"{variant['path']}: {hits}")

    if failures:
        for failure in failures:
            print(f"LEAK: {failure}")
        raise AssertionError(f"Russian leakage found on {len(failures)} approved PL page(s)")

    print(f"PASS: zero Cyrillic leakage across {checked} approved PL page(s)")
    return checked


if __name__ == "__main__":
    validate()
