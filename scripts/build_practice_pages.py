#!/usr/bin/env python3
"""Строит интерактивные страницы практики (site/practice/<lesson-id>/index.html)
из manifest/practice_manifest.json — единого источника истины.

Каждая страница подключает site/assets/js/practice.bundle.js (наш собственный
Pyodide-раннер ноутбуков — не JupyterLite, см.
evidence/jupyterlite-kernel-investigation.md) и рендерит канонический .ipynb
прямо в браузере.
"""

import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_metadata import chapter_title as canonical_chapter_title
from site_lib import NAV_SCRIPT_TAG, mobile_nav_links, site_header

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"
OUT_DIR = ROOT / "site" / "practice"

CHAPTER_23_SAFESORT_LOCAL = {"23-09", "23-13", "23-16", "23-20", "23-21", "23-24"}
CHAPTER_23_HOMEWORK_LOCAL = {"23-01", "23-04", "23-05", "23-06"}


def practice_chapter_title(lesson_id: str) -> str:
    number = int(lesson_id.split("-", 1)[0])
    return f"Глава {number}: {canonical_chapter_title(number)}"


def build_page(lesson_id: str, entry: dict) -> str:
    notebook_url = f"/notebooks/{entry['notebook']}"
    download_name = entry["notebook"].split("/")[-1]
    chapter_title = html.escape(practice_chapter_title(lesson_id))
    lesson_title = html.escape(entry["lesson_title"])
    return_url = html.escape(entry["return_url"])
    next_url = html.escape(entry.get("next_url") or "")
    grader_url = html.escape(entry["grader"])

    # Lessons that use open()/pathlib run against Pyodide's own virtual
    # filesystem — real semantics (write/read/append all work), but files
    # live only in this browser tab, not on the learner's real computer.
    # Stated plainly so nobody mistakes it for local disk access.
    fs_notice = (
        """\n  <div class="practice-fs-notice">💾 Файлы в этой практике (например, """
        """<code class="inline">privet.txt</code>) создаются во """
        """<strong>временной файловой системе Python в браузере</strong> — не на """
        """вашем компьютере. Они существуют, пока открыта эта вкладка, и """
        """исчезают при нажатии «Сбросить среду».</div>"""
        if entry.get("filesystem_note")
        else ""
    )

    config_json = json.dumps(
        {
            "lessonId": lesson_id,
            "chapterTitle": practice_chapter_title(lesson_id),
            "lessonTitle": entry["lesson_title"],
            "notebookUrl": notebook_url,
            "graderUrl": entry["grader"],
            "downloadUrl": notebook_url,
            "returnUrl": entry["return_url"],
            "nextUrl": entry.get("next_url"),
            "assessment": entry.get("assessment", "automatic"),
            "workerUrl": "/assets/js/python-worker.mjs",
            "companionFiles": entry.get("companion_files"),
            "chapterDir": entry["notebook"].split("/")[0],
        },
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Практика {html.escape(lesson_id)} — {lesson_title} — Cartesian School</title>
<meta name="description" content="Интерактивная практика: {lesson_title}." />
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/theory.css" />
<link rel="stylesheet" href="/assets/css/practice.css" />
</head>
<body>

<header class="practice-header">
  <a class="brand" href="/index.html">
    <img src="/assets/img/logo.png" alt="Cartesian School" />
    <span class="brand-word">Cartesian<span class="school">School</span></span>
  </a>
  <div class="practice-titles">
    <div class="practice-chapter">{chapter_title}</div>
    <div class="practice-lesson">{lesson_title}</div>
  </div>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav-panel" aria-label="Меню"><span class="nav-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span></button>
</header>
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links("praktika")}
</nav>

<div class="practice-toolbar">
  <button id="run-all-btn" class="btn-primary">▶▶ Выполнить всё</button>
  <button id="check-btn">Проверить результат</button>
  <button id="reset-btn">Сбросить среду</button>
  <button id="finish-btn" class="btn-finish" disabled>Завершить практику и вернуться</button>
  <span id="status" class="practice-status">Запускается Python…</span>
  <span id="version-label" class="practice-version-label"></span>
</div>

<main class="practice-body">{fs_notice}
  <div id="notebook-mount"></div>
  <div id="result-panel" class="practice-result-panel"></div>
  <a class="practice-download" href="{notebook_url}" download="{html.escape(download_name)}">📄 Скачать оригинальный .ipynb (для VS Code / PyCharm / Jupyter)</a>
</main>

<script type="module">
  import {{ initPracticeApp }} from "/assets/js/practice.bundle.js";

  initPracticeApp({{
    ...{config_json},
    mountEl: document.getElementById("notebook-mount"),
    statusEl: document.getElementById("status"),
    runAllBtn: document.getElementById("run-all-btn"),
    checkBtn: document.getElementById("check-btn"),
    resetBtn: document.getElementById("reset-btn"),
    finishBtn: document.getElementById("finish-btn"),
    resultPanel: document.getElementById("result-panel"),
    versionLabel: document.getElementById("version-label"),
  }});
