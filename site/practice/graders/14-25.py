checks = [
    {"name": "Schet.value — накапливается между вызовами increment()", "passed": schet.value == 2},
    {"name": "srednee_arifmeticheskoe — работает как функция, без лишнего состояния", "passed": callable(srednee_arifmeticheskoe) and srednee_arifmeticheskoe([2, 4, 6]) == 4},
    {"name": "Schet — свежий счётчик начинается с нуля", "passed": Schet().value == 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
