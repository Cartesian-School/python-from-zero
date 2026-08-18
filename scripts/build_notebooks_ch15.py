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
    nb.code('''with open("privet.txt", "w", encoding="utf-8") as f:
    f.write("Привет из файла!\\nЭто вторая строка.")
print("Учебный файл создан.")''')
    nb.md("## Рабочий пример")
    nb.code('''with open("privet.txt", "r", encoding="utf-8") as file:
    content = file.read()
print(content)''')
    nb.md("## Типичная ошибка\n\nЧтение несуществующего файла вызывает FileNotFoundError.")
    nb.code('''open("nesuschestvuyuschij_fajl.txt", "r", encoding="utf-8")''', raises=True)
    nb.md("## Задание ★ Базовая практика\n\nСоздайте файл со своим именем и городом, затем "
          "прочитайте и выведите его содержимое.")
    nb.code('''with open("o_sebe.txt", "w", encoding="utf-8") as f:
    f.write("Cartesian\\nМосква")

with open("o_sebe.txt", "r", encoding="utf-8") as f:
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
with open("spisok.txt", "w", encoding="utf-8") as f:
    f.writelines(item + "\\n" for item in spisok)
print("Учебный файл списка покупок создан.")''')
    nb.md("## Рабочий пример")
    nb.code('''with open("spisok.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())''')
    nb.md("## Эксперимент 1 — readlines()")
    nb.code('''with open("spisok.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

print(len(lines), "строк")
print(lines[0])''')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте, сколько строк в файле, не используя "
          "len(readlines()) — только счётчиком в цикле.")
    nb.code('''count = 0
with open("spisok.txt", "r", encoding="utf-8") as file:
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
    nb.code('''with open("rezultaty.txt", "w", encoding="utf-8") as file:
    file.write("Уровень 1: 100 очков\\n")
    file.write("Уровень 2: 250 очков\\n")

with open("rezultaty.txt", "r", encoding="utf-8") as file:
    print(file.read())''')
    nb.md("## Эксперимент 1 — дозапись")
    nb.code('''with open("rezultaty.txt", "a", encoding="utf-8") as file:
    file.write("Уровень 3: 400 очков\\n")

with open("rezultaty.txt", "r", encoding="utf-8") as file:
    print(file.read())''')
    nb.md("## Эксперимент 2 — режим w стирает старое содержимое")
    nb.code('''with open("rezultaty.txt", "w", encoding="utf-8") as file:
    file.write("Новая игра началась.\\n")

with open("rezultaty.txt", "r", encoding="utf-8") as file:
    print(file.read())   # старые результаты исчезли!''')
    nb.md("## Задание ★ Базовая практика — pathlib")
    nb.code('''from pathlib import Path

file_path = Path("rezultaty.txt")
print(file_path.exists())
print(file_path.name)
print(file_path.suffix)

with file_path.open("r", encoding="utf-8") as f:
    print(f.read())''')
    nb.write(OUT_DIR / "15-03-sozdanie-fajlov.ipynb")
    print(f"Записано: 15-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-04 · Мини-проект — дневник заметок\n\nПрактика к разделу "
          "[«Мини-проект: дневник заметок»](../../site/chapters/glava-15/15-04-mini-proekt-itogi.html).")
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

with fajl_zametok.open("a", encoding="utf-8") as f:
    f.write(novaya_zametka + "\\n")

print("Все заметки:")
with fajl_zametok.open("r", encoding="utf-8") as f:
    for line in f:
        print("-", line.strip())''')
    nb.md("## Задание ★★ Самостоятельная задача — ещё одна заметка (проверка дозаписи)")
    md2, code2 = input_setup(["Вторая заметка"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''from pathlib import Path

fajl_zametok = Path("zametki.txt")
novaya_zametka = input("Новая заметка: ")

with fajl_zametok.open("a", encoding="utf-8") as f:
    f.write(novaya_zametka + "\\n")

print("Все заметки:")
with fajl_zametok.open("r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"{i}. {line.strip()}")''')
    nb.md("## Проверка результата")
    nb.code('''from pathlib import Path

lines = Path("zametki.txt").read_text(encoding="utf-8").splitlines()
assert lines == ["Первая заметка", "Вторая заметка"]
print("Обе заметки сохранились в правильном порядке.")''')
    nb.write(OUT_DIR / "15-04-mini-proekt.ipynb")
    print(f"Записано: 15-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-05 · Файл, папка и файловая система\n\nПрактика к разделу "
          "[«Файл, папка и файловая система»](../../site/chapters/glava-15/15-05-fajl-i-papka.html).")
    nb.md("## Цель\n\nРазличать файлы и папки на реальном маленьком дереве.")
    nb.code('''from pathlib import Path

Path("proekt/data").mkdir(parents=True, exist_ok=True)
Path("proekt/data/scores.txt").write_text("100\\n", encoding="utf-8")
Path("proekt/README.md").write_text("readme", encoding="utf-8")
print("Дерево проекта готово.")''')
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

