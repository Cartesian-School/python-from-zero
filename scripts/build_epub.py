#!/usr/bin/env python3
"""Thin compatibility wrapper — RU EPUB via the canonical book-build pipeline.

Prefer ``python scripts/build_book.py --language ru --format epub``. This
script exists only so the previous per-locale-per-format entry point keeps
working; it delegates entirely to book_pipeline.build_book and contains no
independent publishing logic (docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md,
section 2).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from book_pipeline import build_book
from book_pipeline.locales import get_locale

# Backward-compatible data re-exports (not logic): tests/test_license_consistency.py
# and other tooling historically read these constants off this module.
_RU_CONFIG = get_locale("ru")
RIGHTS_NOTICE_PLAIN = _RU_CONFIG.rights_notice_plain
CONTENT_LICENSE_URL = _RU_CONFIG.content_license_url


def main() -> None:
    build_book(language="ru", output_format="epub")


if __name__ == "__main__":
    main()
