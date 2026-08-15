#!/usr/bin/env python3
"""Строит домашнюю страницу сайта (site/index.html).

Единственный источник правды для каждой секции:
- Главы           -> manifest/coverage_manifest.json (24 главы)
- Практика        -> manifest/practice_manifest.json (122 записи практики)
- Проекты         -> manifest/projects_manifest.json (реальные projects/*)

Главное меню (site_lib.TOP_NAV_ITEMS) и секции этой страницы должны строго
соответствовать друг другу 1:1 — каждый пункт меню ведёт на #якорь одной из
секций ниже, и ни одна секция не переиспользуется под чужой смысл.
"""

import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import NAV_SCRIPT_TAG, mobile_nav_links, project_card, site_header

ROOT = Path(__file__).resolve().parent.parent
COVERAGE = json.loads((ROOT / "manifest" / "coverage_manifest.json").read_text(encoding="utf-8"))
PRACTICE = json.loads((ROOT / "manifest" / "practice_manifest.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8"))["projects"]


def chapter_href(num: int) -> str:
    slug_dir = ROOT / "site" / "chapters" / f"glava-{num:02d}"
    if (slug_dir / "index.html").exists():
        return f"/chapters/glava-{num:02d}/index.html"
    return "#"


def chapter_title_short(c: dict) -> str:
    """Chapter title with the leading "Глава N: " stripped, escaped for HTML,
    and its source *emphasis* markdown (used on a few titles to call out a
    module name, e.g. "...с помощью *Turtle*") rendered as real <em>.
    """
    t = c["title"]
    t = t.split(": ", 1)[-1] if ": " in t else t
    escaped = html.escape(t)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)


def lesson_title_short(entry: dict) -> str:
    t = entry["lesson_title"]
    return t.split(" · ", 1)[-1] if " · " in t else t


def mode_of(entry: dict) -> str:
    backend = entry.get("backend")
    if backend == "browser-pyodide":
        return "browser"
    if backend == "browser-adapted":
        return "adapted"
    return "local"


MODE_LABELS = {"browser": "В браузере", "local": "Локально", "adapted": "В браузере · адаптировано"}
MODE_CLASS = {"browser": "mode-browser", "local": "mode-local", "adapted": "mode-adapted"}

CHAPTERS = sorted((c for c in COVERAGE["chapters"] if c["kind"] == "chapter"), key=lambda c: c["number"])

lessons_by_chapter: dict[int, list[tuple[str, dict]]] = defaultdict(list)
for lesson_id, entry in PRACTICE.items():
    lessons_by_chapter[int(lesson_id.split("-")[0])].append((lesson_id, entry))
for lst in lessons_by_chapter.values():
    lst.sort(key=lambda pair: pair[0])

TOTAL_LESSONS = len(PRACTICE)
TOTAL_PROJECTS = len(PROJECTS)
TOTAL_PAGES = COVERAGE["actual_pdf_total_pages"]
TOTAL_CHAPTERS = COVERAGE["chapter_count"]
BROWSER_COUNT = sum(1 for e in PRACTICE.values() if mode_of(e) == "browser")
LOCAL_COUNT = sum(1 for e in PRACTICE.values() if mode_of(e) == "local")
CHAPTERS_WITH_PRACTICE = sum(1 for c in CHAPTERS if lessons_by_chapter.get(c["number"]))


# ---------------------------------------------------------------------------
# Главы — визуальный маршрут (roadmap) по всем 24 главам
# ---------------------------------------------------------------------------
def build_roadmap() -> str:
    nodes = []
    for c in CHAPTERS:
        num = c["number"]
        href = chapter_href(num)
        entries = lessons_by_chapter.get(num, [])
        lesson_ids_csv = ",".join(lid for lid, _ in entries)
        meta = f"{len(entries)} практических заданий" if entries else "теория — без практики"
        card_body = f"""<div class="jn-card-top">
          <span class="jn-num">Глава {num}</span>
        </div>
        <div class="jn-title">{chapter_title_short(c)}</div>"""
        if entries:
            card_body += '\n        <div class="jn-progress-track"><div class="jn-progress-fill"></div></div>'
        card_body += f"""
        <div class="jn-meta">{meta}</div>
        <span class="jn-state-badge"></span>"""
        nodes.append(f"""
    <div class="journey-node" data-chapter="{num}" data-lesson-ids="{lesson_ids_csv}">
      <div class="jn-dot"></div>
      <a class="jn-card" href="{href}">
        {card_body}
      </a>
    </div>""")
    return "".join(nodes)


