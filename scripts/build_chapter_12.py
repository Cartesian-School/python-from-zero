#!/usr/bin/env python3
"""Строит Главу 12: «Множество увлекательных мини-проектов» (site/chapters/glava-12/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-12"

PAGES = [
    ("index.html", "Обзор главы"),
    ("12-01-chetnoe-ili-nechetnoe.html", "Проект 12-1: Чётное или нечётное"),
    ("12-02-chaevye.html", "Проект 12-2: Достаточно ли чаевых?"),
    ("12-03-elka.html", "Проект 12-3: Рождественская ёлка"),
    ("12-04-spirali.html", "Проект 12-4: Спирали!"),
    ("12-05-slozhnaya-mandala.html", "Проект 12-5: Сложная мандала"),
    ("12-06-gonka-turtle-itogi.html", "Проект 12-6: Гонка Turtle и итоги"),
]

NOTEBOOKS = [
    "12-01-chetnoe-nechetnoe.ipynb",
    "12-02-chaevye.ipynb",
    "12-03-elka.ipynb",
    "12-04-spirali.ipynb",
    "12-05-slozhnaya-mandala.ipynb",
    "12-06-gonka-turtle.ipynb",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 12 · Мини-проекты", items),
        SidebarGroup("Практика", [NavItem(f"📓 {n}", f"../../../notebooks/chapter-12/{n}") for n in NOTEBOOKS]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=12,
        baseline_page=259,
        title="Множество увлекательных мини-проектов!",
        description="Шесть проектов, закрепляющих всё изученное в главах 1-11: условия, циклы, Turtle и списки.",
        meta_items=["⏱ ~3–4 часа", "🎯 закрепление материала", "📓 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("12.1", "Проект 12-1: Чётное или нечётное", "12-01-chetnoe-ili-nechetnoe.html", "259"),
            ChapterSectionLink("12.2", "Проект 12-2: Достаточно ли чаевых оставляет ваша мама?", "12-02-chaevye.html", "262"),
            ChapterSectionLink("12.3", "Проект 12-3: Рисуем рождественскую ёлку", "12-03-elka.html", "264"),
            ChapterSectionLink("12.4", "Проект 12-4: Спирали!", "12-04-spirali.html", "268"),
            ChapterSectionLink("12.5", "Проект 12-5: Сложная мандала — полностью автоматизированная", "12-05-slozhnaya-mandala.html", "276"),
            ChapterSectionLink("12.6", "Проект 12-6: Гонка Turtle с использованием циклов", "12-06-gonka-turtle-itogi.html", "277"),
            ChapterSectionLink("", "Итоги", "12-06-gonka-turtle-itogi.html#itogi", "281"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>Эта глава — без новой теории: шесть проектов, которые заставляют работать вместе всё,
    что вы изучили в главах 1–11.</p>

    <h2>Часть 1 — Ваше число чётное или нечётное?</h2>
    {code_block(
        "chetnoe_ili_nechetnoe.py",
        'number = int(input("Введите число: "))\n\n'
        "if number % 2 == 0:\n"
        '    print(f"{number} — чётное.")\n'
        "else:\n"
        '    print(f"{number} — нечётное.")\n',
    )}

    <h2>Часть 2 — выводим чётные или нечётные числа из диапазона</h2>
    {code_block(
        "chetnye_iz_diapazona.py",
        'nachalo = int(input("Начало диапазона: "))\n'
        'konec = int(input("Конец диапазона: "))\n\n'
        "chetnye = [n for n in range(nachalo, konec + 1) if n % 2 == 0]\n"
        'print("Чётные числа:", chetnye)\n',
    )}
    {callout(
        "info",
        "Какие темы здесь встретились",
        "<code class=\"inline\">input()</code> и <code class=\"inline\">int()</code> — глава 8; "
        "<code class=\"inline\">%</code> — глава 5; <code class=\"inline\">if/else</code> — "
        "глава 9; генератор списков — глава 11.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "12-01-chetnoe-nechetnoe.ipynb · обе части проекта",
        "../../../notebooks/chapter-12/12-01-chetnoe-nechetnoe.ipynb",
    )}
    """
    out = render_page(
        page_title="Проект 12-1: Чётное или нечётное",
        description="Мини-проект: определяем чётность числа и находим все чётные числа в диапазоне.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), ("Чётное или нечётное", "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1="Проект 12-1: Чётное или нечётное",
        lede="Первый проект главы закрепляет условия и оператор % из ранних глав.",
        body_html=body,
        sidebar_groups=sidebar("12-01-chetnoe-ili-nechetnoe.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="12-02-chaevye.html", next_label="Достаточно ли чаевых?"),
    )
    write("12-01-chetnoe-ili-nechetnoe.html", out)


def build_02() -> None:
    body = f"""
    <p>Стандартные чаевые в ресторане — 15–20% от счёта. Проверим, укладывается ли конкретная
    сумма чаевых в этот диапазон.</p>
    {code_block(
        "chaevye.py",
        'schet = float(input("Сумма счёта: "))\n'
        'chaevye = float(input("Сумма чаевых: "))\n\n'
        "procent = (chaevye / schet) * 100\n\n"
        "if procent < 15:\n"
        '    print(f"Маловато — всего {procent:.1f}%. Обычно оставляют 15-20%.")\n'
        "elif procent <= 20:\n"
        '    print(f"В самый раз — {procent:.1f}%!")\n'
        "else:\n"
        '    print(f"Очень щедро — целых {procent:.1f}%!")\n',
    )}

    {exercise(2, "Своя граница щедрости", "Добавьте четвёртую категорию — «сказочно щедро» — для чаевых больше 30%.")}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "12-02-chaevye.ipynb · вычисляем и оцениваем процент чаевых",
        "../../../notebooks/chapter-12/12-02-chaevye.ipynb",
    )}
    """
    out = render_page(
        page_title="Проект 12-2: Достаточно ли чаевых оставляет ваша мама?",
        description="Мини-проект: считаем процент чаевых от счёта и оцениваем его через elif.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), ("Чаевые", "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1="Проект 12-2: Достаточно ли чаевых оставляет ваша мама?",
        lede="Считаем процент чаевых от суммы счёта и оцениваем щедрость через цепочку elif.",
        body_html=body,
        sidebar_groups=sidebar("12-02-chaevye.html"),
        nav=PageNav(prev_href="12-01-chetnoe-ili-nechetnoe.html", prev_label="Чётное или нечётное", next_href="12-03-elka.html", next_label="Рождественская ёлка"),
    )
    write("12-02-chaevye.html", out)


def build_03() -> None:
    body = f"""
    <p>Нарисуем ёлку из треугольных «ярусов» уменьшающегося размера — используя цикл и фигуры
    из главы 6.</p>
    {code_block(
        "elka.py",
        "artist.hideturtle()\n"
        'artist.pencolor("green")\n'
        'artist.fillcolor("green")\n\n'
        "yarusy = 4\n"
        "shirina = 120\n\n"
        "artist.penup()\n"
        "artist.goto(0, 100)\n"
        "artist.pendown()\n\n"
        "for yarus in range(yarusy):\n"
        "    artist.begin_fill()\n"
        "    artist.setheading(240)\n"
        "    artist.forward(shirina)\n"
        "    artist.setheading(0)\n"
        "    artist.forward(shirina)\n"
        "    artist.setheading(120)\n"
        "    artist.forward(shirina)\n"
        "    artist.end_fill()\n\n"
        "    artist.penup()\n"
        "    artist.setheading(270)\n"
        "    artist.forward(30)\n"
        "    artist.pendown()\n"
        "    shirina -= 20\n\n"
        "# ствол\n"
        'artist.pencolor("brown")\n'
        'artist.fillcolor("brown")\n'
        "artist.setheading(270)\n"
        "artist.penup()\n"
        "artist.forward(10)\n"
        "artist.pendown()\n"
        "artist.begin_fill()\n"
        "for _ in range(2):\n"
        "    artist.forward(40)\n"
        "    artist.right(90)\n"
        "    artist.forward(20)\n"
        "    artist.right(90)\n"
        "artist.end_fill()\n",
    )}
    {callout(
        "tip",
        "Каждый ярус — тот же треугольник, что и в главе 6",
        "Формула угла поворота (<code class=\"inline\">360 / 3 = 120</code>) — та же самая, что "
        "и для любого правильного многоугольника из главы 6. Ёлка — это просто несколько "
        "треугольников уменьшающегося размера, нарисованных друг под другом в цикле.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "12-03-elka.ipynb · рисуем ёлку",
        "../../../notebooks/chapter-12/12-03-elka.ipynb",
    )}
    """
    out = render_page(
        page_title="Проект 12-3: Рисуем рождественскую ёлку",
        description="Мини-проект: рисуем ёлку из уменьшающихся треугольных ярусов с помощью Turtle и цикла.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), ("Ёлка", "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1="Проект 12-3: Рисуем рождественскую ёлку",
        lede="Несколько треугольных ярусов уменьшающегося размера, нарисованных циклом.",
        body_html=body,
        sidebar_groups=sidebar("12-03-elka.html"),
        nav=PageNav(prev_href="12-02-chaevye.html", prev_label="Чаевые", next_href="12-04-spirali.html", next_label="Спирали!"),
    )
    write("12-03-elka.html", out)


def build_04() -> None:
    body = f"""
    <p>Пять вариаций одной идеи — фигура, каждый шаг которой немного больше предыдущего.</p>

    <h2>Квадратная спираль</h2>
    {code_block(
        "kvadratnaya_spiral.py",
        "dlina = 5\n"
        "for _ in range(60):\n"
        "    artist.forward(dlina)\n"
        "    artist.right(90)\n"
        "    dlina += 3\n",
    )}

    <h2>Случайная спираль</h2>
    {code_block(
        "sluchaynaya_spiral.py",
        "import random\n\n"
        "dlina = 5\n"
        "for _ in range(60):\n"
        "    artist.forward(dlina)\n"
        "    artist.right(random.randint(80, 100))  # угол чуть-чуть «дрожит»\n"
        "    dlina += 3\n",
    )}

    <h2>Треугольная спираль</h2>
    {code_block(
        "treugolnaya_spiral.py",
        "dlina = 5\n"
        "for _ in range(60):\n"
        "    artist.forward(dlina)\n"
        "    artist.right(120)\n"
        "    dlina += 3\n",
    )}

    <h2>Звёздная спираль</h2>
    {code_block(
        "zvezdnaya_spiral.py",
        "dlina = 5\n"
        "for _ in range(100):\n"
        "    artist.forward(dlina)\n"
        "    artist.right(144)  # угол пятиконечной звезды\n"
        "    dlina += 2\n",
    )}

    <h2>Круговая спираль</h2>
    {code_block(
        "krugovaya_spiral.py",
        "radius = 5\n"
        "for _ in range(60):\n"
        "    artist.circle(radius, 90)\n"
        "    radius += 3\n",
    )}
    {callout(
        "info",
        "Один общий принцип",
        "Все пять спиралей — одна и та же идея из главы 10 («шаг + поворот + увеличение "
        "переменной») с разным углом поворота. Освоив один вариант, вы фактически освоили все "
        "пять.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "12-04-spirali.ipynb · все пять спиралей",
        "../../../notebooks/chapter-12/12-04-spirali.ipynb",
    )}
    """
    out = render_page(
        page_title="Проект 12-4: Спирали!",
        description="Пять вариаций спирали: квадратная, случайная, треугольная, звёздная и круговая.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), ("Спирали", "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1="Проект 12-4: Спирали!",
        lede="Один и тот же принцип — пять разных узоров, в зависимости от угла поворота.",
        body_html=body,
        sidebar_groups=sidebar("12-04-spirali.html"),
        nav=PageNav(prev_href="12-03-elka.html", prev_label="Ёлка", next_href="12-05-slozhnaya-mandala.html", next_label="Сложная мандала"),
    )
    write("12-04-spirali.html", out)


def build_05() -> None:
    body = f"""
    <p>Финальная эволюция мандалы из глав 6 и 10 — добавим случайный цвет на каждый луч и
    сделаем полностью автоматической, без единого «магического числа», прописанного вручную.</p>
    {code_block(
        "slozhnaya_mandala.py",
        "import random\n\n"
        "luchi = 36\n"
        "shag_ugla = 360 / luchi\n"
        "cveta = [\"red\", \"orange\", \"purple\", \"blue\", \"green\"]\n\n"
        "for i in range(luchi):\n"
        "    artist.pencolor(random.choice(cveta))\n"
        "    artist.setheading(i * shag_ugla)\n"
        "    artist.forward(150)\n"
        "    artist.circle(20)\n"
        "    artist.forward(-150)\n",
    )}
    {callout(
        "tip",
        "luchi определяет всё остальное",
        "Измените только <code class=\"inline\">luchi</code> — угол шага, число повторов "
        "цикла и даже плотность узора пересчитаются автоматически, ничего больше менять не "
        "нужно. Это и называется «полностью автоматизировано».",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "12-05-slozhnaya-mandala.ipynb · мандала со случайными цветами",
        "../../../notebooks/chapter-12/12-05-slozhnaya-mandala.ipynb",
    )}
    """
    out = render_page(
        page_title="Проект 12-5: Сложная мандала — полностью автоматизированная",
        description="Финальная версия мандалы: случайные цвета, круги на концах лучей, полностью управляется одной переменной.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), ("Сложная мандала", "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1="Проект 12-5: Сложная мандала — полностью автоматизированная",
        lede="Финальная версия мандалы из глав 6 и 10 — со случайными цветами и кругами на "
        "концах лучей.",
        body_html=body,
        sidebar_groups=sidebar("12-05-slozhnaya-mandala.html"),
        nav=PageNav(prev_href="12-04-spirali.html", prev_label="Спирали", next_href="12-06-gonka-turtle-itogi.html", next_label="Гонка Turtle и итоги"),
    )
    write("12-05-slozhnaya-mandala.html", out)


def build_06() -> None:
    body = f"""
    <p>Помните из главы 6, что экран и черепашка — разные объекты, и черепашек может быть
    несколько? Настало время это использовать: гонка из нескольких черепашек со случайным
    шагом.</p>
    {code_block(
        "gonka_turtle.py",
        "import random\n\n"
        "screen = turtle.Screen()\n"
        'screen.setup(500, 400)\n\n'
        'cveta = ["red", "blue", "green", "orange"]\n'
        "uchastniki = []\n\n"
        "for i, cvet in enumerate(cveta):\n"
        "    t = turtle.Turtle()\n"
        '    t.shape("turtle")\n'
        "    t.color(cvet)\n"
        "    t.penup()\n"
        "    t.goto(-200, i * 40 - 60)\n"
        "    uchastniki.append(t)\n\n"
        "finish_line = 200\n"
        "pobeditel = None\n\n"
        "while pobeditel is None:\n"
        "    for t in uchastniki:\n"
        "        t.forward(random.randint(1, 10))\n"
        "        if t.xcor() >= finish_line:\n"
        "            pobeditel = t.pencolor()\n"
        "            break\n\n"
        'print(f"Победила черепашка цвета {pobeditel}!")\n',
    )}
    {callout(
        "info",
        "Список черепашек — тот же список из главы 11",
        "<code class=\"inline\">uchastniki</code> — обычный список Python (глава 11), просто "
        "хранящий не числа, а объекты <code class=\"inline\">turtle.Turtle()</code>. Цикл "
        "<code class=\"inline\">for t in uchastniki</code> перебирает его точно так же, как "
        "перебирал бы список чисел или строк.",
    )}

    {exercise(3, "Финишная лента", "Нарисуйте вертикальную линию на финише (x=200) перед началом гонки, используя отдельную черепашку-«судью».")}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы закрепили в этой главе", [
        "Условия (<code class=\"inline\">if/elif/else</code>) и операторы сравнения — на "
        "практике в проектах 12-1 и 12-2.",
        "Циклы (<code class=\"inline\">for</code>, <code class=\"inline\">while</code>) — "
        "основа всех фигур и спиралей в этой главе.",
        "Turtle: заливка, повороты, несколько черепашек на одном экране одновременно.",
        "Списки могут хранить любые объекты, включая другие объекты Python (например, "
        "черепашек), а не только числа и строки.",
        "Сложные визуальные эффекты (мандала, спирали, гонка) — это всегда комбинация "
        "нескольких простых, уже знакомых приёмов.",
    ])}
    """
    out = render_page(
        page_title="Проект 12-6: Гонка Turtle с использованием циклов",
        description="Финальный мини-проект главы 12: гонка нескольких черепашек — и краткие итоги главы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), ("Гонка Turtle", "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1="Проект 12-6: Гонка Turtle с использованием циклов",
        lede="Несколько черепашек на одном экране одновременно — и подведение итогов главы.",
        body_html=body,
        sidebar_groups=sidebar("12-06-gonka-turtle-itogi.html"),
        nav=PageNav(prev_href="12-05-slozhnaya-mandala.html", prev_label="Сложная мандала", next_href="../glava-13/index.html", next_label="Глава 13: Автоматизация с помощью функций"),
    )
    write("12-06-gonka-turtle-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
