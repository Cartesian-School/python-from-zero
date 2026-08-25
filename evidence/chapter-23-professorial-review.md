# Глава 23 — финальная профессорская проверка

Дата проверки: 2026-08-25

Ветка: `fix/chapter-23-final-professorial-audit`

Область: академическая точность, педагогическая последовательность, практика,
источники, SafeSort, сборка курса и полный визуальный проход главы 23.

## Итог

| Контрольная группа | Результат |
|---|---:|
| P0 — научная целостность | 4/4 исправлено |
| P1 — серьёзные педагогические дефекты | 12/12 исправлено |
| P2 — существенные улучшения преподавания | 10/10 рассмотрено и исправлено |
| P3 — редакционная полировка | 3/3 выполнено |
| Канонические страницы главы | 67 |
| Визуальная проверка desktop 1440×1000 | 67/67 |
| Визуальная проверка mobile 390×844 | 67/67 |
| Практики главы | 24: 18 SafeSort + 6 домашних |
| Полностью заполненные ответы в starter | 0 |
| Официальные источники | 59 |
| Git-заголовки с официальным знаком | 10/10 |
| Остаточные P0/P1 | 0/0 |

## Трассировка P0

| Audit ID | Находка | Исправление и файлы | Проверка |
|---|---|---|---|
| P0-01 | `pyproject.toml` ошибочно связывался с созданием import package. | В `scripts/build_chapter_23.py` и сгенерированной `23-05-pyproject-toml.html` разделены import package `src/safesort`, distribution/build project и установленная distribution; показаны src-layout и `pip install -e .`. | `scripts/validate_chapter23_outputs.py`; editable-install и import smoke test в CI; полный build. |
| P0-02 | Правильный digest большого файла выдавался за доказательство чтения блоками. | В уроке 23-26 разделены result test (black-box) и interaction/implementation contract. В `projects/python/safesort/tests/test_duplicates.py` введён простой `RecordingReader`, который наблюдает несколько ограниченных `read(size)`. | 85 тестов SafeSort; `scripts/validate_chapter23_outputs.py` проверяет оба вида доказательства. |
| P0-03 | Текст обещал добавление категории TOML, хотя реализация могла заменить всю карту; конфигурационный файл мог попасть в план. | `projects/python/safesort/src/safesort/config.py` реализует defaults + category-specific override; `scanner.py` исключает `safesort.toml`. Урок 23-22 описывает ту же семантику. | `tests/test_config.py`, `tests/test_scanner.py`, 85 тестов SafeSort; output validator. |
| P0-04 | Столкновение мячей могло восприниматься как общая формула 2D, а движение — как «пиксели за кадр». | Домашний проект D ограничен лобовым столкновением двух одинаковых масс на одной прямой; прямо указано, что это не общая 2D-модель. Объяснены `velocity`, `dt`, зависимость численной точности от шага и независимость скорости от FPS в пределах дискретизации. | `scripts/validate_chapter23_outputs.py`; desktop/mobile просмотр `23-hw-04-otskakivayushie-myachi.html`. |

## Трассировка P1

