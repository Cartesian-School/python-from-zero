#!/usr/bin/env python3
"""Генерирует настоящие скриншоты Tkinter-рисовалки для главы 18.

Каждый скриншот получен, запустив реальный код проекта (paint_app_basic.py
или paint_app.py — класс PaintApp) и подведя его к нужному состоянию через
его собственные методы (on_press/on_drag/on_release/set_tool/undo/...) — не
имитация HTML/CSS и не нарисованный вручную интерфейс.

Требует headless X-сервер (xvfb-run).
Использование: xvfb-run -a python3 scripts/generate_chapter_18_outputs.py
"""

import importlib
import sys
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageChops, ImageGrab

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-18" / "output"
sys.path.insert(0, str(ROOT / "projects" / "tkinter" / "paint-app"))

import paint_app as p  # noqa: E402
import paint_app_basic as pb  # noqa: E402

# paint_app_basic.py builds its window at module level (no __main__ guard around
# widget creation) — importing it here for its functions already opens a window.
# ImageGrab.grab() captures the SCREEN at absolute coordinates, not a specific Tk
# window, so this leftover window would silently show through underneath the
# very first capture() call unless destroyed immediately.
pb.root.destroy()


class FakeEvent:
    def __init__(self, x, y):
        self.x, self.y = x, y


