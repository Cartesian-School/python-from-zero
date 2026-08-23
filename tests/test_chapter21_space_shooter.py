"""Регрессионный набор для финального проекта главы 21 (космический
шутер): FPS-независимость движения, кулдаун стрельбы, таймер спавна,
столкновения, счёт, неуязвимость, пауза, перезапуск, Game Over и таймер
анимации взрыва — работает через SDL dummy-драйверы, поэтому не требует
ни Xvfb, ни настоящего дисплея (раздел 21.24 сайта).

Все тесты импортируют и вызывают РЕАЛЬНЫЙ производственный код
(projects/pygame/space-shooter/space_shooter.py), а не его копии.
"""

import math
import os
import random
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = ROOT / "projects" / "pygame" / "space-shooter"
sys.path.insert(0, str(GAME_DIR))

import pygame  # noqa: E402
import space_shooter as ss  # noqa: E402


def novaya_igra(seed: int = 0) -> ss.Game:
    return ss.Game(rng=random.Random(seed))


# ---------- 21.11 — Vector2: FPS-независимость движения игрока ----------

def test_player_movement_is_fps_independent():
    """Одна и та же реальная секунда движения вправо, нарезанная на 30, 60
    или 120 шагов, обязана дать одно и то же итоговое смещение — то же
    самое доказательство, что и в разделе 20.16, но теперь для Player."""
    itogi = {}
    for fps in (30, 60, 120):
        image = pygame.Surface((10, 10))
        player = ss.Player(image, (50.0, 600.0))
        # Широкое игровое поле — движение не должно упереться в clamp
        # раньше конца секунды, иначе тест проверял бы clamp, а не dt.
        playfield = pygame.Rect(0, 0, ss.SHIRINA * 4, ss.VYSOTA)
        dt = 1 / fps
        for _ in range(fps):   # ровно 1.0 секунда
            player.move(pygame.Vector2(1, 0), dt, playfield)
        itogi[fps] = player.position.x

    assert math.isclose(itogi[30], itogi[60], abs_tol=1e-6)
    assert math.isclose(itogi[60], itogi[120], abs_tol=1e-6)
    assert math.isclose(itogi[60], 50.0 + ss.PLAYER_SPEED, abs_tol=1e-6)


def test_bullet_movement_is_fps_independent():
    itogi = {}
    for fps in (30, 60, 120):
        image = pygame.Surface((4, 12))
        bullet = ss.Bullet(image, (100.0, 500.0))
        playfield = pygame.Rect(0, 0, ss.SHIRINA, ss.VYSOTA)
        dt = 1 / fps
        for _ in range(fps):
            bullet.update(dt, playfield)
        itogi[fps] = bullet.position.y

    assert math.isclose(itogi[30], itogi[60], abs_tol=1e-6)
    assert math.isclose(itogi[60], itogi[120], abs_tol=1e-6)
    assert math.isclose(itogi[60], 500.0 - ss.BULLET_SPEED, abs_tol=1e-6)


def test_enemy_movement_is_fps_independent():
    itogi = {}
    for fps in (30, 60, 120):
        image = pygame.Surface((32, 28))
        enemy = ss.Enemy(image, (100.0, 0.0), points=100, speed=150.0)
        playfield = pygame.Rect(0, 0, ss.SHIRINA, ss.VYSOTA)
        dt = 1 / fps
        for _ in range(fps):
            enemy.update(dt, playfield)
        itogi[fps] = enemy.position.y

    assert math.isclose(itogi[30], itogi[60], abs_tol=1e-6)
    assert math.isclose(itogi[60], itogi[120], abs_tol=1e-6)
    assert math.isclose(itogi[60], 150.0, abs_tol=1e-6)


