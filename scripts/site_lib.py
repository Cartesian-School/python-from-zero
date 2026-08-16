"""Переиспользуемый генератор HTML-страниц теории Cartesian School.

Строит страницы из структурированных данных (Python), используя те же CSS-классы,
что и в site/assets/css/theory.css (см. прототип site/chapters/glava-06/).
Не хранит контент — только рендеринг; текст пишется отдельно для каждого раздела.
"""

from __future__ import annotations

import html
import io
import keyword
import tokenize
from dataclasses import dataclass, field


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
    return f"""
    <div class="callout callout-{kind}">
      <div>
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
    return f"""
    <div class="exercise">
      <div class="exercise-stars">{_STARS[stars]}</div>
      <div class="exercise-title">{html.escape(title)}</div>
      <p>{body_html}</p>
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
            _wrap_svg_text(" ".join(sub.split()), max_chars=sub_max_chars, max_lines=sub_max_lines),
        )
        for title, sub in steps
    ]
    max_title_lines = max((len(t) for t, _ in wrapped), default=1)
    max_sub_lines = max((len(s) for _, s in wrapped), default=1)
    box_h = top_pad + max_title_lines * title_line_h + mid_gap + max_sub_lines * sub_line_h + bottom_pad

    total_w = n * box_w + (n - 1) * gap
    total_h = box_h + 40
    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
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
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="14" '
            f'fill="#FAFAFC" stroke="#5B24F9" stroke-width="1.5"/>'
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
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
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


