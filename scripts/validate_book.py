#!/usr/bin/env python3
"""Programmatic validation of the publication artifacts (PDF + EPUB), RU and PL.

Used standalone (python scripts/validate_book.py) or as the final gate inside
build_book.py. Every check that fails is collected and reported together —
the point is a complete picture of what's wrong in one run, not stopping at
the first problem. Exits non-zero if anything failed, per the "build must
fail loudly" requirement: a publication pipeline must never silently produce
an incomplete artifact.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent

CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]")
# A representative sample of common Polish function words/diacritic-bearing
# words that should appear frequently in genuinely-Polish running prose —
# distinct from Russian loanwords/proper nouns that can legitimately appear
# in either language's text (e.g. "Python", "Cartesian School").
POLISH_MARKERS = (
    "jest", "nie", "się", "który", "można", "aby", "które", "być", "języku",
    "programowania", "książki", "rozdział",
)

LOCALES = {
    "ru": {
        "pdf_path": ROOT / "book" / "pdf" / "python-s-nulya-ru.pdf",
        "epub_path": ROOT / "book" / "epub" / "python-s-nulya-ru.epub",
        "language_check": "cyrillic_present",
    },
    "pl": {
        "pdf_path": ROOT / "book" / "pdf" / "python-od-zera-pl.pdf",
        "epub_path": ROOT / "book" / "epub" / "python-od-zera-pl.epub",
        "language_check": "polish_present",
    },
}


def validate_pdf(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.exists():
        return [f"PDF missing: {path}"]

    try:
        reader = PdfReader(str(path))
    except Exception as e:
        return [f"PDF unreadable/corrupt: {e}"]

    try:
        len(reader.pages)
    except Exception as e:
        return [f"PDF page list unreadable: {e}"]

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


def _pdf_body_text_sample(path: Path, *, max_pages: int = 40) -> str:
    """Extract text from a representative slab of body pages (skips the
    cover/title/copyright/TOC front matter, which is short and can be
    unrepresentative — e.g. the RU copyright page also names the CC license
    in English)."""
    reader = PdfReader(str(path))
    start = min(20, max(0, len(reader.pages) - 1))
    end = min(len(reader.pages), start + max_pages)
    return "\n".join((reader.pages[i].extract_text() or "") for i in range(start, end))


def validate_language(path: Path, check: str) -> list[str]:
    if not path.exists():
        return []  # already reported missing by validate_pdf
    errors: list[str] = []
    try:
        sample = _pdf_body_text_sample(path)
    except Exception as e:
        return [f"could not extract text for language check: {e}"]

    if not sample.strip():
        return ["PDF body text extraction returned nothing to language-check"]

    if check == "cyrillic_present":
        if not CYRILLIC_RE.search(sample):
            errors.append("expected RU (Cyrillic) body text, found none in sample pages")
    elif check == "polish_present":
        cyrillic_chars = len(CYRILLIC_RE.findall(sample))
        # Code listings/CLI output can legitimately contain a handful of
        # Cyrillic characters (e.g. this very book's own historical Russian
        # examples used as universal-Unicode demonstrations); the real
        # regression this check must catch is *substantial* untranslated
        # Russian prose, not stray characters.
        if cyrillic_chars > 40:
            errors.append(
                f"PL PDF body text contains {cyrillic_chars} Cyrillic characters in "
                "sample pages — not genuinely Polish"
            )
        lowered = sample.lower()
        marker_hits = sum(1 for word in POLISH_MARKERS if word in lowered)
        if marker_hits < 3:
            errors.append(
                f"PL PDF body text matched only {marker_hits}/{len(POLISH_MARKERS)} "
                "common Polish markers — does not read as genuinely Polish"
            )
    else:
        raise ValueError(f"unknown language check: {check}")
    return errors


def main() -> None:
    all_errors: list[str] = []

    for locale, spec in LOCALES.items():
        pdf_path: Path = spec["pdf_path"]
        epub_path: Path = spec["epub_path"]

        print(f"== [{locale}] PDF: {pdf_path.relative_to(ROOT)} ==")
        pdf_errors = validate_pdf(pdf_path)
        if pdf_errors:
            for e in pdf_errors:
                print(f"  СБОЙ: {e}")
            all_errors.extend(f"[{locale}/pdf] {e}" for e in pdf_errors)
        else:
            reader = PdfReader(str(pdf_path))
            print(f"  OK — {len(reader.pages)} pages, metadata present, {len(reader.outline)} bookmarks, uniform page size")

        lang_errors = validate_language(pdf_path, spec["language_check"])
        if lang_errors:
            for e in lang_errors:
                print(f"  СБОЙ: {e}")
            all_errors.extend(f"[{locale}/pdf-language] {e}" for e in lang_errors)
        elif not pdf_errors:
            print(f"  OK — language check passed ({spec['language_check']})")

        print(f"\n== [{locale}] EPUB: {epub_path.relative_to(ROOT)} ==")
        epub_errors = validate_epub(epub_path)
        if epub_errors:
            for e in epub_errors:
                print(f"  СБОЙ: {e}")
            all_errors.extend(f"[{locale}/epub] {e}" for e in epub_errors)
        else:
            print("  OK — epubcheck: 0 errors")
        print()

    if all_errors:
        print(f"ВАЛИДАЦИЯ ПУБЛИКАЦИИ: FAIL ({len(all_errors)} problem(s))", file=sys.stderr)
        sys.exit(1)

    print("ВАЛИДАЦИЯ ПУБЛИКАЦИИ: PASS")


if __name__ == "__main__":
    main()
