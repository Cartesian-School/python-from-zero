#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 19 (Змейка)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-19"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = '''import turtle

RAZMER_SHAGA = 20
GRANICA = 280

screen = turtle.Screen()
screen.title("Змейка")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)
print("Экран готов.")'''
SETUP_CODE_S_RANDOM = '''import random
import turtle

RAZMER_SHAGA = 20
GRANICA = 280

screen = turtle.Screen()
screen.title("Змейка")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)
print("Экран готов.")'''
TEARDOWN_MD = "## Завершение (выполнить один раз, в самом конце)"
TEARDOWN_CODE = '''screen.bye()
print("Окно закрыто.")'''


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 19-02 · Экран и переменные\n\nПрактика к разделу "
          "[«Настраиваем экран Turtle и переменные»](../../site/chapters/glava-19/19-02-ekran-peremennye.html).")
    nb.md("## Цель\n\nНастроить экран с tracer(0) и завести переменные состояния.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''napravlenie = "stop"
schet = 0
igra_okonchena = False
segmenty = []

print("Направление:", napravlenie)
print("Счёт:", schet)
print("Игра окончена:", igra_okonchena)''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-02-ekran.ipynb")
    print(f"Записано: 19-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 19-03 · Голова и яблоко\n\nПрактика к разделу "
          "[«Рисуем голову и яблоко»](../../site/chapters/glava-19/19-03-golova-yabloko.html).")
    nb.md("## Цель\n\nСоздать голову и яблоко, разместить яблоко случайно.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE_S_RANDOM)
    nb.md("## Рабочий пример")
    nb.code('''golova = turtle.Turtle()
golova.speed(0)
golova.shape("square")
golova.color("white")
golova.penup()
golova.goto(0, 0)

yabloko = turtle.Turtle()
yabloko.speed(0)
yabloko.shape("circle")
yabloko.color("red")
yabloko.penup()

def novoe_yabloko():
    x = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)
    y = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)
    yabloko.goto(x, y)

