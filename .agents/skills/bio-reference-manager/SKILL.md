---
name: bio-reference-manager
description: Manages BibLaTeX reference databases, CSE/APA citation styles, bibliography deduplication, and life sciences citation standards. Ingests and validates student BibTeX files from research_sources/citations/ and merges them into master references.bib with citation key diagnostics.
---

# Bio Reference Manager

The `bio-reference-manager` skill manages citation databases, BibLaTeX configurations, reference merging, and citation resolution across Biology and Zoology dissertations.

## Overview

Life sciences dissertations synthesize hundreds of citations spanning classical taxonomic descriptions, modern molecular phylogenetics, physiological studies, software tools, and digital database records:
- **BibLaTeX Architecture**: Standardizes on `biber` backend with Council of Science Editors (CSE) Name-Year style (`ext-authoryear`).
- **Automated Merging & Deduplication**: Discovers user `.bib` files in `research_sources/citations/` and merges them into the root `references.bib`, automatically resolving duplicate entries via citation keys, normalized DOIs, or title strings.
- **Citation Key Diagnostics**: Audits all `.tex` files across `chapters/` and `frontmatter/` to identify undefined citation keys before LaTeX compilation, preventing broken references (`[?]`).
- **Specialized Citation Formats**: Provides standardized templates for citing phylogenetic software (IQ-TREE, RevBayes), R packages, NCBI GenBank accessions, and museum vouchers.

## Dependencies

- Python 3.9+ with standard library modules (`argparse`, `pathlib`, `re`, `collections`, `sys`).
- Execution via `uv run python`.

## Quick Start

1. **Validate a Staged BibTeX File**:
   ```bash
   uv run python .agents/skills/bio-reference-manager/scripts/bib_manager.py \
       --validate research_sources/citations/student_citations.bib
   ```

2. **Merge Staged Citations into Root Bibliography**:
   ```bash
   uv run python .agents/skills/bio-reference-manager/scripts/bib_manager.py \
       --merge \
       --input research_sources/citations/ \
       --master references.bib
   ```

3. **Check for Undefined Citations in LaTeX Chapters**:
   ```bash
   uv run python .agents/skills/bio-reference-manager/scripts/bib_manager.py \
       --check-citations \
       --tex-dir chapters/ \
       --master references.bib
   ```

## Utility Scripts

### `scripts/bib_manager.py`
Integrated CLI for bibliography maintenance:
- `--validate PATH`: Validates syntax and verifies mandatory fields (`author`/`editor`, `title`, `year`).
- `--merge --input PATH --master PATH`: Deduplicates by key, DOI, and title; cleans and writes sorted entries to master bibliography.
- `--check-citations --tex-dir PATH --master PATH`: Scans `.tex` files for `\cite`, `\citep`, `\citet`, `\textcite`, `\parencite`, `\autocite` keys and compares them with defined entries.

## Workflow & Methodology

```text
[research_sources/citations/*.bib] ---> [bib_manager.py --merge] ---> [references.bib]
                                                                            |
[chapters/*.tex] ------------------------> [bib_manager.py --check] --------+
                                                    |
                                      Zero Undefined Keys Confirmed
```

1. **Staging**: The student exports `.bib` files into `research_sources/citations/`.
2. **Validation & Ingestion**: Run `bib_manager.py --validate` on staged files to guarantee syntactic validity.
3. **Merge**: Run `bib_manager.py --merge` to incorporate entries into `references.bib`.
4. **Pre-Compilation Verification**: Prior to invoking LaTeX compilation (`build.py`), run `--check-citations` to ensure every citation key in the manuscript is defined in `references.bib`.

## References & Templates

- `references/biblatex_styles_guide.md`: Configuration directives for CSE Name-Year and APA styles in `preamble.tex`.
- `references/specialized_citations.md`: Citation guidelines for software, datasets, and taxonomic monographs.
- `examples/sample_library.bib`: Reference BibTeX library fixture.

## Common Mistakes

- **Lowercasing Proper Nouns in Titles**: Forgetting to preserve capitalization with braces (e.g. `{Great} {Basin}`).
- **Inventing Citation Keys**: Citing a paper in `.tex` before adding its entry into `references.bib`.
- **Duplicate DOIs**: Adding duplicate entries from different export formats (e.g. Zotero vs Mendeley) without deduplication.
