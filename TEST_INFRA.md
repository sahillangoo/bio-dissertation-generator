# Test Infrastructure & Specification: Biology & Zoology Dissertation Skill Suite

**Version**: 1.0.0  
**Target Project**: Biology & Zoology Dissertation Skill Suite & Automated LaTeX Dissertation Generator  
**Author**: E2E Test Writer (`teamwork_preview_test_writer_e2e_1`)  
**Scope**: Full Opaque-Box E2E Testing Framework (Tiers 1–4)

---

## 1. Testing Philosophy & Architecture

The testing framework for the Biology & Zoology Dissertation Skill Suite employs a strict **opaque-box, contract-driven methodology**. Rather than testing internal code implementation minutiae, tests verify external interfaces, schema invariants, command-line behavior, file contracts, and artifact generation across four rigorous tiers.

```text
+-------------------------------------------------------------------------+
|                       Tier 4: Real-World Workloads                      |
|  - Headless multi-pass PDF compilation via build.py                     |
|  - Non-zero PDF verification (>10 KB, valid %PDF- header)               |
|  - Zero broken cross-references (no "??" or "[?]" in final output)     |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
|                  Tier 3: Cross-Feature Combinations                     |
|  - Ingestion (research_sources/ -> sources_manifest.json)               |
|  - Citation merging (student_citations.bib -> references.bib)           |
|  - Tree/table synthesis (Newick -> Forest, CSV -> booktabs/siunitx)     |
|  - Pipeline integration: Ingestion -> BibTeX -> Chapter -> PDF          |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
|                    Tier 2: Boundary & Corner Cases                      |
|  - Malformed YAML frontmatter (missing keys, length limits)             |
|  - Empty staging directories (only .gitkeep present)                    |
|  - Missing / unresolvable bibliography keys (\cite{invalid_key})        |
|  - CLI warning handling: --strict exit code 1 vs standard exit code 0   |
|  - Malformed Newick strings and empty CSV tables                        |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
|                      Tier 1: Feature Coverage                           |
|  - 5 Antigravity skills schema (SKILL.md frontmatter, scripts/, docs)   |
|  - Staging directory structure (existing_work, papers, citations, notes)|
|  - Modular LaTeX document hierarchy (dissertation, preamble, chapters)  |
|  - Life Sciences preamble macros (\taxa, \taxonauth, \spnov, \holotype) |
|  - build.py CLI interface and flag parsing (--help, --root, --output)   |
+-------------------------------------------------------------------------+
```

### Key Principles
1. **Opaque-Box Verification**: Tests invoke commands (`uv run python build.py`, `uv run python <script>.py`) and inspect outputs, transcripts, exit codes, and generated files without altering production logic.
2. **Progressive Testability**: Each tier is self-contained. Tier 1 checks structural prerequisites, Tier 2 stresses boundaries using isolated temporary environments, Tier 3 validates data flow across modules, and Tier 4 exercises the full build engine.
3. **Hermetic Isolation**: Tests that generate auxiliary files or test malformed inputs operate within pytest's temporary directory fixture (`tmp_path`) to prevent polluting or mutating production workspace files.
4. **Life Sciences Domain Fidelity**: Validates strict ICZN zoological taxonomic conventions, IACUC animal welfare frontmatter, CSE/APA citation standards, and vector phylogenetic tree rendering.

---

## 2. Four-Tier Testing Methodology

### Tier 1: Feature Coverage (Structural & Contract Smoke Tests)

Validates the presence, formatting, and structural integrity of all declared project deliverables.

