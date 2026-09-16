# Student Research Sources & Existing Work Staging

Welcome to the **Research Sources Staging Hub** for the Biology & Zoology Dissertation Suite. This directory serves as the structured staging environment where graduate students (Master's and Ph.D.) place preliminary drafts, literature summaries, citation databases, datasets, and committee notes. Autonomous AI agents and writing skills automatically discover, index, parse, and synthesize content staged here into publication-ready LaTeX dissertation chapters and bibliographies.

---

## Directory Organization

```text
research_sources/
├── README.md                 # This onboarding guide and agent protocol specification
├── sources_manifest.json     # Automatically generated manifest indexing all staged sources
├── existing_work/            # Preliminary drafts, thesis sections, lab write-ups, datasets
│   ├── .gitkeep              # Keep-alive for version control
│   ├── methods_draft.md      # Sample: Draft text for Materials & Methods
│   └── morphometrics.csv     # Sample: Tabular morphological measurements
├── papers/                   # Literature notes, annotated bibliographies, paper summaries
│   ├── .gitkeep
│   ├── literature_notes.md   # Sample: Literature review matrix and summary notes
│   └── smith2021_notes.md    # Sample: Targeted critique of key phylogenetic reference
├── citations/                # Bibliographic exports and custom BibTeX files
│   ├── .gitkeep
│   └── student_citations.bib # Sample: Valid BibTeX entries ready for synthesis into references.bib
└── notes/                    # Advisory committee feedback, outlines, hypotheses, field notes
    ├── .gitkeep
    └── committee_notes.md    # Sample: Committee recommendations and hypothesis tracking
```

---

## Staging Guide by Subdirectory

### 1. Existing Work (`research_sources/existing_work/`)
Place any material you have authored prior to or during your degree that belongs in the dissertation.
- **Accepted Formats**: Markdown (`.md`), Plain Text (`.txt`), LaTeX (`.tex`), Word (`.docx`), Delimited Data (`.csv`, `.tsv`).
- **Typical Contents**:
  - Preliminary chapter drafts (e.g., introduction, field protocols, experimental procedures).
  - Morphometric measurement sheets, specimen catalogs, ecological survey counts.
  - Molecular assay protocols (PCR primer lists, thermocycling profiles, sequence alignment pipelines).
- **Target Ingestion**:
  - Textual drafts are synthesized into `chapters/01_introduction.tex`, `chapters/03_methods.tex`, etc.
  - Tabular data (`.csv`, `.tsv`) are converted into publication-standard `booktabs` + `siunitx` tables in `chapters/` or `appendices/`.

### 2. Literature & Papers (`research_sources/papers/`)
Place reference material, literature review summaries, and reading notes.
- **Accepted Formats**: Markdown (`.md`), Plain Text (`.txt`), PDF reading notes (`.pdf`, `.md`).
- **Typical Contents**:
  - Summaries of seminal monographs, phylogenetic revisions, and ecological papers.
  - Synthesis tables comparing conflicting phylogenetic hypotheses or divergence dates.
  - Notes on study system biology, geographic distribution, and natural history.
- **Target Ingestion**:
  - Synthesized into `chapters/02_lit_review.tex` and the contextual discussion in `chapters/05_discussion.tex`.

### 3. Citations & Bibliographies (`research_sources/citations/`)
Stage citation databases exported from reference managers (Zotero, Mendeley, EndNote, Paperpile).
- **Accepted Formats**: BibTeX (`.bib`), DOI lists (`.txt`).
- **Requirements**:
  - Must contain valid BibTeX syntax with unique citation keys (e.g., `AuthorYearKeyword`).
  - Standard fields: `author`, `title`, `journal` / `booktitle`, `year`, `volume`, `number`, `pages`, `doi`.
- **Target Ingestion**:
  - Ingested by the `bio-reference-manager` skill (`bib_manager.py`).
  - Automatically deduplicated, validated, and merged into the root `references.bib` document.

### 4. Notes & Committee Feedback (`research_sources/notes/`)
Store informal guidance, committee advice, and conceptual frameworks.
- **Accepted Formats**: Markdown (`.md`), Text (`.txt`).
- **Typical Contents**:
  - Committee meeting minutes, advisor comments, and dissertation defense requirements.
  - Explicit list of research questions, null/alternative hypotheses ($H_0, H_1, H_2$), and predictions.
  - Institutional protocol numbers (IACUC approval numbers, wildlife collection permits, CITES permits).
- **Target Ingestion**:
  - The `bio-chapter-builder` and `bio-nomenclature-ethics` skills consult these notes to ensure compliance with committee expectations and regulatory mandates.

---

## Agent Ingestion Protocol

Autonomous agents operating on this repository adhere to the following workflow:

1. **Discovery & Indexing**:
   Run the `bio-research-sources` ingestion script to scan all staging folders:
   ```bash
   uv run python .agents/skills/bio-research-sources/scripts/ingest_sources.py \
       --sources research_sources/ \
       --output research_sources/sources_manifest.json
   ```
2. **Manifest Verification**:
   The generated `sources_manifest.json` tracks file paths, cryptographic SHA-256 hashes, file types, word/row counts, and inferred chapter targets.
3. **Synthesis & Attribution**:
   - Every claim, method, or dataset ingested from `research_sources/` is tagged with an inline LaTeX comment indicating provenance:
     ```latex
     % [Source: research_sources/existing_work/methods_draft.md, Section: DNA Extraction]
     ```
   - No bibliographic citation is invented. Agents match literature claims exclusively to verified BibTeX keys in `references.bib` or fetch verified DOIs via PubMed/bioRxiv.
4. **Preservation of Gitkeep**:
   Never delete `.gitkeep` files, ensuring empty directory structures remain tracked in version control.
