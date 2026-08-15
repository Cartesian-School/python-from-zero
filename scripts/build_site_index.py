#!/usr/bin/env python3
"""Строит домашнюю страницу сайта (site/index.html)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import NAV_SCRIPT_TAG, mobile_nav_links, site_header

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "manifest" / "coverage_manifest.json").read_text(encoding="utf-8"))

def chapter_href(num: int) -> str:
    slug_dir = ROOT / "site" / "chapters" / f"glava-{num:02d}"
    if (slug_dir / "index.html").exists():
        return f"chapters/glava-{num:02d}/index.html"
    return "#"


chapters = [c for c in MANIFEST["chapters"] if c["kind"] == "chapter"]

rows = []
for c in chapters:
    num = c["number"]
    href = chapter_href(num)
    disabled = href == "#"
    cls = "chapter-card disabled" if disabled else "chapter-card"
    rows.append(f"""
      <a class="{cls}" href="{href}">
        <div class="cc-num">Глава {num}</div>
        <div class="cc-title">{c['title'].split(': ', 1)[-1]}</div>
        <div class="cc-page">стр. {c['canonical_page']}</div>
      </a>""")

chapters_html = "".join(rows)

HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Python с нуля — Cartesian School</title>
<meta name="description" content="Программирование, графика, приложения и игры на Python 3.14 — бесплатный интерактивный курс от Cartesian School." />
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/theory.css" />
<style>
  .home-hero {{
    background: radial-gradient(ellipse 900px 560px at 15% -20%, #2a1470 0%, var(--navy-900) 45%, var(--navy-950) 100%);
    color: #fff; padding: 96px 24px 80px; text-align: center;
  }}
  .home-hero .kicker {{ font-family: 'JetBrains Mono', monospace; color: var(--blue-300); font-size: 14px; letter-spacing: .1em; text-transform: uppercase; margin-bottom: 18px; }}
  .home-hero h1 {{ color: #fff; font-size: clamp(32px, 5vw, 56px); max-width: 800px; margin: 0 auto 20px; }}
  .home-hero p {{ color: var(--gray-400); font-size: 19px; max-width: 620px; margin: 0 auto 32px; }}
  .home-cta {{ display: inline-flex; gap: 14px; flex-wrap: wrap; justify-content: center; }}
  .btn {{ display: inline-block; padding: 14px 28px; border-radius: var(--radius-full); font-weight: 600; text-decoration: none; font-size: 15px; }}
  .btn-primary {{ background: linear-gradient(90deg, var(--violet-500), var(--blue-500)); color: #fff; }}
  .btn-ghost {{ border: 1px solid rgba(255,255,255,.25); color: #fff; }}

  .home-section {{ max-width: 1120px; margin: 0 auto; padding: 64px 24px; }}
  .home-section h2 {{ font-size: 26px; margin-bottom: 8px; }}
  .home-section .sub {{ color: var(--color-text-muted); margin-bottom: 32px; max-width: 560px; }}

  .feature-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
  .feature {{ padding: 24px; border: 1px solid var(--color-border-default); border-radius: var(--radius-lg); }}
  .feature .fi {{ font-size: 24px; margin-bottom: 10px; }}
  .feature h3 {{ font-size: 16px; margin-bottom: 6px; }}
  .feature p {{ font-size: 14px; color: var(--color-text-muted); }}

  .chapters-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
  .chapter-card {{ display: block; padding: 18px; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); text-decoration: none; color: var(--color-text-primary); }}
  .chapter-card:hover {{ border-color: var(--color-brand-blue); }}
  .chapter-card.disabled {{ opacity: .45; pointer-events: none; }}
  .cc-num {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--color-brand-blue); margin-bottom: 4px; }}
  .cc-title {{ font-weight: 600; font-size: 15px; margin-bottom: 4px; }}
  .cc-page {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--color-text-muted); }}

  .home-footer {{ background: var(--color-bg-inverse); color: var(--gray-400); padding: 40px 24px; text-align: center; font-size: 13px; }}

  @media (max-width: 860px) {{
    .feature-grid, .chapters-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

{site_header(None)}
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links(None)}
</nav>

<div class="home-hero" id="o-kurse">
  <div class="kicker">Python 3.14 · Бесплатный интерактивный курс</div>
  <h1>Python с нуля: программирование, графика, приложения и игры</h1>
  <p>24 главы, {MANIFEST['entry_count']} разделов, десятки мини-проектов — от первой строки кода
    до собственных игр и приложений. Теория здесь, практика — в Jupyter Notebook.</p>
  <div class="home-cta">
    <a class="btn btn-primary" href="chapters/glava-01/index.html">Начать с главы 1 →</a>
    <a class="btn btn-ghost" href="front-matter/vvedenie.html">Как устроена книга</a>
  </div>
</div>

<div class="home-section" id="praktika">
  <h2>Как устроен курс</h2>
  <p class="sub">Каждый раздел — это связка из трёх частей.</p>
  <div class="feature-grid">
    <div class="feature"><div class="fi">📖</div><h3>Теория на сайте</h3><p>Понятное объяснение с примерами, диаграммами и разбором типичных ошибок.</p></div>
    <div class="feature"><div class="fi">📓</div><h3>Практика в Jupyter</h3><p>Отдельный ноутбук к каждому разделу — эксперименты, задания, самостоятельная практика.</p></div>
    <div class="feature"><div class="fi">⚖️</div><h3>Классика и современность</h3><p>Где это важно — классический приём и современный Python 3.14 рядом, с честным сравнением.</p></div>
    <div class="feature"><div class="fi">🎮</div><h3>Настоящие проекты</h3><p>Крестики-нолики, Змейка, космический шутер, веб-сайт на Flask — с полным рабочим кодом.</p></div>
  </div>
</div>

<div class="home-section" id="glavy">
  <h2>Оглавление</h2>
  <p class="sub">Главы открываются по мере готовности материала.</p>
  <div class="chapters-grid">{chapters_html}
  </div>
</div>

<div class="home-section" id="proekty">
  <h2>Проекты</h2>
  <p class="sub">Полный исходный код каждого проекта книги — в каталоге <code class="inline">projects/</code> репозитория: Turtle, Tkinter, Pygame, Flask.</p>
</div>

<div class="home-section" id="spravochnik">
  <h2>Справочник и скачать</h2>
  <p class="sub">
    <a href="predmetnyj-ukazatel.html">Предметный указатель</a> — алфавитный список терминов книги с номерами страниц.
    Скачать книгу целиком: <a href="../book/epub/python-s-nulya.epub">EPUB</a> ·
    <a href="../book/pdf/gotovaya-kniga.pdf">PDF</a>.
  </p>
</div>

<div class="home-footer">
  Cartesian School · Python с нуля · Siergej Sobolewski — Software &amp; AI Engineer, основатель Cartesian School
</div>

{NAV_SCRIPT_TAG}
</body>
</html>
"""

OUT = ROOT / "site" / "index.html"
OUT.write_text(HTML, encoding="utf-8")
print(f"Записано: {OUT.relative_to(ROOT)}")
