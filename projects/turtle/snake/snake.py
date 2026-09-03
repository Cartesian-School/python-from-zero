"""Игра «Змейка» на Turtle — финальная версия (глава 19).

Модель игры (GameState и чистые функции next_head/move_snake/is_wall_collision/
is_self_collision/choose_food/calculate_delay) не знает о Turtle вообще —
её можно импортировать и тестировать без окна. SnakeApp отвечает за экран,
клавиатуру и один игровой тик через screen.ontimer() — без busy-цикла и
без time.sleep().

Каждая запланированная через screen.ontimer() задача принадлежит ровно
одному "поколению" (generation). restart() — и, что важно, обе стороны
toggle_pause() тоже — увеличивают self._generation; просроченный callback,
захвативший старое поколение, видит несовпадение и немедленно завершается,
ничего не планируя дальше (раздел 19.22 разбирает это подробно, включая
конкретный баг, который это предотвращает: если возобновление случается
раньше, чем успевает сработать callback, запланированный до паузы, одного
только "тик проверяет status" недостаточно — нужно инвалидировать поколение
сразу в момент паузы, а не полагаться на то, что просроченный тик сам себя
узнает).

Запуск: python snake.py
"""

from __future__ import annotations

import random
import turtle
from dataclasses import dataclass, field
from enum import Enum

STEP = 20
FIELD_HALF = 280  # легальные координаты центра сегмента: -280..280 с шагом STEP

# HUD — отдельная полоса НАД игровым полем, а не поверх него (раздел 19.32).
# Табло рисуется на HUD_Y > FIELD_HALF, то есть строго за пределами легальных
# координат змейки/еды: is_wall_collision() уже гарантирует |y| <= FIELD_HALF
# для любой игровой позиции, так что HUD физически не может перекрыть клетку,
# в которой окажется змейка или еда.
HUD_HEIGHT = 80
HUD_Y = FIELD_HALF + HUD_HEIGHT // 2
WINDOW_WIDTH = 2 * (FIELD_HALF + STEP)
WINDOW_HEIGHT = WINDOW_WIDTH + HUD_HEIGHT

BASE_DELAY_MS = 140
MIN_DELAY_MS = 60
SPEED_STEP_SCORE = 50  # за каждые SPEED_STEP_SCORE очков...
SPEED_STEP_MS = 10  # ...задержка уменьшается на SPEED_STEP_MS (не ниже MIN_DELAY_MS)
FOOD_SCORE = 10

BG_COLOR = "black"
HEAD_COLOR = "white"
BODY_COLOR = "#4ECDC4"
FOOD_COLOR = "#FF5D5D"
TEXT_COLOR = "white"

Position = tuple[int, int]


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


DIRECTION_VECTORS: dict[Direction, Position] = {
    Direction.UP: (0, STEP),
    Direction.DOWN: (0, -STEP),
    Direction.LEFT: (-STEP, 0),
    Direction.RIGHT: (STEP, 0),
}

OPPOSITE: dict[Direction, Direction] = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


class GameStatus(Enum):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    WON = "won"  # змейка заняла все легальные клетки поля — свободных клеток для еды не осталось


@dataclass
class GameState:
    """Чистые данные игры — ни одного объекта Turtle внутри (раздел 19.27).

    food может быть None: это не баг и не временное состояние, а честное
    представление того, что свободных клеток для новой еды не осталось
    (раздел 19.18) — единственный случай, когда это происходит, это WON."""

    snake: list[Position] = field(default_factory=lambda: [(0, 0)])
    direction: Direction = Direction.RIGHT
    next_direction: Direction = Direction.RIGHT
    food: Position | None = (0, 0)
    score: int = 0
    high_score: int = 0
    status: GameStatus = GameStatus.READY
    delay_ms: int = BASE_DELAY_MS


# --------------------------------------------------------------------------
# Чистая игровая логика — без единого обращения к turtle (раздел 19.26)
# --------------------------------------------------------------------------

def is_reverse(current: Direction, requested: Direction) -> bool:
    """True, если requested развернул бы змейку на 180° прямо в собственное тело."""
    return OPPOSITE[current] == requested


def next_head(head: Position, direction: Direction) -> Position:
    dx, dy = DIRECTION_VECTORS[direction]
    return (head[0] + dx, head[1] + dy)


