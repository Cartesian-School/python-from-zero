"""M02-I04 full Polish-course publication contracts."""

import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from localization import ROOT, Routes, read_json
import validate_pl_complete
import validate_pl_leakage
import validate_pl_terminology

SITE = ROOT / "site"


def test_complete_corpus_contract():
    assert validate_pl_complete.validate() == {
        "routes": 1160, "chapters": 24, "lessons": 624, "practice": 493, "projects": 13,
    }


def test_every_route_is_an_exact_publishable_pair():
    routes = Routes()
    assert len(routes.pages) == 1160
    for page_id, page in routes.pages.items():
        available = routes.available(page_id)
        assert available == {
            "ru": page["variants"]["ru"]["path"], "pl": page["variants"]["pl"]["path"],
        }
        assert routes.alternates(available["ru"]) == {
            "ru": available["ru"], "pl": available["pl"], "x-default": available["ru"],
        }


def test_pl_homepage_catalogs_are_fully_enabled():
    soup = BeautifulSoup((SITE / "pl/index.html").read_text(encoding="utf-8"), "html.parser")
    assert len(soup.select("a.jn-card")) == 24
    assert len(soup.select(".practice-chapter-group")) == 24
    assert len(soup.select(".practice-lesson-row[href]")) == 493
    assert len(soup.select("a.project-card")) == 13
    assert not soup.select(
        ".jn-card[aria-disabled], .practice-chapter-group[aria-disabled], "
        ".project-card[aria-disabled], #spravochnik .reference-card[aria-disabled]"
    )


def test_all_polish_pages_have_no_accidental_cyrillic():
    routes = Routes()
    for page_id in routes.pages:
        path = SITE / routes.available(page_id)["pl"].lstrip("/")
        assert validate_pl_leakage.find_leaks(path.read_text(encoding="utf-8"), set()) == []


def test_binding_terminology_across_complete_corpus():
    assert validate_pl_terminology.validate() == 1160


def test_author_and_license_preserve_governed_facts():
    author = (SITE / "pl/front-matter/o-autorze.html").read_text(encoding="utf-8")
    for fact in ("Siergej Sobolewski", "Glaeron LLC", "GuardBSD", "AstraDesk", "AeroNerve",
                 "PySH", "ECLI", "DO-178C", "Kubernetes"):
        assert fact in author
    license_page = (SITE / "pl/front-matter/licencja.html").read_text(encoding="utf-8")
    for term in ("CC BY-NC-SA 4.0", "MIT", "LICENSE-CODE.md", "LICENSE.md"):
        assert term in license_page


def test_translation_memory_is_complete_and_traceable():
    memory = read_json(ROOT / "manifest/i18n/content/pl/course_translation_memory.json")
    assert memory["schema_version"] == 1
    assert memory["source_locale"] == "ru" and memory["target_locale"] == "pl"
    assert memory["entries"] and memory["entries"].keys() == memory["sources"].keys()
    assert all(memory["entries"].values())


def test_leakage_validator_catches_script_config_regressions():
    """Regression guard: an earlier find_leaks() decomposed <script> tags
    before scanning, which produced a false PASS on real leakage (practice
    config chapterTitle/lessonTitle serialized into a <script type="module">
    block). Prove the validator now fails on it."""
    poisoned = (
        '<html lang="pl"><head></head><body>'
        '<script type="module">initPracticeApp({...{"lessonId":"03-01",'
        '"chapterTitle":"Глава 3: Тест","lessonTitle":"Тестовый урок"}});</script>'
        "</body></html>"
    )
    assert validate_pl_leakage.find_leaks(poisoned, set()) != []


def test_leakage_validator_catches_manual_completion_ui_regressions():
    """Regression guard for the manual-completion status/button/confirm text
    that used to leak Russian into the PL runtime UI (site_lib.py's
    local_required_card / build_practice_pages.py's build_local_required_page
    embed this directly as <script> string literals, not visible HTML)."""
    cases = {
        "completion status": (
            '<script>status.innerHTML = "✓ Выполнено локально '
            '— результат не проверялся автоматически";</script>'
        ),
        "completion button": '<script>btn.textContent = "Отметить заново";</script>',
        "confirmation message": (
            '<script>window.confirm("Подтвердите: вы самостоятельно '
            'выполнили это упражнение локально");</script>'
        ),
    }
    for label, script in cases.items():
        html = f'<html lang="pl"><head></head><body>{script}</body></html>'
        assert validate_pl_leakage.find_leaks(html, set()) != [], label


def test_shared_progress_identity_remains_locale_neutral():
    client = (ROOT / "web/src/practice-app.js").read_text(encoding="utf-8")
    assert 'const PROGRESS_KEY = "cartesian.python.progress.v1"' in client
    assert "cartesian.python.progress.pl" not in client
    assert "cartesian.python.progress.ru" not in client