# ---------------------------------------------------------------------------
# Практика — сгруппированный по главам каталог всех 122 записей
# ---------------------------------------------------------------------------
def build_practice_catalog() -> str:
    groups = []
    for c in CHAPTERS:
        num = c["number"]
        entries = lessons_by_chapter.get(num, [])
        if not entries:
            continue  # У главы 2 и 24 действительно нет практики (не ошибка)
        lesson_ids_csv = ",".join(lid for lid, _ in entries)
        rows = []
        for lid, e in entries:
            mode = mode_of(e)
            rows.append(f"""
        <a class="practice-lesson-row" data-lesson-id="{lid}" data-mode="{mode}" href="/practice/{lid}/index.html">
          <div class="plr-left">
            <span class="plr-id">{lid}</span>
            <span class="plr-title">{html.escape(lesson_title_short(e))}</span>
          </div>
          <div style="display:flex;align-items:center;gap:10px;flex-shrink:0">
            <span class="plr-check">✓</span>
            <span class="plr-badge {MODE_CLASS[mode]}">{MODE_LABELS[mode]}</span>
          </div>
        </a>""")
        groups.append(f"""
    <details class="practice-chapter-group" data-chapter="{num}" data-lesson-ids="{lesson_ids_csv}">
      <summary class="pcg-summary">
        <div>
          <div class="pcg-title">Глава {num} · {chapter_title_short(c)}</div>
          <div class="pcg-meta">{len(entries)} практических заданий</div>
        </div>
        <div class="pcg-progress">
          <div class="pcg-bar-track"><div class="pcg-bar-fill"></div></div>
          <span class="pcg-count">0 из {len(entries)}</span>
        </div>
        <span class="pcg-chevron">›</span>
      </summary>
      <div class="pcg-lessons">{"".join(rows)}</div>
    </details>""")
    return "".join(groups)


# ---------------------------------------------------------------------------
# Проекты
# ---------------------------------------------------------------------------
def build_projects_grid() -> str:
    return "".join(project_card(p) for p in PROJECTS)


ROADMAP_HTML = build_roadmap()
PRACTICE_CATALOG_HTML = build_practice_catalog()
PROJECTS_GRID_HTML = build_projects_grid()

HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Python с нуля — Cartesian School</title>
<meta name="description" content="Программирование, графика, приложения и игры на Python 3.14 — бесплатный интерактивный курс от Cartesian School." />
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/theory.css" />
<link rel="stylesheet" href="/assets/css/homepage.css" />
</head>
<body>

{site_header("o-kurse")}
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links("o-kurse")}
</nav>

<div class="home-hero">
  <div class="kicker">Python 3.14 · Бесплатный интерактивный курс</div>
  <h1>Python с нуля: программирование, графика, приложения и игры</h1>
  <p>{TOTAL_CHAPTERS} главы, {TOTAL_LESSONS} практических заданий, {TOTAL_PROJECTS} готовых мини-проектов — от первой строки
    кода до собственных игр и приложений. Теория здесь, практика — прямо в браузере.</p>
  <div class="home-cta">
    <a class="btn btn-primary" href="/chapters/glava-01/index.html">Начать с главы 1 →</a>
    <a class="btn btn-ghost" href="/front-matter/vvedenie.html">Как устроена книга</a>
  </div>
</div>

<div class="home-section panel-canvas" id="o-kurse">
  <div class="kicker-label">Python с нуля</div>
  <h2>О курсе</h2>
  <div class="about-grid">
    <div class="about-copy">
      <p>«Python с нуля» — бесплатный интерактивный курс программирования на Python 3.14 для тех, кто раньше не
      писал код. {TOTAL_CHAPTERS} главы проведут вас от первого <code class="inline">print()</code> до собственных
      игр, GUI-приложений и сайта на Flask.</p>
      <p>Каждый раздел — это связка теории на сайте и практики: {TOTAL_LESSONS} практических заданий, которые можно
      выполнить прямо в браузере или локально, плюс {TOTAL_PROJECTS} готовых мини-проектов с открытым исходным
      кодом.</p>
      <p>Автор курса — Siergej Sobolewski, Software &amp; AI Engineer, основатель Cartesian School.</p>
    </div>
    <div class="about-stats">
      <div class="about-stat"><div class="num">{TOTAL_CHAPTERS}</div><div class="lbl">Главы</div></div>
      <div class="about-stat"><div class="num">{TOTAL_LESSONS}</div><div class="lbl">Практических заданий</div></div>
      <div class="about-stat"><div class="num">{TOTAL_PROJECTS}</div><div class="lbl">Готовых проектов</div></div>
      <div class="about-stat"><div class="num">{TOTAL_PAGES}</div><div class="lbl">Страниц в книге</div></div>
    </div>
  </div>
</div>

<div class="home-section panel-surface">
  <div class="kicker-label">Формат</div>
  <h2>Как устроен курс</h2>
  <p class="sub">Каждый раздел — это связка из трёх частей.</p>
  <div class="feature-grid">
    <div class="feature"><div class="fi">📖</div><h3>Теория на сайте</h3><p>Понятное объяснение с примерами, диаграммами и разбором типичных ошибок.</p></div>
    <div class="feature"><div class="fi">🐍</div><h3>Практика в браузере</h3><p>Интерактивный ноутбук к каждому разделу прямо на странице — эксперименты, задания, самостоятельная практика.</p></div>
    <div class="feature"><div class="fi">⚖️</div><h3>Классика и современность</h3><p>Где это важно — классический приём и современный Python 3.14 рядом, с честным сравнением.</p></div>
    <div class="feature"><div class="fi">🎮</div><h3>Настоящие проекты</h3><p>Крестики-нолики, Змейка, космический шутер, веб-сайт на Flask — с полным рабочим кодом.</p></div>
  </div>
