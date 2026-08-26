#!/usr/bin/env python3
"""Собирает канонический печатный PDF и его фактическую пагинацию.

Переиспользует извлечение содержимого страниц из build_epub.py (тот же <article> /
.chapter-hero+.section-list разбор), но склеивает всё в один HTML-документ с печатной
типографикой: обложка (уже готовый дизайн-концепт, склеен как первая физическая
страница через pypdf), титульный лист, страница авторских прав, оглавление с реальными
номерами страниц (CSS target-counter, без ручного пересчёта),
разрыв страницы перед каждой главой, колонтитулы, приложение с проектами, предметный
указатель.

Нумерация страниц сквозная: обложка и титульный лист не показывают folio, остальные
страницы используют арабские числа физического PDF. Каждая глава начинается на recto
через ``break-before: right``; возникающая blank page учитывается физическим page tree.

Физическое дерево итогового PDF является единственной authority для start pages.
Builder пишет ``data/book-pagination.json`` из реально отрендеренных anchors; старые
минимальные страницы или ручные offsets в расчёте не участвуют.
"""

import hashlib
import json
import os
import sys
from importlib.metadata import version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_epub as be
from bs4 import BeautifulSoup
from chapter_metadata import chapters
from pypdf import PdfReader, PdfWriter
from weasyprint import HTML
from weasyprint import __version__ as WEASYPRINT_VERSION

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "book" / "pdf" / "готовая книга.pdf"
COVER_PDF = ROOT / "design" / "exports" / "cover_concept_v1.pdf"
PAGINATION_OUT = ROOT / "data" / "book-pagination.json"

# FontTools rewrites the OpenType ``head.modified`` field when WeasyPrint
# subsets fonts (notably Noto Color Emoji).  Without a fixed epoch, two
# otherwise identical renders contain different embedded font bytes.  This is
# the standard reproducible-builds boundary supported by FontTools itself.
SOURCE_DATE_EPOCH = "0"

FONT_DIR = ROOT / "book" / "fonts" / "dejavu"
FONT_FILES = {
    "DejaVuSerif.ttf": "8cb29f7db250ebb2551a6ce2c1e0bfd5a0eb520e9e233370db0493e82e1f36f7",
    "DejaVuSerif-Bold.ttf": "aac3f559445d23f0f567a243f91f3f6ad6cb4b5cafa1521a3479fffe0637f0bd",
    "DejaVuSerif-Italic.ttf": "d843bf414381dd64b89e6c7c954075657b74168521f02b30e11d308558eda1d2",
    "DejaVuSerif-BoldItalic.ttf": "ed336a3d81f5a2d6a3d12c16dda400b28ba7304792254fc9e96c0d6835fbeab2",
    "DejaVuSans.ttf": "57f73e11f51999432bf7ab22ce55b6f945d5eca1bf824404cfa9ec2e3718c84e",
    "DejaVuSans-Bold.ttf": "a4c5bc453ca281d90ea079e596da7ae0dfeb5777497c29ec254e76d97ff6f890",
    "DejaVuSans-Oblique.ttf": "e2f09289f4276309a36b9a93e5a0ac64957ef3eb7158151b243d41f667151ee4",
    "DejaVuSansMono.ttf": "54bf827eb99404e8f430c330ad30f063334f637eba0109b6a18d4f566a8e9dd8",
    "DejaVuSansMono-Bold.ttf": "0d3c03d1b667192f91223660a3163325cf83132662fe4d9f7d6e596bf7a995c2",
}

BOOK_TITLE = "Python с нуля"
BOOK_SUBTITLE = "программирование, графика, приложения и игры"
BOOK_AUTHOR = "Siergej Sobolewski"
BOOK_AUTHOR_ROLE = "Software & AI Engineer, основатель Cartesian School"
BOOK_DESCRIPTION = "Книга для начинающих: Python 3.14, графика на Turtle, приложения на Tkinter, игры на Pygame и веб-разработка на Flask."
SITE_URL_DISPLAY = "cartesianschool.org"

