#!/usr/bin/env python3
"""Строит Главу 19: «Проект: игра «Змейка» с Turtle» (site/chapters/glava-19/)."""

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
    notebook_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-19"

PAGES = [
    ("index.html", "Обзор главы"),
    ("19-01-igra-import.html", "Игра «Змейка» и импорт модулей"),
    ("19-02-ekran-peremennye.html", "Настраиваем экран и переменные"),
    ("19-03-golova-yabloko.html", "Рисуем голову и яблоко"),
    ("19-04-klavishi-dvizhenie.html", "Клавиши и движение головы"),
    ("19-05-tablo-scheta.html", "Табло счёта"),
    ("19-06-eda-telo.html", "Змейка ест! Движение тела"),
    ("19-07-stolknoveniya.html", "Проверка столкновений"),
    ("19-08-polnyj-kod-itogi.html", "Полный код и итоги"),
]

NOTEBOOKS = [
    "19-02-ekran.ipynb",
    "19-03-golova-yabloko.ipynb",
    "19-04-dvizhenie.ipynb",
    "19-06-eda-telo.ipynb",
    "19-07-stolknoveniya.ipynb",
    "19-08-polnaya-igra.ipynb",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 19 · Змейка", items),
        SidebarGroup("Практика", [NavItem(f"📓 {n}", f"../../../notebooks/chapter-19/{n}") for n in NOTEBOOKS]),
        SidebarGroup("Исходный код", [NavItem("🐍 snake.py", "../../../projects/turtle/snake/snake.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=19,
        baseline_page=413,
        title="Проект: игра «Змейка» с Turtle",
        description="Классическая игра целиком на Turtle — движение, еда, счёт и столкновения.",
        meta_items=["⏱ ~4 часа", "🐍 Turtle + клавиатура", "📓 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("19.1", "Игра «Змейка»", "19-01-igra-import.html", "413"),
            ChapterSectionLink("", "Импортируем необходимые модули", "19-01-igra-import.html#import", "415"),
            ChapterSectionLink("19.2", "Настраиваем экран Turtle", "19-02-ekran-peremennye.html", "415"),
            ChapterSectionLink("", "Создаём и инициализируем переменные", "19-02-ekran-peremennye.html#peremennye", "417"),
            ChapterSectionLink("19.3", "Рисуем голову", "19-03-golova-yabloko.html", "417"),
            ChapterSectionLink("", "Рисуем первое яблоко", "19-03-golova-yabloko.html#yabloko", "419"),
            ChapterSectionLink("19.4", "Регистрирует ли экран нажатия клавиш?", "19-04-klavishi-dvizhenie.html", "421"),
            ChapterSectionLink("", "Заставляем голову двигаться", "19-04-klavishi-dvizhenie.html#dvizhenie", "423"),
            ChapterSectionLink("19.5", "Запускаем табло счёта", "19-05-tablo-scheta.html", "426"),
            ChapterSectionLink("19.6", "Наша змейка ест!", "19-06-eda-telo.html", "428"),
            ChapterSectionLink("", "Заставляем двигаться всю змейку", "19-06-eda-telo.html#telo", "431"),
            ChapterSectionLink("19.7", "Проверка столкновений", "19-07-stolknoveniya.html", "434"),
            ChapterSectionLink("19.8", "Полный код", "19-08-polnyj-kod-itogi.html", "439"),
            ChapterSectionLink("", "Итоги", "19-08-polnyj-kod-itogi.html#itogi", "444"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Игра «Змейка»</h2>
    <p>«Змейка» — одна из самых узнаваемых игр в истории программирования. Змейка непрерывно
    движется по полю, съедает появляющиеся яблоки и растёт с каждым съеденным яблоком; игра
    заканчивается при столкновении со стеной или с собственным хвостом. Соберём её на уже
    знакомом модуле <code class="inline">turtle</code> (главы 6–7, 12) — только на этот раз
    черепашка станет не художником, а персонажем игры.</p>

    <h2 id="import">Импортируем необходимые модули</h2>
    {code_block(
        "importy.py",
        "import random\n"
        "import turtle\n",
    )}
    <p><code class="inline">random</code> понадобится для случайного положения яблока (глава 5),
    <code class="inline">turtle</code> — для самой графики.</p>

    {notebook_card(
        "Практика в Jupyter Notebook",
        "19-02-ekran.ipynb · начинаем собирать игру",
        "../../../notebooks/chapter-19/19-02-ekran.ipynb",
    )}
    """
    out = render_page(
        page_title="Игра «Змейка» и импорт модулей",
        description="Введение в проект «Змейка» на Turtle и необходимые модули random и turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Игра и импорт", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Игра «Змейка»",
        lede="Классическая игра — движение, еда и столкновения — на уже знакомом модуле "
        "turtle.",
        body_html=body,
        sidebar_groups=sidebar("19-01-igra-import.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="19-02-ekran-peremennye.html", next_label="Экран и переменные"),
    )
    write("19-01-igra-import.html", out)


def build_02() -> None:
    body = f"""
    <h2>Настраиваем экран Turtle</h2>
    <p>Игре нужен предсказуемый, контролируемый экран — и, что важно, отключённое
    автообновление: обновлять картинку мы будем вручную, ровно раз за игровой шаг, а не при
    каждом мелком движении:</p>
    {code_block(
        "nastrojka_ekrana.py",
        "screen = turtle.Screen()\n"
        'screen.title("Змейка")\n'
        'screen.bgcolor("black")\n'
        "screen.setup(width=600, height=600)\n"
        "screen.tracer(0)   # отключаем автообновление\n",
    )}
    {callout(
        "info",
        "Зачем tracer(0)?",
        "Без <code class=\"inline\">tracer(0)</code> Turtle перерисовывает экран после "
        "<em>каждого</em> отдельного движения — для игры, где нужно двигать голову и "
        "несколько сегментов тела на каждом шаге, это выглядело бы мерцающим и медленным. "
        "<code class=\"inline\">tracer(0)</code> + ручной <code class=\"inline\">screen.update()"
        "</code> в конце каждого шага дают куда более плавную анимацию.",
    )}

    <h2 id="peremennye">Создаём и инициализируем необходимые переменные</h2>
    {code_block(
        "peremennye.py",
        "RAZMER_SHAGA = 20\n"
        "GRANICA = 280\n\n"
        'napravlenie = "stop"\n'
        "schet = 0\n"
        "igra_okonchena = False\n"
        "segmenty = []   # тело змейки\n",
    )}
    {callout(
        "tip",
        "ЗАГЛАВНЫЕ_БУКВЫ — соглашение для констант",
        "<code class=\"inline\">RAZMER_SHAGA</code> и <code class=\"inline\">GRANICA</code> не "
        "меняются в процессе игры — по соглашению такие «постоянные» переменные принято "
        "называть заглавными буквами. Само по себе это ничего не меняет технически, но "
        "сигнализирует читателю: «это значение не должно меняться».",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "19-02-ekran.ipynb · настройка экрана и переменных",
        "../../../notebooks/chapter-19/19-02-ekran.ipynb",
    )}
    """
    out = render_page(
        page_title="Настраиваем экран Turtle и переменные",
        description="tracer(0) для ручного управления обновлением экрана и переменные состояния игры «Змейка».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Экран и переменные", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Настраиваем экран Turtle",
        lede="Отключаем автообновление экрана и заводим переменные, которые будут помнить "
        "состояние игры.",
        body_html=body,
        sidebar_groups=sidebar("19-02-ekran-peremennye.html"),
        nav=PageNav(prev_href="19-01-igra-import.html", prev_label="Игра и импорт", next_href="19-03-golova-yabloko.html", next_label="Голова и яблоко"),
    )
    write("19-02-ekran-peremennye.html", out)


def build_03() -> None:
    body = f"""
    <h2>Рисуем голову</h2>
    <p>Голова змейки — обычный объект <code class="inline">turtle.Turtle()</code>, знакомый
    ещё с главы 6, только с квадратной формой и без рисования линий (перо поднято):</p>
    {code_block(
        "golova.py",
        "golova = turtle.Turtle()\n"
        "golova.speed(0)\n"
        'golova.shape("square")\n'
        'golova.color("white")\n'
        "golova.penup()\n"
        "golova.goto(0, 0)\n",
    )}

    <h2 id="yabloko">Рисуем первое яблоко</h2>
    <p>Яблоко — тоже черепашка, только круглая и красная, и появляется в случайном месте поля,
    выровненном по сетке шага (<code class="inline">random.randrange()</code> с шагом
    <code class="inline">RAZMER_SHAGA</code>, чтобы яблоко всегда оказывалось «в клетке»):</p>
    {code_block(
        "yabloko.py",
        "yabloko = turtle.Turtle()\n"
        "yabloko.speed(0)\n"
        'yabloko.shape("circle")\n'
        'yabloko.color("red")\n'
        "yabloko.penup()\n\n"
        "def novoe_yabloko():\n"
        "    x = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)\n"
        "    y = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)\n"
        "    yabloko.goto(x, y)\n\n"
        "novoe_yabloko()\n",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "19-03-golova-yabloko.ipynb · создаём голову и яблоко",
        "../../../notebooks/chapter-19/19-03-golova-yabloko.ipynb",
    )}
    """
    out = render_page(
        page_title="Рисуем голову и яблоко",
        description="Создаём голову змейки и яблоко как объекты turtle.Turtle() со случайным положением.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Голова и яблоко", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Рисуем голову",
        lede="Голова и яблоко — обычные объекты Turtle с разной формой и цветом.",
        body_html=body,
        sidebar_groups=sidebar("19-03-golova-yabloko.html"),
        nav=PageNav(prev_href="19-02-ekran-peremennye.html", prev_label="Экран и переменные", next_href="19-04-klavishi-dvizhenie.html", next_label="Клавиши и движение"),
    )
    write("19-03-golova-yabloko.html", out)


def build_04() -> None:
    body = f"""
    <h2>Регистрирует ли экран нажатия клавиш со стрелками?</h2>
    <p>Чтобы Turtle реагировал на клавиатуру, ему нужно явно разрешить «слушать» события
    (<code class="inline">screen.listen()</code>) и связать конкретные клавиши с функциями через
    <code class="inline">onkeypress()</code> — идея та же, что и <code class="inline">.bind()</code>
    у Tkinter в главе 17, только с более простым, специализированным интерфейсом:</p>
    {code_block(
        "klavishi.py",
        "def idti_vverh():\n"
        "    global napravlenie\n"
        '    if napravlenie != "down":   # нельзя развернуться на 180° мгновенно\n'
        '        napravlenie = "up"\n\n'
        "def idti_vniz():\n"
        "    global napravlenie\n"
        '    if napravlenie != "up":\n'
        '        napravlenie = "down"\n\n'
        "# idti_vlevo() и idti_vpravo() устроены аналогично\n\n"
        "screen.listen()\n"
        'screen.onkeypress(idti_vverh, "Up")\n'
        'screen.onkeypress(idti_vniz, "Down")\n'
        'screen.onkeypress(idti_vlevo, "Left")\n'
        'screen.onkeypress(idti_vpravo, "Right")\n',
    )}
    {callout(
        "warning",
        "Почему нельзя просто развернуться на 180°?",
        "Если змейка двигалась вправо, а игрок нажмёт «влево», голова мгновенно «наедет» на "
        "первый сегмент собственного тела — это выглядело бы как мгновенный проигрыш без "
        "видимой причины. Проверка <code class=\"inline\">if napravlenie != \"down\":</code> "
        "запрещает разворот на месте, разрешая только повороты на 90°.",
    )}

    <h2 id="dvizhenie">Заставляем голову змейки двигаться</h2>
    {code_block(
        "dvizhenie_golovy.py",
        "def dvigat_golovu():\n"
        '    if napravlenie == "up":\n'
        "        golova.sety(golova.ycor() + RAZMER_SHAGA)\n"
        '    elif napravlenie == "down":\n'
        "        golova.sety(golova.ycor() - RAZMER_SHAGA)\n"
        '    elif napravlenie == "left":\n'
        "        golova.setx(golova.xcor() - RAZMER_SHAGA)\n"
        '    elif napravlenie == "right":\n'
        "        golova.setx(golova.xcor() + RAZMER_SHAGA)\n",
    )}
    {callout(
        "tip",
        "sety()/setx() — половина от goto()",
        "<code class=\"inline\">sety(y)</code> меняет только координату Y, оставляя X "
        "прежним — удобнее, чем вычислять обе координаты через "
        "<code class=\"inline\">goto()</code> каждый раз.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "19-04-dvizhenie.ipynb · клавиши и движение головы",
        "../../../notebooks/chapter-19/19-04-dvizhenie.ipynb",
    )}
    """
    out = render_page(
        page_title="Клавиши и движение головы",
        description="onkeypress() для управления с клавиатуры и движение головы змейки по сетке.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Клавиши и движение", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Регистрирует ли экран нажатия клавиш со стрелками?",
        lede="Подключаем клавиатуру и заставляем голову двигаться — с защитой от мгновенного "
        "разворота на 180°.",
        body_html=body,
        sidebar_groups=sidebar("19-04-klavishi-dvizhenie.html"),
        nav=PageNav(prev_href="19-03-golova-yabloko.html", prev_label="Голова и яблоко", next_href="19-05-tablo-scheta.html", next_label="Табло счёта"),
    )
    write("19-04-klavishi-dvizhenie.html", out)


def build_05() -> None:
    body = f"""
    <p>Счёт удобно показывать отдельной черепашкой без формы (<code class="inline">hideturtle()</code>),
    которая ничего не рисует, кроме текста (<code class="inline">write()</code> из главы 7):</p>
    {code_block(
        "tablo_scheta.py",
        "tablo = turtle.Turtle()\n"
        "tablo.speed(0)\n"
        'tablo.color("white")\n'
        "tablo.penup()\n"
        "tablo.hideturtle()\n"
        "tablo.goto(0, 260)\n\n"
        "def obnovit_tablo():\n"
        "    tablo.clear()   # стираем старую надпись перед новой\n"
        '    tablo.write(f"Счёт: {schet}", align="center", font=("Arial", 16, "normal"))\n\n'
        "obnovit_tablo()\n",
    )}
    {callout(
        "warning",
        "clear() перед write() — обязательно",
        "Без <code class=\"inline\">tablo.clear()</code> каждый новый счёт накладывался бы "
        "поверх предыдущего — цифры быстро превратились бы в нечитаемую кашу.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "19-06-eda-telo.ipynb · включает обновление табло при поедании яблока",
        "../../../notebooks/chapter-19/19-06-eda-telo.ipynb",
    )}
    """
    out = render_page(
        page_title="Запускаем табло счёта",
        description="Отдельная черепашка для отображения текущего счёта игры «Змейка».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Табло счёта", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Запускаем табло счёта",
        lede="Отдельная черепашка без формы, которая только показывает текст текущего счёта.",
        body_html=body,
        sidebar_groups=sidebar("19-05-tablo-scheta.html"),
        nav=PageNav(prev_href="19-04-klavishi-dvizhenie.html", prev_label="Клавиши и движение", next_href="19-06-eda-telo.html", next_label="Змейка ест! Тело"),
    )
    write("19-05-tablo-scheta.html", out)


def build_06() -> None:
    body = f"""
    <h2>Наша змейка ест!</h2>
    <p>Проверяем, достаточно ли близко голова оказалась к яблоку (метод
    <code class="inline">.distance()</code> считает расстояние между двумя черепашками) — если
    да, яблоко «съедено»: появляется новое яблоко, змейка растёт, счёт увеличивается:</p>
    {code_block(
        "eda.py",
        "def proverit_edu():\n"
        "    global schet\n"
        "    if golova.distance(yabloko) < RAZMER_SHAGA:\n"
        "        novoe_yabloko()\n"
        "        dobavit_segment()\n"
        "        schet += 10\n"
        "        obnovit_tablo()\n",
    )}

    <h2 id="telo">Заставляем двигаться всю змейку</h2>
    <p>Каждый сегмент тела должен занять место <em>предыдущего</em> сегмента (а первый — место
    головы) — это создаёт эффект «змейка ползёт целиком», а не «части двигаются независимо»:</p>
    {code_block(
        "dobavit_segment.py",
        "def dobavit_segment():\n"
        "    novyj = turtle.Turtle()\n"
        "    novyj.speed(0)\n"
        '    novyj.shape("square")\n'
        '    novyj.color("grey")\n'
        "    novyj.penup()\n"
        "    segmenty.append(novyj)\n",
    )}
    {code_block(
        "dvigat_telo.py",
        "def dvigat_telo():\n"
        "    # начинаем с хвоста и идём к голове, чтобы не потерять позиции по пути\n"
        "    for indeks in range(len(segmenty) - 1, 0, -1):\n"
        "        x = segmenty[indeks - 1].xcor()\n"
        "        y = segmenty[indeks - 1].ycor()\n"
        "        segmenty[indeks].goto(x, y)\n\n"
        "    if segmenty:\n"
        "        segmenty[0].goto(golova.xcor(), golova.ycor())\n",
    )}
    {callout(
        "warning",
        "Порядок вызовов решает всё",
        "<code class=\"inline\">dvigat_telo()</code> обязательно вызывается <strong>до</strong> "
        "<code class=\"inline\">dvigat_golovu()</code> — иначе первый сегмент «унаследует» уже "
        "<em>новую</em> позицию головы вместо старой, и тело слипнется с головой в одну точку.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "19-06-eda-telo.ipynb · поедание яблок и движение тела",
        "../../../notebooks/chapter-19/19-06-eda-telo.ipynb",
    )}
    """
    out = render_page(
        page_title="Змейка ест! Движение тела",
        description="Проверка поедания яблока через distance() и движение всех сегментов тела змейки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Еда и тело", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Наша змейка ест!",
        lede="Съеденное яблоко добавляет сегмент — и каждый сегмент должен правильно следовать "
        "за предыдущим.",
        body_html=body,
        sidebar_groups=sidebar("19-06-eda-telo.html"),
        nav=PageNav(prev_href="19-05-tablo-scheta.html", prev_label="Табло счёта", next_href="19-07-stolknoveniya.html", next_label="Проверка столкновений"),
    )
    write("19-06-eda-telo.html", out)


def build_07() -> None:
    body = f"""
    <p>Игра заканчивается при одном из двух столкновений: со стеной поля или с собственным
    телом.</p>
    {code_block(
        "stolknoveniya.py",
        "def proverit_stolknoveniya():\n"
        "    global igra_okonchena\n\n"
        "    # столкновение со стеной\n"
        "    if abs(golova.xcor()) > GRANICA or abs(golova.ycor()) > GRANICA:\n"
        "        igra_okonchena = True\n\n"
        "    # столкновение с собственным телом\n"
        "    for segment in segmenty:\n"
        "        if segment.distance(golova) < RAZMER_SHAGA / 2:\n"
        "            igra_okonchena = True\n",
    )}
    {callout(
        "info",
        "abs() снова экономит код",
        "<code class=\"inline\">abs(golova.xcor()) > GRANICA</code> проверяет сразу обе "
        "стены (левую и правую) одним сравнением — вместо "
        "<code class=\"inline\">golova.xcor() &gt; GRANICA or golova.xcor() &lt; -GRANICA</code>. "
        "Тот же приём мы использовали для факториала и других вычислений в главе 5.",
    )}

    {exercise(2, "Ускорение игры", "Увеличивайте скорость движения (уменьшайте задержку между шагами) на каждые 50 очков — игра станет постепенно сложнее.")}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "19-07-stolknoveniya.ipynb · столкновение со стеной и с собой",
        "../../../notebooks/chapter-19/19-07-stolknoveniya.ipynb",
    )}
    """
    out = render_page(
        page_title="Проверка столкновений",
        description="Определяем конец игры: столкновение со стеной поля или с собственным телом змейки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Столкновения", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Проверка столкновений",
        lede="Игра заканчивается при столкновении со стеной или с собственным хвостом.",
        body_html=body,
        sidebar_groups=sidebar("19-07-stolknoveniya.html"),
        nav=PageNav(prev_href="19-06-eda-telo.html", prev_label="Еда и тело", next_href="19-08-polnyj-kod-itogi.html", next_label="Полный код и итоги"),
    )
    write("19-07-stolknoveniya.html", out)


def build_08() -> None:
    body = f"""
    <p>Соберём один игровой шаг из всех частей главы — эта функция и есть сердце игры,
    вызываемое снова и снова, пока игра не закончится:</p>
    {code_block(
        "igrovoj_shag.py",
        "def igrovoj_shag():\n"
        "    if igra_okonchena:\n"
        "        return False\n\n"
        "    dvigat_telo()\n"
        "    dvigat_golovu()\n"
        "    proverit_edu()\n"
        "    proverit_stolknoveniya()\n"
        "    screen.update()\n"
        "    return not igra_okonchena\n\n"
        "def glavnyj_cikl():\n"
        '    global napravlenie\n'
        '    napravlenie = "right"\n'
        "    while igrovoj_shag():\n"
        "        screen.update()\n"
        '    tablo.goto(0, 0)\n'
        '    tablo.write(f"Игра окончена! Счёт: {schet}", align="center", font=("Arial", 20, "bold"))\n',
    )}
    <p>Полная, уже собранная и проверенная программа доступна отдельным файлом:</p>
    <p>📄 <a href="../../../projects/turtle/snake/snake.py">projects/turtle/snake/snake.py</a></p>
    {callout(
        "tip",
        "Запустите игру у себя",
        "<code class=\"inline\">python snake.py</code> в терминале — управление стрелками "
        "клавиатуры.",
    )}

    {exercise(3, "Уровни сложности", "Добавьте выбор уровня сложности перед стартом игры (input() из главы 8) — влияющий на начальную скорость через задержку между шагами.")}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "<code class=\"inline\">screen.tracer(0)</code> + ручной "
        "<code class=\"inline\">screen.update()</code> — стандартный приём для плавной "
        "анимации в играх на Turtle.",
        "<code class=\"inline\">screen.onkeypress()</code> связывает клавиши со стрелками с "
        "функциями изменения направления; запрет разворота на 180° предотвращает мгновенное "
        "самостолкновение.",
        "Тело змейки — список отдельных сегментов, каждый из которых следует за предыдущим; "
        "порядок обновления (сначала тело, потом голова) критически важен.",
        "<code class=\"inline\">.distance()</code> между двумя черепашками — удобный способ "
        "проверить, находятся ли они «достаточно близко» (для еды и столкновений).",
        "Игровой цикл — функция, вызываемая снова и снова, пока не наступит условие конца "
        "игры.",
    ])}
    """
    out = render_page(
        page_title="Полный код и итоги",
        description="Собираем игровой шаг воедино, ссылка на полный исходный код и итоги главы 19.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Полный код и итоги", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Полный код",
        lede="Собираем все части в единый игровой цикл — и подводим итоги главы.",
        body_html=body,
        sidebar_groups=sidebar("19-08-polnyj-kod-itogi.html"),
        nav=PageNav(prev_href="19-07-stolknoveniya.html", prev_label="Столкновения", next_href="../glava-20/index.html", next_label="Глава 20: Станьте разработчиком игр с Pygame"),
    )
    write("19-08-polnyj-kod-itogi.html", out)


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
