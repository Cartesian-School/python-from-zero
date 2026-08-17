import io, sys

_buf = io.StringIO()
_old = sys.stdout
sys.stdout = _buf
try:
    a()
finally:
    sys.stdout = _old
_output = _buf.getvalue()

checks = [
    {"name": "a() выводит A1, B, A2 в правильном порядке", "passed": _output.strip() == "A1\nB\nA2"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
