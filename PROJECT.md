# Project: Biology & Zoology Dissertation Skill Suite and Automated LaTeX Dissertation Generator

## Architecture
A specialized, modular academic dissertation engineering platform tailored for Life Sciences (Biology & Zoology) graduate students (Master's and Ph.D.). The architecture consists of four integrated pillars:
1. **Dissertation Skills Suite (`.agents/skills/`)**: Six skills: literature ingestion (`bio-research-sources`), ICZN nomenclature (`bio-nomenclature-ethics`), chapter scaffolding (`bio-chapter-builder`), BibLaTeX (`bio-reference-manager`), scientific formatting (`bio-scientific-formatting`), and pipeline orchestration (`final-output`).
2. **Research Staging Infrastructure (`research_sources/`)**: Dedicated student onboarding and agent discovery workspace with categorized subdirectories (`existing_work/`, `papers/`, `citations/`, `notes/`) and automated manifest tracking (`sources_manifest.json`).
3. **Modular LaTeX Engine & Build Automation**: A modular document architecture (`dissertation.tex`, `preamble.tex`, `frontmatter/`, `chapters/`, `appendices/`, `references.bib`) compiled via a cross-platform Python CLI (`build.py` managed via `uv`) supporting standalone Tectonic auto-bootstrapping, on-demand package downloading, and containerized Docker fallback.
4. **Diagnostic & Verification Suite (`verify.py`, `pipeline.py`)**: Skill schema validation, staging integrity, citation audit, and headless PDF compilation with zero-broken-cross-reference assertions.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Research Staging Directory Hierarchy | Standardized staging directories (`existing_work/`, `papers/`, `citations/`, `notes/`) with `.gitkeep` files | M1 | R2, survey |
| 2 | Research Staging Onboarding Guide | Comprehensive `README.md` in `research_sources/` guiding students and autonomous agents | M1 | R2, survey |
| 3 | Source Manifest Generation Schema | Machine-readable `sources_manifest.json` schema indexing staged files, SHA-256 hashes, categories, and targets | M1 | R1, R2, survey |
| 4 | Skill 1: `bio-research-sources` | Antigravity skill for discovering, ingesting, and synthesizing student drafts/notes and querying PubMed, bioRxiv, NCBI APIs | M2 | R1, survey |
| 5 | Skill 2: `bio-nomenclature-ethics` | Antigravity skill enforcing ICZN taxonomic rules (italicization, authority formats, novel taxa) and IACUC/field ethics compliance | M2 | R1, survey |
| 6 | Skill 3: `bio-chapter-builder` | Antigravity skill standardizing modular dissertation chapter scaffolding, drafting, and cross-chapter synthesis | M2 | R1, survey |
| 7 | Skill 4: `bio-reference-manager` | Antigravity skill for BibLaTeX reference management, CSE/APA styles, `.bib` deduplication, and biological data citations | M2 | R1, survey |
| 8 | Skill 5: `bio-scientific-formatting` | Antigravity skill for TikZ/Forest phylogenetic trees, Newick-to-Forest conversion, `booktabs`/`siunitx` tables, and specimen catalogs | M2 | R1, survey |
| 9 | Root LaTeX Document (`dissertation.tex`) | Master LaTeX root document integrating modular frontmatter, chapters, appendices, and bibliography | M3 | R3, survey |
| 10 | Life Sciences Preamble (`preamble.tex`) | LaTeX package configuration, ICZN nomenclature macros (`\taxa`, `\taxonauth`, `\spnov`, `\holotype`), `siunitx`, `mhchem`, `forest` | M3 | R3, survey |
| 11 | Modular Frontmatter Components | Title page, certificate, declaration, abstract, acknowledgements, abbreviations | M3 | R3, survey |
| 12 | Modular Dissertation Chapters | `01_introduction.tex` through `07_conclusion.tex` (Kashmir M.Sc. sequence) | M3 | R3, survey |
| 13 | Modular Appendix | `appendix_a_template.tex` (raw ZOI triplicates and phytochemical colour key) | M3 | R3, survey |
| 14 | Master Life Sciences Bibliography (`references.bib`) | BibLaTeX bibliography with biological, zoological, phylogenetic, and software reference entries | M3 | R3, survey |
| 15 | Python Project Management (`pyproject.toml`) | Project metadata, dependencies (`click`, `pyyaml`, `rich`), and CLI entry points managed via `uv` | M4 | R3, survey |
| 16 | Automated Compilation CLI (`build.py`) | Cross-platform build CLI (`uv run python build.py`) with multi-pass resolution and intermediate cleanup | M4 | R3, survey |
| 17 | Tectonic Auto-Bootstrapping Engine | Automatically downloads and caches standalone Tectonic binary from GitHub releases if missing from PATH | M4 | R3, survey |
| 18 | Containerized Docker Fallback | Seamless Docker fallback using `dxjoke/tectonic-docker` if native compilation is unavailable | M4 | R3, survey |
| 19 | Cross-Reference Diagnostics | Parser detecting undefined citations (`[?]`) and broken references (`??`), enforcing zero-broken-crossref policy | M4 | R3, R5, survey |
| 20 | Git Repository Configuration | Academic LaTeX and Python `.gitignore`, initial commit with active SSH commit signing (`commit.gpgsign true`) | M5 | R4, survey |
| 21 | GitHub Public Repository Deployment | Remote setup and push to `https://github.com/sahillangoo/bio-dissertation-generator` using verified OAuth credentials | M5 | R4, survey |
| 22 | Automated Verification Suite (`verify.py`) | Test script with diagnostic modules: skill YAML schema validation, staging validation, and headless PDF build check | M6 | R5, survey |
| 23 | E2E Test Suite & Testing Infra | Four-tier test suite (`TEST_INFRA.md` and `TEST_READY.md`) verifying all features, boundary cases, combinations, and full builds | M-E2E | R5, survey |
| 24 | Final Verification & Forensic Audit | End-to-end verification pass, 100% test pass, non-zero PDF verification, and independent forensic integrity audit | M-FINAL | R1-R5, survey |
| 25 | Lean Skills Suite | Six dissertation skills only; unused community/AI-research skills removed (KISS/YAGNI) | M7 | Cleanup |
| 26 | Master Dissertation Pipeline & Final Output Skill | 7-stage orchestrator CLI (`pipeline.py`) & skill (`final-output`) integrating staging, biology logic, drafting, citations, review, style scan, and final build | M8 | User Request |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Research Sources Staging & Integration | `research_sources/` subdirectories, guiding `README.md`, sample staging files, and manifest schema | none | **DONE** |
| M2 | Biology & Zoology Skill Suite | 5 Antigravity skills in `.agents/skills/` with compliant `SKILL.md`, `scripts/`, `references/`, and `examples/` | M1 | **DONE** |
| M3 | Modular LaTeX Dissertation Template | `dissertation.tex`, `preamble.tex`, `frontmatter/`, `chapters/`, `appendices/`, `references.bib` | none | **DONE** |
| M4 | Automated Compilation Engine | `pyproject.toml`, `build.py` with `uv`, Tectonic auto-bootstrap, Docker fallback, warning diagnostics | M3 | **DONE** |
| M5 | Git Setup & GitHub Deployment | Clean signed commit history, remote configuration, push to `sahillangoo/bio-dissertation-generator` | M1, M2, M3, M4 | **DONE** |
| M6 | Automated Verification Suite | `verify.py` diagnostic suite with skill YAML schema checks, staging checks, and headless build check (20/20 checks passed) | M2, M4 | **DONE** |
| M-E2E | E2E Testing Track | Independent opaque-box test runner, test tiers 1-4, `TEST_INFRA.md`, and `TEST_READY.md` publication (84/84 tests passed) | none | **DONE** |
| M-FINAL | Final Acceptance & Forensic Audit | 100% test pass across all tiers, non-zero PDF verification (169.48 KB), zero broken cross-refs, and CLEAN forensic audit | M1-M6, M-E2E | **VERIFIED & LIVE ON GITHUB** |
| M7 | Skills Cleanup (KISS/YAGNI) | Removed 90 unused external skills; repo ships 6 dissertation skills | M2, M6 | **DONE** |
| M8 | Master Pipeline & Final Output Skill | `pipeline.py` 7-stage orchestrator, `final-output` skill, `pipeline_outputs/` checkpointing, pytest (91/91 passed), verify (112/112 passed) | M1-M7 | **DONE** |

## Interface Contracts
### `research_sources/` <-> `bio-research-sources`
- Input: Files in `research_sources/existing_work/`, `papers/`, `citations/`, `notes/`
- Tool: `uv run python .agents/skills/bio-research-sources/scripts/ingest_sources.py --sources research_sources/ --output research_sources/sources_manifest.json`
- Output: `sources_manifest.json` containing array of file objects: `{"path": str, "sha256": str, "type": str, "target_chapter": str, "headings": list[str]}`

### `research_sources/citations/*.bib` <-> `bio-reference-manager` <-> `references.bib`
- Input: User staged `.bib` files in `research_sources/citations/`
- Tool: `uv run python .agents/skills/bio-reference-manager/scripts/bib_manager.py --merge --input research_sources/citations/ --master references.bib`
- Output: Synthesized, deduplicated, sorted master `references.bib`

### `preamble.tex` <-> `chapters/*.tex` & `appendices/*.tex`
- Macros:
  - `\taxa{Genus species}` -> italicized binomial
  - `\taxonauth{Taxon}{(Author, Year)}` -> ICZN compliant authority attribution
  - `\spnov{Taxon}` -> `Taxon \textbf{sp. nov.}`
  - `\holotype{CatalogID}` -> formatted holotype voucher specification
  - `\ce{...}` -> chemical formula rendering via `mhchem`
  - `\SI{value}{unit}` -> unit rendering via `siunitx`
  - `\begin{forest} ... \end{forest}` -> phylogenetic tree rendering

### `build.py` <-> LaTeX Source Files <-> `dissertation.pdf`
- Input: Root document `dissertation.tex` and modular dependencies
- Invocation: `uv run python build.py [--root dissertation.tex] [--output dissertation.pdf] [--strict] [--clean]`
- Output: Exit code 0, `dissertation.pdf` (>10 KB, 165.51 KB generated), warning report (citations, references)

### `verify.py` <-> System Verification
- Invocation: `uv run python verify.py [--skills-only] [--staging-only] [--build-only] [--json]`
- Output: Exit code 0 on pass (20/20 checks passed), structured diagnostics on failure

## Code Layout
```text
d:\sandbox\work-box\dissertation-skills\
├── .gitignore
├── ORIGINAL_REQUEST.md
├── PROJECT.md
├── TEST_INFRA.md
├── TEST_READY.md
├── deploy_github.ps1
├── pyproject.toml
├── build.py
├── verify.py
├── dissertation.tex
├── dissertation.pdf
├── preamble.tex
├── references.bib
├── frontmatter/
│   ├── title.tex
│   ├── certificate.tex
│   ├── declaration.tex
│   ├── abstract.tex
│   ├── acknowledgements.tex
│   └── abbreviations.tex
├── chapters/
│   ├── 01_introduction.tex
│   ├── 02_objectives.tex
│   ├── 03_lit_review.tex
│   ├── 04_methods.tex
│   ├── 05_results.tex
│   ├── 06_discussion.tex
│   └── 07_conclusion.tex
├── appendices/
│   └── appendix_a_template.tex
├── figures/
│   └── .gitkeep
├── research_sources/
│   ├── README.md
│   ├── sources_manifest.json
│   ├── existing_work/
│   │   ├── methods_draft.md
│   │   └── morphometrics.csv
│   ├── papers/
│   │   ├── literature_notes.md
│   │   └── smith2021_phylogeny_notes.md
│   ├── citations/
│   │   └── student_citations.bib
│   └── notes/
│       └── committee_notes.md
├── pipeline.py
├── tests/
│   ├── conftest.py
│   ├── test_build_cli.py
│   ├── test_cross_feature.py
│   ├── test_e2e_workload.py
│   ├── test_latex_structure.py
│   ├── test_pipeline_cli.py
│   ├── test_skills_schema.py
│   ├── test_staging.py
│   └── test_verify_cli.py
└── .agents/
    └── skills/
        ├── bio-research-sources/
        ├── bio-nomenclature-ethics/
        ├── bio-chapter-builder/
        ├── bio-reference-manager/
        ├── bio-scientific-formatting/
        └── final-output/
```
