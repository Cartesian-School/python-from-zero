"""PL locale content discovery and metadata.

PL pages are machine-translated derivatives of the RU pages written by
scripts/build_polish_course.py — same filenames, same page order, just under
site/pl/chapters/rozdzial-NN/ instead of site/chapters/glava-NN/ (and
correspondingly for front matter/projects). There is no PL equivalent of
data/chapters.json (RU's canonical chapter metadata source), so this reuses
locale_ru's own page discovery purely for page identity (slugs, filenames,
ordering — all locale-neutral) and rewrites the site path prefix; PL titles
are read back from the already-translated PL HTML itself (each page's own
<h1>, via book_shared.extract_page_title), never re-derived independently,
so the book can never drift from what a PL reader actually sees on the page.

Contains only what docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md section 4
permits a language edition to contribute — no rendering, packaging, or
pagination logic.
"""

from __future__ import annotations

from functools import cache
from pathlib import Path

import book_shared as bs
from build_polish_course import FRONT_MATTER_NAMES

from book_pipeline import locale_ru
from book_pipeline.config import BookLocaleConfig, ProjectEntry

ROOT = Path(__file__).resolve().parent.parent.parent
SITE = ROOT / "site" / "pl"

BOOK_TITLE = "Python od zera"
BOOK_SUBTITLE = "programowanie, grafika, aplikacje i gry"
BOOK_AUTHOR = "Siergej Sobolewski"
BOOK_AUTHOR_ROLE = "Software & AI Engineer, założyciel Cartesian School"
BOOK_DESCRIPTION = (
    "Książka dla początkujących: Python 3.14, grafika w Turtle, aplikacje w "
    "Tkinter, gry w Pygame i tworzenie stron internetowych we Flasku."
)
SITE_URL_DISPLAY = "cartesianschool.org"

RIGHTS_HOLDER = "Siergej Sobolewski / Cartesian School"
CONTENT_LICENSE_NAME = (
    "Creative Commons Uznanie autorstwa-Użycie niekomercyjne-Na tych samych "
    "warunkach 4.0 Międzynarodowe (CC BY-NC-SA 4.0)"
)
CONTENT_LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pl"

RIGHTS_NOTICE_PLAIN = (
    f"© {RIGHTS_HOLDER}. "
    f"Tekst książki i oryginalne materiały dydaktyczne: {CONTENT_LICENSE_NAME}. "
    f"{CONTENT_LICENSE_URL} "
    "Kod źródłowy — w tym fragmenty kodu i listingi w tekście książki, a nie "
    "tylko osobne projekty i skrypty — o ile nie wskazano inaczej, jest "
    "udostępniany na warunkach licencji MIT."
)

RIGHTS_NOTICE_PARAGRAPHS_HTML = (
    f"<p>© {RIGHTS_HOLDER}</p>"
    "<p>Tekst książki i oryginalne materiały dydaktyczne: "
    f'<a href="{CONTENT_LICENSE_URL}">{CONTENT_LICENSE_NAME}</a>.</p>'
    f"<p>{CONTENT_LICENSE_URL}</p>"
    "<p>Kod źródłowy — w tym fragmenty kodu i listingi w tekście książki, a "
    "nie tylko osobne projekty i skrypty — o ile nie wskazano inaczej, jest "
    "udostępniany na warunkach licencji MIT.</p>"
)


def _pl_path(ru_rel_path: str) -> str:
    """chapters/glava-NN/x.html -> chapters/rozdzial-NN/x.html (relative to
    site/pl/); a bare front-matter/x.html gets its PL-named counterpart via
    FRONT_MATTER_NAMES."""
    if ru_rel_path.startswith("chapters/glava-"):
        rest = ru_rel_path[len("chapters/glava-"):]
        num, _, tail = rest.partition("/")
        return f"chapters/rozdzial-{num}/{tail}"
    if ru_rel_path.startswith("front-matter/"):
        fname = ru_rel_path.split("/", 1)[1]
        return f"front-matter/{FRONT_MATTER_NAMES[fname]}"
    raise ValueError(f"no PL path mapping for {ru_rel_path!r}")