def _autocrop(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    bg = Image.new("RGB", rgb.size, (0, 0, 0))
    bbox = ImageChops.difference(rgb, bg).getbbox()
    return img.crop(bbox) if bbox else img


def capture(name: str, root: tk.Tk, *, grab_w: int = 700, grab_h: int = 500) -> None:
    root.update_idletasks()
    root.update()
    img = ImageGrab.grab(bbox=(0, 0, grab_w, grab_h))
    img = _autocrop(img)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    img.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({img.size[0]}x{img.size[1]})")
    root.destroy()


def new_app() -> tuple[tk.Tk, "p.PaintApp"]:
    root = tk.Tk()
    root.geometry("+0+0")
    app = p.PaintApp(root)
    return root, app


def new_basic_app():
    """paint_app_basic.py строит окно на уровне модуля — как и tic_tac_toe_basic.py
    в главе 17, повторный import ничего не пересоздаст, поэтому используется
    importlib.reload() для получения свежего окна на каждый снимок."""
    importlib.reload(pb)
    pb.root.geometry("+0+0")
    return pb


# ---------------------------------------------------------------------------
# 01 / 31 — финальное приложение
# ---------------------------------------------------------------------------

def paint_pro_final() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.RECTANGLE)
    app.on_press(FakeEvent(40, 40))
    app.on_drag(FakeEvent(160, 120))
    app.on_release(FakeEvent(160, 120))
    app.set_tool(p.Tool.OVAL)
    app.set_color("#dc2626")
    app.on_press(FakeEvent(220, 60))
    app.on_drag(FakeEvent(320, 140))
    app.on_release(FakeEvent(320, 140))
    app.set_tool(p.Tool.LINE)
    app.set_color("#16a34a")
    app.on_press(FakeEvent(60, 180))
    app.on_drag(FakeEvent(250, 200))
    app.on_release(FakeEvent(250, 200))
    app.set_tool(p.Tool.PENCIL)
    app.set_color("#7c3aed")
    app.on_press(FakeEvent(300, 180))
    for x, y in [(310, 190), (325, 195), (340, 185), (355, 200)]:
        app.on_drag(FakeEvent(x, y))
    app.on_release(FakeEvent(355, 200))
    app.width_scale.set(6)
    app.set_tool(p.Tool.LINE)
    capture("paint-pro-final", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# первый прототип (paint_app_basic)
# ---------------------------------------------------------------------------

def empty_canvas() -> None:
    m = new_basic_app()
    capture("empty-canvas", m.root, grab_w=650, grab_h=460)


def toolbar_tools() -> None:
    m = new_basic_app()
    capture("toolbar-tools", m.root, grab_w=650, grab_h=460)


def color_palette() -> None:
    m = new_basic_app()
    capture("color-palette", m.root, grab_w=650, grab_h=460)


def rectangle_final_basic() -> None:
    m = new_basic_app()
    m.vybrat_figuru("pryamougolnik")
    m.nachalo_risovaniya(FakeEvent(40, 40))
    m.vo_vremya_risovaniya(FakeEvent(180, 130))
    m.konec_risovaniya(FakeEvent(180, 130))
    capture("rectangle-final", m.root, grab_w=650, grab_h=460)


def oval_final_basic() -> None:
    m = new_basic_app()
    m.vybrat_figuru("oval")
    m.nachalo_risovaniya(FakeEvent(60, 50))
    m.vo_vremya_risovaniya(FakeEvent(220, 160))
    m.konec_risovaniya(FakeEvent(220, 160))
    capture("oval-final", m.root, grab_w=650, grab_h=460)


def multiple_shapes() -> None:
    m = new_basic_app()
    m.vybrat_figuru("linia")
    m.nachalo_risovaniya(FakeEvent(20, 20))
    m.vo_vremya_risovaniya(FakeEvent(150, 60))
    m.konec_risovaniya(FakeEvent(150, 60))
    m.vybrat_figuru("pryamougolnik")
    m.vybrat_cvet("blue")
    m.nachalo_risovaniya(FakeEvent(30, 90))
    m.vo_vremya_risovaniya(FakeEvent(140, 170))
    m.konec_risovaniya(FakeEvent(140, 170))
    m.vybrat_figuru("oval")
    m.vybrat_cvet("green")
    m.nachalo_risovaniya(FakeEvent(180, 90))
    m.vo_vremya_risovaniya(FakeEvent(280, 170))
    m.konec_risovaniya(FakeEvent(280, 170))
    capture("multiple-shapes", m.root, grab_w=650, grab_h=460)


def freehand_naive_dots() -> None:
    m = new_basic_app()
    m.vybrat_figuru("svobodno")
    points = [(40, 40), (55, 60), (75, 55), (100, 90), (130, 80), (160, 110)]
    m.nachalo_risovaniya(FakeEvent(*points[0]))
    for x, y in points:
        m.vo_vremya_risovaniya(FakeEvent(x, y))
    m.konec_risovaniya(FakeEvent(*points[-1]))
    capture("freehand-naive-dots", m.root, grab_w=650, grab_h=460)


# ---------------------------------------------------------------------------
# координаты / направление осей
# ---------------------------------------------------------------------------

def canvas_coordinate_demo() -> None:
    root, app = new_app()
    p1, p2 = (50, 40), (280, 160)
    app.canvas.create_oval(p1[0] - 4, p1[1] - 4, p1[0] + 4, p1[1] + 4, fill="#5B24F9", outline="")
    app.canvas.create_text(p1[0] + 12, p1[1] - 10, text="P1", fill="#5B24F9", font=("Arial", 12, "bold"), anchor="w")
    app.canvas.create_oval(p2[0] - 4, p2[1] - 4, p2[0] + 4, p2[1] + 4, fill="#DB2777", outline="")
    app.canvas.create_text(p2[0] + 12, p2[1] - 10, text="P2", fill="#DB2777", font=("Arial", 12, "bold"), anchor="w")
    app.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="#0D0230", width=2, dash=(4, 2))
    capture("canvas-coordinate-demo", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# состояние инструмента: активная кнопка
# ---------------------------------------------------------------------------

def tool_pencil_selected() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.PENCIL)
    capture("tool-pencil-selected", root, grab_w=1175, grab_h=560)


def tool_line_selected() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.LINE)
    capture("tool-line-selected", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# жест мыши: press / preview / final (инструмент "Линия")
# ---------------------------------------------------------------------------

def mouse_press_start() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.LINE)
    app.on_press(FakeEvent(80, 80))
    capture("mouse-press-start", root, grab_w=1175, grab_h=560)


