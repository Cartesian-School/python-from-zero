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
    r"treść pojawi się w kolejnym etapie|pojawi[ąę]? się w kolejnych etapach|"
    r"nie została jeszcze przetłumaczona|są już ujęte w planie|"
    r"\bTODO\b|\bFIXME\b|\bTRANSLATE\b|\bTŁUMACZENIE\b|lorem ipsum",
)

# Homepage card selectors that must be real, navigable links to registered PL
# routes -- never a staged/disabled placeholder for content that already has
# a published PL page. A card whose corresponding route exists but which is
# rendered disabled (or without a usable href) is exactly the M02-I03
# "partial shell" regression this validator exists to make impossible again.
_HOME_CARD_SELECTORS = {
    "chapter": "a.jn-card",
    "project": "a.project-card",
    "reference": "#spravochnik a.reference-card",
}
_DISABLED_MARKERS = ("aria-disabled", "disabled")
_DEAD_HREFS = {"", "#", "javascript:void(0)", "javascript:void(0);"}


def _card_is_unusable(card) -> bool:
    if any(card.has_attr(attr) for attr in _DISABLED_MARKERS):
        return True
    href = card.get("href")
    return not href or href.strip() in _DEAD_HREFS or href.strip().startswith("javascript:")


def homepage_navigation_errors(
    home: BeautifulSoup, pages: dict, chapter_openers: set[str], manifest_practice: set[str],
) -> list[str]:
    """Verify every homepage card for existing PL content is a real, enabled
    link to its exact registered route -- not a staged/disabled placeholder.
    Extracted from validate() so regression tests can exercise it directly
    against a synthetic homepage without regenerating the whole site."""
    errors: list[str] = []

    disabled_groups = home.select(".practice-chapter-group[aria-disabled]")
    if disabled_groups:
        errors.append(f"PL homepage has {len(disabled_groups)} disabled practice chapter groups")
    practice_chapters_with_lessons = {int(pid.split("-", 1)[0]) for pid in manifest_practice}
    empty_groups = [
        g for g in home.select(".practice-chapter-group")
        if int(g.get("data-chapter", 0)) in practice_chapters_with_lessons
        and not g.select_one(".practice-lesson-row[href]")
    ]
    if empty_groups:
        errors.append(f"PL homepage has {len(empty_groups)} practice chapter groups missing their manifest lessons")

    expected_chapter_hrefs = {pages[pid]["variants"]["pl"]["path"] for pid in chapter_openers}
    expected_project_hrefs = {page["variants"]["pl"]["path"] for page in pages.values() if "project_id" in page}
    for kind, selector, expected in (
        ("chapter", _HOME_CARD_SELECTORS["chapter"], expected_chapter_hrefs),
        ("project", _HOME_CARD_SELECTORS["project"], expected_project_hrefs),
    ):
        cards = home.select(selector)
        unusable = [c for c in cards if _card_is_unusable(c)]
        if unusable:
            errors.append(f"PL homepage has {len(unusable)} disabled/placeholder {kind} cards")
        found_hrefs = {c.get("href") for c in cards if not _card_is_unusable(c)}
        if found_hrefs != expected:
            errors.append(
                f"PL homepage {kind} cards don't match routes.json: "
                f"missing={sorted(expected - found_hrefs)[:10]}, "
                f"unexpected={sorted(found_hrefs - expected)[:10]}"
            )

    reference_cards = home.select(_HOME_CARD_SELECTORS["reference"])
    unusable_reference = [c for c in reference_cards if _card_is_unusable(c)]
    if unusable_reference:
        errors.append(f"PL homepage has {len(unusable_reference)} disabled/placeholder reference cards")

    return errors


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
    errors.extend(homepage_navigation_errors(home, pages, chapter_openers, manifest_practice))

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
