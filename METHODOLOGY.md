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
- Analyzed only in terms of **professional network relationships** (co-authorship, advisory roles, institutional affiliation)

**No personal data** (addresses, phone numbers, private correspondence, health data, political opinions) is collected, stored, or published.

This processing falls within the "journalistic, academic, artistic or literary expression" exemption of GDPR Article 85 and equivalent implementations (Dutch UAVG Art. 43), and the "legitimate interest" basis for processing publicly available professional data of public figures.

## Methodological Rigor

### Evidence Traceability
Every claim in the database includes a `page` or `source_doc` field linking directly to the source material. Every quote in `evidence_quotes` includes the document name and page number.

### Uncertainty Markers
- **Explicit blind spots** are documented in `docs/BLIND_SPOT_MAPPING.md`
- Positions that are *not* recorded (e.g., Koopmans' stance on the Feb 1 call) are flagged, not fabricated
- All network metrics (betweenness, eigenvector, Louvain) are computed algorithmically and presented with their raw scores — no interpretation is imposed

### No ML Hallucination
Entity extraction uses **curated regex patterns** against a hand-selected target list, not LLM or NER-based extraction. This minimizes fabrication risk but may produce false negatives (persons who are mentioned in the text but not in the target list).

### Limitations
- The source diary is Fauci's **personal narrative**, not an objective record
- OpenAlex data is limited to **top-20 most-cited works** per author
- NIH RePORTER queries are limited to mentions of search terms, not comprehensive grant awards
- Edges in the graph represent **co-occurrence in the data layer**, not necessarily real-world relationships

## No Warranty

THE SOFTWARE AND DATA ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. In no event shall the authors be liable for any claim, damages, or other liability arising from the use of the software or data.

## Attribution

If you use this dataset, methodology, or derived analysis in published research, please cite using the metadata in `CITATION.cff`.
