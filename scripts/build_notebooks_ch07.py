#!/usr/bin/env python3
"""Строит 16 новых ноутбуков практики для Главы 7.

13 локальных (local-required, реальное окно turtle — следуют паттерну
существующих ноутбуков главы: общие screen/artist создаются один раз,
каждая следующая ячейка вызывает artist.reset() перед своим кодом, в конце
— screen.bye()):
    07-10, 07-11, 07-12, 07-13, 07-14, 07-15, 07-16, 07-17, 07-18, 07-19,
    07-20, 07-21, 07-22

3 браузерных (browser-pyodide + automatic, чистые вычисления/предсказания
без import turtle — Pyodide не умеет открывать нативные окна):
    07-23 (отладка), 07-24 (формула шагов), 07-25 (clear/reset/home)

Существующие 07-01/03/04/06/07/09 НЕ трогаем.

ВАЖНО: ни у одного нового ноутбука первая КОДОВАЯ ячейка не помечена
raises=True.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-07"
CH7_URL = "../../site/chapters/glava-07"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = 'import turtle\n\nscreen = turtle.Screen()\nartist = turtle.Turtle()\nartist.pensize(3)\nartist.pencolor("#5B24F9")\nprint("Окно Turtle готово.")'
CLOSE_MD = "## Завершение (выполнить один раз, в самом конце)"
CLOSE_CODE = 'screen.bye()\nprint("Окно Turtle закрыто.")'


def build_10_colormode() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-10 · colormode и цвет\n\nПрактика к разделу [«colormode и цвет»]({CH7_URL}/07-10-colormode-i-cvet.html).")
    nb.md("## Цель\n\nОсвоить colormode(1.0) и colormode(255), задавать цвета через RGB.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nRGB в режиме 255.")
    nb.code('artist.reset()\nscreen.colormode(255)\nartist.pencolor(255, 0, 0)\nartist.forward(100)')
    nb.md("## Задание ★ Базовая практика\n\nВ режиме colormode(255) нарисуйте линию длиной 120 цветом (0, 150, 0) — зелёным.")
    nb.code('artist.reset()\nscreen.colormode(255)\nartist.pencolor(0, 150, 0)\nartist.forward(120)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-10-colormode-i-cvet.ipynb")
    print(f"Записано: 07-10-colormode-i-cvet.ipynb ({len(nb)} ячеек)")


def build_11_pero_zalivka() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-11 · Перо и заливка\n\nПрактика к разделу [«Перо и заливка — не одно и то же»]({CH7_URL}/07-11-pero-i-zalivka.html).")
    nb.md("## Цель\n\nРазличать pencolor(), fillcolor() и color().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\ncolor() задаёт оба цвета разом.")
    nb.code('artist.reset()\nartist.color("blue", "gold")\nartist.begin_fill()\nfor _ in range(4):\n    artist.forward(100)\n    artist.right(90)\nartist.end_fill()')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте треугольник с синим контуром (pencolor) и зелёной заливкой (fillcolor), заданными раздельно.")
    nb.code('artist.reset()\nartist.pencolor("blue")\nartist.fillcolor("green")\nartist.begin_fill()\nfor _ in range(3):\n    artist.forward(100)\n    artist.right(120)\nartist.end_fill()')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-11-pero-i-zalivka.ipynb")
    print(f"Записано: 07-11-pero-i-zalivka.ipynb ({len(nb)} ячеек)")


def build_12_speed_tracer() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-12 · speed, tracer и update\n\nПрактика к разделу [«speed, tracer и update»]({CH7_URL}/07-12-speed-tracer-update.html).")
    nb.md("## Цель\n\nОсвоить пакетное рисование через tracer(0) + update().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\n20 окружностей, нарисованных мгновенно.")
    nb.code('artist.reset()\nscreen.tracer(0)\nfor i in range(20):\n    artist.circle(60)\n    artist.right(18)\nscreen.update()')
    nb.md("## Задание ★ Базовая практика\n\nИспользуя tracer(0) и update(), нарисуйте 24 окружности радиусом 50, каждая повёрнута на 15°.")
    nb.code('artist.reset()\nscreen.tracer(0)\nfor i in range(24):\n    artist.circle(50)\n    artist.right(15)\nscreen.update()')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-12-speed-tracer-update.ipynb")
    print(f"Записано: 07-12-speed-tracer-update.ipynb ({len(nb)} ячеек)")


def build_13_geometriya() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-13 · Геометрия окружности\n\nПрактика к разделу [«Геометрия окружности»]({CH7_URL}/07-13-geometriya-okruzhnosti.html).")
    nb.md("## Цель\n\nПонять направление рисования circle() и роль знака радиуса.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nПоложительный и отрицательный радиус рядом.")
    nb.code('artist.reset()\nartist.circle(70)\nartist.penup(); artist.forward(180); artist.pendown()\nartist.circle(-70)')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте окружность радиусом 90 по часовой стрелке (используйте отрицательный радиус).")
    nb.code('artist.reset()\nartist.circle(-90)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-13-geometriya-okruzhnosti.ipynb")
    print(f"Записано: 07-13-geometriya-okruzhnosti.ipynb ({len(nb)} ячеек)")


def build_14_circle_steps() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-14 · circle(steps=...)\n\nПрактика к разделу [«circle(steps=...) — от круга к многоугольнику»]({CH7_URL}/07-14-circle-steps.html).")
    nb.md("## Цель\n\nПревращать окружность в многоугольник через steps.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nПятиугольник через circle(steps=5).")
    nb.code('artist.reset()\nartist.circle(80, steps=5)')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте восьмиугольник радиусом 70, используя circle() с steps.")
    nb.code('artist.reset()\nartist.circle(70, steps=8)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-14-circle-steps.ipynb")
    print(f"Записано: 07-14-circle-steps.ipynb ({len(nb)} ячеек)")


def build_15_vyravnivanie() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-15 · Выравнивание и шрифт\n\nПрактика к разделу [«Выравнивание и шрифт»]({CH7_URL}/07-15-vyravnivanie-i-shrift.html).")
    nb.md("## Цель\n\nОсвоить align и font в write().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nТри выравнивания у одной точки.")
    nb.code('artist.reset()\nartist.hideturtle()\nartist.penup()\nartist.dot(6)\nartist.write("center", align="center", font=("Arial", 14, "normal"))')
    nb.md("## Задание ★ Базовая практика\n\nВыведите текст \"Cartesian\" крупным (24) жирным шрифтом Arial, выровненным по правому краю (align=\"right\").")
    nb.code('artist.reset()\nartist.hideturtle()\nartist.penup()\nartist.write("Cartesian", align="right", font=("Arial", 24, "bold"))')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-15-vyravnivanie-i-shrift.ipynb")
    print(f"Записано: 07-15-vyravnivanie-i-shrift.ipynb ({len(nb)} ячеек)")


def build_16_tekst_koordinaty() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-16 · Текст и координатная система\n\nПрактика к разделу [«Текст и координатная система»]({CH7_URL}/07-16-tekst-i-koordinaty.html).")
    nb.md("## Цель\n\nСобрать goto(), dot() и write() в подписанный график.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nОдна подписанная точка на оси.")
    nb.code('artist.reset()\nartist.hideturtle()\nartist.penup()\nartist.goto(50, 0)\nartist.dot(6, "#5B24F9")\nartist.goto(50, -20)\nartist.write("50", align="center", font=("Arial", 11, "normal"))')
    nb.md("## Задание ★ Базовая практика\n\nПоставьте три подписанные точки на оси X: -50, 0 и 50 — с числовыми подписями под каждой.")
    nb.code('artist.reset()\nartist.hideturtle()\nartist.penup()\nfor value in [-50, 0, 50]:\n    artist.goto(value, 0)\n    artist.dot(6, "#5B24F9")\n    artist.goto(value, -20)\n    artist.write(str(value), align="center", font=("Arial", 11, "normal"))')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-16-tekst-i-koordinaty.ipynb")
    print(f"Записано: 07-16-tekst-i-koordinaty.ipynb ({len(nb)} ячеек)")


def build_17_forma() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-17 · Черепашка как графический объект\n\nПрактика к разделу [«Черепашка как графический объект»]({CH7_URL}/07-17-forma-cherepashki.html).")
    nb.md("## Цель\n\nОсвоить shape(), shapesize() и tilt().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nУвеличенная форма-черепашка.")
    nb.code('artist.reset()\nartist.shape("turtle")\nartist.shapesize(2, 2)\nartist.stamp()')
    nb.md("## Задание ★ Базовая практика\n\nПоставьте штамп формы \"square\" с shapesize(1.5, 3) — растянутый прямоугольник.")
    nb.code('artist.reset()\nartist.shape("square")\nartist.shapesize(1.5, 3)\nartist.stamp()')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-17-forma-cherepashki.ipynb")
    print(f"Записано: 07-17-forma-cherepashki.ipynb ({len(nb)} ячеек)")


def build_18_neskolko() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-18 · Несколько черепашек\n\nПрактика к разделу [«Несколько черепашек»]({CH7_URL}/07-18-neskolko-cherepashek.html).")
    nb.md("## Цель\n\nСоздать несколько независимых объектов Turtle.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nДве черепашки, разные цвета.")
    nb.code('artist.reset()\nfriend = turtle.Turtle()\nfriend.color("#DB2777")\nfriend.penup(); friend.goto(0, -80); friend.pendown()\nartist.forward(100)\nfriend.forward(100)')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте третью черепашку с именем `third`, зелёного цвета, и переместите её на forward(80).")
    nb.code('third = turtle.Turtle()\nthird.color("green")\nthird.penup(); third.goto(0, 80); third.pendown()\nthird.forward(80)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-18-neskolko-cherepashek.ipynb")
    print(f"Записано: 07-18-neskolko-cherepashek.ipynb ({len(nb)} ячеек)")


def build_19_clone() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-19 · clone()\n\nПрактика к разделу [«clone() — копируем состояние»]({CH7_URL}/07-19-clone.html).")
    nb.md("## Цель\n\nСоздать клон черепашки и заставить его разойтись с оригиналом.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nКлон, повёрнутый в другую сторону.")
    nb.code('artist.reset()\nartist.penup(); artist.goto(0, -100); artist.pendown()\nartist.setheading(90)\ncopy = artist.clone()\ncopy.color("#DB2777")\nartist.left(20); artist.forward(150)\ncopy.right(20); copy.forward(150)')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте клон и разверните его на right(90) относительно оригинала, затем проведите обе черепашки вперёд на 100.")
    nb.code('artist.reset()\ncopy = artist.clone()\ncopy.color("#059669")\ncopy.right(90)\nartist.forward(100)\ncopy.forward(100)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-19-clone.ipynb")
    print(f"Записано: 07-19-clone.ipynb ({len(nb)} ячеек)")


def build_20_clear_reset_home() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-20 · clear(), reset(), home()\n\nПрактика к разделу [«clear(), reset() и home()»]({CH7_URL}/07-20-clear-reset-home.html).")
    nb.md("## Цель\n\nРазличать эффект clear(), reset() и home() на практике.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nreset() стирает рисунок и возвращает домой.")
    nb.code('artist.forward(100)\nartist.left(90)\nartist.forward(60)\nprint(artist.position())\nartist.reset()\nprint(artist.position())')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте квадрат, переместитесь (penup) в точку (80, 80), затем вызовите home() и выведите position() — рисунок должен остаться на месте.")
    nb.code('artist.reset()\nfor _ in range(4):\n    artist.forward(60)\n    artist.right(90)\nartist.penup()\nartist.goto(80, 80)\nartist.home()\nprint(artist.position())')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-20-clear-reset-home.ipynb")
    print(f"Записано: 07-20-clear-reset-home.ipynb ({len(nb)} ячеек)")


def build_21_chasy() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-21 · Часы без времени\n\nПрактика к разделу [«Мини-проект: часы без времени»]({CH7_URL}/07-21-mini-proekt-chasy.html).")
    nb.md("## Цель\n\nПостроить статичный циферблат из делений и стрелок.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nОкружность и 12 делений.")
    nb.code('artist.reset()\nartist.circle(120)\nfor hour in range(12):\n    artist.penup()\n    artist.goto(0, 0)\n    artist.setheading(90 - hour * 30)\n    artist.forward(105)\n    artist.pendown()\n    artist.forward(15)\n    artist.penup()')
    nb.md("## Задание ★★ Самостоятельная практика\n\nДобавьте часовую стрелку (толстая, короткая) на 9 часов и минутную (тоньше, длиннее) на 12 часов.")
    nb.code('artist.pensize(5)\nartist.pencolor("#5B24F9")\nartist.goto(0, 0)\nartist.setheading(90 - 9 * 30)\nartist.pendown()\nartist.forward(70)\nartist.penup()\n\nartist.pensize(3)\nartist.pencolor("#DB2777")\nartist.goto(0, 0)\nartist.setheading(90 - 12 * 30)\nartist.pendown()\nartist.forward(95)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-21-mini-proekt-chasy.ipynb")
    print(f"Записано: 07-21-mini-proekt-chasy.ipynb ({len(nb)} ячеек)")


def build_22_mishen() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-22 · Координатная мишень\n\nПрактика к разделу [«Мини-проект: координатная мишень»]({CH7_URL}/07-22-mini-proekt-mishen.html).")
    nb.md("## Цель\n\nСобрать инфографику из колец, осей, случайных точек и подписи.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nДва концентрических кольца.")
    nb.code('import random\nartist.reset()\nrandom.seed(1)\nfor radius, color in [(100, "#DC2626"), (60, "#FAFAFC")]:\n    artist.penup()\n    artist.goto(0, -radius)\n    artist.pendown()\n    artist.fillcolor(color)\n    artist.begin_fill()\n    artist.circle(radius)\n    artist.end_fill()')
    nb.md("## Задание ★★ Самостоятельная практика\n\nДобавьте третье, самое маленькое кольцо (радиус 25, цвет \"#DC2626\") и 4 случайные точки внутри мишени (random.seed(2)).")
    nb.code('artist.penup()\nartist.goto(0, -25)\nartist.pendown()\nartist.fillcolor("#DC2626")\nartist.begin_fill()\nartist.circle(25)\nartist.end_fill()\n\nrandom.seed(2)\nartist.penup()\nfor _ in range(4):\n    x = random.randint(-90, 90)\n    y = random.randint(-90, 90)\n    artist.goto(x, y)\n    artist.dot(10, "#059669")')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "07-22-mini-proekt-mishen.ipynb")
    print(f"Записано: 07-22-mini-proekt-mishen.ipynb ({len(nb)} ячеек)")


def build_23_otladka() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-23 · Отладка графики\n\nПрактика к разделу [«Отладка графики»]({CH7_URL}/07-23-otladka-grafiki.html) — чистое рассуждение, без окна Turtle.")
    nb.md("## Цель\n\nПонять, к чему приводит забытый screen.update() после tracer(0).")
    nb.md("## Рабочий пример\n\nЕсли tracer(0) установлен, а update() не вызван ни разу — сколько раз экран показал результат рисования?")
    nb.code('# tracer(0) отключает промежуточные обновления полностью\n# без единого update() экран НИ РАЗУ не покажет нарисованное\npokazy = 0\nprint(pokazy)')
    nb.md("## Задание ★ Базовая практика\n\nПрограмма вызывает screen.tracer(0), рисует 100 команд, но НЕ вызывает screen.update() ни разу. Сколько раз обновится экран? Выведите число.")
    nb.code('kolichestvo_obnovlenij = 0\nprint(kolichestvo_obnovlenij)')
    nb.write(OUT_DIR / "07-23-otladka-grafiki.ipynb")
    print(f"Записано: 07-23-otladka-grafiki.ipynb ({len(nb)} ячеек)")


def build_24_steps_formula() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-24 · Формула для circle(steps=...)\n\nПрактика к разделу [«circle(steps=...) — от круга к многоугольнику»]({CH7_URL}/07-14-circle-steps.html) — чистая математика, без окна Turtle.")
    nb.md("## Цель\n\nСчитать угол поворота многоугольника, приближающего окружность, для разного числа steps.")
    nb.md("## Рабочий пример")
    nb.code('steps = 5\npovorot = 360 / steps\nprint(povorot)')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте угол поворота для circle(80, steps=3), circle(80, steps=4) и circle(80, steps=8). Выведите все три числа через пробел одним print().")
    nb.code('povorot_3 = 360 / 3\npovorot_4 = 360 / 4\npovorot_8 = 360 / 8\nprint(povorot_3, povorot_4, povorot_8)')
    nb.write(OUT_DIR / "07-24-formula-shagov.ipynb")
    print(f"Записано: 07-24-formula-shagov.ipynb ({len(nb)} ячеек)")


def build_25_clear_reset_home_predict() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 07-25 · Предскажите: clear, reset, home\n\nПрактика к разделу [«clear(), reset() и home()»]({CH7_URL}/07-20-clear-reset-home.html) — чистое рассуждение, без окна Turtle.")
    nb.md("## Цель\n\nЗапомнить, какая из трёх команд двигает черепашку, а какая — нет.")
    nb.md("## Рабочий пример\n\nПредскажите: clear() двигает черепашку?")
    nb.code('clear_dvigaet_cherepashku = False\nprint(clear_dvigaet_cherepashku)')
    nb.md("## Задание ★ Базовая практика\n\nДля каждой из трёх команд укажите (True/False), двигает ли она черепашку в (0, 0): clear(), reset(), home(). Выведите три значения через пробел одним print(), в этом порядке.")
    nb.code('clear_dvigaet = False\nreset_dvigaet = True\nhome_dvigaet = True\nprint(clear_dvigaet, reset_dvigaet, home_dvigaet)')
    nb.write(OUT_DIR / "07-25-predskazhite-clear-reset-home.ipynb")
    print(f"Записано: 07-25-predskazhite-clear-reset-home.ipynb ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_10_colormode()
    build_11_pero_zalivka()
    build_12_speed_tracer()
    build_13_geometriya()
    build_14_circle_steps()
    build_15_vyravnivanie()
    build_16_tekst_koordinaty()
    build_17_forma()
    build_18_neskolko()
    build_19_clone()
    build_20_clear_reset_home()
    build_21_chasy()
    build_22_mishen()
    build_23_otladka()
    build_24_steps_formula()
    build_25_clear_reset_home_predict()
    print("Все 16 новых ноутбуков главы 7 собраны.")
