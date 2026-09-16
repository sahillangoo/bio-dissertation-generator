# Language-register audit

Scored against [`.agents/skills/bio-chapter-builder/references/language_register_scale.md`](../.agents/skills/bio-chapter-builder/references/language_register_scale.md).

**Target:** Band 2–3 (clear / standard scientific English). Hygiene must pass in scientific chapters.

**Build:** `uv run python build.py --strict` on 2026-09-17. Exit 0. Zero undefined citations, zero broken references. PDF: `dissertation.pdf`.

---

## Per-chapter scores

Dimensions: Voice, Lexicon, Syntax, Epistemic caution (1–5). Hygiene is pass/fail.

| File | Voice | Lexicon | Syntax | Epistemic | Hygiene | Overall | Notes |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `frontmatter/abstract.tex` | 3 | 2 | 2 | 3 | pass | **2** | Short sentences; MIC limit stated. |
| `chapters/01_introduction.tex` | 3 | 3 | 2 | 3 | pass | **3** | Botanical profile rewritten from Band 4–5. Technical names kept. |
| `chapters/02_objectives.tex` | 3 | 2 | 2 | 3 | pass | **2** | Scope and non-claims unchanged. |
| `chapters/03_lit_review.tex` | 3 | 3 | 2 | 3 | pass | **3** | Dense envelope, phytochemistry, and pathogen sections shortened. Compound lists and published numbers kept. |
| `chapters/04_methods.tex` | 3 | 2 | 2 | 4 | pass | **3** | Missing details still omitted rather than invented. |
| `chapters/05_results.tex` | 3 | 2 | 2 | 3 | pass | **2** | Tables and numbers unchanged. |
| `chapters/06_discussion.tex` | 3 | 2 | 2 | 4 | pass | **3** | Long *P. aeruginosa* sentence split; “ledger” wording removed. |
| `chapters/07_conclusion.tex` | 3 | 2 | 2 | 3 | pass | **2** | Claim limits unchanged. |
| `appendices/appendix_a_template.tex` | 3 | 2 | 2 | 3 | pass | **2** | Raw tables only. |
| `frontmatter/acknowledgements.tex` | 1 | 2 | 2 | — | n/a | genre | First person kept (conventional). Stacked praise trimmed. |

Title, certificate, and declaration were not rewritten (institutional wording).

---

## Locked facts checked after rewrite

Unchanged: yield 24.13\% (w/w); C1/C2 zone means and SDs; gentamicin and water controls; Drakhshaan et al. DCM/MeOH zones and MIC range; HPLC markers (rutin 68.66, reserpine 53.76, ferulic acid 31.64 µg/mg); collection coordinates; citations; no MIC, no clinical efficacy, indexed gap not a “first report”.

---

## Result

All scientific chapters sit in Band 2–3 with hygiene pass. The Clinical Empiricist Protocol remains Band 5 on the scale and is not the writing target.
