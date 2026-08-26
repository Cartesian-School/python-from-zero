#!/usr/bin/env python3
"""Programmatic validation of the publication artifacts (PDF + EPUB).

Used standalone (python scripts/validate_book.py) or as the final gate inside
build_book.py. Every check that fails is collected and reported together —
the point is a complete picture of what's wrong in one run, not stopping at
the first problem. Exits non-zero if anything failed, per the "build must
fail loudly" requirement: a publication pipeline must never silently produce
an incomplete artifact.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_pagination import pagination
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "book" / "pdf" / "готовая книга.pdf"
EPUB_PATH = ROOT / "book" / "epub" / "python-s-nulya.epub"


def validate_pdf(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.exists():
        return [f"PDF missing: {path}"]

    try:
        reader = PdfReader(str(path))
    except Exception as e:
        return [f"PDF unreadable/corrupt: {e}"]

    try:
        page_count = len(reader.pages)
    except Exception as e:
        return [f"PDF page list unreadable: {e}"]

    expected_pages = int(pagination()["total_pages"])
    if page_count != expected_pages:
        errors.append(
            f"page count {page_count} != generated pagination total {expected_pages}"
        )

    # No corrupt pages: every page must at least yield a mediabox and allow
    # text extraction without raising.
    sizes = set()
    for i, page in enumerate(reader.pages):
        try:
            box = page.mediabox
            sizes.add((round(float(box.width), 1), round(float(box.height), 1)))
            page.extract_text()
        except Exception as e:
            errors.append(f"page {i + 1} is corrupt/unreadable: {e}")

    if len(sizes) > 1:
        errors.append(f"inconsistent page dimensions across the document: {sorted(sizes)}")

    meta = reader.metadata or {}
    if not meta.get("/Title"):
        errors.append("PDF metadata missing /Title")
    if not meta.get("/Author"):
        errors.append("PDF metadata missing /Author")

    outline = reader.outline or []
    if len(outline) == 0:
        errors.append("PDF has no bookmarks/outline (internal navigation missing)")

    return errors


def validate_epub(path: Path) -> list[str]:
    if not path.exists():
        return [f"EPUB missing: {path}"]

    from epubcheck import EpubCheck

    try:
        result = EpubCheck(str(path))
    except Exception as e:
        return [f"epubcheck failed to run: {e}"]

    if result.valid:
        return []
    return [f"epubcheck: {m}" for m in result.messages]


def main() -> None:
    all_errors: list[str] = []

    print(f"== PDF: {PDF_PATH.relative_to(ROOT)} ==")
    pdf_errors = validate_pdf(PDF_PATH)
    if pdf_errors:
        for e in pdf_errors:
            print(f"  СБОЙ: {e}")
        all_errors.extend(f"[pdf] {e}" for e in pdf_errors)
    else:
        reader = PdfReader(str(PDF_PATH))
        print(f"  OK — {len(reader.pages)} pages, metadata present, {len(reader.outline)} bookmarks, uniform page size")

    print(f"\n== EPUB: {EPUB_PATH.relative_to(ROOT)} ==")
    epub_errors = validate_epub(EPUB_PATH)
    if epub_errors:
        for e in epub_errors:
            print(f"  СБОЙ: {e}")
        all_errors.extend(f"[epub] {e}" for e in epub_errors)
    else:
        print("  OK — epubcheck: 0 errors")

    if all_errors:
        print(f"\nВАЛИДАЦИЯ ПУБЛИКАЦИИ: FAIL ({len(all_errors)} problem(s))", file=sys.stderr)
        sys.exit(1)

    print("\nВАЛИДАЦИЯ ПУБЛИКАЦИИ: PASS")


if __name__ == "__main__":
    main()
