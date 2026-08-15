# Python from Zero — Cartesian School

A free, structured Python 3.14 course for absolute beginners, published by Cartesian School.

## About

This repository contains "Python с нуля" ("Python from Zero"), a Russian-language beginner Python course/book, together with its supporting materials: chapter theory rendered as a static website, canonical Jupyter notebooks for every lesson, standalone mini-projects, and a first-party interactive practice system that runs real Python in the browser.

The course content itself is written in Russian; this README and other repository/crawler-facing documentation are in English.

## Features

- Python 3.14 curriculum, 24 chapters
- Structured theory rendered as a static, responsive website
- Canonical Jupyter notebooks (`.ipynb`) for every lesson — the source of truth, never auto-generated from the HTML
- Browser-based Python execution using [Pyodide](https://pyodide.org/) (Python 3.14, in a Web Worker) — no install required, currently live for Chapter 3
- Automatic grading with a trusted, non-learner-editable grader script per lesson, plus persistent local progress (`localStorage`)
- Downloadable original notebooks for local use in VS Code, PyCharm, or Jupyter
- Standalone mini-projects (Tkinter, Pygame, Flask, and more)
- Static deployment on Vercel — no application server, no database

## Live Site

https://www.cartesianschool.org

## Repository Structure

```
site/         Generated static website (HTML/CSS/JS) — the deploy artifact
notebooks/    Canonical Jupyter notebooks, one per lesson
book/         Compiled PDF/EPUB editions of the book
projects/     Standalone mini-projects referenced by the book
manifest/     Machine-readable manifests (chapter coverage, interactive practice)
scripts/      Python build scripts that generate site/ from structured data
tests/        Automated tests (pytest) for the standalone mini-projects
design/       Design assets and exports
evidence/     Technical investigation write-ups (e.g. the JupyterLite evaluation)
web/          The interactive practice client (Pyodide bridge, notebook renderer)
```

## Local Development

The site is built by a set of Python scripts in `scripts/`, each responsible for one chapter or page family (`build_chapter_03.py`, `build_front_matter.py`, `build_site_index.py`, ...), sharing common rendering helpers from `scripts/site_lib.py`. There is no committed `requirements.txt` yet — install the packages the scripts import as needed (`nbformat`, `nbclient`, `ebooklib`, `weasyprint`, `beautifulsoup4`, `pytest`, `ruff`) with Python 3.14.

Regenerate a single chapter:

```bash
python3 scripts/build_chapter_03.py
```

Regenerate the homepage or subject index:

```bash
python3 scripts/build_site_index.py
python3 scripts/build_index.py
```

Regenerate the interactive practice pages from `manifest/practice_manifest.json`:

```bash
python3 scripts/build_practice_pages.py
```

## Building

A full production build (static site + SEO metadata + sitemap + manifest/navigation validation) is produced by:

```bash
bash scripts/build_vercel.sh
```

This writes the deployable output to `dist/` and is what Vercel runs on every push.

## Testing

```bash
# Standalone mini-projects (pytest; GUI projects need a display or Xvfb)
pytest tests/ -v

# Interactive practice client (Playwright, against a local dist/ build)
cd web && npm install && npm test
```

## Interactive Practice Architecture

Each lesson's canonical `.ipynb` remains the single source of truth — it is parsed and rendered directly in the browser, not converted to another format. The flow:

```
.ipynb (nbformat JSON)
  → browser notebook renderer (CodeMirror 6 + sanitized Markdown)
  → Pyodide Web Worker (Python 3.14.2, persistent interpreter namespace)
  → trusted grader script (reads real execution results, not learner-editable code)
  → progress persisted to localStorage
```

This is a first-party runner, not JupyterLite — see `evidence/jupyterlite-kernel-investigation.md` for why.

## Browser Compatibility

Lessons that only use standard Python (no GUI, no native OS access) execute directly in the browser via Pyodide. Lessons that rely on native GUI toolkits (Tkinter, Turtle) or other local-only APIs are not claimed as browser-compatible — they are meant to be run locally (VS Code, PyCharm, or Jupyter), with the canonical notebook always available for download.

## License

[MIT](LICENSE.md)

## Author

Siergej Sobolewski
Software & AI Engineer
Founder of Cartesian School

## Links

- Live site: https://www.cartesianschool.org
- GitHub repository: https://github.com/Cartesian-School/python-from-zero
