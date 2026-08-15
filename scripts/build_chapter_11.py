#!/usr/bin/env python3
"""Строит Главу 11: «Очень много информации!» (site/chapters/glava-11/)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    classic_vs_modern,
    code_block,
    exercise,
    local_required_card,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-11"

PAGES = [
    ("index.html", "Обзор главы"),
    ("11-01-spiski-osnovy.html", "Списки: основы"),
    ("11-02-srezy-spiskov.html", "Срезы списков"),
    ("11-03-operacii-so-spiskami.html", "Мощные операции со списками"),
    ("11-04-eshche-o-spiskah.html", "Ещё больше о списках"),
    ("11-05-mini-proekt-zvezda.html", "Мини-проект: разноцветная звезда"),
    ("11-06-kortezhi.html", "Кортежи"),
    ("11-07-mnozhestva.html", "Множества"),
    ("11-08-slovari.html", "Словари"),
    ("11-09-mini-proekt-cveta.html", "Мини-проект: бесконечные цвета"),
    ("11-10-mini-proekt-perestanovka-itogi.html", "Мини-проект: перестановка имени и итоги"),
]

LESSON_IDS = ["11-01", "11-02", "11-03", "11-04", "11-05", "11-06", "11-07", "11-08", "11-09", "11-10"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 11 · Данные", items),
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
        chapter_num=11,
        baseline_page=223,
        title="Очень много информации!",
        description="Списки, кортежи, множества и словари — четыре способа хранить сразу много данных.",
        meta_items=["⏱ ~3–4 часа", "📦 list, tuple, set, dict", "📓 10 ноутбуков практики"],
        sections=[
            ChapterSectionLink("11.1", "Храним больше одного значения. Списки", "11-01-spiski-osnovy.html", "223"),
            ChapterSectionLink("11.2", "Делаем срез списка!", "11-02-srezy-spiskov.html", "227"),
            ChapterSectionLink("11.3", "Мощные операции со списками!", "11-03-operacii-so-spiskami.html", "228"),
            ChapterSectionLink("11.4", "Ещё больше интересного со списками!", "11-04-eshche-o-spiskah.html", "235"),
            ChapterSectionLink("11.5", "Мини-проект — автоматическая разноцветная звезда", "11-05-mini-proekt-zvezda.html", "238"),
            ChapterSectionLink("11.6", "Кортежи", "11-06-kortezhi.html", "240"),
            ChapterSectionLink("11.7", "Множества", "11-07-mnozhestva.html", "244"),
            ChapterSectionLink("11.8", "Словари", "11-08-slovari.html", "247"),
            ChapterSectionLink("11.9", "Мини-проект — бесконечные цвета", "11-09-mini-proekt-cveta.html", "252"),
            ChapterSectionLink("11.10", "Мини-проект — перестановка имени и фамилии", "11-10-mini-proekt-perestanovka-itogi.html", "255"),
            ChapterSectionLink("", "Итоги", "11-10-mini-proekt-perestanovka-itogi.html#itogi", "258"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Храним больше одного значения</h2>
    <p>До сих пор каждая переменная хранила одно значение. Но что, если нужно хранить сразу
    список покупок, имена всех игроков или очки за каждый уровень? Для этого в Python есть
    четыре встроенные <strong>коллекции</strong> — списки, кортежи, множества и словари. Начнём
    с самой универсальной — списков.</p>

    <h2>Списки</h2>
    <p><strong>Список</strong> (<code class="inline">list</code>) — упорядоченная коллекция
    значений в квадратных скобках через запятую:</p>
    {code_block("spiski.py", 'fruits = ["яблоко", "банан", "вишня"]\nprint(fruits)\nprint(type(fruits))\n')}
    <p>Список может хранить значения разных типов одновременно, хотя на практике чаще хранят
    значения одного вида:</p>
    {code_block("smeshannyj_spisok.py", 'smeshannyj = ["Cartesian", 5, 3.14, True]\nprint(smeshannyj)\n')}

    <h2>Доступ к значениям списка</h2>
    <p>Как и у строк (глава 8), у элементов списка есть индексы, начиная с нуля:</p>
    {code_block("dostup_k_spisku.py", 'fruits = ["яблоко", "банан", "вишня"]\nprint(fruits[0])    # яблоко\nprint(fruits[-1])   # вишня — последний элемент\n')}

    {practice_card(
        "11-01",
        "Практика: создание списков и доступ по индексу",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-01/index.html",
    )}
    """
    out = render_page(
        page_title="Списки: основы",
        description="Введение в списки Python: создание и доступ к элементам по индексу.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Списки: основы", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Храним больше одного значения",
        lede="Списки — самая универсальная коллекция Python: упорядоченный набор значений в "
        "одной переменной.",
        body_html=body,
        sidebar_groups=sidebar("11-01-spiski-osnovy.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="11-02-srezy-spiskov.html", next_label="Срезы списков"),
    )
    write("11-01-spiski-osnovy.html", out)


def build_02() -> None:
    body = f"""
    <p>Срезы списков работают точно так же, как срезы строк из главы 8:</p>
    {code_block(
        "srezy_spiskov.py",
        'chisla = [10, 20, 30, 40, 50]\n'
        "print(chisla[1:3])    # [20, 30]\n"
        "print(chisla[:2])     # [10, 20]\n"
        "print(chisla[2:])     # [30, 40, 50]\n"
        "print(chisla[::-1])   # [50, 40, 30, 20, 10] — развёрнутый список\n",
    )}
    {callout(
        "tip",
        "Срез списка — это новый список",
        "Как и срез строки, срез списка возвращает <strong>новый</strong> список, не изменяя "
        "исходный.",
    )}

    {practice_card(
        "11-02",
        "Практика: срезы списков",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-02/index.html",
    )}
    """
    out = render_page(
        page_title="Делаем срез списка!",
        description="Срезы списков в Python — та же логика, что и срезы строк.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Срезы списков", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Делаем срез списка!",
        lede="Срезы списков работают точно так же, как срезы строк, — уже знакомая логика в "
        "новом контексте.",
        body_html=body,
        sidebar_groups=sidebar("11-02-srezy-spiskov.html"),
        nav=PageNav(prev_href="11-01-spiski-osnovy.html", prev_label="Списки: основы", next_href="11-03-operacii-so-spiskami.html", next_label="Мощные операции со списками"),
    )
    write("11-02-srezy-spiskov.html", out)


def build_03() -> None:
    body = f"""
    <p>У списков (в отличие от строк) есть методы, которые <strong>изменяют сам список</strong>
    — списки, в отличие от строк, изменяемы.</p>

    <h2>Копирование и добавление</h2>
    {code_block("kopirovanie.py", 'original = [1, 2, 3]\nkopiya = original.copy()\nkopiya.append(4)\nprint(original)  # [1, 2, 3] — не изменился\nprint(kopiya)    # [1, 2, 3, 4]\n')}
    {callout(
        "warning",
        "kopiya = original — это не копия!",
        "<code class=\"inline\">kopiya = original</code> создаёт вторую переменную, "
        "указывающую <strong>на тот же самый</strong> список — изменение через одну переменную "
        "видно и через другую. Чтобы получить настоящую независимую копию, нужен "
        "<code class=\"inline\">.copy()</code> (или срез <code class=\"inline\">original[:]</code>).",
    )}

    <h2>Подсчёт и очистка</h2>
    {code_block("podschet.py", 'chisla = [1, 2, 2, 3, 2]\nprint(chisla.count(2))   # 3 — сколько раз встречается 2\nchisla.clear()\nprint(chisla)             # [] — список пуст\n')}

    <h2>Конкатенация</h2>
    {code_block("konkatenaciya_spiskov.py", 'a = [1, 2]\nb = [3, 4]\nprint(a + b)   # [1, 2, 3, 4]\n')}

    <h2>Поиск внутри списка</h2>
    {code_block("poisk.py", 'fruits = ["яблоко", "банан", "вишня"]\nprint("банан" in fruits)         # True\nprint(fruits.index("вишня"))      # 2 — индекс элемента\n')}

    <h2>Добавление и удаление элементов</h2>
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

    <h2>Разворот и сортировка</h2>
    {code_block("razvorot_sortirovka.py", 'chisla = [3, 1, 4, 1, 5]\nchisla.sort()\nprint(chisla)      # [1, 1, 3, 4, 5]\nchisla.reverse()\nprint(chisla)      # [5, 4, 3, 1, 1]\n')}

    {practice_card(
        "11-03",
        "Практика: операции со списками",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-03/index.html",
    )}
    """
    out = render_page(
        page_title="Мощные операции со списками!",
        description="Методы списков: copy, append, count, clear, конкатенация, index, insert, remove, pop, sort, reverse.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Операции со списками", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Мощные операции со списками!",
        lede="Списки изменяемы — у них есть целый набор методов для добавления, удаления, "
        "поиска и сортировки.",
        body_html=body,
        sidebar_groups=sidebar("11-03-operacii-so-spiskami.html"),
        nav=PageNav(prev_href="11-02-srezy-spiskov.html", prev_label="Срезы списков", next_href="11-04-eshche-o-spiskah.html", next_label="Ещё больше о списках"),
    )
    write("11-03-operacii-so-spiskami.html", out)


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
        "\"хуже\", выбирайте то, что легче прочитать.",
    )

    body = f"""
    <p>Ещё несколько приёмов, которые часто пригождаются при работе со списками.</p>

    <h2>len(), min(), max(), sum()</h2>
    {code_block("vstroennye_funkcii.py", "chisla = [4, 8, 15, 16, 23, 42]\nprint(len(chisla))   # 6 — количество элементов\nprint(min(chisla))   # 4\nprint(max(chisla))   # 42\nprint(sum(chisla))   # 108\n")}

    <h2>Перебор списка циклом for</h2>
    {code_block("perebor_spiska.py", 'fruits = ["яблоко", "банан", "вишня"]\nfor fruit in fruits:\n    print(fruit)\n')}

    <h2>Списки списков (вложенные списки)</h2>
    <p>Элементом списка может быть другой список — так получаются таблицы (матрицы):</p>
    {code_block("vlozhennye_spiski.py", "matrix = [[1, 2, 3], [4, 5, 6]]\nprint(matrix[0])      # [1, 2, 3] — первая строка\nprint(matrix[0][1])   # 2 — второй элемент первой строки\n")}

    {cvm}

    {practice_card(
        "11-04",
        "Практика: len/min/max/sum, вложенные списки, list comprehension",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-04/index.html",
    )}
    """
    out = render_page(
        page_title="Ещё больше интересного со списками!",
        description="len, min, max, sum, вложенные списки и генераторы списков (list comprehension).",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Ещё о списках", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Ещё больше интересного со списками!",
        lede="Полезные встроенные функции, вложенные списки и более компактный способ строить "
        "новые списки.",
        body_html=body,
        sidebar_groups=sidebar("11-04-eshche-o-spiskah.html"),
        nav=PageNav(prev_href="11-03-operacii-so-spiskami.html", prev_label="Операции со списками", next_href="11-05-mini-proekt-zvezda.html", next_label="Мини-проект: разноцветная звезда"),
    )
    write("11-04-eshche-o-spiskah.html", out)


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
    out = render_page(
        page_title="Мини-проект — автоматическая разноцветная звезда",
        description="Комбинируем списки с Turtle: звезда, где каждый луч своего цвета.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Разноцветная звезда", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Мини-проект — автоматическая разноцветная звезда",
        lede="Список цветов + цикл + Turtle — звезда, где каждый луч своего цвета.",
        body_html=body,
        sidebar_groups=sidebar("11-05-mini-proekt-zvezda.html"),
        nav=PageNav(prev_href="11-04-eshche-o-spiskah.html", prev_label="Ещё о списках", next_href="11-06-kortezhi.html", next_label="Кортежи"),
    )
    write("11-05-mini-proekt-zvezda.html", out)


