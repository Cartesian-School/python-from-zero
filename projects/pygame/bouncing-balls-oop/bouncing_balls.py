"""Мини-проект «Отскакивающий от четырёх стен мяч» — версия с классом.

Проект к главе 23 книги «Python с нуля» (Cartesian School).
В отличие от версии из главы 20 (одна переменная-мяч, отдельные функции), здесь мяч
описан классом Myach (глава 15) — это позволяет легко завести сразу несколько мячей
как список объектов.

Запуск: python bouncing_balls.py
"""

import pygame

SHIRINA, VYSOTA = 600, 400
FPS = 60

CVET_FONA = (20, 20, 40)
CVETA_MYACHEJ = [(255, 100, 100), (100, 200, 255), (150, 255, 150)]

pygame.init()
screen = pygame.display.set_mode((SHIRINA, VYSOTA))
pygame.display.set_caption("Отскакивающие мячи")
clock = pygame.time.Clock()


class Myach:
    """Один мяч: своя позиция, скорость, радиус и цвет."""

    def __init__(self, x, y, dx, dy, radius, cvet):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.cvet = cvet
        self.otskokov = 0

    def shag(self):
        """Двигает мяч на один кадр вперёд и отражает его от стен."""
        self.x += self.dx
        self.y += self.dy

        if self.x - self.radius < 0 or self.x + self.radius > SHIRINA:
            self.dx = -self.dx
            self.x = max(self.radius, min(self.x, SHIRINA - self.radius))
            self.otskokov += 1

        if self.y - self.radius < 0 or self.y + self.radius > VYSOTA:
            self.dy = -self.dy
            self.y = max(self.radius, min(self.y, VYSOTA - self.radius))
            self.otskokov += 1

    def narisovat(self):
        pygame.draw.circle(screen, self.cvet, (int(self.x), int(self.y)), self.radius)


def sozdat_myachi(kolichestvo=3):
    myachi = []
    for i in range(kolichestvo):
        myach = Myach(
            x=SHIRINA // 2,
            y=VYSOTA // 2,
            dx=4 + i,
            dy=3 + i,
            radius=15,
            cvet=CVETA_MYACHEJ[i % len(CVETA_MYACHEJ)],
        )
        myachi.append(myach)
    return myachi


def narisovat_kadr(myachi):
    screen.fill(CVET_FONA)
    for myach in myachi:
        myach.narisovat()
    pygame.display.flip()


def glavnyj_cikl():
    myachi = sozdat_myachi()
    rabotaet = True
    while rabotaet:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rabotaet = False

        for myach in myachi:
            myach.shag()
        narisovat_kadr(myachi)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    glavnyj_cikl()