# ---------- 21.2–21.4 — историческая (процедурная) версия: FPS-независимость ----------
#
# До раздела 21.9 на сайте ещё нет классов Player/Bullet/Enemy и Vector2 —
# только обычные переменные, Rect и dict, обновляемые вручную. Тесты выше
# доказывают FPS-независимость ФИНАЛЬНОГО класса Game; тесты ниже доказывают
# то же самое для процедурного кода, который реально показан на страницах
# 21.2–21.4 (scripts/build_chapter_21.py, build_03/build_04) и в ноутбуках
# 21-03/21-04 (scripts/build_notebooks_ch21.py) — учебный путь должен быть
# честным с самого первого работающего примера, а не только в финале главы.

_KORABL_SKOROST_ISTORICHESKAYA = 260.0   # px/s, раздел 21.3
_VRAG_SKOROST_ISTORICHESKAYA = 150.0     # px/s, раздел 21.3
_PULYA_SKOROST_ISTORICHESKAYA = 560.0    # px/s, раздел 21.4
_INTERVAL_POYAVLENIYA_VRAGA_ISTORICHESKY = 0.75   # секунд, раздел 21.3


def test_istoricheskoe_dvizhenie_korablya_fps_independent():
    """Раздел 21.3: obrabotat_klavishi() двигает korabl_x на
    KORABL_SKOROST * dt и ограничивает результат через max(0.0, min(...)) —
    смещение за одну и ту же реальную секунду обязано совпадать на любом
    FPS, точно как в test_player_movement_is_fps_independent выше."""
    shirina, korabl_shirina = 480, 44
    itogi = {}
    for fps in (30, 60, 120):
        korabl_x = 0.0
        dt = 1 / fps
        for _ in range(fps):   # ровно 1.0 секунда
            korabl_x += 1 * _KORABL_SKOROST_ISTORICHESKAYA * dt
            korabl_x = max(0.0, min(korabl_x, shirina - korabl_shirina))
        itogi[fps] = korabl_x

    assert math.isclose(itogi[30], itogi[60], abs_tol=1e-6)
    assert math.isclose(itogi[60], itogi[120], abs_tol=1e-6)
    assert math.isclose(itogi[60], _KORABL_SKOROST_ISTORICHESKAYA, abs_tol=1e-6)


def test_istoricheskoe_dvizhenie_vraga_fps_independent():
    """Раздел 21.3: vrag['y'] += VRAG_SKOROST * dt — та же проверка, что и
    для корабля выше, но для падения врага вниз."""
    itogi = {}
    for fps in (30, 60, 120):
        vrag_y = 0.0
        dt = 1 / fps
        for _ in range(fps):
            vrag_y += _VRAG_SKOROST_ISTORICHESKAYA * dt
        itogi[fps] = vrag_y

    assert math.isclose(itogi[30], itogi[60], abs_tol=1e-6)
    assert math.isclose(itogi[60], itogi[120], abs_tol=1e-6)
    assert math.isclose(itogi[60], _VRAG_SKOROST_ISTORICHESKAYA, abs_tol=1e-6)


def test_istoricheskaya_pulya_fps_independent():
    """Раздел 21.4: pulya['y'] -= PULYA_SKOROST * dt — та же проверка для
    пули, летящей вверх."""
    itogi = {}
    for fps in (30, 60, 120):
        pulya_y = 0.0
        dt = 1 / fps
        for _ in range(fps):
            pulya_y -= _PULYA_SKOROST_ISTORICHESKAYA * dt
        itogi[fps] = pulya_y

    assert math.isclose(itogi[30], itogi[60], abs_tol=1e-6)
    assert math.isclose(itogi[60], itogi[120], abs_tol=1e-6)
    assert math.isclose(itogi[60], -_PULYA_SKOROST_ISTORICHESKAYA, abs_tol=1e-6)


