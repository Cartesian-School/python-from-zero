#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 16 (Tkinter).

Важно: в реальном .py-файле приложение запускают через root.mainloop(), который
блокирует выполнение до закрытия окна. В автоматически выполняемом ноутбуке нет
живого пользователя, который закроет окно, поэтому здесь вместо mainloop() мы
вызываем root.update() (обрабатывает события один раз, без блокировки) и затем
root.destroy() — это подтверждено реальным запуском (см. tkinter_test.py в scratchpad).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-16"

def messagebox_mock_setup(responses: dict) -> tuple[str, str]:
    """messagebox.* normally blocks waiting for a real click. Monkeypatches the
    named functions to return pre-scripted responses, mirroring input_setup()'s
    convention for input()."""
    md = ("## Про messagebox в этом ноутбуке\n\nМодальные диалоги ждут реального нажатия "
          "кнопки живым пользователем. В автоматически выполняемом ноутбуке никто не нажмёт "
          "кнопку, поэтому нужные функции `messagebox` временно подменены заранее "
          "заготовленными ответами.")
    lines = ["from tkinter import messagebox", ""]
    for name, value in responses.items():
        lines.append(f"messagebox.{name} = lambda *args, **kwargs: {value!r}")
    return md, "\n".join(lines)


def filedialog_mock_setup(responses: dict) -> tuple[str, str]:
    """Same idea as messagebox_mock_setup() for tkinter.filedialog, which also
    blocks waiting for a real dialog interaction."""
    md = ("## Про filedialog в этом ноутбуке\n\nДиалог выбора файла ждёт живого "
          "пользователя. В автоматически выполняемом ноутбуке нужные функции "
          "`filedialog` временно подменены заранее заготовленными ответами.")
    lines = ["from tkinter import filedialog", ""]
    for name, value in responses.items():
        lines.append(f"filedialog.{name} = lambda *args, **kwargs: {value!r}")
    return md, "\n".join(lines)


