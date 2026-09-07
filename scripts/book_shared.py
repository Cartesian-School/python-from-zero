#!/usr/bin/env python3
"""Locale-agnostic helpers shared by the RU and PL book (EPUB/PDF) builders.

Every function here operates purely on DOM structure (tag names, class
markers) rather than on any language-specific text, so the same code
produces correct output for both site/ (RU) and site/pl/ (PL) source trees.
The RU-only and PL-only entry points (build_epub.py/build_epub_pl.py,
build_pdf.py/build_pdf_pl.py) each supply their own locale-specific config
(titles, front matter lists, chapter/page discovery, rights notice text,
output paths) and call into this module for the mechanical parts: content
extraction, link rewriting, SVG repair, EPUB packaging/determinism, and PDF
anchor/pagination bookkeeping.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from importlib.metadata import version
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from ebooklib import epub

ROOT = Path(__file__).resolve().parent.parent
BOOK_FONT_DIR = ROOT / "book" / "fonts"
FONTCONFIG_POLICY_PATH = BOOK_FONT_DIR / "pdf-fontconfig.conf"

# Reproducible-builds timestamp boundary: FontTools reads SOURCE_DATE_EPOCH
# when serializing embedded font subsets (notably Noto Color Emoji), so two
# otherwise-identical renders would otherwise embed different bytes.
PDF_SOURCE_DATE_EPOCH = "0"

FONTCONFIG_POLICY_SHA256 = (
    "57e99dae5e8f972aa80f477a539913f2a39804ed7607553072a87e38d82cbaff"
)

# Both books (RU and PL) share the exact same embedded font set: DejaVu Serif
# covers Polish diacritics (ą ć ę ł ń ó ś ź ż) as well as Cyrillic, so no
# locale-specific font is required.
EMOJI_FONT_FILE = "noto-emoji/NotoColorEmoji-subset.ttf"
EMOJI_FONT_FAMILY = "Cartesian Noto Color Emoji"
EMOJI_CODEPOINTS = frozenset(
    {
        0x2139,
        0x26A0,
        0x26D4,
        0x2705,
        0x274C,
        0x1F36C,
        0x1F381,
        0x1F388,
        0x1F389,
        0x1F40D,
        0x1F4C4,
        0x1F4DA,
        0x1F536,
    }
)
PDF_FONT_FILES = {
    "dejavu/DejaVuSerif.ttf": "8cb29f7db250ebb2551a6ce2c1e0bfd5a0eb520e9e233370db0493e82e1f36f7",
    "dejavu/DejaVuSerif-Bold.ttf": "aac3f559445d23f0f567a243f91f3f6ad6cb4b5cafa1521a3479fffe0637f0bd",
    "dejavu/DejaVuSerif-Italic.ttf": "d843bf414381dd64b89e6c7c954075657b74168521f02b30e11d308558eda1d2",
    "dejavu/DejaVuSerif-BoldItalic.ttf": "ed336a3d81f5a2d6a3d12c16dda400b28ba7304792254fc9e96c0d6835fbeab2",
    "dejavu/DejaVuSans.ttf": "57f73e11f51999432bf7ab22ce55b6f945d5eca1bf824404cfa9ec2e3718c84e",
    "dejavu/DejaVuSans-Bold.ttf": "a4c5bc453ca281d90ea079e596da7ae0dfeb5777497c29ec254e76d97ff6f890",
    "dejavu/DejaVuSans-Oblique.ttf": "e2f09289f4276309a36b9a93e5a0ac64957ef3eb7158151b243d41f667151ee4",
    "dejavu/DejaVuSansMono.ttf": "54bf827eb99404e8f430c330ad30f063334f637eba0109b6a18d4f566a8e9dd8",
    "dejavu/DejaVuSansMono-Bold.ttf": "0d3c03d1b667192f91223660a3163325cf83132662fe4d9f7d6e596bf7a995c2",
    EMOJI_FONT_FILE: "294f31aa8ea76e2d7e1df7f5035f04c07f777a5b7e2d2507a28719aebbff2c8a",
}

# Mirrors theory.css's :root primitives — see build_pdf.py for provenance.
# Needed because WeasyPrint's (and most e-reader engines') SVG renderer does
# not reliably resolve CSS custom properties referenced inside SVG
# presentation attributes (e.g. stop-color="var(--navy-950)") the way a
# browser does. Shared verbatim between RU and PL since diagram markup and
# its color tokens are identical in both locales (only text nodes differ).
SVG_COLOR_TOKENS = {
    "navy-950": "#08011C", "navy-900": "#0D0230", "navy-800": "#15104A",
    "violet-300": "#B9A0FC", "violet-400": "#8355FA", "violet-500": "#5B24F9",
    "blue-300": "#8FB7FE", "blue-500": "#185DFA", "blue-600": "#0C43F1",
    "white": "#FFFFFF", "offwhite": "#FAFAFC",
    "gray-100": "#F2F2F6", "gray-200": "#E4E4EC", "gray-400": "#B4B4C4",
    "gray-600": "#6B6B7D", "gray-800": "#2B2B3D",
    "amber-500": "#F59E0B", "red-500": "#EF4444", "green-500": "#22C55E",
}

# BeautifulSoup's "lxml" parser is libxml2's plain HTML parser, not an HTML5
# parser — it doesn't implement the HTML5 spec's "adjust SVG tag names" step
# that restores camelCase for foreign (SVG) content, so it silently
# lowercases every element/attribute name. Real browsers correct this
# automatically; WeasyPrint (and EPUB e-readers) don't.
_SVG_CASE_FIXES = {"lineargradient": "linearGradient", "viewbox": "viewBox", "preserveaspectratio": "preserveAspectRatio"}


def fix_svg_case(html_fragment: str) -> str:
    if "<svg" not in html_fragment:
        return html_fragment
    for wrong, right in _SVG_CASE_FIXES.items():
        html_fragment = re.sub(rf"<{wrong}(?=[ >])", f"<{right}", html_fragment)
        html_fragment = re.sub(rf"</{wrong}>", f"</{right}>", html_fragment)
        html_fragment = re.sub(rf"\b{wrong}=", f"{right}=", html_fragment)
    return html_fragment


def resolve_svg_css_vars(html_fragment: str) -> str:
    if "<svg" not in html_fragment:
        return html_fragment
    html_fragment = re.sub(
        r"var\(--([a-z0-9-]+)\)",
        lambda m: SVG_COLOR_TOKENS.get(m.group(1), m.group(0)),
        html_fragment,
    )
    return fix_svg_case(html_fragment)


def extract_page_title(html_text: str) -> str:
    """Return a page's own displayed title straight from its rendered <h1>.

    Locale-agnostic: lets a language edition whose pages have no separate
    canonical-metadata source of truth (e.g. PL, a machine-translated mirror
    of the RU site) derive TOC/spine labels from what a reader actually sees
    on the page, instead of maintaining a second, independently authored
    title list that could drift from the real page content.
    """
    soup = BeautifulSoup(html_text, "lxml")
    hero_h1 = soup.select_one(".chapter-hero h1")
    if hero_h1:
        return hero_h1.get_text(strip=True)
    article_h1 = soup.select_one("article h1")
    if article_h1:
        return article_h1.get_text(strip=True)
    any_h1 = soup.find("h1")
    if any_h1:
        return any_h1.get_text(strip=True)
    raise RuntimeError("no <h1> found to derive a page title")


def rewrite_links(tag, *, site_origin: str) -> None:
    """Point package-external links at the real production site.

    Notebooks, project source files, and interactive /practice/ pages live
    outside the EPUB/PDF package (on the live site or in the git repo), so a
    package-relative link to them would be dead. hrefs from theory pages are
    site-relative ("../../practice/03-01/..."); hrefs from project detail
    pages are root-relative ("/practice/03-01/..."). Both are normalized to
    the same absolute production URL by locating a known top-level-directory
    marker inside the href and treating everything from there on as the
    site-root-relative path — this also correctly tolerates a source href
    with more ``../`` segments than its own page depth actually requires (a
    real, tolerated pattern in this site's generated HTML that a strict
    urljoin-based resolution would silently truncate).

    A PL href already carries its own "/pl" prefix before the marker
    (build_polish_course.py resolves internal PL links to locale-correct
    absolute paths before this ever runs) — that prefix is preserved so the
    PL book still links into the PL site, not the RU one.
    """
    for a in list(tag.find_all("a", href=True)):
        href = a["href"]
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        marker = next((m for m in ("/notebooks/", "/projects/", "/practice/", "/chapters/") if m in href), None)
        if marker is not None:
            locale_prefix = "/pl" if href.startswith("/pl/") else ""
            site_relative_path = locale_prefix + marker + href.split(marker, 1)[1]
            a["href"] = site_origin + site_relative_path
            continue
        if ".html" in href:
            a["href"] = href.replace(".html", ".xhtml")


def extract_article(html_text: str, *, site_origin: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    article = soup.find("article")
    for cls in ("breadcrumb", "section-kicker", "section-nav"):
        node = article.find("div", class_=cls)
        if node:
            node.decompose()
    # Web-only richer presentation (e.g. the front-matter author page's
    # portrait hero, domain grid, and project list) that would shift accepted
    # PDF/EPUB pagination if included.
    for node in article.find_all(class_="web-presentation"):
        node.decompose()
    for btn in article.find_all("button", class_="copy-btn"):
        btn.decompose()
    # practice_card()/local_required_card() append a small inline <script>
    # that reads localStorage to show live completion status — meaningless
    # (and inert) outside a browser, and would otherwise flag the package as
    # containing script.
    for script in article.find_all("script"):
        script.decompose()
    rewrite_links(article, site_origin=site_origin)
    inner = "".join(str(c) for c in article.contents)
    return resolve_svg_css_vars(f"<html><body>{inner}</body></html>")


def extract_opener(html_text: str, *, site_origin: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    hero = soup.find("div", class_="chapter-hero")
    section_list = soup.find("div", class_="section-list")
    if section_list:
        for script in section_list.find_all("script"):
            script.decompose()
        rewrite_links(section_list, site_origin=site_origin)
    inner = (str(hero) if hero else "") + (str(section_list) if section_list else "")
    return resolve_svg_css_vars(f"<html><body>{inner}</body></html>")


def extract_project(html_text: str, *, site_origin: str) -> str:
    """Extract the stable project fragment used by the accepted publication.

    Project pages embed ``.project-hero`` and ``.project-detail-body`` inside
    an inert publication-source template. Its factual title, description,
    topics, and source path originate from the canonical project manifest
    rather than an independently authored book copy.
    """
    soup = BeautifulSoup(html_text, "lxml")
    hero = soup.find("div", class_="project-hero")
    body = soup.find("div", class_="project-detail-body")
    if body:
        for cls in ("breadcrumb", "section-nav"):
            node = body.find(["div", "p"], class_=cls)
            if node:
                node.decompose()
        for script in body.find_all("script"):
            script.decompose()
        rewrite_links(body, site_origin=site_origin)
    inner = (str(hero) if hero else "") + (str(body) if body else "")
    return resolve_svg_css_vars(f"<html><body>{inner}</body></html>")


# M02-I07 Phase 2B: a code block only fragments across a physical page if it
# carries this class (see the print CSS's `.code-block--splittable` rule).
# 18 physical source lines was chosen, not guessed: an audit of every
# .code-block across the RU chapter corpus (1,458 blocks) found the
# distribution 1-5 lines: 841 (57.7%), 6-10: 338 (23.2%), 11-15: 153 (10.5%),
# 16-18: 52 (3.6%), 19-25: 38 (2.6%), 26-40: 28 (1.9%), 41+: 8 (0.5%) — i.e.
# roughly 94.9% of all code blocks are 18 lines or shorter and keep
# `break-inside: avoid` completely untouched. Only the long tail (5.1%, 74
# blocks) — genuinely long listings where forcing the whole block onto one
# page is what causes the trailing-whitespace waste Phase 2A measured — may
# split. This sits at the conservative (safer, fewer blocks affected) end of
# the 16-18 range the M02-I07 Phase 2B ticket specified.
CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD = 18
_CODE_BLOCK_SPLITTABLE_CLASS = "code-block--splittable"


def classify_splittable_code_blocks(
    content: str, *, threshold: int = CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD
) -> str:
    """Tag every ``.code-block`` whose ``<pre><code>`` content spans more than
    ``threshold`` physical source lines with ``code-block--splittable``,
    leaving every shorter block's markup (and its default ``break-inside:
    avoid``) completely untouched.

    Applied once during canonical page normalization (book_pipeline.model),
    so it runs identically for every language and both publication formats
    — the classification decision itself never looks at ``language``, only
    at the code block's own text content. It is inert for EPUB: EPUB's own
    stylesheet (site/assets/css/theory.css) defines no rule for this class,
    so the added attribute has no visual effect there; only the PDF print
    stylesheet's ``.code-block--splittable`` rule (see
    book_shared.build_print_css) acts on it.

    Source-line count is a PROXY for a code block's rendered physical
    height, not the height itself: a single very long logical line that
    wraps substantially under the print column's ``word-break: break-word``
    can span several physical rows while still counting as "1 line" here.
    This is a known, accepted limitation for this pass — see the M02-I07
    Phase 2B evidence report's visual-QA findings for whether it produced
    any observable mis-classification in practice.
    """
    if "code-block" not in content:
        return content
    soup = BeautifulSoup(content, "lxml")
    changed = False
    for block in soup.find_all("div", class_="code-block"):
        code_element = block.find("code")
        if code_element is None:
            continue
        text = code_element.get_text()
        line_count = text.count("\n") + 1 if text.strip() else 0
        if line_count > threshold:
            classes = block.get("class", [])
            if _CODE_BLOCK_SPLITTABLE_CLASS not in classes:
                block["class"] = [*classes, _CODE_BLOCK_SPLITTABLE_CLASS]
                changed = True
    if not changed:
        return content
    body = soup.find("body")
    inner = "".join(str(c) for c in body.contents) if body else str(soup)
    return f"<html><body>{inner}</body></html>"


def strip_wrapper(content: str) -> str:
    return content[len("<html><body>"):-len("</body></html>")]


def printify_notebook_cards(inner_html: str) -> str:
    """Un-hide the notebook/practice reference card for print and append the
    plain-text URL next to the link, since a physical page can't be clicked."""
    if "notebook-card" not in inner_html:
        return inner_html
    soup = BeautifulSoup(inner_html, "lxml")
    for card in soup.find_all("div", class_="notebook-card"):
        btn = card.find("a", class_="nc-btn")
        if btn and btn.get("href"):
            url_span = soup.new_tag("span")
            url_span["class"] = "nc-url"
            url_span.string = f" ({btn['href']})"
            btn.insert_after(url_span)
    body = soup.find("body")
    return "".join(str(c) for c in body.contents) if body else str(soup)


