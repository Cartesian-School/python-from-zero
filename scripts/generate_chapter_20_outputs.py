#!/usr/bin/env python3
"""Генерирует РЕАЛЬНЫЕ скриншоты Pygame для главы 20.

Каждый кадр — это настоящий pygame.draw(...) поверх настоящей Surface,
сохранённый через pygame.image.save(). Никаких нарисованных Pillow
"поддельных окон": Pillow здесь используется только для того, чтобы СКЛЕИТЬ
уже готовые реальные кадры в сравнительные полосы (см. _polosa()) — так же,
как в generate_chapter_19_outputs.py.

Рендеринг идёт через headless-драйвер SDL "dummy": pygame.display.set_mode()
всё равно возвращает настоящую Surface, на которой работают все обычные
вызовы pygame.draw/blit, а pygame.image.save() сохраняет её напрямую в PNG —
никакого реального окна или X-сервера для этого не требуется в принципе,
поэтому единственное, что нужно — обычный Python (без Xvfb), но Xvfb
одинаково безопасно совместим с этим драйвером и не мешает.

Использование: .venv/bin/python3 scripts/generate_chapter_20_outputs.py
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import sys
from pathlib import Path

import pygame
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-20" / "output"
BALL_DIR = ROOT / "projects" / "pygame" / "bouncing-ball"
sys.path.insert(0, str(BALL_DIR))

SHIRINA, VYSOTA = 600, 400
CVET_FONA = (20, 20, 40)

pygame.init()
FONT = pygame.font.SysFont(None, 26)


def novyj_ekran():
    return pygame.display.set_mode((SHIRINA, VYSOTA))


def sohranit(surface, name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    pygame.image.save(surface, str(path))
    print(f"Сохранено: {path.relative_to(ROOT)}")
    return path


MAKS_SHIRINA_POLOSY = 800   # компактный размер сравнительной полосы на странице


def _polosa(names, out_name):
    """Склеивает уже сохранённые реальные кадры в одну горизонтальную полосу
    сравнения — сама склейка не рисует ничего нового, только компонует
    существующие PNG рядом, а затем сжимает итоговую полосу до компактной
    ширины (страница не должна тянуть несколько полноразмерных кадров)."""
    images = [Image.open(OUT_DIR / f"{n}.png") for n in names]
    zazor = 16
    w = sum(im.width for im in images) + zazor * (len(images) - 1)
    h = max(im.height for im in images)
    strip = Image.new("RGB", (w, h), (245, 244, 250))
    x = 0
    for im in images:
        strip.paste(im, (x, 0))
        x += im.width + zazor
    if strip.width > MAKS_SHIRINA_POLOSY:
        koef = MAKS_SHIRINA_POLOSY / strip.width
        strip = strip.resize((MAKS_SHIRINA_POLOSY, round(strip.height * koef)), Image.LANCZOS)
    path = OUT_DIR / f"{out_name}.png"
    strip.save(path)
    print(f"Сохранена полоса: {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# 20.2 — первый экран и игровой цикл
# ---------------------------------------------------------------------------

def scene_pervoe_okno():
    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    pygame.display.flip()
    sohranit(screen, "pygame-first-window")


def scene_cikl_kvadrat():
    screen = novyj_ekran()
    x = 40
    for _ in range(30):
        screen.fill(CVET_FONA)
        pygame.draw.rect(screen, (100, 200, 255), (x, 180, 40, 40))
        pygame.display.flip()
        x += 4
    sohranit(screen, "game-loop-square")


# ---------------------------------------------------------------------------
# 20.3 — персонажи
# ---------------------------------------------------------------------------

def scene_personazhi():
    screen = novyj_ekran()
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 200, 255), (300, 350, 40, 40))
    pygame.draw.circle(screen, (255, 80, 80), (300, 50), 20)
    pygame.display.flip()
    sohranit(screen, "characters-shapes")


def scene_tri_vraga():
    screen = novyj_ekran()
    screen.fill((0, 0, 0))
    for i, cvet in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
        pygame.draw.circle(screen, cvet, (150 + i * 150, 100), 20)
    pygame.display.flip()
    sohranit(screen, "three-enemies")


# ---------------------------------------------------------------------------
# 20.4 — движение
# ---------------------------------------------------------------------------

def scene_dvizhenie():
    x = 40
    for imya, kadrov in (("movement-before", 0), ("movement-mid", 25), ("movement-after", 50)):
        screen = novyj_ekran()
        pos = 40 + 5 * kadrov
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (100, 200, 255), (pos, 180, 40, 40))
        pygame.display.flip()
        sohranit(screen, imya)
    _polosa(["movement-before", "movement-mid", "movement-after"], "movement-strip")


# ---------------------------------------------------------------------------
# 20.5 — прыгающий мяч (базовая версия)
# ---------------------------------------------------------------------------

def scene_myach_basic():
    import bouncing_ball_basic as bb  # noqa: PLC0415 — использует общий дисплей 600x400

    x, y, dx, dy = bb.SHIRINA // 2, bb.VYSOTA // 2, 4, 3
    imena = ["bouncing-ball-basic-1", "bouncing-ball-basic-2", "bouncing-ball-basic-3"]
    for imya in imena:
        for _ in range(40):
            x, y, dx, dy = bb.shag_fiziki(x, y, dx, dy)
        bb.narisovat_kadr(x, y)
        sohranit(bb.screen, imya)
    _polosa(imena, "bouncing-ball-basic-strip")


# ---------------------------------------------------------------------------
# 20.11 — виртуальные элементы управления (мокап)
# ---------------------------------------------------------------------------

def scene_virtualnye_knopki():
    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    # Виртуальный джойстик слева
    pygame.draw.circle(screen, (60, 60, 90), (90, 320), 55)
    pygame.draw.circle(screen, (150, 180, 255), (100, 310), 26)
    # Виртуальные кнопки справа
    pygame.draw.circle(screen, (255, 120, 120), (480, 330), 30)
    pygame.draw.circle(screen, (120, 255, 160), (540, 290), 30)
    pygame.display.flip()
    sohranit(screen, "virtual-controls-mockup")


# ---------------------------------------------------------------------------
# 20.12 — safe area
# ---------------------------------------------------------------------------

def scene_safe_area():
    screen = novyj_ekran()
    screen.fill((10, 10, 20))
    # Полный экран условно "небезопасен" по краям (вырезы/закруглённые углы)
    pygame.draw.rect(screen, (60, 40, 40), (0, 0, SHIRINA, VYSOTA))
    # safe area — отступ 30px со всех сторон
    safe = pygame.Rect(30, 30, SHIRINA - 60, VYSOTA - 60)
    pygame.draw.rect(screen, (25, 60, 40), safe)
    tekst = FONT.render("safe area", True, (200, 255, 220))
    screen.blit(tekst, (safe.centerx - 40, safe.centery - 10))
    pygame.display.flip()
    sohranit(screen, "safe-area-demo")


# ---------------------------------------------------------------------------
# 20.17 — Surface, blit, альфа
# ---------------------------------------------------------------------------

def scene_surface_blit():
    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    sprajt = pygame.Surface((100, 100))
    sprajt.fill((255, 100, 100))
    screen.blit(sprajt, (50, 50))
    pygame.display.flip()
    sohranit(screen, "surface-blit-demo")


def scene_surface_alpha():
    screen = novyj_ekran()
    screen.fill((0, 0, 0))
    sloj = pygame.Surface((150, 150), pygame.SRCALPHA)
    sloj.fill((255, 0, 0, 130))
    screen.blit(sloj, (0, 0))
    pygame.display.flip()
    sohranit(screen, "surface-alpha-demo")


# ---------------------------------------------------------------------------
# 20.21 — столкновения и хитбоксы
# ---------------------------------------------------------------------------

def scene_stolknoveniya():
    for imya, b_pos, sovpadaet in (
        ("collision-overlap", (120, 120), True),
        ("collision-no-overlap", (400, 300), False),
    ):
        screen = novyj_ekran()
        screen.fill((0, 0, 0))
        a = pygame.Rect(100, 100, 60, 60)
        b = pygame.Rect(b_pos[0], b_pos[1], 60, 60)
        pygame.draw.rect(screen, (100, 200, 255), a)
        cvet_b = (255, 210, 90) if a.colliderect(b) else (255, 80, 80)
        pygame.draw.rect(screen, cvet_b, b)
        pygame.display.flip()
        sohranit(screen, imya)


def scene_hitbox_vs_art():
    screen = novyj_ekran()
    screen.fill((0, 0, 0))
    center = (300, 200)
    pygame.draw.circle(screen, (255, 100, 100), center, 40)
    polnyj = pygame.Rect(0, 0, 80, 80)
    polnyj.center = center
    hitboks = polnyj.inflate(-24, -24)
    pygame.draw.rect(screen, (255, 60, 60), polnyj, width=2)
    pygame.draw.rect(screen, (100, 255, 140), hitboks, width=2)
    pygame.display.flip()
    sohranit(screen, "hitbox-vs-art")


# ---------------------------------------------------------------------------
# 20.22 — простая физика (падение под гравитацией)
# ---------------------------------------------------------------------------

def scene_gravitaciya():
    GRAVITACIYA = 900
    y = 40.0
    skorost_y = 0.0
    imena = ["gravity-fall-1", "gravity-fall-2", "gravity-fall-3"]
    for imya in imena:
        for _ in range(15):
            skorost_y += GRAVITACIYA * (1 / 60)
            y += skorost_y * (1 / 60)
            if y > VYSOTA - 40:
                y = VYSOTA - 40
        screen = novyj_ekran()
        screen.fill(CVET_FONA)
        pygame.draw.circle(screen, (255, 180, 90), (300, int(y)), 20)
        pygame.display.flip()
        sohranit(screen, imya)
    _polosa(imena, "gravity-fall-strip")


# ---------------------------------------------------------------------------
# 20.23 — анимация спрайт-листа (нарисованные вручную позы, не изображение)
# ---------------------------------------------------------------------------

def scene_animatsiya():
    imena = ["animation-frame-1", "animation-frame-2", "animation-frame-3", "animation-frame-4"]
    for i, imya in enumerate(imena):
        screen = novyj_ekran()
        screen.fill(CVET_FONA)
        noga_sdvig = (i % 4) * 6 - 9  # разное положение "ноги" — иллюзия шага
        pygame.draw.rect(screen, (100, 200, 255), (280, 150, 40, 60))       # тело
        pygame.draw.rect(screen, (100, 200, 255), (280 + noga_sdvig, 210, 12, 30))  # нога
        pygame.display.flip()
        sohranit(screen, imya)
    _polosa(imena, "animation-strip")


# ---------------------------------------------------------------------------
# 20.28 — реальные баги, воспроизведённые намеренно
# ---------------------------------------------------------------------------

def scene_bug_bez_fill():
    """Реальное воспроизведение бага «забыли screen.fill()»: рисуем мяч в
    нескольких позициях БЕЗ очистки экрана между кадрами — след виден по
    -настоящему, это не имитация."""
    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    for x in range(60, 480, 60):
        pygame.draw.circle(screen, (255, 100, 100), (x, 200), 18)
        pygame.display.flip()
    sohranit(screen, "debug-missing-fill-trail")


# ---------------------------------------------------------------------------
# 20.25 — состояния игры
# ---------------------------------------------------------------------------

def scene_sostoyaniya_igry():
    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    tekst = FONT.render("PYTHON GAME — нажмите пробел", True, (240, 240, 250))
    screen.blit(tekst, (SHIRINA // 2 - 140, VYSOTA // 2 - 10))
    pygame.display.flip()
    sohranit(screen, "game-states-menu")

    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    pygame.draw.circle(screen, (255, 100, 100), (300, 200), 20)
    tekst = FONT.render("Счёт: 40   Отскоков: 4", True, (240, 240, 250))
    screen.blit(tekst, (12, 10))
    pygame.display.flip()
    sohranit(screen, "game-states-playing")

    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    pygame.draw.circle(screen, (255, 100, 100), (300, 200), 20)
    tekst = FONT.render("ПАУЗА — P, чтобы продолжить", True, (255, 210, 90))
    rect = tekst.get_rect(center=(SHIRINA // 2, VYSOTA // 2))
    screen.blit(tekst, rect)
    pygame.display.flip()
    sohranit(screen, "game-states-paused")

    screen = novyj_ekran()
    screen.fill(CVET_FONA)
    tekst = FONT.render("GAME OVER — счёт: 140", True, (255, 130, 130))
    rect = tekst.get_rect(center=(SHIRINA // 2, VYSOTA // 2))
    screen.blit(tekst, rect)
    pygame.display.flip()
    sohranit(screen, "game-states-game-over")

    _polosa(
        ["game-states-menu", "game-states-playing", "game-states-paused", "game-states-game-over"],
        "game-states-strip",
    )


# ---------------------------------------------------------------------------
# 20.33 — финальный проект: Мяч Pro
# ---------------------------------------------------------------------------

def scene_myach_pro():
    import bouncing_ball as bb  # noqa: PLC0415

    game = bb.BouncingBallGame()
    for _ in range(150):
        game.update(1 / 60)
    game.render()
    sohranit(game.screen, "bouncing-ball-pro-hud")

    game.toggle_pause()
    game.render()
    sohranit(game.screen, "bouncing-ball-pro-paused")


SCENES = [
    scene_pervoe_okno,
    scene_cikl_kvadrat,
    scene_personazhi,
    scene_tri_vraga,
    scene_dvizhenie,
    scene_myach_basic,
    scene_virtualnye_knopki,
    scene_safe_area,
    scene_surface_blit,
    scene_surface_alpha,
    scene_stolknoveniya,
    scene_hitbox_vs_art,
    scene_gravitaciya,
    scene_animatsiya,
    scene_bug_bez_fill,
    scene_sostoyaniya_igry,
    scene_myach_pro,
]


if __name__ == "__main__":
    for scene in SCENES:
        scene()
    pygame.quit()
    print("Готово.")
