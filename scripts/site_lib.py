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
    except (tokenize.TokenizeError, IndentationError, SyntaxError):
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


def flow_diagram(steps: list[tuple[str, str]], *, caption: str = "") -> str:
    """Горизонтальная диаграмма-цепочка шагов (оригинальная, не скриншот).

    steps: список (заголовок, подпись) для каждого прямоугольника.
    """
    n = len(steps)
    box_w, box_h, gap = 176, 92, 56
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
    for i, (title, sub) in enumerate(steps):
        x = i * (box_w + gap)
        y = 10
        parts.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="14" '
            f'fill="#FAFAFC" stroke="#5B24F9" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{x + box_w / 2}" y="{y + box_h / 2 - 6}" text-anchor="middle" '
            f'font-family="Sora, sans-serif" font-weight="700" font-size="15" fill="#0D0230">'
            f'{html.escape(title)}</text>'
        )
        parts.append(
            f'<text x="{x + box_w / 2}" y="{y + box_h / 2 + 16}" text-anchor="middle" '
            f'font-family="Inter, sans-serif" font-size="12" fill="#6B6B7D">'
            f'{html.escape(sub)}</text>'
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
) -> str:
    """depth: how many '../' needed to reach site/ root from this file's folder."""
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

<header class="site-header">
  <div class="brand">
    <img src="{root}assets/img/logo.png" alt="Cartesian School" />
    <span class="brand-word">Cartesian<span class="school">School</span></span>
  </div>
  <ul class="top-nav">
    <li><a href="{root}index.html">О курсе</a></li>
    <li><a href="{root}index.html#glavy" class="active">Главы</a></li>
    <li><a href="{root}index.html#praktika">Практика</a></li>
    <li><a href="{root}index.html#proekty">Проекты</a></li>
    <li><a href="{root}index.html#spravochnik">Справочник</a></li>
  </ul>
  <button class="nav-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">☰ Оглавление</button>
</header>

<div class="layout">
  <nav class="sidebar">
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

<header class="site-header">
  <div class="brand">
    <img src="{root}assets/img/logo.png" alt="Cartesian School" />
    <span class="brand-word">Cartesian<span class="school">School</span></span>
  </div>
  <ul class="top-nav">
    <li><a href="{root}index.html">О курсе</a></li>
    <li><a href="{root}index.html#glavy" class="active">Главы</a></li>
    <li><a href="{root}index.html#praktika">Практика</a></li>
    <li><a href="{root}index.html#proekty">Проекты</a></li>
    <li><a href="{root}index.html#spravochnik">Справочник</a></li>
  </ul>
</header>

<div class="chapter-hero">
  <div class="chapter-hero-inner">
    <div class="chapter-num">ГЛАВА {chapter_num} · СТР. {baseline_page}</div>
    <h1>{html.escape(title)}</h1>
    <p>{description}</p>
    <div class="chapter-meta">{meta_html}</div>
  </div>
</div>

<div class="section-list">
  {rows}
</div>

</body>
</html>
"""
