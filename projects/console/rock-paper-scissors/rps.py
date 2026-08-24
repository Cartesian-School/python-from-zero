"""Мини-проект «Камень, ножницы, бумага».

Домашняя практика к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python rps.py

hod_kompyutera() принимает необязательный rng — экземпляр random.Random,
чтобы тесты могли получать предсказуемый ход компьютера вместо зависимости
от глобального состояния модуля random.
"""

from __future__ import annotations

import random

VARIANTY = ["камень", "ножницы", "бумага"]

# кто побеждает кого: ключ побеждает значение
POBEZHDAET = {
    "камень": "ножницы",
    "ножницы": "бумага",
    "бумага": "камень",
}

POBED_DLYA_POBEDY_V_MATCHE = 3


def hod_kompyutera(rng: random.Random | None = None) -> str:
    generator = rng if rng is not None else random
    return generator.choice(VARIANTY)


def opredelit_pobeditelya(hod_igroka: str, hod_kompyutera: str) -> str:
    """Возвращает 'игрок', 'компьютер' или 'ничья'."""
    if hod_igroka == hod_kompyutera:
        return "ничья"
    if POBEZHDAET[hod_igroka] == hod_kompyutera:
        return "игрок"
    return "компьютер"


def sygrat_raund(hod_igroka: str, rng: random.Random | None = None) -> tuple[str, str]:
    hod_pk = hod_kompyutera(rng)
    pobeditel = opredelit_pobeditelya(hod_igroka, hod_pk)
    return hod_pk, pobeditel


def glavnoe_menyu() -> None:
    """Матч до трёх побед одной из сторон."""
    schet_igroka = 0
    schet_kompyutera = 0

    while schet_igroka < POBED_DLYA_POBEDY_V_MATCHE and schet_kompyutera < POBED_DLYA_POBEDY_V_MATCHE:
        hod_igroka = input("Ваш ход (камень/ножницы/бумага, 'выход' — закончить): ").strip().lower()
        if hod_igroka == "выход":
            break
        if hod_igroka not in VARIANTY:
            print("Не понял ход, попробуйте ещё раз.")
            continue

        hod_pk, pobeditel = sygrat_raund(hod_igroka)
        print(f"Компьютер выбрал: {hod_pk}")

        if pobeditel == "ничья":
            print("Ничья!")
        elif pobeditel == "игрок":
            schet_igroka += 1
            print("Вы победили в этом раунде!")
        else:
            schet_kompyutera += 1
            print("Компьютер победил в этом раунде!")

        print(f"Счёт — вы: {schet_igroka}, компьютер: {schet_kompyutera}\n")

    if schet_igroka == POBED_DLYA_POBEDY_V_MATCHE:
        print(f"Матч выигран! Финальный счёт — вы: {schet_igroka}, компьютер: {schet_kompyutera}")
    elif schet_kompyutera == POBED_DLYA_POBEDY_V_MATCHE:
        print(f"Матч проигран. Финальный счёт — вы: {schet_igroka}, компьютер: {schet_kompyutera}")
    else:
        print(f"Игра остановлена. Счёт на момент выхода — вы: {schet_igroka}, компьютер: {schet_kompyutera}")


if __name__ == "__main__":
    glavnoe_menyu()
