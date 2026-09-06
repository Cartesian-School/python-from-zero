#!/usr/bin/env python3
"""Builds the Polish homepage (site/pl/index.html).

Deliberately independent of build_site_index.py (no import) so this
script never re-triggers that RU builder's own file-write side effect
and never risks RU/PL builder coupling — it reloads the same underlying
manifests directly. Canonical PL prose lives in
manifest/i18n/content/pl/home.json (a single canonical source file for
the whole route, matching the one-source_path-per-variant route schema).

Scope (M02-I03, shell/catalog only): the 24 chapter titles, practice
group titles/counts, project catalog titles/descriptions, and Kompendium
card copy are catalog metadata, translated here. Chapter lesson bodies,
individual exercise bodies and full project tutorial bodies are NOT
translated — roadmap cards, practice groups and project cards render as
non-interactive (aria-disabled) until that content exists and is
reviewed, per the "no misleading cross-language navigation" contract.

The elaborate homepage author-bio panel (portrait, affiliations,
metadata strip — RU id="avtor") is intentionally omitted here: it isn't
reachable from top navigation, isn't part of the task's PL shell
sections (hero/O kursie/Rozdziały/Praktyka/Projekty/Kompendium), and
skipping it avoids re-translating biographical prose beyond what the
dedicated front-matter-author PL page already covers faithfully.
"""

