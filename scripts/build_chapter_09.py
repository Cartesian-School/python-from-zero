#!/usr/bin/env python3
"""Строит Главу 9: «Выполняй мою команду!» (site/chapters/glava-09/)."""

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
    comparison_number_line,
    comparison_table,
    condition_cascade,
    decision_diamond_diagram,
    decision_map,
    exercise,
    flow_diagram,
    flowchart,
    loop_preview_diagram,
    practice_card,
    precedence_ladder,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-09"

PAGES = [
    ("index.html", "Обзор главы"),
    ("09-07-algoritmy-i-komandy.html", "Алгоритмы и команды"),
    ("09-08-tri-struktury-i-vetvlenie.html", "Три структуры алгоритма и ветвление"),
    ("09-01-istina-ili-lozh.html", "Истина или ложь"),
    ("09-02-sravnenie-i-reshenie.html", "Сравниваем и принимаем решение"),
    ("09-09-ravno-i-sravnenie-strok.html", "== против =, и сравнение строк"),
    ("09-10-cepochki-sravnenij.html", "Цепочки сравнений"),
    ("09-11-truthiness-i-none.html", "Truthiness и None"),
    ("09-03-if-inache.html", "Если это произошло — выполни команду!"),
    ("09-12-elif-lestnica.html", "elif — несколько вариантов"),
    ("09-13-neskolko-if-protiv-elif.html", "Несколько if ≠ if/elif/else"),
    ("09-14-and.html", "and — все условия сразу"),
    ("09-15-or.html", "or — хотя бы одно"),
    ("09-16-not.html", "not — переворачиваем условие"),
    ("09-04-neskolko-uslovij.html", "Больше одного условия!"),
    ("09-17-short-circuit.html", "Short-circuit: Python иногда ленится"),
    ("09-18-in-not-in.html", "in / not in как условие"),
    ("09-19-is-vs-ravno.html", "is против =="),
    ("09-20-vlozhennye-uslovija.html", "Вложенные условия"),
    ("09-21-proektirovanie-uslovij.html", "Проектируем условие: ввод, валидация, границы"),
    ("09-22-otladka-logiki.html", "Отладка логических ошибок"),
    ("09-05-mini-proekt-ugadaj-chislo.html", "Мини-проект: «Угадай число»"),
    ("09-23-mini-proekt-klub-i-pogoda.html", "Мини-проекты: клуб и погода"),
    ("09-24-mini-proekt-ocenki-i-komandy.html", "Мини-проекты: оценки и команды"),
    ("09-06-nakoplenie-uslovij-itogi.html", "Условия накапливаются и итоги"),
]

