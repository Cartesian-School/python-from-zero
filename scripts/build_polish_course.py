#!/usr/bin/env python3
"""Build the complete Polish web course from canonical RU outputs and PL resources.

The repository's historical builders render one complete RU document at a time.
This adapter is the locale boundary for those builders: human-facing strings are
resolved through a committed translation memory, while code, identifiers and
machine-readable payloads are retained verbatim.  ``site/pl`` and localized
notebooks are delivery artifacts, never translation sources.

``--collect`` updates the translation memory with untranslated source strings.
``--translate-offline`` fills pending records with locally installed Argos/OPUS
models.  Neither operation runs in production.  A normal invocation is entirely
offline and fails closed when a visible source string has no PL resource.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup, Comment, NavigableString

sys.path.insert(0, str(Path(__file__).resolve().parent))

from localization import source_hash

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PL_ROOT = SITE / "pl"
TM_PATH = ROOT / "manifest/i18n/content/pl/course_translation_memory.json"
ROUTES_PATH = ROOT / "manifest/i18n/routes.json"
PRACTICE_MANIFEST = ROOT / "manifest/practice_manifest.json"

CYRILLIC = re.compile(r"[\u0400-\u04ff]")
SKIP_TEXT_PARENTS = {"code", "pre", "script", "style"}
TRANSLATED_ATTRIBUTES = ("alt", "title", "aria-label", "aria-description", "placeholder")
FRONT_MATTER_NAMES = {
    "vvedenie.html": "wprowadzenie.html",
    "ob-avtore.html": "o-autorze.html",
    "o-tehnicheskom-recenzente.html": "o-recenzencie-technicznym.html",
    "litsenziya.html": "licencja.html",
}


@dataclass(frozen=True)
class PagePair:
    page_id: str
    ru_file: Path
    pl_file: Path
    source_path: str
    dependencies: tuple[str, ...] = ()
    practice_id: str | None = None
    project_id: str | None = None

    @property
    def ru_url(self) -> str:
        return "/" + self.ru_file.relative_to(SITE).as_posix()

    @property
    def pl_url(self) -> str:
        return "/" + self.pl_file.relative_to(SITE).as_posix()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def page_pairs() -> list[PagePair]:
    """Return every stable RU/PL page identity in deterministic order."""
    practice = _read_json(PRACTICE_MANIFEST)
    projects = _read_json(ROOT / "manifest/projects_manifest.json")["projects"]
    project_by_slug = {item["slug"]: item for item in projects}
    pairs: list[PagePair] = [
        PagePair(
            "home", SITE / "index.html", PL_ROOT / "index.html",
            "scripts/build_site_index.py",
            ("scripts/author_profile.py", "data/chapters.json", "data/book-pagination.json",
             "manifest/practice_manifest.json", "manifest/projects_manifest.json",
             "manifest/projects_presentation.json"),
        ),
        PagePair(
            "reference-index", SITE / "predmetnyj-ukazatel.html",
            PL_ROOT / "indeks-rzeczowy.html", "scripts/build_index.py",
            ("data/chapters.json",),
        ),
    ]

    for source in sorted((SITE / "front-matter").glob("*.html")):
        name = FRONT_MATTER_NAMES[source.name]
        logical = {
            "vvedenie.html": "front-matter-introduction",
            "ob-avtore.html": "front-matter-author",
            "o-tehnicheskom-recenzente.html": "front-matter-technical-reviewer",
            "litsenziya.html": "front-matter-license",
        }[source.name]
        if source.name == "litsenziya.html":
            source_path = "scripts/build_license_page.py"
            deps = ("LICENSE.md", "LICENSE-CODE.md", "LICENSE-CONTENT.md")
        else:
            source_path = "scripts/build_front_matter.py"
            deps = ("scripts/author_profile.py",) if source.name == "ob-avtore.html" else ()
        pairs.append(PagePair(logical, source, PL_ROOT / "front-matter" / name, source_path, deps))

    for chapter_dir in sorted((SITE / "chapters").glob("glava-[0-9][0-9]")):
        chapter = chapter_dir.name[-2:]
        builder = f"scripts/build_chapter_{chapter}.py"
        for source in sorted(chapter_dir.glob("*.html")):
            if source.name == "index.html":
                logical = f"chapter-{chapter}"
            else:
                # Most lessons start with NN-NN.  Chapter 23 additionally has
                # named Git/GitHub theory units; the complete canonical stem is
                # already their stable identity and avoids inventing IDs.
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source.stem):
                    raise ValueError(f"Chapter page has no stable lesson identity: {source}")
                logical = f"chapter-{chapter}-lesson-{source.stem}"
            pairs.append(PagePair(
                logical, source, PL_ROOT / "chapters" / f"rozdzial-{chapter}" / source.name,
                builder, ("scripts/site_lib.py", "scripts/chapter_metadata.py", "data/chapters.json"),
            ))

    for practice_id, entry in sorted(practice.items()):
        source = SITE / "practice" / practice_id / "index.html"
        if not source.is_file():
            raise FileNotFoundError(source)
        pairs.append(PagePair(
            f"practice-{practice_id}", source, PL_ROOT / "practice" / practice_id / "index.html",
            f"notebooks/{entry['notebook']}",
            ("scripts/build_practice_pages.py", "manifest/practice_manifest.json", "web/src/practice-app.js"),
            practice_id=practice_id,
        ))

    for source in sorted((SITE / "projects").glob("*/index.html")):
        project = project_by_slug[source.parent.name]
        pairs.append(PagePair(
            f"project-{project['id']}", source,
            PL_ROOT / "projects" / project["id"] / "index.html",
            "manifest/projects_manifest.json",
            ("manifest/projects_presentation.json", "scripts/build_projects.py"),
            project_id=project["id"],
        ))

    ids = [pair.page_id for pair in pairs]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate logical page ID")
    return sorted(pairs, key=lambda item: item.page_id)


class TranslationMemory:
    def __init__(self, *, collect: bool) -> None:
        self.collect = collect
        if TM_PATH.is_file():
            raw = _read_json(TM_PATH)
            self.entries: dict[str, str] = raw.get("entries", {})
            self.sources: dict[str, str] = raw.get("sources", {})
        else:
            self.entries = {}
            self.sources = {}
        self.missing: set[str] = set()

    @staticmethod
    def _key(source: str) -> str:
        return hashlib.sha256(source.encode("utf-8")).hexdigest()

    def translate(self, source: str) -> str:
        if not CYRILLIC.search(source):
            return source
        key = self._key(source)
        self.sources[key] = source
        target = self.entries.get(key)
        if target:
            return target
        self.missing.add(source)
        if self.collect:
            return source
        raise KeyError(f"Missing Polish translation resource for {source!r}")

    def save_pending(self) -> None:
        for source in sorted(self.missing):
            self.entries.setdefault(self._key(source), "")
        payload = {
            "schema_version": 1,
            "source_locale": "ru",
            "target_locale": "pl",
            "entries": dict(sorted(self.entries.items())),
            "sources": dict(sorted(self.sources.items())),
        }
        TM_PATH.parent.mkdir(parents=True, exist_ok=True)
        TM_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _preserve_outer_space(source: str, target: str) -> str:
    leading = source[: len(source) - len(source.lstrip())]
    trailing = source[len(source.rstrip()):]
    return leading + target.strip() + trailing


_SCRIPT_BLOCK = re.compile(r"(<script\b[^>]*>)(.*?)(</script>)", re.S)
_JS_STRING_LITERAL = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'')
_JS_ESCAPE = re.compile(r"\\u([0-9a-fA-F]{4})|\\n|\\t|\\r|\\\\|\\'|\\\"")
_JS_ESCAPE_MAP = {"\\n": "\n", "\\t": "\t", "\\r": "\r", "\\\\": "\\", "\\'": "'", '\\"': '"'}


def _decode_js_literal(raw: str) -> str:
    body = raw[1:-1]

    def repl(match: re.Match[str]) -> str:
        if match.group(1):
            return chr(int(match.group(1), 16))
        return _JS_ESCAPE_MAP[match.group(0)]

    return _JS_ESCAPE.sub(repl, body)


def _translate_script_literals(rendered: str, tm: TranslationMemory) -> str:
    """Translate human-facing string literals embedded inside <script> blocks.

    ``_translate_html_document`` deliberately treats <script> as opaque so the
    BeautifulSoup text-node walker never mangles executable JS. But practice
    pages inline JS-object config (chapterTitle/lessonTitle), manual-completion
    status text, and JSON-LD SEO payloads directly as quoted string literals —
    those still need PL text. Any literal containing Cyrillic is human-facing
    (protected identifiers/paths/enum values in this codebase are all ASCII),
    so it is safe to run every such literal through the same translation
    memory used for visible prose, keyed on its unescaped content.
    """

    def translate_block(block_match: re.Match[str]) -> str:
        open_tag, body, close_tag = block_match.group(1), block_match.group(2), block_match.group(3)

        def translate_literal(lit_match: re.Match[str]) -> str:
            raw = lit_match.group(0)
            decoded = _decode_js_literal(raw)
            if not CYRILLIC.search(decoded):
                return raw
            stripped = decoded.strip()
            translated = _preserve_outer_space(decoded, tm.translate(stripped))
            # Re-escape "<" defensively (mirrors build_seo_meta.py's JSON-LD
            # payload escaping) so translated text can never be mistaken for
            # a closing </script> tag by an HTML parser.
            return json.dumps(translated, ensure_ascii=False).replace("<", "\\u003c")

        return open_tag + _JS_STRING_LITERAL.sub(translate_literal, body) + close_tag

    return _SCRIPT_BLOCK.sub(translate_block, rendered)


def _namespace_svg_ids(soup: BeautifulSoup) -> None:
    """Make inline-SVG fragment identifiers unique within the HTML page.

    The RU generators legitimately reuse short marker identifiers such as
    ``arrow`` in independent SVG elements.  HTML, unlike a standalone SVG,
    has one document-wide ID namespace.  BeautifulSoup also normalizes the
    original single-quoted attributes, exposing those collisions to the
    navigation validator.  Prefix every SVG-local ID and update its local
    references so fragment resolution remains deterministic.
    """
    for svg_index, svg in enumerate(soup.find_all("svg"), 1):
        replacements: dict[str, str] = {}
        for element in svg.find_all(id=True):
            old_id = element["id"]
            new_id = f"pl-svg-{svg_index}-{old_id}"
            element["id"] = new_id
            replacements[old_id] = new_id
        if not replacements:
            continue
        for element in svg.find_all(True):
            for attr, value in list(element.attrs.items()):
                if not isinstance(value, str):
                    continue
                for old_id, new_id in replacements.items():
                    value = value.replace(f"url(#{old_id})", f"url(#{new_id})")
                    if value == f"#{old_id}":
                        value = f"#{new_id}"
                element[attr] = value


def _translate_html_document(source: str, tm: TranslationMemory, ru_url: str,
                             route_map: dict[str, str]) -> str:
    soup = BeautifulSoup(source, "html.parser")
    if soup.html:
        soup.html["lang"] = "pl"

    for node in list(soup.find_all(string=True)):
        if isinstance(node, Comment) or node.parent is None or node.parent.name in SKIP_TEXT_PARENTS:
            continue
        value = str(node)
        if CYRILLIC.search(value):
            stripped = value.strip()
            node.replace_with(NavigableString(_preserve_outer_space(value, tm.translate(stripped))))

    for tag in soup.find_all(True):
        for attr in TRANSLATED_ATTRIBUTES:
            value = tag.get(attr)
            if isinstance(value, str) and CYRILLIC.search(value):
                tag[attr] = tm.translate(value)
        if tag.name == "meta" and tag.get("name") == "description":
            value = tag.get("content")
            if isinstance(value, str) and CYRILLIC.search(value):
                tag["content"] = tm.translate(value)

        for attr in ("href", "src"):
            value = tag.get(attr)
            if not isinstance(value, str) or value.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            raw_url = urlsplit(value)
            if raw_url.scheme or raw_url.netloc:
                # External references are locale-neutral.  Rewriting by path
                # alone would, for example, confuse git-scm.com's "/" with
                # the course homepage route.
                continue
            absolute = urljoin(ru_url, value)
            parsed = urlsplit(absolute)
            counterpart = route_map.get(parsed.path)
            if counterpart is None and parsed.path.endswith("/"):
                counterpart = route_map.get(parsed.path + "index.html")
            if counterpart:
                tag[attr] = counterpart + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
            elif parsed.path.startswith(("/assets/", "/book/", "/notebooks/", "/projects/")):
                tag[attr] = parsed.path + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")

    _namespace_svg_ids(soup)

    # PL publications are intentionally out of scope; label existing RU books.
    for anchor in soup.find_all("a", href=True):
        if anchor["href"].startswith("/book/") and "wersja rosyjska" not in anchor.get_text(" ", strip=True).lower():
            anchor.append(NavigableString(" — wersja rosyjska"))

    rendered = str(soup)
    # JS/JSON string literals embedded in <script> blocks (practice config
    # chapterTitle/lessonTitle, manual-completion status text, JSON-LD SEO
    # payloads) are opaque to the prose translator above; translate them here.
    rendered = _translate_script_literals(rendered, tm)
    # Their navigational URLs are still identity-based, not prose.
    for ru_path, pl_path in sorted(route_map.items(), key=lambda item: -len(item[0])):
        rendered = rendered.replace(f'"{ru_path}"', f'"{pl_path}"')
        rendered = rendered.replace(f"'{ru_path}'", f"'{pl_path}'")
    # Notebook and grader artifacts are locale-specific delivery resources;
    # they retain the same logical lesson/grader identity.
    rendered = rendered.replace('"/notebooks/', '"/pl/notebooks/')
    if not rendered.startswith("<!DOCTYPE"):
        rendered = "<!DOCTYPE html>\n" + rendered
    return rendered


_MARKDOWN_PROTECTED = re.compile(r"(`+[^`]*`+|https?://[^\s)>]+)")


def _translate_markdown(markdown: str, tm: TranslationMemory) -> str:
    output: list[str] = []
    fenced = False
    for line in markdown.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            output.append(line)
            continue
        if fenced or not CYRILLIC.search(line):
            output.append(line)
            continue
        pieces = _MARKDOWN_PROTECTED.split(line)
        for index in range(0, len(pieces), 2):
            value = pieces[index]
            if CYRILLIC.search(value):
                stripped = value.strip()
                if stripped:
                    pieces[index] = _preserve_outer_space(value, tm.translate(stripped))
        output.append("".join(pieces))
    return "".join(output)


def _translate_notebooks(tm: TranslationMemory) -> None:
    practice = _read_json(PRACTICE_MANIFEST)
    for practice_id, entry in sorted(practice.items()):
        source_path = ROOT / "notebooks" / entry["notebook"]
        target_path = PL_ROOT / "notebooks" / entry["notebook"]
        notebook = _read_json(source_path)
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "markdown":
                text = "".join(cell.get("source", []))
                translated = _translate_markdown(text, tm)
                translated = re.sub(
                    r"(?:\.\./)+site/chapters/glava-(\d{2})/",
                    r"/pl/chapters/rozdzial-\1/", translated,
                )
                translated = re.sub(r"(?:\.\./)+site/practice/", "/pl/practice/", translated)
                cell["source"] = translated.splitlines(keepends=True)
            elif cell.get("cell_type") == "code":
                lines = cell.get("source", [])
                translated_lines = []
                for line in lines:
                    match = re.match(r"^(\s*#\s*)(.*)$", line)
                    if match and CYRILLIC.search(match.group(2)) and not re.search(r"noqa|type:\s*ignore|pragma|doctest", line):
                        ending = "\n" if line.endswith("\n") else ""
                        translated_lines.append(match.group(1) + tm.translate(match.group(2).rstrip("\n")) + ending)
                    else:
                        translated_lines.append(line)
                cell["source"] = translated_lines
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _route_source(pair: PagePair) -> dict:
    source = {"locale": "ru", "path": pair.source_path}
    if pair.dependencies:
        source["dependencies"] = list(pair.dependencies)
    source["sha256"] = source_hash(source)
    return source


def _write_routes(pairs: list[PagePair]) -> None:
    pages = {}
    tm_rel = TM_PATH.relative_to(ROOT).as_posix()
    for pair in pairs:
        source = _route_source(pair)
        localized_source = {
            "front-matter-author": "manifest/i18n/content/pl/front-matter-author.json",
            "front-matter-license": "manifest/i18n/content/pl/front-matter-license.json",
        }.get(pair.page_id, tm_rel)
        page = {
            "source": source,
            "variants": {
                "ru": {"path": pair.ru_url, "status": "approved"},
                "pl": {
                    "path": pair.pl_url,
                    "status": "translated",
                    "source_sha256": source["sha256"],
                    "source_path": localized_source,
                    "evidence_path": None,
                },
            },
        }
        if pair.practice_id:
            page["practice_id"] = pair.practice_id
        if pair.project_id:
            page["project_id"] = pair.project_id
        pages[pair.page_id] = page
    ROUTES_PATH.write_text(json.dumps({"schema_version": 1, "pages": pages}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _polish_cleanup(value: str, source: str) -> str:
    replacements = {
        "Referencje": "Kompendium",
        "Odniesienia": "Kompendium",
        "Sekcja": "Rozdział",
        "Ćwiczenia": "Praktyka",
        "Rozdziałów": "Rozdziały",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    if re.search(r"строк", source, re.I):
        value = re.sub(r"\bciąg(?:iem|u|i|ów|ami)?(?:\s+znaków)?\b", "łańcuch znaków", value, flags=re.I)
    return value.replace('"', '„', 1).rsplit('"', 1)[0] + '”' if value.count('"') == 2 else value


def _chunks(text: str, limit: int = 420) -> list[str]:
    if len(text) <= limit:
        return [text]
    parts = re.split(r"(?<=[.!?])\s+", text)
    result: list[str] = []
    current = ""
    for part in parts:
        if current and len(current) + len(part) + 1 > limit:
            result.append(current)
            current = part
        else:
            current = f"{current} {part}".strip()
    if current:
        result.append(current)
    return result


def _translate_pending_offline(ru_model: Path, pl_model: Path) -> None:
    """Populate pending TM entries with deterministic greedy OPUS inference."""
    import ctranslate2
    import sentencepiece as spm
    from argostranslate.tokenizer import BPETokenizer

    data = _read_json(TM_PATH)
    sources = data.get("sources", {})
    pending = [(key, source) for key, source in sources.items() if not data["entries"].get(key)]
    if not pending:
        print("Translation memory has no pending entries")
        return

    ru_tokenizer = spm.SentencePieceProcessor(model_file=str(ru_model / "sentencepiece.model"))
    pl_tokenizer = BPETokenizer(pl_model / "bpe.model", "en", "pl")
    ru_translator = ctranslate2.Translator(str(ru_model / "model"), device="cpu", compute_type="int8")
    pl_translator = ctranslate2.Translator(str(pl_model / "model"), device="cpu", compute_type="int8")

    work: list[tuple[str, str, int, str]] = []
    counts: dict[str, int] = {}
    for key, source in pending:
        chunks = _chunks(source)
        counts[key] = len(chunks)
        work.extend((key, source, index, chunk) for index, chunk in enumerate(chunks))
    results: dict[str, list[str]] = {key: [""] * count for key, count in counts.items()}

    batch_size = 64
    for offset in range(0, len(work), batch_size):
        batch = work[offset:offset + batch_size]
        ru_tokens = [ru_tokenizer.encode(item[3], out_type=str) for item in batch]
        english_results = ru_translator.translate_batch(ru_tokens, beam_size=1)
        english = [ru_tokenizer.decode(item.hypotheses[0]) for item in english_results]
        pl_tokens = [pl_tokenizer.encode(item) for item in english]
        polish_results = pl_translator.translate_batch(pl_tokens, beam_size=1)
        polish = [pl_tokenizer.decode(item.hypotheses[0]) for item in polish_results]
        for item, translated in zip(batch, polish, strict=True):
            key, source, index, _ = item
            results[key][index] = _polish_cleanup(translated, source)
        if offset % (batch_size * 20) == 0:
            print(f"Translated {min(offset + batch_size, len(work))}/{len(work)} chunks", flush=True)

    for key, source in pending:
        data["entries"][key] = " ".join(results[key]).strip()
    data["entries"] = dict(sorted(data["entries"].items()))
    # Retain the exact canonical RU key material for traceability and future
    # stale/diff review; production generation reads only ``entries``.
    TM_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Filled {len(pending)} translation-memory entries")


_BINDING_SOURCE_TERMS = {
    "Практические задания": "Ćwiczenia",
    "практические задания": "ćwiczenia",
    "практическое задание": "ćwiczenie",
    "область видимости": "zasięg",
    "Справочник": "Kompendium",
    "Главы": "Rozdziały",
    "Глава": "Rozdział",
    "Практика": "Praktyka",
    "упражнение": "ćwiczenie",
    "переменная": "zmienna",
    "строка": "łańcuch znaków",
    "список": "lista",
    "словарь": "słownik",
    "множество": "zbiór",
    "исключение": "wyjątek",
}
_LATIN_LITERAL = re.compile(r"[A-Za-z_][A-Za-z0-9_.+/#():\[\]-]*")


def _mask_protected(source: str) -> tuple[str, dict[str, str]]:
    """Protect binding terms and all Latin technical literals from NMT drift."""
    spans: list[tuple[int, int, str]] = []
    occupied: list[tuple[int, int]] = []
    for term, target in sorted(_BINDING_SOURCE_TERMS.items(), key=lambda item: -len(item[0])):
        for match in re.finditer(re.escape(term), source):
            if any(match.start() < end and match.end() > start for start, end in occupied):
                continue
            spans.append((match.start(), match.end(), target))
            occupied.append((match.start(), match.end()))
    for match in _LATIN_LITERAL.finditer(source):
        if any(match.start() < end and match.end() > start for start, end in occupied):
            continue
        spans.append((match.start(), match.end(), match.group(0)))
        occupied.append((match.start(), match.end()))
    replacements: dict[str, str] = {}
    masked = source
    for index, (start, end, target) in enumerate(sorted(spans, reverse=True)):
        token = f"ZXQ{index}ZXQ"
        replacements[token] = target
        masked = masked[:start] + token + masked[end:]
    return masked, replacements


def _translate_all_m2m(model: Path) -> None:
    """Replace every TM target using direct RU->PL M2M-100 inference."""
    import ctranslate2
    import sentencepiece as spm

    data = _read_json(TM_PATH)
    processor = spm.SentencePieceProcessor(model_file=str(model / "sentencepiece.model"))
    translator = ctranslate2.Translator(str(model / "model"), device="cpu", compute_type="int8")
    work: list[tuple[str, str, int, str, dict[str, str]]] = []
    counts: dict[str, int] = {}
    for key, source in sorted(data["sources"].items()):
        chunks = _chunks(source)
        counts[key] = len(chunks)
        for index, chunk in enumerate(chunks):
            masked, replacements = _mask_protected(chunk)
            work.append((key, source, index, masked, replacements))
    results: dict[str, list[str]] = {key: [""] * count for key, count in counts.items()}

    batch_size = 64
    for offset in range(0, len(work), batch_size):
        batch = work[offset:offset + batch_size]
        tokens = [["__ru__", *processor.encode(item[3], out_type=str)] for item in batch]
        translated = translator.translate_batch(
            tokens, target_prefix=[["__pl__"] for _ in tokens], beam_size=1,
        )
        for item, result in zip(batch, translated, strict=True):
            key, source, index, _, replacements = item
            target_tokens = result.hypotheses[0]
            if target_tokens and target_tokens[0] == "__pl__":
                target_tokens = target_tokens[1:]
            target = processor.decode(target_tokens)
            for token, literal in replacements.items():
                target = target.replace(token, literal)
            results[key][index] = _polish_cleanup(target, source)
        if offset % (batch_size * 20) == 0:
            print(f"Translated {min(offset + batch_size, len(work))}/{len(work)} direct chunks", flush=True)

    for key, source in data["sources"].items():
        data["entries"][key] = " ".join(results[key]).strip()
    data["entries"] = dict(sorted(data["entries"].items()))
    TM_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Replaced {len(results)} targets with direct RU->PL translations")


def _bing_config() -> tuple[str, str, int, str]:
    import requests

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150 Safari/537.36 Edg/151"
    response = requests.get("https://www.bing.com/translator", headers={"user-agent": user_agent}, timeout=30)
    response.raise_for_status()
    ig = re.search(r'IG:"([^"]+)"', response.text)
    iid = re.search(r'data-iid="([^"]+)"', response.text)
    abuse = re.search(r'params_AbusePreventionHelper\s?=\s?([^\]]+\])', response.text)
    if not ig or not iid or not abuse:
        raise RuntimeError("Bing translator bootstrap contract changed")
    key, token, _ = json.loads(abuse.group(1))
    return ig.group(1), iid.group(1), key, token


def _bing_request(config: tuple[str, str, int, str], batch_id: int, text: str) -> str:
    import requests

    ig, iid, key, token = config
    url = ("https://www.bing.com/ttranslatev3?isVertical=1&"
           f"&IG={ig}&IID={iid}&SFX={batch_id + 1}&ref=TThis&edgepdftranslator=1")
    body = {
        "fromLang": "ru", "to": "pl", "text": text, "key": key, "token": token,
        "tryFetchingGenderDebiasedTranslations": "true",
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150 Safari/537.36 Edg/151",
        "referer": "https://www.bing.com/translator",
    }
    for attempt in range(5):
        response = requests.post(url, data=body, headers=headers, timeout=60)
        if response.ok:
            payload = response.json()
            return payload[0]["translations"][0]["text"]
        if response.status_code not in {429, 500, 502, 503, 504}:
            response.raise_for_status()
        time.sleep(2 ** attempt)
    raise RuntimeError(f"Bing translation failed after retries: HTTP {response.status_code}")


def _translate_all_bing(workers: int) -> None:
    """Replace every TM target with direct RU->PL Bing translations.

    This maintainer-only resource operation is networked; production builds
    consume the committed result and never call the service.
    """
    data = _read_json(TM_PATH)
    units: list[tuple[str, str, int, str, dict[str, str]]] = []
    counts: dict[str, int] = {}
    for key, source in sorted(data["sources"].items()):
        chunks = _chunks(source, limit=700)
        counts[key] = len(chunks)
        for index, chunk in enumerate(chunks):
            masked, replacements = _mask_protected(chunk)
            units.append((key, source, index, masked, replacements))

    batches: list[list[tuple[str, str, int, str, dict[str, str]]]] = []
    current: list[tuple[str, str, int, str, dict[str, str]]] = []
    size = 0
    for unit in units:
        marker_cost = 28
        if current and size + len(unit[3]) + marker_cost > 2400:
            batches.append(current)
            current = []
            size = 0
        current.append(unit)
        size += len(unit[3]) + marker_cost
    if current:
        batches.append(current)

    config = _bing_config()
    results: dict[str, list[str]] = {key: [""] * count for key, count in counts.items()}

    def run_batch(batch_id: int, batch: list[tuple[str, str, int, str, dict[str, str]]]):
        request = "\n".join(f"ZXQSEG{index:04d}ZXQ {unit[3]}" for index, unit in enumerate(batch))
        response = _bing_request(config, batch_id, request)
        matches = list(re.finditer(r"ZXQSEG(\d{4})ZXQ\s*", response))
        translated: dict[int, str] = {}
        for position, match in enumerate(matches):
            start = match.end()
            end = matches[position + 1].start() if position + 1 < len(matches) else len(response)
            translated[int(match.group(1))] = response[start:end].strip()
        if len(translated) != len(batch):
            # The service can occasionally merge two short labelled lines.
            # Retry this one batch as independent units; no ambiguous output
            # is ever accepted into the canonical resource.
            translated = {
                index: _bing_request(config, batch_id * 1000 + index + 1, unit[3])
                for index, unit in enumerate(batch)
            }
        return batch_id, [(unit, translated[index]) for index, unit in enumerate(batch)]

    complete = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_batch, batch_id, batch): batch_id
                   for batch_id, batch in enumerate(batches)}
        for future in as_completed(futures):
            _, translations = future.result()
            for unit, target in translations:
                key, source, index, _, replacements = unit
                for token, literal in replacements.items():
                    target = target.replace(token, literal)
                results[key][index] = _polish_cleanup(target, source)
            complete += 1
            if complete % 25 == 0 or complete == len(batches):
                print(f"Translated {complete}/{len(batches)} network batches", flush=True)

    for key, source in data["sources"].items():
        data["entries"][key] = " ".join(results[key]).strip()
    data["entries"] = dict(sorted(data["entries"].items()))
    TM_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Replaced {len(results)} targets with direct RU->PL translations")


def _normalize_target(source: str, target: str) -> str:
    exact = {
        "О курсе": "O kursie",
        "Главы": "Rozdziały",
        "Практика": "Praktyka",
        "Проекты": "Projekty",
        "Справочник": "Kompendium",
        "Предметный указатель": "Indeks rzeczowy",
        "Введение": "Wprowadzenie",
        "Об авторе": "O autorze",
        "О техническом рецензенте": "O recenzencie technicznym",
        "Среда выполнения и CLI": "Środowisko wykonawcze i CLI",
        "Официальные ресурсы Python": "Oficjalne zasoby Pythona",
        "Лицензия": "Licencja",
        '# ввод: "  ада  " / "ЛАВЛЕЙС"': '# wejście: "  ada  " / "LOVELACE"',
    }
    if source in exact:
        return exact[source]
    replacements = {
        "Szkoła Kartezjańska": "Cartesian School",
        "Cartesian szkoła": "Cartesian School",
        "Tkliner": "Tkinter",
        "Tkiner": "Tkinter",
    }
    for old, new in replacements.items():
        target = target.replace(old, new)
    return _polish_cleanup(target, source)


def _repair_translation_memory_bing(workers: int) -> None:
    """Retranslate only records where a protected marker was damaged."""
    data = _read_json(TM_PATH)
    broken = [
        (key, data["sources"][key]) for key, target in data["entries"].items()
        if (not target or CYRILLIC.search(target)
            or re.search(r"Z(?:XQ|HK|HQ|HК|KQ|Х|ХQ|ХК)", target, re.I))
    ]
    config = _bing_config()

    def repair(index_item: tuple[int, tuple[str, str]]) -> tuple[str, str, str]:
        index, (key, source) = index_item
        return key, source, _bing_request(config, 100000 + index, source)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        repaired = list(executor.map(repair, enumerate(broken)))
    for key, source, target in repaired:
        data["entries"][key] = _normalize_target(source, target)
    for key, source in data["sources"].items():
        data["entries"][key] = _normalize_target(source, data["entries"][key])
    TM_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Repaired {len(broken)} damaged translation records")


def build(*, collect: bool) -> None:
    pairs = page_pairs()
    route_map = {pair.ru_url: pair.pl_url for pair in pairs}
    if PL_ROOT.exists():
        shutil.rmtree(PL_ROOT)
    tm = TranslationMemory(collect=collect)
    for index, pair in enumerate(pairs, 1):
        translated = _translate_html_document(
            pair.ru_file.read_text(encoding="utf-8"), tm, pair.ru_url, route_map,
        )
        pair.pl_file.parent.mkdir(parents=True, exist_ok=True)
        pair.pl_file.write_text(translated, encoding="utf-8")
        if index % 100 == 0:
            print(f"Processed {index}/{len(pairs)} pages")
    _translate_notebooks(tm)
    if collect:
        tm.save_pending()
        print(f"Collected {len(tm.missing)} missing source strings in {TM_PATH.relative_to(ROOT)}")
        return
    _write_routes(pairs)
    print(f"Built {len(pairs)} Polish pages and 493 localized notebooks")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--translate-offline", action="store_true")
    parser.add_argument("--translate-m2m", action="store_true")
    parser.add_argument("--translate-bing", action="store_true")
    parser.add_argument("--repair-bing", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--ru-model", type=Path)
    parser.add_argument("--pl-model", type=Path)
    args = parser.parse_args()
    if args.repair_bing:
        _repair_translation_memory_bing(args.workers)
    elif args.translate_bing:
        _translate_all_bing(args.workers)
    elif args.translate_m2m:
        if not args.model:
            parser.error("--translate-m2m requires --model")
        _translate_all_m2m(args.model)
    elif args.translate_offline:
        if not args.ru_model or not args.pl_model:
            parser.error("--translate-offline requires --ru-model and --pl-model")
        _translate_pending_offline(args.ru_model, args.pl_model)
    else:
        build(collect=args.collect)


if __name__ == "__main__":
    main()