novoe_yabloko()
print("Голова:", golova.position())
print("Яблоко:", yabloko.position())
screen.update()''')
    nb.md("## Эксперимент 1\n\nПроверьте, что яблоко всегда появляется «в клетке» (координаты "
          "кратны RAZMER_SHAGA).")
    nb.code('''for _ in range(5):
    novoe_yabloko()
    x, y = yabloko.position()
    print(x, y, "-> кратно шагу:", x % RAZMER_SHAGA == 0 and y % RAZMER_SHAGA == 0)''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-03-golova-yabloko.ipynb")
    print(f"Записано: 19-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 19-04 · Клавиши и движение\n\nПрактика к разделу "
          "[«Клавиши и движение головы»](../../site/chapters/glava-19/19-04-klavishi-dvizhenie.html).")
    nb.md("## Цель\n\nОсвоить смену направления с защитой от разворота на 180°.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''golova = turtle.Turtle()
golova.speed(0)
golova.shape("square")
golova.penup()
golova.goto(0, 0)

napravlenie = "stop"

def idti_vverh():
    global napravlenie
    if napravlenie != "down":
        napravlenie = "up"

def idti_vniz():
    global napravlenie
    if napravlenie != "up":
        napravlenie = "down"

def idti_vlevo():
    global napravlenie
    if napravlenie != "right":
        napravlenie = "left"

def idti_vpravo():
    global napravlenie
    if napravlenie != "left":
        napravlenie = "right"

def dvigat_golovu():
    if napravlenie == "up":
        golova.sety(golova.ycor() + RAZMER_SHAGA)
    elif napravlenie == "down":
        golova.sety(golova.ycor() - RAZMER_SHAGA)
    elif napravlenie == "left":
        golova.setx(golova.xcor() - RAZMER_SHAGA)
    elif napravlenie == "right":
        golova.setx(golova.xcor() + RAZMER_SHAGA)

idti_vpravo()
dvigat_golovu()
print("После шага вправо:", golova.position())''')
    nb.md("## Эксперимент 1 — защита от разворота на 180°")
    nb.code('''idti_vpravo()
print("Направление после idti_vpravo():", napravlenie)

idti_vlevo()  # НЕ должно сработать — змейка едет вправо
print("Направление после idti_vlevo() (должно остаться right):", napravlenie)

idti_vverh()  # а вот поворот на 90° должен сработать
print("Направление после idti_vverh():", napravlenie)''')
    nb.md("## Проверка результата")
    nb.code('''assert napravlenie == "up"
print("Верно: разворот на 180° заблокирован, поворот на 90° разрешён.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-04-dvizhenie.ipynb")
    print(f"Записано: 19-04 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 19-06 · Еда и движение тела\n\nПрактика к разделу "
          "[«Змейка ест! Движение тела»](../../site/chapters/glava-19/19-06-eda-telo.html).")
    nb.md("## Цель\n\nОсвоить проверку поедания яблока и движение сегментов тела.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE_S_RANDOM)
    nb.md("## Рабочий пример")
    nb.code('''golova = turtle.Turtle()
golova.speed(0)
golova.shape("square")
golova.penup()
golova.goto(0, 0)

yabloko = turtle.Turtle()
yabloko.speed(0)
yabloko.shape("circle")
yabloko.color("red")
yabloko.penup()
yabloko.goto(20, 0)  # ставим яблоко рядом для теста

schet = 0
segmenty = []

def novoe_yabloko():
    x = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)
    y = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)
    yabloko.goto(x, y)

def dobavit_segment():
    novyj = turtle.Turtle()
    novyj.speed(0)
    novyj.shape("square")
    novyj.color("grey")
    novyj.penup()
    segmenty.append(novyj)

def proverit_edu():
    global schet
    if golova.distance(yabloko) < RAZMER_SHAGA:
        novoe_yabloko()
        dobavit_segment()
        schet += 10

golova.goto(20, 0)  # "подъезжаем" к яблоку
proverit_edu()
print("Счёт:", schet, "| Сегментов:", len(segmenty))''')
    nb.md("## Эксперимент 1 — движение тела вслед за головой\n\nВажен порядок: `dvigat_telo()` "
          "вызывается, пока голова ещё на *старой* позиции — только потом голова едет дальше.")
    nb.code('''def dvigat_telo():
    for indeks in range(len(segmenty) - 1, 0, -1):
        x = segmenty[indeks - 1].xcor()
        y = segmenty[indeks - 1].ycor()
        segmenty[indeks].goto(x, y)
    if segmenty:
        segmenty[0].goto(golova.xcor(), golova.ycor())

print("Голова сейчас:", golova.position())
dvigat_telo()  # сегмент подтягивается к ТЕКУЩЕЙ (пока ещё старой) позиции головы
print("Сегмент после dvigat_telo():", segmenty[0].position())

golova.setx(golova.xcor() + RAZMER_SHAGA)  # и только теперь голова едет дальше
print("Голова уехала вперёд:", golova.position())
print("А сегмент остался на прежнем месте головы:", segmenty[0].position())''')
    nb.md("## Проверка результата")
    nb.code('''assert segmenty[0].position() == (20.0, 0.0)
assert golova.position() == (40.0, 0.0)
print("Верно: сегмент остался там, где раньше была голова, а голова уехала дальше.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-06-eda-telo.ipynb")
    print(f"Записано: 19-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 19-07 · Проверка столкновений\n\nПрактика к разделу "
          "[«Проверка столкновений»](../../site/chapters/glava-19/19-07-stolknoveniya.html).")
    nb.md("## Цель\n\nОпределить столкновение со стеной и с собственным телом.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример — стена")
    nb.code('''golova = turtle.Turtle()
golova.speed(0)
golova.penup()

segmenty = []
igra_okonchena = False

def proverit_stolknoveniya():
    global igra_okonchena
    if abs(golova.xcor()) > GRANICA or abs(golova.ycor()) > GRANICA:
        igra_okonchena = True
    for segment in segmenty:
        if segment.distance(golova) < RAZMER_SHAGA / 2:
            igra_okonchena = True

golova.goto(GRANICA + 10, 0)  # выехали за границу
proverit_stolknoveniya()
print("Игра окончена (стена):", igra_okonchena)''')
    nb.md("## Эксперимент 1 — столкновение с собой")
    nb.code('''igra_okonchena = False
golova.goto(40, 40)

segment = turtle.Turtle()
segment.speed(0)
segment.penup()
segment.goto(40, 40)  # сегмент точно там же, где голова
segmenty.append(segment)

proverit_stolknoveniya()
print("Игра окончена (самостолкновение):", igra_okonchena)''')
    nb.md("## Проверка результата")
    nb.code('''assert igra_okonchena is True
print("Верно: столкновение обнаружено.")''')
    nb.md("## Задание ★★ Самостоятельная задача — без ложных срабатываний")
    nb.code('''igra_okonchena = False
golova.goto(0, 0)
segmenty[0].goto(-200, -200)  # сегмент далеко

proverit_stolknoveniya()
print("Игра окончена (должно быть False):", igra_okonchena)
assert igra_okonchena is False
print("Верно: далёкий сегмент не считается столкновением.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-07-stolknoveniya.ipynb")
    print(f"Записано: 19-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 19-08 · Полная игра\n\nПрактика к разделу "
          "[«Полный код и итоги»](../../site/chapters/glava-19/19-08-polnyj-kod-itogi.html). "
          "Тот же код, что и в `projects/turtle/snake/snake.py`.")
    nb.md("## Цель\n\nСобрать и протестировать всю игру одним шагом за раз.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE_S_RANDOM)
    nb.md("## Полная игра")
    nb.code('''napravlenie = "stop"
schet = 0
igra_okonchena = False
segmenty = []

golova = turtle.Turtle()
golova.speed(0)
golova.shape("square")
golova.color("white")
golova.penup()
golova.goto(0, 0)

yabloko = turtle.Turtle()
yabloko.speed(0)
yabloko.shape("circle")
yabloko.color("red")
yabloko.penup()

tablo = turtle.Turtle()
tablo.speed(0)
tablo.color("white")
tablo.penup()
tablo.hideturtle()
tablo.goto(0, 260)


def novoe_yabloko():
    x = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)
    y = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)
    yabloko.goto(x, y)


def obnovit_tablo():
    tablo.clear()
    tablo.write(f"Счёт: {schet}", align="center", font=("Arial", 16, "normal"))


def idti_vverh():
    global napravlenie
    if napravlenie != "down":
        napravlenie = "up"


def idti_vpravo():
    global napravlenie
    if napravlenie != "left":
        napravlenie = "right"


def dvigat_golovu():
    if napravlenie == "up":
        golova.sety(golova.ycor() + RAZMER_SHAGA)
    elif napravlenie == "down":
        golova.sety(golova.ycor() - RAZMER_SHAGA)
    elif napravlenie == "left":
        golova.setx(golova.xcor() - RAZMER_SHAGA)
    elif napravlenie == "right":
        golova.setx(golova.xcor() + RAZMER_SHAGA)


def dobavit_segment():
    novyj = turtle.Turtle()
    novyj.speed(0)
    novyj.shape("square")
    novyj.color("grey")
    novyj.penup()
    segmenty.append(novyj)


def dvigat_telo():
    for indeks in range(len(segmenty) - 1, 0, -1):
        x = segmenty[indeks - 1].xcor()
        y = segmenty[indeks - 1].ycor()
        segmenty[indeks].goto(x, y)
    if segmenty:
        segmenty[0].goto(golova.xcor(), golova.ycor())


def proverit_edu():
    global schet
    if golova.distance(yabloko) < RAZMER_SHAGA:
        novoe_yabloko()
        dobavit_segment()
        schet += 10
        obnovit_tablo()


def proverit_stolknoveniya():
    global igra_okonchena
    if abs(golova.xcor()) > GRANICA or abs(golova.ycor()) > GRANICA:
        igra_okonchena = True
    for segment in segmenty:
        if segment.distance(golova) < RAZMER_SHAGA / 2:
            igra_okonchena = True


def igrovoj_shag():
    if igra_okonchena:
        return False
    dvigat_telo()
    dvigat_golovu()
    proverit_edu()
    proverit_stolknoveniya()
    screen.update()
    return not igra_okonchena


novoe_yabloko()
obnovit_tablo()
print("Игра построена.")''')
    nb.md("## Проверка результата — двигаемся 5 шагов вправо, затем к яблоку")
    nb.code('''random.seed(11)
idti_vpravo()

# поставим яблоко ровно на два шага вперёд по курсу, чтобы гарантированно съесть его
yabloko.goto(golova.xcor() + RAZMER_SHAGA * 2, golova.ycor())

for _ in range(2):
    igrovoj_shag()

print("Счёт после подхода к яблоку:", schet)
print("Сегментов:", len(segmenty))
assert schet == 10
assert len(segmenty) == 1
print("Верно: яблоко съедено, змейка выросла, счёт увеличился.")''')
    nb.md("## Задание ★★★ Самостоятельная задача — доводим змейку до столкновения со стеной")
    nb.code('''# едем вправо, пока не врежемся в стену
shagov = 0
while igrovoj_shag() and shagov < 100:
    shagov += 1

print("Игра окончена:", igra_okonchena, "после", shagov, "шагов")
assert igra_okonchena is True
print("Верно: столкновение со стеной остановило игру.")''')
    nb.write(OUT_DIR / "19-08-polnaya-igra.ipynb")
    print(f"Записано: 19-08 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_02()
    build_03()
    build_04()
    build_06()
    build_07()
    build_08()