def _wrap_svg_text(text: str, max_chars: int, max_lines: int = 3) -> list[str]:
    """Greedy word-wrap for SVG <text>, which never wraps on its own.

    Wraps the full text first (as many lines as it takes, each up to
    max_chars) and only afterwards truncates to max_lines with a trailing
    "…" if it still doesn't fit. Truncating the line count *before* the
    greedy pass finishes would cut off the last word or two of otherwise
    short text — this two-pass order keeps every word that legitimately
    fits within max_lines.
    """
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
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
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        f'<rect x="{root_x}" y="{root_top}" width="{root_w}" height="{root_h}" rx="14" '
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
    for i, (title, sub) in enumerate(branches):
        x = branches_x_offset + i * (box_w + gap)
        cx = x + box_w / 2
        parts.append(
            f'<path d="M{root_cx},{root_bottom} C{root_cx},{(root_bottom + branches_y) / 2} '
            f'{cx},{(root_bottom + branches_y) / 2} {cx},{branches_y}" '
            f'fill="none" stroke="#B9A0FC" stroke-width="2.5" marker-end="url(#arrow)"/>'
        )
        parts.append(
            f'<rect x="{x}" y="{branches_y}" width="{box_w}" height="{box_h}" rx="14" '
            f'fill="#FAFAFC" stroke="#5B24F9" stroke-width="1.5"/>'
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
    svg = f"""<svg viewBox="0 0 400 90" xmlns="http://www.w3.org/2000/svg" role="img"
      aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:400px">
      <defs><marker id="arrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
        orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#5B24F9"/></marker></defs>
      <text x="10" y="52" font-family="JetBrains Mono, monospace" font-weight="700" font-size="20" fill="#0D0230">{html.escape(name)}</text>
      <line x1="95" y1="45" x2="220" y2="45" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#arrow2)"/>
      <rect x="230" y="15" width="160" height="60" rx="12" fill="#FAFAFC" stroke="#5B24F9" stroke-width="1.5"/>
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
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
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
            f'<rect x="{box_x}" y="{y}" width="{box_w}" height="{box_h}" rx="12" '
            f'fill="#FAFAFC" stroke="#5B24F9" stroke-width="1.5"/>'
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
            f'<rect x="{box_x}" y="{y}" width="{box_w}" height="{box_h}" rx="12" '
            f'fill="none" stroke="#B9A0FC" stroke-width="1.5" stroke-dasharray="6,5"/>'
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
    jumps: optional list of (from, to, label) drawn as a curved arrow above
    the line — for addition/subtraction ("start at 3, move 4, arrive at 7")."""
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
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
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
            f'<path d="M{x1},{y - 8} Q{mid},{arc_h} {x2},{y - 8}" fill="none" '
            f'stroke="#5B24F9" stroke-width="2.5" marker-end="url(#arrownl)"/>'
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


def image_figure(src: str, alt: str, caption: str, *, width: int | None = None) -> str:
    """A real screenshot/photo, not a generated diagram — captioned figure."""
    width_attr = f' width="{width}"' if width else ""
    return f"""
    <figure style="margin:24px 0">
      <img src="{html.escape(src)}" alt="{html.escape(alt)}"{width_attr}
        style="width:100%;height:auto;border-radius:var(--radius-lg,20px);border:1px solid var(--color-border-default,#ddd);display:block" />
      <figcaption style="text-align:center;font-size:13px;color:var(--color-text-muted,#6B6B7D);margin-top:8px">{html.escape(caption)}</figcaption>
    </figure>"""


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
        f'role="img" aria-label="{html.escape(caption)}" style="width:100%;height:auto;max-width:{total_w}px">'
    ]
    parts.append(
        "<defs><marker id='arrowc' viewBox='0 0 10 10' refX='9' refY='5' "
        "markerWidth='6' markerHeight='6' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#B9A0FC'/></marker></defs>"
    )
    target_cx = total_w / 2
    for i, label in enumerate(sources):
        x = sources_x_offset + i * (box_w + gap)
        cx = x + box_w / 2
        parts.append(
            f'<rect x="{x}" y="{sources_y}" width="{box_w}" height="{box_h}" rx="12" '
            f'fill="#FAFAFC" stroke="#5B24F9" stroke-width="1.5"/>'
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
            f'<path d="M{cx},{sources_y + box_h} C{cx},{(sources_y + box_h + target_y) / 2} '
            f'{target_cx},{(sources_y + box_h + target_y) / 2} {target_cx},{target_y}" '
            f'fill="none" stroke="#B9A0FC" stroke-width="2.5" marker-end="url(#arrowc)"/>'
        )
    parts.append(
        f'<rect x="{target_x}" y="{target_y}" width="{target_w}" height="{target_h}" rx="14" fill="#5B24F9"/>'
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


def render_page(
    *,
    page_title: str,
    description: str,
    depth: int,
    breadcrumb: list[tuple[str, str]],
    kicker: str,
    h1: str,
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

    nav_html = '<div class="section-nav">'
    if nav.prev_href:
        nav_html += f'<a href="{html.escape(nav.prev_href)}"><div class="dir">← Назад</div><div class="lbl">{html.escape(nav.prev_label or "")}</div></a>'
    else:
        nav_html += "<div></div>"
    if nav.next_href:
        nav_html += f'<a href="{html.escape(nav.next_href)}" class="next"><div class="dir">Далее →</div><div class="lbl">{html.escape(nav.next_label or "")}</div></a>'
    nav_html += "</div>"

    return f"""<!DOCTYPE html>
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
    <div class="section-kicker">{html.escape(kicker)}</div>
    <h1>{html.escape(h1)}</h1>
    <p class="lede">{lede}</p>

{body_html}

    {nav_html}
  </article>
</div>

{NAV_SCRIPT_TAG}
</body>
</html>
"""


@dataclass
class ChapterSectionLink:
    num: str
    title: str
    href: str
    page: str


def render_chapter_opener(
    *,
    chapter_num: int,
    baseline_page: int,
    title: str,
    description: str,
    meta_items: list[str],
    sections: list[ChapterSectionLink],
    brand_html: str = "",
) -> str:
    root = "../../"
    meta_html = "".join(f"<span>{m}</span>" for m in meta_items)
    rows = "".join(
        f'<a class="section-item" href="{html.escape(s.href)}">'
        f'<span><span class="si-num">{html.escape(s.num)}</span>{html.escape(s.title)}</span>'
        f'<span class="si-page">{html.escape(s.page)}</span></a>'
        for s in sections
    )
    return f"""<!DOCTYPE html>
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
  .chapter-num {{ font-family: 'JetBrains Mono', monospace; color: var(--blue-300); font-size: 15px; margin-bottom: var(--spacing-sm); }}
  .chapter-hero h1 {{ color: white; font-size: 44px; max-width: 640px; }}
  .chapter-hero p {{ color: var(--gray-400); font-size: 18px; max-width: 560px; margin-top: var(--spacing-md); }}
  .chapter-meta {{ display: flex; gap: var(--spacing-xl); margin-top: var(--spacing-xl); font-size: 14px; color: var(--blue-300); flex-wrap: wrap; }}
  .section-list {{ max-width: 900px; margin: var(--spacing-2xl) auto; padding: 0 var(--spacing-2xl); }}
  .section-item {{ display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-md); border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin-bottom: var(--spacing-sm); text-decoration: none; color: var(--color-text-primary); }}
  .section-item:hover {{ border-color: var(--color-brand-blue); }}
  .section-item .si-num {{ font-family: 'JetBrains Mono', monospace; color: var(--color-text-muted); font-size: 13px; margin-right: var(--spacing-md); }}
  .section-item .si-page {{ font-family: 'JetBrains Mono', monospace; color: var(--color-text-muted); font-size: 13px; }}
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
    <div class="chapter-num">ГЛАВА {chapter_num} · СТР. {baseline_page}</div>
    <h1>{html.escape(title)}</h1>
    <p>{description}</p>
    <div class="chapter-meta">{meta_html}</div>
  </div>
</div>

<div class="section-list">
  {rows}
</div>

{NAV_SCRIPT_TAG}
</body>
</html>
"""


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


def project_illustration(project_id: str) -> str:
    """Self-contained 16:9 inline SVG illustration for one real project, used
    both on the homepage Projects card and the project's own detail page.
    Purely decorative (the card/page title carries the accessible name), so
    aria-hidden="true" — no meaningful alt text is lost.
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


def project_card(entry: dict) -> str:
    """Colorful homepage Projects catalog card for one manifest['projects'] entry."""
    slug = entry["slug"]
    topics_html = "".join(f'<span class="project-topic">{html.escape(t)}</span>' for t in entry.get("topics", []))
    return f"""
    <a class="project-card" href="/projects/{slug}/">
      <div class="project-card-visual">{project_illustration(entry["id"])}</div>
      <div class="project-card-body">
        <div class="project-card-title">{html.escape(entry["title"])}</div>
        <p class="project-card-desc">{html.escape(entry["description"])}</p>
        <div class="project-card-topics">{topics_html}</div>
        <span class="project-card-cta">Открыть проект →</span>
      </div>
    </a>"""
