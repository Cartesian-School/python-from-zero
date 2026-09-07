# BOOK BUILD PIPELINE CONTRACT

**Document ID:** BBPC-001  
**Title:** Canonical Book Build Pipeline Architecture Contract  
**Status:** BINDING  
**Authority:** Product Owner Architecture Contract  
**Scope:** ALL BOOK LANGUAGES AND ALL PUBLICATION FORMATS  
**Applies to:** Cartesian School book publishing system  
**Primary outputs:** PDF, EPUB  
**Language editions:** RU, PL, EN, and any future supported language  
**Repository location:** `docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md`

---

## 1. Purpose

This document defines the mandatory architecture of the Cartesian School book publishing system.

Its purpose is to guarantee that all language editions and all supported publication formats are produced by one canonical, deterministic, maintainable, and testable book-build pipeline.

This contract exists to prevent:

- language-specific build forks;
- format-specific duplication of publishing logic;
- divergent PDF and EPUB content;
- inconsistent fixes between RU, PL, EN, or future editions;
- duplicated CSS or rendering rules;
- format regressions being fixed independently in multiple branches of the build system;
- drift between book editions that are expected to represent the same canonical structure.

The rules in this document are architectural constraints, not implementation suggestions.

---

## 2. Binding Architectural Principle

There MUST be exactly **one canonical book-build pipeline** for all supported language editions and all supported publication formats.

The selected language is only an **input parameter**.

The selected publication format is only an **output parameter**.

The canonical conceptual interface is:

```text
build_book(language, output_format)
```

For example:

```text
build_book(language="pl", output_format="pdf")
build_book(language="pl", output_format="epub")

build_book(language="ru", output_format="pdf")
build_book(language="ru", output_format="epub")

build_book(language="en", output_format="pdf")
build_book(language="en", output_format="epub")
```

The architecture MUST NOT be implemented as independent build systems such as:

```text
build_book_pl.py
build_book_ru.py
build_book_en.py

build_pdf_pl.py
build_pdf_ru.py
build_epub_pl.py
build_epub_ru.py
```

if those files duplicate or independently implement book-build logic.

Thin wrappers MAY exist only when they delegate to the same canonical pipeline without introducing independent publishing behavior.

---

## 3. Canonical Pipeline Model

The required high-level architecture is:

```text
Language-specific source content
            +
language = ru | pl | en | ...
            |
            v
Canonical source loader
            |
            v
Canonical book model
            |
            v
Common normalization
            |
            v
Common structural validation
            |
            v
Common component rendering
            |
            v
Common publication validation
            |
            v
Format adapter / format filter
        /                 \
       v                   v
 PDF adapter          EPUB adapter
       |                   |
       v                   v
     PDF                 EPUB
```

The following stages MUST be shared by every language and every publication format:

1. source discovery;
2. chapter ordering;
3. canonical metadata handling;
4. content normalization;
5. canonical component construction;
6. structural validation;
7. common semantic rendering;
8. internal-link resolution;
9. figure and asset resolution;
10. code/output component handling;
11. project-card handling;
12. callout handling;
13. heading hierarchy;
14. chapter mini-TOC generation;
15. common accessibility metadata;
16. common licensing metadata;
17. publication manifest generation;
18. regression validation framework.

Only the final format-specific adapter MAY introduce format-specific presentation behavior.

---

## 4. Language Independence

Formatting and publishing logic MUST be language-independent.

The language edition MUST NOT determine:

- which renderer implementation is used;
- which CSS architecture is used;
- pagination logic;
- heading page-break behavior;
- card layout rules;
- code block layout rules;
- output block layout rules;
- project-card layout rules;
- diagram layout rules;
- table layout architecture;
- chapter mini-TOC component implementation;
- publication validation architecture;
- PDF generation pipeline;
- EPUB generation pipeline.

A language edition MAY provide only content and language-specific metadata, for example:

```text
language code
translated chapter text
translated headings
translated captions
translated callout labels
translated navigation labels
localized metadata
language-specific typography exceptions that are linguistically necessary
```

Any language-specific exception MUST be explicit, minimal, documented, and MUST NOT create a separate build path.

---

## 5. Format Independence

The canonical book content MUST remain format-independent until the final publication adapter stage.

PDF and EPUB MUST be generated from the same canonical book state.

The PDF adapter MAY define:

- fixed page geometry;
- `@page` rules;
- page margins;
- running headers and footers;
- page numbering;
- print-specific widows and orphans handling;
- print-specific page-break behavior;
- print-specific card fragmentation rules;
- print-specific mini-TOC layout;
- font embedding requirements;
- PDF metadata;
- print-output validation metrics.

The EPUB adapter MAY define:

