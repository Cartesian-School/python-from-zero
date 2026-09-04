#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 23.

Глава 23 — два независимых блока практики:

1. 23-01..23-06 — приложение «Дополнительная практика: шесть мини-проектов
   для GitHub»: шесть домашних
   мини-проектов (калькулятор, генератор историй, «Камень, ножницы, бумага»,
   отскакивающие мячи, конвертер температуры, заметки). Tkinter- и
   Pygame-проекты используют те же headless-приёмы, что и в предыдущих
   главах: create-once/update()+destroy() вместо mainloop(), for-в-range()
   вместо игрового while, а физика мяча (Myach.shag(dt)) вообще не касается
   экрана и проверяется без единого вызова pygame.display.

2. 23-07..23-24 — основной материал главы: настоящий проект SafeSort
   (`projects/python/safesort/`), безопасный некомандный файл-организатор.
   Ноутбуки этой части либо буквально импортируют настоящий пакет safesort
   (там, где нужен доступ к файловой системе — local-required), либо
   воспроизводят его чистую логику внутри ноутбука один в один (там, где
   практика выполняется в браузере через Pyodide и у неё нет доступа к
   package safesort) — но в обоих случаях код и поведение соответствуют
   настоящему исходнику, а не упрощённой выдумке.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter23_practice_model import apply_practice_model
from notebook_lib import NotebookBuilder as BaseNotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-23"


class NotebookBuilder(BaseNotebookBuilder):
    """Chapter-local builder enforcing the final task pedagogy contract."""

    def write(self, path: Path) -> Path:
        lesson_id = path.name[:5]
        self._cells = apply_practice_model(self._cells, lesson_id)
        stable_prefixes = ("task-", "tests-", "setup-", "diagnostic-")
        for index, cell in enumerate(self._cells):
            current_id = cell.get("id", "")
            if not current_id.startswith(stable_prefixes):
                cell["id"] = f"cell-{lesson_id}-{index:02d}"
        return super().write(path)


# ---------------------------------------------------------------------------
# 23-01..23-06 — приложение: шесть домашних мини-проектов
# ---------------------------------------------------------------------------


def build_01_kalkulyator() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-01 · Калькулятор\n\nПрактика к разделу "
          "[«Домашний проект A: калькулятор с Tkinter»](../../site/chapters/glava-23/23-hw-01-kalkulyator.html). "
          "Полный файл — `projects/tkinter/calculator/calculator.py`.")
    nb.md("## Цель\n\nПроверить безопасное вычисление выражений через "
          "`vychislit_vyrazhenie()` и последовательность нажатий кнопок, как это "
          "делал бы настоящий пользователь.")
    nb.md("## Рабочий пример")
    nb.code('''import sys

sys.path.insert(0, "../../projects/tkinter/calculator")
import calculator as c

print(c.vychislit_vyrazhenie("2+2"))
print(c.vychislit_vyrazhenie("10-3*2"))
print(c.vychislit_vyrazhenie("(1+2)*3"))
print(c.vychislit_vyrazhenie("7/2"))''')
    nb.md("## Проверка результата")
    nb.code('''assert c.vychislit_vyrazhenie("2+2") == "4"
assert c.vychislit_vyrazhenie("10-3*2") == "4"
assert c.vychislit_vyrazhenie("(1+2)*3") == "9"
assert c.vychislit_vyrazhenie("7/2") == "3.5"
print("Верно: базовые вычисления совпадают с ожидаемыми.")''')
    nb.md("## Эксперимент — некорректный и опасный ввод не приводит к падению")
    nb.code('''print(c.vychislit_vyrazhenie("5/0"))
print(c.vychislit_vyrazhenie("2+*3"))
print(c.vychislit_vyrazhenie("import os"))

assert c.vychislit_vyrazhenie("5/0") == "Ошибка"
assert c.vychislit_vyrazhenie("2+*3") == "Ошибка"
assert c.vychislit_vyrazhenie("import os") == "Ошибка"
print("Верно: деление на ноль, синтаксическая ошибка и посторонний код — везде «Ошибка».")''')
    nb.md("## Почему это безопасно — два независимых барьера\n\n"
          "1. **Белый список символов**: функция сначала проверяет "
          "`set(vyrazhenie) <= DOPUSTIMYE_SIMVOLY` — строка должна состоять только "
          "из цифр, `+ - * / ( ) .` и пробелов. Буквы в `\"import os\"` не входят в "
          "этот список, поэтому функция возвращает `\"Ошибка\"` ещё **до** вызова "
          "`ast.parse()` — до разбора дело просто не доходит.\n"
          "2. **Разбор через `ast.parse(..., mode=\"eval\")`**: строка вроде "
          "`\"2+*3\"` состоит только из разрешённых символов, но не является "
          "корректным арифметическим выражением — `ast.parse()` поднимает "
          "`SyntaxError`, который тоже перехватывается и превращается в "
          "`\"Ошибка\"`. А то, что всё-таки разобралось, дополнительно проверяется "
          "узел за узлом в `vychislit_uzel()`: разрешены только числа, "
          "`+ - * /` и унарный минус — никаких имён и вызовов.")
    nb.md("## Задание ★ Базовая практика\n\nСмоделируйте нажатия кнопок «1», «2», "
          "«+», «8», «=» через `SostoyanieKalkulyatora` — тот же класс, что "
          "хранит состояние экрана внутри `main()` — и проверьте результат.")
    nb.code('''sostoyanie = c.SostoyanieKalkulyatora()
for simvol in "12+8":
    sostoyanie.na_cifru_ili_znak_nazhali(simvol)

assert sostoyanie.na_ekrane() == "12+8"
sostoyanie.na_ravno_nazhali()

assert sostoyanie.na_ekrane() == "20"
print("Верно: 12 + 8 = 20 на экране калькулятора.")''')
    nb.write(OUT_DIR / "23-01-kalkulyator.ipynb")
    print(f"Записано: 23-01 ({len(nb)} ячеек)")


def build_02_generator_istorij() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-02 · Генератор случайных историй\n\nПрактика к разделу "
          "[«Домашний проект B: генератор случайных историй»]"
          "(../../site/chapters/glava-23/23-hw-02-generator-istorij.html). "
          "Полный файл — `projects/console/story-generator/story_generator.py`.")
    nb.md("## Цель\n\nСгенерировать несколько историй и убедиться, что каждая собрана из "
          "ожидаемых списков слов.")
    nb.md("## Рабочий пример")
    nb.code('''import sys
import random

sys.path.insert(0, "../../projects/console/story-generator")
import story_generator as sg

random.seed(7)
for _ in range(3):
    print(sg.sluchajnaya_istoriya())''')
    nb.md("## Проверка результата")
    nb.code('''for _ in range(50):
    istoriya = sg.sluchajnaya_istoriya()
    assert any(p in istoriya for p in sg.PRILAGATELNYE)
    assert any(s in istoriya for s in sg.SUSHESTVITELNYE)
    assert any(m in istoriya for m in sg.MESTA)
    assert any(g in istoriya for g in sg.GLAGOLY)
    assert any(pr in istoriya for pr in sg.PREDMETY)
    assert istoriya.startswith("Однажды") and istoriya.endswith("прежней.")

print("Верно: 50 случайных историй — и все построены по шаблону.")''')
    nb.md("## Задание ★ Базовая практика\n\nПодсчитайте, сколько всего различных историй "
          "теоретически может собрать генератор.")
    nb.code('''kolichestvo_variantov = (
    len(sg.PRILAGATELNYE)
    * len(sg.SUSHESTVITELNYE)
    * len(sg.MESTA)
    * len(sg.GLAGOLY)
    * len(sg.PREDMETY)
)
print("Всего возможных историй:", kolichestvo_variantov)
assert kolichestvo_variantov == 5 * 5 * 4 * 5 * 4''')
    nb.write(OUT_DIR / "23-02-generator-istorij.ipynb")
    print(f"Записано: 23-02 ({len(nb)} ячеек)")


def build_03_rps() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-03 · Камень, ножницы, бумага\n\nПрактика к разделу "
          "[«Домашний проект C: игра «Камень, ножницы, бумага»»]"
          "(../../site/chapters/glava-23/23-hw-03-kamen-nozhnicy-bumaga.html). "
          "Полный файл — `projects/console/rock-paper-scissors/rps.py`.")
    nb.md("## Цель\n\nПроверить логику победителя для всех девяти комбинаций и симулировать "
          "несколько раундов.")
    nb.md("## Рабочий пример — все комбинации")
    nb.code('''import sys
import random

sys.path.insert(0, "../../projects/console/rock-paper-scissors")
import rps

for a in rps.VARIANTY:
    for b in rps.VARIANTY:
        print(f"{a} против {b}: {rps.opredelit_pobeditelya(a, b)}")''')
    nb.md("## Проверка результата")
    nb.code('''assert rps.opredelit_pobeditelya("камень", "ножницы") == "игрок"
assert rps.opredelit_pobeditelya("ножницы", "камень") == "компьютер"
assert rps.opredelit_pobeditelya("бумага", "бумага") == "ничья"
print("Верно: словарь POBEZHDAET определяет победителя правильно.")''')
    nb.md("## Эксперимент — симулируем 200 раундов и считаем статистику")
    nb.code('''random.seed(5)
schet = {"игрок": 0, "компьютер": 0, "ничья": 0}

for _ in range(200):
    _, pobeditel = rps.sygrat_raund("камень")
    schet[pobeditel] += 1

print("Статистика за 200 раундов (всегда «камень»):", schet)
assert sum(schet.values()) == 200
assert schet["игрок"] > 0 and schet["компьютер"] > 0
print("Верно: за 200 случайных раундов встретились все три исхода.")''')
    nb.write(OUT_DIR / "23-03-kamen-nozhnicy-bumaga.ipynb")
    print(f"Записано: 23-03 ({len(nb)} ячеек)")