| Test ID | Module | Target Feature | Validation Rules |
|---|---|---|---|
| `T1-SKILL-01` | `test_skills_schema.py` | Skill Directory Presence | All 5 skills exist under `.agents/skills/`: `bio-research-sources`, `bio-nomenclature-ethics`, `bio-chapter-builder`, `bio-reference-manager`, `bio-scientific-formatting`. |
| `T1-SKILL-02` | `test_skills_schema.py` | YAML Frontmatter Delimiters | Every `SKILL.md` begins with `---` on line 1 and contains a closing `---` delimiter. |
| `T1-SKILL-03` | `test_skills_schema.py` | Skill Name Format | `name` field is lowercase alphanumeric with hyphens (`^[a-z0-9-]+$`), $\le 64$ characters, matching its directory name. |
| `T1-SKILL-04` | `test_skills_schema.py` | Skill Description | `description` field is a non-empty string $\le 1024$ characters containing semantic trigger keywords. |
| `T1-SKILL-05` | `test_skills_schema.py` | Progressive Disclosure Subdirs | Each skill contains `scripts/`, `references/`, and `examples/` subdirectories. |
| `T1-SKILL-06` | `test_skills_schema.py` | Skill CLI Script Executability | All scripts under `scripts/` can be executed with `--help` and exit code 0. |
| `T1-STAGE-01` | `test_staging.py` | Staging Folder Hierarchy | `research_sources/` contains `existing_work/`, `papers/`, `citations/`, `notes/`. |
| `T1-STAGE-02` | `test_staging.py` | Staging Onboarding Guide | `research_sources/README.md` exists and contains instructions for students and agents. |
| `T1-STAGE-03` | `test_staging.py` | Gitkeep Preservation | Every staging subdirectory preserves `.gitkeep` for version control tracking. |
| `T1-STAGE-04` | `test_staging.py` | Sample Staging Files | Realistic sample files exist in staging (`methods_draft.md`, `morphometrics.csv`, `student_citations.bib`, `committee_notes.md`). |
| `T1-LATEX-01` | `test_latex_structure.py` | Root LaTeX Document | `dissertation.tex` exists and inputs frontmatter, chapters, appendices, and bibliography. |
| `T1-LATEX-02` | `test_latex_structure.py` | Life Sciences Preamble | `preamble.tex` exists, loads required packages (`geometry`, `booktabs`, `siunitx`, `mhchem`, `forest`, `biblatex`), and defines ICZN macros (`\taxa`, `\taxonauth`, `\spnov`, `\holotype`). |
| `T1-LATEX-03` | `test_latex_structure.py` | Frontmatter Modules | `frontmatter/` contains `title.tex`, `certificate.tex`, `declaration.tex`, `abstract.tex`, `acknowledgements.tex`, `abbreviations.tex`. |
| `T1-LATEX-04` | `test_latex_structure.py` | Chapter Modules | `chapters/` contains `01_introduction.tex` through `07_conclusion.tex` (Kashmir M.Sc. sequence). |
| `T1-LATEX-05` | `test_latex_structure.py` | Appendix Modules | `appendices/` contains `appendix_a_template.tex`. |
| `T1-LATEX-06` | `test_latex_structure.py` | Master Bibliography | `references.bib` exists and contains valid BibTeX entries. |
| `T1-CLI-01` | `test_build_cli.py` | Build CLI Presence | `build.py` exists and can be executed via Python standard invocation. |
| `T1-CLI-02` | `test_build_cli.py` | CLI Help Output | `build.py --help` exits with code 0 and displays supported arguments (`--root`, `--output`, `--engine`, `--clean`, `--strict`, `--verbose`). |

---

### Tier 2: Boundary & Corner Cases (Stress & Fault Injection Tests)

Validates error recovery, edge-condition handling, and defense against malformed inputs.

