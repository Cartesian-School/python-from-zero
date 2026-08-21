#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 18 (Рисовалка на Canvas), ID 18-09..18-32.

18-02..18-07 существуют с прошлой версии главы и не пересобираются здесь.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-18"

MAINLOOP_NOTE_MD = (
    "## Про mainloop() в этом ноутбуке\n\n"
    "Вместо `root.mainloop()` здесь используется `root.update()` + `root.destroy()` — "
    "приложение строится точно так же, просто без бесконечного ожидания в конце (см. "
    "объяснение в ноутбуках главы 16)."
)


def _lesson_link(lesson_id: str, title: str, href: str) -> str:
    return f"# {lesson_id} · {title}\n\nПрактика к разделу [«{title}»](../../site/chapters/glava-18/{href})."


# ---------------------------------------------------------------------------
# browser-auto (Pyodide): чистая логика, без tkinter
# ---------------------------------------------------------------------------

def build_09() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-09", "Система координат Canvas", "18-09-sistema-koordinat.html"))
    nb.md("## Цель\n\nОпределять направление движения курсора по координатам Canvas — Y растёт вниз.")
    nb.md("## Рабочий пример")
    nb.code('''def event_to_point(x, y):
    return (x, y)


def dvizhenie_vniz(y_start, y_end):
    """True, если курсор сдвинулся ВНИЗ (Y увеличился) — как на Canvas, не как у Turtle."""
    return y_end > y_start


p1 = event_to_point(40, 30)
p2 = event_to_point(160, 120)
print(p1, p2, dvizhenie_vniz(p1[1], p2[1]))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert p1 == (40, 30)
assert p2 == (160, 120)
assert dvizhenie_vniz(30, 120) is True
assert dvizhenie_vniz(120, 30) is False
assert dvizhenie_vniz(50, 50) is False
print("Направление определяется верно.")''')
    nb.write(OUT_DIR / "18-09-sistema-koordinat.ipynb")
    print(f"Записано: 18-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-10", "Item ID: что возвращает create_*", "18-10-item-id.html"))
    nb.md("## Цель\n\nХранить фигуры по item_id — как по ключу словаря, а не как по индексу списка.")
    nb.md("## Рабочий пример")
    nb.code('''shapes_by_id = {}


def zaregistrirovat_figuru(shapes_by_id, item_id, kind):
    shapes_by_id[item_id] = kind
    return shapes_by_id


zaregistrirovat_figuru(shapes_by_id, 3, "rectangle")
zaregistrirovat_figuru(shapes_by_id, 7, "oval")
print(shapes_by_id)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert shapes_by_id[3] == "rectangle"
assert shapes_by_id[7] == "oval"
assert 5 not in shapes_by_id
print("item_id используется как ключ словаря, а не как индекс списка.")''')
    nb.write(OUT_DIR / "18-10-item-id.ipynb")
    print(f"Записано: 18-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-11", "Теги: группируем и выбираем элементы", "18-11-tegi.html"))
    nb.md("## Цель\n\nСмоделировать группировку элементов Canvas по тегам — без Tkinter.")
    nb.md("## Рабочий пример")
    nb.code('''tegi = {}


def dobavit_v_teg(tegi, tag, item_id):
    tegi.setdefault(tag, []).append(item_id)
    return tegi


dobavit_v_teg(tegi, "shape", 12)
dobavit_v_teg(tegi, "shape", 13)
dobavit_v_teg(tegi, "preview", 15)
print(tegi)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert tegi["shape"] == [12, 13]
assert tegi["preview"] == [15]
assert len(tegi["shape"]) == 2
print("Один тег — сразу несколько элементов.")''')
    nb.write(OUT_DIR / "18-11-tegi.ipynb")
    print(f"Записано: 18-11 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-13", "Состояние рисования", "18-13-sostoyanie-risovaniya.html"))
    nb.md("## Цель\n\nСобрать DrawingState как dataclass и проверить выбор инструмента без Tkinter.")
    nb.md("## Рабочий пример")
    nb.code('''from dataclasses import dataclass
from enum import Enum


class Tool(Enum):
    PENCIL = "pencil"
    LINE = "line"
    RECTANGLE = "rectangle"
    OVAL = "oval"
    ERASER = "eraser"


@dataclass
class DrawingState:
    tool: Tool = Tool.PENCIL
    color: str = "#111827"
    width: int = 4


state = DrawingState()
state.tool = Tool.RECTANGLE
state.color = "#2563eb"
print(state)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert state.tool is Tool.RECTANGLE
assert state.color == "#2563eb"
assert state.width == 4
print("Инструмент, цвет и толщина живут в одном объекте состояния.")''')
    nb.write(OUT_DIR / "18-13-sostoyanie-risovaniya.ipynb")
    print(f"Записано: 18-13 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-16", "Геометрия прямоугольника", "18-16-geometriya-pryamougolnika.html"))
    nb.md("## Цель\n\nnormalize_bounds() приводит координаты к (left, top, right, bottom) независимо от направления перетаскивания.")
    nb.md("## Рабочий пример")
    nb.code('''def normalize_bounds(x1, y1, x2, y2):
    """Приводит две произвольные противоположные точки к (left, top, right, bottom)."""
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)


r_vniz_vpravo = normalize_bounds(10, 10, 100, 80)
r_vverh_vlevo = normalize_bounds(100, 80, 10, 10)
print(r_vniz_vpravo, r_vverh_vlevo)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert r_vniz_vpravo == (10, 10, 100, 80)
assert r_vverh_vlevo == (10, 10, 100, 80)
assert normalize_bounds(100, 10, 10, 80) == (10, 10, 100, 80)  # вниз-влево
assert normalize_bounds(10, 80, 100, 10) == (10, 10, 100, 80)  # вверх-вправо
assert normalize_bounds(50, 50, 50, 50) == (50, 50, 50, 50)    # без перетаскивания
print("Все четыре направления дают одинаковые нормализованные границы.")''')
    nb.write(OUT_DIR / "18-16-geometriya-pryamougolnika.ipynb")
    print(f"Записано: 18-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-17", "Геометрия овала", "18-17-geometriya-ovala.html"))
    nb.md("## Цель\n\nПереводить координаты между «центр + радиус» и ограничивающим прямоугольником create_oval.")
    nb.md("## Рабочий пример")
    nb.code('''def bounds_from_center(cx, cy, r):
    return cx - r, cy - r, cx + r, cy + r


def center_from_bounds(x1, y1, x2, y2):
    return (x1 + x2) / 2, (y1 + y2) / 2


bounds = bounds_from_center(50, 50, 20)
center = center_from_bounds(*bounds)
print(bounds, center)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert bounds == (30, 30, 70, 70)
assert center == (50.0, 50.0)
assert bounds_from_center(0, 0, 10) == (-10, -10, 10, 10)
print("Круг — это овал, чей ограничивающий прямоугольник является квадратом.")''')
    nb.write(OUT_DIR / "18-17-geometriya-ovala.ipynb")
    print(f"Записано: 18-17 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-20", "Порядок наложения", "18-20-poryadok-sloev.html"))
    nb.md("## Цель\n\nСмоделировать tag_raise() как список, где последний элемент рисуется сверху.")
    nb.md("## Рабочий пример")
    nb.code('''def podnyat(poryadok, item_id):
    """Аналог canvas.tag_raise(item_id) — переносит элемент в конец списка (наверх)."""
    poryadok.remove(item_id)
    poryadok.append(item_id)
    return poryadok


poryadok = [12, 13, 14]
podnyat(poryadok, 12)
print(poryadok)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert poryadok == [13, 14, 12]
poryadok2 = [1, 2, 3]
podnyat(poryadok2, 2)
assert poryadok2 == [1, 3, 2]
print("Последний элемент списка — верхний в порядке наложения.")''')
    nb.write(OUT_DIR / "18-20-poryadok-sloev.ipynb")
    print(f"Записано: 18-20 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-24", "Отмена действий (Undo)", "18-24-otmena-deystviy.html"))
    nb.md("## Цель\n\nUndo убирает ВСЕ элементы одного действия целиком — даже если их несколько.")
    nb.md("## Рабочий пример")
    nb.code('''document = []
undo_stack = []


def commit_action(document, undo_stack, shapes):
    document.extend(shapes)
    undo_stack.append(shapes)


def undo(document, undo_stack):
    if not undo_stack:
        return
    shapes = undo_stack.pop()
    del document[len(document) - len(shapes):]


commit_action(document, undo_stack, ["rect"])
commit_action(document, undo_stack, ["line1", "line2", "line3"])  # один карандашный штрих
print(document)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''undo(document, undo_stack)
assert document == ["rect"], "Undo должен убрать ВСЕ три отрезка штриха, а не один"
assert len(undo_stack) == 1
print("Штрих из трёх отрезков отменяется одним Undo.")''')
    nb.write(OUT_DIR / "18-24-otmena-deystviy.ipynb")
    print(f"Записано: 18-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-25", "Повтор действий (Redo)", "18-25-povtor-deystviy.html"))
    nb.md("## Цель\n\nRedo восстанавливает отменённое действие; новое действие обязано очистить redo_stack.")
    nb.md("## Рабочий пример")
    nb.code('''document, undo_stack, redo_stack = [], [], []


def commit_action(shapes):
    document.extend(shapes)
    undo_stack.append(shapes)
    redo_stack.clear()  # новое действие делает старую ветку redo недействительной


def undo():
    if not undo_stack:
        return
    shapes = undo_stack.pop()
    del document[len(document) - len(shapes):]
    redo_stack.append(shapes)


def redo():
    if not redo_stack:
        return
    shapes = redo_stack.pop()
    document.extend(shapes)
    undo_stack.append(shapes)


commit_action(["A"])
commit_action(["B"])
undo()
print(document, redo_stack)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert document == ["A"]
assert redo_stack == [["B"]]
redo()
assert document == ["A", "B"]
undo()
commit_action(["C"])  # новое действие ПОСЛЕ undo — должно очистить redo_stack
assert document == ["A", "C"]
assert redo_stack == [], "новое действие обязано очистить старую ветку redo"
print("Redo работает, а новое действие очищает устаревшую историю redo.")''')
    nb.write(OUT_DIR / "18-25-povtor-deystviy.ipynb")
    print(f"Записано: 18-25 ({len(nb)} ячеек)")


