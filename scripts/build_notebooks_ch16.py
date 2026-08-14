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
