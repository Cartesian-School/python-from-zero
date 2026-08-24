"""Мини-проект «Отскакивающий от четырёх стен мяч» — версия с классом.

Домашняя практика к главе 23 книги «Python с нуля» (Cartesian School).
В отличие от версии из главы 20 (одна переменная-мяч, отдельные функции), здесь мяч
описан классом Myach (глава 15) — это позволяет легко завести сразу несколько мячей
как список объектов.

Запуск: python bouncing_balls.py

Импорт этого файла не открывает окно: pygame.init() и создание окна происходят
только внутри main(). Позиция и скорость мяча — pygame.Vector2, скорость задана
в пикселях в секунду, а Myach.shag(dt) двигает мяч на dt секунд вперёд. Поэтому
смещение мяча за одну и ту же секунду одинаково независимо от FPS — тот же
принцип delta time, что и в разделе 20.16.
"""

from __future__ import annotations

import pygame
from pygame import Vector2

SHIRINA, VYSOTA = 600, 400
FPS = 60

CVET_FONA = (20, 20, 40)
CVETA_MYACHEJ = [(255, 100, 100), (100, 200, 255), (150, 255, 150)]


class Myach:
    """Один мяч: позиция и скорость — pygame.Vector2 (скорость в пикселях
    в секунду), радиус и цвет. Класс не создаёт окно и не хранит
    поверхность для рисования — это позволяет вызывать shag() в тестах
    без дисплея."""

    def __init__(self, x: float, y: float, vx: float, vy: float, radius: int, cvet: tuple[int, int, int]) -> None:
        self.pos = Vector2(x, y)
        self.velocity = Vector2(vx, vy)
        self.radius = radius
        self.cvet = cvet
        self.otskokov = 0

    def shag(self, dt: float) -> None:
        """Двигает мяч на dt секунд вперёд и отражает его от стен."""
        self.pos += self.velocity * dt

        if self.pos.x - self.radius < 0 or self.pos.x + self.radius > SHIRINA:
            self.velocity.x = -self.velocity.x
            self.pos.x = max(self.radius, min(self.pos.x, SHIRINA - self.radius))
            self.otskokov += 1

        if self.pos.y - self.radius < 0 or self.pos.y + self.radius > VYSOTA:
            self.velocity.y = -self.velocity.y
            self.pos.y = max(self.radius, min(self.pos.y, VYSOTA - self.radius))
            self.otskokov += 1

    def narisovat(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.cvet, (int(self.pos.x), int(self.pos.y)), self.radius)


def sozdat_myachi(kolichestvo: int = 3) -> list[Myach]:
    myachi = []
    for i in range(kolichestvo):
        myach = Myach(
            x=SHIRINA // 2,
            y=VYSOTA // 2,
            vx=120 + 30 * i,  # пикселей в секунду
            vy=90 + 30 * i,
            radius=15,
            cvet=CVETA_MYACHEJ[i % len(CVETA_MYACHEJ)],
        )
        myachi.append(myach)
    return myachi


def narisovat_kadr(screen: pygame.Surface, myachi: list[Myach]) -> None:
    screen.fill(CVET_FONA)
    for myach in myachi:
        myach.narisovat(screen)
    pygame.display.flip()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SHIRINA, VYSOTA))
    pygame.display.set_caption("Отскакивающие мячи")
    clock = pygame.time.Clock()

    myachi = sozdat_myachi()
    rabotaet = True
    while rabotaet:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rabotaet = False

        for myach in myachi:
            myach.shag(dt)
        narisovat_kadr(screen, myachi)

    pygame.quit()


if __name__ == "__main__":
    main()
