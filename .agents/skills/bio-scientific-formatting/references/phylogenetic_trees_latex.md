# Phylogenetic Trees in LaTeX: TikZ and Forest

This guide explains how to format and render vector phylogenetic trees directly in LaTeX using the `forest` package (built upon TikZ).

---

## 1. Why Native TikZ/Forest over Raster Images?

- **Vector Crispness**: Scales infinitely in PDF output without pixelation or compression artifacts.
- **Font Uniformity**: Labels inherit the exact document font, sizing, and styling (`\taxa{...}`, `\small`, `\textbf`).
- **Dynamic Branch Annotations**: Direct LaTeX control over bootstrap percentages (`95`), posterior probabilities (`0.98`), or divergence times (`3.2 Ma`).

---

## 2. Basic Forest Cladogram Syntax

```latex
\usepackage{forest}

\begin{figure}[htbp]
\centering
\begin{forest}
  for tree={
    grow'=0,                 % Grow horizontally from left to right
    forked edges,            % Right-angle phylogram branches
    font=\small,
    draw,
    rounded corners,
    edge={draw=black, thick},
    parent anchor=east,
    child anchor=west,
    l=1.8cm,                 % Branch length
    s sep=0.7cm              % Sibling separation
  }
  [, edge label={node[midway, below]{\tiny 100}}
    [\textit{Sceloporus occidentalis}]
    [\textit{Sceloporus graciosus}]
  ]
\end{forest}
\caption{Phylogenetic tree showing sister relationship between fence and sagebrush lizards.}
\label{fig:clade_tree}
\end{figure}
```

---

## 3. Converting Newick Strings via Python CLI

Use the included `newick_to_forest.py` script:
```bash
uv run python .agents/skills/bio-scientific-formatting/scripts/newick_to_forest.py \
    --newick "((Sceloporus_occidentalis:0.04,Sceloporus_graciosus:0.05)98:0.03,Uta_stansburiana:0.09);" \
    --caption "Maximum Likelihood phylogeny with UFBoot support." \
    --label "fig:ml_tree" \
    --output figures/tree_figure.tex
```
Then simply include the generated code in your chapter:
```latex
\input{figures/tree_figure.tex}
```
