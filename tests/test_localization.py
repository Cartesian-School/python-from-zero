"""Executable M02 URL, terminology, publication and rendering contracts."""
import copy
import json
from pathlib import Path
import sys

import pytest
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from localization import (ROOT, MANIFEST_DIR, LOCALES, UI_STRINGS, TERMINOLOGY,
                          Routes, read_json, polish_count, effective_status, validate_routes)
from build_localization_fixture import build
from site_structure import _classify
from validate_localization import validate


def test_frozen_baseline():
    validate()


@pytest.mark.parametrize('number,noun', [(0,'ćwiczeń'),(1,'ćwiczenie'),(2,'ćwiczenia'),
    (3,'ćwiczenia'),(4,'ćwiczenia'),(5,'ćwiczeń'),(10,'ćwiczeń'),(12,'ćwiczeń'),
    (21,'ćwiczeń'),(22,'ćwiczenia'),(24,'ćwiczenia'),(25,'ćwiczeń'),
    (101,'ćwiczeń'),(112,'ćwiczeń'),(114,'ćwiczeń'),(122,'ćwiczenia')])
def test_polish_counters(number, noun):
    assert polish_count(number, TERMINOLOGY['practice_rule']['exercise_forms']) == f'{number} {noun}'


@pytest.mark.parametrize('number', [-1, True, 1.5, '2'])
def test_invalid_counts(number):
    with pytest.raises(ValueError):
        polish_count(number, ('a','b','c'))


def test_glossary_contract():
    assert TERMINOLOGY['terms'] == {'Глава':'Rozdział','Практика':'Praktyka',
        'практическое задание':'ćwiczenie','упражнение':'ćwiczenie',
        'Практические задания':'Ćwiczenia','Справочник':'Kompendium',
        'переменная':'zmienna','строка':'łańcuch znaków','список':'lista',
        'словарь':'słownik','множество':'zbiór','исключение':'wyjątek','область видимости':'zasięg'}
    assert UI_STRINGS['pl']['practice'] == 'Praktyka'
    assert set('Python|Python 3.14|REPL|traceback|pip|PyPI|Git|GitHub|Tkinter|Turtle|Pygame|Flask|HTML|CSS|JavaScript|JSON|CLI|API'.split('|')) <= set(TERMINOLOGY['protected_terms'])
    assert set('print input len int float str list dict set tuple Exception'.split()) <= set(TERMINOLOGY['protected_identifiers'])


def test_missing_translation():
    routes = Routes()
    assert routes.available('home') == {'ru':'/index.html'}
    assert routes.alternates('/index.html') == {}
    switch = BeautifulSoup(routes.switcher('home', 'ru'), 'html.parser')
    assert switch.select_one('[aria-disabled="true"]')['lang'] == 'pl'
    assert not switch.select('a')


@pytest.mark.parametrize('bad_path', ['/index.html','/ru/index.html','/pl/../index.html',
                                      '/pl//index.html','/pl/rozdział.html','https://evil.test/a.html'])
def test_bad_paths(bad_path):
    data = read_json(MANIFEST_DIR / 'routes.json')
    data['pages']['home']['variants']['pl']['path'] = bad_path
    with pytest.raises(ValueError):
        validate_routes(data)


def test_duplicate_identity_and_paths(tmp_path):
    path = tmp_path / 'duplicate.json'
    path.write_text('{"home":1,"home":2}')
    with pytest.raises(ValueError):
        read_json(path)
    data = read_json(MANIFEST_DIR / 'routes.json')
    data['pages']['duplicate'] = copy.deepcopy(data['pages']['home'])
    with pytest.raises(ValueError):
        validate_routes(data)


def test_practice_identity():
    data = read_json(MANIFEST_DIR / 'routes.json')
    assert '03-01' in read_json(ROOT / 'manifest/practice_manifest.json')
    data['pages']['practice-03-01']['variants']['pl']['path'] = '/pl/practice/03-02/index.html'
    with pytest.raises(ValueError):
        validate_routes(data)
    client = (ROOT / 'web/src/practice-app.js').read_text()
    assert 'const PROGRESS_KEY = "cartesian.python.progress.v1"' in client
    assert 'all[lessonId] = entry' in client


def test_bilingual_fixture_and_determinism(tmp_path):
    routes = build(tmp_path)
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    for page_id, page in routes.pages.items():
        expected = routes.alternates(page['variants']['ru']['path'])
        assert set(expected) == {'ru','pl','x-default'}
        for locale, variant in page['variants'].items():
            soup = BeautifulSoup((tmp_path / variant['path'].lstrip('/')).read_text(), 'html.parser')
            assert soup.html['lang'] == locale
            assert soup.select_one('[rel="canonical"]')['href'].endswith(variant['path'])
            links = {tag['hreflang']: tag['href'] for tag in soup.select('link[rel="alternate"]')}
            assert links == {code:'https://www.cartesianschool.org'+url for code,url in expected.items()}
            for switch in soup.select('.language-switcher'):
                assert switch.select_one('[aria-current]')['lang'] == locale
                other = 'pl' if locale == 'ru' else 'ru'
                assert switch.a['href'] == page['variants'][other]['path']
            assert len(soup.select('.language-switcher')) == 2
            assert not any(0x1F1E6 <= ord(c) <= 0x1F1FF for c in str(soup))
    build(tmp_path)
    assert before == {p.relative_to(tmp_path):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}


