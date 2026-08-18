checks = [
    {"name": "rel — относительный путь не является абсолютным", "passed": rel.is_absolute() is False},
    {"name": "abs_path — после resolve() путь становится абсолютным", "passed": abs_path.is_absolute() is True},
    {"name": "imya_sovpadaet — имя файла не потерялось при переходе к абсолютному пути", "passed": imya_sovpadaet is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