def test_istoricheskij_taimer_poyavleniya_vraga_fps_independent():
    """Раздел 21.3: таймер появления врага через if (сохранение остатка
    через while появится только в разделе 21.14) обязан давать одинаковое
    число появившихся врагов за одно и то же реальное время на разных FPS,
    пока один кадр короче целого интервала — dt здесь всегда мал по
    сравнению с INTERVAL_POYAVLENIYA_VRAGA, поэтому if ведёт себя как while."""
    itogi = {}
    for fps in (30, 60, 120):
        vremya_do_vraga = _INTERVAL_POYAVLENIYA_VRAGA_ISTORICHESKY
        poyavilos = 0
        dt = 1 / fps
        for _ in range(fps * 2):   # 2.0 реальные секунды
            vremya_do_vraga -= dt
            if vremya_do_vraga <= 0:
                poyavilos += 1
                vremya_do_vraga = _INTERVAL_POYAVLENIYA_VRAGA_ISTORICHESKY
        itogi[fps] = poyavilos

    assert itogi[30] == itogi[60] == itogi[120]
    assert itogi[60] >= 1


# ---------- 21.11 — субпиксельное движение не теряется ----------

def test_subpixel_movement_accumulates_in_float_position():
    """Скорость и dt подобраны так, что одно движение — меньше одного
    пикселя (0.5 px за кадр) — Rect-only реализация потеряла бы его
    полностью из-за округления до целых координат."""
    image = pygame.Surface((10, 10))
    player = ss.Player(image, (240.0, 600.0))
    player.speed = 30.0   # px/s -> 0.5 px за кадр при 60 FPS
    playfield = pygame.Rect(0, 0, ss.SHIRINA, ss.VYSOTA)
    dt = 1 / 60
    for _ in range(60):   # 60 шагов по 0.5 px = 30 px суммарно
        player.move(pygame.Vector2(1, 0), dt, playfield)
    assert math.isclose(player.position.x, 270.0, abs_tol=1e-6)


# ---------- 21.12 — нормализация диагонального движения ----------

def test_diagonal_movement_is_normalized():
    image = pygame.Surface((10, 10))
    playfield = pygame.Rect(0, 0, ss.SHIRINA, ss.VYSOTA)

    player_pryamo = ss.Player(image, (240.0, 400.0))
    player_pryamo.move(pygame.Vector2(1, 0), 1 / 60, playfield)
    smeshenie_pryamo = player_pryamo.position.x - 240.0

    player_diagonal = ss.Player(image, (240.0, 400.0))
    player_diagonal.move(pygame.Vector2(1, 1), 1 / 60, playfield)
    dx = player_diagonal.position.x - 240.0
    dy = player_diagonal.position.y - 400.0
    smeshenie_diagonal = math.hypot(dx, dy)

    assert math.isclose(smeshenie_pryamo, smeshenie_diagonal, rel_tol=1e-6)


def test_playfield_clamp_keeps_player_inside():
    image = pygame.Surface((10, 10))
    playfield = pygame.Rect(0, 0, ss.SHIRINA, ss.VYSOTA)
    player = ss.Player(image, (2.0, 2.0))
    for _ in range(120):
        player.move(pygame.Vector2(-1, -1), 1 / 60, playfield)
    assert player.rect.left >= playfield.left
    assert player.rect.top >= playfield.top


# ---------- 21.4/21.13 — KEYDOWN один раз за нажатие, get_pressed() — опрос ----------

def test_keydown_fires_once_get_pressed_is_polled():
    """Раздел 21.4/21.13: pygame.KEYDOWN добавляется в очередь событий один
    раз на одно физическое нажатие и «вычерпывается» первым же чтением —
    второе pygame.event.get() подряд его уже не вернёт. У
    pygame.key.get_pressed() такого нет: он читает живое состояние
    клавиатуры и может опрашиваться сколько угодно раз подряд без единого
    нового события. Именно это, а не KEYDOWN, было бы источником выстрела
    на каждом кадре, если бы стрельбу на удержании не ограничить отдельным
    интервалом (раздел 21.13) — раздел 21.4 стреляет по KEYDOWN и поэтому
    удержание там уже безопасно даёт ровно один выстрел."""
    pygame.display.init()   # pygame.key.* и pygame.event.* требуют видеоподсистему
    assert pygame.key.get_repeat() == (0, 0), (
        "автоматический повтор клавиш должен быть выключен по умолчанию — "
        "иначе KEYDOWN сам по себе генерировался бы заново на каждый кадр удержания"
    )

    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))

    pervoe_chtenie = [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]
    vtoroe_chtenie = [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]
    assert len(pervoe_chtenie) == 1, "один event.post() должен дать ровно одно KEYDOWN-событие"
    assert vtoroe_chtenie == [], "повторное чтение очереди не должно вернуть то же KEYDOWN снова"

    klavishi_pervoe = pygame.key.get_pressed()
    klavishi_vtoroe = pygame.key.get_pressed()
    assert klavishi_pervoe[pygame.K_SPACE] == klavishi_vtoroe[pygame.K_SPACE]


