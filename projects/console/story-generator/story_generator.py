"""Мини-проект «Генератор случайных историй».

Домашняя практика к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python story_generator.py

sluchajnaya_istoriya() принимает необязательный параметр rng — экземпляр
random.Random. Тесты передают random.Random(seed), чтобы получать
предсказуемый результат вместо зависимости от глобального состояния
модуля random.
"""

from __future__ import annotations

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


def sluchajnaya_istoriya(rng: random.Random | None = None) -> str:
    generator = rng if rng is not None else random
    return SHABLON.format(
        prilagatelnoe=generator.choice(PRILAGATELNYE),
        sushestvitelnoe=generator.choice(SUSHESTVITELNYE),
        mesto=generator.choice(MESTA),
        glagol=generator.choice(GLAGOLY),
        predmet=generator.choice(PREDMETY),
    )


def neskolko_istorij(kolichestvo: int, rng: random.Random | None = None) -> list[str]:
    generator = rng if rng is not None else random
    return [sluchajnaya_istoriya(generator) for _ in range(kolichestvo)]


if __name__ == "__main__":
    print(sluchajnaya_istoriya())
