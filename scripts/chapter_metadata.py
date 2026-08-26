#!/usr/bin/env python3
"""Canonical static metadata for all learner-facing chapters."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_PATH = ROOT / "data" / "chapters.json"


@dataclass(frozen=True, slots=True)
class Chapter:
    number: int
    title: str
    url: str


@lru_cache(maxsize=1)
def chapters() -> tuple[Chapter, ...]:
    document = json.loads(CHAPTERS_PATH.read_text(encoding="utf-8"))
    records = document.get("chapters")
    if document.get("schema_version") != "1.0.0" or not isinstance(records, list):
        raise ValueError(f"invalid canonical chapter metadata: {CHAPTERS_PATH}")
    result = tuple(Chapter(**record) for record in records)
    expected_numbers = tuple(range(1, 25))
    actual_numbers = tuple(chapter.number for chapter in result)
    if actual_numbers != expected_numbers:
        raise ValueError(f"chapter numbers must be exactly 1..24, got {actual_numbers}")
    if len({chapter.title for chapter in result}) != 24:
        raise ValueError("canonical chapter titles must be unique")
    if len({chapter.url for chapter in result}) != 24:
        raise ValueError("canonical chapter URLs must be unique")
    for chapter in result:
        expected_url = f"/chapters/glava-{chapter.number:02d}/index.html"
        if chapter.url != expected_url:
            raise ValueError(
                f"chapter {chapter.number} URL is {chapter.url!r}, expected {expected_url!r}"
            )
        if not chapter.title.strip():
            raise ValueError(f"chapter {chapter.number} has an empty canonical title")
    return result


def chapter(number: int) -> Chapter:
    if not 1 <= number <= 24:
        raise KeyError(number)
    return chapters()[number - 1]


def chapter_title(number: int) -> str:
    return chapter(number).title


def chapter_url(number: int) -> str:
    return chapter(number).url
