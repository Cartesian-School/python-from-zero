"""Игра «Крестики-нолики» на Tkinter — финальная версия (глава 17).

Перестройка прототипа из tic_tac_toe_basic.py: игровое состояние (GameState)
отделено от виджетов, правила — чистые функции, тестируемые без окна.
Мышь и клавиатура ведут к одному и тому же attempt_move(). Есть наведение-
превью, подсветка победной линии, счёт матчей и мягкая анимация победы через
after() (без time.sleep()).

Запуск: python tic_tac_toe.py
"""

import json
import tkinter as tk
from dataclasses import dataclass, field
from pathlib import Path
from tkinter import ttk

WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # строки
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # столбцы
    (0, 4, 8), (2, 4, 6),             # диагонали
)

SCORES_PATH = Path("tic_tac_toe_scores.json")  # относительно текущей рабочей директории

MARK_COLOR = {"X": "#5B24F9", "O": "#DB2777"}
HOVER_COLOR = "#B9A0FC"
WIN_BG = "#D1FAE5"
PULSE_BG = "#6EE7B7"
NEUTRAL_BG = "#FAFAFC"  # намеренный светлый нейтральный фон — не системная константа, чтобы вид не зависел от ОС


def find_winner(board):
    """Возвращает (winner, winning_line): ('X'|'O', (a, b, c)) либо (None, None)."""
    for a, b, c in WINNING_LINES:
        mark = board[a]
        if mark and mark == board[b] == board[c]:
            return mark, (a, b, c)
    return None, None


def is_draw(board):
    """Ничья — это заполненное поле БЕЗ победителя. Порядок проверки важен:
    девятый ход может одновременно заполнить поле и выиграть партию — тогда
    это победа, а не ничья (см. раздел 17.17)."""
    winner, _ = find_winner(board)
    return winner is None and all(board)


@dataclass
class GameState:
    """Только данные партии — ни одной кнопки Tkinter внутри (раздел 17.19)."""

    board: list[str] = field(default_factory=lambda: [""] * 9)
    current_player: str = "X"
    game_over: bool = False
    winner: str | None = None
    winning_line: tuple[int, int, int] | None = None
    score_x: int = 0
    score_o: int = 0
    draws: int = 0


def load_scores():
    if not SCORES_PATH.exists():
        return {"x": 0, "o": 0, "draws": 0}
    with SCORES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_scores(state):
    with SCORES_PATH.open("w", encoding="utf-8") as f:
        json.dump({"x": state.score_x, "o": state.score_o, "draws": state.draws}, f, ensure_ascii=False, indent=2)


