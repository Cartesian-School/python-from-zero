#!/usr/bin/env python3
"""Строит 12 новых ноутбуков практики для Главы 6.

10 локальных (local-required, реальное окно turtle — следуют паттерну
существующих ноутбуков главы: общие screen/artist создаются один раз,
каждая следующая ячейка вызывает artist.reset() перед своим кодом, в конце
— screen.bye()):
    06-09, 06-10, 06-11, 06-12, 06-13, 06-14, 06-15, 06-16, 06-17, 06-18

2 браузерных (browser-pyodide + automatic, чистая геометрия без import
turtle — Pyodide не умеет открывать нативные окна):
    06-19 (предсказать курс и координату), 06-20 (формула 360/n)

Существующие 06-02/03/04/06/07/08 НЕ трогаем.

ВАЖНО: ни у одного нового ноутбука первая КОДОВАЯ ячейка не помечена
raises=True.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-06"
CH6_URL = "../../site/chapters/glava-06"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = 'import turtle\n\nscreen = turtle.Screen()\nartist = turtle.Turtle()\nartist.pensize(3)\nartist.pencolor("#5B24F9")\nprint("Окно Turtle готово.")'
CLOSE_MD = "## Завершение (выполнить один раз, в самом конце)"
CLOSE_CODE = 'screen.bye()\nprint("Окно Turtle закрыто.")'


def build_09_koordinaty() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-09 · Координаты: центр (0, 0)\n\nПрактика к разделу [«Координаты: центр (0, 0)»]({CH6_URL}/06-09-koordinaty.html).")
    nb.md("## Цель\n\nОсвоить систему координат окна Turtle и команду goto().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nПереместимся в четыре разные точки, отмечая каждую точкой.")
    nb.code('artist.reset()\nartist.penup()\nfor x, y in [(100, 0), (-100, 0), (0, 100), (0, -100)]:\n    artist.goto(x, y)\n    artist.dot(12, "#5B24F9")\nartist.goto(0, 0)')
    nb.md("## Эксперимент 1\n\nПредскажите, в какой четверти экрана окажется точка (-150, -100), прежде чем запускать.")
    nb.code('artist.reset()\nartist.penup()\nartist.goto(-150, -100)\nartist.dot(14, "#DB2777")')
    nb.md("## Задание ★ Базовая практика\n\nПоставьте точки в трёх вершинах треугольника: (0, 100), (-100, -100), (100, -100).")
    nb.code('artist.reset()\nartist.penup()\nfor x, y in [(0, 100), (-100, -100), (100, -100)]:\n    artist.goto(x, y)\n    artist.dot(12, "#5B24F9")')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-09-koordinaty.ipynb")
    print(f"Записано: 06-09-koordinaty.ipynb ({len(nb)} ячеек)")


def build_10_napravlenie() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-10 · Направление и угол\n\nПрактика к разделу [«Направление и угол»]({CH6_URL}/06-10-napravlenie-i-ugol.html).")
    nb.md("## Цель\n\nРазличать позицию и курс черепашки; связать градусы с направлениями сторон света.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nЧетыре курса из одной точки.")
    nb.code('artist.reset()\nfor angle in [0, 90, 180, 270]:\n    artist.setheading(angle)\n    artist.forward(80)\n    artist.backward(80)')
    nb.md("## Эксперимент 1\n\nПредскажите курс после этих команд, затем проверьте heading().")
    nb.code('artist.reset()\nartist.left(45)\nartist.right(90)\nprint(artist.heading())')
    nb.md("## Задание ★ Базовая практика\n\nПоверните черепашку так, чтобы её курс стал строго 225°, используя любые left()/right() от начального курса 0°, и выведите artist.heading().")
    nb.code('artist.reset()\nartist.left(225)\nprint(artist.heading())')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-10-napravlenie-i-ugol.ipynb")
    print(f"Записано: 06-10-napravlenie-i-ugol.ipynb ({len(nb)} ячеек)")


def build_11_pervye_figury() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-11 · Первые фигуры и формула 360/n\n\nПрактика к разделу [«Первые фигуры и формула 360/n»]({CH6_URL}/06-11-pervye-figury.html).")
    nb.md("## Цель\n\nПрименить формулу поворота 360/n к разным многоугольникам.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nТреугольник — поворот 360/3 = 120°.")
    nb.code('artist.reset()\nfor _ in range(3):\n    artist.forward(100)\n    artist.right(120)')
    nb.md("## Эксперимент 1\n\nПредскажите угол поворота для восьмиугольника (n=8), затем проверьте.")
    nb.code('artist.reset()\npovorot = 360 / 8\nfor _ in range(8):\n    artist.forward(60)\n    artist.right(povorot)')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте правильный десятиугольник (n=10), вычислив угол поворота по формуле 360/n (не вписывайте число вручную).")
    nb.code('artist.reset()\nn = 10\npovorot = 360 / n\nfor _ in range(n):\n    artist.forward(50)\n    artist.right(povorot)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-11-pervye-figury.ipynb")
    print(f"Записано: 06-11-pervye-figury.ipynb ({len(nb)} ячеек)")


def build_12_pero() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-12 · Поднять и опустить перо\n\nПрактика к разделу [«Поднять и опустить перо»]({CH6_URL}/06-12-pero-vverh-vniz.html).")
    nb.md("## Цель\n\nОсвоить penup()/pendown() — движение без рисования.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nЛиния — пробел — линия.")
    nb.code('artist.reset()\nartist.forward(60)\nartist.penup()\nartist.forward(60)\nartist.pendown()\nartist.forward(60)')
    nb.md("## Эксперимент 1\n\nПроверьте isdown() до и после penup().")
    nb.code('artist.reset()\nprint(artist.isdown())\nartist.penup()\nprint(artist.isdown())\nartist.pendown()')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте пунктирную линию из четырёх штрихов по 20 пикселей с промежутками по 20 пикселей (penup между штрихами).")
    nb.code('artist.reset()\nfor _ in range(4):\n    artist.forward(20)\n    artist.penup()\n    artist.forward(20)\n    artist.pendown()')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-12-pero-vverh-vniz.ipynb")
    print(f"Записано: 06-12-pero-vverh-vniz.ipynb ({len(nb)} ячеек)")


def build_13_cvet() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-13 · Цвет, толщина и внешний вид\n\nПрактика к разделу [«Цвет, толщина и внешний вид»]({CH6_URL}/06-13-cvet-tolschina-vid.html).")
    nb.md("## Цель\n\nОсвоить pensize(), pencolor(), shape() и bgcolor().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nТолстая синяя линия.")
    nb.code('artist.reset()\nartist.pensize(10)\nartist.pencolor("#2563EB")\nartist.forward(200)')
    nb.md("## Эксперимент 1\n\nПоменяйте форму курсора на черепаху и цвет фона окна.")
    nb.code('artist.shape("turtle")\nscreen.bgcolor("#FAFAFC")\nartist.reset()\nartist.pensize(3)\nartist.pencolor("#5B24F9")\nartist.forward(100)')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте линию толщиной 5 и цветом \"green\", длиной 150 пикселей.")
    nb.code('artist.shape("classic")\nartist.reset()\nartist.pensize(5)\nartist.pencolor("green")\nartist.forward(150)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-13-cvet-tolschina-vid.ipynb")
    print(f"Записано: 06-13-cvet-tolschina-vid.ipynb ({len(nb)} ячеек)")


def build_14_zalivka() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-14 · Заливка, круг, дуга и точка\n\nПрактика к разделу [«Заливка, круг, дуга и точка»]({CH6_URL}/06-14-zalivka-krug-tochka.html).")
    nb.md("## Цель\n\nОсвоить begin_fill()/end_fill(), circle() и dot().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nЗакрашенный квадрат.")
    nb.code('artist.reset()\nartist.fillcolor("#B9A0FC")\nartist.begin_fill()\nfor _ in range(4):\n    artist.forward(100)\n    artist.right(90)\nartist.end_fill()')
    nb.md("## Эксперимент 1\n\nНарисуйте окружность радиусом 60, затем половину окружности (extent=180) рядом.")
    nb.code('artist.reset()\nartist.circle(60)\nartist.penup()\nartist.forward(150)\nartist.pendown()\nartist.circle(60, 180)')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте закрашенный круг радиусом 50 (fillcolor любой на ваш выбор).")
    nb.code('artist.reset()\nartist.fillcolor("#DB2777")\nartist.begin_fill()\nartist.circle(50)\nartist.end_fill()')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-14-zalivka-krug-tochka.ipynb")
    print(f"Записано: 06-14-zalivka-krug-tochka.ipynb ({len(nb)} ячеек)")


def build_15_sluchaynoe_dvizhenie() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-15 · Случайное движение\n\nПрактика к разделу [«Случайное движение»]({CH6_URL}/06-15-sluchaynoe-dvizhenie.html).")
    nb.md("## Цель\n\nСмоделировать случайное блуждание (random walk) и увидеть роль random.seed().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nСлучайное блуждание с фиксированным seed.")
    nb.code('import random\n\nartist.reset()\nrandom.seed(1)\nfor _ in range(30):\n    artist.forward(15)\n    artist.right(random.randint(-60, 60))')
    nb.md("## Эксперимент 1\n\nЗапустите ту же ячейку заново — траектория должна получиться ТОЙ ЖЕ самой (тот же seed).")
    nb.code('artist.reset()\nrandom.seed(1)\nfor _ in range(30):\n    artist.forward(15)\n    artist.right(random.randint(-60, 60))')
    nb.md("## Задание ★ Базовая практика\n\nЗапустите случайное блуждание из 50 шагов с random.seed(42).")
    nb.code('artist.reset()\nrandom.seed(42)\nfor _ in range(50):\n    artist.forward(15)\n    artist.right(random.randint(-60, 60))')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-15-sluchaynoe-dvizhenie.ipynb")
    print(f"Записано: 06-15-sluchaynoe-dvizhenie.ipynb ({len(nb)} ячеек)")


def build_16_risuem_po_koordinatam() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-16 · Рисуем по координатам\n\nПрактика к разделу [«Рисуем по координатам»]({CH6_URL}/06-16-risuem-po-koordinatam.html).")
    nb.md("## Цель\n\nСпланировать фигуру в координатах, затем перевести план в код.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nЗакрашенный треугольник по трём координатам.")
    nb.code('artist.reset()\nartist.fillcolor("#B9A0FC")\nartist.penup()\nartist.goto(-60, -50)\nartist.pendown()\nartist.begin_fill()\nartist.goto(60, -50)\nartist.goto(0, 70)\nartist.goto(-60, -50)\nartist.end_fill()')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте закрашенный четырёхугольник по координатам (-80, -40), (80, -40), (60, 60), (-60, 60).")
    nb.code('artist.reset()\nartist.fillcolor("#059669")\nartist.penup()\nartist.goto(-80, -40)\nartist.pendown()\nartist.begin_fill()\nartist.goto(80, -40)\nartist.goto(60, 60)\nartist.goto(-60, 60)\nartist.goto(-80, -40)\nartist.end_fill()')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-16-risuem-po-koordinatam.ipynb")
    print(f"Записано: 06-16-risuem-po-koordinatam.ipynb ({len(nb)} ячеек)")


def build_17_otladka() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-17 · Отладка Turtle\n\nПрактика к разделу [«Отладка Turtle»]({CH6_URL}/06-17-otladka-turtle.html).")
    nb.md("## Цель\n\nНайти и исправить типичные ошибки в коде Turtle.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Типичная ошибка\n\nЭтот код должен был нарисовать квадрат, но забыл один поворот — получается не квадрат.")
    nb.code('artist.reset()\nartist.forward(80)\nartist.right(90)\nartist.forward(80)\nartist.right(90)\nartist.forward(80)\n# пропущен поворот здесь!\nartist.forward(80)')
    nb.md("## Задание ★ Базовая практика\n\nИсправьте код выше так, чтобы получился настоящий квадрат (допишите пропущенный right(90)).")
    nb.code('artist.reset()\nartist.forward(80)\nartist.right(90)\nartist.forward(80)\nartist.right(90)\nartist.forward(80)\nartist.right(90)\nartist.forward(80)')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-17-otladka-turtle.ipynb")
    print(f"Записано: 06-17-otladka-turtle.ipynb ({len(nb)} ячеек)")


def build_18_mini_proekty() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-18 · Мини-проекты\n\nПрактика к разделу [«Мини-проекты»]({CH6_URL}/06-18-mini-proekty.html).")
    nb.md("## Цель\n\nСобрать несколько приёмов главы в одной законченной картинке.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример\n\nПростая мишень из двух колец.")
    nb.code('artist.reset()\nfor radius, color in [(60, "#DC2626"), (30, "#FAFAFC")]:\n    artist.penup()\n    artist.goto(0, -radius)\n    artist.pendown()\n    artist.fillcolor(color)\n    artist.begin_fill()\n    artist.circle(radius)\n    artist.end_fill()')
    nb.md("## Задание ★★ Самостоятельная практика\n\nНарисуйте свою мишень из трёх колец радиусами 80, 55, 30 с чередующимися цветами по вашему выбору.")
    nb.code('artist.reset()\nfor radius, color in [(80, "#2563EB"), (55, "#FAFAFC"), (30, "#2563EB")]:\n    artist.penup()\n    artist.goto(0, -radius)\n    artist.pendown()\n    artist.fillcolor(color)\n    artist.begin_fill()\n    artist.circle(radius)\n    artist.end_fill()')
    nb.md(CLOSE_MD)
    nb.code(CLOSE_CODE)
    nb.write(OUT_DIR / "06-18-mini-proekty.ipynb")
    print(f"Записано: 06-18-mini-proekty.ipynb ({len(nb)} ячеек)")


def build_19_predskazhite() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-19 · Предскажите курс и координату\n\nПрактика к разделу [«Направление и угол»]({CH6_URL}/06-10-napravlenie-i-ugol.html) — на этот раз без реального окна Turtle, чистая геометрия.")
    nb.md("## Цель\n\nНаучиться предсказывать курс и координату черепашки на бумаге, не запуская окно.")
    nb.md("## Рабочий пример\n\nЧерепашка стартует в (0, 0), курс 0° (восток). Команда forward(100) переместит её в (100, 0), курс останется 0°.")
    nb.code('start = (0, 0)\nkurs = 0\n# forward(100) при курсе 0° (восток) прибавляет 100 к x\nfinish = (start[0] + 100, start[1])\nprint(kurs, finish)')
    nb.md("## Задание ★ Базовая практика\n\nЧерепашка начинает в (0, 0), курс 0°. Выполнены команды: forward(120), left(90), forward(80), right(90), forward(50). Посчитайте итоговый курс и координаты вручную и выведите их одним print() в виде `курс координаты` (например: `0 (170, 80)`).")
    nb.code('itogovyj_kurs = 0\nitogovaya_koordinata = (170, 80)\nprint(itogovyj_kurs, itogovaya_koordinata)')
    nb.write(OUT_DIR / "06-19-predskazhite-kurs.ipynb")
    print(f"Записано: 06-19-predskazhite-kurs.ipynb ({len(nb)} ячеек)")


def build_20_formula_mnogougolnika() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 06-20 · Формула 360/n\n\nПрактика к разделу [«Первые фигуры и формула 360/n»]({CH6_URL}/06-11-pervye-figury.html) — чистая математика формулы, без окна Turtle.")
    nb.md("## Цель\n\nСчитать угол поворота для правильного многоугольника с произвольным числом сторон.")
    nb.md("## Рабочий пример")
    nb.code('n = 6\npovorot = 360 / n\nprint(povorot)')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте угол поворота для девятиугольника (n=9) и двенадцатиугольника (n=12). Выведите оба числа через пробел одним print().")
    nb.code('povorot_9 = 360 / 9\npovorot_12 = 360 / 12\nprint(povorot_9, povorot_12)')
    nb.write(OUT_DIR / "06-20-formula-mnogougolnika.ipynb")
    print(f"Записано: 06-20-formula-mnogougolnika.ipynb ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_09_koordinaty()
    build_10_napravlenie()
    build_11_pervye_figury()
    build_12_pero()
    build_13_cvet()
    build_14_zalivka()
    build_15_sluchaynoe_dvizhenie()
    build_16_risuem_po_koordinatam()
    build_17_otladka()
    build_18_mini_proekty()
    build_19_predskazhite()
    build_20_formula_mnogougolnika()
    print("Все 12 новых ноутбуков главы 6 собраны.")
