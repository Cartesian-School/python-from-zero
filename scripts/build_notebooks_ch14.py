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


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-05 · self и связывание методов\n\nПрактика к разделу "
          "[«self и связывание методов»](../../site/chapters/glava-14/14-05-self-i-svyazyvanie-metodov.html).")
    nb.md("## Цель\n\nУвидеть, что obj.method() и Class.method(obj) — один и тот же вызов.")
    nb.md("## Рабочий пример")
    nb.code('''class Sobaka:
    def __init__(self, klichka):
        self.klichka = klichka

    def layat(self):
        return f"{self.klichka}: Гав-гав!"

rex = Sobaka("Рекс")
print(rex.layat())
print(Sobaka.layat(rex))''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте класс `Kot` с атрибутом `klichka` и "
          "методом `myaukat()`, возвращающим строку вида «Барсик: Мяу!».")
    nb.code('''class Kot:
    def __init__(self, klichka):
        self.klichka = klichka

    def myaukat(self):
        return f"{self.klichka}: Мяу!"

kot = Kot("Барсик")
print(kot.myaukat())
print(Kot.myaukat(kot))''')
    nb.write(OUT_DIR / "14-05-self-svyazyvanie.ipynb")
    print(f"Записано: 14-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-06 · __init__ и создание объекта\n\nПрактика к разделу "
          "[«__init__ и создание объекта»](../../site/chapters/glava-14/14-06-init-i-sozdanie-obekta.html).")
    nb.md("## Цель\n\nЗначения по умолчанию в __init__ и независимость объектов.")
    nb.md("## Рабочий пример")
    nb.code('''class Sobaka:
    def __init__(self, klichka, vozrast=1):
        self.klichka = klichka
        self.vozrast = vozrast

shchenok = Sobaka("Бим")
rex = Sobaka("Рекс", vozrast=3)
print(shchenok.vozrast, rex.vozrast)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте класс `Student` с параметрами `imya` и "
          "`kurs=1` (по умолчанию). Создайте `s1` без указания курса и `s2` с курсом 3.")
    nb.code('''class Student:
    def __init__(self, imya, kurs=1):
        self.imya = imya
        self.kurs = kurs

s1 = Student("Аня")
s2 = Student("Боря", 3)
print(s1.kurs, s2.kurs)''')
    nb.write(OUT_DIR / "14-06-init-sozdanie.ipynb")
    print(f"Записано: 14-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-07 · Атрибуты экземпляра и класса\n\nПрактика к разделу "
          "[«Атрибуты экземпляра и класса»](../../site/chapters/glava-14/14-07-atributy-ekzemplyara-i-klassa.html).")
    nb.md("## Цель\n\nОтличить атрибут класса (общий) от атрибута экземпляра (свой).")
    nb.md("## Рабочий пример")
    nb.code('''class Sobaka:
    vid = "Собака"

    def __init__(self, klichka):
        self.klichka = klichka

rex = Sobaka("Рекс")
sharik = Sobaka("Шарик")
print(rex.vid, sharik.vid)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте класс `Rabotnik` с атрибутом класса "
          "`company = \"Cartesian School\"` и атрибутом экземпляра `imya`. Создайте `w1` и "
          "`w2`, затем присвойте `w1.company` новое значение напрямую — `w2.company` не "
          "должно измениться.")
    nb.code('''class Rabotnik:
    company = "Cartesian School"

    def __init__(self, imya):
        self.imya = imya

w1 = Rabotnik("Аня")
w2 = Rabotnik("Боря")
w1.company = "Другая компания"
print(w1.company, w2.company, Rabotnik.company)''')
    nb.write(OUT_DIR / "14-07-atributy.ipynb")
    print(f"Записано: 14-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-08 · Ловушка общего изменяемого атрибута\n\nПрактика к разделу "
          "[«Ловушка общего изменяемого атрибута»](../../site/chapters/glava-14/14-08-lovushka-obshchego-atributa.html).")
    nb.md("## Цель\n\nПравильно объявить изменяемый атрибут — внутри __init__, а не в теле класса.")
    nb.md("## Рабочий пример")
    nb.code('''class Korzina:
    def __init__(self):
        self.tovary = []

    def dobavit(self, tovar):
        self.tovary.append(tovar)

k1 = Korzina()
k2 = Korzina()
k1.dobavit("Хлеб")
print(k1.tovary, k2.tovary)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте класс `Zametki` с атрибутом экземпляра "
          "`spisok = []` (созданным в `__init__`, не в теле класса!) и методом "
          "`dobavit_zametku(tekst)`. Создайте `z1` и `z2`, добавьте разные записи в каждую и "
          "убедитесь, что они не смешиваются.")
    nb.code('''class Zametki:
    def __init__(self):
        self.spisok = []

    def dobavit_zametku(self, tekst):
        self.spisok.append(tekst)

z1 = Zametki()
z2 = Zametki()
z1.dobavit_zametku("Купить хлеб")
z2.dobavit_zametku("Позвонить маме")
print(z1.spisok)
print(z2.spisok)''')
    nb.write(OUT_DIR / "14-08-lovushka-atributa.ipynb")
    print(f"Записано: 14-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-09 · Мини-проект: Player\n\nПрактика к разделу "
          "[«Мини-проект: Player»](../../site/chapters/glava-14/14-09-mini-proekt-player.html).")
    nb.md("## Цель\n\nСобрать класс Player с проверенными изменениями состояния.")
    nb.md("## Рабочий пример")
    nb.code('''class Player:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.score = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def add_score(self, points):
        self.score += points

p = Player("Anna")
p.take_damage(30)
p.add_score(15)
print(p.health, p.score)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте классу `Player` метод "
          "`is_alive()`, возвращающий `True`, если `health` больше 0.")
    nb.code('''class Player:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.score = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def add_score(self, points):
        self.score += points

    def is_alive(self):
        return self.health > 0

p = Player("Anna")
p.take_damage(30)
p.add_score(15)
print(p.health, p.score, p.is_alive())''')
    nb.write(OUT_DIR / "14-09-player.ipynb")
    print(f"Записано: 14-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-10 · Инкапсуляция\n\nПрактика к разделу "
          "[«Инкапсуляция»](../../site/chapters/glava-14/14-10-inkapsulyatsiya.html).")
    nb.md("## Цель\n\nЗащитить состояние объекта, разрешив менять его только через методы.")
    nb.md("## Рабочий пример")
    nb.code('''class Konto:
    def __init__(self, balans):
        self.__balans = balans

    def popolnit(self, summa):
        if summa > 0:
            self.__balans += summa
            return True
        return False

    def poluchit_balans(self):
        return self.__balans

schet = Konto(100)
schet.popolnit(50)
print(schet.poluchit_balans())''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте классу `Konto` метод `snyat(summa)`, "
          "который уменьшает `__balans` только если `summa` не превышает текущий баланс, и "
          "возвращает `True`/`False` в зависимости от успеха.")
    nb.code('''class Konto:
    def __init__(self, balans):
        self.__balans = balans

    def popolnit(self, summa):
        if summa > 0:
            self.__balans += summa
            return True
        return False

    def snyat(self, summa):
        if 0 < summa <= self.__balans:
            self.__balans -= summa
            return True
        return False

    def poluchit_balans(self):
        return self.__balans

schet = Konto(100)
schet.popolnit(50)
uspeshno = schet.snyat(30)
neuspeshno = schet.snyat(9999)
print(schet.poluchit_balans(), uspeshno, neuspeshno)''')
    nb.write(OUT_DIR / "14-10-inkapsulyatsiya.ipynb")
    print(f"Записано: 14-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-11 · property\n\nПрактика к разделу "
          "[«property: вычисляемые атрибуты»](../../site/chapters/glava-14/14-11-property.html).")
    nb.md("## Цель\n\n@property и @x.setter — проверка при присваивании без изменения синтаксиса.")
    nb.md("## Рабочий пример")
    nb.code('''class Krug:
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("радиус должен быть положительным")
        self._radius = value

    @property
    def ploshchad(self):
        return 3.14159 * self.radius ** 2

krug = Krug(10)
print(krug.ploshchad)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте, что присваивание отрицательного "
          "радиуса вызывает `ValueError` — поймайте его через `try/except` и сохраните "
          "результат в переменную `validatsiya_srabotala`.")
    nb.code('''krug = Krug(10)
ploshchad_do = krug.ploshchad

validatsiya_srabotala = False
try:
    krug.radius = -5
except ValueError:
    validatsiya_srabotala = True

print(ploshchad_do, validatsiya_srabotala, krug.radius)''')
    nb.write(OUT_DIR / "14-11-property.ipynb")
    print(f"Записано: 14-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-12 · Мини-проект: Rectangle\n\nПрактика к разделу "
          "[«Мини-проект: Rectangle»](../../site/chapters/glava-14/14-12-mini-proekt-rectangle.html).")
    nb.md("## Цель\n\nПроверенные размеры и вычисляемые площадь с периметром через property.")
    nb.md("## Рабочий пример")
    nb.code('''class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("ширина должна быть положительной")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("высота должна быть положительной")
        self._height = value

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(10, 4)
print(r.area, r.perimeter)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте классу `Rectangle` свойство "
          "`is_square`, возвращающее `True`, если `width` равна `height`.")
    nb.code('''class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("ширина должна быть положительной")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("высота должна быть положительной")
        self._height = value

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

    @property
    def is_square(self):
        return self.width == self.height

kvadrat = Rectangle(5, 5)
ne_kvadrat = Rectangle(5, 9)
print(kvadrat.is_square, ne_kvadrat.is_square)''')
    nb.write(OUT_DIR / "14-12-rectangle.ipynb")
    print(f"Записано: 14-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-13 · Композиция\n\nПрактика к разделу "
          "[«Композиция: объекты внутри объектов»](../../site/chapters/glava-14/14-13-kompozitsiya.html).")
    nb.md("## Цель\n\nОдин объект хранит другой объект (HAS-A) и делегирует ему работу.")
    nb.md("## Рабочий пример")
    nb.code('''class Motor:
    def __init__(self, moshchnost):
        self.moshchnost = moshchnost

    def start(self):
        return f"Двигатель мощностью {self.moshchnost} л.с. запущен"


class Avtomobil:
    def __init__(self, moshchnost):
        self.dvigatel = Motor(moshchnost)

    def start(self):
        return self.dvigatel.start()

mashina = Avtomobil(150)
print(mashina.start())''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте `Avtomobil` метод "
          "`opisanie()`, возвращающий строку с мощностью двигателя, обращаясь к "
          "`self.dvigatel.moshchnost`.")
    nb.code('''class Motor:
    def __init__(self, moshchnost):
        self.moshchnost = moshchnost

    def start(self):
        return f"Двигатель мощностью {self.moshchnost} л.с. запущен"


class Avtomobil:
    def __init__(self, moshchnost):
        self.dvigatel = Motor(moshchnost)

    def start(self):
        return self.dvigatel.start()

    def opisanie(self):
        return f"Автомобиль с двигателем {self.dvigatel.moshchnost} л.с."

mashina = Avtomobil(150)
print(mashina.opisanie())''')
    nb.write(OUT_DIR / "14-13-kompozitsiya.ipynb")
    print(f"Записано: 14-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-14 · Мини-проект: Корзина покупок v2\n\nПрактика к разделу "
          "[«Мини-проект: Корзина покупок v2»](../../site/chapters/glava-14/14-14-mini-proekt-korzina-v2.html).")
    nb.md("## Цель\n\nПереписать корзину покупок главы 12 через объекты Tovar и Korzina.")
    nb.md("## Рабочий пример")
    nb.code('''class Tovar:
    def __init__(self, nazvanie, tsena):
        self.nazvanie = nazvanie
        self.tsena = tsena


class Korzina:
    def __init__(self):
        self.tovary = []

    def dobavit_tovar(self, tovar):
        self.tovary.append(tovar)

    def obshchaya_summa(self):
        return sum(t.tsena for t in self.tovary)

    def kolichestvo_tovarov(self):
        return len(self.tovary)

korzina = Korzina()
korzina.dobavit_tovar(Tovar("Книга", 590))
korzina.dobavit_tovar(Tovar("Ручка", 90))
print(korzina.kolichestvo_tovarov(), korzina.obshchaya_summa())''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте классу `Korzina` метод "
          "`udalit_tovar(nazvanie)`, удаляющий из `self.tovary` первый товар с этим "
          "названием.")
    nb.code('''class Tovar:
    def __init__(self, nazvanie, tsena):
        self.nazvanie = nazvanie
        self.tsena = tsena


class Korzina:
    def __init__(self):
        self.tovary = []

    def dobavit_tovar(self, tovar):
        self.tovary.append(tovar)

    def udalit_tovar(self, nazvanie):
        for t in self.tovary:
            if t.nazvanie == nazvanie:
                self.tovary.remove(t)
                return True
        return False

    def obshchaya_summa(self):
        return sum(t.tsena for t in self.tovary)

    def kolichestvo_tovarov(self):
        return len(self.tovary)

korzina = Korzina()
korzina.dobavit_tovar(Tovar("Книга", 590))
korzina.dobavit_tovar(Tovar("Ручка", 90))
korzina.udalit_tovar("Ручка")
print(korzina.kolichestvo_tovarov(), korzina.obshchaya_summa())''')
    nb.write(OUT_DIR / "14-14-korzina-v2.ipynb")
    print(f"Записано: 14-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-15 · Наследование\n\nПрактика к разделу "
          "[«Наследование»](../../site/chapters/glava-14/14-15-nasledovanie.html).")
    nb.md("## Цель\n\nIS-A отношение: class Child(Parent) переиспользует общее поведение.")
    nb.md("## Рабочий пример")
    nb.code('''class Zhivotnoe:
    def __init__(self, klichka):
        self.klichka = klichka

    def predstavitsya(self):
        return f"Я {self.klichka}"


class Sobaka(Zhivotnoe):
    def zvuk(self):
        return "Гав!"


class Koshka(Zhivotnoe):
    def zvuk(self):
        return "Мяу!"

rex = Sobaka("Рекс")
print(rex.predstavitsya(), rex.zvuk())''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте класс `Korova(Zhivotnoe)` со своим "
          "методом `zvuk()`, возвращающим «Му!».")
    nb.code('''class Korova(Zhivotnoe):
    def zvuk(self):
        return "Му!"

burenka = Korova("Бурёнка")
print(burenka.predstavitsya(), burenka.zvuk())
print(isinstance(burenka, Zhivotnoe))''')
    nb.write(OUT_DIR / "14-15-nasledovanie.ipynb")
    print(f"Записано: 14-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-16 · super()\n\nПрактика к разделу "
          "[«super() и порядок разрешения методов»](../../site/chapters/glava-14/14-16-super.html).")
    nb.md("## Цель\n\nДополнить __init__ родителя, а не заменить его целиком.")
    nb.md("## Рабочий пример")
    nb.code('''class Zhivotnoe:
    def __init__(self, klichka):
        self.klichka = klichka


class Sobaka(Zhivotnoe):
    def __init__(self, klichka, poroda):
        super().__init__(klichka)
        self.poroda = poroda

rex = Sobaka("Рекс", "Дворняга")
print(rex.klichka, rex.poroda)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоздайте класс `Koshka(Zhivotnoe)` с "
          "__init__(self, klichka, okras), вызывающим `super().__init__(klichka)`, затем "
          "устанавливающим `self.okras`.")
    nb.code('''class Koshka(Zhivotnoe):
    def __init__(self, klichka, okras):
        super().__init__(klichka)
        self.okras = okras

murka = Koshka("Мурка", "рыжий")
print(murka.klichka, murka.okras)''')
    nb.write(OUT_DIR / "14-16-super.ipynb")
    print(f"Записано: 14-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-17 · Переопределение методов\n\nПрактика к разделу "
          "[«Переопределение методов»](../../site/chapters/glava-14/14-17-pereopredelenie-metodov.html).")
    nb.md("## Цель\n\nРасширить метод родителя через super().method(), а не заменить его целиком.")
    nb.md("## Рабочий пример")
    nb.code('''class Zhivotnoe:
    def zvuk(self):
        return "Животное подаёт голос: "


class Sobaka(Zhivotnoe):
    def zvuk(self):
        return super().zvuk() + "Гав!"

print(Sobaka().zvuk())''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоздайте класс `Koshka(Zhivotnoe)`, "
          "переопределяющий `zvuk()` через `super().zvuk()` и добавляющий «Мяу!».")
    nb.code('''class Koshka(Zhivotnoe):
    def zvuk(self):
        return super().zvuk() + "Мяу!"

print(Koshka().zvuk())''')
    nb.write(OUT_DIR / "14-17-pereopredelenie.ipynb")
    print(f"Записано: 14-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-18 · Полиморфизм\n\nПрактика к разделу "
          "[«Полиморфизм»](../../site/chapters/glava-14/14-18-polimorfizm.html).")
    nb.md("## Цель\n\nОдин вызов метода — разное поведение в зависимости от класса объекта.")
    nb.md("## Рабочий пример")
    nb.code('''class Sobaka:
    def zvuk(self):
        return "Гав!"


class Koshka:
    def zvuk(self):
        return "Мяу!"


class Korova:
    def zvuk(self):
        return "Му!"


def poluchit_zvuk(zhivotnoe):
    return zhivotnoe.zvuk()

zhivotnye = [Sobaka(), Koshka(), Korova()]
zvuki = [poluchit_zvuk(zh) for zh in zhivotnye]
print(zvuki)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте `poluchit_zvuk()` на каждом классе по "
          "отдельности.")
    nb.code('''zvuk_sobaki = poluchit_zvuk(Sobaka())
zvuk_koshki = poluchit_zvuk(Koshka())
zvuk_korovy = poluchit_zvuk(Korova())
print(zvuk_sobaki, zvuk_koshki, zvuk_korovy)''')
    nb.write(OUT_DIR / "14-18-polimorfizm.ipynb")
    print(f"Записано: 14-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-19 · Duck typing\n\nПрактика к разделу "
          "[«Duck typing»](../../site/chapters/glava-14/14-19-duck-typing.html).")
    nb.md("## Цель\n\nПолиморфизм без общего родителя — важно только наличие метода.")
    nb.md("## Рабочий пример")
    nb.code('''class Chelovek:
    def __init__(self, imya):
        self.imya = imya

    def predstavitsya(self):
        return f"Привет, я {self.imya}!"


class Robot:
    def __init__(self, nomer):
        self.nomer = nomer

    def predstavitsya(self):
        return f"БИП. Я робот номер {self.nomer}."


def poznakomit(obj):
    return obj.predstavitsya()

print(poznakomit(Chelovek("Аня")))
print(poznakomit(Robot(7)))''')
    nb.md("## Задание ★★ Самостоятельная задача\n\n`Chelovek` и `Robot` не имеют общего "
          "родителя (кроме `object`). Проверьте, что `poznakomit()` всё равно работает с "
          "обоими, и сохраните оба результата.")
    nb.code('''rezultat_chelovek = poznakomit(Chelovek("Боря"))
rezultat_robot = poznakomit(Robot(42))
print(rezultat_chelovek)
print(rezultat_robot)''')
    nb.write(OUT_DIR / "14-19-duck-typing.ipynb")
    print(f"Записано: 14-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-20 · Мини-проект: полиморфные фигуры\n\nПрактика к разделу "
          "[«Мини-проект: полиморфные фигуры»](../../site/chapters/glava-14/14-20-mini-proekt-figury.html).")
    nb.md("## Цель\n\nОбщий предок задаёт интерфейс, каждая фигура реализует его по-своему.")
    nb.md("## Рабочий пример")
    nb.code('''class Figura:
    def __init__(self, nazvanie):
        self.nazvanie = nazvanie

    def ploshchad(self):
        raise NotImplementedError


class Krug(Figura):
    def __init__(self, radius):
        super().__init__("круг")
        self.radius = radius

    def ploshchad(self):
        return 3.14159 * self.radius ** 2


class Pryamougolnik(Figura):
    def __init__(self, width, height):
        super().__init__("прямоугольник")
        self.width = width
        self.height = height

    def ploshchad(self):
        return self.width * self.height


class Treugolnik(Figura):
    def __init__(self, base, height):
        super().__init__("треугольник")
        self.base = base
        self.height = height

    def ploshchad(self):
        return 0.5 * self.base * self.height

figury = [Krug(5), Pryamougolnik(4, 6), Treugolnik(8, 3)]
for f in figury:
    print(f.nazvanie, round(f.ploshchad(), 2))''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте `Figura` метод-заглушку "
          "`perimetr()` (`raise NotImplementedError`) и реализуйте его во всех трёх фигурах.")
    nb.code('''class Figura:
    def __init__(self, nazvanie):
        self.nazvanie = nazvanie

    def ploshchad(self):
        raise NotImplementedError

    def perimetr(self):
        raise NotImplementedError


class Krug(Figura):
    def __init__(self, radius):
        super().__init__("круг")
        self.radius = radius

    def ploshchad(self):
        return 3.14159 * self.radius ** 2

    def perimetr(self):
        return 2 * 3.14159 * self.radius


class Pryamougolnik(Figura):
    def __init__(self, width, height):
        super().__init__("прямоугольник")
        self.width = width
        self.height = height

    def ploshchad(self):
        return self.width * self.height

    def perimetr(self):
        return 2 * (self.width + self.height)


class Treugolnik(Figura):
    def __init__(self, base, height):
        super().__init__("треугольник")
        self.base = base
        self.height = height

    def ploshchad(self):
        return 0.5 * self.base * self.height

    def perimetr(self):
        # равнобедренный треугольник: боковая сторона — по теореме Пифагора
        # из половины основания и высоты
        storona = (self.base / 2) ** 2 + self.height ** 2
        return self.base + 2 * storona ** 0.5

krug = Krug(5)
pryamougolnik = Pryamougolnik(4, 6)
treugolnik = Treugolnik(8, 3)
print(round(krug.perimetr(), 2), pryamougolnik.perimetr(), treugolnik.perimetr())''')
    nb.write(OUT_DIR / "14-20-figury.ipynb")
    print(f"Записано: 14-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-21 · Специальные методы\n\nПрактика к разделу "
          "[«Специальные методы»](../../site/chapters/glava-14/14-21-spetsialnye-metody.html).")
    nb.md("## Цель\n\n__str__, __eq__ и __hash__ — как объект подключается к print(), == и set().")
    nb.md("## Рабочий пример")
    nb.code('''class Dengi:
    def __init__(self, summa):
        self.summa = summa

    def __str__(self):
        return f"{self.summa} ₽"

    def __eq__(self, other):
        return self.summa == other.summa

    def __hash__(self):
        return hash(self.summa)

a = Dengi(100)
b = Dengi(100)
print(str(a), a == b)
print(len({a, b}))''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте `Dengi` на нескольких значениях: "
          "убедитесь, что разные суммы не равны и корректно работают в множестве.")
    nb.code('''c = Dengi(250)
ravny = (a == b)
ne_ravny = (a == c)
mnozhestvo = {a, b, c}
print(ravny, ne_ravny, len(mnozhestvo))''')
    nb.write(OUT_DIR / "14-21-spetsialnye-metody.ipynb")
    print(f"Записано: 14-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-22 · Практика: __str__ и __eq__\n\nПрактика к разделу "
          "[«Практика: применяем __str__ и __eq__»](../../site/chapters/glava-14/14-22-primenyaem-dunder-metody.html).")
    nb.md("## Цель\n\nПрименить __str__ и __eq__ к классу Tochka.")
    nb.md("## Рабочий пример")
    nb.code('''class Tochka:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

a = Tochka(1, 2)
b = Tochka(1, 2)
c = Tochka(5, 5)
print(str(a), a == b, a == c)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте `Tochka` метод "
          "`rasstoyanie_do(other)`, возвращающий евклидово расстояние до другой точки.")
    nb.code('''class Tochka:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def rasstoyanie_do(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

nachalo = Tochka(0, 0)
konec = Tochka(3, 4)
rasstoyanie = nachalo.rasstoyanie_do(konec)
print(rasstoyanie)''')
    nb.write(OUT_DIR / "14-22-dunder-praktika.ipynb")
    print(f"Записано: 14-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-23 · dataclasses\n\nПрактика к разделу "
          "[«dataclasses»](../../site/chapters/glava-14/14-23-dataclasses.html).")
    nb.md("## Цель\n\n@dataclass и field(default_factory=...) — избегаем ловушки изменяемого значения по умолчанию.")
    nb.md("## Рабочий пример")
    nb.code('''from dataclasses import dataclass, field

@dataclass
class Korzina:
    tovary: list = field(default_factory=list)

    def dobavit(self, tovar):
        self.tovary.append(tovar)

k1 = Korzina()
k2 = Korzina()
k1.dobavit("Хлеб")
print(k1.tovary, k2.tovary)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте третью корзину `k3` и убедитесь, что она "
          "тоже начинается пустой, независимо от `k1` и `k2`.")
    nb.code('''k3 = Korzina()
k3.dobavit("Молоко")
print(k1.tovary, k2.tovary, k3.tovary)''')
    nb.write(OUT_DIR / "14-23-dataclasses.ipynb")
    print(f"Записано: 14-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-24 · Практика: dataclass\n\nПрактика к разделу "
          "[«Практика: dataclass»](../../site/chapters/glava-14/14-24-praktika-dataclass.html).")
    nb.md("## Цель\n\nПереписать Tovar главы 14.14 через @dataclass и собрать вокруг него Zakaz.")
    nb.md("## Рабочий пример")
    nb.code('''from dataclasses import dataclass

@dataclass
class Tovar:
    nazvanie: str
    tsena: float

    def so_skidkoj(self, protsent):
        return self.tsena * (1 - protsent / 100)

knigi = Tovar("Книга", 590)
print(knigi)
print(knigi.so_skidkoj(10))''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nОпределите `@dataclass Zakaz` с полями "
          "`tovar: Tovar` и `kolichestvo: int`, и методом `summa()`, возвращающим "
          "`self.tovar.tsena * self.kolichestvo`.")
    nb.code('''@dataclass
class Zakaz:
    tovar: Tovar
    kolichestvo: int

    def summa(self):
        return self.tovar.tsena * self.kolichestvo

ruchka = Tovar("Ручка", 100)
zakaz = Zakaz(ruchka, 3)
print(zakaz.summa())''')
    nb.write(OUT_DIR / "14-24-dataclass-praktika.ipynb")
    print(f"Записано: 14-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-25 · Класс или не класс?\n\nПрактика к разделу "
          "[«Класс или не класс? Проектируем модели»](../../site/chapters/glava-14/14-25-proektiruem-modeli.html).")
    nb.md("## Цель\n\nРазличить задачу, которой нужен класс, от задачи, которой хватит функции.")
    nb.md("## Рабочий пример")
    nb.code('''# Разовое вычисление без хранимого состояния — функции достаточно
def srednee_arifmeticheskoe(chisla):
    return sum(chisla) / len(chisla)

print(srednee_arifmeticheskoe([4, 8, 15]))''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоздайте класс `Schet` — счётчик с "
          "состоянием, которое накапливается между вызовами: `value`, начинающееся с 0, и "
          "метод `increment()`, увеличивающий его на 1. Здесь класс оправдан — состояние "
          "должно сохраняться МЕЖДУ вызовами, что функция сама по себе сделать не может.")
    nb.code('''class Schet:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

schet = Schet()
schet.increment()
schet.increment()
print(schet.value)''')
    nb.write(OUT_DIR / "14-25-klass-ili-net.ipynb")
    print(f"Записано: 14-25 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md("# 14-26 · Гонка Turtle v2\n\nПрактика к разделу "
          "[«Мини-проект: гонка Turtle v2»](../../site/chapters/glava-14/14-26-mini-proekt-gonka-v2.html).")
    nb.md("## Цель\n\nGonka как объект, управляющий списком объектов Uchastnik.")
    nb.md("""\
## О случайности в этом ноутбуке

Гонка использует `random.randint()` — для предсказуемого результата в автоматическом
выполнении здесь закрепляем случайность через `random.seed()`.""")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''import random

random.seed(7)
screen.setup(520, 420)

class Uchastnik:
    def __init__(self, cvet, startovyj_y):
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.t.color(cvet)
        self.t.penup()
        self.t.goto(-220, startovyj_y)
        self.cvet = cvet
        self.finishiroval = False

    def sdelat_shag(self):
        if not self.finishiroval:
            self.t.forward(random.randint(1, 10))

    def proverit_finish(self, finish_x):
        if self.t.xcor() >= finish_x:
            self.finishiroval = True
        return self.finishiroval


class Gonka:
    def __init__(self, cveta, finish_x):
        self.finish_x = finish_x
        self.uchastniki = [
            Uchastnik(cvet, i * 50 - 75) for i, cvet in enumerate(cveta)
        ]
        self.rezultaty = []

    def narisovat_finish(self):
        liniya = turtle.Turtle()
        liniya.hideturtle()
        liniya.penup()
        liniya.goto(self.finish_x, -120)
        liniya.pendown()
        liniya.pencolor("#0D0230")
        liniya.pensize(3)
        liniya.setheading(90)
        liniya.forward(240)

    def sygrat_do_kontsa(self):
        self.narisovat_finish()
        while len(self.rezultaty) < len(self.uchastniki):
            for u in self.uchastniki:
                u.sdelat_shag()
                if u.proverit_finish(self.finish_x) and u.cvet not in self.rezultaty:
                    self.rezultaty.append(u.cvet)

gonka = Gonka(["red", "blue", "green"], 210)
gonka.sygrat_do_kontsa()
print(f"Порядок финиша: {gonka.rezultaty}")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "14-26-gonka-v2.ipynb")
    print(f"Записано: 14-26 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
    build_07()
    build_08()
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
    build_22()
    build_23()
    build_24()
    build_25()
    build_26()
