#!/usr/bin/env python3
"""Собирает единый печатный PDF книги (book/pdf/готовая книга.pdf) через WeasyPrint.

Переиспользует извлечение содержимого страниц из build_epub.py (тот же <article> /
.chapter-hero+.section-list разбор), но склеивает всё в один HTML-документ с печатной
типографикой: обложка (уже готовый дизайн-концепт, склеен как первая физическая
страница через pypdf), титульный лист, страница авторских прав, оглавление с реальными
номерами страниц (CSS target-counter — один проход рендеринга, без ручного пересчёта),
разрыв страницы перед каждой главой, колонтитулы, приложение с проектами, предметный
указатель.

Нумерация страниц — сквозная (обложка не нумеруется, титульный лист не нумеруется,
всё остальное — одна арабская последовательность). Сознательный выбор: раздельная
нумерация (римские цифры во вводных материалах + перезапуск на "1" в главе 1, как в
каноническом оглавлении python_book_table_of_contents_ru.md) была бы точнее, но вводит
риск случайно нарушить главное инвариант «глава не может начинаться раньше канонической
страницы» — при сквозной нумерации фактическая страница каждой главы только растёт по
мере добавления нового содержимого (обложка, оглавление, страница авторских прав,
приложение с проектами), никогда не уменьшается, так что инвариант остаётся тривиально
верным.

Все проверки пагинации ОБЯЗАТЕЛЬНЫ: main() завершается sys.exit(1), если хоть одна не
прошла — сборка публикации не должна тихо создавать неполный артефакт.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_epub as be
from bs4 import BeautifulSoup
from pypdf import PdfReader, PdfWriter
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "book" / "pdf" / "готовая книга.pdf"
COVER_PDF = ROOT / "design" / "exports" / "cover_concept_v1.pdf"

BOOK_TITLE = "Python с нуля"
BOOK_SUBTITLE = "программирование, графика, приложения и игры"
BOOK_AUTHOR = "Siergej Sobolewski"
BOOK_AUTHOR_ROLE = "Software & AI Engineer, основатель Cartesian School"
BOOK_DESCRIPTION = "Книга для начинающих: Python 3.14, графика на Turtle, приложения на Tkinter, игры на Pygame и веб-разработка на Flask."
SITE_URL_DISPLAY = "cartesianschool.org"

PRINT_CSS = """
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
        title = be.chapter_title(num).split(": ", 1)[-1]
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


def build_projects_appendix() -> str:
    parts = ['<div class="chapter-break"><h1>Проекты</h1><p>Двенадцать готовых мини-проектов с открытым исходным кодом — от «Крестики-нолики» до полноценного космического шутера. Исходный код и живая версия каждого — на сайте курса.</p></div>']
    for entry in be.PROJECTS:
        html_text = (SITE / "projects" / entry["slug"] / "index.html").read_text(encoding="utf-8")
        inner = strip_wrapper(be.extract_project(html_text))
        parts.append(f'<div id="proj-{entry["slug"]}" class="project-entry">{inner}</div>')
    return "".join(parts)


def build_full_html() -> tuple[str, list[tuple[str, int]]]:
    parts = [build_title_page(), build_copyright_page(), build_toc_entries()]
    markers: list[tuple[str, int]] = []  # (marker_id, chapter_num)

    for rel_path, _title in be.FRONT_MATTER:
        marker = "fm-" + rel_path.rsplit("/", 1)[-1].replace(".html", "")
        html_text = (SITE / rel_path).read_text(encoding="utf-8")
        inner = printify_notebook_cards(strip_wrapper(be.extract_article(html_text)))
        parts.append(f'<div id="{marker}" class="chapter-break">{inner}</div>')

    for num in range(1, 25):
        pages = be.chapter_pages(num)
        for i, (rel_path, _title) in enumerate(pages):
            html_text = (SITE / rel_path).read_text(encoding="utf-8")
            if i == 0:
                marker_id = f"marker-ch-{num}"
                inner = strip_wrapper(be.extract_opener(html_text))
                parts.append(f'<div id="{marker_id}" class="chapter-break">{inner}</div>')
                markers.append((marker_id, num))
            else:
                inner = printify_notebook_cards(strip_wrapper(be.extract_article(html_text)))
                parts.append(inner)

    parts.append(build_projects_appendix())

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
    return full_html, markers


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
    full_html, markers = build_full_html()

    doc = HTML(string=full_html, base_url=str(SITE)).render()
    total_pages = len(doc.pages)

    actual_pages: dict[int, int] = {}
    for marker_id, num in markers:
        for page_index, page in enumerate(doc.pages):
            if marker_id in page.anchors:
                actual_pages[num] = page_index + 1
                break

    index_actual_page = None
    for page_index, page in enumerate(doc.pages):
        if "marker-index" in page.anchors:
            index_actual_page = page_index + 1
            break

    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp_content_pdf = OUT.parent / "_content_tmp.pdf"
    doc.write_pdf(str(tmp_content_pdf))
    merge_cover(tmp_content_pdf, OUT)
    tmp_content_pdf.unlink()

    # +1 physical page for the merged, WeasyPrint-external cover.
    final_total_pages = total_pages + 1
    final_actual_pages = {num: p + 1 for num, p in actual_pages.items()}
    final_index_page = (index_actual_page + 1) if index_actual_page else None

    print(f"Записано: {OUT.relative_to(ROOT)} ({final_total_pages} страниц)")

    failures = []
    for ch in be.MANIFEST["chapters"]:
        num = ch.get("number")
        if num is None or ch["kind"] != "chapter":
            continue
        canonical = ch["canonical_page"]
        actual = final_actual_pages.get(num)
        status = "OK" if actual is not None and actual >= canonical else "СБОЙ"
        print(f"  Глава {num:>2}: канон. стр. {canonical:>3}  →  факт. стр. {actual}  [{status}]")
        if status == "СБОЙ":
            failures.append(f"chapter {num}: actual={actual} < canonical={canonical}")

    idx_manifest = next(c for c in be.MANIFEST["chapters"] if c["id"] == "предметный-указатель")
    idx_canonical = idx_manifest["canonical_page"]
    idx_status = "OK" if final_index_page is not None and final_index_page >= idx_canonical else "СБОЙ"
    print(f"  Указатель: канон. стр. {idx_canonical:>3}  →  факт. стр. {final_index_page}  [{idx_status}]")
    if idx_status == "СБОЙ":
        failures.append(f"index: actual={final_index_page} < canonical={idx_canonical}")

    min_required = be.MANIFEST["min_required_pdf_pages"]
    print(f"\nВсего страниц: {final_total_pages} (нужно ≥ {min_required})")
    if final_total_pages < min_required:
        failures.append(f"total_pages={final_total_pages} < min_required={min_required}")

    if not COVER_PDF.exists():
        failures.append(f"cover PDF missing: {COVER_PDF}")

    if failures:
        print(f"\nСБОЙ СБОРКИ — {len(failures)} проблем(а):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)

    print("Все проверки пагинации пройдены.")


if __name__ == "__main__":
    main()
