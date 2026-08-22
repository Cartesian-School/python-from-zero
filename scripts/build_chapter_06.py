#!/usr/bin/env python3
"""Строит Главу 6: «Рисуем классные вещи с помощью Turtle» (site/chapters/glava-06/).

Curriculum v2: от короткой главы про движение и повороты до полноценного
визуального курса — координаты, направление и углы, многоугольники и
формула 360/n, перо и заливка, цвет, круги/дуги/точки, случайная графика,
рисование по координатам, отладка Turtle и пять мини-проектов, включая
финальную мандалу. Каждый существенный пример показывает РЕАЛЬНЫЙ
выполненный результат (см. chapter_06_examples.py и
generate_chapter_06_outputs.py) — ни одна картинка не нарисована вручную.

Существующие маршруты и практики (06-01..06-08, id 06-02/03/04/06/07/08)
сохранены и расширены на месте; новый материал — новые страницы.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_06_examples import EXAMPLES
from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    axis_compass_diagram,
    callout,
    classic_vs_modern,
    code_block,
    comparison_table,
    decision_map,
    exercise,
    local_required_card,
    math_inline,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-06"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Приступаем (обзор главы)"),
    ("06-01-pristupaem.html", "Приступаем"),
    ("06-09-koordinaty.html", "Координаты: центр (0, 0)"),
    ("06-02-dvizhenie-vpered-nazad.html", "Заставляем Turtle двигаться"),
    ("06-10-napravlenie-i-ugol.html", "Направление и угол"),
    ("06-03-povorot-cherepashki.html", "Меняем направление"),
    ("06-11-pervye-figury.html", "Первые фигуры и формула 360/n"),
    ("06-04-mini-proekty-figury.html", "Мини-проекты: квадрат и шестиугольник"),
    ("06-05-sokraschennye-priemy.html", "Сокращённые приёмы"),
    ("06-12-pero-vverh-vniz.html", "Поднять и опустить перо"),
    ("06-07-goto-kvadrat.html", "goto() и координатная панель"),
    ("06-13-cvet-tolschina-vid.html", "Цвет, толщина и внешний вид"),
    ("06-14-zalivka-krug-tochka.html", "Заливка, круг, дуга и точка"),
    ("06-06-sluchaynye-tochki.html", "Случайные точки на экране"),
    ("06-15-sluchaynoe-dvizhenie.html", "Случайное движение"),
    ("06-16-risuem-po-koordinatam.html", "Рисуем по координатам"),
    ("06-17-otladka-turtle.html", "Отладка Turtle"),
    ("06-18-mini-proekty.html", "Мини-проекты"),
    ("06-08-mandala-itogi.html", "Мандала и итоги"),
]

PRACTICE_IDS = [
    "06-02", "06-09", "06-10", "06-19", "06-03", "06-11", "06-20", "06-04",
    "06-12", "06-07", "06-13", "06-14", "06-06", "06-15", "06-16", "06-17",
    "06-18", "06-08",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 6 · Turtle", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def turtle_output(name: str, filename: str, *, caption: str, alt: str) -> str:
    """КОД → РЕАЛЬНЫЙ OUTPUT: code_block() слева/сверху, реально выполненная
    картинка справа/снизу (см. chapter_06_examples.EXAMPLES — тот же код,
    что показан здесь, был буквально выполнен генератором, чтобы получить
    этот PNG). Код в примере не содержит exitonclick()/bye() — этот вызов
    мы дописываем только для читателя, для локального запуска."""
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
          <img src="{IMG}/chapter-06/output/{name}.png" alt="{alt}"
            style="width:100%;height:auto;border-radius:12px;display:block;background:#fff" />
          <figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>
        </figure>
      </div>
    </div>"""


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=6,
        baseline_page=83,
        title="Рисуем классные вещи с помощью Turtle",
        description="Первая настоящая графика на Python: координаты, движение и повороты, "
        "многоугольники, перо и заливка, круги и цвета, случайная графика — и мандала в финале. "
        "Каждый пример показывает по-настоящему выполненный рисунок, а не описание того, что "
        "должно получиться.",
        meta_items=["⏱ ~4–5 часов", "💻 модуль turtle", "📓 18 практик", "🖼 реальные результаты у каждого примера"],
        sections=[
            ChapterSectionLink("6.1", "Приступаем", "06-01-pristupaem.html", "83"),
            ChapterSectionLink("6.2", "Координаты: центр (0, 0)", "06-09-koordinaty.html", "85"),
            ChapterSectionLink("6.3", "Заставляем Turtle двигаться", "06-02-dvizhenie-vpered-nazad.html", "87"),
            ChapterSectionLink("6.4", "Направление и угол", "06-10-napravlenie-i-ugol.html", "90"),
            ChapterSectionLink("6.5", "Меняем направление", "06-03-povorot-cherepashki.html", "92"),
            ChapterSectionLink("6.6", "Первые фигуры и формула 360/n", "06-11-pervye-figury.html", "94"),
            ChapterSectionLink("6.7", "Мини-проекты: квадрат и шестиугольник", "06-04-mini-proekty-figury.html", "97"),
            ChapterSectionLink("6.8", "Сокращённые приёмы", "06-05-sokraschennye-priemy.html", "99"),
            ChapterSectionLink("6.9", "Поднять и опустить перо", "06-12-pero-vverh-vniz.html", "100"),
            ChapterSectionLink("6.10", "goto() и координатная панель", "06-07-goto-kvadrat.html", "102"),
            ChapterSectionLink("6.11", "Цвет, толщина и внешний вид", "06-13-cvet-tolschina-vid.html", "105"),
            ChapterSectionLink("6.12", "Заливка, круг, дуга и точка", "06-14-zalivka-krug-tochka.html", "108"),
            ChapterSectionLink("6.13", "Случайные точки на экране", "06-06-sluchaynye-tochki.html", "111"),
            ChapterSectionLink("6.14", "Случайное движение", "06-15-sluchaynoe-dvizhenie.html", "113"),
            ChapterSectionLink("6.15", "Рисуем по координатам", "06-16-risuem-po-koordinatam.html", "115"),
            ChapterSectionLink("6.16", "Отладка Turtle", "06-17-otladka-turtle.html", "117"),
            ChapterSectionLink("6.17", "Мини-проекты", "06-18-mini-proekty.html", "119"),
            ChapterSectionLink("6.18", "Мандала и итоги", "06-08-mandala-itogi.html", "123"),
        ],
    )
    write("index.html", out)


def state_card(*, position: str, heading: str, pen: str, color: str = "", width: str = "") -> str:
    """Небольшая повторяющаяся панель «состояние черепашки» — готовит к
    идее объектов с состоянием задолго до главы про ООП."""
    rows = [("position", position), ("heading", heading), ("pen", pen)]
    if color:
        rows.append(("color", color))
    if width:
        rows.append(("width", width))
    rows_html = "".join(
        f'<div style="display:flex;justify-content:space-between;padding:6px 0;'
        f'border-bottom:1px solid var(--color-border-default,#E4E1F5);font-family:\'JetBrains Mono\',monospace;font-size:13px">'
        f'<span style="color:var(--ink-soft,#6B6B7D)">{k}</span><span style="color:#0D0230;font-weight:700">{v}</span></div>'
        for k, v in rows
    )
    return (
        '<div style="max-width:280px;margin:20px 0;padding:16px 18px;background:var(--color-bg-surface,#FAFAFC);'
        'border-radius:var(--radius-lg,16px);border:1.5px solid #5B24F9">'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;'
        'text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Состояние черепашки</div>'
        f'{rows_html}</div>'
    )


