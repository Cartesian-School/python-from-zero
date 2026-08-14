"""Мини-сайт «Список задач» на Flask.

Проект к главе 22 книги «Python с нуля» (Cartesian School).
Запуск: python app.py, затем откройте http://127.0.0.1:5000/ в браузере.
"""

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

zadachi = ["Выучить основы Python", "Собрать сайт на Flask"]


@app.route("/")
def glavnaya():
    return render_template("index.html", zadachi=zadachi)


@app.route("/privet/<imya>")
def privet(imya):
    return render_template("privet.html", imya=imya)


@app.route("/dobavit", methods=["POST"])
def dobavit():
    novaya_zadacha = request.form.get("zadacha", "").strip()
    if novaya_zadacha:
        zadachi.append(novaya_zadacha)
    return redirect(url_for("glavnaya"))


if __name__ == "__main__":
    app.run(debug=True)
