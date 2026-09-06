#!/usr/bin/env python3
"""Fail-fast completeness contract for the full M02-I04 Polish corpus."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))

from localization import ROOT, Routes
from validate_pl_leakage import find_leaks

SITE = ROOT / "site"
TEMPORARY = re.compile(
    r"Tłumaczenie niedostępne|dostępne później|wersja będzie udostępniana etapami|"
    r"treść pojawi się w kolejnym etapie|\bTODO\b|\bFIXME\b|\bTRANSLATE\b|"
    r"\bTŁUMACZENIE\b|lorem ipsum",
)


def validate() -> dict[str, int]:
    routes = Routes()
    errors: list[str] = []
    pages = routes.pages
    pl_variants = {page_id: routes.available(page_id).get("pl") for page_id in pages}
    missing_routes = [page_id for page_id, path in pl_variants.items() if not path]
    if missing_routes:
        errors.append(f"missing publishable PL routes: {missing_routes[:20]}")

    chapter_openers = {page_id for page_id in pages if re.fullmatch(r"chapter-\d{2}", page_id)}
    chapter_lessons = {page_id for page_id in pages if re.match(r"chapter-\d{2}-lesson-", page_id)}
    practices = {page["practice_id"] for page in pages.values() if "practice_id" in page}
    projects = {page["project_id"] for page in pages.values() if "project_id" in page}
    manifest_practice = set(__import__("json").loads((ROOT / "manifest/practice_manifest.json").read_text()))
    manifest_projects = {
        item["id"] for item in __import__("json").loads(
            (ROOT / "manifest/projects_manifest.json").read_text()
        )["projects"]
    }
    if len(chapter_openers) != 24:
        errors.append(f"chapter openers: {len(chapter_openers)} != 24")
    if practices != manifest_practice or len(practices) != 493:
        errors.append(f"practice IDs differ: routes={len(practices)}, manifest={len(manifest_practice)}")
    if projects != manifest_projects or len(projects) != 13:
        errors.append(f"project IDs differ: routes={len(projects)}, manifest={len(manifest_projects)}")

    ru_to_pl = {page["variants"]["ru"]["path"]: page["variants"]["pl"]["path"]
                for page in pages.values() if "pl" in page["variants"]}
    for page_id, path in pl_variants.items():
        if not path:
            continue
        file = SITE / path.lstrip("/")
        soup = BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser")
        if not soup.html or soup.html.get("lang") != "pl":
            errors.append(f"{path}: missing html lang=pl")
        h1 = soup.find("h1")
        primary_title = h1 or soup.select_one(".practice-lesson")
        if primary_title is None or not primary_title.get_text(" ", strip=True):
            errors.append(f"{path}: empty or missing h1")
        visible = BeautifulSoup(str(soup), "html.parser")
        for tag in visible(["script", "style", "code", "pre"]):
            tag.decompose()
        text = visible.get_text(" ", strip=True)
        if TEMPORARY.search(text):
            errors.append(f"{path}: placeholder or temporary localization copy")
        leaks = find_leaks(str(soup), set())
        if leaks:
            errors.append(f"{path}: Cyrillic leakage {leaks[:5]}")
        switch = soup.select_one('.language-switcher [lang="ru"][href]')
        if switch is None or switch.get("href") != pages[page_id]["variants"]["ru"]["path"]:
            errors.append(f"{path}: missing exact PL->RU switch")
        for anchor in soup.find_all("a", href=True):
            if anchor.find_parent(class_="language-switcher"):
                continue
            parsed = urlsplit(urljoin(path, anchor["href"]))
            if parsed.path in ru_to_pl:
                errors.append(f"{path}: RU fallback link {anchor['href']}")

    home = BeautifulSoup((SITE / "pl/index.html").read_text(encoding="utf-8"), "html.parser")
    disabled = home.select(
        ".jn-card[aria-disabled], .practice-chapter-group[aria-disabled], "
        ".project-card[aria-disabled], #spravochnik .reference-card[aria-disabled]"
    )
    if disabled:
        errors.append(f"PL homepage has {len(disabled)} disabled localization cards")

    for practice_id in practices:
        notebook = ROOT / "site/pl/notebooks" / __import__("json").loads(
            (ROOT / "manifest/practice_manifest.json").read_text()
        )[practice_id]["notebook"]
        if not notebook.is_file():
            errors.append(f"missing localized notebook: {practice_id}")

    if errors:
        for error in errors[:200]:
            print(f"PL-COMPLETE: {error}")
        raise AssertionError(f"{len(errors)} Polish completeness violation(s)")

    result = {
        "routes": len(pl_variants), "chapters": len(chapter_openers),
        "lessons": len(chapter_lessons), "practice": len(practices), "projects": len(projects),
    }
    print("PASS: complete Polish corpus", result)
    return result


if __name__ == "__main__":
    validate()
