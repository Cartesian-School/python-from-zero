"""Locale registry: the one place language names resolve to a locale config.

Adding a future locale (e.g. EN) means adding one module (book_pipeline.
locale_en) that builds a BookLocaleConfig, and one entry here — never a new
build path.
"""

from __future__ import annotations

from . import locale_pl, locale_ru
from .config import BookLocaleConfig

_REGISTRY: dict[str, BookLocaleConfig] = {
    "ru": locale_ru.CONFIG,
    "pl": locale_pl.CONFIG,
}

SUPPORTED_LANGUAGES: tuple[str, ...] = tuple(_REGISTRY)


def get_locale(language: str) -> BookLocaleConfig:
    try:
        return _REGISTRY[language]
    except KeyError:
        raise ValueError(
            f"unsupported language: {language!r}; supported: {sorted(_REGISTRY)}"
        ) from None
