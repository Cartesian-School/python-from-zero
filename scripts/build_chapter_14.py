#!/usr/bin/env python3
"""Строит Главу 14: «Создаём объекты реального мира» (site/chapters/glava-14/)."""

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
    local_required_card,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-14"

PAGES = [
    ("index.html", "Обзор главы"),
    ("14-01-chto-takoe-oop.html", "Что такое ООП?"),
    ("14-02-klassy.html", "Классы и объекты со своими значениями"),
    ("14-03-upravlyaem-obektami.html", "Управляем объектами. Действия объектов"),
    ("14-04-gonka-turtle-obekty-itogi.html", "Гонка Turtle с объектами и итоги"),
]

LESSON_IDS = ["14-01", "14-02", "14-03", "14-04"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 14 · Объекты", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=14,
        baseline_page=311,
        title="Создаём объекты реального мира",
        description="Классы, объекты, атрибуты и методы — основы объектно-ориентированного программирования.",
        meta_items=["⏱ ~2 часа", "🧱 class и self", "📓 4 ноутбука практики"],
        sections=[
            ChapterSectionLink("14.1", "Что такое объектно-ориентированное программирование?", "14-01-chto-takoe-oop.html", "312"),
            ChapterSectionLink("", "Давайте это докажем!", "14-01-chto-takoe-oop.html#dokazhem", "313"),
            ChapterSectionLink("14.2", "Классы", "14-02-klassy.html", "314"),
            ChapterSectionLink("", "Объекты со своими значениями", "14-02-klassy.html#znacheniya", "315"),
            ChapterSectionLink("14.3", "Управляем объектами", "14-03-upravlyaem-obektami.html", "317"),
            ChapterSectionLink("", "Объекты выполняют действия", "14-03-upravlyaem-obektami.html#dejstviya", "318"),
            ChapterSectionLink("14.4", "Гонка Turtle с объектами", "14-04-gonka-turtle-obekty-itogi.html", "319"),
            ChapterSectionLink("", "Итоги", "14-04-gonka-turtle-obekty-itogi.html#itogi", "322"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Что такое объектно-ориентированное программирование?</h2>
    <p>Присмотритесь к коду из предыдущих глав: <code class="inline">artist.forward(100)</code>,
    <code class="inline">"Python".upper()</code>, <code class="inline">[1,2,3].append(4)</code>
    — во всех трёх у нас есть какой-то <strong>объект</strong> (черепашка, строка, список) и
    команда, которую мы у него вызываем через точку. Это и есть объектно-ориентированное
    программирование (ООП): способ организовать код вокруг объектов, у которых есть свои
    данные и свои действия — а не только вокруг отдельных функций и переменных.</p>

    <h2 id="dokazhem">Давайте это докажем!</h2>
    <p>Вы уже пользовались объектами с самой главы 6, даже не называя их так:</p>
    {code_block(
        "vy_uzhe_polzovalis_obektami.py",
        "import turtle\n\n"
        "artist = turtle.Turtle()   # artist — объект класса Turtle\n"
        "artist.forward(100)         # forward() — действие (метод) этого объекта\n"
        "artist.color(\"red\")         # у объекта есть и своё состояние — например, цвет\n",
    )}
    <p><code class="inline">turtle.Turtle</code> — это <strong>класс</strong>: чертёж, шаблон,
    описывающий, какими бывают черепашки и что они умеют. Каждый вызов
    <code class="inline">turtle.Turtle()</code> создаёт новый, независимый
    <strong>объект</strong> (говорят также «экземпляр класса») по этому чертежу — вспомните
    главу 12, где несколько независимых черепашек участвовали в гонке одновременно.</p>

    {practice_card(
        "14-01",
        "Практика: находим объекты в уже знакомом коде",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-01/index.html",
    )}
    """
    out = render_page(
        page_title="Что такое объектно-ориентированное программирование?",
        description="Введение в ООП: классы и объекты на примере уже знакомого кода (Turtle, строки, списки).",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 14", "index.html"), ("Что такое ООП?", "")],
        kicker="Глава 14 · Создаём объекты реального мира",
        h1="Что такое объектно-ориентированное программирование?",
        lede="Вы уже пользовались объектами много глав подряд — просто ещё не называли их так.",
        body_html=body,
        sidebar_groups=sidebar("14-01-chto-takoe-oop.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="14-02-klassy.html", next_label="Классы"),
    )
    write("14-01-chto-takoe-oop.html", out)


def build_02() -> None:
    body = f"""
    <h2>Классы</h2>
    <p>Определим свой собственный класс — чертёж для объекта «Собака»:</p>
    {code_block(
        "klass_sobaka.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast):\n"
        "        self.klichka = klichka\n"
        "        self.vozrast = vozrast\n\n"
        "rex = Sobaka(\"Рекс\", 3)\n"
        "print(rex.klichka, rex.vozrast)\n",
    )}
    <p><code class="inline">__init__</code> — специальный метод, который автоматически
    выполняется при создании объекта (<code class="inline">Sobaka("Рекс", 3)</code>) и настраивает
    его начальное состояние. <code class="inline">self</code> — ссылка на сам создаваемый объект;
    Python передаёт её автоматически, и первым параметром <code class="inline">__init__</code>
    (и любого другого метода) она должна быть всегда.</p>

    {callout(
        "info",
        "Класс vs объект — аналогия с формой для печенья",
        "Класс — как форма для печенья: одна и та же форма может «вырезать» сколько угодно "
        "печений (объектов) — каждое своё, но по одному и тому же шаблону.",
    )}

    <h2 id="znacheniya">Объекты со своими значениями</h2>
    <p>Каждый объект хранит свои собственные значения атрибутов, независимо от других объектов
    того же класса:</p>
    {code_block(
        "raznye_obekty.py",
        'rex = Sobaka("Рекс", 3)\n'
        'sharik = Sobaka("Шарик", 5)\n\n'
        "print(rex.klichka, rex.vozrast)      # Рекс 3\n"
        "print(sharik.klichka, sharik.vozrast)  # Шарик 5 — независимо от rex\n",
    )}

    {practice_card(
        "14-02",
        "Практика: создаём собственные классы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-02/index.html",
    )}
    """
    out = render_page(
        page_title="Классы",
        description="Определение классов через class и __init__, создание объектов со своими значениями.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 14", "index.html"), ("Классы", "")],
        kicker="Глава 14 · Создаём объекты реального мира",
        h1="Классы",
        lede="Пишем свой первый класс — чертёж, по которому Python будет создавать объекты.",
        body_html=body,
        sidebar_groups=sidebar("14-02-klassy.html"),
        nav=PageNav(prev_href="14-01-chto-takoe-oop.html", prev_label="Что такое ООП?", next_href="14-03-upravlyaem-obektami.html", next_label="Управляем объектами"),
    )
    write("14-02-klassy.html", out)


def build_03() -> None:
    body = f"""
    <h2>Управляем объектами</h2>
    <p>Значения атрибутов можно менять уже после создания объекта — так же, как менять значение
    обычной переменной:</p>
    {code_block(
        "menyaem_atributy.py",
        'rex = Sobaka("Рекс", 3)\n'
        "rex.vozrast = 4   # у Рекса был день рождения\n"
        "print(rex.vozrast)\n",
    )}

    <h2 id="dejstviya">Объекты выполняют действия</h2>
    <p>Кроме данных (атрибутов), у класса могут быть свои действия — <strong>методы</strong>:
    обычные функции, определённые внутри класса, которые имеют доступ к
    <code class="inline">self</code> и, через него, к атрибутам объекта:</p>
    {code_block(
        "metody.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast):\n"
        "        self.klichka = klichka\n"
        "        self.vozrast = vozrast\n\n"
        "    def layat(self):\n"
        '        print(f"{self.klichka} говорит: Гав-гав!")\n\n'
        "    def prazdnovat_den_rozhdeniya(self):\n"
        "        self.vozrast += 1\n"
        '        print(f"Теперь {self.klichka} исполнилось {self.vozrast}!")\n\n'
        'rex = Sobaka("Рекс", 3)\n'
        "rex.layat()\n"
        "rex.prazdnovat_den_rozhdeniya()\n",
    )}
    {callout(
        "tip",
        "Знакомая запись",
        "<code class=\"inline\">rex.layat()</code> устроена точно так же, как "
        "<code class=\"inline\">artist.forward(100)</code> или "
        "<code class=\"inline\">\"текст\".upper()</code> — методы объектов, которыми вы уже "
        "давно пользуетесь, устроены абсолютно так же, как метод <code class=\"inline\">layat"
        "()</code>, который вы только что написали сами.",
    )}

    {practice_card(
        "14-03",
        "Практика: методы и изменение атрибутов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-03/index.html",
    )}
    """
    out = render_page(
        page_title="Управляем объектами. Объекты выполняют действия",
        description="Изменение атрибутов объекта и определение собственных методов класса.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 14", "index.html"), ("Управляем объектами", "")],
        kicker="Глава 14 · Создаём объекты реального мира",
        h1="Управляем объектами",
        lede="Атрибуты можно менять после создания объекта — а методы дают объекту собственные "
        "действия.",
        body_html=body,
        sidebar_groups=sidebar("14-03-upravlyaem-obektami.html"),
        nav=PageNav(prev_href="14-02-klassy.html", prev_label="Классы", next_href="14-04-gonka-turtle-obekty-itogi.html", next_label="Гонка Turtle с объектами и итоги"),
    )
    write("14-03-upravlyaem-obektami.html", out)


def build_04() -> None:
    body = f"""
    <p>Вернёмся к гонке черепашек из главы 12 — на этот раз обернём каждого участника в свой
    собственный класс, а не просто в объект <code class="inline">turtle.Turtle</code> напрямую.</p>
    {code_block(
        "gonka_s_klassom.py",
        "import random\n\n"
        "class Uchastnik:\n"
        "    def __init__(self, cvet, startovyj_y):\n"
        "        self.t = turtle.Turtle()\n"
        '        self.t.shape("turtle")\n'
        "        self.t.color(cvet)\n"
        "        self.t.penup()\n"
        "        self.t.goto(-200, startovyj_y)\n"
        "        self.cvet = cvet\n\n"
        "    def sdelat_shag(self):\n"
        "        self.t.forward(random.randint(1, 10))\n\n"
        "    def finishiroval(self, finish_line):\n"
        "        return self.t.xcor() >= finish_line\n\n"
        'cveta = ["red", "blue", "green", "orange"]\n'
        "uchastniki = [Uchastnik(cvet, i * 40 - 60) for i, cvet in enumerate(cveta)]\n\n"
        "pobeditel = None\n"
        "while pobeditel is None:\n"
        "    for u in uchastniki:\n"
        "        u.sdelat_shag()\n"
        "        if u.finishiroval(200):\n"
        "            pobeditel = u.cvet\n"
        "            break\n\n"
        'print(f"Победил участник цвета {pobeditel}!")\n',
    )}
    {callout(
        "info",
        "Зачем оборачивать Turtle в свой класс?",
        "В главе 12 логика гонки (движение, проверка финиша) была разбросана по основному "
        "коду. Теперь каждый участник — самостоятельный объект <code class=\"inline\">"
        "Uchastnik</code>, который сам знает, как сделать шаг и как проверить, финишировал ли "
        "он. Для маленькой гонки разница не критична, но в более крупных программах именно "
        "так поддерживают порядок при росте кода.",
    )}
    {exercise(3, "Счёт очков", "Добавьте классу Uchastnik атрибут ochki и метод nabrat_ochki(n), увеличивающий счёт — начислите очки победителю в конце гонки.")}
{local_required_card(
        "14-04",
        "Практика: гонка Turtle с объектами",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/14-04/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "ООП организует код вокруг <strong>объектов</strong> — данных и действий, собранных "
        "вместе.",
        "<code class=\"inline\">class</code> определяет чертёж объекта; "
        "<code class=\"inline\">__init__</code> настраивает его начальное состояние.",
        "<code class=\"inline\">self</code> — ссылка объекта на самого себя, обязательный "
        "первый параметр каждого метода.",
        "Атрибуты хранят данные объекта и независимы у каждого экземпляра класса.",
        "Методы — функции внутри класса, дающие объекту собственные действия — работают "
        "точно так же, как уже знакомые <code class=\"inline\">.forward()</code>, "
        "<code class=\"inline\">.upper()</code>, <code class=\"inline\">.append()</code>.",
    ])}
    """
    out = render_page(
        page_title="Гонка Turtle с объектами",
        description="Итоговый мини-проект главы 14: гонка черепашек через собственный класс — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 14", "index.html"), ("Гонка с объектами", "")],
        kicker="Глава 14 · Создаём объекты реального мира",
        h1="Гонка Turtle с объектами",
        lede="Переписываем гонку из главы 12 с собственным классом — и подводим итоги главы.",
        body_html=body,
        sidebar_groups=sidebar("14-04-gonka-turtle-obekty-itogi.html"),
        nav=PageNav(prev_href="14-03-upravlyaem-obektami.html", prev_label="Управляем объектами", next_href="../glava-15/index.html", next_label="Глава 15: Python и файлы"),
    )
    write("14-04-gonka-turtle-obekty-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
