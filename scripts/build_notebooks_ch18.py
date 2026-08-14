#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 18 (рисовалка).

Мышь в ноутбуке симулируется маленьким классом FakeEvent(x, y) с полями .x/.y —
он подставляется вместо настоящего события Tkinter напрямую в функции-обработчики,
проверяя, что сама логика рисования работает правильно.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-18"

MAINLOOP_NOTE_MD = (
    "## Про mainloop() и события мыши в этом ноутбуке\n\n"
    "Вместо `root.mainloop()` здесь используется `root.update()` + `root.destroy()`. А вместо "
    "настоящих кликов мышью мы вызываем функции-обработчики напрямую с маленьким объектом "
    "`FakeEvent(x, y)` вместо настоящего события — Tkinter в реальном приложении передаёт "
    "объект с такими же полями `.x`/`.y`, так что код обработчиков проверяется по-настоящему."
)

FAKE_EVENT = '''class FakeEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y'''


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 18-02 · Холст (Canvas)\n\nПрактика к разделу "
          "[«Настраиваем экран. Создаём холст»](../../site/chapters/glava-18/18-02-ekran-holst.html).")
    nb.md("## Цель\n\nСоздать Canvas и нарисовать на нём вручную.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

canvas.create_line(10, 10, 100, 100, fill="black", width=2)
print("Фигур на холсте:", len(canvas.find_all()))
root.update()
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте прямоугольник и овал прямо командами "
          "create_rectangle/create_oval.")
    nb.code('''root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=400, bg="white")

canvas.create_rectangle(50, 50, 150, 120, outline="red", width=3)
canvas.create_oval(200, 50, 300, 150, outline="blue", width=3)

print("Фигур на холсте:", len(canvas.find_all()))
root.update()
root.destroy()''')
    nb.write(OUT_DIR / "18-02-holst.ipynb")
    print(f"Записано: 18-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 18-03 · Панель инструментов и параметры\n\nПрактика к разделу "
          "[«Создаём первое меню (фигуры). Параметры рисования»](../../site/chapters/glava-18/18-03-menu-parametry.html).")
    nb.md("## Цель\n\nПостроить панель инструментов и переменные состояния.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
toolbar = tk.Frame(root)
toolbar.pack(side="top", fill="x")

tekuschaya_figura = "linia"

def vybrat_figuru(figura):
    global tekuschaya_figura
    tekuschaya_figura = figura

tk.Button(toolbar, text="Линия", command=lambda: vybrat_figuru("linia")).pack(side="left")
tk.Button(toolbar, text="Прямоугольник", command=lambda: vybrat_figuru("pryamougolnik")).pack(side="left")
tk.Button(toolbar, text="Овал", command=lambda: vybrat_figuru("oval")).pack(side="left")

root.update()

# симулируем клик по кнопке "Овал"
toolbar.winfo_children()[2].invoke()
print("Текущая фигура:", tekuschaya_figura)
root.destroy()''')
    nb.write(OUT_DIR / "18-03-parametry.ipynb")
    print(f"Записано: 18-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 18-04 · Позиция мыши и линии\n\nПрактика к разделу "
          "[«Получаем позицию мыши. Рисуем линии»](../../site/chapters/glava-18/18-04-mysh-linii.html).")
    nb.md("## Цель\n\nОтследить позицию мыши и нарисовать линию по событиям.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code(FAKE_EVENT)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

pozicia_label = tk.Label(root, text="x=0, y=0")
pozicia_label.pack()

def pokazat_poziciyu(event):
    pozicia_label.config(text=f"x={event.x}, y={event.y}")

pokazat_poziciyu(FakeEvent(150, 75))
print(pozicia_label.cget("text"))''')
    nb.md("## Эксперимент 1 — рисуем линию по двум событиям")
    nb.code('''tekuschij_cvet = "black"
tolschina = 3
start_x, start_y = None, None

def nachalo_risovaniya(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def vo_vremya_risovaniya(event):
    canvas.create_line(start_x, start_y, event.x, event.y, fill=tekuschij_cvet, width=tolschina)

before = len(canvas.find_all())
nachalo_risovaniya(FakeEvent(10, 10))
vo_vremya_risovaniya(FakeEvent(200, 150))
after = len(canvas.find_all())
print("Фигур до/после:", before, after)
root.update()
root.destroy()''')
    nb.md("## Проверка результата")
    nb.code('''assert after == before + 1
print("Верно: ровно одна новая линия появилась на холсте.")''')
    nb.write(OUT_DIR / "18-04-linii.ipynb")
    print(f"Записано: 18-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 18-05 · Фигуры\n\nПрактика к разделу "
          "[«Квадраты и прямоугольники! Круги и овалы!»](../../site/chapters/glava-18/18-05-figury.html).")
    nb.md("## Цель\n\nНарисовать прямоугольник и овал по событиям мыши.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code(FAKE_EVENT)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

tekuschaya_figura = "pryamougolnik"
tekuschij_cvet = "red"
tolschina = 2
start_x, start_y = 20, 20

def narisovat_figuru(event, figura):
    if figura == "pryamougolnik":
        return canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=tekuschij_cvet, width=tolschina)
    elif figura == "oval":
        return canvas.create_oval(start_x, start_y, event.x, event.y, outline=tekuschij_cvet, width=tolschina)

