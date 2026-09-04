"""Переиспользуемый генератор HTML-страниц теории Cartesian School.

Строит страницы из структурированных данных (Python), используя те же CSS-классы,
что и в site/assets/css/theory.css (см. прототип site/chapters/glava-06/).
Не хранит контент — только рендеринг; текст пишется отдельно для каждого раздела.
"""

from __future__ import annotations

import html
import io
import itertools
import keyword
import re
import tokenize
from dataclasses import dataclass, field
from urllib.parse import urljoin

from book_pagination import chapter_start, page_for_url
from chapter_metadata import chapter


# ---------------------------------------------------------------------------
# Cartesian School icon system
# ---------------------------------------------------------------------------
# Original local SVG sprite at site/assets/icons/cartesian/icons.svg replaces
# decorative Unicode emoji (💡🚀⚠️ etc.) across chapter content — see
# docs/ICON-SYSTEM.md for the full semantic mapping and rationale.
#
# Call sites never write raw <svg> markup: they embed a plain-text marker via
# icon_label("idea", "Заголовок") -> "[[icon:idea]] Заголовок". The marker
# survives html.escape() unchanged (none of its characters are HTML-special),
# so it can sit inside a title string that later gets escaped by callout(),
# exercise(), render_sidebar() etc. exactly like the emoji it replaced. The
# *only* place the marker is ever resolved into real <svg> markup is
# _render_icon_markers(), called once on the fully-assembled page HTML in
# render_page() / render_chapter_opener() — so every chapter script gets the
# icon system "for free" and never has to think about the escaping order.
CS_ICON_NAMES = frozenset({
    "idea", "launch", "warning", "success", "error", "debug", "experiment",
    "timer", "practice", "code", "file", "folder", "game", "architecture",
    "palette", "tools", "loop", "note", "compare", "profile", "search",
    "device",
})

_ICON_MARKER_RE = re.compile(r"\[\[icon:([a-z-]+)\]\]")


def cs_icon(name: str) -> str:
    """Inline <svg><use> reference into the shared Cartesian icon sprite.

    Uses `currentColor` so the icon inherits its color from CSS (see
    .cs-icon / .cs-icon--<name> in theory.css) — never call this to produce
    a permanently-colored icon.
    """
    if name not in CS_ICON_NAMES:
        raise ValueError(f"unknown cs_icon name: {name!r} (see CS_ICON_NAMES)")
    return (
        f'<svg class="cs-icon cs-icon--{name}" aria-hidden="true">'
        f'<use href="/assets/icons/cartesian/icons.svg#icon-{name}"></use></svg>'
    )


_LEADING_ICON_RE = re.compile(r"^\[\[icon:([a-z-]+)\]\]\s*")


def _extract_leading_icon(title: str) -> tuple[str, str]:
    """If `title` starts with an icon_label() marker, returns (icon_name,
    rest-of-title); otherwise ("", title). Used by callout()/exercise() to
    pull the icon out of the (escaped) title text and render it as its own
    Level A emblem tile instead — see cs_icon_emblem()."""
    m = _LEADING_ICON_RE.match(title)
    if not m:
        return "", title
    return m.group(1), title[m.end():]


def cs_icon_emblem(name: str) -> str:
    """A Level A "signal" tile: the icon at ~26px on a ~40px rounded tile
    tinted with its own semantic color (see .cs-icon-emblem in theory.css).

    This is the strong, attention-grabbing presentation — reserved for
    important semantic blocks (callout()/exercise() titles, Debug Lab
    headings). Everyday inline use (sidebar links, chapter metadata badges,
    directory-tree illustrations) should keep using the plain cs_icon()/
    icon_label() — see docs/ICON-SYSTEM.md's "signal levels" section.
    """
    if name not in CS_ICON_NAMES:
        raise ValueError(f"unknown cs_icon name: {name!r} (see CS_ICON_NAMES)")
    return f'<div class="cs-icon-emblem cs-icon-emblem--{name}">{cs_icon(name)}</div>'


def icon_label(name: str, text: str) -> str:
    """Prefix `text` with a semantic Cartesian icon marker.

    This is the one API future chapter scripts should use instead of typing
    a decorative emoji: icon_label("idea", "Почему это работает") instead of
    "💡 Почему это работает". Works anywhere a plain title/label string is
    accepted (callout(), exercise(), NavItem(), meta_items=[...], raw
    <h2> text, ...) — the marker is resolved to real markup later by
    _render_icon_markers().
    """
    if name not in CS_ICON_NAMES:
        raise ValueError(f"unknown cs_icon name: {name!r} (see CS_ICON_NAMES)")
    return f"[[icon:{name}]] {text}"


def _render_icon_markers(page_html: str) -> str:
    """Resolves every [[icon:name]] marker in fully-assembled page HTML into
    real <svg> markup. Called once per page, at the end of render_page() /
    render_chapter_opener() — see module docstring above."""
    def _sub(m: re.Match[str]) -> str:
        name = m.group(1)
        if name not in CS_ICON_NAMES:
            raise ValueError(f"unknown cs_icon marker: [[icon:{name}]] (see CS_ICON_NAMES)")
        return cs_icon(name)
    return _ICON_MARKER_RE.sub(_sub, page_html)


# ---------------------------------------------------------------------------
# Подсветка кода
# ---------------------------------------------------------------------------

_BUILTIN_SOFT = {
    "print", "input", "len", "range", "int", "float", "str", "list", "dict",
    "set", "tuple", "bool", "sum", "min", "max", "sorted", "enumerate", "zip",
    "abs", "round", "type", "isinstance", "open", "map", "filter",
}


def highlight_python(code: str) -> str:
    """Оборачивает токены Python-кода в <span class="tok-*"> для theory.css.

    Использует стандартный tokenize, поэтому корректно обрабатывает f-строки,
    многострочные строки и русские комментарии/строки. Реконструирует источник
    по абсолютным смещениям символов — не по построчной догонялке, — чтобы
    переводы строк не дублировались.
    """
    code = code.rstrip("\n")
    lines = code.splitlines(keepends=True)
    # смещение начала каждой (1-indexed) строки в исходном тексте
    line_offsets = [0]
    for line in lines:
        line_offsets.append(line_offsets[-1] + len(line))

    def offset(row: int, col: int) -> int:
        if row - 1 >= len(line_offsets):
            return len(code)
        return line_offsets[row - 1] + col

    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code + "\n").readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return html.escape(code)

    out: list[str] = []
    cursor = 0

    for tok in tokens:
        tok_type, tok_str, start, end, _line = tok
        if tok_type in (tokenize.ENCODING, tokenize.ENDMARKER):
            continue
        start_off = min(offset(*start), len(code))
        end_off = min(offset(*end), len(code))
        if start_off < cursor:
            continue  # перекрывающийся/синтетический токен — пропускаем

        # необработанный промежуток (пробелы и т. п.) — копируем как есть
        if start_off > cursor:
            out.append(html.escape(code[cursor:start_off]))

        text = html.escape(code[start_off:end_off])
        css = None
        if tok_type == tokenize.COMMENT:
            css = "tok-com"
        elif tok_type in (
            tokenize.STRING,
            getattr(tokenize, "FSTRING_START", -1),
            getattr(tokenize, "FSTRING_MIDDLE", -1),
            getattr(tokenize, "FSTRING_END", -1),
        ):
            css = "tok-str"
        elif tok_type == tokenize.NUMBER:
            css = "tok-num"
        elif tok_type == tokenize.NAME:
            if keyword.iskeyword(tok_str) or keyword.issoftkeyword(tok_str):
                css = "tok-kw"
            elif tok_str in _BUILTIN_SOFT:
                css = "tok-fn"

        out.append(f'<span class="{css}">{text}</span>' if css else text)
        cursor = end_off

    if cursor < len(code):
        out.append(html.escape(code[cursor:]))

    return "".join(out)


# ---------------------------------------------------------------------------
# Блоки контента
# ---------------------------------------------------------------------------

def code_block(filename: str, code: str, *, lang: str = "python") -> str:
    highlighted = highlight_python(code) if lang == "python" else html.escape(code)
    return f"""
    <div class="code-block">
      <div class="code-label"><span>{html.escape(filename)}</span><button class="copy-btn" onclick="navigator.clipboard.writeText(this.closest('.code-block').querySelector('code').innerText)">Копировать</button></div>
      <pre><code>{highlighted}</code></pre>
    </div>"""


def callout(kind: str, title: str, body_html: str) -> str:
    icon_name, title = _extract_leading_icon(title)
    emblem_html = cs_icon_emblem(icon_name) + "\n      " if icon_name else ""
    return f"""
    <div class="callout callout-{kind}">
      {emblem_html}<div>
        <div class="callout-title">{html.escape(title)}</div>
        <div class="callout-body">{body_html}</div>
      </div>
    </div>"""


def classic_vs_modern(
    header: str,
    classic_label: str,
    classic_code: str,
    modern_label: str,
    modern_code: str,
    verdict_html: str,
) -> str:
    return f"""
    <div class="cvm">
      <div class="cvm-header">{html.escape(header)}</div>
      <div class="cvm-grid">
        <div class="cvm-col classic">
          <div class="cvm-label">{html.escape(classic_label)}</div>
          <pre><code>{highlight_python(classic_code)}</code></pre>
        </div>
        <div class="cvm-col modern">
          <div class="cvm-label">{html.escape(modern_label)}</div>
          <pre><code>{highlight_python(modern_code)}</code></pre>
        </div>
      </div>
      <div class="cvm-verdict"><strong>Что использовать сегодня:</strong> {verdict_html}</div>
    </div>"""


_STARS = {1: "★ Базовая практика", 2: "★★ Самостоятельная задача", 3: "★★★ Задача повышенной сложности"}


def exercise(stars: int, title: str, body_html: str) -> str:
    icon_name, title = _extract_leading_icon(title)
    emblem_html = cs_icon_emblem(icon_name) if icon_name else ""
    inner = f"""<div class="exercise-stars">{_STARS[stars]}</div>
      <div class="exercise-title">{html.escape(title)}</div>
      <p>{body_html}</p>"""
    if not emblem_html:
        return f'\n    <div class="exercise">\n      {inner}\n    </div>'
    return f"""
    <div class="exercise exercise-signal">
      {emblem_html}
      <div>
      {inner}
      </div>
    </div>"""


def notebook_card(title: str, sub: str, href: str) -> str:
    return f"""
    <div class="notebook-card">
      <div>
        <div class="nc-title">{html.escape(title)}</div>
        <div class="nc-sub">{html.escape(sub)}</div>
      </div>
      <a class="nc-btn" href="{html.escape(href)}">Открыть ноутбук →</a>
    </div>"""


def practice_card(lesson_id: str, title: str, sub: str, practice_href: str) -> str:
    """Like notebook_card, but links to an interactive /practice/<lesson-id>/ page
    (our own Pyodide runner, not a raw .ipynb) and shows live completion status
    read from localStorage (cartesian.python.progress.v1)."""
    lesson_id_js = html.escape(lesson_id).replace('"', '\\"')
    return f"""
    <div class="notebook-card">
      <div>
        <div class="nc-title">{html.escape(title)}</div>
        <div class="nc-sub">{html.escape(sub)}</div>
        <div class="practice-inline-status" data-lesson-id="{html.escape(lesson_id)}"></div>
      </div>
      <a class="nc-btn" href="{html.escape(practice_href)}">Открыть практику →</a>
    </div>
    <script>
    (function () {{
      try {{
        var all = JSON.parse(localStorage.getItem("cartesian.python.progress.v1") || "{{}}");
        var entry = all["{lesson_id_js}"];
        var el = document.querySelector('.practice-inline-status[data-lesson-id="{lesson_id_js}"]');
        if (entry && entry.passed && el) {{
          el.innerHTML = '<strong style="color:#15803d">✓ Практика пройдена</strong> — Результат: ' + entry.score + '%';
        }}
      }} catch (e) {{}}
    }})();
    </script>"""


def local_required_card(lesson_id: str, title: str, sub: str, practice_href: str) -> str:
    """Like practice_card(), but for lessons whose canonical code (e.g. `import
    turtle`) cannot run in the browser (Pyodide has no turtle/tkinter — see
    evidence gathered for the Chapter 6/7 rollout). Links to a local-required
    practice page (build_practice_pages.py's build_local_required_page())
    instead of a live Pyodide runner, and shows one of three states read from
    localStorage (cartesian.python.progress.v1): not yet acknowledged, or
    learner-declared local completion — never a fabricated PASS/score.
    """
    lesson_id_js = html.escape(lesson_id).replace('"', '\\"')
    return f"""
    <div class="notebook-card">
      <div>
        <div class="nc-title">{html.escape(title)}</div>
        <div class="nc-sub">{html.escape(sub)}</div>
        <div class="practice-inline-status" data-lesson-id="{html.escape(lesson_id)}">Практика выполняется локально</div>
      </div>
      <a class="nc-btn" href="{html.escape(practice_href)}">Открыть практику →</a>
    </div>
    <script>
    (function () {{
      try {{
        var all = JSON.parse(localStorage.getItem("cartesian.python.progress.v1") || "{{}}");
        var entry = all["{lesson_id_js}"];
        var el = document.querySelector('.practice-inline-status[data-lesson-id="{lesson_id_js}"]');
        if (entry && entry.status === "completed-local" && el) {{
          el.innerHTML = '<strong style="color:#15803d">✓ Выполнено локально</strong> — результат не проверялся автоматически';
        }}
      }} catch (e) {{}}
    }})();
    </script>"""


