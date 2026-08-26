#!/usr/bin/env python3
"""Строит манифест покрытия из структурного оглавления курса.

Разбирает python_book_table_of_contents_ru.md (не изменяя его) и строит
manifest/coverage_manifest.json — по одной записи на каждый заголовок
(глава/раздел/подраздел). Заголовки глав берутся из data/chapters.json;
физическая пагинация сюда принципиально не входит и генерируется только
scripts/build_pdf.py в data/book-pagination.json.

Остальные поля (html_section, notebook, code_examples, illustrations,
exercises, validation_status) заполняются по мере производства материала;
изначально они None/[] — манифест ещё не означает готовность контента.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_metadata import chapter_title

ROOT = Path(__file__).resolve().parent.parent
TOC_PATH = ROOT / "python_book_table_of_contents_ru.md"
OUT_PATH = ROOT / "manifest" / "coverage_manifest.json"

CHAPTER_RE = re.compile(r"^##\s+Глава\s+(\d+)\s*$")
ENTRY_RE = re.compile(r"^(\s*)-\s+(.+?)\s*$")


def parse_toc(text: str) -> list[dict]:
    chapters = []
    current = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        m = CHAPTER_RE.match(line)
        if m:
            num = int(m.group(1))
            current = {
                "id": f"ch{num:02d}",
                "kind": "chapter",
                "number": num,
                "title": f"Глава {num}: {chapter_title(num)}",
                "html_section": None,
                "notebook": None,
                "code_examples": [],
                "illustrations": [],
                "exercises": [],
                "validation_status": "not_started",
                "entries": [],
            }
            chapters.append(current)
            continue

        if line.startswith("## "):
            # Front matter / index sections without a numeric chapter.
            fm = re.match(r"^##\s+(.+?)\s*$", line)
            if fm:
                title = fm.group(1)
                current = {
                    "id": re.sub(r"\W+", "-", title.strip().lower()).strip("-"),
                    "kind": "frontmatter",
                    "number": None,
                    "title": title.strip(),
                    "html_section": None,
                    "notebook": None,
                    "code_examples": [],
                    "illustrations": [],
                    "exercises": [],
                    "validation_status": "not_started",
                    "entries": [],
                }
                chapters.append(current)
            continue

        em = ENTRY_RE.match(raw_line)
        if em and current is not None:
            indent, title = em.groups()
            depth = len(indent) // 2
            current["entries"].append(
                {
                    "title": title.strip(),
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
    manifest = {
        "source": str(TOC_PATH.relative_to(ROOT)),
        "generated_note": (
            "coverage only; titles derive from data/chapters.json; physical pages "
            "derive from data/book-pagination.json"
        ),
        "chapter_count": sum(1 for c in chapters if c["kind"] == "chapter"),
        "entry_count": total_entries,
        "chapters": chapters,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Глав (kind=chapter): {manifest['chapter_count']}")
    print(f"Всего пунктов оглавления: {total_entries}")
    print(f"Записано: {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
