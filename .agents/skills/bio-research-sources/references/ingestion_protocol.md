# Source Ingestion Protocol for Life Sciences Dissertations

This protocol establishes the formal methodology for autonomous agents discovering, parsing, and incorporating student research materials into modular LaTeX dissertations.

---

## 1. Directory Structure and Taxonomy

All student files reside under `research_sources/`:
- **`existing_work/`**: Student drafts, lab protocols, DNA extraction protocols, morphometric sheets (`.md`, `.txt`, `.docx`, `.tex`, `.csv`, `.tsv`).
- **`papers/`**: Reading notes, annotated bibliographies, PDF summaries (`.md`, `.txt`, `.pdf`).
- **`citations/`**: BibTeX databases (`.bib`) exported from Zotero, Mendeley, or EndNote.
- **`notes/`**: Advisor guidance, committee minutes, research hypotheses, institutional approvals (`.md`, `.txt`).

---

## 2. Ingestion Workflow

```text
[research_sources/] ---> [ingest_sources.py] ---> [sources_manifest.json]
                                                      |
                    +---------------------------------+---------------------------------+
                    |                                 |                                 |
           [Textual Drafts]                    [Tabular Data]                   [Citations]
                    |                                 |                                 |
         Synthesized into Chapters          Converted to LaTeX Tables       Merged into references.bib
         (Intro, Methods, Discussion)         (booktabs + siunitx)            via bib_manager.py
```

### Step 1: Scan and Manifest Generation
The agent triggers `ingest_sources.py`:
```bash
uv run python .agents/skills/bio-research-sources/scripts/ingest_sources.py --sources research_sources/ --output research_sources/sources_manifest.json
```
This produces a cryptographically validated manifest mapping each file's SHA-256 digest, category, and inferred destination chapter.

### Step 2: Content Parsing & Heading Extraction
- **Markdown / Plain Text**: Headings (`#`, `##`, `###`) delineate sub-sections (e.g. "Taxonomic Sampling", "PCR Amplification").
- **CSV / TSV**: Header row identifies column names and units. Data rows are summarized or transformed using `format_table.py`.
- **BibTeX**: Citation keys are harvested and cross-referenced with chapter citations.

### Step 3: Attribution & Provenance
To ensure academic honesty and traceability:
- Every section incorporating student draft material must begin with an inline LaTeX comment:
  ```latex
  % [Source: research_sources/existing_work/methods_draft.md, Section: DNA Extraction]
  ```
- Any scientific claim originating from literature must cite a valid key in `references.bib` (never invent fake citations).

---

## 3. Handling Conflicting Information

When student notes or drafts conflict with existing template text or external literature:
1. **Research Direction & Hypotheses**: User notes (`research_sources/notes/`) are strictly authoritative.
2. **Empirical Data**: Data in `existing_work/` takes precedence over general literature averages.
3. **Nomenclature & Citations**: Scientific naming must still obey ICZN rules and BibLaTeX formatting standards.
