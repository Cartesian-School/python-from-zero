# M01 -- Russian technical terminology register

Scope covered: Chapters 2-4 (Batch A); to be extended by each later batch

Policy: Prefer the term a working Russian-speaking Python developer would actually say and immediately understand. Do not mechanically translate every English term, and do not force a Russian gloss after a term is already established.

This register is additive: later batches (Chapters 5-24) extend it with new terms
as they are encountered, and revisit an existing entry only when a batch finds a real,
evidenced inconsistency -- not to relitigate an already-settled decision without cause.

| English | Preferred RU | Accepted variants | Avoid | Chapters |
|---|---|---|---|---|
| interpreter | интерпретатор | -- | -- | 2, 3, 4 |
| terminal | терминал | -- | -- | 2, 3 |
| shell | shell (командная оболочка) | командная оболочка | исполняющая оболочка (unused, awkward if it appeared) | 2, 3 |
| Python REPL / Python Shell | Python REPL | Python Shell (only when quoting English documentation's own naming) | 'Python-оболочка' as a free-standing translation without qualifying it as distinct from an OS shell | 3 |
| PATH (environment variable) | переменная окружения PATH | PATH (bare, once introduced) | 'путь' alone for the variable (reserve 'путь' for a filesystem path, a distinct concept the course correctly keeps separate) | 2 |
| virtual environment | виртуальное окружение | окружение (once venv is established) | 'виртуальная среда окружения' (redundant, awkward double-noun stacking) | 2 |
| package (PyPI/pip) | пакет | -- | -- | 2 |
| extension (editor) | расширение | -- | -- | 2 |
| name / variable | имя (переменная) | переменная (once 'имя' is established as the precise term) | 'переменная' alone as the ONLY term where the reference/binding distinction matters -- the course correctly leads with 'имя' to support the reference model | 3, 4 |
| reference / binding | ссылка | указывает на (verb form: 'the name points to the object') | 'переменная содержит значение' (contains a value) -- the exact calque/false-model the course explicitly and correctly rejects | 3, 4 |
| object / value | объект / значение | -- | -- | 3, 4 |
| namespace | пространство имён | -- | -- | 3 |
| exception | исключение | -- | -- | 3, 4 |
| traceback | traceback | трассировка (as an occasional descriptive gloss, e.g. 'трассировка исключения') | forcing 'трассировка' as the primary, exclusive term throughout learner-facing prose | 3 |
| int / integer | целое число | int (the type name itself, left as code) | -- | 4 |
| float | число с плавающей точкой | float (bare, once introduced, especially in code-adjacent prose) | -- | 4 |
| truncation vs rounding | усечение / округление | -- | using 'округление' loosely for int()'s truncation behavior | 4 |
| floor division | целочисленное деление | floor-деление (in the specifically-negative-number deep-dive subsection) | -- | 4 |
| banker's rounding / round-half-to-even | округление до чётного | банковское округление (used once as an English-speaking-industry cross-reference) | -- | 4 |
| CPython implementation detail | деталь реализации CPython | -- | presenting a CPython-specific behavior (small-int caching, immediate refcount-zero deallocation) as a guaranteed Python-language rule | 3, 4 |
| random (module) vs secrets (module) | random / secrets (module names left as code, never translated) | -- | treating 'случайный' (random) as a single undifferentiated safety level for both modules | 4 |
| IDE / editor | редактор кода / IDE (contextual) | среда разработки (for 'IDE' when spelled out) | treating VS Code and PyCharm's roles as identical to 'the interpreter' -- the course explicitly and repeatedly guards against this conflation ('IDE does not own the environment') | 2 |
| breakpoint | точка останова | -- | 'брейкпоинт' as the primary term (real usage exists but 'точка останова' is the more broadly recognized, professionally standard Russian term and is what the course correctly uses) | 2, 3 |
| kernel (Jupyter) | ядро | -- | conflating 'ядро' (kernel, the running process) with 'notebook' (the file) | 2, 3 |

## Rationale and evidence per term

### interpreter -> интерпретатор

Standard, universal Russian CS term with no viable alternative; matches course-wide usage exactly.

- **Evidence:** scripts/build_chapter_02.py (used consistently across all 18 lessons); scripts/build_chapter_03.py:01
- **First-use guidance:** No parenthetical English gloss needed; the term is already the default in Russian technical speech.
- **Affected chapters:** 2, 3, 4

### terminal -> терминал

Directly borrowed, universally understood, no natural alternative in professional use.

- **Evidence:** scripts/build_chapter_02.py:02-04-terminal-shell-i-path; scripts/build_chapter_03.py:03-06
- **First-use guidance:** None needed.
- **Affected chapters:** 2, 3

### shell -> shell (командная оболочка)

The course correctly keeps 'shell' untranslated as the primary term while glossing it once as 'командная оболочка' on first use, and explicitly and correctly warns that English documentation's 'Python Shell' (the REPL) is a different sense of the same word from an OS shell (Bash/PowerShell). This is the single highest-value terminology decision in Chapters 2-3 and is handled correctly.

- **Evidence:** scripts/build_chapter_03.py:03-06-terminal-shell-i-python-repl (dedicated disambiguation section with a warning callout)
- **First-use guidance:** Gloss once at first use ('shell (командная оболочка)'), then use 'shell' bare; never call the Python REPL a 'shell' without immediately qualifying it as 'Python REPL' or 'Python Shell' to avoid the exact collision the course itself warns about.
- **Affected chapters:** 2, 3

### Python REPL / Python Shell -> Python REPL

REPL is the course's own established acronym (Read-Eval-Print-Loop), introduced and used consistently; 'Python Shell' is kept only as an explicit cross-reference to the name used in English documentation, not as the course's own default term.

- **Evidence:** scripts/build_chapter_03.py:03-02-interaktivny-rezhim
- **First-use guidance:** Introduce as 'Python REPL (он же Python Shell)' once, then use 'REPL' consistently.
- **Affected chapters:** 3

### PATH (environment variable) -> переменная окружения PATH

The course precisely distinguishes 'путь' (a filesystem path) from 'переменная окружения PATH' (the specific lookup variable) rather than conflating them, which is the correct and more precise choice.

- **Evidence:** scripts/build_chapter_02.py:02-04-terminal-shell-i-path
- **First-use guidance:** Full form 'переменная окружения PATH' on first use, then 'PATH' bare afterward.
- **Affected chapters:** 2

### virtual environment -> виртуальное окружение

'виртуальное окружение' is the standard, widely used Russian developer term; the course never uses the awkward, redundant longer form.

- **Evidence:** scripts/build_chapter_02.py:02-10-zachem-nuzhny-venv, 02-11-sozdanie-venv
- **First-use guidance:** None beyond the course's own motivating explanation of why isolation is needed before naming the term.
- **Affected chapters:** 2

### package (PyPI/pip) -> пакет

Standard term; the course explicitly and correctly distinguishes it from 'расширение' (a VS Code extension) with a dedicated callout, preventing a real and common beginner conflation.

- **Evidence:** scripts/build_chapter_02.py:02-07-vscode-ustanovka-i-rasshireniya ('Расширение != пакет' callout), 02-12-pervyj-paket
- **First-use guidance:** None needed beyond the explicit disambiguation from 'extension' already present.
- **Affected chapters:** 2

### extension (editor) -> расширение

Standard term; correctly kept distinct from 'пакет' (package).

- **Evidence:** scripts/build_chapter_02.py:02-07-vscode-ustanovka-i-rasshireniya
- **First-use guidance:** None needed.
- **Affected chapters:** 2

### name / variable -> имя (переменная)

The course's central Chapter 3 model (a name points to a value, not a box containing it) requires 'имя' as the precise term, with 'переменная' used as the familiar, accepted synonym once the model is established. This precision is exactly what the M01 rubric's SM03 criterion and the M01-I04 brief's 'имя vs переменная' check ask for, and it is handled correctly.

- **Evidence:** scripts/build_chapter_03.py:03-11-imena-i-znacheniya
- **First-use guidance:** Lead with 'имя' when precision matters (binding/rebinding/aliasing discussions); 'переменная' is fine in casual, non-precision-critical prose.
- **Affected chapters:** 3, 4

### reference / binding -> ссылка

This is the single most important terminology decision in the whole curriculum's early chapters: the course explicitly names and rejects the 'box containing a value' model in favor of 'ссылка' / 'указывает на', which is both more natural in Russian and technically correct for Python's actual binding semantics.

- **Evidence:** scripts/build_chapter_03.py:03-11-imena-i-znacheniya (explicit 'Не коробка' section); reused correctly in scripts/build_chapter_04.py:04-01
- **First-use guidance:** Introduce with the arrow/reference diagram already used by the course before any formal definition.
- **Affected chapters:** 3, 4

### object / value -> объект / значение

Used precisely and distinctly throughout: an object is the thing in memory; a value is what it represents. No conflation found.

- **Evidence:** scripts/build_chapter_03.py:03-11-imena-i-znacheniya; scripts/build_chapter_04.py:04-01
- **First-use guidance:** None needed.
- **Affected chapters:** 3, 4

### namespace -> пространство имён

Standard, correct Russian CS term, introduced with an English gloss on first use per the course's own first-use convention.

- **Evidence:** scripts/build_chapter_03.py:03-11-imena-i-znacheniya ('пространство имён (namespace)')
- **First-use guidance:** 'пространство имён (namespace)' once, then 'пространство имён' bare -- exactly what the course already does.
- **Affected chapters:** 3

### exception -> исключение

Standard term, used consistently; the course correctly distinguishes exception types by name (NameError, SyntaxError, IndentationError, ValueError, TypeError, ZeroDivisionError, ModuleNotFoundError) rather than using 'ошибка' (error) as a single undifferentiated catch-all.

- **Evidence:** scripts/build_chapter_03.py:03-13-oshibki-i-traceback; scripts/build_chapter_04.py:04-22-chislovye-oshibki
- **First-use guidance:** None needed.
- **Affected chapters:** 3, 4

### traceback -> traceback

Independently checked against Russian Python documentation and community usage: official docs.python.ru-style sources translate the module name as 'трассировка', but working tutorials and blogs (python-scripts.com, webdevblog.ru) commonly keep 'traceback' untranslated in running prose, which matches how Russian-speaking developers actually talk about it day to day. The course's choice to keep 'traceback' as the primary learner-facing term, with 'трассировка' used only as an occasional clarifying gloss, matches real professional usage better than a strict, exclusive translation would.

- **Evidence:** scripts/build_chapter_03.py:03-13-oshibki-i-traceback; web verification: http://grep.cs.msu.ru/python3.8_RU/... (official-style translation uses 'трассировка'); https://python-scripts.com/python-traceback and https://webdevblog.ru/traceback-v-python/ (community usage keeps 'Traceback')
- **First-use guidance:** Use 'traceback' as the primary term throughout; 'трассировка' may appear once as a clarifying gloss but should not replace 'traceback' as the default.
- **Affected chapters:** 3

### int / integer -> целое число

Standard term; the course correctly keeps the type name 'int' as code/inline-code rather than translating it, while using 'целое число' in prose.

- **Evidence:** scripts/build_chapter_04.py:04-06-int-glubzhe
- **First-use guidance:** None needed.
- **Affected chapters:** 4

### float -> число с плавающей точкой

Standard term; the course uses the full Russian phrase for the concept and 'float' bare for the type/code identifier, a natural and common split in Russian technical writing.

- **Evidence:** scripts/build_chapter_04.py:04-12-float-osnovy
- **First-use guidance:** None needed beyond keeping 'float' as code when referring to the type.
- **Affected chapters:** 4

### truncation vs rounding -> усечение / округление

This precise distinction is exactly the kind of terminological precision the M01 rubric's SM03 asks for, and the course gets it right with a dedicated warning callout distinguishing int()'s truncation-toward-zero from round()'s rounding.

- **Evidence:** scripts/build_chapter_04.py:04-04-preobrazovanie-tipov
- **First-use guidance:** None needed beyond the existing warning callout.
- **Affected chapters:** 4

### floor division -> целочисленное деление

The course correctly explains that // rounds toward negative infinity (a fixed language definition), not simply 'discards the fractional part', which would be incorrect for negative operands -- exactly the kind of implementation-vs-specification precision the M01 rubric's Dimension A calls for.

- **Evidence:** scripts/build_chapter_04.py:04-10-delenie-i-ostatok
- **First-use guidance:** None needed.
- **Affected chapters:** 4

### banker's rounding / round-half-to-even -> округление до чётного

Correct, standard Russian statistical/CS term, with the informal English-industry name given once for cross-reference.

- **Evidence:** scripts/build_chapter_04.py:04-15-okruglenie
- **First-use guidance:** None needed.
- **Affected chapters:** 4

### CPython implementation detail -> деталь реализации CPython

This exact distinction is named as a specific audit risk in the M01-I04 brief (Section 15: 'implementation-specific CPython details are not presented as universal Python-language rules'). The course handles it correctly and repeatedly, explicitly contrasting CPython's behavior with PyPy's different memory-management approach.

- **Evidence:** scripts/build_chapter_03.py:03-11-imena-i-znacheniya (refcounting aside); scripts/build_chapter_04.py:04-06-int-glubzhe (id()-caching warning)
- **First-use guidance:** Always name 'CPython' explicitly rather than 'Python' when describing an implementation detail.
- **Affected chapters:** 3, 4

### random (module) vs secrets (module) -> random / secrets (module names left as code, never translated)

This is the specific historical risk item ('random.random() description') the M01-I04 brief named for re-verification; the course draws the security boundary explicitly and correctly (random is not for passwords/tokens; secrets is), matching official Python guidance exactly.

- **Evidence:** scripts/build_chapter_04.py:04-20-random-i-secrets
- **First-use guidance:** None needed beyond the existing explicit security callout.
- **Affected chapters:** 4

### IDE / editor -> редактор кода / IDE (contextual)

The course's central Chapter 2 message (editor != interpreter != pip != venv) depends on keeping these terms distinct, and it does so consistently across all 17 non-opener lessons.

- **Evidence:** scripts/build_chapter_02.py:02-01, 02-08, 02-09, 02-15
- **First-use guidance:** None needed.
- **Affected chapters:** 2

### breakpoint -> точка останова

Standard, correct, professionally recognized Russian developer term.

- **Evidence:** scripts/build_chapter_02.py:02-08-vscode-konfiguraciya; scripts/build_chapter_03.py:03-15-otladchik-v-ide
- **First-use guidance:** None needed.
- **Affected chapters:** 2, 3

### kernel (Jupyter) -> ядро

Standard, correct Russian Jupyter term; the course explicitly and correctly separates the notebook file from the kernel process it runs against.

- **Evidence:** scripts/build_chapter_02.py:02-15-ide-i-okruzheniya; scripts/build_chapter_03.py:03-16-notebook-i-kernel
- **First-use guidance:** None needed.
- **Affected chapters:** 2, 3