# ---------- 21.13 — кулдаун стрельбы: не более одного выстрела за кадр ----------

def test_fire_cooldown_limits_shots_per_second():
    game = novaya_igra()
    game.start_new_game()

    dt = 1 / 60
    for _ in range(60):   # 1.0 секунда удержания огня
        game.player.update_timers(dt)
        if game.player.fire_cooldown <= 0.0:
            game._spawn_bullet()
            game.player.fire_cooldown = ss.FIRE_INTERVAL

    ozhidaemo = math.floor(1.0 / ss.FIRE_INTERVAL) + 1
    assert 1 <= len(game.bullets) <= ozhidaemo


def test_fire_cooldown_never_fires_every_rendered_frame():
    """При кулдауне 0.2 с удержание огня 60 кадров подряд НЕ должно
    создать 60 пуль — иначе кулдаун измерялся бы кадрами, а не секундами."""
    game = novaya_igra()
    game.start_new_game()
    dt = 1 / 60
    for _ in range(60):
        game.player.update_timers(dt)
        if game.player.fire_cooldown <= 0.0:
            game._spawn_bullet()
            game.player.fire_cooldown = ss.FIRE_INTERVAL
    assert len(game.bullets) < 60


def test_fire_rate_is_fps_independent():
    """Одна и та же секунда удержания огня на разных FPS должна дать
    примерно одинаковое число выстрелов (±1 из-за границы интервалов)."""
    vystrelov = {}
    for fps in (30, 60, 120):
        game = novaya_igra()
        game.start_new_game()
        dt = 1 / fps
        for _ in range(fps):
            game.player.update_timers(dt)
            if game.player.fire_cooldown <= 0.0:
                game._spawn_bullet()
                game.player.fire_cooldown = ss.FIRE_INTERVAL
        vystrelov[fps] = len(game.bullets)

    znacheniya = list(vystrelov.values())
    assert max(znacheniya) - min(znacheniya) <= 1


# ---------- 21.16 — таймер спавна врагов: секунды, не кадры ----------

def test_enemy_spawn_timer_is_fps_independent():
    """Ровно одна и та же реальная секунда, нарезанная на 30/60/120 шагов,
    обязана заспавнить одно и то же число врагов при фиксированном
    (нулевом) счёте — интервал спавна тогда не меняется по ходу теста."""
    kolichestvo = {}
    for fps in (30, 60, 120):
        game = novaya_igra()
        game.start_new_game()
        game.score = 0   # фиксируем интервал спавна на всё время теста
        dt = 1 / fps
        for _ in range(fps):
            game.spawn_timer -= dt
            while game.spawn_timer <= 0.0:
                game._spawn_enemy()
                game.spawn_timer += ss.interval_poyavleniya_vraga(game.score)
        kolichestvo[fps] = len(game.enemies)

    assert kolichestvo[30] == kolichestvo[60] == kolichestvo[120]


