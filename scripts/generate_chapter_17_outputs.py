#!/usr/bin/env python3
"""Генерирует настоящие скриншоты Tkinter-игры «Крестики-нолики» для главы 17.

Каждый скриншот получен, запустив реальный projects/tkinter/tic-tac-toe/tic_tac_toe.py
(класс TicTacToeApp) и подведя его к нужному состоянию через его собственные
методы (attempt_move/on_cell_enter/new_round/...) — не имитация HTML/CSS.

Требует headless X-сервер (xvfb-run).
Использование: xvfb-run -a python3 scripts/generate_chapter_17_outputs.py
"""

import importlib
import sys
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageGrab

_FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-17" / "output"
sys.path.insert(0, str(ROOT / "projects" / "tkinter" / "tic-tac-toe"))

import tic_tac_toe as t  # noqa: E402
import tic_tac_toe_basic as tb  # noqa: E402


def _autocrop(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    bg = Image.new("RGB", rgb.size, (0, 0, 0))
    bbox = ImageChops.difference(rgb, bg).getbbox()
    return img.crop(bbox) if bbox else img


def capture(name: str, root: tk.Tk, *, grab_w: int = 500, grab_h: int = 560) -> None:
    root.update_idletasks()
    root.update()
    img = ImageGrab.grab(bbox=(0, 0, grab_w, grab_h))
    img = _autocrop(img)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    img.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({img.size[0]}x{img.size[1]})")
    root.destroy()


def new_app() -> tuple[tk.Tk, "t.TicTacToeApp"]:
    root = tk.Tk()
    root.geometry("+0+0")
    app = t.TicTacToeApp(root)
    return root, app


def empty_board() -> None:
    root, app = new_app()
    capture("empty-board", root)


def x_first_move() -> None:
    root, app = new_app()
    app.attempt_move(4)  # X takes the center
    capture("x-first-move", root)


def x_turn() -> None:
    root, app = new_app()
    capture("x-turn", root)  # fresh round: X to move


def o_turn() -> None:
    root, app = new_app()
    app.attempt_move(0)  # X moves, turn passes to O
    capture("o-turn", root)


def mid_game() -> None:
    root, app = new_app()
    for i in (0, 4, 1, 3, 8):  # X, O, X, O, X — no winner yet
        app.attempt_move(i)
    capture("mid-game", root)


def x_win() -> None:
    root, app = new_app()
    for i in (0, 3, 1, 4, 2):  # X takes the top row
        app.attempt_move(i)
    app.cancel_pulse()  # freeze on the static highlight, not mid-pulse
    app.render()
    capture("x-win", root)


def o_win() -> None:
    root, app = new_app()
    for i in (0, 1, 3, 4, 6, 7):  # X: 0,3,6 blocked; O wins the middle column 1,4,7
        app.attempt_move(i)
    app.cancel_pulse()
    app.render()
    capture("o-win", root)


def winning_highlight() -> None:
    root, app = new_app()
    for i in (0, 1, 4, 2, 8):  # X wins the main diagonal 0,4,8
        app.attempt_move(i)
    app.cancel_pulse()
    app.render()
    capture("winning-highlight", root)


def draw() -> None:
    root, app = new_app()
    # X O X / X O O / O X X — full board, no winner
    for i in (0, 1, 2, 4, 3, 5, 7, 6, 8):
        app.attempt_move(i)
    capture("draw", root)


def hover_preview_x() -> None:
    root, app = new_app()
    app.on_cell_enter(4)  # X to move: hover shows a muted X preview
    capture("hover-preview-x", root)


def hover_preview_o() -> None:
    root, app = new_app()
    app.attempt_move(0)  # X moves, now O to move
    app.on_cell_enter(4)
    capture("hover-preview-o", root)


def scoreboard() -> None:
    root, app = new_app()
    app.state.score_x, app.state.score_o, app.state.draws = 2, 1, 1
    app.render()
    capture("scoreboard", root)


def new_round_reset() -> None:
    root, app = new_app()
    for i in (0, 3, 1, 4, 2):  # finish one round with an X win
        app.attempt_move(i)
    app.new_round()  # board resets, score from the finished round remains
    capture("new-round", root)


def new_match_reset() -> None:
    """A real New Match transition: both board and accumulated score reset."""
    root, app = new_app()
    app.state.score_x, app.state.score_o, app.state.draws = 2, 1, 1
    app.state.board = ["X", "", "", "", "O", "", "", "", "X"]
    app.state.current_player = "O"
    app.render()
    app.new_match()
    capture("new-match", root)


def new_basic_app():
    """tic_tac_toe_basic.py строит окно и виджеты на уровне модуля (раздел 17.6) —
    в отличие от TicTacToeApp, здесь нет конструктора, который можно вызвать заново.
    importlib.reload() заново выполняет код модуля и создаёт свежее окно."""
    importlib.reload(tb)
    tb.root.geometry("+0+0")
    return tb


def basic_empty_board() -> None:
    m = new_basic_app()
    capture("basic-empty-board", m.root)


def basic_first_move() -> None:
    m = new_basic_app()
    m.na_knopku_nazhali(0)  # X ставит первую отметку в клетку 0
    capture("basic-first-move", m.root)


def basic_win() -> None:
    m = new_basic_app()
    for i in (0, 3, 1, 4, 2):  # X собирает верхнюю строку
        m.na_knopku_nazhali(i)
    capture("basic-win", m.root)


def basic_draw() -> None:
    m = new_basic_app()
    # X O X / X O O / O X X — поле заполнено, победителя нет
    for i in (0, 1, 2, 4, 3, 5, 7, 6, 8):
        m.na_knopku_nazhali(i)
    capture("basic-draw", m.root)


def basic_new_game_reset() -> None:
    m = new_basic_app()
    for i in (0, 3, 1, 4, 2):  # сначала X выигрывает партию
        m.na_knopku_nazhali(i)
    m.novaya_igra()  # кнопка "Новая игра" — поле и статус сброшены
    capture("basic-new-game-reset", m.root)


def adaptive_board_small() -> None:
    """Same representative game state as mid_game(), captured at a normal
    window size — paired with adaptive_board_large() to visually prove
    the board grows with the window, not just describe it in prose."""
    root, app = new_app()
    for i in (0, 4, 1, 3, 8):
        app.attempt_move(i)
    root.geometry("340x420+0+0")
    root.update_idletasks()
    root.update()
    app.render()  # re-asserts fg/bg after the geometry change settles
    capture("adaptive-board-small", root, grab_w=420, grab_h=480)


def adaptive_board_large() -> None:
    """Identical game state to adaptive_board_small(), same app, only the
    window geometry differs — the board frame's own real Tk layout does
    the resizing, nothing is scaled or faked."""
    root, app = new_app()
    for i in (0, 4, 1, 3, 8):
        app.attempt_move(i)
    root.geometry("700x820+0+0")
    root.update_idletasks()
    root.update()
    app.render()  # re-asserts fg/bg after the geometry change settles
    capture("adaptive-board-large", root, grab_w=760, grab_h=880)


def adaptive_board_comparison() -> None:
    """Composes the two REAL captures onto one canvas at their TRUE
    relative pixel scale — neither image is resized, so the size
    difference is visible without reading the caption. Requires
    adaptive_board_small()/adaptive_board_large() to have already run."""
    small = Image.open(OUT_DIR / "adaptive-board-small.png").convert("RGB")
    large = Image.open(OUT_DIR / "adaptive-board-large.png").convert("RGB")

    label_h = 56
    gap = 40
    pad = 24
    max_img_h = max(small.height, large.height)
    canvas_w = pad * 2 + small.width + gap + large.width
    canvas_h = pad * 2 + label_h + max_img_h

    canvas = Image.new("RGB", (canvas_w, canvas_h), "#FAFAFC")
    draw = ImageDraw.Draw(canvas)
    font_title = ImageFont.truetype(str(_FONT_DIR / "DejaVuSans-Bold.ttf"), 20)
    font_dims = ImageFont.truetype(str(_FONT_DIR / "DejaVuSans.ttf"), 15)

    def draw_label(center_x: int, title: str, dims: str) -> None:
        title_w = draw.textlength(title, font=font_title)
        draw.text((center_x - title_w / 2, pad), title, font=font_title, fill="#0D0230")
        dims_w = draw.textlength(dims, font=font_dims)
        draw.text((center_x - dims_w / 2, pad + 27), dims, font=font_dims, fill="#6B6B7D")

    x_small, x_large = pad, pad + small.width + gap
    img_top = pad + label_h

    draw_label(x_small + small.width // 2, "Обычный размер", f"{small.width} × {small.height} px")
    draw_label(x_large + large.width // 2, "После увеличения окна", f"{large.width} × {large.height} px")

    # Bottom-aligned, as if both windows sat on the same table — makes the
    # height difference read as naturally as the width difference.
    canvas.paste(small, (x_small, img_top + (max_img_h - small.height)))
    canvas.paste(large, (x_large, img_top + (max_img_h - large.height)))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "adaptive-board-comparison.png"
    canvas.save(out_path)
    print(f"Сохранено: {out_path.relative_to(ROOT)} ({canvas.size[0]}x{canvas.size[1]})")


def win_pulse_step_0() -> None:
    """Captured immediately after the winning move, before the after()
    -scheduled next tick has had a chance to run — real tick=0 colors
    (PULSE_BG accent), not a synthetic freeze."""
    root, app = new_app()
    for i in (0, 3, 1, 4, 2):  # X wins the top row
        app.attempt_move(i)
    capture("win-pulse-step-0", root)


def win_pulse_step_1() -> None:
    """Capture the single settled tick after the calm 400ms accent."""
    root, app = new_app()
    for i in (0, 3, 1, 4, 2):
        app.attempt_move(i)
    app.cancel_pulse()
    app.pulse_winning_line(tick=1)
    capture("win-pulse-step-1", root)


def win_pulse_final() -> None:
    """The settled state once the pulse finishes — same call pattern as
    x_win()/winning_highlight(): cancel the pending job, then render()
    from the model, which is exactly what the natural end of the pulse
    loop leaves on screen."""
    root, app = new_app()
    for i in (0, 3, 1, 4, 2):
        app.attempt_move(i)
    app.cancel_pulse()
    app.render()
    capture("win-pulse-final", root)


def tic_tac_toe_pro() -> None:
    root, app = new_app()
    for i in (0, 4, 1, 3, 8):  # a representative mid-game with score already on the board
        app.attempt_move(i)
    app.state.score_x, app.state.score_o, app.state.draws = 1, 2, 1
    app.render()
    capture("tic-tac-toe-pro", root)


if __name__ == "__main__":
    basic_empty_board()
    basic_first_move()
    basic_win()
    basic_draw()
    basic_new_game_reset()
    empty_board()
    x_first_move()
    x_turn()
    o_turn()
    mid_game()
    x_win()
    o_win()
    winning_highlight()
    draw()
    hover_preview_x()
    hover_preview_o()
    scoreboard()
    new_round_reset()
    new_match_reset()
    adaptive_board_small()
    adaptive_board_large()
    adaptive_board_comparison()
    win_pulse_step_0()
    win_pulse_step_1()
    win_pulse_final()
    tic_tac_toe_pro()