def build_04_myach() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-04 · Отскакивающий мяч (класс)\n\nПрактика к разделу "
          "[«Домашний проект D: отскакивающие мячи с Pygame»]"
          "(../../site/chapters/glava-23/23-hw-04-otskakivayushie-myachi.html). "
          "Полный файл — `projects/pygame/bouncing-balls-oop/bouncing_balls.py`.")
    nb.md("## Про этот ноутбук\n\nВ отличие от главы 20-21 здесь не нужен даже "
          "for-в-range() вместо игрового while: класс `Myach` и его метод "
          "`shag(dt)` вообще ни разу не касаются экрана — окно и вызовы "
          "`pygame.display` есть только внутри `main()`. Это позволяет проверять "
          "физику мяча совсем без дисплея.")
    nb.md("## Рабочий пример")
    nb.code('''import sys

sys.path.insert(0, "../../projects/pygame/bouncing-balls-oop")
import bouncing_balls as bb

myach = bb.Myach(x=300, y=200, vx=100, vy=50, radius=15, cvet=(255, 100, 100))
print(myach.pos, myach.velocity, myach.otskokov)''')
    nb.md("## Проверка результата — одна и та же секунда, разное число кадров")
    nb.code('''def proigrat_sekundu(obrazec, kolichestvo_kadrov):
    myach = bb.Myach(
        obrazec.pos.x, obrazec.pos.y, obrazec.velocity.x, obrazec.velocity.y,
        obrazec.radius, obrazec.cvet,
    )
    dt = 1 / kolichestvo_kadrov
    for _ in range(kolichestvo_kadrov):
        myach.shag(dt)
    return myach.pos


pozicii = {n: proigrat_sekundu(myach, n) for n in (30, 60, 120)}
for n, poz in pozicii.items():
    print(n, "кадров/сек ->", poz)

assert abs(pozicii[30].x - pozicii[60].x) < 1e-6
assert abs(pozicii[30].y - pozicii[60].y) < 1e-6
assert abs(pozicii[30].x - pozicii[120].x) < 1e-6
assert abs(pozicii[30].y - pozicii[120].y) < 1e-6
print("Верно для свободного равномерного движения: позиции совпали в пределах численной "
      "точности. При дискретных столкновениях результат всё ещё может зависеть от dt.")''')
    nb.md("## Эксперимент — отскок от стены тоже считается через dt")
    nb.code('''myach_u_steny = bb.Myach(x=bb.SHIRINA - 20, y=200, vx=200, vy=0, radius=15, cvet=(100, 200, 255))
for _ in range(60):
    myach_u_steny.shag(1 / 60)

print("Позиция:", myach_u_steny.pos, "отскоков:", myach_u_steny.otskokov)
assert myach_u_steny.otskokov >= 1
assert myach_u_steny.radius <= myach_u_steny.pos.x <= bb.SHIRINA - myach_u_steny.radius
print("Верно: мяч отразился от правой стены и остался внутри границ экрана.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоздайте три мяча через "
          "`sozdat_myachi(3)` и прогоните 300 кадров по 1/60 секунды — проверьте, "
          "что все мячи остаются внутри границ экрана и у каждого хотя бы один отскок.")
    nb.code('''myachi = bb.sozdat_myachi(3)
for _ in range(300):
    for m in myachi:
        m.shag(1 / 60)

for m in myachi:
    assert m.radius <= m.pos.x <= bb.SHIRINA - m.radius
    assert m.radius <= m.pos.y <= bb.VYSOTA - m.radius
    assert m.otskokov > 0

print("Отскоков у каждого мяча:", [m.otskokov for m in myachi])
print("Верно: после 300 кадров все мячи внутри экрана и хотя бы раз отскочили.")''')
    nb.write(OUT_DIR / "23-04-otskakivayushij-myach.ipynb")
    print(f"Записано: 23-04 ({len(nb)} ячеек)")


def build_05_temperatura() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-05 · Преобразование температуры\n\nПрактика к разделу "
          "[«Домашний проект E: приложение для преобразования температуры»]"
          "(../../site/chapters/glava-23/23-hw-05-temperatura.html). "
          "Полный файл — `projects/tkinter/temperature-converter/temperature_converter.py`.")
    nb.md("## Цель\n\nПроверить формулы перевода на известных опорных точках и "
          "убедиться, что `preobrazovat()` отклоняет физически невозможные значения.")
    nb.md("## Рабочий пример")
    nb.code('''import sys

sys.path.insert(0, "../../projects/tkinter/temperature-converter")
import temperature_converter as tc

print(tc.preobrazovat(0, "C"))
print(tc.preobrazovat(100, "C"))
print(tc.preobrazovat(32, "F"))
print(tc.preobrazovat(0, "K"))''')
    nb.md("## Проверка результата")
    nb.code('''r = tc.preobrazovat(0, "C")
assert abs(r["F"] - 32) < 1e-9
assert abs(r["K"] - 273.15) < 1e-9

r = tc.preobrazovat(100, "C")
assert abs(r["F"] - 212) < 1e-9

r = tc.preobrazovat(32, "F")
assert abs(r["C"] - 0) < 1e-9

r = tc.preobrazovat(0, "K")
assert abs(r["C"] - (-273.15)) < 1e-9

print("Верно: 0 °C = 32 °F = 273.15 K, 100 °C = 212 °F, 0 K = -273.15 °C.")''')
    nb.md("## Эксперимент — ниже абсолютного нуля такой температуры не существует")
    nb.code('''tc.preobrazovat(-274, "C")''', raises=True)
    nb.md("## Как это выглядит в коде\n\nВызов выше завершился трассировкой "
          "`ValueError` — так и задумано: `preobrazovat()` не пытается тихо "
          "«исправить» физически невозможное значение, а поднимает понятную "
          "ошибку. Настоящий обработчик кнопки внутри `main()` перехватывает "
          "именно этот `ValueError` и показывает пользователю фразу «Такой "
          "температуры не существует — ниже абсолютного нуля» вместо падения "
          "программы.")
    nb.code('''try:
    tc.preobrazovat(-460, "F")   # ниже -459.67°F — тоже ниже абсолютного нуля
except ValueError as oshibka:
    poymano = True
    tekst_oshibki = str(oshibka)
else:
    poymano = False

assert poymano is True
assert "абсолютного нуля" in tekst_oshibki
print("Верно: значение ниже абсолютного нуля в градусах Фаренгейта тоже отклоняется.")''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что 0 Кельвин (абсолютный "
          "ноль) — ещё допустимое значение, а -0.01 K — уже нет.")
    nb.code('''assert tc.preobrazovat(0, "K")["C"] == -273.15  # ровно абсолютный ноль — ещё допустимо

try:
    tc.preobrazovat(-0.01, "K")
    proshlo_bez_oshibki = True
except ValueError:
    proshlo_bez_oshibki = False

assert proshlo_bez_oshibki is False
print("Верно: 0 K допустим, а отрицательные значения в Кельвинах — нет.")''')
    nb.write(OUT_DIR / "23-05-temperatura.ipynb")
    print(f"Записано: 23-05 ({len(nb)} ячеек)")


def build_06_fajly_tkinter() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-06 · Файлы и Tkinter\n\nПрактика к разделу "
          "[«Домашний проект F: приложение «Заметки»»]"
          "(../../site/chapters/glava-23/23-hw-06-zametki.html). "
          "Полный файл — `projects/tkinter/notes-app/notes_app.py`.")
    nb.md("## Цель\n\nПроверить сохранение и загрузку заметки через чистые "
          "функции `sohranit_v_fajl()`/`zagruzit_iz_fajla()`, а также поведение "
          "при отсутствии сохранённого файла.")
    nb.md("## Рабочий пример")
    nb.code('''import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "../../projects/tkinter/notes-app")
import notes_app as na

katalog = tempfile.TemporaryDirectory()
put_k_zametke = Path(katalog.name) / "zametka.txt"

print("Файл существует до сохранения:", put_k_zametke.exists())''')
    nb.md("## Проверка результата — загрузка несуществующего файла поднимает понятную ошибку")
    nb.code('''try:
    na.zagruzit_iz_fajla(put_k_zametke)
    fajl_najden = True
except FileNotFoundError:
    fajl_najden = False

assert fajl_najden is False
print("Верно: попытка загрузки без сохранённого файла поднимает FileNotFoundError, "
      "а не падает трудночитаемой ошибкой позже.")''')
    nb.md("## Эксперимент — сохраняем и загружаем заметку")
    nb.code('''tekst_zametki = "Купить молоко\\nПозвонить маме"
na.sohranit_v_fajl(put_k_zametke, tekst_zametki)

assert put_k_zametke.exists()
assert put_k_zametke.read_text(encoding="utf-8") == tekst_zametki
print("Верно: sohranit_v_fajl() записывает переданный текст в файл в кодировке UTF-8.")

zagruzhennyj_tekst = na.zagruzit_iz_fajla(put_k_zametke)
assert zagruzhennyj_tekst == tekst_zametki
print("Верно: zagruzit_iz_fajla() возвращает ровно то, что было сохранено.")''')
    nb.md("## Задание ★ Базовая практика\n\nПерезапишите файл текстом с "
          "кириллицей, переносами строк и эмодзи, убедитесь, что кодировка "
          "UTF-8 не искажает текст, а затем уберите временный каталог.")
    nb.code('''novyj_tekst = "Список покупок:\\n- хлеб\\n- сыр\\n- яблоки 🍎"
na.sohranit_v_fajl(put_k_zametke, novyj_tekst)

assert na.zagruzit_iz_fajla(put_k_zametke) == novyj_tekst
print("Верно: UTF-8 сохраняет кириллицу, переносы строк и эмодзи без искажений.")

katalog.cleanup()
assert not put_k_zametke.exists()
print("Временный каталог удалён.")''')
    nb.write(OUT_DIR / "23-06-fajly-tkinter.ipynb")
    print(f"Записано: 23-06 ({len(nb)} ячеек)")