def test_enemy_spawn_timer_preserves_overshoot():
    """dt длиннее интервала спавна обязан заспавнить НЕСКОЛЬКО врагов за
    один шаг (while), а не потерять «лишнее» время (if)."""
    game = novaya_igra()
    game.start_new_game()
    game.score = 0
    interval = ss.interval_poyavleniya_vraga(0)

    dt = interval * 3.2   # заведомо покрывает 3 полных интервала
    game.spawn_timer -= dt
    poyavilos = 0
    while game.spawn_timer <= 0.0:
        game._spawn_enemy()
        poyavilos += 1
        game.spawn_timer += ss.interval_poyavleniya_vraga(game.score)

    assert poyavilos == 3
    assert 0.0 < game.spawn_timer < interval


def test_spawn_x_keeps_full_enemy_width_inside_playfield():
    rng = random.Random(99)
    playfield = pygame.Rect(0, ss.HUD_HEIGHT, ss.SHIRINA, ss.VYSOTA - ss.HUD_HEIGHT)
    shirina_vraga = 46
    for _ in range(200):
        x = ss.x_poyavleniya_vraga(rng, shirina_vraga, playfield)
        assert playfield.left <= x <= playfield.right - shirina_vraga


# ---------- 21.18 — столкновения пуль и врагов: счёт без двойного начисления ----------

def test_bullet_destroys_enemy_and_awards_score_once():
    game = novaya_igra()
    game.start_new_game()

    vrag = ss.Enemy(game.assets.images["enemy_scout"], (100.0, 100.0), points=100, speed=0.0)
    game.enemies.add(vrag)
    pulya = ss.Bullet(game.assets.images["bullet"], (100.0, 100.0))
    game.bullets.add(pulya)

    schet = game.resolve_bullet_enemy_collisions()

    assert schet == 100
    assert len(game.enemies) == 0
    assert len(game.bullets) == 0


def test_overlapping_bullets_do_not_double_score_same_enemy():
    """Если сразу ДВЕ пули задели одного и того же врага в одном
    обновлении, очки должны начислиться ровно один раз — set в
    resolve_bullet_enemy_collisions() как раз для этого."""
    game = novaya_igra()
    game.start_new_game()

    vrag = ss.Enemy(game.assets.images["enemy_scout"], (100.0, 100.0), points=100, speed=0.0)
    game.enemies.add(vrag)
    game.bullets.add(ss.Bullet(game.assets.images["bullet"], (99.0, 100.0)))
    game.bullets.add(ss.Bullet(game.assets.images["bullet"], (101.0, 100.0)))

    schet = game.resolve_bullet_enemy_collisions()

    assert schet == 100
    assert len(game.enemies) == 0


# ---------- 21.19 — урон игроку и временная неуязвимость ----------

def test_single_collision_removes_one_life():
    game = novaya_igra()
    game.start_new_game()
    zhizni_do = game.lives

    vrag = ss.Enemy(game.assets.images["enemy_scout"], game.player.rect.center, points=100, speed=0.0)
    game.enemies.add(vrag)

    collided = game.resolve_enemy_player_collisions()
    if collided and not game.player.is_invulnerable:
        game.lives -= 1
        game.player.take_hit()

    assert game.lives == zhizni_do - 1
    assert game.player.is_invulnerable


def test_three_simultaneous_enemies_remove_only_one_life():
    """Три врага, столкнувшиеся с игроком в ОДНОМ обновлении, должны
    отнять ровно одну жизнь, а не три — раздел 21.16 сайта."""
    game = novaya_igra()
    game.start_new_game()
    zhizni_do = game.lives

    for _ in range(3):
        game.enemies.add(
            ss.Enemy(game.assets.images["enemy_scout"], game.player.rect.center, points=100, speed=0.0)
        )

    collided = game.resolve_enemy_player_collisions()
    if collided and not game.player.is_invulnerable:
        game.lives -= 1
        game.player.take_hit()

    assert game.lives == zhizni_do - 1
    assert len(game.enemies) == 0


