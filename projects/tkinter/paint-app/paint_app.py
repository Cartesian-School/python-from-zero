"""Приложение для рисования на Tkinter — финальная версия (глава 18).

Перестройка прототипа из paint_app_basic.py: параметры инструмента живут в
DrawingState, нарисованные фигуры — в документе (списке Shape), Canvas
только отображает документ через render_document(). Undo/redo работают по
действиям (один карандашный штрих — одно действие, даже если состоит из
многих отрезков), а не по отдельным элементам Canvas. Сохранение — в JSON,
без глобальных переменных: вся логика — методы класса PaintApp.

Запуск: python paint_app.py
"""

import json
import tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox, ttk


class Tool(Enum):
    PENCIL = "pencil"
    LINE = "line"
    RECTANGLE = "rectangle"
    OVAL = "oval"
    ERASER = "eraser"


TOOL_LABELS = {
    Tool.PENCIL: "Карандаш",
    Tool.LINE: "Линия",
    Tool.RECTANGLE: "Прямоугольник",
    Tool.OVAL: "Овал",
    Tool.ERASER: "Ластик",
}

# (имя, hex) — имя нужно и для подписи текущего цвета, и для доступности:
# состояние инструмента не должно опираться только на цвет (раздел 18.32).
PALETTE = [
    ("Чёрный", "#111827"),
    ("Красный", "#dc2626"),
    ("Синий", "#2563eb"),
    ("Зелёный", "#16a34a"),
    ("Оранжевый", "#f59e0b"),
    ("Фиолетовый", "#7c3aed"),
]

CANVAS_BG = "#ffffff"
MIN_DRAG = 2  # px — короче считаем «кликом без перетаскивания», раздел 18.7
DOCUMENT_VERSION = 1


def normalize_bounds(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float, float, float]:
    """Приводит две произвольные противоположные точки перетаскивания к
    (left, top, right, bottom) — не зависит от того, в какую сторону мышь
    тянули: вниз-вправо, вверх-влево и так далее (раздел 18.16)."""
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)


@dataclass
class Shape:
    """Одна логическая фигура документа — то, что рисуется на Canvas и то,
    что сохраняется в JSON. Ничего не знает о Tkinter."""

    kind: str  # "line" | "rectangle" | "oval"
    coords: list[float]
    color: str
    width: int

    def to_dict(self) -> dict:
        return {"kind": self.kind, "coords": self.coords, "color": self.color, "width": self.width}

    @staticmethod
    def from_dict(data: dict) -> "Shape":
        return Shape(kind=data["kind"], coords=list(data["coords"]), color=data["color"], width=int(data["width"]))


@dataclass
class DrawingState:
    """Только ТЕКУЩИЕ параметры инструмента — не сами нарисованные фигуры
    (раздел 18.13). Фигуры живут в PaintApp.document."""

    tool: Tool = Tool.PENCIL
    color: str = PALETTE[0][1]
    width: int = 4
    start_x: float | None = None
    start_y: float | None = None
    last_x: float | None = None
    last_y: float | None = None
    preview_id: int | None = None
    pending_shapes: list[Shape] = field(default_factory=list)


