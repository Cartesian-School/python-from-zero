#!/usr/bin/env python3
"""Строит Главу 22: «Веб-разработка с Python» (site/chapters/glava-22/)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    code_block,
    exercise,
    flow_diagram,
    local_required_card,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-22"

PAGES = [
    ("index.html", "Обзор главы"),
    ("22-01-python-i-veb.html", "Python и веб-разработка"),
    ("22-02-html.html", "Строительные блоки — HTML"),
    ("22-03-css.html", "Делаем красивее — CSS"),
    ("22-04-javascript.html", "Динамический фронтенд — JavaScript"),
    ("22-05-flask.html", "Flask в Python"),
    ("22-06-itogi.html", "Итоги"),
]

NOTEBOOKS = [
    "22-02-html-css.ipynb",
    "22-05-flask.ipynb",
]

LESSON_IDS = ["22-02", "22-05"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 22 · Веб-разработка", items),
        SidebarGroup(
            "Практика",
            [NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS],
        ),
        SidebarGroup("Исходный код", [NavItem("🐍 projects/flask/todo-app/", "../../../projects/flask/todo-app/app.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=22,
        baseline_page=497,
        title="Веб-разработка с Python",
        description="Как устроен веб, из чего состоит сайт и как Python с помощью Flask превращается в сервер.",
        meta_items=["⏱ ~2 часа", "🌐 HTML, CSS, JS и Flask", "📓 2 ноутбука практики"],
        sections=[
            ChapterSectionLink("22.1", "Python и веб-разработка", "22-01-python-i-veb.html", "497"),
            ChapterSectionLink("22.2", "Строительные блоки — HTML", "22-02-html.html", "499"),
            ChapterSectionLink("22.3", "Делаем красивее — CSS", "22-03-css.html", "502"),
            ChapterSectionLink("22.4", "Динамический фронтенд — JavaScript", "22-04-javascript.html", "504"),
            ChapterSectionLink("22.5", "Flask в Python", "22-05-flask.html", "507"),
            ChapterSectionLink("22.6", "Итоги", "22-06-itogi.html", "510"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Python и веб-разработка</h2>
    <p>Каждый раз, когда вы открываете сайт в браузере, происходит короткий диалог между
    двумя программами: браузером (<strong>клиентом</strong>) и другой программой, которая
    отвечает на его запросы (<strong>сервером</strong>). Браузер спрашивает — сервер
    отвечает:</p>

    {flow_diagram([
        ("Браузер", "отправляет запрос"),
        ("Интернет", "передаёт данные"),
        ("Сервер", "готовит ответ"),
        ("Браузер", "показывает страницу"),
    ], caption="Путь запроса от браузера до сервера и обратно")}

    <p>Этот диалог называется <strong>HTTP</strong> (HyperText Transfer Protocol — протокол
    передачи гипертекста). Браузер отправляет HTTP-запрос («дай мне главную страницу»),
    сервер отправляет HTTP-ответ (обычно — HTML-страницу).</p>

    {callout(
        "info",
        "Фронтенд и бэкенд",
        "То, что видит и с чем взаимодействует пользователь в браузере — HTML, CSS, "
        "JavaScript — называют <strong>фронтендом</strong> (front — «перед»). Программа, "
        "которая работает на сервере и готовит ответы — <strong>бэкенд</strong> (back — "
        "«зад», «тыл»). Python на сайтах почти всегда работает именно как бэкенд.",
    )}

    <p>В этой главе мы кратко познакомимся со всеми тремя языками фронтенда — HTML, CSS и
    JavaScript, — а затем напишем свой первый бэкенд на Python с помощью библиотеки
    <strong>Flask</strong>.</p>
    """
    out = render_page(
        page_title="Python и веб-разработка",
        description="Как браузер и сервер обмениваются данными через HTTP, и что такое фронтенд и бэкенд.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Python и веб-разработка", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Python и веб-разработка",
        lede="Каждый сайт — это диалог между браузером и сервером. Разберёмся, как он устроен.",
        body_html=body,
        sidebar_groups=sidebar("22-01-python-i-veb.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="22-02-html.html", next_label="Строительные блоки — HTML"),
    )
    write("22-01-python-i-veb.html", out)


def build_02() -> None:
    body = f"""
    <h2>Строительные блоки — HTML</h2>
    <p><strong>HTML</strong> (HyperText Markup Language — язык гипертекстовой разметки)
    описывает <em>структуру</em> страницы: где заголовок, где текст, где картинка, где
    ссылка. Каждый кусочек содержимого оборачивается в <strong>тег</strong>:</p>

    {code_block(
        "stranica.html",
        '<!doctype html>\n'
        '<html lang="ru">\n'
        '<head>\n'
        '  <meta charset="utf-8">\n'
        '  <title>Моя первая страница</title>\n'
        '</head>\n'
        '<body>\n'
        '  <h1>Привет, мир!</h1>\n'
        '  <p>Это мой первый сайт на HTML.</p>\n'
        '  <ul>\n'
        '    <li>Учу Python</li>\n'
        '    <li>Учу HTML</li>\n'
        '  </ul>\n'
        '  <a href="https://python.org">Официальный сайт Python</a>\n'
        '</body>\n'
        '</html>',
        lang="html",
    )}

    {callout(
        "tip",
        "Теги обычно идут парами",
        "<code class=\"inline\">&lt;h1&gt;</code> открывает заголовок, "
        "<code class=\"inline\">&lt;/h1&gt;</code> (со слэшем) его закрывает — почти как "
        "открывающая и закрывающая скобки в Python. Всё, что между ними, и есть содержимое "
        "этого элемента.",
    )}

    <p>Самые частые теги: <code class="inline">&lt;h1&gt;</code>…<code class="inline">&lt;h6&gt;</code>
    — заголовки разного уровня, <code class="inline">&lt;p&gt;</code> — абзац текста,
    <code class="inline">&lt;ul&gt;</code>/<code class="inline">&lt;li&gt;</code> — список,
    <code class="inline">&lt;a href="…"&gt;</code> — ссылка, <code class="inline">&lt;img
    src="…"&gt;</code> — картинка.</p>

    {practice_card(
        "22-02",
        "Практика: HTML и CSS вживую",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-02/index.html",
    )}
    """
    out = render_page(
        page_title="Строительные блоки — HTML",
        description="Основные теги HTML: заголовки, абзацы, списки и ссылки — на примере простой страницы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("HTML", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Строительные блоки — HTML",
        lede="HTML описывает структуру страницы: где заголовок, где текст, где ссылка.",
        body_html=body,
        sidebar_groups=sidebar("22-02-html.html"),
        nav=PageNav(prev_href="22-01-python-i-veb.html", prev_label="Python и веб-разработка", next_href="22-03-css.html", next_label="Делаем красивее — CSS"),
    )
    write("22-02-html.html", out)


def build_03() -> None:
    body = f"""
    <h2>Делаем красивее — CSS</h2>
    <p>Сам по себе HTML выглядит скучно — чёрный текст на белом фоне. За внешний вид
    отвечает <strong>CSS</strong> (Cascading Style Sheets — каскадные таблицы стилей). CSS
    выбирает элементы и задаёт им свойства — цвет, отступы, размер шрифта:</p>

    {code_block(
        "stili.css",
        'body {\n'
        '  font-family: sans-serif;\n'
        '  background: #f7f7fb;\n'
        '  color: #1a1a2e;\n'
        '}\n\n'
        'h1 {\n'
        '  color: #4a2fbd;\n'
        '}\n\n'
        'p {\n'
        '  line-height: 1.6;\n'
        '}',
        lang="css",
    )}

    <p>Подключить CSS-файл к HTML-странице можно одной строкой внутри
    <code class="inline">&lt;head&gt;</code>:</p>
    {code_block(
        "podklyuchenie.html",
        '<link rel="stylesheet" href="stili.css">',
        lang="html",
    )}

    {callout(
        "info",
        "«Каскадные» — откуда название",
        "Если два правила CSS задают один и тот же элемент по-разному, побеждает то, что "
        "идёт <em>позже</em> или более точно указывает на элемент — стили как бы "
        "«стекают» друг на друга, как каскад. Именно поэтому в имени CSS есть слово "
        "«каскадные».",
    )}

    {practice_card(
        "22-02",
        "Практика: включает пример CSS",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-02/index.html",
    )}
    """
    out = render_page(
        page_title="Делаем красивее — CSS",
        description="Как CSS задаёт цвета, шрифты и отступы для элементов HTML-страницы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("CSS", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Делаем красивее — CSS",
        lede="CSS превращает голый HTML в страницу с цветом, шрифтами и аккуратными отступами.",
        body_html=body,
        sidebar_groups=sidebar("22-03-css.html"),
        nav=PageNav(prev_href="22-02-html.html", prev_label="HTML", next_href="22-04-javascript.html", next_label="JavaScript"),
    )
    write("22-03-css.html", out)


def build_04() -> None:
    body = f"""
    <h2>Динамический фронтенд — JavaScript</h2>
    <p>HTML описывает структуру, CSS — оформление, а <strong>JavaScript</strong> добавляет
    <em>поведение</em>: реакцию на клики, изменение текста без перезагрузки страницы,
    проверку форм. JavaScript выполняется прямо в браузере пользователя:</p>

    {code_block(
        "povedenie.html",
        '<button id="knopka">Нажми меня</button>\n'
        '<p id="tekst">Пока ничего не произошло.</p>\n\n'
        '<script>\n'
        '  const knopka = document.getElementById("knopka");\n'
        '  const tekst = document.getElementById("tekst");\n\n'
        '  knopka.addEventListener("click", function () {\n'
        '    tekst.textContent = "Кнопку нажали!";\n'
        '  });\n'
        '</script>',
        lang="javascript",
    )}

    {callout(
        "info",
        "JavaScript и Python — похожи, но разные",
        "Синтаксис отличается (фигурные скобки вместо отступов, <code class=\"inline\">"
        "const</code>/<code class=\"inline\">function</code> вместо привычных конструкций "
        "Python), но идеи те же: переменные, функции, условия, циклы. Если вы понимаете "
        "Python — освоить основы JavaScript будет намного проще.",
    )}

    <p>Три языка вместе — HTML, CSS и JavaScript — и есть тот самый «фронтенд», который
    видит и с которым взаимодействует пользователь. Теперь перейдём к тому, что происходит
    на сервере — то есть к Python.</p>
    """
    out = render_page(
        page_title="Динамический фронтенд — JavaScript",
        description="JavaScript добавляет странице поведение: реакцию на клики и изменение содержимого без перезагрузки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("JavaScript", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Динамический фронтенд — JavaScript",
        lede="Если HTML — это скелет, а CSS — одежда, то JavaScript — это движения страницы.",
        body_html=body,
        sidebar_groups=sidebar("22-04-javascript.html"),
        nav=PageNav(prev_href="22-03-css.html", prev_label="CSS", next_href="22-05-flask.html", next_label="Flask в Python"),
    )
    write("22-04-javascript.html", out)


def build_05() -> None:
    body = f"""
    <h2>Flask в Python</h2>
    <p><strong>Flask</strong> — это лёгкая библиотека, которая превращает программу на
    Python в веб-сервер: она принимает HTTP-запросы от браузера и отправляет в ответ
    HTML-страницы. Установка — как у любой библиотеки:</p>
    {code_block("terminal.txt", "pip install flask", lang="text")}

    <h2>Самое маленькое Flask-приложение</h2>
    {code_block(
        "app_minimal.py",
        "from flask import Flask\n\n"
        "app = Flask(__name__)\n\n"
        '@app.route("/")\n'
        "def glavnaya():\n"
        '    return "Привет, мир!"\n\n'
        'if __name__ == "__main__":\n'
        "    app.run(debug=True)\n",
    )}
    {callout(
        "tip",
        "@app.route(\"/\") — декоратор маршрута",
        "Строчка над функцией — <strong>декоратор</strong> (глава 15 показывала похожую "
        "идею). <code class=\"inline\">@app.route(\"/\")</code> говорит Flask: «когда "
        "браузер запросит адрес <code class=\"inline\">/</code>, вызови функцию "
        "<code class=\"inline\">glavnaya()</code> и отправь то, что она вернёт».",
    )}

    <h2>Шаблоны — HTML с вставками Python</h2>
    <p>Возвращать HTML прямо строкой в Python неудобно. Flask использует движок шаблонов
    <strong>Jinja2</strong> — обычный HTML-файл, куда можно вставлять python-подобные
    выражения в фигурных скобках <code class="inline">{{{{ }}}}</code>:</p>
    {code_block(
        "templates/index.html",
        '<h1>Мой список задач</h1>\n'
        '<ul>\n'
        '  {% for zadacha in zadachi %}\n'
        '    <li>{{ zadacha }}</li>\n'
        '  {% endfor %}\n'
        '</ul>',
        lang="html",
    )}
    {code_block(
        "app.py",
        "from flask import Flask, render_template\n\n"
        "app = Flask(__name__)\n"
        'zadachi = ["Выучить основы Python", "Собрать сайт на Flask"]\n\n'
        '@app.route("/")\n'
        "def glavnaya():\n"
        '    return render_template("index.html", zadachi=zadachi)\n',
    )}

    <h2>Динамические адреса</h2>
    <p>Часть адреса можно превратить в параметр функции — Flask сам передаст в неё нужное
    значение из URL:</p>
    {code_block(
        "dinamicheskij_marshrut.py",
        '@app.route("/privet/<imya>")\n'
        "def privet(imya):\n"
        '    return render_template("privet.html", imya=imya)\n',
    )}
    {callout(
        "info",
        "/privet/Сергей → imya = \"Сергей\"",
        "Открыв в браузере адрес <code class=\"inline\">/privet/Сергей</code>, вы получите "
        "в переменной <code class=\"inline\">imya</code> строку <code class=\"inline\">"
        "\"Сергей\"</code> — Flask сам достаёт эту часть из адреса.",
    )}

    <h2>Принимаем данные из формы</h2>
    <p>Чтобы пользователь мог что-то отправить на сервер (например, добавить задачу),
    используется HTML-форма и маршрут, принимающий метод <code class="inline">POST</code>:</p>
    {code_block(
        "dobavlenie.py",
        'from flask import request, redirect, url_for\n\n'
        '@app.route("/dobavit", methods=["POST"])\n'
        "def dobavit():\n"
        '    novaya_zadacha = request.form.get("zadacha", "").strip()\n'
        "    if novaya_zadacha:\n"
        "        zadachi.append(novaya_zadacha)\n"
        '    return redirect(url_for("glavnaya"))\n',
    )}

    <h2>Полный проект</h2>
    <p>Всё вместе — маршруты, шаблоны, форма и статический CSS-файл — собрано в готовый
    мини-сайт «Список задач»:</p>
    <p>📄 <a href="../../../projects/flask/todo-app/app.py">projects/flask/todo-app/app.py</a></p>
    {callout(
        "tip",
        "Запустите сайт у себя",
        "<code class=\"inline\">python app.py</code> в терминале внутри "
        "<code class=\"inline\">projects/flask/todo-app/</code>, затем откройте "
        "<code class=\"inline\">http://127.0.0.1:5000/</code> в браузере.",
    )}

    {exercise(2, "Счётчик задач", "Добавьте в index.html строку, показывающую общее количество задач: {{ zadachi|length }}.")}
    {exercise(3, "Удаление задачи", "Добавьте маршрут /udalit/&lt;int:indeks&gt;, который удаляет задачу по её номеру в списке и делает редирект на главную.")}

    {local_required_card(
        "22-05",
        "Практика: маршруты, шаблоны и формы",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-05/index.html",
    )}
    """
    out = render_page(
        page_title="Flask в Python",
        description="Первое Flask-приложение: маршруты, шаблоны Jinja2, динамические адреса и приём данных из формы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Flask", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Flask в Python",
        lede="Flask превращает программу на Python в веб-сервер — и делает это на удивление просто.",
        body_html=body,
        sidebar_groups=sidebar("22-05-flask.html"),
        nav=PageNav(prev_href="22-04-javascript.html", prev_label="JavaScript", next_href="22-06-itogi.html", next_label="Итоги"),
    )
    write("22-05-flask.html", out)


def build_06() -> None:
    body = f"""
    {summary_box("Что мы узнали в этой главе", [
        "Сайт — это диалог по протоколу HTTP: браузер (клиент) отправляет запрос, "
        "сервер отвечает.",
        "Фронтенд (то, что видит пользователь) строится из трёх языков: HTML "
        "(структура), CSS (оформление) и JavaScript (поведение).",
        "Бэкенд — программа на сервере, которая готовит ответы. На Python для этого "
        "часто используют библиотеку Flask.",
        "<code class=\"inline\">@app.route(\"/адрес\")</code> связывает адрес с функцией, "
        "которая на него отвечает.",
        "Шаблоны Jinja2 позволяют вставлять данные Python прямо в HTML через "
        "<code class=\"inline\">{{ }}</code> и <code class=\"inline\">{% %}</code>.",
        "Формы с методом POST и <code class=\"inline\">request.form</code> позволяют "
        "принимать данные, которые пользователь ввёл в браузере.",
    ])}

    <p>Веб-разработка — огромная тема, и эта глава лишь приоткрыла дверь. Если вам
    понравилось — в главе 24 («Что дальше?») есть раздел с идеями, куда двигаться
    дальше.</p>
    """
    out = render_page(
        page_title="Итоги главы 22",
        description="Итоги главы о веб-разработке: HTTP, HTML, CSS, JavaScript и первое приложение на Flask.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Итоги", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Итоги",
        lede="От HTTP-запроса до собственного сайта на Flask — коротко о том, что мы прошли.",
        body_html=body,
        sidebar_groups=sidebar("22-06-itogi.html"),
        nav=PageNav(prev_href="22-05-flask.html", prev_label="Flask в Python", next_href="../glava-23/index.html", next_label="Глава 23: Ещё больше мини-проектов"),
    )
    write("22-06-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
