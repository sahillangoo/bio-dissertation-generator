#!/usr/bin/env python3
"""
scaffold_dissertation.py - Modular Life Sciences Dissertation Scaffolder

Generates modular LaTeX directory architecture and chapter templates tailored
for Biology and Zoology dissertations (Introduction, Literature Review, Methods,
Results, Discussion, Specimen Appendices, and Frontmatter).
"""

import argparse
from pathlib import Path
import sys
from typing import Dict, Optional

CHAPTER_TEMPLATES: Dict[str, str] = {
    "01_introduction.tex": r"""\chapter{Introduction and Theoretical Framework}
\label{ch:introduction}

\section{Evolutionary and Ecological Background}
\label{sec:intro_background}
% Introduce the broader evolutionary, ecological, or developmental context.
% Provide paleoclimatic or biogeographic foundation for the study system.

\section{Knowledge Gaps in Systematics and Functional Morphology}
\label{sec:intro_gaps}
% Highlight specific contradictions or unaddressed questions in the existing literature.

\section{Study System Justification}
\label{sec:intro_studysystem}
% Justify selection of focal taxa (e.g. western fence lizards, Sceloporus occidentalis).

\section{Research Objectives and Hypotheses}
\label{sec:intro_hypotheses}
This dissertation investigates three primary hypotheses:
\begin{enumerate}
    \item[\textbf{H$_1$}:] \textit{Ecomorphological Convergence}: Substrate specialization drives convergent changes in limb and cranial proportions.
    \item[\textbf{H$_2$}:] \textit{Cytonuclear Discordance}: Mitochondrial introgression across contact zones obscures nuclear species boundaries.
    \item[\textbf{H$_3$}:] \textit{Thermal Restriction}: Elevational thermal gradients dictate microhabitat activity budgets.
\end{enumerate}
""",
    "02_lit_review.tex": r"""\chapter{Comprehensive Literature Review}
\label{ch:lit_review}

\section{Historical Perspectives in Squamate Speciation}
\label{sec:lit_history}
% Classic vicariance paradigms (Pleistocene pluvial lakes, mountain uplift).

\section{Molecular Systematics and Species Delimitation}
\label{sec:lit_systematics}
% Transition from single-locus mitochondrial barcoding to multi-locus phylogenomics.

\section{Ecological Divergence and Morphometrics}
\label{sec:lit_ecomorphology}
% Functional morphology, substrate adaptation, and thermal physiology literature.

\section{Synthesis and Analytical Framework}
\label{sec:lit_synthesis}
% Conceptual model connecting molecular divergence with morphological differentiation.
""",
    "03_methods.tex": r"""\chapter{Materials and Methods}
\label{ch:methods}

\section{Taxon Sampling and Geographic Localities}
\label{sec:methods_sampling}
% Detailed field collection transects, coordinates, and voucher depositions.

\section{Morphometric Measurements}
\label{sec:methods_morphometrics}
% Caliper measurement landmarks (SVL, HL, HW, HD, FLL, HLL) and error assessments.

\section{Molecular Protocols and Sequencing}
\label{sec:methods_molecular}
% DNA extraction protocols, target loci (COI, RAG1), primer sequences, PCR cycling.

\section{Phylogenetic and Statistical Analyses}
\label{sec:methods_analyses}
% Sequence alignment (MAFFT), model selection (PartitionFinder), ML (IQ-TREE), Bayesian (RevBayes).
% Morphometric statistics (PCA, PGLS, MANOVA in R).

\section{Ethical Statements and Scientific Permits}
\label{sec:methods_ethics}
% Mandatory IACUC protocol numbers, state collecting permits, and welfare compliance.
""",
    "04_results.tex": r"""\chapter{Results}
\label{ch:results}

\section{Phylogenetic Topology and Divergence Dating}
\label{sec:results_phylogeny}
% Maximum Likelihood and Bayesian gene trees, branch support (UFBoot, SH-aLRT).

\section{Morphometric Variation and Trait Divergence}
\label{sec:results_morphometrics}
% Summary tables, PCA loadings, cranial and limb trait differentiation.

\section{Cytonuclear Discordance and Gene Flow}
\label{sec:results_discordance}
% Comparison of mitochondrial vs nuclear topologies across geographic transects.

\section{Thermal Restriction Patterns}
\label{sec:results_thermal}
% Elevational correlation with daily activity hours (hr).
""",
    "05_discussion.tex": r"""\chapter{Discussion}
\label{ch:discussion}

\section{Evaluation of Central Hypotheses}
\label{sec:disc_hypotheses}
% Evaluate empirical support for H1, H2, and H3 against results.

\section{Evolutionary Mechanisms and Selection Pressures}
\label{sec:disc_mechanisms}
% Interpret results in light of broader evolutionary theory.

\section{Comparison with Previous Life Sciences Studies}
\label{sec:disc_comparisons}
% Contextualize findings with published literature.

\section{Limitations and Future Research Directions}
\label{sec:disc_future}
% Methodological limitations, genomic coverage expansion, future field seasons.
"""
}