papka = Path("proekt/data")
fajl = Path("proekt/data/scores.txt")
print(papka.is_dir())
print(fajl.is_file())''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте папку `proekt/assets` с одним файлом внутри "
          "и посчитайте, сколько элементов лежит непосредственно в `proekt/`.")
    nb.code('''from pathlib import Path

Path("proekt/assets").mkdir(exist_ok=True)
Path("proekt/assets/logo.txt").write_text("logo", encoding="utf-8")

total_items = len(list(Path("proekt").iterdir()))
print(total_items)''')
    nb.write(OUT_DIR / "15-05-fajl-i-papka.ipynb")
    print(f"Записано: 15-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-06 · Абсолютные и относительные пути\n\nПрактика к разделу "
          "[«Пути: абсолютные и относительные»](../../site/chapters/glava-15/15-06-puti-absolyutnye-i-otnositelnye.html).")
    nb.md("## Цель\n\nОтличать относительный путь от абсолютного и уметь получить абсолютный "
          "вариант через .resolve().")
    nb.code('''from pathlib import Path

Path("data").mkdir(exist_ok=True)
Path("data/a.txt").write_text("привет", encoding="utf-8")''')
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

rel = Path("data/a.txt")
abs_path = rel.resolve()
print(rel.is_absolute())
print(abs_path.is_absolute())''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что имя файла не потерялось при переходе "
          "к абсолютному пути.")
    nb.code('''from pathlib import Path

rel = Path("data/a.txt")
abs_path = rel.resolve()
imya_sovpadaet = abs_path.name == rel.name
print(imya_sovpadaet)''')
    nb.write(OUT_DIR / "15-06-puti-absolyutnye-i-otnositelnye.ipynb")
    print(f"Записано: 15-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-07 · Текущая рабочая директория (CWD)\n\nЛокальная практика к разделу "
          "[«Текущая рабочая директория (CWD)»](../../site/chapters/glava-15/15-07-tekushaya-rabochaya-directoriya.html).\n\n"
          "**Этот ноутбук выполняется локально** — на вашем компьютере, а не в браузере: "
          "смысл упражнения именно в том, чтобы увидеть разницу между CWD и папкой, где лежит "
          "исходный файл, на настоящей файловой системе.")
    nb.md("## Шаг 1 — где я нахожусь?")
    nb.code('''from pathlib import Path

print("CWD:", Path.cwd())''')
    nb.md("## Шаг 2 — папка самого скрипта")
    nb.code('''from pathlib import Path

if "__file__" in globals():
    print("Папка файла:", Path(__file__).resolve().parent)
else:
    print("__file__ не определён в этой среде выполнения (например, в интерактивном ноутбуке) — "
          "это нормально и ожидаемо, см. раздел 15.7.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСохраните этот файл как обычный `.py`-скрипт "
          "в папке `project/src/`, создайте `project/data/config.json`, и запустите скрипт "
          "дважды: один раз из `project/`, другой раз из `project/src/`. Сравните значение "
          "`Path.cwd()` и то, какой путь `Path(\"data/config.json\")` разрешает в каждом "
          "случае — и убедитесь, что надёжный вариант — путь через `Path(__file__).resolve()."
          "parent`, а не через CWD.")
    nb.write(OUT_DIR / "15-07-cwd.ipynb")
    print(f"Записано: 15-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-08 · pathlib.Path: пути как объекты\n\nПрактика к разделу "
          "[«pathlib.Path: пути как объекты»](../../site/chapters/glava-15/15-08-pochemu-pathlib.html).")
    nb.md("## Цель\n\nСобирать путь через / вместо конкатенации строк.")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

file_path = Path("data") / "players" / "anna.json"
print(file_path)
print(file_path.name)
print(file_path.parent.as_posix())''')
    nb.md("## Задание ★ Базовая практика\n\nПостройте путь на один уровень глубже и проверьте, "
          "что число частей пути увеличилось.")
    nb.code('''from pathlib import Path

file_path = Path("data") / "players" / "anna.json"
deeper_path = Path("data") / "players" / "guilds" / "anna.json"
parts_increased = len(deeper_path.parts) > len(file_path.parts)
print(parts_increased)''')
    nb.write(OUT_DIR / "15-08-pochemu-pathlib.ipynb")
    print(f"Записано: 15-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-09 · Разбираем путь: name, stem, suffix, parent\n\nПрактика к разделу "
          "[«Разбираем путь»](../../site/chapters/glava-15/15-09-razbiraem-put.html).")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

