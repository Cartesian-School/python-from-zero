"""Приложение для рисования на Tkinter.

Проект к главе 18 книги «Python с нуля» (Cartesian School).
Запуск: python paint_app.py
"""

import tkinter as tk

root = tk.Tk()
root.title("Рисовалка")

# --- переменные состояния рисования ---
tekuschaya_figura = "linia"     # "linia", "pryamougolnik", "oval", "svobodno"
tekuschij_cvet = "black"
tolschina = 3
start_x = None
start_y = None
vremennaya_figura = None


def vybrat_figuru(figura):
    global tekuschaya_figura
    tekuschaya_figura = figura
    status_label.config(text=f"Инструмент: {figura}")


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
        vremennaya_figura = canvas.create_line(
            start_x, start_y, event.x, event.y, fill=tekuschij_cvet, width=tolschina
        )
    elif tekuschaya_figura == "pryamougolnik":
        vremennaya_figura = canvas.create_rectangle(
            start_x, start_y, event.x, event.y, outline=tekuschij_cvet, width=tolschina
        )
    elif tekuschaya_figura == "oval":
        vremennaya_figura = canvas.create_oval(
            start_x, start_y, event.x, event.y, outline=tekuschij_cvet, width=tolschina
        )


def konec_risovaniya(event):
    global vremennaya_figura
    vremennaya_figura = None


def ochistit_holst():
    canvas.delete("all")


# --- позиция мыши в строке состояния ---
def pokazat_poziciyu(event):
    pozicia_label.config(text=f"x={event.x}, y={event.y}")


# --- строим интерфейс ---
toolbar = tk.Frame(root)
toolbar.pack(side="top", fill="x")

tk.Button(toolbar, text="Линия", command=lambda: vybrat_figuru("linia")).pack(side="left")
tk.Button(toolbar, text="Прямоугольник", command=lambda: vybrat_figuru("pryamougolnik")).pack(side="left")
tk.Button(toolbar, text="Овал", command=lambda: vybrat_figuru("oval")).pack(side="left")
tk.Button(toolbar, text="Свободно", command=lambda: vybrat_figuru("svobodno")).pack(side="left")
tk.Button(toolbar, text="Очистить", command=ochistit_holst).pack(side="left")

cveta = ["black", "red", "blue", "green", "orange", "purple"]
for cvet in cveta:
    tk.Button(toolbar, bg=cvet, width=2, command=lambda c=cvet: vybrat_cvet(c)).pack(side="left")

tk.Label(toolbar, text="Толщина:").pack(side="left", padx=(10, 0))
tolschina_scale = tk.Scale(toolbar, from_=1, to=10, orient="horizontal", command=vybrat_tolschinu)
tolschina_scale.set(3)
tolschina_scale.pack(side="left")

status_label = tk.Label(root, text="Инструмент: linia")
status_label.pack(side="top", anchor="w")

pozicia_label = tk.Label(root, text="x=0, y=0")
pozicia_label.pack(side="bottom", anchor="w")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

canvas.bind("<Button-1>", nachalo_risovaniya)
canvas.bind("<B1-Motion>", vo_vremya_risovaniya)
canvas.bind("<ButtonRelease-1>", konec_risovaniya)
canvas.bind("<Motion>", pokazat_poziciyu)


if __name__ == "__main__":
    root.mainloop()
