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


def _lesson_link(lesson_id: str, title: str, href: str) -> str:
    return f"# {lesson_id} · {title}\n\nПрактика к разделу [«{title}»](../../site/chapters/glava-17/{href})."


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-07", "Event, callback, command и binding", "17-07-event-callback-command-binding.html"))
    nb.md("## Цель\n\nЧётко различать четыре термина: событие, callback, command, binding.")
    nb.md("## Рабочий пример — кто вызывает callback")
    nb.code('''registered_callbacks = {}

def on(event_name, callback):
    registered_callbacks[event_name] = callback

def dispatch(event_name):
    """Имитация событийного цикла Tk: вызывает callback, когда 'происходит' событие."""
    callback = registered_callbacks.get(event_name)
    if callback:
        callback()

def on_click():
    print("Кнопка нажата — но эту строку вызвали НЕ мы напрямую")

on("button_click", on_click)
print("Callback зарегистрирован, но ЕЩЁ НЕ вызван")
dispatch("button_click")  # только теперь Tk-подобный диспетчер его вызывает''')
    nb.md("## Задание ★ Базовая практика — классификация")
    nb.code('''# Определите термин для каждого описания: "event", "callback", "command" или "binding"

term_proizoshlo = "event"          # сам факт "что-то случилось"
term_funkciya_v_otvet = "callback"  # функция, вызванная в ответ на событие
term_svyaz_sobytiya_i_funkcii = "binding"  # связь между последовательностью события и callback-ом
term_semanticheskaya_aktivaciya = "command"  # высокоуровневый крючок виджета типа Button

print(term_proizoshlo, term_funkciya_v_otvet, term_svyaz_sobytiya_i_funkcii, term_semanticheskaya_aktivaciya)''')
    nb.write(OUT_DIR / "17-07-event-callback-command-binding.ipynb")
    print(f"Записано: 17-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-08", "Объект Event", "17-08-obyekt-event.html"))
    nb.md("## Цель\n\nПосмотреть на реальные поля объекта tkinter.Event для разных типов событий.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример — событие клавиатуры")
    nb.code('''import tkinter as tk

root = tk.Tk()
label = tk.Label(root, text="...")
label.pack()
poslednee = {}

def on_key(event):
    poslednee["type"] = str(event.type)
    poslednee["keysym"] = event.keysym
    poslednee["char"] = event.char
    label.config(text=f"keysym={event.keysym!r} char={event.char!r}")

root.bind("<Key>", on_key)
root.update()
label.event_generate("<Key>", keysym="Return")
root.update()
print(poslednee)''')
    nb.md("## Эксперимент — событие мыши (Enter/Leave)")
    nb.code('''poslednee_mouse = {}

def on_enter(event):
    poslednee_mouse["widget"] = str(event.widget)
    poslednee_mouse["type"] = str(event.type)

label.bind("<Enter>", on_enter)
root.update()
label.event_generate("<Enter>")
root.update()
print(poslednee_mouse)
# Обратите внимание: у события <Enter> event.keysym/event.char не несут полезной информации —
# это поля, осмысленные для КЛАВИАТУРНЫХ событий.
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПривяжите `<Button-1>` к отдельному виджету и распечатайте `event.x`/`event.y` "
          "— координаты клика внутри виджета.")
    nb.write(OUT_DIR / "17-08-obyekt-event.ipynb")
    print(f"Записано: 17-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-09", "Синтаксис событий Tk", "17-09-sintaksis-sobytij.html"))
    nb.md("## Цель\n\nСопоставить описание действия с правильной строкой-последовательностью события Tk.")
    nb.md("## Рабочий пример")
    nb.code('''opisaniya_i_posledovatelnosti = {
    "нажата клавиша Enter": "<Return>",
    "курсор вошёл в виджет": "<Enter>",
    "курсор покинул виджет": "<Leave>",
    "нажата левая кнопка мыши": "<Button-1>",
}
for opisanie, posledovatelnost in opisaniya_i_posledovatelnosti.items():
    print(f"{opisanie:30} -> {posledovatelnost}")''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''seq_klavisha_enter = "<Return>"
seq_navedenie_vhod = "<Enter>"
seq_navedenie_vyhod = "<Leave>"
seq_klik_levoj_knopkoj = "<Button-1>"

print(seq_klavisha_enter, seq_navedenie_vhod, seq_navedenie_vyhod, seq_klik_levoj_knopkoj)''')
    nb.write(OUT_DIR / "17-09-sintaksis-sobytij.ipynb")
    print(f"Записано: 17-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-10", "command vs bind — что выбирать", "17-10-command-vs-bind.html"))
    nb.md("## Цель\n\nДля трёх сценариев игры выбрать правильный инструмент: command= или bind().")
    nb.md("## Рабочий пример")
    nb.code('''def choose_tool(scenario):
    if scenario == "клик по клетке — основной ход":
        return "command"
    if scenario in ("наведение мыши — превью", "клавиши 1-9 — управление"):
        return "bind"
    return "неизвестно"

for scenario in ["клик по клетке — основной ход", "наведение мыши — превью", "клавиши 1-9 — управление"]:
    print(scenario, "->", choose_tool(scenario))''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''vybor_hod_po_kletke = "command"
vybor_hover_effekt = "bind"
vybor_klavishi_1_9 = "bind"

print(vybor_hod_po_kletke, vybor_hover_effekt, vybor_klavishi_1_9)''')
    nb.write(OUT_DIR / "17-10-command-vs-bind.ipynb")
    print(f"Записано: 17-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-11", "Focus и клавиатура", "17-11-focus-i-klaviatura.html"))
    nb.md("## Цель\n\nУвидеть, как фокус ввода определяет, какой виджет получает клавиатурные события.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
entry = tk.Entry(root)
entry.pack()
button = tk.Button(root, text="Кнопка")
button.pack()
root.update()

entry.focus_set()
root.update()
print("Фокус на Entry:", root.focus_get() is entry)

button.focus_set()
root.update()
print("Фокус на Button:", root.focus_get() is button)
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПривяжите `<Key>` и к root, и к entry (у entry — с обработчиком, "
          "который явно возвращает `\"break\"`). Установите фокус на entry и проверьте: сработает обработчик entry, "
          "а обработчик root — нет. Затем уберите `\"break\"` у entry и проверьте ещё раз: теперь сработают ОБА "
          "обработчика. Вывод: событие останавливает именно `\"break\"` где-то на пути по bindtags, а не сам факт "
          "того, что фокус находится на другом виджете.")
    nb.write(OUT_DIR / "17-11-focus-i-klaviatura.ipynb")
    print(f"Записано: 17-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-12", "Mouse Enter/Leave и hover", "17-12-enter-leave-hover.html"))
    nb.md("## Цель\n\nПостроить простой hover-эффект через <Enter>/<Leave> — без единого клика.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
button = tk.Button(root, text="Наведите на меня")
button.pack()

def on_enter(_event):
    button.config(bg="#B9A0FC")

def on_leave(_event):
    button.config(bg="SystemButtonFace" if False else "#FAFAFC")

button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)
root.update()

button.event_generate("<Enter>")
root.update()
print("После Enter:", button.cget("bg"))

button.event_generate("<Leave>")
root.update()
print("После Leave:", button.cget("bg"))
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоберите три кнопки в ряд и подсветите наведённую, гарантируя, что "
          "остальные две остаются в обычном цвете.")
    nb.write(OUT_DIR / "17-12-enter-leave-hover.ipynb")
    print(f"Записано: 17-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-13", "Модель игрового состояния", "17-13-model-sostoyaniya.html"))
    nb.md("## Цель\n\nСмоделировать игровое состояние словарём — без единого виджета.")
    nb.md("## Рабочий пример")
    nb.code('''def new_state():
    return {
        "board": [""] * 9,
        "current_player": "X",
        "game_over": False,
        "winner": None,
        "winning_line": None,
        "score_x": 0,
        "score_o": 0,
    }

state = new_state()
print(state)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''assert len(state["board"]) == 9
assert all(cell == "" for cell in state["board"])
assert state["current_player"] == "X"
assert state["game_over"] is False
print("Начальное состояние верно.")''')
    nb.write(OUT_DIR / "17-13-model-sostoyaniya.ipynb")
    print(f"Записано: 17-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-14", "Индексы, строки и столбцы", "17-14-indeksy-stroki-stolbcy.html"))
    nb.md("## Цель\n\nПреобразовать индекс клетки 0..8 в (row, column) и обратно.")
    nb.md("## Рабочий пример")
    nb.code('''def index_to_row_col(index):
    return index // 3, index % 3

def row_col_to_index(row, column):
    return row * 3 + column

for i in range(9):
    print(i, "->", index_to_row_col(i))''')
    nb.md("## Задание ★ Базовая практика — round-trip для всех 9 клеток")
    nb.code('''roundtrip_ok = all(row_col_to_index(*index_to_row_col(i)) == i for i in range(9))
assert index_to_row_col(4) == (1, 1)
assert row_col_to_index(2, 2) == 8
assert roundtrip_ok is True
print("Прямое и обратное преобразование верны для всех 9 клеток.")''')
    nb.write(OUT_DIR / "17-14-indeksy-stroki-stolbcy.ipynb")
    print(f"Записано: 17-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-15", "Правильный алгоритм хода", "17-15-algoritm-hoda.html"))
    nb.md("## Цель\n\nПроверить, что невалидный ход не меняет ни поле, ни текущего игрока.")
    nb.md("## Рабочий пример")
    nb.code('''def attempt_move_pure(board, index, current_player, game_over):
    """Возвращает (new_board, new_player, moved: bool) — не трогает Tkinter вообще."""
    if game_over or board[index]:
        return board, current_player, False
    new_board = list(board)
    new_board[index] = current_player
    next_player = "O" if current_player == "X" else "X"
    return new_board, next_player, True

board = [""] * 9
board, player, moved = attempt_move_pure(board, 0, "X", False)
print(board, player, moved)''')
    nb.md("## Задание ★★ Самостоятельная задача — занятая клетка не переключает игрока")
    nb.code('''board_occupied = ["X"] + [""] * 8
board2, player2, moved2 = attempt_move_pure(board_occupied, 0, "O", False)

assert moved2 is False
assert player2 == "O", "невалидный ход не должен переключать игрока"
assert board2 == board_occupied, "невалидный ход не должен менять поле"
print("Невалидный ход корректно отклонён.")''')
    nb.write(OUT_DIR / "17-15-algoritm-hoda.ipynb")
    print(f"Записано: 17-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-16", "Восемь выигрышных линий", "17-16-vosem-linij-pobedy.html"))
    nb.md("## Цель\n\nПроверить find_winner() на всех восьми линиях для X и для O.")
    nb.md("## Рабочий пример")
    nb.code('''WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

def find_winner(board):
    for a, b, c in WINNING_LINES:
        mark = board[a]
        if mark and mark == board[b] == board[c]:
            return mark, (a, b, c)
    return None, None

doska = ["X", "X", "X", "", "O", "O", "", "", ""]
print(find_winner(doska))''')
    nb.md("## Проверка результата — все восемь линий, оба игрока")
    nb.code('''def board_for_line(line, mark):
    board = [""] * 9
    for i in line:
        board[i] = mark
    return board

vse_linii_ok = True
for mark in ("X", "O"):
    for line in WINNING_LINES:
        winner, winning_line = find_winner(board_for_line(line, mark))
        if winner != mark or set(winning_line) != set(line):
            vse_linii_ok = False

assert vse_linii_ok is True
assert find_winner([""] * 9) == (None, None)
print("Все восемь линий верны для X и O.")''')
    nb.write(OUT_DIR / "17-16-vosem-linij-pobedy.ipynb")
    print(f"Записано: 17-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-17", "Победа, ничья и terminal state", "17-17-pobeda-nichya-terminal.html"))
    nb.md("## Цель\n\nУбедиться, что победа на последнем ходу не превращается в ложную ничью.")
    nb.md("## Рабочий пример")
    nb.code('''WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

def find_winner(board):
    for a, b, c in WINNING_LINES:
        mark = board[a]
        if mark and mark == board[b] == board[c]:
            return mark, (a, b, c)
    return None, None

def is_draw(board):
    winner, _ = find_winner(board)
    return winner is None and all(board)

nichya = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
print("Ничья:", is_draw(nichya))''')
    nb.md("## Задание ★★ Самостоятельная задача — победа побеждает ничью")
    nb.code('''# Поле полностью заполнено, И последний ход выигрывает диагональ 0-4-8
posledny_hod_pobeda = ["X", "O", "O",
                        "O", "X", "X",
                        "O", "X", "X"]

winner, line = find_winner(posledny_hod_pobeda)
assert winner == "X"
assert set(line) == {0, 4, 8}
assert is_draw(posledny_hod_pobeda) is False, "победа на последнем ходу — это НЕ ничья"
print("Порядок проверки верный: победа обнаружена раньше ничьей.")''')
    nb.write(OUT_DIR / "17-17-pobeda-nichya-terminal.ipynb")
    print(f"Записано: 17-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-18", "От widgets-as-state к board model", "17-18-model-a-ne-widgets.html"))
    nb.md("## Цель\n\nНа игрушечной модели виджета показать, почему button.text как единственный источник "
          "состояния ломается при наведении-превью.")
    nb.md("## Рабочий пример — виджет как (неудачный) источник состояния")
    nb.code('''class FakeButton:
    """Достаточно правил игрушечной кнопки, чтобы показать проблему — не настоящий Tkinter."""
    def __init__(self):
        self.text = ""

fake_buttons = [FakeButton() for _ in range(9)]

def hover_preview_broken(buttons, index, player):
    buttons[index].text = player  # naive: превью пишет ПРЯМО в "состояние"

def find_winner_from_widgets(buttons):
    board = [b.text for b in buttons]
    return board.count("X") >= 3  # упрощённая проверка для примера

hover_preview_broken(fake_buttons, 0, "X")
hover_preview_broken(fake_buttons, 1, "X")
hover_preview_broken(fake_buttons, 2, "X")
print("Победа определена ТОЛЬКО наведением мыши:", find_winner_from_widgets(fake_buttons))
# Ни одного клика не было — а "победа" уже "найдена". Это и есть архитектурная ошибка.''')
    nb.md("## Задание ★★ Самостоятельная задача — модель как источник истины")
    nb.code('''board_model = [""] * 9

def hover_preview_correct(buttons, model, index, player):
    if model[index]:
        return
    buttons[index].text = player  # виджет меняется — модель НЕТ

fresh_buttons = [FakeButton() for _ in range(9)]
hover_preview_correct(fresh_buttons, board_model, 0, "X")

assert fresh_buttons[0].text == "X", "виджет должен показать превью"
assert board_model[0] == "", "модель обязана остаться нетронутой при простом наведении"
print("Модель не изменилась при наведении — именно так и должно быть.")''')
    nb.write(OUT_DIR / "17-18-model-a-ne-widgets.ipynb")
    print(f"Записано: 17-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-19", "GameState с dataclass", "17-19-gamestate-dataclass.html"))
    nb.md("## Цель\n\nСобрать GameState как @dataclass и проверить, что board НЕ расшаривается между экземплярами.")
    nb.md("## Рабочий пример")
    nb.code('''from dataclasses import dataclass, field

@dataclass
class GameState:
    board: list[str] = field(default_factory=lambda: [""] * 9)
    current_player: str = "X"
    game_over: bool = False
    winner: str | None = None
    winning_line: tuple[int, int, int] | None = None
    score_x: int = 0
    score_o: int = 0

s1 = GameState()
s2 = GameState()
print(s1)''')
    nb.md("## Задание ★★ Самостоятельная задача — независимость экземпляров")
    nb.code('''s1.board[0] = "X"

assert s1.board[0] == "X"
assert s2.board[0] == "", "изменение board у s1 НЕ должно быть видно в s2 (field(default_factory=...))"
assert s1.current_player == "X" and s2.current_player == "X"
print("s1 и s2 — полностью независимые экземпляры GameState.")''')
    nb.write(OUT_DIR / "17-19-gamestate-dataclass.ipynb")
    print(f"Записано: 17-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-20", "Архитектура TicTacToeApp", "17-20-arhitektura-app.html"))
    nb.md("## Цель\n\nСобрать минимальный объектный граф app.root / app.state и убедиться, что домен и UI разделены.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk
from dataclasses import dataclass, field

@dataclass
class GameState:
    board: list[str] = field(default_factory=lambda: [""] * 9)
    current_player: str = "X"

class TicTacToeApp:
    def __init__(self, root):
        self.root = root          # app HAS-A root — не наследование от tk.Tk
        self.state = GameState()  # app HAS-A state
        self.buttons = []

root = tk.Tk()
app = TicTacToeApp(root)
print("app.root — это Tk:", isinstance(app.root, tk.Tk))
print("app.state — это GameState:", isinstance(app.state, GameState))
root.update()
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте методу build_board(self) создание девяти tk.Button и убедитесь, что "
          "len(self.buttons) == 9 после его вызова.")
    nb.write(OUT_DIR / "17-20-arhitektura-app.ipynb")
    print(f"Записано: 17-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-21", "Адаптивное игровое поле", "17-21-adaptivnoe-pole.html"))
    nb.md("## Цель\n\nСобрать поле 3×3 через grid() с sticky и weight, чтобы оно адаптировалось к размеру окна.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()
board_frame = ttk.Frame(root)
board_frame.pack(fill="both", expand=True)

for i in range(3):
    board_frame.rowconfigure(i, weight=1)
    board_frame.columnconfigure(i, weight=1)

buttons = []
for index in range(9):
    btn = tk.Button(board_frame, text="", width=3, height=1)
    btn.grid(row=index // 3, column=index % 3, sticky="nsew", padx=3, pady=3)
    buttons.append(btn)

root.update()
print("Клеток создано:", len(buttons))
print("weight столбца 0:", board_frame.grid_columnconfigure(0)["weight"])
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что `sticky=\"nsew\"` задан у всех девяти клеток через "
          "`btn.grid_info()[\"sticky\"]`.")
    nb.write(OUT_DIR / "17-21-adaptivnoe-pole.ipynb")
    print(f"Записано: 17-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-22", "Визуальный стиль X/O", "17-22-vizualnyj-stil.html"))
    nb.md("## Цель\n\nПокрасить X в фиолетовый, O — в розовый через прямой fg= у tk.Button.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

MARK_COLOR = {"X": "#5B24F9", "O": "#DB2777"}

root = tk.Tk()
btn = tk.Button(root, text="X", fg=MARK_COLOR["X"], font=("Arial", 24, "bold"))
btn.pack()
root.update()
print("Цвет X:", btn.cget("fg"))

btn.config(text="O", fg=MARK_COLOR["O"])
root.update()
print("Цвет O:", btn.cget("fg"))
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоберите три кнопки: с X, с O и пустую — и проверьте, что "
          "MARK_COLOR.get(text, \"#0D0230\") даёт нейтральный цвет для пустой клетки.")
    nb.write(OUT_DIR / "17-22-vizualnyj-stil.ipynb")
    print(f"Записано: 17-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-23", "Hover preview через bind()", "17-23-hover-preview.html"))
    nb.md("## Цель\n\nСобрать hover-превью на реальной кнопке и доказать, что модель не меняется.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
board = [""] * 9
btn = tk.Button(root, text="")
btn.pack()

def on_enter(_event, index=4):
    if board[index]:
        return
    btn.config(text="X", fg="#B9A0FC")

def on_leave(_event, index=4):
    btn.config(text=board[index], fg="#0D0230")

btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)
root.update()

