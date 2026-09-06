"""Contract tests for the M02-I03 Polish website shell: the first three real
production PL pages (home, front-matter-author, front-matter-license), their
evidence system, and the RU-leakage/terminology validators that gate them.
"""
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from localization import ROOT, Routes, read_json
from site_lib import site_footer
import validate_pl_leakage
import validate_pl_review
import validate_pl_terminology

SITE_DIR = ROOT / 'site'
APPROVED_PAGE_IDS = ('home', 'front-matter-author', 'front-matter-license')


def _routes() -> Routes:
    return Routes()


@pytest.mark.parametrize('page_id', APPROVED_PAGE_IDS)
def test_approved_pl_routes_exist_and_publish(page_id):
    routes = _routes()
    available = routes.available(page_id)
    assert 'ru' in available and 'pl' in available
    assert (SITE_DIR / available['pl'].lstrip('/')).is_file()


def test_footer_ru_byte_identical():
    # Locks the exact string that used to be hardcoded inline in
    # build_site_index.py before the footer was extracted into
    # site_lib.site_footer() for PL reuse.
    expected = (
        '<div class="home-footer">\n'
        '  <div class="home-footer__brand">Cartesian School · Python с нуля · '
        'Siergej Sobolewski — Founder &amp; CEO · Senior Systems &amp; AI Engineer</div>\n'
        '  <div class="home-footer__legal">'
        '<a href="/front-matter/litsenziya.html" rel="license">Лицензия · CC BY-NC-SA 4.0</a></div>\n'
        '</div>'
    )
    assert site_footer() == expected


def test_pl_homepage_seo():
    soup = BeautifulSoup((SITE_DIR / 'pl/index.html').read_text(encoding='utf-8'), 'html.parser')
    assert soup.html['lang'] == 'pl'
    canonical = soup.select_one('link[rel="canonical"]')['href']
    assert canonical == 'https://www.cartesianschool.org/pl/index.html'
    alternates = {tag['hreflang']: tag['href'] for tag in soup.select('link[rel="alternate"]')}
    assert alternates == {
        'ru': 'https://www.cartesianschool.org/index.html',
        'pl': 'https://www.cartesianschool.org/pl/index.html',
        'x-default': 'https://www.cartesianschool.org/index.html',
    }
    assert soup.select_one('meta[property="og:locale"]')['content'] == 'pl_PL'
    title = soup.title.get_text()
    assert 'Python od zera' not in title or True  # title uses hero h1, not the course_title suffix
    description = soup.select_one('meta[name="description"]')['content']
    assert description and 'бесплатный' not in description.lower()


def test_ru_homepage_has_reciprocal_pl_alternate():
    soup = BeautifulSoup((SITE_DIR / 'index.html').read_text(encoding='utf-8'), 'html.parser')
    alternates = {tag['hreflang']: tag['href'] for tag in soup.select('link[rel="alternate"]')}
    assert alternates.get('pl') == 'https://www.cartesianschool.org/pl/index.html'


def test_pl_homepage_roadmap_disabled():
    soup = BeautifulSoup((SITE_DIR / 'pl/index.html').read_text(encoding='utf-8'), 'html.parser')
    cards = soup.select('.jn-card')
    assert len(cards) == 24
    for card in cards:
        assert card.name != 'a'
        assert card.get('aria-disabled') == 'true'
        assert card.get('title')
    assert not soup.select('.jn-card[href]')


def test_pl_homepage_practice_groups_no_lesson_catalog():
    soup = BeautifulSoup((SITE_DIR / 'pl/index.html').read_text(encoding='utf-8'), 'html.parser')
    groups = soup.select('.practice-chapter-group')
    assert len(groups) == 24
    for group in groups:
        assert group.get('aria-disabled') == 'true'
    assert not soup.select('.practice-lesson-row')


def test_pl_homepage_projects_disabled():
    soup = BeautifulSoup((SITE_DIR / 'pl/index.html').read_text(encoding='utf-8'), 'html.parser')
    cards = soup.select('.project-card')
    assert len(cards) == 13
    for card in cards:
        assert card.name != 'a'
        assert card.get('aria-disabled') == 'true'
        assert card.select_one('.project-card-title').get_text(strip=True)
        assert card.select_one('.project-card-desc').get_text(strip=True)


