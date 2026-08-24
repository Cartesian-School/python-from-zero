"""Мини-проект «Преобразование температуры» на Tkinter.

Домашняя практика к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python temperature_converter.py

Импорт этого файла не открывает окно: tk.Tk() создаётся только внутри
main(). preobrazovat() — чистая функция без Tkinter: она отклоняет значения
ниже абсолютного нуля, поэтому её можно проверять тестами без дисплея.
"""

from __future__ import annotations

import tkinter as tk

ABSOLYUTNYJ_NOL_C = -273.15


def celsij_v_farengejt(c: float) -> float:
    return c * 9 / 5 + 32


def celsij_v_kelvin(c: float) -> float:
    return c + 273.15


def farengejt_v_celsij(f: float) -> float:
    return (f - 32) * 5 / 9


def kelvin_v_celsij(k: float) -> float:
    return k - 273.15


def preobrazovat(znachenie: float, iz_edinicy: str) -> dict[str, float]:
    """Переводит значение в градусы Цельсия, Фаренгейта и Кельвина.

    iz_edinicy — одна из "C", "F", "K": единица, в которой дано исходное значение.
    Возвращает словарь {"C": ..., "F": ..., "K": ...}.
    Вызывает ValueError, если значение ниже абсолютного нуля (-273.15°C,
    -459.67°F, 0 K) — такой температуры не существует."""
    if iz_edinicy == "C":
        c = znachenie
    elif iz_edinicy == "F":
        c = farengejt_v_celsij(znachenie)
    elif iz_edinicy == "K":
        c = kelvin_v_celsij(znachenie)
    else:
        raise ValueError(f"неизвестная единица измерения: {iz_edinicy!r}")

    if c < ABSOLYUTNYJ_NOL_C:
        raise ValueError("температура ниже абсолютного нуля")

    return {
        "C": c,
        "F": celsij_v_farengejt(c),
        "K": celsij_v_kelvin(c),
    }


def main() -> None:
    root = tk.Tk()
    root.title("Преобразование температуры")

    edinica = tk.StringVar(value="C")
    rezultat_text = tk.StringVar(value="")

    def na_preobrazovat_nazhali() -> None:
        tekst = pole_vvoda.get().strip().replace(",", ".")
        try:
            znachenie = float(tekst)
        except ValueError:
            rezultat_text.set("Введите число")
            return

        try:
            rezultaty = preobrazovat(znachenie, edinica.get())
        except ValueError:
            rezultat_text.set("Такой температуры не существует — ниже абсолютного нуля")
            return

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

    root.mainloop()


if __name__ == "__main__":
    main()
