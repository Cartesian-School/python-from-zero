# Расследование: JupyterLite Pyodide-ядро не регистрируется

Дата: 2026-08-15
Ветка: `feat/interactive-jupyter-practice`

## Итог

JupyterLite отклонён как рантайм выполнения практики. Причина — воспроизводимый,
подтверждённый баг регистрации Pyodide-ядра в `jupyterlite-pyodide-kernel`, не
зависящий от версии пакета и не связанный с окружением (браузер/Worker/WASM/сеть —
всё работает). Реализован собственный (first-party) раннер на чистом Pyodide.

## Симптом

На странице ноутбука (`/lab/index.html?path=...`) диалог «Select Kernel» и экран
Launcher показывают **только** `"No Kernel"` — ни один Python-кернел никогда не
появляется в списке, сколько бы времени ни прошло (проверено вплоть до 40+ секунд
ожидания). Панель Launcher не показывает категорию «Notebook» вообще.

## Протестированные комбинации версий

| jupyterlite-core | jupyterlite-pyodide-kernel | Результат |
|---|---|---|
| 0.8.1 | 0.8.3 ("latest" на момент теста) | FAIL |
| 0.6.2 | 0.6.1 (давно стабильная линия) | FAIL |
| 0.8.1 | 0.8.2 (официально совместимая пара по матрице совместимости: `jupyterlite-pyodide-kernel 0.8.* → jupyterlite-core >=0.8,<0.9 → Pyodide 314.* → Python 3.14.*`) | FAIL |
| 0.8.0 | 0.8.0 (согласованный fallback) | FAIL |

Все пять комбинаций дали идентичный симптом: `<select>` кернела содержит ровно один
`<option>` — `"No Kernel"` (проверено прямым запросом `document.querySelectorAll('select')`
через DOM, а не только по accessibility-дереву).

## Исключённые причины (систематически проверено и отвергнуто)

- **Кеш браузера / Service Worker** — воспроизведено на полностью новых origin
  (разные порты 8899–8911, никогда ранее не посещавшиеся), с явной очисткой
  `serviceWorker.getRegistrations()`, `indexedDB.databases()`, `caches.keys()`,
  `localStorage`/`sessionStorage` перед тестом.
- **Конфликт с `jupyter-iframe-commands`** — воспроизведено в сборке, из которой
  это расширение было полностью удалено (`pip uninstall jupyter-iframe-commands`).
- **Заголовки COOP/COEP** — протестировано и с заголовками
  (`Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Embedder-Policy:
  require-corp`, `crossOriginIsolated === true` подтверждён) и без них
  (`crossOriginIsolated === false`) — идентичный результат в обоих случаях.
- **Недостающие опциональные зависимости** — установлены `jupyter_server`,
  `jupyterlab_server`, `libarchive-c`; результат не изменился.
- **Возможности окружения браузера** — явно проверено и подтверждено рабочим:
  `typeof Worker !== 'undefined'`, `typeof WebAssembly !== 'undefined'`,
  `typeof SharedArrayBuffer !== 'undefined'` — все `true`.
- **Доступность сети/CDN** — `fetch()` к `cdn.jsdelivr.net/pyodide/v314.0.4/full/
  pyodide-lock.json` и `.../pyodide.mjs` **напрямую из вкладки браузера** возвращают
  `200 OK` с корректным содержимым.
- **Сам Pyodide в этом окружении** — прямой тест: создан обычный `Worker` с
  `import { loadPyodide } from 'https://cdn.jsdelivr.net/pyodide/v314.0.4/full/pyodide.mjs'`,
  вызван `await loadPyodide()` — успешно вернул `pyodide.version === "314.0.4"`.
  **Это ключевое доказательство: Pyodide 314.x/Python 3.14 полностью работоспособен
  в данном браузере/окружении — проблема исключительно в слое регистрации кернела
  JupyterLite.**

## Найденная техническая причина

Через прямую интроспекцию Module Federation контейнера (`window._JUPYTERLAB['@jupyterlite/pyodide-kernel-extension']`)
подтверждено, что:

1. Расширение **загружается** как JS-модуль корректно (без ошибок).
2. Плагин `@jupyterlite/pyodide-kernel-extension:kernel` (`autoStart: true`)
   требует единственный обязательный сервис-токен: `@jupyterlite/services:IKernelSpecs`.