| Audit ID | Находка | Исправление и файлы | Проверка |
|---|---|---|---|
| P1-01 | Не хватало цельной модели commit graph, branch, HEAD, `origin/main`, fetch/pull/push. | Урок `23-git-10-working-tree-staging-commit.html` фундаментально расширен: граф коммитов, подвижная ссылка-ветка, HEAD, три различных состояния local main / origin/main / GitHub main и команды наблюдения. | P0-contract validator; desktop/mobile visual; проверка обязательных терминов и команд. |
| P1-02 | Git-страницы не имели требуемого официального брендинга. | Добавлены неизменённые assets из `https://git-scm.com/downloads/logos`; `scripts/site_lib.py` предоставляет reusable Git-heading helper; CSS задаёт 40×40 desktop и 31×31 mobile, mixed heading — 34×34/28×28. | 10/10 H1; `h1LogoFirst=true`; `scripts/validate_chapter23_outputs.py`; 134 визуальных снимка. |
| P1-03 | Локальные операции Git смешивались с объектами GitHub. | В 23-29 добавлены две дорожки: switch/edit/test/stage/commit выполняются локально; Issue, PR, review и merge принадлежат GitHub; граница показана на `git push`. | Output validator; visual review страницы 23-29. |
| P1-04 | Зелёные Checks могли восприниматься как замена review. | В 23-29 явно разделены автоматические Checks и инженерное human review с Comment / Approve / Request changes. | Output validator; desktop/mobile review. |
| P1-05 | Starter практики содержали или могли раскрывать полное решение. | `scripts/chapter23_practice_model.py`, `build_notebooks_ch23.py`, `build_chapter23_graders.py` и `build_practice_pages.py` задают структуру Example → Starter → Task → Tests → Hint → Solution; starter не содержит готового решения. | `scripts/validate_chapter23_practices.py`: 24/24, untouched starter fails, solution passes, prefilled=0. |
| P1-06 | Не было надёжного пути от попытки к полному решению. | Для всех 24 задач сохранены отдельные solution cells/sections, при этом решение не исполняется как starter. | Practice validator исполняет attempt и solution изолированно для каждого notebook. |
| P1-07 | Навигация практик не гарантировала монотонный порядок. | `build_practice_pages.py` строит prev/next из канонического manifest; все 24 практики главы индексированы последовательно. | `validate_practice_manifest.py`: 493 практики курса без gaps; chapter practice validator. |
| P1-08 | Локальные практики не имели воспроизводимой инструкции среды. | 10 задач, требующих filesystem/Tkinter/Pygame, явно помечены local-required и содержат команды установки/запуска; остальные 14 имеют browser graders. | Practice validator: 10 local-required, 14 graders, 24/24. |
| P1-09 | `frozen=True` мог ошибочно трактоваться как чистая функция или защита файловой системы. | 23-07 объясняет только запрет переназначения полей объекта и отдельно показывает, что побочные эффекты функции от этого не исчезают. | Output validator; visual review 23-07. |
| P1-10 | Объяснение logging не связывало имя logger с formatter. | 23-21 разделяет пользовательский output и диагностику; `getLogger(__name__)` связывается с `LogRecord.name`, а `%(name)s` делает имя видимым. | Output validator; visual review 23-21. |
| P1-11 | Тесты появлялись слишком поздно, отдельно от feature development. | В каждой feature-странице введён test-checkpoint; в Части V проверки собраны как feature-level regression evidence. `capsys`, `tmp_path`, result/interaction tests объясняются на наблюдаемом поведении. | 157 course tests, 85 SafeSort tests, output validator. |
| P1-12 | Release-модель была неполной, а `gh` мог появиться без предпосылки. | 23-31 теперь проходит `python -m build` → wheel/sdist → чистый venv → install artifact → import/console smoke test → tag → отдельный GitHub Release. В основном learner flow PR создаётся через web UI; GitHub CLI только опционален с явной установкой/auth. | Dry-run editable install; SafeSort tests; output validator; CI workflow; desktop/mobile 23-29/23-31. |

## Трассировка P2

