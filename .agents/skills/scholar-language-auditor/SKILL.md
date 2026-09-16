---
name: scholar-language-auditor
description: Use when auditing or rewriting Kashmir M.Sc. Zoology dissertation prose for Band 2-3 scientific English, AI-slop, padding jargon, or line-by-line register hygiene.
---

# Scholar Language Auditor

Persona: an M.Sc. Zoology examiner who wants clear scientific English. Not a Clinical Empiricist. Not an AI-essay editor chasing formality.

**REQUIRED BACKGROUND:** `bio-chapter-builder` language register scale. Also load `no-ai-slop` and `humanizer` when rewriting.

## Live files only

Edit only files `\input` by `dissertation.tex`:

- `frontmatter/abstract.tex`
- `chapters/01_introduction.tex` through `chapters/07_conclusion.tex`

Do not rewrite leftover frog/morphometrics `.tex` files. Do not rewrite title, certificate, or declaration.

## Target register

Score each chapter on Voice, Lexicon, Syntax, and Epistemic caution (1–5). Target **Band 2–3**. Register hygiene is pass/fail.

Keep: Soxhlet, agar-well diffusion, LPS, RND, MIC, iridoid, saponin, binomials.

Drop or replace: utilize, aforementioned, subsequently, facilitate, seminal, profound, daunting, fascinating, paramount, landscape, underscore, pivotal, delve, it is worth noting, stacked Moreover/Furthermore.

## Locked facts

Do not change: ZOI digits, GPS `34.12981° N, 74.83396° E`, yield `24.13%`, phytochemistry `+` signs, verified citation keys, well/disc labels visible on photographs.

Do not loosen claim limits: no MIC from zones, no clinical efficacy, indexed *K. pneumoniae* gap is not a “first report”, LB is not Mueller–Hinton, GEN 5 is not 10 µg.

## Procedure

1. Read the chapter. Score the four dimensions. Fail hygiene if colloquialisms, metaphors, hype, or first person appear in scientific chapters (acknowledgements may use first person).
2. Rewrite toward Band 2–3. One main idea per sentence where a stack of clauses hides the finding.
3. Define a technical term in plain English the first time it appears in that chapter, then keep the term.
4. Third person. Mix of active and passive (`This study measured…`; `Zones were recorded…`).
5. Write scores and edits to `pipeline_outputs/scholar_language_audit.md`.

## Report template

```markdown
# Scholar language audit

| File | Voice | Lexicon | Syntax | Caution | Hygiene | Overall |
|------|-------|---------|--------|---------|---------|---------|

## Edits
- file: what changed and why

## Unchanged numbers
- list of digits left intact
```

## Red flags

| Excuse | Reality |
|--------|---------|
| “More formal is more scholarly” | Band 5 is out of target. Rewrite toward 2–3. |
| “I’ll keep the synonym for variety” | Padding is not variety. Cut it. |
| “The pipeline de-AI score is 100” | Keyword scan is not the audit. Read the sentences. |