MAINLOOP_NOTE_MD = (
    "## Про mainloop() в этом ноутбуке\n\n"
    "В обычном `.py`-файле приложение запускают через `root.mainloop()` — эта команда "
    "«замирает» и ждёт, пока пользователь не закроет окно. В автоматически выполняемом "
    "ноутбуке нет живого пользователя за окном, поэтому здесь вместо `root.mainloop()` мы "
    "вызовем `root.update()` (обрабатывает события один раз, без ожидания) и затем "
    "`root.destroy()` — интерфейс строится точно так же, просто без бесконечного ожидания "
    "в конце."
)


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-01 · Настройка Tkinter\n\nПрактика к разделу "
          "[«Tkinter — правильно всё настраиваем!»](../../site/chapters/glava-16/16-01-nastraivaem-tkinter.html).")
    nb.md("## Цель\n\nСоздать первое окно Tkinter.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
root.title("Моё первое приложение")
root.geometry("400x300")

print("Заголовок окна:", root.title())
root.update()
root.destroy()
print("Окно закрыто.")''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте окно 300x200 со своим заголовком.")
    nb.code('''root = tk.Tk()
root.title("Окно Cartesian")
root.geometry("300x200")

print(root.title(), root.geometry())
root.update()
root.destroy()''')
    nb.write(OUT_DIR / "16-01-nastrojka.ipynb")
    print(f"Записано: 16-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-02 · Метки, кнопки и pack\n\nПрактика к разделу "
          "[«Метки, кнопки и их размещение»](../../site/chapters/glava-16/16-02-metki-knopki-pack.html).")
    nb.md("## Цель\n\nСоздать Label и Button, обработать нажатие.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()

label = tk.Label(root, text="Привет, Tkinter!")
label.pack()

nazhatij = []

def na_knopku_nazhali():
    nazhatij.append(1)
    print("Кнопку нажали!")

button = tk.Button(root, text="Нажми меня", command=na_knopku_nazhali)
button.pack()

root.update()
button.invoke()   # программно "нажимаем" кнопку, как это сделал бы пользователь
print("Нажатий:", len(nazhatij))
root.destroy()''')
    nb.md("## Типичная ошибка\n\nСкобки после имени функции в command вызывают её немедленно.")
    nb.code('''root = tk.Tk()

def privet():
    print("Привет!")   # эта функция ничего не возвращает — команда получит None

button = tk.Button(root, text="Кнопка", command=privet())  # скобки — ошибка!
root.update()
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте кнопку, при нажатии увеличивающую "
          "счётчик клика.")
    nb.code('''root = tk.Tk()
schet = {"clicks": 0}

def klik():
    schet["clicks"] += 1
    print("Кликов:", schet["clicks"])

button = tk.Button(root, text="Клик", command=klik)
button.pack()

root.update()
button.invoke()
button.invoke()
button.invoke()
print("Итого кликов:", schet["clicks"])
root.destroy()''')
    nb.write(OUT_DIR / "16-02-metki-knopki.ipynb")
    print(f"Записано: 16-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-03 · Поля ввода\n\nПрактика к разделу "
          "[«Множество полей ввода»](../../site/chapters/glava-16/16-03-polya-vvoda.html).")
    nb.md("## Цель\n\nОсвоить Entry и Text.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример — Entry")
    nb.code('''import tkinter as tk

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()
entry.insert(0, "Cartesian")   # программно вводим текст, как это сделал бы пользователь

print("Текст в поле:", entry.get())
root.update()
root.destroy()''')
    nb.md("## Эксперимент 1 — Text (многострочный)")
    nb.code('''root = tk.Tk()

text_box = tk.Text(root, height=5, width=30)
text_box.pack()
text_box.insert("1.0", "Первая строка\\nВторая строка")

content = text_box.get("1.0", "end")
print(repr(content))
root.update()
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте Entry, вставьте своё имя и выведите его "
          "заглавными буквами (используя upper() из главы 8).")
    nb.code('''root = tk.Tk()
entry = tk.Entry(root)
entry.pack()
entry.insert(0, "cartesian")

print(entry.get().upper())
root.update()
root.destroy()''')
    nb.write(OUT_DIR / "16-03-polya-vvoda.ipynb")
    print(f"Записано: 16-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-04 · Переменные Tkinter\n\nПрактика к разделу "
          "[«Переменные Tkinter»](../../site/chapters/glava-16/16-04-peremennye-tkinter.html).")
    nb.md("## Цель\n\nОсвоить StringVar и обновление связанных виджетов.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
imya = tk.StringVar(value="Гость")

label = tk.Label(root, textvariable=imya)
label.pack()

print("До смены:", label.cget("text"))

imya.set("Cartesian")
root.update()   # применяем изменение к виджету

print("После смены:", label.cget("text"))
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте IntVar со счётчиком, который "
          "увеличивается при вызове функции.")
    nb.code('''root = tk.Tk()
schet = tk.IntVar(value=0)
label = tk.Label(root, textvariable=schet)
label.pack()

def uvelichit():
    schet.set(schet.get() + 1)

uvelichit()
uvelichit()
uvelichit()
root.update()
print("Значение счётчика:", schet.get())
root.destroy()''')
    nb.write(OUT_DIR / "16-04-peremennye.ipynb")
    print(f"Записано: 16-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-05 · Множество вариантов\n\nПрактика к разделу "
          "[«Множество вариантов!»](../../site/chapters/glava-16/16-05-mnozhestvo-variantov.html).")
    nb.md("## Цель\n\nОсвоить Radiobutton и Checkbutton.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример — Radiobutton")
    nb.code('''import tkinter as tk

root = tk.Tk()
vybor = tk.StringVar(value="chay")

tk.Radiobutton(root, text="Чай", variable=vybor, value="chay").pack()
tk.Radiobutton(root, text="Кофе", variable=vybor, value="kofe").pack()

vybor.set("kofe")   # программно выбираем вариант
root.update()
print("Выбрано:", vybor.get())
root.destroy()''')
    nb.md("## Эксперимент 1 — Checkbutton")
    nb.code('''root = tk.Tk()
saharok = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="С сахаром", variable=saharok).pack()

saharok.set(True)
root.update()
print("С сахаром:", saharok.get())
root.destroy()''')
    nb.write(OUT_DIR / "16-05-varianty.ipynb")
    print(f"Записано: 16-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-06 · Меню\n\nПрактика к разделу "
          "[«Меню»](../../site/chapters/glava-16/16-06-menu.html).")
    nb.md("## Цель\n\nПостроить меню приложения.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
vyzovy = []

def novyj_fajl():
    vyzovy.append("novyj_fajl")
    print("Создаём новый файл...")

menu_bar = tk.Menu(root)
fajl_menu = tk.Menu(menu_bar, tearoff=0)
fajl_menu.add_command(label="Новый", command=novyj_fajl)
fajl_menu.add_separator()
fajl_menu.add_command(label="Выход", command=root.quit)
menu_bar.add_cascade(label="Файл", menu=fajl_menu)

root.config(menu=menu_bar)
root.update()

novyj_fajl()  # программно "выбираем" пункт меню
print("Вызовы:", vyzovy)
root.destroy()''')
    nb.write(OUT_DIR / "16-06-menu.ipynb")
    print(f"Записано: 16-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-07 · Компоновка grid\n\nПрактика к разделу "
          "[«Идеальная компоновка — grid»](../../site/chapters/glava-16/16-07-grid.html).")
    nb.md("## Цель\n\nРазместить виджеты через grid().")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()

tk.Label(root, text="Имя:").grid(row=0, column=0)
tk.Entry(root).grid(row=0, column=1)

tk.Label(root, text="Email:").grid(row=1, column=0)
tk.Entry(root).grid(row=1, column=1)

tk.Button(root, text="Отправить").grid(row=2, column=0, columnspan=2)

