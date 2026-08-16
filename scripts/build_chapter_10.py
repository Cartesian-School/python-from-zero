#!/usr/bin/env python3
"""Строит Главу 10: «Немного автоматизации!» (site/chapters/glava-10/).

Curriculum v2: от короткой главы про for/while и три мини-проекта до
полноценного курса циклов и автоматизации — повторение как третья
структура алгоритма (после последовательности и ветвления из главы 9),
терминология цикла (тело/итерация/условие/счётчик/состояние) вводится
постепенно и наглядно, range() разобран подробно (три сигнатуры, почему
stop не включён — через связь со срезами из главы 8, шаг и отрицательный
шаг), канонические flowchart'ы for/while/break/continue/loop-else,
итерируемость и enumerate(), счётчик и накопитель, вложенные циклы,
поиск/фильтрация/суммирование, проверка ввода, отдельный урок отладки
циклов (10 именованных типов ошибок), и наконец настоящая автоматизация
всех фигур из глав 6-7 через Turtle — с РЕАЛЬНО выполненными картинками
(см. chapter_10_examples.py + generate_chapter_10_outputs.py, тот же
пайплайн, что и в главах 6-7), а не нарисованными вручную.

Существующие маршруты и практики (10-01..10-08) сохранены и расширены на
месте; новый материал — новые страницы (10-09..10-15) и новые ID практик
(10-09..10-24), без переиспользования занятых ID.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_10_examples import EXAMPLES
from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    capability_map,
    classic_vs_modern,
    code_block,
    comparison_table,
    decision_map,
    exercise,
    flowchart,
    for_loop_flowchart,
    local_required_card,
    loop_else_flowchart,
    break_continue_flowchart,
    loop_preview_diagram,
    math_formula,
    nested_loop_grid,
    practice_card,
    range_diagram,
    render_chapter_opener,
    render_page,
    summary_box,
    timeline_diagram,
    while_loop_flowchart,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-10"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Обзор главы"),
    ("10-01-cikly-for.html", "Повторение и первый цикл for"),
    ("10-09-range-podrobno.html", "range() подробно: старт, стоп, шаг"),
    ("10-10-enumerate-i-nakoplenie.html", "Индекс, значение, enumerate() и накопление"),
    ("10-02-if-vlozhennye-cikly.html", "if внутри циклов, вложенные циклы"),
    ("10-03-perebor-strok-while.html", "Перебор строк и циклы while"),
    ("10-04-break-continue.html", "break, continue и loop-else"),
    ("10-11-poisk-filtr-summa.html", "Поиск, фильтрация и суммирование"),
    ("10-12-proverka-vvoda.html", "Проверка ввода в цикле"),
    ("10-05-mini-proekt-ugadaj-v2.html", "Мини-проект: «Угадай число», версия 2"),
    ("10-13-otladka-ciklov.html", "Отладка циклов: 10 типичных ошибок"),
    ("10-06-avtomatiziruem-figury.html", "Автоматизируем квадрат и любую фигуру"),
    ("10-07-avtomatiziruem-mandalu.html", "Автоматически рисуем мандалу"),
    ("10-14-sluchajnye-uzory.html", "Случайные узоры: блуждание и звёзды"),
    ("10-15-setka-figur.html", "Сетка фигур: вложенные циклы в Turtle"),
    ("10-08-spirali-itogi.html", "Спирали из дуг и итоги"),
]

# ID практик в порядке появления на странице; несколько практик на одной
# странице — нормальный паттерн (см. главу 7: 07-24/07-25).
PRACTICE_IDS = [
    "10-01", "10-09", "10-10", "10-11", "10-02", "10-12", "10-24",
    "10-03", "10-23", "10-04", "10-13", "10-14", "10-22", "10-15",
    "10-05", "10-16", "10-17", "10-18", "10-06", "10-07", "10-19",
    "10-20", "10-08", "10-21",
]

LOCAL_REQUIRED_IDS = {"10-06", "10-07", "10-19", "10-20", "10-08", "10-21"}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 10 · Циклы", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def turtle_output(name: str, filename: str, *, caption: str, alt: str) -> str:
    """КОД → РЕАЛЬНЫЙ OUTPUT — тот же компонент, что и в главах 6-7 (см.
    scripts/build_chapter_07.py:turtle_output). code_block() слева/сверху,
    реально выполненная картинка справа/снизу; код в EXAMPLES не содержит
    exitonclick()/bye() — эта строка дописывается только для читателя."""
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
          <img src="{IMG}/chapter-10/output/{name}.png" alt="{alt}"
            style="width:100%;height:auto;border-radius:12px;display:block;background:#fff" />
          <figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>
        </figure>
      </div>
    </div>"""


