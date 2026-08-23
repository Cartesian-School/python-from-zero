"""Pytest-обёртка над проверками всех мини-проектов книги «Python с нуля».

Каждый проект с GUI (Tkinter/Pygame/Turtle) создаёт собственное окно/экран при
импорте — чтобы не сталкивать несколько таких модулей в одном процессе, каждая
проверка запускается отдельным подпроцессом под Xvfb (там, где нужен дисплей).

Запуск: pytest tests/ -v   (для GUI-тестов нужен доступный дисплей — реальный или Xvfb)
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_with_display(code: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["xvfb-run", "-a", sys.executable, "-c", code],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=60,
    )


def run_plain(code: str, cwd: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    import os

    full_env = {**os.environ, **env} if env else None
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=30,
        env=full_env,
    )


def test_calculator():
    r = run_with_display(
        """
import calculator as c
assert c.vychislit_vyrazhenie("2+2") == "4"
assert c.vychislit_vyrazhenie("10-3*2") == "4"
assert c.vychislit_vyrazhenie("(1+2)*3") == "9"
assert c.vychislit_vyrazhenie("5/0") == "Ошибка"
assert c.vychislit_vyrazhenie("import os") == "Ошибка"
c.na_ochistit_nazhali()
for s in "12+8":
    c.na_cifru_ili_znak_nazhali(s)
c.na_ravno_nazhali()
assert c.ekran_text.get() == "20"
print("OK")
""",
        ROOT / "projects" / "tkinter" / "calculator",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_temperature_converter():
    r = run_with_display(
        """
import temperature_converter as tc
r0 = tc.preobrazovat(0, "C")
assert abs(r0["F"] - 32) < 1e-9
assert abs(r0["K"] - 273.15) < 1e-9
r100 = tc.preobrazovat(100, "C")
assert abs(r100["F"] - 212) < 1e-9
tc.pole_vvoda.insert(0, "не число")
tc.na_preobrazovat_nazhali()
assert tc.rezultat_text.get() == "Введите число"
print("OK")
""",
        ROOT / "projects" / "tkinter" / "temperature-converter",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_notes_app():
    r = run_with_display(
        """
import notes_app as na
if na.FAJL_ZAMETOK.exists():
    na.FAJL_ZAMETOK.unlink()
na.polye_teksta.insert("1.0", "test note")
na.sohranit_zametku()
assert na.FAJL_ZAMETOK.read_text(encoding="utf-8") == "test note"
na.ochistit_polye()
na.zagruzit_zametku()
assert na.polye_teksta.get("1.0", "end-1c") == "test note"
na.FAJL_ZAMETOK.unlink()
print("OK")
""",
        ROOT / "projects" / "tkinter" / "notes-app",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_tic_tac_toe_basic():
    r = run_with_display(
        """
import tic_tac_toe_basic as t
t.novaya_igra()
for i in (0, 3, 1, 4, 2):  # X wins the top row
    t.na_knopku_nazhali(i)
assert t.proverit_pobedu() == "X"
assert t.igra_okonchena is True
print("OK")
""",
        ROOT / "projects" / "tkinter" / "tic-tac-toe",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_tic_tac_toe_pro():
    r = run_with_display(
        """
import tkinter as tk
import tic_tac_toe as t

root = tk.Tk()
app = t.TicTacToeApp(root)
root.update()

# adaptive chain: the real center cell grows with the window in both axes
root.geometry("340x420")
root.update_idletasks()
root.update()
small_size = (app.buttons[4].winfo_width(), app.buttons[4].winfo_height())
root.geometry("700x820")
root.update_idletasks()
root.update()
large_size = (app.buttons[4].winfo_width(), app.buttons[4].winfo_height())
assert large_size[0] > small_size[0]
assert large_size[1] > small_size[1]

# occupied cell: rejected, does not switch player
app.attempt_move(0)
app.attempt_move(0)
assert app.state.board[0] == "X"
assert app.state.current_player == "O"

# hover preview never mutates the model, and is cleared on leave
app.on_cell_enter(4)
root.update()
assert app.state.board[4] == ""
assert app.buttons[4]["text"] == "O"
app.on_cell_leave(4)
root.update()
assert app.buttons[4]["text"] == ""

# full game: win detection, winning-line highlight, score, board lock
app.new_round()
for i in (0, 3, 1, 4, 2):  # X takes the top row
    app.attempt_move(i)
