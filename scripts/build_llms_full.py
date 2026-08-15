#!/usr/bin/env python3
"""Generates site/llms-full.txt: the llms.txt overview plus a real, generated
URL map of every chapter (from manifest/coverage_manifest.json, the same
source build_site_index.py uses) and every top-level page family (from
site_structure.py). Not hand-maintained, so it can't go stale as chapters
are added — and it does not duplicate book text, only titles and URLs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_structure import SITE_DIR, SITE_ORIGIN, iter_pages

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "manifest" / "coverage_manifest.json").read_text(encoding="utf-8"))
LLMS_TXT = (SITE_DIR / "llms.txt").read_text(encoding="utf-8")
OUT_PATH = SITE_DIR / "llms-full.txt"


def _short_title(title: str | None, url_path: str) -> str:
    if not title:
        return url_path
    # Every generated <title> ends in " — ... Cartesian School" (chapter/front-matter
    # pages: "<title> — Python с нуля — Cartesian School"; practice pages: "<title>
    # — Cartesian School"). Strip that shared suffix so this list stays scannable
    # instead of repeating the same words on every line.
    return title.split(" — Cartesian School", 1)[0].split(" — Python с нуля", 1)[0]


def chapter_lines() -> list[str]:
    lines = ["## Chapters"]
    for c in MANIFEST["chapters"]:
        if c["kind"] != "chapter":
            continue
        num = c["number"]
        title = c["title"].split(": ", 1)[-1]  # drop the leading "Глава N: "
        pages = [p for p in iter_pages() if p.kind == "chapter-opener" and f"glava-{num:02d}/" in p.url_path]
        url = pages[0].canonical_url if pages else None
        if url:
            lines.append(f"- Chapter {num}: {title} — {url}")
        else:
            lines.append(f"- Chapter {num}: {title} (not yet published)")
    return lines


def front_matter_lines() -> list[str]:
    lines = ["", "## Front matter"]
    for p in iter_pages():
        if p.kind == "front-matter":
            lines.append(f"- {_short_title(p.title, p.url_path)} — {p.canonical_url}")
    return lines


def practice_lines() -> list[str]:
    lines = ["", "## Interactive practice (browser, Python 3.14 via Pyodide)"]
    for p in iter_pages():
        if p.kind == "practice":
            lines.append(f"- {_short_title(p.title, p.url_path)} — {p.canonical_url}")
    return lines


def main() -> None:
    parts = [LLMS_TXT.rstrip(), "", "---", ""]
    parts += chapter_lines()
    parts += front_matter_lines()
    parts += practice_lines()
    parts.append("")
    parts.append(f"## Reference")
    parts.append(f"- Subject index — {SITE_ORIGIN}/predmetnyj-ukazatel.html")
    parts.append("")

    OUT_PATH.write_text("\n".join(parts), encoding="utf-8")
    print(f"llms-full.txt записан в {OUT_PATH.relative_to(SITE_DIR.parent)}")


if __name__ == "__main__":
    main()