def build_31() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-31", "Debug Labs", "18-31-debug-labs.html"))
    nb.md("## Цель\n\nОчистка холста обязана обнулять историю отмены вместе с документом.")
    nb.md("## Рабочий пример — воспроизводим Debug Lab 11")
    nb.code('''document = ["A"]
undo_stack = [["A"]]
redo_stack = []


def clear_canvas(document, undo_stack, redo_stack):
    document.clear()
    undo_stack.clear()
    redo_stack.clear()


clear_canvas(document, undo_stack, redo_stack)
print(document, undo_stack, redo_stack)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert document == []
assert undo_stack == [], "история отмены должна очищаться вместе с документом"
assert redo_stack == []
print("Очистка холста обнулила и документ, и всю его историю.")''')
    nb.write(OUT_DIR / "18-31-debug-labs.ipynb")
    print(f"Записано: 18-31 ({len(nb)} ячеек)")


# ---------------------------------------------------------------------------
# local-required: настоящий tkinter, выполняется на компьютере читателя
# ---------------------------------------------------------------------------

def build_12() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-12", "Жизненный цикл жеста мыши", "18-12-zhest-myshi.html"))
    nb.md("## Цель\n\nУвидеть на живом окне последовательность press → drag → release.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

log = []

def on_press(event):
    log.append(("press", event.x, event.y))

def on_drag(event):
    log.append(("drag", event.x, event.y))

def on_release(event):
    log.append(("release", event.x, event.y))

canvas.bind("<Button-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)
root.update()
print("Привязки готовы — реальный клик и перетаскивание добавят записи в log.")
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоздайте окно с холстом БЕЗ `root.destroy()`, запустите `root.mainloop()`, "
          "нарисуйте мышью несколько жестов и напечатайте `log` — убедитесь, что порядок всегда "
          "`press → (drag)* → release`, и что между `release` одного жеста и `press` следующего нет `drag`.")
    nb.write(OUT_DIR / "18-12-zhest-myshi.ipynb")
    print(f"Записано: 18-12 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-14", "Карандаш: непрерывный штрих", "18-14-karandash.html"))
    nb.md("## Цель\n\nПостроить непрерывный штрих через last_x/last_y вместо отдельных кружков.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

last_x, last_y = None, None

def on_press(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def on_drag(event):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y, width=3, capstyle=tk.ROUND, smooth=True)
    last_x, last_y = event.x, event.y

canvas.bind("<Button-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
root.update()
print("Готово — попробуйте нарисовать мышью, штрих не должен рассыпаться на точки.")
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nЗамените непрерывный штрих на версию из раздела 18.7 (кружок на каждое "
          "движение мыши) и сравните визуально с этой версией на резком, быстром движении курсора — где заметнее разрывы?")
    nb.write(OUT_DIR / "18-14-karandash.ipynb")
    print(f"Записано: 18-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-15", "Инструмент «Линия»", "18-15-instrument-liniya.html"))
    nb.md("## Цель\n\nСобрать инструмент «Линия» с пунктирным превью, обновляемым через coords().")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

start_x = start_y = None
preview_id = None

def on_press(event):
    global start_x, start_y, preview_id
    start_x, start_y = event.x, event.y
    preview_id = canvas.create_line(event.x, event.y, event.x, event.y, dash=(4, 2))

def on_drag(event):
    canvas.coords(preview_id, start_x, start_y, event.x, event.y)

def on_release(event):
    canvas.delete(preview_id)
    canvas.create_line(start_x, start_y, event.x, event.y, width=3)

canvas.bind("<Button-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)
root.update()
print("Готово — потяните мышью: пунктир превью должен смениться сплошной линией на отпускании.")
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте `fill=\"red\"` в оба вызова `create_line` — и в превью, и в "
          "финальную линию — так, чтобы цвет совпадал.")
    nb.write(OUT_DIR / "18-15-instrument-liniya.ipynb")
    print(f"Записано: 18-15 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-18", "Живое превью: coords()", "18-18-zhivoe-prevyu.html"))
    nb.md("## Цель\n\nCREATE ONCE → UPDATE MANY TIMES → COMMIT для прямоугольника-превью.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

start_x = start_y = None
preview_id = None

def on_press(event):
    global start_x, start_y, preview_id
    start_x, start_y = event.x, event.y
    preview_id = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="blue", dash=(4, 2))

