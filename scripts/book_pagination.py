#!/usr/bin/env python3
"""Access the generated physical pagination of the canonical PDF book."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGINATION_PATH = ROOT / "data" / "book-pagination.json"


@lru_cache(maxsize=1)
def pagination() -> dict:
    if not PAGINATION_PATH.exists():
        raise FileNotFoundError(
            f"generated pagination is missing: {PAGINATION_PATH}; run scripts/build_pdf.py"
        )
    document = json.loads(PAGINATION_PATH.read_text(encoding="utf-8"))
    if document.get("schema_version") != "1.0.0":
        raise ValueError(f"unsupported pagination schema in {PAGINATION_PATH}")
    chapters = document.get("chapters")
    if not isinstance(chapters, dict) or set(chapters) != {f"{n:02d}" for n in range(1, 25)}:
        raise ValueError("generated pagination must contain exactly chapters 01..24")
    return document


def total_pages() -> int:
    return int(pagination()["total_pages"])


def chapter_start(number: int) -> int:
    return int(pagination()["chapters"][f"{number:02d}"]["start_page"])


def page_for_url(url: str) -> int | None:
    """Return a physical page for a top-level site page, not an in-page anchor."""
    if "#" in url:
        return None
    value = pagination().get("pages", {}).get(url)
    return int(value) if value is not None else None