# ---------------------------------------------------------------------------
# 23-07..23-24 — SafeSort
# ---------------------------------------------------------------------------


def build_07_argparse_cli() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-07 · Разбор аргументов командной строки\n\nПрактика к разделу "
          "[«pyproject.toml и установка проекта»](../../site/chapters/glava-23/23-05-pyproject-toml.html) "
          "и разделу [«Командная строка SafeSort»](../../site/chapters/glava-23/23-06-komandnaya-stroka.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/cli.py`.")
    nb.md("## Цель\n\nСобрать парсер, который повторяет форму настоящего "
          "`safesort.cli.build_parser()`: пять подкоманд, у каждой — позиционный "
          "аргумент `root`, а `undo` умеет обходиться и вовсе без аргумента.")
    nb.md("## Рабочий пример")
    nb.code('''import argparse
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(
        prog="safesort",
        description=(
            "SafeSort: a safe, non-destructive file organizer. "
            "scan/plan/duplicates are read-only; 'apply' sorts and 'undo' restores files."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("scan", "plan", "apply", "duplicates"):
        sub = subparsers.add_parser(name)
        sub.add_argument("root", type=Path)

    undo_parser = subparsers.add_parser("undo")
    undo_parser.add_argument("root", type=Path, nargs="?", default=Path("."))

    return parser


parser = build_parser()

args_scan = parser.parse_args(["scan", "/home/anna/Downloads"])
args_apply = parser.parse_args(["apply", "/home/anna/Downloads"])
args_undo_default = parser.parse_args(["undo"])
args_undo_explicit = parser.parse_args(["undo", "/home/anna/Downloads"])

print(args_scan)
print(args_undo_default)''')
    nb.md("## Проверка результата")
    nb.code('''assert args_scan.command == "scan"
assert args_scan.root == Path("/home/anna/Downloads")
assert args_apply.command == "apply"
assert args_undo_default.command == "undo"
assert args_undo_default.root == Path(".")
assert args_undo_explicit.root == Path("/home/anna/Downloads")
print("Верно: пять подкоманд разобраны, а undo получает root по умолчанию, если он не передан.")''')
    nb.md("## Эксперимент — без подкоманды argparse сам сообщает об ошибке")
    nb.code('''import contextlib
import io

buffer = io.StringIO()
try:
    with contextlib.redirect_stderr(buffer):
        parser.parse_args([])
    kod_zaversheniya = None
except SystemExit as exc:
    kod_zaversheniya = exc.code

print("Код завершения:", kod_zaversheniya)
assert kod_zaversheniya is not None and kod_zaversheniya != 0
print("Верно: dest=\\"command\\", required=True сам формирует понятную ошибку без ручных проверок.")''')
    nb.md("## Задание ★ Базовая практика\n\nРазберите "
          "`[\"duplicates\", \"/home/anna/Photos\"]` и проверьте, что команда — "
          "duplicates, а root — правильный путь.")
    nb.code('''zadanie_args = parser.parse_args(["duplicates", "/home/anna/Photos"])

assert zadanie_args.command == "duplicates"
assert zadanie_args.root == Path("/home/anna/Photos")
print("Верно: duplicates разобрана с правильным путём.")''')
    nb.write(OUT_DIR / "23-07-argparse-cli.ipynb")
    print(f"Записано: 23-07 ({len(nb)} ячеек)")


def build_08_pathlib() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-08 · Операции с Path\n\nПрактика к разделу "
          "[«pathlib: работаем с путями и каталогами»](../../site/chapters/glava-23/23-07-pathlib.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/models.py`.")
    nb.md("## Цель\n\nПотренироваться в операциях над `Path` — оператор `/`, "
          "`.name`, `.suffix`, `.parent` — и собрать неизменяемую модель "
          "`FileInfo`, на которой строится вся модель данных SafeSort.")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path

koren = Path("/home/anna/Downloads")
fajl = koren / "otchet.pdf"

print(fajl.name)
print(fajl.suffix)
print(fajl.parent)''')
    nb.md("## Проверка результата")
    nb.code('''assert fajl.name == "otchet.pdf"
assert fajl.suffix == ".pdf"
assert fajl.parent == koren
assert (koren / "podkatalog" / "vlozhennyj.txt").parent.name == "podkatalog"
print("Верно: оператор / и атрибуты name/suffix/parent работают как ожидается.")''')
    nb.md("## FileInfo — неизменяемая модель данных")
    nb.code('''from dataclasses import dataclass, FrozenInstanceError


@dataclass(frozen=True)
class FileInfo:
    path: Path
    size: int
    extension: str


primer = FileInfo(path=fajl, size=204800, extension=fajl.suffix.lower())
print(primer)

try:
    primer.size = 0
except FrozenInstanceError as oshibka:
    print("Изменить поле нельзя:", oshibka)''')
    nb.md("## Задание ★ Базовая практика\n\nСоберите `FileInfo` для файла "
          "`photo.JPG` размером 2048 байт и проверьте, что расширение "
          "приведено к нижнему регистру, как это делает настоящий сканер.")
    nb.code('''put_k_foto = koren / "photo.JPG"
zadanie_info = FileInfo(path=put_k_foto, size=2048, extension=put_k_foto.suffix.lower())

assert zadanie_info.extension == ".jpg"
assert zadanie_info.size == 2048
assert zadanie_info.path.name == "photo.JPG"
print("Верно:", zadanie_info)''')
    nb.write(OUT_DIR / "23-08-pathlib.ipynb")
    print(f"Записано: 23-08 ({len(nb)} ячеек)")


def build_09_scan() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-09 · Сканируем настоящий каталог\n\nПрактика к разделу "
          "[«Сканируем каталог»](../../site/chapters/glava-23/23-08-skaniruem-katalog.html). "
          "Использует настоящий пакет `safesort` (`projects/python/safesort/`).")
    nb.md("## Цель\n\nПрогнать настоящую функцию `safesort.scanner.scan()` по "
          "временному каталогу с вложенными файлами и убедиться, что она "
          "находит именно то, что нужно, — и ничего лишнего.")
    nb.md("## Рабочий пример")
    nb.code('''import tempfile
from pathlib import Path

from safesort.config import Config
from safesort.scanner import scan

tmpdir = tempfile.TemporaryDirectory()
koren = Path(tmpdir.name)

(koren / "podkatalog").mkdir()
(koren / "podkatalog" / "otchet.pdf").write_text("...", encoding="utf-8")
(koren / "photo.jpg").write_text("...", encoding="utf-8")
(koren / ".git").mkdir()
(koren / ".git" / "config").write_text("...", encoding="utf-8")

fajly = scan(koren, Config())
imena = {f.path.name for f in fajly}
print("Найдено файлов:", len(fajly))
print(imena)''')
    nb.md("## Проверка результата")
    nb.code('''assert imena == {"otchet.pdf", "photo.jpg"}
assert all(f.path.name != "config" for f in fajly)  # .git исключён по умолчанию
print("Верно: сканер нашёл вложенный файл и файл в корне, но не заглянул в .git.")''')
    nb.md("## Эксперимент — повторный запуск не находит уже отсортированные файлы")
    nb.code('''(koren / "Sorted" / "documents").mkdir(parents=True)
(koren / "Sorted" / "documents" / "staryj.pdf").write_text("...", encoding="utf-8")

fajly_posle = scan(koren, Config())
imena_posle = {f.path.name for f in fajly_posle}

assert "staryj.pdf" not in imena_posle
assert imena_posle == {"otchet.pdf", "photo.jpg"}
print("Верно: каталог результата Sorted/ исключён из повторного сканирования.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте символическую "
          "ссылку на `photo.jpg` и убедитесь, что сканер её пропускает.")
    nb.code('''ssylka = koren / "ssylka_na_foto.jpg"
try:
    ssylka.symlink_to(koren / "photo.jpg")
    podderzhivayutsya_ssylki = True
except (OSError, NotImplementedError):
    podderzhivayutsya_ssylki = False

if podderzhivayutsya_ssylki:
    fajly_so_ssylkoj = scan(koren, Config())
    imena_so_ssylkoj = {f.path.name for f in fajly_so_ssylkoj}
    assert "ssylka_na_foto.jpg" not in imena_so_ssylkoj
    print("Верно: символическая ссылка не попала в список найденных файлов.")
else:
    print("Символические ссылки не поддерживаются в этом окружении — пропускаем эту проверку.")

tmpdir.cleanup()''')
    nb.write(OUT_DIR / "23-09-scan.ipynb")
    print(f"Записано: 23-09 ({len(nb)} ячеек)")


