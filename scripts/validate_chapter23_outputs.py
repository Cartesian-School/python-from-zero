#!/usr/bin/env python3
"""Validate the generated Chapter 23 academic and branding contracts."""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_chapter_23 import HOMEWORK_PAGES, PAGES

ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-23"
SOURCE_MANIFEST = ROOT / "data" / "chapter-23-official-sources.json"
BRAND_MANIFEST = ROOT / "data" / "git-brand-assets.json"

GIT_BRANDED_PAGES = {
    "23-git-01-chto-takoe-git-github.html",
    "23-git-02-ustanavlivaem-git.html",
    "23-git-03-pervaya-nastrojka.html",
    "23-git-05-autentifikaciya.html",
    "23-git-06-ssh.html",
    "23-git-07-sozdaem-repozitorij.html",
    "23-git-08-kloniruem.html",
    "23-git-09-lokalnyj-i-udalennyj.html",
    "23-git-10-working-tree-staging-commit.html",
    "23-28-git-kommit.html",
}

OFFICIAL_GIT_ASSET_HASHES = {
    "lockup-color.svg": "c5f6153fc8e226accca81b404961b2bc465baccfb8521d081799eaaf4be3379d",
    "lockup-black.svg": "bc76df3f745738484b172beb0b4fcf770de0603fde451487dafa2b45f76371ce",
    "lockup-white.svg": "4b92d8fe6d9d7fa010a2cb526cb61bc9c7083678f7e9ffb5065d8b899817687f",
    "mark-orange.svg": "1080a5430edb6278dc03e4b04efc16c8bed5b943408d648ad721a28836814220",
    "mark-black.svg": "0bf58ad2b4a330d0023d65ffbf056f5d93abee6b29eca81904951b014b3c9cd9",
    "mark-white.svg": "4b62d3bdfe913e88de9bd9d25cf466af9d4ac759dfecc8a17d86016b35b97a6e",
}


def text_of(filename: str) -> str:
    source = (CHAPTER_DIR / filename).read_text(encoding="utf-8")
    source = re.sub(r"<script.*?</script>", " ", source, flags=re.DOTALL)
    source = re.sub(r"<style.*?</style>", " ", source, flags=re.DOTALL)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", source))).strip()


def require_tokens(errors: list[str], filename: str, tokens: tuple[str, ...]) -> None:
    text = text_of(filename)
    for token in tokens:
        if token not in text:
            errors.append(f"{filename}: отсутствует обязательный academic contract token {token!r}")


def require_html_tokens(errors: list[str], filename: str, tokens: tuple[str, ...]) -> None:
    source = (CHAPTER_DIR / filename).read_text(encoding="utf-8")
    for token in tokens:
        if token not in source:
            errors.append(f"{filename}: отсутствует обязательный HTML contract token {token!r}")