PRINT_CSS = """
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/DejaVuSerif.ttf'); font-style: normal; font-weight: 400; }
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/DejaVuSerif-Bold.ttf'); font-style: normal; font-weight: 700; }
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/DejaVuSerif-Italic.ttf'); font-style: italic; font-weight: 400; }
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/DejaVuSerif-BoldItalic.ttf'); font-style: italic; font-weight: 700; }
@font-face { font-family: 'DejaVu Sans'; src: url('__FONT_DIR_URI__/DejaVuSans.ttf'); font-style: normal; font-weight: 400; }
@font-face { font-family: 'DejaVu Sans'; src: url('__FONT_DIR_URI__/DejaVuSans-Bold.ttf'); font-style: normal; font-weight: 700; }
@font-face { font-family: 'DejaVu Sans'; src: url('__FONT_DIR_URI__/DejaVuSans-Oblique.ttf'); font-style: italic; font-weight: 400; }
@font-face { font-family: 'DejaVu Sans Mono'; src: url('__FONT_DIR_URI__/DejaVuSansMono.ttf'); font-style: normal; font-weight: 400; }
@font-face { font-family: 'DejaVu Sans Mono'; src: url('__FONT_DIR_URI__/DejaVuSansMono-Bold.ttf'); font-style: normal; font-weight: 700; }
@page {
  size: 152mm 229mm;
  margin: 24mm 20mm 26mm 20mm;
  @top-center { content: string(chaptitle); font-family: 'DejaVu Sans', sans-serif; font-size: 8pt; color: #888; letter-spacing: .04em; text-transform: uppercase; }
  @bottom-center { content: counter(page); font-family: 'DejaVu Sans', sans-serif; font-size: 9pt; color: #666; }
}
@page :left { @top-left { content: string(chaptitle); font-family: 'DejaVu Sans', sans-serif; font-size: 8pt; color: #888; letter-spacing: .04em; text-transform: uppercase; } @top-center { content: none; } }
@page :right { @top-right { content: "Python с нуля"; font-family: 'DejaVu Sans', sans-serif; font-size: 8pt; color: #888; letter-spacing: .04em; text-transform: uppercase; } @top-center { content: none; } }
@page :first {
  /* The cover (design/exports/cover_concept_v1.pdf) is merged in afterwards as
     an extra, external physical page 1 that WeasyPrint never renders or counts
     — so its own internal page 1 (this title page) is actually true physical
     page 2. Reset the counter here so every printed folio matches the page's
     real position in the final merged PDF, not WeasyPrint's un-offset count. */
  counter-reset: page 2;
  @top-left { content: none; } @top-center { content: none; } @top-right { content: none; } @bottom-center { content: ""; }
}
@page unnumbered { @top-left { content: none; } @top-center { content: none; } @top-right { content: none; } @bottom-center { content: ""; } }
@page opener { @top-left { content: none; } @top-center { content: none; } @top-right { content: none; } }

:root {
  --navy-900: #150a3d; --violet-500: #7c3aed; --blue-500: #2563eb; --blue-300: #93c5fd;
  --amber-500: #d97706; --gray-400: #9ca3af;
  --color-text-primary: #1a1a2e; --color-text-muted: #55536b; --color-text-inverse: #fff;
  --color-bg-surface: #f4f3fb; --color-border-default: #ddd9ee;
  --color-brand-blue: #2563eb; --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-full: 999px;
  --spacing-sm: 6px; --spacing-md: 12px; --spacing-lg: 18px; --spacing-xl: 24px; --spacing-2xl: 32px; --spacing-3xl: 48px; --spacing-4xl: 64px;
}
* { box-sizing: border-box; }
body { font-family: 'DejaVu Serif', Georgia, serif; font-size: 13.8pt; line-height: 1.95; color: var(--color-text-primary); }
h1, h2, h3 { font-family: 'DejaVu Sans', sans-serif; color: var(--navy-900); break-after: avoid; }
h1 { font-size: 25pt; margin: 0 0 15pt; string-set: chaptitle content(); }
h2 { font-size: 18pt; margin: 28pt 0 11pt; }
h3 { font-size: 14.5pt; margin: 19pt 0 8pt; }
p { margin: 0 0 13pt; orphans: 3; widows: 3; }
a { color: var(--color-brand-blue); text-decoration: none; }
code, pre { font-family: 'DejaVu Sans Mono', monospace; }
code.inline { background: var(--color-bg-surface); padding: 1px 5px; border-radius: 4px; font-size: 12pt; }
.code-block { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 15pt 0; break-inside: avoid; overflow: hidden; }
.code-block .code-label { background: var(--navy-900); color: #cbd5ff; font-size: 10.5pt; padding: 7pt 11pt; font-family: 'DejaVu Sans Mono', monospace; }
.code-block .copy-btn { display: none; }
.code-block pre { margin: 0; padding: 12pt 14pt; font-size: 11pt; line-height: 1.6; white-space: pre-wrap; word-break: break-word; }
.tok-kw { color: #7c3aed; font-weight: 600; }
.tok-str { color: #059669; }
.tok-com { color: #6b7280; font-style: italic; }
.tok-num { color: #d97706; }
.tok-fn { color: #2563eb; }
.callout { border: 1px solid var(--color-border-default); border-left: 4px solid var(--color-brand-blue); border-radius: var(--radius-md); padding: 8pt 12pt; margin: 10pt 0; background: var(--color-bg-surface); break-inside: avoid; }
.callout-title { font-weight: 700; font-family: 'DejaVu Sans', sans-serif; font-size: 10pt; margin-bottom: 3pt; }
.callout-warning { border-left-color: var(--amber-500); }
.exercise { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 8pt 12pt; margin: 10pt 0; break-inside: avoid; }
.exercise-stars { color: var(--amber-500); font-size: 9pt; }
.exercise-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 10.5pt; }
.summary-box { background: var(--color-bg-surface); border-radius: var(--radius-lg); padding: 10pt 14pt; margin: 14pt 0; break-inside: avoid; }
.summary-box ul { margin: 6pt 0 0 16pt; }
.cvm { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 10pt 0; break-inside: avoid; overflow: hidden; }
.cvm-header { background: var(--color-bg-surface); font-weight: 700; font-family: 'DejaVu Sans', sans-serif; padding: 6pt 10pt; font-size: 9.5pt; }
.cvm-grid { display: table; width: 100%; }
.cvm-col { display: table-cell; width: 50%; padding: 8pt 10pt; vertical-align: top; }
.cvm-col.classic { border-right: 1px solid var(--color-border-default); }
.cvm-col pre { margin: 4pt 0 0; font-size: 10pt; white-space: pre-wrap; }
.cvm-verdict { padding: 6pt 10pt; font-size: 9pt; border-top: 1px solid var(--color-border-default); }
.section-item { display: block; padding: 6pt 8pt; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin-bottom: 5pt; text-decoration: none; color: var(--color-text-primary); }
.section-item .si-num { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-text-muted); font-size: 8.5pt; margin-right: 6pt; }
.section-item .si-page { float: right; font-family: 'DejaVu Sans Mono', monospace; color: var(--color-text-muted); font-size: 8.5pt; }
.chapter-hero { page: opener; break-before: right; padding-top: 30pt; }
.chapter-hero .chapter-num { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-brand-blue); font-size: 10pt; margin-bottom: 6pt; }
.chapter-hero .chapter-num::after { content: " · СТР. " counter(page); }
.chapter-hero .chapter-num img { display: none; }
.chapter-hero h1 { font-size: 26pt; }
.chapter-hero p { font-size: 11.5pt; color: var(--color-text-muted); max-width: 90%; }
.chapter-meta { display: none; }
.idx-list { list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 20pt; }
.idx-entry { display: flex; justify-content: space-between; gap: 6pt; padding: 3pt 0; font-size: 9pt; border-bottom: 1px dotted var(--color-border-default); break-inside: avoid; }
.idx-term { flex: 1; min-width: 0; }
.idx-page { flex: none; font-family: 'DejaVu Sans Mono', monospace; color: var(--color-text-muted); }
.idx-note { color: var(--color-text-muted); font-size: 8pt; }
.title-page { page: unnumbered; break-after: page; text-align: center; padding-top: 70mm; }
.title-page .kicker { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-brand-blue); letter-spacing: 2px; font-size: 10pt; }
.title-page h1 { font-size: 30pt; margin: 14pt 0 6pt; string-set: none; }
.title-page .subtitle { font-size: 13pt; color: var(--color-text-muted); margin-bottom: 40pt; }
.title-page .author { font-size: 12pt; font-weight: 700; margin-top: 60pt; }
.title-page .author-role { font-size: 10pt; color: var(--color-text-muted); }
.chapter-break { break-before: page; }

/* ---------- Copyright page ---------- */
.copyright-page { page: unnumbered; break-before: page; break-after: page; font-size: 9pt; line-height: 1.4; color: var(--color-text-muted); padding-top: 8mm; }
.copyright-page p { margin: 0 0 7pt; font-size: 9pt; }
.copyright-page .cp-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; color: var(--color-text-primary); font-size: 11pt; margin-bottom: 4pt; }

/* ---------- Table of contents ---------- */
.toc-page { break-before: page; }
.toc-page h1 { string-set: none; }
.toc-part-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 10pt; text-transform: uppercase; letter-spacing: .05em; color: var(--color-brand-blue); margin: 16pt 0 6pt; }
.toc-part-title:first-child { margin-top: 0; }
.toc-entry {
  display: flex; justify-content: space-between; align-items: baseline; gap: 10pt;
  text-decoration: none; color: var(--color-text-primary); font-size: 11pt; padding: 3pt 0;
  border-bottom: 1px dotted var(--color-border-default);
}
.toc-entry.toc-chapter { font-weight: 700; margin-top: 8pt; border-bottom: none; padding-bottom: 0; }
.toc-entry::after {
  content: target-counter(attr(href url), page);
  flex-shrink: 0; font-family: 'DejaVu Sans Mono', monospace; font-size: 9.5pt; color: var(--color-text-muted);
}

/* ---------- Notebook / practice reference card (print-safe: visible, real URL) ---------- */
.notebook-card { border: 1px solid var(--color-border-default); border-left: 4px solid var(--blue-300); border-radius: var(--radius-md); padding: 8pt 12pt; margin: 10pt 0; break-inside: avoid; background: var(--color-bg-surface); }
.notebook-card .nc-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 10.5pt; color: var(--color-text-primary); }
.notebook-card .nc-sub { font-size: 9.5pt; color: var(--color-text-muted); margin-bottom: 4pt; }
.notebook-card .nc-btn { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; }
.notebook-card .nc-url { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; color: var(--color-text-muted); }
.practice-inline-status { display: none; }

/* ---------- Projects appendix ---------- */
.project-entry { break-before: page; }
.project-entry .project-hero { width: 100%; height: 62mm; overflow: hidden; border-radius: var(--radius-md); margin-bottom: 12pt; }
.project-entry .project-hero svg { display: block; width: 100%; height: 100%; }
.project-meta-row { margin: 4pt 0 10pt; }
.project-topic { display: inline-block; font-family: 'DejaVu Sans', sans-serif; font-size: 8.5pt; font-weight: 700; background: var(--color-bg-surface); color: var(--color-text-muted); padding: 2pt 8pt; border-radius: var(--radius-full); margin: 0 4pt 4pt 0; }
.reference-board { margin: 10pt 0; }
.reference-card { display: block; padding: 6pt 0; text-decoration: none; color: var(--color-text-primary); border-bottom: 1px dotted var(--color-border-default); }
.reference-card .ri { display: none; }
.reference-card .rt { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 10.5pt; }
.reference-card .rs { font-size: 9.5pt; color: var(--color-text-muted); }
"""
PRINT_CSS = PRINT_CSS.replace("__FONT_DIR_URI__", FONT_DIR.as_uri())


