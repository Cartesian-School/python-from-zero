#!/usr/bin/env python3
"""Build a non-public bilingual fixture from canonical fixture source strings."""
from __future__ import annotations
import argparse
import html
from pathlib import Path
from localization import ROOT, LOCALES, UI_STRINGS, Routes, sha256
from site_lib import site_header, mobile_nav_links, NAV_KEYS
from build_seo_meta import _seo_block
from site_structure import PageRecord




def build(output: Path) -> Routes:
    output = output.resolve()
    if output == ROOT or output.is_relative_to(ROOT / 'site') or output.is_relative_to(ROOT / 'dist'):
        raise ValueError('Fixture must not enter production output')
    output.mkdir(parents=True, exist_ok=True)
    # Approval here applies exclusively to synthetic fixture content, never to course pages.
    source = output / 'fixture-source.txt'
    source.write_text('Synthetic RU/PL localization contract fixture.\n', encoding='utf-8')
    evidence = output / 'fixture-evidence.txt'
    evidence.write_text('Synthetic test approval, not M02-PL review evidence.\n', encoding='utf-8')
    data = {'schema_version': 1, 'pages': {}}
    for page_id, suffix in [('home', '/index.html'), ('practice-03-01', '/practice/03-01/index.html')]:
        page = {'source': {'locale': 'ru', 'path': source.name, 'sha256': sha256(source)}, 'variants': {}}
        if page_id.startswith('practice-'):
            page['practice_id'] = '03-01'
        for locale, meta in LOCALES.items():
            route = meta['prefix'] + suffix
            page['variants'][locale] = {'path': route, 'status': 'approved',
                'source_sha256': sha256(source), 'source_path': source.name, 'evidence_path': evidence.name}
            dest = output / route.lstrip('/')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.touch()
        data['pages'][page_id] = page
    routes = Routes(data, root=output, site_dir=output)
    for page_id, page in routes.pages.items():
        for locale, variant in page['variants'].items():
            path = output / variant['path'].lstrip('/')
            title = UI_STRINGS[locale]['home' if page_id == 'home' else 'practice']
            record = PageRecord(path, variant['path'], title, title, locale, 'home' if page_id == 'home' else 'practice')
            sections = ''.join(f'<section id="{anchor}"><h2>{html.escape(UI_STRINGS[locale][key])}</h2></section>' for anchor, key in NAV_KEYS)
            path.write_text(f'''<!DOCTYPE html>
<html lang="{LOCALES[locale]['html_lang']}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><link rel="stylesheet" href="/assets/css/theory.css">
<link rel="stylesheet" href="/assets/css/localization.css">{_seo_block(record, [record], routes)}</head><body>
{site_header(page_id=page_id, locale=locale, routes=routes)}
<aside id="mobile-nav-panel" class="sidebar">{mobile_nav_links(page_id=page_id, locale=locale, routes=routes)}</aside>
<main><h1>{title}</h1>{sections}</main><script src="/assets/js/nav.js" defer></script>
</body></html>''', encoding='utf-8')
    return routes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    build(parser.parse_args().output)