def printify_opener(inner_html: str, num: int, marker_id: str, *, chapter_label: str) -> str:
    """Make the opener's page labels depend only on the print page counter.

    Website opener labels are generated from the previous PDF build. Keeping
    them in the render input would create a metadata/layout cycle. The print
    edition therefore removes those labels before layout and obtains its
    chapter folio from CSS ``counter(page)`` on the final rendered page.
    ``chapter_label`` is the locale's own "Chapter N" string (e.g. "ГЛАВА 3"
    / "ROZDZIAŁ 3").
    """
    soup = BeautifulSoup(inner_html, "lxml")
    hero = soup.select_one(".chapter-hero")
    if hero is None:
        raise RuntimeError(f"chapter {num}: opener has no .chapter-hero")
    hero["id"] = marker_id
    chapter_num = soup.select_one(".chapter-num")
    if chapter_num is None:
        raise RuntimeError(f"chapter {num}: opener has no .chapter-num")
    chapter_num.clear()
    chapter_num.string = chapter_label
    for page_label in soup.select(".si-page"):
        page_label.decompose()
    body = soup.find("body")
    return "".join(str(c) for c in body.contents) if body else str(soup)


def resolve_anchor_pages(doc, marker_ids: set[str]) -> dict[str, int]:
    """Return first one-based WeasyPrint page occupied by each marked element.

    WeasyPrint repeats an element anchor in ``page.anchors`` when the marked
    wrapper spans more than one physical page. The first occurrence is the
    target-counter destination and therefore the authoritative start page.
    """
    resolved: dict[str, int] = {}
    for page_index, page in enumerate(doc.pages, start=1):
        for marker_id in marker_ids.intersection(page.anchors):
            resolved.setdefault(marker_id, page_index)
    missing = marker_ids.difference(resolved)
    if missing:
        raise RuntimeError(f"PDF render lost anchors: {', '.join(sorted(missing))}")
    return resolved


