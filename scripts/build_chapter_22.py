#!/usr/bin/env python3
"""Строит Главу 22: «Веб-разработка с Python» (site/chapters/glava-22/).

Разделы 22.1-22.6 воспроизводят исторический печатный порядок изложения
(с оригинальными номерами страниц бумажной книги). Разделы 22.7+ продолжают
ту же тему в цифровом издании и не имеют физической пагинации — см.
render_chapter_opener() и аналогичный комментарий в build_chapter_21.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    capability_map,
    code_block,
    comparison_table,
    decision_map,
    exercise,
    flow_diagram,
    image_figure,
    local_required_card,
    path_anatomy_diagram,
    pipeline_diagram,
    practice_card,
    relationship_diagram,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-22"
IMG = "../../assets/img/chapter-22/output"

PAGES = [
    ("index.html", "Обзор главы"),
    ("22-01-python-i-veb.html", "Основы веб-разработки: клиент, сервер и Python"),
    ("22-02-html.html", "HTML: структура веб-страницы"),
    ("22-03-css.html", "CSS: оформление и расположение элементов веб-страницы"),
    ("22-04-javascript.html", "JavaScript: программирование в браузере"),
    ("22-05-flask.html", "Первое веб-приложение на Flask"),
    ("22-06-itogi.html", "Итоги первого веб-проекта"),
    ("22-07-put-zaprosa.html", "Как браузер получает веб-страницу"),
    ("22-08-url-anatomiya.html", "URL: домен, путь, параметры и фрагмент"),
    ("22-09-http.html", "HTTP: запросы, ответы, методы и коды состояния"),
    ("22-10-https.html", "HTTPS: защита соединения с сайтом"),
    ("22-11-flask-marshrutizaciya.html", "Маршрутизация во Flask: URL и функции-обработчики"),
    ("22-12-jinja-shablony.html", "Jinja: шаблоны HTML с данными"),
    ("22-13-formy.html", "HTML-формы и отправка данных на сервер"),
    ("22-14-staticheskie-fajly.html", "Статические файлы: CSS, изображения и JavaScript"),
    ("22-15-json.html", "JSON: формат обмена данными"),
    ("22-16-api.html", "HTTP API: обмен данными между программами"),
    ("22-17-veb-frejmvorki.html", "Веб-фреймворки на Python: Flask, Django, FastAPI и другие"),
    ("22-18-flask-django-fastapi.html", "Сравнение Flask, Django и FastAPI"),
    ("22-19-wsgi-asgi.html", "WSGI и ASGI: связь веб-приложения с сервером"),
    ("22-20-zachem-baza-dannyh.html", "Зачем веб-приложению база данных"),
    ("22-21-relyacionnaya-baza.html", "Реляционные базы данных: таблицы, ключи и связи"),
    ("22-22-sql.html", "SQL: создаём, читаем и изменяем данные"),
    ("22-23-sqlite.html", "SQLite: встраиваемая реляционная СУБД"),
    ("22-24-postgresql-mysql-sqlite.html", "PostgreSQL, MySQL/MariaDB и SQLite: основные различия"),
    ("22-25-nosql.html", "NoSQL: основные виды нереляционных баз данных"),
    ("22-26-orm.html", "ORM: работа с базой данных через объекты Python"),
    ("22-27-migracii-shemy.html", "Миграции схемы базы данных"),
    ("22-28-perenos-dannyh.html", "Перенос данных между базами"),
    ("22-29-flask-sqlite.html", "Flask и SQLite: сохраняем данные в базе"),
    ("22-30-cookies-session.html", "Cookie и сессии: состояние между HTTP-запросами"),
    ("22-31-validaciya-oshibki.html", "Проверка входных данных и обработка ошибок"),
    ("22-32-bezopasnost.html", "Основы безопасности веб-приложений"),
    ("22-33-testiruem-flask.html", "Автоматическое тестирование Flask-приложения"),
    ("22-34-razvyortyvanie.html", "Развёртывание Flask-приложения"),
    ("22-35-itogovyj-proekt.html", "Итоговый проект: список задач на Flask и SQLite"),
    ("22-36-chto-dalshe.html", "Дальнейшее изучение веб-разработки на Python"),
]

LESSON_IDS = [
    "22-02", "22-05", "22-08", "22-09", "22-11", "22-12", "22-13", "22-15",
    "22-16", "22-18", "22-19", "22-22", "22-23", "22-26", "22-27", "22-28",
    "22-29", "22-30", "22-31", "22-32", "22-33", "22-35",
]

FUTURE_COURSE = (
    "Этой теме будет посвящён отдельный курс Cartesian School «Веб-разработка "
    "на Python: от HTTP до развёртывания» (курс готовится). Он продолжит "
    "материал этой главы значительно глубже."
)


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 22 · Веб-разработка", items),
        SidebarGroup(
            "Практика",
            [NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS],
        ),
        SidebarGroup("Исходный код", [NavItem("[[icon:code]] projects/flask/todo-app/", "../../../projects/flask/todo-app/app.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=22,
        baseline_page=497,
        title="Веб-разработка с Python",
        description="Введение в устройство веб-приложений: браузер и сервер, HTTP и HTTPS, HTML/CSS/"
        "JavaScript, Flask, базы данных, SQL, JSON и API. Более глубокое изучение продолжается "
        "в отдельном курсе по веб-разработке на Python.",
        meta_items=["[[icon:timer]] ~8-10 часов", "[[icon:note]] от HTTP-запроса до Flask с базой данных", "[[icon:practice]] 22 практики"],
        sections=[
            ChapterSectionLink("22.1", "Основы веб-разработки: клиент, сервер и Python", "22-01-python-i-veb.html", "497"),
            ChapterSectionLink("22.2", "HTML: структура веб-страницы", "22-02-html.html", "499"),
            ChapterSectionLink("22.3", "CSS: оформление и расположение элементов веб-страницы", "22-03-css.html", "502"),
            ChapterSectionLink("22.4", "JavaScript: программирование в браузере", "22-04-javascript.html", "504"),
            ChapterSectionLink("22.5", "Первое веб-приложение на Flask", "22-05-flask.html", "507"),
            ChapterSectionLink("22.6", "Итоги первого веб-проекта", "22-06-itogi.html", "510"),
            # С 22.7 главу продолжают страницы цифрового издания — у них нет
            # физической страницы бумажного макета, поэтому page не указывается.
            ChapterSectionLink("22.7", "Как браузер получает веб-страницу", "22-07-put-zaprosa.html"),
            ChapterSectionLink("22.8", "URL: домен, путь, параметры и фрагмент", "22-08-url-anatomiya.html"),
            ChapterSectionLink("22.9", "HTTP: запросы, ответы, методы и коды состояния", "22-09-http.html"),
            ChapterSectionLink("22.10", "HTTPS: защита соединения с сайтом", "22-10-https.html"),
            ChapterSectionLink("22.11", "Маршрутизация во Flask: URL и функции-обработчики", "22-11-flask-marshrutizaciya.html"),
            ChapterSectionLink("22.12", "Jinja: шаблоны HTML с данными", "22-12-jinja-shablony.html"),
            ChapterSectionLink("22.13", "HTML-формы и отправка данных на сервер", "22-13-formy.html"),
            ChapterSectionLink("22.14", "Статические файлы: CSS, изображения и JavaScript", "22-14-staticheskie-fajly.html"),
            ChapterSectionLink("22.15", "JSON: формат обмена данными", "22-15-json.html"),
            ChapterSectionLink("22.16", "HTTP API: обмен данными между программами", "22-16-api.html"),
            ChapterSectionLink("22.17", "Веб-фреймворки на Python: Flask, Django, FastAPI и другие", "22-17-veb-frejmvorki.html"),
            ChapterSectionLink("22.18", "Сравнение Flask, Django и FastAPI", "22-18-flask-django-fastapi.html"),
            ChapterSectionLink("22.19", "WSGI и ASGI: связь веб-приложения с сервером", "22-19-wsgi-asgi.html"),
            ChapterSectionLink("22.20", "Зачем веб-приложению база данных", "22-20-zachem-baza-dannyh.html"),
            ChapterSectionLink("22.21", "Реляционные базы данных: таблицы, ключи и связи", "22-21-relyacionnaya-baza.html"),
            ChapterSectionLink("22.22", "SQL: создаём, читаем и изменяем данные", "22-22-sql.html"),
            ChapterSectionLink("22.23", "SQLite: встраиваемая реляционная СУБД", "22-23-sqlite.html"),
            ChapterSectionLink("22.24", "PostgreSQL, MySQL/MariaDB и SQLite: основные различия", "22-24-postgresql-mysql-sqlite.html"),
            ChapterSectionLink("22.25", "NoSQL: основные виды нереляционных баз данных", "22-25-nosql.html"),
            ChapterSectionLink("22.26", "ORM: работа с базой данных через объекты Python", "22-26-orm.html"),
            ChapterSectionLink("22.27", "Миграции схемы базы данных", "22-27-migracii-shemy.html"),
            ChapterSectionLink("22.28", "Перенос данных между базами", "22-28-perenos-dannyh.html"),
            ChapterSectionLink("22.29", "Flask и SQLite: сохраняем данные в базе", "22-29-flask-sqlite.html"),
            ChapterSectionLink("22.30", "Cookie и сессии: состояние между HTTP-запросами", "22-30-cookies-session.html"),
            ChapterSectionLink("22.31", "Проверка входных данных и обработка ошибок", "22-31-validaciya-oshibki.html"),
            ChapterSectionLink("22.32", "Основы безопасности веб-приложений", "22-32-bezopasnost.html"),
            ChapterSectionLink("22.33", "Автоматическое тестирование Flask-приложения", "22-33-testiruem-flask.html"),
            ChapterSectionLink("22.34", "Развёртывание Flask-приложения", "22-34-razvyortyvanie.html"),
            ChapterSectionLink("22.35", "Итоговый проект: список задач на Flask и SQLite", "22-35-itogovyj-proekt.html"),
            ChapterSectionLink("22.36", "Дальнейшее изучение веб-разработки на Python", "22-36-chto-dalshe.html"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>Веб-приложение обычно состоит из двух взаимодействующих сторон: клиента и сервера.
    Клиентом чаще всего является браузер. Он отправляет HTTP-запросы и отображает полученные
    ответы. Серверная часть принимает запросы, выполняет логику приложения, при необходимости
    обращается к базе данных и формирует ответ.</p>

    <p>Python часто используется для программирования серверной части веб-приложения. В этой
    главе серверное приложение написано на Python с использованием Flask.</p>

    {callout(
        "info",
        "А как же Python в браузере?",
        "Это не означает, что Python принципиально не может выполняться в браузере. "
        "Существуют среды на основе WebAssembly, например Pyodide — на нём построена "
        "интерактивная практика этой книги, — которые позволяют выполнять Python на стороне "
        "клиента. Однако это другая модель выполнения; здесь изучается классическая серверная "
        "веб-разработка.",
    )}

    <h2>Клиент и сервер</h2>
    <p><strong>Клиент</strong> — программа, которая отправляет запрос и получает на него ответ.
    <strong>Сервер</strong> — программа, которая принимает запросы и отвечает на них. Слово
    «сервер» обозначает именно серверную программу (процесс); в разговорной речи им иногда
    называют и компьютер, на котором эта программа запущена, — из контекста обычно понятно,
    что имеется в виду.</p>

    {flow_diagram([
        ("Браузер (клиент)", "отправляет запрос"),
        ("Интернет", "передаёт данные"),
        ("Сервер", "готовит ответ"),
        ("Браузер (клиент)", "показывает страницу"),
    ], caption="Один цикл: запрос уходит на сервер, ответ возвращается и отображается в браузере")}

    <p>Этот обмен запросами и ответами подчиняется общему правилу — протоколу
    <strong>HTTP</strong> (HyperText Transfer Protocol, протокол передачи гипертекста).
    Подробнее об этом — в разделах 22.7-22.10; здесь достаточно знать, что браузер и сервер
    обмениваются сообщениями по одним и тем же правилам, независимо от того, кто их написал.</p>

    <h2>Что делает браузер</h2>
    <p>Браузер — это клиентская программа, которая по адресу пользователя строит и отправляет
    HTTP-запрос, получает HTTP-ответ и отображает его: разбирает HTML, применяет CSS,
    выполняет JavaScript, показывает изображения и другие ресурсы страницы.</p>

    <h2>Что делает серверное приложение</h2>
    <p>Серверное приложение принимает запрос, определяет, что нужно сделать (открыть список
    задач, сохранить новую запись, вернуть данные в формате JSON), при необходимости обращается
    к базе данных и формирует ответ — чаще всего HTML-страницу или данные.</p>

    <h2>Где используется Python</h2>
    <p>В типичном веб-приложении Python работает на серверной стороне: код выполняется на
    сервере, а браузеру отправляется уже готовый результат. Дальше в этой главе так и есть —
    Python исполняется сервером, собранным на Flask.</p>

    <h2>Интернет и Всемирная паутина</h2>
    <p><strong>Интернет</strong> — это сеть, которая физически соединяет компьютеры друг с
    другом и умеет передавать между ними данные. <strong>Всемирная паутина</strong> (World Wide
    Web, веб) — один из способов использовать эту сеть: сайты, ссылки между ними, протокол
    HTTP. По тому же интернету работают и другие сервисы — почта, мессенджеры, онлайн-игры, —
    веб лишь один из них, хотя и самый заметный.</p>

    <h2>Адрес сайта: домен и IP-адрес</h2>
    <p>Чтобы браузер знал, к какому серверу обращаться, у сайта есть <strong>домен</strong> —
    имя вида <code class="inline">python.org</code>, которое человеку легко запомнить. Но
    компьютеры в интернете находят друг друга по числовым адресам —
    <strong>IP-адресам</strong>. Специальная служба, DNS, превращает домен в IP-адрес перед
    отправкой запроса. Весь этот путь подробно рассматривается в разделе 22.7, а устройство
    самого адреса — в разделе 22.8.</p>

    <h2>Фронтенд и бэкенд</h2>
    <p>То, что видит и с чем взаимодействует пользователь в браузере — HTML, CSS, JavaScript, —
    называют <strong>фронтендом</strong> (front — «перед»). Программу, которая работает на
    сервере и готовит ответы, называют <strong>бэкендом</strong> (back — «тыл»).</p>

    <h2>Статическая страница и динамическое приложение</h2>
    <p>Самый простой сайт — это просто файлы <code class="inline">.html</code>, лежащие на
    сервере: сервер отдаёт их без изменений, это <strong>статическая</strong> страница. Если
    же ответ каждый раз собирается заново — с учётом того, кто спросил, что хранится в базе
    данных, что человек только что отправил в форме, — такое приложение называют
    <strong>динамическим</strong>. Сайт, который вы соберёте в этой главе на Flask, —
    динамический: он строит HTML-страницу из данных прямо во время запроса.</p>

    <p>В следующих трёх разделах — краткое знакомство с языками фронтенда: HTML (раздел 22.2),
    CSS (раздел 22.3) и JavaScript (раздел 22.4). Затем — первый бэкенд на Python с
    библиотекой <strong>Flask</strong> (раздел 22.5).</p>
    """
    out = render_page(
        page_title="Основы веб-разработки: клиент, сервер и Python",
        description="Клиент и сервер, интернет и Всемирная паутина, фронтенд и бэкенд, статические и динамические страницы, где работает Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Клиент, сервер и Python", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Основы веб-разработки: клиент, сервер и Python",
        lede="Веб-приложение — это диалог между клиентом и сервером. Разберёмся, кто в нём кто.",
        body_html=body,
        sidebar_groups=sidebar("22-01-python-i-veb.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="22-02-html.html", next_label="HTML: структура веб-страницы"),
    )
    write("22-01-python-i-veb.html", out)


def build_02() -> None:
    body = f"""
    <p><strong>HTML</strong> (HyperText Markup Language — язык гипертекстовой разметки)
    описывает не поведение и не внешний вид, а <em>структуру</em> страницы: где заголовок,
    где абзац текста, где картинка, где ссылка. HTML — язык разметки, а не язык
    программирования: в нём нет условий, циклов или переменных, только описание того, что и
    в каком порядке показать.</p>

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

    {image_figure(
        f"{IMG}/01-raw-html.png",
        "Страница в браузере без единой строчки CSS: чёрный заголовок, обычный текст, список точками, синяя подчёркнутая ссылка",
        "Тот же файл, открытый в браузере, без единого правила CSS — браузер сам выбирает шрифт, отступы и цвет ссылки по умолчанию.",
        width=420,
    )}

    {callout(
        "tip",
        "Теги обычно идут парами",
        "<code class=\"inline\">&lt;h1&gt;</code> — открывающий тег заголовка, "
        "<code class=\"inline\">&lt;/h1&gt;</code> (со слэшем) — закрывающий, а вместе с "
        "содержимым между ними они образуют один <strong>элемент</strong> страницы. У "
        "некоторых элементов, например <code class=\"inline\">&lt;img&gt;</code>, нет "
        "закрывающего тега и вложенного содержимого — это называют "
        "<strong>void-элементом</strong>: вся нужная информация передаётся через атрибуты.",
    )}

    <h2>Атрибуты — дополнительные свойства тега</h2>
    <p>Внутри открывающего тега можно указать <strong>атрибуты</strong> — пары
    <code class="inline">имя="значение"</code>. У ссылки <code class="inline">&lt;a&gt;</code>
    атрибут <code class="inline">href</code> задаёт адрес, у картинки
    <code class="inline">&lt;img&gt;</code> — <code class="inline">src</code> задаёт файл, а
    <code class="inline">alt</code> задаёт текстовую альтернативу изображения, соответствующую
    его смыслу на странице: её используют программы для чтения с экрана и она показывается,
    если файл не загрузился:</p>
    {code_block(
        "atributy.html",
        '<img src="kotik.jpg" alt="Рыжий кот спит на подоконнике">',
        lang="html",
    )}

    <h2>Частые теги</h2>
    {comparison_table(
        ["Тег", "Что описывает"],
        [
            ["<code class=\"inline\">&lt;h1&gt;</code>…<code class=\"inline\">&lt;h6&gt;</code>", "Заголовки от самого важного (h1) до самого мелкого (h6)"],
            ["<code class=\"inline\">&lt;p&gt;</code>", "Абзац текста"],
            ["<code class=\"inline\">&lt;ul&gt;</code> / <code class=\"inline\">&lt;li&gt;</code>", "Список и его пункты"],
            ["<code class=\"inline\">&lt;a href=\"…\"&gt;</code>", "Ссылка на другую страницу"],
            ["<code class=\"inline\">&lt;img src=\"…\" alt=\"…\"&gt;</code>", "Изображение с текстовым описанием"],
            ["<code class=\"inline\">&lt;label&gt;</code> / <code class=\"inline\">&lt;input&gt;</code>", "Поле формы и его подпись"],
        ],
    )}

    {callout(
        "info",
        "Заголовки — не просто крупный шрифт",
        "Уровни <code class=\"inline\">h1</code>-<code class=\"inline\">h6</code> задают "
        "логическую структуру страницы, как оглавление книги: <code class=\"inline\">h1</code> "
        "— главный заголовок, у него на странице обычно один, а <code class=\"inline\">h2</code>"
        " — заголовки разделов внутри. Программы для чтения с экрана и поисковые системы "
        "используют именно эту структуру, а не то, крупным ли шрифтом что-то нарисовано.",
    )}

    <h2>Формы</h2>
    <p>Форма собирает то, что ввёл пользователь, и отправляет это на сервер:</p>
    {code_block(
        "forma.html",
        '<form>\n'
        '  <label for="imya">Ваше имя</label>\n'
        '  <input type="text" id="imya" name="imya">\n'
        '  <button type="submit">Отправить</button>\n'
        '</form>',
        lang="html",
    )}
    <p><code class="inline">&lt;label for="imya"&gt;</code> связан с
    <code class="inline">&lt;input id="imya"&gt;</code> по совпадающему идентификатору — клик
    по подписи ставит курсор в поле, а программа для чтения с экрана озвучивает подпись, когда
    поле получает фокус. Что происходит с этими данными на сервере — в разделе 22.13.</p>

    {practice_card(
        "22-02",
        "Практика: структура HTML и стили CSS",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-02/index.html",
    )}
    """
    out = render_page(
        page_title="HTML: структура веб-страницы",
        description="HTML описывает структуру страницы: заголовки, абзацы, списки, ссылки, атрибуты и основы доступности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("HTML", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="HTML: структура веб-страницы",
        lede="HTML — язык разметки, а не программирования: он описывает структуру, а не поведение.",
        body_html=body,
        sidebar_groups=sidebar("22-02-html.html"),
        nav=PageNav(prev_href="22-01-python-i-veb.html", prev_label="Основы веб-разработки: клиент, сервер и Python", next_href="22-03-css.html", next_label="CSS: оформление и расположение элементов веб-страницы"),
    )
    write("22-02-html.html", out)


def build_03() -> None:
    body = f"""
    <p><strong>CSS</strong> (Cascading Style Sheets — каскадные таблицы стилей) — язык таблиц
    стилей, предназначенный для описания внешнего вида и расположения элементов документа,
    написанного на HTML или другом языке разметки. С помощью CSS задают цвета, шрифты,
    размеры, отступы, рамки, расположение элементов и адаптацию страницы к разным размерам
    экрана.</p>

    <p>HTML задаёт структуру документа, а CSS определяет, как эта структура отображается на
    экране: без собственных стилей браузер применяет стандартное оформление — обычный шрифт,
    чёрный текст, минимальные отступы. CSS выбирает элементы страницы и задаёт им свойства:</p>

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

    <p>Каждое правило CSS — это <strong>селектор</strong> (какие элементы выбирает правило: по
    тегу, классу или идентификатору) и фигурные скобки с парами <strong>свойство: значение</strong>. Подключить
    CSS-файл к HTML-странице можно одной строкой внутри
    <code class="inline">&lt;head&gt;</code>:</p>
    {code_block(
        "podklyuchenie.html",
        '<link rel="stylesheet" href="stili.css">',
        lang="html",
    )}

    {image_figure(
        f"{IMG}/02-html-css.png",
        "Та же страница с подключённым CSS: светло-сиреневый фон, тёмно-фиолетовый заголовок и увеличенный межстрочный интервал у абзаца",
        "Ровно тот же HTML из раздела 22.2, но с подключённым stili.css: фон, цвет заголовка и межстрочный интервал теперь заданы явно, а не оставлены на усмотрение браузера.",
        width=420,
    )}

    <h2>Классы — стилизуем не все теги подряд</h2>
    <p>Селектор по тегу (<code class="inline">p {{ }}</code>) красит все абзацы разом. Чтобы
    выделить только некоторые элементы, им дают атрибут <code class="inline">class</code>, а в
    CSS обращаются к нему через точку:</p>
    {code_block(
        "klass.html",
        '<p class="preduprezhdenie">Осторожно, ступенька!</p>',
        lang="html",
    )}
    {code_block("klass.css", '.preduprezhdenie {\n  color: #b3261e;\n  font-weight: 700;\n}', lang="css")}

    {callout(
        "info",
        "Каскад и наследование — два разных механизма",
        "<strong>Каскад</strong> решает, какое из нескольких конкурирующих правил применить к "
        "одному и тому же элементу: в упрощённом случае, когда остальные условия равны, более "
        "специфичный селектор побеждает менее специфичный, а при одинаковой специфичности — "
        "решает порядок правил в файле. Это часть алгоритма каскада, а не он целиком. "
        "<strong>Наследование</strong> — отдельный механизм: некоторые свойства (например, "
        "<code class=\"inline\">font-family</code>) элемент по умолчанию перенимает от "
        "родителя, если для него самого явно ничего не задано.",
    )}

    <h2>Блочная модель</h2>
    <p>У каждого элемента есть содержимое, а вокруг него — отступ внутри рамки
    (<code class="inline">padding</code>), сама рамка (<code class="inline">border</code>) и
    отступ снаружи, до соседних элементов (<code class="inline">margin</code>):</p>
    {code_block(
        "blochnaya_model.css",
        '.kartochka {\n'
        '  padding: 16px;\n'
        '  border: 1px solid #ccc;\n'
        '  margin: 12px;\n'
        '}',
        lang="css",
    )}

    <h2>Расположение элементов: display и flexbox</h2>
    <p>Свойство <code class="inline">display</code> определяет, ведёт ли себя элемент как блок
    на всю ширину (<code class="inline">block</code>, как <code class="inline">&lt;p&gt;</code>
    и <code class="inline">&lt;div&gt;</code>) или как часть строки
    (<code class="inline">inline</code>, как <code class="inline">&lt;a&gt;</code> и
    <code class="inline">&lt;span&gt;</code>). Чтобы выстроить несколько элементов в ряд с
    равными промежутками, чаще всего используют <code class="inline">flexbox</code>:</p>
    {code_block(
        "flexbox.css",
        '.panel {\n'
        '  display: flex;\n'
        '  gap: 12px;\n'
        '  align-items: center;\n'
        '}',
        lang="css",
    )}

    <h2>Адаптивная вёрстка: одна страница, разные экраны</h2>
    <p><strong>Медиа-запрос</strong> (media query) применяет часть правил только при
    определённых условиях — например, только на узких экранах:</p>
    {code_block(
        "adaptivnost.css",
        '@media (max-width: 480px) {\n'
        '  .panel {\n'
        '    flex-direction: column;\n'
        '  }\n'
        '}',
        lang="css",
    )}
    <p>Так одна и та же страница может выстраивать элементы в ряд на широком экране и
    столбиком — на узком, без отдельного мобильного сайта. Итоговый проект главы (раздел
    22.35) использует именно этот приём.</p>

    <p>Официальная документация: <a href="https://developer.mozilla.org/ru/docs/Web/CSS">MDN — CSS</a>.</p>

    {practice_card(
        "22-02",
        "Практика: структура HTML и стили CSS",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-02/index.html",
    )}
    """
    out = render_page(
        page_title="CSS: оформление и расположение элементов веб-страницы",
        description="CSS как язык таблиц стилей: селекторы, классы, каскад и наследование, блочная модель, flexbox и медиа-запросы для адаптивной вёрстки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("CSS", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="CSS: оформление и расположение элементов веб-страницы",
        lede="CSS определяет внешний вид и расположение элементов HTML-документа.",
        body_html=body,
        sidebar_groups=sidebar("22-03-css.html"),
        nav=PageNav(prev_href="22-02-html.html", prev_label="HTML: структура веб-страницы", next_href="22-04-javascript.html", next_label="JavaScript: программирование в браузере"),
    )
    write("22-03-css.html", out)


def build_04() -> None:
    body = f"""
    <p><strong>JavaScript</strong> (JS) — язык программирования, широко используемый в
    веб-разработке. Ядро языка стандартизовано спецификацией ECMAScript (ECMA-262). В браузере
    JavaScript выполняет программную логику страницы: обрабатывает события, работает с DOM,
    изменяет содержимое страницы и может отправлять сетевые запросы.</p>

    {callout(
        "info",
        "JavaScript работает не только в браузере",
        "JavaScript используется не только в браузерах. Он также работает в серверных и других "
        "средах выполнения, например Node.js. Поэтому JavaScript — не просто «язык для "
        "браузера», хотя именно браузерное применение рассматривается в этом разделе.",
    )}

    <h2>Основные свойства JavaScript</h2>
    {capability_map([
        ("Типизация и память", ["Динамическая типизация", "Автоматическое управление памятью (сборка мусора)"]),
        ("Модель объектов", ["Прототипная модель объектов", "Функции — значения первого класса"]),
        ("Стили программирования", ["Императивный стиль", "Объектный стиль", "Функциональный стиль"]),
    ], title="Что за язык JavaScript")}

    {callout(
        "warning",
        "ECMAScript, DOM и Web API — не одно и то же",
        "<strong>ECMAScript</strong> — стандарт, описывающий сам язык: синтаксис, типы, "
        "операторы, функции. <strong>DOM</strong> (Document Object Model) и такие функции, как "
        "<code class=\"inline\">fetch()</code>, не входят в ECMAScript — это отдельные "
        "программные интерфейсы (Web API), которые браузер предоставляет коду JavaScript в "
        "дополнение к самому языку.",
    )}

    <p>JavaScript добавляет странице <em>поведение</em>: реакцию на клики, изменение содержимого
    без перезагрузки страницы, проверку формы перед отправкой. JavaScript нужен не каждой
    странице: простая статья или документ хорошо работают на одном HTML (плюс CSS для
    оформления) — браузер отображает такую страницу без единой строчки JavaScript. JavaScript
    нужен именно там, где странице требуется реагировать на действия пользователя без нового
    запроса к серверу.</p>

    <h2>DOM — представление страницы, с которым работает JavaScript</h2>
    <p>Когда браузер разбирает HTML, он строит из тегов дерево объектов в памяти — DOM
    (Document Object Model). JavaScript не редактирует исходный текст HTML-файла — он находит
    нужный узел в этом дереве и меняет его:</p>
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

    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div style="flex:1 1 260px;min-width:220px">
        {image_figure(
            f"{IMG}/03-js-before-click.png",
            "Страница с кнопкой «Нажми меня» и текстом «Пока ничего не произошло.» до клика",
            "До клика: обработчик подписан, но событие ещё не произошло.",
        )}
      </div>
      <div style="flex:1 1 260px;min-width:220px">
        {image_figure(
            f"{IMG}/04-js-after-click.png",
            "Та же страница сразу после клика по кнопке: текст сменился на «Кнопку нажали!»",
            "После клика: та же страница, без перезагрузки — JavaScript просто заменил содержимое узла #tekst.",
        )}
      </div>
    </div>

    <p><code class="inline">addEventListener("click", ...)</code> подписывает функцию на
    <strong>событие</strong> — клик по кнопке. Событий много: <code class="inline">"click"</code>,
    <code class="inline">"submit"</code> (отправка формы), <code class="inline">"input"</code>
    (ввод текста) и другие — код выполняется только тогда, когда событие действительно
    произошло.</p>

    {callout(
        "info",
        "Знакомые конструкции в другом синтаксисе",
        "И в Python, и в JavaScript есть переменные, функции, условия и циклы. Но их системы "
        "типов, модели объектов и среды выполнения существенно различаются: например, JavaScript "
        "использует прототипную модель объектов и фигурные скобки вместо отступов. Если вы "
        "понимаете Python, освоить основы JavaScript будет заметно проще, чем начинать с нуля.",
    )}

    <h2>Проверка формы прямо в браузере</h2>
    <p>JavaScript может проверить поле формы ещё до отправки — и сразу показать подсказку, не
    дожидаясь ответа сервера:</p>
    {code_block(
        "validaciya.js",
        'forma.addEventListener("submit", function (event) {\n'
        '  if (pole.value.trim() === "") {\n'
        '    event.preventDefault();\n'
        '    oshibka.textContent = "Поле не должно быть пустым";\n'
        '  }\n'
        '});',
        lang="javascript",
    )}
    <p><code class="inline">event.preventDefault()</code> останавливает обычную отправку формы
    — страница не перезагрузится, пока ошибка не исправлена. Ту же проверку всё равно
    необходимо повторить и на сервере (раздел 22.31): пользователь может отправить
    запрос вообще без браузера, в обход любого JavaScript.</p>

    <h2>fetch() — запрос к серверу без перезагрузки страницы</h2>
    <p>Функция <code class="inline">fetch()</code> отправляет HTTP-запрос из JavaScript и
    получает ответ, не перезагружая страницу целиком:</p>
    {code_block(
        "fetch.js",
        'fetch("/api/tasks")\n'
        '  .then(function (response) { return response.json(); })\n'
        '  .then(function (data) { console.log(data); });',
        lang="javascript",
    )}
    <p>Что такое <code class="inline">/api/tasks</code> и что именно возвращает такой запрос —
    в разделе 22.16.</p>

    <p>Три языка вместе — HTML, CSS и JavaScript — и есть тот самый «фронтенд», который видит и
    с которым взаимодействует пользователь. Дальше в главе речь пойдёт о том, что происходит на
    сервере, — то есть о Python.</p>

    <p>Официальная документация: <a href="https://developer.mozilla.org/ru/docs/Web/JavaScript">MDN — JavaScript</a>,
    <a href="https://tc39.es/ecma262/">ECMA-262 (ECMAScript)</a>.</p>
    """
    out = render_page(
        page_title="JavaScript: программирование в браузере",
        description="JavaScript как язык программирования, стандарт ECMAScript, DOM и Web API, события, проверка форм и fetch().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("JavaScript", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="JavaScript: программирование в браузере",
        lede="Язык программирования, который в браузере отвечает за поведение страницы: реакцию на действия пользователя и изменение содержимого.",
        body_html=body,
        sidebar_groups=sidebar("22-04-javascript.html"),
        nav=PageNav(prev_href="22-03-css.html", prev_label="CSS: оформление и расположение элементов веб-страницы", next_href="22-05-flask.html", next_label="Первое веб-приложение на Flask"),
    )
    write("22-04-javascript.html", out)


def build_05() -> None:
    body = f"""
    <p><strong>Flask</strong> — лёгкий веб-фреймворк для создания веб-приложений на языке
    Python. Он предоставляет маршрутизацию, объекты запроса и ответа, работу с шаблонами Jinja
    и другие базовые средства, необходимые серверному приложению. Сам Flask не принимает
    сетевые соединения напрямую — этим занимается отдельный сервер (раздел 22.19 объясняет эту
    границу подробнее); при локальном запуске Flask временно берёт эту роль на себя через
    встроенный сервер разработки Werkzeug. Установка — как у любой библиотеки:</p>
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
        "Строчка над функцией — <strong>декоратор</strong> (глава 15 показывала похожую идею). "
        "<code class=\"inline\">@app.route(\"/\")</code> регистрирует маршрут: связывает адрес "
        "<code class=\"inline\">/</code> с функцией <code class=\"inline\">glavnaya()</code>, "
        "которая обрабатывает запрос к этому адресу и формирует ответ. Этот механизм подробно "
        "рассматривается в разделе 22.11.",
    )}

    <h2>Шаблоны — HTML с выражениями Jinja</h2>
    <p>Возвращать HTML прямо строкой в Python неудобно. Flask использует движок шаблонов
    <strong>Jinja</strong> (раздел 22.12 рассматривает его подробно) — это отдельный язык
    шаблонов со своим синтаксисом: обычный HTML-файл, куда можно вставлять выражения и
    управляющие конструкции Jinja в фигурных скобках
    <code class="inline">{{{{ }}}}</code>:</p>
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
    <p>Часть адреса можно превратить в параметр маршрута — Flask передаёт его значение
    аргументом функции-обработчика:</p>
    {code_block(
        "dinamicheskij_marshrut.py",
        '@app.route("/privet/<imya>")\n'
        "def privet(imya):\n"
        '    return render_template("privet.html", imya=imya)\n',
    )}
    {callout(
        "info",
        "/privet/Сергей → imya = \"Сергей\"",
        "Открыв в браузере адрес <code class=\"inline\">/privet/Сергей</code>, вы получите в "
        "переменной <code class=\"inline\">imya</code> строку <code class=\"inline\">"
        "\"Сергей\"</code> — эту часть адреса Flask передаёт функции-обработчику как аргумент.",
    )}

    {image_figure(
        f"{IMG}/06-flask-privet.png",
        "Страница в браузере: заголовок «Привет, Ада!» и ссылка «Назад к списку задач»",
        "Итоговый проект использует именно этот маршрут: адрес /privet/Ада в браузере — и Flask подставляет имя из URL в шаблон.",
        width=420,
    )}

    <h2>Принимаем данные из формы</h2>
    <p>Чтобы пользователь мог что-то отправить на сервер (например, добавить задачу),
    используется HTML-форма и маршрут, принимающий метод <code class="inline">POST</code>
    (почему именно POST, а не GET — в разделе 22.13):</p>
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

    <h2>Готовый мини-сайт «Список задач»</h2>
    <p>Маршруты, шаблоны, форма и статический CSS-файл из этого раздела собраны в готовый
    мини-сайт «Список задач»:</p>
    <p>[[icon:file]] <a href="../../../projects/flask/todo-app/app.py">projects/flask/todo-app/app.py</a></p>
    {callout(
        "tip",
        "Запустите сайт у себя",
        "<code class=\"inline\">python app.py</code> в терминале внутри "
        "<code class=\"inline\">projects/flask/todo-app/</code>, затем откройте "
        "<code class=\"inline\">http://127.0.0.1:5000/</code> в браузере. Так запускается "
        "сервер разработки; чем он отличается от рабочего развёртывания — в разделе 22.34.",
    )}

    <p>Сейчас задачи хранятся в обычном списке Python и исчезают при перезапуске программы —
    почему это проблема, объясняет раздел 22.20, а разделы 22.20-22.29 постепенно заменят
    список на базу данных SQLite.</p>

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
        page_title="Первое веб-приложение на Flask",
        description="Первое Flask-приложение: маршруты, шаблоны Jinja, динамические адреса и приём данных из формы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Первое приложение на Flask", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Первое веб-приложение на Flask",
        lede="Flask — лёгкий веб-фреймворк для создания веб-приложений на Python.",
        body_html=body,
        sidebar_groups=sidebar("22-05-flask.html"),
        nav=PageNav(prev_href="22-04-javascript.html", prev_label="JavaScript: программирование в браузере", next_href="22-06-itogi.html", next_label="Итоги первого веб-проекта"),
    )
    write("22-05-flask.html", out)


def build_06() -> None:
    body = f"""
    {summary_box("Что мы узнали в этой части главы", [
        "Сайт — это диалог по протоколу HTTP: браузер (клиент) отправляет запрос, "
        "сервер отвечает.",
        "Фронтенд (то, что видит пользователь) строится из трёх языков: HTML "
        "(структура), CSS (оформление) и JavaScript (поведение).",
        "Бэкенд — программа на сервере, которая готовит ответы. На Python для этого "
        "часто используют библиотеку Flask.",
        "<code class=\"inline\">@app.route(\"/адрес\")</code> связывает адрес с функцией, "
        "которая на него отвечает.",
        "Шаблоны Jinja позволяют вставлять данные Python прямо в HTML через "
        "<code class=\"inline\">{{ }}</code> и <code class=\"inline\">{% %}</code>.",
        "Формы с методом POST и <code class=\"inline\">request.form</code> позволяют "
        "принимать данные, которые пользователь ввёл в браузере.",
    ])}

    <p>На этом заканчивается исторический печатный раздел главы — но не сама глава. Список
    задач пока хранится в обычном списке Python и исчезает при каждом перезапуске: страница
    полностью рабочая, но данные в ней не переживают перезапуск программы. Цифровое издание
    книги продолжает ту же тему дальше: как устроен путь запроса до сервера и
    обратно, как устроены HTTP и HTTPS, как связать Flask с базой данных
    и как проверить готовое приложение тестами — начиная с раздела 22.7 в боковом меню.</p>
    """
    out = render_page(
        page_title="Итоги первого веб-проекта",
        description="Итоги печатного раздела главы 22 и переход к цифровому продолжению: HTTP, базы данных, тесты и итоговый проект.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Итоги проекта", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Итоги первого веб-проекта",
        lede="От HTTP-запроса до собственного сайта на Flask — и продолжение впереди, в цифровом издании главы.",
        body_html=body,
        sidebar_groups=sidebar("22-06-itogi.html"),
        nav=PageNav(prev_href="22-05-flask.html", prev_label="Первое веб-приложение на Flask", next_href="22-07-put-zaprosa.html", next_label="Как браузер получает веб-страницу"),
    )
    write("22-06-itogi.html", out)


def build_07() -> None:
    body = f"""
    <p>Раздел 22.1 показал общую картину: браузер отправляет запрос, сервер отвечает. Теперь
    разберём этот путь по шагам — что в точности происходит между нажатием Enter в адресной
    строке и появлением страницы на экране.</p>

    {pipeline_diagram([
        {"kind": "plain", "title": "URL", "rows": ["адрес в строке браузера"]},
        {"kind": "plain", "title": "DNS", "rows": ["домен → IP-адрес"]},
        {"kind": "plain", "title": "Соединение", "rows": ["браузер связывается с сервером по IP"]},
        {"kind": "plain", "title": "HTTP-запрос", "rows": ["браузер посылает запрос"]},
        {"kind": "plain", "title": "Приложение", "rows": ["сервер готовит ответ"]},
        {"kind": "plain", "title": "HTTP-ответ", "rows": ["ответ возвращается браузеру"]},
        {"kind": "plain", "title": "Отрисовка", "rows": ["браузер показывает страницу"]},
    ], caption="Путь от адресной строки до готовой страницы на экране")}

    <h2>DNS: как доменное имя связывается с сетевыми адресами</h2>
    <p>Домен вроде <code class="inline">python.org</code> удобен человеку, но компьютеры в
    интернете находят друг друга по числовым <strong>IP-адресам</strong>. Служба
    <strong>DNS</strong> (Domain Name System — система доменных имён) хранит соответствия
    между доменами и записями, которые помогают найти нужный сервер, и превращает домен в
    IP-адрес прежде, чем браузер сможет отправить запрос.</p>

    {callout(
        "warning",
        "Один домен — не обязательно один постоянный IP-адрес",
        "У крупных сайтов один и тот же домен на практике может отвечать разными IP-адресами "
        "в разное время или в разных регионах — например, чтобы распределять нагрузку между "
        "несколькими серверами или ускорить доставку данных пользователям в разных частях "
        "света. Модель «один домен — ровно один сервер навсегда» верна только для самых "
        "простых случаев.",
    )}

    <h2>Соединение и запрос</h2>
    <p>Получив IP-адрес, браузер устанавливает соединение с сервером и отправляет
    <strong>HTTP-запрос</strong> — его устройство подробно рассматривается в разделе 22.9.
    Сервер (в нашем случае — приложение на Flask) обрабатывает запрос и отправляет
    <strong>HTTP-ответ</strong>: обычно HTML-страницу, но иногда — данные в формате JSON
    (раздел 22.15), изображение или файл.</p>

    <h2>Отрисовка</h2>
    <p>Получив ответ, браузер разбирает HTML и строит из него дерево DOM (раздел 22.4). По мере
    разбора он находит ссылки на CSS и JavaScript и запрашивает их отдельными HTTP-запросами
    (раздел 22.14); отображение страницы при этом может обновляться постепенно, по мере
    получения нужных данных, а не только после того, как загрузится буквально всё.</p>

    {callout(
        "info",
        "Мы намеренно не разбираем TCP/IP на уровне пакетов",
        "У соединения между браузером и сервером есть более глубокие технические уровни — "
        "разбиение данных на пакеты, подтверждение доставки и так далее. Для веб-разработки "
        "на уровне этой главы достаточно мысленной модели «браузер посылает запрос — сервер "
        "отвечает»; сетевые протоколы этого уровня — тема отдельного курса.",
    )}
    """
    out = render_page(
        page_title="Как браузер получает веб-страницу",
        description="Путь от ввода адреса до готовой страницы: URL, DNS, соединение, HTTP-запрос и ответ, отрисовка в браузере.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Путь запроса", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Как браузер получает веб-страницу",
        lede="От нажатия Enter в адресной строке до готовой страницы на экране — путь одного запроса.",
        body_html=body,
        sidebar_groups=sidebar("22-07-put-zaprosa.html"),
        nav=PageNav(prev_href="22-06-itogi.html", prev_label="Итоги первого веб-проекта", next_href="22-08-url-anatomiya.html", next_label="URL: домен, путь, параметры и фрагмент"),
    )
    write("22-07-put-zaprosa.html", out)


def build_08() -> None:
    body = f"""
    <p>URL (Uniform Resource Locator — единый указатель ресурса) — это полный адрес чего-то в
    вебе: страницы, изображения, API-ответа. У него есть чёткая структура, и каждая часть
    отвечает за своё:</p>

    {path_anatomy_diagram(
        "https://example.com:443/products/42?sort=price#details",
        [
            ("схема", "https"),
            ("хост (домен)", "example.com"),
            ("порт", "443"),
            ("путь", "/products/42"),
            ("строка запроса", "?sort=price"),
            ("фрагмент", "#details"),
        ],
        caption="Разбор одного URL по частям",
    )}

    {comparison_table(
        ["Часть", "Значение в примере", "За что отвечает"],
        [
            ["Схема", "https", "Каким протоколом пользоваться (раздел 22.10)"],
            ["Хост (домен)", "example.com", "К какому серверу обращаться"],
            ["Порт", "443", "Номер сетевого порта, к которому выполняется подключение — часто не пишется явно, потому что у схемы есть порт по умолчанию"],
            ["Путь", "/products/42", "Какой ресурс на сервере нужен"],
            ["Строка запроса", "?sort=price", "Дополнительные параметры в формате ключ=значение"],
            ["Фрагмент", "#details", "Место внутри самой страницы"],
        ],
    )}

    {callout(
        "warning",
        "Фрагмент не уходит на сервер",
        "Часть адреса после <code class=\"inline\">#</code> обрабатывает сам браузер — обычно "
        "чтобы прокрутить страницу к элементу с таким идентификатором. Она не передаётся на "
        "сервер как часть HTTP-запроса: сервер, ответивший на "
        "<code class=\"inline\">/products/42?sort=price#details</code>, физически не видит "
        "<code class=\"inline\">#details</code> — он получает запрос только на "
        "<code class=\"inline\">/products/42?sort=price</code>.",
    )}

    <h2>Строка запроса — несколько параметров</h2>
    <p>После <code class="inline">?</code> параметры перечисляются через
    <code class="inline">&amp;</code>: <code class="inline">?sort=price&amp;page=2</code> —
    два параметра, <code class="inline">sort</code> и <code class="inline">page</code>. Flask
    читает их через <code class="inline">request.args</code>:</p>
    {code_block(
        "query_params.py",
        '@app.route("/tovary")\n'
        "def tovary():\n"
        '    sortirovka = request.args.get("sort", "name")\n'
        "    return f\"Сортировка: {{sortirovka}}\"\n",
    )}

    {practice_card(
        "22-08",
        "Практика: разбор URL",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-08/index.html",
    )}
    """
    out = render_page(
        page_title="URL: домен, путь, параметры и фрагмент",
        description="Устройство URL по частям: схема, домен, порт, путь, строка запроса и фрагмент — и почему фрагмент не доходит до сервера.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Устройство URL", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="URL: домен, путь, параметры и фрагмент",
        lede="У каждого адреса в вебе есть чёткая структура — разберём её по частям на одном примере.",
        body_html=body,
        sidebar_groups=sidebar("22-08-url-anatomiya.html"),
        nav=PageNav(prev_href="22-07-put-zaprosa.html", prev_label="Как браузер получает веб-страницу", next_href="22-09-http.html", next_label="HTTP: запросы, ответы, методы и коды состояния"),
    )
    write("22-08-url-anatomiya.html", out)


def build_09() -> None:
    body = f"""
    <p><strong>HTTP</strong> (HyperText Transfer Protocol) — прикладной протокол обмена
    сообщениями между клиентом и сервером в вебе: он задаёт общий набор правил, по которым
    браузер и сервер обмениваются запросами и ответами. Каждое сообщение — запрос или ответ —
    состоит из похожих частей.</p>

    {comparison_table(
        ["HTTP-запрос", "HTTP-ответ"],
        [
            ["Метод: что нужно сделать (GET, POST…)", "Код состояния: как всё прошло (200, 404…)"],
            ["Путь: какой ресурс нужен", "Заголовки: метаданные ответа"],
            ["Заголовки: метаданные запроса", "Тело: содержимое — HTML, JSON, файл…"],
            ["Тело: необязательные данные (например, форма)", ""],
        ],
    )}

    <h2>Основные методы HTTP</h2>
    {comparison_table(
        ["Метод", "Обычный смысл"],
        [
            ["GET", "Получить данные — открыть страницу, посмотреть список"],
            ["POST", "Отправить новые данные — добавить задачу, отправить форму"],
            ["PUT", "Полностью заменить существующий ресурс"],
            ["PATCH", "Частично изменить существующий ресурс"],
            ["DELETE", "Удалить ресурс"],
        ],
    )}
    <p>Это распространённые соглашения, а не физический закон: ни один из методов не
    заставляет сервер вести себя определённым образом — Flask выполнит любой код, какой вы
    напишете в обработчике, независимо от метода. Но следование этим соглашениям делает
    приложение понятным для других разработчиков и для инструментов вроде браузерного кеша.
    Не каждое приложение использует все пять методов — маленький сайт вполне может обойтись
    только GET и POST, как в разделе 22.5.</p>

    {callout(
        "warning",
        "GET не «безопаснее» POST — и наоборот",
        "GET и POST не отличаются по защите передаваемых данных: это определяет протокол "
        "(HTTP или HTTPS, раздел 22.10), а не метод. Разница в другом: по определению HTTP "
        "GET предназначен для получения данных и не должен вызывать побочные изменения на "
        "сервере — именно на этом основано поведение браузеров, кеширующих прокси и других "
        "инструментов, которые считают GET безопасным для повтора: обновление страницы или "
        "добавление в закладки не должно ничего менять. Поэтому удаление задачи через "
        "GET-ссылку — плохая идея (правильный вариант показывает раздел 22.35): случайное "
        "обновление страницы браузером не должно ничего удалять.",
    )}

    <h2>Коды состояния: как прошёл запрос</h2>
    {comparison_table(
        ["Диапазон", "Смысл", "Примеры"],
        [
            ["2xx", "Успех", "200 OK, 201 Created"],
            ["3xx", "Перенаправление", "302 Found, 303 See Other — «ресурс нужно смотреть по другому адресу»"],
            ["4xx", "Ошибка клиента", "400 Bad Request, 404 Not Found"],
            ["5xx", "Ошибка сервера", "500 Internal Server Error"],
        ],
    )}
    <p>Раздел 22.13 показывает код 303 в деле — как часть паттерна POST-Redirect-GET, а раздел
    22.31 — коды 400 и 404 в обработке ошибок ввода.</p>

    <h2>Тело сообщения — не только HTML</h2>
    <p>Тело HTTP-ответа может содержать HTML-страницу, но так же легко — данные в формате JSON
    (раздел 22.15), изображение, CSS-файл, JavaScript-файл или любой другой файл. Именно
    заголовок <code class="inline">Content-Type</code> сообщает браузеру, как понимать тело
    ответа — <code class="inline">text/html</code>, <code class="inline">application/json</code>,
    <code class="inline">image/png</code> и так далее.</p>

    {practice_card(
        "22-09",
        "Практика: классификация кодов состояния",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-09/index.html",
    )}
    """
    out = render_page(
        page_title="HTTP: запросы, ответы, методы и коды состояния",
        description="Из чего состоят HTTP-запрос и ответ, что означают методы GET/POST/PUT/PATCH/DELETE и группы кодов состояния 2xx-5xx.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("HTTP", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="HTTP: запросы, ответы, методы и коды состояния",
        lede="Общий набор правил, по которым браузер и сервер обмениваются сообщениями.",
        body_html=body,
        sidebar_groups=sidebar("22-09-http.html"),
        nav=PageNav(prev_href="22-08-url-anatomiya.html", prev_label="URL: домен, путь, параметры и фрагмент", next_href="22-10-https.html", next_label="HTTPS: защита соединения с сайтом"),
    )
    write("22-09-http.html", out)


def build_10() -> None:
    body = f"""
    <p><strong>HTTPS</strong> — использование протокола HTTP поверх TLS (Transport Layer
    Security): те же сообщения запрос-ответ, но соединение, по которому они передаются,
    защищено. Это важно, потому что обычный HTTP-запрос идёт по сети без транспортного
    шифрования: любой, кто технически способен перехватить трафик между браузером и сервером
    (например, в общей Wi-Fi сети), может его прочитать или незаметно изменить.</p>

    {comparison_table(
        ["", "HTTP", "HTTPS"],
        [
            ["Данные в пути", "Без шифрования", "Зашифрованы"],
            ["Можно ли перехватить и прочитать", "Да, технически возможно", "Практически нет — без ключа шифрования содержимое нечитаемо"],
            ["Можно ли незаметно подменить данные в пути", "Да", "Нет — подмена нарушает проверку целостности, и соединение считается недействительным"],
            ["Подтверждение личности сервера", "Нет", "Сертификат подтверждает, что сервер — тот, за кого себя выдаёт"],
        ],
    )}

    <p>TLS решает три задачи: <strong>конфиденциальность</strong> (данные в пути нечитаемы для
    посторонних), <strong>целостность</strong> (получатель может обнаружить, что данные были
    изменены в пути) и <strong>подлинность сервера</strong> (сертификат подтверждает, что вы
    говорите именно с тем сервером, а не с подменённым).</p>

    {callout(
        "warning",
        "HTTPS защищает канал, а не само приложение",
        "HTTPS не делает сайт «безопасным» в широком смысле. Он защищает данные "
        "<em>по пути</em> между браузером и сервером — но если в самом приложении есть ошибка "
        "(например, SQL-инъекция — раздел 22.32), HTTPS её никак не устраняет: данные "
        "доедут до сервера в целости и там же будут неправильно обработаны. Это разные слои "
        "защиты, и один не заменяет другой.",
    )}

    <p>Мы намеренно не разбираем математику шифрования — для веб-разработки на уровне этой
    главы достаточно знать, зачем HTTPS нужен и что именно он защищает. В разработке локально
    (раздел 22.34) чаще всего используют обычный HTTP на своём компьютере — шифровать канал
    внутри одной машины не требуется; HTTPS становится нужен, когда приложение реально
    развёрнуто и доступно через интернет.</p>
    """
    out = render_page(
        page_title="HTTPS: защита соединения с сайтом",
        description="Что именно защищает HTTPS: конфиденциальность, целостность данных в пути и подтверждение подлинности сервера — и чего он не защищает.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("HTTPS", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="HTTPS: защита соединения с сайтом",
        lede="HTTPS защищает канал между браузером и сервером — но не заменяет безопасность самого приложения.",
        body_html=body,
        sidebar_groups=sidebar("22-10-https.html"),
        nav=PageNav(prev_href="22-09-http.html", prev_label="HTTP: запросы, ответы, методы и коды состояния", next_href="22-11-flask-marshrutizaciya.html", next_label="Маршрутизация во Flask: URL и функции-обработчики"),
    )
    write("22-10-https.html", out)


def build_11() -> None:
    body = f"""
    <p>Раздел 22.5 уже показал <code class="inline">@app.route("/")</code> — но что именно
    Flask делает с этим декоратором? Разберём весь путь одного запроса внутри приложения.</p>

    {pipeline_diagram([
        {"kind": "plain", "title": "GET /task/42", "rows": ["HTTP-запрос от браузера"]},
        {"kind": "plain", "title": "Маршрутизатор Flask", "rows": ["ищет подходящее правило"]},
        {"kind": "plain", "title": "Функция-обработчик", "rows": ["view function"]},
        {"kind": "plain", "title": "Шаблон или данные", "rows": ["строится содержимое ответа"]},
        {"kind": "plain", "title": "HTTP-ответ", "rows": ["возвращается браузеру"]},
    ], caption="Путь одного запроса внутри Flask-приложения")}

    <p>Каждый вызов <code class="inline">@app.route(...)</code> регистрирует
    <strong>правило</strong> (URL rule) — сам шаблон пути, например
    <code class="inline">/task/&lt;int:task_id&gt;</code>. Совокупность всех правил называют
    <strong>маршрутизацией</strong> (routing). У каждого правила есть также
    <strong>эндпоинт</strong> (endpoint) — символическое имя, под которым Flask знает связанную
    функцию: по умолчанию это имя самой функции. Именно по эндпоинту, а не по URL напрямую,
    <code class="inline">url_for(...)</code> строит адрес — это и позволяет менять сам путь, не
    трогая код, который на него ссылается. Когда приходит запрос, Flask ищет среди
    зарегистрированных правил подходящее по пути и методу и вызывает связанную с ним
    <strong>функцию-обработчик</strong> — вы уже видели этот механизм в разделе 22.5, просто
    без названий.</p>

    <h2>Параметр пути — типизированная часть URL</h2>
    <p>Часть пути в угловых скобках Flask передаёт в функцию как аргумент. Можно указать её
    ожидаемый тип прямо в правиле:</p>
    {code_block(
        "path_param.py",
        '@app.route("/task/<int:task_id>")\n'
        "def poluchit_zadachu(task_id):\n"
        '    return f"Задача №{{task_id}}"\n',
    )}
    {callout(
        "info",
        "<int:task_id> — нечисловой адрес отклоняется до вызова функции",
        "Если открыть <code class=\"inline\">/task/abc</code>, Flask не вызовет "
        "<code class=\"inline\">poluchit_zadachu()</code> вообще — правило "
        "<code class=\"inline\">&lt;int:task_id&gt;</code> требует целое число, и запрос "
        "получит стандартный ответ 404 (раздел 22.9) прежде, чем дойдёт до вашего кода.",
    )}

    <h2>Функция-обработчик возвращает содержимое ответа</h2>
    <p>То, что возвращает функция, становится телом HTTP-ответа: строка, отрендеренный шаблон
    (раздел 22.12) или, например, словарь — такой словарь Flask преобразует в JSON (раздел
    22.15-22.16). Именно поэтому обработчики называют <em>функциями представления</em> (view
    functions): их задача — подготовить представление данных для конкретного запроса.</p>

    {practice_card(
        "22-11",
        "Практика: маршруты и параметры пути",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-11/index.html",
    )}
    """
    out = render_page(
        page_title="Маршрутизация во Flask: URL и функции-обработчики",
        description="URL-правила, эндпоинты, типизированные параметры пути и то, что именно функция-обработчик возвращает в ответ.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Маршрутизация Flask", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Маршрутизация во Flask: URL и функции-обработчики",
        lede="От HTTP-запроса до вызова нужной функции — устройство маршрутизации Flask.",
        body_html=body,
        sidebar_groups=sidebar("22-11-flask-marshrutizaciya.html"),
        nav=PageNav(prev_href="22-10-https.html", prev_label="HTTPS: защита соединения с сайтом", next_href="22-12-jinja-shablony.html", next_label="Jinja: шаблоны HTML с данными"),
    )
    write("22-11-flask-marshrutizaciya.html", out)


def build_12() -> None:
    body = f"""
    <p>Раздел 22.5 уже использовал шаблоны — теперь разберём, как устроен движок
    <strong>Jinja</strong>, который Flask использует по умолчанию. Шаблон — обычный
    HTML-файл, куда вставлены два вида конструкций: <code class="inline">{{{{ выражение }}}}</code>
    (вывести значение) и <code class="inline">{{% команда %}}</code> (условие, цикл,
    наследование).</p>

    {code_block(
        "templates/spisok.html",
        '<ul>\n'
        '  {% for zadacha in zadachi %}\n'
        '    <li>{{ zadacha.title }}</li>\n'
        '  {% endfor %}\n'
        '</ul>\n\n'
        '{% if not zadachi %}\n'
        '  <p>Задач пока нет.</p>\n'
        '{% endif %}',
        lang="html",
    )}

    <h2>Автоэкранирование — Jinja защищает вас по умолчанию</h2>
    <p>Если значение, которое вставляет <code class="inline">{{{{ }}}}</code>, содержит
    HTML-разметку (например, пользователь ввёл в поле <code class="inline">&lt;b&gt;</code>),
    Jinja по умолчанию экранирует специальные символы — превращает
    <code class="inline">&lt;</code> в <code class="inline">&amp;lt;</code> и так далее.
    Браузер покажет это как обычный текст, а не выполнит как разметку. Это называют
    <strong>автоэкранированием</strong> (autoescaping), и оно включено для HTML-шаблонов
    Flask по умолчанию.</p>

    {callout(
        "warning",
        "|safe отключает именно эту защиту",
        "У Jinja есть фильтр <code class=\"inline\">|safe</code>, который отключает "
        "автоэкранирование для конкретного значения — Jinja вставит его как есть, включая "
        "любую разметку. Это уместно для текста, который вы полностью контролируете сами "
        "(например, HTML, зашитый в код приложения), но <strong>не для данных, которые ввёл "
        "пользователь</strong>: к чему это приводит на практике, показывает раздел 22.32. Если "
        "сомневаетесь — не добавляйте <code class=\"inline\">|safe</code>.",
    )}

    <h2>Наследование шаблонов — общий каркас страницы</h2>
    <p>Чтобы не повторять <code class="inline">&lt;head&gt;</code>, навигацию и подключение
    CSS в каждом шаблоне, заводят базовый шаблон с именованными блоками, которые заполняют
    дочерние шаблоны:</p>
    {code_block(
        "templates/base.html",
        '<!doctype html>\n'
        '<html lang="ru">\n'
        '<head>\n'
        '  <meta charset="utf-8">\n'
        '  <title>{% block title %}Список задач{% endblock %}</title>\n'
        '  <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">\n'
        '</head>\n'
        '<body>\n'
        '  {% block content %}{% endblock %}\n'
        '</body>\n'
        '</html>',
        lang="html",
    )}
    {code_block(
        "templates/index.html",
        '{% extends "base.html" %}\n\n'
        '{% block content %}\n'
        '  <h1>Мой список задач</h1>\n'
        '  ...\n'
        '{% endblock %}',
        lang="html",
    )}
    <p><code class="inline">{{% extends "base.html" %}}</code> говорит: «возьми базовый
    шаблон и подставь моё содержимое в отмеченные блоки». Итоговый проект главы (раздел 22.35)
    использует именно эту структуру — <code class="inline">base.html</code> и несколько
    дочерних шаблонов.</p>

    {local_required_card(
        "22-12",
        "Практика: шаблоны и автоэкранирование",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-12/index.html",
    )}
    """
    out = render_page(
        page_title="Jinja: шаблоны HTML с данными",
        description="Выражения и команды Jinja, автоэкранирование по умолчанию, риск фильтра |safe и наследование шаблонов через extends/block.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Шаблоны Jinja", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Jinja: шаблоны HTML с данными",
        lede="HTML-шаблон с выражениями Jinja и данными из Python — и встроенная защита от случайно выполненной разметки.",
        body_html=body,
        sidebar_groups=sidebar("22-12-jinja-shablony.html"),
        nav=PageNav(prev_href="22-11-flask-marshrutizaciya.html", prev_label="Маршрутизация во Flask: URL и функции-обработчики", next_href="22-13-formy.html", next_label="HTML-формы и отправка данных на сервер"),
    )
    write("22-12-jinja-shablony.html", out)


def build_13() -> None:
    body = f"""
    <p>Раздел 22.2 показал HTML-форму, раздел 22.5 — маршрут, который её принимает. Теперь
    разберём этот путь целиком, с одной важной деталью: что делать <em>после</em> того, как
    форма обработана.</p>

    {code_block(
        "templates/forma.html",
        '<form action="{{ url_for(\'dobavit\') }}" method="post">\n'
        '  <label for="zadacha">Новая задача</label>\n'
        '  <input type="text" id="zadacha" name="zadacha" required>\n'
        '  <button type="submit">Добавить</button>\n'
        '</form>',
        lang="html",
    )}
    <p><code class="inline">method="post"</code> говорит браузеру отправить данные формы как
    тело POST-запроса, а не как часть адреса. Атрибут <code class="inline">name="zadacha"</code>
    у поля определяет ключ, под которым значение придёт на сервер.</p>

    {code_block(
        "app.py",
        '@app.route("/dobavit", methods=["POST"])\n'
        "def dobavit():\n"
        '    novaya_zadacha = request.form.get("zadacha", "").strip()\n'
        "    if novaya_zadacha:\n"
        "        zadachi.append(novaya_zadacha)\n"
        '    return redirect(url_for("glavnaya"), code=303)\n',
    )}
    <p><code class="inline">request.form.get("zadacha", "")</code> достаёт значение поля по
    имени; второй аргумент — что вернуть, если поля вообще не было. Какие ещё проверки стоит
    добавить перед тем, как сохранять введённое значение — в разделе 22.31.</p>

    <h2>POST-Redirect-GET — зачем нужен redirect в конце</h2>
    <p>Обработчик формы заканчивается не отрисовкой страницы, а
    <code class="inline">redirect(url_for("glavnaya"), code=303)</code> — HTTP-ответом с кодом
    303 See Other (раздел 22.9), который сообщает браузеру адрес, откуда нужно запросить
    результат методом GET. Браузер выполняет второй, уже безопасный запрос и показывает
    страницу.</p>

    {pipeline_diagram([
        {"kind": "plain", "title": "Браузер", "rows": ["POST /dobavit", "с данными формы"]},
        {"kind": "plain", "title": "Flask", "rows": ["сохраняет задачу", "303 See Other, Location: /"]},
        {"kind": "plain", "title": "Браузер", "rows": ["GET /", "уже без формы"]},
        {"kind": "plain", "title": "Flask", "rows": ["показывает список"]},
    ], caption="POST-Redirect-GET: два отдельных запроса вместо одного")}

    {callout(
        "warning",
        "Без redirect повторная отправка дублирует данные",
        "Если обработчик POST-запроса сразу возвращает готовую страницу (а не делает "
        "redirect), браузер связывает уже показанную страницу именно с этим POST-запросом — и "
        "обновление страницы (F5) отправит форму ещё раз, молча продублировав задачу. "
        "Redirect гарантирует, что после ответа сервера текущей операцией браузера окажется "
        "безопасный GET, который можно повторять сколько угодно.",
    )}

    {local_required_card(
        "22-13",
        "Практика: форма и POST-Redirect-GET",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-13/index.html",
    )}
    """
    out = render_page(
        page_title="HTML-формы и отправка данных на сервер",
        description="Метод POST, request.form и паттерн POST-Redirect-GET — почему обработчик формы заканчивается редиректом, а не страницей.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Формы", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="HTML-формы и отправка данных на сервер",
        lede="От HTML-формы до сохранённых данных — и почему после сохранения нужен ещё один запрос.",
        body_html=body,
        sidebar_groups=sidebar("22-13-formy.html"),
        nav=PageNav(prev_href="22-12-jinja-shablony.html", prev_label="Jinja: шаблоны HTML с данными", next_href="22-14-staticheskie-fajly.html", next_label="Статические файлы: CSS, изображения и JavaScript"),
    )
    write("22-13-formy.html", out)


def build_14() -> None:
    body = f"""
    <p>Открывая страницу со стилями, браузер на самом деле делает несколько отдельных
    HTTP-запросов: один за HTML, ещё по одному — за каждый CSS-файл, изображение и
    JavaScript-файл, на которые страница ссылается. Такие файлы называют
    <strong>статическими</strong>: сервер отдаёт их без изменений, в отличие от HTML, который
    Jinja рендерит заново для каждого запроса.</p>

    {flow_diagram([
        ("GET /", "запрос HTML-страницы"),
        ("GET /static/style.css", "отдельный запрос за CSS"),
        ("GET /static/logo.png", "отдельный запрос за картинкой"),
    ], caption="Одна страница — несколько независимых HTTP-запросов")}

    <p>Flask по умолчанию ожидает статические файлы в папке <code class="inline">static/</code>
    рядом с приложением и отдаёт их по адресам вида
    <code class="inline">/static/имя_файла</code>:</p>
    {code_block(
        "struktura_proekta.txt",
        "todo-app/\n"
        "  app.py\n"
        "  templates/\n"
        "    base.html\n"
        "  static/\n"
        "    style.css\n",
        lang="text",
    )}
    <p>Адрес статического файла удобнее не прописывать в шаблоне вручную, а получать через
    <code class="inline">url_for('static', filename='style.css')</code> — эта функция строит
    URL на основе конфигурации маршрутизации Flask, а не просто склеивает строку. Это заодно
    избавляет от лишней работы, если структура папок когда-нибудь изменится:</p>
    {code_block(
        "templates/base.html",
        '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">',
        lang="html",
    )}

    {callout(
        "info",
        "templates/ и static/ — разные папки, разные роли",
        "<code class=\"inline\">templates/</code> хранит файлы, которые Jinja рендерит заново "
        "под каждый запрос, подставляя в них данные из Python. "
        "<code class=\"inline\">static/</code> хранит готовые файлы, которые отдаются как "
        "есть, без обработки, — CSS, изображения, JavaScript, шрифты.",
    )}
    """
    out = render_page(
        page_title="Статические файлы: CSS, изображения и JavaScript",
        description="Почему CSS, изображения и JavaScript запрашиваются отдельными HTTP-запросами, и как Flask отдаёт файлы из папки static/.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Статические файлы", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Статические файлы: CSS, изображения и JavaScript",
        lede="Одна страница — несколько независимых запросов: HTML собирается заново, статика отдаётся как есть.",
        body_html=body,
        sidebar_groups=sidebar("22-14-staticheskie-fajly.html"),
        nav=PageNav(prev_href="22-13-formy.html", prev_label="HTML-формы и отправка данных на сервер", next_href="22-15-json.html", next_label="JSON: формат обмена данными"),
    )
    write("22-14-staticheskie-fajly.html", out)


def build_15() -> None:
    body = f"""
    <p><strong>JSON</strong> (JavaScript Object Notation) — текстовый формат для передачи
    структурированных данных между программами. Название напоминает про JavaScript, но JSON
    давно используется программами на любых языках, включая Python, — это просто текстовый
    формат, а не код, который где-то выполняется.</p>

    {comparison_table(
        ["Значение JSON", "Соответствие в Python"],
        [
            ["объект <code class=\"inline\">{{\"ключ\": значение}}</code>", "<code class=\"inline\">dict</code>"],
            ["массив <code class=\"inline\">[1, 2, 3]</code>", "<code class=\"inline\">list</code>"],
            ["строка <code class=\"inline\">\"текст\"</code>", "<code class=\"inline\">str</code>"],
            ["число <code class=\"inline\">42</code> / <code class=\"inline\">3.14</code>", "<code class=\"inline\">int</code> / <code class=\"inline\">float</code>"],
            ["<code class=\"inline\">true</code> / <code class=\"inline\">false</code>", "<code class=\"inline\">True</code> / <code class=\"inline\">False</code>"],
            ["<code class=\"inline\">null</code>", "<code class=\"inline\">None</code>"],
        ],
    )}

    {callout(
        "warning",
        "JSON — не то же самое, что запись словаря Python",
        "У JSON строгий синтаксис: ключи и строковые значения обязаны быть в двойных "
        "кавычках. <code class=\"inline\">{{'name': 'Ada'}}</code> — это распечатка словаря "
        "Python, а не JSON: в корректном JSON она выглядит как "
        "<code class=\"inline\">{{\"name\": \"Ada\"}}</code>. Одинарные кавычки, "
        "<code class=\"inline\">True</code> с большой буквы, завершающая запятая перед "
        "закрывающей скобкой — всё это ломает JSON, даже если выглядит почти правильно.",
    )}

    <h2>Модуль json — стандартная библиотека Python</h2>
    {code_block(
        "json_primer.py",
        'import json\n\n'
        'zadacha = {{"title": "Купить хлеб", "done": False}}\n\n'
        '# Python -> текст JSON\n'
        'tekst = json.dumps(zadacha, ensure_ascii=False)\n'
        'print(tekst)   # {{"title": "Купить хлеб", "done": false}}\n\n'
        '# текст JSON -> Python\n'
        'obratno = json.loads(tekst)\n'
        'print(obratno["title"])   # Купить хлеб\n',
    )}
    {callout(
        "info",
        "ensure_ascii=False — чтобы кириллица оставалась кириллицей",
        "По умолчанию <code class=\"inline\">json.dumps()</code> заменяет все не-ASCII "
        "символы на escape-последовательности вроде <code class=\"inline\">\\u041a</code> — "
        "валидный, но нечитаемый для человека JSON. "
        "<code class=\"inline\">ensure_ascii=False</code> оставляет кириллицу как есть; "
        "результат остаётся тем же самым JSON, просто удобным для чтения.",
    )}

    <h2>Ограничения формата JSON</h2>
    <p>У формата нет отдельного типа для даты и времени — их обычно передают строкой в
    оговорённом формате (например, <code class="inline">"2026-08-23"</code>) и разбирают уже
    на своей стороне. Нет и типа для двоичных данных (изображение, файл) — их обычно кодируют
    в текст (например, Base64) или передают отдельным запросом. А ещё JSON не различает целые
    и вещественные числа так строго, как Python: очень большие или очень точные числа при
    передаче между разными языками программирования иногда требуют аккуратности.</p>

    {callout(
        "warning",
        "JSON — формат данных, а не база данных и не API сам по себе",
        "JSON описывает, <em>как записать</em> данные в виде текста. Он не хранит данные "
        "постоянно сам по себе (для этого нужна база данных — раздел 22.20) и не является "
        "программным интерфейсом сам по себе (для этого нужен код, который его обрабатывает "
        "— пример такого кода есть в разделе 22.16). JSON — распространённый текстовый формат "
        "обмена данными между разными частями системы.",
    )}

    {practice_card(
        "22-15",
        "Практика: преобразование данных между Python и JSON",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-15/index.html",
    )}
    """
    out = render_page(
        page_title="JSON: формат обмена данными",
        description="Соответствие типов JSON и Python, json.dumps()/json.loads(), ограничения формата и разница между JSON и Python-словарём.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("JSON", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="JSON: формат обмена данными",
        lede="Распространённый текстовый формат для структурированных данных, который понимают программы на разных языках.",
        body_html=body,
        sidebar_groups=sidebar("22-15-json.html"),
        nav=PageNav(prev_href="22-14-staticheskie-fajly.html", prev_label="Статические файлы: CSS, изображения и JavaScript", next_href="22-16-api.html", next_label="HTTP API: обмен данными между программами"),
    )
    write("22-15-json.html", out)


def build_16() -> None:
    body = f"""
    <p>До сих пор Flask-приложение отвечало HTML-страницами — их читает человек через браузер.
    Но у ответа сервера может быть и другой получатель: мобильное приложение, другой сервер
    или JavaScript-код на той же странице (раздел 22.4 уже показал
    <code class="inline">fetch()</code>). Такой ответ обычно приходит не в виде HTML, а в
    виде данных — чаще всего JSON.</p>

    <p>Программный интерфейс, через который одна программа получает данные от другой, называют
    <strong>API</strong> (Application Programming Interface — программный интерфейс
    приложения). Конкретный адрес внутри API тоже называют <strong>эндпоинтом</strong> — это
    более широкое, общеупотребительное значение слова, чем эндпоинт-имя маршрута Flask из
    раздела 22.11: там речь шла о внутреннем идентификаторе для <code class="inline">url_for()
    </code>, здесь — просто о конкретном URL, который отдаёт данные, а не HTML-страницу.</p>

    {comparison_table(
        ["", "Обычный маршрут", "API-эндпоинт"],
        [
            ["Кто читает ответ", "Человек через браузер", "Программа: JavaScript, приложение, другой сервер"],
            ["Формат ответа", "HTML", "Чаще всего JSON"],
            ["Content-Type ответа", "text/html", "application/json"],
        ],
    )}

    <h2>Маленький JSON-эндпоинт на Flask</h2>
    {code_block(
        "app.py",
        'from flask import jsonify\n\n'
        '@app.route("/api/tasks")\n'
        "def api_tasks():\n"
        '    return jsonify([{{"id": z["id"], "title": z["title"], "done": z["done"]}} for z in zadachi])\n',
    )}
    <p><code class="inline">jsonify(...)</code> делает две вещи сразу: превращает данные
    Python в текст JSON (как <code class="inline">json.dumps()</code> из раздела 22.15) и
    выставляет заголовок ответа <code class="inline">Content-Type: application/json</code>,
    чтобы получатель знал, как читать тело ответа.</p>

    {image_figure(
        f"{IMG}/07-api-tasks-json.png",
        "Ответ /api/tasks в браузере: массив JSON-объектов с полями done, id и title, кириллица в title показана как экранированные последовательности вида \\u0418",
        "Реальный ответ GET /api/tasks итогового проекта. Это валидный JSON — но по умолчанию jsonify() экранирует кириллицу в \\uXXXX-последовательности, ровно как описывал раздел 22.15 про json.dumps() без ensure_ascii=False.",
        width=520,
    )}

    {callout(
        "info",
        "REST — распространённый стиль, а не обязательный стандарт",
        "Многие API строят в стиле <strong>REST</strong> (Representational State Transfer): "
        "путь называет ресурс (<code class=\"inline\">/api/tasks</code>), а метод определяет "
        "действие над ним — GET получает список, POST создаёт новую запись. Это популярное и "
        "полезное соглашение, но не единственно возможный способ построить API — важно "
        "понимать сам принцип «данные вместо HTML», а не заучивать REST как жёсткое правило.",
    )}

    <p>Раздел 22.35 добавит такой эндпоинт в итоговый проект — GET /api/tasks, возвращающий
    текущий список задач в формате JSON.</p>

    {practice_card(
        "22-16",
        "Практика: форматируем данные для API-ответа",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-16/index.html",
    )}
    """
    out = render_page(
        page_title="HTTP API: обмен данными между программами",
        description="Что такое API и эндпоинт, зачем нужен jsonify() и что означает Content-Type: application/json.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("API", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="HTTP API: обмен данными между программами",
        lede="Тот же сервер, тот же Flask — но получатель ответа теперь другая программа, а не браузер человека.",
        body_html=body,
        sidebar_groups=sidebar("22-16-api.html"),
        nav=PageNav(prev_href="22-15-json.html", prev_label="JSON: формат обмена данными", next_href="22-17-veb-frejmvorki.html", next_label="Веб-фреймворки на Python: Flask, Django, FastAPI и другие"),
    )
    write("22-16-api.html", out)


def build_17() -> None:
    body = f"""
    <p><strong>Веб-фреймворк</strong> — набор библиотек, правил и готовых компонентов, которые
    упрощают создание веб-приложений: маршрутизацию, обработку HTTP-запросов и ответов, работу
    с шаблонами, проверку данных, доступ к базе данных и другие типичные задачи. Flask — не
    единственный веб-фреймворк для Python; у остальных другой набор встроенных возможностей.</p>

    {callout(
        "info",
        "Flask",
        "Flask — лёгкий WSGI-фреймворк для создания веб-приложений на Python (раздел 22.19). "
        "Его основное ядро сравнительно невелико, а дополнительные возможности обычно "
        "подключаются библиотеками и расширениями.",
    )}

    {callout(
        "info",
        "Django",
        "Django — полнофункциональный веб-фреймворк на Python. В его состав входят ORM, "
        "система миграций, маршрутизация, шаблоны, средства аутентификации и административный "
        "интерфейс.",
    )}

    {callout(
        "info",
        "FastAPI",
        "FastAPI — веб-фреймворк для создания HTTP API на Python. Он использует аннотации "
        "типов Python для описания и проверки данных и может автоматически формировать "
        "документацию API на основе OpenAPI.",
    )}

    {callout(
        "info",
        "Starlette",
        "Starlette — лёгкий ASGI-фреймворк и инструментарий для создания асинхронных "
        "веб-сервисов на Python. FastAPI использует Starlette как один из своих базовых "
        "компонентов.",
    )}

    <p>Каждый фреймворк берёт на себя часть типовой работы: маршрутизацию (кто отвечает за
    какой адрес — раздел 22.11), обработку запроса и ответа, иногда — шаблоны, проверку
    входных данных, работу с базой данных, авторизацию, инструменты для тестирования. Разница
    между фреймворками — в том, <em>сколько именно</em> он берёт на себя и насколько легко
    заменить любую из этих частей на свою.</p>

    <h2>Другие веб-фреймворки для Python</h2>
    <p>Кроме Flask, Django, FastAPI и Starlette, в веб-разработке на Python используются и
    другие проекты. Ни один из них не рассматривается в этой главе подробно — они упомянуты,
    чтобы вы узнавали названия, встретив их в реальных проектах.</p>

    {comparison_table(
        ["Фреймворк", "Основной фокус", "Интерфейс/модель", "Типичное применение"],
        [
            ["Litestar", "Производительность и строгая типизация", "ASGI", "API-сервисы, где важны типы и валидация"],
            ["Quart", "API, совместимый с Flask", "ASGI", "Перенос Flask-приложений на асинхронную модель"],
            ["Pyramid", "Гибкая архитектура без навязанной структуры", "WSGI", "Проекты, растущие от небольшого скрипта до крупного приложения"],
            ["Tornado", "Асинхронный ввод-вывод, долгоживущие соединения", "Собственный асинхронный движок + ASGI/WSGI-совместимость", "Веб-сокеты, длительные соединения"],
            ["Bottle", "Минимализм, один файл", "WSGI", "Совсем маленькие сервисы и прототипы"],
        ],
    )}

    {callout(
        "warning",
        "Не выбирайте фреймворк по рейтингам популярности",
        "Бенчмарки производительности и списки «самых быстрых фреймворков» сильно зависят от "
        "того, что именно измеряется, и быстро устаревают. Разумнее спрашивать: что должно "
        "делать именно моё приложение, какой опыт уже есть у команды, что здесь уже "
        "используется. Более предметное сравнение по конкретным задачам, а не по абстрактному "
        "«что лучше», — в разделе 22.18.",
    )}

    <p>Официальная документация: <a href="https://flask.palletsprojects.com/">Flask</a>,
    <a href="https://www.djangoproject.com/">Django</a>,
    <a href="https://fastapi.tiangolo.com/">FastAPI</a>,
    <a href="https://www.starlette.io/">Starlette</a>.</p>
    """
    out = render_page(
        page_title="Веб-фреймворки на Python: Flask, Django, FastAPI и другие",
        description="Что такое веб-фреймворк, точные определения Flask, Django, FastAPI и Starlette, и какие ещё фреймворки существуют в экосистеме Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Фреймворки", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Веб-фреймворки на Python: Flask, Django, FastAPI и другие",
        lede="Веб-фреймворк — набор готовых средств для создания веб-приложений. У Flask, Django, FastAPI и Starlette разный набор встроенных возможностей.",
        body_html=body,
        sidebar_groups=sidebar("22-17-veb-frejmvorki.html"),
        nav=PageNav(prev_href="22-16-api.html", prev_label="HTTP API: обмен данными между программами", next_href="22-18-flask-django-fastapi.html", next_label="Сравнение Flask, Django и FastAPI"),
    )
    write("22-17-veb-frejmvorki.html", out)


def build_18() -> None:
    body = f"""
    <p>Раздел 22.17 показал общую карту. Теперь сравним три самых заметных фреймворка —
    Flask, Django и FastAPI — по конкретным задачам, а не по общим впечатлениям.</p>

    {comparison_table(
        ["Критерий", "Flask", "Django", "FastAPI"],
        [
            ["Назначение", "Общего назначения, часто сайты с HTML-страницами", "Общего назначения, приложения вокруг базы данных", "Прежде всего HTTP API"],
            ["Маршрутизация", "Встроенная", "Встроенная", "Встроенная"],
            ["Шаблоны HTML", "Jinja", "Встроенный движок шаблонов", "Не основная задача — фреймворк ориентирован на API"],
            ["ORM", "Нет своего — через сторонний ORM (раздел 22.26)", "Да, встроенный", "Нет своего — через сторонний ORM"],
            ["Миграции", "Нет своих — через сторонний инструмент", "Да, встроенные (makemigrations/migrate)", "Нет своих — через сторонний инструмент"],
            ["Административный интерфейс", "Нет своего", "Да, встроенный автоматический", "Нет своего"],
            ["Аутентификация", "Нет своей — через расширения", "Да, встроенная система пользователей", "Нет своей — через сторонние библиотеки"],
            ["Проверка данных", "Вручную или через расширения", "Через формы и сериализаторы Django/DRF", "Встроенная, на основе подсказок типов Python"],
            ["OpenAPI", "Нет своей", "Нет своей в ядре", "Да, встроенная, автоматическая"],
            ["WSGI / ASGI (раздел 22.19)", "WSGI, с ограниченной поддержкой async-обработчиков", "Поддерживает и WSGI, и ASGI режимы развёртывания", "ASGI изначально"],
            ["Типичные проекты", "Небольшие и средние сайты, простые API", "Крупные приложения с базой данных и админкой", "HTTP API, сервисы с типизированными данными"],
        ],
    )}

    {callout(
        "warning",
        "Django REST Framework — отдельный проект, а не часть ядра Django",
        "Django из коробки умеет отдавать HTML-страницы и имеет админ-панель, но полноценный "
        "инструментарий для REST API — это отдельный пакет, Django REST Framework (DRF), "
        "который устанавливают и подключают самостоятельно. Он не входит в состав самого "
        "Django и не устанавливается вместе с ним автоматически.",
    )}

    {decision_map([
        ("Нужен сайт с формами, шаблонами, без готовой админки", "Flask"),
        ("Нужна бизнес-система с базой данных и админ-панелью «из коробки»", "Django"),
        ("Нужен API-сервис с автоматической документацией", "FastAPI"),
        ("Нужен низкоуровневый контроль над ASGI-приложением", "Starlette"),
    ], title="Отправная точка для выбора", caption="Реальные проекты часто смешивают инструменты — это стартовые ориентиры, а не жёсткие правила")}

    <h2>Почему для учебного проекта выбран Flask</h2>
    <p>В этой главе первый серверный проект построен на Flask. Flask предоставляет основные
    средства веб-приложения — маршрутизацию, обработку запросов и ответов и работу с
    шаблонами — без большого набора обязательных подсистем. Поэтому на небольшом учебном
    проекте удобно последовательно рассмотреть каждый из этих механизмов.</p>

    <p>Django предоставляет больше готовых компонентов, например ORM, миграции, аутентификацию
    и административный интерфейс. FastAPI ориентирован прежде всего на создание HTTP API и
    тесно использует аннотации типов Python.</p>

    <p>Flask выбран здесь как подходящий инструмент для первого учебного веб-приложения. Это
    не означает, что Flask является лучшим решением для любого проекта.</p>

    {practice_card(
        "22-18",
        "Практика: выбор фреймворка по задаче",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-18/index.html",
    )}
    """
    out = render_page(
        page_title="Сравнение Flask, Django и FastAPI",
        description="Сравнение Flask, Django и FastAPI по объективным критериям: маршрутизация, шаблоны, ORM, миграции, админ-интерфейс, аутентификация, валидация и OpenAPI.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Сравнение фреймворков", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Сравнение Flask, Django и FastAPI",
        lede="Flask, Django и FastAPI решают разные классы задач и предоставляют разный набор встроенных возможностей.",
        body_html=body,
        sidebar_groups=sidebar("22-18-flask-django-fastapi.html"),
        nav=PageNav(prev_href="22-17-veb-frejmvorki.html", prev_label="Веб-фреймворки на Python: Flask, Django, FastAPI и другие", next_href="22-19-wsgi-asgi.html", next_label="WSGI и ASGI: связь веб-приложения с сервером"),
    )
    write("22-18-flask-django-fastapi.html", out)


def build_19() -> None:
    body = f"""
    <p>Раздел 22.18 упомянул WSGI и ASGI как техническую разницу между фреймворками. Разберём,
    что они означают на уровне идеи, без деталей реализации.</p>

    <p><strong>WSGI</strong> (Web Server Gateway Interface) и <strong>ASGI</strong>
    (Asynchronous Server Gateway Interface) — стандартные интерфейсы, описывающие, как сервер
    приложений передаёт HTTP-запрос Python-приложению и получает от него ответ. В обычном
    развёртывании сетевые соединения принимает сервер приложений или другая серверная
    инфраструктура, а не сам фреймворк (Flask, Django, FastAPI) напрямую — WSGI/ASGI и есть то
    общее соглашение между ними.</p>

    {comparison_table(
        ["", "WSGI", "ASGI"],
        [
            ["Полное название", "Web Server Gateway Interface", "Asynchronous Server Gateway Interface"],
            ["Модель обработки запроса", "Синхронная — один запрос обрабатывается целиком, прежде чем начать следующий в этом потоке", "Поддерживает асинхронную обработку — приложение может ждать медленную операцию, не блокируя весь процесс"],
            ["Долгоживущие соединения (WebSocket)", "Не рассчитан на такой сценарий", "Поддерживается совместимыми фреймворками и серверами"],
            ["Кто использует", "Flask", "Starlette, FastAPI"],
        ],
    )}

    {callout(
        "info",
        "Django поддерживает WSGI и ASGI",
        "Современный Django поддерживает оба режима развёртывания — традиционный WSGI и "
        "ASGI — в зависимости от того, как настроен проект. Это не значит, что каждая часть "
        "Django одинаково хорошо работает асинхронно, но сам фреймворк не привязан жёстко "
        "только к одному протоколу.",
    )}

    <h2>Flask и async — не то же самое, что ASGI-фреймворк</h2>
    <p>Flask умеет вызывать <code class="inline">async def</code>-обработчики, но само
    приложение при этом остаётся WSGI-приложением по архитектуре: для выполнения такого
    обработчика Flask запускает событийный цикл и выполняет в нём корутину, занимая при этом
    один обработчик запроса на всё время её работы. Это удобно, когда конкретному обработчику
    нужно ждать медленную операцию ввода-вывода, но не превращает Flask в полноценный
    ASGI-фреймворк вроде FastAPI — если приложению принципиально важна асинхронная модель на
    всех уровнях, ASGI-фреймворк подойдёт лучше.</p>

    <h2>Фреймворк и сервер приложений — разные вещи</h2>
    <p>Сам Flask или FastAPI описывает <em>что</em> делать с запросом. Отдельная программа —
    <strong>сервер приложений</strong> — отвечает за то, чтобы реально принять соединение по
    сети и передать запрос фреймворку по протоколу WSGI или ASGI:</p>
    {comparison_table(
        ["Протокол", "Примеры серверов приложений"],
        [
            ["WSGI", "Gunicorn, Waitress"],
            ["ASGI", "Uvicorn, Hypercorn"],
        ],
    )}
    <p>К этому различию мы вернёмся в разделе 22.34 — сервер разработки, встроенный во Flask, и
    сервер приложений для рабочего окружения решают одну и ту же задачу по-разному.</p>

    {practice_card(
        "22-19",
        "Практика: WSGI или ASGI?",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-19/index.html",
    )}
    """
    out = render_page(
        page_title="WSGI и ASGI: связь веб-приложения с сервером",
        description="Разница между синхронным протоколом WSGI и асинхронным ASGI, и почему это отдельный слой от самого фреймворка.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("WSGI и ASGI", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="WSGI и ASGI: связь веб-приложения с сервером",
        lede="Фреймворк описывает, что делать с запросом. WSGI и ASGI — соглашение о том, как запрос до него доходит.",
        body_html=body,
        sidebar_groups=sidebar("22-19-wsgi-asgi.html"),
        nav=PageNav(prev_href="22-18-flask-django-fastapi.html", prev_label="Сравнение Flask, Django и FastAPI", next_href="22-20-zachem-baza-dannyh.html", next_label="Зачем веб-приложению база данных"),
    )
    write("22-19-wsgi-asgi.html", out)


def build_20() -> None:
    body = f"""
    <p>Список задач в разделе 22.5 хранится вот так:</p>
    {code_block("app.py", 'zadachi = ["Выучить основы Python", "Собрать сайт на Flask"]')}
    <p>Это обычная переменная Python — список, который живёт в оперативной памяти, пока
    работает процесс приложения. У такого хранения есть ограничения, которые незаметны на
    маленьком примере, но становятся серьёзной проблемой по мере роста приложения и нагрузки
    на него.</p>

    {comparison_table(
        ["Проблема", "Что происходит"],
        [
            ["Перезапуск", "Остановили процесс Python (обновили код, перезагрузили сервер) — список исчез вместе с ним"],
            ["Несколько процессов", "Рабочее развёртывание (раздел 22.34) часто запускает несколько процессов приложения одновременно — у каждого своя копия памяти, свой список, они не видят изменений друг друга"],
            ["Запрос данных", "Список умеет перебор и фильтрацию средствами Python, но не умеет быстро находить нужные записи среди миллионов без полного перебора"],
            ["Согласованность при одновременных изменениях", "Два запроса, пришедшие почти одновременно, могут непредсказуемо испортить список, если оба меняют его в один и тот же момент"],
        ],
    )}

    <p><strong>СУБД</strong> (система управления базами данных) — программная система,
    создающая, хранящая, обрабатывающая запросы и управляющая базами данных; <strong>база
    данных</strong> — это организованные хранимые данные, с которыми работает СУБД. СУБД
    предоставляет механизмы постоянного хранения, запросов, транзакций, ограничений и
    согласованной работы с данными — она решает именно эти проблемы. Конкретные гарантии при
    этом зависят от выбранной СУБД, спроектированной схемы, использования транзакций и кода
    самого приложения: СУБД не устраняет проблему автоматически сама по себе, если ей не
    пользоваться правильно.</p>

    {callout(
        "info",
        "Персистентность — данные, которые переживают перезапуск программы",
        "Свойство хранить данные так, что они не исчезают после завершения процесса, называют "
        "<strong>сохранением данных между запусками</strong>, или persistence. Список Python "
        "в памяти этим свойством не обладает; файл на диске или база данных — обладают.",
    )}

    <p>Разделы 22.21-22.28 разбирают, как устроены базы данных и на каком языке с ними
    работают, а раздел 22.29 заменяет список Python в проекте главы на базу данных SQLite.</p>
    """
    out = render_page(
        page_title="Зачем веб-приложению база данных",
        description="Почему список Python в памяти не годится для хранения данных настоящего приложения: перезапуск, несколько процессов, поиск, согласованность.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Зачем нужна база данных", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Зачем веб-приложению база данных",
        lede="Список Python в памяти хранит данные только до перезапуска процесса — а рано или поздно процесс перезапускается.",
        body_html=body,
        sidebar_groups=sidebar("22-20-zachem-baza-dannyh.html"),
        nav=PageNav(prev_href="22-19-wsgi-asgi.html", prev_label="WSGI и ASGI: связь веб-приложения с сервером", next_href="22-21-relyacionnaya-baza.html", next_label="Реляционные базы данных: таблицы, ключи и связи"),
    )
    write("22-20-zachem-baza-dannyh.html", out)


def build_21() -> None:
    body = f"""
    <p>Самый распространённый вид базы данных — <strong>реляционная</strong>: данные хранятся
    в <strong>таблицах</strong>, похожих на лист расчётной таблицы. Каждая
    <strong>строка</strong> — одна запись, каждый <strong>столбец</strong> — одно её свойство
    с заранее заданным типом.</p>

    {relationship_diagram(
        "users",
        "tasks",
        "1 — N",
        style="has-a",
        caption="Одному пользователю users может соответствовать несколько строк tasks",
    )}

    {comparison_table(
        ["id", "title", "done"],
        [
            ["1", "Выучить основы Python", "1"],
            ["2", "Собрать сайт на Flask", "0"],
        ],
    )}
    <p>Такая таблица — <code class="inline">tasks</code>: у каждой строки есть
    <code class="inline">id</code> — уникальный номер, по которому её можно однозначно найти.
    Столбец, который делает это (обычно <code class="inline">id</code>), называют
    <strong>первичным ключом</strong> (primary key).</p>

    <h2>Связь между таблицами — внешний ключ</h2>
    <p>Если бы у каждой задачи был владелец, вторая таблица <code class="inline">users</code>
    хранила бы пользователей, а таблица <code class="inline">tasks</code> — ссылку на строку
    в ней:</p>
    {comparison_table(
        ["id", "title", "done", "user_id"],
        [
            ["1", "Выучить основы Python", "1", "7"],
            ["2", "Собрать сайт на Flask", "0", "7"],
        ],
    )}
    <p>Столбец <code class="inline">user_id</code>, который ссылается на
    <code class="inline">id</code> в другой таблице, называют <strong>внешним ключом</strong>
    (foreign key).</p>

    {callout(
        "info",
        "Откуда взялось слово «реляционная»",
        "Название происходит от математического понятия relation (отношение), лежащего в "
        "основе реляционной модели данных: отношение — это множество кортежей одинаковой "
        "структуры, а на практике его представляют в виде таблицы. Связи между таблицами через "
        "внешние ключи — важная часть проектирования баз данных, но не источник названия "
        "модели: одна таблица без единого внешнего ключа всё равно остаётся реляционной.",
    )}

    {callout(
        "tip",
        "Итоговый проект остаётся без пользователей — и это осознанно",
        "Как раздел 22.31 объясняет подробнее: чтобы не расширять эту главу до полноценной "
        "аутентификации, итоговый проект (раздел 22.35) использует только одну таблицу — "
        "<code class=\"inline\">tasks</code>, без <code class=\"inline\">users</code> и без "
        "внешних ключей. Связи между таблицами — важная идея, но не обязательный элемент "
        "самого маленького работающего приложения.",
    )}
    """
    out = render_page(
        page_title="Реляционные базы данных: таблицы, ключи и связи",
        description="Таблицы, строки, столбцы, первичный и внешний ключ — базовые понятия реляционных баз данных на примере задач и пользователей.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Реляционная база данных", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Реляционные базы данных: таблицы, ключи и связи",
        lede="Данные в строках и столбцах — и связи между таблицами через первичные и внешние ключи.",
        body_html=body,
        sidebar_groups=sidebar("22-21-relyacionnaya-baza.html"),
        nav=PageNav(prev_href="22-20-zachem-baza-dannyh.html", prev_label="Зачем веб-приложению база данных", next_href="22-22-sql.html", next_label="SQL: создаём, читаем и изменяем данные"),
    )
    write("22-21-relyacionnaya-baza.html", out)


def build_22() -> None:
    body = f"""
    <p><strong>SQL</strong> (Structured Query Language — язык структурированных запросов) —
    язык определения структуры данных и выполнения запросов к реляционной базе данных: им
    создают таблицы, читают, добавляют, изменяют и удаляют строки. У SQL есть общий стандарт, но у каждой
    конкретной системы (SQLite, PostgreSQL, MySQL) — свои расширения и особенности поверх
    него, поэтому говорят не о «разных языках SQL», а о разных <strong>диалектах</strong>
    одного языка. Примеры на этой странице выполняются в SQLite (раздел 22.23).</p>

    <h2>CREATE TABLE — описываем структуру</h2>
    {code_block(
        "sozdanie_tablicy.sql",
        'CREATE TABLE tasks (\n'
        '    id INTEGER PRIMARY KEY,\n'
        '    title TEXT NOT NULL,\n'
        '    done INTEGER NOT NULL DEFAULT 0\n'
        ');',
        lang="sql",
    )}
    {callout(
        "warning",
        "NOT NULL запрещает именно значение NULL, а не пустую строку",
        "<code class=\"inline\">NOT NULL</code> запрещает записывать в столбец специальное "
        "SQL-значение <code class=\"inline\">NULL</code> («значение неизвестно / отсутствует»). "
        "Пустая строка <code class=\"inline\">''</code> — это по-прежнему допустимое значение "
        "типа TEXT, и <code class=\"inline\">NOT NULL</code> её не отклонит. Если приложению "
        "нужно запретить именно пустой (или состоящий из пробелов) заголовок задачи, для этого "
        "нужна отдельная проверка — на стороне приложения (раздел 22.31) или явное ограничение "
        "<code class=\"inline\">CHECK</code>, как показывает раздел 22.29.",
    )}
    <p><code class="inline">DEFAULT 0</code> задаёт значение по умолчанию, если его не указали
    явно.</p>

    <h2>Четыре операции CRUD</h2>
    {comparison_table(
        ["Действие", "SQL", "Что делает"],
        [
            ["Create", "INSERT", "Добавить новую строку"],
            ["Read", "SELECT", "Прочитать одну или несколько строк"],
            ["Update", "UPDATE", "Изменить существующую строку"],
            ["Delete", "DELETE", "Удалить строку"],
        ],
    )}

    {code_block(
        "insert.sql",
        "INSERT INTO tasks (title) VALUES ('Купить хлеб');",
        lang="sql",
    )}
    {code_block(
        "select.sql",
        "SELECT id, title, done FROM tasks WHERE done = 0 ORDER BY id LIMIT 10;",
        lang="sql",
    )}
    <p><code class="inline">WHERE</code> оставляет только подходящие строки,
    <code class="inline">ORDER BY</code> задаёт порядок, <code class="inline">LIMIT</code>
    ограничивает количество результатов.</p>
    {code_block(
        "update.sql",
        "UPDATE tasks SET done = 1 WHERE id = 1;",
        lang="sql",
    )}
    {code_block(
        "delete.sql",
        "DELETE FROM tasks WHERE id = 1;",
        lang="sql",
    )}

    <h2>SQL из Python: модуль sqlite3</h2>
    {code_block(
        "sql_iz_python.py",
        'import sqlite3\n\n'
        'baza = sqlite3.connect("zadachi.db")\n'
        'baza.execute(\n'
        '    "INSERT INTO tasks (title) VALUES (?)",\n'
        '    ("Купить хлеб",),\n'
        ')\n'
        'baza.commit()\n\n'
        'stroki = baza.execute("SELECT id, title, done FROM tasks").fetchall()\n'
        'for stroka in stroki:\n'
        "    print(stroka)\n",
    )}
    {callout(
        "warning",
        "Знак вопроса вместо f-строки — не стилистический выбор",
        "<code class=\"inline\">?</code> в SQL-строке — это <strong>параметризованный "
        "запрос</strong>: значение подставляет сам модуль <code class=\"inline\">sqlite3"
        "</code>, безопасно, отдельно от текста запроса. Если вместо этого собрать запрос "
        "через f-строку с пользовательским вводом внутри, это открывает путь к SQL-инъекции "
        "— что именно может пойти не так и почему параметризация обязательна, а не желательна, "
        "показывает раздел 22.32.",
    )}

    {practice_card(
        "22-22",
        "Практика: CRUD на SQLite",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-22/index.html",
    )}
    """
    out = render_page(
        page_title="SQL: создаём, читаем и изменяем данные",
        description="CREATE TABLE, SELECT, INSERT, UPDATE, DELETE и соответствие CRUD-операций — с примерами на SQLite и через модуль sqlite3.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("SQL", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="SQL: создаём, читаем и изменяем данные",
        lede="Один язык — и создание таблиц, и чтение, и изменение, и удаление данных.",
        body_html=body,
        sidebar_groups=sidebar("22-22-sql.html"),
        nav=PageNav(prev_href="22-21-relyacionnaya-baza.html", prev_label="Реляционные базы данных: таблицы, ключи и связи", next_href="22-23-sqlite.html", next_label="SQLite: встраиваемая реляционная СУБД"),
    )
    write("22-22-sql.html", out)


def build_23() -> None:
    body = f"""
    <p><strong>СУБД</strong> — система управления базами данных: программное обеспечение,
    которое создаёт, хранит, обрабатывает запросы и управляет базами данных. <strong>SQLite
    </strong> — встраиваемая реляционная СУБД, реализованная в виде программной библиотеки. В
    отличие от PostgreSQL или MySQL, SQLite не требует отдельного процесса сервера базы
    данных: приложение обращается к библиотеке SQLite непосредственно, внутри собственного
    процесса.</p>

    <p>При обычном файловом использовании содержимое базы SQLite хранится в одном основном
    файле. Во время работы SQLite может создавать дополнительные служебные файлы, например
    rollback journal или WAL. SQLite также поддерживает базу данных в оперативной памяти
    (<code class="inline">:memory:</code>), которая не сохраняется на диск вовсе — это удобно,
    например, для тестов (раздел 22.33).</p>

    <p>Для работы с SQLite в Python используется модуль <code class="inline">sqlite3</code>,
    предоставляющий интерфейс DB-API 2.0. В обычных сборках CPython он доступен без установки
    отдельного пакета через pip, однако технически <code class="inline">sqlite3</code>
    относится к опциональным модулям конкретной сборки интерпретатора и использует библиотеку
    SQLite, установленную в системе или собранную вместе с Python.</p>

    {comparison_table(
        ["", "Обычная клиент-серверная СУБД", "SQLite"],
        [
            ["Отдельный процесс-сервер", "Да, работает постоянно", "Нет — работает внутри процесса приложения"],
            ["Основное хранение", "Управляется сервером базы данных", "Основной файл базы данных (возможны служебные файлы journal/WAL)"],
            ["Настройка для старта", "Установить и запустить сервер, настроить доступ", "Не требуется отдельная настройка сервера"],
            ["Несколько серверов приложения пишут одновременно", "Штатный сценарий", "Ограниченная поддержка одновременной записи"],
        ],
    )}

    {callout(
        "warning",
        "Где SQLite подходит особенно хорошо",
        "SQLite — полноценный SQL-движок, которым пользуются и очень крупные приложения — как "
        "основное хранилище локальных данных или как часть более крупной системы. SQLite хорошо "
        "подходит для локальных приложений, обучения, прототипов, тестов (раздел 22.33) и "
        "многих небольших и средних развёртываний, где модели одновременного доступа SQLite "
        "достаточно. Клиент-серверную базу выбирают не потому, что SQLite чем-то хуже как "
        "движок, а когда нескольким серверам приложения нужно надёжно писать в одну базу "
        "параллельно — эту разницу подробнее рассматривает раздел 22.24.",
    )}

    <h2>Подключение и курсор</h2>
    {code_block(
        "podklyuchenie.py",
        'import sqlite3\n\n'
        'baza = sqlite3.connect("zadachi.db")\n'
        'baza.row_factory = sqlite3.Row   # доступ к столбцам по имени\n\n'
        'kursor = baza.execute("SELECT id, title FROM tasks")\n'
        'for stroka in kursor:\n'
        '    print(stroka["id"], stroka["title"])\n\n'
        'baza.close()\n',
    )}
    <p><code class="inline">sqlite3.connect(...)</code> открывает (или создаёт, если файла ещё
    нет) файл базы данных. <code class="inline">row_factory = sqlite3.Row</code> позволяет
    обращаться к столбцам результата по имени, а не только по числовому индексу — удобнее и
    надёжнее, особенно если порядок столбцов в запросе когда-нибудь изменится.</p>

    {callout(
        "info",
        "Отдельное подключение на каждый поток",
        "По умолчанию одно соединение <code class=\"inline\">sqlite3.connect(...)</code> "
        "нельзя без осторожности использовать сразу из нескольких потоков. Практичный способ "
        "организовать подключения во Flask-приложении — открывать соединение под каждый запрос "
        "и закрывать его сразу после — показывает раздел 22.29.",
    )}

    <p>Официальная документация: <a href="https://sqlite.org/docs.html">SQLite</a>,
    <a href="https://docs.python.org/3/library/sqlite3.html">Python — модуль sqlite3</a>.</p>

    {practice_card(
        "22-23",
        "Практика: подключение к SQLite через sqlite3",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-23/index.html",
    )}
    """
    out = render_page(
        page_title="SQLite: встраиваемая реляционная СУБД",
        description="SQLite как встраиваемая СУБД без отдельного процесса сервера, модуль sqlite3, подключение, курсор и уместные сценарии использования.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("SQLite", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="SQLite: встраиваемая реляционная СУБД",
        lede="SQLite — реляционная СУБД, работающая как библиотека внутри процесса приложения, без отдельного сервера.",
        body_html=body,
        sidebar_groups=sidebar("22-23-sqlite.html"),
        nav=PageNav(prev_href="22-22-sql.html", prev_label="SQL: создаём, читаем и изменяем данные", next_href="22-24-postgresql-mysql-sqlite.html", next_label="PostgreSQL, MySQL/MariaDB и SQLite: основные различия"),
    )
    write("22-23-sqlite.html", out)


def build_24() -> None:
    body = f"""
    <p>SQLite — не единственная реляционная СУБД. Разберём, чем от неё и друг от друга
    отличаются два широко используемых клиент-серверных варианта.</p>

    {callout("info", "PostgreSQL", "PostgreSQL — объектно-реляционная СУБД с клиент-серверной "
        "архитектурой: приложение подключается к отдельно запущенному серверу PostgreSQL по "
        "сети. Известна широким набором встроенных типов данных и расширяемостью.")}
    {callout("info", "MySQL", "MySQL — реляционная клиент-серверная СУБД, одна из самых "
        "распространённых в веб-разработке.")}
    {callout("info", "MariaDB", "MariaDB — отдельная реляционная СУБД, исторически возникшая "
        "как форк MySQL и во многом остающаяся с ним совместимой.")}
    {callout("info", "SQLite", "SQLite — встраиваемая реляционная СУБД: она работает как "
        "библиотека внутри процесса приложения, без отдельного сервера (раздел 22.23).")}

    {callout(
        "warning",
        "MySQL и MariaDB — не взаимозаменяемые синонимы",
        "MariaDB возникла как форк MySQL и во многом остаётся с ним совместимой, но это два "
        "отдельных проекта с собственной историей разработки — они не идентичны и не всегда "
        "развиваются синхронно. В документации и в вакансиях их иногда упоминают вместе "
        "(«MySQL/MariaDB»), но для конкретного проекта стоит уточнять, какая именно из двух "
        "систем используется.",
    )}

    <p>Выбор между PostgreSQL, MySQL/MariaDB и SQLite почти никогда не сводится к «какая из
    них лучше в целом» — обычно это вопрос требований конкретного проекта: сколько серверов
    приложения будут писать в базу одновременно, какие возможности SQL нужны, что уже
    используется в команде и в её опыте, как будет устроено развёртывание. Ни одно из этих
    решений не является универсально правильным по умолчанию.</p>

    <p>Официальная документация: <a href="https://www.postgresql.org/docs/">PostgreSQL</a>,
    <a href="https://dev.mysql.com/doc/">MySQL</a>,
    <a href="https://mariadb.org/documentation/">MariaDB</a>,
    <a href="https://www.sqlite.org/docs.html">SQLite</a>.</p>
    """
    out = render_page(
        page_title="PostgreSQL, MySQL/MariaDB и SQLite: основные различия",
        description="Сравнение трёх реляционных систем: PostgreSQL, MySQL/MariaDB и SQLite — без утверждений о том, какая из них абсолютно лучше.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("PostgreSQL, MySQL и SQLite", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="PostgreSQL, MySQL/MariaDB и SQLite: основные различия",
        lede="Эти СУБД различаются архитектурой, возможностями и требованиями к эксплуатации — выбор зависит от требований проекта.",
        body_html=body,
        sidebar_groups=sidebar("22-24-postgresql-mysql-sqlite.html"),
        nav=PageNav(prev_href="22-23-sqlite.html", prev_label="SQLite: встраиваемая реляционная СУБД", next_href="22-25-nosql.html", next_label="NoSQL: основные виды нереляционных баз данных"),
    )
    write("22-24-postgresql-mysql-sqlite.html", out)


def build_25() -> None:
    body = f"""
    <p><strong>NoSQL</strong> — общее название для нереляционных систем управления базами
    данных, использующих модели данных, отличные от классической реляционной модели таблиц.</p>

    {callout(
        "info",
        "NoSQL — «не только SQL», а не «никогда не SQL»",
        "Термин NoSQL часто трактуют как Not Only SQL — «не только SQL». Это не название "
        "одного языка и не единый стандарт: под NoSQL объединяют несколько разных семейств "
        "СУБД. Многие нереляционные системы всё равно поддерживают SQL-подобные или собственные "
        "языки запросов — название описывает отход от классической реляционной модели таблиц, "
        "а не полный отказ от идеи структурированных запросов.",
    )}

    <p>Реляционные базы (разделы 22.21-22.24) хранят данные в таблицах с заранее заданной
    структурой. Иногда такая структура неудобна — например, если форма записей сильно
    отличается от документа к документу, нужна очень быстрая работа по ключу, или данные
    естественно представляются как узлы и связи. Ниже — четыре основных семейства NoSQL-СУБД,
    у каждого своя модель данных.</p>

    <h2>Ключ — значение</h2>
    <p>Каждая запись доступна по уникальному ключу. Значением может быть строка, число,
    структура данных или другой объект, в зависимости от СУБД.</p>
    <p><strong>Пример:</strong> Redis — сервер структур данных, в котором каждый объект имеет
    ключ; Redis поддерживает строки, списки, множества, хеши, потоки и другие структуры
    данных.</p>
    {code_block("primer_redis.txt", 'SET session:42 \'{{"user_id": 42, "expires": "2026-08-24"}}\'\nGET session:42', lang="text")}
    <p>Типичное применение: кеш, счётчики, хранение сессий/состояния, очереди и потоки данных
    — часто как дополнение к основной базе, а не её замена.</p>

    <h2>Документоориентированные базы данных</h2>
    <p>Данные хранятся в документах, состоящих из полей и значений. Документы могут содержать
    вложенные структуры.</p>
    <p><strong>Пример:</strong> MongoDB хранит документы в формате BSON, который по структуре
    близок к JSON.</p>
    {code_block(
        "primer_dokument.json",
        '{{\n'
        '  "name": "Механическая клавиатура",\n'
        '  "price": 8900,\n'
        '  "characteristics": {{"switches": "red", "layout": "ru"}}\n'
        '}}',
        lang="text",
    )}
    <p>Удобны, когда форма записей может меняться от документа к документу.</p>

    <h2>Ширококолоночные базы данных</h2>
    <p>Данные организуются вокруг ключей разделов (partition keys) и строк с набором столбцов.
    Такая модель рассчитана на распределённое хранение больших объёмов данных и заранее
    продуманные шаблоны запросов.</p>
    <p><strong>Пример:</strong> Apache Cassandra — распределённая ширококолоночная СУБД,
    доступная через собственный язык запросов CQL.</p>
    {code_block("primer_wide_column.txt", "Партиция: device_id = 42\nСтроки внутри партиции упорядочены по date", lang="text")}
    <p>Типичное применение: события и метрики с высокой скоростью записи, распределённые
    по устройству, пользователю или другому ключу раздела.</p>

    <h2>Графовые базы данных</h2>
    <p>Данные представлены узлами, связями между ними и свойствами. Такая модель удобна, когда
    сами связи являются важной частью задачи.</p>
    <p><strong>Пример:</strong> Neo4j — графовая СУБД, где запросы явно оперируют узлами и
    связями.</p>
    {code_block("primer_graf.txt", "(Ада)-[:ДРУГ]->(Борис)-[:ДРУГ]->(Вера)", lang="text")}
    <p>Типичное применение: социальные связи, рекомендации, сети зависимостей, анализ связей
    при выявлении мошенничества.</p>

    <h2>Специализированные системы хранения и поиска</h2>
    <p>Отдельно стоят системы полнотекстового поиска, векторные и временные базы данных — их не
    относят к четырём каноническим семействам выше. Эти категории могут пересекаться друг с
    другом и с уже перечисленными моделями, а некоторые продукты сочетают несколько моделей в
    одной СУБД (multi-model).</p>

    <h2>Общие особенности NoSQL-систем</h2>
    <p>У многих NoSQL-СУБД схема данных более гибкая, чем в реляционной модели, — это не
    значит, что схема отсутствует полностью. Многие NoSQL-СУБД проектируются с расчётом на
    распределённую работу и горизонтальное масштабирование, но конкретные гарантии
    (согласованность, поддержка транзакций, устойчивость к сбоям) зависят от продукта и его
    настройки. Производительность зависит от модели данных, конкретной СУБД и типа запросов —
    не существует правила «NoSQL всегда быстрее».</p>

    {comparison_table(
        ["Критерий", "Реляционная СУБД", "NoSQL-системы"],
        [
            ["Модель данных", "Таблицы, строки, столбцы", "Зависит от типа: документы, ключ-значение, wide-column, граф"],
            ["Схема", "Обычно определяется явно", "Часто более гибкая; зависит от конкретной СУБД"],
            ["Связи", "Внешние ключи, JOIN и другие реляционные операции", "Реализуются по-разному: ссылки, вложенные документы, графовые связи и другое"],
            ["Язык запросов", "SQL и его диалекты", "Собственные языки запросов, команды или API; некоторые поддерживают SQL-подобные интерфейсы"],
            ["Транзакции", "Зависят от СУБД, обычно развитая поддержка транзакций", "Зависят от конкретной СУБД; многие современные системы также поддерживают транзакции"],
            ["Масштабирование", "Возможны вертикальные и распределённые архитектуры", "Многие системы изначально проектируются для распределённой работы"],
            ["Когда выбирать", "Когда реляционная модель хорошо соответствует данным и запросам", "Когда конкретная нереляционная модель лучше соответствует данным и нагрузке"],
        ],
    )}

    <h2>Что выбрать</h2>
    <p>Реляционную СУБД стоит рассматривать, когда данные имеют естественную реляционную
    структуру, важны связи и ограничения, запросы хорошо ложатся на SQL, а транзакционная
    целостность важна для задачи. Конкретную NoSQL-СУБД стоит рассматривать, когда одна из
    моделей — документная, ключ-значение, ширококолоночная или графовая — естественно
    соответствует задаче, шаблон доступа к данным хорошо понятен заранее, а требования к
    распределению и масштабированию склоняют выбор в сторону конкретной нереляционной
    архитектуры.</p>

    {callout(
        "warning",
        "Для простого приложения достаточно одной подходящей СУБД",
        "Крупные реальные системы нередко используют не одну технологию хранения, но учебный "
        "проект стоит начинать с самой простой подходящей. Для обычного CRUD-приложения вроде "
        "списка задач не нужны одновременно PostgreSQL, MongoDB, Redis и векторная база — это "
        "добавит сложности эксплуатации без реальной выгоды. Итоговый проект этой главы "
        "(раздел 22.35) обходится одной таблицей в SQLite.",
    )}

    <p>Официальная документация: <a href="https://www.mongodb.com/docs/">MongoDB</a>,
    <a href="https://redis.io/docs/">Redis</a>,
    <a href="https://cassandra.apache.org/doc/">Apache Cassandra</a>,
    <a href="https://neo4j.com/docs/">Neo4j</a>.</p>
    """
    out = render_page(
        page_title="NoSQL: основные виды нереляционных баз данных",
        description="Ключ-значение, документные, ширококолоночные и графовые СУБД — четыре основных семейства NoSQL, их модели данных и когда их стоит выбирать.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("NoSQL", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="NoSQL: основные виды нереляционных баз данных",
        lede="NoSQL объединяет несколько нереляционных моделей хранения: ключ-значение, документы, ширококолоночные хранилища и графы.",
        body_html=body,
        sidebar_groups=sidebar("22-25-nosql.html"),
        nav=PageNav(prev_href="22-24-postgresql-mysql-sqlite.html", prev_label="PostgreSQL, MySQL/MariaDB и SQLite: основные различия", next_href="22-26-orm.html", next_label="ORM: работа с базой данных через объекты Python"),
    )
    write("22-25-nosql.html", out)


def build_26() -> None:
    body = f"""
    <p>Раздел 22.22 писал SQL-запросы текстом. <strong>ORM</strong> (Object-Relational
    Mapper — объектно-реляционное отображение) — это библиотека, которая позволяет работать
    со строками таблицы как с обычными объектами Python, а не собирать SQL-текст вручную. У
    разных ORM разный API — вот один и тот же запрос и одна и та же вставка в двух самых
    заметных ORM экосистемы Python:</p>

    {comparison_table(
        ["Действие", "SQL напрямую", "Django ORM", "SQLAlchemy 2.x"],
        [
            ["Прочитать невыполненные задачи", "<code class=\"inline\">SELECT id, title FROM tasks WHERE done = 0</code>", "<code class=\"inline\">Task.objects.filter(done=False)</code>", "<code class=\"inline\">select(Task).where(Task.done.is_(False))</code>"],
            ["Добавить новую задачу", "<code class=\"inline\">INSERT INTO tasks (title) VALUES (?)</code>", "<code class=\"inline\">Task.objects.create(title=\"Купить хлеб\")</code>", "<code class=\"inline\">session.add(Task(title=\"Купить хлеб\"))</code>"],
        ],
    )}

    <p><strong>SQLAlchemy</strong> (описывает себя как «инструментарий SQL и
    объектно-реляционный преобразователь для Python») используется вместе с разными
    фреймворками, включая Flask, и распространяется отдельным пакетом. Встроенный
    <strong>ORM Django</strong> поставляется вместе с самим фреймворком и тесно с ним
    интегрирован — это разные библиотеки с разным API, а не два имени одного и того же
    инструмента.</p>

    {callout(
        "warning",
        "ORM не отменяет необходимость понимать SQL",
        "ORM удобно избавляет от рутины — не нужно вручную собирать текст запроса для каждой "
        "операции. Но он не убирает саму реляционную модель: ORM всё равно формирует и "
        "выполняет SQL-запросы на основе операций с объектами, и понимание того, как устроены "
        "таблицы, связи и запросы (разделы 22.21-22.22), напрямую влияет на то, насколько "
        "эффективно и правильно вы используете ORM — особенно когда запрос через ORM работает "
        "не так быстро, как ожидалось, и нужно понять, какой именно SQL он выполнил.",
    )}

    <h2>Почему в итоговом проекте используется sqlite3</h2>
    <p>Для проекта этой главы (раздел 22.29) выбран прямой модуль
    <code class="inline">sqlite3</code>, а не ORM: цель этой главы — понять, что именно
    происходит с данными на каждом шаге, а не спрятать это за слоем абстракции ещё до того,
    как эта абстракция станет понятна. ORM — полезный и распространённый инструмент для
    реальных проектов, но здесь он отвлёк бы от самой идеи главы.</p>

    {practice_card(
        "22-26",
        "Практика: SQL и его отображение в ORM",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-26/index.html",
    )}
    """
    out = render_page(
        page_title="ORM: работа с базой данных через объекты Python",
        description="Что такое ORM, чем SQLAlchemy и ORM Django отличаются друг от друга, и почему знание SQL остаётся нужным даже при работе через ORM.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("ORM", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="ORM: работа с базой данных через объекты Python",
        lede="Строки таблицы как объекты Python — удобно, но ORM всё равно формирует и выполняет обычный SQL.",
        body_html=body,
        sidebar_groups=sidebar("22-26-orm.html"),
        nav=PageNav(prev_href="22-25-nosql.html", prev_label="NoSQL: основные виды нереляционных баз данных", next_href="22-27-migracii-shemy.html", next_label="Миграции схемы базы данных"),
    )
    write("22-26-orm.html", out)


def build_27() -> None:
    body = f"""
    <p>Слово «миграция» в веб-разработке означает две разные вещи, и их легко перепутать. Эта
    страница — про первую: <strong>миграцию схемы</strong> — изменение структуры базы данных
    со временем. Вторая — перенос самих данных между базами — рассматривается в разделе
    22.28.</p>

    <p>Приложение растёт, и структура таблицы, спроектированная в начале, перестаёт хватать.
    Например, у задачи появляется отметка «выполнено»:</p>

    {comparison_table(
        ["Версия 1", "Версия 2"],
        [
            ["tasks(id, title)", "tasks(id, title, done)"],
        ],
    )}

    <p><strong>Миграция схемы</strong> — это записанное изменение структуры, которое можно
    применить к базе данных так же предсказуемо на любом компьютере: у разработчика локально,
    у коллеги, на сервере. В SQL для этого есть команда <code class="inline">ALTER TABLE</code>:</p>
    {code_block(
        "migraciya.sql",
        "ALTER TABLE tasks ADD COLUMN done INTEGER NOT NULL DEFAULT 0;",
        lang="sql",
    )}
    <p>Старые строки не исчезают — у каждой из них новый столбец <code class="inline">done</code>
    получает значение по умолчанию, <code class="inline">0</code>.</p>

    {code_block(
        "migraciya.py",
        'import sqlite3\n\n'
        'baza = sqlite3.connect("zadachi.db")\n'
        'baza.execute("ALTER TABLE tasks ADD COLUMN done INTEGER NOT NULL DEFAULT 0")\n'
        'baza.commit()\n',
    )}

    <h2>Инструменты, которые записывают миграции за вас</h2>
    <p>В маленьком проекте достаточно выполнить <code class="inline">ALTER TABLE</code>
    вручную один раз. В более крупном проекте с несколькими разработчиками и несколькими
    окружениями миграции обычно оформляют отдельными файлами с номерами и порядком применения
    — чтобы каждое изменение структуры можно было применить, отследить и, если нужно,
    откатить. В экосистеме SQLAlchemy для этого используют <strong>Alembic</strong> — отдельный
    инструмент для миграций схемы, который умеет сравнивать текущую структуру базы с описанием
    в коде и формировать черновик миграции; такой автосгенерированный файл — не готовое
    решение, а «черновая миграция» (candidate migration), которую нужно проверить и при
    необходимости поправить вручную перед применением. В Django миграции встроены в сам
    фреймворк: команда <code class="inline">makemigrations</code> создаёт файлы миграций по
    обнаруженным изменениям моделей, а <code class="inline">migrate</code> применяет их к
    базе данных.</p>

    {callout(
        "info",
        "Миграция схемы — про структуру, а не про содержимое",
        "Миграция схемы отвечает на вопрос «как теперь устроена таблица», а не «что переехало "
        "из одной базы в другую». Это принципиально другая задача, чем перенос данных, о "
        "котором пойдёт речь в разделе 22.28 — не путайте эти два значения слова «миграция», "
        "когда встретите его в реальных проектах.",
    )}

    {practice_card(
        "22-27",
        "Практика: миграция схемы SQLite",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-27/index.html",
    )}
    """
    out = render_page(
        page_title="Миграции схемы базы данных",
        description="Что такое миграция схемы, ALTER TABLE, и как инструменты вроде Alembic и Django migrations записывают изменения структуры базы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Миграции схемы", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Миграции схемы базы данных",
        lede="Структура таблицы меняется вместе с приложением — миграция записывает это изменение предсказуемо.",
        body_html=body,
        sidebar_groups=sidebar("22-27-migracii-shemy.html"),
        nav=PageNav(prev_href="22-26-orm.html", prev_label="ORM: работа с базой данных через объекты Python", next_href="22-28-perenos-dannyh.html", next_label="Перенос данных между базами"),
    )
    write("22-27-migracii-shemy.html", out)


def build_28() -> None:
    body = f"""
    <p>Второе значение слова «миграция» — <strong>перенос данных</strong> между базами или
    системами: например, из старой базы в новую, из одного формата хранения в другой. Не
    путайте с миграцией схемы из раздела 22.27 — там менялась структура таблицы, здесь
    переезжают сами записи.</p>

    {pipeline_diagram([
        {"kind": "plain", "title": "Исходная база", "rows": ["читаем строки"]},
        {"kind": "plain", "title": "Python", "rows": ["преобразуем данные"]},
        {"kind": "plain", "title": "JSON", "rows": ["промежуточный файл (необязательно)"]},
        {"kind": "plain", "title": "Целевая база", "rows": ["записываем строки"]},
        {"kind": "plain", "title": "Проверка", "rows": ["сверяем количество и содержимое"]},
    ], caption="Перенос данных: чтение, преобразование, запись, проверка")}

    <p>JSON (раздел 22.15) удобен как <em>промежуточный</em> формат в этом процессе — он
    текстовый, человекочитаемый и его легко прочитать в любом языке программирования. Но JSON
    — не универсальный формат переноса без потерь: у него нет отдельного типа для дат, для
    двоичных данных, и он не хранит ограничения и связи между таблицами (внешние ключи,
    раздел 22.21) — их приходится восстанавливать отдельно на стороне целевой базы.</p>

    <h2>Маленький воспроизводимый пример</h2>
    {code_block(
        "eksport_v_json.py",
        'import json\n'
        'import sqlite3\n\n'
        'istochnik = sqlite3.connect("zadachi.db")\n'
        'istochnik.row_factory = sqlite3.Row\n\n'
        'stroki = istochnik.execute("SELECT title, done FROM tasks").fetchall()\n'
        'dannye = [dict(stroka) for stroka in stroki]\n\n'
        'with open("zadachi.json", "w", encoding="utf-8") as fajl:\n'
        "    json.dump(dannye, fajl, ensure_ascii=False, indent=2)\n",
    )}
    {code_block(
        "import_iz_json.py",
        'import json\n'
        'import sqlite3\n\n'
        'with open("zadachi.json", encoding="utf-8") as fajl:\n'
        "    dannye = json.load(fajl)\n\n"
        'cel = sqlite3.connect("novaya_zadachi.db")\n'
        'cel.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")\n'
        'for zapis in dannye:\n'
        '    cel.execute(\n'
        '        "INSERT INTO tasks (title, done) VALUES (?, ?)",\n'
        '        (zapis["title"], zapis["done"]),\n'
        "    )\n"
        "cel.commit()\n",
    )}

    {callout(
        "warning",
        "Идентификаторы — решение, которое нужно явно продумать и проверить",
        "В примере выше новая база сама назначает новые значения <code class=\"inline\">id"
        "</code> при вставке — старые идентификаторы не переносятся. Это осознанный выбор, "
        "не случайность: если приложению важно сохранить исходные <code class=\"inline\">id"
        "</code> (например, на них ссылаются извне), их нужно переносить явно и после этого "
        "проверить, что они остались уникальными. Любой перенос данных должен заканчиваться "
        "проверкой: совпадает ли количество строк и совпадают ли представительные записи в "
        "источнике и в цели.",
    )}

    <p>Перенос между локальными файлами SQLite в этом примере воспроизводит тот же принцип,
    что и перенос в промышленную базу вроде PostgreSQL, — читать, преобразовывать, записывать,
    проверять. Отличаются только конкретные инструменты и драйверы подключения; сначала —
    обязательная резервная копия исходных данных.</p>

    {practice_card(
        "22-28",
        "Практика: перенос данных через JSON",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-28/index.html",
    )}
    """
    out = render_page(
        page_title="Перенос данных между базами",
        description="Перенос данных как отдельное значение слова «миграция», роль JSON как промежуточного формата и обязательная проверка результата.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Перенос данных", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Перенос данных между базами",
        lede="Не структура таблицы, а сами записи — как их переносят между базами и почему перенос обязательно проверяют.",
        body_html=body,
        sidebar_groups=sidebar("22-28-perenos-dannyh.html"),
        nav=PageNav(prev_href="22-27-migracii-shemy.html", prev_label="Миграции схемы базы данных", next_href="22-29-flask-sqlite.html", next_label="Flask и SQLite: сохраняем данные в базе"),
    )
    write("22-28-perenos-dannyh.html", out)


def build_29() -> None:
    body = f"""
    <p>Теперь список Python из раздела 22.5 заменяется базой данных SQLite. Схема простая —
    одна таблица:</p>
    {code_block(
        "schema.sql",
        "CREATE TABLE IF NOT EXISTS tasks (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    title TEXT NOT NULL,\n"
        "    done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))\n"
        ");",
        lang="sql",
    )}
    <p><code class="inline">CHECK (done IN (0, 1))</code> — дополнительное ограничение:
    SQLite не даст записать в столбец <code class="inline">done</code> ничего, кроме 0 или 1,
    даже если в коде приложения где-то закрадётся ошибка.</p>

    <h2>Одно подключение на запрос</h2>
    <p>Открывать соединение с базой на каждый маленький вызов — расточительно, а держать одно
    общее соединение на всё приложение без осторожности — рискованно при параллельных
    запросах. Flask предлагает удобное место для данных, которые должны жить ровно один
    запрос, — объект <code class="inline">g</code>:</p>
    {code_block(
        "app.py",
        'import sqlite3\n'
        'from flask import Flask, g\n\n'
        'app = Flask(__name__)\n'
        'app.config["DATABASE"] = "zadachi.db"\n\n\n'
        'def get_db():\n'
        '    if "db" not in g:\n'
        '        g.db = sqlite3.connect(app.config["DATABASE"])\n'
        '        g.db.row_factory = sqlite3.Row\n'
        "    return g.db\n\n\n"
        "@app.teardown_appcontext\n"
        "def close_db(exception=None):\n"
        '    db = g.pop("db", None)\n'
        "    if db is not None:\n"
        "        db.close()\n",
    )}
    {callout(
        "info",
        "g привязан к контексту приложения, а не буквально к запросу",
        "<code class=\"inline\">g</code> хранит данные в рамках <em>контекста приложения</em> "
        "Flask. При обычной обработке HTTP-запроса этот контекст живёт ровно с начала обработки "
        "запроса до его конца и создаётся заново для каждого следующего запроса — поэтому на "
        "практике <code class=\"inline\">g</code> ведёт себя как хранилище на один запрос, а "
        "не как общая переменная, из которой данные могут случайно «утечь» в другой запрос. "
        "<code class=\"inline\">teardown_appcontext</code> вызывается при закрытии контекста "
        "приложения, даже если обработчик завершился с ошибкой, — соединение всегда "
        "закрывается.",
    )}

    <h2>Маршруты поверх базы данных</h2>
    {code_block(
        "app.py",
        '@app.route("/")\n'
        "def glavnaya():\n"
        "    db = get_db()\n"
        '    zadachi = db.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()\n'
        '    return render_template("index.html", zadachi=zadachi)\n\n\n'
        '@app.route("/dobavit", methods=["POST"])\n'
        "def dobavit():\n"
        '    title = clean_title(request.form.get("zadacha", ""))\n'
        "    if title is None:\n"
        '        flash("Название задачи не может быть пустым и не длиннее 200 символов.")\n'
        '        return redirect(url_for("glavnaya"), code=303)\n'
        "    db = get_db()\n"
        '    db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))\n'
        "    db.commit()\n"
        '    return redirect(url_for("glavnaya"), code=303)\n',
    )}
    <p>Обратите внимание: <code class="inline">?</code> в SQL-запросе и значение отдельным
    аргументом — тот же параметризованный запрос из раздела 22.22, теперь внутри рабочего
    приложения. <code class="inline">clean_title(...)</code> — простая функция проверки из
    раздела 22.31: пустое или слишком длинное название отклоняется ещё до обращения к базе.</p>

    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div style="flex:1 1 260px;min-width:220px">
        {image_figure(
            f"{IMG}/08-todo-empty.png",
            "Пустой список задач: заголовок «Мой список задач», подпись «Задач пока нет — добавьте первую ниже» и поле ввода",
            "Список задач сразу после init_db() — таблица создана, но пуста.",
        )}
      </div>
      <div style="flex:1 1 260px;min-width:220px">
        {image_figure(
            f"{IMG}/09-todo-after-add.png",
            "Список задач с одной строкой «Купить хлеб» и пустым круглым чекбоксом слева",
            "После отправки формы: INSERT прошёл, редирект вернул на / — задача видна в списке.",
        )}
      </div>
      <div style="flex:1 1 260px;min-width:220px">
        {image_figure(
            f"{IMG}/10-todo-completed.png",
            "Тот же список: «Купить хлеб» зачёркнут, чекбокс слева с галочкой",
            "После клика по кружку: UPDATE tasks SET done = 1 — строка помечена как выполненная.",
        )}
      </div>
    </div>

    <p>Полный рабочий файл — со всеми маршрутами, обработкой ошибок и API — лежит здесь:</p>
    <p>[[icon:file]] <a href="../../../projects/flask/todo-app/app.py">projects/flask/todo-app/app.py</a></p>

    {callout(
        "tip",
        "Проверьте сами: перезапустите — задачи никуда не делись",
        "Запустите <code class=\"inline\">python app.py</code>, добавьте пару задач, "
        "остановите процесс (Ctrl+C) и запустите заново. Список останется тем же самым — "
        "именно то, чего не хватало версии из раздела 22.5.",
    )}

    {image_figure(
        f"{IMG}/12-todo-persisted-after-restart.png",
        "Список задач в браузере после перезапуска процесса: «Купить хлеб» по-прежнему отмечен выполненным, ниже добавлена новая строка «Написать тесты для API»",
        "Реальная проверка: процесс Flask был полностью остановлен и запущен заново на том же файле базы данных. «Купить хлеб» остался отмеченным, а новая задача, добавленная уже новым процессом, сохранилась рядом — файл SQLite пережил перезапуск, обычный список Python не пережил бы.",
        width=520,
    )}

    {local_required_card(
        "22-29",
        "Практика: Flask поверх SQLite",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-29/index.html",
    )}
    """
    out = render_page(
        page_title="Flask и SQLite: сохраняем данные в базе",
        description="Схема задач, подключение через g и teardown_appcontext, параметризованные запросы внутри маршрутов Flask.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Flask и SQLite", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Flask и SQLite: сохраняем данные в базе",
        lede="Список Python из раздела 22.5 становится таблицей SQLite, которая переживает перезапуск.",
        body_html=body,
        sidebar_groups=sidebar("22-29-flask-sqlite.html"),
        nav=PageNav(prev_href="22-28-perenos-dannyh.html", prev_label="Перенос данных между базами", next_href="22-30-cookies-session.html", next_label="Cookie и сессии: состояние между HTTP-запросами"),
    )
    write("22-29-flask-sqlite.html", out)


def build_30() -> None:
    body = f"""
    <p>HTTP-запросы независимы друг от друга: сам по себе протокол не связывает один запрос
    со следующим. Но приложению из раздела 22.29 уже нужно сохранять что-то между запросами —
    например, сообщение об ошибке, которое должно появиться на следующей странице после
    <code class="inline">flash(...)</code>. Для этого существуют cookie и сессионные
    механизмы.</p>

    <h2>Cookie — маленькое значение, которое хранит браузер</h2>
    <p><strong>Cookie</strong> — небольшой кусочек данных, который сервер просит браузер
    сохранить, а браузер затем прикладывает к следующим запросам на тот же сайт. Именно так
    сервер может связать несколько запросов друг с другом как пришедшие от одного и того же
    браузера.</p>

    {pipeline_diagram([
        {"kind": "plain", "title": "Запрос 1", "rows": ["сервер отправляет Set-Cookie"]},
        {"kind": "plain", "title": "Браузер", "rows": ["сохраняет cookie"]},
        {"kind": "plain", "title": "Запрос 2", "rows": ["браузер прикладывает cookie обратно"]},
        {"kind": "plain", "title": "Сервер", "rows": ["связывает запрос с тем же cookie"]},
    ], caption="Cookie передаётся вместе с каждым запросом к тому же сайту")}

    <h2>Сессия — механизм сохранения состояния между запросами</h2>
    <p><strong>Сессия</strong> (session) — механизм уровня приложения, который использует
    cookie, чтобы связать несколько запросов друг с другом и хранить между ними какие-то
    данные. Реализации бывают разными: данные сессии можно хранить на сервере (в базе данных
    или отдельном хранилище, а в cookie передавать только идентификатор), а можно — прямо в
    самом cookie на стороне браузера. Flask по умолчанию использует второй вариант и
    предоставляет готовый объект <code class="inline">session</code>, который ведёт себя как
    словарь:</p>
    {code_block(
        "session_primer.py",
        'from flask import session\n\n'
        'session["poslednij_vizit"] = "22-30"\n'
        '# на следующем запросе того же браузера:\n'
        'session.get("poslednij_vizit")   # "22-30"\n',
    )}
    <p>Функция <code class="inline">flash(...)</code>, использованная в разделе 22.29, устроена
    поверх того же механизма session: сообщение сохраняется в сессии на один следующий запрос
    и автоматически стирается после того, как его прочитали через
    <code class="inline">get_flashed_messages()</code> в шаблоне.</p>

    {callout(
        "warning",
        "Подписано — не значит зашифровано",
        "По умолчанию Flask хранит содержимое сессии прямо в cookie на стороне браузера, "
        "защищённое подписью с помощью <code class=\"inline\">SECRET_KEY</code>. Подпись "
        "гарантирует <strong>подлинность</strong>: если кто-то изменит содержимое cookie, "
        "подпись перестанет совпадать, и Flask отклонит такую сессию. Но подпись — "
        "<strong>не шифрование</strong>: содержимое сессии по умолчанию можно прочитать, не "
        "зная секретный ключ, — оно просто не поддаётся необнаруживаемому изменению. Никогда "
        "не кладите в сессию пароли или другие данные, которые должны оставаться "
        "нечитаемыми для пользователя, чей браузер их хранит.",
    )}

    <p>Проект этой главы намеренно останавливается здесь: полноценный вход пользователей
    (аутентификация) добавил бы главе объём отдельного курса. Где эта тема продолжается —
    в разделе 22.36.</p>

    {local_required_card(
        "22-30",
        "Практика: сообщение через flash() и session",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-30/index.html",
    )}
    """
    out = render_page(
        page_title="Cookie и сессии: состояние между HTTP-запросами",
        description="Cookie как переносчик данных между запросами, объект session во Flask, flash() и разница между подписанными и зашифрованными данными.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Cookies и session", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Cookie и сессии: состояние между HTTP-запросами",
        lede="HTTP-запросы независимы друг от друга — cookie и сессионные механизмы позволяют связать состояние между ними.",
        body_html=body,
        sidebar_groups=sidebar("22-30-cookies-session.html"),
        nav=PageNav(prev_href="22-29-flask-sqlite.html", prev_label="Flask и SQLite: сохраняем данные в базе", next_href="22-31-validaciya-oshibki.html", next_label="Проверка входных данных и обработка ошибок"),
    )
    write("22-30-cookies-session.html", out)


def build_31() -> None:
    body = f"""
    <p>Раздел 22.4 показал проверку формы в браузере через JavaScript. Это удобно для
    пользователя, но никогда не единственная линия защиты: запрос можно отправить и вовсе без
    браузера — например, программой, которая обращается прямо к <code class="inline">/dobavit
    </code> или <code class="inline">/api/tasks</code>, без единой строчки JavaScript. Входные
    данные необходимо повторно проверять на серверной стороне в каждом маршруте, который их
    принимает.</p>

    {callout(
        "warning",
        "Не доверяйте вводу только потому, что он пришёл из вашей формы",
        "HTML-форма из раздела 22.13 задаёт <code class=\"inline\">required</code> и "
        "<code class=\"inline\">maxlength</code> — но это подсказки для браузера, а не "
        "гарантия. Ничто не мешает отправить POST-запрос на <code class=\"inline\">/dobavit"
        "</code> напрямую, в обход формы и любых её ограничений.",
    )}

    <h2>Проверка в проекте главы</h2>
    {code_block(
        "app.py",
        "MAX_TITLE_LENGTH = 200\n\n\n"
        "def clean_title(raw_title):\n"
        "    title = raw_title.strip()\n"
        "    if not title or len(title) > MAX_TITLE_LENGTH:\n"
        "        return None\n"
        "    return title\n",
    )}
    <p><code class="inline">strip()</code> убирает случайные пробелы по краям (например, если
    пользователь нажал пробел, а затем Enter). Пустая строка после этого и слишком длинная
    строка — оба случая считаются недопустимыми и возвращают <code class="inline">None</code>.</p>

    <h2>HTML-маршрут и API-маршрут реагируют на ошибку по-разному</h2>
    {comparison_table(
        ["", "HTML-форма (/dobavit)", "API (/api/tasks)"],
        [
            ["Кто читает ответ", "Человек в браузере", "Программа"],
            ["Реакция на невалидные данные", "flash(...) с понятным текстом и редирект обратно (раздел 22.30)", "Код 400 и тело JSON с описанием ошибки"],
            ["Пример ответа", "Страница со списком задач и сообщением сверху", "<code class=\"inline\">{{\"error\": \"title не может быть пустым\"}}</code>"],
        ],
    )}

    {image_figure(
        f"{IMG}/11-todo-validation-error.png",
        "Список задач с розовым сообщением сверху: «Название задачи не может быть пустым и не длиннее 200 символов.»",
        "Реальный результат отправки формы с полем из одних пробелов: clean_title() вернул None, flash() показал сообщение, редирект вернул на ту же страницу — задача не добавлена.",
        width=520,
    )}

    {code_block(
        "app.py",
        'data = request.get_json(silent=True)\n'
        'if not isinstance(data, dict) or not isinstance(data.get("title"), str):\n'
        '    return jsonify({{"error": "поле title обязательно и должно быть строкой"}}), 400\n'
        'title = clean_title(data["title"])\n'
        "if title is None:\n"
        '    return jsonify({{"error": "title не может быть пустым и не длиннее 200 символов"}}), 400\n',
    )}

    <h2>404 — обращение к тому, чего нет</h2>
    <p>Если попытаться отметить выполненной или удалить задачу с несуществующим
    <code class="inline">id</code>, маршрут вызывает <code class="inline">abort(404)</code> —
    Flask сразу возвращает стандартную страницу ошибки (или JSON для API-путей, раздел 22.9),
    не выполняя код дальше.</p>

    {practice_card(
        "22-31",
        "Практика: проверяем ввод",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-31/index.html",
    )}
    """
    out = render_page(
        page_title="Проверка входных данных и обработка ошибок",
        description="Почему проверка на сервере обязательна независимо от JavaScript, clean_title() в проекте главы и разница между HTML- и JSON-ошибками.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Проверка данных", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Проверка входных данных и обработка ошибок",
        lede="Форма в браузере — не единственный способ отправить запрос, поэтому проверка на сервере обязательна.",
        body_html=body,
        sidebar_groups=sidebar("22-31-validaciya-oshibki.html"),
        nav=PageNav(prev_href="22-30-cookies-session.html", prev_label="Cookie и сессии: состояние между HTTP-запросами", next_href="22-32-bezopasnost.html", next_label="Основы безопасности веб-приложений"),
    )
    write("22-31-validaciya-oshibki.html", out)


def build_32() -> None:
    body = f"""
    <p>Веб-безопасность — большая тема; здесь — только самые частые ошибки и принципы,
    которые нужно знать даже в маленьком проекте. Глубокое изучение остаётся будущему
    специализированному курсу (раздел 22.36).</p>

    <h2>SQL-инъекция</h2>
    <p>Если собрать SQL-запрос склеиванием строк с пользовательским вводом, часть введённого
    текста может быть воспринята как часть самого запроса, а не как данные:</p>
    {code_block(
        "opasno.py",
        '# ТАК ДЕЛАТЬ НЕЛЬЗЯ\n'
        'db.execute(f"SELECT * FROM tasks WHERE title = \'{{user_input}}\'")\n',
    )}
    {code_block(
        "bezopasno.py",
        'db.execute("SELECT * FROM tasks WHERE title = ?", (user_input,))',
    )}
    <p>Раздел 22.22 уже показывал этот приём — <strong>параметризованный запрос</strong>,
    где значение передаётся отдельно от текста SQL и никогда не смешивается с ним. Модуль
    <code class="inline">sqlite3</code> сам отвечает за то, чтобы значение осталось данными,
    что бы в нём ни было — даже фрагмент, похожий на SQL.</p>

    <h2>XSS — межсайтовый скриптинг</h2>
    <p>Если чужой текст попадает в HTML-страницу без обработки, он может содержать
    исполняемый код, который выполнится в браузере другого пользователя, — например,
    <code class="inline">&lt;script&gt;...&lt;/script&gt;</code> в названии задачи. Раздел
    22.12 уже показал защиту: в автоэкранируемом HTML-контексте Jinja заменяет специальные
    символы HTML соответствующими escape-последовательностями, поэтому введённый текст не
    интерпретируется как разметка. Это не делает значение безопасным вставлять куда угодно —
    например, внутрь атрибута <code class="inline">&lt;script&gt;</code> или URL нужна уже
    другая защита, — именно поэтому фильтр <code class="inline">|safe</code>, который вообще
    отключает экранирование, нельзя применять к вводу, который вы не полностью контролируете
    сами.</p>

    <h2>CSRF — подделка межсайтового запроса</h2>
    <p>CSRF (Cross-Site Request Forgery) актуален там, где браузер автоматически прикладывает
    учётные данные (например, cookie сессии, раздел 22.30) к запросам, а сам запрос меняет
    состояние на сервере: пользователь, залогиненный на сайте, открывает другую, вредоносную
    страницу, а та страница теоретически может незаметно отправить от его имени запрос на ваш
    сайт — браузер сам приложит те же cookie. Пока в проекте главы нет входа пользователей,
    риск CSRF ограничен, но для приложений, где авторизация или состояние опираются на
    автоматически отправляемые браузером cookie, изменяющие состояние запросы должны быть
    защищены от CSRF соответствующим механизмом — обычно его предоставляет сам фреймворк или
    расширение.</p>

    <h2>Пароли</h2>
    <p>Пароли никогда не хранят как обычный текст — только в виде хеша, полученного через
    проверенный, специально предназначенный для паролей инструмент. Изобретать собственную
    схему хеширования паролей не нужно и не стоит — для этого есть готовые, тщательно
    проверенные библиотеки. Проект этой главы не хранит пароли вообще: раздел 22.30 уже
    объяснил, почему полноценный вход пользователей остался за пределами этой главы.</p>

    <h2>Секреты</h2>
    <p><code class="inline">SECRET_KEY</code> приложения, пароли к базе данных, ключи внешних
    API — всё это не должно попадать в публичный исходный код. Как такие значения обычно
    передают через переменные окружения вместо того, чтобы записывать их прямо в файл с
    кодом, — в разделе 22.34.</p>

    <h2>HTTPS — ещё раз, коротко</h2>
    <p>Раздел 22.10 уже объяснил: HTTPS защищает данные <em>по пути</em> между браузером и
    сервером, но не устраняет ошибки внутри самого приложения — SQL-инъекцию, XSS или утечку
    секретов HTTPS не остановит. Это разные, дополняющие друг друга уровни защиты.</p>

    {practice_card(
        "22-32",
        "Практика: параметризация против инъекции",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/22-32/index.html",
    )}
    """
    out = render_page(
        page_title="Основы безопасности веб-приложений",
        description="SQL-инъекция, XSS, CSRF, хранение паролей и секретов — базовые принципы безопасности на уровне, достаточном для первого приложения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Основы безопасности", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Основы безопасности веб-приложений",
        lede="Несколько частых ошибок и принципов, которые нужно знать даже в маленьком проекте.",
        body_html=body,
        sidebar_groups=sidebar("22-32-bezopasnost.html"),
        nav=PageNav(prev_href="22-31-validaciya-oshibki.html", prev_label="Проверка входных данных и обработка ошибок", next_href="22-33-testiruem-flask.html", next_label="Автоматическое тестирование Flask-приложения"),
    )
    write("22-32-bezopasnost.html", out)


def build_33() -> None:
    body = f"""
    <p>Проверять каждое изменение вручную через браузер медленно и легко забыть повторить
    после следующей правки. У Flask есть встроенный <strong>тестовый клиент</strong> — он
    позволяет отправлять запросы приложению из кода теста и проверять ответ.</p>

    {callout(
        "warning",
        "Тестовый клиент не открывает сетевой порт",
        "<code class=\"inline\">app.test_client()</code> не создаёт сетевое HTTP-соединение. "
        "Он формирует запрос внутри процесса и передаёт его напрямую обработчику Flask через "
        "тестовый интерфейс библиотеки Werkzeug, на которой построен Flask, — быстро и без "
        "сети, но с той же логикой обработки запроса. Полный путь запроса через браузер и сеть "
        "показывал раздел 22.7 — тестовый клиент сознательно пропускает именно эту часть.",
    )}

    {code_block(
        "test_app.py",
        'import app as todoapp\n\n'
        'def test_glavnaya_pustoj_spisok(baza_dannyh):\n'
        "    client = todoapp.app.test_client()\n"
        '    otvet = client.get("/")\n'
        "    assert otvet.status_code == 200\n"
        '    assert "Задач пока нет" in otvet.get_data(as_text=True)\n',
    )}

    <h2>Проверка JSON-ответа</h2>
    {code_block(
        "test_api.py",
        'def test_api_tasks_vozvrashchaet_json(baza_dannyh):\n'
        "    client = todoapp.app.test_client()\n"
        '    otvet = client.get("/api/tasks")\n'
        "    assert otvet.status_code == 200\n"
        '    assert otvet.content_type == "application/json"\n'
        "    dannye = otvet.get_json()\n"
        "    assert isinstance(dannye, list)\n",
    )}
    <p><code class="inline">otvet.get_json()</code> сам разбирает тело ответа как JSON —
    это то же самое, что <code class="inline">json.loads(otvet.get_data())</code> из раздела
    22.15, но короче.</p>

    <h2>Отдельная база данных для тестов</h2>
    <p>Тесты не должны трогать ту же базу данных, с которой вы работаете вручную, — иначе
    прогон тестов может стереть или испортить сохранённые в ней задачи. Перед каждым тестом
    создаётся временная база данных, а после — удаляется:</p>
    {code_block(
        "conftest.py",
        'import tempfile\n'
        'import os\n'
        'import pytest\n\n'
        'import app as todoapp\n\n\n'
        '@pytest.fixture\n'
        "def baza_dannyh():\n"
        "    fd, put = tempfile.mkstemp()\n"
        '    todoapp.app.config["DATABASE"] = put\n'
        "    with todoapp.app.app_context():\n"
        "        todoapp.init_db()\n"
        "    yield put\n"
        "    os.close(fd)\n"
        "    os.unlink(put)\n",
    )}
    <p>Полный набор тестов проекта — в <code class="inline">tests/test_chapter22_todo_app.py</code>
    в репозитории книги; он проверяет маршруты, сохранение в базе, валидацию, JSON API и
    защиту от SQL-инъекции и XSS из разделов 22.31-22.32.</p>

    {local_required_card(
        "22-33",
        "Практика: тесты для Flask-приложения",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-33/index.html",
    )}
    """
    out = render_page(
        page_title="Автоматическое тестирование Flask-приложения",
        description="Тестовый клиент Flask, проверка HTML- и JSON-ответов, временная база данных для тестов и правильная формулировка того, что тестовый клиент делает.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Тестируем Flask", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Автоматическое тестирование Flask-приложения",
        lede="Тестовый клиент проверяет логику приложения быстро и без обращения к сети.",
        body_html=body,
        sidebar_groups=sidebar("22-33-testiruem-flask.html"),
        nav=PageNav(prev_href="22-32-bezopasnost.html", prev_label="Основы безопасности веб-приложений", next_href="22-34-razvyortyvanie.html", next_label="Развёртывание Flask-приложения"),
    )
    write("22-33-testiruem-flask.html", out)


def build_34() -> None:
    body = f"""
    <p>Раздел 22.5 запускал приложение командой <code class="inline">python app.py</code>,
    которая внутри вызывает <code class="inline">app.run(debug=True)</code>. Это
    <strong>сервер разработки</strong> (development server) — встроенный во Flask, удобный
    для локальной работы, но не предназначенный для реальной эксплуатации. Раздел
    «Deploying to Production» официальной документации Flask прямо предупреждает об этом.</p>

    {comparison_table(
        ["", "Среда разработки", "Рабочее развёртывание"],
        [
            ["Кто использует", "Вы сами, локально", "Реальные пользователи через интернет"],
            ["Сервер", "Встроенный сервер разработки Flask", "Отдельный сервер приложений (раздел 22.19)"],
            ["debug=True", "Удобно — подробные ошибки, автоперезапуск", "Опасно — может показать посторонним внутренние детали кода и данные"],
            ["Секреты (SECRET_KEY и т.п.)", "Можно временное значение для локальной работы", "Обязательно отдельное, не публикуемое значение"],
        ],
    )}

    {callout(
        "warning",
        "debug=True в открытом приложении — реальная уязвимость",
        "В режиме отладки Flask может показать интерактивный отладчик с полным доступом к "
        "выполнению кода прямо в браузере при необработанной ошибке. Это огромное удобство "
        "локально и серьёзный риск, если приложение доступно кому-то ещё, — отладочный режим "
        "должен быть выключен в любом развёртывании, доступном не только вам.",
    )}

    <h2>Путь запроса до рабочего приложения</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "Браузер", "rows": ["пользователь в интернете"]},
        {"kind": "plain", "title": "HTTPS / обратный прокси", "rows": ["раздел 22.10"]},
        {"kind": "plain", "title": "Сервер приложений", "rows": ["Gunicorn, Uvicorn… (раздел 22.19)"]},
        {"kind": "plain", "title": "Flask-приложение", "rows": ["та же логика, что и локально"]},
        {"kind": "plain", "title": "База данных", "rows": ["отдельное надёжное хранилище"]},
    ], caption="Тот же Flask-код — но между браузером и им теперь несколько дополнительных слоёв")}

    <h2>Конфигурация через переменные окружения</h2>
    <p>Проект этой главы уже читает путь к базе данных и секретный ключ из переменных
    окружения, с явным резервным значением для локальной разработки:</p>
    {code_block(
        "app.py",
        'app.config["DATABASE"] = os.environ.get("TODO_APP_DB", str(DEFAULT_DB_PATH))\n'
        'app.config["SECRET_KEY"] = os.environ.get(\n'
        '    "TODO_APP_SECRET_KEY", "dev-only-secret-do-not-use-in-production"\n'
        ")\n",
    )}
    <p>Так один и тот же код работает и локально (без единой настройки), и в другом окружении
    — там, где нужно, значения переменных окружения просто задают иначе, не трогая сам код.</p>

    <h2>Логи, несколько процессов, персистентность</h2>
    <p>У рабочего развёртывания есть и другие практические заботы, которые выходят за рамки
    этой главы: <strong>логи</strong> (записанная история происходящего, чтобы разбирать
    проблемы постфактум), запуск <strong>нескольких процессов или потоков</strong>
    одновременно для обработки параллельных запросов, и то, что база данных должна физически
    находиться на надёжном, не исчезающем хранилище. Мы намеренно не превращаем эту главу в
    учебник по эксплуатации — где эта тема продолжается, показывает раздел 22.36.</p>

    <p>Официальная документация: <a href="https://flask.palletsprojects.com/en/stable/deploying/">Flask — Deploying to Production</a>.</p>
    """
    out = render_page(
        page_title="Развёртывание Flask-приложения",
        description="Разница между сервером разработки Flask и рабочим развёртыванием, конфигурация через переменные окружения и что остаётся за рамками главы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("После разработки", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Развёртывание Flask-приложения",
        lede="Сервер разработки Flask удобен локально — но не для того, что доступно всему интернету.",
        body_html=body,
        sidebar_groups=sidebar("22-34-razvyortyvanie.html"),
        nav=PageNav(prev_href="22-33-testiruem-flask.html", prev_label="Автоматическое тестирование Flask-приложения", next_href="22-35-itogovyj-proekt.html", next_label="Итоговый проект: список задач на Flask и SQLite"),
    )
    write("22-34-razvyortyvanie.html", out)


def build_35() -> None:
    body = f"""
    <p>Всё, что разбирали разделы 22.7-22.34, сходится в одном рабочем приложении — том же
    списке задач, с которого началась глава, теперь с постоянным хранением в SQLite.</p>

    <p>[[icon:file]] <a href="../../../projects/flask/todo-app/app.py">projects/flask/todo-app/app.py</a></p>

    {comparison_table(
        ["Файл", "Роль"],
        [
            ["app.py", "Маршруты, работа с базой данных, API"],
            ["schema.sql", "Структура таблицы tasks"],
            ["templates/base.html", "Общий каркас страницы, включая сообщения flash()"],
            ["templates/index.html", "Список задач, форма добавления"],
            ["templates/privet.html", "Историческая страница приветствия из раздела 22.5"],
            ["templates/404.html", "Страница «не найдено»"],
            ["static/style.css", "Собственные стили, без внешних CDN"],
        ],
    )}

    <h2>Что умеет готовое приложение</h2>
    {capability_map([
        ("Список задач", ["GET / — показывает все задачи", "Пустое состояние, если задач нет"]),
        ("Добавление", ["POST /dobavit", "Проверка ввода (раздел 22.31)", "POST-Redirect-GET (раздел 22.13)"]),
        ("Отметка выполнения", ["POST /vypolnit/<id>", "Переключает done между 0 и 1"]),
        ("Удаление", ["POST /udalit/<id>", "Полностью убирает строку из базы"]),
        ("JSON API", ["GET /api/tasks — список", "POST /api/tasks — добавление с JSON-телом"]),
    ], title="Пять возможностей одного маленького приложения")}

    {image_figure(
        f"{IMG}/05-flask-todo-final.png",
        "Итоговый список задач в браузере: две выполненные (зачёркнутые) задачи вверху и две ещё не выполненные ниже, поле добавления и кнопка «Поздороваться» снизу",
        "Локально запущенное Flask-приложение в браузере — итоговый вид проекта: выполненные и невыполненные задачи, форма добавления и ссылка на историческую страницу /privet/<имя> из раздела 22.5.",
        width=520,
    )}

    {callout(
        "info",
        "Удаление и отметка выполнения — тоже POST, не GET",
        "Раздел 22.9 уже объяснял: GET не должен менять состояние на сервере, потому что "
        "браузер может повторить его без предупреждения — например, при обновлении страницы. "
        "Поэтому у кнопок «Выполнено» и «Удалить» в шаблоне — собственные маленькие формы с "
        "<code class=\"inline\">method=\"post\"</code>, а не простые ссылки "
        "<code class=\"inline\">&lt;a href=\"/udalit/…\"&gt;</code>.",
    )}

    <h2>Запуск</h2>
    {code_block(
        "terminal.txt",
        "cd projects/flask/todo-app\n"
        "python app.py",
        lang="text",
    )}
    <p>Первый запуск сам создаёт файл базы данных и таблицу — отдельная команда для этого не
    нужна. Откройте <code class="inline">http://127.0.0.1:5000/</code>: добавьте задачу,
    отметьте её выполненной, удалите, обновите страницу посреди процесса, перезапустите сам
    процесс и убедитесь, что список остался прежним.</p>

    <p>Приложение работает и на узких экранах: раскладка CSS (раздел 22.3) перестраивается
    под мобильную ширину без горизонтальной прокрутки страницы.</p>

    {exercise(2, "Счётчик оставшихся задач", "Добавьте в index.html строку с числом невыполненных задач — {{ zadachi|selectattr('done', 'equalto', 0)|list|length }}.")}
    {exercise(3, "Сортировка по статусу", "Измените запрос в glavnaya(), чтобы невыполненные задачи всегда показывались раньше выполненных — ORDER BY done, id.")}

    {local_required_card(
        "22-35",
        "Практика: работаем с готовым проектом",
        "Модуль flask не установлен в браузерном окружении Pyodide — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/22-35/index.html",
    )}
    """
    out = render_page(
        page_title="Итоговый проект: список задач на Flask и SQLite",
        description="Полный обзор итогового проекта главы: маршруты, шаблоны, база данных, JSON API, POST-Redirect-GET и запуск приложения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Итоговый проект", "")],
        kicker="Глава 22 · Проект: список задач",
        h1="Итоговый проект: список задач на Flask и SQLite",
        lede="Тот же список задач, с которого началась глава, — теперь с постоянным хранением, JSON API и проверкой ввода.",
        body_html=body,
        sidebar_groups=sidebar("22-35-itogovyj-proekt.html"),
        nav=PageNav(prev_href="22-34-razvyortyvanie.html", prev_label="Развёртывание Flask-приложения", next_href="22-36-chto-dalshe.html", next_label="Дальнейшее изучение веб-разработки на Python"),
    )
    write("22-35-itogovyj-proekt.html", out)


def build_36() -> None:
    body = f"""
    {summary_box("Что теперь понятно после этой главы", [
        "Как устроен диалог браузера и сервера: запрос, ответ, HTTP и HTTPS.",
        "Из чего состоит фронтенд — HTML, CSS, JavaScript — и что каждый из них делает.",
        "Как Flask превращает функции Python в обработчики HTTP-запросов через маршруты.",
        "Как шаблоны Jinja собирают HTML из данных, и почему автоэкранирование включено по умолчанию.",
        "Что такое JSON и API, и чем ответ с данными отличается от HTML-страницы.",
        "Чем отличаются друг от друга Flask, Django и FastAPI — и что такое WSGI и ASGI.",
        "Зачем нужна база данных, что такое SQL, и чем реляционные базы отличаются от нереляционных.",
        "Что такое миграция схемы и перенос данных — и почему это два разных значения одного слова.",
        "Базовые принципы безопасности: параметризованные запросы, автоэкранирование, секреты.",
        "Как проверить Flask-приложение тестами и чем сервер разработки отличается от рабочего развёртывания.",
    ])}

    <p>Вы прошли путь от обмена сообщениями по HTTP между браузером и сервером до работающего
    приложения с базой данных, JSON API и тестами — солидная основа, но далеко не вся
    веб-разработка. {FUTURE_COURSE}</p>

    {capability_map([
        ("Фреймворки глубже", ["Архитектура Flask за пределами основ", "Django целиком", "FastAPI и типизированные API"]),
        ("Базы данных", ["PostgreSQL на практике", "SQLAlchemy и Alembic", "ORM и миграции Django"]),
        ("API и обмен данными", ["REST подробно", "OpenAPI", "Аутентификация и авторизация"]),
        ("Параллельность и реальное время", ["Асинхронный Python", "ASGI на практике", "WebSocket"]),
        ("Инфраструктура сервиса", ["Фоновые задачи", "Redis и кеширование", "Docker, обратные прокси, CI/CD"]),
        ("Эксплуатация", ["Конфигурация и секреты", "Логи, метрики, наблюдаемость", "Рабочее развёртывание"]),
    ], title="Чем займётся будущий специализированный курс")}

    <p>А следующая глава книги возвращается к настольным мини-проектам на Python — совсем
    другая часть языка в деле.</p>
    """
    out = render_page(
        page_title="Дальнейшее изучение веб-разработки на Python",
        description="Итоги главы 22 целиком и обзор направлений для дальнейшего изучения — от основ HTTP и Flask до отдельного специализированного курса.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 22", "index.html"), ("Что дальше", "")],
        kicker="Глава 22 · Веб-разработка с Python",
        h1="Дальнейшее изучение веб-разработки на Python",
        lede="От первого HTTP-запроса до работающего приложения с базой данных — и куда двигаться дальше.",
        body_html=body,
        sidebar_groups=sidebar("22-36-chto-dalshe.html"),
        nav=PageNav(prev_href="22-35-itogovyj-proekt.html", prev_label="Итоговый проект: список задач на Flask и SQLite", next_href="../glava-23/index.html", next_label="Глава 23: Ещё больше мини-проектов"),
    )
    write("22-36-chto-dalshe.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
    build_07()
    build_08()
    build_09()
    build_10()
    build_11()
    build_12()
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_22()
    build_23()
    build_24()
    build_25()
    build_26()
    build_27()
    build_28()
    build_29()
    build_30()
    build_31()
    build_32()
    build_33()
    build_34()
    build_35()
    build_36()