</script>

{NAV_SCRIPT_TAG}
</body>
</html>
"""


def _local_required_explanation(lesson_id: str, entry: dict) -> tuple[str, str, str]:
    """Returns (main_paragraph_html, vscode_tail, jupyter_tail) explaining why
    this specific lesson can't run in the browser. Uses entry["unavailable_module"]
    / entry["unavailable_kind"] ("window" or "server") when present for accurate,
    per-lesson wording (tkinter/turtle/Pygame open a window; Flask starts a
    server). Falls back to a generic, always-true sentence that names no
    specific module, rather than risk a false claim for entries that predate
    this field.
    """
    if lesson_id in CHAPTER_23_SAFESORT_LOCAL:
        main = (
            "Задание проверяет локальный checkout SafeSort, системные пути, Git или "
            "операции с локальной файловой системой. Браузерная среда не даёт тот же "
            "инженерный контекст. Выполните канонический ноутбук в отдельном окружении Python 3.14."
        )
        return main, "код выполнится в checkout SafeSort", "ядро будет использовать окружение SafeSort"
    if lesson_id in CHAPTER_23_HOMEWORK_LOCAL:
        main = (
            "Задание импортирует код дополнительного проекта из репозитория курса и может "
            "использовать локальную графическую или файловую подсистему. Выполните канонический "
            "ноутбук в отдельном окружении Python 3.14."
        )
        return main, "код выполнится в checkout курса", "ядро будет использовать окружение курса"

    module = entry.get("unavailable_module")
    kind = entry.get("unavailable_kind", "window")
    if not module:
        main = (
            "Эта практика использует функциональность, недоступную в текущей "
            "браузерной среде Python (Pyodide). Выполните это упражнение "
            "локально в Python 3.14."
        )
        return main, "на вашем компьютере", "как обычно"
    esc_module = html.escape(module)
    if kind == "server":
        main = (
            f'Эта практика использует <code class="inline">{esc_module}</code>, '
            "который запускает веб-сервер на вашем компьютере. Такой режим "
            "недоступен в текущей браузерной среде Python. Выполните это "
            "упражнение локально в Python 3.14."
        )
        return main, f"сервер {esc_module} запустится на вашем компьютере", f"сервер {esc_module} запустится как обычно"
    main = (
        f'Эта практика использует <code class="inline">{esc_module}</code>, '
        "который открывает нативное графическое окно Python. Такой режим "
        "недоступен в текущей браузерной среде Python. Выполните это "
        "упражнение локально в Python 3.14."
    )
    return main, f"окно {esc_module} откроется на вашем компьютере", f"окно {esc_module} откроется как обычно"


def _chapter_23_local_setup(lesson_id: str) -> str:
    """Return the exact reproducible setup shown in Chapter 23 notebooks."""
    if lesson_id in CHAPTER_23_SAFESORT_LOCAL:
        return """
  <div class="local-setup-contract">
    <h2>Воспроизводимое окружение SafeSort</h2>
    <pre><code>git clone https://github.com/Cartesian-School/safesort.git
cd safesort
python3.14 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
python -m pip install jupyter ipykernel
python -m ipykernel install --user --name safesort-py314 --display-name "SafeSort Python 3.14"
jupyter lab</code></pre>
    <p>Выберите kernel <strong>SafeSort Python 3.14</strong>. До работы запустите диагностику:</p>
    <pre><code>import sys
import safesort

print(sys.executable)
print(safesort.__file__)</code></pre>
    <p>Первый путь должен вести в <code class="inline">.venv</code>, второй в checkout <code class="inline">src/safesort</code>.</p>
  </div>"""
    if lesson_id in CHAPTER_23_HOMEWORK_LOCAL:
        return """
  <div class="local-setup-contract">
    <h2>Воспроизводимое окружение проектов курса</h2>
    <pre><code>git clone https://github.com/Cartesian-School/python-from-zero.git
cd python-from-zero
python3.14 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -U pip
python -m pip install pytest pygame-ce jupyter ipykernel
python -m ipykernel install --user --name course-py314 --display-name "Course Python 3.14"
jupyter lab</code></pre>
    <p>Выберите kernel <strong>Course Python 3.14</strong>. На Linux для Tkinter может понадобиться системный пакет <code class="inline">python3-tk</code>. Проверьте окружение:</p>
    <pre><code>import sys
from pathlib import Path