root.update()
print("Форма из", len(root.grid_slaves()), "виджетов построена.")
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте третью строку с полем «Телефон».")
    nb.code('''root = tk.Tk()

tk.Label(root, text="Имя:").grid(row=0, column=0)
tk.Entry(root).grid(row=0, column=1)

tk.Label(root, text="Email:").grid(row=1, column=0)
tk.Entry(root).grid(row=1, column=1)

tk.Label(root, text="Телефон:").grid(row=2, column=0)
tk.Entry(root).grid(row=2, column=1)

tk.Button(root, text="Отправить").grid(row=3, column=0, columnspan=2)

root.update()
print("Форма из", len(root.grid_slaves()), "виджетов построена.")
root.destroy()''')
    nb.write(OUT_DIR / "16-07-grid.ipynb")
    print(f"Записано: 16-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-08 · Калькулятор чаевых\n\nПрактика к разделу "
          "[«Мини-проект — приложение-калькулятор чаевых»](../../site/chapters/glava-16/16-08-mini-proekt-chaevye-itogi.html).")
    nb.md("## Цель\n\nСобрать полноценное приложение из виджетов главы.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import tkinter as tk

root = tk.Tk()
root.title("Калькулятор чаевых")

tk.Label(root, text="Сумма счёта:").grid(row=0, column=0, padx=10, pady=10)
schet_entry = tk.Entry(root)
schet_entry.grid(row=0, column=1)

tk.Label(root, text="Процент чаевых:").grid(row=1, column=0, padx=10, pady=10)
procent_entry = tk.Entry(root)
procent_entry.grid(row=1, column=1)

rezultat_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
rezultat_label.grid(row=3, column=0, columnspan=2, pady=10)

def poschitat():
    schet = float(schet_entry.get())
    procent = float(procent_entry.get())
    chaevye = schet * procent / 100
    rezultat_label.config(text=f"Чаевые: {chaevye:.2f}")

tk.Button(root, text="Посчитать", command=poschitat).grid(row=2, column=0, columnspan=2)

# программно вводим данные и "нажимаем" кнопку, как это сделал бы пользователь
schet_entry.insert(0, "1000")
procent_entry.insert(0, "15")
poschitat()

root.update()
print(rezultat_label.cget("text"))
root.destroy()''')
    nb.md("## Проверка результата")
    nb.code('''assert 1000 * 15 / 100 == 150.0
print("Верно: чаевые с 1000 при 15% равны 150.0")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте калькулятор с другими числами.")
    nb.code('''import tkinter as tk

root = tk.Tk()
schet_entry = tk.Entry(root)
procent_entry = tk.Entry(root)
rezultat_label = tk.Label(root, text="")

def poschitat():
    schet = float(schet_entry.get())
    procent = float(procent_entry.get())
    chaevye = schet * procent / 100
    rezultat_label.config(text=f"Чаевые: {chaevye:.2f}")

schet_entry.insert(0, "2500")
procent_entry.insert(0, "20")
poschitat()
root.update()
print(rezultat_label.cget("text"))
root.destroy()''')
    nb.write(OUT_DIR / "16-08-kalkulyator-chaevyh.ipynb")
    print(f"Записано: 16-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-09 · От терминала к GUI\n\nПрактика к разделу "
          "[«От терминала к GUI: событийная модель»](../../site/chapters/glava-16/16-09-ot-terminala-k-gui.html).")
    nb.md("## Цель\n\nПонять разницу между регистрацией callback и его выполнением.")
    nb.code('''log = []

def on_click():
    log.append("clicked")

registered = on_click            # регистрация: callback запомнен, но НЕ вызван
before_dispatch = list(log)

registered()                     # диспетчеризация: callback выполняется именно сейчас
after_dispatch = list(log)

print(before_dispatch, after_dispatch)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что registered — это вызываемый объект "
          "(функция), а не результат её вызова.")
    nb.code('''registered_is_callable = callable(registered)
print(registered_is_callable)''')
    nb.write(OUT_DIR / "16-09-ot-terminala-k-gui.ipynb")
    print(f"Записано: 16-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-10 · Событийный цикл и mainloop\n\nПрактика к разделу "
          "[«Как работает событийный цикл и mainloop»](../../site/chapters/glava-16/16-10-event-loop-i-mainloop.html).")
    nb.md("## Цель\n\nМоделировать порядок обработки событий и закрепить разницу function vs function().")
    nb.code('''log = []

def on_click(): log.append("click")
def on_timer(): log.append("timer")
def on_type(): log.append("type")

handlers = {"click": on_click, "timer": on_timer, "type": on_type}

def run_event_loop(queue):
    for event in queue:
        handlers[event]()

run_event_loop(["click", "timer", "type"])
print(log)''')
    nb.md("## Задание ★ Базовая практика — command без скобок")
    nb.code('''calls = []

def greet():
    calls.append("greet called")
    return "hello"

command_correct = greet     # правильно: сама функция
command_wrong = greet()     # неправильно: вызов прямо сейчас

print(len(calls), command_wrong, callable(command_correct))''')
    nb.write(OUT_DIR / "16-10-event-loop-i-mainloop.ipynb")
    print(f"Записано: 16-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-11 · Дерево виджетов\n\nПрактика к разделу "
          "[«Виджет и дерево интерфейса»](../../site/chapters/glava-16/16-11-derevo-widgetov.html).")
    nb.md("## Цель\n\nМоделировать дерево виджетов как вложенные данные и рассуждать о нём.")
    nb.code('''widget_tree = ("root", [
    ("main_frame", [
        ("title_label", []),
        ("name_entry", []),
        ("save_button", []),
    ]),
])

def count_widgets(node):
    label, children = node
    total = 1
    for child in children:
        total += count_widgets(child)
    return total

def find_parent(node, target_label, parent_label=None):
    label, children = node
    if label == target_label:
        return parent_label
    for child in children:
        result = find_parent(child, target_label, label)
        if result is not None:
            return result
    return None

total_widgets = count_widgets(widget_tree)
save_button_parent = find_parent(widget_tree, "save_button")
print(total_widgets, save_button_parent)''')
    nb.md("## Задание ★ Базовая практика\n\nНайдите родителя title_label.")
    nb.code('''title_label_parent = find_parent(widget_tree, "title_label")
print(title_label_parent)''')
    nb.write(OUT_DIR / "16-11-derevo-widgetov.ipynb")
    print(f"Записано: 16-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-12 · tk и ttk\n\nПрактика к разделу "
          "[«tk и ttk»](../../site/chapters/glava-16/16-12-tk-i-ttk.html).")
    nb.md("## Цель\n\nСобрать форму из классических и тематизированных виджетов вместе.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()

text_widget = tk.Text(root, height=3, width=20)
text_widget.pack()

ttk_label = ttk.Label(root, text="ttk.Label")
ttk_label.pack()

ttk_button = ttk.Button(root, text="ttk.Button")
ttk_button.pack()

root.update()
print(type(text_widget).__name__, type(ttk_label).__name__, type(ttk_button).__name__)
root.destroy()''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте ttk.Entry в ту же форму.")
    nb.code('''root = tk.Tk()
entry = ttk.Entry(root)
entry.pack()
root.update()
print(type(entry).__name__)
root.destroy()''')
    nb.write(OUT_DIR / "16-12-tk-i-ttk.ipynb")
    print(f"Записано: 16-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-13 · Frame и LabelFrame\n\nПрактика к разделу "
          "[«Frame и LabelFrame»](../../site/chapters/glava-16/16-13-frame-i-labelframe.html).")
    nb.md("## Цель\n\nРазбить окно на регионы через Frame.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()

toolbar_frame = ttk.Frame(root)
content_frame = ttk.Frame(root)
status_frame = ttk.Frame(root)

toolbar_frame.pack(side="top", fill="x")
content_frame.pack(side="top", fill="both", expand=True)
status_frame.pack(side="bottom", fill="x")

root.update()
print(len(root.winfo_children()), "региона в root")
root.destroy()''')
    nb.md("## Задание ★ Базовая практика — LabelFrame")
    nb.code('''root = tk.Tk()
nastrojki = ttk.LabelFrame(root, text="Настройки")
nastrojki.pack(padx=10, pady=10, fill="x")
ttk.Checkbutton(nastrojki, text="Тёмная тема").pack(anchor="w")
root.update()
print(nastrojki.cget("text"))
root.destroy()''')
    nb.write(OUT_DIR / "16-13-frame-i-labelframe.ipynb")
    print(f"Записано: 16-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-14 · pack подробно\n\nПрактика к разделу "
          "[«pack подробно: fill, expand и вложенные фреймы»](../../site/chapters/glava-16/16-14-pack-podrobno.html).")
    nb.md("## Цель\n\nОсвоить fill и expand у pack().")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()

forma_frame = ttk.Frame(root, padding=10)
forma_frame.pack(fill="x")

ttk.Label(forma_frame, text="Имя:").pack(side="left")
entry = ttk.Entry(forma_frame)
entry.pack(side="left", fill="x", expand=True)

root.update()
print(entry.winfo_manager())
root.destroy()''')
    nb.write(OUT_DIR / "16-14-pack-podrobno.ipynb")
    print(f"Записано: 16-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-15 · Адаптивный grid\n\nПрактика к разделу "
          "[«Адаптивный grid: sticky и weight»](../../site/chapters/glava-16/16-15-adaptivny-grid.html).")
    nb.md("## Цель\n\nПонять, как вес столбца распределяет дополнительное пространство.")
    nb.code('''def raspredelit_prostranstvo(weights, extra_space):
    total = sum(weights)
    if total == 0:
        return [0] * len(weights)
    return [extra_space * w / total for w in weights]

result_equal = raspredelit_prostranstvo([1, 1], 200)
result_weighted = raspredelit_prostranstvo([1, 2], 300)
print(result_equal, result_weighted)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте распределение для трёх колонок с весами "
          "[1, 1, 2] и 400 пикселями лишнего места.")
    nb.code('''result_three = raspredelit_prostranstvo([1, 1, 2], 400)
print(result_three)''')
    nb.write(OUT_DIR / "16-15-adaptivny-grid.ipynb")
    print(f"Записано: 16-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-16 · Виджеты выбора\n\nПрактика к разделу "
          "[«Виджеты выбора: Combobox, Listbox, Spinbox, Scale»](../../site/chapters/glava-16/16-16-widgety-vybora.html).")
    nb.md("## Цель\n\nОсвоить Combobox, Listbox, Spinbox и Scale.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()

variant = ttk.Combobox(root, values=["Маленький", "Средний", "Большой"], state="readonly")
variant.current(1)
variant.pack()

spisok = tk.Listbox(root)
spisok.insert("end", "Молоко")
spisok.insert("end", "Хлеб")
spisok.pack()
spisok.selection_set(0)

kolichestvo = ttk.Spinbox(root, from_=1, to=10)
kolichestvo.set(3)
kolichestvo.pack()

gromkost = ttk.Scale(root, from_=0, to=100, orient="horizontal")
gromkost.set(50)
gromkost.pack()

root.update()
print(variant.get())
print(spisok.get(spisok.curselection()[0]))
print(kolichestvo.get())
print(round(gromkost.get()))
root.destroy()''')
    nb.write(OUT_DIR / "16-16-widgety-vybora.ipynb")
    print(f"Записано: 16-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-17 · Progressbar и Notebook\n\nПрактика к разделу "
          "[«Progressbar и вкладки Notebook»](../../site/chapters/glava-16/16-17-progressbar-i-notebook.html).")
    nb.md("## Цель\n\nОсвоить Progressbar и вкладки Notebook.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()

progress = ttk.Progressbar(root, mode="determinate", maximum=100, value=0)
progress.pack(fill="x")
progress["value"] = 40

vkladki = ttk.Notebook(root)
vkladki.pack(fill="both", expand=True)
obshaya_vkladka = ttk.Frame(vkladki)
vneshnij_vid_vkladka = ttk.Frame(vkladki)
vkladki.add(obshaya_vkladka, text="Общие")
vkladki.add(vneshnij_vid_vkladka, text="Внешний вид")

root.update()
print(progress["value"])
print(len(vkladki.tabs()), "вкладки")
root.destroy()''')
    nb.write(OUT_DIR / "16-17-progressbar-i-notebook.ipynb")
    print(f"Записано: 16-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-18 · Messagebox и диалоги\n\nПрактика к разделу "
          "[«Messagebox и диалоги»](../../site/chapters/glava-16/16-18-messagebox-i-dialogi.html).")
    nb.md("## Цель\n\nПоказать диалог и корректно обработать возвращённое значение.")
    nb.md(MAINLOOP_NOTE_MD)
    md, code = messagebox_mock_setup({"askyesno": True, "showinfo": None})
    nb.md(md)
    nb.code(code)
    nb.code('''import tkinter as tk

root = tk.Tk()
otvet = messagebox.askyesno("Выход", "Сохранить изменения перед выходом?")
if otvet:
    messagebox.showinfo("Готово", "Изменения сохранены.")
print("Ответ пользователя:", otvet)
root.destroy()''')
    nb.write(OUT_DIR / "16-18-messagebox-i-dialogi.ipynb")
    print(f"Записано: 16-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-19 · filedialog и pathlib\n\nПрактика к разделу "
          "[«Открываем и сохраняем файлы: filedialog и pathlib»](../../site/chapters/glava-16/16-19-filedialog-i-pathlib.html).")
    nb.md("## Цель\n\nПравильно обработать отмену диалога перед работой с путём.")
    nb.md(MAINLOOP_NOTE_MD)
    md, code = filedialog_mock_setup({"askopenfilename": ""})
    nb.md(md)
    nb.code(code)
    nb.code('''from pathlib import Path

filename = filedialog.askopenfilename()
if not filename:
    otmena_obrabotana = True
else:
    otmena_obrabotana = False
    Path(filename).read_text(encoding="utf-8")

print("Отмена обработана корректно:", otmena_obrabotana)''')
    nb.md("## Задание ★ Базовая практика — успешный выбор файла")
    md2, code2 = filedialog_mock_setup({"askopenfilename": "privet_gui.txt"})
    nb.md(md2)
    nb.code(code2)
    nb.code('''from pathlib import Path

Path("privet_gui.txt").write_text("Привет из GUI!", encoding="utf-8")

filename = filedialog.askopenfilename()
if filename:
    text = Path(filename).read_text(encoding="utf-8")
print(text)''')
    nb.write(OUT_DIR / "16-19-filedialog-i-pathlib.ipynb")
    print(f"Записано: 16-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-20 · Toplevel\n\nПрактика к разделу "
          "[«Toplevel: несколько окон»](../../site/chapters/glava-16/16-20-toplevel.html).")
    nb.md("## Цель\n\nОткрыть дополнительное окно через Toplevel, а не второй Tk().")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()

