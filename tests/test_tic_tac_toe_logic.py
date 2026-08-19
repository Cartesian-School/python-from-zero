"""Регрессионный набор для чистой игровой логики главы 17 (find_winner/is_draw) —
без Tkinter и без Xvfb, потому что правила не зависят от окна (раздел 17.28).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "projects" / "tkinter" / "tic-tac-toe"))

from tic_tac_toe import WINNING_LINES, find_winner, is_draw  # noqa: E402

EMPTY = [""] * 9


def board_for_line(line, mark):
    board = [""] * 9
    for i in line:
        board[i] = mark
    return board


def test_all_eight_lines_both_players():
    assert len(WINNING_LINES) == 8
    for mark in ("X", "O"):
        for line in WINNING_LINES:
            board = board_for_line(line, mark)
            winner, winning_line = find_winner(board)
            assert winner == mark, (mark, line, board)
            assert set(winning_line) == set(line)


def test_no_winner_on_empty_or_partial_board():
    assert find_winner(EMPTY) == (None, None)
    partial = ["X", "O", "", "", "X", "", "", "", ""]
    assert find_winner(partial) == (None, None)


def test_draw_detection():
    draw_board = ["X", "O", "X",
                  "X", "O", "O",
                  "O", "X", "X"]
    assert find_winner(draw_board) == (None, None)
    assert is_draw(draw_board) is True


def test_last_move_creates_win_not_draw():
    # Board is completely full AND the last mark completes a diagonal.
    board = ["X", "O", "O",
             "O", "X", "X",
             "O", "X", "X"]
    winner, line = find_winner(board)
    assert winner == "X"
    assert set(line) == {0, 4, 8}
    assert is_draw(board) is False, "a winning final move must never be reported as a draw"


def test_is_draw_false_while_board_has_empty_cells():
    assert is_draw(["X", "O", "", "", "", "", "", "", ""]) is False


def test_winning_lines_cover_rows_cols_diagonals_exactly_once():
    rows = {(0, 1, 2), (3, 4, 5), (6, 7, 8)}
    cols = {(0, 3, 6), (1, 4, 7), (2, 5, 8)}
    diagonals = {(0, 4, 8), (2, 4, 6)}
    assert set(WINNING_LINES) == rows | cols | diagonals
