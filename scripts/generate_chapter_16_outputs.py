#!/usr/bin/env python3
"""Генерирует настоящие скриншоты Tkinter-окон для главы 16.

Требует headless X-сервер (xvfb-run) — сами окна реальны, не имитация HTML/CSS.
Использование: xvfb-run -a python3 scripts/generate_chapter_16_outputs.py

Меню (tk.Menu) — единственное подтверждённое исключение: строка меню не
отображается в headless Xvfb без оконного менеджера (проверено), поэтому её
схематическое изображение строится отдельно как HTML/CSS в build_chapter_16.py,
явно подписанное «Схематическое изображение» — а не сгенерировано этим скриптом.
"""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageChops, ImageGrab

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-16" / "output"


def _autocrop(img: Image.Image) -> Image.Image:
    """Crops away the black margin ImageGrab captures outside any real X
    window — lets every capture() call grab a generously large area without
    having to precompute an exact popup/secondary-window bounding box."""
    rgb = img.convert("RGB")
    bg = Image.new("RGB", rgb.size, (0, 0, 0))
    bbox = ImageChops.difference(rgb, bg).getbbox()
    return img.crop(bbox) if bbox else img


def capture(name: str, *, grab_w: int = 900, grab_h: int = 700, root: tk.Tk | None = None) -> None:
    if root is not None:
        root.update_idletasks()
        root.update()
    img = ImageGrab.grab(bbox=(0, 0, grab_w, grab_h))
    img = _autocrop(img)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    img.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({img.size[0]}x{img.size[1]})")
    if root is not None:
        root.destroy()


def label_button() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    label = tk.Label(root, text="Привет, Tkinter!")
    label.pack(pady=10)
    button = tk.Button(root, text="Нажми меня")
    button.pack(pady=10)
    capture("label-button", root=root)


def button_states() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    ttk.Button(root, text="Обычная кнопка").pack(padx=16, pady=8)
    disabled = ttk.Button(root, text="Недоступна", state="disabled")
    disabled.pack(padx=16, pady=8)
    capture("button-states", root=root)


def entry_vs_text() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    outer = ttk.Frame(root, padding=14)
    outer.pack()
    left = ttk.Frame(outer)
    left.grid(row=0, column=0, padx=10)
    ttk.Label(left, text="Entry — одна строка").pack()
    entry = ttk.Entry(left)
    entry.insert(0, "Cartesian")
    entry.pack()
    right = ttk.Frame(outer)
    right.grid(row=0, column=1, padx=10)
    ttk.Label(right, text="Text — несколько строк").pack()
    text = tk.Text(right, height=4, width=16, wrap="none")
    text.insert("1.0", "Первая\nВторая\nТретья")
    text.pack()
    capture("entry-vs-text", root=root)


def frame_labelframe() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    toolbar = ttk.Frame(root, padding=6)
    toolbar.pack(fill="x")
    ttk.Button(toolbar, text="Открыть").pack(side="left", padx=4)
    ttk.Button(toolbar, text="Сохранить").pack(side="left", padx=4)
    settings = ttk.LabelFrame(root, text="Настройки", padding=10)
    settings.pack(fill="x", padx=10, pady=10)
    ttk.Checkbutton(settings, text="Тёмная тема").pack(anchor="w")
    ttk.Checkbutton(settings, text="Автосохранение").pack(anchor="w")
    capture("frame-labelframe", root=root)


def checkbutton_states() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    v_off = tk.BooleanVar(value=False)
    v_on = tk.BooleanVar(value=True)
    ttk.Checkbutton(root, text="С сахаром (снят)", variable=v_off).pack(anchor="w", padx=14, pady=6)
    ttk.Checkbutton(root, text="С сахаром (установлен)", variable=v_on).pack(anchor="w", padx=14, pady=6)
    capture("checkbutton-states", root=root)


def radiobutton_group() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    vybor = tk.StringVar(value="kofe")
    ttk.Radiobutton(root, text="Чай", variable=vybor, value="chay").pack(anchor="w", padx=14, pady=4)
    ttk.Radiobutton(root, text="Кофе", variable=vybor, value="kofe").pack(anchor="w", padx=14, pady=4)
    ttk.Radiobutton(root, text="Вода", variable=vybor, value="voda").pack(anchor="w", padx=14, pady=4)
    capture("radiobutton-group", root=root)


