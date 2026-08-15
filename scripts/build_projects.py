#!/usr/bin/env python3
"""Строит страницы проектов (site/projects/<slug>/index.html) из
manifest/projects_manifest.json — единого источника истины для каталога
Проектов на главной странице и для этих детальных страниц.
"""

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import NAV_SCRIPT_TAG, mobile_nav_links, project_illustration, site_header

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest" / "projects_manifest.json"
PRACTICE_MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"
OUT_DIR = ROOT / "site" / "projects"

PROJECTS = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["projects"]
PRACTICE = json.loads(PRACTICE_MANIFEST_PATH.read_text(encoding="utf-8"))


def build_page(entry: dict) -> str:
    slug = entry["slug"]
    title = entry["title"]
    description = entry["description"]
    topics = entry.get("topics", [])
    source_path = entry["source_path"]
    chapter = entry.get("chapter")
    lesson_id = entry.get("lesson_id")

    topics_html = "".join(f'<span class="project-topic">{html.escape(t)}</span>' for t in topics)

    related_html = ""
    if chapter is not None:
        chapter_dir = ROOT / "site" / "chapters" / f"glava-{chapter:02d}"
        chapter_href = f"/chapters/glava-{chapter:02d}/index.html" if (chapter_dir / "index.html").exists() else None
        practice_entry = PRACTICE.get(lesson_id) if lesson_id else None
        parts = []
        if chapter_href:
            parts.append(f'<a class="reference-card" href="{chapter_href}"><span class="ri">📚</span><div><div class="rt">Глава {chapter}</div><div class="rs">Теория, из которой вырос этот проект</div></div></a>')
        if practice_entry:
            parts.append(f'<a class="reference-card" href="/practice/{lesson_id}/index.html"><span class="ri">🐍</span><div><div class="rt">Практика {lesson_id}</div><div class="rs">{html.escape(practice_entry["lesson_title"])}</div></div></a>')
        if parts:
            related_html = f'<div class="reference-board" style="margin-bottom:32px">{"".join(parts)}</div>'

    source_url = f"/{source_path}"
    download_name = Path(source_path).name

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)} — Проекты — Cartesian School</title>
<meta name="description" content="{html.escape(description)}" />
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/theory.css" />
<link rel="stylesheet" href="/assets/css/homepage.css" />
</head>
<body>

{site_header("proekty")}
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links("proekty")}
</nav>

<div class="project-hero">{project_illustration(entry["id"])}</div>

<div class="project-detail-body">
  <div class="breadcrumb"><a href="/index.html#proekty">← Все проекты</a></div>
  <h1>{html.escape(title)}</h1>
  <p class="lede">{html.escape(description)}</p>
  <div class="project-meta-row">{topics_html}</div>

  {related_html}

  <h2>Исходный код</h2>
  <p>Полный, уже проверенный файл — отдельно:</p>
  <p>📄 <a href="{source_url}" download="{html.escape(download_name)}">{html.escape(source_path)}</a></p>
  <p class="sub">Запустите локально: <code class="inline">python {html.escape(download_name)}</code></p>

  <p class="section-nav" style="border-top:1px solid var(--color-border-default);padding-top:24px;margin-top:40px">
    <a href="/index.html#proekty">← Вернуться к проектам</a>
  </p>
</div>

{NAV_SCRIPT_TAG}
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for entry in PROJECTS:
        slug = entry["slug"]
        out_dir = OUT_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "index.html"
        out_path.write_text(build_page(entry), encoding="utf-8")
        print(f"Записано: {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
