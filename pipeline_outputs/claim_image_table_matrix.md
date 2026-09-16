# Claim × image × table matrix (Wave 3 Evidence)

Reviewer: report-only. Source of truth: `pipeline_outputs/evidence_ledger.md` and `pipeline_outputs/figure_inventory.md`. Compiled draft: Kashmir Ch.1–7, 2026-09-17.

| Claim | Ledger | Image | Table | Verdict |
|-------|--------|-------|-------|---------|
| Roll 24061119001; Bazilla Saleem; Zoology, University of Kashmir | E01–E03 | title page | n/a | PASS |
| Collection Botanical Garden; GPS 34.12981 N, 74.83396 E from photo filename | E04–E05 | fig:collection_site | n/a | PASS |
| No voucher / collection date invented | E06 | n/a | n/a | PASS (omitted) |
| Whole plant, shade-dried, mortar powder | E07 | fig1–3 | n/a | PASS |
| Soxhlet 50 g : 500 mL, 24 h | E08 | fig4–5 | eq:yield | PASS |
| Yield 24.13% w/w | E09 | n/a | Results §5.1 | PASS |
| Three lab stocks on LB; no ATCC | E10 | fig6–7 | tab:bacterial_taxonomy | PASS |
| Well diffusion extract + water; gentamicin disc; 6 mm; 37 °C; 24 h; n=3 | E11 | fig8a, fig8b, fig:gen5_disc | ZOI tables | PASS |
| C1 50 µg mL⁻¹; C2 100 µg mL⁻¹ | E12 | captions | all ZOI tables | PASS |
| *E. coli* C1 11.94±0.14; C2 14.99±0.51; + 17.00; − 0 | E13 | fig8a (N vs C only) | tab:zoi_ecoli + appendix | PASS |
| *P. aeruginosa* C1 16.03±0.25; C2 12.53±0.45; + 17.17; − 0 | E14 | **no inhibition plate** | tab:zoi_paeruginosa | PASS numbers; IMAGE absent (disclosed) |
| *K. pneumoniae* C1 12.35±0.56; C2 13.25±0.43; + 15.17; − 0 | E15 | fig8b | tab:zoi_kpneumoniae | PASS |
| Phytochem all + | E16 | fig:phytochem | tab:phytochem_results | PASS |
| Gentamicin not claimed as 10 µg; GEN 5 labelled where photographed | E17 | fig:gen5_disc | + column as “disc” | PASS |
| No MIC/MBC/HPLC of this extract | E18 | n/a | n/a | PASS (excluded) |
| ChatGPT PNG unused | E19 | excluded | n/a | PASS |
| wani2017 not cited | E20 | n/a | n/a | PASS |
| *K. pneumoniae* novelty as indexed gap | E21 | n/a | discussion | **FAIL in Ch.1 gap list** (“no study… novel scientific contribution”); Ch.5–7 OK |
| Inverse Pa dose reported, not explained as potency | E22 | none | tab:zoi_paeruginosa | PASS |

## FAIL rows for writer
1. `chapters/01_introduction.tex` §gaps — **PATCHED** to indexed-literature wording.

## Notes (not FAIL)
- Unused leftover frog chapter/appendix files may still sit on disk; they are not `\input` in `dissertation.tex`.
- Bar chart omits SD whiskers; numerical SD is in tables.
