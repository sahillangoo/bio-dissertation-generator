# Original User Request

## 2026-09-16T12:40:25Z

A specialized dissertation skill suite and automated LaTeX dissertation generator for Master's and PhD students in Biology and Zoology, providing modular thesis scaffolding, user source ingestion, research/writing skills, and an automated LaTeX-to-PDF compilation pipeline.

Working directory: d:\sandbox\work-box\dissertation-skills
Integrity mode: development

## Requirements

### R1. Biology & Zoology Dissertation Skills Suite
Create and register Antigravity-compatible skills in `.agents/skills/` tailored for Life Sciences (Biology & Zoology) academic research and dissertation authoring:
- Source ingestion & literature synthesis (actively processing user drafts, papers, and notes from `research_sources/`, integrating with PubMed, bioRxiv, and NCBI).
- Zoological/biological nomenclature (ICZN standards, binomial taxon formatting) and ethical guidelines (IACUC / animal care statements).
- Modular dissertation chapter planning and drafting (Introduction, Literature Review, Materials & Methods, Results, Discussion, Specimen Appendices).
- Reference management using BibLaTeX (CSE, APA, and journal-standard life-sciences citation styles).
- Scientific formatting support for phylogenetic trees, anatomical tables, specimen catalogs, and statistical reporting.

### R2. User Research Sources & Existing Work Staging Integration
Integrate the dedicated `research_sources/` staging structure (`existing_work/`, `papers/`, `citations/`, `notes/`) so agents can easily discover, ingest, and synthesize the student's existing drafts, reference papers, and custom citations into the thesis document and bibliography.

### R3. Modular LaTeX Dissertation Template & Automated Compilation Engine
Provide a clean, modular academic dissertation template using standard LaTeX classes and BibLaTeX. Python tooling and dependencies must be managed using `uv` (with `pyproject.toml`). Implement a robust cross-platform compilation CLI (`uv run python build.py` or `uv run dissertation-build`) that aggregates modular chapters, manages bibliography passes, and produces a publication-ready PDF using Tectonic (auto-fetching packages on demand), with Docker fallback.

### R4. Git Initialization & GitHub Public Repository
Initialize git version control in the workspace with an academic LaTeX/Python `.gitignore`, create a public repository named `bio-dissertation-generator` on GitHub under the user's profile (`sahillangoo`), and push the initial codebase.

### R5. Automated Verification & Diagnostic Suite
Include a test/verification script that validates all skill YAML metadata schemas, checks source folder ingestion, and executes an end-to-end headless PDF build of the dissertation template to verify zero compilation errors.

## Acceptance Criteria

### Source Staging & Ingestion
- [ ] `research_sources/` directory contains organized subdirectories (`existing_work/`, `papers/`, `citations/`, `notes/`) and guiding documentation for agent consumption.
- [ ] The writing and citation skills include explicit workflows to read from `research_sources/` and incorporate user-provided content.

### Skill Compliance
- [ ] Every skill directory under `.agents/skills/` contains a valid `SKILL.md` with compliant YAML frontmatter (`name`, `description`) and structured instructions.
- [ ] Running a skill verification check confirms all declared skills are parseable and ready for progressive disclosure.

### Dissertation Template & PDF Build
- [ ] The dissertation template includes modular chapter files (`frontmatter`, `intro`, `methods`, `results`, `discussion`, `appendices`, `references.bib`).
- [ ] Executing `uv run python build.py` compiles the dissertation and generates a valid `dissertation.pdf` file with non-zero size.
- [ ] The generated PDF includes compiled front matter, structured chapters, rendered bibliography entries, and table of contents without broken cross-references.

### Git & Remote Repository
- [ ] Git repository is initialized with a clean commit history.
- [ ] Remote `origin` points to `https://github.com/sahillangoo/bio-dissertation-generator`.
- [ ] Repository is pushed to GitHub as a public repository.
