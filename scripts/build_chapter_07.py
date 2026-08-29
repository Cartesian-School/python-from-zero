#!/usr/bin/env python3
"""Строит Главу 7: «Глубокое погружение в Turtle» (site/chapters/glava-07/).

Curriculum v2: от короткой главы про настройку экрана и пары мини-проектов
до полноценного продвинутого курса графики Turtle — окно как графическая
система (window/canvas/coordinate world), colormode и цвет, перо и заливка
раздельно, speed/tracer/update, глубокая геометрия окружности (центр слева
от черепашки, положительный/отрицательный радиус, extent, steps —
многоугольник как окружность), штампы, текст (write, align, font),
интеграция текста с координатной системой, черепашка как графический
объект (shape/shapesize/tilt), несколько черепашек и clone() — тихий мост
к ООП, clear/reset/home, отладка графики, и профессиональные версии двух
существующих мини-проектов плюс два новых (часы, координатная мишень).

Каждый существенный пример показывает РЕАЛЬНЫЙ выполненный результат (см.
chapter_07_examples.py и generate_chapter_07_outputs.py, использующие
общий пайплайн из turtle_output_lib.py) — ни одна картинка не нарисована
вручную.

Существующие маршруты и практики (07-01..07-09, id 07-01/03/04/06/07/09)
сохранены и расширены на месте; новый материал — новые страницы.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_07_examples import EXAMPLES
from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    code_block,
    comparison_table,
    exercise,
    local_required_card,
    practice_card,
    practice_revisit_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-07"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Обзор главы"),
    ("07-01-nastraivaem-ekran.html", "Экран как графическая система"),
    ("07-10-colormode-i-cvet.html", "colormode и цвет"),
    ("07-02-nastraivaem-grafiku.html", "Настраиваем саму Turtle"),
    ("07-11-pero-i-zalivka.html", "Перо и заливка — не одно и то же"),
    ("07-12-speed-tracer-update.html", "speed, tracer и update"),
    ("07-03-figury-bez-linij.html", "Фигуры без линий, окружности, точки"),
    ("07-13-geometriya-okruzhnosti.html", "Геометрия окружности"),
    ("07-04-dugi.html", "Дуги"),
    ("07-14-circle-steps.html", "circle(steps=...) — от круга к многоугольнику"),
    ("07-05-eshche-vozmozhnosti.html", "Штампы и другие приёмы"),
    ("07-06-tekst-na-ekrane.html", "Рисуем текст на экране"),
    ("07-15-vyravnivanie-i-shrift.html", "Выравнивание и шрифт"),
    ("07-16-tekst-i-koordinaty.html", "Текст и координатная система"),
    ("07-17-forma-cherepashki.html", "Черепашка как графический объект"),
    ("07-18-neskolko-cherepashek.html", "Несколько черепашек"),
    ("07-19-clone.html", "clone() — копируем состояние"),
    ("07-20-clear-reset-home.html", "clear(), reset() и home()"),
    ("07-23-otladka-grafiki.html", "Отладка графики"),
    ("07-07-mini-proekt-okruzhnost-kvadrat.html", "Мини-проект: окружность в квадрате"),
    ("07-08-napravlenie-risovaniya.html", "Меняем направление рисования"),
    ("07-21-mini-proekt-chasy.html", "Мини-проект: часы без времени"),
    ("07-22-mini-proekt-mishen.html", "Мини-проект: координатная мишень"),
    ("07-09-mini-proekt-smajlik-itogi.html", "Мини-проект: смайлик и итоги"),
]

PRACTICE_IDS = [
    "07-01", "07-10", "07-11", "07-12", "07-03", "07-13", "07-04",
    "07-14", "07-24", "07-06", "07-15", "07-16", "07-17", "07-18",
    "07-19", "07-20", "07-25", "07-23", "07-07", "07-21", "07-22", "07-09",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 7 · Turtle подробно", items),
        SidebarGroup("Практика", [
            NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def turtle_output(name: str, filename: str, *, caption: str, alt: str) -> str:
    """КОД → РЕАЛЬНЫЙ OUTPUT — тот же компонент, что и в главе 6 (см.
    scripts/build_chapter_06.py:turtle_output). code_block() слева/сверху,
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
          <img src="{IMG}/chapter-07/output/{name}.png" alt="{alt}"
            style="width:100%;height:auto;border-radius:12px;display:block;background:#fff" />
          <figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>
        </figure>
      </div>
    </div>"""


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=7,
        description="Turtle как настоящая графическая система: окно и холст, цвет и режимы "
        "colormode, перо и заливка раздельно, глубокая геометрия окружности, штампы, текст и "
        "координаты, несколько черепашек и clone(), отладка графики — и четыре мини-проекта, "
        "включая часы и координатную мишень.",
        meta_items=["[[icon:timer]] ~5–6 часов", "[[icon:code]] модуль turtle", "[[icon:practice]] 22 практики", "[[icon:palette]] реальные результаты у каждого примера"],
        sections=[
            ChapterSectionLink("7.1", "Экран как графическая система", "07-01-nastraivaem-ekran.html"),
            ChapterSectionLink("7.2", "colormode и цвет", "07-10-colormode-i-cvet.html"),
            ChapterSectionLink("7.3", "Настраиваем саму Turtle", "07-02-nastraivaem-grafiku.html"),
            ChapterSectionLink("7.4", "Перо и заливка — не одно и то же", "07-11-pero-i-zalivka.html"),
            ChapterSectionLink("7.5", "speed, tracer и update", "07-12-speed-tracer-update.html"),
            ChapterSectionLink("7.6", "Фигуры без линий, окружности, точки", "07-03-figury-bez-linij.html"),
            ChapterSectionLink("7.7", "Геометрия окружности", "07-13-geometriya-okruzhnosti.html"),
            ChapterSectionLink("7.8", "Дуги", "07-04-dugi.html"),
            ChapterSectionLink("7.9", "circle(steps=...) — от круга к многоугольнику", "07-14-circle-steps.html"),
            ChapterSectionLink("7.10", "Штампы и другие приёмы", "07-05-eshche-vozmozhnosti.html"),
            ChapterSectionLink("7.11", "Рисуем текст на экране", "07-06-tekst-na-ekrane.html"),
            ChapterSectionLink("7.12", "Выравнивание и шрифт", "07-15-vyravnivanie-i-shrift.html"),
            ChapterSectionLink("7.13", "Текст и координатная система", "07-16-tekst-i-koordinaty.html"),
            ChapterSectionLink("7.14", "Черепашка как графический объект", "07-17-forma-cherepashki.html"),
            ChapterSectionLink("7.15", "Несколько черепашек", "07-18-neskolko-cherepashek.html"),
            ChapterSectionLink("7.16", "clone() — копируем состояние", "07-19-clone.html"),
            ChapterSectionLink("7.17", "clear(), reset() и home()", "07-20-clear-reset-home.html"),
            ChapterSectionLink("7.18", "Отладка графики", "07-23-otladka-grafiki.html"),
            ChapterSectionLink("7.19", "Мини-проект — окружность в квадрате", "07-07-mini-proekt-okruzhnost-kvadrat.html"),
            ChapterSectionLink("7.20", "Меняем направление рисования", "07-08-napravlenie-risovaniya.html"),
            ChapterSectionLink("7.21", "Мини-проект — часы без времени", "07-21-mini-proekt-chasy.html"),
            ChapterSectionLink("7.22", "Мини-проект — координатная мишень", "07-22-mini-proekt-mishen.html"),
            ChapterSectionLink("7.23", "Мини-проект — смайлик и итоги", "07-09-mini-proekt-smajlik-itogi.html"),
        ],
    )
    write("index.html", out)


def build_01_ekran() -> None:
    window_diagram = (
        '<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        '<div style="border:2px solid #0D0230;border-radius:8px;padding:18px;background:#fff;max-width:380px;width:100%">'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:11px;color:var(--ink-soft,#6B6B7D);margin-bottom:8px">РАБОЧИЙ СТОЛ</div>'
        '<div style="border:2px solid #5B24F9;border-radius:6px;padding:14px;background:#FAFAFC">'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:11px;color:#5B24F9;margin-bottom:8px">ОКНО TURTLE (screen.setup)</div>'
        '<div style="border:2px dashed #B9A0FC;border-radius:4px;padding:20px;background:#fff;text-align:center">'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:11px;color:#B9A0FC">ХОЛСТ (screen.screensize)</div>'
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:var(--ink-soft,#6B6B7D);margin-top:6px">координатный мир: любые числа x, y</div>'
        '</div></div></div>'
        '<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">'
        'Три разных вещи: окно (видимый размер), холст (область для рисования, может быть больше окна) и координатный мир (числа, которым вообще нет предела)</figcaption>'
        '</figure>'
    )
    light = turtle_output(
        "07-01-light-theme", "svetlaya_tema.py",
        caption="setup(width=500, height=360), title(...) и светлый bgcolor()",
        alt="Светлое окно Turtle светло-фиолетового оттенка с заголовком Cartesian Turtle Studio и короткой фиолетовой линией",
    )
    dark = turtle_output(
        "07-01-dark-theme", "temnaya_tema.py",
        caption="Тот же код, но с тёмным bgcolor() — тема окна не меняет ничего в логике рисования",
        alt="Тёмно-синее окно Turtle с той же линией, нарисованной светло-фиолетовым цветом",
    )
    body = f"""
    <p>В главе 6 мы уже создавали окно и черепашку — но не разбирались, что вообще внутри
    происходит. Начнём с того, что Turtle — это не просто «нарисовать линию», а настоящая
    графическая система с несколькими слоями.</p>

    <h2>Три разные вещи, которые легко перепутать</h2>
    <p>Когда мы говорим о «размере» в Turtle, на самом деле речь может идти о трёх разных
    вещах:</p>
{window_diagram}
    <ul>
      <li><strong>Окно</strong> — то, что видно на экране компьютера, размер задаёт <code class="inline">screen.setup()</code>.</li>
      <li><strong>Холст</strong> — область, на которой можно рисовать; обычно совпадает с окном, но может быть и больше (тогда появляются полосы прокрутки) — размер задаёт <code class="inline">screen.screensize()</code>.</li>
      <li><strong>Координатный мир</strong> — числа x и y, которыми мы оперируем в коде; они ничем не ограничены и не обязаны совпадать с пикселями окна один в один.</li>
    </ul>
{callout(
        "info",
        "Для начала достаточно setup()",
        "В подавляющем большинстве учебных программ довольно одного "
        "<code class=\"inline\">screen.setup()</code> — окно и холст совпадают, и думать о "
        "разнице не приходится. <code class=\"inline\">screensize()</code> нужен реже — "
        "например, когда рисунок больше, чем разумно показывать на экране целиком.",
    )}

    <h2>Настраиваем окно: до и после</h2>
    <p>Три команды экрана — заголовок, цвет фона и размер:</p>
{light}
{code_block("svetlaya_tema_kod.py", 'screen.setup(width=700, height=500)\nscreen.title("Cartesian Turtle Studio")\nscreen.bgcolor("#F5F2FF")\n')}
    <p>Меняем только цвет фона — вся остальная логика рисования остаётся той же:</p>
{dark}

