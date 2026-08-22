"""Регрессионный набор для чистой игровой логики главы 19 (направления,
движение, столкновения, еда, скорость) — без Turtle и без Xvfb, потому что
модель игры не зависит от экрана (раздел 19.26).
"""

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "projects" / "turtle" / "snake"))

from snake import (  # noqa: E402
    FIELD_HALF,
    HUD_HEIGHT,
    HUD_Y,
    STEP,
    Direction,
    GameState,
    GameStatus,
    all_cells,
    calculate_delay,
    choose_food,
    is_reverse,
    is_self_collision,
    is_wall_collision,
    move_snake,
    new_game_state,
    next_head,
)


# ---------- направление ----------

def test_is_reverse_blocks_only_exact_opposite():
    assert is_reverse(Direction.RIGHT, Direction.LEFT) is True
    assert is_reverse(Direction.LEFT, Direction.RIGHT) is True
    assert is_reverse(Direction.UP, Direction.DOWN) is True
    assert is_reverse(Direction.DOWN, Direction.UP) is True


def test_is_reverse_allows_90_degree_turn():
    assert is_reverse(Direction.RIGHT, Direction.UP) is False
    assert is_reverse(Direction.RIGHT, Direction.DOWN) is False
    assert is_reverse(Direction.RIGHT, Direction.RIGHT) is False


# ---------- движение головы ----------

def test_next_head_all_four_directions():
    assert next_head((0, 0), Direction.UP) == (0, STEP)
    assert next_head((0, 0), Direction.DOWN) == (0, -STEP)
    assert next_head((0, 0), Direction.LEFT) == (-STEP, 0)
    assert next_head((0, 0), Direction.RIGHT) == (STEP, 0)


# ---------- движение тела ----------

def test_move_snake_without_growth_drops_tail():
    snake = [(0, 0), (-20, 0), (-40, 0)]
    result = move_snake(snake, (20, 0), grow=False)
    assert result == [(20, 0), (0, 0), (-20, 0)]
    assert len(result) == len(snake)


def test_move_snake_with_growth_keeps_tail():
    snake = [(0, 0), (-20, 0), (-40, 0)]
    result = move_snake(snake, (20, 0), grow=True)
    assert result == [(20, 0), (0, 0), (-20, 0), (-40, 0)]
    assert len(result) == len(snake) + 1


# ---------- стены ----------

def test_wall_collision_boundary_is_safe():
    assert is_wall_collision((280, 280)) is False
    assert is_wall_collision((-280, -280)) is False


def test_wall_collision_beyond_boundary():
    assert is_wall_collision((300, 0)) is True
    assert is_wall_collision((0, -300)) is True


# ---------- самостолкновение ----------

def test_self_collision_true_when_head_enters_body():
    body_after_move = [(0, 0), (-20, 0), (-40, 0)]
    assert is_self_collision((0, 0), body_after_move) is True


def test_self_collision_false_when_tail_vacated_this_tick():
    # Змейка не растёт: move_snake() уже отбросил старый хвост, значит заехать
    # именно в клетку старого хвоста — законный ход, а не столкновение.
    snake = [(0, 0), (20, 0), (40, 0), (40, 20)]
    new_head = (40, 20)  # клетка, где ДО этого хода был хвост
    new_snake = move_snake(snake, new_head, grow=False)
    assert new_snake[1:] == [(0, 0), (20, 0), (40, 0)]  # хвост уже отброшен
    assert is_self_collision(new_head, new_snake[1:]) is False


def test_self_collision_false_for_distant_body():
    assert is_self_collision((0, 0), [(200, 200), (220, 200)]) is False


# ---------- еда ----------

def test_choose_food_is_grid_aligned():
    rng = random.Random(7)
    for _ in range(20):
        x, y = choose_food([(0, 0)], rng)
        assert x % STEP == 0
        assert y % STEP == 0


def test_choose_food_never_lands_on_snake():
    rng = random.Random(1)
    snake = [(0, 0), (-20, 0), (-40, 0), (-60, 0)]
    for _ in range(50):
        food = choose_food(snake, rng)
        assert food not in snake


def test_choose_food_deterministic_with_same_seed():
    a = choose_food([(0, 0)], random.Random(42))
    b = choose_food([(0, 0)], random.Random(42))
    assert a == b


def test_choose_food_full_board_returns_none():
    """Змейка занимает буквально каждую легальную клетку поля — choose_food()
    обязана вернуть None, а не тайком подставить клетку самой змейки
    (раздел 19.18: food ∈ FREE_CELLS, а не food = snake[0])."""
    full_snake = list(all_cells())
    assert choose_food(full_snake, random.Random(0)) is None


def test_choose_food_exactly_one_free_cell():
    """Ровно одна свободная клетка — choose_food() обязана вернуть именно её,
    без вариативности (единственный кандидат, а не случайный выбор из пустого)."""
    everything = list(all_cells())
    last_free = everything[-1]
    almost_full_snake = [cell for cell in everything if cell != last_free]
    assert choose_food(almost_full_snake, random.Random(5)) == last_free


def test_hud_band_is_outside_the_legal_playfield():
    """Табло стоит строго над легальным полем, а не поверх геймплея: любая
    легальная клетка змейки/еды имеет |y| <= FIELD_HALF, а HUD_Y — нет
    (раздел 19.32 — HUD не должен перекрывать игровые клетки)."""
    assert HUD_Y > FIELD_HALF
    legal_ys = {y for _, y in all_cells()}
    assert HUD_Y not in legal_ys
    assert HUD_HEIGHT > 0


# ---------- скорость ----------

def test_calculate_delay_decreases_with_score():
    assert calculate_delay(0) == 140
    assert calculate_delay(50) == 130
    assert calculate_delay(100) == 120


def test_calculate_delay_respects_minimum():
    assert calculate_delay(100_000) == 60
    assert calculate_delay(100_000) >= 60


# ---------- GameState / new_game_state ----------

def test_new_game_state_starts_ready_with_single_segment_snake():
    state = new_game_state(random.Random(3))
    assert state.status is GameStatus.READY
    assert state.snake == [(0, 0)]
    assert state.direction is Direction.RIGHT
    assert state.score == 0
    assert state.food != state.snake[0]


def test_game_state_holds_no_turtle_objects():
    state = GameState()
    for value in vars(state).values():
        assert type(value).__module__ != "turtle"
