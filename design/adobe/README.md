# Adobe-produced assets

## Обложка — концепт 1

- **Файл-источник:** `cover_concept_v1.html` (self-contained, авторство по правилам
  Adobe `create_visual_design_express_skill` — фиксированный canvas 6in×9in,
  `hz:slide-selector`/`hz:canvas-*` метаданные, инлайновые стили).
- **Инструменты Adobe, которые реально были вызваны:**
  - `get_account_type` → `auth` (полный аккаунт, не guest)
  - `create_visual_design_express_skill` → загружен playbook для авторства HTML-дизайна
  - `find_fonts` → проверены `Sora`, `Inter`, `JetBrains Mono` в библиотеке Adobe Fonts:
    все три отсутствуют (`not_found`/`not_entitled`) — по правилам skill (шаг 6,
    Font source fallback) переключились на Google Fonts `@import`, чтобы сохранить
    визуальную согласованность с типографикой, уже установленной в Figma-системе.
- **По решению Product Owner:** доставка как standalone PDF/PNG (не Adobe Express
  документ) — поэтому `html_export_readiness_skill` / `export_html_to_express` не
  вызывались (не требуются для этого пути).
- **Рендер:** `google-chrome --headless --print-to-pdf` / `--screenshot`
  → `../exports/cover_concept_v1.pdf` (553 KB, 1 страница, 6in×9in),
    `../exports/cover_concept_v1.png` (576×864, для быстрого просмотра).
- **Логотип:** использован подлинный ассет `сartesian_logo/logo.png` (встроен как
  base64), а не перерисован — согласно требованию мастер-промпта не подменять
  официальный логотип AI-имитацией.
- **Цвета:** те же токены, что и в Figma-системе (`navy/900 #0D0230`,
  `violet/500 #5B24F9`, `blue/500 #185DFA`) — извлечены из реальных ассетов
  (см. `../figma/state_ledger.json` → `sourcedColors`).

## Дальнейшие шаги (после апрува)

- Ещё 2–4 альтернативных концепта обложки (другая композиция/акцент).
- Печатный вариант с корешком и задней обложкой (полная разворотная обложка) —
  потребуется финальный подсчёт страниц PDF-книги для точной ширины корешка.
- Возможна векторизация иллюстративных элементов через `image_vectorize`, если
  потребуются дополнительные editorial-иллюстрации для глав.