def mouse_drag_preview_line() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.LINE)
    app.on_press(FakeEvent(80, 80))
    app.on_drag(FakeEvent(260, 160))
    capture("mouse-drag-preview-line", root, grab_w=1175, grab_h=560)


def line_final() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.LINE)
    app.on_press(FakeEvent(80, 80))
    app.on_drag(FakeEvent(260, 160))
    app.on_release(FakeEvent(260, 160))
    capture("line-final", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# живое превью прямоугольника/овала
# ---------------------------------------------------------------------------

def rectangle_preview() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.RECTANGLE)
    app.on_press(FakeEvent(60, 60))
    app.on_drag(FakeEvent(220, 150))
    capture("rectangle-preview", root, grab_w=1175, grab_h=560)


def oval_preview() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.OVAL)
    app.on_press(FakeEvent(60, 60))
    app.on_drag(FakeEvent(220, 150))
    capture("oval-preview", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# карандаш: непрерывный штрих (Pro)
# ---------------------------------------------------------------------------

def freehand_connected_stroke() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.PENCIL)
    points = [(40, 40), (55, 60), (75, 55), (100, 90), (130, 80), (160, 110)]
    app.on_press(FakeEvent(*points[0]))
    for x, y in points:
        app.on_drag(FakeEvent(x, y))
    app.on_release(FakeEvent(*points[-1]))
    capture("freehand-connected-stroke", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# толщина кисти — реальное сравнение
# ---------------------------------------------------------------------------

def width_comparison() -> None:
    root, app = new_app()
    y = 40
    for width in (1, 3, 8, 16):
        app.canvas.create_line(40, y, 240, y, fill="#111827", width=width, capstyle=tk.ROUND)
        app.canvas.create_text(260, y, text=f"width={width}", anchor="w", font=("Arial", 11))
        y += 40
    capture("width-comparison", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# пользовательский цвет
# ---------------------------------------------------------------------------

def custom_color_result() -> None:
    root, app = new_app()
    app.set_color("#0891b2")  # эмулирует результат выбора через colorchooser
    app.set_tool(p.Tool.LINE)
    app.on_press(FakeEvent(60, 80))
    app.on_drag(FakeEvent(220, 80))
    app.on_release(FakeEvent(220, 80))
    capture("custom-color-result", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# порядок наложения
# ---------------------------------------------------------------------------

def _three_overlapping_shapes(app: "p.PaintApp"):
    rect_id = app.canvas.create_rectangle(40, 40, 160, 140, fill="#dc2626", outline="")
    oval_id = app.canvas.create_oval(100, 70, 220, 170, fill="#2563eb", outline="")
    line_id = app.canvas.create_line(20, 160, 240, 60, fill="#111827", width=6)
    return rect_id, oval_id, line_id


def stacking_order_before() -> None:
    root, app = new_app()
    _three_overlapping_shapes(app)
    capture("stacking-order-before", root, grab_w=1175, grab_h=560)


def stacking_order_after() -> None:
    root, app = new_app()
    rect_id, _oval_id, _line_id = _three_overlapping_shapes(app)
    app.canvas.tag_raise(rect_id)
    capture("stacking-order-after", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# ластик
# ---------------------------------------------------------------------------

def _drawing_for_eraser(app: "p.PaintApp") -> None:
    app.set_tool(p.Tool.RECTANGLE)
    app.on_press(FakeEvent(40, 40))
    app.on_drag(FakeEvent(240, 160))
    app.on_release(FakeEvent(240, 160))
    app.set_tool(p.Tool.LINE)
    app.on_press(FakeEvent(40, 100))
    app.on_drag(FakeEvent(240, 100))
    app.on_release(FakeEvent(240, 100))


def eraser_before() -> None:
    root, app = new_app()
    _drawing_for_eraser(app)
    capture("eraser-before", root, grab_w=1175, grab_h=560)


def eraser_after() -> None:
    root, app = new_app()
    _drawing_for_eraser(app)
    app.set_tool(p.Tool.ERASER)
    app.on_press(FakeEvent(80, 90))
    for x in range(80, 200, 10):
        app.on_drag(FakeEvent(x, 100))
    app.on_release(FakeEvent(200, 100))
    capture("eraser-after", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# undo / redo
# ---------------------------------------------------------------------------

def _drawing_for_undo(app: "p.PaintApp") -> None:
    app.set_tool(p.Tool.OVAL)
    app.set_color("#16a34a")
    app.on_press(FakeEvent(40, 40))
    app.on_drag(FakeEvent(140, 120))
    app.on_release(FakeEvent(140, 120))
    app.set_tool(p.Tool.RECTANGLE)
    app.set_color("#dc2626")
    app.on_press(FakeEvent(180, 50))
    app.on_drag(FakeEvent(280, 140))
    app.on_release(FakeEvent(280, 140))


def undo_before() -> None:
    root, app = new_app()
    _drawing_for_undo(app)
    capture("undo-before", root, grab_w=1175, grab_h=560)


def undo_after() -> None:
    root, app = new_app()
    _drawing_for_undo(app)
    app.undo()
    capture("undo-after", root, grab_w=1175, grab_h=560)


def redo_after() -> None:
    root, app = new_app()
    _drawing_for_undo(app)
    app.undo()
    app.redo()
    capture("redo-after", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# строка состояния
# ---------------------------------------------------------------------------

def status_bar() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.PENCIL)
    app.set_color("#2563eb")
    app.width_scale.set(5)
    app._update_status(314, 208)
    capture("status-bar", root, grab_w=1175, grab_h=560)


# ---------------------------------------------------------------------------
# сохранение / загрузка
# ---------------------------------------------------------------------------

def saved_document() -> None:
    root, app = new_app()
    _drawing_for_undo(app)
    tmp_path = OUT_DIR.parent / "_tmp_saved_document.json"
    app._write_document(tmp_path)
    capture("saved-document", root, grab_w=1175, grab_h=560)
    tmp_path.unlink(missing_ok=True)


def loaded_document() -> None:
    root1, app1 = new_app()
    _drawing_for_undo(app1)
    tmp_path = OUT_DIR.parent / "_tmp_loaded_document.json"
    app1._write_document(tmp_path)
    app1.root.destroy()

    root2, app2 = new_app()
    app2.load_from_path(tmp_path)
    capture("loaded-document", root2, grab_w=1175, grab_h=560)
    tmp_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# изменение размера окна
# ---------------------------------------------------------------------------

def resized_window() -> None:
    root, app = new_app()
    app.set_tool(p.Tool.RECTANGLE)
    app.on_press(FakeEvent(40, 40))
    app.on_drag(FakeEvent(140, 110))
    app.on_release(FakeEvent(140, 110))
    root.geometry("1200x650+0+0")
    root.update_idletasks()
    root.update()
    app.render_document()  # переасинхронное обновление цвета после resize (см. главу 17)
    capture("resized-window", root, grab_w=1230, grab_h=700)


if __name__ == "__main__":
    paint_pro_final()
    empty_canvas()
    toolbar_tools()
    color_palette()
    rectangle_final_basic()
    oval_final_basic()
    multiple_shapes()
    freehand_naive_dots()
    canvas_coordinate_demo()
    tool_pencil_selected()
    tool_line_selected()
    mouse_press_start()
    mouse_drag_preview_line()
    line_final()
    rectangle_preview()
    oval_preview()
    freehand_connected_stroke()
    width_comparison()
    custom_color_result()
    stacking_order_before()
    stacking_order_after()
    eraser_before()
    eraser_after()
    undo_before()
    undo_after()
    redo_after()
    status_bar()
    saved_document()
    loaded_document()
    resized_window()