class PaintApp:
    def __init__(self, root, *, autosave: bool = False):
        self.root = root
        self.root.title("Рисовалка Pro")
        self.state = DrawingState()
        self.document: list[Shape] = []
        self.undo_stack: list[list[Shape]] = []  # каждый элемент — фигуры ОДНОГО действия
        self.redo_stack: list[list[Shape]] = []
        self.autosave = autosave
        self.tool_buttons: dict[Tool, tk.Button] = {}
        self.color_var = tk.StringVar(value=self.state.color)
        self.status_var = tk.StringVar()
        self.build_ui()
        self.set_tool(Tool.PENCIL)
        self._update_status(x=None, y=None)

    # ---------- построение интерфейса ----------
    def build_ui(self):
        outer = ttk.Frame(self.root, padding=8)
        outer.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)  # строка холста растягивается вместе с окном

        self.build_toolbar(outer)

        self.canvas = tk.Canvas(outer, width=640, height=420, bg=CANVAS_BG, cursor="crosshair")
        self.canvas.grid(row=1, column=0, sticky="nsew", pady=(8, 4))
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)

        status = ttk.Label(outer, textvariable=self.status_var, anchor="w", font=("Consolas", 10))
        status.grid(row=2, column=0, sticky="ew", pady=(4, 0))

        self.root.bind("<Control-z>", lambda _e: self.undo())
        self.root.bind("<Control-y>", lambda _e: self.redo())
        self.root.bind("<Control-Shift-Z>", lambda _e: self.redo())
        self.root.bind("<Control-s>", lambda _e: self.save_document())
        self.root.bind("<Control-o>", lambda _e: self.load_document())
        self.root.bind("<Control-n>", lambda _e: self.clear_canvas())

    def build_toolbar(self, outer):
        toolbar = ttk.Frame(outer)
        toolbar.grid(row=0, column=0, sticky="ew")

        tools_frame = ttk.Frame(toolbar)
        tools_frame.pack(side="left")
        for tool in Tool:
            btn = tk.Button(
                tools_frame, text=TOOL_LABELS[tool], relief="raised", width=13,
                command=lambda t=tool: self.set_tool(t),
            )
            btn.pack(side="left", padx=2)
            self.tool_buttons[tool] = btn

        colors_frame = ttk.Frame(toolbar)
        colors_frame.pack(side="left", padx=(14, 0))
        for name, hex_color in PALETTE:
            swatch = tk.Button(
                colors_frame, bg=hex_color, width=2, relief="raised",
                command=lambda c=hex_color: self.set_color(c),
            )
            swatch.pack(side="left", padx=1)
        tk.Button(colors_frame, text="Свой цвет…", command=self.choose_custom_color).pack(side="left", padx=(6, 0))
        tk.Label(colors_frame, textvariable=self.color_var, width=9).pack(side="left", padx=(6, 0))

        width_frame = ttk.Frame(toolbar)
        width_frame.pack(side="left", padx=(14, 0))
        ttk.Label(width_frame, text="Толщина:").pack(side="left")
        self.width_scale = tk.Scale(
            width_frame, from_=1, to=20, orient="horizontal", length=120, command=self.set_width,
        )
        self.width_scale.set(self.state.width)
        self.width_scale.pack(side="left")

        actions_frame = ttk.Frame(toolbar)
        actions_frame.pack(side="right")
        ttk.Button(actions_frame, text="Открыть", command=self.load_document).pack(side="left", padx=2)
        ttk.Button(actions_frame, text="Сохранить", command=self.save_document).pack(side="left", padx=2)
        ttk.Button(actions_frame, text="Очистить", command=self.clear_canvas).pack(side="left", padx=2)
        ttk.Button(actions_frame, text="Отменить (Ctrl+Z)", command=self.undo).pack(side="left", padx=2)
        ttk.Button(actions_frame, text="Повторить (Ctrl+Y)", command=self.redo).pack(side="left", padx=2)

    # ---------- инструмент, цвет, толщина ----------
    def set_tool(self, tool: Tool):
        self.state.tool = tool
        for t, btn in self.tool_buttons.items():
            btn.config(relief="sunken" if t is tool else "raised")
        self._update_status(x=None, y=None)

    def set_color(self, hex_color: str):
        self.state.color = hex_color
        self.color_var.set(hex_color)

    def choose_custom_color(self):
        # askcolor() возвращает (rgb_tuple, hex_string) или (None, None), если
        # пользователь нажал «Отмена» — обязательно проверяем перед использованием.
        _rgb, hex_color = colorchooser.askcolor(color=self.state.color, title="Выберите цвет")
        if hex_color is not None:
            self.set_color(hex_color)

    def set_width(self, value: str):
        self.state.width = int(value)

    # ---------- события мыши: press → drag → release ----------
    def on_press(self, event):
        self.state.start_x, self.state.start_y = event.x, event.y
        self.state.last_x, self.state.last_y = event.x, event.y
        self.state.pending_shapes = []
        if self.state.tool in (Tool.LINE, Tool.RECTANGLE, Tool.OVAL):
            self.state.preview_id = self._create_preview(event.x, event.y, event.x, event.y)

    def on_drag(self, event):
        tool = self.state.tool
        if tool in (Tool.PENCIL, Tool.ERASER):
            color = CANVAS_BG if tool is Tool.ERASER else self.state.color
            self.canvas.create_line(
                self.state.last_x, self.state.last_y, event.x, event.y,
                fill=color, width=self.state.width, capstyle=tk.ROUND, smooth=True,
                tags=("shape", tool.value),
            )
            self.state.pending_shapes.append(
                Shape(kind="line", coords=[self.state.last_x, self.state.last_y, event.x, event.y],
                      color=color, width=self.state.width)
            )
            self.state.last_x, self.state.last_y = event.x, event.y
        elif tool in (Tool.LINE, Tool.RECTANGLE, Tool.OVAL) and self.state.preview_id is not None:
            self.canvas.coords(self.state.preview_id, self.state.start_x, self.state.start_y, event.x, event.y)
        self._update_status(event.x, event.y)

    def on_release(self, event):
        tool = self.state.tool
        if tool in (Tool.PENCIL, Tool.ERASER):
            if self.state.pending_shapes:
                self._commit_action(self.state.pending_shapes)
        elif tool in (Tool.LINE, Tool.RECTANGLE, Tool.OVAL):
            x1, y1 = self.state.start_x, self.state.start_y
            x2, y2 = event.x, event.y
            if self.state.preview_id is not None:
                self.canvas.delete(self.state.preview_id)
                self.state.preview_id = None
            if abs(x2 - x1) >= MIN_DRAG or abs(y2 - y1) >= MIN_DRAG:
                if tool in (Tool.RECTANGLE, Tool.OVAL):
                    # Прямоугольник и овал хранятся в документе с
                    # нормализованными границами — не важно, в какую сторону
                    # тянули мышь (раздел 18.16); линия остаётся "точка A -> точка B".
                    coords = list(normalize_bounds(x1, y1, x2, y2))
                else:
                    coords = [x1, y1, x2, y2]
                shape = Shape(kind=tool.value, coords=coords, color=self.state.color, width=self.state.width)
                self._commit_action([shape])
        self.state.pending_shapes = []
        self.state.start_x = self.state.start_y = None

    def on_motion(self, event):
        self._update_status(event.x, event.y)

    def _create_preview(self, x1, y1, x2, y2) -> int:
        tool = self.state.tool
        common = dict(outline=self.state.color, width=self.state.width, dash=(4, 2), tags=("preview",))
        if tool is Tool.LINE:
            return self.canvas.create_line(x1, y1, x2, y2, fill=self.state.color, width=self.state.width, dash=(4, 2), tags=("preview",))
        if tool is Tool.RECTANGLE:
            return self.canvas.create_rectangle(x1, y1, x2, y2, **common)
        return self.canvas.create_oval(x1, y1, x2, y2, **common)

    # ---------- документ, история, отрисовка ----------
    def _commit_action(self, shapes: list[Shape]):
        self.document.extend(shapes)
        self.undo_stack.append(shapes)
        self.redo_stack.clear()  # новое действие делает старую историю "redo" недействительной
        self.render_document()
        if self.autosave:
            self._maybe_autosave()

    def render_document(self):
        """Единственное место, которое рисует Canvas ИЗ документа — то же
        правило, что и render() в главе 17: модель меняют действия
        пользователя, Canvas только отображает её текущее состояние."""
        self.canvas.delete("shape")
        for shape in self.document:
            self._draw_shape(shape)

    def _draw_shape(self, shape: Shape):
        if shape.kind == "line":
            self.canvas.create_line(
                *shape.coords, fill=shape.color, width=shape.width,
                capstyle=tk.ROUND, smooth=True, tags=("shape", shape.kind),
            )
        elif shape.kind == "rectangle":
            self.canvas.create_rectangle(*shape.coords, outline=shape.color, width=shape.width, tags=("shape", shape.kind))
        elif shape.kind == "oval":
            self.canvas.create_oval(*shape.coords, outline=shape.color, width=shape.width, tags=("shape", shape.kind))

    def undo(self):
        if not self.undo_stack:
            return
        shapes = self.undo_stack.pop()
        del self.document[len(self.document) - len(shapes):]
        self.redo_stack.append(shapes)
        self.render_document()

    def redo(self):
        if not self.redo_stack:
            return
        shapes = self.redo_stack.pop()
        self.document.extend(shapes)
        self.undo_stack.append(shapes)
        self.render_document()

    def clear_canvas(self):
        if self.document and not messagebox.askyesno("Очистить холст", "Удалить весь рисунок без возможности отмены?"):
            return
        self.document.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.render_document()

    # ---------- сохранение и загрузка ----------
    def save_document(self):
        path_str = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Рисунок JSON", "*.json")])
        if not path_str:  # пользователь нажал «Отмена» — path_str == ""
            return
        self._write_document(Path(path_str))

    def _write_document(self, path: Path):
        data = {
            "version": DOCUMENT_VERSION,
            "canvas": {"background": CANVAS_BG},
            "items": [shape.to_dict() for shape in self.document],
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _maybe_autosave(self):
        pass  # переопределяется в тестах при необходимости

    def load_document(self):
        path_str = filedialog.askopenfilename(filetypes=[("Рисунок JSON", "*.json")])
        if not path_str:  # пользователь нажал «Отмена»
            return
        self.load_from_path(Path(path_str))

    def load_from_path(self, path: Path):
        data = json.loads(path.read_text(encoding="utf-8"))
        self.document = [Shape.from_dict(item) for item in data["items"]]
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.render_document()

    # ---------- строка состояния ----------
    def _update_status(self, x, y):
        coords = f"x={x} y={y}" if x is not None else "x=— y=—"
        self.status_var.set(
            f"Инструмент: {TOOL_LABELS[self.state.tool]} | {coords} | "
            f"Цвет: {self.state.color} | Толщина: {self.state.width}"
        )


def main():
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
