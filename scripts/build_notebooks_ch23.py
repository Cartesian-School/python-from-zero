#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 23 (Ещё больше мини-проектов).

Tkinter- и Pygame-проекты используют те же headless-приёмы, что и в предыдущих главах:
create-once/update()+destroy() вместо mainloop(), for-в-range() вместо игрового while.
Проект «Камень, ножницы, бумага» использует ту же симуляцию input(), что и главы 8/10.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-23"


def build_01_kalkulyator() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-01 · Калькулятор\n\nПрактика к разделу "
          "[«Проект 23-1: Калькулятор с Tkinter»](../../site/chapters/glava-23/23-01-kalkulyator.html). "
          "Полный файл — `projects/tkinter/calculator/calculator.py`.")
    nb.md("## Цель\n\nПроверить вычисление выражений и последовательность нажатий кнопок, "
          "как это делал бы настоящий пользователь.")
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
print("Верно: базовые вычисления совпадают с ожидаемыми.")''')
    nb.md("## Эксперимент — некорректный и опасный ввод не приводит к падению")
    nb.code('''print(c.vychislit_vyrazhenie("5/0"))
print(c.vychislit_vyrazhenie("2+*3"))
print(c.vychislit_vyrazhenie("import os"))

assert c.vychislit_vyrazhenie("5/0") == "Ошибка"
assert c.vychislit_vyrazhenie("2+*3") == "Ошибка"
assert c.vychislit_vyrazhenie("import os") == "Ошибка"
print("Верно: деление на ноль, синтаксическая ошибка и посторонний код — везде «Ошибка».")''')
    nb.md("## Задание ★ Базовая практика\n\nСимулируйте нажатия кнопок «1», «2», «+», «8», «=» "
          "и проверьте результат на экране.")
    nb.code('''c.na_ochistit_nazhali()
for simvol in "12+8":
    c.na_cifru_ili_znak_nazhali(simvol)

assert c.ekran_text.get() == "12+8"
c.na_ravno_nazhali()

assert c.ekran_text.get() == "20"
print("Верно: 12 + 8 = 20 на экране калькулятора.")''')
    nb.write(OUT_DIR / "23-01-kalkulyator.ipynb")
    print(f"Записано: 23-01 ({len(nb)} ячеек)")


def build_02_generator_istorij() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-02 · Генератор случайных историй\n\nПрактика к разделу "
          "[«Проект 23-2: Генератор случайных историй»]"
          "(../../site/chapters/glava-23/23-02-generator-istorij.html). "
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
          "[«Проект 23-3: Игра «Камень, ножницы, бумага»»]"
          "(../../site/chapters/glava-23/23-03-kamen-nozhnicy-bumaga.html). "
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
          "[«Проект 23-4: Отскакивающий от четырёх стен мяч с Pygame»]"
          "(../../site/chapters/glava-23/23-04-otskakivayushij-myach.html). "
          "Полный файл — `projects/pygame/bouncing-balls-oop/bouncing_balls.py`.")
    nb.md("## Про игровой цикл в этом ноутбуке\n\n"
          "Как и в главах 20-21: настоящий игровой цикл — `while rabotaet:`. Здесь вместо "
          "него используется `for kadr in range(N):` с фиксированным числом кадров — сама "
          "физика мяча (`Myach.shag()`) при этом та же, что в настоящей игре.")
    nb.md("## Рабочий пример")
    nb.code('''import sys

sys.path.insert(0, "../../projects/pygame/bouncing-balls-oop")
import bouncing_balls as bb

myachi = bb.sozdat_myachi(3)
print("Создано мячей:", len(myachi))
for m in myachi:
    print(" -", m.cvet, "радиус", m.radius)''')
    nb.md("## Проверка результата")
    nb.code('''assert len(myachi) == 3
assert len({m.cvet for m in myachi}) == 3
print("Верно: три мяча с тремя разными цветами.")''')
    nb.md("## Эксперимент — 300 кадров: мячи остаются в границах и отскакивают")
    nb.code('''for kadr in range(300):
    for myach in myachi:
        myach.shag()

for myach in myachi:
    assert myach.radius <= myach.x <= bb.SHIRINA - myach.radius
    assert myach.radius <= myach.y <= bb.VYSOTA - myach.radius
    assert myach.otskokov > 0

