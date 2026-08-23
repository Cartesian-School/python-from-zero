"""Регрессионный набор для итогового проекта главы 22 (список задач на
Flask + SQLite): маршруты, персистентность, валидация, JSON API, SQL-
инъекция, экранирование Jinja, миграция схемы и перенос данных через JSON.

Все тесты используют настоящий production-код
(projects/flask/todo-app/app.py), а не его копии, и работают на временной
базе данных, изолированной от git-репозитория.
"""

import importlib
import json
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "projects" / "flask" / "todo-app"
sys.path.insert(0, str(APP_DIR))

import app as todoapp  # noqa: E402


@pytest.fixture
def temp_db_path(tmp_path):
    return str(tmp_path / "zadachi_test.db")


@pytest.fixture
def app_instance(temp_db_path, monkeypatch):
    """Свежий экземпляр приложения на изолированной временной базе данных
    для каждого теста — тесты не должны трогать репозиторную базу."""
    monkeypatch.setitem(todoapp.app.config, "DATABASE", temp_db_path)
    todoapp.app.config.update(TESTING=True)
    with todoapp.app.app_context():
        todoapp.init_db()
    yield todoapp.app


@pytest.fixture
def client(app_instance):
    return app_instance.test_client()


def db_rows(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------- маршрутизация ----------

def test_glavnaya_pustoj_spisok(client):
    otvet = client.get("/")
    assert otvet.status_code == 200
    assert "Задач пока нет" in otvet.get_data(as_text=True)


def test_privet_podstavlyaet_imya(client):
    otvet = client.get("/privet/Ада")
    assert otvet.status_code == 200
    assert "Привет, Ада!" in otvet.get_data(as_text=True)


def test_dobavit_redirect(client):
    otvet = client.post("/dobavit", data={"zadacha": "Купить хлеб"})
    assert otvet.status_code in (302, 303)
    assert otvet.headers["Location"].endswith("/")


def test_neizvestnyj_adres_404(client):
    otvet = client.get("/takogo-adresa-net")
    assert otvet.status_code == 404
    assert "Страница не найдена" in otvet.get_data(as_text=True)


def test_neizvestnyj_api_adres_404_json(client):
    otvet = client.get("/api/takogo-adresa-net")
    assert otvet.status_code == 404
    assert otvet.content_type == "application/json"
    assert otvet.get_json() == {"error": "not found"}


# ---------- база данных: сохранение, изменение, удаление ----------

def test_dobavlennaya_zadacha_soxranyaetsya(client, temp_db_path):
    client.post("/dobavit", data={"zadacha": "Купить хлеб"}, follow_redirects=True)
    stroki = db_rows(temp_db_path)
    assert len(stroki) == 1
    assert stroki[0]["title"] == "Купить хлеб"
    assert stroki[0]["done"] == 0


def test_vypolnit_perekluchaet_status(client, temp_db_path):
    client.post("/dobavit", data={"zadacha": "Полить цветы"}, follow_redirects=True)
    task_id = db_rows(temp_db_path)[0]["id"]

    client.post(f"/vypolnit/{task_id}", follow_redirects=True)
    assert db_rows(temp_db_path)[0]["done"] == 1

    client.post(f"/vypolnit/{task_id}", follow_redirects=True)
    assert db_rows(temp_db_path)[0]["done"] == 0


def test_udalit_ubiraet_zapis(client, temp_db_path):
    client.post("/dobavit", data={"zadacha": "Временная задача"}, follow_redirects=True)
    task_id = db_rows(temp_db_path)[0]["id"]

    client.post(f"/udalit/{task_id}", follow_redirects=True)
    assert db_rows(temp_db_path) == []


def test_vypolnit_nesushchestvuyushchej_zadachi_404(client):
    otvet = client.post("/vypolnit/999999")
    assert otvet.status_code == 404


def test_udalit_nesushchestvuyushchej_zadachi_404(client):
    otvet = client.post("/udalit/999999")
    assert otvet.status_code == 404


def test_persistence_posle_novogo_ekzemplyara_prilozheniya(temp_db_path, monkeypatch):
    """Новый объект приложения на том же файле базы данных должен видеть
    те же задачи — то есть вести себя так же, как после перезапуска
    процесса (раздел 22.20 сайта)."""
    monkeypatch.setitem(todoapp.app.config, "DATABASE", temp_db_path)
    with todoapp.app.app_context():
        todoapp.init_db()
    client1 = todoapp.app.test_client()
    client1.post("/dobavit", data={"zadacha": "Переживает перезапуск"}, follow_redirects=True)

    del sys.modules["app"]
    import app as todoapp2  # noqa: E402

    monkeypatch.setitem(todoapp2.app.config, "DATABASE", temp_db_path)
    client2 = todoapp2.app.test_client()
    otvet = client2.get("/api/tasks")
    zadachi = otvet.get_json()

    assert len(zadachi) == 1
    assert zadachi[0]["title"] == "Переживает перезапуск"


# ---------- валидация ----------

def test_pustaya_zadacha_ne_dobavlyaetsya(client, temp_db_path):
    client.post("/dobavit", data={"zadacha": "   "}, follow_redirects=True)
    assert db_rows(temp_db_path) == []


def test_slishkom_dlinnaya_zadacha_otklonyaetsya(client, temp_db_path):
    client.post("/dobavit", data={"zadacha": "а" * 201}, follow_redirects=True)
    assert db_rows(temp_db_path) == []


def test_zadacha_maksimalnoj_dliny_prinimaetsya(client, temp_db_path):
    client.post("/dobavit", data={"zadacha": "а" * 200}, follow_redirects=True)
    assert len(db_rows(temp_db_path)) == 1


def test_probely_po_krayam_obrezayutsya(client, temp_db_path):
    client.post("/dobavit", data={"zadacha": "  Купить хлеб  "}, follow_redirects=True)
    assert db_rows(temp_db_path)[0]["title"] == "Купить хлеб"


# ---------- Jinja-экранирование (раздел 22.32 сайта) ----------

def test_script_teg_v_nazvanii_ekranируется(client):
    client.post("/dobavit", data={"zadacha": "<script>alert(1)</script>"}, follow_redirects=True)
    html = client.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


# ---------- SQL-инъекция (раздел 22.32 сайта) ----------

def test_sql_pohozhij_vvod_hranitsya_kak_dannye(client, temp_db_path):
    zlovrednyj_tekst = "'); DROP TABLE tasks; --"
    client.post("/dobavit", data={"zadacha": zlovrednyj_tekst}, follow_redirects=True)

    stroki = db_rows(temp_db_path)
    assert len(stroki) == 1
    assert stroki[0]["title"] == zlovrednyj_tekst

    # Таблица physически цела — параметризация не дала тексту стать SQL-командой.
    conn = sqlite3.connect(temp_db_path)
    tablicy = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    conn.close()
    assert "tasks" in tablicy


# ---------- JSON API ----------

def test_api_tasks_get_vozvrashchaet_json(client):
    client.post("/dobavit", data={"zadacha": "Купить хлеб"}, follow_redirects=True)
    otvet = client.get("/api/tasks")

    assert otvet.status_code == 200
    assert otvet.content_type == "application/json"
    dannye = otvet.get_json()
    assert isinstance(dannye, list)
    assert dannye[0]["title"] == "Купить хлеб"
    assert dannye[0]["done"] is False
    assert isinstance(dannye[0]["id"], int)


def test_api_tasks_post_dobavlyaet_zadachu(client, temp_db_path):
    otvet = client.post("/api/tasks", json={"title": "Через API"})
    assert otvet.status_code == 201
    telo = otvet.get_json()
    assert telo["title"] == "Через API"
    assert telo["done"] is False
    assert db_rows(temp_db_path)[0]["title"] == "Через API"


def test_api_tasks_post_bez_title_400(client):
    otvet = client.post("/api/tasks", json={})
    assert otvet.status_code == 400
    assert "error" in otvet.get_json()


def test_api_tasks_post_pustoj_title_400(client):
    otvet = client.post("/api/tasks", json={"title": "   "})
    assert otvet.status_code == 400


def test_api_response_eto_validnyj_json_a_ne_python_repr(client):
    """Раздел 22.15 сайта: JSON — не то же самое, что распечатка dict
    Python (одинарные кавычки, True/False с большой буквы)."""
    client.post("/dobavit", data={"zadacha": "Проверка формата"}, follow_redirects=True)
    otvet = client.get("/api/tasks")
    syroj_tekst = otvet.get_data(as_text=True)

    # Настоящий JSON не парсится как питоновский repr словаря.
    razobrannyj = json.loads(syroj_tekst)
    assert razobrannyj[0]["title"] == "Проверка формата"
    assert "'" not in syroj_tekst.replace("Проверка формата", "")


# ---------- миграция схемы (раздел 22.27 сайта) ----------

def test_migraciya_shemy_dobavlyaet_stolbec_soxranyaya_stroki(tmp_path):
    put = str(tmp_path / "migraciya.db")
    conn = sqlite3.connect(put)
    conn.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
    conn.execute("INSERT INTO tasks (title) VALUES ('Задача версии 1')")
    conn.commit()

    conn.execute("ALTER TABLE tasks ADD COLUMN done INTEGER NOT NULL DEFAULT 0")
    conn.commit()

    stroki = conn.execute("SELECT id, title, done FROM tasks").fetchall()
    conn.close()

    assert len(stroki) == 1
    assert stroki[0][1] == "Задача версии 1"
    assert stroki[0][2] == 0


# ---------- перенос данных через JSON (раздел 22.28 сайта) ----------

def test_perenos_dannyh_cherez_json_roundtrip(tmp_path):
    istochnik_put = str(tmp_path / "istochnik.db")
    cel_put = str(tmp_path / "cel.db")

    istochnik = sqlite3.connect(istochnik_put)
    istochnik.row_factory = sqlite3.Row
    istochnik.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
    istochnik.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        [("Задача А", 0), ("Задача Б", 1), ("Задача В", 0)],
    )
    istochnik.commit()

    iskhodnye_stroki = istochnik.execute("SELECT title, done FROM tasks ORDER BY id").fetchall()
    dannye = [dict(r) for r in iskhodnye_stroki]
    tekst_json = json.dumps(dannye, ensure_ascii=False)
    istochnik.close()

    # Проверяем, что промежуточный формат — валидный, настоящий JSON.
    zagruzhennye = json.loads(tekst_json)

    cel = sqlite3.connect(cel_put)
    cel.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
    for zapis in zagruzhennye:
        cel.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (zapis["title"], zapis["done"]))
    cel.commit()

    itogovye_stroki = cel.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    cel.close()

    assert len(itogovye_stroki) == len(iskhodnye_stroki) == 3
    assert [r[1] for r in itogovye_stroki] == [r["title"] for r in iskhodnye_stroki]
    assert [r[2] for r in itogovye_stroki] == [r["done"] for r in iskhodnye_stroki]
    # Новые id должны остаться уникальными (перегенерированы целевой базой).
    novye_id = [r[0] for r in itogovye_stroki]
    assert len(novye_id) == len(set(novye_id))


