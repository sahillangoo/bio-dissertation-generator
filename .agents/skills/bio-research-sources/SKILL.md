---
name: bio-research-sources
description: Discovers, indexes, and synthesizes user-provided research sources from research_sources/ (existing drafts, datasets, notes, citations) into dissertation chapters. Integrates with PubMed, bioRxiv, and NCBI Entrez APIs for life sciences literature synthesis, taxonomic verification, and provenance tracking.
---

# Bio Research Sources

The `bio-research-sources` skill equips agents to discover, ingest, and synthesize student-provided materials staged in `research_sources/` into publication-grade LaTeX dissertation chapters and bibliographies. It also defines protocols for retrieving peer-reviewed literature and taxonomy records from NCBI Entrez (PubMed, Taxonomy) and bioRxiv.

## Overview

Graduate students in biology and zoology produce diverse preliminary assets: lab protocols, field survey sheets, morphometric CSV files, reading notes, and reference manager exports. This skill bridges raw student inputs with structured LaTeX thesis authoring:
- **Manifest Tracking**: Automatically scans `research_sources/` and compiles `sources_manifest.json` with cryptographic SHA-256 hashes.
- **Chapter Routing**: Analyzes headings and content types to route drafts into appropriate thesis modules (`chapters/01_introduction.tex`, `chapters/03_methods.tex`, etc.).
- **Data Conversion**: Directs CSV and TSV tabular datasets to morphological table generation.
- **Literature Integration**: Synthesizes reading notes with external bibliographic databases while maintaining academic provenance.

## Dependencies

- Python 3.9+ with standard library modules (`argparse`, `pathlib`, `json`, `csv`, `hashlib`, `re`, `urllib`).
- Package manager: `uv` (standard runner: `uv run python`).
- Network access (optional): For live PubMed/NCBI or bioRxiv queries when verifying citations or taxonomic keys.

## Quick Start

1. **Scan and Index Staged Sources**:
   ```bash
   uv run python .agents/skills/bio-research-sources/scripts/ingest_sources.py \
       --sources research_sources/ \
       --output research_sources/sources_manifest.json \
       --summary
   ```

2. **Inspect the Generated Manifest**:
   Examine `research_sources/sources_manifest.json` to verify that files in `existing_work/`, `papers/`, `citations/`, and `notes/` have been detected, classified, and assigned target chapters.

## Utility Scripts

### `scripts/ingest_sources.py`
Scans all 4 staging folders under `research_sources/` (`existing_work/`, `papers/`, `citations/`, `notes/`).
- Computes SHA-256 digests to detect modifications.
- Extracts section headers from Markdown and LaTeX files.
- Extracts citation keys from `.bib` files.
- Extracts column headers and row counts from `.csv` and `.tsv` files.
- Maps each file to its target dissertation chapter.

**CLI Options**:
- `--sources PATH`: Path to the staging directory (default: `research_sources`).
- `--output PATH`: Path for the generated JSON manifest (default: `research_sources/sources_manifest.json`).
- `--summary`: Print human-readable summary table to stdout.

## Workflow & Methodology

```text
[research_sources/] ---> [ingest_sources.py] ---> [sources_manifest.json]
                                                        |
                    +-----------------------------------+-----------------------------------+
                    |                                   |                                   |
           [Drafts & Notes]                      [Tabular Data]                   [Bibliographies]
                    |                                   |                                   |
        Synthesize into Chapters             Convert via format_table.py         Merge via bib_manager.py
     (Intro, Methods, Discussion)             (booktabs + siunitx)                 into references.bib
```

1. **Step 1: Staging Discovery**: Run `ingest_sources.py` at the start of any drafting session to capture the current state of user materials.
2. **Step 2: Provenance Tagging**: When synthesizing text from staged drafts, insert an inline LaTeX provenance comment:
   ```latex
   % [Source: research_sources/existing_work/methods_draft.md, Section: DNA Extraction]
   ```
3. **Step 3: Verification with External Databases**:
   - Cross-check species binomials against NCBI Taxonomy.
   - Verify literature references against PubMed or bioRxiv using the query patterns documented in `references/external_apis_guide.md`.
4. **Step 4: Respect User Directives**: If advice in `research_sources/notes/` specifies specific research hypotheses ($H_1, H_2$) or methodology limits, these take precedence over generic academic defaults.

## References & Templates

- `references/ingestion_protocol.md`: Detailed protocol on file classification, token budgets, and conflict resolution.
- `references/external_apis_guide.md`: Query patterns, rate limits, and endpoint specifications for PubMed, NCBI Taxonomy, and bioRxiv.
- `examples/manifest_example.json`: Schema reference for `sources_manifest.json`.

## Common Mistakes

- **Deleting `.gitkeep` files**: Never delete `.gitkeep` files when scanning or cleaning staging directories.
- **Inventing citations**: Do not generate hallucinated citations. Every bibliographic entry must exist in `citations/` or be verified via PubMed/Crossref.
- **Ignoring student notes**: Committee directives in `notes/` are constraints, not suggestions; always check them before writing chapter introductions or discussions.
