# Biology & Zoology Dissertation Skill Suite & Automated LaTeX Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Package Manager: uv](https://img.shields.io/badge/managed%20by-uv-purple.svg)](https://github.com/astral-sh/uv)
[![LaTeX Engine: Tectonic](https://img.shields.io/badge/latex-tectonic-orange.svg)](https://tectonic-typesetting.github.io/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An end-to-end academic dissertation engineering platform and automated LaTeX dissertation generator tailored specifically for Master's and Ph.D. graduate students in **Biology**, **Zoology**, and related Life Sciences.

This repository combines **six dissertation skills**, a **structured research staging workspace**, a **modular academic LaTeX template** with biological nomenclature macros, and a **zero-configuration cross-platform build engine** powered by `uv` and Tectonic (with Docker fallback).

---

## Table of Contents

- [Overview & Architecture](#overview--architecture)
- [Key Features](#key-features)
- [Directory Layout](#directory-layout)
- [Prerequisites & Installation](#prerequisites--installation)
- [Quickstart Guide](#quickstart-guide)
- [Research Staging Workflow (`research_sources/`)](#research-staging-workflow-research_sources)
- [Life Sciences Antigravity Skills Suite](#life-sciences-antigravity-skills-suite)
- [Master Dissertation Pipeline CLI (`pipeline.py`)](#master-dissertation-pipeline-cli-pipelinepy)
- [Modular LaTeX Structure](#modular-latex-structure)
- [Build CLI Reference (`build.py`)](#build-cli-reference-buildpy)
- [Automated Verification & Diagnostics (`verify.py`)](#automated-verification--diagnostics-verifypy)
- [Running Automated Tests](#running-automated-tests)
- [GitHub Deployment](#github-deployment)

---

## Overview & Architecture

Writing a Life Sciences dissertation requires complex formatting: binomial taxonomic nomenclature (ICZN rules), ethical animal care statements (IACUC / field permits), phylogenetic cladograms, high-dimensional morphometric tables, and dense literature syntheses.

This platform unifies these demands into three integrated layers:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      1. Student Input Layer                            │
│   research_sources/ (existing_work, papers, citations, notes)          │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   2. Antigravity AI Skills Suite                       │
│   .agents/skills/ (bio-research-sources, bio-nomenclature-ethics,      │
│    bio-chapter-builder, bio-reference-manager,                         │
│    bio-scientific-formatting, final-output)                            │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│               3. Modular LaTeX Engine & Build Automation               │
│   dissertation.tex, preamble.tex, chapters/, appendices/, build.py     │
│   ──> Output: dissertation.pdf (Publication-Standard Quality)          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Key Features

1. **Autonomous Research Staging**:
   - Staging area (`research_sources/`) for notes, drafts, datasets, and citation files.
   - Automated ingestion scripts (`ingest_sources.py`) generate machine-readable manifests (`sources_manifest.json`) for agent analysis.
2. **Domain-Specific Biological Typography**:
   - ICZN-compliant nomenclature macros: `\taxa{Genus species}`, `\taxonauth{Taxon}{Author, Year}`, `\spnov{Species}`, `\holotype{Museum:ID}`.
   - Built-in packages: `forest` & `tikz` (phylogenetic trees), `siunitx` (scientific units), `mhchem` (chemical buffers), `booktabs` (publication tables).
3. **Six Dissertation Skills**:
   - Progressive-disclosure skills covering literature synthesis, nomenclature, chapter scaffolding, BibLaTeX, scientific figures, and pipeline orchestration.
4. **Zero-Configuration LaTeX Compilation**:
   - Automatically bootstraps the standalone **Tectonic** engine from GitHub releases if no LaTeX engine is installed on the host system.
   - Includes seamless **Docker** fallback (`dxjoke/tectonic-docker` or `texlive/texlive`).
5. **Strict Cross-Reference & Bibliography Diagnostics**:
   - Detects undefined citations (`[?]`) and broken references (`??`), preventing malformed PDF submissions.
6. **One-Command Diagnostic Suite**:
   - `uv run python verify.py` validates skills schemas, staging integrity, and runs headless compilation checks.

---

## Directory Layout

```text
bio-dissertation-generator/
├── README.md                      # Comprehensive user and project documentation
├── PROJECT.md                     # System architecture and milestone tracking
├── ORIGINAL_REQUEST.md            # Verified project specification and acceptance criteria
├── TEST_INFRA.md                  # Test infrastructure specification and tier mapping
├── TEST_READY.md                  # Multi-tier test summary
├── pyproject.toml                 # Python project configuration (managed via uv)
├── uv.lock                        # Deterministic dependency lockfile
├── build.py                       # Automated cross-platform LaTeX compilation CLI
├── verify.py                      # Automated three-pass diagnostic verification CLI
├── pipeline.py                    # 7-stage dissertation pipeline orchestrator
├── deploy_github.ps1              # Automated Git staging and GitHub deployment script
│
├── dissertation.tex               # Root LaTeX document aggregating all components
├── preamble.tex                   # Life Sciences LaTeX packages, macros, and styling
├── references.bib                 # Master BibLaTeX bibliography database
│
├── frontmatter/                   # Modular front matter components
│   ├── title.tex                  # Academic title page
│   ├── certificate.tex            # Department certificate
│   ├── declaration.tex            # Candidate declaration
│   ├── abstract.tex               # Structured scientific abstract
│   ├── acknowledgements.tex       # Academic and personal acknowledgments
│   └── abbreviations.tex          # Glossary of acronyms
│
├── chapters/                      # Modular dissertation chapters (Kashmir M.Sc. sequence)
│   ├── 01_introduction.tex
│   ├── 02_objectives.tex
│   ├── 03_lit_review.tex
│   ├── 04_methods.tex
│   ├── 05_results.tex
│   ├── 06_discussion.tex
│   └── 07_conclusion.tex
│
├── appendices/                    # Modular appendices
│   └── appendix_a_template.tex    # Raw triplicate ZOI and phytochemical colour key
│
├── figures/                       # Plates used by Methods and Results
│   └── .gitkeep
│
├── research_sources/              # Student input staging workspace
│   ├── README.md                  # Staging guide and agent ingestion protocol
│   ├── sources_manifest.json      # Ingested manifest of all staged sources
│   ├── existing_work/             # Preliminary drafts, lab notes, CSV datasets
│   ├── papers/                    # Reference PDFs, paper summaries, matrices
│   ├── citations/                 # Custom .bib exports from Zotero/Mendeley
│   └── notes/                     # Committee guidance, outlines, hypotheses
│
├── .agents/skills/                # Dissertation skill suite (6 skills only)
│   ├── bio-research-sources/      # Source ingestion and API querying (PubMed/NCBI)
│   ├── bio-nomenclature-ethics/   # ICZN formatting and IACUC compliance
│   ├── bio-chapter-builder/       # Chapter scaffolding, section drafting, outlines
│   ├── bio-reference-manager/     # BibLaTeX deduplication and citation formatting
│   ├── bio-scientific-formatting/ # Phylogenetic trees, tables, voucher catalogs
│   └── final-output/              # 7-stage pipeline orchestrator
│
└── tests/                         # Comprehensive multi-tier test suite (84 tests)
```

---

## Prerequisites & Installation

### 1. Install `uv`
This project uses **[`uv`](https://docs.astral.sh/uv/)**, a fast Python package installer and resolver.

- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS / Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Clone & Sync Dependencies
```bash
git clone https://github.com/sahillangoo/bio-dissertation-generator.git
cd bio-dissertation-generator

# Sync all virtual environment dependencies
uv sync
```

*(Note: No manual LaTeX installation is required. The build CLI automatically bootstraps Tectonic on demand.)*

---

## Quickstart Guide

### 1. Compile the Dissertation to PDF
To build the complete dissertation into `dissertation.pdf`:
```bash
uv run python build.py
```
*Tectonic will download on first run (if needed), resolve references, and generate `dissertation.pdf` in the workspace root.*

### 2. Run Diagnostics
To verify that skills, staging, and the LaTeX pipeline are error-free:
```bash
uv run python verify.py
```

### 3. Run the E2E Test Suite
To run the automated test suite across all 4 tiers:
```bash
uv run pytest
```

---

## Research Staging Workflow (`research_sources/`)

Graduate students can drop existing material into `research_sources/` so autonomous agents can integrate it into the dissertation:

| Subfolder | Recommended Input | Ingestion Action |
|:---|:---|:---|
| `existing_work/` | `.docx`, `.md`, `.txt`, lab tables and plates | Ingested into `chapters/04_methods.tex` and `chapters/05_results.tex` |
| `papers/` | `.md`, `.pdf` reading notes, literature matrices | Synthesized into `chapters/03_lit_review.tex` and `chapters/06_discussion.tex` |
| `citations/` | `.bib` exports from Zotero, Mendeley, or EndNote | Merged and deduplicated into root `references.bib` |
| `notes/` | Advisor comments, research questions, committee minutes | Directs chapter structure and hypotheses ($H_0/H_1$) |

To index staged sources:
```bash
uv run python .agents/skills/bio-research-sources/scripts/ingest_sources.py \
    --sources research_sources/ \
    --output research_sources/sources_manifest.json
```

---

## Life Sciences Antigravity Skills Suite

Located in `.agents/skills/`, each skill contains detailed guidelines, examples, reference documents, and executable Python scripts:

| Skill | Role | Key Tools / Scripts |
|:---|:---|:---|
| **`bio-research-sources`** | Discovers, parses, and indexes student sources; queries PubMed & NCBI Entrez APIs | `ingest_sources.py`, `ncbi_query.py` |
| **`bio-nomenclature-ethics`** | Enforces ICZN taxonomic rules, authority citations, and IACUC/field ethical statements | `verify_nomenclature.py`, `ethics_templates.md` |
| **`bio-chapter-builder`** | Plans, outlines, and drafts modular chapters with standard biological argumentation | `build_outline.py`, `dissertation_structure_guide.md` |
| **`bio-reference-manager`** | Validates, formats, and deduplicates BibLaTeX entries across life sciences styles | `bib_manager.py`, `biblatex_styles_guide.md` |
| **`bio-scientific-formatting`** | Converts Newick trees to TikZ/Forest cladograms; formats `siunitx` tables & museum catalogs | `newick_to_forest.py`, `format_table.py` |
| **`final-output`** | 7-stage dissertation pipeline: staging, nomenclature, drafting, citations, review, style scan, PDF build | `run_pipeline.py`, `pipeline.py` |

---

## Master Dissertation Pipeline CLI (`pipeline.py`)

The platform includes a unified orchestrator CLI (`pipeline.py`) that chains all specialized skills into an automated 7-stage workflow:

```bash
uv run python pipeline.py [OPTIONS]
```

### Options

| Flag | Description |
|:---|:---|
| `--all` | Executes all 7 pipeline stages sequentially from staging to publication build |
| `--stage <name>` | Runs a specific stage (`staging`, `biology_logic`, `chapter_drafting`, `citation_audit`, `adversarial_review`, `de_ai_humanizer`, `final_build`) |
| `--list-stages` | Displays all 7 stages with descriptions |
| `--audit-skills` | Audits the 6 dissertation skills and writes `pipeline_outputs/skills_inventory.*` |
| `--status` | Displays the latest checkpoint state from `pipeline_outputs/pipeline_state.json` |
| `--clean` | Cleans previous artifacts in `pipeline_outputs/` before execution |
| `--json` | Emits machine-readable JSON status |

### Generated Audit Deliverables (`pipeline_outputs/`)

- `pipeline_outputs/sources_manifest.json`: Machine-readable index of staged drafts, notes, and datasets.
- `pipeline_outputs/skills_inventory.json`: Catalog of the 6 dissertation skills.
- `pipeline_outputs/skills_inventory.md`: Markdown inventory of skill roles and paths.
- `pipeline_outputs/biology_logic_audit.json`: ICZN taxonomic binomials, novel taxa designations, and IACUC ethics permit audit.
- `pipeline_outputs/drafting_status.json`: Chapter word counts, structural breakdown, and figure/table label census.
- `pipeline_outputs/citation_verification.json`: BibLaTeX key resolution rate (100% assertion) and citation diagnostics.
- `pipeline_outputs/reviewer2_audit.md`: Adversarial peer-review critique across hypotheses, methods, and results.
- `pipeline_outputs/de_ai_humanizer_report.md`: Stylistic authenticity score, cliché analysis, and de-AI refinement recommendations.
- `pipeline_outputs/pipeline_state.json`: Execution timestamps, stage durations, and convergence status.
- `dissertation.pdf`: Final publication-ready PDF artifact in root.

---

## Modular LaTeX Structure

The master document [`dissertation.tex`](file:///d:/sandbox/work-box/dissertation-skills/dissertation.tex) cleanly assembles the dissertation using modular `\input{...}` commands:

- **Preamble ([`preamble.tex`](file:///d:/sandbox/work-box/dissertation-skills/preamble.tex))**: Configures hyperref, geometry, booktabs, siunitx, forest, and biological macros:
  - `\taxa{Genus species}` -> *Genus species*
  - `\taxonauth{Balaenoptera musculus}{(Linnaeus, 1758)}` -> *Balaenoptera musculus* (Linnaeus, 1758)
  - `\spnov{Cryptic chlorophyta}` -> *Cryptic chlorophyta* sp. nov.
  - `\holotype{USNM 123456}` -> Holotype: USNM 123456
- **Front Matter (`frontmatter/`)**: Title page, certificate, declaration, abstract, acknowledgments, and abbreviations glossary.
- **Chapters (`chapters/`)**: Modular chapter files (`01_introduction.tex` through `07_conclusion.tex`) with `booktabs` tables and laboratory plates.
- **Appendices (`appendices/`)**: Raw triplicate zone-of-inhibition data (`appendix_a_template.tex`).
- **Bibliography ([`references.bib`](file:///d:/sandbox/work-box/dissertation-skills/references.bib))**: Validated BibLaTeX entries with DOI links.

---

## Build CLI Reference (`build.py`)

The build CLI supports comprehensive compilation controls:

```bash
uv run python build.py [OPTIONS]
```

### Options

| Flag | Short | Default | Description |
|:---|:---|:---|:---|
| `--root` | `-r` | `dissertation.tex` | Master LaTeX source file |
| `--output` | `-o` | `dissertation.pdf` | Destination PDF path |
| `--engine` | `-e` | `auto` | Compiler: `auto`, `tectonic`, `docker`, or `system` |
| `--clean` | `-c` | `False` | Cleans auxiliary files before/after compilation |
| `--keep-intermediates` | | `False` | Retains temporary auxiliary files (`.aux`, `.bcf`, etc.) |
| `--strict` | | `False` | Fails build if undefined citations or broken cross-references exist |
| `--watch` | `-w` | `False` | Watches source directory and recompiles automatically upon edit |
| `--verbose` | `-v` | `False` | Outputs detailed compiler diagnostics |

---

## Automated Verification & Diagnostics (`verify.py`)

Run the three-pass verification suite to audit the entire project before submission or defense:

```bash
uv run python verify.py
```

### Verification Checks Performed:
1. **Skill YAML Frontmatter & Schema Validation**: Verifies `name`, `description`, instructions, and examples for the 5 core bio skills plus `final-output`.
2. **Staging Directory & Manifest Integrity**: Verifies staging directories, file formats, and `sources_manifest.json` consistency.
3. **Headless Compilation & Cross-Reference Audit**: Executes a real-time compilation pass and verifies:
   - Valid non-zero PDF generation.
   - Zero missing citations (`[?]`).
   - Zero broken section/figure cross-references (`??`).

---

## Running Automated Tests

Run the full pytest suite (84 automated tests across 4 tiers):

```bash
# Run all tests
uv run pytest

# Run with coverage and verbose output
uv run pytest -v
```

### Test Tiers Covered:
- **Tier 1 (Contract & Schema)**: Skill YAML validation, staging manifest structure, CLI option parsing.
- **Tier 2 (Integration)**: Source ingestion workflows, BibTeX deduplication, LaTeX macro consistency.
- **Tier 3 (Compilation)**: Tectonic bootstrapping, multi-pass PDF compilation, cross-reference integrity.
- **Tier 4 (Edge Cases)**: Empty staging directories, malformed BibTeX handling, corrupt cache recovery.

---

## GitHub Deployment

To commit all project components and publish to GitHub under your profile:

```powershell
# Run the automated deployment script
.\deploy_github.ps1
```

Or manually:
```bash
git add .
git commit -m "feat: initialize biology and zoology dissertation skills suite and automated latex generator"
git remote add origin https://github.com/sahillangoo/bio-dissertation-generator.git
git branch -M main
git push -u origin main
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