def flow_diagram(steps: list[tuple[str, str]], *, caption: str = "") -> str:
    """Горизонтальная диаграмма-цепочка шагов (оригинальная, не скриншот).

    steps: список (заголовок, подпись) для каждого прямоугольника. Заголовок
    и подпись переносятся по словам (см. _wrap_svg_text) и никогда не выходят
    за пределы прямоугольника — высота блока подстраивается под самый длинный
    заголовок/подпись во всей цепочке, чтобы стрелки и текст оставались на
    одном уровне у всех шагов.
    """
    n = len(steps)
    box_w, gap = 184, 56
    title_max_chars, title_max_lines, title_line_h = 16, 2, 18
    sub_max_chars, sub_max_lines, sub_line_h = 21, 3, 14
    top_pad, mid_gap, bottom_pad = 22, 10, 16

    wrapped = [
        (
            _wrap_svg_text(" ".join(title.split()), max_chars=title_max_chars, max_lines=title_max_lines),
            _wrap_svg_text(
                " ".join(sub.split()),
                max_chars=sub_max_chars,
                max_lines=sub_max_lines,
                hard_split_long_words=True,
            ),
        )
        for title, sub in steps
    ]
    max_title_lines = max((len(t) for t, _ in wrapped), default=1)
    max_sub_lines = max((len(s) for _, s in wrapped), default=1)
    box_h = top_pad + max_title_lines * title_line_h + mid_gap + max_sub_lines * sub_line_h + bottom_pad

    total_w = n * box_w + (n - 1) * gap
    total_h = box_h + 40
    # Below ~5 boxes, shrinking the SVG to fit a narrow viewport still leaves
    # legible text, so it's left free to shrink (matches every existing
    # diagram across the book). At 5+ boxes shrink-to-fit makes the labels
    # unreadably small on a 390px phone; forcing a min-width keeps the
    # diagram at full, legible size and relies on the figure's own
    # overflow-x:auto (below) to scroll it horizontally instead — the same
    # trade-off already used for wide tables and code blocks.
    min_width_style = f"min-width:{total_w}px;" if n >= 5 else ""
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="process-flow" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px;{min_width_style}">'
    ]
    parts.append(
        "<defs><marker id='arrow' viewBox='0 0 10 10' refX='9' refY='5' "
        "markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#5B24F9'/></marker></defs>"
    )
    sub_top_offset = top_pad + max_title_lines * title_line_h + mid_gap
    for i, (title_lines, sub_lines) in enumerate(wrapped):
        x = i * (box_w + gap)
        y = 10
        cx = x + box_w / 2
        parts.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="#EDE9FE" stroke="#5B24F9" stroke-width="2"/>'
        )
        title_top = y + top_pad
        title_tspans = "".join(
            f'<tspan x="{cx}" y="{title_top + li * title_line_h}">{html.escape(line)}</tspan>'
            for li, line in enumerate(title_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" '
            f'font-size="15" fill="#0D0230">{title_tspans}</text>'
        )
        sub_top = y + sub_top_offset
        sub_tspans = "".join(
            f'<tspan x="{cx}" y="{sub_top + li * sub_line_h}">{html.escape(line)}</tspan>'
            for li, line in enumerate(sub_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="Inter, sans-serif" font-size="12" '
            f'fill="#6B6B7D">{sub_tspans}</text>'
        )
        if i < n - 1:
            ax1 = x + box_w + 6
            ax2 = x + box_w + gap - 6
            ay = y + box_h / 2
            parts.append(
                f'<line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" '
                f'stroke="#5B24F9" stroke-width="2" marker-end="url(#arrow)"/>'
            )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto">{svg}{cap}</figure>'


def timeline_diagram(events: list[tuple[str, str]], *, caption: str = "") -> str:
    """Вертикальная диаграмма-хронология (оригинальная, не скриншот).

    events: список (заголовок-веха, пояснение) сверху вниз.
    """
    n = len(events)
    row_h = 88
    pad_top = 20
    total_h = n * row_h + pad_top
    total_w = 640
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="timeline" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    if n > 1:
        parts.append(
            f'<line x1="28" y1="{pad_top + 24}" x2="28" y2="{pad_top + (n - 1) * row_h + 24}" '
            f'stroke="#B9A0FC" stroke-width="3"/>'
        )
    for i, (title, sub) in enumerate(events):
        y = pad_top + i * row_h
        parts.append(f'<circle cx="28" cy="{y + 24}" r="9" fill="#5B24F9"/>')
        parts.append(f'<circle cx="28" cy="{y + 24}" r="4" fill="#fff"/>')
        parts.append(
            f'<text x="56" y="{y + 20}" font-family="Sora, sans-serif" font-weight="700" '
            f'font-size="16" fill="#0D0230">{html.escape(title)}</text>'
        )
        parts.append(
            f'<text x="56" y="{y + 42}" font-family="Inter, sans-serif" font-size="13" fill="#6B6B7D">'
            f'{html.escape(sub)}</text>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto">{svg}{cap}</figure>'


def _wrap_svg_text(
    text: str, max_chars: int, max_lines: int = 3, *, hard_split_long_words: bool = False
) -> list[str]:
    """Greedy word-wrap for SVG <text>, which never wraps on its own.

    Wraps the full text first (as many lines as it takes, each up to
    max_chars) and only afterwards truncates to max_lines with a trailing
    "…" if it still doesn't fit. Truncating the line count *before* the
    greedy pass finishes would cut off the last word or two of otherwise
    short text — this two-pass order keeps every word that legitimately
    fits within max_lines.

    hard_split_long_words: a whitespace-delimited token longer than
    max_chars — a code literal like ['python','python','code'] or a path
    like Cartesian-School/safesort, neither of which contains a space for
    the greedy pass to break on — is normally still accepted onto its own
    oversized line unconditionally (the character budget is only a proxy
    for the box's real pixel width, and most callers' boxes have enough
    slack that an over-budget word still fits — hard-splitting those would
    needlessly mangle words that were never actually overflowing). Pass
    True only at a call site whose box is known to have no such slack —
    where max_chars is a tight fit — to hard-split the token instead: each
    cut prefers the last punctuation break (',' '/' '.' '-' '_') in the
    second half of the max_chars window, e.g. splitting
    ['python','python','code'] after the second comma rather than through
    the middle of 'code', and falls back to a raw character cut only when
    no such break point exists.
    """
    break_chars = (",", "/", ".", "-", "_")

    def hard_split(word: str) -> list[str]:
        chunks: list[str] = []
        while len(word) > max_chars:
            window = word[:max_chars]
            cut = max((window.rfind(c) for c in break_chars), default=-1)
            if cut < max_chars // 2:
                cut = max_chars - 1  # no good punctuation break — raw cut
            chunks.append(word[: cut + 1])
            word = word[cut + 1 :]
        chunks.append(word)
        return chunks

    lines: list[str] = []
    current = ""
    for word in text.split():
        if hard_split_long_words and len(word) > max_chars:
            # An oversized word's hard-split pieces are pushed straight into
            # `lines`, bypassing the space-joining logic below entirely —
            # two pieces of the SAME original word must never be rejoined
            # with a space, which would corrupt the code/URL they came from.
            if current:
                lines.append(current)
                current = ""
            lines.extend(hard_split(word))
            continue
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    if len(lines) <= max_lines:
        return lines

    kept = lines[:max_lines]
    last = kept[-1].rstrip()
    if len(last) > max_chars - 1:
        last = last[: max_chars - 1].rstrip()
    kept[-1] = last + "…"
    return kept


def branch_diagram(root: str, branches: list[tuple[str, str]], *, caption: str = "") -> str:
    """Диаграмма «один корень → несколько ветвей» (оригинальная, не скриншот).

    branches: список (заголовок, пояснение) для каждого прямоугольника-ветви.
    root: заголовок корневого блока — переносится по словам (см.
    _wrap_svg_text) и никогда не выходит за пределы фиолетового
    прямоугольника; сам прямоугольник растёт по высоте под многострочный
    текст, а холст диаграммы — по ширине, если корень шире, чем ряд ветвей
    (иначе ветви центрируются относительно уширенного холста).
    """
    n = len(branches)
    box_w, box_h, gap = 196, 116, 28
    branches_w = n * box_w + (n - 1) * gap

    root_w = 240
    root_max_chars, root_max_lines, root_line_h = 18, 3, 20
    root_lines = _wrap_svg_text(" ".join(root.split()), max_chars=root_max_chars, max_lines=root_max_lines)
    root_h = 56 + (len(root_lines) - 1) * root_line_h

    total_w = max(branches_w, root_w + 40, 260)
    branches_x_offset = (total_w - branches_w) / 2
    root_x = (total_w - root_w) / 2
    root_top = 10
    root_bottom = root_top + root_h
    branches_y = root_bottom + 54
    total_h = branches_y + box_h + 10
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="block-diagram" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        f'<rect x="{root_x}" y="{root_top}" width="{root_w}" height="{root_h}" rx="4" '
        f'fill="#5B24F9"/>'
    )
    root_cx = total_w / 2
    root_first_line_y = root_top + root_h / 2 - (len(root_lines) - 1) * root_line_h / 2 + 5
    root_tspans = "".join(
        f'<tspan x="{root_cx}" y="{root_first_line_y + li * root_line_h}">{html.escape(line)}</tspan>'
        for li, line in enumerate(root_lines)
    )
    parts.append(
        f'<text text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" '
        f'font-size="16" fill="#fff">{root_tspans}</text>'
    )
    branch_centres = [branches_x_offset + i * (box_w + gap) + box_w / 2 for i in range(n)]
    bus_y = root_bottom + 27
    if branch_centres:
        parts.append(
            f'<line x1="{root_cx}" y1="{root_bottom}" x2="{root_cx}" y2="{bus_y}" '
            f'stroke="#5B24F9" stroke-width="2.5"/>'
        )
        parts.append(
            f'<line x1="{min(branch_centres)}" y1="{bus_y}" x2="{max(branch_centres)}" y2="{bus_y}" '
            f'stroke="#5B24F9" stroke-width="2.5"/>'
        )
    branch_fills = ("#EDE9FE", "#DBEAFE", "#DCFCE7", "#FEF3C7", "#FCE7F3")
    for i, (title, sub) in enumerate(branches):
        x = branches_x_offset + i * (box_w + gap)
        cx = x + box_w / 2
        parts.append(
            f'<path d="M{cx},{bus_y} V{branches_y}" '
            f'fill="none" stroke="#B9A0FC" stroke-width="2.5" marker-end="url(#arrow)"/>'
        )
        parts.append(
            f'<rect x="{x}" y="{branches_y}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="{branch_fills[i % len(branch_fills)]}" stroke="#5B24F9" stroke-width="2"/>'
        )
        title_lines = _wrap_svg_text(title, max_chars=20, max_lines=2)
        title_top = branches_y + 26
        title_tspans = "".join(
            f'<tspan x="{cx}" y="{title_top + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(title_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" '
            f'font-size="14" fill="#0D0230">{title_tspans}</text>'
        )
        sub_lines = _wrap_svg_text(sub, max_chars=26, max_lines=3)
        sub_top = title_top + len(title_lines) * 18 + 14
        sub_tspans = "".join(
            f'<tspan x="{cx}" y="{sub_top + li * 14}">{html.escape(line)}</tspan>' for li, line in enumerate(sub_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="Inter, sans-serif" font-size="11" '
            f'fill="#6B6B7D">{sub_tspans}</text>'
        )
    parts.insert(
        1,
        "<defs><marker id='arrow' viewBox='0 0 10 10' refX='9' refY='5' "
        "markerWidth='6' markerHeight='6' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>",
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def name_value_diagram(name: str, value_repr: str, *, caption: str = "") -> str:
    """Маленькая диаграмма «имя указывает на значение» (не «коробка с данными»)."""
    svg = f"""<svg viewBox="0 0 400 90" xmlns="http://www.w3.org/2000/svg" role="img" data-diagram="reference-diagram"
      aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:400px">
      <defs><marker id="arrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
        orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#5B24F9"/></marker></defs>
      <text x="10" y="52" font-family="JetBrains Mono, monospace" font-weight="700" font-size="20" fill="#0D0230">{html.escape(name)}</text>
      <line x1="95" y1="45" x2="220" y2="45" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#arrow2)"/>
      <rect x="230" y="15" width="160" height="60" rx="4" fill="#EDE9FE" stroke="#5B24F9" stroke-width="2"/>
      <text x="310" y="52" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="17" fill="#0D0230">{html.escape(value_repr)}</text>
    </svg>"""
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;justify-content:center;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def namespace_diagram(
    bindings: list[tuple[str, str]],
    *,
    unreachable: list[str] | None = None,
    caption: str = "",
) -> str:
    """Snapshot of a namespace: each (name, value_repr) pair drawn as its own
    independent row — name on the left, an arrow, a value box on the right —
    stacked top to bottom. Two rows that happen to share a value_repr are
    drawn as two SEPARATE boxes (this function never merges rows), which is
    exactly right for showing "these two names now point to different
    objects" after a rebinding. For "several names point at the SAME single
    object" use converge_diagram() instead — merging boxes there is the
    correct picture, not this one.

    unreachable: optional list of value_repr strings drawn below the normal
    rows, each in a dashed muted box with no incoming arrow and a small
    "0 ссылок" label — for showing an object nothing refers to any more.
    """
    unreachable = unreachable or []
    row_h = 64
    name_col_w = 170
    box_w, box_h = 160, 46
    total_w = name_col_w + box_w + 40
    n = len(bindings)
    m = len(unreachable)
    top_pad = 16
    total_h = top_pad + n * row_h + (m * (row_h + 14) if m else 0) + 10

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="reference-diagram" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        "<defs><marker id='arrowns' viewBox='0 0 10 10' refX='9' refY='5' "
        "markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#5B24F9'/></marker></defs>"
    )
    box_x = name_col_w + 30
    for i, (name, value_repr) in enumerate(bindings):
        y = top_pad + i * row_h
        cy = y + box_h / 2
        name_lines = _wrap_svg_text(" ".join(name.split()), max_chars=16, max_lines=2)
        name_tspans = "".join(
            f'<tspan x="0" y="{cy - (len(name_lines) - 1) * 10 + 6 + li * 20}">{html.escape(line)}</tspan>'
            for li, line in enumerate(name_lines)
        )
        parts.append(
            f'<text font-family="JetBrains Mono, monospace" font-weight="700" font-size="17" '
            f'fill="#0D0230">{name_tspans}</text>'
        )
        parts.append(
            f'<line x1="{name_col_w - 30}" y1="{cy}" x2="{box_x - 8}" y2="{cy}" '
            f'stroke="#5B24F9" stroke-width="2.5" marker-end="url(#arrowns)"/>'
        )
        parts.append(
            f'<rect x="{box_x}" y="{y}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="#EDE9FE" stroke="#5B24F9" stroke-width="2"/>'
        )
        value_lines = _wrap_svg_text(" ".join(value_repr.split()), max_chars=16, max_lines=2)
        value_top = cy - (len(value_lines) - 1) * 9 + 5
        value_tspans = "".join(
            f'<tspan x="{box_x + box_w / 2}" y="{value_top + li * 18}">{html.escape(line)}</tspan>'
            for li, line in enumerate(value_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="15" '
            f'fill="#0D0230">{value_tspans}</text>'
        )
    for j, value_repr in enumerate(unreachable):
        y = top_pad + n * row_h + j * (row_h + 14) + (14 if n else 0)
        cy = y + box_h / 2
        parts.append(
            f'<rect x="{box_x}" y="{y}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="#F3F4F6" stroke="#B9A0FC" stroke-width="2" stroke-dasharray="6,5"/>'
        )
        value_lines = _wrap_svg_text(" ".join(value_repr.split()), max_chars=16, max_lines=2)
        value_top = cy - (len(value_lines) - 1) * 9 + 5
        value_tspans = "".join(
            f'<tspan x="{box_x + box_w / 2}" y="{value_top + li * 18}">{html.escape(line)}</tspan>'
            for li, line in enumerate(value_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="15" '
            f'fill="#8A8A9A">{value_tspans}</text>'
        )
        parts.append(
            f'<text x="{box_x + box_w / 2}" y="{y + box_h + 16}" text-anchor="middle" '
            f'font-family="Inter, sans-serif" font-size="11" fill="#8A8A9A">0 ссылок</text>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px 20px 12px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def place_value_diagram(digits: list[str], place_values: list[int], *, total: str = "", caption: str = "") -> str:
    """HTML/CSS place-value breakdown for a number system explanation, e.g.
    1010(2) -> boxes [1,0,1,0] over place values [8,4,2,1] -> sum -> total.
    digits and place_values must be the same length, most-significant first.
    """
    n = len(digits)
    cells = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px">'
        f'<div style="width:56px;height:56px;border-radius:12px;background:var(--color-bg-canvas,#fff);'
        f'border:1.5px solid #5B24F9;display:flex;align-items:center;justify-content:center;'
        f'font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:22px;color:#0D0230">'
        f'{html.escape(d)}</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:var(--ink-soft,#6B6B7D)">×{pv}</div>'
        f'</div>'
        for d, pv in zip(digits, place_values)
    )
    plus_row = "".join(
        '<div style="width:56px;text-align:center;font-size:18px;color:#B9A0FC">'
        + ("+" if i < n - 1 else "")
        + "</div>"
        for i in range(n)
    )
    sum_html = (
        f'<div style="margin-top:14px;text-align:center;font-family:\'JetBrains Mono\',monospace;'
        f'font-size:15px;color:#0D0230">= {html.escape(total)}</div>'
        if total
        else ""
    )
    inner = (
        f'<div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">{cells}</div>'
        f'<div style="display:flex;gap:14px;justify-content:center;margin-top:2px">{plus_row}</div>'
        f'{sum_html}'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto">{inner}{cap}</figure>'


def string_index_diagram(text: str, *, caption: str = "") -> str:
    """Character-box diagram for string indexing: each character of `text` in
    its own box, positive index (0, 1, 2, ...) above, negative index
    (-n, ..., -1) below — the same box, read two ways. Spaces render as a
    small centered dot so an "invisible" character stays visible."""
    n = len(text)
    box = 44

    def cell(content: str, *, color: str = "#0D0230", weight: str = "700", size: str = "13px") -> str:
        return (
            f'<div style="width:{box}px;text-align:center;font-family:\'JetBrains Mono\',monospace;'
            f'font-weight:{weight};font-size:{size};color:{color}">{content}</div>'
        )

    pos_row = "".join(cell(str(i), color="#5B24F9") for i in range(n))
    char_row = "".join(
        f'<div style="width:{box}px;height:{box}px;border:1.5px solid #0D0230;border-radius:8px;'
        f'display:flex;align-items:center;justify-content:center;font-family:\'JetBrains Mono\',monospace;'
        f'font-weight:700;font-size:18px;background:#fff;color:#0D0230">'
        f'{"·" if ch == " " else html.escape(ch)}</div>'
        for ch in text
    )
    neg_row = "".join(cell(str(i - n), color="#DB2777") for i in range(n))
    inner = (
        f'<div style="display:flex">{pos_row}</div>'
        f'<div style="display:flex;margin:4px 0">{char_row}</div>'
        f'<div style="display:flex">{neg_row}</div>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{inner}</div></div>'
        f'{cap}</figure>'
    )


def string_slice_diagram(text: str, start: int, stop: int, *, caption: str = "") -> str:
    """Slice-window diagram: characters as boxes, and BOUNDARY numbers (0..n)
    drawn in the gaps between/around them — the correct mental model for
    slicing ("cut here, cut there"). The [start:stop) range is shaded, and
    the resulting substring is printed below. start/stop must already be
    resolved to non-negative in-range ints by the caller (e.g. word[2:] ->
    start=2, stop=len(word))."""
    n = len(text)
    box = 44

    char_row = "".join(
        f'<div style="width:{box}px;height:{box}px;border:1.5px solid #0D0230;border-radius:8px;'
        f'display:flex;align-items:center;justify-content:center;font-family:\'JetBrains Mono\',monospace;'
        f'font-weight:700;font-size:18px;color:#0D0230;'
        f'background:{"#E7DEFF" if start <= i < stop else "#fff"}">'
        f'{"·" if ch == " " else html.escape(ch)}</div>'
        for i, ch in enumerate(text)
    )
    boundary_row = "".join(
        f'<div style="width:{box}px;text-align:center;font-family:\'JetBrains Mono\',monospace;'
        f'font-weight:700;font-size:12px;color:{"#5B24F9" if j in (start, stop) else "#B9A0FC"}">{j}</div>'
        for j in range(n + 1)
    )
    result = html.escape(text[start:stop])
    inner = (
        f'<div style="display:flex;margin-left:-{box // 2}px">{boundary_row}</div>'
        f'<div style="display:flex;margin:4px 0">{char_row}</div>'
        f'<div style="text-align:center;font-family:\'JetBrains Mono\',monospace;font-size:14px;'
        f'color:#0D0230;margin-top:6px">→ <strong>"{result}"</strong></div>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{inner}</div></div>'
        f'{cap}</figure>'
    )


def decision_diamond_diagram(
    question: str,
    *,
    yes_label: str = "True",
    no_label: str = "False",
    yes_result: str = "",
    no_result: str = "",
    caption: str = "",
) -> str:
    """The core recurring Chapter 9 visual: one question in a diamond,
    branching down-left to a True/Да outcome and down-right to a False/Нет
    outcome. Used for every single-condition decision throughout the
    chapter (age >= 18?, temperature < 0?, the first if, if/else, ...)."""
    q_lines = _wrap_svg_text(" ".join(question.split()), max_chars=15, max_lines=3)
    dia_w, dia_base_h = 240, 100
    dia_h = dia_base_h + (len(q_lines) - 1) * 20
    box_w, box_h, gap = 190, 76, 90

    total_w = max(2 * box_w + gap, dia_w + 40)
    cx = total_w / 2
    dia_top, dia_bottom = 10, 10 + dia_h
    dia_cy = (dia_top + dia_bottom) / 2
    left_v = (cx - dia_w / 2, dia_cy)
    right_v = (cx + dia_w / 2, dia_cy)

    boxes_y = dia_bottom + 56
    left_x = cx - gap / 2 - box_w
    right_x = cx + gap / 2
    left_cx, right_cx = left_x + box_w / 2, right_x + box_w / 2
    total_h = boxes_y + box_h + 10

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
        "<defs><marker id='arrowdd' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>"
    ]
    parts.append(
        f'<polygon data-flow-shape="decision" '
        f'points="{cx},{dia_top} {right_v[0]},{dia_cy} {cx},{dia_bottom} {left_v[0]},{dia_cy}" '
        f'fill="#5B24F9" stroke="#3B0FBF" stroke-width="2"/>'
    )
    q_first_y = dia_cy - (len(q_lines) - 1) * 10 + 5
    q_tspans = "".join(
        f'<tspan x="{cx}" y="{q_first_y + li * 20}">{html.escape(line)}</tspan>' for li, line in enumerate(q_lines)
    )
    parts.append(
        f'<text text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" '
        f'font-size="15" fill="#fff">{q_tspans}</text>'
    )
    parts.append(
        f'<path d="M{left_v[0]},{left_v[1]} H{left_cx} V{boxes_y}" fill="none" stroke="#059669" '
        f'stroke-width="2.5" marker-end="url(#arrowdd)"/>'
    )
    parts.append(
        f'<path d="M{right_v[0]},{right_v[1]} H{right_cx} V{boxes_y}" fill="none" stroke="#DB2777" '
        f'stroke-width="2.5" marker-end="url(#arrowdd)"/>'
    )
    mid_left = ((left_v[0] + left_cx) / 2, left_v[1] - 12)
    mid_right = ((right_v[0] + right_cx) / 2, right_v[1] - 12)
    parts.append(
        f'<text x="{mid_left[0]}" y="{mid_left[1]}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="13" fill="#059669">{html.escape(yes_label)}</text>'
    )
    parts.append(
        f'<text x="{mid_right[0]}" y="{mid_right[1]}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="13" fill="#DB2777">{html.escape(no_label)}</text>'
    )
    for x, cxb, result, color, fill in (
        (left_x, left_cx, yes_result, "#059669", "#DCFCE7"),
        (right_x, right_cx, no_result, "#DB2777", "#FCE7F3"),
    ):
        skew = 18
        x1 = x + box_w
        parts.append(
            f'<polygon data-flow-shape="input-output" '
            f'points="{x + skew},{boxes_y} {x1},{boxes_y} {x1 - skew},{boxes_y + box_h} {x},{boxes_y + box_h}" '
            f'fill="{fill}" stroke="{color}" stroke-width="2"/>'
        )
        r_lines = _wrap_svg_text(" ".join(result.split()), max_chars=20, max_lines=3)
        r_first_y = boxes_y + box_h / 2 - (len(r_lines) - 1) * 9 + 5
        r_tspans = "".join(
            f'<tspan x="{cxb}" y="{r_first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(r_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="13" '
            f'fill="#0D0230">{r_tspans}</text>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def elif_ladder_diagram(steps: list[tuple[str, str]], *, else_label: str = "", caption: str = "") -> str:
    """Vertical cascade of conditions — condition 1, and if False, condition
    2, and so on — with each True branch peeling off to the right to a
    labeled result, and the final False falling through to else_label (if
    given). Used for if/elif/else, elif ordering, and the Guess-the-Number
    decision tree."""
    dia_w, dia_h = 220, 64
    box_w, box_h = 190, 60
    row_gap = 46
    col_gap = 60

    n = len(steps)
    total_w = dia_w + col_gap + box_w + 20
    dia_cx = 10 + dia_w / 2
    total_h = 10 + n * (dia_h + row_gap) + (box_h + 30 if else_label else 0)

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
        "<defs><marker id='arrowel' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>"
    ]
    y = 10
    for i, (cond, result) in enumerate(steps):
        top, bottom = y, y + dia_h
        cy = (top + bottom) / 2
        left_v = (dia_cx - dia_w / 2, cy)
        right_v = (dia_cx + dia_w / 2, cy)
        parts.append(
            f'<polygon data-flow-shape="decision" '
            f'points="{dia_cx},{top} {right_v[0]},{cy} {dia_cx},{bottom} {left_v[0]},{cy}" '
            f'fill="#5B24F9" stroke="#3B0FBF" stroke-width="2"/>'
        )
        c_lines = _wrap_svg_text(" ".join(cond.split()), max_chars=17, max_lines=2)
        c_first_y = cy - (len(c_lines) - 1) * 9 + 5
        c_tspans = "".join(
            f'<tspan x="{dia_cx}" y="{c_first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(c_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" font-size="13" '
            f'fill="#fff">{c_tspans}</text>'
        )
        box_x = dia_cx + dia_w / 2 + col_gap
        box_cx = box_x + box_w / 2
        parts.append(
            f'<path d="M{right_v[0]},{cy} L{box_x},{cy}" fill="none" stroke="#059669" stroke-width="2.5" '
            f'marker-end="url(#arrowel)"/>'
        )
        parts.append(
            f'<text x="{(right_v[0] + box_x) / 2}" y="{cy - 10}" text-anchor="middle" '
            f'font-family="JetBrains Mono, monospace" font-weight="700" font-size="12" fill="#059669">True</text>'
        )
        result_top = cy - box_h / 2
        result_skew = 16
        parts.append(
            f'<polygon data-flow-shape="input-output" '
            f'points="{box_x + result_skew},{result_top} {box_x + box_w},{result_top} '
            f'{box_x + box_w - result_skew},{result_top + box_h} {box_x},{result_top + box_h}" '
            f'fill="#DCFCE7" stroke="#059669" stroke-width="2"/>'
        )
        r_lines = _wrap_svg_text(" ".join(result.split()), max_chars=20, max_lines=2)
        r_first_y = cy - (len(r_lines) - 1) * 9 + 5
        r_tspans = "".join(
            f'<tspan x="{box_cx}" y="{r_first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(r_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="13" '
            f'fill="#0D0230">{r_tspans}</text>'
        )
        next_top = bottom + row_gap
        if i < n - 1 or else_label:
            arrow_bottom = next_top if i < n - 1 else next_top
            parts.append(
                f'<path d="M{dia_cx},{bottom} L{dia_cx},{arrow_bottom}" fill="none" stroke="#DB2777" '
                f'stroke-width="2.5" marker-end="url(#arrowel)"/>'
            )
            parts.append(
                f'<text x="{dia_cx + 14}" y="{(bottom + arrow_bottom) / 2 + 4}" '
                f'font-family="JetBrains Mono, monospace" font-weight="700" font-size="12" fill="#DB2777">False</text>'
            )
        y = next_top
    if else_label:
        el_lines = _wrap_svg_text(" ".join(else_label.split()), max_chars=22, max_lines=2)
        el_cy = y + box_h / 2
        el_first_y = el_cy - (len(el_lines) - 1) * 9 + 5
        el_tspans = "".join(
            f'<tspan x="{dia_cx}" y="{el_first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(el_lines)
        )
        parts.append(
            f'<rect data-flow-shape="process" x="{dia_cx - box_w / 2}" y="{y}" '
            f'width="{box_w}" height="{box_h}" rx="2" fill="#EDE9FE" '
            f'stroke="#5B24F9" stroke-width="2" stroke-dasharray="5 4"/>'
        )
        parts.append(
            f'<text text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="13" '
            f'fill="#0D0230">{el_tspans}</text>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def comparison_number_line(
    *,
    axis_lo: float,
    axis_hi: float,
    lo_bound: float | None = None,
    hi_bound: float | None = None,
    lo_inclusive: bool = True,
    hi_inclusive: bool = True,
    caption: str = "",
) -> str:
    """Horizontal number line shading the region that satisfies a
    comparison. Pass only lo_bound for "value >= / > lo_bound" (shades
    right of it); only hi_bound for "value < / <= hi_bound" (shades left of
    it); both for a chained/range comparison (shades between them). Filled
    circle = inclusive boundary (>=, <=); open circle = exclusive (>, <)."""
    total_w, pad = 640, 50
    usable = total_w - 2 * pad
    y = 70
    total_h = 110

    def x_of(v: float) -> float:
        return pad + (v - axis_lo) / (axis_hi - axis_lo) * usable

    shade_lo = x_of(lo_bound) if lo_bound is not None else x_of(axis_lo)
    shade_hi = x_of(hi_bound) if hi_bound is not None else x_of(axis_hi)

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="number-line" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
        "<defs><marker id='arrownc' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>"
    ]
    parts.append(
        f'<line x1="{pad - 8}" y1="{y}" x2="{total_w - pad + 8}" y2="{y}" stroke="#E4E1F5" stroke-width="4" '
        f'marker-end="url(#arrownc)"/>'
    )
    parts.append(f'<line x1="{shade_lo}" y1="{y}" x2="{shade_hi}" y2="{y}" stroke="#5B24F9" stroke-width="6"/>')

    def boundary(x: float, value: float, inclusive: bool) -> None:
        fill = "#5B24F9" if inclusive else "#FAFAFC"
        parts.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{fill}" stroke="#5B24F9" stroke-width="2.5"/>')
        label = _fmt_num(value)
        parts.append(
            f'<text x="{x}" y="{y - 20}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
            f'font-weight="700" font-size="14" fill="#0D0230">{html.escape(label)}</text>'
        )

    if lo_bound is not None:
        boundary(x_of(lo_bound), lo_bound, lo_inclusive)
    if hi_bound is not None:
        boundary(x_of(hi_bound), hi_bound, hi_inclusive)

    label_y = y + 32
    if lo_bound is not None and hi_bound is None:
        parts.append(f'<text x="{(pad + shade_lo) / 2}" y="{label_y}" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" fill="#8A8A9A">False</text>')
        parts.append(f'<text x="{(shade_lo + total_w - pad) / 2}" y="{label_y}" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="12" fill="#059669">True</text>')
    elif hi_bound is not None and lo_bound is None:
        parts.append(f'<text x="{(pad + shade_hi) / 2}" y="{label_y}" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="12" fill="#059669">True</text>')
        parts.append(f'<text x="{(shade_hi + total_w - pad) / 2}" y="{label_y}" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" fill="#8A8A9A">False</text>')
    elif lo_bound is not None and hi_bound is not None:
        parts.append(f'<text x="{(shade_lo + shade_hi) / 2}" y="{label_y}" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="12" fill="#059669">True</text>')
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def _fmt_num(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else str(v)


# ---------------------------------------------------------------------------
# Conventional flowchart primitives (terminator/process/input-output/decision)
# ---------------------------------------------------------------------------
# Shared by flowchart(), condition_cascade() and loop_preview_diagram() so
# every algorithm/control-flow diagram in the course uses the same visual
# vocabulary: rounded PILL = start/end, RECTANGLE = process/action,
# PARALLELOGRAM = input/output, DIAMOND = decision. Shape carries meaning —
# never rely on color alone (see accessibility note in each caption).

_FC_TERM_W, _FC_TERM_H = 190, 52
_FC_PROC_W, _FC_PROC_H = 210, 56
_FC_IO_W, _FC_IO_H = 220, 56
_FC_IO_SKEW = 22
_FC_DEC_W, _FC_DEC_H = 230, 100
_FC_GAP_Y = 26
_FC_BRANCH_GAP = 32
_FC_MERGE_GAP = 32
_FC_BRANCH_OFFSET = 200

_fc_id_counter = itertools.count()


def _fc_new_marker_id() -> str:
    """A fresh marker id per diagram instance — pages routinely embed
    several flowchart()/condition_cascade()/loop_preview_diagram() figures,
    and each one's own <defs><marker id=...> must be unique across the
    whole HTML document, not just within its own <svg>."""
    return f"arrowfc{next(_fc_id_counter)}"


_FC_ARROW_COLORS = {"#B9A0FC": "", "#059669": "-g", "#DB2777": "-p", "#5B24F9": "-v"}


def _fc_marker_ref(marker_id: str, color: str) -> str:
    """Arrowhead markers are per-color (see _fc_arrow_defs) so a green ДА
    arrow gets a green arrowhead, not a mismatched default one."""
    return f"{marker_id}{_FC_ARROW_COLORS.get(color, '')}"


def _fc_arrow_defs(marker_id: str) -> str:
    markers = "".join(
        f"<marker id='{marker_id}{suffix}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
        f"orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{color}'/></marker>"
        for color, suffix in _FC_ARROW_COLORS.items()
    )
    return f"<defs>{markers}</defs>"


def _fc_node_height(kind: str, label: str) -> float:
    if kind in ("start", "end"):
        return _FC_TERM_H
    if kind == "process":
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=22, max_lines=2)
        return max(_FC_PROC_H, 26 + len(lines) * 20)
    if kind in ("input", "output"):
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=20, max_lines=2)
        return max(_FC_IO_H, 26 + len(lines) * 20)
    if kind == "decision":
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=15, max_lines=3)
        return max(_FC_DEC_H, 60 + len(lines) * 20)
    raise ValueError(f"unknown flowchart node kind: {kind}")


def _fc_node_width(kind: str) -> float:
    return {
        "start": _FC_TERM_W, "end": _FC_TERM_W, "process": _FC_PROC_W,
        "input": _FC_IO_W, "output": _FC_IO_W, "decision": _FC_DEC_W,
    }[kind]


def _fc_draw_node(parts: list[str], kind: str, label: str, cx: float, top: float) -> None:
    h = _fc_node_height(kind, label)
    w = _fc_node_width(kind)
    cy = top + h / 2
    if kind in ("start", "end"):
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=22, max_lines=2)
        parts.append(
            f'<rect data-flow-shape="terminator" x="{cx - w/2}" y="{top}" width="{w}" height="{h}" '
            f'rx="{h/2}" fill="#0D0230" stroke="#5B24F9" stroke-width="2"/>'
        )
        color, family, weight, size = "#fff", "Sora, sans-serif", "700", 14
    elif kind == "process":
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=22, max_lines=2)
        parts.append(
            f'<rect data-flow-shape="process" x="{cx - w/2}" y="{top}" width="{w}" height="{h}" '
            f'rx="2" fill="#EDE9FE" stroke="#5B24F9" stroke-width="2"/>'
        )
        color, family, weight, size = "#0D0230", "'JetBrains Mono', monospace", "600", 13
    elif kind in ("input", "output"):
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=20, max_lines=2)
        skew = _FC_IO_SKEW
        x0, x1 = cx - w / 2, cx + w / 2
        points = f"{x0 + skew},{top} {x1},{top} {x1 - skew},{top + h} {x0},{top + h}"
        fill = "#DBEAFE" if kind == "input" else "#DCFCE7"
        stroke = "#2563EB" if kind == "input" else "#059669"
        parts.append(
            f'<polygon data-flow-shape="input-output" points="{points}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
        color, family, weight, size = "#0D0230", "'JetBrains Mono', monospace", "600", 13
    elif kind == "decision":
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=15, max_lines=3)
        top_v, right_v, bot_v, left_v = (cx, top), (cx + w / 2, cy), (cx, top + h), (cx - w / 2, cy)
        parts.append(
            f'<polygon data-flow-shape="decision" '
            f'points="{top_v[0]},{top_v[1]} {right_v[0]},{right_v[1]} '
            f'{bot_v[0]},{bot_v[1]} {left_v[0]},{left_v[1]}" '
            f'fill="#5B24F9" stroke="#3B0FBF" stroke-width="2"/>'
        )
        color, family, weight, size = "#fff", "Sora, sans-serif", "700", 13
    else:
        raise ValueError(f"unknown flowchart node kind: {kind}")
    first_y = cy - (len(lines) - 1) * 9 + 5
    tspans = "".join(
        f'<tspan x="{cx}" y="{first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(lines)
    )
    parts.append(
        f'<text text-anchor="middle" font-family="{family}" font-weight="{weight}" '
        f'font-size="{size}" fill="{color}">{tspans}</text>'
    )


def _fc_arrow(
    parts: list[str],
    mid: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: str = "#B9A0FC",
    route: str = "auto",
    arrowhead: bool = True,
    mid_x: float | None = None,
    mid_y: float | None = None,
) -> None:
    """Draw an arrow using only orthogonal (horizontal/vertical) segments.

    ``route`` controls the first and last segment when endpoints are not
    aligned: ``hv`` leaves horizontally and enters vertically, ``vh`` leaves
    vertically and enters horizontally, ``hvh`` enters horizontally, and
    ``vhv`` enters vertically.  Curves and diagonal shortcuts are forbidden
    for course block diagrams.

    For ``hvh``/``vhv``, the turn point defaults to the arithmetic midpoint
    between the two endpoints, but callers that need the elbow to clear a
    specific x (``hvh``) or y (``vhv``) — e.g. routing a branch OUT and away
    from a shape's edge before turning back in, instead of cutting straight
    across it — may pass ``mid_x``/``mid_y`` explicitly.
    """
    if x1 == x2 and y1 == y2:
        return

    marker = _fc_marker_ref(mid, color)
    marker_attr = f' marker-end="url(#{marker})"' if arrowhead else ""
    if x1 == x2 or y1 == y2:
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="2.5"{marker_attr}/>'
        )
        return

    if route == "auto":
        route = "vhv"
    if route == "hv":
        path = f"M{x1},{y1} H{x2} V{y2}"
    elif route == "vh":
        path = f"M{x1},{y1} V{y2} H{x2}"
    elif route == "hvh":
        mx = mid_x if mid_x is not None else (x1 + x2) / 2
        path = f"M{x1},{y1} H{mx} V{y2} H{x2}"
    elif route == "vhv":
        my = mid_y if mid_y is not None else (y1 + y2) / 2
        path = f"M{x1},{y1} V{my} H{x2} V{y2}"
    else:
        raise ValueError(f"unknown orthogonal route: {route}")
    parts.append(
        f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.5" '
        f'stroke-linejoin="miter"{marker_attr}/>'
    )


def _fc_label(parts: list[str], x: float, y: float, text: str, color: str, *, anchor: str = "middle") -> None:
    parts.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="12" fill="{color}">{html.escape(text)}</text>'
    )


