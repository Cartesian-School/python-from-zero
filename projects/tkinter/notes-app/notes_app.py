"""Мини-проект «Заметки»: знакомство с файлами и Tkinter.

Домашняя практика к главе 23 книги «Python с нуля» (Cartesian School).
Запуск: python notes_app.py

Импорт этого файла не открывает окно: tk.Tk() создаётся только внутри
main(). Чтение и запись файла вынесены в отдельные функции без Tkinter
(sohranit_v_fajl, zagruzit_iz_fajla) — их можно проверять во временном
каталоге, не запуская GUI.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox

FAJL_ZAMETOK_PO_UMOLCHANIYU = Path(__file__).parent / "zametka.txt"


def sohranit_v_fajl(put: Path, tekst: str) -> None:
    """Сохраняет текст в файл put в кодировке UTF-8.

    Пробрасывает PermissionError и OSError дальше — вызывающий код решает,
    как показать ошибку пользователю."""
    put.write_text(tekst, encoding="utf-8")


def zagruzit_iz_fajla(put: Path) -> str:
    """Читает текст из файла put в кодировке UTF-8.

    Пробрасывает FileNotFoundError, если файла ещё нет, — это ожидаемая
    ситуация при первом запуске, а не повод падать с трудночитаемой
    трассировкой. read_text() уже поднимает это исключение сам; отдельная
    проверка put.exists() до чтения не нужна — а вдобавок оставляла бы
    короткий промежуток, за который файл мог бы исчезнуть между проверкой
    и самим чтением."""
    return put.read_text(encoding="utf-8")


def main() -> None:
    root = tk.Tk()
    root.title("Заметки")

    fajl_zametok = FAJL_ZAMETOK_PO_UMOLCHANIYU
    status_text = tk.StringVar(value="")
    est_nesohranennye_izmeneniya = tk.BooleanVar(value=False)

    polye_teksta = tk.Text(root, width=50, height=15)
    polye_teksta.pack(padx=8, pady=8)

    def na_izmenenie_teksta(event: object) -> None:
        # <<Modified>> — встроенный сигнал Tk «содержимое виджета изменилось»:
        # он срабатывает при любом изменении текста, а не только при вводе с
        # клавиатуры (например, и при вставке через контекстное меню мыши).
        # У события есть особенность: после срабатывания флаг edit_modified
        # нужно сбросить вручную через edit_modified(False), иначе оно больше
        # не сработает ни разу — сброс здесь на каждое реальное изменение
        # держит счётчик рабочим постоянно.
        if polye_teksta.edit_modified():
            est_nesohranennye_izmeneniya.set(True)
            polye_teksta.edit_modified(False)

    polye_teksta.bind("<<Modified>>", na_izmenenie_teksta)

    def zamenit_tekst_programmno(novyj_tekst: str) -> None:
        """Заменяет содержимое поля программно (после load/очистки) так,
        чтобы это НЕ отметилось как несохранённое изменение пользователя:
        edit_modified(False) сбрасывает флаг, который сама вставка
        выставляет, — иначе загрузка немедленно выглядела бы как
        «несохранённые изменения»."""
        polye_teksta.delete("1.0", "end")
        polye_teksta.insert("1.0", novyj_tekst)
        polye_teksta.edit_modified(False)
        est_nesohranennye_izmeneniya.set(False)

    def sohranit_zametku() -> None:
        tekst = polye_teksta.get("1.0", "end-1c")
        try:
            sohranit_v_fajl(fajl_zametok, tekst)
        except (PermissionError, OSError) as oshibka:
            status_text.set(f"Не удалось сохранить: {oshibka}")
            return
        est_nesohranennye_izmeneniya.set(False)
        status_text.set(f"Сохранено в {fajl_zametok.name}")

    def zagruzit_zametku() -> None:
        if est_nesohranennye_izmeneniya.get():
            status_text.set("Есть несохранённые изменения — сначала сохраните или очистите поле")
            return
        try:
            tekst = zagruzit_iz_fajla(fajl_zametok)
        except FileNotFoundError:
            status_text.set("Файл заметки ещё не создан — сначала сохраните.")
            return
        except (PermissionError, OSError) as oshibka:
            status_text.set(f"Не удалось загрузить: {oshibka}")
            return
        zamenit_tekst_programmno(tekst)
        status_text.set(f"Загружено из {fajl_zametok.name}")

    def ochistit_polye() -> None:
        if est_nesohranennye_izmeneniya.get():
            status_text.set("Есть несохранённые изменения — сначала сохраните, иначе очистка их сотрёт")
            return
        zamenit_tekst_programmno("")
        status_text.set("Поле очищено (файл не тронут)")

    def na_zakrytie_okna() -> None:
        if est_nesohranennye_izmeneniya.get():
            zakryt_bez_sohraneniya = messagebox.askyesno(
                "Есть несохранённые изменения",
                "Закрыть без сохранения? Несохранённые изменения будут потеряны.",
            )
            if not zakryt_bez_sohraneniya:
                return
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", na_zakrytie_okna)

    knopki = tk.Frame(root)
    knopki.pack(pady=4)
    tk.Button(knopki, text="Сохранить", command=sohranit_zametku).pack(side="left", padx=4)
    tk.Button(knopki, text="Загрузить", command=zagruzit_zametku).pack(side="left", padx=4)
    tk.Button(knopki, text="Очистить поле", command=ochistit_polye).pack(side="left", padx=4)

    tk.Label(root, textvariable=status_text, fg="gray").pack(pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()