FRONTMATTER_TEMPLATES: Dict[str, str] = {
    "title.tex": r"""\begin{titlepage}
\begin{center}
    \vspace*{1.5cm}
    {\LARGE \textbf{EVALUATING ECOMORPHOLOGICAL DIVERGENCE AND CYTONUCLEAR DISCORDANCE ACROSS ELEVATIONAL GRADIENTS IN PHRYNOSOMATID LIZARDS}\par}
    \vspace{1.5cm}
    {\large By\par}
    \vspace{0.5cm}
    {\large \textbf{Candidate Researcher}\par}
    \vspace{2cm}
    {\normalsize A Dissertation Submitted to the Faculty of the Graduate School\\
    in Partial Fulfillment of the Requirements for the Degree of\\
    \textbf{Doctor of Philosophy in Integrative Biology}\par}
    \vspace{2cm}
    {\normalsize Department of Integrative Biology\\
    University of California, Berkeley\par}
    \vspace{1cm}
    {\normalsize 2026\par}
\end{center}
\end{titlepage}
""",
    "abstract.tex": r"""\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
Understanding the mechanisms that drive speciation across environmental ecotones is a fundamental objective in evolutionary biology. In this dissertation, I investigate molecular divergence, cytonuclear discordance, and morphological adaptation across elevational transects in western North American phrynosomatid lizards (\taxa{Sceloporus occidentalis}). Utilizing multi-locus sequence data (mitochondrial COI and nuclear RAG1) combined with eleven linear morphometric measurements across 86 museum-vouchered specimens, I test whether phenotypic divergence is structured by geographic barriers or local thermal regimes...
""",
    "dedication.tex": r"""\chapter*{Dedication}
\addcontentsline{toc}{chapter}{Dedication}
\textit{Dedicated to my mentors, family, and the natural history of the Great Basin and Sierra Nevada.}
""",
    "acknowledgements.tex": r"""\chapter*{Acknowledgements}
\addcontentsline{toc}{chapter}{Acknowledgements}
I express my deepest gratitude to my dissertation chair, Dr. Elena Vance, for unflagging support, insightful critiques, and field guidance throughout this research...
""",
    "abbreviations.tex": r"""\chapter*{List of Abbreviations}
\addcontentsline{toc}{chapter}{List of Abbreviations}
\begin{description}
    \item[COI] Cytochrome c Oxidase Subunit I
    \item[RAG1] Recombination Activating Gene 1
    \item[SVL] Snout-Vent Length
    \item[HL] Head Length
    \item[HW] Head Width
    \item[HD] Head Depth
    \item[IACUC] Institutional Animal Care and Use Committee
    \item[ICZN] International Code of Zoological Nomenclature
    \item[MVZ] Museum of Vertebrate Zoology
    \item[PGLS] Phylogenetic Generalized Least Squares
\end{description}
""",
    "ethics_statement.tex": r"""\chapter*{Animal Ethics and Research Compliance}
\addcontentsline{toc}{chapter}{Animal Ethics and Research Compliance}
All research protocols involving live vertebrate animals were conducted in strict accordance with federal animal welfare legislation and the recommendations of the National Research Council. Field capture, handling, tissue biopsies, and humane euthanasia protocols were reviewed and approved by the Institutional Animal Care and Use Committee (IACUC) under Protocol Number \textbf{\#IACUC-2024-0892-VANCE}. Field sampling was conducted under California Department of Fish and Wildlife Scientific Collecting Permit \textbf{SC-12849} and Nevada Department of Wildlife Permit \textbf{38921}.
"""
}

APPENDIX_TEMPLATES: Dict[str, str] = {
    "appendix_a_specimens.tex": r"""\chapter{Specimen Voucher Catalog}
\label{app:specimens}
This appendix catalogs all museum voucher specimens examined in this study, deposited in the Museum of Vertebrate Zoology (MVZ), University of California, Berkeley.
""",
    "appendix_b_primers.tex": r"""\chapter{Molecular Protocols and Primers}
\label{app:primers}
Detailed thermocycling profiles, PCR master mix formulations, and primer sequences utilized for Sanger sequencing.
""",
    "appendix_c_stats.tex": r"""\chapter{Supplementary Statistical Tables}
\label{app:stats}
Full factor loadings, eigenvalue scree statistics, and MANOVA tables for morphological characters.
"""
}


def scaffold_project(target_dir: Path, force: bool = False) -> int:
    """Create modular dissertation directories and files."""
    frontmatter_dir = target_dir / "frontmatter"
    chapters_dir = target_dir / "chapters"
    appendices_dir = target_dir / "appendices"

    created = 0
    skipped = 0

    for directory, templates in [
        (frontmatter_dir, FRONTMATTER_TEMPLATES),
        (chapters_dir, CHAPTER_TEMPLATES),
        (appendices_dir, APPENDIX_TEMPLATES),
    ]:
        directory.mkdir(parents=True, exist_ok=True)
        for filename, content in templates.items():
            filepath = directory / filename
            if filepath.exists() and not force:
                skipped += 1
            else:
                filepath.write_text(content, encoding="utf-8")
                created += 1

    print(f"Scaffolding complete in {target_dir}: {created} file(s) created, {skipped} existing file(s) preserved.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold modular LaTeX dissertation chapters and frontmatter for Biology & Zoology."
    )
    parser.add_argument(
        "--target-dir",
        "-t",
        type=Path,
        default=Path("."),
        help="Target directory where modular directories should be created (default: .)",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing template files if they already exist",
    )

    args = parser.parse_args()
    return scaffold_project(args.target_dir.resolve(), args.force)


if __name__ == "__main__":
    sys.exit(main())