def merge_cover(content_pdf_path: Path, cover_pdf_path: Path, out_path: Path) -> None:
    """Prepends an already-approved cover design as the literal first
    physical page. The cover is unnumbered, matching normal book convention.

    Uses PdfWriter.append() (not per-page add_page()) specifically so the PDF
    outline/bookmarks WeasyPrint auto-generates from headings survive the
    merge — append() re-targets outline destinations to the new page
    indices; add_page() only copies page content, silently dropping the
    outline tree.
    """
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter()
    content_reader = PdfReader(str(content_pdf_path))

    cover_reader = PdfReader(str(cover_pdf_path))
    cover_page = cover_reader.pages[0]
    target_w = float(content_reader.pages[0].mediabox.width)
    target_h = float(content_reader.pages[0].mediabox.height)
    cover_page.scale_to(target_w, target_h)
    writer.append(cover_reader)

    writer.append(content_reader, import_outline=True)

    if content_reader.metadata:
        writer.add_metadata(content_reader.metadata)

    with open(out_path, "wb") as f:
        writer.write(f)


class CaseSafeEpubHtml(epub.EpubHtml):
    """Preserve case-sensitive SVG names after EbookLib serializes XHTML.

    EbookLib parses ``EpubHtml.content`` with lxml's HTML parser inside
    :meth:`EpubHtml.get_content`. That second HTML parse happens after our
    normalizer and lowercases SVG foreign-content names again. XHTML readers
    treat ``viewBox`` and related SVG names as case-sensitive, so applying
    the repair only before assigning ``item.content`` is insufficient:
    diagrams fall back to SVG's 300x150 default viewport and are visibly
    clipped.
    """

    def get_content(self, default=None) -> bytes:
        serialized = super().get_content(default)
        if not serialized:
            return serialized
        return fix_svg_case(serialized.decode("utf-8")).encode("utf-8")


def ncx_id(file_name: str) -> str:
    """XML NCName-safe id for use in toc.ncx (no '/' or '.')."""
    return "nav_" + file_name.replace("/", "_").replace(".", "_")


def literalize_pseudotags(soup: BeautifulSoup) -> None:
    """Repair traceback/URL literals that permissive HTML parsed as elements."""
    for code in soup.find_all(["code", "pre"]):
        for tag in list(code.find_all("module")):
            tag.insert_before(NavigableString("<module>"))
            tag.unwrap()
        for tag in list(code.find_all("class")):
            type_name = next(iter(tag.attrs), "object")
            tag.insert_before(NavigableString(f"<class {type_name}>"))
            tag.unwrap()
        for tag in list(code.find_all("svg")):
            tag.replace_with(NavigableString(str(tag)))
    for tag in list(soup.find_all("id")):
        tag.replace_with(NavigableString("<id>"))