- reflowable layout rules;
- EPUB navigation document generation;
- reader-safe responsive image behavior;
- reflowable tables;
- code-block overflow behavior;
- EPUB package metadata;
- semantic HTML requirements;
- EPUB accessibility metadata;
- EPUB package structure;
- EPUB validation requirements.

The EPUB adapter MUST NOT inherit print-only page concepts unless required by the EPUB specification or intentionally represented as semantic section boundaries.

The PDF adapter MUST NOT alter canonical content merely to solve layout defects.

---

## 6. Canonical Content Model

The pipeline SHOULD use a canonical intermediate representation of the book instead of applying unrelated transformations directly to output-specific HTML.

A representative model is:

```text
Book
├── Metadata
├── FrontMatter
├── Chapter
│   ├── Section
│   ├── Subsection
│   ├── Paragraph
│   ├── CodeBlock
│   ├── OutputBlock
│   ├── Callout
│   ├── Exercise
│   ├── Diagram
│   ├── Figure
│   ├── Table
│   ├── ProjectCard
│   └── NavigationEntry
├── Appendices
├── Projects
├── Index
└── LicenseInformation
```

The same canonical component MUST represent the same semantic element for every language and every output format.

For example:

```text
ProjectCard
```

must remain one canonical component.

Its format behavior may differ:

```text
PDF:
- avoid fragmentation where practical;
- allow controlled internal fragmentation when the component is larger than one page.

EPUB:
- no fixed-page constraint;
- fully reflowable;
- responsive width;
- semantic structure preserved.
```

This distinction MUST be implemented by the output adapter, not by duplicating `ProjectCard` implementations per language or format.

---

## 7. Single Source of Publishing Truth

Publishing rules MUST have one authoritative implementation.

A defect fixed in the common pipeline MUST automatically apply to all languages.

For example, if a page-break defect affects:

```text
PL PDF
RU PDF
```

the fix MUST NOT be implemented independently for Polish and Russian editions.

The root cause MUST be fixed in the shared build pipeline so that the correction naturally propagates to:

```text
PL PDF
PL EPUB
RU PDF
RU EPUB
EN PDF
EN EPUB
```

where applicable.

The same principle applies to:

- broken cards;
- orphan headings;
- mini-TOC layout;
- code/output blocks;
- project cards;
- diagrams;
- tables;
- internal links;
- metadata;
- accessibility;
- chapter structure;
- asset resolution.

---

## 8. Root-Cause Requirement

No formatting defect may be treated as language-specific unless repository evidence proves that the defect originates from language-specific content.

For layout or pagination defects, the implementation team MUST trace:

```text
Rendered symptom
    ->
Canonical component
    ->
Generated HTML / semantic structure
    ->
CSS or renderer rule
    ->
Concrete source file
    ->
Root cause
```

A PDF or EPUB symptom is evidence of a defect, but not by itself proof of its source-code cause.

Before changing page-break, fragmentation, margin, padding, or component rules, the responsible agent MUST inspect the actual implementation and identify the root cause in code.

---

## 9. Required Build Interface

The canonical CLI SHOULD expose language and format as explicit parameters.

Recommended interface:

```bash
python scripts/build_book.py --language pl --format pdf
python scripts/build_book.py --language pl --format epub

python scripts/build_book.py --language ru --format pdf
python scripts/build_book.py --language ru --format epub

python scripts/build_book.py --language en --format pdf
python scripts/build_book.py --language en --format epub
```

Equivalent typed interfaces are acceptable, for example:

```python
from enum import StrEnum


class BookLanguage(StrEnum):
    PL = "pl"
    RU = "ru"
    EN = "en"


class PublicationFormat(StrEnum):
    PDF = "pdf"
    EPUB = "epub"


def build_book(
    language: BookLanguage,
    output_format: PublicationFormat,
) -> None:
    ...
```

The actual implementation MAY use a different internal structure, but the architecture MUST preserve the same semantics:

```text
language -> input parameter
format   -> output parameter
pipeline -> one canonical implementation
```

---

## 10. Common Rendering Rules

The following component families MUST have shared canonical definitions:

- chapter;
- section;
- subsection;
- paragraph;
- heading;
- code block;
- output/result block;
- note;
- idea;
- warning;
- typical mistake;
- official source;
- practice block;
- exercise;
- difficulty marker;
- project card;
- architecture diagram;
- state diagram;
- figure;
- figure caption;
- table;
- checklist;
- mini-TOC;
- appendix entry;
- license block.

Language selection MAY change their textual labels.

Language selection MUST NOT change their architectural implementation.

---

## 11. PDF-Specific Contract Boundary

PDF-specific logic MUST remain confined to the PDF publication adapter and its associated print stylesheet or renderer configuration.

The PDF adapter is responsible for:

