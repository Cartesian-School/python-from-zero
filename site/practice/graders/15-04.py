from pathlib import Path

checks = [
    {"name": "zametki.txt — обе заметки сохранились в правильном порядке", "passed": Path("zametki.txt").read_text().splitlines() == ["Первая заметка", "Вторая заметка"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
