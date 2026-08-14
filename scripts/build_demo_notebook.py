#!/usr/bin/env python3
"""Строит notebooks/chapter-06/06-02-turtle-dvizhenie.ipynb программно через nbformat.

Важно: turtle.Screen() — процесс-синглтон (Turtle._screen). Повторные
screen.bye() + turtle.Screen() в одном и том же ядре Jupyter приводят к
turtle.Terminator (проверено эмпирически на этом окружении). Поэтому
экран и черепашка создаются один раз в первой ячейке, а каждая следующая
ячейка вызывает artist.reset() перед рисованием; screen.bye() вызывается
только в самой последней ячейке.
"""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "notebooks" / "chapter-06" / "06-02-turtle-dvizhenie.ipynb"

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))


def code(text):
    cells.append(nbf.v4.new_code_cell(text))


md("""\
# 06-02 · Движение вперёд и назад

Практика к разделу [«Движение вперёд и назад»](../../site/chapters/glava-06/06-02-dvizhenie-vpered-nazad.html)
(Глава 6 · Turtle, книга «Python с нуля», Cartesian School).""")

md("""\
## Цель

Научиться управлять черепашкой Turtle: `forward`, `backward`, `right`, `left` —
и на практике почувствовать разницу между **движением** и **поворотом**.""")

md("""\
## Что нужно знать

Этот ноутбук — лаборатория к уже прочитанному разделу теории. Если вы попали сюда
впервые, коротко: у черепашки есть позиция и курс (направление). `forward`/`backward`
двигают её по прямой, `left`/`right` только поворачивают курс.""")

md("""\
## Краткое напоминание

- `artist.forward(n)` / `artist.fd(n)` — вперёд на `n` пикселей
- `artist.backward(n)` / `artist.bk(n)` / `artist.back(n)` — назад на `n` пикселей
- `artist.left(угол)` / `artist.lt(угол)` — повернуть против часовой стрелки
- `artist.right(угол)` / `artist.rt(угол)` — повернуть по часовой стрелке

**Особенность работы в Jupyter:** окно Turtle открывается один раз на весь ноутбук —
мы создаём `screen` и `artist` в следующей ячейке. Перед каждым новым рисунком
вызываем `artist.reset()`, чтобы очистить холст и вернуть черепашку в начало
координат; закрываем окно командой `screen.bye()` только в самой последней ячейке.
(Технически создать и закрыть отдельное окно Turtle в каждой ячейке невозможно —
модуль `turtle` не рассчитан на это внутри одного процесса.)""")

md("## Настройка (выполнить один раз)")

code("""\
import turtle

screen = turtle.Screen()
artist = turtle.Turtle()
print("Окно Turtle готово. Позиция:", artist.position(), "| курс:", artist.heading())""")

md("## Рабочий пример")

code("""\
artist.reset()

# едем вперёд на 120 пикселей
artist.forward(120)

# поворачиваем на 90 градусов против часовой стрелки
artist.left(90)

# едем вперёд ещё раз — получаем букву «Г»
artist.forward(80)

print("Позиция:", artist.position())
print("Курс:", artist.heading())""")

md("""\
## Эксперимент 1

Измените расстояние `120` на `250` и угол `90` на `45`. Перед запуском попробуйте
предсказать: в какую сторону теперь «смотрит» черепашка после поворота?""")

code("""\
artist.reset()

artist.forward(250)   # было 120
artist.left(45)       # было 90
artist.forward(80)

print("Курс после поворота:", artist.heading(), "градусов")""")

md("""\
## Эксперимент 2

Добавьте третью пару команд `left(90)` и `forward(120)` в конец программы. Какая
фигура получится?""")

code("""\
artist.reset()

artist.forward(120)
artist.left(90)
artist.forward(80)
artist.left(90)        # новый поворот
artist.forward(120)    # новая сторона

print("Позиция:", artist.position())
print("Курс:", artist.heading())""")