def combobox_closed() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    combo = ttk.Combobox(root, values=["Маленький", "Средний", "Большой"], state="readonly")
    combo.current(0)
    combo.pack(padx=20, pady=20)
    capture("combobox-closed", root=root)


def combobox_open() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    combo = ttk.Combobox(root, values=["Маленький", "Средний", "Большой"], state="readonly")
    combo.current(0)
    combo.pack(padx=20, pady=20)
    root.update()
    combo.event_generate("<Button-1>")
    combo.event_generate("<ButtonRelease-1>")
    capture("combobox-open", root=root, grab_h=300)


def listbox_selection() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    spisok = tk.Listbox(root, height=4)
    for item in ("Молоко", "Хлеб", "Яблоки", "Сыр"):
        spisok.insert("end", item)
    spisok.pack(padx=20, pady=20)
    spisok.selection_set(1)
    capture("listbox-selection", root=root)


def spinbox_widget() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    ttk.Label(root, text="Количество:").pack(padx=14, pady=(14, 2))
    spin = ttk.Spinbox(root, from_=1, to=10)
    spin.set(3)
    spin.pack(padx=14, pady=(0, 14))
    capture("spinbox", root=root)


def scale_widget() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    value_var = tk.StringVar(value="50")
    row = ttk.Frame(root, padding=14)
    row.pack()
    scale = ttk.Scale(row, from_=0, to=100, orient="horizontal", length=160,
                       command=lambda v: value_var.set(str(round(float(v)))))
    scale.set(50)
    scale.pack(side="left")
    ttk.Label(row, textvariable=value_var).pack(side="left", padx=10)
    capture("scale", root=root)


def progressbar_states() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    ttk.Style().configure("TProgressbar", thickness=16)
    frame = ttk.Frame(root, padding=14)
    frame.pack()
    for pct in (0, 35, 70, 100):
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=f"{pct}%", width=5).pack(side="left")
        bar = ttk.Progressbar(row, mode="determinate", maximum=100, value=pct, length=160)
        bar.pack(side="left")
    capture("progressbar-states", root=root)


def notebook_tabs() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    notebook = ttk.Notebook(root, width=220, height=100)
    notebook.pack(padx=10, pady=10)
    general_tab = ttk.Frame(notebook)
    appearance_tab = ttk.Frame(notebook)
    files_tab = ttk.Frame(notebook)
    ttk.Checkbutton(general_tab, text="Автосохранение").pack(padx=10, pady=10, anchor="w")
    ttk.Checkbutton(appearance_tab, text="Тёмная тема").pack(padx=10, pady=10, anchor="w")
    ttk.Label(files_tab, text="Папка по умолчанию: ~/Documents").pack(padx=10, pady=10, anchor="w")
    notebook.add(general_tab, text="Общие")
    notebook.add(appearance_tab, text="Внешний вид")
    notebook.add(files_tab, text="Файлы")
    notebook.select(general_tab)
    capture("notebook-tabs", root=root)


def toplevel_windows() -> None:
    root = tk.Tk()
    root.title("Приложение")
    root.geometry("220x140+0+0")
    ttk.Label(root, text="Главное окно").pack(padx=20, pady=45)

    settings = tk.Toplevel(root)
    settings.title("Настройки")
    settings.geometry("220x140+260+0")
    ttk.Label(settings, text="Окно настроек\n(Toplevel)").pack(padx=20, pady=40)

    capture("toplevel-windows", grab_w=500, grab_h=160, root=root)


def canvas_basics() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    canvas = tk.Canvas(root, width=260, height=170, background="white")
    canvas.pack(padx=10, pady=10)
    canvas.create_line(10, 10, 240, 10, fill="#5B24F9", width=2)
    canvas.create_rectangle(10, 30, 90, 90, outline="#DB2777", width=2)
    canvas.create_oval(130, 30, 210, 90, outline="#059669", width=2)
    canvas.create_text(130, 130, text="(0,0) — верхний левый угол", font=("Arial", 9))
    capture("canvas-basics", root=root)


def photoimage_widget() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    size = 48
    image = tk.PhotoImage(width=size, height=size)
    for yy in range(size):
        for xx in range(size):
            color = "#5B24F9" if (xx // 6 + yy // 6) % 2 == 0 else "#E7DEFF"
            image.put(color, (xx, yy))
    label = ttk.Label(root, image=image)
    label.image = image  # keep a reference alive for the widget's lifetime
    label.pack(padx=20, pady=20)
    capture("photoimage", root=root)


def style_default_vs_custom() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    style = ttk.Style()
    style.configure("Accent.TButton", font=("TkDefaultFont", 11, "bold"), padding=8)
    row = ttk.Frame(root, padding=14)
    row.pack()
    ttk.Button(row, text="Обычная кнопка").pack(side="left", padx=8)
    ttk.Button(row, text="Сохранить", style="Accent.TButton").pack(side="left", padx=8)
    capture("style-default-vs-custom", root=root)


def tk_vs_ttk() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    outer = ttk.Frame(root, padding=14)
    outer.pack()
    left = ttk.LabelFrame(outer, text="tk (классический)")
    left.grid(row=0, column=0, padx=10, sticky="n")
    tk.Label(left, text="tk.Label").pack(padx=10, pady=4)
    tk.Entry(left).pack(padx=10, pady=4)
    tk.Button(left, text="tk.Button").pack(padx=10, pady=4)
    right = ttk.LabelFrame(outer, text="ttk (тематизированный)")
    right.grid(row=0, column=1, padx=10, sticky="n")
    ttk.Label(right, text="ttk.Label").pack(padx=10, pady=4)
    ttk.Entry(right).pack(padx=10, pady=4)
    ttk.Button(right, text="ttk.Button").pack(padx=10, pady=4)
    capture("tk-vs-ttk", root=root)


def tip_calculator_pro() -> None:
    root = tk.Tk()
    root.geometry("+0+0")

    frame = ttk.Frame(root, padding=12)
    frame.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)

    ttk.Label(frame, text="Сумма счёта:").grid(row=0, column=0, sticky="w")
    amount_entry = ttk.Entry(frame)
    amount_entry.insert(0, "1000")
    amount_entry.grid(row=0, column=1, sticky="ew")

    ttk.Label(frame, text="Процент чаевых:").grid(row=1, column=0, sticky="w")
    percent_combo = ttk.Combobox(frame, values=["10", "15", "20"], state="readonly")
    percent_combo.set("15")
    percent_combo.grid(row=1, column=1, sticky="ew")

    ttk.Label(frame, text="Количество человек:").grid(row=2, column=0, sticky="w")
    people_entry = ttk.Entry(frame)
    people_entry.insert(0, "2")
    people_entry.grid(row=2, column=1, sticky="ew")

    ttk.Button(frame, text="Посчитать").grid(row=3, column=0, columnspan=2, pady=8)
    ttk.Label(frame, text="Чаевые с человека: 75.00").grid(row=4, column=0, columnspan=2)
    frame.columnconfigure(1, weight=1)

    capture("tip-calculator-pro", root=root)


def temperature_converter() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    frame = ttk.Frame(root, padding=14)
    frame.pack()
    ttk.Label(frame, text="Температура в °C:").grid(row=0, column=0, sticky="w")
    celsius_entry = ttk.Entry(frame)
    celsius_entry.insert(0, "-40")
    celsius_entry.grid(row=0, column=1, sticky="ew", padx=6)
    ttk.Button(frame, text="В Фаренгейты").grid(row=1, column=0, columnspan=2, pady=8)
    ttk.Label(frame, text="Результат: -40.0 °F").grid(row=2, column=0, columnspan=2)
    capture("temperature-converter", root=root)


def timer_widget() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    frame = ttk.Frame(root, padding=14)
    frame.pack()
    ttk.Label(frame, text="00:42", font=("Arial", 22)).pack(pady=6)
    controls = ttk.Frame(frame)
    controls.pack()
    ttk.Button(controls, text="Старт").pack(side="left", padx=4)
    ttk.Button(controls, text="Стоп").pack(side="left", padx=4)
    ttk.Button(controls, text="Сброс").pack(side="left", padx=4)
    capture("timer-widget", root=root)


def todo_list() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    frame = ttk.Frame(root, padding=14)
    frame.pack()
    listbox = tk.Listbox(frame, height=4, width=26)
    for task in ("Купить молоко", "Позвонить", "Сделать практику 16-29"):
        listbox.insert("end", task)
    listbox.selection_set(1)
    listbox.pack()
    controls = ttk.Frame(frame)
    controls.pack(fill="x", pady=6)
    entry = ttk.Entry(controls)
    entry.pack(side="left", fill="x", expand=True)
    ttk.Button(controls, text="+").pack(side="left", padx=4)
    ttk.Button(controls, text="−").pack(side="left")
    capture("todo-list", root=root)