def flowchart(
    steps: list[dict],
    *,
    yes_label: str = "ДА",
    no_label: str = "НЕТ",
    caption: str = "",
) -> str:
    """Recursive top-down flowchart with conventional shape semantics —
    the single reusable primitive behind every algorithm/control-flow
    diagram in Chapter 9. Each step is a dict:

      {"kind": "start"|"end"|"process"|"input"|"output", "label": str}
      {"kind": "decision", "label": str, "yes": [steps], "no": [steps],
       "yes_label": optional override, "no_label": optional override}

    A decision's "yes"/"no" branches are laid out side by side and
    automatically merge back into the continuing flow below — the reader
    never has to wonder whether a branch just stops. An empty/omitted
    branch list means "nothing happens on this path": drawn as a single
    direct, labeled bypass arrow from the diamond straight to the merge
    point, showing that the block is skipped, not that the program halts.

    A branch whose LAST step has kind "end" is terminal: it is drawn with
    no outgoing arrow and is excluded from the merge below the decision —
    it truly stops there, it does not rejoin the continuing flow. If both
    branches of a decision terminate this way, the decision has no
    continuation at all (nothing merges, nothing is drawn below it).
    """
    parts: list[str] = []
    mid = _fc_new_marker_id()
    bounds = {"min_x": 0.0, "max_x": 0.0, "max_y": 0.0}

    def track(x0: float, x1: float, y1: float) -> None:
        bounds["min_x"] = min(bounds["min_x"], x0)
        bounds["max_x"] = max(bounds["max_x"], x1)
        bounds["max_y"] = max(bounds["max_y"], y1)

    def draw(kind: str, label: str, cx: float, top: float) -> float:
        h = _fc_node_height(kind, label)
        w = _fc_node_width(kind)
        track(cx - w / 2, cx + w / 2, top + h)
        _fc_draw_node(parts, kind, label, cx, top)
        return h

    def render(steps_list: list[dict], cx: float, y: float) -> float | None:
        prev_bottom: float | None = None
        entered = False
        for step in steps_list:
            entered = True
            kind = step["kind"]
            label = step.get("label", "")
            if kind == "decision":
                if prev_bottom is not None:
                    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
                h = draw("decision", label, cx, y)
                w = _FC_DEC_W
                dia_cy = y + h / 2
                dia_bottom = y + h
                left_vx, right_vx = cx - w / 2, cx + w / 2
                left_x, right_x = cx - _FC_BRANCH_OFFSET, cx + _FC_BRANCH_OFFSET
                branch_top = dia_bottom + _FC_BRANCH_GAP
                yes_steps = step.get("yes") or []
                no_steps = step.get("no") or []
                yl = step.get("yes_label", yes_label)
                nl = step.get("no_label", no_label)

                if yes_steps:
                    _fc_arrow(parts, mid, left_vx, dia_cy, left_x, branch_top, route="hv", color="#059669")
                    _fc_label(parts, (left_vx + left_x) / 2, dia_cy - 12, yl, "#059669")
                    yes_bottom = render(yes_steps, left_x, branch_top)
                else:
                    yes_bottom = dia_cy
                if no_steps:
                    _fc_arrow(parts, mid, right_vx, dia_cy, right_x, branch_top, route="hv", color="#DB2777")
                    _fc_label(parts, (right_vx + right_x) / 2, dia_cy - 12, nl, "#DB2777")
                    no_bottom = render(no_steps, right_x, branch_top)
                else:
                    no_bottom = dia_cy

                # A branch ending in an "end" node is terminal — render() returns
                # None for it, so it draws no outgoing arrow and never rejoins
                # the merge below. Only non-terminal branches contribute.
                continuing = [b for b in (yes_bottom, no_bottom) if b is not None]
                if not continuing:
                    prev_bottom = None
                    y = dia_bottom
                elif len(continuing) == 1:
                    # Only one branch continues — nothing to merge it WITH, so pass
                    # its endpoint straight through instead of drawing a stub arrow
                    # to an empty merge point that nothing else ever reaches.
                    prev_bottom = continuing[0]
                    y = prev_bottom
                else:
                    merge_y = max(continuing + [dia_bottom]) + _FC_MERGE_GAP
                    if yes_bottom is not None:
                        if yes_steps:
                            _fc_arrow(
                                parts, mid, left_x, yes_bottom, cx, merge_y,
                                route="vh", arrowhead=False,
                            )
                        else:
                            # Empty branch: this single "hvh" segment is the ONLY
                            # connector drawn for the whole bypass path. It stays
                            # arrowhead=False like every other segment feeding the
                            # merge collector below — the junction dot drawn at
                            # (cx, merge_y) is what marks "flows meet here", and the
                            # one arrow leaving that dot toward the next block is the
                            # only arrowhead this junction needs.
                            # Route the elbow OUT through left_x (the same offset a
                            # non-empty branch's node column would sit at) instead of
                            # the plain midpoint: the plain midpoint sits INSIDE the
                            # vertex (between it and center), so the line cuts back
                            # toward the diamond immediately instead of bulging away
                            # from it first — reads as backward routing regardless of
                            # any arrowhead.
                            track(left_x, left_x, merge_y)
                            _fc_arrow(
                                parts, mid, left_vx, dia_cy, cx, merge_y,
                                route="hvh", color="#059669", mid_x=left_x,
                                arrowhead=False,
                            )
                            # Label sits over the vertex->left_x exit segment, the
                            # same placement convention as the non-empty branch case
                            # above (label right next to the diamond, not out at the
                            # far merge collector).
                            _fc_label(parts, (left_vx + left_x) / 2, dia_cy - 12, yl, "#059669")
                    if no_bottom is not None:
                        if no_steps:
                            _fc_arrow(
                                parts, mid, right_x, no_bottom, cx, merge_y,
                                route="vh", arrowhead=False,
                            )
                        else:
                            # Same reasoning as the "yes" bypass above, mirrored: stays
                            # arrowhead=False, and routes OUT through right_x before
                            # turning down and back in, instead of cutting inward
                            # across the diamond's own footprint.
                            track(right_x, right_x, merge_y)
                            _fc_arrow(
                                parts, mid, right_vx, dia_cy, cx, merge_y,
                                route="hvh", color="#DB2777", mid_x=right_x,
                                arrowhead=False,
                            )
                            # Same placement convention as the "yes" bypass above.
                            _fc_label(parts, (right_vx + right_x) / 2, dia_cy - 12, nl, "#DB2777")
                    # The two branches join on one orthogonal collector. Mark the
                    # junction explicitly with a small filled dot — otherwise an
                    # unmarked T-meeting of two undecorated lines reads as
                    # ambiguous/reversed, especially on the side that bulged out
                    # and back in. The next iteration draws exactly one vertical
                    # arrow from this dot into the following block; that is the
                    # only arrowhead this junction needs.
                    parts.append(
                        f'<circle cx="{cx}" cy="{merge_y}" r="4.5" fill="#B9A0FC"/>'
                    )
                    y = merge_y + _FC_GAP_Y
                    prev_bottom = merge_y
            else:
                if prev_bottom is not None:
                    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
                h = draw(kind, label, cx, y)
                this_bottom = y + h
                # An "end" node is terminal: no outgoing arrow, and it must not
                # be mistaken for "nothing was drawn" by the caller.
                prev_bottom = None if kind == "end" else this_bottom
                y = this_bottom + _FC_GAP_Y
        return prev_bottom if entered else y

    render(steps, 0.0, 10.0)
    pad = 40
    min_x, max_x, max_y = bounds["min_x"] - pad, bounds["max_x"] + pad, bounds["max_y"] + pad
    width, height = max_x - min_x, max_y
    svg = (
        f'<svg viewBox="{min_x} 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{width:.0f}px">'
        f'{_fc_arrow_defs(mid)}{"".join(parts)}</svg>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def condition_cascade(
    conditions: list[tuple[str, str]],
    *,
    default_label: str,
    start_label: str = "СТАРТ",
    input_label: str | None = None,
    end_label: str = "КОНЕЦ",
    exit_label: str = "ДА",
    continue_label: str = "НЕТ",
    caption: str = "",
) -> str:
    """Vertical cascade of conditions (elif-ladder / short-circuit shape),
    built from the same shape vocabulary as flowchart(): each condition is
    tested in turn; the `exit_label` branch immediately peels off to its
    paired result and merges toward END, while the other branch falls
    through to the next condition. After the last condition, default_label
    executes unconditionally. Every result — peeled or default — visibly
    merges through a shared collector line into one END, so "first true
    wins, the rest is skipped" is impossible to misread."""
    parts: list[str] = []
    mid = _fc_new_marker_id()
    dia_w = _FC_DEC_W
    box_w, box_h = _FC_IO_W, _FC_IO_H
    col_gap = 70
    row_gap = 40

    cx = dia_w / 2 + 20
    box_x = cx + dia_w / 2 + col_gap
    box_cx = box_x + box_w / 2
    collector_x = box_x + box_w + 60

    y = 10.0
    h = _fc_node_height("start", start_label)
    _fc_draw_node(parts, "start", start_label, cx, y)
    prev_bottom = y + h
    y = prev_bottom + _FC_GAP_Y

    if input_label:
        _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
        h = _fc_node_height("input", input_label)
        _fc_draw_node(parts, "input", input_label, cx, y)
        prev_bottom = y + h
        y = prev_bottom + _FC_GAP_Y

    result_ys: list[float] = []
    max_box_bottom = prev_bottom
    for i, (cond, result) in enumerate(conditions):
        _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
        dh = _fc_node_height("decision", cond)
        _fc_draw_node(parts, "decision", cond, cx, y)
        dia_cy = y + dh / 2
        dia_bottom = y + dh

        _fc_arrow(parts, mid, cx + dia_w / 2, dia_cy, box_x, dia_cy, color="#059669")
        _fc_label(parts, (cx + dia_w / 2 + box_x) / 2, dia_cy - 10, exit_label, "#059669")
        box_h_actual = _fc_node_height("output", result)
        _fc_draw_node(parts, "output", result, box_cx, dia_cy - box_h_actual / 2)
        result_ys.append(dia_cy)
        max_box_bottom = max(max_box_bottom, dia_cy + box_h_actual / 2)

        prev_bottom = dia_bottom
        y = dia_bottom + row_gap
        _fc_label(parts, cx + 24, (dia_bottom + y) / 2, continue_label, "#DB2777")

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    dh = _fc_node_height("output", default_label)
    _fc_draw_node(parts, "output", default_label, cx, y)
    default_bottom = y + dh
    y = default_bottom + _FC_GAP_Y

    end_y = y
    eh = _fc_node_height("end", end_label)
    end_cy = end_y + eh / 2

    for by in result_ys:
        parts.append(f'<line x1="{box_x + box_w}" y1="{by}" x2="{collector_x}" y2="{by}" stroke="#B9A0FC" stroke-width="2"/>')
    top_collector_y = min(result_ys) if result_ys else end_cy
    parts.append(f'<line x1="{collector_x}" y1="{top_collector_y}" x2="{collector_x}" y2="{end_cy}" stroke="#B9A0FC" stroke-width="2"/>')
    _fc_arrow(parts, mid, collector_x, end_cy, cx + _FC_TERM_W / 2, end_cy, color="#B9A0FC")
    _fc_arrow(parts, mid, cx, default_bottom, cx, end_y)
    _fc_draw_node(parts, "end", end_label, cx, end_y)

    pad = 40
    min_x = -pad
    max_x = collector_x + pad
    max_y = end_y + eh + pad
    width, height = max_x - min_x, max_y
    svg = (
        f'<svg viewBox="{min_x} 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{width:.0f}px">'
        f'{_fc_arrow_defs(mid)}{"".join(parts)}</svg>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def loop_preview_diagram(*, action_label: str, question_label: str, caption: str = "") -> str:
    """One-off cyclic diagram for the repetition preview and the Chapter
    9 -> 10 bridge: START -> ACTION -> question? -> ДА loops visibly
    BACKWARD to ACTION again, НЕТ continues down to END. Loop syntax is
    deliberately not shown — only the shape of repetition itself."""
    parts: list[str] = []
    mid = _fc_new_marker_id()
    cx = 150.0

    y = 10.0
    h = _fc_node_height("start", "СТАРТ")
    _fc_draw_node(parts, "start", "СТАРТ", cx, y)
    prev_bottom = y + h
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    ph = _fc_node_height("process", action_label)
    proc_top = y
    _fc_draw_node(parts, "process", action_label, cx, y)
    prev_bottom = y + ph
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    dh = _fc_node_height("decision", question_label)
    _fc_draw_node(parts, "decision", question_label, cx, y)
    dia_cy = y + dh / 2
    dia_bottom = y + dh
    dia_right = cx + _FC_DEC_W / 2

    loop_x = dia_right + 110
    proc_cy = proc_top + ph / 2
    parts.append(
        f'<path d="M{dia_right},{dia_cy} L{loop_x},{dia_cy} L{loop_x},{proc_cy} L{cx + _FC_PROC_W / 2},{proc_cy}" '
        f'fill="none" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#{mid}-v)"/>'
    )
    _fc_label(parts, loop_x + 8, dia_cy - 10, "ДА — повторить", "#5B24F9", anchor="start")

    prev_bottom = dia_bottom
    y = dia_bottom + _FC_GAP_Y
    _fc_arrow(parts, mid, cx, prev_bottom, cx, y, color="#DB2777")
    _fc_label(parts, cx + 26, (prev_bottom + y) / 2, "НЕТ", "#DB2777")
    _fc_draw_node(parts, "end", "КОНЕЦ", cx, y)
    end_bottom = y + _fc_node_height("end", "КОНЕЦ")

    pad = 40
    min_x, max_x = cx - _FC_PROC_W / 2 - pad, loop_x + 150 + pad
    max_y = end_bottom + pad
    width, height = max_x - min_x, max_y
    svg = (
        f'<svg viewBox="{min_x} 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{width:.0f}px">'
        f'{_fc_arrow_defs(mid)}{"".join(parts)}</svg>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def for_loop_flowchart(source_label: str, item_label: str, body_label: str, *, caption: str = "") -> str:
    """Canonical FOR-loop flowchart: START -> get next item from
    source_label -> item_label exists? -> ДА: body_label, looping visibly
    BACK to "get next item" -> НЕТ: END. This is the one shape every for
    loop in the chapter maps onto — a for loop is repeatedly asking "is
    there a next item", not "run the body N times by magic"."""
    parts: list[str] = []
    mid = _fc_new_marker_id()
    cx = 160.0

    y = 10.0
    h = _fc_node_height("start", "СТАРТ")
    _fc_draw_node(parts, "start", "СТАРТ", cx, y)
    prev_bottom = y + h
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    get_next_label = f"Получить следующий элемент из {source_label}"
    ph = _fc_node_height("process", get_next_label)
    proc_top = y
    _fc_draw_node(parts, "process", get_next_label, cx, y)
    prev_bottom = y + ph
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    dh = _fc_node_height("decision", item_label)
    _fc_draw_node(parts, "decision", item_label, cx, y)
    dia_cy = y + dh / 2
    dia_bottom = y + dh
    dia_right = cx + _FC_DEC_W / 2

    body_x = dia_right + 130
    body_top = dia_cy - _fc_node_height("process", body_label) / 2
    _fc_arrow(parts, mid, dia_right, dia_cy, body_x - _FC_PROC_W / 2, dia_cy, color="#059669")
    _fc_label(parts, (dia_right + body_x - _FC_PROC_W / 2) / 2, dia_cy - 10, "ДА", "#059669")
    _fc_draw_node(parts, "process", body_label, body_x, body_top)

    loop_x = body_x + _FC_PROC_W / 2 + 60
    proc_cy = proc_top + ph / 2
    body_cy = body_top + _fc_node_height("process", body_label) / 2
    parts.append(
        f'<path d="M{body_x + _FC_PROC_W / 2},{body_cy} L{loop_x},{body_cy} L{loop_x},{proc_cy} '
        f'L{cx + _FC_PROC_W / 2},{proc_cy}" fill="none" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#{mid}-v)"/>'
    )
    _fc_label(parts, loop_x + 8, (body_cy + proc_cy) / 2, "назад", "#5B24F9", anchor="start")

    prev_bottom = dia_bottom
    y = dia_bottom + _FC_GAP_Y
    _fc_arrow(parts, mid, cx, prev_bottom, cx, y, color="#DB2777")
    _fc_label(parts, cx + 26, (prev_bottom + y) / 2, "НЕТ", "#DB2777")
    _fc_draw_node(parts, "end", "КОНЕЦ", cx, y)
    end_bottom = y + _fc_node_height("end", "КОНЕЦ")

    pad = 40
    min_x, max_x = cx - _FC_PROC_W / 2 - pad, loop_x + 150 + pad
    max_y = end_bottom + pad
    width, height = max_x - min_x, max_y
    svg = (
        f'<svg viewBox="{min_x} 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{width:.0f}px">'
        f'{_fc_arrow_defs(mid)}{"".join(parts)}</svg>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def while_loop_flowchart(init_label: str, condition_label: str, body_label: str, update_label: str, *, caption: str = "") -> str:
    """Canonical WHILE-loop flowchart: START -> INIT -> condition_label? ->
    ДА: body_label -> update_label, looping visibly BACK to the condition
    -> НЕТ: END. The three-part model (initialize / condition / update)
    is the reusable mental model for every while loop in the chapter."""
    parts: list[str] = []
    mid = _fc_new_marker_id()
    cx = 160.0

    y = 10.0
    h = _fc_node_height("start", "СТАРТ")
    _fc_draw_node(parts, "start", "СТАРТ", cx, y)
    prev_bottom = y + h
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    ih = _fc_node_height("process", init_label)
    _fc_draw_node(parts, "process", init_label, cx, y)
    prev_bottom = y + ih
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    dh = _fc_node_height("decision", condition_label)
    dia_top = y
    _fc_draw_node(parts, "decision", condition_label, cx, y)
    dia_cy = y + dh / 2
    dia_bottom = y + dh
    dia_right = cx + _FC_DEC_W / 2

    body_x = dia_right + 130
    body_h = _fc_node_height("process", body_label)
    body_top = dia_cy - body_h - 6
    _fc_arrow(
        parts, mid, dia_right, dia_cy, body_x - _FC_PROC_W / 2, body_top + body_h / 2,
        color="#059669", route="hvh",
    )
    _fc_label(parts, (dia_right + body_x - _FC_PROC_W / 2) / 2, dia_cy - 16, "ДА", "#059669")
    _fc_draw_node(parts, "process", body_label, body_x, body_top)
    body_cy = body_top + body_h / 2

    update_top = dia_cy + 6
    update_h = _fc_node_height("process", update_label)
    _fc_arrow(parts, mid, body_x, body_top + body_h, body_x, update_top)
    _fc_draw_node(parts, "process", update_label, body_x, update_top)
    update_cy = update_top + update_h / 2

    loop_x = body_x + _FC_PROC_W / 2 + 60
    parts.append(
        f'<path d="M{body_x + _FC_PROC_W / 2},{update_cy} L{loop_x},{update_cy} L{loop_x},{dia_cy} '
        f'L{dia_right},{dia_cy}" fill="none" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#{mid}-v)"/>'
    )
    _fc_label(parts, loop_x + 8, (update_cy + dia_cy) / 2, "назад", "#5B24F9", anchor="start")

    prev_bottom = dia_bottom
    y = dia_bottom + _FC_GAP_Y
    _fc_arrow(parts, mid, cx, prev_bottom, cx, y, color="#DB2777")
    _fc_label(parts, cx + 26, (prev_bottom + y) / 2, "НЕТ", "#DB2777")
    _fc_draw_node(parts, "end", "КОНЕЦ", cx, y)
    end_bottom = y + _fc_node_height("end", "КОНЕЦ")

    pad = 40
    min_x = cx - _FC_PROC_W / 2 - pad
    max_x = loop_x + 150 + pad
    max_y = max(end_bottom, update_top + update_h) + pad
    width, height = max_x - min_x, max_y
    svg = (
        f'<svg viewBox="{min_x} 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{width:.0f}px">'
        f'{_fc_arrow_defs(mid)}{"".join(parts)}</svg>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def break_continue_flowchart(kind: str, loop_label: str, condition_label: str, *, caption: str = "") -> str:
    """Shared shape for break (kind='break') and continue (kind='continue')
    inside a loop: START -> loop_label -> condition_label? -> ДА takes the
    action the keyword actually performs (break: exit straight to END,
    bypassing the rest of the loop; continue: jump straight BACK to
    loop_label, skipping the rest of the body) -> НЕТ: the rest of the
    body runs, then loops back to loop_label as usual."""
    is_break = kind == "break"
    parts: list[str] = []
    mid = _fc_new_marker_id()
    cx = 160.0

    y = 10.0
    h = _fc_node_height("start", "СТАРТ")
    _fc_draw_node(parts, "start", "СТАРТ", cx, y)
    prev_bottom = y + h
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    lh = _fc_node_height("process", loop_label)
    loop_top = y
    _fc_draw_node(parts, "process", loop_label, cx, y)
    prev_bottom = y + lh
    y = prev_bottom + _FC_GAP_Y
    loop_cy = loop_top + lh / 2

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    dh = _fc_node_height("decision", condition_label)
    _fc_draw_node(parts, "decision", condition_label, cx, y)
    dia_cy = y + dh / 2
    dia_bottom = y + dh
    dia_right = cx + _FC_DEC_W / 2

    rest_x = cx
    rest_top = dia_bottom + _FC_BRANCH_GAP
    rest_label = "остальная часть тела" if is_break else "остальная часть тела"
    rh = _fc_node_height("process", rest_label)
    _fc_arrow(parts, mid, cx, dia_bottom, rest_x, rest_top, color="#DB2777")
    _fc_label(parts, cx - 40, (dia_bottom + rest_top) / 2, "НЕТ", "#DB2777")
    _fc_draw_node(parts, "process", rest_label, rest_x, rest_top)
    rest_bottom = rest_top + rh

    loop_x = dia_right + 150
    if is_break:
        end_top = rest_bottom + _FC_GAP_Y
        parts.append(
            f'<path d="M{dia_right},{dia_cy} L{loop_x},{dia_cy} L{loop_x},{end_top + _fc_node_height("end", "КОНЕЦ") / 2} '
            f'L{cx + _FC_TERM_W / 2},{end_top + _fc_node_height("end", "КОНЕЦ") / 2}" '
            f'fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#{mid}-g)"/>'
        )
        _fc_label(parts, loop_x + 8, dia_cy - 10, "ДА — break: выйти из цикла", "#059669", anchor="start")
        _fc_arrow(parts, mid, rest_x, rest_bottom, cx, rest_bottom + _FC_GAP_Y - 4, color="#5B24F9")
        # rest-of-body path loops back up to loop_label
        loop_back_x = cx - 150
        parts.append(
            f'<path d="M{rest_x - _FC_PROC_W / 2},{rest_top + rh / 2} L{loop_back_x},{rest_top + rh / 2} '
            f'L{loop_back_x},{loop_cy} L{cx - _FC_PROC_W / 2},{loop_cy}" fill="none" stroke="#5B24F9" '
            f'stroke-width="2.5" marker-end="url(#{mid}-v)"/>'
        )
        _fc_draw_node(parts, "end", "КОНЕЦ", cx, end_top)
        max_y_bottom = end_top + _fc_node_height("end", "КОНЕЦ") + 40
    else:
        parts.append(
            f'<path d="M{dia_right},{dia_cy} L{loop_x},{dia_cy} L{loop_x},{loop_cy} '
            f'L{cx + _FC_PROC_W / 2},{loop_cy}" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#{mid}-g)"/>'
        )
        _fc_label(parts, loop_x + 8, dia_cy - 10, "ДА — continue: сразу к следующему шагу", "#059669", anchor="start")
        loop_back_x = cx - 150
        parts.append(
            f'<path d="M{rest_x - _FC_PROC_W / 2},{rest_top + rh / 2} L{loop_back_x},{rest_top + rh / 2} '
            f'L{loop_back_x},{loop_cy} L{cx - _FC_PROC_W / 2},{loop_cy}" fill="none" stroke="#5B24F9" '
            f'stroke-width="2.5" marker-end="url(#{mid}-v)"/>'
        )
        max_y_bottom = rest_bottom + 40

    pad = 40
    min_x = min(cx - _FC_PROC_W / 2, loop_back_x if not is_break else cx - 150) - pad
    max_x = loop_x + 260 + pad
    width, height = max_x - min_x, max_y_bottom
    svg = (
        f'<svg viewBox="{min_x} 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{width:.0f}px">'
        f'{_fc_arrow_defs(mid)}{"".join(parts)}</svg>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def loop_else_flowchart(source_label: str, item_label: str, found_label: str, action_label: str, else_label: str, *, caption: str = "") -> str:
    """The for/else search shape: get next item -> item_label exists? ->
    НЕТ (the loop ran out of items without breaking): else_label runs,
    then END -> ДА: found_label? -> ДА: action_label, then break straight
    to END (skipping else) -> НЕТ: loop back for the next item. This is
    the one flowchart that makes `for ... else` legible."""
    parts: list[str] = []
    mid = _fc_new_marker_id()
    cx = 180.0

    y = 10.0
    h = _fc_node_height("start", "СТАРТ")
    _fc_draw_node(parts, "start", "СТАРТ", cx, y)
    prev_bottom = y + h
    y = prev_bottom + _FC_GAP_Y

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    get_next_label = f"Получить следующий элемент из {source_label}"
    ph = _fc_node_height("process", get_next_label)
    proc_top = y
    _fc_draw_node(parts, "process", get_next_label, cx, y)
    prev_bottom = y + ph
    y = prev_bottom + _FC_GAP_Y
    proc_cy = proc_top + ph / 2

    _fc_arrow(parts, mid, cx, prev_bottom, cx, y)
    dh1 = _fc_node_height("decision", item_label)
    _fc_draw_node(parts, "decision", item_label, cx, y)
    dia1_cy = y + dh1 / 2
    dia1_bottom = y + dh1
    dia1_left = cx - _FC_DEC_W / 2
    dia1_right = cx + _FC_DEC_W / 2

    else_x = cx - 220
    else_top = dia1_cy - _fc_node_height("output", else_label) / 2
    _fc_arrow(parts, mid, dia1_left, dia1_cy, else_x + _FC_IO_W / 2, dia1_cy, color="#DB2777")
    _fc_label(parts, (dia1_left + else_x + _FC_IO_W / 2) / 2, else_top - 10, "НЕТ", "#DB2777")
    _fc_draw_node(parts, "output", else_label, else_x, else_top)
    else_bottom = else_top + _fc_node_height("output", else_label)

    y2 = dia1_bottom + _FC_BRANCH_GAP
    _fc_arrow(parts, mid, cx, dia1_bottom, cx, y2, color="#059669")
    _fc_label(parts, cx + 26, (dia1_bottom + y2) / 2, "ДА", "#059669")
    dh2 = _fc_node_height("decision", found_label)
    _fc_draw_node(parts, "decision", found_label, cx, y2)
    dia2_cy = y2 + dh2 / 2
    dia2_bottom = y2 + dh2
    dia2_right = cx + _FC_DEC_W / 2

    action_x = cx + 230
    action_top = dia2_cy - _fc_node_height("output", action_label) / 2
    _fc_arrow(parts, mid, dia2_right, dia2_cy, action_x - _FC_IO_W / 2, dia2_cy, color="#059669")
    _fc_label(parts, (dia2_right + action_x - _FC_IO_W / 2) / 2, action_top - 10, "ДА", "#059669")
    _fc_draw_node(parts, "output", action_label, action_x, action_top)

    end_x = (else_x + action_x) / 2
    end_top = max(else_bottom, action_top + _fc_node_height("output", action_label)) + _FC_GAP_Y + 20
    parts.append(
        f'<line x1="{else_x}" y1="{else_bottom}" x2="{else_x}" y2="{end_top + _fc_node_height("end", "КОНЕЦ") / 2}" stroke="#B9A0FC" stroke-width="2"/>'
    )
    action_bottom = action_top + _fc_node_height("output", action_label)
    parts.append(
        f'<line x1="{action_x}" y1="{action_bottom}" x2="{action_x}" y2="{end_top + _fc_node_height("end", "КОНЕЦ") / 2}" stroke="#B9A0FC" stroke-width="2"/>'
    )
    parts.append(
        f'<line x1="{else_x}" y1="{end_top + _fc_node_height("end", "КОНЕЦ") / 2}" x2="{action_x}" y2="{end_top + _fc_node_height("end", "КОНЕЦ") / 2}" stroke="#B9A0FC" stroke-width="2"/>'
    )
    _fc_arrow(parts, mid, end_x, end_top + _fc_node_height("end", "КОНЕЦ") / 2, end_x, end_top)
    _fc_draw_node(parts, "end", "КОНЕЦ", end_x, end_top)
    end_bottom = end_top + _fc_node_height("end", "КОНЕЦ")

    loop_x = action_x + _FC_IO_W / 2 + 60
    parts.append(
        f'<path d="M{dia2_right},{dia2_cy + 6} L{loop_x},{dia2_cy + 6} L{loop_x},{proc_cy} '
        f'L{cx + _FC_PROC_W / 2},{proc_cy}" fill="none" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#{mid}-v)"/>'
    )
    _fc_label(parts, loop_x + 8, (dia2_cy + proc_cy) / 2, "НЕТ — назад", "#5B24F9", anchor="start")

    pad = 40
    min_x = else_x - _FC_IO_W / 2 - pad
    max_x = loop_x + 150 + pad
    max_y = max(end_bottom, action_top + _fc_node_height("output", action_label)) + pad
    width, height = max_x - min_x, max_y
    svg = (
        f'<svg viewBox="{min_x} 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="flowchart" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{width:.0f}px">'
        f'{_fc_arrow_defs(mid)}{"".join(parts)}</svg>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def nested_loop_grid(rows: int, cols: int, *, row_label: str = "строка", col_label: str = "столбец", caption: str = "") -> str:
    """Simple dot-grid visual for nested loops — rows × cols dots, labeled
    axes. Deliberately NOT a flowchart (per the "prefer clarity over
    formal graph complexity" rule): the grid itself is the clearest way to
    show what an outer/inner loop pair actually iterates over."""
    cell = 46
    pad_left, pad_top = 70, 50
    total_w = pad_left + cols * cell + 40
    total_h = pad_top + rows * cell + 50
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        f'<text x="{pad_left + cols * cell / 2}" y="20" text-anchor="middle" font-family="Sora, sans-serif" '
        f'font-weight="700" font-size="13" fill="#5B24F9">внутренний цикл — {html.escape(col_label)} →</text>'
    )
    parts.append(
        f'<text x="18" y="{pad_top + rows * cell / 2}" text-anchor="middle" font-family="Sora, sans-serif" '
        f'font-weight="700" font-size="13" fill="#DB2777" transform="rotate(-90 18 {pad_top + rows * cell / 2})">'
        f'внешний цикл — {html.escape(row_label)} ↓</text>'
    )
    for r in range(rows):
        for c in range(cols):
            cx = pad_left + c * cell + cell / 2
            cy = pad_top + r * cell + cell / 2
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#5B24F9"/>')
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def range_diagram(*, start: int, stop: int, step: int = 1, caption: str = "") -> str:
    """Dots-and-arrows progression visual for range(start, stop, step):
    a filled dot per value actually produced, a connecting arrow labeled
    with the step where it isn't 1, and stop drawn as a faded, unfilled
    dot past the last real value — visibly excluded, never reached."""
    values = list(range(start, stop, step)) if step != 0 else []
    n = max(len(values), 1)
    slot = 78
    pad = 50
    total_w = pad * 2 + slot * n + (40 if step != 1 else 0)
    total_h = 110
    y = 55
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
        "<defs><marker id='arrowrd' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>"
    ]
    xs = [pad + i * slot for i in range(n)]
    for i, v in enumerate(values):
        x = xs[i]
        if i > 0:
            parts.append(f'<line x1="{xs[i-1] + 10}" y1="{y}" x2="{x - 10}" y2="{y}" stroke="#B9A0FC" stroke-width="2.5" marker-end="url(#arrowrd)"/>')
            if step not in (1,):
                parts.append(
                    f'<text x="{(xs[i-1] + x) / 2}" y="{y - 12}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
                    f'font-weight="700" font-size="11" fill="#5B24F9">{"+" if step > 0 else ""}{step}</text>'
                )
        parts.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#5B24F9"/>')
        parts.append(
            f'<text x="{x}" y="{y + 30}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
            f'font-weight="700" font-size="14" fill="#0D0230">{v}</text>'
        )
    stop_x = (xs[-1] if values else pad) + slot
    if values:
        parts.append(f'<line x1="{xs[-1] + 10}" y1="{y}" x2="{stop_x - 10}" y2="{y}" stroke="#E4E1F5" stroke-width="2.5" stroke-dasharray="4 4"/>')
    parts.append(f'<circle cx="{stop_x}" cy="{y}" r="10" fill="#fff" stroke="#B9A0FC" stroke-width="2.5"/>')
    parts.append(
        f'<text x="{stop_x}" y="{y + 30}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-size="13" fill="#8A8A9A">{stop}</text>'
    )
    parts.append(
        f'<text x="{stop_x}" y="{y - 20}" text-anchor="middle" font-family="Inter, sans-serif" '
        f'font-size="11" fill="#8A8A9A">stop — исключён</text>'
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def precedence_ladder(levels: list[tuple[str, str]], *, caption: str = "") -> str:
    """HTML ladder of precedence levels, highest first. levels: list of
    (symbols, description), e.g. ("() ", "скобки — всегда первыми")."""
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:16px;padding:10px 16px;'
        f'background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);'
        f'border-radius:12px;margin-bottom:8px">'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:16px;'
        f'color:#5B24F9;min-width:64px">{html.escape(sym)}</div>'
        f'<div style="font-size:14px;color:#0D0230">{html.escape(desc)}</div>'
        f'</div>'
        for sym, desc in levels
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">{rows}{cap}</figure>'


def number_line_diagram(
    marks: list[tuple[float, str]],
    *,
    lo: float,
    hi: float,
    highlight: float | None = None,
    jumps: list[tuple[float, float, str]] | None = None,
    caption: str = "",
) -> str:
    """A horizontal number line from lo to hi with labeled tick marks —
    used for floor/ceil/trunc and negative floor-division explanations.
    marks: list of (position, label).
    jumps: optional list of (from, to, label) drawn as an orthogonal arrow
    above the line — for addition/subtraction ("start at 3, move 4, arrive
    at 7")."""
    total_w = 640
    pad = 40
    usable = total_w - 2 * pad
    jumps = jumps or []
    total_h = 110 + (46 if jumps else 0)
    y_offset = 46 if jumps else 0

    def x_of(v: float) -> float:
        return pad + (v - lo) / (hi - lo) * usable

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="number-line" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        "<defs><marker id='arrownl' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#5B24F9'/></marker></defs>"
    )
    y = 55 + y_offset
    parts.append(f'<line x1="{pad}" y1="{y}" x2="{total_w - pad}" y2="{y}" stroke="#B9A0FC" stroke-width="2.5"/>')
    for v in range(int(lo), int(hi) + 1):
        x = x_of(v)
        parts.append(f'<line x1="{x}" y1="{y - 6}" x2="{x}" y2="{y + 6}" stroke="#B9A0FC" stroke-width="2"/>')
        parts.append(
            f'<text x="{x}" y="{y + 24}" text-anchor="middle" font-family="Inter, sans-serif" '
            f'font-size="11" fill="#8A8A9A">{v}</text>'
        )
    for jfrom, jto, jlabel in jumps:
        x1, x2 = x_of(jfrom), x_of(jto)
        mid = (x1 + x2) / 2
        arc_h = y - 34
        parts.append(
            f'<path d="M{x1},{y - 8} V{arc_h} H{x2} V{y - 8}" fill="none" '
            f'stroke="#5B24F9" stroke-width="2.5" stroke-linejoin="miter" '
            f'marker-end="url(#arrownl)"/>'
        )
        parts.append(
            f'<text x="{mid}" y="{arc_h - 8}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
            f'font-weight="700" font-size="13" fill="#5B24F9">{html.escape(jlabel)}</text>'
        )
    for pos, label in marks:
        x = x_of(pos)
        filled = highlight is not None and abs(pos - highlight) < 1e-9
        parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{"#5B24F9" if filled else "#0D0230"}"/>')
        parts.append(
            f'<text x="{x}" y="{y - 16}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
            f'font-weight="700" font-size="13" fill="#0D0230">{html.escape(label)}</text>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def fraction_bar_diagram(numerator: int, denominator: int, *, caption: str = "") -> str:
    """A horizontal bar split into `denominator` equal segments, the first
    `numerator` of them filled — a visual for Fraction(numerator, denominator)."""
    denominator = max(denominator, 1)
    total_w, total_h = 420, 90
    bar_w = 360
    seg_w = bar_w / denominator
    bar_x = (total_w - bar_w) / 2
    bar_y = 20
    bar_h = 44
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    for i in range(denominator):
        x = bar_x + i * seg_w
        fill = "#5B24F9" if i < numerator else "#FAFAFC"
        parts.append(
            f'<rect x="{x}" y="{bar_y}" width="{seg_w}" height="{bar_h}" '
            f'fill="{fill}" stroke="#0D0230" stroke-width="1.2"/>'
        )
    parts.append(
        f'<text x="{total_w / 2}" y="{bar_y + bar_h + 26}" text-anchor="middle" '
        f'font-family="JetBrains Mono, monospace" font-weight="700" font-size="16" fill="#0D0230">'
        f'{numerator}/{denominator}</text>'
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def complex_plane_diagram(real: float, imag: float, *, caption: str = "") -> str:
    """Plots one point z = real + imag*j on a labeled complex plane."""
    total_w, total_h = 320, 320
    cx, cy = total_w / 2, total_h / 2
    scale = 30
    px = cx + real * scale
    py = cy - imag * scale
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        "<defs><marker id='arrowcx' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#0D0230'/></marker></defs>"
    )
    parts.append(f'<line x1="20" y1="{cy}" x2="{total_w - 12}" y2="{cy}" stroke="#0D0230" stroke-width="1.5" marker-end="url(#arrowcx)"/>')
    parts.append(f'<line x1="{cx}" y1="{total_h - 20}" x2="{cx}" y2="12" stroke="#0D0230" stroke-width="1.5" marker-end="url(#arrowcx)"/>')
    parts.append(f'<text x="{total_w - 16}" y="{cy - 8}" text-anchor="end" font-family="Inter, sans-serif" font-size="12" fill="#6B6B7D">real</text>')
    parts.append(f'<text x="{cx + 10}" y="20" font-family="Inter, sans-serif" font-size="12" fill="#6B6B7D">imaginary</text>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#B9A0FC" stroke-width="2" stroke-dasharray="4,4"/>')
    parts.append(f'<circle cx="{px}" cy="{py}" r="7" fill="#5B24F9"/>')
    label = f"({real:g}, {imag:g})"
    parts.append(
        f'<text x="{px + 12}" y="{py - 10}" font-family="JetBrains Mono, monospace" font-weight="700" '
        f'font-size="13" fill="#0D0230">z = {real:g}{"+" if imag >= 0 else "-"}{abs(imag):g}j</text>'
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def _dot_group_html(count: int) -> str:
    dots = "".join(
        '<span style="display:inline-block;width:14px;height:14px;border-radius:50%;'
        'background:#5B24F9;margin:2px"></span>'
        for _ in range(count)
    )
    return (
        '<div style="display:inline-flex;flex-wrap:wrap;max-width:120px;padding:8px;'
        'border:1.5px solid #5B24F9;border-radius:10px;background:var(--color-bg-canvas,#fff)">'
        f'{dots}</div>'
    )


def grouping_diagram(total: int, group_size: int, *, caption: str = "") -> str:
    """Dot-grouping visual for floor division / modulo, e.g. 17 objects into
    groups of 5 -> 3 full groups + a remainder group of 2. HTML/CSS, not
    SVG — a real grid of dots communicates "these things are being counted
    out and grouped" far better than an abstract box diagram."""
    full_groups = total // group_size
    remainder = total % group_size
    groups_html = "".join(_dot_group_html(group_size) for _ in range(full_groups))
    if remainder:
        groups_html += _dot_group_html(remainder)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    label = f'{total} // {group_size} = {full_groups}, {total} % {group_size} = {remainder}'
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">{groups_html}</div>'
        f'<div style="text-align:center;font-family:\'JetBrains Mono\',monospace;font-size:13px;'
        f'color:#0D0230;margin-top:12px">{html.escape(label)}</div>'
        f'{cap}</figure>'
    )


def rectangle_grid_diagram(width: int, height: int, *, caption: str = "") -> str:
    """Dot-grid rectangle for multiplication as area, e.g. 4 x 3 = 12 —
    HTML/CSS grid, one row per unit of height, one dot per unit of width."""
    rows = "".join(
        '<div style="display:flex;gap:6px;justify-content:center">'
        + "".join(
            '<span style="display:inline-block;width:16px;height:16px;border-radius:4px;'
            'background:#5B24F9"></span>'
            for _ in range(width)
        )
        + "</div>"
        for _ in range(height)
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    label = f'{width} × {height} = {width * height}'
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;flex-direction:column;gap:6px;align-items:center">{rows}</div>'
        f'<div style="text-align:center;font-family:\'JetBrains Mono\',monospace;font-size:13px;'
        f'color:#0D0230;margin-top:12px">{html.escape(label)}</div>'
        f'{cap}</figure>'
    )


def square_area_diagram(side: float, *, label_area: bool = True, caption: str = "") -> str:
    """A labeled square — side length on the edge, area inside — for
    x**2 (area from a side) and sqrt(area) (side from an area), used
    together so the two directions of the same picture teach both ideas."""
    area = side * side
    size_px = 140
    total_w, total_h = 220, 190
    x0 = (total_w - size_px) / 2
    y0 = 20
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(f'<rect x="{x0}" y="{y0}" width="{size_px}" height="{size_px}" rx="6" fill="#FAFAFC" stroke="#5B24F9" stroke-width="2"/>')
    if label_area:
        parts.append(
            f'<text x="{x0 + size_px / 2}" y="{y0 + size_px / 2 + 6}" text-anchor="middle" '
            f'font-family="JetBrains Mono, monospace" font-weight="700" font-size="18" fill="#0D0230">'
            f'{area:g}</text>'
        )
    parts.append(
        f'<text x="{x0 + size_px / 2}" y="{y0 + size_px + 22}" text-anchor="middle" '
        f'font-family="JetBrains Mono, monospace" font-size="13" fill="#5B24F9">сторона = {side:g}</text>'
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def right_triangle_diagram(a: float, b: float, c: float, *, caption: str = "") -> str:
    """A right triangle with legs a (horizontal), b (vertical) and
    hypotenuse c labeled — for math.hypot(). Scale is derived from a and b
    so the triangle always fills most of the canvas, whether the legs are
    small (3, 4) or larger — a fixed scale factor would either shrink small
    triangles to an unreadable speck or overflow the canvas for big ones."""
    total_w, total_h = 260, 200
    x0, y0 = 40, 170
    avail_w, avail_h = total_w - x0 - 50, y0 - 30
    scale = min(avail_w / max(a, 1e-9), avail_h / max(b, 1e-9))
    scale = max(min(scale, 30), 1)
    x1 = x0 + a * scale
    y1 = y0 - b * scale
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(f'<polygon points="{x0},{y0} {x1},{y0} {x1},{y1}" fill="#FAFAFC" stroke="#5B24F9" stroke-width="2"/>')
    parts.append(f'<rect x="{x1 - 12}" y="{y0 - 12}" width="12" height="12" fill="none" stroke="#B9A0FC" stroke-width="1.5"/>')
    parts.append(f'<text x="{(x0 + x1) / 2}" y="{y0 + 18}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13" fill="#0D0230">a = {a:g}</text>')
    parts.append(f'<text x="{x1 + 14}" y="{(y0 + y1) / 2}" text-anchor="start" font-family="JetBrains Mono, monospace" font-size="13" fill="#0D0230">b = {b:g}</text>')
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    parts.append(f'<text x="{mx - 18}" y="{my - 8}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="700" font-size="13" fill="#5B24F9">c = {c:g}</text>')
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def axis_compass_diagram(*, size: int = 560, caption: str = "") -> str:
    """A large, plain Cartesian axis compass — just the two axes, arrowheads
    pointing in all four directions, the origin marked, and +x/-x/+y/-y
    labels at each arrow tip. For introducing "this is how the coordinate
    system is oriented" before any points are plotted — for actual plotted
    points use coordinate_plane_diagram() instead. Deliberately large (the
    default 560px viewBox matches the ~500-620px desktop drawing width a
    diagram like this needs to read clearly at normal zoom) — a compass
    this simple has no excuse to ever look cramped."""
    total_w = size
    total_h = round(size * 0.68)
    cx, cy = total_w / 2, total_h / 2
    pad_x, pad_y = 44, 28
    x0, x1 = pad_x, total_w - pad_x
    y0, y1 = pad_y, total_h - pad_y
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        "<defs><marker id='arrowac' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='8' markerHeight='8' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#0D0230'/></marker></defs>"
    )
    parts.append(
        f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="#0D0230" stroke-width="2.5" '
        f'marker-start="url(#arrowac)" marker-end="url(#arrowac)"/>'
    )
    parts.append(
        f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y0}" stroke="#0D0230" stroke-width="2.5" '
        f'marker-start="url(#arrowac)" marker-end="url(#arrowac)"/>'
    )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#5B24F9"/>')
    parts.append(
        f'<text x="{cx + 14}" y="{cy + 24}" font-family="JetBrains Mono, monospace" font-weight="700" '
        f'font-size="17" fill="#5B24F9">(0, 0)</text>'
    )
    label_font = 'font-family="Sora, sans-serif" font-weight="700" font-size="22" fill="#0D0230"'
    parts.append(f'<text x="{x1 - 8}" y="{cy - 16}" text-anchor="end" {label_font}>+x</text>')
    parts.append(f'<text x="{x0 + 8}" y="{cy - 16}" text-anchor="start" {label_font}>-x</text>')
    parts.append(f'<text x="{cx + 16}" y="{y0 + 26}" text-anchor="start" {label_font}>+y</text>')
    parts.append(f'<text x="{cx + 16}" y="{y1 - 10}" text-anchor="start" {label_font}>-y</text>')
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:24px 20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'{svg}{cap}</figure>'
    )


def coordinate_plane_diagram(
    points: list[tuple[float, float, str]],
    *,
    circle_radius: float | None = None,
    lo: float = -5,
    hi: float = 5,
    caption: str = "",
) -> str:
    """A Cartesian x/y plane with labeled points, and an optional circle of
    given radius centered at the origin (for angle/unit-circle diagrams).
    points: list of (x, y, label)."""
    total_w = total_h = 320
    cx = cy = total_w / 2
    scale = (total_w / 2 - 30) / max(abs(lo), abs(hi))
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        "<defs><marker id='arrowcp' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#0D0230'/></marker></defs>"
    )
    parts.append(f'<line x1="18" y1="{cy}" x2="{total_w - 12}" y2="{cy}" stroke="#0D0230" stroke-width="1.5" marker-end="url(#arrowcp)"/>')
    parts.append(f'<line x1="{cx}" y1="{total_h - 18}" x2="{cx}" y2="12" stroke="#0D0230" stroke-width="1.5" marker-end="url(#arrowcp)"/>')
    parts.append(f'<text x="{total_w - 16}" y="{cy - 8}" text-anchor="end" font-family="Inter, sans-serif" font-size="12" fill="#6B6B7D">x</text>')
    parts.append(f'<text x="{cx + 10}" y="18" font-family="Inter, sans-serif" font-size="12" fill="#6B6B7D">y</text>')
    if circle_radius is not None:
        r_px = circle_radius * scale
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r_px}" fill="none" stroke="#B9A0FC" stroke-width="1.5" stroke-dasharray="4,4"/>')
    for x, y, label in points:
        px = cx + x * scale
        py = cy - y * scale
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#B9A0FC" stroke-width="2" stroke-dasharray="3,3"/>')
        parts.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#5B24F9"/>')
        # Anchor/offset the label away from whichever edge the point is near,
        # so it never runs off the canvas (e.g. a point near the right edge
        # gets a right-aligned label placed to its LEFT, not clipped text
        # spilling past the viewBox on the right).
        anchor = "start" if px <= cx else "end"
        label_x = px + 10 if anchor == "start" else px - 10
        label_y = py - 8 if py > 30 else py + 20
        parts.append(
            f'<text x="{label_x}" y="{label_y}" text-anchor="{anchor}" font-family="JetBrains Mono, monospace" '
            f'font-weight="700" font-size="12" fill="#0D0230">{html.escape(label)}</text>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def expression_tree(node: tuple, *, caption: str = "") -> str:
    """Recursive expression tree: node is either a leaf value (str/number)
    or a tuple (operator_label, left_node, right_node). Deeper subtrees are
    laid out with enough horizontal spacing that labels never collide —
    used for operator-precedence and associativity explanations, where
    SEEING which operation nests inside which is the entire point.
    """
    LEAF_W = 70

    def layout(n) -> tuple[list, float]:
        """Returns (list of (depth, cx, label, is_op), subtree_width)."""
        if not isinstance(n, tuple):
            return [(0, 0.0, str(n), False)], LEAF_W
        op, left, right = n
        left_items, left_w = layout(left)
        right_items, right_w = layout(right)
        gap = 20
        width = left_w + right_w + gap
        left_cx = left_w / 2
        right_cx = left_w + gap + right_w / 2
        root_cx = (left_cx + right_cx) / 2
        items = [(0, root_cx, op, True)]
        for depth, cx, label, is_op in left_items:
            items.append((depth + 1, cx, label, is_op))
        for depth, cx, label, is_op in right_items:
            items.append((depth + 1, cx, label, is_op))
        return items, width

    items, total_w_raw = layout(node)
    total_w = max(total_w_raw, 160)
    max_depth = max(depth for depth, *_ in items)
    row_h = 56
    total_h = (max_depth + 1) * row_h + 20

    # Re-derive child->parent lines by re-walking the tree structurally.
    def collect_edges(n, depth, cx, edges):
        if not isinstance(n, tuple):
            return
        op, left, right = n

        def subtree_w(m):
            if not isinstance(m, tuple):
                return LEAF_W
            _, l, r = m
            return subtree_w(l) + subtree_w(r) + 20

        lw, rw = subtree_w(left), subtree_w(right)
        left_cx = cx - (rw + 20) / 2
        right_cx = cx + (lw + 20) / 2
        edges.append((cx, depth, left_cx, depth + 1))
        edges.append((cx, depth, right_cx, depth + 1))
        collect_edges(left, depth + 1, left_cx, edges)
        collect_edges(right, depth + 1, right_cx, edges)

    root_cx = total_w / 2
    edges: list[tuple[float, int, float, int]] = []
    collect_edges(node, 0, root_cx, edges)

    def y_of(depth: int) -> float:
        return 20 + depth * row_h

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    for x1, d1, x2, d2 in edges:
        parts.append(f'<line x1="{x1}" y1="{y_of(d1) + 10}" x2="{x2}" y2="{y_of(d2) - 10}" stroke="#B9A0FC" stroke-width="2"/>')

    def render_items(n, depth, cx):
        if not isinstance(n, tuple):
            parts.append(
                f'<rect x="{cx - 26}" y="{y_of(depth) - 16}" width="52" height="32" rx="9" '
                f'fill="#FAFAFC" stroke="#5B24F9" stroke-width="1.5"/>'
            )
            parts.append(
                f'<text x="{cx}" y="{y_of(depth) + 5}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
                f'font-size="14" fill="#0D0230">{html.escape(str(n))}</text>'
            )
            return
        op, left, right = n

        def subtree_w(m):
            if not isinstance(m, tuple):
                return LEAF_W
            _, l, r = m
            return subtree_w(l) + subtree_w(r) + 20

        lw, rw = subtree_w(left), subtree_w(right)
        left_cx = cx - (rw + 20) / 2
        right_cx = cx + (lw + 20) / 2
        parts.append(f'<circle cx="{cx}" cy="{y_of(depth)}" r="18" fill="#5B24F9"/>')
        parts.append(
            f'<text x="{cx}" y="{y_of(depth) + 5}" text-anchor="middle" font-family="JetBrains Mono, monospace" '
            f'font-weight="700" font-size="15" fill="#fff">{html.escape(op)}</text>'
        )
        render_items(left, depth + 1, left_cx)
        render_items(right, depth + 1, right_cx)

    render_items(node, 0, root_cx)
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def step_reduction_diagram(steps: list[str], *, caption: str = "") -> str:
    """Vertical stack of progressively-reduced expression strings — for
    walking an expression down to its final value one operation at a
    time. steps are plain text (already formatted, e.g. via monospace-
    friendly spacing); each renders as its own row with a down arrow
    between rows."""
    rows = []
    for i, step in enumerate(steps):
        rows.append(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:15px;color:#0D0230;'
            f'text-align:center;padding:8px 0">{html.escape(step)}</div>'
        )
        if i < len(steps) - 1:
            rows.append('<div style="text-align:center;color:#B9A0FC;font-size:18px">↓</div>')
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'{"".join(rows)}{cap}</figure>'
    )


def decision_map(entries: list[tuple[str, str]], *, title: str = "", caption: str = "") -> str:
    """Q -> A decision ladder, e.g. for "which numeric type do I need?".
    entries: list of (question, answer)."""
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:14px;padding:14px 18px;'
        f'background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);'
        f'border-radius:14px;margin-bottom:10px">'
        f'<div style="flex:1;font-size:14px;color:#0D0230">{q}</div>'
        f'<div style="font-size:16px;color:#B9A0FC">→</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:15px;'
        f'color:#5B24F9;white-space:nowrap">{a}</div>'
        f'</div>'
        for q, a in entries
    )
    title_html = f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:16px;margin-bottom:12px;color:#0D0230">{html.escape(title)}</div>' if title else ""
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto">{title_html}{rows}{cap}</figure>'