def build_10_isklyucheniya() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-10 · Проверка исключённых каталогов\n\nПрактика к разделу "
          "[«Какие каталоги не нужно сканировать»](../../site/chapters/glava-23/23-09-isklyucheniya.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/config.py`.")
    nb.md("## Цель\n\nВоспроизвести `Config.excluded_names()` и проверить, что "
          "каталог результата и служебный `.safesort` исключены всегда — даже "
          "если их явно нет в пользовательских настройках.")
    nb.md("## Рабочий пример")
    nb.code('''from dataclasses import dataclass, field

DEFAULT_DESTINATION = "Sorted"
DEFAULT_EXCLUDE = (".git", ".venv")
STATE_DIRNAME = ".safesort"


@dataclass(frozen=True)
class Config:
    destination: str = DEFAULT_DESTINATION
    exclude: tuple = field(default_factory=lambda: DEFAULT_EXCLUDE)

    def excluded_names(self):
        return frozenset({*self.exclude, self.destination, STATE_DIRNAME})


nastrojki = Config()
print(sorted(nastrojki.excluded_names()))''')
    nb.md("## Проверка результата")
    nb.code('''imena_dlya_proverki = [".git", ".venv", "Sorted", ".safesort", "Downloads", "photo.jpg"]
propuskat = {imya: imya in nastrojki.excluded_names() for imya in imena_dlya_proverki}
print(propuskat)

assert propuskat[".git"] is True
assert propuskat["Sorted"] is True
assert propuskat[".safesort"] is True
assert propuskat["Downloads"] is False
assert propuskat["photo.jpg"] is False
print("Верно: обязательные исключения пропускаются, обычные имена — нет.")''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте `Config` со своим списком "
          "исключений (добавьте `\"node_modules\"`) и убедитесь, что теперь "
          "пропускается и он, а `Sorted/` и `.safesort` по-прежнему исключены "
          "всегда — даже если их явно нет в `exclude`.")
    nb.code('''svoi_nastrojki = Config(exclude=(".git", ".venv", "node_modules"))

assert "node_modules" in svoi_nastrojki.excluded_names()
assert "Sorted" in svoi_nastrojki.excluded_names()
assert ".safesort" in svoi_nastrojki.excluded_names()
print("Верно:", sorted(svoi_nastrojki.excluded_names()))''')
    nb.write(OUT_DIR / "23-10-isklyucheniya.ipynb")
    print(f"Записано: 23-10 ({len(nb)} ячеек)")


def build_11_klassifikator() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-11 · classify() и собственные категории\n\nПрактика к разделу "
          "[«Определяем категорию файла»](../../site/chapters/glava-23/23-10-klassifikaciya.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/classifier.py`.")
    nb.md("## Цель\n\nВоспроизвести `classify()` и проверить, что классификация "
          "по расширению регистронезависима, а неизвестное расширение всегда "
          "получает категорию `\"other\"`.")
    nb.md("## Рабочий пример")
    nb.code('''OTHER_CATEGORY = "other"

DEFAULT_EXTENSIONS = {
    "documents": [".pdf", ".docx", ".txt", ".odt"],
    "images": [".jpg", ".jpeg", ".png", ".webp"],
    "video": [".mp4", ".mkv", ".mov"],
    "audio": [".mp3", ".wav", ".flac"],
    "archives": [".zip", ".tar", ".gz", ".7z"],
    "code": [".py", ".js", ".ts", ".rs", ".java"],
    "data": [".json", ".csv", ".xml"],
}


def classify(extension, mapping):
    normalized = extension.lower()
    for category, extensions in mapping.items():
        lowered = {ext.lower() for ext in extensions}
        if normalized in lowered:
            return category
    return OTHER_CATEGORY


print(classify(".pdf", DEFAULT_EXTENSIONS))
print(classify(".PDF", DEFAULT_EXTENSIONS))
print(classify(".exe", DEFAULT_EXTENSIONS))''')
    nb.md("## Проверка результата")
    nb.code('''assert classify(".pdf", DEFAULT_EXTENSIONS) == "documents"
assert classify(".PNG", DEFAULT_EXTENSIONS) == "images"
assert classify(".py", DEFAULT_EXTENSIONS) == "code"
assert classify(".exe", DEFAULT_EXTENSIONS) == "other"
print("Верно: сравнение расширений регистронезависимо, а неизвестное расширение попадает в other.")''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте собственную категорию "
          "`presentations` (`.pptx`, `.key`) в копию словаря и убедитесь, что "
          "`classify()` её находит, не ломая остальные категории.")
    nb.code('''svoi_kategorii = {**DEFAULT_EXTENSIONS, "presentations": [".pptx", ".key"]}

assert classify(".pptx", svoi_kategorii) == "presentations"
assert classify(".key", svoi_kategorii) == "presentations"
assert classify(".pdf", svoi_kategorii) == "documents"
print("Верно: собственная категория работает наравне со встроенными.")''')
    nb.write(OUT_DIR / "23-11-klassifikator.ipynb")
    print(f"Записано: 23-11 ({len(nb)} ячеек)")


def build_12_plan() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-12 · Строим план из списка файлов\n\nПрактика к разделу "
          "[«От анализа к плану действий»](../../site/chapters/glava-23/23-11-plan-dejstvij.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/planner.py`.")
    nb.md("## Цель\n\nВоспроизвести `build_plan()` и убедиться, что каждый файл "
          "получает предсказуемый путь назначения `root/Sorted/<категория>/<имя>` "
          "— как обычные данные, без единого изменения файловой системы.")
    nb.md("## Рабочий пример — модели и вспомогательные функции")
    nb.code('''from dataclasses import dataclass
from pathlib import Path

OTHER_CATEGORY = "other"
DEFAULT_EXTENSIONS = {
    "documents": [".pdf", ".docx", ".txt", ".odt"],
    "images": [".jpg", ".jpeg", ".png", ".webp"],
    "archives": [".zip", ".tar", ".gz", ".7z"],
}


def classify(extension, mapping):
    normalized = extension.lower()
    for category, extensions in mapping.items():
        if normalized in {ext.lower() for ext in extensions}:
            return category
    return OTHER_CATEGORY


@dataclass(frozen=True)
class FileInfo:
    path: Path
    size: int
    extension: str


@dataclass(frozen=True)
class MoveOperation:
    source: Path
    destination: Path


@dataclass(frozen=True)
class SortPlan:
    root: Path
    operations: tuple''')
    nb.md("## build_plan() — план как данные")
    nb.code('''def _resolve_collision(candidate, reserved):
    if candidate not in reserved and not candidate.exists():
        return candidate
    stem, suffix, parent = candidate.stem, candidate.suffix, candidate.parent
    counter = 1
    while True:
        alternative = parent / f"{stem} ({counter}){suffix}"
        if alternative not in reserved and not alternative.exists():
            return alternative
        counter += 1


def build_plan(files, root, destination_name, extensions_mapping):
    root = Path(root)
    dest_root = root / destination_name
    reserved = set()
    operations = []
    for file in files:
        category = classify(file.extension, extensions_mapping)
        dest_dir = dest_root / category
        candidate = dest_dir / file.path.name
        destination = _resolve_collision(candidate, reserved)
        reserved.add(destination)
        operations.append(MoveOperation(source=file.path, destination=destination))
    return SortPlan(root=root, operations=tuple(operations))


koren = Path("/home/anna/Downloads")
fajly = [
    FileInfo(path=koren / "otchet.pdf", size=1200, extension=".pdf"),
    FileInfo(path=koren / "photo.jpg", size=204800, extension=".jpg"),
    FileInfo(path=koren / "archiv.zip", size=5000, extension=".zip"),
]

plan = build_plan(fajly, koren, "Sorted", DEFAULT_EXTENSIONS)
for op in plan.operations:
    print(op.source, "->", op.destination)''')
    nb.md("## Проверка результата")
    nb.code('''destinations = {op.source.name: op.destination for op in plan.operations}
assert destinations["otchet.pdf"] == koren / "Sorted" / "documents" / "otchet.pdf"
assert destinations["photo.jpg"] == koren / "Sorted" / "images" / "photo.jpg"
assert destinations["archiv.zip"] == koren / "Sorted" / "archives" / "archiv.zip"
print("Верно: каждый файл получил путь Sorted/<категория>/<имя>.")''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте в список файл с "
          "неизвестным расширением `.xyz` и проверьте, что он попал в "
          "`Sorted/other/`.")
    nb.code('''fajly_s_neizvestnym = fajly + [FileInfo(path=koren / "strannyj.xyz", size=10, extension=".xyz")]
plan2 = build_plan(fajly_s_neizvestnym, koren, "Sorted", DEFAULT_EXTENSIONS)

destination_neizvestnogo = next(
    op.destination for op in plan2.operations if op.source.name == "strannyj.xyz"
)
assert destination_neizvestnogo == koren / "Sorted" / "other" / "strannyj.xyz"
print("Верно:", destination_neizvestnogo)''')
    nb.write(OUT_DIR / "23-12-plan.ipynb")
    print(f"Записано: 23-12 ({len(nb)} ячеек)")


def build_13_executor() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-13 · Перемещаем файлы во временном каталоге\n\nПрактика к разделу "
          "[«Безопасно перемещаем файлы»](../../site/chapters/glava-23/23-13-peremeshaem-fajly.html). "
          "Использует настоящий пакет `safesort`.")
    nb.md("## Цель\n\nВызвать настоящую `safesort.executor.apply_plan()` во "
          "временном каталоге и убедиться, что она перемещает файлы и "
          "отказывается перезаписывать уже занятое место назначения.")
    nb.md("## Рабочий пример")
    nb.code('''import tempfile
from pathlib import Path

from safesort.executor import apply_plan
from safesort.models import MoveOperation, SortPlan

tmpdir = tempfile.TemporaryDirectory()
koren = Path(tmpdir.name)

istochnik = koren / "otchet.pdf"
istochnik.write_text("содержимое отчёта", encoding="utf-8")

naznachenie = koren / "Sorted" / "documents" / "otchet.pdf"
plan = SortPlan(root=koren, operations=(MoveOperation(source=istochnik, destination=naznachenie),))

rezultaty = apply_plan(plan)
print(rezultaty)''')
    nb.md("## Проверка результата")
    nb.code('''assert rezultaty[0].completed is True
assert not istochnik.exists()
assert naznachenie.exists()
assert naznachenie.read_text(encoding="utf-8") == "содержимое отчёта"
print("Верно: файл перемещён, содержимое не повреждено, исходное место пусто.")''')
    nb.md("## Эксперимент — существующий файл в месте назначения не перезаписывается")
    nb.code('''istochnik2 = koren / "zametka.txt"
istochnik2.write_text("новый текст", encoding="utf-8")

naznachenie2 = koren / "Sorted" / "documents" / "zametka.txt"
naznachenie2.parent.mkdir(parents=True, exist_ok=True)
naznachenie2.write_text("уже лежавший здесь текст", encoding="utf-8")

plan2 = SortPlan(root=koren, operations=(MoveOperation(source=istochnik2, destination=naznachenie2),))
rezultaty2 = apply_plan(plan2)

assert rezultaty2[0].completed is False
assert "already exists" in rezultaty2[0].error
assert istochnik2.exists()
assert naznachenie2.read_text(encoding="utf-8") == "уже лежавший здесь текст"
print("Верно: apply_plan отказался перезаписать существующий файл.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПереместите два файла в "
          "одном плане и проверьте, что оба оказались на месте.")
    nb.code('''a = koren / "a.txt"
b = koren / "b.txt"
a.write_text("A", encoding="utf-8")
b.write_text("B", encoding="utf-8")

plan3 = SortPlan(
    root=koren,
    operations=(
        MoveOperation(source=a, destination=koren / "Sorted" / "documents" / "a.txt"),
        MoveOperation(source=b, destination=koren / "Sorted" / "documents" / "b.txt"),
    ),
)
rezultaty3 = apply_plan(plan3)

assert all(r.completed for r in rezultaty3)
assert (koren / "Sorted" / "documents" / "a.txt").exists()
assert (koren / "Sorted" / "documents" / "b.txt").exists()
print("Верно: оба файла перемещены за один apply_plan.")

tmpdir.cleanup()''')
    nb.write(OUT_DIR / "23-13-executor.ipynb")
    print(f"Записано: 23-13 ({len(nb)} ячеек)")


def build_14_kollizii() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-14 · Безопасное имя при конфликте\n\nПрактика к разделу "
          "[«Что делать, если имя уже занято»](../../site/chapters/glava-23/23-14-imya-zanyato.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/planner.py`.")
    nb.md("## Цель\n\nВоспроизвести `_resolve_collision()` и убедиться, что "
          "свободное имя ищется по схеме `name (1).ext`, `name (2).ext`, ...")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path


