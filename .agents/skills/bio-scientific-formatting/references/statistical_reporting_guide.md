# Statistical Reporting Guide for Life Sciences Dissertations

This guide establishes mathematical and statistical typography standards for life sciences research writing.

---

## 1. Mathematical Typography Rules

- **Italicize**: Test statistics and variable symbols ($F, t, U, W, \chi^2, p, r, R^2, z, N, n$).
- **Roman (Upright)**: Descriptive subscripts, abbreviations, mathematical operators ($\log, \ln, \exp, \sin$), and Greek letters in biological names ($\alpha, \beta, \Delta$).
- **Spacing**: Use standard mathematical spacing before and after operators: $p < 0.001$, not $p<0.001$.

---

## 2. Standard Test Reporting Templates

### Analysis of Variance (ANOVA)
- Structure: $F(\text{df}_{\text{effect}}, \text{df}_{\text{error}}) = F\text{-value}, p = \text{value}, \eta^2 = \text{value}$.
- Example:
  ```latex
  Head depth differed significantly among habitat types 
  ($F(2, 42) = 14.82, p < 0.001, \eta^2 = 0.41$).
  ```

### Student's $t$-Test
- Structure: $t(\text{df}) = t\text{-value}, p = \text{value}, \text{Cohen's } d = \text{value}$.
- Example:
  ```latex
  Male lizards exhibited significantly greater SVL than females 
  ($t(38) = 2.45, p = 0.019, \text{Cohen's } d = 0.78$).
  ```

### Regression & Morphometrics (PGLS)
- Structure: $\beta = \text{value} \pm \text{SE}, t = \text{value}, p = \text{value}, R^2 = \text{value}, \lambda = \text{value}$.
- Example:
  ```latex
  Phylogenetic Generalized Least Squares revealed a significant negative relationship 
  between elevation and head depth ($\beta = -0.0034 \pm 0.0008, t = -4.25, p < 0.001, 
  R^2 = 0.38, \text{Pagel's } \lambda = 0.72$).
  ```

### Principal Component Analysis (PCA)
- Structure: PC axis, percentage of variance explained, eigenvalue.
- Example:
  ```latex
  The first principal component (PC1: 42.1\% of total variance, eigenvalue = 4.63) 
  loaded strongly on cranial dimensions (HL: 0.88, HW: 0.85).
  ```

### Confidence Intervals and Descriptive Measures
- Structure: Mean $\pm$ SD [95% CI lower, upper].
- Example:
  ```latex
  Mean adult body mass was $12.4 \pm 1.8\text{ g}$ ($95\%\text{ CI } [11.6, 13.2]$).
  ```
