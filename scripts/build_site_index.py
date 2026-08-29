#!/usr/bin/env python3
"""Строит домашнюю страницу сайта (site/index.html).

Единственный источник правды для каждой секции:
- Главы           -> data/chapters.json (24 главы)
- Страницы книги  -> data/book-pagination.json (фактический PDF)
- Практика        -> manifest/practice_manifest.json (122 записи практики)
- Проекты         -> manifest/projects_manifest.json (реальные projects/*)

Главное меню (site_lib.TOP_NAV_ITEMS) и секции этой страницы должны строго
соответствовать друг другу 1:1 — каждый пункт меню ведёт на #якорь одной из
секций ниже, и ни одна секция не переиспользуется под чужой смысл.
"""

import html
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_pagination import total_pages
from chapter_metadata import Chapter, chapters
from site_lib import (
    NAV_SCRIPT_TAG,
    _render_icon_markers,
    mobile_nav_links,
    project_card,
    site_header,
)

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = json.loads((ROOT / "manifest" / "practice_manifest.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8"))["projects"]


def chapter_href(num: int) -> str:
    slug_dir = ROOT / "site" / "chapters" / f"glava-{num:02d}"
    if (slug_dir / "index.html").exists():
        return f"/chapters/glava-{num:02d}/index.html"
    return "#"


def chapter_title_short(chapter: Chapter) -> str:
    return html.escape(chapter.title)


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

# Percent-encoded "готовая книга.pdf" — matches build_pdf.py's OUT filename exactly.
PDF_HREF = "/book/pdf/%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0.pdf"

CHAPTERS = chapters()

lessons_by_chapter: dict[int, list[tuple[str, dict]]] = defaultdict(list)
for lesson_id, entry in PRACTICE.items():
    lessons_by_chapter[int(lesson_id.split("-")[0])].append((lesson_id, entry))
for lst in lessons_by_chapter.values():
    lst.sort(key=lambda pair: pair[0])

TOTAL_LESSONS = len(PRACTICE)
TOTAL_PROJECTS = len(PROJECTS)
TOTAL_PAGES = total_pages()
TOTAL_CHAPTERS = len(CHAPTERS)
BROWSER_COUNT = sum(1 for e in PRACTICE.values() if mode_of(e) == "browser")
LOCAL_COUNT = sum(1 for e in PRACTICE.values() if mode_of(e) == "local")
CHAPTERS_WITH_PRACTICE = sum(1 for chapter in CHAPTERS if lessons_by_chapter.get(chapter.number))


# ---------------------------------------------------------------------------
# Главы — визуальный маршрут (roadmap) по всем 24 главам
# ---------------------------------------------------------------------------
def build_roadmap() -> str:
    nodes = []
    for chapter in CHAPTERS:
        num = chapter.number
        href = chapter_href(num)
        entries = lessons_by_chapter.get(num, [])
        lesson_ids_csv = ",".join(lid for lid, _ in entries)
        meta = f"{len(entries)} практических заданий" if entries else "теория — без практики"
        card_body = f"""<div class="jn-card-top">
          <span class="jn-num">Глава {num}</span>
        </div>
        <div class="jn-title">{chapter_title_short(chapter)}</div>"""
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
    for chapter in CHAPTERS:
        num = chapter.number
        entries = lessons_by_chapter.get(num, [])
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
          <div class="pcg-title">Глава {num} · {chapter_title_short(chapter)}</div>
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

