---
name: dissertation-checker
description: Use when examining the finished Kashmir M.Sc. Dipsacus inermis dissertation for claim-data mismatches, figure caption errors, table/chart layout, broken citations, or leftover template content before PDF finalization.
---

# Dissertation Checker

Persona: internal examiner plus copy editor. Fix what is wrong in `.tex`. Note what only the candidate can supply.

**REQUIRED BACKGROUND:** `academic-paper-reviewer`, `adversarial-review`, `bio-nomenclature-ethics`, `bio-reference-manager`, `bio-scientific-formatting`.

## Source of truth

- Laboratory table: `research_sources/existing_work/Antibacterial Efficacy Results - Zone of Inhibition.md`
- Collection coordinates: `34.12981° N, 74.83396° E` (state as Botanical Garden locality; do not mention the filename)
- Live root: `dissertation.tex` inputs only

## Check order

1. Every ZOI mean, SD, and replicate matches the laboratory file.
2. Literature comparison table includes aqueous C2 and Drakhshaan DCM/MeOH at both 50 and 100 µg mL⁻¹ when those numbers exist in the source extract.
3. Figure captions name only what is visible (organism on the lid, C1/C2/N/GEN 5). Unlabelled plates stay unlabelled.
4. No ChatGPT, WhatsApp, or “filename” wording in captions.
5. No invented Fig. 8c for *P. aeruginosa*. No ATCC, MIC, ANOVA, or `wani2017`.
6. Binomials italic; genus spelled out at sentence start.
7. Every `\cite` / `\citep` / `\citet` key exists in `references.bib`.
8. Tables use booktabs; numeric columns align; the ZOI chart has SD error bars and fits `\textwidth`.
9. Leftover frog chapters are not `\input`.
10. Compile notes: broken refs (`??`), undefined cites (`[?]`), overflow.

## Fix vs note

**Fix** in `.tex`: wrong digit vs laboratory file, overflow table, caption that names an unlabelled organism, Band 4–5 padding missed by the scholar pass, missing DCM/MeOH 50 µg rows, GPS phrased as “from the filename”.

**Note only:** missing lab-assistant names, missing voucher, missing ATCC, missing *P. aeruginosa* species-labelled inhibition plate, acknowledgements that stay generic.

## Output

Write `pipeline_outputs/dissertation_checker_report.md`:

```markdown
# Dissertation checker report

## Verdict
PASS | REVISE

## Majors fixed
## Majors noted (candidate)
## Layout
## Citations
## Nomenclature
```

Then run:

```bash
uv run python pipeline.py --all
uv run python verify.py
uv run python -m pytest tests/test_latex_structure.py tests/test_pipeline_cli.py tests/test_skills_schema.py -q
```
