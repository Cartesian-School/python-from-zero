#!/usr/bin/env python3
"""Validate generated pagination against the final physical PDF page tree."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_metadata import chapters

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "book" / "pdf" / "готовая книга.pdf"
PAGINATION_PATH = ROOT / "data" / "book-pagination.json"
HOMEPAGE_PATH = ROOT / "site" / "index.html"


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value).replace("‑", "-")


def flatten_outline(reader: Any):
    for item in reader.outline or []:
        if isinstance(item, list):
            yield from flatten_outline_items(reader, item)
        else:
            yield item


def flatten_outline_items(reader: Any, items):
    for item in items:
        if isinstance(item, list):
            yield from flatten_outline_items(reader, item)
        else:
            yield item


def validate(*, portable: bool = False) -> list[str]:
    errors: list[str] = []
    metadata = json.loads(PAGINATION_PATH.read_text(encoding="utf-8"))
    if metadata.get("schema_version") != "1.0.0":
        errors.append("unsupported pagination schema")
    if metadata.get("source_date_epoch") != 0:
        errors.append("canonical SOURCE_DATE_EPOCH render contract drift")

    expected_keys = {f"{number:02d}" for number in range(1, 25)}
    chapter_data = metadata.get("chapters", {})
    if set(chapter_data) != expected_keys:
        errors.append("generated pagination must contain exactly chapters 01..24")
        return errors

    canonical = chapters()
    starts = [int(chapter_data[f"{item.number:02d}"]["start_page"]) for item in canonical]
    if starts != sorted(set(starts)):
        errors.append(f"chapter start pages are not strictly increasing: {starts}")

    total_pages = int(metadata["total_pages"])
    for index, item in enumerate(canonical):
        entry = chapter_data[f"{item.number:02d}"]
        if entry.get("title") != item.title or entry.get("url") != item.url:
            errors.append(f"chapter {item.number}: static/generated metadata drift")
        expected_end = starts[index + 1] - 1 if index < 23 else int(entry["end_page"])
        if int(entry["end_page"]) != expected_end:
            errors.append(f"chapter {item.number}: non-contiguous generated page range")
        if int(entry["end_page"]) < int(entry["start_page"]):
            errors.append(f"chapter {item.number}: invalid generated page range")
    if int(chapter_data["24"]["end_page"]) >= total_pages:
        errors.append("chapter 24 must end before generated back matter")

    if not PDF_PATH.is_file():
        return errors + ["canonical PDF is missing"]
    actual_pdf_sha256 = hashlib.sha256(PDF_PATH.read_bytes()).hexdigest()
    if metadata.get("pdf_sha256") != actual_pdf_sha256:
        errors.append("pagination sidecar belongs to a different PDF SHA-256")

    reader = None
    compact_toc = ""
    outlines: dict[str, set[int]] = {}
    if not portable:
        # The deep PDF semantic audit belongs to the publication CI image,
        # which installs the renderer/parser toolchain. Vercel's portable
        # deployment gate still binds the committed PDF bytes to the sidecar,
        # homepage, and all opener labels without mutable build-time installs.
        import build_pdf
        from pypdf import PdfReader

        if metadata.get("source_date_epoch") != int(build_pdf.SOURCE_DATE_EPOCH):
            errors.append("build renderer SOURCE_DATE_EPOCH contract drift")
        reader = PdfReader(str(PDF_PATH))
        if len(reader.pages) != total_pages:
            errors.append(
                f"physical PDF has {len(reader.pages)} pages, metadata has {total_pages}"
            )

        toc_text = "\n".join(
            (reader.pages[index].extract_text() or "") for index in range(3, 7)
        )
        compact_toc = compact(toc_text)
        for destination in flatten_outline(reader):
            title = getattr(destination, "title", "")
            outlines.setdefault(title, set()).add(
                reader.get_destination_page_number(destination) + 1
            )

    for item in canonical:
        entry = chapter_data[f"{item.number:02d}"]
        physical_page = int(entry["start_page"])
        expected_label = f"ГЛАВА {item.number} · СТР. {physical_page}"
        if reader is not None:
            if physical_page > len(reader.pages):
                errors.append(f"chapter {item.number}: start page is outside the PDF")
                continue
            page_text = reader.pages[physical_page - 1].extract_text() or ""
            if compact(expected_label) not in compact(page_text):
                errors.append(
                    f"chapter {item.number}: physical opener page lacks {expected_label!r}"
                )
            if compact(item.title) not in compact(page_text):
                errors.append(f"chapter {item.number}: physical opener title drift")
            toc_token = compact(f"Глава {item.number}. {item.title} {physical_page}")
            if toc_token not in compact_toc:
                errors.append(f"chapter {item.number}: PDF TOC page/title drift")
            if physical_page not in outlines.get(item.title, set()):
                errors.append(f"chapter {item.number}: PDF bookmark destination drift")

        opener_html = (ROOT / "site" / item.url.lstrip("/")).read_text(
            encoding="utf-8"
        )
        if f"ГЛАВА {item.number} · СТР. {physical_page}" not in opener_html:
            errors.append(f"chapter {item.number}: website opener pagination drift")

    homepage = HOMEPAGE_PATH.read_text(encoding="utf-8")
    if not re.search(
        rf'<div class="num">{total_pages}</div><div class="lbl">Страниц в книге</div>',
        homepage,
    ):
        errors.append("homepage exact total-page statistic drift")

    if not portable:
        font_records = build_pdf.validate_font_files()
        full_html, _chapter_markers, _page_markers, _project_marker = (
            build_pdf.build_full_html()
        )
        current_fingerprint = build_pdf.source_fingerprint(full_html, font_records)
        if metadata.get("generated_from") != f"sha256:{current_fingerprint}":
            errors.append("pagination metadata fingerprint is stale for current book inputs")

    forbidden_fields = re.compile(
        r"baseline_page|canonical_page|actual_pdf_page|min_required_pdf_pages"
    )
    active_paths = [
        ROOT / "scripts" / f"build_chapter_{number:02d}.py"
        for number in range(1, 25)
    ] + [
        ROOT / "scripts" / "build_manifest.py",
        ROOT / "manifest" / "coverage_manifest.json",
        ROOT / "python_book_table_of_contents_ru.md",
    ]
    for path in active_paths:
        source = path.read_text(encoding="utf-8")
        if forbidden_fields.search(source):
            errors.append(f"stale manual pagination field remains in {path.relative_to(ROOT)}")
        if path.name.startswith("build_chapter_") and re.search(
            r"render_chapter_opener\([^)]*(?:title|baseline_page)\s*=", source, re.DOTALL
        ):
            errors.append(f"manual opener title/page remains in {path.relative_to(ROOT)}")

    return errors


def main() -> None:
    args = sys.argv[1:]
    if args not in ([], ["--portable"]):
        print("usage: validate_pagination.py [--portable]", file=sys.stderr)
        raise SystemExit(2)
    errors = validate(portable=bool(args))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    metadata = json.loads(PAGINATION_PATH.read_text(encoding="utf-8"))
    print(
        "Canonical pagination: PASS "
        f"(24 chapters, {metadata['total_pages']} physical pages, PDF/TOC/site consistent)"
    )


if __name__ == "__main__":
    main()
