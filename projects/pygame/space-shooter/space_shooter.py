"""Игра «Космический шутер» на Pygame.

Финальный проект главы 21 книги «Python с нуля» (Cartesian School).
Запуск: python space_shooter.py
Управление: стрелки — движение корабля во всех четырёх направлениях,
пробел — стрельба (можно удерживать), P — пауза, Enter — начать/заново,
Esc — выход.

Архитектура: класс Game владеет игроком (Player), группами спрайтов
(Bullet, Enemy, Explosion) и текущим состоянием (GameStatus). Все скорости
заданы в пикселях в секунду (px/s) и применяются через delta time — то же
самое, чему учит глава 20, — а не «пикселей за кадр», как в исторической
версии этого проекта.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import pygame

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "assets" / "images"
AUDIO_DIR = BASE_DIR / "assets" / "audio"

# ---------------------------------------------------------------------------
# Логическое разрешение и игровое поле
# ---------------------------------------------------------------------------

SHIRINA, VYSOTA = 480, 720
FPS = 60
MAX_DT = 0.05   # защита от гигантского dt после паузы отладчика/зависания ОС

HUD_HEIGHT = 64

BG_COLOR = (8, 10, 24)
HUD_BG_COLOR = (14, 17, 36)
HUD_BORDER_COLOR = (40, 46, 80)
HUD_TEXT_COLOR = (235, 238, 250)
ACCENT_COLOR = (110, 200, 255)
WARNING_COLOR = (255, 120, 120)
OVERLAY_COLOR = (6, 8, 18, 190)

# ---------------------------------------------------------------------------
# Игрок
# ---------------------------------------------------------------------------

STARTING_LIVES = 3
PLAYER_SPEED = 260.0                  # px/s
PLAYER_INVULNERABLE_SECONDS = 1.2     # окно неуязвимости после столкновения

# ---------------------------------------------------------------------------
# Стрельба и пули
# ---------------------------------------------------------------------------

FIRE_INTERVAL = 0.20                  # секунд между выстрелами при удержании SPACE
BULLET_SPEED = 560.0                  # px/s, вверх

# ---------------------------------------------------------------------------
# Враги и сложность
# ---------------------------------------------------------------------------

BASE_SPAWN_INTERVAL = 1.10            # секунд между врагами в начале игры
MIN_SPAWN_INTERVAL = 0.35             # нижняя граница — иначе спавн станет невозможным
SPAWN_INTERVAL_SCORE_FACTOR = 0.00055

MAX_ENEMY_SPEED_BONUS = 0.9           # враги ускоряются максимум в 1.9 раза
ENEMY_SPEED_SCORE_FACTOR = 0.00045

MAX_FIGHTER_PROBABILITY = 0.55
FIGHTER_PROBABILITY_SCORE_FACTOR = 0.00055

WAVE_SCORE_STEP = 500                 # очков на одну «волну»

# ---------------------------------------------------------------------------
# Взрывы и звёзды
# ---------------------------------------------------------------------------

EXPLOSION_FRAME_INTERVAL = 0.055

STAR_COUNT = 70
STAR_COLORS = ((255, 255, 255), (170, 200, 255), (255, 230, 180))
STAR_MIN_SPEED, STAR_MAX_SPEED = 20.0, 90.0


class GameStatus(Enum):
    """Явные состояния игры (раздел 21.18 сайта) — как enum.Enum из главы
    20, а не несколько независимых булевых флагов."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


@dataclass(frozen=True)
class EnemySpec:
    """Неизменяемое описание ТИПА врага — не конкретного экземпляра.
    base_speed ещё не учитывает бонус сложности текущей игры."""

    name: str
    base_speed: float
    points: int
    image_key: str


ENEMY_SPECS = {
    "scout": EnemySpec("scout", base_speed=150.0, points=100, image_key="enemy_scout"),
    "fighter": EnemySpec("fighter", base_speed=85.0, points=200, image_key="enemy_fighter"),
}


@dataclass
class Star:
    """Одна декоративная звезда фона — не Sprite: у неё нет ни
    столкновений, ни собственного изображения, поэтому рисуется напрямую
    через pygame.draw.circle()."""

    x: float
    y: float
    speed: float
    radius: int
    color: tuple[int, int, int]