{practice_card(
        "07-01",
        "Практика: настройка экрана как системы",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-01/index.html",
    )}
    """
    out = render_page(
        page_title="Экран как графическая система",
        description="Окно, холст и координатный мир Turtle — три разные вещи. setup(), screensize(), title(), bgcolor() с реальным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Экран как система", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Экран как графическая система",
        lede="Прежде чем рисовать что-то сложнее квадратов, разберёмся, что вообще значит "
        "«размер» в Turtle — окно, холст и координатный мир не одно и то же.",
        body_html=body,
        sidebar_groups=sidebar("07-01-nastraivaem-ekran.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="07-10-colormode-i-cvet.html", next_label="colormode и цвет"),
    )
    write("07-01-nastraivaem-ekran.html", out)


def build_10_colormode() -> None:
    swatches = turtle_output(
        "07-10-rgb-swatches", "rgb_svatchi.py",
        caption="colormode(255) — четыре цвета, заданных тройками (r, g, b) от 0 до 255",
        alt="Четыре цветных квадрата в ряд — красный, зелёный, синий и жёлтый — с подписями под каждым",
    )
    body = f"""
    <p>Мы уже задавали цвета по имени — <code class="inline">\"purple\"</code>,
    <code class="inline">\"gold\"</code>. Но у Turtle есть и числовой способ — через компоненты
    красного, зелёного и синего (RGB).</p>

    <h2>Два режима: 0.0–1.0 и 0–255</h2>
    <p><code class="inline">screen.colormode()</code> определяет, в каком диапазоне
    записываются числа RGB:</p>
{comparison_table(
        ["Режим", "Диапазон каждого числа", "Пример красного"],
        [
            ["<code class=\"inline\">colormode(1.0)</code> (по умолчанию)", "0.0 — 1.0", "<code class=\"inline\">(1.0, 0.0, 0.0)</code>"],
            ["<code class=\"inline\">colormode(255)</code>", "0 — 255", "<code class=\"inline\">(255, 0, 0)</code>"],
        ],
    )}
{code_block("colormode_kod.py", 'screen.colormode(255)\nartist.pencolor(255, 0, 0)   # красный, компоненты 0-255\n\nscreen.colormode(1.0)\nartist.pencolor(1.0, 0, 0)  # тот же красный, компоненты 0.0-1.0\n')}
{callout(
        "warning",
        "Числа вне диапазона — ошибка",
        "Если установлен <code class=\"inline\">colormode(1.0)</code>, а вы передадите "
        "<code class=\"inline\">(255, 0, 0)</code> — Turtle не поймёт, что вы имели в виду "
        "красный: 255 вне диапазона 0.0–1.0, и будет ошибка. Режим и числа должны совпадать.",
    )}

    <h2>RGB-палитра целиком</h2>
{swatches}
{code_block("rgb_svatchi_kod.py", 'screen.colormode(255)\n\nartist.fillcolor(255, 0, 0)     # красный\nartist.fillcolor(0, 200, 0)     # зелёный\nartist.fillcolor(0, 0, 255)     # синий\nartist.fillcolor(255, 210, 0)   # жёлтый\n')}

    <h2>Три способа задать один и тот же цвет</h2>
{comparison_table(
        ["Способ", "Пример", "Когда удобно"],
        [
            ["Название", "<code class=\"inline\">\"red\"</code>", "быстро, для стандартных цветов"],
            ["HEX-код", "<code class=\"inline\">\"#FF0000\"</code>", "точный оттенок, как в CSS/дизайне"],
            ["RGB-кортеж", "<code class=\"inline\">(255, 0, 0)</code>", "когда цвет вычисляется в коде (например, случайный)"],
        ],
    )}
{callout(
        "tip",
        "Не углубляемся в теорию цвета",
        "Этого достаточно для практики этой главы. Как RGB устроен «под капотом» — тема для "
        "отдельного курса по графике, а не для этой книги.",
    )}

{practice_card(
        "07-10",
        "Практика: colormode и RGB",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-10/index.html",
    )}
    """
    out = render_page(
        page_title="colormode и цвет",
        description="Режимы colormode(1.0) и colormode(255) в Turtle, RGB-палитра и сравнение названий цветов, HEX-кодов и RGB-кортежей.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("colormode и цвет", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="colormode и цвет",
        lede="Название, HEX-код или тройка чисел RGB — три способа сказать Turtle одно и то же: "
        "«вот этот цвет».",
        body_html=body,
        sidebar_groups=sidebar("07-10-colormode-i-cvet.html"),
        nav=PageNav(prev_href="07-01-nastraivaem-ekran.html", prev_label="Экран как система", next_href="07-02-nastraivaem-grafiku.html", next_label="Настраиваем саму Turtle"),
    )
    write("07-10-colormode-i-cvet.html", out)


def build_02_grafika() -> None:
    config = turtle_output(
        "07-02-turtle-config", "nastrojka_grafiki.py",
        caption="speed(3), pensize(4), pencolor(\"purple\"), shape(\"turtle\") — четыре настройки черепашки разом",
        alt="Толстая фиолетовая линия, нарисованная черепашкой с формой курсора в виде силуэта черепахи",
    )
    body = f"""
    <p>В прошлом разделе мы настраивали <strong>экран</strong>. Теперь настроим саму
    <strong>черепашку</strong>: скорость рисования, толщину и цвет линии, форму указателя.</p>
{config}
{code_block("nastrojka_grafiki_kod.py", "artist.speed(3)          # скорость от 1 (медленно) до 10 (быстро), 0 — мгновенно\nartist.pensize(4)        # толщина линии в пикселях\nartist.pencolor(\"purple\") # цвет линии\nartist.shape(\"turtle\")    # форма указателя — черепашка вместо стрелки\n")}
{callout(
        "info",
        "speed(0) — режим художника",
        "Когда важен результат, а не сам процесс рисования (например, в сложных узорах вроде "
        "мандалы из главы 6), удобно поставить <code class=\"inline\">artist.speed(0)</code> — "
        "черепашка рисует мгновенно, без анимации движения. Мы разберём, почему это не влияет "
        "на итоговый рисунок, в разделе «speed, tracer и update».",
    )}

{practice_revisit_card(
        "07-01",
        "Практика: включает настройку графики черепашки",
        "Тот же ноутбук, что и в разделе «Экран как система» — он охватывает и эту тему",
        "../../practice/07-01/index.html",
    )}
    """
    out = render_page(
        page_title="Настраиваем саму Turtle",
        description="Скорость рисования, толщина и цвет линии, форма черепашки — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Настраиваем графику", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Настраиваем саму Turtle",
        lede="Экран настроен — теперь настроим саму черепашку: скорость, толщина, цвет, форма "
        "указателя.",
        body_html=body,
        sidebar_groups=sidebar("07-02-nastraivaem-grafiku.html"),
        nav=PageNav(prev_href="07-10-colormode-i-cvet.html", prev_label="colormode и цвет", next_href="07-11-pero-i-zalivka.html", next_label="Перо и заливка"),
    )
    write("07-02-nastraivaem-grafiku.html", out)


def build_11_pero_zalivka() -> None:
    pencolor_only = turtle_output(
        "07-11-pencolor-only", "tolko_pencolor.py",
        caption="pencolor(\"blue\") без fillcolor — только контур, заливки нет",
        alt="Квадрат, нарисованный только синим контуром, без заливки внутри",
    )
    combined = turtle_output(
        "07-11-color-combined", "color_vmeste.py",
        caption="color(\"blue\", \"gold\") задаёт И контур, И заливку одной командой",
        alt="Тот же квадрат с синим контуром, но теперь с золотой заливкой внутри",
    )
    body = f"""
    <p>Мы уже пользовались и <code class="inline">pencolor()</code>, и
    <code class="inline">fillcolor()</code> по отдельности — но важно чётко понимать, что это
    <strong>два разных</strong> цвета, отвечающих за разное.</p>

    <h2>Контур — это не то же самое, что заливка</h2>
{comparison_table(
        ["Команда", "За что отвечает"],
        [
            ["<code class=\"inline\">pencolor()</code>", "цвет ЛИНИИ — границы фигуры"],
            ["<code class=\"inline\">fillcolor()</code>", "цвет ЗАЛИВКИ — области внутри фигуры (виден только между begin_fill()/end_fill())"],
            ["<code class=\"inline\">color()</code>", "задаёт оба сразу: color(контур, заливка)"],
        ],
    )}
{pencolor_only}
{code_block("tolko_pencolor_kod.py", 'artist.pencolor("blue")\n\nfor _ in range(4):\n    artist.forward(120)\n    artist.right(90)\n')}

    <h2>Оба цвета одной командой</h2>
{combined}
{code_block("color_vmeste_kod.py", 'artist.color("blue", "gold")   # (контур, заливка)\n\nartist.begin_fill()\nfor _ in range(4):\n    artist.forward(120)\n    artist.right(90)\nartist.end_fill()\n')}
{callout(
        "tip",
        "color() без аргументов — узнать текущие цвета",
        "<code class=\"inline\">artist.color()</code> без аргументов возвращает пару "
        "<code class=\"inline\">(pencolor, fillcolor)</code> — удобно для отладки, если "
        "непонятно, почему фигура выглядит не так, как ожидалось.",
    )}

{practice_card(
        "07-11",
        "Практика: перо и заливка",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-11/index.html",
    )}
    """
    out = render_page(
        page_title="Перо и заливка — не одно и то же",
        description="pencolor(), fillcolor() и color() в Turtle — контур и заливка отвечают за разные вещи.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Перо и заливка", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Перо и заливка — не одно и то же",
        lede="Контур фигуры и её внутренняя область красятся разными командами — разбираемся, "
        "какая за что отвечает.",
        body_html=body,
        sidebar_groups=sidebar("07-11-pero-i-zalivka.html"),
        nav=PageNav(prev_href="07-02-nastraivaem-grafiku.html", prev_label="Настраиваем графику", next_href="07-12-speed-tracer-update.html", next_label="speed, tracer и update"),
    )
    write("07-11-pero-i-zalivka.html", out)


def build_12_speed_tracer() -> None:
    batch = turtle_output(
        "07-12-tracer-batch", "tracer_batch.py",
        caption="36 окружностей, каждая повёрнута на 10° — нарисованы мгновенно благодаря tracer(0) + update()",
        alt="Сложный симметричный узор из 36 наложенных друг на друга окружностей, образующих цветочный паттерн",
    )
    flow = (
        '<div style="display:flex;gap:20px;flex-wrap:wrap;margin:24px 0">'
        '<div style="flex:1;min-width:220px;padding:16px 18px;background:var(--color-bg-surface,#FAFAFC);border-radius:16px">'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;color:#5B24F9;margin-bottom:10px">ОБЫЧНЫЙ РЕЖИМ</div>'
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:13px;line-height:2.2;color:#0D0230">команда → экран обновился<br>команда → экран обновился<br>команда → экран обновился</div>'
        '</div>'
        '<div style="flex:1;min-width:220px;padding:16px 18px;background:var(--color-bg-surface,#FAFAFC);border-radius:16px">'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;color:#DB2777;margin-bottom:10px">ПАКЕТНЫЙ РЕЖИМ — tracer(0)</div>'
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:13px;line-height:2.2;color:#0D0230">tracer(0)<br>команда, команда, команда, ...<br>update() → экран обновился ОДИН раз</div>'
        '</div></div>'
    )
    body = f"""
    <h2>speed() меняет анимацию, а не результат</h2>
    <p><code class="inline">artist.speed()</code> управляет тем, <strong>как быстро</strong>
    видно рисование — не тем, что в итоге получится. Финальный рисунок при
    <code class="inline">speed(1)</code> и при <code class="inline">speed(0)</code>
    получится геометрически <strong>абсолютно одинаковым</strong> — разница только в том,
    видите ли вы сам процесс или сразу готовый результат. Статичная картинка физически не
    может показать разницу в скорости — её видно только вживую, при запуске кода.</p>

    <h2>tracer() и update(): рисовать пакетами</h2>
    <p>Для действительно сложных рисунков (сотни и тысячи команд) даже
    <code class="inline">speed(0)</code> может ощущаться медленным — экран обновляется после
    <strong>каждой</strong> команды. <code class="inline">screen.tracer(0)</code> отключает
    промежуточные обновления совсем, а <code class="inline">screen.update()</code> обновляет
    экран один раз, вручную, когда рисунок готов:</p>
{flow}
{batch}
{code_block("tracer_batch_kod.py", 'screen.tracer(0)   # отключаем промежуточные обновления\n\nfor i in range(36):\n    artist.circle(80)\n    artist.right(10)\n\nscreen.update()    # один финальный апдейт — и весь узор появляется разом\n')}
{callout(
        "info",
        "Зачем это нужно",
        "Для 10 команд разницы почти не заметно. Но для тысяч операций "
        "<code class=\"inline\">tracer(0)</code> + <code class=\"inline\">update()</code> "
        "может сделать рисование в разы быстрее — экран просто не тратит время на "
        "перерисовку после каждого шага.",
    )}

    <h2><code class="inline">delay()</code> — отдельная настройка</h2>
    <p><code class="inline">screen.delay()</code> задаёт задержку в миллисекундах между
    кадрами анимации — концептуально похоже на <code class="inline">speed()</code>, но
    работает на уровне экрана, а не отдельной черепашки:</p>
{code_block("delay_kod.py", "screen.delay(15)   # миллисекунды между кадрами анимации\nprint(screen.delay())  # без аргумента — вернёт текущее значение\n")}

    <h2>Классическая ловушка отладки</h2>
{callout(
        "warning",
        "tracer(0) без update() — пустой экран",
        "Если вызвать <code class=\"inline\">tracer(0)</code> и что-то нарисовать, но забыть "
        "<code class=\"inline\">update()</code> — экран останется пустым! Это одна из самых "
        "частых и неочевидных ошибок с Turtle — код выполняется без единой ошибки, а на "
        "экране ничего нет. Подробнее разберём в разделе про отладку графики.",
    )}