def build_title_page() -> str:
    return f"""
    <div class="title-page">
      <div class="kicker">PYTHON 3.14 · С НУЛЯ</div>
      <h1>{BOOK_TITLE}</h1>
      <div class="subtitle">{BOOK_SUBTITLE}</div>
      <div class="author">{BOOK_AUTHOR}</div>
      <div class="author-role">{BOOK_AUTHOR_ROLE}</div>
    </div>
    """


def build_license_paragraphs() -> str:
    """Full MIT license text from the repo's own LICENSE.md, reflowed (each
    paragraph's hard-wrapped source lines joined into one line) — never
    truncated, since this is a real legal notice, not editorial copy."""
    license_text = (ROOT / "LICENSE.md").read_text(encoding="utf-8").strip()
    paragraphs = [p.replace("\n", " ").strip() for p in license_text.split("\n\n")]
    return "".join(f"<p>{p}</p>" for p in paragraphs)


def build_copyright_page() -> str:
    return f"""
    <div class="copyright-page">
      <p class="cp-title">{BOOK_TITLE}: {BOOK_SUBTITLE}</p>
      <p>{BOOK_AUTHOR} — {BOOK_AUTHOR_ROLE}</p>
      <p>Издание Cartesian School, 2026. Python 3.14.</p>
      <p>Электронное издание. Онлайн-версия курса, интерактивная практика в браузере
      и исходный код всех проектов — {SITE_URL_DISPLAY}</p>
      {build_license_paragraphs()}
    </div>
    """


