# Controlled Markov stochastic approximation research note

Quarto is the canonical source. `index.qmd` assembles nine section files into
one article with linked HTML and an understated LuaLaTeX PDF. Authoring
patterns are documented here rather than included in the manuscript.

## Requirements and setup

- [Quarto CLI](https://quarto.org/docs/get-started/) 1.6 or newer, including its bundled Pandoc.
- Python 3.10 or newer, using only the standard library.
- GNU Make (on Windows, use WSL or an equivalent Make installation).
- LuaLaTeX from a current TeX Live or TinyTeX installation, with Latin Modern
  fonts and the standard Pandoc article packages. The additional preamble uses
  `microtype` and `booktabs`; Quarto supplies AMS mathematics,
  `amsthm`, `fontspec`, `unicode-math`, and hyperlink support as needed.
- Zotero plus [Better BibTeX](https://retorque.re/zotero-better-bibtex/) for bibliography management.

No R, Jupyter, Python packages, Quarto extensions, Biber, or separate
`pandoc-crossref` executable is required. HTML math uses Quarto's MathJax CDN
loader, so reading the mathematics in a browser requires an internet connection.

From this directory:

```sh
quarto --version
python3 --version
quarto check
make check
```

If you need a TeX distribution, `quarto install tinytex` installs one. With an
existing TeX Live installation, install missing packages through its package
manager. Automatic package installation during rendering is disabled, so builds
do not silently change your TeX installation. Typical TinyTeX additions are
`tlmgr install microtype booktabs`; Pandoc's other standard packages
must also be present. TeX Live's recommended LaTeX, fonts, and LuaTeX collections
are a convenient alternative.

Replace the bracketed author and affiliation in `index.qmd`. Start drafting in
`sections/03-momentum.qmd` and `sections/04-adam-field.qmd` to settle the notation.
No details for real publications have been invented.

## Preview, build, and check

| Command | Result |
| --- | --- |
| `make preview` | Live HTML preview with automatic rebuilding |
| `make html` | `_output/index.html` and its supporting assets |
| `make pdf` | `_output/index.pdf` using LuaLaTeX |
| `make render` | Both formats |
| `make check` | Source checks, checker tests, both renders, diagnostics and HTML link checks |
| `make check-source` | Fast source checks and checker tests without rendering |
| `make clean` | Generated output, Quarto cache, and main-article LaTeX intermediates |

Make defaults to project-local Quarto and TeX caches, so it also works when the
home directory is read-only. Existing `XDG_CACHE_HOME`, `TEXMFVAR`, and
`TEXMFCACHE` environment settings take precedence. Caches are ignored by Git
and removed by `make clean`.

You can also run `quarto render --to all` directly. Only `index.qmd` is rendered;
the section and example files are includes, not standalone articles. `make check`
first verifies macro synchronization, citation keys in every `.qmd`, and duplicate
labels/unresolved references in the article's include tree. It then renders both
formats, rejects unresolved-reference diagnostics, and checks local HTML anchors.
These lightweight checks handle common Markdown patterns, not every Pandoc
extension; final rendering remains authoritative.

HTML footnotes appear as linked endnotes, with hover previews. PDF footnotes
use the standard page-bottom placement.

Every render synchronizes MathJax macros from `macros.tex`. After changing that
file, `make sync-macros` updates the generated header; commit both files.
`make check-source` detects a stale header before rendering can repair it.

## Zotero and Better BibTeX

`references.bib` is the sole bibliography database and is version controlled.
Zotero should own it after setup:

1. Install Zotero and Better BibTeX, then create a collection for this note.
2. Right-click that collection and choose **Export Collection…**.
3. Choose **Better BibTeX** and enable **Keep updated**.
4. Export directly to `<repo>/references.bib`, including the papers already cited.
5. In Better BibTeX preferences, review **Automatic exports** and choose an
   update schedule such as on change or on idle.

This is Better BibTeX's [automatic-export workflow](https://retorque.re/zotero-better-bibtex/exporting/auto/).
Do not maintain a second bibliography or hand-edit metadata that Zotero will
overwrite. Keep citation keys stable in Zotero and commit refreshed exports.
For Windows Zotero with WSL, select the Windows path to this same repository.

Use the actual exported keys. The following real-looking keys are **syntax
examples only**, not supplied bibliography records:

```markdown
This follows from @kassing2025.
The parenthetical form is [@kassing2025].
Compare [@kassing2025; @andrieuVihola2014].
See [@kassing2025, p. 12] or [@andrieuVihola2014, sec. 3].
```

The local `styles/numeric.csl` style produces linked citations such as `[1]`
and a numbered References list in order of first citation, in both HTML and
PDF. Numbers update automatically; keep writing citation keys rather than
typing numbers. The style is version controlled and requires no download.
A journal CSL can replace it through `csl: path/to/style.csl` in `_quarto.yml`.

## Common writing patterns

### Equations and semantic labels

```markdown
$$
\theta_{n+1}
=
\theta_n+\gamma_{n+1}H(\theta_n,X_{n+1})
$$ {#eq-controlled-sa}

By @eq-controlled-sa, ...
```

```markdown
$$
\Ftheta
=
\E_{\statlawtheta}
\left[
  \frac{\Mtheta}{\sqrt{\Vtheta}+\eps}
\right]
$$ {#eq-frozen-field}

As shown in @eq-frozen-field, ...
```

Numbered equations receive labels explicitly. Use native references throughout;
never write a positional number such as “equation (7)” or a positional label
such as `eq-1`. Semantic names like `eq-adam-m`, `eq-adam-v`, `eq-adam-update`,
and `eq-poisson` survive reordering. Labels must be unique across all included
sections.

### Results, assumptions, and proofs

```markdown
::: {#prp-momentum-field}
## Momentum proposition — draft

TODO: Supply hypotheses and a justified statement.
:::

See @prp-momentum-field.

::: {.proof}
TODO: Supply the proof.
:::

::: {#asm-uniform-ergodicity}
## Uniform ergodicity — draft

TODO: Specify constants, norms, and parameter range.
:::

Under @asm-uniform-ergodicity, ...
```

Quarto's [native proposition prefix is `prp-`](https://quarto.org/docs/authoring/cross-references.html#theorems-and-proofs),
so this repository uses `prp-momentum-field` instead of `prop-momentum-field`.
Write `@prp-momentum-field` on its own; it already prints “Proposition” and the
number. Writing `Proposition @prp-momentum-field` repeats the prefix.

| Label prefix | Meaning |
| --- | --- |
| `sec-` | Numbered section |
| `eq-` | Equation |
| `fig-`, `tbl-` | Figure, table |
| `thm-`, `prp-`, `lem-`, `cor-` | Theorem, proposition, lemma, corollary |
| `def-`, `asm-` | Definition, assumption |
| `rem-`, `exm-` | Remark, example |

Use lowercase semantic identifiers with hyphens, avoiding underscores. The label
prefix determines the native theorem environment; a `.proposition` class is not
necessary. A remark uses `::: {#rem-name .remark}`. Theorem blocks use a heading
for their name; that heading does not create a numbered subsection.

Assumptions use a small portable adapter: `filters/assumptions.lua` converts
`asm-` identifiers and references to Quarto's native `cnj-` theorem type, renamed
“Assumption” in `_quarto.yml`. This retains native numbering, hyperlinks, and
`amsthm` output in both formats. Reserve `cnj-` for the adapter; do not use it for
conjectures. HTML anchors for assumptions consequently start with `cnj-`; source
prose should use `@asm-...`. The adapter also handles local Markdown links.

Theorem types have separate counters within sections. HTML uses Quarto's native
top-level-section numbering (`crossref.chapters`); PDF uses `article` section
counters and `\numberwithin` for equations, figures, and tables. These settings
keep the numbering consistent without adding a chapter-based document class or
a competing cross-reference package.

### Macros, sections, figures, and tables

```tex
\Pkern{\theta_n}{X_n}{\dd x}
\Pstepn
\SAupdate
\Momentumupdate
\Secondmomentupdate
\Adamupdate
\FrozenAdamfield
\norm{x} \inner{x}{y} \Eunder{\statlawtheta}{f(X)}
```

`macros.tex` is the canonical semantic vocabulary; the same definitions are
generated into `mathjax-macros.html`. See `notes/notation.md` for all commands,
their arguments, and the notation templates. Keep new definitions in the
documented portable one-line `\newcommand` form so both formats agree.

```markdown
# Controlled Markov stochastic approximation {#sec-controlled-markov-sa}

See @sec-controlled-markov-sa.

![Caption describing the experiment.](figures/experiment.pdf){#fig-experiment}

See @fig-experiment.

| Parameter | Value |
|:----------|------:|
| Example | 1 |

: Caption describing the table. {#tbl-parameters}

See @tbl-parameters.
```

For actual figures, prefer a format readable by both outputs, such as PNG, or
provide PDF/SVG variants where necessary. The PDF path above is illustrative.
Keep mathematical source on deliberately broken lines; the source editor and
`.editorconfig` do not impose automatic line wrapping.

## Structure and adding sections

```text
_quarto.yml                 shared settings and format-specific configuration
index.qmd                   metadata, ordered section includes, References
sections/01-…09-*.qmd        nine modular research sections
macros.tex                  canonical semantic mathematical macros
mathjax-macros.html          generated HTML macro configuration
references.bib              Zotero-owned, version-controlled bibliography
tex/preamble.tex            shared PDF layout and counter setup
tex/pdf-only.tex            your additional PDF-only raw LaTeX preamble
filters/assumptions.lua     assumption adapter to native Quarto theorems
notes/notation.md           macro cheat sheet and notation conventions
notes/proof-obligations.md  internal PROVED / LITERATURE / TODO tracking
notes/literature-map.md     literature TODO headings
figures/                    figure source and assets
scripts/                    standard-library checking, synchronization, cleaning
tests/                      source-checker regression tests
_output/                    generated HTML, PDF, assets (ignored)
```

To add a section, create a `.qmd` under `sections/`, give its heading a unique
`sec-...` label, and insert `{{< include sections/your-section.qmd >}}` at the
desired position in `index.qmd`, before References. Includes resolve relative to
the main article; use repository-relative figure paths. Do not add separate YAML
front matter to section includes. Run `make check` after moving material.

Put custom raw LaTeX that affects only PDF in `tex/pdf-only.tex`. Keep ordinary
`.qmd` prose and theorem blocks in native Quarto syntax. The PDF build keeps the
generated `index.tex` (possibly moved under `_output/` by Quarto), making future
LaTeX submission work concrete: copy that TeX, bibliography and figure assets,
then adapt the document class and bibliography to the venue. Mathematical
expressions and semantic macros remain usable; venue-specific cleanup of
Quarto/Pandoc scaffolding may still be required.

## Validation environment

The setup is validated with Quarto 1.9.37 and TinyTeX/TeX Live 2026 using
LuaLaTeX. `make check` uses writable project-local caches automatically. When
running Quarto directly in a sandbox with a read-only home directory, use:

```sh
mkdir -p .quarto/cache _output/tex-var _output/tex-cache
XDG_CACHE_HOME="$PWD/.quarto/cache" \
TEXMFVAR=_output/tex-var \
TEXMFCACHE=_output/tex-cache \
quarto render --to all
```

Normal desktop installations do not need these cache overrides.
