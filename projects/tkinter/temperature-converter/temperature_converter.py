"""Мини-проект «Преобразование температуры» на Tkinter.

Проект к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python temperature_converter.py
"""

import tkinter as tk

root = tk.Tk()
root.title("Преобразование температуры")

edinica = tk.StringVar(value="C")
rezultat_text = tk.StringVar(value="")


def celsij_v_farengejt(c):
    return c * 9 / 5 + 32


def celsij_v_kelvin(c):
    return c + 273.15


def farengejt_v_celsij(f):
    return (f - 32) * 5 / 9


def kelvin_v_celsij(k):
    return k - 273.15


def preobrazovat(znachenie, iz_edinicy):
    """Переводит значение в градусы Цельсия, Фаренгейта и Кельвина.

    iz_edinicy — одна из "C", "F", "K": единица, в которой дано исходное значение.
    Возвращает словарь {"C": ..., "F": ..., "K": ...}.
    """
    if iz_edinicy == "C":
        c = znachenie
    elif iz_edinicy == "F":
        c = farengejt_v_celsij(znachenie)
    else:
        c = kelvin_v_celsij(znachenie)

    return {
        "C": c,
        "F": celsij_v_farengejt(c),
        "K": celsij_v_kelvin(c),
    }


def na_preobrazovat_nazhali():
    tekst = pole_vvoda.get().strip().replace(",", ".")
    try:
        znachenie = float(tekst)
    except ValueError:
        rezultat_text.set("Введите число")
        return

    rezultaty = preobrazovat(znachenie, edinica.get())
    rezultat_text.set(
        f"{rezultaty['C']:.1f}°C = {rezultaty['F']:.1f}°F = {rezultaty['K']:.1f}K"
    )


tk.Label(root, text="Введите температуру:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
pole_vvoda = tk.Entry(root)
pole_vvoda.grid(row=0, column=1, padx=8, pady=4)

for i, (kod, podpis) in enumerate([("C", "Цельсий"), ("F", "Фаренгейт"), ("K", "Кельвин")]):
    tk.Radiobutton(root, text=podpis, variable=edinica, value=kod).grid(row=1, column=i, sticky="w")

tk.Button(root, text="Преобразовать", command=na_preobrazovat_nazhali).grid(row=2, column=0, columnspan=3, pady=8)
tk.Label(root, textvariable=rezultat_text, font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=3, pady=4)


if __name__ == "__main__":
    root.mainloop()
