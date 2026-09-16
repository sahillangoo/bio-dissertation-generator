# Life Sciences Dissertation Structural Architecture

This document defines the formal modular architecture for Ph.D. and Master's theses in Biology and Zoology.

---

## 1. Modular Directory Organization

```text
dissertation_root/
├── dissertation.tex          # Master LaTeX root compiling all modular components
├── preamble.tex              # Global packages, macros, SI units, and ICZN styles
├── references.bib            # Master BibLaTeX bibliography database
├── frontmatter/
│   ├── title.tex             # Institutional title page
│   ├── abstract.tex          # 250-350 word structured abstract
│   ├── dedication.tex        # Dedication statement
│   ├── acknowledgements.tex  # Funding, advisor, and committee acknowledgements
│   ├── abbreviations.tex     # List of biological and statistical acronyms
│   └── ethics_statement.tex  # Mandatory IACUC and collecting permit statement
├── chapters/
│   ├── 01_introduction.tex   # Background, knowledge gaps, study system, hypotheses
│   ├── 02_lit_review.tex     # Thematic literature review and historical paradigms
│   ├── 03_methods.tex        # Sampling, morphometrics, molecular assays, software pipelines
│   ├── 04_results.tex        # Phylogenies, morphometric tests, PCA, statistical tables
│   └── 05_discussion.tex     # Biological synthesis, hypothesis testing, future directions
└── appendices/
    ├── appendix_a_specimens.tex # Museum voucher catalog with GPS and accessions
    ├── appendix_b_primers.tex   # Sanger sequencing primers and cycling conditions
    └── appendix_c_stats.tex     # Complete MANOVA tables and factor loadings
```

---

## 2. Word Count Budgets & Length Guidelines

| Dissertation Component | Master's Thesis (M.S.) | Doctoral Dissertation (Ph.D.) |
|---|---|---|
| **Abstract** | 250–350 words | 300–450 words |
| **Chapter 1 (Introduction)** | 3,000–5,000 words | 5,000–8,000 words |
| **Chapter 2 (Lit Review)** | 4,000–6,000 words | 8,000–12,000 words |
| **Chapter 3 (Methods)** | 3,000–5,000 words | 5,000–8,000 words |
| **Chapter 4 (Results)** | 4,000–7,000 words | 6,000–10,000 words |
| **Chapter 5 (Discussion)** | 4,000–6,000 words | 6,000–10,000 words |
| **Appendices & Catalogs** | As needed | Comprehensive museum voucher lists |

---

## 3. Cross-Referencing Conventions

Maintain strict label naming schemes to guarantee zero undefined cross-references:
- Chapters: `\label{ch:introduction}`, `\label{ch:methods}`
- Sections: `\label{sec:methods_molecular}`, `\label{sec:results_phylogeny}`
- Figures: `\label{fig:phylogeny_mcmc}`, `\label{fig:pca_morphometrics}`
- Tables: `\label{tab:morphometric_summary}`, `\label{tab:primers_used}`
- Appendices: `\label{app:specimens}`, `\label{app:primers}`
