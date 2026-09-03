"""Игра «Змейка» на Turtle — первый прототип (главы 19.1–19.8).

Состояние живёт в глобальных переменных, тело — в списке Turtle-сегментов,
игровой цикл — обычный while с screen.update() и time.sleep() внутри.
Сознательный выбор для первой версии (см. раздел 19.26). Финальная
архитектура с GameState, игровым тиком на screen.ontimer() и разделением
модели и отображения — в snake.py.

time.sleep() здесь допустим ровно потому, что цикл и так блокирующий:
пока он крутится, ничего другого в программе не происходит, а
screen.update() в конце каждого шага успевает разобрать накопившиеся
события клавиатуры. В архитектуре на screen.ontimer() (раздел 19.13) тот
же самый sleep уже становится ошибкой — см. Debug Lab 4 в разделе 19.31.

Проект к главе 19 книги «Python с нуля» (Cartesian School).
Запуск: python snake_basic.py
"""

import random
import time
import turtle

RAZMER_SHAGA = 20
GRANICA = 280
ZADERZHKA_SEK = 0.12  # пауза между шагами: без неё игра закончилась бы за миллисекунды

# --- экран ---
screen = turtle.Screen()
screen.title("Змейка")
screen.bgcolor("black")
screen.setup(width=600, height=600, startx=0, starty=0)
screen.tracer(0)  # отключаем автообновление — обновляем экран вручную

# --- переменные состояния игры ---
napravlenie = "stop"
schet = 0
igra_okonchena = False

# --- голова змейки ---
golova = turtle.Turtle()
golova.speed(0)
golova.shape("square")
golova.color("white")
golova.penup()
golova.goto(0, 0)

# --- яблоко ---
yabloko = turtle.Turtle()
yabloko.speed(0)
yabloko.shape("circle")
yabloko.color("red")
yabloko.penup()

# --- табло счёта ---
tablo = turtle.Turtle()
tablo.speed(0)
tablo.color("white")
tablo.penup()
tablo.hideturtle()
tablo.goto(0, 260)

segmenty = []  # тело змейки — список дополнительных turtle-сегментов


def novoe_yabloko():
    # GRANICA + RAZMER_SHAGA, а не GRANICA: у randrange правая граница
    # исключается, поэтому без этого яблоко никогда не попало бы в крайний
    # легальный ряд клеток (+280), куда змейка спокойно доезжает.
    x = random.randrange(-GRANICA, GRANICA + RAZMER_SHAGA, RAZMER_SHAGA)
    y = random.randrange(-GRANICA, GRANICA + RAZMER_SHAGA, RAZMER_SHAGA)
    yabloko.goto(x, y)


def obnovit_tablo():
    tablo.clear()
    tablo.write(f"Счёт: {schet}", align="center", font=("Arial", 16, "normal"))


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


def poziciya_za_golovoj():
    """Клетка прямо позади головы — туда встаёт самый первый сегмент тела."""
    x = golova.xcor()
    y = golova.ycor()
    if napravlenie == "up":
        return x, y - RAZMER_SHAGA
    elif napravlenie == "down":
        return x, y + RAZMER_SHAGA
    elif napravlenie == "left":
        return x + RAZMER_SHAGA, y
    else:
        return x - RAZMER_SHAGA, y


def dobavit_segment():
    novyj = turtle.Turtle()
    novyj.speed(0)
    novyj.shape("square")
    novyj.color("grey")
    novyj.penup()
    # Новый сегмент обязательно нужно сразу поставить на место. Иначе он
    # остался бы в (0, 0), и проверка столкновений в этом же шаге увидела бы
    # его под головой (если яблоко было съедено в центре поля) и завершила бы
    # игру. Ставим его в хвост — на следующем шаге dvigat_telo() подтянет его.
    if segmenty:
        x, y = segmenty[-1].position()
    else:
        x, y = poziciya_za_golovoj()
    novyj.goto(x, y)
    segmenty.append(novyj)


def dvigat_telo():
    # каждый сегмент занимает место предыдущего, начиная с хвоста
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

    # столкновение со стеной
    if abs(golova.xcor()) > GRANICA or abs(golova.ycor()) > GRANICA:
        igra_okonchena = True

    # столкновение с собственным телом
    for segment in segmenty:
        if segment.distance(golova) < RAZMER_SHAGA / 2:
            igra_okonchena = True


def igrovoj_shag():
    """Один шаг игры: движение, проверка еды и столкновений. Возвращает True, пока игра идёт."""
    if igra_okonchena:
        return False

    dvigat_telo()
    dvigat_golovu()
    proverit_edu()
    proverit_stolknoveniya()
    screen.update()
    return not igra_okonchena


screen.listen()
screen.onkeypress(idti_vverh, "Up")
screen.onkeypress(idti_vniz, "Down")
screen.onkeypress(idti_vlevo, "Left")
screen.onkeypress(idti_vpravo, "Right")

novoe_yabloko()
obnovit_tablo()


def glavnyj_cikl():
    """Настоящий игровой цикл — используется только при прямом запуске файла."""
    global napravlenie
    napravlenie = "right"
    while igrovoj_shag():
        screen.update()
        time.sleep(ZADERZHKA_SEK)   # без паузы игра закончилась бы за миллисекунды
    tablo.goto(0, 0)
    tablo.write(f"Игра окончена! Счёт: {schet}", align="center", font=("Arial", 20, "bold"))


if __name__ == "__main__":
    glavnyj_cikl()
    screen.exitonclick()