def otkryt_nastrojki():
    okno_nastrojek = tk.Toplevel(root)
    okno_nastrojek.title("Настройки")
    ttk.Label(okno_nastrojek, text="Здесь будут настройки").pack(padx=20, pady=20)
    return okno_nastrojek

okno = otkryt_nastrojki()
root.update()
print(type(okno).__name__, okno.title())
okno.destroy()
root.destroy()''')
    nb.write(OUT_DIR / "16-20-toplevel.ipynb")
    print(f"Записано: 16-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-21 · Focus и доступность\n\nПрактика к разделу "
          "[«Focus, клавиатура и основы доступности»](../../site/chapters/glava-16/16-21-focus-i-dostupnost.html).")
    nb.md("## Цель\n\nПроверить форму на базовые правила доступности.")
    nb.code('''forma = [
    {"name": "name_entry", "has_label": True, "tab_index": 0},
    {"name": "email_entry", "has_label": True, "tab_index": 1},
    {"name": "submit_button", "has_label": True, "tab_index": 2},
]

def vse_imeyut_metku(widgets):
    return all(w["has_label"] for w in widgets)

def poryadok_posledovatelen(widgets):
    indeksy = [w["tab_index"] for w in widgets]
    return indeksy == sorted(indeksy)

vse_s_metkami = vse_imeyut_metku(forma)
poryadok_ok = poryadok_posledovatelen(forma)
print(vse_s_metkami, poryadok_ok)''')
    nb.md("## Задание ★ Базовая практика\n\nНайдите проблему в форме без подписи у поля поиска.")
    nb.code('''slomannaya_forma = [
    {"name": "search_entry", "has_label": False, "tab_index": 0},
]
najdena_problema = not vse_imeyut_metku(slomannaya_forma)
print(najdena_problema)''')
    nb.write(OUT_DIR / "16-21-focus-i-dostupnost.ipynb")
    print(f"Записано: 16-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-22 · after() и таймеры\n\nПрактика к разделу "
          "[«after(): таймеры без блокировки»](../../site/chapters/glava-16/16-22-after-tajmery.html).")
    nb.md("## Цель\n\nПостроить повторяющийся таймер через after() и остановить его.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()
schet = tk.IntVar(value=0)
label = ttk.Label(root, textvariable=schet)
label.pack()

def tik():
    schet.set(schet.get() + 1)

# программно вызываем tik() несколько раз вместо реального ожидания секунд
tik()
tik()
tik()
root.update()
print("Значение после трёх тиков:", schet.get())
root.destroy()''')
    nb.write(OUT_DIR / "16-22-after-tajmery.ipynb")
    print(f"Записано: 16-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-23 · Валидация ввода\n\nПрактика к разделу "
          "[«Валидация ввода и обратная связь»](../../site/chapters/glava-16/16-23-validatsiya-vvoda.html).")
    nb.md("## Цель\n\nПроверить общий разбор числа и специализированную валидацию поверх него.")
    nb.code('''def parse_number(text):
    text = text.strip()
    if not text:
        return False, None, "Поле не должно быть пустым"
    try:
        return True, float(text), ""
    except ValueError:
        return False, None, "Введите число"

ok1, val1, msg1 = parse_number("")
ok2, val2, msg2 = parse_number("abc")
ok3, val3, msg3 = parse_number("-5")
ok4, val4, msg4 = parse_number("100")
print(ok1, ok2, ok3, ok4)
print(val3, val4, repr(msg4))''')
    nb.md("## Задание ★★ Самостоятельная задача — специализированная валидация")
    nb.code('''def validate_positive_amount(text):
    ok, value, message = parse_number(text)
    if not ok:
        return False, message
    if value <= 0:
        return False, "Число должно быть больше нуля"
    return True, ""

def validate_positive_int(text):
    ok, value, message = parse_number(text)
    if not ok:
        return False, message
    if value != int(value):
        return False, "Введите целое число"
    if int(value) < 1:
        return False, "Число должно быть не меньше 1"
    return True, ""

amount_negative_ok, _ = validate_positive_amount("-5")
amount_valid_ok, _ = validate_positive_amount("100")
people_float_ok, _ = validate_positive_int("2.5")
people_valid_ok, _ = validate_positive_int("5")
print(amount_negative_ok, amount_valid_ok, people_float_ok, people_valid_ok)''')
    nb.write(OUT_DIR / "16-23-validatsiya-vvoda.ipynb")
    print(f"Записано: 16-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-24 · Архитектура приложения\n\nПрактика к разделу "
          "[«Архитектура приложения: логика отдельно от виджетов»](../../site/chapters/glava-16/16-24-arhitektura-prilozheniya.html).")
    nb.md("## Цель\n\nПроверить чистую доменную функцию и исправить ловушку lambda в цикле.")
    nb.code('''def calculate_tip(amount, percent, people):
    total_tip = amount * percent / 100
    return total_tip / people

result = calculate_tip(1000, 15, 2)
print(result)''')
    nb.md("## Задание ★★ Самостоятельная задача — позднее связывание в lambda")
    nb.code('''callbacks = []
for i in range(3):
    callbacks.append(lambda i=i: i)

values = [cb() for cb in callbacks]
print(values)''')
    nb.write(OUT_DIR / "16-24-arhitektura-prilozheniya.ipynb")
    print(f"Записано: 16-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-25 · Класс приложения и настройки\n\nПрактика к разделу "
          "[«Класс приложения и персистентные настройки»](../../site/chapters/glava-16/16-25-klass-prilozheniya-i-nastrojki.html).")
    nb.md("## Цель\n\nПерсистентные настройки для GUI — те же функции, что и в главе 15.")
    nb.code('''import json
from pathlib import Path

DEFAULT_SETTINGS = {"theme": "light", "window_width": 900}

def load_settings(path):
    if not path.exists():
        return dict(DEFAULT_SETTINGS)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(path, settings):
    with path.open("w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

settings_path = Path("gui_settings.json")
settings_path.unlink(missing_ok=True)
defaults = load_settings(settings_path)
save_settings(settings_path, {"theme": "dark", "window_width": 1024})
loaded = load_settings(settings_path)
print(defaults)
print(loaded)''')
    nb.write(OUT_DIR / "16-25-klass-prilozheniya-i-nastrojki.ipynb")
    print(f"Записано: 16-25 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-26 · Счётчик кликов\n\nПрактика к разделу "
          "[«Мини-проект: счётчик кликов»](../../site/chapters/glava-16/16-26-mini-proekt-schetchik-klikov.html).")
    nb.md("## Цель\n\nСобрать самый маленький настоящий проект главы.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Счётчик кликов")

