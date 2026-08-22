#!/usr/bin/env python3
"""Строит Главу 4: «Python любит числа» (site/chapters/glava-04/).

Curriculum v2: от короткого введения в int/float/complex до полноценного
курса числовой арифметики Python 3.14 — что компьютер называет числом,
имена и неизменяемые числовые объекты (продолжение модели памяти из главы
3), системы счисления, операторы и их порядок, деление и остаток, степени,
float и почему 0.1 + 0.2 != 0.3, округление, Decimal, Fraction, complex,
math/cmath, random/secrets, statistics, inf/nan, отладка числовых ошибок и
несколько мини-проектов. Существующие маршруты (index, 04-01..04-05)
сохранены и расширены на месте; новый материал добавлен как новые страницы.
"""

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    branch_diagram,
    callout,
    capability_map,
    classic_vs_modern,
    code_block,
    comparison_table,
    complex_plane_diagram,
    converge_diagram,
    decision_map,
    exercise,
    flow_diagram,
    fraction_bar_diagram,
    image_figure,
    name_value_diagram,
    namespace_diagram,
    number_line_diagram,
    place_value_diagram,
    practice_card,
    precedence_ladder,
    render_chapter_opener,
    render_page,
    summary_box,
    timeline_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-04"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Приступаем"),
    ("04-01-chisla-i-peremennye.html", "Что такое число для компьютера"),
    ("04-06-int-glubzhe.html", "int — целые числа без страха"),
    ("04-07-sistemy-schisleniya.html", "Системы счисления"),
    ("04-02-kommentarii.html", "Комментарии в вычислениях"),
    ("04-08-operatory.html", "Арифметические операторы"),
    ("04-09-poryadok-operacij.html", "Порядок выполнения операций"),
    ("04-10-delenie-i-ostatok.html", "Деление и остаток"),
    ("04-11-stepeni.html", "Степени и abs()"),
    ("04-03-vidy-chisel.html", "Карта числовых типов"),
    ("04-12-float-osnovy.html", "float — дробные числа"),
    ("04-13-pochemu-01-02.html", "Почему 0.1 + 0.2 не равно 0.3"),
    ("04-14-sravnenie-float.html", "Сравниваем float правильно"),
    ("04-15-okruglenie.html", "Округление: round, floor, ceil, trunc"),
    ("04-16-decimal.html", "Decimal — точная десятичная арифметика"),
    ("04-17-fraction.html", "Fraction — точные дроби"),
    ("04-18-kompleksnye-chisla.html", "complex и cmath"),
    ("04-04-preobrazovanie-tipov.html", "Преобразование типов чисел"),
    ("04-19-modul-math.html", "Модуль math"),
    ("04-20-random-i-secrets.html", "random и secrets"),
    ("04-21-statistics-i-inf-nan.html", "statistics, inf и nan"),
    ("04-22-chislovye-oshibki.html", "Числовые ошибки и отладка"),
    ("04-05-mini-proekt-itogi.html", "Мини-проекты и итоги"),
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    practice_ids = ["04-01", "04-02", "04-06", "04-07", "04-08", "04-09", "04-10",
                     "04-11", "04-12", "04-13", "04-14", "04-15", "04-16", "04-17",
                     "04-18", "04-19", "04-20", "04-21", "04-22", "04-03", "04-04", "04-05"]
    return [
        SidebarGroup("Глава 4 · Числа", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {pid}: Практика", f"../../practice/{pid}/index.html") for pid in practice_ids
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=4,
        baseline_page=39,
        title="Python любит числа",
        description="Полноценные числовые основы Python 3.14: что компьютер называет числом, "
        "int и системы счисления, операторы и их порядок, деление и остаток, float и "
        "почему 0.1 + 0.2 не равно 0.3, округление, Decimal, Fraction, complex, math, "
        "random/secrets, statistics — и несколько мини-проектов.",
        meta_items=["⏱ ~4 часа", "🔢 int, float, complex, Decimal, Fraction", "📓 22 практики"],
        sections=[
            ChapterSectionLink("4.1", "Что такое число для компьютера", "04-01-chisla-i-peremennye.html", "39"),
            ChapterSectionLink("4.2", "int — целые числа без страха", "04-06-int-glubzhe.html", ""),
            ChapterSectionLink("4.3", "Системы счисления", "04-07-sistemy-schisleniya.html", ""),
            ChapterSectionLink("4.4", "Комментарии в вычислениях", "04-02-kommentarii.html", "46"),
            ChapterSectionLink("4.5", "Арифметические операторы", "04-08-operatory.html", ""),
            ChapterSectionLink("4.6", "Порядок выполнения операций", "04-09-poryadok-operacij.html", ""),
            ChapterSectionLink("4.7", "Деление и остаток", "04-10-delenie-i-ostatok.html", ""),
            ChapterSectionLink("4.8", "Степени и abs()", "04-11-stepeni.html", ""),
            ChapterSectionLink("4.9", "Карта числовых типов", "04-03-vidy-chisel.html", "47"),
            ChapterSectionLink("4.10", "float — дробные числа", "04-12-float-osnovy.html", "49"),
            ChapterSectionLink("4.11", "Почему 0.1 + 0.2 не равно 0.3", "04-13-pochemu-01-02.html", ""),
            ChapterSectionLink("4.12", "Сравниваем float правильно", "04-14-sravnenie-float.html", ""),
            ChapterSectionLink("4.13", "Округление: round, floor, ceil, trunc", "04-15-okruglenie.html", ""),
            ChapterSectionLink("4.14", "Decimal — точная десятичная арифметика", "04-16-decimal.html", ""),
            ChapterSectionLink("4.15", "Fraction — точные дроби", "04-17-fraction.html", ""),
            ChapterSectionLink("4.16", "complex и cmath", "04-18-kompleksnye-chisla.html", "50"),
            ChapterSectionLink("4.17", "Преобразование типов чисел", "04-04-preobrazovanie-tipov.html", "53"),
            ChapterSectionLink("4.18", "Модуль math", "04-19-modul-math.html", ""),
            ChapterSectionLink("4.19", "random и secrets", "04-20-random-i-secrets.html", ""),
            ChapterSectionLink("4.20", "statistics, inf и nan", "04-21-statistics-i-inf-nan.html", ""),
            ChapterSectionLink("4.21", "Числовые ошибки и отладка", "04-22-chislovye-oshibki.html", ""),
            ChapterSectionLink("4.22", "Мини-проекты и итоги", "04-05-mini-proekt-itogi.html", "57"),
        ],
    )
    write("index.html", out)


def build_01_what_is_a_number() -> None:
    human_vs_machine = flow_diagram(
        [
            ("Число\nв математике", "10, 3.14, 1/3, ∞"),
            ("Представление\nв компьютере", "конкретный способ хранения"),
            ("Результат\nвычисления", "иногда точный, иногда — нет"),
        ],
        caption="Математическое число и его представление в компьютере — связаны, но не всегда совпадают",
    )

    body = f"""
    <p>Человек видит числа как абстрактные понятия: <code class="inline">10</code>,
    <code class="inline">3.14</code>, <code class="inline">1/3</code>, даже
    <code class="inline">∞</code>. Компьютер же не «понимает» числа в математическом смысле —
    он хранит их <strong>представление</strong>: конкретную последовательность байтов по
    конкретным правилам.</p>

{human_vs_machine}

    <p>Для целых чисел это различие почти незаметно — представление в компьютере ведёт себя
    так же, как число в математике. Но для дробных чисел разница становится важной — и мы
    подробно разберём её в разделах 4.10–4.11, когда дойдём до <code class="inline">float</code>.
    Пока достаточно запомнить сам принцип: то, что вы пишете в коде, и то, что реально хранится
    внутри, — связанные, но не обязательно тождественные вещи.</p>

    <h2 id="imena-i-chisla">Имена указывают на числовые объекты</h2>
    <p>В главе 3 мы разобрали важный принцип: имя (переменная) — это не «коробка», в которую
    кладут значение, а скорее стрелка, указывающая на объект. Этот же принцип полностью
    относится и к числам.</p>

{code_block("age.py", 'age = 10\nprint(age)\n')}

{name_value_diagram("age", "10", caption="age указывает на числовой объект 10 — не «содержит» его")}

    <h2 id="peremennaya-menyaet-znachenie">Что происходит при age = age + 1</h2>
    <p>Числа в Python — <strong>неизменяемые</strong> (immutable) объекты: сам объект
    <code class="inline">10</code> невозможно «отредактировать» в 11. Когда мы пишем:</p>

{code_block("age2.py", 'age = 10\nage = age + 1\nprint(age)  # 11\n')}

    <p>происходит не редактирование, а переприсваивание — Python вычисляет новое значение и
    заставляет имя <code class="inline">age</code> указывать на НОВЫЙ объект:</p>

{namespace_diagram(
        [("age (до)", "10")],
        caption="ДО: age указывает на 10",
    )}

    <p style="text-align:center;font-family:'JetBrains Mono',monospace;color:var(--ink-soft,#6B6B7D);margin:8px 0">
    вычисление: 10 + 1 → 11
    </p>

{namespace_diagram(
        [("age (после)", "11")],
        caption="ПОСЛЕ: age указывает на новый объект 11 — старый объект 10 больше не нужен",
    )}

{callout(
        "warning",
        "⚠️ Точная формулировка важна",
        "Python не «изменил число 10 на 11». Целые числа <strong>неизменяемы</strong>: Python "
        "вычислил результат <code class=\"inline\">10 + 1</code>, получил новый объект "
        "<code class=\"inline\">11</code> и переприсвоил имя <code class=\"inline\">age</code> "
        "этому новому объекту. Это ровно та же модель «имя → объект» и «переприсваивание меняет "
        "связь, а не сам объект», которую мы разбирали в главе 3.",
    )}

    <p>Мы будем возвращаться к этому принципу неизменяемости на протяжении всего курса — он
    объясняет поведение строк, кортежей и (в отличие от них) то, почему списки ведут себя
    иначе, когда мы дойдём до них в следующих главах.</p>

{callout(
        "tip",
        "🐍 Попробуем",
        "Наберите этот пример в браузерной практике или в REPL (глава 3) — и после каждой "
        "строки проверяйте <code class=\"inline\">id(age)</code>. Число (адрес объекта в памяти "
        "для CPython) изменится после переприсваивания — наглядное подтверждение того, что "
        "объект действительно стал другим.",
    )}

{practice_card(
        "04-01",
        "Практика: числа как объекты, а не коробки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-01/index.html",
    )}"""

    out = render_page(
        page_title="Что такое число для компьютера",
        description="Разница между математическим числом и его представлением в компьютере, и "
        "как имена указывают на неизменяемые числовые объекты — без модели «коробки».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Что такое число для компьютера", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Что такое число для компьютера",
        lede="Прежде чем изучать типы чисел — разберёмся, что вообще значит «число» с точки "
        "зрения компьютера, и как имена связаны с числовыми объектами.",
        body_html=body,
        sidebar_groups=sidebar("04-01-chisla-i-peremennye.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="04-06-int-glubzhe.html", next_label="int — целые числа без страха"),
    )
    write("04-01-chisla-i-peremennye.html", out)


def build_06_int_deeper() -> None:
    body = f"""
    <p><code class="inline">int</code> (integer — целое число) — тип для чисел без дробной
    части: положительных, отрицательных и нуля.</p>
{code_block("celye.py", "print(0)\nprint(42)\nprint(-17)\nprint(type(42))\n")}

    <h2 id="bolshie-chisla">Числа практически без ограничения размера</h2>
    <p>В отличие от многих других языков программирования, где целые числа ограничены
    фиксированным диапазоном (например, 32 или 64 бита), в Python <code class="inline">int</code>
    может расти сколь угодно — точность <strong>произвольная</strong>, ограниченная практически
    только доступной памятью компьютера, а не языком.</p>

{code_block("bolshoe_chislo.py", "huge = 10 ** 100\nprint(huge)\n")}

{callout(
        "info",
        "💡 Точная формулировка",
        "Правильно говорить «произвольная точность, ограниченная доступными ресурсами», а не "
        "«неограниченный размер». Формально предел есть — но на практике вы почти никогда его "
        "не достигнете в обычных программах.",
    )}

    <h2 id="immutable-int">Числа неизменяемы — продолжение</h2>
    <p>Мы уже видели это в разделе 4.1 на примере <code class="inline">age</code>. Ещё раз, уже
    с двумя именами:</p>
{code_block("a_b.py", "a = 10\nb = a\na += 1\nprint(a)  # 11\nprint(b)  # 10 — b не изменился\n")}
{namespace_diagram(
        [("a", "11"), ("b", "10")],
        caption="После a += 1: у a — новая связь; b по-прежнему указывает на прежний объект",
    )}

{callout(
        "warning",
        "⚠️ Не используйте id() как учебный трюк для «кеша целых чисел»",
        "Вы можете где-то встретить сравнение <code class=\"inline\">id(256)</code> и "
        "<code class=\"inline\">id(257)</code> как «доказательство» особого поведения маленьких "
        "чисел. Это деталь реализации CPython (оптимизация кеширования маленьких целых чисел), "
        "а не гарантия языка Python — полагаться на неё в реальном коде нельзя, и как "
        "обучающий пример она скорее запутывает, чем помогает.",
    )}

    <h2 id="bool">bool — особый родственник int</h2>
    <p>Значения <code class="inline">True</code> и <code class="inline">False</code> образуют
    тип <code class="inline">bool</code> — и исторически он тесно связан с
    <code class="inline">int</code>: <code class="inline">True</code> ведёт себя как
    <code class="inline">1</code>, а <code class="inline">False</code> — как
    <code class="inline">0</code>.</p>
{code_block("bool_int.py", "print(int(True))   # 1\nprint(int(False))  # 0\nprint(True + True) # 2\n")}
{callout(
        "tip",
        "💡 Но в обычном коде — это логические значения",
        "То, что <code class=\"inline\">bool</code> технически «числовой» — деталь языка, а не "
        "приглашение складывать <code class=\"inline\">True + True</code> в реальном коде. "
        "Полноценно об условиях и логике — в главе про условия; здесь достаточно знать связь с "
        "числами, если вы её где-то встретите.",
    )}

    <h2 id="podcherkivaniya">Разделители-подчёркивания для читаемости</h2>
    <p>В длинных числах легко потерять счёт нулям. Python позволяет разбивать число
    подчёркиваниями — они не влияют на значение, только на читаемость:</p>
{code_block("naselenie.py", "population = 38_000_000\nprint(population)  # 38000000\n")}

    <h2 id="augmented">Сокращённое присваивание</h2>
    <p>Операторы вроде <code class="inline">+=</code> — это компактная запись «пересчитать и
    переприсвоить», а не «изменить число на месте»:</p>
{code_block("augmented.py", "x = 10\nx += 1   # то же, что x = x + 1\nx -= 2   # то же, что x = x - 2\nx *= 3   # то же, что x = x * 3\n")}

{practice_card(
        "04-06",
        "Практика: большие числа и неизменяемость int",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-06/index.html",
    )}"""

    out = render_page(
        page_title="int — целые числа без страха больших значений",
        description="int в Python: произвольная точность, неизменяемость, связь с bool, "
        "подчёркивания-разделители и сокращённое присваивание.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("int — целые числа", "")],
        kicker="Глава 4 · Python любит числа",
        h1="int — целые числа без страха больших значений",
        lede="Целые числа в Python могут расти намного больше, чем в большинстве других "
        "языков — и остаются при этом неизменяемыми объектами.",
        body_html=body,
        sidebar_groups=sidebar("04-06-int-glubzhe.html"),
        nav=PageNav(prev_href="04-01-chisla-i-peremennye.html", prev_label="Что такое число для компьютера", next_href="04-07-sistemy-schisleniya.html", next_label="Системы счисления"),
    )
    write("04-06-int-glubzhe.html", out)


def build_07_number_systems() -> None:
    same_value = converge_diagram(
        ["10", "0b1010", "0o12", "0xA"],
        "одно и то же число",
        caption="Четыре записи — один и тот же результат",
    )

    body = f"""
    <p>Мы привыкли записывать числа в <strong>десятичной</strong> системе (base 10) — десять
    цифр, от 0 до 9. Но это не единственный способ, и компьютеры часто используют другие
    системы счисления.</p>

    <h2 id="sistemy">Четыре системы, с которыми вы встретитесь</h2>
{comparison_table(
        ["Система", "Основание", "Цифры", "Python-литерал"],
        [
            ["Десятичная (decimal)", "10", "0–9", "<code class=\"inline\">10</code>"],
            ["Двоичная (binary)", "2", "0–1", "<code class=\"inline\">0b1010</code>"],
            ["Восьмеричная (octal)", "8", "0–7", "<code class=\"inline\">0o12</code>"],
            ["Шестнадцатеричная (hexadecimal)", "16", "0–9, A–F", "<code class=\"inline\">0xA</code>"],
        ],
    )}

{same_value}

    <h2 id="mesta-znachenij">Как читать позиционную запись</h2>
    <p>В любой системе счисления каждая позиция цифры имеет свой «вес» — степень основания.
    Возьмём двоичное число <code class="inline">1010</code>:</p>

{place_value_diagram(["1", "0", "1", "0"], [8, 4, 2, 1], total="10", caption="1010₂ = 1×8 + 0×4 + 1×2 + 0×1 = 10")}

    <p>Ровно тот же принцип работает и для десятичной системы, которой вы пользуетесь каждый
    день — просто вес позиций там 1000, 100, 10, 1 (степени десяти), а не степени двойки.</p>

    <h2 id="zachem-hex">Зачем программисту шестнадцатеричная система</h2>
    <p>Шестнадцатеричная запись встречается на практике куда чаще, чем кажется:</p>
    <ul>
      <li><strong>Цвета</strong> в вебе и графике: <code class="inline">#FF0000</code> — ярко-красный;</li>
      <li><strong>Байтовые/битовые шаблоны</strong> — компактная запись двоичных данных;</li>
      <li><strong>Сетевые протоколы и форматы файлов</strong> — MAC-адреса, хеш-суммы;</li>
      <li><strong>Символы Unicode</strong> — код символа часто записывают в hex (забегая вперёд,
        подробно про Unicode — в главе про строки).</li>
    </ul>
{code_block("cvet.py", "red = 0xFF\nprint(red)  # 255\n")}

    <h2 id="funkcii">Функции bin(), oct(), hex()</h2>
    <p>Переводят число ИЗ десятичной записи В строку с другой системой счисления:</p>
{code_block("v_druguyu_sistemu.py", "print(bin(10))  # '0b1010'\nprint(oct(10))  # '0o12'\nprint(hex(10))  # '0xa'\n")}

    <h2 id="parsing">int() с указанием основания — обратное преобразование</h2>
    <p>А функция <code class="inline">int()</code> с двумя аргументами делает обратное —
    читает текст в указанной системе счисления и возвращает обычное (десятичное) число:</p>
{code_block("iz_teksta.py", 'print(int("1010", 2))  # 10\nprint(int("FF", 16))   # 255\n')}

{callout(
        "tip",
        "🐍 Попробуем",
        "Переведите свой год рождения в двоичную и шестнадцатеричную запись через "
        "<code class=\"inline\">bin()</code> и <code class=\"inline\">hex()</code> — а затем "
        "переведите результат обратно через <code class=\"inline\">int(..., 2)</code> и "
        "<code class=\"inline\">int(..., 16)</code>, чтобы убедиться, что получили то же число.",
    )}

{practice_card(
        "04-07",
        "Практика: переводчик систем счисления",
        "Интерактивный ноутбук прямо в браузере — bin(), oct(), hex(), int(x, base)",
        "../../practice/04-07/index.html",
    )}"""

    out = render_page(
        page_title="Системы счисления",
        description="Десятичная, двоичная, восьмеричная и шестнадцатеричная запись чисел в "
        "Python: литералы, bin()/oct()/hex() и int() с основанием.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Системы счисления", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Как записывать числа: системы счисления",
        lede="Десятичная система — не единственная. Разберём двоичную, восьмеричную и "
        "шестнадцатеричную запись — и зачем они вообще нужны программисту.",
        body_html=body,
        sidebar_groups=sidebar("04-07-sistemy-schisleniya.html"),
        nav=PageNav(prev_href="04-06-int-glubzhe.html", prev_label="int — целые числа", next_href="04-02-kommentarii.html", next_label="Комментарии в вычислениях"),
    )
    write("04-07-sistemy-schisleniya.html", out)


def build_02_comments() -> None:
    body = f"""
    <p>Комментарии мы уже подробно разбирали в главе 3 — здесь не будем повторять весь урок, а
    сосредоточимся на том, чем комментарии особенно полезны именно в вычислениях: единицы
    измерения, формулы и скрытые предположения.</p>

    <h2 id="edinicy">Число само по себе не несёт единицу измерения</h2>
    <p>Взгляните на эту строку:</p>
{code_block("distance.py", "distance = 120  # км\n")}
    <p>Комментарий здесь помогает — но остаётся хрупким: он живёт отдельно от значения и никто
    не проверяет, что он всё ещё верен. Более надёжный (хоть и не идеальный) приём — включить
    единицу прямо в имя:</p>
{code_block("distance2.py", "distance_km = 120\n")}
    <p>Так яснее видно из самого кода, что именно хранится — без необходимости искать
    комментарий рядом. Мы вернёмся к более строгим способам связывать значения с их смыслом
    (типы, структуры данных) в следующих главах — здесь достаточно осознавать саму проблему:
    <strong>Python не знает, что число 120 означает километры</strong>. Это знание существует
    только в голове того, кто написал код — и в лучшем случае в имени или комментарии.</p>

    <h2 id="formuly">Комментарии для формул и предположений</h2>
    <p>Отдельная, очень полезная роль комментариев — объяснить формулу или зафиксировать
    предположение, которое иначе останется «магическим числом»:</p>
{code_block("nds.py", "# НДС в учебном примере: 23 %\nvat_rate = 0.23\nprice = 100\ntotal = price * (1 + vat_rate)\nprint(total)\n")}

{callout(
        "tip",
        "💡 Хороший комментарий объясняет то, чего не видно из кода",
        "<code class=\"inline\">vat_rate = 0.23</code> — само число не объясняет, откуда оно "
        "взялось и что означает. Комментарий <code class=\"inline\"># НДС в учебном примере: 23 "
        "%</code> отвечает именно на этот вопрос — «почему именно это число», а не «что делает "
        "эта строка».",
    )}

    <p>Этот же приём пригодится буквально в каждом разделе этой главы — формулы для площади
    круга, конвертации времени, скидок и процентов читаются заметно понятнее, если рядом
    зафиксировано, что означает каждое число.</p>

{practice_card(
        "04-02",
        "Практика: единицы измерения и комментарии к формулам",
        "Интерактивный ноутбук прямо в браузере — сделайте числовой код понятным",
        "../../practice/04-02/index.html",
    )}"""

    out = render_page(
        page_title="Комментарии в вычислениях",
        description="Комментарии для единиц измерения, формул и предположений в числовом коде — "
        "продолжение темы комментариев из главы 3, применительно к вычислениям.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Комментарии в вычислениях", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Комментарии в вычислениях: единицы, формулы и намерение",
        lede="Числа сами по себе не несут смысла — комментарии и осмысленные имена помогают "
        "зафиксировать, что именно они означают.",
        body_html=body,
        sidebar_groups=sidebar("04-02-kommentarii.html"),
        nav=PageNav(prev_href="04-07-sistemy-schisleniya.html", prev_label="Системы счисления", next_href="04-08-operatory.html", next_label="Арифметические операторы"),
    )
    write("04-02-kommentarii.html", out)


def build_08_operators() -> None:
    body = f"""
    <p>Python поддерживает полный набор арифметических операторов — большинство из них уже
    знакомы из математики, но у нескольких есть особое, «программистское» поведение.</p>

{comparison_table(
        ["Оператор", "Название", "Пример", "Результат"],
        [
            ["<code class=\"inline\">+</code>", "Сложение", "<code class=\"inline\">7 + 3</code>", "10"],
            ["<code class=\"inline\">-</code>", "Вычитание", "<code class=\"inline\">7 - 3</code>", "4"],
            ["<code class=\"inline\">*</code>", "Умножение", "<code class=\"inline\">7 * 3</code>", "21"],
            ["<code class=\"inline\">/</code>", "Деление (всегда float)", "<code class=\"inline\">7 / 3</code>", "2.333…"],
            ["<code class=\"inline\">//</code>", "Целочисленное деление", "<code class=\"inline\">7 // 3</code>", "2"],
            ["<code class=\"inline\">%</code>", "Остаток от деления", "<code class=\"inline\">7 % 3</code>", "1"],
            ["<code class=\"inline\">**</code>", "Возведение в степень", "<code class=\"inline\">7 ** 3</code>", "343"],
        ],
    )}

    <h2 id="unarnye">Унарные + и -</h2>
    <p>Плюс и минус работают и как унарные операторы — перед одним числом, без второго
    операнда:</p>
{code_block("unarnye.py", "x = 5\nprint(-x)   # -5\nprint(+x)   # 5 (унарный + почти не используется, но существует)\n")}

    <h2 id="v-dele">Операторы в связке с реальной задачей</h2>
    <p>Возьмём цену товара со скидкой:</p>
{code_block("skidka.py", 'price = 1000\ndiscount_percent = 15\ndiscount_amount = price * discount_percent / 100\nfinal_price = price - discount_amount\nprint(final_price)  # 850.0\n')}

{practice_card(
        "04-08",
        "Практика: арифметические операторы",
        "Интерактивный ноутбук прямо в браузере — предскажите и проверьте результат",
        "../../practice/04-08/index.html",
    )}"""

    out = render_page(
        page_title="Арифметические операторы",
        description="Полный набор арифметических операторов Python: +, -, *, /, //, %, ** и "
        "унарные + / -.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Арифметические операторы", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Арифметические операторы",
        lede="Полный набор операторов для работы с числами — от сложения до возведения в "
        "степень.",
        body_html=body,
        sidebar_groups=sidebar("04-08-operatory.html"),
        nav=PageNav(prev_href="04-02-kommentarii.html", prev_label="Комментарии в вычислениях", next_href="04-09-poryadok-operacij.html", next_label="Порядок выполнения операций"),
    )
    write("04-08-operatory.html", out)


def build_09_precedence() -> None:
    ladder = precedence_ladder(
        [
            ("()", "скобки — всегда выполняются первыми"),
            ("**", "возведение в степень"),
            ("+x  -x", "унарный плюс/минус"),
            ("*  /  //  %", "умножение, деление, целочисленное деление, остаток"),
            ("+  -", "сложение, вычитание"),
        ],
        caption="Порядок операций этой главы — от высшего приоритета к низшему",
    )

    body = f"""
    <p>Как и в математике, в Python операции выполняются не строго слева направо — у каждого
    оператора есть свой <strong>приоритет</strong>.</p>

{code_block("primer.py", "print(2 + 3 * 4)     # 14, а не 20\nprint((2 + 3) * 4)   # 20 — скобки меняют порядок\n")}

{ladder}

{callout(
        "info",
        "📚 Это не полная таблица",
        "Официальная таблица приоритетов Python включает намного больше операторов — сравнения, "
        "логические, битовые и другие, до которых мы ещё не дошли. Здесь — только то, что "
        "относится к арифметике этой главы. Полную таблицу можно найти в разделе «Operator "
        "precedence» на docs.python.org, когда она вам понадобится целиком.",
    )}

{callout(
        "tip",
        "🚀 Правило хорошего тона",
        "Даже когда вы точно помните приоритет операторов, скобки почти ничего не стоят, а "
        "читаемость улучшают ощутимо. Если есть сомнение, как прочитает выражение другой "
        "человек (или вы сами через полгода) — добавьте скобки.",
    )}

{practice_card(
        "04-09",
        "Практика: почините порядок операций",
        "Интерактивный ноутбук прямо в браузере — предскажите результат, затем расставьте скобки",
        "../../practice/04-09/index.html",
    )}"""

    out = render_page(
        page_title="Порядок выполнения операций",
        description="Приоритет арифметических операторов в Python и когда стоит добавлять "
        "скобки для читаемости.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Порядок выполнения операций", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Порядок выполнения операций",
        lede="2 + 3 * 4 — это 14 или 20? Разберём, в каком порядке Python на самом деле "
        "вычисляет выражения.",
        body_html=body,
        sidebar_groups=sidebar("04-09-poryadok-operacij.html"),
        nav=PageNav(prev_href="04-08-operatory.html", prev_label="Арифметические операторы", next_href="04-10-delenie-i-ostatok.html", next_label="Деление и остаток"),
    )
    write("04-09-poryadok-operacij.html", out)


def build_10_division() -> None:
    body = f"""
    <p>У деления в Python на самом деле три родственных, но разных оператора — и путаница между
    ними одна из самых частых у новичков.</p>

    <h2 id="konfety">17 конфет на 5 детей</h2>
    <p>Представим задачу: у нас 17 конфет, и мы делим их поровну между 5 детьми.</p>
    <div style="font-size:28px;text-align:center;padding:16px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);margin:20px 0;letter-spacing:4px">
      🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬🍬
    </div>
{code_block("konfety.py", "candies = 17\nchildren = 5\n\nprint(candies / children)   # 3.4  — точное дробное деление\nprint(candies // children)  # 3    — по 3 конфеты каждому ребёнку\nprint(candies % children)   # 2    — 2 конфеты остались нераспределены\n")}

    <p>Каждый ребёнок получает <code class="inline">candies // children</code> целых конфет, а
    <code class="inline">candies % children</code> — сколько осталось «в остатке». Удобно
    получить оба числа сразу:</p>
{code_block("divmod_demo.py", "print(divmod(17, 5))  # (3, 2)\n")}

    <h2 id="otricatelnoe">🚀 Чуть глубже: отрицательное floor-деление</h2>
    <p>С отрицательными числами <code class="inline">//</code> ведёт себя не так, как «просто
    отбросить дробную часть» — а округляет результат <strong>в сторону минус
    бесконечности</strong> (floor):</p>
{code_block("otricatelnoe.py", "print(-7 // 3)  # -3, а не -2\nprint(-7 % 3)   # 2\n")}

{number_line_diagram(
        [(-3, "-7 // 3"), (-2.333, "-7 / 3")],
        lo=-4, hi=0, highlight=-3,
        caption="-7 // 3 округляется вниз, к -3 (в сторону минус бесконечности), а не к -2",
    )}

{callout(
        "info",
        "💡 Почему так, а не иначе",
        "<code class=\"inline\">//</code> в Python определён как «floor division» — округление "
        "результата деления вниз, к ближайшему целому В СТОРОНУ минус бесконечности. Для "
        "положительных чисел это выглядит как обычное отбрасывание дробной части, но для "
        "отрицательных — даёт число МЕНЬШЕ, а не ближе к нулю. Это не баг, а осознанное "
        "определение оператора, одинаковое во всех версиях Python.",
    )}

{practice_card(
        "04-10",
        "Практика: деление, остаток и divmod()",
        "Интерактивный ноутбук прямо в браузере — включая отрицательное floor-деление",
        "../../practice/04-10/index.html",
    )}"""

    out = render_page(
        page_title="Деление и остаток",
        description="Три оператора деления в Python: /, // и % — на примере с конфетами, "
        "divmod() и отрицательное floor-деление.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Деление и остаток", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Деление: /, //, % и divmod()",
        lede="Три родственных оператора деления — и почему отрицательное целочисленное деление "
        "работает не так, как кажется на первый взгляд.",
        body_html=body,
        sidebar_groups=sidebar("04-10-delenie-i-ostatok.html"),
        nav=PageNav(prev_href="04-09-poryadok-operacij.html", prev_label="Порядок выполнения операций", next_href="04-11-stepeni.html", next_label="Степени и abs()"),
    )
    write("04-10-delenie-i-ostatok.html", out)


def build_11_powers() -> None:
    body = f"""
    <p>Возведение в степень в Python — оператор <code class="inline">**</code> или функция
    <code class="inline">pow()</code>:</p>
{code_block("stepeni.py", "print(2 ** 10)     # 1024\nprint(pow(2, 10))  # 1024 — то же самое\n")}

    <h2 id="pow-modulus">🚀 Необязательный третий аргумент pow()</h2>
    <p><code class="inline">pow()</code> умеет ещё и третий, необязательный аргумент —
    модуль:</p>
{code_block("pow_mod.py", "print(pow(2, 10, 1000))  # 24 — то же, что (2 ** 10) % 1000, но эффективнее для больших чисел\n")}
    <p>Такое «модульное возведение в степень» — важный строительный блок в алгоритмах и
    криптографии (мы не будем изучать криптографию сейчас — просто полезно знать, что этот
    инструмент существует и эффективен даже для огромных чисел).</p>

    <h2 id="abs">abs() — модуль числа</h2>
    <p><code class="inline">abs()</code> возвращает число без знака — расстояние до нуля:</p>
{code_block("abs_demo.py", "print(abs(-7))   # 7\nprint(abs(7))    # 7\nprint(abs(-3.5)) # 3.5\n")}

{practice_card(
        "04-11",
        "Практика: степени, pow() и abs()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-11/index.html",
    )}"""

    out = render_page(
        page_title="Степени и abs()",
        description="Возведение в степень оператором ** и функцией pow(), модульное "
        "возведение в степень, и функция abs().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Степени и abs()", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Степени, pow() и abs()",
        lede="Возведение в степень — и функция abs(), которая пригодится буквально в каждой "
        "следующей главе курса.",
        body_html=body,
        sidebar_groups=sidebar("04-11-stepeni.html"),
        nav=PageNav(prev_href="04-10-delenie-i-ostatok.html", prev_label="Деление и остаток", next_href="04-03-vidy-chisel.html", next_label="Карта числовых типов"),
    )
    write("04-11-stepeni.html", out)


def build_03_numeric_map() -> None:
    builtin_map = branch_diagram(
        "Числа в Python",
        [
            ("int", "целые числа"),
            ("float", "приближённые дробные (двоичная плавающая точка)"),
            ("complex", "действительная + мнимая часть"),
        ],
        caption="Три встроенных числовых типа — литералы понимает сам язык",
    )

    exact_map = branch_diagram(
        "Точные помощники из стандартной библиотеки",
        [
            ("Decimal", "десятичная точность — для денег и учёта"),
            ("Fraction", "точные обычные дроби p/q"),
        ],
        caption="Decimal и Fraction — НЕ встроенные литералы, а классы из модулей стандартной библиотеки",
    )

    body = f"""
    <p>Прежде чем идти глубже — соберём общую карту. В Python есть три <strong>встроенных</strong>
    числовых типа, литералы которых понимает сам язык:</p>

{builtin_map}

    <p>Кроме них, в стандартной библиотеке (модули, которые устанавливаются вместе с Python, но
    требуют явного <code class="inline">import</code>) есть ещё два важных числовых
    инструмента:</p>

{exact_map}

{callout(
        "warning",
        "⚠️ Важное различие",
        "<code class=\"inline\">int</code>, <code class=\"inline\">float</code> и "
        "<code class=\"inline\">complex</code> — часть самого языка: их литералы "
        "(<code class=\"inline\">42</code>, <code class=\"inline\">3.14</code>, "
        "<code class=\"inline\">3+4j</code>) работают без единого <code class=\"inline\">import</code>. "
        "<code class=\"inline\">Decimal</code> и <code class=\"inline\">Fraction</code> — обычные "
        "классы Python из модулей <code class=\"inline\">decimal</code> и "
        "<code class=\"inline\">fractions</code>, и без <code class=\"inline\">import</code> "
        "они недоступны. Мы разберём оба подробно в разделах 4.14–4.15.</p>",
    )}

    <p>Дальше в этой главе мы пройдём по каждому из пяти инструментов подробно — а в самом
    конце главы (раздел 4.22) соберём их все в одну финальную карту выбора: какой тип нужен для
    какой задачи.</p>"""

    out = render_page(
        page_title="Карта числовых типов",
        description="Обзорная карта числовых типов Python: встроенные int/float/complex и "
        "точные помощники Decimal/Fraction из стандартной библиотеки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Карта числовых типов", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Карта числовых типов Python",
        lede="Прежде чем идти глубже в каждый тип по отдельности — увидим общую картину целиком.",
        body_html=body,
        sidebar_groups=sidebar("04-03-vidy-chisel.html"),
        nav=PageNav(prev_href="04-11-stepeni.html", prev_label="Степени и abs()", next_href="04-12-float-osnovy.html", next_label="float — дробные числа"),
    )
    write("04-03-vidy-chisel.html", out)


def build_12_float_basics() -> None:
    body = f"""
    <p><code class="inline">float</code> — тип для чисел с дробной частью: измерения, цены,
    доли, научные величины. В отличие от <code class="inline">int</code>, у которого одна
    прямолинейная запись, у <code class="inline">float</code> их две.</p>

    <h2 id="obychnaya-zapis">Обычная запись</h2>
{code_block("float_obychnaya.py", "pi = 3.14\nprint(type(pi))\n\nwhole = 2.0\nprint(type(whole))  # float, несмотря на нулевую дробную часть\n")}

{callout(
        "info",
        "💡 Точка делает число float",
        "Даже <code class=\"inline\">2.0</code> — <code class=\"inline\">float</code>, а не "
        "<code class=\"inline\">int</code>, хотя математически это целое число. Тип определяет "
        "запись в коде, а не математический смысл значения.",
    )}

    <h2 id="nauchnaya-zapis">Научная (экспоненциальная) запись</h2>
    <p>Для очень больших или очень маленьких чисел удобна научная запись —
    <code class="inline">e</code> означает «умножить на 10 в степени»:</p>
{code_block("nauchnaya.py", "print(1e6)     # 1000000.0  (1 × 10^6)\nprint(2.5e-3)  # 0.0025     (2.5 × 10^-3)\n")}

    <h2 id="operacii">float в вычислениях</h2>
    <p>Оператор <code class="inline">/</code> (обычное деление, раздел 4.7) всегда возвращает
    <code class="inline">float</code>, даже если числа делятся нацело:</p>
{code_block("delenie_float.py", "print(10 / 2)  # 5.0, а не 5\n")}

{practice_card(
        "04-12",
        "Практика: float — запись и первые вычисления",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-12/index.html",
    )}"""

    out = render_page(
        page_title="float — дробные числа",
        description="Тип float в Python: обычная и научная запись, и почему деление всегда "
        "возвращает float.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("float — дробные числа", "")],
        kicker="Глава 4 · Python любит числа",
        h1="float — дробные числа",
        lede="Первое знакомство с float — прежде чем разобраться, почему его поведение иногда "
        "удивляет (следующий раздел).",
        body_html=body,
        sidebar_groups=sidebar("04-12-float-osnovy.html"),
        nav=PageNav(prev_href="04-03-vidy-chisel.html", prev_label="Карта числовых типов", next_href="04-13-pochemu-01-02.html", next_label="Почему 0.1 + 0.2 не равно 0.3"),
    )
    write("04-12-float-osnovy.html", out)


def build_13_float_precision() -> None:
    approx_flow = flow_diagram(
        [
            ("Десятичное\n0.1", "то, что вы написали"),
            ("Ближайшее\nдвоичное значение", "то, что реально хранится"),
            ("Крошечная\nошибка", "разница почти не заметна"),
        ],
        caption="0.1 не хранится ровно — хранится ближайшее представимое двоичное приближение",
    )

    sign_exp_sig = branch_diagram(
        "float (binary64)",
        [
            ("Знак", "плюс или минус"),
            ("Экспонента", "масштаб числа"),
            ("Мантисса", "значащие цифры"),
        ],
        caption="Из чего состоит типичный float на современном CPython (стандарт binary64)",
    )

    body = f"""
    <p>Один из самых знаменитых «сюрпризов» Python — да и практически любого языка
    программирования:</p>
{code_block("surpriz.py", "print(0.1 + 0.2)\n")}
{code_block("Реальный вывод", "0.30000000000000004", lang="text")}

{callout(
        "warning",
        "⚠️ Это не баг Python",
        "Точно такое же поведение вы увидите в JavaScript, Java, C, C++ и почти любом другом "
        "распространённом языке. Причина — не ошибка Python, а то, как ЛЮБОЙ компьютер хранит "
        "дробные числа в двоичном виде.",
    )}

    <h2 id="analogiya">Простая аналогия: 1/3 в десятичной записи</h2>
    <p>В десятичной системе <code class="inline">1/3</code> нельзя записать конечным числом
    цифр — только <code class="inline">0.333333...</code>, до бесконечности. Не потому, что
    десятичная система «плохая» — просто у неё есть числа, которые она не может выразить точно
    конечной записью.</p>
    <p>У компьютера в двоичной системе — точно такая же проблема, только с другими числами.
    <code class="inline">0.1</code> в десятичной записи выглядит «простым» — но в двоичной
    системе он превращается в бесконечно повторяющуюся дробь, совсем как <code class="inline">1/3</code>
    в десятичной. Компьютер вынужден её обрезать до конечного числа битов — отсюда и крошечная
    погрешность.</p>

{approx_flow}

    <h2 id="glubzhe">🔬 Что происходит глубже</h2>
    <p>На большинстве современных компьютеров и в стандартном CPython
    <code class="inline">float</code> соответствует аппаратному формату двойной точности,
    известному как <strong>binary64</strong> (часть стандарта IEEE 754). Концептуально число
    хранится тремя частями:</p>

{sign_exp_sig}

{callout(
        "info",
        "📚 Не нужно запоминать наизусть",
        "Точное число битов на каждую часть (1/11/52 в стандарте binary64) — деталь, которую не "
        "нужно заучивать прямо сейчас. Важно понимать сам принцип: значение хранится "
        "приближённо, а не то, что Python «плохо считает». Это распространённое, хорошо "
        "изученное поведение — стандарт binary64, а не собственное правило языка Python.",
    )}

    <h2 id="tochnoe-znachenie">Python может показать точное сохранённое значение</h2>
    <p>Хорошая новость: приближение не случайно и не загадочно — Python может показать вам,
    что именно хранится:</p>
{code_block("tochnoe.py", "print((0.1).as_integer_ratio())\n# (3602879701896397, 36028797018963968) — точная дробь, которая реально хранится\n")}
{code_block("hex_predstavlenie.py", 'print((0.1).hex())\n# \'0x1.999999999999ap-4\' — точное представление в шестнадцатеричном виде\n')}

{callout(
        "tip",
        "💡 Главный вывод раздела",
        "0.1 хранится не «примерно как получится», а как совершенно точное, предсказуемое и "
        "объяснимое приближение — просто не то десятичное число 0.1, которое вы написали. Это "
        "приближение, а не случайность.",
    )}

{practice_card(
        "04-13",
        "Практика: 0.1 + 0.2 — исследуем приближение",
        "Интерактивный ноутбук прямо в браузере — as_integer_ratio(), hex() и предсказание результата",
        "../../practice/04-13/index.html",
    )}"""

    out = render_page(
        page_title="Почему 0.1 + 0.2 не равно 0.3",
        description="Простое и точное объяснение бинарного приближения float: аналогия с 1/3, "
        "as_integer_ratio(), и краткий взгляд на IEEE 754 binary64.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Почему 0.1 + 0.2 не равно 0.3", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Почему 0.1 + 0.2 не равно ровно 0.3",
        lede="Самый знаменитый «сюрприз» float — и совершенно логичное, точное объяснение, "
        "почему он происходит.",
        body_html=body,
        sidebar_groups=sidebar("04-13-pochemu-01-02.html"),
        nav=PageNav(prev_href="04-12-float-osnovy.html", prev_label="float — дробные числа", next_href="04-14-sravnenie-float.html", next_label="Сравниваем float правильно"),
    )
    write("04-13-pochemu-01-02.html", out)


def build_14_float_comparison() -> None:
    body = f"""
    <p>Раз <code class="inline">0.1 + 0.2</code> не равно ровно <code class="inline">0.3</code>
    (раздел 4.11), прямое сравнение через <code class="inline">==</code> для float — плохая
    идея:</p>
{code_block("sravnenie_ploho.py", "print(0.1 + 0.2 == 0.3)  # False!\n")}

    <h2 id="isclose">math.isclose() — сравнение «достаточно близко»</h2>
    <p>Правильный инструмент — сравнение с допуском (tolerance): вместо «равно точно» проверяем
    «достаточно близко»:</p>
{code_block("isclose_demo.py", "from math import isclose\n\nprint(isclose(0.1 + 0.2, 0.3))  # True\n")}

{callout(
        "warning",
        "⚠️ Не изобретайте свой допуск на глаз",
        "Часто встречается самодельная проверка вроде <code class=\"inline\">abs(a - b) < "
        "0.000001</code>. Она работает не всегда — для очень больших или очень маленьких чисел "
        "фиксированный порог может оказаться слишком строгим или слишком мягким. "
        "<code class=\"inline\">math.isclose()</code> по умолчанию использует "
        "<strong>относительный</strong> допуск (пропорциональный размеру самих чисел), что "
        "гораздо надёжнее для чисел разного масштаба.",
    )}

{code_block("otnositelnyj_dopusk.py", "from math import isclose\n\nprint(isclose(1000.0001, 1000.0002))  # True — разница мала относительно размера чисел\nprint(isclose(0.0001, 0.0002))        # False — та же абсолютная разница, но огромна относительно размера\n")}

{practice_card(
        "04-14",
        "Практика: почините сравнение float",
        "Интерактивный ноутбук прямо в браузере — замените == на math.isclose()",
        "../../practice/04-14/index.html",
    )}"""

    out = render_page(
        page_title="Сравниваем float правильно",
        description="Почему == ненадёжен для float и как правильно сравнивать дробные числа "
        "через math.isclose().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Сравниваем float правильно", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Сравниваем float правильно",
        lede="== почти никогда не подходит для float. Разберём правильный инструмент — "
        "math.isclose().",
        body_html=body,
        sidebar_groups=sidebar("04-14-sravnenie-float.html"),
        nav=PageNav(prev_href="04-13-pochemu-01-02.html", prev_label="Почему 0.1 + 0.2 не равно 0.3", next_href="04-15-okruglenie.html", next_label="Округление"),
    )
    write("04-14-sravnenie-float.html", out)


def build_15_rounding() -> None:
    floor_line = number_line_diagram(
        [(-3, "floor(-2.3)"), (-2, "ceil(-2.3) и trunc(-2.3)")],
        lo=-4, hi=0, highlight=-2.3,
        caption="floor округляет вниз, к -3; ceil и trunc здесь совпадают — оба дают -2",
    )

    body = f"""
    <p>Есть сразу несколько способов превратить дробное число в целое — и они ведут себя
    по-разному, особенно для отрицательных чисел.</p>

    <h2 id="round">round() — обычное округление</h2>
{code_block("round_demo.py", "print(round(3.14159, 2))  # 3.14\nprint(round(7.5))          # 8\n")}

    <h2 id="chetnoe-okruglenie">Округление «до чётного» на границе .5</h2>
    <p>Внимательный взгляд на округление ровно посередине даёт неожиданный на первый взгляд
    результат:</p>
{code_block("granica.py", "print(round(2.5))  # 2, а не 3!\nprint(round(3.5))  # 4\n")}
{callout(
        "info",
        "💡 Округление до ближайшего чётного",
        "Это не ошибка и не случайность: <code class=\"inline\">round()</code> в Python "
        "округляет значение ровно между двумя целыми к БЛИЖАЙШЕМУ ЧЁТНОМУ — стандартный "
        "статистический приём («банковское округление»), который снижает систематический "
        "перекос при округлении множества значений. Для большинства повседневных задач это "
        "почти незаметно — но полезно знать, если результат округления вас удивил.",
    )}

    <h2 id="floor-ceil-trunc">math.floor(), math.ceil(), math.trunc()</h2>
{code_block("floor_ceil_trunc.py", "from math import floor, ceil, trunc\n\nprint(floor(-2.3))  # -3 — вниз, к меньшему целому\nprint(ceil(-2.3))   # -2 — вверх, к большему целому\nprint(trunc(-2.3))  # -2 — просто отбросить дробную часть\n")}

{floor_line}

{callout(
        "warning",
        "⚠️ Для отрицательных чисел это три разных ответа",
        "Для положительных чисел <code class=\"inline\">floor()</code> и "
        "<code class=\"inline\">trunc()</code> часто совпадают, поэтому разница легко ускользает "
        "от внимания. Для отрицательных — не совпадают почти никогда, как видно на числовой "
        "прямой выше.",
    )}

{practice_card(
        "04-15",
        "Практика: round, floor, ceil, trunc",
        "Интерактивный ноутбук прямо в браузере — предскажите результат для отрицательных чисел",
        "../../practice/04-15/index.html",
    )}"""

    out = render_page(
        page_title="Округление: round, floor, ceil, trunc",
        description="round() и округление до чётного, math.floor(), math.ceil(), math.trunc() "
        "и их разница для отрицательных чисел.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Округление", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Округление: round(), floor(), ceil(), trunc()",
        lede="Несколько способов превратить дробное число в целое — и почему для "
        "отрицательных чисел они дают разные ответы.",
        body_html=body,
        sidebar_groups=sidebar("04-15-okruglenie.html"),
        nav=PageNav(prev_href="04-14-sravnenie-float.html", prev_label="Сравниваем float правильно", next_href="04-16-decimal.html", next_label="Decimal"),
    )
    write("04-15-okruglenie.html", out)


def build_16_decimal() -> None:
    body = f"""
    <p>Мы уже видели, что <code class="inline">float</code> хранит приближение (раздел 4.11).
    Для большинства задач это не проблема — но для денег даже крошечная погрешность
    накапливается и может стать заметной. Для этого в стандартной библиотеке есть модуль
    <code class="inline">decimal</code>.</p>

{code_block("decimal_demo.py", 'from decimal import Decimal\n\nprint(Decimal("0.1") + Decimal("0.2"))  # 0.3 — точно, без погрешности\n')}

    <h2 id="stroka-ne-float">Создавайте Decimal из строки, не из float</h2>
    <p>Это едва ли не самая важная практическая деталь во всём разделе:</p>
{code_block("stroka_vs_float.py", 'from decimal import Decimal\n\nprint(Decimal("19.99"))  # Decimal(\'19.99\') — именно то, что вы написали\nprint(Decimal(19.99))    # Decimal(\'19.9900000000000002131628...\') — унаследовал погрешность float!\n')}

{callout(
        "warning",
        "⚠️ Почему так происходит",
        "<code class=\"inline\">Decimal(19.99)</code> сначала создаёт обычный "
        "<code class=\"inline\">float</code> <code class=\"inline\">19.99</code> — уже с тем "
        "самым приближением из раздела 4.11 — а потом заворачивает это приближённое значение в "
        "Decimal. Точность к этому моменту уже потеряна. "
        "<code class=\"inline\">Decimal(\"19.99\")</code> читает текст напрямую и не проходит "
        "через float вообще — поэтому сохраняет именно то значение, которое вы написали.",
    )}

    <h2 id="dengi-primer">Пример: покупка</h2>
{code_block("pokupka.py", 'from decimal import Decimal\n\nprice = Decimal("19.99")\nquantity = 3\ntotal = price * quantity\nprint(total)  # 59.97 — точно\n')}

    <h2 id="ne-vsegda-luchshe">Decimal — не «всегда лучше»</h2>
{comparison_table(
        ["", "float", "Decimal"],
        [
            ["Скорость", "Быстрый — аппаратная поддержка", "Медленнее — программная реализация"],
            ["Типичное применение", "Научные расчёты, измерения, общего назначения", "Деньги, бухгалтерия, где важна десятичная точность"],
            ["Точность", "Двоичное приближение", "Точная десятичная запись"],
        ],
    )}

{callout(
        "tip",
        "💡 Не заменяйте каждый float на Decimal",
        "Decimal — правильный выбор для денег и учёта, где важна десятичная точность и "
        "предсказуемое округление. Для большинства научных и повседневных вычислений обычный "
        "<code class=\"inline\">float</code> быстрее и абсолютно достаточен.",
    )}

{practice_card(
        "04-16",
        "Практика: Decimal и деньги",
        "Интерактивный ноутбук прямо в браузере — Decimal(str) vs Decimal(float)",
        "../../practice/04-16/index.html",
    )}"""

    out = render_page(
        page_title="Decimal — точная десятичная арифметика",
        description="Модуль decimal: точная десятичная арифметика для денег, и почему важно "
        "создавать Decimal из строки, а не из float.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Decimal", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Decimal — когда нужна точная десятичная арифметика",
        lede="Для денег и учёта даже крошечная погрешность float может быть неприемлема — "
        "разберём инструмент, который её убирает.",
        body_html=body,
        sidebar_groups=sidebar("04-16-decimal.html"),
        nav=PageNav(prev_href="04-15-okruglenie.html", prev_label="Округление", next_href="04-17-fraction.html", next_label="Fraction"),
    )
    write("04-16-decimal.html", out)


def build_17_fraction() -> None:
    third_bar = fraction_bar_diagram(1, 3, caption="Fraction(1, 3) — ровно одна треть, без приближения")

    decision = decision_map(
        [
            ("Нужен обычный расчёт или измерение?", "float"),
            ("Нужна десятичная точность (деньги)?", "Decimal"),
            ("Нужна точная дробь p/q?", "Fraction"),
        ],
        title="float vs Decimal vs Fraction",
        caption="Три инструмента для трёх разных видов точности",
    )

    body = f"""
    <p>Ещё один точный числовой инструмент из стандартной библиотеки —
    <code class="inline">Fraction</code>, обычная рациональная дробь «числитель / знаменатель»,
    без какого-либо приближения.</p>

{code_block("fraction_demo.py", "from fractions import Fraction\n\nthird = Fraction(1, 3)\nprint(third)  # 1/3\n")}

{third_bar}

    <h2 id="arifmetika">Арифметика с Fraction — точная</h2>
{code_block("fraction_math.py", "from fractions import Fraction\n\nresult = Fraction(1, 3) + Fraction(1, 6)\nprint(result)  # 1/2 — точно, не приближённо\n")}

    <h2 id="iz-teksta-vs-float">Fraction из текста и из float — тоже разница</h2>
{code_block("fraction_stroka.py", 'from fractions import Fraction\n\nprint(Fraction("0.1"))  # 1/10 — прочитано из десятичного текста точно\nprint(Fraction(0.1))    # 3602879701896397/36028797018963968 — унаследовал приближение float!\n')}
    <p>Та же самая логика, что и с <code class="inline">Decimal</code> в разделе 4.14: если
    сначала создать <code class="inline">float</code>, приближение уже произошло раньше, чем
    <code class="inline">Fraction</code> успел его получить.</p>

    <h2 id="sravnenie-troih">float, Decimal и Fraction рядом</h2>
{comparison_table(
        ["Инструмент", "Представляет", "Точен для", "Типичное применение"],
        [
            ["<code class=\"inline\">float</code>", "Двоичное приближение", "Степеней двойки и их сумм", "Наука, измерения, общие расчёты"],
            ["<code class=\"inline\">Decimal</code>", "Десятичную дробь", "Десятичных значений", "Деньги, бухгалтерия"],
            ["<code class=\"inline\">Fraction</code>", "Рациональное число p/q", "Любой обычной дроби", "Точная рациональная арифметика"],
        ],
    )}

{decision}

{practice_card(
        "04-17",
        "Практика: Fraction и точные дроби",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-17/index.html",
    )}"""

    out = render_page(
        page_title="Fraction — точные дроби",
        description="Модуль fractions: точные рациональные числа p/q, и итоговое сравнение "
        "float, Decimal и Fraction.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Fraction", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Fraction — точные обычные дроби",
        lede="Когда нужна не десятичная, а самая обычная точная дробь — числитель через "
        "знаменатель, без приближения.",
        body_html=body,
        sidebar_groups=sidebar("04-17-fraction.html"),
        nav=PageNav(prev_href="04-16-decimal.html", prev_label="Decimal", next_href="04-18-kompleksnye-chisla.html", next_label="complex и cmath"),
    )
    write("04-17-fraction.html", out)


def build_18_complex() -> None:
    plane = complex_plane_diagram(3, 4, caption="z = 3 + 4j на комплексной плоскости")

    body = f"""
    <p><code class="inline">complex</code> — тип для комплексных чисел: значений вида
    «действительная часть + мнимая часть». В Python мнимую единицу записывают буквой
    <code class="inline">j</code> (а не <code class="inline">i</code>, как в математике —
    инженерное соглашение, чтобы не путать с обозначением тока).</p>

{code_block("complex_demo.py", "z = 3 + 4j\nprint(z)\nprint(type(z))\n")}

    <h2 id="chasti">Действительная и мнимая часть</h2>
{code_block("real_imag.py", "z = 3 + 4j\nprint(z.real)  # 3.0\nprint(z.imag)  # 4.0\nprint(abs(z))  # 5.0 — длина вектора от начала координат\n")}

{plane}

    <h2 id="gde-primenyaetsya">Где встречается на практике</h2>
    <p>В обычном прикладном коде комплексные числа — редкость. Но в некоторых областях они
    незаменимы:</p>
    <ul>
      <li><strong>Электротехника</strong> — расчёт переменного тока;</li>
      <li><strong>Обработка сигналов</strong> — преобразование Фурье и связанные вычисления;</li>
      <li><strong>Системы управления</strong> — анализ устойчивости;</li>
      <li><strong>Физика</strong> — квантовая механика, волновые процессы.</li>
    </ul>
    <p>Если ни одна из этих областей не входит в ваши ближайшие планы — вполне нормально
    просто знать, что <code class="inline">complex</code> существует, и вернуться к этому
    разделу, когда он действительно понадобится.</p>

    <h2 id="cmath">cmath — математика для комплексных чисел</h2>
    <p>Обычный модуль <code class="inline">math</code> (раздел 4.18) не умеет работать с
    комплексными числами — для них есть отдельный модуль <code class="inline">cmath</code>:</p>
{code_block("cmath_demo.py", "import cmath\n\nz = 3 + 4j\nprint(cmath.phase(z))  # угол вектора z в радианах\n")}

{practice_card(
        "04-18",
        "Практика: комплексная плоскость",
        "Интерактивный ноутбук прямо в браузере — real, imag, abs() для комплексных чисел",
        "../../practice/04-18/index.html",
    )}"""

    out = render_page(
        page_title="complex и cmath",
        description="Комплексные числа в Python: real, imag, комплексная плоскость и модуль "
        "cmath для комплексной математики.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("complex и cmath", "")],
        kicker="Глава 4 · Python любит числа",
        h1="complex — комплексные числа",
        lede="Последний из трёх встроенных числовых типов — для инженерных и научных задач, "
        "где нужна и действительная, и мнимая часть.",
        body_html=body,
        sidebar_groups=sidebar("04-18-kompleksnye-chisla.html"),
        nav=PageNav(prev_href="04-17-fraction.html", prev_label="Fraction", next_href="04-04-preobrazovanie-tipov.html", next_label="Преобразование типов чисел"),
    )
    write("04-18-kompleksnye-chisla.html", out)


def build_04_conversions() -> None:
    cvm = classic_vs_modern(
        "Сборка строки из чисел: конкатенация → f-строка",
        "Классический подход",
        'age = 10\nmessage = "Возраст: " + str(age) + " лет"\nprint(message)\n'
        "# обязательно вручную оборачивать число в str()",
        "Современный Python 3.14",
        'age = 10\nmessage = f"Возраст: {age} лет"\nprint(message)\n'
        "# f-строка сама выполняет преобразование внутри {}",
        "f-строки (f-strings), появившиеся в Python 3.6 и с тех пор ставшие стандартом. Они "
        "короче, меньше подвержены ошибкам (не нужно помнить о str()) и позволяют сразу писать "
        "выражения внутри фигурных скобок.",
    )

    body = f"""
    <p>У каждого числового типа есть своя функция-преобразователь с тем же именем:
    <code class="inline">int()</code>, <code class="inline">float()</code>,
    <code class="inline">complex()</code>. Кроме того, любое число можно превратить в текст
    функцией <code class="inline">str()</code> — и наоборот, текст, похожий на число, можно
    превратить обратно.</p>

{code_block("preobrazovanie.py", 'whole = int(3.99)\nprint(whole)      # 3 — дробная часть отбрасывается, а не округляется\n\ndecimal = float(7)\nprint(decimal)    # 7.0\n\ntext = str(42)\nprint(text, type(text))   # "42" <class \'str\'>\n')}

{callout(
        "warning",
        "⚠️ int() отбрасывает дробную часть, а не округляет",
        "<code class=\"inline\">int(3.99)</code> равно <code class=\"inline\">3</code>, а не "
        "<code class=\"inline\">4</code> — это <strong>усечение</strong> (truncation) в сторону "
        "нуля, а не округление. Для настоящего округления нужна отдельная функция "
        "<code class=\"inline\">round()</code> (раздел 4.13).",
    )}

    <p>Направление усечения важно и для отрицательных чисел — <code class="inline">int()</code>
    всегда идёт К нулю, а не «вниз» в математическом смысле:</p>
{code_block("int_otricatelnoe.py", "print(int(3.9))   # 3\nprint(int(-3.9))  # -3, а не -4\n")}

    <h2 id="tekst-v-chislo">Преобразование текста в число</h2>
{code_block("tekst_v_chislo.py", 'age_text = "10"\nage = int(age_text)\nprint(age + 5)   # 15 — теперь это настоящее число\n')}

{callout(
        "warning",
        "⚠️ Не любой текст получится преобразовать",
        "<code class=\"inline\">int(\"десять\")</code> вызовет <code class=\"inline\">ValueError</code> "
        "— Python не умеет читать числа словами. Преобразовать можно только текст, который "
        "выглядит как число.",
    )}

    <h2 id="s-osnovaniem">Разбор текста с указанием системы счисления</h2>
    <p>Мы уже видели это в разделе 4.3 — <code class="inline">int()</code> умеет читать текст не
    только в десятичной системе:</p>
{code_block("s_osnovaniem.py", 'print(int("1010", 2))  # 10\nprint(int("FF", 16))   # 255\n')}

{cvm}

{practice_card(
        "04-04",
        "Практика: int(), float(), str() и парсинг с основанием",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-04/index.html",
    )}"""

    out = render_page(
        page_title="Преобразование типов чисел",
        description="int(), float(), str() и типичные ошибки при преобразовании типов в "
        "Python, включая разбор текста с указанием системы счисления.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Преобразование типов чисел", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Преобразование типов чисел",
        lede="Числа можно превращать друг в друга и в текст — но не всегда наоборот, и не "
        "всегда так, как кажется на первый взгляд.",
        body_html=body,
        sidebar_groups=sidebar("04-04-preobrazovanie-tipov.html"),
        nav=PageNav(prev_href="04-18-kompleksnye-chisla.html", prev_label="complex и cmath", next_href="04-19-modul-math.html", next_label="Модуль math"),
    )
    write("04-04-preobrazovanie-tipov.html", out)


def build_19_math_module() -> None:
    math_map = capability_map(
        [
            ("Константы", ["pi · e · tau · inf · nan"]),
            ("Корни и степени", ["sqrt · isqrt · pow"]),
            ("Округление", ["floor · ceil · trunc"]),
            ("Целочисленная математика", ["factorial · gcd · lcm", "comb · perm"]),
            ("Геометрия", ["hypot · dist"]),
            ("Тригонометрия", ["sin · cos · tan", "radians · degrees"]),
        ],
        title="math",
        caption="math как организованный набор возможностей, а не случайный список имён",
    )

    body = f"""
    <p>Модуль <code class="inline">math</code> из стандартной библиотеки — набор готовых
    математических инструментов, которые не нужно писать самостоятельно.</p>
{code_block("import.py", "import math\n\nprint(math.sqrt(16))  # 4.0\n")}

{math_map}

    <h2 id="konstanty">Константы</h2>
{code_block("konstanty.py", "import math\n\nprint(math.pi)   # 3.141592653589793\nprint(math.e)    # 2.718281828459045\nprint(math.tau)  # 6.283185307179586 — это 2 * pi\n")}

    <h2 id="korni-stepeni">Корни и степени</h2>
{code_block("korni.py", "import math\n\nprint(math.sqrt(16))    # 4.0 — квадратный корень (float)\nprint(math.isqrt(16))   # 4   — целочисленный квадратный корень (int)\n")}

    <h2 id="celochislennaya">Целочисленная математика</h2>
{code_block("celochislennaya.py", "import math\n\nprint(math.factorial(5))  # 120 — 5!\nprint(math.gcd(12, 18))   # 6   — наибольший общий делитель\nprint(math.lcm(4, 6))     # 12  — наименьшее общее кратное\nprint(math.comb(5, 2))    # 10  — число сочетаний\nprint(math.perm(5, 2))    # 20  — число размещений\n")}

    <h2 id="geometriya">Геометрия</h2>
{code_block("geometriya.py", "import math\n\nprint(math.hypot(3, 4))       # 5.0 — гипотенуза (длина вектора)\nprint(math.dist((0, 0), (3, 4)))  # 5.0 — расстояние между точками\n")}

    <h2 id="trigonometriya">🚀 Тригонометрия — краткий обзор</h2>
    <p>Тригонометрические функции работают в <strong>радианах</strong>, а не градусах:</p>
{code_block("trig.py", "import math\n\nangle_deg = 90\nangle_rad = math.radians(angle_deg)\nprint(math.sin(angle_rad))  # 1.0\n")}
    <p>Если сейчас тригонометрия не входит в ваши задачи — вполне нормально вернуться к этому
    подразделу позже.</p>

{practice_card(
        "04-19",
        "Практика: модуль math",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-19/index.html",
    )}"""

    out = render_page(
        page_title="Модуль math",
        description="Организованный обзор стандартного модуля math: константы, корни, "
        "округление, целочисленная математика, геометрия и тригонометрия.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Модуль math", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Модуль math",
        lede="Готовый набор математических инструментов из стандартной библиотеки — "
        "организованный по смыслу, а не по алфавиту.",
        body_html=body,
        sidebar_groups=sidebar("04-19-modul-math.html"),
        nav=PageNav(prev_href="04-04-preobrazovanie-tipov.html", prev_label="Преобразование типов чисел", next_href="04-20-random-i-secrets.html", next_label="random и secrets"),
    )
    write("04-19-modul-math.html", out)


def build_20_random_secrets() -> None:
    decision = branch_diagram(
        "Нужна случайность?",
        [
            ("random", "симуляции, игры, обучение"),
            ("secrets", "токены, пароли, безопасность"),
        ],
        caption="Выбор модуля зависит от того, поставлена ли безопасность на карту",
    )

    body = f"""
    <p>Модуль <code class="inline">random</code> из стандартной библиотеки генерирует
    <strong>псевдослучайные</strong> числа — они выглядят случайными и достаточно хороши для игр,
    симуляций и учебных примеров.</p>

{code_block("random_demo.py", "import random\n\nprint(random.randint(1, 6))   # случайное целое от 1 до 6 включительно\nprint(random.random())        # случайное число от 0.0 до 1.0\nprint(random.choice([\"орёл\", \"решка\"]))  # случайный выбор из списка\n")}

    <h2 id="seed">Воспроизводимость через seed</h2>
    <p>Иногда нужно, чтобы «случайная» последовательность повторялась — например, для отладки.
    Для этого есть <code class="inline">seed()</code>:</p>
{code_block("seed_demo.py", "import random\n\nrandom.seed(42)\nprint(random.randint(1, 100))  # всегда одно и то же число при одном и том же seed\n")}

{decision}

    <h2 id="bezopasnost">⚠️ БЕЗОПАСНОСТЬ: random — не для паролей и токенов</h2>
{callout(
        "warning",
        "⚠️ Не генерируйте пароли и токены модулем random",
        "<code class=\"inline\">random</code> оптимизирован для скорости и статистического "
        "качества, а не для непредсказуемости против злоумышленника — его результат в принципе "
        "можно предсказать, зная внутреннее состояние генератора. Для всего "
        "«чувствительного к безопасности» (пароли, токены сессий, ключи) используйте модуль "
        "<code class=\"inline\">secrets</code>.",
    )}
{code_block("secrets_demo.py", "import secrets\n\ntoken = secrets.token_hex(16)\nprint(token)  # криптографически стойкий случайный токен\n")}

{practice_card(
        "04-20",
        "Практика: random vs secrets",
        "Интерактивный ноутбук прямо в браузере — выберите правильный инструмент для задачи",
        "../../practice/04-20/index.html",
    )}"""

    out = render_page(
        page_title="random и secrets",
        description="Модуль random для игр и симуляций, seed для воспроизводимости, и модуль "
        "secrets для случайности, чувствительной к безопасности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("random и secrets", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Случайные числа: random и secrets",
        lede="Два модуля для случайности — и правило, которое стоит запомнить с первого дня: "
        "не всякая случайность одинаково безопасна.",
        body_html=body,
        sidebar_groups=sidebar("04-20-random-i-secrets.html"),
        nav=PageNav(prev_href="04-19-modul-math.html", prev_label="Модуль math", next_href="04-21-statistics-i-inf-nan.html", next_label="statistics, inf и nan"),
    )
    write("04-20-random-i-secrets.html", out)


def build_21_statistics_inf_nan() -> None:
    special_values = capability_map(
        [
            ("inf", ["+∞", "бесконечность", "math.isinf()"]),
            ("-inf", ["−∞", "минус бесконечность", "math.isinf()"]),
            ("nan", ["не число", "not a number", "math.isnan()"]),
        ],
        title="Особые значения float",
        caption="Три особых состояния, которые может принимать float — проверяются тремя разными функциями",
    )

    body = f"""
    <h2 id="statistics">Модуль statistics</h2>
    <p>Простые статистические расчёты уже есть в стандартной библиотеке — не нужно писать их
    вручную:</p>
{code_block("statistics_demo.py", "import statistics\n\nscores = [85, 90, 78, 92, 88]\n\nprint(statistics.mean(scores))    # 86.6 — среднее\nprint(statistics.median(scores))  # 88   — медиана (среднее значение по порядку)\n")}

    <h2 id="mode-stdev">🚀 Мода и стандартное отклонение</h2>
{code_block("mode_stdev.py", "import statistics\n\nscores = [85, 90, 78, 92, 88]\n\nprint(statistics.mode(scores))    # самое частое значение\nprint(statistics.pstdev(scores))  # стандартное отклонение генеральной совокупности\n")}
    <p>Это лишь маленькая часть модуля <code class="inline">statistics</code> — задача этого
    раздела не превратить курс в курс статистики, а показать: типовые статистические расчёты
    уже есть готовыми в Python, и не нужно писать формулу среднего вручную каждый раз.</p>

    <h2 id="inf-nan">Особые значения: inf и nan</h2>
    <p>Кроме обычных чисел, <code class="inline">float</code> умеет представлять несколько
    особых состояний:</p>
{code_block("inf_nan_demo.py", 'positive_infinity = float("inf")\nnegative_infinity = float("-inf")\nnot_a_number = float("nan")\n\nprint(positive_infinity)  # inf\nprint(not_a_number)       # nan\n')}

{special_values}

{callout(
        "warning",
        "⚠️ nan не равен даже самому себе",
        "Одно из самых неожиданных свойств <code class=\"inline\">nan</code>: сравнение "
        "<code class=\"inline\">nan == nan</code> возвращает <code class=\"inline\">False</code>. "
        "Это не ошибка Python, а часть стандарта IEEE 754 (тот же стандарт, что мы упоминали в "
        "разделе про float) — nan специально определён как «не равный ничему, включая себя».",
    )}
{code_block("nan_sravnenie.py", 'x = float("nan")\nprint(x == x)  # False!\n')}

    <h2 id="proverki">Как проверять эти состояния правильно</h2>
{code_block("proverki.py", 'import math\n\nx = float("nan")\ny = float("inf")\n\nprint(math.isnan(x))     # True\nprint(math.isinf(y))     # True\nprint(math.isfinite(5.0))  # True — обычное конечное число\n')}

    <p>Такие значения не выдумка — они реально появляются в данных и вычислениях: деление,
    дающее переполнение, отсутствующие данные при анализе, результат неопределённой операции.
    Полезно уметь распознать их и обработать осознанно, а не удивляться, откуда они взялись.</p>

{practice_card(
        "04-21",
        "Практика: statistics, inf и nan",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-21/index.html",
    )}"""

    out = render_page(
        page_title="statistics, inf и nan",
        description="Модуль statistics для простых расчётов, и особые значения float — inf и "
        "nan, включая почему nan != nan.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("statistics, inf и nan", "")],
        kicker="Глава 4 · Python любит числа",
        h1="statistics, inf и nan",
        lede="Готовые статистические инструменты — и особые числовые состояния, которые "
        "полезно уметь распознавать.",
        body_html=body,
        sidebar_groups=sidebar("04-21-statistics-i-inf-nan.html"),
        nav=PageNav(prev_href="04-20-random-i-secrets.html", prev_label="random и secrets", next_href="04-22-chislovye-oshibki.html", next_label="Числовые ошибки и отладка"),
    )
    write("04-21-statistics-i-inf-nan.html", out)


def build_22_debugging() -> None:
    def _branch(header: str, symptoms: list[str], action: str) -> str:
        symptoms_html = "<br>".join(html.escape(s) for s in symptoms)
        return f"""
        <div style="flex:1;min-width:230px;max-width:340px;display:flex;flex-direction:column;align-items:center;gap:10px">
          <div style="width:100%;box-sizing:border-box;padding:14px 16px;background:#5B24F9;color:#fff;
            border-radius:14px;text-align:center;font-family:Sora,sans-serif;font-weight:700;font-size:14px">{html.escape(header)}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#0D0230;text-align:center;line-height:1.7">{symptoms_html}</div>
          <div style="color:#B9A0FC;font-size:20px">↓</div>
          <div style="width:100%;box-sizing:border-box;padding:14px 16px;border:1.5px solid #5B24F9;
            border-radius:14px;text-align:center;font-size:13px;color:#0D0230">{html.escape(action)}</div>
        </div>"""

    error_flow = f"""
    <div style="margin:24px 0;padding:24px 20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      <div style="text-align:center;font-family:Sora,sans-serif;font-weight:700;font-size:17px;color:#0D0230;margin-bottom:20px">Что пошло не так?</div>
      <div style="display:flex;justify-content:center;gap:32px;flex-wrap:wrap">
{_branch(
        "Python остановился с исключением",
        ["ZeroDivisionError", "ValueError", "TypeError"],
        "Читаем traceback и исправляем причину",
    )}
{_branch(
        "Код выполнился без исключения",
        ["Но результат выглядит неожиданно"],
        "Проверяем математическую модель и представление чисел",
    )}
      </div>
      <div style="text-align:center;color:#B9A0FC;font-size:22px;margin:14px 0">↓</div>
      <div style="max-width:420px;margin:0 auto;box-sizing:border-box;padding:14px 18px;background:#5B24F9;color:#fff;
        border-radius:14px;text-align:center;font-family:Sora,sans-serif;font-weight:700;font-size:14px">
        Исправляем код, ожидания или выбор числового типа
      </div>
    </div>"""

    def lab(num, title, code, symptom, explanation):
        return f"""
        <div class="callout callout-debug">
          <div>
            <div class="callout-title">🐞 Лаборатория {num}. {title}</div>
            <div class="callout-body">
{code_block("предскажите и запустите", code, lang="python")}
              <p><strong>Наблюдение:</strong> {symptom}</p>
              <p><strong>Объяснение:</strong> {explanation}</p>
            </div>
          </div>
        </div>"""

    labs_html = "".join([
        lab(1, "Почему 10 / 2 даёт 5.0?", "print(10 / 2)",
            "результат — <code class=\"inline\">5.0</code>, а не <code class=\"inline\">5</code>.",
            "оператор <code class=\"inline\">/</code> в Python ВСЕГДА возвращает float (раздел 4.7), даже при делении нацело."),
        lab(2, "Почему int(3.99) равно 3?", "print(int(3.99))",
            "результат — <code class=\"inline\">3</code>, а не <code class=\"inline\">4</code>.",
            "<code class=\"inline\">int()</code> отбрасывает дробную часть (усечение к нулю), а не округляет (раздел 4.16)."),
        lab(3, "Почему сравнение 0.1 + 0.2 == 0.3 не срабатывает?", "print(0.1 + 0.2 == 0.3)",
            "результат — <code class=\"inline\">False</code>.",
            "float хранит приближение (раздел 4.11) — используйте <code class=\"inline\">math.isclose()</code> вместо <code class=\"inline\">==</code>."),
        lab(4, "Почему Decimal(0.1) выглядит странно?", 'from decimal import Decimal\nprint(Decimal(0.1))',
            "результат — длинная некруглая дробь, а не <code class=\"inline\">0.1</code>.",
            "аргумент — float, а значит приближение из раздела 4.11 уже произошло ДО создания Decimal. Используйте <code class=\"inline\">Decimal(\"0.1\")</code>."),
        lab(5, "Почему 7 // 3 отличается от 7 / 3?", "print(7 // 3)\nprint(7 / 3)",
            "<code class=\"inline\">2</code> против <code class=\"inline\">2.333...</code>.",
            "<code class=\"inline\">//</code> — целочисленное деление (отбрасывает дробную часть результата), <code class=\"inline\">/</code> — обычное деление, всегда float."),
        lab(6, "Предскажите: -7 // 3 и -7 % 3", "print(-7 // 3)\nprint(-7 % 3)",
            "<code class=\"inline\">-3</code> и <code class=\"inline\">2</code> — не то, что многие ожидают.",
            "<code class=\"inline\">//</code> округляет к минус бесконечности, а не к нулю (раздел 4.7)."),
        lab(7, "Исправьте: int(\"FF\", 16)", 'print(int("FF"))', "ValueError: invalid literal for int() with base 10: 'FF'",
            "без указания основания <code class=\"inline\">int()</code> ожидает десятичную запись. Нужно: <code class=\"inline\">int(\"FF\", 16)</code>."),
        lab(8, "Почините ZeroDivisionError", "price = 100\nquantity = 0\nprint(price / quantity)",
            "ZeroDivisionError: division by zero.",
            "перед делением стоит проверить делитель на ноль, если он может быть нулевым — подробно про условия будет в следующей главе; здесь достаточно узнать сам тип ошибки."),
        lab(9, "Выберите верный числовой тип", "# Задача: посчитать точную сумму чека в рублях и копейках",
            "float способен дать погрешность в дробных суммах.",
            "для денег правильный выбор — <code class=\"inline\">Decimal</code> (раздел 4.14), а не <code class=\"inline\">float</code>."),
    ])

    body = f"""
    <p>Собрали девять коротких лабораторий — часть из них про настоящие ошибки с исключением,
    часть — про валидный, но неожиданный числовой результат. Важно уметь отличать эти два
    сценария.</p>

{error_flow}

{labs_html}

{practice_card(
        "04-22",
        "Практика: отладка числовых ошибок",
        "Интерактивный ноутбук прямо в браузере — найдите и исправьте типичные числовые проблемы",
        "../../practice/04-22/index.html",
    )}"""

    out = render_page(
        page_title="Числовые ошибки и отладка",
        description="Девять лабораторий отладки числового кода: ZeroDivisionError, "
        "ValueError, погрешность float и выбор правильного числового типа.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Числовые ошибки и отладка", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Числовые ошибки и отладка",
        lede="Девять коротких лабораторий — от настоящих исключений до валидных, но "
        "неожиданных числовых результатов.",
        body_html=body,
        sidebar_groups=sidebar("04-22-chislovye-oshibki.html"),
        nav=PageNav(prev_href="04-21-statistics-i-inf-nan.html", prev_label="statistics, inf и nan", next_href="04-05-mini-proekt-itogi.html", next_label="Мини-проекты и итоги"),
    )
    write("04-22-chislovye-oshibki.html", out)


def build_05_mini_projects() -> None:
    final_map = decision_map(
        [
            ("Нужен целый счёт?", "int"),
            ("Нужно обычное дробное измерение?", "float"),
            ("Нужна точная десятичная сумма (деньги)?", "Decimal"),
            ("Нужна точная дробь p/q?", "Fraction"),
            ("Нужна действительная + мнимая часть?", "complex"),
            ("Нужны готовые математические функции?", "math / cmath"),
            ("Нужна случайность для игр/симуляций?", "random"),
            ("Нужна случайность для безопасности?", "secrets"),
        ],
        title="Какой числовой тип/инструмент мне нужен?",
        caption="Главная сводная карта главы 4 — возвращайтесь к ней в будущих проектах",
    )

    body = f"""
    <p>Три небольших, но настоящих проекта — каждый использует только то, что мы уже прошли в
    этой главе (и в главе 3).</p>

    <h2 id="proekt-a">Проект A: калькулятор покупки</h2>
    <p>Вводим цену и количество, считаем сумму. Сравним float и Decimal на одном и том же
    примере:</p>
{code_block(
        "kalkulyator_pokupki.py",
        'from decimal import Decimal\n\n'
        '# Версия на float — обычная, но с риском погрешности\n'
        'price_float = 19.99\nquantity = 3\nprint(price_float * quantity)  # 59.97 — здесь совпало, но не всегда так повезёт\n\n'
        '# Версия на Decimal — предсказуемая точность для денег\n'
        'price_decimal = Decimal("19.99")\nprint(price_decimal * quantity)  # 59.97 — точно, гарантированно\n',
    )}
{exercise(1, "Challenge", "Добавьте налог (например, 23%) к сумме — версией на Decimal.")}

    <h2 id="proekt-b">Проект B: конвертер времени</h2>
    <p>Вводим общее число секунд — считаем часы, минуты и секунды через <code class="inline">//</code>
    и <code class="inline">%</code> (раздел 4.7) — здесь у этих операторов появляется настоящее
    применение:</p>
{code_block(
        "konverter_vremeni.py",
        'total_seconds = 3725\n\n'
        'hours = total_seconds // 3600\n'
        'minutes = (total_seconds % 3600) // 60\n'
        'seconds = total_seconds % 60\n\n'
        'print(f"{hours}ч {minutes}м {seconds}с")  # 1ч 2м 5с\n',
    )}
{exercise(2, "Challenge", "Проверьте свою функцию на 0 секунд и на 90000 секунд (больше суток).")}

    <h2 id="proekt-c">Проект C: геометрический калькулятор</h2>
    <p>Вводим радиус окружности — считаем диаметр, длину окружности и площадь через
    <code class="inline">math.pi</code>:</p>
{code_block(
        "geometricheskij.py",
        'import math\n\n'
        'radius = 5\n'
        'diameter = radius * 2\n'
        'circumference = 2 * math.pi * radius\n'
        'area = math.pi * radius ** 2\n\n'
        'print(f"Диаметр: {diameter}")\n'
        'print(f"Длина окружности: {circumference:.2f}")\n'
        'print(f"Площадь: {area:.2f}")\n',
    )}
{exercise(3, "Challenge · системы счисления", "Дополнительно: напишите мини-«переводчик» — по введённому десятичному числу выведите его bin(), oct() и hex() (раздел 4.3).")}

{practice_card(
        "04-05",
        "Практика: мини-проекты главы 4",
        "Интерактивный ноутбук прямо в браузере — калькулятор покупки, конвертер времени, геометрия",
        "../../practice/04-05/index.html",
    )}

    <h2 id="finalnaya-karta">Финальная карта: какой числовой тип мне нужен?</h2>
{final_map}

    <h2 id="itogi">Итоги главы</h2>
{summary_box("Что мы теперь умеем", [
        "Понимаем разницу между математическим числом и его представлением в компьютере, и "
        "что имена указывают на неизменяемые числовые объекты — не «коробки».",
        "Уверенно работаем с int: произвольная точность, связь с bool, подчёркивания-разделители.",
        "Понимаем системы счисления — decimal/binary/octal/hex — и умеем конвертировать между ними.",
        "Знаем полный набор арифметических операторов и их порядок выполнения.",
        "Различаем /, // и % — и понимаем, как работает отрицательное floor-деление.",
        "Понимаем, почему 0.1 + 0.2 не равно ровно 0.3, и умеем сравнивать float через "
        "math.isclose().",
        "Умеем округлять числа через round(), floor(), ceil() и trunc() — и знаем их разницу "
        "для отрицательных чисел.",
        "Знаем, когда использовать Decimal (деньги) и Fraction (точные дроби) вместо float.",
        "Понимаем complex и комплексную плоскость, и умеем пользоваться math/cmath, "
        "random/secrets и statistics.",
        "Умеем распознавать inf и nan, и отлаживать типичные числовые ошибки.",
        "Собрали три мини-проекта, использующих числа Python для реальных задач.",
    ])}

{callout(
        "tip",
        "🚀 Что дальше",
        "В главе 5 мы продолжим работать с числами — сравнения, логические операции и первые "
        "условные конструкции.",
    )}"""

    out = render_page(
        page_title="Мини-проекты и итоги",
        description="Три мини-проекта главы 4 — калькулятор покупки, конвертер времени, "
        "геометрический калькулятор — и финальная карта выбора числового типа.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Мини-проекты и итоги", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Мини-проекты и итоги главы",
        lede="Собираем всё пройденное в три небольших, но настоящих проекта — и подводим "
        "итоги главы финальной картой выбора числового типа.",
        body_html=body,
        sidebar_groups=sidebar("04-05-mini-proekt-itogi.html"),
        nav=PageNav(prev_href="04-22-chislovye-oshibki.html", prev_label="Числовые ошибки и отладка", next_href="../glava-05/index.html", next_label="Глава 5: Давайте поиграем с числами!"),
    )
    write("04-05-mini-proekt-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01_what_is_a_number()
    build_06_int_deeper()
    build_07_number_systems()
    build_02_comments()
    build_08_operators()
    build_09_precedence()
    build_10_division()
    build_11_powers()
    build_03_numeric_map()
    build_12_float_basics()
    build_13_float_precision()
    build_14_float_comparison()
    build_15_rounding()
    build_16_decimal()
    build_17_fraction()
    build_18_complex()
    build_04_conversions()
    build_19_math_module()
    build_20_random_secrets()
    build_21_statistics_inf_nan()
    build_22_debugging()
    build_05_mini_projects()
    print(f"Готово: {len(PAGES)} страниц Главы 4")