def capability_map(groups: list[tuple[str, list[str]]], *, title: str = "", caption: str = "") -> str:
    """Responsive HTML/CSS card grid (NOT an SVG diagram) for organizing a
    toolbox (e.g. a stdlib module) or a small set of comparable states into
    clearly labeled cards. Reflows naturally via CSS grid — 3 columns on a
    wide desktop, 2 on tablet, 1 on mobile — instead of cramming many nodes
    into a single SVG row, which is exactly what makes branch_diagram()
    degrade into unreadably tiny text once it has more than 3-4 branches
    or any branch needs more than one line of body content. Use this
    instead whenever that's the case.

    groups: list of (heading, body_lines) where body_lines is a list of
    lines rendered stacked inside the card (e.g. a symbol, a short
    description, and a function name on separate lines) — pass a
    single-item list for a simple one-line card.
    """
    def render_card(heading: str, body_lines: list[str]) -> str:
        lines_html = "".join(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;color:#0D0230;'
            f'line-height:1.7">{line}</div>'
            for line in body_lines
        )
        return (
            f'<div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);'
            f'border-radius:16px;padding:18px 20px">'
            f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:14px;letter-spacing:.02em;'
            f'text-transform:uppercase;color:#5B24F9;margin-bottom:10px">{html.escape(heading)}</div>'
            f'{lines_html}'
            f'</div>'
        )

    cards = "".join(render_card(heading, body_lines) for heading, body_lines in groups)
    title_html = (
        f'<div style="text-align:center;font-family:Sora,sans-serif;font-weight:700;font-size:18px;'
        f'margin-bottom:16px;color:#0D0230">{html.escape(title)}</div>'
        if title
        else ""
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">'
        f'{title_html}'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px">{cards}</div>'
        f'{cap}'
        f'</figure>'
    )


def _render_math_node(node) -> str:
    """Recursively renders one node of the tiny MathML DSL used by
    math_formula()/math_inline(). A node is either a plain string (auto-
    classified as <mn> if it looks like a number, <mi> otherwise — this
    covers both real identifiers like "x" and symbols like "π", which
    MathML also renders as an italic <mi>), or a tuple whose first element
    names the MathML construct:

      ("mo", "+")            -> <mo>+</mo>                (explicit operator/paren)
      ("sup", base, exp)     -> <msup>...</msup>           (x², superscript)
      ("frac", num, den)     -> <mfrac>...</mfrac>         (real stacked fraction)
      ("sqrt", arg)          -> <msqrt>...</msqrt>         (real radical)
      ("row", *items)        -> <mrow>...</mrow>           (adjacent items — e.g. implicit "2x")
    """
    if isinstance(node, str):
        text = node.strip()
        is_number = text.replace(".", "", 1).replace("-", "", 1).isdigit()
        wrapper = "mn" if is_number else "mi"
        return f"<{wrapper}>{html.escape(text)}</{wrapper}>"
    tag, *rest = node
    if tag == "mo":
        return f"<mo>{html.escape(rest[0])}</mo>"
    if tag == "sup":
        base, exp = rest
        return f"<msup>{_render_math_node(base)}{_render_math_node(exp)}</msup>"
    if tag == "frac":
        num, den = rest
        return f"<mfrac>{_render_math_node(num)}{_render_math_node(den)}</mfrac>"
    if tag == "sqrt":
        return f"<msqrt>{_render_math_node(rest[0])}</msqrt>"
    if tag == "row":
        return "<mrow>" + "".join(_render_math_node(n) for n in rest) + "</mrow>"
    raise ValueError(f"Неизвестный узел math DSL: {tag!r}")


