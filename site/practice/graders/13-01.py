import io, sys

_buf = io.StringIO()
_old = sys.stdout
sys.stdout = _buf
try:
    poproshchatsya()
finally:
    sys.stdout = _old
_output = _buf.getvalue()

checks = [
    {"name": "poproshchatsya — определена и вызывается без ошибок", "passed": callable(poproshchatsya)},
    {"name": "poproshchatsya — при вызове действительно печатает текст", "passed": len(_output.strip()) > 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
