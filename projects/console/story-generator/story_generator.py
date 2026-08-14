"""Мини-проект «Генератор случайных историй».

Проект к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python story_generator.py
"""

import random

PRILAGATELNYE = ["храбрый", "любопытный", "рассеянный", "весёлый", "загадочный"]
SUSHESTVITELNYE = ["дракон", "программист", "кот", "путешественник", "робот"]
MESTA = ["в тёмном лесу", "на далёкой планете", "в старой библиотеке", "в подвале дома"]
GLAGOLY = ["нашёл", "потерял", "починил", "изобрёл", "испугался"]
PREDMETY = ["волшебный ноутбук", "древний свиток", "сломанный компас", "банку варенья"]

SHABLON = (
    "Однажды {prilagatelnoe} {sushestvitelnoe} {mesto} {glagol} {predmet}. "
    "С тех пор жизнь его больше не была прежней."
)


def sluchajnaya_istoriya():
    return SHABLON.format(
        prilagatelnoe=random.choice(PRILAGATELNYE),
        sushestvitelnoe=random.choice(SUSHESTVITELNYE),
        mesto=random.choice(MESTA),
        glagol=random.choice(GLAGOLY),
        predmet=random.choice(PREDMETY),
    )


if __name__ == "__main__":
    print(sluchajnaya_istoriya())
