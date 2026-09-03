# Доверенный грейдер для практики 20-21 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки),
# а также сами определённые учеником функции — они лежат в общем globals().
#
# Здесь мы не ограничиваемся флагом "ячейка не упала": AABB-проверку и
# уменьшение хитбокса грейдер прогоняет на собственных векторах, которых нет
# в ноутбуке, — иначе задание можно было бы "сдать", ничего не реализовав.

_cells = __cartesian__["cells"]

_proverka = _cells.get("5a3b85db", {})  # "Проверка результата" -- AABB-пересечение
_zadanie = _cells.get("b557e3f8", {})   # "Задание ★★" -- уменьшенный хитбокс

_g = globals()


def _proverit_aabb():
    """Прогоняет функцию ученика на собственных случаях, включая пограничные."""
    fn = _g.get("pryamougolniki_peresekayutsya")
    if not callable(fn):
        return False
    sluchai = [
        (((100, 100, 40, 40), (120, 120, 40, 40)), True),   # обычное перекрытие
        (((100, 100, 40, 40), (400, 400, 40, 40)), False),  # далеко друг от друга
        (((0, 0, 40, 40), (40, 0, 40, 40)), False),         # касание ровно краем
        (((0, 0, 40, 40), (39, 0, 40, 40)), True),          # перекрытие в один пиксель
        (((0, 0, 40, 40), (20, 40, 40, 40)), False),        # соседи по вертикали
        (((0, 0, 40, 40), (10, 10, 5, 5)), True),           # один внутри другого
    ]
    try:
        return all(fn(a, b) is ozhidaem for (a, b), ozhidaem in sluchai)
    except Exception:
        return False


def _proverit_szhatie():
    """Хитбокс обязан реально уменьшаться и менять исход у краевого врага."""
    szhat = _g.get("szhat")
    fn = _g.get("pryamougolniki_peresekayutsya")
    if not callable(szhat) or not callable(fn):
        return False
    try:
        # 1. Сжатие само по себе: центр сохраняется, размер падает на 2*na.
        if szhat((100, 100, 40, 40), 10) != (110, 110, 20, 20):
            return False
        if szhat((0, 0, 100, 100), 25) != (25, 25, 50, 50):
            return False
        # 2. Поведение: глубокое столкновение остаётся, краевое исчезает.
        igrok_polnyj = (100, 100, 40, 40)
        igrok_malyj = szhat(igrok_polnyj, 10)
        gluboko = (120, 120, 40, 40)
        kraem = (135, 135, 40, 40)
        return (
            fn(igrok_polnyj, gluboko) is True
            and fn(igrok_malyj, gluboko) is True
            and fn(igrok_polnyj, kraem) is True
            and fn(igrok_malyj, kraem) is False
        )
    except Exception:
        return False


checks = [
    {
        "name": "Проверка результата: пересечение прямоугольников находится верно",
        "passed": bool(_proverka) and _proverka.get("ok", False) and _proverit_aabb(),
    },
    {
        "name": "Задание ★★: хитбокс реально уменьшается и убирает попадание по краю",
        "passed": bool(_zadanie) and _zadanie.get("ok", False) and _proverit_szhatie(),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "20-21", "passed": passed, "score": score, "checks": checks}
