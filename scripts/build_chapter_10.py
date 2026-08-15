#!/usr/bin/env python3
"""Строит Главу 10: «Немного автоматизации!» (site/chapters/glava-10/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-10"

PAGES = [
    ("index.html", "Обзор главы"),
    ("10-01-cikly-for.html", "Волшебные циклы! Циклы for"),
    ("10-02-if-vlozhennye-cikly.html", "if внутри циклов, вложенные циклы"),
    ("10-03-perebor-strok-while.html", "Перебор строк и циклы while"),
    ("10-04-break-continue.html", "break и continue"),
    ("10-05-mini-proekt-ugadaj-v2.html", "Мини-проект: «Угадай число», версия 2"),
    ("10-06-avtomatiziruem-figury.html", "Автоматизируем квадрат и любую фигуру"),
    ("10-07-avtomatiziruem-mandalu.html", "Автоматически рисуем мандалу"),
    ("10-08-spirali-itogi.html", "Спирали из дуг и итоги"),
]

LESSON_IDS = ["10-01", "10-02", "10-03", "10-04", "10-05", "10-06", "10-07", "10-08"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 10 · Циклы", items),
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
        chapter_num=10,
        baseline_page=195,
        title="Немного автоматизации!",
        description="Циклы for и while, break/continue — и наконец-то настоящая автоматизация всех фигур из глав 6-7.",
        meta_items=["⏱ ~3 часа", "🔁 for / while", "📓 8 ноутбуков практики"],
        sections=[
            ChapterSectionLink("10.1", "Волшебные циклы! Циклы for", "10-01-cikly-for.html", "195"),
            ChapterSectionLink("10.2", "Условия if внутри циклов for", "10-02-if-vlozhennye-cikly.html", "200"),
            ChapterSectionLink("", "Вложенные циклы for", "10-02-if-vlozhennye-cikly.html#vlozhennye", "201"),
            ChapterSectionLink("10.3", "Перебор строк", "10-03-perebor-strok-while.html", "204"),
            ChapterSectionLink("", "Циклы while", "10-03-perebor-strok-while.html#while", "205"),
            ChapterSectionLink("10.4", "Прервать миссию! break и continue", "10-04-break-continue.html", "207"),
            ChapterSectionLink("10.5", "Мини-проект — «Угадай число», версия 2", "10-05-mini-proekt-ugadaj-v2.html", "209"),
            ChapterSectionLink("10.6", "Мини-проект — автоматизируем квадрат", "10-06-avtomatiziruem-figury.html", "211"),
            ChapterSectionLink("", "Автоматизируем любую простую фигуру", "10-06-avtomatiziruem-figury.html#lyubaya-figura", "212"),
            ChapterSectionLink("10.7", "Мини-проект — автоматически рисуем мандалу", "10-07-avtomatiziruem-mandalu.html", "216"),
            ChapterSectionLink("10.8", "Мини-проект — спирали из дуг", "10-08-spirali-itogi.html", "218"),
            ChapterSectionLink("", "Итоги", "10-08-spirali-itogi.html#itogi", "221"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    cvm = classic_vs_modern(
        "Квадрат из главы 6: 8 строк → 2 строки",
        "Без цикла (глава 6)",
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)",
        "С циклом for",
        "for _ in range(4):\n"
        "    artist.forward(100)\n"
        "    artist.right(90)",
        "цикл <code class=\"inline\">for</code>. Он не «современнее» в смысле версии Python — "
        "циклы существуют с самых первых версий языка, — но именно ради него стоило дочитать "
        "до этой главы: то же самое поведение, в 4 раза короче, и легко изменить число повторов "
        "одной цифрой.",
    )

    body = f"""
    <h2>Волшебные циклы!</h2>
    <p>Вспомните квадрат и шестиугольник из главы 6 — каждый состоял из одинаковых блоков
    команд, повторённых вручную. <strong>Циклы</strong> — это способ сказать Python «повтори
    это N раз» вместо того, чтобы копировать код руками.</p>

    <h2>Циклы for</h2>
    <p>Самый частый вид цикла в Python — <code class="inline">for</code>. Вместе с
    <code class="inline">range()</code> он умеет повторить блок кода заданное число раз:</p>
    {code_block("cikl_for.py", 'for i in range(5):\n    print(i)\n')}
    <p><code class="inline">range(5)</code> генерирует числа от 0 до 4 (пять чисел, не включая
    5) — <code class="inline">i</code> на каждом шаге принимает следующее из них.</p>

    {callout(
        "info",
        "range() с разными аргументами",
        "<code class=\"inline\">range(5)</code> — от 0 до 4. "
        "<code class=\"inline\">range(2, 8)</code> — от 2 до 7. "
        "<code class=\"inline\">range(0, 10, 2)</code> — от 0 до 8 с шагом 2: 0, 2, 4, 6, 8.",
    )}

    <h2>Когда переменная цикла не нужна</h2>
    <p>Если само число повторов важно, а не значение счётчика — по традиции его называют
    <code class="inline">_</code> (нижнее подчёркивание), сигнализируя «это значение
    сознательно не используется»:</p>
    {cvm}

    {practice_card(
        "10-01",
        "Практика: цикл for и range()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-01/index.html",
    )}
    """
    out = render_page(
        page_title="Волшебные циклы! Циклы for",
        description="Введение в циклы: for и range() — автоматизация повторяющихся действий.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Циклы for", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Волшебные циклы! Циклы for",
        lede="Наконец-то настоящая автоматизация: вместо повторения кода вручную — просим "
        "Python повторить его самостоятельно.",
        body_html=body,
        sidebar_groups=sidebar("10-01-cikly-for.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="10-02-if-vlozhennye-cikly.html", next_label="if внутри циклов, вложенные циклы"),
    )
    write("10-01-cikly-for.html", out)


def build_02() -> None:
    body = f"""
    <h2>Условия if внутри циклов for</h2>
    <p><code class="inline">if</code> из главы 9 прекрасно работает внутри цикла — на каждом
    шаге можно принимать своё решение:</p>
    {code_block("if_v_cikle.py", "for number in range(1, 11):\n    if number % 2 == 0:\n        print(number, \"— чётное\")\n")}

    <h2 id="vlozhennye">Вложенные циклы for</h2>
    <p>Цикл можно поместить внутрь другого цикла — тогда внутренний цикл выполняется полностью
    на каждом шаге внешнего:</p>
    {code_block(
        "vlozhennye_cikly.py",
        "for row in range(3):\n"
        "    for col in range(4):\n"
        '        print(f"({row}, {col})", end=" ")\n'
        "    print()  # новая строка после каждого ряда\n",
    )}
    {callout(
        "tip",
        "Сколько раз выполнится внутренний цикл?",
        "Внешний цикл выполняется 3 раза, внутренний — 4 раза <em>на каждом</em> шаге внешнего "
        "— итого <code class=\"inline\">print(...)</code> внутри сработает "
        "<code class=\"inline\">3 * 4 = 12</code> раз. Вложенные циклы — частая причина "
        "неожиданно долгого выполнения, если не следить за их количеством.",
    )}

    {practice_card(
        "10-02",
        "Практика: условия и вложенные циклы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-02/index.html",
    )}
    """
    out = render_page(
        page_title="Условия if внутри циклов for, вложенные циклы",
        description="Комбинируем if с for и учимся вкладывать циклы друг в друга.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("if и вложенные циклы", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Условия if внутри циклов for",
        lede="Циклы и условия отлично работают вместе — а циклы можно вкладывать друг в друга.",
        body_html=body,
        sidebar_groups=sidebar("10-02-if-vlozhennye-cikly.html"),
        nav=PageNav(prev_href="10-01-cikly-for.html", prev_label="Циклы for", next_href="10-03-perebor-strok-while.html", next_label="Перебор строк и циклы while"),
    )
    write("10-02-if-vlozhennye-cikly.html", out)


def build_03() -> None:
    body = f"""
    <h2>Перебор строк</h2>
    <p>Строка — это последовательность символов (глава 8), а значит, <code class="inline">for</code>
    умеет перебирать и её — символ за символом, без индексов:</p>
    {code_block("perebor_strok.py", 'for letter in "Python":\n    print(letter)\n')}

    <h2 id="while">Циклы while</h2>
    <p>В отличие от <code class="inline">for</code>, который повторяется заданное число раз,
    <code class="inline">while</code> повторяется, <strong>пока истинно условие</strong> — сколько
    раз потребуется, заранее неизвестно:</p>
    {code_block(
        "cikl_while.py",
        "count = 0\n"
        "while count < 5:\n"
        "    print(count)\n"
        "    count += 1\n",
    )}
    {callout(
        "warning",
        "Бесконечный цикл",
        "Если забыть <code class=\"inline\">count += 1</code>, условие "
        "<code class=\"inline\">count &lt; 5</code> останется истинным навсегда — программа "
        "зависнет в <strong>бесконечном цикле</strong>. Всегда проверяйте, что внутри "
        "<code class=\"inline\">while</code> есть шаг, который в итоге сделает условие ложным.",
    )}

    {callout(
        "info",
        "for или while?",
        "Используйте <code class=\"inline\">for</code>, когда число повторов известно заранее "
        "(«нарисовать 4 стороны квадрата»). Используйте <code class=\"inline\">while</code>, "
        "когда неизвестно («повторять, пока пользователь не угадает число»).",
    )}

    {practice_card(
        "10-03",
        "Практика: перебор строк и цикл while",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-03/index.html",
    )}
    """
    out = render_page(
        page_title="Перебор строк и циклы while",
        description="Перебор символов строки циклом for и знакомство с циклом while.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Строки и while", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Перебор строк",
        lede="for умеет перебирать не только числа — а while повторяет действие, пока условие "
        "остаётся истинным.",
        body_html=body,
        sidebar_groups=sidebar("10-03-perebor-strok-while.html"),
        nav=PageNav(prev_href="10-02-if-vlozhennye-cikly.html", prev_label="if и вложенные циклы", next_href="10-04-break-continue.html", next_label="break и continue"),
    )
    write("10-03-perebor-strok-while.html", out)


def build_04() -> None:
    body = f"""
    <p>Иногда нужно выйти из цикла раньше времени или пропустить один шаг, не завершая цикл
    целиком — для этого есть два ключевых слова.</p>

    <h2><code class="inline">break</code> — прервать цикл полностью</h2>
    {code_block(
        "break.py",
        "for number in range(1, 100):\n"
        "    if number == 5:\n"
        "        break  # цикл останавливается насовсем\n"
        "    print(number)\n",
    )}
    <p>Выведет только 1, 2, 3, 4 — как только <code class="inline">number</code> становится
    равным 5, цикл прерывается, не дожидаясь оставшихся 94 значений <code class="inline">range()</code>.</p>

    <h2><code class="inline">continue</code> — пропустить этот шаг</h2>
    {code_block(
        "continue.py",
        "for number in range(1, 6):\n"
        "    if number == 3:\n"
        "        continue  # пропускаем оставшуюся часть тела цикла для этого шага\n"
        "    print(number)\n",
    )}
    <p>Выведет 1, 2, 4, 5 — число 3 пропущено, но цикл продолжается дальше, в отличие от
    <code class="inline">break</code>.</p>

    {callout(
        "tip",
        "break/continue работают и в while",
        "Оба ключевых слова работают одинаково в цикле <code class=\"inline\">while</code> — "
        "мы воспользуемся <code class=\"inline\">break</code> в следующем разделе, переписывая "
        "игру «Угадай число».",
    )}

    {practice_card(
        "10-04",
        "Практика: break и continue",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-04/index.html",
    )}
    """
    out = render_page(
        page_title="Прервать миссию! break и continue",
        description="Досрочное прерывание цикла (break) и пропуск шага (continue) в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("break и continue", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Прервать миссию! break и continue",
        lede="Два способа управлять циклом изнутри: остановить его совсем или пропустить один "
        "шаг.",
        body_html=body,
        sidebar_groups=sidebar("10-04-break-continue.html"),
        nav=PageNav(prev_href="10-03-perebor-strok-while.html", prev_label="Строки и while", next_href="10-05-mini-proekt-ugadaj-v2.html", next_label="«Угадай число», версия 2"),
    )
    write("10-04-break-continue.html", out)


def build_05() -> None:
    body = f"""
    <p>Помните игру «Угадай число» из главы 9? У неё была одна проблема — всего одна попытка.
    Теперь, вооружившись <code class="inline">while</code> и <code class="inline">break</code>,
    дадим игроку сколько угодно попыток.</p>
    {code_block(
        "ugadaj_chislo_v2.py",
        "import random\n\n"
        "zagadannoe = random.randint(1, 20)\n"
        "popytki = 0\n\n"
        "while True:\n"
        "    popytka = int(input(\"Угадайте число от 1 до 20: \"))\n"
        "    popytki += 1\n\n"
        "    if popytka == zagadannoe:\n"
        "        print(f\"Поздравляем, вы угадали за {popytki} попыток(ки)!\")\n"
        "        break\n"
        "    elif popytka < zagadannoe:\n"
        "        print(\"Загаданное число больше.\")\n"
        "    else:\n"
        "        print(\"Загаданное число меньше.\")\n",
    )}
    {callout(
        "info",
        "while True — намеренно бесконечный цикл",
        "<code class=\"inline\">while True:</code> создаёт цикл, который сам по себе никогда "
        "не остановится, — единственный выход из него: <code class=\"inline\">break</code> "
        "внутри. Это распространённый и совершенно нормальный приём, когда условие остановки "
        "естественнее проверить в середине цикла, а не в его начале.",
    )}
    {exercise(2, "Ограничение попыток", "Добавьте ограничение — не более 5 попыток; если игрок не угадал за 5 попыток, сообщите правильный ответ и завершите игру.")}

    {practice_card(
        "10-05",
        "Практика: «Угадай число» с неограниченными попытками",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-05/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — «Угадай число», версия 2",
        description="Переписываем игру «Угадай число» из главы 9, добавляя цикл и несколько попыток.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Угадай число v2", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — игра «Угадай число», версия 2",
        lede="Та же игра, что и в главе 9, — но теперь с неограниченным числом попыток, "
        "благодаря while и break.",
        body_html=body,
        sidebar_groups=sidebar("10-05-mini-proekt-ugadaj-v2.html"),
        nav=PageNav(prev_href="10-04-break-continue.html", prev_label="break и continue", next_href="10-06-avtomatiziruem-figury.html", next_label="Автоматизируем квадрат и любую фигуру"),
    )
    write("10-05-mini-proekt-ugadaj-v2.html", out)


def build_06() -> None:
    body = f"""
    <h2>Мини-проект — автоматизируем квадрат</h2>
    <p>Применим цикл к квадрату из главы 6 (мы уже видели этот пример в начале главы):</p>
    {code_block("avto_kvadrat.py", "for _ in range(4):\n    artist.forward(100)\n    artist.right(90)\n")}

    <h2 id="lyubaya-figura">Автоматизируем любую простую фигуру</h2>
    <p>Обобщим квадрат до функции-подобного шаблона, который рисует
    <strong>любой</strong> правильный многоугольник — вспомним формулу угла поворота из главы 6:
    <code class="inline">360 / количество_сторон</code>.</p>
    {code_block(
        "avto_lyubaya_figura.py",
        "storony = 8       # хотим восьмиугольник — просто меняем это число\n"
        "dlina = 60\n"
        "ugol = 360 / storony\n\n"
        "for _ in range(storony):\n"
        "    artist.forward(dlina)\n"
        "    artist.right(ugol)\n",
    )}
    {callout(
        "tip",
        "Одна переменная — любая фигура",
        "Поменяйте <code class=\"inline\">storony</code> на 3, 5, 10, 20 — программа "
        "автоматически нарисует треугольник, пятиугольник, десятиугольник или почти окружность, "
        "без единого изменения остального кода.",
    )}

    {local_required_card(
        "10-06",
        "Практика: автоматизируем фигуры циклом",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-06/index.html",
    )}
    """
    out = render_page(
        page_title="Автоматизируем квадрат и любую фигуру",
        description="Переписываем квадрат и любой правильный многоугольник из главы 6 с помощью цикла for.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Автоматизация фигур", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — автоматизируем рисование квадрата",
        lede="Возвращаемся к фигурам из главы 6 — на этот раз с циклами вместо ручного "
        "повторения.",
        body_html=body,
        sidebar_groups=sidebar("10-06-avtomatiziruem-figury.html"),
        nav=PageNav(prev_href="10-05-mini-proekt-ugadaj-v2.html", prev_label="Угадай число v2", next_href="10-07-avtomatiziruem-mandalu.html", next_label="Автоматически рисуем мандалу"),
    )
    write("10-06-avtomatiziruem-figury.html", out)


def build_07() -> None:
    body = f"""
    <p>В главе 6 мандала рисовалась циклом <code class="inline">while</code> с ручным
    увеличением угла. Теперь, когда мы понимаем оба вида циклов, перепишем её на
    <code class="inline">for</code> с <code class="inline">range()</code> — станет ещё короче:</p>
    {code_block(
        "avto_mandala.py",
        "shag_ugla = 10\n\n"
        "for ugol in range(0, 360, shag_ugla):\n"
        "    artist.setheading(ugol)\n"
        "    artist.forward(150)\n"
        "    artist.backward(150)\n",
    )}
    {callout(
        "info",
        "range() с тремя аргументами — то же, что и ручной while",
        "<code class=\"inline\">range(0, 360, shag_ugla)</code> генерирует именно те же числа, "
        "что мы получали вручную в главе 6: <code class=\"inline\">while ugol &lt; 360: ... ugol "
        "+= shag_ugla</code>. Цикл <code class=\"inline\">for</code> просто делает это короче "
        "и без риска забыть увеличить счётчик.",
    )}

    {local_required_card(
        "10-07",
        "Практика: мандала через for + range()",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-07/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — автоматически рисуем мандалу",
        description="Переписываем мандалу из главы 6 с циклом for вместо while.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Автоматическая мандала", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — автоматически рисуем мандалу",
        lede="Та же мандала, что и в главе 6, — но короче и понятнее благодаря range() с тремя "
        "аргументами.",
        body_html=body,
        sidebar_groups=sidebar("10-07-avtomatiziruem-mandalu.html"),
        nav=PageNav(prev_href="10-06-avtomatiziruem-figury.html", prev_label="Автоматизация фигур", next_href="10-08-spirali-itogi.html", next_label="Спирали из дуг и итоги"),
    )
    write("10-07-avtomatiziruem-mandalu.html", out)


def build_08() -> None:
    body = f"""
    <p>Финальный мини-проект главы: спираль из дуг — каждая следующая дуга немного больше
    предыдущей.</p>
    {code_block(
        "spirali_iz_dug.py",
        "radius = 5\n\n"
        "for _ in range(60):\n"
        "    artist.circle(radius, 90)   # дуга в четверть окружности\n"
        "    radius += 3                 # каждый раз чуть больше\n",
    )}
    {callout(
        "tip",
        "Изменение переменной внутри цикла — обычное дело",
        "В отличие от предыдущих примеров, здесь <code class=\"inline\">radius</code> меняется "
        "<em>на каждом шаге</em> цикла — это и создаёт эффект нарастающей спирали, а не "
        "повторяющегося узора.",
    )}
    {exercise(2, "Спираль из квадратов", "Замените дугу на маленький квадрат (цикл на 4 стороны) внутри внешнего цикла — получится спираль из уменьшающихся или увеличивающихся квадратов.")}
{local_required_card(
        "10-08",
        "Практика: спирали из дуг",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-08/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "<code class=\"inline\">for ... in range(n)</code> повторяет блок кода заданное число "
        "раз — и заменяет ручное копирование одинаковых строк.",
        "<code class=\"inline\">for</code> умеет перебирать не только числа, но и символы "
        "строки.",
        "<code class=\"inline\">while</code> повторяет действие, пока условие остаётся "
        "истинным — используется, когда число повторов заранее неизвестно.",
        "<code class=\"inline\">break</code> прерывает цикл полностью; "
        "<code class=\"inline\">continue</code> пропускает текущий шаг и переходит к "
        "следующему.",
        "Циклы можно вкладывать друг в друга — тогда внутренний цикл выполняется полностью на "
        "каждом шаге внешнего.",
        "Все фигуры из глав 6–7, нарисованные вручную, теперь можно записать в 2–4 строки с "
        "циклом.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — спирали из дуг",
        description="Итоговый мини-проект главы 10: спирали из дуг с растущим радиусом — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Спирали и итоги", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — спирали из дуг",
        lede="Завершаем главу узором, который меняется на каждом шаге цикла, — и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("10-08-spirali-itogi.html"),
        nav=PageNav(prev_href="10-07-avtomatiziruem-mandalu.html", prev_label="Автоматическая мандала", next_href="../glava-11/index.html", next_label="Глава 11: Очень много информации!"),
    )
    write("10-08-spirali-itogi.html", out)


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