def build_toc_entries() -> str:
    parts = ['<div class="toc-part-title">Вводные материалы</div>']
    for anchor_id, title in be.FRONT_MATTER:
        marker = "fm-" + anchor_id.rsplit("/", 1)[-1].replace(".html", "")
        parts.append(f'<a class="toc-entry" href="#{marker}"><span class="toc-label">{title}</span></a>')

    for num in range(1, 25):
        title = be.chapter_title(num)
        parts.append(f'<a class="toc-entry toc-chapter" href="#marker-ch-{num}"><span class="toc-label">Глава {num}. {title}</span></a>')

    parts.append('<div class="toc-part-title">Проекты</div>')
    for entry in be.PROJECTS:
        parts.append(f'<a class="toc-entry" href="#proj-{entry["slug"]}"><span class="toc-label">{entry["title"]}</span></a>')

    parts.append('<div class="toc-part-title">Справочник</div>')
    parts.append('<a class="toc-entry" href="#marker-index"><span class="toc-label">Предметный указатель</span></a>')

    return f"""
    <div class="toc-page chapter-break">
      <h1>Оглавление</h1>
      {"".join(parts)}
    </div>
    """


def strip_wrapper(content: str) -> str:
    return content[len("<html><body>"):-len("</body></html>")]


def printify_notebook_cards(inner_html: str) -> str:
    """be.extract_article() already absolutizes .nc-btn hrefs (rewrite_links);
    for print we additionally un-hide the card (PRINT_CSS no longer sets
    display:none) and append the plain-text URL next to the link, since a
    physical page can't be clicked."""
    if "notebook-card" not in inner_html:
        return inner_html
    soup = BeautifulSoup(inner_html, "lxml")
    for card in soup.find_all("div", class_="notebook-card"):
        btn = card.find("a", class_="nc-btn")
        if btn and btn.get("href"):
            url_span = soup.new_tag("span")
            url_span["class"] = "nc-url"
            url_span.string = f" ({btn['href']})"
            btn.insert_after(url_span)
    body = soup.find("body")
    return "".join(str(c) for c in body.contents) if body else str(soup)


