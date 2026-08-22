#!/usr/bin/env python3
"""Строит Главу 14: «Создаём объекты реального мира» (site/chapters/glava-14/).

Curriculum v2: критически важная глава — первое системное знакомство с ООП.
Путь: ОБЪЕКТ → ТИП → КЛАСС → ЭКЗЕМПЛЯР → СОСТОЯНИЕ → АТРИБУТЫ → ПОВЕДЕНИЕ →
МЕТОДЫ → self → СОЗДАНИЕ ОБЪЕКТА → __init__ → атрибуты экземпляра vs класса →
связывание методов → инкапсуляция/property → композиция → наследование →
super() → полиморфизм → duck typing → специальные методы → dataclasses →
проектирование объектных моделей. Отправная точка всегда — уже знакомый
объект (черепашка, строка, список), а не «класс — это шаблон, просто
запомните» без опоры на то, что уже понятно.

Существующие маршруты и практики (14-01..14-04, включая Turtle-проект)
сохранены на месте и расширены по тому же шаблону, что и в главах 12-13;
новый материал — новые страницы и новые ID практик (14-05..14-26), без
переиспользования занятых ID. Композиция (Uchastnik HAS-A turtle.Turtle) уже
была в исходном 14-04 — формализуем её в 14-13, не переделываем с нуля.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_14_examples import EXAMPLES
from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    branch_diagram,
    callout,
    capability_map,
    class_diagram,
    classic_vs_modern,
    code_block,
    comparison_table,
    converge_diagram,
    decision_map,
    exercise,
    flow_diagram,
    local_required_card,
    object_diagram,
    practice_card,
    relationship_diagram,
    render_chapter_opener,
    render_page,
    summary_box,
    tree_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-14"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Обзор главы"),
    ("14-01-chto-takoe-oop.html", "Что такое ООП?"),
    ("14-02-klassy.html", "Классы и объекты со своими значениями"),
    ("14-03-upravlyaem-obektami.html", "Управляем объектами. Действия объектов"),
    ("14-04-gonka-turtle-obekty-itogi.html", "Гонка Turtle с объектами"),
    ("14-05-self-i-svyazyvanie-metodov.html", "self и связывание методов"),
    ("14-06-init-i-sozdanie-obekta.html", "__init__ и создание объекта"),
    ("14-07-atributy-ekzemplyara-i-klassa.html", "Атрибуты экземпляра и класса"),
    ("14-08-lovushka-obshchego-atributa.html", "Ловушка общего изменяемого атрибута"),
    ("14-09-mini-proekt-player.html", "Мини-проект: Player"),
    ("14-10-inkapsulyatsiya.html", "Инкапсуляция"),
    ("14-11-property.html", "property: вычисляемые атрибуты"),
    ("14-12-mini-proekt-rectangle.html", "Мини-проект: Rectangle"),
    ("14-13-kompozitsiya.html", "Композиция: объекты внутри объектов"),
    ("14-14-mini-proekt-korzina-v2.html", "Мини-проект: Корзина покупок v2"),
    ("14-15-nasledovanie.html", "Наследование"),
    ("14-16-super.html", "super() и порядок разрешения методов"),
    ("14-17-pereopredelenie-metodov.html", "Переопределение методов"),
    ("14-18-polimorfizm.html", "Полиморфизм"),
    ("14-19-duck-typing.html", "Duck typing"),
    ("14-20-mini-proekt-figury.html", "Мини-проект: полиморфные фигуры"),
    ("14-21-spetsialnye-metody.html", "Специальные методы"),
    ("14-22-primenyaem-dunder-metody.html", "Практика: применяем __str__ и __eq__"),
    ("14-23-dataclasses.html", "dataclasses"),
    ("14-24-praktika-dataclass.html", "Практика: dataclass"),
    ("14-25-proektiruem-modeli.html", "Класс или не класс? Проектируем модели"),
    ("14-26-mini-proekt-gonka-v2.html", "Мини-проект: гонка Turtle v2"),
    ("14-27-itogi-glavy.html", "Итоги главы"),
]

PRACTICE_IDS = [
    "14-01", "14-02", "14-03", "14-04", "14-05", "14-06", "14-07", "14-08",
    "14-09", "14-10", "14-11", "14-12", "14-13", "14-14", "14-15", "14-16",
    "14-17", "14-18", "14-19", "14-20", "14-21", "14-22", "14-23", "14-24",
    "14-25", "14-26",
]

LOCAL_REQUIRED_IDS = {"14-04", "14-26"}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 14 · Объекты", items),
        SidebarGroup("Практика", [
            NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def two_up(left_html: str, right_html: str) -> str:
    return f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin:20px 0;align-items:flex-start">
      <div style="flex:1 1 260px;min-width:220px">{left_html}</div>
      <div style="flex:1 1 260px;min-width:220px">{right_html}</div>
    </div>"""


def requirements_card(uses: list[str], level: str, result: str) -> str:
    uses_html = "".join(f'<code class="inline">{u}</code>' for u in uses)
    return f"""
    <div style="display:flex;gap:24px;flex-wrap:wrap;margin:20px 0;padding:18px 22px;
      background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      <div style="flex:2 1 260px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Используем</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">{uses_html}</div>
      </div>
      <div style="flex:1 1 140px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Уровень</div>
        <div style="font-size:16px">{level}</div>
      </div>
      <div style="flex:1 1 200px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Результат</div>
        <div style="font-size:16px">{result}</div>
      </div>
    </div>"""


def terminal_transcript(lines: list[str], *, caption: str = "") -> str:
    body = "\n".join(lines)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>' if caption else ""
    return f"""
    <figure style="margin:24px 0">
      <pre style="background:#0D0230;color:#E7DEFF;border-radius:var(--radius-lg,20px);
        padding:18px 22px;overflow-x:auto;font-family:'JetBrains Mono',monospace;font-size:14px;
        line-height:1.7"><code>{body}</code></pre>
      {cap}
    </figure>"""


def debug_lab(n: int, title: str, broken_code_filename: str, broken_code: str, symptom_lines: list[str], explanation_html: str, fixed_code_filename: str, fixed_code: str) -> str:
    """Единый компонент Debug Lab: сломанный код → что происходит на экране →
    объяснение → исправленный код. Используется во всех 14 обязательных
    debug-лабораториях главы, чтобы у них была одна узнаваемая форма."""
    return f"""
    <div style="margin:28px 0;padding:4px 4px 20px;border:2px dashed #DB2777;border-radius:var(--radius-lg,20px)">
      <div style="padding:14px 20px 4px;font-family:Sora,sans-serif;font-weight:700;font-size:13px;
        letter-spacing:.05em;text-transform:uppercase;color:#DB2777">[[icon:debug]] Debug Lab {n}: {title}</div>
      <div style="padding:0 20px">
{code_block(broken_code_filename, broken_code)}
{terminal_transcript(symptom_lines, caption="Что видно на экране")}
        <p>{explanation_html}</p>
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#059669;margin:16px 0 8px">Исправленный код</div>
{code_block(fixed_code_filename, fixed_code)}
      </div>
    </div>"""