def on_drag(event):
    canvas.coords(preview_id, start_x, start_y, event.x, event.y)  # ОДИН и тот же элемент

canvas.bind("<Button-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
root.update()
before = canvas.find_all()
print("Элементов на холсте после нажатия:", len(before))
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПодтвердите на реальном окне, что во время долгого перетаскивания "
          "количество элементов на холсте (`len(canvas.find_all())`) не растёт — потому что coords() обновляет "
          "существующий элемент, а не создаёт новые.")
    nb.write(OUT_DIR / "18-18-zhivoe-prevyu.ipynb")
    print(f"Записано: 18-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-19", "itemconfig, move, delete", "18-19-redaktirovanie-elementov.html"))
    nb.md("## Цель\n\nИзменить уже существующий элемент Canvas: coords, itemconfig, move, delete.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

item_id = canvas.create_rectangle(10, 10, 80, 60, outline="black", width=2)
root.update()

canvas.itemconfig(item_id, outline="blue", width=4)
canvas.move(item_id, 30, 0)
root.update()
print("Текущие координаты:", canvas.coords(item_id))
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nВызовите `canvas.move(item_id, 30, 0)` ДВАЖДЫ подряд и напечатайте "
          "`canvas.coords(item_id)` — убедитесь, что элемент сдвинулся на 60 пикселей суммарно, а не остался на месте.")
    nb.write(OUT_DIR / "18-19-redaktirovanie-elementov.ipynb")
    print(f"Записано: 18-19 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-21", "Система цвета", "18-21-sistema-cveta.html"))
    nb.md("## Цель\n\nПалитра цветов и честная проверка отмены colorchooser.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

PALETTE = [("Чёрный", "#111827"), ("Красный", "#dc2626"), ("Синий", "#2563eb")]

root = tk.Tk()
current_color = tk.StringVar(value=PALETTE[0][1])

def set_color(hex_color):
    current_color.set(hex_color)

toolbar = tk.Frame(root)
toolbar.pack()
for name, hex_color in PALETTE:
    tk.Button(toolbar, bg=hex_color, width=2, command=lambda c=hex_color: set_color(c)).pack(side="left")

root.update()
print("Текущий цвет:", current_color.get())
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nНапишите функцию `choose_custom_color()`, вызывающую "
          "`tkinter.colorchooser.askcolor()`, и явно проверьте `hex_color is not None` перед вызовом "
          "`set_color(hex_color)` — что произойдёт, если убрать эту проверку и нажать «Отмена» в диалоге?")
    nb.write(OUT_DIR / "18-21-sistema-cveta.ipynb")
    print(f"Записано: 18-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-22", "Толщина кисти", "18-22-tolschina-kisti.html"))
    nb.md("## Цель\n\nScale для толщины линии, связанный с состоянием рисования.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
width = {"value": 4}

def set_width(value):
    width["value"] = int(value)

scale = tk.Scale(root, from_=1, to=20, orient="horizontal", command=set_width)
scale.set(4)
scale.pack()
root.update()
print("Текущая толщина:", width["value"])
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСвяжите `width['value']` с реальным рисованием: нарисуйте на холсте "
          "четыре линии с шириной 1, 3, 8 и 16, используя `scale.set(...)` перед каждой.")
    nb.write(OUT_DIR / "18-22-tolschina-kisti.ipynb")
    print(f"Записано: 18-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-23", "Ластик", "18-23-lastik.html"))
    nb.md("## Цель\n\nЛастик как штрих цветом фона — тот же механизм, что и карандаш.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

CANVAS_BG = "#ffffff"

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg=CANVAS_BG)
canvas.pack()

