# Dissertation Committee Meeting Notes & Directives

**Candidate**: Candidate Researcher  
**Meeting Date**: January 15, 2026  
**Committee Members Present**:
- **Dr. Elena Vance** (Dissertation Chair, Evolutionary Biology)
- **Dr. Marcus Thorne** (Committee Member, Systematic Zoology & ICZN Commissioner)
- **Dr. Sarah Lin** (Committee Member, Physiological Ecology & Functional Morphology)

---

## 1. Core Research Hypotheses

The committee formally approved the following three central hypotheses guiding the dissertation:

### Hypothesis 1 ($H_1$): Ecomorphological Divergence Along Elevational Gradients
- **Hypothesis**: Natural selection for substrate utilization drives convergent morphometric differentiation between boulder-dwelling (saxicolous) and woodland arboreal populations of *Sceloporus occidentalis*.
- **Predictions**: Saxicolous morphs will exhibit significantly lower relative head depth ($HD / HL$) to exploit rock crevices, and elongated hindlimbs ($HLL / SVL$) enhancing sprint acceleration on steep granite surfaces, regardless of clade ancestry.
- **Statistical Test**: Phylogenetic Generalized Least Squares (PGLS) and MANOVA on the 11 linear morphometric traits.

### Hypothesis 2 ($H_2$): Cytonuclear Discordance and Introgression Across Sierra Passes
- **Hypothesis**: Pleistocene climatic fluctuations caused secondary contact and asymmetric mitochondrial capture between Pacific and Great Basin lineages.
- **Predictions**: Mitochondrial gene trees (COI) will show deep divergence between eastern Sierra and western Sierra haplogroups, whereas nuclear markers (RAG1) will reveal extensive gene flow and admixed genotypes at low-elevation passes.
- **Statistical Test**: Shimodaira-Hasegawa (SH) test comparing constrained vs. unconstrained tree topologies; STRUCTURE / ADMIXTURE clustering.

### Hypothesis 3 ($H_3$): Thermal Restriction and Microhabitat Buffering
- **Hypothesis**: Ectotherm activity windows are constrained by environmental thermal maxima at lower elevations, forcing behavioral retreat to thermal refugia and limiting foraging duration.
- **Predictions**: Daily restriction hours ($h_r$) will exceed 4.5 hours/day in desert-margin localities during June–August, correlating with smaller adult body mass.
- **Statistical Test**: Linear mixed-effects modeling relating $h_r$ to elevational transect sites.

---

## 2. Chapter Architecture & Directives

1. **Frontmatter**:
   - Must include dedicated Ethics Statement citing **IACUC Protocol #2024-0892-VANCE** and California DFW Scientific Collecting Permit **SC-12849**.
2. **Chapter 1 (Introduction)**:
   - Provide clear geological and paleoclimatic context for the Great Basin / Sierra Nevada transition.
   - Conclude with a dedicated subsections for $H_1$, $H_2$, and $H_3$.
3. **Chapter 2 (Literature Review)**:
   - Contrast classic vicariance models with recent ecological speciation paradigms.
   - Include a comparative table of previous phylogeographic studies on western North American herpetofauna.
4. **Chapter 3 (Methods)**:
   - Explicitly define Mitutoyo digital caliper measurement landmarks.
   - List primer sequences for COI (`LCO1490`/`HCO2198`) and RAG1 (`RAG1-F1`/`RAG1-R1`).
   - Detail model selection criteria (BIC in PartitionFinder 2).
5. **Chapter 4 (Results)**:
   - Present maximum likelihood and Bayesian trees with dual branch support metrics (UFBoot2 / posterior probability).
   - Display morphological PCA biplots and summary tables using publication-standard formatting (`booktabs`, `siunitx`).
6. **Chapter 5 (Discussion)**:
   - Synthesize findings in light of Smith et al. (2021) and Sinervo et al. (2010).
   - Discuss conservation implications of thermal niche erosion.
7. **Appendices**:
   - **Appendix A**: Complete specimen voucher catalog with MVZ accession numbers, localities, and GPS coordinates.
   - **Appendix B**: PCR thermocycling conditions and primer sequences.
   - **Appendix C**: Full ANOVA tables and factor loadings.

---

## 3. Committee Revisions and Quality Checklist

- [x] Ensure strict ICZN adherence for all taxonomic names (italicize binomials, uppercase Roman for higher taxa).
- [x] Full binomial must appear at first mention in each chapter (*Sceloporus occidentalis* Baird & Girard, 1852); subsequent mentions use *S. occidentalis*.
- [x] Ensure zero broken cross-references (`??` or `[?]`) in the compiled LaTeX document.
- [x] Deposit all sequence data under mock GenBank accession numbers (e.g., `OR892100`–`OR892185`) in the methods and specimen table.
