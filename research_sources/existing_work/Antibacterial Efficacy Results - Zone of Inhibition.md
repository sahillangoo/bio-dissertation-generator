# **Antibacterial Potential of Aqueous Plant Extract: In Vitro Zone of Inhibition (ZOI) Analysis**

---

**Experiment Details:**

> * **Method:** Soxhlet Extraction (Aqueous / Polar Extract)  
> * **Plant to Extract Ratio:** 1:10 (50 g plant material : 500 mL solvent)  
> * **Assay Type:** Disc/Well Diffusion Assay (Triplicate measurements: R1, R2, R3 in mm, including disc/well)

## **1\. Summary Table of Antibacterial Efficacy**

| Bacterial Strain | Treatment Concentration / Control | R1 (mm) | R2 (mm) | R3 (mm) | Mean ± SD (mm)&nbsp;&nbsp; |
| :---: | :---: | :---: | :---: | :---: | ----- |
| *Escherichia coli* | C1 (50 μg) | 12.00 | 11.78 | 12.05 | **11.94 ± 0.14** |
|  | C2 (100 μg) | 15.00 | 15.50 | 14.48 | **14.99 ± 0.51** |
|  | Positive Control (+) | 17.00 | 17.00 | 17.00 | **17.00 ± 0.00** |
|  | Negative Control (-) | 0.00 | 0.00 | 0.00 | 0.00 ± 0.00 |
| *Pseudomonas aeruginosa* | C1 (50 μg) | 16.00 | 16.30 | 15.80 | **16.03 ± 0.25** |
|  | C2 (100 μg) | 13.00 | 12.50 | 12.10 | **12.53 ± 0.45** |
|  | Positive Control (+) | 17.50 | 17.00 | 17.00 | **17.17 ± 0.29** |
|  | Negative Control (-) | 0.00 | 0.00 | 0.00 | 0.00 ± 0.00 |
| *Klebsiella pneumoniae* | C1 (50 μg) | 12.00 | 13.00 | 12.05 | **12.35 ± 0.56** |
|  | C2 (100 μg) | 13.50 | 13.50 | 12.75 | **13.25 ± 0.43** |
|  | Positive Control (+) | 15.50 | 15.00 | 15.00 | **15.17 ± 0.29** |
|  | Negative Control (-) | 0.00 | 0.00 | 0.00 | 0.00 ± 0.00 |

## **2\. Python Script to Recreate the Bar Graph**

import matplotlib.pyplot as plt  
import numpy as np

strains \= \["E. coli", "P. aeruginosa", "K. pneumoniae"\]  
x \= np.arange(len(strains))  
width \= 0.25

means\_c1 \= \[11.94, 16.03, 12.35\]  
std\_c1 \= \[0.14, 0.25, 0.56\]

means\_c2 \= \[14.99, 12.53, 13.25\]  
std\_c2 \= \[0.51, 0.45, 0.43\]

means\_pos \= \[17.00, 17.17, 15.17\]  
std\_pos \= \[0.00, 0.29, 0.29\]

fig, ax \= plt.subplots(figsize=(9, 6), dpi=300)

rects1 \= ax.bar(x \- width, means\_c1, width, yerr=std\_c1, capsize=5, label=r"$C\_1\\ (50\\,\\mu\\mathrm{g})$", color="\#4C72B0", edgecolor="black", linewidth=0.8)  
rects2 \= ax.bar(x, means\_c2, width, yerr=std\_c2, capsize=5, label=r"$C\_2\\ (100\\,\\mu\\mathrm{g})$", color="\#55A868", edgecolor="black", linewidth=0.8)  
rects3 \= ax.bar(x \+ width, means\_pos, width, yerr=std\_pos, capsize=5, label="Positive Control (+)", color="\#C44E52", edgecolor="black", linewidth=0.8)

ax.set\_ylabel("Zone of Inhibition (mm, mean ± SD)", fontsize=12, fontweight="bold")  
ax.set\_title("Antibacterial Efficacy of Aqueous Extract", fontsize=14, fontweight="bold")  
ax.set\_xticks(x)  
ax.set\_xticklabels(strains, fontsize=11, fontstyle="italic", fontweight="semibold")  
ax.set\_ylim(0, 22\)  
ax.legend(frameon=True, fontsize=10)  
ax.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight\_layout()  
plt.show()

&nbsp;

&nbsp;

Generated from experimental laboratory notes. [fill the details in this]

| Constituent | Result |
| :---- | :---- |
| Flavonoids | \+ |
| Phenolics | \+ |
| Quinones | \+ |
| Terpenoids | \+ |
| Tannins | \+ |
| Carbohydrates | \+ |
| Saponins | \+ |
| Alkaloids | \+ |
| Phytosterols | \+ |

&nbsp;

&nbsp;

Here is the exact transcribed table data from the provided image.

| S.No | Phytoconstituent | Tests | Reagents | Color |
| :---- | :---- | :---- | :---- | :---- |
| 01 | Alkaloids | Mayer's test | 2ml mayers reagent \+ Extract | Dull white ppt |
| 02 | Carbohydrates | Fehlings test | Extract \+ Equal quantities of Fehling A & B (Heated) | Brick Red ppt |
| 03 | Saponins | Foam test | 1ml Extract \+ 5ml H2O (Shaken) | Foam Formation |
| 04 | Phytosteroids | Salkowski Test | 2ml plant extract \+2ml chloroform \+2ml sulphuric acid | Reddish brown |
| 05 | Tannins | Ferric Chloride test | Extract \+ Ferric Chloride solution 3-4 drops | Dark blue / Greenish black |
| 06 | Phenols | Ferric Chloride test | Extract \+ 10%Ferric Chloride solution 3-4 drops | Bluish black |
| 07 | Flavonoids | Alkaline reagent test | Extract \+ Few drops of 10%NaOH solution | Yellow color |
| 09 | Terpenoids | Salkowski test | 1ml Extract \+ Thionyl Chloride | Pink color |
| 10 | Quinones | Sulphuric Acid Test&nbsp; | 1ml Extract \+ 1ml H2SO4 | Red |

&nbsp;