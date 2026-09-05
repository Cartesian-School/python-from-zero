"""Narrow legal-consistency guards for the dual-license model.

Educational/editorial content (book/course prose, diagrams,
assignments/instructions, the website's own editorial material) is
CC BY-NC-SA 4.0. ALL code — including inline code snippets/listings shown
inside the book/course text, not just standalone scripts/projects — is MIT
(LICENSE-CODE.md) unless a file/directory states otherwise. Code never
becomes CC-licensed merely by being printed inside a CC-licensed page.

These tests do not re-litigate that choice — they guard against the two
licenses silently blending back into one blanket grant (the PDF copyright
page used to embed the full MIT text from LICENSE.md as if MIT governed the
whole book), and against the two formats independently drifting apart (the
website once described inline code snippets as CC-licensed while the
PDF/EPUB notice already said code was MIT — this file's test C guards
against that exact regression).

Lettering (A-H) matches the licensing closure's own required-assertions
list.
"""

from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path
from types import ModuleType

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LICENSE_PAGE = SITE / "front-matter" / "litsenziya.html"
PDF_PATH = ROOT / "book" / "pdf" / "готовая книга.pdf"
EPUB_PATH = ROOT / "book" / "epub" / "python-s-nulya.epub"

CC_IDENTIFIER = "CC BY-NC-SA 4.0"
CC_CANONICAL_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"


