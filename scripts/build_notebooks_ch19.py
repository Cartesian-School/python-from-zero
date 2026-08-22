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


def _lesson_link(lesson_id: str, title: str, href: str) -> str:
    return f"# {lesson_id} · {title}\n\nПрактика к разделу [«{title}»](../../site/chapters/glava-19/{href})."


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


# ---------------------------------------------------------------------------
# browser-auto (Pyodide): чистая логика, без turtle
# ---------------------------------------------------------------------------

def build_09() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-09", "Мир игры как сетка", "19-09-mir-kak-setka.html"))
    nb.md("## Цель\n\nОпределять, лежит ли точка на решётке с шагом STEP.")
    nb.md("## Рабочий пример")
    nb.code('''STEP = 20

def is_on_grid(x, y, step=STEP):
    return x % step == 0 and y % step == 0

print(is_on_grid(40, -60))
print(is_on_grid(41, -60))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert is_on_grid(0, 0) is True
assert is_on_grid(-280, 280) is True
assert is_on_grid(21, 0) is False
assert is_on_grid(0, -5) is False
print("Легальные позиции определены верно.")''')
    nb.write(OUT_DIR / "19-09-mir-kak-setka.ipynb")
    print(f"Записано: 19-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-10", "Координаты клетки и пиксели Turtle", "19-10-koordinaty-kletki.html"))
    nb.md("## Цель\n\nПеревести пиксельные координаты в клетку, аккуратно с отрицательными числами.")
    nb.md("## Рабочий пример")
    nb.code('''STEP = 20

def pixel_to_cell(x, y, step=STEP):
    return x // step, y // step

print(pixel_to_cell(40, 60))
print(pixel_to_cell(-10, 0))   # округление вниз, не к нулю!''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert pixel_to_cell(40, 60) == (2, 3)
assert pixel_to_cell(-10, 0) == (-1, 0)
assert pixel_to_cell(-20, 0) == (-1, 0)
assert pixel_to_cell(-21, 0) == (-2, 0)
print("Отрицательные координаты переведены верно.")''')
    nb.write(OUT_DIR / "19-10-koordinaty-kletki.ipynb")
    print(f"Записано: 19-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-11", "Направление как вектор", "19-11-napravlenie-kak-vektor.html"))
    nb.md("## Цель\n\nВычислить новую позицию головы через словарь векторов вместо if/elif.")
    nb.md("## Рабочий пример")
    nb.code('''STEP = 20
DIRECTION_VECTORS = {
    "up": (0, STEP),
    "down": (0, -STEP),
    "left": (-STEP, 0),
    "right": (STEP, 0),
}

def next_head(head, direction):
    dx, dy = DIRECTION_VECTORS[direction]
    return head[0] + dx, head[1] + dy

print(next_head((0, 0), "right"))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert next_head((0, 0), "up") == (0, 20)
assert next_head((0, 0), "down") == (0, -20)
assert next_head((0, 0), "left") == (-20, 0)
assert next_head((100, 100), "right") == (120, 100)
print("next_head() верна для всех четырёх направлений.")''')
    nb.write(OUT_DIR / "19-11-napravlenie-kak-vektor.ipynb")
    print(f"Записано: 19-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-12", "Один игровой тик", "19-12-odin-igrovoj-tik.html"))
    nb.md("## Цель\n\nПроверить еду ДО применения нового тела — порядок шагов тика имеет значение.")
    nb.md("## Рабочий пример")
    nb.code('''def tick_order(head, food, snake_without_head):
    grow = head == food
    if grow:
        new_snake = [head, *snake_without_head]
    else:
        new_snake = [head, *snake_without_head[:-1]]
    return new_snake, grow

new_snake, grow = tick_order((20, 0), (20, 0), [(0, 0), (-20, 0)])
print(new_snake, grow)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''snake_no_food, grow_no_food = tick_order((20, 0), (100, 100), [(0, 0), (-20, 0)])
assert grow_no_food is False
assert len(snake_no_food) == 2

snake_food, grow_food = tick_order((20, 0), (20, 0), [(0, 0), (-20, 0)])
assert grow_food is True
assert len(snake_food) == 3
print("Еда проверяется раньше сборки нового тела — рост считается верно.")''')
    nb.write(OUT_DIR / "19-12-odin-igrovoj-tik.ipynb")
    print(f"Записано: 19-12 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-14", "Время, скорость и задержка", "19-14-vremya-skorost.html"))
    nb.md("## Цель\n\ncalculate_delay() уменьшает задержку со счётом, не опускаясь ниже минимума.")
    nb.md("## Рабочий пример")
    nb.code('''def calculate_delay(score, *, base_ms=140, min_ms=60, step_score=50, step_ms=10):
    steps = score // step_score
    return max(min_ms, base_ms - steps * step_ms)

print(calculate_delay(0), calculate_delay(50), calculate_delay(100))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert calculate_delay(0) == 140
assert calculate_delay(50) == 130
assert calculate_delay(100_000) == 60
print("Скорость растёт со счётом и не опускается ниже минимума.")''')
    nb.write(OUT_DIR / "19-14-vremya-skorost.ipynb")
    print(f"Записано: 19-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-15", "Состояние игры", "19-15-sostoyanie-igry.html"))
    nb.md("## Цель\n\nОпределять, какие переходы между состояниями игры легальны.")
    nb.md("## Рабочий пример")
    nb.code('''LEGAL_TRANSITIONS = {
    "ready": {"running"},
    "running": {"paused", "game_over"},
    "paused": {"running"},
    "game_over": {"ready"},
}

def can_transition(current, target):
    return target in LEGAL_TRANSITIONS[current]

print(can_transition("running", "paused"))
print(can_transition("paused", "game_over"))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert can_transition("ready", "running") is True
assert can_transition("running", "paused") is True
assert can_transition("paused", "running") is True
assert can_transition("game_over", "ready") is True
assert can_transition("paused", "game_over") is False
assert can_transition("ready", "paused") is False
print("Только явно разрешённые переходы состояния считаются легальными.")''')
    nb.write(OUT_DIR / "19-15-sostoyanie-igry.ipynb")
    print(f"Записано: 19-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-16", "Голова, тело и модель Snake", "19-16-model-snake.html"))
    nb.md("## Цель\n\nЗмейка — список позиций; snake[0] всегда голова.")
    nb.md("## Рабочий пример")
    nb.code('''snake = [(0, 0), (-20, 0), (-40, 0)]

def head_of(snake):
    return snake[0]

def body_of(snake):
    return snake[1:]

print(head_of(snake), body_of(snake))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert head_of(snake) == (0, 0)
assert body_of(snake) == [(-20, 0), (-40, 0)]
assert len(snake) == 3
print("Модель змейки — обычный список координат.")''')
    nb.write(OUT_DIR / "19-16-model-snake.ipynb")
    print(f"Записано: 19-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-17", "Почему тело движется с хвоста", "19-17-pochemu-s-hvosta.html"))
    nb.md("## Цель\n\nПоказать, что обновление от хвоста к голове не теряет позиции.")
    nb.md("## Рабочий пример")
    nb.code('''def move_from_tail(segments, head_pos):
    segments = list(segments)
    for i in range(len(segments) - 1, 0, -1):
        segments[i] = segments[i - 1]
    if segments:
        segments[0] = head_pos
    return segments

print(move_from_tail([(0, 0), (-20, 0), (-40, 0)], (20, 0)))''')
    nb.md("## Задание ★★ Найдите баг в обратном порядке")
    nb.code('''def move_from_head_BROKEN(segments, head_pos):
    segments = list(segments)
    segments[0] = head_pos
    for i in range(1, len(segments)):
        segments[i] = segments[i - 1]   # уже перезаписанное значение!
    return segments

correct = move_from_tail([(0, 0), (-20, 0), (-40, 0)], (20, 0))
broken = move_from_head_BROKEN([(0, 0), (-20, 0), (-40, 0)], (20, 0))
print("Правильно:", correct)
print("Сломано:", broken)
assert correct == [(20, 0), (0, 0), (-20, 0)]
assert broken == [(20, 0), (20, 0), (20, 0)]   # все сегменты схлопнулись
print("Подтверждено: обратный порядок схлопывает сегменты в одну точку.")''')
    nb.write(OUT_DIR / "19-17-pochemu-s-hvosta.ipynb")
    print(f"Записано: 19-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-18", "Еда и свободная клетка", "19-18-eda-svobodnaya-kletka.html"))
    nb.md("## Цель\n\nmove_snake() и choose_food() — новая голова плюс старое тело, еда только на свободной клетке.")
    nb.md("## Рабочий пример")
    nb.code('''import random

STEP = 20

def move_snake(snake, new_head, *, grow):
    if grow:
        return [new_head, *snake]
    return [new_head, *snake[:-1]]

def all_cells(half=100, step=STEP):
    coords = range(-half, half + 1, step)
    return tuple((x, y) for x in coords for y in coords)

def choose_food(snake, rng, *, half=100, step=STEP):
    occupied = set(snake)
    free = tuple(c for c in all_cells(half, step) if c not in occupied)
    return rng.choice(free)

rng = random.Random(7)
print(move_snake([(0, 0), (-20, 0), (-40, 0)], (20, 0), grow=False))
print(choose_food([(0, 0)], rng))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''rng = random.Random(1)
snake = [(0, 0), (-20, 0), (-40, 0), (-60, 0)]
for _ in range(50):
    food = choose_food(snake, rng)
    assert food not in snake

grown = move_snake(snake, (20, 0), grow=True)
assert len(grown) == len(snake) + 1
shifted = move_snake(snake, (20, 0), grow=False)
assert len(shifted) == len(snake)
print("Еда никогда не попадает на змейку; move_snake растит или сдвигает верно.")''')
    nb.write(OUT_DIR / "19-18-eda-svobodnaya-kletka.ipynb")
    print(f"Записано: 19-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-19", "Столкновение со стеной", "19-19-stolknovenie-so-stenoj.html"))
    nb.md("## Цель\n\nis_wall_collision() — граница включена в легальную область.")
    nb.md("## Рабочий пример")
    nb.code('''def is_wall_collision(head, half=280):
    x, y = head
    return abs(x) > half or abs(y) > half

print(is_wall_collision((280, 0)))
print(is_wall_collision((300, 0)))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert is_wall_collision((280, 280)) is False
assert is_wall_collision((-280, -280)) is False
assert is_wall_collision((300, 0)) is True
assert is_wall_collision((0, -281)) is True
print("Граница входит в легальную область; шаг за неё — столкновение.")''')
    nb.write(OUT_DIR / "19-19-stolknovenie-so-stenoj.ipynb")
    print(f"Записано: 19-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-20", "Столкновение с собой", "19-20-stolknovenie-s-soboj.html"))
    nb.md("## Цель\n\nis_self_collision() проверяется против тела ПОСЛЕ хода — заезд в клетку освободившегося хвоста легален.")
    nb.md("## Рабочий пример")
    nb.code('''def move_snake(snake, new_head, *, grow):
    if grow:
        return [new_head, *snake]
    return [new_head, *snake[:-1]]

def is_self_collision(new_head, body_after_move):
    return new_head in body_after_move

snake = [(0, 0), (20, 0), (40, 0), (40, 20)]
new_head = (40, 20)   # клетка старого хвоста
new_snake = move_snake(snake, new_head, grow=False)
print(is_self_collision(new_head, new_snake[1:]))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert is_self_collision(new_head, new_snake[1:]) is False  # хвост уже освободил клетку

middle_hit = move_snake(snake, (20, 0), grow=False)
assert is_self_collision((20, 0), middle_hit[1:]) is True  # (20,0) — не хвост, настоящий удар

grown = move_snake(snake, new_head, grow=True)
assert is_self_collision(new_head, grown[1:]) is True  # при росте хвост НЕ освобождается
print("Заезд в клетку освободившегося хвоста легален только без роста.")''')
    nb.write(OUT_DIR / "19-20-stolknovenie-s-soboj.ipynb")
    print(f"Записано: 19-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-21", "Game Over как состояние", "19-21-game-over.html"))
    nb.md("## Цель\n\nОпределить, какие столкновения переводят игру в GAME_OVER.")
    nb.md("## Рабочий пример")
    nb.code('''def resolve_tick(head, status, *, wall_hit, self_hit):
    if wall_hit or self_hit:
        return "game_over"
    return status

print(resolve_tick((0, 0), "running", wall_hit=True, self_hit=False))
print(resolve_tick((0, 0), "running", wall_hit=False, self_hit=False))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert resolve_tick((0, 0), "running", wall_hit=True, self_hit=False) == "game_over"
assert resolve_tick((0, 0), "running", wall_hit=False, self_hit=True) == "game_over"
assert resolve_tick((0, 0), "running", wall_hit=False, self_hit=False) == "running"
print("Любое из двух столкновений переводит игру в game_over.")''')
    nb.write(OUT_DIR / "19-21-game-over.ipynb")
    print(f"Записано: 19-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-22", "Pause / Resume", "19-22-pauza.html"))
    nb.md("## Цель\n\nТик во время PAUSED не должен менять модель.")
    nb.md("## Рабочий пример")
    nb.code('''def game_tick(snake, status, direction):
    if status != "running":
        return snake, status   # ничего не меняется
    new_snake = [(snake[0][0] + 20, snake[0][1]), *snake[:-1]]
    return new_snake, status

snake = [(0, 0), (-20, 0)]
snake, status = game_tick(snake, "paused", "right")
print(snake, status)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''before = [(0, 0), (-20, 0)]
after, status = game_tick(list(before), "paused", "right")
assert after == before
running_after, _ = game_tick(list(before), "running", "right")
assert running_after != before
print("PAUSED действительно замораживает модель — RUNNING продолжает её двигать.")''')
    nb.write(OUT_DIR / "19-22-pauza.ipynb")
    print(f"Записано: 19-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-23", "Restart / New Game", "19-23-restart.html"))
    nb.md("## Цель\n\nRestart переносит high_score в новое состояние и увеличивает generation.")
    nb.md("## Рабочий пример")
    nb.code('''def new_game_state(high_score=0):
    return {"snake": [(0, 0)], "score": 0, "high_score": high_score, "status": "ready"}

def restart(state, generation):
    return new_game_state(high_score=state["high_score"]), generation + 1

state = {"snake": [(0, 0), (-20, 0), (-40, 0)], "score": 40, "high_score": 40, "status": "game_over"}
new_state, new_generation = restart(state, generation=3)
print(new_state, new_generation)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert new_state["snake"] == [(0, 0)]
assert new_state["score"] == 0
assert new_state["high_score"] == 40   # рекорд пережил рестарт
assert new_generation == 4              # поколение увеличилось
print("Restart сбрасывает игру, сохраняя рекорд и защищая от старых тиков через generation.")''')
    nb.write(OUT_DIR / "19-23-restart.ipynb")
    print(f"Записано: 19-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-24", "Скорость и рост сложности", "19-24-skorost-slozhnost.html"))
    nb.md("## Цель\n\nКаждое съеденное яблоко пересчитывает delay_ms через calculate_delay().")
    nb.md("## Рабочий пример")
    nb.code('''def calculate_delay(score, *, base_ms=140, min_ms=60, step_score=50, step_ms=10):
    steps = score // step_score
    return max(min_ms, base_ms - steps * step_ms)

def eat_food(score, delay_ms, food_score=10):
    score += food_score
    delay_ms = calculate_delay(score)
    return score, delay_ms

score, delay = 0, 140
for _ in range(3):
    score, delay = eat_food(score, delay)
print(score, delay)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''score, delay = eat_food(40, 140)
assert score == 50
assert delay == 130

score, delay = eat_food(999_990, 60)
assert delay == 60  # уже на минимуме, ниже не опускается
print("Скорость растёт вместе со счётом при каждом съеденном яблоке.")''')
    nb.write(OUT_DIR / "19-24-skorost-slozhnost.ipynb")
    print(f"Записано: 19-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-25", "High Score", "19-25-high-score.html"))
    nb.md("## Цель\n\nscore всегда с нуля при рестарте; high_score обновляется через max() и переживает рестарт.")
    nb.md("## Рабочий пример")
    nb.code('''def update_high_score(score, high_score):
    return max(score, high_score)

score, high_score = 0, 40
score += 10
high_score = update_high_score(score, high_score)
print(score, high_score)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert update_high_score(30, 40) == 40    # рекорд не понижается
assert update_high_score(50, 40) == 50    # но обновляется, если счёт его превысил
assert update_high_score(0, 0) == 0
print("high_score никогда не уменьшается — только растёт или остаётся прежним.")''')
    nb.write(OUT_DIR / "19-25-high-score.ipynb")
    print(f"Записано: 19-25 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-26", "Чистая игровая логика без Turtle", "19-26-chistaya-logika.html"))
    nb.md("## Цель\n\nОтличить функции правил (чистая логика) от кода, которому нужен реальный экран.")
    nb.md("## Рабочий пример")
    nb.code('''PURE_LOGIC_NAMES = {
    "next_head", "move_snake", "is_wall_collision",
    "is_self_collision", "choose_food", "calculate_delay",
}
NEEDS_SCREEN_NAMES = {"render", "bind_keys", "game_tick_ontimer_wrapper"}

def is_pure_logic(name):
    return name in PURE_LOGIC_NAMES

print(is_pure_logic("next_head"), is_pure_logic("render"))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert is_pure_logic("move_snake") is True
assert is_pure_logic("is_wall_collision") is True
assert is_pure_logic("render") is False
assert is_pure_logic("bind_keys") is False
print("Правила игры не зависят от экрана — отображение зависит.")''')
    nb.write(OUT_DIR / "19-26-chistaya-logika.ipynb")
    print(f"Записано: 19-26 ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-27", "GameState с dataclass", "19-27-gamestate-dataclass.html"))
    nb.md("## Цель\n\nСоздавать, сравнивать и обновлять GameState как обычный dataclass.")
    nb.md("## Рабочий пример")
    nb.code('''from dataclasses import dataclass, field, replace

@dataclass
class GameState:
    snake: list
    score: int = 0
    high_score: int = 0
    status: str = "ready"

state = GameState(snake=[(0, 0)])
print(state)
state2 = replace(state, score=10)
print(state2)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''a = GameState(snake=[(0, 0)], score=10)
b = GameState(snake=[(0, 0)], score=10)
assert a == b   # dataclass сравнивается по значениям полей

c = replace(a, status="running")
assert c.status == "running"
assert c.score == 10   # остальные поля не изменились
assert a.status == "ready"   # replace() не мутирует исходный объект
print("GameState ведёт себя как обычные данные — сравнение и replace() работают предсказуемо.")''')
    nb.write(OUT_DIR / "19-27-gamestate-dataclass.ipynb")
    print(f"Записано: 19-27 ({len(nb)} ячеек)")


