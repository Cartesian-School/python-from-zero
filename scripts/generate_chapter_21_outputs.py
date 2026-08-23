#!/usr/bin/env python3
"""Генерирует РЕАЛЬНЫЕ скриншоты финального проекта главы 21 (космический
шутер): каждый кадр — это настоящий Game.render() из
projects/pygame/space-shooter/space_shooter.py, сохранённый через
pygame.image.save(). Pillow используется только для того, чтобы склеить
уже готовые реальные кадры в сравнительные полосы (см. _polosa()) — тот же
приём, что и в generate_chapter_20_outputs.py. Никаких «нарисованных
Pillow окон» вместо настоящей игры.

Рендеринг идёт через headless-драйвер SDL "dummy" — окно нигде физически
не появляется, но Surface настоящая, и pygame.image.save() сохраняет её
как обычный PNG.

Использование: .venv/bin/python3 scripts/generate_chapter_21_outputs.py
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import random
import sys
from pathlib import Path

import pygame
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = ROOT / "projects" / "pygame" / "space-shooter"
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-21" / "output"
sys.path.insert(0, str(GAME_DIR))

import space_shooter as ss  # noqa: E402


def novaya_igra(seed: int = 0) -> ss.Game:
    return ss.Game(rng=random.Random(seed))


def sohranit(surface: pygame.Surface, name: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    pygame.image.save(surface, str(path))
    print(f"Сохранено: {path.relative_to(ROOT)}")
    return path


MAKS_SHIRINA_POLOSY = 820


def _polosa(names: list[str], out_name: str) -> None:
    images = [Image.open(OUT_DIR / f"{n}.png") for n in names]
    zazor = 16
    w = sum(im.width for im in images) + zazor * (len(images) - 1)
    h = max(im.height for im in images)
    strip = Image.new("RGB", (w, h), (10, 12, 26))
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


def _crop(name: str, box: tuple[int, int, int, int], out_name: str) -> None:
    im = Image.open(OUT_DIR / f"{name}.png")
    cropped = im.crop(box)
    path = OUT_DIR / f"{out_name}.png"
    cropped.save(path)
    print(f"Сохранён фрагмент: {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# 21.9 / 21.22 — меню
# ---------------------------------------------------------------------------

def scene_menu() -> None:
    game = novaya_igra(seed=1)
    game.render()
    sohranit(game.screen, "01-menu")


# ---------------------------------------------------------------------------
# 21.12 — пустое игровое поле сразу после старта
# ---------------------------------------------------------------------------

def scene_empty_playfield() -> None:
    game = novaya_igra(seed=1)
    game.start_new_game()
    game.render()
    sohranit(game.screen, "02-empty-playfield")
    _crop("02-empty-playfield", (
        game.player.rect.left - 30, game.player.rect.top - 20,
        game.player.rect.right + 30, game.player.rect.bottom + 20,
    ), "03-player-ship")


# ---------------------------------------------------------------------------
# 21.12 — движение корабля влево/по центру/вправо
# ---------------------------------------------------------------------------

def scene_player_movement() -> None:
    game = novaya_igra(seed=12)
    game.start_new_game()

    for _ in range(45):
        game.player.move(pygame.Vector2(-1, 0), 1 / 60, game.playfield)
    game.render()
    sohranit(game.screen, "04-player-left")

    game.player.position.x = ss.SHIRINA / 2
    game.player.rect.centerx = round(game.player.position.x)
    game.render()
    sohranit(game.screen, "05-player-center")

    for _ in range(45):
        game.player.move(pygame.Vector2(1, 0), 1 / 60, game.playfield)
    game.render()
    sohranit(game.screen, "06-player-right")

    _polosa(["04-player-left", "05-player-center", "06-player-right"], "player-movement-strip")


# ---------------------------------------------------------------------------
# 21.15 — первый враг и волна врагов
# ---------------------------------------------------------------------------

def scene_first_enemy() -> None:
    game = novaya_igra(seed=2)
    game.start_new_game()
    game._spawn_enemy()
    for _ in range(20):
        game.enemies.update(1 / 60, game.playfield)
    game.render()
    sohranit(game.screen, "07-first-enemy")


def scene_enemy_wave() -> None:
    game = novaya_igra(seed=3)
    game.start_new_game()
    game.score = 900   # выше вероятность fighter — видно оба типа сразу
    for _ in range(6):
        game._spawn_enemy()
        for _ in range(10):
            game.enemies.update(1 / 60, game.playfield)
    game.render()
    sohranit(game.screen, "08-enemy-wave")


def scene_two_enemy_types() -> None:
    game = novaya_igra(seed=4)
    game.start_new_game()
    scout = ss.Enemy(game.assets.images["enemy_scout"], (150.0, 220.0), points=100, speed=0.0)
    fighter = ss.Enemy(game.assets.images["enemy_fighter"], (320.0, 220.0), points=200, speed=0.0)
    game.enemies.add(scout, fighter)
    game.render()
    sohranit(game.screen, "19-two-enemy-types")


# ---------------------------------------------------------------------------
# 21.13/21.14 — стрельба
# ---------------------------------------------------------------------------

def scene_first_bullet() -> None:
    game = novaya_igra(seed=5)
    game.start_new_game()
    game._spawn_bullet()
    game.render()
    sohranit(game.screen, "09-first-bullet")


def scene_held_fire() -> None:
    game = novaya_igra(seed=5)
    game.start_new_game()
    dt = 1 / 60
    for _ in range(60):   # 1 секунда удержания SPACE
        game.player.update_timers(dt)
        if game.player.fire_cooldown <= 0.0:
            game._spawn_bullet()
            game.player.fire_cooldown = ss.FIRE_INTERVAL
        game.bullets.update(dt, game.playfield)
    game.render()
    sohranit(game.screen, "10-held-fire-cooldown")


# ---------------------------------------------------------------------------
# 21.18 — столкновение пули и врага
# ---------------------------------------------------------------------------

def scene_bullet_before_hit() -> None:
    game = novaya_igra(seed=6)
    game.start_new_game()
    vrag = ss.Enemy(game.assets.images["enemy_scout"], (game.player.rect.centerx, 260.0), points=100, speed=40.0)
    game.enemies.add(vrag)
    game._spawn_bullet()
    game.render()
    sohranit(game.screen, "11-bullet-before-hit")


def scene_bullet_hits_enemy() -> None:
    game = novaya_igra(seed=6)
    game.start_new_game()
    tochka = (game.player.rect.centerx, 300.0)
    vrag = ss.Enemy(game.assets.images["enemy_scout"], tochka, points=100, speed=0.0)
    game.enemies.add(vrag)
    pulya = ss.Bullet(game.assets.images["bullet"], tochka)
    game.bullets.add(pulya)

    ochki = game.resolve_bullet_enemy_collisions()
    game.score += ochki
    game.render()
    sohranit(game.screen, "12-bullet-enemy-hit")
    # 15 — крупный план табло счёта в тот же момент: тот же реальный кадр,
    # но другой, содержательно отличающийся файл (обрезка HUD, не полный
    # экран), поэтому не совпадает побайтово с 12-bullet-enemy-hit.png.
    _crop("12-bullet-enemy-hit", (0, 0, ss.SHIRINA, ss.HUD_HEIGHT), "15-score-after-hit")
    return game


def scene_explosion_frames(game: ss.Game) -> None:
    """12-bullet-enemy-hit.png уже показывает взрыв в момент рождения
    (frame_index=0) — поэтому здесь кадры сняты ПОЗЖЕ по времени анимации,
    а не заново с нуля, иначе 13 стал бы побайтовым дублем 12."""
    vzryv = next(iter(game.explosions), None)
    if vzryv is None:
        vzryv = ss.Explosion(game.assets.explosion_frames, (ss.SHIRINA / 2, 300.0))
        game.explosions.add(vzryv)

    vzryv.update(ss.EXPLOSION_FRAME_INTERVAL * 1.5)
    game.render()
    sohranit(game.screen, "13-explosion-frame-1")

    vzryv.update(ss.EXPLOSION_FRAME_INTERVAL * 2.0)
    game.render()
    sohranit(game.screen, "14-explosion-frame-2")

    _polosa(
        ["09-first-bullet", "11-bullet-before-hit", "13-explosion-frame-1"],
        "fire-sequence-strip",
    )


# ---------------------------------------------------------------------------
# 21.19 — урон игроку и неуязвимость
# ---------------------------------------------------------------------------

def scene_player_hit() -> None:
    game = novaya_igra(seed=7)
    game.start_new_game()
    zhizni_do = game.lives
    vrag = ss.Enemy(game.assets.images["enemy_fighter"], game.player.rect.center, points=200, speed=0.0)
    game.enemies.add(vrag)

    collided = game.resolve_enemy_player_collisions()
    if collided and not game.player.is_invulnerable:
        game.lives -= 1
        game.player.take_hit()
    game.render()
    sohranit(game.screen, "16-player-hit")
    assert game.lives == zhizni_do - 1

    # Неуязвимость ещё активна, но игрок успел отодвинуться в сторону —
    # реально другой кадр, а не то же самое изображение под другим именем.
    for _ in range(30):
        game.player.move(pygame.Vector2(1, 0), 1 / 60, game.playfield)
        game.player.update_timers(1 / 60)
    game.render()
    sohranit(game.screen, "17-invulnerability")
    assert game.player.is_invulnerable
    _crop("16-player-hit", (0, 0, ss.SHIRINA, ss.HUD_HEIGHT), "18-lives-hud")

    _polosa(["03-player-ship", "16-player-hit", "17-invulnerability"], "damage-sequence-strip")


# ---------------------------------------------------------------------------
# 21.20/21.21 — сложность и волны
# ---------------------------------------------------------------------------

def scene_difficulty_waves() -> None:
    game = novaya_igra(seed=8)
    game.start_new_game()
    for _ in range(3):
        game._spawn_enemy()
        for _ in range(15):
            game.enemies.update(1 / 60, game.playfield)
    game.render()
    sohranit(game.screen, "20-wave-1")

    game2 = novaya_igra(seed=9)
    game2.start_new_game()
    game2.score = 2200
    for _ in range(6):
        game2._spawn_enemy()
        for _ in range(15):
            game2.enemies.update(1 / 60, game2.playfield)
    game2.render()
    sohranit(game2.screen, "21-wave-harder")

    _polosa(["20-wave-1", "21-wave-harder"], "difficulty-strip")


# ---------------------------------------------------------------------------
# 21.22 — пауза, Game Over, перезапуск
# ---------------------------------------------------------------------------

def scene_states() -> None:
    game = novaya_igra(seed=10)
    game.start_new_game()
    game.score = 450
    for _ in range(2):
        game._spawn_enemy()
        for _ in range(20):
            game.enemies.update(1 / 60, game.playfield)
    game.toggle_pause()
    game.render()
    sohranit(game.screen, "22-paused")

    game3 = novaya_igra(seed=11)
    game3.start_new_game()
    game3.score = 780
    game3.high_score = 780
    game3.lives = 0
    game3.state = ss.GameStatus.GAME_OVER
    game3.render()
    sohranit(game3.screen, "23-game-over")

    game3.start_new_game()
    game3.render()
    sohranit(game3.screen, "24-restarted-game")

    _polosa(["02-empty-playfield", "22-paused", "23-game-over"], "game-states-strip")


# ---------------------------------------------------------------------------
# 21.33/21.34 — финальный, насыщенный кадр геймплея
# ---------------------------------------------------------------------------

def scene_final_gameplay() -> None:
    game = novaya_igra(seed=42)
    game.start_new_game()
    game.score = 640

    dt = 1 / 60
    for kadr in range(150):
        if kadr % 25 == 0:
            game._spawn_enemy()
        if kadr % 12 == 0:
            game._spawn_bullet()
        game.enemies.update(dt, game.playfield)
        game.bullets.update(dt, game.playfield)
        game._update_stars(dt)

    # Один эффектный взрыв на переднем плане для финального кадра
    vzryv = ss.Explosion(game.assets.explosion_frames, (ss.SHIRINA / 2 - 40, 260.0))
    vzryv.update(ss.EXPLOSION_FRAME_INTERVAL * 1.5)
    game.explosions.add(vzryv)

    game.render()
    sohranit(game.screen, "25-final-gameplay")


SCENES = [
    scene_menu,
    scene_empty_playfield,
    scene_player_movement,
    scene_first_enemy,
    scene_enemy_wave,
    scene_two_enemy_types,
    scene_first_bullet,
    scene_held_fire,
    scene_bullet_before_hit,
]


if __name__ == "__main__":
    for scene in SCENES:
        scene()
    igra_s_popadaniem = scene_bullet_hits_enemy()
    scene_explosion_frames(igra_s_popadaniem)
    scene_player_hit()
    scene_difficulty_waves()
    scene_states()
    scene_final_gameplay()
    pygame.quit()
    print("Готово.")
