#!/usr/bin/env python3
"""Injects the RU|PL language switcher into site/front-matter/ob-avtore.html
without ever touching scripts/build_front_matter.py.

scripts/build_front_matter.py is a canonical M01-tracked source: it backs
the ob-avtore/o-tehnicheskom-recenzente/vvedenie supplementary units in
manifest/ru_content_audit_inventory.json, and M02-I01/I02's frozen baseline
(manifest/i18n/ru_baseline.json) locks the exact recorded bytes of every
M01 evidence file. Any edit to build_front_matter.py -- even one that adds
zero bytes to the reviewed educational prose -- changes its hash and would
require resyncing three M01 review records, which is explicitly out of
scope here ("M02-I03 should not change RU source... if baseline mismatch
appears, STOP and investigate"). This script instead post-processes the
already-rendered HTML, exactly mirroring how build_seo_meta.py injects an
SEO block into rendered pages without touching their builders.

Idempotent: strips any previous injection before reinjecting, so running
the full pipeline twice in a row (the determinism contract) is a no-op on
the second pass.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from localization import Routes
from site_lib import mobile_nav_links, site_header

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "site" / "front-matter" / "ob-avtore.html"
PAGE_ID = "front-matter-author"
ACTIVE_SECTION = "o-kurse"

START = "<!-- cartesian:pl-switcher:start -->"
END = "<!-- cartesian:pl-switcher:end -->"


def _desktop_switch_html(routes: Routes) -> str:
    rendered = site_header(ACTIVE_SECTION, page_id=PAGE_ID, locale="ru", routes=routes)
    match = re.search(r'<div class="language-switcher-desktop">.*?</div>', rendered, re.S)
    assert match, "site_header() did not render a desktop switcher"
    return match.group(0)


def _mobile_switch_html(routes: Routes) -> str:
    rendered = mobile_nav_links(ACTIVE_SECTION, page_id=PAGE_ID, locale="ru", routes=routes)
    match = re.search(r'<nav class="language-switcher".*?</nav>', rendered, re.S)
    assert match, "mobile_nav_links() did not render a switcher"
    return match.group(0)


def inject() -> None:
    routes = Routes()
    html = TARGET.read_text(encoding="utf-8")
    html = re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)

    # Callable replacements (not backslash-template strings) so literal HTML
    # in the injected block is never misread as a regex backreference.
    desktop_pattern = r'(<ul class="top-nav">.*?</ul>\n)(  <button class="nav-toggle")'
    desktop_block = START + _desktop_switch_html(routes) + END
    html, count = re.subn(
        desktop_pattern,
        lambda m: m.group(1) + desktop_block + m.group(2),
        html, count=1, flags=re.S,
    )
    assert count == 1, "could not find desktop nav insertion point in ob-avtore.html"

    mobile_pattern = r'(<div class="mobile-nav-links">.*?<ul class="toc-list">.*?</ul>)(</div>)'
    mobile_block = START + _mobile_switch_html(routes) + END
    html, count = re.subn(
        mobile_pattern,
        lambda m: m.group(1) + mobile_block + m.group(2),
        html, count=1, flags=re.S,
    )
    assert count == 1, "could not find mobile nav insertion point in ob-avtore.html"

    TARGET.write_text(html, encoding="utf-8")
    print(f"Injected RU|PL switcher into {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    inject()
