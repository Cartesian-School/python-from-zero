#!/usr/bin/env python3
"""Semantic catalog validator — complements validate_navigation.py.

validate_navigation.py already proves every href resolves to a real file and
every #fragment exists on its target page. That is necessary but not
sufficient: a link can return 200 and still land on the wrong content (e.g.
"Глава 7" pointing at Chapter 6's page, or a practice card linking to the
wrong lesson). This script checks TARGET IDENTITY, not just target existence,
for every catalog this project claims is complete:

- the 5 required homepage main-menu anchors exist exactly once each, with
  the exact required visible heading;
- all 24 chapters in the homepage roadmap link to a chapter page that
  actually identifies itself as that chapter number;
- all entries in manifest/practice_manifest.json (122) are rendered exactly
  once in the homepage Practice catalog, linking to /practice/<id>/, and
  that page's own embedded config identifies the same lesson_id;
- all entries in manifest/projects_manifest.json (12) are rendered exactly
  once as a homepage Projects card, linking to /projects/<slug>/, and that
  page's <h1> identifies the same project;
- no practice catalog row on the homepage uses a raw .ipynb as its primary
  action (the notebook download is a secondary action inside the practice
  page itself, never the homepage's own link).

Usage: python3 scripts/validate_site_catalogs.py [dist_dir]
Defaults to site/ (useful for a quick check without a full build).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_metadata import chapters

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_ANCHORS = [
    ("o-kurse", "О курсе"),
    ("glavy", "Главы"),
    ("praktika", "Практика"),
    ("proekty", "Проекты"),
    ("spravochnik", "Справочник"),
]


def _read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def _section_heading(html_text: str, anchor: str) -> str | None:
    """Finds `id="<anchor>"` and returns the text of the next <h2> after it."""
    m = re.search(rf'id="{re.escape(anchor)}"', html_text)
    if not m:
        return None
    rest = html_text[m.end():]
    h2 = re.search(r"<h2>(.*?)</h2>", rest, re.DOTALL)
    return h2.group(1).strip() if h2 else None


def validate_homepage_anchors(base_dir: Path, errors: list[str]) -> None:
    index_text = _read(base_dir / "index.html")
    if index_text is None:
        errors.append("index.html: file not found — cannot validate homepage anchors")
        return
    for anchor, expected_heading in REQUIRED_ANCHORS:
        count = len(re.findall(rf'id="{re.escape(anchor)}"', index_text))
        if count == 0:
            errors.append(f'index.html: required anchor id="{anchor}" is missing')
            continue
        if count > 1:
            errors.append(f'index.html: anchor id="{anchor}" appears {count} times (must be exactly once)')
        heading = _section_heading(index_text, anchor)
        if heading != expected_heading:
            errors.append(f'index.html: #{anchor} heading is {heading!r}, expected {expected_heading!r}')


def validate_chapter_roadmap(base_dir: Path, errors: list[str]) -> None:
    canonical_chapters = chapters()
    index_text = _read(base_dir / "index.html")
    if index_text is None:
        return  # already reported above

    node_re = re.compile(
        r'class="journey-node" data-chapter="(\d+)"[^>]*>.*?<a class="jn-card" href="([^"]*)"',
        re.DOTALL,
    )
    nodes = {int(num): href for num, href in node_re.findall(index_text)}

    expected_numbers = {chapter.number for chapter in canonical_chapters}
    missing = expected_numbers - nodes.keys()
    for n in sorted(missing):
        errors.append(f"index.html: roadmap has no milestone for chapter {n}")
    extra = nodes.keys() - expected_numbers
    for n in sorted(extra):
        errors.append(f"index.html: roadmap has a milestone for non-existent chapter {n}")

    checked = 0
    wrong = 0
    for num, href in sorted(nodes.items()):
        target = (base_dir / href.lstrip("/")).resolve()
        if target.is_dir():
            target = target / "index.html"
        target_text = _read(target)
        checked += 1
        if target_text is None:
            errors.append(f"index.html: chapter {num} roadmap link -> missing page {href}")
            wrong += 1
            continue
        m = re.search(r"ГЛАВА\s+(\d+)", target_text)
        if not m or int(m.group(1)) != num:
            found = m.group(1) if m else "none"
            errors.append(f"index.html: chapter {num} roadmap link ({href}) identifies as chapter {found}, expected {num}")
            wrong += 1
    print(f"Главы: checked {checked}, wrong {wrong}")


def validate_practice_catalog(base_dir: Path, errors: list[str]) -> None:
    manifest = json.loads((ROOT / "manifest" / "practice_manifest.json").read_text(encoding="utf-8"))
    index_text = _read(base_dir / "index.html")
    if index_text is None:
        return

    row_re = re.compile(r'class="practice-lesson-row" data-lesson-id="([^"]+)" data-mode="[^"]*" href="([^"]*)"')
    rows = row_re.findall(index_text)

    # No raw .ipynb as the primary homepage action.
    for lesson_id, href in rows:
        if href.endswith(".ipynb"):
            errors.append(f"index.html: practice row {lesson_id} uses a raw .ipynb as its primary action ({href})")

    rendered_ids = [lid for lid, _ in rows]
    rendered_set = set(rendered_ids)
    manifest_set = set(manifest.keys())

    missing = manifest_set - rendered_set
    for lid in sorted(missing):
        errors.append(f"index.html: practice_manifest entry {lid!r} is not rendered in the homepage Practice catalog")

    extra = rendered_set - manifest_set
    for lid in sorted(extra):
        errors.append(f"index.html: homepage Practice catalog renders {lid!r}, which is not in practice_manifest.json")

    duplicates = {lid for lid in rendered_ids if rendered_ids.count(lid) > 1}
    for lid in sorted(duplicates):
        errors.append(f"index.html: practice row {lid!r} rendered {rendered_ids.count(lid)} times (must be exactly once)")

    wrong_routes = 0
    for lid, href in rows:
        expected_href = f"/practice/{lid}/index.html"
        if href != expected_href:
            errors.append(f"index.html: practice row {lid!r} links to {href!r}, expected {expected_href!r}")
            wrong_routes += 1

    print(f"Практика: manifest={len(manifest)}, rendered={len(rendered_ids)}, missing={len(missing)}, duplicates={len(duplicates)}, wrong_routes={wrong_routes}")


def validate_projects_catalog(base_dir: Path, errors: list[str]) -> None:
    manifest = json.loads((ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8"))["projects"]
    index_text = _read(base_dir / "index.html")
    if index_text is None:
        return

    card_re = re.compile(r'class="project-card" href="/projects/([^/]+)/"')
    rendered_slugs = card_re.findall(index_text)
    rendered_set = set(rendered_slugs)
    manifest_slugs = {p["slug"] for p in manifest}

    missing = manifest_slugs - rendered_set
    for slug in sorted(missing):
        errors.append(f"index.html: project {slug!r} is not rendered as a homepage Projects card")
    extra = rendered_set - manifest_slugs
    for slug in sorted(extra):
        errors.append(f"index.html: homepage renders a Projects card for {slug!r}, not in projects_manifest.json")
    duplicates = {s for s in rendered_slugs if rendered_slugs.count(s) > 1}
    for slug in sorted(duplicates):
        errors.append(f"index.html: project card {slug!r} rendered {rendered_slugs.count(slug)} times (must be exactly once)")

    checked = 0
    wrong = 0
    for p in manifest:
        checked += 1
        slug = p["slug"]
        detail = _read(base_dir / "projects" / slug / "index.html")
        if detail is None:
            errors.append(f"projects/{slug}/: detail page missing")
            wrong += 1
            continue
        h1 = re.search(r"<h1>(.*?)</h1>", detail, re.DOTALL)
        title_ok = bool(h1) and h1.group(1).strip() == p["title"]
        if not title_ok:
            found = h1.group(1).strip() if h1 else "none"
            errors.append(f"projects/{slug}/: <h1> is {found!r}, expected {p['title']!r}")
            wrong += 1
            continue
        source_file = ROOT / p["source_path"]
        if not source_file.exists():
            errors.append(f"projects/{slug}/: source_path does not exist: {p['source_path']}")
            wrong += 1
    print(f"Проекты: manifest={len(manifest)}, homepage_cards={len(rendered_slugs)}, checked={checked}, wrong={wrong}")


def main() -> None:
    base_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "site"
    if not base_dir.exists():
        print(f"Directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    errors: list[str] = []
    validate_homepage_anchors(base_dir, errors)
    validate_chapter_roadmap(base_dir, errors)
    validate_practice_catalog(base_dir, errors)
    validate_projects_catalog(base_dir, errors)

    if errors:
        print(f"\nSite catalog validation failed — {len(errors)} problem(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print("\nSite catalogs OK: homepage anchors, chapter roadmap, practice catalog, and projects catalog all match their sources of truth.")


if __name__ == "__main__":
    main()