| Test ID | Module | Target Boundary | Validation Rules |
|---|---|---|---|
| `T2-SKILL-01` | `test_skills_schema.py` | Malformed Frontmatter Delimiters | Missing `---` delimiters or missing `name`/`description` fields are rejected by validator with informative errors. |
| `T2-SKILL-02` | `test_skills_schema.py` | Excessive Description Length | Descriptions exceeding 1024 characters are flagged as schema violations. |
| `T2-SKILL-03` | `test_skills_schema.py` | Invalid Skill Name Characters | Skill names with uppercase letters, spaces, or underscores are flagged as invalid. |
| `T2-STAGE-01` | `test_staging.py` | Empty Staging Directory Handling | `ingest_sources.py` run on an empty staging folder (containing only `.gitkeep`) produces a valid empty/minimal JSON manifest without crashing. |
| `T2-STAGE-02` | `test_staging.py` | Unrecognized File Extension Handling | Staging unknown file types (e.g. `.bin`, `.xyz`) logs warnings or categorizes gracefully without uncaught exceptions. |
| `T2-BIB-01` | `test_latex_structure.py` | Undefined Citation Key Detection | `bib_manager.py` detects when a `.tex` document cites a key absent from `references.bib`. |
| `T2-BIB-02` | `test_cross_feature.py` | Duplicate BibTeX Entry Deduplication | Merging two `.bib` files containing identical citation keys or DOIs retains exactly one entry without duplicate key syntax errors. |
| `T2-CLI-01` | `test_build_cli.py` | Non-Existent Root Document | `build.py --root non_existent_file.tex` exits with non-zero exit code and reports error message. |
| `T2-CLI-02` | `test_build_cli.py` | `--strict` Mode Warning Enforcement | In `--strict` mode, compilation encounters undefined reference/citation warnings and enforces non-zero exit code. |
| `T2-TREE-01` | `test_cross_feature.py` | Malformed Newick String Handling | `newick_to_forest.py` fed an unbalanced Newick string (e.g. `((A, B);`) raises a clear parsing error rather than producing corrupted LaTeX code. |
| `T2-TAB-01` | `test_cross_feature.py` | Empty CSV Table Formatting | `format_table.py` fed an empty CSV file or CSV with only headers produces a valid empty `tabular` environment or exits gracefully. |

---

### Tier 3: Cross-Feature Interactions (Data Flow & Pipeline Tests)

Validates the integrated lifecycle from raw research staging to LaTeX compilation.

| Test ID | Module | Interaction Flow | Validation Rules |
|---|---|---|---|
| `T3-INT-01` | `test_cross_feature.py` | Ingestion $\rightarrow$ Manifest | `ingest_sources.py` scans `research_sources/` and generates `sources_manifest.json` with valid SHA-256 hashes, file types, and mapped target chapters. |
| `T3-INT-02` | `test_cross_feature.py` | Staged Bib $\rightarrow$ Master Bib | `bib_manager.py --merge` merges `research_sources/citations/*.bib` into master `references.bib`, producing valid BibTeX syntax verifiable by regex/bibtex parser. |
| `T3-INT-03` | `test_cross_feature.py` | Newick String $\rightarrow$ Forest LaTeX | `newick_to_forest.py` converts phylogenetic trees into valid `\begin{forest} ... \end{forest}` LaTeX code with correct node nesting and branch support values. |
| `T3-INT-04` | `test_cross_feature.py` | CSV Data $\rightarrow$ booktabs Table | `format_table.py` transforms `morphometrics.csv` into a publication-ready LaTeX table utilizing `\toprule`, `\midrule`, `\bottomrule`, and `siunitx` alignment. |
| `T3-INT-05` | `test_cross_feature.py` | Nomenclature Validation on LaTeX | `validate_nomenclature.py` inspects chapter drafts, correctly detecting unitalicized binomials (e.g. `Panthera leo`) while approving italicized ones (`\textit{Panthera leo}` or `\taxa{Panthera leo}`). |
| `T3-INT-06` | `test_cross_feature.py` | End-to-End Staging Pipeline | Executes full sequence: Ingest sources $\rightarrow$ Merge citations $\rightarrow$ Format specimen table $\rightarrow$ Verify syntax in modular chapters. |

---

### Tier 4: Real-World Workloads (Full Headless Compilation & Integrity)

Validates the entire dissertation compilation pipeline from master document to publication-ready PDF.