def namespace_and_uniquify_svg(soup: BeautifulSoup) -> None:
    for svg_index, svg in enumerate(soup.find_all("svg"), start=1):
        svg["xmlns"] = "http://www.w3.org/2000/svg"
        replacements: dict[str, str] = {}
        for node in svg.find_all(id=True):
            old_id = node["id"]
            new_id = f"epub-{svg_index}-{old_id}"
            node["id"] = new_id
            replacements[old_id] = new_id
        if not replacements:
            continue
        for node in svg.find_all(True):
            for attribute, value in list(node.attrs.items()):
                if not isinstance(value, str):
                    continue
                for old_id, new_id in replacements.items():
                    value = value.replace(f"url(#{old_id})", f"url(#{new_id})")
                    if value == f"#{old_id}":
                        value = f"#{new_id}"
                node[attribute] = value
    for math in soup.find_all("math"):
        math["xmlns"] = "http://www.w3.org/1998/Math/MathML"


# CSS3-level parser rejects :has() as CSS-008; neither rule means anything in
# an e-reader anyway since the EPUB has no JS-driven mobile-nav drawer for it
# to react to.
_HAS_SELECTOR_RULE_RE = re.compile(r"[^{};]*:has\([^)]*\)[^{};]*\{[^{}]*\}")


def strip_has_selector_rules(css_text: str) -> str:
    return _HAS_SELECTOR_RULE_RE.sub("", css_text)


def normalize_epub_content(
    content: str,
    rel_html_path: str,
    included_paths: frozenset[str],
    *,
    site_origin: str,
    output_xhtml_path: str | None = None,
) -> str:
    """Convert permissive site HTML to deterministic, self-contained XHTML.

    ``included_paths`` is the locale's own set of site-root-relative HTML
    paths bundled inside the package (so an internal cross-reference resolves
    to a relative in-package link, while anything else becomes an absolute
    production URL).
    """
    import posixpath

    soup = BeautifulSoup(content, "lxml")
    literalize_pseudotags(soup)
    for caption in soup.find_all("figcaption"):
        if caption.find_parent("figure") is None:
            caption.name = "p"
            caption["class"] = [*caption.get("class", []), "figcaption"]
    namespace_and_uniquify_svg(soup)

    current_xhtml = output_xhtml_path or (
        rel_html_path.removesuffix(".html") + ".xhtml"
    )
    depth = current_xhtml.count("/")
    asset_prefix = "../" * depth
    for node in soup.find_all(True):
        for attribute in ("src", "href", "xlink:href"):
            value = node.get(attribute)
            if isinstance(value, str) and value.startswith("/assets/"):
                node[attribute] = asset_prefix + value.lstrip("/")

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        href_without_fragment, separator, fragment = href.partition("#")
        if not href_without_fragment.endswith((".html", ".xhtml")):
            continue
        resolved = posixpath.normpath(
            posixpath.join(posixpath.dirname(rel_html_path), href_without_fragment)
        ).lstrip("/")
        resolved_html = re.sub(r"\.xhtml$", ".html", resolved)
        if resolved_html in included_paths:
            target_xhtml = resolved_html.removesuffix(".html") + ".xhtml"
            relative = posixpath.relpath(
                target_xhtml, start=posixpath.dirname(current_xhtml) or "."
            )
            anchor["href"] = relative + (separator + fragment if separator else "")
        else:
            anchor["href"] = (
                f"{site_origin}/{resolved_html}" + (separator + fragment if separator else "")
            )

    body = soup.find("body")
    normalized = "".join(str(child) for child in body.contents) if body else str(soup)
    return resolve_svg_css_vars(f"<html><body>{normalized}</body></html>")


def normalize_epub_zip_determinism(path: Path, mtime) -> None:
    """Repack the just-written EPUB so its ZIP container is reproducible.

    ebooklib's own writer only fixes <meta property="dcterms:modified">
    inside the OPF — the ZIP entries themselves are still written via
    ``zipfile.ZipFile.writestr(plain_filename, data)``, and CPython's zipfile
    stamps every such entry's ZipInfo.date_time with ``time.localtime()`` at
    write time. That means two builds from byte-identical source content
    still differ, entry by entry, purely on wall-clock seconds.

    This reopens the finished file with the stdlib ``zipfile`` module and
    rewrites every entry with the exact same filename, content, and
    compression method (read back from the original), but a fixed
    ``date_time`` — preserving member order and every other piece of
    metadata untouched.
    """
    date_time = (mtime.year, mtime.month, mtime.day, mtime.hour, mtime.minute, mtime.second)
    with zipfile.ZipFile(path, "r") as src:
        entries = [(info, src.read(info.filename)) for info in src.infolist()]

    tmp_path = path.with_name(path.name + ".tmp")
    with zipfile.ZipFile(tmp_path, "w") as dst:
        for info, data in entries:
            new_info = zipfile.ZipInfo(filename=info.filename, date_time=date_time)
            new_info.compress_type = info.compress_type
            new_info.external_attr = info.external_attr
            new_info.internal_attr = info.internal_attr
            new_info.create_system = info.create_system
            dst.writestr(new_info, data)
    tmp_path.replace(path)


