#!/usr/bin/env python3
"""Строит ноутбуки практики 06-03..06-08 для Главы 6 (Turtle).

Важно: turtle.Screen() — процесс-синглтон. Экран и черепашка создаются один раз в
первой ячейке, каждая следующая ячейка вызывает artist.reset() перед рисованием;
screen.bye() — только в последней ячейке. (См. notebooks/chapter-06/06-02-turtle-dvizhenie.ipynb
и заметку в scripts/build_demo_notebook.py, где эта проблема была впервые обнаружена
и исправлена через реальный запуск.)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-06"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = '''import turtle

screen = turtle.Screen()
artist = turtle.Turtle()
artist.speed(0)
print("Окно Turtle готово.")'''
TEARDOWN_MD = "## Завершение (выполнить один раз, в самом конце)"
TEARDOWN_CODE = '''screen.bye()
print("Окно Turtle закрыто.")'''


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 06-03 · Меняем направление\n\nПрактика к разделу "
          "[«Заставляем черепашку менять направление»](../../site/chapters/glava-06/06-03-povorot-cherepashki.html).")
    nb.md("## Цель\n\nОсвоить абсолютное направление: `setheading()`, `heading()`, `home()`.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
artist.setheading(90)
artist.forward(100)
artist.setheading(180)
artist.forward(100)
print("Курс:", artist.heading())''')
    nb.md("## Эксперимент 1\n\nПроверьте курс для всех четырёх сторон света: 0°, 90°, 180°, 270°.")
    nb.code('''artist.reset()
for ugol in [0, 90, 180, 270]:
    artist.setheading(ugol)
    artist.forward(60)
    print(f"Курс {ugol}° -> позиция {artist.position()}")''')
    nb.md("## Эксперимент 2\n\n`home()` возвращает черепашку в исходную точку и исходный курс "
          "одной командой.")
    nb.code('''artist.reset()
artist.setheading(45)
artist.forward(100)
print("До home():", artist.position(), artist.heading())

artist.home()
print("После home():", artist.position(), artist.heading())''')
    nb.md("## Типичная ошибка\n\n`left()`/`right()` меняют курс *относительно текущего*, а "
          "`setheading()` — задаёт курс *абсолютно*. Если перепутать, фигура получится не той, "
          "что ожидалось.")
    nb.code('''artist.reset()
artist.setheading(90)   # смотрим вверх
artist.left(90)         # ОТНОСИТЕЛЬНЫЙ поворот от 90 -> 180, а не setheading(90)!
print("Итоговый курс:", artist.heading(), "(вероятно, не то, что ожидали)")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте крест (плюс) из четырёх лучей, выходящих "
          "из центра, используя `setheading()` для каждого луча: 0°, 90°, 180°, 270°.")
    nb.code('''artist.reset()
for ugol in [0, 90, 180, 270]:
    artist.setheading(ugol)
    artist.forward(80)
    artist.backward(80)
print("Готово, финальная позиция:", artist.position())''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "06-03-povorot.ipynb")
    print(f"Записано: 06-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 06-04 · Мини-проекты: квадрат и шестиугольник\n\nПрактика к разделу "
          "[«Мини-проекты: квадрат и шестиугольник»](../../site/chapters/glava-06/06-04-mini-proekty-figury.html).")
    nb.md("## Цель\n\nНарисовать первые настоящие фигуры: квадрат и шестиугольник.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример — квадрат")
    nb.code('''artist.reset()
for _ in range(4):
    artist.forward(100)
    artist.right(90)
print("Курс после квадрата:", artist.heading())''')
    nb.md("## Эксперимент 1 — шестиугольник\n\nУгол поворота = 360 / количество сторон.")
    nb.code('''artist.reset()
for _ in range(6):
    artist.forward(80)
    artist.right(60)
print("Курс после шестиугольника:", artist.heading())''')
    nb.md("## Эксперимент 2\n\nПопробуйте формулу `360 / n` для треугольника (n=3) и "
          "восьмиугольника (n=8).")
    nb.code('''for n in [3, 8]:
    artist.reset()
    ugol = 360 / n
    for _ in range(n):
        artist.forward(70)
        artist.right(ugol)
    print(f"n={n}: угол поворота = {ugol}°")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте правильный пятиугольник, используя "
          "формулу `360 / n`.")
    nb.code('''artist.reset()
n = 5
ugol = 360 / n
for _ in range(n):
    artist.forward(90)
    artist.right(ugol)
print("Пятиугольник готов, угол поворота был", ugol, "градусов")''')
    nb.md("## Проверка результата")
    nb.code('''assert 360 / 5 == 72.0
print("Верно: для пятиугольника угол поворота 72°.")''')
    nb.md("## Дополнительная задача ★★★\n\nНапишите фигуру с n=20 сторонами — на что она "
          "похожа?")
    nb.code('''artist.reset()
n = 20
ugol = 360 / n
for _ in range(n):
    artist.forward(30)
    artist.right(ugol)
print("20-угольник почти неотличим от окружности!")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "06-04-figury.ipynb")
    print(f"Записано: 06-04 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 06-06 · Случайные точки на экране\n\nПрактика к разделу "
          "[«Переходим к случайным точкам на экране»](../../site/chapters/glava-06/06-06-sluchaynye-tochki.html).")
    nb.md("## Цель\n\nОсвоить `goto()`, `penup()`/`pendown()` вместе со случайными числами.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''import random

artist.reset()
artist.penup()
for _ in range(10):
    x = random.randint(-200, 200)
    y = random.randint(-150, 150)
    artist.goto(x, y)
    artist.pendown()
    artist.dot(10)
    artist.penup()
print("10 точек нарисовано.")''')
    nb.md("## Эксперимент 1\n\nЧто произойдёт, если убрать `penup()`/`pendown()`? Проверьте — "
          "чем это отличается от точек выше?")
    nb.code('''import random

artist.reset()
for _ in range(10):
    x = random.randint(-200, 200)
    y = random.randint(-150, 150)
    artist.goto(x, y)   # без penup — линия рисуется при каждом переходе
print("На этот раз получились линии, а не отдельные точки.")''')
    nb.md("## Эксперимент 2\n\nПопробуйте разные размеры точек через `artist.dot(размер)`.")
    nb.code('''import random

artist.reset()
artist.penup()
for размер in [5, 15, 25]:
    x = random.randint(-150, 150)
    y = random.randint(-100, 100)
    artist.goto(x, y)
    artist.dot(размер)
print("Точки трёх разных размеров нарисованы.")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте 5 случайных точек, но так, чтобы все они "
          "были в правой половине экрана (x > 0).")
    nb.code('''import random

artist.reset()
artist.penup()
for _ in range(5):
    x = random.randint(0, 200)
    y = random.randint(-150, 150)
    artist.goto(x, y)
    artist.dot(10)
print("Готово — все точки справа от центра.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "06-06-sluchaynye-tochki.ipynb")
    print(f"Записано: 06-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 06-07 · Квадрат с помощью goto\n\nПрактика к разделу "
          "[«Рисуем квадрат с помощью goto»](../../site/chapters/glava-06/06-07-goto-kvadrat.html).")
    nb.md("## Цель\n\nНарисовать фигуру через прямые координаты, а не движение и повороты.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
artist.goto(100, 0)
artist.goto(100, 100)
artist.goto(0, 100)
artist.goto(0, 0)
print("Квадрат через goto готов.")''')
    nb.md("## Эксперимент 1\n\nНарисуйте треугольник тремя вызовами `goto()`.")
    nb.code('''artist.reset()
artist.goto(100, 0)
artist.goto(50, 90)
artist.goto(0, 0)
print("Треугольник готов.")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте прямоугольник (не квадрат — стороны "
          "разной длины) через `goto()`.")
    nb.code('''artist.reset()
artist.goto(150, 0)
artist.goto(150, 80)
artist.goto(0, 80)
artist.goto(0, 0)
print("Прямоугольник 150x80 готов.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "06-07-goto.ipynb")
    print(f"Записано: 06-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 06-08 · Мини-проект — мандала из прямых линий\n\nПрактика к разделу "
          "[«Мандала и итоги»](../../site/chapters/glava-06/06-08-mandala-itogi.html).")
    nb.md("## Цель\n\nСобрать все приёмы главы в одном узоре.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
shag_ugla = 10
ugol = 0
while ugol < 360:
    artist.setheading(ugol)
    artist.forward(150)
    artist.backward(150)
    ugol += shag_ugla
print("Мандала готова, лучей:", 360 // shag_ugla)''')
    nb.md("## Эксперимент 1 ★ — другой шаг угла\n\nПопробуйте `shag_ugla = 30` — узор станет "
          "гораздо более разреженным.")
    nb.code('''artist.reset()
shag_ugla = 30
ugol = 0
while ugol < 360:
    artist.setheading(ugol)
    artist.forward(150)
    artist.backward(150)
    ugol += shag_ugla
print("Лучей на этот раз:", 360 // shag_ugla)''')
    nb.md("## Эксперимент 2 ★★ — своя длина луча\n\nПопробуйте `forward(80)` вместо 150.")
    nb.code('''artist.reset()
shag_ugla = 10
dlina = 80
ugol = 0
while ugol < 360:
    artist.setheading(ugol)
    artist.forward(dlina)
    artist.backward(dlina)
    ugol += shag_ugla
print("Мандала меньшего размера готова.")''')
    nb.md("## Дополнительная задача ★★★\n\nПопробуйте два цвета: чётные лучи — одним цветом, "
          "нечётные — другим (используем счётчик и `%` из главы 5).")
    nb.code('''artist.reset()
shag_ugla = 10
ugol = 0
i = 0
while ugol < 360:
    artist.pencolor("purple" if i % 2 == 0 else "blue")
    artist.setheading(ugol)
    artist.forward(150)
    artist.backward(150)
    ugol += shag_ugla
    i += 1
artist.pencolor("black")
print("Двухцветная мандала готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "06-08-mandala.ipynb")
    print(f"Записано: 06-08 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_03()
    build_04()
    build_06()
    build_07()
    build_08()
