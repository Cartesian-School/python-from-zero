"""Регрессионные проверки для главы 22: определения ключевых терминов
"вперёд" (термин объясняется раньше, чем используется) не должны
исчезнуть при последующем редактировании, а исправленные неточности
и запрещённые формулировки не должны вернуться."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-22"


def stranica(imya_fajla: str) -> str:
    return (CHAPTER_DIR / imya_fajla).read_text(encoding="utf-8")


def bez_tegov(html: str) -> str:
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", html)


REQUIRED_TERMS = {
    "22-03-css.html": ["Cascading Style Sheets", "язык таблиц стилей"],
    "22-04-javascript.html": ["язык программирования", "ECMAScript"],
    "22-05-flask.html": ["веб-фреймворк"],
    "22-17-veb-frejmvorki.html": ["Flask", "Django", "FastAPI", "Starlette"],
    "22-23-sqlite.html": ["СУБД", "встраива", "sqlite3"],
    "22-25-nosql.html": ["ключ", "документ", "граф", "MongoDB", "Redis", "Cassandra", "Neo4j"],
}


def test_stranicy_soderzhat_obyazatelnye_terminy():
    for imya_fajla, terminy in REQUIRED_TERMS.items():
        tekst = stranica(imya_fajla)
        for termin in terminy:
            assert termin in tekst, f"{imya_fajla}: не найден обязательный термин {termin!r}"


def test_sqlite_opisan_kak_subd_a_ne_kak_otdelnyj_server():
    tekst = bez_tegov(stranica("22-23-sqlite.html"))
    assert "отдельного процесс" in tekst or "без отдельного процесса" in tekst


PROHIBITED_ANYWHERE = [
    "голый HTML",
    "Python-веб",
    "включает пример",
    "вживую",
    "магия",
    "под капотом",
    "зоопарк",
    "сайт запоминает",
    "HTTP помнит",
    "Flask сам",
    "программа разговаривает",
    "слабая типизация",
    "карта территории",
    "на слуху",
    "пора заменить",
    "попробуйте всё сразу",
]

# "BASE" встречается только как часть literal-строки app.config["DATABASE"]
# в примерах кода — сам акроним CAP/BASE в главе не используется.
FALSE_ABSOLUTES = [
    "CSS превращает голый HTML",
    "работает только в браузере",
    "SQL масштабируется только вертикально",
    "NoSQL масштабируется только горизонтально",
    "SQL — ACID, NoSQL — BASE",
    "хранит данные по столбцам вместо строк",
    "NoSQL не имеет схемы",
]

STALE_TITLES = [
    "Как устроен веб и где в нём работает Python",
    "Другие фреймворки Python-веба",
    "Flask, Django и FastAPI: как выбрать подход",
    "Практика: включает пример CSS",
    "HTML и CSS вживую",
]


def vse_stranicy_glavy():
    return sorted(CHAPTER_DIR.glob("*.html"))


def test_zapreshchennye_frazy_otsutstvuyut():
    for put in vse_stranicy_glavy():
        tekst = bez_tegov(put.read_text(encoding="utf-8"))
        for fraza in PROHIBITED_ANYWHERE:
            assert fraza not in tekst, f"{put.name}: найдена запрещённая формулировка {fraza!r}"


def test_lozhnye_absolyuty_otsutstvuyut():
    for put in vse_stranicy_glavy():
        tekst = bez_tegov(put.read_text(encoding="utf-8"))
        for fraza in FALSE_ABSOLUTES:
            assert fraza not in tekst, f"{put.name}: найдено ложное обобщение {fraza!r}"


def test_ustarevshie_zagolovki_otsutstvuyut():
    for put in vse_stranicy_glavy():
        tekst = put.read_text(encoding="utf-8")
        for zagolovok in STALE_TITLES:
            assert zagolovok not in tekst, f"{put.name}: найден устаревший заголовок {zagolovok!r}"


def test_nosql_ne_nazyvaet_mongodb_json_bukvalno():
    """MongoDB хранит документы в BSON, а не в буквальном JSON — упоминание
    JSON рядом с MongoDB допустимо только вместе с BSON, без утверждения,
    что MongoDB буквально хранит JSON."""
    tekst = bez_tegov(stranica("22-25-nosql.html"))
    assert "BSON" in tekst
