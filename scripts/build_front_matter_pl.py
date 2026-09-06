#!/usr/bin/env python3
"""Builds the Polish "O autorze" front-matter page (site/pl/front-matter/o-autorze.html).

Separate from build_front_matter.py so editing this file never perturbs
that RU builder's canonical source hash (manifest/i18n/routes.json binds
front-matter-author's source to build_front_matter.py, unchanged here).

Canonical PL prose lives in manifest/i18n/content/pl/front-matter-author.json
and content/pl/author.json (Polish counterpart of author_profile.Domain's
title_ru/desc_ru fields) — this script only renders it.
"""

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import author_profile as ap
from localization import UI_STRINGS, Routes, load_pl_content
from site_lib import NavItem, PageNav, SidebarGroup, render_page

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "pl" / "front-matter"

CONTENT = load_pl_content(
    "front-matter-author",
    required_keys=("page", "core_paragraphs", "professional_path", "domains_heading",
                    "domains", "portrait_alt", "projects_section", "educator_section",
                    "cartesian_school_section", "sidebar"),
)
DOMAINS_PL = CONTENT["domains"]


def write(name: str, html_out: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Zapisano: {path.relative_to(ROOT)}")


def build_o_autorze() -> None:
    page = CONTENT["page"]
    sidebar_copy = CONTENT["sidebar"]

    # Only the translated item is linked — no fake PL route for the
    # (not yet translated) technical-reviewer/introduction pages.
    sidebar = [SidebarGroup(sidebar_copy["group_title"], [
        NavItem(sidebar_copy["author_item"], "o-autorze.html", active=True),
    ])]

    hero = f"""
    <div class="author-page__hero web-presentation">
      <div class="author-page__portrait">
        <picture>
          <source srcset="{ap.PORTRAIT_WEBP}" type="image/webp">
          <img src="{ap.PORTRAIT_JPG}" width="{ap.PORTRAIT_WIDTH}" height="{ap.PORTRAIT_HEIGHT}"
               alt="{html.escape(CONTENT["portrait_alt"])}" loading="lazy" decoding="async">
        </picture>
      </div>
      <div class="author-page__hero-copy">
        <h2 class="author-page__name">{ap.NAME}</h2>
        <p class="author-page__role">{html.escape(ap.ROLE)}</p>
        <p class="author-page__specialization">{"".join(f"<span>{html.escape(s)}</span>" for s in ap.SPECIALIZATIONS)}</p>
      </div>
    </div>
    """

    core = "".join(f"<p>{p}</p>" for p in CONTENT["core_paragraphs"])

    domains_html = "".join(f'''<li class="author-page__domain{" author-page__domain--wide" if d.wide else ""}">
        <span class="author-page__domain-index">{d.index}</span><div><h3>{html.escape(DOMAINS_PL[d.index]["title"])}</h3><p>{html.escape(DOMAINS_PL[d.index]["desc"])}</p></div>
      </li>''' for d in ap.DOMAINS)

    projects_html = "".join(f"<li>{html.escape(p)}</li>" for p in ap.PROJECTS)

    prof = CONTENT["professional_path"]
    proj_section = CONTENT["projects_section"]
    educator = CONTENT["educator_section"]
    cs_section = CONTENT["cartesian_school_section"]

    rest = f"""
    <section class="author-page__section web-presentation">
      <h2>{html.escape(prof["heading"])}</h2>
      {"".join(f"<p>{p}</p>" for p in prof["paragraphs"])}
    </section>

    <section class="author-page__section web-presentation">
      <h2>{html.escape(CONTENT["domains_heading"])}</h2>
      <ul class="author-page__domains" aria-label="{html.escape(CONTENT["domains_heading"])}">
      {domains_html}
      </ul>
    </section>

    <section class="author-page__section web-presentation">
      <h2>{html.escape(proj_section["heading"])}</h2>
      <p>{html.escape(proj_section["lead"])}</p>
      <ul class="author-page__projects" aria-label="{html.escape(proj_section["heading"])}">{projects_html}</ul>
    </section>

    <section class="author-page__section web-presentation">
      <h2>{html.escape(educator["heading"])}</h2>
      <p>{html.escape(educator["paragraph"])}</p>
    </section>

    <section class="author-page__section web-presentation">
      <h2>{html.escape(cs_section["heading"])}</h2>
      <p>{html.escape(cs_section["paragraph"])}</p>
    </section>
    """

    body = "\n".join(line.rstrip() for line in (hero + core + rest).splitlines())

    out = render_page(
        active_section="o-kurse",
        page_title=page["title"],
        description=page["description"],
        depth=2,
        breadcrumb=[(UI_STRINGS["pl"]["course_title"], "../index.html"), (page["title"], "")],
        kicker=page["kicker"],
        h1=page["h1"],
        lede=page["lede"],
        body_html=body,
        sidebar_groups=sidebar,
        nav=PageNav(),
        page_id="front-matter-author",
        locale="pl",
        routes=Routes(),
    )
    write("o-autorze.html", out)


if __name__ == "__main__":
    build_o_autorze()