def math_inline(node, *, aria_label: str = "") -> str:
    """Real, semantic MathML for one formula — <msup>/<mfrac>/<msqrt>, not
    <sup>/&frasl;/<sub> text hacks. Renders inline (no surrounding figure),
    so it can sit inside a table cell or a sentence. Native MathML gives
    correctly-shaped fractions, superscripts and radicals with zero JS
    runtime cost — no MathJax/KaTeX needed for formulas this simple.
    aria_label is optional spoken-form text (e.g. "икс в квадрате") for
    screen readers; browsers already read MathML structurally without it,
    so most callers can omit it."""
    inner = _render_math_node(node)
    label_attr = f' aria-label="{html.escape(aria_label)}"' if aria_label else ""
    return (
        f'<math xmlns="http://www.w3.org/1998/Math/MathML"{label_attr} '
        f'style="font-size:1.15em;color:#0D0230">{inner}</math>'
    )


def math_formula(node, *, caption: str = "", aria_label: str = "") -> str:
    """Like math_inline(), but as a standalone centered display-block figure
    — for showing one formula on its own, at a size large enough that a
    fraction bar and its numerator/denominator are unmistakably legible."""
    inner = _render_math_node(node)
    label_attr = f' aria-label="{html.escape(aria_label or caption)}"' if (aria_label or caption) else ""
    math_html = (
        f'<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"{label_attr} '
        f'style="font-size:2em;color:#0D0230">{inner}</math>'
    )
    cap = (
        f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>'
        if caption
        else ""
    )
    return (
        f'<figure style="margin:24px 0;padding:28px 20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);display:flex;flex-direction:column;align-items:center;overflow-x:auto">'
        f'{math_html}{cap}</figure>'
    )


def image_figure(src: str, alt: str, caption: str, *, size: str | None = None, width: int | None = None) -> str:
    """A real screenshot/photo, not a generated diagram — captioned figure.

    size controls the figure's max display width via a CSS preset class
    (see .chapter-figure--* in theory.css): "narrow" (~460px, a small
    supporting example), "medium" (~620px), or "wide" (~840px, an
    evidence-grade screenshot that needs to be read without zooming).

    width is the older, pre-preset call style (still used by several
    other chapters) — kept exactly as it behaved before the preset
    system existed, so those chapters' rendered output does not change.
    Pass size for new call sites; width is not consulted when size is
    given."""
    if size is not None:
        assert size in ("narrow", "medium", "wide"), f"unknown figure size: {size!r}"
        return f"""
    <figure class="chapter-figure chapter-figure--{size}">
      <img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy" />
      <figcaption>{html.escape(caption)}</figcaption>
    </figure>"""
    width_attr = f' width="{width}"' if width else ""
    return f"""
    <figure style="margin:24px 0">
      <img src="{html.escape(src)}" alt="{html.escape(alt)}"{width_attr}
        style="width:100%;height:auto;border-radius:var(--radius-lg,20px);border:1px solid var(--color-border-default,#ddd);display:block" />
      <figcaption style="text-align:center;font-size:13px;color:var(--color-text-muted,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>
    </figure>"""


def image_figure_pair(
    src_a: str, alt_a: str, caption_a: str,
    src_b: str, alt_b: str, caption_b: str,
) -> str:
    """Two real screenshots meant to be compared side by side (e.g. a
    before/after state) — equal-size boxes with object-fit:contain, so
    source images of different native proportions still line up cleanly.
    Stacks vertically on narrow/mobile viewports."""

    def _cell(src: str, alt: str, caption: str) -> str:
        return f"""
      <figure class="chapter-figure">
        <div class="chapter-figure-imgbox">
          <img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy" />
        </div>
        <figcaption>{html.escape(caption)}</figcaption>
      </figure>"""

    return f'\n    <div class="chapter-figure-pair">{_cell(src_a, alt_a, caption_a)}{_cell(src_b, alt_b, caption_b)}\n    </div>'


def image_figure_sequence(figures: list[tuple[str, str, str]], *, size: str = "medium") -> str:
    """Several real screenshots meant to be read as an ordered, chronological
    sequence (step 1, step 2, step 3...) — stacked vertically with
    consistent spacing on both desktop and mobile, instead of squeezed
    side by side into a shrinking row."""
    items = "".join(image_figure(src, alt, caption, size=size) for src, alt, caption in figures)
    return f'\n    <div class="chapter-figure-sequence">{items}\n    </div>'


def converge_diagram(sources: list[str], target: str, *, caption: str = "") -> str:
    """Diagram inverse of branch_diagram(): several source boxes on top, each
    with an arrow flowing DOWN into one shared target box at the bottom.
    Used for "several tools/editors, one shared environment" concepts.

    Both source and target labels wrap by word (see _wrap_svg_text) and never
    exceed their box — the target box grows in height for multi-line text,
    and the canvas grows in width if the target is wider than the row of
    source boxes (sources are then re-centered under the wider canvas)."""
    n = len(sources)
    box_w, box_h, gap = 156, 60, 24
    sources_w = n * box_w + (n - 1) * gap

    target_w = 240
    target_max_chars, target_max_lines, target_line_h = 16, 2, 19
    target_lines = _wrap_svg_text(" ".join(target.split()), max_chars=target_max_chars, max_lines=target_max_lines)
    target_h = 60 + (len(target_lines) - 1) * target_line_h

    total_w = max(sources_w, target_w + 40, 260)
    sources_x_offset = (total_w - sources_w) / 2
    target_x = (total_w - target_w) / 2
    sources_y = 10
    target_y = sources_y + box_h + 100
    total_h = target_y + target_h + 10
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="block-diagram" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        "<defs><marker id='arrowc' viewBox='0 0 10 10' refX='9' refY='5' "
        "markerWidth='6' markerHeight='6' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>"
    )
    target_cx = total_w / 2
    source_centres = [sources_x_offset + i * (box_w + gap) + box_w / 2 for i in range(n)]
    bus_y = sources_y + box_h + 50
    for i, label in enumerate(sources):
        x = sources_x_offset + i * (box_w + gap)
        cx = x + box_w / 2
        parts.append(
            f'<rect x="{x}" y="{sources_y}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>'
        )
        label_lines = _wrap_svg_text(label, max_chars=18, max_lines=2)
        label_top = sources_y + box_h / 2 - (len(label_lines) - 1) * 8 + 4
        label_tspans = "".join(
            f'<tspan x="{cx}" y="{label_top + li * 16}">{html.escape(line)}</tspan>' for li, line in enumerate(label_lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" '
            f'font-size="13" fill="#0D0230">{label_tspans}</text>'
        )
        parts.append(
            f'<line x1="{cx}" y1="{sources_y + box_h}" x2="{cx}" y2="{bus_y}" '
            f'stroke="#B9A0FC" stroke-width="2.5"/>'
        )
    if source_centres:
        parts.append(
            f'<line x1="{min(source_centres)}" y1="{bus_y}" x2="{max(source_centres)}" y2="{bus_y}" '
            f'stroke="#B9A0FC" stroke-width="2.5"/>'
        )
        parts.append(
            f'<path d="M{target_cx},{bus_y} V{target_y}" fill="none" stroke="#5B24F9" '
            f'stroke-width="2.5" marker-end="url(#arrowc)"/>'
        )
    parts.append(
        f'<rect x="{target_x}" y="{target_y}" width="{target_w}" height="{target_h}" rx="4" '
        f'fill="#5B24F9" stroke="#3B0FBF" stroke-width="2"/>'
    )
    target_first_line_y = target_y + target_h / 2 - (len(target_lines) - 1) * target_line_h / 2 + 5
    target_tspans = "".join(
        f'<tspan x="{target_cx}" y="{target_first_line_y + li * target_line_h}">{html.escape(line)}</tspan>'
        for li, line in enumerate(target_lines)
    )
    parts.append(
        f'<text text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="700" '
        f'font-size="16" fill="#fff">{target_tspans}</text>'
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">{svg}{cap}</figure>'


def comparison_table(headers: list[str], rows: list[list[str]]) -> str:
    """A real HTML comparison table (not an image) — headers + rows of cell HTML."""
    thead = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    tbody = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    return f"""
    <div style="overflow-x:auto;margin:20px 0">
    <table class="compare-table">
      <thead><tr>{thead}</tr></thead>
      <tbody>{tbody}</tbody>
    </table>
    </div>"""


def summary_box(title: str, items_html: list[str]) -> str:
    items = "".join(f"<li>{item}</li>" for item in items_html)
    return f"""
    <div class="summary-box">
      <h3>{html.escape(title)}</h3>
      <ul>{items}</ul>
    </div>"""


# ---------------------------------------------------------------------------
# Главa 11 — коллекции: индексы/срезы списков, Венн-диаграммы множеств,
# вложенные деревья, поверхностное копирование, матрицы
# ---------------------------------------------------------------------------

def list_box_diagram(items: list[str], *, indices: bool = True, highlight: list[int] | None = None, caption: str = "") -> str:
    """Box-per-element diagram for a list/tuple, each box sized to its own
    content (values can be longer than one character, unlike
    string_index_diagram) — positive index above (purple), negative index
    below (pink). `highlight` marks specific positions (e.g. a just-changed
    or just-inserted cell) with an accent fill. Set indices=False for a
    plain "these are the elements" picture (e.g. a set's unique values)."""
    highlight = set(highlight or [])
    n = len(items)
    box_h = 52
    pad_x = 14
    widths = [max(52, 11 * len(str(it)) + pad_x * 2) for it in items]
    gaps = 6
    total_w = sum(widths) + gaps * max(0, n - 1) + 20
    top_h = 26 if indices else 6
    bot_h = 26 if indices else 6
    total_h = top_h + box_h + bot_h + 10

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    x = 10
    box_y = top_h
    for i, it in enumerate(items):
        w = widths[i]
        cx = x + w / 2
        is_hl = i in highlight
        fill = "#E7DEFF" if is_hl else "#fff"
        stroke = "#5B24F9" if is_hl else "#0D0230"
        sw = "2.5" if is_hl else "1.5"
        parts.append(
            f'<rect x="{x}" y="{box_y}" width="{w}" height="{box_h}" rx="10" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{box_y + box_h / 2 + 6}" text-anchor="middle" '
            f'font-family="\'JetBrains Mono\', monospace" font-weight="700" font-size="15" '
            f'fill="#0D0230">{html.escape(str(it))}</text>'
        )
        if indices:
            parts.append(
                f'<text x="{cx}" y="{top_h - 9}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" '
                f'font-weight="700" font-size="12" fill="#5B24F9">{i}</text>'
            )
            parts.append(
                f'<text x="{cx}" y="{box_y + box_h + 18}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" '
                f'font-weight="700" font-size="12" fill="#DB2777">{i - n}</text>'
            )
        x += w + gaps
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{svg}</div></div>'
        f'{cap}</figure>'
    )


def list_slice_diagram(items: list[str], start: int, stop: int, *, caption: str = "") -> str:
    """Boundary-cut slice diagram for a list — the list_box_diagram sibling
    of string_slice_diagram(): boundary numbers (0..n) live in the GAPS
    between/around variable-width element boxes, the [start:stop) span is
    shaded, and the resulting sub-list is printed below. start/stop must
    already be resolved to non-negative in-range ints by the caller."""
    n = len(items)
    box_h = 52
    pad_x = 14
    widths = [max(52, 11 * len(str(it)) + pad_x * 2) for it in items]
    gaps = 6
    total_w = sum(widths) + gaps * max(0, n - 1) + 20
    total_h = 26 + box_h + 40

    xs = [10]
    for w in widths:
        xs.append(xs[-1] + w + gaps)
    centers = [xs[i] + widths[i] / 2 for i in range(n)]
    boundary_xs = [xs[0]] + [xs[i] + widths[i] + gaps / 2 for i in range(n)]
    boundary_xs[-1] = xs[-1] - gaps + widths[-1] if n else xs[0]
    # boundary j sits at the left edge of box j (or right edge of the last box for j == n)
    boundary_xs = [xs[i] for i in range(n)] + ([xs[n - 1] + widths[n - 1]] if n else [xs[0]])

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    box_y = 26
    for i, it in enumerate(items):
        w = widths[i]
        in_slice = start <= i < stop
        parts.append(
            f'<rect x="{xs[i]}" y="{box_y}" width="{w}" height="{box_h}" rx="10" '
            f'fill="{"#E7DEFF" if in_slice else "#fff"}" stroke="#0D0230" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{centers[i]}" y="{box_y + box_h / 2 + 6}" text-anchor="middle" '
            f'font-family="\'JetBrains Mono\', monospace" font-weight="700" font-size="15" '
            f'fill="#0D0230">{html.escape(str(it))}</text>'
        )
    for j in range(n + 1):
        bx = boundary_xs[j] if j < len(boundary_xs) else xs[-1] + widths[-1]
        on_edge = j in (start, stop)
        parts.append(
            f'<text x="{bx}" y="{box_y - 9}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" '
            f'font-weight="700" font-size="12" fill="{"#5B24F9" if on_edge else "#B9A0FC"}">{j}</text>'
        )
    result = "[" + ", ".join(str(it) for it in items[start:stop]) + "]"
    parts.append(
        f'<text x="{total_w / 2}" y="{box_y + box_h + 28}" text-anchor="middle" '
        f'font-family="\'JetBrains Mono\', monospace" font-size="14" fill="#0D0230">→ '
        f'<tspan font-weight="700">{html.escape(result)}</tspan></text>'
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{svg}</div></div>'
        f'{cap}</figure>'
    )


def venn_diagram(
    label_a: str,
    label_b: str,
    only_a: list[str],
    both: list[str],
    only_b: list[str],
    *,
    mode: str = "venn",
    highlight: str = "none",
    result_label: str = "",
    caption: str = "",
) -> str:
    """Two-circle Venn diagram for set algebra (union/intersection/
    difference/symmetric difference). Rather than clip-path region shading
    (fragile across renderers), the outline stays constant and the
    individual VALUE CHIPS in the highlighted region(s) get an accent fill
    — this points straight at the actual resulting values, which is exactly
    what a learner checking "did I get the right elements?" needs.

    highlight: "union" | "intersection" | "diff_a" | "diff_b" | "symdiff" | "none".
    mode: "venn" (two overlapping circles) or "subset" (small circle inside
    a big one — for A <= B / issubset). In "subset" mode only_a is ignored
    (pass []), `both` holds A's items (drawn inside the inner circle) and
    only_b holds B's extra items (drawn in the outer ring).
    """
    hl_a = highlight in ("union", "diff_a", "symdiff")
    hl_both = highlight in ("union", "intersection")
    hl_b = highlight in ("union", "diff_b", "symdiff")

    def chip(text: str, hl: bool) -> str:
        bg = "#5B24F9" if hl else "#fff"
        fg = "#fff" if hl else "#0D0230"
        bd = "#5B24F9" if hl else "#B9A0FC"
        return (
            f'<div style="display:inline-block;margin:3px;padding:4px 10px;border-radius:999px;'
            f'background:{bg};color:{fg};border:1.5px solid {bd};font-family:\'JetBrains Mono\',monospace;'
            f'font-size:13px;font-weight:700;white-space:nowrap">{html.escape(str(text))}</div>'
        )

    def zone(items: list[str], hl: bool) -> str:
        if not items:
            return '<div style="min-height:24px"></div>'
        return "".join(chip(it, hl) for it in items)

    if mode == "subset":
        svg_w, svg_h = 420, 300
        svg = f"""<svg viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" role="img"
          aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{svg_w}px">
          <ellipse cx="{svg_w/2}" cy="{svg_h/2+6}" rx="190" ry="120" fill="none" stroke="#5B24F9" stroke-width="2"/>
          <ellipse cx="{svg_w/2}" cy="{svg_h/2+40}" rx="95" ry="60" fill="none" stroke="#DB2777" stroke-width="2"/>
          <text x="{svg_w/2}" y="30" text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" font-size="15" fill="#5B24F9">{html.escape(label_b)}</text>
          <text x="{svg_w/2}" y="{svg_h/2-1}" text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" font-size="14" fill="#DB2777">{html.escape(label_a)}</text>
        </svg>"""
        rows = (
            f'<div style="text-align:center;margin-top:-64px;padding:0 20px">{zone(both, hl_both)}</div>'
            f'<div style="text-align:center;margin-top:74px;padding:0 12px">{zone(only_b, hl_b)}</div>'
        )
        body = svg + rows
    else:
        svg_w, svg_h = 460, 230
        svg = f"""<svg viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" role="img"
          aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{svg_w}px">
          <ellipse cx="180" cy="115" rx="145" ry="100" fill="none" stroke="#5B24F9" stroke-width="2"/>
          <ellipse cx="280" cy="115" rx="145" ry="100" fill="none" stroke="#DB2777" stroke-width="2"/>
          <text x="95" y="26" text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" font-size="15" fill="#5B24F9">{html.escape(label_a)}</text>
          <text x="365" y="26" text-anchor="middle" font-family="Sora, sans-serif" font-weight="700" font-size="15" fill="#DB2777">{html.escape(label_b)}</text>
        </svg>"""
        rows = (
            f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:-38px;padding:0 6px;align-items:start">'
            f'<div style="text-align:center">{zone(only_a, hl_a)}</div>'
            f'<div style="text-align:center">{zone(both, hl_both)}</div>'
            f'<div style="text-align:center">{zone(only_b, hl_b)}</div>'
            f'</div>'
        )
        body = svg + rows

    result_html = (
        f'<div style="text-align:center;margin-top:14px;font-family:\'JetBrains Mono\',monospace;'
        f'font-size:14px;color:#0D0230">→ <strong>{html.escape(result_label)}</strong></div>'
        if result_label
        else ""
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        f'<div style="width:100%;max-width:520px">{body}</div>{result_html}{cap}</figure>'
    )


def tree_diagram(node: tuple, *, caption: str = "") -> str:
    """Indented HTML/CSS tree (not SVG, so it reflows naturally on mobile
    instead of demanding fragile auto-layout width math) for nested
    dict/list structures — node = (label, children), children a list of
    such tuples or [] for a leaf. Root dots are purple, branch dots pink,
    leaf dots green."""

    def render_node(n: tuple, depth: int) -> str:
        label, children = n
        leaf = not children
        dot_color = "#5B24F9" if depth == 0 else ("#059669" if leaf else "#DB2777")
        out = (
            f'<div style="display:flex;align-items:center;gap:10px;padding:5px 0">'
            f'<span style="width:9px;height:9px;border-radius:50%;background:{dot_color};flex-shrink:0"></span>'
            f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:14px;color:#0D0230">{html.escape(str(label))}</span>'
            f'</div>'
        )
        if children:
            kids = "".join(render_node(c, depth + 1) for c in children)
            out += f'<div style="margin-left:22px;padding-left:14px;border-left:2px solid #E4E1F5">{kids}</div>'
        return out

    body = render_node(node, 0)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px 24px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">{body}{cap}</figure>'
    )


# ---------------------------------------------------------------------------
# Глава 23 — визуальная система для пошагового проекта SafeSort: дерево
# каталога, индикатор этапа, терминал, карточка состояния проекта, граница
# безопасности "только чтение / меняет файлы".
# ---------------------------------------------------------------------------

def dir_tree(node: tuple, *, highlight: frozenset[str] = frozenset(), faded: frozenset[str] = frozenset(), caption: str = "") -> str:
    """Иллюстрация дерева каталогов: node = (имя, вид, дети), вид — "dir"
    или "file", дети — список таких же кортежей ([] для файла). Использует
    иконки folder/file Cartesian (не Unicode-эмодзи) с теми же соединительными
    линиями, что и tree_diagram(). `highlight` — точные отображаемые имена
    ("scanner.py"), появившиеся именно в этом уроке: подсвечиваются и
    получают метку «НОВОЕ». `faded` — имена, которых ещё нет («появятся
    позже»): показываются полупрозрачными с пунктирной связью."""

    def render_node(n: tuple, depth: int) -> str:
        name, kind, children = n
        icon = cs_icon("folder" if kind == "dir" else "file")
        is_new = name in highlight
        is_faded = name in faded
        row_style = "display:flex;align-items:center;gap:6px;padding:4px 8px;border-radius:8px"
        badge = ""
        if is_new:
            row_style += ";background:#EAF1FF"
            badge = '<span style="margin-left:8px;font-size:11px;font-weight:700;color:var(--blue-600);letter-spacing:.02em">НОВОЕ</span>'
        elif is_faded:
            row_style += ";opacity:.45"
        label = html.escape(name) + ("/" if kind == "dir" else "")
        out = (
            f'<div style="{row_style}">'
            f'{icon}'
            f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:14px;color:#0D0230">{label}</span>'
            f'{badge}'
            f'</div>'
        )
        if children:
            kids = "".join(render_node(c, depth + 1) for c in children)
            border = "border-left:2px dashed #D8D3F0" if is_faded else "border-left:2px solid #E4E1F5"
            out += f'<div style="margin-left:11px;padding-left:17px;{border}">{kids}</div>'
        return out

    body = render_node(node, 0)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px 24px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">{body}{cap}</figure>'
    )


def before_after_trees(before_node: tuple, after_node: tuple, *, label_before: str = "Было", label_after: str = "Стало", caption: str = "") -> str:
    """Two dir_tree()-style panels side by side (stacks vertically on
    mobile) — the "messy folder -> organized folder" picture used on the
    chapter opener and the apply-page before/after."""

    def panel(label: str, node: tuple, accent: str) -> str:
        tree_html = dir_tree(node)
        # dir_tree() already wraps in <figure>; unwrap so we can nest two
        # panels inside one flex row without a doubled card background.
        inner = re.sub(r'^\s*<figure[^>]*>|</figure>\s*$', '', tree_html.strip())
        return (
            f'<div style="flex:1;min-width:220px;background:var(--color-bg-canvas,#fff);'
            f'border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">'
            f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;letter-spacing:.04em;'
            f'text-transform:uppercase;color:{accent};margin-bottom:10px">{html.escape(label)}</div>'
            f'{inner}</div>'
        )

    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">'
        f'<div style="display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start">'
        f'{panel(label_before, before_node, "#6B6B7D")}'
        f'<div style="align-self:center;font-size:22px;color:#B9A0FC;flex:0 0 auto;padding:0 4px">→</div>'
        f'{panel(label_after, after_node, "#059669")}'
        f'</div>{cap}</figure>'
    )


SAFESORT_STAGES: list[str] = [
    "Git и GitHub", "Планирование", "Проект", "Реализация", "Тесты и CI", "Релиз",
]


def stage_tracker(
    current: int, *, stages: list[str] = SAFESORT_STAGES, full: bool = False
) -> str:
    """Persistent "where are we" strip for a multi-stage project (Chapter
    23 / SafeSort): a row of labels with the current one highlighted, plus
    an "Этап N из M" line above it. `current` is 1-based. Small and
    reusable at the top of every main SafeSort page — never a heavy visual,
    just a constant orientation cue."""
    n = len(stages)
    current = max(1, min(current, n))
    if not full:
        return (
            '<div class="stage-tracker-compact" aria-label="Положение в проекте SafeSort">'
            f'<span>SafeSort · Часть {current} из {n}</span>'
            f'<strong>{html.escape(stages[current - 1])}</strong>'
            '</div>'
        )
    items = "".join(
        (
            f'<span style="display:flex;align-items:center;gap:6px">'
            f'<span style="font-family:Sora,sans-serif;font-weight:{700 if i + 1 == current else 500};'
            f'font-size:13px;padding:4px 10px;border-radius:999px;white-space:nowrap;'
            f'background:{"linear-gradient(90deg,var(--violet-500),var(--blue-500))" if i + 1 == current else "transparent"};'
            f'color:{"#fff" if i + 1 == current else "var(--gray-600)"}">{html.escape(label)}</span>'
            f'</span>'
            + (f'<span style="color:#D8D3F0;font-size:12px">→</span>' if i < n - 1 else "")
        )
        for i, label in enumerate(stages)
    )
    return (
        f'<div style="margin:0 0 24px;padding:12px 16px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:14px;border:1px solid var(--color-border-default,#E4E1F5)">'
        f'<div style="font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;'
        f'color:#5B24F9;margin-bottom:8px">SafeSort · Часть {current} из {n}</div>'
        f'<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">{items}</div>'
        f'</div>'
    )


def terminal_capture(lines: list[str], *, cwd: str = "~/safesort", caption: str = "") -> str:
    """A real captured terminal session, styled as an actual terminal window
    (traffic-light dots + monospace pane) — visually distinct from
    code_block()'s source-file tab, so it reads unmistakably as "this really
    ran", not as a source listing. `lines` is the literal sequence to
    display: prefix a line with "$ " for a typed command (bold, bright);
    anything else is program output (dimmed). Every line here must be
    genuine captured output — never invented."""
    rendered = []
    for line in lines:
        if line.startswith("$ "):
            rendered.append(
                f'<div><span style="color:#8FB7FE">{html.escape(cwd)} $</span> '
                f'<span style="color:#fff">{html.escape(line[2:])}</span></div>'
            )
        elif line == "":
            rendered.append('<div>&nbsp;</div>')
        else:
            rendered.append(f'<div style="color:#B4B4C4">{html.escape(line)}</div>')
    body = "".join(rendered)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return f"""
    <figure style="margin:24px 0">
    <div style="background:var(--navy-950,#08011C);border-radius:var(--radius-md,14px);overflow:hidden;box-shadow:var(--shadow-sm)">
      <div style="display:flex;gap:6px;padding:10px 14px;background:rgba(255,255,255,0.04);border-bottom:1px solid rgba(255,255,255,0.08)">
        <span style="width:10px;height:10px;border-radius:50%;background:#EF4444"></span>
        <span style="width:10px;height:10px;border-radius:50%;background:#F5B93D"></span>
        <span style="width:10px;height:10px;border-radius:50%;background:#22C55E"></span>
      </div>
      <div style="padding:16px;font-family:'JetBrains Mono',monospace;font-size:13.5px;line-height:1.75;overflow-x:auto">{body}</div>
    </div>{cap}
    </figure>"""


def project_state_card(done: list[str], now: str, upcoming: list[str]) -> str:
    """"Что уже есть" checklist: done items with a check, the current
    lesson's item bolded/highlighted, future items dimmed with an empty
    circle. Gives continuity without repeating the full stage_tracker."""
    rows = "".join(
        f'<div style="display:flex;align-items:center;gap:10px;padding:3px 0;color:#059669">'
        f'<span style="flex-shrink:0">{cs_icon("success")}</span>'
        f'<span style="font-size:14px">{html.escape(item)}</span></div>'
        for item in done
    )
    rows += (
        f'<div style="display:flex;align-items:center;gap:10px;padding:3px 0">'
        f'<span style="width:9px;height:9px;border-radius:50%;background:#5B24F9;flex-shrink:0;margin:0 3.5px"></span>'
        f'<span style="font-size:14px;font-weight:700;color:#0D0230">{html.escape(now)}</span></div>'
    )
    rows += "".join(
        f'<div style="display:flex;align-items:center;gap:10px;padding:3px 0;opacity:.5">'
        f'<span style="width:9px;height:9px;border-radius:50%;border:1.5px solid #B4B4C4;flex-shrink:0;margin:0 3.5px"></span>'
        f'<span style="font-size:14px;color:#6B6B7D">{html.escape(item)}</span></div>'
        for item in upcoming
    )
    return (
        f'<div style="margin:24px 0;padding:18px 20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px)">'
        f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;letter-spacing:.04em;'
        f'text-transform:uppercase;color:#6B6B7D;margin-bottom:10px">Что уже есть</div>{rows}</div>'
    )


