#!/usr/bin/env python3
"""Injects canonical link, Open Graph, Twitter card, and JSON-LD structured
data into every generated site/**/*.html page, using site_structure.py as
the single source of truth for each page's canonical URL/title/description.

Does NOT touch each page's existing <title>/<meta name="description"> —
those stay exactly as the page generators wrote them (Russian, matching the
page's own lang="ru" content — see the "future multilingual architecture"
note in build_seo_meta.py's design: og:locale/JSON-LD inLanguage are derived
from each page's own <html lang="..."> rather than hardcoded, so adding a
genuinely-translated page later only requires it to declare its own lang;
nothing here assumes "ru" globally).

Idempotent: re-running replaces the previously-injected block (marked by
CARTESIAN_SEO_MARKER_START/END) rather than duplicating it, so it's safe to
run after every rebuild.

Practice pages (thin application shells wrapping notebook content that's
already represented on their parent theory page) are marked noindex,follow —
sound SEO judgment: the shell has near-duplicate content, but internal link
equity to the theory page should still be followed.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import author_profile as ap
from site_structure import SITE_ORIGIN, PageRecord, iter_pages

AUTHOR_PAGE_URL_PATH = "/front-matter/ob-avtore.html"

MARKER_START = "<!-- cartesian:seo-meta:start -->"
MARKER_END = "<!-- cartesian:seo-meta:end -->"

LOGO_URL = f"{SITE_ORIGIN}/assets/img/logo.png"
SITE_NAME = "Cartesian School"

_OG_LOCALE = {"ru": "ru_RU", "en": "en_US", "pl": "pl_PL", "zh-Hans": "zh_CN"}


def _json_ld_script(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Guard against "</script>" breaking out of the script element if it
    # were ever present inside a string value.
    payload = payload.replace("<", "\\u003c")
    return f'<script type="application/ld+json">{payload}</script>'


def _json_ld_for(page: PageRecord, all_pages: list[PageRecord]) -> str | None:
    website_node = {
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_ORIGIN + "/index.html",
        "inLanguage": page.lang,
    }

    if page.kind == "home":
        return _json_ld_script(
            {
                "@context": "https://schema.org",
                "@graph": [
                    website_node,
                    {
                        "@type": "EducationalOrganization",
                        "name": SITE_NAME,
                        "url": SITE_ORIGIN + "/index.html",
                        "logo": LOGO_URL,
                        "description": page.description or "",
                    },
                ],
            }
        )

    if page.kind in ("chapter-opener", "chapter-lesson", "front-matter", "reference"):
        learning_resource_node = {
            "@type": "LearningResource",
            "name": page.title or "",
            "description": page.description or "",
            "url": page.canonical_url,
            "inLanguage": page.lang,
            "isPartOf": website_node,
            "learningResourceType": "lesson" if page.kind == "chapter-lesson" else "chapter",
            "isAccessibleForFree": True,
        }
        if page.url_path == AUTHOR_PAGE_URL_PATH:
            # The one page whose subject is a person, not a lesson — add a
            # Person node alongside the generic LearningResource one, using
            # only facts already verified in author_profile.py.
            person_node = {
                "@type": "Person",
                "name": ap.NAME,
                "jobTitle": ap.ROLE,
                "image": SITE_ORIGIN + ap.PORTRAIT_JPG,
                "url": page.canonical_url,
                "worksFor": [
                    {"@type": "Organization", "name": a.name, **({"url": a.url} if a.url else {})}
                    for a in ap.AFFILIATIONS
                ],
            }
            return _json_ld_script({"@context": "https://schema.org", "@graph": [website_node, learning_resource_node, person_node]})
        return _json_ld_script({"@context": "https://schema.org", **learning_resource_node})

    return None  # practice/other: no structured data — see module docstring


def _seo_block(page: PageRecord, all_pages: list[PageRecord]) -> str:
    title = page.title or SITE_NAME
    description = page.description or ""
    locale = _OG_LOCALE.get(page.lang, page.lang)
    og_type = "website" if page.kind in ("home", "chapter-opener", "reference", "practice") else "article"

    parts = [MARKER_START]
    parts.append(f'<link rel="canonical" href="{html.escape(page.canonical_url)}" />')
    if page.kind == "practice":
        parts.append('<meta name="robots" content="noindex, follow" />')
    parts.append(f'<meta property="og:type" content="{og_type}" />')
    parts.append(f'<meta property="og:site_name" content="{html.escape(SITE_NAME)}" />')
    parts.append(f'<meta property="og:title" content="{html.escape(title)}" />')
    parts.append(f'<meta property="og:description" content="{html.escape(description)}" />')
    parts.append(f'<meta property="og:url" content="{html.escape(page.canonical_url)}" />')
    parts.append(f'<meta property="og:image" content="{html.escape(LOGO_URL)}" />')
    parts.append(f'<meta property="og:locale" content="{html.escape(locale)}" />')
    parts.append('<meta name="twitter:card" content="summary_large_image" />')
    parts.append(f'<meta name="twitter:title" content="{html.escape(title)}" />')
    parts.append(f'<meta name="twitter:description" content="{html.escape(description)}" />')
    parts.append(f'<meta name="twitter:image" content="{html.escape(LOGO_URL)}" />')
    json_ld = _json_ld_for(page, all_pages)
    if json_ld:
        parts.append(json_ld)
    parts.append(MARKER_END)
    return "\n".join(parts)


def inject(page: PageRecord, all_pages: list[PageRecord]) -> bool:
    text = page.path.read_text(encoding="utf-8")
    block = _seo_block(page, all_pages)

    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start != -1 and end != -1:
        new_text = text[:start] + block + text[end + len(MARKER_END):]
    else:
        if "</head>" not in text:
            return False
        new_text = text.replace("</head>", block + "\n</head>", 1)

    if new_text != text:
        page.path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    pages = iter_pages()
    changed = 0
    for page in pages:
        if inject(page, pages):
            changed += 1
    print(f"SEO-мета: обработано {len(pages)} страниц, изменено {changed}.")


if __name__ == "__main__":
    main()