import html
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_pagination import total_pages
from chapter_metadata import chapters
from localization import Routes, load_pl_content, polish_count
from site_lib import (
    NAV_SCRIPT_TAG,
    _render_icon_markers,
    disabled_card_attrs,
    mobile_nav_links,
    practice_illustration,
    project_illustration,
    reference_illustration,
    site_footer,
    site_header,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "pl" / "index.html"

PRACTICE = json.loads((ROOT / "manifest" / "practice_manifest.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8"))["projects"]

HOME = load_pl_content(
    "home",
    required_keys=("counters", "chapter_titles", "topic_translations", "projects_catalog",
                    "hero", "about", "format", "roadmap", "practice", "projects", "reference"),
)
CHAPTER_TITLES_PL = HOME["chapter_titles"]
PROJECTS_PL = HOME["projects_catalog"]
TOPIC_TRANSLATIONS = HOME["topic_translations"]

CHAPTERS = chapters()

lessons_by_chapter: dict[int, list[tuple[str, dict]]] = defaultdict(list)
for lesson_id, entry in PRACTICE.items():
    lessons_by_chapter[int(lesson_id.split("-")[0])].append((lesson_id, entry))
for lst in lessons_by_chapter.values():
    lst.sort(key=lambda pair: pair[0])


def mode_of(entry: dict) -> str:
    backend = entry.get("backend")
    if backend == "browser-pyodide":
        return "browser"
    if backend == "browser-adapted":
        return "adapted"
    return "local"


TOTAL_LESSONS = len(PRACTICE)
TOTAL_PROJECTS = len(PROJECTS)
TOTAL_PAGES = total_pages()
TOTAL_CHAPTERS = len(CHAPTERS)
BROWSER_COUNT = sum(1 for e in PRACTICE.values() if mode_of(e) == "browser")
LOCAL_COUNT = sum(1 for e in PRACTICE.values() if mode_of(e) == "local")
CHAPTERS_WITH_PRACTICE = sum(1 for chapter in CHAPTERS if lessons_by_chapter.get(chapter.number))

# Context-specific declension forms (bare-noun forms live in
# manifest/i18n/pl_terminology.json / content JSON where they're reused
# across pages; these two are homepage-hero-specific phrasings and are
# only used once each, mirroring how build_site_index.py itself keeps
# MODE_LABELS as a local Python constant rather than shared data).
CHAPTERS_PHRASE_FORMS = ("rozdział", "rozdziały", "rozdziałów")
PROJECTS_PHRASE_FORMS = ("gotowy mini-projekt", "gotowe mini-projekty", "gotowych mini-projektów")

CHAPTERS_PHRASE = polish_count(TOTAL_CHAPTERS, CHAPTERS_PHRASE_FORMS)
LESSONS_PHRASE = polish_count(TOTAL_LESSONS, HOME["counters"]["exercises_forms"])
PROJECTS_PHRASE = polish_count(TOTAL_PROJECTS, PROJECTS_PHRASE_FORMS)


def chapter_title_pl(number: int) -> str:
    return html.escape(CHAPTER_TITLES_PL[str(number)])


# ---------------------------------------------------------------------------
# Rozdziały — roadmap (visual only; deep links disabled until translated)
# ---------------------------------------------------------------------------
def build_roadmap() -> str:
    roadmap = HOME["roadmap"]
    nodes = []
    for chapter in CHAPTERS:
        num = chapter.number
        entries = lessons_by_chapter.get(num, [])
        meta = (polish_count(len(entries), roadmap["practice_forms"])
                if entries else roadmap["no_practice_label"])
        card_body = f"""<div class="jn-card-top" data-module="{(num - 1) % 4}">
          <span class="jn-num">Rozdział {num}</span>
          <span class="jn-part" aria-hidden="true">CS / {num:02d}</span>
        </div>
        <div class="jn-title">{chapter_title_pl(num)}</div>"""
        if entries:
            card_body += '\n        <div class="jn-progress-track"><div class="jn-progress-fill"></div></div>'
        card_body += f"""
        <div class="jn-meta">{meta}</div>
        <span class="jn-state-badge"></span>"""
        nodes.append(f"""
    <div class="journey-node" data-chapter="{num}">
      <svg class="jn-route" viewBox="0 0 82 180" preserveAspectRatio="none" aria-hidden="true">
        <path class="jn-route-base" d="M0 0V72H38V90H82M0 180V108H26V102H82" />
        <path class="jn-route-secondary" d="M8 0V60H50V78H82M8 180V120H50V114H82" />
        <path class="pcb-packet" pathLength="100" d="M0 0V72H38V90H76V102H26V108H0V180" />
        <circle class="jn-via" cx="38" cy="72" r="3" />
        <circle class="jn-via" cx="26" cy="108" r="3" />
      </svg>
      <div class="jn-dot" aria-hidden="true"></div>
      <span class="jn-card" {disabled_card_attrs("pl")}>
        <span class="jn-pins" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        <span class="jn-pads" aria-hidden="true"><i></i><i></i><i></i></span>
        {card_body}
      </span>
    </div>""")
    return "".join(nodes)


# ---------------------------------------------------------------------------
# Praktyka — group summaries only (no per-lesson catalog: see module docstring)
# ---------------------------------------------------------------------------
def build_practice_catalog() -> str:
    roadmap = HOME["roadmap"]
    groups = []
    for chapter in CHAPTERS:
        num = chapter.number
        entries = lessons_by_chapter.get(num, [])
        meta = polish_count(len(entries), roadmap["practice_forms"])
        groups.append(f"""
    <div class="practice-chapter-group" data-chapter="{num}" {disabled_card_attrs("pl")}>
      <div class="pcg-summary">
        <span class="pcg-num" aria-hidden="true">{num:02d}</span>
        <div class="pcg-heading">
          <div class="pcg-title-row">
            <div class="pcg-title">Rozdział {num} · {chapter_title_pl(num)}</div>
          </div>
          <div class="pcg-meta">{meta}</div>
        </div>
      </div>
    </div>""")
    return "".join(groups)


# ---------------------------------------------------------------------------
# Projekty — disabled catalog cards (deep links unavailable until translated)
# ---------------------------------------------------------------------------
def build_projects_grid() -> str:
    cards = []
    for entry in PROJECTS:
        pid = entry["id"]
        copy = PROJECTS_PL[pid]
        topics_html = "".join(
            f'<span class="project-topic">{html.escape(TOPIC_TRANSLATIONS.get(t, t))}</span>'
            for t in entry.get("topics", [])
        )
        cards.append(f"""
    <div class="project-card" data-project="{html.escape(pid)}" {disabled_card_attrs("pl")}>
      <div class="project-card-visual">{project_illustration(pid, "pl")}</div>
      <div class="project-card-body">
        <h3 class="project-card-title">{html.escape(copy["title"])}</h3>
        <p class="project-card-desc">{html.escape(copy["description"])}</p>
        <div class="project-card-topics">{topics_html}</div>
        <span class="project-card-cta">{html.escape(HOME["projects"]["cta_unavailable"])}</span>
      </div>
    </div>""")
    return "".join(cards)


ROADMAP_HTML = build_roadmap()
PRACTICE_CATALOG_HTML = build_practice_catalog()
PROJECTS_GRID_HTML = build_projects_grid()

HERO = HOME["hero"]
ABOUT = HOME["about"]
FORMAT = HOME["format"]
ROADMAP = HOME["roadmap"]
PRACTICE_COPY = HOME["practice"]
PROJECTS_COPY = HOME["projects"]
REFERENCE = HOME["reference"]

HERO_LEDE = HERO["lede"].format(chapters_phrase=CHAPTERS_PHRASE, lessons_phrase=LESSONS_PHRASE, projects_phrase=PROJECTS_PHRASE)
ABOUT_PARAGRAPHS = "".join(
    f"<p>{p.format(chapters_phrase=CHAPTERS_PHRASE, lessons_phrase=LESSONS_PHRASE, projects_phrase=PROJECTS_PHRASE)}</p>"
    for p in ABOUT["paragraphs"]
)
ABOUT_HIGHLIGHTS = "".join(
    f'<li><span class="about-highlight__mark" aria-hidden="true">{i:02d}</span><span>{html.escape(h)}</span></li>'
    for i, h in enumerate(ABOUT["highlights"], start=1)
)

FORMAT_STAGES_HTML = "".join(f"""
        <li class="course-stage">
          <span class="course-stage__node" aria-hidden="true"><i></i></span>
          <article class="course-stage__content">
            <div class="course-stage__meta"><span>{s["meta_num"]}</span><span>{html.escape(s["meta_label"])}</span></div>
            <h3>{html.escape(s["title"])}</h3>
            <p>{html.escape(s["body"])}</p>
            <span class="course-stage__output">{html.escape(s["output"])}</span>
          </article>
        </li>""" for s in FORMAT["stages"])

PRACTICE_SUB = PRACTICE_COPY["sub"].format(lessons_phrase=LESSONS_PHRASE, chapters_with_practice=CHAPTERS_WITH_PRACTICE)

REFERENCE_CARDS = REFERENCE["cards"]

# Percent-encoded "готовая книга.pdf" — matches build_pdf.py's OUT filename.
PDF_HREF = "/book/pdf/%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BA%D0%BD%D0%B8%D0%B3%D0%B0.pdf"


def reference_card(key: str, href: str | None, icon: str, arrow: str = "→") -> str:
    copy = REFERENCE_CARDS[key]
    title = html.escape(copy["title"])
    desc = html.escape(copy["description"])
    inner = (
        f'<span class="ri">[[icon:{icon}]]</span>'
        f'<div class="reference-card__copy"><div class="rt">{title}</div><div class="rs">{desc}</div></div>'
        f'<span class="reference-card__arrow" aria-hidden="true">{arrow}</span>'
    )
    if href:
        extra_class = " reference-card--license" if key == "license" else ""
        return f'<a class="reference-card{extra_class}" href="{href}">{inner}</a>'
    return f'<span class="reference-card" {disabled_card_attrs("pl")}>{inner}</span>'


REFERENCE_BOARD_HTML = "".join([
    reference_card("index", None, "note"),
    reference_card("introduction", None, "note"),
    reference_card("author", "/pl/front-matter/o-autorze.html", "profile"),
    reference_card("technical_reviewer", None, "search"),
    reference_card("cli", None, "code"),
    reference_card("official_resources", None, "folder"),
    reference_card("pdf", PDF_HREF, "file", arrow="↓"),
    reference_card("epub", "/book/epub/python-s-nulya.epub", "device", arrow="↓"),
    reference_card("license", "/pl/front-matter/licencja.html", "license"),
])

HTML = _render_icon_markers(f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(HERO["h1"])} — Cartesian School</title>
<meta name="description" content="{html.escape(HERO_LEDE)}" />
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/theory.css" />
<link rel="stylesheet" href="/assets/css/homepage.css" />
<link rel="stylesheet" href="/assets/css/localization.css" />
</head>
<body>

{site_header("o-kurse", page_id="home", locale="pl", routes=Routes())}
<nav class="mobile-nav-panel" id="mobile-nav-panel">
  {mobile_nav_links("o-kurse", page_id="home", locale="pl", routes=Routes())}
</nav>

<section class="home-hero" aria-labelledby="course-hero-title">
  <div class="home-hero__inner">
    <div class="home-hero__content">
      <div class="kicker">
        <img src="/assets/img/brand/python-logo-mark.svg" width="25" height="30" alt="" aria-hidden="true" />
        <span>{html.escape(HERO["kicker"])}</span>
      </div>
      <h1 id="course-hero-title">{html.escape(HERO["h1"])}</h1>
      <p>{HERO_LEDE}</p>
      <div class="home-cta">
        <a class="btn btn-primary" href="#glavy">{html.escape(HERO["cta_primary"])}</a>
        <a class="btn btn-ghost" href="#o-kurse">{html.escape(HERO["cta_secondary"])}</a>
      </div>
    </div>

    <div class="hero-system" aria-hidden="true">
      <div class="hero-system__grid"></div>
      <div class="hero-system__backdrop">
        <span class="hero-system__prompt">&gt;&gt;&gt;</span>
        <span class="hero-token hero-token--def">def</span>
        <span class="hero-token hero-token--py">.py</span>
        <span class="hero-token hero-token--range">range()</span>
        <span class="hero-token hero-token--lambda">lambda</span>
      </div>

      <div class="hero-system__plane">
        <svg class="hero-connectors hero-connectors--desktop" viewBox="0 0 620 520" preserveAspectRatio="none">
          <g class="hero-axes">
            <path d="M50 466H585" />
            <path d="M50 466V54" />
            <path d="M578 461L585 466L578 471" />
            <path d="M45 61L50 54L55 61" />
            <text x="589" y="471">x</text>
            <text x="43" y="45">y</text>
          </g>
          <g class="hero-connector-lines">
            <path id="hero-route-code" d="M310 244V164H353" />
            <path id="hero-route-graph" d="M310 244H260V154" />
            <path id="hero-route-app" d="M310 244H440V343" />
            <path id="hero-route-game" d="M310 244H180V353" />
          </g>
          <g class="hero-connector-signals">
            <path class="hero-signal hero-signal--code" d="M310 244V164H353" />
            <path class="hero-signal hero-signal--graph" d="M310 244H260V154" />
            <path class="hero-signal hero-signal--app" d="M310 244H440V343" />
            <path class="hero-signal hero-signal--game" d="M310 244H180V353" />
          </g>
          <g class="hero-route-nodes">
            <circle cx="310" cy="164" r="4" />
            <circle cx="260" cy="244" r="4" />
            <circle cx="440" cy="244" r="4" />
            <circle cx="180" cy="244" r="4" />
          </g>
        </svg>

        <svg class="hero-connectors hero-connectors--mobile" viewBox="0 0 360 430" preserveAspectRatio="none">
          <g class="hero-axes">
            <path d="M18 302H344" />
            <path d="M18 302V24" />
            <text x="347" y="307">x</text>
            <text x="12" y="18">y</text>
          </g>
          <g class="hero-connector-lines">
            <path d="M180 194V130" />
            <path d="M180 194H295V145" />
            <path d="M180 194H85V322" />
            <path d="M180 194H275V322" />
          </g>
          <g class="hero-route-nodes">
            <circle cx="180" cy="130" r="4" />
            <circle cx="295" cy="194" r="4" />
            <circle cx="85" cy="194" r="4" />
            <circle cx="275" cy="194" r="4" />
          </g>
        </svg>

        <div class="hero-core">
          <span class="hero-core__orbit"></span>
          <span class="hero-core__mark"><img src="/assets/img/brand/python-logo-mark.svg" width="40" height="48" alt="" /></span>
          <span class="hero-core__name">Python</span>
          <span class="hero-core__runtime">runtime 3.14</span>
        </div>

        <div class="hero-module hero-module--code">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>Code</span>
            <span>square.py</span>
          </div>
          <pre><span class="syntax-prompt">&gt;&gt;&gt;</span> <span class="syntax-keyword">def</span> square(x):
<span class="syntax-prompt">...</span>     <span class="syntax-keyword">return</span> x ** 2
<span class="syntax-prompt">&gt;&gt;&gt;</span> square(5)
<span class="syntax-result">25</span><span class="hero-code-cursor">▌</span></pre>
        </div>

        <div class="hero-module hero-module--graph">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>Graph</span>
            <span>f(x)</span>
          </div>
          <svg class="hero-plot" viewBox="0 0 210 94">
            <g class="hero-plot__grid">
              <path d="M8 16H204M8 39H204M8 62H204M8 85H204M32 7V88M76 7V88M120 7V88M164 7V88" />
            </g>
            <path class="hero-plot__axis" d="M8 80H204M22 88V7" />
            <path class="hero-plot__curve" d="M9 69C40 67 49 18 82 23C111 27 119 72 146 67C168 63 177 29 203 16" />
            <path class="hero-plot__vector" d="M111 53L146 36M139 35L146 36L143 43" />
            <circle class="hero-plot__point hero-plot__point--a" cx="82" cy="23" r="3.5" />
            <circle class="hero-plot__point hero-plot__point--b" cx="146" cy="67" r="3.5" />
          </svg>
        </div>

        <div class="hero-module hero-module--app">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>App</span>
            <span class="hero-app-status"><b></b>running</span>
          </div>
          <div class="hero-app-ui">
            <div class="hero-app-ui__chart">
              <span style="--bar: .42"></span><span style="--bar: .72"></span><span style="--bar: .56"></span><span style="--bar: .88"></span>
            </div>
            <div class="hero-app-ui__panel">
              <span></span><span></span><b>run()</b>
            </div>
          </div>
        </div>

        <div class="hero-module hero-module--game">
          <div class="hero-module__head">
            <span class="hero-module__label"><i></i>Game</span>
            <span>score 0250</span>
          </div>
          <svg class="hero-game" viewBox="0 0 210 76">
            <path class="hero-game__trajectory" d="M18 58H72V38H126V18H190" />
            <g class="hero-game__target"><circle cx="181" cy="18" r="10" /><circle cx="181" cy="18" r="3" /></g>
            <g class="hero-game__sprite"><path d="M35 51L53 58L35 65L39 58Z" /><path d="M31 55H20M31 61H25" /></g>
            <rect class="hero-game__collision" x="126" y="47" width="24" height="18" rx="2" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="course-experience" aria-label="{html.escape(ABOUT["heading"])}">
  <div class="course-experience__geometry" aria-hidden="true">
    <span class="course-experience__axis course-experience__axis--x"></span>
    <span class="course-experience__axis course-experience__axis--y"></span>
    <span class="course-experience__point course-experience__point--a"></span>
    <span class="course-experience__point course-experience__point--b"></span>
    <span class="course-experience__point course-experience__point--c"></span>
  </div>

  <div class="home-section course-overview" id="o-kurse">
    <div class="course-section-heading experience-reveal">
      <div class="kicker-label">{html.escape(ABOUT["kicker_label"])}</div>
      <h2>{html.escape(ABOUT["heading"])}</h2>
      <p class="course-section-lead">{html.escape(ABOUT["lead"])}</p>
    </div>

    <div class="about-grid">
      <div class="about-copy experience-reveal">
        {ABOUT_PARAGRAPHS}
        <ul class="about-highlights" aria-label="{html.escape(ABOUT["heading"])}">
          {ABOUT_HIGHLIGHTS}
        </ul>
      </div>

      <div class="about-stats experience-reveal" aria-label="{html.escape(ABOUT["heading"])}">
        <svg class="about-stats__routes" viewBox="0 0 600 430" preserveAspectRatio="none" aria-hidden="true">
          <path class="about-stats__route" d="M48 184H202V113H358" />
          <path class="about-stats__route" d="M202 184V315H338" />
          <path class="about-stats__route" d="M338 315H534V242" />
          <path class="about-stats__signal" d="M48 184H202V113H358" />
          <circle cx="202" cy="184" r="4" />
          <circle cx="202" cy="113" r="4" />
          <circle cx="338" cy="315" r="4" />
        </svg>

        <div class="about-stat about-stat--chapters">
          <span class="about-stat__code">CURRICULUM / 01</span>
          <div class="about-stat__number-zone"><div class="num">{TOTAL_CHAPTERS}</div></div>
          <div class="about-stat__copy">
            <div class="lbl">{html.escape(ABOUT["stats"]["chapters_label"])}</div>
            <span class="about-stat__detail">{html.escape(ABOUT["stats"]["chapters_detail"])}</span>
          </div>
        </div>
        <div class="about-stat about-stat--pages">
          <span class="about-stat__code">BOOK / PDF</span>
          <div class="about-stat__number-zone"><div class="num">{TOTAL_PAGES}</div></div>
          <div class="about-stat__copy"><div class="lbl">{html.escape(ABOUT["stats"]["pages_label"])}</div></div>
        </div>
        <div class="about-stat about-stat--projects">
          <span class="about-stat__code">BUILD / SHIP</span>
          <div class="about-stat__number-zone"><div class="num">{TOTAL_PROJECTS}</div></div>
          <div class="about-stat__copy"><div class="lbl">{html.escape(ABOUT["stats"]["projects_label"])}</div></div>
        </div>
        <div class="about-stat about-stat--practice">
          <span class="about-stat__code">REPL / PRACTICE</span>
          <div class="about-stat__number-zone"><div class="num">{TOTAL_LESSONS}</div></div>
          <div class="about-stat__copy">
            <div class="lbl">{html.escape(ABOUT["stats"]["practice_label"])}</div>
            <span class="about-stat__detail">{html.escape(ABOUT["stats"]["practice_detail"])}</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="course-experience__bridge" aria-hidden="true"><span></span></div>

  <div class="home-section course-format" aria-labelledby="course-format-title">
    <div class="course-section-heading experience-reveal">
      <div class="kicker-label">{html.escape(FORMAT["kicker_label"])}</div>
      <h2 id="course-format-title">{html.escape(FORMAT["heading"])}</h2>
      <p class="sub">{html.escape(FORMAT["sub"])}</p>
    </div>

    <div class="course-path experience-reveal" aria-label="{html.escape(FORMAT["heading"])}">
      <svg class="course-path__rail course-path__rail--desktop" viewBox="0 0 1120 108" preserveAspectRatio="none" aria-hidden="true">
        <path class="course-path__base" d="M70 54H1050" />
        <path class="course-path__segment course-path__segment--1" d="M70 54H315" />
        <path class="course-path__segment course-path__segment--2" d="M315 54H560" />
        <path class="course-path__segment course-path__segment--3" d="M560 54H805" />
        <path class="course-path__segment course-path__segment--4" d="M805 54H1050" />
        <path class="course-path__signal" d="M70 54H1050" />
      </svg>
      <svg class="course-path__rail course-path__rail--mobile" viewBox="0 0 52 760" preserveAspectRatio="none" aria-hidden="true">
        <path class="course-path__base" d="M26 34V726" />
        <path class="course-path__signal" d="M26 34V726" />
      </svg>

      <ol class="course-path__stages">{FORMAT_STAGES_HTML}
      </ol>
    </div>
  </div>
</section>

<div class="home-section panel-canvas" id="glavy">
  <div class="kicker-label">{html.escape(ROADMAP["kicker_label"])}</div>
  <h2>{html.escape(ROADMAP["heading"])}</h2>
  <p class="sub">{html.escape(ROADMAP["sub"])}</p>
  <p class="sub">{html.escape(ROADMAP["note"])}</p>

  <div class="pcb-board">
    <svg class="pcb-surface" width="100%" height="100%" aria-hidden="true">
      <defs>
        <pattern id="pcb-routing" width="960" height="680" patternUnits="userSpaceOnUse">
          <g class="pcb-traces">
            <path d="M18 0V110H126V162H218M30 0V98H138V150H230M42 0V86H150V138H242" />
            <path d="M960 38H864V190H752V248H680M960 50H876V202H764V260H692M960 62H888V214H776V272H704" />
            <path d="M0 350H84V278H196V236H284M0 362H96V290H208V248H296M0 374H108V302H220V260H308" />
            <path d="M960 450H842V388H738V350H654M960 462H830V400H726V362H642M960 474H818V412H714V374H630" />
            <path d="M54 680V562H152V514H234M66 680V574H164V526H246M78 680V586H176V538H258" />
            <path d="M908 680V580H780V540H694M896 680V592H768V552H682M884 680V604H756V564H670" />
          </g>
          <g class="pcb-vias">
            {"".join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x,y in [(218,162),(230,150),(242,138),(680,248),(692,260),(704,272),(284,236),(296,248),(308,260),(654,350),(642,362),(630,374),(234,514),(246,526),(258,538),(694,540),(682,552),(670,564),(84,350),(842,450),(152,562),(864,190),(126,110),(780,580)])}
          </g>
          <g class="pcb-components">
            <path d="M340 78h52v34h-52zM350 70v8m12-8v8m12-8v8m12-8v8m-36 34v8m12-8v8m12-8v8m12-8v8M328 90h12m52 0h12M328 102h12m52 0h12" />
            <path d="M592 478h40v52h-40zM584 488h8m-8 12h8m-8 12h8m40-24h8m-8 12h8m-8 12h8" />
            <path d="M108 432h16m0-6h22v12h-22zM146 432h16M780 108h16m0-6h22v12h-22zM818 108h16M364 566h20m0-9v18m8-18v18m0-9h20" />
            <rect x="302" y="382" width="48" height="22" rx="3" />
            <path d="M312 388v10m10-10v10m10-10v10m10-10v10" />
          </g>
          <g class="pcb-silkscreen"><text x="338" y="62">IO</text><text x="592" y="464">BUS-B</text><text x="108" y="420">R02</text><text x="300" y="370">CS-24</text></g>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#pcb-routing)" />
    </svg>
  <div class="journey-rail"><div class="pcb-bus" aria-hidden="true"><i></i><i></i><i></i></div>{ROADMAP_HTML}
  </div>
  </div>