{practice_card(
        "07-12",
        "Практика: speed, tracer и update",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-12/index.html",
    )}
    """
    out = render_page(
        page_title="speed, tracer и update",
        description="speed() влияет только на анимацию, не на результат. tracer(0) + update() для пакетного рисования сложной графики.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("speed, tracer, update", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="speed, tracer и update",
        lede="Скорость анимации и итоговая геометрия рисунка — совершенно разные вещи. А для "
        "по-настоящему сложных узоров есть приём куда мощнее, чем просто speed(0).",
        body_html=body,
        sidebar_groups=sidebar("07-12-speed-tracer-update.html"),
        nav=PageNav(prev_href="07-11-pero-i-zalivka.html", prev_label="Перо и заливка", next_href="07-03-figury-bez-linij.html", next_label="Фигуры без линий"),
    )
    write("07-12-speed-tracer-update.html", out)


def build_03_figury() -> None:
    zalivka = turtle_output(
        "07-03-zalivka", "zalivka.py",
        caption="begin_fill()/end_fill() закрашивают замкнутый контур",
        alt="Золотой закрашенный квадрат",
    )
    okruzhnost = turtle_output(
        "07-03-okruzhnost", "okruzhnost.py",
        caption="circle(80) — готовая команда для окружности, без единого поворота вручную",
        alt="Фиолетовая окружность радиусом 80 пикселей",
    )
    tochka = turtle_output(
        "07-03-tochka", "tochka.py",
        caption="dot(50, \"red\") — точка без движения черепашки",
        alt="Одна крупная красная точка диаметром 50 пикселей",
    )
    body = f"""
    <p>Три инструмента, с которыми мы уже вскользь встречались в главе 6 — теперь наведём
    порядок и посмотрим на них внимательнее, прежде чем идти глубже.</p>

    <h2>Фигуры без линий: заливка цветом</h2>
    <p>Чтобы нарисовать не просто контур, а закрашенную фигуру, оберните рисование между
    <code class="inline">begin_fill()</code> и <code class="inline">end_fill()</code>:</p>
{zalivka}
{code_block("zalivka_kod.py", 'artist.fillcolor("gold")\nartist.begin_fill()\nfor _ in range(4):\n    artist.forward(100)\n    artist.right(90)\nartist.end_fill()\n')}

    <h2 id="okruzhnosti">Окружности</h2>
    <p>Рисовать окружность вручную через множество коротких отрезков не нужно — у Turtle есть
    готовая команда <code class="inline">circle(радиус)</code>:</p>
{okruzhnost}

    <h2 id="tochki">Точки</h2>
    <p><code class="inline">dot()</code> — маленький (или не очень) закрашенный кружок в
    текущей позиции, без движения черепашки:</p>
{tochka}
{code_block("tochka_kod.py", 'artist.dot(50, "red")   # точка диаметром 50, красная\n')}
{callout(
        "info",
        "Впереди — намного глубже",
        "Это только знакомство. В следующих трёх разделах разберём геометрию окружности "
        "по-настоящему подробно — откуда берётся центр, что значит отрицательный радиус, и как "
        "окружность превращается в многоугольник.",
    )}

{practice_revisit_card(
        "07-03",
        "Практика: заливка, окружности и точки",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-03/index.html",
    )}
    """
    out = render_page(
        page_title="Фигуры без линий, окружности, точки",
        description="Заливка цветом (begin_fill/end_fill), готовая команда circle() и точки dot() — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Фигуры, окружности, точки", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Фигуры без линий, окружности, точки",
        lede="Три инструмента из главы 6, но теперь с реальным выполненным результатом — и "
        "мостом к более глубокой геометрии окружности впереди.",
        body_html=body,
        sidebar_groups=sidebar("07-03-figury-bez-linij.html"),
        nav=PageNav(prev_href="07-12-speed-tracer-update.html", prev_label="speed, tracer, update", next_href="07-13-geometriya-okruzhnosti.html", next_label="Геометрия окружности"),
    )
    write("07-03-figury-bez-linij.html", out)


def build_13_geometriya_okruzhnosti() -> None:
    center_diagram = (
        '<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        '<svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" role="img" '
        'aria-label="Центр окружности находится слева от черепашки, на расстоянии radius" style="width:100%;height:auto;max-width:320px">'
        '<circle cx="160" cy="110" r="80" fill="none" stroke="#B9A0FC" stroke-width="2" stroke-dasharray="5,5"/>'
        '<circle cx="160" cy="110" r="4" fill="#0D0230"/>'
        '<text x="160" y="138" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13" fill="#0D0230">центр</text>'
        '<line x1="160" y1="110" x2="240" y2="110" stroke="#5B24F9" stroke-width="2"/>'
        '<text x="200" y="98" text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="#5B24F9">radius</text>'
        '<polygon points="240,110 228,104 228,116" fill="#DB2777"/>'
        '<text x="248" y="114" font-family="Sora, sans-serif" font-weight="700" font-size="13" fill="#DB2777">черепашка</text>'
        '</svg>'
        '<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">'
        'Центр окружности находится на расстоянии radius слева от черепашки — не там, где сама черепашка стоит</figcaption>'
        '</figure>'
    )
    positive = turtle_output(
        "07-13-circle-positive", "krug_polozhitelnyj.py",
        caption="circle(80) — положительный радиус, против часовой стрелки",
        alt="Окружность, нарисованная фиолетовым цветом против часовой стрелки",
    )
    negative = turtle_output(
        "07-13-circle-negative", "krug_otricatelnyj.py",
        caption="circle(-80) — тот же радиус по модулю, но по часовой стрелке",
        alt="Окружность того же размера, нарисованная розовым цветом по часовой стрелке",
    )
    body = f"""
    <p><code class="inline">circle()</code> выглядит как одна простая команда, но за ней стоит
    настоящая геометрия — разберём её по-настоящему, а не как «магическую» функцию.</p>

    <h2>Где на самом деле центр</h2>
    <p>Официальное поведение <code class="inline">circle(radius)</code>: центр окружности
    находится на расстоянии <code class="inline">radius</code> <strong>слева</strong> от
    черепашки (относительно направления её курса) — не в текущей позиции черепашки, как можно
    было бы подумать:</p>
{center_diagram}
{callout(
        "info",
        "Один конец дуги — там, где стоит черепашка",
        "Если нарисовать не полную окружность, а дугу (<code class=\"inline\">extent</code> "
        "меньше 360°) — одним из концов дуги всегда будет текущая позиция черепашки. Это "
        "удобно: не нужно заранее вычислять, откуда начнётся дуга.",
    )}

    <h2>Положительный и отрицательный радиус</h2>
    <p>Положительный радиус рисует окружность против часовой стрелки; отрицательный — по
    часовой, с тем же радиусом по модулю:</p>
    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div style="flex:1 1 280px">{positive}</div>
      <div style="flex:1 1 280px">{negative}</div>
    </div>
{code_block("napravlenie_kod.py", "artist.circle(80)    # против часовой стрелки\nartist.circle(-80)   # по часовой стрелке — тот же размер, другое направление\n")}
{callout(
        "tip",
        "Направление меняет и курс черепашки в конце",
        "После полной окружности курс черепашки возвращается к исходному в обоих случаях. Но "
        "если рисовать дугу (не полный круг), финальный курс будет РАЗНЫМ для положительного и "
        "отрицательного радиуса — черепашка развернётся в противоположные стороны.",
    )}

{practice_card(
        "07-13",
        "Практика: геометрия окружности",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-13/index.html",
    )}
    """
    out = render_page(
        page_title="Геометрия окружности",
        description="Где находится центр окружности относительно черепашки, и как положительный/отрицательный радиус меняет направление рисования.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Геометрия окружности", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Геометрия окружности",
        lede="circle() — не магия: у неё есть точная геометрия, которую полезно понимать, а не "
        "просто запомнить как заклинание.",
        body_html=body,
        sidebar_groups=sidebar("07-13-geometriya-okruzhnosti.html"),
        nav=PageNav(prev_href="07-03-figury-bez-linij.html", prev_label="Фигуры, окружности, точки", next_href="07-04-dugi.html", next_label="Дуги"),
    )
    write("07-13-geometriya-okruzhnosti.html", out)


def build_04_dugi() -> None:
    arcs = turtle_output(
        "07-04-arcs-labeled", "dugi_podpisannye.py",
        caption="Пять дуг одного радиуса, но разного extent — от 60° до полной окружности 360°",
        alt="Пять цветных дуг разной длины, выходящих из одной точки, каждая подписана своим значением extent в градусах",
    )
    body = f"""
    <p><strong>Дуга</strong> — это часть окружности. У <code class="inline">circle()</code>
    есть второй, необязательный аргумент <code class="inline">extent</code> — сколько градусов
    окружности нужно нарисовать.</p>

    <h2>От четверти до полного круга</h2>
{arcs}
{code_block(
        "dugi_kod.py",
        'arcs = [(60, "#5B24F9"), (90, "#DB2777"), (180, "#059669"), (270, "#D97706"), (360, "#0D0230")]\n'
        'for extent, color in arcs:\n'
        '    artist.pencolor(color)\n'
        '    artist.circle(90, extent)\n',
    )}
{comparison_table(
        ["extent", "Что рисуется"],
        [
            ["90°", "четверть окружности"],
            ["180°", "половина окружности (полукруг)"],
            ["270°", "три четверти окружности"],
            ["360° (или не указан)", "полная окружность"],
        ],
    )}
{callout(
        "tip",
        "Полукруг + прямая = купол",
        "Комбинируя дугу с обычной линией, легко получить составные фигуры — например, "
        "полукруглый купол домика или арку. Мы используем именно такую дугу в мини-проекте "
        "«смайлик» в конце главы — улыбка окажется дугой в 120°.",
    )}

