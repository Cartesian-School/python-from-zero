#!/usr/bin/env python3
"""Строит Главу 7: «Глубокое погружение в Turtle» (site/chapters/glava-07/)."""

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
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-07"

PAGES = [
    ("index.html", "Обзор главы"),
    ("07-01-nastraivaem-ekran.html", "Настраиваем экран"),
    ("07-02-nastraivaem-grafiku.html", "Настраиваем графику"),
    ("07-03-figury-bez-linij.html", "Фигуры без линий, окружности, точки"),
    ("07-04-dugi.html", "Дуги"),
    ("07-05-eshche-vozmozhnosti.html", "Ещё больше возможностей"),
    ("07-06-tekst-na-ekrane.html", "Рисуем текст на экране"),
    ("07-07-mini-proekt-okruzhnost-kvadrat.html", "Мини-проект: окружность в квадрате"),
    ("07-08-napravlenie-risovaniya.html", "Меняем направление рисования"),
    ("07-09-mini-proekt-smajlik-itogi.html", "Мини-проект: смайлик и итоги"),
]

LESSON_IDS = ["07-01", "07-03", "07-04", "07-06", "07-07", "07-09"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 7 · Turtle подробно", items),
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
        chapter_num=7,
        baseline_page=107,
        title="Глубокое погружение в Turtle",
        description="Настройка экрана и графики, окружности, дуги, текст на экране и два новых мини-проекта.",
        meta_items=["⏱ ~2–3 часа", "💻 модуль turtle", "📓 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("7.1", "Настраиваем экран", "07-01-nastraivaem-ekran.html", "107"),
            ChapterSectionLink("7.2", "Настраиваем графику", "07-02-nastraivaem-grafiku.html", "109"),
            ChapterSectionLink("7.3", "Фигуры без линий", "07-03-figury-bez-linij.html", "112"),
            ChapterSectionLink("", "Окружности", "07-03-figury-bez-linij.html#okruzhnosti", "112"),
            ChapterSectionLink("", "Точки", "07-03-figury-bez-linij.html#tochki", "113"),
            ChapterSectionLink("7.4", "Дуги", "07-04-dugi.html", "114"),
            ChapterSectionLink("7.5", "Ещё больше возможностей!", "07-05-eshche-vozmozhnosti.html", "116"),
            ChapterSectionLink("7.6", "Рисуем текст на экране", "07-06-tekst-na-ekrane.html", "120"),
            ChapterSectionLink("7.7", "Мини-проект — окружность внутри квадрата", "07-07-mini-proekt-okruzhnost-kvadrat.html", "124"),
            ChapterSectionLink("7.8", "Меняем направление рисования", "07-08-napravlenie-risovaniya.html", "126"),
            ChapterSectionLink("7.9", "Мини-проект — смайлик", "07-09-mini-proekt-smajlik-itogi.html", "131"),
            ChapterSectionLink("", "Итоги", "07-09-mini-proekt-smajlik-itogi.html#itogi", "135"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>Прежде чем рисовать что-то сложнее квадратов, полезно настроить сам холст — размер окна,
    заголовок, цвет фона.</p>
    {code_block(
        "nastrojka_ekrana.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        'screen.title("Моя первая картина")     # заголовок окна\n'
        'screen.bgcolor("lightblue")             # цвет фона\n'
        "screen.setup(width=600, height=500)     # размер окна в пикселях\n\n"
        "artist = turtle.Turtle()\n"
        "screen.exitonclick()\n",
    )}
    {callout(
        "tip",
        "Цвет можно задать и по-другому",
        "Кроме названий вроде <code class=\"inline\">\"lightblue\"</code>, Turtle понимает "
        "шестнадцатеричные коды: <code class=\"inline\">screen.bgcolor(\"#0D0230\")</code> "
        "— тот же формат, что мы используем для фирменных цветов Cartesian School на сайте книги.",
    )}
    {local_required_card(
        "07-01",
        "Практика: настройка экрана и графики",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-01/index.html",
    )}
    """
    out = render_page(
        page_title="Настраиваем экран",
        description="Заголовок окна, цвет фона и размер экрана в модуле turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Настраиваем экран", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Настраиваем экран",
        lede="Прежде чем рисовать, настроим сам холст: заголовок окна, цвет фона и размер.",
        body_html=body,
        sidebar_groups=sidebar("07-01-nastraivaem-ekran.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="07-02-nastraivaem-grafiku.html", next_label="Настраиваем графику"),
    )
    write("07-01-nastraivaem-ekran.html", out)


def build_02() -> None:
    body = f"""
    <p>Теперь настроим саму черепашку: скорость рисования, толщину и цвет линии, форму
    указателя.</p>
    {code_block(
        "nastrojka_grafiki.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        "artist.speed(3)          # скорость от 1 (медленно) до 10 (быстро), 0 — мгновенно\n"
        "artist.pensize(3)        # толщина линии в пикселях\n"
        'artist.pencolor("purple") # цвет линии\n'
        'artist.shape("turtle")    # форма указателя — черепашка вместо стрелки\n\n'
        "artist.forward(100)\n"
        "screen.exitonclick()\n",
    )}
    {callout(
        "info",
        "speed(0) — режим художника",
        "Когда важен результат, а не сам процесс рисования (например, в сложных узорах вроде "
        "мандалы из главы 6), удобно поставить <code class=\"inline\">artist.speed(0)</code> — "
        "черепашка рисует мгновенно, без анимации движения.",
    )}
    {local_required_card(
        "07-01",
        "Практика: включает настройку графики",
        "Тот же ноутбук, что и в разделе «Настраиваем экран» — он охватывает и эту тему",
        "../../practice/07-01/index.html",
    )}
    """
    out = render_page(
        page_title="Настраиваем графику",
        description="Скорость рисования, толщина и цвет линии, форма черепашки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Настраиваем графику", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Настраиваем графику",
        lede="Скорость, толщина линии, цвет и форма черепашки — тонкая настройка перед "
        "рисованием.",
        body_html=body,
        sidebar_groups=sidebar("07-02-nastraivaem-grafiku.html"),
        nav=PageNav(prev_href="07-01-nastraivaem-ekran.html", prev_label="Настраиваем экран", next_href="07-03-figury-bez-linij.html", next_label="Фигуры без линий"),
    )
    write("07-02-nastraivaem-grafiku.html", out)


def build_03() -> None:
    body = f"""
    <h2>Фигуры без линий: заливка цветом</h2>
    <p>Чтобы нарисовать не просто контур, а закрашенную фигуру, оберните рисование между
    <code class="inline">begin_fill()</code> и <code class="inline">end_fill()</code> — цвет
    заливки задаётся заранее командой <code class="inline">fillcolor()</code>.</p>
    {code_block(
        "zalivka.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        'artist.fillcolor("gold")\n'
        "artist.begin_fill()\n"
        "for _ in range(4):\n"
        "    artist.forward(100)\n"
        "    artist.right(90)\n"
        "artist.end_fill()\n\n"
        "screen.exitonclick()\n",
    )}

    <h2 id="okruzhnosti">Окружности</h2>
    <p>Рисовать окружность вручную через множество коротких отрезков не нужно — у Turtle есть
    готовая команда <code class="inline">circle(радиус)</code>:</p>
    {code_block("okruzhnost.py", "artist.circle(60)              # окружность радиусом 60\nartist.circle(-60)             # отрицательный радиус — по часовой стрелке\n")}

    <h2 id="tochki">Точки</h2>
    <p>Мы уже видели <code class="inline">dot()</code> в главе 6 — маленький закрашенный кружок
    в текущей позиции, без движения черепашки:</p>
    {code_block("tochki.py", 'artist.dot(20, "red")   # точка диаметром 20, красная\n')}

    {local_required_card(
        "07-03",
        "Практика: заливка, окружности и точки",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-03/index.html",
    )}
    """
    out = render_page(
        page_title="Фигуры без линий, окружности, точки",
        description="Заливка цветом (begin_fill/end_fill), готовая команда circle() и точки dot().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Фигуры, окружности, точки", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Фигуры без линий",
        lede="Закрашенные фигуры, готовая команда для окружностей и точки без движения "
        "черепашки.",
        body_html=body,
        sidebar_groups=sidebar("07-03-figury-bez-linij.html"),
        nav=PageNav(prev_href="07-02-nastraivaem-grafiku.html", prev_label="Настраиваем графику", next_href="07-04-dugi.html", next_label="Дуги"),
    )
    write("07-03-figury-bez-linij.html", out)


def build_04() -> None:
    body = f"""
    <p><strong>Дуга</strong> — это часть окружности. У <code class="inline">circle()</code>
    есть второй, необязательный аргумент <code class="inline">extent</code> — сколько градусов
    окружности нужно нарисовать:</p>
    {code_block(
        "dugi.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        "artist.circle(80, 180)   # половина окружности (180°)\n"
        "artist.circle(80, 90)    # четверть окружности (90°)\n\n"
        "screen.exitonclick()\n",
    )}
    {callout(
        "tip",
        "Полукруг + прямая = купол",
        "Комбинируя дугу с обычной линией, легко получить составные фигуры — например, "
        "полукруглый купол домика или арку. Попробуйте в ноутбуке практики.",
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
        description="Рисуем части окружности с помощью параметра extent команды circle().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Дуги", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Дуги",
        lede="circle() умеет рисовать не только полные окружности, но и их части — дуги "
        "заданного размера.",
        body_html=body,
        sidebar_groups=sidebar("07-04-dugi.html"),
        nav=PageNav(prev_href="07-03-figury-bez-linij.html", prev_label="Фигуры, окружности, точки", next_href="07-05-eshche-vozmozhnosti.html", next_label="Ещё больше возможностей"),
    )
    write("07-04-dugi.html", out)


def build_05() -> None:
    body = f"""
    <p>Ещё несколько приёмов, которые пригодятся в будущих главах — особенно в играх.</p>

    <h2>Штамп: <code class="inline">stamp()</code></h2>
    <p>Оставляет отпечаток текущей формы черепашки на экране, не рисуя линию — полезно для
    множества одинаковых объектов на экране (например, звёзд неба или врагов в игре):</p>
    {code_block("stamp.py", 'artist.shape("circle")\nartist.stamp()\nartist.forward(50)\nartist.stamp()\n')}

    <h2>Скрыть и показать черепашку</h2>
    {code_block("skryt.py", "artist.hideturtle()   # спрятать указатель черепашки (сама линия останется)\nartist.showturtle()   # показать обратно\n")}

    {callout(
        "info",
        "Зачем прятать черепашку?",
        "В готовых рисунках указатель черепашки (маленький треугольник или другая форма) может "
        "визуально мешать. <code class=\"inline\">hideturtle()</code> в конце программы делает "
        "финальный результат чище.",
    )}

    <h2>Отмена последнего действия: <code class="inline">undo()</code></h2>
    {code_block("undo.py", "artist.forward(100)\nartist.undo()   # отменяет последнее движение, как Ctrl+Z\n")}

    {local_required_card(
        "07-03",
        "Практика: включает stamp(), hideturtle() и undo()",
        "Тот же ноутбук, что и в разделе «Фигуры, окружности, точки» — он охватывает и эту тему",
        "../../practice/07-03/index.html",
    )}
    """
    out = render_page(
        page_title="Ещё больше возможностей!",
        description="stamp(), hideturtle()/showturtle() и undo() в модуле turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Ещё больше возможностей", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Ещё больше возможностей!",
        lede="Несколько приёмов на будущее: штампы, скрытие черепашки и отмена последнего "
        "действия.",
        body_html=body,
        sidebar_groups=sidebar("07-05-eshche-vozmozhnosti.html"),
        nav=PageNav(prev_href="07-04-dugi.html", prev_label="Дуги", next_href="07-06-tekst-na-ekrane.html", next_label="Текст на экране"),
    )
    write("07-05-eshche-vozmozhnosti.html", out)


def build_06() -> None:
    body = f"""
    <p>Turtle умеет не только рисовать линии, но и выводить текст прямо на холсте — командой
    <code class="inline">write()</code>:</p>
    {code_block(
        "tekst.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        'artist.write("Привет, Turtle!", font=("Arial", 20, "normal"))\n\n'
        "screen.exitonclick()\n",
    )}
    <p>Параметр <code class="inline">font</code> — кортеж из трёх значений: название шрифта,
    размер и начертание (<code class="inline">"normal"</code>, <code class="inline">"bold"</code>
    или <code class="inline">"italic"</code>).</p>

    {callout(
        "tip",
        "Текст можно выровнять",
        "Необязательный параметр <code class=\"inline\">align</code> "
        "(<code class=\"inline\">\"left\"</code>, <code class=\"inline\">\"center\"</code> или "
        "<code class=\"inline\">\"right\"</code>) управляет тем, как текст выравнивается "
        "относительно текущей позиции черепашки.",
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
        description="Команда write() для вывода текста на холсте Turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Текст на экране", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Рисуем текст на экране",
        lede="Turtle умеет не только линии — научим её подписывать собственные рисунки.",
        body_html=body,
        sidebar_groups=sidebar("07-06-tekst-na-ekrane.html"),
        nav=PageNav(prev_href="07-05-eshche-vozmozhnosti.html", prev_label="Ещё больше возможностей", next_href="07-07-mini-proekt-okruzhnost-kvadrat.html", next_label="Мини-проект: окружность в квадрате"),
    )
    write("07-06-tekst-na-ekrane.html", out)


def build_07() -> None:
    body = f"""
    <p>Соберём фигуры этой главы в одном рисунке: квадрат с вписанной в него окружностью.</p>
    {code_block(
        "okruzhnost_v_kvadrate.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n"
        "artist.speed(0)\n\n"
        "razmer = 150\n\n"
        "# квадрат\n"
        "for _ in range(4):\n"
        "    artist.forward(razmer)\n"
        "    artist.right(90)\n\n"
        "# перемещаемся к точке, откуда начнётся вписанная окружность\n"
        "artist.penup()\n"
        "artist.goto(razmer / 2, -razmer / 2)\n"
        "artist.setheading(0)\n"
        "artist.pendown()\n"
        "artist.circle(razmer / 2)\n\n"
        "screen.exitonclick()\n",
    )}
    {callout(
        "info",
        "Откуда взялась эта точка?",
        "Чтобы окружность радиусом <code class=\"inline\">razmer / 2</code> идеально "
        "вписалась в квадрат, черепашка должна начать рисовать её из точки на полпути вдоль "
        "нижней стороны — отсюда и вычисление координат через <code class=\"inline\">penup()"
        "</code>/<code class=\"inline\">goto()</code> из главы 6.",
    )}
    {exercise(2, "Окружность в шестиугольнике", "Замените квадрат на шестиугольник из главы 6 и впишите в него окружность подходящего радиуса.")}

    {local_required_card(
        "07-07",
        "Практика: вписанная окружность",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-07/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — окружность внутри квадрата",
        description="Комбинируем фигуры: рисуем окружность, идеально вписанную в квадрат.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Окружность в квадрате", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Мини-проект — окружность внутри квадрата",
        lede="Первая композиция из нескольких фигур — квадрат и точно вписанная в него "
        "окружность.",
        body_html=body,
        sidebar_groups=sidebar("07-07-mini-proekt-okruzhnost-kvadrat.html"),
        nav=PageNav(prev_href="07-06-tekst-na-ekrane.html", prev_label="Текст на экране", next_href="07-08-napravlenie-risovaniya.html", next_label="Меняем направление рисования"),
    )
    write("07-07-mini-proekt-okruzhnost-kvadrat.html", out)


def build_08() -> None:
    body = f"""
    <p>По умолчанию <code class="inline">circle()</code> рисует окружность против часовой
    стрелки. Отрицательный радиус меняет направление на противоположное — по часовой стрелке:</p>
    {code_block("napravlenie.py", "artist.circle(60)    # против часовой стрелки\nartist.circle(-60)   # по часовой стрелке\n")}

    <h2>Режимы измерения углов</h2>
    <p>По умолчанию Turtle измеряет углы в градусах. Если по какой-то причине удобнее работать
    в радианах (например, для совместимости с формулами из модуля <code class="inline">math</code>
    из главы 5) — есть команды <code class="inline">degrees()</code> и
    <code class="inline">radians()</code>:</p>
    {code_block("radiany.py", "import math\n\nartist.radians()\nartist.left(math.pi / 2)   # поворот на 90°, выраженный в радианах\n\nartist.degrees()            # возвращаемся к привычным градусам\n")}

    {local_required_card(
        "07-07",
        "Практика: включает практику с направлением рисования",
        "Тот же ноутбук, что и в разделе «Окружность в квадрате» — он охватывает и эту тему",
        "../../practice/07-07/index.html",
    )}
    """
    out = render_page(
        page_title="Меняем направление рисования",
        description="Направление рисования окружности (по/против часовой стрелки) и режимы измерения углов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Направление рисования", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Меняем направление рисования",
        lede="Отрицательный радиус и режимы измерения углов — ещё немного тонкой настройки "
        "перед финальным мини-проектом главы.",
        body_html=body,
        sidebar_groups=sidebar("07-08-napravlenie-risovaniya.html"),
        nav=PageNav(prev_href="07-07-mini-proekt-okruzhnost-kvadrat.html", prev_label="Окружность в квадрате", next_href="07-09-mini-proekt-smajlik-itogi.html", next_label="Мини-проект: смайлик и итоги"),
    )
    write("07-08-napravlenie-risovaniya.html", out)


def build_09() -> None:
    body = f"""
    <p>Финальный мини-проект главы: нарисуем простой смайлик, используя всё, что узнали —
    окружности, заливку, дуги и точки.</p>
    {code_block(
        "smajlik.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n"
        "artist.speed(0)\n\n"
        "# лицо\n"
        'artist.fillcolor("yellow")\n'
        "artist.begin_fill()\n"
        "artist.circle(100)\n"
        "artist.end_fill()\n\n"
        "# глаза\n"
        "artist.penup()\n"
        "artist.goto(-35, 120)\n"
        "artist.pendown()\n"
        'artist.dot(20, "black")\n'
        "artist.penup()\n"
        "artist.goto(35, 120)\n"
        "artist.pendown()\n"
        'artist.dot(20, "black")\n\n'
        "# улыбка — нижняя дуга окружности\n"
        "artist.penup()\n"
        "artist.goto(-50, 60)\n"
        "artist.setheading(-60)\n"
        "artist.pendown()\n"
        "artist.pensize(4)\n"
        "artist.circle(60, 120)\n\n"
        "artist.hideturtle()\n"
        "screen.exitonclick()\n",
    )}

    {exercise(1, "Другое настроение", "Измените дугу улыбки на дугу нахмуренных бровей — переверните направление extent.")}
    {exercise(2, "Цветной смайлик", "Смените fillcolor лица на любой другой цвет.")}
    {exercise(3, "Щёчки", "Добавьте два маленьких розовых dot() под глазами — получатся румяные щёчки.")}

    {local_required_card(
        "07-09",
        "Практика: рисуем смайлик",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/07-09/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "<code class=\"inline\">begin_fill()</code>/<code class=\"inline\">end_fill()</code> "
        "закрашивают фигуру выбранным цветом.",
        "<code class=\"inline\">circle(радиус, extent)</code> рисует окружности и дуги; "
        "отрицательный радиус меняет направление на противоположное.",
        "<code class=\"inline\">write()</code> выводит текст прямо на холсте.",
        "<code class=\"inline\">stamp()</code>, <code class=\"inline\">hideturtle()</code> и "
        "<code class=\"inline\">undo()</code> — полезные инструменты для более сложных "
        "рисунков.",
        "Композиция из нескольких фигур (квадрат + окружность, смайлик) строится "
        "последовательным применением уже знакомых команд.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — смайлик",
        description="Финальный мини-проект главы 7: рисуем смайлик — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 7", "index.html"), ("Смайлик и итоги", "")],
        kicker="Глава 7 · Глубокое погружение в Turtle",
        h1="Мини-проект — смайлик",
        lede="Собираем все приёмы главы в одном дружелюбном рисунке — и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("07-09-mini-proekt-smajlik-itogi.html"),
        nav=PageNav(prev_href="07-08-napravlenie-risovaniya.html", prev_label="Направление рисования", next_href="../glava-08/index.html", next_label="Глава 8: Играем с буквами и словами"),
    )
    write("07-09-mini-proekt-smajlik-itogi.html", out)


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
