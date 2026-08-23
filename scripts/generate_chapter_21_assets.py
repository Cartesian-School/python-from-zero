#!/usr/bin/env python3
"""Генерирует ОРИГИНАЛЬНЫЕ игровые ассеты для проекта «Космический шутер»
(глава 21): изображения кораблей/пуль/взрыва как прозрачные PNG и звуковые
эффекты как WAV.

Все формы нарисованы вручную через pygame.draw(...) на Surface с флагом
SRCALPHA — простые геометрические фигуры без внешних изображений и без
сети, ни один существующий коммерческий спрайт (Space Invaders, Galaga,
Star Wars и подобные) не копируется. Звуки — короткие синтезированные
сигналы (синус/шум с затуханием), собранные вручную через встроенный
модуль wave, без сторонних библиотек и без сети.

Использование: .venv/bin/python3 scripts/generate_chapter_21_assets.py
"""

import math
import os
import random
import wave
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = ROOT / "projects" / "pygame" / "space-shooter"
IMAGE_DIR = GAME_DIR / "assets" / "images"
AUDIO_DIR = GAME_DIR / "assets" / "audio"

pygame.init()
pygame.display.set_mode((1, 1))


def novaya_poverhnost(size: tuple[int, int]) -> pygame.Surface:
    return pygame.Surface(size, pygame.SRCALPHA)