def test_stale_and_publication_gates(tmp_path):
    routes = build(tmp_path)
    page = routes.pages['home']
    page['variants']['pl']['status'] = 'translated'
    assert 'pl' not in routes.available('home')
    page['variants']['pl']['status'] = 'reviewed'
    assert 'pl' not in routes.available('home')
    page['variants']['pl']['status'] = 'approved'
    (tmp_path / 'pl/index.html').unlink()
    assert 'pl' not in routes.available('home')
    (tmp_path / 'pl/index.html').touch()
    (tmp_path / 'fixture-source.txt').write_text('RU changed')
    assert effective_status(page, 'pl', tmp_path) == 'stale'
    assert 'pl' not in routes.available('home')
    with pytest.raises(ValueError, match='Stale'):
        validate_routes(routes.data, tmp_path)


def test_approved_requires_evidence():
    data = read_json(MANIFEST_DIR / 'routes.json')
    data['pages']['home']['variants']['pl']['status'] = 'approved'
    with pytest.raises(ValueError):
        validate_routes(data)


def test_locale_classification():
    assert _classify('/pl/index.html') == 'home'
    assert _classify('/pl/practice/03-01/index.html') == 'practice'
    assert _classify('/pl/chapters/rozdzial-01/index.html') == 'chapter-opener'
    assert LOCALES['ru']['prefix'] == ''
    assert LOCALES['pl']['prefix'] == '/pl'


def test_sitemap_reciprocity(tmp_path, monkeypatch):
    import build_sitemap
    from site_structure import PageRecord
    import xml.etree.ElementTree as ET
    routes = build(tmp_path)
    pages = [PageRecord(tmp_path / v['path'].lstrip('/'), v['path'], 'Fixture', 'Fixture', locale, 'home')
             for locale, v in routes.pages['home']['variants'].items()]
    output = tmp_path / 'sitemap.xml'
    monkeypatch.setattr(build_sitemap, 'Routes', lambda: routes)
    monkeypatch.setattr(build_sitemap, 'iter_pages', lambda: pages)
    monkeypatch.setattr(build_sitemap, 'OUT_PATH', output)
    monkeypatch.setattr(build_sitemap, 'SITE_DIR', tmp_path)
    build_sitemap.main()
    tree = ET.fromstring(output.read_text())
    assert len(tree) == 2
    for entry in tree:
        links = entry.findall('{http://www.w3.org/1999/xhtml}link')
        assert {x.attrib['hreflang'] for x in links} == {'ru','pl','x-default'}
        assert next(x.attrib['href'] for x in links if x.attrib['hreflang'] == 'x-default').endswith('/index.html')


def test_fixture_cannot_publish():
    with pytest.raises(ValueError, match='production'):
        build(ROOT / 'site/pl')


def test_invalid_identity_and_status():
    data = read_json(MANIFEST_DIR / 'routes.json')
    data['pages']['translated/slug'] = data['pages'].pop('home')
    with pytest.raises(ValueError, match='page ID'):
        validate_routes(data)
    data = read_json(MANIFEST_DIR / 'routes.json')
    data['pages']['home']['variants']['pl']['status'] = 'published'
    with pytest.raises(ValueError, match='state'):
        validate_routes(data)


def test_imported_source_change_invalidates_translation(tmp_path):
    from localization import source_hash
    routes = build(tmp_path)
    dependency = tmp_path / 'author.txt'
    dependency.write_text('Original canonical author profile')
    page = routes.pages['home']
    page['source']['dependencies'] = [dependency.name]
    page['source']['sha256'] = source_hash(page['source'], tmp_path)
    page['variants']['pl']['source_sha256'] = page['source']['sha256']
    assert effective_status(page, 'pl', tmp_path) == 'approved'
    dependency.write_text('Revised canonical author profile')
    assert effective_status(page, 'pl', tmp_path) == 'stale'


def test_sitemap_omits_unapproved_and_unknown_pl(tmp_path, monkeypatch):
    import build_sitemap
    from site_structure import PageRecord
    routes = build(tmp_path)
    routes.pages['home']['variants']['pl']['status'] = 'reviewed'
    pages = [PageRecord(tmp_path / 'ignored', path, 'Fixture', 'Fixture', 'pl', 'home')
             for path in ['/index.html', '/pl/index.html', '/pl/unknown.html']]
    monkeypatch.setattr(build_sitemap, 'Routes', lambda: routes)
    monkeypatch.setattr(build_sitemap, 'iter_pages', lambda: pages)
    monkeypatch.setattr(build_sitemap, 'SITE_DIR', tmp_path)
    monkeypatch.setattr(build_sitemap, 'OUT_PATH', tmp_path / 'sitemap.xml')
    build_sitemap.main()
    content = (tmp_path / 'sitemap.xml').read_text()
    assert '/pl/' not in content
    assert 'xhtml' not in content
    assert 'https://www.cartesianschool.org/index.html' in content


def test_machine_readable_route_schema():
    from jsonschema import Draft202012Validator
    schema = read_json(ROOT / 'manifest/schemas/localization_routes.schema.json')
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(read_json(MANIFEST_DIR / 'routes.json'))