def github_issue_card(number: int, title: str, *, area: str, priority: str, branch: str | None = None) -> str:
    """Compact "real work item" opener for a SafeSort feature cluster in
    Part IV: ties the following pages to a genuine Issue in the real
    GitHub Project (github.com/orgs/Cartesian-School/projects/1 —
    "SafeSort — первый релиз"), not a hypothetical example. Area/Priority
    are that Issue's real field values in the live Project, not invented
    for the lesson. One card per feature cluster (not per page) — see
    github_issue_checkpoint() for the matching closer."""
    branch_row = (
        f'<div style="margin-top:8px;font-family:\'JetBrains Mono\',monospace;font-size:13px;color:#0D0230">'
        f"git switch -c {html.escape(branch)}</div>"
        if branch
        else ""
    )
    return (
        f'<div style="margin:24px 0;padding:16px 20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-left:3px solid #5B24F9;border-radius:0 12px 12px 0">'
        f'<div style="display:flex;align-items:center;gap:6px;font-family:Sora,sans-serif;font-weight:700;'
        f'font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin-bottom:6px">'
        f'{github_mark(15)}<span>Issue #{number} · Project «SafeSort — первый релиз»</span></div>'
        f'<div style="font-size:15px;font-weight:700;color:#0D0230;margin-bottom:8px">{html.escape(title)}</div>'
        f'<div style="display:flex;gap:18px;font-size:13px;color:#6B6B7D">'
        f'<span>Area: <strong style="color:#0D0230">{html.escape(area)}</strong></span>'
        f'<span>Priority: <strong style="color:#0D0230">{html.escape(priority)}</strong></span>'
        f"</div>{branch_row}</div>"
    )


def github_issue_checkpoint(issues: list[int], *, commit_subject: str, history: str, project_outcome: str = "Done") -> str:
    """Compact "checkpoint" closer for a SafeSort feature cluster, pairing
    with github_issue_card() at the cluster's start. `history` is the real
    closing story for these Issues, in whatever shape it actually took —
    a single PR, one PR closing several related Issues, or (for #10/#11,
    genuinely) a manual close with no PR "Closes" keyword because the work
    landed inside another Issue's commit. Never invent a uniform
    one-Issue-one-PR pattern the real repository doesn't have."""
    issue_list = ", ".join(f"#{n}" for n in issues)
    return (
        f'<div style="margin:24px 0;padding:16px 20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-left:3px solid #059669;border-radius:0 12px 12px 0">'
        f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:11px;letter-spacing:.04em;'
        f'text-transform:uppercase;color:#059669;margin-bottom:6px">Чекпойнт · Issue {issue_list}</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:13px;color:#0D0230;margin-bottom:8px">'
        f'git commit -m "{html.escape(commit_subject)}"</div>'
        f'<div style="font-size:13.5px;color:#3A3A4A;line-height:1.5;margin-bottom:6px">{history}</div>'
        f'<div style="font-size:13px;color:#6B6B7D">Статус в реальном Project: '
        f'<strong style="color:#059669">{html.escape(project_outcome)}</strong></div>'
        f"</div>"
    )


def safety_boundary(read_only: list[str], modifying: list[str]) -> str:
    """The read-only-vs-modifying-commands picture (scan/plan/duplicates
    never touch disk; apply/undo do) — two visually distinct cards so the
    boundary reads as a hard line, not a sentence buried in prose."""

    def card(title: str, items: list[str], color: str, bg: str) -> str:
        rows = "".join(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;color:#0D0230;'
            f'padding:3px 0">{html.escape(item)}</div>'
            for item in items
        )
        return (
            f'<div style="flex:1;min-width:200px;background:{bg};border:1.5px solid {color};'
            f'border-radius:16px;padding:16px 20px">'
            f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;letter-spacing:.03em;'
            f'text-transform:uppercase;color:{color};margin-bottom:10px">{html.escape(title)}</div>{rows}</div>'
        )

    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">'
        f'<div style="display:flex;gap:16px;flex-wrap:wrap">'
        f'{card("Только читают", read_only, "#059669", "#ECFDF5")}'
        f'{card("Меняют файлы", modifying, "#DC2626", "#FEF2F2")}'
        f'</div></figure>'
    )


def github_mark(size: int = 24, *, on_dark: bool = False) -> str:
    """Official GitHub Invertocat mark, downloaded from brand.github.com
    (GitHub_Logos.zip) and stored verbatim at
    site/assets/brand/github/invertocat-{black,white}.svg — real brand
    asset, not a hand-approximated recreation. Per GitHub's own usage
    guidance the mark must stay one of the permitted flat colors (black
    on light backgrounds, white on dark — never recolored via
    currentColor or a gradient), so `on_dark` picks the correct file
    instead of tinting a single asset. Native aspect ratio is 98:96;
    height is derived from `size` (the width) to avoid distortion."""
    variant = "white" if on_dark else "black"
    height = round(size * 96 / 98)
    return (
        f'<img src="/assets/brand/github/invertocat-{variant}.svg" alt="GitHub" '
        f'width="{size}" height="{height}" '
        f'style="display:inline-block;vertical-align:-0.15em" />'
    )


def official_sources(entries: list[tuple[str, str]], *, adapted: bool = True) -> str:
    """Small "Официальная документация" box: (title, url) pairs the page's
    content is adapted from. Not visually dominant — a compact list, not a
    callout. When `adapted` is True (the default — this is Chapter 23's
    normal case), appends a one-line CC BY 4.0 attribution notice per
    docs/CHAPTER-23-GITHUB-SOURCES.md's policy: GitHub Docs content is
    reused in translated/adapted form, not simply linked."""
    rows = "".join(
        f'<div style="margin:3px 0"><a href="{html.escape(url)}" style="color:#185DFA">{html.escape(title)}</a></div>'
        for title, url in entries
    )
    note = (
        '<div style="margin-top:8px;font-size:12px;color:#6B6B7D">'
        "Перевод и учебная адаптация официальной документации GitHub. "
        "Исходный материал — CC BY 4.0.</div>"
        if adapted
        else ""
    )
    return (
        f'<div style="margin:20px 0;padding:14px 18px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:12px;font-size:13.5px">'
        f'<div style="font-weight:700;color:#6B6B7D;font-size:11px;letter-spacing:.04em;'
        f'text-transform:uppercase;margin-bottom:6px">Официальная документация</div>'
        f'{rows}{note}</div>'
    )


def github_lockup(width: int = 140, *, on_dark: bool = False) -> str:
    """Official GitHub logo lockup (Invertocat + wordmark), same source
    and provenance as github_mark(). Reserved for places that function as
    a real link/identification to github.com (per GitHub's brand usage
    guidance) — the chapter opener and "what is GitHub" introduction —
    not as page decoration; use the smaller github_mark() elsewhere.
    Native aspect ratio is 416:95."""
    variant = "white" if on_dark else "black"
    height = round(width * 95 / 416)
    return (
        f'<img src="/assets/brand/github/lockup-{variant}.svg" alt="GitHub" '
        f'width="{width}" height="{height}" style="display:block" />'
    )


def git_mark(size: int = 24, *, on_dark: bool = False, aria_label: str | None = None) -> str:
    """Official Git icon mark (the tilted diamond), downloaded verbatim
    from git-scm.com/downloads/logos — Jason Long's Git logo, CC BY 3.0 —
    and stored as mark-orange.svg for light surfaces and mark-white.svg for
    dark surfaces. Kept in a
    brand directory of its own, separate from
    site/assets/icons/cartesian/icons.svg, so Git's real mark is never
    confused with a Cartesian School semantic icon. Native aspect ratio is
    78:78 (square).

    Decorative by default (empty alt + aria-hidden), matching Git's own
    brand guidance for a mark placed next to the visible word "Git" — the
    text already carries the meaning, so a screen reader would otherwise
    announce "Git" twice. Pass `aria_label` (e.g. "Git — официальный
    сайт") only for the rare case of the mark used alone as a link, with
    no adjacent visible "Git" text."""
    variant = "white" if on_dark else "orange"
    if aria_label:
        alt_attrs = f'alt="" role="img" aria-label="{html.escape(aria_label)}"'
    else:
        alt_attrs = 'alt="" aria-hidden="true"'
    return (
        f'<img src="/assets/brand/git/mark-{variant}.svg" {alt_attrs} '
        f'width="{size}" height="{size}" '
        f'style="display:inline-block;vertical-align:-0.15em" />'
    )


def git_lockup(width: int = 90, *, on_dark: bool = False, aria_label: str | None = None) -> str:
    """Official Git logo lockup (mark + "git" wordmark), same source and
    provenance as git_mark(). Reserved for places that establish Git as a
    distinct technology in its own right — the Git-vs-GitHub comparison
    and the installation-lesson opener — not repeated next to every
    mention of the word "Git"; use the smaller git_mark() there instead,
    or no mark at all. Native aspect ratio is 219:92.

    Decorative by default, same reasoning as git_mark(); pass
    `aria_label` only when the lockup stands alone as a link."""
    variant = "white" if on_dark else "color"
    height = round(width * 92 / 219)
    if aria_label:
        alt_attrs = f'alt="" role="img" aria-label="{html.escape(aria_label)}"'
    else:
        alt_attrs = 'alt="" aria-hidden="true"'
    return (
        f'<img src="/assets/brand/git/lockup-{variant}.svg" {alt_attrs} '
        f'width="{width}" height="{height}" style="display:block" />'
    )


def shallow_copy_diagram(outer_a_label: str, outer_b_label: str, inner_items: list[str], *, caption: str = "") -> str:
    """Two independent OUTER lists (e.g. `original` and `original.copy()`),
    drawn as two stacked rows of slot boxes, both fanning arrows down into
    ONE SHARED row of inner-object boxes below — the correct picture for a
    shallow copy: a new outer container, but the same referenced inner
    objects."""
    n = len(inner_items)
    slot_w, slot_h, gap = 100, 44, 18
    label_col = 130
    row_w = n * slot_w + max(0, n - 1) * gap
    total_w = label_col + row_w + 20
    outer_a_y, outer_b_y = 10, 84
    inner_y = 210
    total_h = inner_y + slot_h + 10

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="reference-diagram" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
        "<defs><marker id='arrowsc' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>"
    ]

    def label_text(text: str, y: float, color: str) -> None:
        parts.append(
            f'<text x="0" y="{y + slot_h / 2 + 5}" font-family="Sora, sans-serif" font-weight="700" '
            f'font-size="13" fill="{color}">{html.escape(text)}</text>'
        )

    label_text(outer_a_label, outer_a_y, "#5B24F9")
    label_text(outer_b_label, outer_b_y, "#DB2777")

    for i in range(n):
        x = label_col + i * (slot_w + gap)
        cx = x + slot_w / 2
        for y, color in ((outer_a_y, "#5B24F9"), (outer_b_y, "#DB2777")):
            parts.append(
                f'<rect x="{x}" y="{y}" width="{slot_w}" height="{slot_h}" rx="4" '
                f'fill="{"#EDE9FE" if color == "#5B24F9" else "#FCE7F3"}" '
                f'stroke="{color}" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{cx}" y="{y + slot_h / 2 + 5}" text-anchor="middle" '
                f'font-family="\'JetBrains Mono\', monospace" font-size="12" fill="#0D0230">[{i}]</text>'
            )
        parts.append(
            f'<rect x="{x}" y="{inner_y}" width="{slot_w}" height="{slot_h}" rx="4" '
            f'fill="#DCFCE7" stroke="#059669" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{inner_y + slot_h / 2 + 5}" text-anchor="middle" '
            f'font-family="\'JetBrains Mono\', monospace" font-weight="700" font-size="13" '
            f'fill="#0D0230">{html.escape(str(inner_items[i]))}</text>'
        )
        parts.append(
            f'<path d="M{cx - 8},{outer_a_y + slot_h} V{(outer_a_y + slot_h + inner_y) / 2} '
            f'H{cx - 4} V{inner_y}" '
            f'fill="none" stroke="#5B24F9" stroke-width="2" marker-end="url(#arrowsc)"/>'
        )
        parts.append(
            f'<path d="M{cx + 8},{outer_b_y + slot_h} V{(outer_b_y + slot_h + inner_y) / 2} '
            f'H{cx + 4} V{inner_y}" '
            f'fill="none" stroke="#DB2777" stroke-width="2" marker-end="url(#arrowsc)"/>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{svg}</div></div>'
        f'{cap}</figure>'
    )


def matrix_diagram(
    rows: list[list[str]],
    *,
    row_labels: list[str] | None = None,
    col_labels: list[str] | None = None,
    highlight: tuple[int, int] | None = None,
    caption: str = "",
) -> str:
    """Real-value grid for a nested list (matrix/board) — an HTML/CSS grid
    (not SVG) so arbitrary-width cell content reflows safely. Distinct from
    nested_loop_grid(), which draws an ABSTRACT rows×cols shape; this one
    shows the actual values, with optional row/col index headers and a
    single highlighted (row, col) cell."""
    ncols = max((len(r) for r in rows), default=0)
    has_col_labels = col_labels is not None
    has_row_labels = row_labels is not None
    n_grid_cols = ncols + (1 if has_row_labels else 0)

    def cell(text: str, *, header: bool = False, hl: bool = False) -> str:
        bg = "#5B24F9" if hl else ("#F1EEFC" if header else "#fff")
        fg = "#fff" if hl else ("#5B24F9" if header else "#0D0230")
        return (
            f'<div style="min-width:44px;padding:10px 12px;border-radius:8px;background:{bg};color:{fg};'
            f'text-align:center;font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:14px;'
            f'border:1.5px solid {"#5B24F9" if hl else "#E4E1F5"}">{html.escape(str(text))}</div>'
        )

    grid_rows = []
    if has_col_labels:
        header_row = [cell("", header=True)] if has_row_labels else []
        header_row += [cell(c, header=True) for c in col_labels]
        grid_rows.append(header_row)
    for ri, r in enumerate(rows):
        row_html = [cell(row_labels[ri], header=True)] if has_row_labels else []
        row_html += [cell(v, hl=(highlight == (ri, ci))) for ci, v in enumerate(r)]
        grid_rows.append(row_html)

    grid_html = "".join(
        "".join(c for c in row) for row in grid_rows
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:inline-grid;grid-template-columns:repeat({n_grid_cols},auto);gap:6px;'
        f'margin:0 auto">{grid_html}</div>{cap}</figure>'
    )


# ---------------------------------------------------------------------------
# Главa 13 — функции: вызов/возврат, стек вызовов
# ---------------------------------------------------------------------------

def call_flow_diagram(
    before_steps: list[str],
    call_label: str,
    function_steps: list[str],
    after_steps: list[str],
    *,
    function_name: str = "",
    caption: str = "",
) -> str:
    """The signature Chapter 13 visual: two columns — the CALLER's statements
    top-to-bottom on the left (with the call itself highlighted), the
    FUNCTION's body statements on the right — connected by two orthogonal
    arrows: one from the call site INTO the function (green, "вызов"), one
    from the end of the function body back to the statement right after the
    call (pink, "возврат"). Makes concrete that a call does not just "run
    somewhere" — control jumps in, then jumps back to continue exactly
    where it left off."""
    box_w, box_h, gap_y = 230, 52, 16
    col_gap = 150
    left_x = 10
    right_x = left_x + box_w + col_gap
    total_w = right_x + box_w + 20

    left_steps = list(before_steps) + [call_label] + list(after_steps)
    call_idx = len(before_steps)

    left_ys: list[float] = []
    y = 30
    for _ in left_steps:
        left_ys.append(y)
        y += box_h + gap_y
    left_bottom = y - gap_y

    call_y = left_ys[call_idx]
    right_ys: list[float] = []
    y2 = call_y
    for _ in function_steps:
        right_ys.append(y2)
        y2 += box_h + gap_y
    right_bottom = y2 - gap_y

    total_h = max(left_bottom, right_bottom) + 30

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="control-flow" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
        "<defs>"
        "<marker id='arrowcfg' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#059669'/></marker>"
        "<marker id='arrowcfp' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#DB2777'/></marker>"
        "<marker id='arrowcfv' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker>"
        "</defs>"
    ]
    parts.append(
        f'<text x="{left_x}" y="18" font-family="Sora, sans-serif" font-weight="700" font-size="12" '
        f'letter-spacing="0.04em" fill="#6B6B7D">ОСНОВНАЯ ПРОГРАММА</text>'
    )
    parts.append(
        f'<text x="{right_x}" y="18" font-family="Sora, sans-serif" font-weight="700" font-size="12" '
        f'letter-spacing="0.04em" fill="#6B6B7D">ФУНКЦИЯ {html.escape(function_name)}</text>'
    )
    left_cx = left_x + box_w / 2
    for i, (label, ly) in enumerate(zip(left_steps, left_ys)):
        is_call = i == call_idx
        fill = "#5B24F9" if is_call else "#EDE9FE"
        fg = "#fff" if is_call else "#0D0230"
        stroke = "#5B24F9"
        parts.append(
            f'<rect x="{left_x}" y="{ly}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=24, max_lines=2)
        first_y = ly + box_h / 2 - (len(lines) - 1) * 9 + 5
        tspans = "".join(
            f'<tspan x="{left_cx}" y="{first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-weight="700" '
            f'font-size="13" fill="{fg}">{tspans}</text>'
        )
        if i > 0:
            prev_bottom = left_ys[i - 1] + box_h
            parts.append(
                f'<line x1="{left_cx}" y1="{prev_bottom}" x2="{left_cx}" y2="{ly}" '
                f'stroke="#B9A0FC" stroke-width="2" marker-end="url(#arrowcfv)"/>'
            )
    right_cx = right_x + box_w / 2
    for i, (label, ry) in enumerate(zip(function_steps, right_ys)):
        parts.append(
            f'<rect x="{right_x}" y="{ry}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="#DCFCE7" stroke="#059669" stroke-width="2"/>'
        )
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=24, max_lines=2)
        first_y = ry + box_h / 2 - (len(lines) - 1) * 9 + 5
        tspans = "".join(
            f'<tspan x="{right_cx}" y="{first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-weight="700" '
            f'font-size="13" fill="#0D0230">{tspans}</text>'
        )
        if i > 0:
            prev_bottom = right_ys[i - 1] + box_h
            parts.append(
                f'<line x1="{right_cx}" y1="{prev_bottom}" x2="{right_cx}" y2="{ry}" '
                f'stroke="#059669" stroke-width="2" marker-end="url(#arrowcfg)"/>'
            )
    call_right = (left_x + box_w, call_y + box_h / 2)
    func_top = (right_x, right_ys[0] + box_h / 2) if right_ys else (right_x, call_y + box_h / 2)
    call_mid_x = (call_right[0] + func_top[0]) / 2
    parts.append(
        f'<path d="M{call_right[0]},{call_right[1]} H{call_mid_x} V{func_top[1]} H{func_top[0]}" '
        f'fill="none" stroke="#059669" stroke-width="2.5" stroke-linejoin="miter" '
        f'marker-end="url(#arrowcfg)"/>'
    )
    parts.append(
        f'<text x="{(call_right[0] + func_top[0]) / 2}" y="{min(call_right[1], func_top[1]) - 10}" '
        f'text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="700" font-size="12" '
        f'fill="#059669">вызов</text>'
    )
    if right_ys and after_steps:
        func_bottom = (right_x, right_ys[-1] + box_h)
        after_left = (left_x, left_ys[call_idx + 1] + box_h / 2)
        parts.append(
            f'<path d="M{func_bottom[0]},{func_bottom[1]} H{(func_bottom[0] + after_left[0]) / 2} '
            f'V{after_left[1]} H{after_left[0]}" fill="none" stroke="#DB2777" '
            f'stroke-width="2.5" stroke-linejoin="miter" marker-end="url(#arrowcfp)"/>'
        )
        parts.append(
            f'<text x="{(func_bottom[0] + after_left[0]) / 2}" y="{max(func_bottom[1], after_left[1]) + 18}" '
            f'text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="700" font-size="12" '
            f'fill="#DB2777">возврат</text>'
        )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{svg}</div></div>'
        f'{cap}</figure>'
    )


def call_stack_diagram(frames: list[str], *, caption: str = "") -> str:
    """A snapshot of the call stack — frames stacked bottom (oldest, e.g.
    "main") to top (the currently executing call), topmost frame
    highlighted and labeled. Call this once per stage (before/during/after
    a nested call) to show the stack growing and shrinking, the same way
    Chapter 10 staged its mandala construction."""
    box_w, box_h = 210, 50
    total_w = box_w + 150
    n = len(frames)
    top_pad = 30
    total_h = top_pad + n * box_h + 20

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="stack-diagram" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    cx = 20 + box_w / 2
    for i, frame in enumerate(reversed(frames)):
        y = top_pad + i * box_h
        is_top = i == 0
        fill = "#5B24F9" if is_top else "#EDE9FE"
        fg = "#fff" if is_top else "#0D0230"
        parts.append(
            f'<rect x="20" y="{y}" width="{box_w}" height="{box_h}" rx="4" '
            f'fill="{fill}" stroke="#5B24F9" stroke-width="2"/>'
        )
        lines = _wrap_svg_text(" ".join(frame.split()), max_chars=22, max_lines=2)
        first_y = y + box_h / 2 - (len(lines) - 1) * 9 + 5
        tspans = "".join(
            f'<tspan x="{cx}" y="{first_y + li * 18}">{html.escape(line)}</tspan>' for li, line in enumerate(lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-weight="700" '
            f'font-size="13" fill="{fg}">{tspans}</text>'
        )
        if is_top:
            parts.append(
                f'<text x="{20 + box_w + 14}" y="{y + box_h / 2 + 5}" font-family="Sora, sans-serif" '
                f'font-weight="700" font-size="12" fill="#5B24F9">← верх стека</text>'
            )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{svg}</div></div>'
        f'{cap}</figure>'
    )


_UML_BOX_W = 260
_UML_PAD_X = 16
_UML_ROW_MAX_CHARS = 22  # safe for 13.5px 'JetBrains Mono' within box_w - 2*pad_x
_UML_LINE_H = 18
_UML_ROW_GAP = 10  # vertical gap between two different attribute/method rows


def _uml_wrapped_rows(labels: list[str]) -> list[list[str]]:
    """Wraps each label to _UML_ROW_MAX_CHARS, returning one list of lines
    per label — used by class_diagram()/object_diagram() so a long
    attribute/method/value never crosses the box's right edge."""
    return [_wrap_svg_text(" ".join(label.split()), max_chars=_UML_ROW_MAX_CHARS, max_lines=4) for label in labels]


def class_diagram(
    name: str,
    attributes: list[str],
    methods: list[str],
    *,
    caption: str = "",
) -> str:
    """Simplified UML-style class box: class NAME in a purple header band,
    then an "атрибуты" section listing instance-attribute names, then a
    "методы" section listing method signatures (already including the
    trailing "()", e.g. "take_damage(amount)"). This is the TYPE-level
    diagram — it describes every future instance, never a specific one's
    values. Use object_diagram() for a specific instance's actual state.

    Each attribute/method wraps safely instead of crossing the box edge —
    a row with long text simply grows taller (more lines), and the whole
    box grows with it; box width never changes."""
    box_w = _UML_BOX_W
    header_h = 40
    section_gap = 10
    pad_x = _UML_PAD_X
    attrs_wrapped = _uml_wrapped_rows(attributes or ["—"])
    meths_wrapped = _uml_wrapped_rows(methods or ["—"])

    def section_h(wrapped_rows: list[list[str]]) -> float:
        return sum(len(lines) * _UML_LINE_H + _UML_ROW_GAP for lines in wrapped_rows) + 4

    attrs_h = section_h(attrs_wrapped)
    meths_h = section_h(meths_wrapped)
    total_h = header_h + attrs_h + meths_h + 6
    total_w = box_w + 20

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="uml-class" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    x = 10
    parts.append(
        f'<rect x="{x}" y="0" width="{box_w}" height="{total_h}" rx="2" '
        f'fill="#EDE9FE" stroke="#5B24F9" stroke-width="2"/>'
    )
    parts.append(
        f'<rect x="{x}" y="0" width="{box_w}" height="{header_h}" rx="0" fill="#5B24F9"/>'
    )
    parts.append(
        f'<text x="{x + box_w / 2}" y="{header_h / 2 + 6}" text-anchor="middle" '
        f'font-family="\'JetBrains Mono\', monospace" font-weight="700" font-size="16" fill="#fff">'
        f'{html.escape(name)}</text>'
    )
    y = header_h
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x + box_w}" y2="{y}" stroke="#5B24F9" stroke-width="1.5"/>')
    ay = y + section_gap + 12
    for lines in attrs_wrapped:
        tspans = "".join(
            f'<tspan x="{x + pad_x}" y="{ay + li * _UML_LINE_H}">{html.escape(line)}</tspan>' for li, line in enumerate(lines)
        )
        parts.append(
            f'<text font-family="\'JetBrains Mono\', monospace" font-size="13.5" fill="#0D0230">{tspans}</text>'
        )
        ay += len(lines) * _UML_LINE_H + _UML_ROW_GAP
    y = header_h + attrs_h
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x + box_w}" y2="{y}" stroke="#5B24F9" stroke-width="1.5"/>')
    my = y + section_gap + 12
    for lines in meths_wrapped:
        tspans = "".join(
            f'<tspan x="{x + pad_x}" y="{my + li * _UML_LINE_H}">{html.escape(line)}</tspan>' for li, line in enumerate(lines)
        )
        parts.append(
            f'<text font-family="\'JetBrains Mono\', monospace" font-size="13.5" fill="#5B24F9" '
            f'font-weight="600">{tspans}</text>'
        )
        my += len(lines) * _UML_LINE_H + _UML_ROW_GAP
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{svg}</div></div>'
        f'{cap}</figure>'
    )


