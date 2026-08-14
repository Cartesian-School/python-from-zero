#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 14 (объекты и классы)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-14"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = '''import turtle

screen = turtle.Screen()
print("Окно Turtle готово.")'''
TEARDOWN_MD = "## Завершение (выполнить один раз, в самом конце)"
TEARDOWN_CODE = '''screen.bye()
print("Окно Turtle закрыто.")'''


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-01 · Что такое ООП?\n\nПрактика к разделу "
          "[«Что такое объектно-ориентированное программирование?»](../../site/chapters/glava-14/14-01-chto-takoe-oop.html).")
    nb.md("## Цель\n\nУзнать объекты в уже знакомом коде.")
    nb.md("## Рабочий пример")
    nb.code('''text = "Python"
print(type(text))          # str — это класс
print(text.upper())        # upper() — метод этого объекта''')
    nb.md("## Эксперимент 1\n\nПроверьте класс нескольких уже знакомых объектов.")
    nb.code('''for value in [42, 3.14, "текст", [1, 2, 3], {"a": 1}]:
    print(value, "->", type(value))''')
    nb.md("## Задание ★ Базовая практика\n\nНайдите три метода у списка (глава 11) и объясните "
          "своими словами, что каждый из них делает.")
    nb.code('''numbers = [3, 1, 2]
numbers.append(4)   # добавляет элемент
numbers.sort()       # сортирует список
numbers.reverse()    # разворачивает список
print(numbers)''')
    nb.write(OUT_DIR / "14-01-chto-takoe-oop.ipynb")
    print(f"Записано: 14-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-02 · Классы\n\nПрактика к разделу "
          "[«Классы»](../../site/chapters/glava-14/14-02-klassy.html).")
    nb.md("## Цель\n\nОпределить собственный класс и создать несколько объектов.")
    nb.md("## Рабочий пример")
    nb.code('''class Sobaka:
    def __init__(self, klichka, vozrast):
        self.klichka = klichka
        self.vozrast = vozrast

rex = Sobaka("Рекс", 3)
print(rex.klichka, rex.vozrast)''')
    nb.md("## Эксперимент 1 — независимые объекты")
    nb.code('''rex = Sobaka("Рекс", 3)
sharik = Sobaka("Шарик", 5)

print(rex.klichka, rex.vozrast)
print(sharik.klichka, sharik.vozrast)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте класс `Kniga` с атрибутами `nazvanie` и "
          "`avtor`, затем создайте три объекта.")
    nb.code('''class Kniga:
    def __init__(self, nazvanie, avtor):
        self.nazvanie = nazvanie
        self.avtor = avtor

knigi = [
    Kniga("Война и мир", "Толстой"),
    Kniga("Мастер и Маргарита", "Булгаков"),
    Kniga("Преступление и наказание", "Достоевский"),
]

for k in knigi:
    print(f"{k.nazvanie} — {k.avtor}")''')
    nb.write(OUT_DIR / "14-02-klassy.ipynb")
    print(f"Записано: 14-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-03 · Методы\n\nПрактика к разделу "
          "[«Управляем объектами. Объекты выполняют действия»](../../site/chapters/glava-14/14-03-upravlyaem-obektami.html).")
    nb.md("## Цель\n\nИзменять атрибуты и определять методы.")
    nb.md("## Рабочий пример")
    nb.code('''class Sobaka:
    def __init__(self, klichka, vozrast):
        self.klichka = klichka
        self.vozrast = vozrast

    def layat(self):
        print(f"{self.klichka} говорит: Гав-гав!")

    def prazdnovat_den_rozhdeniya(self):
        self.vozrast += 1
        print(f"Теперь {self.klichka} исполнилось {self.vozrast}!")

rex = Sobaka("Рекс", 3)
rex.layat()
rex.prazdnovat_den_rozhdeniya()''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте классу `Kniga` метод `opisanie()`, "
          "возвращающий строку вида «Название — Автор».")
    nb.code('''class Kniga:
    def __init__(self, nazvanie, avtor):
        self.nazvanie = nazvanie
        self.avtor = avtor

    def opisanie(self):
        return f"{self.nazvanie} — {self.avtor}"

k = Kniga("Война и мир", "Толстой")
print(k.opisanie())''')
    nb.md("## Дополнительная задача ★★★\n\nДобавьте класс `Biblioteka`, который хранит список "
          "книг и умеет добавлять новую книгу методом `dobavit_knigu()`.")
    nb.code('''class Biblioteka:
    def __init__(self):
        self.knigi = []

    def dobavit_knigu(self, kniga):
        self.knigi.append(kniga)

    def pokazat_vse(self):
        for k in self.knigi:
            print(k.opisanie())

biblioteka = Biblioteka()
biblioteka.dobavit_knigu(Kniga("Война и мир", "Толстой"))
biblioteka.dobavit_knigu(Kniga("Мастер и Маргарита", "Булгаков"))
biblioteka.pokazat_vse()''')
    nb.write(OUT_DIR / "14-03-metody.ipynb")
    print(f"Записано: 14-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-04 · Гонка Turtle с объектами\n\nПрактика к разделу "
          "[«Гонка Turtle с объектами»](../../site/chapters/glava-14/14-04-gonka-turtle-obekty-itogi.html).")
    nb.md("## Цель\n\nОбернуть гонку черепашек в собственный класс.")
    nb.md("""\
## О случайности в этом ноутбуке

Гонка использует `random.randint()` — для предсказуемого результата в автоматическом
выполнении здесь закрепляем случайность через `random.seed()`.""")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''import random

random.seed(5)
screen.setup(500, 400)

class Uchastnik:
    def __init__(self, cvet, startovyj_y):
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.t.color(cvet)
        self.t.penup()
        self.t.goto(-200, startovyj_y)
        self.cvet = cvet

    def sdelat_shag(self):
        self.t.forward(random.randint(1, 10))

    def finishiroval(self, finish_line):
        return self.t.xcor() >= finish_line

cveta = ["red", "blue", "green", "orange"]
uchastniki = [Uchastnik(cvet, i * 40 - 60) for i, cvet in enumerate(cveta)]

pobeditel = None
while pobeditel is None:
    for u in uchastniki:
        u.sdelat_shag()
        if u.finishiroval(200):
            pobeditel = u.cvet
            break

print(f"Победил участник цвета {pobeditel}!")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "14-04-gonka-obekty.ipynb")
    print(f"Записано: 14-04 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