btn.event_generate("<Enter>")
root.update()
print("Во время наведения — текст кнопки:", btn.cget("text"), " модель:", board[4])

btn.event_generate("<Leave>")
root.update()
print("После ухода курсора — текст кнопки:", repr(btn.cget("text")), " модель:", repr(board[4]))
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте, что наведение на клетку, где `board[index]` уже не пустое, "
          "НЕ переписывает существующую отметку.")
    nb.write(OUT_DIR / "17-23-hover-preview.ipynb")
    print(f"Записано: 17-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-24", "Управление клавиатурой", "17-24-upravlenie-klaviaturoj.html"))
    nb.md("## Цель\n\nПоказать, что клавиша '1'..'9' ведёт в ТОТ ЖЕ attempt_move(), что и клик мышью.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
board = [""] * 9
current_player = ["X"]
moves_log = []

def attempt_move(index):
    if board[index]:
        return
    board[index] = current_player[0]
    moves_log.append(index)
    current_player[0] = "O" if current_player[0] == "X" else "X"

def on_key(event):
    if event.char and event.char.isdigit():
        n = int(event.char)
        if 1 <= n <= 9:
            attempt_move(n - 1)

root.bind("<Key>", on_key)
root.update()

root.event_generate("<Key>", keysym="3")
root.update()
print("board после клавиши '3':", board)
print("Ход записан в тот же moves_log:", moves_log)
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что клавиша `0` (вне диапазона 1-9) не вызывает `attempt_move()`.")
    nb.write(OUT_DIR / "17-24-upravlenie-klaviaturoj.ipynb")
    print(f"Записано: 17-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-25", "Подсветка выигрышной линии", "17-25-podsvetka-linii.html"))
    nb.md("## Цель\n\nПодсветить ИМЕННО победную линию, а не любые совпавшие символы на поле.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

WIN_BG = "#D1FAE5"
NEUTRAL_BG = "#FAFAFC"

root = tk.Tk()
board = ["X", "X", "X", "X", "", "", "", "", ""]  # верхняя строка ПОБЕДНАЯ, четвёртый X — нет
winning_line = (0, 1, 2)

buttons = [tk.Button(root, text=board[i]) for i in range(9)]
for i, btn in enumerate(buttons):
    btn.config(bg=WIN_BG if i in winning_line else NEUTRAL_BG)
root.update()

for i in (0, 1, 2, 3):
    print(i, buttons[i].cget("bg") == WIN_BG)
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nУбедитесь, что клетка 3 (тоже 'X', но не часть `winning_line`) "
          "НЕ подсвечена — используйте `bg` кнопки для проверки.")
    nb.write(OUT_DIR / "17-25-podsvetka-linii.ipynb")
    print(f"Записано: 17-25 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-26", "Счёт матчей", "17-26-schyot-matchej.html"))
    nb.md("## Цель\n\nОбновлять счёт матча чистой функцией — по одному разу за партию.")
    nb.md("## Рабочий пример")
    nb.code('''def apply_round_result(scores, winner):
    """scores: {'x': int, 'o': int, 'draws': int}. winner: 'X' | 'O' | None."""
    scores = dict(scores)
    if winner == "X":
        scores["x"] += 1
    elif winner == "O":
        scores["o"] += 1
    else:
        scores["draws"] += 1
    return scores

scores = {"x": 0, "o": 0, "draws": 0}
scores = apply_round_result(scores, "X")
print(scores)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''scores2 = {"x": 0, "o": 0, "draws": 0}
scores2 = apply_round_result(scores2, "X")
scores2 = apply_round_result(scores2, "O")
scores2 = apply_round_result(scores2, None)  # ничья

assert scores2 == {"x": 1, "o": 1, "draws": 1}
print("Счёт обновляется верно для победы X, победы O и ничьей.")''')
    nb.write(OUT_DIR / "17-26-schyot-matchej.ipynb")
    print(f"Записано: 17-26 ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-27", "New Round vs New Match", "17-27-new-round-vs-new-match.html"))
    nb.md("## Цель\n\nРазличить сброс раунда (счёт сохраняется) и сброс матча (счёт обнуляется), и сохранить счёт в JSON.")
    nb.md("## Рабочий пример")
    nb.code('''def new_round(state):
    state = dict(state)
    state["board"] = [""] * 9
    state["current_player"] = "X"
    state["game_over"] = False
    return state

def new_match(state):
    state = new_round(state)
    state["score_x"] = 0
    state["score_o"] = 0
    state["draws"] = 0
    return state

state = {"board": ["X"] * 9, "current_player": "O", "game_over": True, "score_x": 3, "score_o": 1, "draws": 0}
after_round = new_round(state)
print("После New Round — счёт сохранён:", after_round["score_x"], after_round["score_o"])''')
    nb.md("## Задание ★ Базовая практика — New Round сохраняет счёт, New Match обнуляет")
    nb.code('''after_match = new_match(state)

assert after_round["score_x"] == 3 and after_round["score_o"] == 1, "New Round обязан сохранить счёт"
assert after_match["score_x"] == 0 and after_match["score_o"] == 0, "New Match обязан обнулить счёт"
print("New Round и New Match ведут себя по-разному, как и должны.")''')
    nb.md("## Необязательное расширение — сохранение счёта в JSON (виртуальная файловая система браузера)")
    nb.code('''import json
from pathlib import Path

SCORES_PATH = Path("tic_tac_toe_scores_practice.json")
SCORES_PATH.write_text(json.dumps({"x": 3, "o": 1, "draws": 0}), encoding="utf-8")

loaded = json.loads(SCORES_PATH.read_text(encoding="utf-8"))
assert loaded == {"x": 3, "o": 1, "draws": 0}
print("Счёт успешно сохранён и прочитан обратно:", loaded)''')
    nb.write(OUT_DIR / "17-27-new-round-vs-new-match.ipynb")
    print(f"Записано: 17-27 ({len(nb)} ячеек)")


