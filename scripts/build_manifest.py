#!/usr/bin/env python3
"""Строит манифест покрытия/пагинации из канонического оглавления.

Разбирает python_book_table_of_contents_ru.md (не изменяя его) и строит
manifest/coverage_manifest.json — по одной записи на каждый заголовок
(глава/раздел/подраздел) с базовой страницей-условием (canonical_page).
Остальные поля (html_section, notebook, code_examples, illustrations,
exercises, actual_pdf_page, validation_status) заполняются по мере
производства материала; изначально они None/[] — манифест ещё не
означает готовность контента.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT / "python_book_table_of_contents_ru.md"
OUT_PATH = ROOT / "manifest" / "coverage_manifest.json"

CHAPTER_RE = re.compile(r"^##\s+(Глава\s+(\d+):\s+.+?)\s+—\s+(\d+)\s*$")
FRONT_CHAPTER_RE = re.compile(r"^##\s+(.+?)\s*$")
ENTRY_RE = re.compile(r"^(\s*)-\s+(.+?)\s+—\s+\*\*([a-zA-Zа-яА-Я0-9]+)\*\*\s*$")


def _page_value(raw: str):
    """Numeric page as int, or the raw roman-numeral label (front matter)."""
    return int(raw) if raw.isdigit() else raw


def parse_toc(text: str) -> list[dict]:
    chapters = []
    current = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        m = CHAPTER_RE.match(line)
        if m:
            title, num, page = m.groups()
            current = {
                "id": f"ch{int(num):02d}",
                "kind": "chapter",
                "number": int(num),
                "title": title.strip(),
                "canonical_page": int(page),
                "html_section": None,
                "notebook": None,
                "code_examples": [],
                "illustrations": [],
                "exercises": [],
                "actual_pdf_page": None,
                "validation_status": "not_started",
                "entries": [],
            }
            chapters.append(current)
            continue

        if line.startswith("## "):
            # Front matter / index sections without a numeric chapter, e.g.
            # "## Вводные материалы" or "## Предметный указатель — 545"
            fm = re.match(r"^##\s+(.+?)(?:\s+—\s+(\d+))?\s*$", line)
            if fm:
                title, page = fm.groups()
                current = {
                    "id": re.sub(r"\W+", "-", title.strip().lower()).strip("-"),
                    "kind": "frontmatter",
                    "number": None,
                    "title": title.strip(),
                    "canonical_page": int(page) if page else None,
                    "html_section": None,
                    "notebook": None,
                    "code_examples": [],
                    "illustrations": [],
                    "exercises": [],
                    "actual_pdf_page": None,
                    "validation_status": "not_started",
                    "entries": [],
                }
                chapters.append(current)
            continue

        em = ENTRY_RE.match(raw_line)
        if em and current is not None:
            indent, title, page = em.groups()
            depth = len(indent) // 2
            current["entries"].append(
                {
                    "title": title.strip(),
                    "canonical_page": _page_value(page),
                    "depth": depth,
                    "html_anchor": None,
                    "notebook": None,
                    "validation_status": "not_started",
                }
            )
            continue

    return chapters


def main() -> None:
    text = TOC_PATH.read_text(encoding="utf-8")
    chapters = parse_toc(text)

    total_entries = sum(len(c["entries"]) for c in chapters)
    numeric_pages = [c["canonical_page"] for c in chapters if isinstance(c["canonical_page"], int)]
    numeric_pages += [
        e["canonical_page"]
        for c in chapters
        for e in c["entries"]
        if isinstance(e["canonical_page"], int)
    ]
    max_page = max(numeric_pages)

    manifest = {
        "source": str(TOC_PATH.relative_to(ROOT)),
        "generated_note": "canonical TOC is READ-ONLY; this manifest tracks coverage only",
        "chapter_count": sum(1 for c in chapters if c["kind"] == "chapter"),
        "entry_count": total_entries,
        "canonical_baseline_max_page": max_page,
        "min_required_pdf_pages": 545,
        "chapters": chapters,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Глав (kind=chapter): {manifest['chapter_count']}")
    print(f"Всего пунктов оглавления: {total_entries}")
    print(f"Максимальная базовая страница: {max_page}")
    print(f"Записано: {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
