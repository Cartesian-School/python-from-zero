"""Мини-проект «Заметки»: знакомство с файлами и Tkinter.

Проект к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python notes_app.py
"""

import tkinter as tk
from pathlib import Path

FAJL_ZAMETOK = Path(__file__).parent / "zametka.txt"

root = tk.Tk()
root.title("Заметки")

status_text = tk.StringVar(value="")

polye_teksta = tk.Text(root, width=50, height=15)
polye_teksta.pack(padx=8, pady=8)


def sohranit_zametku():
    tekst = polye_teksta.get("1.0", "end-1c")
    FAJL_ZAMETOK.write_text(tekst, encoding="utf-8")
    status_text.set(f"Сохранено в {FAJL_ZAMETOK.name}")


def zagruzit_zametku():
    if not FAJL_ZAMETOK.exists():
        status_text.set("Файл заметки ещё не создан — сначала сохраните.")
        return
    tekst = FAJL_ZAMETOK.read_text(encoding="utf-8")
    polye_teksta.delete("1.0", "end")
    polye_teksta.insert("1.0", tekst)
    status_text.set(f"Загружено из {FAJL_ZAMETOK.name}")


def ochistit_polye():
    polye_teksta.delete("1.0", "end")
    status_text.set("Поле очищено (файл не тронут)")


knopki = tk.Frame(root)
knopki.pack(pady=4)
tk.Button(knopki, text="Сохранить", command=sohranit_zametku).pack(side="left", padx=4)
tk.Button(knopki, text="Загрузить", command=zagruzit_zametku).pack(side="left", padx=4)
tk.Button(knopki, text="Очистить поле", command=ochistit_polye).pack(side="left", padx=4)

tk.Label(root, textvariable=status_text, fg="gray").pack(pady=4)


if __name__ == "__main__":
    root.mainloop()
