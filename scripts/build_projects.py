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

from site_lib import (
    NAV_SCRIPT_TAG,
    _render_icon_markers,
    mobile_nav_links,
    project_illustration,
    project_publication_illustration,
    site_header,
)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest" / "projects_manifest.json"
PRESENTATION_PATH = ROOT / "manifest" / "projects_presentation.json"
PRACTICE_MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"
OUT_DIR = ROOT / "site" / "projects"

PROJECTS = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["projects"]
PROJECT_PRESENTATION = json.loads(PRESENTATION_PATH.read_text(encoding="utf-8"))["projects"]
PRACTICE = json.loads(PRACTICE_MANIFEST_PATH.read_text(encoding="utf-8"))


def build_publication_fragment(entry: dict, topics_html: str) -> str:
    """Preserve the closed PDF/EPUB project appendix input byte-for-byte.

    build_epub.extract_project() reads these two legacy classes from inside the
    inert template. Browsers do not render or expose template descendants in
    the document tree, so the redesigned page still has exactly one H1.
    """
    chapter = entry.get("chapter")
    lesson_id = entry.get("lesson_id")
    parts = []
    if chapter is not None:
        chapter_dir = ROOT / "site" / "chapters" / f"glava-{chapter:02d}"
        if (chapter_dir / "index.html").exists():
            parts.append(f'<a class="reference-card" href="/chapters/glava-{chapter:02d}/index.html"><span class="ri">📚</span><div><div class="rt">Глава {chapter}</div><div class="rs">Теория, из которой вырос этот проект</div></div></a>')
        practice_entry = PRACTICE.get(lesson_id) if lesson_id else None
        if practice_entry:
            publication_title = PROJECT_PRESENTATION[entry["id"]].get(
                "publication_practice_title", practice_entry["lesson_title"]
            )
            parts.append(f'<a class="reference-card" href="/practice/{lesson_id}/index.html"><span class="ri">🐍</span><div><div class="rt">Практика {lesson_id}</div><div class="rs">{html.escape(publication_title)}</div></div></a>')
    related_html = f'<div class="reference-board" style="margin-bottom:32px">{"".join(parts)}</div>' if parts else ""
    source_path = entry["source_path"]
    download_name = Path(source_path).name
    return f"""<template id="project-publication-source">
<div class="project-hero">{project_publication_illustration(entry["id"])}</div>

<div class="project-detail-body">
  <div class="breadcrumb"><a href="/index.html#proekty">← Все проекты</a></div>
  <h1>{html.escape(entry["title"])}</h1>
  <p class="lede">{html.escape(entry["description"])}</p>
  <div class="project-meta-row">{topics_html}</div>

  {related_html}

  <h2>Исходный код</h2>
  <p>Полный, уже проверенный файл — отдельно:</p>
  <p>📄 <a href="/{source_path}" download="{html.escape(download_name)}">{html.escape(source_path)}</a></p>
  <p class="sub">Запустите локально: <code class="inline">python {html.escape(download_name)}</code></p>

  <p class="section-nav" style="border-top:1px solid var(--color-border-default);padding-top:24px;margin-top:40px">
    <a href="/index.html#proekty">← Вернуться к проектам</a>
  </p>
</div>
</template>"""


