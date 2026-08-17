#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 12 (мини-проекты)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-12"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = '''import turtle

screen = turtle.Screen()
artist = turtle.Turtle()
artist.speed(0)
print("Окно Turtle готово.")'''
TEARDOWN_MD = "## Завершение (выполнить один раз, в самом конце)"
TEARDOWN_CODE = '''screen.bye()
print("Окно Turtle закрыто.")'''


def input_setup(answers: list[str]) -> tuple[str, str]:
    md = ("## Про input() в этом ноутбуке\n\nЭтот ноутбук выполняется автоматически, поэтому "
          "`input()` временно подменён на заранее заготовленные ответы.")
    answers_repr = ", ".join(repr(a) for a in answers)
    code = f"""_answers = iter([{answers_repr}])

def input(prompt=""):
    answer = next(_answers)
    print(prompt + answer)
    return answer"""
    return md, code


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-01 · Чётное или нечётное\n\nПрактика к разделу "
          "[«Проект 12-1»](../../site/chapters/glava-12/12-01-chetnoe-ili-nechetnoe.html).")
    nb.md("## Цель\n\nЗакрепить условия и оператор %.")
    md, code = input_setup(["17"])
    nb.md(md)
    nb.code(code)
    nb.md("## Часть 1 — одно число")
    nb.code('''number = int(input("Введите число: "))
if number % 2 == 0:
    print(f"{number} — чётное.")
else:
    print(f"{number} — нечётное.")''')
    nb.md("## Часть 2 — диапазон")
    md2, code2 = input_setup(["1", "20"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''nachalo = int(input("Начало диапазона: "))
konec = int(input("Конец диапазона: "))

chetnye = [n for n in range(nachalo, konec + 1) if n % 2 == 0]
print("Чётные числа:", chetnye)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nВыведите нечётные числа из того же "
          "диапазона.")
    nb.code('''nachalo, konec = 1, 20