id1 = narisovat_figuru(FakeEvent(120, 100), "pryamougolnik")
id2 = narisovat_figuru(FakeEvent(220, 180), "oval")
print("Создано id:", id1, id2)
print("Всего фигур:", len(canvas.find_all()))
root.update()
root.destroy()''')
    nb.write(OUT_DIR / "18-05-figury.ipynb")
    print(f"Записано: 18-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 18-06 · Размер и цвет\n\nПрактика к разделу "
          "[«Выбираем размер! Очень много цветов!»](../../site/chapters/glava-18/18-06-razmer-cveta.html).")
    nb.md("## Цель\n\nОсвоить Scale и палитру цветов циклом.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример — Scale")
    nb.code('''import tkinter as tk

root = tk.Tk()
tolschina = 3

def vybrat_tolschinu(znachenie):
    global tolschina
    tolschina = int(znachenie)

scale = tk.Scale(root, from_=1, to=10, orient="horizontal", command=vybrat_tolschinu)
scale.set(7)
root.update()
print("Толщина:", tolschina)
root.destroy()''')
    nb.md("## Эксперимент 1 — палитра цветов циклом")
    nb.code('''root = tk.Tk()
toolbar = tk.Frame(root)
toolbar.pack()

tekuschij_cvet = "black"

def vybrat_cvet(cvet):
    global tekuschij_cvet
    tekuschij_cvet = cvet

cveta = ["black", "red", "blue", "green", "orange", "purple"]
knopki = []
for cvet in cveta:
    b = tk.Button(toolbar, bg=cvet, width=2, command=lambda c=cvet: vybrat_cvet(c))
    b.pack(side="left")
    knopki.append(b)

root.update()
knopki[3].invoke()  # "зелёный" — четвёртая кнопка
print("Выбранный цвет:", tekuschij_cvet)
root.destroy()''')
    nb.md("## Проверка результата")
    nb.code('''assert tekuschij_cvet == "green"
print("Верно: четвёртая кнопка палитры выбрала зелёный.")''')
    nb.write(OUT_DIR / "18-06-razmer-cveta.ipynb")
    print(f"Записано: 18-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 18-07 · Полное приложение\n\nПрактика к разделу "
          "[«Я закончил рисовать! Полная программа»](../../site/chapters/glava-18/18-07-polnaya-programma-itogi.html).")
    nb.md("## Цель\n\nСобрать и протестировать рисовалку целиком — тот же код, что и в "
          "`projects/tkinter/paint-app/paint_app.py`.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code(FAKE_EVENT)
    nb.md("## Полное приложение")
    nb.code('''import tkinter as tk

root = tk.Tk()
root.title("Рисовалка")

tekuschaya_figura = "linia"
tekuschij_cvet = "black"
tolschina = 3
start_x = None
start_y = None
vremennaya_figura = None


def vybrat_figuru(figura):
    global tekuschaya_figura
    tekuschaya_figura = figura


def vybrat_cvet(cvet):
    global tekuschij_cvet
    tekuschij_cvet = cvet


def vybrat_tolschinu(znachenie):
    global tolschina
    tolschina = int(znachenie)


def nachalo_risovaniya(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y
    if tekuschaya_figura == "svobodno":
        canvas.create_oval(
            event.x - tolschina, event.y - tolschina,
            event.x + tolschina, event.y + tolschina,
            fill=tekuschij_cvet, outline=tekuschij_cvet,
        )


def vo_vremya_risovaniya(event):
    global vremennaya_figura
    if tekuschaya_figura == "svobodno":
        canvas.create_oval(
            event.x - tolschina, event.y - tolschina,
            event.x + tolschina, event.y + tolschina,
            fill=tekuschij_cvet, outline=tekuschij_cvet,
        )
        return

    if vremennaya_figura is not None:
        canvas.delete(vremennaya_figura)

    if tekuschaya_figura == "linia":
        vremennaya_figura = canvas.create_line(start_x, start_y, event.x, event.y, fill=tekuschij_cvet, width=tolschina)
    elif tekuschaya_figura == "pryamougolnik":
        vremennaya_figura = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=tekuschij_cvet, width=tolschina)
    elif tekuschaya_figura == "oval":
        vremennaya_figura = canvas.create_oval(start_x, start_y, event.x, event.y, outline=tekuschij_cvet, width=tolschina)


def konec_risovaniya(event):
    global vremennaya_figura
    vremennaya_figura = None


def ochistit_holst():
    canvas.delete("all")


canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()
canvas.bind("<Button-1>", nachalo_risovaniya)
canvas.bind("<B1-Motion>", vo_vremya_risovaniya)
canvas.bind("<ButtonRelease-1>", konec_risovaniya)

print("Рисовалка построена.")
root.update()''')
    nb.md("## Проверка результата — рисуем линию, прямоугольник, очищаем")
    nb.code('''before = len(canvas.find_all())
nachalo_risovaniya(FakeEvent(10, 10))
vo_vremya_risovaniya(FakeEvent(100, 100))
konec_risovaniya(FakeEvent(100, 100))
posle_linii = len(canvas.find_all())
print("После линии:", posle_linii, "(было", before, ")")
assert posle_linii == before + 1

vybrat_figuru("pryamougolnik")
nachalo_risovaniya(FakeEvent(20, 20))
vo_vremya_risovaniya(FakeEvent(80, 80))
konec_risovaniya(FakeEvent(80, 80))
posle_pryamougolnika = len(canvas.find_all())
print("После прямоугольника:", posle_pryamougolnika)
assert posle_pryamougolnika == posle_linii + 1

ochistit_holst()
assert len(canvas.find_all()) == 0
print("Холст очищен — всё верно.")

root.destroy()''')
    nb.write(OUT_DIR / "18-07-polnoe-prilozhenie.ipynb")
    print(f"Записано: 18-07 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
    build_07()