def _resolve_collision(candidate, reserved):
    if candidate not in reserved and not candidate.exists():
        return candidate
    stem, suffix, parent = candidate.stem, candidate.suffix, candidate.parent
    counter = 1
    while True:
        alternative = parent / f"{stem} ({counter}){suffix}"
        if alternative not in reserved and not alternative.exists():
            return alternative
        counter += 1


papka = Path("/home/anna/Downloads/Sorted/documents")
kandidat = papka / "otchet.pdf"

reserved = set()
imena = []
for _ in range(3):
    novoe_imya = _resolve_collision(kandidat, reserved)
    reserved.add(novoe_imya)
    imena.append(novoe_imya)

print([i.name for i in imena])''')
    nb.md("## Проверка результата")
    nb.code('''assert imena[0].name == "otchet.pdf"
assert imena[1].name == "otchet (1).pdf"
assert imena[2].name == "otchet (2).pdf"
print("Верно: свободное имя находится по схеме name (n).ext.")''')
    nb.md("## Задание ★ Базовая практика\n\nПовторите то же самое для файла "
          "`photo.jpg` и убедитесь, что счётчик и расширение работают одинаково.")
    nb.code('''kandidat2 = papka.parent / "images" / "photo.jpg"
reserved2 = set()
imena2 = []
for _ in range(3):
    novoe = _resolve_collision(kandidat2, reserved2)
    reserved2.add(novoe)
    imena2.append(novoe)

assert [i.name for i in imena2] == ["photo.jpg", "photo (1).jpg", "photo (2).jpg"]
print("Верно:", [i.name for i in imena2])''')
    nb.write(OUT_DIR / "23-14-kollizii.ipynb")
    print(f"Записано: 23-14 ({len(nb)} ячеек)")


def build_15_manifest_json() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-15 · Манифест как обычный JSON\n\nПрактика к разделу "
          "[«Журнал выполненных операций»](../../site/chapters/glava-23/23-15-zhurnal-operacij.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/manifest.py`.")
    nb.md("## Цель\n\nСобрать манифест той же формы, что пишет настоящий "
          "`write_manifest()`, и убедиться, что он переживает "
          "`json.dumps()`/`json.loads()` без потерь.")
    nb.md("## Рабочий пример")
    nb.code('''import json
from pathlib import Path

operation_id = "20260824T011640800152"
moves = [
    {
        "source": str(Path("/home/anna/Downloads/otchet.pdf")),
        "destination": str(Path("/home/anna/Downloads/Sorted/documents/otchet.pdf")),
        "completed": True,
        "error": None,
    },
    {
        "source": str(Path("/home/anna/Downloads/zametka.txt")),
        "destination": str(Path("/home/anna/Downloads/Sorted/documents/zametka.txt")),
        "completed": False,
        "error": "destination already exists: ...",
    },
]

manifest = {
    "operation_id": operation_id,
    "root": str(Path("/home/anna/Downloads")),
    "timestamp": "2026-08-24T01:16:40",
    "moves": moves,
}

tekst_json = json.dumps(manifest, indent=2)
print(tekst_json)''')
    nb.md("## Проверка результата")
    nb.code('''zagruzhennyj = json.loads(tekst_json)

assert zagruzhennyj == manifest
assert zagruzhennyj["operation_id"] == operation_id
assert len(zagruzhennyj["moves"]) == 2
assert zagruzhennyj["moves"][0]["completed"] is True
assert zagruzhennyj["moves"][1]["error"] is not None
print("Верно: структура манифеста пережила dumps()/loads() без потерь.")''')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте, сколько перемещений в "
          "манифесте действительно завершились успешно (`completed=True`), "
          "не заглядывая в код вручную — только через `zagruzhennyj`.")
    nb.code('''uspeshnyh = sum(1 for move in zagruzhennyj["moves"] if move["completed"])

assert uspeshnyh == 1
print("Верно: успешных перемещений —", uspeshnyh)''')
    nb.write(OUT_DIR / "23-15-manifest-json.ipynb")
    print(f"Записано: 23-15 ({len(nb)} ячеек)")


def build_16_undo() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-16 · Отмена и конфликт при восстановлении\n\nПрактика к разделу "
          "[«Отмена последней операции»](../../site/chapters/glava-23/23-16-otmena-operacii.html). "
          "Использует настоящий пакет `safesort`.")
    nb.md("## Цель\n\nПрименить план, отменить его настоящей "
          "`safesort.manifest.undo()` и убедиться, что при конфликте (на "
          "исходном месте уже что-то есть) отмена отказывается перезаписывать.")
    nb.md("## Рабочий пример")
    nb.code('''import tempfile
from pathlib import Path

from safesort.config import Config
from safesort.scanner import scan
from safesort.planner import build_plan
from safesort.executor import apply_plan
from safesort.manifest import write_manifest, read_manifest, find_latest_manifest, undo

tmpdir = tempfile.TemporaryDirectory()
koren = Path(tmpdir.name)

(koren / "otchet.pdf").write_text("отчёт", encoding="utf-8")
(koren / "zametka.txt").write_text("заметка", encoding="utf-8")

nastrojki = Config()
fajly = scan(koren, nastrojki)
plan = build_plan(fajly, koren, nastrojki)
rezultaty = apply_plan(plan)
_manifest_obj, put_k_manifestu = write_manifest(koren, rezultaty)

print("Перемещено файлов:", sum(1 for r in rezultaty if r.completed))
print("Манифест записан в:", put_k_manifestu)''')
    nb.md("## Проверка результата — файлы действительно перемещены")
    nb.code('''assert not (koren / "otchet.pdf").exists()
assert not (koren / "zametka.txt").exists()
assert (koren / "Sorted" / "documents" / "otchet.pdf").exists()
assert put_k_manifestu.exists()
print("Верно: оба файла оказались в Sorted/documents/, манифест записан на диск.")''')
    nb.md("## Эксперимент — undo восстанавливает файлы")
    nb.code('''najdennyj_manifest = find_latest_manifest(koren)
manifest_dlya_otmeny = read_manifest(najdennyj_manifest)

rezultat_otmeny = undo(manifest_dlya_otmeny)

