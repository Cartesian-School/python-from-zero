#!/usr/bin/env python3
"""Generate Polish crawler summaries from every published PL route."""

from __future__ import annotations

import html
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))

from localization import ROOT, Routes
from site_structure import SITE_ORIGIN

SITE = ROOT / "site"


def _metadata(path: Path) -> tuple[str, str]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else path.stem
    meta = soup.select_one('meta[name="description"]')
    description = html.unescape(meta.get("content", "")) if meta else ""
    return title, description


def main() -> None:
    routes = Routes()
    records = []
    for page_id in sorted(routes.pages):
        path = routes.available(page_id).get("pl")
        if not path:
            continue
        title, description = _metadata(SITE / path.lstrip("/"))
        records.append((page_id, title, description, SITE_ORIGIN + path))

    overview = """# Cartesian School — Python od zera

> Bezpłatny, kompletny kurs Python 3.14 w języku polskim: 24 rozdziały, 493 interaktywne ćwiczenia, 13 projektów oraz pełne Kompendium.

## Serwis

- Strona główna: https://www.cartesianschool.org/pl/index.html
- Rozdziały: https://www.cartesianschool.org/pl/index.html#glavy
- Praktyka: https://www.cartesianschool.org/pl/index.html#praktika
- Projekty: https://www.cartesianschool.org/pl/index.html#proekty
- Indeks rzeczowy: https://www.cartesianschool.org/pl/indeks-rzeczowy.html
- Pełna mapa kursu: https://www.cartesianschool.org/pl/llms-full.txt
- Mapa witryny: https://www.cartesianschool.org/sitemap.xml

## Tożsamość i licencje

Autorem kursu jest Siergej Sobolewski, założyciel Cartesian School. Treść jest udostępniana na licencji CC BY-NC-SA 4.0, a kod — na licencji MIT.
"""
    out_dir = SITE / "pl"
    (out_dir / "llms.txt").write_text(overview, encoding="utf-8")
    lines = [overview.rstrip(), "", "---", "", "## Pełna mapa opublikowanego kursu", ""]
    for page_id, title, description, url in records:
        lines.append(f"- {title} — {url}")
        if description:
            lines.append(f"  {description}")
    lines.append("")
    (out_dir / "llms-full.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"Polish llms outputs generated for {len(records)} routes")


if __name__ == "__main__":
    main()
