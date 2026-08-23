"""Мини-сайт «Список задач» на Flask с постоянным хранением в SQLite.

Проект к главе 22 книги «Python с нуля» (Cartesian School).
Запуск (сервер разработки): python app.py, затем откройте
http://127.0.0.1:5000/ в браузере. Раздел 22.34 сайта объясняет, чем
сервер разработки отличается от рабочего развёртывания — использовать
этот способ запуска для реальной эксплуатации не стоит.
"""

import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, flash, g, get_flashed_messages, jsonify, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
DEFAULT_DB_PATH = BASE_DIR / "zadachi.db"

MAX_TITLE_LENGTH = 200

app = Flask(__name__)
app.config["DATABASE"] = os.environ.get("TODO_APP_DB", str(DEFAULT_DB_PATH))
# Значение по умолчанию явно помечено как непригодное для реальной
# эксплуатации — раздел 22.30 сайта объясняет, зачем вообще нужен секретный
# ключ и почему подписанные данные сессии — не то же самое, что зашифрованные.
app.config["SECRET_KEY"] = os.environ.get("TODO_APP_SECRET_KEY", "dev-only-secret-do-not-use-in-production")


# -- база данных: одно подключение на запрос (раздел 22.29 сайта) ----------

def get_db() -> sqlite3.Connection:
    """Открывает соединение лениво и хранит его в g — специальном месте
    Flask для данных, живущих ровно один запрос. teardown_appcontext ниже
    закрывает его сразу после того, как запрос обработан."""
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception: BaseException | None = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Создаёт таблицы схемы, если их ещё нет — вызывать внутри app_context()."""
    db = get_db()
    with open(SCHEMA_PATH, encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())
    db.commit()


@app.cli.command("init-db")
def init_db_command() -> None:
    """flask --app app.py init-db — создать таблицы в текущей базе данных."""
    init_db()
    print("База данных готова:", app.config["DATABASE"])


# -- вспомогательные функции ------------------------------------------------

def task_row_to_dict(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


def clean_title(raw_title: str) -> str | None:
    """Возвращает очищенное название задачи или None, если оно недопустимо
    (раздел 22.31 сайта: пустое или слишком длинное значение отклоняется)."""
    title = raw_title.strip()
    if not title or len(title) > MAX_TITLE_LENGTH:
        return None
    return title


# -- HTML-маршруты -----------------------------------------------------------

@app.route("/")
def glavnaya():
    db = get_db()
    zadachi = db.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    return render_template("index.html", zadachi=zadachi)


@app.route("/privet/<imya>")
def privet(imya):
    return render_template("privet.html", imya=imya)


@app.route("/dobavit", methods=["POST"])
def dobavit():
    title = clean_title(request.form.get("zadacha", ""))
    if title is None:
        flash("Название задачи не может быть пустым и не длиннее 200 символов.")
        return redirect(url_for("glavnaya"))
    db = get_db()
    db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    return redirect(url_for("glavnaya"))


@app.route("/vypolnit/<int:task_id>", methods=["POST"])
def vypolnit(task_id):
    db = get_db()
    stroka = db.execute("SELECT id, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if stroka is None:
        abort(404)
    db.execute("UPDATE tasks SET done = ? WHERE id = ?", (0 if stroka["done"] else 1, task_id))
    db.commit()
    return redirect(url_for("glavnaya"))


@app.route("/udalit/<int:task_id>", methods=["POST"])
def udalit(task_id):
    db = get_db()
    stroka = db.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if stroka is None:
        abort(404)
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return redirect(url_for("glavnaya"))


# -- API-маршрут: тот же список, но в формате JSON (раздел 22.16 сайта) -----

@app.route("/api/tasks", methods=["GET", "POST"])
def api_tasks():
    db = get_db()
    if request.method == "POST":
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("title"), str):
            return jsonify({"error": "поле title обязательно и должно быть строкой"}), 400
        title = clean_title(data["title"])
        if title is None:
            return jsonify({"error": "title не может быть пустым и не длиннее 200 символов"}), 400
        cursor = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        db.commit()
        novaya = db.execute("SELECT id, title, done FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return jsonify(task_row_to_dict(novaya)), 201

    stroki = db.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    return jsonify([task_row_to_dict(s) for s in stroki])


# -- обработчики ошибок -------------------------------------------------------

@app.errorhandler(404)
def stranica_ne_najdena(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "not found"}), 404
    return render_template("404.html"), 404


if __name__ == "__main__":
    if not Path(app.config["DATABASE"]).exists():
        with app.app_context():
            init_db()
    # debug=True запускает сервер РАЗРАБОТКИ — удобно локально, но не для
    # рабочего развёртывания (раздел 22.34 сайта).
    app.run(debug=True)
