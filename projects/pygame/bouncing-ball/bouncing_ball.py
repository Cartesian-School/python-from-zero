"""Мини-проект «Прыгающий мяч Pro» на Pygame — финальная версия.

Проект к разделу 20.33 книги «Python с нуля» (Cartesian School). Та же идея,
что и у bouncing_ball_basic.py (раздел 20.5), но пересобранная с архитектурой
класса Game (раздел 20.26): движение считается через delta time и не зависит
от FPS конкретного устройства (раздел 20.16), есть пауза, рестарт без
перезапуска процесса, необязательный толчок мяча кликом мыши, счёт очков и
необязательный звук отскока.

Управление: P — пауза/продолжить, R — начать заново, клик мышью — толкнуть
мяч в сторону клика.

Запуск: python bouncing_ball.py
"""

import math
import random
from enum import Enum, auto
from pathlib import Path

import pygame

SHIRINA, VYSOTA = 600, 400
RADIUS = 20
FPS = 60
NACHALNAYA_SKOROST = 220.0  # пикселей в секунду — не зависит от FPS (раздел 20.16)
OCHKOV_ZA_OTSKOK = 10

BASE_DIR = Path(__file__).resolve().parent

CVET_FONA = (20, 20, 40)
CVET_MYACHA = (255, 100, 100)
CVET_TEKSTA = (240, 240, 250)
CVET_PAUZY = (255, 210, 90)


class SostoyanieIgry(Enum):
    """Состояния этой мини-игры (раздел 20.25). MENU и GAME_OVER — упражнение
    в конце раздела 20.33, здесь показаны только IGRA и PAUZA."""

    IGRA = auto()
    PAUZA = auto()


def normalizovat(vx: float, vy: float) -> tuple[float, float]:
    """Возвращает единичный вектор того же направления, что (vx, vy), или
    (0, 0), если вектор нулевой.

    Нужен толчку мышью: без нормализации итоговая скорость мяча после клика
    зависела бы от того, насколько далеко от мяча кликнул игрок, — та же
    ошибка "ненормализованного вектора", что и с диагональным движением в
    разделе 20.16, только на этот раз с направлением на точку клика.
    """
    dlina = math.hypot(vx, vy)
    if dlina == 0:
        return 0.0, 0.0
    return vx / dlina, vy / dlina


class BouncingBallGame:
    """Прыгающий мяч с архитектурой Game (раздел 20.26):
    handle_events -> update(dt) -> render -> run.
    """

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SHIRINA, VYSOTA))
        pygame.display.set_caption("Прыгающий мяч Pro")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.running = True
        self.state = SostoyanieIgry.IGRA
        self.zvuk_otskoka = self._zagruzit_zvuk()
        self._reset_myach()

    def _zagruzit_zvuk(self) -> "pygame.mixer.Sound | None":
        """Пытается подготовить звук отскока. Аудиоустройство может быть
        недоступно (например, в headless-окружении CI без звуковой карты) —
        в этом случае игра обязана продолжать работать молча, а не падать."""
        try:
            pygame.mixer.init()
            put = BASE_DIR / "assets" / "otskok.wav"
            if put.exists():
                return pygame.mixer.Sound(str(put))
        except pygame.error:
            pass
        return None

    def _reset_myach(self) -> None:
        self.x, self.y = SHIRINA / 2, VYSOTA / 2
        ugol = random.uniform(0, 2 * math.pi)
        self.vx = NACHALNAYA_SKOROST * math.cos(ugol)
        self.vy = NACHALNAYA_SKOROST * math.sin(ugol)
        self.otskokov = 0
        self.schet = 0

    def toggle_pause(self) -> None:
        self.state = SostoyanieIgry.PAUZA if self.state is SostoyanieIgry.IGRA else SostoyanieIgry.IGRA

    def tolknut_k_tochke(self, tx: float, ty: float) -> None:
        """Необязательное взаимодействие мышью: разворачивает скорость мяча
        в сторону точки клика, сохраняя её прежнюю величину."""
        nx, ny = normalizovat(tx - self.x, ty - self.y)
        if nx == 0 and ny == 0:
            return
        skorost = math.hypot(self.vx, self.vy)
        self.vx, self.vy = nx * skorost, ny * skorost

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()
                elif event.key == pygame.K_r:
                    self._reset_myach()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.state is SostoyanieIgry.IGRA:
                self.tolknut_k_tochke(*event.pos)

    def update(self, dt: float) -> None:
        if self.state is not SostoyanieIgry.IGRA:
            return   # на паузе физика не обновляется (раздел 20.26)

        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x - RADIUS < 0 or self.x + RADIUS > SHIRINA:
            self.vx = -self.vx
            self.x = max(RADIUS, min(self.x, SHIRINA - RADIUS))
            self._na_otskok()

        if self.y - RADIUS < 0 or self.y + RADIUS > VYSOTA:
            self.vy = -self.vy
            self.y = max(RADIUS, min(self.y, VYSOTA - RADIUS))
            self._na_otskok()

    def _na_otskok(self) -> None:
        self.otskokov += 1
        self.schet += OCHKOV_ZA_OTSKOK
        if self.zvuk_otskoka is not None:
            self.zvuk_otskoka.play()

    def render(self) -> None:
        self.screen.fill(CVET_FONA)
        pygame.draw.circle(self.screen, CVET_MYACHA, (int(self.x), int(self.y)), RADIUS)

        tekst = self.font.render(f"Счёт: {self.schet}   Отскоков: {self.otskokov}", True, CVET_TEKSTA)
        self.screen.blit(tekst, (12, 10))

        if self.state is SostoyanieIgry.PAUZA:
            pauza = self.font.render("ПАУЗА — P, чтобы продолжить", True, CVET_PAUZY)
            rect = pauza.get_rect(center=(SHIRINA // 2, VYSOTA // 2))
            self.screen.blit(pauza, rect)

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.render()
        pygame.quit()


if __name__ == "__main__":
    BouncingBallGame().run()