assert (koren / "otchet.pdf").exists()
assert (koren / "zametka.txt").exists()
assert rezultat_otmeny.conflicts == ()
print("Верно: оба файла вернулись на исходное место, конфликтов не было.")''')
    nb.md("## Задание ★★ Самостоятельная задача — конфликт при повторной "
          "отмене\n\nПовторите перемещение, затем создайте новый файл на "
          "исходном месте ДО отмены — и проверьте, что undo отказывается его "
          "затирать.")
    nb.code('''fajly2 = scan(koren, nastrojki)
plan2 = build_plan(fajly2, koren, nastrojki)
rezultaty2 = apply_plan(plan2)
_manifest_obj2, put_k_manifestu2 = write_manifest(koren, rezultaty2)

# кто-то создал новый файл на месте, откуда только что уехал otchet.pdf
(koren / "otchet.pdf").write_text("новый файл, положенный руками", encoding="utf-8")

manifest_dlya_otmeny2 = read_manifest(find_latest_manifest(koren))
rezultat_otmeny2 = undo(manifest_dlya_otmeny2)

assert len(rezultat_otmeny2.conflicts) == 1
assert rezultat_otmeny2.conflicts[0].source == koren / "otchet.pdf"
assert (koren / "otchet.pdf").read_text(encoding="utf-8") == "новый файл, положенный руками"
print("Верно: undo отказался перезаписать новый файл и сообщил о конфликте.")

tmpdir.cleanup()''')
    nb.write(OUT_DIR / "23-16-undo.ipynb")
    print(f"Записано: 23-16 ({len(nb)} ячеек)")


def build_17_sha256() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-17 · Хеш содержимого по частям\n\nПрактика к разделу "
          "[«SHA-256 и хеш содержимого файла»](../../site/chapters/glava-23/23-18-sha256.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/duplicates.py`.")
    nb.md("## Цель\n\nВоспроизвести `sha256_file()` — поблочное чтение файла — "
          "и сверить результат с `hashlib.sha256()`, вычисленным напрямую по "
          "всему содержимому.")
    nb.md("## Рабочий пример")
    nb.code('''import hashlib
from pathlib import Path

DEFAULT_CHUNK_SIZE = 1024 * 1024


def sha256_file(path, chunk_size=DEFAULT_CHUNK_SIZE):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


soderzhimoe = ("тестовое содержимое файла для проверки sha256_file " * 50).encode("utf-8")
put = Path("proverka_sha256.bin")
put.write_bytes(soderzhimoe)

print("Размер файла:", put.stat().st_size, "байт")
print("Дайджест:", sha256_file(put))''')
    nb.md("## Проверка результата")
    nb.code('''ozhidaemyj = hashlib.sha256(soderzhimoe).hexdigest()

assert sha256_file(put) == ozhidaemyj
assert sha256_file(put, chunk_size=16) == ozhidaemyj  # тот же результат при маленьком размере блока
print("Верно: результат sha256_file совпадает с hashlib.sha256() напрямую — при любом размере блока.")

put.unlink()  # временный файл больше не нужен -- дальше работаем только с soderzhimoe (bytes)''')
    nb.md("## Задание ★ Базовая практика\n\nИзмените хотя бы один байт "
          "содержимого и убедитесь, что дайджест изменился. Малое изменение обычно меняет "
          "много выходных битов, но не обязано менять каждую hex-цифру.")
    nb.code('''izmenennoe_soderzhimoe = b"x" + soderzhimoe[1:]
put2 = Path("proverka_sha256_izmenen.bin")
put2.write_bytes(izmenennoe_soderzhimoe)

digest_izmenennogo = sha256_file(put2)

assert digest_izmenennogo != sha256_file(put)
print("Верно: один изменённый байт дал совсем другой дайджест.")

put.unlink()
put2.unlink()''')
    nb.write(OUT_DIR / "23-17-sha256.ipynb")
    print(f"Записано: 23-17 ({len(nb)} ячеек)")


def build_18_duplicaty() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-18 · Группируем файлы в дубликаты\n\nПрактика к разделу "
          "[«Находим группы дубликатов»](../../site/chapters/glava-23/23-19-gruppy-dublikatov.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/duplicates.py`.")
    nb.md("## Цель\n\nВоспроизвести двухэтапную логику `find_duplicates()` "
          "(сначала группировка по размеру, потом по дайджесту) на синтетических "
          "записях, чтобы не создавать настоящие файлы на диске.")
    nb.md("## Рабочий пример")
    nb.code('''import hashlib
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class FileInfo:
    name: str
    size: int
    content: bytes


def find_duplicates(files):
    by_size = defaultdict(list)
    for file in files:
        by_size[file.size].append(file)

    groups = []
    for size, candidates in by_size.items():
        if len(candidates) < 2:
            continue
        by_digest = defaultdict(list)
        for candidate in candidates:
            digest = hashlib.sha256(candidate.content).hexdigest()
            by_digest[digest].append(candidate)
        for digest, matched in by_digest.items():
            if len(matched) >= 2:
                groups.append({"size": size, "digest": digest, "files": tuple(matched)})
    return groups


fajly = [
    FileInfo("notes.txt", 8, b"AAAAAAAA"),
    FileInfo("copy_of_notes.txt", 8, b"AAAAAAAA"),
    FileInfo("unikalnyj.txt", 8, b"BBBBBBBB"),   # тот же размер, другое содержимое
    FileInfo("photo1.jpg", 100, b"J" * 100),
    FileInfo("photo2.jpg", 100, b"J" * 100),
    FileInfo("odinokij.pdf", 55, b"P" * 55),      # уникальный размер — не может быть дубликатом
]

gruppy = find_duplicates(fajly)
for g in gruppy:
    print(g["size"], g["digest"][:12], [f.name for f in g["files"]])''')
    nb.md("## Проверка результата")
    nb.code('''imena_v_gruppah = {frozenset(f.name for f in g["files"]) for g in gruppy}

assert len(gruppy) == 2
assert frozenset({"notes.txt", "copy_of_notes.txt"}) in imena_v_gruppah
assert frozenset({"photo1.jpg", "photo2.jpg"}) in imena_v_gruppah
assert not any("odinokij.pdf" in imena for imena in imena_v_gruppah)
print("Верно: найдены ровно две группы дубликатов, уникальные файлы не попали ни в одну.")''')
    nb.md("## Задание ★★ Самостоятельная задача — пустые файлы тоже дубликаты")
    nb.code('''fajly_s_pustymi = fajly + [
    FileInfo("pustoj_a.txt", 0, b""),
    FileInfo("pustoj_b.txt", 0, b""),
]

gruppy2 = find_duplicates(fajly_s_pustymi)
gruppa_pustyh = next(g for g in gruppy2 if g["size"] == 0)

assert {f.name for f in gruppa_pustyh["files"]} == {"pustoj_a.txt", "pustoj_b.txt"}
assert gruppa_pustyh["digest"] == hashlib.sha256(b"").hexdigest()
print("Верно: два файла нулевого размера образовали отдельную группу дубликатов.")''')
    nb.write(OUT_DIR / "23-18-duplicaty.ipynb")
    print(f"Записано: 23-18 ({len(nb)} ячеек)")


def build_19_toml_config() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-19 · Читаем и проверяем TOML-настройки\n\nПрактика к разделу "
          "[«Настройки проекта»](../../site/chapters/glava-23/23-22-nastrojki-proekta.html). "
          "Настоящий файл — `projects/python/safesort/src/safesort/config.py`.")
    nb.md("## Цель\n\nРазобрать `safesort.toml`-подобный текст через `tomllib` "
          "и построить из него `Config`-подобный объект — с теми же значениями "
          "по умолчанию, что и настоящий `load_config()`.")
    nb.md("## Рабочий пример")
    nb.code('''import tomllib
from dataclasses import dataclass, field

DEFAULT_DESTINATION = "Sorted"
DEFAULT_EXCLUDE = (".git", ".venv")
DEFAULT_EXTENSIONS = {
    "documents": [".pdf", ".docx", ".txt", ".odt"],
    "images": [".jpg", ".jpeg", ".png", ".webp"],
}


@dataclass(frozen=True)
class Config:
    destination: str = DEFAULT_DESTINATION
    exclude: tuple = field(default_factory=lambda: DEFAULT_EXCLUDE)
    extensions: dict = field(default_factory=lambda: {k: list(v) for k, v in DEFAULT_EXTENSIONS.items()})


TEKST_TOML = """
destination = "Archive"
exclude = [".git", ".venv", "node_modules"]

[extensions]
documents = [".pdf", ".docx", ".txt"]
images = [".jpg", ".jpeg", ".png", ".webp"]
"""

raw = tomllib.loads(TEKST_TOML)
print(raw)''')
    nb.md("## Проверка результата — TOML разобран в обычный словарь Python")
    nb.code('''assert raw["destination"] == "Archive"
assert raw["exclude"] == [".git", ".venv", "node_modules"]
assert raw["extensions"]["documents"] == [".pdf", ".docx", ".txt"]
print("Верно: tomllib.loads() вернул обычный словарь с ожидаемой структурой.")''')
    nb.md("## Строим Config из разобранного TOML")
    nb.code('''def config_from_raw(raw):
    extensions = {k: list(v) for k, v in DEFAULT_EXTENSIONS.items()}
    extensions.update(raw.get("extensions", {}))
    return Config(
        destination=raw.get("destination", DEFAULT_DESTINATION),
        exclude=tuple(raw.get("exclude", list(DEFAULT_EXCLUDE))),
        extensions=extensions,
    )


nastrojki = config_from_raw(raw)
print(nastrojki)''')
    nb.md("## Задание ★ Базовая практика\n\nРазберите TOML без секции "
          "`[extensions]` и убедитесь, что `config_from_raw()` подставляет "
          "`DEFAULT_EXTENSIONS`, — точно так же, как это делает настоящий "
          "`load_config()` при отсутствующем ключе.")
    nb.code('''TEKST_BEZ_EXTENSIONS = \'destination = "Sorted2"\\n\'
raw_minimalnyj = tomllib.loads(TEKST_BEZ_EXTENSIONS)
nastrojki_minimalnye = config_from_raw(raw_minimalnyj)

assert nastrojki_minimalnye.destination == "Sorted2"
assert nastrojki_minimalnye.extensions == DEFAULT_EXTENSIONS
assert nastrojki_minimalnye.exclude == DEFAULT_EXCLUDE
print("Верно: без явных настроек используются значения по умолчанию.")''')
    nb.write(OUT_DIR / "23-19-toml-config.ipynb")
    print(f"Записано: 23-19 ({len(nb)} ячеек)")


