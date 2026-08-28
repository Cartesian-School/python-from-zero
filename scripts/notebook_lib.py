"""Переиспользуемый помощник для сборки практических ноутбуков Cartesian School.

Использование:

    from notebook_lib import NotebookBuilder

    nb = NotebookBuilder()
    nb.md("# Заголовок")
    nb.code("print('привет')")
    nb.write(Path("notebooks/chapter-01/01-01-example.ipynb"))
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

KERNELSPEC = {
    "display_name": "Cartesian Python 3.14",
    "language": "python",
    "name": "cartesian-python314",
}
LANGUAGE_INFO = {"name": "python", "version": "3.14.6"}


class NotebookBuilder:
    def __init__(self) -> None:
        self._cells: list = []

    def md(self, text: str, *, cell_id: str | None = None) -> NotebookBuilder:
        """Append a Markdown cell, optionally with a stable delivery identifier."""

        cell = nbf.v4.new_markdown_cell(text)
        if cell_id is not None:
            cell["id"] = cell_id
        self._cells.append(cell)
        return self

    def code(
        self,
        text: str,
        *,
        raises: bool = False,
        cell_id: str | None = None,
    ) -> NotebookBuilder:
        """raises=True marks a cell that is EXPECTED to raise (e.g. a "типичная
        ошибка" demo). nbclient's standard "raises-exception" cell tag makes it
        capture the traceback as output and continue, instead of halting the run."""
        cell = nbf.v4.new_code_cell(text)
        if cell_id is not None:
            cell["id"] = cell_id
        if raises:
            cell["metadata"]["tags"] = ["raises-exception"]
        self._cells.append(cell)
        return self

    def write(self, path: Path) -> Path:
        nb = nbf.v4.new_notebook()
        nb["cells"] = self._cells
        nb["metadata"] = {"kernelspec": KERNELSPEC, "language_info": LANGUAGE_INFO}
        path.parent.mkdir(parents=True, exist_ok=True)
        nbf.write(nb, path)
        return path

    def __len__(self) -> int:
        return len(self._cells)
