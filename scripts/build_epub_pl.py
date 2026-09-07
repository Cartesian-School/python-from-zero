#!/usr/bin/env python3
"""Thin compatibility wrapper — PL EPUB via the canonical book-build pipeline.

Prefer ``python scripts/build_book.py --language pl --format epub``. See
build_epub.py's RU counterpart for why this wrapper exists and what it may
(and may not) contain.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from book_pipeline import build_book


def main() -> None:
    build_book(language="pl", output_format="epub")


if __name__ == "__main__":
    main()
