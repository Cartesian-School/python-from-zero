"""Игра «Крестики-нолики» на Tkinter — первый рабочий прототип (раздел 17.6).

Состояние игры живёт в глобальных переменных, а текст кнопок одновременно
служит и отображением, и хранилищем состояния поля — сознательный выбор для
самой первой версии (см. раздел 17.13). Финальная архитектура с отдельной
GameState — в tic_tac_toe.py.

Запуск: python tic_tac_toe_basic.py
"""

import tkinter as tk

root = tk.Tk()
root.title("Крестики-нолики")

# --- глобальные переменные состояния игры ---
tekuschij_igrok = "X"
polya = []  # список из 9 кнопок, по порядку слева направо, сверху вниз
igra_okonchena = False


def proverit_pobedu():
    """Возвращает 'X', 'O' или None, если победителя пока нет."""
    linii_pobedy = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # строки
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # столбцы
        (0, 4, 8), (2, 4, 6),             # диагонали
    ]
    for a, b, c in linii_pobedy:
        znacheniya = (polya[a]["text"], polya[b]["text"], polya[c]["text"])
        if znacheniya[0] != "" and znacheniya[0] == znacheniya[1] == znacheniya[2]:
            return znacheniya[0]
    return None


def polye_zapolneno():
    return all(knopka["text"] != "" for knopka in polya)


def na_knopku_nazhali(indeks):
    global tekuschij_igrok, igra_okonchena

    if igra_okonchena or polya[indeks]["text"] != "":
        return  # клетка уже занята или игра уже закончена

    polya[indeks]["text"] = tekuschij_igrok

    pobeditel = proverit_pobedu()
    if pobeditel:
        status_label.config(text=f"Победил игрок {pobeditel}!")
        igra_okonchena = True
        return

    if polye_zapolneno():
        status_label.config(text="Ничья!")
        igra_okonchena = True
        return

    tekuschij_igrok = "O" if tekuschij_igrok == "X" else "X"
    status_label.config(text=f"Ход игрока: {tekuschij_igrok}")


def novaya_igra():
    global tekuschij_igrok, igra_okonchena
    tekuschij_igrok = "X"
    igra_okonchena = False
    for knopka in polya:
        knopka.config(text="")
    status_label.config(text=f"Ход игрока: {tekuschij_igrok}")


status_label = tk.Label(root, text=f"Ход игрока: {tekuschij_igrok}", font=("Arial", 14))
status_label.grid(row=0, column=0, columnspan=3, pady=10)

pole_frame = tk.Frame(root)
pole_frame.grid(row=1, column=0, columnspan=3)

for indeks in range(9):
    knopka = tk.Button(
        pole_frame,
        text="",
        font=("Arial", 24, "bold"),
        width=3,
        height=1,
        command=lambda i=indeks: na_knopku_nazhali(i),
    )
    knopka.grid(row=indeks // 3, column=indeks % 3)
    polya.append(knopka)

novaya_igra_button = tk.Button(root, text="Новая игра", command=novaya_igra)
novaya_igra_button.grid(row=2, column=0, columnspan=3, pady=10)


if __name__ == "__main__":
    root.mainloop()
