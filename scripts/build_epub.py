#!/usr/bin/env python3
"""Собирает EPUB-издание книги из готовых HTML-страниц site/ (book/python-s-nulya.epub).

Извлекает содержимое <article> (для обычных страниц) или .chapter-hero+.section-list
(для страниц-открывашек глав) из уже собранных HTML-файлов, убирает элементы навигации
сайта (breadcrumb, section-nav, header, sidebar) и собирает главы в EPUB со сквозным
оглавлением, обложкой и общим стилем.
"""

import importlib
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "book" / "epub" / "python-s-nulya.epub"

MANIFEST = json.loads((ROOT / "manifest" / "coverage_manifest.json").read_text(encoding="utf-8"))

FRONT_MATTER = [
    ("front-matter/ob-avtore.html", "Об авторе"),
    ("front-matter/o-tehnicheskom-recenzente.html", "О техническом рецензенте"),
    ("front-matter/vvedenie.html", "Введение"),
]


def chapter_title(num: int) -> str:
    for ch in MANIFEST["chapters"]:
        if ch.get("number") == num:
            return ch["title"].replace("*", "")
    raise KeyError(num)


def chapter_pages(num: int) -> list[tuple[str, str]]:
    mod = importlib.import_module(f"build_chapter_{num:02d}")
    return [(f"chapters/glava-{num:02d}/{href}", title) for href, title in mod.PAGES]


def rewrite_links(tag) -> None:
    # notebooks and project source files live in the git repo, not inside the EPUB
    # package — turn those references into plain text instead of dead/invalid links.
    for a in list(tag.find_all("a", href=True)):
        href = a["href"]
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        if "/notebooks/" in href or "/projects/" in href:
            a.unwrap()
            continue
        if ".html" in href:
            a["href"] = href.replace(".html", ".xhtml")


def extract_article(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    article = soup.find("article")
    for cls in ("breadcrumb", "section-kicker", "section-nav"):
        node = article.find("div", class_=cls)
        if node:
            node.decompose()
    # copy-to-clipboard buttons rely on onclick JS with no purpose in an e-reader —
    # drop them so pages don't need to be flagged as "scripted" content.
    for btn in article.find_all("button", class_="copy-btn"):
        btn.decompose()
    rewrite_links(article)
    inner = "".join(str(c) for c in article.contents)
    return f"<html><body>{inner}</body></html>"


def extract_opener(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    hero = soup.find("div", class_="chapter-hero")
    section_list = soup.find("div", class_="section-list")
    if section_list:
        rewrite_links(section_list)
    inner = (str(hero) if hero else "") + (str(section_list) if section_list else "")
    return f"<html><body>{inner}</body></html>"


def ncx_id(file_name: str) -> str:
    """XML NCName-safe id for use in toc.ncx (no '/' or '.')."""
    return "nav_" + file_name.replace("/", "_").replace(".", "_")


def build_item(rel_html_path: str, title: str, *, is_opener: bool) -> epub.EpubHtml:
    src = SITE / rel_html_path
    html_text = src.read_text(encoding="utf-8")
    content = (extract_opener if is_opener else extract_article)(html_text)
    file_name = rel_html_path.replace(".html", ".xhtml")
    item = epub.EpubHtml(title=title, file_name=file_name, lang="ru")
    item.content = content
    if "<svg" in content:
        item.properties.append("svg")
    depth = rel_html_path.count("/")
    css_href = "../" * depth + "assets/css/theory.css"
    item.add_link(href=css_href, rel="stylesheet", type="text/css")
    return item


def main() -> None:
    book = epub.EpubBook()
    book.set_identifier("cartesian-school-python-s-nulya-2026")
    book.set_title("Python с нуля: программирование, графика, приложения и игры")
    book.set_language("ru")
    book.add_author("Siergej Sobolewski")
    book.add_metadata("DC", "description", "Книга для начинающих: Python 3.14, графика на Turtle, приложения на Tkinter, игры на Pygame и веб-разработка на Flask.")
    book.add_metadata("DC", "publisher", "Cartesian School")

    css_bytes = (SITE / "assets" / "css" / "theory.css").read_bytes()
    css_item = epub.EpubItem(uid="theory_css", file_name="assets/css/theory.css", media_type="text/css", content=css_bytes)
    book.add_item(css_item)

    cover_path = ROOT / "design" / "exports" / "cover_concept_v1.png"
    book.set_cover("cover.png", cover_path.read_bytes())

    toc = []
    spine = ["nav"]

    fm_links = []
    for rel_path, title in FRONT_MATTER:
        item = build_item(rel_path, title, is_opener=False)
        book.add_item(item)
        spine.append(item)
        fm_links.append(epub.Link(item.file_name, title, ncx_id(item.file_name)))
    toc.append((epub.Section("Вводные материалы"), tuple(fm_links)))

    for num in range(1, 25):
        pages = chapter_pages(num)
        ch_links = []
        for i, (rel_path, title) in enumerate(pages):
            item = build_item(rel_path, title, is_opener=(i == 0))
            book.add_item(item)
            spine.append(item)
            ch_links.append(epub.Link(item.file_name, title, ncx_id(item.file_name)))
        toc.append((epub.Section(f"Глава {num}: {chapter_title(num).split(': ', 1)[-1]}"), tuple(ch_links)))

    idx_item = build_item("predmetnyj-ukazatel.html", "Предметный указатель", is_opener=False)
    book.add_item(idx_item)
    spine.append(idx_item)
    toc.append(epub.Link(idx_item.file_name, "Предметный указатель", ncx_id(idx_item.file_name)))

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine

    OUT.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(OUT), book)
    print(f"Записано: {OUT.relative_to(ROOT)} ({len(spine) - 1} страниц)")


if __name__ == "__main__":
    main()