print("Отскоков у каждого мяча:", [m.otskokov for m in myachi])
print("Верно: после 300 кадров все мячи внутри экрана и хотя бы раз отскочили.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nОтрисуйте кадр и убедитесь, что каждый "
          "мяч нарисован своим собственным цветом.")
    nb.code('''bb.narisovat_kadr(myachi)
for myach in myachi:
    cvet_na_ekrane = bb.screen.get_at((int(myach.x), int(myach.y)))[:3]
    assert cvet_na_ekrane == myach.cvet

print("Верно: каждый мяч нарисован своим цветом.")
bb.pygame.quit()''')
    nb.write(OUT_DIR / "23-04-otskakivayushij-myach.ipynb")
    print(f"Записано: 23-04 ({len(nb)} ячеек)")


def build_05_temperatura() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-05 · Преобразование температуры\n\nПрактика к разделу "
          "[«Проект 23-5: Приложение для преобразования температуры»]"
          "(../../site/chapters/glava-23/23-05-temperatura.html). "
          "Полный файл — `projects/tkinter/temperature-converter/temperature_converter.py`.")
    nb.md("## Цель\n\nПроверить формулы перевода на известных опорных точках и симулировать "
          "ввод пользователя.")
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

r = tc.preobrazovat(0, "K")
assert abs(r["C"] - (-273.15)) < 1e-9

print("Верно: 0°C = 32°F = 273.15K, 100°C = 212°F, 0K = -273.15°C (абсолютный ноль).")''')
    nb.md("## Эксперимент — симулируем ввод через поле и кнопку")
    nb.code('''tc.pole_vvoda.insert(0, "100")
tc.edinica.set("C")
tc.na_preobrazovat_nazhali()

print("На экране:", tc.rezultat_text.get())
assert "212.0" in tc.rezultat_text.get()
print("Верно: нажатие «Преобразовать» обновляет надпись на экране.")''')
    nb.md("## Задание ★ Базовая практика\n\nВведите текст вместо числа и убедитесь, что "
          "приложение не падает, а показывает понятное сообщение.")
    nb.code('''tc.pole_vvoda.delete(0, "end")
tc.pole_vvoda.insert(0, "не число")
tc.na_preobrazovat_nazhali()

assert tc.rezultat_text.get() == "Введите число"
print("Верно: некорректный ввод обрабатывается без падения программы.")''')
    nb.write(OUT_DIR / "23-05-temperatura.ipynb")
    print(f"Записано: 23-05 ({len(nb)} ячеек)")


def build_06_fajly_tkinter() -> None:
    nb = NotebookBuilder()
    nb.md("# 23-06 · Файлы и Tkinter\n\nПрактика к разделу "
          "[«Проект 23-6: Знакомство с файлами и Tkinter»]"
          "(../../site/chapters/glava-23/23-06-fajly-tkinter-itogi.html). "
          "Полный файл — `projects/tkinter/notes-app/notes_app.py`.")
    nb.md("## Цель\n\nПроверить сохранение и загрузку заметки, а также поведение при "
          "отсутствии сохранённого файла.")
    nb.md("## Рабочий пример")
    nb.code('''import sys

sys.path.insert(0, "../../projects/tkinter/notes-app")
import notes_app as na

if na.FAJL_ZAMETOK.exists():
    na.FAJL_ZAMETOK.unlink()

na.zagruzit_zametku()
print(na.status_text.get())''')
    nb.md("## Проверка результата")
    nb.code('''assert "ещё не создан" in na.status_text.get()
print("Верно: попытка загрузки без сохранённого файла даёт понятное сообщение, а не падение.")''')
    nb.md("## Эксперимент — сохраняем и загружаем заметку")
    nb.code('''na.polye_teksta.insert("1.0", "Купить молоко\\nПозвонить маме")
na.sohranit_zametku()

assert na.FAJL_ZAMETOK.exists()
assert na.FAJL_ZAMETOK.read_text(encoding="utf-8") == "Купить молоко\\nПозвонить маме"
print("Верно: сохранение записывает содержимое поля в файл.")

na.ochistit_polye()
assert na.polye_teksta.get("1.0", "end-1c") == ""

na.zagruzit_zametku()
assert na.polye_teksta.get("1.0", "end-1c") == "Купить молоко\\nПозвонить маме"
print("Верно: после очистки поля загрузка восстанавливает текст из файла.")''')
    nb.md("## Задание ★ Базовая практика\n\nУберите тестовый файл заметки, чтобы не "
          "засорять репозиторий, и убедитесь, что он действительно удалён.")
    nb.code('''na.FAJL_ZAMETOK.unlink()
assert not na.FAJL_ZAMETOK.exists()
print("Верно: тестовый файл заметки удалён.")''')
    nb.write(OUT_DIR / "23-06-fajly-tkinter.ipynb")
    print(f"Записано: 23-06 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01_kalkulyator()
    build_02_generator_istorij()
    build_03_rps()
    build_04_myach()
    build_05_temperatura()
    build_06_fajly_tkinter()
