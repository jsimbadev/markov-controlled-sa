# Notation and macro cheat sheet

`macros.tex` is the canonical vocabulary for PDF and HTML. After changing it,
run `python3 scripts/sync-macros.py` to regenerate `mathjax-macros.html`.
`python3 scripts/sync-macros.py --check` detects drift without changing files.
Do not edit the generated HTML header by hand.

Use one portable `\newcommand` definition per line, with mandatory arguments
only. This intentionally small common subset works in LaTeX and MathJax.
Reserve PDF-only customizations and raw LaTeX for `tex/pdf-only.tex`;
put mathematical notation that must work in both formats in `macros.tex`.

## Vocabulary

| Purpose | Source | Meaning |
| --- | --- | --- |
| Probability | `\E`, `\Etheta`, `\Prob` | Expectation, expectation at parameter theta, probability |
| Operators | `\Var`, `\Cov`, `\Law` | Variance, covariance, distribution |
| Filtration | `\cF_n` | Filtration at time n |
| Stationary law | `\statlawtheta`, `\statlaw{\vartheta}` | Stationary path/history law, distinct from the one-state invariant law |
| Expectations | `\expect{Z}`, `\Eunder{\statlawtheta}{Z}` | Bracketed expectation, optionally with an explicit law |
| Indicator | `\indicator{A}` | Indicator of event A |
| Kernel | `\Ptheta`, `\Pthetan`, `\Pvartheta` | Kernel at theta, theta_n, or vartheta |
| Invariant law | `\pitheta` | One-state invariant law at theta |
| Kernel evaluation | `\Pkern{\theta_n}{X_n}{\dd x}` | Transition kernel, current state, and integration measure |
| Kernel shorthand | `\Pstep`, `\Pstepn` | `P_theta(x, dot)` and `P_theta_n(X_n, dot)` |
| Mean field | `\htheta`, `\meanfieldtheta` | `h(theta)` and `pi_theta(H_theta)` |
| Update functions | `\Htheta`, `\Gtheta` | Parameterized functions H and G |
| SA recursion | `\SAupdate` | Full controlled stochastic approximation update |
| Frozen Adam notation | `\Ftheta`, `\Mtheta`, `\Vtheta` | Field F(theta), stationary first and second moments |
| Adam ratio | `\Adamratio{M}{V}` | Componentwise `M / (sqrt(V) + eps)` |
| Moment recursions | `\Momentumupdate`, `\Secondmomentupdate` | Full first- and second-moment updates |
| Adam recursion | `\Adamupdate` | Full parameter update using the two moment variables |
| Frozen field | `\FrozenAdamfield` | Full stationary expectation defining F(theta) |
| Spaces | `\ThetaSet`, `\StateSpace`, `\R`, `\N` | Parameter space, state space, reals, naturals |
| Geometry | `\norm{x}`, `\inner{x}{y}`, `\abs{a}` | Norm, inner product, absolute value |
| Pushforward | `\pushforward{T}{\mu}` | Image of measure mu under T |
| Convenience | `\eps`, `\dd x` | Epsilon and integration differential |
| Asymptotics | `\bigO{a_n}`, `\littleo{a_n}` | Big-O and little-o |
| Distributions and limits | `\eqdist`, `\convprob`, `\convlaw` | Equality in distribution, convergence in probability or distribution |

The recursion macros fix the initial indexing convention. Use their expanded
forms when a proof needs different indices or assumptions. The macros are
notation only: they make no assertions about existence, convergence, or
regularity. The square, square root, and quotient in Adam notation are
componentwise; state this convention where it is first used in the note.

## Initial notation: copyable source

These are source templates, not results. Place an expression in a displayed
math block in a `.qmd` section and give it a semantic label when needed.

```tex
X_{n+1}\mid\cF_n \sim \Pstepn
```

```tex
\SAupdate
```

```tex
\htheta = \meanfieldtheta
```

```tex
\Momentumupdate
```

```tex
\Secondmomentupdate
```

```tex
\Adamupdate
```

```tex
\FrozenAdamfield
```

For more control over line breaks, write the same vocabulary explicitly:

```tex
F(\theta)
=
\E_{\statlawtheta}
\left[
  \frac{\Mtheta}{\sqrt{\Vtheta}+\eps}
\right].
```

## Labels

Use semantic prefixes `sec-`, `eq-`, `fig-`, `tbl-`, `thm-`, `prp-`,
`lem-`, `cor-`, `def-`, `asm-`, `rem-`, and `exm-`. Names such as
`eq-frozen-adam-field` survive reordering; positional names such as `eq-1`
do not communicate meaning. A label is unique across all included sections.
Quarto's native proposition prefix is `prp-`; use it instead of `prop-`.

Start substantive drafting with `sections/03-momentum.qmd` and
`sections/04-adam-field.qmd` if that helps settle notation first. The section
skeleton deliberately contains no mathematical claims.
