"""Мини-проект «Прыгающий мяч» на Pygame — первый, учебный прототип.

Проект к разделу 20.5 книги «Python с нуля» (Cartesian School).
Движение здесь считается «пикселей за кадр» — простое решение для первого
знакомства с игровым циклом (раздел 20.2), но зависящее от FPS конкретного
устройства (раздел 20.16 объясняет, почему, и раздел 20.33 показывает
профессионально организованную версию этого же проекта — bouncing_ball.py).

Запуск: python bouncing_ball_basic.py
"""

import pygame

SHIRINA, VYSOTA = 600, 400
RADIUS = 20
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SHIRINA, VYSOTA))
pygame.display.set_caption("Прыгающий мяч")
clock = pygame.time.Clock()

# позиция и скорость мяча
x, y = SHIRINA // 2, VYSOTA // 2
dx, dy = 4, 3

CVET_FONA = (20, 20, 40)
CVET_MYACHA = (255, 100, 100)


def shag_fiziki(x, y, dx, dy):
    """Один шаг физики: новая позиция и скорость после отскоков от стен."""
    x += dx
    y += dy

    if x - RADIUS < 0 or x + RADIUS > SHIRINA:
        dx = -dx
        x = max(RADIUS, min(x, SHIRINA - RADIUS))

    if y - RADIUS < 0 or y + RADIUS > VYSOTA:
        dy = -dy
        y = max(RADIUS, min(y, VYSOTA - RADIUS))

    return x, y, dx, dy


def narisovat_kadr(x, y):
    screen.fill(CVET_FONA)
    pygame.draw.circle(screen, CVET_MYACHA, (int(x), int(y)), RADIUS)
    pygame.display.flip()


def glavnyj_cikl():
    global x, y, dx, dy
    rabotaet = True
    while rabotaet:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rabotaet = False

        x, y, dx, dy = shag_fiziki(x, y, dx, dy)
        narisovat_kadr(x, y)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    glavnyj_cikl()