</div>

<div class="home-section panel-canvas" id="glavy">
  <div class="kicker-label">Ваш путь по курсу</div>
  <h2>Главы</h2>
  <p class="sub">Проходите главы последовательно и отслеживайте свой прогресс — все {TOTAL_CHAPTERS} главы уже
  открыты, прогресс сохраняется в этом браузере.</p>

  <div class="journey-progress" id="journey-progress" data-total-lessons="{TOTAL_LESSONS}">
    <div class="jp-top">
      <div class="jp-headline">Ваш прогресс</div>
      <div class="jp-pct">0%</div>
    </div>
    <div class="jp-detail">0 из {TOTAL_LESSONS} практических заданий выполнено</div>
    <div class="jp-bar-track"><div class="jp-bar-fill"></div></div>
    <div class="jp-stats-row">
      <span class="jp-stat"><strong class="jp-stat-completed-chapters">0</strong> из {TOTAL_CHAPTERS} глав завершено</span>
      <span class="jp-stat">Текущая глава: <strong class="jp-stat-current-chapter">—</strong></span>
    </div>
  </div>

  <div class="journey-rail">{ROADMAP_HTML}
  </div>
</div>

<div class="home-section panel-surface" id="praktika">
  <div class="kicker-label">Практика</div>
  <h2>Практика</h2>
  <p class="sub">{TOTAL_LESSONS} практических заданий по {CHAPTERS_WITH_PRACTICE} главам — выполняйте прямо в
  браузере или локально, без установки чего-либо для большинства уроков.</p>

  <div class="practice-summary">
    <span class="practice-stat-chip"><strong>{BROWSER_COUNT}</strong> в браузере</span>
    <span class="practice-stat-chip"><strong>{LOCAL_COUNT}</strong> локально</span>
    <span class="practice-stat-chip"><strong>{TOTAL_LESSONS}</strong> всего</span>
  </div>

  <div class="practice-filters" role="group" aria-label="Фильтр практики">
    <button class="pf-btn active" data-filter="all" type="button">Все</button>
    <button class="pf-btn" data-filter="browser" type="button">В браузере</button>
    <button class="pf-btn" data-filter="local" type="button">Локально</button>
  </div>

{PRACTICE_CATALOG_HTML}
</div>

<div class="home-section panel-canvas" id="proekty">
  <div class="kicker-label">Проекты</div>
  <h2>Проекты</h2>
  <p class="sub">{TOTAL_PROJECTS} готовых мини-проектов с открытым исходным кодом — от «Крестики-нолики» до
  полноценного космического шутера.</p>
  <div class="projects-grid">{PROJECTS_GRID_HTML}</div>
</div>

<div class="home-section panel-surface" id="spravochnik">
  <div class="kicker-label">Справочник</div>
  <h2>Справочник</h2>
  <p class="sub">Материалы книги и техническая информация о курсе.</p>
  <div class="reference-board">
    <a class="reference-card" href="/predmetnyj-ukazatel.html">
      <span class="ri">📇</span>
      <div><div class="rt">Предметный указатель</div><div class="rs">Алфавитный список терминов книги с номерами страниц</div></div>
    </a>
    <a class="reference-card" href="/front-matter/vvedenie.html">
      <span class="ri">📖</span>
      <div><div class="rt">Введение</div><div class="rs">Как получить максимум от этой книги</div></div>
    </a>
    <a class="reference-card" href="/front-matter/ob-avtore.html">
      <span class="ri">👤</span>
      <div><div class="rt">Об авторе</div><div class="rs">Siergej Sobolewski — Cartesian School</div></div>
    </a>
    <a class="reference-card" href="/front-matter/o-tehnicheskom-recenzente.html">
      <span class="ri">🔍</span>
      <div><div class="rt">О техническом рецензенте</div><div class="rs">Кто проверял код и объяснения книги</div></div>
    </a>
    <a class="reference-card" href="/book/pdf/gotovaya-kniga.pdf">
      <span class="ri">📄</span>
      <div><div class="rt">Скачать PDF</div><div class="rs">Вся книга целиком</div></div>
    </a>
    <a class="reference-card" href="/book/epub/python-s-nulya.epub">
      <span class="ri">📱</span>
      <div><div class="rt">Скачать EPUB</div><div class="rs">Для читалок и мобильных устройств</div></div>
    </a>
  </div>
</div>

<div class="home-footer">
  Cartesian School · Python с нуля · Siergej Sobolewski — Software &amp; AI Engineer, основатель Cartesian School
</div>

{NAV_SCRIPT_TAG}
<script src="/assets/js/progress.js" defer></script>
</body>
</html>
"""

OUT = ROOT / "site" / "index.html"
OUT.write_text(HTML, encoding="utf-8")
print(f"Записано: {OUT.relative_to(ROOT)}")