assert app.state.game_over is True
assert app.state.winner == "X"
assert app.state.winning_line == (0, 1, 2)
assert app.state.score_x == 1
app.attempt_move(5)  # move after game_over must be rejected
assert app.state.board[5] == ""

# calm win effect: one accent frame, then one settled frame
app.cancel_pulse()
app.pulse_winning_line(0)
assert app.buttons[0]["bg"] == t.PULSE_BG
app.cancel_pulse()
app.pulse_winning_line(1)
assert app.buttons[0]["bg"] == t.WIN_BG
assert app._pulse_job is None

# keyboard path reuses attempt_move (same pipeline as mouse)
app.new_round()
class FakeEvent:
    def __init__(self, char, keysym):
        self.char, self.keysym = char, keysym
app.on_key(FakeEvent("1", "1"))
assert app.state.board[0] == "X"

# New Round keeps match score, New Match resets it
app.new_round()
assert app.state.score_x == 1
app.new_match()
assert app.state.score_x == 0 and app.state.score_o == 0 and app.state.draws == 0
root.destroy()
print("OK")
""",
        ROOT / "projects" / "tkinter" / "tic-tac-toe",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_paint_app_basic():
    r = run_with_display(
        """
import paint_app_basic as p

class FakeEvent:
    def __init__(self, x, y):
        self.x, self.y = x, y

p.vybrat_figuru("linia")
p.vybrat_cvet("red")
p.nachalo_risovaniya(FakeEvent(10, 10))
p.vo_vremya_risovaniya(FakeEvent(50, 50))
p.konec_risovaniya(FakeEvent(50, 50))
assert len(p.canvas.find_all()) == 1
p.ochistit_holst()
assert len(p.canvas.find_all()) == 0
print("OK")
""",
        ROOT / "projects" / "tkinter" / "paint-app",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_paint_app_pro():
    r = run_with_display(
        """
import tkinter as tk
import paint_app as p

root = tk.Tk()
app = p.PaintApp(root)
root.update()

class FakeEvent:
    def __init__(self, x, y):
        self.x, self.y = x, y

# rectangle: press -> drag -> release commits exactly one Shape
app.set_tool(p.Tool.RECTANGLE)
app.on_press(FakeEvent(10, 10))
app.on_drag(FakeEvent(100, 80))
app.on_release(FakeEvent(100, 80))
assert len(app.document) == 1
assert app.document[0].kind == "rectangle"

# pencil stroke: several drag segments are ONE undo-able action
app.set_tool(p.Tool.PENCIL)
app.on_press(FakeEvent(200, 200))
app.on_drag(FakeEvent(210, 205))
app.on_drag(FakeEvent(220, 210))
app.on_release(FakeEvent(220, 210))
assert len(app.document) == 3  # 1 rectangle + 2 line segments

app.undo()
assert len(app.document) == 1  # whole stroke removed, not just one segment
app.redo()
assert len(app.document) == 3

# a fresh action clears the redo stack (Debug Lab: stale redo)
app.undo()
app.set_tool(p.Tool.OVAL)
app.on_press(FakeEvent(5, 5))
app.on_drag(FakeEvent(40, 40))
app.on_release(FakeEvent(40, 40))
assert app.redo_stack == []

# clicking without dragging past MIN_DRAG does not commit a degenerate shape
before = len(app.document)
app.set_tool(p.Tool.LINE)
app.on_press(FakeEvent(300, 300))
app.on_release(FakeEvent(300, 300))
assert len(app.document) == before

root.destroy()
print("OK")
""",
        ROOT / "projects" / "tkinter" / "paint-app",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_snake_basic():
    r = run_with_display(
        """
import snake_basic as s
s.napravlenie = "right"
x0 = s.golova.xcor()
s.igrovoj_shag()
assert s.golova.xcor() == x0 + s.RAZMER_SHAGA
print("OK")
""",
        ROOT / "projects" / "turtle" / "snake",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_snake_pro():
    r = run_with_display(
        """
import random
import snake as s

app = s.SnakeApp(rng=random.Random(11))
assert app.state.status is s.GameStatus.READY

# READY -> RUNNING happens on the first requested direction
app.request_direction(s.Direction.RIGHT)
assert app.state.status is s.GameStatus.RUNNING

