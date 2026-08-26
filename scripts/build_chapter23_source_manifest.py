#!/usr/bin/env python3
"""Deterministically regenerate Chapter 23's official-source manifest."""

from __future__ import annotations

import json
import re
from pathlib import Path

from validate_chapter23_sources import (
    MANIFEST_PATH,
    PROVIDER_LICENSE,
    classify_source,
    extract_sources_from_build_script,
)

CHECKED_DATE = "2026-08-26"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "source"


def build_manifest() -> dict:
    actual, calls = extract_sources_from_build_script()
    adapted_by_url: dict[str, bool] = {}
    for call in calls:
        for url in call["urls"]:
            previous = adapted_by_url.setdefault(url, call["adapted"])
            if previous != call["adapted"]:
                raise ValueError(f"source has conflicting adapted flags: {url}")

    sources = []
    used_ids: set[str] = set()
    for url, entry in sorted(actual.items()):
        provider, category = classify_source(url)
        source_id = f"{provider}-{slugify(entry['title'])}"
        if source_id in used_ids:
            source_id = f"{source_id}-{len(used_ids) + 1}"
        used_ids.add(source_id)
        sources.append(
            {
                "id": source_id,
                "title": entry["title"],
                "url": url,
                "provider": provider,
                "category": category,
                "license": PROVIDER_LICENSE[provider],
                "checked_date": CHECKED_DATE,
                "adapted": adapted_by_url[url],
                "routes": sorted(entry["routes"]),
            }
        )

    return {
        "schema_version": "2.0.0",
        "chapter": "23",
        "description": (
            "Official primary sources used by Chapter 23, regenerated from "
            "official_sources(...) calls in scripts/build_chapter_23.py."
        ),
        "sources": sources,
    }


def main() -> None:
    manifest = build_manifest()
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Записано источников: {len(manifest['sources'])} -> {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