print(sys.executable)
print(Path.cwd())</code></pre>
  </div>"""
    return ""


def build_local_required_page(lesson_id: str, entry: dict) -> str:
    """Practice page for lessons whose canonical code cannot run in the
    browser (confirmed: Pyodide has no turtle or tkinter, and pygame's
    display.set_mode()/flask are similarly unavailable — see the Chapter
    6/7/20/22 rollout evidence). No Pyodide worker, no grader, no score: the
    learner runs the canonical .ipynb locally and may optionally
    self-declare completion, clearly marked as unverified.
    """
    notebook_url = f"/notebooks/{entry['notebook']}"
    download_name = entry["notebook"].split("/")[-1]
    chapter_title = html.escape(practice_chapter_title(lesson_id))
    lesson_title = html.escape(entry["lesson_title"])
    return_url = html.escape(entry["return_url"])
    next_url = html.escape(entry.get("next_url") or entry["return_url"])
    lesson_id_js = html.escape(lesson_id).replace('"', '\\"')
    explanation_html, vscode_tail, jupyter_tail = _local_required_explanation(lesson_id, entry)
    setup_html = _chapter_23_local_setup(lesson_id)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Практика {html.escape(lesson_id)} — {lesson_title} — Cartesian School</title>
<meta name="description" content="Локальная практика: {lesson_title}." />
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/theory.css" />
<link rel="stylesheet" href="/assets/css/practice.css" />
</head>
<body>

{site_header("praktika")}
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links("praktika")}
</nav>

<main class="practice-unsupported">
  <div class="practice-chapter">{chapter_title}</div>
  <div class="local-required-badge">Требуется локальный Python</div>
  <h1>{lesson_title}</h1>
  <p>{explanation_html}</p>

  <div class="actions">
    <a class="btn-primary" href="{notebook_url}" download="{html.escape(download_name)}">📄 Скачать .ipynb</a>
  </div>

{setup_html}

  <div class="local-instructions">
    <div class="instruction-card">
      <h3>VS Code</h3>
      <p>Установите расширения <strong>Python</strong> и <strong>Jupyter</strong> (Microsoft), откройте
      скачанный файл прямо в VS Code, выберите интерпретатор Python 3.14 и запускайте ячейки
      (<code class="inline">Shift+Enter</code>) — {vscode_tail}.</p>
    </div>
    <div class="instruction-card">
      <h3>PyCharm</h3>
      <p>Откройте скачанный файл в PyCharm (Professional поддерживает ноутбуки нативно, в
      Community установите плагин Jupyter), выберите интерпретатор Python 3.14 и запускайте
      ячейки.</p>
    </div>
    <div class="instruction-card">
      <h3>Jupyter</h3>
      <p>Установите Jupyter (<code class="inline">pip install notebook</code>), запустите
      <code class="inline">jupyter notebook</code> в папке со скачанным файлом и откройте его
      в браузере — ядро выполняется локально, поэтому {jupyter_tail}.</p>
    </div>
  </div>

  <div class="local-complete-block">
    <button id="mark-local-complete-btn" class="btn-secondary" type="button">Я выполнил упражнение локально</button>
    <div id="local-complete-status" class="local-complete-status"></div>
  </div>

  <div class="practice-route-links">
    <a class="practice-return" href="{return_url}">← Вернуться к уроку</a>
    <a class="practice-next" href="{next_url}">Следующая страница теории →</a>
  </div>
</main>

{NAV_SCRIPT_TAG}
<script>
(function () {{
  var btn = document.getElementById("mark-local-complete-btn");
  var status = document.getElementById("local-complete-status");
  var lessonId = "{lesson_id_js}";
  var key = "cartesian.python.progress.v1";

  function render() {{
    try {{
      var all = JSON.parse(localStorage.getItem(key) || "{{}}");
      var entry = all[lessonId];
      if (entry && entry.status === "completed-local") {{
        status.innerHTML = '<strong style="color:#15803d">✓ Выполнено локально</strong> — результат не проверялся автоматически';
        btn.textContent = "Отметить заново";
      }}
    }} catch (e) {{}}
  }}

  btn.addEventListener("click", function () {{
    var confirmed = window.confirm(
      "Подтвердите: вы самостоятельно выполнили это упражнение локально " +
      "(в VS Code, PyCharm или Jupyter). Результат не будет проверен автоматически."
    );
    if (!confirmed) return;
    try {{
      var all = JSON.parse(localStorage.getItem(key) || "{{}}");
      all[lessonId] = {{
        status: "completed-local",
        assessment: "local-required",
        verified: false,
        score: null,
        completedAt: new Date().toISOString()
      }};
      localStorage.setItem(key, JSON.stringify(all));
      render();
    }} catch (e) {{}}
  }});

  render();
}})();
</script>
</body>
</html>
"""


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for lesson_id, entry in manifest.items():
        out_dir = OUT_DIR / lesson_id
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "index.html"
        if entry.get("backend") == "local-required":
            out_path.write_text(build_local_required_page(lesson_id, entry), encoding="utf-8")
        else:
            out_path.write_text(build_page(lesson_id, entry), encoding="utf-8")
        print(f"Записано: {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