def build_06() -> None:
    body = f"""
    <p><strong>Кортеж</strong> (<code class="inline">tuple</code>) — почти то же самое, что
    список, но в круглых скобках и с одним принципиальным отличием: кортежи
    <strong>неизменяемы</strong> — после создания их нельзя изменить.</p>
    {code_block("kortezhi.py", 'coords = (10, 20)\nprint(coords)\nprint(coords[0])   # 10 — индексация работает как у списков\n')}
    {code_block("kortezh_nelzya_menyat.py", "coords = (10, 20)\ncoords[0] = 99   # TypeError: 'tuple' object does not support item assignment\n")}

    <h2>Зачем нужны неизменяемые коллекции?</h2>
    <p>Неизменяемость — не недостаток, а гарантия: если вы передаёте координаты точки в другую
    часть программы как кортеж, вы точно знаете, что их никто случайно не изменит. Кортежи часто
    используют для координат, RGB-цветов и других «пакетов» значений, которые логически
    представляют собой единое целое.</p>

    <h2>Распаковка кортежа</h2>
    {code_block("raspakovka.py", "coords = (10, 20)\nx, y = coords\nprint(x, y)   # 10 20\n")}
    {callout(
        "tip",
        "Мы уже пользовались распаковкой",
        "<code class=\"inline\">artist.position()</code> в модуле turtle возвращает именно "
        "такой кортеж <code class=\"inline\">(x, y)</code> — можно сразу распаковать его в две "
        "переменные.",
    )}

    {practice_card(
        "11-06",
        "Практика: кортежи и распаковка",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-06/index.html",
    )}
    """
    out = render_page(
        page_title="Кортежи",
        description="Кортежи (tuple) — неизменяемые последовательности в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Кортежи", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Кортежи",
        lede="Почти список, но неизменяемый — и именно поэтому иногда более подходящий выбор.",
        body_html=body,
        sidebar_groups=sidebar("11-06-kortezhi.html"),
        nav=PageNav(prev_href="11-05-mini-proekt-zvezda.html", prev_label="Разноцветная звезда", next_href="11-07-mnozhestva.html", next_label="Множества"),
    )
    write("11-06-kortezhi.html", out)


