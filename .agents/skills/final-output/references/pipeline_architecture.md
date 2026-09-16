# Final Output: Dissertation Pipeline Architecture

This document defines the 7-stage architecture, data contracts, and error recovery policies for the Biology & Zoology Dissertation Pipeline.

## Pipeline Lifecycle

```text
[research_sources/] 
       │
       ▼
[Stage 1: Staging & Literature Discovery] ────► pipeline_outputs/sources_manifest.json
       │
       ▼
[Stage 2: Biology Logic & Nomenclature]   ────► pipeline_outputs/biology_logic_audit.json
       │
       ▼
[Stage 3: Chapter Structure & Drafting]   ────► pipeline_outputs/drafting_status.json
       │
       ▼
[Stage 4: Citation & Reference Audit]     ────► pipeline_outputs/citation_verification.json
       │
       ▼
[Stage 5: Reviewer 2 Adversarial Review]  ────► pipeline_outputs/reviewer2_audit.md
       │
       ▼
[Stage 6: De-AI & Stylistic Humanizer]    ────► pipeline_outputs/de_ai_humanizer_report.md
       │
       ▼
[Stage 7: Final Tectonic Build]           ────► dissertation.pdf & final_verification_report.json
```

## Stage Specifications

### Stage 1: `staging`
- **Purpose**: Discovers and indexes student materials in `research_sources/`, and catalogs the six dissertation skills.
- **Tools**: `bio-research-sources/scripts/ingest_sources.py`, `pipeline.py --audit-skills`.
- **Output**: `pipeline_outputs/sources_manifest.json`, `pipeline_outputs/skills_inventory.json`, `pipeline_outputs/skills_inventory.md`.
- **Criteria**: All files categorized with valid SHA-256, target chapter mapping, 0 duplicate skills detected.

### Stage 2: `biology_logic`
- **Purpose**: Enforces taxonomic nomenclature macros, authority citations, holotype voucher citations, and ethics notes.
- **Tools**: `bio-nomenclature-ethics/scripts/validate_nomenclature.py`.
- **Output**: `pipeline_outputs/biology_logic_audit.json`.
- **Criteria**: Zero invalid binomials, proper italicization; missing IACUC is allowed for in-vitro plant work.

### Stage 3: `chapter_drafting`
- **Purpose**: Validates Kashmir M.Sc. frontmatter, seven chapters, and the live appendix.
- **Tools**: `bio-chapter-builder`.
- **Output**: `pipeline_outputs/drafting_status.json`.
- **Criteria**: All modular components present, valid label conventions (`ch:`, `sec:`, `fig:`, `tab:`, `app:`).

### Stage 4: `citation_audit`
- **Purpose**: Verifies all cited keys in live LaTeX files resolve to entries in `references.bib`.
- **Tools**: `bio-reference-manager/scripts/bib_manager.py`.
- **Output**: `pipeline_outputs/citation_verification.json`.
- **Criteria**: 100% cited keys resolved, zero duplicate citation keys.

### Stage 5: `adversarial_review`
- **Purpose**: Audits claims, sample-size justification, statistical rigor, and alternative hypotheses.
- **Tools**: Pipeline heuristics in `pipeline.py`.
- **Output**: `pipeline_outputs/reviewer2_audit.md`.
- **Criteria**: Report covers Title, Abstract, Introduction, Methods, Results, and Discussion.

### Stage 6: `de_ai_humanizer`
- **Purpose**: Scans text for AI writing patterns (inflated symbols, rule-of-three, copula overuse, repetitive sentence rhythms).
- **Tools**: Pipeline heuristics in `pipeline.py`.
- **Output**: `pipeline_outputs/de_ai_humanizer_report.md`.
- **Criteria**: Style tightening suggestions and human voice score.

### Stage 7: `final_build`
- **Purpose**: Executes automated multi-pass compilation via Tectonic and zero-broken-cross-reference diagnostics.
- **Tools**: `build.py`, `verify.py`.
- **Output**: `dissertation.pdf` (>100 KB), `pipeline_outputs/final_verification_report.json`.
- **Criteria**: 0 fatal LaTeX errors, 0 undefined citations (`[?]`), 0 broken cross-references (`??`).
