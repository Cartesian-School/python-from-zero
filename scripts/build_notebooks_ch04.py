#!/usr/bin/env python3
"""Строит 4 ноутбука практики для Главы 4."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-04"


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 04-01 · Числа и переменные\n\nПрактика к разделу "
          "[«Числа в Python, сохраняем числа»](../../site/chapters/glava-04/04-01-chisla-i-peremennye.html).")
    nb.md("## Цель\n\nНаучиться сохранять числа в переменные и правильно их называть.")
    nb.md("## Что нужно знать\n\n`print()` — уже знакомая команда из глав 1 и 3.")
    nb.md("## Краткое напоминание\n\nИмя переменной — буквы, цифры, `_`; не начинается с цифры; "
          "стиль — `snake_case`.")
    nb.md("## Рабочий пример")
    nb.code('''age = 10
print(age)

age = 11  # значение можно заменить
print(age)''')
    nb.md("## Эксперимент 1\n\nСоздайте переменную `city` со своим городом и выведите её.")
    nb.code('''city = "Москва"
print(city)''')
    nb.md("## Эксперимент 2\n\nСоздайте две переменные и выведите их сумму.")
    nb.code('''a = 5
b = 7
print(a + b)''')
    nb.md("## Типичная ошибка\n\nИмя переменной не может начинаться с цифры.")
    nb.code('''1_place = "Cartesian"''', raises=True)
    nb.md("## Исправление")
    nb.code('''place_1 = "Cartesian"
print(place_1)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте переменные `name`, `age`, `city` со своими "
          "данными и выведите их одной командой `print()` через запятую.")
    nb.code('''name = "Cartesian"
age = 5
city = "Москва"
print(name, age, city)''')
    nb.md("## Самостоятельная практика ★★\n\nПосчитайте, сколько дней в `age` годах (приблизительно, "
          "365 дней в году), сохранив результат в новую переменную `days`.")
    nb.code('''age = 12
days = age * 365
print(days)''')
    nb.write(OUT_DIR / "04-01-chisla-i-peremennye.ipynb")
    print(f"Записано: 04-01 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 04-03 · Числа бывают разных видов\n\nПрактика к разделу "
          "[«Числа бывают разных видов»](../../site/chapters/glava-04/04-03-vidy-chisel.html).")
    nb.md("## Цель\n\nПотрогать три числовых типа руками: `int`, `float`, `complex`.")
    nb.md("## Что нужно знать\n\n`type(значение)` показывает тип значения.")
    nb.md("## Краткое напоминание\n\n`int` — целые, `float` — дробные, `complex` — комплексные "
          "(с `j`).")
    nb.md("## Рабочий пример")
    nb.code('''print(type(10))
print(type(10.0))
print(type(3 + 4j))''')
    nb.md("## Эксперимент 1\n\nПроверьте тип результата деления `/` и целочисленного деления "
          "`//`.")
    nb.code('''print(10 / 2, type(10 / 2))
print(10 // 2, type(10 // 2))''')
    nb.md("## Эксперимент 2\n\nУ комплексного числа есть части `.real` и `.imag` — попробуйте.")
    nb.code('''z = 3 + 4j
print(z.real)
print(z.imag)''')
    nb.md("## Типичная ошибка\n\nЛегко перепутать `float` с нулевой дробной частью и `int` — они "
          "выглядят по-разному только благодаря точке.")
    nb.code('''a = 2
b = 2.0
print(a == b)       # True — значения равны
print(type(a) == type(b))  # False — типы разные''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте по одному значению каждого типа (`int`, "
          "`float`, `complex`) и выведите тип каждого через `type()`.")
    nb.code('''i = 42
f = 3.14
c = 1 + 2j
print(type(i), type(f), type(c))''')
    nb.md("## Дополнительная задача ★★★\n\n`10 ** 100` — очень большое целое число. Выведите "
          "его и его тип: осталось ли оно `int`, несмотря на огромный размер?")
    nb.code('''huge = 10 ** 100
print(type(huge))
print(len(str(huge)), "цифр")''')
    nb.write(OUT_DIR / "04-03-vidy-chisel.ipynb")
    print(f"Записано: 04-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 04-04 · Преобразование типов чисел\n\nПрактика к разделу "
          "[«Преобразование типов чисел»](../../site/chapters/glava-04/04-04-preobrazovanie-tipov.html).")
    nb.md("## Цель\n\nОсвоить `int()`, `float()`, `str()` и их подводные камни.")
    nb.md("## Что нужно знать\n\nКаждый числовой тип — одновременно и функция-преобразователь.")
    nb.md("## Краткое напоминание\n\n`int()` **отбрасывает** дробную часть, а не округляет.")
    nb.md("## Рабочий пример")
    nb.code('''print(int(3.99))
print(float(7))
print(str(42), type(str(42)))''')
    nb.md("## Эксперимент 1\n\nСравните `int(3.99)` и `int(-3.99)` — куда «отбрасывается» "
          "дробная часть у отрицательного числа?")
    nb.code('''print(int(3.99))
print(int(-3.99))''')
    nb.md("## Эксперимент 2\n\nПреобразуйте текст `\"25\"` в число и прибавьте к нему 5.")
    nb.code('''age_text = "25"
age = int(age_text)
print(age + 5)''')
    nb.md("## Типичная ошибка\n\nНе любой текст можно превратить в число.")
    nb.code('''int("десять")''', raises=True)
    nb.md("## Исправление\n\nПреобразовывать можно только текст, который действительно выглядит "
          "как число.")
    nb.code('''int("10")''')
    nb.md("## Задание ★ Базовая практика\n\nИсправьте ошибку: соберите строку "
          "`\"Итого: 100\"` из текста `\"Итого: \"` и числа `100` — сначала через "
          "`str()`, затем через f-строку.")
    nb.code('''total = 100
print("Итого: " + str(total))
print(f"Итого: {total}")''')
    nb.write(OUT_DIR / "04-04-preobrazovanie-tipov.ipynb")
    print(f"Записано: 04-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 04-05 · Мини-проект — Понимаете ли вы числа?\n\nПрактика к разделу "
          "[«Мини-проект — Понимаете ли вы числа?»](../../site/chapters/glava-04/04-05-mini-proekt-itogi.html).")
    nb.md("## Цель\n\nПроверить понимание чисел и типов — сначала угадать, потом проверить "
          "запуском.")
    nb.md("""\
