checks = [
    {"name": "docstring_present — у функции есть докстринг", "passed": docstring_present is True},
    {"name": "area — rectangle_area(3, 4)", "passed": area == 12},
    {"name": "rectangle_area.__annotations__ — есть аннотации типов", "passed": bool(rectangle_area.__annotations__)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
