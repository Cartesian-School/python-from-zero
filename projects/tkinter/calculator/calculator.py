"""Мини-проект «Калькулятор» на Tkinter.

Проект к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python calculator.py
"""

import tkinter as tk

root = tk.Tk()
root.title("Калькулятор")

ekran_text = tk.StringVar(value="0")
tekushee_vyrazhenie = ""


def obnovit_ekran():
    ekran_text.set(tekushee_vyrazhenie if tekushee_vyrazhenie else "0")


def na_cifru_ili_znak_nazhali(simvol):
    global tekushee_vyrazhenie
    tekushee_vyrazhenie += simvol
    obnovit_ekran()


def vychislit_vyrazhenie(vyrazhenie):
    """Безопасно вычисляет арифметическое выражение из цифр и + - * / ( )."""
    dopustimye_simvoly = set("0123456789+-*/(). ")
    if not vyrazhenie or not set(vyrazhenie) <= dopustimye_simvoly:
        return "Ошибка"
    try:
        return str(eval(vyrazhenie, {"__builtins__": {}}, {}))
    except (SyntaxError, ZeroDivisionError, ValueError):
        return "Ошибка"


def na_ravno_nazhali():
    global tekushee_vyrazhenie
    tekushee_vyrazhenie = vychislit_vyrazhenie(tekushee_vyrazhenie)
    obnovit_ekran()


def na_ochistit_nazhali():
    global tekushee_vyrazhenie
    tekushee_vyrazhenie = ""
    obnovit_ekran()


ekran = tk.Label(root, textvariable=ekran_text, font=("Arial", 24), anchor="e", width=12)
ekran.grid(row=0, column=0, columnspan=4, sticky="we", padx=4, pady=8)

KNOPKI = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

for podpis, stroka, stolbec in KNOPKI:
    if podpis == "=":
        knopka = tk.Button(root, text=podpis, command=na_ravno_nazhali)
    else:
        knopka = tk.Button(root, text=podpis, command=lambda s=podpis: na_cifru_ili_znak_nazhali(s))
    knopka.grid(row=stroka, column=stolbec, sticky="we")

knopka_c = tk.Button(root, text="C", command=na_ochistit_nazhali)
knopka_c.grid(row=5, column=0, columnspan=4, sticky="we", pady=4)


if __name__ == "__main__":
    root.mainloop()
