#!/usr/bin/env python3
"""Validate every learner-facing chapter title against one static authority."""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path
from zipfile import BadZipFile, ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_pagination import pagination
from chapter_metadata import chapters

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PRACTICE_PATH = ROOT / "manifest" / "practice_manifest.json"
EPUB_PATH = ROOT / "book" / "epub" / "python-s-nulya.epub"


def text(node) -> str:
    return " ".join(node.get_text(" ", strip=True).split()) if node else ""


def validate() -> list[str]:
    # Imported only for the full publication/CI audit. The Vercel portable
    # audit below intentionally depends on the Python standard library only.
    from bs4 import BeautifulSoup

    errors: list[str] = []
    canonical = chapters()
    canonical_by_number = {item.number: item for item in canonical}
    page_data = pagination()
    practice = json.loads(PRACTICE_PATH.read_text(encoding="utf-8"))

    if any("chapter_title" in entry for entry in practice.values()):
        errors.append(
            "practice_manifest.json must not duplicate canonical chapter titles"
        )

    homepage = BeautifulSoup((SITE / "index.html").read_text(encoding="utf-8"), "lxml")
    journey = {
        int(node["data-chapter"]): node
        for node in homepage.select(".journey-node[data-chapter]")
    }
    groups = {
        int(node["data-chapter"]): node
        for node in homepage.select(".practice-chapter-group[data-chapter]")
    }
    expected_numbers = set(range(1, 25))
    if set(journey) != expected_numbers:
        errors.append(f"homepage journey chapter set is {sorted(journey)}, expected 1..24")
    if set(groups) != expected_numbers:
        errors.append(f"homepage practice group set is {sorted(groups)}, expected 1..24")

    practice_by_chapter: dict[int, list[str]] = {number: [] for number in expected_numbers}
    for lesson_id in practice:
        practice_by_chapter[int(lesson_id.split("-", 1)[0])].append(lesson_id)

    for item in canonical:
        key = f"{item.number:02d}"
        generated = page_data["chapters"].get(key, {})
        if generated.get("title") != item.title or generated.get("url") != item.url:
            errors.append(f"chapter {key}: generated pagination title/URL drift")

        opener_path = SITE / item.url.lstrip("/")
        if not opener_path.is_file():
            errors.append(f"chapter {key}: opener missing: {item.url}")
            continue
        opener = BeautifulSoup(opener_path.read_text(encoding="utf-8"), "lxml")
        if text(opener.select_one(".chapter-hero h1")) != item.title:
            errors.append(f"chapter {key}: opener H1 differs from canonical title")
        expected_document_title = (
            f"Глава {item.number}. {item.title} — Python с нуля — Cartesian School"
        )
        if text(opener.title) != expected_document_title:
            errors.append(f"chapter {key}: document <title> differs from canonical title")

        expected_page_label = (
            f"ГЛАВА {item.number} · СТР. {generated.get('start_page')}"
        )
        if text(opener.select_one(".chapter-num")) != expected_page_label:
            errors.append(f"chapter {key}: opener page label is not {expected_page_label!r}")

        card = journey.get(item.number)
        if card:
            if text(card.select_one(".jn-title")) != item.title:
                errors.append(f"chapter {key}: homepage journey title drift")
            card_link = card.select_one("a.jn-card")
            if not card_link or card_link.get("href") != item.url:
                errors.append(f"chapter {key}: homepage journey URL drift")
            actual_ids = sorted(filter(None, card.get("data-lesson-ids", "").split(",")))
            if actual_ids != sorted(practice_by_chapter[item.number]):
                errors.append(f"chapter {key}: homepage journey practice relationship drift")

        group = groups.get(item.number)
        if group:
            expected_group_title = f"Глава {item.number} · {item.title}"
            if text(group.select_one(".pcg-title")) != expected_group_title:
                errors.append(f"chapter {key}: homepage practice-group title drift")
            actual_ids = sorted(filter(None, group.get("data-lesson-ids", "").split(",")))
            if actual_ids != sorted(practice_by_chapter[item.number]):
                errors.append(f"chapter {key}: homepage practice-group membership drift")

    expected_total = int(page_data["total_pages"])
    total_node = next(
        (
            node
            for node in homepage.select(".about-stat")
            if text(node.select_one(".lbl")) == "Страниц в книге"
        ),
        None,
    )
    if not total_node or text(total_node.select_one(".num")) != str(expected_total):
        errors.append("homepage exact book total differs from generated pagination")

    for lesson_id in sorted(practice):
        number = int(lesson_id.split("-", 1)[0])
        page_path = SITE / "practice" / lesson_id / "index.html"
        if not page_path.is_file():
            errors.append(f"practice {lesson_id}: generated page missing")
            continue
        soup = BeautifulSoup(page_path.read_text(encoding="utf-8"), "lxml")
        expected = f"Глава {number}: {canonical_by_number[number].title}"
        if text(soup.select_one(".practice-chapter")) != expected:
            errors.append(f"practice {lesson_id}: chapter title drift")

    llms_path = SITE / "llms-full.txt"
    if llms_path.is_file():
        llms = llms_path.read_text(encoding="utf-8")
        for item in canonical:
            expected = f"- Chapter {item.number}: {item.title} —"
            if expected not in llms:
                errors.append(f"llms-full.txt: missing canonical chapter {item.number}")

    coverage = json.loads(
        (ROOT / "manifest" / "coverage_manifest.json").read_text(encoding="utf-8")
    )
    coverage_chapters = {
        entry["number"]: re.sub(r"[*_`]", "", entry["title"])
        for entry in coverage["chapters"]
        if entry.get("kind") == "chapter"
    }
    for item in canonical:
        if coverage_chapters.get(item.number) != f"Глава {item.number}: {item.title}":
            errors.append(f"coverage catalog: title drift for chapter {item.number}")

    try:
        with ZipFile(EPUB_PATH) as archive:
            ncx = archive.read("EPUB/toc.ncx").decode("utf-8")
        for item in canonical:
            if f"Глава {item.number}: {item.title}" not in ncx:
                errors.append(f"EPUB TOC: title drift for chapter {item.number}")
    except (FileNotFoundError, KeyError, BadZipFile, UnicodeDecodeError) as exc:
        errors.append(f"EPUB TOC cannot be validated: {exc}")

    active_sources = [
        ROOT / "data" / "chapters.json",
        ROOT / "scripts" / "build_site_index.py",
        SITE / "index.html",
        SITE / "chapters" / "glava-23" / "index.html",
    ]
    for path in active_sources:
        if "Ещё больше мини-проектов" in path.read_text(encoding="utf-8"):
            errors.append(f"stale current Chapter 23 title remains in {path.relative_to(ROOT)}")

    return errors


