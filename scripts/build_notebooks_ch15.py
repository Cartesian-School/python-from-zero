#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 15 (файлы).

Ноутбуки создают собственные учебные файлы прямо в notebooks/chapter-15/, чтобы
чтение было настоящим, а не гипотетическим — это тоже часть проверки: если бы
пример на самом деле не работал с файловой системой, выполнение бы это поймало.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-15"


def input_setup(answers: list[str]) -> tuple[str, str]:
    md = ("## Про input() в этом ноутбуке\n\nЭтот ноутбук выполняется автоматически, поэтому "
          "`input()` временно подменён на заранее заготовленные ответы.")
    answers_repr = ", ".join(repr(a) for a in answers)
    code = f"""_answers = iter([{answers_repr}])

def input(prompt=""):
    answer = next(_answers)
    print(prompt + answer)
    return answer"""
    return md, code


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-01 · Открытие и чтение файлов\n\nПрактика к разделу "
          "[«Зачем нужны файлы? Открытие и чтение»](../../site/chapters/glava-15/15-01-zachem-fajly.html).")
    nb.md("## Цель\n\nОткрывать и читать файлы через with.")
    nb.md("## Подготовка — создаём учебный файл")
    nb.code('''with open("privet.txt", "w") as f:
    f.write("Привет из файла!\\nЭто вторая строка.")
print("Учебный файл создан.")''')
    nb.md("## Рабочий пример")
    nb.code('''with open("privet.txt", "r") as file:
    content = file.read()
print(content)''')
    nb.md("## Типичная ошибка\n\nЧтение несуществующего файла вызывает FileNotFoundError.")
    nb.code('''open("nesuschestvuyuschij_fajl.txt", "r")''', raises=True)
    nb.md("## Задание ★ Базовая практика\n\nСоздайте файл со своим именем и городом, затем "
          "прочитайте и выведите его содержимое.")
    nb.code('''with open("o_sebe.txt", "w") as f:
    f.write("Cartesian\\nМосква")

with open("o_sebe.txt", "r") as f:
    print(f.read())''')
    nb.write(OUT_DIR / "15-01-otkrytie-chtenie.ipynb")
    print(f"Записано: 15-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-02 · Строка за строкой\n\nПрактика к разделу "
          "[«Строка за строкой»](../../site/chapters/glava-15/15-02-stroka-za-strokoj.html).")
    nb.md("## Цель\n\nОсвоить построчное чтение файлов.")
    nb.md("## Подготовка — создаём учебный файл")
    nb.code('''spisok = ["яблоки", "хлеб", "молоко", "сыр"]
with open("spisok.txt", "w") as f:
    f.writelines(item + "\\n" for item in spisok)
print("Учебный файл списка покупок создан.")''')
    nb.md("## Рабочий пример")
    nb.code('''with open("spisok.txt", "r") as file:
    for line in file:
        print(line.strip())''')
    nb.md("## Эксперимент 1 — readlines()")
    nb.code('''with open("spisok.txt", "r") as file:
    lines = file.readlines()

print(len(lines), "строк")
print(lines[0])''')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте, сколько строк в файле, не используя "
          "len(readlines()) — только счётчиком в цикле.")
    nb.code('''count = 0
with open("spisok.txt", "r") as file:
    for line in file:
        count += 1

print("Строк в файле:", count)''')
    nb.write(OUT_DIR / "15-02-stroka-za-strokoj.ipynb")
    print(f"Записано: 15-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-03 · Создание новых файлов\n\nПрактика к разделу "
          "[«Создание новых файлов»](../../site/chapters/glava-15/15-03-sozdanie-fajlov.html).")
    nb.md("## Цель\n\nОсвоить режимы записи (w), дозаписи (a) и pathlib.")
    nb.md("## Рабочий пример — запись")
    nb.code('''with open("rezultaty.txt", "w") as file:
    file.write("Уровень 1: 100 очков\\n")
    file.write("Уровень 2: 250 очков\\n")

with open("rezultaty.txt", "r") as file:
    print(file.read())''')
    nb.md("## Эксперимент 1 — дозапись")
    nb.code('''with open("rezultaty.txt", "a") as file:
    file.write("Уровень 3: 400 очков\\n")

with open("rezultaty.txt", "r") as file:
    print(file.read())''')
    nb.md("## Эксперимент 2 — режим w стирает старое содержимое")
    nb.code('''with open("rezultaty.txt", "w") as file:
    file.write("Новая игра началась.\\n")

with open("rezultaty.txt", "r") as file:
    print(file.read())   # старые результаты исчезли!''')
    nb.md("## Задание ★ Базовая практика — pathlib")
    nb.code('''from pathlib import Path

file_path = Path("rezultaty.txt")
print(file_path.exists())
print(file_path.name)
print(file_path.suffix)

with file_path.open("r") as f:
    print(f.read())''')
    nb.write(OUT_DIR / "15-03-sozdanie-fajlov.ipynb")
    print(f"Записано: 15-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-04 · Мини-проект — дневник заметок\n\nПрактика к разделу "
          "[«Мини-проект — знакомство с файлами»](../../site/chapters/glava-15/15-04-mini-proekt-itogi.html).")
    nb.md("## Цель\n\nСобрать чтение и запись в одном мини-проекте.")
    nb.code('''from pathlib import Path

# начинаем с чистого файла заметок для повторяемости примера
Path("zametki.txt").unlink(missing_ok=True)
print("Готово к новым заметкам.")''')
    md, code = input_setup(["Первая заметка"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

fajl_zametok = Path("zametki.txt")

novaya_zametka = input("Новая заметка: ")

with fajl_zametok.open("a") as f:
    f.write(novaya_zametka + "\\n")

print("Все заметки:")
with fajl_zametok.open("r") as f:
    for line in f:
        print("-", line.strip())''')
    nb.md("## Задание ★★ Самостоятельная задача — ещё одна заметка (проверка дозаписи)")
    md2, code2 = input_setup(["Вторая заметка"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''from pathlib import Path

fajl_zametok = Path("zametki.txt")
novaya_zametka = input("Новая заметка: ")

with fajl_zametok.open("a") as f:
    f.write(novaya_zametka + "\\n")

print("Все заметки:")
with fajl_zametok.open("r") as f:
    for i, line in enumerate(f, start=1):
        print(f"{i}. {line.strip()}")''')
    nb.md("## Проверка результата")
    nb.code('''from pathlib import Path

lines = Path("zametki.txt").read_text().splitlines()
assert lines == ["Первая заметка", "Вторая заметка"]
print("Обе заметки сохранились в правильном порядке.")''')
    nb.write(OUT_DIR / "15-04-mini-proekt.ipynb")
    print(f"Записано: 15-04 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