- physical page dimensions;
- print margins;
- running page elements;
- pagination;
- controlled page breaks;
- widows and orphans;
- print typography;
- page-number references;
- print-specific navigation;
- page-density validation;
- font embedding;
- final PDF validation.

The PDF adapter MUST NOT:

- maintain independent chapter content;
- own translated strings that belong to source content;
- duplicate common book components;
- independently reorder chapters;
- introduce a language-specific build fork.

---

## 12. EPUB-Specific Contract Boundary

EPUB-specific logic MUST remain confined to the EPUB publication adapter and EPUB packaging layer.

The EPUB adapter is responsible for:

- reflowable HTML/CSS;
- EPUB navigation;
- package manifest;
- reading order;
- responsive images;
- semantic anchors;
- code-block overflow;
- table reflow strategy;
- EPUB metadata;
- accessibility metadata;
- EPUB validation.

The EPUB adapter MUST NOT:

- contain independent book content;
- duplicate translated chapters;
- use PDF pagination logic;
- depend on physical page numbers for normal navigation;
- duplicate common rendering logic;
- introduce a language-specific build fork.

---

## 13. Content Parity

For a given source revision and language, PDF and EPUB MUST represent the same canonical content.

The following MUST match semantically between formats:

- chapter count;
- chapter order;
- section hierarchy;
- code examples;
- output examples;
- project content;
- diagrams;
- figures;
- tables;
- appendices;
- licenses;
- navigation targets;
- canonical metadata.

Presentation may differ because PDF is fixed-layout and EPUB is reflowable.

Content MUST NOT differ because two independent build paths were used.

---

## 14. Build Manifest

Every publication run SHOULD generate a machine-readable manifest.

Recommended structure:

```json
{
  "book_version": "1.0.0",
  "language": "pl",
  "source_commit": "<git-commit>",
  "content_hash": "sha256:<canonical-content-hash>",
  "pipeline_version": "<pipeline-version>",
  "outputs": {
    "pdf": {
      "file": "python-od-zera-pl.pdf",
      "sha256": "<sha256>"
    },
    "epub": {
      "file": "python-od-zera-pl.epub",
      "sha256": "<sha256>"
    }
  }
}
```

The manifest MUST make it possible to prove which source revision and canonical content state produced a publication artifact.

---

## 15. CI Build Matrix

Continuous integration SHOULD validate the complete supported language/format matrix.

For the current language set:

```text
PL x PDF
PL x EPUB
RU x PDF
RU x EPUB
EN x PDF
EN x EPUB
```

The matrix MUST use the same canonical build entry point.

It MUST NOT invoke independent language-specific publishers.

A representative CI model is:

```text
matrix.language = [pl, ru, en]
matrix.format   = [pdf, epub]

build_book(
    language=matrix.language,
    output_format=matrix.format
)
```

---

## 16. Common Validation Gates

Every build MUST pass common structural validation before format-specific acceptance.

At minimum, common validation SHOULD verify:

- all expected chapters are present;
- chapter order is valid;
- required front matter is present;
- required appendices are present;
- required project artifacts are referenced;
- internal anchors are valid;
- images and diagrams resolve;
- code blocks are present;
- output/result blocks are structurally valid;
- navigation is complete;
- publication metadata is complete;
- language metadata matches the selected language;
- no production placeholders remain;
- licensing sections are preserved;
- no unsupported language-specific build fork was used.

---

## 17. PDF Regression Gates

PDF validation SHOULD include, at minimum:

```text
PDF generation succeeds
page count within approved threshold
average word density within approved threshold
median word density within approved threshold
no accidental near-empty pages
no uncontrolled card fragmentation
no orphaned headings
no missing chapters
no missing images
fonts embedded as required
internal links valid
text extraction succeeds
metadata valid
```

For the current remediation milestone, the target production range is approximately:

```text
600-800 pages
```

without deleting educational content merely to reach that target.

The page-count target may later be revised by an explicit Product Owner decision.

---

## 18. EPUB Regression Gates

EPUB validation SHOULD include, at minimum:

```text
EPUB generation succeeds
epubcheck PASS
navigation document valid
spine / reading order valid
all referenced resources present
internal anchors valid
images resolve
reflowable layout preserved
no print-only pagination dependency
no clipped code blocks
no unusable tables
language metadata valid
accessibility metadata valid
```

---

## 19. Protected Educational Structure

Publishing refactors MUST NOT remove or weaken approved pedagogical structures merely to simplify layout.

The following are protected unless explicitly changed by the Product Owner:

- theory -> code -> result -> explanation;
- exercise difficulty levels;
- classic approach -> modern Python 3.14 comparison blocks;
- architecture diagrams;
- state diagrams;
- accessibility guidance;
- engineering project workflows;
- SafeSort/GitHub engineering structure;
- separate licensing of educational text and source code.

