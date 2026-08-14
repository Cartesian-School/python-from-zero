#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 22 (Веб-разработка с Python / Flask).

HTML/CSS демонстрируются через IPython.display.HTML — так можно увидеть готовый
результат прямо в ноутбуке. Flask демонстрируется через встроенный `test_client()` —
он отправляет настоящие HTTP-запросы Flask-приложению без необходимости запускать
отдельный сервер, поэтому ноутбук выполняется от начала до конца без ручного участия
(тот же принцип, что и headless-тестирование Turtle/Tkinter/Pygame в предыдущих главах).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-22"


def build_html_css() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-02 · HTML и CSS вживую\n\nПрактика к разделам "
          "[«Строительные блоки — HTML»](../../site/chapters/glava-22/22-02-html.html) и "
          "[«Делаем красивее — CSS»](../../site/chapters/glava-22/22-03-css.html).")
    nb.md("## Цель\n\nУвидеть, как HTML-теги превращаются в структуру страницы, а CSS "
          "меняет её внешний вид — прямо внутри ноутбука.")
    nb.md("## Рабочий пример — HTML без стилей")
    nb.code('''from IPython.display import HTML, display

html_bez_stilej = """
<h1>Привет, мир!</h1>
<p>Это мой первый сайт на HTML.</p>
<ul>
  <li>Учу Python</li>
  <li>Учу HTML</li>
</ul>
"""

display(HTML(html_bez_stilej))
print("Длина HTML-кода:", len(html_bez_stilej), "символов")''')
    nb.md("## Проверка результата")
    nb.code('''assert "<h1>" in html_bez_stilej
assert "<li>Учу Python</li>" in html_bez_stilej
print("Верно: страница содержит заголовок и оба пункта списка.")''')
    nb.md("## Эксперимент — та же страница со стилями CSS")
    nb.code('''html_so_stilyami = """
<style>
  .demo-blok { font-family: sans-serif; background: #f7f7fb; padding: 12px; }
  .demo-blok h1 { color: #4a2fbd; }
  .demo-blok p { line-height: 1.6; }
</style>
<div class="demo-blok">
  <h1>Привет, мир!</h1>
  <p>Теперь у страницы есть цвет, фон и аккуратные отступы.</p>
</div>
"""

display(HTML(html_so_stilyami))''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте в CSS ещё одно правило — измените "
          "цвет текста внутри <li> на зелёный, — и убедитесь, что строка появилась в коде.")
    nb.code('''html_svoj_stil = """
<style>
  .demo-blok2 li { color: green; }
</style>
<div class="demo-blok2">
  <ul><li>Зелёный пункт списка</li></ul>
</div>
"""

display(HTML(html_svoj_stil))

assert "color: green" in html_svoj_stil
print("Верно: правило для зелёного текста добавлено.")''')
    nb.write(OUT_DIR / "22-02-html-css.ipynb")
    print(f"Записано: 22-02-html-css ({len(nb)} ячеек)")


def build_flask() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-05 · Flask: маршруты, шаблоны и формы\n\nПрактика к разделу "
          "[«Flask в Python»](../../site/chapters/glava-22/22-05-flask.html). "
          "Полный проект — `projects/flask/todo-app/app.py`.")
    nb.md("## Про тестовый клиент в этом ноутбуке\n\n"
          "Обычно Flask-приложение запускают командой `python app.py`, и оно ждёт запросы "
          "браузера бесконечно (`app.run()`). В автоматически выполняемом ноутбуке нет "
          "браузера и нет смысла ждать вечно, поэтому мы используем "
          "`app.test_client()` — он отправляет настоящие HTTP-запросы "
          "(GET, POST) прямо внутри Python, без сервера и без браузера. Это стандартный "
          "способ Flask тестировать приложения.")
    nb.md("## Рабочий пример — собираем маленькое приложение")
    nb.code('''from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)
zadachi = ["Выучить основы Python", "Собрать сайт на Flask"]

SHABLON_GLAVNOJ = """
<h1>Мой список задач</h1>
<ul>
{% for zadacha in zadachi %}
  <li>{{ zadacha }}</li>
{% endfor %}
</ul>
"""

SHABLON_PRIVET = "<h1>Привет, {{ imya }}!</h1>"


@app.route("/")
def glavnaya():
    return render_template_string(SHABLON_GLAVNOJ, zadachi=zadachi)


@app.route("/privet/<imya>")
def privet(imya):
    return render_template_string(SHABLON_PRIVET, imya=imya)


@app.route("/dobavit", methods=["POST"])
def dobavit():
    novaya_zadacha = request.form.get("zadacha", "").strip()
    if novaya_zadacha:
        zadachi.append(novaya_zadacha)
    return redirect(url_for("glavnaya"))


client = app.test_client()
print("Приложение и тестовый клиент готовы.")''')
    nb.md("## Эксперимент 1 — главная страница (GET /)")
    nb.code('''otvet = client.get("/")
telo = otvet.get_data(as_text=True)

print("Код ответа:", otvet.status_code)
print(telo)''')
    nb.md("## Проверка результата")
    nb.code('''assert otvet.status_code == 200
assert "Выучить основы Python" in telo
assert "Собрать сайт на Flask" in telo
print("Верно: главная страница отдаёт список задач с кодом 200.")''')
    nb.md("## Эксперимент 2 — динамический маршрут /privet/<imya>")
    nb.code('''otvet2 = client.get("/privet/Ада")
telo2 = otvet2.get_data(as_text=True)

print(telo2)
assert "Привет, Ада!" in telo2
print("Верно: значение из адреса подставилось в шаблон.")''')
    nb.md("## Эксперимент 3 — отправка формы (POST /dobavit)")
    nb.code('''kolichestvo_do = len(zadachi)

otvet3 = client.post("/dobavit", data={"zadacha": "Прочитать книгу"})
print("Код ответа:", otvet3.status_code)   # 302 — редирект на главную
print("Задач было:", kolichestvo_do, "-> стало:", len(zadachi))

assert otvet3.status_code == 302
assert len(zadachi) == kolichestvo_do + 1
assert "Прочитать книгу" in zadachi
print("Верно: POST-запрос добавил новую задачу и вернул редирект.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nОтправьте форму с пустой задачей "
          "(`{\"zadacha\": \"   \"}`) и убедитесь, что список задач не изменился — как и в "
          "настоящем `app.py`.")
    nb.code('''kolichestvo_do2 = len(zadachi)
client.post("/dobavit", data={"zadacha": "   "})

assert len(zadachi) == kolichestvo_do2
print("Верно: пустая (только пробелы) задача не была добавлена.")''')
    nb.write(OUT_DIR / "22-05-flask.ipynb")
    print(f"Записано: 22-05-flask ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_html_css()
    build_flask()