# rapid Up-then-Left before the tick consumes Up must not sneak a reversal
app.request_direction(s.Direction.UP)
app.request_direction(s.Direction.LEFT)
assert app.state.next_direction is s.Direction.UP

# a normal tick moves the head and keeps the snake's length
before = app.state.snake[0]
app.game_tick()
assert app.state.snake[0] == s.next_head(before, s.Direction.UP)
assert len(app.state.snake) == 1

# eating food grows the snake by exactly one segment and scores
app.state.food = s.next_head(app.state.snake[0], s.Direction.UP)
app.game_tick()
assert app.state.score == 10
assert len(app.state.snake) == 2
assert app.state.high_score == 10

# pause freezes the model: a tick during PAUSED must not move anything
app.toggle_pause()
assert app.state.status is s.GameStatus.PAUSED
frozen_snake = list(app.state.snake)
app.game_tick()
assert app.state.snake == frozen_snake
app.toggle_pause()
assert app.state.status is s.GameStatus.RUNNING

# --- required audit hotfix: pause/resume must never create two ontimer
# chains (a real bug found after PR #35 — resume before the pre-pause
# callback fires used to leave BOTH chains alive). game_tick() alone can't
# reproduce this: it must go through _schedule_next_tick()/_on_timer() with
# real generation tokens, simulating "the timer fires later" by calling
# _on_timer() directly instead of sleeping on a real Tk mainloop.
app.state.snake = [(0, 0)]
app.state.direction = s.Direction.RIGHT
app.state.next_direction = s.Direction.RIGHT
app.state.status = s.GameStatus.RUNNING
app._schedule_next_tick()
gen_a = app._generation  # timer A's captured generation

app.toggle_pause()  # RUNNING -> PAUSED must invalidate timer A immediately
assert app.state.status is s.GameStatus.PAUSED
assert app._generation != gen_a

app.toggle_pause()  # PAUSED -> RUNNING must start exactly ONE fresh chain
assert app.state.status is s.GameStatus.RUNNING
gen_b = app._generation
assert gen_b != gen_a

# stale timer A fires late (resume already happened before it did): must
# be a pure no-op — no move, no state change, no new callback scheduled.
snake_before_stale = list(app.state.snake)
app._on_timer(gen_a)
assert app.state.snake == snake_before_stale
assert app.state.status is s.GameStatus.RUNNING

# timer B (the real, current chain) fires: exactly one tick happens.
before_b = app.state.snake[0]
app._on_timer(gen_b)
assert app.state.snake[0] == s.next_head(before_b, s.Direction.RIGHT)

# rapid pause/resume/pause/resume must still land on exactly one live chain
app.state.status = s.GameStatus.RUNNING
app._schedule_next_tick()
gen_r1 = app._generation
app.toggle_pause()
app.toggle_pause()
app.toggle_pause()
app.toggle_pause()
assert app.state.status is s.GameStatus.RUNNING
gen_r2 = app._generation
assert gen_r2 != gen_r1
snake_before_rapid = list(app.state.snake)
app._on_timer(gen_r1)  # every earlier generation must be dead
assert app.state.snake == snake_before_rapid
before_r2 = app.state.snake[0]
app._on_timer(gen_r2)  # the survivor still works
assert app.state.snake[0] == s.next_head(before_r2, s.Direction.RIGHT)

# restart after pause invalidates the paused chain's generation too
app.state.status = s.GameStatus.RUNNING
app._schedule_next_tick()
gen_running = app._generation
app.toggle_pause()
gen_paused = app._generation
app.restart()
gen_after_restart_from_pause = app._generation
assert len({gen_running, gen_paused, gen_after_restart_from_pause}) == 3
app._on_timer(gen_running)
assert app.state.snake == [(0, 0)]
app._on_timer(gen_paused)
assert app.state.snake == [(0, 0)]

# restart after resume invalidates the resumed chain's generation
app.request_direction(s.Direction.RIGHT)  # READY -> RUNNING, schedules a tick
gen_resumed_running = app._generation
app.restart()
assert app._generation != gen_resumed_running
app._on_timer(gen_resumed_running)
assert app.state.snake == [(0, 0)]

# repeated restart cannot multiply chains: every restart's generation is unique
gens = set()
for _ in range(5):
    app.restart()
    gens.add(app._generation)
assert len(gens) == 5

