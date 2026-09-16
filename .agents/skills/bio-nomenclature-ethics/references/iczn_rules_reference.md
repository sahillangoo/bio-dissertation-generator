# ICZN Zoological Nomenclature Reference Guide

This reference provides standard rules and LaTeX formatting practices based on the **International Code of Zoological Nomenclature (ICZN, 4th Edition)**.

---

## 1. Binomial and Trinomial Names (Articles 5 & 6)

- **Binomials**: Species names consist of two words: the genus name (capitalized) and the specific epithet (lowercase).
  - Both must always be italicized in print: `\textit{Sceloporus occidentalis}` or `\taxa{Sceloporus occidentalis}`.
  - Subspecies (trinomials) follow the same rule: `\textit{Sceloporus occidentalis bocourtii}`.
- **Higher Taxa**: Taxa above genus (Tribe, Subfamily, Family, Superfamily, Order, Class, Phylum, Kingdom) are capitalized but set in **Roman (upright)** font:
  - Class Reptilia, Order Squamata, Family Phrynosomatidae, Genus *Sceloporus*.

---

## 2. Abbreviation Rules

1. **First Mention**: In each chapter, abstract, and standalone section, spell out the full genus name on first mention:
   - *Sceloporus occidentalis* Baird & Girard, 1852.
2. **Subsequent Mentions**: Use the initial letter of the genus followed by a period and space:
   - *S. occidentalis*.
3. **Beginning of a Sentence**: **Never** begin a sentence with an abbreviated genus name:
   - ❌ Incorrect: "*S. occidentalis* is widely distributed."
   - ✅ Correct: "*Sceloporus occidentalis* is widely distributed." or "The western fence lizard, *S. occidentalis*, is widely distributed."
4. **Disambiguation**: If two genera share the same initial in the same section, use two-letter or full abbreviations:
   - *Sc. occidentalis* vs. *Sa. spinosus*.

---

## 3. Taxonomic Authority Attribution (Article 22A & 51)

Zoological authority citations indicate who described the taxon and in what year.
- **Original Combination (No Parentheses)**:
  - If the species remains in the genus in which it was originally described:
  - *Homo sapiens* Linnaeus, 1758
  - *Sceloporus occidentalis* Baird & Girard, 1852
- **Transferred Combination (In Parentheses)**:
  - If the species was transferred to a different genus from the original description:
  - *Panthera leo* (Linnaeus, 1758) [originally described as *Felis leo* Linnaeus, 1758].
- **Comma Requirement (Art. 22A)**:
  - In zoology, a comma **must** separate the author from the year (`Linnaeus, 1758`). This distinguishes zoological authority citations from botanical nomenclature where the comma is omitted.

---

## 4. Novel Taxa and Type Designations (Articles 13, 16 & 72–75)

When describing a new species or genus in a dissertation:
- **Designation Tags**:
  - `sp. nov.` (species nova) or `\spnov{Taxon}`
  - `gen. nov.` (genus novum)
  - `comb. nov.` (combinatio nova)
- **Mandatory Type Specimen**:
  - Holotype designation is mandatory (ICZN Art. 16.4).
  - Explicit repository acronym and catalog number: `MVZ:Herp:29401` or `\holotype{MVZ:Herp:29401}`.
  - Precise type locality including geographic coordinates (WGS84) and elevation.
  - Complete specimen diagnosis contrasting with all congeners.
