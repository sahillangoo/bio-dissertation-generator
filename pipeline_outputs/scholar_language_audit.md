# Scholar language audit

| File | Voice | Lexicon | Syntax | Caution | Hygiene | Overall |
|------|-------|---------|--------|---------|---------|---------|
| frontmatter/abstract.tex | 3 | 3 | 2 | 3 | PASS | Band 3 |
| chapters/01_introduction.tex | 3 | 3 | 3 | 3 | PASS | Band 3 |
| chapters/02_lit_review.tex | 3 | 3 | 3 | 3 | PASS | Band 3 |
| chapters/03_methods.tex | 3 | 2 | 2 | 3 | PASS | Band 2–3 |
| chapters/04_results.tex | 3 | 2 | 2 | 3 | PASS | Band 2 |
| chapters/05_discussion.tex | 3 | 3 | 3 | 3 | PASS | Band 3 |
| chapters/06_conclusion.tex | 3 | 3 | 2 | 3 | PASS | Band 3 |

Live `\input` files only. Acknowledgements remain first person. Scientific chapters stay third person, British spelling, Band 2–3.

## This pass (AI-slop / humanizer)

- Skills used: `scholar-language-auditor` (sentence read) and pipeline stage `de_ai_humanizer` (keyword scan). Standalone `no-ai-slop` / `humanizer` folders are not in the live `.agents/skills/` set.
- Keyword scan: **0** hits in live chapters and abstract for delve, tapestry, pivotal, paramount, moreover, furthermore, utilize, aforementioned, seminal, profound, shed light, it is worth noting, IN VITRO-style hype.
- One leftover frog file (`frontmatter/ethics_statement.tex`) contains “subsequently”; it is **not** `\input` and was not rewritten.
- “Taken together” appears once in the national synthesis of Chapter 2. That is ordinary scientific English, not a stacked Moreover/Furthermore opener. Left as written.
- **Rewrite: skipped.** The live dissertation is already aligned.

## Edits this pass
- none

## Unchanged numbers
- ZOI means, SDs, Appendix A replicates
- GPS 34.12981° N, 74.83396° E
- Yield 24.13% (w/w)
- C1 50 mg/mL, C2 100 mg/mL
- Phytochemical + scores
- GEN 5 = 5 µg
