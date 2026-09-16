---
name: bio-nomenclature-ethics
description: Enforces International Code of Zoological Nomenclature (ICZN) taxonomic formatting rules, binomial/trinomial italicization, authority citations, novel taxon designations, and mandatory animal care (IACUC) and field collection ethical permit compliance in LaTeX dissertations.
---

# Bio Nomenclature & Ethics

The `bio-nomenclature-ethics` skill enforces zoological taxonomic standards governed by the **International Code of Zoological Nomenclature (ICZN, 4th Edition)** and institutional ethical compliance regulations (IACUC, field permits, CITES, Nagoya Protocol) across life sciences dissertation manuscripts.

## Overview

Taxonomic zoology and evolutionary biology require strict adherence to international nomenclature conventions:
- **Typographic Accuracy**: Generic, specific, and subspecific names must be italicized (`\textit{Sceloporus occidentalis}` or `\taxa{Sceloporus occidentalis}`), whereas suprageneric taxa (Families, Orders, Classes) remain Roman.
- **Authority Formatting**: Zoological authority citations require a comma between author and date (ICZN Art. 22A), with parentheses indicating altered generic combinations (Art. 51).
- **Abbreviation Rules**: Generic abbreviations (*S. occidentalis*) are forbidden at the start of sentences and require full spelling upon initial mention in each chapter.
- **Novel Taxa & Typification**: Strict syntax for `sp. nov.`, holotype designations, institution acronyms, and type locality coordinates.
- **Regulatory Ethics**: Dissertations involving vertebrate animals must cite explicit Institutional Animal Care and Use Committee (IACUC) protocol approval numbers and scientific collecting permits.

## Dependencies

- Python 3.9+ with standard library modules (`argparse`, `pathlib`, `re`, `json`, `sys`).
- Execution via `uv run python`.

## Quick Start

1. **Validate All Chapters for Nomenclature & Ethics**:
   ```bash
   uv run python .agents/skills/bio-nomenclature-ethics/scripts/validate_nomenclature.py \
       --dir chapters/ \
       --strict
   ```

2. **Validate a Single Manuscript Draft**:
   ```bash
   uv run python .agents/skills/bio-nomenclature-ethics/scripts/validate_nomenclature.py \
       --file research_sources/existing_work/methods_draft.md
   ```

## Utility Scripts

### `scripts/validate_nomenclature.py`
Scans LaTeX (`.tex`) and Markdown (`.md`) files to detect:
1. Unitalicized Latin binomials and trinomials.
2. Uncapitalized genus names.
3. Abbreviated genera starting a sentence (e.g., `S. occidentalis was observed...`).
4. Missing commas in zoological authority citations (e.g., `Baird & Girard 1852`).
5. Absence of mandatory IACUC approval or wildlife permit citations in methods and frontmatter.

**CLI Options**:
- `--file PATH`: Scan a single target file.
- `--dir PATH`: Scan all LaTeX and Markdown files in a directory (default: `.`).
- `--strict`: Return non-zero exit code if any warning is reported.
- `--json`: Output structured JSON diagnostics for automated test pipelines.

## Workflow & Methodology

1. **Initial Draft Audit**: Before drafting or integrating any new chapter, run `validate_nomenclature.py` to identify unformatted binomials or missing ethical statements.
2. **Standard LaTeX Macros**: Use the standardized preamble macros for taxonomic consistency:
   - `\taxa{Genus species}` -> Formats italicized binomial.
   - `\taxonauth{Taxon}{(Author, Year)}` -> Formats ICZN-compliant authority attribution.
   - `\spnov{Taxon}` -> Formats novel species designation (`Taxon \textbf{sp. nov.}`).
   - `\holotype{CatalogID}` -> Formats holotype voucher catalog number.
3. **Sentence Structuring**: When an abbreviated taxon appears at the beginning of a paragraph or sentence, restructure the sentence to spell out the genus in full or introduce a common name prefix.
4. **Ethics Verification**: Ensure the exact IACUC protocol number (e.g., `#IACUC-2024-0892-VANCE`) and state permit numbers appear in both `frontmatter/ethics_statement.tex` and `chapters/03_methods.tex`.

## References & Templates

- `references/iczn_rules_reference.md`: Comprehensive ICZN articles, authority formats, and novel taxon checklists.
- `references/iacuc_ethics_templates.md`: Standard boilerplates for vertebrate research, anesthesia, and field collection permits.
- `references/cites_nagoya_guidelines.md`: International tissue transfer, CITES appendices, and Nagoya Protocol documentation.
- `examples/sample_nomenclature_check.tex`: Test fixture demonstrating compliant syntax.

## Common Mistakes

- **Omitting the Comma in Zoological Authorities**: Writing `Baird & Girard 1852` instead of `Baird & Girard, 1852`.
- **Abbreviating at Sentence Start**: Writing `S. occidentalis displays...` instead of `Sceloporus occidentalis displays...`.
- **Missing Voucher Deposition**: Describing a new taxon or phylogenetic dataset without depositing specimens in an accredited museum.
- **Forgetting IACUC Protocol Numbers**: Stating "Animals were cared for humanely" without providing the specific institutional approval protocol number.
