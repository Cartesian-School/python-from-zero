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

## EPUB и PDF

`scripts/build_epub.py` собирает `book/epub/python-s-nulya.epub` из уже готовых HTML-страниц
сайта: извлекает `<article>` (обычные страницы) или `.chapter-hero`+`.section-list`
(страницы-открывашки глав) через BeautifulSoup/lxml, убирает элементы навигации сайта и
ссылки на файлы вне EPUB-пакета (ноутбуки, исходники проектов — превращаются в обычный текст,
а не мёртвые ссылки), собирает сквозное оглавление. Проверено через `epubcheck`
(pip-пакет, оборачивает официальный Java-валидатор) — 0 ошибок.

`scripts/build_pdf.py` переиспользует то же извлечение контента из `build_epub.py`, но
склеивает всё в один HTML-документ с печатной типографикой (WeasyPrint) — обложка, разрыв
страницы перед каждой главой, нумерация страниц. Все девять файлов шрифтов и их SHA-256
закреплены. После рендеринга скрипт находит первые физические страницы всех глав через
якоря WeasyPrint, проверяет финальное дерево PDF через pypdf и генерирует
`data/book-pagination.json` с 24 диапазонами, общим числом страниц, версиями рендера,
форматом и fingerprint входных данных. Этот generated-файл — единственный источник
физической пагинации для открывашек сайта и homepage; `manifest/coverage_manifest.json`
хранит только состояние покрытия учебного материала.

## Валидация

- `python -m compileall <path>` — синтаксическая проверка
- `ruff check` / `ruff format --check` — линтинг и форматирование
- `pytest tests/ -v` — `tests/test_projects.py` покрывает все 12 мини-проектов книги; каждый
  GUI-проект (Tkinter/Pygame/Turtle) запускается отдельным подпроцессом под `xvfb-run`, чтобы
  несколько модулей, создающих собственное окно/экран при импорте, не конфликтовали внутри
  одного процесса
- `python scripts/run_notebook.py <path.ipynb>` — выполнение ноутбука через nbclient «сверху вниз» (создаётся на следующем шаге)
- `python -m epubcheck book/epub/python-s-nulya.epub` — валидация EPUB по официальному стандарту