def object_diagram(
    instance_label: str,
    class_name: str,
    values: list[tuple[str, str]],
    *,
    width: int | None = None,
    caption: str = "",
) -> str:
    """Simplified object (instance) box, deliberately styled close to
    class_diagram() but in pink instead of purple, and header reads
    "instance_label : ClassName" — the classic UML instance notation. Body
    rows show name = value_repr, i.e. actual current state, never types or
    method signatures. Two objects of the same class drawn side by side
    with different values makes "same class, own state" visible at a
    glance; that is the primary use of this diagram.

    Each "field = value" row wraps safely instead of crossing the box edge
    — the field name stays on the first line in muted color, the value
    (which is usually the longer, more variable part) wraps onto as many
    dark-colored lines as it needs; the box grows taller to fit.

    `width` overrides the default box width (in px) for diagrams whose
    values are naturally long (e.g. a 9-element list literal) — the
    per-line character budget scales with it, so a wider box actually
    lets more text fit on one line instead of just adding empty margin."""
    box_w = width if width else _UML_BOX_W
    row_max_chars = max(_UML_ROW_MAX_CHARS, round(_UML_ROW_MAX_CHARS * box_w / _UML_BOX_W))
    header_h = 40
    pad_x = _UML_PAD_X
    rows = values or [("—", "—")]

    # First line is "field = " (muted) + as much of value (dark) as fits;
    # remaining value text continues on its own dark line(s) below, never
    # repeating the field prefix.
    row_lines: list[tuple[str, str, list[str]]] = []
    for field, val in rows:
        prefix = f"{field} = "
        first_budget = max(row_max_chars - len(prefix), 6)
        val_words = val.split()
        first_line = ""
        rest = val
        if val_words:
            wrapped_val = _wrap_svg_text(" ".join(val_words), max_chars=first_budget, max_lines=1)
            first_line = wrapped_val[0] if wrapped_val else ""
            rest = val[len(first_line):].strip()
        remaining_lines = _wrap_svg_text(rest, max_chars=row_max_chars, max_lines=3) if rest else []
        row_lines.append((prefix, first_line, remaining_lines))

    def row_h(entry: tuple[str, str, list[str]]) -> float:
        _, _, remaining = entry
        return (1 + len(remaining)) * _UML_LINE_H + _UML_ROW_GAP

    body_h = sum(row_h(r) for r in row_lines) + 10
    total_h = header_h + body_h
    total_w = box_w + 20

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="uml-object" aria-label="{html.escape(caption)}" '
        f'style="display:block;width:100%;height:auto">'
    ]
    x = 10
    parts.append(
        f'<rect x="{x}" y="0" width="{box_w}" height="{total_h}" rx="2" '
        f'fill="#FCE7F3" stroke="#DB2777" stroke-width="2"/>'
    )
    parts.append(
        f'<rect x="{x}" y="0" width="{box_w}" height="{header_h}" rx="0" fill="#DB2777"/>'
    )
    header_text = f"{instance_label} : {class_name}"
    parts.append(
        f'<text x="{x + box_w / 2}" y="{header_h / 2 + 6}" text-anchor="middle" '
        f'font-family="\'JetBrains Mono\', monospace" font-weight="700" font-size="14.5" fill="#fff" '
        f'text-decoration="underline">{html.escape(header_text)}</text>'
    )
    y = header_h
    parts.append(f'<line x1="{x}" y1="{y}" x2="{x + box_w}" y2="{y}" stroke="#DB2777" stroke-width="1.5"/>')
    ry = y + 20 + 12
    for prefix, first_value_line, remaining in row_lines:
        parts.append(
            f'<text x="{x + pad_x}" y="{ry}" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="13.5" fill="#0D0230">'
            f'<tspan fill="#6B6B7D">{html.escape(prefix)}</tspan>{html.escape(first_value_line)}</text>'
        )
        line_y = ry
        for cont_line in remaining:
            line_y += _UML_LINE_H
            parts.append(
                f'<text x="{x + pad_x}" y="{line_y}" font-family="\'JetBrains Mono\', monospace" '
                f'font-size="13.5" fill="#0D0230">{html.escape(cont_line)}</text>'
            )
        ry += (1 + len(remaining)) * _UML_LINE_H + _UML_ROW_GAP
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    # width:min(100%, Npx) gives the wrapper a DEFINITE width for the SVG's
    # width:100% to resolve against — a shrink-to-fit inline-block parent has
    # no such definite width, so the SVG collapsed toward its own intrinsic
    # size instead of actually rendering at up to total_w CSS pixels.
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="width:min(100%, {total_w}px);margin:0 auto">{svg}</div>'
        f'{cap}</figure>'
    )


def relationship_diagram(
    from_label: str,
    to_label: str,
    relation: str,
    *,
    style: str = "has-a",
    caption: str = "",
) -> str:
    """Two boxes connected by one relationship arrow, drawn with a
    notation that matches the relationship's real meaning:

    style="has-a" (composition): a small filled diamond sits at the
    from_label end, a plain arrowhead points at to_label — "the object on
    the left OWNS / holds a reference to the object on the right."

    style="is-a" (inheritance): an open (unfilled) triangle arrowhead
    points from from_label (the child) to to_label (the parent) — the
    classic UML "is a kind of" arrow. Never use this for composition and
    never use the filled-diamond arrow for inheritance; the two
    relationships are not interchangeable.
    """
    box_w, box_h = 220, 72
    gap = 140
    left_x = 10
    right_x = left_x + box_w + gap
    total_w = right_x + box_w + 20
    total_h = box_h + 80

    is_a = style == "is-a"
    line_color = "#5B24F9" if is_a else "#059669"
    cy = 46

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" data-diagram="uml-relationship" aria-label="{html.escape(caption)}" '
        f'style="width:100%;height:auto;max-width:{total_w}px">'
        "<defs>"
        "<marker id='arrowrelis' viewBox='0 0 14 12' refX='13' refY='6' markerWidth='16' markerHeight='14' "
        "orient='auto-start-reverse'><path d='M1,1 L13,6 L1,11 z' fill='#FAFAFC' stroke='#5B24F9' "
        "stroke-width='1.5'/></marker>"
        "<marker id='arrowrelhas' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='8' markerHeight='8' "
        "orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#059669'/></marker>"
        "<marker id='diamondrel' viewBox='0 0 16 10' refX='1' refY='5' markerWidth='11' markerHeight='7' "
        "orient='auto-start-reverse'><path d='M1,5 L8,1 L15,5 L8,9 z' fill='#059669'/></marker>"
        "</defs>"
    ]
    for box_index, (lx, label) in enumerate(((left_x, from_label), (right_x, to_label))):
        box_fill = "#EDE9FE" if box_index == 0 else "#DCFCE7"
        parts.append(
            f'<rect x="{lx}" y="{cy - box_h / 2}" width="{box_w}" height="{box_h}" rx="2" '
            f'fill="{box_fill}" stroke="#0D0230" stroke-width="2"/>'
        )
        lines = _wrap_svg_text(" ".join(label.split()), max_chars=20, max_lines=2)
        first_y = cy - (len(lines) - 1) * 10 + 6
        tspans = "".join(
            f'<tspan x="{lx + box_w / 2}" y="{first_y + li * 21}">{html.escape(line)}</tspan>'
            for li, line in enumerate(lines)
        )
        parts.append(
            f'<text text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-weight="700" '
            f'font-size="17" fill="#0D0230">{tspans}</text>'
        )
    line_x1 = left_x + box_w
    line_x2 = right_x
    marker_end = "url(#arrowrelis)" if is_a else "url(#arrowrelhas)"
    marker_start = "url(#diamondrel)" if not is_a else ""
    extra = f' marker-start="{marker_start}"' if marker_start else ""
    parts.append(
        f'<line x1="{line_x1 + (10 if not is_a else 0)}" y1="{cy}" x2="{line_x2 - 2}" y2="{cy}" '
        f'stroke="{line_color}" stroke-width="2.5" marker-end="{marker_end}"{extra}/>'
    )
    rel_label = relation.upper()
    parts.append(
        f'<text x="{(line_x1 + line_x2) / 2}" y="{cy - 14}" text-anchor="middle" '
        f'font-family="Sora, sans-serif" font-weight="700" font-size="15" letter-spacing="0.04em" '
        f'fill="{line_color}">{html.escape(rel_label)}</text>'
    )
    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>' if caption else ""
    # A bare <svg width:100%> with no HTML width/height attribute has no
    # definite width to resolve against inside display:inline-block (whose
    # own width is auto/shrink-to-fit) — browsers then fall back to the
    # SVG's small CSS-replaced-element default size instead of growing up
    # to max-width. Sizing the wrapper itself (width:min(100%, total_w))
    # gives the SVG a definite width to fill, so it actually reaches its
    # intended size.
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="width:min(100%, {total_w}px);margin:0 auto">{svg}</div>'
        f'{cap}</figure>'
    )


# ---------------------------------------------------------------------------
# Главa 15 — файлы: путь, курсор файла, конвейер память↔диск, до/после записи
# ---------------------------------------------------------------------------


def path_anatomy_diagram(
    path_str: str,
    parts: list[tuple[str, str]],
    *,
    caption: str = "",
) -> str:
    """HTML/CSS breakdown of one path string into labeled parts, e.g.
    path_str="/home/anna/project/data/scores.txt" with
    parts=[("parent", "/home/anna/project/data"), ("name", "scores.txt"),
    ("stem", "scores"), ("suffix", ".txt")]. Renders the whole path as one
    monospace line, then each (label, value) pair as its own labeled chip
    below — reflows on mobile instead of trying to draw brackets under
    sub-spans of the path string, which breaks as soon as the path wraps."""
    chips = "".join(
        f'<div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);'
        f'border-radius:12px;padding:10px 16px;min-width:120px">'
        f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:11px;letter-spacing:.05em;'
        f'text-transform:uppercase;color:#5B24F9;margin-bottom:4px">{html.escape(label)}</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:14px;color:#0D0230;word-break:break-all">'
        f'{html.escape(value) if value else "&mdash;"}</div>'
        f'</div>'
        for label, value in parts
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px 24px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="text-align:center;font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:16px;'
        f'color:#0D0230;background:var(--color-bg-canvas,#fff);border-radius:12px;padding:12px 16px;'
        f'margin-bottom:16px;word-break:break-all">{html.escape(path_str)}</div>'
        f'<div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">{chips}</div>'
        f'{cap}</figure>'
    )


def file_cursor_diagram(
    data: str,
    position: int,
    *,
    label_consumed: str = "прочитано",
    label_remaining: str = "осталось",
    caption: str = "",
) -> str:
    """Cursor/boundary diagram for the file-position mental model: `data`
    rendered as one box per character (spaces as a centered dot), boundary
    numbers 0..len(data) drawn in the gaps between/around them exactly like
    string_slice_diagram(), and ONE pointer (▼) at the `position` boundary —
    everything left of it shaded as label_consumed, everything right of it
    as label_remaining. position must already be a valid boundary
    (0 <= position <= len(data)), resolved by the caller."""
    n = len(data)
    box = 44

    boundary_row = "".join(
        f'<div style="width:{box}px;text-align:center;position:relative">'
        + (
            f'<span style="position:absolute;left:50%;transform:translateX(-50%);top:-20px;'
            f'font-size:16px;color:#DB2777">▼</span>'
            if j == position
            else ""
        )
        + f'<span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:12px;'
        f'color:{"#DB2777" if j == position else "#B9A0FC"}">{j}</span></div>'
        for j in range(n + 1)
    )
    char_row = "".join(
        f'<div style="width:{box}px;height:{box}px;border:1.5px solid #0D0230;border-radius:8px;'
        f'display:flex;align-items:center;justify-content:center;font-family:\'JetBrains Mono\',monospace;'
        f'font-weight:700;font-size:18px;color:#0D0230;'
        f'background:{"#E7DEFF" if i < position else "#fff"}">'
        f'{"·" if ch == " " else html.escape(ch)}</div>'
        for i, ch in enumerate(data)
    )
    legend = (
        f'<div style="display:flex;justify-content:center;gap:22px;margin-top:10px;font-size:13px;'
        f'font-family:Inter,sans-serif;color:#6B6B7D">'
        f'<span><span style="display:inline-block;width:12px;height:12px;background:#E7DEFF;'
        f'border-radius:3px;margin-right:6px;vertical-align:middle"></span>{html.escape(label_consumed)}</span>'
        f'<span><span style="display:inline-block;width:12px;height:12px;background:#fff;'
        f'border:1.5px solid #0D0230;border-radius:3px;margin-right:6px;vertical-align:middle"></span>'
        f'{html.escape(label_remaining)}</span></div>'
    )
    inner = (
        f'<div style="display:flex;margin-left:-{box // 2}px;margin-top:20px">{boundary_row}</div>'
        f'<div style="display:flex;margin:4px 0">{char_row}</div>'
        f'{legend}'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;justify-content:center"><div style="display:inline-block">{inner}</div></div>'
        f'{cap}</figure>'
    )


_PIPELINE_STYLES = {
    "memory": ("#DB2777", "dashed", "#6B6B7D", "#FCE7F3"),
    "file": ("#B45309", "solid", "#92603A", "#FEF3C7"),
    "object": ("#5B24F9", "solid", "#6B6B7D", "#EDE9FE"),
    "plain": ("#0D0230", "solid", "#6B6B7D", "#E5E7EB"),
}


def pipeline_diagram(nodes: list[dict], *, caption: str = "") -> str:
    """Vertical HTML/CSS pipeline of labeled boxes connected by arrows —
    the reusable picture for "program memory ↔ file" and "Python objects →
    serialized text/bytes → file" (and back). Reflows safely on mobile
    because it is a flex column, not an SVG with fixed width math.

    Each item of `nodes` is a dict:
      kind: "memory" (pink dashed box — ephemeral process state),
            "file" (amber solid box — persistent bytes on disk/storage),
            "object" (purple solid box — a Python object/value),
            "plain" (neutral box — anything else, e.g. "программа
            завершается")
      title: header text of the box
      rows: optional list of strings shown stacked inside the box
            (e.g. "score = 1200"); omit or [] for a title-only box
      note: optional short label drawn on the arrow ABOVE this node
            (e.g. "программа завершается", "следующий запуск") — ignored
            on the first node, which has no incoming arrow
    """
    parts = []
    for i, node in enumerate(nodes):
        kind = node.get("kind", "plain")
        title = node.get("title", "")
        rows = node.get("rows") or []
        note = node.get("note", "")
        color, border_style, row_color, background = _PIPELINE_STYLES.get(kind, _PIPELINE_STYLES["plain"])
        if i > 0:
            note_html = (
                f'<div style="font-size:12px;font-family:Inter,sans-serif;color:#6B6B7D;'
                f'margin:2px 0">{html.escape(note)}</div>'
                if note
                else ""
            )
            parts.append(
                f'<div style="display:flex;flex-direction:column;align-items:center;margin:2px 0">'
                f'{note_html}<span style="font-size:20px;color:#B9A0FC">↓</span></div>'
            )
        rows_html = "".join(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:13.5px;color:{row_color};'
            f'text-align:center">{html.escape(row)}</div>'
            for row in rows
        )
        parts.append(
            f'<div data-diagram-node="pipeline" style="min-width:220px;max-width:340px;padding:14px 20px;'
            f'border-radius:4px;background:{background};border:2px {border_style} {color};text-align:center">'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:15px;'
            f'color:{color}">{html.escape(title)}</div>'
            + (f'<div style="margin-top:8px;display:flex;flex-direction:column;gap:3px">{rows_html}</div>' if rows_html else "")
            + '</div>'
        )
    body = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;flex-direction:column;align-items:center">{body}</div>'
        f'{cap}</figure>'
    )


def file_state_diagram(
    before_label: str,
    before_lines: list[str],
    after_label: str,
    after_lines: list[str],
    *,
    action_label: str = "",
    caption: str = "",
) -> str:
    """BEFORE/AFTER file-content comparison: two amber "file" boxes (same
    visual language as pipeline_diagram's kind="file") side by side —
    wraps to a column on narrow screens — with an arrow and optional
    action_label (the code/mode that ran) between them. before_lines/
    after_lines are shown one per line inside each box; pass [] to show an
    empty-file box, which is exactly the picture "w" truncation needs."""

    def box(label: str, lines: list[str]) -> str:
        content = "".join(
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:13.5px;color:#92603A;'
            f'white-space:pre-wrap">{html.escape(line)}</div>'
            for line in lines
        ) or '<div style="font-family:\'JetBrains Mono\',monospace;font-size:13.5px;color:#B9A0FC;font-style:italic">(пустой файл)</div>'
        return (
            f'<div data-diagram-node="file-state" style="flex:1 1 200px;min-width:180px;padding:14px 18px;'
            f'border-radius:4px;background:#FEF3C7;border:2px solid #B45309">'
            f'<div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;'
            f'text-transform:uppercase;color:#B45309;margin-bottom:8px">{html.escape(label)}</div>'
            f'{content}</div>'
        )

    arrow = (
        f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;'
        f'padding:0 10px;flex:0 0 auto">'
        + (f'<div style="font-size:12px;font-family:\'JetBrains Mono\',monospace;color:#6B6B7D;'
           f'margin-bottom:4px;white-space:nowrap">{html.escape(action_label)}</div>' if action_label else "")
        + '<span style="font-size:22px;color:#B9A0FC">→</span></div>'
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        f'<div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px">'
        f'{box(before_label, before_lines)}{arrow}{box(after_label, after_lines)}</div>'
        f'{cap}</figure>'
    )


# ---------------------------------------------------------------------------
# Главa 16 — Tkinter: витрина виджетов (реальные скриншоты, не имитация)
# ---------------------------------------------------------------------------


def gui_component_card(
    name: str,
    purpose: str,
    screenshots: list[tuple[str, str, str]],
    *,
    when_to_use: str = "",
    api: str = "",
    trap: str = "",
    is_schematic: bool = False,
) -> str:
    """One widget's "contact sheet" entry: name, one-line purpose, one or
    more REAL screenshots (each a (src, alt, small_state_label) triple —
    e.g. two entries for "снят"/"установлен" checkbox states), then compact
    "когда использовать" / API / "частая ошибка" notes. Used standalone or
    stacked into gui_component_gallery().

    is_schematic=True switches the screenshot area's own small label to
    "Схематическое изображение" instead of nothing — use ONLY when a native
    screenshot genuinely cannot be captured (e.g. an open native dropdown
    popup); never for anything a real Tk window can show."""
    shots_html = "".join(
        f'<figure style="margin:0;flex:1 1 160px;min-width:140px">'
        f'<img src="{html.escape(src)}" alt="{html.escape(alt)}" '
        f'style="width:100%;height:auto;border-radius:12px;border:1px solid var(--color-border-default,#E4E1F5);display:block;background:#fff" />'
        + (f'<figcaption style="text-align:center;font-size:11.5px;color:var(--ink-soft,#6B6B7D);margin-top:4px">{html.escape(state_label)}</figcaption>' if state_label else "")
        + '</figure>'
        for src, alt, state_label in screenshots
    )
    schematic_note = (
        '<div style="font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;'
        'color:#B45309;margin-bottom:6px">Схематическое изображение</div>'
        if is_schematic
        else ""
    )
    meta_rows = "".join(
        f'<div style="margin-top:8px;font-size:13px;line-height:1.5"><strong>{html.escape(label)}:</strong> {value}</div>'
        for label, value in (
            ("Когда использовать", when_to_use),
            ("API", api),
            ("Частая ошибка", trap),
        )
        if value
    )
    return f"""
    <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);
      border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:4px">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:15px;color:#5B24F9">{html.escape(name)}</div>
      <div style="font-size:13.5px;color:#0D0230;margin-bottom:8px">{html.escape(purpose)}</div>
      {schematic_note}
      <div style="display:flex;gap:10px;flex-wrap:wrap">{shots_html}</div>
      {meta_rows}
    </div>"""


def gui_component_gallery(cards_html: list[str], *, title: str = "", caption: str = "") -> str:
    """Responsive CSS-grid wall of gui_component_card() entries — 3 columns
    desktop, 2 tablet, 1 mobile, via the same auto-fit pattern as
    capability_map(), so it never degrades into a tiny-text multi-column
    strip on narrow screens."""
    title_html = (
        f'<div style="text-align:center;font-family:Sora,sans-serif;font-weight:700;font-size:18px;'
        f'margin-bottom:16px;color:#0D0230">{html.escape(title)}</div>'
        if title
        else ""
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">'
        f'{title_html}'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px">{"".join(cards_html)}</div>'
        f'{cap}'
        f'</figure>'
    )


def color_swatch_row(swatches: list[tuple[str, str, str]]) -> str:
    """Row of real color patches — each (hex, human_name, hex_label) — so a
    color is always seen before its numeric value, never the numeric value
    alone. Wraps to multiple rows on narrow screens."""
    chips = "".join(
        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;'
        f'background:var(--color-bg-canvas,#fff);border:1px solid var(--color-border-default,#E4E1F5);'
        f'border-radius:12px;min-width:170px">'
        f'<span style="width:28px;height:28px;border-radius:8px;background:{html.escape(hexval)};'
        f'border:1px solid rgba(0,0,0,.15);flex-shrink:0"></span>'
        f'<span style="font-size:13px;line-height:1.3"><strong>{html.escape(name)}</strong><br>'
        f'<span style="font-family:\'JetBrains Mono\',monospace;color:var(--ink-soft,#6B6B7D)">{html.escape(hexval)}</span></span>'
        f'</div>'
        for hexval, name, _label in swatches
    )
    return (
        f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin:20px 0">{chips}</div>'
    )


def _schematic_label() -> str:
    return (
        '<div style="font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;'
        'color:#B45309;margin-bottom:8px">🔶 Схематическое изображение (не реальный скриншот)</div>'
    )


_MESSAGEBOX_ACCENTS = {
    "info": ("#5B24F9", "ℹ️"),
    "warning": ("#B45309", "⚠️"),
    "error": ("#DB2777", "⛔"),
}


def messagebox_schematic(kind: str, title: str, message: str, buttons: list[str]) -> str:
    """Clearly-labeled schematic of one native messagebox dialog — used
    because the native dialog itself cannot be captured reliably headless
    (see generate_chapter_16_outputs.py). NEVER pass this off as a real
    screenshot; the schematic label is always rendered."""
    accent, icon = _MESSAGEBOX_ACCENTS.get(kind, _MESSAGEBOX_ACCENTS["info"])
    btns = "".join(
        f'<div style="padding:5px 16px;border:1px solid #9a97a8;border-radius:4px;'
        f'font-size:12.5px;background:#ececec;color:#222">{html.escape(b)}</div>'
        for b in buttons
    )
    return f"""
    <div style="max-width:280px;border-radius:8px;border:1px solid #9a97a8;overflow:hidden;
      box-shadow:0 6px 16px rgba(0,0,0,.15);font-family:sans-serif">
      <div style="background:#e2e2e2;padding:6px 10px;font-size:12px;color:#333;border-bottom:1px solid #b8b8b8">{html.escape(title)}</div>
      <div style="background:#ececec;padding:16px;display:flex;gap:12px;align-items:flex-start">
        <span style="font-size:22px;line-height:1">{icon}</span>
        <span style="font-size:13px;color:#111;padding-top:2px">{html.escape(message)}</span>
      </div>
      <div style="background:#ececec;padding:8px 12px;display:flex;gap:8px;justify-content:flex-end;
        border-top:1px solid #d5d5d5">{btns}</div>
    </div>"""


def messagebox_gallery(entries: list[tuple[str, str, str, list[str]]], *, caption: str = "") -> str:
    """Row of messagebox_schematic() cards — entries are (kind, title,
    message, buttons)."""
    cards = "".join(messagebox_schematic(kind, title, message, buttons) for kind, title, message, buttons in entries)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:12px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">'
        f'{_schematic_label()}'
        f'<div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center">{cards}</div>'
        f'{cap}</figure>'
    )


def menu_bar_schematic(menu_labels: list[str], open_index: int, open_items: list[str]) -> str:
    """Clearly-labeled schematic of a window's menu bar with one menu open
    — used because tk.Menu does not render visibly under a headless X
    server without a window manager (confirmed: the menu-bar strip and its
    popdown are simply blank in that environment), so no reliable native
    screenshot exists to capture. NEVER pass this off as a real screenshot;
    the schematic label is always rendered."""
    bar_items = "".join(
        f'<div style="padding:5px 12px;font-size:13px;'
        + (f'background:#dcdcdc;color:#111;font-weight:600' if i == open_index else 'color:#222')
        + f'">{html.escape(label)}</div>'
        for i, label in enumerate(menu_labels)
    )
    rows = []
    for item in open_items:
        if item == "---":
            rows.append('<div style="height:1px;background:#d5d5d5;margin:4px 0"></div>')
        else:
            rows.append(f'<div style="padding:5px 22px 5px 14px;font-size:13px;color:#111;white-space:nowrap">{html.escape(item)}</div>')
    dropdown = "".join(rows)
    return f"""
    <figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      {_schematic_label()}
      <div style="display:flex;justify-content:center">
        <div style="border:1px solid #9a97a8;border-radius:6px;overflow:visible;position:relative;
          background:#ececec;min-width:260px;box-shadow:0 4px 12px rgba(0,0,0,.1)">
          <div style="display:flex;border-bottom:1px solid #cfcfcf;background:#f4f4f4">{bar_items}</div>
          <div style="height:90px"></div>
          <div style="position:absolute;top:30px;left:0;background:#ececec;border:1px solid #9a97a8;
            border-radius:0 4px 4px 4px;box-shadow:0 6px 14px rgba(0,0,0,.18);padding:4px 0;min-width:170px">
            {dropdown}
          </div>
        </div>
      </div>
    </figure>"""


# ---------------------------------------------------------------------------
# Навигация / компоновка страницы
# ---------------------------------------------------------------------------

# Site-wide top-nav sections, in display order. The anchor ids must match the
# real `id="..."` elements on site/index.html (see build_site_index.py) —
# this is the single source of truth both the desktop bar and the mobile
# drawer render from, so they can never drift into different destinations.
TOP_NAV_ITEMS = [
    ("o-kurse", "О курсе"),
    ("glavy", "Главы"),
    ("praktika", "Практика"),
    ("proekty", "Проекты"),
    ("spravochnik", "Справочник"),
]


def _top_nav_items_html(active_section: str | None, li_class: str = "") -> str:
    parts = []
    for anchor, label in TOP_NAV_ITEMS:
        classes = (li_class + " active").strip() if anchor == active_section else li_class
        cls_attr = f' class="{classes}"' if classes else ""
        parts.append(f'<li><a href="/index.html#{anchor}"{cls_attr}>{html.escape(label)}</a></li>')
    return "".join(parts)


def site_header(active_section: str | None = "glavy") -> str:
    """Shared site header: home-linking logo + desktop top-nav + mobile toggle.

    All hrefs are root-relative (the site is deployed at the domain root), so
    this is depth-independent — no more counting '../' per page. The toggle
    button's aria-controls points at "mobile-nav-panel"; every page template
    must give its mobile drawer element that same id (see mobile_nav_links()
    and site/assets/js/nav.js, which drives the open/close behavior for any
    element referenced this way, regardless of which template renders it).
    """
    nav_items = _top_nav_items_html(active_section)
    return (
        '<header class="site-header">\n'
        '  <a class="brand" href="/index.html">\n'
        '    <img src="/assets/img/logo.png" alt="Cartesian School" />\n'
        '    <span class="brand-word">Cartesian<span class="school">School</span></span>\n'
        "  </a>\n"
        f'  <ul class="top-nav">{nav_items}</ul>\n'
        '  <button class="nav-toggle" type="button" aria-expanded="false" '
        'aria-controls="mobile-nav-panel">☰ Меню</button>\n'
        "</header>"
    )


def mobile_nav_links(active_section: str | None = "glavy") -> str:
    """The site-wide nav links, for inclusion inside a page's mobile drawer.

    Kept separate from any page-local table of contents so it can be
    prepended into an existing `.sidebar` (chapter pages) or used as the
    entire contents of a page's mobile drawer (pages with no page-local TOC:
    the homepage, chapter openers, practice pages).
    """
    items = _top_nav_items_html(active_section, li_class="")
    return f'<div class="mobile-nav-links"><ul class="toc-list">{items}</ul></div>'


NAV_SCRIPT_TAG = '<script src="/assets/js/nav.js" defer></script>'


@dataclass
class NavItem:
    title: str
    href: str
    active: bool = False
    sub: bool = False


@dataclass
class SidebarGroup:
    title: str
    items: list[NavItem] = field(default_factory=list)


@dataclass
class PageNav:
    prev_href: str | None = None
    prev_label: str | None = None
    next_href: str | None = None
    next_label: str | None = None


@dataclass(frozen=True)
class BrandedHeading:
    """Trusted description of an H1 with external technology branding.

    The builder passes only plain text and a known brand variant.  Rendering
    stays centralized, so official assets, accessibility attributes, and
    responsive sizing cannot drift from page to page.
    """

    text: str
    brand: str


def git_heading(text: str) -> BrandedHeading:
    """Return an H1 model with the official Git mark before visible text."""
    return BrandedHeading(text=text, brand="git")