# direct proof: a stale _on_timer() must not call screen.ontimer() at all —
# i.e. it cannot schedule a follow-up callback, not just "appear to do nothing"
scheduled = []
app.screen.ontimer = lambda *a, **k: scheduled.append((a, k))
app.state.status = s.GameStatus.RUNNING
app._schedule_next_tick()
live_gen = app._generation
scheduled.clear()
app._on_timer(live_gen - 1)  # deliberately stale
assert scheduled == []

# --- required micro-hotfix: game_tick() -> render() -> screen.update() can
# process pending Tk events, so a Pause/Resume (or Restart) may happen
# REENTRANTLY while _on_timer() is still inside game_tick() and change the
# generation before _on_timer() gets back control. A callback that went
# stale during its own tick must not ALSO schedule a continuation on top
# of whatever fresh chain that reentrant event already started.
scheduled.clear()
app.state.status = s.GameStatus.RUNNING
reentrant_start_gen = app._generation
real_game_tick = app.game_tick


def fake_reentrant_tick():
    # Simulate Pause -> Resume happening reentrantly inside
    # game_tick() -> render() -> screen.update().
    app._generation += 2
    app.state.status = s.GameStatus.RUNNING
    app._schedule_next_tick()  # Resume starts exactly one fresh chain


app.game_tick = fake_reentrant_tick
app._on_timer(reentrant_start_gen)
assert len(scheduled) == 1  # only Resume's own timer — the stale callback must not add a second
app.game_tick = real_game_tick

# same shape, but generation does NOT change during the tick — the fix must
# not accidentally suppress the ordinary, unchanged-generation continuation
scheduled.clear()
app.state.status = s.GameStatus.RUNNING
unchanged_gen = app._generation


def fake_normal_tick():
    pass


app.game_tick = fake_normal_tick
app._on_timer(unchanged_gen)
assert len(scheduled) == 1
app.game_tick = real_game_tick

print("REENTRANT GENERATION GUARD OK")
print("PAUSE/RESUME TIMER CHAIN OK")

# --- required audit hotfix: full board must return an explicit terminal
# state, never food silently placed inside the snake. Build a snake that
# occupies every legal cell except one, with food on that last free cell
# and the head one step away from it — the next tick eats it, fills the
# board completely, and choose_food() must report None.
app2 = s.SnakeApp(rng=random.Random(3))
all_cells_list = list(s.all_cells())
last_free = all_cells_list[-1]
head_cell = s.next_head(last_free, s.OPPOSITE[s.Direction.RIGHT])
body_cells = [c for c in all_cells_list if c not in (last_free, head_cell)]
app2.state.snake = [head_cell, *body_cells]
app2.state.direction = s.Direction.RIGHT
app2.state.next_direction = s.Direction.RIGHT
app2.state.status = s.GameStatus.RUNNING
app2.state.food = last_free
app2.game_tick()
assert app2.state.status is s.GameStatus.WON
assert app2.state.food is None
assert len(app2.state.snake) == len(all_cells_list)
app2.render()  # must not crash trying to Turtle.goto(None)
print("FULL BOARD / WON OK")

# --- required audit hotfix: HUD must sit outside the legal playfield —
# check the actual on-screen scoreboard position after a real render(),
# not just the HUD_Y constant in isolation.
assert s.HUD_Y > s.FIELD_HALF
app3 = s.SnakeApp(rng=random.Random(4))
app3.render()
scoreboard_y = app3.scoreboard.ycor()
assert scoreboard_y == s.HUD_Y
legal_ys = {y for _, y in s.all_cells()}
assert round(scoreboard_y) not in legal_ys
print("HUD OK")

print("OK")
""",
        ROOT / "projects" / "turtle" / "snake",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_bouncing_ball_basic():
    r = run_with_display(
        """
import bouncing_ball_basic as b
x, y, dx, dy = b.shag_fiziki(b.RADIUS - 1, 200, -5, 3)
assert dx == 5
print("OK")
""",
        ROOT / "projects" / "pygame" / "bouncing-ball",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_bouncing_ball_pro():
    r = run_with_display(
        """
import math
import bouncing_ball as b

game = b.BouncingBallGame()
assert game.state is b.SostoyanieIgry.IGRA

