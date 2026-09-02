#!/usr/bin/env python3
"""Строит Главу 11: «Очень много информации!» (site/chapters/glava-11/).

Curriculum v2: от короткого обзора list/tuple/set/dict до полноценного
курса структур данных Python. Начинаем не со списка методов, а с проблемы
(«нужно хранить сразу много значений») и карты коллекций — только потом
list/tuple/set/dict по отдельности. Mutable vs immutable, references /
aliasing и поверхностное копирование разобраны как отдельная, полноценная
тема (не мимоходом), set-алгебра — через Венн-диаграммы, вложенные
структуры — как деревья, comprehensions — только после обычных циклов,
выбор структуры данных — отдельный навык с decision-map, отдельный урок
отладки коллекций (14 именованных ошибок), и несколько мини-проектов,
включая классический «подсчёт частоты слов».

Существующие маршруты и практики (11-01..11-10, включая оба turtle-проекта
11-05/11-09) сохранены на месте — их страницы и ноутбуки не переименованы и
не лишились ни одной изначальной темы, только дополнены. Новый материал —
новые страницы и новые ID практик (11-11..11-26), без переиспользования
занятых ID.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    branch_diagram,
    callout,
    capability_map,
    classic_vs_modern,
    code_block,
    comparison_table,
    converge_diagram,
    decision_map,
    exercise,
    flow_diagram,
    list_box_diagram,
    list_slice_diagram,
    local_required_card,
    matrix_diagram,
    namespace_diagram,
    practice_card,
    render_chapter_opener,
    render_page,
    shallow_copy_diagram,
    summary_box,
    timeline_diagram,
    tree_diagram,
    venn_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-11"

PAGES = [
    ("index.html", "Обзор главы"),
    ("11-11-zachem-hranit-mnogo.html", "Зачем хранить много значений"),
    ("11-01-spiski-osnovy.html", "Списки: основы"),
    ("11-02-srezy-spiskov.html", "Срезы списков"),
    ("11-12-izmenyaem-spisok.html", "Изменяем список"),
    ("11-13-append-extend-insert.html", "append, extend, insert"),
    ("11-14-remove-pop-clear.html", "remove, pop, clear, del"),
    ("11-03-operacii-so-spiskami.html", "Мощные операции со списками"),
    ("11-15-spiski-i-cikly.html", "Списки и циклы"),
    ("11-16-ssylki-aliasing.html", "Ссылки, aliasing, == и is"),
    ("11-17-kopirovanie-spiskov.html", "Копирование списков"),
    ("11-04-eshche-o-spiskah.html", "Ещё больше о списках"),
    ("11-05-mini-proekt-zvezda.html", "Мини-проект: разноцветная звезда"),
    ("11-06-kortezhi.html", "Кортежи"),
    ("11-18-zip-i-raspakovka.html", "zip() и распаковка"),
    ("11-07-mnozhestva.html", "Множества"),
    ("11-19-mnozhestva-operacii.html", "Операции множеств и хешируемость"),
    ("11-08-slovari.html", "Словари"),
    ("11-20-slovari-metody.html", "Методы словарей"),
    ("11-21-vlozhennye-struktury.html", "Вложенные структуры"),
    ("11-22-preobrazovaniya-i-comprehensions.html", "Преобразования и comprehensions"),
    ("11-09-mini-proekt-cveta.html", "Мини-проект: бесконечные цвета"),
    ("11-23-vybor-struktury.html", "Как выбрать правильную структуру"),
    ("11-24-debugging-kollekcij.html", "Отладка коллекций"),
    ("11-25-slovar-chastoty-slov.html", "Мини-проект: частота слов"),
    ("11-26-mini-proekty-kollekcii.html", "Мини-проекты с коллекциями"),
    ("11-10-mini-proekt-perestanovka-itogi.html", "Перестановка имени и итоги"),
]

PRACTICE_IDS = [
    "11-11", "11-01", "11-02", "11-12", "11-13", "11-14", "11-03", "11-15",
    "11-16", "11-17", "11-04", "11-05", "11-06", "11-18", "11-07", "11-19",
    "11-08", "11-20", "11-21", "11-22", "11-09", "11-23", "11-24", "11-25",
    "11-26", "11-10",
]

LOCAL_REQUIRED_IDS = {"11-05", "11-09"}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 11 · Данные", items),
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


_HREFS = [h for h, _ in PAGES]
_TITLES = dict(PAGES)


def nav_for(current_href: str) -> PageNav:
    i = _HREFS.index(current_href)
    prev_href, prev_label = (_HREFS[i - 1], _TITLES[_HREFS[i - 1]]) if i > 0 else (None, None)
    if i < len(_HREFS) - 1:
        next_href, next_label = _HREFS[i + 1], _TITLES[_HREFS[i + 1]]
    else:
        next_href, next_label = "../glava-12/index.html", "Глава 12: Множество увлекательных мини-проектов"
    return PageNav(prev_href=prev_href, prev_label=prev_label, next_href=next_href, next_label=next_label)


def page(href: str, *, page_title: str, description: str, kicker_suffix: str, h1: str, lede: str, body_html: str) -> None:
    out = render_page(
        page_title=page_title,
        description=description,
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), (kicker_suffix, "")],
        kicker="Глава 11 · Очень много информации!",
        h1=h1,
        lede=lede,
        body_html=body_html,
        sidebar_groups=sidebar(href),
        nav=nav_for(href),
    )
    write(href, out)


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=11,
        description="Списки, кортежи, множества и словари — четыре основных способа хранить сразу "
        "много данных. Не список методов, а разбор того, зачем нужна каждая структура, как они "
        "устроены внутри (ссылки, изменяемость, копирование) и как выбирать между ними.",
        meta_items=["[[icon:timer]] ~6 часов", "[[icon:architecture]] list, tuple, set, dict", "[[icon:practice]] 26 практик"],
        sections=[
            ChapterSectionLink("11.1", "Зачем хранить много значений. Карта коллекций", "11-11-zachem-hranit-mnogo.html"),
            ChapterSectionLink("11.2", "Списки: основы", "11-01-spiski-osnovy.html"),
            ChapterSectionLink("11.3", "Срезы списков", "11-02-srezy-spiskov.html"),
            ChapterSectionLink("11.4", "Изменяем список: mutable vs immutable", "11-12-izmenyaem-spisok.html"),
            ChapterSectionLink("11.5", "append, extend, insert", "11-13-append-extend-insert.html"),
            ChapterSectionLink("11.6", "remove, pop, clear, del", "11-14-remove-pop-clear.html"),
            ChapterSectionLink("11.7", "Мощные операции со списками", "11-03-operacii-so-spiskami.html"),
            ChapterSectionLink("11.8", "Списки и циклы", "11-15-spiski-i-cikly.html"),
            ChapterSectionLink("11.9", "Ссылки, aliasing, == и is", "11-16-ssylki-aliasing.html"),
            ChapterSectionLink("11.10", "Копирование списков и shallow copy", "11-17-kopirovanie-spiskov.html"),
            ChapterSectionLink("11.11", "Ещё больше о списках: вложенные списки", "11-04-eshche-o-spiskah.html"),
            ChapterSectionLink("11.12", "Мини-проект — разноцветная звезда", "11-05-mini-proekt-zvezda.html"),
            ChapterSectionLink("11.13", "Кортежи", "11-06-kortezhi.html"),
            ChapterSectionLink("11.14", "zip() и распаковка", "11-18-zip-i-raspakovka.html"),
            ChapterSectionLink("11.15", "Множества", "11-07-mnozhestva.html"),
            ChapterSectionLink("11.16", "Операции множеств: Венн-диаграммы, хешируемость", "11-19-mnozhestva-operacii.html"),
            ChapterSectionLink("11.17", "Словари", "11-08-slovari.html"),
            ChapterSectionLink("11.18", "Методы словарей", "11-20-slovari-metody.html"),
            ChapterSectionLink("11.19", "Вложенные структуры", "11-21-vlozhennye-struktury.html"),
            ChapterSectionLink("11.20", "Преобразования и comprehensions", "11-22-preobrazovaniya-i-comprehensions.html"),
            ChapterSectionLink("11.21", "Мини-проект — бесконечные цвета", "11-09-mini-proekt-cveta.html"),
            ChapterSectionLink("11.22", "Как выбрать правильную структуру", "11-23-vybor-struktury.html"),
            ChapterSectionLink("11.23", "Отладка коллекций: 14 типичных ошибок", "11-24-debugging-kollekcij.html"),
            ChapterSectionLink("11.24", "Мини-проект — частота слов", "11-25-slovar-chastoty-slov.html"),
            ChapterSectionLink("11.25", "Мини-проекты с коллекциями", "11-26-mini-proekty-kollekcii.html"),
            ChapterSectionLink("11.26", "Мини-проект — перестановка имени и итоги", "11-10-mini-proekt-perestanovka-itogi.html"),
            ChapterSectionLink("", "Итоги главы", "11-10-mini-proekt-perestanovka-itogi.html#itogi"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 11-11 · Зачем хранить много значений. Карта коллекций
# ---------------------------------------------------------------------------

def build_11() -> None:
    five_vars = 'score_1 = 95\nscore_2 = 82\nscore_3 = 91\nscore_4 = 77\nscore_5 = 88\n'
    body = f"""
    <h2>Одна переменная — одно значение. А если их пятьсот?</h2>
    <p>До сих пор каждая переменная хранила одно значение. Представьте, что нужно сохранить оценки
    пяти учеников:</p>
    {code_block("pyat_peremennyh.py", five_vars)}
    <p>Работает. А теперь представьте, что учеников не пять, а <strong>пятьсот</strong>. Заводить
    <code class="inline">score_1</code> … <code class="inline">score_500</code> вручную — не просто
    долго, а по сути невозможно поддерживать: нельзя пройтись по ним циклом, нельзя посчитать
    среднее одной строкой, нельзя добавить оценку 501-го ученика без правки кода.</p>

    <h2>Коллекция: одно имя — много значений</h2>
    <p>Для этого в Python есть <strong>коллекции</strong> — типы данных, которые хранят сразу
    много значений под одним именем:</p>
    {code_block("odin_spisok.py", "scores = [95, 82, 91, 77, 88]\nprint(scores)\n")}
    {branch_diagram(
        "scores (список)",
        [("95", "индекс 0"), ("82", "индекс 1"), ("91", "индекс 2"), ("77", "индекс 3"), ("88", "индекс 4")],
        caption="Одно имя scores указывает на ОДИН объект-коллекцию, который хранит ссылки на пять значений",
    )}
    {callout(
        "info",
        "Коллекция организует ссылки на объекты, а не «складывает предметы в коробку»",
        "Мы уже видели в главе 3, что переменная — это имя, указывающее на объект. Коллекция "
        "устроена похоже: <code class=\"inline\">scores</code> указывает на один объект-список, "
        "а список хранит ссылки на несколько отдельных значений. Подробности внутреннего "
        "устройства CPython нам сейчас не нужны — этой картинки достаточно.",
    )}

    <h2>Карта коллекций Python</h2>
    <p>В Python четыре основных встроенных коллекции. Они делятся на три семейства по тому,
    <strong>как</strong> устроен доступ к значениям:</p>
    {tree_diagram(
        ("МНОГО ЗНАЧЕНИЙ", [
            ("SEQUENCE — по позиции (индексу)", [
                ("list — можно изменять", []),
                ("tuple — изменить нельзя", []),
            ]),
            ("SET — только уникальные значения", [
                ("set — можно изменять", []),
            ]),
            ("MAPPING — по ключу", [
                ("dict — ключ → значение", []),
            ]),
        ]),
        caption="Три семейства коллекций Python: последовательность (по позиции), множество (уникальность), отображение (по ключу)",
    )}
    {capability_map([
        ("list", ["упорядочен", "изменяем", "повторы разрешены", "<code class=\"inline\">[1, 2, 2]</code>"]),
        ("tuple", ["упорядочен", "неизменяем", "повторы разрешены", "<code class=\"inline\">(1, 2, 2)</code>"]),
        ("set", ["без индексов", "изменяем", "только уникальные", "<code class=\"inline\">{1, 2}</code>"]),
        ("dict", ["по ключу", "изменяем", "ключи уникальны", "<code class=\"inline\">{\"a\": 1}</code>"]),
    ], title="Четыре встроенные коллекции — коротко")}

    <h2>Как выбрать? Пока — ориентир, не закон</h2>
    <p>Полный разбор выбора структуры будет в §11.22, но уже сейчас полезно иметь общий ориентир:</p>
    {decision_map([
        ("Нужна пара «ключ → значение»?", "dict"),
        ("Нужны только уникальные значения, порядок не важен?", "set"),
        ("Нужен порядок, и придётся часто менять содержимое?", "list"),
        ("Нужен порядок, но значения фиксированы раз и навсегда?", "tuple"),
    ], title="Какую коллекцию выбрать? (первый ориентир)", caption="Это правило большого пальца, а не математический закон — из него будут исключения")}

    {practice_card(
        "11-11",
        "Практика: превращаем пять переменных в один список",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-11/index.html",
    )}
    """
    page(
        "11-11-zachem-hranit-mnogo.html",
        page_title="Зачем хранить много значений",
        description="Зачем нужны коллекции в Python и карта четырёх встроенных типов: list, tuple, set, dict.",
        kicker_suffix="Зачем хранить много значений",
        h1="Зачем хранить много значений",
        lede="Прежде чем список методов — вопрос «зачем»: одна переменная хранит одно значение, "
        "а коллекция хранит их сразу много под одним именем.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-01 · Списки: основы (расширено)
# ---------------------------------------------------------------------------

def build_01() -> None:
    body = f"""
    <h2>Списки</h2>
    <p><strong>Список</strong> (<code class="inline">list</code>) — упорядоченная коллекция
    значений в квадратных скобках через запятую:</p>
    {code_block("spiski.py", 'fruits = ["яблоко", "банан", "вишня"]\nprint(fruits)\nprint(type(fruits))\n')}
    <p>Список может хранить значения разных типов одновременно, хотя на практике чаще хранят
    значения одного вида — так код проще читать:</p>
    {code_block("smeshannyj_spisok.py", 'smeshannyj = ["Cartesian", 5, 3.14, True]\nprint(smeshannyj)\n')}
    {callout(
        "info",
        "Список любого типа — не ошибка, а выбор",
        "Python не запрещает смешивать типы в одном списке. Но если элементы списка означают "
        "разные вещи (имя, число, флаг), почти всегда понятнее использовать словарь (§11.17) — "
        "список удобнее, когда все элементы одного смысла: имена, оценки, координаты.",
    )}

    <h2>Длина списка: len()</h2>
    <p>Как и у строк (глава 8), у списка есть длина:</p>
    {code_block("dlina_spiska.py", "numbers = [10, 20, 30]\nprint(len(numbers))   # 3\n")}
    {list_box_diagram(["10", "20", "30"], indices=True, caption="len(numbers) = 3 → допустимые индексы: от 0 до len-1 = 2")}

    <h2>Доступ к значениям списка по индексу</h2>
    <p>Как и у строк, у элементов списка есть индексы, начиная с нуля — с тем же правилом
    отрицательных индексов «с конца»:</p>
    {list_box_diagram(['"Anna"', '"Oleg"', '"Maria"', '"Leo"'], indices=True, caption='names = ["Anna", "Oleg", "Maria", "Leo"]')}
    {code_block("dostup_k_spisku.py", 'names = ["Anna", "Oleg", "Maria", "Leo"]\nprint(names[0])    # Anna\nprint(names[-1])   # Leo — последний элемент\n')}

    {practice_card(
        "11-01",
        "Практика: создание списков и доступ по индексу",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-01/index.html",
    )}
    """
    page(
        "11-01-spiski-osnovy.html",
        page_title="Списки: основы",
        description="Введение в списки Python: создание, len(), доступ к элементам по индексу.",
        kicker_suffix="Списки: основы",
        h1="Храним больше одного значения",
        lede="Списки — самая универсальная коллекция Python: упорядоченный набор значений в "
        "одной переменной.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-02 · Срезы списков (расширено)
# ---------------------------------------------------------------------------

def build_02() -> None:
    body = f"""
    <p>Срезы списков работают точно так же, как срезы строк из главы 8: <code class="inline">start</code>
    входит в срез, <code class="inline">stop</code> — нет.</p>
    {list_slice_diagram(["10", "20", "30", "40", "50"], 1, 3, caption="chisla[1:3] → [20, 30] — граница 1 включена, граница 3 нет")}
    {code_block(
        "srezy_spiskov.py",
        'chisla = [10, 20, 30, 40, 50]\n'
        "print(chisla[1:3])    # [20, 30]\n"
        "print(chisla[:2])     # [10, 20]\n"
        "print(chisla[2:])     # [30, 40, 50]\n"
        "print(chisla[::-1])   # [50, 40, 30, 20, 10] — развёрнутый список\n",
    )}
    {two_up(
        list_slice_diagram(["10", "20", "30", "40", "50"], 0, 2, caption="chisla[:2]"),
        list_slice_diagram(["10", "20", "30", "40", "50"], 2, 5, caption="chisla[2:]"),
    )}
    {callout(
        "tip",
        "Срез списка — это новый список",
        "Как и срез строки, срез списка возвращает <strong>новый</strong> список, не изменяя "
        "исходный. Это важно запомнить — пригодится в §11.10 «Копирование списков».",
    )}

    {practice_card(
        "11-02",
        "Практика: срезы списков",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-02/index.html",
    )}
    """
    page(
        "11-02-srezy-spiskov.html",
        page_title="Делаем срез списка!",
        description="Срезы списков в Python — та же логика, что и срезы строк.",
        kicker_suffix="Срезы списков",
        h1="Делаем срез списка!",
        lede="Срезы списков работают точно так же, как срезы строк, — уже знакомая логика в "
        "новом контексте.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-12 · Изменяем список: mutable vs immutable
# ---------------------------------------------------------------------------

def build_12() -> None:
    body = f"""
    <h2>Список можно изменить «на месте»</h2>
    <p>Это фундаментальное отличие списка от строки. Присвоим новое значение элементу по индексу:</p>
    {code_block("izmenenie_elementa.py", 'numbers = [10, 20, 30]\nnumbers[1] = 999\nprint(numbers)   # [10, 999, 30]\n')}
    {two_up(
        list_box_diagram(["10", "20", "30"], caption="До: numbers[1] ещё 20"),
        list_box_diagram(["10", "999", "30"], highlight=[1], caption="После: numbers[1] = 999 — тот же объект"),
    )}
    {callout(
        "info",
        "Это тот же самый объект, а не новый список",
        "После <code class=\"inline\">numbers[1] = 999</code> список не пересоздаётся — "
        "изменяется содержимое того же объекта. Это станет важно в §11.9, когда у одного списка "
        "будет две ссылки-переменные сразу.",
    )}

    <h2>Mutable vs immutable</h2>
    <p>Мы уже встречали неизменяемые типы — числа и строки. Список — первый по-настоящему
    <strong>изменяемый (mutable)</strong> тип, который мы изучаем:</p>
    {comparison_table(
        ["Тип", "Можно ли заменить часть значения «на месте»?"],
        [
            ["<code class=\"inline\">str</code>", "Нет — <code class=\"inline\">name[0] = \"P\"</code> вызывает TypeError, нужна новая строка"],
            ["<code class=\"inline\">tuple</code>", "Нет — кортежи тоже неизменяемы (§11.13)"],
            ["<code class=\"inline\">list</code>", "Да — <code class=\"inline\">numbers[1] = 999</code> меняет тот же объект"],
        ],
    )}
    {callout(
        "warning",
        "Изменяемость — свойство типа, а не конкретного значения",
        "Не бывает «изменяемых строк» и «неизменяемых списков» в зависимости от содержимого — "
        "изменяемость целиком определяется <strong>типом</strong> объекта: все "
        "<code class=\"inline\">list</code> изменяемы, все <code class=\"inline\">tuple</code> и "
        "<code class=\"inline\">str</code> — нет.",
    )}

    {practice_card(
        "11-12",
        "Практика: изменяем элемент списка на месте",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-12/index.html",
    )}
    """
    page(
        "11-12-izmenyaem-spisok.html",
        page_title="Изменяем список",
        description="Списки изменяемы (mutable) — в отличие от строк и кортежей. Сравнение mutable vs immutable.",
        kicker_suffix="Изменяем список",
        h1="Изменяем список",
        lede="Первый по-настоящему изменяемый тип данных: элемент списка можно заменить, не "
        "создавая новый объект.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-13 · append, extend, insert
# ---------------------------------------------------------------------------

def build_13() -> None:
    body = f"""
    <h2>append() — добавить один элемент</h2>
    {two_up(
        list_box_diagram(["1", "2"], caption="До: numbers.append(3)"),
        list_box_diagram(["1", "2", "3"], highlight=[2], caption="После: [1, 2, 3]"),
    )}
    {code_block("append.py", "numbers = [1, 2]\nnumbers.append(3)\nprint(numbers)   # [1, 2, 3]\n")}
    <p><code class="inline">append()</code> всегда добавляет <strong>ровно один</strong> новый
    элемент — даже если этот элемент сам является списком.</p>

    <h2>append() vs extend() — важная ловушка</h2>
    {code_block(
        "append_vs_extend.py",
        'a = [1, 2]\n'
        'a.append([3, 4])\n'
        "print(a)   # [1, 2, [3, 4]] — список внутри списка!\n\n"
        'b = [1, 2]\n'
        'b.extend([3, 4])\n'
        "print(b)   # [1, 2, 3, 4]\n",
    )}
    {two_up(
        list_box_diagram(["1", "2", "[3, 4]"], highlight=[2], caption="append([3, 4]) → один НОВЫЙ элемент-список"),
        list_box_diagram(["1", "2", "3", "4"], highlight=[2, 3], caption="extend([3, 4]) → два элемента ИЗ списка"),
    )}
    {callout(
        "warning",
        "append() добавляет один объект, extend() — элементы из итерируемого",
        "<code class=\"inline\">append(x)</code> кладёт <code class=\"inline\">x</code> внутрь "
        "как ОДИН новый элемент, каким бы он ни был. <code class=\"inline\">extend(iterable)</code> "
        "разворачивает переданный список (или любой другой итерируемый объект) и добавляет "
        "каждый его элемент по отдельности. Перепутать их — классическая ошибка новичка.",
    )}

    <h2>insert() — вставить по индексу</h2>
    {code_block("insert.py", 'fruits = ["яблоко", "банан", "вишня"]\nfruits.insert(1, "манго")\nprint(fruits)   # ["яблоко", "манго", "банан", "вишня"]\n')}
    {two_up(
        list_box_diagram(['"яблоко"', '"банан"', '"вишня"'], caption="До: insert(1, 'манго')"),
        list_box_diagram(['"яблоко"', '"манго"', '"банан"', '"вишня"'], highlight=[1], caption="После: остальные элементы сдвинулись вправо"),
    )}
    <p>Элементы начиная с указанного индекса как будто «раздвигаются», освобождая место для нового
    значения — а их индексы после вставки увеличиваются на единицу.</p>

    {practice_card(
        "11-13",
        "Практика: append, extend, insert",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-13/index.html",
    )}
    """
    page(
        "11-13-append-extend-insert.html",
        page_title="append, extend, insert",
        description="Добавление элементов в список: append() добавляет один объект, extend() — элементы из итерируемого, insert() — по индексу.",
        kicker_suffix="append, extend, insert",
        h1="append, extend, insert",
        lede="Три способа добавить что-то в список — и одна из самых частых ловушек новичка: "
        "append() и extend() делают совсем разные вещи.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-14 · remove, pop, clear, del
# ---------------------------------------------------------------------------

def build_14() -> None:
    body = f"""
    <h2>remove() — удалить по значению</h2>
    {code_block("remove.py", 'names = ["Anna", "Oleg", "Maria"]\nnames.remove("Oleg")\nprint(names)   # ["Anna", "Maria"]\n')}

    <h2>pop() — удалить по позиции и вернуть значение</h2>
    {code_block("pop.py", 'names = ["Anna", "Oleg", "Maria"]\nremoved = names.pop(1)\nprint(names, removed)   # ["Anna", "Maria"] Oleg\n')}
    {comparison_table(
        ["", "remove(value)", "pop(index)"],
        [
            ["Удаляет по", "значению", "позиции (индексу)"],
            ["Что возвращает", "ничего (<code class=\"inline\">None</code>)", "удалённое значение"],
            ["Если аргумент не подходит", "<code class=\"inline\">ValueError</code>, если значения нет", "<code class=\"inline\">IndexError</code>, если индекса нет"],
        ],
    )}
    {callout(
        "tip",
        "pop() без аргумента — удаляет последний элемент",
        "<code class=\"inline\">names.pop()</code> без индекса убирает и возвращает "
        "<strong>последний</strong> элемент списка. Это пригодится, если использовать список как "
        "стек — подробнее о стеках будет в следующих главах.",
    )}

    <h2>clear() и del — два разных способа «опустошить»</h2>
    {code_block(
        "clear_del.py",
        'items = [1, 2, 3]\n'
        "items.clear()\n"
        "print(items)      # [] — тот же список, но пустой\n\n"
        'other = [1, 2, 3]\n'
        "del other[1]\n"
        "print(other)       # [1, 3] — удалили один элемент по индексу\n\n"
        'third = [1, 2, 3]\n'
        "del third           # удалили саму переменную\n",
    )}
    {comparison_table(
        ["Команда", "Что происходит"],
        [
            ["<code class=\"inline\">items.clear()</code>", "тот же объект-список остаётся, но становится пустым"],
            ["<code class=\"inline\">del items[i]</code>", "удаляет элемент с индексом i (сам список остаётся)"],
            ["<code class=\"inline\">del items</code>", "удаляет саму переменную-имя (глава 3) — после этого <code class=\"inline\">items</code> не существует"],
        ],
    )}
    {callout(
        "warning",
        "После del items имя items больше не существует",
        "<code class=\"inline\">print(items)</code> после <code class=\"inline\">del items</code> "
        "вызовет <code class=\"inline\">NameError</code> — это то же самое поведение "
        "<code class=\"inline\">del</code>, что мы видели в главе 3 для обычных переменных, "
        "только теперь применённое к списку.",
    )}

    {practice_card(
        "11-14",
        "Практика: remove, pop, clear, del",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-14/index.html",
    )}
    """
    page(
        "11-14-remove-pop-clear.html",
        page_title="remove, pop, clear, del",
        description="Удаление элементов списка: remove() по значению, pop() по индексу с возвратом, clear() и del.",
        kicker_suffix="remove, pop, clear",
        h1="remove, pop, clear, del",
        lede="Четыре способа что-то убрать из списка — у каждого своя роль, и путать их не стоит.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-03 · Мощные операции со списками (расширено: sort()/sorted(), поиск)
# ---------------------------------------------------------------------------

def build_03() -> None:
    body = f"""
    <p>У списков (в отличие от строк) есть методы, которые <strong>изменяют сам список</strong>
    — списки, в отличие от строк, изменяемы (§11.4).</p>

    <h2>Копирование и добавление</h2>
    {code_block("kopirovanie.py", 'original = [1, 2, 3]\nkopiya = original.copy()\nkopiya.append(4)\nprint(original)  # [1, 2, 3] — не изменился\nprint(kopiya)    # [1, 2, 3, 4]\n')}
    {callout(
        "warning",
        "kopiya = original — это не копия!",
        "<code class=\"inline\">kopiya = original</code> создаёт вторую переменную, "
        "указывающую <strong>на тот же самый</strong> список — изменение через одну переменную "
        "видно и через другую. Это называется <strong>aliasing</strong> — подробно разберём в "
        "§11.9. Чтобы получить настоящую независимую копию, нужен "
        "<code class=\"inline\">.copy()</code> (или срез <code class=\"inline\">original[:]</code>) "
        "— подробности и важный нюанс с вложенными списками в §11.10.",
    )}

    <h2>Подсчёт и очистка</h2>
    {code_block("podschet.py", 'chisla = [1, 2, 2, 3, 2]\nprint(chisla.count(2))   # 3 — сколько раз встречается 2\nchisla.clear()\nprint(chisla)             # [] — список пуст\n')}

    <h2>Конкатенация</h2>
    {code_block("konkatenaciya_spiskov.py", 'a = [1, 2]\nb = [3, 4]\nprint(a + b)   # [1, 2, 3, 4]\n')}

    <h2>Поиск и проверка наличия: in, index(), count()</h2>
    {code_block("poisk.py", 'fruits = ["яблоко", "банан", "вишня"]\nprint("банан" in fruits)         # True\nprint(fruits.index("вишня"))      # 2 — индекс элемента\n')}
    <p>Проверка <code class="inline">in</code> — то же логическое выражение из главы 9, только
    теперь слева не число, а коллекция:</p>
    {code_block("membership_primer.py", 'allowed_users = ["anna", "oleg", "maria"]\nusername = "oleg"\nif username in allowed_users:\n    print("Доступ разрешён")\n')}
    {callout(
        "warning",
        "index() вызывает ValueError, если значения нет",
        "Безопасный порядок — сначала проверить <code class=\"inline\">in</code>, потом искать "
        "индекс: <code class=\"inline\">if value in items: position = items.index(value)</code>.",
    )}

    <h2>Добавление и удаление элементов</h2>
    <p>Коротко — подробный разбор с визуальными диаграммами в §11.5 и §11.6:</p>
    {code_block(
        "dobavlenie_udalenie.py",
        'fruits = ["яблоко", "банан"]\n'
        'fruits.append("вишня")        # добавить в конец\n'
        'fruits.insert(0, "манго")     # вставить по индексу\n'
        "print(fruits)\n\n"
        'fruits.remove("банан")        # удалить по значению\n'
        "last = fruits.pop()            # удалить и вернуть последний элемент\n"
        "print(fruits, last)\n",
    )}

    <h2>sort() мутирует и возвращает None — классическая ловушка</h2>
    {code_block("razvorot_sortirovka.py", 'chisla = [3, 1, 4, 1, 5]\nchisla.sort()\nprint(chisla)      # [1, 1, 3, 4, 5]\nchisla.reverse()\nprint(chisla)      # [5, 4, 3, 1, 1]\n')}
    {code_block(
        "sort_none_lovushka.py",
        "chisla = [3, 1, 2]\n"
        "chisla = chisla.sort()\n"
        "print(chisla)   # None — а не отсортированный список!\n",
    )}
    {callout(
        "warning",
        "Никогда не пишите x = x.sort()",
        "<code class=\"inline\">.sort()</code> сортирует список <strong>на месте</strong> и "
        "возвращает <code class=\"inline\">None</code> — это распространённый способ Python "
        "показать «я изменил объект, а не создал новый» (тот же принцип, что и у "
        "<code class=\"inline\">.append()</code>). Присваивание результата обратно в переменную "
        "стирает список, заменяя его на <code class=\"inline\">None</code>.",
    )}

    <h2>sorted() — та же задача, но без мутации</h2>
    {comparison_table(
        ["", "list.sort()", "sorted(list)"],
        [
            ["Изменяет исходный список?", "Да — мутирует", "Нет — не трогает"],
            ["Что возвращает?", "<code class=\"inline\">None</code>", "новый отсортированный список"],
        ],
    )}
    {code_block(
        "sorted_primer.py",
        "chisla = [3, 1, 4, 1, 5]\n"
        "novyj = sorted(chisla)\n"
        "print(chisla)   # [3, 1, 4, 1, 5] — не изменился\n"
        "print(novyj)     # [1, 1, 3, 4, 5]\n",
    )}
    <p><code class="inline">sorted()</code> умеет и <code class="inline">key</code> — по какому
    свойству сравнивать элементы:</p>
    {code_block(
        "sorted_key.py",
        'names = ["Bob", "Alexandra", "Li"]\n'
        "print(sorted(names, key=len))   # ['Li', 'Bob', 'Alexandra']\n",
    )}

    {practice_card(
        "11-03",
        "Практика: операции со списками",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-03/index.html",
    )}
    """
    page(
        "11-03-operacii-so-spiskami.html",
        page_title="Мощные операции со списками!",
        description="Методы списков: copy, count, clear, конкатенация, поиск, sort/sorted, key=len.",
        kicker_suffix="Операции со списками",
        h1="Мощные операции со списками!",
        lede="Списки изменяемы — у них есть целый набор методов для добавления, удаления, "
        "поиска и сортировки.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-15 · Списки и циклы
# ---------------------------------------------------------------------------

def build_15() -> None:
    body = f"""
    <h2>Перебор списка циклом for</h2>
    <p>Глава 10 наконец окупается — перебирать список циклом можно, обращаясь сразу к значениям,
    без ручной работы с индексами:</p>
    {code_block("perebor_spiska.py", 'fruits = ["яблоко", "банан", "вишня"]\nfor fruit in fruits:\n    print(fruit)\n')}
    {flow_diagram([
        ("fruits", "['яблоко', 'банан', 'вишня']"),
        ("следующий элемент", "берётся по очереди"),
        ("тело цикла", "print(fruit)"),
    ], caption="for в цикле сам достаёт следующий элемент — вручную считать индексы не нужно")}

    <h2>enumerate() — когда нужен и индекс, и значение</h2>
    {code_block(
        "enumerate_spiski.py",
        'names = ["Anna", "Oleg", "Maria"]\n'
        "for index, name in enumerate(names):\n"
        '    print(index, name)\n',
    )}
    {comparison_table(
        ["index", "name"],
        [["0", "Anna"], ["1", "Oleg"], ["2", "Maria"]],
    )}

    <h2>Коллекция + цикл + условие</h2>
    <p>Один из самых частых паттернов в программировании — пройтись по коллекции и что-то сделать
    только с подходящими значениями:</p>
    {code_block(
        "spisok_cikl_uslovie.py",
        "scores = [95, 82, 91, 58, 77]\n"
        "for score in scores:\n"
        "    if score >= 90:\n"
        '        print(score, "— отлично!")\n',
    )}
    {callout(
        "tip",
        "Коллекция + цикл + условие — фундаментальная связка",
        "Этот паттерн — «перебрать коллекцию и отфильтровать по условию» — встретится ещё "
        "десятки раз: поиск (§11.19), фильтрация, подсчёт частоты слов (§11.24). Он объединяет "
        "главу 9 (условия) и главу 10 (циклы) с этой главой (коллекции).",
    )}

    {practice_card(
        "11-15",
        "Практика: списки, enumerate() и фильтрация циклом",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-15/index.html",
    )}
    """
    page(
        "11-15-spiski-i-cikly.html",
        page_title="Списки и циклы",
        description="Перебор списков циклом for, enumerate() для индекса и значения одновременно, паттерн коллекция+цикл+условие.",
        kicker_suffix="Списки и циклы",
        h1="Списки и циклы",
        lede="Глава 10 наконец окупается: перебираем список циклом, вместо ручной работы с "
        "индексами.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-16 · Ссылки, aliasing, == и is
# ---------------------------------------------------------------------------

def build_16() -> None:
    body = f"""
    <h2>Aliasing: два имени — один и тот же объект</h2>
    <p>В §11.7 мы уже видели предупреждение: <code class="inline">b = a</code> не создаёт копию
    списка. Разберём подробно, что происходит на самом деле.</p>
    {code_block("aliasing.py", "a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)   # [1, 2, 3, 4] — тоже изменился!\nprint(b)   # [1, 2, 3, 4]\n")}
    {converge_diagram(["a", "b"], "[1, 2, 3, 4]", caption="a и b — это ДВА ИМЕНИ одного и того же объекта-списка, а не два списка")}
    {callout(
        "warning",
        "Мы не создали второй список — мы создали второе имя",
        "<code class=\"inline\">b = a</code> не копирует данные. Python просто говорит: "
        "«теперь имя <code class=\"inline\">b</code> указывает туда же, куда и "
        "<code class=\"inline\">a</code>». Формальный термин для этого — "
        "<strong>aliasing</strong> (совместная ссылка). Изменение через любое из двух имён "
        "видно через оба, потому что список-объект на самом деле один.",
    )}

    <h2>== сравнивает содержимое, is — сравнивает объект</h2>
    <p>Отличная возможность закрепить материал главы 9 на новом материале:</p>
    {code_block(
        "eq_vs_is.py",
        "a = [1, 2, 3]\n"
        "b = [1, 2, 3]\n"
        "print(a == b)   # True — содержимое одинаковое\n"
        "print(a is b)   # False — это два РАЗНЫХ объекта\n\n"
        "c = a\n"
        "print(a is c)   # True — c это то же самое имя-alias для a\n",
    )}
    {namespace_diagram(
        [("a", "[1, 2, 3]"), ("b", "[1, 2, 3]")],
        caption="a и b — два разных объекта с одинаковым содержимым: a == b, но не a is b",
    )}
    {comparison_table(
        ["Оператор", "Что проверяет", "a = [1,2,3]; b = [1,2,3]"],
        [
            ["<code class=\"inline\">==</code>", "одинаковое ли содержимое", "<code class=\"inline\">True</code>"],
            ["<code class=\"inline\">is</code>", "один ли и тот же объект в памяти", "<code class=\"inline\">False</code>"],
        ],
    )}

    {exercise(2, "Предсказать результат", "Дано: <code class=\"inline\">x = [10, 20]</code>, "
    "<code class=\"inline\">y = x</code>, <code class=\"inline\">y.append(30)</code>. "
    "Не запуская код, ответьте: чему равен <code class=\"inline\">x</code>? А если бы вместо "
    "<code class=\"inline\">y = x</code> было <code class=\"inline\">y = x.copy()</code>?")}

    {practice_card(
        "11-16",
        "Практика: aliasing, == и is",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-16/index.html",
    )}
    """
    page(
        "11-16-ssylki-aliasing.html",
        page_title="Ссылки, aliasing, == и is",
        description="Почему b = a не копирует список: aliasing (совместная ссылка), разница между == и is для коллекций.",
        kicker_suffix="Ссылки и aliasing",
        h1="Ссылки, aliasing, == и is",
        lede="Два имени могут указывать на один и тот же список — и это не баг, а фундаментальная "
        "особенность того, как Python работает с изменяемыми объектами.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-17 · Копирование списков и shallow copy
# ---------------------------------------------------------------------------

def build_17() -> None:
    body = f"""
    <h2>Три безопасных способа скопировать список</h2>
    {code_block(
        "sposoby_kopirovaniya.py",
        "original = [1, 2, 3]\n\n"
        "kopiya_1 = original.copy()\n"
        "kopiya_2 = list(original)\n"
        "kopiya_3 = original[:]\n\n"
        "kopiya_1.append(4)\n"
        "print(original)   # [1, 2, 3] — не изменился\n"
        "print(kopiya_1)   # [1, 2, 3, 4]\n",
    )}
    <p>Все три способа создают новый ВНЕШНИЙ список. Но что, если элементы сами являются
    списками?</p>

    <h2>Поверхностная копия (shallow copy) — важный нюанс</h2>
    {code_block(
        "shallow_copy_trap.py",
        'original = [["Anna", 10], ["Bob", 20]]\n'
        "kopiya = original.copy()\n\n"
        'kopiya[0][1] = 999\n'
        "print(original)   # [['Anna', 999], ['Bob', 20]] — тоже изменился!\n",
    )}
    {shallow_copy_diagram(
        "original",
        "kopiya = original.copy()",
        ['["Anna", 10]', '["Bob", 20]'],
        caption="Два РАЗНЫХ внешних списка, но их элементы — ОДНИ И ТЕ ЖЕ внутренние списки",
    )}
    {callout(
        "warning",
        ".copy() копирует только один уровень вложенности",
        "<code class=\"inline\">.copy()</code> (и <code class=\"inline\">list(...)</code>, и "
        "срез <code class=\"inline\">[:]</code>) создают новый внешний список, но "
        "<strong>не</strong> копируют вложенные списки внутри него — они остаются общими. Это и "
        "называется <strong>поверхностной копией (shallow copy)</strong>. Изменение вложенного "
        "списка через копию видно и в оригинале.",
    )}

    <h2>copy.deepcopy() — когда нужна полностью независимая копия</h2>
    {code_block(
        "deepcopy.py",
        "import copy\n\n"
        'original = [["Anna", 10], ["Bob", 20]]\n'
        "polnaya_kopiya = copy.deepcopy(original)\n"
        "polnaya_kopiya[0][1] = 999\n"
        "print(original)   # [['Anna', 10], ['Bob', 20]] — не изменился\n",
    )}
    {callout(
        "info",
        "deepcopy — не всегда правильный ответ по умолчанию",
        "<code class=\"inline\">copy.deepcopy()</code> рекурсивно пытается скопировать всю "
        "вложенную структуру целиком. Это решает проблему выше, но для больших или сложных "
        "структур глубокое копирование может быть заметно медленнее и не всегда нужно — часто "
        "достаточно скопировать только тот уровень, который реально будет меняться.",
    )}

    {practice_card(
        "11-17",
        "Практика: копирование списков и поверхностная копия",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-17/index.html",
    )}
    """
    page(
        "11-17-kopirovanie-spiskov.html",
        page_title="Копирование списков",
        description="copy(), list(), срез [:] для копирования списков; поверхностная копия (shallow copy) и ловушка с вложенными списками; copy.deepcopy().",
        kicker_suffix="Копирование списков",
        h1="Копирование списков",
        lede="Скопировать внешний список легко — а вот вложенные списки внутри него по "
        "умолчанию остаются общими. Разберём, почему и что с этим делать.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-04 · Ещё больше о списках (расширено: матрица, ловушка умножения)
# ---------------------------------------------------------------------------

def build_04() -> None:
    cvm = classic_vs_modern(
        "Построение списка: цикл с append() → генератор списков",
        "Классический подход",
        "kvadraty = []\n"
        "for n in range(1, 6):\n"
        "    kvadraty.append(n ** 2)\n"
        "print(kvadraty)",
        "Современный Python (list comprehension)",
        "kvadraty = [n ** 2 for n in range(1, 6)]\n"
        "print(kvadraty)",
        "list comprehension (генератор списков) для простых случаев — он существует в Python "
        "с версии 2.0, так что это не вопрос новизны, а вопрос стиля: короче и, при некоторой "
        "практике, читается как одно предложение («квадрат n для каждого n из диапазона»). Для "
        "более сложной логики (с несколькими условиями или побочными эффектами) цикл с "
        "<code class=\"inline\">append()</code> часто остаётся понятнее — это не всегда "
        "\"хуже\", выбирайте то, что легче прочитать. Подробный разбор comprehensions — в §11.20.",
    )

    body = f"""
    <p>Ещё несколько приёмов, которые часто пригождаются при работе со списками.</p>

    <h2>len(), min(), max(), sum()</h2>
    {code_block("vstroennye_funkcii.py", "chisla = [4, 8, 15, 16, 23, 42]\nprint(len(chisla))   # 6 — количество элементов\nprint(min(chisla))   # 4\nprint(max(chisla))   # 42\nprint(sum(chisla))   # 108\n")}

    <h2>Списки списков (вложенные списки) — матрица</h2>
    <p>Элементом списка может быть другой список — так получаются таблицы (матрицы):</p>
    {code_block("vlozhennye_spiski.py", "matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nprint(matrix[0])      # [1, 2, 3] — первая строка\nprint(matrix[0][1])   # 2 — второй элемент первой строки\nprint(matrix[1][2])   # 6 — строка 1, столбец 2\n")}
    {matrix_diagram(
        [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]],
        row_labels=["строка 0", "строка 1", "строка 2"],
        col_labels=["столбец 0", "столбец 1", "столбец 2"],
        highlight=(1, 2),
        caption="matrix[1][2] → 6 — сначала строка, потом столбец",
    )}
    {code_block(
        "perebor_matricy.py",
        "for row in matrix:\n"
        "    for value in row:\n"
        "        print(value, end=' ')\n"
        "    print()\n",
    )}
    {callout(
        "tip",
        "Вложенный список + вложенный цикл — прямой перенос из главы 10",
        "Внешний цикл идёт по строкам, внутренний — по значениям внутри строки. Это ровно тот же "
        "паттерн вложенных циклов, что и таблица умножения в главе 10, только теперь данные уже "
        "готовы в виде матрицы, а не вычисляются на лету.",
    )}

    <h2>Ловушка: [[0] * 3] * 3</h2>
    <p>Хочется создать сетку 3×3 из нулей одной строкой — но это частая и коварная ошибка:</p>
    {code_block(
        "lovushka_umnozheniya.py",
        "grid = [[0] * 3] * 3\n"
        "grid[0][0] = 1\n"
        "print(grid)   # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] — изменились ВСЕ строки!\n",
    )}
    {converge_diagram(["grid[0]", "grid[1]", "grid[2]"], "[0, 0, 0]", caption="[[0]*3]*3 создаёт ОДИН внутренний список и трижды копирует на него ссылку")}
    {callout(
        "warning",
        "*3 повторяет ссылку, а не создаёт три независимых списка",
        "<code class=\"inline\">[значение] * n</code> для неизменяемых значений (чисел, строк) "
        "работает безопасно. Но когда <code class=\"inline\">значение</code> само является "
        "списком, <code class=\"inline\">* n</code> просто копирует ссылку на один и тот же "
        "внутренний список n раз — ровно тот же принцип aliasing из §11.9. Правильный способ "
        "создать три НЕЗАВИСИМЫЕ строки — через comprehension:",
    )}
    {code_block("pravilnaya_setka.py", "grid = [[0] * 3 for _ in range(3)]\ngrid[0][0] = 1\nprint(grid)   # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] — только первая строка\n")}

    <h2>Перебор списка циклом for</h2>
    {code_block("perebor_spiska_v4.py", 'fruits = ["яблоко", "банан", "вишня"]\nfor fruit in fruits:\n    print(fruit)\n')}

    {cvm}

    {practice_card(
        "11-04",
        "Практика: len/min/max/sum, вложенные списки, list comprehension",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-04/index.html",
    )}
    """
    page(
        "11-04-eshche-o-spiskah.html",
        page_title="Ещё больше интересного со списками!",
        description="len, min, max, sum, вложенные списки (матрицы), ловушка [[0]*3]*3 и генераторы списков (list comprehension).",
        kicker_suffix="Ещё о списках",
        h1="Ещё больше интересного со списками!",
        lede="Полезные встроенные функции, вложенные списки, известная ловушка с умножением "
        "вложенного списка — и более компактный способ строить новые списки.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-05 · Мини-проект — разноцветная звезда (без изменений, только навигация)
# ---------------------------------------------------------------------------

def build_05() -> None:
    body = f"""
    <p>Соединим списки с Turtle (главы 6–7): нарисуем звезду, где каждый луч — своего цвета из
    заранее заданного списка.</p>
    {code_block(
        "raznocvetnaya_zvezda.py",
        'cveta = ["red", "orange", "yellow", "green", "blue"]\n\n'
        "for cvet in cveta:\n"
        "    artist.pencolor(cvet)\n"
        "    artist.forward(150)\n"
        "    artist.right(144)  # угол пятиконечной звезды из главы 6\n",
    )}
    {callout(
        "tip",
        "Список любой длины — тот же код",
        "Добавьте в <code class=\"inline\">cveta</code> ещё пару значений — цикл "
        "<code class=\"inline\">for cvet in cveta</code> сам подстроится под новую длину "
        "списка, без изменений остального кода.",
    )}
    {exercise(2, "Случайные цвета", "Замените список фиксированных цветов на random.choice() из списка — чтобы цвет каждого луча выбирался случайно.")}

    {local_required_card(
        "11-05",
        "Практика: разноцветная звезда (списки + Turtle)",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/11-05/index.html",
    )}
    """
    page(
        "11-05-mini-proekt-zvezda.html",
        page_title="Мини-проект — автоматическая разноцветная звезда",
        description="Комбинируем списки с Turtle: звезда, где каждый луч своего цвета.",
        kicker_suffix="Разноцветная звезда",
        h1="Мини-проект — автоматическая разноцветная звезда",
        lede="Список цветов + цикл + Turtle — звезда, где каждый луч своего цвета.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-06 · Кортежи (расширено: одиночный кортеж, packing/unpacking, star, swap)
# ---------------------------------------------------------------------------

def build_06() -> None:
    body = f"""
    <p><strong>Кортеж</strong> (<code class="inline">tuple</code>) — не «список в круглых
    скобках», а отдельная идея: иногда несколько значений логически образуют ОДНУ запись
    (координата, RGB-цвет), и хочется быть уверенным, что её случайно не изменят.</p>
    {code_block("kortezhi.py", 'point = (10, 20)\nprint(point)\nprint(point[0])   # 10 — индексация работает как у списков\n')}
    {code_block("kortezh_nelzya_menyat.py", "point = (10, 20)\npoint[0] = 99   # TypeError: 'tuple' object does not support item assignment\n")}

    <h2>Кортеж — последовательность, как и список</h2>
    <p><code class="inline">len</code>, индексация, срезы, перебор, <code class="inline">in</code>
    — всё это работает у кортежа так же, как у списка (§11.1–§11.2). Разница только одна, но
    принципиальная: кортеж нельзя изменить.</p>
    {comparison_table(
        ["", "list", "tuple"],
        [
            ["Синтаксис", "<code class=\"inline\">[1, 2, 3]</code>", "<code class=\"inline\">(1, 2, 3)</code>"],
            ["Изменяем?", "да", "нет"],
            ["Индексация, срезы, len, in", "да", "да"],
        ],
    )}

    <h2>Кортеж из одного элемента — нужна запятая</h2>
    {code_block("odinochnyj_kortezh.py", "not_a_tuple = (42)\nprint(type(not_a_tuple))   # <class 'int'>\n\none = (42,)\nprint(type(one))            # <class 'tuple'>\n")}
    {callout(
        "warning",
        "Кортеж создаёт запятая, а не круглые скобки",
        "<code class=\"inline\">(42)</code> — это просто число 42 в скобках, как в математике. "
        "Кортежем его делает запятая: <code class=\"inline\">(42,)</code>. Без запятой Python не "
        "поймёт, что вы хотели кортеж, и тихо создаст обычное число — без ошибки, что особенно "
        "коварно.",
    )}

    <h2>Packing и unpacking</h2>
    {code_block("packing.py", "point = 10, 20   # скобки необязательны — Python «упаковывает» в кортеж сам\nprint(point, type(point))\n")}
    {code_block("raspakovka.py", "point = (10, 20)\nx, y = point\nprint(x, y)   # 10 20\n")}
    {branch_diagram("point = (10, 20)", [("x", "10"), ("y", "20")], caption="x, y = point — распаковка: число имён должно совпадать с числом значений")}
    {callout(
        "tip",
        "Мы уже пользовались распаковкой",
        "<code class=\"inline\">artist.position()</code> в модуле turtle возвращает именно "
        "такой кортеж <code class=\"inline\">(x, y)</code> — можно сразу распаковать его в две "
        "переменные.",
    )}

    <h2>Классический трюк: обмен значений</h2>
    {code_block("swap.py", "a = 1\nb = 2\na, b = b, a\nprint(a, b)   # 2 1\n")}
    <p>Работает благодаря той же паре «packing + unpacking»: справа сначала упаковывается кортеж
    <code class="inline">(b, a)</code>, потом он распаковывается в <code class="inline">a, b</code>
    — без промежуточной переменной.</p>

    <h2>Звёздочная распаковка</h2>
    {code_block("star_unpacking.py", "first, *middle, last = [1, 2, 3, 4, 5]\nprint(first)    # 1\nprint(middle)   # [2, 3, 4]\nprint(last)     # 5\n")}
    {callout(
        "info",
        "Звёздочка собирает «всё остальное» в список",
        "<code class=\"inline\">*middle</code> забирает все значения, не разобранные другими "
        "именами, и упаковывает их в обычный список — даже если распаковывается кортеж.",
    )}

    <h2>Функции могут возвращать несколько значений сразу</h2>
    {code_block("divmod_primer.py", "quotient, remainder = divmod(17, 5)\nprint(quotient, remainder)   # 3 2\n")}
    <p><code class="inline">divmod()</code> из главы 4 на самом деле возвращает один кортеж
    <code class="inline">(3, 2)</code> — просто мы сразу распаковываем его в две переменные.</p>

    <h2>Нюанс: кортеж может содержать изменяемые объекты</h2>
    {code_block(
        "tuple_s_listom.py",
        "t = ([1, 2], [3, 4])\n"
        "t[0].append(99)\n"
        "print(t)   # ([1, 2, 99], [3, 4]) — сработало!\n",
    )}
    {callout(
        "warning",
        "Неизменяемость кортежа — только про сами «ячейки»",
        "<code class=\"inline\">t[0] = [...]</code> (заменить ссылку на другой список) — "
        "запрещено. А вот <code class=\"inline\">t[0].append(99)</code> (изменить сам список, "
        "на который кортеж ссылается) — разрешено: кортеж не даёт переставить, ЧТО он "
        "хранит по каждой позиции, но не запрещает изменяемым объектам внутри меняться.",
    )}

    {practice_card(
        "11-06",
        "Практика: кортежи и распаковка",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-06/index.html",
    )}
    """
    page(
        "11-06-kortezhi.html",
        page_title="Кортежи",
        description="Кортежи (tuple) — неизменяемые последовательности: единственный элемент, packing/unpacking, star-unpacking, swap, кортеж с изменяемым содержимым.",
        kicker_suffix="Кортежи",
        h1="Кортежи",
        lede="Почти список, но неизменяемый — и именно поэтому иногда более подходящий выбор.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-18 · zip() и распаковка
# ---------------------------------------------------------------------------

def build_18() -> None:
    body = f"""
    <h2>zip() — соединяем два списка попарно</h2>
    {code_block(
        "zip_primer.py",
        'names = ["Anna", "Bob"]\n'
        "scores = [95, 82]\n\n"
        "for name, score in zip(names, scores):\n"
        '    print(name, "—", score)\n',
    )}
    {flow_diagram([
        ("names[0], scores[0]", "Anna, 95"),
        ("names[1], scores[1]", "Bob, 82"),
    ], caption="zip() берёт по одному элементу из каждого списка на одинаковой позиции")}
    {callout(
        "info",
        "zip() останавливается на самом коротком",
        "Если списки разной длины, <code class=\"inline\">zip()</code> по умолчанию "
        "останавливается, как только заканчивается более короткий — «лишние» элементы длинного "
        "списка просто игнорируются, без ошибки.",
    )}

    <h2>zip() + dict — собрать словарь из двух списков</h2>
    {code_block(
        "zip_v_dict.py",
        'names = ["Anna", "Bob", "Maria"]\n'
        "scores = [95, 82, 91]\n\n"
        "result = dict(zip(names, scores))\n"
        "print(result)   # {'Anna': 95, 'Bob': 82, 'Maria': 91}\n",
    )}

    <h2>Распаковка в циклах</h2>
    <p>Мы уже пользовались этим для словарей (§11.17) — тот же принцип, что и распаковка кортежа
    из §11.13, только применённая внутри цикла:</p>
    {code_block(
        "raspakovka_v_cikle.py",
        'pary = [("Anna", 95), ("Bob", 82)]\n'
        "for name, score in pary:\n"
        '    print(f"{name}: {score}")\n',
    )}

    {practice_card(
        "11-18",
        "Практика: zip() и распаковка в циклах",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-18/index.html",
    )}
    """
    page(
        "11-18-zip-i-raspakovka.html",
        page_title="zip() и распаковка",
        description="zip() соединяет несколько списков поэлементно; dict(zip(...)) собирает словарь; распаковка кортежей в циклах.",
        kicker_suffix="zip() и распаковка",
        h1="zip() и распаковка",
        lede="Один инструмент, который часто идёт рука об руку с кортежами и распаковкой: "
        "соединить два списка поэлементно.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-07 · Множества (расширено: свойства, пустое множество, методы)
# ---------------------------------------------------------------------------

def build_07() -> None:
    body = f"""
    <p><strong>Множество</strong> (<code class="inline">set</code>) — коллекция в фигурных
    скобках, у которой два ключевых отличия от списка: элементы в ней не повторяются, а обращения
    по числовому индексу нет — множество не позиционная последовательность.</p>
    {code_block("mnozhestva.py", 'chisla = {1, 2, 2, 3, 3, 3}\nprint(chisla)   # {1, 2, 3} — повторы исчезли сами\n')}

    <h2>Зачем нужны множества?</h2>
    <p>Два самых частых случая: быстро убрать повторы из списка и быстро проверить, есть ли
    значение в коллекции.</p>
    {code_block("primenenie_mnozhestv.py", 'spisok_s_povtorami = [1, 2, 2, 3, 1, 4]\nunikalnye = set(spisok_s_povtorami)\nprint(unikalnye)   # {1, 2, 3, 4}\n')}
    {code_block("chlenstvo_mnozhestva.py", 'allowed = {"admin", "editor", "viewer"}\nrole = "editor"\nif role in allowed:\n    print("Доступ разрешён")\n')}
    {callout(
        "info",
        "Множество не «случайно упорядочено» — оно просто не позиционное",
        "Не стоит думать про set как про «список со случайным порядком». Правильная модель: у "
        "множества <strong>нет</strong> позиций вообще — писать <code class=\"inline\">my_set[0]</code> "
        "нельзя (TypeError), и код никогда не должен полагаться на то, в каком порядке множество "
        "переберётся циклом.",
    )}

    <h2>Пустое множество — частая ловушка</h2>
    {code_block("pustoe_mnozhestvo.py", "print(type({}))        # <class 'dict'> — это пустой словарь!\nprint(type(set()))    # <class 'set'> — а это пустое множество\n")}
    {callout(
        "warning",
        "{} — это пустой словарь, а не пустое множество",
        "Фигурные скобки без содержимого Python по умолчанию считает пустым "
        "<code class=\"inline\">dict</code> (§11.17), потому что словари появились в языке как "
        "более базовый случай использования <code class=\"inline\">{}</code>. Чтобы создать "
        "пустое множество, нужно явно написать <code class=\"inline\">set()</code>.",
    )}

    <h2>add, remove, discard, pop, clear</h2>
    {code_block(
        "metody_mnozhestv.py",
        "tags = {\"python\", \"beginner\"}\n"
        "tags.add(\"tutorial\")\n"
        "tags.discard(\"missing\")   # без ошибки, даже если элемента нет\n"
        "print(tags)\n",
    )}
    {comparison_table(
        ["Метод", "Если элемента нет"],
        [
            ["<code class=\"inline\">.remove(x)</code>", "<code class=\"inline\">KeyError</code>"],
            ["<code class=\"inline\">.discard(x)</code>", "ничего не происходит, ошибки нет"],
        ],
    )}
    {callout(
        "tip",
        "pop() у множества удаляет ПРОИЗВОЛЬНЫЙ элемент",
        "В отличие от <code class=\"inline\">list.pop()</code>, у множества нет понятия "
        "«последний элемент» — <code class=\"inline\">set.pop()</code> удаляет и возвращает "
        "какой-то один элемент, но заранее неизвестно какой.",
    )}

    <h2>Операции над множествами</h2>
    {code_block(
        "operacii_mnozhestv.py",
        "a = {1, 2, 3}\n"
        "b = {2, 3, 4}\n\n"
        "print(a | b)   # объединение: {1, 2, 3, 4}\n"
        "print(a & b)   # пересечение: {2, 3}\n"
        "print(a - b)   # разность: {1}\n",
    )}
    {callout(
        "info",
        "Полная алгебра множеств — в §11.16",
        "Здесь — только знакомство. Венн-диаграммы для всех четырёх операций, подмножества и "
        "хешируемость разберём в следующем разделе.",
    )}

    {practice_card(
        "11-07",
        "Практика: множества и их операции",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-07/index.html",
    )}
    """
    page(
        "11-07-mnozhestva.html",
        page_title="Множества",
        description="Множества (set) в Python: уникальные значения, пустое множество, add/remove/discard/pop, операции объединения/пересечения/разности.",
        kicker_suffix="Множества",
        h1="Множества",
        lede="Коллекция без повторов и без позиций — быстрый способ убрать дубликаты и "
        "сравнивать наборы значений.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-19 · Операции множеств: Венн-диаграммы, подмножества, хешируемость, frozenset
# ---------------------------------------------------------------------------

def build_19() -> None:
    python_users = ["Anna", "Bob", "Maria"]
    data_users = ["Bob", "Li"]
    body = f"""
    <h2>Множества как круги на диаграмме Венна</h2>
    <p>Две группы участников курсов — удобный пример, на котором видно все четыре операции сразу:</p>
    {code_block(
        "dve_gruppy.py",
        f'python_users = {python_users!r}\n'
        f'data_users = {data_users!r}\n',
    )}

    <h3>Объединение — union, |</h3>
    {venn_diagram("python_users", "data_users", ["Anna", "Maria"], ["Bob"], ["Li"], highlight="union", result_label="{'Anna', 'Bob', 'Maria', 'Li'}", caption="python_users | data_users — все, кто есть хоть в одной группе")}
    {code_block("union.py", "print(set(python_users) | set(data_users))\n")}

    <h3>Пересечение — intersection, &amp;</h3>
    {venn_diagram("python_users", "data_users", ["Anna", "Maria"], ["Bob"], ["Li"], highlight="intersection", result_label="{'Bob'}", caption="python_users & data_users — кто есть в ОБЕИХ группах")}
    {code_block("intersection.py", "print(set(python_users) & set(data_users))\n")}

    <h3>Разность — difference, -</h3>
    {venn_diagram("python_users", "data_users", ["Anna", "Maria"], ["Bob"], ["Li"], highlight="diff_a", result_label="{'Anna', 'Maria'}", caption="python_users - data_users — только в первой группе")}
    {code_block("difference.py", "print(set(python_users) - set(data_users))\n")}

    <h3>Симметричная разность — symmetric_difference, ^</h3>
    {venn_diagram("python_users", "data_users", ["Anna", "Maria"], ["Bob"], ["Li"], highlight="symdiff", result_label="{'Anna', 'Maria', 'Li'}", caption="python_users ^ data_users — в одной группе, но не в обеих сразу")}
    {code_block("symmetric_difference.py", "print(set(python_users) ^ set(data_users))\n")}

    {comparison_table(
        ["Операция", "Оператор", "Метод"],
        [
            ["объединение", "<code class=\"inline\">a | b</code>", "<code class=\"inline\">a.union(b)</code>"],
            ["пересечение", "<code class=\"inline\">a &amp; b</code>", "<code class=\"inline\">a.intersection(b)</code>"],
            ["разность", "<code class=\"inline\">a - b</code>", "<code class=\"inline\">a.difference(b)</code>"],
            ["симметричная разность", "<code class=\"inline\">a ^ b</code>", "<code class=\"inline\">a.symmetric_difference(b)</code>"],
        ],
    )}

    <h2>Подмножество и надмножество</h2>
    {code_block(
        "podmnozhestvo.py",
        'required = {"python", "git"}\n'
        'available = {"python", "git", "docker", "linux"}\n\n'
        "print(required <= available)     # True — required ЦЕЛИКОМ входит в available\n"
        "print(required.issubset(available))   # то же самое\n",
    )}
    {venn_diagram("required", "available", [], ["python", "git"], ["docker", "linux"], mode="subset", highlight="intersection", caption="required <= available — required (внутренний круг) целиком лежит внутри available (внешний круг)")}
    {comparison_table(
        ["Оператор / метод", "Значение"],
        [
            ["<code class=\"inline\">a &lt;= b</code> / <code class=\"inline\">a.issubset(b)</code>", "все элементы a есть и в b"],
            ["<code class=\"inline\">a &gt;= b</code> / <code class=\"inline\">a.issuperset(b)</code>", "все элементы b есть и в a"],
            ["<code class=\"inline\">a.isdisjoint(b)</code>", "у a и b нет общих элементов вообще"],
        ],
    )}

    <h2>Хешируемость: почему в множестве нельзя хранить список</h2>
    {code_block("hashability_error.py", "bad = {[1, 2], [3, 4]}\n# TypeError: cannot use 'list' as a set element (unhashable type: 'list')\n")}
    {callout(
        "info",
        "Элементы множества и ключи словаря должны быть достаточно «стабильными»",
        "Python должен быть уверен, что значение внутри множества (или ключ словаря) не "
        "изменится незаметно, пока лежит там. Формальный термин для такой стабильности — "
        "<strong>хешируемость (hashable)</strong>. Изменяемые типы (список, словарь, множество) "
        "хешируемыми не бывают именно поэтому.",
    )}
    {capability_map([
        ("Обычно хешируемы", ["int, float, str", "bool, bytes", "tuple — если все элементы тоже хешируемы", "frozenset"]),
        ("Не хешируемы", ["list", "dict", "set"]),
    ], title="Что можно класть в множество / использовать как ключ словаря")}

    <h2>frozenset — неизменяемое множество</h2>
    {code_block("frozenset_primer.py", 'zamorozhennoe = frozenset({"python", "git"})\nprint(zamorozhennoe)\n# zamorozhennoe.add("docker")  # AttributeError — метода add() нет\n')}
    {callout(
        "tip",
        "Когда пригодится frozenset",
        "<code class=\"inline\">frozenset</code> нужен, когда множество само должно быть "
        "хешируемым — например, чтобы использовать его как элемент другого множества или как "
        "ключ словаря, что с обычным <code class=\"inline\">set</code> невозможно.",
    )}

    {practice_card(
        "11-19",
        "Практика: алгебра множеств, подмножества, хешируемость",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-19/index.html",
    )}
    """
    page(
        "11-19-mnozhestva-operacii.html",
        page_title="Операции множеств и хешируемость",
        description="Венн-диаграммы для union/intersection/difference/symmetric_difference, subset/superset, хешируемость, frozenset.",
        kicker_suffix="Операции множеств",
        h1="Операции множеств и хешируемость",
        lede="Четыре операции алгебры множеств на Венн-диаграммах — и почему список нельзя "
        "положить внутрь множества.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-08 · Словари (расширено: mapping mental model)
# ---------------------------------------------------------------------------

def build_08() -> None:
    body = f"""
    <h2>От позиции к ключу</h2>
    <p>У списка доступ идёт по числовой позиции. У словаря — по <strong>ключу</strong>, обычно
    строке:</p>
    {comparison_table(
        ["", "list", "dict"],
        [
            ["Модель доступа", "позиция → значение", "ключ → значение"],
            ["Пример", "<code class=\"inline\">names[0]</code>", "<code class=\"inline\">student[\"name\"]</code>"],
        ],
    )}
    <p><strong>Словарь</strong> (<code class="inline">dict</code>) — самая гибкая коллекция:
    хранит пары «ключ — значение» вместо простых значений по порядку.</p>
    {code_block(
        "slovari.py",
        "student = {\n"
        '    "name": "Cartesian",\n'
        '    "age": 12,\n'
        '    "city": "Москва",\n'
        "}\n"
        'print(student["name"])   # Cartesian\n',
    )}
    {namespace_diagram(
        [('"name"', '"Cartesian"'), ('"age"', "12"), ('"city"', '"Москва"')],
        caption="Словарь — таблица «ключ → значение», а не пронумерованные ячейки",
    )}
    {callout(
        "info",
        "Повторяющийся ключ в литерале — побеждает последнее значение",
        "Если в фигурных скобках дважды написать один и тот же ключ, ошибки не будет — "
        "останется только значение, написанное позже.",
    )}

    <h2>Добавление и изменение значений</h2>
    {code_block(
        "izmenenie_slovarya.py",
        'student["age"] = 13         # изменить существующее значение\n'
        'student["grade"] = "7 класс" # добавить новый ключ\n'
        "print(student)\n",
    )}

    <h2>Доступ по ключу: [] и get()</h2>
    {code_block("dostup_get.py", 'print(student["name"])        # Cartesian\nprint(student.get("email"))    # None — ключа нет, но ошибки тоже нет\nprint(student.get("email", "нет email"))  # с явным значением по умолчанию\n')}
    {callout(
        "warning",
        "KeyError — обращение к несуществующему ключу",
        "<code class=\"inline\">student[\"phone\"]</code>, если такого ключа нет, вызовет "
        "<code class=\"inline\">KeyError</code>. Более безопасный способ — метод "
        "<code class=\"inline\">student.get(\"phone\")</code>, который просто вернёт "
        "<code class=\"inline\">None</code> вместо ошибки. Квадратные скобки не «хуже» — они "
        "уместны, когда отсутствие ключа само по себе является ошибкой в программе.",
    )}

    <h2>Перебор словаря</h2>
    {code_block(
        "perebor_slovarya.py",
        "for key, value in student.items():\n"
        '    print(f"{key}: {value}")\n',
    )}

    <h2>Проверка наличия ключа</h2>
    {code_block("proverka_klyucha.py", 'print("name" in student)      # True\nprint("phone" in student)     # False\n')}

    {practice_card(
        "11-08",
        "Практика: словари — создание, изменение, перебор",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-08/index.html",
    )}
    """
    page(
        "11-08-slovari.html",
        page_title="Словари",
        description="Словари (dict) в Python: пары ключ-значение, доступ по ключу vs позиции, get(), добавление, изменение и перебор.",
        kicker_suffix="Словари",
        h1="Словари",
        lede="Самая гибкая встроенная коллекция Python — доступ по ключу вместо числового "
        "индекса.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-20 · Методы словарей
# ---------------------------------------------------------------------------

def build_20() -> None:
    body = f"""
    <h2>pop() и popitem()</h2>
    {code_block(
        "dict_pop.py",
        'student = {"name": "Cartesian", "age": 13, "grade": "7 класс"}\n'
        'age = student.pop("age")\n'
        "print(student, age)   # {'name': 'Cartesian', 'grade': '7 класс'} 13\n",
    )}
    {code_block("dict_popitem.py", "last_pair = student.popitem()\nprint(last_pair)   # ('grade', '7 класс') — последняя добавленная пара\n")}
    {callout(
        "info",
        "pop() у словаря — по ключу, не по позиции",
        "В отличие от <code class=\"inline\">list.pop(index)</code>, у словаря "
        "<code class=\"inline\">.pop(key)</code> принимает КЛЮЧ, а не числовую позицию — "
        "позиций у словаря просто нет. Можно передать значение по умолчанию вторым аргументом, "
        "если ключа может не быть: <code class=\"inline\">student.pop(\"phone\", None)</code>.",
    )}

    <h2>update() — слить несколько пар сразу</h2>
    {code_block("dict_update.py", 'student = {"name": "Cartesian", "age": 13}\nstudent.update({"age": 14, "city": "Москва"})\nprint(student)   # age заменился, city добавился\n')}

    <h2>setdefault() — добавить значение, только если ключа ещё нет</h2>
    {code_block(
        "setdefault.py",
        "counts = {}\n"
        'word = "python"\n'
        "counts.setdefault(word, 0)\n"
        "counts[word] += 1\n"
        "print(counts)   # {'python': 1}\n",
    )}
    {callout(
        "tip",
        "setdefault() = «если ключа нет — создай со значением по умолчанию»",
        "<code class=\"inline\">counts.setdefault(word, 0)</code> ничего не делает, если "
        "<code class=\"inline\">word</code> уже есть в словаре, и создаёт запись со значением 0, "
        "если ключа не было — в обоих случаях после вызова можно смело писать "
        "<code class=\"inline\">counts[word] += 1</code>. Полный алгоритм подсчёта частоты слов "
        "с таким подходом — в §11.24.",
    )}

    <h2>keys(), values(), items() — не обычные списки</h2>
    {code_block(
        "keys_values_items.py",
        'student = {"name": "Cartesian", "age": 13}\n'
        "print(student.keys())     # dict_keys(['name', 'age'])\n"
        "print(student.values())   # dict_values(['Cartesian', 13])\n"
        "print(student.items())     # dict_items([('name', 'Cartesian'), ('age', 13)])\n",
    )}
    {callout(
        "info",
        "Это «живые» представления, а не списки",
        "<code class=\"inline\">.keys()</code>, <code class=\"inline\">.values()</code> и "
        "<code class=\"inline\">.items()</code> возвращают объекты-представления "
        "(<code class=\"inline\">dict_keys</code> и т.д.) — они отражают словарь в реальном "
        "времени. Для перебора циклом это не важно, но если нужен именно список, оберните в "
        "<code class=\"inline\">list(student.keys())</code>.",
    )}

    <h2>Порядок словаря</h2>
    {callout(
        "info",
        "Современный Python сохраняет порядок вставки",
        "Начиная с Python 3.7 порядок пар в словаре гарантированно совпадает с порядком, в "
        "котором их добавили — это официальная гарантия языка, а не случайность реализации. Но "
        "словарь остаётся <strong>отображением</strong> (доступ по ключу), а не позиционной "
        "коллекцией — не стоит писать код, который полагается на числовые позиции словаря.",
    )}

    <h2>Проверка in — только по ключам</h2>
    {code_block(
        "membership_dict.py",
        'student = {"name": "Cartesian", "age": 13}\n'
        'print("name" in student)          # True — есть такой КЛЮЧ\n'
        'print("Cartesian" in student)     # False — это значение, не ключ!\n'
        'print("Cartesian" in student.values())   # True — а вот так корректно проверить значение\n',
    )}
    {callout(
        "warning",
        "in у словаря проверяет ключи, а не значения",
        "Частая ошибка новичка: <code class=\"inline\">value in my_dict</code> проверяет, есть "
        "ли <code class=\"inline\">value</code> среди КЛЮЧЕЙ. Чтобы проверить значения, нужно "
        "явно написать <code class=\"inline\">value in my_dict.values()</code>.",
    )}

    <h2>Ключи словаря тоже должны быть хешируемыми</h2>
    {code_block("hashable_keys.py", '{["x", "y"]: 1}\n# TypeError: cannot use \'list\' as a dict key (unhashable type: \'list\')\n')}
    <p>Тот же принцип хешируемости из §11.16 — список нельзя использовать как ключ словаря по
    той же причине, по которой его нельзя положить в множество.</p>

    {practice_card(
        "11-20",
        "Практика: pop, update, setdefault, keys/values/items",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-20/index.html",
    )}
    """
    page(
        "11-20-slovari-metody.html",
        page_title="Методы словарей",
        description="pop, popitem, update, setdefault, keys/values/items как представления, порядок вставки, membership по ключам, хешируемые ключи.",
        kicker_suffix="Методы словарей",
        h1="Методы словарей",
        lede="pop, update, setdefault и представления keys/values/items — инструменты, без "
        "которых не обходится ни один реальный словарь.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-21 · Вложенные структуры
# ---------------------------------------------------------------------------

def build_21() -> None:
    body = f"""
    <h2>Вложенный словарь</h2>
    {code_block(
        "vlozhennyj_slovar.py",
        "student = {\n"
        '    "name": "Anna",\n'
        '    "scores": {"math": 95, "python": 100},\n'
        "}\n"
        'print(student["scores"]["python"])   # 100\n',
    )}
    {tree_diagram(
        ("student", [("name → \"Anna\"", []), ("scores", [("math → 95", []), ("python → 100", [])])]),
        caption="student['scores']['python'] — сначала внешний ключ, потом внутренний",
    )}

    <h2>Список словарей — самый частый реальный паттерн</h2>
    {code_block(
        "spisok_slovarej.py",
        "students = [\n"
        '    {"name": "Anna", "score": 95},\n'
        '    {"name": "Bob", "score": 82},\n'
        "]\n\n"
        "for student in students:\n"
        '    print(student["name"], student["score"])\n',
    )}
    {tree_diagram(
        ("students (список)", [
            ("[0]", [("name → \"Anna\"", []), ("score → 95", [])]),
            ("[1]", [("name → \"Bob\"", []), ("score → 82", [])]),
        ]),
        caption="Список словарей — так часто выглядят настоящие данные (записи из базы, ответ API)",
    )}
    {callout(
        "tip",
        "Список словарей — это уже почти JSON",
        "Ровно так организованы данные, приходящие от многих веб-сервисов (JSON) — подробно про "
        "JSON поговорим в одной из следующих глав, но структура «список записей, у каждой записи "
        "свои поля» уже полностью знакома.",
    )}

    <h2>Словарь списков — обратный вариант</h2>
    {code_block(
        "slovar_spiskov.py",
        "classroom = {\n"
        '    "students": ["Anna", "Bob"],\n'
        '    "scores": [95, 82],\n'
        "}\n",
    )}
    <p>Оба представления валидны — какое выбрать, зависит от того, как с данными будут работать
    дальше: список словарей удобнее, если часто нужна ОДНА запись целиком (найти Bob'а и все его
    данные); словарь списков — если чаще нужна ОДНА колонка целиком (все имена или все оценки).</p>

    {practice_card(
        "11-21",
        "Практика: вложенные словари и список словарей",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-21/index.html",
    )}
    """
    page(
        "11-21-vlozhennye-struktury.html",
        page_title="Вложенные структуры",
        description="Вложенные словари, список словарей, словарь списков — как выглядят настоящие данные (запись, коллекция записей).",
        kicker_suffix="Вложенные структуры",
        h1="Вложенные структуры",
        lede="Настоящие данные редко бывают плоскими: списки словарей и словари внутри "
        "словарей — норма, а не исключение.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-22 · Преобразования и comprehensions
# ---------------------------------------------------------------------------

def build_22() -> None:
    body = f"""
    <h2>Преобразования между коллекциями</h2>
    {code_block(
        "preobrazovaniya.py",
        'print(list("Python"))            # [\'P\', \'y\', \'t\', \'h\', \'o\', \'n\']\n'
        "print(tuple([1, 2, 3]))          # (1, 2, 3)\n"
        "print(set([1, 1, 2, 3]))          # {1, 2, 3}\n",
    )}
    {callout(
        "info",
        "dict() требует пары «ключ, значение»",
        "<code class=\"inline\">dict(...)</code> превращает в словарь не любую коллекцию, а "
        "только такую, из которой можно собрать пары: например, <code class=\"inline\">dict(zip(a, b))</code> "
        "из §11.14. Просто <code class=\"inline\">dict([1, 2, 3])</code> вызовет ошибку.",
    )}

    <h2>Строка ↔ список — самое частое преобразование</h2>
    {flow_diagram([
        ("строка", '"a,b,c"'),
        ("split()", "['a', 'b', 'c']"),
        ("join()", '"a,b,c"'),
    ], caption="text.split() → список, ' '.join(список) → строка обратно")}
    {code_block("split_join.py", 'text = "python git linux"\nwords = text.split()\nprint(words)          # [\'python\', \'git\', \'linux\']\nprint(" ".join(words))   # "python git linux"\n')}

    <h2>sorted() для разных коллекций</h2>
    {code_block(
        "sorted_raznoe.py",
        "print(sorted((3, 1, 2)))          # [1, 2, 3] — из кортежа\n"
        "print(sorted({3, 1, 2}))           # [1, 2, 3] — из множества\n"
        'print(sorted({"b": 1, "a": 2}))   # [\'a\', \'b\'] — из словаря сортируются КЛЮЧИ\n',
    )}
    {callout(
        "tip",
        "sorted() всегда возвращает список",
        "Независимо от того, что было на входе — кортеж, множество или словарь — "
        "<code class=\"inline\">sorted()</code> всегда отдаёт обычный <code class=\"inline\">list</code>.",
    )}

    <h2>List comprehension — уже знакомо, теперь по шагам</h2>
    {code_block("comprehension_klassika.py", "kvadraty = []\nfor n in range(1, 6):\n    kvadraty.append(n ** 2)\nprint(kvadraty)\n")}
    {code_block("comprehension_novyj.py", "kvadraty = [n ** 2 for n in range(1, 6)]\nprint(kvadraty)\n")}
    {flow_diagram([
        ("источник", "range(1, 6)"),
        ("выражение", "n ** 2"),
        ("результат", "[1, 4, 9, 16, 25]"),
    ], caption="[выражение for n in источник] — то же самое, что цикл, но в одну строку")}

    <h2>Comprehension с условием</h2>
    {code_block("comprehension_uslovie.py", "chetnye = [n for n in range(10) if n % 2 == 0]\nprint(chetnye)   # [0, 2, 4, 6, 8]\n")}
    {flow_diagram([
        ("источник", "range(10)"),
        ("фильтр", "if n % 2 == 0"),
        ("результат", "[0, 2, 4, 6, 8]"),
    ], caption="Условие в конце — фильтр: элемент попадёт в результат, только если условие True")}

    <h2>Set и dict comprehension</h2>
    {code_block("set_comprehension.py", 'unikalnye_bukvy = {ch.lower() for ch in "Python"}\nprint(unikalnye_bukvy)\n')}
    {code_block("dict_comprehension.py", "kvadraty_slovar = {n: n ** 2 for n in range(5)}\nprint(kvadraty_slovar)   # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}\n")}
    <p>Та же идея «источник → выражение → результат», только результат оформляется в фигурных
    скобках — с двоеточием получаем словарь, без — множество.</p>

    {callout(
        "info",
        "[[icon:launch]] Чуть глубже — генераторные выражения",
        "<code class=\"inline\">(n ** 2 for n in range(5))</code> — генераторное выражение, "
        "похожее на comprehension, но не строящее список целиком в памяти сразу, а отдающее "
        "значения по одному. Пригодится позже, когда будем говорить об итераторах и работе с "
        "большими объёмами данных.",
    )}

    {classic_vs_modern(
        "Сборка списка: цикл vs comprehension",
        "Цикл с append()",
        "kuby = []\nfor n in range(1, 6):\n    if n % 2 == 0:\n        kuby.append(n ** 3)",
        "List comprehension",
        "kuby = [n ** 3 for n in range(1, 6) if n % 2 == 0]",
        "comprehension для простых преобразований и фильтров — короче и читается как одна "
        "мысль. Но comprehension — это НЕ универсальный инструмент глубокого копирования и не "
        "заменяет цикл, если внутри нужны побочные эффекты (print, запись в файл, несколько "
        "условий с разной логикой) — тогда обычный цикл с append() читается понятнее.",
    )}

    {practice_card(
        "11-22",
        "Практика: преобразования и comprehensions",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-22/index.html",
    )}
    """
    page(
        "11-22-preobrazovaniya-i-comprehensions.html",
        page_title="Преобразования и comprehensions",
        description="Преобразования между коллекциями, split()/join(), sorted() для разных коллекций, list/set/dict comprehension, генераторные выражения.",
        kicker_suffix="Преобразования и comprehensions",
        h1="Преобразования и comprehensions",
        lede="От list()/tuple()/set() до компактного способа строить новые коллекции одной "
        "строкой — но только после того, как понятен обычный цикл.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-09 · Мини-проект — бесконечные цвета (без изменений, только навигация)
# ---------------------------------------------------------------------------

def build_09() -> None:
    body = f"""
    <p>Словарь отлично подходит для «перевода» одного значения в другое — например, названия
    цвета в его код. Нарисуем фигуру, «раскрашенную по словарю».</p>
    {code_block(
        "beskonechnye_cveta.py",
        "cvetovaya_karta = {\n"
        '    "огонь": "red",\n'
        '    "трава": "green",\n'
        '    "небо": "blue",\n'
        "}\n\n"
        'zapros = "небо"\n'
        "artist.pencolor(cvetovaya_karta[zapros])\n"
        "artist.circle(50)\n",
    )}
    {exercise(2, "Добавьте свои цвета", "Добавьте в cvetovaya_karta ещё 3-4 пары «слово — цвет» и нарисуйте для каждого отдельную фигуру.")}

    {local_required_card(
        "11-09",
        "Практика: бесконечные цвета (словари + Turtle)",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/11-09/index.html",
    )}
    """
    page(
        "11-09-mini-proekt-cveta.html",
        page_title="Мини-проект — бесконечные цвета",
        description="Словарь как карта соответствий — раскрашиваем фигуры Turtle через словарь.",
        kicker_suffix="Бесконечные цвета",
        h1="Мини-проект — бесконечные цвета",
        lede="Словарь как «переводчик» — от слова к конкретному цвету Turtle.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-23 · Как выбрать правильную структуру
# ---------------------------------------------------------------------------

def build_23() -> None:
    body = f"""
    <h2>Таблица изменяемости</h2>
    {comparison_table(
        ["Тип", "Упорядочен?", "Изменяем?", "Повторы?", "Доступ"],
        [
            ["<code class=\"inline\">list</code>", "да", "да", "да", "по индексу"],
            ["<code class=\"inline\">tuple</code>", "да", "нет", "да", "по индексу"],
            ["<code class=\"inline\">set</code>", "нет позиций", "да", "нет — только уникальные", "по членству (in)"],
            ["<code class=\"inline\">frozenset</code>", "нет позиций", "нет", "нет — только уникальные", "по членству (in)"],
            ["<code class=\"inline\">dict</code>", "сохраняет порядок вставки", "да", "ключи уникальны", "по ключу"],
        ],
    )}

    <h2>Таблица хешируемости</h2>
    {capability_map([
        ("Обычно хешируемы", ["int, float, str", "bool, bytes", "tuple (если элементы хешируемы)", "frozenset"]),
        ("Не хешируемы", ["list", "dict", "set"]),
    ], title="Что можно класть в множество / использовать как ключ словаря")}

    <h2>Итоговый ориентир выбора</h2>
    {decision_map([
        ("Нужна пара «ключ → значение»?", "dict"),
        ("Иначе: нужны только уникальные значения, порядок не важен?", "set"),
        ("Иначе: нужен порядок, значения точно не изменятся?", "tuple"),
        ("Иначе: нужен порядок и придётся менять содержимое?", "list"),
    ], title="Полный ориентир выбора структуры", caption="Правило большого пальца — сначала думайте о задаче, потом о синтаксисе")}

    <h2>Истинность коллекций (truthiness)</h2>
    <p>Из главы 9: пустая коллекция — <code class="inline">False</code> в логическом контексте,
    непустая — <code class="inline">True</code>, независимо от значений внутри:</p>
    {comparison_table(
        ["Пусто → False", "Не пусто → True"],
        [
            ["<code class=\"inline\">[]</code>", "<code class=\"inline\">[0]</code>"],
            ["<code class=\"inline\">()</code>", "<code class=\"inline\">(\"\",)</code>"],
            ["<code class=\"inline\">set()</code>", "<code class=\"inline\">{0}</code>"],
            ["<code class=\"inline\">{}</code>", "<code class=\"inline\">{\"x\": None}</code>"],
        ],
    )}
    {code_block("truthiness_kollekcij.py", 'items = []\nif items:\n    print("Есть элементы")\nelse:\n    print("Список пуст")\n')}
    {callout(
        "tip",
        "if items: — идиоматичнее, чем if len(items) > 0:",
        "Обе записи работают одинаково, но <code class=\"inline\">if items:</code> прямо "
        "спрашивает «список непустой?», без промежуточного подсчёта длины — это стандартный "
        "стиль в Python-коде.",
    )}

    <h2>Изменение коллекции во время перебора — ещё одна ловушка</h2>
    {code_block(
        "mutation_during_iteration.py",
        "items = [2, 4, 6, 8]\n"
        "for item in items:\n"
        "    if item % 2 == 0:\n"
        "        items.remove(item)\n"
        "print(items)   # [4, 8] — а не [], хотя условие подходит КАЖДОМУ элементу!\n",
    )}
    {callout(
        "warning",
        "Не меняйте размер коллекции, пока перебираете её тем же циклом",
        "Удаление элементов списка во время перебора этого же списка сдвигает индексы прямо "
        "«под ногами» у цикла — часть элементов будет пропущена. Для словаря или множества "
        "Python вообще выбросит <code class=\"inline\">RuntimeError: dictionary changed size "
        "during iteration</code>. Безопасные способы: собирать результат в НОВУЮ коллекцию, "
        "использовать comprehension, или перебирать явную копию — "
        "<code class=\"inline\">for item in items.copy():</code>.",
    )}

    {practice_card(
        "11-23",
        "Практика: выбор структуры данных по сценарию",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-23/index.html",
    )}
    """
    page(
        "11-23-vybor-struktury.html",
        page_title="Как выбрать правильную структуру",
        description="Таблица изменяемости и хешируемости, итоговая decision-map выбора структуры данных, truthiness коллекций, ловушка изменения во время перебора.",
        kicker_suffix="Выбор структуры",
        h1="Как выбрать правильную структуру",
        lede="Теперь, когда все четыре коллекции знакомы по отдельности, — как решить, какую "
        "использовать в конкретной задаче.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-24 · Отладка коллекций: 14 типичных ошибок
# ---------------------------------------------------------------------------

def build_24() -> None:
    bugs = [
        ("1 · IndexError", "items = ['A', 'B', 'C']\nprint(items[3])\n", "Допустимые индексы — от 0 до len(items)-1 = 2. Индекс 3 не существует."),
        ("2 · KeyError", "student = {'name': 'Anna'}\nprint(student['email'])\n", "Такого ключа в словаре нет. Безопаснее: student.get('email')."),
        ("3 · ValueError от index()/remove()", "fruits = ['яблоко', 'банан']\nfruits.remove('вишня')\n", "'вишня' нет в списке — remove() ищет по значению и не находит его. Проверьте через in перед вызовом."),
        ("4 · TypeError: unhashable type", "bad = {[1, 2]: 'значение'}\n", "Список нельзя использовать как ключ словаря (или элемент множества) — он изменяем, а значит не хешируем (§11.16)."),
        ("5 · append() вместо extend()", "a = [1, 2]\na.append([3, 4])\nprint(a)   # [1, 2, [3, 4]], а не [1, 2, 3, 4]", "append() всегда добавляет один объект. Чтобы добавить элементы ИЗ списка — нужен extend()."),
        ("6 · x = x.sort() — потеря списка", "numbers = [3, 1, 2]\nnumbers = numbers.sort()\nprint(numbers)   # None", "sort() мутирует список на месте и возвращает None. Присваивание результата обратно стирает список."),
        ("7 · Aliasing вместо копии", "a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)   # тоже [1, 2, 3, 4]!", "b = a не копирует список — оба имени указывают на один и тот же объект (§11.9). Нужно b = a.copy()."),
        ("8 · Поверхностная копия и вложенный список", "original = [[1, 2]]\ncopy_ = original.copy()\ncopy_[0][0] = 99\nprint(original)   # [[99, 2]] — тоже изменился!", ".copy() копирует только внешний список — вложенные списки остаются общими (§11.10). Нужен copy.deepcopy()."),
        ("9 · [[0]*3]*3 — общая строка", "grid = [[0] * 3] * 3\ngrid[0][0] = 1\nprint(grid)   # изменились ВСЕ строки", "*3 копирует ссылку на один и тот же внутренний список трижды. Используйте [[0]*3 for _ in range(3)]."),
        ("10 · Изменение списка во время перебора", "items = [1, 2, 3, 4]\nfor x in items:\n    if x % 2 == 0:\n        items.remove(x)\nprint(items)   # не то, что ожидали", "Удаление элемента сдвигает индексы прямо во время перебора — часть значений пропускается. Стройте новый список или перебирайте копию."),
        ("11 · {} вместо set()", "empty = {}\nprint(type(empty))   # <class 'dict'>, а не set!", "Пустой словарь и пустое множество выглядят по-разному только в непустом виде. Пустое множество — всегда set()."),
        ("12 · Кортеж из одного элемента без запятой", "point = (42)\nprint(type(point))   # <class 'int'>", "Кортеж создаёт запятая, а не скобки. Нужно (42,)."),
        ("13 · in у словаря проверяет ключи, не значения", "student = {'name': 'Anna'}\nprint('Anna' in student)   # False!", "'Anna' — значение, а не ключ. Для проверки значений: 'Anna' in student.values()."),
        ("14 · Перепутан порядок вложенного индекса", "matrix = [[1, 2, 3], [4, 5, 6]]\nprint(matrix[2][0])   # IndexError", "У matrix всего 2 строки (индексы 0 и 1) по 3 столбца — сначала строка, потом столбец, не наоборот."),
    ]
    bugs_html = "".join(
        f"""
        <div style="margin:20px 0;padding:18px 20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
          <div style="font-family:Sora,sans-serif;font-weight:700;font-size:15px;color:#DB2777;margin-bottom:10px">{title}</div>
          {code_block("bug.py", code)}
          <p style="margin-top:10px">{explanation}</p>
        </div>"""
        for title, code, explanation in bugs
    )

    body = f"""
    <p>14 типичных ошибок при работе со списками, кортежами, множествами и словарями — каждая с
    примером и объяснением. Первые две разберём отдельно с диаграммой, остальные — компактно.</p>

    <h2>IndexError — визуально</h2>
    {list_box_diagram(["A", "B", "C"], indices=True, caption="items = ['A', 'B', 'C'] — допустимые индексы только 0, 1, 2 (и -1, -2, -3)")}
    {code_block("indexerror.py", "items = ['A', 'B', 'C']\nprint(items[3])\n# IndexError: list index out of range\n")}

    <h2>KeyError — визуально</h2>
    {namespace_diagram([("'name'", "'Anna'")], caption="У student есть только ключ 'name' — обращение по ключу 'email' не находит ничего и вызывает KeyError")}
    {code_block("keyerror.py", "student = {'name': 'Anna'}\nprint(student['email'])\n# KeyError: 'email'\n")}

    <h2>Ещё 12 типичных ошибок</h2>
    {bugs_html}

    {summary_box("Метод отладки: трасса по шагам", [
        "Перед запуском предскажите, что будет в переменной — потом сравните с реальным выводом.",
        "Для ошибок с индексами/ключами явно выпишите допустимый диапазон или список ключей.",
        "Если результат «странный, но без ошибки» — подозревайте aliasing или поверхностную копию.",
        "print() после каждого шага — самый надёжный способ найти момент, где ожидание разошлось с реальностью.",
    ])}

    {practice_card(
        "11-24",
        "Практика: находим и исправляем ошибки в коллекциях",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-24/index.html",
    )}
    """
    page(
        "11-24-debugging-kollekcij.html",
        page_title="Отладка коллекций: 14 типичных ошибок",
        description="14 именованных типичных ошибок при работе со списками, кортежами, множествами и словарями — с примерами и объяснениями.",
        kicker_suffix="Отладка коллекций",
        h1="Отладка коллекций: 14 типичных ошибок",
        lede="IndexError, KeyError, путаница append/extend, aliasing, поверхностная копия и "
        "другие ловушки — в одном месте, с примерами и разбором.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-25 · Мини-проект — подсчёт частоты слов
# ---------------------------------------------------------------------------

def build_25() -> None:
    body = f"""
    <p>Классическая задача, которая объединяет почти всё из этой главы: строки (глава 8), циклы
    (глава 10) и словарь как счётчик.</p>

    <h2>Алгоритм по шагам</h2>
    {code_block(
        "chastota_slov.py",
        'text = "python is great and python is fun"\n'
        "words = text.lower().split()\n\n"
        "counts = {}\n"
        "for word in words:\n"
        "    counts[word] = counts.get(word, 0) + 1\n\n"
        "print(counts)\n",
    )}
    {timeline_diagram([
        ("word = 'python'", "counts.get('python', 0) + 1 = 1 → counts = {'python': 1}"),
        ("word = 'is'", "counts = {'python': 1, 'is': 1}"),
        ("word = 'great'", "counts = {'python': 1, 'is': 1, 'great': 1}"),
        ("word = 'and'", "counts = {..., 'and': 1}"),
        ("word = 'python' снова", "counts.get('python', 0) + 1 = 2 → counts['python'] = 2"),
    ], caption="counts.get(word, 0) + 1 — если слова ещё нет, get() вернёт 0, и счётчик начнётся с 1")}
    {callout(
        "tip",
        "Почему именно .get(word, 0), а не counts[word]",
        "На первой встрече слова ключа <code class=\"inline\">word</code> в "
        "<code class=\"inline\">counts</code> ещё нет — <code class=\"inline\">counts[word]</code> "
        "вызвал бы <code class=\"inline\">KeyError</code>. <code class=\"inline\">.get(word, 0)</code> "
        "возвращает 0 для нового слова, и код одинаково работает и для новых, и для уже "
        "встречавшихся слов.",
    )}

    <h2>Тот же алгоритм через setdefault()</h2>
    {code_block(
        "chastota_setdefault.py",
        "counts = {}\n"
        "for word in words:\n"
        "    counts.setdefault(word, 0)\n"
        "    counts[word] += 1\n",
    )}

    <h2>[[icon:launch]] Чуть глубже — стандартная библиотека уже решила эту задачу</h2>
    {code_block(
        "counter_preview.py",
        "from collections import Counter\n\n"
        "counts = Counter(words)\n"
        "print(counts)             # Counter({'python': 2, 'is': 2, 'great': 1, 'and': 1, 'fun': 1})\n"
        "print(counts.most_common(2))   # [('python', 2), ('is', 2)]\n",
    )}
    {callout(
        "info",
        "Ручной алгоритм важнее, чем готовая функция",
        "<code class=\"inline\">Counter</code> из стандартной библиотеки делает то же самое в "
        "одну строку — и в реальном коде часто лучше использовать именно его. Но алгоритм на "
        "<code class=\"inline\">.get(word, 0) + 1</code> стоило пройти руками: он показывает, "
        "как вообще устроен подсчёт через словарь, а не только то, что для этого есть готовый "
        "инструмент.",
    )}

    {practice_card(
        "11-25",
        "Практика: подсчёт частоты слов в тексте",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-25/index.html",
    )}
    """
    page(
        "11-25-slovar-chastoty-slov.html",
        page_title="Мини-проект — подсчёт частоты слов",
        description="Классический алгоритм подсчёта частоты слов через словарь и .get(word, 0) + 1, вариант через setdefault(), превью collections.Counter.",
        kicker_suffix="Частота слов",
        h1="Мини-проект — подсчёт частоты слов",
        lede="Строки, циклы и словарь-счётчик в одной классической задаче — с ручным алгоритмом "
        "и превью готового инструмента из стандартной библиотеки.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-26 · Мини-проекты с коллекциями
# ---------------------------------------------------------------------------

def build_26() -> None:
    body = f"""
    <h2>Записная книжка контактов (dict)</h2>
    {code_block(
        "zapisnaya_knizhka.py",
        "contacts = {\n"
        '    "Anna": "anna@example.com",\n'
        '    "Bob": "bob@example.com",\n'
        "}\n\n"
        'contacts["Maria"] = "maria@example.com"   # добавить\n'
        'contacts["Anna"] = "anna.new@example.com"  # изменить\n'
        'del contacts["Bob"]                          # удалить\n\n'
        "for name, email in contacts.items():\n"
        '    print(f"{name}: {email}")\n',
    )}
    {callout(
        "tip",
        "Уже мини-база данных",
        "Записная книжка — это, по сути, крошечная база данных в памяти: словарь как хранилище, "
        "ключ как уникальный идентификатор записи.",
    )}

    <h2>Игровое поле (вложенный список)</h2>
    {code_block(
        "igrovoe_pole.py",
        'board = [\n'
        '    [".", ".", "."],\n'
        '    [".", "X", "."],\n'
        '    [".", ".", "."],\n'
        "]\n\n"
        "for row in board:\n"
        '    print(" ".join(row))\n',
    )}
    {matrix_diagram([[".", ".", "."], [".", "X", "."], [".", ".", "."]], row_labels=["0", "1", "2"], col_labels=["0", "1", "2"], highlight=(1, 1), caption="board[1][1] = 'X' — та же модель матрицы, что и в §11.11")}

    <h2>Список класса (список словарей)</h2>
    {code_block(
        "spisok_klassa.py",
        "roster = [\n"
        '    {"name": "Anna", "score": 95},\n'
        '    {"name": "Bob", "score": 82},\n'
        '    {"name": "Maria", "score": 91},\n'
        "]\n\n"
        "total = sum(student[\"score\"] for student in roster)\n"
        "average = total / len(roster)\n"
        'print(f"Средний балл: {average:.1f}")\n',
    )}

    <h2>Сравнение множеств: чего не хватает</h2>
    {code_block(
        "sravnenie_navykov.py",
        'required = {"python", "git", "sql"}\n'
        'available = {"python", "git"}\n\n'
        "missing = required - available\n"
        "common = required & available\n"
        'print("Не хватает:", missing)\n'
        'print("Уже есть:", common)\n',
    )}
    {venn_diagram("required", "available", ["sql"], ["python", "git"], [], highlight="diff_a", result_label="{'sql'}", caption="required - available — каких навыков не хватает")}

    {practice_card(
        "11-26",
        "Практика: мини-проекты с коллекциями",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-26/index.html",
    )}
    """
    page(
        "11-26-mini-proekty-kollekcii.html",
        page_title="Мини-проекты с коллекциями",
        description="Четыре мини-проекта: записная книжка контактов (dict), игровое поле (вложенный список), список класса (список словарей), сравнение множеств навыков.",
        kicker_suffix="Мини-проекты",
        h1="Мини-проекты с коллекциями",
        lede="Четыре коротких, но настоящих применения того, что мы изучили: контакты, игровое "
        "поле, список класса и сравнение множеств.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 11-10 · Мини-проект — перестановка имени и итоги (расширено: полный toolbox)
# ---------------------------------------------------------------------------

def build_10() -> None:
    body = f"""
    <p>Финальный мини-проект главы: разбить полное имя на части и собрать заново в другом
    порядке — «Фамилия Имя» вместо «Имя Фамилия», используя методы строк из главы 8 и списки
    из этой главы.</p>
    {code_block(
        "perestanovka_imeni.py",
        'full_name = input("Введите имя и фамилию через пробел: ")\n'
        "parts = full_name.split()   # split() возвращает список\n"
        "name, surname = parts        # распаковка, как у кортежей\n\n"
        'print(f"{surname} {name}")\n',
    )}
    {callout(
        "info",
        "split() возвращает список",
        "Мы видели <code class=\"inline\">.split()</code> в главе 8, но не заостряли внимание "
        "на том, что результат — это именно <code class=\"inline\">list</code>. Теперь, зная "
        "про списки, можно распаковывать его так же, как распаковывали кортежи в §11.13.",
    )}
    {exercise(3, "Три части имени", "Обработайте случай с отчеством (три слова): «Имя Отчество Фамилия» → «Фамилия И.О.» с инициалами.")}
{practice_card(
        "11-10",
        "Практика: перестановка имени и фамилии",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-10/index.html",
    )}

    <h2 id="itogi">Итоги главы</h2>
    {decision_map([
        ("Нужна пара «ключ → значение»?", "dict"),
        ("Нужны только уникальные значения, порядок не важен?", "set"),
        ("Нужен порядок, значения точно не изменятся?", "tuple"),
        ("Нужен порядок, и придётся менять содержимое?", "list"),
        ("Нужен неизменяемый набор уникальных значений?", "frozenset"),
        ("Нужны позиция и значение вместе при переборе?", "enumerate(...)"),
        ("Нужно перебрать несколько коллекций попарно?", "zip(...)"),
        ("Нужна новая коллекция, преобразованная из старой?", "comprehension"),
        ("Нужна независимая внешняя копия?", ".copy() / list(...) / [:]"),
        ("Нужна полностью независимая копия вложенных структур?", "copy.deepcopy(...) — с осторожностью"),
    ], title="Итоговый инструментарий главы 11", caption="Полная версия этой карты выбора — в §11.22")}

    {summary_box("Что мы узнали в этой главе", [
        "<strong>Список</strong> (<code class=\"inline\">list</code>) — упорядоченная, "
        "изменяемая коллекция в <code class=\"inline\">[]</code>: индексы, срезы, "
        "append/extend/insert, remove/pop/clear.",
        "<strong>Кортеж</strong> (<code class=\"inline\">tuple</code>) — как список, но "
        "неизменяемый, в <code class=\"inline\">()</code>: packing/unpacking, звёздочная "
        "распаковка, кортеж из одного элемента требует запятой.",
        "<strong>Множество</strong> (<code class=\"inline\">set</code>) — уникальные значения "
        "без позиций, в <code class=\"inline\">{}</code> (но <code class=\"inline\">{}</code> без "
        "содержимого — это dict, а не set!): union/intersection/difference/symmetric_difference.",
        "<strong>Словарь</strong> (<code class=\"inline\">dict</code>) — пары «ключ: значение», "
        "сохраняет порядок вставки, доступ по ключу, а не по позиции.",
        "<code class=\"inline\">b = a</code> для изменяемых объектов создаёт ВТОРОЕ ИМЯ того же "
        "объекта (aliasing), а не копию — для копии нужен <code class=\"inline\">.copy()</code>, "
        "а для вложенных структур — <code class=\"inline\">copy.deepcopy()</code>.",
        "Хешируемыми (и годными в качестве ключей словаря или элементов множества) бывают только "
        "неизменяемые типы: числа, строки, кортежи из хешируемых элементов, frozenset.",
        "Генератор списков <code class=\"inline\">[выражение for элемент in коллекция]</code> — "
        "компактная альтернатива циклу с <code class=\"inline\">append()</code>, но не замена "
        "циклу везде, где нужна более сложная логика.",
        "Выбор структуры данных — это в первую очередь вопрос к задаче («нужен ли порядок?», "
        "«нужны ли уникальные значения?», «нужен ли ключ?»), а не вопрос синтаксиса.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — перестановка имени и фамилии",
        description="Итоговый мини-проект главы 11: split(), распаковка списков — и полные итоги главы про коллекции.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Перестановка имени", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Мини-проект — перестановка имени и фамилии",
        lede="Собираем split(), распаковку и строки из главы 8 в одной короткой, но полезной "
        "программе — и подводим полные итоги главы.",
        body_html=body,
        sidebar_groups=sidebar("11-10-mini-proekt-perestanovka-itogi.html"),
        nav=PageNav(
            prev_href="11-26-mini-proekty-kollekcii.html",
            prev_label="Мини-проекты с коллекциями",
            next_href="../glava-12/index.html",
            next_label="Глава 12: Множество увлекательных мини-проектов",
        ),
    )
    write("11-10-mini-proekt-perestanovka-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_11()
    build_01()
    build_02()
    build_12()
    build_13()
    build_14()
    build_03()
    build_15()
    build_16()
    build_17()
    build_04()
    build_05()
    build_06()
    build_18()
    build_07()
    build_19()
    build_08()
    build_20()
    build_21()
    build_22()
    build_09()
    build_23()
    build_24()
    build_25()
    build_26()
    build_10()