{local_required_card(
        "07-04",
        "Практика: дуги разного размера",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-04/index.html",
    )}
    """
    out = render_page(
        page_title="Дуги",
        description="Рисуем части окружности с помощью параметра extent команды circle() — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Дуги", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Дуги",
        lede="circle() умеет рисовать не только полные окружности, но и их части — дуги "
        "заданного размера.",
        body_html=body,
        sidebar_groups=sidebar("07-04-dugi.html"),
        nav=PageNav(prev_href="07-13-geometriya-okruzhnosti.html", prev_label="Геометрия окружности", next_href="07-14-circle-steps.html", next_label="circle(steps=...)"),
    )
    write("07-04-dugi.html", out)


def build_14_circle_steps() -> None:
    s3 = turtle_output(
        "07-14-steps-3", "steps_3.py",
        caption="circle(80, steps=3) — окружность, приближённая треугольником",
        alt="Треугольник, вписанный в невидимую окружность радиусом 80",
    )
    s4 = turtle_output(
        "07-14-steps-4", "steps_4.py",
        caption="circle(80, steps=4) — тот же радиус, но 4 стороны вместо 3",
        alt="Квадрат, вписанный в невидимую окружность радиусом 80",
    )
    s6 = turtle_output(
        "07-14-steps-6", "steps_6.py",
        caption="circle(80, steps=6) — 6 сторон, уже больше похоже на окружность",
        alt="Правильный шестиугольник, вписанный в невидимую окружность радиусом 80",
    )
    body = f"""
    <p>Вот секрет, который многое объясняет: <code class="inline">circle()</code> на самом деле
    <strong>не</strong> умеет рисовать идеальную окружность — она приближает её правильным
    многоугольником со множеством маленьких сторон. Третий аргумент,
    <code class="inline">steps</code>, позволяет управлять числом этих сторон явно.</p>

    <h2>От треугольника до шестиугольника — тот же радиус</h2>
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div style="flex:1 1 220px">{s3}</div>
      <div style="flex:1 1 220px">{s4}</div>
      <div style="flex:1 1 220px">{s6}</div>
    </div>
{code_block("circle_steps_kod.py", "artist.circle(80, steps=3)   # треугольник\nartist.circle(80, steps=4)   # квадрат\nartist.circle(80, steps=6)   # шестиугольник\n")}
{callout(
        "info",
        "Мост к формуле 360/n из главы 6",
        "Это та же самая идея правильного многоугольника, что мы строили вручную в главе 6 "
        "через <code class=\"inline\">forward()</code>/<code class=\"inline\">right(360 / n)</code>. "
        "<code class=\"inline\">circle(radius, steps=n)</code> — просто более короткий способ "
        "получить тот же результат, если известен нужный радиус описанной окружности.",
    )}
{callout(
        "tip",
        "А если steps не указан?",
        "Если <code class=\"inline\">steps</code> не задан, Turtle сам подбирает достаточно "
        "большое число сторон, чтобы многоугольник выглядел гладкой окружностью — обычно "
        "несколько десятков. Мы просто не замечаем, что это тоже многоугольник.",
    )}

{practice_card(
        "07-14",
        "Практика: circle(steps=...) как многоугольник",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-14/index.html",
    )}
{practice_card(
        "07-24",
        "Практика: предскажите многоугольник по steps (без Turtle)",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/07-24/index.html",
    )}
    """
    out = render_page(
        page_title="circle(steps=...) — от круга к многоугольнику",
        description="circle() на самом деле рисует вписанный многоугольник — steps управляет числом его сторон. Мост к формуле 360/n из главы 6.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("circle(steps=...)", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="circle(steps=...) — от круга к многоугольнику",
        lede="Секрет circle(): под капотом это всегда многоугольник — просто иногда с очень "
        "большим числом сторон.",
        body_html=body,
        sidebar_groups=sidebar("07-14-circle-steps.html"),
        nav=PageNav(prev_href="07-04-dugi.html", prev_label="Дуги", next_href="07-05-eshche-vozmozhnosti.html", next_label="Штампы и другие приёмы"),
    )
    write("07-14-circle-steps.html", out)


def build_05_shtampy() -> None:
    stamps = turtle_output(
        "07-05-stamps", "shtampy.py",
        caption="stamp() шесть раз подряд — оставляет отпечаток формы, не рисуя линию между ними",
        alt="Шесть одинаковых фиолетовых кружков-штампов в ряд, без соединяющей их линии",
    )
    clearstamps = turtle_output(
        "07-05-clearstamps", "clearstamp.py",
        caption="Те же шесть штампов, но три из них удалены через clearstamp(id)",
        alt="Три оставшихся фиолетовых кружка-штампа из первоначальных шести, промежутки между удалёнными штампами пустые",
    )
    body = f"""
    <h2>Штамп — это не линия и не курсор</h2>
    <p><code class="inline">stamp()</code> оставляет отпечаток текущей формы черепашки на
    экране, не рисуя линию — важное отличие от обычного движения. Полезно для множества
    одинаковых объектов на экране (звёзд неба, врагов в игре, отметок на графике).</p>
{stamps}
{code_block("shtampy_kod.py", 'artist.shape("circle")\nartist.color("#5B24F9")\nartist.penup()\n\nfor _ in range(6):\n    artist.stamp()\n    artist.forward(60)\n')}
{callout(
        "info",
        "stamp() возвращает номер — запомните его",
        "Каждый вызов <code class=\"inline\">stamp()</code> возвращает целое число — "
        "идентификатор именно этого штампа. Без него нельзя удалить конкретный штамп позже.",
    )}

    <h2>Удаляем конкретные штампы</h2>
{clearstamps}
{code_block(
        "clearstamp_kod.py",
        'stamp_ids = []\nfor _ in range(6):\n    stamp_ids.append(artist.stamp())\n    artist.forward(60)\n\n'
        'artist.clearstamp(stamp_ids[0])\nartist.clearstamp(stamp_ids[2])\nartist.clearstamp(stamp_ids[4])\n',
    )}
{comparison_table(
        ["Команда", "Что делает"],
        [
            ["<code class=\"inline\">clearstamp(id)</code>", "удаляет ОДИН конкретный штамп по его номеру"],
            ["<code class=\"inline\">clearstamps(n)</code>", "удаляет первые n штампов (или последние n, если n отрицательное)"],
            ["<code class=\"inline\">clearstamps()</code>", "удаляет ВСЕ штампы черепашки"],
        ],
    )}

    <h2>Скрыть и показать черепашку</h2>
{code_block("skryt.py", "artist.hideturtle()   # спрятать указатель черепашки (сама линия останется)\nartist.showturtle()   # показать обратно\n")}
{callout(
        "tip",
        "Зачем прятать черепашку?",
        "В готовых рисунках указатель черепашки может визуально мешать. "
        "<code class=\"inline\">hideturtle()</code> в конце программы делает финальный "
        "результат чище — мы используем это во всех мини-проектах главы.",
    )}

    <h2>Отмена последнего действия: <code class="inline">undo()</code></h2>
{code_block("undo.py", "artist.forward(100)\nartist.undo()   # отменяет последнее движение, как Ctrl+Z\n")}

{local_required_card(
        "07-03",
        "Практика: включает штампы и другие приёмы",
        "Тот же ноутбук, что и в разделе «Фигуры, окружности, точки» — он охватывает и эту тему",
        "../../practice/07-03/index.html",
    )}
    """
    out = render_page(
        page_title="Штампы и другие приёмы",
        description="stamp(), clearstamp(), clearstamps(), hideturtle()/showturtle() и undo() в модуле turtle — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Штампы", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Штампы и другие приёмы",
        lede="stamp() — новая идея: отпечаток формы черепашки без движения и без линии.",
        body_html=body,
        sidebar_groups=sidebar("07-05-eshche-vozmozhnosti.html"),
        nav=PageNav(prev_href="07-14-circle-steps.html", prev_label="circle(steps=...)", next_href="07-06-tekst-na-ekrane.html", next_label="Текст на экране"),
    )
    write("07-05-eshche-vozmozhnosti.html", out)


def build_06_tekst() -> None:
    write_basic = turtle_output(
        "07-06-write-basic", "tekst_bazovyj.py",
        caption="write() выводит текст в текущей позиции черепашки",
        alt="Текст «Привет, Turtle!» шрифтом Arial размером 20, выведенный на белом фоне",
    )
    body = f"""
    <p>Turtle умеет не только рисовать линии, но и выводить текст прямо на холсте — командой
    <code class="inline">write()</code>.</p>
{write_basic}
{code_block("tekst_bazovyj_kod.py", 'artist.write("Привет, Turtle!", font=("Arial", 20, "normal"))\n')}
    <p>Параметр <code class="inline">font</code> — это набор из трёх значений вместе: название
    шрифта, размер и начертание (<code class="inline">"normal"</code>,
    <code class="inline">"bold"</code> или <code class="inline">"italic"</code>). Такую
    группировку нескольких значений в одно (<em>кортеж</em>) мы разберём формально в главе про
    коллекции — пока достаточно писать её по образцу, как в примере.</p>
{callout(
        "tip",
        "Текст появляется от текущей позиции",
        "<code class=\"inline\">write()</code> не двигает черепашку и не поднимает/опускает "
        "перо — он просто печатает текст, начиная от текущей координаты. Чтобы разместить "
        "текст в конкретном месте, сначала переместитесь туда через "
        "<code class=\"inline\">goto()</code> (обычно с <code class=\"inline\">penup()</code>, "
        "чтобы не провести лишнюю линию).",
    )}

{local_required_card(
        "07-06",
        "Практика: write() и параметры шрифта",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-06/index.html",
    )}
    """
    out = render_page(
        page_title="Рисуем текст на экране",
        description="Команда write() для вывода текста на холсте Turtle — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Текст на экране", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Рисуем текст на экране",
        lede="Turtle умеет не только линии — научим её подписывать собственные рисунки.",
        body_html=body,
        sidebar_groups=sidebar("07-06-tekst-na-ekrane.html"),
        nav=PageNav(prev_href="07-05-eshche-vozmozhnosti.html", prev_label="Штампы", next_href="07-15-vyravnivanie-i-shrift.html", next_label="Выравнивание и шрифт"),
    )
    write("07-06-tekst-na-ekrane.html", out)


def build_15_vyravnivanie() -> None:
    align = turtle_output(
        "07-15-align", "vyravnivanie.py",
        caption="Одна и та же точка (0, y), три разных align — текст растёт в разные стороны от неё",
        alt="Три строки текста (left, center, right), каждая выровнена по-своему относительно отмеченной точки в начале строки",
    )
    font = turtle_output(
        "07-15-font", "shrift.py",
        caption="Два разных шрифта и размера — тот же метод write(), другие параметры font",
        alt="Две строки текста разного размера: маленький обычный текст и крупный жирный текст",
    )
    body = f"""
    <p>У <code class="inline">write()</code> есть два параметра, которые превращают текст из
    подписи «куда получится» в управляемый элемент интерфейса — важно для меток и подписей.</p>

    <h2>align — откуда растёт текст</h2>
    <p>Точка, куда мы переместили черепашку — это не всегда начало текста. Параметр
    <code class="inline">align</code> определяет, как текст расположен ОТНОСИТЕЛЬНО этой
    точки:</p>
{align}
{code_block("vyravnivanie_kod.py", 'for y, align, text in [(60, "left", "left"), (0, "center", "center"), (-60, "right", "right")]:\n    artist.goto(0, y)\n    artist.dot(6, "#5B24F9")\n    artist.write(text, align=align, font=("Arial", 16, "normal"))\n')}
{comparison_table(
        ["align", "Где точка относительно текста"],
        [
            ["<code class=\"inline\">\"left\"</code> (по умолчанию)", "точка — начало текста, текст растёт вправо"],
            ["<code class=\"inline\">\"center\"</code>", "точка — центр текста"],
            ["<code class=\"inline\">\"right\"</code>", "точка — конец текста, текст растёт влево"],
        ],
    )}

    <h2>font — размер и начертание</h2>
{font}
{code_block("shrift_kod.py", 'artist.write("Arial 12 normal", font=("Arial", 12, "normal"))\nartist.write("Arial 26 bold", font=("Arial", 26, "bold"))\n')}
{callout(
        "tip",
        "align=\"center\" — то, что нужно для подписей на графиках",
        "Когда мы подписываем деления координатной оси или центр фигуры, "
        "<code class=\"inline\">align=\"center\"</code> почти всегда выглядит аккуратнее — "
        "иначе подпись съезжает в сторону от точки, которую описывает.",
    )}