</div>

<div class="home-section panel-surface" id="praktika">
  <div class="practice-hero">
    <div class="practice-hero__copy">
      <div class="kicker-label">{html.escape(PRACTICE_COPY["kicker_label"])}</div>
      <h2>{html.escape(PRACTICE_COPY["heading"])}</h2>
      <p class="sub">{PRACTICE_SUB}</p>

      <div class="practice-summary">
        <span class="practice-stat-chip"><strong>{BROWSER_COUNT}</strong> {html.escape(PRACTICE_COPY["summary_browser"])}</span>
        <span class="practice-stat-chip"><strong>{LOCAL_COUNT}</strong> {html.escape(PRACTICE_COPY["summary_local"])}</span>
        <span class="practice-stat-chip"><strong>{TOTAL_LESSONS}</strong> {html.escape(PRACTICE_COPY["summary_total"])}</span>
      </div>

      <div class="practice-filters" role="group" aria-label="{html.escape(PRACTICE_COPY["heading"])}">
        <span class="pf-btn active" {disabled_card_attrs("pl")}>{html.escape(PRACTICE_COPY["filters"]["all"])}</span>
        <span class="pf-btn" {disabled_card_attrs("pl")}>{html.escape(PRACTICE_COPY["filters"]["browser"])}</span>
        <span class="pf-btn" {disabled_card_attrs("pl")}>{html.escape(PRACTICE_COPY["filters"]["local"])}</span>
      </div>
      <p class="sub">{html.escape(PRACTICE_COPY["note"])}</p>
    </div>
    <div class="practice-hero__art">{practice_illustration("pl")}</div>
  </div>