| Audit ID | Находка | Исправление и файлы | Проверка |
|---|---|---|---|
| P2-01 | Kelvin записывался с градусом и без физической границы. | 23-hw-05 использует `K`, не `°K`, объясняет абсолютный ноль и отклоняет значения ниже него. | Output validator; BIPM source; visual review. |
| P2-02 | Формулировки о SHA-256 были сильнее научного доказательства. | 23-18 объясняет many-to-one, collision possibility, avalanche effect и то, что совпавший digest — фильтр, а не доказательство равенства. | NIST FIPS 180-4; output validator. |
| P2-03 | Группировка только по digest могла объединить коллизию. | `duplicates.py` после size+digest выполняет побайтовое подтверждение и строит независимые exact groups, включая пустые файлы. | `test_duplicates.py`; 85 тестов; output validator. |
| P2-04 | Упрощения Git скрывали staging snapshot, remote-tracking и различие tag/Release. | Исправлены 23-git-10, 23-28, 23-31 и связанные диаграммы/таблицы. | Output validator; Git model gates; visual review. |
| P2-05 | Issue IDs и practice IDs могли выглядеть одной нумерацией. | Issue/checkpoint карточки явно маркируются как GitHub Project evidence, практики — как отдельная последовательность 23-01…23-24. | Practice manifest validator; visual review. |
| P2-06 | Модель RPS через один winner value не расширялась до пяти ходов. | Домашний проект C учит `dict[str, set[str]]`, проверку membership и полный набор 25 пар. | Output validator; notebook solution execution. |
| P2-07 | Advanced GitHub Projects перегружал ученика до первого feature cycle. | Базовая последовательность доведена до Issue → branch → PR раньше; copy, archive, templates, Insights и детали automation перенесены после цикла и помечены необязательными. | Канонический порядок 67 страниц; link/full-build validation; visual review. |
| P2-08 | Источники были сконцентрированы на Git/GitHub. | `data/chapter-23-official-sources.json` расширен Python, packaging, testing, NIST, SemVer и BIPM источниками; `build_chapter23_source_manifest.py` формирует точное отображение на страницы. | `validate_chapter23_sources.py`: 59/59, exact manifest/source match. |
| P2-09 | Число и индекс практик были неоднозначны. | Глава и manifest фиксируют ровно 24: 18 SafeSort и 6 домашних; index/navigation строятся из одной модели. | Practice validator и manifest validator. |
| P2-10 | Слова «меняет/не меняет» не различали объекты, disk state и interface output. | Уточнены boundaries read-only/mutating для `scan`, `plan`, `duplicates`, `apply`, `undo`; mutation wording проверяется контрактами. | Output validator; 85 SafeSort tests; visual review. |

## Трассировка P3

| Audit ID | Находка | Исправление и файлы | Проверка |
|---|---|---|---|
| P3-01 | Русский текст звучал машинно и местами был перегружен длинными тире. | После содержательных правок выполнены два отдельных Humanizer-прохода по learner-facing prose без изменения команд, формул, URL, цитат и технических терминов. | Повторная source/output validation и полный visual review. |
| P3-02 | Этапы проекта повторялись без устойчивой системы ориентации. | Единый stage tracker показывает 6 частей и текущий этап на проектных страницах; итоговая timeline связывает требования, Git/GitHub, реализацию, тесты и release. | Output validator; visual review index/23-32. |
| P3-03 | Generated output, CI и визуальные доказательства могли расходиться с source of truth. | Builders/validators сделаны каноническими, добавлен `.github/workflows/course-site-validation.yml`; `build_vercel.sh` последовательно выбирает `PYTHON_BIN`, локальную `.venv` или системный `python3`; проверена детерминированность всех 2606 tracked+untracked generated files и выполнен полный browser pass. Vercel структурно проверяет 24 практики и исполняет 14 browser-compatible, а CI в подготовленной среде исполняет все 24, включая 10 local-required. | Два build-прохода дали идентичные SHA-256; full и portable варианты `bash scripts/build_vercel.sh`; `git diff --check`; 67+67 screenshots. |

## Git branding и provenance

Официальный источник: `https://git-scm.com/downloads/logos`.

| Asset | SHA-256 |
|---|---|
| `site/assets/brand/git/mark-black.svg` | `0bf58ad2b4a330d0023d65ffbf056f5d93abee6b29eca81904951b014b3c9cd9` |
| `site/assets/brand/git/mark-white.svg` | `4b62d3bdfe913e88de9bd9d25cf466af9d4ac759dfecc8a17d86016b35b97a6e` |
| `site/assets/brand/git/lockup-black.svg` | `bc76df3f745738484b172beb0b4fcf770de0603fde451487dafa2b45f76371ce` |
| `site/assets/brand/git/lockup-white.svg` | `4b92d8fe6d9d7fa010a2cb526cb61bc9c7083678f7e9ffb5065d8b899817687f` |