def build_30() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-30", "Тестируем правила игры", "19-30-testiruem-pravila.html"))
    nb.md("## Цель\n\nНаписать тест, который ловит намеренно сломанную версию функции.")
    nb.md("## Рабочий пример")
    nb.code('''def is_wall_collision(head, half=280):
    x, y = head
    return abs(x) > half or abs(y) > half

def is_wall_collision_BROKEN(head, half=280):
    x, y = head
    return abs(x) >= half or abs(y) >= half   # >=, не > — раздел 19.31, Debug Lab 11

def test_boundary_is_safe(fn):
    return fn((280, 0)) is False

print(test_boundary_is_safe(is_wall_collision))
print(test_boundary_is_safe(is_wall_collision_BROKEN))''')
    nb.md("## Задание ★★ Найдите, какая версия ломает тест")
    nb.code('''assert test_boundary_is_safe(is_wall_collision) is True
assert test_boundary_is_safe(is_wall_collision_BROKEN) is False
print("Тест на границе ловит ошибку >= там, где нужно строгое >.")''')
    nb.write(OUT_DIR / "19-30-testiruem-pravila.ipynb")
    print(f"Записано: 19-30 ({len(nb)} ячеек)")


def build_31() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-31", "Debug Labs", "19-31-debug-labs.html"))
    nb.md("## Цель\n\nПо симптому определить, какая часть игры сломана.")
    nb.md("## Рабочий пример")
    nb.code('''SYMPTOMS = {
    "змейка мгновенно врезается в себя при развороте": "is_reverse не проверяется",
    "окно не реагирует на клавиши несколько секунд": "time.sleep() в игровом цикле",
    "после Restart появляется фигура из прошлой игры": "нет generation guard",
    "оверлей ПАУЗА показан, но змейка всё равно едет": "status не проверяется в game_tick",
}

def diagnose(symptom):
    return SYMPTOMS.get(symptom, "неизвестный симптом")

print(diagnose("окно не реагирует на клавиши несколько секунд"))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert diagnose("змейка мгновенно врезается в себя при развороте") == "is_reverse не проверяется"
assert diagnose("после Restart появляется фигура из прошлой игры") == "нет generation guard"
print("Симптом уверенно указывает на конкретную причину — раздел 19.31 разбирает все случаи.")''')
    nb.write(OUT_DIR / "19-31-debug-labs.ipynb")
    print(f"Записано: 19-31 ({len(nb)} ячеек)")