# ---------------------------------------------------------------------------
# Чистые функции — их можно тестировать без запуска Pygame вообще
# ---------------------------------------------------------------------------

def interval_poyavleniya_vraga(score: int) -> float:
    """Интервал между появлением врагов, в секундах — уменьшается вместе
    со счётом, но не ниже MIN_SPAWN_INTERVAL (иначе спавн стал бы
    физически невозможным на высоком счёте)."""
    return max(MIN_SPAWN_INTERVAL, BASE_SPAWN_INTERVAL - score * SPAWN_INTERVAL_SCORE_FACTOR)


def mnozhitel_skorosti_vraga(score: int) -> float:
    """Множитель скорости врага (1.0 — обычная скорость), растущий со
    счётом, но ограниченный сверху — без резких скачков сложности."""
    return 1.0 + min(MAX_ENEMY_SPEED_BONUS, score * ENEMY_SPEED_SCORE_FACTOR)


def veroyatnost_istrebitelya(score: int) -> float:
    """Вероятность (0..1) того, что следующий враг — «истребитель»
    (fighter), а не «разведчик» (scout). Растёт со счётом, ограничена
    сверху MAX_FIGHTER_PROBABILITY."""
    return min(MAX_FIGHTER_PROBABILITY, score * FIGHTER_PROBABILITY_SCORE_FACTOR)


def vybrat_tip_vraga(rng: random.Random, score: int) -> EnemySpec:
    if rng.random() < veroyatnost_istrebitelya(score):
        return ENEMY_SPECS["fighter"]
    return ENEMY_SPECS["scout"]


def x_poyavleniya_vraga(rng: random.Random, shirina_vraga: float, pole: pygame.Rect) -> float:
    """Левая граница X для нового врага — вся ширина спрайта гарантированно
    остаётся внутри игрового поля, без частичного «обрезания» по краю."""
    levaya, pravaya = pole.left, pole.right - shirina_vraga
    if pravaya <= levaya:
        return float(levaya)
    return rng.uniform(levaya, pravaya)


def nomer_volny(score: int) -> int:
    return 1 + score // WAVE_SCORE_STEP


def ochki_za_unichtozhennyh(vragi) -> int:
    """Сумма очков за уничтоженных врагов — чистая функция, не завязанная
    на конкретный способ обнаружения столкновений."""
    return sum(vrag.points for vrag in vragi)


# ---------------------------------------------------------------------------
# Ассеты — загружаются один раз в AssetStore, а не внутри игрового цикла
# ---------------------------------------------------------------------------

class AssetStore:
    """Загружает все изображения и звуки ровно один раз при создании игры.
    Звук — не обязательное условие для запуска: если в системе нет
    звукового устройства (например, в headless-тестах), sounds[key]
    остаётся None, а AssetStore.play() просто ничего не делает."""

    def __init__(self, image_dir: Path, audio_dir: Path) -> None:
        self.images: dict[str, pygame.Surface] = {}
        self.explosion_frames: list[pygame.Surface] = []
        self.sounds: dict[str, pygame.mixer.Sound | None] = {}
        self._load_images(image_dir)
        self._load_sounds(audio_dir)

    def _load_images(self, image_dir: Path) -> None:
        for key in ("player_ship", "enemy_scout", "enemy_fighter", "bullet"):
            self.images[key] = pygame.image.load(image_dir / f"{key}.png").convert_alpha()

        sheet = pygame.image.load(image_dir / "explosion_sheet.png").convert_alpha()
        frame_side = sheet.get_height()
        frame_count = sheet.get_width() // frame_side
        self.explosion_frames = [
            sheet.subsurface((i * frame_side, 0, frame_side, frame_side)).copy()
            for i in range(frame_count)
        ]

    def _load_sounds(self, audio_dir: Path) -> None:
        for key in ("laser", "explosion", "player_hit"):
            path = audio_dir / f"{key}.wav"
            try:
                self.sounds[key] = pygame.mixer.Sound(str(path))
            except (pygame.error, FileNotFoundError):
                self.sounds[key] = None

    def play(self, key: str) -> None:
        sound = self.sounds.get(key)
        if sound is not None:
            sound.play()


