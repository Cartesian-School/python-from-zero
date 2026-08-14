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


def run_plain(code: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=30,
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


def test_tic_tac_toe():
    r = run_with_display(
        """
import tic_tac_toe as t
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


def test_paint_app():
    r = run_with_display(
        """
import paint_app as p

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


def test_snake():
    r = run_with_display(
        """
import snake as s
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


def test_bouncing_ball():
    r = run_with_display(
        """
import bouncing_ball as b
x, y, dx, dy = b.shag_fiziki(b.RADIUS - 1, 200, -5, 3)
assert dx == 5
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
state = sh.novaya_igra()
sh.vystrelit(state)
assert len(state["puli"]) == 1
vrag = sh.pygame.Rect(state["korabl"].centerx - 20, state["korabl"].top - 30, sh.VRAG_SHIRINA, sh.VRAG_VYSOTA)
state["vragi"] = [vrag]
for _ in range(10):
    sh.obnovit_igru(state)
    if state["schet"]:
        break
assert state["schet"] == 10
assert len(state["vragi"]) == 0
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
    r = run_plain(
        """
import app as app_module
client = app_module.app.test_client()
resp = client.get("/")
assert resp.status_code == 200
assert "Выучить основы Python" in resp.get_data(as_text=True)
resp2 = client.post("/dobavit", data={"zadacha": "Новая задача"})
assert resp2.status_code == 302
assert "Новая задача" in app_module.zadachi
print("OK")
""",
        ROOT / "projects" / "flask" / "todo-app",
    )
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout
