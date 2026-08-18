#!/usr/bin/env python3
"""Генерирует настоящие скриншоты Tkinter-окон для главы 16.

Требует headless X-сервер (xvfb-run) — сами окна реальны, не имитация HTML/CSS.
Использование: xvfb-run -a python3 scripts/generate_chapter_16_outputs.py
"""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-16" / "output"


def capture(root: tk.Tk, name: str) -> None:
    root.update_idletasks()
    root.update()
    x, y = root.winfo_rootx(), root.winfo_rooty()
    w, h = root.winfo_width(), root.winfo_height()
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    img.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({img.size[0]}x{img.size[1]})")
    root.destroy()


def label_button() -> None:
    root = tk.Tk()
    root.title("Метки и кнопки")
    root.geometry("300x150")
    label = tk.Label(root, text="Привет, Tkinter!")
    label.pack(pady=10)
    button = tk.Button(root, text="Нажми меня")
    button.pack(pady=10)
    capture(root, "label-button")


def tip_calculator_pro() -> None:
    root = tk.Tk()
    root.title("Tip Calculator Pro")
    root.geometry("360x230")

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

    capture(root, "tip-calculator-pro")


if __name__ == "__main__":
    label_button()
    tip_calculator_pro()