# ---------- flash / session (раздел 22.30 сайта) ----------

def test_flash_soobshchenie_pokazyvaetsya_odin_raz(client):
    client.post("/dobavit", data={"zadacha": "   "}, follow_redirects=False)
    otvet1 = client.get("/")
    otvet2 = client.get("/")

    telo1 = otvet1.get_data(as_text=True)
    telo2 = otvet2.get_data(as_text=True)

    assert "не может быть пустым" in telo1
    assert "не может быть пустым" not in telo2


# ---------- сквозная приёмочная проверка (раздел 22.51 спецификации) ----------

def test_polnyj_scenarij_ot_pustogo_spiska_do_udaleniya(temp_db_path, monkeypatch):
    monkeypatch.setitem(todoapp.app.config, "DATABASE", temp_db_path)
    with todoapp.app.app_context():
        todoapp.init_db()
    client = todoapp.app.test_client()

    assert "Задач пока нет" in client.get("/").get_data(as_text=True)

    client.post("/dobavit", data={"zadacha": "Задача А"}, follow_redirects=True)
    assert "Задача А" in client.get("/").get_data(as_text=True)

    task_id = db_rows(temp_db_path)[0]["id"]
    client.post(f"/vypolnit/{task_id}", follow_redirects=True)
    assert db_rows(temp_db_path)[0]["done"] == 1

    client.post("/dobavit", data={"zadacha": "'); DROP TABLE tasks; --"}, follow_redirects=True)
    assert len(db_rows(temp_db_path)) == 2

    client.post("/dobavit", data={"zadacha": "<script>alert(1)</script>"}, follow_redirects=True)
    assert "<script>alert(1)</script>" not in client.get("/").get_data(as_text=True)

    otvet_api = client.get("/api/tasks")
    assert otvet_api.status_code == 200
    assert isinstance(otvet_api.get_json(), list)
    assert len(otvet_api.get_json()) == 3

    client.post(f"/udalit/{task_id}", follow_redirects=True)
    assert len(db_rows(temp_db_path)) == 2