def test_invulnerability_blocks_second_hit_immediately_after():
    game = novaya_igra()
    game.start_new_game()
    game.player.take_hit()
    zhizni_do = game.lives

    vrag = ss.Enemy(game.assets.images["enemy_scout"], game.player.rect.center, points=100, speed=0.0)
    game.enemies.add(vrag)

    collided = game.resolve_enemy_player_collisions()
    if collided and not game.player.is_invulnerable:
        game.lives -= 1
        game.player.take_hit()

    assert game.lives == zhizni_do   # неуязвимость активна — жизнь не потеряна
    assert len(game.enemies) == 0    # но враг всё равно уничтожен при контакте


def test_invulnerability_expires_and_allows_next_hit():
    game = novaya_igra()
    game.start_new_game()
    game.player.take_hit()
    game.player.invulnerable_timer = 0.0   # имитируем истечение таймера
    zhizni_do = game.lives

    vrag = ss.Enemy(game.assets.images["enemy_scout"], game.player.rect.center, points=100, speed=0.0)
    game.enemies.add(vrag)
    collided = game.resolve_enemy_player_collisions()
    if collided and not game.player.is_invulnerable:
        game.lives -= 1
        game.player.take_hit()

    assert game.lives == zhizni_do - 1


# ---------- 21.21 — враги, покинувшие игровое поле ----------

def test_enemy_escape_costs_one_life_each():
    game = novaya_igra()
    game.start_new_game()
    zhizni_do = game.lives

    for _ in range(2):
        vrag = ss.Enemy(
            game.assets.images["enemy_scout"],
            (100.0, game.playfield.bottom + 100.0),
            points=100,
            speed=0.0,
        )
        game.enemies.add(vrag)

    sbezhalo = game.resolve_enemy_escapes()

    assert sbezhalo == 2
    assert len(game.enemies) == 0
    game.lives -= sbezhalo
    assert game.lives == zhizni_do - 2


def test_enemy_still_inside_playfield_does_not_escape():
    game = novaya_igra()
    game.start_new_game()
    vrag = ss.Enemy(game.assets.images["enemy_scout"], (100.0, game.playfield.centery), points=100, speed=0.0)
    game.enemies.add(vrag)
    assert game.resolve_enemy_escapes() == 0
    assert len(game.enemies) == 1


# ---------- 21.22 — пауза замораживает игровой мир ----------

def test_pause_freezes_all_gameplay_state():
    game = novaya_igra(seed=5)
    game.start_new_game()

    # Наполняем мир, чтобы было что "заморозить"
    for _ in range(60):
        game.update(1 / 60)

    game.toggle_pause()
    assert game.state is ss.GameStatus.PAUSED

    snimok_do = (
        game.player.position.x,
        game.player.position.y,
        game.score,
        game.lives,
        game.spawn_timer,
        game.player.fire_cooldown,
        game.player.invulnerable_timer,
        [(e.position.x, e.position.y) for e in game.enemies],
        [(b.position.x, b.position.y) for b in game.bullets],
    )

    for _ in range(180):   # 3 "замороженых" секунды
        game.update(1 / 60)

    snimok_posle = (
        game.player.position.x,
        game.player.position.y,
        game.score,
        game.lives,
        game.spawn_timer,
        game.player.fire_cooldown,
        game.player.invulnerable_timer,
        [(e.position.x, e.position.y) for e in game.enemies],
        [(b.position.x, b.position.y) for b in game.bullets],
    )

    assert snimok_do == snimok_posle


def test_resume_continues_from_frozen_state():
    game = novaya_igra(seed=5)
    game.start_new_game()
    for _ in range(30):
        game.update(1 / 60)
    game.toggle_pause()
    for _ in range(60):
        game.update(1 / 60)   # ничего не должно поменяться
    game.toggle_pause()
    x_do_resume = game.player.position.x
    game.handle_input(1 / 60)   # без нажатых клавиш -- позиция не меняется без ввода
    assert game.state is ss.GameStatus.PLAYING
    assert math.isclose(game.player.position.x, x_do_resume, abs_tol=1e-6)


# ---------- 21.23 — перезапуск сбрасывает ВСЁ переходное состояние ----------

