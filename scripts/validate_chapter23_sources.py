#!/usr/bin/env python3
"""Валидирует data/chapter-23-official-sources.json против реального содержимого
scripts/build_chapter_23.py — без обращений к сети.

Источник истины — это не сам JSON-файл, а вызовы official_sources([...]) внутри
scripts/build_chapter_23.py: манифест обязан описывать ровно то же самое множество
источников и маршрутов, которое реально используется в главе. Скрипт заново
извлекает это множество из исходника и сравнивает с манифестом.

Отклоняет манифест, если:
- отсутствует обязательное поле верхнего уровня или записи (id, title, url,
  provider, license, checked_date, adapted, routes);
- есть повторяющийся id или повторяющийся url среди записей;
- route ссылается на файл, которого нет в site/chapters/glava-23/;
- provider не соответствует домену официального источника;
- license не соответствует правилам provider (GitHub Docs: CC BY 4.0,
  остальные первичные источники в этом манифесте: link-only);
- манифест не совпадает с фактическими official_sources(...) в
  build_chapter_23.py — ни по множеству URL, ни по множеству маршрутов
  на каждый URL (это ловит и забытые добавления, и устаревшие записи).

Использование: python3 scripts/validate_chapter23_sources.py
Возвращает ненулевой код выхода и печатает все найденные ошибки, если манифест
невалиден — предназначен для вызова из build-конвейера.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "data" / "chapter-23-official-sources.json"
BUILD_SCRIPT_PATH = ROOT / "scripts" / "build_chapter_23.py"
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-23"

REQUIRED_TOP_KEYS = {"schema_version", "chapter", "sources"}
REQUIRED_ENTRY_KEYS = {
    "id", "title", "url", "provider", "category", "license",
    "checked_date", "adapted", "routes",
}
PROVIDER_LICENSE = {
    "github-docs": "CC BY 4.0",
    "git-source-mirror": "link-only",
    "git-scm": "link-only",
    "python-docs": "link-only",
    "packaging-guide": "link-only",
    "pytest-docs": "link-only",
    "nist": "link-only",
    "semver": "link-only",
    "bipm": "link-only",
}
VALID_PROVIDERS = set(PROVIDER_LICENSE)
VALID_CATEGORIES = {
    "git-github", "python-packaging", "testing", "cryptography",
    "versioning", "metrology", "physics",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def classify_source(url: str) -> tuple[str, str]:
    """Return the manifest provider and academic coverage category."""
    if url.startswith("https://docs.github.com/"):
        return "github-docs", "git-github"
    if url == "https://github.com/git/git":
        return "git-source-mirror", "git-github"
    if url.startswith("https://git-scm.com/"):
        return "git-scm", "git-github"
    if url.startswith("https://docs.python.org/"):
        category = "testing" if "/unittest.mock" in url else "python-packaging"
        return "python-docs", category
    if url.startswith("https://packaging.python.org/"):
        return "packaging-guide", "python-packaging"
    if url.startswith("https://docs.pytest.org/"):
        return "pytest-docs", "testing"
    if url.startswith("https://csrc.nist.gov/"):
        return "nist", "cryptography"
    if url.startswith("https://semver.org/"):
        return "semver", "versioning"
    if url.startswith("https://www.bipm.org/"):
        return "bipm", "metrology"
    raise ValueError(f"неизвестный официальный source URL: {url}")


def extract_sources_from_build_script() -> tuple[dict[str, dict], list[dict]]:
    """Заново вычисляет множество источников из official_sources(...) вызовов
    в build_chapter_23.py. Возвращает (by_url, calls):
    - by_url: {url: {"title": ..., "adapted": bool|None, "routes": set[str]}}
    - calls: список отдельных вызовов official_sources(...) — по одному на
      каждую "коробку" на странице — как {"route", "urls": [...], "adapted": bool},
      где adapted уже разрешён к фактическому значению (True по умолчанию,
      если аргумент не передан), нужен для проверки атрибуции git-scm."""
    text = BUILD_SCRIPT_PATH.read_text(encoding="utf-8")
    func_pattern = re.compile(r"^def (build_\w+)\(\) -> None:", re.MULTILINE)
    starts = [(m.group(1), m.start()) for m in func_pattern.finditer(text)]
    starts.append(("__END__", len(text)))

    by_url: dict[str, dict] = {}
    calls: list[dict] = []
    for i in range(len(starts) - 1):
        _name, start = starts[i]
        end = starts[i + 1][1]
        block = text[start:end]
        write_m = re.search(r'write\("([^"]+)"', block)
        if not write_m:
            continue
        route = write_m.group(1)
        for os_m in re.finditer(
            r"official_sources\(\[(.*?)\](?:,\s*adapted=(\w+))?\)",
            block,
            re.DOTALL,
        ):
            body = os_m.group(1)
            adapted_raw = os_m.group(2)
            adapted = None if adapted_raw is None else (adapted_raw == "True")
            call_urls: list[str] = []
            for title, url in re.findall(r'\(\s*"([^"]+)",\s*"(https://[^"]+)"\s*\)', body):
                entry = by_url.setdefault(url, {"title": title, "adapted": adapted, "routes": set()})
                entry["routes"].add(route)
                call_urls.append(url)
            if call_urls:
                calls.append({"route": route, "urls": call_urls, "adapted": True if adapted is None else adapted})
    return by_url, calls


def validate() -> list[str]:
    errors: list[str] = []

    if not MANIFEST_PATH.exists():
        return [f"Манифест не найден: {MANIFEST_PATH.relative_to(ROOT)}"]

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    missing_top = REQUIRED_TOP_KEYS - manifest.keys()
    if missing_top:
        errors.append(f"В манифесте отсутствуют обязательные поля верхнего уровня: {sorted(missing_top)}")
        return errors

    sources = manifest["sources"]
    if not isinstance(sources, list) or not sources:
        errors.append("Поле 'sources' должно быть непустым списком")
        return errors

    seen_ids: dict[str, int] = {}
    seen_urls: dict[str, int] = {}
    manifest_by_url: dict[str, dict] = {}

    for idx, entry in enumerate(sources):
        prefix = f"sources[{idx}] (id={entry.get('id', '?')!r})"
        missing = REQUIRED_ENTRY_KEYS - entry.keys()
        if missing:
            errors.append(f"{prefix}: отсутствуют поля {sorted(missing)}")
            continue

        entry_id = entry["id"]
        url = entry["url"]
        provider = entry["provider"]
        category = entry["category"]
        license_ = entry["license"]
        checked_date = entry["checked_date"]
        adapted = entry["adapted"]
        routes = entry["routes"]

        if entry_id in seen_ids:
            errors.append(f"{prefix}: дублирующийся id {entry_id!r} (уже использован в sources[{seen_ids[entry_id]}])")
        else:
            seen_ids[entry_id] = idx

        if url in seen_urls:
            errors.append(f"{prefix}: дублирующийся url {url!r} (уже использован в sources[{seen_urls[url]}])")
        else:
            seen_urls[url] = idx
            manifest_by_url[url] = entry

        if provider not in VALID_PROVIDERS:
            errors.append(f"{prefix}: неизвестный provider {provider!r} (ожидается один из {sorted(VALID_PROVIDERS)})")
        elif license_ != PROVIDER_LICENSE[provider]:
            errors.append(f"{prefix}: provider={provider!r} требует license={PROVIDER_LICENSE[provider]!r}, получено {license_!r}")

        if category not in VALID_CATEGORIES:
            errors.append(f"{prefix}: неизвестная category {category!r}")
        try:
            expected_provider, expected_category = classify_source(url)
        except ValueError as exc:
            errors.append(f"{prefix}: {exc}")
        else:
            if provider != expected_provider or category != expected_category:
                errors.append(
                    f"{prefix}: URL требует provider/category "
                    f"{expected_provider}/{expected_category}, получено {provider}/{category}"
                )

        if not DATE_RE.match(str(checked_date)):
            errors.append(f"{prefix}: checked_date {checked_date!r} не в формате YYYY-MM-DD")

        if not isinstance(adapted, bool):
            errors.append(f"{prefix}: 'adapted' должен быть bool, получено {adapted!r}")

        if not isinstance(routes, list) or not routes:
            errors.append(f"{prefix}: 'routes' должен быть непустым списком имён файлов")
            continue
        for route in routes:
            if not (CHAPTER_DIR / route).exists():
                errors.append(f"{prefix}: route {route!r} не найден в site/chapters/glava-23/")

    # Сверка с фактическим содержимым build_chapter_23.py.
    actual, calls = extract_sources_from_build_script()

    actual_urls = set(actual.keys())
    manifest_urls = set(manifest_by_url.keys())

    missing_from_manifest = actual_urls - manifest_urls
    for url in sorted(missing_from_manifest):
        errors.append(
            f"Источник используется в build_chapter_23.py, но отсутствует в манифесте: "
            f"{actual[url]['title']!r} ({url})"
        )

    stale_in_manifest = manifest_urls - actual_urls
    for url in sorted(stale_in_manifest):
        errors.append(
            f"Манифест ссылается на источник, которого больше нет в build_chapter_23.py: "
            f"{manifest_by_url[url]['title']!r} ({url})"
        )

    for url in sorted(actual_urls & manifest_urls):
        actual_routes = actual[url]["routes"]
        manifest_routes = set(manifest_by_url[url]["routes"])
        if actual_routes != manifest_routes:
            missing_routes = actual_routes - manifest_routes
            extra_routes = manifest_routes - actual_routes
            detail = []
            if missing_routes:
                detail.append(f"отсутствуют в манифесте: {sorted(missing_routes)}")
            if extra_routes:
                detail.append(f"лишние в манифесте: {sorted(extra_routes)}")
            errors.append(f"Маршруты для {url} не совпадают ({'; '.join(detail)})")

    # Link-only sources are not translated GitHub documentation. No source
    # box containing only link-only providers may render the GitHub CC BY note.
    # не должна рендерить примечание "официальной документации GitHub... CC
    # BY 4.0" — это ложная атрибуция. Разрешено только если та же коробка
    # реально содержит источник с provider=github-docs (смешанная коробка).
    for call in calls:
        providers = {manifest_by_url[u]["provider"] for u in call["urls"] if u in manifest_by_url}
        if providers and "github-docs" not in providers and call["adapted"]:
            errors.append(
                f"{call['route']}: official_sources({call['urls']}) содержит только "
                f"link-only providers, но adapted не установлен в False — рендерится ложная "
                f"атрибуция 'официальной документации GitHub... CC BY 4.0' на ссылки git-scm.com"
            )

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Манифест источников главы 23 невалиден — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print(
        f"Манифест источников главы 23 валиден: {len(manifest['sources'])} источник(ов), "
        f"сверено с фактическими official_sources(...) в build_chapter_23.py, "
        f"расхождений не найдено."
    )


if __name__ == "__main__":
    main()