# ---------------------------------------------------------------------------
# local-required: нужен настоящий экран Turtle
# ---------------------------------------------------------------------------

def build_13() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-13", "Настоящий игровой цикл", "19-13-nastoyaschij-cikl.html"))
    nb.md("## Цель\n\nЗапустить цепочку тиков через screen.ontimer() вместо busy-цикла.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''golova = turtle.Turtle()
golova.speed(0)
golova.shape("square")
golova.penup()
golova.goto(0, 0)

tiki = []

def game_tick():
    golova.setx(golova.xcor() + RAZMER_SHAGA)
    tiki.append(golova.xcor())
    screen.update()
    if len(tiki) < 3:
        screen.ontimer(game_tick, 200)

game_tick()
screen.update()
print("Первый тик выполнен, остальные два запланированы через ontimer().")''')
    nb.md("## Эксперимент 1 — подождать, пока сработают запланированные тики")
    nb.code('''screen.update()
print("tiki пока:", tiki)
print("Запустите эту ячейку ещё раз через секунду, чтобы увидеть остальные тики.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-13-nastoyaschij-cikl.ipynb")
    print(f"Записано: 19-13 ({len(nb)} ячеек)")


def build_28() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-28", "SnakeApp: отделяем модель от визуализации", "19-28-snakeapp-arhitektura.html"))
    nb.md("## Цель\n\nСобрать мини-объект приложения: state отдельно от Turtle-виджетов.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''class MiniSnakeApp:
    def __init__(self):
        self.state = {"snake": [(0, 0)], "score": 0}
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.penup()

    def render(self):
        self.head.goto(*self.state["snake"][0])
        screen.update()

app = MiniSnakeApp()
app.state["snake"] = [(40, 0)]
app.render()
print("app.state — обычный словарь; app.head — единственный Turtle-объект.")''')
    nb.md("## Проверка результата")
    nb.code('''assert app.state["snake"] == [(40, 0)]
assert isinstance(app.head, turtle.Turtle)
assert app.head.position() == (40.0, 0.0)
print("Модель (state) и виджет (head) — разные атрибуты, не одно и то же.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-28-snakeapp-arhitektura.ipynb")
    print(f"Записано: 19-28 ({len(nb)} ячеек)")


def build_29() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-29", "Render: модель → Turtle", "19-29-render-model.html"))
    nb.md("## Цель\n\nrender() переиспользует существующие Turtle-сегменты вместо создания новых.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''segment_pool = []

def ensure_pool(needed):
    while len(segment_pool) < needed:
        seg = turtle.Turtle()
        seg.speed(0)
        seg.shape("square")
        seg.color("grey")
        seg.penup()
        segment_pool.append(seg)

def render(body):
    ensure_pool(len(body))
    for i, seg in enumerate(segment_pool):
        if i < len(body):
            seg.showturtle()
            seg.goto(*body[i])
        else:
            seg.hideturtle()
    screen.update()

render([(-20, 0), (-40, 0)])
print("Сегментов в пуле:", len(segment_pool))''')
    nb.md("## Эксперимент 1 — змейка укоротилась, лишний сегмент прячется")
    nb.code('''render([(-20, 0)])
assert segment_pool[0].isvisible() is True
assert segment_pool[1].isvisible() is False
print("Лишний сегмент спрятан, а не удалён — пул готов вырасти снова без пересоздания.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "19-29-render-model.ipynb")
    print(f"Записано: 19-29 ({len(nb)} ячеек)")


def build_32() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("19-32", "Snake Pro целиком", "19-32-snake-pro-itogi.html") +
          " Тот же код, что и в `projects/turtle/snake/snake.py`.")
    nb.md("## Цель\n\nЗапустить настоящий SnakeApp и провести его через несколько тиков без реального таймера.")
    nb.md("## Настройка (SnakeApp сам открывает свой экран — отдельно ничего настраивать не нужно)")
    nb.code('''import random
import sys
sys.path.insert(0, "../../projects/turtle/snake")
import snake as s

app = s.SnakeApp(rng=random.Random(11))
print("Статус при создании:", app.state.status)''')
    nb.md("## Рабочий пример")
    nb.code('''app.request_direction(s.Direction.RIGHT)   # READY -> RUNNING
app.state.food = s.next_head(app.state.snake[0], s.Direction.RIGHT)
app.game_tick()
print("Счёт:", app.state.score, "| Длина змейки:", len(app.state.snake))''')
    nb.md("## Проверка результата")
    nb.code('''assert app.state.status is s.GameStatus.RUNNING
assert app.state.score == 10
assert len(app.state.snake) == 2
print("Настоящий SnakeApp работает без единого вызова screen.mainloop().")''')
    nb.md("## Завершение (выполнить один раз, в самом конце)")
    nb.code('''app.screen.bye()
print("Окно закрыто.")''')
    nb.write(OUT_DIR / "19-32-snake-pro-itogi.ipynb")
    print(f"Записано: 19-32 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_02()
    build_03()
    build_04()
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
    build_27()
    build_28()
    build_29()
    build_30()
    build_31()
    build_32()
