#!/usr/bin/env python3
"""Генерирует настоящие скриншоты Tkinter-игры «Крестики-нолики» для главы 17.

Каждый скриншот получен, запустив реальный projects/tkinter/tic-tac-toe/tic_tac_toe.py
(класс TicTacToeApp) и подведя его к нужному состоянию через его собственные
методы (attempt_move/on_cell_enter/new_round/...) — не имитация HTML/CSS.

Требует headless X-сервер (xvfb-run).
Использование: xvfb-run -a python3 scripts/generate_chapter_17_outputs.py
"""

import sys
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageChops, ImageGrab

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-17" / "output"
sys.path.insert(0, str(ROOT / "projects" / "tkinter" / "tic-tac-toe"))

import tic_tac_toe as t  # noqa: E402


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


def tic_tac_toe_pro() -> None:
    root, app = new_app()
    for i in (0, 4, 1, 3, 8):  # a representative mid-game with score already on the board
        app.attempt_move(i)
    app.state.score_x, app.state.score_o, app.state.draws = 1, 2, 1
    app.render()
    capture("tic-tac-toe-pro", root)


if __name__ == "__main__":
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
    tic_tac_toe_pro()