def build_07() -> None:
    body = f"""
    <p><strong>Множество</strong> (<code class="inline">set</code>) — коллекция в фигурных
    скобках, у которой два ключевых отличия от списка: элементы в ней не повторяются, а порядок
    не гарантирован.</p>
    {code_block("mnozhestva.py", 'chisla = {1, 2, 2, 3, 3, 3}\nprint(chisla)   # {1, 2, 3} — повторы исчезли сами\n')}

    <h2>Зачем нужны множества?</h2>
    <p>Два самых частых случая: быстро убрать повторы из списка и быстро проверить, есть ли
    значение в коллекции (проверка через <code class="inline">in</code> у множества намного
    быстрее, чем у длинного списка).</p>
    {code_block("primenenie_mnozhestv.py", 'spisok_s_povtorami = [1, 2, 2, 3, 1, 4]\nunikalnye = set(spisok_s_povtorami)\nprint(unikalnye)   # {1, 2, 3, 4}\n')}

    <h2>Операции над множествами</h2>
    {code_block(
        "operacii_mnozhestv.py",
        "a = {1, 2, 3}\n"
        "b = {2, 3, 4}\n\n"
        "print(a | b)   # объединение: {1, 2, 3, 4}\n"
        "print(a & b)   # пересечение: {2, 3}\n"
        "print(a - b)   # разность: {1}\n",
    )}

    {practice_card(
        "11-07",
        "Практика: множества и их операции",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-07/index.html",
    )}
    """
    out = render_page(
        page_title="Множества",
        description="Множества (set) в Python: уникальные значения и операции объединения/пересечения/разности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Множества", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Множества",
        lede="Коллекция без повторов — быстрый способ убрать дубликаты и сравнивать наборы "
        "значений.",
        body_html=body,
        sidebar_groups=sidebar("11-07-mnozhestva.html"),
        nav=PageNav(prev_href="11-06-kortezhi.html", prev_label="Кортежи", next_href="11-08-slovari.html", next_label="Словари"),
    )
    write("11-07-mnozhestva.html", out)