def build_01_pristupaem() -> None:
    output = turtle_output(
        "06-01-screen-turtle", "screen_i_cherepashka.py",
        caption="Пустое окно 480×360 с черепашкой в начале координат, курс направлен вправо",
        alt="Белое окно Turtle с маленьким чёрным треугольником-черепашкой в центре, направленным вправо",
    )
    card = state_card(position="(0, 0)", heading="0° (восток)", pen="down")
    body = f"""
    <p>Модуль <code class="inline">turtle</code> входит в стандартную поставку Python — ничего
    дополнительно устанавливать не нужно.</p>

    <h2>Немного истории</h2>
    <p>Идея «черепашьей графики» появилась в конце 1960-х в языке Logo, который придумали Сеймур
    Пейперт и его коллеги специально для обучения детей программированию. Мысль была простой и
    сильной: пусть код будет виден — не абстрактные числа на экране, а линия, которую оставляет за
    собой воображаемая черепашка. Эта идея настолько удачная, что дожила до наших дней почти без
    изменений — модуль <code class="inline">turtle</code> в Python прямой потомок той самой Logo-черепашки.</p>

    <h2>Экран и черепашка — два разных объекта</h2>
    <p>Прежде чем рисовать, нужны два объекта: <strong>экран</strong>
    (<code class="inline">turtle.Screen()</code>) — окно, в котором происходит рисование, и
    <strong>черепашка</strong> (<code class="inline">turtle.Turtle()</code>) — то, что, собственно,
    рисует.</p>
{output}
    <p>Маленький чёрный треугольник в центре — это и есть черепашка в исходном положении. Курс
    (направление) черепашки по умолчанию направлен вправо — на восток.</p>
{card}

    <h2>У черепашки есть состояние</h2>
    <p>Заметьте: у черепашки в любой момент есть несколько характеристик одновременно — где она
    находится (<em>позиция</em>), куда смотрит (<em>курс</em>), и рисует ли она сейчас
    (<em>перо</em>). Каждая команда, которую мы будем изучать в этой главе, меняет какую-то одну из
    этих характеристик, не трогая остальные. Мы будем возвращаться к этой панели состояния на
    протяжении всей главы.</p>

{callout(
        "info",
        "Зачем два отдельных объекта?",
        "Разделение экрана и черепашки позволяет иметь на одном экране сразу <strong>несколько"
        "</strong> черепашек — у каждой будет своё собственное состояние, независимое от остальных.",
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
        description="Первое знакомство с модулем turtle: немного истории, экран и черепашка, состояние черепашки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Приступаем", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Приступаем",
        lede="Знакомимся с двумя главными объектами графики Turtle — экраном и самой черепашкой — "
        "и с идеей, что у черепашки есть состояние.",
        body_html=body,
        sidebar_groups=sidebar("06-01-pristupaem.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="06-09-koordinaty.html", next_label="Координаты: центр (0, 0)"),
    )
    write("06-01-pristupaem.html", out)


def build_09_koordinaty() -> None:
    output = turtle_output(
        "06-09-axes", "koordinaty.py",
        caption="Оси, начало координат (0, 0) и точка (120, 80), отмеченные прямо в окне Turtle",
        alt="Окно Turtle с горизонтальной и вертикальной осью, пересекающимися в центре, и двумя подписанными точками: (0, 0) и (120, 80)",
    )
    body = f"""
    <p>Мы уже встречали координаты в главе 5 — точки на плоскости с координатами x и y. Окно
    Turtle устроено ровно по той же системе, и она будет буквально управлять тем, что рисует
    черепашка.</p>

    <h2>Центр экрана — точка (0, 0)</h2>
    <p>В отличие от многих других графических систем (где ось Y растёт <em>вниз</em>), Turtle
    использует привычную математическую систему координат:</p>
{axis_compass_diagram(caption="Центр окна — точка (0, 0). Ось X растёт вправо, ось Y растёт вверх.")}
    <ul>
      <li><strong>x</strong> — горизонталь: положительные значения вправо, отрицательные влево.</li>
      <li><strong>y</strong> — вертикаль: положительные значения вверх, отрицательные вниз.</li>
      <li>Центр окна — точка <code class="inline">(0, 0)</code>, где черепашка появляется по умолчанию.</li>
    </ul>
{comparison_table(
        ["Координата", "Куда указывает"],
        [
            ["<code class=\"inline\">(100, 0)</code>", "вправо от центра"],
            ["<code class=\"inline\">(-100, 0)</code>", "влево от центра"],
            ["<code class=\"inline\">(0, 100)</code>", "вверх от центра"],
            ["<code class=\"inline\">(0, -100)</code>", "вниз от центра"],
        ],
    )}

    <h2>Координаты на самом деле управляют окном</h2>
    <p>Это не просто абстрактная схема — координатная система по-настоящему определяет, куда
    черепашка попадёт, если её туда отправить:</p>
{output}
{callout(
        "tip",
        "write() — подписать точку на экране",
        "В примере выше использована команда <code class=\"inline\">artist.write(\"текст\")</code> — "
        "она печатает текст в текущей позиции черепашки. Удобно для подписи точек на схемах, как "
        "здесь.",
    )}

{practice_card(
        "06-09",
        "Практика: координаты и goto()",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-09/index.html",
    )}
    """
    out = render_page(
        page_title="Координаты: центр (0, 0)",
        description="Система координат окна Turtle: центр (0, 0), ось X вправо, ось Y вверх — с реальным примером на экране.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Координаты", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Координаты: центр (0, 0)",
        lede="Числа из главы 5 становятся местом на экране — знакомимся с координатной системой "
        "окна Turtle.",
        body_html=body,
        sidebar_groups=sidebar("06-09-koordinaty.html"),
        nav=PageNav(prev_href="06-01-pristupaem.html", prev_label="Приступаем", next_href="06-02-dvizhenie-vpered-nazad.html", next_label="Заставляем Turtle двигаться"),
    )
    write("06-09-koordinaty.html", out)


def build_02_dvizhenie() -> None:
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
        "зато сразу готовит вас к главе про объекты и легко масштабируется — если позже "
        "понадобится нарисовать сцену из нескольких черепашек, у каждой будет своё имя и своё "
        "состояние. Модульные функции (<code class=\"inline\">turtle.forward()</code> без объекта) "
        "всё ещё встречаются в старом коде и учебниках — знать их полезно, но начинайте привычку "
        "сразу с объекта.",
    )

    fwd = turtle_output(
        "06-02-forward-120", "vpered_120.py",
        caption="artist.forward(120) — черепашка проехала 120 пикселей вправо, оставив линию",
        alt="Прямая фиолетовая линия длиной 120 пикселей от центра окна вправо, с черепашкой на конце",
    )
    fwd_bk = turtle_output(
        "06-02-forward-backward", "vpered_nazad.py",
        caption="Тот же forward(120), затем backward(50) — черепашка отступила назад по той же линии",
        alt="Та же линия, но короче — черепашка вернулась на 50 пикселей назад по прямой",
    )
    letter_g = turtle_output(
        "06-02-letter-g", "bukva_g.py",
        caption="forward(120), left(90), forward(80) — получилась буква «Г»",
        alt="Уголок из двух отрезков в форме буквы Г, нарисованный черепашкой",
    )

    body = f"""
    <h2>Зачем это нужно</h2>
    <p>Всё, что вы нарисуете дальше — многоугольники, дома, мандалы — строится из одной и той же
    пары действий: <strong>«проехать немного»</strong> и <strong>«повернуть на какой-то угол»</strong>.
    Освоив четыре команды этого раздела, вы получите строительные блоки для всей главы.</p>

    <h2>Синтаксис</h2>
    <ul>
      <li><code class="inline">forward(расстояние)</code> — проехать вперёд на указанное число пикселей (короткая форма — <code class="inline">fd</code>)</li>
      <li><code class="inline">backward(расстояние)</code> — проехать назад, не поворачиваясь (короткие формы — <code class="inline">bk</code>, <code class="inline">back</code>)</li>
      <li><code class="inline">right(угол)</code> — повернуть по часовой стрелке на угол в градусах (короткая форма — <code class="inline">rt</code>)</li>
      <li><code class="inline">left(угол)</code> — повернуть против часовой стрелки на угол в градусах (короткая форма — <code class="inline">lt</code>)</li>
    </ul>

    <h2>Первый шаг: просто вперёд</h2>
{fwd}

    <h2>Вперёд, потом назад</h2>
{fwd_bk}
{callout(
        "tip",
        "Совет",
        "Числа в <code class=\"inline\">forward()</code> тоже могут быть отрицательными. "
        "<code class=\"inline\">forward(-50)</code> и <code class=\"inline\">backward(50)</code> "
        "делают одно и то же.",
    )}

    <h2>Первая настоящая программа: буква «Г»</h2>
    <p>Проедем вперёд, повернём и проедем ещё раз:</p>
{letter_g}
    <h3>Разбор по шагам</h3>
    <ul>
      <li><code class="inline">turtle.Screen()</code> открывает окно для рисования.</li>
      <li><code class="inline">turtle.Turtle()</code> создаёт саму черепашку — в начале координат, курс направлен вправо.</li>
      <li><code class="inline">artist.forward(120)</code> — черепашка проезжает 120 пикселей в направлении курса, оставляя линию.</li>
      <li><code class="inline">artist.left(90)</code> — курс поворачивается на 90° против часовой стрелки.</li>
      <li>Второй вызов <code class="inline">forward()</code> едет уже в новом направлении — отсюда и уголок буквы «Г».</li>
    </ul>

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

    <h2>Попробуйте изменить</h2>
{exercise(1, "Другое расстояние и угол", "Измените расстояние 120 на 250 и угол 90 на 45. Перед запуском попробуйте предсказать: в какую сторону теперь «смотрит» черепашка после поворота?")}
{exercise(2, "Третий отрезок", "Добавьте третью пару команд left(90) и forward(120) в конец программы. Какая фигура получится?")}

    <h2>Современный вариант</h2>
    <p>В старом коде черепашку часто рисуют без явного объекта — модуль
    <code class="inline">turtle</code> автоматически создаёт «черепашку по умолчанию».</p>
{cvm}

{local_required_card(
        "06-02",
        "Практика: эксперименты, задание и самостоятельная практика",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-02/index.html",
    )}