3. Этот токен **никогда не резолвится** — Lumino/JupyterLab тихо пропускает
   активацию плагина, если обязательная зависимость недоступна, **без исключения
   и без записи в консоль** (это архитектурная особенность Lumino plugin system,
   не баг конкретно в моей сборке).
4. Как следствие: **ни разу не зафиксирован ни один сетевой запрос к какому-либо
   Pyodide CDN** (`cdn.jsdelivr.net/pyodide/...`) ни в одной из пяти протестированных
   сборок — код, который должен был бы инициировать этот запрос, никогда не
   достигается.
5. `jupyter lite status` во всех сборках показывает
   `status:jupyterlite-pyodide-kernel-pyodide:pyodide → URL: None` (этот конкретный
   индикатор сам по себе может быть некритичным — по независимому issue он также
   встречался в случаях с другой первопричиной, — но зафиксирован для полноты).

## Соответствие известной проблеме в апстриме

Симптом «полная тишина при сбое инициализации кернела» — задокументированная,
подтверждённая, открытая проблема в самом `jupyterlite-pyodide-kernel`:
[jupyterlite/pyodide-kernel#138 «Feedback on kernel start crash»](https://github.com/jupyterlite/pyodide-kernel/issues/138) —
цитата из issue: «often no indication as to what has happened and why the kernel
is not up and running» и «there is no try/catch around all kernel init code».

Дополнительный контекст: `jupyterlite-pyodide-kernel 0.8.3` был опубликован
2026-08-11 — за 4 дня до тестирования, то есть это очень свежий релиз, в котором
теоретически может быть ещё не выявленная регрессия. Однако баг воспроизведён
идентично и на связке 0.8.0/0.8.0, и на давно стабильной 0.6.x — то есть проблема
не специфична для одного релиза.

## Решение

По решению Product Owner: не переключаться на серверный Jupyter-бэкенд, не
понижать версию браузерного рантайма до Python 3.13 (эти опции были явно
отклонены). Вместо использования `jupyterlite-pyodide-kernel` реализован
собственный (first-party) раннер ноутбуков:

- прямая загрузка Pyodide 314.x в выделенном ES-module Web Worker
  (`site/assets/js/python-worker.mjs`);
- нотбуки `.ipynb` остаются каноническим форматом, парсятся напрямую как
  nbformat JSON на клиенте (без прохождения через JupyterLite/JupyterLab UI);
- собственный лёгкий рендерер ячеек (markdown + CodeMirror 6 для кода) в стиле
  дизайн-системы Cartesian School, без имитации интерфейса JupyterLab;
- структурированный протокол сообщений worker↔host с `requestId` вместо
  недокументированного/непрозрачного поведения `jupyterlite-pyodide-kernel`.

Это решение напрямую обосновано диагностикой выше: раз голый Pyodide 314.x
доказанно работает в этом окружении, а сбой изолирован именно в слое
JupyterLite/Lumino-регистрации кернела, — обход этого слоя полностью снимает
блокер, сохраняя все технические требования (Python 3.14, WebAssembly,
статический Vercel-деплой, отсутствие серверного бэкенда).

## Минимальное воспроизведение (для возможного будущего issue в апстрим)

```bash
pip install jupyterlite-core==0.8.1 jupyterlite-pyodide-kernel==0.8.2
mkdir -p content
cat > content/minimal.ipynb <<'EOF'
{
 "cells": [{"cell_type": "code", "execution_count": null, "id": "x",
            "metadata": {}, "outputs": [],
            "source": ["print(\"Cartesian School Python 3.14\")\n",
                       "import sys\n", "print(sys.version)"]}],
 "metadata": {}, "nbformat": 4, "nbformat_minor": 5
}
EOF
jupyter lite build --contents ./content --output-dir ./_output
cd _output && python3 -m http.server 8899   # обслуживать по HTTP, не file://
# открыть http://localhost:8899/lab/index.html?path=minimal.ipynb
# наблюдаемый результат: диалог "Select Kernel" содержит только "No Kernel"
```

Апстрим-issue пока не заведён (по решению Product Owner — приоритет отдан
доставке функциональности Cartesian School; это расследование сохранено как
готовая основа для будущего issue при необходимости).