def build_28() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-28", "Тестируем игру без Tkinter", "17-28-testiruem-bez-tkinter.html"))
    nb.md("## Цель\n\nПрогнать полную регрессионную матрицу игровой логики — без единого открытого окна.")
    nb.md("## Рабочий пример")
    nb.code('''WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

def find_winner(board):
    for a, b, c in WINNING_LINES:
        mark = board[a]
        if mark and mark == board[b] == board[c]:
            return mark, (a, b, c)
    return None, None

def is_draw(board):
    winner, _ = find_winner(board)
    return winner is None and all(board)

def board_for_line(line, mark):
    board = [""] * 9
    for i in line:
        board[i] = mark
    return board

print("8 линий × 2 игрока — проверяем ниже")''')
    nb.md("## Проверка результата — полная матрица")
    nb.code('''all_lines_ok = True
for mark in ("X", "O"):
    for line in WINNING_LINES:
        winner, winning_line = find_winner(board_for_line(line, mark))
        if winner != mark or set(winning_line) != set(line):
            all_lines_ok = False

draw_board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
draw_ok = is_draw(draw_board) is True and find_winner(draw_board) == (None, None)

last_move_board = ["X", "O", "O", "O", "X", "X", "O", "X", "X"]
last_move_winner, last_move_line = find_winner(last_move_board)
last_move_ok = last_move_winner == "X" and set(last_move_line) == {0, 4, 8} and is_draw(last_move_board) is False

empty_ok = find_winner([""] * 9) == (None, None)

assert all_lines_ok is True
assert draw_ok is True
assert last_move_ok is True
assert empty_ok is True
print("Вся регрессионная матрица игровой логики пройдена — без единого открытого окна.")''')
    nb.write(OUT_DIR / "17-28-testiruem-bez-tkinter.ipynb")
    print(f"Записано: 17-28 ({len(nb)} ячеек)")