{summary_box("Что запомнить", [
        "<code class=\"inline\">forward()</code>/<code class=\"inline\">backward()</code> "
        "двигают черепашку по прямой; <code class=\"inline\">left()</code>/"
        "<code class=\"inline\">right()</code> только поворачивают курс.",
        "Позиция и курс — это два независимых свойства черепашки.",
        "Современный стиль — создавать явный объект <code class=\"inline\">turtle.Turtle()</code>, "
        "а не полагаться на скрытую черепашку по умолчанию.",
    ])}
    """
    out = render_page(
        page_title="Движение вперёд и назад",
        description="Учимся управлять черепашкой Turtle: forward, backward, right, left — с реальным выполненным результатом у каждого примера.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Движение вперёд и назад", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Движение вперёд и назад",
        lede="Первое, что должна уметь черепашка — двигаться. В этом разделе вы напишете свою "
        "первую программу, которая по-настоящему рисует.",
        body_html=body,
        sidebar_groups=sidebar("06-02-dvizhenie-vpered-nazad.html"),
        nav=PageNav(prev_href="06-09-koordinaty.html", prev_label="Координаты", next_href="06-10-napravlenie-i-ugol.html", next_label="Направление и угол"),
    )
    write("06-02-dvizhenie-vpered-nazad.html", out)


def build_10_napravlenie() -> None:
    heading_states = turtle_output(
        "06-10-heading-states", "chetyre_napravleniya.py",
        caption="Одна и та же точка (0, 0) — четыре разных курса, отмеченных отрезком и штампом черепашки",
        alt="Четыре цветных отрезка из центра окна в четырёх направлениях — вправо, вверх, влево, вниз — подписанные 0°, 90°, 180°, 270°",
    )
    before_after = (
        '<div style="display:flex;gap:20px;flex-wrap:wrap;margin:20px 0">'
        + state_card(position="(0, 0)", heading="0° (восток)", pen="down")
        + '<div style="display:flex;align-items:center;font-size:22px;color:#B9A0FC">→ left(90) →</div>'
        + state_card(position="(0, 0)", heading="90° (север)", pen="down")
        + '</div>'
    )
    body = f"""
    <p>Важно различать две вещи, которые легко перепутать: <strong>позицию</strong> черепашки
    (где она находится) и её <strong>курс</strong> (куда она смотрит). Черепашка может стоять в
    одной и той же точке и при этом смотреть в четыре совершенно разные стороны.</p>

    <h2>Четыре состояния в одной точке</h2>
{heading_states}

    <h2>Поворот меняет курс, но не позицию</h2>
    <p>Вот что происходит с состоянием черепашки при повороте — обратите внимание, что
    <code class="inline">position</code> не изменилась ни на пиксель:</p>
{before_after}

    <h2>Углы из главы 5</h2>
    <p>Мы уже встречали эти углы в главе 5, когда говорили о тригонометрии и единичной окружности
    — теперь они управляют направлением черепашки напрямую:</p>
{comparison_table(
        ["Угол", "Что означает для черепашки"],
        [
            ["360°", "полный оборот — черепашка снова смотрит туда же, откуда начала"],
            ["180°", "разворот — черепашка смотрит строго в противоположную сторону"],
            ["90°", "четверть оборота — прямой угол, курс становится перпендикулярным"],
            ["45°", "половина прямого угла — курс «по диагонали»"],
        ],
    )}
{callout(
        "info",
        "Направление в градусах, начиная с востока",
        "В Turtle 0° — это восток (курс по умолчанию), и градусы растут против часовой стрелки: "
        "90° — север, 180° — запад, 270° — юг. Это тот же принцип, что и на единичной окружности "
        "из главы 5.",
    )}

{practice_card(
        "06-10",
        "Практика: направление и состояние черепашки",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-10/index.html",
    )}
{practice_card(
        "06-19",
        "Практика: предскажите курс и координату (без Turtle)",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/06-19/index.html",
    )}
    """
    out = render_page(
        page_title="Направление и угол",
        description="Позиция и курс черепашки — два независимых свойства. Разбираемся с направлением в градусах и связью с углами из главы 5.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Направление и угол", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Направление и угол",
        lede="Черепашка может стоять на месте и смотреть в четыре разные стороны — разбираемся, "
        "чем курс отличается от позиции.",
        body_html=body,
        sidebar_groups=sidebar("06-10-napravlenie-i-ugol.html"),
        nav=PageNav(prev_href="06-02-dvizhenie-vpered-nazad.html", prev_label="Заставляем Turtle двигаться", next_href="06-03-povorot-cherepashki.html", next_label="Меняем направление"),
    )
    write("06-10-napravlenie-i-ugol.html", out)


def build_03_povorot() -> None:
    output = turtle_output(
        "06-03-setheading-home", "setheading.py",
        caption="setheading(90) → forward(100), затем setheading(180) → forward(100) — курс задан абсолютно, независимо от предыдущего направления",
        alt="Два перпендикулярных отрезка — один вверх, один влево — образующие прямой угол, начатые из одной точки",
    )
    body = f"""
    <p>Команды <code class="inline">left()</code>/<code class="inline">right()</code> из
    предыдущего раздела поворачивают черепашку <strong>относительно</strong> её текущего курса.
    Иногда удобнее задать направление <strong>абсолютно</strong> — «смотри строго на север»,
    независимо от того, куда черепашка смотрела раньше.</p>

    <h2>Абсолютный курс: <code class="inline">setheading()</code></h2>
{output}
{code_block("setheading_kod.py", 'artist.setheading(90)   # смотрим строго вверх, неважно, куда смотрели раньше\nartist.forward(100)\n\nartist.setheading(180)  # смотрим строго влево\nartist.forward(100)\n')}

    <h2>Возврат домой: <code class="inline">home()</code></h2>
    <p>Возвращает черепашку в исходную точку (0, 0) с исходным курсом (0°) — удобно, чтобы
    начать рисунок заново, не создавая нового объекта:</p>
{code_block("home.py", "artist.home()\n")}

