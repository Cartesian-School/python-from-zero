# M01 -- Russian technical terminology register

Scope covered: Chapters 2-20 (Batch A: 2-4; Batch B: 5-8; Batch C: 9-12; Batch D: 13-16; Batch E: 17-20); to be extended by each later batch

Policy: Prefer the term a working Russian-speaking Python developer would actually say and immediately understand. Do not mechanically translate every English term, and do not force a Russian gloss after a term is already established.

This register is additive: later batches (Chapters 17-24) extend it with new terms
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
| expression vs statement | выражение / инструкция | оператор (only for `x = 5 + 3` style, never as a synonym for 'операция') | using 'выражение' and 'инструкция' interchangeably -- the course draws a precise, correct distinction between them | 5 |
| operator precedence | приоритет операторов | -- | 'порядок операций' as the primary term (acceptable as an occasional gloss, but 'приоритет' is what Python developers say) | 5 |
| associativity | ассоциативность | -- | -- | 5 |
| truthiness | истинность | 'ложность' only as the direct negation, not as a standalone primary term | stating a general 'every non-empty value is True' rule before the generalizing type (list, dict, etc.) is taught -- the course correctly scopes the claim to strings only and explicitly marks the general rule as a Chapter 9 forward reference | 8 |
| immutability (string) | неизменяемость | неизменяемый (adjective, applied to a specific type: 'строки неизменяемы') | 'срез — это всегда копия' stated without qualification -- true for strings (immutable) but the course is careful to scope this claim to strings and note lists differ later | 8 |
| membership (in / not in) | in / not in (left as code, described with the verb 'содержит' / 'входит') | проверка вхождения | 'принадлежность' as a free-standing noun -- the course never uses this abstract noun for string membership, preferring concrete verb phrasing ('содержится ли одна строка внутри другой', 'входит ли ... в ...'), which reads more naturally in Russian and is what a working developer would say | 8 |
| index | индекс | -- | -- | 8 |
| slice | срез | -- | 'срез — это всегда копия' as an unqualified universal claim -- correct for the built-in sequence type covered so far (str), but the course should keep this scoped when mutable sequences are introduced later | 8 |
| sequence (string as a sequence of characters) | последовательность (символов) | -- | -- | 8 |
| escape sequence | экранирование | служебная последовательность (for \n, \t specifically) | -- | 8 |
| raw string | raw-строка | -- | translating 'raw' (e.g. 'сырая строка') -- 'raw-строка' is the term Python developers actually use in Russian | 8 |
| f-string | f-строка | форматированная строковая литеральная запись (only as a one-time formal gloss, never as the primary working term) | -- | 8 |
| equality vs identity (== vs is) | == сравнивает значение, is сравнивает объект (descriptive phrasing, not the noun 'идентичность') | -- | introducing the formal noun 'идентичность' before Chapter 14, where `is` is formally taught -- the course correctly uses plain descriptive language ('is проверяет, один ли это объект в памяти') instead | 8 |
| heading (turtle graphics) | курс | направление (as an occasional plain-language gloss) | 'заголовок' -- a false-friend calque of 'heading' in its document-heading sense, which would be actively misleading here | 6, 7 |
| seed (random module) | seed (left as code; described with 'воспроизводимость') | зерно (unused by the course; would be an unnecessary and unfamiliar calque) | translating 'seed' to 'зерно' or similar -- no working Russian-speaking Python developer says this; 'seed' is used bare, exactly as in English-language code and documentation | 5 |
| condition | условие | -- | -- | 9 |
| branching | ветвление | -- | -- | 9 |
| truthiness (general rule, all types) | истинность | -- | treating the general rule (0/None/empty-collection are falsy, everything else truthy) as available before Chapter 9 -- the course correctly waits until enough types (numbers, None) exist to state it fully | 9 |
| short-circuit evaluation | short-circuit (короткое замыкание) | короткое замыкание (as an explanatory gloss on first use) | presenting short-circuiting only as a performance optimization -- the course correctly and additionally frames it as a genuine safety technique (guarding against IndexError), which is the more important practical lesson at this level | 9 |
| control flow | поток управления | -- | overclaiming implementation-level precision -- the course explicitly and correctly labels its own 'invisible pointer' explanation as a simplified mental model, not a claim about CPython internals | 9 |
| loop vocabulary (loop/body/iteration/counter/accumulator) | цикл / тело цикла / итерация / счётчик / накопитель | -- | conflating 'счётчик' (counter, counts iterations) with 'накопитель' (accumulator, accumulates a result) -- the course correctly treats them as two distinct, precisely-named roles for loop state | 10 |
| sentinel value | сентинел | сентинел-цикл (for the specific loop pattern) | translating 'sentinel' literally as 'часовой' or similar -- no working Russian-speaking Python developer uses this; the transliterated 'сентинел' is standard | 10 |
| off-by-one error | off-by-one (ошибка на единицу) | ошибка на единицу (as a Russian gloss, used interchangeably once introduced) | -- | 9, 10 |
| mutability (list vs tuple) | изменяемость / неизменяемость | -- | implying mutability depends on a value's content rather than its type -- the course explicitly and correctly states mutability is a property of the TYPE (all list are mutable, all tuple/str are not), preempting a natural but wrong generalization | 11 |
| aliasing | aliasing (совместная ссылка) | совместная ссылка (as an explanatory gloss) | describing 'b = a' as 'copying' the list in any sense -- the course precisely and repeatedly states this creates a second NAME for the same object, not a second object | 11 |
| shallow copy | поверхностная копия | -- | assuming .copy()/list(...)/[:]  produce a fully independent copy for nested structures -- the course correctly and explicitly demonstrates the shared-inner-list trap before introducing deepcopy as the fix | 11 |
| hashability | хешируемость | -- | explaining hashability via hash-table implementation details at this level -- the course correctly keeps the explanation at the operational level (a hashable value cannot change unexpectedly while stored in a set/dict key) | 11 |
| comprehension (list/set/dict) | comprehension (генератор списков / словаря / множества) | генератор списков (specifically for list comprehension, an established Russian rendering) | introducing comprehension syntax before the equivalent explicit loop -- the course consistently shows the loop-with-append() version first, then the comprehension as a compact alternative, at every one of its three introductions (11-04 preview, 11-22 full treatment, and again contrasted in 11-04's classic-vs-modern block) | 11 |
| decomposition | декомпозиция | -- | -- | 12 |
| refactoring | рефакторинг | -- | conflating refactoring with 'making the code work' -- the course correctly and precisely defines it as improving structure WITHOUT changing behavior, demonstrated by showing the hardcoded and data-driven quiz versions behave identically for the same input | 12 |
| parameter vs argument | параметр (в определении) / аргумент (в вызове) | -- | using 'параметр' and 'аргумент' interchangeably -- casual Russian-language material often blurs them, but the course draws the distinction precisely and consistently | 13 |
| LEGB (scope resolution order) | LEGB (left as the English acronym; each letter explained in Russian) | Local -> Enclosing -> Global -> Builtins (spelled out in the elif_ladder_diagram) | inventing a Russian acronym or translating the letters -- 'LEGB' is the term working Python developers actually use and search for | 13 |
| closure | замыкание | -- | 'закрытие' (a literal but semantically wrong calque -- reads as 'closing', not the functional-programming concept) | 13 |
| keyword-only / positional-only parameters | параметры только по имени (keyword-only) / только по позиции (positional-only) | -- | translating 'keyword-only'/'positional-only' into a single unclear Russian phrase without keeping the English term visible -- the syntax markers (bare * and /) are themselves language-agnostic and readers will meet the English names in real documentation | 13 |
| pure function vs side effect | чистая функция / побочный эффект | -- | 'сайд-эффект' (an unnecessary Runglish loanword when a precise, established Russian term already exists) | 13 |
| self (not a keyword) | self (left as code; explicitly described as convention, not a reserved word) | -- | presenting 'self' as a Python keyword or reserved word -- it is an ordinary parameter name that happens to be universal convention | 14 |
| encapsulation | инкапсуляция | -- | presenting Python's __name mangling as 'true privacy' -- the course explicitly and correctly debunks this ('в Python нет настоящей приватности на уровне языка') | 14 |
| composition (HAS-A) vs inheritance (IS-A) | композиция (HAS-A) / наследование (IS-A) | -- | translating HAS-A/IS-A into Russian -- the course correctly keeps these as bare English mnemonics since they are the standard OOP vocabulary a developer will meet in any language's documentation | 14 |
| duck typing | duck typing (left as the English term; described via the 'если это выглядит как утка...' idiom) | -- | 'утиная типизация' as the primary form without keeping 'duck typing' visible -- both should appear, since 'duck typing' is what appears in real error discussions and interviews | 14 |
| dunder / special methods | специальные методы (дандер-методы as an accepted colloquial variant) | дандер-методы (from 'double underscore'; used colloquially in the Russian-speaking Python community) | 'магические методы' (a widely-seen but discouraged calque of 'magic methods' -- the course correctly avoids implying anything mystical about a well-defined protocol) | 14 |
| dataclass | dataclass (left as code/the decorator name; described as 'класс-данные' or 'класс для хранения данных') | -- | implying @dataclass produces something other than a normal class -- the course explicitly and correctly debunks this misconception | 14 |
| serialization / deserialization | сериализация / десериализация | -- | using only informal phrasing ('сохранить в файл') without the precise terms -- the course explicitly introduces the precise vocabulary via a dedicated callout | 15 |
| current working directory (CWD) | текущая рабочая директория (CWD as an accepted bare acronym) | CWD (used bare after first introduction, matching real tooling/documentation) | conflating CWD with 'the folder where the script file lives' -- the course dedicates an entire section and a Debug Lab specifically to correcting this exact misconception | 15 |
| event-driven programming | событийно-ориентированное программирование | -- | describing mainloop()/the event loop as the program 'freezing' or 'waiting idly' -- the course explicitly and repeatedly corrects this exact misconception | 16 |
| widget | виджет | -- | 'элемент управления' as the primary term -- 'виджет' is what Russian-speaking Tkinter/GUI developers actually say and is used consistently by the course itself | 16 |
| event binding (bind()) | привязка события | bind() | биндинг | 17 |
| input focus | фокус ввода | фокус | -- | 17 |
| source of truth | источник истины | -- | -- | 17, 18 |
| canvas | холст | Canvas (виджет) | канвас | 18 |
| canvas item / item id | элемент Canvas / идентификатор элемента | item ID | -- | 18 |
| stacking order (z-order) | порядок наложения | -- | z-order (без перевода) | 18 |
| game tick | игровой тик | -- | -- | 19 |
| game loop | игровой цикл | -- | -- | 19, 20 |
| direction vector | вектор направления | вектор смещения (dx, dy) | -- | 19 |
| game state vs game status | состояние игры (GameState) / статус игры (GameStatus) | -- | -- | 19 |
| frame vs animation frame | кадр (шаг игрового цикла) / кадр анимации | -- | -- | 20 |
| delta time (dt) | delta time (dt) | -- | дельта времени | 20 |
| sprite | спрайт | -- | -- | 20 |
| hitbox / AABB collision | хитбокс / AABB (прямоугольники, выровненные по осям) | -- | -- | 20 |
| world vs screen coordinates | мировые / экранные координаты | -- | -- | 20 |

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

### expression vs statement -> выражение / инструкция

Chapter 5 introduces a precise, professionally correct distinction: an expression (выражение) always has a value and can be substituted wherever a value is expected; a statement (инструкция, e.g. assignment) does not. The course uses this to explain, correctly, why `print(x = 5)` is an error while `print(x == 5)` is valid. This is exactly the terminology a working Python developer would use.

- **Evidence:** scripts/build_chapter_05.py:05-01-osnovnye-operacii (callout 'Выражение — не то же самое, что команда (statement)')
- **First-use guidance:** Introduce both terms together, in contrast, the first time an assignment statement is shown next to a bare expression -- exactly as Chapter 5 does.
- **Affected chapters:** 5

### operator precedence -> приоритет операторов

Standard, universally understood Russian developer term; the course builds a full precedence ladder (**, unary +/-, */,//,%, +/-) and uses it consistently across every arithmetic lesson in Chapter 5.

- **Evidence:** scripts/build_chapter_05.py:05-09-unarnye-operatory, 05-03-prisvaivanie-poryadok (precedence_ladder diagrams)
- **First-use guidance:** None needed -- already the default term.
- **Affected chapters:** 5

### associativity -> ассоциативность

Standard term, correctly used to explain the one real trap in this area: `**` is right-associative (2 ** 3 ** 2 == 512, not 64) while most other operators are left-associative. Verified correct by direct execution.

- **Evidence:** scripts/build_chapter_05.py:05-10-associativnost
- **First-use guidance:** Introduce with a worked left-associative example (subtraction) before the right-associative exception (**), matching the course's order.
- **Affected chapters:** 5

### truthiness -> истинность

Chapter 8 correctly bounds this claim to strings specifically (bool("") == False, bool(" ") == True since a space is non-empty) and explicitly labels the general boolean-coercion rule as material for Chapter 9's full `if`. This is exactly the kind of scope discipline the audit was asked to check for and found done correctly.

- **Evidence:** scripts/build_chapter_08.py:08-05-istina-lozh (section 'Пустая строка — это «ложь»')
- **First-use guidance:** When truthiness is introduced for a new type in a later chapter, follow the same pattern: state the rule for that type only, and cross-reference rather than re-generalize prematurely.
- **Affected chapters:** 8

### immutability (string) -> неизменяемость

Extends the int/float immutability entries from the Batch A register to strings. The course gives a correct mechanical explanation (word[0] = 'B' raises TypeError; the fix is to build a new string via concatenation) and correctly frames it as a deliberate language design choice rather than a limitation, with an explicit forward pointer to mutable lists in a later chapter.

- **Evidence:** scripts/build_chapter_08.py:08-15-neizmenyaemost
- **First-use guidance:** Pair every immutability claim with the concrete TypeError a learner will actually see, as the course does, rather than stating the rule abstractly.
- **Affected chapters:** 8

### membership (in / not in) -> in / not in (left as code, described with the verb 'содержит' / 'входит')

The course consistently prefers operational, verb-based Russian ('X содержит Y', 'Y входит в X') over the abstract noun 'принадлежность', which would read as an unnecessary calque-flavored formalism at this level. This is a correct, deliberate register choice, not an omission.

- **Evidence:** scripts/build_chapter_08.py:08-05-istina-lozh ('Оператор in проверяет, содержится ли одна строка внутри другой'); 08-22-mini-proekt-parol-i-email
- **First-use guidance:** Keep using verb phrasing for membership checks through at least Chapter 10; introduce 'принадлежность' as a noun only if a later chapter's register specifically calls for formal set-theory language.
- **Affected chapters:** 8

### index -> индекс

Standard term, used correctly and consistently for both positive (0-based) and negative (-1-based, from the end) string indexing, with diagrams.

- **Evidence:** scripts/build_chapter_08.py:08-03-indeksy-srezy
- **First-use guidance:** None needed.
- **Affected chapters:** 8

### slice -> срез

Standard, correct term for [start:stop:step] notation; the course's slice diagrams and all worked slice examples (word[:3], word[-3:], word[::2], word[::-1]) verified correct by direct execution.

- **Evidence:** scripts/build_chapter_08.py:08-14-srezy-stroki
- **First-use guidance:** None needed beyond the existing diagrams.
- **Affected chapters:** 8

### sequence (string as a sequence of characters) -> последовательность (символов)

Correct, standard framing of a string as an ordered sequence of characters, used to motivate indexing/slicing/iteration together as one coherent idea rather than three unrelated features.

- **Evidence:** scripts/build_chapter_08.py:08-01-stroki ('строка — это последовательность символов')
- **First-use guidance:** Introduce at the very first mention of what a string 'is', before indexing -- as the course does.
- **Affected chapters:** 8

### escape sequence -> экранирование

Standard Russian developer term for backslash escapes; correctly paired with repr() as the tool for seeing escape sequences 'as written in code' rather than their rendered effect.

- **Evidence:** scripts/build_chapter_08.py:08-11-ekranirovanie
- **First-use guidance:** Introduce repr() in the same breath as escaping, as the course does -- the two ideas reinforce each other.
- **Affected chapters:** 8

### raw string -> raw-строка

The course correctly keeps 'raw' untranslated as a hybrid English-Russian compound, which matches real developer usage, and correctly demonstrates raw strings solving the Windows-path backslash-escaping problem with a direct equality check.

- **Evidence:** scripts/build_chapter_08.py:08-12-mnogostrochnye-i-raw-stroki
- **First-use guidance:** None needed.
- **Affected chapters:** 8

### f-string -> f-строка

'f-строка' is the universal term Russian-speaking Python developers use; the course correctly presents it as the modern preferred choice after showing %-formatting and .format() as historical context, and all f-string format-spec examples (:.2f, :,  :.1%, alignment) verified correct by execution.

- **Evidence:** scripts/build_chapter_08.py:08-06-formatirovanie-strok
- **First-use guidance:** None needed.
- **Affected chapters:** 8

### equality vs identity (== vs is) -> == сравнивает значение, is сравнивает объект (descriptive phrasing, not the noun 'идентичность')

The course draws the == vs is line precisely and correctly for strings, explicitly defers full treatment of `is` to Chapter 14, and avoids introducing identity-related jargon before it is needed. This matches this register's general policy of not front-loading vocabulary a learner cannot yet ground in taught concepts.

- **Evidence:** scripts/build_chapter_08.py:08-05-istina-lozh (callout '== сравнивает значение, is сравнивает объект')
- **First-use guidance:** When Chapter 14 formally introduces `is`, this register should gain a dedicated 'identity / идентичность' entry; until then keep using the descriptive phrasing established here.
- **Affected chapters:** 8

### heading (turtle graphics) -> курс

The course correctly picks the navigation/aviation sense of 'курс' (heading, as in a ship's or aircraft's course) rather than the false-friend calque 'заголовок'. This is the single highest-value terminology decision in the Turtle graphics chapters (6-7), and it is made correctly and used consistently across dozens of examples and diagrams.

- **Evidence:** scripts/build_chapter_06.py:06-10-napravlenie-i-ugol; scripts/build_chapter_07.py (circle()/clone() sections referencing heading throughout)
- **First-use guidance:** Always pair 'курс' with a concrete degree value and a compass-style diagram on first use per chapter, as the course does, since the term alone is somewhat abstract for a beginner.
- **Affected chapters:** 6, 7

### seed (random module) -> seed (left as code; described with 'воспроизводимость')

The course correctly leaves 'seed' untranslated as a bare code-level term and builds the surrounding explanation around 'воспроизводимость' (reproducibility) as the Russian concept being taught. All seeded-random examples used by the automated graders (random.seed(1)->randint(1,10)==3, seed(3)->sample(range(1,6),k=3)==[2,5,4], seed(5)->randint(1,100)==80) were independently re-verified against the actual Python 3.14 random module and are correct.

- **Evidence:** scripts/build_chapter_05.py:05-20-seed
- **First-use guidance:** None needed -- 'seed' should stay bare/untranslated throughout the course.
- **Affected chapters:** 5

### condition -> условие

Standard, precise term for the True/False-producing expression in if/while; the course correctly and repeatedly distinguishes 'condition is False' (a normal, successful outcome) from 'the program failed' -- an important distinction stated explicitly, not left implicit.

- **Evidence:** scripts/build_chapter_09.py:09-02-sravnenie-i-reshenie (callout 'False -- тоже правильный ответ')
- **First-use guidance:** Pair every new conditional construct with a reminder that a False condition is a normal outcome, not an error, as the course does at first introduction.
- **Affected chapters:** 9

### branching -> ветвление

Standard term for the second of the three fundamental algorithm structures (sequence, branching, repetition); the course correctly introduces it at the algorithm/flowchart level, before any if syntax, so the concept is grounded before the keyword.

- **Evidence:** scripts/build_chapter_09.py:09-08-tri-struktury-i-vetvlenie
- **First-use guidance:** Introduce at the flowchart/algorithm level before syntax, as the course does, rather than defining it as 'what if does'.
- **Affected chapters:** 9

### truthiness (general rule, all types) -> истинность

Extends and fulfills the promise made in the Batch B register's string-scoped [[truthiness]] entry ('when truthiness is introduced for a new type... cross-reference rather than re-generalize prematurely'). Chapter 9 correctly generalizes from Chapter 8's string-only rule to the full falsy/truthy table (0, None, empty collections vs. everything else), explicitly repeating the same 'bool("False") is True' caution rather than silently dropping it.

- **Evidence:** scripts/build_chapter_09.py:09-11-truthiness-i-none
- **First-use guidance:** When truthiness is extended again for a not-yet-covered type (e.g. custom objects, in a later OOP chapter), follow the same pattern: state the rule, then explicitly reconcile it with the general table established here.
- **Affected chapters:** 9

### short-circuit evaluation -> short-circuit (короткое замыкание)

The course correctly glosses the English term with a literal Russian translation ('короткое замыкание') on first use, matching how a working Russian-speaking Python developer would name it, then uses 'short-circuit' bare afterward.

- **Evidence:** scripts/build_chapter_09.py:09-17-short-circuit
- **First-use guidance:** Gloss once at first use, then use bare, matching the course's own pattern for other English-technical-term-with-established-RU-gloss cases (cf. [[interpreter]]-era terms).
- **Affected chapters:** 9

### control flow -> поток управления

Standard, correct Russian rendering; the course explicitly flags its own explanation as a simplified model rather than an implementation claim, an honest and appropriate scoping choice.

- **Evidence:** scripts/build_chapter_09.py:09-13-neskolko-if-protiv-elif
- **First-use guidance:** Keep the 'simplified model' disclaimer when this term is revisited with more precision in a later chapter on generators/coroutines.
- **Affected chapters:** 9

### loop vocabulary (loop/body/iteration/counter/accumulator) -> цикл / тело цикла / итерация / счётчик / накопитель

The course introduces this five-term vocabulary set together, upfront, before writing a single loop, and then uses every term precisely and consistently for the rest of the chapter -- a well-designed terminology foundation rather than ad hoc naming.

- **Evidence:** scripts/build_chapter_10.py:10-01-cikly-for (vocabulary table); 10-10-enumerate-i-nakoplenie (counter vs accumulator distinction)
- **First-use guidance:** Introduce all five terms together as a set before the first loop example, as the course does, rather than defining them piecemeal as they happen to become relevant.
- **Affected chapters:** 10

### sentinel value -> сентинел

The course correctly transliterates rather than translates this term, matching real developer usage, and gives it a precise operational definition (a value that signals 'no more data' rather than being real data itself) rather than assuming it's already known.

- **Evidence:** scripts/build_chapter_10.py:10-11-poisk-filtr-summa (сентинел-цикл section)
- **First-use guidance:** Always pair with a concrete worked example (e.g. summing numbers until 'stop' is entered) rather than defining it abstractly, as the course does.
- **Affected chapters:** 10

### off-by-one error -> off-by-one (ошибка на единицу)

The course correctly identifies this as a named, recognized bug category (not just 'a mistake'), first introduced for condition boundaries in Chapter 9 and explicitly reused, not re-derived, for loop ranges in Chapter 10 -- good cross-chapter terminology consistency.

- **Evidence:** scripts/build_chapter_09.py:09-21-proektirovanie-uslovij; scripts/build_chapter_10.py:10-13-otladka-ciklov (dedicated deep-dive section)
- **First-use guidance:** Once introduced, treat as a known, reusable vocabulary item across any future boundary/range discussion rather than re-explaining it each time, as the course does.
- **Affected chapters:** 9, 10

### mutability (list vs tuple) -> изменяемость / неизменяемость

Extends the Batch B register's string-immutability entry to list (mutable) and tuple (immutable, like str). The course gives a precise, explicit callout that mutability is type-level, not value-level -- a genuinely important clarification since a beginner might otherwise wonder whether a 'simple' list could be immutable.

- **Evidence:** scripts/build_chapter_11.py:11-12-izmenyaem-spisok (callout 'Изменяемость -- свойство типа, а не конкретного значения')
- **First-use guidance:** Pair every mutability claim with a concrete demonstration (index assignment succeeding for list, TypeError for str/tuple), as the course does, rather than stating the rule abstractly.
- **Affected chapters:** 11

### aliasing -> aliasing (совместная ссылка)

The course gives an unusually precise and correct explanation: 'b = a' does not copy data, it makes a second name point to the same object -- directly extends Chapter 3's name/object model to the specific, consequential case of mutable objects with two names.

- **Evidence:** scripts/build_chapter_11.py:11-16-ssylki-aliasing
- **First-use guidance:** Always use a converge-diagram (two names, one object) rather than prose alone when introducing aliasing, as the course does -- the visual is more convincing than the sentence.
- **Affected chapters:** 11

### shallow copy -> поверхностная копия

Standard, correct Russian rendering; the course demonstrates the shallow-copy nested-list trap with a verified, real failing example before presenting copy.deepcopy() as the targeted fix, rather than asserting the distinction abstractly.

- **Evidence:** scripts/build_chapter_11.py:11-17-kopirovanie-spiskov
- **First-use guidance:** Pair with a concrete before/after diagram showing the outer list is duplicated but inner lists are shared, as the course does.
- **Affected chapters:** 11

### hashability -> хешируемость

Standard, correct term, introduced with a genuinely useful operational definition (why list can't be a set element or dict key) at exactly the right level of depth for this course stage, with a clear hashable/non-hashable capability-map reference.

- **Evidence:** scripts/build_chapter_11.py:11-19-mnozhestva-operacii
- **First-use guidance:** Keep the explanation operational (what breaks and why) rather than implementation-level, as the course does, until a later chapter on custom __hash__ methods if one exists.
- **Affected chapters:** 11

### comprehension (list/set/dict) -> comprehension (генератор списков / словаря / множества)

The course's 'loop first, shortcut second' sequencing is applied consistently across list, set, and dict comprehensions, and is explicitly and correctly scoped ('not a universal replacement for loops with side effects') rather than presented as strictly superior.

- **Evidence:** scripts/build_chapter_11.py:11-04-eshche-o-spiskah (preview); 11-22-preobrazovaniya-i-comprehensions (full treatment)
- **First-use guidance:** Always show the equivalent explicit loop first, as the course does, before introducing comprehension syntax for a new collection type.
- **Affected chapters:** 11

### decomposition -> декомпозиция

Standard, correct term for breaking a large task into small, testable steps; the course introduces it with a genuinely worked example (breaking 'build a guessing game' into 8 concrete steps) rather than defining it purely abstractly.

- **Evidence:** scripts/build_chapter_12.py:12-07-chto-takoe-proekt
- **First-use guidance:** Pair with a concrete worked decomposition example, as the course does, rather than a bare definition.
- **Affected chapters:** 12

### refactoring -> рефакторинг

Standard, correct developer term, introduced with the course's single clearest and most important architectural lesson (representing quiz questions as data rather than hardcoded logic) as the motivating example -- genuinely well-chosen, not an arbitrary illustration.

- **Evidence:** scripts/build_chapter_12.py:12-16-viktorina (explicitly labeled 'самый важный архитектурный урок главы')
- **First-use guidance:** Always demonstrate BEFORE/AFTER code producing identical behavior when introducing refactoring, as the course does, to make the 'behavior unchanged' part of the definition concrete rather than asserted.
- **Affected chapters:** 12

### parameter vs argument -> параметр (в определении) / аргумент (в вызове)

build_chapter_13.py §13.4 explicitly teaches the distinction with a comparison table ('Параметр -- в определении... Аргумент -- в вызове...') and a converge_diagram showing the argument value flowing into the parameter name. Verified the course maintains this precise usage throughout Chapter 13 rather than using the terms interchangeably, which is the single most common terminology slip in Russian-language beginner material on functions.

- **Evidence:** scripts/build_chapter_13.py:13-02-zachem-funkcii
- **First-use guidance:** Introduce both terms together with the definition/call-site contrast, exactly as the course does -- never introduce one without immediately contrasting it with the other.
- **Affected chapters:** 13

### LEGB (scope resolution order) -> LEGB (left as the English acronym; each letter explained in Russian)

build_chapter_13.py §13.12 introduces LEGB as a bare acronym via an elif_ladder_diagram (L -> E -> G -> B, each with a one-line Russian gloss), then walks through UnboundLocalError as a direct consequence of the model. Verified the course never attempts a Russian translation of the acronym itself -- correct, since 'LEGB' is the term a Russian-speaking developer would encounter in documentation, Stack Overflow, and job interviews.

- **Evidence:** scripts/build_chapter_13.py:13-05-globalnye-lokalnye
- **First-use guidance:** Keep 'LEGB' as a bare acronym; explain each letter in Russian but never replace the acronym itself.
- **Affected chapters:** 13

### closure -> замыкание

build_chapter_13.py §13.13 uses 'замыкание' correctly and consistently for the nested-function-retains-enclosing-state concept (make_greeter/greet_anna example), explicitly flagging it as a term to recognize now with full treatment deferred to decorators later. 'Замыкание' is the standard, unambiguous Russian term used in Russian-language Python documentation and courses -- verified no confusion with the unrelated literal sense of 'closing'.

- **Evidence:** scripts/build_chapter_13.py:13-16-vlozhennye-funkcii-nonlocal
- **First-use guidance:** Introduce 'замыкание' at first mention of a nested function outliving its enclosing call; note explicitly that full treatment (decorators) comes later, exactly as the course already does.
- **Affected chapters:** 13

### keyword-only / positional-only parameters -> параметры только по имени (keyword-only) / только по позиции (positional-only)

build_chapter_13.py §13.9 teaches the bare-* and bare-/ syntax with a three-zone capability_map ('только позиционно' / 'позиционно ИЛИ по имени' / 'только по имени'). Verified the course keeps the English technical names present alongside the Russian description rather than replacing them outright, which matters because these exact English terms appear in Python's own error messages and PEP 570 documentation.

- **Evidence:** scripts/build_chapter_13.py:13-14-positional-only-keyword-only
- **First-use guidance:** Always pair the Russian descriptive phrase with the English term in parentheses on first use, since the English term is what appears in real tracebacks and docs.
- **Affected chapters:** 13

### pure function vs side effect -> чистая функция / побочный эффект

build_chapter_13.py §13.11 defines both terms precisely (побочный эффект = функция меняет что-то ВНЕ своего возвращаемого результата; чистая функция = результат зависит только от аргументов) and explicitly frames both as legitimate function roles rather than one being universally superior. Verified this framing avoids the common overcorrection of presenting side effects as always-bad.

- **Evidence:** scripts/build_chapter_13.py:13-15-funkcii-vhod-vyhod
- **First-use guidance:** Introduce 'побочный эффект' before 'чистая функция' (effect first, then its absence), matching the course's own sequencing, and explicitly state both are legitimate.
- **Affected chapters:** 13

### self (not a keyword) -> self (left as code; explicitly described as convention, not a reserved word)

build_chapter_13.py §14.3 and §14.5 both explicitly call out 'self -- это не ключевое слово' (self is not a keyword) -- a callout box states it works even with a different parameter name but that using anything else would confuse every other Python reader. Verified this is factually correct (self is convention, not syntax) and the course states it twice for emphasis without contradiction.

- **Evidence:** scripts/build_chapter_14.py:14-05-self-i-svyazyvanie-metodov
- **First-use guidance:** State explicitly on first use that self is a naming convention, not a language keyword -- this is a common beginner misconception worth pre-empting.
- **Affected chapters:** 14

### encapsulation -> инкапсуляция

build_chapter_14.py §14.10 defines encapsulation precisely as hiding state behind methods that can validate new values, then correctly explains that _name and __name are conventions/name-mangling rather than language-enforced access control (schet._Konto__balans is shown working). Verified this avoids the widespread beginner-course error of claiming Python has 'private' attributes.

- **Evidence:** scripts/build_chapter_14.py:14-10-inkapsulyatsiya
- **First-use guidance:** Always pair 'инкапсуляция' with the explicit disclaimer that Python enforces this by convention (name mangling), not by language-level access control.
- **Affected chapters:** 14

### composition (HAS-A) vs inheritance (IS-A) -> композиция (HAS-A) / наследование (IS-A)

build_chapter_14.py §14.13 and §14.15 both use the HAS-A/IS-A test as the practical way to choose between the two relationships (Uchastnik HAS-A turtle.Turtle, Sobaka IS-A Zhivotnoe), reinforced by relationship_diagram calls with style='has-a'/'is-a'. Verified the course explicitly warns against using inheritance just to 'borrow' methods without a genuine IS-A relationship -- correct OOP design guidance.

- **Evidence:** scripts/build_chapter_14.py:14-13-kompozitsiya
- **First-use guidance:** Introduce the HAS-A/IS-A question as the practical test before naming which relationship (composition or inheritance) applies -- matches the course's own sequencing.
- **Affected chapters:** 14

### duck typing -> duck typing (left as the English term; described via the 'если это выглядит как утка...' idiom)

build_chapter_14.py §14.19 introduces the concept through the full English idiom and its literal Russian translation, then explicitly and correctly states 'полиморфизм не требует наследования' (polymorphism does not require inheritance) as the key misconception it corrects. Verified this term is genuinely bilingual in real Russian-language Python usage, so keeping both forms visible is the right call.

- **Evidence:** scripts/build_chapter_14.py:14-19-duck-typing
- **First-use guidance:** Present the idiom in both languages on first use; do not silently drop the English 'duck typing' after the initial introduction.
- **Affected chapters:** 14

### dunder / special methods -> специальные методы (дандер-методы as an accepted colloquial variant)

build_chapter_14.py §14.21 consistently uses 'специальные методы' as the primary Russian term and explains the double-underscore ('дандер', double underscore) etymology explicitly, never using 'магические методы'. Verified this is the more precise and increasingly standard choice in Russian-language Python material, since these methods follow a documented protocol rather than being 'magic'.

- **Evidence:** scripts/build_chapter_14.py:14-21-spetsialnye-metody
- **First-use guidance:** Use 'специальные методы' as the default; 'дандер-методы' may appear as a secondary colloquial gloss, but never 'магические методы'.
- **Affected chapters:** 14

### dataclass -> dataclass (left as code/the decorator name; described as 'класс-данные' or 'класс для хранения данных')

build_chapter_14.py §14.23 explicitly names and corrects two beginner misconceptions in one callout: '"dataclass -- это не настоящий класс" или "в dataclass нельзя писать методы" -- Оба неверны' (both are wrong). Verified @dataclass is accurately described as an ordinary class decorator that only adds generated __init__/__repr__/__eq__, with methods and properties working exactly as in any other class.

- **Evidence:** scripts/build_chapter_14.py:14-23-dataclasses
- **First-use guidance:** Keep '@dataclass'/'dataclass' as code, glossed as 'класс-данные'; explicitly state it remains a normal class on first use.
- **Affected chapters:** 14

### serialization / deserialization -> сериализация / десериализация

build_chapter_15.py §15.24 defines both terms precisely in a dedicated callout ('Сериализация -- превращение структуры Python... в представление, которое можно сохранить или передать... Десериализация -- восстановление структуры данных обратно') before the JSON/CSV sections that use the concept repeatedly. Verified both Russian terms are the standard, unambiguous ones used throughout Russian-language software engineering material.

- **Evidence:** scripts/build_chapter_15.py:15-24-kak-vybrat-format
- **First-use guidance:** Introduce both terms together, before the first concrete format (JSON), exactly as the course does.
- **Affected chapters:** 15

### current working directory (CWD) -> текущая рабочая директория (CWD as an accepted bare acronym)

build_chapter_15.py §15.7 states the distinction as a callout ('CWD -- это НЕ "папка со скриптом"') and reinforces it with Debug Lab 2, showing a FileNotFoundError that results from confusing CWD with the script's own directory. Verified this is one of the most common real-world path bugs, and the course's terminology and worked example are both accurate.

- **Evidence:** scripts/build_chapter_15.py:15-07-tekushaya-rabochaya-directoriya
- **First-use guidance:** Introduce 'текущая рабочая директория' with its acronym CWD together, and immediately contrast it with 'папка со скриптом' to pre-empt the standard confusion.
- **Affected chapters:** 15

### event-driven programming -> событийно-ориентированное программирование

build_chapter_16.py §16.1 and §16.9-16.10 introduce 'событийно-ориентированное программирование' as the term for GUI control flow, contrasted directly against the sequential terminal model, with repeated explicit callouts that mainloop() is 'не "замирание", а цикл обработки событий' (not freezing, but an event-processing loop). Verified the term and its contrast with sequential execution are both accurate and consistently reinforced across the chapter's opening and closing sections.

- **Evidence:** scripts/build_chapter_16.py:16-09-ot-terminala-k-gui
- **First-use guidance:** Introduce the term by direct contrast with the terminal's sequential model (глава 1-15), not in isolation -- matches the course's own §16.9 structure.
- **Affected chapters:** 16

### widget -> виджет

build_chapter_16.py §16.2 and §16.11 define 'виджет' as any visible/interactive interface object and build a whole dedicated section around the widget tree (each widget has a parent/master except the root). Verified the course uses 'виджет' as a fully naturalized loanword throughout the chapter without ever reaching for a native-Russian paraphrase, matching real Russian-language Tkinter/GUI-framework usage.

- **Evidence:** scripts/build_chapter_16.py:16-02-metki-knopki-pack
- **First-use guidance:** Use 'виджет' from first mention without translation; the course's own definition ('любой видимый/интерактивный элемент интерфейса') can serve as the one-line gloss on first use.
- **Affected chapters:** 16

## Batch E additions (Chapters 17-20)

### event binding (bind()) -> привязка события

The chapter's central new mechanism, explicitly contrasted with command= (Ch. 16) as a distinct, more general way to react to events.

- **Evidence:** scripts/build_chapter_17.py (17-07, 17-09, 17-10)
- **First-use guidance:** Introduce paired with command= to make the contrast concrete.
- **Affected chapters:** 17

### input focus -> фокус ввода

Introduced in Ch. 17 and immediately load-bearing for focus_get()/focus_set() and keyboard-event handling.

- **Evidence:** scripts/build_chapter_17.py (17-11)
- **First-use guidance:** Gloss once at first use, then use bare.
- **Affected chapters:** 17

### source of truth -> источник истины

The chapter's most repeated architectural phrase, distinguishing the state model from what widgets display.

- **Evidence:** scripts/build_chapter_17.py (17-13, 17-18)
- **First-use guidance:** Introduce when separating GameState from widgets.
- **Affected chapters:** 17, 18

### canvas -> холст

Consistent for both the Tkinter widget and its drawing surface; never calqued.

- **Evidence:** scripts/build_chapter_18.py (18-02)
- **First-use guidance:** No gloss needed after first introduction.
- **Affected chapters:** 18

### canvas item / item id -> элемент Canvas / идентификатор элемента

Central to the chapter's mental model: Canvas stores retained items (not pixels), each with an integer id that is not a Python id().

- **Evidence:** scripts/build_chapter_18.py (18-08, 18-10)
- **First-use guidance:** Explicitly contrast with Python's own id() the first time it appears.
- **Affected chapters:** 18

### stacking order (z-order) -> порядок наложения

The chapter's Russian rendering for how later-created Canvas items render above earlier ones; z-order stays as the English equivalent, not the primary term.

- **Evidence:** scripts/build_chapter_18.py (18-20)
- **First-use guidance:** Introduce with tag_raise/tag_lower.
- **Affected chapters:** 18

### game tick -> игровой тик

One discrete step of game-state update, distinct from the game loop that repeats it.

- **Evidence:** scripts/build_chapter_19.py (19-12)
- **First-use guidance:** Introduce before the real timer-driven loop (19.13).
- **Affected chapters:** 19

### game loop -> игровой цикл

The event-driven repetition mechanism (screen.ontimer in Turtle, the frame loop in Pygame); used consistently across the two game-project chapters.

- **Evidence:** scripts/build_chapter_19.py (19-08, 19-13); scripts/build_chapter_20.py (20-02, 20-14)
- **First-use guidance:** Distinguish a busy/blocking loop (anti-pattern) from the real timer/frame-driven loop from first use.
- **Affected chapters:** 19, 20

### direction vector -> вектор направления

Represents movement as a (dx, dy) pair rather than four separate boolean flags; central to the grid/vector model.

- **Evidence:** scripts/build_chapter_19.py (19-11)
- **First-use guidance:** Introduce alongside the grid-as-coordinates model.
- **Affected chapters:** 19

### game state vs game status -> состояние игры (GameState) / статус игры (GameStatus)

The dataclass holding all mutable game data is distinct from the enum describing which phase the game is in; the chapter is careful to keep the two separate.

- **Evidence:** scripts/build_chapter_19.py (19-15, 19-27)
- **First-use guidance:** Name both terms together the first time GameState/GameStatus appear.
- **Affected chapters:** 19

### frame vs animation frame -> кадр (шаг игрового цикла) / кадр анимации

Pygame chapter deliberately distinguishes one iteration of the game loop from one frame of a sprite's animation sequence -- the one real terminology collision risk in this vocabulary, worth keeping apart.

- **Evidence:** scripts/build_chapter_20.py (20-14 vs 20-23)
- **First-use guidance:** Name the distinction explicitly the first time animation frames are introduced.
- **Affected chapters:** 20

### delta time (dt) -> delta time (dt)

Kept in Latin script with dt as the code identifier, matching real Russian Pygame-community practice; never translated in prose.

- **Evidence:** scripts/build_chapter_20.py (20-16)
- **First-use guidance:** Gloss once as 'время, прошедшее с прошлого кадра', then use dt bare.
- **Affected chapters:** 20

### sprite -> спрайт

Standard Russian gamedev term; the chapter uses it primarily as 'image object' rather than pygame.sprite.Sprite specifically -- worth noting both senses exist.

- **Evidence:** scripts/build_chapter_20.py (20-19, 20-23)
- **First-use guidance:** Note the general-image-object sense is what this course teaches, distinct from the pygame.sprite.Sprite class.
- **Affected chapters:** 20

### hitbox / AABB collision -> хитбокс / AABB (прямоугольники, выровненные по осям)

Established transliteration in Russian gamedev for the simplified collision rectangle; AABB kept as the acronym with a one-time gloss.

- **Evidence:** scripts/build_chapter_20.py (20-21)
- **First-use guidance:** Gloss AABB once on first use.
- **Affected chapters:** 20

### world vs screen coordinates -> мировые / экранные координаты

Distinguishes the game's logical coordinate space from actual pixel positions on screen; explicitly scoped as 'not needed for this book's projects' rather than left ambiguous.

- **Evidence:** scripts/build_chapter_20.py (20-18)
- **First-use guidance:** Introduce alongside Rect, note it is out of scope for the book's own projects.
- **Affected chapters:** 20
