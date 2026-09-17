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

## 2026-09-17T07:06:18Z

Enrich the Kashmir M.Sc. Zoology dissertation manuscript by integrating chemical, mechanistic, and taxonomic depth (triterpenoid saponins, iridoids, APG IV classification, and Gram-negative RND efflux dynamics) into Chapters 2 and 5, while resolving test suite assertion mismatches and updating the evaluation pipeline.

Working directory: d:/sandbox/work-box/dissertation-skills
Integrity mode: development
Requested team: Full multi-agent team (specialized across scientific drafting, bibliography management, test suite maintenance, and adversarial review)

## Requirements

### R1. Manuscript Scientific & Mechanistic Enrichment
Enrich Chapter 2 (Literature Review) and Chapter 5 (Discussion) with deeper phytochemical and molecular context:
- Incorporate verified Dipsacus triterpenoid saponin (e.g. dipsacoside B, asperosaponin VI) and iridoid glucoside (cantleyoside, loganin, sweroside) profiles from published chemical literature.
- Deepen the mechanistic discussion of the Pseudomonas aeruginosa C1 > C2 zone inversion, expanding on RND tripartite efflux complexes (MexAB-OprM) and outer-membrane porin constraints (OprF).
- Maintain Band 2–3 scholarly English register, third-person objective voice, and zero AI-slop keywords (delve, tapestry, pivotal, paramount, moreover, furthermore).
- Strictly preserve all locked empirical laboratory values (ZOI replicates, means, standard deviations, 24.13% yield, coordinates 34.12981° N, 74.83396° E).
- Retain honest disclaimers for unrecorded candidate metadata (voucher accession, strain IDs, well volume, collection month).

### R2. Test Suite & Build Verification Remediation
Align repository diagnostic tests and compilation scripts with current workspace architecture:
- Update tests/test_pipeline_cli.py to reflect the 9 active skill suites in .agents/skills.
- Resolve test suite failures in tests/test_agent_definitions.py to ensure consistency with active agent definitions.
- Ensure build.py and verify.py pass cleanly under --strict mode without intermediate compiler warning false-positives.

### R3. Pipeline Output & Dossier Synchronization
Execute the complete end-to-end dissertation pipeline (pipeline.py --all) to regenerate all audit artifacts in pipeline_outputs/ (Reviewer 2 audit, scholar language audit, checker report, and final verification report) and compile synchronized dissertation.pdf and dissertation.docx deliverables.

## Acceptance Criteria

### Scientific Integrity & Numerical Exactness
- [ ] All ZOI means, SDs, and replicates in chapters/04_results.tex and appendices/appendix_a_zoi.tex match research_sources/existing_work/Antibacterial Efficacy Results - Zone of Inhibition.md exactly.
- [ ] Zero undefined citations ([?]) and zero broken cross-references (??) across all .tex modules.
- [ ] Zero occurrences of prohibited buzzwords (delve, tapestry, pivotal, paramount, moreover, furthermore, utilize, aforementioned) in scientific chapters.

### Test Suite Execution
- [ ] uv run python -m pytest tests/test_latex_structure.py tests/test_staging.py tests/test_docx_export.py tests/test_cross_feature.py tests/test_build_cli.py tests/test_skills_schema.py tests/test_verify_cli.py tests/test_e2e_workload.py tests/test_pipeline_cli.py -q passes with 0 failures.
- [ ] uv run python verify.py exits with status code 0 across all passes.

### Artifact Deliverables
- [ ] dissertation.pdf is generated as a valid, non-empty PDF document (>10 MB, 41+ pages).
- [ ] dissertation.docx is generated as a valid OOXML document conforming to thesis styling (Times New Roman, A4, 1.25" margins, 1.5 spacing).
- [ ] pipeline_outputs/ contains updated and consistent reports for all 7 pipeline stages.
