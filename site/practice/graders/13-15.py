checks = [
    {"name": "area — rectangle_area вернула результат (чистая функция)", "passed": area == 20},
    {"name": "log — draw_square_effect записала побочный эффект", "passed": log == ["Нарисован квадрат 10"]},
    {"name": "rectangle_area — верна на новых аргументах", "passed": rectangle_area(2, 3) == 6},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