def validate_portable() -> list[str]:
    """Validate deployable title bindings without publication dependencies.

    GitHub CI runs :func:`validate` with BeautifulSoup/lxml and performs the
    complete semantic audit. Vercel receives already-built publication files,
    so its build gate verifies the exact committed HTML/EPUB/catalog bindings
    using only the standard library instead of installing a second, mutable
    Python publication toolchain during deployment.
    """
    errors: list[str] = []
    canonical = chapters()
    canonical_by_number = {item.number: item for item in canonical}
    page_data = pagination()
    practice = json.loads(PRACTICE_PATH.read_text(encoding="utf-8"))
    homepage = (SITE / "index.html").read_text(encoding="utf-8")

    if any("chapter_title" in entry for entry in practice.values()):
        errors.append(
            "practice_manifest.json must not duplicate canonical chapter titles"
        )

    expected_numbers = set(range(1, 25))
    journey_numbers = {
        int(value)
        for value in re.findall(
            r'<div class="journey-node" data-chapter="(\d+)"', homepage
        )
    }
    group_numbers = {
        int(value)
        for value in re.findall(
            r'<details class="practice-chapter-group" data-chapter="(\d+)"',
            homepage,
        )
    }
    if journey_numbers != expected_numbers:
        errors.append(
            f"homepage journey chapter set is {sorted(journey_numbers)}, expected 1..24"
        )
    if group_numbers != expected_numbers:
        errors.append(
            f"homepage practice group set is {sorted(group_numbers)}, expected 1..24"
        )

    practice_by_chapter: dict[int, list[str]] = {number: [] for number in expected_numbers}
    for lesson_id in practice:
        practice_by_chapter[int(lesson_id.split("-", 1)[0])].append(lesson_id)

    for item in canonical:
        key = f"{item.number:02d}"
        generated = page_data["chapters"].get(key, {})
        if generated.get("title") != item.title or generated.get("url") != item.url:
            errors.append(f"chapter {key}: generated pagination title/URL drift")

        opener_path = SITE / item.url.lstrip("/")
        if not opener_path.is_file():
            errors.append(f"chapter {key}: opener missing: {item.url}")
            continue
        opener = opener_path.read_text(encoding="utf-8")
        expected_document_title = (
            f"Глава {item.number}. {item.title} — Python с нуля — Cartesian School"
        )
        expected_page_label = (
            f"ГЛАВА {item.number} · СТР. {generated.get('start_page')}"
        )
        if f"<h1>{escape(item.title)}</h1>" not in opener:
            errors.append(f"chapter {key}: opener H1 differs from canonical title")
        if f"<title>{escape(expected_document_title)}</title>" not in opener:
            errors.append(f"chapter {key}: document <title> differs from canonical title")
        if expected_page_label not in opener:
            errors.append(f"chapter {key}: opener page label is not {expected_page_label!r}")

        expected_ids = ",".join(sorted(practice_by_chapter[item.number]))
        journey_pattern = re.compile(
            rf'<div class="journey-node" data-chapter="{item.number}" '
            rf'data-lesson-ids="{re.escape(expected_ids)}">(?P<body>.*?)'
            rf'(?=<div class="journey-node"|<div class="home-section panel-surface" id="praktika")',
            re.DOTALL,
        )
        journey_match = journey_pattern.search(homepage)
        if not journey_match:
            errors.append(f"chapter {key}: homepage journey relationship drift")
        else:
            body = journey_match.group("body")
            if f'<a class="jn-card" href="{item.url}">' not in body:
                errors.append(f"chapter {key}: homepage journey URL drift")
            if f'<div class="jn-title">{escape(item.title)}</div>' not in body:
                errors.append(f"chapter {key}: homepage journey title drift")

        group_pattern = re.compile(
            rf'<details class="practice-chapter-group" data-chapter="{item.number}" '
            rf'data-lesson-ids="{re.escape(expected_ids)}">(?P<body>.*?)'
            rf'(?=<details class="practice-chapter-group"|<div class="home-section[^"]*" id="proekty")',
            re.DOTALL,
        )
        group_match = group_pattern.search(homepage)
        if not group_match:
            errors.append(f"chapter {key}: homepage practice-group membership drift")
        elif (
            f'<div class="pcg-title">Глава {item.number} · {escape(item.title)}</div>'
            not in group_match.group("body")
        ):
            errors.append(f"chapter {key}: homepage practice-group title drift")

    expected_total = int(page_data["total_pages"])
    if (
        f'<div class="num">{expected_total}</div>'
        '<div class="lbl">Страниц в книге</div>'
        not in homepage
    ):
        errors.append("homepage exact book total differs from generated pagination")

    for lesson_id in sorted(practice):
        number = int(lesson_id.split("-", 1)[0])
        page_path = SITE / "practice" / lesson_id / "index.html"
        if not page_path.is_file():
            errors.append(f"practice {lesson_id}: generated page missing")
            continue
        expected = f"Глава {number}: {canonical_by_number[number].title}"
        page = page_path.read_text(encoding="utf-8")
        if f'<div class="practice-chapter">{escape(expected)}</div>' not in page:
            errors.append(f"practice {lesson_id}: chapter title drift")

    llms_path = SITE / "llms-full.txt"
    if llms_path.is_file():
        llms = llms_path.read_text(encoding="utf-8")
        for item in canonical:
            if f"- Chapter {item.number}: {item.title} —" not in llms:
                errors.append(f"llms-full.txt: missing canonical chapter {item.number}")

    coverage = json.loads(
        (ROOT / "manifest" / "coverage_manifest.json").read_text(encoding="utf-8")
    )
    coverage_chapters = {
        entry["number"]: re.sub(r"[*_`]", "", entry["title"])
        for entry in coverage["chapters"]
        if entry.get("kind") == "chapter"
    }
    for item in canonical:
        if coverage_chapters.get(item.number) != f"Глава {item.number}: {item.title}":
            errors.append(f"coverage catalog: title drift for chapter {item.number}")

    try:
        with ZipFile(EPUB_PATH) as archive:
            ncx = archive.read("EPUB/toc.ncx").decode("utf-8")
        for item in canonical:
            if f"Глава {item.number}: {item.title}" not in ncx:
                errors.append(f"EPUB TOC: title drift for chapter {item.number}")
    except (FileNotFoundError, KeyError, BadZipFile, UnicodeDecodeError) as exc:
        errors.append(f"EPUB TOC cannot be validated: {exc}")

    active_sources = [
        ROOT / "data" / "chapters.json",
        ROOT / "scripts" / "build_site_index.py",
        SITE / "index.html",
        SITE / "chapters" / "glava-23" / "index.html",
    ]
    for path in active_sources:
        if "Ещё больше мини-проектов" in path.read_text(encoding="utf-8"):
            errors.append(f"stale current Chapter 23 title remains in {path.relative_to(ROOT)}")

    return errors


def main() -> None:
    args = sys.argv[1:]
    if args not in ([], ["--portable"]):
        print("usage: validate_chapter_titles.py [--portable]", file=sys.stderr)
        raise SystemExit(2)
    errors = validate_portable() if args else validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print(
        "Canonical chapter titles: PASS "
        "(24 openers, 24 journey cards, 24 practice groups, all practice pages)"
    )


if __name__ == "__main__":
    main()