# ---------------------------------------------------------------------------
# Игровые объекты
# ---------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    """Корабль игрока. Позиция хранится как pygame.Vector2 (с плавающей
    точкой) — Rect использует только целые числа и молча теряет мелкое
    движение при накоплении, поэтому Rect каждый кадр пересобирается ИЗ
    position, а не обновляется напрямую."""

    def __init__(self, image: pygame.Surface, center: tuple[float, float]) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(center)
        self.rect.center = (round(self.position.x), round(self.position.y))
        self.speed = PLAYER_SPEED
        self.fire_cooldown = 0.0
        self.invulnerable_timer = 0.0

    @property
    def is_invulnerable(self) -> bool:
        return self.invulnerable_timer > 0.0

    def move(self, direction: pygame.Vector2, dt: float, playfield: pygame.Rect) -> None:
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.position += direction * self.speed * dt

        half_w, half_h = self.rect.width / 2, self.rect.height / 2
        self.position.x = max(playfield.left + half_w, min(self.position.x, playfield.right - half_w))
        self.position.y = max(playfield.top + half_h, min(self.position.y, playfield.bottom - half_h))
        self.rect.center = (round(self.position.x), round(self.position.y))

    def update_timers(self, dt: float) -> None:
        self.fire_cooldown = max(0.0, self.fire_cooldown - dt)
        self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)

    def take_hit(self) -> None:
        self.invulnerable_timer = PLAYER_INVULNERABLE_SECONDS


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, center: tuple[float, float]) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(center)
        self.velocity = pygame.Vector2(0.0, -BULLET_SPEED)
        self.rect.center = (round(self.position.x), round(self.position.y))

    def update(self, dt: float, playfield: pygame.Rect) -> None:
        self.position += self.velocity * dt
        self.rect.center = (round(self.position.x), round(self.position.y))
        if self.rect.bottom < playfield.top:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, center: tuple[float, float], points: int, speed: float) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(center)
        self.velocity = pygame.Vector2(0.0, speed)
        self.points = points
        self.rect.center = (round(self.position.x), round(self.position.y))

    def update(self, dt: float, playfield: pygame.Rect) -> None:
        # Побег за нижнюю границу поля — отдельный, явный шаг конвейера
        # обновления (Game.resolve_enemy_escapes), поэтому здесь враг
        # только двигается и не убивает себя сам.
        self.position += self.velocity * dt
        self.rect.center = (round(self.position.x), round(self.position.y))


class Explosion(pygame.sprite.Sprite):
    """Анимация взрыва — тот же while-based аккумулятор времени, что и на
    странице 20.23: длинный кадр продвигает несколько кадров анимации
    подряд, а не теряет остаток времени."""

    def __init__(self, frames: list[pygame.Surface], center: tuple[float, float]) -> None:
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_time = 0.0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center)

    def update(self, dt: float) -> None:
        self.animation_time += dt
        while self.animation_time >= EXPLOSION_FRAME_INTERVAL:
            self.animation_time -= EXPLOSION_FRAME_INTERVAL
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
                return
            self.image = self.frames[self.frame_index]
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)


# ---------------------------------------------------------------------------
# Game — владеет всем состоянием и управляет игровым циклом
# ---------------------------------------------------------------------------

class Game:
    def __init__(self, *, rng: random.Random | None = None, debug: bool = False) -> None:
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass   # нет звукового устройства — игра всё равно должна запуститься

        self.screen = pygame.display.set_mode((SHIRINA, VYSOTA))
        pygame.display.set_caption("Космический шутер")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 56)
        self.font_small = pygame.font.SysFont(None, 22)

        self.assets = AssetStore(IMAGE_DIR, AUDIO_DIR)
        self.rng = rng if rng is not None else random.Random()
        self.debug = debug

        self.playfield = pygame.Rect(0, HUD_HEIGHT, SHIRINA, VYSOTA - HUD_HEIGHT)

        self.state = GameStatus.MENU
        self.bullets: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.explosions: pygame.sprite.Group = pygame.sprite.Group()
        self.stars: list[Star] = []

        self.player = self._make_player()
        self.score = 0
        self.high_score = 0
        self.lives = STARTING_LIVES
        self.spawn_timer = interval_poyavleniya_vraga(0)
        self.running = True

        self._reset_stars()

    # -- сборка и сброс состояния -----------------------------------------

    def _make_player(self) -> Player:
        image = self.assets.images["player_ship"]
        center = (SHIRINA / 2, self.playfield.bottom - image.get_height())
        return Player(image, center)

    def _reset_stars(self) -> None:
        self.stars = [
            Star(
                x=self.rng.uniform(0, SHIRINA),
                y=self.rng.uniform(self.playfield.top, self.playfield.bottom),
                speed=self.rng.uniform(STAR_MIN_SPEED, STAR_MAX_SPEED),
                radius=self.rng.choice((1, 1, 2)),
                color=self.rng.choice(STAR_COLORS),
            )
            for _ in range(STAR_COUNT)
        ]

    def start_new_game(self) -> None:
        """Полный сброс контракта перезапуска (раздел 21.19 сайта): игрок,
        пули, враги, взрывы, счёт, жизни, таймер спавна, кулдаун выстрела и
        неуязвимость возвращаются к начальному состоянию. Рекорд сессии
        (high_score) сознательно НЕ сбрасывается."""
        self.bullets.empty()
        self.enemies.empty()
        self.explosions.empty()
        self.player = self._make_player()
        self.score = 0
        self.lives = STARTING_LIVES
        self.spawn_timer = interval_poyavleniya_vraga(0)
        self._reset_stars()
        self.state = GameStatus.PLAYING

    def toggle_pause(self) -> None:
        if self.state is GameStatus.PLAYING:
            self.state = GameStatus.PAUSED
        elif self.state is GameStatus.PAUSED:
            self.state = GameStatus.PLAYING

    # -- ввод ---------------------------------------------------------------

    def handle_events(self) -> None:
        """Разовые события — переходы между состояниями. QUIT и Esc
        работают из любого состояния."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RETURN:
                    if self.state in (GameStatus.MENU, GameStatus.GAME_OVER):
                        self.start_new_game()
                elif event.key == pygame.K_p:
                    self.toggle_pause()
                elif event.key == pygame.K_F3:
                    self.debug = not self.debug

    def handle_input(self, dt: float) -> None:
        """Удерживаемые клавиши — движение и стрельба. Работает только в
        PLAYING: это гарантирует, что в PAUSED/MENU/GAME_OVER корабль не
        реагирует на управление (раздел 21.18 сайта)."""
        if self.state is not GameStatus.PLAYING:
            return

        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
            keys[pygame.K_DOWN] - keys[pygame.K_UP],
        )
        self.player.move(direction, dt, self.playfield)
        self.player.update_timers(dt)

        if keys[pygame.K_SPACE] and self.player.fire_cooldown <= 0.0:
            self._spawn_bullet()
            self.player.fire_cooldown = FIRE_INTERVAL

    # -- спавн ----------------------------------------------------------

    def _spawn_bullet(self) -> None:
        image = self.assets.images["bullet"]
        center = (self.player.rect.centerx, self.player.rect.top)
        self.bullets.add(Bullet(image, center))
        self.assets.play("laser")

    def _spawn_enemy(self) -> None:
        spec = vybrat_tip_vraga(self.rng, self.score)
        image = self.assets.images[spec.image_key]
        x = x_poyavleniya_vraga(self.rng, image.get_width(), self.playfield) + image.get_width() / 2
        y = self.playfield.top - image.get_height() / 2
        speed = spec.base_speed * mnozhitel_skorosti_vraga(self.score)
        self.enemies.add(Enemy(image, (x, y), spec.points, speed))

    def _spawn_explosion(self, center: tuple[float, float]) -> None:
        self.explosions.add(Explosion(self.assets.explosion_frames, center))
        self.assets.play("explosion")

    # -- столкновения -----------------------------------------------------

    def resolve_bullet_enemy_collisions(self) -> int:
        """pygame.sprite.groupcollide() удаляет столкнувшиеся спрайты из
        обеих групп сразу. Один и тот же враг может попасть в результат
        только один раз (он один физический объект), но если сразу
        НЕСКОЛЬКО пуль задели его в этом кадре, они всё равно вернут его
        как один и тот же объект в разных списках-значениях — поэтому
        подсчёт очков идёт через множество (set), а не суммированием по
        всем найденным парам, иначе один враг был бы засчитан дважды."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        destroyed = {vrag for vragi in collisions.values() for vrag in vragi}
        for vrag in destroyed:
            self._spawn_explosion(vrag.rect.center)
        return ochki_za_unichtozhennyh(destroyed)

    def resolve_enemy_player_collisions(self) -> bool:
        """Столкнувшиеся враги удаляются безусловно. Но берёт ли игрок
        урон — решает отдельная проверка неуязвимости в _update_playing():
        так три одновременно столкнувшихся врага не отнимают три жизни
        разом (раздел 21.16 сайта)."""
        hit = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for vrag in hit:
            self._spawn_explosion(vrag.rect.center)
        return len(hit) > 0

    def resolve_enemy_escapes(self) -> int:
        """Враг, полностью пересекший нижнюю границу игрового поля, стоит
        игроку одну жизнь за каждого сбежавшего — правило намеренно
        простое и явное, а не выведено случайно из порядка мутации списка."""
        escaped = [vrag for vrag in self.enemies if vrag.rect.top > self.playfield.bottom]
        for vrag in escaped:
            vrag.kill()
        return len(escaped)

    # -- обновление и отрисовка --------------------------------------------

    def update(self, dt: float) -> None:
        dt = min(dt, MAX_DT)
        self.handle_input(dt)
        if self.state is GameStatus.PLAYING:
            self._update_playing(dt)

    def _update_playing(self, dt: float) -> None:
        """Порядок обновления одного кадра (разделы 21.14–21.16 сайта):
        1) ввод и движение игрока уже обработаны в handle_input();
        2) пули; 3) враги; 4) взрывы; 5) звёзды;
        6) появление новых врагов (с сохранением остатка времени сверх интервала);
        7) столкновения пуль с врагами;
        8) столкновения врагов с игроком;
        9) враги, покинувшие игровое поле;
        10) обновление счёта/жизней и, если нужно, переход в GAME_OVER."""
        self.bullets.update(dt, self.playfield)
        self.enemies.update(dt, self.playfield)
        self.explosions.update(dt)
        self._update_stars(dt)

        self.spawn_timer -= dt
        while self.spawn_timer <= 0.0:
            self._spawn_enemy()
            self.spawn_timer += interval_poyavleniya_vraga(self.score)

        self.score += self.resolve_bullet_enemy_collisions()

        collided = self.resolve_enemy_player_collisions()
        if collided and not self.player.is_invulnerable:
            self.lives -= 1
            self.player.take_hit()
            self.assets.play("player_hit")

        self.lives -= self.resolve_enemy_escapes()

        self.high_score = max(self.high_score, self.score)
        if self.lives <= 0:
            self.lives = 0
            self.state = GameStatus.GAME_OVER

    def _update_stars(self, dt: float) -> None:
        for star in self.stars:
            star.y += star.speed * dt
            if star.y > self.playfield.bottom:
                star.y = self.playfield.top
                star.x = self.rng.uniform(0, SHIRINA)

    def render(self) -> None:
        self.screen.fill(BG_COLOR)
        self._render_stars()
        self.enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        if self.player.is_invulnerable:
            # Ровное кольцо, а не мигание — спокойный, не раздражающий
            # индикатор временной неуязвимости (раздел 21.16 сайта).
            pygame.draw.circle(self.screen, ACCENT_COLOR, self.player.rect.center, self.player.rect.width // 2 + 6, width=2)
        self.explosions.draw(self.screen)
        if self.debug:
            self._render_debug_overlay()
        self._render_hud()

        if self.state is GameStatus.MENU:
            self._render_menu_overlay()
        elif self.state is GameStatus.PAUSED:
            self._render_pause_overlay()
        elif self.state is GameStatus.GAME_OVER:
            self._render_game_over_overlay()

        pygame.display.flip()

    def _render_stars(self) -> None:
        for star in self.stars:
            pygame.draw.circle(self.screen, star.color, (round(star.x), round(star.y)), star.radius)

    def _render_hud(self) -> None:
        pygame.draw.rect(self.screen, HUD_BG_COLOR, (0, 0, SHIRINA, HUD_HEIGHT))
        pygame.draw.line(self.screen, HUD_BORDER_COLOR, (0, HUD_HEIGHT), (SHIRINA, HUD_HEIGHT), 2)

        schet_tekst = self.font.render(f"Счёт: {self.score}", True, HUD_TEXT_COLOR)
        self.screen.blit(schet_tekst, (14, 12))

        zhizni_tekst = self.font.render(f"Жизни: {self.lives}", True, HUD_TEXT_COLOR)
        rect = zhizni_tekst.get_rect(topright=(SHIRINA - 14, 12))
        self.screen.blit(zhizni_tekst, rect)

        volna_tekst = self.font_small.render(f"Волна {nomer_volny(self.score)}", True, ACCENT_COLOR)
        self.screen.blit(volna_tekst, (14, 38))

        if self.high_score > 0:
            rekord_tekst = self.font_small.render(f"Рекорд: {self.high_score}", True, ACCENT_COLOR)
            rekord_rect = rekord_tekst.get_rect(topright=(SHIRINA - 14, 38))
            self.screen.blit(rekord_tekst, rekord_rect)

    def _render_debug_overlay(self) -> None:
        pygame.draw.rect(self.screen, (255, 80, 80), self.player.rect, width=1)
        for vrag in self.enemies:
            pygame.draw.rect(self.screen, (255, 80, 80), vrag.rect, width=1)
        for pulya in self.bullets:
            pygame.draw.rect(self.screen, (255, 80, 80), pulya.rect, width=1)
        fps_tekst = self.font_small.render(f"FPS: {self.clock.get_fps():.0f}", True, (150, 255, 150))
        self.screen.blit(fps_tekst, (14, VYSOTA - 24))

    def _overlay_backdrop(self) -> pygame.Surface:
        overlay = pygame.Surface((SHIRINA, VYSOTA), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        return overlay

    def _render_menu_overlay(self) -> None:
        self.screen.blit(self._overlay_backdrop(), (0, 0))
        stroki = [
            ("КОСМИЧЕСКИЙ ШУТЕР", self.font_big, ACCENT_COLOR),
            ("", self.font_small, HUD_TEXT_COLOR),
            ("Enter — начать", self.font, HUD_TEXT_COLOR),
            ("Стрелки — движение", self.font_small, HUD_TEXT_COLOR),
            ("Space — огонь", self.font_small, HUD_TEXT_COLOR),
            ("P — пауза", self.font_small, HUD_TEXT_COLOR),
            ("Esc — выход", self.font_small, HUD_TEXT_COLOR),
        ]
        self._render_center_block(stroki, VYSOTA // 2 - 120)

    def _render_pause_overlay(self) -> None:
        self.screen.blit(self._overlay_backdrop(), (0, 0))
        stroki = [
            ("ПАУЗА", self.font_big, ACCENT_COLOR),
            ("P — продолжить", self.font, HUD_TEXT_COLOR),
        ]
        self._render_center_block(stroki, VYSOTA // 2 - 60)

    def _render_game_over_overlay(self) -> None:
        self.screen.blit(self._overlay_backdrop(), (0, 0))
        stroki = [
            ("ИГРА ОКОНЧЕНА", self.font_big, WARNING_COLOR),
            (f"Счёт: {self.score}", self.font, HUD_TEXT_COLOR),
            (f"Рекорд сессии: {self.high_score}", self.font_small, ACCENT_COLOR),
            ("Enter — заново", self.font, HUD_TEXT_COLOR),
            ("Esc — выход", self.font_small, HUD_TEXT_COLOR),
        ]
        self._render_center_block(stroki, VYSOTA // 2 - 120)

    def _render_center_block(self, stroki: list[tuple[str, pygame.font.Font, tuple[int, int, int]]], top: int) -> None:
        y = top
        for tekst, shrift, cvet in stroki:
            if not tekst:
                y += shrift.get_height() // 2
                continue
            poverhnost = shrift.render(tekst, True, cvet)
            rect = poverhnost.get_rect(center=(SHIRINA // 2, y))
            self.screen.blit(poverhnost, rect)
            y += shrift.get_height() + 6

    # -- цикл ---------------------------------------------------------------

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