{practice_card(
        "07-15",
        "Практика: выравнивание и шрифт текста",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-15/index.html",
    )}
    """
    out = render_page(
        page_title="Выравнивание и шрифт",
        description="Параметры align и font команды write() в Turtle — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Выравнивание и шрифт", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Выравнивание и шрифт",
        lede="Текст можно не просто вывести, а управлять тем, как он растёт от точки — и как "
        "выглядит.",
        body_html=body,
        sidebar_groups=sidebar("07-15-vyravnivanie-i-shrift.html"),
        nav=PageNav(prev_href="07-06-tekst-na-ekrane.html", prev_label="Текст на экране", next_href="07-16-tekst-i-koordinaty.html", next_label="Текст и координаты"),
    )
    write("07-15-vyravnivanie-i-shrift.html", out)


def build_16_tekst_koordinaty() -> None:
    chart = turtle_output(
        "07-16-coordinate-chart", "koordinatnyj_chart.py",
        caption="Оси с числовыми подписями делений — goto(), dot() и write() вместе",
        alt="Координатная плоскость с осями X и Y, точками-делениями через каждые 50 пикселей и подписанными числами -100, -50, 0, 50, 100",
    )
    body = f"""
    <p>Соберём вместе три инструмента из этой главы — <code class="inline">goto()</code>,
    <code class="inline">dot()</code> и <code class="inline">write()</code> — и координаты из
    главы 6, чтобы получить нечто похожее на настоящий график с подписанными делениями.</p>

    <h2>Настоящий график начинается с плана</h2>
    <p>План простой: нарисовать две оси, затем в нескольких точках вдоль каждой оси поставить
    точку-деление и подписать её числом.</p>
{chart}
{code_block(
        "koordinatnyj_chart_kod.py",
        '# оси\n'
        'artist.penup(); artist.goto(-180, 0); artist.pendown(); artist.goto(180, 0)\n'
        'artist.penup(); artist.goto(0, -180); artist.pendown(); artist.goto(0, 180)\n\n'
        '# деления и подписи\n'
        'artist.penup()\n'
        'for value in [-100, -50, 50, 100]:\n'
        '    artist.goto(value, 0)\n'
        '    artist.dot(6, "#5B24F9")\n'
        '    artist.goto(value, -20)\n'
        '    artist.write(str(value), align="center", font=("Arial", 11, "normal"))\n'
        '    artist.goto(0, value)\n'
        '    artist.dot(6, "#5B24F9")\n'
        '    artist.goto(15, value)\n'
        '    artist.write(str(value), font=("Arial", 11, "normal"))\n',
    )}
{callout(
        "info",
        "Три главы в одном рисунке",
        "Эта картинка — не случайность: числа и координаты из главы 5, идея координатного мира "
        "из главы 6, и <code class=\"inline\">write()</code>/<code class=\"inline\">dot()</code> "
        "из этой главы соединились в один полезный инструмент. Мы используем эту же идею в "
        "мини-проекте «координатная мишень» в конце главы.",
    )}

{practice_card(
        "07-16",
        "Практика: текст и координатная система",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-16/index.html",
    )}
    """
    out = render_page(
        page_title="Текст и координатная система",
        description="Собираем goto(), dot() и write() в подписанную координатную плоскость — реальный выполненный результат.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Текст и координаты", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Текст и координатная система",
        lede="Три инструмента порознь — просто команды. Вместе они превращаются в подписанный "
        "координатный график.",
        body_html=body,
        sidebar_groups=sidebar("07-16-tekst-i-koordinaty.html"),
        nav=PageNav(prev_href="07-15-vyravnivanie-i-shrift.html", prev_label="Выравнивание и шрифт", next_href="07-17-forma-cherepashki.html", next_label="Черепашка как объект"),
    )
    write("07-16-tekst-i-koordinaty.html", out)


def build_17_forma() -> None:
    gallery = turtle_output(
        "07-17-shapes-gallery", "galereya_form.py",
        caption="Все встроенные формы курсора черепашки — от arrow до classic",
        alt="Шесть разных значков-курсоров черепашки в ряд: arrow, turtle, circle, square, triangle, classic — каждый подписан своим именем",
    )
    shapesize = turtle_output(
        "07-17-shapesize", "razmer_formy.py",
        caption="shapesize() растягивает вид курсора — 0.5×, 1× и 2× одной и той же формы",
        alt="Три силуэта черепахи разного размера — маленький, обычный и увеличенный вдвое",
    )
    tilt = turtle_output(
        "07-17-tilt", "naklon.py",
        caption="tilt(45) поворачивает ВИД курсора на 45°, не меняя направление движения",
        alt="Два стрелочных курсора одинакового размера — левый смотрит прямо, правый наклонён на 45 градусов",
    )
    body = f"""
    <p>До сих пор форма черепашки была для нас просто «указателем». Но у неё есть собственные
    настройки внешнего вида — размер и наклон — независимые от логики движения.</p>

    <h2>Встроенные формы</h2>
{gallery}
{code_block("galereya_form_kod.py", 'shapes = ["arrow", "turtle", "circle", "square", "triangle", "classic"]\nfor shape_name in shapes:\n    artist.shape(shape_name)\n    artist.stamp()\n')}

    <h2>shapesize() — размер курсора, не размер рисунка</h2>
{shapesize}
{code_block("razmer_formy_kod.py", 'artist.shape("turtle")\nfor factor in [0.5, 1, 2]:\n    artist.shapesize(factor, factor)\n    artist.stamp()\n')}
{callout(
        "warning",
        "shapesize() не меняет координаты",
        "Увеличенная черепашка выглядит больше, но это только внешний вид курсора — все "
        "координаты, повороты и расстояния в коде остаются точно такими же, как были.",
    )}

    <h2>tilt() — наклон вида, а не курс движения</h2>
    <p>Здесь важно различать два похожих, но разных понятия:</p>
{comparison_table(
        ["Понятие", "Что означает"],
        [
            ["<strong>heading</strong> (курс)", "куда черепашка ДВИЖЕТСЯ — это меняют left()/right()/setheading()"],
            ["<strong>tilt</strong> (наклон)", "как повёрнут ВИД курсора на экране — это меняет только tilt()/tiltangle()"],
        ],
    )}
{tilt}
{code_block("naklon_kod.py", 'artist.shape("arrow")\nartist.shapesize(3, 3)\n\nartist.stamp()          # обычный вид\n\nartist.tilt(45)          # только поворачиваем ВИД, курс движения не изменился\nartist.stamp()\n')}
{callout(
        "info",
        "Зачем это может понадобиться",
        "Представьте самолётик или машинку в игре: она может ЛЕТЕТЬ строго вправо (курс "
        "фиксирован), но слегка покачиваться визуально — это и есть разница между heading и "
        "tilt. Для базовых учебных рисунков tilt() нужен редко, но полезно знать, что курс "
        "движения и внешний вид — разные вещи.",
    )}

{local_required_card(
        "07-17",
        "Практика: черепашка как графический объект",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-17/index.html",
    )}
    """
    out = render_page(
        page_title="Черепашка как графический объект",
        description="shape(), shapesize() и tilt() — внешний вид курсора черепашки отдельно от логики движения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Черепашка как объект", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Черепашка как графический объект",
        lede="Форма, размер и наклон курсора — настройки внешнего вида, независимые от того, "
        "куда и как черепашка на самом деле движется.",
        body_html=body,
        sidebar_groups=sidebar("07-17-forma-cherepashki.html"),
        nav=PageNav(prev_href="07-16-tekst-i-koordinaty.html", prev_label="Текст и координаты", next_href="07-18-neskolko-cherepashek.html", next_label="Несколько черепашек"),
    )
    write("07-17-forma-cherepashki.html", out)


def build_18_neskolko() -> None:
    two_turtles = turtle_output(
        "07-18-two-turtles", "dve_cherepashki.py",
        caption="alice и bob — два независимых объекта Turtle на одном экране",
        alt="Два отрезка разного цвета из разных точек — фиолетовый от Alice и розовый от Bob",
    )
    diagram = (
        '<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;justify-content:center">'
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;color:#0D0230;line-height:1.9">'
        'SCREEN<br>'
        '├── alice<br>'
        '│&nbsp;&nbsp;&nbsp;&nbsp;├ position<br>'
        '│&nbsp;&nbsp;&nbsp;&nbsp;├ heading<br>'
        '│&nbsp;&nbsp;&nbsp;&nbsp;└ color<br>'
        '│<br>'
        '└── bob<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├ position<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├ heading<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ color'
        '</div></figure>'
    )
    body = f"""
    <p>Мы создавали одну черепашку на весь скрипт. Но ничто не мешает создать сразу несколько —
    у каждой будет своё, полностью независимое состояние.</p>

    <h2>Один экран, разные черепашки</h2>
{two_turtles}
{code_block(
        "dve_cherepashki_kod.py",
        'alice = turtle.Turtle()\n'
        'alice.color("#5B24F9")\n'
        'alice.penup(); alice.goto(-100, -80); alice.pendown()\n'
        'alice.setheading(70)\n'
        'alice.forward(140)\n\n'
        'bob = turtle.Turtle()\n'
        'bob.color("#DB2777")\n'
        'bob.penup(); bob.goto(100, -80); bob.pendown()\n'
        'bob.setheading(110)\n'
        'bob.forward(140)\n',
    )}
{diagram}
{callout(
        "info",
        "Своё состояние — значит, независимое поведение",
        "Изменение курса или цвета <code class=\"inline\">alice</code> НИКАК не влияет на "
        "<code class=\"inline\">bob</code> — они существуют на одном экране, но живут "
        "полностью раздельно. Это и есть суть того, что "
        "<code class=\"inline\">turtle.Turtle()</code> — не просто функция, а фабрика "
        "самостоятельных объектов.",
    )}
{code_block("sravnenie_sostoyaniya.py", "print(alice.position(), alice.heading())\nprint(bob.position(), bob.heading())\n")}
{callout(
        "tip",
        "Название для этого — впереди",
        "Позже, в главе про объектно-ориентированное программирование, мы дадим этому явлению "
        "формальное имя и разберём его гораздо глубже. Пока достаточно самого наблюдения: "
        "каждый <code class=\"inline\">Turtle()</code> — отдельный, независимый объект со "
        "своим состоянием.",
    )}