HTML = _render_icon_markers(f"""<!DOCTYPE html>
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

<section class="home-hero" aria-labelledby="course-hero-title">
  <div class="home-hero__inner">
    <div class="home-hero__content">
      <div class="kicker">
        <img src="/assets/img/brand/python-logo-mark.svg" width="25" height="30" alt="" aria-hidden="true" />
        <span>Python 3.14 · Бесплатный интерактивный курс</span>
      </div>
      <h1 id="course-hero-title">Python с нуля: программирование, графика, приложения и игры</h1>
      <p>{TOTAL_CHAPTERS} главы, {TOTAL_LESSONS} практических заданий, {TOTAL_PROJECTS} готовых мини-проектов — от первой строки
        кода до собственных игр и приложений. Теория здесь, практика — прямо в браузере.</p>
      <div class="home-cta">
        <a class="btn btn-primary" href="/chapters/glava-01/index.html">Начать с главы 1 →</a>
        <a class="btn btn-ghost" href="/front-matter/vvedenie.html">Как устроена книга</a>
      </div>
    </div>

    <div class="hero-system" aria-hidden="true">
      <div class="hero-system__grid"></div>
      <div class="hero-system__backdrop">
        <span class="hero-system__prompt">&gt;&gt;&gt;</span>
        <span class="hero-token hero-token--def">def</span>
        <span class="hero-token hero-token--py">.py</span>
        <span class="hero-token hero-token--range">range()</span>
        <span class="hero-token hero-token--lambda">lambda</span>
      </div>

      <div class="hero-system__plane">
        <svg class="hero-connectors hero-connectors--desktop" viewBox="0 0 620 520" preserveAspectRatio="none">
          <g class="hero-axes">
            <path d="M50 466H585" />
            <path d="M50 466V54" />
            <path d="M578 461L585 466L578 471" />
            <path d="M45 61L50 54L55 61" />
            <text x="589" y="471">x</text>
            <text x="43" y="45">y</text>
          </g>
          <g class="hero-connector-lines">
            <path id="hero-route-code" d="M310 244V164H353" />
            <path id="hero-route-graph" d="M310 244H260V154" />
            <path id="hero-route-app" d="M310 244H440V343" />
            <path id="hero-route-game" d="M310 244H180V353" />
          </g>
          <g class="hero-connector-signals">
            <path class="hero-signal hero-signal--code" d="M310 244V164H353" />
            <path class="hero-signal hero-signal--graph" d="M310 244H260V154" />
            <path class="hero-signal hero-signal--app" d="M310 244H440V343" />
            <path class="hero-signal hero-signal--game" d="M310 244H180V353" />
          </g>
          <g class="hero-route-nodes">
            <circle cx="310" cy="164" r="4" />
            <circle cx="260" cy="244" r="4" />
            <circle cx="440" cy="244" r="4" />
            <circle cx="180" cy="244" r="4" />
          </g>
        </svg>

        <svg class="hero-connectors hero-connectors--mobile" viewBox="0 0 360 430" preserveAspectRatio="none">
          <g class="hero-axes">
            <path d="M18 302H344" />
            <path d="M18 302V24" />
            <text x="347" y="307">x</text>
            <text x="12" y="18">y</text>
          </g>
          <g class="hero-connector-lines">
            <path d="M180 194V130" />
            <path d="M180 194H295V145" />
            <path d="M180 194H85V322" />
            <path d="M180 194H275V322" />
          </g>
          <g class="hero-route-nodes">
            <circle cx="180" cy="130" r="4" />
            <circle cx="295" cy="194" r="4" />
            <circle cx="85" cy="194" r="4" />
            <circle cx="275" cy="194" r="4" />
          </g>
        </svg>

        <div class="hero-core">
          <span class="hero-core__orbit"></span>
          <span class="hero-core__mark"><img src="/assets/img/brand/python-logo-mark.svg" width="40" height="48" alt="" /></span>
          <span class="hero-core__name">Python</span>
          <span class="hero-core__runtime">runtime 3.14</span>
        </div>

        <div class="hero-module hero-module--code">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>Code</span>
            <span>square.py</span>
          </div>
          <pre><span class="syntax-prompt">&gt;&gt;&gt;</span> <span class="syntax-keyword">def</span> square(x):
<span class="syntax-prompt">...</span>     <span class="syntax-keyword">return</span> x ** 2
<span class="syntax-prompt">&gt;&gt;&gt;</span> square(5)
<span class="syntax-result">25</span><span class="hero-code-cursor">▌</span></pre>
        </div>

        <div class="hero-module hero-module--graph">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>Graph</span>
            <span>f(x)</span>
          </div>
          <svg class="hero-plot" viewBox="0 0 210 94">
            <g class="hero-plot__grid">
              <path d="M8 16H204M8 39H204M8 62H204M8 85H204M32 7V88M76 7V88M120 7V88M164 7V88" />
            </g>
            <path class="hero-plot__axis" d="M8 80H204M22 88V7" />
            <path class="hero-plot__curve" d="M9 69C40 67 49 18 82 23C111 27 119 72 146 67C168 63 177 29 203 16" />
            <path class="hero-plot__vector" d="M111 53L146 36M139 35L146 36L143 43" />
            <circle class="hero-plot__point hero-plot__point--a" cx="82" cy="23" r="3.5" />
            <circle class="hero-plot__point hero-plot__point--b" cx="146" cy="67" r="3.5" />
          </svg>
        </div>

        <div class="hero-module hero-module--app">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>App</span>
            <span class="hero-app-status"><b></b>running</span>
          </div>
          <div class="hero-app-ui">
            <div class="hero-app-ui__chart">
              <span style="--bar: .42"></span><span style="--bar: .72"></span><span style="--bar: .56"></span><span style="--bar: .88"></span>
            </div>
            <div class="hero-app-ui__panel">
              <span></span><span></span><b>run()</b>
            </div>
          </div>
        </div>

        <div class="hero-module hero-module--game">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>Game</span>
            <span>score 0250</span>
          </div>
          <svg class="hero-game" viewBox="0 0 210 76">
            <path class="hero-game__trajectory" d="M18 58H72V38H126V18H190" />
            <g class="hero-game__target"><circle cx="181" cy="18" r="10" /><circle cx="181" cy="18" r="3" /></g>
            <g class="hero-game__sprite"><path d="M35 51L53 58L35 65L39 58Z" /><path d="M31 55H20M31 61H25" /></g>
            <rect class="hero-game__collision" x="126" y="47" width="24" height="18" rx="2" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</section>

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
    <div class="feature"><div class="fi">[[icon:note]]</div><h3>Теория на сайте</h3><p>Понятное объяснение с примерами, диаграммами и разбором типичных ошибок.</p></div>
    <div class="feature"><div class="fi">[[icon:practice]]</div><h3>Практика в браузере</h3><p>Интерактивный ноутбук к каждому разделу прямо на странице — эксперименты, задания, самостоятельная практика.</p></div>
    <div class="feature"><div class="fi">[[icon:compare]]</div><h3>Классика и современность</h3><p>Где это важно — классический приём и современный Python 3.14 рядом, с честным сравнением.</p></div>
    <div class="feature"><div class="fi">[[icon:game]]</div><h3>Настоящие проекты</h3><p>Крестики-нолики, Змейка, космический шутер, веб-сайт на Flask — с полным рабочим кодом.</p></div>
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
      <span class="ri">[[icon:note]]</span>
      <div><div class="rt">Предметный указатель</div><div class="rs">Алфавитный список терминов книги по главам</div></div>
    </a>
    <a class="reference-card" href="/front-matter/vvedenie.html">
      <span class="ri">[[icon:note]]</span>
      <div><div class="rt">Введение</div><div class="rs">Как получить максимум от этой книги</div></div>
    </a>
    <a class="reference-card" href="/front-matter/ob-avtore.html">
      <span class="ri">[[icon:profile]]</span>
      <div><div class="rt">Об авторе</div><div class="rs">Siergej Sobolewski — Cartesian School</div></div>
    </a>
    <a class="reference-card" href="/front-matter/o-tehnicheskom-recenzente.html">
      <span class="ri">[[icon:search]]</span>
      <div><div class="rt">О техническом рецензенте</div><div class="rs">Кто проверял код и объяснения книги</div></div>
    </a>
    <a class="reference-card" href="{PDF_HREF}">
      <span class="ri">[[icon:file]]</span>
      <div><div class="rt">Скачать PDF</div><div class="rs">Вся книга целиком</div></div>
    </a>
    <a class="reference-card" href="/book/epub/python-s-nulya.epub">
      <span class="ri">[[icon:device]]</span>
      <div><div class="rt">Скачать EPUB</div><div class="rs">Для читалок и мобильных устройств</div></div>
    </a>
  </div>
</div>

<div class="home-footer">
  Cartesian School · Python с нуля · Siergej Sobolewski — Software &amp; AI Engineer, основатель Cartesian School
</div>

{NAV_SCRIPT_TAG}
<script src="/assets/js/hero.js" defer></script>
<script src="/assets/js/progress.js" defer></script>
</body>
</html>
""")

OUT = ROOT / "site" / "index.html"
OUT.write_text(HTML, encoding="utf-8")
print(f"Записано: {OUT.relative_to(ROOT)}")
