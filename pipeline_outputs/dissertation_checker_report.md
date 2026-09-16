# Dissertation checker report

**Date:** 2026-09-17  
**Persona:** internal examiner + copy editor  
**Live root:** `dissertation.tex` (Kashmir M.Sc. sequence only)

## Verdict
PASS

## Majors fixed
- Laboratory ZOI means, SD, and R1–R3 values in Chapter 5 and Appendix A match `research_sources/existing_work/Antibacterial Efficacy Results - Zone of Inhibition.md`.
- Literature comparison table now includes aqueous C1/C2 and Drakhshaan DCM/MeOH at both 50 and 100 µg mL⁻¹ (`12.93 ± 0.11`, `13.10 ± 0.17`, `11.13 ± 0.23`, `9.07 ± 0.11` restored).
- All 20 research-source photographs are copied under descriptive names and `\includegraphics`’d once each (process plates in Chapter 4; species-labelled inhibition in Chapter 5; remaining culture/assay near-duplicates in Appendix B).
- Collection locality is the University of Kashmir Botanical Garden at 34.12981° N, 74.83396° E. Captions do not mention the geotagged filename, ChatGPT, or WhatsApp.
- Unlabelled C1/C2/N/GEN 5 lids are not assigned to *E. coli*, *P. aeruginosa*, or *K. pneumoniae*. MET 5 and GEN 2 plates are documented as not the tabulated GEN 5 control.
- No invented Fig. 8c. *P. aeruginosa* culture plates are labelled as cultures, not inhibition assays.
- pgfplots grouped bars with SD error bars replace the overflowing TikZ chart; invalid `error bars/cap size` key removed so Tectonic completes bibtex and label resolution.
- `build.py` now requests two Tectonic reruns and scores the **final** engine log (not first-pass `-p` chatter), yielding 0 undefined citations and 0 broken references in `--strict` mode.
- Appendix A phytochemical colour key uses wrapping `tabularx` columns to stop overfull `l` cells.
- Targeted PubMed/Crossref keys (12: `nikaido2003`, `li2015`, `blair2015`, `apgiv2016`, `harborne1998`, `luquedecastro2010`, `eloff1998`, `andrews2001`, `kaper2004`, `lister2009`, `paczosa2016`, `navonvenezia2017`) are in `references.bib` and `\cite`d. `wani2017` is not cited. WHO “10 million deaths” is not attached to `who2024`.

## Majors noted (candidate)
- No ATCC/NCTC numbers for the three laboratory stocks.
- No *P. aeruginosa* species-labelled **inhibition** plate (culture plates exist).
- No KASH voucher, authenticating botanist, or collection month in the notes.
- Well-fill volume was not recorded.
- Acknowledgements thank laboratory colleagues generically; named lab assistants were not in the `.tex` (workdown placeholders were not copied into the current file).
- IACUC/animal-ethics wording is omitted because this is in-vitro plant work, not a vertebrate protocol.

## Layout
- Numeric tables use `booktabs`; comparative tables use `tabularx` within `\textwidth`.
- ZOI chart: `ybar` groups for C1, C2, and gentamicin; SD as `error bars/y explicit`; negative control omitted (zero). Width 0.98`\textwidth`, `[hbt!]`.
- Unique Soxhlet/processing photographs stay in methods; Appendix B holds the plate gallery so the narrative is not a contact sheet.
- Earlier leftover frog chapters (`02_lit_review.tex`, `03_methods.tex`, `04_results.tex`, `05_discussion.tex`) are **not** `\input`.

## Citations
- Live-file keys all resolve in `references.bib`.
- Strict Tectonic pass (2026-09-17): 0 `[?]`, 0 `??` in the engine log; PDF 26.7 MB.
- New keys appear in Chapter 1 (envelope/RND/APG), Chapter 3 (pathogens, assay limits), and Chapter 4 (Harborne, Soxhlet).

## Nomenclature
- Live chapters and abstract: `validate_nomenclature.py --file` reported 0 binomial/abbreviation errors.
- Binomials italic; genus spelled out at sentence start in the live files.
- `--dir chapters/ --strict` was **not** used: leftover frog files still sit in `chapters/` and are out of scope for this document.
