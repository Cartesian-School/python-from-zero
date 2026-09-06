#!/usr/bin/env python3
"""Fail closed if an approved PL page uses a forbidden synonym for a binding
glossary term, or if the PL homepage's required section headings drift from
the approved glossary (Praktyka, Rozdziały, Kompendium, ...).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bs4 import BeautifulSoup
from localization import ROOT, TERMINOLOGY, Routes

# (anchor id, expected <h2> text) for the PL homepage sections.
PL_HOME_REQUIRED_HEADINGS = [
    ("o-kurse", "O kursie"),
    ("glavy", "Rozdziały"),
    ("praktika", "Praktyka"),
    ("proekty", "Projekty"),
    ("spravochnik", "Kompendium"),
]


def _visible_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text()


def _check_forbidden_synonyms(page_path: str, text: str) -> list[str]:
    return [
        f"{page_path}: forbidden synonym {word!r} ({reason})"
        for word, reason in TERMINOLOGY["forbidden_synonyms"].items()
        if word in text
    ]


def _check_home_headings(site_dir: Path) -> list[str]:
    home_file = site_dir / "pl" / "index.html"
    if not home_file.is_file():
        return []
    soup = BeautifulSoup(home_file.read_text(encoding="utf-8"), "html.parser")
    errors = []
    for anchor, expected in PL_HOME_REQUIRED_HEADINGS:
        section = soup.find(id=anchor)
        if section is None:
            errors.append(f"/pl/index.html: missing #{anchor} section")
            continue
        heading = section.find("h2") if section.name != "h2" else section
        if heading is None or heading.get_text(strip=True) != expected:
            actual = heading.get_text(strip=True) if heading else None
            errors.append(f"/pl/index.html: #{anchor} heading is {actual!r}, expected {expected!r}")
    return errors


def validate() -> int:
    routes = Routes()
    site_dir = ROOT / "site"
    errors: list[str] = []
    checked = 0

    for page_id, page in routes.pages.items():
        variant = page["variants"].get("pl")
        if not variant or variant["status"] != "approved":
            continue
        path = site_dir / variant["path"].lstrip("/")
        if not path.is_file():
            continue
        text = _visible_text(path.read_text(encoding="utf-8"))
        errors += _check_forbidden_synonyms(variant["path"], text)
        checked += 1

    errors += _check_home_headings(site_dir)

    if errors:
        for error in errors:
            print(f"TERMINOLOGY: {error}")
        raise AssertionError(f"{len(errors)} terminology violation(s) found")

    print(f"PASS: terminology contract holds across {checked} approved PL page(s)")
    return checked


if __name__ == "__main__":
    validate()