| Test ID | Module | Workload Target | Validation Rules |
|---|---|---|---|
| `T4-E2E-01` | `test_e2e_workload.py` | Headless Compilation Execution | `uv run python build.py` executes successfully on `dissertation.tex` with exit code 0. |
| `T4-E2E-02` | `test_e2e_workload.py` | PDF Artifact Generation | `dissertation.pdf` is generated, has non-zero size (> 10,000 bytes), and begins with valid PDF magic bytes (`%PDF-`). |
| `T4-E2E-03` | `test_e2e_workload.py` | Zero Broken Cross-References | Engine transcript and log contain zero instances of `LaTeX Warning: Reference '...' undefined` or `LaTeX Warning: There were undefined references`. |
| `T4-E2E-04` | `test_e2e_workload.py` | Zero Unresolved Citations | Engine transcript and log contain zero instances of `LaTeX Warning: Citation '...' undefined` or `Citation '...' on page X undefined`. |
| `T4-E2E-05` | `test_e2e_workload.py` | Multi-Pass Cross-Reference Convergence | Aux/TOC generation passes successfully resolve Table of Contents, List of Figures, List of Tables, and Chapter references. |
| `T4-E2E-06` | `test_e2e_workload.py` | Clean Build Flag Support | Executing `build.py --clean` removes temporary auxiliary files (`.aux`, `.bbl`, `.blg`, `.log`, `.out`, `.toc`, `.lof`, `.lot`). |

---

## 3. Feature Inventory Coverage Matrix

Mapping all 24 features from `PROJECT.md` to automated tests:

| Feature # | Feature Name | Milestone | Tier | Primary Test(s) |
|---|---|---|---|---|
| F1 | Research Staging Directory Hierarchy | M1 | Tier 1 | `test_staging.py::test_staging_directories_exist` |
| F2 | Research Staging Onboarding Guide | M1 | Tier 1 | `test_staging.py::test_staging_readme_exists_and_describes_protocol` |
| F3 | Source Manifest Generation Schema | M1 | Tier 1, 3 | `test_staging.py::test_manifest_schema_compliance`, `test_cross_feature.py::test_ingest_sources_manifest_generation` |
| F4 | Skill: `bio-research-sources` | M2 | Tier 1, 3 | `test_skills_schema.py::test_skill_bio_research_sources_frontmatter`, `test_cross_feature.py::test_ingest_sources_cli` |
| F5 | Skill: `bio-nomenclature-ethics` | M2 | Tier 1, 3 | `test_skills_schema.py::test_skill_bio_nomenclature_ethics_frontmatter`, `test_cross_feature.py::test_validate_nomenclature_cli` |
| F6 | Skill: `bio-chapter-builder` | M2 | Tier 1, 3 | `test_skills_schema.py::test_skill_bio_chapter_builder_frontmatter`, `test_cross_feature.py::test_scaffold_dissertation_cli` |
| F7 | Skill: `bio-reference-manager` | M2 | Tier 1, 2, 3 | `test_skills_schema.py::test_skill_bio_reference_manager_frontmatter`, `test_cross_feature.py::test_bib_manager_merge` |
| F8 | Skill: `bio-scientific-formatting` | M2 | Tier 1, 3 | `test_skills_schema.py::test_skill_bio_scientific_formatting_frontmatter`, `test_cross_feature.py::test_newick_to_forest` |
| F9 | Root Document (`dissertation.tex`) | M3 | Tier 1, 4 | `test_latex_structure.py::test_dissertation_root_exists`, `test_e2e_workload.py::test_full_headless_build` |
| F10 | Life Sciences Preamble (`preamble.tex`) | M3 | Tier 1 | `test_latex_structure.py::test_preamble_packages_and_macros` |
| F11 | Modular Frontmatter Components | M3 | Tier 1 | `test_latex_structure.py::test_frontmatter_modules_exist` |
| F12 | Modular Dissertation Chapters | M3 | Tier 1, 4 | `test_latex_structure.py::test_chapters_modules_exist`, `test_e2e_workload.py::test_pdf_content_integrity` |
| F13 | Modular Specimen/Stats Appendices | M3 | Tier 1 | `test_latex_structure.py::test_appendices_modules_exist` |
| F14 | Master Bibliography (`references.bib`) | M3 | Tier 1, 2 | `test_latex_structure.py::test_references_bib_validity`, `test_latex_structure.py::test_no_missing_citation_keys` |
| F15 | Python Packaging (`pyproject.toml`) | M4 | Tier 1 | `test_build_cli.py::test_pyproject_toml_configuration` |
| F16 | Compilation CLI (`build.py`) | M4 | Tier 1, 2 | `test_build_cli.py::test_build_help`, `test_build_cli.py::test_build_cli_options` |
| F17 | Tectonic Auto-Bootstrapping Engine | M4 | Tier 1, 4 | `test_build_cli.py::test_tectonic_binary_discovery_or_download`, `test_e2e_workload.py` |
| F18 | Containerized Docker Fallback | M4 | Tier 1, 2 | `test_build_cli.py::test_docker_fallback_option` |
| F19 | Cross-Reference Diagnostics | M4 | Tier 2, 4 | `test_build_cli.py::test_strict_mode_warning_handling`, `test_e2e_workload.py::test_zero_broken_cross_references` |
| F20 | Git Setup & Configuration | M5 | Tier 1 | Verified via repository metadata (`.gitignore`, commit history) |
| F21 | GitHub Deployment | M5 | Post-M5 | Verified via remote inspection (`git remote -v`) |
| F22 | Diagnostic Suite (`verify.py`) | M6 | Tier 1, 4 | `test_build_cli.py::test_verify_script_execution` |
| F23 | E2E Testing Track | M-E2E | Tiers 1-4 | Complete suite under `tests/` executing via `uv run pytest tests` |
| F24 | Final Acceptance & Forensic Audit | M-FINAL | Tiers 1-4 | Full green test run across all tiers with zero warnings |