{local_required_card(
        "07-18",
        "Практика: несколько черепашек",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-18/index.html",
    )}
    """
    out = render_page(
        page_title="Несколько черепашек",
        description="Создаём несколько независимых объектов Turtle на одном экране — тихий мост к объектно-ориентированному программированию.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Несколько черепашек", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Несколько черепашек",
        lede="Один экран может держать сколько угодно черепашек — и у каждой будет своё, "
        "полностью независимое состояние.",
        body_html=body,
        sidebar_groups=sidebar("07-18-neskolko-cherepashek.html"),
        nav=PageNav(prev_href="07-17-forma-cherepashki.html", prev_label="Черепашка как объект", next_href="07-19-clone.html", next_label="clone()"),
    )
    write("07-18-neskolko-cherepashek.html", out)


def build_19_clone() -> None:
    clone_output = turtle_output(
        "07-19-clone", "clone.py",
        caption="original и copy стартуют из одной точки с одинаковым состоянием, затем расходятся",
        alt="Два отрезка, выходящих из одной общей нижней точки в разные стороны — один синий, один розовый",
    )
    body = f"""
    <p><code class="inline">clone()</code> — ещё один способ получить вторую черепашку, но
    принципиально другой: не «создать с нуля», а «скопировать состояние существующей».</p>

    <h2>Копия стартует с того же места</h2>
{clone_output}
{code_block(
        "clone_kod.py",
        'original = turtle.Turtle()\n'
        'original.color("#5B24F9")\n'
        'original.penup(); original.goto(0, -100); original.pendown()\n'
        'original.setheading(90)\n\n'
        'copy = original.clone()   # тот же цвет, та же позиция, тот же курс\n'
        'copy.color("#DB2777")     # меняем только цвет — чтобы отличить на рисунке\n\n'
        'original.left(30)\n'
        'original.forward(160)\n\n'
        'copy.right(30)\n'
        'copy.forward(160)\n',
    )}
{callout(
        "info",
        "clone() ≠ ссылка на ту же черепашку",
        "<code class=\"inline\">copy</code> — полностью НОВЫЙ, независимый объект. Он "
        "начинает с теми же позицией, курсом и настройками, что и <code class=\"inline\">original</code> "
        "в момент клонирования — но дальнейшие изменения одной черепашки никак не затрагивают "
        "другую, как мы уже видели с <code class=\"inline\">alice</code> и "
        "<code class=\"inline\">bob</code>.",
    )}
{callout(
        "tip",
        "Когда это полезно",
        "Представьте узор с несколькими одинаковыми лучами, но повёрнутыми под разными "
        "углами — вместо того, чтобы настраивать каждую черепашку с нуля, можно один раз "
        "настроить \"эталонную\" черепашку и клонировать её сколько угодно раз.",
    )}

{practice_card(
        "07-19",
        "Практика: clone() и независимые копии",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-19/index.html",
    )}
    """
    out = render_page(
        page_title="clone() — копируем состояние",
        description="clone() создаёт новую независимую черепашку с тем же стартовым состоянием, что и оригинал — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("clone()", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="clone() — копируем состояние",
        lede="Не «новая черепашка с нуля», а «точная копия существующей» — а дальше они "
        "полностью независимы.",
        body_html=body,
        sidebar_groups=sidebar("07-19-clone.html"),
        nav=PageNav(prev_href="07-18-neskolko-cherepashek.html", prev_label="Несколько черепашек", next_href="07-20-clear-reset-home.html", next_label="clear(), reset(), home()"),
    )
    write("07-19-clone.html", out)


def build_20_clear_reset_home() -> None:
    clear_out = turtle_output(
        "07-20-clear-effect", "clear_effekt.py",
        caption="После clear() рисунок исчез, но точка появилась там же, куда мы переместились ДО очистки — позиция не сбросилась",
        alt="Пустой экран с розовой точкой в правом верхнем углу и чёрным курсором черепашки рядом с ней — квадрат стёрт, но позиция черепашки осталась прежней",
    )
    reset_out = turtle_output(
        "07-20-reset-effect", "reset_effekt.py",
        caption="После reset() рисунок исчез И черепашка вернулась в (0, 0) — точка появилась в центре",
        alt="Пустой экран с розовой точкой точно в центре — квадрат стёрт, и черепашка вернулась в начало координат",
    )
    body = f"""
    <p>Три похожих по звучанию команды — но с разным эффектом. Разберём их одну за другой,
    используя ОДИН и тот же сценарий: нарисовать квадрат, отойти в сторону, затем очистить.</p>

{comparison_table(
        ["Команда", "Стирает рисунок?", "Двигает черепашку?"],
        [
            ["<code class=\"inline\">clear()</code>", "да", "нет — черепашка остаётся, где была"],
            ["<code class=\"inline\">reset()</code>", "да", "да — возвращает в (0, 0) с курсом по умолчанию"],
            ["<code class=\"inline\">home()</code>", "нет", "да — возвращает в (0, 0), но НЕ трогает рисунок"],
        ],
    )}

    <h2><code class="inline">clear()</code> — стирает рисунок, не двигает черепашку</h2>
{clear_out}
{code_block(
        "clear_effekt_kod.py",
        'for _ in range(4):\n    artist.forward(100)\n    artist.right(90)\n\n'
        'artist.penup()\n'
        'artist.goto(120, 80)\n'
        'artist.clear()\n'
        '# clear() стирает рисунок, но НЕ трогает позицию черепашки —\n'
        '# точка появится там же, куда мы её только что переместили\n'
        'artist.dot(14, "#DB2777")\n',
    )}

    <h2><code class="inline">reset()</code> — стирает рисунок И возвращает домой</h2>
{reset_out}
{code_block(
        "reset_effekt_kod.py",
        'for _ in range(4):\n    artist.forward(100)\n    artist.right(90)\n\n'
        'artist.penup()\n'
        'artist.goto(120, 80)\n'
        'artist.reset()\n'
        '# reset() стирает рисунок И возвращает черепашку в (0, 0) —\n'
        '# точка появится в начале координат, а не там, где мы были\n'
        'artist.dot(14, "#DB2777")\n',
    )}

    <h2><code class="inline">home()</code> — только движение, рисунок остаётся</h2>
    <p>Мы уже встречали <code class="inline">home()</code> в главе 6 — она перемещает
    черепашку в (0, 0) с курсом по умолчанию, но, в отличие от <code class="inline">reset()</code>,
    НЕ стирает то, что уже нарисовано:</p>
{code_block("home_kod.py", "artist.forward(100)\nartist.left(45)\nartist.forward(60)\nartist.home()   # рисунок остаётся на месте, домой возвращается только черепашка\n")}
{callout(
        "tip",
        "Как выбрать нужную команду",
        "Нужно стереть рисунок, но остаться на месте? <code class=\"inline\">clear()</code>. "
        "Нужно полностью начать заново — и рисунок, и позицию? "
        "<code class=\"inline\">reset()</code>. Нужно просто вернуться в центр, ничего не "
        "стирая? <code class=\"inline\">home()</code>.",
    )}

{local_required_card(
        "07-20",
        "Практика: clear, reset, home",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-20/index.html",
    )}
{practice_card(
        "07-25",
        "Практика: предскажите эффект clear/reset/home (без Turtle)",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/07-25/index.html",
    )}
    """
    out = render_page(
        page_title="clear(), reset() и home()",
        description="Три похожие команды Turtle с разным эффектом на рисунок и позицию черепашки — с реальным выполненным результатом каждой.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("clear, reset, home", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="clear(), reset() и home()",
        lede="Три похожие по звучанию команды — но каждая стирает и двигает что-то своё.",
        body_html=body,
        sidebar_groups=sidebar("07-20-clear-reset-home.html"),
        nav=PageNav(prev_href="07-19-clone.html", prev_label="clone()", next_href="07-23-otladka-grafiki.html", next_label="Отладка графики"),
    )
    write("07-20-clear-reset-home.html", out)


def build_23_otladka() -> None:
    body = f"""
    <p>Графика добавляет несколько новых, специфичных для более продвинутого Turtle способов
    что-то сделать не так — разберём их по схеме «симптом → причина → исправление».</p>

{comparison_table(
        ["Симптом", "Причина", "Исправление"],
        [
            [
                "Окружность рисуется не в ту сторону, чем ожидалось",
                "Радиус имеет не тот знак — положительный вместо отрицательного или наоборот",
                "Проверьте знак: положительный радиус — против часовой стрелки, отрицательный — по",
            ],
            [
                "Текст появился совсем не там, где ожидалось",
                "Забыли переместить черепашку через <code class=\"inline\">goto()</code>/"
                "<code class=\"inline\">penup()</code> перед <code class=\"inline\">write()</code> — "
                "текст выводится от ТЕКУЩЕЙ позиции",
                "Переместитесь в нужную точку до вызова <code class=\"inline\">write()</code>",
            ],
            [
                "Заливка не закрасилась, хотя fillcolor() был задан",
                "Контур между <code class=\"inline\">begin_fill()</code> и "
                "<code class=\"inline\">end_fill()</code> не замкнулся — черепашка не "
                "вернулась в стартовую точку",
                "Проверьте, что путь образует ЗАМКНУТУЮ фигуру — конец совпадает с началом",
            ],
            [
                "RGB-цвет вызывает ошибку вроде «недопустимое значение цвета»",
                "Числа не соответствуют текущему <code class=\"inline\">colormode</code> — "
                "например, <code class=\"inline\">(255, 0, 0)</code> при "
                "<code class=\"inline\">colormode(1.0)</code>",
                "Сверьте числа с активным режимом — 0–255 или 0.0–1.0",
            ],
            [
                "Код выполняется без ошибок, но на экране совсем ничего не появилось",
                "Вызван <code class=\"inline\">screen.tracer(0)</code>, но забыт "
                "<code class=\"inline\">screen.update()</code> — экран так и не обновился ни разу",
                "Добавьте <code class=\"inline\">screen.update()</code> после всех команд рисования",
            ],
            [
                "На экране остался штамп, хотя казалось, что он должен был исчезнуть",
                "<code class=\"inline\">clearstamp()</code> вызван с неверным id, либо "
                "id вообще не был сохранён при вызове <code class=\"inline\">stamp()</code>",
                "Сохраняйте id каждого stamp() в переменную/список сразу при создании",
            ],
            [
                "Две черепашки двигаются одинаково, хотя должны были разойтись",
                "Обе переменные на самом деле ссылаются на ОДНУ и ту же черепашку "
                "(например, <code class=\"inline\">bob = alice</code> вместо "
                "<code class=\"inline\">bob = turtle.Turtle()</code>)",
                "Создавайте каждую черепашку отдельным вызовом "
                "<code class=\"inline\">turtle.Turtle()</code> или через "
                "<code class=\"inline\">clone()</code>",
            ],
            [
                "Курсор черепашки выглядит повёрнутым не в ту сторону, хотя движется верно",
                "Спутаны <code class=\"inline\">heading</code> (направление движения) и "
                "<code class=\"inline\">tilt</code> (визуальный поворот курсора) — они "
                "независимы",
                "heading меняют left()/right()/setheading(); внешний вид — только tilt()/tiltangle()",
            ],
            [
                "Часть рисунка не видна, хотя код точно её рисует",
                "Координаты вышли за пределы окна — оно не бесконечное",
                "Проверьте <code class=\"inline\">screen.setup()</code>/<code class=\"inline\">screensize()</code> "
                "и держите координаты в пределах видимой области",
            ],
        ],
    )}

    <h2><code class="inline">tracer(0)</code> без <code class="inline">update()</code> — разберём подробно</h2>
    <p>Это настолько частая и настолько незаметная ошибка, что заслуживает отдельного разбора.
    Программа выполняется полностью, без единой ошибки — но экран остаётся девственно пустым:</p>
{code_block("tracer_bug.py", "screen.tracer(0)\n\nfor _ in range(4):\n    artist.forward(100)\n    artist.right(90)\n\n# если здесь нет screen.update() — окно так и останется пустым!\n")}
{callout(
        "warning",
        "Мысленная модель",
        "<code class=\"inline\">tracer(0)</code> — это не «выключить рисование», а «не "
        "показывать его на экране, пока не попросят». Рисование продолжает происходить "
        "по-настоящему, просто оно невидимо, пока не вызван <code class=\"inline\">update()</code>.",
    )}