def build_29() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-29", "Debug Labs", "17-29-debug-labs.html"))
    nb.md("## Цель\n\nНайти баг по симптому: неправильный порядок проверки победы/ничьей.")
    nb.md("## Сломанный код — ничья проверяется раньше победы")
    nb.code('''def find_winner_ok(board):
    lines = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for a, b, c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def status_broken(board):
    if all(board):
        return "Ничья!"
    winner = find_winner_ok(board)
    if winner:
        return f"Победил игрок {winner}!"
    return "Игра продолжается"

# 9-й ход заполняет поле И выигрывает диагональ — но сломанный код проверяет ничью первой
posledny_hod = ["O", "O", "X", "O", "X", "O", "X", "O", "X"]
print("Сломанный результат:", status_broken(posledny_hod))  # неверно покажет "Ничья!"''', raises=False)
    nb.md("## Задание ★★ Самостоятельная задача — исправление")
    nb.code('''def status_fixed(board):
    winner = find_winner_ok(board)
    if winner:
        return f"Победил игрок {winner}!"
    if all(board):
        return "Ничья!"
    return "Игра продолжается"

assert status_broken(posledny_hod) == "Ничья!", "так ведёт себя СЛОМАННАЯ версия"
assert status_fixed(posledny_hod) != "Ничья!", "исправленная версия обязана найти победителя"
assert "Победил" in status_fixed(posledny_hod)
print("status_fixed() находит победителя там, где status_broken() ошибочно объявляет ничью.")''')
    nb.write(OUT_DIR / "17-29-debug-labs.ipynb")
    print(f"Записано: 17-29 ({len(nb)} ячеек)")