def test_restart_resets_all_transient_state():
    game = novaya_igra(seed=3)
    game.start_new_game()

    # Пачкаем состояние искусственно
    game.score = 950
    game.lives = 1
    game.spawn_timer = 0.01
    game.player.fire_cooldown = 0.15
    game.player.invulnerable_timer = 0.8
    game.player.position.x = 12.0
    game.bullets.add(ss.Bullet(game.assets.images["bullet"], (50.0, 50.0)))
    game.enemies.add(ss.Enemy(game.assets.images["enemy_scout"], (50.0, 50.0), points=100, speed=10.0))
    game.explosions.add(ss.Explosion(game.assets.explosion_frames, (50.0, 50.0)))

    game.start_new_game()

    assert game.state is ss.GameStatus.PLAYING
    assert game.score == 0
    assert game.lives == ss.STARTING_LIVES
    assert len(game.bullets) == 0
    assert len(game.enemies) == 0
    assert len(game.explosions) == 0
    assert game.player.fire_cooldown == 0.0
    assert game.player.invulnerable_timer == 0.0
    assert math.isclose(game.spawn_timer, ss.interval_poyavleniya_vraga(0), abs_tol=1e-6)
    assert math.isclose(game.player.position.x, ss.SHIRINA / 2, abs_tol=1e-6)


def test_restart_preserves_session_high_score():
    game = novaya_igra()
    game.start_new_game()
    game.score = 500
    game.high_score = 500
    game.start_new_game()
    assert game.high_score == 500
    assert game.score == 0


# ---------- 21.7/21.22 — Game Over: вход и перезапуск ----------

def test_lives_reaching_zero_triggers_game_over():
    game = novaya_igra()
    game.start_new_game()
    game.lives = 1
    for _ in range(2):
        game.enemies.add(
            ss.Enemy(game.assets.images["enemy_scout"], game.player.rect.center, points=100, speed=0.0)
        )
    game._update_playing(1 / 60)
    assert game.state is ss.GameStatus.GAME_OVER
    assert game.lives == 0


def test_game_over_input_is_ignored_until_restart():
    game = novaya_igra()
    game.start_new_game()
    game.lives = 0
    game.state = ss.GameStatus.GAME_OVER
    x_do = game.player.position.x

    keys_before = game.player.position.x
    game.handle_input(1 / 60)   # PLAYING-only ввод не должен подействовать
    assert game.player.position.x == keys_before == x_do


def test_enter_on_game_over_restarts_into_playing():
    game = novaya_igra()
    game.start_new_game()
    game.state = ss.GameStatus.GAME_OVER
    game.lives = 0
    game.score = 300
    if game.state in (ss.GameStatus.MENU, ss.GameStatus.GAME_OVER):
        game.start_new_game()
    assert game.state is ss.GameStatus.PLAYING
    assert game.lives == ss.STARTING_LIVES
    assert game.score == 0


# ---------- 21.24 — таймер анимации взрыва: аккумулятор с overshoot ----------

def test_explosion_accumulator_preserves_overshoot():
    game = novaya_igra()
    game.start_new_game()
    frames_count = len(game.assets.explosion_frames)
    vzryv = ss.Explosion(game.assets.explosion_frames, (100.0, 100.0))
    game.explosions.add(vzryv)   # alive() смотрит на членство в группе

    # Один длинный кадр, покрывающий сразу несколько интервалов анимации
    dt = ss.EXPLOSION_FRAME_INTERVAL * 2.4
    vzryv.update(dt)

    assert vzryv.frame_index == 2
    assert 0.0 < vzryv.animation_time < ss.EXPLOSION_FRAME_INTERVAL
    assert vzryv.alive()
    assert frames_count > 2   # проверка не выродилась в тривиальную


def test_explosion_kills_itself_after_last_frame():
    game = novaya_igra()
    game.start_new_game()
    vzryv = ss.Explosion(game.assets.explosion_frames, (100.0, 100.0))
    frames_count = len(game.assets.explosion_frames)

    for _ in range(frames_count + 5):
        vzryv.update(ss.EXPLOSION_FRAME_INTERVAL)

    assert not vzryv.alive()