def build_08() -> None:
    body = f"""
    <p><strong>Словарь</strong> (<code class="inline">dict</code>) — самая гибкая коллекция:
    хранит пары «ключ — значение», а не просто значения по порядку. Вместо числового индекса
    доступ идёт по ключу — обычно строке.</p>
    {code_block(
        "slovari.py",
        "student = {\n"
        '    "name": "Cartesian",\n'
        '    "age": 12,\n'
        '    "city": "Москва",\n'
        "}\n"
        'print(student["name"])   # Cartesian\n',
    )}

    <h2>Добавление и изменение значений</h2>
    {code_block(
        "izmenenie_slovarya.py",
        'student["age"] = 13         # изменить существующее значение\n'
        'student["grade"] = "7 класс" # добавить новый ключ\n'
        "print(student)\n",
    )}

    <h2>Перебор словаря</h2>
    {code_block(
        "perebor_slovarya.py",
        "for key, value in student.items():\n"
        '    print(f"{key}: {value}")\n',
    )}

    <h2>Проверка наличия ключа</h2>
    {code_block("proverka_klyucha.py", 'print("name" in student)      # True\nprint("phone" in student)     # False\n')}

    {callout(
        "warning",
        "KeyError — обращение к несуществующему ключу",
        "<code class=\"inline\">student[\"phone\"]</code>, если такого ключа нет, вызовет "
        "<code class=\"inline\">KeyError</code>. Более безопасный способ — метод "
        "<code class=\"inline\">student.get(\"phone\")</code>, который просто вернёт "
        "<code class=\"inline\">None</code> вместо ошибки.",
    )}

    {practice_card(
        "11-08",
        "Практика: словари — создание, изменение, перебор",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-08/index.html",
    )}
    """
    out = render_page(
        page_title="Словари",
        description="Словари (dict) в Python: пары ключ-значение, добавление, изменение и перебор.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Словари", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Словари",
        lede="Самая гибкая встроенная коллекция Python — доступ по ключу вместо числового "
        "индекса.",
        body_html=body,
        sidebar_groups=sidebar("11-08-slovari.html"),
        nav=PageNav(prev_href="11-07-mnozhestva.html", prev_label="Множества", next_href="11-09-mini-proekt-cveta.html", next_label="Мини-проект: бесконечные цвета"),
    )
    write("11-08-slovari.html", out)


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
    out = render_page(
        page_title="Мини-проект — бесконечные цвета",
        description="Словарь как карта соответствий — раскрашиваем фигуры Turtle через словарь.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Бесконечные цвета", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Мини-проект — бесконечные цвета",
        lede="Словарь как «переводчик» — от слова к конкретному цвету Turtle.",
        body_html=body,
        sidebar_groups=sidebar("11-09-mini-proekt-cveta.html"),
        nav=PageNav(prev_href="11-08-slovari.html", prev_label="Словари", next_href="11-10-mini-proekt-perestanovka-itogi.html", next_label="Перестановка имени и итоги"),
    )
    write("11-09-mini-proekt-cveta.html", out)


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
        "про списки, можно распаковывать его так же, как распаковывали кортежи в разделе 11.6.",
    )}
    {exercise(3, "Три части имени", "Обработайте случай с отчеством (три слова): «Имя Отчество Фамилия» → «Фамилия И.О.» с инициалами.")}
{practice_card(
        "11-10",
        "Практика: перестановка имени и фамилии",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/11-10/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "<strong>Список</strong> (<code class=\"inline\">list</code>) — упорядоченная, "
        "изменяемая коллекция значений в <code class=\"inline\">[]</code>.",
        "<strong>Кортеж</strong> (<code class=\"inline\">tuple</code>) — как список, но "
        "неизменяемый, в <code class=\"inline\">()</code>.",
        "<strong>Множество</strong> (<code class=\"inline\">set</code>) — коллекция без "
        "повторов и без гарантированного порядка, в <code class=\"inline\">{}</code>.",
        "<strong>Словарь</strong> (<code class=\"inline\">dict</code>) — пары «ключ: значение», "
        "тоже в <code class=\"inline\">{}</code>, но с двоеточиями.",
        "У списков десятки полезных методов: <code class=\"inline\">append, insert, remove, "
        "pop, sort, reverse, index, count</code> и другие.",
        "Генератор списков <code class=\"inline\">[выражение for элемент in коллекция]</code> — "
        "компактная альтернатива циклу с <code class=\"inline\">append()</code>.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — перестановка имени и фамилии",
        description="Итоговый мини-проект главы 11: split(), распаковка списков — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 11", "index.html"), ("Перестановка имени", "")],
        kicker="Глава 11 · Очень много информации!",
        h1="Мини-проект — перестановка имени и фамилии",
        lede="Собираем split(), распаковку и строки из главы 8 в одной короткой, но полезной "
        "программе — и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("11-10-mini-proekt-perestanovka-itogi.html"),
        nav=PageNav(prev_href="11-09-mini-proekt-cveta.html", prev_label="Бесконечные цвета", next_href="../glava-12/index.html", next_label="Глава 12: Множество увлекательных мини-проектов"),
    )
    write("11-10-mini-proekt-perestanovka-itogi.html", out)


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