def turtle_output(name: str, filename: str, *, caption: str, alt: str) -> str:
    code = EXAMPLES[name] + "\nscreen.exitonclick()\n"
    return f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin:24px 0;align-items:flex-start">
      <div style="flex:1 1 340px;min-width:280px">
{code_block(filename, code)}
      </div>
      <div style="flex:1 1 300px;min-width:260px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Результат выполнения</div>
        <figure style="margin:0;padding:14px;background:var(--color-bg-surface,#FAFAFC);
          border-radius:var(--radius-lg,20px)">
          <img src="{IMG}/chapter-14/output/{name}.png" alt="{alt}"
            style="width:100%;height:auto;border-radius:12px;display:block;background:#fff" />
          <figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>
        </figure>
      </div>
    </div>"""


_HREFS = [h for h, _ in PAGES]
_TITLES = dict(PAGES)


def nav_for(current_href: str) -> PageNav:
    i = _HREFS.index(current_href)
    prev_href, prev_label = (_HREFS[i - 1], _TITLES[_HREFS[i - 1]]) if i > 0 else (None, None)
    if i < len(_HREFS) - 1:
        next_href, next_label = _HREFS[i + 1], _TITLES[_HREFS[i + 1]]
    else:
        next_href, next_label = "../glava-15/index.html", "Глава 15: Python и файлы"
    return PageNav(prev_href=prev_href, prev_label=prev_label, next_href=next_href, next_label=next_label)


def page(href: str, *, page_title: str, description: str, kicker_suffix: str, h1: str, lede: str, body_html: str) -> None:
    out = render_page(
        page_title=page_title,
        description=description,
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 14", "index.html"), (kicker_suffix, "")],
        kicker="Глава 14 · Создаём объекты реального мира",
        h1=h1,
        lede=lede,
        body_html=body_html,
        sidebar_groups=sidebar(href),
        nav=nav_for(href),
    )
    write(href, out)


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=14,
        baseline_page=311,
        title="Создаём объекты реального мира",
        description="Классы, объекты, атрибуты и методы — основы объектно-ориентированного "
        "программирования. От уже знакомых объектов (черепашка, строка, список) — к собственным "
        "классам: состояние и поведение, self и __init__, инкапсуляция и property, композиция и "
        "наследование, super(), полиморфизм и duck typing, специальные методы, dataclasses — и "
        "к вопросу, который важнее любого синтаксиса: когда классу вообще стоит появляться в "
        "программе.",
        meta_items=["[[icon:timer]] ~11 часов", "[[icon:architecture]] class, self, super()", "[[icon:practice]] 26 практик"],
        sections=[
            ChapterSectionLink("14.1", "Что такое ООП?", "14-01-chto-takoe-oop.html", "312"),
            ChapterSectionLink("", "Давайте это докажем!", "14-01-chto-takoe-oop.html#dokazhem", "313"),
            ChapterSectionLink("14.2", "Классы и объекты со своими значениями", "14-02-klassy.html", "314"),
            ChapterSectionLink("", "Объекты со своими значениями", "14-02-klassy.html#znacheniya", "315"),
            ChapterSectionLink("14.3", "Управляем объектами. Действия объектов", "14-03-upravlyaem-obektami.html", "317"),
            ChapterSectionLink("14.4", "Гонка Turtle с объектами", "14-04-gonka-turtle-obekty-itogi.html", "319"),
            ChapterSectionLink("14.5", "self и связывание методов", "14-05-self-i-svyazyvanie-metodov.html", "322"),
            ChapterSectionLink("14.6", "__init__ и создание объекта", "14-06-init-i-sozdanie-obekta.html", "325"),
            ChapterSectionLink("14.7", "Атрибуты экземпляра и класса", "14-07-atributy-ekzemplyara-i-klassa.html", "328"),
            ChapterSectionLink("14.8", "Ловушка общего изменяемого атрибута", "14-08-lovushka-obshchego-atributa.html", "331"),
            ChapterSectionLink("14.9", "Мини-проект: Player", "14-09-mini-proekt-player.html", "334"),
            ChapterSectionLink("14.10", "Инкапсуляция", "14-10-inkapsulyatsiya.html", "337"),
            ChapterSectionLink("14.11", "property: вычисляемые атрибуты", "14-11-property.html", "340"),
            ChapterSectionLink("14.12", "Мини-проект: Rectangle", "14-12-mini-proekt-rectangle.html", "343"),
            ChapterSectionLink("14.13", "Композиция: объекты внутри объектов", "14-13-kompozitsiya.html", "346"),
            ChapterSectionLink("14.14", "Мини-проект: Корзина покупок v2", "14-14-mini-proekt-korzina-v2.html", "349"),
            ChapterSectionLink("14.15", "Наследование", "14-15-nasledovanie.html", "352"),
            ChapterSectionLink("14.16", "super() и порядок разрешения методов", "14-16-super.html", "355"),
            ChapterSectionLink("14.17", "Переопределение методов", "14-17-pereopredelenie-metodov.html", "358"),
            ChapterSectionLink("14.18", "Полиморфизм", "14-18-polimorfizm.html", "361"),
            ChapterSectionLink("14.19", "Duck typing", "14-19-duck-typing.html", "364"),
            ChapterSectionLink("14.20", "Мини-проект: полиморфные фигуры", "14-20-mini-proekt-figury.html", "367"),
            ChapterSectionLink("14.21", "Специальные методы", "14-21-spetsialnye-metody.html", "370"),
            ChapterSectionLink("14.22", "Практика: применяем __str__ и __eq__", "14-22-primenyaem-dunder-metody.html", "373"),
            ChapterSectionLink("14.23", "dataclasses", "14-23-dataclasses.html", "376"),
            ChapterSectionLink("14.24", "Практика: dataclass", "14-24-praktika-dataclass.html", "379"),
            ChapterSectionLink("14.25", "Класс или не класс? Проектируем модели", "14-25-proektiruem-modeli.html", "382"),
            ChapterSectionLink("14.26", "Мини-проект: гонка Turtle v2", "14-26-mini-proekt-gonka-v2.html", "385"),
            ChapterSectionLink("", "Итоги главы", "14-27-itogi-glavy.html", "388"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 14-01 · Что такое ООП? (расширено)
# ---------------------------------------------------------------------------

def build_01() -> None:
    body = f"""
    <h2>Объект — то, что уже знакомо, но с новым именем</h2>
    <p>Присмотритесь к коду из предыдущих глав: <code class="inline">artist.forward(100)</code>,
    <code class="inline">"Python".upper()</code>, <code class="inline">[1,2,3].append(4)</code>
    — во всех трёх у нас есть какой-то <strong>объект</strong> (черепашка, строка, список) и
    команда, которую мы у него вызываем через точку. Всё это время вы уже работали с объектами
    — этот раздел просто даёт знакомой идее точное имя.</p>
    <p>У любого объекта в Python есть две стороны:</p>
    {comparison_table(
        ["Сторона объекта", "Пример у artist (черепашки)"],
        [
            ["<strong>Состояние</strong> — данные, которые объект хранит прямо сейчас", "текущие координаты, цвет, направление"],
            ["<strong>Поведение</strong> — действия, которые объект умеет выполнять", "<code class=\"inline\">forward()</code>, <code class=\"inline\">right()</code>, <code class=\"inline\">color()</code>"],
        ],
    )}
    <p>Объектно-ориентированное программирование (ООП) — это способ организовать код вокруг
    таких объектов: данные и действия, которые к ним относятся, живут <strong>вместе</strong>, а
    не разбросаны по отдельным переменным и функциям.</p>

    <h2>Тип объекта: <code class="inline">type()</code></h2>
    <p>У каждого объекта в Python есть тип — узнать его можно встроенной функцией
    <code class="inline">type()</code>, с которой вы уже знакомы:</p>
    {code_block(
        "tip_obekta.py",
        'artist = __import__("turtle").Turtle()\n'
        'print(type(artist))     # <class \'turtle.Turtle\'>\n'
        'print(type("Python"))   # <class \'str\'>\n'
        'print(type([1, 2, 3]))  # <class \'list\'>\n',
    )}
    <p>Слово <code class="inline">class</code> в каждом ответе — не случайность. Тип объекта
    — это и есть его <strong>класс</strong>.</p>

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
    главу 12, где несколько независимых черепашек участвовали в гонке одновременно: у каждой
    было своё состояние (позиция, цвет), хотя все они были черепашками одного и того же класса.</p>
    {callout(
        "info",
        "Класс описывает БУДУЩИЕ объекты, а не один конкретный",
        "<code class=\"inline\">turtle.Turtle</code> сам по себе не имеет позиции на экране — "
        "позиция появляется только у КАЖДОГО созданного объекта <code class=\"inline\">turtle."
        "Turtle()</code> отдельно. Класс — это описание того, какими будут объекты, а не сам "
        "объект.",
    )}

    {practice_card(
        "14-01",
        "Практика: находим объекты в уже знакомом коде",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-01/index.html",
    )}
    """
    page(
        "14-01-chto-takoe-oop.html",
        page_title="Что такое объектно-ориентированное программирование?",
        description="Введение в ООП: состояние и поведение, type(), классы и объекты на примере уже знакомого кода.",
        kicker_suffix="Что такое ООП?",
        h1="Что такое объектно-ориентированное программирование?",
        lede="Вы уже пользовались объектами много глав подряд — просто ещё не называли их так.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-02 · Классы и объекты со своими значениями (расширено)
# ---------------------------------------------------------------------------

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
    (и любого другого метода) она должна быть всегда. Подробно, что здесь происходит «под
    капотом», разберём в разделах 14.5-14.6 — сейчас достаточно рабочей модели.</p>

    {callout(
        "info",
        "Класс vs объект — аналогия с формой для печенья",
        "Класс — как форма для печенья: одна и та же форма может «вырезать» сколько угодно "
        "печений (объектов) — каждое своё, но по одному и тому же шаблону.",
    )}
    {callout(
        "warning",
        "Где аналогия ломается",
        "Форма для печенья — пассивный инструмент: она сама ничего не делает и не хранит "
        "состояния. Класс в Python — не пассивный шаблон, а самостоятельный объект: у него "
        "можно спросить <code class=\"inline\">type(rex)</code>, ему самому можно назначать "
        "атрибуты, его можно передать в переменную. Пользуйтесь аналогией, чтобы запомнить "
        "«один чертёж → много экземпляров», но не воспринимайте её буквально дальше этого.",
    )}

    <div style="margin:24px 0">
{class_diagram("Sobaka", ["klichka", "vozrast"], [], caption="Класс Sobaka — описывает БУДУЩИЕ атрибуты, но ещё не содержит ни одного значения")}
    </div>

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
    {two_up(
        object_diagram("rex", "Sobaka", [("klichka", "'Рекс'"), ("vozrast", "3")], caption="Объект rex — конкретные значения"),
        object_diagram("sharik", "Sobaka", [("klichka", "'Шарик'"), ("vozrast", "5")], caption="Объект sharik — свои значения, тот же класс"),
    )}
    <p>Один класс — сколько угодно объектов, и у каждого своё, независимое состояние. Именно
    это отличает объект от простого словаря с похожими ключами: объект <em>принадлежит</em>
    своему классу и получает через него доступ к общим методам (раздел 14.3).</p>

    {practice_card(
        "14-02",
        "Практика: создаём собственные классы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-02/index.html",
    )}
    """
    page(
        "14-02-klassy.html",
        page_title="Классы",
        description="Определение классов через class и __init__, class_diagram, объекты со своими значениями.",
        kicker_suffix="Классы",
        h1="Классы",
        lede="Пишем свой первый класс — чертёж, по которому Python будет создавать объекты.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-03 · Управляем объектами. Действия объектов (расширено)
# ---------------------------------------------------------------------------

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
    <div style="margin:24px 0">
{class_diagram("Sobaka", ["klichka", "vozrast"], ["layat()", "prazdnovat_den_rozhdeniya()"], caption="Класс Sobaka — теперь с методами")}
    </div>
    {callout(
        "warning",
        "self — это не ключевое слово",
        "<code class=\"inline\">self</code> — обычное имя параметра, выбранное по соглашению, "
        "а не зарезервированное слово Python (в отличие от <code class=\"inline\">if</code> или "
        "<code class=\"inline\">class</code>). Технически метод заработает и с именем "
        "<code class=\"inline\">this</code> или <code class=\"inline\">obj</code> — но "
        "используйте <code class=\"inline\">self</code> всегда: так его называет весь код на "
        "Python, и любое другое имя будет путать других читающих ваш код. Подробно, откуда "
        "<code class=\"inline\">self</code> берётся при вызове, разберём в разделе 14.5.",
    )}

    {practice_card(
        "14-03",
        "Практика: методы и изменение атрибутов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-03/index.html",
    )}
    """
    page(
        "14-03-upravlyaem-obektami.html",
        page_title="Управляем объектами. Объекты выполняют действия",
        description="Изменение атрибутов объекта и определение собственных методов класса.",
        kicker_suffix="Управляем объектами",
        h1="Управляем объектами",
        lede="Атрибуты можно менять после создания объекта — а методы дают объекту собственные "
        "действия.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-04 · Гонка Turtle с объектами (сфокусировано на проекте — итоги переехали в 14-27)
# ---------------------------------------------------------------------------

def build_04() -> None:
    body = f"""
    <p>Вернёмся к гонке черепашек из главы 12 — на этот раз обернём каждого участника в свой
    собственный класс, а не просто в объект <code class="inline">turtle.Turtle</code> напрямую.</p>
{turtle_output("14-gonka-obektov", "gonka_s_klassom.py", caption="Четыре объекта Uchastnik — независимое состояние, общий класс", alt="Четыре черепашки разных цветов на финише гонки, каждая — отдельный объект класса Uchastnik")}
    {callout(
        "info",
        "Зачем оборачивать Turtle в свой класс?",
        "В главе 12 логика гонки (движение, проверка финиша) была разбросана по основному "
        "коду. Теперь каждый участник — самостоятельный объект <code class=\"inline\">"
        "Uchastnik</code>, который сам знает, как сделать шаг и как проверить, финишировал ли "
        "он. Обратите внимание: <code class=\"inline\">Uchastnik</code> не является черепашкой "
        "— он ХРАНИТ черепашку в атрибуте <code class=\"inline\">self.t</code>. Это называется "
        "<strong>композицией</strong> — формально разберём её в разделе 14.13.",
    )}
{relationship_diagram("Uchastnik", "turtle.Turtle", "has-a", style="has-a", caption="Uchastnik ХРАНИТ объект turtle.Turtle — а не является им")}
    {exercise(3, "Счёт очков", "Добавьте классу Uchastnik атрибут ochki и метод nabrat_ochki(n), увеличивающий счёт — начислите очки победителю в конце гонки.")}
{local_required_card(
        "14-04",
        "Практика: гонка Turtle с объектами",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/14-04/index.html",
    )}
    """
    page(
        "14-04-gonka-turtle-obekty-itogi.html",
        page_title="Гонка Turtle с объектами",
        description="Мини-проект: гонка черепашек через собственный класс Uchastnik — первый пример композиции.",
        kicker_suffix="Гонка с объектами",
        h1="Гонка Turtle с объектами",
        lede="Переписываем гонку из главы 12 с собственным классом — и впервые видим композицию "
        "в деле.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-05 · self и связывание методов
# ---------------------------------------------------------------------------

def build_05() -> None:
    body = f"""
    <h2>Две равносильные записи одного вызова</h2>
    <p><code class="inline">rex.layat()</code> — не единственный способ вызвать этот метод.
    Тот же самый вызов можно записать и через класс, передав объект вручную первым аргументом:</p>
    {classic_vs_modern(
        "Одно и то же действие — два способа записи",
        "Через объект (обычная запись)",
        'rex.layat()\n',
        "Через класс (то, что происходит на самом деле)",
        'Sobaka.layat(rex)\n',
        "На письме всегда используйте запись через объект — <code class=\"inline\">rex.layat()"
        "</code>. Вторая форма показана только для того, чтобы стало видно, откуда берётся "
        "<code class=\"inline\">self</code>: это и есть <code class=\"inline\">rex</code>, "
        "переданный автоматически первым аргументом.",
    )}

    <h2>Что происходит при вызове <code class="inline">rex.layat()</code></h2>
    {flow_diagram(
        [
            ("rex.layat()", "вызов через точку"),
            ("Python ищет layat", "в классе Sobaka"),
            ("находит layat(self)", "метод определён в классе"),
            ("self = rex", "подставляется автоматически"),
            ("тело метода выполняется", "с доступом к self.klichka и т.д."),
        ],
        caption="Связывание метода: объект слева от точки становится self внутри метода",
    )}
    {callout(
        "warning",
        "self — снова не ключевое слово",
        "Как уже говорилось в разделе 14.3: <code class=\"inline\">self</code> — это просто имя "
        "первого параметра метода, выбранное по соглашению. Python подставляет в него объект "
        "слева от точки НЕЗАВИСИМО от того, как вы его назвали — но называйте его "
        "<code class=\"inline\">self</code> всегда, это единственное имя, которое ожидает "
        "увидеть любой человек, читающий код на Python.",
    )}

{debug_lab(
        1,
        "забыли self в определении метода",
        "bez_self.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka):\n"
        "        self.klichka = klichka\n\n"
        "    def layat():          # забыли self первым параметром\n"
        '        print("Гав-гав!")\n\n'
        'rex = Sobaka("Рекс")\n'
        "rex.layat()\n",
        [
            "Traceback (most recent call last):",
            '  File "bez_self.py", line 9, in <module>',
            "    rex.layat()",
            "TypeError: Sobaka.layat() takes 0 positional arguments but 1 was given",
        ],
        "Python всё равно попытался подставить <code class=\"inline\">rex</code> первым "
        "аргументом при вызове <code class=\"inline\">rex.layat()</code> — связывание метода "
        "происходит ВСЕГДА, а не только когда вы этого ожидаете. Раз в определении метода не "
        "было параметра, чтобы его принять, — Python сообщает, что аргументов передано на один "
        "больше, чем метод способен принять.",
        "s_self.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka):\n"
        "        self.klichka = klichka\n\n"
        "    def layat(self):\n"
        '        print(f"{self.klichka}: Гав-гав!")\n\n'
        'rex = Sobaka("Рекс")\n'
        "rex.layat()\n",
    )}

    {practice_card(
        "14-05",
        "Практика: self и связывание методов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-05/index.html",
    )}
    """
    page(
        "14-05-self-i-svyazyvanie-metodov.html",
        page_title="self и связывание методов",
        description="Как obj.method() превращается в Class.method(obj); self — не ключевое слово; Debug Lab: забытый self.",
        kicker_suffix="self и связывание методов",
        h1="self и связывание методов",
        lede="rex.layat() и Sobaka.layat(rex) — один и тот же вызов. Разбираемся, откуда self "
        "берётся на самом деле.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-06 · __init__ и создание объекта
# ---------------------------------------------------------------------------

def build_06() -> None:
    body = f"""
    <h2>Что на самом деле происходит при <code class="inline">Sobaka("Рекс", 3)</code></h2>
    {flow_diagram(
        [
            ("Sobaka(\"Рекс\", 3)", "вызов класса"),
            ("Python создаёт новый пустой объект", "объект уже существует"),
            ("вызывается __init__(self, ...)", "self — это тот самый новый объект"),
            ("__init__ настраивает атрибуты", "self.klichka = ..."),
            ("готовый объект возвращается", "rex = ..."),
        ],
        caption="__init__ НЕ создаёт объект — он настраивает объект, который Python уже создал",
    )}
    {callout(
        "warning",
        "Частое заблуждение: «__init__ создаёт объект»",
        "Это не так. К моменту вызова <code class=\"inline\">__init__</code> объект уже "
        "существует — иначе Python не смог бы передать его первым аргументом "
        "(<code class=\"inline\">self</code>)! Роль <code class=\"inline\">__init__</code> — "
        "не создать объект, а <strong>настроить его начальное состояние</strong>: имя честнее "
        "было бы «инициализатор», а не «конструктор» — так его и называют в документации "
        "Python.",
    )}

    <h2>Значения по умолчанию в __init__</h2>
    <p><code class="inline">__init__</code> — обычная функция (глава 13 применима целиком):
    параметры могут иметь значения по умолчанию:</p>
    {code_block(
        "init_s_umolchaniem.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast=1):\n"
        "        self.klichka = klichka\n"
        "        self.vozrast = vozrast\n\n"
        'shchenok = Sobaka("Бим")             # vozrast = 1 по умолчанию\n'
        'rex = Sobaka("Рекс", vozrast=3)      # явно указан\n',
    )}

    <h2>__init__ может вызывать другие методы</h2>
    {code_block(
        "init_vyzyvaet_metod.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast=1):\n"
        "        self.klichka = klichka\n"
        "        self.vozrast = vozrast\n"
        "        self.privet()          # метод можно вызвать уже внутри __init__\n\n"
        "    def privet(self):\n"
        '        print(f"Новый пёс на сцене: {self.klichka}!")\n\n'
        'rex = Sobaka("Рекс")   # печатает приветствие сразу при создании\n',
    )}

{debug_lab(
        2,
        "self.x = x записали просто как x = x",
        "poteryannyj_atribut.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast):\n"
        "        klichka = klichka      # это просто локальная переменная!\n"
        "        self.vozrast = vozrast\n\n"
        'rex = Sobaka("Рекс", 3)\n'
        "print(rex.klichka)\n",
        [
            "Traceback (most recent call last):",
            '  File "poteryannyj_atribut.py", line 7, in <module>',
            "    print(rex.klichka)",
            "AttributeError: 'Sobaka' object has no attribute 'klichka'",
        ],
        "Строка <code class=\"inline\">klichka = klichka</code> без <code class=\"inline\">"
        "self.</code> слева создаёт обычную ЛОКАЛЬНУЮ переменную внутри "
        "<code class=\"inline\">__init__</code>, которая исчезает, как только "
        "<code class=\"inline\">__init__</code> заканчивается — на объекте она никогда не "
        "сохранялась. Чтобы значение осталось частью объекта НАВСЕГДА, слева от <code "
        "class=\"inline\">=</code> обязательно должно стоять <code class=\"inline\">self."
        "имя_атрибута</code>.",
        "atribut_ispravlen.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast):\n"
        "        self.klichka = klichka\n"
        "        self.vozrast = vozrast\n\n"
        'rex = Sobaka("Рекс", 3)\n'
        "print(rex.klichka)\n",
    )}

    {practice_card(
        "14-06",
        "Практика: __init__ и создание объекта",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-06/index.html",
    )}
    """
    page(
        "14-06-init-i-sozdanie-obekta.html",
        page_title="__init__ и создание объекта",
        description="Порядок создания объекта, значения по умолчанию в __init__, вызов методов изнутри __init__; Debug Lab: потерянный атрибут.",
        kicker_suffix="__init__ и создание объекта",
        h1="__init__ и создание объекта",
        lede="__init__ не создаёт объект — он настраивает объект, который уже существует.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-07 · Атрибуты экземпляра и класса
# ---------------------------------------------------------------------------

def build_07() -> None:
    body = f"""
    <h2>Два места, где может жить атрибут</h2>
    <p>До сих пор все атрибуты создавались внутри <code class="inline">__init__</code> через
    <code class="inline">self.имя = ...</code> — это <strong>атрибуты экземпляра</strong>, у
    каждого объекта свои. Но атрибут можно объявить и прямо в теле класса, без
    <code class="inline">self</code> — тогда это <strong>атрибут класса</strong>, один на все
    объекты сразу:</p>
    {code_block(
        "atribut_klassa.py",
        "class Sobaka:\n"
        '    vid = "Собака"          # атрибут КЛАССА — один на всех\n\n'
        "    def __init__(self, klichka, vozrast):\n"
        "        self.klichka = klichka    # атрибут ЭКЗЕМПЛЯРА — свой у каждого\n"
        "        self.vozrast = vozrast\n\n"
        'rex = Sobaka("Рекс", 3)\n'
        'sharik = Sobaka("Шарик", 5)\n'
        "print(rex.vid, sharik.vid)   # Собака Собака — общий атрибут\n",
    )}
    <div style="margin:24px 0">
{class_diagram("Sobaka", ["vid  (атрибут класса)", "klichka", "vozrast"], [], caption="Атрибут класса объявлен в теле класса; атрибуты экземпляра — внутри __init__")}
    </div>

    {two_up(
        object_diagram("rex", "Sobaka", [("vid", "'Собака'"), ("klichka", "'Рекс'"), ("vozrast", "3")], caption="rex — vid читается с класса"),
        object_diagram("sharik", "Sobaka", [("vid", "'Собака'"), ("klichka", "'Шарик'"), ("vozrast", "5")], caption="sharik — тот же vid, но не своя копия"),
    )}
    {callout(
        "warning",
        "Частое заблуждение: «атрибуты класса копируются в каждый объект»",
        "Это не так. <code class=\"inline\">vid</code> хранится ОДИН раз — в самом классе "
        "<code class=\"inline\">Sobaka</code>. Когда вы пишете <code class=\"inline\">rex.vid"
        "</code>, Python сначала ищет <code class=\"inline\">vid</code> среди атрибутов ЭКЗЕМПЛЯРА "
        "<code class=\"inline\">rex</code> — не находит — и только затем смотрит на класс "
        "<code class=\"inline\">Sobaka</code>, где и находит общее значение. Ни один байт "
        "<code class=\"inline\">vid</code> не копируется в <code class=\"inline\">rex</code>.",
    )}
    <p>Если присвоить атрибуту с тем же именем значение ЧЕРЕЗ ОБЪЕКТ — Python создаст новый
    атрибут ЭКЗЕМПЛЯРА, который отныне «затеняет» атрибут класса именно для этого объекта, не
    трогая остальные:</p>
    {code_block(
        "zatenenie.py",
        'rex.vid = "Дворняга"    # создаёт vid у САМОГО rex, не трогая класс\n'
        "print(rex.vid, sharik.vid)   # Дворняга Собака — sharik не изменился\n",
    )}

    {practice_card(
        "14-07",
        "Практика: атрибуты экземпляра и класса",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-07/index.html",
    )}
    """
    page(
        "14-07-atributy-ekzemplyara-i-klassa.html",
        page_title="Атрибуты экземпляра и класса",
        description="Атрибут экземпляра vs атрибут класса, поиск через объект, затенение при присваивании через объект.",
        kicker_suffix="Атрибуты экземпляра и класса",
        h1="Атрибуты экземпляра и класса",
        lede="Один атрибут может жить в объекте, а другой — в самом классе, общим на всех. Это "
        "не одно и то же.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-08 · Ловушка общего изменяемого атрибута класса (Debug Lab)
# ---------------------------------------------------------------------------

def build_08() -> None:
    body = f"""
    <h2>Когда «общий атрибут» превращается в баг</h2>
    <p>Атрибут класса с НЕИЗМЕНЯЕМЫМ значением (число, строка) безопасен — присваивание через
    объект просто создаёт новый атрибут экземпляра (раздел 14.7). Но атрибут класса со
    <strong>ИЗМЕНЯЕМЫМ</strong> значением — список или словарь — устроен иначе: если его не
    ПЕРЕПРИСВОИТЬ, а ИЗМЕНИТЬ на месте (<code class="inline">.append()</code>, <code
    class="inline">[key] = ...</code>), это затронет объект класса, который используют ВСЕ
    экземпляры сразу.</p>

{debug_lab(
        3,
        "общий изменяемый список как атрибут класса",
        "obshchaya_korzina.py",
        "class Korzina:\n"
        "    tovary = []          # атрибут КЛАССА — один список на все корзины!\n\n"
        "    def dobavit(self, tovar):\n"
        "        self.tovary.append(tovar)   # .append() меняет список НА МЕСТЕ\n\n"
        'k1 = Korzina()\n'
        'k2 = Korzina()\n'
        'k1.dobavit("Хлеб")\n'
        "print(k2.tovary)\n",
        [
            ">>> print(k2.tovary)",
            "['Хлеб']",
        ],
        "<code class=\"inline\">k2</code> ни разу не вызывал <code class=\"inline\">dobavit()"
        "</code>, но «Хлеб» уже в его корзине! Причина: <code class=\"inline\">self.tovary."
        "append(...)</code> не создаёт новый список — он ИЗМЕНЯЕТ существующий, а этот список "
        "один-единственный, унаследован обоими объектами от класса <code class=\"inline\">"
        "Korzina</code>.",
        "svoya_korzina.py",
        "class Korzina:\n"
        "    def __init__(self):\n"
        "        self.tovary = []    # атрибут ЭКЗЕМПЛЯРА — свой список у каждой корзины\n\n"
        "    def dobavit(self, tovar):\n"
        "        self.tovary.append(tovar)\n\n"
        'k1 = Korzina()\n'
        'k2 = Korzina()\n'
        'k1.dobavit("Хлеб")\n'
        "print(k2.tovary)   # [] — пусто, как и должно быть\n",
    )}
{converge_diagram(["k1.tovary", "k2.tovary"], "[] — общий список класса Korzina", caption="Без self.tovary = [] в __init__ оба обращения ведут к ОДНОМУ И ТОМУ ЖЕ списку")}
    {callout(
        "tip",
        "Правило: изменяемые значения — только в __init__",
        "Если атрибуту нужно значение <code class=\"inline\">list</code>, <code class=\"inline\">"
        "dict</code> или <code class=\"inline\">set</code> — создавайте его внутри "
        "<code class=\"inline\">__init__</code> через <code class=\"inline\">self.имя = []</code>, "
        "а не в теле класса. Это тот же самый принцип, что и «ловушка изменяемого значения по "
        "умолчанию» у параметров функций (глава 13) — и грабли те же самые.",
    )}

    {practice_card(
        "14-08",
        "Практика: находим общий изменяемый атрибут",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-08/index.html",
    )}
    """
    page(
        "14-08-lovushka-obshchego-atributa.html",
        page_title="Ловушка общего изменяемого атрибута",
        description="Debug Lab: почему изменяемый атрибут класса (список, словарь) оказывается общим на все объекты — и как это исправить.",
        kicker_suffix="Ловушка общего атрибута",
        h1="Ловушка общего изменяемого атрибута",
        lede="Один список «на двоих» — классический баг ООП-новичка. Разбираем, откуда он "
        "берётся и как его избежать.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-09 · Мини-проект: Player
# ---------------------------------------------------------------------------

def build_09() -> None:
    body = f"""
    <h2>Мини-проект: Player</h2>
    <p>Соберём всё из разделов 14.1-14.8 в один настоящий класс — модель игрока с очками
    здоровья и счётом:</p>
    {code_block(
        "player.py",
        "class Player:\n"
        '    def __init__(self, name, health=100):\n'
        "        self.name = name\n"
        "        self.health = health\n"
        "        self.score = 0\n\n"
        "    def take_damage(self, amount):\n"
        "        self.health -= amount\n"
        "        if self.health < 0:\n"
        "            self.health = 0\n\n"
        "    def heal(self, amount):\n"
        "        self.health += amount\n"
        "        if self.health > 100:\n"
        "            self.health = 100\n\n"
        "    def add_score(self, points):\n"
        "        self.score += points\n",
    )}
    <div style="margin:24px 0">
{class_diagram("Player", ["name", "health", "score"], ["take_damage(amount)", "heal(amount)", "add_score(points)"], caption="Класс Player")}
    </div>
    {code_block(
        "dva_igroka.py",
        'anna = Player("Anna")\n'
        'bob = Player("Bob")\n'
        "anna.take_damage(30)\n"
        "anna.add_score(10)\n\n"
        "print(anna.health, anna.score)   # 70 10\n"
        "print(bob.health, bob.score)     # 100 0 — bob не пострадал\n",
    )}
    {two_up(
        object_diagram("anna", "Player", [("name", "'Anna'"), ("health", "70"), ("score", "10")], caption="anna — своё состояние"),
        object_diagram("bob", "Player", [("name", "'Bob'"), ("health", "100"), ("score", "0")], caption="bob — не затронут действиями anna"),
    )}

{debug_lab(
        4,
        "== сравнивает не значения, а сами объекты",
        "sravnenie_igrokov.py",
        'a1 = Player("Anna")\n'
        'a2 = Player("Anna")   # те же имя, здоровье и счёт, что у a1\n\n'
        "print(a1 == a2)\n",
        [
            ">>> print(a1 == a2)",
            "False",
        ],
        "Хотя у <code class=\"inline\">a1</code> и <code class=\"inline\">a2</code> одинаковые "
        "значения ВСЕХ атрибутов, <code class=\"inline\">==</code> по умолчанию сравнивает "
        "объекты по <strong>идентичности</strong> — это два РАЗНЫХ объекта в памяти, поэтому "
        "результат <code class=\"inline\">False</code>, даже если содержимое совпадает "
        "полностью. Чтобы <code class=\"inline\">==</code> сравнивал значения, классу нужен "
        "специальный метод <code class=\"inline\">__eq__</code> — дойдём до него в разделе "
        "14.21.",
        "sravnenie_cherez_pole.py",
        "# Пока сравниваем нужные поля вручную:\n"
        "print(a1.name == a2.name and a1.health == a2.health)\n",
    )}

    {exercise(2, "is_alive", "Добавьте классу Player метод is_alive(self), возвращающий True, если health больше 0, и False иначе.")}

    {practice_card(
        "14-09",
        "Практика: класс Player",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-09/index.html",
    )}
    """
    page(
        "14-09-mini-proekt-player.html",
        page_title="Мини-проект: Player",
        description="Собираем класс Player: __init__, методы take_damage/heal/add_score, независимость состояния; Debug Lab: сравнение объектов через ==.",
        kicker_suffix="Мини-проект: Player",
        h1="Мини-проект: Player",
        lede="Модель игрока с очками здоровья и счётом — первый самостоятельный класс главы.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-10 · Инкапсуляция
# ---------------------------------------------------------------------------

def build_10() -> None:
    body = f"""
    <h2>Проблема: атрибуты доступны напрямую</h2>
    <p>Ничто не мешает изменить атрибут объекта в обход всех методов — напрямую, снаружи
    класса:</p>
{debug_lab(
        5,
        "прямое присваивание ломает состояние объекта",
        "slomannoe_zdorove.py",
        'anna = Player("Anna")\n'
        "anna.health = -50    # напрямую, в обход take_damage()\n"
        "print(anna.health)\n",
        [
            ">>> print(anna.health)",
            "-50",
        ],
        "Метод <code class=\"inline\">take_damage()</code> аккуратно не даёт "
        "<code class=\"inline\">health</code> уйти ниже нуля — но НИЧТО не заставляет "
        "пользоваться именно этим методом. Присваивание <code class=\"inline\">anna.health = "
        "-50</code> обходит всю защитную логику напрямую, и объект оказывается в состоянии, "
        "которое сам класс считал невозможным.",
        "cherez_metod.py",
        "anna.take_damage(150)   # health корректно останавливается на 0\n"
        "print(anna.health)\n",
    )}
    <p><strong>Инкапсуляция</strong> — идея хранить состояние объекта «внутри» и разрешать
    менять его только через методы, которые могут проверить, что новое значение осмысленно.</p>

    <h2>Соглашение об именах: _internal и __name</h2>
    {comparison_table(
        ["Запись", "Что означает по соглашению"],
        [
            ["<code class=\"inline\">name</code>", "публичный атрибут — пользуйтесь снаружи свободно"],
            ["<code class=\"inline\">_name</code>", "«внутреннее» — не трогайте снаружи, хотя технически доступ есть"],
            ["<code class=\"inline\">__name</code>", "включает подмену имени (name mangling) — доступ снаружи усложнён, но не исчезает"],
        ],
    )}
    {code_block(
        "dvojnoe_podcherkivanie.py",
        "class Konto:\n"
        "    def __init__(self, balans):\n"
        "        self.__balans = balans\n\n"
        "schet = Konto(100)\n"
        "print(schet._Konto__balans)   # 100 — доступ ЕСТЬ, просто имя изменено\n",
    )}
    {callout(
        "warning",
        "Частое заблуждение: «__private по-настоящему приватно»",
        "Это не так — в Python нет настоящей приватности на уровне языка. "
        "<code class=\"inline\">__balans</code> автоматически переименовывается в "
        "<code class=\"inline\">_Konto__balans</code> (name mangling) — это защищает в основном "
        "от СЛУЧАЙНОГО совпадения имён при наследовании, а не от намеренного доступа снаружи. "
        "Инкапсуляция в Python — это соглашение и дисциплина команды, а не запрет со стороны "
        "интерпретатора.",
    )}

    {practice_card(
        "14-10",
        "Практика: инкапсуляция",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-10/index.html",
    )}
    """
    page(
        "14-10-inkapsulyatsiya.html",
        page_title="Инкапсуляция",
        description="Зачем прятать состояние объекта, соглашения _internal и __name, name mangling; Debug Lab: сломанный health.",
        kicker_suffix="Инкапсуляция",
        h1="Инкапсуляция",
        lede="Атрибуты доступны напрямую — и это может сломать состояние объекта. Разбираемся, "
        "как этого избежать.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-11 · property: вычисляемые атрибуты
# ---------------------------------------------------------------------------

def build_11() -> None:
    body = f"""
    <h2>property: проверка при записи, без изменения синтаксиса чтения</h2>
    <p>Декоратор <code class="inline">@property</code> позволяет обращаться к методу ТАК ЖЕ,
    как к обычному атрибуту — без круглых скобок:</p>
    {code_block(
        "property_getter.py",
        "class Krug:\n"
        "    def __init__(self, radius):\n"
        "        self._radius = radius\n\n"
        "    @property\n"
        "    def ploshchad(self):\n"
        "        return 3.14159 * self._radius ** 2\n\n"
        'krug = Krug(10)\n'
        "print(krug.ploshchad)   # 314.159 — без скобок, хотя это метод!\n",
    )}
    <p><code class="inline">ploshchad</code> нигде не хранится — она вычисляется заново при
    каждом обращении. Снаружи это неотличимо от обычного атрибута.</p>

    <h2>@x.setter: проверка при присваивании</h2>
    {code_block(
        "property_setter.py",
        "class Krug:\n"
        "    def __init__(self, radius):\n"
        "        self.radius = radius     # проходит через setter ниже\n\n"
        "    @property\n"
        "    def radius(self):\n"
        "        return self._radius\n\n"
        "    @radius.setter\n"
        "    def radius(self, value):\n"
        "        if value <= 0:\n"
        '            raise ValueError("радиус должен быть положительным")\n'
        "        self._radius = value\n\n"
        'krug = Krug(10)\n'
        "krug.radius = 5     # проходит проверку\n"
        "krug.radius = -1    # ValueError — присваивание отклонено\n",
    )}
    {callout(
        "tip",
        "Главная польза property: код снаружи не меняется",
        "Если сегодня <code class=\"inline\">radius</code> — обычный атрибут, а завтра "
        "понадобилась проверка — можно превратить его в property, и весь код, который писал "
        "<code class=\"inline\">krug.radius = 5</code>, продолжит работать без единой правки. "
        "Именно поэтому в Python принято начинать с обычных атрибутов и добавлять property "
        "только когда проверка действительно понадобилась — а не оборачивать в property "
        "вообще всё с самого начала.",
    )}

{debug_lab(
        6,
        "забыли декоратор @radius.setter",
        "bez_setter.py",
        "class Krug:\n"
        "    def __init__(self, radius):\n"
        "        self._radius = radius\n\n"
        "    @property\n"
        "    def radius(self):\n"
        "        return self._radius\n\n"
        "    def radius(self, value):    # забыли @radius.setter сверху!\n"
        "        self._radius = value\n\n"
        'krug = Krug(10)\n'
        "krug.radius = 5\n",
        [
            "Traceback (most recent call last):",
            '  File "bez_setter.py", line 11, in <module>',
            "    krug.radius = 5",
            "AttributeError: property 'radius' of 'Krug' object has no setter",
        ],
        "Без декоратора <code class=\"inline\">@radius.setter</code> вторая функция "
        "<code class=\"inline\">radius</code> — это отдельный обычный метод "
        "<code class=\"inline\">radius(self, value)</code>, который просто ЗАМЕНИЛ собой "
        "property сверху (то же имя!). Property без setter доступно только для чтения — "
        "отсюда и ошибка при попытке присвоить значение.",
        "s_setter.py",
        "    @radius.setter\n"
        "    def radius(self, value):\n"
        "        self._radius = value\n",
    )}

    {practice_card(
        "14-11",
        "Практика: property",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-11/index.html",
    )}
    """
    page(
        "14-11-property.html",
        page_title="property: вычисляемые атрибуты",
        description="@property, @x.setter, вычисляемые атрибуты, проверка при присваивании; Debug Lab: property без setter.",
        kicker_suffix="property",
        h1="property: вычисляемые атрибуты",
        lede="@property позволяет вызывать метод так, будто это обычный атрибут — с проверкой "
        "при присваивании и без изменения синтаксиса снаружи.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-12 · Мини-проект: Rectangle
# ---------------------------------------------------------------------------

def build_12() -> None:
    body = f"""
    <h2>Мини-проект: Rectangle</h2>
    <p>Класс прямоугольника с проверенными размерами и вычисляемыми площадью/периметром:</p>
    {code_block(
        "rectangle.py",
        "class Rectangle:\n"
        "    def __init__(self, width, height):\n"
        "        self.width = width\n"
        "        self.height = height\n\n"
        "    @property\n"
        "    def width(self):\n"
        "        return self._width\n\n"
        "    @width.setter\n"
        "    def width(self, value):\n"
        "        if value <= 0:\n"
        '            raise ValueError("ширина должна быть положительной")\n'
        "        self._width = value\n\n"
        "    @property\n"
        "    def height(self):\n"
        "        return self._height\n\n"
        "    @height.setter\n"
        "    def height(self, value):\n"
        "        if value <= 0:\n"
        '            raise ValueError("высота должна быть положительной")\n'
        "        self._height = value\n\n"
        "    @property\n"
        "    def area(self):\n"
        "        return self.width * self.height\n\n"
        "    @property\n"
        "    def perimeter(self):\n"
        "        return 2 * (self.width + self.height)\n",
    )}
    <div style="margin:24px 0">
{class_diagram("Rectangle", ["width  (property)", "height  (property)"], ["area  (property)", "perimeter  (property)"], caption="Rectangle — все четыре доступны как атрибуты, но два из них проверяют значение, два вычисляются")}
    </div>
    {code_block(
        "ispolzovanie.py",
        "r = Rectangle(10, 4)\n"
        "print(r.area, r.perimeter)   # 40 28\n"
        "r.width = 6\n"
        "print(r.area)                 # 24 — пересчиталось само\n"
        "r.width = -1                  # ValueError\n",
    )}

    {exercise(2, "is_square", "Добавьте Rectangle property is_square, возвращающую True, если width равна height.")}

    {practice_card(
        "14-12",
        "Практика: класс Rectangle",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-12/index.html",
    )}
    """
    page(
        "14-12-mini-proekt-rectangle.html",
        page_title="Мини-проект: Rectangle",
        description="Класс Rectangle с проверенными через property width/height и вычисляемыми area/perimeter.",
        kicker_suffix="Мини-проект: Rectangle",
        h1="Мини-проект: Rectangle",
        lede="Проверенные размеры и вычисляемые площадь с периметром — property в реальном "
        "классе.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-13 · Композиция: объекты внутри объектов
# ---------------------------------------------------------------------------

def build_13() -> None:
    body = f"""
    <h2>Объект как атрибут другого объекта</h2>
    <p>В разделе 14.4 класс <code class="inline">Uchastnik</code> хранил объект
    <code class="inline">turtle.Turtle</code> в своём атрибуте <code class="inline">self.t</code>
    — не наследовал от него, а именно ХРАНИЛ. Это называется <strong>композицией</strong>:
    один объект строится ИЗ других объектов, отвечая за них.</p>
{relationship_diagram("Uchastnik", "turtle.Turtle", "has-a", style="has-a", caption="Композиция: Uchastnik ХРАНИТ Turtle в своём атрибуте self.t")}
    {callout(
        "tip",
        "Правило именования отношений: HAS-A",
        "Композицию легко проверить вопросом «X — это Y?» или «X ИМЕЕТ Y?». "
        "<code class=\"inline\">Uchastnik</code> не является черепашкой (HAS-A верно, IS-A "
        "неверно) — поэтому это композиция, а не наследование (о нём — в разделе 14.15).",
    )}

    <h2>Объектный граф: композиция может идти в глубину</h2>
    <p>Объект может хранить не только один объект, а целый список объектов — и те, в свою
    очередь, могут хранить свои:</p>
{tree_diagram(("Zakaz", [("Tovar('Книга', 590)", []), ("Tovar('Ручка', 90)", []), ("Tovar('Тетрадь', 120)", [])]), caption="Zakaz хранит СПИСОК объектов Tovar — композиция, где владелец хранит несколько объектов сразу")}

{debug_lab(
        7,
        "перепутали уровень вложенности атрибута",
        "propushchennyj_uroven.py",
        "class Mashina:\n"
        "    def __init__(self):\n"
        "        self.dvigatel = Dvigatel()\n\n"
        "mashina = Mashina()\n"
        "mashina.start()     # а где именно определён start()?\n",
        [
            "Traceback (most recent call last):",
            '  File "propushchennyj_uroven.py", line 5, in <module>',
            "    mashina.start()",
            "AttributeError: 'Mashina' object has no attribute 'start'",
        ],
        "<code class=\"inline\">start()</code> определён у <code class=\"inline\">Dvigatel"
        "</code>, а не у <code class=\"inline\">Mashina</code> — при композиции методы "
        "вложенного объекта НЕ становятся автоматически методами владельца. Нужно обратиться "
        "явно, через тот атрибут, в котором вложенный объект хранится.",
        "cherez_atribut.py",
        "mashina.dvigatel.start()   # явно: через self.dvigatel\n",
    )}

    {practice_card(
        "14-13",
        "Практика: композиция",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-13/index.html",
    )}
    """
    page(
        "14-13-kompozitsiya.html",
        page_title="Композиция: объекты внутри объектов",
        description="HAS-A отношение, объектные графы, композиция в глубину; Debug Lab: пропущенный уровень вложенности.",
        kicker_suffix="Композиция",
        h1="Композиция: объекты внутри объектов",
        lede="Один объект может ХРАНИТЬ другие объекты, отвечая за них — так был устроен "
        "Uchastnik ещё в разделе 14.4.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-14 · Мини-проект: Корзина покупок v2
# ---------------------------------------------------------------------------

def build_14() -> None:
    body = f"""
    <h2>Мини-проект: Корзина покупок v2</h2>
    <p>В главе 12 корзина покупок хранилась как список словарей. Теперь у нас есть инструменты,
    чтобы сделать её надёжнее: класс <code class="inline">Tovar</code> для одного товара и класс
    <code class="inline">Korzina</code>, который хранит СПИСОК объектов <code class="inline">
    Tovar</code> — композиция из раздела 14.13 в действии.</p>
    {code_block(
        "korzina_v2.py",
        "class Tovar:\n"
        "    def __init__(self, nazvanie, tsena):\n"
        "        self.nazvanie = nazvanie\n"
        "        self.tsena = tsena\n\n\n"
        "class Korzina:\n"
        "    def __init__(self):\n"
        "        self.tovary = []      # атрибут ЭКЗЕМПЛЯРА — раздел 14.8!\n\n"
        "    def dobavit_tovar(self, tovar):\n"
        "        self.tovary.append(tovar)\n\n"
        "    def obshchaya_summa(self):\n"
        "        return sum(t.tsena for t in self.tovary)\n\n"
        "    def kolichestvo_tovarov(self):\n"
        "        return len(self.tovary)\n",
    )}
{relationship_diagram("Korzina", "Tovar", "has-a (список)", style="has-a", caption="Korzina хранит список объектов Tovar")}
    {code_block(
        "ispolzovanie.py",
        "korzina = Korzina()\n"
        'korzina.dobavit_tovar(Tovar("Книга", 590))\n'
        'korzina.dobavit_tovar(Tovar("Ручка", 90))\n\n'
        "print(korzina.kolichestvo_tovarov())   # 2\n"
        "print(korzina.obshchaya_summa())        # 680\n",
    )}
    {callout(
        "info",
        "Почему это лучше словаря",
        "У объекта <code class=\"inline\">Tovar</code> всегда есть ровно <code class=\"inline\">"
        "nazvanie</code> и <code class=\"inline\">tsena</code> — опечатка в ключе словаря "
        "(<code class=\"inline\">tovar[\"cena\"]</code> вместо <code class=\"inline\">tovar["
        "\"tsena\"]</code>) обнаружится только во время выполнения, а обращение к "
        "несуществующему атрибуту объекта — тоже во время выполнения, но с классом легче "
        "добавить проверки и методы (подсчёт суммы, скидки) в одном понятном месте.",
    )}

    {exercise(2, "udalit_tovar", "Добавьте Korzina метод udalit_tovar(self, nazvanie), удаляющий из self.tovary первый товар с этим названием.")}

    {practice_card(
        "14-14",
        "Практика: Корзина покупок v2",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-14/index.html",
    )}
    """
    page(
        "14-14-mini-proekt-korzina-v2.html",
        page_title="Мини-проект: Корзина покупок v2",
        description="Переписываем корзину покупок главы 12 на объекты: Tovar и Korzina через композицию.",
        kicker_suffix="Мини-проект: Корзина v2",
        h1="Мини-проект: Корзина покупок v2",
        lede="Список словарей из главы 12 становится списком объектов Tovar внутри Korzina.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-15 · Наследование
# ---------------------------------------------------------------------------

def build_15() -> None:
    body = f"""
    <h2>Строим класс на основе существующего</h2>
    <p>Если два класса имеют много общего, но один — более общее понятие, а другой — его
    частный случай, отношение между ними — <strong>IS-A</strong> («Кошка — это животное»). Для
    такого отношения в Python есть <strong>наследование</strong>:</p>
    {code_block(
        "nasledovanie.py",
        "class Zhivotnoe:\n"
        "    def __init__(self, klichka):\n"
        "        self.klichka = klichka\n\n"
        "    def predstavitsya(self):\n"
        '        print(f"Я {self.klichka}")\n\n\n'
        "class Sobaka(Zhivotnoe):     # Sobaka — это Zhivotnoe\n"
        "    def zvuk(self):\n"
        '        return "Гав!"\n\n\n'
        "class Koshka(Zhivotnoe):     # Koshka — это тоже Zhivotnoe\n"
        "    def zvuk(self):\n"
        '        return "Мяу!"\n\n\n'
        'rex = Sobaka("Рекс")\n'
        "rex.predstavitsya()    # унаследовано от Zhivotnoe — работает без переопределения\n"
        "print(rex.zvuk())       # своё, определено в Sobaka\n",
    )}
{tree_diagram(("Zhivotnoe", [("Sobaka", []), ("Koshka", [])]), caption="Sobaka и Koshka наследуют от Zhivotnoe — общее поведение (predstavitsya) не нужно писать дважды")}
{relationship_diagram("Sobaka", "Zhivotnoe", "is-a", style="is-a", caption="IS-A: открытый треугольник указывает на родителя")}
    {callout(
        "tip",
        "Наследование — это переиспользование, а не обязанность",
        "<code class=\"inline\">Sobaka</code> получает <code class=\"inline\">predstavitsya()"
        "</code> БЕСПЛАТНО, ничего не переписывая — в этом весь смысл. Но наследование "
        "оправдано только когда отношение реально IS-A. Если тянет унаследовать класс просто "
        "чтобы «одолжить» пару методов без настоящего родства понятий — это сигнал, что нужна "
        "композиция (раздел 14.13), а не наследование.",
    )}

{debug_lab(
        8,
        "забыли вызвать super().__init__()",
        "propushchennyj_super.py",
        "class Zhivotnoe:\n"
        "    def __init__(self, klichka):\n"
        "        self.klichka = klichka\n\n\n"
        "class Sobaka(Zhivotnoe):\n"
        "    def __init__(self, klichka, poroda):\n"
        "        self.poroda = poroda     # klichka из Zhivotnoe не настроен!\n\n"
        'rex = Sobaka("Рекс", "Дворняга")\n'
        "print(rex.klichka)\n",
        [
            "Traceback (most recent call last):",
            '  File "propushchennyj_super.py", line 9, in <module>',
            "    print(rex.klichka)",
            "AttributeError: 'Sobaka' object has no attribute 'klichka'",
        ],
        "Когда дочерний класс определяет СОБСТВЕННЫЙ <code class=\"inline\">__init__</code>, он "
        "полностью ЗАМЕНЯЕТ родительский <code class=\"inline\">__init__</code> — родительский "
        "код настройки атрибутов сам по себе больше не выполняется. Чтобы получить и то, и "
        "другое, дочерний <code class=\"inline\">__init__</code> должен явно вызвать "
        "родительский — разберём как именно, в разделе 14.16.",
        "s_super.py",
        "class Sobaka(Zhivotnoe):\n"
        "    def __init__(self, klichka, poroda):\n"
        "        super().__init__(klichka)   # сначала настраиваем родительскую часть\n"
        "        self.poroda = poroda\n",
    )}

    {practice_card(
        "14-15",
        "Практика: наследование",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-15/index.html",
    )}
    """
    page(
        "14-15-nasledovanie.html",
        page_title="Наследование",
        description="IS-A отношение, class Child(Parent), переиспользование поведения; Debug Lab: пропущенный super().__init__().",
        kicker_suffix="Наследование",
        h1="Наследование",
        lede="Когда один класс — это более частный случай другого, наследование позволяет не "
        "переписывать общее поведение заново.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-16 · super() и порядок разрешения методов
# ---------------------------------------------------------------------------

def build_16() -> None:
    body = f"""
    <h2>super(): позвать родителя, а не заменить его</h2>
    <p><code class="inline">super()</code> даёт доступ к методам родительского класса ИЗНУТРИ
    переопределённого метода — обычно чтобы ДОПОЛНИТЬ поведение родителя, а не заменить его
    целиком:</p>
    {code_block(
        "super_init.py",
        "class Zhivotnoe:\n"
        "    def __init__(self, klichka):\n"
        "        self.klichka = klichka\n\n\n"
        "class Sobaka(Zhivotnoe):\n"
        "    def __init__(self, klichka, poroda):\n"
        "        super().__init__(klichka)   # выполняет Zhivotnoe.__init__(self, klichka)\n"
        "        self.poroda = poroda         # затем добавляет своё\n\n"
        'rex = Sobaka("Рекс", "Дворняга")\n'
        "print(rex.klichka, rex.poroda)   # Рекс Дворняга — оба атрибута на месте\n",
    )}
    {callout(
        "warning",
        "Частое заблуждение: «super() возвращает объект родительского класса»",
        "Это не так. <code class=\"inline\">super()</code> возвращает специальный "
        "промежуточный объект (прокси), который умеет находить методы РОДИТЕЛЯ для ТЕКУЩЕГО "
        "<code class=\"inline\">self</code> — <code class=\"inline\">self</code> остаётся "
        "объектом класса <code class=\"inline\">Sobaka</code>, он не превращается в "
        "<code class=\"inline\">Zhivotnoe</code>. Просто поиск метода на этот раз начинается "
        "не с <code class=\"inline\">Sobaka</code>, а на уровень выше.",
    )}

    <h2>Порядок разрешения методов (MRO)</h2>
    <p>При обычном одиночном наследовании порядок поиска метода простой и предсказуемый:
    сначала сам класс объекта, затем его родитель, затем родитель родителя — и так до
    <code class="inline">object</code>, базового класса для всех классов в Python:</p>
{flow_diagram([("Sobaka", "сначала здесь"), ("Zhivotnoe", "затем здесь"), ("object", "и в самом конце")], caption="MRO для одиночного наследования — предсказуемый порядок поиска")}

{debug_lab(
        9,
        "используют атрибут ДО вызова super().__init__()",
        "nepravilnyj_poryadok.py",
        "class Sobaka(Zhivotnoe):\n"
        "    def __init__(self, klichka, poroda):\n"
        "        self.poroda = poroda\n"
        '        print(f"Порода: {self.poroda}, кличка: {self.klichka}")   # klichka ещё нет!\n'
        "        super().__init__(klichka)\n",
        [
            "Traceback (most recent call last):",
            "    print(f\"Порода: {self.poroda}, кличка: {self.klichka}\")",
            "AttributeError: 'Sobaka' object has no attribute 'klichka'",
        ],
        "<code class=\"inline\">super().__init__(klichka)</code> стоит ПОСЛЕ строки, которая "
        "уже пытается прочитать <code class=\"inline\">self.klichka</code> — на этот момент "
        "родительский <code class=\"inline\">__init__</code> ещё не выполнялся, атрибут ещё не "
        "создан. Порядок вызовов внутри <code class=\"inline\">__init__</code> исполняется "
        "строго сверху вниз, как и в любой другой функции.",
        "pravilnyj_poryadok.py",
        "class Sobaka(Zhivotnoe):\n"
        "    def __init__(self, klichka, poroda):\n"
        "        super().__init__(klichka)   # сначала родительская часть\n"
        "        self.poroda = poroda\n"
        '        print(f"Порода: {self.poroda}, кличка: {self.klichka}")\n',
    )}

    {practice_card(
        "14-16",
        "Практика: super()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-16/index.html",
    )}
    """
    page(
        "14-16-super.html",
        page_title="super() и порядок разрешения методов",
        description="super() как способ дополнить, а не заменить поведение родителя; MRO для одиночного наследования; Debug Lab: неверный порядок вызова.",
        kicker_suffix="super()",
        h1="super() и порядок разрешения методов",
        lede="super() позволяет дочернему классу воспользоваться методом родителя изнутри "
        "переопределения — а не заново писать его с нуля.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-17 · Переопределение методов
# ---------------------------------------------------------------------------

def build_17() -> None:
    body = f"""
    <h2>Переопределение: свой вариант метода родителя</h2>
    <p>Дочерний класс может определить метод с ТЕМ ЖЕ именем, что и у родителя — это называется
    <strong>переопределением</strong> (override). Python при поиске метода находит версию
    дочернего класса первой (раздел 14.16, MRO) и использует именно её:</p>
    {code_block(
        "pereopredelenie.py",
        "class Zhivotnoe:\n"
        "    def zvuk(self):\n"
        '        print("Какое-то животное издаёт звук")\n\n\n'
        "class Sobaka(Zhivotnoe):\n"
        "    def zvuk(self):     # полностью заменяет родительскую версию\n"
        '        print("Гав!")\n\n'
        'Sobaka().zvuk()   # Гав! — версия Zhivotnoe даже не вызывается\n',
    )}
    <p>Иногда нужно не полностью заменить поведение родителя, а ДОПОЛНИТЬ его — тогда
    переопределённый метод вызывает <code class="inline">super().метод()</code> и добавляет
    что-то своё:</p>
    {code_block(
        "rasshirenie.py",
        "class Zhivotnoe:\n"
        "    def zvuk(self):\n"
        '        print("Животное подаёт голос:")\n\n\n'
        "class Sobaka(Zhivotnoe):\n"
        "    def zvuk(self):\n"
        "        super().zvuk()     # сначала родительская часть\n"
        '        print("Гав!")      # затем своя\n\n'
        "Sobaka().zvuk()\n"
        '# Животное подаёт голос:\n'
        "# Гав!\n",
    )}

{debug_lab(
        10,
        "переопределили метод, но забыли расширить через super()",
        "poteryannoe_povedenie.py",
        "class Zhivotnoe:\n"
        "    def zvuk(self):\n"
        '        print("Животное подаёт голос:")\n\n\n'
        "class Sobaka(Zhivotnoe):\n"
        "    def zvuk(self):\n"
        '        print("Гав!")     # хотели ДОПОЛНИТЬ, но случайно заменили целиком\n\n'
        "Sobaka().zvuk()\n",
        [
            ">>> Sobaka().zvuk()",
            "Гав!",
        ],
        "Строка «Животное подаёт голос:» пропала — переопределение по умолчанию ЗАМЕНЯЕТ "
        "родительский метод целиком, а не дополняет его автоматически. Если задумывалось "
        "именно дополнение, вызов <code class=\"inline\">super().zvuk()</code> нужно "
        "прописать явно — Python никогда не вызывает родительскую версию сам, если вы её не "
        "попросили.",
        "s_rasshireniem.py",
        "class Sobaka(Zhivotnoe):\n"
        "    def zvuk(self):\n"
        "        super().zvuk()\n"
        '        print("Гав!")\n',
    )}

    {practice_card(
        "14-17",
        "Практика: переопределение методов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-17/index.html",
    )}
    """
    page(
        "14-17-pereopredelenie-metodov.html",
        page_title="Переопределение методов",
        description="override: замена метода родителя полностью или через super() как дополнение; Debug Lab: случайная потеря родительского поведения.",
        kicker_suffix="Переопределение методов",
        h1="Переопределение методов",
        lede="Дочерний класс может заменить метод родителя целиком — или дополнить его через "
        "super().",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-18 · Полиморфизм
# ---------------------------------------------------------------------------

def build_18() -> None:
    body = f"""
    <h2>Один вызов, разные результаты</h2>
    <p><strong>Полиморфизм</strong> («много форм») — когда один и тот же вызов метода даёт
    разное поведение в зависимости от того, у объекта какого класса он вызван:</p>
    {code_block(
        "polimorfizm.py",
        "class Sobaka:\n"
        "    def zvuk(self):\n"
        '        return "Гав!"\n\n\n'
        "class Koshka:\n"
        "    def zvuk(self):\n"
        '        return "Мяу!"\n\n\n'
        "class Korova:\n"
        "    def zvuk(self):\n"
        '        return "Му!"\n\n\n'
        "zhivotnye = [Sobaka(), Koshka(), Korova()]\n"
        "for zh in zhivotnye:\n"
        "    print(zh.zvuk())    # каждый раз вызывается СВОЯ версия zvuk()\n",
    )}
{branch_diagram("zvuk()", [("Sobaka", "Гав!"), ("Koshka", "Мяу!"), ("Korova", "Му!")], caption="Один и тот же вызов .zvuk() — разный результат для каждого класса")}
    {callout(
        "info",
        "Цикл не знает и не должен знать, с каким классом работает",
        "Строка <code class=\"inline\">zh.zvuk()</code> внутри цикла ОДНА — ей не нужно "
        "проверять <code class=\"inline\">if isinstance(zh, Sobaka): ...</code> и так для "
        "каждого класса. Именно в этом ценность полиморфизма: код, который ИСПОЛЬЗУЕТ объекты, "
        "остаётся простым и не растёт с каждым новым классом животного.",
    )}

    {practice_card(
        "14-18",
        "Практика: полиморфизм",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-18/index.html",
    )}
    """
    page(
        "14-18-polimorfizm.html",
        page_title="Полиморфизм",
        description="Один вызов метода — разное поведение в зависимости от класса объекта; код, использующий объекты, не растёт с числом классов.",
        kicker_suffix="Полиморфизм",
        h1="Полиморфизм",
        lede="Одна и та же строка кода — .zvuk() — ведёт себя по-разному в зависимости от того, "
        "какой именно объект её вызвал.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-19 · Duck typing
# ---------------------------------------------------------------------------

def build_19() -> None:
    body = f"""
    <h2>«Если это выглядит как утка и крякает как утка...»</h2>
    <p>В разделе 14.18 все классы разделяли общего родителя не всегда. На самом деле Python
    вообще не проверяет, от какого класса объект унаследован, чтобы вызвать метод — важно
    только, ЕСТЬ ли у объекта нужный метод:</p>
    {code_block(
        "duck_typing.py",
        "class Sobaka:                    # никак не связана с Robot\n"
        "    def predstavitsya(self):\n"
        '        print("Гав! Я собака.")\n\n\n'
        "class Robot:                     # никак не связана с Sobaka\n"
        "    def predstavitsya(self):\n"
        '        print("БИП. Я робот.")\n\n\n'
        "def poznakomit(obj):\n"
        "    obj.predstavitsya()   # неважно, какого obj класса — важно, что метод есть\n\n"
        "poznakomit(Sobaka())\n"
        "poznakomit(Robot())\n",
    )}
    {callout(
        "warning",
        "Частое заблуждение: «полиморфизм требует наследования»",
        "Это не так, и duck typing — прямое тому доказательство. <code class=\"inline\">Sobaka"
        "</code> и <code class=\"inline\">Robot</code> НЕ имеют общего родителя (кроме "
        "неявного <code class=\"inline\">object</code>), но <code class=\"inline\">poznakomit()"
        "</code> одинаково успешно работает с обоими. В Python интерфейс — это фактическое "
        "наличие нужного метода, а не формальная запись в дереве наследования.",
    )}
    <p>Название пришло из выражения «если оно выглядит как утка, плавает как утка и крякает как
    утка — вероятно, это и есть утка»: неважно, как объект был создан, важно, что он УМЕЕТ.</p>

{debug_lab(
        11,
        "не у всех объектов в списке есть ожидаемый метод",
        "nesovmestimyj_obekt.py",
        'zhivotnye = [Sobaka(), Robot(), "просто строка"]\n'
        "for zh in zhivotnye:\n"
        "    zh.predstavitsya()\n",
        [
            "Гав! Я собака.",
            "БИП. Я робот.",
            "Traceback (most recent call last):",
            "AttributeError: 'str' object has no attribute 'predstavitsya'",
        ],
        "Duck typing не проверяет наличие метода заранее — Python просто пытается вызвать "
        "<code class=\"inline\">predstavitsya()</code> и падает в момент вызова, если метода "
        "нет. Гибкость duck typing не отменяет ответственность: класть в один список объекты, "
        "которые ДОЛЖНЫ поддерживать общий метод, нужно осознанно.",
        "s_proverkoj.py",
        "for zh in zhivotnye:\n"
        '    if hasattr(zh, "predstavitsya"):\n'
        "        zh.predstavitsya()\n",
    )}

    {practice_card(
        "14-19",
        "Практика: duck typing",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-19/index.html",
    )}
    """
    page(
        "14-19-duck-typing.html",
        page_title="Duck typing",
        description="Полиморфизм без общего родителя: важно наличие метода, а не место в иерархии наследования; Debug Lab: несовместимый объект в списке.",
        kicker_suffix="Duck typing",
        h1="Duck typing",
        lede="Python не проверяет, от какого класса унаследован объект — только то, есть ли у "
        "него нужный метод.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-20 · Мини-проект: полиморфные фигуры
# ---------------------------------------------------------------------------

def build_20() -> None:
    body = f"""
    <h2>Мини-проект: полиморфные фигуры</h2>
    <p>Общий предок <code class="inline">Figura</code> хранит имя фигуры; каждая конкретная
    фигура переопределяет <code class="inline">ploshchad()</code> по-своему — наследование
    (14.15) и полиморфизм (14.18) вместе:</p>
    {code_block(
        "figury.py",
        "class Figura:\n"
        "    def __init__(self, nazvanie):\n"
        "        self.nazvanie = nazvanie\n\n"
        "    def ploshchad(self):\n"
        "        raise NotImplementedError\n\n\n"
        "class Krug(Figura):\n"
        "    def __init__(self, radius):\n"
        '        super().__init__("круг")\n'
        "        self.radius = radius\n\n"
        "    def ploshchad(self):\n"
        "        return 3.14159 * self.radius ** 2\n\n\n"
        "class Pryamougolnik(Figura):\n"
        "    def __init__(self, width, height):\n"
        '        super().__init__("прямоугольник")\n'
        "        self.width = width\n"
        "        self.height = height\n\n"
        "    def ploshchad(self):\n"
        "        return self.width * self.height\n\n\n"
        "class Treugolnik(Figura):\n"
        "    def __init__(self, base, height):\n"
        '        super().__init__("треугольник")\n'
        "        self.base = base\n"
        "        self.height = height\n\n"
        "    def ploshchad(self):\n"
        "        return 0.5 * self.base * self.height\n",
    )}
{tree_diagram(("Figura", [("Krug", []), ("Pryamougolnik", []), ("Treugolnik", [])]), caption="Все три фигуры — IS-A Figura, каждая переопределяет ploshchad() по-своему")}
    {code_block(
        "ispolzovanie.py",
        "figury = [Krug(5), Pryamougolnik(4, 6), Treugolnik(8, 3)]\n"
        "for f in figury:\n"
        '    print(f"{f.nazvanie}: {f.ploshchad():.2f}")\n\n'
        "# круг: 78.54\n"
        "# прямоугольник: 24.00\n"
        "# треугольник: 12.00\n",
    )}
    {callout(
        "tip",
        "raise NotImplementedError — сигнал «доделай в наследнике»",
        "<code class=\"inline\">Figura.ploshchad()</code> намеренно не вычисляет ничего "
        "полезного — она существует только чтобы задать ОБЩИЙ ИНТЕРФЕЙС, который обязаны "
        "реализовать наследники. Если забыть переопределить <code class=\"inline\">ploshchad()"
        "</code> в новой фигуре, ошибка обнаружится сразу же при первом вызове, а не тихо "
        "выдаст неверную площадь.",
    )}

    {exercise(2, "perimetr", "Добавьте Figura метод-заглушку perimetr() (raise NotImplementedError) и реализуйте его во всех трёх фигурах. Подсказка для Treugolnik: base и height одних не хватает для точного периметра — считайте его равнобедренным и найдите боковую сторону по теореме Пифагора.")}

    {practice_card(
        "14-20",
        "Практика: полиморфные фигуры",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-20/index.html",
    )}
    """
    page(
        "14-20-mini-proekt-figury.html",
        page_title="Мини-проект: полиморфные фигуры",
        description="Figura, Krug, Pryamougolnik, Treugolnik — наследование и полиморфизм в одном мини-проекте.",
        kicker_suffix="Мини-проект: фигуры",
        h1="Мини-проект: полиморфные фигуры",
        lede="Общий предок задаёт интерфейс, каждая фигура реализует его по-своему — "
        "наследование и полиморфизм вместе.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-21 · Специальные методы (dunders)
# ---------------------------------------------------------------------------

def build_21() -> None:
    body = f"""
    <h2>Как объекты подключаются к встроенным операциям</h2>
    <p>Когда вы пишете <code class="inline">print(rex)</code> или <code class="inline">len(text)
    </code>, Python на самом деле вызывает специальный метод объекта с именем вида
    <code class="inline">__имя__</code> («дандер», double underscore). Вы уже пользовались
    одним таким методом с самого начала главы — <code class="inline">__init__</code>.</p>
    {comparison_table(
        ["Что вы пишете", "Что Python вызывает на самом деле"],
        [
            ["<code class=\"inline\">Sobaka(\"Рекс\", 3)</code>", "<code class=\"inline\">__init__(self, ...)</code>"],
            ["<code class=\"inline\">print(rex)</code>", "<code class=\"inline\">__str__(self)</code>"],
            ["<code class=\"inline\">len(korzina)</code>", "<code class=\"inline\">__len__(self)</code>"],
            ["<code class=\"inline\">a + b</code>", "<code class=\"inline\">__add__(self, other)</code>"],
            ["<code class=\"inline\">a == b</code>", "<code class=\"inline\">__eq__(self, other)</code>"],
        ],
    )}

    <h2>__str__ и __repr__</h2>
    <p>Без специального метода <code class="inline">print(объект)</code> выводит малополезную
    строку вроде <code class="inline">&lt;__main__.Sobaka object at 0x7f...&gt;</code>.
    <code class="inline">__str__</code> позволяет задать понятный человеку вид:</p>
    {code_block(
        "str_metod.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast):\n"
        "        self.klichka = klichka\n"
        "        self.vozrast = vozrast\n\n"
        "    def __str__(self):\n"
        '        return f"{self.klichka} ({self.vozrast} года)"\n\n'
        'rex = Sobaka("Рекс", 3)\n'
        "print(rex)   # Рекс (3 года) — а не адрес в памяти\n",
    )}

    <h2>__eq__: сравнение по значению, а не по идентичности</h2>
    <p>В разделе 14.9 <code class="inline">a1 == a2</code> у двух Player с одинаковыми
    значениями оказалось <code class="inline">False</code> — потому что <code class="inline">==
    </code> по умолчанию сравнивает объекты как разные ячейки памяти. <code class="inline">
    __eq__</code> это меняет:</p>
    {code_block(
        "eq_metod.py",
        "class Sobaka:\n"
        "    def __init__(self, klichka, vozrast):\n"
        "        self.klichka = klichka\n"
        "        self.vozrast = vozrast\n\n"
        "    def __eq__(self, other):\n"
        "        return self.klichka == other.klichka and self.vozrast == other.vozrast\n\n"
        'Sobaka("Рекс", 3) == Sobaka("Рекс", 3)   # теперь True\n',
    )}

{debug_lab(
        12,
        "__eq__ определили, а объект стал unhashable",
        "unhashable_obekt.py",
        "class Tochka:\n"
        "    def __init__(self, x, y):\n"
        "        self.x = x\n"
        "        self.y = y\n\n"
        "    def __eq__(self, other):\n"
        "        return self.x == other.x and self.y == other.y\n\n"
        "tochki = {Tochka(1, 2), Tochka(3, 4)}   # положили объекты в множество\n",
        [
            "Traceback (most recent call last):",
            "TypeError: unhashable type: 'Tochka'",
        ],
        "У объекта по умолчанию есть автоматический <code class=\"inline\">__hash__</code>, "
        "основанный на его адресе в памяти. Как только вы определяете свой "
        "<code class=\"inline\">__eq__</code>, Python СНИМАЕТ автоматический "
        "<code class=\"inline\">__hash__</code> — ведь если объекты «равны» по значению, у "
        "равных объектов логично ожидать и одинаковый хеш, а старый адресный хеш этому больше "
        "не соответствует. Объект без хеша нельзя положить в <code class=\"inline\">set</code> "
        "или использовать как ключ <code class=\"inline\">dict</code>.",
        "s_hash.py",
        "    def __eq__(self, other):\n"
        "        return self.x == other.x and self.y == other.y\n\n"
        "    def __hash__(self):\n"
        "        return hash((self.x, self.y))\n",
    )}

    {practice_card(
        "14-21",
        "Практика: специальные методы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-21/index.html",
    )}
    """
    page(
        "14-21-spetsialnye-metody.html",
        page_title="Специальные методы",
        description="__str__, __eq__, карта dunder-методов и встроенных операций; Debug Lab: __eq__ без __hash__.",
        kicker_suffix="Специальные методы",
        h1="Специальные методы",
        lede="__init__ — не единственный дандер-метод. __str__ и __eq__ подключают объект к "
        "print() и ==.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-22 · Практика: применяем __str__ и __eq__
# ---------------------------------------------------------------------------

def build_22() -> None:
    body = f"""
    <h2>Практика: точка на плоскости</h2>
    <p>Применим оба метода из раздела 14.21 к небольшому классу <code class="inline">Tochka
    </code> — координата <code class="inline">x</code>, <code class="inline">y</code>:</p>
    {code_block(
        "tochka.py",
        "class Tochka:\n"
        "    def __init__(self, x, y):\n"
        "        self.x = x\n"
        "        self.y = y\n\n"
        "    def __str__(self):\n"
        '        return f"({self.x}, {self.y})"\n\n'
        "    def __eq__(self, other):\n"
        "        return self.x == other.x and self.y == other.y\n\n"
        "a = Tochka(1, 2)\n"
        "b = Tochka(1, 2)\n"
        "c = Tochka(5, 5)\n\n"
        "print(a)          # (1, 2)\n"
        "print(a == b)      # True — совпадают координаты\n"
        "print(a == c)      # False\n",
    )}
    {callout(
        "tip",
        "f-string и __str__ работают вместе",
        "<code class=\"inline\">f\"Точка: {a}\"</code> вызывает тот же самый "
        "<code class=\"inline\">__str__</code>, что и <code class=\"inline\">print(a)</code> — "
        "любое место, где Python нужно превратить объект в строку для человека, проходит через "
        "этот метод.",
    )}

    {exercise(2, "rasstoyanie", "Добавьте Tochka метод rasstoyanie_do(self, other), возвращающий евклидово расстояние до другой точки: ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5.")}

    {practice_card(
        "14-22",
        "Практика: __str__ и __eq__ на практике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-22/index.html",
    )}
    """
    page(
        "14-22-primenyaem-dunder-metody.html",
        page_title="Практика: применяем __str__ и __eq__",
        description="Класс Tochka с __str__ и __eq__ — закрепляем специальные методы на практике.",
        kicker_suffix="Практика: dunder-методы",
        h1="Практика: применяем __str__ и __eq__",
        lede="Небольшой класс Tochka — площадка, чтобы закрепить оба метода из раздела 14.21.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-23 · dataclasses
# ---------------------------------------------------------------------------

def build_23() -> None:
    body = f"""
    <h2>Меньше шаблонного кода для классов-данных</h2>
    <p>Классы вроде <code class="inline">Tochka</code> из раздела 14.22 — в основном
    шаблонный код: <code class="inline">__init__</code>, который просто копирует параметры в
    <code class="inline">self</code>, плюс <code class="inline">__str__</code> и
    <code class="inline">__eq__</code>, которые почти всегда выглядят одинаково. Модуль
    <code class="inline">dataclasses</code> умеет сгенерировать всё это автоматически:</p>
    {classic_vs_modern(
        "Класс-данные: вручную и через @dataclass",
        "Обычный класс",
        "class Tochka:\n"
        "    def __init__(self, x, y):\n"
        "        self.x = x\n"
        "        self.y = y\n\n"
        "    def __repr__(self):\n"
        "        return f\"Tochka(x={self.x}, y={self.y})\"\n\n"
        "    def __eq__(self, other):\n"
        "        return self.x == other.x and self.y == other.y\n",
        "С @dataclass",
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class Tochka:\n"
        "    x: int\n"
        "    y: int\n"
        "# __init__, __repr__ и __eq__ сгенерированы автоматически\n",
        "@dataclass — там, где класс в основном ХРАНИТ данные и не выигрывает от ручного "
        "контроля над __init__/__repr__/__eq__. Он всё ещё обычный класс — методы добавляются "
        "в тело точно так же, как и всегда.",
    )}
    {code_block(
        "dataclass_s_metodom.py",
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class Tochka:\n"
        "    x: int\n"
        "    y: int\n\n"
        "    def rasstoyanie_do(self, other):\n"
        "        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5\n\n"
        "a = Tochka(0, 0)\n"
        "b = Tochka(3, 4)\n"
        "print(a)                    # Tochka(x=0, y=0) — __repr__ уже готов\n"
        "print(a.rasstoyanie_do(b))   # 5.0\n",
    )}
    {callout(
        "warning",
        "Частое заблуждение: «dataclass — это не настоящий класс» или «в dataclass нельзя писать методы»",
        "Оба неверны. <code class=\"inline\">@dataclass</code> — это обычный декоратор класса: "
        "он лишь ДОБАВЛЯЕТ автосгенерированные <code class=\"inline\">__init__</code>, <code "
        "class=\"inline\">__repr__</code>, <code class=\"inline\">__eq__</code> поверх "
        "обычного тела класса. Методы, property и вообще всё, что можно писать в обычном "
        "классе, точно так же пишется и в dataclass.",
    )}

{debug_lab(
        13,
        "изменяемое значение по умолчанию в dataclass",
        "izmenyaemoe_polei_umolchanie.py",
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class Korzina:\n"
        "    tovary: list = []   # похоже на ловушку из раздела 14.8!\n",
        [
            "Traceback (most recent call last):",
            "ValueError: mutable default <class 'list'> for field tovary is not allowed",
        ],
        "Python <code class=\"inline\">dataclasses</code> УМЫШЛЕННО запрещает изменяемое "
        "значение по умолчанию прямо в аннотации — это тот же самый риск общего списка на все "
        "объекты, что и в разделе 14.8, только для dataclass он обнаруживается сразу, ошибкой "
        "при определении класса, а не тихим багом во время выполнения.",
        "s_default_factory.py",
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\n"
        "class Korzina:\n"
        "    tovary: list = field(default_factory=list)   # новый список для КАЖДОГО объекта\n",
    )}

    {practice_card(
        "14-23",
        "Практика: dataclasses",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-23/index.html",
    )}
    """
    page(
        "14-23-dataclasses.html",
        page_title="dataclasses",
        description="@dataclass как способ избежать шаблонного __init__/__repr__/__eq__; field(default_factory=...); Debug Lab: изменяемое значение по умолчанию.",
        kicker_suffix="dataclasses",
        h1="dataclasses",
        lede="Классы, которые в основном хранят данные, не обязаны писать __init__ и __repr__ "
        "вручную.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-24 · Практика: dataclass
# ---------------------------------------------------------------------------

def build_24() -> None:
    body = f"""
    <h2>Практика: Tovar как dataclass</h2>
    <p>Перепишем <code class="inline">Tovar</code> из раздела 14.14 через
    <code class="inline">@dataclass</code>:</p>
    {code_block(
        "tovar_dataclass.py",
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class Tovar:\n"
        "    nazvanie: str\n"
        "    tsena: float\n\n"
        "    def so_skidkoj(self, protsent):\n"
        "        return self.tsena * (1 - protsent / 100)\n\n"
        'knigi = Tovar("Книга", 590)\n'
        "print(knigi)                    # Tovar(nazvanie='Книга', tsena=590)\n"
        "print(knigi.so_skidkoj(10))      # 531.0\n",
    )}
    {callout(
        "tip",
        "__eq__ достаётся бесплатно",
        "<code class=\"inline\">Tovar(\"Книга\", 590) == Tovar(\"Книга\", 590)</code> — "
        "<code class=\"inline\">True</code>, хотя мы не писали <code class=\"inline\">__eq__"
        "</code> вручную ни разу: dataclass сравнивает по значениям всех полей автоматически.",
    )}

    {exercise(2, "Zakaz как dataclass", "Определите @dataclass Zakaz с полями tovar: Tovar и kolichestvo: int, и методом summa(self), возвращающим self.tovar.tsena * self.kolichestvo.")}

    {practice_card(
        "14-24",
        "Практика: dataclass Tovar",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-24/index.html",
    )}
    """
    page(
        "14-24-praktika-dataclass.html",
        page_title="Практика: dataclass",
        description="Переписываем Tovar главы 14.14 через @dataclass — практика на автосгенерированные __init__/__repr__/__eq__.",
        kicker_suffix="Практика: dataclass",
        h1="Практика: dataclass",
        lede="Tovar главы 14.14, но короче — @dataclass берёт на себя шаблонный код.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-25 · Класс или не класс? Проектируем модели
# ---------------------------------------------------------------------------

def build_25() -> None:
    body = f"""
    <h2>Не каждая задача требует класса</h2>
    <p>После 24 разделов про классы легко решить, что классом нужно оборачивать вообще всё.
    Это не так — класс полезен, когда есть И состояние, И поведение, которые имеет смысл
    держать вместе, и когда объектов этого вида будет несколько, с независимой историей.</p>
    {decision_map(
        [
            ("Нужно и хранить данные, и выполнять над ними действия?", "→ вероятно, класс"),
            ("Будет несколько независимых экземпляров с разным состоянием?", "→ класс"),
            ("Это разовое вычисление без хранимого состояния?", "→ обычная функция"),
            ("Данные без всякого поведения, читаются один раз?", "→ dict / tuple / dataclass без методов"),
            ("Нужна проверка при изменении значения?", "→ property (раздел 14.11)"),
        ],
        title="Класс или не класс?",
    )}

{debug_lab(
        14,
        "класс ради одного вычисления без состояния",
        "izlishnij_klass.py",
        "class SredneeArifmeticheskoe:\n"
        "    def __init__(self, chisla):\n"
        "        self.chisla = chisla\n\n"
        "    def vychislit(self):\n"
        "        return sum(self.chisla) / len(self.chisla)\n\n"
        "rezultat = SredneeArifmeticheskoe([4, 8, 15]).vychislit()\n",
        [
            "# Код работает правильно — ошибка не во время выполнения,",
            "# а в самом ДИЗАЙНЕ: слишком много церемоний для одного вычисления",
        ],
        "Формально это рабочий код, но здесь нет ни настоящего состояния (объект создаётся и "
        "сразу используется один раз), ни нескольких экземпляров — просто вычисление, "
        "притворяющееся классом. Обычная функция читается и тестируется проще: "
        "<code class=\"inline\">srednee(chisla)</code>. Класс оправдан, когда объект живёт "
        "какое-то время И меняет состояние — как <code class=\"inline\">Player</code> из "
        "раздела 14.9, а не когда он существует одну строчку.",
        "prostaya_funkciya.py",
        "def srednee_arifmeticheskoe(chisla):\n"
        "    return sum(chisla) / len(chisla)\n\n"
        "rezultat = srednee_arifmeticheskoe([4, 8, 15])\n",
    )}

    {callout(
        "tip",
        "Признаки, что классу самое место",
        "Объект несколько раз меняет состояние ПОСЛЕ создания (не только при __init__); в "
        "программе будет больше одного такого объекта одновременно; данные и действия над "
        "ними логически связаны настолько, что разделять их неудобно. Если ни один признак не "
        "выполняется — начните с функции или словаря, класс всегда можно добавить позже, когда "
        "он реально понадобится.",
    )}

    {exercise(2, "Функция или класс?", "Для каждого сценария решите, что уместнее — функция или класс, и обоснуйте: (1) перевод температуры из Цельсия в Фаренгейт; (2) банковский счёт с балансом и историей операций; (3) проверка, является ли число простым.")}

    {practice_card(
        "14-25",
        "Практика: класс или не класс",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/14-25/index.html",
    )}
    """
    page(
        "14-25-proektiruem-modeli.html",
        page_title="Класс или не класс? Проектируем модели",
        description="Когда класс оправдан, а когда достаточно функции или словаря; финальный чек-лист проектирования; Debug Lab: излишний класс.",
        kicker_suffix="Класс или не класс?",
        h1="Класс или не класс? Проектируем модели",
        lede="Не каждая задача требует класса — а неправильный выбор виден не сразу, а только "
        "когда код становится сложнее читать.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-26 · Мини-проект: гонка Turtle v2 (композиция, объект-менеджер)
# ---------------------------------------------------------------------------

def build_26() -> None:
    body = f"""
    <h2>Мини-проект: гонка Turtle v2</h2>
    <p>Расширим проект из раздела 14.4. На этот раз не только участники (<code class="inline">
    Uchastnik</code>) — сама гонка тоже становится объектом: класс <code class="inline">Gonka
    </code> хранит список участников, рисует финишную линию и определяет порядок финиша —
    ещё один пример композиции (раздел 14.13), но уже объект, управляющий другими объектами.</p>
{turtle_output("14-gonka-v2", "gonka_v2.py", caption="Gonka хранит трёх Uchastnik и сама рисует финишную линию", alt="Три черепашки на дорожках рядом с вертикальной финишной линией")}
{relationship_diagram("Gonka", "Uchastnik", "has-a (список)", style="has-a", caption="Gonka хранит список объектов Uchastnik и управляет гонкой в целом")}
    {callout(
        "info",
        "Объекты, сотрудничающие друг с другом",
        "<code class=\"inline\">Gonka</code> не дублирует логику шага или проверки финиша — она "
        "делегирует её каждому <code class=\"inline\">Uchastnik</code> "
        "(<code class=\"inline\">u.sdelat_shag()</code>, <code class=\"inline\">u."
        "proverit_finish(...)</code>) и только координирует их. Это типичная для ООП картина: "
        "не один гигантский класс, который умеет всё, а несколько небольших классов, каждый "
        "отвечает за своё, и сотрудничающих через понятные методы друг друга.",
    )}

    {exercise(3, "Таблица результатов", "Добавьте Gonka метод tablitsa_rezultatov(self), возвращающий self.rezultaty в виде пронумерованного текста («1 место: red», «2 место: blue», ...).")}

{local_required_card(
        "14-26",
        "Практика: гонка Turtle v2",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/14-26/index.html",
    )}
    """
    page(
        "14-26-mini-proekt-gonka-v2.html",
        page_title="Мини-проект: гонка Turtle v2",
        description="Класс Gonka, управляющий списком объектов Uchastnik — композиция и сотрудничающие объекты в действии.",
        kicker_suffix="Мини-проект: гонка v2",
        h1="Мини-проект: гонка Turtle v2",
        lede="Гонка сама становится объектом — управляет участниками, а не дублирует их логику.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 14-27 · Итоги главы
# ---------------------------------------------------------------------------

def build_27() -> None:
    body = f"""
    <h2>Инструментарий ООП, который у вас теперь есть</h2>
{capability_map(
        [
            ("Основы", ["class, __init__, self", "атрибуты и методы", "экземпляр vs класс (14.7)"]),
            ("Инкапсуляция", ["_internal, __name", "property и @x.setter"]),
            ("Отношения объектов", ["композиция — HAS-A (14.13)", "наследование — IS-A (14.15)", "super() (14.16)"]),
            ("Гибкость поведения", ["полиморфизм (14.18)", "duck typing (14.19)"]),
            ("Современный Python", ["специальные методы (14.21)", "@dataclass (14.23)"]),
            ("Проектирование", ["класс или не класс? (14.25)"]),
        ],
        title="Итоговая карта главы 14",
    )}

    <h2>Путь, который мы прошли</h2>
{tree_diagram(("Объект = состояние + поведение", [
        ("Класс описывает будущие объекты", [("__init__ настраивает состояние", []), ("self связывает метод с объектом", [])]),
        ("Отношения между объектами", [("Композиция: объект ХРАНИТ объект", []), ("Наследование: объект ЯВЛЯЕТСЯ объектом", [])]),
        ("Гибкость поведения", [("Полиморфизм", []), ("Duck typing", [])]),
    ]), caption="От одного объекта — к моделям из нескольких сотрудничающих классов")}

    {summary_box("Что мы узнали в этой главе", [
        "ООП организует код вокруг <strong>объектов</strong> — состояния и поведения, "
        "собранных вместе.",
        "<code class=\"inline\">class</code> определяет чертёж; <code class=\"inline\">__init__"
        "</code> настраивает состояние уже существующего объекта, а не создаёт его.",
        "<code class=\"inline\">self</code> — не ключевое слово, а объект слева от точки, "
        "подставленный автоматически при связывании метода.",
        "Атрибут экземпляра — свой у каждого объекта; атрибут класса — один на всех, и "
        "изменяемые значения там опасны.",
        "Инкапсуляция и property защищают состояние, не меняя синтаксис снаружи.",
        "Композиция (HAS-A) и наследование (IS-A) — два разных способа связать классы; "
        "выбор между ними определяется реальным отношением понятий, а не удобством.",
        "Полиморфизм и duck typing позволяют коду работать с разными объектами одинаково, не "
        "проверяя их класс явно.",
        "Специальные методы подключают объект к print(), ==, len() и другим встроенным "
        "операциям; @dataclass убирает шаблонный код там, где он не нужен.",
        "Не каждая задача требует класса — это тоже часть проектирования, а не исключение из "
        "правил.",
    ])}

    {callout(
        "tip",
        "Дальше — глава 15: Python и файлы",
        "Все объекты этой главы жили только пока работала программа: закрыли Python — и "
        "<code class=\"inline\">Player</code>, и <code class=\"inline\">Korzina</code> исчезли "
        "вместе с процессом. В следующей главе научимся сохранять данные на диск — в текстовые "
        "файлы и файлы CSV — чтобы состояние переживало перезапуск программы, а не терялось "
        "каждый раз.",
    )}
    """
    page(
        "14-27-itogi-glavy.html",
        page_title="Итоги главы 14",
        description="Итоговая карта инструментов ООП главы 14 и мотивированный переход к главе 15 «Python и файлы».",
        kicker_suffix="Итоги главы",
        h1="Итоги главы",
        lede="От первого объекта — к моделям из нескольких сотрудничающих классов. Собираем всё "
        "воедино.",
        body_html=body,
    )


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