def sohranit(surface: pygame.Surface, name: str) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGE_DIR / f"{name}.png"
    pygame.image.save(surface, str(path))
    print(f"Сохранено: {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Корабль игрока — 44x44, сине-голубой, нос вверх
# ---------------------------------------------------------------------------

def sprite_player_ship() -> None:
    w, h = 44, 44
    surf = novaya_poverhnost((w, h))

    korpus = (60, 170, 255)
    svetlyj = (170, 225, 255)
    dvigatel = (255, 180, 90)

    # Корпус — стреловидный силуэт, нос вверх
    pygame.draw.polygon(
        surf,
        korpus,
        [(22, 2), (36, 30), (28, 26), (28, 38), (16, 38), (16, 26), (8, 30)],
    )
    # Светлая полоса-кабина ближе к носу
    pygame.draw.polygon(surf, svetlyj, [(22, 8), (27, 22), (17, 22)])
    # Тонкая обводка корпуса для контраста с тёмным фоном игры
    pygame.draw.polygon(
        surf,
        (20, 60, 110),
        [(22, 2), (36, 30), (28, 26), (28, 38), (16, 38), (16, 26), (8, 30)],
        width=2,
    )
    # Свечение двигателя внизу
    pygame.draw.ellipse(surf, dvigatel, (16, 36, 12, 8))

    sohranit(surf, "player_ship")


# ---------------------------------------------------------------------------
# Враг «разведчик» (scout) — маленький, быстрый, оранжево-красный, нос вниз
# ---------------------------------------------------------------------------

def sprite_enemy_scout() -> None:
    w, h = 32, 28
    surf = novaya_poverhnost((w, h))

    korpus = (255, 110, 80)
    temnyj = (150, 40, 30)

    pygame.draw.polygon(surf, korpus, [(4, 2), (28, 2), (16, 26)])
    pygame.draw.polygon(surf, temnyj, [(4, 2), (28, 2), (16, 26)], width=2)
    pygame.draw.circle(surf, (255, 220, 190), (16, 10), 4)

    sohranit(surf, "enemy_scout")


# ---------------------------------------------------------------------------
# Враг «истребитель» (fighter) — крупнее, медленнее, пурпурно-красный
# ---------------------------------------------------------------------------

def sprite_enemy_fighter() -> None:
    w, h = 46, 40
    surf = novaya_poverhnost((w, h))

    korpus = (200, 50, 90)
    temnyj = (110, 20, 45)
    podsvetka = (255, 150, 170)

    pygame.draw.polygon(
        surf,
        korpus,
        [(23, 4), (40, 20), (34, 20), (30, 36), (16, 36), (12, 20), (6, 20)],
    )
    pygame.draw.polygon(
        surf,
        temnyj,
        [(23, 4), (40, 20), (34, 20), (30, 36), (16, 36), (12, 20), (6, 20)],
        width=2,
    )
    # Боковые модули (пилоны)
    pygame.draw.circle(surf, temnyj, (8, 22), 5)
    pygame.draw.circle(surf, temnyj, (38, 22), 5)
    pygame.draw.circle(surf, podsvetka, (23, 16), 4)

    sohranit(surf, "enemy_fighter")


# ---------------------------------------------------------------------------
# Пуля — маленькая яркая капсула
# ---------------------------------------------------------------------------

def sprite_bullet() -> None:
    w, h = 6, 18
    surf = novaya_poverhnost((w, h))

    pygame.draw.rect(surf, (255, 240, 120), (0, 0, w, h), border_radius=3)
    pygame.draw.rect(surf, (255, 255, 210), (1, 1, w - 2, h // 2), border_radius=2)

    sohranit(surf, "bullet")


# ---------------------------------------------------------------------------
# Спрайт-лист взрыва — 6 кадров 48x48 в ряд, расширяющаяся вспышка
# ---------------------------------------------------------------------------

def sprite_explosion_sheet() -> None:
    frame = 48
    kadrov = 6
    sheet = novaya_poverhnost((frame * kadrov, frame))

    for i in range(kadrov):
        progress = i / (kadrov - 1)   # 0.0 в начале, 1.0 в конце
        cx = i * frame + frame // 2
        cy = frame // 2

        # Внешнее кольцо расширяется и тускнеет к концу анимации
        outer_radius = int(6 + progress * 18)
        outer_alpha = int(255 * (1.0 - progress) ** 1.3)
        pygame.draw.circle(sheet, (255, 140, 40, outer_alpha), (cx, cy), outer_radius)

        # Среднее кольцо — оранжевое, чуть меньше и ярче
        mid_radius = max(1, int(outer_radius * 0.7))
        mid_alpha = int(255 * (1.0 - progress) ** 1.0)
        pygame.draw.circle(sheet, (255, 190, 70, mid_alpha), (cx, cy), mid_radius)

        # Яркое жёлто-белое ядро, самое заметное в первых кадрах
        core_radius = max(1, int(outer_radius * 0.35 * (1.0 - progress * 0.8)))
        core_alpha = int(255 * (1.0 - progress) ** 0.6)
        pygame.draw.circle(sheet, (255, 250, 210, core_alpha), (cx, cy), core_radius)

    sohranit(sheet, "explosion_sheet")


# ---------------------------------------------------------------------------
# Звуки — короткие синтезированные WAV без сторонних библиотек
# ---------------------------------------------------------------------------

SAMPLE_RATE = 22050


def _wav_zapisat(name: str, samples: list[float]) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    path = AUDIO_DIR / f"{name}.wav"
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        kadry = bytearray()
        for s in samples:
            znachenie = max(-1.0, min(1.0, s))
            kadry += int(znachenie * 32767).to_bytes(2, byteorder="little", signed=True)
        wav_file.writeframes(bytes(kadry))
    print(f"Сохранено: {path.relative_to(ROOT)}")


def _envelope(i: int, total: int) -> float:
    """Линейное затухание к концу звука — без него звук обрывается щелчком."""
    return max(0.0, 1.0 - i / total)


def zvuk_lazera() -> None:
    dlitelnost = 0.18
    total = int(SAMPLE_RATE * dlitelnost)
    samples = []
    for i in range(total):
        t = i / SAMPLE_RATE
        chastota = 1200 - 900 * (i / total)   # нисходящий свист
        samples.append(0.5 * math.sin(2 * math.pi * chastota * t) * _envelope(i, total))
    _wav_zapisat("laser", samples)


def zvuk_vzryva() -> None:
    dlitelnost = 0.35
    total = int(SAMPLE_RATE * dlitelnost)
    rng = random.Random(21)
    samples = []
    for i in range(total):
        shum = rng.uniform(-1.0, 1.0)
        samples.append(0.6 * shum * _envelope(i, total) ** 1.5)
    _wav_zapisat("explosion", samples)


def zvuk_popadaniya() -> None:
    dlitelnost = 0.22
    total = int(SAMPLE_RATE * dlitelnost)
    samples = []
    for i in range(total):
        t = i / SAMPLE_RATE
        osnova = math.sin(2 * math.pi * 130 * t)
        prizvuk = 0.3 * math.sin(2 * math.pi * 90 * t)
        samples.append(0.6 * (osnova + prizvuk) * _envelope(i, total))
    _wav_zapisat("player_hit", samples)


IMAGE_SCENES = [
    sprite_player_ship,
    sprite_enemy_scout,
    sprite_enemy_fighter,
    sprite_bullet,
    sprite_explosion_sheet,
]

AUDIO_SCENES = [
    zvuk_lazera,
    zvuk_vzryva,
    zvuk_popadaniya,
]


if __name__ == "__main__":
    for scene in IMAGE_SCENES:
        scene()
    for scene in AUDIO_SCENES:
        scene()
    pygame.quit()
    print("Готово.")
