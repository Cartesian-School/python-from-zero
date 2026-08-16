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