Assets не recolored, не перерисованы, не помещены в Cartesian icon sprite и
рендерятся с сохранением aspect ratio. На mixed Git/GitHub странице марки
разделены и не создают видимость единого бренда.

## Источники

| Категория | Количество |
|---|---:|
| Git/GitHub | 41 |
| Python/Packaging | 13 |
| Testing | 2 |
| Cryptography | 1 |
| Versioning | 1 |
| Metrology | 1 |
| Physics | 0 |
| **Всего** | **59** |

Physics=0 является осознанным результатом условия аудита: первичный physics
source требовался только при преподавании общей 2D-формулы. Глава её не
преподаёт и прямо ограничивает упражнение лобовым столкновением одинаковых
масс; приписывать этому примеру общую 2D-модель запрещено.

## Визуальная методология и результат

Собранный текущий `dist/` отдавался локальным HTTP server на порту 8876.
Google Chrome запускался через Playwright driver с двумя viewport:
1440×1000 и 390×844. Для каждой из 67 канонических страниц выполнялись
полная прокрутка lazy images, DOM-preflight и full-page PNG. Каждый полный
PNG разбивался на вертикальные фрагменты и был просмотрен вручную через
contact sheet; всего просмотрено 134/134 снимка.

Первый capture с порта 8765 был отвергнут до зачёта: порт обслуживал устаревший
временный `dist`, что было обнаружено по отсутствующим Git logos. Все 134
зачтённых снимка сделаны заново с текущего `/home/astra/Projects/Python_001/dist`.

Итог preflight:

- HTTP 200: 134/134;
- desktop: 67/67;
- mobile: 67/67;
- page-level horizontal overflow: 0;
- broken images после полной прокрутки: 0;
- Git H1 branding: 10/10 на каждой ширине;
- знак стоит первым дочерним элементом H1: 10/10;
- desktop Git mark: 40×40 px, mixed heading: 34×34 px;
- mobile Git mark: 31×31 px, mixed heading: 28×28 px;
- desktop full-page height: 1611…6099 px;
- mobile full-page height: 2194…8002 px.

Широкие многоузловые схемы используют локальный горизонтальный scroll
container. Это сохраняет размер подписей на mobile и не создаёт overflow
страницы.

## Верификация

| Gate | Доказательство |
|---|---|
| Python syntax | builders/validators успешно прошли `py_compile` |
| Course tests | 157 passed |
| SafeSort tests | 85 passed |
| Chapter practices | 24/24; 14 browser graders; 10 local-required; starter fails; solution passes |
| Practice manifest | 493 canonical practices, gaps=0 |
| SafeSort upstream sync | 19 locked files, 9 documented educational corrections, base `v0.1.0` / `fe610cf09392` |
| Chapter output | 67 pages; Git H1 10/10; P0 contracts PASS |
| Source validation | 59 sources; exact manifest/source match |
| Full site build | navigation 1134 pages, broken links/fragments=0; catalogs 24 chapters / 493 practices / 13 projects; SEO 1134; sitemap 654 |
| Determinism | 2606 files byte-identical across two complete generator/build passes |
| Whitespace | `git diff --check` PASS |
| Course/site CI definition | checkout/setup Python 3.14, regeneration, tests, validators, full build, generated diff and whitespace gates |
| Vercel deployment gate | system Python без необъявленных third-party imports; структура 24/24, исполнение 14/14 browser-compatible; полный build PASS |

## Профессорский вывод

После главы ученик получает связную инженерную модель: требование становится
Issue, работа изолируется веткой, изменение подтверждается тестами, review и
CI, distribution собирается как wheel/sdist, artifact проверяется в чистой
среде, а tag и GitHub Release остаются разными объектами. Научные ограничения
SHA-256, Kelvin, `dt` и учебной collision model сформулированы явно.

Остаточных P0 и P1 нет. Глава 23 готова к публикации после зелёного внешнего
course/site CI на Pull Request.
