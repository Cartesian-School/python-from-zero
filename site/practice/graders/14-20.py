checks = [
    {"name": "Krug.perimetr() — длина окружности", "passed": abs(krug.perimetr() - 31.4159) < 0.01},
    {"name": "Pryamougolnik.perimetr() — верный периметр", "passed": pryamougolnik.perimetr() == 20},
    {"name": "Treugolnik.perimetr() — верный периметр равнобедренного треугольника", "passed": abs(treugolnik.perimetr() - 18.0) < 0.01},
    {"name": "все фигуры — экземпляры Figura", "passed": isinstance(krug, Figura) and isinstance(pryamougolnik, Figura) and isinstance(treugolnik, Figura)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
