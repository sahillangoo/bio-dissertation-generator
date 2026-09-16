# Specialized Biological Citations Guide

This guide provides BibTeX templates for non-traditional academic entities: software packages, genetic repositories, museum vouchers, and taxonomic monographs.

---

## 1. Citing Software and Computational Pipelines

Always cite both the software paper and the exact version used in analyses.

### Phylogenetic Inference Packages
```bibtex
@article{minh2020iqtree,
  author    = {Minh, Bui Quang and Schmidt, Heiko A. and Chernomor, Olga and Schrempf, Dominik and Woodhams, Michael D. and von Haeseler, Arndt and Lanfear, Robert},
  title     = {{IQ-TREE} 2: new models and efficient methods for phylogenomic inference in the genomic era},
  journal   = {Molecular Biology and Evolution},
  volume    = {37},
  number    = {5},
  pages     = {1530--1534},
  year      = {2020},
  doi       = {10.1093/molbev/msaa015}
}

@article{hohna2016revbayes,
  author    = {H{\"o}hna, Sebastian and Landis, Michael J. and Heath, Tracy A. and Boussau, Bastien and Lartillot, Nicolas and Moore, Brian R. and Huelsenbeck, John P. and Ronquist, Fredrik},
  title     = {{RevBayes}: {Bayesian} phylogenetic inference using graphical models and an interactive language},
  journal   = {Systematic Biology},
  volume    = {65},
  number    = {4},
  pages     = {726--736},
  year      = {2016},
  doi       = {10.1093/sysbio/syw021}
}
```

### R Packages (Morphometrics and Phylogenetics)
```bibtex
@manual{rcore2024,
  title        = {R: A Language and Environment for Statistical Computing},
  author       = {{R Core Team}},
  organization = {R Foundation for Statistical Computing},
  address      = {Vienna, Austria},
  year         = {2024},
  url          = {https://www.R-project.org/}
}

@article{paradis2019ape,
  author    = {Paradis, Emmanuel and Schliep, Klaus},
  title     = {ape 5.0: an environment for modern phylogenetics and evolutionary analyses in {R}},
  journal   = {Bioinformatics},
  volume    = {35},
  number    = {3},
  pages     = {526--528},
  year      = {2019},
  doi       = {10.1093/bioinformatics/bty633}
}
```

---

## 2. Citing Public Repositories and Data Registries

### NCBI GenBank Accessions
```bibtex
@misc{genbank2026sceloporus,
  author       = {Researcher, Candidate and Vance, Elena},
  title        = {\textit{Sceloporus occidentalis} cytochrome c oxidase subunit {I} ({COI}) and {RAG1} gene sequences},
  howpublished = {NCBI GenBank Accessions OR892100--OR892185},
  year         = {2026}
}
```

### MorphoBank & TreeBASE
```bibtex
@misc{morphobank2026project,
  author       = {Researcher, Candidate},
  title        = {Phenotypic matrix and 3D micro-CT cranial scans for western {Phrynosomatidae}},
  howpublished = {MorphoBank Project p4892},
  year         = {2026},
  doi          = {10.7934/P4892}
}
```

---

## 3. Citing Zoological Authorities and Taxonomic Codes

```bibtex
@book{iczn1999code,
  author    = {{International Commission on Zoological Nomenclature}},
  title     = {International Code of Zoological Nomenclature},
  edition   = {4th},
  publisher = {The International Trust for Zoological Nomenclature},
  address   = {London, UK},
  year      = {1999}
}
```