def _extract_title(rel_path: str) -> str:
    return bs.extract_page_title((SITE / rel_path).read_text(encoding="utf-8"))


FRONT_MATTER: list[tuple[str, str]] = [
    (pl_rel_path, _extract_title(pl_rel_path))
    for pl_rel_path in (_pl_path(ru_rel_path) for ru_rel_path, _ru_title in locale_ru.FRONT_MATTER)
]


@cache
def chapter_pages(num: int) -> list[tuple[str, str]]:
    return [
        (pl_rel_path, _extract_title(pl_rel_path))
        for pl_rel_path in (_pl_path(ru_rel_path) for ru_rel_path, _ru_title in locale_ru.chapter_pages(num))
    ]


def chapter_title(num: int) -> str:
    return chapter_pages(num)[0][1]


def chapter_canonical_url(num: int) -> str:
    return f"/pl/chapters/rozdzial-{num:02d}/index.html"


PROJECT_ENTRIES = [
    ProjectEntry(
        slug=entry.slug,
        title=_extract_title(f"projects/{entry.slug}/index.html"),
    )
    for entry in locale_ru.PROJECT_ENTRIES
]

CONFIG = BookLocaleConfig(
    language="pl",
    html_lang="pl",
    site=SITE,
    assets_root=locale_ru.SITE,  # site/pl/ has no assets of its own; shared verbatim from RU
    book_title=BOOK_TITLE,
    book_subtitle=BOOK_SUBTITLE,
    book_author=BOOK_AUTHOR,
    book_author_role=BOOK_AUTHOR_ROLE,
    book_description=BOOK_DESCRIPTION,
    site_url_display=SITE_URL_DISPLAY,
    rights_holder=RIGHTS_HOLDER,
    content_license_name=CONTENT_LICENSE_NAME,
    content_license_url=CONTENT_LICENSE_URL,
    rights_notice_plain=RIGHTS_NOTICE_PLAIN,
    rights_notice_paragraphs_html=RIGHTS_NOTICE_PARAGRAPHS_HTML,
    chapter_word="Rozdział",
    title_page_kicker="PYTHON 3.14 · OD ZERA",
    page_abbrev="STR.",
    toc_title="Spis treści",
    toc_intro_label="Materiały wprowadzające",
    toc_projects_label="Projekty",
    toc_reference_label="Kompendium",
    toc_index_label="Indeks rzeczowy",
    copyright_edition_line="Wydanie Cartesian School, 2026. Python 3.14.",
    copyright_electronic_line=(
        "Wydanie elektroniczne. Wersja online kursu, interaktywna praktyka w\n"
        f"      przeglądarce i kod źródłowy wszystkich projektów — {SITE_URL_DISPLAY}"
    ),
    projects_intro_html=(
        "<h1>Projekty</h1><p>Dwanaście gotowych mini-projektów z otwartym "
        "kodem źródłowym — od „Kółko i krzyżyk” po pełnoprawną kosmiczną "
        "strzelankę. Kod źródłowy i działająca wersja każdego z nich — na "
        "stronie kursu.</p>"
    ),
    epub_copyright_title="Informacje prawne",
    epub_identifier="cartesian-school-python-od-zera-2026",
    url_path_prefix="/pl",
    index_relpath="indeks-rzeczowy.html",
    pdf_output_path=ROOT / "book" / "pdf" / "python-od-zera-pl.pdf",
    pagination_output_path=ROOT / "data" / "book-pagination-pl.json",
    cover_pdf_path=ROOT / "design" / "exports" / "cover_concept_v1_pl.pdf",
    epub_output_path=ROOT / "book" / "epub" / "python-od-zera-pl.epub",
    cover_png_path=ROOT / "design" / "exports" / "cover_concept_v1_pl.png",
    front_matter=FRONT_MATTER,
    project_entries=PROJECT_ENTRIES,
    chapter_pages=chapter_pages,
    chapter_title=chapter_title,
    chapter_canonical_url=chapter_canonical_url,
)
