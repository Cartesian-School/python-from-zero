# Скрипты и окружение

## Виртуальное окружение

Python 3.14.6 установлен локально через `uv` (`~/.local/bin/python3.14`), т.к. в системе
не было ни `pip`, ни sudo-доступа для установки пакетов глобально.

```bash
uv python install 3.14        # уже выполнено, Python 3.14.6 в ~/.local/share/uv/python/
python3.14 -m venv .venv
source .venv/bin/activate
pip install nbformat nbclient ipykernel ebooklib ruff flask beautifulsoup4 lxml weasyprint pypdf epubcheck
```

Зарегистрированное ядро Jupyter: `cartesian-python314` ("Cartesian Python 3.14").

## Pygame на Python 3.14

На момент написания книги у пакета `pygame` ещё нет собранного wheel-пакета для
Python 3.14 (пробовали `pip install pygame` — падает при сборке из исходников:
`Unable to run "sdl-config"`). Вместо него используется **`pygame-ce`**
(Pygame Community Edition) — активно поддерживаемый форк с полностью совместимым
API (`import pygame` работает без изменений), у которого уже есть готовый wheel
для 3.14 (`pip install pygame-ce`). Проверено: `pygame-ce 2.5.8` инициализирует
дисплей и рисует под Xvfb без ошибок.

## Flask на Python 3.14

В отличие от `pygame`, `flask` (проверено: 3.1.3) устанавливается на Python 3.14 без каких-либо
проблем — готовый wheel есть у самого Flask и у всех его зависимостей (Werkzeug, Jinja2,
MarkupSafe, itsdangerous, click, blinker). Дополнительных мер (аналогичных `pygame-ce`) не
потребовалось.

## EPUB и PDF: единый канонический конвейер сборки книги

Начиная с M02-I06, публикация книги — это ОДИН язык-независимый,
формат-параметризованный конвейер (`scripts/book_pipeline/`), а не отдельные
RU/PL-реализации на формат. Обязывающая архитектура закреплена в
`docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md`. Канонический вызов:

```bash
python scripts/build_book.py --language ru --format pdf
python scripts/build_book.py --language ru --format epub
python scripts/build_book.py --language pl --format pdf
python scripts/build_book.py --language pl --format epub
python scripts/build_book.py --language ru --format all   # оба формата
python scripts/build_book.py --all                        # вся матрица + validate_book.py
```

Программный эквивалент — `book_pipeline.build_book(language=..., output_format=...)`.
`language` — только входной параметр (выбирает `BookLocaleConfig` из
`scripts/book_pipeline/locale_ru.py` / `locale_pl.py`: заголовки, права, локализованные
подписи TOC/copyright, пути вывода). `output_format` — только выходной параметр (выбирает
`pdf_adapter.build()` или `epub_adapter.build()`).

Конвейер: язык → `BookLocaleConfig` (`book_pipeline/locales.py`) → канонический
загрузчик контента `CanonicalBookLoader` (`book_pipeline/model.py`) — читает HTML-страницы
сайта РОВНО ОДИН РАЗ и извлекает их стабильный фрагмент (`<article>`,
`.chapter-hero`+`.section-list` или карточка проекта) через locale-agnostic функции
`scripts/book_shared.py` — → неизменяемый `CanonicalBookModel` (главы, front-matter,
проекты, предметный указатель) → формат-адаптер. PDF- и EPUB-адаптеры получают ОДНУ И ТУ ЖЕ
модель; ни один из них не хранит собственный список глав, переводы или порядок страниц.

`book_pipeline/pdf_adapter.py` склеивает модель в один HTML-документ с печатной
типографикой (WeasyPrint) — обложка, титул, copyright, оглавление с `target-counter`,
разрыв страницы перед каждой главой, колонтитулы. Все десять файлов шрифтов и их SHA-256
закреплены; отдельная Fontconfig-политика исключает системный Noto Color Emoji. После
рендеринга адаптер находит физические страницы глав через якоря WeasyPrint, проверяет
финальное дерево PDF через pypdf и пишет `<language>.pagination_output_path`
(`data/book-pagination.json` для RU, `data/book-pagination-pl.json` для PL) — 24
диапазона, общее число страниц, версии рендера, fingerprint входных данных. Этот
generated-файл — единственный источник физической пагинации для открывашек сайта и
homepage.

`book_pipeline/epub_adapter.py` пакует ту же модель в EPUB (EbookLib): метаданные, общий
`theory.css`/`project.css`, ассеты (всегда из RU `site/assets/` — у `site/pl/` своих
ассетов нет), сквозные spine/TOC/nav. Проверяется через `epubcheck` — 0 ошибок.

`scripts/build_epub.py`, `scripts/build_epub_pl.py`, `scripts/build_pdf.py`,
`scripts/build_pdf_pl.py` остались как тонкие обёртки обратной совместимости — каждая
вызывает `book_pipeline.build_book(...)` с фиксированными `language`/`output_format` и не
содержит собственной логики публикации.

## Валидация

- `python -m compileall <path>` — синтаксическая проверка
- `ruff check` / `ruff format --check` — линтинг и форматирование
- `pytest tests/ -v` — `tests/test_projects.py` покрывает все 12 мини-проектов книги; каждый
  GUI-проект (Tkinter/Pygame/Turtle) запускается отдельным подпроцессом под `xvfb-run`, чтобы
  несколько модулей, создающих собственное окно/экран при импорте, не конфликтовали внутри
  одного процесса
- `python scripts/run_notebook.py <path.ipynb>` — выполнение ноутбука через nbclient «сверху вниз» (создаётся на следующем шаге)
- `python -m epubcheck book/epub/python-s-nulya-ru.epub` — валидация EPUB по официальному стандарту (аналогично для `book/epub/python-od-zera-pl.epub`)
