# Preliminary Draft: Materials and Methods

**Target Chapter**: `chapters/03_methods.tex`  
**Author**: Candidate Researcher  
**Date**: Updated Spring 2026  
**Status**: Rough Draft for Integration  

---

## 1. Taxonomic Sampling and Field Collection

Field collections were conducted across 14 geographic localities spanning the Great Basin and Sierra Nevada ecotone (California and Nevada, USA) between May 2023 and August 2025. Sampling focused on the western fence lizard complex (*Sceloporus occidentalis* Baird & Girard, 1852), with comparative outgroup material from the sagebrush lizard (*Sceloporus graciosus* Baird & Girard, 1852) and the side-blotched lizard (*Uta stansburiana* Baird & Girard, 1852).

A total of 86 adult individuals were sampled under California Department of Fish and Wildlife Scientific Collecting Permit SC-12849 and Nevada Department of Wildlife Scientific Collection Permit 38921. Voucher specimens were euthanized using intracoelomic injection of buffered 1% sodium pentobarbital (100 mg/kg), fixed in 10% neutral buffered formalin, and permanently transferred to 70% ethanol. All voucher specimens and associated frozen tissue samples were deposited in the Museum of Vertebrate Zoology (MVZ), University of California, Berkeley.

---

## 2. Morphometric Protocol

For each adult specimen, eleven linear morphometric characters were measured using Mitutoyo 500-196-30 digital calipers to the nearest 0.01 mm:
1. **Snout-Vent Length (SVL)**: Tip of the snout to the anterior margin of the cloacal opening.
2. **Tail Length (TL)**: Posterior margin of the cloaca to the tip of the unregenerated tail.
3. **Head Length (HL)**: Tip of the snout to the anterior margin of the tympanic opening.
4. **Head Width (HW)**: Maximum width across the skull at the level of the jugal arch.
5. **Head Depth (HD)**: Maximum vertical height of the skull immediately behind the orbits.
6. **Interorbital Distance (IOD)**: Minimum distance across the dorsal cranial surface between the medial margins of the eyes.
7. **Snout Length (SL)**: Anterior margin of the orbit to the tip of the rostral scale.
8. **Axilla-Groin Distance (AGD)**: Posterior margin of the forelimb insertion to the anterior margin of the hindlimb insertion.
9. **Forelimb Length (FLL)**: Body wall to the distal tip of the longest digit (digit IV), excluding the claw.
10. **Hindlimb Length (HLL)**: Body wall to the distal tip of the longest toe (toe IV), excluding the claw.
11. **Femur Length (FL)**: Articulation of the femur at the pelvis to the knee joint.

All morphometric measurements were performed in triplicate by a single investigator to eliminate inter-observer error, and the arithmetic mean was used for subsequent statistical analysis.

---

## 3. DNA Extraction, PCR Amplification, and Sequencing

Genomic DNA was extracted from ethanol-preserved liver or skeletal muscle tissue using the DNeasy Blood & Tissue Kit (Qiagen, Hilden, Germany) following the manufacturer's standard protocol with an extended 14-hour proteinase K lysis at 56 °C. DNA concentration and purity were assessed using a NanoDrop 2000 spectrophotometer and fluorometric quantification on a Qubit 4.0 Fluorometer (Thermo Fisher Scientific).

Two genetic markers were targeted:
- **Mitochondrial Cytochrome c Oxidase Subunit I (COI)**: Amplified using primers `LCO1490` (5'-GGTCAACAAATCATAAAGATATTGG-3') and `HCO2198` (5'-TAAACTTCAGGGTGACCAAAAAATCA-3') (Folmer et al., 1994). Thermocycling conditions: initial denaturation at 95 °C for 3 min; 35 cycles of 95 °C for 30 s, 48 °C for 45 s, 72 °C for 60 s; final elongation at 72 °C for 7 min.
- **Nuclear Recombination Activating Gene 1 (RAG1)**: Amplified using degenerate primers `RAG1-F1` (5'-AGCTGCAGYCARACCAAYAA-3') and `RAG1-R1` (5'-TCCACTTTRTCRTCATCYTC-3'). Thermocycling conditions: touchdown PCR from 58 °C to 50 °C (-0.5 °C/cycle for 16 cycles), followed by 24 cycles at 50 °C annealing temperature.

Amplicons were visualized on 1.5% agarose gels stained with GelGreen, enzymatically purified with ExoSAP-IT (Applied Biosystems), and bidirectionally sequenced on an ABI 3730xl DNA Analyzer.

---

## 4. Phylogenetic and Comparative Analyses

Chromatograms were inspected, trimmed, and assembled into contiguous sequences in Geneious Prime 2024.0. Multiple sequence alignments were generated using MAFFT v7.505 under the L-INS-i iterative refinement method. The optimal nucleotide substitution model for each codon partition was identified using PartitionFinder 2 based on the Bayesian Information Criterion (BIC).

Maximum Likelihood (ML) gene trees and concatenated phylogenies were reconstructed in IQ-TREE 2.2.0. Branch support was evaluated with 1,000 ultrafast bootstrap (UFBoot2) replicates and the Shimodaira-Hasegawa approximate likelihood ratio test (SH-aLRT). Bayesian phylogenetic inference was performed in RevBayes v1.2.2 with four independent MCMC chains running for 20 million generations, sampling every 2,000 generations, with the first 25% discarded as burn-in.

---

## 5. Animal Care and Ethical Approval

All handling, collection, and sampling protocols involving live vertebrates were reviewed and approved by the Institutional Animal Care and Use Committee (IACUC) at the University of California, Berkeley under protocol **#IACUC-2024-0892-VANCE**. Field work adhered to guidelines established by the American Society of Ichthyologists and Herpetologists (ASIH) for the use of live amphibians and reptiles in field and laboratory research.
