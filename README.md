# Dutch Pandemic Governance & Virology Network Analysis Toolkit (Knowledge Graph)

> **Automated entity extraction, multiplex network analysis, and blind-spot mapping**
> tracing Dutch institutional involvement (Fouchier, Koopmans, Erasmus MC) and the COVID-19 lab-origin discourse (Feb 1 2020 conference call, Proximal Origin paper) from Dr. Anthony Fauci's personal diary, OpenAlex, and NIH RePORTER.

---

## Executive Summary

This repository contains a **knowledge graph** spanning relationship layers:

| Layer | What it captures |
|-------|-----------------|
| **CO_AUTHOR** | Scientific co-authorship networks (OpenAlex publications) |
| **POLICY_ADVISORY** | Meeting participation & advisory positions (Feb 1 2020 call) |
| **MEDIA_NARRATIVE** | Journalist coverage, narrative framing |

### Key Finding

On **1 February 2020**, Anthony Jeremy Farrar (Wellcome Trust) convened an international group of 12 scientists, with Anthony Fauci and Francis Collins as co-hosts, to discuss the furin cleavage site in the SARS-CoV-2 spike protein. Two Dutch virologists from Erasmus MC participated:

- **Ron Fouchier** argued the site could occur naturally — "the original GOF person with Yoshi Kawaoka" (Fauci diary p14 characterization)
- **Marion Koopmans** was present — her position was **not recorded** by Fauci (explicit blind spot)

**Outcome:** No consensus. The group split: Fouchier + Drosten (natural origin) vs Fauci, Collins, Andersen, Holmes, Rambaut (deliberate insertion possible).

### Leiden/Louvain Community Detection

Dynamic sub-graph clustering on the co-authorship layer groups Ron Fouchier, Marion Koopmans, Thijs Kuiken, Bart Haagmans, and Ab Osterhaus into a densely connected Erasmus MC / Dutch virology core community. 

*Note: Algorithmic community assignments are based purely on publication co-occurrence statistics and do NOT represent personal agreements, political alignments, or scientific consensus. Refer to the disclaimers in `docs/LIMITATIONS.md` and `docs/EVIDENCE_TAXONOMY.md`.*

### Betweenness Centrality — Hidden Bridges

Centrality calculations are performed on the weighted simple graph projection of the multiplex graph. Virology-filtered betweenness centrality highlights key connectors (such as Marion Koopmans, Ron Fouchier, and Menno de Jong) bridging policy, advisory, and academic research. Sizing nodes by betweenness centrality visually represents structural connectivity in the data, not culpability or influence.

---

## Repository Structure

```
├── src/                        # Python pipeline
│   ├── auto_downloader_v2.py   # Ingest OpenAlex (ORCID-seeded) + NIH + FOIA
│   ├── setup_multiplex_db.py   # SQLite database builder (data-loss fixed)
│   ├── analyze_multiplex.py    # NetworkX centrality (MultiGraph) + Louvain
│   ├── setup_sql_views.py      # Forensic SQLite views
│   ├── export_forensic_data.py # Export Parquet + CSV + SHA-256
│   └── export_multiplex.py     # graph.json + dossier generation (dynamic communities)
├── data/                       # Generated artifacts (gitignored)
│   ├── downloads/              # External data (OpenAlex, NIH, FOIA)
│   ├── network_data.db         # SQLite multiplex database
│   └── graph.json              # NetworkX export (node-link MultiGraph)
├── docs/
│   ├── LIMITATIONS.md          # Methodological disclaimers [NEW]
│   ├── EVIDENCE_TAXONOMY.md    # Evidence verifiability levels [NEW]
│   ├── CORRECTION_POLICY.md    # Notice and Takedown & Right-of-Reply [NEW]
│   ├── DUTCH_CONNECTIONS_DOSSIER.md  # Master report (dynamic community data)
│   ├── BLIND_SPOT_MAPPING.md        # Epistemological audit
│   └── ANALYSIS_REPORT.md           # Full corpus analysis
├── .env.example                # Environment variables template
├── CITATION.cff                # Citation metadata
├── CLAUDE.md                   # AI assistant context
├── CONTRIBUTING.md             # Contribution guidelines
├── Dockerfile                  # Containerized execution
├── LICENSE                     # MIT
├── llms.txt                    # LLM index
├── llm-context.md              # Detailed AI context
├── METHODOLOGY.md              # Methodological & legal disclaimer (patched)
└── requirements.txt            # Python dependencies
```

## Quick Start

```bash
# 1. Clone & install
pip install -r requirements.txt

# 2. Extract PDF text (requires 2026.07.24_Tonys-Diary-Package.pdf in data/)
python src/extract_pdf.py

# 3. Run pipeline (sequential)
python src/auto_downloader_v2.py     # Ingest OpenAlex (ORCID) + NIH RePORTER
python src/setup_multiplex_db.py     # Build SQLite database
python src/analyze_multiplex.py      # MultiGraph centrality + Leiden
python src/setup_sql_views.py        # Build SQLite forensic views
python src/export_forensic_data.py   # Export Parquet/CSV and compute SHA-256
python src/enrich_expert_layers.py   # Ingest BIG, DEFUSE and Woo references
python build_web_app.py              # Export visualization docs/data.json
python src/export_multiplex.py       # Generate Master Dossier and graph.json

# Alternatively, use Docker:
docker build -t virology-kg .
docker run -v $(pwd)/data:/app/data virology-kg
```

## Data Ingestion & Quality

* **ORCID-Seeded Ingestion:** To prevent false merges with homonyms, the OpenAlex ingest query is seeded using verified ORCID identifiers.
* **Erasmus MC ROR Filter:** The pipeline queries OpenAlex using ROR institutional code `https://ror.org/018906e22` for Erasmus MC target authors without ORCID to enforce data quality.
* **Verification Ledgers:** All policy and media edges are verified against primary citations and published with complete URL references.

---

## Citation

```bibtex
@software{dutch_virology_kg_2026,
  title = {Dutch Pandemic Governance \& Virology Network Analysis Toolkit},
  author = {Kilo OSINT Research Team},
  year = {2026},
  url = {https://github.com/TriggerMinds/dutch-virology-network-analysis}
}
```

## License

MIT — see `LICENSE`. Source PDF is public domain (U.S. Congressional release).