nechetnye = [n for n in range(nachalo, konec + 1) if n % 2 != 0]
print("Нечётные числа:", nechetnye)''')
    nb.write(OUT_DIR / "12-01-chetnoe-nechetnoe.ipynb")
    print(f"Записано: 12-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-02 · Достаточно ли чаевых?\n\nПрактика к разделу "
          "[«Проект 12-2»](../../site/chapters/glava-12/12-02-chaevye.html).")
    nb.md("## Цель\n\nЗакрепить арифметику, форматирование и elif.")
    md, code = input_setup(["1000", "150"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''schet = float(input("Сумма счёта: "))
chaevye = float(input("Сумма чаевых: "))

procent = (chaevye / schet) * 100

if procent < 15:
    print(f"Маловато — всего {procent:.1f}%. Обычно оставляют 15-20%.")
elif procent <= 20:
    print(f"В самый раз — {procent:.1f}%!")
else:
    print(f"Очень щедро — целых {procent:.1f}%!")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте категорию «сказочно щедро» для "
          "чаевых больше 30%.")
    md2, code2 = input_setup(["1000", "350"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''schet = float(input("Сумма счёта: "))
chaevye = float(input("Сумма чаевых: "))
procent = (chaevye / schet) * 100

if procent < 15:
    print(f"Маловато — всего {procent:.1f}%.")
elif procent <= 20:
    print(f"В самый раз — {procent:.1f}%!")
elif procent <= 30:
    print(f"Очень щедро — целых {procent:.1f}%!")
else:
    print(f"Сказочно щедро — {procent:.1f}%!")''')
    nb.write(OUT_DIR / "12-02-chaevye.ipynb")
    print(f"Записано: 12-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-03 · Рождественская ёлка\n\nПрактика к разделу "
          "[«Проект 12-3»](../../site/chapters/glava-12/12-03-elka.html).")
    nb.md("## Цель\n\nНарисовать ёлку из уменьшающихся треугольных ярусов.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
artist.pencolor("green")
artist.fillcolor("green")

yarusy = 4
shirina = 120

artist.penup()
artist.goto(0, 100)
artist.pendown()

for yarus in range(yarusy):
    artist.begin_fill()
    artist.setheading(240)
    artist.forward(shirina)
    artist.setheading(0)
    artist.forward(shirina)
    artist.setheading(120)
    artist.forward(shirina)
    artist.end_fill()

    artist.penup()
    artist.setheading(270)
    artist.forward(30)
    artist.pendown()
    shirina -= 20

print("Ёлка из", yarusy, "ярусов готова.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nИзмените число ярусов на 6 и начальную "
          "ширину — на 150.")
    nb.code('''artist.reset()
artist.pencolor("green")
artist.fillcolor("green")

yarusy = 6
shirina = 150

artist.penup()
artist.goto(0, 130)
artist.pendown()

for yarus in range(yarusy):
    artist.begin_fill()
    artist.setheading(240)
    artist.forward(shirina)
    artist.setheading(0)
    artist.forward(shirina)
    artist.setheading(120)
    artist.forward(shirina)
    artist.end_fill()

    artist.penup()
    artist.setheading(270)
    artist.forward(25)
    artist.pendown()
    shirina -= 20

print("Ёлка из", yarusy, "ярусов готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-03-elka.ipynb")
    print(f"Записано: 12-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-04 · Спирали!\n\nПрактика к разделу "
          "[«Проект 12-4»](../../site/chapters/glava-12/12-04-spirali.html).")
    nb.md("## Цель\n\nНарисовать все пять вариантов спирали.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Квадратная спираль")
    nb.code('''artist.reset()
dlina = 5
for _ in range(60):
    artist.forward(dlina)
    artist.right(90)
    dlina += 3
print("Квадратная спираль готова.")''')
    nb.md("## Случайная спираль")
    nb.code('''import random

artist.reset()
dlina = 5
for _ in range(60):
    artist.forward(dlina)
    artist.right(random.randint(80, 100))
    dlina += 3
print("Случайная спираль готова.")''')
    nb.md("## Треугольная спираль")
    nb.code('''artist.reset()
dlina = 5
for _ in range(60):
    artist.forward(dlina)
    artist.right(120)
    dlina += 3
print("Треугольная спираль готова.")''')
    nb.md("## Звёздная спираль")
    nb.code('''artist.reset()
dlina = 5
for _ in range(100):
    artist.forward(dlina)
    artist.right(144)
    dlina += 2
print("Звёздная спираль готова.")''')
    nb.md("## Круговая спираль")
    nb.code('''artist.reset()
radius = 5
for _ in range(60):
    artist.circle(radius, 90)
    radius += 3
print("Круговая спираль готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-04-spirali.ipynb")
    print(f"Записано: 12-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-05 · Сложная мандала\n\nПрактика к разделу "
          "[«Проект 12-5»](../../site/chapters/glava-12/12-05-slozhnaya-mandala.html).")
    nb.md("## Цель\n\nПолностью автоматизированная мандала со случайными цветами.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''import random

artist.reset()
luchi = 36
shag_ugla = 360 / luchi
cveta = ["red", "orange", "purple", "blue", "green"]

for i in range(luchi):
    artist.pencolor(random.choice(cveta))
    artist.setheading(i * shag_ugla)
    artist.forward(150)
    artist.circle(20)
    artist.forward(-150)

print("Мандала готова, лучей:", luchi)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nИзмените `luchi` на 12 — реже расставленные "
          "лучи, но тот же принцип.")
    nb.code('''import random

artist.reset()
luchi = 12
shag_ugla = 360 / luchi
cveta = ["red", "orange", "purple", "blue", "green"]
for i in range(luchi):
    artist.pencolor(random.choice(cveta))
    artist.setheading(i * shag_ugla)
    artist.forward(150)
    artist.circle(20)
    artist.forward(-150)
print(f"luchi={luchi}: готово")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-05-slozhnaya-mandala.ipynb")
    print(f"Записано: 12-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-06 · Гонка Turtle\n\nПрактика к разделу "
          "[«Проект 12-6»](../../site/chapters/glava-12/12-06-gonka-turtle-itogi.html).")
    nb.md("## Цель\n\nНесколько черепашек на одном экране одновременно.")
    nb.md("""\
## О случайности в этом ноутбуке

Гонка использует `random.randint()` для шага каждой черепашки — результат может отличаться
при каждом запуске. Чтобы ноутбук выполнялся предсказуемо, здесь дополнительно закрепляем
случайность через `random.seed()`.""")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''import random

random.seed(3)
screen.setup(500, 400)

cveta = ["red", "blue", "green", "orange"]
uchastniki = []

for i, cvet in enumerate(cveta):
    t = turtle.Turtle()
    t.shape("turtle")
    t.color(cvet)
    t.penup()
    t.goto(-200, i * 40 - 60)
    uchastniki.append(t)

finish_line = 200
pobeditel = None

while pobeditel is None:
    for t in uchastniki:
        t.forward(random.randint(1, 10))
        if t.xcor() >= finish_line:
            pobeditel = t.pencolor()
            break

print(f"Победила черепашка цвета {pobeditel}!")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-06-gonka-turtle.ipynb")
    print(f"Записано: 12-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-07 · Статистика трёх чисел\n\nПрактика к разделу "
          "[«Что такое проект»](../../site/chapters/glava-12/12-07-chto-takoe-proekt.html).")
    nb.md("## Цель\n\nОт задачи до кода на маленькой программе: список, min/max/sum/среднее.")
    md, code = input_setup(["10", "20", "30"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''a = float(input("Первое число: "))
b = float(input("Второе число: "))
c = float(input("Третье число: "))

chisla = [a, b, c]
minimum = min(chisla)
maksimum = max(chisla)
summa = sum(chisla)
average = summa / len(chisla)

print(f"Минимум: {minimum}")
print(f"Максимум: {maksimum}")
print(f"Сумма: {summa}")
print(f"Среднее: {average:.2f}")''')
    nb.write(OUT_DIR / "12-07-statistika-treh-chisel.ipynb")
    print(f"Записано: 12-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-08 · Debug Lab — счётчик\n\nПрактика к разделу "
          "[«Строим проект по шагам»](../../site/chapters/glava-12/12-08-stroim-proekt-po-shagam.html).")
    nb.md("## Цель\n\nНайти и исправить ошибку: счётчик обнуляется внутри цикла.")
    nb.md("""\
## Сломанный код (не выполняем)

```python
for correct, given in zip(answers, user_answers):
    score = 0
    if given == correct:
        score += 1
```

`score = 0` стоит ВНУТРИ цикла — счётчик никогда не накапливается.""")
    nb.md("## Задание ★ Базовая практика — исправленная версия")
    nb.code('''answers = ["python", "git", "sql"]
user_answers = ["python", "python", "sql"]

score = 0
for correct, given in zip(answers, user_answers):
    if given == correct:
        score += 1

print("Итоговый счёт:", score)''')
    nb.write(OUT_DIR / "12-08-debug-lab-schet.ipynb")
    print(f"Записано: 12-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-09 · Угадай число, версия 3\n\nПрактика к разделу "
          "[«Проект: угадай число, версия 3»](../../site/chapters/glava-12/12-09-ugadaj-chislo-v3.html).")
    nb.md("## Цель\n\nПолная игра-угадайка: while, if/elif/else, счётчик попыток.")
    nb.md("## О случайности в этом ноутбуке\n\nЗдесь секретное число зафиксировано "
          "(`secret = 37`), а не выбрано случайно — иначе автоматическая проверка результата "
          "была бы недетерминированной.")
    md, code = input_setup(["50", "25", "37"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''secret = 37
attempts = 0
guess = None

while guess != secret:
    guess = int(input("Ваша попытка: "))
    attempts += 1
    if guess < secret:
        print("Слишком мало!")
    elif guess > secret:
        print("Слишком много!")
    else:
        print(f"Поздравляем! Загадано было {secret}. Попыток: {attempts}")''')
    nb.write(OUT_DIR / "12-09-ugadaj-chislo-v3.ipynb")
    print(f"Записано: 12-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-10 · Угадай число — ограничение попыток\n\nПрактика к разделу "
          "[«Проект: угадай число, версия 3»](../../site/chapters/glava-12/12-09-ugadaj-chislo-v3.html#uroven-3).")
    nb.md("## Цель\n\nУровень 3: игра заканчивается поражением после ограниченного числа "
          "попыток.")
    md, code = input_setup(["50", "25", "37"])
    nb.md(md)
    nb.code(code)
    nb.md("## Задание ★★★ Задача повышенной сложности")
    nb.code('''secret = 37
max_attempts = 5
attempts = 0
guess = None

while guess != secret and attempts < max_attempts:
    guess = int(input("Ваша попытка: "))
    attempts += 1
    if guess < secret:
        print("Слишком мало!")
    elif guess > secret:
        print("Слишком много!")

if guess == secret:
    print(f"Победа за {attempts} попыток!")
    pobeda = True
else:
    print(f"Числа закончились. Было загадано {secret}.")
    pobeda = False''')
    nb.write(OUT_DIR / "12-10-ugadaj-chislo-limit.ipynb")
    print(f"Записано: 12-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-11 · Анализатор текста\n\nПрактика к разделу "
          "[«Проект: анализатор текста и частота слов»](../../site/chapters/glava-12/12-11-analizator-teksta.html).")
    nb.md("## Цель\n\nСимволы, слова, уникальные слова — строки, циклы и множества вместе.")
    md, code = input_setup(["Python is great and python is fun"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''text = input("Введите текст: ")
normalized = text.lower().split()
unikalnye = set(normalized)

kolichestvo_simvolov = len(text)
kolichestvo_slov = len(normalized)
kolichestvo_unikalnyh = len(unikalnye)

print("Символов:", kolichestvo_simvolov)
print("Слов:", kolichestvo_slov)
print("Уникальных слов:", kolichestvo_unikalnyh)''')
    nb.write(OUT_DIR / "12-11-analizator-teksta.ipynb")
    print(f"Записано: 12-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-12 · Частота слов\n\nПрактика к разделу "
          "[«Проект: анализатор текста и частота слов»](../../site/chapters/glava-12/12-11-analizator-teksta.html#etap-3).")
    nb.md("## Цель\n\nПодсчёт частоты слов и поиск самого частого слова через max(key=...).")
    md, code = input_setup(["Python is great and python is fun"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''text = input("Введите текст: ")
normalized = text.lower().split()

counts = {}
for word in normalized:
    counts[word] = counts.get(word, 0) + 1

samoe_chastoe = max(counts, key=counts.get)

print(counts)
print("Самое частое слово:", samoe_chastoe, "—", counts[samoe_chastoe], "раз(а)")''')
    nb.write(OUT_DIR / "12-12-chastota-slov-proekt.ipynb")
    print(f"Записано: 12-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-13 · Записная книжка\n\nПрактика к разделу "
          "[«Проект: записная книжка»](../../site/chapters/glava-12/12-13-zapisnaya-knizhka.html).")
    nb.md("## Цель\n\nDict как контактная книга: добавить, изменить, удалить.")
    nb.md("## Рабочий пример")
    nb.code('''contacts = {
    "Anna": "+48 111 111 111",
    "Bob": "+48 222 222 222",
}

contacts["Maria"] = "+48 333 333 333"
contacts["Anna"] = "+48 111 000 000"
del contacts["Bob"]

kolichestvo = len(contacts)
print(contacts)
print("Контактов:", kolichestvo)''')
    nb.write(OUT_DIR / "12-13-zapisnaya-knizhka.ipynb")
    print(f"Записано: 12-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-14 · Журнал оценок\n\nПрактика к разделу "
          "[«Проекты: журнал оценок и корзина покупок»](../../site/chapters/glava-12/12-14-zhurnal-i-korzina.html#zhurnal-ocenok).")
    nb.md("## Цель\n\nСписок словарей + накопитель: среднее, максимум, минимум, отличники.")
    nb.md("## Рабочий пример")
    nb.code('''students = [
    {"name": "Anna", "score": 95},
    {"name": "Bob", "score": 82},
    {"name": "Maria", "score": 91},
    {"name": "Leo", "score": 58},
]

scores = [student["score"] for student in students]
average = sum(scores) / len(scores)
maksimum = max(scores)
minimum = min(scores)
otlichniki = [s for s in students if s["score"] >= 90]

print(f"Средний балл: {average:.1f}")
print("Максимум:", maksimum)
print("Минимум:", minimum)
print("Отличников:", len(otlichniki))''')
    nb.write(OUT_DIR / "12-14-zhurnal-ocenok.ipynb")
    print(f"Записано: 12-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-15 · Корзина покупок\n\nПрактика к разделу "
          "[«Проекты: журнал оценок и корзина покупок»](../../site/chapters/glava-12/12-14-zhurnal-i-korzina.html#korzina-pokupok).")
    nb.md("## Цель\n\nСписок словарей + накопитель: чек и итоговая сумма.")
    nb.md("## Рабочий пример")
    nb.code('''cart = [
    {"name": "Молоко", "price": 4.50, "qty": 2},
    {"name": "Хлеб", "price": 2.20, "qty": 1},
    {"name": "Сыр", "price": 9.90, "qty": 1},
]

total = 0
for item in cart:
    line_total = item["price"] * item["qty"]
    total += line_total
    print(f"{item['name']:<10} {item['qty']} x {item['price']:.2f} = {line_total:.2f}")

total = round(total, 2)
print(f"Итого: {total:.2f}")''')
    nb.write(OUT_DIR / "12-15-korzina-pokupok.ipynb")
    print(f"Записано: 12-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-16 · Викторина\n\nПрактика к разделу "
          "[«Проект: викторина»](../../site/chapters/glava-12/12-16-viktorina.html).")
    nb.md("## Цель\n\nДанные (список вопросов) + один алгоритм (цикл), а не захардкоженная "
          "логика.")
    md, code = input_setup(["paris", "56", "python"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''questions = [
    {"question": "Столица Франции?", "answer": "paris"},
    {"question": "7 * 8?", "answer": "56"},
    {"question": "Язык, который мы изучаем?", "answer": "python"},
]

score = 0
for q in questions:
    user_answer = input(q["question"] + " ").strip().lower()
    if user_answer == q["answer"]:
        print("✅ Верно!")
        score += 1
    else:
        print(f"❌ Неверно. Правильный ответ: {q['answer']}")

print(f"Счёт: {score} из {len(questions)}")''')
    nb.write(OUT_DIR / "12-16-viktorina.ipynb")
    print(f"Записано: 12-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-17 · Викторина — процент правильных ответов\n\nПрактика к разделу "
          "[«Проект: викторина»](../../site/chapters/glava-12/12-16-viktorina.html#uroven-4).")
    nb.md("## Цель\n\nУровень 4: посчитать долю правильных ответов в процентах.")
    md, code = input_setup(["paris", "54", "python"])
    nb.md(md)
    nb.code(code)
    nb.md("## Задание ★★★★ Challenge")
    nb.code('''questions = [
    {"question": "Столица Франции?", "answer": "paris"},
    {"question": "7 * 8?", "answer": "56"},
    {"question": "Язык, который мы изучаем?", "answer": "python"},
]

score = 0
for q in questions:
    user_answer = input(q["question"] + " ").strip().lower()
    if user_answer == q["answer"]:
        score += 1

procent = score / len(questions) * 100
print(f"Результат: {procent:.0f}%")''')
    nb.write(OUT_DIR / "12-17-viktorina-procent.ipynb")
    print(f"Записано: 12-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-18 · Консоль команд\n\nПрактика к разделу "
          "[«Проекты: консоль команд и проверка пароля»](../../site/chapters/glava-12/12-18-konsol-i-validator.html#konsol-komand).")
    nb.md("## Цель\n\nwhile True + if/elif/else + break — паттерн, который встречается в "
          "меню, консолях и ботах.")
    md, code = input_setup(["help", "hello", "status", "exit"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''history = []

while True:
    command = input("> ").strip().lower()
    history.append(command)

    if command == "exit":
        print("До встречи!")
        break
    elif command == "help":
        print("Команды: help, hello, status, exit")
    elif command == "hello":
        print("Привет!")
    elif command == "status":
        print(f"Команд выполнено: {len(history)}")
    else:
        print(f"Неизвестная команда: {command}")

print(history)''')
    nb.write(OUT_DIR / "12-18-konsol-komand.ipynb")
    print(f"Записано: 12-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-19 · Проверка пароля\n\nПрактика к разделу "
          "[«Проекты: консоль команд и проверка пароля»](../../site/chapters/glava-12/12-18-konsol-i-validator.html#validator-parolya).")
    nb.md("## Цель\n\nНакопление состояния через булевы флаги при переборе строки посимвольно.")
    nb.md("""\
## Это учебное упражнение по строкам

Не полноценная политика безопасности паролей — тренировка работы со строками и булевыми
флагами.""")
    md, code = input_setup(["Python3Code"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''password = input("Придумайте пароль: ")

has_digit = False
has_letter = False
has_space = False

for ch in password:
    if ch.isdigit():
        has_digit = True
    elif ch.isalpha():
        has_letter = True
    elif ch == " ":
        has_space = True

dlinnyj_dostatochno = len(password) >= 8
podhodit = dlinnyj_dostatochno and has_digit and has_letter and not has_space

print("Подходит:", podhodit)''')
    nb.write(OUT_DIR / "12-19-validator-parolya.ipynb")
    print(f"Записано: 12-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-20 · Угол многоугольника\n\nПрактика к разделу "
          "[«Проект: студия многоугольников»](../../site/chapters/glava-12/12-20-studiya-mnogougolnikov.html).")
    nb.md("## Цель\n\nЧистая геометрия без Turtle: одна формула для любого числа сторон.")
    nb.md("## Рабочий пример")
    nb.code('''storony_1 = 5
ugol_1 = 360 / storony_1

storony_2 = 8
ugol_2 = 360 / storony_2

print(f"{storony_1} сторон → угол {ugol_1}°")
print(f"{storony_2} сторон → угол {ugol_2}°")''')
    nb.write(OUT_DIR / "12-20-ugol-mnogougolnika.ipynb")
    print(f"Записано: 12-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-21 · Студия многоугольников (Turtle)\n\nПрактика к разделу "
          "[«Проект: студия многоугольников»](../../site/chapters/glava-12/12-20-studiya-mnogougolnikov.html).")
    nb.md("## Цель\n\nНарисовать многоугольник по числу сторон, используя ту же формулу.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
storony = 6
dlina = 300 / storony
ugol = 360 / storony

for _ in range(storony):
    artist.forward(dlina)
    artist.right(ugol)

print("Многоугольник с", storony, "сторонами готов.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-21-studiya-mnogougolnikov.ipynb")
    print(f"Записано: 12-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-22 · Пиксельная графика по сетке\n\nПрактика к разделу "
          "[«Проект: пиксельная графика по сетке»](../../site/chapters/glava-12/12-22-setka-piksel-art.html).")
    nb.md("## Цель\n\nВложенный список + вложенный цикл рисуют картинку по матрице 0/1.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
artist.penup()

picture = [
    [0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
]

razmer = 40
for row_index, row in enumerate(picture):
    for col_index, value in enumerate(row):
        if value == 1:
            x = -100 + col_index * razmer
            y = 100 - row_index * razmer
            artist.goto(x, y)
            artist.pendown()
            artist.fillcolor("#DB2777")
            artist.begin_fill()
            for _ in range(4):
                artist.forward(razmer)
                artist.right(90)
            artist.end_fill()
            artist.penup()

print("Готово.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-22-setka-piksel-art.ipynb")
    print(f"Записано: 12-22 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_07()
    build_08()
    build_01()
    build_02()
    build_09()
    build_10()
    build_11()
    build_12()
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_03()
    build_04()
    build_05()
    build_22()
    build_06()