PRACTICE_IDS = [
    "09-07", "09-08", "09-01", "09-02", "09-09", "09-10", "09-11", "09-03",
    "09-12", "09-13", "09-14", "09-15", "09-16", "09-04", "09-17", "09-18",
    "09-19", "09-20", "09-21", "09-22", "09-05", "09-23", "09-24", "09-06",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 9 · Условия", items),
        SidebarGroup("Практика", [
            NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def state_cards(cards: list[tuple[str, str, str]]) -> str:
    """Small side-by-side colored state cards, e.g. TRUE/FALSE. Each card is
    (label, sublabel, color)."""
    items = "".join(
        f'<div style="flex:1;min-width:160px;padding:24px;border-radius:16px;background:{color}12;'
        f'border:2px solid {color};text-align:center">'
        f'<div style="font-family:Sora,sans-serif;font-weight:800;font-size:26px;color:{color}">{label}</div>'
        f'<div style="font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:6px">{sub}</div>'
        f'</div>'
        for label, sub, color in cards
    )
    return f'<div style="display:flex;gap:16px;flex-wrap:wrap;margin:24px 0">{items}</div>'


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=9,
        description="До сих пор наши программы в основном выполняли команды одну за другой. "
        "Теперь мы научим их выбирать, какую команду выполнить дальше. Разберём алгоритмы и "
        "поток управления, как условия создают развилки и как Python принимает решения с "
        "помощью True, False и if/elif/else — и соберём первую настоящую игру.",
        meta_items=["[[icon:timer]] ~6–7 часов", "[[icon:code]] алгоритмы · условия · if/elif/else", "[[icon:practice]] 24 практики", "[[icon:game]] 5 мини-проектов"],
        sections=[
            ChapterSectionLink("9.1", "Алгоритмы и команды", "09-07-algoritmy-i-komandy.html"),
            ChapterSectionLink("9.2", "Три структуры алгоритма и ветвление", "09-08-tri-struktury-i-vetvlenie.html"),
            ChapterSectionLink("9.3", "Истина или ложь", "09-01-istina-ili-lozh.html"),
            ChapterSectionLink("9.4", "Сравниваем и принимаем решение", "09-02-sravnenie-i-reshenie.html"),
            ChapterSectionLink("9.5", "== против =, и сравнение строк", "09-09-ravno-i-sravnenie-strok.html"),
            ChapterSectionLink("9.6", "Цепочки сравнений", "09-10-cepochki-sravnenij.html"),
            ChapterSectionLink("9.7", "Truthiness и None", "09-11-truthiness-i-none.html"),
            ChapterSectionLink("9.8", "Если это произошло — выполни команду!", "09-03-if-inache.html"),
            ChapterSectionLink("9.9", "elif — несколько вариантов", "09-12-elif-lestnica.html"),
            ChapterSectionLink("9.10", "Несколько if ≠ if/elif/else", "09-13-neskolko-if-protiv-elif.html"),
            ChapterSectionLink("9.11", "and — все условия сразу", "09-14-and.html"),
            ChapterSectionLink("9.12", "or — хотя бы одно", "09-15-or.html"),
            ChapterSectionLink("9.13", "not — переворачиваем условие", "09-16-not.html"),
            ChapterSectionLink("9.14", "Больше одного условия!", "09-04-neskolko-uslovij.html"),
            ChapterSectionLink("9.15", "Short-circuit: Python иногда ленится", "09-17-short-circuit.html"),
            ChapterSectionLink("9.16", "in / not in как условие", "09-18-in-not-in.html"),
            ChapterSectionLink("9.17", "is против ==", "09-19-is-vs-ravno.html"),
            ChapterSectionLink("9.18", "Вложенные условия", "09-20-vlozhennye-uslovija.html"),
            ChapterSectionLink("9.19", "Проектируем условие", "09-21-proektirovanie-uslovij.html"),
            ChapterSectionLink("9.20", "Отладка логических ошибок", "09-22-otladka-logiki.html"),
            ChapterSectionLink("9.21", "Мини-проект — «Угадай число»", "09-05-mini-proekt-ugadaj-chislo.html"),
            ChapterSectionLink("9.22", "Мини-проекты — клуб и погода", "09-23-mini-proekt-klub-i-pogoda.html"),
            ChapterSectionLink("9.23", "Мини-проекты — оценки и команды", "09-24-mini-proekt-ocenki-i-komandy.html"),
            ChapterSectionLink("9.24", "Условия накапливаются и итоги", "09-06-nakoplenie-uslovij-itogi.html"),
            ChapterSectionLink("", "Итоги", "09-06-nakoplenie-uslovij-itogi.html#itogi"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 9.1 — Алгоритмы и команды
# ---------------------------------------------------------------------------

def build_07() -> None:
    legend = f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin:24px 0;padding:20px;
      background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      <div style="flex:1;min-width:150px;text-align:center">
        <svg viewBox="0 0 140 50" style="width:100%;max-width:140px;height:auto">
          <rect x="5" y="5" width="130" height="40" rx="20" fill="#0D0230"/>
        </svg>
        <div style="font-size:13px;margin-top:6px"><strong>Начало / конец</strong><br>терминатор</div>
      </div>
      <div style="flex:1;min-width:150px;text-align:center">
        <svg viewBox="0 0 140 50" style="width:100%;max-width:140px;height:auto">
          <rect x="5" y="5" width="130" height="40" rx="10" fill="#FAFAFC" stroke="#5B24F9" stroke-width="2"/>
        </svg>
        <div style="font-size:13px;margin-top:6px"><strong>Действие</strong><br>процесс / команда</div>
      </div>
      <div style="flex:1;min-width:150px;text-align:center">
        <svg viewBox="0 0 140 50" style="width:100%;max-width:140px;height:auto">
          <polygon points="27,5 135,5 113,45 5,45" fill="#EDE9FE" stroke="#5B24F9" stroke-width="2"/>
        </svg>
        <div style="font-size:13px;margin-top:6px"><strong>Ввод / вывод</strong><br>параллелограмм</div>
      </div>
      <div style="flex:1;min-width:150px;text-align:center">
        <svg viewBox="0 0 140 50" style="width:100%;max-width:140px;height:auto">
          <polygon points="70,3 137,25 70,47 3,25" fill="#5B24F9"/>
        </svg>
        <div style="font-size:13px;margin-top:6px"><strong>Условие?</strong><br>решение (ромб)</div>
      </div>
    </div>
    """
    tea_algo = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "process", "label": "Взять кружку"},
            {"kind": "process", "label": "Положить чай"},
            {"kind": "process", "label": "Вскипятить воду"},
            {"kind": "process", "label": "Налить воду"},
            {"kind": "process", "label": "Подождать"},
            {"kind": "process", "label": "Выпить чай"},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Алгоритм «приготовить чай» — все шесть действий, от старта до результата",
    )
    trace = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "output", "label": 'print("Старт")'},
            {"kind": "input", "label": "name = input(...)"},
            {"kind": "output", "label": 'print("Привет,", name)'},
            {"kind": "output", "label": 'print("Конец")'},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Тот же код как блок-схема — ввод и вывод нарисованы по-разному, не как одинаковые прямоугольники",
    )

    body = f"""
    <p>До сих пор наши программы выполняли одни и те же команды в одном и том же порядке при
    каждом запуске. Прежде чем научить программу <strong>выбирать</strong>, что делать дальше,
    разберёмся, что вообще значит «выполнять команды» — и договоримся об одном важном
    инструменте: языке блок-схем.</p>

    <h2>Форма блока — не украшение</h2>
    <p>Каждая фигура на блок-схеме имеет строгий смысл: она подсказывает, какого рода шаг
    алгоритма перед вами. Мы будем пользоваться этим языком на протяжении всей главы:</p>
    {legend}

    <h2>Что такое алгоритм</h2>
    <p><strong>Алгоритм</strong> — это понятная последовательность действий, которая приводит
    нас от исходной ситуации к нужному результату. Мы пользуемся алгоритмами каждый день, даже
    не называя их так:</p>

    <div style="margin:24px 0;padding:18px 20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      <div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;color:#5B24F9;margin-bottom:10px">АЛГОРИТМ: приготовить чай</div>
      <ol style="margin:0;padding-left:20px;font-size:15px;line-height:1.9">
        <li>Взять кружку.</li>
        <li>Положить чай.</li>
        <li>Вскипятить воду.</li>
        <li>Налить воду.</li>
        <li>Подождать.</li>
        <li>Выпить чай.</li>
      </ol>
    </div>
    {tea_algo}

    <p>Каждый отдельный шаг — это <strong>команда</strong> (инструкция): указание компьютеру
    (или человеку) выполнить конкретное действие. Весь упорядоченный набор шагов — это и есть
    алгоритм.</p>

    <h2>Команда и выражение — это разные вещи</h2>
    <p>Мы уже пользовались командами с самой первой программы в главе 1 — только не называли их
    так:</p>
    {code_block("znakomye_komandy.py", 'print("Привет")\n\nname = input("Как вас зовут? ")\n\nscore = 10\n')}
    <ul>
      <li><code class="inline">print(...)</code> — команда «показать что-то на экране».</li>
      <li><code class="inline">input(...)</code> — команда «запросить информацию у пользователя».</li>
      <li><code class="inline">score = 10</code> — команда «связать имя с значением» (присваивание).</li>
    </ul>

    {callout(
        "info",
        "2 + 2 — это выражение, а не команда",
        "<code class=\"inline\">2 + 2</code> само по себе ничего не «делает» — это "
        "<strong>выражение</strong>: оно вычисляется и производит значение "
        "(<code class=\"inline\">4</code>). А вот <code class=\"inline\">print(2 + 2)</code> — "
        "уже команда: она берёт значение выражения и что-то с ним делает (показывает на "
        "экране). Формальное различие пока не обязательно запоминать дословно — но не стоит "
        "путать «вычислить значение» и «выполнить действие».",
    )}

    <h2>Программа — это последовательность команд</h2>
    <p>Рассмотрим простую программу и проследим, как Python выполняет её команда за командой.
    Обратите внимание: <code class="inline">input()</code> нарисован как ВВОД, а
    <code class="inline">print()</code> — как ВЫВОД, разными фигурами, а не одинаковыми
    прямоугольниками:</p>
    {code_block("posledovatelnaya_programma.py", 'print("Старт")\n\nname = input("Как вас зовут? ")\n\nprint("Привет,", name)\n\nprint("Конец")\n')}
    {trace}

    <p>Обычно Python выполняет команды строго <strong>сверху вниз</strong>, одну за другой. Это
    называется <strong>последовательным</strong> (или линейным) выполнением: каждый следующий
    шаг идёт сразу после предыдущего, без пропусков и без выбора.</p>

    {practice_card(
        "09-07",
        "Практика: алгоритмы, команды и последовательное выполнение",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-07/index.html",
    )}
    """
    out = render_page(
        page_title="Алгоритмы и команды",
        description="Что такое алгоритм, чем команда отличается от выражения, и что значит последовательное выполнение программы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Алгоритмы и команды", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Алгоритмы и команды",
        lede="Прежде чем учить программу выбирать между вариантами, разберёмся, что вообще "
        "значит «выполнять команды» — и откуда берётся сам термин «алгоритм».",
        body_html=body,
        sidebar_groups=sidebar("09-07-algoritmy-i-komandy.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="09-08-tri-struktury-i-vetvlenie.html", next_label="Три структуры алгоритма и ветвление"),
    )
    write("09-07-algoritmy-i-komandy.html", out)


# ---------------------------------------------------------------------------
# 9.2 — Три структуры алгоритма и ветвление
# ---------------------------------------------------------------------------

def build_08() -> None:
    seq_diagram = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "process", "label": "A"},
            {"kind": "process", "label": "B"},
            {"kind": "process", "label": "C"},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Последовательность — каждый шаг идёт сразу после предыдущего",
    )
    branch_diagram = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "decision", "label": "условие?", "yes": [{"kind": "process", "label": "A"}], "no": [{"kind": "process", "label": "B"}]},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Ветвление — выбирается ровно один путь, оба варианта затем сходятся",
    )
    repeat_diagram = loop_preview_diagram(
        action_label="Действие",
        question_label="Повторить?",
        caption="Повторение — предварительная схема, синтаксис циклов изучим в главе 10",
    )
    umbrella_algo = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "decision", "label": "Идёт дождь?", "yes": [{"kind": "process", "label": "Взять зонт"}], "no": [{"kind": "process", "label": "Идти без зонта"}]},
            {"kind": "process", "label": "Выйти из дома"},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Ветвление, а затем продолжение: обе ветки сходятся и алгоритм идёт дальше",
    )
    human_python = comparison_table(
        ["Человек", "Python"],
        [["да", "<code class=\"inline\">True</code>"], ["нет", "<code class=\"inline\">False</code>"]],
    )

    body = f"""
    <h2>Три структуры, из которых строится любой алгоритм</h2>
    <p>Почти любой алгоритм — от рецепта чая до огромной программы — собирается всего из трёх
    базовых идей:</p>
    {decision_map([
        ("Команды идут одна за другой, без выбора?", "Последовательность — уже знакомо"),
        ("Нужно выбрать ОДИН путь из нескольких, в зависимости от условия?", "Ветвление — эта глава"),
        ("Нужно повторить действие несколько раз?", "Повторение — глава 10"),
    ], title="Какая структура нужна?")}

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:24px 0">
      <div>{seq_diagram}</div>
      <div>{branch_diagram}</div>
      <div>{repeat_diagram}</div>
    </div>

    <h2>Когда одной последовательности не хватает</h2>
    <p>Простой линейный алгоритм — «выйти из дома, идти гулять» — прекрасно работает, пока в
    реальной жизни не появляется вопрос. Идёт дождь?</p>

    <h2>Что такое ветвление</h2>
    <p><strong>Ветвление</strong> — это место в алгоритме, где дальнейшие действия зависят от
    ответа на вопрос. Каждая развилка начинается с <strong>условия</strong> — вопроса, на
    который можно ответить «да» или «нет». Программа не выбирает ветку случайно: она вычисляет
    условие, и результат определяет путь. Какую бы ветку ни выбрала программа, дальше
    выполнение обычно продолжается с одного и того же следующего шага:</p>
    {umbrella_algo}
    <p>Это уже не чисто последовательный алгоритм — он <strong>ветвится</strong>, а затем обе
    ветки снова сходятся к шагу «Выйти из дома».</p>

    <h2>От «да/нет» к True/False</h2>
    <p>Человеческие «да» и «нет» в Python превращаются в два особых значения:</p>
    {human_python}
    <p>Именно поэтому следующий раздел — про <code class="inline">True</code> и
    <code class="inline">False</code> — теперь не абстрактная тема «из ниоткуда», а прямое
    продолжение идеи ветвления.</p>

    {practice_card(
        "09-08",
        "Практика: три структуры алгоритма и ветвление",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-08/index.html",
    )}
    """
    out = render_page(
        page_title="Три структуры алгоритма и ветвление",
        description="Последовательность, ветвление и повторение — три базовые структуры алгоритмов; что такое ветвление и условие.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Три структуры и ветвление", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Три структуры алгоритма и ветвление",
        lede="Любой алгоритм собирается из трёх идей: последовательность, ветвление, "
        "повторение. Эта глава — про вторую из них.",
        body_html=body,
        sidebar_groups=sidebar("09-08-tri-struktury-i-vetvlenie.html"),
        nav=PageNav(prev_href="09-07-algoritmy-i-komandy.html", prev_label="Алгоритмы и команды", next_href="09-01-istina-ili-lozh.html", next_label="Истина или ложь"),
    )
    write("09-08-tri-struktury-i-vetvlenie.html", out)


# ---------------------------------------------------------------------------
# 9.3 — True/False, bool (существующий, расширяем)
# ---------------------------------------------------------------------------

def build_01() -> None:
    cards = state_cards([
        ("TRUE", "✓ условие выполнено", "#059669"),
        ("FALSE", "✗ условие не выполнено", "#DB2777"),
    ])

    body = f"""
    <p>Мы выяснили: программа отвечает на вопросы «да» или «нет» значениями
    <code class="inline">True</code> и <code class="inline">False</code>. Пора познакомиться с
    типом данных, который их хранит.</p>

    <h2>bool — логический тип с двумя значениями</h2>
    <p>Тип <code class="inline">bool</code> имеет ровно два возможных значения:</p>
    {cards}
    <p>Обратите внимание: <code class="inline">True</code> и <code class="inline">False</code>
    пишутся с заглавной буквы — это ключевые слова Python, а не обычный текст.</p>
    {code_block("bool.py", "is_sunny = True\nis_raining = False\nprint(is_sunny, type(is_sunny))\n# True <class 'bool'>\n")}

    <h2>bool — это не строка!</h2>
    <p>Легко перепутать <code class="inline">True</code> (значение типа bool) со строкой
    <code class="inline">"True"</code> — но это совершенно разные вещи:</p>
    {code_block("bool_ne_stroka.py", 'print(type(True))     # <class \'bool\'>\nprint(type("True"))   # <class \'str\'>\nprint(True == "True")  # False — разные типы, разные значения\n')}

    {callout(
        "warning",
        "\"True\" — это просто текст из четырёх букв",
        "Строка <code class=\"inline\">\"True\"</code> не имеет никакого особого смысла для "
        "Python — это обычный непустой текст, который, как мы увидим дальше, при проверке "
        "истинности сам ведёт себя как <code class=\"inline\">True</code>, но это два разных "
        "явления, которые легко перепутать.",
    )}

    <h2>Как чаще всего получают bool</h2>
    <p>Вручную писать <code class="inline">True</code>/<code class="inline">False</code>
    приходится редко — обычно их получают в результате сравнения (следующий раздел):</p>
    {code_block("sravnenie_bool.py", "print(5 > 3)     # True\nprint(5 == 3)    # False\n")}

    {practice_card(
        "09-01",
        "Практика: тип bool и True/False",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-01/index.html",
    )}
    """
    out = render_page(
        page_title="Истина или ложь",
        description="Логический тип bool в Python: True и False, и почему bool — это не строка.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Истина или ложь", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Истина или ложь",
        lede="Прежде чем программа сможет принимать решения, ей нужен способ хранить сам "
        "результат решения — логический тип bool.",
        body_html=body,
        sidebar_groups=sidebar("09-01-istina-ili-lozh.html"),
        nav=PageNav(prev_href="09-08-tri-struktury-i-vetvlenie.html", prev_label="Три структуры и ветвление", next_href="09-02-sravnenie-i-reshenie.html", next_label="Сравниваем и принимаем решение"),
    )
    write("09-01-istina-ili-lozh.html", out)


# ---------------------------------------------------------------------------
# 9.4 — Сравнение чисел (существующий, СИЛЬНО расширяем)
# ---------------------------------------------------------------------------

def build_02() -> None:
    machine_true = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "input", "label": "Значения: 5 и 3"},
            {"kind": "process", "label": "Сравнение: 5 > 3"},
            {"kind": "output", "label": "Результат: True"},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="5 > 3 — сравнение выполнилось УСПЕШНО и дало True",
    )
    machine_false = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "input", "label": "Значения: 2 и 3"},
            {"kind": "process", "label": "Сравнение: 2 > 3"},
            {"kind": "output", "label": "Результат: False"},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="2 > 3 — сравнение ТОЖЕ выполнилось успешно, просто дало False",
    )
    nl_ge = comparison_number_line(axis_lo=0, axis_hi=30, lo_bound=18, lo_inclusive=True, caption="age >= 18 — закрашенная точка: 18 включено")
    nl_lt = comparison_number_line(axis_lo=-10, axis_hi=10, hi_bound=0, hi_inclusive=False, caption="temperature < 0 — пустая точка: 0 НЕ включён")

    ops_table = comparison_table(
        ["Вопрос", "Математика", "Python", "Пример", "Результат"],
        [
            ["равно?", "=", "<code class=\"inline\">==</code>", "<code class=\"inline\">5 == 5</code>", "True"],
            ["не равно?", "≠", "<code class=\"inline\">!=</code>", "<code class=\"inline\">5 != 3</code>", "True"],
            ["больше?", "&gt;", "<code class=\"inline\">&gt;</code>", "<code class=\"inline\">5 &gt; 3</code>", "True"],
            ["меньше?", "&lt;", "<code class=\"inline\">&lt;</code>", "<code class=\"inline\">5 &lt; 3</code>", "False"],
            ["больше или равно?", "≥", "<code class=\"inline\">&gt;=</code>", "<code class=\"inline\">5 &gt;= 5</code>", "True"],
            ["меньше или равно?", "≤", "<code class=\"inline\">&lt;=</code>", "<code class=\"inline\">5 &lt;= 3</code>", "False"],
        ],
    )

    body = f"""
    <h2>Сравнение — это шаг алгоритма, который производит bool</h2>
    <p>Возьмите два значения, примените оператор сравнения — и получите ровно одно из двух:
    <code class="inline">True</code> или <code class="inline">False</code>. Оба исхода —
    <strong>одинаково успешный</strong> результат: сравнение не «падает» и не «не срабатывает»,
    когда ответ False — оно просто честно отвечает «нет».</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:24px 0">
      <div>{machine_true}</div>
      <div>{machine_false}</div>
    </div>
    {code_block("sravnenie.py", "print(5 > 3)     # True\nprint(5 == 3)    # False\n")}
    {callout(
        "info",
        "False — тоже правильный ответ",
        "<code class=\"inline\">2 &gt; 3</code> выполняется так же успешно, как "
        "<code class=\"inline\">5 &gt; 3</code> — просто их результаты разные. Не путайте "
        "«условие ложно» с «программа не сработала»: это два совершенно разных явления, и мы "
        "вернёмся к этому различию в разделе про <code class=\"inline\">if</code>.",
    )}

    <h2>Все шесть операторов сравнения</h2>
    {ops_table}
    {code_block(
        "operatory_sravneniya.py",
        "print(5 == 5)   # равно\n"
        "print(5 != 3)   # не равно\n"
        "print(5 > 3)    # больше\n"
        "print(5 < 3)    # меньше\n"
        "print(5 >= 5)   # больше или равно\n"
        "print(5 <= 3)   # меньше или равно\n",
    )}

    <h2>Числовая прямая — увидеть сравнение</h2>
    <p><code class="inline">age &gt;= 18</code> означает «age больше ИЛИ равно 18». Гораздо
    нагляднее увидеть это на числовой прямой:</p>
    {nl_ge}
    <p>Слева от 18 — область, где условие ложно; сама точка 18 и всё, что правее, — область,
    где условие истинно. Точка на 18 <strong>закрашена</strong>: значит, 18 входит в истинную
    область (<code class="inline">&gt;=</code> включает границу).</p>

    <h2>Открытая и закрытая граница</h2>
    <p>Сравните с <code class="inline">temperature &lt; 0</code>:</p>
    {nl_lt}
    <p>Здесь точка на 0 <strong>пустая</strong> (не закрашена) — граница НЕ включена: значение
    <code class="inline">0</code> не удовлетворяет условию <code class="inline">&lt; 0</code>.
    Условимся так на протяжении всей главы:</p>
    <ul>
      <li><strong>закрашенная точка</strong> — граница включена (<code class="inline">&gt;=</code>, <code class="inline">&lt;=</code>)</li>
      <li><strong>пустая точка</strong> — граница исключена (<code class="inline">&gt;</code>, <code class="inline">&lt;</code>)</li>
    </ul>

    {practice_card(
        "09-02",
        "Практика: шесть операторов сравнения и границы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-02/index.html",
    )}
    """
    out = render_page(
        page_title="Сравниваем и принимаем решение",
        description="Шесть операторов сравнения ==, !=, <, >, <=, >= и наглядное представление границ на числовой прямой.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Сравниваем и решаем", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Сравниваем и принимаем решение",
        lede="Шесть операторов, которые превращают два значения в один bool — и числовая "
        "прямая, чтобы увидеть их границы.",
        body_html=body,
        sidebar_groups=sidebar("09-02-sravnenie-i-reshenie.html"),
        nav=PageNav(prev_href="09-01-istina-ili-lozh.html", prev_label="Истина или ложь", next_href="09-09-ravno-i-sravnenie-strok.html", next_label="== против =, и сравнение строк"),
    )
    write("09-02-sravnenie-i-reshenie.html", out)


# ---------------------------------------------------------------------------
# 9.5 — == vs =, сравнение строк
# ---------------------------------------------------------------------------

def build_09() -> None:
    eq_cvm = classic_vs_modern(
        "= — присваивание, == — сравнение",
        "= (один знак) — ПРИСВАИВАНИЕ",
        'name = "Anna"\n\n# смысл: связать имя name\n# со значением "Anna".\n# Ничего не сравнивается!',
        "== (два знака) — СРАВНЕНИЕ",
        'name == "Anna"\n\n# смысл: равны ли значения?\n# результат — True или False,\n# сама переменная не меняется',
        "Перепутать <code class=\"inline\">=</code> и <code class=\"inline\">==</code> — одна из "
        "самых частых ошибок у новичков в любом языке программирования. Если в условии "
        "<code class=\"inline\">if</code> случайно написать одиночный <code class=\"inline\">=</code>, "
        "Python сразу сообщит об ошибке синтаксиса — присваивание нельзя использовать как "
        "условие, так что эта конкретная ошибка, к счастью, не проходит незамеченной.",
    )

    body = f"""
    <h2>= — это не ==</h2>
    <p>Этот раздел заслуживает отдельного внимания — путаница между одиночным и двойным
    «равно» встречается постоянно.</p>
    {eq_cvm}

    <h2>!= — «не равно»</h2>
    <p><code class="inline">!=</code> — оператор, обратный <code class="inline">==</code>:</p>
    {code_block("ne_ravno.py", 'password = ""\nprint(password != "")   # False — пароль как раз пустой\n\npassword = "secret123"\nprint(password != "")   # True — пароль НЕ пустой\n')}

    <h2>Сравнение строк</h2>
    <p>Мы видели в главе 8: строки сравниваются по символам, и регистр важен:</p>
    {code_block("sravnenie_strok.py", 'print("Python" == "python")   # False — регистр важен\nprint("cat" < "dog")          # True\n')}

    {callout(
        "info",
        "«cat» < «dog» — не совсем «по алфавиту»",
        "Python сравнивает строки по <strong>кодовым позициям символов</strong>, а не по "
        "«человеческому» алфавитному порядку словаря. Для обычных латинских букв в одном "
        "регистре результат обычно совпадает с интуицией, но при смешении регистров или "
        "разных алфавитов это уже не всегда «алфавитный порядок» в привычном смысле.",
    )}

    {callout(
        "tip",
        "[[icon:experiment]] ЧУТЬ ГЛУБЖЕ — код символа",
        "Каждому символу соответствует число — его код. Функция <code class=\"inline\">ord()</code> "
        "показывает его: <code class=\"inline\">ord(\"A\")</code> → 65, "
        "<code class=\"inline\">ord(\"a\")</code> → 97. Именно эти числа Python на самом деле "
        "сравнивает. Для этой главы знать точные числа не обязательно — важно лишь понимать, "
        "что сравнение строк работает через них, а не через словарь.",
    )}

    <h2>Нормализация перед сравнением</h2>
    <p>Пользователь может ввести «Да», «ДА», « да» — с разным регистром и пробелами. Методы
    строк из главы 8 решают эту проблему одной строкой:</p>
    {code_block("normalizaciya.py", 'answer = input("Продолжить? ").strip().lower()\n\nif answer == "да":\n    print("Продолжаем")\n')}
    <p><code class="inline">.strip()</code> убирает случайные пробелы по краям,
    <code class="inline">.lower()</code> приводит к нижнему регистру — теперь неважно, как
    именно пользователь набрал ответ.</p>

    {practice_card(
        "09-09",
        "Практика: == против =, != и сравнение строк",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-09/index.html",
    )}
    """
    out = render_page(
        page_title="== против =, и сравнение строк",
        description="Разница между присваиванием (=) и сравнением (==), оператор !=, сравнение строк и нормализация ввода.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("== против =", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="== против =, и сравнение строк",
        lede="Одна из самых частых ошибок новичков — и как строки из главы 8 участвуют в "
        "условиях.",
        body_html=body,
        sidebar_groups=sidebar("09-09-ravno-i-sravnenie-strok.html"),
        nav=PageNav(prev_href="09-02-sravnenie-i-reshenie.html", prev_label="Сравниваем и решаем", next_href="09-10-cepochki-sravnenij.html", next_label="Цепочки сравнений"),
    )
    write("09-09-ravno-i-sravnenie-strok.html", out)


# ---------------------------------------------------------------------------
# 9.6 — Цепочки сравнений
# ---------------------------------------------------------------------------

def build_10() -> None:
    nl_chain1 = comparison_number_line(axis_lo=0, axis_hi=80, lo_bound=18, hi_bound=65, caption="18 <= age <= 65 — включённый диапазон")
    nl_chain2 = comparison_number_line(axis_lo=-20, axis_hi=40, lo_bound=-10, hi_bound=30, caption="-10 < temperature < 30")

    body = f"""
    <h2>Диапазон значений — цепочка сравнений</h2>
    <p>Частая задача: проверить, что значение находится МЕЖДУ двумя границами. В Python это
    можно записать одной изящной цепочкой:</p>
    {code_block("cepochka.py", "age = 30\nprint(18 <= age <= 65)   # True\n")}
    {nl_chain1}
    <p>Это ровно то же самое, что:</p>
    {code_block("cepochka_razvernuto.py", "age = 30\nprint(age >= 18 and age <= 65)   # тот же результат\n")}
    <p>но цепочка <code class="inline">18 &lt;= age &lt;= 65</code> читается ближе к тому, как
    мы формулируем это на человеческом языке — «age между 18 и 65».</p>

    <h2>Ещё примеры</h2>
    {code_block("primery_cepochek.py", 'print(0 <= score <= 100)      # score от 0 до 100 включительно\nprint(-10 < temperature < 30) # температура строго между -10 и 30\nprint(1 <= month <= 12)       # month — допустимый номер месяца\n')}
    {nl_chain2}
    <p>Обратите внимание: здесь обе границы <strong>открытые</strong> (строгие
    <code class="inline">&lt;</code>) — значения -10 и 30 сами НЕ входят в диапазон, что видно
    по пустым точкам на прямой.</p>

    {exercise(1, "Допустимый месяц", "Даны значения month = 0, month = 1, month = 12, month = 13. Для каждого предскажите результат 1 <= month <= 12, затем проверьте в коде.")}

    {practice_card(
        "09-10",
        "Практика: цепочки сравнений",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-10/index.html",
    )}
    """
    out = render_page(
        page_title="Цепочки сравнений",
        description="Цепочки сравнений вида a <= x <= b в Python — удобная запись диапазона значений.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Цепочки сравнений", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Цепочки сравнений",
        lede="Как проверить, что значение лежит в диапазоне, — одной изящной строкой вместо "
        "двух отдельных сравнений.",
        body_html=body,
        sidebar_groups=sidebar("09-10-cepochki-sravnenij.html"),
        nav=PageNav(prev_href="09-09-ravno-i-sravnenie-strok.html", prev_label="== против =", next_href="09-11-truthiness-i-none.html", next_label="Truthiness и None"),
    )
    write("09-10-cepochki-sravnenij.html", out)


# ---------------------------------------------------------------------------
# 9.7 — Truthiness и None
# ---------------------------------------------------------------------------

def build_11() -> None:
    falsy_table = comparison_table(
        ["Значение", "bool(...)", "Почему"],
        [
            ["<code class=\"inline\">False</code>", "False", "уже ложь"],
            ["<code class=\"inline\">None</code>", "False", "«здесь нет значения»"],
            ["<code class=\"inline\">0</code>, <code class=\"inline\">0.0</code>", "False", "ноль считается ложью"],
            ["<code class=\"inline\">\"\"</code>", "False", "пустая строка"],
            ["<code class=\"inline\">[]</code>, <code class=\"inline\">{}</code>", "False", "пустые коллекции — подробно изучим позже"],
        ],
    )
    truthy_table = comparison_table(
        ["Значение", "bool(...)", "Почему"],
        [
            ["<code class=\"inline\">True</code>", "True", "уже истина"],
            ["<code class=\"inline\">-10</code>, <code class=\"inline\">1</code>, <code class=\"inline\">42</code>", "True", "любое ненулевое число"],
            ["<code class=\"inline\">\"нет\"</code>, <code class=\"inline\">\"0\"</code>, <code class=\"inline\">\"False\"</code>", "True", "любая непустая строка — даже такая!"],
        ],
    )

    body = f"""
    <h2>Условию не всегда нужно явное сравнение</h2>
    <p>Мы уже видели в главе 8: пустая строка ведёт себя как <code class="inline">False</code>,
    а непустая — как <code class="inline">True</code>. Это работает не только для строк —
    Python умеет спросить о ЛЮБОМ значении: «ведёшь ли ты себя как истина или как ложь?» Это
    называется <strong>truthiness</strong> («истинностью») значения.</p>

    <h2>Falsy — значения, которые ведут себя как False</h2>
    {falsy_table}

    <h2>Truthy — почти всё остальное</h2>
    {truthy_table}

    {code_block("truthiness.py", 'print(bool(0))        # False\nprint(bool(1))        # True\nprint(bool(-10))      # True — отрицательное тоже не ноль!\nprint(bool(""))       # False\nprint(bool("False"))  # True — это непустая СТРОКА, а не значение False\nprint(bool("0"))      # True — тоже непустая строка\n')}

    {callout(
        "warning",
        "Текст \"False\" — это не значение False!",
        "<code class=\"inline\">bool(\"False\")</code> равно <code class=\"inline\">True</code>, "
        "потому что строка <code class=\"inline\">\"False\"</code> состоит из пяти символов — "
        "она непустая, а значит truthy. То же самое с <code class=\"inline\">\"0\"</code>: это "
        "текст из одного символа, а не число ноль.",
    )}

    <h2>None — «здесь нет значения»</h2>
    <p><code class="inline">None</code> — особое значение, означающее примерно «здесь нет
    значения» (а не 0, не False и не пустая строка):</p>
    {code_block("none.py", 'value = None\n\nprint(value is None)       # True\nprint(bool(value))          # False — None тоже falsy\nprint(value == 0)           # False — None это не 0\nprint(value == "")          # False — None это не пустая строка\n')}
    <p>Обратите внимание на оператор <code class="inline">is</code> вместо
    <code class="inline">==</code> — к разнице между ними мы вернёмся в разделе 9.17.</p>

    {practice_card(
        "09-11",
        "Практика: truthiness и None",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-11/index.html",
    )}
    """
    out = render_page(
        page_title="Truthiness и None",
        description="Что Python считает истинным и ложным без явного сравнения — truthiness — и особое значение None.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Truthiness и None", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Truthiness и None",
        lede="Условию не всегда нужно явное сравнение — Python умеет спросить о любом "
        "значении, истинно оно или ложно.",
        body_html=body,
        sidebar_groups=sidebar("09-11-truthiness-i-none.html"),
        nav=PageNav(prev_href="09-10-cepochki-sravnenij.html", prev_label="Цепочки сравнений", next_href="09-03-if-inache.html", next_label="Если это произошло — выполни команду!"),
    )
    write("09-11-truthiness-i-none.html", out)


# ---------------------------------------------------------------------------
# 9.8 — Первый if, отступ, if/else (существующий, СИЛЬНО расширяем)
# ---------------------------------------------------------------------------

def build_03() -> None:
    pseudocode_diagram = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "input", "label": "temperature"},
            {"kind": "decision", "label": "temperature < 0?", "yes": [{"kind": "output", "label": '"мороз"'}], "no": []},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Сначала решаем задачу как схему — потом переводим на Python",
    )
    if_flow = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "input", "label": "temperature"},
            {"kind": "decision", "label": "temperature < 0?", "yes": [{"kind": "output", "label": '"Мороз"'}], "no": []},
            {"kind": "process", "label": "Продолжаем программу"},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Первый if — при False блок просто пропускается, выполнение идёт дальше",
    )
    if_else_flow = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {"kind": "input", "label": "age"},
            {"kind": "decision", "label": "age >= 18?", "yes": [{"kind": "output", "label": '"Доступ разрешён"'}], "no": [{"kind": "output", "label": '"Доступ запрещён"'}]},
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="if/else: два пути — один из них выполнится обязательно, и оба сходятся дальше",
    )

    body = f"""
    <h2>Сначала схема, потом код</h2>
    <p>Возьмём задачу: «если температура ниже нуля, показать „мороз“». Прежде чем писать
    Python, решим её как схему:</p>
    {pseudocode_diagram}
    <p>Где здесь вопрос? Какая ветка выполнится? Что произойдёт, если условие ложно? Только
    когда ответы понятны — переводим схему на Python.</p>

    <h2>Первый if</h2>
    {code_block("if_prostoj.py", 'temperature = -5\n\nif temperature < 0:\n    print("Мороз")\n')}
    <p>Разберём по словам:</p>
    <ul>
      <li><code class="inline">if</code> — «если»</li>
      <li><code class="inline">temperature &lt; 0</code> — условие (вопрос)</li>
      <li><code class="inline">:</code> — здесь начинается блок команд</li>
      <li>строка с отступом — команда, принадлежащая этому блоку</li>
    </ul>

    <h2>Полный пример с обеими ветками</h2>
    {code_block(
        "if.py",
        "age = 20\n\n"
        "if age >= 18:\n"
        '    print("Доступ разрешён.")\n',
    )}
    {if_flow}
    <p>Если условие ложно, блок <code class="inline">if</code> просто <strong>пропускается</strong>
    — программа не «падает», не выдаёт ошибку, а идёт дальше как ни в чём не бывало. Ложное
    условие не означает «программа остановилась»: она продолжает выполнение со следующего шага.</p>

    <h2>Отступ — это часть программы</h2>
    <p>В Python отступ — не просто оформление для красоты. Именно отступом Python определяет,
    какие строки относятся к блоку <code class="inline">if</code>, а какие уже нет:</p>
    {code_block(
        "blok_komand.py",
        'if temperature < 0:\n'
        '    print("На улице мороз.")\n'
        '    print("Наденьте тёплую куртку.")\n'
        '    print("Не забудьте перчатки.")\n\n'
        'print("Программа закончена")\n',
    )}
    <p>Первые три команды имеют одинаковый отступ — все они относятся к блоку
    <code class="inline">if</code>. Последняя строка отступа не имеет — она выполнится
    <strong>всегда</strong>, независимо от условия.</p>

    {callout(
        "tip",
        "Рекомендация: 4 пробела",
        "Стандартный отступ в Python — 4 пробела на один уровень вложенности. Не смешивайте "
        "пробелы и табуляцию в одном файле — Python в некоторых случаях сочтёт это ошибкой.",
    )}

    <h2>IndentationError</h2>
    <p>Если забыть про отступ — Python не сможет понять, что относится к блоку:</p>
    {code_block("indentationerror.py", 'if age >= 18:\nprint("OK")\n# IndentationError: expected an indented block after \'if\' statement\n')}
    <p><strong>Исправление:</strong> добавить отступ перед <code class="inline">print</code>.</p>

    <h2 id="inache">А иначе? — if/else</h2>
    <p><code class="inline">else</code> задаёт блок кода, который выполнится, если условие
    оказалось ложным:</p>
    {code_block(
        "if_else.py",
        "age = 15\n\n"
        "if age >= 18:\n"
        '    print("Доступ разрешён.")\n'
        "else:\n"
        '    print("Доступ запрещён — вам ещё нет 18.")\n',
    )}
    {if_else_flow}

    <h2>Ветки снова сходятся</h2>
    <p>Какая бы ветка ни выполнилась — <code class="inline">if</code> или
    <code class="inline">else</code> — дальше программа обычно продолжается с одного и того же
    следующего шага. На схеме выше это видно по стрелкам, сходящимся в общую точку перед
    <code class="inline">КОНЕЦ</code>.</p>

    {practice_card(
        "09-03",
        "Практика: первый if, отступ и if/else",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-03/index.html",
    )}
    """
    out = render_page(
        page_title="Если это произошло — выполни команду!",
        description="Первый условный оператор if, отступ как часть синтаксиса, IndentationError и альтернативная ветка else.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("if / else", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Если это произошло — выполни команду!",
        lede="Первый настоящий условный оператор: код, который выполняется только при "
        "определённых обстоятельствах — сначала как схема, потом на Python.",
        body_html=body,
        sidebar_groups=sidebar("09-03-if-inache.html"),
        nav=PageNav(prev_href="09-11-truthiness-i-none.html", prev_label="Truthiness и None", next_href="09-12-elif-lestnica.html", next_label="elif — несколько вариантов"),
    )
    write("09-03-if-inache.html", out)


# ---------------------------------------------------------------------------
# 9.9 — elif лестница
# ---------------------------------------------------------------------------

def build_12() -> None:
    ladder = condition_cascade(
        [
            ("temperature < 0?", '"мороз"'),
            ("temperature < 15?", '"прохладно"'),
            ("temperature < 25?", '"комфортно"'),
        ],
        default_label='"жарко"',
        input_label="temperature",
        caption="if/elif/else как лестница условий — первое истинное условие выигрывает, остальное пропускается",
    )
    bad_order = decision_diamond_diagram(
        "score >= 50?",
        yes_label="True",
        no_label="False",
        yes_result="branch выбрана — остальные elif ПРОПУЩЕНЫ, даже >= 90",
        no_result="проверяем следующее условие",
        caption="score = 95: если >= 50 стоит первым, программа никогда не дойдёт до >= 90",
    )

    body = f"""
    <h2>Когда исходов больше двух</h2>
    <p>Температура: ниже нуля — «мороз», от 0 до 14 — «прохладно», от 15 до 24 —
    «комфортно», иначе — «жарко». Четыре исхода, а не два — здесь <code class="inline">if/else</code>
    уже не хватает.</p>
    {ladder}
    {code_block(
        "elif_cepochka.py",
        "temperature = 10\n\n"
        "if temperature < 0:\n"
        '    print("мороз")\n'
        "elif temperature < 15:\n"
        '    print("прохладно")\n'
        "elif temperature < 25:\n"
        '    print("комфортно")\n'
        "else:\n"
        '    print("жарко")\n',
    )}
    <p><code class="inline">elif</code> — сокращение от <em>else if</em>, «а иначе, если». Он
    добавляет ещё одно условие между <code class="inline">if</code> и
    <code class="inline">else</code>.</p>

    <h2>Первое истинное условие побеждает</h2>
    <p>Python проверяет условия <strong>по порядку, сверху вниз</strong>, и останавливается на
    первом истинном — даже если следующие условия тоже подошли бы. Оставшаяся часть цепочки
    просто пропускается.</p>

    <h2>Порядок условий имеет значение</h2>
    {code_block(
        "nepravilnyj_poryadok.py",
        "score = 95\n\n"
        "if score >= 50:\n"
        '    bukva = "D"\n'
        "elif score >= 90:\n"
        '    bukva = "A"   # никогда не выполнится для score >= 50!\n',
    )}
    {bad_order}
    {callout(
        "warning",
        "score = 95 попадёт в «D», а не в «A»",
        "Раз <code class=\"inline\">score &gt;= 50</code> стоит первым и <code class=\"inline\">95 &gt;= 50"
        "</code> истинно, Python выбирает именно эту ветку и даже не проверяет"
        " <code class=\"inline\">score &gt;= 90</code>.",
    )}
    <p><strong>Исправление</strong> — расположить условия от более строгого к менее строгому:</p>
    {code_block(
        "pravilnyj_poryadok.py",
        "score = 95\n\n"
        "if score >= 90:\n"
        '    bukva = "A"\n'
        "elif score >= 75:\n"
        '    bukva = "B"\n'
        "elif score >= 50:\n"
        '    bukva = "C"\n'
        "else:\n"
        '    bukva = "D"\n',
    )}

    {exercise(2, "Три ступени скидки", "Постройте elif-лестницу: сумма покупки >= 5000 — скидка 15%, >= 2000 — скидка 10%, >= 500 — скидка 5%, иначе — скидки нет. Проверьте на сумме 3000 — какая скидка выиграет?")}

    {practice_card(
        "09-12",
        "Практика: elif-лестница и порядок условий",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-12/index.html",
    )}
    """
    out = render_page(
        page_title="elif — несколько вариантов",
        description="Оператор elif для нескольких взаимоисключающих вариантов; почему порядок условий критически важен.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("elif", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="elif — несколько вариантов",
        lede="Когда исходов больше двух — elif проверяет условия по очереди, и первое "
        "истинное побеждает.",
        body_html=body,
        sidebar_groups=sidebar("09-12-elif-lestnica.html"),
        nav=PageNav(prev_href="09-03-if-inache.html", prev_label="if / else", next_href="09-13-neskolko-if-protiv-elif.html", next_label="Несколько if ≠ if/elif/else"),
    )
    write("09-12-elif-lestnica.html", out)


# ---------------------------------------------------------------------------
# 9.10 — Несколько if ≠ if/elif/else
# ---------------------------------------------------------------------------

def build_13() -> None:
    cvm = classic_vs_modern(
        "Независимые if против цепочки if/elif",
        "Два НЕЗАВИСИМЫХ if",
        'temperature = 30\n\n'
        'if temperature > 20:\n'
        '    print("тепло")\n\n'
        'if temperature > 25:\n'
        '    print("жарко")\n\n'
        '# ОБА условия истинны —\n'
        '# ОБЕ строки напечатаются!',
        "Цепочка if / elif",
        'temperature = 30\n\n'
        'if temperature > 25:\n'
        '    print("жарко")\n'
        'elif temperature > 20:\n'
        '    print("тепло")\n\n'
        '# только ОДНА ветка\n'
        '# в этой цепочке выполнится',
        "Каждый самостоятельный <code class=\"inline\">if</code> проверяется независимо от "
        "остальных — Python может выполнить несколько таких блоков подряд. А в цепочке "
        "<code class=\"inline\">if/elif/else</code> выполняется РОВНО ОДНА ветка — первая "
        "истинная. Это очень частая путаница у новичков: если нужен «выбор одного варианта из "
        "нескольких» — нужна именно цепочка elif, а не несколько отдельных if.",
    )

    body = f"""
    <h2>Блок команд и невидимый указатель</h2>
    <p>Ветка условия может содержать несколько команд — мы это уже видели. Полезно
    представлять, что Python держит невидимый «указатель»: какую команду выполнить следующей.
    В линейной программе он просто идёт вниз строка за строкой; при <code class="inline">if</code>
    он выбирает, в какую ветку «зайти».</p>

    {callout(
        "info",
        "Это упрощённая мысленная модель",
        "Внутри компьютера существует похожая идея (её называют «поток управления» — "
        "control flow), но для наших целей достаточно этой простой картинки: команды идут по "
        "порядку, а if/elif/else временно направляет поток в одну из веток.",
    )}

    <h2>Поток управления</h2>
    <p><strong>Поток управления</strong> — это порядок, в котором на самом деле выполняются
    команды программы. До этой главы он был почти всегда прямой линией сверху вниз. Теперь он
    может <strong>разветвляться</strong>. В главе 10 он научится ещё и возвращаться назад —
    повторяться.</p>

    <h2>Несколько if — это НЕ то же самое, что if/elif/else</h2>
    <p>Это одна из самых частых путаниц у новичков — разберём её на конкретном примере:</p>
    {cvm}

    {exercise(2, "Найдите разницу", "Возьмите score = 85. Постройте вариант с тремя независимыми if (score > 50, score > 70, score > 90) и вариант с elif-цепочкой на тех же условиях. Сравните, сколько строк напечатает каждый вариант.")}

    {practice_card(
        "09-13",
        "Практика: независимые if против elif",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-13/index.html",
    )}
    """
    out = render_page(
        page_title="Несколько if ≠ if/elif/else",
        description="Разница между несколькими независимыми if и цепочкой if/elif/else; поток управления.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("if против elif", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Несколько if ≠ if/elif/else",
        lede="Очень частая путаница у новичков: несколько отдельных if могут сработать все "
        "разом, а в цепочке elif — только один.",
        body_html=body,
        sidebar_groups=sidebar("09-13-neskolko-if-protiv-elif.html"),
        nav=PageNav(prev_href="09-12-elif-lestnica.html", prev_label="elif", next_href="09-14-and.html", next_label="and — все условия сразу"),
    )
    write("09-13-neskolko-if-protiv-elif.html", out)


# ---------------------------------------------------------------------------
# 9.11 — and
# ---------------------------------------------------------------------------

def build_14() -> None:
    gate = decision_map([
        ("age >= 18?", "нужно ДА"),
        ("has_ticket?", "нужно ДА тоже"),
    ], title="Вход в зал разрешён только если ОБА условия истинны")
    truth_and = comparison_table(
        ["A", "B", "A and B"],
        [["False", "False", "False"], ["False", "True", "False"], ["True", "False", "False"], ["True", "True", "True"]],
    )

    body = f"""
    <h2>Все условия должны быть True</h2>
    <p>Реальная ситуация: вас пускают в зал, только если вам есть 18 лет И у вас есть билет.
    Оба условия обязательны:</p>
    {gate}
    {code_block(
        "and_primer.py",
        "age = 20\n"
        "has_ticket = True\n\n"
        "if age >= 18 and has_ticket:\n"
        '    print("Проходите в зал.")\n',
    )}

    <h2>Таблица истинности and</h2>
    {truth_and}
    <p>Результат <code class="inline">and</code> истинен, только когда истинны <strong>оба</strong>
    операнда — во всех остальных трёх случаях результат ложен.</p>

    <h2>Переведите на человеческий язык</h2>
    <p>Полезный навык — читать условие вслух как предложение:</p>
    {code_block("chitaem_vsluh.py", 'age >= 18 and country == "PL"\n# "age не меньше 18 И country равно PL"\n')}

    {exercise(1, "Своё условие с and", "Напишите условие: can_drive — можно водить машину, если age >= 18 И has_license равно True. Проверьте на age=20, has_license=False.")}

    {practice_card(
        "09-14",
        "Практика: and и таблица истинности",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-14/index.html",
    )}
    """
    out = render_page(
        page_title="and — все условия сразу",
        description="Логический оператор and: оба условия должны быть истинны. Таблица истинности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("and", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="and — все условия сразу",
        lede="Иногда решение зависит не от одного, а сразу от всех перечисленных условий.",
        body_html=body,
        sidebar_groups=sidebar("09-14-and.html"),
        nav=PageNav(prev_href="09-13-neskolko-if-protiv-elif.html", prev_label="if против elif", next_href="09-15-or.html", next_label="or — хотя бы одно"),
    )
    write("09-14-and.html", out)


# ---------------------------------------------------------------------------
# 9.12 — or
# ---------------------------------------------------------------------------

def build_15() -> None:
    gate = decision_map([
        ("student?", "достаточно ДА"),
        ("senior?", "или ДА здесь"),
    ], title="Скидка положена, если истинно ХОТЯ БЫ ОДНО условие")
    truth_or = comparison_table(
        ["A", "B", "A or B"],
        [["False", "False", "False"], ["False", "True", "True"], ["True", "False", "True"], ["True", "True", "True"]],
    )

    body = f"""
    <h2>Достаточно одного True</h2>
    <p>Скидка положена студентам ИЛИ пенсионерам — достаточно подходить хотя бы под одну
    категорию:</p>
    {gate}
    {code_block(
        "or_primer.py",
        "is_student = False\n"
        "is_senior = True\n\n"
        "if is_student or is_senior:\n"
        '    print("Скидка применена.")\n',
    )}

    <h2>Таблица истинности or</h2>
    {truth_or}
    <p>Результат <code class="inline">or</code> ложен только тогда, когда ложны <strong>оба</strong>
    операнда — во всех остальных случаях он истинен.</p>

    {exercise(1, "Выходной или праздник", "Напишите условие: can_rest — можно не работать, если is_weekend равно True ИЛИ is_holiday равно True. Проверьте на is_weekend=False, is_holiday=True.")}

    {practice_card(
        "09-15",
        "Практика: or и таблица истинности",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-15/index.html",
    )}
    """
    out = render_page(
        page_title="or — хотя бы одно",
        description="Логический оператор or: достаточно, чтобы хотя бы одно условие было истинно. Таблица истинности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("or", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="or — хотя бы одно",
        lede="Иногда для срабатывания достаточно, чтобы истинным было хотя бы одно из "
        "перечисленных условий.",
        body_html=body,
        sidebar_groups=sidebar("09-15-or.html"),
        nav=PageNav(prev_href="09-14-and.html", prev_label="and", next_href="09-16-not.html", next_label="not — переворачиваем условие"),
    )
    write("09-15-or.html", out)


# ---------------------------------------------------------------------------
# 9.13 — not
# ---------------------------------------------------------------------------

def build_16() -> None:
    truth_not = comparison_table(["A", "not A"], [["True", "False"], ["False", "True"]])

    body = f"""
    <h2>Переворачиваем логическое значение</h2>
    <p><code class="inline">not</code> — самый простой логический оператор: он просто
    переворачивает <code class="inline">True</code> в <code class="inline">False</code> и
    наоборот.</p>
    {truth_not}
    {code_block(
        "not_primer.py",
        "is_raining = False\n\n"
        "if not is_raining:\n"
        '    print("Можно гулять")\n',
    )}
    <p>Читаем вслух: «если НЕ идёт дождь». Условие <code class="inline">not is_raining</code>
    истинно ровно тогда, когда <code class="inline">is_raining</code> ложно.</p>

    {code_block("not_s_sravneniem.py", 'age = 15\nprint(not (age >= 18))   # True — потому что age >= 18 само по себе False\n')}

    {exercise(1, "Двойное not", "Предскажите результат not not True — затем проверьте в коде. Объясните своими словами, почему получился именно такой ответ.")}

    {practice_card(
        "09-16",
        "Практика: not и инверсия условий",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-16/index.html",
    )}
    """
    out = render_page(
        page_title="not — переворачиваем условие",
        description="Логический оператор not для инверсии условия.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("not", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="not — переворачиваем условие",
        lede="Простейший логический оператор: превращает True в False и обратно.",
        body_html=body,
        sidebar_groups=sidebar("09-16-not.html"),
        nav=PageNav(prev_href="09-15-or.html", prev_label="or", next_href="09-04-neskolko-uslovij.html", next_label="Больше одного условия!"),
    )
    write("09-16-not.html", out)


# ---------------------------------------------------------------------------
# 9.14 — Больше одного условия (существующий, расширяем — синтез and/or/not)
# ---------------------------------------------------------------------------

def build_04() -> None:
    prec = precedence_ladder(
        [
            ("not", "выполняется первым"),
            ("and", "выполняется вторым"),
            ("or", "выполняется последним"),
        ],
        caption="Приоритет логических операторов — как +/- и */÷ в арифметике",
    )
    human_table = comparison_table(
        ["Человеческая фраза", "Python-условие"],
        [
            ["«возраст не меньше 18»", "<code class=\"inline\">age &gt;= 18</code>"],
            ["«температура ниже нуля»", "<code class=\"inline\">temperature &lt; 0</code>"],
            ["«имя не пустое»", "<code class=\"inline\">name</code> (достаточно самого имени — truthiness)"],
            ["«ответ — да или yes»", "<code class=\"inline\">answer in (\"да\", \"yes\")</code>"],
            ["«совершеннолетний и с билетом»", "<code class=\"inline\">age &gt;= 18 and has_ticket</code>"],
        ],
    )

    body = f"""
    <p>Мы разобрали <code class="inline">and</code>, <code class="inline">or</code> и
    <code class="inline">not</code> по отдельности — теперь соберём их вместе и разберём, как
    Python понимает более сложные условия.</p>

    {code_block(
        "logicheskie_operatory.py",
        "age = 20\n"
        "has_ticket = True\n\n"
        "if age >= 18 and has_ticket:\n"
        '    print("Проходите в зал.")\n\n'
        "is_weekend = False\n"
        "is_holiday = True\n"
        "if is_weekend or is_holiday:\n"
        '    print("Сегодня можно не ходить на работу.")\n\n'
        "if not has_ticket:\n"
        '    print("Сначала нужно купить билет.")\n',
    )}

    <h2>Приоритет операторов</h2>
    <p>Когда в одном условии встречаются <code class="inline">and</code> и
    <code class="inline">or</code> вместе, Python сначала вычисляет
    <code class="inline">not</code>, затем <code class="inline">and</code>, и только потом
    <code class="inline">or</code> — совсем как умножение выполняется раньше сложения в
    арифметике:</p>
    {prec}
    {code_block("prioritet.py", "print(True or False and False)\n# and выполнится первым: False and False -> False\n# затем or: True or False -> True\n")}

    {callout(
        "tip",
        "Скобки помогают читать сложные условия",
        "Не заставляйте читателя (и себя в будущем) запоминать таблицу приоритетов. Когда "
        "условий много, скобки делают порядок явным: <code class=\"inline\">is_admin or "
        "(is_owner and is_active)</code> читается однозначно, в отличие от варианта без "
        "скобок.",
    )}

    <h2>Переводим человеческий язык в условие — и обратно</h2>
    {human_table}
    <p>Это фундаментальный навык: научиться формулировать вопрос на человеческом языке, а
    затем перевести его в Python-условие — и наоборот, читать готовое условие как предложение.</p>

    {practice_card(
        "09-04",
        "Практика: and, or, not вместе и приоритет",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-04/index.html",
    )}
    """
    out = render_page(
        page_title="Больше одного условия!",
        description="Комбинируем and, or, not; приоритет логических операторов и перевод человеческого языка в условие.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Больше одного условия", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Больше одного условия! :O",
        lede="and, or и not вместе — приоритет операторов и перевод человеческой фразы в "
        "Python-условие.",
        body_html=body,
        sidebar_groups=sidebar("09-04-neskolko-uslovij.html"),
        nav=PageNav(prev_href="09-16-not.html", prev_label="not", next_href="09-17-short-circuit.html", next_label="Short-circuit: Python иногда ленится"),
    )
    write("09-04-neskolko-uslovij.html", out)


# ---------------------------------------------------------------------------
# 9.15 — Short-circuit
# ---------------------------------------------------------------------------

def build_17() -> None:
    and_flow = condition_cascade(
        [("A?", "False"), ("B?", "False")],
        default_label="True",
        exit_label="НЕТ",
        continue_label="ДА",
        caption="and: НЕТ на любом шаге сразу даёт False — второе условие проверяется, только если первое истинно",
    )
    or_flow = condition_cascade(
        [("A?", "True"), ("B?", "True")],
        default_label="False",
        exit_label="ДА",
        continue_label="НЕТ",
        caption="or: ДА на любом шаге сразу даёт True — второе условие проверяется, только если первое ложно",
    )

    body = f"""
    <h2>Python иногда не проверяет всё условие</h2>
    <p>У <code class="inline">and</code> и <code class="inline">or</code> есть важное
    свойство — <strong>short-circuit</strong> («короткое замыкание»): Python вычисляет второй
    операнд, только если это действительно нужно для ответа.</p>

    <h2>and: если A уже False</h2>
    {and_flow}
    <p>Если <code class="inline">A</code> ложно, весь <code class="inline">A and B</code> уже
    обязан быть ложным — независимо от <code class="inline">B</code>. Python это понимает и не
    тратит время на вычисление <code class="inline">B</code>.</p>

    <h2>or: если A уже True</h2>
    {or_flow}
    <p>Аналогично: если <code class="inline">A</code> истинно, весь
    <code class="inline">A or B</code> уже обязан быть истинным.</p>

    <h2>Реальная польза: защита от ошибки</h2>
    <p>Это не просто оптимизация скорости — иногда именно она спасает программу от падения:</p>
    {code_block("short_circuit_zashchita.py", 'name = ""\n\nif name and name[0] == "A":\n    print("Имя начинается на A")\nelse:\n    print("Условие не выполнено")\n')}
    <p>Если <code class="inline">name</code> — пустая строка, она сама по себе falsy (глава 8),
    поэтому <code class="inline">name and ...</code> уже ложно, и Python <strong>даже не
    пытается</strong> вычислить <code class="inline">name[0]</code>. Если бы порядок был
    обратным...</p>
    {code_block("bez_zashchity.py", 'name = ""\nprint(name[0] == "A" and name)\n# IndexError: string index out of range!\n')}
    {callout(
        "warning",
        "Порядок операндов имеет значение",
        "<code class=\"inline\">name and name[0] == \"A\"</code> — безопасно: сначала "
        "проверяется, что name вообще непустая. <code class=\"inline\">name[0] == \"A\" and "
        "name</code> — опасно: Python попытается вычислить <code class=\"inline\">name[0]</code> "
        "ещё до всякой проверки на пустоту, и получит <code class=\"inline\">IndexError</code> "
        "для пустой строки (глава 8, раздел про индексы).",
    )}

    {exercise(2, "Безопасная проверка последнего символа", "Напишите условие, которое безопасно проверяет, заканчивается ли непустая строка text на символ '!' — так, чтобы для пустой строки не возникало IndexError.")}

    {practice_card(
        "09-17",
        "Практика: short-circuit и защита от ошибок",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-17/index.html",
    )}
    """
    out = render_page(
        page_title="Short-circuit: Python иногда ленится",
        description="Short-circuit evaluation для and/or: Python не всегда вычисляет второй операнд — и как это защищает от ошибок вроде IndexError.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Short-circuit", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Short-circuit: Python иногда ленится",
        lede="and и or не всегда вычисляют оба операнда — и это свойство можно использовать, "
        "чтобы защититься от ошибок.",
        body_html=body,
        sidebar_groups=sidebar("09-17-short-circuit.html"),
        nav=PageNav(prev_href="09-04-neskolko-uslovij.html", prev_label="Больше одного условия", next_href="09-18-in-not-in.html", next_label="in / not in как условие"),
    )
    write("09-17-short-circuit.html", out)


# ---------------------------------------------------------------------------
# 9.16 — in / not in
# ---------------------------------------------------------------------------

def build_18() -> None:
    membership = decision_diamond_diagram(
        '"py" in "python"?',
        yes_result="True",
        no_result="False",
        caption="in — вопрос «найдено ли значение внутри»",
    )

    body = f"""
    <h2>Проверка вхождения как условие</h2>
    <p>Мы познакомились с <code class="inline">in</code>/<code class="inline">not in</code> в
    главе 8 — теперь используем их прямо в условиях <code class="inline">if</code>.</p>
    {code_block("in_kak_uslovie.py", 'text = "python"\nprint("py" in text)        # True\nprint("java" not in text)  # True\n')}
    {membership}

    <h2>Группа допустимых ответов</h2>
    <p>Частая задача: проверить, что ответ пользователя входит в набор принятых вариантов.
    Пока мы не изучали списки подробно (это будет в главе 10-11), но уже можем использовать
    простую группу значений в скобках — <strong>кортеж</strong>:</p>
    {code_block(
        "gruppa_otvetov.py",
        'answer = input("Продолжить? ").strip().lower()\n\n'
        'if answer in ("да", "yes", "y"):\n'
        '    print("Продолжаем")\n'
        'elif answer in ("нет", "no", "n"):\n'
        '    print("Останавливаемся")\n'
        'else:\n'
        '    print("Не понял ответ")\n',
    )}
    {callout(
        "info",
        "Что такое (\"да\", \"yes\", \"y\")",
        "Это <strong>кортеж</strong> — группа значений в круглых скобках. "
        "<code class=\"inline\">answer in (...)</code> проверяет: «совпадает ли answer хотя бы "
        "с одним из перечисленных значений?» Списки и кортежи подробно разберём в следующих "
        "главах — сейчас достаточно уметь применять этот полезный приём.",
    )}

    {callout(
        "warning",
        "Осторожно с in для строки-подстроки",
        "<code class=\"inline\">\"да\" in \"давай\"</code> тоже даёт <code class=\"inline\">True"
        "</code> — потому что <code class=\"inline\">in</code> для строки ищет ПОДСТРОКУ, а не "
        "точное совпадение целого слова. Для сравнения с набором вариантов используйте "
        "кортеж/список значений, как в примере выше, а не проверку «одна строка внутри "
        "другой».",
    )}

    {practice_card(
        "09-18",
        "Практика: in / not in в условиях",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-18/index.html",
    )}
    """
    out = render_page(
        page_title="in / not in как условие",
        description="Оператор in/not in в условиях if, проверка вхождения ответа в группу допустимых значений.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("in / not in", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="in / not in как условие",
        lede="Проверка вхождения из главы 8 — теперь прямо внутри условий if.",
        body_html=body,
        sidebar_groups=sidebar("09-18-in-not-in.html"),
        nav=PageNav(prev_href="09-17-short-circuit.html", prev_label="Short-circuit", next_href="09-19-is-vs-ravno.html", next_label="is против =="),
    )
    write("09-18-in-not-in.html", out)


# ---------------------------------------------------------------------------
# 9.17 — is vs ==
# ---------------------------------------------------------------------------

def build_19() -> None:
    body = f"""
    <h2>Два разных вопроса</h2>
    <p><code class="inline">==</code> и <code class="inline">is</code> выглядят похоже, но
    спрашивают о совершенно разном:</p>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin:24px 0">
      <div style="flex:1;min-width:220px;padding:20px;border-radius:16px;background:var(--color-bg-surface,#FAFAFC);border:1.5px solid var(--color-border-default,#E4E1F5)">
        <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:18px;color:#5B24F9">==</div>
        <div style="font-size:14px;margin-top:8px;color:#0D0230">«Равны ли ЗНАЧЕНИЯ?»</div>
      </div>
      <div style="flex:1;min-width:220px;padding:20px;border-radius:16px;background:var(--color-bg-surface,#FAFAFC);border:1.5px solid var(--color-border-default,#E4E1F5)">
        <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:18px;color:#DB2777">is</div>
        <div style="font-size:14px;margin-top:8px;color:#0D0230">«Это ОДИН И ТОТ ЖЕ объект?»</div>
      </div>
    </div>

    <h2>Главное практическое применение — None</h2>
    <p>В подавляющем большинстве случаев для чисел, строк и вообще обычных сравнений нужен
    именно <code class="inline">==</code>. Правильное и по-настоящему важное применение
    <code class="inline">is</code> на этом этапе — проверка на <code class="inline">None</code>:</p>
    {code_block("is_none.py", 'value = None\n\nprint(value is None)       # True — правильный способ\nprint(value is not None)   # False\n')}

    {callout(
        "tip",
        "Почему не value == None",
        "Технически <code class=\"inline\">value == None</code> в большинстве случаев тоже "
        "сработает — но <code class=\"inline\">is None</code> считается более правильным "
        "стилем в Python: он однозначно спрашивает «это именно None?», а не «равно ли значение "
        "чему-то, что ведёт себя как None?». Договоримся всегда использовать "
        "<code class=\"inline\">is None</code> / <code class=\"inline\">is not None</code>.",
    )}

    {callout(
        "warning",
        "Не используйте is для чисел и строк",
        "<code class=\"inline\">256 is 256</code> или <code class=\"inline\">\"a\" is \"a\"</code> "
        "могут вести себя неожиданно — их результат зависит от внутренних деталей реализации "
        "Python, которые не гарантированы и могут отличаться в разных ситуациях. Это не то, "
        "чему стоит учиться сейчас: для сравнения значений всегда используйте "
        "<code class=\"inline\">==</code>. Идея «сравнение по объекту» подробно вернётся в "
        "главе про ООП.",
    )}

    {practice_card(
        "09-19",
        "Практика: is против ==",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-19/index.html",
    )}
    """
    out = render_page(
        page_title="is против ==",
        description="Разница между == (равенство значений) и is (тождественность объекта); правильная проверка на None.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("is против ==", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="is против ==",
        lede="Два похожих оператора спрашивают о совершенно разных вещах — и есть ровно один "
        "правильный повод использовать is прямо сейчас.",
        body_html=body,
        sidebar_groups=sidebar("09-19-is-vs-ravno.html"),
        nav=PageNav(prev_href="09-18-in-not-in.html", prev_label="in / not in", next_href="09-20-vlozhennye-uslovija.html", next_label="Вложенные условия"),
    )
    write("09-19-is-vs-ravno.html", out)


# ---------------------------------------------------------------------------
# 9.18 — Вложенные условия
# ---------------------------------------------------------------------------

def build_20() -> None:
    nested_flow = flowchart(
        [
            {"kind": "start", "label": "СТАРТ"},
            {
                "kind": "decision", "label": "has_account?",
                "yes": [{
                    "kind": "decision", "label": "password_ok?",
                    "yes": [{"kind": "output", "label": '"Добро пожаловать"'}],
                    "no": [{"kind": "output", "label": '"Неверный пароль"'}],
                }],
                "no": [{"kind": "output", "label": '"Зарегистрируйтесь"'}],
            },
            {"kind": "end", "label": "КОНЕЦ"},
        ],
        caption="Вложенное условие: password_ok проверяется только внутри ветки has_account = True",
    )
    flatten = classic_vs_modern(
        "Вложенные условия vs один and",
        "Вложенные if",
        'if has_account:\n'
        '    if password_ok:\n'
        '        print("Login")',
        "Один if с and",
        'if has_account and password_ok:\n'
        '    print("Login")',
        "Оба варианта корректны и в этом простом случае дают одинаковый результат. Вложенный "
        "вариант удобен, когда каждой ветке нужна СВОЯ отдельная обработка (например, разные "
        "сообщения для «нет аккаунта» и «неверный пароль», как в примере ниже). Один "
        "<code class=\"inline\">and</code> компактнее, когда обе ветки нужны только вместе — "
        "выбор между ними определяется читаемостью, а не «правильностью» одного варианта.",
    )

    body = f"""
    <h2>Условие внутри условия</h2>
    <p>Внутри блока <code class="inline">if</code> может быть ещё один
    <code class="inline">if</code> — это называется <strong>вложенным условием</strong>. Решим
    задачу входа в аккаунт целиком, одной схемой.</p>
    {nested_flow}
    {code_block(
        "vlozhennye_usloviya.py",
        "has_account = True\n"
        "password_ok = False\n\n"
        "if has_account:\n"
        "    if password_ok:\n"
        '        print("Добро пожаловать")\n'
        "    else:\n"
        '        print("Неверный пароль")\n'
        "else:\n"
        '    print("Зарегистрируйтесь")\n',
    )}

    <h2>Уровни отступа = уровни вложенности</h2>
    <p>Каждый дополнительный уровень отступа означает более глубокий уровень условной
    проверки:</p>
    {code_block(
        "urovni_otstupa.py",
        "# уровень 0\n"
        "if has_account:\n"
        "    # уровень 1\n"
        "    if password_ok:\n"
        "        # уровень 2\n"
        '        print("...")\n',
    )}
    {callout(
        "warning",
        "Не увлекайтесь глубокой вложенностью",
        "Три-четыре уровня вложенных if подряд («пирамида») читать становится тяжело. Часто "
        "часть условий можно объединить оператором <code class=\"inline\">and</code> — как "
        "показано ниже.",
    )}

    <h2>Упрощаем: вложенность → and</h2>
    {flatten}

    {exercise(2, "Третий уровень", "Добавьте третий уровень вложенности: внутри «Добро пожаловать» проверьте ещё и is_active (аккаунт не заблокирован) — если False, выведите «Аккаунт заблокирован».")}

    {practice_card(
        "09-20",
        "Практика: вложенные условия",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-20/index.html",
    )}
    """
    out = render_page(
        page_title="Вложенные условия",
        description="if внутри if — вложенные условия, уровни отступа и упрощение вложенности через and.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Вложенные условия", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Вложенные условия",
        lede="Условие внутри условия — и когда его стоит упростить одним and вместо глубокой "
        "вложенности.",
        body_html=body,
        sidebar_groups=sidebar("09-20-vlozhennye-uslovija.html"),
        nav=PageNav(prev_href="09-19-is-vs-ravno.html", prev_label="is против ==", next_href="09-21-proektirovanie-uslovij.html", next_label="Проектируем условие"),
    )
    write("09-20-vlozhennye-uslovija.html", out)


# ---------------------------------------------------------------------------
# 9.19 — Проектируем условие: ввод, валидация, границы
# ---------------------------------------------------------------------------

def build_21() -> None:
    workflow = flow_diagram(
        [
            ("ТРЕБОВАНИЕ", "что нужно проверить"),
            ("ВОПРОС", "сформулировать явно"),
            ("УСЛОВИЕ", "перевести в Python"),
            ("ВЕТКИ", "что делать при True/False"),
            ("ГРАНИЦЫ", "протестировать край"),
        ],
        caption="Повторяемый workflow проектирования условия — от требования до протестированного кода",
    )
    boundary_table = comparison_table(
        ["Значение", "1 &lt;= number &lt;= 10", "Комментарий"],
        [["0", "False", "ниже границы"], ["1", "True", "ровно на границе — входит"], ["10", "True", "ровно на границе — входит"], ["11", "False", "выше границы"]],
    )

    body = f"""
    <h2>Валидация — это не то же самое, что решение</h2>
    <p>Прежде чем принимать решение по введённым данным, нужно проверить, что данные вообще
    осмысленны. Это два разных шага:</p>
    <ul>
      <li><strong>Валидация</strong> — допустим ли ввод? (например, это вообще число?)</li>
      <li><strong>Решение</strong> — что делать с допустимым вводом?</li>
    </ul>
    {code_block(
        "validaciya_i_reshenie.py",
        'age_text = input("Возраст: ").strip()\n\n'
        "if age_text.isdigit():          # 1. валидация\n"
        "    age = int(age_text)\n"
        "    if age >= 18:                # 2. решение\n"
        '        print("Доступ разрешён")\n'
        "    else:\n"
        '        print("Доступ запрещён")\n'
        "else:\n"
        '    print("Это не похоже на число")\n',
    )}
    {callout(
        "info",
        "Полноценная обработка ошибок — впереди",
        "Здесь мы проверяем ввод вручную через <code class=\"inline\">isdigit()</code> "
        "(глава 8). Настоящий механизм обработки исключений — <code class=\"inline\">try/except"
        "</code> — придёт в отдельной главе позже; пока достаточно этого простого подхода.",
    )}

    <h2>Границы — источник большинства ошибок</h2>
    <p>«Разрешены значения от 1 до 10 включительно» — как записать это правильно?</p>
    {code_block("granicy.py", "number = 1\nprint(1 <= number <= 10)   # True — правильно, включает края\nprint(1 < number < 10)     # False — ЛОВУШКА: отвергает 1 и 10!\n")}
    {boundary_table}
    {callout(
        "warning",
        "Off-by-one — классическая ошибка",
        "Если формулировка говорит «включительно», а в коде стоит строгое "
        "<code class=\"inline\">&lt;</code>/<code class=\"inline\">&gt;</code> вместо "
        "<code class=\"inline\">&lt;=</code>/<code class=\"inline\">&gt;=</code>, граничные "
        "значения незаметно отбрасываются. Такую ошибку называют <strong>off-by-one</strong> "
        "(«ошибка на единицу») — она встречается настолько часто, что заслуживает отдельного "
        "имени.",
    )}

    <h2>Повторяемый способ проектировать условие</h2>
    {workflow}
    <p>Перед тем как писать код:</p>
    <ol style="font-size:15px;line-height:1.9">
      <li>Какой вопрос мы задаём?</li>
      <li>Какие значения в нём участвуют?</li>
      <li>Что означает результат True?</li>
      <li>Что делать, если True? А если False?</li>
      <li>Есть ли больше двух исходов?</li>
      <li>Какие здесь граничные значения?</li>
    </ol>
    <p>Всегда тестируйте <strong>значение чуть ниже границы, ровно на границе, и чуть выше</strong>
    — это простое правило ловит огромную долю логических ошибок ещё до того, как они попадут
    к пользователю.</p>

    {exercise(2, "Спроектируйте сами", "Требование: «Скидка положена при сумме покупки от 1000 рублей». Пройдите весь workflow — от вопроса до протестированного кода — и проверьте граничные значения 999, 1000, 1001.")}

    {practice_card(
        "09-21",
        "Практика: валидация, границы и off-by-one",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-21/index.html",
    )}
    """
    out = render_page(
        page_title="Проектируем условие: ввод, валидация, границы",
        description="Разница между валидацией и решением, работа с числовым вводом, граничные значения и off-by-one ошибки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Проектируем условие", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Проектируем условие: ввод, валидация, границы",
        lede="Повторяемый способ подходить к любому условию — от требования до "
        "протестированного граничного значения.",
        body_html=body,
        sidebar_groups=sidebar("09-21-proektirovanie-uslovij.html"),
        nav=PageNav(prev_href="09-20-vlozhennye-uslovija.html", prev_label="Вложенные условия", next_href="09-22-otladka-logiki.html", next_label="Отладка логических ошибок"),
    )
    write("09-21-proektirovanie-uslovij.html", out)


# ---------------------------------------------------------------------------
# 9.20 — Отладка логических ошибок
# ---------------------------------------------------------------------------

def build_22() -> None:
    error_types = comparison_table(
        ["Тип ошибки", "Что происходит", "Пример"],
        [
            ["SyntaxError", "Python не может даже начать выполнение кода", "<code class=\"inline\">if age &gt;= 18</code> (забыто двоеточие)"],
            ["Runtime-ошибка", "программа стартует, но падает на середине", "<code class=\"inline\">age_text + 5</code> (str + int)"],
            ["Логическая ошибка", "программа выполняется успешно, но результат неверный", "<code class=\"inline\">if age &gt; 18</code> вместо <code class=\"inline\">&gt;=</code>"],
        ],
    )
    debug_flow = flow_diagram(
        [
            ("1. print значения", "age, has_ticket"),
            ("2. print условие", "age >= 18 and has_ticket"),
            ("3. границы", "17, 18, 19"),
            ("4. упростить", "разбить на части"),
            ("5. по отдельности", "каждое под-условие"),
        ],
        caption="Метод отладки условий — от вывода значений до проверки каждой части отдельно",
    )
    naming_table = comparison_table(
        ["Хорошее имя", "Плохое имя"],
        [
            ["<code class=\"inline\">is_ready</code>", "<code class=\"inline\">flag1</code>"],
            ["<code class=\"inline\">has_ticket</code>", "<code class=\"inline\">thing</code>"],
            ["<code class=\"inline\">can_enter</code>", "<code class=\"inline\">value2</code>"],
            ["<code class=\"inline\">needs_update</code>", "<code class=\"inline\">x</code>"],
        ],
    )

    body = f"""
    <h2>Логическая ошибка — это не ошибка Python</h2>
    <p>Программа <code class="inline">if age &gt; 18:</code> выполняется прекрасно и не выдаёт
    никакой ошибки. Но если по условию задачи «доступ с 18 лет включительно», это —
    <strong>логическая ошибка</strong>: Python не может знать, что вы имели в виду.</p>
    {error_types}

    <h2>Метод отладки условий</h2>
    <p>Когда результат условия кажется неправильным, не гадайте — выведите промежуточные
    значения:</p>
    {debug_flow}
    {code_block(
        "otladka_uslovij.py",
        "age = 20\n"
        "has_ticket = False\n"
        "eligible = age >= 18 and has_ticket\n\n"
        'print("age >= 18:", age >= 18)\n'
        'print("has_ticket:", has_ticket)\n'
        'print("eligible:", eligible)\n'
        "# age >= 18: True\n"
        "# has_ticket: False\n"
        "# eligible: False\n",
    )}
    <p>Разбив сложное условие на части и выведя каждую отдельно, сразу видно, ЧТО именно
    сделало итог ложным.</p>

    <h2>Называйте логические переменные осмысленно</h2>
    {naming_table}
    <p>Приставки <code class="inline">is_</code>, <code class="inline">has_</code>,
    <code class="inline">can_</code>, <code class="inline">needs_</code> — не обязательный
    синтаксис, а полезное соглашение: сразу видно, что переменная хранит
    <code class="inline">True</code>/<code class="inline">False</code>.</p>

    <h2>Сохраняйте сложное условие в переменную</h2>
    {code_block("imenovannoe_uslovie.py", "can_enter = age >= 18 and has_ticket\n\nif can_enter:\n    print(\"Проходите\")\n")}
    <p><code class="inline">can_enter</code> читается сразу — не нужно заново разбирать
    выражение <code class="inline">age &gt;= 18 and has_ticket</code> каждый раз, когда вы
    возвращаетесь к этому коду.</p>

    {callout(
        "tip",
        "[[icon:launch]] ЧУТЬ ГЛУБЖЕ — условное выражение",
        "После того как if/else хорошо усвоен, полезно знать компактную форму для ПРОСТОГО "
        "выбора значения: <code class=\"inline\">status = \"adult\" if age &gt;= 18 else \"minor\""
        "</code>. Это не замена обычному if/else — только удобство для одной строки.",
    )}

    {callout(
        "info",
        "match/case — на будущее",
        "В Python есть и структурное сопоставление <code class=\"inline\">match/case</code> для "
        "некоторых многовариантных ситуаций. Мы изучим его подробно позже — сейчас достаточно "
        "знать, что оно существует.",
    )}

    {practice_card(
        "09-22",
        "Практика: отладка логических ошибок",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-22/index.html",
    )}
    """
    out = render_page(
        page_title="Отладка логических ошибок",
        description="Синтаксическая ошибка, ошибка выполнения и логическая ошибка — метод отладки условий, именование bool-переменных.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Отладка логики", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Отладка логических ошибок",
        lede="Программа может выполняться без единой ошибки — и всё равно давать неверный "
        "результат. Учимся находить такие ошибки методично.",
        body_html=body,
        sidebar_groups=sidebar("09-22-otladka-logiki.html"),
        nav=PageNav(prev_href="09-21-proektirovanie-uslovij.html", prev_label="Проектируем условие", next_href="09-05-mini-proekt-ugadaj-chislo.html", next_label="Мини-проект: «Угадай число»"),
    )
    write("09-22-otladka-logiki.html", out)


# ---------------------------------------------------------------------------
# 9.21 — Мини-проект: «Угадай число» (существующий, СИЛЬНО расширяем)
# ---------------------------------------------------------------------------

def build_05() -> None:
    game_tree = condition_cascade(
        [
            ("guess == secret?", "🎉 Вы угадали!"),
            ("guess < secret?", '"Слишком мало"'),
        ],
        default_label='"Слишком много"',
        input_label="guess",
        start_label="СТАРТ",
        caption="Решающее дерево игры — переводим прямо в if / elif / else",
    )

    body = f"""
    <p>Первая настоящая игра в этой книге! Компьютер загадывает число, вы вводите один
    вариант — программа говорит, угадали вы или нет.</p>

    <h2>Сначала — как это выглядит для игрока</h2>
    {code_block(
        "terminal_dialog.txt",
        "Я загадал число от 1 до 10.\n\n"
        "Ваш вариант: 7\n"
        "Слишком большое!\n"
        "Я загадал: 4\n",
        lang="text",
    )}
    <p>Или, если угадали с первой попытки:</p>
    {code_block(
        "terminal_dialog_win.txt",
        "Я загадал число от 1 до 10.\n\n"
        "Ваш вариант: 4\n\n"
        "🎉 Вы угадали!\n",
        lang="text",
    )}

    {callout(
        "info",
        "Одна попытка — и это нормально",
        "Пока мы не проходили циклы (глава 10), поэтому у игрока ровно одна попытка. Полная, "
        "переигрываемая версия с повтором до угадывания появится там же — уже сейчас держите "
        "это в голове как мотивацию для следующей главы.",
    )}

    <h2>Решающее дерево игры</h2>
    {game_tree}
    {code_block(
        "reshenie_v_kod.py",
        "if guess == secret:\n"
        '    print("🎉 Вы угадали!")\n'
        "elif guess < secret:\n"
        '    print("Слишком мало!")\n'
        "else:\n"
        '    print("Слишком много!")\n',
    )}

    <h2>Строим игру по шагам</h2>

    <h3>Шаг 1 — загадываем число</h3>
    {code_block("shag_1.py", "import random\n\nsecret = random.randint(1, 10)\n")}

    <h3>Шаг 2 — читаем ответ игрока</h3>
    {code_block("shag_2.py", 'guess_text = input("Ваш вариант: ")\n')}

    <h3>Шаг 3 — преобразуем в число</h3>
    {code_block("shag_3.py", "guess = int(guess_text)\n")}
    {callout(
        "warning",
        "Забытый int() — источник ошибки",
        "Если сравнить <code class=\"inline\">guess_text &lt; secret</code> напрямую (строку с "
        "числом), Python выдаст <code class=\"inline\">TypeError</code> — сравнивать строку и "
        "число нельзя. Преобразование <code class=\"inline\">int()</code> обязательно.",
    )}

    <h3>Шаг 4 — проверяем точное совпадение</h3>
    {code_block("shag_4.py", 'if guess == secret:\n    print("🎉 Вы угадали!")\n')}

    <h3>Шаг 5 — добавляем «слишком мало»</h3>
    {code_block("shag_5.py", 'if guess == secret:\n    print("🎉 Вы угадали!")\nelif guess < secret:\n    print("Слишком мало!")\n')}

    <h3>Шаг 6 — else означает «слишком много»</h3>
    {code_block("shag_6.py", 'if guess == secret:\n    print("🎉 Вы угадали!")\nelif guess < secret:\n    print("Слишком мало!")\nelse:\n    print("Слишком много!")\n')}

    <h3>Шаг 7 — финальная версия</h3>
    {code_block(
        "ugadaj_chislo.py",
        "import random\n\n"
        "secret = random.randint(1, 10)\n"
        'guess = int(input("Ваш вариант: "))\n\n'
        "if guess == secret:\n"
        '    print("🎉 Вы угадали!")\n'
        "elif guess < secret:\n"
        '    print("Слишком мало!")\n'
        "else:\n"
        '    print("Слишком много!")\n\n'
        'print(f"Загаданное число было: {secret}")\n',
    )}

    {callout(
        "tip",
        "Фиксированное число для примеров курса",
        "В примерах документации иногда используют фиксированное число вместо "
        "<code class=\"inline\">random.randint(...)</code>, чтобы вывод был предсказуем при "
        "показе. В настоящей игре это не нужно — случайность там как раз то, что делает игру "
        "интересной.",
    )}

    <h2>[[icon:debug]] Debug-лаборатория: пять багов</h2>

    <p><strong>Баг 1 — забыт int()</strong></p>
    {code_block("bug_1.py", 'guess = input("Ваш вариант: ")\nif guess < secret:\n    ...\n# TypeError: \'<\' not supported between instances of \'str\' and \'int\'\n', lang="text")}
    <p><strong>Исправление:</strong> <code class="inline">guess = int(input(...))</code>.</p>

    <p><strong>Баг 2 — неверный порядок веток</strong></p>
    {code_block("bug_2.py", "if guess < secret:\n    ...\nelif guess == secret:\n    ...\n", lang="text")}
    <p>Само по себе не сломается, но порядок «сначала неточные, потом точное» менее логичен —
    сравните с шагами 4-6 выше.</p>

    <p><strong>Баг 3 — = вместо ==</strong></p>
    {code_block("bug_3.py", "if guess = secret:\n    ...\n# SyntaxError: invalid syntax\n", lang="text")}
    <p>Одиночный <code class="inline">=</code> в условии — синтаксическая ошибка, Python даже
    не запустит программу (раздел 9.5).</p>

    <p><strong>Баг 4 — неверная граница</strong></p>
    {code_block("bug_4.py", "secret = random.randint(1, 10)\n# но подсказка написана как \"от 1 до 9\" — граница не совпадает с кодом\n", lang="text")}

    <p><strong>Баг 5 — два независимых if вместо elif</strong></p>
    {code_block(
        "bug_5.py",
        "if guess < secret:\n"
        '    print("Слишком мало!")\n'
        "if guess > secret:\n"
        '    print("Слишком много!")\n'
        "# при guess == secret НИ ОДНО сообщение не покажется — а if/elif/else это учитывает\n",
        lang="text",
    )}

    {exercise(2, "Подсказка «горячо/холодно»", "Добавьте четвёртое условие: если разница между guess и secret меньше 3 (используйте abs()) — выведите «Очень близко!» перед основным сообщением.")}

    {practice_card(
        "09-05",
        "Практика: собираем игру «Угадай число» целиком",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-05/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — игра «Угадай число»",
        description="Первая мини-игра книги: угадать случайное число, используя if/elif/else — с решающим деревом и пятью debug-лабораториями.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Угадай число", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Мини-проект — игра «Угадай число»",
        lede="Первая настоящая игра книги — компьютер загадывает число, вы пытаетесь угадать.",
        body_html=body,
        sidebar_groups=sidebar("09-05-mini-proekt-ugadaj-chislo.html"),
        nav=PageNav(prev_href="09-22-otladka-logiki.html", prev_label="Отладка логики", next_href="09-23-mini-proekt-klub-i-pogoda.html", next_label="Мини-проекты: клуб и погода"),
    )
    write("09-05-mini-proekt-ugadaj-chislo.html", out)


# ---------------------------------------------------------------------------
# 9.22 — Мини-проекты: клуб (access checker) и погода (weather advisor)
# ---------------------------------------------------------------------------

def build_23() -> None:
    body = f"""
    <p>Соберём два коротких, но показательных проекта на комбинирование условий.</p>

    <h2>Мини-проект — «Клуб Python»</h2>
    <p>Вход в клуб разрешён только совершеннолетним посетителям с билетом. Это чисто
    учебная логическая задача — не настоящая система безопасности!</p>
    {code_block(
        "klub_python.py",
        'age = int(input("Ваш возраст: "))\n'
        'has_ticket = input("У вас есть билет? (да/нет): ").strip().lower() == "да"\n\n'
        "if age >= 18 and has_ticket:\n"
        '    print("Добро пожаловать в «Клуб Python»!")\n'
        "elif age < 18:\n"
        '    print("Вход только с 18 лет.")\n'
        "else:\n"
        '    print("Нужен билет.")\n',
    )}
    {exercise(2, "VIP без билета", "Добавьте переменную is_vip. VIP-гости проходят даже без билета — используйте or для этого исключения.")}

    <h2 id="pogoda">Мини-проект — советчик погоды</h2>
    <p>Программа даёт рекомендацию на основе температуры и того, идёт ли дождь:</p>
    {code_block(
        "sovetchik_pogody.py",
        'temperature = int(input("Температура: "))\n'
        'is_raining = input("Идёт дождь? (да/нет): ").strip().lower() == "да"\n\n'
        "if temperature < 10 and is_raining:\n"
        '    print("Тёплая куртка и зонт")\n'
        "elif temperature < 10:\n"
        '    print("Тёплая куртка")\n'
        "elif is_raining:\n"
        '    print("Просто зонт")\n'
        "else:\n"
        '    print("Лёгкая одежда, зонт не нужен")\n',
    )}
    {callout(
        "tip",
        "Порядок условий продуман заранее",
        "Обратите внимание: самое специфичное условие (холодно И дождь) стоит первым — точно "
        "по тому же принципу «первое истинное побеждает» из раздела 9.9.",
    )}

    {exercise(2, "Ветреная погода", "Добавьте третий фактор is_windy. При сильном ветре добавьте в рекомендацию «и шапку» к любому из четырёх исходов.")}

    {practice_card(
        "09-23",
        "Практика: клуб и советчик погоды",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-23/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проекты: клуб и погода",
        description="Два мини-проекта: проверка доступа в клуб (and) и советчик погоды (and/or/elif вместе).",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Клуб и погода", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Мини-проекты — клуб и советчик погоды",
        lede="Два практичных мини-проекта на комбинирование условий из разделов 9.11–9.17.",
        body_html=body,
        sidebar_groups=sidebar("09-23-mini-proekt-klub-i-pogoda.html"),
        nav=PageNav(prev_href="09-05-mini-proekt-ugadaj-chislo.html", prev_label="Угадай число", next_href="09-24-mini-proekt-ocenki-i-komandy.html", next_label="Мини-проекты: оценки и команды"),
    )
    write("09-23-mini-proekt-klub-i-pogoda.html", out)


# ---------------------------------------------------------------------------
# 9.23 — Мини-проекты: классификатор оценок и интерпретатор команд
# ---------------------------------------------------------------------------

def build_24() -> None:
    boundaries = comparison_table(
        ["score", "уровень"],
        [["0–49", "неудовлетворительно"], ["50–74", "удовлетворительно"], ["75–89", "хорошо"], ["90–100", "отлично"]],
    )

    body = f"""
    <h2>Мини-проект — классификатор баллов</h2>
    <p>Переводим числовой балл (0–100) в уровень — учебный пример, границы курса условны и не
    отражают реальные образовательные стандарты:</p>
    {boundaries}
    {code_block(
        "klassifikator_ballov.py",
        'score = int(input("Ваш балл (0-100): "))\n\n'
        "if score >= 90:\n"
        '    level = "отлично"\n'
        "elif score >= 75:\n"
        '    level = "хорошо"\n'
        "elif score >= 50:\n"
        '    level = "удовлетворительно"\n'
        "else:\n"
        '    level = "неудовлетворительно"\n\n'
        'print(f"Уровень: {level}")\n',
    )}
    {exercise(2, "Проверьте все границы", "Прогоните классификатор на значениях 0, 49, 50, 74, 75, 89, 90, 100 — убедитесь, что каждое попадает в ожидаемый уровень (раздел 9.19 про границы).")}

    <h2 id="komandy">Мини-проект — текстовый интерпретатор команд</h2>
    <p>Пользователь вводит текстовую команду — программа реагирует. Прямая связь между
    строками из главы 8 и условиями этой главы:</p>
    {code_block(
        "interpretator_komand.py",
        'command = input("Введите команду (start/stop/help): ").strip().lower()\n\n'
        'if command == "start":\n'
        '    print("Запуск...")\n'
        'elif command == "stop":\n'
        '    print("Остановка...")\n'
        'elif command == "help":\n'
        '    print("Доступные команды: start, stop, help")\n'
        "else:\n"
        '    print(f"Неизвестная команда: {command}")\n',
    )}
    {callout(
        "info",
        "[[icon:launch]] В следующей главе",
        "Сейчас программа реагирует на ОДНУ команду и завершается. С циклом "
        "<code class=\"inline\">while</code> (глава 10) она сможет ждать команду за командой, "
        "как настоящая мини-консоль — до тех пор, пока пользователь не введёт «exit».",
    )}

    {exercise(1, "Регистронезависимость", "Проверьте интерпретатор на вводе «START», « Stop », «HELP» — убедитесь, что .strip().lower() делает программу нечувствительной к регистру и пробелам.")}

    {practice_card(
        "09-24",
        "Практика: классификатор оценок и интерпретатор команд",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-24/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проекты: оценки и команды",
        description="Два мини-проекта: классификатор баллов через цепочку elif и текстовый интерпретатор команд.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Оценки и команды", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Мини-проекты — классификатор оценок и интерпретатор команд",
        lede="Упорядоченные elif-цепочки и связь строк из главы 8 с условиями этой главы.",
        body_html=body,
        sidebar_groups=sidebar("09-24-mini-proekt-ocenki-i-komandy.html"),
        nav=PageNav(prev_href="09-23-mini-proekt-klub-i-pogoda.html", prev_label="Клуб и погода", next_href="09-06-nakoplenie-uslovij-itogi.html", next_label="Условия накапливаются и итоги"),
    )
    write("09-24-mini-proekt-ocenki-i-komandy.html", out)


# ---------------------------------------------------------------------------
# 9.24 — Итоги, карта решений, мост к главе 10 (существующий, переработан)
# ---------------------------------------------------------------------------

def build_06() -> None:
    toolbox = decision_map([
        ("Нужно задать один вопрос да/нет?", "if"),
        ("Нужны две альтернативы?", "if / else"),
        ("Нужно несколько взаимоисключающих вариантов?", "if / elif / else"),
        ("Нужно, чтобы ВСЕ условия были истинны?", "and"),
        ("Достаточно ХОТЯ БЫ ОДНОГО истинного условия?", "or"),
        ("Нужно перевернуть условие?", "not"),
        ("Нужно проверить вхождение в текст/группу?", "in"),
        ("Нужно сравнить с None?", "is"),
        ("Нужно сравнить значения?", "==, !=, &lt;, &gt;, &lt;=, &gt;="),
        ("Нужно проверить диапазон?", "цепочка сравнений"),
    ], title="Карта принятия решений — что использовать?")

    body = f"""
    <p>Условия могут накапливаться сколько угодно — <code class="inline">elif</code>,
    <code class="inline">and</code>/<code class="inline">or</code> и вложенность позволяют
    выразить сколь угодно сложное решение. Подведём итоги главы.</p>

    <h2 id="itogi">Карта принятия решений</h2>
    {toolbox}

    <h2>Что мы теперь умеем</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Алгоритм — понятная последовательность действий; собирается из трёх структур: "
        "последовательность, ветвление, повторение.",
        "Тип <code class=\"inline\">bool</code> хранит <code class=\"inline\">True</code> или "
        "<code class=\"inline\">False</code>; шесть операторов сравнения превращают значения в bool.",
        "Truthiness: ноль и пустые значения ведут себя как ложь, всё остальное — как истина "
        "(но текст <code class=\"inline\">\"False\"</code> — это истина!).",
        "<code class=\"inline\">if</code>/<code class=\"inline\">elif</code>/<code class=\"inline\">else"
        "</code> выбирают ровно ОДНУ ветку — в отличие от нескольких независимых "
        "<code class=\"inline\">if</code>, которые могут сработать все разом.",
        "<code class=\"inline\">and</code>, <code class=\"inline\">or</code>, "
        "<code class=\"inline\">not</code> комбинируют условия; у and/or есть short-circuit — "
        "Python не всегда вычисляет второй операнд.",
        "<code class=\"inline\">is</code> и <code class=\"inline\">==</code> — разные вопросы; "
        "<code class=\"inline\">is None</code> — правильный способ проверки на None.",
        "Условия можно вкладывать, но часто их стоит упростить через and; всегда проверяйте "
        "граничные значения.",
    ])}

    <h2>Мост к главе 10</h2>
    <p>Теперь программа умеет принимать ОДНО решение. Но игры и настоящие приложения обычно
    принимают решения СНОВА И СНОВА. «Угадай число» пока даёт только одну попытку — в
    следующей главе мы научим программу <strong>повторять</strong> действия, и игра сможет
    продолжаться, пока число не будет угадано.</p>
    {loop_preview_diagram(
        action_label="Спросить попытку",
        question_label="Угадал?",
        caption="Глава 10: тот же backward-стрелка добавляет повтор — «Угадай число» сможет продолжаться, пока число не будет угадано",
    )}

    {practice_card(
        "09-06",
        "Практика: карта принятия решений",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/09-06/index.html",
    )}
    """
    out = render_page(
        page_title="Условия продолжают накапливаться!",
        description="Карта принятия решений по главе 9 и мост к циклам в главе 10.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Итоги", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Условия продолжают накапливаться!",
        lede="Итоговая карта: какой инструмент выбрать для какой задачи — и что дальше.",
        body_html=body,
        sidebar_groups=sidebar("09-06-nakoplenie-uslovij-itogi.html"),
        nav=PageNav(prev_href="09-24-mini-proekt-ocenki-i-komandy.html", prev_label="Оценки и команды", next_href="../glava-10/index.html", next_label="Глава 10: Немного автоматизации!"),
    )
    write("09-06-nakoplenie-uslovij-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_07()
    build_08()
    build_01()
    build_02()
    build_09()
    build_10()
    build_11()
    build_03()
    build_12()
    build_13()
    build_14()
    build_15()
    build_16()
    build_04()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_22()
    build_05()
    build_23()
    build_24()
    build_06()
