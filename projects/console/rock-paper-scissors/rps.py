"""Мини-проект «Камень, ножницы, бумага».

Проект к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python rps.py
"""

import random

VARIANTY = ["камень", "ножницы", "бумага"]

# кто побеждает кого: ключ побеждает значение
POBEZHDAET = {
    "камень": "ножницы",
    "ножницы": "бумага",
    "бумага": "камень",
}


def hod_kompyutera():
    return random.choice(VARIANTY)


def opredelit_pobeditelya(hod_igroka, hod_kompyutera):
    """Возвращает 'игрок', 'компьютер' или 'ничья'."""
    if hod_igroka == hod_kompyutera:
        return "ничья"
    if POBEZHDAET[hod_igroka] == hod_kompyutera:
        return "игрок"
    return "компьютер"


def sygrat_raund(hod_igroka):
    hod_pk = hod_kompyutera()
    pobeditel = opredelit_pobeditelya(hod_igroka, hod_pk)
    return hod_pk, pobeditel


def glavnoe_menyu():
    schet_igroka = 0
    schet_kompyutera = 0

    while True:
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

    print(f"Игра окончена. Финальный счёт — вы: {schet_igroka}, компьютер: {schet_kompyutera}")


if __name__ == "__main__":
    glavnoe_menyu()