def move_snake(snake: list[Position], new_head: Position, *, grow: bool) -> list[Position]:
    """Новая голова + старое тело; при grow=False хвост отбрасывается — тот же
    результат, что и «подтягивание» сегментов друг за другом, но без цикла."""
    if grow:
        return [new_head, *snake]
    return [new_head, *snake[:-1]]


def is_wall_collision(head: Position, *, half: int = FIELD_HALF) -> bool:
    x, y = head
    return abs(x) > half or abs(y) > half


def is_self_collision(new_head: Position, body_after_move: list[Position]) -> bool:
    """body_after_move — тело ПОСЛЕ move_snake, без учёта самой головы
    (snake[1:]). Если хвост в этом тике освободил клетку (змейка не растёт),
    его в body_after_move уже нет — заехать туда законно."""
    return new_head in body_after_move


def all_cells(*, half: int = FIELD_HALF, step: int = STEP) -> tuple[Position, ...]:
    coords = range(-half, half + 1, step)
    return tuple((x, y) for x in coords for y in coords)


def choose_food(snake: list[Position], rng: random.Random, *, half: int = FIELD_HALF, step: int = STEP) -> Position | None:
    """Случайная свободная клетка сетки — никогда не внутри змейки (раздел 19.18).

    Возвращает None, если свободных клеток не осталось (змейка заняла всё
    поле). Это не крайний случай, о котором можно забыть, — вызывающий код
    обязан явно обработать None, а не подставлять первую попавшуюся клетку
    змейки: еда никогда не может совпадать со змейкой, даже на до предела
    заполненном поле."""
    occupied = set(snake)
    free = tuple(cell for cell in all_cells(half=half, step=step) if cell not in occupied)
    if not free:
        return None
    return rng.choice(free)


def calculate_delay(
    score: int,
    *,
    base_ms: int = BASE_DELAY_MS,
    min_ms: int = MIN_DELAY_MS,
    step_score: int = SPEED_STEP_SCORE,
    step_ms: int = SPEED_STEP_MS,
) -> int:
    steps = score // step_score
    return max(min_ms, base_ms - steps * step_ms)


def new_game_state(rng: random.Random, *, high_score: int = 0) -> GameState:
    snake = [(0, 0)]
    return GameState(
        snake=snake,
        direction=Direction.RIGHT,
        next_direction=Direction.RIGHT,
        food=choose_food(snake, rng),
        score=0,
        high_score=high_score,
        status=GameStatus.READY,
        delay_ms=BASE_DELAY_MS,
    )


# --------------------------------------------------------------------------
# SnakeApp — экран, клавиатура, один тик за раз; модель отделена от отображения
# --------------------------------------------------------------------------