def build_30() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-30", "Visual effects и after()", "17-30-visual-effects-after.html"))
    nb.md("## Цель\n\nСобрать короткую неблокирующую анимацию победной линии через self-rescheduling after().")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
buttons = [tk.Button(root, text="X") for _ in range(3)]
for b in buttons:
    b.pack(side="left")

ticks_seen = []

def pulse(tick=0):
    ticks_seen.append(tick)
    color = "#6EE7B7" if tick % 2 == 0 else "#D1FAE5"
    for b in buttons:
        b.config(bg=color)
    if tick < 3:
        root.after(10, pulse, tick + 1)

pulse()
root.update()
root.after(80, root.quit)
root.mainloop()

print("Тиков анимации:", ticks_seen)
root.destroy()''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте `cancel_pulse()`, который вызывает `root.after_cancel(job_id)`, "
          "и проверьте, что после отмены анимация не продолжается.")
    nb.write(OUT_DIR / "17-30-visual-effects-after.ipynb")
    print(f"Записано: 17-30 ({len(nb)} ячеек)")


def build_31() -> None:
    nb = NotebookBuilder()
    nb.md(_lesson_link("17-31", "Tic-Tac-Toe Pro — итоги главы", "17-31-tic-tac-toe-pro-itogi.html"))
    nb.md("## Цель\n\nЗапустить финальную версию игры целиком и пройти её чек-лист — тот же код, что и в "
          "`projects/tkinter/tic-tac-toe/tic_tac_toe.py`.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Полная финальная игра — импортируем и проверяем")
    nb.code('''import sys
sys.path.insert(0, "../../projects/tkinter/tic-tac-toe")  # только для локального запуска этого ноутбука

import tkinter as tk
import tic_tac_toe as t

root = tk.Tk()
app = t.TicTacToeApp(root)
root.update()
print("Игра построена, клеток:", len(app.buttons))''')
    nb.md("## Проверка результата — полный чек-лист")
    nb.code('''# X выигрывает верхнюю строку
for i in (0, 3, 1, 4, 2):
    app.attempt_move(i)

assert app.state.game_over is True
assert app.state.winner == "X"
assert app.state.winning_line == (0, 1, 2)
assert app.state.score_x == 1

# ход после конца игры игнорируется
app.attempt_move(5)
assert app.state.board[5] == ""

# New Round сохраняет счёт, New Match обнуляет
app.new_round()
assert app.state.score_x == 1
app.new_match()
assert app.state.score_x == 0

print("Чек-лист готовой игры пройден: модель, правила, счёт, сброс — всё работает вместе.")
root.destroy()''')
    nb.write(OUT_DIR / "17-31-tic-tac-toe-pro-itogi.ipynb")
    print(f"Записано: 17-31 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_03()
    build_04()
    build_05()
    build_06()
    build_07()
    build_08()
    build_09()
    build_10()
    build_11()
    build_12()
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_22()
    build_23()
    build_24()
    build_25()
    build_26()
    build_27()
    build_28()
    build_29()
    build_30()
    build_31()