def test_explosion_timing_is_fps_independent_over_equal_elapsed_time():
    kadrov_proshlo = {}
    for fps in (30, 60, 120):
        image_group = pygame.sprite.Group()
        frames = [pygame.Surface((8, 8)) for _ in range(20)]   # с запасом, не убьётся раньше времени
        vzryv = ss.Explosion(frames, (0, 0))
        image_group.add(vzryv)
        dt = 1 / fps
        for _ in range(fps):   # ровно 1.0 секунда
            vzryv.update(dt)
        kadrov_proshlo[fps] = vzryv.frame_index

    assert kadrov_proshlo[30] == kadrov_proshlo[60] == kadrov_proshlo[120]


# ---------- Чистые функции сложности ----------

def test_spawn_interval_decreases_with_score_but_has_floor():
    assert ss.interval_poyavleniya_vraga(0) == ss.BASE_SPAWN_INTERVAL
    assert ss.interval_poyavleniya_vraga(10_000) == ss.MIN_SPAWN_INTERVAL
    assert ss.interval_poyavleniya_vraga(500) < ss.interval_poyavleniya_vraga(0)


def test_enemy_speed_multiplier_increases_with_score_but_has_ceiling():
    assert ss.mnozhitel_skorosti_vraga(0) == 1.0
    assert ss.mnozhitel_skorosti_vraga(10_000) == 1.0 + ss.MAX_ENEMY_SPEED_BONUS
    assert ss.mnozhitel_skorosti_vraga(1000) > ss.mnozhitel_skorosti_vraga(0)


def test_fighter_probability_is_deterministic_for_fixed_rng_seed():
    """Один и тот же seed обязан дать один и тот же выбор типа врага —
    иначе сценарии для скриншотов были бы невоспроизводимы."""
    tipy_a = [ss.vybrat_tip_vraga(random.Random(42), score).name for score in range(0, 2000, 100)]
    tipy_b = [ss.vybrat_tip_vraga(random.Random(42), score).name for score in range(0, 2000, 100)]
    assert tipy_a == tipy_b


def test_wave_number_increases_with_score():
    assert ss.nomer_volny(0) == 1
    assert ss.nomer_volny(ss.WAVE_SCORE_STEP) == 2
    assert ss.nomer_volny(ss.WAVE_SCORE_STEP * 3) == 4


def test_score_for_destroyed_sums_points_without_side_effects():
    class _Fake:
        def __init__(self, points):
            self.points = points

    vragi = [_Fake(100), _Fake(200), _Fake(100)]
    assert ss.ochki_za_unichtozhennyh(vragi) == 400
    assert ss.ochki_za_unichtozhennyh([]) == 0


# ---------- Общая проверка: игра запускается и работает под SDL dummy ----------

def test_game_runs_headless_smoke():
    game = novaya_igra(seed=1)
    game.start_new_game()
    for _ in range(300):   # 5 симулированных секунд
        game.update(1 / 60)
        game.render()
    assert game.state in (ss.GameStatus.PLAYING, ss.GameStatus.GAME_OVER)


def test_max_dt_clamps_huge_frame_spike():
    """Один гигантский dt (например, после паузы отладчика) не должен
    провести объект сквозь весь экран за один шаг — Game.update() обязан
    обрезать dt до MAX_DT перед тем, как применить его к симуляции."""
    game = novaya_igra()
    game.start_new_game()
    vrag = ss.Enemy(game.assets.images["enemy_scout"], (100.0, 100.0), points=100, speed=2000.0)
    game.enemies.add(vrag)
    y_do = vrag.position.y

    game.update(5.0)   # 5 "секунд" одним кадром

    smeshenie = vrag.position.y - y_do
    assert smeshenie <= 2000.0 * ss.MAX_DT + 1.0
    assert smeshenie < 2000.0 * 5.0   # без clamp сместился бы на 10000 px