{PRACTICE_CATALOG_HTML}
</div>

<div class="home-section panel-canvas" id="proekty">
  <div class="kicker-label">{html.escape(PROJECTS_COPY["kicker_label"])}</div>
  <h2>{html.escape(PROJECTS_COPY["heading"])}</h2>
  <p class="sub">{html.escape(PROJECTS_COPY["sub"])}</p>
  <div class="projects-grid">{PROJECTS_GRID_HTML}</div>
</div>

<div class="home-section panel-surface" id="spravochnik">
  <div class="reference-hero">
    <div class="reference-hero__copy">
      <div class="kicker-label">{html.escape(REFERENCE["kicker_label"])}</div>
      <h2>{html.escape(REFERENCE["heading"])}</h2>
      <p class="sub">{html.escape(REFERENCE["sub"])}</p>
      <p class="reference-hero__note">{html.escape(REFERENCE["note"])}</p>
    </div>
    <div class="reference-hero__art">{reference_illustration("pl")}</div>
  </div>
  <div class="reference-board">{REFERENCE_BOARD_HTML}</div>
</div>

{site_footer("pl", Routes())}

{NAV_SCRIPT_TAG}
<script src="/assets/js/hero.js" defer></script>
<script src="/assets/js/experience.js" defer></script>
<script src="/assets/js/progress.js" defer></script>
</body>
</html>
""")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print(f"Zapisano: {OUT.relative_to(ROOT)}")
