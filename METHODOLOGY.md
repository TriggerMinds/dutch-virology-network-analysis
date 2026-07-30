# Methodology & Legal Disclaimer

## Project Nature

This repository is a **forensic data engineering and network analysis project**. Its purpose is to extract, structure, and analyze publicly available information to enable evidence-based investigation of institutional relationships and scientific discourse. It is **not** legal advice, journalistic publication, or academic peer-reviewed research.

## Data Sources & Legality

All data processed by this pipeline originates from:

1. **Tony's Diary (Fauci)** — A public Congressional document release published by Chairman Rand Paul (U.S. Senate Homeland Security Committee, July 2026). This document is in the U.S. public domain as a government publication.
2. **OpenAlex** — An open scholarly index available under the [CC0 1.0 Universal license](https://openalex.org/about). All queries use the public API with rate-limited access. See `OPENALEX_EMAIL` in `.env.example` for polite pool access.
3. **NIH RePORTER** — A U.S. federal government database of publicly funded research grants. Data is in the public domain.
4. **FOIA/Woo references** — Links to publicly available documents are provided for reference only. No copyrighted or classified content is hosted in this repository.

## GDPR / AVG Compliance

This project processes names, institutional affiliations, and professional roles of individuals who are:

- **Public figures** (senior scientists, government advisors, published academics) acting in their professional capacity
- Identified exclusively through **publicly available** databases (OpenAlex, NIH, Congressional records)
- Leafed only in terms of **professional network relationships** (co-authorship, advisory roles, institutional affiliation)

**GDPR Data Minimization & Stance Profiling Disclaimer:**
We process only data strictly necessary for mapping pandemic governance. Algorithmic faction assignments (e.g. network clustering) are purely mathematical classifications based on document co-occurrence and do *not* represent sensitive political or scientific profiling under GDPR Art. 9.

**Correction and Right-of-Reply (Wederhoor):**
Individuals have the right to object to their inclusion or request corrections. If a named individual disputes an edge or a listed conflict of interest, they may submit a statement via our Correction Policy, which will be published adjacent to the claim. Refer to `docs/CORRECTION_POLICY.md` for SLAs.

## Methodological Rigor & Claims Classification

All data points in this repository are categorized as:
- **Level 1: Documented Fact [FACT]** — Directly supported by primary source citations (e.g., meeting attendance).
- **Level 2: Source-Derived Claim [CLAIM]** — Stated by an actor in a source document (e.g., Fauci's summary of Fouchier's stance).
- **Level 3: Algorithmic Inference [INFERENCE]** — Calculated mathematically (e.g., centrality rankings, community clusters).

Entity extraction uses **curated regex patterns** against a hand-selected target list. Plaintext OpenAlex searches are verified against ORCID records and ROR affiliations to prevent false merges.

## Limitations

Refer to `docs/LIMITATIONS.md` for a comprehensive list of analytical, network, and database limitations.

## No Warranty

THE SOFTWARE AND DATA ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. In no event shall the authors be liable for any claim, damages, or other liability arising from the use of the software or data.

## Attribution

If you use this dataset, methodology, or derived analysis in published research, please cite using the metadata in `CITATION.cff`.
