#!/usr/bin/env python3
"""Validate editorial invariants that executable-code tests cannot cover."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


def main() -> None:
    errors: list[str] = []
    owners: dict[str, list[str]] = defaultdict(list)
    for path in sorted((SITE / "chapters").glob("glava-*/*.html")):
        if path.name == "index.html":
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for card in soup.select(".notebook-card:not(.notebook-card-revisit)"):
            link = card.select_one('a[href*="/practice/"]')
            match = re.search(r"/practice/(\d{2}-\d{2})/index\.html", link.get("href", "")) if link else None
            if match:
                owners[match.group(1)].append(str(path.relative_to(ROOT)))

    for lesson_id, paths in sorted(owners.items()):
        if len(paths) > 1:
            errors.append(f"practice {lesson_id} is introduced as new on multiple pages: {paths}")
    if owners.get("04-03") != ["site/chapters/glava-04/04-03-vidy-chisel.html"]:
        errors.append(f"practice 04-03 must be owned by the numeric-type map: {owners.get('04-03')}")

    chapter_20 = BeautifulSoup((SITE / "chapters/glava-20/index.html").read_text(encoding="utf-8"), "html.parser")
    for item in chapter_20.select(".section-item"):
        number = item.select_one(".si-num")
        if not number or not number.get_text(strip=True):
            errors.append(f"chapter 20 unnumbered section: {item.get_text(' ', strip=True)}")
    chapter_20_links = [a.get("href") for a in chapter_20.select(".section-item[href]")]
    expected_20 = [
        "20-05-mini-proekt-myach-itogi.html", "20-14-igrovoj-cikl.html",
        "20-28-otladka-igr.html", "20-06-mir-gejmdeva.html",
        "20-13-mobilnyj-realnost.html", "20-29-upakovka-desktop.html",
    ]
    positions = [chapter_20_links.index(href) for href in expected_20]
    if positions != sorted(positions):
        errors.append("chapter 20 technical core and industry appendix are out of editorial order")

    chapter_23 = BeautifulSoup((SITE / "chapters/glava-23/index.html").read_text(encoding="utf-8"), "html.parser")
    for item in chapter_23.select(".section-item"):
        number = item.select_one(".si-num")
        if not number or not number.get_text(strip=True):
            errors.append(f"chapter 23 unnumbered section: {item.get_text(' ', strip=True)}")

    legacy = {
        f"https://www.cartesianschool.org/chapters/glava-23/23-{n:02d}-{slug}.html"
        for n, slug in (
            (1, "kalkulyator"), (2, "generator-istorij"),
            (3, "kamen-nozhnicy-bumaga"), (4, "otskakivayushij-myach"),
            (5, "temperatura"), (6, "fajly-tkinter-itogi"),
        )
    }
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    leaked = sorted(url for url in legacy if url in sitemap)
    if leaked:
        errors.append(f"legacy Chapter 23 redirects leaked into sitemap: {leaked}")

    if errors:
        print("Editorial structure: FAIL", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Editorial structure: PASS ({len(owners)} unique practice owners)")


if __name__ == "__main__":
    main()
