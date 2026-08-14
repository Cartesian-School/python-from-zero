#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 7 (Turtle подробно)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-07"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = '''import turtle

screen = turtle.Screen()
artist = turtle.Turtle()
artist.speed(0)
print("Окно Turtle готово.")'''
TEARDOWN_MD = "## Завершение (выполнить один раз, в самом конце)"
TEARDOWN_CODE = '''screen.bye()
print("Окно Turtle закрыто.")'''


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 07-01 · Настраиваем экран и графику\n\nПрактика к разделам "
          "[«Настраиваем экран»](../../site/chapters/glava-07/07-01-nastraivaem-ekran.html) и "
          "[«Настраиваем графику»](../../site/chapters/glava-07/07-02-nastraivaem-grafiku.html).")
    nb.md("## Цель\n\nНастроить холст и черепашку: заголовок, фон, скорость, толщину и цвет линии.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''screen.title("Моя первая картина")
screen.bgcolor("lightblue")
artist.pensize(3)
artist.pencolor("purple")
artist.forward(100)
print("Настройки применены.")''')
    nb.md("## Эксперимент 1\n\nПопробуйте свой любимый цвет фона и линии.")
    nb.code('''artist.reset()
screen.bgcolor("black")
artist.pencolor("yellow")
artist.forward(100)
print("Готово.")''')
    nb.md("## Эксперимент 2\n\nИзмените скорость на 1 (медленно) и на 0 (мгновенно) — сравните "
          "разницу, если запускаете локально с настоящим окном.")
    nb.code('''artist.reset()
artist.speed(1)
artist.forward(80)
print("Скорость 1 — медленно.")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте квадрат толстой (5px) красной линией на "
          "жёлтом фоне.")
    nb.code('''artist.reset()
screen.bgcolor("yellow")
artist.pensize(5)
artist.pencolor("red")
for _ in range(4):
    artist.forward(100)
    artist.right(90)
print("Готово.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "07-01-ekran-i-grafika.ipynb")
    print(f"Записано: 07-01 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 07-03 · Фигуры без линий, окружности, точки\n\nПрактика к разделу "
          "[«Фигуры без линий, окружности, точки»](../../site/chapters/glava-07/07-03-figury-bez-linij.html) "
          "(включает материал из «Ещё больше возможностей»).")
    nb.md("## Цель\n\nОсвоить заливку, circle(), dot(), stamp(), hideturtle() и undo().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример — заливка")
    nb.code('''artist.reset()
artist.fillcolor("gold")
artist.begin_fill()
for _ in range(4):
    artist.forward(100)
    artist.right(90)
artist.end_fill()
print("Квадрат залит золотым цветом.")''')
    nb.md("## Эксперимент 1 — окружности")
    nb.code('''artist.reset()
artist.circle(60)
print("Позиция после окружности:", artist.position())''')
    nb.md("## Эксперимент 2 — точки разных цветов и размеров")
    nb.code('''artist.reset()
artist.penup()
for i, цвет in enumerate(["red", "green", "blue"]):
    artist.goto(i * 40, 0)
    artist.dot(20, цвет)
print("Три цветные точки нарисованы.")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте залитый зелёный круг радиусом 50.")
    nb.code('''artist.reset()
artist.fillcolor("green")
artist.begin_fill()
artist.circle(50)
artist.end_fill()
print("Зелёный круг готов.")''')
    nb.md("## Дополнительная задача ★★★ — stamp() и undo()")
    nb.code('''artist.reset()
artist.shape("circle")
artist.stamp()
artist.forward(40)
artist.stamp()
artist.undo()  # отменяем последний stamp/движение
print("Готово — попробуйте разное число undo().")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "07-03-figury-okruzhnosti.ipynb")
    print(f"Записано: 07-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 07-04 · Дуги\n\nПрактика к разделу "
          "[«Дуги»](../../site/chapters/glava-07/07-04-dugi.html).")
    nb.md("## Цель\n\nНарисовать дуги разного размера с помощью параметра extent.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
artist.circle(80, 180)
print("Позиция после полукруга:", artist.position())''')
    nb.md("## Эксперимент 1\n\nПопробуйте extent = 90, 270 и 360 (полная окружность) на том же "
          "радиусе.")
    nb.code('''for extent in [90, 270, 360]:
    artist.reset()
    artist.circle(80, extent)
    print(f"extent={extent}: финальная позиция {artist.position()}")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте купол домика: дугу 180° радиусом 60, "
          "затем прямую вниз с обеих сторон.")
    nb.code('''artist.reset()
artist.circle(60, 180)
artist.left(90)
artist.forward(60)
print("Купол с одной стеной готов.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "07-04-dugi.ipynb")
    print(f"Записано: 07-04 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 07-06 · Текст на экране\n\nПрактика к разделу "
          "[«Рисуем текст на экране»](../../site/chapters/glava-07/07-06-tekst-na-ekrane.html).")
    nb.md("## Цель\n\nВыводить текст на холсте Turtle командой write().")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
artist.write("Привет, Turtle!", font=("Arial", 20, "normal"))
print("Текст нарисован.")''')
    nb.md("## Эксперимент 1\n\nПопробуйте выравнивание по центру и полужирное начертание.")
    nb.code('''artist.reset()
artist.write("По центру", align="center", font=("Arial", 24, "bold"))
print("Готово.")''')
    nb.md("## Задание ★ Базовая практика\n\nВыведите своё имя большим курсивным шрифтом в "
          "верхней части экрана.")
    nb.code('''artist.reset()
artist.penup()
artist.goto(0, 100)
artist.write("Cartesian", align="center", font=("Arial", 28, "italic"))
print("Готово.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "07-06-tekst.ipynb")
    print(f"Записано: 07-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 07-07 · Окружность внутри квадрата\n\nПрактика к разделам "
          "[«Мини-проект — окружность внутри квадрата»](../../site/chapters/glava-07/07-07-mini-proekt-okruzhnost-kvadrat.html) "
          "и [«Меняем направление рисования»](../../site/chapters/glava-07/07-08-napravlenie-risovaniya.html).")
    nb.md("## Цель\n\nСкомбинировать фигуры и попрактиковать направление рисования окружности.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
razmer = 150

for _ in range(4):
    artist.forward(razmer)
    artist.right(90)

artist.penup()
artist.goto(razmer / 2, -razmer / 2)
artist.setheading(0)
artist.pendown()
artist.circle(razmer / 2)
print("Квадрат с вписанной окружностью готов.")''')
    nb.md("## Эксперимент 1 — направление окружности")
    nb.code('''artist.reset()
artist.circle(60)    # против часовой стрелки
print("Курс после обычной окружности:", artist.heading())

artist.reset()
artist.circle(-60)   # по часовой стрелке
print("Курс после окружности с отрицательным радиусом:", artist.heading())''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nВпишите окружность в шестиугольник со "
          "стороной 80 (подсказка: радиус вписанной окружности шестиугольника — "
          "`сторона * 0.866`).")
    nb.code('''import math

artist.reset()
storona = 80
for _ in range(6):
    artist.forward(storona)
    artist.right(60)

radius = storona * math.sqrt(3) / 2
artist.penup()
artist.goto(0, -radius)
artist.setheading(0)
artist.pendown()
artist.circle(radius)
print("Окружность вписана в шестиугольник, радиус:", round(radius, 1))''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "07-07-okruzhnost-v-kvadrate.ipynb")
    print(f"Записано: 07-07 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 07-09 · Мини-проект — смайлик\n\nПрактика к разделу "
          "[«Мини-проект — смайлик»](../../site/chapters/glava-07/07-09-mini-proekt-smajlik-itogi.html).")
    nb.md("## Цель\n\nСобрать все приёмы главы в одном рисунке.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()

artist.fillcolor("yellow")
artist.begin_fill()
artist.circle(100)
artist.end_fill()

artist.penup()
artist.goto(-35, 120)
artist.pendown()
artist.dot(20, "black")
artist.penup()
artist.goto(35, 120)
artist.pendown()
artist.dot(20, "black")

artist.penup()
artist.goto(-50, 60)
artist.setheading(-60)
artist.pendown()
artist.pensize(4)
artist.circle(60, 120)

print("Смайлик готов.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте две розовые щёчки под глазами.")
    nb.code('''artist.penup()
artist.goto(-55, 90)
artist.pendown()
artist.dot(15, "pink")

artist.penup()
artist.goto(55, 90)
artist.pendown()
artist.dot(15, "pink")

print("Румяные щёчки добавлены.")''')
    nb.md("## Дополнительная задача ★★★\n\nПоменяйте выражение лица: разверните дугу улыбки, "
          "чтобы получились нахмуренные брови.")
    nb.code('''artist.reset()
artist.fillcolor("yellow")
artist.begin_fill()
artist.circle(100)
artist.end_fill()

artist.penup()
artist.goto(-50, 20)
artist.setheading(60)
artist.pendown()
artist.pensize(4)
artist.circle(-60, 120)  # отрицательный радиус — дуга рисуется в другую сторону
print("Хмурое лицо готово.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "07-09-smajlik.ipynb")
    print(f"Записано: 07-09 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_03()
    build_04()
    build_06()
    build_07()
    build_09()