def git_github_heading(text: str) -> BrandedHeading:
    """Return a balanced mixed Git/GitHub H1 without merging the brands."""
    return BrandedHeading(text=text, brand="git-github")


def _render_h1(heading: str | BrandedHeading) -> str:
    if isinstance(heading, str):
        return f"<h1>{html.escape(heading)}</h1>"

    text = html.escape(heading.text)
    if heading.brand == "git":
        marks = (
            '<span class="technology-heading__brands" aria-hidden="true">'
            '<img class="technology-heading__mark technology-heading__mark--git" '
            'src="/assets/brand/git/mark-orange.svg" alt=""></span>'
        )
    elif heading.brand == "git-github":
        marks = (
            '<span class="technology-heading__brands technology-heading__brands--pair" '
            'aria-hidden="true">'
            '<span class="technology-heading__brand-token">'
            '<img class="technology-heading__mark technology-heading__mark--git" '
            'src="/assets/brand/git/mark-orange.svg" alt=""><span>Git</span></span>'
            '<span class="technology-heading__not-equal">≠</span>'
            '<span class="technology-heading__brand-token">'
            '<img class="technology-heading__mark technology-heading__mark--github" '
            'src="/assets/brand/github/invertocat-black.svg" alt=""><span>GitHub</span></span>'
            '</span>'
        )
    else:
        raise ValueError(f"unknown heading brand: {heading.brand!r}")
    return f'<h1 class="technology-heading">{marks}<span>{text}</span></h1>'


def render_sidebar(groups: list[SidebarGroup]) -> str:
    parts = []
    for g in groups:
        parts.append(f'<div class="sidebar-title">{html.escape(g.title)}</div>')
        items = []
        for it in g.items:
            cls = []
            if it.active:
                cls.append("active")
            if it.sub:
                cls.append("sub")
            cls_attr = f' class="{" ".join(cls)}"' if cls else ""
            items.append(f'<li><a href="{html.escape(it.href)}"{cls_attr}>{html.escape(it.title)}</a></li>')
        parts.append(f'<ul class="toc-list">{"".join(items)}</ul>')
    return "".join(parts)


def _page_nav_label(href: str | None, fallback: str | None) -> str:
    """Canonicalize only cross-chapter opener links; keep local labels intact."""
    if href:
        match = re.search(r"(?:^|/)glava-(\d{2})/index\.html$", href)
        if match:
            number = int(match.group(1))
            return f"Глава {number}: {chapter(number).title}"
    return fallback or ""


def render_page(
    *,
    page_title: str,
    description: str,
    depth: int,
    breadcrumb: list[tuple[str, str]],
    kicker: str,
    h1: str | BrandedHeading,
    lede: str,
    body_html: str,
    sidebar_groups: list[SidebarGroup],
    nav: PageNav,
    active_section: str | None = "glavy",
) -> str:
    """depth: how many '../' needed to reach site/ root from this file's folder
    (used only for page-local asset paths — the shared header/nav below is
    root-relative regardless of depth, see site_header())."""
    root = "../" * depth

    crumb_parts = []
    for i, (label, href) in enumerate(breadcrumb):
        if href:
            crumb_parts.append(f'<a href="{html.escape(href)}">{html.escape(label)}</a>')
        else:
            crumb_parts.append(html.escape(label))
    breadcrumb_html = " / ".join(crumb_parts)

    sidebar_html = render_sidebar(sidebar_groups)
    h1_html = _render_h1(h1)

    nav_html = '<div class="section-nav">'
    if nav.prev_href:
        prev_label = _page_nav_label(nav.prev_href, nav.prev_label)
        nav_html += f'<a href="{html.escape(nav.prev_href)}"><div class="dir">← Назад</div><div class="lbl">{html.escape(prev_label)}</div></a>'
    else:
        nav_html += "<div></div>"
    if nav.next_href:
        next_label = _page_nav_label(nav.next_href, nav.next_label)
        nav_html += f'<a href="{html.escape(nav.next_href)}" class="next"><div class="dir">Далее →</div><div class="lbl">{html.escape(next_label)}</div></a>'
    nav_html += "</div>"

    return _render_icon_markers(f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(page_title)} — Python с нуля — Cartesian School</title>
<meta name="description" content="{html.escape(description)}" />
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/theory.css" />
</head>
<body>

{site_header(active_section)}

<div class="layout">
  <nav class="sidebar" id="mobile-nav-panel">
    {mobile_nav_links(active_section)}
    {sidebar_html}
  </nav>

  <article>
    <div class="breadcrumb">{breadcrumb_html}</div>
    <div class="section-kicker">{f'<img src="{root}assets/img/brand/python-logo-mark.svg" alt="" aria-hidden="true" />' if kicker.startswith("Глава ") else ""}{html.escape(kicker)}</div>
    {h1_html}
    <p class="lede">{lede}</p>

{body_html}

    {nav_html}
  </article>
</div>

{NAV_SCRIPT_TAG}
</body>
</html>
""")


@dataclass
class ChapterSectionLink:
    num: str
    title: str
    href: str


def render_chapter_opener(
    *,
    chapter_num: int,
    description: str,
    meta_items: list[str],
    sections: list[ChapterSectionLink],
    brand_html: str = "",
    intro_html: str = "",
) -> str:
    root = "../../"
    canonical = chapter(chapter_num)
    title = canonical.title
    physical_page = chapter_start(chapter_num)
    meta_html = "".join(f"<span>{m}</span>" for m in meta_items)
    rows = []
    for section in sections:
        absolute_url = urljoin(canonical.url, section.href)
        section_page = page_for_url(absolute_url)
        page_html = f'<span class="si-page">{section_page}</span>' if section_page else ""
        rows.append(
            f'<a class="section-item" href="{html.escape(section.href)}">'
            f'<span><span class="si-num">{html.escape(section.num)}</span>'
            f'{html.escape(section.title)}</span>{page_html}</a>'
        )
    rows_html = "".join(rows)
    return _render_icon_markers(f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Глава {chapter_num}. {html.escape(title)} — Python с нуля — Cartesian School</title>
<meta name="description" content="{html.escape(description)}" />
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/theory.css" />
<style>
  .chapter-hero {{
    background: radial-gradient(ellipse 900px 500px at 20% -20%, #2a1470 0%, var(--navy-900) 45%, var(--navy-950) 100%);
    color: var(--color-text-inverse);
    padding: var(--spacing-4xl) var(--spacing-2xl);
  }}
  .chapter-hero-inner {{ max-width: 900px; margin: 0 auto; }}
  .chapter-num {{ display: flex; align-items: flex-start; gap: 8px; font-family: 'JetBrains Mono', monospace; color: var(--blue-300); font-size: 15px; margin-bottom: var(--spacing-sm); }}
  .chapter-num img {{ width: 22px; height: 22px; display: block; flex-shrink: 0; }}
  .chapter-hero h1 {{ color: white; font-size: 44px; max-width: 640px; }}
  .chapter-hero p {{ color: var(--gray-400); font-size: 18px; max-width: 560px; margin-top: var(--spacing-md); }}
  .chapter-meta {{ display: flex; gap: var(--spacing-xl); margin-top: var(--spacing-xl); font-size: 14px; color: var(--blue-300); flex-wrap: wrap; }}
  .section-list {{ max-width: 900px; margin: var(--spacing-2xl) auto; padding: 0 var(--spacing-2xl); }}
  .section-item {{ display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-md); border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin-bottom: var(--spacing-sm); text-decoration: none; color: var(--color-text-primary); }}
  .section-item:hover {{ border-color: var(--color-brand-blue); }}
  .section-item > span:first-child {{ min-width: 0; overflow-wrap: anywhere; }}
  .section-item .si-num {{ font-family: 'JetBrains Mono', monospace; color: var(--color-text-muted); font-size: 13px; margin-right: var(--spacing-md); }}
  .section-item .si-page {{ flex: none; margin-left: var(--spacing-md); font-family: 'JetBrains Mono', monospace; color: var(--color-text-muted); font-size: 13px; }}
  .chapter-intro {{ max-width: 900px; margin: var(--spacing-2xl) auto 0; padding: 0 var(--spacing-2xl); }}
  @media (max-width: 860px) {{ .chapter-hero h1 {{ font-size: 30px; }} }}
</style>
</head>
<body>

{site_header("glavy")}
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links("glavy")}
</nav>

<div class="chapter-hero">
  <div class="chapter-hero-inner">
{brand_html}
    <div class="chapter-num"><img src="{root}assets/img/brand/python-logo-mark.svg" alt="" aria-hidden="true" />ГЛАВА {chapter_num} · СТР. {physical_page}</div>
    <h1>{html.escape(title)}</h1>
    <p>{description}</p>
    <div class="chapter-meta">{meta_html}</div>
  </div>
</div>

<div class="chapter-intro">
  {intro_html}
</div>

<div class="section-list">
  {rows_html}
</div>

{NAV_SCRIPT_TAG}
</body>
</html>
""")


# ---------------------------------------------------------------------------
# Проекты — визуальные карточки (site/index.html #proekty) и страницы проектов
# ---------------------------------------------------------------------------
#
# Ни один из projects/**/*.py не имеет собственного скриншота или готового
# арт-ассета (projects/**/ содержит только .py-файлы и, для todo-app,
# static/templates без изображений). Поэтому каждая карточка получает
# оригинальную встроенную SVG-иллюстрацию, написанную вручную по реальному
# содержимому конкретного проекта — тот же приём, что уже применяется в
# flow_diagram() выше (векторная графика, ноль внешних запросов, доли
# килобайта на карточку), а не сгенерированная растровая картинка.

# (project id -> (акцентный цвет 1, акцентный цвет 2)) — общая формула
# "фирменный градиент + один акцент" держит карточки единым визуальным
# семейством, при этом акцент делает каждую карточку узнаваемой.
PROJECT_ACCENTS: dict[str, tuple[str, str]] = {
    "paint-app": ("var(--violet-500)", "var(--blue-500)"),
    "snake": ("var(--green-500)", "var(--blue-600)"),
    "bouncing-ball": ("var(--amber-500)", "var(--violet-500)"),
    "space-shooter": ("var(--navy-950)", "var(--violet-500)"),
    "todo-app": ("var(--blue-500)", "var(--green-500)"),
    "calculator": ("var(--gray-800)", "var(--violet-500)"),
    "story-generator": ("var(--violet-500)", "var(--amber-500)"),
    "rock-paper-scissors": ("var(--red-500)", "var(--amber-500)"),
    "bouncing-balls-oop": ("var(--blue-500)", "var(--green-500)"),
    "temperature-converter": ("var(--blue-500)", "var(--red-500)"),
    "notes-app": ("var(--gray-600)", "var(--blue-500)"),
    "tic-tac-toe": ("var(--navy-950)", "var(--blue-500)"),
    "safesort": ("var(--navy-950)", "var(--green-500)"),
}


def _project_icon_svg(project_id: str) -> str:
    """Inner SVG markup (icon only, white/light fills at partial opacity) for
    one project, centered roughly on (200, 112) in a 400x225 viewBox. Each
    icon is a deliberate, legible composition of the real project's own
    subject matter (its actual mechanic/UI), not a generic pictogram.
    """
    if project_id == "paint-app":
        return """
        <circle cx="150" cy="95" r="30" fill="#fff" opacity=".85"/>
        <circle cx="205" cy="80" r="24" fill="#fff" opacity=".55"/>
        <circle cx="230" cy="130" r="26" fill="#fff" opacity=".7"/>
        <rect x="120" y="150" width="140" height="18" rx="9" fill="#fff" opacity=".9" transform="rotate(-8 190 159)"/>"""
    if project_id == "snake":
        return """
        <g fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".9">
          <path d="M110 150 h40 v-40 h40 v-40 h40 v40 h40"/>
        </g>
        <circle cx="290" cy="70" r="10" fill="#fff" opacity=".95"/>"""
    if project_id == "bouncing-ball":
        return """
        <circle cx="150" cy="145" r="10" fill="#fff" opacity=".3"/>
        <circle cx="175" cy="120" r="14" fill="#fff" opacity=".5"/>
        <circle cx="205" cy="95" r="30" fill="#fff" opacity=".95"/>
        <path d="M120 168 q85 26 170 0" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 8" opacity=".35"/>"""
    if project_id == "bouncing-balls-oop":
        # Several independent objects, each on its own trajectory — the
        # visual point of the OOP variant vs. the single-ball original.
        return """
        <circle cx="120" cy="150" r="9" fill="#fff" opacity=".35"/>
        <circle cx="150" cy="110" r="16" fill="#fff" opacity=".8"/>
        <circle cx="210" cy="150" r="11" fill="#fff" opacity=".45"/>
        <circle cx="245" cy="95" r="22" fill="#fff" opacity=".95"/>
        <circle cx="290" cy="135" r="13" fill="#fff" opacity=".6"/>
        <path d="M100 168 q100 30 200 0" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 8" opacity=".3"/>"""
    if project_id == "space-shooter":
        return """
        <polygon points="200,60 175,140 200,122 225,140" fill="#fff" opacity=".95"/>
        <rect x="192" y="35" width="6" height="18" rx="3" fill="#fff" opacity=".8"/>
        <rect x="204" y="35" width="6" height="18" rx="3" fill="#fff" opacity=".8"/>
        <circle cx="130" cy="55" r="3" fill="#fff" opacity=".8"/>
        <circle cx="270" cy="45" r="3" fill="#fff" opacity=".6"/>
        <circle cx="290" cy="90" r="2.5" fill="#fff" opacity=".7"/>
        <circle cx="120" cy="110" r="2.5" fill="#fff" opacity=".5"/>"""
    if project_id == "todo-app":
        rows_y = [70, 105, 140]
        rows = []
        for i, y in enumerate(rows_y):
            rows.append(f'<rect x="120" y="{y}" width="160" height="20" rx="10" fill="#fff" opacity="{".9" if i else ".55"}"/>')
        check = '<path d="M132 80 l7 7 12 -14" fill="none" stroke="var(--navy-950)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>'
        return "\n        ".join(rows) + "\n        " + check
    if project_id == "calculator":
        cells = []
        for row in range(3):
            for col in range(4):
                x = 130 + col * 38
                y = 60 + row * 38
                op = ".9" if (row + col) % 2 == 0 else ".55"
                cells.append(f'<rect x="{x}" y="{y}" width="28" height="28" rx="7" fill="#fff" opacity="{op}"/>')
        return "\n        ".join(cells)
    if project_id == "story-generator":
        # An open book feeding into a spark of generated text — clearer
        # "random story assembly" read than the original stray robot face.
        return """
        <path d="M130 150 V85 q0 -12 12 -12 h45 v77 z" fill="#fff" opacity=".85"/>
        <path d="M270 150 V85 q0 -12 -12 -12 h-45 v77 z" fill="#fff" opacity=".7"/>
        <rect x="148" y="98" width="34" height="6" rx="3" fill="var(--navy-950)" opacity=".25"/>
        <rect x="148" y="112" width="26" height="6" rx="3" fill="var(--navy-950)" opacity=".25"/>
        <rect x="218" y="98" width="34" height="6" rx="3" fill="var(--navy-950)" opacity=".2"/>
        <path d="M270 55 l6 14 14 6 -14 6 -6 14 -6 -14 -14 -6 14 -6 z" fill="#fff" opacity=".95"/>"""
    if project_id == "rock-paper-scissors":
        # Three distinct, legible silhouettes side by side rather than one
        # ambiguous cluster — rock (textured circle), paper (card), scissors
        # (crossed blades with visible finger loops).
        return """
        <circle cx="130" cy="115" r="26" fill="#fff" opacity=".9"/>
        <circle cx="122" cy="106" r="3.5" fill="var(--navy-950)" opacity=".18"/>
        <circle cx="138" cy="122" r="3" fill="var(--navy-950)" opacity=".18"/>
        <rect x="182" y="82" width="42" height="56" rx="6" fill="#fff" opacity=".75"/>
        <rect x="190" y="94" width="26" height="4" rx="2" fill="var(--navy-950)" opacity=".2"/>
        <rect x="190" y="104" width="26" height="4" rx="2" fill="var(--navy-950)" opacity=".2"/>
        <g stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none" opacity=".95">
          <path d="M258 90 L300 132 M298 90 L256 132"/>
        </g>
        <circle cx="258" cy="90" r="7" fill="none" stroke="#fff" stroke-width="4" opacity=".8"/>
        <circle cx="298" cy="90" r="7" fill="none" stroke="#fff" stroke-width="4" opacity=".8"/>"""
    if project_id == "temperature-converter":
        return """
        <rect x="192" y="45" width="16" height="85" rx="8" fill="#fff" opacity=".9"/>
        <circle cx="200" cy="145" r="20" fill="#fff" opacity=".95"/>
        <rect x="196" y="60" width="8" height="65" rx="4" fill="var(--red-500)" opacity=".9"/>
        <circle cx="200" cy="145" r="11" fill="var(--red-500)" opacity=".9"/>"""
    if project_id == "notes-app":
        return """
        <path d="M140 55 h90 l30 30 v90 h-120 z" fill="#fff" opacity=".9"/>
        <path d="M230 55 v30 h30 z" fill="#fff" opacity=".5"/>
        <rect x="155" y="105" width="90" height="7" rx="3.5" fill="var(--navy-950)" opacity=".35"/>
        <rect x="155" y="123" width="90" height="7" rx="3.5" fill="var(--navy-950)" opacity=".35"/>
        <rect x="155" y="141" width="55" height="7" rx="3.5" fill="var(--navy-950)" opacity=".35"/>"""
    if project_id == "safesort":
        # A folder receiving files that are already sorted into labeled
        # bins, with a small shield-checkmark standing for the safety
        # contract (nothing moves without an explicit apply).
        return """
        <path d="M110 150 V95 q0 -8 8 -8 h34 l14 16 h74 q8 0 8 8 v39 z" fill="#fff" opacity=".55"/>
        <rect x="150" y="100" width="34" height="34" rx="6" fill="#fff" opacity=".9"/>
        <rect x="192" y="100" width="34" height="34" rx="6" fill="#fff" opacity=".75"/>
        <rect x="234" y="100" width="34" height="34" rx="6" fill="#fff" opacity=".6"/>
        <path d="M280 55 l22 8 v20 q0 22 -22 30 q-22 -8 -22 -30 v-20 z" fill="#fff" opacity=".95"/>
        <path d="M271 84 l6 6 12 -14" fill="none" stroke="var(--navy-950)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>"""
    if project_id == "tic-tac-toe":
        return """
        <g stroke="#fff" stroke-width="6" opacity=".55">
          <path d="M170 55 v120 M230 55 v120 M140 90 h120 M140 145 h120"/>
        </g>
        <g stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".95">
          <path d="M148 68 l32 32 M180 68 l-32 32"/>
        </g>
        <circle cx="255" cy="118" r="17" fill="none" stroke="#fff" stroke-width="9" opacity=".95"/>"""
    return '<circle cx="200" cy="112" r="30" fill="#fff" opacity=".8"/>'


def _story_generator_scene() -> str:
    """Bespoke web illustration for story-generator: three independent source
    pools feed a random-selection hub that assembles one generated result —
    replaces the old generic icon-in-wrapper composition (two document
    sheets + a sparkle) with a purpose-built scene that reads as "random
    composition" on sight.

    Deliberately independent of _project_icon_svg(), which the closed
    PDF/EPUB appendix (project_publication_illustration()) still relies on
    unchanged — this scene is consumed only by project_illustration(), so
    the accepted publication byte contract for this project is untouched.
    """
    tokens_y = [44, 98, 152]
    token_opacity = [".92", ".78", ".62"]
    token_bar_w = [44, 34, 26]
    tokens_html = "".join(
        f'<g class="story-token">'
        f'<rect x="34" y="{y}" width="76" height="32" rx="9" fill="#fff" opacity="{op}"/>'
        f'<rect x="46" y="{y + 13}" width="{w}" height="7" rx="3.5" fill="var(--navy-950)" opacity=".24"/>'
        f'</g>'
        for y, op, w in zip(tokens_y, token_opacity, token_bar_w)
    )
    return f"""
  <g class="story-routes" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="4 7" opacity=".55">
    <path class="story-route" d="M110 60 Q150 60 190 112"/>
    <path class="story-route" d="M110 114 Q150 114 190 112"/>
    <path class="story-route" d="M110 168 Q150 168 190 112"/>
    <path class="story-route story-route--out" d="M198 112 L244 112"/>
  </g>
  <g class="story-tokens">{tokens_html}</g>
  <g class="story-hub" fill="#fff">
    <circle class="story-hub-dot" cx="185" cy="105" r="2.6"/>
    <circle class="story-hub-dot" cx="197" cy="105" r="2.6"/>
    <circle class="story-hub-dot" cx="191" cy="120" r="2.6"/>
  </g>
  <g class="story-output">
    <rect class="story-output-card" x="244" y="44" width="122" height="140" rx="16" fill="#fff" opacity=".95"/>
    <g class="story-output-lines">
      <rect class="story-output-line" x="262" y="78" width="88" height="9" rx="4.5" fill="var(--navy-950)" opacity=".8"/>
      <rect class="story-output-line story-output-line--accent" x="262" y="100" width="68" height="9" rx="4.5" fill="var(--amber-500)" opacity=".95"/>
      <rect class="story-output-line" x="262" y="122" width="56" height="9" rx="4.5" fill="var(--navy-950)" opacity=".45"/>
    </g>
  </g>
  <path class="story-spark" d="M356 30 l6 14 14 6 -14 6 -6 14 -6 -14 -14 -6 14 -6 z" fill="var(--amber-500)" opacity=".95"/>"""


def project_illustration(project_id: str) -> str:
    """Self-contained 16:9 inline SVG illustration for one real project, used
    both on the homepage Projects card and the project's own detail page.
    Purely decorative (the card/page title carries the accessible name), so
    aria-hidden="true" — no meaningful alt text is lost.
    """
    c1, c2 = PROJECT_ACCENTS.get(project_id, ("var(--navy-900)", "var(--violet-500)"))
    if project_id == "story-generator":
        scene = _story_generator_scene()
    else:
        icon = _project_icon_svg(project_id)
        scene = f"""
  <path class="project-art__route" d="M34 183 C102 150 135 190 202 162 S320 120 370 151" fill="none" stroke="#fff" stroke-width="1" stroke-dasharray="3 8" opacity=".16"/>
  <g class="project-art__subject">{icon}</g>
  <g class="project-art__nodes" fill="#fff">
    <circle cx="34" cy="183" r="2.5"/><circle cx="202" cy="162" r="2.5"/><circle cx="370" cy="151" r="2.5"/>
  </g>"""
    return f"""<svg class="project-art project-art--{project_id}" viewBox="0 0 400 225" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="grad-{project_id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <pattern id="grid-{project_id}" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M25 0H0V25" fill="none" stroke="#fff" stroke-width=".7" opacity=".12"/>
    </pattern>
  </defs>
  <rect width="400" height="225" fill="url(#grad-{project_id})"/>
  <rect class="project-art__grid" width="400" height="225" fill="url(#grid-{project_id})"/>
  <circle cx="360" cy="20" r="70" fill="#fff" opacity=".05"/>
  <circle cx="20" cy="205" r="90" fill="#000" opacity=".08"/>{scene}
</svg>"""


def project_publication_illustration(project_id: str) -> str:
    """Stable project art consumed by the accepted PDF/EPUB appendix.

    The web redesign may evolve independently, but the closed publication
    contract continues to receive the exact pre-redesign illustration bytes.
    """
    c1, c2 = PROJECT_ACCENTS.get(project_id, ("var(--navy-900)", "var(--violet-500)"))
    icon = _project_icon_svg(project_id)
    return f"""<svg viewBox="0 0 400 225" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="grad-{project_id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="225" fill="url(#grad-{project_id})"/>
  <circle cx="360" cy="20" r="70" fill="#fff" opacity=".05"/>
  <circle cx="20" cy="205" r="90" fill="#000" opacity=".08"/>
{icon}
</svg>"""


def reference_illustration() -> str:
    """Decorative handbook/index map for the homepage reference section."""
    return """<svg class="reference-art" viewBox="0 0 620 390" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="reference-bg" x1=".08" y1="0" x2=".92" y2="1">
      <stop offset="0" stop-color="#171044"/><stop offset="1" stop-color="#09021f"/>
    </linearGradient>
    <linearGradient id="reference-page" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dfe8ff"/>
    </linearGradient>
    <pattern id="reference-grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#8fb7fe" stroke-width=".7" opacity=".13"/>
    </pattern>
    <filter id="reference-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="620" height="390" rx="30" fill="url(#reference-bg)"/>
  <rect width="620" height="390" rx="30" fill="url(#reference-grid)"/>
  <path d="M73 307C151 252 170 275 235 231S361 173 443 214 531 165 565 103" fill="none" stroke="#8fb7fe" stroke-width="1.5" stroke-dasharray="4 10" opacity=".34"/>
  <g class="reference-art__book">
    <path d="M176 118q0-18 18-18h96q29 0 39 19v170q-12-18-39-18h-114z" fill="url(#reference-page)"/>
    <path d="M484 118q0-18-18-18h-96q-29 0-39 19v170q12-18 39-18h114z" fill="#eef2ff"/>
    <path d="M330 119v170" fill="none" stroke="#b9a0fc" stroke-width="3" opacity=".85"/>
    <g fill="#3d72ff" opacity=".4"><rect x="204" y="141" width="89" height="7" rx="3.5"/><rect x="204" y="161" width="70" height="7" rx="3.5"/><rect x="204" y="181" width="84" height="7" rx="3.5"/></g>
    <g fill="#5b24f9" opacity=".35"><rect x="369" y="141" width="84" height="7" rx="3.5"/><rect x="369" y="161" width="63" height="7" rx="3.5"/><rect x="369" y="181" width="78" height="7" rx="3.5"/></g>
    <path d="M390 218l15 13 28-34" fill="none" stroke="#5b24f9" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g class="reference-art__search" filter="url(#reference-glow)">
    <circle cx="481" cy="88" r="41" fill="#171044" stroke="#8fb7fe" stroke-width="6"/><path d="M510 117l36 36" stroke="#8fb7fe" stroke-width="10" stroke-linecap="round"/>
  </g>
  <g class="reference-art__code" fill="none" stroke="#b9a0fc" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M96 153l-18 17 18 17M129 153l18 17-18 17M119 140l-13 60"/>
  </g>
  <g class="reference-art__nodes" fill="#09021f" stroke="#8fb7fe" stroke-width="2">
    <circle cx="73" cy="307" r="6"/><circle cx="235" cy="231" r="6"/><circle cx="443" cy="214" r="6"/><circle cx="565" cy="103" r="6"/>
  </g>
  <text x="48" y="52" fill="#8fb7fe" opacity=".62" font-family="JetBrains Mono, monospace" font-size="11" letter-spacing="2">УКАЗАТЕЛЬ / КАРТА ЗНАНИЙ</text>
</svg>"""


def project_card(entry: dict) -> str:
    """Colorful homepage Projects catalog card for one manifest['projects'] entry."""
    slug = entry["slug"]
    topics_html = "".join(f'<span class="project-topic">{html.escape(t)}</span>' for t in entry.get("topics", []))
    return f"""
    <a class="project-card" data-project="{html.escape(entry['id'])}" href="/projects/{slug}/">
      <div class="project-card-visual">{project_illustration(entry["id"])}</div>
      <div class="project-card-body">
        <h3 class="project-card-title">{html.escape(entry["title"])}</h3>
        <p class="project-card-desc">{html.escape(entry["description"])}</p>
        <div class="project-card-topics">{topics_html}</div>
        <span class="project-card-cta">Открыть проект <span aria-hidden="true">→</span></span>
      </div>
    </a>"""