def build_20_test_peremeshenie() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-20 · Тестируем перемещение и отмену\n\nПрактика к разделу "
          "[«Проверяем перемещение и отмену»](../../site/chapters/glava-23/23-25-testy-peremeshheniya.html). "
          "Использует настоящий пакет `safesort`.")
    nb.md("## Цель\n\nНаписать и запустить три теста в духе тех, что живут в "
          "`projects/python/safesort/tests/test_executor.py` и "
          "`test_manifest.py`: успешное перемещение, полная отмена и конфликт "
          "при восстановлении.")
    nb.md("## Рабочий пример — тесты apply_plan() и undo()")
    nb.code('''import tempfile
from pathlib import Path

from safesort.config import Config
from safesort.scanner import scan
from safesort.planner import build_plan
from safesort.executor import apply_plan
from safesort.manifest import write_manifest, undo
from safesort.models import MoveOperation, SortPlan


def test_apply_plan_moves_file_to_destination(tmp_path):
    source = tmp_path / "otchet.pdf"
    source.write_text("...", encoding="utf-8")
    destination = tmp_path / "Sorted" / "documents" / "otchet.pdf"
    plan = SortPlan(root=tmp_path, operations=(MoveOperation(source, destination),))

    results = apply_plan(plan)

    assert results[0].completed is True
    assert not source.exists()
    assert destination.exists()


def test_undo_restores_original_location(tmp_path):
    source = tmp_path / "otchet.pdf"
    source.write_text("...", encoding="utf-8")
    nastrojki = Config()
    plan = build_plan(scan(tmp_path, nastrojki), tmp_path, nastrojki)
    moves = apply_plan(plan)
    manifest_obj, _ = write_manifest(tmp_path, moves)

    result = undo(manifest_obj)

    assert source.exists()
    assert result.conflicts == ()


def test_undo_refuses_to_overwrite_conflict(tmp_path):
    source = tmp_path / "otchet.pdf"
    source.write_text("оригинал", encoding="utf-8")
    nastrojki = Config()
    plan = build_plan(scan(tmp_path, nastrojki), tmp_path, nastrojki)
    moves = apply_plan(plan)
    manifest_obj, _ = write_manifest(tmp_path, moves)

    source.write_text("кто-то создал новый файл здесь", encoding="utf-8")
    result = undo(manifest_obj)

    assert len(result.conflicts) == 1
    assert source.read_text(encoding="utf-8") == "кто-то создал новый файл здесь"


for test_func in (
    test_apply_plan_moves_file_to_destination,
    test_undo_restores_original_location,
    test_undo_refuses_to_overwrite_conflict,
):
    with tempfile.TemporaryDirectory() as tmp:
        test_func(Path(tmp))
    print(f"OK: {test_func.__name__}")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nНапишите "
          "`test_apply_plan_reports_missing_source(tmp_path)`, которая "
          "планирует перемещение уже не существующего файла и проверяет, что "
          "`completed` равен `False`.")
    nb.code('''def test_apply_plan_reports_missing_source(tmp_path):
    source = tmp_path / "prizrak.pdf"  # файла никогда не было
    destination = tmp_path / "Sorted" / "documents" / "prizrak.pdf"
    plan = SortPlan(root=tmp_path, operations=(MoveOperation(source, destination),))

    results = apply_plan(plan)

    assert results[0].completed is False
    assert results[0].error is not None


with tempfile.TemporaryDirectory() as tmp:
    test_apply_plan_reports_missing_source(Path(tmp))
print("OK: test_apply_plan_reports_missing_source")''')
    nb.write(OUT_DIR / "23-20-test-peremeshenie.ipynb")
    print(f"Записано: 23-20 ({len(nb)} ячеек)")


def build_21_test_scan() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-21 · Тестируем сканер и классификатор\n\nПрактика к разделу "
          "[«Проверяем сканирование и классификацию»](../../site/chapters/glava-23/23-24-testy-skanirovaniya.html). "
          "Использует настоящий пакет `safesort`.")
    nb.md("## Цель\n\nНаписать и запустить тесты в духе "
          "`projects/python/safesort/tests/test_scanner.py` и "
          "`test_classifier.py`: вложенные файлы, исключение каталога "
          "результата, пустой каталог и известные/неизвестные расширения.")
    nb.md("## Рабочий пример")
    nb.code('''import tempfile
from pathlib import Path

from safesort.config import Config, DEFAULT_EXTENSIONS
from safesort.scanner import scan
from safesort.classifier import classify


def test_scan_finds_nested_files(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "otchet.pdf").write_text("...", encoding="utf-8")
    (tmp_path / "photo.jpg").write_text("...", encoding="utf-8")

    files = scan(tmp_path, Config())
    names = {f.path.name for f in files}
    assert names == {"otchet.pdf", "photo.jpg"}


def test_scan_skips_destination_directory(tmp_path):
    (tmp_path / "Sorted" / "documents").mkdir(parents=True)
    (tmp_path / "Sorted" / "documents" / "staryj.pdf").write_text("...", encoding="utf-8")

    files = scan(tmp_path, Config())
    assert files == []


def test_scan_empty_directory_returns_empty_list(tmp_path):
    files = scan(tmp_path, Config())
    assert files == []


def test_classify_known_extension():
    assert classify(".pdf", DEFAULT_EXTENSIONS) == "documents"


def test_classify_unknown_extension_is_other():
    assert classify(".xyz", DEFAULT_EXTENSIONS) == "other"


for test_func in (
    test_scan_finds_nested_files,
    test_scan_skips_destination_directory,
    test_scan_empty_directory_returns_empty_list,
):
    with tempfile.TemporaryDirectory() as tmp:
        test_func(Path(tmp))
    print(f"OK: {test_func.__name__}")

test_classify_known_extension()
test_classify_unknown_extension_is_other()
print("OK: test_classify_known_extension, test_classify_unknown_extension_is_other")''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите "
          "`test_scan_skips_symlinks(tmp_path)`, создающую символическую "
          "ссылку на файл, и убедитесь, что она не попадает в результат "
          "`scan()`.")
    nb.code('''def test_scan_skips_symlinks(tmp_path):
    fajl = tmp_path / "photo.jpg"
    fajl.write_text("...", encoding="utf-8")
    ssylka = tmp_path / "ssylka.jpg"
    try:
        ssylka.symlink_to(fajl)
    except (OSError, NotImplementedError):
        return  # символические ссылки не поддерживаются в этом окружении

    files = scan(tmp_path, Config())
    names = {f.path.name for f in files}
    assert "ssylka.jpg" not in names
    assert "photo.jpg" in names


with tempfile.TemporaryDirectory() as tmp:
    test_scan_skips_symlinks(Path(tmp))
print("OK: test_scan_skips_symlinks")''')
    nb.write(OUT_DIR / "23-21-test-scan.ipynb")
    print(f"Записано: 23-21 ({len(nb)} ячеек)")


