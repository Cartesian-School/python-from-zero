#!/usr/bin/env python3
"""Выполняет .ipynb сверху вниз через nbclient и сохраняет результат.

Использование: python scripts/run_notebook.py notebooks/chapter-06/06-02-forward-back.ipynb
Завершается с ненулевым кодом, если выполнение прервалось с ошибкой.
"""

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def run(path: Path, timeout: int = 120) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    nbformat.write(nb, path)
    print(f"OK: {path} выполнен без ошибок")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: run_notebook.py <файл.ipynb> [ещё файлы...]")
        sys.exit(2)
    failed = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        try:
            run(p)
        except Exception as exc:  # nbclient raises CellExecutionError on failed cells
            print(f"FAIL: {p} — {exc}")
            failed.append(p)
    if failed:
        sys.exit(1)