def _load_module(name: str, path: Path) -> ModuleType:
    """Load a scripts/*.py module directly, without making scripts a package
    (same approach as tests/test_ru_content_audit_inventory.py)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_epub_module() -> ModuleType:
    return _load_module("build_epub", ROOT / "scripts" / "build_epub.py")


def test_a_website_states_educational_content_is_cc() -> None:
    text = LICENSE_PAGE.read_text(encoding="utf-8")
    assert CC_IDENTIFIER in text
    index_text = (SITE / "index.html").read_text(encoding="utf-8")
    assert CC_IDENTIFIER in index_text


def test_b_website_states_code_is_mit() -> None:
    text = LICENSE_PAGE.read_text(encoding="utf-8")
    assert "MIT" in text
    assert "Программный код" in text  # the dedicated code-licensing section


def test_c_license_page_does_not_classify_inline_snippets_as_cc_only() -> None:
    """Regression guard for the exact inconsistency this closure fixed: the
    website used to say inline lesson code snippets were part of the prose
    and thus CC-licensed ("...фрагменты кода прямо внутри текста урока
    ...часть учебного изложения и распространяются вместе с текстом урока на
    условиях CC BY-NC-SA 4.0"), while the PDF/EPUB notice already said code
    was MIT. That exact old (wrong) sentence must be gone..."""
    text = LICENSE_PAGE.read_text(encoding="utf-8")
    assert "распространяются вместе с текстом урока на условиях" not in text

    # ...replaced by an explicit statement that code, INCLUDING inline
    # snippets/listings shown inside lesson text, is MIT — not CC-only.
    lowered = text.lower()
    assert "фрагмент" in lowered
    assert "внутри текста урока" in lowered
    snippet_idx = lowered.find("внутри текста урока")
    window = lowered[max(0, snippet_idx - 200) : snippet_idx + 400]
    assert "mit" in window


def test_d_pdf_notice_states_content_cc_and_code_mit() -> None:
    """Physical page 3 (0-indexed 2): cover(1), title(2), copyright(3) — see
    build_pdf.py's build_full_html() ordering and its own
    front_matter_numbering pagination metadata note."""
    if not PDF_PATH.exists():
        pytest.skip(f"PDF not built: {PDF_PATH}")
    reader = PdfReader(str(PDF_PATH))
    text = reader.pages[2].extract_text()
    assert CC_IDENTIFIER in text
    assert "MIT License" in text
    # The full MIT boilerplate must never be embedded here — a short, scoped
    # software reference is the accurate statement for a book copyright page.
    assert "THE SOFTWARE IS PROVIDED" not in text
    assert "Permission is hereby granted" not in text


def test_e_epub_notice_states_content_cc_and_code_mit() -> None:
    if not EPUB_PATH.exists():
        pytest.skip(f"EPUB not built: {EPUB_PATH}")
    with zipfile.ZipFile(EPUB_PATH) as z:
        copyright_xhtml = z.read("EPUB/copyright.xhtml").decode("utf-8")
        opf_names = [n for n in z.namelist() if n.endswith(".opf")]
        assert opf_names, "EPUB package has no .opf document"
        opf = z.read(opf_names[0]).decode("utf-8")
    assert CC_IDENTIFIER in copyright_xhtml
    assert "MIT License" in copyright_xhtml
    assert "<dc:rights>" in opf
    assert CC_IDENTIFIER in opf
    assert "MIT License" in opf


def test_f_license_md_map_states_content_cc_and_code_mit() -> None:
    root_license = (ROOT / "LICENSE.md").read_text(encoding="utf-8")
    # Must read as a map between two licenses, never a bare, unscoped MIT
    # grant for the whole repository (the pre-fix shape this closure
    # replaced).
    assert not root_license.lstrip().startswith("MIT License")
    assert CC_IDENTIFIER in root_license or "CC BY-NC-SA" in root_license
    assert "MIT" in root_license
    # Must explicitly say code (including inline snippets) is MIT, not just
    # "source code" in the abstract — this is the exact scope this closure
    # had to make unambiguous.
    assert "inline code snippet" in root_license.lower() or "snippet" in root_license.lower()


def test_g_readme_states_content_cc_and_code_mit() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert CC_IDENTIFIER in readme
    assert "MIT" in readme
    assert "inline code snippet" in readme.lower() or "snippet" in readme.lower()


def test_h_repository_code_license_remains_mit() -> None:
    code_license = (ROOT / "LICENSE-CODE.md").read_text(encoding="utf-8")
    assert "MIT License" in code_license
    assert "Permission is hereby granted" in code_license


def test_no_contradiction_between_website_and_publication_code_scope() -> None:
    """The two independent sources of truth for code licensing (the website
    license page, and the shared PDF/EPUB rights-notice constant) must agree:
    both must say MIT, and neither may say CC governs code."""
    be = _build_epub_module()
    assert "MIT" in be.RIGHTS_NOTICE_PLAIN
    assert CC_IDENTIFIER in be.RIGHTS_NOTICE_PLAIN

    website_text = LICENSE_PAGE.read_text(encoding="utf-8")
    assert "MIT" in website_text
    assert CC_IDENTIFIER in website_text


def test_i_official_cc_canonical_url_is_exact() -> None:
    license_text = LICENSE_PAGE.read_text(encoding="utf-8")
    assert CC_CANONICAL_URL in license_text

    be = _build_epub_module()
    assert be.CONTENT_LICENSE_URL == CC_CANONICAL_URL

    seo = _load_module("build_seo_meta", ROOT / "scripts" / "build_seo_meta.py")
    assert seo.CONTENT_LICENSE_URL == CC_CANONICAL_URL


def test_j_approved_kratko_wording_replaced_harvard_cs50_removed() -> None:
    """Product Owner-approved wording correction: the "Кратко" callout's two
    opening paragraphs were replaced verbatim, and every Harvard/CS50
    reference was removed from this page (it previously compared the
    license to Harvard CS50's — see git history of this test file for the
    superseded wording). Scoped to this page only; Harvard/CS50 mentions
    elsewhere in the course (e.g. Chapter reference material) are untouched
    and out of scope here."""
    text = LICENSE_PAGE.read_text(encoding="utf-8")

    # A: new first paragraph present.
    assert "Все материалы курса, включая прозаический текст" in text
    # B: new code paragraph present.
    assert "Все примеры кода, фрагменты и полные проекты" in text
    # C: old wording absent.
    assert "Текст курса — проза книги" not in text
    # D: Harvard/CS50 fully absent from this page.
    assert "Harvard" not in text
    assert "CS50" not in text

    # E/F: the dual-license model itself is unchanged by this wording fix.
    assert CC_IDENTIFIER in text
    assert "MIT" in text
