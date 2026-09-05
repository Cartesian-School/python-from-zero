"""Canonical author-identity facts shared by the homepage author profile
(build_site_index.py) and the front-matter author page (build_front_matter.py)
— a single source of truth so the two surfaces can never silently diverge on
name, role, or core facts.

Only presentation-safe, already-verified material belongs here — everything
below was already published on the homepage author profile before this
module existed. Do not add claims that haven't been reviewed there first.
"""

from dataclasses import dataclass

NAME = "Siergej Sobolewski"
NAME_RU = "Сергей Соболевски"
ROLE = "Founder & CEO · Senior Systems & AI Engineer"

SPECIALIZATIONS = ["AI/ML", "Embedded Systems", "Radar & Avionics", "High-Assurance Engineering"]

BIO_LEAD = (
    "Более двух десятилетий инженерной практики — от embedded, radar и avionics "
    "до операционных систем, cloud-native инфраструктуры и production AI/ML."
)

BIO_PARAGRAPHS = [
    "Опыт охватывает low-level engineering, safety-critical разработку, включая "
    "инженерные практики и процессы DO-178C, embedded-системы, разработку "
    "операционных систем и инженерных платформ с контролируемыми границами отказа.",
    "В AI и инфраструктуре: RAG, IBM watsonx, Kubernetes, DevOps, observability и "
    "управляемые agentic-системы, где результат должен быть воспроизводимым и проверяемым.",
    "Автор GuardBSD, AstraDesk, AeroNerve, PySH, ECLI и Cartesian School Agency AI; "
    "пишет технические книги и создаёт образовательные программы для инженеров.",
]

PROJECTS = ["GuardBSD", "AstraDesk", "AeroNerve", "PySH", "ECLI", "Cartesian School Agency AI"]


@dataclass
class Domain:
    index: str
    title: str
    desc: str
    title_ru: str = ""
    desc_ru: str = ""
    wide: bool = False


DOMAINS = [
    Domain("01", "Secure AI Systems", "Agentic Platforms · RAG · Evidence-Oriented AI",
           "Безопасные AI-системы", "Агентные платформы · RAG · доказательный подход"),
    Domain("02", "Systems Engineering", "Rust · Operating Systems · Embedded · Low-Level",
           "Системная инженерия", "Rust · операционные системы · embedded · low-level"),
    Domain("03", "Radar & Avionics", "Safety-Critical · Autonomous Systems",
           "Радар и авионика", "Safety-critical · автономные системы"),
    Domain("04", "Cloud-Native", "Kubernetes · DevOps · Observability",
           "Cloud-native", "Kubernetes · DevOps · observability"),
    Domain("05", "Developer Systems", "CLI/TUI · Automation · Python Tooling",
           "Инструменты разработчика", "CLI/TUI · автоматизация · Python-инструменты", wide=True),
]


@dataclass
class Affiliation:
    label: str
    name: str
    role: str
    url: str = ""


AFFILIATIONS = [
    Affiliation("COMPANY / USA", "Glaeron LLC", "Founder & CEO", "https://www.glaeron.com"),
    Affiliation("EDUCATION / AUTHORSHIP", "Cartesian School", "Founder · Author"),
]

METADATA_STRIP = [
    ("20+ YEARS", "Engineering"),
    ("SYSTEMS → AI", "Full-stack engineering spectrum"),
    ("GLAERON LLC", "Founder & CEO"),
    ("CARTESIAN SCHOOL", "Founder · Author"),
]

PORTRAIT_JPG = "/assets/img/author/siergej-sobolewski.jpg"
PORTRAIT_WEBP = "/assets/img/author/siergej-sobolewski.webp"
PORTRAIT_ALT = "Siergej Sobolewski — инженер системного программного обеспечения и AI"
PORTRAIT_WIDTH = 456
PORTRAIT_HEIGHT = 570