def build_page(entry: dict) -> str:
    slug = entry["slug"]
    title = entry["title"]
    description = entry["description"]
    topics = entry.get("topics", [])
    source_path = entry["source_path"]
    chapter = entry.get("chapter")
    lesson_id = entry.get("lesson_id")
    detail = PROJECT_PRESENTATION[entry["id"]]

    topics_html = "".join(f'<span class="project-topic">{html.escape(t)}</span>' for t in topics)
    features_html = "".join(f'<li>{html.escape(item)}</li>' for item in detail["features"])
    outcomes_html = "".join(f'<li>{html.escape(item)}</li>' for item in detail["learning_outcomes"])
    commands_html = "".join(
        f'<div class="project-command"><span aria-hidden="true">$</span><code>{html.escape(command)}</code></div>'
        for command in detail["run_commands"]
    )
    run_note_html = (
        f'<p class="project-run-note">{html.escape(detail["run_note"])}</p>'
        if detail.get("run_note")
        else "<!-- No additional runtime note for this project. -->"
    )

    related_items = []
    if chapter is not None:
        chapter_dir = ROOT / "site" / "chapters" / f"glava-{chapter:02d}"
        chapter_href = f"/chapters/glava-{chapter:02d}/index.html" if (chapter_dir / "index.html").exists() else None
        practice_entry = PRACTICE.get(lesson_id) if lesson_id else None
        if chapter_href:
            related_items.append(
                f'<a class="project-related-card" href="{chapter_href}"><span class="project-related-card__icon">[[icon:note]]</span>'
                f'<span><strong>Глава {chapter}</strong><small>Теория проекта</small></span><span aria-hidden="true">→</span></a>'
            )
        if practice_entry:
            related_items.append(
                f'<a class="project-related-card" href="/practice/{lesson_id}/index.html"><span class="project-related-card__icon">[[icon:practice]]</span>'
                f'<span><strong>Практика {lesson_id}</strong><small>{html.escape(practice_entry["lesson_title"].split(" · ", 1)[-1])}</small></span><span aria-hidden="true">→</span></a>'
            )
    related_html = "".join(related_items)
    publication_fragment = build_publication_fragment(entry, topics_html)

    source_url = f"/{source_path}"
    download_name = Path(source_path).name
    source_cta = "Скачать README" if Path(source_path).suffix.lower() == ".md" else "Скачать исходник"

    return _render_icon_markers(f"""<!DOCTYPE html>
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
<link rel="stylesheet" href="/assets/css/projects.css" />
</head>
<body>

{site_header("proekty")}
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links("proekty")}
</nav>

<main class="project-detail">
  <section class="project-detail-hero" aria-labelledby="project-title">
    <div class="project-detail-hero__inner">
      <div class="project-detail-hero__copy">
        <div class="breadcrumb"><a href="/index.html#proekty">← Все проекты</a></div>
        <p class="project-detail-hero__eyebrow">Учебный проект · Глава {chapter}</p>
        <h1 id="project-title">{html.escape(title)}</h1>
        <p class="lede">{html.escape(description)}</p>
        <div class="project-meta-row">{topics_html}</div>
        <div class="project-detail-actions">
          <a class="btn btn-primary" href="{source_url}" download="{html.escape(download_name)}">{source_cta}</a>
          {f'<a class="btn btn-secondary" href="/practice/{lesson_id}/index.html">Открыть практику</a>' if lesson_id in PRACTICE else ''}
        </div>
      </div>
      <div class="project-detail-hero__visual">{project_illustration(entry["id"])}</div>
    </div>
  </section>

  <div class="project-detail-grid">
    <div class="project-detail-content">
      <section class="project-detail-section" aria-labelledby="about-project">
        <p class="project-section-index">01 / О проекте</p>
        <h2 id="about-project">Как устроен проект</h2>
        <p class="project-about">{html.escape(detail["about"])}</p>
      </section>

      <div class="project-detail-panels">
        <section class="project-info-panel" aria-labelledby="features-project">
          <span class="project-info-panel__icon">[[icon:architecture]]</span>
          <h2 id="features-project">Возможности</h2>
          <ul class="project-check-list">{features_html}</ul>
        </section>
        <section class="project-info-panel" aria-labelledby="outcomes-project">
          <span class="project-info-panel__icon">[[icon:success]]</span>
          <h2 id="outcomes-project">Что вы отработаете</h2>
          <ol class="project-outcome-list">{outcomes_html}</ol>
        </section>
      </div>

      <section class="project-detail-section project-run" aria-labelledby="run-project">
        <p class="project-section-index">02 / Локальный запуск</p>
        <h2 id="run-project">Запуск проекта</h2>
        <div class="project-command-list">{commands_html}</div>
        {run_note_html}
      </section>
    </div>

    <aside class="project-detail-sidebar" aria-label="Ресурсы проекта">
      <section class="project-resource-panel">
        <p class="project-resource-panel__label">Исходный код</p>
        <h2>{html.escape(download_name)}</h2>
        <p>Канонический файл проекта в репозитории курса.</p>
        <a class="project-source-link" href="{source_url}" download="{html.escape(download_name)}"><span>[[icon:file]]</span><span>{html.escape(source_path)}</span><span aria-hidden="true">↓</span></a>
      </section>
      <section class="project-related" aria-labelledby="related-project">
        <p class="project-resource-panel__label">Маршрут обучения</p>
        <h2 id="related-project">Связанные материалы</h2>
        <div class="project-related-list">{related_html}</div>
      </section>
    </aside>
  </div>

  <nav class="project-detail-back" aria-label="Назад к каталогу">
    <a href="/index.html#proekty">← Вернуться ко всем проектам</a>
  </nav>
</main>

{publication_fragment}

{NAV_SCRIPT_TAG}
</body>
</html>
""")


def main() -> None:
    canonical_ids = [entry["id"] for entry in PROJECTS]
    canonical_slugs = [entry["slug"] for entry in PROJECTS]
    if len(PROJECTS) != 13 or len(canonical_ids) != len(set(canonical_ids)) or len(canonical_slugs) != len(set(canonical_slugs)):
        raise ValueError("projects_manifest.json must contain exactly 13 unique ids and slugs")
    project_ids = set(canonical_ids)
    presentation_ids = set(PROJECT_PRESENTATION)
    if project_ids != presentation_ids:
        missing = sorted(project_ids - presentation_ids)
        extra = sorted(presentation_ids - project_ids)
        raise ValueError(f"projects_presentation.json mismatch: missing={missing}, extra={extra}")
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