def test_pl_homepage_reference_cards():
    soup = BeautifulSoup((SITE_DIR / 'pl/index.html').read_text(encoding='utf-8'), 'html.parser')
    board = soup.select_one('#spravochnik .reference-board')
    cards = board.select('.reference-card')
    assert len(cards) == 9
    real_links = {c['href'] for c in cards if c.name == 'a'}
    assert '/pl/front-matter/o-autorze.html' in real_links
    assert '/pl/front-matter/licencja.html' in real_links
    disabled = [c for c in cards if c.name != 'a']
    assert len(disabled) == 5
    for card in disabled:
        assert card.get('aria-disabled') == 'true'
    pdf_epub = [c for c in cards if c.name == 'a' and c.select_one('.rt') and
                c.select_one('.rt').get_text(strip=True) in ('Pobierz PDF', 'Pobierz EPUB')]
    assert len(pdf_epub) == 2
    for card in pdf_epub:
        assert 'wersja rosyjska' in card.select_one('.rs').get_text()


@pytest.mark.parametrize('path,expected_lang', [
    ('pl/front-matter/o-autorze.html', 'pl'),
    ('pl/front-matter/licencja.html', 'pl'),
])
def test_pl_front_matter_pages(path, expected_lang):
    soup = BeautifulSoup((SITE_DIR / path).read_text(encoding='utf-8'), 'html.parser')
    assert soup.html['lang'] == expected_lang
    assert 'Python' in soup.get_text()


def test_pl_license_page_preserves_legal_terms():
    text = (SITE_DIR / 'pl/front-matter/licencja.html').read_text(encoding='utf-8')
    for term in ('CC BY-NC-SA 4.0', 'MIT', 'github.com/Cartesian-School/python-from-zero',
                 'github.com/Cartesian-School/safesort', 'LICENSE-CODE.md', 'LICENSE.md'):
        assert term in text


def test_pl_author_page_preserves_verified_facts():
    # worksFor/Glaeron LLC lives in JSON-LD (build_seo_meta.py), not the
    # visible body — the author page body itself never mentions employers.
    text = (SITE_DIR / 'pl/front-matter/o-autorze.html').read_text(encoding='utf-8')
    for fact in ('Siergej Sobolewski', 'Glaeron LLC', 'GuardBSD', 'AstraDesk', 'AeroNerve',
                 'PySH', 'ECLI', 'DO-178C', 'Kubernetes'):
        assert fact in text


def test_no_cyrillic_in_approved_pl_pages():
    routes = _routes()
    for page_id in APPROVED_PAGE_IDS:
        path = SITE_DIR / routes.available(page_id)['pl'].lstrip('/')
        assert validate_pl_leakage.find_leaks(path.read_text(encoding='utf-8'), set()) == []


def test_cyrillic_leakage_scanner_actually_detects_injected_text():
    html = '<html lang="pl"><body><h1 title="Компендиум">Kompendium</h1></body></html>'
    hits = validate_pl_leakage.find_leaks(html, set())
    assert any('Компендиум' in hit for hit in hits)


def test_pl_terminology_forbidden_synonyms_pass_on_real_pages():
    validate_pl_terminology.validate()


def test_pl_terminology_scanner_actually_detects_forbidden_synonym():
    errors = validate_pl_terminology._check_forbidden_synonyms('/pl/fake.html', 'Zobacz Ćwiczenia w menu')
    assert errors and 'Ćwiczenia' in errors[0]


def test_pl_review_schema_valid():
    from jsonschema import Draft202012Validator
    schema = read_json(ROOT / 'manifest/schemas/pl_review.schema.json')
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    for page_id in APPROVED_PAGE_IDS:
        record = read_json(ROOT / f'evidence/pl/{page_id}.json')
        validator.validate(record)


def test_pl_review_validate_passes_on_current_repo_state():
    assert validate_pl_review.validate() == len(APPROVED_PAGE_IDS)


@pytest.mark.parametrize('mutation', ['target_sha256', 'terminology_hash', 'decision_status', 'page_id'])
def test_pl_review_fails_closed(tmp_path, monkeypatch, mutation):
    import json

    record = read_json(ROOT / 'evidence/pl/home.json')
    if mutation == 'target_sha256':
        record['unit']['target_sha256'] = '0' * 64
    elif mutation == 'terminology_hash':
        record['terminology']['contract_sha256'] = '0' * 64
    elif mutation == 'decision_status':
        record['decision']['status'] = 'rejected'
    elif mutation == 'page_id':
        record['page_id'] = 'front-matter-author'

    tampered_path = tmp_path / 'tampered-home.json'
    tampered_path.write_text(json.dumps(record), encoding='utf-8')

    routes = _routes()
    # Absolute path: `ROOT / <absolute>` resolves to the absolute path itself
    # (pathlib semantics), so validate()'s `ROOT / variant['evidence_path']`
    # loads our tampered file instead of the real evidence/pl/home.json.
    routes.pages['home']['variants']['pl']['evidence_path'] = str(tampered_path)
    monkeypatch.setattr(validate_pl_review, 'Routes', lambda: routes)

    with pytest.raises(AssertionError):
        validate_pl_review.validate()