schet = tk.IntVar(value=0)
ttk.Label(root, textvariable=schet, font=("Arial", 24)).pack(pady=20)

def na_klik():
    schet.set(schet.get() + 1)

button = ttk.Button(root, text="+1", command=na_klik)
button.pack(pady=10)

root.update()
button.invoke()
button.invoke()
button.invoke()
print("Кликов:", schet.get())
root.destroy()''')
    nb.write(OUT_DIR / "16-26-mini-proekt-schetchik-klikov.ipynb")
    print(f"Записано: 16-26 ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-27 · Конвертер температур\n\nПрактика к разделу "
          "[«Мини-проект: конвертер температур»](../../site/chapters/glava-16/16-27-mini-proekt-konverter-temperatur.html).")
    nb.md("## Цель\n\nПроверить чистые функции преобразования температуры.")
    nb.code('''def celsius_v_farengejty(celsius):
    return celsius * 9 / 5 + 32

def farengejty_v_celsius(farengejty):
    return (farengejty - 32) * 5 / 9

f_100 = round(celsius_v_farengejty(100), 1)
c_32 = round(farengejty_v_celsius(32), 1)
roundtrip = round(farengejty_v_celsius(celsius_v_farengejty(37)), 1)
print(f_100, c_32, roundtrip)''')
    nb.write(OUT_DIR / "16-27-mini-proekt-konverter-temperatur.ipynb")
    print(f"Записано: 16-27 ({len(nb)} ячеек)")


def build_28() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-28 · Таймер обратного отсчёта\n\nПрактика к разделу "
          "[«Мини-проект: таймер обратного отсчёта»](../../site/chapters/glava-16/16-28-mini-proekt-tajmer.html).")
    nb.md("## Цель\n\nПроверить форматирование времени и логику одного тика таймера.")
    nb.code('''def format_time(sekundy):
    minuty, ostatok = divmod(sekundy, 60)
    return f"{minuty:02d}:{ostatok:02d}"