path = Path("data/scores.txt")
print(path.name)
print(path.stem)
print(path.suffix)
print(path.parent.as_posix())''')
    nb.md("## Задание ★ Базовая практика\n\nРазберите путь без расширения и убедитесь, что "
          "suffix у него — пустая строка.")
    nb.code('''from pathlib import Path

path_bez_suffiksa = Path("data/README")
suffix_pust = path_bez_suffiksa.suffix == ""
stem_ravno_name = path_bez_suffiksa.stem == path_bez_suffiksa.name
print(suffix_pust, stem_ravno_name)''')
    nb.write(OUT_DIR / "15-09-razbiraem-put.ipynb")
    print(f"Записано: 15-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-10 · Практика: пути и CWD\n\nПрактика к разделу "
          "[«Практика: пути и CWD»](../../site/chapters/glava-15/15-10-praktika-puti-i-cwd.html).")
    nb.md("## Рабочий пример — путь относительно базовой папки")
    nb.code('''from pathlib import Path

BASE_DIR = Path.cwd()
data_dir = BASE_DIR / "data"
data_dir.mkdir(exist_ok=True)

file_path = data_dir / "otchet.txt"
file_path.unlink(missing_ok=True)   # для повторяемости примера при повторном запуске
existed_before = file_path.exists()
file_path.write_text("готово", encoding="utf-8")
existed_after = file_path.exists()
print(existed_before, existed_after)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПостройте путь к родителю родителя "
          "`data_dir` и убедитесь, что это тот же путь, что и `BASE_DIR.parent`.")
    nb.code('''from pathlib import Path

BASE_DIR = Path.cwd()
data_dir = BASE_DIR / "data"
sovpadaet = data_dir.parent.parent == BASE_DIR.parent
print(sovpadaet)''')
    nb.write(OUT_DIR / "15-10-praktika-puti-i-cwd.ipynb")
    print(f"Записано: 15-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-11 · open() возвращает объект файла\n\nПрактика к разделу "
          "[«open() возвращает объект файла»](../../site/chapters/glava-15/15-11-file-object.html).")
    nb.md("## Подготовка")
    nb.code('''with open("privet2.txt", "w", encoding="utf-8") as f:
    f.write("привет")
print("Готово.")''')
    nb.md("## Рабочий пример")
    nb.code('''with open("privet2.txt", "r", encoding="utf-8") as file:
    mode_value = file.mode
    name_value = file.name
    closed_during = file.closed
    content = file.read()
closed_after = file.closed
print(mode_value, name_value, closed_during, closed_after)
print(content)''')
    nb.md("## Задание ★ Базовая практика\n\nВыведите тип объекта file и убедитесь, что это "
          "не строка и не список.")
    nb.code('''with open("privet2.txt", "r", encoding="utf-8") as file:
    tip_ne_str = not isinstance(file, str)
    tip_ne_list = not isinstance(file, list)
print(tip_ne_str, tip_ne_list)''')
    nb.write(OUT_DIR / "15-11-file-object.ipynb")
    print(f"Записано: 15-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-12 · Жизненный цикл файла и with\n\nПрактика к разделу "
          "[«Жизненный цикл файла и with»](../../site/chapters/glava-15/15-12-zhiznenny-cikl-i-with.html).")
    nb.md("## Рабочий пример")
    nb.code('''with open("cikl.txt", "w", encoding="utf-8") as f:
    f.write("data")

with open("cikl.txt", "r", encoding="utf-8") as file:
    closed_inside = file.closed
closed_outside = file.closed
print(closed_inside, closed_outside)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nОткройте файл БЕЗ with, прочитайте его и "
          "закройте вручную — убедитесь, что file.closed становится True только после "
          "явного close().")
    nb.code('''file = open("cikl.txt", "r", encoding="utf-8")
closed_before_manual_close = file.closed
file.read()
file.close()
closed_after_manual_close = file.closed
print(closed_before_manual_close, closed_after_manual_close)''')
    nb.write(OUT_DIR / "15-12-zhiznenny-cikl-i-with.ipynb")
    print(f"Записано: 15-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-13 · Курсор файла: tell() и seek()\n\nПрактика к разделу "
          "[«Курсор файла»](../../site/chapters/glava-15/15-13-kursor-fajla.html).")
    nb.md("## Подготовка")
    nb.code('''with open("alfavit2.txt", "w", encoding="utf-8") as f:
    f.write("ABCDE")
print("Готово.")''')
    nb.md("## Рабочий пример")
    nb.code('''with open("alfavit2.txt", "r", encoding="utf-8") as f:
    first = f.read(2)
    pos_after_first = f.tell()
    second = f.read(2)
    f.seek(0)
    reread = f.read()
print(first, pos_after_first, second, reread)''')
    nb.md("## Задание ★ Базовая практика\n\nПрочитайте файл до конца, затем прочитайте ещё раз "
          "без seek() — убедитесь, что курсор сам не возвращается.")
    nb.code('''with open("alfavit2.txt", "r", encoding="utf-8") as f:
    f.read()
    posle_konca = f.read()
posle_konca_pusto = posle_konca == ""
print(posle_konca_pusto)''')
    nb.write(OUT_DIR / "15-13-kursor-fajla.ipynb")
    print(f"Записано: 15-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-14 · Читаем файлы: read(), readline(), readlines()\n\nПрактика к разделу "
          "[«Читаем файлы»](../../site/chapters/glava-15/15-14-chitaem-fajly.html).")
    nb.md("## Подготовка")
    nb.code('''with open("spisok2.txt", "w", encoding="utf-8") as f:
    f.write("a\\nb\\nc\\n")
print("Готово.")''')
    nb.md("## Рабочий пример")
    nb.code('''with open("spisok2.txt", "r", encoding="utf-8") as f:
    first_line = f.readline().strip()
    second_line = f.readline().strip()

with open("spisok2.txt", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

counted = 0
with open("spisok2.txt", "r", encoding="utf-8") as f:
    for line in f:
        counted += 1

print(first_line, second_line, len(all_lines), counted)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что число строк, посчитанное циклом, "
          "совпадает с длиной списка из readlines().")
    nb.code('''sovpadaet = counted == len(all_lines)
print(sovpadaet)''')
    nb.write(OUT_DIR / "15-14-chitaem-fajly.ipynb")
    print(f"Записано: 15-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-15 · Пишем в файлы: write() и режимы r/w/a/x\n\nПрактика к разделу "
          "[«write() и режимы r/w/a/x»](../../site/chapters/glava-15/15-15-pishem-i-rezhimy.html).")
    nb.md("## Рабочий пример — w, a, x")
    nb.code('''with open("igra.txt", "w", encoding="utf-8") as f:
    f.write("старт\\n")

with open("igra.txt", "a", encoding="utf-8") as f:
    f.write("продолжение\\n")

with open("igra.txt", "r", encoding="utf-8") as f:
    posle_dozapisi = f.read()

x_failed_as_expected = False
try:
    with open("igra.txt", "x", encoding="utf-8") as f:
        pass
except FileExistsError:
    x_failed_as_expected = True

print(posle_dozapisi)
print(x_failed_as_expected)''')
    nb.md("## Задание ★★ Самостоятельная задача — ловушка writelines()")
    nb.code('''imena = ["Anna", "Bob"]
with open("igroki2.txt", "w", encoding="utf-8") as f:
    f.writelines(imya + "\\n" for imya in imena)

with open("igroki2.txt", "r", encoding="utf-8") as f:
    igroki_content = f.read()
print(igroki_content)''')
    nb.write(OUT_DIR / "15-15-pishem-i-rezhimy.ipynb")
    print(f"Записано: 15-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-16 · Текст, bytes и кодировка UTF-8\n\nПрактика к разделу "
          "[«Текст, bytes и UTF-8»](../../site/chapters/glava-15/15-16-text-bytes-encoding.html).")
    nb.md("## Рабочий пример")
    nb.code('''text = "Питон"
encoded = text.encode("utf-8")
chars_len = len(text)
bytes_len = len(encoded)
decoded_back = encoded.decode("utf-8")
print(chars_len, bytes_len, decoded_back)''')
    nb.md("## Задание ★ Базовая практика\n\nЗапишите строку с кириллицей в файл с "
          "явным encoding=\"utf-8\" и прочитайте её обратно.")
    nb.code('''with open("privet3.txt", "w", encoding="utf-8") as f:
    f.write("Привет!")

with open("privet3.txt", "r", encoding="utf-8") as f:
    read_back = f.read()
print(read_back)''')
    nb.write(OUT_DIR / "15-16-text-bytes-encoding.ipynb")
    print(f"Записано: 15-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-17 · Бинарные файлы и переносы строк\n\nПрактика к разделу "
          "[«Бинарные файлы и переносы строк»](../../site/chapters/glava-15/15-17-binarnye-fajly-i-perevody-strok.html).")
    nb.md("## Рабочий пример")
    nb.code('''data = bytes([10, 20, 30])
with open("signal2.bin", "wb") as f:
    f.write(data)

with open("signal2.bin", "rb") as f:
    read_data = f.read()
print(read_data)''')
    nb.md("## Задание ★ Базовая практика — символы против байтов")
    nb.code('''text2 = "Питон🐍"
chars_len2 = len(text2)
bytes_len2 = len(text2.encode("utf-8"))
print(chars_len2, bytes_len2)''')
    nb.write(OUT_DIR / "15-17-binarnye-fajly.ipynb")
    print(f"Записано: 15-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-18 · pathlib: read_text, write_text, read_bytes, write_bytes\n\nПрактика к разделу "
          "[«pathlib: удобные методы»](../../site/chapters/glava-15/15-18-pathlib-udobnye-metody.html).")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

p = Path("nastroyki3.txt")
p.write_text("привет", encoding="utf-8")
text_back = p.read_text(encoding="utf-8")
print(text_back)''')
    nb.md("## Задание ★ Базовая практика — бинарные данные")
    nb.code('''from pathlib import Path

pb = Path("signal3.bin")
pb.write_bytes(bytes([1, 2, 3]))
bytes_back = pb.read_bytes()
print(bytes_back)''')
    nb.write(OUT_DIR / "15-18-pathlib-udobnye-metody.ipynb")
    print(f"Записано: 15-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-19 · Папки: exists(), is_file(), mkdir()\n\nПрактика к разделу "
          "[«Папки: exists(), is_file(), mkdir()»](../../site/chapters/glava-15/15-19-papki-exists-mkdir.html).")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

p = Path("nesuschestvuyuschaya_papka")
exists_before = p.exists()

Path("vlozhennaya/papka").mkdir(parents=True, exist_ok=True)
created = Path("vlozhennaya/papka").is_dir()
print(exists_before, created)''')
    nb.md("## Задание ★ Базовая практика")
    nb.code('''from pathlib import Path

Path("vlozhennaya/papka/fajl.txt").write_text("ok", encoding="utf-8")
is_file_check = Path("vlozhennaya/papka/fajl.txt").is_file()
print(is_file_check)''')
    nb.write(OUT_DIR / "15-19-papki-exists-mkdir.ipynb")
    print(f"Записано: 15-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-20 · Поиск файлов: iterdir() и glob()\n\nПрактика к разделу "
          "[«iterdir() и glob()»](../../site/chapters/glava-15/15-20-poisk-fajlov-glob.html).")
    nb.md("## Подготовка")
    nb.code('''from pathlib import Path

Path("otchet_dir").mkdir(exist_ok=True)
Path("otchet_dir/a.txt").write_text("1", encoding="utf-8")
Path("otchet_dir/b.csv").write_text("2", encoding="utf-8")
Path("otchet_dir/c.txt").write_text("3", encoding="utf-8")
print("Готово.")''')
    nb.md("## Рабочий пример — мини-проект: отчёт по папке")
    nb.code('''from pathlib import Path

vse_items = sorted(p.name for p in Path("otchet_dir").iterdir())
txt_files = sorted(p.name for p in Path("otchet_dir").glob("*.txt"))
print(vse_items)
print(txt_files)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПостройте отчёт вида "
          "«имя — файл/папка» для каждого элемента `otchet_dir`, используя `is_dir()`.")
    nb.code('''from pathlib import Path

otchet = []
for item in sorted(Path("otchet_dir").iterdir()):
    vid = "папка" if item.is_dir() else "файл"
    otchet.append(f"{item.name} — {vid}")
print(otchet)''')
    nb.write(OUT_DIR / "15-20-poisk-fajlov-glob.ipynb")
    print(f"Записано: 15-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-21 · Переименование, копирование, удаление\n\nПрактика к разделу "
          "[«Переименование, копирование, удаление»](../../site/chapters/glava-15/15-21-pereimenovanie-kopirovanie-udalenie.html).")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path
import shutil

Path("chernovik2.txt").write_text("draft", encoding="utf-8")
Path("chernovik2.txt").rename("gotovo2.txt")
rename_ok = Path("gotovo2.txt").exists() and not Path("chernovik2.txt").exists()

shutil.copy("gotovo2.txt", "gotovo2_backup.txt")
copy_ok = Path("gotovo2_backup.txt").read_text(encoding="utf-8") == "draft"
print(rename_ok, copy_ok)''')
    nb.md("## Задание ★ Базовая практика — безопасное удаление")
    nb.code('''from pathlib import Path

Path("vremenny2.txt").write_text("temp", encoding="utf-8")
Path("vremenny2.txt").unlink()
delete_ok = not Path("vremenny2.txt").exists()
print(delete_ok)''')
    nb.write(OUT_DIR / "15-21-pereimenovanie-kopirovanie-udalenie.ipynb")
    print(f"Записано: 15-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-22 · Ошибки файловой системы\n\nПрактика к разделу "
          "[«Ошибки файловой системы»](../../site/chapters/glava-15/15-22-oshibki-fajlovoj-sistemy.html).")
    nb.md("## Рабочий пример — FileNotFoundError")
    nb.code('''from pathlib import Path

not_found_caught = False
try:
    Path("net_takogo_fajla.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    not_found_caught = True
print(not_found_caught)''')
    nb.md("## Задание ★★ Самостоятельная задача — IsADirectoryError")
    nb.code('''from pathlib import Path

Path("papka_test").mkdir(exist_ok=True)
is_dir_error_caught = False
try:
    open("papka_test", "r", encoding="utf-8")
except IsADirectoryError:
    is_dir_error_caught = True
print(is_dir_error_caught)''')
    nb.write(OUT_DIR / "15-22-oshibki-fajlovoj-sistemy.ipynb")
    print(f"Записано: 15-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-23 · Большие файлы и потоковая обработка\n\nПрактика к разделу "
          "[«Большие файлы и потоковая обработка»](../../site/chapters/glava-15/15-23-bolshie-fajly-i-potoki.html).")
    nb.md("## Подготовка")
    nb.code('''from pathlib import Path

text_for_analysis = "первая строка\\nвторая строка чуть длиннее\\nтретья\\n"
Path("analiz2.txt").write_text(text_for_analysis, encoding="utf-8")
print("Готово.")''')
    nb.md("## Рабочий пример — мини-проект: анализатор текстового файла")
    nb.code('''from pathlib import Path

def analiz_fajla(path):
    stroki = 0
    slova = 0
    simvoly = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stroki += 1
            slova += len(line.split())
            simvoly += len(line)
    return {"строки": stroki, "слова": slova, "символы": simvoly}

result = analiz_fajla(Path("analiz2.txt"))
print(result)''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте к отчёту размер файла в байтах через "
          "stat().st_size.")
    nb.code('''from pathlib import Path

razmer_v_baytah = Path("analiz2.txt").stat().st_size
print(razmer_v_baytah)''')
    nb.write(OUT_DIR / "15-23-bolshie-fajly-i-potoki.ipynb")
    print(f"Записано: 15-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-24 · Как выбрать формат хранения данных\n\nПрактика к разделу "
          "[«Как выбрать формат хранения данных»](../../site/chapters/glava-15/15-24-kak-vybrat-format.html).")
    nb.md("## Задание ★ Базовая практика\n\nДля каждой задачи выберите подходящий формат "
          "хранения: \"текст\", \"CSV\" или \"JSON\".")
    nb.code('''# настройки приложения (вложенная структура: тема, язык, размер окна)
vybor_dlya_nastroek = "JSON"

# таблица результатов игроков (одинаковые строки: имя, очки, уровень)
vybor_dlya_tablitsy_rezultatov = "CSV"

# простой список заметок, одна на строку
vybor_dlya_zametok = "текст"

print(vybor_dlya_nastroek, vybor_dlya_tablitsy_rezultatov, vybor_dlya_zametok)''')
    nb.write(OUT_DIR / "15-24-kak-vybrat-format.ipynb")
    print(f"Записано: 15-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-25 · JSON: сохраняем структуры данных\n\nПрактика к разделу "
          "[«JSON»](../../site/chapters/glava-15/15-25-json-serializatsiya.html).")
    nb.md("## Рабочий пример — dump/load")
    nb.code('''import json

data = {"name": "Anna", "score": 1200}
with open("igrok2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("igrok2.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded)''')
    nb.md("## Задание ★★ Самостоятельная задача — мини-проект: менеджер настроек")
    nb.code('''import json
from pathlib import Path

DEFAULT_SETTINGS = {"theme": "light", "language": "ru"}

def load_settings(path):
    if not path.exists():
        return dict(DEFAULT_SETTINGS)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(path, settings):
    with path.open("w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

settings_path = Path("nastroyki2.json")
settings_path.unlink(missing_ok=True)   # для повторяемости примера при повторном запуске
settings_missing = load_settings(settings_path)
save_settings(settings_path, {"theme": "dark", "language": "ru"})
settings_loaded = load_settings(settings_path)
print(settings_missing)
print(settings_loaded)''')
    nb.write(OUT_DIR / "15-25-json-serializatsiya.ipynb")
    print(f"Записано: 15-25 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-26 · Мини-проект — сохраняем Player\n\nПрактика к разделу "
          "[«Мини-проект: сохраняем Player»](../../site/chapters/glava-15/15-26-mini-proekt-save-player.html).")
    nb.md("## Рабочий пример")
    nb.code('''from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass
class Player:
    name: str
    score: int
    inventory: list

player = Player(name="Anna", score=1200, inventory=["меч", "щит"])
with Path("save2.json").open("w", encoding="utf-8") as f:
    json.dump(asdict(player), f, ensure_ascii=False, indent=2)''')
    nb.md("## Задание ★★ Самостоятельная задача — загрузка")
    nb.code('''with Path("save2.json").open("r", encoding="utf-8") as f:
    data = json.load(f)

loaded_player = Player(**data)
is_same_object = loaded_player is player
print(loaded_player == player)
print(is_same_object)
print(loaded_player.inventory)''')
    nb.write(OUT_DIR / "15-26-mini-proekt-save-player.ipynb")
    print(f"Записано: 15-26 ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-27 · CSV: таблицы в текстовом виде\n\nПрактика к разделу "
          "[«CSV»](../../site/chapters/glava-15/15-27-csv-tablitsy.html).")
    nb.md("## Рабочий пример — почему не split(\",\")")
    nb.code('''import csv
import io

stroka_s_zapyatoj = \'Anna,"Отлично, продолжай!"\'
reader = csv.reader(io.StringIO(stroka_s_zapyatoj))
razobrannaya_stroka = next(reader)
print(razobrannaya_stroka)''')
    nb.md("## Задание ★★ Самостоятельная задача — writer и DictReader")
    nb.code('''rows = [{"name": "Anna", "score": 1200}, {"name": "Bob", "score": 900}]
with open("rekordy2.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "score"])
    writer.writeheader()
    writer.writerows(rows)

with open("rekordy2.csv", "r", encoding="utf-8", newline="") as f:
    zagruzhennye = list(csv.DictReader(f))
print(zagruzhennye)''')
    nb.write(OUT_DIR / "15-27-csv-tablitsy.ipynb")
    print(f"Записано: 15-27 ({len(nb)} ячеек)")


def build_28() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-28 · Безопасная работа с файлами\n\nПрактика к разделу "
          "[«Безопасная работа с файлами»](../../site/chapters/glava-15/15-28-bezopasnaya-rabota-s-fajlami.html).")
    nb.md("## Рабочий пример — сохранение через временный файл")
    nb.code('''import json
from pathlib import Path

def bezopasno_sohranit(path, data):
    vremenny = path.with_suffix(path.suffix + ".tmp")
    with vremenny.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    vremenny.replace(path)

target = Path("bezopasno2.json")
bezopasno_sohranit(target, {"score": 500})

tmp_exists_after = target.with_suffix(target.suffix + ".tmp").exists()
result_data = json.loads(target.read_text(encoding="utf-8"))
print(tmp_exists_after)
print(result_data)''')
    nb.write(OUT_DIR / "15-28-bezopasnaya-rabota-s-fajlami.ipynb")
    print(f"Записано: 15-28 ({len(nb)} ячеек)")


def build_29() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-29 · Мини-проект — таблица рекордов\n\nПрактика к разделу "
          "[«Мини-проект: таблица рекордов»](../../site/chapters/glava-15/15-29-mini-proekt-rekordy-i-nastrojki.html).")
    nb.md("## Рабочий пример")
    nb.code('''import csv
from pathlib import Path

def load_rekordy(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [{"name": row["name"], "score": int(row["score"])} for row in reader]

def save_rekordy(path, rekordy):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "score"])
        writer.writeheader()
        writer.writerows(rekordy)

def top_n(rekordy, n):
    return sorted(rekordy, key=lambda r: r["score"], reverse=True)[:n]

path = Path("rekordy3.csv")
path.unlink(missing_ok=True)   # для повторяемости примера при повторном запуске
rekordy = load_rekordy(path)
rekordy.append({"name": "Anna", "score": 800})
rekordy.append({"name": "Bob", "score": 1500})
rekordy.append({"name": "Carlos", "score": 1200})
save_rekordy(path, rekordy)

top2 = top_n(load_rekordy(path), 2)
print(top2)''')
    nb.md("## Задание ★★★ Задача повышенной сложности\n\nДобавьте функцию, которая обновляет "
          "рекорд существующего игрока вместо добавления второй строки с тем же именем.")
    nb.code('''def add_or_update(rekordy, name, score):
    for zapis in rekordy:
        if zapis["name"] == name:
            zapis["score"] = max(zapis["score"], score)
            return rekordy
    rekordy.append({"name": name, "score": score})
    return rekordy

obnovlennye = add_or_update(list(rekordy), "Anna", 2000)
anna_score = next(z["score"] for z in obnovlennye if z["name"] == "Anna")
print(anna_score)''')
    nb.write(OUT_DIR / "15-29-mini-proekt-rekordy.ipynb")
    print(f"Записано: 15-29 ({len(nb)} ячеек)")


def build_30() -> None:
    nb = NotebookBuilder()
    nb.md("# 15-30 · Браузер и локальный диск: две файловые системы\n\nЛокальная практика к "
          "разделу [«Браузер и локальный диск»](../../site/chapters/glava-15/15-30-brauzer-vs-lokalny-disk.html).\n\n"
          "**Этот ноутбук выполняется локально** — смысл упражнения именно в том, чтобы увидеть "
          "настоящую персистентность на настоящем диске, а не в виртуальной файловой системе "
          "браузера.")
    nb.md("## Шаг 1 — создаём файл в реальной папке data/")
    nb.code('''from pathlib import Path

Path("data").mkdir(exist_ok=True)
Path("data/moya_zametka.txt").write_text("Привет с настоящего диска!", encoding="utf-8")
print("Файл записан в data/moya_zametka.txt")''')
    nb.md("## Шаг 2 — остановите выполнение, затем запустите ноутбук заново")
    nb.code('''from pathlib import Path

print(Path("data/moya_zametka.txt").read_text(encoding="utf-8"))''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nОткройте `data/moya_zametka.txt` в "
          "проводнике/Finder или в самом редакторе — убедитесь, что это настоящий файл на "
          "вашем диске, а не что-то видимое только внутри этого ноутбука.")
    nb.write(OUT_DIR / "15-30-brauzer-vs-lokalny-disk.ipynb")
    print(f"Записано: 15-30 ({len(nb)} ячеек)")


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
