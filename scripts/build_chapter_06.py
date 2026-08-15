#!/usr/bin/env python3
"""Строит Главу 6: «Рисуем классные вещи с помощью Turtle» (site/chapters/glava-06/)."""

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
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-06"

PAGES = [
    ("index.html", "Приступаем (обзор главы)"),
    ("06-01-pristupaem.html", "Приступаем"),
    ("06-02-dvizhenie-vpered-nazad.html", "Заставляем Turtle двигаться"),
    ("06-03-povorot-cherepashki.html", "Меняем направление"),
    ("06-04-mini-proekty-figury.html", "Мини-проекты: квадрат и шестиугольник"),
    ("06-05-sokraschennye-priemy.html", "Сокращённые приёмы"),
    ("06-06-sluchaynye-tochki.html", "Случайные точки на экране"),
    ("06-07-goto-kvadrat.html", "Квадрат с помощью goto"),
    ("06-08-mandala-itogi.html", "Мандала и итоги"),
]

LESSON_IDS = ["06-02", "06-03", "06-04", "06-06", "06-07", "06-08"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 6 · Turtle", items),
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
        chapter_num=6,
        baseline_page=83,
        title="Рисуем классные вещи с помощью Turtle",
        description="Первая графика на Python: движение, повороты, готовые фигуры и мандалы из "
        "прямых линий.",
        meta_items=["⏱ ~2–3 часа", "💻 модуль turtle", "📓 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("6.1", "Приступаем", "06-01-pristupaem.html", "83"),
            ChapterSectionLink("6.2", "Заставляем Turtle двигаться", "06-02-dvizhenie-vpered-nazad.html", "86"),
            ChapterSectionLink("", "Движение вперёд и назад", "06-02-dvizhenie-vpered-nazad.html", "86"),
            ChapterSectionLink("", "Заставляем черепашку менять направление", "06-03-povorot-cherepashki.html", "89"),
            ChapterSectionLink("6.4", "Мини-проект — рисуем квадрат", "06-04-mini-proekty-figury.html", "91"),
            ChapterSectionLink("", "Мини-проект — рисуем шестиугольник", "06-04-mini-proekty-figury.html#shestiugolnik", "93"),
            ChapterSectionLink("6.5", "Сокращённые приёмы", "06-05-sokraschennye-priemy.html", "95"),
            ChapterSectionLink("6.6", "Переходим к случайным точкам на экране", "06-06-sluchaynye-tochki.html", "96"),
            ChapterSectionLink("6.7", "Рисуем квадрат с помощью goto", "06-07-goto-kvadrat.html", "98"),
            ChapterSectionLink("6.8", "Мини-проект — мандала только из прямых линий", "06-08-mandala-itogi.html", "100"),
            ChapterSectionLink("", "Итоги", "06-08-mandala-itogi.html#itogi", "105"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>Модуль <code class="inline">turtle</code> входит в стандартную поставку Python — ничего
    дополнительно устанавливать не нужно. Название отсылает к «черепашьей графике» (turtle
    graphics), придуманной ещё в 1960-х годах для обучения детей программированию — идея
    настолько удачная, что дожила до наших дней практически без изменений.</p>

    <h2>Экран и черепашка — два разных объекта</h2>
    <p>Прежде чем рисовать, нужны два объекта: <strong>экран</strong>
    (<code class="inline">turtle.Screen()</code>) — окно, в котором происходит рисование, и
    <strong>черепашка</strong> (<code class="inline">turtle.Turtle()</code>) — то, что, собственно,
    рисует.</p>

    {code_block("nastroyka_ekrana.py", 'import turtle\n\nscreen = turtle.Screen()\nartist = turtle.Turtle()\n\nscreen.exitonclick()  # держим окно открытым до клика мышью\n')}

    <p>Запустив этот код, вы увидите пустое белое окно с маленьким чёрным треугольником посередине
    — это и есть черепашка в исходном положении. Курс (направление) черепашки по умолчанию
    направлен вправо — на восток.</p>

    {callout(
        "info",
        "Зачем два отдельных объекта?",
        "Разделение экрана и черепашки позволяет иметь на одном экране сразу <strong>несколько"
        "</strong> черепашек — мы воспользуемся этим в мини-проекте «Гонка Turtle» в главе 12.",
    )}

    {local_required_card(
        "06-02",
        "Практика: начинаем с настройки экрана",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-02/index.html",
    )}
    """
    out = render_page(
        page_title="Приступаем",
        description="Первое знакомство с модулем turtle: экран и черепашка.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Приступаем", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Приступаем",
        lede="Знакомимся с двумя главными объектами графики Turtle: экраном и самой черепашкой.",
        body_html=body,
        sidebar_groups=sidebar("06-01-pristupaem.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="06-02-dvizhenie-vpered-nazad.html", next_label="Заставляем Turtle двигаться"),
    )
    write("06-01-pristupaem.html", out)


def build_02() -> None:
    cvm = classic_vs_modern(
        "Классический подход → современный Python 3.14",
        "Классический подход",
        "import turtle\n\n"
        "# без явного объекта —\n"
        "# используется скрытая\n"
        "# черепашка по умолчанию\n"
        "turtle.forward(120)\n"
        "turtle.left(90)\n"
        "turtle.forward(80)\n"
        "turtle.done()",
        "Современный Python 3.14",
        "import turtle\n\n"
        "# явный объект — понятно,\n"
        "# какая черепашка рисует,\n"
        "# легко добавить вторую\n"
        "artist = turtle.Turtle()\n"
        "artist.forward(120)\n"
        "artist.left(90)\n"
        "artist.forward(80)\n"
        "turtle.done()",
        "явный объект <code class=\"inline\">turtle.Turtle()</code>. Он ничего не усложняет, "
        "зато сразу готовит вас к главе 14 (объекты) и легко масштабируется — если позже "
        "понадобится нарисовать гонку из нескольких черепашек (см. мини-проект в главе 12), у "
        "каждой будет своё имя и своё состояние. Модульные функции "
        "(<code class=\"inline\">turtle.forward()</code> без объекта) всё ещё встречаются в "
        "старом коде и учебниках — знать их полезно, но начинайте привычку сразу с объекта.",
    )

    body = f"""
    <h2>Зачем это нужно</h2>
    <p>Всё, что вы нарисуете дальше — квадраты, шестиугольники, мандалы, даже персонажей в
    играх — строится из одной и той же пары действий: <strong>«проехать немного»</strong> и
    <strong>«повернуть на какой-то угол»</strong>. Освоив эти четыре команды, вы получите
    строительные блоки для всей главы.</p>

    <h2>Простая модель</h2>
    <p>Представьте черепашку как перо на листе бумаги. У пера есть две вещи:
    <strong>позиция</strong> (где оно сейчас находится) и <strong>курс</strong> — направление, в
    которое оно «смотрит». Когда черепашка едет вперёд, она просто перемещается по прямой в
    сторону своего курса. Когда она поворачивает, меняется курс, а позиция остаётся прежней —
    как будто вы стоите на месте и просто поворачиваетесь.</p>

    <h2>Синтаксис</h2>
    <p>У объекта черепашки есть четыре базовые команды движения:</p>
    <ul>
      <li><code class="inline">forward(расстояние)</code> — проехать вперёд на указанное число пикселей (короткая форма — <code class="inline">fd</code>)</li>
      <li><code class="inline">backward(расстояние)</code> — проехать назад, не поворачиваясь (короткие формы — <code class="inline">bk</code>, <code class="inline">back</code>)</li>
      <li><code class="inline">right(угол)</code> — повернуть по часовой стрелке на угол в градусах (короткая форма — <code class="inline">rt</code>)</li>
      <li><code class="inline">left(угол)</code> — повернуть против часовой стрелки на угол в градусах (короткая форма — <code class="inline">lt</code>)</li>
    </ul>

    <h2>Первый рабочий пример</h2>
    <p>Нарисуем букву «Г»: проедем вперёд, повернём и проедем ещё раз.</p>
    {code_block(
        "turtle_dvizhenie.py",
        "import turtle\n\n"
        "# создаём окно и черепашку\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        "# едем вперёд на 120 пикселей\n"
        "artist.forward(120)\n\n"
        "# поворачиваем на 90 градусов против часовой стрелки\n"
        "artist.left(90)\n\n"
        "# едем вперёд ещё раз — получаем букву «Г»\n"
        "artist.forward(80)\n\n"
        "screen.exitonclick()  # окно закроется по клику мыши\n",
    )}

    <h3>Разбор по шагам</h3>
    <ul>
      <li><code class="inline">turtle.Screen()</code> открывает окно для рисования.</li>
      <li><code class="inline">turtle.Turtle()</code> создаёт саму черепашку — в начале координат, курс направлен вправо (на восток).</li>
      <li><code class="inline">artist.forward(120)</code> — черепашка проезжает 120 пикселей в направлении курса, оставляя линию.</li>
      <li><code class="inline">artist.left(90)</code> — курс поворачивается на 90° против часовой стрелки (теперь черепашка «смотрит» вверх).</li>
      <li>Второй вызов <code class="inline">forward()</code> едет уже в новом направлении — отсюда и получается уголок буквы «Г».</li>
      <li><code class="inline">screen.exitonclick()</code> держит окно открытым, пока вы не кликнете по нему — без этой строки окно может закрыться мгновенно.</li>
    </ul>

    {callout(
        "tip",
        "Совет",
        "Числа в <code class=\"inline\">forward()</code> и <code class=\"inline\">right()</code>/"
        "<code class=\"inline\">left()</code> могут быть отрицательными. "
        "<code class=\"inline\">forward(-50)</code> и <code class=\"inline\">backward(50)</code> "
        "делают одно и то же.",
    )}

    <h2>Эксперимент 1</h2>
    <p>Измените расстояние 120 на 250 и угол 90 на 45. Перед запуском попробуйте предсказать: в
    какую сторону теперь «смотрит» черепашка после поворота?</p>

    <h2>Эксперимент 2</h2>
    <p>Добавьте третью пару команд <code class="inline">left(90)</code> и
    <code class="inline">forward(120)</code> в конец программы. Какая фигура получится?</p>

    <h2>Типичная ошибка</h2>
    {callout(
        "warning",
        "Внимание",
        "Начинающие часто путают <code class=\"inline\">right()</code>/<code class=\"inline\">left()"
        "</code> с движением — кажется, что черепашка должна сместиться в сторону. На самом деле "
        "эти команды <strong>только поворачивают</strong> курс и не двигают черепашку ни на "
        "пиксель.",
    )}
    <p><strong>Диагностика:</strong> если после поворота фигура выглядит «сплющенной» или линии
    накладываются друг на друга — скорее всего, вы забыли вызвать <code class="inline">forward()</code>
    после поворота, либо перепутали местами поворот и движение.</p>
    <p><strong>Исправление:</strong> перечитайте программу построчно и для каждой команды
    спросите себя: «это движение или поворот?» — держите эти два действия отдельно друг от
    друга.</p>

    <h2>Современный вариант</h2>
    <p>В старом коде черепашку часто рисуют без явного объекта — модуль
    <code class="inline">turtle</code> автоматически создаёт «черепашку по умолчанию», и её можно
    двигать напрямую через функции модуля.</p>
    {cvm}

    {local_required_card(
        "06-02",
        "Практика: эксперименты, задание и самостоятельная практика",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-02/index.html",
    )}

    <h2>Задание</h2>
    {exercise(1, "Буква «Т»", "Используя только <code class=\"inline\">forward</code>, <code class=\"inline\">backward</code>, <code class=\"inline\">left</code> и <code class=\"inline\">right</code>, нарисуйте букву «Т» одной непрерывной линией пера.")}
    {exercise(2, "Лестница из трёх ступенек", "Нарисуйте лестницу, состоящую из трёх одинаковых «ступенек» (вперёд-поворот-вперёд-поворот). Попробуйте обойтись без повторения одинакового блока кода вручную — подсказка: этому вы научитесь в главе 10, а пока просто повторите блок трижды подряд.")}

    {summary_box("Что запомнить", [
        "<code class=\"inline\">forward()</code>/<code class=\"inline\">backward()</code> "
        "двигают черепашку по прямой; <code class=\"inline\">left()</code>/"
        "<code class=\"inline\">right()</code> только поворачивают курс.",
        "Позиция и курс — это два независимых свойства черепашки.",
        "Современный стиль — создавать явный объект <code class=\"inline\">turtle.Turtle()</code>, "
        "а не полагаться на скрытую черепашку по умолчанию.",
        "<code class=\"inline\">screen.exitonclick()</code> или <code class=\"inline\">turtle.done()</code> "
        "нужны, чтобы окно не закрылось мгновенно.",
    ])}
    """

    out = render_page(
        page_title="Движение вперёд и назад",
        description="Учимся управлять черепашкой Turtle: forward, backward, right, left. Разбор примера, типичная ошибка и современный подход к работе с Turtle в Python 3.14.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Движение вперёд и назад", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Движение вперёд и назад",
        lede="Первое, что должна уметь черепашка — двигаться. В этом разделе вы напишете свою "
        "первую программу, которая по-настоящему рисует.",
        body_html=body,
        sidebar_groups=sidebar("06-02-dvizhenie-vpered-nazad.html"),
        nav=PageNav(prev_href="06-01-pristupaem.html", prev_label="Приступаем", next_href="06-03-povorot-cherepashki.html", next_label="Меняем направление"),
    )
    write("06-02-dvizhenie-vpered-nazad.html", out)


def build_03() -> None:
    body = f"""
    <p>Команды <code class="inline">left()</code>/<code class="inline">right()</code> из
    предыдущего раздела поворачивают черепашку <strong>относительно</strong> её текущего курса.
    Иногда удобнее задать направление <strong>абсолютно</strong> — «смотри строго на север»,
    независимо от того, куда черепашка смотрела раньше.</p>

    <h2>Абсолютный курс: <code class="inline">setheading()</code></h2>
    <p>В Turtle направления измеряются в градусах против часовой стрелки, начиная с востока
    (0°): восток — 0°, север — 90°, запад — 180°, юг — 270°.</p>
    {code_block("setheading.py", 'import turtle\n\nscreen = turtle.Screen()\nartist = turtle.Turtle()\n\nartist.setheading(90)   # смотрим строго вверх, неважно, куда смотрели раньше\nartist.forward(100)\n\nartist.setheading(180)  # смотрим строго влево\nartist.forward(100)\n\nscreen.exitonclick()\n')}

    <h2>Возврат домой: <code class="inline">home()</code></h2>
    <p>Возвращает черепашку в исходную точку (0, 0) с исходным курсом (0°) — удобно, чтобы
    начать рисунок заново, не создавая нового объекта:</p>
    {code_block("home.py", "artist.home()\n")}

    {callout(
        "tip",
        "heading() — узнать текущий курс",
        "Если нужно не задать курс, а <em>узнать</em> его — используйте "
        "<code class=\"inline\">artist.heading()</code>: она возвращает текущее направление в "
        "градусах, не меняя его.",
    )}

    {local_required_card(
        "06-03",
        "Практика: setheading(), heading() и home()",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-03/index.html",
    )}
    """
    out = render_page(
        page_title="Заставляем черепашку менять направление",
        description="Абсолютное направление в Turtle: setheading(), heading() и home().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Меняем направление", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Заставляем черепашку менять направление",
        lede="Кроме относительных поворотов left()/right(), у черепашки есть способ задать "
        "направление абсолютно — вне зависимости от того, куда она смотрела раньше.",
        body_html=body,
        sidebar_groups=sidebar("06-03-povorot-cherepashki.html"),
        nav=PageNav(prev_href="06-02-dvizhenie-vpered-nazad.html", prev_label="Заставляем Turtle двигаться", next_href="06-04-mini-proekty-figury.html", next_label="Мини-проекты: фигуры"),
    )
    write("06-03-povorot-cherepashki.html", out)


def build_04() -> None:
    body = f"""
    <p>Применим движение и повороты, чтобы нарисовать первые настоящие фигуры.</p>

    <h2>Мини-проект — рисуем квадрат</h2>
    <p>У квадрата четыре одинаковые стороны и четыре угла по 90°. Значит, нужно четыре раза
    повторить одну и ту же пару команд: проехать вперёд, повернуть на 90°.</p>
    {code_block(
        "kvadrat.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        "artist.forward(100)\n"
        "artist.right(90)\n"
        "artist.forward(100)\n"
        "artist.right(90)\n"
        "artist.forward(100)\n"
        "artist.right(90)\n"
        "artist.forward(100)\n"
        "artist.right(90)\n\n"
        "screen.exitonclick()\n",
    )}
    {callout(
        "tip",
        "Заметили повторение?",
        "Четыре одинаковых блока подряд — явный признак того, что напрашивается цикл "
        "<code class=\"inline\">for</code>. Мы вернёмся к этому же квадрату в главе 10 и "
        "перепишем его в 2 строки вместо 8.",
    )}

    <h2 id="shestiugolnik">Мини-проект — рисуем шестиугольник</h2>
    <p>У шестиугольника шесть равных сторон, и сумма всех внешних углов многоугольника всегда
    равна 360° — значит, угол поворота на каждом шаге равен <code class="inline">360 / 6 = 60</code>
    градусов.</p>
    {code_block(
        "shestiugolnik.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        "artist.forward(80)\n"
        "artist.right(60)\n"
        "artist.forward(80)\n"
        "artist.right(60)\n"
        "artist.forward(80)\n"
        "artist.right(60)\n"
        "artist.forward(80)\n"
        "artist.right(60)\n"
        "artist.forward(80)\n"
        "artist.right(60)\n"
        "artist.forward(80)\n"
        "artist.right(60)\n\n"
        "screen.exitonclick()\n",
    )}

    {callout(
        "info",
        "Формула для любого правильного многоугольника",
        "Угол поворота = <code class=\"inline\">360 / количество_сторон</code>. Треугольник — "
        "120°, квадрат — 90°, пятиугольник — 72°, шестиугольник — 60°. Попробуйте эту формулу "
        "в ноутбуке практики на фигуре по вашему выбору.",
    )}

    {local_required_card(
        "06-04",
        "Практика: квадрат, шестиугольник и другие многоугольники",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-04/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проекты: квадрат и шестиугольник",
        description="Рисуем первые фигуры циклом команд forward/right — квадрат и шестиугольник.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Мини-проекты: фигуры", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Мини-проект — рисуем квадрат",
        lede="Первые настоящие фигуры — применяем движение и повороты из предыдущих разделов.",
        body_html=body,
        sidebar_groups=sidebar("06-04-mini-proekty-figury.html"),
        nav=PageNav(prev_href="06-03-povorot-cherepashki.html", prev_label="Меняем направление", next_href="06-05-sokraschennye-priemy.html", next_label="Сокращённые приёмы"),
    )
    write("06-04-mini-proekty-figury.html", out)


def build_05() -> None:
    cvm = classic_vs_modern(
        "Полные имена команд → короткие псевдонимы",
        "Полные имена",
        "artist.forward(100)\nartist.backward(50)\nartist.left(90)\nartist.right(90)",
        "Короткие псевдонимы",
        "artist.fd(100)\nartist.bk(50)\nartist.lt(90)\nartist.rt(90)",
        "оба варианта официальны и делают ровно одно и то же — псевдонимы существуют в "
        "модуле turtle специально для более быстрого написания. В этой книге мы обычно "
        "используем полные имена, потому что они понятнее при первом чтении, но короткие формы "
        "стоит узнавать: в чужом коде и примерах в интернете вы будете встречать оба варианта.",
    )

    body = f"""
    <p>У каждой команды движения, которую мы изучили, есть более короткий псевдоним — они
    делают абсолютно то же самое, только короче печатать:</p>
    <ul>
      <li><code class="inline">forward()</code> → <code class="inline">fd()</code></li>
      <li><code class="inline">backward()</code> → <code class="inline">bk()</code> (или
        <code class="inline">back()</code>)</li>
      <li><code class="inline">left()</code> → <code class="inline">lt()</code></li>
      <li><code class="inline">right()</code> → <code class="inline">rt()</code></li>
    </ul>

    {cvm}

    <h2>Другие полезные сокращения</h2>
    <p>Помимо движения, часто используют ещё две короткие команды для оформления:</p>
    {code_block("oformlenie.py", 'artist.pencolor("purple")   # цвет линии\nartist.pensize(3)            # толщина линии\n')}

    {local_required_card(
        "06-04",
        "Практика: включает практику с короткими командами",
        "Тот же ноутбук, что и в разделе «Мини-проекты: фигуры» — он охватывает и эту тему",
        "../../practice/06-04/index.html",
    )}
    """
    out = render_page(
        page_title="Сокращённые приёмы",
        description="Короткие псевдонимы команд Turtle: fd, bk, lt, rt — и настройка цвета/толщины линии.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Сокращённые приёмы", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Сокращённые приёмы",
        lede="Каждая команда движения имеет более короткий псевдоним — полезно уметь читать оба "
        "варианта.",
        body_html=body,
        sidebar_groups=sidebar("06-05-sokraschennye-priemy.html"),
        nav=PageNav(prev_href="06-04-mini-proekty-figury.html", prev_label="Мини-проекты: фигуры", next_href="06-06-sluchaynye-tochki.html", next_label="Случайные точки на экране"),
    )
    write("06-05-sokraschennye-priemy.html", out)


def build_06() -> None:
    body = f"""
    <p>До сих пор черепашка двигалась только относительно своей текущей позиции. Но можно
    сразу «телепортировать» её в конкретную точку экрана командой
    <code class="inline">goto(x, y)</code> — а вместе со случайными числами из главы 5 это
    открывает интересные возможности.</p>

    <h2>Система координат экрана</h2>
    <p>Центр экрана Turtle — точка <code class="inline">(0, 0)</code>. Ось X растёт вправо, ось
    Y растёт вверх (в отличие от многих других графических систем, где Y растёт вниз — ещё один
    повод свериться с документацией, если работаете с другой библиотекой). По умолчанию окно
    имеет размер 400×300 точек в каждую сторону от центра.</p>

    {code_block("sluchaynye_tochki.py", 'import turtle\nimport random\n\nscreen = turtle.Screen()\nartist = turtle.Turtle()\nartist.penup()  # поднимаем перо — при движении линия не рисуется\n\nfor _ in range(10):\n    x = random.randint(-200, 200)\n    y = random.randint(-150, 150)\n    artist.goto(x, y)\n    artist.pendown()\n    artist.dot(10)  # рисуем точку диаметром 10\n    artist.penup()\n\nscreen.exitonclick()\n')}

    {callout(
        "warning",
        "penup() / pendown()",
        "Без <code class=\"inline\">penup()</code> черепашка будет рисовать линию при каждом "
        "перемещении <code class=\"inline\">goto()</code> — что обычно не то, что нужно для "
        "«прыжка» в новую точку. Не забывайте включить перо обратно <code class=\"inline\">"
        "pendown()</code>, когда снова понадобится рисовать.",
    )}

    {local_required_card(
        "06-06",
        "Практика: goto(), penup()/pendown() и random",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-06/index.html",
    )}
    """
    out = render_page(
        page_title="Переходим к случайным точкам на экране",
        description="goto(), penup()/pendown() и модуль random вместе — рисуем случайные точки на экране.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Случайные точки", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Переходим к случайным точкам на экране",
        lede="goto() перемещает черепашку в любую точку экрана напрямую — вместе со случайными "
        "числами получается интересный эффект.",
        body_html=body,
        sidebar_groups=sidebar("06-06-sluchaynye-tochki.html"),
        nav=PageNav(prev_href="06-05-sokraschennye-priemy.html", prev_label="Сокращённые приёмы", next_href="06-07-goto-kvadrat.html", next_label="Квадрат с помощью goto"),
    )
    write("06-06-sluchaynye-tochki.html", out)


def build_07() -> None:
    body = f"""
    <p>Вернёмся к квадрату из раздела 6.4 — на этот раз нарисуем его без единого поворота,
    задавая напрямую четыре угловые точки командой <code class="inline">goto()</code>.</p>
    {code_block(
        "kvadrat_goto.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n\n"
        "artist.goto(100, 0)\n"
        "artist.goto(100, 100)\n"
        "artist.goto(0, 100)\n"
        "artist.goto(0, 0)\n\n"
        "screen.exitonclick()\n",
    )}

    {callout(
        "tip",
        "Два способа — один результат",
        "<code class=\"inline\">forward()</code> + <code class=\"inline\">right()</code> "
        "описывают движение <em>относительно черепашки</em> («проехать, повернуть»); "
        "<code class=\"inline\">goto()</code> описывает движение <em>относительно экрана</em> "
        "(«окажись в этой точке»). Иногда одно удобнее другого — например, goto() удобен, "
        "когда координаты фигуры уже известны заранее.",
    )}

    {local_required_card(
        "06-07",
        "Практика: рисуем фигуры через координаты",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-07/index.html",
    )}
    """
    out = render_page(
        page_title="Рисуем квадрат с помощью goto",
        description="Альтернативный способ рисовать фигуры в Turtle — через координаты точек, а не движение и повороты.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Квадрат с помощью goto", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Рисуем квадрат с помощью goto",
        lede="Тот же квадрат, что и раньше, — но на этот раз через прямое указание координат "
        "каждого угла.",
        body_html=body,
        sidebar_groups=sidebar("06-07-goto-kvadrat.html"),
        nav=PageNav(prev_href="06-06-sluchaynye-tochki.html", prev_label="Случайные точки", next_href="06-08-mandala-itogi.html", next_label="Мандала и итоги"),
    )
    write("06-07-goto-kvadrat.html", out)


def build_08() -> None:
    body = f"""
    <p>Соберём все приёмы главы в одном мини-проекте: мандалу, составленную только из прямых
    линий, — множество отрезков одинаковой длины, каждый раз повёрнутых на небольшой угол.</p>

    {code_block(
        "mandala.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n"
        "artist.speed(0)  # максимальная скорость рисования\n\n"
        "shag_ugla = 10\n"
        "ugol = 0\n"
        "while ugol < 360:\n"
        "    artist.setheading(ugol)\n"
        "    artist.forward(150)\n"
        "    artist.backward(150)\n"
        "    ugol += shag_ugla\n\n"
        "screen.exitonclick()\n",
    )}

    {callout(
        "info",
        "Забегаем вперёд",
        "Цикл <code class=\"inline\">while</code> подробно разберём в главе 10 — здесь "
        "достаточно увидеть, что <code class=\"inline\">setheading()</code> из раздела 6.3 "
        "позволяет нарисовать сложный узор всего в нескольких строках, перебирая углы от 0 "
        "до 360.",
    )}

    {exercise(
        1,
        "Другой шаг угла",
        "Измените <code class=\"inline\">shag_ugla</code> на 5 или на 30 — как меняется "
        "узор?",
    )}
    {exercise(
        2,
        "Другая длина луча",
        "Измените длину <code class=\"inline\">forward(150)</code> — попробуйте 80 и 250.",
    )}
    {exercise(
        3,
        "Цветная мандала",
        "Добавьте <code class=\"inline\">artist.pencolor(\"violet\")</code> перед циклом и "
        "поэкспериментируйте с другими цветами.",
    )}

    {local_required_card(
        "06-08",
        "Практика: мандала из прямых линий",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-08/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Экран (<code class=\"inline\">turtle.Screen()</code>) и черепашка "
        "(<code class=\"inline\">turtle.Turtle()</code>) — два разных объекта.",
        "<code class=\"inline\">forward()</code>/<code class=\"inline\">backward()</code> "
        "двигают черепашку; <code class=\"inline\">left()</code>/<code class=\"inline\">right()"
        "</code> поворачивают её курс относительно текущего направления.",
        "<code class=\"inline\">setheading()</code> задаёт направление абсолютно, "
        "<code class=\"inline\">home()</code> возвращает черепашку в начало координат.",
        "Угол поворота для правильного многоугольника — "
        "<code class=\"inline\">360 / количество_сторон</code>.",
        "<code class=\"inline\">goto(x, y)</code> перемещает черепашку в конкретную точку "
        "экрана; <code class=\"inline\">penup()</code>/<code class=\"inline\">pendown()</code> "
        "управляют тем, рисуется ли линия при движении.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — мандала из прямых линий",
        description="Итоговый мини-проект главы 6: мандала из прямых линий — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Мандала и итоги", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Мини-проект — рисуем мандалу только из прямых линий",
        lede="Собираем все приёмы главы в одном узоре — и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("06-08-mandala-itogi.html"),
        nav=PageNav(prev_href="06-07-goto-kvadrat.html", prev_label="Квадрат с помощью goto", next_href="../glava-07/index.html", next_label="Глава 7: Глубокое погружение в Turtle"),
    )
    write("06-08-mandala-itogi.html", out)


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
