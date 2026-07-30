# Dutch Pandemic Governance & Virology Network Analysis Toolkit (Multiplex Knowledge Graph)

> **Automated entity extraction, multiplex network analysis, and blind-spot mapping**
> tracing Dutch institutional involvement (Fouchier, Koopmans, Erasmus MC) and the COVID-19 lab-origin discourse (Feb 1 2020 conference call, Proximal Origin paper) from Dr. Anthony Fauci's personal diary, OpenAlex, and NIH RePORTER.

---

## Executive Summary

This repository contains a **multiplex knowledge graph** of **5,401 nodes** and **6,530 edges** spanning three relationship layers:

| Layer | Edges | What it captures |
|-------|-------|-----------------|
| **CO_AUTHOR** | 6,509 | Scientific co-authorship networks (OpenAlex top-20 works) |
| **POLICY_ADVISORY** | 19 | Meeting participation & advisory positions (Feb 1 2020 call) |
| **MEDIA_NARRATIVE** | 2 | Journalist coverage, narrative framing |

### Key Finding

On **1 February 2020**, Anthony Jeremy Farrar (Wellcome Trust) convened 12, with Anthony Fauci and Francis Collins as co-hosts international scientists to discuss the furin cleavage site in the SARS-CoV-2 spike protein. Two Dutch virologists from Erasmus MC participated:

- **Ron Fouchier** argued the site could occur naturally — "the original GOF person with Yoshi Kawaoka"
- **Marion Koopmans** was present — her position was **not recorded** by Fauci (explicit blind spot)

**Outcome:** No consensus. The group split: Fouchier + Drosten (natural origin) vs Fauci, Collins, Andersen, Holmes, Rambaut (deliberate insertion possible).

### Louvain Community Detection

The Dutch virology core (Fouchier, Koopmans, Osterhaus, Kuiken, Haagmans) forms a distinct co-author community of **708 nodes** — a densely connected Erasmus MC network operating independently of Fauci's daily awareness.

### Betweenness Centrality — Hidden Bridges

| Rank | Entity | Score | Role |
|------|--------|-------|------|
| 1 | **Arfan Ikram** (Tier 2, Erasmus MC) | 0.484 | Largest bridge in the network |
| 2 | **Menno de Jong** (Tier 2, RIVM) | 0.319 | Policy-science interface |
| 3 | **Massimo Palmarini** (Tier 2, Glasgow) | 0.318 | International connector |
| 4 | **Annemiek van der Eijk** (Tier 2, Erasmus MC) | 0.210 | Diagnostic virology hub |
| 5 | **Ernst Kuipers** (Tier 2, Erasmus MC) | 0.202 | Clinical-policy bridge |

---

## Repository Structure

```
├── src/                        # Python pipeline
│   ├── auto_downloader_v2.py   # OpenAlex + NIH + FOIA fetching (16 authors)
│   ├── setup_multiplex_db.py   # SQLite database builder
│   ├── analyze_multiplex.py    # NetworkX centrality + Louvain detection
│   └── export_multiplex.py     # graph.json + dossier generation
├── data/                       # Generated artifacts (gitignored)
│   ├── downloads/              # External data (OpenAlex, NIH, FOIA)
│   ├── network_data.db         # SQLite multiplex database
│   └── graph.json              # NetworkX export (node-link)
├── docs/
│   ├── DUTCH_CONNECTIONS_DOSSIER.md  # Master report
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
├── METHODOLOGY.md              # Methodological & legal disclaimer
└── requirements.txt            # Python dependencies
```

## Quick Start

```bash
# 1. Clone & install
pip install -r requirements.txt

# 2. Place PDF at: data/2026.07.24_Tonys-Diary-Package.pdf

# 3. Run pipeline (sequential)
python src/auto_downloader_v2.py   # Fetch OpenAlex + NIH data
python src/setup_multiplex_db.py   # Build multiplex database
python src/analyze_multiplex.py    # Centrality + community detection
python src/export_multiplex.py     # Export graph + dossier

# Alternatively, use Docker:
docker build -t virology-kg .
docker run -v $(pwd)/data:/app/data virology-kg
```

## Data Sources

| Source | Type | Coverage |
|--------|------|----------|
| **Tony's Diary** (Fauci) | Congressional document release | 1,141 pages, Jan 2020–Dec 2022 |
| **[OpenAlex](https://openalex.org/)** | Open scholarly index | 16 author profiles, top-20 works each |
| **[NIH RePORTER](https://reporter.nih.gov/)** | U.S. federal grant database | 23 queries targeting Dutch virologists + consortia |
| **WashPost FOIA** | Fauci email correspondence | Reference link (separate from diary) |

## Tiered Target Nodes

- **Tier 1** (Direct Core): Fouchier, Koopmans, Osterhaus, Kuiken, Haagmans, Van Dissel, Gommers, Kluytmans
- **Tier 2** (Institutional Bridges): Timen, De Jong, Bonten, Van der Eijk, Palmarini, Ikram, Kuipers
- **Tier 3** (Media/Narrative): Maarten Keulemans (Volkskrant)
- **Consortia**: PDPC, NCOH, VEO, DURABLE, ECRAID, ESWI, ZonMw

## Known Limitations

1. **Diary ≠ Email archive** — Fauci's diary is a personal narrative, not a complete correspondence log
2. **Limited diary coverage of Dutch actors** — Only 2 of 16 Tier-1/2 persons appear in 1,141 pages
3. **OpenAlex top-20 sampling** — Co-author network incomplete (~15% of Fouchier's output)
4. **Consortium funding layer = 0 edges** — No ZonMw or EU Horizon data ingested
5. **No ML/NER** — Regex-only entity extraction (intentional — minimizes hallucination risk)

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

---

*This is a living document. Contributions that improve accuracy, add sources, or identify blind spots are actively sought — see `CONTRIBUTING.md`.*
