"""Canonical, language-independent, format-parameterized book-build pipeline.

Binding architecture contract: docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md

    build_book(language="pl", output_format="pdf")

``language`` is only an input parameter (selects locale content/config, see
:mod:`book_pipeline.locales`); ``output_format`` is only an output parameter
(selects the publication adapter, see :mod:`book_pipeline.pdf_adapter` /
:mod:`book_pipeline.epub_adapter`). Every other stage — source discovery,
canonical book model construction, common semantic rendering (article/opener/
project extraction, link rewriting, SVG repair) — is shared by every language
and every format; see :mod:`book_pipeline.model`.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Every scripts/*.py entry point in this repository runs with `scripts/` on
# sys.path (each inserts it itself before importing bare module names like
# `book_shared` or `chapter_metadata`). book_pipeline's submodules reuse that
# same convention, so this package must guarantee `scripts/` is importable
# even when a caller imports `book_pipeline` directly without having done
# that dance first (e.g. a test importing `import book_pipeline`).
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from .locales import SUPPORTED_LANGUAGES, get_locale
from .pipeline import SUPPORTED_FORMATS, build_book

__all__ = ["SUPPORTED_FORMATS", "SUPPORTED_LANGUAGES", "build_book", "get_locale"]
