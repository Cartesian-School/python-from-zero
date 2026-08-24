"""Мини-проект «Калькулятор» на Tkinter.

Домашняя практика к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python calculator.py

Вычисление выражения (vychislit_vyrazhenie) не использует eval() — оно
разбирает выражение через модуль ast и вычисляет только числа и операторы
+ - * / из уже проверенного дерева разбора. Импорт этого файла не
открывает окно: tk.Tk() создаётся только внутри main().
"""

from __future__ import annotations

import ast
import operator
import tkinter as tk

DOPUSTIMYE_SIMVOLY = set("0123456789+-*/(). ")

DOPUSTIMYE_OPERATORY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def vychislit_uzel(uzel: ast.AST) -> float:
    """Вычисляет один узел дерева разбора ast — только числа, бинарные
    операторы + - * / и унарный минус. Любой другой узел (имя переменной,
    вызов функции, импорт и так далее) — недопустим и вызывает ValueError,
    поэтому такое выражение, как "import os", никогда не будет выполнено:
    ast.parse превратит его в узел Import, а не Expression с числами."""
    if isinstance(uzel, ast.Constant) and isinstance(uzel.value, int | float):
        return uzel.value
    if isinstance(uzel, ast.BinOp) and type(uzel.op) in DOPUSTIMYE_OPERATORY:
        levaya = vychislit_uzel(uzel.left)
        pravaya = vychislit_uzel(uzel.right)
        return DOPUSTIMYE_OPERATORY[type(uzel.op)](levaya, pravaya)
    if isinstance(uzel, ast.UnaryOp) and isinstance(uzel.op, ast.USub):
        return -vychislit_uzel(uzel.operand)
    raise ValueError(f"недопустимый узел выражения: {ast.dump(uzel)}")


def vychislit_vyrazhenie(vyrazhenie: str) -> str:
    """Безопасно вычисляет арифметическое выражение из цифр и + - * / ( ).

    Сначала проверяет, что строка состоит только из разрешённых символов,
    затем разбирает её в дерево ast.parse(..., mode="eval") и вычисляет
    само дерево через vychislit_uzel — без вызова eval()."""
    if not vyrazhenie or not set(vyrazhenie) <= DOPUSTIMYE_SIMVOLY:
        return "Ошибка"
    try:
        derevo = ast.parse(vyrazhenie, mode="eval")
        rezultat = vychislit_uzel(derevo.body)
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError):
        return "Ошибка"
    if isinstance(rezultat, float) and rezultat.is_integer():
        rezultat = int(rezultat)
    return str(rezultat)


class SostoyanieKalkulyatora:
    """Текущее выражение калькулятора — обычная строка, без Tkinter.
    GUI в main() лишь читает и меняет объект этого класса."""

    def __init__(self) -> None:
        self.tekushee_vyrazhenie = ""

    def na_cifru_ili_znak_nazhali(self, simvol: str) -> None:
        self.tekushee_vyrazhenie += simvol

    def na_ravno_nazhali(self) -> None:
        self.tekushee_vyrazhenie = vychislit_vyrazhenie(self.tekushee_vyrazhenie)

    def na_ochistit_nazhali(self) -> None:
        self.tekushee_vyrazhenie = ""

    def na_ekrane(self) -> str:
        return self.tekushee_vyrazhenie if self.tekushee_vyrazhenie else "0"


def main() -> None:
    root = tk.Tk()
    root.title("Калькулятор")

    sostoyanie = SostoyanieKalkulyatora()
    ekran_text = tk.StringVar(value="0")

    def obnovit_ekran() -> None:
        ekran_text.set(sostoyanie.na_ekrane())

    def na_cifru_ili_znak_nazhali(simvol: str) -> None:
        sostoyanie.na_cifru_ili_znak_nazhali(simvol)
        obnovit_ekran()

    def na_ravno_nazhali() -> None:
        sostoyanie.na_ravno_nazhali()
        obnovit_ekran()

    def na_ochistit_nazhali() -> None:
        sostoyanie.na_ochistit_nazhali()
        obnovit_ekran()

    ekran = tk.Label(root, textvariable=ekran_text, font=("Arial", 24), anchor="e", width=12)
    ekran.grid(row=0, column=0, columnspan=4, sticky="we", padx=4, pady=8)

    knopki = [
        ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
        ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
        ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ]

    for podpis, stroka, stolbec in knopki:
        if podpis == "=":
            knopka = tk.Button(root, text=podpis, command=na_ravno_nazhali)
        else:
            knopka = tk.Button(root, text=podpis, command=lambda s=podpis: na_cifru_ili_znak_nazhali(s))
        knopka.grid(row=stroka, column=stolbec, sticky="we")

    knopka_c = tk.Button(root, text="C", command=na_ochistit_nazhali)
    knopka_c.grid(row=5, column=0, columnspan=4, sticky="we", pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()
