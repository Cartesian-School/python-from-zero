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

from site_lib import NAV_SCRIPT_TAG, mobile_nav_links, site_header

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"
OUT_DIR = ROOT / "site" / "practice"


def build_page(lesson_id: str, entry: dict) -> str:
    notebook_url = f"/notebooks/{entry['notebook']}"
    download_name = entry["notebook"].split("/")[-1]
    chapter_title = html.escape(entry["chapter_title"])
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
            "chapterTitle": entry["chapter_title"],
            "lessonTitle": entry["lesson_title"],
            "notebookUrl": notebook_url,
            "graderUrl": entry["grader"],
            "downloadUrl": notebook_url,
            "returnUrl": entry["return_url"],
            "nextUrl": entry.get("next_url"),
            "assessment": entry.get("assessment", "automatic"),
            "workerUrl": "/assets/js/python-worker.mjs",
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
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav-panel">☰ Меню</button>
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


def build_local_required_page(lesson_id: str, entry: dict) -> str:
    """Practice page for lessons whose canonical code cannot run in the
    browser (confirmed: Pyodide has no turtle or tkinter — see the Chapter
    6/7 rollout evidence). No Pyodide worker, no grader, no score: the
    learner runs the canonical .ipynb locally and may optionally
    self-declare completion, clearly marked as unverified.
    """
    notebook_url = f"/notebooks/{entry['notebook']}"
    download_name = entry["notebook"].split("/")[-1]
    chapter_title = html.escape(entry["chapter_title"])
    lesson_title = html.escape(entry["lesson_title"])
    return_url = html.escape(entry["return_url"])
    lesson_id_js = html.escape(lesson_id).replace('"', '\\"')

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
  <p>Эта практика использует модуль <code class="inline">turtle</code>, который открывает
  нативное графическое окно Python. Такой режим недоступен в текущей браузерной среде
  Python. Выполните это упражнение локально в Python 3.14.</p>

  <div class="actions">
    <a class="btn-primary" href="{notebook_url}" download="{html.escape(download_name)}">📄 Скачать .ipynb</a>
  </div>

  <div class="local-instructions">
    <div class="instruction-card">
      <h3>VS Code</h3>
      <p>Установите расширения <strong>Python</strong> и <strong>Jupyter</strong> (Microsoft), откройте
      скачанный файл прямо в VS Code, выберите интерпретатор Python 3.14 и запускайте ячейки
      (<code class="inline">Shift+Enter</code>) — окно Turtle откроется на вашем компьютере.</p>
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
      в браузере — ядро выполняется локально, поэтому окно Turtle откроется как обычно.</p>
    </div>
  </div>

  <div class="local-complete-block">
    <button id="mark-local-complete-btn" class="btn-secondary" type="button">Я выполнил упражнение локально</button>
    <div id="local-complete-status" class="local-complete-status"></div>
  </div>

  <a class="practice-return" href="{return_url}">← Вернуться к уроку</a>
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