def validate_font_files() -> list[dict[str, str]]:
    """Pin every font used by print CSS so fallback cannot silently repaginate."""
    from fontTools.ttLib import TTFont

    records: list[dict[str, str]] = []
    for filename, expected_sha256 in PDF_FONT_FILES.items():
        font_path = BOOK_FONT_DIR / filename
        if not font_path.is_file():
            raise RuntimeError(f"required PDF font is missing: {font_path}")
        actual_sha256 = hashlib.sha256(font_path.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise RuntimeError(
                f"PDF font drift: {font_path}: expected {expected_sha256}, got {actual_sha256}"
            )
        records.append(
            {"file": str(font_path.relative_to(ROOT)), "sha256": actual_sha256}
        )

    # Fontconfig/Pango resolves faces by their internal family name.  Reusing
    # the system-wide "Noto Color Emoji" name lets an installed 11 MB face win
    # over this pinned 20 KB subset, silently changing pagination and PDF bytes.
    emoji_font = TTFont(BOOK_FONT_DIR / EMOJI_FONT_FILE)
    try:
        family_names = {
            record.toUnicode()
            for record in emoji_font["name"].names
            if record.nameID in {1, 16}
        }
        if family_names != {EMOJI_FONT_FAMILY}:
            raise RuntimeError(
                "PDF emoji font family drift: "
                f"expected {EMOJI_FONT_FAMILY!r}, got {sorted(family_names)!r}"
            )
        actual_codepoints = frozenset(emoji_font.getBestCmap())
        if actual_codepoints != EMOJI_CODEPOINTS:
            raise RuntimeError(
                "PDF emoji subset cmap drift: "
                f"expected {sorted(EMOJI_CODEPOINTS)!r}, "
                f"got {sorted(actual_codepoints)!r}"
            )
        if len(emoji_font.getGlyphOrder()) != len(EMOJI_CODEPOINTS) + 1:
            raise RuntimeError("PDF emoji subset contains unexpected glyph records")
    finally:
        emoji_font.close()
    return records


def validate_fontconfig_policy() -> dict[str, str]:
    """Bind Fontconfig's external-font rejection policy to the build contract."""
    if not FONTCONFIG_POLICY_PATH.is_file():
        raise RuntimeError(
            f"required PDF Fontconfig policy is missing: {FONTCONFIG_POLICY_PATH}"
        )
    actual_sha256 = hashlib.sha256(FONTCONFIG_POLICY_PATH.read_bytes()).hexdigest()
    if actual_sha256 != FONTCONFIG_POLICY_SHA256:
        raise RuntimeError(
            "PDF Fontconfig policy drift: "
            f"expected {FONTCONFIG_POLICY_SHA256}, got {actual_sha256}"
        )
    return {
        "file": str(FONTCONFIG_POLICY_PATH.relative_to(ROOT)),
        "sha256": actual_sha256,
    }


def pdf_source_fingerprint(
    full_html: str,
    font_records: list[dict[str, str]],
    cover_pdf_path: Path,
    *,
    layout_version_tag: str,
    weasyprint_version: str,
) -> str:
    digest = hashlib.sha256()
    digest.update(f"{layout_version_tag}\0".encode())
    digest.update(
        (
            f"weasyprint={weasyprint_version}\0pypdf={version('pypdf')}\0"
            f"source_date_epoch={PDF_SOURCE_DATE_EPOCH}\0"
        ).encode()
    )
    normalized_html = full_html.replace(ROOT.as_uri(), "file://<REPOSITORY_ROOT>")
    digest.update(normalized_html.encode("utf-8"))
    digest.update(b"\0cover\0")
    digest.update(cover_pdf_path.read_bytes())
    fontconfig_policy = validate_fontconfig_policy()
    digest.update(b"\0fontconfig-policy\0")
    digest.update(fontconfig_policy["file"].encode())
    digest.update(b"\0")
    digest.update(fontconfig_policy["sha256"].encode())
    for record in font_records:
        digest.update(b"\0font\0")
        digest.update(record["file"].encode())
        digest.update(b"\0")
        digest.update(record["sha256"].encode())
    return digest.hexdigest()


def write_pdf_pagination_metadata(
    *,
    out_pdf: Path,
    pagination_out: Path,
    cover_pdf_path: Path,
    full_html: str,
    font_records: list[dict[str, str]],
    final_total_pages: int,
    final_anchor_pages: dict[str, int],
    chapter_markers: list[tuple[str, int]],
    page_markers: list[tuple[str, str]],
    project_marker: str,
    chapter_title_url: dict[int, tuple[str, str]],
    layout_version_tag: str,
    weasyprint_version: str,
) -> None:
    """Write the generated physical pagination of a canonical PDF book.

    ``chapter_title_url`` maps chapter number -> (title, canonical site URL),
    letting RU and PL each supply their own canonical chapter metadata source
    (data/chapters.json for RU; the PL homepage's chapter_titles map for PL)
    without this bookkeeping function needing to know which.
    """
    from pypdf import PdfReader

    chapter_starts = {
        num: final_anchor_pages[marker_id] for marker_id, num in chapter_markers
    }
    if sorted(chapter_starts) != list(range(1, 25)):
        raise RuntimeError("pagination metadata does not contain exactly chapters 1..24")
    starts = [chapter_starts[num] for num in range(1, 25)]
    if starts != sorted(set(starts)):
        raise RuntimeError(f"chapter starts are not strictly increasing: {starts}")

    projects_start = final_anchor_pages[project_marker]
    if projects_start <= chapter_starts[24]:
        raise RuntimeError("projects appendix does not start after chapter 24")

    chapter_data: dict[str, dict[str, object]] = {}
    for num in range(1, 25):
        next_boundary = chapter_starts[num + 1] if num < 24 else projects_start
        title, url = chapter_title_url[num]
        chapter_data[f"{num:02d}"] = {
            "number": num,
            "title": title,
            "url": url,
            "start_page": chapter_starts[num],
            "end_page": next_boundary - 1,
        }

    url_pages: dict[str, int] = {}
    for marker_id, url in page_markers:
        if url in url_pages:
            raise RuntimeError(f"duplicate canonical page URL in PDF pagination: {url}")
        url_pages[url] = final_anchor_pages[marker_id]

    reader = PdfReader(str(out_pdf))
    if len(reader.pages) != final_total_pages:
        raise RuntimeError(
            f"final PDF page tree has {len(reader.pages)} pages, expected {final_total_pages}"
        )
    first_width = float(reader.pages[0].mediabox.width)
    first_height = float(reader.pages[0].mediabox.height)
    for physical_page, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - first_width) > 0.01 or abs(height - first_height) > 0.01:
            raise RuntimeError(
                f"PDF trim drift on physical page {physical_page}: {width}x{height} pt"
            )

    metadata = {
        "schema_version": "1.0.0",
        "generated_from": "sha256:" + pdf_source_fingerprint(
            full_html,
            font_records,
            cover_pdf_path,
            layout_version_tag=layout_version_tag,
            weasyprint_version=weasyprint_version,
        ),
        "pdf_sha256": hashlib.sha256(out_pdf.read_bytes()).hexdigest(),
        "render_engine": f"WeasyPrint {weasyprint_version}",
        "pdf_writer": f"pypdf {version('pypdf')}",
        "source_date_epoch": int(PDF_SOURCE_DATE_EPOCH),
        "fontconfig_policy": validate_fontconfig_policy(),
        "page_format": {
            "width_mm": round(first_width * 25.4 / 72, 3),
            "height_mm": round(first_height * 25.4 / 72, 3),
        },
        "front_matter_numbering": (
            "physical page 1 cover unnumbered; physical page 2 title unnumbered; "
            "continuous Arabic physical folios thereafter"
        ),
        "chapter_start_policy": (
            "fresh page via break-before:page (Phase 2B, M02-I07: relaxed from "
            "recto/right-hand break-before:right)"
        ),
        "total_pages": final_total_pages,
        "fonts": font_records,
        "chapters": chapter_data,
        "pages": dict(sorted(url_pages.items())),
    }
    pagination_out.parent.mkdir(parents=True, exist_ok=True)
    pagination_out.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_print_css(*, book_title: str, page_abbrev: str) -> str:
    """The full print stylesheet shared by both locales' PDF builders.

    Only two things vary by locale: the running-header book title in the
    ``:right`` page margin box, and the chapter-opener "page N" abbreviation
    (СТР./STR.) — every other rule (typography, spacing, chapter openers,
    code blocks, callouts, tables, diagrams) is identical between RU and PL,
    so a layout change here applies to both books at once.
    """
    css = """
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSerif.ttf'); font-style: normal; font-weight: 400; }
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSerif-Bold.ttf'); font-style: normal; font-weight: 700; }
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSerif-Italic.ttf'); font-style: italic; font-weight: 400; }
@font-face { font-family: 'DejaVu Serif'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSerif-BoldItalic.ttf'); font-style: italic; font-weight: 700; }
@font-face { font-family: 'DejaVu Sans'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSans.ttf'); font-style: normal; font-weight: 400; }
@font-face { font-family: 'DejaVu Sans'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSans-Bold.ttf'); font-style: normal; font-weight: 700; }
@font-face { font-family: 'DejaVu Sans'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSans-Oblique.ttf'); font-style: italic; font-weight: 400; }
@font-face { font-family: 'DejaVu Sans Mono'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSansMono.ttf'); font-style: normal; font-weight: 400; }
@font-face { font-family: 'DejaVu Sans Mono'; src: url('__FONT_DIR_URI__/dejavu/DejaVuSansMono-Bold.ttf'); font-style: normal; font-weight: 700; }
@font-face { font-family: 'Cartesian Noto Color Emoji'; src: url('__FONT_DIR_URI__/noto-emoji/NotoColorEmoji-subset.ttf'); font-style: normal; font-weight: 100 900; }
@page {
  size: 152mm 229mm;
  margin: 24mm 20mm 26mm 20mm;
  @top-center { content: string(chaptitle); font-family: 'DejaVu Sans', sans-serif; font-size: 8pt; color: #888; letter-spacing: .04em; text-transform: uppercase; }
  @bottom-center { content: counter(page); font-family: 'DejaVu Sans', sans-serif; font-size: 9pt; color: #666; }
}
@page :left { @top-left { content: string(chaptitle); font-family: 'DejaVu Sans', sans-serif; font-size: 8pt; color: #888; letter-spacing: .04em; text-transform: uppercase; } @top-center { content: none; } }
@page :right { @top-right { content: "__BOOK_TITLE__"; font-family: 'DejaVu Sans', sans-serif; font-size: 8pt; color: #888; letter-spacing: .04em; text-transform: uppercase; } @top-center { content: none; } }
@page :first {
  /* The cover is merged in afterwards as an extra, external physical page 1
     that WeasyPrint never renders or counts — so its own internal page 1
     (this title page) is actually true physical page 2. Reset the counter
     here so every printed folio matches the page's real position in the
     final merged PDF, not WeasyPrint's un-offset count. */
  counter-reset: page 2;
  @top-left { content: none; } @top-center { content: none; } @top-right { content: none; } @bottom-center { content: ""; }
}
@page unnumbered { @top-left { content: none; } @top-center { content: none; } @top-right { content: none; } @bottom-center { content: ""; } }
@page opener { @top-left { content: none; } @top-center { content: none; } @top-right { content: none; } }

:root {
  --navy-900: #150a3d; --violet-500: #7c3aed; --blue-500: #2563eb; --blue-300: #93c5fd;
  --amber-500: #d97706; --gray-400: #9ca3af; --red-500: #dc2626;
  --color-text-primary: #1a1a2e; --color-text-muted: #55536b; --color-text-inverse: #fff;
  --color-bg-surface: #f4f3fb; --color-border-default: #ddd9ee;
  --color-brand-blue: #2563eb; --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-full: 999px;
  --spacing-sm: 6px; --spacing-md: 12px; --spacing-lg: 18px; --spacing-xl: 24px; --spacing-2xl: 32px; --spacing-3xl: 48px; --spacing-4xl: 64px;
  --callout-info-bg: #eaf1ff; --callout-info-border: #185dfa;
  --callout-tip-bg: #f3eeff; --callout-tip-border: #5b24f9;
  --callout-warning-bg: #fef3e2; --callout-warning-border: #d97706;
  --callout-security-bg: #fde8e8; --callout-security-border: #dc2626;
  --callout-debug-bg: #fde8e8; --callout-debug-border: #dc2626;
}
* { box-sizing: border-box; }
body { font-family: 'DejaVu Serif', 'DejaVu Sans', 'Cartesian Noto Color Emoji', serif; font-size: 9.8pt; line-height: 1.40; color: var(--color-text-primary); }
h1, h2, h3 { font-family: 'DejaVu Sans', sans-serif; color: var(--navy-900); break-after: avoid; }
h1 { font-size: 21pt; margin: 0 0 10pt; string-set: chaptitle content(); }
h2 { font-size: 14.5pt; margin: 20pt 0 8pt; padding-top: 4pt; border-top: 1px solid var(--color-border-default); }
h3 { font-size: 12pt; margin: 14pt 0 6pt; }
p { margin: 0 0 8pt; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 8pt; padding-left: 18pt; }
li { margin-bottom: 3pt; }
li > ul, li > ol { margin-top: 3pt; margin-bottom: 0; }
a { color: var(--color-brand-blue); text-decoration: none; }
table { width: 100%; border-collapse: collapse; margin: 10pt 0; font-size: 9.3pt; }
table:not(.compare-table) th, table:not(.compare-table) td { padding: 4pt 7pt; border-bottom: 1px solid var(--color-border-default); text-align: left; vertical-align: top; }
table:not(.compare-table) th { font-family: 'DejaVu Sans', sans-serif; font-size: 8.5pt; color: var(--color-text-muted); background: var(--color-bg-surface); }
code, pre { font-family: 'DejaVu Sans Mono', monospace; }
code.inline { background: var(--color-bg-surface); padding: 1px 4px; border-radius: 3px; font-size: 9.2pt; }
.code-block { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 10pt 0; break-inside: avoid; overflow: hidden; }
/* Only code blocks long enough to be classified `code-block--splittable`
   (scripts/book_shared.py's classify_splittable_code_blocks(), applied
   during canonical page normalization — see book_pipeline/model.py) may
   fragment across a page boundary; every other code block keeps the
   `break-inside: avoid` above intact. `overflow: visible` is required here
   because WeasyPrint (like other renderers) will not fragment a box whose
   overflow is clipped, and CSS Fragmentation's default box-decoration-break
   ("slice") already gives a clean look at the split: the border/background
   simply stops at the bottom of the first fragment and resumes at the top
   of the next, with no duplicated border in the middle. */
.code-block--splittable { break-inside: auto; overflow: visible; }
.code-block .code-label { background: var(--navy-900); color: #cbd5ff; font-size: 8.6pt; padding: 5pt 9pt; font-family: 'DejaVu Sans Mono', monospace; letter-spacing: .02em; }
.code-block .copy-btn { display: none; }
.code-block pre { margin: 0; padding: 9pt 11pt; font-size: 8.8pt; line-height: 1.42; white-space: pre-wrap; word-break: break-word; }
.tok-kw { color: #7c3aed; font-weight: 600; }
.tok-str { color: #059669; }
.tok-com { color: #6b7280; font-style: italic; }
.tok-num { color: #d97706; }
.tok-fn { color: #2563eb; }
.callout { border: 1px solid var(--color-border-default); border-left: 3.5pt solid var(--color-brand-blue); border-radius: var(--radius-md); padding: 6pt 10pt; margin: 8pt 0; background: var(--color-bg-surface); break-inside: avoid; }
/* The web layout is a flex row with a ~24px icon emblem beside the text;
   print never declared a size for that icon, so its SVG rendered at an
   unconstrained default size and pushed the actual title/body text far down
   inside the box, leaving a large blank area — the left accent border above
   already carries the same "what kind of callout is this" signal in print. */
/* Every icon-emblem wrapper (callouts, exercises, front-matter cards) is a
   web-only ~24px flex-row icon with no print sizing declared anywhere —
   left unhidden, its SVG renders at an unconstrained default size and pushes
   the actual text far down inside its container. Hiding it globally is the
   same convention already used for .reference-card .ri and the chapter-num
   logo mark. */
.cs-icon-emblem { display: none; }
.callout-title { font-weight: 700; font-family: 'DejaVu Sans', sans-serif; font-size: 9pt; margin-bottom: 2pt; }
.callout-body { font-size: 9.7pt; }
.callout-info { background: var(--callout-info-bg); border-left-color: var(--callout-info-border); }
.callout-tip { background: var(--callout-tip-bg); border-left-color: var(--callout-tip-border); }
.callout-warning { background: var(--callout-warning-bg); border-left-color: var(--callout-warning-border); }
.callout-security { background: var(--callout-security-bg); border-left-color: var(--callout-security-border); }
.callout-debug { background: var(--callout-debug-bg); border-left-color: var(--callout-debug-border); }
.exercise { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 6pt 10pt; margin: 8pt 0; break-inside: avoid; }
.exercise-stars { color: var(--amber-500); font-size: 8.5pt; }
.exercise-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 9.5pt; }
.summary-box { background: var(--color-bg-surface); border-radius: var(--radius-lg); padding: 8pt 12pt; margin: 10pt 0; break-inside: avoid; }
.summary-box ul { margin: 4pt 0 0 16pt; }
.cvm { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 8pt 0; break-inside: avoid; overflow: hidden; }
.cvm-header { background: var(--color-bg-surface); font-weight: 700; font-family: 'DejaVu Sans', sans-serif; padding: 5pt 9pt; font-size: 8.8pt; }
.cvm-grid { display: table; width: 100%; }
.cvm-col { display: table-cell; width: 50%; padding: 7pt 9pt; vertical-align: top; }
.cvm-col.classic { border-right: 1px solid var(--color-border-default); }
.cvm-col pre { margin: 3pt 0 0; font-size: 9pt; white-space: pre-wrap; }
.cvm-verdict { padding: 5pt 9pt; font-size: 8.5pt; border-top: 1px solid var(--color-border-default); }
.section-item { display: block; padding: 5pt 7pt; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin-bottom: 4pt; text-decoration: none; color: var(--color-text-primary); }
.section-item .si-num { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-text-muted); font-size: 8pt; margin-right: 6pt; }
.section-item .si-page { float: right; font-family: 'DejaVu Sans Mono', monospace; color: var(--color-text-muted); font-size: 8pt; }
.chapter-hero { page: opener; break-before: page; padding-top: 26pt; }
.chapter-hero::before { content: ""; display: block; width: 32pt; height: 3pt; background: var(--color-brand-blue); border-radius: var(--radius-full); margin-bottom: 12pt; }
.chapter-hero .chapter-num { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-brand-blue); font-size: 9.5pt; letter-spacing: .04em; margin-bottom: 6pt; }
.chapter-hero .chapter-num::after { content: " · __PAGE_ABBREV__ " counter(page); }
.chapter-hero .chapter-num img { display: none; }
.chapter-hero h1 { font-size: 23pt; margin-bottom: 6pt; }
.chapter-hero p { font-size: 10.5pt; color: var(--color-text-muted); max-width: 90%; padding-top: 6pt; border-top: 1px dotted var(--color-border-default); }
.chapter-meta { display: none; }
.chapter-figure { margin: 10pt auto; break-inside: avoid; }
.chapter-figure img, .chapter-figure svg { width: 100%; height: auto; border-radius: var(--radius-md); border: 1px solid var(--color-border-default); display: block; }
.chapter-figure figcaption, p.figcaption { text-align: center; font-size: 8.5pt; color: var(--color-text-muted); margin-top: 5pt; font-family: 'DejaVu Sans', sans-serif; }
.chapter-figure--narrow { max-width: 70mm; }
.chapter-figure--medium { max-width: 95mm; }
.chapter-figure--wide { max-width: 112mm; }
.chapter-figure-imgbox { display: flex; align-items: center; justify-content: center; background: var(--color-bg-surface); border-radius: var(--radius-md); border: 1px solid var(--color-border-default); padding: 8pt; }
.chapter-figure-imgbox img { max-width: 100%; height: auto; width: auto; }
.chapter-figure-pair { display: block; margin: 10pt 0; }
.chapter-figure-pair .chapter-figure { max-width: 100%; margin: 0 0 10pt; }
.chapter-figure-sequence { display: block; margin: 10pt 0; }
.chapter-figure-sequence .chapter-figure { margin: 0 0 10pt; width: 100%; }
.idx-list { list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 20pt; }
.idx-entry { display: flex; justify-content: space-between; gap: 6pt; padding: 3pt 0; font-size: 9pt; border-bottom: 1px dotted var(--color-border-default); break-inside: avoid; }
.idx-term { flex: 1; min-width: 0; }
.idx-page { flex: none; font-family: 'DejaVu Sans Mono', monospace; color: var(--color-text-muted); }
.idx-note { color: var(--color-text-muted); font-size: 8pt; }
.title-page { page: unnumbered; break-after: page; text-align: center; padding-top: 70mm; }
.title-page .kicker { font-family: 'DejaVu Sans Mono', monospace; color: var(--color-brand-blue); letter-spacing: 2px; font-size: 9.5pt; }
.title-page h1 { font-size: 27pt; margin: 12pt 0 6pt; string-set: none; }
.title-page .subtitle { font-size: 12pt; color: var(--color-text-muted); margin-bottom: 36pt; }
.title-page .author { font-size: 11pt; font-weight: 700; margin-top: 50pt; }
.title-page .author-role { font-size: 9.5pt; color: var(--color-text-muted); }
.chapter-break { break-before: page; }

/* ---------- Copyright page ---------- */
.copyright-page { page: unnumbered; break-before: page; break-after: page; font-size: 9pt; line-height: 1.4; color: var(--color-text-muted); padding-top: 8mm; }
.copyright-page p { margin: 0 0 7pt; font-size: 9pt; }
.copyright-page .cp-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; color: var(--color-text-primary); font-size: 11pt; margin-bottom: 4pt; }

/* ---------- Table of contents ---------- */
.toc-page { break-before: page; }
.toc-page h1 { string-set: none; }
.toc-part-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 9pt; text-transform: uppercase; letter-spacing: .05em; color: var(--color-brand-blue); margin: 12pt 0 5pt; }
.toc-part-title:first-child { margin-top: 0; }
.toc-entry {
  display: flex; justify-content: space-between; align-items: baseline; gap: 10pt;
  text-decoration: none; color: var(--color-text-primary); font-size: 9.5pt; padding: 2.5pt 0;
  border-bottom: 1px dotted var(--color-border-default);
}
.toc-entry.toc-chapter { font-weight: 700; margin-top: 6pt; border-bottom: none; padding-bottom: 0; }
/* min-width:0 overrides the flex item's content-based auto minimum so a long
   chapter title actually shrinks/wraps instead of colliding with the page
   number — without it a title that exactly fills the row abuts the
   ::after-generated counter with no gap at all. */
.toc-label { flex: 1 1 auto; min-width: 0; }
.toc-entry::after {
  content: target-counter(attr(href url), page);
  flex: none; font-family: 'DejaVu Sans Mono', monospace; font-size: 8.5pt; color: var(--color-text-muted);
}

/* ---------- Notebook / practice reference card (print-safe: visible, real URL) ---------- */
.notebook-card { border: 1px solid var(--color-border-default); border-left: 3.5pt solid var(--blue-300); border-radius: var(--radius-md); padding: 6pt 10pt; margin: 8pt 0; break-inside: avoid; background: var(--color-bg-surface); }
.notebook-card .nc-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 9.3pt; color: var(--color-text-primary); }
.notebook-card .nc-sub { font-size: 8.5pt; color: var(--color-text-muted); margin-bottom: 3pt; }
.notebook-card .nc-btn { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.3pt; }
.notebook-card .nc-url { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.3pt; color: var(--color-text-muted); }
.practice-inline-status { display: none; }

/* ---------- Comparison tables (used throughout the book, not just the
   Chapter 24 roadmap — a table this book uses to teach "classic vs modern"
   or "option A vs option B" comparisons needs to look like a designed table
   on every page it appears, not just the one chapter it happened to be
   audited on) ---------- */
.compare-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 8.8pt;
  line-height: 1.35;
  margin: 8pt 0;
}
.compare-table thead { display: table-header-group; }
.compare-table tr { break-inside: avoid; }
.compare-table th,
.compare-table td {
  padding: 5pt 6pt;
  border-bottom: 1px solid var(--color-border-default);
  text-align: left;
  vertical-align: top;
  overflow-wrap: anywhere;
  word-break: break-word;
  hyphens: auto;
}
.compare-table th {
  font-family: 'DejaVu Sans', sans-serif;
  font-size: 8pt;
  line-height: 1.25;
  color: var(--color-text-muted);
  background: var(--color-bg-surface);
}
.compare-table td:first-child, .compare-table th:first-child { font-weight: 600; }
div[id^="marker-page-24-"] article[data-future-course] { break-inside: avoid-page; }

/* ---------- Projects appendix ---------- */
.project-entry { break-before: page; }
.project-entry .project-hero { width: 100%; height: 45mm; overflow: hidden; border-radius: var(--radius-md); margin-bottom: 12pt; }
.project-entry .project-hero svg { display: block; width: 100%; height: 100%; }
.project-meta-row { margin: 4pt 0 10pt; }
.project-topic { display: inline-block; font-family: 'DejaVu Sans', sans-serif; font-size: 8.5pt; font-weight: 700; background: var(--color-bg-surface); color: var(--color-text-muted); padding: 2pt 8pt; border-radius: var(--radius-full); margin: 0 4pt 4pt 0; }
.reference-board { margin: 10pt 0; }
.reference-card { display: block; padding: 5pt 0; text-decoration: none; color: var(--color-text-primary); border-bottom: 1px dotted var(--color-border-default); }
.reference-card .ri { display: none; }
.reference-card .rt { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 9.5pt; }
.reference-card .rs { font-size: 8.7pt; color: var(--color-text-muted); }
"""
    css = css.replace("__FONT_DIR_URI__", BOOK_FONT_DIR.as_uri())
    css = css.replace("__BOOK_TITLE__", book_title)
    css = css.replace("__PAGE_ABBREV__", page_abbrev)
    return css