md("""\
## Задание ★ Базовая практика

Используя только `forward`, `backward`, `left` и `right`, нарисуйте букву «Т» одной
непрерывной линией пера: сначала верхнюю перекладину, потом ножку вниз от её середины.

Один из вариантов решения — ниже. Попробуйте написать свой вариант **до** того, как
запускать эту ячейку.""")

code("""\
artist.reset()

# верхняя перекладина: сначала правая половина, потом через центр — левая
artist.forward(40)
artist.backward(80)
artist.forward(40)  # возвращаемся точно в центр перекладины

# ножка буквы «Т» — вниз от центра перекладины
artist.right(90)
artist.forward(100)

print("Позиция:", artist.position())
print("Курс:", artist.heading())""")

md("""\
## Проверка результата

После выполнения ячейки с заданием черепашка должна закончить движение в точке
`(0.0, -100.0)` с курсом `270°` (смотрит вниз) — низ ножки буквы «Т».

Следующая ячейка повторяет решение и автоматически проверяет конечное состояние.""")

code("""\
artist.reset()

artist.forward(40)
artist.backward(80)
artist.forward(40)
artist.right(90)
artist.forward(100)

x, y = artist.position()
assert round(x, 1) == 0.0, f"Неожиданная координата x: {x}"
assert round(y, 1) == -100.0, f"Неожиданная координата y: {y}"
assert artist.heading() == 270.0, f"Неожиданный курс: {artist.heading()}"

print("Проверка пройдена: буква «Т» нарисована корректно.")""")

md("""\
## Типичная ошибка

Начинающие часто путают `right()`/`left()` с движением — кажется, что черепашка
должна сместиться в сторону. На самом деле эти команды **только поворачивают** курс
и не двигают черепашку ни на пиксель. Ниже — программа с этой ошибкой: вместо буквы
«Г» получается просто прямая линия длиной 200, потому что поворот «потерялся» между
двумя одинаковыми движениями вперёд.""")

code("""\
artist.reset()

artist.forward(120)
# ошибка: забыли повернуть здесь
artist.forward(80)

print("Курс (не изменился!):", artist.heading())
print("Черепашка проехала прямо, а не буквой «Г»:", artist.position())""")

md("""\
## Исправление

Добавляем пропущенный поворот между двумя движениями:""")

code("""\
artist.reset()

artist.forward(120)
artist.left(90)   # добавили поворот
artist.forward(80)

print("Курс после исправления:", artist.heading())
print("Позиция:", artist.position())""")

md("""\
## Самостоятельная практика

Нарисуйте лестницу из трёх одинаковых «ступенек» (вперёд-поворот-вперёд-поворот,
повторить трижды). Пока не изучены циклы (глава 10), просто повторите нужный блок
команд вручную три раза подряд.""")

code("""\
artist.reset()

# одна ступенька — допишите ещё две по тому же образцу
artist.forward(40)
artist.left(90)
artist.forward(40)
artist.right(90)

print("Позиция после одной ступеньки:", artist.position())""")

md("""\
## Дополнительная задача ★★★

Нарисуйте пятиконечную звезду одной линией, используя только `forward` и один и тот
же угол поворота между всеми пятью движениями. Подсказка: сумма внешних углов
многоугольника всегда равна 360° — для пятиконечной звезды этот угол равен 144°.""")

code("""\
artist.reset()

for _ in range(5):
    artist.forward(150)
    artist.right(144)

print("Звезда нарисована. Финальная позиция:", artist.position())""")

md("## Завершение (выполнить один раз, в самом конце)")

code("""\
screen.bye()
print("Окно Turtle закрыто.")""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {
        "display_name": "Cartesian Python 3.14",
        "language": "python",
        "name": "cartesian-python314",
    },
    "language_info": {"name": "python", "version": "3.14.6"},
}

OUT.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, OUT)
print(f"Записано: {OUT}")
print(f"Ячеек: {len(cells)}")