class TicTacToeApp:
    def __init__(self, root, *, persist_scores=False):
        self.root = root
        self.root.title("Крестики-нолики")
        self.persist_scores = persist_scores
        self.state = GameState()
        if persist_scores:
            saved = load_scores()
            self.state.score_x = saved.get("x", 0)
            self.state.score_o = saved.get("o", 0)
            self.state.draws = saved.get("draws", 0)
        self.buttons: list[tk.Button] = []
        self.status_var = tk.StringVar()
        self.score_var = tk.StringVar()
        self._pulse_job = None
        self.build_ui()
        self.render()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- UI construction ----------
    def build_ui(self):
        outer = ttk.Frame(self.root, padding=14)
        outer.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(outer, textvariable=self.status_var, font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(0, 8)
        )

        self.build_board(outer)

        ttk.Label(outer, textvariable=self.score_var, font=("Arial", 11)).grid(
            row=2, column=0, columnspan=3, pady=(10, 4)
        )

        controls = ttk.Frame(outer)
        controls.grid(row=3, column=0, columnspan=3, pady=(4, 0))
        ttk.Button(controls, text="Новый раунд (R)", command=self.new_round).pack(side="left", padx=4)
        ttk.Button(controls, text="Новый матч", command=self.new_match).pack(side="left", padx=4)

        for i in range(3):
            outer.columnconfigure(i, weight=1)

        # Клавиатура и мышь ведут к одной и той же игровой логике (раздел 17.24).
        self.root.bind("<Key>", self.on_key)

    def build_board(self, outer):
        board_frame = ttk.Frame(outer)
        board_frame.grid(row=1, column=0, columnspan=3)
        for i in range(3):
            board_frame.rowconfigure(i, weight=1)
            board_frame.columnconfigure(i, weight=1)
        for index in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=3,
                height=1,
                relief="raised",
                command=lambda i=index: self.attempt_move(i),
            )
            btn.grid(row=index // 3, column=index % 3, sticky="nsew", padx=3, pady=3)
            btn.bind("<Enter>", lambda _event, i=index: self.on_cell_enter(i))
            btn.bind("<Leave>", lambda _event, i=index: self.on_cell_leave(i))
            self.buttons.append(btn)

    # ---------- callbacks: mutate model, then render ----------
    def attempt_move(self, index):
        state = self.state
        if state.game_over or state.board[index]:
            return  # игра окончена или клетка занята — ход не засчитывается, ход не переключается

        state.board[index] = state.current_player

        winner, line = find_winner(state.board)
        if winner:
            state.winner = winner
            state.winning_line = line
            state.game_over = True
            if winner == "X":
                state.score_x += 1
            else:
                state.score_o += 1
            self.render()
            self.pulse_winning_line()
            self._maybe_save_scores()
            return

        if is_draw(state.board):
            state.game_over = True
            state.draws += 1
            self.render()
            self._maybe_save_scores()
            return

        state.current_player = "O" if state.current_player == "X" else "X"
        self.render()

    def on_cell_enter(self, index):
        state = self.state
        if state.game_over or state.board[index]:
            return  # превью не показываем поверх занятой клетки или после конца игры
        self.buttons[index].config(text=state.current_player, fg=HOVER_COLOR)

    def on_cell_leave(self, index):
        # Превью — не ход: модель не менялась, поэтому просто перерисовываем
        # из состояния — реальная (или пустая) клетка возвращается сама.
        self.render()

    def on_key(self, event):
        if event.keysym in ("r", "R"):
            self.new_round()
            return
        if event.char and event.char.isdigit():
            n = int(event.char)
            if 1 <= n <= 9:
                self.attempt_move(n - 1)  # клавиши 1-9 вызывают ТОТ ЖЕ attempt_move(), что и клик

    # ---------- render(): единственное место, что красит виджеты ----------
    def render(self):
        state = self.state
        for index, btn in enumerate(self.buttons):
            mark = state.board[index]
            is_win_cell = state.winning_line is not None and index in state.winning_line
            btn.config(
                text=mark,
                fg=MARK_COLOR.get(mark, "#0D0230"),
                bg=WIN_BG if is_win_cell else NEUTRAL_BG,
                # Отключаем кнопку только когда партия ОКОНЧЕНА (item 67) — занятая,
                # но ещё активная клетка обязана сохранять цвет своей отметки (item 64):
                # attempt_move() и так безопасно игнорирует клик по уже занятой клетке.
                state="disabled" if state.game_over else "normal",
            )
        if state.game_over:
            self.status_var.set(f"Победил игрок {state.winner}!" if state.winner else "Ничья!")
        else:
            self.status_var.set(f"Ход игрока: {state.current_player}")
        self.score_var.set(f"X: {state.score_x}  |  O: {state.score_o}  |  Ничьи: {state.draws}")

    # ---------- round / match lifecycle ----------
    def new_round(self):
        """Новый раунд: очищает партию, СОХРАНЯЕТ счёт матча (раздел 17.27)."""
        self.cancel_pulse()
        state = self.state
        state.board = [""] * 9
        state.current_player = "X"
        state.game_over = False
        state.winner = None
        state.winning_line = None
        self.render()

    def new_match(self):
        """Новый матч: обнуляет счёт и начинает новый раунд."""
        self.state.score_x = 0
        self.state.score_o = 0
        self.state.draws = 0
        self._maybe_save_scores()
        self.new_round()

    def _maybe_save_scores(self):
        if self.persist_scores:
            save_scores(self.state)

    # ---------- ненавязчивая анимация победы через after(), без time.sleep() ----------
    def pulse_winning_line(self, tick=0):
        if not self.state.winning_line:
            return
        color = PULSE_BG if tick % 2 == 0 else WIN_BG
        for index in self.state.winning_line:
            self.buttons[index].config(bg=color)
        if tick < 5:
            self._pulse_job = self.root.after(150, self.pulse_winning_line, tick + 1)
        else:
            self._pulse_job = None

    def cancel_pulse(self):
        if self._pulse_job is not None:
            self.root.after_cancel(self._pulse_job)
            self._pulse_job = None

    def on_close(self):
        self.cancel_pulse()
        self._maybe_save_scores()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