{practice_card(
        "07-23",
        "Практика: отладка графики (без Turtle)",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/07-23/index.html",
    )}
    """
    out = render_page(
        page_title="Отладка графики",
        description="Частые проблемы продвинутой графики Turtle: направление окружности, tracer без update, colormode-конфликты, спутанные черепашки — симптом, причина, исправление.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Отладка графики", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Отладка графики",
        lede="Более продвинутая графика добавляет новые, специфичные способы ошибиться — "
        "разберём их по схеме «симптом → причина → исправление».",
        body_html=body,
        sidebar_groups=sidebar("07-23-otladka-grafiki.html"),
        nav=PageNav(prev_href="07-20-clear-reset-home.html", prev_label="clear, reset, home", next_href="07-07-mini-proekt-okruzhnost-kvadrat.html", next_label="Мини-проект: окружность в квадрате"),
    )
    write("07-23-otladka-grafiki.html", out)


def build_07_okruzhnost_v_kvadrate() -> None:
    final = turtle_output(
        "07-07-circle-inscribed", "okruzhnost_v_kvadrate.py",
        caption="Готовый результат: квадрат со стороной 150 и вписанная в него окружность",
        alt="Синий квадрат со стороной 150 пикселей и розовая окружность, вписанная точно внутри него",
    )
    plan = turtle_output(
        "07-07-square-plan", "kvadrat_plan.py",
        caption="Шаг 1 — сначала просто квадрат, без окружности",
        alt="Один синий квадрат со стороной 150 пикселей, без каких-либо других фигур",
    )
    concentric = turtle_output(
        "07-07-challenge-concentric", "koncentricheskie.py",
        caption="Задание-вызов: несколько окружностей одна в другой вместо одной",
        alt="Тот же квадрат с тремя разноцветными концентрическими окружностями внутри вместо одной",
    )
    body = f"""
    <h2>Что мы построим</h2>
{final}

    <h2>Разложим на части</h2>
    <p>Прежде чем писать код, разберём рисунок на простые фигуры: квадрат со стороной
    <code class="inline">razmer</code>, и окружность радиусом <code class="inline">razmer / 2</code>,
    вписанная точно по центру.</p>

    <h2>Координатный план</h2>
    <p>Чтобы окружность идеально вписалась в квадрат, её нужно начать рисовать из точки на
    полпути вдоль нижней стороны квадрата — не из угла и не из центра:</p>
{comparison_table(
        ["Что рисуем", "Откуда начинаем", "Курс в начале"],
        [
            ["Квадрат", "нижний левый угол: (-razmer/2, -razmer/2)", "0° (вправо)"],
            ["Окружность", "середина нижней стороны: (0, -razmer/2)", "0° (вправо)"],
        ],
    )}

    <h2>Шаг 1: только квадрат</h2>
{plan}
{code_block(
        "kvadrat_plan_kod.py",
        'razmer = 150\n'
        'artist.penup()\n'
        'artist.goto(-razmer / 2, -razmer / 2)\n'
        'artist.pendown()\n'
        'for _ in range(4):\n'
        '    artist.forward(razmer)\n'
        '    artist.left(90)\n',
    )}

    <h2>Шаг 2: добавляем вписанную окружность</h2>
{code_block(
        "okruzhnost_v_kvadrate_kod.py",
        'artist.pencolor("#DB2777")\n'
        'artist.penup()\n'
        'artist.goto(0, -razmer / 2)\n'
        'artist.setheading(0)\n'
        'artist.pendown()\n'
        'artist.circle(razmer / 2)\n',
    )}
{callout(
        "info",
        "Откуда взялась эта точка",
        "Радиус вписанной окружности — ровно половина стороны квадрата. А центр окружности "
        "находится слева от черепашки (см. раздел «Геометрия окружности») — значит, чтобы "
        "центр совпал с центром квадрата, черепашка должна начать рисовать РОВНО из точки на "
        "нижней стороне, на расстоянии radius от центра.",
    )}

    <h2>Задание-вызов</h2>
{concentric}
{exercise(2, "Свой набор колец", "Измените код так, чтобы получить свой набор концентрических окружностей — другие радиусы, другие цвета.")}
{exercise(2, "Окружность в шестиугольнике", "Замените квадрат на шестиугольник из главы 6 и впишите в него окружность подходящего радиуса.")}
{exercise(3, "Толстый контур", "Увеличьте pensize() квадрата и окружности — как меняется восприятие фигуры?")}

