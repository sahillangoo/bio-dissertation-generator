---
name: bio-scientific-formatting
description: Formats life sciences scientific outputs in LaTeX, including Newick phylogenetic tree conversion to TikZ/Forest cladograms, publication-grade anatomical and morphometric tables with booktabs and siunitx, museum voucher catalogs, and statistical reporting.
---

# Bio Scientific Formatting

The `bio-scientific-formatting` skill automates the production of publication-ready scientific figures, vector cladograms, morphological tables, and statistical notations in LaTeX for Biology and Zoology dissertations.

## Overview

Presenting complex biological data requires specialized LaTeX packages and consistent typography:
- **Phylogenetic Vector Trees**: Converts Newick tree strings directly into crisp vector graphics using the `forest` package (TikZ), including branch support metrics and italicized terminal taxa.
- **Publication Tables**: Generates standard `booktabs` tables with strict zero vertical lines, distinct horizontal rule weights (`\toprule`, `\midrule`, `\bottomrule`), and decimal point alignment via `siunitx` (`S` column specifications).
- **Specimen Catalogs**: Employs `longtable` environments for multi-page museum voucher appendices.
- **Statistical Notation**: Formats ANOVA, Student's $t$, PGLS, and PCA statistics according to life sciences journal guidelines.

## Dependencies

- Python 3.9+ standard library (`argparse`, `csv`, `pathlib`, `re`, `sys`).
- Execution via `uv run python`.
- LaTeX packages: `forest`, `tikz`, `booktabs`, `siunitx`, `longtable`.

## Quick Start

1. **Convert a Newick Tree to Forest LaTeX**:
   ```bash
   uv run python .agents/skills/bio-scientific-formatting/scripts/newick_to_forest.py \
       --input .agents/skills/bio-scientific-formatting/examples/sample_tree.nwk \
       --output figures/sample_phylogeny.tex
   ```

2. **Convert a Morphometric CSV to a Publication Table**:
   ```bash
   uv run python .agents/skills/bio-scientific-formatting/scripts/format_table.py \
       --input research_sources/existing_work/morphometrics.csv \
       --output chapters/morphometrics_table.tex \
       --caption "Linear morphometric measurements of sampled phrynosomatid lizards." \
       --label "tab:morphometrics"
   ```

## Utility Scripts

### `scripts/newick_to_forest.py`
Parses Newick phylogenetic trees and generates LaTeX `forest` environments.
- Automatically handles nested parenthetical clades, branch lengths, and interior node support labels.
- Converts taxon label underscores into spaces and wraps binomial names in `\textit{...}`.
- Outputs complete LaTeX `figure` environment with customizable caption and label.

**CLI Options**:
- `--input PATH`: Path to `.nwk` or text file containing Newick string.
- `--newick STRING`: Direct Newick string on the command line.
- `--output PATH`: Target file for generated LaTeX code.
- `--caption STRING`: Figure caption text.
- `--label STRING`: Figure cross-reference label.

### `scripts/format_table.py`
Converts CSV and TSV tabular datasets into publication-standard LaTeX `booktabs` tables.
- Automatically identifies numeric columns and applies `siunitx` decimal alignment (`S[table-format=X.Y]`).
- Automatically encloses column headers in braces in `S` columns.
- Escapes special LaTeX characters (`%`, `&`, `_`, `$`).
- Supports multi-page tables via the `--longtable` flag.

**CLI Options**:
- `--input PATH`: Path to input CSV or TSV file.
- `--output PATH`: Target file for generated LaTeX table.
- `--caption STRING`: Table caption text.
- `--label STRING`: Table label.
- `--longtable`: Emit a multi-page `longtable` environment.

## Workflow & Methodology

```text
[Newick File / Tree String] ---> [newick_to_forest.py] ---> [TikZ/Forest LaTeX Figure]
                                                                     |
[CSV Data / Measurements]   ---> [format_table.py]     ---> [Booktabs / SIunitx Table]
                                                                     |
                                                          Integrated into LaTeX Chapters
```

1. **Phylogenetic Reconstruction**: After generating a consensus or maximum likelihood tree in IQ-TREE or RevBayes, export the tree in Newick format.
2. **Vector Translation**: Run `newick_to_forest.py` to produce a vector TikZ/Forest figure, avoiding bitmap pixelation.
3. **Morphometric Formatting**: Convert raw measurement tables staged in `research_sources/existing_work/*.csv` using `format_table.py`.
4. **Statistical Reporting**: Format all in-text test statistics using the mathematical typography templates provided in `references/statistical_reporting_guide.md`.

## References & Templates

- `references/phylogenetic_trees_latex.md`: Syntax guide and styling options for `forest` trees.
- `references/anatomical_tables_guide.md`: Typography rules and examples for morphometric matrices and voucher catalogs.
- `references/statistical_reporting_guide.md`: Rules and formulas for reporting ANOVA, $t$-tests, PGLS, and PCA.
- `examples/sample_tree.nwk`: Reference Newick tree fixture.
- `examples/sample_table.csv`: Reference CSV table fixture.

## Common Mistakes

- **Vertical Lines in Tables**: Using `|` in table columns; vertical rules are strictly prohibited in scientific publishing.
- **Unprotected Text Headers in `siunitx` Columns**: Forgetting to brace text headers in `S` columns (e.g. `{Head Length}` vs `Head Length`), which causes `siunitx` parsing errors.
- **Rasterizing Cladograms**: Pasting blurry low-resolution PNG screenshots of trees instead of using native vector `forest` code.
- **Unitalicized Test Statistics**: Writing `F(2, 42) = 14.8` or `p < 0.05` without math mode italics (`$F(2, 42) = 14.8$`, `$p < 0.05$`).