---

## 4. Test Execution Architecture

### Test Runner Invocation
Tests are executed using `pytest` orchestrated by `uv`:

```bash
# Execute entire 4-tier test suite
uv run pytest tests -v

# Execute specific tiers
uv run pytest tests/test_skills_schema.py tests/test_staging.py -v       # Tier 1 & 2 (Skills & Staging)
uv run pytest tests/test_latex_structure.py tests/test_build_cli.py -v   # Tier 1 & 2 (LaTeX & Build CLI)
uv run pytest tests/test_cross_feature.py -v                             # Tier 3 (Cross-Feature)
uv run pytest tests/test_e2e_workload.py -v                              # Tier 4 (Real-World E2E)

# Standalone execution without pytest
uv run python -m unittest discover -s tests -p "test_*.py"
```

### Test Directory Layout
```text
tests/
├── conftest.py                # Pytest configuration, fixtures, paths, helper validators
├── test_skills_schema.py      # Tier 1 & 2: Antigravity skill YAML frontmatter & scripts
├── test_staging.py            # Tier 1 & 2: Research staging hierarchy, onboarding, sample files
├── test_latex_structure.py    # Tier 1 & 2: Modular LaTeX documents, preamble macros, .bib keys
├── test_build_cli.py          # Tier 1 & 2: build.py CLI options, engine flags, --strict mode
├── test_cross_feature.py      # Tier 3: Ingestion -> Manifest -> BibTeX merge -> Chapter synthesis
└── test_e2e_workload.py       # Tier 4: Headless PDF compilation, non-zero PDF, zero broken refs
```

---

## 5. Exit Criteria & Quality Gates

A release is marked `TEST_READY` when:
1. **100% Pass Rate**: Every test in Tiers 1 through 4 passes without failure.
2. **Strict Verification**: Headless compilation produces `dissertation.pdf` exceeding 10 KB with valid PDF magic bytes.
3. **Zero Diagnostic Broken References**: No undefined citation (`[?]`) or reference (`??`) warnings in the final compilation log.
4. **Skill Conformance**: All 5 skills pass YAML frontmatter parsing, directory structure validation, and CLI `--help` checks.
5. **Hermetic Test Integrity**: No tests leave dangling temporary files outside `tmp_path` or alter the production git state.