Layout remediation MUST solve layout problems architecturally, not by deleting valuable educational content.

---

## 20. Prohibited Architecture

The following patterns are prohibited:

### 20.1 Language-specific build forks

```text
if language == "pl":
    run_polish_book_builder()

if language == "ru":
    run_russian_book_builder()
```

when those builders contain independent publishing logic.

### 20.2 Format-specific duplicated canonical logic

```text
build_pdf_book_model(...)
build_epub_book_model(...)
```

when both independently construct chapter/component semantics.

### 20.3 Copy-pasted CSS per language

```text
book-pl.css
book-ru.css
book-en.css
```

containing duplicated layout systems with language-specific divergence.

Language-specific typography overrides MAY exist only as narrow, documented exceptions layered on the shared base stylesheet.

### 20.4 Independent chapter ordering by output format

PDF and EPUB MUST NOT maintain separate chapter-order configuration.

### 20.5 Manual post-build content correction

A publication artifact MUST NOT require manual editing to become canonical.

If a generated PDF or EPUB requires manual content repair, the pipeline is defective and MUST be corrected at source.

---

## 21. Permitted Exceptions

An exception to this contract is allowed only when all of the following are true:

1. the requirement cannot be represented safely in the canonical pipeline;
2. the exception is technically necessary;
3. the exception is documented;
4. the exception is narrowly scoped;
5. the exception does not duplicate the whole publishing pipeline;
6. the exception is approved explicitly by the Product Owner.

Examples of potentially legitimate narrow exceptions:

- language-specific hyphenation dictionaries;
- font fallback required for a particular script;
- language-specific quotation-mark conventions;
- format-required metadata differences;
- EPUB-only semantic packaging data;
- PDF-only print crop or page metadata.

An exception MUST NOT become an alternate publisher.

---

## 22. Change-Control Rule

Any change that modifies one of the following requires review against this contract:

- build entry point;
- canonical book model;
- source loader;
- chapter ordering;
- normalization;
- shared renderer;
- shared CSS;
- PDF adapter;
- EPUB adapter;
- language routing;
- publication manifest;
- publication validation;
- CI publication matrix.

A proposed change MUST be rejected if it creates duplicate publishing logic without an approved architectural exception.

---

## 23. Review Checklist

Every publishing-related pull request SHOULD answer:

```text
[ ] Does this change preserve one canonical pipeline?
[ ] Is language still only an input parameter?
[ ] Is format still only an output parameter?
[ ] Is common rendering logic still shared?
[ ] Does this avoid language-specific build duplication?
[ ] Does this avoid PDF/EPUB content duplication?
[ ] Is the change made at the correct architectural layer?
[ ] Are common validation gates preserved?
[ ] Are PDF-specific rules confined to the PDF adapter?
[ ] Are EPUB-specific rules confined to the EPUB adapter?
[ ] Does the CI matrix still exercise supported language/format combinations?
[ ] Is content parity preserved between PDF and EPUB?
```

---

## 24. Acceptance Criteria for the Contract

The repository conforms to this contract when all of the following are true:

1. one canonical build entry point exists;
2. supported languages are passed as parameters;
3. supported formats are passed as parameters;
4. common source loading is shared;
5. one canonical book model is used;
6. common normalization is shared;
7. common validation is shared;
8. common components are shared;
9. PDF-specific behavior exists only in the PDF adapter;
10. EPUB-specific behavior exists only in the EPUB adapter;
11. no independent language-specific publisher exists;
12. CI can build all supported language/format combinations from the same pipeline;
13. PDF and EPUB for the same language are traceable to the same canonical source revision;
14. publishing fixes propagate across language editions when the root cause is language-independent.

---

## 25. Architectural Invariant

The following statement is the controlling invariant of this contract:

> **Formatting and publishing logic MUST be language-independent. There MUST be exactly one canonical book-build pipeline for all language editions and all supported publication formats. The selected language is only an input parameter. The selected publication format is only an output parameter.**

Any implementation that violates this invariant is non-conforming, even if its generated output appears visually correct.

---

## 26. Final Normative Model

```text
                    +----------------------+
                    | Selected language    |
                    | ru | pl | en | ...   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Canonical source     |
                    | loader               |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Canonical book model |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Common normalization |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Common validation    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Common rendering     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Format adapter       |
                    +----------+-----------+
                               |
                   +-----------+-----------+
                   |                       |
                   v                       v
          +----------------+      +----------------+
          | PDF adapter    |      | EPUB adapter   |
          +-------+--------+      +-------+--------+
                  |                       |
                  v                       v
                .pdf                    .epub
```

There is one publishing architecture.

Language selects the content.

Format selects the final representation.

Everything else remains canonical and shared.

---

**End of Contract**
