#!/usr/bin/env python3
"""Собирает единый печатный PDF книги (book/pdf/gotovaya-kniga.pdf) через WeasyPrint.

Переиспользует извлечение содержимого страниц из build_epub.py (тот же <article> /
.chapter-hero+.section-list разбор), но склеивает всё в один HTML-документ с печатной
типографикой: титульный лист, нумерация страниц, разрыв страницы перед каждой главой.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_epub as be
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "book" / "pdf" / "gotovaya-kniga.pdf"

PRINT_CSS = """
@page {
  size: 152mm 229mm;
  margin: 24mm 20mm 26mm 20mm;
  @bottom-center { content: counter(page); font-family: 'DejaVu Sans', sans-serif; font-size: 9pt; color: #666; }
}
@page :first {
  @bottom-center { content: ""; }
}
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
h1 { font-size: 25pt; margin: 0 0 15pt; }
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
.notebook-card { display: none; }
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
.chapter-hero { break-before: right; padding-top: 30pt; }
.chapter-hero .chapter-num { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-brand-blue); font-size: 10pt; margin-bottom: 6pt; }
.chapter-hero h1 { font-size: 26pt; }
.chapter-hero p { font-size: 11.5pt; color: var(--color-text-muted); max-width: 90%; }
.chapter-meta { display: none; }
.idx-list { list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 20pt; }
.idx-entry { display: flex; justify-content: space-between; gap: 6pt; padding: 3pt 0; font-size: 9pt; border-bottom: 1px dotted var(--color-border-default); break-inside: avoid; }
.idx-term { flex: 1; min-width: 0; }
.idx-page { flex: none; font-family: 'DejaVu Sans Mono', monospace; color: var(--color-text-muted); }
.idx-note { color: var(--color-text-muted); font-size: 8pt; }
.title-page { break-after: page; text-align: center; padding-top: 70mm; }
.title-page .kicker { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-brand-blue); letter-spacing: 2px; font-size: 10pt; }
.title-page h1 { font-size: 30pt; margin: 14pt 0 6pt; }
.title-page .subtitle { font-size: 13pt; color: var(--color-text-muted); margin-bottom: 40pt; }
.title-page .author { font-size: 12pt; font-weight: 700; margin-top: 60pt; }
.title-page .author-role { font-size: 10pt; color: var(--color-text-muted); }
.chapter-break { break-before: page; }
"""


def build_title_page() -> str:
    return """
    <div class="title-page">
      <div class="kicker">PYTHON 3.14 · С НУЛЯ</div>
      <h1>Python с нуля</h1>
      <div class="subtitle">программирование, графика, приложения и игры</div>
      <div class="author">Siergej Sobolewski</div>
      <div class="author-role">Software &amp; AI Engineer, основатель Cartesian School</div>
    </div>
    """


def strip_wrapper(content: str) -> str:
    return content[len("<html><body>"):-len("</body></html>")]


def build_full_html() -> tuple[str, list[tuple[str, int]]]:
    parts = [build_title_page()]
    markers: list[tuple[str, int]] = []  # (marker_id, chapter_num)

    for rel_path, _title in be.FRONT_MATTER:
        html_text = (SITE / rel_path).read_text(encoding="utf-8")
        inner = strip_wrapper(be.extract_article(html_text))
        parts.append(f'<div class="chapter-break">{inner}</div>')

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
                inner = strip_wrapper(be.extract_article(html_text))
                parts.append(inner)

    idx_html = (SITE / "predmetnyj-ukazatel.html").read_text(encoding="utf-8")
    idx_inner = strip_wrapper(be.extract_article(idx_html))
    parts.append(f'<div class="chapter-break">{idx_inner}</div>')

    full_html = f"<html><head><meta charset='utf-8'><style>{PRINT_CSS}</style></head><body>{''.join(parts)}</body></html>"
    return full_html, markers


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

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.write_pdf(str(OUT))
    print(f"Записано: {OUT.relative_to(ROOT)} ({total_pages} страниц)")

    shortfalls = []
    for ch in be.MANIFEST["chapters"]:
        num = ch.get("number")
        if num is None or ch["kind"] != "chapter":
            continue
        canonical = ch["canonical_page"]
        actual = actual_pages.get(num)
        status = "OK" if actual is not None and actual >= canonical else "СБОЙ"
        print(f"  Глава {num:>2}: канон. стр. {canonical:>3}  →  факт. стр. {actual}  [{status}]")
        if status == "СБОЙ":
            shortfalls.append(num)

    print(f"\nВсего страниц: {total_pages} (нужно ≥ {be.MANIFEST['min_required_pdf_pages']})")
    if total_pages < be.MANIFEST["min_required_pdf_pages"]:
        shortfalls.append("total_pages")
    if shortfalls:
        print(f"ПРОБЛЕМА: несоответствия у: {shortfalls}")
    else:
        print("Все проверки пагинации пройдены.")

    return total_pages, actual_pages, shortfalls


if __name__ == "__main__":
    main()