def notes_editor() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    root.title("Редактор заметок — zametki_glavy_16.txt")
    text = tk.Text(root, height=6, width=34, wrap="word")
    text.insert("1.0", "Заметка о главе 16.\n\nTkinter — событийная модель, виджеты, макеты.")
    text.pack(padx=8, pady=8)
    capture("notes-editor", root=root)


def click_counter() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    schet = tk.IntVar(value=3)
    ttk.Label(root, textvariable=schet, font=("Arial", 24)).pack(pady=14)
    ttk.Button(root, text="+1").pack(pady=(0, 14))
    capture("click-counter", root=root)


def grid_resize_comparison() -> None:
    def build_form(root_w: ttk.Frame, weighted: bool) -> None:
        ttk.Label(root_w, text="Имя:").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(root_w)
        entry.grid(row=0, column=1, sticky="ew")
        if weighted:
            root_w.columnconfigure(1, weight=1)

    root = tk.Tk()
    root.geometry("+0+0")
    outer = ttk.Frame(root, padding=10)
    outer.pack()

    left = ttk.LabelFrame(outer, text="Без weight — окно 340px")
    left.grid(row=0, column=0, padx=8, sticky="n")
    left_inner = ttk.Frame(left, width=300)
    left_inner.pack()
    left_inner.pack_propagate(False)
    build_form(left_inner, weighted=False)

    right = ttk.LabelFrame(outer, text="column weight=1, sticky=ew — окно 340px")
    right.grid(row=0, column=1, padx=8, sticky="n")
    right_inner = ttk.Frame(right, width=300)
    right_inner.pack()
    right_inner.pack_propagate(False)
    build_form(right_inner, weighted=True)

    capture("grid-resize-comparison", root=root)


def widget_gallery() -> None:
    root = tk.Tk()
    root.geometry("+0+0")
    ttk.Style().configure("TProgressbar", thickness=16)
    outer = ttk.Frame(root, padding=12)
    outer.pack()

    row0 = ttk.Frame(outer)
    row0.pack(fill="x", pady=4)
    ttk.Label(row0, text="Label").pack(side="left", padx=6)
    ttk.Entry(row0, width=10).pack(side="left", padx=6)
    ttk.Button(row0, text="Button").pack(side="left", padx=6)

    row1 = ttk.Frame(outer)
    row1.pack(fill="x", pady=4)
    ttk.Checkbutton(row1, text="Checkbutton").pack(side="left", padx=6)
    ttk.Radiobutton(row1, text="Radiobutton", value=1).pack(side="left", padx=6)

    row2 = ttk.Frame(outer)
    row2.pack(fill="x", pady=4)
    combo = ttk.Combobox(row2, values=["Combobox"], width=10, state="readonly")
    combo.current(0)
    combo.pack(side="left", padx=6)
    ttk.Spinbox(row2, from_=1, to=5, width=6).pack(side="left", padx=6)
    ttk.Scale(row2, from_=0, to=100, length=80).pack(side="left", padx=6)

    row3 = ttk.Frame(outer)
    row3.pack(fill="x", pady=4)
    ttk.Progressbar(row3, value=60, length=140).pack(side="left", padx=6)

    row4 = ttk.Frame(outer)
    row4.pack(fill="x", pady=4)
    nb = ttk.Notebook(row4, width=200, height=60)
    tab = ttk.Frame(nb)
    nb.add(tab, text="Вкладка")
    nb.pack(side="left", padx=6)

    capture("widget-gallery", root=root)


if __name__ == "__main__":
    click_counter()
    grid_resize_comparison()
    label_button()
    button_states()
    entry_vs_text()
    frame_labelframe()
    checkbutton_states()
    radiobutton_group()
    combobox_closed()
    combobox_open()
    listbox_selection()
    spinbox_widget()
    scale_widget()
    progressbar_states()
    notebook_tabs()
    toplevel_windows()
    canvas_basics()
    photoimage_widget()
    style_default_vs_custom()
    tk_vs_ttk()
    tip_calculator_pro()
    temperature_converter()
    timer_widget()
    todo_list()
    notes_editor()
    widget_gallery()
