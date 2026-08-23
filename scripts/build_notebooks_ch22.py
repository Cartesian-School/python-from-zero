#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 22 (Веб-разработка с Python / Flask).

HTML/CSS демонстрируются через IPython.display.HTML — так можно увидеть готовый
результат прямо в ноутбуке. Flask демонстрируется через встроенный `test_client()`.
Он формирует запрос внутри процесса и передаёт его приложению через тестовый
интерфейс Flask/Werkzeug — без открытия сетевого порта и без настоящего
браузера (раздел 22.33 сайта уточняет эту формулировку). Часть практик,
посвящённых SQL и SQLite, использует модуль sqlite3 стандартной
библиотеки Python — он доступен и в браузерном окружении Pyodide, начиная с
версии 314 (проверено эмпирически в этом же окружении перед добавлением
практик).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-22"


def build_html_css() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-02 · Структура HTML и стили CSS\n\nПрактика к разделам "
          "[«HTML: структура веб-страницы»](../../site/chapters/glava-22/22-02-html.html) и "
          "[«CSS: оформление и расположение элементов веб-страницы»](../../site/chapters/glava-22/22-03-css.html).")
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
          "[«Первое веб-приложение на Flask»](../../site/chapters/glava-22/22-05-flask.html). "
          "Полный проект — `projects/flask/todo-app/app.py`.")
    nb.md("## Про тестовый клиент в этом ноутбуке\n\n"
          "Обычно Flask-приложение запускают командой `python app.py`, и оно ждёт запросы "
          "браузера бесконечно (`app.run()`). В автоматически выполняемом ноутбуке нет "
          "браузера и нет смысла ждать вечно, поэтому мы используем `app.test_client()`. "
          "Он формирует запрос внутри процесса и передаёт его приложению через тестовый "
          "интерфейс Flask/Werkzeug, не открывая сетевой порт и не запуская настоящий "
          "сервер, — та же логика обработки запроса, что и в реальном приложении, но без сети "
          "(раздел 22.33 сайта разбирает это различие подробнее).")
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


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-08 · Разбор URL\n\nПрактика к разделу "
          "[«URL: домен, путь, параметры и фрагмент»](../../site/chapters/glava-22/22-08-url-anatomiya.html).")
    nb.md("## Цель\n\nРазобрать URL на части модулем urllib.parse из стандартной "
          "библиотеки Python и убедиться, что фрагмент не попадает в путь и в query.")
    nb.md("## Рабочий пример")
    nb.code('''from urllib.parse import urlparse, parse_qs

url = "https://example.com:443/products/42?sort=price&page=2#details"
razobrannyj = urlparse(url)

print("схема:", razobrannyj.scheme)
print("хост:", razobrannyj.hostname)
print("порт:", razobrannyj.port)
print("путь:", razobrannyj.path)
print("query:", razobrannyj.query)
print("фрагмент:", razobrannyj.fragment)
print("параметры:", parse_qs(razobrannyj.query))''')
    nb.md("## Проверка результата")
    nb.code('''assert razobrannyj.scheme == "https"
assert razobrannyj.hostname == "example.com"
assert razobrannyj.port == 443
assert razobrannyj.path == "/products/42"
assert razobrannyj.fragment == "details"
assert parse_qs(razobrannyj.query) == {"sort": ["price"], "page": ["2"]}
print("Верно: URL разобран по частям, фрагмент отдельно от query.")''')
    nb.md("## Задание ★ Базовая практика\n\nРазберите адрес "
          "`http://localhost:5000/api/tasks?done=0` и проверьте, что путь равен "
          "`/api/tasks`, а параметр `done` равен `[\"0\"]`.")
    nb.code('''url2 = "http://localhost:5000/api/tasks?done=0"
razobrannyj2 = urlparse(url2)
parametry2 = parse_qs(razobrannyj2.query)

assert razobrannyj2.path == "/api/tasks"
assert parametry2["done"] == ["0"]
print("Верно: путь и параметр разобраны правильно.")''')
    nb.write(OUT_DIR / "22-08-url.ipynb")
    print(f"Записано: 22-08-url ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-09 · Коды состояния HTTP\n\nПрактика к разделу "
          "[«HTTP: запросы, ответы, методы и коды состояния»](../../site/chapters/glava-22/22-09-http.html).")
    nb.md("## Цель\n\nНаписать функцию, которая классифицирует код состояния HTTP по "
          "диапазону — 2xx, 3xx, 4xx, 5xx.")
    nb.md("## Рабочий пример")
    nb.code('''def gruppa_koda(kod):
    if 200 <= kod < 300:
        return "успех"
    if 300 <= kod < 400:
        return "перенаправление"
    if 400 <= kod < 500:
        return "ошибка клиента"
    if 500 <= kod < 600:
        return "ошибка сервера"
    return "неизвестный диапазон"


for kod in (200, 201, 302, 400, 404, 500):
    print(kod, "->", gruppa_koda(kod))''')
    nb.md("## Проверка результата")
    nb.code('''assert gruppa_koda(200) == "успех"
assert gruppa_koda(201) == "успех"
assert gruppa_koda(303) == "перенаправление"
assert gruppa_koda(404) == "ошибка клиента"
assert gruppa_koda(500) == "ошибка сервера"
print("Верно: код состояния классифицируется по диапазону.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nНапишите функцию "
          "`eto_uspeh(kod)`, которая возвращает True только для кодов 2xx.")
    nb.code('''def eto_uspeh(kod):
    return 200 <= kod < 300


assert eto_uspeh(200) is True
assert eto_uspeh(201) is True
assert eto_uspeh(404) is False
assert eto_uspeh(302) is False
print("Верно: eto_uspeh() отличает 2xx от остальных диапазонов.")''')
    nb.write(OUT_DIR / "22-09-http-kody.ipynb")
    print(f"Записано: 22-09-http-kody ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-11 · Маршруты и параметры пути\n\nПрактика к разделу "
          "[«Маршрутизация во Flask: URL и функции-обработчики»](../../site/chapters/glava-22/22-11-flask-marshrutizaciya.html).")
    nb.md("## Цель\n\nУбедиться, что типизированный параметр пути `<int:...>` принимает "
          "число и отклоняет нечисловой адрес кодом 404.")
    nb.md("## Рабочий пример")
    nb.code('''from flask import Flask

app = Flask(__name__)


@app.route("/task/<int:task_id>")
def poluchit_zadachu(task_id):
    return f"Задача №{task_id}", 200


client = app.test_client()

otvet_chislo = client.get("/task/42")
otvet_tekst = client.get("/task/abc")

print("Число:", otvet_chislo.status_code, otvet_chislo.get_data(as_text=True))
print("Не число:", otvet_tekst.status_code)''')
    nb.md("## Проверка результата")
    nb.code('''assert otvet_chislo.status_code == 200
assert "Задача №42" in otvet_chislo.get_data(as_text=True)
assert otvet_tekst.status_code == 404
print("Верно: <int:task_id> принимает число и отклоняет нечисловой адрес.")''')
    nb.write(OUT_DIR / "22-11-flask-marshruty.ipynb")
    print(f"Записано: 22-11-flask-marshruty ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-12 · Автоэкранирование Jinja\n\nПрактика к разделу "
          "[«Jinja: шаблоны HTML с данными»](../../site/chapters/glava-22/22-12-jinja-shablony.html).")
    nb.md("## Цель\n\nУбедиться, что Jinja экранирует потенциально опасный текст по "
          "умолчанию, и увидеть, что делает фильтр |safe.")
    nb.md("## Рабочий пример")
    nb.code('''from flask import Flask, render_template_string

app = Flask(__name__)

opasnyj_tekst = "<script>alert(1)</script>"

SHABLON = "<p>{{ tekst }}</p>"
SHABLON_SAFE = "<p>{{ tekst|safe }}</p>"


@app.route("/bez-safe")
def bez_safe():
    return render_template_string(SHABLON, tekst=opasnyj_tekst)


@app.route("/s-safe")
def s_safe():
    return render_template_string(SHABLON_SAFE, tekst=opasnyj_tekst)


# Оба маршрута зарегистрированы до первого запроса — Flask больше не
# позволяет добавлять маршруты после того, как приложение уже ответило
# на первый запрос.
client = app.test_client()

otvet = client.get("/bez-safe")
telo = otvet.get_data(as_text=True)
print(telo)''')
    nb.md("## Проверка результата")
    nb.code('''assert "<script>alert(1)</script>" not in telo
assert "&lt;script&gt;" in telo
print("Верно: Jinja экранировала тег script — он показан как текст, а не выполнен.")''')
    nb.md("## Эксперимент — с |safe разметка проходит как есть")
    nb.code('''otvet2 = client.get("/s-safe")
telo2 = otvet2.get_data(as_text=True)

assert "<script>alert(1)</script>" in telo2
print("Так и есть: |safe отключает экранирование — поэтому его нельзя применять к вводу, который вы не контролируете.")''')
    nb.write(OUT_DIR / "22-12-jinja-avtoekranirovanie.ipynb")
    print(f"Записано: 22-12-jinja-avtoekranirovanie ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-13 · POST-Redirect-GET\n\nПрактика к разделу "
          "[«HTML-формы и отправка данных на сервер»](../../site/chapters/glava-22/22-13-formy.html).")
    nb.md("## Цель\n\nУбедиться, что обработчик формы отвечает редиректом (код 303 See Other), "
          "а не сразу готовой страницей.")
    nb.md("## Рабочий пример")
    nb.code('''from flask import Flask, redirect, request, url_for

app = Flask(__name__)
zapisi = []


@app.route("/")
def glavnaya():
    return f"Записей: {len(zapisi)}"


@app.route("/dobavit", methods=["POST"])
def dobavit():
    tekst = request.form.get("tekst", "").strip()
    if tekst:
        zapisi.append(tekst)
    # code=303 (See Other) точнее, чем редирект Flask по умолчанию (302
    # Found), описывает POST-Redirect-GET: результат смотрите по другому
    # адресу через GET.
    return redirect(url_for("glavnaya"), code=303)


client = app.test_client()
otvet = client.post("/dobavit", data={"tekst": "Первая запись"})

print("Код ответа:", otvet.status_code)
print("Заголовок Location:", otvet.headers.get("Location"))''')
    nb.md("## Проверка результата")
    nb.code('''assert otvet.status_code == 303
assert otvet.headers.get("Location") is not None
assert zapisi == ["Первая запись"]
print("Верно: POST ответил редиректом 303, а не HTML-страницей напрямую.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПройдите по редиректу вручную: "
          "выполните GET на адрес из заголовка Location и убедитесь, что он показывает "
          "актуальное количество записей.")
    nb.code('''otvet_posle_redirecta = client.get(otvet.headers["Location"])
telo = otvet_posle_redirecta.get_data(as_text=True)

assert "Записей: 1" in telo
print("Верно: страница после редиректа показывает уже обновлённые данные.")''')
    nb.write(OUT_DIR / "22-13-post-redirect-get.ipynb")
    print(f"Записано: 22-13-post-redirect-get ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-15 · Преобразование данных между Python и JSON\n\nПрактика к разделу "
          "[«JSON: формат обмена данными»](../../site/chapters/glava-22/22-15-json.html).")
    nb.md("## Цель\n\nПревратить словарь Python в текст JSON и обратно, и увидеть разницу "
          "между распечаткой словаря Python и корректным JSON.")
    nb.md("## Рабочий пример")
    nb.code('''import json

zadacha = {"title": "Купить хлеб", "done": False}

tekst_json = json.dumps(zadacha, ensure_ascii=False)
print("JSON:", tekst_json)
print("Словарь Python:", zadacha)

obratno = json.loads(tekst_json)
print("Снова словарь после loads():", obratno)''')
    nb.md("## Проверка результата")
    nb.code('''assert tekst_json == \'{"title": "Купить хлеб", "done": false}\'
assert '\\'' not in tekst_json, "в корректном JSON строки — только в двойных кавычках"
assert obratno == zadacha
print("Верно: json.dumps() дал валидный JSON, json.loads() восстановил тот же словарь.")''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что список из двух задач "
          "превращается в JSON-массив объектов, а не в распечатку списка Python.")
    nb.code('''zadachi = [{"title": "A", "done": True}, {"title": "B", "done": False}]
tekst_spiska = json.dumps(zadachi, ensure_ascii=False)

assert tekst_spiska == '[{"title": "A", "done": true}, {"title": "B", "done": false}]'
print("Верно:", tekst_spiska)''')
    nb.write(OUT_DIR / "22-15-json.ipynb")
    print(f"Записано: 22-15-json ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-16 · Формируем API-ответ\n\nПрактика к разделу "
          "[«HTTP API: обмен данными между программами»](../../site/chapters/glava-22/22-16-api.html).")
    nb.md("## Цель\n\nНаписать чистую функцию, которая превращает внутреннее "
          "представление задачи в словарь, готовый для API-ответа — без Flask, "
          "чистой логикой.")
    nb.md("## Рабочий пример")
    nb.code('''def zadacha_dlya_api(id_, title, done):
    return {"id": id_, "title": title, "done": bool(done)}


zapis_iz_bazy = (1, "Купить хлеб", 0)   # так вернёт sqlite3.Row/tuple
otvet = zadacha_dlya_api(*zapis_iz_bazy)
print(otvet)''')
    nb.md("## Проверка результата")
    nb.code('''assert otvet == {"id": 1, "title": "Купить хлеб", "done": False}
assert otvet["done"] is False   # bool, а не 0 — так короче JSON-ответ
print("Верно: числовой флаг из базы превращён в настоящий bool для API-ответа.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nНапишите функцию "
          "`spisok_dlya_api(zapisi)`, которая применяет `zadacha_dlya_api()` "
          "к списку кортежей и возвращает список словарей.")
    nb.code('''def spisok_dlya_api(zapisi):
    return [zadacha_dlya_api(*z) for z in zapisi]


rezultat = spisok_dlya_api([(1, "A", 1), (2, "B", 0)])
assert rezultat == [{"id": 1, "title": "A", "done": True}, {"id": 2, "title": "B", "done": False}]
print("Верно:", rezultat)''')
    nb.write(OUT_DIR / "22-16-api-otvet.ipynb")
    print(f"Записано: 22-16-api-otvet ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-18 · Выбор фреймворка по задаче\n\nПрактика к разделу "
          "[«Сравнение Flask, Django и FastAPI»](../../site/chapters/glava-22/22-18-flask-django-fastapi.html).")
    nb.md("## Цель\n\nСвязать описание задачи с наиболее подходящим стартовым выбором "
          "фреймворка — на основе таблицы сравнения с сайта, а не личных предпочтений.")
    nb.md("## Рабочий пример")
    nb.code('''vybor = {
    "sajt_s_admin_panelyu": "Django",
    "api_s_avtomaticheskoj_dokumentaciej": "FastAPI",
    "prostoj_sajt_bez_gotovoj_adminki": "Flask",
}

for zadacha, frejmvork in vybor.items():
    print(zadacha, "->", frejmvork)''')
    nb.md("## Проверка результата")
    nb.code('''assert vybor["sajt_s_admin_panelyu"] == "Django"
assert vybor["api_s_avtomaticheskoj_dokumentaciej"] == "FastAPI"
assert vybor["prostoj_sajt_bez_gotovoj_adminki"] == "Flask"
print("Верно: выбор соответствует таблице сравнения на сайте.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте в словарь `vybor` ключ "
          "`nizkourovnevyj_kontrol_nad_asgi` со значением `\"Starlette\"`.")
    nb.code('''vybor["nizkourovnevyj_kontrol_nad_asgi"] = "Starlette"

assert vybor["nizkourovnevyj_kontrol_nad_asgi"] == "Starlette"
print("Верно:", vybor["nizkourovnevyj_kontrol_nad_asgi"])''')
    nb.write(OUT_DIR / "22-18-vybor-frejmvorka.ipynb")
    print(f"Записано: 22-18-vybor-frejmvorka ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-19 · WSGI или ASGI?\n\nПрактика к разделу "
          "[«WSGI и ASGI: связь веб-приложения с сервером»](../../site/chapters/glava-22/22-19-wsgi-asgi.html).")
    nb.md("## Цель\n\nОтнести фреймворк или сервер приложений к WSGI или ASGI по "
          "таблице сравнения с сайта.")
    nb.md("## Рабочий пример")
    nb.code('''protokol = {
    "Flask": "WSGI",
    "Starlette": "ASGI",
    "FastAPI": "ASGI",
    "Gunicorn": "WSGI",
    "Uvicorn": "ASGI",
}

for imya, tip in protokol.items():
    print(imya, "->", tip)''')
    nb.md("## Проверка результата")
    nb.code('''assert protokol["Flask"] == "WSGI"
assert protokol["FastAPI"] == "ASGI"
assert protokol["Uvicorn"] == "ASGI"
assert protokol["Gunicorn"] == "WSGI"
print("Верно: сопоставление совпадает с разделом 22.19 сайта.")''')
    nb.write(OUT_DIR / "22-19-wsgi-asgi.ipynb")
    print(f"Записано: 22-19-wsgi-asgi ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-22 · CRUD на SQLite\n\nПрактика к разделу "
          "[«SQL: создаём, читаем и изменяем данные»](../../site/chapters/glava-22/22-22-sql.html).")
    nb.md("## Цель\n\nВыполнить все четыре операции CRUD настоящими SQL-запросами через "
          "модуль sqlite3 — прямо в этом ноутбуке, без установки чего-либо дополнительно.")
    nb.md("## Рабочий пример")
    nb.code('''import sqlite3

baza = sqlite3.connect(":memory:")
baza.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")

baza.execute("INSERT INTO tasks (title) VALUES (?)", ("Купить хлеб",))
baza.execute("INSERT INTO tasks (title) VALUES (?)", ("Выучить SQL",))
baza.commit()

stroki = baza.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
print(stroki)''')
    nb.md("## Проверка результата")
    nb.code('''assert len(stroki) == 2
assert stroki[0][1] == "Купить хлеб"
assert stroki[1][1] == "Выучить SQL"
assert stroki[0][2] == 0
print("Верно: обе задачи добавлены (Create) и прочитаны (Read).")''')
    nb.md("## Эксперимент — Update и Delete")
    nb.code('''baza.execute("UPDATE tasks SET done = 1 WHERE title = ?", ("Купить хлеб",))
baza.execute("DELETE FROM tasks WHERE title = ?", ("Выучить SQL",))
baza.commit()

posle = baza.execute("SELECT id, title, done FROM tasks").fetchall()
print(posle)

assert len(posle) == 1
assert posle[0][1] == "Купить хлеб"
assert posle[0][2] == 1
print("Верно: Update изменил done, Delete убрал вторую задачу.")''')
    nb.write(OUT_DIR / "22-22-sql-crud.ipynb")
    print(f"Записано: 22-22-sql-crud ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-23 · Подключение к SQLite через sqlite3\n\nПрактика к разделу "
          "[«SQLite: встраиваемая реляционная СУБД»](../../site/chapters/glava-22/22-23-sqlite.html).")
    nb.md("## Цель\n\nИспользовать row_factory для обращения к столбцам по имени и "
          "убедиться, что sqlite3.Row ведёт себя как строка результата.")
    nb.md("## Рабочий пример")
    nb.code('''import sqlite3

baza = sqlite3.connect(":memory:")
baza.row_factory = sqlite3.Row
baza.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
baza.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Полить цветы", 1))
baza.commit()

stroka = baza.execute("SELECT id, title, done FROM tasks").fetchone()
print("По имени:", stroka["title"], stroka["done"])
print("По индексу:", stroka[0], stroka[1])''')
    nb.md("## Проверка результата")
    nb.code('''assert stroka["title"] == "Полить цветы"
assert stroka["done"] == 1
assert stroka[1] == stroka["title"]
print("Верно: sqlite3.Row доступен и по имени столбца, и по числовому индексу.")''')
    nb.write(OUT_DIR / "22-23-sqlite-podklyuchenie.ipynb")
    print(f"Записано: 22-23-sqlite-podklyuchenie ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-26 · SQL и его отображение в ORM\n\nПрактика к разделу "
          "[«ORM: работа с базой данных через объекты Python»](../../site/chapters/glava-22/22-26-orm.html).")
    nb.md("## Цель\n\nПроверить, что запрос через игрушечный ORM-объект и прямой SQL-запрос "
          "дают одинаковый результат — на маленьком, полностью реальном примере sqlite3.")
    nb.md("## Рабочий пример")
    nb.code('''import sqlite3

baza = sqlite3.connect(":memory:")
baza.row_factory = sqlite3.Row
baza.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
baza.executemany(
    "INSERT INTO tasks (title, done) VALUES (?, ?)",
    [("A", 0), ("B", 1), ("C", 0)],
)
baza.commit()


class ProstoyORM:
    """Игрушечная имитация одного метода ORM: формирует и выполняет обычный SQL."""

    def __init__(self, soedinenie):
        self.soedinenie = soedinenie

    def nevypolnennye(self):
        return self.soedinenie.execute(
            "SELECT id, title, done FROM tasks WHERE done = 0 ORDER BY id"
        ).fetchall()


orm = ProstoyORM(baza)
cherez_orm = orm.nevypolnennye()
cherez_sql = baza.execute("SELECT id, title, done FROM tasks WHERE done = 0 ORDER BY id").fetchall()

print([dict(s) for s in cherez_orm])''')
    nb.md("## Проверка результата")
    nb.code('''assert [dict(s) for s in cherez_orm] == [dict(s) for s in cherez_sql]
assert [s["title"] for s in cherez_orm] == ["A", "C"]
print("Верно: ORM-обёртка и прямой SQL-запрос вернули одинаковый результат — ORM формирует тот же SQL.")''')
    nb.write(OUT_DIR / "22-26-orm.ipynb")
    print(f"Записано: 22-26-orm ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-27 · Миграция схемы\n\nПрактика к разделу "
          "[«Миграции схемы базы данных»](../../site/chapters/glava-22/22-27-migracii-shemy.html).")
    nb.md("## Цель\n\nДобавить столбец в уже существующую таблицу через ALTER TABLE и "
          "убедиться, что старые строки не потерялись.")
    nb.md("## Рабочий пример — версия 1 схемы")
    nb.code('''import sqlite3

baza = sqlite3.connect(":memory:")
baza.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
baza.execute("INSERT INTO tasks (title) VALUES (?)", ("Задача из версии 1",))
baza.commit()

do_migracii = baza.execute("SELECT * FROM tasks").fetchall()
print("До миграции:", do_migracii)''')
    nb.md("## Эксперимент — миграция до версии 2")
    nb.code('''baza.execute("ALTER TABLE tasks ADD COLUMN done INTEGER NOT NULL DEFAULT 0")
baza.commit()

posle_migracii = baza.execute("SELECT id, title, done FROM tasks").fetchall()
print("После миграции:", posle_migracii)''')
    nb.md("## Проверка результата")
    nb.code('''assert len(posle_migracii) == 1, "старая строка должна была сохраниться"
assert posle_migracii[0][1] == "Задача из версии 1"
assert posle_migracii[0][2] == 0, "новый столбец должен получить значение по умолчанию"
print("Верно: структура изменилась, старые данные остались на месте.")''')
    nb.write(OUT_DIR / "22-27-migraciya-shemy.ipynb")
    print(f"Записано: 22-27-migraciya-shemy ({len(nb)} ячеек)")


def build_28() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-28 · Перенос данных через JSON\n\nПрактика к разделу "
          "[«Перенос данных между базами»](../../site/chapters/glava-22/22-28-perenos-dannyh.html).")
    nb.md("## Цель\n\nПеренести три строки из одной базы SQLite в другую через JSON как "
          "промежуточный формат — и проверить, что количество и содержимое совпали.")
    nb.md("## Рабочий пример — исходная база")
    nb.code('''import json
import sqlite3

istochnik = sqlite3.connect(":memory:")
istochnik.row_factory = sqlite3.Row
istochnik.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
istochnik.executemany(
    "INSERT INTO tasks (title, done) VALUES (?, ?)",
    [("Купить хлеб", 0), ("Выучить SQL", 1), ("Собрать сайт", 0)],
)
istochnik.commit()

stroki = istochnik.execute("SELECT title, done FROM tasks ORDER BY id").fetchall()
dannye = [dict(stroka) for stroka in stroki]
tekst_json = json.dumps(dannye, ensure_ascii=False)
print(tekst_json)''')
    nb.md("## Эксперимент — импорт в новую базу")
    nb.code('''zagruzhennye = json.loads(tekst_json)

cel = sqlite3.connect(":memory:")
cel.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
for zapis in zagruzhennye:
    cel.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (zapis["title"], zapis["done"]))
cel.commit()

itog = cel.execute("SELECT title, done FROM tasks ORDER BY id").fetchall()
print(itog)''')
    nb.md("## Проверка результата")
    nb.code('''iskhodnye_nazvaniya = [s["title"] for s in stroki]
itogovye_nazvaniya = [s[0] for s in itog]

assert len(itog) == len(stroki) == 3
assert itogovye_nazvaniya == iskhodnye_nazvaniya
assert [s[1] for s in itog] == [s["done"] for s in stroki]
print("Верно: количество строк и их содержимое совпадают после переноса через JSON.")''')
    nb.md("## Важная деталь\n\nНовые идентификаторы `id` в целевой базе назначаются "
          "заново — при вставке они не передавались явно. Это осознанный выбор для "
          "такого простого случая: если бы исходные `id` были важны (например, на них "
          "кто-то уже ссылается), их нужно было бы переносить явно и после этого "
          "проверить, что они остались уникальными.")
    nb.write(OUT_DIR / "22-28-perenos-cherez-json.ipynb")
    print(f"Записано: 22-28-perenos-cherez-json ({len(nb)} ячеек)")


def build_29() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-29 · Flask поверх SQLite\n\nПрактика к разделу "
          "[«Flask и SQLite: сохраняем данные в базе»](../../site/chapters/glava-22/22-29-flask-sqlite.html). "
          "Полный проект — `projects/flask/todo-app/app.py`.")
    nb.md("## Цель\n\nСобрать маленькое Flask-приложение поверх базы SQLite и "
          "убедиться, что данные переживают создание нового объекта приложения — то есть "
          "ведут себя так же, как после перезапуска процесса.")
    nb.md("## Рабочий пример")
    nb.code('''import sqlite3
import tempfile
import os

from flask import Flask, g, jsonify, redirect, request, url_for

put_k_baze = os.path.join(tempfile.mkdtemp(), "zadachi.db")


def sozdat_prilozhenie():
    prilozhenie = Flask(__name__)
    prilozhenie.config["DATABASE"] = put_k_baze

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(prilozhenie.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @prilozhenie.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @prilozhenie.route("/api/tasks", methods=["GET", "POST"])
    def api_tasks():
        db = get_db()
        if request.method == "POST":
            db.execute("INSERT INTO tasks (title) VALUES (?)", (request.get_json()["title"],))
            db.commit()
            return "", 201
        stroki = db.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
        return jsonify([dict(s) for s in stroki])

    with prilozhenie.app_context():
        get_db().execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
        get_db().commit()

    return prilozhenie


prilozhenie1 = sozdat_prilozhenie()
client1 = prilozhenie1.test_client()
client1.post("/api/tasks", json={"title": "Задача до перезапуска"})

otvet1 = client1.get("/api/tasks")
print("До «перезапуска»:", otvet1.get_json())''')
    nb.md("## Проверка результата — новый объект приложения видит те же данные")
    nb.code('''prilozhenie2 = sozdat_prilozhenie()   # как будто процесс перезапустили
client2 = prilozhenie2.test_client()

otvet2 = client2.get("/api/tasks")
print("После «перезапуска»:", otvet2.get_json())

assert otvet2.get_json() == otvet1.get_json()
assert len(otvet2.get_json()) == 1
print("Верно: данные хранятся в файле базы данных, а не в памяти процесса — новый объект приложения видит их.")''')
    nb.write(OUT_DIR / "22-29-flask-sqlite.ipynb")
    print(f"Записано: 22-29-flask-sqlite ({len(nb)} ячеек)")


def build_30() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-30 · flash() и session\n\nПрактика к разделу "
          "[«Cookie и сессии: состояние между HTTP-запросами»](../../site/chapters/glava-22/22-30-cookies-session.html).")
    nb.md("## Цель\n\nУвидеть, что flash()-сообщение появляется на следующей странице "
          "ровно один раз, а затем исчезает.")
    nb.md("## Рабочий пример")
    nb.code('''from flask import Flask, flash, get_flashed_messages, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-secret-do-not-use-in-production"


@app.route("/deystvie")
def deystvie():
    flash("Что-то произошло!")
    return redirect(url_for("stranica"))


@app.route("/stranica")
def stranica():
    soobshcheniya = get_flashed_messages()
    return f"Сообщений: {len(soobshcheniya)}; {soobshcheniya}"


client = app.test_client()
client.get("/deystvie")
otvet1 = client.get("/stranica")
otvet2 = client.get("/stranica")

print("Первый визит:", otvet1.get_data(as_text=True))
print("Второй визит:", otvet2.get_data(as_text=True))''')
    nb.md("## Проверка результата")
    nb.code('''assert "Что-то произошло!" in otvet1.get_data(as_text=True)
assert "Сообщений: 0" in otvet2.get_data(as_text=True)
print("Верно: flash-сообщение показано один раз и не появляется на следующем запросе снова.")''')
    nb.write(OUT_DIR / "22-30-flash-session.ipynb")
    print(f"Записано: 22-30-flash-session ({len(nb)} ячеек)")


def build_31() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-31 · Проверяем ввод\n\nПрактика к разделу "
          "[«Проверка входных данных и обработка ошибок»](../../site/chapters/glava-22/22-31-validaciya-oshibki.html).")
    nb.md("## Цель\n\nПроверить ту же функцию clean_title(), которая используется в "
          "настоящем проекте (projects/flask/todo-app/app.py), на нескольких "
          "граничных случаях.")
    nb.md("## Рабочий пример")
    nb.code('''MAX_TITLE_LENGTH = 200


def clean_title(raw_title):
    title = raw_title.strip()
    if not title or len(title) > MAX_TITLE_LENGTH:
        return None
    return title


print(clean_title("Купить хлеб"))
print(clean_title("   "))
print(clean_title("а" * 201))''')
    nb.md("## Проверка результата")
    nb.code('''assert clean_title("Купить хлеб") == "Купить хлеб"
assert clean_title("  Пробелы по краям  ") == "Пробелы по краям"
assert clean_title("") is None
assert clean_title("   ") is None
assert clean_title("а" * 200) == "а" * 200
assert clean_title("а" * 201) is None
print("Верно: пустой, состоящий из пробелов и слишком длинный ввод отклоняются.")''')
    nb.write(OUT_DIR / "22-31-validaciya.ipynb")
    print(f"Записано: 22-31-validaciya ({len(nb)} ячеек)")


def build_32() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-32 · Параметризация против инъекции\n\nПрактика к разделу "
          "[«Основы безопасности веб-приложений»](../../site/chapters/glava-22/22-32-bezopasnost.html).")
    nb.md("## Цель\n\nНа настоящем sqlite3 сравнить опасную сборку запроса через "
          "f-строку с безопасным параметризованным запросом — и увидеть, к чему "
          "приводит SQL-инъекция, если её не остановить.")
    nb.md("## Рабочий пример — уязвимый вариант")
    nb.code('''import sqlite3

baza = sqlite3.connect(":memory:")
baza.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
baza.execute("INSERT INTO tasks (title) VALUES ('Обычная задача')")
baza.commit()

vvod_polzovatelya = "x'; DROP TABLE tasks; --"

# ТАК ДЕЛАТЬ НЕЛЬЗЯ — показано специально, чтобы увидеть последствия:
try:
    baza.executescript(f"SELECT * FROM tasks WHERE title = '{vvod_polzovatelya}'")
except sqlite3.Error as oshibka:
    print("sqlite3 сообщил об ошибке:", oshibka)

tablicy_posle = baza.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Таблицы после уязвимого запроса:", tablicy_posle)''')
    nb.md("## Проверка результата — таблица пострадала")
    nb.code('''nazvaniya_tablic = [t[0] for t in tablicy_posle]
assert "tasks" not in nazvaniya_tablic, "уязвимый вариант удалил таблицу — именно поэтому f-строки в SQL опасны"
print("Так и есть: таблица tasks исчезла — вставленный текст выполнился как часть SQL-команды.")''')
    nb.md("## Эксперимент — параметризованный запрос безопасен")
    nb.code('''baza2 = sqlite3.connect(":memory:")
baza2.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
baza2.execute("INSERT INTO tasks (title) VALUES ('Обычная задача')")
baza2.commit()

vvod_kak_dannye = "x'; DROP TABLE tasks; --"
rezultat = baza2.execute("SELECT * FROM tasks WHERE title = ?", (vvod_kak_dannye,)).fetchall()

tablicy_posle2 = baza2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Найдено строк:", rezultat)
print("Таблицы:", tablicy_posle2)

assert [t[0] for t in tablicy_posle2] == ["tasks"]
print("Верно: параметризованный запрос обработал вредоносный текст как обычное значение — таблица цела.")''')
    nb.write(OUT_DIR / "22-32-sql-inekciya.ipynb")
    print(f"Записано: 22-32-sql-inekciya ({len(nb)} ячеек)")


def build_33() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-33 · Тесты для Flask\n\nПрактика к разделу "
          "[«Автоматическое тестирование Flask-приложения»](../../site/chapters/glava-22/22-33-testiruem-flask.html).")
    nb.md("## Про тестовый клиент\n\n`app.test_client()` формирует запрос внутри "
          "процесса и передаёт его приложению через тестовый интерфейс Flask/Werkzeug — "
          "без открытия сетевого порта и без настоящего браузера.")
    nb.md("## Рабочий пример — маленькое приложение и три проверки")
    nb.code('''from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok"})


@app.route("/net-takogo-adresa-tut-net")
def zavedomo_otsutstvuet():
    pass


client = app.test_client()

otvet_ping = client.get("/api/ping")
otvet_404 = client.get("/adres-kotorogo-net")

print(otvet_ping.status_code, otvet_ping.get_json())
print(otvet_404.status_code)''')
    nb.md("## Проверка результата")
    nb.code('''assert otvet_ping.status_code == 200
assert otvet_ping.content_type == "application/json"
assert otvet_ping.get_json() == {"status": "ok"}
assert otvet_404.status_code == 404
print("Верно: успешный JSON-ответ и код 404 для несуществующего адреса проверены тестовым клиентом.")''')
    nb.write(OUT_DIR / "22-33-testy-flask.ipynb")
    print(f"Записано: 22-33-testy-flask ({len(nb)} ячеек)")


def build_35() -> None:
    nb = NotebookBuilder()
    nb.md("# 22-35 · Приёмочная проверка итогового проекта\n\nПрактика к разделу "
          "[«Итоговый проект: список задач на Flask и SQLite»](../../site/chapters/glava-22/22-35-itogovyj-proekt.html). "
          "Использует настоящий `projects/flask/todo-app/app.py`.")
    nb.md("## Цель\n\nПройти по итоговому проекту от начала до конца: добавить задачу, "
          "отметить её выполненной, проверить API и persistence — на реальном "
          "приложении, во временной базе данных.")
    nb.md("## Рабочий пример")
    nb.code('''import sys
import tempfile
import os

sys.path.insert(0, "../../projects/flask/todo-app")

os.environ["TODO_APP_DB"] = os.path.join(tempfile.mkdtemp(), "itogovyj_test.db")

import app as todo_app

with todo_app.app.app_context():
    todo_app.init_db()

client = todo_app.app.test_client()

otvet_pustoj = client.get("/")
print("Пустой список:", "Задач пока нет" in otvet_pustoj.get_data(as_text=True))

client.post("/dobavit", data={"zadacha": "Проверить итоговый проект"}, follow_redirects=True)
otvet_api = client.get("/api/tasks")
zadachi = otvet_api.get_json()
print("После добавления:", zadachi)''')
    nb.md("## Проверка результата")
    nb.code('''assert "Задач пока нет" in otvet_pustoj.get_data(as_text=True)
assert len(zadachi) == 1
assert zadachi[0]["title"] == "Проверить итоговый проект"
assert zadachi[0]["done"] is False
print("Верно: задача добавлена и видна через HTML-страницу и через JSON API.")''')
    nb.md("## Эксперимент — отметка выполнения и persistence")
    nb.code('''task_id = zadachi[0]["id"]
client.post(f"/vypolnit/{task_id}", follow_redirects=True)

otvet_posle = client.get("/api/tasks").get_json()
assert otvet_posle[0]["done"] is True
print("Верно: задача отмечена выполненной.")

# "перезапуск": создаём новый объект приложения на том же файле базы данных
del sys.modules["app"]
import app as todo_app2

client2 = todo_app2.app.test_client()
otvet_posle_perezapuska = client2.get("/api/tasks").get_json()

assert len(otvet_posle_perezapuska) == 1
assert otvet_posle_perezapuska[0]["done"] is True
print("Верно: данные пережили создание нового объекта приложения — то есть ведут себя так же, как после перезапуска процесса.")''')
    nb.write(OUT_DIR / "22-35-priyomochnaya-proverka.ipynb")
    print(f"Записано: 22-35-priyomochnaya-proverka ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_html_css()
    build_flask()
    build_08()
    build_09()
    build_11()
    build_12()
    build_13()
    build_15()
    build_16()
    build_18()
    build_19()
    build_22()
    build_23()
    build_26()
    build_27()
    build_28()
    build_29()
    build_30()
    build_31()
    build_32()
    build_33()
    build_35()