def two_up(left_html: str, right_html: str) -> str:
    return f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin:20px 0;align-items:flex-start">
      <div style="flex:1 1 260px;min-width:220px">{left_html}</div>
      <div style="flex:1 1 260px;min-width:220px">{right_html}</div>
    </div>"""


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=10,
        baseline_page=195,
        title="Немного автоматизации!",
        description="Циклы for и while как третья структура алгоритма после ветвления из главы 9, "
        "range() и enumerate() без мифов, break/continue/loop-else, вложенные циклы, отладка "
        "типичных ошибок циклов — и наконец-то настоящая автоматизация всех фигур из глав 6-7.",
        meta_items=["⏱ ~5 часов", "🔁 for / while", "📓 24 практики"],
        sections=[
            ChapterSectionLink("10.1", "Повторение и первый цикл for", "10-01-cikly-for.html", "195"),
            ChapterSectionLink("", "Три структуры алгоритма: вспоминаем", "10-01-cikly-for.html#tri-struktury", "196"),
            ChapterSectionLink("", "Канонический flowchart цикла for", "10-01-cikly-for.html#flowchart-for", "198"),
            ChapterSectionLink("10.2", "range() подробно", "10-09-range-podrobno.html", "200"),
            ChapterSectionLink("10.3", "Индекс, значение и enumerate()", "10-10-enumerate-i-nakoplenie.html", "203"),
            ChapterSectionLink("", "Мини-проект: анализатор текста", "10-10-enumerate-i-nakoplenie.html#analizator-teksta", "206"),
            ChapterSectionLink("10.4", "if внутри циклов for", "10-02-if-vlozhennye-cikly.html", "208"),
            ChapterSectionLink("", "Вложенные циклы for", "10-02-if-vlozhennye-cikly.html#vlozhennye", "209"),
            ChapterSectionLink("", "Мини-проект: таблица умножения", "10-02-if-vlozhennye-cikly.html#tablica-umnozheniya", "211"),
            ChapterSectionLink("10.5", "Перебор строк, циклы while", "10-03-perebor-strok-while.html", "213"),
            ChapterSectionLink("", "Бесконечный цикл и while True", "10-03-perebor-strok-while.html#while-true", "215"),
            ChapterSectionLink("10.6", "break, continue и loop-else", "10-04-break-continue.html", "217"),
            ChapterSectionLink("", "Мини-проект: цикл команд", "10-04-break-continue.html#cikl-komand", "220"),
            ChapterSectionLink("10.7", "Поиск, фильтрация и суммирование", "10-11-poisk-filtr-summa.html", "222"),
            ChapterSectionLink("10.8", "Проверка ввода в цикле", "10-12-proverka-vvoda.html", "224"),
            ChapterSectionLink("10.9", "Мини-проект — «Угадай число», версия 2", "10-05-mini-proekt-ugadaj-v2.html", "226"),
            ChapterSectionLink("10.10", "Отладка циклов: 10 типичных ошибок", "10-13-otladka-ciklov.html", "228"),
            ChapterSectionLink("10.11", "Мини-проект — автоматизируем фигуры", "10-06-avtomatiziruem-figury.html", "231"),
            ChapterSectionLink("10.12", "Мини-проект — автоматически рисуем мандалу", "10-07-avtomatiziruem-mandalu.html", "234"),
            ChapterSectionLink("10.13", "Случайные узоры Turtle", "10-14-sluchajnye-uzory.html", "236"),
            ChapterSectionLink("10.14", "Сетка фигур: вложенные циклы в Turtle", "10-15-setka-figur.html", "238"),
            ChapterSectionLink("10.15", "Спирали из дуг и итоги", "10-08-spirali-itogi.html", "240"),
            ChapterSectionLink("", "Итоги главы", "10-08-spirali-itogi.html#itogi", "242"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 10-01 · Повторение и первый цикл for
# ---------------------------------------------------------------------------

def build_10_01() -> None:
    repeated_square = (
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)"
    )
    cvm = classic_vs_modern(
        "Квадрат из главы 6: 8 строк → 2 строки",
        "Без цикла (глава 6)",
        repeated_square,
        "С циклом for",
        "for _ in range(4):\n    artist.forward(100)\n    artist.right(90)",
        "цикл <code class=\"inline\">for</code>. Он не «современнее» в смысле версии Python — "
        "циклы существуют с самых первых версий языка, — но именно ради него стоило дочитать "
        "до этой главы: то же самое поведение, в 4 раза короче, и легко изменить число повторов "
        "одной цифрой.",
    )

    body = f"""
    <h2>Прежде чем Python: повторение вокруг нас</h2>
    <p>Мы повторяем действия постоянно, даже не задумываясь: чистим зубы одинаковыми движениями,
    маршируем одинаковыми шагами, поём куплет за куплетом одной и той же мелодии. <strong>Повторение
    — это отдельный, самостоятельный способ устроить действие</strong>, наравне с «сделать одно
    за другим» и «выбрать один из двух путей».</p>

    <h2 id="tri-struktury">Три структуры алгоритма: вспоминаем</h2>
    <p>В главе 9 мы разобрали первые две из трёх фундаментальных структур, из которых складывается
    любой алгоритм. Третья — <strong>повторение</strong> — и есть тема этой главы.</p>
    {capability_map([
        ("1 · Последовательность", ["Шаги идут один за другим", "«Сначала… потом… потом…»", "Глава 9"]),
        ("2 · Ветвление", ["Выбор одного из путей по условию", "<code class=\"inline\">if / elif / else</code>", "Глава 9"]),
        ("3 · Повторение", ["Один и тот же блок — снова и снова", "<code class=\"inline\">for</code> / <code class=\"inline\">while</code>", "Эта глава"]),
    ], title="Три структуры, из которых строится любой алгоритм")}

    <h2>Что не так с этим кодом?</h2>
    <p>Вот квадрат из главы 6 — уже знакомый код: четыре одинаковых блока «шаг вперёд, поворот»,
    записанных вручную:</p>
    {code_block("kvadrat_bez_cikla.py", repeated_square)}
    <p>А теперь представьте, что нужен не квадрат, а <strong>двадцатиугольник</strong>. Копировать
    эти две строки ещё 16 раз вручную — долго и легко ошибиться. Именно для таких повторяющихся
    блоков и существуют <strong>циклы</strong>: способ сказать Python «повтори это N раз» вместо
    того, чтобы копировать код руками.</p>

    <h2>Термины цикла</h2>
    <p>Прежде чем писать первый цикл, договоримся о словах, которыми будем его описывать —
    дальше они встретятся во всей главе:</p>
    {comparison_table(
        ["Термин", "Что это"],
        [
            ["<strong>цикл</strong>", "конструкция, которая повторяет один и тот же блок кода несколько раз"],
            ["<strong>тело цикла</strong>", "тот самый блок кода, который повторяется (строки с отступом под <code class=\"inline\">for</code>/<code class=\"inline\">while</code>)"],
            ["<strong>итерация</strong>", "один проход тела цикла — один «раз» из «повтори N раз»"],
            ["<strong>условие</strong>", "то, что цикл проверяет, чтобы решить, продолжать или остановиться"],
            ["<strong>счётчик</strong>", "переменная, которая считает номер итерации или меняется с каждым шагом"],
        ],
    )}

    <h2>Циклы for</h2>
    <p>Самый частый вид цикла в Python — <code class="inline">for</code>. Вместе с
    <code class="inline">range()</code> он умеет повторить блок кода заданное число раз:</p>
    {code_block("cikl_for.py", 'for i in range(5):\n    print(i)\n')}

    <h3>Разбираем по словам</h3>
    {comparison_table(
        ["Часть кода", "Что означает"],
        [
            ["<code class=\"inline\">for</code>", "«начинаем цикл»"],
            ["<code class=\"inline\">i</code>", "переменная цикла — на каждом шаге получает следующее значение из <code class=\"inline\">range(5)</code>"],
            ["<code class=\"inline\">in range(5)</code>", "источник значений: числа от 0 до 4"],
            ["<code class=\"inline\">:</code>", "дальше начинается тело цикла (с отступом)"],
            ["<code class=\"inline\">print(i)</code>", "тело цикла — то, что повторяется на каждой итерации"],
        ],
    )}

    {timeline_diagram([
        ("Итерация 1", "i = 0 → print(0)"),
        ("Итерация 2", "i = 1 → print(1)"),
        ("Итерация 3", "i = 2 → print(2)"),
        ("Итерация 4", "i = 3 → print(3)"),
        ("Итерация 5", "i = 4 → print(4)"),
    ], caption="for i in range(5): print(i) — пять итераций одного и того же тела цикла")}

    <h3 id="flowchart-for">Канонический flowchart цикла for</h3>
    <p>Важно сразу привыкнуть к правильной картине происходящего: <code class="inline">for</code>
    не «выполняет тело N раз по волшебству» — на каждом шаге он спрашивает «есть ли следующий
    элемент?», и если да — выполняет тело и спрашивает снова:</p>
    {for_loop_flowchart(
        "range(5)", "Есть следующее число?", "print(i)",
        caption="for i in range(5): print(i) — цикл каждый раз запрашивает следующий элемент",
    )}

    <h3>Трасса выполнения</h3>
    <p>Таблица трассировки — способ построчно проследить, что происходит на каждой итерации. Мы
    будем пользоваться такой таблицей всю главу:</p>
    {comparison_table(
        ["Итерация", "i", "Вывод (print)"],
        [["1", "0", "0"], ["2", "1", "1"], ["3", "2", "2"], ["4", "3", "3"], ["5", "4", "4"]],
    )}

    {callout(
        "info",
        "range() с разными аргументами — коротко",
        "<code class=\"inline\">range(5)</code> — от 0 до 4. "
        "<code class=\"inline\">range(2, 8)</code> — от 2 до 7. "
        "<code class=\"inline\">range(0, 10, 2)</code> — от 0 до 8 с шагом 2: 0, 2, 4, 6, 8. "
        "Подробный разбор — на следующей странице.",
    )}

    <h2>Когда переменная цикла не нужна</h2>
    <p>Если само число повторов важно, а не значение счётчика — по традиции его называют
    <code class="inline">_</code> (нижнее подчёркивание), сигнализируя «это значение
    сознательно не используется»:</p>
    {cvm}
    {callout(
        "warning",
        "_ — соглашение, а не специальный синтаксис",
        "<code class=\"inline\">_</code> — обычное имя переменной, Python не обрабатывает его "
        "как-то по-особому. Это просто договорённость между программистами: «здесь мы намеренно "
        "не используем значение цикла». Написать <code class=\"inline\">for x in range(4):</code> "
        "тоже сработает — но будет менее понятно читателю кода.",
    )}

    {practice_card(
        "10-01",
        "Практика: цикл for и терминология",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-01/index.html",
    )}
    """
    out = render_page(
        page_title="Повторение и первый цикл for",
        description="Повторение как третья структура алгоритма, терминология цикла, первый for и его канонический flowchart.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Циклы for", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Волшебные циклы! Циклы for",
        lede="Наконец-то настоящая автоматизация: вместо повторения кода вручную — просим "
        "Python повторить его самостоятельно.",
        body_html=body,
        sidebar_groups=sidebar("10-01-cikly-for.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="10-09-range-podrobno.html", next_label="range() подробно"),
    )
    write("10-01-cikly-for.html", out)


# ---------------------------------------------------------------------------
# 10-09 · range() подробно
# ---------------------------------------------------------------------------

def build_10_09() -> None:
    body = f"""
    <h2>range() — не список</h2>
    <p><code class="inline">range()</code> — одна из самых частых причин путаницы у новичков.
    Разберёмся сразу и точно.</p>
    {callout(
        "warning",
        "range() НЕ создаёт список",
        "<code class=\"inline\">range(5)</code> создаёт особый объект-генератор чисел — он "
        "выдаёт числа по одному, по требованию, а не хранит их все сразу в памяти как список. "
        "<code class=\"inline\">list(range(5))</code> действительно даст "
        "<code class=\"inline\">[0, 1, 2, 3, 4]</code> — но это отдельное, явное превращение, "
        "а не то, чем является сам <code class=\"inline\">range</code>.",
    )}

    <h2>Три уровня сигнатуры</h2>
    {comparison_table(
        ["Вызов", "Что означает", "Пример"],
        [
            ["<code class=\"inline\">range(stop)</code>", "от 0 до stop, не включая stop", "<code class=\"inline\">range(5)</code> → 0, 1, 2, 3, 4"],
            ["<code class=\"inline\">range(start, stop)</code>", "от start до stop, не включая stop", "<code class=\"inline\">range(2, 8)</code> → 2, 3, 4, 5, 6, 7"],
            ["<code class=\"inline\">range(start, stop, step)</code>", "от start до stop с шагом step, не включая stop", "<code class=\"inline\">range(0, 10, 2)</code> → 0, 2, 4, 6, 8"],
        ],
    )}
    {range_diagram(start=0, stop=5, caption="range(5) — пять значений: 0, 1, 2, 3, 4; сам stop=5 в результат не входит")}
    {range_diagram(start=2, stop=8, caption="range(2, 8) — от 2 до 7 включительно; 8 не входит")}

    <h2>Почему stop не включается</h2>
    <p>Это не произвольная прихоть языка — это то же самое правило, что мы уже видели в главе 8
    у срезов строк. <code class="inline">"Python"[0:3]</code> берёт символы с индексами 0, 1, 2 —
    и не включает символ с индексом 3. <code class="inline">range(0, 3)</code> устроен ровно так
    же: 0, 1, 2, без 3. Python последователен: «конец диапазона» везде означает «до этого места,
    не включая его».</p>
    {callout(
        "info",
        "Полезное следствие",
        "Благодаря этому правилу <code class=\"inline\">range(n)</code> всегда даёт ровно "
        "<code class=\"inline\">n</code> чисел, а длина среза <code class=\"inline\">s[a:b]</code> "
        "всегда равна <code class=\"inline\">b - a</code> — считать количество элементов "
        "получается без дополнительных +1/-1 в уме.",
    )}

    <h2>Шаг: step</h2>
    <p>Третий аргумент задаёт, на сколько увеличивается (или уменьшается) число на каждом шаге:</p>
    {code_block("shag.py", "for number in range(0, 10, 2):\n    print(number)\n")}
    {range_diagram(start=0, stop=10, step=2, caption="range(0, 10, 2) — шаг 2: 0, 2, 4, 6, 8")}

    <h2>Отрицательный шаг</h2>
    <p>Шаг может быть отрицательным — тогда числа идут в обратную сторону, но start и stop
    нужно тоже поменять местами по смыслу: start должен быть больше, чем stop.</p>
    {code_block("otricatelnyj_shag.py", "for number in range(10, 0, -2):\n    print(number)\n")}
    {range_diagram(start=10, stop=0, step=-2, caption="range(10, 0, -2) — отсчёт назад с шагом 2: 10, 8, 6, 4, 2")}
    {callout(
        "warning",
        "Отрицательный range без отрицательного шага — пустой",
        "<code class=\"inline\">range(10, 0)</code> (без шага) не выдаст ничего — шаг по "
        "умолчанию равен +1, а с ним никогда не попасть от 10 вниз к 0. Чтобы диапазон шёл вниз, "
        "шаг обязательно должен быть отрицательным и соответствовать направлению.",
    )}
    {callout(
        "warning",
        "Шаг 0 — ошибка, а не бесконечный цикл",
        "<code class=\"inline\">range(0, 10, 0)</code> не зависает и не превращается в "
        "бесконечный цикл — Python сразу поднимает "
        "<code class=\"inline\">ValueError: range() arg 3 must not be zero</code>, потому что "
        "с нулевым шагом никогда не сдвинуться от start к stop.",
    )}

    {practice_card(
        "10-09",
        "Практика: range() — старт, стоп, шаг",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-09/index.html",
    )}
    """
    out = render_page(
        page_title="range() подробно: старт, стоп, шаг",
        description="Три сигнатуры range(), почему stop не включён (связь со срезами строк), шаг и отрицательный шаг.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("range() подробно", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="range() подробно",
        lede="range() — не список, а генератор чисел по требованию. Разбираем все три его формы "
        "и то, откуда взялось правило «stop не включён».",
        body_html=body,
        sidebar_groups=sidebar("10-09-range-podrobno.html"),
        nav=PageNav(prev_href="10-01-cikly-for.html", prev_label="Циклы for", next_href="10-10-enumerate-i-nakoplenie.html", next_label="enumerate() и накопление"),
    )
    write("10-09-range-podrobno.html", out)


# ---------------------------------------------------------------------------
# 10-10 · Индекс, значение, enumerate() и накопление
# ---------------------------------------------------------------------------

def build_10_10() -> None:
    body = f"""
    <h2>for умеет перебирать не только числа</h2>
    <p>Строка — это последовательность символов (глава 8), а значит, <code class="inline">for</code>
    умеет перебирать и её — символ за символом, без индексов:</p>
    {code_block("perebor_strok.py", 'for letter in "Python":\n    print(letter)\n')}
    <p>То же самое работает для списков и любых других <strong>итерируемых</strong> объектов —
    так называют всё, что <code class="inline">for</code> умеет перебирать по одному элементу.
    Строка, список, диапазон <code class="inline">range()</code> — всё это итерируемые объекты;
    точный технический механизм, как именно Python это делает «под капотом», мы разберём в
    следующих главах, когда будем подробно изучать списки.</p>

    <h2>Индекс против значения</h2>
    <p>В цикле <code class="inline">for letter in "Python":</code> мы получаем сам символ
    («значение»), но не его номер по счёту («индекс»). Иногда номер важен — например, чтобы
    вывести «символ №1: P».</p>

    <h3>Классический вариант — цикл по индексам</h3>
    {code_block(
        "cikl_po_indeksam.py",
        'slovo = "Python"\nfor i in range(len(slovo)):\n    print(i, slovo[i])\n',
    )}

    <h3>«Питонический» вариант — enumerate()</h3>
    {code_block(
        "enumerate_variant.py",
        'slovo = "Python"\nfor i, letter in enumerate(slovo):\n    print(i, letter)\n',
    )}
    {comparison_table(
        ["i", "letter"],
        [["0", "P"], ["1", "y"], ["2", "t"], ["3", "h"], ["4", "o"], ["5", "n"]],
    )}
    {callout(
        "tip",
        "Когда использовать enumerate()",
        "<code class=\"inline\">enumerate()</code> нужен именно тогда, когда важны и индекс, "
        "и значение одновременно. Если индекс вообще не нужен — используйте "
        "<code class=\"inline\">for letter in slovo:</code>, без него. Цикл по индексам "
        "(<code class=\"inline\">range(len(...))</code>) — не «неправильный» способ, а просто "
        "более многословный там, где <code class=\"inline\">enumerate()</code> справится короче.",
    )}

    <h2>Счётчик — переменная, которая считает</h2>
    <p><strong>Счётчик</strong> — переменная, которая с каждой итерацией увеличивается (или
    уменьшается) на фиксированный шаг, обычно на 1. Она отслеживает «сколько раз мы это уже
    сделали».</p>
    {code_block(
        "schetchik.py",
        'glasnye = "аеёиоуыэюя"\nslovo = "программирование"\nkolichestvo = 0\n\nfor letter in slovo:\n'
        "    if letter in glasnye:\n        kolichestvo += 1\n\nprint(kolichestvo)\n",
    )}
    {comparison_table(
        ["Символ", "letter in glasnye?", "kolichestvo после шага"],
        [["п", "нет", "0"], ["р", "нет", "0"], ["о", "да", "1"], ["г", "нет", "1"], ["р", "нет", "1"], ["а", "да", "2"], ["…", "…", "…"]],
    )}

    <h2>Накопитель (аккумулятор) — переменная, которая копит результат</h2>
    <p><strong>Накопитель</strong> устроен похоже на счётчик, но копит не количество шагов, а
    сам результат — сумму, произведение, склеенную строку:</p>
    {code_block(
        "nakopitel.py",
        "chisla = [4, 8, 15, 16, 23, 42]\nsumma = 0\n\nfor n in chisla:\n    summa += n\n\nprint(summa)\n",
    )}
    {comparison_table(
        ["Итерация", "n", "summa после шага"],
        [["1", "4", "4"], ["2", "8", "12"], ["3", "15", "27"], ["4", "16", "43"], ["5", "23", "66"], ["6", "42", "108"]],
    )}
    {callout(
        "info",
        "Общее в счётчике и накопителе: состояние",
        "И счётчик, и накопитель — примеры <strong>состояния</strong>: переменной, которая "
        "живёт снаружи цикла, но меняется на каждой итерации внутри него. Перед циклом "
        "состояние обязательно нужно инициализировать (<code class=\"inline\">kolichestvo = 0</code>) "
        "— без этого шага <code class=\"inline\">kolichestvo += 1</code> на первой же итерации "
        "упадёт с ошибкой, потому что переменной ещё не существует.",
    )}

    <h2 id="analizator-teksta">Мини-проект: анализатор текста</h2>
    <p>Соберём счётчик и накопитель вместе в одном небольшом инструменте — подсчитаем гласные,
    длину самого длинного слова и общее число слов в тексте:</p>
    {code_block(
        "analizator_teksta.py",
        'tekst = "python это просто и понятно"\nslova = tekst.split()\n\n'
        "glasnye_count = 0\nfor letter in tekst:\n    if letter in \"аеёиоуыэюя\":\n        glasnye_count += 1\n\n"
        "samoe_dlinnoe = \"\"\nfor slovo in slova:\n    if len(slovo) > len(samoe_dlinnoe):\n        samoe_dlinnoe = slovo\n\n"
        'print(f"Слов: {len(slova)}, гласных: {glasnye_count}, самое длинное: {samoe_dlinnoe}")\n',
    )}
    {callout(
        "tip",
        "Три независимых накопителя рядом",
        "Обратите внимание: <code class=\"inline\">glasnye_count</code> и "
        "<code class=\"inline\">samoe_dlinnoe</code> — два разных накопителя, каждый со своим "
        "циклом и своей начальной инициализацией. Комбинировать несколько состояний в одной "
        "программе — обычное дело, главное — не запутать, какое состояние меняется в каком цикле.",
    )}

    {practice_card(
        "10-10",
        "Практика: индекс, значение и enumerate()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-10/index.html",
    )}
    {practice_card(
        "10-11",
        "Практика: мини-проект «Анализатор текста»",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-11/index.html",
    )}
    """
    out = render_page(
        page_title="Индекс, значение, enumerate() и накопление",
        description="for по строкам, индекс против значения, enumerate(), счётчик и накопитель, мини-проект «Анализатор текста».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("enumerate() и накопление", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Индекс, значение и enumerate()",
        lede="for умеет перебирать не только числа — а счётчик и накопитель превращают простой "
        "перебор в настоящий инструмент анализа данных.",
        body_html=body,
        sidebar_groups=sidebar("10-10-enumerate-i-nakoplenie.html"),
        nav=PageNav(prev_href="10-09-range-podrobno.html", prev_label="range() подробно", next_href="10-02-if-vlozhennye-cikly.html", next_label="if и вложенные циклы"),
    )
    write("10-10-enumerate-i-nakoplenie.html", out)


# ---------------------------------------------------------------------------
# 10-02 · if внутри циклов, вложенные циклы
# ---------------------------------------------------------------------------

def build_10_02() -> None:
    body = f"""
    <h2>Условия if внутри циклов for</h2>
    <p><code class="inline">if</code> из главы 9 прекрасно работает внутри цикла — на каждом
    шаге можно принимать своё решение:</p>
    {code_block("if_v_cikle.py", "for number in range(1, 11):\n    if number % 2 == 0:\n        print(number, \"— чётное\")\n")}

    <h2 id="vlozhennye">Вложенные циклы for</h2>
    <p>Цикл можно поместить внутрь другого цикла — тогда внутренний цикл выполняется полностью
    на каждом шаге внешнего. Представьте сетку: внешний цикл идёт по строкам, внутренний — по
    столбцам каждой строки:</p>
    {code_block(
        "vlozhennye_cikly.py",
        "for row in range(3):\n"
        "    for col in range(4):\n"
        '        print(f"({row}, {col})", end=" ")\n'
        "    print()  # новая строка после каждого ряда\n",
    )}
    {nested_loop_grid(3, 4, row_label="row (0..2)", col_label="col (0..3)", caption="Внешний цикл — 3 строки, внутренний — 4 столбца в каждой: 3 × 4 = 12 ячеек")}

    <h3>Сколько раз выполнится внутренний цикл?</h3>
    {math_formula(("row", "строк", ("mo", "×"), "столбцов", ("mo", "="), "итераций тела"), caption="Формула числа итераций вложенного цикла")}
    {comparison_table(
        ["row", "col", "print(...) сработал раз №"],
        [["0", "0", "1"], ["0", "1", "2"], ["0", "2", "3"], ["0", "3", "4"], ["1", "0", "5"], ["…", "…", "…"], ["2", "3", "12"]],
    )}
    {callout(
        "tip",
        "Вложенные циклы — частая причина неожиданной медлительности",
        "Внешний цикл выполняется 3 раза, внутренний — 4 раза <em>на каждом</em> шаге внешнего "
        "— итого <code class=\"inline\">print(...)</code> внутри сработает "
        "<code class=\"inline\">3 * 4 = 12</code> раз. Если оба цикла идут не до 3-4, а до "
        "тысяч, итоговое число итераций перемножается — и программа может выполняться заметно "
        "дольше, чем кажется на первый взгляд.",
    )}

    <h2 id="tablica-umnozheniya">Мини-проект: таблица умножения</h2>
    <p>Классическая задача на вложенные циклы — напечатать таблицу умножения от 1 до 5:</p>
    {code_block(
        "tablica_umnozheniya.py",
        "for a in range(1, 6):\n"
        "    for b in range(1, 6):\n"
        '        print(a * b, end="\\t")\n'
        "    print()\n",
    )}
    {callout(
        "info",
        "Один или два примера — этого достаточно",
        "Специально не будем множить примеры узоров на вложенных циклах — таблица умножения "
        "(и сетка выше) дают достаточно интуиции, чтобы читать и писать любые похожие конструкции "
        "самостоятельно.",
    )}

    <h2>Цикл + строка + условие</h2>
    <p>Вложенность работает и там, где внутренний «цикл» — это перебор символов строки внутри
    внешнего перебора списка слов:</p>
    {code_block(
        "cikl_stroka_uslovie.py",
        'slova = ["python", "код", "цикл"]\n\nfor slovo in slova:\n    bukvy_o = 0\n'
        "    for letter in slovo:\n        if letter == \"о\":\n            bukvy_o += 1\n"
        '    print(slovo, "—", bukvy_o)\n',
    )}

    {practice_card(
        "10-02",
        "Практика: условия и вложенные циклы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-02/index.html",
    )}
    {practice_card(
        "10-12",
        "Практика: мини-проект «Таблица умножения»",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-12/index.html",
    )}
    {practice_card(
        "10-24",
        "Практика: сколько итераций во вложенном цикле?",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-24/index.html",
    )}
    """
    out = render_page(
        page_title="Условия if внутри циклов for, вложенные циклы",
        description="Комбинируем if с for, учимся вкладывать циклы друг в друга, мини-проект «Таблица умножения».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("if и вложенные циклы", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Условия if внутри циклов for",
        lede="Циклы и условия отлично работают вместе — а циклы можно вкладывать друг в друга.",
        body_html=body,
        sidebar_groups=sidebar("10-02-if-vlozhennye-cikly.html"),
        nav=PageNav(prev_href="10-10-enumerate-i-nakoplenie.html", prev_label="enumerate() и накопление", next_href="10-03-perebor-strok-while.html", next_label="Перебор строк и циклы while"),
    )
    write("10-02-if-vlozhennye-cikly.html", out)


# ---------------------------------------------------------------------------
# 10-03 · Перебор строк и циклы while
# ---------------------------------------------------------------------------

def build_10_03() -> None:
    body = f"""
    <h2>Когда число повторов заранее неизвестно</h2>
    <p><code class="inline">for</code> отлично подходит, когда мы заранее знаем, сколько раз
    нужно повторить действие — «4 стороны квадрата», «все буквы слова». Но что делать, если
    число повторов заранее неизвестно — например, «повторяй, пока пользователь не угадает
    число»? Для таких задач существует второй вид цикла — <code class="inline">while</code>.</p>

    <h2>Циклы while</h2>
    <p>В отличие от <code class="inline">for</code>, <code class="inline">while</code>
    повторяется <strong>пока истинно условие</strong>:</p>
    {code_block(
        "cikl_while.py",
        "count = 0\n"
        "while count < 5:\n"
        "    print(count)\n"
        "    count += 1\n",
    )}

    <h3>Канонический flowchart цикла while</h3>
    {while_loop_flowchart(
        "count = 0", "count < 5?", "print(count)", "count += 1",
        caption="while count < 5: — проверка условия ПЕРЕД каждым телом, включая самое первое",
    )}

    <h3>Три части цикла while</h3>
    {comparison_table(
        ["Часть", "Код", "Роль"],
        [
            ["Инициализация", "<code class=\"inline\">count = 0</code>", "готовит состояние ДО первой проверки условия"],
            ["Условие", "<code class=\"inline\">count &lt; 5</code>", "проверяется перед каждой итерацией, включая самую первую"],
            ["Обновление", "<code class=\"inline\">count += 1</code>", "меняет состояние так, чтобы условие рано или поздно стало ложным"],
        ],
    )}
    {comparison_table(
        ["Итерация", "Проверка count &lt; 5", "Вывод", "count после шага"],
        [["1", "0 &lt; 5 → да", "0", "1"], ["2", "1 &lt; 5 → да", "1", "2"], ["3", "2 &lt; 5 → да", "2", "3"],
         ["4", "3 &lt; 5 → да", "3", "4"], ["5", "4 &lt; 5 → да", "4", "5"], ["—", "5 &lt; 5 → нет", "цикл завершён", "—"]],
    )}
    {callout(
        "info",
        "while — это pre-test цикл",
        "Условие в <code class=\"inline\">while</code> проверяется <strong>до</strong> тела "
        "— значит, если условие изначально ложно, тело не выполнится вообще ни разу (ноль "
        "итераций). В Python нет отдельного «сначала выполни, потом проверь» цикла (в некоторых "
        "других языках он называется <code class=\"inline\">do/while</code>) — если такое "
        "поведение нужно, его моделируют через <code class=\"inline\">while True</code> с "
        "<code class=\"inline\">break</code> в конце тела (мы увидим этот приём на следующей "
        "странице).",
    )}

    <h2 id="while-true">Бесконечный цикл — намеренно и случайно</h2>
    <p>Посмотрите на этот код внимательно:</p>
    {code_block(
        "beskonechnyj_cikl.py",
        "count = 0\nwhile count < 5:\n    print(count)\n    # забыли count += 1!\n",
    )}
    {loop_preview_diagram(
        action_label="print(count)",
        question_label="count < 5?",
        caption="Состояние (count) не меняется между итерациями — условие остаётся истинным навсегда",
    )}
    {callout(
        "warning",
        "Как остановить зависшую программу",
        "Если программа зависла в бесконечном цикле — в терминале нажмите "
        "<code class=\"inline\">Ctrl+C</code> (или кнопку «Стоп»/«Interrupt kernel» в Jupyter). "
        "Всегда проверяйте, что внутри <code class=\"inline\">while</code> есть шаг, который "
        "рано или поздно сделает условие ложным.",
    )}

    <h2>while True — тоже нормально</h2>
    <p><code class="inline">while True</code> создаёт цикл, условие которого само по себе никогда
    не станет ложным — единственный выход из него: <code class="inline">break</code> внутри тела.
    Это распространённый и совершенно правильный приём, когда условие остановки естественнее
    проверить в середине тела, а не в его начале — мы воспользуемся им уже на следующей странице.</p>
    {callout(
        "warning",
        "while True сам по себе — не ошибка",
        "<code class=\"inline\">while True:</code> не является «плохой практикой» сама по себе "
        "— это осознанный инструмент. Проблема возникает только тогда, когда внутри забыли "
        "поставить <code class=\"inline\">break</code> — вот тогда цикл действительно никогда "
        "не остановится.",
    )}

    <h2>Перебор строк — напоминание</h2>
    <p>Строка — это последовательность символов (глава 8) — <code class="inline">for</code>
    умеет перебирать её напрямую, без индексов (подробный разбор индекса и значения — на
    странице про enumerate()):</p>
    {code_block("perebor_strok.py", 'for letter in "Python":\n    print(letter)\n')}

    <h2>for или while?</h2>
    {decision_map([
        ("Число повторов известно заранее («нарисовать 4 стороны», «перебрать все буквы»)", "for"),
        ("Число повторов заранее неизвестно («пока пользователь не угадает»)", "while"),
        ("Естественнее проверять условие остановки в середине тела", "while True + break"),
        ("Нужно пройти по готовой последовательности (строка, список, range)", "for"),
    ], title="Ориентир, а не жёсткое правило", caption="Оба вида цикла в Python одинаково мощные — выбор влияет на читаемость кода, а не на то, что вообще возможно сделать")}

    {practice_card(
        "10-03",
        "Практика: циклы while",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-03/index.html",
    )}
    {practice_card(
        "10-23",
        "Практика: for или while — что выбрать?",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-23/index.html",
    )}
    """
    out = render_page(
        page_title="Перебор строк и циклы while",
        description="while мотивирован задачами с неизвестным числом повторов: канонический flowchart, три части, while True, for-vs-while.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Строки и while", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Циклы while",
        lede="for умеет перебирать не только числа — а while повторяет действие, пока условие "
        "остаётся истинным, сколько бы раз это ни потребовалось.",
        body_html=body,
        sidebar_groups=sidebar("10-03-perebor-strok-while.html"),
        nav=PageNav(prev_href="10-02-if-vlozhennye-cikly.html", prev_label="if и вложенные циклы", next_href="10-04-break-continue.html", next_label="break, continue и loop-else"),
    )
    write("10-03-perebor-strok-while.html", out)


# ---------------------------------------------------------------------------
# 10-04 · break, continue и loop-else
# ---------------------------------------------------------------------------

def build_10_04() -> None:
    body = f"""
    <p>Иногда нужно выйти из цикла раньше времени или пропустить один шаг, не завершая цикл
    целиком — для этого есть два ключевых слова, и один особый способ узнать, был ли break.</p>

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
    {break_continue_flowchart("break", "for number in range(1, 100)", "number == 5?", caption="break выходит СРАЗУ из цикла целиком — но не из программы")}
    {callout(
        "warning",
        "break не завершает программу",
        "<code class=\"inline\">break</code> прерывает только тот цикл, в котором находится "
        "— код после цикла продолжает выполняться как обычно. Это не аналог выхода из "
        "программы, а именно выход из повторения.",
    )}

    <h2><code class="inline">continue</code> — пропустить этот шаг</h2>
    {code_block(
        "continue.py",
        "for number in range(1, 6):\n"
        "    if number == 3:\n"
        "        continue  # пропускаем оставшуюся часть тела для этого шага\n"
        "    print(number)\n",
    )}
    <p>Выведет 1, 2, 4, 5 — число 3 пропущено, но цикл продолжается дальше, в отличие от
    <code class="inline">break</code>.</p>
    {break_continue_flowchart("continue", "for number in range(1, 6)", "number == 3?", caption="continue пропускает остаток ТЕЛА и переходит к следующей итерации — цикл продолжается")}
    {callout(
        "warning",
        "continue не выходит из цикла",
        "<code class=\"inline\">continue</code> обрывает только текущий проход тела — сам цикл "
        "как продолжался, так и продолжается со следующего элемента. Это противоположность "
        "<code class=\"inline\">break</code>, а не его более мягкий вариант.",
    )}

    <h2>break и continue рядом</h2>
    {comparison_table(
        ["", "break", "continue"],
        [
            ["Что происходит", "цикл останавливается насовсем", "текущая итерация обрывается, цикл идёт дальше"],
            ["Код после цикла", "выполняется сразу", "выполняется только после того, как цикл закончится сам"],
            ["Частый пример", "нашли то, что искали — незачем продолжать", "этот элемент не подходит — пропускаем именно его"],
        ],
    )}

    <h2>break в while True</h2>
    <p>Самое частое место для <code class="inline">break</code> — цикл <code class="inline">while
    True</code>, где условие остановки естественнее проверить в середине тела:</p>
    {code_block(
        "while_true_break.py",
        'komanda = ""\nwhile True:\n    komanda = input("Введите команду (stop — выход): ")\n'
        '    if komanda == "stop":\n        break\n    print("Выполняю:", komanda)\n',
    )}

    {callout(
        "warning",
        "continue перед обновлением счётчика — частая ловушка",
        "В цикле <code class=\"inline\">while</code> размещать "
        "<code class=\"inline\">continue</code> ДО строки, которая меняет состояние (например, "
        "<code class=\"inline\">count += 1</code>), опасно: эта строка будет пропускаться "
        "каждый раз, когда сработал <code class=\"inline\">continue</code>, — и цикл может "
        "никогда не завершиться. Подробнее разберём в уроке об отладке циклов.",
    )}

    <h2>loop-else — else у цикла, а не у if</h2>
    <p>У циклов <code class="inline">for</code> и <code class="inline">while</code> есть редко
    используемая, но иногда очень удобная возможность — блок <code class="inline">else</code>,
    который выполняется, <strong>только если цикл завершился без break</strong>:</p>
    {code_block(
        "loop_else.py",
        "chisla = [4, 8, 15, 16, 23, 42]\n\nfor n in chisla:\n    if n == 100:\n        print(\"Нашли 100!\")\n        break\nelse:\n    print(\"100 не найдено ни разу\")\n",
    )}
    {loop_else_flowchart(
        "chisla", "Есть следующее число?", "n == 100?", "print('Нашли!'); break", "print('не найдено')",
        caption="else у цикла выполняется, только если цикл дошёл до конца БЕЗ break",
    )}
    {callout(
        "warning",
        "loop-else — это НЕ if/else",
        "Хотя слово <code class=\"inline\">else</code> то же самое, что и у "
        "<code class=\"inline\">if</code>, смысл совершенно другой. "
        "<code class=\"inline\">else</code> у <code class=\"inline\">if</code> означает "
        "«если условие ложно». <code class=\"inline\">else</code> у цикла означает «если цикл "
        "закончился сам, а не через break». Если внутри цикла не было "
        "<code class=\"inline\">break</code> вообще — блок <code class=\"inline\">else</code> "
        "выполнится всегда, как только цикл дойдёт до конца.",
    )}

    <h2 id="cikl-komand">Мини-проект: цикл команд</h2>
    <p>Соберём <code class="inline">while True</code>, <code class="inline">break</code> и
    работу со строками/условиями из глав 8-9 в маленький интерактивный цикл. Это учебная
    демонстрация приёма, а не замена интерпретатору PySH из введения курса:</p>
    {code_block(
        "cikl_komand.py",
        'zhurnal = []\nwhile True:\n    komanda = input("Команда (help/list/stop): ").strip().lower()\n'
        '    if komanda == "stop":\n        print("Завершаю работу.")\n        break\n'
        '    elif komanda == "help":\n        print("Доступно: help, list, stop")\n'
        '    elif komanda == "list":\n        print("Журнал:", zhurnal)\n'
        "    else:\n        zhurnal.append(komanda)\n"
        '        print(f"Добавлено в журнал: {komanda}")\n',
    )}

    {practice_card(
        "10-04",
        "Практика: break и continue",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-04/index.html",
    )}
    {practice_card(
        "10-13",
        "Практика: мини-проект «Цикл команд» и loop-else",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-13/index.html",
    )}
    """
    out = render_page(
        page_title="Прервать миссию! break, continue и loop-else",
        description="Досрочное прерывание цикла (break), пропуск шага (continue) и редкий, но полезный loop-else.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("break и continue", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Прервать миссию! break и continue",
        lede="Два способа управлять циклом изнутри — остановить его совсем или пропустить один "
        "шаг — и особый блок else, который знает, был ли break.",
        body_html=body,
        sidebar_groups=sidebar("10-04-break-continue.html"),
        nav=PageNav(prev_href="10-03-perebor-strok-while.html", prev_label="Циклы while", next_href="10-11-poisk-filtr-summa.html", next_label="Поиск, фильтрация и суммирование"),
    )
    write("10-04-break-continue.html", out)


# ---------------------------------------------------------------------------
# 10-11 · Поиск, фильтрация и суммирование
# ---------------------------------------------------------------------------

def build_10_11() -> None:
    body = f"""
    <h2>Цикл + if = настоящие алгоритмы</h2>
    <p>Большинство реальных задач с циклами — это <code class="inline">for</code> или
    <code class="inline">while</code> в связке с <code class="inline">if</code>. Разберём три
    самых частых паттерна: поиск, фильтрация, суммирование.</p>

    <h2>Поиск (search)</h2>
    {code_block(
        "poisk.py",
        "chisla = [4, 8, 15, 16, 23, 42]\niskomoe = 16\nnajdeno = False\n\n"
        "for n in chisla:\n    if n == iskomoe:\n        najdeno = True\n        break\n\n"
        "print(najdeno)\n",
    )}

    <h2>Подсчёт (counting)</h2>
    {code_block(
        "podschet.py",
        "chisla = [4, 8, 15, 16, 23, 42, 8, 4]\nchetnye = 0\n\n"
        "for n in chisla:\n    if n % 2 == 0:\n        chetnye += 1\n\nprint(chetnye)\n",
    )}

    <h2>Суммирование: вручную и через sum()</h2>
    {code_block(
        "summa_vruchnuyu.py",
        "chisla = [4, 8, 15, 16, 23, 42]\nsumma = 0\n\nfor n in chisla:\n    summa += n\n\nprint(summa)\n",
    )}
    {code_block("summa_cherez_sum.py", "chisla = [4, 8, 15, 16, 23, 42]\nsumma = sum(chisla)\nprint(summa)\n")}
    {callout(
        "info",
        "sum() — не магия, а тот же цикл внутри",
        "<code class=\"inline\">sum()</code> — встроенная функция, которая делает ровно то же "
        "самое, что и ручной цикл с накопителем выше, просто в одну строку. Полезно сначала "
        "написать вручную (чтобы понять, что происходит), а потом знать, что для готового "
        "результата есть короткий путь.",
    )}

    <h2>Предпросмотр: поиск минимума и максимума</h2>
    {code_block(
        "min_max_vruchnuyu.py",
        "chisla = [4, 8, 15, 16, 23, 42]\nmaksimum = chisla[0]\n\n"
        "for n in chisla:\n    if n > maksimum:\n        maksimum = n\n\nprint(maksimum)\n"
        "# то же самое короче: print(max(chisla))\n",
    )}

    <h2>Фильтрация — собираем только нужное</h2>
    {code_block(
        "filtraciya.py",
        "chisla = [4, 8, 15, 16, 23, 42]\nchetnye_chisla = []\n\n"
        "for n in chisla:\n    if n % 2 == 0:\n        chetnye_chisla.append(n)\n\nprint(chetnye_chisla)\n",
    )}
    {flowchart([
        {"kind": "start", "label": "СТАРТ"},
        {"kind": "input", "label": "chisla, пустой список результата"},
        {"kind": "decision", "label": "n % 2 == 0?",
         "yes": [{"kind": "process", "label": "добавить n в результат"}], "no": []},
        {"kind": "output", "label": "вернуть список результата"},
        {"kind": "end", "label": "КОНЕЦ"},
    ], caption="Паттерн фильтрации: пройти по всем элементам, оставить только те, что прошли условие")}

    <h2>Сентинел-цикл — особое значение как сигнал остановки</h2>
    <p><strong>Сентинел</strong> — специальное значение, которое само по себе не является частью
    данных, а сигнализирует «данные закончились»:</p>
    {code_block(
        "sentinel_cikl.py",
        'summa = 0\nwhile True:\n    chislo = input("Введите число (stop — закончить): ")\n'
        '    if chislo == "stop":\n        break\n    summa += int(chislo)\n\nprint("Сумма:", summa)\n',
    )}
    {while_loop_flowchart(
        'summa = 0', 'ввод == "stop"?', 'summa += int(ввод)', "получить следующий ввод",
        caption="Сентинел-цикл: пользователь сам решает, когда данные закончились",
    )}

    <h2>Необязательно: FizzBuzz</h2>
    <p>Классическая, но необязательная задача-разминка на циклы и условия — если интересно,
    попробуйте написать её сами перед тем, как посмотреть решение:</p>
    {code_block(
        "fizzbuzz.py",
        "for n in range(1, 21):\n    if n % 15 == 0:\n        print(\"ФиззБазз\")\n"
        "    elif n % 3 == 0:\n        print(\"Фызз\")\n    elif n % 5 == 0:\n        print(\"Базз\")\n"
        "    else:\n        print(n)\n",
    )}

    {practice_card(
        "10-14",
        "Практика: поиск, подсчёт, суммирование, фильтрация",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-14/index.html",
    )}
    {practice_card(
        "10-22",
        "Практика: сентинел-цикл",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-22/index.html",
    )}
    """
    out = render_page(
        page_title="Поиск, фильтрация и суммирование",
        description="Цикл+if как настоящий алгоритм: поиск, подсчёт, суммирование, min/max, фильтрация, сентинел-цикл, FizzBuzz.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Поиск и фильтрация", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Поиск, фильтрация и суммирование",
        lede="Цикл в связке с if — это уже настоящий алгоритм: три самых частых паттерна, из "
        "которых строится большинство программ на циклах.",
        body_html=body,
        sidebar_groups=sidebar("10-11-poisk-filtr-summa.html"),
        nav=PageNav(prev_href="10-04-break-continue.html", prev_label="break и continue", next_href="10-12-proverka-vvoda.html", next_label="Проверка ввода в цикле"),
    )
    write("10-11-poisk-filtr-summa.html", out)


# ---------------------------------------------------------------------------
# 10-12 · Проверка ввода в цикле
# ---------------------------------------------------------------------------

def build_10_12() -> None:
    body = f"""
    <h2>Проблема: пользователь может ввести что угодно</h2>
    <p>Программа из главы 9 ожидала число от пользователя — но что, если он введёт слово или
    оставит поле пустым? Цикл <code class="inline">while</code> позволяет переспрашивать, пока
    ввод не станет подходящим:</p>
    {code_block(
        "proverka_vvoda.py",
        'vozrast = input("Введите возраст: ")\nwhile not vozrast.isdigit():\n'
        '    print("Нужно ввести число!")\n    vozrast = input("Введите возраст: ")\n\n'
        'vozrast = int(vozrast)\nprint("Спасибо! Вам", vozrast, "лет")\n',
    )}
    {while_loop_flowchart(
        "получить первый ввод", "ввод не число?", "сообщить об ошибке", "получить новый ввод",
        caption="Цикл проверки: переспрашивать, пока ввод не станет подходящим",
    )}

    {callout(
        "warning",
        "isdigit() — простая, но ограниченная проверка",
        "<code class=\"inline\">str.isdigit()</code> проверяет, что строка состоит только из "
        "цифр — этого достаточно для целых положительных чисел, но не отличает "
        "<code class=\"inline\">\"-5\"</code> (отрицательное число) или "
        "<code class=\"inline\">\"3.5\"</code> (дробное) от некорректного ввода. Более надёжный "
        "способ проверки — конструкция <code class=\"inline\">try/except</code> — мы изучим её "
        "в следующих главах; сейчас достаточно уметь проверять целые положительные числа.",
    )}

    <h2>Ограничение количества попыток</h2>
    <p>Иногда бесконечно переспрашивать не годится — разумно ограничить число попыток:</p>
    {code_block(
        "proverka_s_limitom.py",
        'popytki = 0\nmax_popytok = 3\n\nwhile popytki < max_popytok:\n'
        '    vozrast = input("Введите возраст: ")\n    if vozrast.isdigit():\n'
        "        print(\"Принято:\", vozrast)\n        break\n"
        '    print("Это не похоже на число.")\n    popytki += 1\nelse:\n'
        '    print("Слишком много неверных попыток.")\n',
    )}
    {callout(
        "tip",
        "Здесь снова пригодился loop-else",
        "Блок <code class=\"inline\">else</code> у <code class=\"inline\">while</code> "
        "выполнится, только если попытки закончились без успешного <code class=\"inline\">break</code> "
        "— ровно то, что нужно для сообщения «слишком много неверных попыток».",
    )}

    {practice_card(
        "10-15",
        "Практика: проверка ввода в цикле",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-15/index.html",
    )}
    """
    out = render_page(
        page_title="Проверка ввода в цикле",
        description="Цикл-переспрос, пока ввод не станет корректным; ограничение числа попыток с loop-else.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Проверка ввода", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Проверка ввода в цикле",
        lede="Один из самых практичных паттернов while — переспрашивать пользователя, пока "
        "введённое не станет подходящим.",
        body_html=body,
        sidebar_groups=sidebar("10-12-proverka-vvoda.html"),
        nav=PageNav(prev_href="10-11-poisk-filtr-summa.html", prev_label="Поиск и фильтрация", next_href="10-05-mini-proekt-ugadaj-v2.html", next_label="«Угадай число», версия 2"),
    )
    write("10-12-proverka-vvoda.html", out)


# ---------------------------------------------------------------------------
# 10-05 · Мини-проект: «Угадай число», версия 2
# ---------------------------------------------------------------------------

def build_10_05() -> None:
    body = f"""
    <p>Помните игру «Угадай число» из главы 9? У неё была одна проблема — всего одна попытка.
    Теперь, вооружившись <code class="inline">while</code> и <code class="inline">break</code>,
    дадим игроку сколько угодно попыток. Спроектируем её как настоящий алгоритм — сначала
    словами, потом схемой, потом кодом.</p>

    <h2>Шаг 1 — псевдокод</h2>
    {code_block(
        "psevdokod.txt",
        "загадать случайное число от 1 до 20\nсчётчик попыток = 0\nповторять пока не угадано:\n"
        "    получить попытку игрока\n    увеличить счётчик попыток\n"
        "    если попытка равна загаданному — сообщить победу и остановиться\n"
        "    иначе если попытка меньше — подсказать «больше»\n"
        "    иначе — подсказать «меньше»",
        lang="text",
    )}

    <h2>Шаг 2 — flowchart</h2>
    {flowchart([
        {"kind": "start", "label": "СТАРТ"},
        {"kind": "process", "label": "загадать число 1..20, popytki = 0"},
        {"kind": "input", "label": "получить попытку игрока"},
        {"kind": "process", "label": "popytki += 1"},
        {"kind": "decision", "label": "попытка == загаданное?",
         "yes": [{"kind": "output", "label": "сообщить победу"}],
         "no": [{"kind": "decision", "label": "попытка < загаданное?",
                 "yes": [{"kind": "output", "label": "подсказать «больше»"}],
                 "no": [{"kind": "output", "label": "подсказать «меньше»"}]}]},
        {"kind": "end", "label": "КОНЕЦ"},
    ], yes_label="ДА", no_label="НЕТ", caption="Угадай число v2 — алгоритм целиком, до единой строчки Python")}

    <h2>Шаг 3 — таблица трассировки (пример игры)</h2>
    {comparison_table(
        ["Попытка №", "Ввод игрока", "Загадано", "Результат"],
        [["1", "10", "14", "меньше"], ["2", "17", "14", "больше"], ["3", "14", "14", "угадал!"]],
    )}

    <h2>Шаг 4 — код</h2>
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
        "<code class=\"inline\">while True:</code> сам по себе никогда не остановится — "
        "единственный выход: <code class=\"inline\">break</code> внутри. Условие остановки "
        "(«игрок угадал») естественнее проверить в середине тела, а не в начале — идеальный "
        "случай для этого приёма.",
    )}

    <h2>Задача на закрепление: ограничение попыток и loop-else</h2>
    {exercise(2, "Ограничение попыток", "Перепишите игру так, чтобы у игрока было не более 5 попыток — используйте цикл for по range(5) вместо while True, и блок else у цикла, чтобы сообщить правильный ответ, если игрок за 5 попыток не угадал.")}

    {practice_card(
        "10-05",
        "Практика: «Угадай число» с неограниченными попытками",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-05/index.html",
    )}
    {practice_card(
        "10-16",
        "Практика: «Угадай число» с ограничением попыток (loop-else)",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-16/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — «Угадай число», версия 2",
        description="Проектируем игру заново: псевдокод → flowchart → трассировка → код. while+break, затем ограничение попыток с loop-else.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Угадай число v2", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — игра «Угадай число», версия 2",
        lede="Та же игра, что и в главе 9, — но теперь с неограниченным числом попыток, "
        "спроектированная от псевдокода и схемы до готового кода.",
        body_html=body,
        sidebar_groups=sidebar("10-05-mini-proekt-ugadaj-v2.html"),
        nav=PageNav(prev_href="10-12-proverka-vvoda.html", prev_label="Проверка ввода", next_href="10-13-otladka-ciklov.html", next_label="Отладка циклов"),
    )
    write("10-05-mini-proekt-ugadaj-v2.html", out)


# ---------------------------------------------------------------------------
# 10-13 · Отладка циклов: 10 типичных ошибок
# ---------------------------------------------------------------------------

def build_10_13() -> None:
    bugs = [
        ("1. Забыли обновить состояние", "while count < 5:\n    print(count)\n    # забыли count += 1",
         "Условие никогда не станет ложным — бесконечный цикл. Проверьте, что внутри while есть строка, меняющая переменную из условия."),
        ("2. Ошибка на единицу в range()", "for i in range(1, 10):\n    print(i)  # не выведет 10!",
         "range(1, 10) даёт 1..9 — если нужно включить 10, это range(1, 11). Классическая off-by-one ошибка."),
        ("3. Неверный отступ тела", "for n in chisla:\nprint(n)  # SyntaxError: ожидался отступ",
         "Тело цикла обязано иметь отступ. Без него Python даже не запустит программу."),
        ("4. Счётчик обнулён внутри цикла", "for n in chisla:\n    kolichestvo = 0\n    kolichestvo += 1",
         "kolichestvo сбрасывается на каждой итерации — в конце в нём всегда 1, а не общее количество. Инициализация должна быть ДО цикла, не внутри."),
        ("5. break на неверном уровне отступа", "for n in chisla:\n    if n == 5:\n    break  # не в теле if!",
         "break, стоящий вне if (из-за отступа), сработает на первой же итерации независимо от условия. Проверяйте отступы так же внимательно, как и условия."),
        ("6. continue перед обновлением", "while count < 5:\n    if count == 2:\n        continue\n    print(count)\n    count += 1",
         "Когда count == 2, continue пропускает count += 1 — и count навсегда останется равным 2. Бесконечный цикл, и его особенно трудно заметить."),
        ("7. Путаница переменных вложенных циклов", "for i in range(3):\n    for i in range(4):\n        print(i)",
         "Внутренний цикл использует то же имя i, что и внешний — внешнее значение i затирается и теряется. Используйте разные имена, например i и j."),
        ("8. Неверный отрицательный шаг", "for n in range(10, 0):\n    print(n)  # ничего не выведет",
         "range(10, 0) с шагом по умолчанию +1 никогда не дойдёт от 10 до 0 — нужен range(10, 0, -1)."),
        ("9. Несоответствие состояния и условия", "while spisok:\n    print(spisok[0])\n    # забыли удалить элемент из spisok",
         "Условие проверяет spisok (пока список не пуст), но тело никогда не уменьшает список — бесконечный цикл, хотя выглядит иначе, чем счётчик."),
        ("10. Условие ложно с самого начала", "n = 10\nwhile n < 5:\n    print(n)\n    n += 1",
         "Тело не выполнится ни разу — ноль итераций. Это не ошибка сама по себе, но частая неожиданность, если условие не проверили заранее."),
    ]
    bugs_html = "".join(
        f'<div style="margin:18px 0;padding:16px 20px;background:var(--color-bg-surface,#FAFAFC);border-left:4px solid #DB2777;border-radius:10px">'
        f'<div style="font-family:Sora,sans-serif;font-weight:700;margin-bottom:8px">{title}</div>'
        f'{code_block("bug.py", code)}'
        f'<p style="margin-top:8px">{explain}</p></div>'
        for title, code, explain in bugs
    )

    body = f"""
    <h2>Как читать чужой (и свой) сломанный цикл</h2>
    <p>Циклы — самое частое место, где программа <em>работает</em>, но выдаёт не тот результат,
    или вообще зависает. Хорошая новость: подавляющее большинство таких ошибок укладывается
    всего в десяток типовых сценариев. Разберём их по одному.</p>

    {callout(
        "warning",
        "Важно: мы НЕ будем запускать зависающий код",
        "Некоторые примеры ниже описывают бесконечные циклы — в практике этой страницы вы "
        "будете <strong>читать и предсказывать</strong> поведение кода, а не запускать реальный "
        "зависающий цикл в браузере. Если код в вашей программе действительно завис — "
        "остановите его вручную (<code class=\"inline\">Ctrl+C</code> в терминале, «Interrupt "
        "kernel» в Jupyter), не дожидаясь самостоятельной остановки.",
    )}

    <h2>10 типичных ошибок циклов</h2>
    {bugs_html}

    <h2>Метод отладки: таблица трассировки вручную</h2>
    <p>Когда цикл ведёт себя не так, как ожидалось, самый надёжный способ разобраться — построить
    ту же таблицу трассировки, что мы использовали весь этот раздел, но теперь для реального,
    сломанного кода:</p>
    {comparison_table(
        ["Итерация", "Условие", "Переменные ДО тела", "Что выводится", "Переменные ПОСЛЕ тела"],
        [["1", "…", "…", "…", "…"], ["2", "…", "…", "…", "…"], ["…", "…", "…", "…", "…"]],
    )}
    {callout(
        "tip",
        "Заполняйте таблицу построчно, как будто вы — Python",
        "Не пытайтесь угадать результат целиком. Возьмите первую итерацию, честно распишите "
        "условие, значения переменных до и после тела — и повторяйте, пока не увидите, где "
        "ожидание разошлось с тем, что происходит на самом деле.",
    )}

    <h2>Off-by-one — отдельный разбор</h2>
    <p>«Ошибка на единицу» — самая частая семья багов циклов: цикл выполняется на один раз
    больше или меньше, чем нужно.</p>
    {two_up(
        range_diagram(start=1, stop=10, caption="range(1, 10) — последнее значение 9, не 10!"),
        range_diagram(start=1, stop=11, caption="range(1, 11) — правильно, если нужно дойти до 10 включительно"),
    )}
    <h3>Чек-лист граничных случаев</h3>
    {comparison_table(
        ["Вопрос", "Зачем проверять"],
        [
            ["Что произойдёт при нуле повторов (пустая последовательность)?", "тело цикла не выполнится вообще — не сломается ли код после цикла"],
            ["Что произойдёт при одном повторе?", "самый частый источник ошибок на единицу"],
            ["Включена ли последняя граница туда, куда нужно?", "stop у range() и срезов не включён по умолчанию"],
            ["Совпадает ли направление шага с направлением start→stop?", "положительный шаг для роста, отрицательный — для убывания"],
        ],
    )}
    {comparison_table(
        ["Случай", "Пример", "Сколько итераций"],
        [["Ноль", "for n in []:", "0 — тело не выполнится ни разу"],
         ["Один", "for n in [7]:", "1"],
         ["Много", "for n in range(1000):", "1000"]],
    )}

    <h2>Переменная цикла после его завершения</h2>
    {code_block("peremennaya_posle_cikla.py", "for n in range(5):\n    pass\n\nprint(n)  # 4 — последнее значение, которое приняла n\n")}
    {callout(
        "info",
        "Переменная не исчезает после for",
        "После завершения <code class=\"inline\">for</code> переменная цикла остаётся связана "
        "с последним полученным значением — в отличие от некоторых других языков, в Python у "
        "циклов нет отдельной «области видимости». Исключение: если последовательность была "
        "пустой, тело не выполнилось ни разу, и переменная цикла вообще не была создана — "
        "обращение к ней после цикла в этом случае вызовет <code class=\"inline\">NameError</code>.",
    )}

    <h2>Имена переменных цикла</h2>
    <p>Короткие имена вроде <code class="inline">i</code>, <code class="inline">j</code>,
    <code class="inline">k</code> — давняя традиция для простых числовых счётчиков (особенно во
    вложенных циклах), но как только переменная цикла имеет реальный смысл — называйте её
    осмысленно: <code class="inline">for slovo in slova:</code> читается понятнее, чем
    <code class="inline">for x in y:</code>.</p>
    {callout(
        "warning",
        "Затенение переменных (shadowing)",
        "Если внутри цикла переменной цикла присвоить новое значение вручную, или использовать "
        "имя, которое уже существовало снаружи цикла, — можно случайно затереть нужное "
        "значение. Особенно легко так ошибиться во вложенных циклах с одинаковыми именами "
        "(см. ошибку №7 выше).",
    )}

    <h2>Предпросмотр: изменение списка во время перебора</h2>
    {callout(
        "warning",
        "Не изменяйте список, который сейчас перебираете",
        "Удаление или добавление элементов в список прямо во время цикла "
        "<code class=\"inline\">for элемент in spisok:</code> может привести к тому, что "
        "некоторые элементы будут пропущены или обработаны дважды. Подробно разберём эту тему "
        "и безопасные способы её обхода в главе про списки — сейчас достаточно знать, что так "
        "делать не стоит.",
    )}

    <h2>Немного о производительности</h2>
    <p>Каждая лишняя вложенность цикла умножает число итераций (мы уже видели это на примере
    таблицы умножения). Пока считать нужно тысячи, а не миллионы значений — разница
    незаметна. Формальный разбор скорости алгоритмов ждёт вас в старших главах — сейчас
    достаточно интуиции: вложенный цикл внутри цикла обычно работает заметно медленнее одного
    цикла того же размера.</p>

    {practice_card(
        "10-17",
        "Практика: найди ошибку в цикле",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-17/index.html",
    )}
    {practice_card(
        "10-18",
        "Практика: off-by-one — посчитай итерации",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/10-18/index.html",
    )}
    """
    out = render_page(
        page_title="Отладка циклов: 10 типичных ошибок",
        description="10 именованных типов ошибок циклов, метод трассировки, off-by-one, переменная после for, имена и shadowing.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Отладка циклов", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Отладка циклов",
        lede="Десять типовых ошибок циклов и универсальный метод их поиска — таблица "
        "трассировки, построенная вручную, строка за строкой.",
        body_html=body,
        sidebar_groups=sidebar("10-13-otladka-ciklov.html"),
        nav=PageNav(prev_href="10-05-mini-proekt-ugadaj-v2.html", prev_label="Угадай число v2", next_href="10-06-avtomatiziruem-figury.html", next_label="Автоматизируем фигуры"),
    )
    write("10-13-otladka-ciklov.html", out)


# ---------------------------------------------------------------------------
# 10-06 · Автоматизируем квадрат и любую фигуру
# ---------------------------------------------------------------------------

def build_10_06() -> None:
    body = f"""
    <h2>Мини-проект — автоматизируем квадрат</h2>
    <p>Применим цикл к квадрату из главы 6. Обе версии кода ниже рисуют абсолютно одинаковый
    квадрат — единственная разница в том, сколько строк для этого понадобилось:</p>
    {classic_vs_modern(
        "Квадрат: 8 строк вручную против 2 строк с циклом",
        "Без цикла (глава 6)",
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)\n"
        "artist.forward(100)\nartist.right(90)",
        "С циклом for",
        "for _ in range(4):\n    artist.forward(100)\n    artist.right(90)",
        "цикл — тот же самый результат, но в 4 раза короче и с одним местом для изменения числа сторон.",
    )}
    {turtle_output("10-square", "avto_kvadrat.py", caption="Реальный результат — оба варианта кода выше рисуют именно этот квадрат", alt="Квадрат, нарисованный Turtle")}

    <h2 id="lyubaya-figura">Автоматизируем любую простую фигуру</h2>
    <p>Обобщим квадрат до шаблона, который рисует <strong>любой</strong> правильный
    многоугольник — используя формулу угла поворота из главы 6:</p>
    {math_formula(("row", "360°", ("mo", "÷"), "количество сторон", ("mo", "="), "угол поворота"), caption="Чем больше сторон — тем меньше угол поворота на каждом шаге")}
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
        "Поменяйте <code class=\"inline\">storony</code> на 3, 5, 6, 20 — программа "
        "автоматически нарисует треугольник, пятиугольник, шестиугольник или почти окружность, "
        "без единого изменения остального кода. Ниже — реальный результат для нескольких "
        "значений <code class=\"inline\">storony</code>.",
    )}

    <h3>Треугольник (storony = 3)</h3>
    {turtle_output("10-polygon-3", "treugolnik.py", caption="storony = 3, dlina = 110 → правильный треугольник", alt="Треугольник, нарисованный Turtle")}
    <h3>Пятиугольник (storony = 5)</h3>
    {turtle_output("10-polygon-5", "pyatiugolnik.py", caption="storony = 5, dlina = 75 → правильный пятиугольник", alt="Пятиугольник, нарисованный Turtle")}
    <h3>Шестиугольник (storony = 6)</h3>
    {turtle_output("10-polygon-6", "shestiugolnik.py", caption="storony = 6, dlina = 65 → правильный шестиугольник", alt="Шестиугольник, нарисованный Turtle")}
    <h3>Восьмиугольник (storony = 8)</h3>
    {turtle_output("10-polygon-8", "vosmiugolnik.py", caption="storony = 8, dlina = 55 → правильный восьмиугольник", alt="Восьмиугольник, нарисованный Turtle")}

    <h2>Мини-проект: студия автоматических многоугольников</h2>
    {exercise(2, "Студия многоугольников", "Оформите программу выше так, чтобы storony запрашивалось у пользователя через input() (не забудьте int()). Проверьте на нескольких значениях — включая большие, вроде 30 или 50, — и посмотрите, во что превращается фигура.")}

    {local_required_card(
        "10-06",
        "Практика: студия автоматических многоугольников",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-06/index.html",
    )}
    """
    out = render_page(
        page_title="Автоматизируем квадрат и любую фигуру",
        description="Переписываем квадрат и любой правильный многоугольник из главы 6 с помощью цикла for — с реальными выполненными изображениями.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Автоматизация фигур", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — автоматизируем рисование квадрата",
        lede="Возвращаемся к фигурам из главы 6 — на этот раз с циклами вместо ручного "
        "повторения, и с настоящими выполненными результатами.",
        body_html=body,
        sidebar_groups=sidebar("10-06-avtomatiziruem-figury.html"),
        nav=PageNav(prev_href="10-13-otladka-ciklov.html", prev_label="Отладка циклов", next_href="10-07-avtomatiziruem-mandalu.html", next_label="Автоматически рисуем мандалу"),
    )
    write("10-06-avtomatiziruem-figury.html", out)


# ---------------------------------------------------------------------------
# 10-07 · Автоматически рисуем мандалу
# ---------------------------------------------------------------------------

def build_10_07() -> None:
    body = f"""
    <p>В главе 6 мандала рисовалась циклом <code class="inline">while</code> с ручным
    увеличением угла. Теперь распишем её по стадиям — от одного лепестка до полного узора —
    и посмотрим на реальный результат каждой стадии.</p>

    <h2>Стадия 1 — один мотив</h2>
    <p><code class="inline">circle(60)</code> без параметра extent рисует полную окружность и
    возвращает черепашку точно в исходную точку и с исходным направлением:</p>
    {turtle_output("10-mandala-1", "mandala_stadiya_1.py", caption="Один мотив — просто circle(60)", alt="Один круг мандалы")}

    <h2>Стадия 2 — четыре мотива</h2>
    {code_block(
        "mandala_stadiya_2.py",
        "for _ in range(4):\n    artist.circle(60)\n    artist.left(90)\n",
    )}
    {turtle_output("10-mandala-4", "mandala_stadiya_2.py", caption="4 мотива, повёрнутых на 90° друг относительно друга", alt="Четыре круга мандалы")}

    <h2>Стадия 3 — двенадцать мотивов</h2>
    {code_block(
        "mandala_stadiya_3.py",
        "for _ in range(12):\n    artist.circle(60)\n    artist.left(30)\n",
    )}
    {turtle_output("10-mandala-12", "mandala_stadiya_3.py", caption="12 мотивов, повёрнутых на 30° — уже настоящий узор", alt="Двенадцать кругов мандалы")}

    <h2>Стадия 4 — полная мандала</h2>
    {code_block(
        "mandala_polnaya.py",
        "cvieta = ['#5B24F9', '#DB2777', '#059669']\nfor i in range(24):\n    artist.pencolor(cvieta[i % 3])\n    artist.circle(80)\n    artist.left(15)\n",
    )}
    {turtle_output("10-mandala-full", "mandala_polnaya.py", caption="24 мотива с чередованием трёх цветов через i % 3", alt="Полная разноцветная мандала")}
    {callout(
        "info",
        "range() с тремя аргументами — то же, что и ручной while",
        "<code class=\"inline\">for ugol in range(0, 360, shag_ugla):</code> генерирует именно "
        "те же числа, что мы получали вручную в главе 6: "
        "<code class=\"inline\">while ugol &lt; 360: ... ugol += shag_ugla</code>. Цикл "
        "<code class=\"inline\">for</code> просто делает это короче и без риска забыть "
        "увеличить счётчик.",
    )}
    {callout(
        "tip",
        "cvieta[i % 3] — остаток от деления как «зацикленный» индекс",
        "<code class=\"inline\">i % 3</code> даёт 0, 1, 2, 0, 1, 2, … — какое бы большое ни было "
        "<code class=\"inline\">i</code>, результат остатка всегда укладывается в диапазон "
        "индексов списка из 3 цветов. Этот приём — циклический перебор конечного набора значений "
        "— встречается очень часто.",
    )}

    {exercise(2, "Своя мандала", "Поменяйте количество мотивов (24 → 36), радиус (80 → 50) и список цветов — соберите собственный узор.")}

    {local_required_card(
        "10-07",
        "Практика: мандала через for + range(), по стадиям",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-07/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — автоматически рисуем мандалу",
        description="Мандала из главы 6, разложенная по стадиям — 1, 4, 12, 24 мотива — с реальными выполненными изображениями каждой стадии.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Автоматическая мандала", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — автоматически рисуем мандалу",
        lede="Та же мандала, что и в главе 6, — теперь по стадиям, короче и понятнее благодаря "
        "range() с тремя аргументами.",
        body_html=body,
        sidebar_groups=sidebar("10-07-avtomatiziruem-mandalu.html"),
        nav=PageNav(prev_href="10-06-avtomatiziruem-figury.html", prev_label="Автоматизация фигур", next_href="10-14-sluchajnye-uzory.html", next_label="Случайные узоры"),
    )
    write("10-07-avtomatiziruem-mandalu.html", out)


# ---------------------------------------------------------------------------
# 10-14 · Случайные узоры: блуждание и звёзды
# ---------------------------------------------------------------------------

def build_10_14() -> None:
    body = f"""
    <h2>Циклы и случайность</h2>
    <p>Модуль <code class="inline">random</code> из главы 9 отлично сочетается с циклами —
    каждая итерация может принимать своё, заранее неизвестное решение. Чтобы результат можно
    было воспроизвести и проверить, в примерах ниже используется
    <code class="inline">random.seed(...)</code> — она делает «случайную» последовательность
    одинаковой при каждом запуске.</p>

    <h2>Случайное блуждание</h2>
    {code_block(
        "sluchajnoe_bluzhdanie.py",
        "import random\nrandom.seed(7)\n\nfor _ in range(100):\n"
        "    artist.setheading(random.randint(0, 360))\n    artist.forward(10)\n",
    )}
    {turtle_output("10-random-walk", "sluchajnoe_bluzhdanie.py", caption="100 шагов в случайном направлении, seed(7) — при повторном запуске получится тот же путь", alt="Траектория случайного блуждания")}
    {callout(
        "tip",
        "seed() — не про случайность фигуры, а про воспроизводимость",
        "Без <code class=\"inline\">random.seed(...)</code> результат был бы каждый раз новым "
        "— что интересно для творчества, но неудобно для практики, где важно проверить "
        "конкретный, повторяемый результат.",
    )}

    <h2>Звёздное поле</h2>
    {code_block(
        "zvezdnoe_pole.py",
        "import random\nrandom.seed(3)\n\nfor _ in range(60):\n"
        "    x = random.randint(-190, 190)\n    y = random.randint(-190, 190)\n"
        "    artist.goto(x, y)\n    artist.dot(6, \"white\")\n",
    )}
    {turtle_output("10-star-field", "zvezdnoe_pole.py", caption="60 точек в случайных координатах — тёмный фон и dot() вместо линий", alt="Звёздное поле из точек")}

    {exercise(2, "Своё случайное блуждание", "Поменяйте seed на другое число и количество шагов — сравните, насколько по-разному выглядит путь.")}

    {local_required_card(
        "10-19",
        "Практика: случайное блуждание и звёздное поле",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-19/index.html",
    )}
    """
    out = render_page(
        page_title="Случайные узоры: блуждание и звёзды",
        description="Циклы + random: случайное блуждание черепашки и звёздное поле — с фиксированным seed() для воспроизводимости.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Случайные узоры", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Случайные узоры Turtle",
        lede="Каждая итерация цикла может сделать своё, заранее неизвестное движение — а seed() "
        "делает случайный результат воспроизводимым.",
        body_html=body,
        sidebar_groups=sidebar("10-14-sluchajnye-uzory.html"),
        nav=PageNav(prev_href="10-07-avtomatiziruem-mandalu.html", prev_label="Автоматическая мандала", next_href="10-15-setka-figur.html", next_label="Сетка фигур"),
    )
    write("10-14-sluchajnye-uzory.html", out)


# ---------------------------------------------------------------------------
# 10-15 · Сетка фигур: вложенные циклы в Turtle
# ---------------------------------------------------------------------------

def build_10_15() -> None:
    body = f"""
    <h2>Вложенные циклы как настоящая графика</h2>
    <p>Мы уже видели вложенные циклы на числах (таблица умножения) и на тексте (буквы внутри
    слов). Тот же самый паттерн «строки × столбцы» — основа для сеточного искусства:</p>
    {code_block(
        "setka_figur.py",
        "shag = 60\nfor row in range(5):\n    for col in range(5):\n"
        "        x = -140 + col * shag\n        y = -140 + row * shag\n"
        "        artist.goto(x, y)\n        artist.dot(16, '#5B24F9')\n",
    )}
    {turtle_output("10-grid", "setka_figur.py", caption="5 × 5 = 25 точек — внешний цикл по строкам, внутренний по столбцам", alt="Сетка из точек 5 на 5")}
    {callout(
        "tip",
        "Тот же формула, что и в таблице умножения",
        "row и col снова пробегают весь диапазон независимо друг от друга — общее число "
        "нарисованных точек равно <code class=\"inline\">5 * 5 = 25</code>, ровно как мы "
        "считали формулой «строки × столбцы» на странице про вложенные циклы.",
    )}

    {exercise(2, "Сетка фигур вместо точек", "Замените artist.dot(...) на маленький квадрат (ещё один, третий, вложенный цикл на 4 стороны) — получится сетка из маленьких квадратов вместо точек.")}

    {local_required_card(
        "10-20",
        "Практика: сетка фигур на вложенных циклах",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-20/index.html",
    )}
    """
    out = render_page(
        page_title="Сетка фигур: вложенные циклы в Turtle",
        description="Вложенные циклы rows × cols как основа сеточного искусства — реальная 5×5 сетка, выполненная Turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Сетка фигур", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Сетка фигур",
        lede="Тот же паттерн «строки × столбцы», что и в таблице умножения — только теперь он "
        "рисует, а не печатает числа.",
        body_html=body,
        sidebar_groups=sidebar("10-15-setka-figur.html"),
        nav=PageNav(prev_href="10-14-sluchajnye-uzory.html", prev_label="Случайные узоры", next_href="10-08-spirali-itogi.html", next_label="Спирали из дуг и итоги"),
    )
    write("10-15-setka-figur.html", out)


# ---------------------------------------------------------------------------
# 10-08 · Спирали из дуг и итоги
# ---------------------------------------------------------------------------

def build_10_08() -> None:
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
    {turtle_output("10-spiral", "spirali_iz_dug.py", caption="60 дуг, радиус растёт с 5 на 3 каждый шаг — раскручивающаяся спираль", alt="Спираль из растущих дуг")}
    {callout(
        "tip",
        "Изменение переменной внутри цикла — обычное дело",
        "В отличие от предыдущих примеров, здесь <code class=\"inline\">radius</code> меняется "
        "<em>на каждом шаге</em> цикла — это и создаёт эффект нарастающей спирали, а не "
        "повторяющегося узора.",
    )}

    <h2>break в Turtle — остановиться, не дойдя до конца</h2>
    <p><code class="inline">break</code> прекрасно работает и внутри циклов, рисующих графику
    — например, чтобы не выйти за границу экрана:</p>
    {code_block(
        "break_v_turtle.py",
        "dlina = 10\nfor _ in range(50):\n    if artist.xcor() > 150:\n        break\n"
        "    artist.forward(dlina)\n    artist.left(90)\n    dlina += 6\n",
    )}
    {turtle_output("10-break-turtle", "break_v_turtle.py", caption="Квадратная спираль обрывается посередине последнего витка — как только xcor() превысил 150, break остановил цикл", alt="Квадратная спираль, обрезанная break")}
    {callout(
        "info",
        "50 запланировано, но сработало меньше",
        "Цикл был готов выполниться 50 раз, но фактически завершился раньше — как только "
        "условие <code class=\"inline\">artist.xcor() &gt; 150</code> стало истинным. Именно "
        "поэтому последний отрезок на картинке короче, чем должен был бы быть полный виток "
        "— break прервал рисование строго посередине шага.",
    )}

    {exercise(2, "Спираль из квадратов", "Замените дугу на маленький квадрат (цикл на 4 стороны) внутри внешнего цикла — получится спираль из уменьшающихся или увеличивающихся квадратов.")}

    {local_required_card(
        "10-08",
        "Практика: спирали из дуг",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-08/index.html",
    )}
    {local_required_card(
        "10-21",
        "Практика: break в Turtle — квадратная спираль",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/10-21/index.html",
    )}

    <h2 id="itogi">Итоги главы</h2>
    <h3>Инструментарий циклов — на будущее</h3>
    {decision_map([
        ("Число повторов известно заранее", "for ... in range(n)"),
        ("Перебор готовой последовательности (строка, список)", "for элемент in последовательность"),
        ("Нужен и индекс, и значение", "for i, значение in enumerate(...)"),
        ("Число повторов заранее неизвестно", "while условие"),
        ("Условие остановки удобнее проверить в середине тела", "while True + break"),
        ("Нужно узнать, был ли break", "for/while … else"),
        ("Нужно пропустить один шаг, не выходя из цикла", "continue"),
    ], title="Итоговая шпаргалка главы 10", caption="Не жёсткие правила — ориентиры, которые становятся привычкой с практикой")}

    {summary_box("Что мы узнали в этой главе", [
        "Повторение — третья структура алгоритма после последовательности и ветвления (глава 9).",
        "<code class=\"inline\">for ... in range(n)</code> повторяет блок кода заданное число "
        "раз — цикл каждый раз спрашивает «есть следующий элемент?», а не выполняет тело N раз "
        "«по волшебству».",
        "<code class=\"inline\">range()</code> не список, а генератор чисел; его stop не "
        "включается — та же логика, что и у срезов строк из главы 8.",
        "<code class=\"inline\">enumerate()</code> даёт и индекс, и значение сразу; счётчик и "
        "накопитель — два базовых паттерна состояния внутри цикла.",
        "<code class=\"inline\">while</code> повторяет действие, пока условие остаётся "
        "истинным — используется, когда число повторов заранее неизвестно.",
        "<code class=\"inline\">break</code> прерывает цикл полностью; "
        "<code class=\"inline\">continue</code> пропускает текущий шаг; необязательный "
        "<code class=\"inline\">else</code> у цикла срабатывает только без break.",
        "Циклы можно вкладывать друг в друга — тогда внутренний цикл выполняется полностью на "
        "каждом шаге внешнего, а общее число итераций перемножается.",
        "Большинство ошибок циклов укладываются в десяток типовых сценариев — таблица "
        "трассировки, построенная вручную, помогает найти любой из них.",
        "Все фигуры из глав 6–7, нарисованные вручную, теперь можно записать в 2–4 строки с "
        "циклом — и мы увидели их реальные, по-настоящему выполненные результаты.",
    ])}

    <h2>Что дальше</h2>
    <p>Мы уже видели циклы, которые работают со списками чисел — <code class="inline">[4, 8, 15,
    16, 23, 42]</code>. В следующей главе разберём подробно, как устроены сами коллекции данных
    — списки, кортежи, множества и словари — то, ради чего циклы в первую очередь и существуют
    в реальных программах.</p>
    """
    out = render_page(
        page_title="Мини-проект — спирали из дуг",
        description="Итоговый мини-проект главы 10: спирали из дуг с растущим радиусом, break в Turtle, итоговый инструментарий и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 10", "index.html"), ("Спирали и итоги", "")],
        kicker="Глава 10 · Немного автоматизации!",
        h1="Мини-проект — спирали из дуг",
        lede="Завершаем главу узором, который меняется на каждом шаге цикла, — и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("10-08-spirali-itogi.html"),
        nav=PageNav(prev_href="10-15-setka-figur.html", prev_label="Сетка фигур", next_href="../glava-11/index.html", next_label="Глава 11: Очень много информации!"),
    )
    write("10-08-spirali-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_10_01()
    build_10_09()
    build_10_10()
    build_10_02()
    build_10_03()
    build_10_04()
    build_10_11()
    build_10_12()
    build_10_05()
    build_10_13()
    build_10_06()
    build_10_07()
    build_10_14()
    build_10_15()
    build_10_08()
