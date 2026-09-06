#!/usr/bin/env python3
"""Builds the Polish "Licencja" page (site/pl/front-matter/licencja.html).

Separate from build_license_page.py so editing this file never perturbs
that RU builder's canonical source hash. Mirrors build_license_page.py's
own docstring precedent: a dedicated file keeps unrelated M02/M01 hash
churn out of each other's way.

Canonical PL prose lives in manifest/i18n/content/pl/front-matter-license.json
— this script only renders it. Legal substance (CC BY-NC-SA 4.0 for
educational content, MIT for code) is unchanged; only surrounding
explanatory prose is translated.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import author_profile as ap
from build_license_page import CC_DEED_URL, CC_LEGALCODE_URL, REPO_URL, SAFESORT_REPO_URL
from localization import Routes, load_pl_content
from site_lib import NavItem, PageNav, SidebarGroup, callout, icon_label, render_page

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "pl" / "front-matter"

CONTENT = load_pl_content(
    "front-matter-license",
    required_keys=("page", "callout_brief", "rightsholder", "course_materials",
                    "what_cc_means", "noncommercial", "sharealike", "no_endorsement",
                    "code_section", "rel_license", "third_party", "trademark",
                    "attribution_example", "sidebar"),
)


def write(name: str, html_out: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Zapisano: {path.relative_to(ROOT)}")


def build_licencja() -> None:
    sidebar_copy = CONTENT["sidebar"]
    # Only the translated item is linked — the reference index page isn't
    # translated yet, so no fake PL route is created for it.
    sidebar = [SidebarGroup(sidebar_copy["group_title"], [
        NavItem(sidebar_copy["license_item"], "licencja.html", active=True),
    ])]

    brief = CONTENT["callout_brief"]
    materials = CONTENT["course_materials"]
    cc_means = CONTENT["what_cc_means"]
    code = CONTENT["code_section"]
    attribution = CONTENT["attribution_example"]

    body = f"""
    {callout(
        "info",
        icon_label("license", brief["title"]),
        "".join(f"<p>{p}</p>" for p in brief["body_paragraphs"]),
    )}

    <h2>{CONTENT["rightsholder"]["heading"]}</h2>
    <p>{CONTENT["rightsholder"]["body"].format(name=ap.NAME)}</p>

    <h2>{materials["heading"]}</h2>
    <p>{materials["intro"].format(cc_link=f'<a href="{CC_DEED_URL}">{materials["cc_link_text"]}</a>')}</p>
    <ul>
      {"".join(f"<li>{item}</li>" for item in materials["items"])}
    </ul>
    <p>{materials["code_excluded"]}</p>

    <h2>{cc_means["heading"]}</h2>
    <ul>
      {"".join(f"<li>{item}</li>" for item in cc_means["items"])}
    </ul>
    <p>{cc_means["official_text"].format(
        deed_link=f'<a href="{CC_DEED_URL}">{cc_means["deed_link_text"]}</a>',
        legalcode_link=f'<a href="{CC_LEGALCODE_URL}">{cc_means["legalcode_link_text"]}</a>',
    )}</p>

    <h2>{CONTENT["noncommercial"]["heading"]}</h2>
    <p>{CONTENT["noncommercial"]["body"]}</p>

    <h2>{CONTENT["sharealike"]["heading"]}</h2>
    <p>{CONTENT["sharealike"]["body"]}</p>

    <h2>{CONTENT["no_endorsement"]["heading"]}</h2>
    <p>{CONTENT["no_endorsement"]["body"].format(name=ap.NAME)}</p>

    <h2>{code["heading"]}</h2>
    <p>{code["intro"]}</p>
    <ul>
      <li>{code["items"][0].format(repo_link=f'<a href="{REPO_URL}">github.com/Cartesian-School/python-from-zero</a>')}</li>
      <li>{code["items"][1].format(safesort_link=f'<a href="{SAFESORT_REPO_URL}">github.com/Cartesian-School/safesort</a>')}</li>
    </ul>
    <p>{code["outro"]}</p>

    <h2>{CONTENT["rel_license"]["heading"]}</h2>
    <p>{CONTENT["rel_license"]["body"].format(cc_legalcode_url=CC_LEGALCODE_URL)}</p>

    <h2>{CONTENT["third_party"]["heading"]}</h2>
    <p>{CONTENT["third_party"]["body"]}</p>

    <h2>{CONTENT["trademark"]["heading"]}</h2>
    <p>{CONTENT["trademark"]["body"]}</p>

    {callout(
        "tip",
        attribution["title"],
        "".join(f"<p>{p}</p>" for p in attribution["body_paragraphs"]),
    )}
    """
    body = "\n".join(line.rstrip() for line in body.splitlines())

    page = CONTENT["page"]
    out = render_page(
        active_section="spravochnik",
        page_title=page["title"],
        description=page["description"],
        depth=2,
        breadcrumb=[("Python od zera", "../index.html"), (page["title"], "")],
        kicker=page["kicker"],
        h1=page["h1"],
        lede=page["lede"],
        body_html=body,
        sidebar_groups=sidebar,
        nav=PageNav(),
        page_id="front-matter-license",
        locale="pl",
        routes=Routes(),
    )
    write("licencja.html", out)


if __name__ == "__main__":
    build_licencja()
