# External Life Sciences APIs Guide

This reference outlines patterns for querying biomedical and evolutionary biology literature and sequence databases during literature synthesis and nomenclature verification.

---

## 1. NCBI Entrez E-Utilities (PubMed, Taxonomy, Nucleotide)

NCBI E-utilities provide programmatic access to PubMed literature and GenBank taxonomy/sequences.

### Base URLs
- **ESearch**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- **ESummary**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`
- **EFetch**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

### Rate Limits
- **Unauthenticated**: 3 requests per second maximum.
- **Authenticated (`api_key` parameter or `NCBI_API_KEY` env var)**: 10 requests per second.
- Mandatory parameters: `tool=bio_dissertation_suite` and `email=researcher@institution.edu`.

### Common Query Patterns
1. **Literature Search (PubMed)**:
   ```text
   GET /esearch.fcgi?db=pubmed&term=Sceloporus+occidentalis+phylogeography&retmode=json&retmax=20
   ```
2. **Taxon Verification (NCBI Taxonomy)**:
   ```text
   GET /esearch.fcgi?db=taxonomy&term=Sceloporus+occidentalis[Scientific+Name]&retmode=json
   ```
3. **Sequence Metadata (GenBank Nucleotide)**:
   ```text
   GET /esummary.fcgi?db=nuccore&id=OR892100&retmode=json
   ```

---

## 2. bioRxiv & medRxiv API

bioRxiv provides a RESTful API for retrieving preprints in Zoology, Evolutionary Biology, Ecology, and Genomics.

### Base URL
- `https://api.biorxiv.org/details/[server]/[interval]/[cursor]/[format]`
- Example: `https://api.biorxiv.org/details/biorxiv/2025-01-01/2025-12-31/0/json`

### Usage in Dissertation Drafting
- Identify emerging preprints on disputed taxonomic complexes or novel phylogenomic methodologies.
- Retrieve publication status and DOI updates for manuscripts currently in preprint form.

---

## 3. Best Practices for Agents

- **Cache Responses**: Avoid redundant queries for identical taxon names or PMIDs.
- **Graceful Fallback**: If network is unavailable or API returns HTTP 429/503, rely on local staging data in `research_sources/`.
- **Integrity**: Never synthesize mock DOIs or imaginary paper abstracts. Citations must match real records.
