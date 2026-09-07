"""The one canonical build entry point.

    build_book(language="pl", output_format="pdf")

Every language and every format goes through the exact same four calls
below: resolve locale config -> load the canonical book model -> hand it to
the requested format adapter. Nothing else may vary this sequence.
"""

from __future__ import annotations

from . import epub_adapter, pdf_adapter
from .locales import get_locale
from .model import CanonicalBookLoader

SUPPORTED_FORMATS: tuple[str, ...] = ("pdf", "epub")

_ADAPTERS = {
    "pdf": pdf_adapter.build,
    "epub": epub_adapter.build,
}


def build_book(*, language: str, output_format: str) -> None:
    config = get_locale(language)  # raises ValueError for an unsupported language
    try:
        adapter = _ADAPTERS[output_format]
    except KeyError:
        raise ValueError(
            f"unsupported output format: {output_format!r}; supported: {sorted(_ADAPTERS)}"
        ) from None
    model = CanonicalBookLoader.load(config)
    adapter(model, config)