def printify_opener(inner_html: str, num: int, marker_id: str) -> str:
    """Make the opener's page labels depend only on the print page counter.

    Website opener labels are generated from the previous PDF build. Keeping them
    in the render input would create a metadata/layout cycle. The print edition
    therefore removes those labels before layout and obtains its chapter folio
    from CSS ``counter(page)`` on the final rendered page.
    """
    soup = BeautifulSoup(inner_html, "lxml")
    hero = soup.select_one(".chapter-hero")
    if hero is None:
        raise RuntimeError(f"chapter {num}: opener has no .chapter-hero")
    hero["id"] = marker_id
    chapter_num = soup.select_one(".chapter-num")
    if chapter_num is None:
        raise RuntimeError(f"chapter {num}: opener has no .chapter-num")
    chapter_num.clear()
    chapter_num.string = f"ГЛАВА {num}"
    for page_label in soup.select(".si-page"):
        page_label.decompose()
    body = soup.find("body")
    return "".join(str(c) for c in body.contents) if body else str(soup)


def validate_font_files() -> list[dict[str, str]]:
    """Pin every font used by print CSS so fallback cannot silently repaginate."""
    records: list[dict[str, str]] = []
    for filename, expected_sha256 in FONT_FILES.items():
        font_path = FONT_DIR / filename
        if not font_path.is_file():
            raise RuntimeError(f"required PDF font is missing: {font_path}")
        actual_sha256 = hashlib.sha256(font_path.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise RuntimeError(
                f"PDF font drift: {font_path}: expected {expected_sha256}, got {actual_sha256}"
            )
        records.append(
            {"file": str(font_path.relative_to(ROOT)), "sha256": actual_sha256}
        )
    return records


def build_projects_appendix() -> str:
    parts = ['<div class="chapter-break"><h1>Проекты</h1><p>Двенадцать готовых мини-проектов с открытым исходным кодом — от «Крестики-нолики» до полноценного космического шутера. Исходный код и живая версия каждого — на сайте курса.</p></div>']
    for entry in be.PROJECTS:
        html_text = (SITE / "projects" / entry["slug"] / "index.html").read_text(encoding="utf-8")
        inner = strip_wrapper(be.extract_project(html_text))
        parts.append(f'<div id="proj-{entry["slug"]}" class="project-entry">{inner}</div>')
    return "".join(parts)


def build_full_html() -> tuple[
    str,
    list[tuple[str, int]],
    list[tuple[str, str]],
    str,
]:
    parts = [build_title_page(), build_copyright_page(), build_toc_entries()]
    chapter_markers: list[tuple[str, int]] = []  # (marker_id, chapter_num)
    page_markers: list[tuple[str, str]] = []  # (marker_id, canonical URL)

    for rel_path, _title in be.FRONT_MATTER:
        marker = "fm-" + rel_path.rsplit("/", 1)[-1].replace(".html", "")
        html_text = (SITE / rel_path).read_text(encoding="utf-8")
        inner = printify_notebook_cards(strip_wrapper(be.extract_article(html_text)))
        parts.append(f'<div id="{marker}" class="chapter-break">{inner}</div>')
        page_markers.append((marker, f"/{rel_path}"))

    for num in range(1, 25):
        pages = be.chapter_pages(num)
        for i, (rel_path, _title) in enumerate(pages):
            html_text = (SITE / rel_path).read_text(encoding="utf-8")
            if i == 0:
                marker_id = f"marker-ch-{num}"
                inner = printify_opener(
                    strip_wrapper(be.extract_opener(html_text)), num, marker_id
                )
                parts.append(inner)
                chapter_markers.append((marker_id, num))
            else:
                marker_id = f"marker-page-{num:02d}-{i:03d}"
                inner = printify_notebook_cards(strip_wrapper(be.extract_article(html_text)))
                parts.append(f'<div id="{marker_id}">{inner}</div>')
            page_markers.append((marker_id, f"/{rel_path}"))

    project_marker = "marker-projects"
    projects_html = build_projects_appendix().replace(
        '<div class="chapter-break">',
        f'<div id="{project_marker}" class="chapter-break">',
        1,
    )
    parts.append(projects_html)

    idx_html = (SITE / "predmetnyj-ukazatel.html").read_text(encoding="utf-8")
    idx_inner = strip_wrapper(be.extract_article(idx_html))
    parts.append(f'<div id="marker-index" class="chapter-break">{idx_inner}</div>')

    full_html = (
        "<html lang='ru'><head><meta charset='utf-8'>"
        f"<title>{BOOK_TITLE}: {BOOK_SUBTITLE}</title>"
        f"<meta name='author' content='{BOOK_AUTHOR}'>"
        f"<meta name='description' content='{BOOK_DESCRIPTION}'>"
        f"<style>{PRINT_CSS}</style></head><body>{''.join(parts)}</body></html>"
    )
    return full_html, chapter_markers, page_markers, project_marker


def resolve_anchor_pages(doc, marker_ids: set[str]) -> dict[str, int]:
    """Return first one-based WeasyPrint page occupied by each marked element.

    WeasyPrint repeats an element anchor in ``page.anchors`` when the marked
    wrapper spans more than one physical page. The first occurrence is the
    target-counter destination and therefore the authoritative start page.
    """
    resolved: dict[str, int] = {}
    for page_index, page in enumerate(doc.pages, start=1):
        for marker_id in marker_ids.intersection(page.anchors):
            resolved.setdefault(marker_id, page_index)
    missing = marker_ids.difference(resolved)
    if missing:
        raise RuntimeError(f"PDF render lost anchors: {', '.join(sorted(missing))}")
    return resolved


def source_fingerprint(full_html: str, font_records: list[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    digest.update(b"cartesian-school-book-layout-v1\0")
    digest.update(
        (
            f"weasyprint={WEASYPRINT_VERSION}\0pypdf={version('pypdf')}\0"
            f"source_date_epoch={SOURCE_DATE_EPOCH}\0"
        ).encode()
    )
    normalized_html = full_html.replace(ROOT.as_uri(), "file://<REPOSITORY_ROOT>")
    digest.update(normalized_html.encode("utf-8"))
    digest.update(b"\0cover\0")
    digest.update(COVER_PDF.read_bytes())
    for record in font_records:
        digest.update(b"\0font\0")
        digest.update(record["file"].encode())
        digest.update(b"\0")
        digest.update(record["sha256"].encode())
    return digest.hexdigest()


def write_pagination_metadata(
    *,
    full_html: str,
    font_records: list[dict[str, str]],
    final_total_pages: int,
    final_anchor_pages: dict[str, int],
    chapter_markers: list[tuple[str, int]],
    page_markers: list[tuple[str, str]],
    project_marker: str,
) -> None:
    chapter_starts = {
        num: final_anchor_pages[marker_id] for marker_id, num in chapter_markers
    }
    if sorted(chapter_starts) != list(range(1, 25)):
        raise RuntimeError("pagination metadata does not contain exactly chapters 1..24")
    starts = [chapter_starts[num] for num in range(1, 25)]
    if starts != sorted(set(starts)):
        raise RuntimeError(f"chapter starts are not strictly increasing: {starts}")

    projects_start = final_anchor_pages[project_marker]
    if projects_start <= chapter_starts[24]:
        raise RuntimeError("projects appendix does not start after chapter 24")

    chapter_data: dict[str, dict[str, object]] = {}
    canonical_chapters = {item.number: item for item in chapters()}
    for num in range(1, 25):
        next_boundary = chapter_starts[num + 1] if num < 24 else projects_start
        item = canonical_chapters[num]
        chapter_data[f"{num:02d}"] = {
            "number": num,
            "title": item.title,
            "url": item.url,
            "start_page": chapter_starts[num],
            "end_page": next_boundary - 1,
        }

    url_pages: dict[str, int] = {}
    for marker_id, url in page_markers:
        if url in url_pages:
            raise RuntimeError(f"duplicate canonical page URL in PDF pagination: {url}")
        url_pages[url] = final_anchor_pages[marker_id]

    reader = PdfReader(str(OUT))
    if len(reader.pages) != final_total_pages:
        raise RuntimeError(
            f"final PDF page tree has {len(reader.pages)} pages, expected {final_total_pages}"
        )
    first_width = float(reader.pages[0].mediabox.width)
    first_height = float(reader.pages[0].mediabox.height)
    for physical_page, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - first_width) > 0.01 or abs(height - first_height) > 0.01:
            raise RuntimeError(
                f"PDF trim drift on physical page {physical_page}: {width}x{height} pt"
            )

    metadata = {
        "schema_version": "1.0.0",
        "generated_from": f"sha256:{source_fingerprint(full_html, font_records)}",
        "pdf_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "render_engine": f"WeasyPrint {WEASYPRINT_VERSION}",
        "pdf_writer": f"pypdf {version('pypdf')}",
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "page_format": {
            "width_mm": round(first_width * 25.4 / 72, 3),
            "height_mm": round(first_height * 25.4 / 72, 3),
        },
        "front_matter_numbering": (
            "physical page 1 cover unnumbered; physical page 2 title unnumbered; "
            "continuous Arabic physical folios thereafter"
        ),
        "chapter_start_policy": (
            "recto/right-hand via break-before:right; inserted blank pages count"
        ),
        "total_pages": final_total_pages,
        "fonts": font_records,
        "chapters": chapter_data,
        "pages": dict(sorted(url_pages.items())),
    }
    PAGINATION_OUT.parent.mkdir(parents=True, exist_ok=True)
    PAGINATION_OUT.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def merge_cover(content_pdf_path: Path, out_path: Path) -> None:
    """Prepends the already-approved cover design (design/exports/cover_concept_v1.pdf,
    a real vector/text HTML->PDF render, not a rasterized low-DPI image) as the
    literal first physical page. The cover is unnumbered, matching normal book
    convention — see PRINT_CSS's `@page :first` for the title page immediately
    after it.

    Uses PdfWriter.append() (not per-page add_page()) specifically so the PDF
    outline/bookmarks WeasyPrint auto-generates from headings survive the merge
    — append() re-targets outline destinations to the new page indices;
    add_page() only copies page content, silently dropping the outline tree.
    """
    writer = PdfWriter()
    content_reader = PdfReader(str(content_pdf_path))

    cover_reader = PdfReader(str(COVER_PDF))
    cover_page = cover_reader.pages[0]
    # Match the book's trim size exactly (cover is 432x648pt / 6x9in; book is
    # 152mm x 229mm ~= 430.87x649.13pt — a sub-point rounding difference).
    target_w = float(content_reader.pages[0].mediabox.width)
    target_h = float(content_reader.pages[0].mediabox.height)
    cover_page.scale_to(target_w, target_h)
    writer.append(cover_reader)

    writer.append(content_reader, import_outline=True)

    if content_reader.metadata:
        writer.add_metadata(content_reader.metadata)

    with open(out_path, "wb") as f:
        writer.write(f)


def main() -> None:
    # FontTools reads SOURCE_DATE_EPOCH when serializing embedded subsets.
    # Override any caller-specific value so this canonical build has one
    # explicit, portable timestamp contract.
    os.environ["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    if not COVER_PDF.is_file():
        raise RuntimeError(f"cover PDF is missing: {COVER_PDF}")
    font_records = validate_font_files()
    full_html, chapter_markers, page_markers, project_marker = build_full_html()

    doc = HTML(string=full_html, base_url=str(SITE)).render()
    total_pages = len(doc.pages)
    marker_ids = {
        marker_id for marker_id, _num in chapter_markers
    } | {
        marker_id for marker_id, _url in page_markers
    } | {project_marker, "marker-index"}
    anchor_pages = resolve_anchor_pages(doc, marker_ids)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp_content_pdf = OUT.parent / "_content_tmp.pdf"
    doc.write_pdf(str(tmp_content_pdf))
    merge_cover(tmp_content_pdf, OUT)
    tmp_content_pdf.unlink()

    # +1 physical page for the merged, WeasyPrint-external cover.
    final_total_pages = total_pages + 1
    final_anchor_pages = {marker_id: page + 1 for marker_id, page in anchor_pages.items()}

    write_pagination_metadata(
        full_html=full_html,
        font_records=font_records,
        final_total_pages=final_total_pages,
        final_anchor_pages=final_anchor_pages,
        chapter_markers=chapter_markers,
        page_markers=page_markers,
        project_marker=project_marker,
    )

    print(f"Записано: {OUT.relative_to(ROOT)} ({final_total_pages} страниц)")
    for marker_id, num in chapter_markers:
        print(f"  Глава {num:>2}: физическая стр. {final_anchor_pages[marker_id]}")
    print(f"  Предметный указатель: физическая стр. {final_anchor_pages['marker-index']}")
    print(f"  Всего физических страниц: {final_total_pages}")
    print(f"Записано: {PAGINATION_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