{callout(
        "tip",
        "heading() — узнать текущий курс",
        "Если нужно не задать курс, а <em>узнать</em> его — используйте "
        "<code class=\"inline\">artist.heading()</code>: она возвращает текущее направление в "
        "градусах, не меняя его. У <code class=\"inline\">setheading()</code> есть и короткий "
        "псевдоним — <code class=\"inline\">seth()</code>.",
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
        description="Абсолютное направление в Turtle: setheading(), heading() и home() — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Меняем направление", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Заставляем черепашку менять направление",
        lede="Кроме относительных поворотов left()/right(), у черепашки есть способ задать "
        "направление абсолютно — вне зависимости от того, куда она смотрела раньше.",
        body_html=body,
        sidebar_groups=sidebar("06-03-povorot-cherepashki.html"),
        nav=PageNav(prev_href="06-10-napravlenie-i-ugol.html", prev_label="Направление и угол", next_href="06-11-pervye-figury.html", next_label="Первые фигуры и формула 360/n"),
    )
    write("06-03-povorot-cherepashki.html", out)


def build_11_pervye_figury() -> None:
    triangle = turtle_output(
        "06-11-triangle", "treugolnik.py",
        caption="Правильный треугольник — три поворота по 120°",
        alt="Равносторонний треугольник, нарисованный сплошной фиолетовой линией",
    )
    rectangle = turtle_output(
        "06-11-rectangle", "pryamougolnik.py",
        caption="Прямоугольник — стороны разной длины, все повороты по 90°",
        alt="Прямоугольник шире, чем выше, нарисованный сплошной фиолетовой линией",
    )
    pentagon = turtle_output(
        "06-11-pentagon", "pyatiugolnik.py",
        caption="Правильный пятиугольник — пять поворотов по 72°",
        alt="Правильный пятиугольник, нарисованный сплошной фиолетовой линией",
    )
    formula_tree = comparison_table(
        ["Фигура", "Сторон (n)", "Поворот = 360 / n"],
        [
            ["Треугольник", "3", "120°"],
            ["Квадрат", "4", "90°"],
            ["Пятиугольник", "5", "72°"],
            ["Шестиугольник", "6", "60°"],
        ],
    )
    body = f"""
    <p>Применим движение и повороты, чтобы нарисовать первые настоящие фигуры — пока без циклов,
    просто повторяя одну и ту же пару команд нужное число раз.</p>

    <h2>Треугольник</h2>
    <p>У треугольника три стороны и три угла поворота. Сумма всех внешних углов любого
    многоугольника всегда равна 360°, поэтому один поворот здесь — <code class="inline">360 / 3 = 120</code> градусов:</p>
{triangle}

    <h2>Прямоугольник</h2>
    <p>У прямоугольника углы всё ещё прямые (90°), но стороны чередуются — длинная, короткая,
    длинная, короткая:</p>
{rectangle}

    <h2>Пятиугольник</h2>
{pentagon}

    <h2>Формула для любого правильного многоугольника</h2>
    <p>Общее правило, которое работает для всех фигур выше:</p>
{math_inline(("row", "поворот", ("mo", "="), ("frac", "360", "n")))}
    <p>где <code class="inline">n</code> — число сторон. Каждый раз, когда черепашка обходит
    правильный многоугольник по кругу и возвращается в исходную точку с исходным курсом, сумма
    всех поворотов обязана составить ровно один полный оборот — 360°.</p>
{formula_tree}
{callout(
        "info",
        "Квадрат и шестиугольник — в следующем разделе",
        "Мы намеренно оставили квадрат (360 / 4 = 90°) и шестиугольник (360 / 6 = 60°) для "
        "следующего мини-проекта — там разберём их подробнее.",
    )}

{local_required_card(
        "06-11",
        "Практика: первые фигуры",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-11/index.html",
    )}
{practice_card(
        "06-20",
        "Практика: формула 360/n (без Turtle)",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/06-20/index.html",
    )}
    """
    out = render_page(
        page_title="Первые фигуры и формула 360/n",
        description="Рисуем треугольник, прямоугольник и пятиугольник, выводим формулу поворота 360/n для правильных многоугольников.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Первые фигуры", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Первые фигуры и формула 360/n",
        lede="От отдельных отрезков — к настоящим многоугольникам, и к формуле, которая объясняет "
        "их все разом.",
        body_html=body,
        sidebar_groups=sidebar("06-11-pervye-figury.html"),
        nav=PageNav(prev_href="06-03-povorot-cherepashki.html", prev_label="Меняем направление", next_href="06-04-mini-proekty-figury.html", next_label="Мини-проекты: квадрат и шестиугольник"),
    )
    write("06-11-pervye-figury.html", out)


def build_04_mini_proekty() -> None:
    kvadrat = turtle_output(
        "06-04-kvadrat", "kvadrat.py",
        caption="Квадрат: четыре стороны по 100 пикселей, четыре поворота по 90°",
        alt="Правильный квадрат, нарисованный сплошной фиолетовой линией",
    )
    hexagon = turtle_output(
        "06-04-shestiugolnik", "shestiugolnik.py",
        caption="Шестиугольник: шесть сторон по 80 пикселей, шесть поворотов по 60°",
        alt="Правильный шестиугольник, нарисованный сплошной фиолетовой линией",
    )
    body = f"""
    <p>Применим формулу <code class="inline">360 / n</code> из предыдущего раздела к двум самым
    узнаваемым фигурам.</p>

    <h2>Мини-проект — рисуем квадрат</h2>
    <p>У квадрата четыре одинаковые стороны и четыре угла по 90°: <code class="inline">360 / 4 = 90</code>.
    Значит, нужно четыре раза повторить одну и ту же пару команд: проехать вперёд, повернуть на 90°.</p>
{kvadrat}
{callout(
        "tip",
        "Заметили повторение?",
        "Четыре одинаковых блока подряд — явный признак того, что напрашивается цикл "
        "<code class=\"inline\">for</code>. Мы вернёмся к этому же квадрату в главе про циклы и "
        "перепишем его в 2 строки вместо 8.",
    )}

    <h2>Мини-проект — рисуем шестиугольник</h2>
    <p>У шестиугольника шесть равных сторон: <code class="inline">360 / 6 = 60</code> градусов на
    каждом шаге.</p>
{hexagon}

{local_required_card(
        "06-04",
        "Практика: квадрат, шестиугольник и другие многоугольники",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-04/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проекты: квадрат и шестиугольник",
        description="Рисуем квадрат и шестиугольник, применяя формулу поворота 360/n — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Мини-проекты: фигуры", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Мини-проект — рисуем квадрат и шестиугольник",
        lede="Применяем формулу 360/n к двум самым узнаваемым многоугольникам.",
        body_html=body,
        sidebar_groups=sidebar("06-04-mini-proekty-figury.html"),
        nav=PageNav(prev_href="06-11-pervye-figury.html", prev_label="Первые фигуры", next_href="06-05-sokraschennye-priemy.html", next_label="Сокращённые приёмы"),
    )
    write("06-04-mini-proekty-figury.html", out)


def build_05_sokraschennye() -> None:
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
    oformlenie = turtle_output(
        "06-05-oformlenie", "oformlenie.py",
        caption="pencolor(\"purple\") и pensize(6) — толстая фиолетовая линия вместо тонкой чёрной по умолчанию",
        alt="Толстая фиолетовая горизонтальная линия",
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

    <h2>Первый взгляд на оформление линии</h2>
    <p>Помимо движения, есть ещё две команды, которые встретятся уже в следующих разделах —
    познакомимся с ними коротко прямо сейчас:</p>
{oformlenie}
{code_block("oformlenie_kod.py", 'artist.pencolor("purple")   # цвет линии\nartist.pensize(6)            # толщина линии\n')}

{local_required_card(
        "06-04",
        "Практика: включает практику с короткими командами",
        "Тот же ноутбук, что и в разделе «Мини-проекты: фигуры» — он охватывает и эту тему",
        "../../practice/06-04/index.html",
    )}
    """
    out = render_page(
        page_title="Сокращённые приёмы",
        description="Короткие псевдонимы команд Turtle: fd, bk, lt, rt — и первое знакомство с цветом и толщиной линии.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Сокращённые приёмы", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Сокращённые приёмы",
        lede="Каждая команда движения имеет более короткий псевдоним — полезно уметь читать оба "
        "варианта.",
        body_html=body,
        sidebar_groups=sidebar("06-05-sokraschennye-priemy.html"),
        nav=PageNav(prev_href="06-04-mini-proekty-figury.html", prev_label="Мини-проекты: фигуры", next_href="06-12-pero-vverh-vniz.html", next_label="Поднять и опустить перо"),
    )
    write("06-05-sokraschennye-priemy.html", out)


def build_12_pero() -> None:
    output = turtle_output(
        "06-12-pen-up-down", "pero.py",
        caption="Линия — пробел — линия: penup() между двумя движениями оставляет видимый разрыв",
        alt="Два коротких фиолетовых отрезка на одной прямой с явным пробелом между ними — след от поднятого пера",
    )
    body = f"""
    <p>До сих пор каждое движение черепашки оставляло линию. Но иногда нужно переместиться, ничего
    не рисуя — например, чтобы начать новую фигуру в другом месте экрана, не соединяя её с
    предыдущей.</p>

    <h2>Мысленная модель</h2>
    <p>Представьте настоящую ручку на бумаге: пока она касается листа, любое движение руки
    оставляет след. Поднимите ручку — и рука может двигаться куда угодно, не оставляя ни одной
    линии.</p>

    <h2><code class="inline">penup()</code> и <code class="inline">pendown()</code></h2>
{output}
{code_block("pero_kod.py", "artist.forward(60)      # перо опущено — рисует\nartist.penup()\nartist.forward(60)      # перо поднято — просто перемещение, без линии\nartist.pendown()\nartist.forward(60)      # перо снова опущено — рисует\n")}
{callout(
        "warning",
        "Не забудьте включить перо обратно",
        "Самая частая ошибка с <code class=\"inline\">penup()</code> — забыть вызвать "
        "<code class=\"inline\">pendown()</code> после него. Тогда всё, что рисуется дальше в "
        "программе, окажется невидимым — черепашка честно двигается, просто ничего не оставляет "
        "на экране.",
    )}
{callout(
        "tip",
        "isdown() — проверить состояние пера",
        "Если нужно узнать, опущено ли перо прямо сейчас — <code class=\"inline\">artist.isdown()</code> "
        "вернёт <code class=\"inline\">True</code> или <code class=\"inline\">False</code>, не "
        "меняя само состояние.",
    )}

{practice_card(
        "06-12",
        "Практика: penup() и pendown()",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-12/index.html",
    )}
    """
    out = render_page(
        page_title="Поднять и опустить перо",
        description="penup() и pendown() в Turtle — перемещение без рисования, с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Перо вверх/вниз", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Поднять и опустить перо",
        lede="Иногда нужно переместиться, ничего не рисуя — знакомимся с penup() и pendown().",
        body_html=body,
        sidebar_groups=sidebar("06-12-pero-vverh-vniz.html"),
        nav=PageNav(prev_href="06-05-sokraschennye-priemy.html", prev_label="Сокращённые приёмы", next_href="06-07-goto-kvadrat.html", next_label="goto() и координатная панель"),
    )
    write("06-12-pero-vverh-vniz.html", out)


def build_07_goto() -> None:
    goto_square = turtle_output(
        "06-07-goto-square", "kvadrat_goto.py",
        caption="Тот же квадрат — на этот раз каждая вершина задана координатой напрямую, без единого поворота",
        alt="Правильный квадрат, нарисованный через goto() — визуально идентичен квадрату из предыдущего раздела",
    )
    navigation = turtle_output(
        "06-07-navigation", "navigacionnaya_panel.py",
        caption="Точка старта (0, 0) и точка после setx(150), sety(80) — обе отмечены и подписаны",
        alt="Две точки на экране: одна в центре подписана «старт (0, 0)», вторая правее и выше подписана координатами после setx/sety",
    )
    body = f"""
    <p>Вернёмся к квадрату из раздела про мини-проекты — на этот раз нарисуем его без единого
    поворота, задавая напрямую четыре угловые точки командой <code class="inline">goto()</code>.</p>

    <h2>Абсолютное перемещение: <code class="inline">goto(x, y)</code></h2>
{goto_square}
{code_block("kvadrat_goto_kod.py", "artist.goto(100, 0)\nartist.goto(100, 100)\nartist.goto(0, 100)\nartist.goto(0, 0)\n")}
{callout(
        "tip",
        "Два способа — один результат",
        "<code class=\"inline\">forward()</code> + <code class=\"inline\">right()</code> "
        "описывают движение <em>относительно черепашки</em> («проехать, повернуть»); "
        "<code class=\"inline\">goto()</code> описывает движение <em>относительно экрана</em> "
        "(«окажись в этой точке»). goto() удобен, когда координаты фигуры уже известны заранее.",
    )}

    <h2>Навигационная панель черепашки</h2>
    <p>Кроме <code class="inline">goto()</code>, у черепашки есть ещё несколько команд для работы
    с координатами напрямую:</p>
{comparison_table(
        ["Команда", "Что делает"],
        [
            ["<code class=\"inline\">position()</code> (или <code class=\"inline\">pos()</code>)", "вернуть текущие координаты (x, y)"],
            ["<code class=\"inline\">xcor()</code>", "вернуть только координату x"],
            ["<code class=\"inline\">ycor()</code>", "вернуть только координату y"],
            ["<code class=\"inline\">setx(x)</code>", "переместиться, изменив только x"],
            ["<code class=\"inline\">sety(y)</code>", "переместиться, изменив только y"],
            ["<code class=\"inline\">home()</code>", "вернуться в (0, 0) с курсом 0°"],
        ],
    )}
{navigation}
{code_block("navigaciya_kod.py", 'print(artist.position())   # текущие координаты\n\nartist.setx(150)\nartist.sety(80)\nprint(artist.position())   # координаты изменились по одной оси за раз\n')}

{local_required_card(
        "06-07",
        "Практика: рисуем фигуры через координаты",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-07/index.html",
    )}
    """
    out = render_page(
        page_title="goto() и координатная панель",
        description="Альтернативный способ рисовать фигуры в Turtle — через координаты точек: goto(), position(), setx(), sety().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("goto() и координаты", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="goto() и координатная панель",
        lede="Тот же квадрат, что и раньше, — но на этот раз через прямое указание координат "
        "каждого угла.",
        body_html=body,
        sidebar_groups=sidebar("06-07-goto-kvadrat.html"),
        nav=PageNav(prev_href="06-12-pero-vverh-vniz.html", prev_label="Перо вверх/вниз", next_href="06-13-cvet-tolschina-vid.html", next_label="Цвет, толщина и внешний вид"),
    )
    write("06-07-goto-kvadrat.html", out)


def build_13_cvet() -> None:
    thin = turtle_output(
        "06-13-thin-black", "tonkaya_chernaya.py",
        caption="pensize(1), pencolor(\"black\") — тонкая чёрная линия по умолчанию",
        alt="Тонкая чёрная горизонтальная линия",
    )
    thick = turtle_output(
        "06-13-thick-blue", "tolstaya_sinyaya.py",
        caption="pensize(10), pencolor(\"#2563EB\") — та же линия, но толстая и синяя",
        alt="Толстая синяя горизонтальная линия той же длины",
    )
    shape_bg = turtle_output(
        "06-13-shape-bgcolor", "vid_i_fon.py",
        caption="shape(\"turtle\") меняет курсор на силуэт черепашки; bgcolor() задаёт фон окна",
        alt="Уголок из двух отрезков, нарисованный черепашкой в форме силуэта черепахи вместо треугольника",
    )
    body = f"""
    <p>До сих пор мы рисовали фиолетовой линией по умолчанию. Пора научиться управлять тем, как
    именно выглядит рисунок — и как выглядит сама черепашка.</p>

    <h2>Толщина и цвет линии</h2>
    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div style="flex:1 1 280px">{thin}</div>
      <div style="flex:1 1 280px">{thick}</div>
    </div>
{code_block("cvet_i_tolschina.py", 'artist.pensize(10)\nartist.pencolor("#2563EB")\nartist.forward(220)\n')}
{callout(
        "tip",
        "Цвет можно задавать по-разному",
        "<code class=\"inline\">pencolor(\"blue\")</code> (имя цвета), "
        "<code class=\"inline\">pencolor(\"#2563EB\")</code> (шестнадцатеричный код, как в CSS) — "
        "оба варианта работают одинаково. Имена цветов проще запомнить, коды дают точный оттенок.",
    )}

    <h2>Внешний вид черепашки и фон окна</h2>
{shape_bg}
{code_block("vid_kod.py", 'screen.bgcolor("#FAFAFC")\nartist.shape("turtle")   # вместо треугольника-стрелки — силуэт черепахи\n')}
{comparison_table(
        ["Команда", "Что меняет"],
        [
            ["<code class=\"inline\">screen.title(\"...\")</code>", "заголовок окна"],
            ["<code class=\"inline\">screen.bgcolor(\"...\")</code>", "цвет фона"],
            ["<code class=\"inline\">artist.shape(\"turtle\")</code>", "форма курсора черепашки"],
            ["<code class=\"inline\">artist.hideturtle()</code> / <code class=\"inline\">showturtle()</code>", "скрыть/показать курсор (сама линия не исчезает)"],
        ],
    )}

    <h2>Скорость — это про анимацию, не про рисунок</h2>
    <p><code class="inline">artist.speed(0)</code> ускоряет анимацию рисования до максимума
    (0 — самая быстрая, 1 — самая медленная, 6 — обычная). Это касается только того,
    <strong>как быстро</strong> линия появляется на экране, — итоговый рисунок будет совершенно
    одинаковым что на скорости 1, что на скорости 0. Статичная картинка не может показать разницу
    в скорости — её видно только вживую, при запуске кода.</p>
{code_block("skorost.py", "artist.speed(0)   # максимально быстро — удобно для сложных узоров\n")}

{practice_card(
        "06-13",
        "Практика: цвет, толщина и внешний вид",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-13/index.html",
    )}
    """
    out = render_page(
        page_title="Цвет, толщина и внешний вид",
        description="pensize(), pencolor(), shape(), bgcolor() и speed() в Turtle — с реальным выполненным результатом каждого примера.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Цвет и внешний вид", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Цвет, толщина и внешний вид",
        lede="Управляем тем, как выглядит линия и сама черепашка — и разбираемся, что speed() "
        "меняет, а что нет.",
        body_html=body,
        sidebar_groups=sidebar("06-13-cvet-tolschina-vid.html"),
        nav=PageNav(prev_href="06-07-goto-kvadrat.html", prev_label="goto() и координаты", next_href="06-14-zalivka-krug-tochka.html", next_label="Заливка, круг, дуга и точка"),
    )
    write("06-13-cvet-tolschina-vid.html", out)


def build_14_zalivka() -> None:
    outline = turtle_output(
        "06-14-outline-triangle", "kontur_treugolnika.py",
        caption="Треугольник без заливки — только контурная линия",
        alt="Равносторонний треугольник, нарисованный только контуром, без заливки внутри",
    )
    filled = turtle_output(
        "06-14-filled-triangle", "zalityj_treugolnik.py",
        caption="Тот же треугольник, но begin_fill()/end_fill() закрасили область внутри контура",
        alt="Тот же равносторонний треугольник, но с закрашенной светло-фиолетовой заливкой внутри контура",
    )
    circle = turtle_output(
        "06-14-circle", "krug.py",
        caption="circle(80) — полная окружность радиусом 80 пикселей",
        alt="Правильная окружность, нарисованная сплошной фиолетовой линией",
    )
    arc = turtle_output(
        "06-14-arc", "duga.py",
        caption="circle(80, 90) — та же окружность, но только четверть (90° из 360°)",
        alt="Дуга — четверть окружности, нарисованная сплошной фиолетовой линией",
    )
    dots = turtle_output(
        "06-14-dots", "tochki.py",
        caption="dot() рисует точку заданного диаметра и цвета — без всякого движения черепашки",
        alt="Три цветных точки разного размера в ряд",
    )
    body = f"""
    <h2>Заливка фигур</h2>
    <p>Контур — это ещё не всё: часто фигуру хочется закрасить внутри. Для этого черепашке нужно
    «запомнить», где начинается контур, и «отпустить», когда контур замкнётся.</p>
{outline}
{filled}
{code_block("zalivka_kod.py", 'artist.pencolor("#5B24F9")\nartist.fillcolor("#B9A0FC")\n\nartist.begin_fill()\nartist.forward(140)\nartist.left(120)\nartist.forward(140)\nartist.left(120)\nartist.forward(140)\nartist.left(120)\nartist.end_fill()\n')}
{callout(
        "info",
        "Как это работает",
        "<code class=\"inline\">begin_fill()</code> запоминает точку старта. Затем обычные "
        "команды рисования (<code class=\"inline\">forward()</code>, <code class=\"inline\">left()</code> "
        "и другие) вычерчивают замкнутый контур, как обычно. <code class=\"inline\">end_fill()</code> "
        "закрашивает область внутри этого контура цветом <code class=\"inline\">fillcolor()</code>.",
    )}

    <h2><code class="inline">circle()</code> — готовая команда для окружностей</h2>
    <p>Рисовать круг вручную (много маленьких прямых под небольшим углом) не нужно — есть готовая
    команда:</p>
{circle}
{code_block("krug_kod.py", "artist.circle(80)   # радиус в пикселях\n")}

    <h2>Дуга — часть окружности</h2>
    <p>Второй, необязательный аргумент <code class="inline">circle()</code> — это
    <code class="inline">extent</code>, сколько градусов окружности рисовать:</p>
{arc}
{code_block("duga_kod.py", "artist.circle(80, 90)   # радиус 80, но только 90° из 360°\n")}

    <h2><code class="inline">dot()</code> — точка без движения</h2>
    <p>В отличие от всех предыдущих команд, <code class="inline">dot()</code> не двигает черепашку
    ни на пиксель — она просто ставит закрашенный кружок в текущей позиции:</p>
{dots}
{code_block("tochki_kod.py", 'artist.dot(20, "#5B24F9")\nartist.forward(100)\nartist.dot(30, "#DB2777")\n')}

{local_required_card(
        "06-14",
        "Практика: заливка, круг, дуга и точка",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-14/index.html",
    )}
    """
    out = render_page(
        page_title="Заливка, круг, дуга и точка",
        description="begin_fill()/end_fill(), circle() и dot() в Turtle — с реальным выполненным результатом каждого примера.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Заливка и круги", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Заливка, круг, дуга и точка",
        lede="От пустого контура — к закрашенным фигурам, готовым окружностям, дугам и точкам.",
        body_html=body,
        sidebar_groups=sidebar("06-14-zalivka-krug-tochka.html"),
        nav=PageNav(prev_href="06-13-cvet-tolschina-vid.html", prev_label="Цвет и внешний вид", next_href="06-06-sluchaynye-tochki.html", next_label="Случайные точки на экране"),
    )
    write("06-14-zalivka-krug-tochka.html", out)


def build_06_sluchaynye_tochki() -> None:
    output = turtle_output(
        "06-06-random-points", "sluchaynye_tochki.py",
        caption="10 случайных точек — при random.seed(7) каждый запуск даёт одну и ту же картину",
        alt="Десять фиолетовых точек, разбросанных по окну в случайных, но воспроизводимых местах",
    )
    body = f"""
    <p>До сих пор черепашка двигалась только относительно своей текущей позиции или по заранее
    известным координатам. Но можно сразу «телепортировать» её в конкретную точку экрана командой
    <code class="inline">goto(x, y)</code> — а вместе со случайными числами из главы 5 это
    открывает интересные возможности.</p>

    <h2>Случайные точки на экране</h2>
{output}
{code_block("sluchaynye_tochki_kod.py", 'import turtle\nimport random\n\nrandom.seed(7)   # фиксируем seed — картинка будет одинаковой при каждом запуске\nscreen = turtle.Screen()\nartist = turtle.Turtle()\nartist.penup()\n\nfor _ in range(10):\n    x = random.randint(-200, 200)\n    y = random.randint(-150, 150)\n    artist.goto(x, y)\n    artist.dot(14, "#5B24F9")\n')}
{callout(
        "warning",
        "penup() перед goto()",
        "Без <code class=\"inline\">penup()</code> черепашка будет рисовать линию при каждом "
        "перемещении <code class=\"inline\">goto()</code> — что обычно не то, что нужно для "
        "«прыжка» в новую точку перед тем, как поставить точку.",
    )}
{callout(
        "tip",
        "Зачем здесь random.seed(7)",
        "Мы разбирали <code class=\"inline\">random.seed()</code> в главе 5 — здесь она нужна "
        "именно затем, чтобы КАЖДЫЙ запуск этого кода давал одну и ту же картину, а не новую "
        "каждый раз. Уберите строку с seed — и точки станут по-настоящему случайными при каждом "
        "запуске.",
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
        description="goto(), penup()/pendown() и модуль random вместе — рисуем случайные точки на экране с фиксированным seed.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Случайные точки", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Переходим к случайным точкам на экране",
        lede="goto() перемещает черепашку в любую точку экрана напрямую — вместе со случайными "
        "числами получается интересный эффект.",
        body_html=body,
        sidebar_groups=sidebar("06-06-sluchaynye-tochki.html"),
        nav=PageNav(prev_href="06-14-zalivka-krug-tochka.html", prev_label="Заливка и круги", next_href="06-15-sluchaynoe-dvizhenie.html", next_label="Случайное движение"),
    )
    write("06-06-sluchaynye-tochki.html", out)


def build_15_sluchaynoe_dvizhenie() -> None:
    output = turtle_output(
        "06-15-random-walk", "sluchaynoe_dvizhenie.py",
        caption="«Случайное блуждание»: 40 маленьких шагов, каждый раз со случайным поворотом от −60° до 60°",
        alt="Извилистая фиолетовая линия, блуждающая по окну без определённого направления",
    )
    body = f"""
    <p>Комбинируя маленький шаг вперёд со случайным поворотом на каждой итерации, можно получить
    неповторяющуюся, органично выглядящую траекторию — приём, который называется «случайным
    блужданием» (random walk).</p>

    <h2>Идея — сначала без кода</h2>
    <p>Представьте: сделать маленький шаг, слегка повернуть в случайную сторону, снова шаг, снова
    случайный поворот — и так много раз подряд. Никакого плана, только повторение одного и того же
    маленького решения.</p>

{output}
{callout(
        "info",
        "🚀 Забегаем вперёд",
        "Код ниже использует цикл <code class=\"inline\">for</code> — мы разберём его подробно "
        "позже. Пока не нужно понимать синтаксис цикла целиком: важна сама идея — маленький шаг и "
        "случайный поворот, повторённые много раз.",
    )}
{code_block("sluchaynoe_dvizhenie_kod.py", 'import turtle\nimport random\n\nrandom.seed(3)   # фиксируем seed для воспроизводимой картинки\nscreen = turtle.Screen()\nartist = turtle.Turtle()\nartist.pensize(2)\nartist.pencolor("#5B24F9")\nartist.speed(0)\n\nfor _ in range(40):\n    artist.forward(15)\n    artist.right(random.randint(-60, 60))\n')}
{callout(
        "tip",
        "Попробуйте изменить",
        "Уберите <code class=\"inline\">random.seed(3)</code> — траектория станет новой при "
        "каждом запуске. Измените диапазон <code class=\"inline\">randint(-60, 60)</code> на "
        "более узкий, например <code class=\"inline\">(-15, 15)</code> — путь станет более "
        "прямым и предсказуемым.",
    )}

{practice_card(
        "06-15",
        "Практика: случайное движение",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-15/index.html",
    )}
    """
    out = render_page(
        page_title="Случайное движение",
        description="Random walk в Turtle: маленький шаг и случайный поворот, повторённые много раз — с фиксированным seed для воспроизводимости.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Случайное движение", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Случайное движение",
        lede="Маленький шаг и случайный поворот, повторённые много раз, — и получается извилистая, "
        "неповторяющаяся траектория.",
        body_html=body,
        sidebar_groups=sidebar("06-15-sluchaynoe-dvizhenie.html"),
        nav=PageNav(prev_href="06-06-sluchaynye-tochki.html", prev_label="Случайные точки", next_href="06-16-risuem-po-koordinatam.html", next_label="Рисуем по координатам"),
    )
    write("06-15-sluchaynoe-dvizhenie.html", out)


def build_16_risuem_po_koordinatam() -> None:
    output = turtle_output(
        "06-16-triangle-mark", "risuem_po_koordinatam.py",
        caption="Треугольник, построенный по трём заранее продуманным координатам, с заливкой",
        alt="Закрашенный светло-фиолетовый треугольник, построенный по трём явным координатам",
    )
    body = f"""
    <p>До сих пор мы строили фигуры движением («проехать, повернуть») или уже готовыми командами
    (<code class="inline">circle()</code>). Но можно спланировать рисунок сразу в координатах — на
    бумаге или в голове — и просто перечислить точки для <code class="inline">goto()</code>.</p>

    <h2>Сначала — план на координатной плоскости</h2>
    <p>Прежде чем писать код, решим, где будут находиться вершины треугольника:</p>
{comparison_table(
        ["Вершина", "Координата"],
        [
            ["Нижний левый угол", "(-60, -50)"],
            ["Нижний правый угол", "(60, -50)"],
            ["Верхний угол", "(0, 70)"],
        ],
    )}

    <h2>Теперь — код</h2>
{code_block("risuem_po_koordinatam_kod.py", 'artist.fillcolor("#B9A0FC")\nartist.penup()\nartist.goto(-60, -50)\nartist.pendown()\n\nartist.begin_fill()\nartist.goto(60, -50)\nartist.goto(0, 70)\nartist.goto(-60, -50)\nartist.end_fill()\n')}

    <h2>И, наконец, результат</h2>
{output}
{callout(
        "tip",
        "Планирование в координатах — мощный приём",
        "Такой подход особенно удобен, когда фигура сложная и должна получиться <strong>точно"
        "</strong> такой, как задумано — гораздо надёжнее, чем подбирать углы и расстояния на "
        "глаз. В следующем разделе мы соберём несколько фигур в одну композицию именно так — "
        "план сначала, код потом.",
    )}

{local_required_card(
        "06-16",
        "Практика: рисуем по координатам",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-16/index.html",
    )}
    """
    out = render_page(
        page_title="Рисуем по координатам",
        description="Планируем фигуру в координатах заранее, затем переводим план в код goto() — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Рисуем по координатам", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Рисуем по координатам",
        lede="План на бумаге в координатах — и тот же план, переведённый в код goto().",
        body_html=body,
        sidebar_groups=sidebar("06-16-risuem-po-koordinatam.html"),
        nav=PageNav(prev_href="06-15-sluchaynoe-dvizhenie.html", prev_label="Случайное движение", next_href="06-17-otladka-turtle.html", next_label="Отладка Turtle"),
    )
    write("06-16-risuem-po-koordinatam.html", out)


def build_17_otladka() -> None:
    body = f"""
    <p>Графика добавляет несколько новых, специфичных для Turtle способов что-то сделать не так —
    разберём самые частые из них по схеме «симптом → причина → исправление».</p>

{comparison_table(
        ["Симптом", "Причина", "Исправление"],
        [
            [
                "Окно открывается и сразу же закрывается",
                "Программа закончилась, и Python закрыл окно вместе с ней",
                "Добавьте <code class=\"inline\">screen.exitonclick()</code> (ждёт клика) или "
                "<code class=\"inline\">turtle.done()</code> в самом конце программы",
            ],
            [
                "Черепашка «смотрит не туда», хотя код кажется верным",
                "Перепутаны <code class=\"inline\">left()</code>/<code class=\"inline\">right()</code>, "
                "или забыт один из поворотов в последовательности",
                "Перечитайте программу построчно и для каждой команды спросите: "
                "«это движение или поворот?»",
            ],
            [
                "Часть рисунка не появляется на экране",
                "Забыт <code class=\"inline\">pendown()</code> после "
                "<code class=\"inline\">penup()</code> — черепашка честно двигается, просто ничего не рисует",
                "Проверьте, что перед каждым «настоящим» движением перо снова опущено",
            ],
            [
                "Фигура нарисовалась, но заливки нет",
                "Забыт <code class=\"inline\">end_fill()</code>, либо контур не замкнулся в "
                "точности там, где начался",
                "Убедитесь, что путь между <code class=\"inline\">begin_fill()</code> и "
                "<code class=\"inline\">end_fill()</code> возвращается в стартовую точку",
            ],
            [
                "Часть рисунка «пропадает» за краем окна",
                "Координаты вышли за пределы видимой области — окно не бесконечное",
                "Проверьте <code class=\"inline\">screen.setup()</code> и не выходите за половину "
                "ширины/высоты окна от центра",
            ],
            [
                "<code class=\"inline\">TclError</code> или окно вовсе не открывается на сервере/Linux без монитора",
                "Turtle использует Tk — нативный GUI, которому нужен настоящий (или виртуальный) дисплей",
                "Запускайте Turtle на компьютере с обычным рабочим столом; для автоматизации без "
                "монитора нужен виртуальный дисплей вроде Xvfb — это уже не начальный уровень",
            ],
            [
                "Практика Turtle не открывается прямо в браузере на этом сайте",
                "Браузерная среда Python (Pyodide) не умеет открывать нативные Tk-окна — это "
                "техническое ограничение, а не ошибка в вашем коде",
                "Такие практики отмечены «требуется локальный Python» — скачайте .ipynb и "
                "запустите его в VS Code, PyCharm или Jupyter на своём компьютере",
            ],
        ],
    )}

{callout(
        "info",
        "Почему Turtle нельзя запустить прямо в браузере на этом сайте",
        "Обычный Python (CPython) рисует Turtle через Tk — библиотеку нативных окон операционной "
        "системы. Браузерная версия Python, на которой работают интерактивные практики этого "
        "курса, не имеет доступа к нативным окнам вообще — поэтому практики Turtle помечены как "
        "локальные с самого начала главы, а не потому что что-то не работает.",
    )}

    <h2>Предскажите, прежде чем запускать</h2>
    <p>Как и с числами в главе 5, лучшая привычка — предсказать курс и примерные координаты
    черепашки <strong>до</strong> запуска, а не после. Если предсказание разошлось с реальностью —
    вы либо нашли баг, либо неточно понимаете команды. Оба случая стоит разобрать.</p>
{exercise(1, "Предскажите курс", "Черепашка стоит на (0, 0), курс 0°. Выполнены команды: left(90), right(45). Каков итоговый курс? Проверьте себя, выполнив это в реальном окне Turtle.")}
{exercise(2, "Найдите ошибку", "В программе, рисующей квадрат, после третьего поворота получается пятиугольник, а не квадрат. Сколько раз в коде повторяется пара forward()/right(90)? Сколько должно быть?")}

{practice_card(
        "06-17",
        "Практика: отладка Turtle",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-17/index.html",
    )}
    """
    out = render_page(
        page_title="Отладка Turtle",
        description="Частые проблемы Turtle: окно закрывается мгновенно, неверный курс, забытый pendown/end_fill, координаты за пределами окна — симптом, причина, исправление.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Отладка Turtle", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Отладка Turtle",
        lede="Графика добавляет несколько новых способов ошибиться — разберём их по схеме "
        "«симптом → причина → исправление».",
        body_html=body,
        sidebar_groups=sidebar("06-17-otladka-turtle.html"),
        nav=PageNav(prev_href="06-16-risuem-po-koordinatam.html", prev_label="Рисуем по координатам", next_href="06-18-mini-proekty.html", next_label="Мини-проекты"),
    )
    write("06-17-otladka-turtle.html", out)


def build_18_mini_proekty() -> None:
    house = turtle_output(
        "06-18-house", "cvetnoj_dom.py",
        caption="Проект A: Цветной дом — стены, крыша и дверь, три отдельные заливки",
        alt="Домик из фиолетовых стен, красной треугольной крыши и коричневой прямоугольной двери",
    )
    target = turtle_output(
        "06-18-target", "mishen.py",
        caption="Проект B: Мишень — четыре концентрические окружности с чередующейся заливкой",
        alt="Круглая мишень из чередующихся красных и белых концентрических колец",
    )
    stars = turtle_output(
        "06-18-starry-sky", "zvezdnoe_nebo.py",
        caption="Проект C: Звёздное небо — тёмный фон и случайно расположенные точки-звёзды",
        alt="Тёмно-фиолетовое небо с рассыпанными по нему жёлтыми точками-звёздами разного размера",
    )
    star_pattern = turtle_output(
        "06-18-star-pattern", "geometricheskaya_zvezda.py",
        caption="Проект D: Геометрическая звезда — пять отрезков по 150 пикселей, поворот 144° каждый раз",
        alt="Пятиконечная звезда, нарисованная одной непрерывной фиолетовой линией",
    )
    body = f"""
    <p>Четыре небольших, но по-настоящему готовых проекта — каждый использует только то, что мы
    уже прошли в этой главе. Пятый проект, мандала, ждёт в самом конце главы — это финал.</p>

    <h2 id="proekt-a">Проект A: цветной дом</h2>
    <p>Три отдельные фигуры (стены, крыша, дверь), каждая со своей заливкой, собранные в одну
    композицию с помощью <code class="inline">penup()</code>/<code class="inline">goto()</code>
    между ними:</p>
{house}
{exercise(1, "Окно", "Добавьте квадратное окно в стене дома — ещё один маленький begin_fill()/end_fill() блок.")}

    <h2 id="proekt-b">Проект B: мишень</h2>
    <p>Четыре окружности одна внутри другой, с уменьшающимся радиусом и чередующимися цветами:</p>
{target}
{code_block(
        "mishen_kod.py",
        'rings = [(90, "#DC2626"), (65, "#FAFAFC"), (40, "#DC2626"), (15, "#FAFAFC")]\n'
        'for radius, color in rings:\n'
        '    artist.penup()\n'
        '    artist.goto(0, -radius)\n'
        '    artist.pendown()\n'
        '    artist.fillcolor(color)\n'
        '    artist.begin_fill()\n'
        '    artist.circle(radius)\n'
        '    artist.end_fill()\n',
    )}
{callout(
        "info",
        "🚀 Забегаем вперёд",
        "Здесь использован цикл <code class=\"inline\">for</code> по списку пар (радиус, цвет) — "
        "мы разберём списки и циклы подробно позже. Пока достаточно увидеть идею: одна и та же "
        "последовательность действий повторяется для каждой пары значений.",
    )}
{exercise(2, "Свои цвета", "Замените цвета колец на свои — например, оттенки синего и жёлтого.")}

    <h2 id="proekt-c">Проект C: звёздное небо</h2>
    <p>Тёмный фон, много точек случайного размера в случайных местах — тот же приём, что и в
    разделе про случайные точки, но с другим настроением:</p>
{stars}
{exercise(2, "Луна", "Добавьте одну большую белую точку в углу экрана — «луну», нарисованную заранее, до случайных звёзд.")}

    <h2 id="proekt-d">Проект D: геометрическая звезда</h2>
    <p>Пятиконечная звезда рисуется одной линией, без единого отрыва пера — секрет в том, что
    поворот на 144° (а не на 72°) заставляет линию пересекать саму себя:</p>
{star_pattern}
{code_block("geometricheskaya_zvezda_kod.py", "for _ in range(5):\n    artist.forward(150)\n    artist.right(144)\n")}
{callout(
        "tip",
        "Откуда взялось число 144",
        "144° — это <code class=\"inline\">2 × 360 / 5</code>: чтобы звезда «сложилась» "
        "правильно, черепашка должна обойти вокруг центра дважды за пять шагов, а не один раз, "
        "как в обычном пятиугольнике.",
    )}
{exercise(3, "Звезда о семи концах", "Замените 5 на 7 и 144° на подходящий угол (подсказка: тот же принцип — обойти дважды за семь шагов). Что получится?")}

{local_required_card(
        "06-18",
        "Практика: мини-проекты",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-18/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проекты",
        description="Четыре мини-проекта главы 6: цветной дом, мишень, звёздное небо и геометрическая звезда — с реальным выполненным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Мини-проекты", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Мини-проекты",
        lede="Четыре небольших, но по-настоящему готовых проекта — собираем всё, что прошли в "
        "этой главе, в законченные картинки.",
        body_html=body,
        sidebar_groups=sidebar("06-18-mini-proekty.html"),
        nav=PageNav(prev_href="06-17-otladka-turtle.html", prev_label="Отладка Turtle", next_href="06-08-mandala-itogi.html", next_label="Мандала и итоги"),
    )
    write("06-18-mini-proekty.html", out)


def build_08_mandala() -> None:
    motif = turtle_output(
        "06-08-motif", "motiv.py",
        caption="Один мотив: несколько лучей под небольшим углом друг к другу — ещё не полная мандала",
        alt="Веер из нескольких фиолетовых лучей, выходящих из одной точки под небольшим углом друг к другу",
    )
    full = turtle_output(
        "06-08-mandala-full", "mandala.py",
        caption="Тот же приём, доведённый до полного оборота 360° — мандала из прямых линий",
        alt="Симметричная мандала из множества прямых фиолетовых лучей, расходящихся из центра во все стороны",
    )
    final_map = decision_map(
        [
            ("Нужно узнать, где сейчас черепашка?", "position() / xcor() / ycor()"),
            ("Нужно переместиться, не рисуя?", "penup() / pendown()"),
            ("Нужно попасть в конкретную точку?", "goto(x, y)"),
            ("Нужен правильный многоугольник?", "поворот = 360 / n"),
            ("Нужна закрашенная фигура?", "begin_fill() / end_fill()"),
            ("Нужна окружность или дуга?", "circle(радиус, [extent])"),
            ("Нужна повторяемая случайность?", "random.seed()"),
        ],
        title="Какая команда Turtle мне нужна?",
        caption="Главная сводная карта главы 6 — возвращайтесь к ней в будущих проектах",
    )
    body = f"""
    <p>Соберём все приёмы главы в одном финальном узоре: мандале, составленной только из прямых
    линий, — множество лучей одинаковой длины, каждый раз повёрнутых на небольшой угол.</p>

    <h2>Планирование: что вообще происходит</h2>
    <p>Идея простая: встать в одну точку, посмотреть в направлении <code class="inline">ugol</code>,
    проехать вперёд и сразу же вернуться назад по той же линии — а затем немного повернуть курс и
    повторить. Если повторить это достаточно много раз, покрывая все 360° вокруг центра, лучи
    сольются в симметричный узор.</p>

    <h2>Один мотив</h2>
    <p>Сначала — всего несколько лучей, чтобы увидеть сам приём до того, как он превратится в
    насыщенный узор:</p>
{motif}
{code_block(
        "motiv_kod.py",
        'shag_ugla = 10\n'
        'ugol = 0\n'
        'while ugol < 60:\n'
        '    artist.setheading(ugol)\n'
        '    artist.forward(150)\n'
        '    artist.backward(150)\n'
        '    ugol += shag_ugla\n',
    )}
{callout(
        "info",
        "🚀 Забегаем вперёд",
        "Цикл <code class=\"inline\">while</code> подробно разберём позже — здесь достаточно "
        "увидеть, что <code class=\"inline\">setheading()</code> позволяет нарисовать сложный "
        "узор всего в нескольких строках, перебирая углы по кругу.",
    )}

    <h2>Полный оборот — готовая мандала</h2>
    <p>Тот же код, только цикл теперь идёт не до 60°, а до полных 360°:</p>
{full}
{code_block(
        "mandala_kod.py",
        'shag_ugla = 10\n'
        'ugol = 0\n'
        'while ugol < 360:\n'
        '    artist.setheading(ugol)\n'
        '    artist.forward(150)\n'
        '    artist.backward(150)\n'
        '    ugol += shag_ugla\n',
    )}

{exercise(1, "Другой шаг угла", "Измените shag_ugla на 5 или на 30 — как меняется узор?")}
{exercise(2, "Другая длина луча", "Измените длину forward(150) — попробуйте 80 и 250.")}
{exercise(3, "Цветная мандала", "Добавьте artist.pencolor(\"violet\") перед циклом и поэкспериментируйте с другими цветами.")}

{local_required_card(
        "06-08",
        "Практика: мандала из прямых линий",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/06-08/index.html",
    )}

    <h2 id="finalnaya-karta">Финальная карта главы</h2>
{final_map}

    <h2 id="itogi">Итоги</h2>
{summary_box("Что мы узнали в этой главе", [
        "Экран (<code class=\"inline\">turtle.Screen()</code>) и черепашка "
        "(<code class=\"inline\">turtle.Turtle()</code>) — два разных объекта; у черепашки есть "
        "состояние: позиция, курс, перо, цвет.",
        "Окно Turtle использует ту же координатную систему, что и математика: центр (0, 0), "
        "x вправо, y вверх.",
        "<code class=\"inline\">forward()</code>/<code class=\"inline\">backward()</code> "
        "двигают черепашку; <code class=\"inline\">left()</code>/<code class=\"inline\">right()"
        "</code> поворачивают курс относительно текущего направления; "
        "<code class=\"inline\">setheading()</code> задаёт направление абсолютно.",
        "Угол поворота для правильного многоугольника — <code class=\"inline\">360 / n</code>.",
        "<code class=\"inline\">penup()</code>/<code class=\"inline\">pendown()</code> управляют "
        "тем, рисуется ли линия при движении; <code class=\"inline\">goto(x, y)</code> "
        "перемещает черепашку в конкретную точку экрана напрямую.",
        "<code class=\"inline\">begin_fill()</code>/<code class=\"inline\">end_fill()</code> "
        "закрашивают замкнутый контур; <code class=\"inline\">circle()</code> рисует окружности "
        "и дуги; <code class=\"inline\">dot()</code> ставит точку без движения.",
        "random.seed() делает случайную графику воспроизводимой — полезно и для документации, "
        "и для отладки.",
    ])}

    <h2 id="dalshe">Что дальше</h2>
    <p>В главе 7 мы вернёмся к Turtle и настроим её ещё тоньше — научимся точно настраивать экран,
    рисовать текст, освоим дуги подробнее и соберём собственного смайлика. Всё, что вы узнали
    здесь — координаты, углы, перо, заливка, — станет тем фундаментом, на котором строится более
    тонкая настройка.</p>
    """
    out = render_page(
        page_title="Мини-проект — мандала из прямых линий",
        description="Итоговый мини-проект главы 6: мандала из прямых линий с реальным выполненным результатом — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 6", "index.html"), ("Мандала и итоги", "")],
        kicker="Глава 6 · Рисуем классные вещи с помощью Turtle",
        h1="Мини-проект — рисуем мандалу только из прямых линий",
        lede="Собираем все приёмы главы в одном узоре — от первого мотива до полного результата — "
        "и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("06-08-mandala-itogi.html"),
        nav=PageNav(prev_href="06-18-mini-proekty.html", prev_label="Мини-проекты", next_href="../glava-07/index.html", next_label="Глава 7: Глубокое погружение в Turtle"),
    )
    write("06-08-mandala-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01_pristupaem()
    build_09_koordinaty()
    build_02_dvizhenie()
    build_10_napravlenie()
    build_03_povorot()
    build_11_pervye_figury()
    build_04_mini_proekty()
    build_05_sokraschennye()
    build_12_pero()
    build_07_goto()
    build_13_cvet()
    build_14_zalivka()
    build_06_sluchaynye_tochki()
    build_15_sluchaynoe_dvizhenie()
    build_16_risuem_po_koordinatam()
    build_17_otladka()
    build_18_mini_proekty()
    build_08_mandala()
    print("Глава 6 полностью собрана.")