canvas.create_line(20, 20, 200, 20, fill="black", width=6)  # "нарисованная" линия

def stereet(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, fill=CANVAS_BG, width=10, capstyle=tk.ROUND)

stereet(50, 20, 150, 20)
root.update()
print("Элементов на холсте:", len(canvas.find_all()))  # линия НЕ удалена, просто перекрыта
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте на реальном окне: `len(canvas.find_all())` после "
          "«стирания» БОЛЬШЕ, а не меньше — потому что ластик добавляет новый элемент поверх старого, а не удаляет его. "
          "Как это скажется, если фон холста позже станет не белым?")
    nb.write(OUT_DIR / "18-23-lastik.ipynb")
    print(f"Записано: 18-23 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-26", "Очистка холста", "18-26-ochistka-holsta.html"))
    nb.md("## Цель\n\nОчистка холста с подтверждением и полным обнулением истории.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()
canvas.create_rectangle(10, 10, 80, 60)
canvas.create_oval(100, 30, 160, 90)

document = ["rect", "oval"]
undo_stack = [["rect"], ["oval"]]

def clear_canvas():
    canvas.delete("all")
    document.clear()
    undo_stack.clear()

clear_canvas()
root.update()
print("Элементов на холсте:", len(canvas.find_all()), "| документ:", document, "| история:", undo_stack)
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте `messagebox.askyesno(...)` перед очисткой — но только если "
          "`document` не пуст. Проверьте, что при пустом документе диалог не появляется вовсе.")
    nb.write(OUT_DIR / "18-26-ochistka-holsta.ipynb")
    print(f"Записано: 18-26 ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-27", "Горячие клавиши", "18-27-goryachie-klavishi.html"))
    nb.md("## Цель\n\nПривязать Ctrl+Z/Ctrl+Y к отмене и повтору на уровне окна.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
log = []

def undo(_event=None):
    log.append("undo")

def redo(_event=None):
    log.append("redo")

root.bind("<Control-z>", undo)
root.bind("<Control-y>", redo)
root.update()
print("Привязки готовы:", root.bind("<Control-z>") is not None)
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nЗапустите окно с `root.mainloop()` (без `root.destroy()`), нажмите "
          "Ctrl+Z и Ctrl+Y несколько раз и напечатайте `log` — убедитесь, что порядок вызовов совпадает с порядком нажатий.")
    nb.write(OUT_DIR / "18-27-goryachie-klavishi.ipynb")
    print(f"Записано: 18-27 ({len(nb)} ячеек)")