{local_required_card(
        "07-07",
        "Практика: вписанная окружность",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-07/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — окружность внутри квадрата",
        description="Профессиональная версия: геометрический план, пошаговая сборка и вызовы для комбинации квадрата и вписанной окружности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Окружность в квадрате", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Мини-проект — окружность внутри квадрата",
        lede="Результат сначала, план потом, шаги по одному — учимся строить композицию из "
        "фигур осознанно, а не методом подбора.",
        body_html=body,
        sidebar_groups=sidebar("07-07-mini-proekt-okruzhnost-kvadrat.html"),
        nav=PageNav(prev_href="07-23-otladka-grafiki.html", prev_label="Отладка графики", next_href="07-08-napravlenie-risovaniya.html", next_label="Направление рисования"),
    )
    write("07-07-mini-proekt-okruzhnost-kvadrat.html", out)


def build_08_napravlenie() -> None:
    cw_ccw = turtle_output(
        "07-08-cw-ccw", "cw_ccw.py",
        caption="Против часовой (радиус положительный) и по часовой (радиус отрицательный) — рядом, для прямого сравнения",
        alt="Две окружности рядом, каждая со стрелкой направления — левая подписана «против часовой (+)», правая «по часовой (-)»",
    )
    body = f"""
    <p>Мы уже разобрали геометрию окружности подробно в начале главы. Здесь соберём три связанные
    идеи вместе — направление рисования, знак радиуса и режим измерения углов — и закрепим их
    перед финальными мини-проектами.</p>

    <h2>По часовой или против — определяет знак радиуса</h2>
{cw_ccw}
{code_block("cw_ccw_kod.py", "artist.circle(60)    # против часовой стрелки — положительный радиус\nartist.circle(-60)   # по часовой стрелке — отрицательный радиус\n")}

    <h2>Режимы измерения углов</h2>
    <p>По умолчанию Turtle измеряет углы в градусах. Если по какой-то причине удобнее работать
    в радианах (например, для совместимости с формулами из модуля <code class="inline">math</code>
    из главы 5) — есть команды <code class="inline">degrees()</code> и
    <code class="inline">radians()</code>:</p>
{code_block("radiany.py", "import math\n\nartist.radians()\nartist.left(math.pi / 2)   # поворот на 90°, выраженный в радианах\n\nartist.degrees()            # возвращаемся к привычным градусам\n")}
{callout(
        "warning",
        "Не забудьте вернуться в градусы",
        "Если вызвать <code class=\"inline\">radians()</code> и забыть "
        "<code class=\"inline\">degrees()</code> в конце — все последующие повороты в "
        "программе будут интерпретироваться как радианы, а не градусы, что почти всегда "
        "приводит к неожиданным результатам.",
    )}

{practice_revisit_card(
        "07-07",
        "Практика: включает практику с направлением рисования",
        "Тот же ноутбук, что и в разделе «Окружность в квадрате» — он охватывает и эту тему",
        "../../practice/07-07/index.html",
    )}
    """
    out = render_page(
        page_title="Меняем направление рисования",
        description="Направление рисования окружности (по/против часовой стрелки) и режимы измерения углов — сводим воедино.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Направление рисования", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Меняем направление рисования",
        lede="Направление, знак радиуса и режим измерения углов — три связанные идеи, "
        "собранные вместе перед финальными мини-проектами.",
        body_html=body,
        sidebar_groups=sidebar("07-08-napravlenie-risovaniya.html"),
        nav=PageNav(prev_href="07-07-mini-proekt-okruzhnost-kvadrat.html", prev_label="Окружность в квадрате", next_href="07-21-mini-proekt-chasy.html", next_label="Мини-проект: часы"),
    )
    write("07-08-napravlenie-risovaniya.html", out)


def build_21_chasy() -> None:
    final = turtle_output(
        "07-21-clock-full", "chasy_polnye.py",
        caption="Готовый результат: циферблат с делениями, числами 12/3/6/9 и двумя стрелками",
        alt="Циферблат аналоговых часов с делениями на 12 часов, числами 12, 3, 6, 9 и двумя стрелками, показывающими фиксированное время",
    )
    marks = turtle_output(
        "07-21-clock-marks", "chasy_delenia.py",
        caption="Шаг 1 — окружность и 12 делений, без чисел и стрелок",
        alt="Круглый циферблат с двенадцатью короткими штрихами-делениями по кругу, без цифр и стрелок",
    )
    body = f"""
    <h2>Что мы построим</h2>
    <p>«Часы без времени» — статичный циферблат аналоговых часов. Модуль
    <code class="inline">datetime</code> нам пока не нужен — стрелки встанут на фиксированный
    угол, просто чтобы показать, как из геометрии собирается узнаваемый объект.</p>
{final}

    <h2>Геометрический план</h2>
    <p>12 делений циферблата расположены по кругу через равные промежутки — знакомая формула
    <code class="inline">360 / 12 = 30</code> градусов между соседними часами. Но в отличие от
    обычного многоугольника, здесь удобнее задавать угол каждого деления АБСОЛЮТНО, через
    <code class="inline">setheading()</code>, а не накапливать поворотами:</p>
{code_block(
        "ugol_deleniya.py",
        "# час 0 (12 часов) — направление вверх, 90°\n"
        "# час 3            — направление вправо, 0°\n"
        "# час 6            — направление вниз, -90°\n"
        "# час 9            — направление влево, 180°\n"
        "# в общем виде: ugol = 90 - hour * 30\n",
    )}

    <h2>Шаг 1: окружность и деления</h2>
{marks}
{code_block(
        "chasy_delenia_kod.py",
        'artist.circle(150)\n\n'
        'for hour in range(12):\n'
        '    artist.penup()\n'
        '    artist.goto(0, 0)\n'
        '    artist.setheading(90 - hour * 30)\n'
        '    artist.forward(135)\n'
        '    artist.pendown()\n'
        '    artist.forward(15)\n'
        '    artist.penup()\n',
    )}
{callout(
        "info",
        "Почему goto(0, 0) перед каждым делением",
        "Каждое деление начинается заново от центра — иначе черепашка рисовала бы деления одно "
        "за другим по кругу, а не как независимые лучи от центра. penup()/pendown() вокруг "
        "каждого шага гарантирует, что линии между делениями не будет.",
    )}

    <h2>Шаг 2: числа и стрелки</h2>
{code_block(
        "chasy_chisla_strelki_kod.py",
        'for hour, label in [(0, "12"), (3, "3"), (6, "6"), (9, "9")]:\n'
        '    artist.goto(0, 0)\n'
        '    artist.setheading(90 - hour * 30)\n'
        '    artist.forward(110)\n'
        '    artist.write(label, align="center", font=("Arial", 16, "bold"))\n\n'
        '# часовая стрелка — короче, толще, фиксирована на 12\n'
        'artist.pensize(5)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.goto(0, 0)\n'
        'artist.setheading(90 - 12 * 30)\n'
        'artist.pendown()\n'
        'artist.forward(80)\n'
        'artist.penup()\n\n'
        '# минутная стрелка — длиннее, тоньше, фиксирована на 2\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#DB2777")\n'
        'artist.goto(0, 0)\n'
        'artist.setheading(90 - 2 * 30)\n'
        'artist.pendown()\n'
        'artist.forward(120)\n',
    )}

    <h2>Готовый результат</h2>
{final}

{exercise(1, "Все 12 чисел", "Добавьте оставшиеся 8 чисел (1, 2, 4, 5, 7, 8, 10, 11) по тому же принципу.")}
{exercise(2, "Секундная стрелка", "Добавьте третью, самую тонкую стрелку — секундную — на любой фиксированный угол.")}
{exercise(3, "Другое время", "Измените углы часовой и минутной стрелки, чтобы часы показывали другое (тоже фиксированное) время.")}

{local_required_card(
        "07-21",
        "Практика: часы без времени",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-21/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — часы без времени",
        description="Строим статичный циферблат аналоговых часов: деления, числа и стрелки — геометрия, а не datetime.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Часы без времени", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Мини-проект — часы без времени",
        lede="Узнаваемый циферблат — просто геометрия: деления через равные углы, числа, две "
        "стрелки на фиксированных направлениях.",
        body_html=body,
        sidebar_groups=sidebar("07-21-mini-proekt-chasy.html"),
        nav=PageNav(prev_href="07-08-napravlenie-risovaniya.html", prev_label="Направление рисования", next_href="07-22-mini-proekt-mishen.html", next_label="Мини-проект: мишень"),
    )
    write("07-21-mini-proekt-chasy.html", out)


def build_22_mishen() -> None:
    final = turtle_output(
        "07-22-target-infographic", "koordinatnaya_mishen.py",
        caption="Готовый результат: концентрическая мишень, перекрестье осей, случайные точки-попадания и подпись",
        alt="Мишень из красных и белых концентрических колец с чёрным перекрестьем осей, шестью зелёными точками-попаданиями и заголовком «Координатная мишень»",
    )
    body = f"""
    <h2>Что мы построим</h2>
{final}
    <p>Полноценная небольшая инфографика — не просто мишень, а мишень С осями координат, точками
    «попаданий» и подписью. Соберём её из того, что уже знаем: концентрические окружности с
    заливкой, оси через <code class="inline">goto()</code>, случайные точки из главы 6 и
    подпись через <code class="inline">write()</code>.</p>

    <h2>Разложим на слои</h2>
{comparison_table(
        ["Слой", "Из чего состоит", "Что уже знакомо"],
        [
            ["Кольца мишени", "4 закрашенные окружности убывающего радиуса", "begin_fill()/circle()/end_fill()"],
            ["Перекрестье", "две линии через центр", "goto() из главы 6"],
            ["Точки попаданий", "случайные координаты", "random + dot() из главы 6"],
            ["Подпись", "текст в углу", "write() из этой главы"],
        ],
    )}

    <h2>Код целиком</h2>
{code_block(
        "koordinatnaya_mishen_kod.py",
        'import random\n\n'
        'random.seed(4)   # фиксированный seed — точки одинаковые при каждом запуске\n\n'
        '# кольца мишени\n'
        'rings = [(140, "#DC2626"), (100, "#FAFAFC"), (60, "#DC2626"), (20, "#FAFAFC")]\n'
        'for radius, color in rings:\n'
        '    artist.penup()\n'
        '    artist.goto(0, -radius)\n'
        '    artist.pendown()\n'
        '    artist.fillcolor(color)\n'
        '    artist.begin_fill()\n'
        '    artist.circle(radius)\n'
        '    artist.end_fill()\n\n'
        '# перекрестье осей\n'
        'artist.penup(); artist.goto(-160, 0); artist.pendown(); artist.goto(160, 0)\n'
        'artist.penup(); artist.goto(0, -160); artist.pendown(); artist.goto(0, 160)\n\n'
        '# случайные точки попаданий\n'
        'artist.penup()\n'
        'for _ in range(6):\n'
        '    x = random.randint(-120, 120)\n'
        '    y = random.randint(-120, 120)\n'
        '    artist.goto(x, y)\n'
        '    artist.dot(10, "#059669")\n\n'
        '# подпись\n'
        'artist.goto(-190, 170)\n'
        'artist.write("Координатная мишень", font=("Arial", 13, "bold"))\n',
    )}
{callout(
        "tip",
        "Почему random.seed(4)",
        "Как и в главе 6, фиксированный seed делает картинку воспроизводимой — при каждом "
        "запуске точки окажутся ровно там же. Уберите эту строку, чтобы получить новый набор "
        "точек при каждом запуске.",
    )}

{exercise(2, "Подпись координат", "Рядом с каждой точкой попадания добавьте write() с её координатами.")}
{exercise(3, "Счёт попаданий в яблочко", "Посчитайте (напечатайте в консоль), сколько случайных точек попало в центральное красное кольцо (радиус < 60) — потребуется формула расстояния из главы 5.")}

{local_required_card(
        "07-22",
        "Практика: координатная мишень",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-22/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — координатная мишень",
        description="Собираем инфографику: концентрическая мишень, оси координат, случайные точки попаданий и подпись.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Координатная мишень", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Мини-проект — координатная мишень",
        lede="Настоящая маленькая инфографика — мишень, оси, случайные точки и подпись, "
        "собранные из уже знакомых инструментов.",
        body_html=body,
        sidebar_groups=sidebar("07-22-mini-proekt-mishen.html"),
        nav=PageNav(prev_href="07-21-mini-proekt-chasy.html", prev_label="Часы без времени", next_href="07-09-mini-proekt-smajlik-itogi.html", next_label="Мини-проект: смайлик и итоги"),
    )
    write("07-22-mini-proekt-mishen.html", out)


def build_09_smajlik() -> None:
    final = turtle_output(
        "07-09-smiley-final", "smajlik.py",
        caption="Готовый результат: жёлтое лицо, два глаза и улыбка-дуга",
        alt="Жёлтый закрашенный круг с двумя чёрными точками-глазами и изогнутой улыбкой из толстой линии",
    )
    face = turtle_output(
        "07-09-smiley-face", "smajlik_lico.py",
        caption="Этап 1 — лицо: закрашенная окружность",
        alt="Жёлтый закрашенный круг без каких-либо деталей лица",
    )
    eyes = turtle_output(
        "07-09-smiley-eyes", "smajlik_glaza.py",
        caption="Этап 2 — добавляем глаза: две точки",
        alt="Тот же жёлтый круг, теперь с двумя чёрными точками-глазами сверху",
    )
    body = f"""
    <h2>Что мы построим</h2>
    <p>Финальный мини-проект главы — и всего блока о Turtle. Соберём дружелюбное лицо из
    примитивов, которые мы разбирали на протяжении всей главы: заливка, точки, дуга.</p>
{final}

    <h2>Разложим лицо на примитивы</h2>
{comparison_table(
        ["Деталь", "Из чего состоит", "Инструмент"],
        [
            ["Лицо", "закрашенная окружность радиусом 100", "fillcolor() + circle() + begin_fill()/end_fill()"],
            ["Глаза", "две точки", "dot()"],
            ["Улыбка", "дуга окружности радиусом 60, extent 120°", "circle(radius, extent)"],
        ],
    )}

    <h2>Координатный план</h2>
{comparison_table(
        ["Деталь", "Координата/угол"],
        [
            ["Левый глаз", "(-35, 120)"],
            ["Правый глаз", "(35, 120)"],
            ["Старт улыбки", "(-50, 60), курс -60°"],
        ],
    )}

    <h2>Этап 1: лицо</h2>
{face}
{code_block("smajlik_lico_kod.py", 'artist.fillcolor("yellow")\nartist.pencolor("#0D0230")\nartist.pensize(2)\n\nartist.begin_fill()\nartist.circle(100)\nartist.end_fill()\n')}

    <h2>Этап 2: глаза</h2>
{eyes}
{code_block(
        "smajlik_glaza_kod.py",
        'artist.penup()\n'
        'artist.goto(-35, 120)\n'
        'artist.pendown()\n'
        'artist.dot(20, "black")\n\n'
        'artist.penup()\n'
        'artist.goto(35, 120)\n'
        'artist.pendown()\n'
        'artist.dot(20, "black")\n',
    )}

    <h2>Этап 3: улыбка — и готово</h2>
{code_block(
        "smajlik_ulybka_kod.py",
        'artist.penup()\n'
        'artist.goto(-50, 60)\n'
        'artist.setheading(-60)\n'
        'artist.pendown()\n'
        'artist.pensize(4)\n'
        'artist.circle(60, 120)\n\n'
        'artist.hideturtle()\n',
    )}
{final}

{exercise(1, "Другое настроение", "Измените дугу улыбки на дугу нахмуренных бровей — переверните направление extent.")}
{exercise(2, "Цветной смайлик", "Смените fillcolor лица на любой другой цвет.")}
{exercise(3, "Щёчки", "Добавьте два маленьких розовых dot() под глазами — получатся румяные щёчки.")}

{local_required_card(
        "07-09",
        "Практика: рисуем смайлик",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-09/index.html",
    )}

    <h2 id="itogi">Итоги главы</h2>
{summary_box("Что мы узнали в этой главе", [
        "Окно, холст и координатный мир — три разные вещи, которые Turtle позволяет настраивать раздельно.",
        "colormode(1.0) и colormode(255) — два способа записать один и тот же RGB-цвет.",
        "pencolor() красит контур, fillcolor() — заливку; color() задаёт оба сразу.",
        "speed() влияет только на анимацию, не на итоговую геометрию; tracer(0) + update() "
        "ускоряют сложную графику, рисуя её пакетом.",
        "circle() рисует вписанный многоугольник — center находится слева от черепашки, "
        "знак радиуса определяет направление, а steps управляет числом сторон явно.",
        "stamp() оставляет отпечаток формы без движения и без линии.",
        "write() выводит текст с настраиваемым align и font, начиная от текущей позиции.",
        "Несколько объектов turtle.Turtle() живут на одном экране независимо — у каждого своё "
        "состояние; clone() копирует стартовое состояние, а дальше объекты расходятся.",
        "clear(), reset() и home() стирают и двигают разные комбинации рисунка и позиции.",
    ])}

    <h2 id="dalshe">Что дальше</h2>
    <p>Turtle-графика на этом не заканчивается насовсем — но дальше курс пойдёт в сторону
    новых инструментов языка. В главе 8 мы начнём работать с текстом по-настоящему — со
    строками и словами, которые до сих пор появлялись у нас только как подписи на экране.</p>
    """
    out = render_page(
        page_title="Мини-проект — смайлик",
        description="Финальный мини-проект главы 7: собираем дружелюбное лицо из примитивов Turtle поэтапно — и подводим итоги главы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Смайлик и итоги", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Мини-проект — смайлик",
        lede="Собираем все приёмы главы в одном дружелюбном рисунке, поэтапно — и подводим "
        "итоги.",
        body_html=body,
        sidebar_groups=sidebar("07-09-mini-proekt-smajlik-itogi.html"),
        nav=PageNav(prev_href="07-22-mini-proekt-mishen.html", prev_label="Координатная мишень", next_href="../glava-08/index.html", next_label="Глава 8: Играем с буквами и словами"),
    )
    write("07-09-mini-proekt-smajlik-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01_ekran()
    build_10_colormode()
    build_02_grafika()
    build_11_pero_zalivka()
    build_12_speed_tracer()
    build_03_figury()
    build_13_geometriya_okruzhnosti()
    build_04_dugi()
    build_14_circle_steps()
    build_05_shtampy()
    build_06_tekst()
    build_15_vyravnivanie()
    build_16_tekst_koordinaty()
    build_17_forma()
    build_18_neskolko()
    build_19_clone()
    build_20_clear_reset_home()
    build_23_otladka()
    build_07_okruzhnost_v_kvadrate()
    build_08_napravlenie()
    build_21_chasy()
    build_22_mishen()
    build_09_smajlik()
    print("Глава 7 полностью собрана.")
