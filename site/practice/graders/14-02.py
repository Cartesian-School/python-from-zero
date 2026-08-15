checks = [
    {"name": "knigi — три объекта Kniga созданы", "passed": len(knigi) == 3},
    {"name": "у каждой книги есть nazvanie и avtor", "passed": all(hasattr(k, "nazvanie") and hasattr(k, "avtor") for k in knigi)},
    {"name": "первая книга — «Война и мир» Толстого", "passed": knigi[0].nazvanie == "Война и мир" and knigi[0].avtor == "Толстой"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
