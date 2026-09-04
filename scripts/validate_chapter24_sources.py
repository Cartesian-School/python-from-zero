#!/usr/bin/env python3
"""Validate the offline authoritative-source contract for Chapter 24."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_chapter_24 import PAGES

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "chapter-24-official-sources.json"
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-24"
DOCUMENTED_AUDIT_DATE = "2026-09-03"

EXPECTED_COUNTS = {
    "Python": 9,
    "Software Engineering": 7,
    "Backend": 5,
    "Data / AI": 5,
    "DevOps": 4,
    "Other": 6,
}

ALLOWED_HOSTS = {
    "docs.python.org",
    "packaging.python.org",
    "docs.pytest.org",
    "docs.astral.sh",
    "mypy.readthedocs.io",
    "git-scm.com",
    "docs.github.com",
    "flask.palletsprojects.com",
    "fastapi.tiangolo.com",
    "docs.djangoproject.com",
    "www.postgresql.org",
    "www.rfc-editor.org",
    "numpy.org",
    "pandas.pydata.org",
    "scikit-learn.org",
    "docs.pytorch.org",
    "matplotlib.org",
    "docs.docker.com",
    "www.gnu.org",
    "diataxis.fr",
    "doc.qt.io",
    "www.pygame.org",
    "semver.org",
    "docs.unity3d.com",
    "dev.epicgames.com",
}


def main() -> None:
    errors: list[str] = []
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = document.get("sources", [])

    if document.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if document.get("verified_on") != DOCUMENTED_AUDIT_DATE:
        errors.append(
            f"verified_on must record the documented audit date {DOCUMENTED_AUDIT_DATE}"
        )
    if len(sources) != sum(EXPECTED_COUNTS.values()):
        errors.append(f"expected {sum(EXPECTED_COUNTS.values())} sources, got {len(sources)}")

    ids = [entry.get("id") for entry in sources]
    urls = [entry.get("url") for entry in sources]
    if len(set(ids)) != len(ids):
        errors.append("source ids are not unique")
    if len(set(urls)) != len(urls):
        errors.append("source URLs are not unique")
    actual_counts = Counter(entry.get("category") for entry in sources)
    if actual_counts != Counter(EXPECTED_COUNTS):
        errors.append(f"category counts differ: expected {EXPECTED_COUNTS}, got {dict(actual_counts)}")

    for entry in sources:
        for field in ("id", "category", "title", "url"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"source has invalid {field}: {entry!r}")
        parsed = urlparse(entry.get("url", ""))
        if parsed.scheme != "https":
            errors.append(f"source is not HTTPS: {entry.get('url')}")
        if parsed.netloc not in ALLOWED_HOSTS:
            errors.append(f"source host is outside the authoritative allowlist: {parsed.netloc}")

    combined = "\n".join(
        (CHAPTER_DIR / filename).read_text(encoding="utf-8")
        for filename, _title in PAGES
        if (CHAPTER_DIR / filename).exists()
    )
    for entry in sources:
        if entry["url"] not in combined:
            errors.append(f"manifest source is not cited by Chapter 24: {entry['id']}")
    if "CC BY 4.0" in combined:
        errors.append("Chapter 24 link-only references must not claim adapted GitHub text")

    if errors:
        print(f"Chapter 24 source validation failed: {len(errors)} problem(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "Chapter 24 sources OK: "
        f"{len(sources)} authoritative references; categories={dict(actual_counts)}"
    )


if __name__ == "__main__":
    main()
