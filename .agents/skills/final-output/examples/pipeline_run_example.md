# Example: Running the Final Output Dissertation Pipeline

This example demonstrates executing the complete 7-stage pipeline.

## Execution Command

```bash
uv run python pipeline.py --all
```

## Example Console Output

```text
================================================================================
             BIOLOGY & ZOOLOGY DISSERTATION MASTER PIPELINE                     
================================================================================
Executing 7-stage dissertation workflow...

[STAGE 1/7] Staging & Literature Ingestion...
  • Ingesting research_sources/ -> pipeline_outputs/sources_manifest.json
  • Indexed 6 source files across existing_work, papers, citations, notes.
  ✔ Stage 1 completed successfully.

[STAGE 2/7] Biology Logic & Nomenclature Verification...
  • Auditing taxon macros and ethics notes...
  • Binomials verified; in-vitro plant work has no IACUC chapter.
  ✔ Stage 2 completed successfully.

[STAGE 3/7] Chapter Structure & Drafting Validation...
  • Validating 7 chapters, 6 frontmatter files, and 1 appendix...
  • All modular components present; zero broken section labels.
  ✔ Stage 3 completed successfully.

[STAGE 4/7] Citation & Reference Integrity Audit...
  • Resolving cited keys against master references.bib...
  • 18/18 cited keys resolved (100% resolution rate).
  ✔ Stage 4 completed successfully.

[STAGE 5/7] Reviewer 2 Adversarial Review Audit...
  • Simulating adversarial peer review on manuscript...
  • Generated pipeline_outputs/reviewer2_audit.md.
  ✔ Stage 5 completed successfully.

[STAGE 6/7] De-AI & Stylistic Humanizer Scan...
  • Scanning prose for AI tells, clichés, and style tightening opportunities...
  • Generated pipeline_outputs/de_ai_humanizer_report.md.
  ✔ Stage 6 completed successfully.

[STAGE 7/7] Final Headless Dissertation Build & Verification...
  • Compiling dissertation.tex -> dissertation.pdf via Tectonic...
  • Zero undefined citations ([?]); Zero broken references (??).
  ✔ Stage 7 completed successfully: dissertation.pdf (165.51 KB).

================================================================================
                  PIPELINE EXECUTION SUMMARY: ALL STAGES PASSED                 
================================================================================
Deliverables:
  - dissertation.pdf (Publication-Ready PDF)
  - pipeline_outputs/pipeline_state.json
  - pipeline_outputs/reviewer2_audit.md
  - pipeline_outputs/de_ai_humanizer_report.md
  - pipeline_outputs/sources_manifest.json
  - pipeline_outputs/final_verification_report.json
================================================================================
```
