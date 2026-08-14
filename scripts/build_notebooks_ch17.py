#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 17 (Крестики-нолики)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-17"

MAINLOOP_NOTE_MD = (
    "## Про mainloop() в этом ноутбуке\n\n"
    "Вместо `root.mainloop()` здесь используется `root.update()` + `root.destroy()` — "
    "приложение строится точно так же, просто без бесконечного ожидания в конце (см. "
    "объяснение в ноутбуках главы 16)."
)


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 17-01 · Привязка событий\n\nПрактика к разделу "
          "[«Привязка событий»](../../site/chapters/glava-17/17-01-privyazka-sobytij.html).")
    nb.md("## Цель\n\nОсвоить .bind() для реакции на события клавиатуры.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
label = tk.Label(root, text="Нажмите любую клавишу", font=("Arial", 14))
label.pack(padx=20, pady=20)

nazhatiya = []

def na_klavishu(event):
    nazhatiya.append(event.keysym)
    label.config(text=f"Вы нажали: {event.keysym}")

root.bind("<Key>", na_klavishu)
root.update()

# программно "нажимаем" клавишу, как это сделал бы пользователь
label.event_generate("<Key>", keysym="Up")
root.update()

print("Нажатия:", nazhatiya)
print("Текст метки:", label.cget("text"))
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nПривяжите обработчик к событию `<Return>` (клавиша "
          "Enter) вместо `<Key>`.")
    nb.code('''root = tk.Tk()
label = tk.Label(root, text="Ожидание Enter")

def na_enter(event):
    label.config(text="Enter нажат!")

root.bind("<Return>", na_enter)
root.update()
label.event_generate("<Return>")
root.update()

print(label.cget("text"))
root.destroy()''')
    nb.write(OUT_DIR / "17-01-bind.ipynb")
    print(f"Записано: 17-01 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 17-03 · Переменные и кнопки\n\nПрактика к разделу "
          "[«Создаём глобальные переменные и кнопки»](../../site/chapters/glava-17/17-03-peremennye-knopki.html).")
    nb.md("## Цель\n\nСоздать переменные состояния и поле из девяти кнопок.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()

tekuschij_igrok = "X"
polya = []
igra_okonchena = False

pole_frame = tk.Frame(root)
pole_frame.pack()

for indeks in range(9):
    knopka = tk.Button(pole_frame, text="", font=("Arial", 24, "bold"), width=3, height=1)
    knopka.grid(row=indeks // 3, column=indeks % 3)
    polya.append(knopka)

print("Создано кнопок:", len(polya))
print("Позиция кнопки 4 (центр):", polya[4].grid_info()["row"], polya[4].grid_info()["column"])
root.update()
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что indeks // 3 и indeks % 3 дают "
          "правильные координаты для всех девяти клеток.")
    nb.code('''for indeks in range(9):
    print(indeks, "-> row", indeks // 3, "col", indeks % 3)''')
    nb.write(OUT_DIR / "17-03-peremennye-knopki.ipynb")
    print(f"Записано: 17-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 17-04 · Рисуем на кнопке\n\nПрактика к разделу "
          "[«При нажатии на кнопку рисуем на ней»](../../site/chapters/glava-17/17-04-risuem-na-knopke.html).")
    nb.md("## Цель\n\nОбработать клик по клетке поля с правильной лямбдой.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Типичная ошибка — lambda без i=indeks")
    nb.code('''import tkinter as tk

root = tk.Tk()
klikov = []

def obrabotat(indeks):
    klikov.append(indeks)

# ОШИБКА: все кнопки запомнят одно и то же значение indeks (последнее — 2)
knopki_nepravilno = []
for indeks in range(3):
    b = tk.Button(root, text=str(indeks), command=lambda: obrabotat(indeks))
    knopki_nepravilno.append(b)

for b in knopki_nepravilno:
    b.invoke()

print("Неправильно:", klikov)  # все три клика запишут одно и то же число!''')
    nb.md("## Исправление — lambda с i=indeks")
    nb.code('''klikov_pravilno = []

def obrabotat2(indeks):
    klikov_pravilno.append(indeks)

knopki_pravilno = []
for indeks in range(3):
    b = tk.Button(root, text=str(indeks), command=lambda i=indeks: obrabotat2(i))
    knopki_pravilno.append(b)

for b in knopki_pravilno:
    b.invoke()

print("Правильно:", klikov_pravilno)  # 0, 1, 2 — как и ожидалось
root.update()
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоберите функцию na_knopku_nazhali(), "
          "которая рисует X или O и переключает игрока, и проверьте её на трёх кликах.")
    nb.code('''root = tk.Tk()
tekuschij_igrok = "X"
polya = []

def na_knopku_nazhali(indeks):
    global tekuschij_igrok
    if polya[indeks]["text"] != "":
        return
    polya[indeks]["text"] = tekuschij_igrok
    tekuschij_igrok = "O" if tekuschij_igrok == "X" else "X"

for indeks in range(9):
    b = tk.Button(root, text="", command=lambda i=indeks: na_knopku_nazhali(i))
    polya.append(b)

na_knopku_nazhali(0)
na_knopku_nazhali(1)
na_knopku_nazhali(2)

print([b["text"] for b in polya[:3]])  # X, O, X
root.update()
root.destroy()''')
    nb.write(OUT_DIR / "17-04-risuem.ipynb")
    print(f"Записано: 17-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 17-05 · Проверка победы\n\nПрактика к разделу "
          "[«Проверяем после каждого хода, победил ли игрок»](../../site/chapters/glava-17/17-05-proverka-pobedy.html).")
    nb.md("## Цель\n\nПроверить все восемь выигрышных линий.")
    nb.md("## Рабочий пример")
    nb.code('''def proverit_pobedu(polya_teksty):
    linii_pobedy = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for a, b, c in linii_pobedy:
        znacheniya = (polya_teksty[a], polya_teksty[b], polya_teksty[c])
        if znacheniya[0] != "" and znacheniya[0] == znacheniya[1] == znacheniya[2]:
            return znacheniya[0]
    return None

# верхняя строка выиграна X
doska = ["X", "X", "X", "", "O", "O", "", "", ""]
print(proverit_pobedu(doska))''')
    nb.md("## Эксперимент 1 — все восемь линий")
    nb.code('''test_slucai = [
    (["X","X","X","","","","","",""], "X", "строка 1"),
    (["","","","O","O","O","","",""], "O", "строка 2"),
    (["X","","","X","","","X","",""], "X", "столбец 1"),
    (["X","","","","X","","","","X"], "X", "диагональ"),
    (["","","X","","X","","X","",""], "X", "антидиагональ"),
    (["X","O","X","O","X","O","O","X","O"], None, "нет победителя"),
]

for doska, ozhidaemyj, opisanie in test_slucai:
    result = proverit_pobedu(doska)
    status = "OK" if result == ozhidaemyj else "ОШИБКА"
    print(f"{opisanie}: получили {result}, ожидали {ozhidaemyj} -> {status}")''')
    nb.md("## Проверка результата")
    nb.code('''assert proverit_pobedu(["X","X","X","","","","","",""]) == "X"
assert proverit_pobedu(["O","X","O","X","O","X","X","O","X"]) is None
print("Обе проверки пройдены.")''')
    nb.md("## Задание ★ Базовая практика — ничья")
    nb.code('''def polye_zapolneno(polya_teksty):
    return all(t != "" for t in polya_teksty)

polnaya_bez_pobeditelya = ["X","O","X","X","O","O","O","X","X"]
print("Заполнено:", polye_zapolneno(polnaya_bez_pobeditelya))
print("Победитель:", proverit_pobedu(polnaya_bez_pobeditelya))''')
    nb.write(OUT_DIR / "17-05-pobeda.ipynb")
    print(f"Записано: 17-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 17-06 · Полная игра\n\nПрактика к разделу "
          "[«Кнопка новой игры и полная программа»](../../site/chapters/glava-17/17-06-novaya-igra-itogi.html).")
    nb.md("## Цель\n\nСобрать и полностью протестировать игру целиком — тот же код, что и в "
          "`projects/tkinter/tic-tac-toe/tic_tac_toe.py`.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Полная игра")
    nb.code('''import tkinter as tk

root = tk.Tk()
root.title("Крестики-нолики")

tekuschij_igrok = "X"
polya = []
igra_okonchena = False


def proverit_pobedu():
    linii_pobedy = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for a, b, c in linii_pobedy:
        znacheniya = (polya[a]["text"], polya[b]["text"], polya[c]["text"])
        if znacheniya[0] != "" and znacheniya[0] == znacheniya[1] == znacheniya[2]:
            return znacheniya[0]
    return None


def polye_zapolneno():
    return all(knopka["text"] != "" for knopka in polya)


def na_knopku_nazhali(indeks):
    global tekuschij_igrok, igra_okonchena
    if igra_okonchena or polya[indeks]["text"] != "":
        return

    polya[indeks]["text"] = tekuschij_igrok

    pobeditel = proverit_pobedu()
    if pobeditel:
        status_label.config(text=f"Победил игрок {pobeditel}!")
        igra_okonchena = True
        return

    if polye_zapolneno():
        status_label.config(text="Ничья!")
        igra_okonchena = True
        return

    tekuschij_igrok = "O" if tekuschij_igrok == "X" else "X"
    status_label.config(text=f"Ход игрока: {tekuschij_igrok}")


def novaya_igra():
    global tekuschij_igrok, igra_okonchena
    tekuschij_igrok = "X"
    igra_okonchena = False
    for knopka in polya:
        knopka.config(text="")
    status_label.config(text=f"Ход игрока: {tekuschij_igrok}")


status_label = tk.Label(root, text=f"Ход игрока: {tekuschij_igrok}", font=("Arial", 14))
status_label.grid(row=0, column=0, columnspan=3, pady=10)

pole_frame = tk.Frame(root)
pole_frame.grid(row=1, column=0, columnspan=3)

for indeks in range(9):
    knopka = tk.Button(
        pole_frame, text="", font=("Arial", 24, "bold"), width=3, height=1,
        command=lambda i=indeks: na_knopku_nazhali(i),
    )
    knopka.grid(row=indeks // 3, column=indeks % 3)
    polya.append(knopka)

tk.Button(root, text="Новая игра", command=novaya_igra).grid(row=2, column=0, columnspan=3, pady=10)

print("Игра построена, кнопок:", len(polya))
root.update()''')
    nb.md("## Проверка результата — полная партия")
    nb.code('''# X играет верхнюю строку, O играет 3 и 4
for i in [0, 3, 1, 4, 2]:
    polya[i].invoke()

print(status_label.cget("text"))
assert igra_okonchena is True
assert "X" in status_label.cget("text")
print("Партия завершилась победой X — верно.")''')
    nb.md("## Задание ★★ Самостоятельная задача — новая игра")
    nb.code('''novaya_igra()
print(status_label.cget("text"))
assert igra_okonchena is False
assert all(b["text"] == "" for b in polya)
print("Поле очищено, игра готова к новой партии.")
root.destroy()''')
    nb.write(OUT_DIR / "17-06-polnaya-igra.ipynb")
    print(f"Записано: 17-06 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_03()
    build_04()
    build_05()
    build_06()
