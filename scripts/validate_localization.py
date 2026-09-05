#!/usr/bin/env python3
"""Validate localization contracts and the frozen M02 RU delivery baseline."""
from localization import (ROOT, MANIFEST_DIR, DEFAULT_LOCALE, LOCALES,
                          UI_STRINGS, TERMINOLOGY, Routes, read_json, sha256)


def validate() -> None:
    assert DEFAULT_LOCALE == 'ru'
    assert LOCALES['ru']['prefix'] == '' and LOCALES['pl']['prefix'] == '/pl'
    assert len({v['prefix'] for v in LOCALES.values()}) == len(LOCALES)
    for locale, metadata in LOCALES.items():
        assert metadata['html_lang'] == locale
        assert UI_STRINGS[locale].keys() == UI_STRINGS[DEFAULT_LOCALE].keys()
        assert all(isinstance(s, str) and s for s in UI_STRINGS[locale].values())
    assert UI_STRINGS['pl']['practice'] == 'Praktyka'
    assert TERMINOLOGY['practice_rule']['exercise_forms'] == ['ćwiczenie', 'ćwiczenia', 'ćwiczeń']
    assert all(TERMINOLOGY['terms'].values())
    assert len(set(TERMINOLOGY['protected_terms'])) == len(TERMINOLOGY['protected_terms'])
    routes = Routes()
    baseline = read_json(MANIFEST_DIR / 'ru_baseline.json')
    current = sorted('/' + p.relative_to(ROOT / 'site').as_posix()
                     for p in (ROOT / 'site').rglob('*.html')
                     if not any(p.relative_to(ROOT / 'site').as_posix().startswith(v['prefix'].lstrip('/') + '/')
                                for v in LOCALES.values() if v['prefix']))
    assert current == baseline['ru_paths'], 'Frozen RU routes changed'
    for page in routes.pages.values():
        assert page['variants'][DEFAULT_LOCALE]['path'] in baseline['ru_paths']
    for artifact in ('pdf', 'epub'):
        spec = baseline[artifact]
        assert sha256(ROOT / spec['path']) == spec['sha256'], f'{artifact} changed'
    frozen_m01 = set(baseline['m01']['files'])
    actual_m01 = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/m01').rglob('*') if p.is_file()}
    actual_m01.add('manifest/ru_content_audit_inventory.json')
    assert actual_m01 == frozen_m01, 'M01 file inventory changed'
    for path, digest in baseline['m01']['files'].items():
        assert sha256(ROOT / path) == digest, f'M01 changed: {path}'
    # Staged routes cannot be accidentally deployed as placeholder HTML.
    for path in (ROOT / 'site').glob('pl/**/*.html'):
        url = '/' + path.relative_to(ROOT / 'site').as_posix()
        page_id = routes.by_path.get(url)
        assert page_id and routes.available(page_id).get('pl') == url, f'Unapproved PL output: {url}'
    print(f'PASS: localization; RU paths={len(current)}; M01/PDF/EPUB unchanged')


if __name__ == '__main__':
    validate()