## Задание ★ Базовая практика

Сначала запишите на бумаге (или в уме) ваш ответ для каждого выражения, и только потом
запускайте ячейку и сверяйтесь:

1. Тип `10`
2. Тип `10.0`
3. Тип `10 / 2`
4. Тип `10 // 2`
5. Тип `"10"`""")
    nb.code('''print(type(10))
print(type(10.0))
print(type(10 / 2))
print(type(10 // 2))
print(type("10"))''')
    nb.md("## Проверка результата")
    nb.code('''assert type(10) is int
assert type(10.0) is float
assert type(10 / 2) is float
assert type(10 // 2) is int
assert type("10") is str
print("Все пять ответов верны!")''')
    nb.md("""\
## Задание ★★ Самостоятельная задача

Что выведет `print(str(7) + str(9))` — число 16 или что-то другое? Предскажите, затем
проверьте.""")
    nb.code('''print(str(7) + str(9))''')
    nb.md("## Дополнительная задача ★★★\n\nПочему `\"Итого: \" + 100` вызывает ошибку, а "
          "`\"Итого: \" + str(100)` — нет? Продемонстрируйте оба варианта.")
    nb.code('''print("Итого: " + 100)''', raises=True)
    nb.code('''print("Итого: " + str(100))''')
    nb.write(OUT_DIR / "04-05-mini-proekt-chisla.ipynb")
    print(f"Записано: 04-05 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_03()
    build_04()
    build_05()
