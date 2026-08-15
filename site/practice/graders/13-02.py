import io, sys

_buf = io.StringIO()
_old = sys.stdout
sys.stdout = _buf
try:
    plosch_pryamougolnika(4, 5)
finally:
    sys.stdout = _old
_output = _buf.getvalue()

checks = [
    {"name": "plosch_pryamougolnika(4, 5) — верно печатает площадь 20", "passed": "20" in _output},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
