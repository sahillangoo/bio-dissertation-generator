---
name: bio-chapter-builder
description: Standardizes modular dissertation scaffolding, chapter planning, section drafting, and cross-chapter synthesis for Biology and Zoology graduate dissertations. Generates LaTeX chapter structures, frontmatter, and specimen appendices with academic biological argumentation.
---

# Bio Chapter Builder

The `bio-chapter-builder` skill standardizes the architecture, scaffolding, and drafting progression of doctoral dissertations and master's theses in Biology, Zoology, and Evolutionary Ecology.

## Overview

A life sciences dissertation requires a rigorous organizational framework that coordinates empirical data, molecular protocols, phylogenetic topologies, and biological argumentation:
- **Modular Scaffolding**: Decomposes the thesis into discrete, independently testable files (`frontmatter/`, `chapters/`, `appendices/`).
- **Standardized Chapters**: Enforces the canonical Life Sciences structure:
  1. `01_introduction.tex`: Conceptual framing, evolutionary background, study system, hypotheses ($H_1, H_2, H_3$).
  2. `02_lit_review.tex`: Historical biogeography, phylogenetic paradigms, ecomorphological literature.
  3. `03_methods.tex`: Sampling, voucher catalogs, molecular assays, software pipelines, IACUC permits.
  4. `04_results.tex`: Trees, morphometric PCA, summary statistics, strict separation from interpretation.
  5. `05_discussion.tex`: Hypothesis testing, biological synthesis, study limitations, future research.
- **Appendices**: Dedicated repositories for museum voucher catalogs, primer tables, and statistical outputs.

## Dependencies

- Python 3.9+ standard library (`argparse`, `pathlib`, `sys`).
- Execution via `uv run python`.

## Quick Start

1. **Scaffold the Full Dissertation Structure**:
   ```bash
   uv run python .agents/skills/bio-chapter-builder/scripts/scaffold_dissertation.py \
       --target-dir .
   ```
   This generates `frontmatter/`, `chapters/`, and `appendices/` populated with structured templates without overwriting existing files.

2. **Force Re-generation of Modular Templates**:
   ```bash
   uv run python .agents/skills/bio-chapter-builder/scripts/scaffold_dissertation.py \
       --target-dir staging_test/ \
       --force
   ```

## Utility Scripts

### `scripts/scaffold_dissertation.py`
Generates the directory tree and standard starter files for:
- Frontmatter (`title.tex`, `abstract.tex`, `dedication.tex`, `acknowledgements.tex`, `abbreviations.tex`, `ethics_statement.tex`).
- Chapters (`01_introduction.tex`, `02_lit_review.tex`, `03_methods.tex`, `04_results.tex`, `05_discussion.tex`).
- Appendices (`appendix_a_specimens.tex`, `appendix_b_primers.tex`, `appendix_c_stats.tex`).

**CLI Options**:
- `--target-dir PATH`: Directory where modular directories should be scaffolded (default: `.`).
- `--force`: Overwrite existing files if present (default: preserve existing).

## Workflow & Methodology

```text
[Research Questions & Notes] ---> [Scaffold Architecture] ---> [Draft Individual Chapters]
                                           |                                |
                                  [Modular Directories]            [Cross-Chapter Synthesis]
                                   chapters/ frontmatter/             Consistent Labels & Citations
```

1. **Phase 1: Scaffolding**: Initialize the directory architecture using `scaffold_dissertation.py`.
2. **Phase 2: Ingest Staged Sources**: Cross-reference files indexed by `bio-research-sources` (`sources_manifest.json`) and assign content to respective chapters.
3. **Phase 3: Sectional Drafting**: Draft sections iteratively following the criteria in `references/chapter_drafting_guidelines.md`.
4. **Phase 4: Cross-Chapter Label Validation**: Ensure that all figure, table, and chapter cross-references adhere to the uniform labeling convention (`\label{ch:...}`, `\label{sec:...}`, `\label{fig:...}`, `\label{tab:...}`).

## References & Templates

- `references/chapter_drafting_guidelines.md`: In-depth advice on tone, pacing, biological argumentation, and separating results from discussion.
- `references/dissertation_structure_guide.md`: Structural specification, word count budgets, and label conventions.
- `examples/sample_outline.md`: Complete worked outline for an evolutionary ecology Ph.D. dissertation.

## Common Mistakes

- **Blending Results and Discussion**: Never mix interpretive evolutionary speculation into Chapter 4 (Results); reserve interpretation exclusively for Chapter 5 (Discussion).
- **Monolithic LaTeX Documents**: Never write the entire dissertation into a single `.tex` file; maintain modular chapter compartmentalization.
- **Inconsistent Labeling**: Using conflicting prefix conventions (e.g. `\label{Figure1}` vs. `\label{fig:tree}`); always follow standard lowercase prefixes (`ch:`, `sec:`, `fig:`, `tab:`, `app:`).
