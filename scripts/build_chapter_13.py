#!/usr/bin/env python3
"""Строит Главу 13: «Автоматизация с помощью функций» (site/chapters/glava-13/).

Curriculum v2: одна из фундаментальных глав курса — не просто синтаксис
`def`, а идея «функция — именованный переиспользуемый кусок поведения,
который получает данные, работает с ними и возвращает результат»,
переносимая на любой другой язык программирования. Циклы vs функции,
декомпозиция и абстракция — раньше синтаксиса; определение vs вызов с
управлением потоком выполнения (call site → тело функции → возврат);
параметр vs аргумент через уже знакомую модель имена→объекты, без ложных
«передача по значению/по ссылке»; изменяемые и неизменяемые аргументы,
rebinding vs mutation; позиционные/именованные/умолчания/ловушка
изменяемого значения по умолчанию; positional-only и keyword-only;
*args/**kwargs и распаковка на месте вызова; return во всей глубине
(implicit None, ранний return, несколько значений); чистые функции и
побочные эффекты; LEGB, UnboundLocalError, global, nonlocal и вложенные
функции; стек вызовов и его связь с traceback; докстринги и type hints;
функции как объекты первого класса и lambda; рефакторинг реальных
проектов главы 12 в функции; отдельный урок отладки функций; тестирование
функций; и финальная Turtle Function Studio с настоящими сгенерированными
результатами.

Существующие маршруты и практики (13-01..13-08, включая Turtle-проект)
сохранены на месте и расширены по этому же шаблону; новый материал —
новые страницы и новые ID практик (13-09..13-27), без переиспользования
занятых ID.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_13_examples import EXAMPLES
from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    branch_diagram,
    call_flow_diagram,
    call_stack_diagram,
    callout,
    capability_map,
    classic_vs_modern,
    code_block,
    comparison_table,
    converge_diagram,
    decision_map,
    elif_ladder_diagram,
    exercise,
    flow_diagram,
    flowchart,
    local_required_card,
    namespace_diagram,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
    tree_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-13"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Обзор главы"),
    ("13-09-zachem-programme-funkcii.html", "Зачем программе функции"),
    ("13-01-nastoyashaya-avtomatizaciya.html", "Настоящая автоматизация. Первая функция"),
    ("13-10-vyzov-i-vozvrat-upravlenie.html", "Что происходит во время вызова"),
    ("13-02-zachem-funkcii.html", "Параметр и аргумент"),
    ("13-11-izmenyaemye-i-nezmenyaemye-argumenty.html", "Изменяемые и неизменяемые аргументы"),
    ("13-12-pozicionnye-i-imennye.html", "Позиционные и именованные аргументы"),
    ("13-04-argumenty.html", "Значения по умолчанию и *args"),
    ("13-13-args-kwargs-raspakovka.html", "*args, **kwargs и распаковка"),
    ("13-14-positional-only-keyword-only.html", "Positional-only и keyword-only"),
    ("13-03-vozvrashaem-otvet.html", "Возвращаем ответ"),
    ("13-15-funkcii-vhod-vyhod.html", "Вход, работа, выход: чистые функции"),
    ("13-05-globalnye-lokalnye.html", "Глобальные и локальные переменные"),
    ("13-16-vlozhennye-funkcii-nonlocal.html", "Вложенные функции и nonlocal"),
    ("13-17-stek-vyzovov.html", "Стек вызовов и traceback"),
    ("13-18-proektiruem-funkciyu.html", "Проектируем хорошую функцию"),
    ("13-19-dokumentaciya-i-tipy.html", "Докстринги и подсказки типов"),
    ("13-20-funkcii-kak-obekty.html", "Функции как объекты"),
    ("13-06-lambda.html", "Лямбда-функции"),
    ("13-21-funkcii-kak-konvejer.html", "Функции как конвейер"),
    ("13-22-refaktoring-glavy-12.html", "Рефакторим проекты главы 12"),
    ("13-23-debug-lab-funkcii.html", "Debug Lab: типичные ошибки функций"),
    ("13-24-testirovanie-funkcij.html", "Тестируем функции"),
    ("13-07-mini-proekt-domashka.html", "Мини-проект: домашнее задание по математике"),
    ("13-25-mini-proekt-analizator-v2.html", "Мини-проект: анализатор текста v2"),
    ("13-26-mini-proekt-konverter-i-utility.html", "Мини-проекты: конвертер и утилиты коллекций"),
    ("13-08-mini-proekt-figury-itogi.html", "Мини-проект: Turtle Function Studio и итоги"),
]

PRACTICE_IDS = [
    "13-09", "13-01", "13-10", "13-02", "13-11", "13-12", "13-04", "13-13",
    "13-14", "13-03", "13-15", "13-05", "13-16", "13-17", "13-18", "13-19",
    "13-20", "13-06", "13-21", "13-22", "13-23", "13-24", "13-07", "13-25",
    "13-26", "13-27", "13-08",
]

LOCAL_REQUIRED_IDS = {"13-08"}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 13 · Функции", items),
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


def turtle_output(name: str, filename: str, *, caption: str, alt: str) -> str:
    """КОД → РЕАЛЬНЫЙ OUTPUT — тот же компонент, что и в главах 6-7-10-12.
    code_block() слева/сверху, реально выполненная картинка справа/снизу;
    код в EXAMPLES не содержит exitonclick()/bye() — эта строка дописывается
    только для читателя."""
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
          <img src="{IMG}/chapter-13/output/{name}.png" alt="{alt}"
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
        next_href, next_label = "../glava-14/index.html", "Глава 14: Создаём объекты реального мира"
    return PageNav(prev_href=prev_href, prev_label=prev_label, next_href=next_href, next_label=next_label)


def page(href: str, *, page_title: str, description: str, kicker_suffix: str, h1: str, lede: str, body_html: str) -> None:
    out = render_page(
        page_title=page_title,
        description=description,
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), (kicker_suffix, "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1=h1,
        lede=lede,
        body_html=body_html,
        sidebar_groups=sidebar(href),
        nav=nav_for(href),
    )
    write(href, out)


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=13,
        baseline_page=283,
        title="Автоматизация с помощью функций",
        description="Функции · декомпозиция · параметры · return · области видимости. Научимся "
        "превращать большие программы в понятные части: давать алгоритмам имена, передавать им "
        "данные, получать результаты, управлять областью видимости и переиспользовать код без "
        "копирования — идея, которая переносится на любой другой язык программирования.",
        meta_items=["[[icon:timer]] ~9 часов", "[[icon:architecture]] def, return, scope", "[[icon:practice]] 27 практик"],
        sections=[
            ChapterSectionLink("13.1", "Зачем программе функции", "13-09-zachem-programme-funkcii.html", "283"),
            ChapterSectionLink("13.2", "Настоящая автоматизация. Первая функция", "13-01-nastoyashaya-avtomatizaciya.html", "287"),
            ChapterSectionLink("13.3", "Что происходит во время вызова", "13-10-vyzov-i-vozvrat-upravlenie.html", "290"),
            ChapterSectionLink("13.4", "Параметр и аргумент", "13-02-zachem-funkcii.html", "293"),
            ChapterSectionLink("13.5", "Изменяемые и неизменяемые аргументы", "13-11-izmenyaemye-i-nezmenyaemye-argumenty.html", "296"),
            ChapterSectionLink("13.6", "Позиционные и именованные аргументы", "13-12-pozicionnye-i-imennye.html", "299"),
            ChapterSectionLink("13.7", "Значения по умолчанию и *args", "13-04-argumenty.html", "302"),
            ChapterSectionLink("", "Ловушка изменяемого значения по умолчанию", "13-04-argumenty.html#lovushka", "304"),
            ChapterSectionLink("13.8", "*args, **kwargs и распаковка", "13-13-args-kwargs-raspakovka.html", "306"),
            ChapterSectionLink("13.9", "Positional-only и keyword-only", "13-14-positional-only-keyword-only.html", "309"),
            ChapterSectionLink("13.10", "Возвращаем ответ", "13-03-vozvrashaem-otvet.html", "312"),
            ChapterSectionLink("13.11", "Вход, работа, выход: чистые функции", "13-15-funkcii-vhod-vyhod.html", "315"),
            ChapterSectionLink("13.12", "Глобальные и локальные переменные", "13-05-globalnye-lokalnye.html", "318"),
            ChapterSectionLink("13.13", "Вложенные функции и nonlocal", "13-16-vlozhennye-funkcii-nonlocal.html", "321"),
            ChapterSectionLink("13.14", "Стек вызовов и traceback", "13-17-stek-vyzovov.html", "324"),
            ChapterSectionLink("13.15", "Проектируем хорошую функцию", "13-18-proektiruem-funkciyu.html", "327"),
            ChapterSectionLink("13.16", "Докстринги и подсказки типов", "13-19-dokumentaciya-i-tipy.html", "330"),
            ChapterSectionLink("13.17", "Функции как объекты", "13-20-funkcii-kak-obekty.html", "333"),
            ChapterSectionLink("13.18", "Лямбда-функции", "13-06-lambda.html", "336"),
            ChapterSectionLink("13.19", "Функции как конвейер", "13-21-funkcii-kak-konvejer.html", "339"),
            ChapterSectionLink("13.20", "Рефакторим проекты главы 12", "13-22-refaktoring-glavy-12.html", "342"),
            ChapterSectionLink("13.21", "Debug Lab: типичные ошибки функций", "13-23-debug-lab-funkcii.html", "345"),
            ChapterSectionLink("13.22", "Тестируем функции", "13-24-testirovanie-funkcij.html", "348"),
            ChapterSectionLink("13.23", "Мини-проект — домашнее задание по математике", "13-07-mini-proekt-domashka.html", "351"),
            ChapterSectionLink("13.24", "Мини-проект — анализатор текста v2", "13-25-mini-proekt-analizator-v2.html", "354"),
            ChapterSectionLink("13.25", "Мини-проекты — конвертер и утилиты коллекций", "13-26-mini-proekt-konverter-i-utility.html", "357"),
            ChapterSectionLink("13.26", "Мини-проект — Turtle Function Studio", "13-08-mini-proekt-figury-itogi.html", "360"),
            ChapterSectionLink("", "Итоги главы", "13-08-mini-proekt-figury-itogi.html#itogi", "364"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 13-09 · Зачем программе функции
# ---------------------------------------------------------------------------

def build_09() -> None:
    body = f"""
    <h2>Проблема, которую циклы не решают</h2>
    <p>В главе 12 наши проекты становились всё крупнее — и в них стали появляться повторяющиеся
    логические блоки. Например, в викторине один и тот же набор действий — «спросить вопрос,
    нормализовать ответ, сравнить, посчитать» — фактически повторяется на каждой итерации. Цикл
    (глава 10) отлично с этим справляется, <strong>пока повторение происходит подряд, в одном
    месте</strong>.</p>
    <p>Но что, если тот же самый набор действий нужен:</p>
    <ul>
      <li>в <strong>разных местах</strong> программы — не подряд;</li>
      <li>с <strong>разными данными</strong> каждый раз;</li>
      <li>из <strong>разных проектов</strong> вообще;</li>
      <li><strong>по требованию</strong>, а не по расписанию цикла?</li>
    </ul>
    <p>Цикл здесь не поможет — он умеет повторять только то, что стоит прямо у него в теле.
    Нужен другой инструмент: способ <strong>дать этому действию имя</strong> и вызывать его
    откуда угодно.</p>

    <h2>Цикл vs функция</h2>
    {two_up(
        flow_diagram([("ПОВТОРИТЬ", "сейчас"), ("ПОВТОРИТЬ", "сейчас"), ("ПОВТОРИТЬ", "сейчас")], caption="Цикл: один поток повторяющегося выполнения"),
        branch_diagram("draw_square (определена один раз)", [("ВЫЗОВ", "откуда угодно"), ("ВЫЗОВ", "откуда угодно"), ("ВЫЗОВ", "откуда угодно")], caption="Функция: определена один раз, вызывается по требованию"),
    )}
    {callout(
        "info",
        "Не альтернативы, а дополнение друг друга",
        "<strong>Циклы автоматизируют повторение в потоке выполнения.</strong> "
        "<strong>Функции автоматизируют переиспользование поведения.</strong> Совсем скоро мы "
        "увидим, как функция вызывается ИЗНУТРИ цикла — они прекрасно работают вместе, а не "
        "вместо друг друга.",
    )}

    <h2>Функции — это декомпозиция</h2>
    <p>В главе 12 мы уже разбивали большую задачу на маленькие шаги — это называлось
    <strong>декомпозицией</strong>. Функция — это способ не просто мысленно выделить шаг, а
    буквально дать ему имя в коде:</p>
    {branch_diagram(
        "ВИКТОРИНА",
        [("show_question()", "показать вопрос"), ("check_answer()", "проверить ответ"), ("show_result()", "показать результат")],
        caption="Большая задача → части с понятными именами — это и есть декомпозиция в коде",
    )}
    <p>Каждая функция — это осмысленное имя для одной части большего алгоритма.</p>

    <h2>Абстракция: полезный уровень детализации</h2>
    <p>Вы уже пользуетесь <code class="inline">print(...)</code>, не думая о том, как именно
    текст оказывается на экране. Точно так же вызов <code class="inline">draw_house()</code>
    мог бы скрыть десятки команд рисования крыши, стен и окон:</p>
    {flow_diagram([("draw_house()", "один вызов"), ("десятки команд", "рисования внутри")], caption="Вызов прячет детали реализации за понятным именем")}
    {callout(
        "tip",
        "Абстракция — не «спрятать всё», а выбрать полезный уровень детализации",
        "<strong>Абстракция</strong> означает, что мы можем пользоваться осмысленной операцией, "
        "не думая каждый раз о каждой детали её реализации. Это не значит, что детали "
        "недоступны или неважны — просто для большинства задач достаточно знать ЧТО делает "
        "<code class=\"inline\">draw_house()</code>, а не КАК именно.",
    )}

    <h2>Вы уже вызывали функции — с самой первой главы</h2>
    <p><code class="inline">print()</code>, <code class="inline">input()</code>,
    <code class="inline">len()</code>, <code class="inline">type()</code>,
    <code class="inline">int()</code>, <code class="inline">range()</code>,
    <code class="inline">sorted()</code>, <code class="inline">min()</code>,
    <code class="inline">max()</code> — все они функции, просто <strong>встроенные</strong> в
    Python. Всё это время вы их ВЫЗЫВАЛИ. Теперь научимся их СОЗДАВАТЬ:</p>
    {comparison_table(
        ["Встроенная функция", "Ваша будущая функция"],
        [["<code class=\"inline\">len(\"Python\")</code>", "<code class=\"inline\">calculate_area(10, 5)</code>"]],
    )}
    <p>Общая модель одна и та же для обеих:</p>
    {flow_diagram([("ИМЯ + АРГУМЕНТЫ", ""), ("ВЫЗОВ", ""), ("РЕЗУЛЬТАТ / ЭФФЕКТ", "")], caption="Имя функции + аргументы → вызов → результат или эффект — для встроенных функций и ваших собственных одинаково")}

    {practice_card(
        "13-09",
        "Практика: цикл или функция — что решает задачу",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-09/index.html",
    )}
    """
    page(
        "13-09-zachem-programme-funkcii.html",
        page_title="Зачем программе функции",
        description="Циклы против функций, декомпозиция, абстракция — и напоминание, что встроенные функции были функциями всё это время.",
        kicker_suffix="Зачем программе функции",
        h1="Зачем программе функции",
        lede="Циклы автоматизируют повторение в потоке выполнения. Функции автоматизируют "
        "переиспользование поведения — и это не одно и то же.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-01 · Настоящая автоматизация. Наша первая функция (расширено)
# ---------------------------------------------------------------------------

def build_01() -> None:
    body = f"""
    <h2>Настоящая автоматизация</h2>
    <p>Циклы из главы 10 автоматизировали повторение одного и того же кода. Но что если один и
    тот же <em>набор действий</em> нужен в разных местах программы — не подряд, а время от
    времени? Копировать код каждый раз — плохая идея: любое исправление придётся вносить
    во все копии. <strong>Функции</strong> решают эту проблему раз и навсегда.</p>

    <h2>Наша первая функция</h2>
    {code_block(
        "pervaya_funkciya.py",
        "def privetstvie():\n"
        '    print("Привет, Python!")\n\n'
        "privetstvie()\n"
        "privetstvie()\n"
        "privetstvie()\n",
    )}

    <h2>Анатомия def</h2>
    {comparison_table(
        ["Часть", "Значение"],
        [
            ["<code class=\"inline\">def</code>", "ключевое слово: «дальше идёт определение функции»"],
            ["<code class=\"inline\">privetstvie</code>", "имя функции — по нему функцию будут вызывать"],
            ["<code class=\"inline\">()</code>", "список параметров (здесь пуст — функция не принимает данных)"],
            ["<code class=\"inline\">:</code>", "начало тела функции"],
            ["<code class=\"inline\">    print(...)</code>", "тело — код с отступом, который выполнится при вызове"],
        ],
    )}
    <p><code class="inline">def</code> <strong>определяет</strong> функцию — записывает её код,
    но пока не выполняет его. Функция выполняется только тогда, когда вы её
    <strong>вызываете</strong> — по имени со скобками: <code class="inline">privetstvie()</code>.</p>

    {callout(
        "warning",
        "Определение — это ещё не вызов",
        "Если написать только <code class=\"inline\">def privetstvie(): ...</code> и не "
        "добавить <code class=\"inline\">privetstvie()</code> ниже, программа не выведет "
        "ничего — Python просто запомнит функцию, но не запустит её.",
    )}

    <h2>Определение выполняется один раз, по-особому</h2>
    <p>Когда Python доходит до строки <code class="inline">def privetstvie():</code>, тело
    функции <strong>не выполняется</strong> как обычные последовательные команды. Вместо этого
    создаётся объект функции, привязанный к имени <code class="inline">privetstvie</code> — и
    выполнение программы продолжается СРАЗУ ПОСЛЕ определения. Тело запустится только позже,
    когда произойдёт вызов.</p>

    <h2>Функция как объект</h2>
    <p>Мы уже знаем модель «имя указывает на объект» (глава 3). Функция — не исключение:</p>
    {namespace_diagram([("privetstvie", "ФУНКЦИЯ-ОБЪЕКТ")], caption="После def имя privetstvie указывает на объект функции")}
    {code_block("imya_bez_skobok.py", "print(privetstvie)   # <function privetstvie at 0x...> — сам объект функции\nprivetstvie()          # Привет, Python! — а это ВЫЗОВ\n")}
    {callout(
        "tip",
        "privetstvie и privetstvie() — не одно и то же",
        "Без скобок — обращение к самому объекту функции (её можно передать, сохранить, "
        "сравнить). Со скобками — команда «выполни её прямо сейчас». Это различие станет "
        "особенно важным в §13.17, когда функции начнут передаваться как обычные значения.",
    )}

    {practice_card(
        "13-01",
        "Практика: определяем и вызываем первую функцию",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-01/index.html",
    )}
    """
    page(
        "13-01-nastoyashaya-avtomatizaciya.html",
        page_title="Настоящая автоматизация. Наша первая функция",
        description="Введение в функции Python: анатомия def, определение vs вызов, функция как объект.",
        kicker_suffix="Первая функция",
        h1="Настоящая автоматизация",
        lede="Функции переиспользуют набор действий столько раз, сколько нужно — без "
        "копирования кода.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-10 · Что происходит во время вызова
# ---------------------------------------------------------------------------

def build_10() -> None:
    body = f"""
    <h2>Вызов — это не «выполнение где-то в стороне»</h2>
    <p>Разберём по шагам, что реально происходит, когда программа доходит до
    <code class="inline">greet()</code>:</p>
    {code_block(
        "poryadok_vypolneniya.py",
        "def greet():\n"
        '    print("Привет")\n\n'
        'print("До")\n'
        "greet()\n"
        'print("После")\n',
    )}
    {terminal_transcript(["До", "Привет", "После"], caption="Порядок вывода — сверху вниз, как и порядок выполнения строк")}

    <h2>Управление потоком выполнения</h2>
    {call_flow_diagram(
        ['print("До")'],
        "greet()",
        ['print("Привет")'],
        ['print("После")'],
        function_name="greet",
        caption="Вызов передаёт управление в тело функции; после её завершения управление возвращается точно на следующую строку",
    )}
    <p>Учащийся должен буквально <strong>увидеть</strong>: вызов → переход внутрь функции →
    выполнение тела → возврат к месту вызова → продолжение со следующей строки. Функция не
    выполняется «где-то в стороне» — выполнение программы буквально ныряет внутрь неё и
    возвращается обратно.</p>

    <h2>Место вызова</h2>
    <p>Строка, где стоит <code class="inline">greet()</code>, называется
    <strong>местом вызова</strong> (call site). Именно сюда возвращается управление, когда
    функция заканчивается:</p>
    {code_block("mesto-vyzova.py", "result = calculate(2, 3)\n# ↑ это место вызова — после calculate() выполнение продолжится СРАЗУ ЗДЕСЬ\n")}

    {practice_card(
        "13-10",
        "Практика: предсказываем порядок вывода",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-10/index.html",
    )}
    """
    page(
        "13-10-vyzov-i-vozvrat-upravlenie.html",
        page_title="Что происходит во время вызова",
        description="Управление потоком выполнения при вызове функции: переход в тело, выполнение, возврат к месту вызова.",
        kicker_suffix="Вызов и возврат",
        h1="Что происходит во время вызова",
        lede="Вызов функции — это переход управления внутрь тела функции и обязательный "
        "возврат к месту вызова, а не «выполнение где-то в стороне».",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-02 · Параметр и аргумент (расширено)
# ---------------------------------------------------------------------------

def build_02() -> None:
    body = f"""
    <h2>Зачем нужны функции?</h2>
    <ul>
      <li><strong>Код не повторяется</strong> — исправление вносится в одном месте.</li>
      <li><strong>Программу легче читать</strong> — имя функции объясняет, что происходит, не
        заставляя вникать в детали реализации.</li>
      <li><strong>Легче искать ошибки</strong> — если что-то сломалось в приветствии, вы точно
        знаете, где искать: внутри <code class="inline">privetstvie()</code>.</li>
    </ul>

    <h2>Каждый раз делаем что-то новое!</h2>
    <p>Функция без входных данных всегда делает одно и то же. Чтобы функция вела себя по-разному
    в зависимости от ситуации, ей передают <strong>аргументы</strong> — значения в скобках при
    вызове:</p>
    {code_block(
        "argumenty.py",
        "def privetstvie(imya):\n"
        '    print(f"Привет, {imya}!")\n\n'
        'privetstvie("Ада")\n'
        'privetstvie("Cartesian")\n',
    )}

    <h2>Параметр vs аргумент — точное различие</h2>
    <p>Эти два слова легко перепутать, но у них разные роли:</p>
    {comparison_table(
        ["", "Где встречается", "Что это"],
        [
            ["<strong>Параметр</strong>", "в определении: <code class=\"inline\">def privetstvie(imya):</code>", "локальное имя внутри функции"],
            ["<strong>Аргумент</strong>", "в вызове: <code class=\"inline\">privetstvie(\"Ада\")</code>", "объект/значение, переданное при вызове"],
        ],
    )}
    {converge_diagram(['"Ада" (аргумент)'], "imya (параметр)", caption="Аргумент из места вызова становится значением параметра внутри функции")}

    <h2>Параметры — это локальные имена</h2>
    <p>Продолжим уже знакомую модель «имя указывает на объект» (глава 3): вызов функции создаёт
    новую привязку параметра к переданному объекту:</p>
    {namespace_diagram([("imya", '"Ада"')], caption="Внутри вызова privetstvie(\"Ада\") имя imya указывает на переданный объект")}

    {callout(
        "warning",
        "«Передача по значению» и «по ссылке» — вводят в заблуждение",
        "Не думайте о Python как о языке, где «всё передаётся по ссылке» или «всё передаётся по "
        "значению» — обе формулировки слишком неточны и здесь не нужны. Точнее так: "
        "<strong>при вызове функции её параметры привязываются к тем же объектам, что и "
        "переданные аргументы</strong> — та же модель «имя → объект», что мы используем с самой "
        "главы 3. Иногда это называют <em>call by sharing</em>, но специальный термин "
        "запоминать не обязательно — важна сама модель.",
    )}

    <h2>Без аргументов?</h2>
    <p>Функция без параметров в скобках — например, <code class="inline">privetstvie()</code>
    из §13.2 — тоже совершенно нормальна: не каждой функции нужны входные данные.</p>

    {practice_card(
        "13-02",
        "Практика: параметр vs аргумент",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-02/index.html",
    )}
    """
    page(
        "13-02-zachem-funkcii.html",
        page_title="Параметр и аргумент",
        description="Точное различие параметра и аргумента, параметры как локальные имена — и почему «передача по значению/по ссылке» вводит в заблуждение.",
        kicker_suffix="Параметр и аргумент",
        h1="Зачем нужны функции?",
        lede="Параметр — это имя в определении. Аргумент — значение, переданное при вызове. "
        "Разница между ними — фундамент всего, что будет дальше.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-11 · Изменяемые и неизменяемые аргументы
# ---------------------------------------------------------------------------

def build_11() -> None:
    body = f"""
    <h2>Неизменяемый аргумент: rebinding не выходит наружу</h2>
    {code_block(
        "immutable_argument.py",
        "def add_one(number):\n"
        "    number += 1\n"
        "    print(number)\n\n"
        "x = 10\n"
        "add_one(x)\n"
        "print(x)\n",
    )}
    {terminal_transcript(["11", "10"], caption="add_one(x) печатает 11, но x снаружи остался 10")}
    {two_up(
        namespace_diagram([("x", "10")], caption="До вызова: x → 10"),
        namespace_diagram([("x", "10"), ("number", "11")], caption="Внутри add_one: number += 1 привязывает number к НОВОМУ объекту 11 — x это не затрагивает"),
    )}
    {callout(
        "warning",
        "Не «функция получает копию x»",
        "Точнее: <code class=\"inline\">number</code> сначала указывает туда же, куда и "
        "<code class=\"inline\">x</code> (на 10). Но <code class=\"inline\">number += 1</code> "
        "— это <code class=\"inline\">number = number + 1</code>: создаётся НОВЫЙ объект "
        "<code class=\"inline\">11</code>, и <code class=\"inline\">number</code> начинает "
        "указывать на него. <code class=\"inline\">x</code> по-прежнему указывает на старый "
        "объект <code class=\"inline\">10</code> — они разошлись.",
    )}

    <h2>Изменяемый аргумент: мутация видна снаружи</h2>
    {code_block(
        "mutable_argument.py",
        "def add_item(items):\n"
        '    items.append("Python")\n\n'
        'skills = ["Git"]\n'
        "add_item(skills)\n"
        "print(skills)\n",
    )}
    {terminal_transcript(["['Git', 'Python']"], caption="skills изменился, хотя мы вызвали функцию, а не присвоили skills напрямую")}
    {converge_diagram(["skills (снаружи)", "items (параметр)"], "['Git', 'Python']", caption="skills и items — два имени ОДНОГО списка; items.append(...) меняет его для обоих")}
    {callout(
        "tip",
        "Это не магия — это тот же aliasing из главы 11",
        "<code class=\"inline\">items</code> внутри функции указывает на ТОТ ЖЕ объект-список, "
        "что и <code class=\"inline\">skills</code> снаружи. <code class=\"inline\">.append(...)</code> "
        "мутирует этот общий объект — поэтому изменение видно через оба имени. Это ровно тот же "
        "принцип aliasing, что мы разбирали в §11.9, только теперь одно из «двух имён» —"
        " параметр функции.",
    )}

    <h2>Rebinding vs mutation — сравниваем напрямую</h2>
    {code_block(
        "rebinding_vs_mutation.py",
        "def replace(items):\n"
        '    items = ["new"]      # rebinding: items теперь указывает на ДРУГОЙ список\n\n'
        "def modify(items):\n"
        '    items.append("new")  # mutation: меняется ТОТ ЖЕ список\n',
    )}
    {comparison_table(
        ["", "replace(items)", "modify(items)"],
        [
            ["Что происходит", "переприсваивание локального имени <code class=\"inline\">items</code>", "изменение объекта, на который <code class=\"inline\">items</code> указывает"],
            ["Видно снаружи после вызова?", "нет — снаружи всё как было", "да — тот же объект изменился"],
        ],
    )}
    {callout(
        "info",
        "Главное практическое правило",
        "Присваивание параметру (<code class=\"inline\">items = ...</code>) отвязывает "
        "локальное имя от аргумента — снаружи ничего не меняется. Вызов мутирующего метода "
        "(<code class=\"inline\">.append()</code>, <code class=\"inline\">.sort()</code>, "
        "<code class=\"inline\">[i] = ...</code>) меняет сам объект — и это видно снаружи, если "
        "объект изменяемый.",
    )}

    {practice_card(
        "13-11",
        "Практика: rebinding vs mutation",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-11/index.html",
    )}
    """
    page(
        "13-11-izmenyaemye-i-nezmenyaemye-argumenty.html",
        page_title="Изменяемые и неизменяемые аргументы",
        description="Почему изменения неизменяемого аргумента не видны снаружи функции, а мутация изменяемого — видна. Rebinding vs mutation.",
        kicker_suffix="Изменяемые аргументы",
        h1="Изменяемые и неизменяемые аргументы",
        lede="Один из самых важных уроков главы: присваивание параметру и мутация объекта, на "
        "который он указывает, — это два совершенно разных действия.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-12 · Позиционные и именованные аргументы
# ---------------------------------------------------------------------------

def build_12() -> None:
    body = f"""
    <h2>Несколько параметров</h2>
    {code_block("neskolko_parametrov.py", "def rectangle_area(width, height):\n    return width * height\n\nprint(rectangle_area(10, 5))   # 50\n")}
    {comparison_table(["Аргумент", "Параметр"], [["10", "width"], ["5", "height"]])}

    <h2>Позиционные аргументы</h2>
    <p>По умолчанию Python сопоставляет аргументы с параметрами <strong>по порядку</strong> —
    первый аргумент попадает в первый параметр, и так далее:</p>
    {code_block("pozicionnye.py", 'create_user("Anna", 25)\n# position 1 → name = "Anna"\n# position 2 → age  = 25\n')}
    {callout(
        "warning",
        "Перепутанный порядок — не всегда ошибка Python, но всегда ошибка логики",
        "<code class=\"inline\">create_user(25, \"Anna\")</code> может не вызвать никакой "
        "ошибки типов — Python не запрещает передать число туда, где обычно передают строку. "
        "Но результат окажется логически неверным: <code class=\"inline\">name</code> получит "
        "<code class=\"inline\">25</code>, а <code class=\"inline\">age</code> — "
        "<code class=\"inline\">\"Anna\"</code>. Позиционные аргументы удобны, но требуют "
        "помнить точный порядок.",
    )}

    <h2>Именованные аргументы</h2>
    <p>Аргумент можно передать по имени параметра — тогда порядок уже не важен:</p>
    {code_block(
        "imennye.py",
        "create_user(\n"
        '    name="Anna",\n'
        "    age=25,\n"
        ")\n",
    )}
    {capability_map([
        ("Читаемость", ["видно, что есть что, прямо в вызове"]),
        ("Порядок неважен", ["age=25, name=\"Anna\" — сработает так же"]),
        ("Удобство API", ["особенно при многих параметрах"]),
    ], title="Зачем именованные аргументы")}

    <h2>Смешиваем позиционные и именованные</h2>
    {code_block("smeshannye.py", "def function(width, height, color):\n    ...\n\nfunction(10, height=20, color=\"red\")   # можно\n")}
    {callout(
        "info",
        "Правило порядка",
        "Позиционные аргументы всегда идут ПЕРЕД именованными в вызове — "
        "<code class=\"inline\">function(width=10, 20, \"red\")</code> вызовет "
        "<code class=\"inline\">SyntaxError</code>. И один и тот же параметр нельзя получить "
        "дважды — <code class=\"inline\">function(10, 20, width=5)</code> вызовет "
        "<code class=\"inline\">TypeError</code>, так как <code class=\"inline\">width</code> "
        "уже получил значение позиционно.",
    )}

    {practice_card(
        "13-12",
        "Практика: позиционные и именованные аргументы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-12/index.html",
    )}
    """
    page(
        "13-12-pozicionnye-i-imennye.html",
        page_title="Позиционные и именованные аргументы",
        description="Сопоставление аргументов по позиции и по имени параметра, риск перепутанного порядка, смешивание позиционных и именованных.",
        kicker_suffix="Позиционные и именованные",
        h1="Позиционные и именованные аргументы",
        lede="Два способа сообщить функции, какой аргумент к какому параметру относится — у "
        "каждого свои плюсы.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-04 · Значения по умолчанию и *args (расширено: ловушка изменяемого умолчания)
# ---------------------------------------------------------------------------

def build_04() -> None:
    body = f"""
    <h2>Нет аргументов? Что делать!</h2>
    <p>Если вызвать функцию без обязательного аргумента, Python сообщит об ошибке. Чтобы
    аргумент можно было пропустить, ему задают <strong>значение по умолчанию</strong>:</p>
    {code_block(
        "znachenie_po_umolchaniyu.py",
        "def privetstvie(imya=\"друг\"):\n"
        '    print(f"Привет, {imya}!")\n\n'
        "privetstvie()          # Привет, друг!\n"
        'privetstvie("Ада")     # Привет, Ада!\n',
    )}
    {comparison_table(
        ["Сигнатура", "Роль"],
        [["<code class=\"inline\">imya</code>", "обязательный параметр — если бы не было умолчания"], ["<code class=\"inline\">imya=\"друг\"</code>", "необязательный параметр со значением по умолчанию"]],
    )}

    <h2 id="lovushka">Ловушка изменяемого значения по умолчанию</h2>
    <p>Это один из самых известных сюрпризов Python — и его нужно разобрать не торопясь.</p>
    {code_block(
        "mutable_default_trap.py",
        "def add_task(task, tasks=[]):\n"
        "    tasks.append(task)\n"
        "    return tasks\n\n"
        'print(add_task("A"))\n'
        'print(add_task("B"))\n',
    )}
    {terminal_transcript(["['A']", "['A', 'B']"], caption="Второй вызов не начинает с пустого списка — B добавился к тому же списку, что и A!")}
    {callout(
        "warning",
        "Список по умолчанию создаётся ОДИН РАЗ — когда выполняется def",
        "<code class=\"inline\">tasks=[]</code> вычисляется в момент <strong>определения</strong> "
        "функции, а не заново при каждом вызове. Получается один и тот же список-объект по "
        "умолчанию, общий для всех вызовов, где аргумент не передан явно.",
    )}
    {call_flow_diagram(
        [],
        "def add_task(task, tasks=[]):",
        ["создаётся список-объект по умолчанию []"],
        [],
        function_name="(на этапе определения)",
        caption="Список по умолчанию создаётся один раз, когда Python выполняет саму строку def",
    )}
    {converge_diagram(["Вызов 1: add_task('A')", "Вызов 2: add_task('B')"], "ОДИН И ТОТ ЖЕ список по умолчанию", caption="Оба вызова без явного tasks используют один и тот же общий список")}

    <h2>Правильный паттерн: None как отметка «не передано»</h2>
    {code_block(
        "mutable_default_fix.py",
        "def add_task(task, tasks=None):\n"
        "    if tasks is None:\n"
        "        tasks = []\n\n"
        "    tasks.append(task)\n"
        "    return tasks\n",
    )}
    {callout(
        "tip",
        "None — безопасный сигнальный аргумент по умолчанию",
        "<code class=\"inline\">None</code> — неизменяемый одиночный объект, поэтому его можно "
        "безопасно использовать как значение по умолчанию. Проверка "
        "<code class=\"inline\">if tasks is None</code> (глава 9: <code class=\"inline\">is "
        "None</code>) создаёт НОВЫЙ пустой список при каждом вызове без аргумента — ровно то "
        "поведение, которое интуитивно ожидалось. Это не единственный способ решить проблему, "
        "но самый распространённый.",
    )}

    <h2>Слишком много аргументов!</h2>
    <p>Иногда заранее неизвестно, сколько аргументов понадобится передать. Символ
    <code class="inline">*</code> перед именем параметра собирает <strong>любое</strong>
    количество аргументов в один кортеж (глава 11):</p>
    {code_block(
        "args.py",
        "def summa_vseh(*chisla):\n"
        "    itog = 0\n"
        "    for n in chisla:\n"
        "        itog += n\n"
        "    return itog\n\n"
        "print(summa_vseh(1, 2))           # 3\n"
        "print(summa_vseh(1, 2, 3, 4, 5))  # 15 — сколько угодно аргументов\n",
    )}

    {callout(
        "info",
        "Именованные аргументы — напоминание",
        "Аргументы можно передавать и по имени, а не только по порядку: "
        "<code class=\"inline\">privetstvie(imya=\"Ада\")</code> — подробнее об этом в §13.6.",
    )}

    {practice_card(
        "13-04",
        "Практика: значения по умолчанию и ловушка изменяемого умолчания",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-04/index.html",
    )}
    """
    page(
        "13-04-argumenty.html",
        page_title="Значения по умолчанию и *args",
        description="Значения по умолчанию, знаменитая ловушка изменяемого значения по умолчанию и правильный паттерн с None, *args для произвольного числа аргументов.",
        kicker_suffix="Значения по умолчанию",
        h1="Нет аргументов? Слишком много аргументов!",
        lede="Значения по умолчанию делают аргумент необязательным — но изменяемое значение по "
        "умолчанию скрывает одну из самых известных ловушек Python.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-13 · *args, **kwargs и распаковка
# ---------------------------------------------------------------------------

def build_13() -> None:
    body = f"""
    <h2>*args — произвольное число позиционных аргументов</h2>
    {code_block("args_povtorenie.py", "def total(*numbers):\n    return sum(numbers)\n\ntotal(1, 2, 3, 4)\n")}
    {namespace_diagram([("numbers", "(1, 2, 3, 4)")], caption="Внутри функции numbers — обычный кортеж (глава 11)")}
    {callout(
        "info",
        "args — просто общепринятое имя",
        "Работает именно символ <code class=\"inline\">*</code> перед параметром — имя "
        "<code class=\"inline\">args</code> лишь общепринятое соглашение. "
        "<code class=\"inline\">def total(*numbers)</code> работает совершенно так же, как "
        "<code class=\"inline\">def total(*args)</code>.",
    )}

    <h2>**kwargs — произвольное число именованных аргументов</h2>
    {code_block(
        "kwargs.py",
        "def show_profile(**fields):\n"
        "    for key, value in fields.items():\n"
        '        print(f"{key}: {value}")\n\n'
        "show_profile(\n"
        '    name="Anna",\n'
        '    city="Warsaw",\n'
        ")\n",
    )}
    {namespace_diagram([("fields", '{"name": "Anna", "city": "Warsaw"}')], caption="Внутри функции fields — обычный словарь (глава 11)")}
    {callout(
        "info",
        "** собирает лишние именованные аргументы в словарь",
        "Любые именованные аргументы, для которых нет отдельного параметра, попадают в словарь "
        "<code class=\"inline\">fields</code> — ключ - имя аргумента, значение - переданное "
        "значение.",
    )}

    <h2>*args vs **kwargs</h2>
    {code_block("vyzov_s_oboimi.py", 'func(10, 20, color="red", size=3)\n')}
    {comparison_table(
        ["", "*args", "**kwargs"],
        [
            ["Собирает", "лишние позиционные аргументы", "лишние именованные аргументы"],
            ["Тип внутри функции", "<code class=\"inline\">tuple</code>", "<code class=\"inline\">dict</code>"],
            ["В примере выше", "<code class=\"inline\">(10, 20)</code>", "<code class=\"inline\">{'color': 'red', 'size': 3}</code>"],
        ],
    )}

    <h2>Распаковка аргументов на месте вызова</h2>
    <p>Тот же символ <code class="inline">*</code>/<code class="inline">**</code>, но теперь на
    стороне ВЫЗОВА, а не определения — связываем с распаковкой из главы 11:</p>
    {code_block("raspakovka_pri_vyzove.py", "point = (10, 20)\nmove(*point)   # эквивалентно move(10, 20)\n")}
    {flow_diagram([("(10, 20)", "кортеж"), ("*", "распаковка"), ("move(10, 20)", "два аргумента")], caption="* перед аргументом при вызове раскладывает кортеж/список на отдельные позиционные аргументы")}
    {code_block(
        "raspakovka_slovarya.py",
        "options = {\n"
        '    "color": "red",\n'
        '    "size": 3,\n'
        "}\n"
        "draw(**options)   # эквивалентно draw(color=\"red\", size=3)\n",
    )}

    <h2>* и ** встречаются в нескольких разных контекстах</h2>
    {comparison_table(
        ["Контекст", "Пример", "Что делает"],
        [
            ["Определение функции", "<code class=\"inline\">def f(*args, **kwargs):</code>", "собирает лишние аргументы"],
            ["Вызов функции", "<code class=\"inline\">f(*values, **mapping)</code>", "распаковывает коллекцию в аргументы"],
            ["Литерал коллекции (глава 11)", "<code class=\"inline\">[*a, *b]</code>", "объединяет коллекции"],
        ],
    )}
    {callout(
        "info",
        "Один символ, разный смысл в зависимости от контекста",
        "<code class=\"inline\">*</code> и <code class=\"inline\">**</code> не означают везде "
        "буквально одну и ту же операцию — их роль зависит от того, где они стоят: в "
        "определении функции, в вызове или в литерале коллекции.",
    )}

    {practice_card(
        "13-13",
        "Практика: *args, **kwargs и распаковка при вызове",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-13/index.html",
    )}
    """
    page(
        "13-13-args-kwargs-raspakovka.html",
        page_title="*args, **kwargs и распаковка",
        description="Произвольное число позиционных и именованных аргументов, распаковка аргументов на месте вызова через * и **.",
        kicker_suffix="*args и **kwargs",
        h1="*args, **kwargs и распаковка",
        lede="*args собирает лишние позиционные аргументы в кортеж, **kwargs — лишние "
        "именованные в словарь. Те же символы на месте вызова распаковывают коллекцию обратно "
        "в аргументы.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-14 · Positional-only и keyword-only
# ---------------------------------------------------------------------------

def build_14() -> None:
    body = f"""
    <h2>Keyword-only параметры — практично уже сейчас</h2>
    <p>Бывают параметры, которые ХОЧЕТСЯ заставить передавать только по имени — обычно это
    необязательные флаги или настройки, где голая позиция путает читателя:</p>
    {code_block("keyword_only.py", "def draw_rectangle(width, height, *, color=\"blue\", filled=False):\n    ...\n\ndraw_rectangle(100, 50, color=\"red\")   # можно\n")}
    {callout(
        "info",
        "Одинокая * в списке параметров",
        "Всё, что стоит ПОСЛЕ одинокого <code class=\"inline\">*</code> в определении функции, "
        "обязано передаваться по имени при вызове — позиционно эти параметры передать нельзя.",
    )}
    {two_up(
        code_block("bez_keyword_only.py", 'draw_rectangle(100, 50, "red", True)\n# что здесь True? filled? Неочевидно.\n'),
        code_block("s_keyword_only.py", 'draw_rectangle(\n    100,\n    50,\n    color="red",\n    filled=True,\n)\n# сразу понятно, что есть что\n'),
    )}
    <p>Второй вариант читается и понимается значительно быстрее — именно ради этого существуют
    keyword-only параметры.</p>

    <h2>[[icon:experiment]] Чуть глубже — positional-only параметры</h2>
    <p>Реже, но тоже встречается обратная ситуация: параметр, который МОЖНО передавать только
    позиционно, без имени.</p>
    {code_block("positional_only.py", "def function(x, /):\n    ...\n")}
    {callout(
        "info",
        "Одинокая / в списке параметров",
        "Всё, что стоит ДО <code class=\"inline\">/</code>, можно передать только позиционно — "
        "имя параметра нельзя использовать при вызове. Так делают, когда автор функции не "
        "хочет, чтобы имя параметра стало частью «контракта» — его можно будет свободно менять "
        "в будущем, не ломая код, который её вызывает.",
    )}

    <h2>Анатомия полной сигнатуры</h2>
    {code_block(
        "signatura.py",
        "def draw(\n"
        "    x, y, /,\n"
        "    width, height,\n"
        "    *,\n"
        "    color=\"blue\",\n"
        "    filled=False,\n"
        "):\n"
        "    ...\n",
    )}
    {capability_map([
        ("x, y", ["только позиционно", "до /"]),
        ("width, height", ["позиционно ИЛИ по имени", "между / и *"]),
        ("color, filled", ["только по имени", "после *"]),
    ], title="Одна сигнатура, три зоны")}
    {callout(
        "tip",
        "Не обязательно запоминать наизусть с первого раза",
        "Это продвинутая, но ценная грамотность чтения API — она особенно пригодится при "
        "чтении документации сторонних библиотек. Для собственных небольших функций чаще всего "
        "достаточно обычных параметров без <code class=\"inline\">/</code> и одинокой "
        "<code class=\"inline\">*</code> — используйте их осознанно, когда это действительно "
        "улучшает читаемость вызова.",
    )}

    {practice_card(
        "13-14",
        "Практика: keyword-only параметры",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-14/index.html",
    )}
    """
    page(
        "13-14-positional-only-keyword-only.html",
        page_title="Positional-only и keyword-only",
        description="Keyword-only параметры после одинокой *, positional-only параметры до /, полная анатомия сигнатуры функции.",
        kicker_suffix="Positional/keyword-only",
        h1="Positional-only и keyword-only",
        lede="Иногда хочется заставить аргумент передаваться только по имени (или только по "
        "позиции) — сигнатура функции умеет это явно требовать.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-03 · Возвращаем ответ (расширено: implicit None, ранний return, несколько значений)
# ---------------------------------------------------------------------------

def build_03() -> None:
    body = f"""
    <p>До сих пор наши функции только печатали текст. Но часто нужно не вывести результат на
    экран, а <strong>вернуть</strong> его — чтобы использовать дальше в программе.
    Ключевое слово <code class="inline">return</code> делает именно это:</p>
    {code_block(
        "return.py",
        "def summa(a, b):\n"
        "    return a + b\n\n"
        "result = summa(5, 7)\n"
        "print(result)         # 12\n"
        "print(summa(2, 3) * 10)  # результат функции можно использовать сразу — 50\n",
    )}
    {flow_diagram([("10, 20 (аргументы)", ""), ("calculate()", "работа функции"), ("30 (return)", "")], caption="Вход → работа функции → результат уходит обратно в место вызова")}

    {callout(
        "warning",
        "print() внутри функции — это не то же самое, что return",
        "Функция, которая только печатает результат, ничего не <em>возвращает</em> — попытка "
        "сохранить её результат в переменную даст <code class=\"inline\">None</code>:",
    )}
    {code_block(
        "print_vs_return.py",
        "def summa_pechataet(a, b):\n"
        "    print(a + b)   # выводит на экран, но не возвращает\n\n"
        "x = summa_pechataet(5, 7)  # на экране появится 12\n"
        "print(x)                    # но x — это None!\n",
    )}
    {comparison_table(
        ["", "print(...) внутри функции", "return ... внутри функции"],
        [["Результат", "текст на экране", "объект уходит в место вызова"], ["x = f(...)", "x станет None", "x станет вычисленным значением"]],
    )}

    <h2>Неявный None</h2>
    <p>Если функция доходит до конца тела, ни разу не выполнив <code class="inline">return</code>,
    Python сам возвращает <code class="inline">None</code>:</p>
    {code_block(
        "implicit_none.py",
        "def hello():\n"
        '    print("Hello")\n\n'
        "result = hello()\n"
        "print(result)\n",
    )}
    {terminal_transcript(["Hello", "None"], caption="hello() ничего не return-ит — Python сам подставляет None")}
    {callout(
        "info",
        "None — настоящий объект, а не «пустота»",
        "<code class=\"inline\">None</code> — это конкретный объект Python, обозначающий "
        "отсутствие значения в данном контексте (глава 9). Функция без "
        "<code class=\"inline\">return</code> не «ничего не возвращает» в смысле полного "
        "отсутствия результата — она возвращает именно объект <code class=\"inline\">None</code>.",
    )}

    <h2>Голый return</h2>
    <p><code class="inline">return</code> без выражения после него тоже возвращает
    <code class="inline">None</code> — и сразу завершает функцию. Полезно для досрочного
    выхода:</p>
    {code_block("bare_return.py", "def process(value):\n    if value is None:\n        return\n    print(value)\n")}

    <h2>Ранний return</h2>
    {code_block(
        "early_return.py",
        "def classify_age(age):\n"
        "    if age < 0:\n"
        '        return "Некорректный возраст"\n\n'
        "    if age < 18:\n"
        '        return "Несовершеннолетний"\n\n'
        '    return "Совершеннолетний"\n',
    )}
    {flowchart([
        {"kind": "input", "label": "age"},
        {"kind": "decision", "label": "age < 0?", "yes": [{"kind": "end", "label": "return «Некорректный возраст»"}], "no": []},
        {"kind": "decision", "label": "age < 18?", "yes": [{"kind": "end", "label": "return «Несовершеннолетний»"}], "no": []},
        {"kind": "end", "label": "return «Совершеннолетний»"},
    ], caption="Каждый return завершает функцию немедленно — код после него в этом вызове не выполнится")}
    {callout(
        "tip",
        "return сразу завершает функцию",
        "Как только выполняется <code class=\"inline\">return</code>, функция немедленно "
        "заканчивает работу — код после него внутри функции не выполнится.",
    )}

    <h2>Возвращаем несколько значений</h2>
    {code_block("neskolko_znachenij.py", "def min_max(numbers):\n    return min(numbers), max(numbers)\n\nlow, high = min_max([3, 7, 1, 9])\nprint(low, high)   # 1 9\n")}
    {callout(
        "info",
        "На самом деле возвращается один кортеж",
        "<code class=\"inline\">return a, b</code> на уровне Python создаёт и возвращает ОДИН "
        "объект — кортеж <code class=\"inline\">(a, b)</code> (глава 11). Функция не "
        "«возвращает два объекта одновременно» — она возвращает один кортеж, который затем "
        "можно распаковать в две переменные при вызове, точно как любой другой кортеж.",
    )}

    {practice_card(
        "13-03",
        "Практика: return, implicit None, ранний return",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-03/index.html",
    )}
    """
    page(
        "13-03-vozvrashaem-otvet.html",
        page_title="Возвращаем ответ",
        description="return в полной глубине: разница с print(), неявный None, голый return, ранний return, возврат нескольких значений через кортеж.",
        kicker_suffix="Возвращаем ответ",
        h1="Возвращаем ответ",
        lede="return передаёт результат работы функции обратно туда, откуда она была вызвана — "
        "а функция без return всё равно кое-что возвращает: None.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-15 · Вход, работа, выход: чистые функции
# ---------------------------------------------------------------------------

def build_15() -> None:
    body = f"""
    <h2>Универсальная модель функции</h2>
    {flow_diagram([("ПАРАМЕТРЫ", "вход"), ("ФУНКЦИЯ", "алгоритм"), ("RETURN", "выход")], caption="Параметры → тело функции → return — модель, применимая к любой функции с результатом")}
    {comparison_table(
        ["Пример", "Вход", "Выход"],
        [
            ["<code class=\"inline\">convert_temperature</code>", "градусы Цельсия", "градусы Фаренгейта"],
            ["<code class=\"inline\">normalize</code>", "сырой текст", "очищенный текст"],
            ["<code class=\"inline\">calculate_average</code>", "список чисел", "одно число"],
        ],
    )}

    <h2>Два законных вида функций</h2>
    <p>Не каждая функция обязана возвращать значение — у функций есть две законные роли:</p>
    {comparison_table(
        ["Функция-команда / эффект", "Функция-вычисление"],
        [["<code class=\"inline\">show_menu()</code>, <code class=\"inline\">draw_square()</code>, <code class=\"inline\">print_report()</code>", "<code class=\"inline\">area(...)</code>, <code class=\"inline\">normalize(...)</code>, <code class=\"inline\">average(...)</code>"], ["главная цель — эффект (вывод, рисование)", "главная цель — вернуть значение"]],
    )}
    {callout(
        "info",
        "Оба вида — легитимны",
        "Не каждая функция обязана что-то возвращать осмысленное — <code class=\"inline\">"
        "draw_square()</code> вполне нормальна, даже если она ничего не return-ит: её работа "
        "— эффект на экране, а не значение.",
    )}

    <h2>Побочный эффект</h2>
    <p><strong>Побочный эффект</strong> — это когда функция меняет что-то ВНЕ своего
    возвращаемого результата: печатает на экран, рисует Turtle, мутирует переданный список,
    позже — пишет в файл.</p>
    {code_block("storonnij_effekt.py", 'def add_item(items):\n    items.append("Python")   # побочный эффект: мутирует переданный список\n')}

    <h2>Чистые функции</h2>
    <p><strong>Чистая функция</strong> — результат зависит только от аргументов, и функция
    намеренно ничего не меняет вне себя:</p>
    {code_block("chistaya_funkciya.py", "def rectangle_area(width, height):\n    return width * height\n")}
    {two_up(
        flow_diagram([("ВХОД", ""), ("ФУНКЦИЯ", ""), ("ВЫХОД", "")], caption="Чистая функция: только вход → результат"),
        flow_diagram([("ВХОД", ""), ("ФУНКЦИЯ", ""), ("выход / эффект", "экран, Turtle, мутация...")], caption="Функция с побочным эффектом: результат ИЛИ/И эффект вовне"),
    )}
    {capability_map([
        ("Легче понимать", ["результат зависит только от входа"]),
        ("Легче тестировать", ["не нужен экран/файл/сеть — просто вызов"]),
        ("Предсказуемость", ["один и тот же вход → всегда один и тот же выход"]),
    ], title="Почему чистые функции удобны")}
    {callout(
        "warning",
        "Не каждая функция ДОЛЖНА быть чистой",
        "Графика, ввод/вывод, работа с интерфейсом — всё это по своей природе требует побочных "
        "эффектов. Чистота — полезное свойство там, где оно естественно, а не универсальное "
        "правило, которому обязана подчиняться каждая функция программы.",
    )}

    {practice_card(
        "13-15",
        "Практика: чистые функции vs функции с побочным эффектом",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-15/index.html",
    )}
    """
    page(
        "13-15-funkcii-vhod-vyhod.html",
        page_title="Вход, работа, выход: чистые функции",
        description="Универсальная модель функции (параметры → алгоритм → return), функции-команды vs функции-вычисления, побочные эффекты, чистые функции.",
        kicker_suffix="Чистые функции",
        h1="Вход, работа, выход: чистые функции",
        lede="Не каждая функция обязана что-то возвращать — но полезно чётко понимать, ради "
        "чего написана каждая конкретная функция: ради результата или ради эффекта.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-05 · Глобальные и локальные переменные (перестроено: LEGB, shadowing, UnboundLocalError)
# ---------------------------------------------------------------------------

def build_05() -> None:
    body = f"""
    <h2>Переменные внутри функций</h2>
    <p>Переменная, созданная внутри функции, называется <strong>локальной</strong> — она
    существует только пока функция выполняется и недоступна снаружи:</p>
    {code_block(
        "lokalnye_peremennye.py",
        "def moya_funkciya():\n"
        '    message = "Я живу только внутри функции"\n'
        "    print(message)\n\n"
        "moya_funkciya()\n"
        "print(message)   # NameError: message не определена здесь\n",
    )}

    <h2>Глобальные переменные</h2>
    <p><strong>Глобальная</strong> переменная объявлена вне всех функций — и доступна для чтения
    внутри любой из них:</p>
    {code_block(
        "globalnye_peremennye.py",
        'course_name = "Python"\n\n'
        "def lesson():\n"
        '    topic = "Функции"\n'
        "    print(course_name)   # чтение глобальной — работает без всяких оговорок\n"
        "    print(topic)\n\n"
        "lesson()\n",
    )}
    {two_up(
        namespace_diagram([("course_name", '"Python"'), ("lesson", "ФУНКЦИЯ-ОБЪЕКТ")], caption="Глобальное пространство имён"),
        namespace_diagram([("topic", '"Функции"')], caption="Локальное пространство имён lesson() во время вызова"),
    )}
    {callout(
        "info",
        "Функция может смотреть наружу, но не наоборот",
        "Функция может ЧИТАТЬ глобальные имена, но переменные, созданные внутри неё, не "
        "становятся автоматически видны снаружи.",
    )}

    <h2>Затенение (shadowing)</h2>
    {code_block(
        "shadowing.py",
        'name = "GLOBAL"\n\n'
        "def demo():\n"
        '    name = "LOCAL"\n'
        "    print(name)\n\n"
        "demo()\n"
        "print(name)\n",
    )}
    {terminal_transcript(["LOCAL", "GLOBAL"], caption="Локальное имя name существует только внутри demo() и не трогает глобальное")}
    {callout(
        "tip",
        "Локальное имя затеняет глобальное с тем же именем",
        "Внутри <code class=\"inline\">demo()</code> создаётся СВОЁ, отдельное локальное имя "
        "<code class=\"inline\">name</code> — оно временно «заслоняет» глобальное "
        "<code class=\"inline\">name</code> для кода внутри функции, но не заменяет и не "
        "удаляет его.",
    )}

    <h2>LEGB: как Python ищет имя</h2>
    <p>Когда Python встречает имя, он ищет его по чёткому порядку — эту модель называют
    <strong>LEGB</strong>:</p>
    {elif_ladder_diagram(
        [
            ("L — Local?", "нашли → используем"),
            ("E — Enclosing?", "нашли → используем"),
            ("G — Global?", "нашли → используем"),
            ("B — Builtins?", "нашли → используем"),
        ],
        else_label="NameError",
        caption="Local → Enclosing → Global → Builtins — поиск останавливается на первом совпадении",
    )}
    {comparison_table(
        ["Буква", "Что это", "Пример"],
        [
            ["L — Local", "имена внутри текущей функции", "<code class=\"inline\">topic</code> внутри <code class=\"inline\">lesson()</code>"],
            ["E — Enclosing", "имена внешней функции для вложенной (§13.13)", "рассмотрим дальше"],
            ["G — Global", "имена на уровне модуля", "<code class=\"inline\">course_name</code>"],
            ["B — Builtins", "встроенные имена Python", "<code class=\"inline\">len</code>, <code class=\"inline\">print</code>"],
        ],
    )}

    <h2>UnboundLocalError — почему это НЕ случайность</h2>
    {code_block(
        "unbound_local.py",
        "count = 10\n\n"
        "def increment():\n"
        "    count += 1\n\n"
        "increment()\n",
    )}
    {callout(
        "warning",
        "Присваивание где-либо в теле делает имя локальным ВО ВСЁМ теле функции",
        "Python видит <code class=\"inline\">count += 1</code> (это "
        "<code class=\"inline\">count = count + 1</code>) и заранее решает: раз "
        "<code class=\"inline\">count</code> присваивается внутри функции, значит, это "
        "ЛОКАЛЬНОЕ имя — на протяжении ВСЕГО тела функции, а не только после присваивания. Но "
        "правая часть <code class=\"inline\">count + 1</code> пытается ПРОЧИТАТЬ "
        "<code class=\"inline\">count</code> ДО того, как локальное значение вообще появилось "
        "— отсюда <code class=\"inline\">UnboundLocalError</code>. Это не случайное поведение, "
        "а прямое следствие того, как Python заранее размечает локальные имена функции.",
    )}

    <h2>global — если действительно нужно изменить глобальную переменную</h2>
    {code_block(
        "global_keyword.py",
        "count = 10\n\n"
        "def increment():\n"
        "    global count\n"
        "    count += 1\n\n"
        "increment()\n"
        "print(count)   # 11\n",
    )}
    {callout(
        "warning",
        "global нужен только для присваивания, не для чтения",
        "Просто ПРОЧИТАТЬ глобальную переменную можно без <code class=\"inline\">global</code> "
        "(мы это уже делали с <code class=\"inline\">course_name</code> выше). "
        "<code class=\"inline\">global</code> нужен, только когда функция собирается "
        "ИЗМЕНИТЬ (присвоить) глобальное имя.",
    )}
    {callout(
        "info",
        "global работает, но чаще есть способ лучше",
        "<code class=\"inline\">global</code> — не запрещённая, но зачастую не лучшая "
        "практика: функции, которые читают параметры и возвращают результат через "
        "<code class=\"inline\">return</code>, легче тестировать и переиспользовать, потому "
        "что их поведение не зависит от скрытого внешнего состояния. Это не абсолютное "
        "правило «глобальные переменные — всегда плохо» — иногда общее состояние действительно "
        "уместно, — но по умолчанию стоит предпочитать параметры и return.",
    )}

    {practice_card(
        "13-05",
        "Практика: локальные, глобальные переменные и LEGB",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-05/index.html",
    )}
    """
    page(
        "13-05-globalnye-lokalnye.html",
        page_title="Глобальные и локальные переменные",
        description="LEGB — как Python ищет имя (Local → Enclosing → Global → Builtins), затенение, UnboundLocalError и ключевое слово global.",
        kicker_suffix="Область видимости",
        h1="Глобальные и локальные переменные",
        lede="Где «живёт» переменная и в каком порядке Python её ищет — модель LEGB избавит "
        "от многих загадочных ошибок.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-16 · Вложенные функции и nonlocal
# ---------------------------------------------------------------------------

def build_16() -> None:
    body = f"""
    <h2>Функция внутри функции</h2>
    <p>Функцию можно определить прямо внутри тела другой функции:</p>
    {code_block(
        "vlozhennaya_funkciya.py",
        "def outer():\n"
        '    message = "Hello"\n\n'
        "    def inner():\n"
        "        print(message)\n\n"
        "    inner()\n\n"
        "outer()\n",
    )}
    {callout(
        "info",
        "inner видит message — это и есть Enclosing из LEGB",
        "<code class=\"inline\">inner()</code> не имеет своего <code class=\"inline\">message</code>, "
        "но находит его в объемлющей функции <code class=\"inline\">outer()</code> — это буква "
        "«E» (Enclosing) из ладдера LEGB (§13.12).",
    )}
    {callout(
        "warning",
        "Отступ — это не украшение, а объявление вложенности",
        "Если случайно сдвинуть <code class=\"inline\">def inner():</code> на уровень отступа "
        "меньше, чем нужно, она перестанет быть вложенной в <code class=\"inline\">outer</code> "
        "— и наоборот. Отступ буквально определяет, какая функция находится «внутри» какой.",
    )}

    <h2>nonlocal</h2>
    <p>Как и с глобальными переменными, ПРОЧИТАТЬ имя из объемлющей функции можно свободно, а
    вот ИЗМЕНИТЬ (присвоить) — нужно явно попросить:</p>
    {code_block(
        "nonlocal.py",
        "def outer():\n"
        "    count = 0\n\n"
        "    def inner():\n"
        "        nonlocal count\n"
        "        count += 1\n\n"
        "    inner()\n"
        "    inner()\n"
        "    print(count)\n\n"
        "outer()\n",
    )}
    {terminal_transcript(["2"], caption="nonlocal позволил inner() изменить count из outer(), а не создать свою локальную копию")}
    {callout(
        "info",
        "nonlocal — это НЕ global",
        "<code class=\"inline\">nonlocal</code> ищет имя в БЛИЖАЙШЕЙ подходящей объемлющей "
        "функции — не на уровне модуля. Если убрать <code class=\"inline\">nonlocal count</code>, "
        "получится та же ошибка <code class=\"inline\">UnboundLocalError</code>, что и в §13.12 "
        "— по той же самой причине: присваивание внутри <code class=\"inline\">inner</code> "
        "сделало бы <code class=\"inline\">count</code> локальным именем самой "
        "<code class=\"inline\">inner</code>.",
    )}

    <h2>[[icon:launch]] Чуть глубже — замыкание (closure)</h2>
    <p>Вложенная функция способна «запомнить» значения из объемлющей функции даже после того,
    как внешний вызов уже завершился:</p>
    {code_block(
        "closure.py",
        "def make_greeter(name):\n"
        "    def greet():\n"
        '        print(f"Привет, {name}!")\n'
        "    return greet\n\n"
        'greet_anna = make_greeter("Anna")\n'
        "greet_anna()   # Привет, Anna! — хотя make_greeter уже закончила работу\n",
    )}
    {callout(
        "info",
        "Замыкание — тема на будущее",
        "Это называется <strong>замыканием</strong> — <code class=\"inline\">greet</code> "
        "«уносит с собой» доступ к <code class=\"inline\">name</code>. Здесь достаточно "
        "увидеть, что так вообще бывает — подробный разбор замыканий и их практических "
        "применений (декораторы и не только) не входит в эту главу.",
    )}

    {practice_card(
        "13-16",
        "Практика: вложенные функции и nonlocal",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-16/index.html",
    )}
    """
    page(
        "13-16-vlozhennye-funkcii-nonlocal.html",
        page_title="Вложенные функции и nonlocal",
        description="Функция внутри функции, Enclosing из LEGB, ключевое слово nonlocal, беглое знакомство с замыканиями.",
        kicker_suffix="Вложенные функции",
        h1="Вложенные функции и nonlocal",
        lede="Функция может быть определена прямо внутри другой функции — а nonlocal позволяет "
        "ей изменить имя из объемлющей функции, а не только прочитать его.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-17 · Стек вызовов и traceback
# ---------------------------------------------------------------------------

def build_17() -> None:
    body = f"""
    <h2>Кадр вызова (call frame)</h2>
    <p>Когда функция вызывается, Python создаёт временный «контейнер» для этого конкретного
    вызова — с параметрами, локальными именами и отметкой, куда вернуться после завершения:</p>
    {code_block("call_frame.py", "def area(width, height):\n    return width * height\n\narea(5, 3)\n")}
    {namespace_diagram([("width", "5"), ("height", "3")], caption="Кадр вызова area(5, 3): параметры существуют, пока этот конкретный вызов не завершится")}

    <h2>Функции могут вызывать другие функции</h2>
    {code_block(
        "vlozhennye_vyzovy.py",
        "def calculate_tax(amount):\n"
        "    return amount * 0.2\n\n"
        "def calculate_invoice(amount):\n"
        "    tax = calculate_tax(amount)\n"
        "    return amount + tax\n\n"
        "calculate_invoice(100)\n",
    )}
    <p>Пока <code class="inline">calculate_tax()</code> выполняется, вызов
    <code class="inline">calculate_invoice()</code> не заканчивается — он «ждёт» на паузе.
    Python отслеживает все ожидающие вызовы в структуре, которую называют
    <strong>стеком вызовов</strong>.</p>

    <h2>Стек растёт и уменьшается</h2>
    {two_up(
        call_stack_diagram(["main"], caption="Шаг 1 — выполняется основная программа"),
        call_stack_diagram(["main", "calculate_invoice()"], caption="Шаг 2 — main вызвала calculate_invoice()"),
    )}
    {two_up(
        call_stack_diagram(["main", "calculate_invoice()", "calculate_tax()"], caption="Шаг 3 — calculate_invoice вызвала calculate_tax(); стек на пике"),
        call_stack_diagram(["main", "calculate_invoice()"], caption="Шаг 4 — calculate_tax() вернула результат и исчезла со стека"),
    )}
    {callout(
        "tip",
        "Последним вошёл — первым вышел",
        "Стек вызовов растёт с каждым новым вызовом и уменьшается с каждым завершением — самый "
        "недавний вызов всегда наверху и завершается первым. Это называют принципом LIFO "
        "(Last In, First Out).",
    )}

    <h2>Traceback — это и есть снимок стека вызовов</h2>
    <p>Вспомним отладку из главы 3: когда возникает ошибка, Python печатает traceback — и это
    буквально показывает цепочку вызовов, которая привела к ошибке:</p>
    {code_block(
        "traceback_primer.py",
        "def divide(a, b):\n"
        "    return a / b\n\n"
        "def calculate():\n"
        "    return divide(10, 0)\n\n"
        "def main():\n"
        "    calculate()\n\n"
        "main()\n",
    )}
    {terminal_transcript([
        "Traceback (most recent call last):",
        '  File "example.py", line 8, in &lt;module&gt;',
        "    main()",
        '  File "example.py", line 6, in main',
        "    calculate()",
        '  File "example.py", line 4, in calculate',
        "    return divide(10, 0)",
        '  File "example.py", line 2, in divide',
        "    return a / b",
        "ZeroDivisionError: division by zero",
    ], caption="Каждая строка traceback — это один кадр из стека вызовов на момент ошибки")}
    {callout(
        "info",
        "Читаем traceback снизу вверх",
        "Самая нижняя строка — сама ошибка. Строка над ней — где именно она произошла "
        "(<code class=\"inline\">divide</code>). Выше — кто её вызвал "
        "(<code class=\"inline\">calculate</code>), и ещё выше — кто вызвал того "
        "(<code class=\"inline\">main</code>). Traceback — это ровно тот стек вызовов, который "
        "мы только что визуализировали, показанный в момент, когда что-то пошло не так.",
    )}

    {practice_card(
        "13-17",
        "Практика: читаем стек вызовов и traceback",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-17/index.html",
    )}
    """
    page(
        "13-17-stek-vyzovov.html",
        page_title="Стек вызовов и traceback",
        description="Кадр вызова, вложенные вызовы функций, рост и уменьшение стека вызовов (LIFO), и как traceback показывает этот же стек в момент ошибки.",
        kicker_suffix="Стек вызовов",
        h1="Стек вызовов и traceback",
        lede="Функции, вызывающие функции, образуют стек ожидающих вызовов — и traceback из "
        "главы 3 на самом деле показывает именно этот стек в момент ошибки.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-18 · Проектируем хорошую функцию
# ---------------------------------------------------------------------------

def build_18() -> None:
    body = f"""
    <h2>Хорошие имена — глаголы-действия</h2>
    {comparison_table(
        ["Хорошо", "Плохо"],
        [
            ["<code class=\"inline\">calculate_total()</code>", "<code class=\"inline\">do_it()</code>"],
            ["<code class=\"inline\">normalize_text()</code>", "<code class=\"inline\">func1()</code>"],
            ["<code class=\"inline\">draw_polygon()</code>", "<code class=\"inline\">thing()</code>"],
            ["<code class=\"inline\">find_max_score()</code>", "<code class=\"inline\">test2()</code>"],
        ],
    )}
    <p>Функции обычно представляют ДЕЙСТВИЕ — имя должно быть глаголом или глагольной фразой.
    Для функций, возвращающих <code class="inline">True</code>/<code class="inline">False</code>,
    хорошо работают префиксы <code class="inline">is_</code>, <code class="inline">has_</code>,
    <code class="inline">can_</code>, <code class="inline">contains_</code> — они прямо
    сообщают, что вернётся булево значение.</p>

    <h2>Одна функция — одна понятная обязанность</h2>
    {code_block(
        "plohaya_dekompoziciya.py",
        "def process_everything():\n"
        "    # спрашивает ввод\n"
        "    # проверяет\n"
        "    # считает\n"
        "    # печатает\n"
        "    # рисует\n"
        "    # обновляет пять структур данных\n"
        "    ...\n",
    )}
    {code_block(
        "horoshaya_dekompoziciya.py",
        "def read_answer(): ...\n"
        "def normalize_answer(answer): ...\n"
        "def check_answer(answer, correct): ...\n"
        "def show_result(correct): ...\n",
    )}
    {callout(
        "info",
        "Это ориентир, а не догма",
        "Небольшие программы вполне могут разумно объединять несколько простых действий в одной "
        "функции — не нужно дробить каждую строку в отдельную функцию искусственно (пример "
        "того, ЧЕГО не стоит делать, — в §13.19). Цель — ясность, а не количество функций.",
    )}

    <h2>Сколько строк должна занимать функция?</h2>
    <p>Не существует правила вида «максимум 10 строк». Вместо количества строк спрашивайте:</p>
    {capability_map([
        ("1", ["Есть ли у неё одна ясная цель?"]),
        ("2", ["Объясняет ли имя, что она делает?"]),
        ("3", ["Легко ли её протестировать отдельно?"]),
        ("4", ["Есть ли внутри сильно повторяющаяся логика?"]),
        ("5", ["Понятны ли входы и выход читателю?"]),
    ], title="Вопросы вместо количества строк")}

    <h2>Контракт функции</h2>
    <p>Прежде чем писать реализацию, полезно явно сформулировать контракт — что функция
    принимает, что возвращает, и есть ли у неё побочные эффекты:</p>
    {comparison_table(
        ["Часть контракта", "calculate_discount(price, percent)"],
        [
            ["Вход", "price: число, percent: число"],
            ["Выход", "цена со скидкой"],
            ["Побочные эффекты", "нет"],
            ["Пример", "<code class=\"inline\">calculate_discount(100, 10) → 90</code>"],
        ],
    )}

    <h2>Предусловия</h2>
    <p>Некоторые функции ожидают осмысленный вход — например, <code class="inline">draw_polygon(sides,
    length)</code> предполагает <code class="inline">sides >= 3</code> и
    <code class="inline">length > 0</code>. Это <strong>предусловия</strong> — требования к
    входным данным, которые стоит проверить обычными условиями:</p>
    {code_block(
        "predusloviya.py",
        "def polygon_angle(sides):\n"
        "    if sides < 3:\n"
        "        return None\n\n"
        "    return 360 / sides\n",
    )}
    {callout(
        "info",
        "None — не единственный вариант",
        "Возврат <code class=\"inline\">None</code> при неверном входе — простой и рабочий "
        "вариант на этом уровне курса. Более строгие способы (например, поднять исключение) "
        "рассматриваются в главах, посвящённых обработке ошибок.",
    )}

    <h2>Чек-лист проектирования функции</h2>
    {summary_box("Прежде чем написать def", [
        "Какую ОДНУ работу она выполняет?",
        "Какие данные ей нужны? Это и есть параметры.",
        "Возвращает ли она результат — и какой?",
        "Меняет ли она что-то намеренно (побочный эффект)?",
        "Как её назвать, чтобы имя объясняло действие?",
        "На каких входных данных её стоит проверить?",
    ])}

    {practice_card(
        "13-18",
        "Практика: проектируем функцию по контракту",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-18/index.html",
    )}
    """
    page(
        "13-18-proektiruem-funkciyu.html",
        page_title="Проектируем хорошую функцию",
        description="Хорошие имена функций, единственная обязанность, контракт функции (вход/выход/побочные эффекты), предусловия, чек-лист проектирования.",
        kicker_suffix="Проектируем функцию",
        h1="Проектируем хорошую функцию",
        lede="Прежде чем писать реализацию, полезно спроектировать функцию: одна ясная "
        "обязанность, понятное имя, чёткий контракт.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-19 · Докстринги и подсказки типов
# ---------------------------------------------------------------------------

def build_19() -> None:
    body = f"""
    <h2>Докстринг — документация функции</h2>
    {code_block(
        "docstring.py",
        "def rectangle_area(width, height):\n"
        '    """Возвращает площадь прямоугольника."""\n'
        "    return width * height\n",
    )}
    {comparison_table(
        ["", "Комментарий (# ...)", "Докстринг (\"\"\"...\"\"\")"],
        [["Объясняет", "почему код написан именно так", "что делает функция — как API"], ["Виден снаружи?", "нет, только в исходнике", "да, через help() и __doc__"]],
    )}

    <h2>help() показывает докстринг во время работы программы</h2>
    {code_block("help_primer.py", "help(rectangle_area)\nprint(rectangle_area.__doc__)\n")}
    {terminal_transcript([
        "Help on function rectangle_area in module __main__:",
        "",
        "rectangle_area(width, height)",
        "    Возвращает площадь прямоугольника.",
    ], caption="help() достаёт докстринг прямо из объекта функции — та же идея, что мы уже видели у встроенных функций")}

    <h2>Type hints — подсказки типов</h2>
    {code_block("type_hints.py", "def rectangle_area(width: float, height: float) -> float:\n    return width * height\n")}
    {comparison_table(
        ["Часть", "Значение"],
        [["<code class=\"inline\">width: float</code>", "ожидаемый тип параметра"], ["<code class=\"inline\">-> float</code>", "ожидаемый тип возвращаемого значения"]],
    )}
    {callout(
        "warning",
        "Подсказки типов не проверяются автоматически во время выполнения",
        "<code class=\"inline\">def add(a: int, b: int) -> int:</code> НЕ помешает вызвать "
        "<code class=\"inline\">add(\"2\", \"3\")</code> — Python не станет автоматически "
        "приводить строки к числам и не выбросит ошибку сам по себе. Аннотации типов — это "
        "документация и подсказка для инструментов разработки, а не runtime-проверка.",
    )}

    <h2>Аннотации коллекций</h2>
    {code_block(
        "annotacii_kollekcij.py",
        "def average(scores: list[float]) -> float:\n"
        "    return sum(scores) / len(scores)\n\n"
        "def count_words(text: str) -> dict[str, int]:\n"
        "    ...\n",
    )}

    <h2>Необязательное значение в аннотации</h2>
    {code_block("optional_annotation.py", "def find_user(name: str) -> str | None:\n    ...\n")}
    {callout(
        "info",
        "str | None читается как «строка или None»",
        "Такая аннотация говорит: функция либо вернёт строку, либо "
        "<code class=\"inline\">None</code>, если ничего не найдено. Это не отдельная "
        "тема — просто способ явно описать словами то, что мы уже видели на практике "
        "(например, у <code class=\"inline\">dict.get()</code>).",
    )}

    <h2>Аннотации не отменяют ловушку изменяемого умолчания</h2>
    {code_block("annotacii_ne_spasayut.py", "def add(item: str, items: list[str] = []):\n    ...\n    # всё ещё та же ловушка из §13.7!\n")}
    {callout(
        "warning",
        "Аннотации типов — это документация, а не защита от ошибок времени выполнения",
        "Даже с полными аннотациями <code class=\"inline\">items: list[str] = []</code> "
        "остаётся тем же изменяемым значением по умолчанию, что и раньше — аннотация ничего не "
        "меняет в реальном поведении функции.",
    )}

    {practice_card(
        "13-19",
        "Практика: докстринги и подсказки типов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-19/index.html",
    )}
    """
    page(
        "13-19-dokumentaciya-i-tipy.html",
        page_title="Докстринги и подсказки типов",
        description="Докстринги, help(), подсказки типов (type hints) — что они дают и чего НЕ делают: не проверяют типы во время выполнения и не отменяют ловушку изменяемого умолчания.",
        kicker_suffix="Докстринги и типы",
        h1="Докстринги и подсказки типов",
        lede="Профессиональная привычка, которую стоит выработать рано: документировать "
        "функцию так, чтобы её можно было понять, не читая реализацию.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-20 · Функции как объекты
# ---------------------------------------------------------------------------

def build_20() -> None:
    body = f"""
    <h2>Функцию можно сохранить под другим именем</h2>
    <p>Вернёмся к различию из §13.2 — <code class="inline">greet</code> и
    <code class="inline">greet()</code> — и пойдём на шаг дальше:</p>
    {code_block(
        "funkciya_kak_obekt.py",
        "def greet(name):\n"
        '    return f"Привет, {name}"\n\n'
        "action = greet\n\n"
        'print(action("Anna"))   # Привет, Anna\n',
    )}
    {converge_diagram(["greet", "action"], "ФУНКЦИЯ-ОБЪЕКТ", caption="greet и action — два имени одного и того же объекта функции, точно как с любым другим объектом (глава 3)")}
    {callout(
        "info",
        "Это то же самое aliasing, что и всегда",
        "<code class=\"inline\">action = greet</code> не копирует функцию и не создаёт вторую "
        "— оба имени указывают на один и тот же объект функции. Функции в Python — это "
        "<strong>объекты первого класса</strong>: их можно сохранять в переменных, класть в "
        "коллекции, передавать в другие функции — как любые другие значения.",
    )}

    <h2>Функции в коллекциях</h2>
    {code_block(
        "funkcii_v_slovare.py",
        "def double(x):\n"
        "    return x * 2\n\n"
        "def square(x):\n"
        "    return x ** 2\n\n"
        "operations = {\n"
        '    "double": double,\n'
        '    "square": square,\n'
        "}\n\n"
        'operation = operations["square"]\n'
        "result = operation(5)\n"
        "print(result)   # 25\n",
    )}
    {callout(
        "tip",
        "Словарь функций + глава 11",
        "<code class=\"inline\">operations</code> — обычный словарь (глава 11), просто "
        "хранящий не числа и не строки, а объекты функций.",
    )}

    <h2>Передача функции как аргумента</h2>
    <p>Вы уже это делали, даже не задумываясь:</p>
    {code_block("sorted_key.py", 'words = ["python", "я", "программирование"]\nprint(sorted(words, key=len))\n')}
    {flow_diagram([("слово", ""), ("len(слово)", "ключ сортировки"), ("порядок", "по этому ключу")], caption="sorted() вызывает переданную функцию len для каждого элемента, чтобы получить ключ сортировки")}
    {callout(
        "info",
        "len — это ФУНКЦИЯ-ОБЪЕКТ, а не результат её вызова",
        "<code class=\"inline\">key=len</code> передаёт саму функцию <code class=\"inline\">len</code> "
        "— БЕЗ скобок. <code class=\"inline\">sorted()</code> сама вызовет "
        "<code class=\"inline\">len(...)</code> для каждого элемента, когда придёт время "
        "сравнивать. Если написать <code class=\"inline\">key=len()</code> — это была бы "
        "попытка вызвать <code class=\"inline\">len</code> прямо сейчас, без аргумента, что "
        "приведёт к ошибке.",
    )}

    <h2>[[icon:experiment]] Термин: функция высшего порядка</h2>
    <p>Функция, которая принимает другую функцию как аргумент (как <code class="inline">sorted()</code>)
    или возвращает функцию (как <code class="inline">make_greeter()</code> из §13.13), называется
    <strong>функцией высшего порядка</strong>. Специальная теория функционального
    программирования здесь не нужна — достаточно узнавать этот паттерн, когда он встречается.</p>

    {practice_card(
        "13-20",
        "Практика: функции как объекты первого класса",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-20/index.html",
    )}
    """
    page(
        "13-20-funkcii-kak-obekty.html",
        page_title="Функции как объекты",
        description="Функции — объекты первого класса: их можно сохранять под другим именем, класть в коллекции, передавать другим функциям. sorted(key=len) как пример.",
        kicker_suffix="Функции как объекты",
        h1="Функции как объекты",
        lede="Функция — такой же объект, как список или строка: её можно сохранить под другим "
        "именем, положить в словарь, передать другой функции.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-06 · Лямбда-функции (расширено и переосмыслено)
# ---------------------------------------------------------------------------

def build_06() -> None:
    body = f"""
    <p>В §13.20 мы передавали <code class="inline">len</code> как аргумент в
    <code class="inline">sorted()</code>. А что, если нужное правило сортировки не существует
    как готовая функция — и заводить ради него отдельный <code class="inline">def</code>
    кажется излишним? Для этого существует <strong>lambda</strong>.</p>

    <h2>lambda создаёт маленький безымянный объект функции</h2>
    {code_block("lambda_sortirovka.py", 'students = [{"name": "Anna", "score": 82}, {"name": "Bob", "score": 95}]\nstudents.sort(key=lambda student: student["score"])\n')}
    {callout(
        "info",
        "Не «более короткий def», а инструмент для конкретной ситуации",
        "Главная задача lambda — передать маленькое правило/преобразование туда, где полноценная "
        "именованная функция была бы избыточной. Это НЕ более современная замена "
        "<code class=\"inline\">def</code> — это отдельный инструмент для узкого случая.",
    )}

    <h2>Анатомия lambda</h2>
    {code_block("lambda_anatomiya.py", "lambda x: x ** 2\n")}
    {comparison_table(
        ["Часть", "Значение"],
        [
            ["<code class=\"inline\">lambda</code>", "ключевое слово — создать функцию-выражение"],
            ["<code class=\"inline\">x</code>", "параметр (без скобок)"],
            ["<code class=\"inline\">x ** 2</code>", "единственное выражение — его результат возвращается автоматически"],
        ],
    )}
    {code_block("lambda_vyzov.py", "kvadrat = lambda x: x ** 2\nprint(kvadrat(5))   # 25\n")}
    <p>Никакого явного <code class="inline">return</code> и никаких блочных инструкций внутри —
    только одно выражение.</p>

    <h2>Ограничения lambda</h2>
    {capability_map([
        ("Только выражение", ["ни одной инструкции", "ни присваивания, ни print"]),
        ("Не для сложной логики", ["ветвление с эффектами", "длинные вычисления"]),
        ("Без имени и докстринга", ["нечего показать в traceback", "нечего документировать"]),
    ], title="Когда lambda НЕ подходит — берите def")}
    {callout(
        "tip",
        "Если логика заслуживает имени — используйте def",
        "Как только правило становится достаточно важным, чтобы его стоило переиспользовать, "
        "протестировать отдельно или объяснить докстрингом — самое время превратить lambda в "
        "обычную функцию с <code class=\"inline\">def</code>.",
    )}

    <h2>def → lambda: сравнение стиля, а не «улучшение»</h2>
    {classic_vs_modern(
        "Простая функция: def → lambda",
        "Обычная функция (def)",
        "def kvadrat(x):\n"
        "    return x ** 2\n\n"
        "print(kvadrat(5))",
        "Лямбда-функция",
        "kvadrat = lambda x: x ** 2\n\n"
        "print(kvadrat(5))",
        "обычную функцию с <code class=\"inline\">def</code> — она читается яснее, у неё есть "
        "нормальное имя для отладки, и в неё легко добавить несколько строк логики или "
        "комментарий. <code class=\"inline\">lambda</code> удобна только для одной короткой "
        "строки без имени — например, как аргумент функции <code class=\"inline\">sorted()</code> "
        "или <code class=\"inline\">max()</code>. Присваивание lambda имени "
        "(<code class=\"inline\">kvadrat = lambda x: ...</code>) не более «современно», чем "
        "<code class=\"inline\">def</code> — во многих реальных проектах такой стиль сочли бы "
        "менее читаемым, а не прогрессивным.",
    )}

    <h2>[[icon:experiment]] Необязательно: map() и filter()</h2>
    <p>Раз вы уже знаете comprehensions (глава 11), полезно увидеть их альтернативу:</p>
    {two_up(
        code_block("map_primer.py", "numbers = [1, 2, 3, 4]\nkvadraty = list(map(lambda n: n ** 2, numbers))\nprint(kvadraty)\n"),
        code_block("comprehension_ekvivalent.py", "numbers = [1, 2, 3, 4]\nkvadraty = [n ** 2 for n in numbers]\nprint(kvadraty)\n"),
    )}
    {two_up(
        code_block("filter_primer.py", "chetnye = list(filter(lambda n: n % 2 == 0, numbers))\n"),
        code_block("comprehension_s_if.py", "chetnye = [n for n in numbers if n % 2 == 0]\n"),
    )}
    {callout(
        "info",
        "Python чаще предпочитает comprehensions",
        "Для простых преобразований и фильтров comprehension обычно читается яснее, чем "
        "<code class=\"inline\">map()</code>/<code class=\"inline\">filter()</code> с lambda. "
        "Знать оба стиля полезно — вы встретите оба в реальном коде, — но по умолчанию тянитесь "
        "к comprehension, если задача простая.",
    )}

    {practice_card(
        "13-06",
        "Практика: лямбда-функции",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-06/index.html",
    )}
    """
    page(
        "13-06-lambda.html",
        page_title="Лямбда-функции",
        description="lambda как инструмент для конкретной ситуации (не «короткий def»): анатомия, ограничения, сравнение с def, map()/filter() против comprehensions.",
        kicker_suffix="Лямбда-функции",
        h1="Лямбда-функции",
        lede="Маленький безымянный объект функции для одного выражения — полезен в узких "
        "случаях, а не как более современная замена def.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-21 · Функции как конвейер
# ---------------------------------------------------------------------------

def build_21() -> None:
    body = f"""
    <h2>Результат одной функции — вход для следующей</h2>
    {code_block(
        "konvejer.py",
        "clean = normalize_text(input_text)\n"
        "words = split_words(clean)\n"
        "counts = count_words(words)\n",
    )}
    {flow_diagram([
        ("СЫРОЙ ТЕКСТ", ""),
        ("normalize_text", ""),
        ("ЧИСТЫЙ ТЕКСТ", ""),
        ("split_words", ""),
        ("СЛОВА", ""),
        ("count_words", ""),
        ("ЧАСТОТЫ", ""),
    ], caption="Каждая функция — одна понятная стадия; результат одной становится входом следующей")}
    {callout(
        "tip",
        "Это архитектурный приём, а не просто удобство",
        "Разбиение на такие стадии — мощный способ организовать программу: каждая функция "
        "решает одну понятную задачу, у каждой ясный вход и выход, и стадии можно "
        "тестировать по отдельности (§13.24).",
    )}

    <h2>Граф вызовов (call graph)</h2>
    <p>Когда функции вызывают другие функции, получившуюся структуру можно изобразить как
    дерево — <strong>граф вызовов</strong>:</p>
    {tree_diagram(
        ("MAIN", [
            ("normalize_text", []),
            ("analyze_text", [("count_words", []), ("count_unique", [])]),
            ("show_report", []),
        ]),
        caption="Граф вызовов — какая функция кого вызывает; показывает структуру программы целиком",
    )}
    <p>Мы вернёмся к этой идее в §13.22, когда будем рефакторить реальные проекты главы 12 в
    похожую структуру.</p>

    {practice_card(
        "13-21",
        "Практика: конвейер из функций",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-21/index.html",
    )}
    """
    page(
        "13-21-funkcii-kak-konvejer.html",
        page_title="Функции как конвейер",
        description="Результат одной функции становится входом следующей — паттерн конвейера обработки данных, и граф вызовов (call graph) как способ увидеть структуру программы.",
        kicker_suffix="Функции как конвейер",
        h1="Функции как конвейер",
        lede="Несколько маленьких функций, каждая с ясным входом и выходом, могут вместе "
        "выполнить крупную задачу — не хуже одного длинного скрипта, но гораздо понятнее.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-22 · Рефакторим проекты главы 12
# ---------------------------------------------------------------------------

def build_22() -> None:
    body = f"""
    <h2>Рефакторинг: меняем структуру, не меняем поведение</h2>
    {callout(
        "info",
        "Рефакторинг",
        "<strong>Рефакторинг</strong> — улучшение внутренней структуры программы без "
        "намеренного изменения того, что она должна делать снаружи. Мы уже видели этот термин "
        "в главе 12 (§12.9, Викторина) — здесь применим его к нескольким проектам подряд.",
    )}

    <h2>Викторина</h2>
    {code_block(
        "viktorina_do.py",
        "# ДО — один длинный скрипт (глава 12, §12.9)\n"
        "score = 0\n"
        "for q in questions:\n"
        '    user_answer = input(q["question"] + " ").strip().lower()\n'
        "    if user_answer == q[\"answer\"]:\n"
        "        score += 1\n",
    )}
    {code_block(
        "viktorina_posle.py",
        "def ask_question(question):\n"
        '    return input(question["question"] + " ").strip().lower()\n\n'
        "def check_answer(user_answer, question):\n"
        "    return user_answer == question[\"answer\"]\n\n"
        "def run_quiz(questions):\n"
        "    score = 0\n"
        "    for q in questions:\n"
        "        user_answer = ask_question(q)\n"
        "        if check_answer(user_answer, q):\n"
        "            score += 1\n"
        "    return score\n",
    )}

    <h2>Анализатор текста</h2>
    {code_block(
        "analizator_posle.py",
        "def normalize_text(text):\n"
        "    return text.lower().split()\n\n"
        "def count_words(words):\n"
        "    return len(words)\n\n"
        "def count_unique(words):\n"
        "    return len(set(words))\n",
    )}

    <h2>Записная книжка</h2>
    {code_block(
        "zapisnaya_knizhka_posle.py",
        "def add_contact(contacts, name, phone):\n"
        "    contacts[name] = phone\n\n"
        "def find_contact(contacts, name):\n"
        "    return contacts.get(name)\n\n"
        "def remove_contact(contacts, name):\n"
        "    del contacts[name]\n",
    )}

    <h2>Главная программа становится читаемым описанием алгоритма</h2>
    {two_up(
        code_block("do_glavnaya.py", "text = input(\"Текст: \")\ntext = text.lower()\nwords = text.split()\ncount = len(words)\nunique = set(words)\nunique_count = len(unique)\ncounts = {}\nfor word in words:\n    counts[word] = counts.get(word, 0) + 1\n# ... ещё 40 строк ...\n"),
        code_block("posle_glavnaya.py", "text = input(\"Текст: \")\nclean = normalize_text(text)\nstats = analyze_text(clean)\nshow_report(stats)\n"),
    )}
    {callout(
        "tip",
        "Главный выигрыш рефакторинга — читаемость верхнего уровня",
        "Правая версия читается почти как обычное предложение: «получить текст, нормализовать, "
        "проанализировать, показать отчёт». Вся сложность спрятана внутри отдельных функций — "
        "и каждую из них можно понять, протестировать и исправить независимо.",
    )}

    {exercise(3, "Turtle тоже рефакторится", "Возьмите код ёлки или мандалы из главы 12 и выделите отдельную функцию для одного яруса/луча — точно так же, как студия многоугольников в §13.26 выделяет draw_polygon().")}

    {practice_card(
        "13-22",
        "Практика: рефакторинг проекта из главы 12",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-22/index.html",
    )}
    """
    page(
        "13-22-refaktoring-glavy-12.html",
        page_title="Рефакторим проекты главы 12",
        description="Рефакторинг реальных проектов главы 12 (Викторина, Анализатор текста, Записная книжка) в наборы функций — с сохранением поведения.",
        kicker_suffix="Рефакторинг главы 12",
        h1="Рефакторим проекты главы 12",
        lede="Возьмём три готовых проекта прошлой главы и превратим их из одного длинного "
        "скрипта в набор понятных функций — поведение снаружи останется тем же.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-23 · Debug Lab: типичные ошибки функций
# ---------------------------------------------------------------------------

def build_23() -> None:
    bugs = [
        ("1 · Случайный вызов до определения", "greet()\n\ndef greet():\n    print('Привет')", "На момент вызова greet() ещё не определена — Python выполняет код сверху вниз, и NameError возникает раньше, чем строка def успевает выполниться."),
        ("2 · Незаметный def внутри def", "def outer():\n    ...\n\n    def helper():\n        ...", "Отступ определяет вложенность. Если helper случайно оказался с отступом внутри outer, он не будет виден снаружи как самостоятельная функция — только через outer."),
        ("3 · Функция всегда возвращает None", "def calculate(x):\n    print(x * 2)\n\nresult = calculate(5) + 1", "calculate печатает, но не возвращает — result станет None, и None + 1 вызовет TypeError."),
        ("4 · Не все пути функции возвращают значение", "def sign(number):\n    if number > 0:\n        return 'positive'\n    # а если number <= 0?", "Для отрицательных и нулевых чисел функция доходит до конца без return — и молча возвращает None."),
        ("5 · return внутри цикла на первой итерации", "def contains_even(numbers):\n    for n in numbers:\n        if n % 2 == 0:\n            return True\n        else:\n            return False", "return в ветке else срабатывает уже на первом элементе — проверяются не все числа. Правильно: return True внутри if, а return False — после всего цикла, с тем же отступом, что и for."),
        ("6 · return перепутан с break", "def find_first_even(numbers):\n    for n in numbers:\n        if n % 2 == 0:\n            break   # а не return n!", "break просто останавливает цикл — n нужно ещё явно вернуть отдельной строкой после цикла. return сразу выходит из ВСЕЙ функции, break — только из ближайшего цикла."),
        ("7 · Неожиданная мутация переданного списка", "def sorted_names(names):\n    names.sort()\n    return names", "names.sort() мутирует список вызывающего кода на месте. Если это не входит в план, безопаснее return sorted(names) — новый список, оригинал не тронут."),
        ("8 · Забыли скопировать перед изменением", "def normalize_items(items):\n    items[0] = items[0].strip()\n    return items", "Если исходные данные нужно сохранить нетронутыми, начните с items = items.copy() — но помните про поверхностность копии (глава 11, §11.10) для вложенных структур."),
        ("9 · Глобальное состояние усложняет тестирование", "score = 0\n\ndef add_point():\n    global score\n    score += 1", "Работает, но такую функцию сложнее тестировать изолированно — её результат зависит от скрытой глобальной переменной. def add_point(score): return score + 1 тестируется одной строкой, без всякой настройки."),
        ("10 · Параметр затеняет встроенное имя", "def total(list):\n    return sum(list)", "list — имя встроенного типа. Затенение его параметром работает, но сбивает с толку читателя и ломает доступ к настоящему list() внутри этой функции. Лучше: def total(numbers):"),
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
    <p>Десять типичных ошибок, связанных с функциями, — каждая с примером и объяснением.
    Первые две уже разбирались отдельно (§13.1, §13.13) — здесь для полноты списка, компактно;
    остальные восемь — подробно.</p>

    {bugs_html}

    {summary_box("Метод отладки функций", [
        "Печатает функция или возвращает? Проверьте на бумаге, прежде чем читать код.",
        "Проверены ли ВСЕ пути выполнения функции, включая неявный «конец без return»?",
        "return внутри цикла — точно ли он должен сработать именно на этой итерации?",
        "Мутирует ли функция переданный аргумент намеренно? Если нет — скопируйте.",
        "Не перепутано ли имя параметра со встроенным именем Python?",
    ])}

    {practice_card(
        "13-23",
        "Практика: находим и исправляем ошибки в функциях",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-23/index.html",
    )}
    """
    page(
        "13-23-debug-lab-funkcii.html",
        page_title="Debug Lab: типичные ошибки функций",
        description="10 типичных ошибок при работе с функциями: None-баги, непокрытые пути return, return внутри цикла, return vs break, случайная мутация аргумента и другие.",
        kicker_suffix="Debug Lab: функции",
        h1="Debug Lab: типичные ошибки функций",
        lede="Забытый return, return внутри цикла на первой итерации, случайно мутированный "
        "аргумент — десять ошибок, которые встречаются в реальном коде снова и снова.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-24 · Тестируем функции
# ---------------------------------------------------------------------------

def build_24() -> None:
    body = f"""
    <h2>Главное практическое преимущество функций</h2>
    {code_block("testiruemaya_funkciya.py", "def rectangle_area(w, h):\n    return w * h\n")}
    {code_block(
        "proverki.py",
        "rectangle_area(2, 3) == 6\n"
        "rectangle_area(0, 5) == 0\n"
        "rectangle_area(10, 1) == 10\n",
    )}
    {callout(
        "tip",
        "Не нужен ни пользовательский ввод, ни всё приложение целиком",
        "Функцию можно проверить в изоляции — вызвать напрямую с конкретными значениями и "
        "сравнить с ожидаемым результатом. Это и есть идея <strong>тестирования отдельных "
        "единиц</strong> кода.",
    )}

    <h2>Таблица тестов</h2>
    {comparison_table(
        ["Вход", "Ожидание", "Факт", "Пройден?"],
        [
            ["<code class=\"inline\">classify_score(95)</code>", "«отлично»", "«отлично»", "[[icon:success]]"],
            ["<code class=\"inline\">classify_score(60)</code>", "«хорошо»", "«хорошо»", "[[icon:success]]"],
            ["<code class=\"inline\">classify_score(0)</code>", "«пересдача»", "«пересдача»", "[[icon:success]]"],
            ["<code class=\"inline\">classify_score(100)</code>", "граница сверху", "?", "проверить"],
        ],
    )}
    {callout(
        "info",
        "Граничные случаи — из главы 9",
        "Тестовая таблица — прямое продолжение граничного тестирования условий из главы 9: "
        "проверяем не только «обычные» значения, но и границы диапазонов.",
    )}

    <h2>assert — лёгкая проверка предположения</h2>
    {code_block("assert_primer.py", "assert rectangle_area(2, 3) == 6\nassert rectangle_area(0, 5) == 0\nprint(\"Все проверки пройдены\")\n")}
    {code_block("assert_padaet.py", "assert rectangle_area(2, 3) == 7\n# AssertionError\n")}
    {callout(
        "warning",
        "assert — инструмент разработчика, не проверка пользовательского ввода",
        "<code class=\"inline\">assert</code> проверяет предположение и поднимает "
        "<code class=\"inline\">AssertionError</code>, если оно ложно — это удобно для "
        "самопроверки во время разработки и отладки. Это НЕ механизм валидации "
        "пользовательского ввода и не защита безопасности — для проверки данных, полученных от "
        "пользователя, используются обычные условия (глава 9), как мы уже делали.",
    )}

    <h2>Рабочий процесс: контракт → примеры → реализация → проверка</h2>
    {flow_diagram([
        ("Требование", "что функция должна делать"),
        ("Примеры", "вход → ожидаемый выход"),
        ("Реализация", "пишем def"),
        ("Вызов", "с тестовыми значениями"),
        ("Проверка", "совпало ли с ожиданием"),
    ], caption="Этот порядок мысли — прямой предвестник полноценного unit-тестирования, которое встретится в будущих главах")}

    {practice_card(
        "13-24",
        "Практика: тестируем функцию по таблице",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-24/index.html",
    )}
    """
    page(
        "13-24-testirovanie-funkcij.html",
        page_title="Тестируем функции",
        description="Функции легко тестировать в изоляции: таблица тестов, assert как инструмент разработчика (не валидация ввода), рабочий процесс контракт → примеры → реализация → проверка.",
        kicker_suffix="Тестируем функции",
        h1="Тестируем функции",
        lede="Функцию можно проверить отдельно от всей программы — без пользовательского "
        "ввода и без запуска приложения целиком.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-07 · Мини-проект — домашнее задание по математике (расширено: граф вызовов)
# ---------------------------------------------------------------------------

def build_07() -> None:
    body = f"""
    {requirements_card(["def", "return", "*args (опционально)", "random", "циклы"], "★★★ интеграционный", "текстовый тренажёр")}

    <p>Соберём функции, аргументы и return в одном полезном инструменте: генераторе примеров
    для тренировки таблицы умножения. Разобьём задачу на функции по смыслу, а не оставим одним
    куском:</p>
    {tree_diagram(
        ("MAIN", [
            ("sgenerirovat_primer", []),
            ("proverit_otvet", []),
        ]),
        caption="Граф вызовов: главная программа опирается на две маленькие, независимо проверяемые функции",
    )}
    {code_block(
        "domashnee_zadanie.py",
        "import random\n\n"
        "def sgenerirovat_primer():\n"
        "    a = random.randint(2, 9)\n"
        "    b = random.randint(2, 9)\n"
        "    return a, b, a * b\n\n"
        "def proverit_otvet(pravilnyj_otvet, otvet_polzovatelya):\n"
        "    return pravilnyj_otvet == otvet_polzovatelya\n\n"
        "a, b, pravilnyj_otvet = sgenerirovat_primer()\n"
        'otvet = int(input(f"Сколько будет {a} x {b}? "))\n\n'
        "if proverit_otvet(pravilnyj_otvet, otvet):\n"
        '    print("Верно!")\n'
        "else:\n"
        '    print(f"Неверно — правильный ответ: {pravilnyj_otvet}")\n',
    )}
    {callout(
        "info",
        "Функция возвращает сразу три значения",
        "<code class=\"inline\">return a, b, a * b</code> на самом деле возвращает один кортеж "
        "<code class=\"inline\">(a, b, a * b)</code> — мы распаковываем его в три переменные "
        "сразу, как в §13.10 и главе 11.",
    )}
    {callout(
        "tip",
        "sgenerirovat_primer и proverit_otvet тестируются отдельно",
        "<code class=\"inline\">proverit_otvet(56, 56)</code> и "
        "<code class=\"inline\">proverit_otvet(56, 50)</code> можно вызвать напрямую и "
        "проверить результат — без единого <code class=\"inline\">input()</code>. Это ровно "
        "идея из §13.24: чистая логика проверки отделена от ввода/вывода.",
    )}
    {exercise(2, "Счётчик правильных ответов", "Оберните генерацию примера в цикл на 5 вопросов подряд и посчитайте, сколько из них решено верно.")}

    {practice_card(
        "13-07",
        "Практика: генератор примеров по математике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-07/index.html",
    )}
    """
    page(
        "13-07-mini-proekt-domashka.html",
        page_title="Мини-проект — домашнее задание по математике",
        description="Мини-проект: генератор примеров на умножение, разбитый на независимо тестируемые функции — генерацию и проверку.",
        kicker_suffix="Домашнее задание",
        h1="Мини-проект — выполняем домашнее задание по математике с Python",
        lede="Функции для генерации и проверки примеров на умножение — практика на все приёмы "
        "главы, с чистой логикой проверки, отделённой от ввода-вывода.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-25 · Мини-проект — анализатор текста v2
# ---------------------------------------------------------------------------

def build_25() -> None:
    body = f"""
    {requirements_card(["def", "return", "list", "set", "dict"], "★★★ интеграционный", "текстовый отчёт")}

    <p>Полный рефакторинг анализатора текста из главы 12 (§12.6) в конвейер из чистых функций
    — прямое продолжение идеи §13.21.</p>
    {tree_diagram(
        ("MAIN", [
            ("normalize_text", []),
            ("split_words", []),
            ("word_frequency", []),
            ("build_summary", []),
        ]),
        caption="Каждая стадия — отдельная, независимо тестируемая функция",
    )}
    {code_block(
        "analizator_v2.py",
        "def normalize_text(text):\n"
        "    return text.lower()\n\n"
        "def split_words(text):\n"
        "    return text.split()\n\n"
        "def word_frequency(words):\n"
        "    counts = {}\n"
        "    for word in words:\n"
        "        counts[word] = counts.get(word, 0) + 1\n"
        "    return counts\n\n"
        "def build_summary(text):\n"
        "    clean = normalize_text(text)\n"
        "    words = split_words(clean)\n"
        "    counts = word_frequency(words)\n"
        "    return {\n"
        '        "total_words": len(words),\n'
        '        "unique_words": len(set(words)),\n'
        '        "counts": counts,\n'
        "    }\n\n"
        'summary = build_summary("Python is great and python is fun")\n'
        "print(summary)\n",
    )}
    {callout(
        "tip",
        "build_summary — это конвейер, вызывающий остальные три",
        "Точно паттерн из §13.21: <code class=\"inline\">build_summary</code> ничего не "
        "вычисляет сама — она передаёт данные по цепочке "
        "<code class=\"inline\">normalize_text → split_words → word_frequency</code> и "
        "собирает итог в словарь.",
    )}

    {practice_card(
        "13-25",
        "Практика: анализатор текста как конвейер функций",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-25/index.html",
    )}
    """
    page(
        "13-25-mini-proekt-analizator-v2.html",
        page_title="Мини-проект — анализатор текста v2",
        description="Полный рефакторинг анализатора текста в конвейер чистых функций: normalize_text, split_words, word_frequency, build_summary.",
        kicker_suffix="Анализатор текста v2",
        h1="Мини-проект — анализатор текста, версия 2",
        lede="Тот же анализатор текста из главы 12 — но теперь как чистый, тестируемый "
        "конвейер функций.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-26 · Мини-проекты — конвертер единиц и утилиты коллекций
# ---------------------------------------------------------------------------

def build_26() -> None:
    body = f"""
    {requirements_card(["def", "return", "type hints", "assert"], "★★ средний", "набор чистых функций")}

    <h2 id="konverter">Конвертер единиц измерения</h2>
    <p>Маленький проект из полностью чистых функций — идеальных кандидатов для тестирования из
    §13.24:</p>
    {code_block(
        "konverter.py",
        "def celsius_to_fahrenheit(celsius: float) -> float:\n"
        "    return celsius * 9 / 5 + 32\n\n"
        "def fahrenheit_to_celsius(fahrenheit: float) -> float:\n"
        "    return (fahrenheit - 32) * 5 / 9\n\n"
        "def km_to_miles(km: float) -> float:\n"
        "    return km * 0.621371\n\n"
        "assert celsius_to_fahrenheit(0) == 32\n"
        "assert celsius_to_fahrenheit(100) == 212\n"
        "assert round(km_to_miles(10), 2) == 6.21\n",
    )}
    {callout(
        "tip",
        "Ни одного input(), ни одного print() внутри самих функций",
        "Все три функции — чистые: результат целиком зависит от аргумента, побочных эффектов "
        "нет. Именно поэтому их можно проверить через <code class=\"inline\">assert</code>, не "
        "запуская вообще ничего похожего на полноценную программу.",
    )}

    <h2 id="utility">Утилиты для работы с коллекциями</h2>
    <p>Набор маленьких, сфокусированных функций поверх списков и словарей из главы 11:</p>
    {code_block(
        "kollekciya_utility.py",
        "def average(scores: list[float]) -> float:\n"
        "    return sum(scores) / len(scores)\n\n"
        "def count_above(scores: list[float], threshold: float) -> int:\n"
        "    return len([s for s in scores if s > threshold])\n\n"
        "def unique_words(text: str) -> set[str]:\n"
        "    return set(text.lower().split())\n\n"
        "def find_top_score(students: list[dict]) -> dict:\n"
        "    return max(students, key=lambda s: s[\"score\"])\n",
    )}
    {callout(
        "info",
        "find_top_score использует функцию как аргумент",
        "<code class=\"inline\">key=lambda s: s[\"score\"]</code> — то же самое сочетание "
        "<code class=\"inline\">max()</code>/<code class=\"inline\">sorted()</code> + lambda "
        "из §13.20 и §13.26, только теперь на списке словарей (глава 11, §11.14).",
    )}
    {exercise(2, "Ещё одна утилита", "Напишите find_students_below(students, threshold) — список имён учеников с баллом ниже threshold. Проверьте её на 2-3 примерах через assert.")}

    {practice_card(
        "13-26",
        "Практика: конвертер единиц измерения",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-26/index.html",
    )}
    {practice_card(
        "13-27",
        "Практика: утилиты для списков и словарей",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/13-27/index.html",
    )}
    """
    page(
        "13-26-mini-proekt-konverter-i-utility.html",
        page_title="Мини-проекты: конвертер и утилиты коллекций",
        description="Два мини-проекта из чистых функций: конвертер единиц измерения (температура, километры-мили) и утилиты для списков/словарей (average, count_above, unique_words, find_top_score).",
        kicker_suffix="Конвертер и утилиты",
        h1="Мини-проекты — конвертер единиц и утилиты коллекций",
        lede="Два небольших проекта, полностью состоящих из чистых функций — образцовых "
        "кандидатов для независимого тестирования.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 13-08 · Мини-проект — Turtle Function Studio (расширено: реальный вывод + полные итоги)
# ---------------------------------------------------------------------------

def build_08() -> None:
    body = f"""
    {requirements_card(["def", "параметры", "циклы", "Turtle"], "★★★★ challenge", "графика Turtle")}

    <h2>Что создаём</h2>
    <p>Финальный проект главы: превратим повторяющийся код рисования фигур из глав 6 и 10 в
    настоящую переиспользуемую функцию с параметрами.</p>

    <h2>Поток данных функции</h2>
    {flow_diagram([
        ("ВЫЗОВ", "draw_polygon(artist, 6, 80)"),
        ("ПАРАМЕТРЫ", "artist, sides=6, length=80"),
        ("РАСЧЁТ", "angle = 360 / sides"),
        ("ЦИКЛ", "sides раз"),
        ("РЕАЛЬНЫЙ ВЫВОД", "шестиугольник"),
    ], caption="Один вызов — параметры разворачиваются в расчёт, цикл и итоговый рисунок")}

    {turtle_output(
        "13-polygon-function",
        "draw_polygon.py",
        caption="draw_polygon(artist, 6, 80) — правильный шестиугольник",
        alt="Правильный шестиугольник, нарисованный функцией draw_polygon",
    )}

    <h2>Почему функция принимает artist явно</h2>
    {code_block(
        "figura_funkciya.py",
        "def draw_polygon(artist, sides, length):\n"
        "    angle = 360 / sides\n"
        "    for _ in range(sides):\n"
        "        artist.forward(length)\n"
        "        artist.right(angle)\n\n"
        "draw_polygon(artist, 4, 100)    # квадрат\n"
        "draw_polygon(artist, 3, 100)    # треугольник, без повторения кода!\n"
        "draw_polygon(artist, 8, 60)     # восьмиугольник\n",
    )}
    {callout(
        "tip",
        "Явный параметр artist — не лишняя формальность",
        "Функция могла бы полагаться на глобальную переменную <code class=\"inline\">artist</code>, "
        "как в главе 10. Но параметр делает зависимость ЯВНОЙ (§13.15): сразу видно, что "
        "функция работает именно с той черепашкой, которую ей передали, — её можно "
        "переиспользовать с другой черепашкой (например, во время гонки Turtle из §12.6, где "
        "черепашек несколько) без единого изменения кода внутри.",
    )}

    <h2>Функция внутри цикла: то же поведение, новый параметр на каждом шаге</h2>
    {code_block(
        "figury_v_cikle.py",
        "cveta = [\"#5B24F9\", \"#DB2777\", \"#059669\"]\n"
        "for i, sides in enumerate(range(3, 9)):\n"
        "    artist.pencolor(cveta[i % 3])\n"
        "    draw_polygon(artist, sides, 70)\n"
        "    artist.right(15)\n",
    )}
    {turtle_output(
        "13-polygon-scene",
        "figury_v_cikle.py",
        caption="Цикл вызывает draw_polygon с новым sides на каждом шаге — веер многоугольников",
        alt="Веер из шести повёрнутых многоугольников от треугольника до восьмиугольника, нарисованный циклом, вызывающим draw_polygon",
    )}
    {callout(
        "info",
        "Цикл автоматизирует повторение, функция — поведение",
        "Ровно идея §13.1: цикл решает, СКОЛЬКО раз и с какими данными вызвать "
        "<code class=\"inline\">draw_polygon</code>; сама функция решает, КАК нарисовать "
        "многоугольник с этими данными. Ни один из двух инструментов не заменяет другой.",
    )}

    {exercise(3, "Функция с позицией", "Добавьте функции параметры x, y (со значениями по умолчанию 0, 0) — чтобы можно было указать, откуда начинать рисовать фигуру.")}
{local_required_card(
        "13-08",
        "Практика: Turtle Function Studio",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/13-08/index.html",
    )}

    <h2 id="itogi">Итоги главы</h2>

    <h3>Инструментарий проектирования функции</h3>
    {decision_map([
        ("Нужно повторно использовать один и тот же набор действий?", "выделите функцию"),
        ("Функции нужны входные данные?", "параметры"),
        ("Нужно вернуть результат для дальнейшего использования?", "return"),
        ("Аргументов может быть неизвестное количество?", "*args / **kwargs"),
        ("Некоторые аргументы стоит сделать необязательными?", "значения по умолчанию (не изменяемые!)"),
        ("Некоторые аргументы должны передаваться только по имени?", "keyword-only, после *"),
        ("Функция должна вести себя предсказуемо и легко тестироваться?", "чистая функция, без побочных эффектов"),
        ("Нужно передать саму функцию как значение?", "функция — объект первого класса"),
        ("Нужно крошечное правило для sorted()/max()?", "lambda"),
    ], title="Итоговый инструментарий главы 13", caption="Полный чек-лист проектирования — в §13.18")}

    {summary_box("Что мы узнали в этой главе", [
        "Функция — именованный переиспользуемый кусок поведения: получает данные (параметры), "
        "работает с ними, возвращает результат (<code class=\"inline\">return</code>).",
        "Вызов функции передаёт управление в её тело и обязательно возвращается к месту "
        "вызова — функция не выполняется «где-то в стороне».",
        "Параметр — имя в определении, аргумент — значение в вызове. Присваивание параметру и "
        "мутация переданного объекта — два разных действия с разными последствиями снаружи.",
        "Изменяемое значение по умолчанию создаётся ОДИН РАЗ при определении функции — "
        "используйте <code class=\"inline\">None</code> как сигнальное значение вместо "
        "<code class=\"inline\">[]</code> или <code class=\"inline\">{}</code>.",
        "<code class=\"inline\">*args</code> и <code class=\"inline\">**kwargs</code> собирают "
        "лишние аргументы в кортеж и словарь соответственно; та же <code class=\"inline\">*</code>/"
        "<code class=\"inline\">**</code> на месте вызова распаковывает коллекцию обратно.",
        "Функция без <code class=\"inline\">return</code> всё равно возвращает "
        "<code class=\"inline\">None</code> — это не «ничего», а конкретный объект.",
        "Python ищет имя по правилу LEGB: Local → Enclosing → Global → Builtins.",
        "Функции, вызывающие функции, образуют стек вызовов — и traceback из главы 3 "
        "показывает именно этот стек в момент ошибки.",
        "Функции — объекты первого класса: их можно сохранять под другим именем, класть в "
        "коллекции, передавать другим функциям (<code class=\"inline\">sorted(key=...)</code>).",
        "<code class=\"inline\">lambda</code> — маленькая безымянная функция для одного "
        "выражения, не более «современная» замена <code class=\"inline\">def</code>.",
        "Рефакторинг большого скрипта в набор функций делает главную программу читаемым "
        "описанием алгоритма, а каждую часть — независимо тестируемой.",
    ])}

    <h3>Что дальше</h3>
    <p>Мы научились группировать ПОВЕДЕНИЕ в функции. Но во многих наших проектах данные и
    поведение, которое с ними работает, естественно ходят парой — контакт со своим телефоном,
    ученик со своим баллом, черепашка со своим цветом и позицией. В следующей главе —
    <strong>«Создаём объекты реального мира»</strong> — мы научимся объединять данные и функции,
    которые с ними работают, в одну именованную структуру.</p>
    """
    out = render_page(
        page_title="Мини-проект — Turtle Function Studio",
        description="Финальный мини-проект главы 13: универсальная функция рисования многоугольников с явным параметром artist — и полные итоги главы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Turtle Function Studio", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Мини-проект — Turtle Function Studio",
        lede="Фигуры из глав 6 и 10 становятся настоящей переиспользуемой функцией с явными "
        "параметрами — и подводим итоги всей главы о функциях.",
        body_html=body,
        sidebar_groups=sidebar("13-08-mini-proekt-figury-itogi.html"),
        nav=nav_for("13-08-mini-proekt-figury-itogi.html"),
    )
    write("13-08-mini-proekt-figury-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_09()
    build_01()
    build_10()
    build_02()
    build_11()
    build_12()
    build_04()
    build_13()
    build_14()
    build_03()
    build_15()
    build_05()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_06()
    build_21()
    build_22()
    build_23()
    build_24()
    build_07()
    build_25()
    build_26()
    build_08()