def validate() -> list[str]:
    errors = []
    canonical = [entry[0] for entry in PAGES] + [entry[0] for entry in HOMEWORK_PAGES]
    if len(canonical) != 67 or len(set(canonical)) != 67:
        errors.append(f"Канонический набор должен содержать 67 уникальных страниц, получено {len(set(canonical))}")
    for filename in canonical:
        path = CHAPTER_DIR / filename
        if not path.exists():
            errors.append(f"Каноническая страница не найдена: {filename}")
            continue
        source = path.read_text(encoding="utf-8")
        if source.count("<h1") != 1:
            errors.append(f"{filename}: ожидался ровно один видимый H1")
        if filename != "index.html" and "class=\"section-nav\"" not in source:
            errors.append(f"{filename}: отсутствует каноническая навигация страницы")

    for name, expected_hash in OFFICIAL_GIT_ASSET_HASHES.items():
        path = ROOT / "site" / "assets" / "brand" / "git" / name
        if not path.exists():
            errors.append(f"Официальный Git asset отсутствует: {path.relative_to(ROOT)}")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"Git asset изменён или перерисован: {name}, sha256={actual_hash}")

    brand_manifest = json.loads(BRAND_MANIFEST.read_text(encoding="utf-8"))
    if brand_manifest.get("official_source") != "https://git-scm.com/downloads/logos":
        errors.append("Git brand metadata не указывает официальный logo source")
    if brand_manifest.get("author") != "Jason Long" or brand_manifest.get("license") != "CC BY 3.0":
        errors.append("Git logo attribution должна быть отделена от GitHub Docs CC BY 4.0")
    manifest_hashes = {
        Path(asset["path"]).name: asset["sha256"] for asset in brand_manifest.get("assets", [])
    }
    if manifest_hashes != OFFICIAL_GIT_ASSET_HASHES:
        errors.append("Git brand metadata не совпадает с pinned official asset hashes")

    actual_git_branded = set()
    for filename in canonical:
        path = CHAPTER_DIR / filename
        if not path.exists():
            continue
        source = path.read_text(encoding="utf-8")
        match = re.search(r"<h1[^>]*>.*?</h1>", source, flags=re.DOTALL)
        h1 = match.group(0) if match else ""
        if "/assets/brand/git/mark-black.svg" in h1:
            errors.append(f"{filename}: black Git mark запрещён в light-surface H1")
        if "/assets/brand/git/mark-orange.svg" in h1:
            actual_git_branded.add(filename)
            if 'alt=""' not in h1 or 'aria-hidden="true"' not in h1:
                errors.append(f"{filename}: Git heading mark нарушает accessibility contract")
            h1_inner = re.sub(r"^<h1[^>]*>\s*", "", h1)
            if not h1_inner.startswith('<span class="technology-heading__brands'):
                errors.append(f"{filename}: Git mark не является ведущим H1 brand element")
            if any(token in h1 for token in ("filter:", "currentColor", "assets/icons/cartesian")):
                errors.append(f"{filename}: Git H1 пытается recolor/reconstruct официальный asset")
    if actual_git_branded != GIT_BRANDED_PAGES:
        errors.append(
            f"Git heading branding: missing={sorted(GIT_BRANDED_PAGES - actual_git_branded)}, "
            f"extra={sorted(actual_git_branded - GIT_BRANDED_PAGES)}"
        )

    mixed = (CHAPTER_DIR / "23-git-01-chto-takoe-git-github.html").read_text(encoding="utf-8")
    mixed_h1 = re.search(r"<h1[^>]*>.*?</h1>", mixed, flags=re.DOTALL).group(0)
    if (
        "/assets/brand/git/mark-orange.svg" not in mixed_h1
        or "/assets/brand/github/invertocat-black.svg" not in mixed_h1
    ):
        errors.append("Смешанный Git/GitHub H1 не показывает отдельный официальный GitHub mark")
    github_pr_h1 = re.search(
        r"<h1[^>]*>.*?</h1>",
        (CHAPTER_DIR / "23-29-github-pr.html").read_text(encoding="utf-8"),
        flags=re.DOTALL,
    ).group(0)
    if "/assets/brand/git/" in github_pr_h1:
        errors.append("GitHub-primary страница 23-29 ошибочно получила Git mark в H1")

    require_tokens(errors, "index.html", ("24 практики: 18 SafeSort + 6 домашних",))
    require_tokens(
        errors,
        "23-git-01-chto-takoe-git-github.html",
        (
            "Официальные ресурсы Git",
            "Официальный сайт Git",
            "Справочная документация Git",
            "Книга Pro Git",
            "Git Source Code Mirror on GitHub",
            "Сам Git не зависит от GitHub",
            "Jason Long",
            "CC BY 3.0",
        ),
    )
    require_html_tokens(
        errors,
        "23-git-01-chto-takoe-git-github.html",
        (
            'href="https://git-scm.com/"',
            'href="https://git-scm.com/docs"',
            'href="https://git-scm.com/book/en/v2"',
            'href="https://github.com/git/git"',
        ),
    )
    require_tokens(
        errors,
        "23-05-pyproject-toml.html",
        (
            "Импортируемый пакет",
            "Distribution/build project",
            "Установленная distribution",
            "python -m pip install -e .",
            "src-layout",
            "import safesort",
            "safesort --help",
        ),
    )
    require_tokens(
        errors,
        "23-git-10-working-tree-staging-commit.html",
        ("граф коммитов", "branch", "HEAD", "origin/main", "git fetch", "git pull", "git push", "git branch -vv"),
    )
    require_tokens(
        errors,
        "23-07-pathlib.html",
        ("frozen=True", "Неизменяемые данные не означают чистую функцию", "Функция может получать frozen-объект и всё равно записывать файлы"),
    )
    require_tokens(
        errors,
        "23-18-sha256.html",
        ("many-to-one", "вычислительно неосуществим на практике", "не доказывает равенство файлов", "NIST FIPS 180-4"),
    )
    require_tokens(
        errors,
        "23-19-gruppy-dublikatov.html",
        ("создаёт новый класс", "сравнивает файлы внутри неё побайтово"),
    )
    require_tokens(
        errors,
        "23-22-nastrojki-proekta.html",
        ("Приоритет настроек: defaults → пользовательские additions/overrides → эффективная Config", "books", "конфигурация остаётся в корне"),
    )
    require_tokens(
        errors,
        "23-26-testy-dublikatov.html",
        ("result test (black-box)", "interaction/implementation contract", "RecordingReader", "requested_sizes"),
    )
    require_tokens(
        errors,
        "23-27-testy-cli.html",
        ("SystemExit(0)", "код 0 означает успешное завершение", "обычно 2"),
    )
    require_tokens(
        errors,
        "23-29-github-pr.html",
        ("LOCAL GIT", "GITHUB", "Граница пересекается на git push", "Conversation", "Commits", "Checks", "Files changed", "Approve", "Request changes"),
    )
    require_tokens(
        errors,
        "23-31-versiya-reliz.html",
        ("python -m build", "safesort-0.1.0-py3-none-any.whl", "safesort-0.1.0.tar.gz", "Smoke test в чистом окружении", "Git tag и GitHub Release: разные объекты"),
    )
    require_tokens(
        errors,
        "23-hw-03-kamen-nozhnicy-bumaga.html",
        ("dict[str, set[str]]", "opponent in beats[player]", "изменилось требование", "модель данных"),
    )
    require_tokens(
        errors,
        "23-hw-04-otskakivayushie-myachi.html",
        ("лобовое столкновение одинаковых мячей", "Не выдавайте этот приём за общую формулу", "может зависеть от размера шага времени"),
    )
    require_tokens(
        errors,
        "23-hw-05-temperatura.html",
        ("Единица SI называется кельвин", "273.15 K", "BIPM SI Brochure"),
    )

    forbidden = {
        "apply — единственная команда, которая меняет диск",
        "перемещает файлы исключительно apply",
        "apply — единственная команда, после которой файлы",
        "git add перемещает файл",
        "целиком на GitHub",
        "gh pr create",
        "хеш невозможно обратить",
    }
    all_text = "\n".join(text_of(filename) for filename in canonical if (CHAPTER_DIR / filename).exists())
    for phrase in forbidden:
        if phrase.casefold() in all_text.casefold():
            errors.append(f"В канонической Главе 23 осталось запрещённое утверждение: {phrase!r}")

    source_manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    category_counts = {}
    for source in source_manifest["sources"]:
        category_counts[source["category"]] = category_counts.get(source["category"], 0) + 1
    minimums = {
        "git-github": 1,
        "python-packaging": 1,
        "testing": 1,
        "cryptography": 1,
        "versioning": 1,
        "metrology": 1,
    }
    for category, minimum in minimums.items():
        if category_counts.get(category, 0) < minimum:
            errors.append(f"Недостаточно источников категории {category}: {category_counts.get(category, 0)}")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Generated Chapter 23 невалидна: {len(errors)} ошибок", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "Generated Chapter 23 валидна: 67 canonical pages; 10/10 Git-branded H1; "
        "academic P0 contracts, mutation wording, release pipeline, and source coverage PASS."
    )


if __name__ == "__main__":
    main()
