# BibLaTeX Citation Styles Guide for Life Sciences

This reference outlines citation and bibliography configurations for biology, zoology, and evolutionary ecology dissertations using BibLaTeX and Biber.

---

## 1. Preferred Biological Citation Style: Council of Science Editors (CSE) Name-Year

The **Council of Science Editors (CSE) Name-Year** format is the standard across organismal biology, ecology, and zoology.

### Preamble Configuration
```latex
\usepackage[
    backend=biber,
    style=ext-authoryear,
    natbib=true,
    maxcitenames=2,
    mincitenames=1,
    maxbibnames=99,
    giveninits=true,
    uniquename=false,
    uniquelist=false,
    doi=true,
    isbn=false,
    url=false,
    date=year
]{biblatex}

% Omit "In:" before journal title
\renewbibmacro{in:}{%
  \ifentrytype{article}{}{\printtext{\bibstring{in}\addspace}}}

% Volume(Number):Pages format
\DeclareFieldFormat[article]{volume}{\textbf{#1}}
\DeclareFieldFormat[article]{number}{\mkbibparens{#1}}
\DeclareFieldFormat{pages}{#1}
```

### In-Text Citation Usage
- Parenthetical: `\citep{leache2002molecular}` -> `(Leaché & Reeder, 2002)`
- Narrative: `\citet{leache2002molecular}` or `\textcite{leache2002molecular}` -> `Leaché & Reeder (2002)`
- Three or more authors: `\citep{smith2021phylogenomics}` -> `(Smith et al., 2021)`
- Multiple citations grouped: `\citep{baird1852characteristics, wiens2002speciation}` -> `(Baird & Girard, 1852; Wiens & Penkrot, 2002)`

---

## 2. APA 7th Edition Style (Interdisciplinary & Behavioral Biology)

If your department or committee requires APA style:
```latex
\usepackage[
    backend=biber,
    style=apa,
    natbib=true
]{biblatex}
```

---

## 3. Best Practices for Dissertation Bibliographies

1. **Always Include DOIs**: Digital Object Identifiers provide permanent resolution to literature records.
2. **Standardize Journal Abbreviations**: Either spell out full journal names (*Systematic Biology*, *Molecular Ecology*) or consistently use ISO4 abbreviations (*Syst. Biol.*, *Mol. Ecol.*).
3. **Preserve Case for Scientific Names in Titles**: Enclose Latin binomials and proper nouns in braces in `.bib` titles:
   ```bibtex
   title = {Molecular systematics of {\textit{Sceloporus occidentalis}} in the {Great} {Basin}}
   ```