def build_28() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-28", "Строка состояния", "18-28-stroka-sostoyaniya.html"))
    nb.md("## Цель\n\nСтрока состояния, обновляемая по координатам мыши и параметрам инструмента.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()
status_var = tk.StringVar()
tk.Label(root, textvariable=status_var).pack()

def update_status(x, y):
    status_var.set(f"Инструмент: Карандаш | x={x} y={y} | Цвет: #111827 | Толщина: 4")

canvas.bind("<Motion>", lambda event: update_status(event.x, event.y))
root.update()
update_status(0, 0)
print(status_var.get())
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nЗапустите с `root.mainloop()`, подвигайте мышью над холстом и "
          "убедитесь, что координаты в строке состояния меняются в реальном времени.")
    nb.write(OUT_DIR / "18-28-stroka-sostoyaniya.ipynb")
    print(f"Записано: 18-28 ({len(nb)} ячеек)")


def build_29() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-29", "Архитектура PaintApp", "18-29-arhitektura-paintapp.html"))
    nb.md("## Цель\n\nСобрать объектный граф PaintApp: root, state, document, canvas — в одном классе.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import sys
sys.path.insert(0, "../../projects/tkinter/paint-app")

import tkinter as tk
import paint_app as p

root = tk.Tk()
app = p.PaintApp(root)
root.update()

print(type(app.root), type(app.state), type(app.document), type(app.canvas))
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте, что `app.state.tool` меняется после вызова "
          "`app.set_tool(p.Tool.RECTANGLE)`, и что это же отражается на `relief` соответствующей кнопки панели инструментов.")
    nb.write(OUT_DIR / "18-29-arhitektura-paintapp.ipynb")
    print(f"Записано: 18-29 ({len(nb)} ячеек)")