def build_22_test_duplicaty() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-22 · Тесты дубликатов и пустых файлов\n\nПрактика к разделу "
          "[«Проверяем поиск дубликатов»](../../site/chapters/glava-23/23-26-testy-dublikatov.html). "
          "Повторяет `projects/python/safesort/tests/test_duplicates.py`, но "
          "полностью в памяти — без обращения к диску.")
    nb.md("## Цель\n\nНаписать и запустить тесты для группировки дубликатов: "
          "типичный случай, файлы без пары и — отдельно — пустые файлы, "
          "которые тоже считаются дубликатами друг друга.")
    nb.md("## Рабочий пример")
    nb.code('''import hashlib
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class FileInfo:
    name: str
    size: int
    content: bytes


def find_duplicates(files):
    by_size = defaultdict(list)
    for file in files:
        by_size[file.size].append(file)

    groups = []
    for size, candidates in by_size.items():
        if len(candidates) < 2:
            continue
        by_digest = defaultdict(list)
        for candidate in candidates:
            digest = hashlib.sha256(candidate.content).hexdigest()
            by_digest[digest].append(candidate)
        for digest, matched in by_digest.items():
            if len(matched) >= 2:
                groups.append({"size": size, "digest": digest, "files": tuple(matched)})
    return groups


def test_identical_content_files_are_grouped():
    files = [
        FileInfo("notes.txt", 12, b"tot zhe text"),
        FileInfo("copy_of_notes.txt", 12, b"tot zhe text"),
    ]
    groups = find_duplicates(files)
    assert len(groups) == 1
    assert len(groups[0]["files"]) == 2


def test_different_content_same_size_not_grouped():
    files = [
        FileInfo("a.txt", 4, b"AAAA"),
        FileInfo("b.txt", 4, b"BBBB"),
    ]
    groups = find_duplicates(files)
    assert groups == []


def test_empty_files_are_duplicates_of_each_other():
    files = [
        FileInfo("a.txt", 0, b""),
        FileInfo("b.txt", 0, b""),
    ]
    groups = find_duplicates(files)
    assert len(groups) == 1
    assert groups[0]["size"] == 0
    assert groups[0]["digest"] == hashlib.sha256(b"").hexdigest()


for test_func in (
    test_identical_content_files_are_grouped,
    test_different_content_same_size_not_grouped,
    test_empty_files_are_duplicates_of_each_other,
):
    test_func()
    print(f"OK: {test_func.__name__}")''')
    nb.md("## Проверка результата")
    nb.code('''groups_dlya_proverki = find_duplicates([
    FileInfo("x1.bin", 3, b"XXX"),
    FileInfo("x2.bin", 3, b"XXX"),
    FileInfo("x3.bin", 3, b"XXX"),
])

assert len(groups_dlya_proverki) == 1
assert len(groups_dlya_proverki[0]["files"]) == 3
print("Верно: три файла с одинаковым содержимым образовали одну группу из трёх, "
      "а не полтора дубликата.")''')
    nb.md("## Задание ★★ Самостоятельная задача")
    nb.code('''def test_three_size_groups_only_two_have_duplicates():
    files = [
        FileInfo("a1.txt", 5, b"AAAAA"),
        FileInfo("a2.txt", 5, b"AAAAA"),
        FileInfo("b1.txt", 7, b"BBBBBBB"),
        FileInfo("c1.txt", 9, b"CCCCCCCCC"),  # уникальный размер — не дубликат
    ]
    groups = find_duplicates(files)
    assert len(groups) == 1
    assert {f.name for f in groups[0]["files"]} == {"a1.txt", "a2.txt"}


test_three_size_groups_only_two_have_duplicates()
print("OK: test_three_size_groups_only_two_have_duplicates")''')
    nb.write(OUT_DIR / "23-22-test-duplicaty.ipynb")
    print(f"Записано: 23-22 ({len(nb)} ячеек)")


def build_23_test_cli() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-23 · Тесты аргументов командной строки\n\nПрактика к разделу "
          "[«Проверяем интерфейс командной строки»](../../site/chapters/glava-23/23-27-testy-cli.html). "
          "Повторяет `projects/python/safesort/tests/test_cli.py` в части разбора "
          "аргументов — полностью через argparse, без обращения к диску.")
    nb.md("## Цель\n\nНаписать и запустить тесты для парсера аргументов: "
          "все пять подкоманд, значение root по умолчанию для undo и "
          "ненулевой код завершения при отсутствии или ошибке в подкоманде.")
    nb.md("## Рабочий пример")
    nb.code('''import argparse
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(prog="safesort")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("scan", "plan", "apply", "duplicates"):
        sub = subparsers.add_parser(name)
        sub.add_argument("root", type=Path)
    undo_parser = subparsers.add_parser("undo")
    undo_parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    return parser


def test_parser_accepts_all_subcommands():
    parser = build_parser()
    for name in ("scan", "plan", "apply", "duplicates"):
        args = parser.parse_args([name, "/tmp/x"])
        assert args.command == name
        assert args.root == Path("/tmp/x")


def test_undo_defaults_to_current_directory():
    parser = build_parser()
    args = parser.parse_args(["undo"])
    assert args.command == "undo"
    assert args.root == Path(".")


def test_missing_subcommand_exits_nonzero():
    import contextlib
    import io

    parser = build_parser()
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stderr(buffer):
            parser.parse_args([])
        podnyalos_iskluchenie = False
        kod = None
    except SystemExit as exc:
        podnyalos_iskluchenie = True
        kod = exc.code

    assert podnyalos_iskluchenie is True
    assert kod != 0


test_parser_accepts_all_subcommands()
test_undo_defaults_to_current_directory()
test_missing_subcommand_exits_nonzero()
print("OK: все три теста прошли.")''')
    nb.md("## Проверка результата")
    nb.code('''parser_dlya_proverki = build_parser()
args_proverki = parser_dlya_proverki.parse_args(["apply", "/home/anna/Downloads"])

assert args_proverki.command == "apply"
assert args_proverki.root == Path("/home/anna/Downloads")
print("Верно: apply разобран с правильным путём.")''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите "
          "`test_unknown_subcommand_exits_nonzero()`, которая проверяет, что "
          "несуществующая подкоманда `\"zip\"` тоже завершает разбор с "
          "ненулевым кодом.")
    nb.code('''def test_unknown_subcommand_exits_nonzero():
    import contextlib
    import io

    parser = build_parser()
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stderr(buffer):
            parser.parse_args(["zip", "/tmp/x"])
        assert False, "ожидался SystemExit"
    except SystemExit as exc:
        assert exc.code != 0


test_unknown_subcommand_exits_nonzero()
print("OK: test_unknown_subcommand_exits_nonzero")''')
    nb.write(OUT_DIR / "23-23-test-cli.ipynb")
    print(f"Записано: 23-23 ({len(nb)} ячеек)")


def build_24_git_diff() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-24 · Читаем git diff и группируем изменения\n\nПрактика к разделу "
          "[«Самопроверка изменений и дисциплина коммитов»](../../site/chapters/glava-23/23-28-git-kommit.html).")
    nb.md("## Цель\n\n`git diff` не выполняется — его читают. Это упражнение "
          "не о запуске кода, а о том, чтобы разобраться, что именно "
          "изменилось, и сформулировать по этому изменению короткое, честное "
          "commit-сообщение.")
    nb.md("## Пример — результат git diff перед коммитом")
    nb.code('''PRIMER_DIFF = """diff --git a/src/safesort/duplicates.py b/src/safesort/duplicates.py
index 1a2b3c4..5d6e7f8 100644
--- a/src/safesort/duplicates.py
+++ b/src/safesort/duplicates.py
@@ -40,6 +40,9 @@ def find_duplicates(files, chunk_size=DEFAULT_CHUNK_SIZE):
     for size, candidates in by_size.items():
         if len(candidates) < 2:
             continue
+
+        if size == 0:
+            logger.info("Пустые файлы тоже считаются дубликатами: %d штук", len(candidates))
         by_digest = defaultdict(list)
diff --git a/tests/test_duplicates.py b/tests/test_duplicates.py
index 9f8e7d6..2c3b4a5 100644
--- a/tests/test_duplicates.py
+++ b/tests/test_duplicates.py
@@ -12,3 +12,10 @@ def test_identical_content_files_are_grouped(tmp_path):
     assert len(groups) == 1
     assert len(groups[0].files) == 2
+
+
+def test_empty_files_are_duplicates_of_each_other(tmp_path):
+    (tmp_path / "a.txt").write_text("")
+    (tmp_path / "b.txt").write_text("")
+    groups = find_duplicates(scan(tmp_path, Config()))
+    assert len(groups) == 1
"""

print(PRIMER_DIFF)''')
    nb.md("## Разбираем diff построчно")
    nb.code('''stroki = PRIMER_DIFF.splitlines()

izmenennye_fajly = [s.split()[-1][2:] for s in stroki if s.startswith("diff --git")]
dobavlennye_stroki = [s for s in stroki if s.startswith("+") and not s.startswith("+++")]
udalennye_stroki = [s for s in stroki if s.startswith("-") and not s.startswith("---")]

print("Изменённые файлы:", izmenennye_fajly)
print("Добавлено строк:", len(dobavlennye_stroki))
print("Удалено строк:", len(udalennye_stroki))''')
    nb.md("## Проверка")
    nb.code('''assert izmenennye_fajly == ["src/safesort/duplicates.py", "tests/test_duplicates.py"]
assert len(dobavlennye_stroki) > 0
assert len(udalennye_stroki) == 0  # в этом diff ничего не удалено, только добавлено
print("Верно: diff затронул два файла, и в нём только добавления.")''')
    nb.md("## Задание ★ Базовая практика\n\nПрочитайте diff выше и "
          "сформулируйте commit-сообщение, которое описывало бы это изменение "
          "одной строкой в духе Conventional Commits (например, `feat: ...` "
          "или `test: ...`). Запишите его в переменную "
          "`moe_commit_soobshenie` и проверьте, что оно не пустое и "
          "начинается с одного из принятых префиксов.")
    nb.code('''moe_commit_soobshenie = "feat: treat zero-byte files as duplicates of each other"

dopustimye_prefiksy = ("feat:", "fix:", "test:", "docs:", "refactor:", "chore:")

assert moe_commit_soobshenie.strip() != ""
assert moe_commit_soobshenie.startswith(dopustimye_prefiksy)
print("Верно:", moe_commit_soobshenie)''')
    nb.write(OUT_DIR / "23-24-git-diff.ipynb")
    print(f"Записано: 23-24 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01_kalkulyator()
    build_02_generator_istorij()
    build_03_rps()
    build_04_myach()
    build_05_temperatura()
    build_06_fajly_tkinter()
    build_07_argparse_cli()
    build_08_pathlib()
    build_09_scan()
    build_10_isklyucheniya()
    build_11_klassifikator()
    build_12_plan()
    build_13_executor()
    build_14_kollizii()
    build_15_manifest_json()
    build_16_undo()
    build_17_sha256()
    build_18_duplicaty()
    build_19_toml_config()
    build_20_test_peremeshenie()
    build_21_test_scan()
    build_22_test_duplicaty()
    build_23_test_cli()
    build_24_git_diff()
