_correct = move_from_tail([(0, 0), (-20, 0), (-40, 0)], (20, 0))
_broken = move_from_head_BROKEN([(0, 0), (-20, 0), (-40, 0)], (20, 0))
checks = [
    {"name": "движение с хвоста сохраняет позиции", "passed": _correct == [(20, 0), (0, 0), (-20, 0)]},
    {"name": "движение с головы схлопывает сегменты", "passed": _broken == [(20, 0), (20, 0), (20, 0)]},
    {"name": "два варианта дают разный результат", "passed": _correct != _broken},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