def build_30() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-30", "Сохранение и загрузка JSON", "18-30-sohranenie-json.html"))
    nb.md("## Цель\n\nСохранить документ рисунка в JSON и загрузить его заново — без потери фигур.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import sys
sys.path.insert(0, "../../projects/tkinter/paint-app")

import tkinter as tk
from pathlib import Path
import paint_app as p

root = tk.Tk()
app = p.PaintApp(root)

app.document = [p.Shape(kind="rectangle", coords=[10, 10, 100, 80], color="#2563eb", width=4)]

tmp_path = Path("_tmp_practice_drawing.json")
app._write_document(tmp_path)
app.load_from_path(tmp_path)

print(app.document)
tmp_path.unlink()
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nНарисуйте мышью несколько настоящих фигур на реальном окне, "
          "сохраните через `app.save_document()` (Ctrl+S), закройте приложение, откройте заново и загрузите файл "
          "через `app.load_document()` (Ctrl+O) — рисунок должен восстановиться.")
    nb.write(OUT_DIR / "18-30-sohranenie-json.ipynb")
    print(f"Записано: 18-30 ({len(nb)} ячеек)")


def build_32() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("18-32", "Paint Pro — итоги главы", "18-32-paint-pro-itogi.html"))
    nb.md("## Цель\n\nСобрать и запустить готовое приложение Paint Pro целиком.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import sys
sys.path.insert(0, "../../projects/tkinter/paint-app")

import tkinter as tk
import paint_app as p

root = tk.Tk()
app = p.PaintApp(root)
root.update()

class FakeEvent:
    def __init__(self, x, y):
        self.x, self.y = x, y

app.set_tool(p.Tool.RECTANGLE)
app.on_press(FakeEvent(10, 10))
app.on_drag(FakeEvent(100, 80))
app.on_release(FakeEvent(100, 80))
print("Фигур в документе:", len(app.document))
root.destroy()''')
    nb.md("## Задание ★★★ Итоговая практика\n\nЗапустите `python paint_app.py` целиком, нарисуйте рисунок с "
          "использованием всех инструментов (карандаш, линия, прямоугольник, овал, ластик), отмените и повторите "
          "хотя бы одно действие, сохраните рисунок и откройте его заново.")
    nb.write(OUT_DIR / "18-32-paint-pro-itogi.ipynb")
    print(f"Записано: 18-32 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_09()
    build_10()
    build_11()
    build_12()
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_22()
    build_23()
    build_24()
    build_25()
    build_26()
    build_27()
    build_28()
    build_29()
    build_30()
    build_31()
    build_32()