# Много тиков физики -- мяч обязан хотя бы раз отскочить от стены поля
# 600x400, и счёт должен расти ровно на OCHKOV_ZA_OTSKOK за каждый отскок
# (раздел 20.33 -- отдельная проверка соответствия схема schet <-> otskokov).
for _ in range(240):
    game.update(1 / 60)
assert game.otskokov > 0
assert game.schet == game.otskokov * b.OCHKOV_ZA_OTSKOK
assert b.RADIUS <= game.x <= b.SHIRINA - b.RADIUS
assert b.RADIUS <= game.y <= b.VYSOTA - b.RADIUS

# Пауза обязана останавливать именно update(), а не только отрисовку --
# раздел 20.26, тот самый Debug Lab про "пауза не останавливает управление".
game.toggle_pause()
assert game.state is b.SostoyanieIgry.PAUZA
frozen = (game.x, game.y, game.vx, game.vy)
for _ in range(60):
    game.update(1 / 60)
assert (game.x, game.y, game.vx, game.vy) == frozen
game.toggle_pause()
assert game.state is b.SostoyanieIgry.IGRA

# Рестарт без перезапуска процесса -- отскоки и счёт обнуляются.
game._reset_myach()
assert game.otskokov == 0 and game.schet == 0
assert (game.x, game.y) == (b.SHIRINA / 2, b.VYSOTA / 2)

# Клик мышью разворачивает мяч к точке клика, сохраняя величину скорости
# (нормализация вектора -- раздел 20.16 про диагональное движение).
skorost_do = math.hypot(game.vx, game.vy)
game.tolknut_k_tochke(game.x + 100, game.y)
assert game.vx > 0
assert math.isclose(math.hypot(game.vx, game.vy), skorost_do, rel_tol=1e-9)

# render() не должен падать -- в том числе состояние ПАУЗА с оверлеем текста.
game.render()
game.toggle_pause()
game.render()

print("OK")
""",
        ROOT / "projects" / "pygame" / "bouncing-ball",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_bouncing_balls_oop():
    r = run_with_display(
        """
import bouncing_balls as bb
myachi = bb.sozdat_myachi(3)
assert len(myachi) == 3
for kadr in range(300):
    for m in myachi:
        m.shag()
for m in myachi:
    assert m.radius <= m.x <= bb.SHIRINA - m.radius
    assert m.otskokov > 0
print("OK")
""",
        ROOT / "projects" / "pygame" / "bouncing-balls-oop",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_space_shooter():
    r = run_with_display(
        """
import space_shooter as sh

game = sh.Game()
game.start_new_game()

game._spawn_bullet()
assert len(game.bullets) == 1

vrag = sh.Enemy(
    game.assets.images["enemy_scout"],
    game.player.rect.midtop,
    points=100,
    speed=0.0,
)
game.enemies.add(vrag)

for _ in range(30):
    game.update(1 / 60)
    if game.score:
        break

assert game.score == 100
assert len(game.enemies) == 0
game.render()
print("OK")
""",
        ROOT / "projects" / "pygame" / "space-shooter",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_story_generator():
    r = run_plain(
        """
import random
import story_generator as sg
random.seed(1)
istoriya = sg.sluchajnaya_istoriya()
assert istoriya.startswith("Однажды") and istoriya.endswith("прежней.")
print("OK")
""",
        ROOT / "projects" / "console" / "story-generator",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_rock_paper_scissors():
    r = run_plain(
        """
import rps
assert rps.opredelit_pobeditelya("камень", "ножницы") == "игрок"
assert rps.opredelit_pobeditelya("ножницы", "камень") == "компьютер"
assert rps.opredelit_pobeditelya("бумага", "бумага") == "ничья"
print("OK")
""",
        ROOT / "projects" / "console" / "rock-paper-scissors",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_flask_todo_app():
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        r = run_plain(
            """
import app as app_module
with app_module.app.app_context():
    app_module.init_db()
client = app_module.app.test_client()
resp = client.get("/")
assert resp.status_code == 200
assert "Задач пока нет" in resp.get_data(as_text=True)
resp2 = client.post("/dobavit", data={"zadacha": "Новая задача"})
assert resp2.status_code == 303
resp3 = client.get("/")
assert "Новая задача" in resp3.get_data(as_text=True)
print("OK")
""",
            ROOT / "projects" / "flask" / "todo-app",
            env={"TODO_APP_DB": str(Path(tmpdir) / "zadachi_test.db")},
        )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout
