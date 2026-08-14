#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 8 (строки).

Некоторые разделы используют input() — в автоматически выполняемом ноутбуке нет
живого человека за клавиатурой, поэтому в ячейках с input() он временно подменяется
на функцию, которая подставляет заранее заготовленные ответы (см. INPUT_SETUP_MD/CODE).
Сам код с input() при этом выглядит и работает так же, как в обычном .py-файле.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-08"


def input_setup(answers: list[str]) -> tuple[str, str]:
    md = (
        "## Про input() в этом ноутбуке\n\n"
        "В обычном `.py`-файле `input()` ждёт, пока вы наберёте текст и нажмёте Enter. Этот "
        "ноутбук выполняется автоматически, без живого человека за клавиатурой — поэтому здесь "
        "`input()` временно подменён на заранее заготовленные ответы. Сам код с `input()` ниже "
        "выглядит и работает точно так же, как в обычном файле, который вы запускаете сами."
    )
    answers_repr = ", ".join(repr(a) for a in answers)
    code = f"""_answers = iter([{answers_repr}])

def input(prompt=""):
    answer = next(_answers)
    print(prompt + answer)
    return answer"""
    return md, code


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-01 · Что такое строки?\n\nПрактика к разделам "
          "[«Что такое строки?»](../../site/chapters/glava-08/08-01-chto-takoe-stroki.html) и "
          "[«Кавычки и объединение строк»](../../site/chapters/glava-08/08-02-kavychki-konkatenaciya.html).")
    nb.md("## Цель\n\nСоздавать строки, объединять их и работать с кавычками внутри текста.")
    nb.md("## Рабочий пример")
    nb.code('''greeting = "Привет"
name = "Cartesian"
print(greeting, name)''')
    nb.md("## Эксперимент 1 — многострочная строка")
    nb.code('''poem = """Код за кодом,
шаг за шагом —
так рождается
программа."""
print(poem)''')
    nb.md("## Эксперимент 2 — конкатенация")
    nb.code('''first = "Ада"
last = "Лавлейс"
full = first + " " + last
print(full)''')
    nb.md("## Типичная ошибка\n\nСложение строки и числа напрямую вызывает `TypeError`.")
    nb.code('''"Возраст: " + 10''', raises=True)
    nb.md("## Исправление")
    nb.code('''print("Возраст: " + str(10))
print(f"Возраст: {10}")''')
    nb.md("## Задание ★ Базовая практика\n\nСоставьте строку с кавычками внутри двумя способами "
          "— через другой тип кавычек снаружи и через экранирование.")
    nb.code('''q1 = "Она сказала: 'Привет!'"
q2 = 'Она сказала: "Привет!"'
q3 = "Она сказала: \\"Привет!\\""
print(q1)
print(q2)
print(q3)''')
    nb.write(OUT_DIR / "08-01-stroki.ipynb")
    print(f"Записано: 08-01 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-03 · Индексы, срезы и сравнение строк\n\nПрактика к разделам "
          "[«Доступ к символам строки»](../../site/chapters/glava-08/08-03-dostup-k-simvolam.html) "
          "и [«Истина? Ложь?»](../../site/chapters/glava-08/08-05-istina-lozh.html).")
    nb.md("## Цель\n\nОсвоить индексы, отрицательные индексы, срезы и сравнение строк.")
    nb.md("## Рабочий пример")
    nb.code('''word = "Python"
print(word[0])
print(word[-1])
print(word[0:3])
print(word[::-1])''')
    nb.md("## Эксперимент 1\n\nПроверьте, что `word[::-1]` действительно разворачивает строку "
          "для нескольких разных слов.")
    nb.code('''for w in ["Python", "Cartesian", "мандала"]:
    print(w, "->", w[::-1])''')
    nb.md("## Эксперимент 2 — сравнение и in")
    nb.code('''language = "Python"
print(language == "python")
print("thon" in language)
print("Java" in language)''')
    nb.md("## Типичная ошибка\n\nИндекс за пределами строки вызывает `IndexError`.")
    nb.code('''word = "Python"
word[10]''', raises=True)
    nb.md("## Исправление\n\nПроверяйте длину строки через `len()`, если не уверены в границах.")
    nb.code('''word = "Python"
print(len(word))
if len(word) > 10:
    print(word[10])
else:
    print("Индекс 10 вне диапазона — строка короче.")''')
    nb.md("## Задание ★ Базовая практика\n\nДостаньте первые три и последние три символа слова "
          "«Cartesian» срезами.")
    nb.code('''word = "Cartesian"
print(word[:3])
print(word[-3:])''')
    nb.md("## Проверка результата")
    nb.code('''assert "Cartesian"[:3] == "Car"
assert "Cartesian"[-3:] == "ian"
print("Оба среза верны.")''')
    nb.write(OUT_DIR / "08-03-indeksy-srezy.ipynb")
    print(f"Записано: 08-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-04 · Методы строк\n\nПрактика к разделу "
          "[«Методы строк»](../../site/chapters/glava-08/08-04-metody-strok.html).")
    nb.md("## Цель\n\nОсвоить upper, lower, strip, replace, count, split и другие методы.")
    nb.md("## Рабочий пример")
    nb.code('''text = "Python с нуля"
print(text.upper())
print(text.lower())
print(text.title())''')
    nb.md("## Эксперимент 1")
    nb.code('''text = "  Python с нуля  "
print(repr(text.strip()))
print(text.replace("нуля", "начала"))
print(text.count("н"))''')
    nb.md("## Эксперимент 2 — split()")
    nb.code('''sentence = "Python любит числа и буквы"
words = sentence.split()
print(words)
print(len(words), "слов")''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, начинается ли и заканчивается ли слово "
          "«Cartesian» определёнными буквами.")
    nb.code('''word = "Cartesian"
print(word.startswith("Car"))
print(word.endswith("an"))
print(word.startswith("art"))''')
    nb.md("## Дополнительная задача ★★★\n\nПосчитайте, сколько слов длиннее 4 букв в "
          "предложении.")
    nb.code('''sentence = "Python любит числа и красивые буквы очень сильно"
words = sentence.split()
count = 0
for w in words:
    if len(w) > 4:
        count += 1
print("Длинных слов:", count)''')
    nb.write(OUT_DIR / "08-04-metody-strok.ipynb")
    print(f"Записано: 08-04 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-06 · Форматирование строк\n\nПрактика к разделу "
          "[«Форматирование строк»](../../site/chapters/glava-08/08-06-formatirovanie-strok.html).")
    nb.md("## Цель\n\nСравнить %, .format() и f-строки на практике.")
    nb.md("## Рабочий пример")
    nb.code('''name = "Cartesian"
age = 5

print("Привет, %s! Тебе %d лет." % (name, age))
print("Привет, {}! Тебе {} лет.".format(name, age))
print(f"Привет, {name}! Тебе {age} лет.")''')
    nb.md("## Эксперимент 1 — выражения внутри f-строки")
    nb.code('''age = 5
print(f"Через год будет {age + 1}.")
print(f"Заглавными: {name.upper()}")''')
    nb.md("## Эксперимент 2 — форматирование чисел")
    nb.code('''pi = 3.14159265
print(f"Пи округлённо: {pi:.2f}")
print(f"{1234567:,}")''')
    nb.md("## Задание ★ Базовая практика\n\nВыведите таблицу «имя — возраст» тремя способами "
          "(%, .format(), f-строка) для одних и тех же данных, сравните длину кода.")
    nb.code('''name, age = "Ада", 28
print("%s — %d" % (name, age))
print("{} — {}".format(name, age))
print(f"{name} — {age}")''')
    nb.write(OUT_DIR / "08-06-formatirovanie.ipynb")
    print(f"Записано: 08-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-07 · Ввод от пользователя\n\nПрактика к разделам "
          "[«Получение ввода от пользователей»](../../site/chapters/glava-08/08-07-vvod-polzovatelya.html) "
          "и [«Мини-проект — текст Turtle»](../../site/chapters/glava-08/08-08-mini-proekt-turtle-tekst.html).")
    nb.md("## Цель\n\nОсвоить input() и преобразование введённого текста в числа.")
    md, code = input_setup(["Cartesian", "12", "25", "Cartesian"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''name = input("Как вас зовут? ")
print(f"Привет, {name}!")''')
    nb.md("## Эксперимент 1 — преобразование в число")
    nb.code('''age_text = input("Сколько вам лет? ")
age = int(age_text)
print(f"Через 5 лет вам будет {age + 5}.")''')
    nb.md("## Типичная ошибка\n\nБез `int()` строка и число не складываются.")
    nb.code('''age_text = input("Сколько вам лет? ")
age_text + 5''', raises=True)
    nb.md("## Исправление")
    nb.code('''age = int(age_text)
print(age + 5)''')
    nb.md("## Мини-проект — текст Turtle (без окна, только логика)\n\nВ настоящей программе "
          "эта строка попала бы на холст через `artist.write()` (глава 7) — здесь проверим "
          "только текстовую часть.")
    nb.code('''name = input("Как вас зовут? ")
message = f"Привет, {name}!"
print(message)''')
    nb.write(OUT_DIR / "08-07-vvod-polzovatelya.ipynb")
    print(f"Записано: 08-07 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-09 · Крик и переворот имени\n\nПрактика к разделу "
          "[«Мини-проекты: крик и переворот имени»](../../site/chapters/glava-08/08-09-mini-proekty-krik-perevorot.html).")
    nb.md("## Цель\n\nПрименить upper() и срез [::-1] в двух коротких мини-проектах.")
    md, code = input_setup(["python это круто", "Cartesian", "довод", "Python"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример — кричим на экран")
    nb.code('''phrase = input("Что вы хотите прокричать? ")
krik = phrase.upper() + "!!!"
print(krik)''')
    nb.md("## Рабочий пример — переворот имени")
    nb.code('''name = input("Как вас зовут? ")
perevernutoe = name[::-1]
print(f"Ваше имя задом наперёд: {perevernutoe}")''')
    nb.md("## Задание ★★ Самостоятельная задача — палиндром?")
    nb.code('''word = input("Введите слово: ")
is_palindrome = word.lower() == word.lower()[::-1]
print(f"«{word}» — палиндром: {is_palindrome}")''')
    nb.md("## Проверка результата")
    nb.code('''word = input("Введите слово: ")
print(word.lower() == word.lower()[::-1])''')
    nb.write(OUT_DIR / "08-09-krik-perevorot.ipynb")
    print(f"Записано: 08-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-10 · Мини-проект — динамическая математика\n\nПрактика к разделу "
          "[«Мини-проект — динамическая математика»](../../site/chapters/glava-08/08-10-mini-proekt-matematika-itogi.html).")
    nb.md("## Цель\n\nСобрать ввод, числа, f-строки в одном мини-калькуляторе (без окна Turtle "
          "— только логика вычислений и текста).")
    md, code = input_setup(["6", "7"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''a = float(input("Первое число: "))
b = float(input("Второе число: "))

print(f"{a} + {b} = {a + b}")
print(f"{a} * {b} = {a * b}")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте вычитание и деление к выводу.")
    md2, code2 = input_setup(["10", "4"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''a = float(input("Первое число: "))
b = float(input("Второе число: "))

print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")''')
    nb.write(OUT_DIR / "08-10-dinamicheskaya-matematika.ipynb")
    print(f"Записано: 08-10 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_03()
    build_04()
    build_06()
    build_07()
    build_09()
    build_10()
