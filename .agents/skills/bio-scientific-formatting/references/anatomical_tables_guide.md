# Anatomical & Morphometric Tables in LaTeX

This guide establishes the typographic standards for anatomical, morphometric, and voucher tables in biological dissertations.

---

## 1. Core Principles of Academic Table Typography

1. **Zero Vertical Lines**: Never use vertical rules (`|`). They impede horizontal readability and violate academic publishing standards.
2. **Three Horizontal Rule Weights**:
   - `\toprule`: Heavy rule at the table head.
   - `\midrule`: Thin rule separating headers from data rows.
   - `\bottomrule`: Heavy rule terminating the table.
3. **Align Numbers on Decimals**: Use `siunitx` column type `S[table-format=X.Y]` so numbers align cleanly by decimal point rather than being centered.
4. **Header Protection**: Text headers in `S` columns must be enclosed in braces: `{Head Length (mm)}`.

---

## 2. Standard Morphometric Table Template

```latex
\begin{table}[htbp]
\centering
\caption{Morphometric variation in adult males across three phrynosomatid species (mean $\pm$ SD in mm).}
\label{tab:morphometric_summary}
\begin{tabular}{l S[table-format=2.2] S[table-format=2.2] S[table-format=2.2]}
\toprule
Species & {SVL (mm)} & {Head Length (mm)} & {Femur Length (mm)} \\
\midrule
\textit{Sceloporus occidentalis} & 71.05 & 15.82 & 14.33 \\
\textit{Sceloporus graciosus}    & 54.05 & 11.73 & 10.78 \\
\textit{Uta stansburiana}        & 48.65 & 10.53 & 9.30  \\
\bottomrule
\end{tabular}
\end{table}
```

---

## 3. Museum Voucher Catalogs (Longtable)

For multi-page specimen voucher catalogs in appendices, use `longtable`:
```latex
\begin{longtable}{l l l S[table-format=4.0] l}
\caption{Examined museum voucher specimens deposited at MVZ.}\label{tab:voucher_catalog} \\
\toprule
{Voucher ID} & {Taxon} & {Sex} & {Elevation (m)} & {Locality} \\
\midrule
\endfirsthead
...
\end{longtable}
```
Convert existing CSV datasets directly to this format using:
```bash
uv run python .agents/skills/bio-scientific-formatting/scripts/format_table.py \
    --input research_sources/existing_work/morphometrics.csv \
    --longtable \
    --output appendices/morphometrics_table.tex
```
