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


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-11 · Экранирование\n\nПрактика к разделу "
          "[«Экранирование: \\n, \\t и другие»](../../site/chapters/glava-08/08-11-ekranirovanie.html).")
    nb.md("## Цель\n\nОсвоить служебные последовательности \\n, \\t и экранирование кавычек, "
          "научиться пользоваться repr() для отладки.")
    nb.md("## Рабочий пример")
    nb.code('''print("Первая строка\\nВторая строка")
print("Имя:\\tВозраст:")''')
    nb.md("## Эксперимент 1 — repr() показывает служебные символы «как в коде»")
    nb.code('''text = "a\\tb\\nc"
print(text)
print(repr(text))''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте строку `quote` с экранированной двойной "
          "кавычкой внутри — «Он сказал: \\\"привет\\\"» — и строку `two_lines` из двух строк "
          "текста, разделённых `\\n`.")
    nb.code('''quote = "Он сказал: \\"привет\\""
two_lines = "Первая\\nВторая"
print(quote)
print(two_lines)''')
    nb.write(OUT_DIR / "08-11-ekranirovanie.ipynb")
    print(f"Записано: 08-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-12 · Многострочные и raw-строки\n\nПрактика к разделу "
          "[«Многострочные и raw-строки»](../../site/chapters/glava-08/08-12-mnogostrochnye-i-raw-stroki.html).")
    nb.md("## Цель\n\nОсвоить тройные кавычки для многострочного текста и raw-строки r\"...\".")
    nb.md("## Рабочий пример")
    nb.code('''poem = """Код за кодом,
шаг за шагом —
так рождается
программа."""
print(poem)''')
    nb.md("## Эксперимент 1 — raw-строка против обычной")
    nb.code('''bez_raw = "C:\\\\Users\\\\Cartesian"
s_raw = r"C:\\Users\\Cartesian"
print(bez_raw)
print(s_raw)
print(bez_raw == s_raw)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте `multiline` — строку из трёх строк текста "
          "через тройные кавычки — и `raw_path` — строку `D:\\Data\\file.txt` через raw-строку.")
    nb.code('''multiline = """Первая
Вторая
Третья"""
raw_path = r"D:\\Data\\file.txt"
print(multiline)
print(raw_path)''')
    nb.write(OUT_DIR / "08-12-mnogostrochnye-i-raw-stroki.ipynb")
    print(f"Записано: 08-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-13 · Длина строки: len()\n\nПрактика к разделу "
          "[«Длина строки: len()»](../../site/chapters/glava-08/08-13-dlina-stroki.html).")
    nb.md("## Цель\n\nСчитать символы строки функцией len() и понимать связь длины с индексами.")
    nb.md("## Рабочий пример")
    nb.code('''word = "Python"
print(len(word))

phrase = "Python с нуля"
print(len(phrase))''')
    nb.md("## Задание ★ Базовая практика\n\nДля слова «Cartesian» найдите его длину `dlina` и "
          "индекс последнего символа `posledniy_index` (через len()) — затем убедитесь, что "
          "`word[posledniy_index]` совпадает с `word[-1]`.")
    nb.code('''word = "Cartesian"
dlina = len(word)
posledniy_index = dlina - 1
print(dlina, posledniy_index)
print(word[posledniy_index] == word[-1])''')
    nb.write(OUT_DIR / "08-13-dlina-stroki.ipynb")
    print(f"Записано: 08-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-14 · Срезы строки\n\nПрактика к разделам "
          "[«Срезы строки»](../../site/chapters/glava-08/08-14-srezy-stroki.html) и "
          "[«Строки нельзя изменить»](../../site/chapters/glava-08/08-15-neizmenyaemost.html).")
    nb.md("## Цель\n\nОсвоить срезы [start:stop:step] и убедиться, что строки неизменяемы.")
    nb.md("## Рабочий пример")
    nb.code('''word = "Cartesian"
print(word[0:3])
print(word[-3:])
print(word[::-1])''')
    nb.md("## Типичная ошибка — строку нельзя изменить «на месте»")
    nb.code('''word = "Cat"
word[0] = "B"''', raises=True)
    nb.md("## Исправление")
    nb.code('''word = "Cat"
word = "B" + word[1:]
print(word)''')
    nb.md("## Задание ★ Базовая практика\n\nДля слова «Cartesian» получите срезами: первые три "
          "символа `first3`, последние три `last3`, каждый второй символ `every_second` и слово "
          "задом наперёд `reversed_word`.")
    nb.code('''word = "Cartesian"
first3 = word[:3]
last3 = word[-3:]
every_second = word[::2]
reversed_word = word[::-1]
print(first3, last3, every_second, reversed_word)''')
    nb.write(OUT_DIR / "08-14-srezy-stroki.ipynb")
    print(f"Записано: 08-14 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-16 · Методы строк: поиск и разбор\n\nПрактика к разделу "
          "[«Методы строк: поиск и разбор»](../../site/chapters/glava-08/08-16-metody-strok-poisk-i-razbor.html).")
    nb.md("## Цель\n\nОсвоить replace, split, join, count, find, index, startswith, endswith.")
    nb.md("## Рабочий пример")
    nb.code('''text = "я люблю Java"
print(text.replace("Java", "Python"))

sentence = "кот и пёс"
words = sentence.split()
print(words)
print("-".join(words))''')
    nb.md("## Эксперимент 1 — find() и index()")
    nb.code('''text = "Python"
print(text.find("th"))
print(text.find("zz"))''')
    nb.md("## Задание ★ Базовая практика\n\nДля имени файла «report_final.pdf» проверьте, "
          "заканчивается ли оно на «.pdf» (`is_pdf`), найдите позицию символа «_» (`position`), "
          "и разбейте имя по «_» на список частей (`parts`).")
    nb.code('''filename = "report_final.pdf"
is_pdf = filename.endswith(".pdf")
position = filename.find("_")
parts = filename.split("_")
print(is_pdf, position, parts)''')
    nb.write(OUT_DIR / "08-16-metody-strok-poisk-i-razbor.ipynb")
    print(f"Записано: 08-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-17 · Методы проверки строки\n\nПрактика к разделу "
          "[«Методы проверки: isalpha и другие»](../../site/chapters/glava-08/08-17-metody-proverki.html).")
    nb.md("## Цель\n\nОсвоить isalpha, isdigit, isalnum, isspace для проверки состава строки.")
    nb.md("## Рабочий пример")
    nb.code('''print("Python".isalpha())
print("2026".isdigit())
print("Python3".isalnum())
print("   ".isspace())''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте три строки: `s1 = \"Python\"` методом "
          "isalpha() → `r1`, `s2 = \"2026\"` методом isdigit() → `r2`, `s3 = \"   \"` методом "
          "isspace() → `r3`.")
    nb.code('''s1 = "Python"
s2 = "2026"
s3 = "   "
r1 = s1.isalpha()
r2 = s2.isdigit()
r3 = s3.isspace()
print(r1, r2, r3)''')
    nb.write(OUT_DIR / "08-17-metody-proverki.ipynb")
    print(f"Записано: 08-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-18 · Перебор строки в цикле\n\nПрактика к разделу "
          "[«Перебираем строку в цикле»](../../site/chapters/glava-08/08-18-cikl-po-stroke.html).")
    nb.md("## Цель\n\nПройтись по строке циклом for и посчитать вхождения символа вручную.")
    nb.md("## Рабочий пример")
    nb.code('''word = "Python"
for ch in word:
    print(ch)''')
    nb.md("## Задание ★ Базовая практика\n\nВ строке «миссисипи» посчитайте в цикле for, "
          "сколько раз встречается буква «и» — сохраните результат в `count`.")
    nb.code('''text = "миссисипи"
bukva = "и"
count = 0
for ch in text:
    if ch == bukva:
        count += 1
print(count)''')
    nb.write(OUT_DIR / "08-18-cikl-po-stroke.ipynb")
    print(f"Записано: 08-18 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-20 · Отладка проблем со строками\n\nПрактика к разделу "
          "[«Отладка проблем со строками»](../../site/chapters/glava-08/08-20-otladka-strok.html).")
    nb.md("## Цель\n\nНаучиться находить невидимые пробелы и другие частые ошибки строк.")
    nb.md("## Рабочий пример")
    nb.code('''password = "секрет "
print(password == "секрет")
print(repr(password))''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте `password = \"секрет \"` (с пробелом в "
          "конце): сравните его с `\"секрет\"` в `is_equal_before`, затем очистите через "
          "strip() в `cleaned` и сравните снова в `is_equal_after`.")
    nb.code('''password = "секрет "
is_equal_before = password == "секрет"
cleaned = password.strip()
is_equal_after = cleaned == "секрет"
print(is_equal_before, is_equal_after)''')
    nb.write(OUT_DIR / "08-20-otladka-strok.ipynb")
    print(f"Записано: 08-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-21 · Приветствие и форматирование ФИО\n\nПрактика к разделу "
          "[«Мини-проект: приветствие и ФИО»](../../site/chapters/glava-08/08-21-mini-proekt-privetstvie-i-imya.html).")
    nb.md("## Цель\n\nСобрать strip(), capitalize() и f-строки в форматировщике ФИО.")
    md, code = input_setup(["  ада  ", "ЛАВЛЕЙС"])
    nb.md(md)
    nb.code(code)
    nb.md("## Задание ★ Базовая практика\n\nСпросите имя и фамилию через input(), приведите "
          "каждое к аккуратному виду (strip + capitalize) и соберите `full_name` и `initials`.")
    nb.code('''raw_first = input("Имя: ")
raw_last = input("Фамилия: ")

first = raw_first.strip().capitalize()
last = raw_last.strip().capitalize()
full_name = f"{first} {last}"
initials = f"{first[0]}. {last[0]}."

print(full_name)
print(initials)''')
    nb.write(OUT_DIR / "08-21-mini-proekt-privetstvie-i-imya.ipynb")
    print(f"Записано: 08-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-22 · Проверка пароля и e-mail\n\nПрактика к разделу "
          "[«Мини-проект: пароль и e-mail»](../../site/chapters/glava-08/08-22-mini-proekt-parol-i-email.html).")
    nb.md("## Цель\n\nСобрать методы проверки строк (isdigit, isalpha, in) в простой валидации ввода.")
    nb.md("## Рабочий пример")
    nb.code('''password = "abc12345"
print(len(password) >= 8)
print(any(ch.isdigit() for ch in password))''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте `password = \"abc12345\"` по трём "
          "правилам (длина от 8, есть цифра, есть буква) — итог в `nadyozhnyj`. Проверьте "
          "`email = \"ada@cartesianschool.org\"` — есть ровно один «@» — итог в "
          "`pohozhe_na_email`.")
    nb.code('''password = "abc12345"
dostatochno_dlinnyj = len(password) >= 8
est_cifra = any(ch.isdigit() for ch in password)
est_bukva = any(ch.isalpha() for ch in password)
nadyozhnyj = dostatochno_dlinnyj and est_cifra and est_bukva

email = "ada@cartesianschool.org"
est_sobachka = "@" in email
odna_sobachka = email.count("@") == 1
pohozhe_na_email = est_sobachka and odna_sobachka

print(nadyozhnyj, pohozhe_na_email)''')
    nb.write(OUT_DIR / "08-22-mini-proekt-parol-i-email.ipynb")
    print(f"Записано: 08-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 08-23 · Счётчик слов\n\nПрактика к разделу "
          "[«Мини-проект: счётчик слов»](../../site/chapters/glava-08/08-23-mini-proekt-schetchik-slov.html).")
    nb.md("## Цель\n\nСобрать split() и подсчёт в словаре для анализа текста.")
    nb.md("## Рабочий пример")
    nb.code('''text = "кот и пёс и кот"
words = text.lower().split()
print(words)
print(len(words))''')
    nb.md("## Задание ★ Базовая практика\n\nДля `text = \"кот и пёс и кот\"` разбейте на слова "
          "(`words`), посчитайте их количество (`total`), и через словарь `schetchik` "
          "посчитайте, сколько раз встречается каждое слово.")
    nb.code('''text = "кот и пёс и кот"
words = text.lower().split()
total = len(words)

schetchik = {}
for word in words:
    schetchik[word] = schetchik.get(word, 0) + 1

print(total)
print(schetchik)''')
    nb.write(OUT_DIR / "08-23-mini-proekt-schetchik-slov.ipynb")
    print(f"Записано: 08-23 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_03()
    build_04()
    build_06()
    build_07()
    build_09()
    build_10()
    build_11()
    build_12()
    build_13()
    build_14()
    build_16()
    build_17()
    build_18()
    build_20()
    build_21()
    build_22()
    build_23()