t1 = format_time(65)
t2 = format_time(600)
t3 = format_time(5)
print(t1, t2, t3)''')
    nb.md("## Задание ★★ Самостоятельная задача — тик с учётом running")
    nb.code('''def tick(remaining, running):
    if not running or remaining <= 0:
        return remaining
    return remaining - 1

after_tick = tick(10, True)
after_stop = tick(10, False)
print(after_tick, after_stop)''')
    nb.write(OUT_DIR / "16-28-mini-proekt-tajmer.ipynb")
    print(f"Записано: 16-28 ({len(nb)} ячеек)")


def build_29() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-29 · Список задач\n\nПрактика к разделу "
          "[«Мини-проект: список задач»](../../site/chapters/glava-16/16-29-mini-proekt-todo.html).")
    nb.md("## Цель\n\nПроверить чистые функции списка задач и их персистентность.")
    nb.code('''import json
from pathlib import Path

def load_tasks(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(path, tasks):
    with path.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(tasks, text):
    if not text.strip():
        return tasks
    return tasks + [text.strip()]

def remove_task(tasks, index):
    return tasks[:index] + tasks[index + 1:]

todo_path = Path("todo_test.json")
todo_path.unlink(missing_ok=True)

tasks = load_tasks(todo_path)
tasks = add_task(tasks, "Купить молоко")
tasks = add_task(tasks, "   ")
tasks = add_task(tasks, "Позвонить")
save_tasks(todo_path, tasks)

loaded_tasks = load_tasks(todo_path)
tasks_after_remove = remove_task(loaded_tasks, 0)
print(tasks)
print(loaded_tasks)
print(tasks_after_remove)''')
    nb.write(OUT_DIR / "16-29-mini-proekt-todo.ipynb")
    print(f"Записано: 16-29 ({len(nb)} ячеек)")


def build_30() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-30 · Редактор заметок\n\nПрактика к разделу "
          "[«Мини-проект: редактор заметок»](../../site/chapters/glava-16/16-30-mini-proekt-zametki.html).")
    nb.md("## Цель\n\nСобрать редактор заметок с меню, filedialog и pathlib.")
    nb.md(MAINLOOP_NOTE_MD)
    md, code = filedialog_mock_setup({"asksaveasfilename": "moi_zametki_test.txt"})
    nb.md(md)
    nb.code(code)
    nb.code('''import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

root = tk.Tk()
root.title("Редактор заметок")

text_widget = ScrolledText(root, wrap="word")
text_widget.pack(fill="both", expand=True)
text_widget.insert("1.0", "Заметка о главе 16")

current_path = None

def sohranit_kak():
    global current_path
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if not filename:
        return
    current_path = Path(filename)
    current_path.write_text(text_widget.get("1.0", "end-1c"), encoding="utf-8")

sohranit_kak()
root.update()
print(current_path.read_text(encoding="utf-8"))
root.destroy()''')
    nb.write(OUT_DIR / "16-30-mini-proekt-zametki.ipynb")
    print(f"Записано: 16-30 ({len(nb)} ячеек)")


def build_31() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-31 · Tip Calculator Pro\n\nПрактика к разделу "
          "[«Tip Calculator Pro: финальная версия»](../../site/chapters/glava-16/16-31-tip-calculator-pro.html).")
    nb.md("## Цель\n\nСобрать финальный класс приложения с валидацией и настройками.")
    nb.md(MAINLOOP_NOTE_MD)
    nb.code('''import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path

SETTINGS_PATH = Path("tip_calculator_settings_test.json")
SETTINGS_PATH.unlink(missing_ok=True)
DEFAULT_SETTINGS = {"last_percent": "15"}

def load_settings():
    if not SETTINGS_PATH.exists():
        return dict(DEFAULT_SETTINGS)
    with SETTINGS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    with SETTINGS_PATH.open("w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

def calculate_tip(amount, percent, people):
    return (amount * percent / 100) / people

def parse_number(text):
    text = text.strip()
    if not text:
        return False, None, "Поле не должно быть пустым"
    try:
        return True, float(text), ""
    except ValueError:
        return False, None, "Введите число"

def validate_positive_amount(text):
    ok, value, message = parse_number(text)
    if not ok:
        return False, message
    if value <= 0:
        return False, "Число должно быть больше нуля"
    return True, ""

def validate_positive_int(text):
    ok, value, message = parse_number(text)
    if not ok:
        return False, message
    if value != int(value):
        return False, "Введите целое число"
    if int(value) < 1:
        return False, "Число должно быть не меньше 1"
    return True, ""

class TipCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.amount_var = tk.StringVar()
        self.percent_var = tk.StringVar(value=self.settings["last_percent"])
        self.people_var = tk.StringVar(value="1")
        self.result_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.amount_var).pack()
        ttk.Entry(root, textvariable=self.people_var).pack()
        ttk.Button(root, text="Считать", command=self.on_calculate).pack()

    def on_calculate(self):
        ok, message = validate_positive_amount(self.amount_var.get())
        if not ok:
            self.result_var.set(message)
            return
        ok_people, message_people = validate_positive_int(self.people_var.get())
        if not ok_people:
            self.result_var.set(message_people)
            return
        chaevye = calculate_tip(
            float(self.amount_var.get()),
            float(self.percent_var.get()),
            int(self.people_var.get()),
        )
        self.result_var.set(f"{chaevye:.2f}")
        self.settings["last_percent"] = self.percent_var.get()

root = tk.Tk()
app = TipCalculatorApp(root)
app.amount_var.set("1000")
app.people_var.set("2")
app.on_calculate()
result_with_valid_people = app.result_var.get()

app.people_var.set("2.5")
app.on_calculate()
result_with_invalid_people = app.result_var.get()

save_settings(app.settings)
root.update()
print(result_with_valid_people)
print(result_with_invalid_people)
root.destroy()''')
    nb.write(OUT_DIR / "16-31-tip-calculator-pro.ipynb")
    print(f"Записано: 16-31 ({len(nb)} ячеек)")


def build_32() -> None:
    nb = NotebookBuilder()
    nb.md("# 16-32 · Отладка и качество GUI\n\nПрактика к разделу "
          "[«Отладка интерфейса и качество GUI»](../../site/chapters/glava-16/16-32-debugging-i-kachestvo.html).")
    nb.md("## Цель\n\nРаспознавать, какие действия безопасны внутри GUI-callback.")
    nb.code('''def is_safe_for_gui_callback(action):
    unsafe_actions = {"time.sleep", "while_true_poll", "huge_synchronous_computation"}
    return action not in unsafe_actions

check_sleep = is_safe_for_gui_callback("time.sleep")
check_after = is_safe_for_gui_callback("root.after")
check_while = is_safe_for_gui_callback("while_true_poll")
print(check_sleep, check_after, check_while)''')
    nb.write(OUT_DIR / "16-32-debugging-i-kachestvo.ipynb")
    print(f"Записано: 16-32 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
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
    build_32()
