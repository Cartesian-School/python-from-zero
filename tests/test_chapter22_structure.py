"""Регрессионные проверки структуры главы 22: старые адреса страниц и
идентификаторы практик не должны исчезать или менять смысл после
расширения главы с 7 до 37 страниц."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-22"
MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"

ORIGINAL_ROUTES = [
    "index.html",
    "22-01-python-i-veb.html",
    "22-02-html.html",
    "22-03-css.html",
    "22-04-javascript.html",
    "22-05-flask.html",
    "22-06-itogi.html",
]

ORIGINAL_PRACTICE_IDS = ["22-02", "22-05"]


def test_originalnye_adresa_glavy_sohraneny():
    for imya_fajla in ORIGINAL_ROUTES:
        put = CHAPTER_DIR / imya_fajla
        assert put.exists(), f"Исходная страница {imya_fajla} исчезла"


def test_novye_stranicy_prisutstvuyut():
    for nomer in range(7, 37):
        sovpadeniya = list(CHAPTER_DIR.glob(f"22-{nomer:02d}-*.html"))
        assert sovpadeniya, f"Не найдена новая страница 22-{nomer:02d}"


def test_glava_soderzhit_37_stranic():
    vse_stranicy = list(CHAPTER_DIR.glob("*.html"))
    assert len(vse_stranicy) == 37


def test_originalnye_id_praktik_sohraneny_v_manifeste():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for practice_id in ORIGINAL_PRACTICE_IDS:
        assert practice_id in manifest, f"Практика {practice_id} исчезла из манифеста"


def test_praktiki_glavy_22_ssylayutsya_na_sushchestvuyushchie_stranicy():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    praktiki_22 = {k: v for k, v in manifest.items() if k.startswith("22-")}
    assert len(praktiki_22) == 22

    for practice_id, zapis in praktiki_22.items():
        return_put = ROOT / "site" / zapis["return_url"].lstrip("/")
        assert return_put.exists(), f"{practice_id}: return_url указывает на несуществующий файл {return_put}"


def test_fizicheskie_nomera_ne_vydumany_dlya_novyh_razdelov():
    """В опенере главы (site-item со ссылками на все 36 разделов) только
    у оригинальных разделов 22.1-22.6 должен быть номер бумажной
    страницы (si-page); у новых цифровых разделов 22.7-22.36 такого
    номера быть не должно — их не существовало в бумажной книге."""
    import re

    tekst = (CHAPTER_DIR / "index.html").read_text(encoding="utf-8")
    razdely_s_nomerom_stranicy = set()
    for blok in re.findall(r'<a class="section-item".*?</a>', tekst):
        nomer = re.search(r'"si-num">22\.(\d+)<', blok)
        est_stranica = 'si-page' in blok
        if nomer and est_stranica:
            razdely_s_nomerom_stranicy.add(int(nomer.group(1)))

    assert razdely_s_nomerom_stranicy == {1, 2, 3, 4, 5, 6}
