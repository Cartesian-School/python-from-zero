#!/usr/bin/env python3
"""Генерирует настоящие скриншоты Turtle-змейки для главы 19.

Каждый скриншот получен, запустив реальный код проекта (класс SnakeApp из
snake.py) и подведя его к нужному состоянию через его собственные методы
(request_direction/game_tick/toggle_pause/restart) — не имитация HTML/CSS и
не нарисованный вручную интерфейс. Позиции головы/еды иногда задаются прямой
записью в app.state (это просто данные — тот же приём, что и в тестах),
но рисует их всегда настоящий Turtle через app.render().

Требует headless X-сервер (xvfb-run).
Использование: xvfb-run -a python3 scripts/generate_chapter_19_outputs.py
"""

import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageGrab

_LABEL_FONT = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18
)  # шрифт по умолчанию в Pillow не знает кириллицу — подписи вроде "тик N" превращались бы в тофу-квадраты

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-19" / "output"
sys.path.insert(0, str(ROOT / "projects" / "turtle" / "snake"))

import snake as s  # noqa: E402

WIN_W, WIN_H = 600, 600


def _autocrop(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    bg = Image.new("RGB", rgb.size, (0, 0, 0))
    bbox = ImageChops.difference(rgb, bg).getbbox()
    return img.crop(bbox) if bbox else img


def capture(name: str, app: "s.SnakeApp") -> Image.Image:
    app.screen.update()
    img = ImageGrab.grab(bbox=(0, 0, WIN_W, WIN_H))
    img = _autocrop(img)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    img.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({img.size[0]}x{img.size[1]})")
    return img


_APP: "s.SnakeApp | None" = None


def get_app() -> "s.SnakeApp":
    """turtle.Screen() — единственный на процесс синглтон: Screen.bye() рвёт
    его насовсем (следующий Screen() бросает Terminator), поэтому один и тот
    же SnakeApp переиспользуется для всех сценариев, а не пересоздаётся."""
    global _APP
    if _APP is None:
        _APP = s.SnakeApp(rng=random.Random(0))
    return _APP


def reset_app(seed: int) -> "s.SnakeApp":
    app = get_app()
    app.rng = random.Random(seed)
    app.state = s.new_game_state(app.rng)
    app._clear_overlay()
    app.render()  # прячет «лишние» сегменты пула от предыдущего сценария
    return app


def close(app: "s.SnakeApp") -> None:
    pass  # см. get_app(): окно закрывается один раз, в конце скрипта


def run(app: "s.SnakeApp", direction: "s.Direction", ticks: int) -> None:
    app.request_direction(direction)
    for _ in range(ticks):
        app.game_tick()


def compose_strip(names: list[str], out_name: str, *, labels: list[str] | None = None) -> None:
    """Склеивает уже сохранённые реальные скриншоты в один горизонтальный
    ряд — тот же масштаб, стрелка между кадрами, необязательная подпись под
    каждым. Ничего не дорисовывает ВНУТРИ игрового поля — только компонует
    и подписывает снаружи (раздел 19.39)."""
    imgs = [Image.open(OUT_DIR / f"{n}.png").convert("RGB") for n in names]
    h = max(im.height for im in imgs)
    gap = 56
    label_h = 36 if labels else 0
    total_w = sum(im.width for im in imgs) + gap * (len(imgs) - 1)
    strip = Image.new("RGB", (total_w, h + label_h), "#0D0230")
    draw = ImageDraw.Draw(strip)
    x = 0
    for i, im in enumerate(imgs):
        strip.paste(im, (x, 0))
        if labels:
            text_w = draw.textlength(labels[i], font=_LABEL_FONT)
            draw.text(
                (x + im.width / 2 - text_w / 2, h + 8),
                labels[i], fill="#FFFFFF", font=_LABEL_FONT,
            )
        x += im.width
        if i < len(imgs) - 1:
            mid_y = h // 2
            draw.line([(x + 10, mid_y), (x + gap - 10, mid_y)], fill="#B9A0FC", width=4)
            draw.polygon(
                [(x + gap - 10, mid_y - 8), (x + gap - 10, mid_y + 8), (x + gap, mid_y)],
                fill="#B9A0FC",
            )
            x += gap
    path = OUT_DIR / f"{out_name}.png"
    strip.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({strip.size[0]}x{strip.size[1]})")


# ---------------------------------------------------------------------------
# Сценарии
# ---------------------------------------------------------------------------

def empty_field() -> None:
    app = reset_app(seed=1)
    app.state.food = (100, 40)
    app.render()
    capture("snake-empty-field", app)
    close(app)


def head_food() -> None:
    app = reset_app(seed=2)
    app.state.food = (60, 0)
    app.render()
    capture("snake-head-food", app)
    close(app)


def moving_right_and_growing() -> None:
    app = reset_app(seed=3)
    app.state.food = (200, 0)
    run(app, s.Direction.RIGHT, 1)
    capture("snake-first-move", app)

    app.state.food = s.next_head(app.state.snake[0], s.Direction.RIGHT)
    capture("snake-food-eaten-before", app)
    run(app, s.Direction.RIGHT, 1)
    # choose_food() честно выбрала следующую еду случайно — для этого кадра
    # переставим её подальше от табло счёта, чтобы не перекрывать текст.
    app.state.food = (100, -100)
    app.render()
    capture("snake-food-eaten-after", app)
    capture("snake-one-segment", app)

    app.state.food = (240, 40)
    run(app, s.Direction.RIGHT, 3)
    capture("snake-body-follow-1", app)
    run(app, s.Direction.RIGHT, 1)
    capture("snake-body-follow-2", app)
    run(app, s.Direction.RIGHT, 1)
    capture("snake-body-follow-3", app)
    capture("snake-moving-right", app)
    capture("snake-score", app)

    run(app, s.Direction.UP, 3)
    capture("snake-moving-up", app)

    close(app)


def growing_and_speed() -> None:
    app = reset_app(seed=4)
    for i in range(6):
        app.state.food = s.next_head(app.state.snake[0], s.Direction.RIGHT)
        run(app, s.Direction.RIGHT, 1)
    capture("snake-growing", app)
    capture("snake-normal-speed", app)
    close(app)


def fast_speed() -> None:
    app = reset_app(seed=5)
    # Высокий счёт достигается напрямую в состоянии — снимок демонстрирует
    # эффект calculate_delay(), а не 45 честных тиков ради того же числа.
    app.state.snake = [(-40, 0), (-60, 0), (-80, 0), (-100, 0), (-120, 0)]
    app.state.score = 450
    app.state.high_score = 450
    app.state.delay_ms = s.calculate_delay(app.state.score)
    app.state.food = (60, 100)
    app.render()
    assert app.state.delay_ms == s.MIN_DELAY_MS
    capture("snake-fast-speed", app)
    close(app)


def wall_collision() -> None:
    app = reset_app(seed=6)
    # голова уже на легальной границе (280) — следующий шаг вправо выведет
    # её за пределы поля (see 19-22: граница — это координата ЦЕНТРА сегмента)
    app.state.snake = [(280, 0)]
    app.state.direction = s.Direction.RIGHT
    app.state.next_direction = s.Direction.RIGHT
    app.state.score = 40
    app.state.high_score = 40
    app.state.food = (-100, 100)
    app.state.status = s.GameStatus.RUNNING
    app.game_tick()
    assert app.state.status is s.GameStatus.GAME_OVER
    capture("snake-wall-collision", app)
    close(app)


def self_collision_and_game_over() -> None:
    app = reset_app(seed=7)
    # S-образное тело: следующий шаг ВПРАВО из головы приведёт ровно в ячейку
    # пятого сегмента (не хвоста) — настоящее столкновение, а не легальный
    # заезд в клетку, которую хвост освобождает в этом же тике (раздел 19.23).
    # Сдвинуто в нижний левый угол поля, чтобы тело не пересекалось с
    # текстом оверлея GAME OVER, который всегда рисуется по центру экрана.
    ox, oy = -140, -140
    app.state.snake = [
        (ox + 0, oy + 0), (ox + 0, oy + 20), (ox + 0, oy + 40),
        (ox + 20, oy + 40), (ox + 20, oy + 20), (ox + 20, oy + 0), (ox + 20, oy - 20),
    ]
    app.state.direction = s.Direction.RIGHT
    app.state.next_direction = s.Direction.RIGHT
    app.state.score = 70
    app.state.high_score = 70
    app.state.food = (-200, -200)
    app.state.status = s.GameStatus.RUNNING
    app.game_tick()
    assert app.state.status is s.GameStatus.GAME_OVER
    capture("snake-self-collision", app)
    capture("snake-game-over", app)
    close(app)


def paused() -> None:
    app = reset_app(seed=8)
    # Ниже центра поля — иначе тело перекрывает текст оверлея «ПАУЗА»,
    # который всегда рисуется по центру экрана (та же причина, что и в
    # self_collision_and_game_over()).
    app.state.snake = [(-100, -120)]
    app.state.direction = s.Direction.RIGHT
    app.state.next_direction = s.Direction.RIGHT
    for i in range(5):
        app.state.food = s.next_head(app.state.snake[0], s.Direction.RIGHT)
        run(app, s.Direction.RIGHT, 1)
    capture("snake-running-before-pause", app)
    app.toggle_pause()
    capture("snake-paused", app)
    close(app)


def restarted_and_high_score() -> None:
    app = reset_app(seed=9)
    for i in range(4):
        app.state.food = s.next_head(app.state.snake[0], s.Direction.RIGHT)
        run(app, s.Direction.RIGHT, 1)
    assert app.state.high_score == 40
    app.restart()
    app.state.food = (140, 0)
    app.render()
    capture("snake-restarted", app)
    capture("snake-high-score", app)
    close(app)


def grid_demo() -> None:
    app = reset_app(seed=10)
    app.state.snake = [(0, 0)]
    app.state.food = (80, -40)
    app.render()

    grid = s.turtle.Turtle()
    grid.hideturtle()
    grid.speed(0)
    grid.color("#3A2E63")
    grid.penup()
    step, half = s.STEP, 120
    for x in range(-half, half + 1, step):
        grid.goto(x, -half)
        grid.pendown()
        grid.goto(x, half)
        grid.penup()
    for y in range(-half, half + 1, step):
        grid.goto(-half, y)
        grid.pendown()
        grid.goto(half, y)
        grid.penup()

    label = s.turtle.Turtle()
    label.hideturtle()
    label.speed(0)
    label.penup()
    label.color("#B9A0FC")
    label.goto(0, 10)
    label.write("head cell", align="center", font=("Arial", 10, "normal"))
    label.goto(80, -30)
    label.color(s.FOOD_COLOR)
    label.write("food cell", align="center", font=("Arial", 10, "normal"))

    app.screen.update()
    capture("snake-grid-demo", app)
    # grid/label — временные черепашки только для этого сценария; экран
    # переиспользуется дальше (см. get_app()), поэтому их след обязательно
    # стереть, иначе линии сетки и подписи «протекут» в следующие снимки.
    grid.clear()
    label.clear()
    close(app)


def final_pro() -> None:
    app = reset_app(seed=11)
    for i in range(9):
        app.state.food = s.next_head(app.state.snake[0], s.Direction.RIGHT)
        run(app, s.Direction.RIGHT, 1)
    run(app, s.Direction.UP, 3)
    app.state.food = (-140, 140)
    app.render()
    capture("snake-final-pro", app)
    close(app)


def final_overview() -> None:
    app = reset_app(seed=12)
    for i in range(5):
        app.state.food = s.next_head(app.state.snake[0], s.Direction.RIGHT)
        run(app, s.Direction.RIGHT, 1)
    run(app, s.Direction.UP, 2)
    app.state.food = (-120, 100)
    app.render()
    capture("snake-final-overview", app)
    close(app)


def build_composites() -> None:
    compose_strip(
        ["snake-body-follow-1", "snake-body-follow-2", "snake-body-follow-3"],
        "snake-body-follow-strip",
        labels=["тик N", "тик N+1", "тик N+2"],
    )
    compose_strip(
        ["snake-food-eaten-before", "snake-food-eaten-after"],
        "snake-food-eaten-strip",
        labels=["до", "после"],
    )
    compose_strip(
        ["snake-running-before-pause", "snake-paused"],
        "snake-pause-strip",
        labels=["идёт", "пауза"],
    )


if __name__ == "__main__":
    empty_field()
    head_food()
    moving_right_and_growing()
    growing_and_speed()
    fast_speed()
    wall_collision()
    self_collision_and_game_over()
    paused()
    restarted_and_high_score()
    grid_demo()
    final_pro()
    final_overview()
    build_composites()
    get_app().screen.bye()