class SnakeApp:
    def __init__(self, *, rng: random.Random | None = None) -> None:
        self.rng = rng if rng is not None else random.Random()
        self.state = new_game_state(self.rng)
        self._generation = 0
        self._segment_pool: list[turtle.Turtle] = []

        self.screen = turtle.Screen()
        self.screen.title("Змейка")
        self.screen.bgcolor(BG_COLOR)
        self.screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, startx=0, starty=0)
        # Мир игры шире, чем окно: HUD-полоса добавлена ТОЛЬКО сверху, а не
        # поровну с обеих сторон, поэтому игровое поле остаётся у нижнего
        # края ровно там же, где было без HUD (раздел 19.32).
        half = WINDOW_WIDTH / 2
        self.screen.setworldcoordinates(-half, -half, half, half + HUD_HEIGHT)
        self.screen.tracer(0)

        self.head = self._make_turtle("square", HEAD_COLOR)
        self.food_turtle = self._make_turtle("circle", FOOD_COLOR)
        self.scoreboard = self._make_text_turtle()
        self.overlay = self._make_text_turtle()

        self.bind_keys()
        self.render()

    @staticmethod
    def _make_turtle(shape: str, color: str) -> turtle.Turtle:
        t = turtle.Turtle()
        t.speed(0)
        t.shape(shape)
        t.color(color)
        t.penup()
        return t

    @staticmethod
    def _make_text_turtle() -> turtle.Turtle:
        t = turtle.Turtle()
        t.speed(0)
        t.color(TEXT_COLOR)
        t.penup()
        t.hideturtle()
        return t

    def _ensure_segment_pool(self, needed: int) -> None:
        while len(self._segment_pool) < needed:
            self._segment_pool.append(self._make_turtle("square", BODY_COLOR))

    # ---------- клавиатура ----------
    def bind_keys(self) -> None:
        """Клавиши привязываются по keysym, а keysym буквенной клавиши зависит
        от раскладки: в русской раскладке физическая W даёт Cyrillic_tse, а R —
        Cyrillic_ka. Поэтому WASD и R привязаны сразу в трёх видах — латиница,
        латиница с Shift/CapsLock и кириллица, — иначе половина управления
        молчала бы ровно тогда, когда у игрока включена русская раскладка.
        Стрелки и space от раскладки не зависят."""
        self.screen.listen()
        for key, direction in (
            ("Up", Direction.UP), ("Down", Direction.DOWN),
            ("Left", Direction.LEFT), ("Right", Direction.RIGHT),
            ("w", Direction.UP), ("s", Direction.DOWN),
            ("a", Direction.LEFT), ("d", Direction.RIGHT),
            ("W", Direction.UP), ("S", Direction.DOWN),
            ("A", Direction.LEFT), ("D", Direction.RIGHT),
            # те же физические клавиши в русской раскладке: Ц, Ы, Ф, В
            ("Cyrillic_tse", Direction.UP), ("Cyrillic_yeru", Direction.DOWN),
            ("Cyrillic_ef", Direction.LEFT), ("Cyrillic_ve", Direction.RIGHT),
            ("Cyrillic_TSE", Direction.UP), ("Cyrillic_YERU", Direction.DOWN),
            ("Cyrillic_EF", Direction.LEFT), ("Cyrillic_VE", Direction.RIGHT),
        ):
            self.screen.onkeypress(lambda d=direction: self.request_direction(d), key)
        self.screen.onkeypress(self.toggle_pause, "space")
        # R — та же клавиша, что и русская К
        for key in ("r", "R", "Cyrillic_ka", "Cyrillic_KA"):
            self.screen.onkeypress(self.restart, key)

    def request_direction(self, direction: Direction) -> None:
        """Клавиша только ЗАПРАШИВАЕТ направление — реальный поворот происходит
        на следующем тике (раздел 19.31, Debug Lab 5). Проверяем разворот против
        direction, которое тик применит СЕЙЧАС, а не против уже запрошенного
        next_direction — иначе быстрая пара клавиш перед одним тиком могла бы
        протащить разворот на 180° (раздел 19.31, Debug Lab 6)."""
        if is_reverse(self.state.direction, direction):
            return
        self.state.next_direction = direction
        if self.state.status is GameStatus.READY:
            self.state.status = GameStatus.RUNNING
            self._schedule_next_tick()

    # ---------- один тик и планирование следующего ----------
    def game_tick(self) -> None:
        """Один игровой тик: применить направление, подвинуть голову, проверить
        еду и столкновения, обновить модель, отрисовать. Не планирует сам себя —
        это отдельно, в _schedule_next_tick()/_on_timer(), поэтому game_tick()
        безопасно вызывать напрямую из тестов без реального таймера."""
        if self.state.status is not GameStatus.RUNNING:
            return

        state = self.state
        state.direction = state.next_direction
        head = next_head(state.snake[0], state.direction)
        grow = head == state.food

        if is_wall_collision(head):
            state.status = GameStatus.GAME_OVER
            self.render()
            self._show_overlay("GAME OVER", f"Счёт: {state.score}  |  R — новая игра")
            return

        new_snake = move_snake(state.snake, head, grow=grow)
        if is_self_collision(head, new_snake[1:]):
            state.status = GameStatus.GAME_OVER
            self.render()
            self._show_overlay("GAME OVER", f"Счёт: {state.score}  |  R — новая игра")
            return

        state.snake = new_snake
        if grow:
            state.score += FOOD_SCORE
            state.high_score = max(state.high_score, state.score)
            next_food = choose_food(state.snake, self.rng)
            if next_food is None:
                # поле заполнено целиком — свободной клетки для новой еды не
                # осталось. Это победа, а не ошибка: явный терминальный статус,
                # а не еда, тайком поставленная внутрь змейки (раздел 19.18).
                state.food = None
                state.status = GameStatus.WON
                self.render()
                self._show_overlay("ПОБЕДА", f"Поле заполнено — счёт: {state.score}")
                return
            state.food = next_food
            state.delay_ms = calculate_delay(state.score)

        self.render()

    def _schedule_next_tick(self) -> None:
        generation = self._generation
        self.screen.ontimer(lambda: self._on_timer(generation), self.state.delay_ms)

    def _on_timer(self, generation: int) -> None:
        if generation != self._generation:
            return  # просроченная цепочка от игры до restart() — само гасится
        self.game_tick()
        # game_tick() -> render() -> screen.update() может успеть обработать
        # событие Pause/Resume/Restart прямо ВНУТРИ этого вызова и изменить
        # поколение реентерабельно — колбэк, устаревший во время тика, не
        # должен планировать продолжение (иначе новая цепочка, запущенная
        # тем событием, окажется не единственной).
        if generation != self._generation:
            return
        if self.state.status is GameStatus.RUNNING:
            self._schedule_next_tick()

    # ---------- pause / restart ----------
    def toggle_pause(self) -> None:
        if self.state.status is GameStatus.RUNNING:
            self._generation += 1  # обрывает уже запланированный тик немедленно, а не когда он сработает
            self.state.status = GameStatus.PAUSED
            self._show_overlay("ПАУЗА", "Space — продолжить")
        elif self.state.status is GameStatus.PAUSED:
            self._generation += 1  # новое поколение — ровно одна свежая цепочка тиков
            self.state.status = GameStatus.RUNNING
            self._clear_overlay()
            self._schedule_next_tick()

    def restart(self) -> None:
        self._generation += 1  # обрывает любую ещё тикающую цепочку прошлой игры
        high_score = self.state.high_score
        self.state = new_game_state(self.rng, high_score=high_score)
        self._clear_overlay()
        self.render()

    # ---------- отображение: модель -> Turtle ----------
    def render(self) -> None:
        self.head.goto(*self.state.snake[0])

        body = self.state.snake[1:]
        self._ensure_segment_pool(len(body))
        for i, segment in enumerate(self._segment_pool):
            if i < len(body):
                segment.showturtle()
                segment.goto(*body[i])
            else:
                segment.hideturtle()

        if self.state.food is not None:
            self.food_turtle.showturtle()
            self.food_turtle.goto(*self.state.food)
        else:
            self.food_turtle.hideturtle()  # WON — свободных клеток для еды не осталось
        self._render_scoreboard()
        self.screen.update()

    def _render_scoreboard(self) -> None:
        self.scoreboard.clear()
        self.scoreboard.goto(0, HUD_Y)  # HUD, а не игровое поле — раздел 19.32
        self.scoreboard.write(
            f"Счёт: {self.state.score}   Рекорд: {self.state.high_score}",
            align="center", font=("Arial", 16, "normal"),
        )

    def _show_overlay(self, title: str, subtitle: str) -> None:
        self.overlay.clear()
        # screen.update() re-raises every VISIBLE turtle's own shape to the
        # front of the canvas stacking order (so a moving turtle icon always
        # stays above the trail it leaves) — head/food/each body segment all
        # get this treatment. write() text does not, so on a crowded board
        # (at the extreme: GameStatus.WON, where the snake covers the whole
        # field) the overlay could end up stacked BEHIND the game pieces
        # instead of on top of them. Let update() do its usual re-raising
        # first, then explicitly raise exactly the items this call just
        # created — so the overlay is guaranteed visible on top regardless
        # of how many pieces are on screen.
        canvas = self.screen.getcanvas()
        before = set(canvas.find_all())
        self.overlay.goto(0, 10)
        self.overlay.write(title, align="center", font=("Arial", 24, "bold"))
        self.overlay.goto(0, -20)
        self.overlay.write(subtitle, align="center", font=("Arial", 14, "normal"))
        new_items = [item for item in canvas.find_all() if item not in before]
        self.screen.update()
        for item in new_items:
            canvas.tag_raise(item)
        canvas.update_idletasks()  # flush the corrected stacking order to the screen

    def _clear_overlay(self) -> None:
        self.overlay.clear()

    # ---------- запуск ----------
    def run(self) -> None:
        self.screen.mainloop()


def main() -> None:
    app = SnakeApp()
    app.run()


if __name__ == "__main__":
    main()
