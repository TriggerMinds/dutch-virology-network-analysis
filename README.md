[![Pipeline](https://img.shields.io/badge/Pipeline-Passing-brightgreen)](https://github.com/TriggerMinds/dutch-virology-network-analysis/actions)
[![Nodes](https://img.shields.io/badge/Nodes-4929-blue)](https://triggerminds.github.io/dutch-virology-network-analysis/)
[![Edges](https://img.shields.io/badge/Edges-7934-blue)](https://triggerminds.github.io/dutch-virology-network-analysis/)
[![SHA-256](https://img.shields.io/badge/SHA--256-Verified-success)](https://github.com/TriggerMinds/dutch-virology-network-analysis/blob/main/data/checksums.sha256)
[![TEAMDYNAMICA](https://img.shields.io/badge/TEAMDYNAMICA-v1.5--Compliant-success)](TEAMDYNAMICA.md)
[![Wiki](https://img.shields.io/badge/GitHub%20Wiki-Live-blue)](https://github.com/TriggerMinds/dutch-virology-network-analysis/wiki)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/TriggerMinds/dutch-virology-network-analysis/blob/main/LICENSE)
[![Web App](https://img.shields.io/badge/GitHub%20Pages-Live%20Web%20App-success)](https://triggerminds.github.io/dutch-virology-network-analysis/)

# Dutch Pandemic Governance & Virology Network Analysis Toolkit (Knowledge Graph & Forensics)

> **Automated entity extraction, meertalige SQLite FTS5 documentzoekmachine, redaction delta-tracking, open macro-data harvesters, multiplex network analysis, global FOIA forensics, en blind-spot mapping.**  
> Tracing Dutch institutional involvement (Erasmus MC, Ron Fouchier, Marion Koopmans, Ab Osterhaus, RIVM, OMT, AIVD) and cross-border European pandemic policy alignment (Feb 1 2020 conference call, *Proximal Origin* paper, Corman-Drosten PCR fast-track <48h, RKI-Protokolle leaks, Bergamo inchiesta, French Senate mask dissimulation, Spanish Caso Koldo) from Dr. Anthony Fauci's personal diary, USRTK FOIA disclosures, U.S. House Select Subcommittee records, OpenAlex, NIH RePORTER v2 API, EU CORDIS, CBS StatLine OData, Tweede Kamer OData, and patent databases.

---

## Executive Summary & Core Forensic Dossiers

This repository contains a **multiplex knowledge graph**, a **multi-lingual document archive (`data/archive.db`)**, and a forensic analysis suite built strictly under **TEAMDYNAMICA v1.5** evidence-first rules.

### Master Forensic Dossiers & Reports

| Document | Description & Key Findings |
|----------|----------------------------|
| **[OPERATIONAL_INVESTIGATIVE_MANUAL.md](docs/OPERATIONAL_INVESTIGATIVE_MANUAL.md)** | **Operational Manual & Promptbook**: Complete hands-on guide with terminal commands, SQLite FTS5 queries, redaction delta scripts, and AI research prompts for truth-seeking. |
| **[EU_MEMBER_STATES_FORENSIC_DOSSIER.md](docs/EU_MEMBER_STATES_FORENSIC_DOSSIER.md)** | **Cross-Border EU Forensic Audit**: Analyzes Germany (RKI-Protokolle leaks), Italy (Procura di Bergamo inchiesta #3274/2020 WG), France (Sénat Rapport n° 199 mask dissimulation), Spain (Caso Koldo procurement corruption), Belgium (Chambre des représentants), and EU Parliament (COVI Committee & Von der Leyen SMS audit). |
| **[MASTER_UNTURNED_STONES_AUDIT.md](docs/MASTER_UNTURNED_STONES_AUDIT.md)** | **Master Unturned Stones Audit**: Evaluates all missing files, 68.5% WOO redactions (Art. 5.2), AIVD circular evidence loop, 20.800+ unexplained excess mortality gap, and the top 7 highest-leverage WOO/FOIA targets. |
| **[DUTCH_ANOMALIES_FORENSIC_AUDIT.md](docs/DUTCH_ANOMALIES_FORENSIC_AUDIT.md)** | **Dutch Specific Forensic Audit**: Documents the 6 core Dutch anomalies (Corman-Drosten PCR fast-track <48h without Wuhan sample, OMT double-hats & €67,6M+ funding concentration, Viroscience B.V. private spin-off, 107-day media narrative lag). |
| **[GLOBAL_FOIA_PROXIMAL_ORIGIN_DOSSIER.md](docs/GLOBAL_FOIA_PROXIMAL_ORIGIN_DOSSIER.md)** | **Proximal Origin Draft Feedback Dossier**: Analyzes USRTK FOIA & Congressional emails (Feb 2020) detailing Fouchier and Koopmans' substantive draft feedback and pushback against lab-origin phrasing via Jeremy Farrar. |
| **[GLOBAL_SOURCES_DUTCH_COVID_ROLE.md](docs/GLOBAL_SOURCES_DUTCH_COVID_ROLE.md)** | **Consolidated Master Forensic Report**: Comprehensive analysis across 6 priority search domains, cross-referencing Dutch actors with international counterparts (Fauci, Farrar, Collins, Baric, Daszak, Drosten). |
| **[BLIND_SPOT_MAPPING.md](docs/BLIND_SPOT_MAPPING.md)** | **Critical Blind-Spot Mapping & Audit**: Epistemological audit of findings, qualifying PREDICT sub-awards (`PRIMARY_DOCS_REQUIRED`) and Corman-Drosten editorial records (`TO_BE_CONFIRMED`). |
| **[DUTCH_CONNECTIONS_DOSSIER.md](docs/DUTCH_CONNECTIONS_DOSSIER.md)** | **Multiplex Network Dossier**: Centrality, betweenness, and community structure across `CO_AUTHOR`, `POLICY_ADVISORY`, `CONSORTIUM_FUNDING`, and `MEDIA_NARRATIVE` layers. |
| **[EXPERT_GUIDE.md](docs/EXPERT_GUIDE.md)** | **Developer & Forensic Query Guide**: SQL and Python code snippets for querying `data/archive.db`, FTS5 full-text search, `redaction_deltas`, CBS StatLine macro-data, and `coverage_status` dictionaries. |
| **[TEAMDYNAMICA.md](TEAMDYNAMICA.md)** | **Independent COVID Truth-Finding Rules (v1.5)**: 11-bias deactivation protocol and the 4-Axis Forensic Qualification Framework (**Intentie, Causaliteit, Verantwoordelijkheid, Timing**). |

---

## Data Engineering Architecture & Pipelines

The repository features four core automated data engineering pipelines:

```
                               DATA ENGINEERING ARCHITECTURE
┌───────────────────────────────┐     ┌───────────────────────────────┐     ┌───────────────────────────────┐
│     SQLite Archive DB         │     │     Redaction Delta Tracker   │     │    Open Macro-Data Harvester  │
│      (data/archive.db)        │     │(src/track_redaction_deltas.py)│     │(src/fetch_open_macro_data.py) │
│ - FTS5 Virtual Table Index    │     │ - Page-by-page PDF Diffing    │     │ - CBS StatLine OData API      │
│ - SHA-256 Provenance Hashing  │     │ - Version A vs B Snippets     │     │ - Tweede Kamer OData API      │
│ - EuroVoc Taxonomy Topics     │     │ - Stores to redaction_deltas  │     │ - Crossref DOI API            │
└──────────────┬────────────────┘     └──────────────┬────────────────┘     └──────────────┬────────────────┘
               │                                     │                                     │
               └─────────────────────────────────────┼─────────────────────────────────────┘
                                                     ▼
                                      ┌───────────────────────────────┐
                                      │  Coverage Status Dictionary   │
                                      │(src/build_coverage_dictionary)│
                                      │ - VERIFIED_PUBLIC             │
                                      │ - STATUTORY_RESTRICTED        │
                                      │ - PENDING_APPEAL              │
                                      └──────────────┬────────────────┘
                                                     ▼
                                      ┌───────────────────────────────┐
                                      │    Multiplex Knowledge Graph  │
                                      │   (data/network_data.db)      │
                                      │  - 4,929 Nodes / 7,934 Edges  │
                                      │  - Interactive Web App        │
                                      └───────────────────────────────┘
```

---

## Knowledge Graph Layers & Data Coverage

| Layer | What it captures | Primary Data Sources |
|-------|------------------|----------------------|
| **CO_AUTHOR** | Scientific co-authorship networks (7,882 edges) | OpenAlex API, PubMed, Crossref |
| **POLICY_ADVISORY** | Meeting participation, FOIA draft reviews, advisory positions (19 edges) | U.S. House Select Subcommittee, Tony's Diary, USRTK FOIA |
| **CONSORTIUM_FUNDING** | EU Horizon 2020 & ZonMw grant flows (€67,6M+ total) | EU CORDIS REST API, NIH RePORTER v2 API, ZonMw Ledgers |
| **MEDIA_NARRATIVE** | Science journalist coverage and narrative lag tracking (107 days lag) | Volkskrant, NOS, VWS Press Directives |

### Coverage Status Dictionary

Every node, document, and quote is tagged with an explicit coverage status badge:
- **`VERIFIED_PUBLIC`**: 100% public, verified HTTP 200 OK source document.
- **`STATUTORY_RESTRICTED`**: Redacted under Art. 5.1/5.2 Woo or GDPR statutory restrictions.
- **`PENDING_APPEAL`**: Open Woo/FOIA appeal or primary documentation pending (`PRIMARY_DOCS_REQUIRED`).

---

## TEAMDYNAMICA v1.5 Standard & 4-Axis Qualification

All claims in this repository are strictly qualified under the **4-Axis Forensic Qualification Framework**:

1. **Intentie (Intent):** Premeditated intent vs. institutional self-preservation vs. scientific reflex.
2. **Causaliteit (Causality):** Direct control/steering vs. substantive expert feedback that contributed to text.
3. **Verantwoordelijkheid (Responsibility):** Executive decision-maker vs. formal co-author vs. external consultant.
4. **Timing (Chronology):** Contemporaneous knowledge (Feb 2020) vs. retrospective reconstruction.

---

## Quick Start & Pipeline Execution

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize Archive DB & Ingest PDFs
python src/init_archive_db.py
python src/ingest_pdf_archive.py

# 3. Run Data Engineering Modules
python src/track_redaction_deltas.py
python src/fetch_open_macro_data.py
python src/fetch_open_academic_data.py
python src/sync_cordis_open_data.py
python src/verify_open_documents.py

# 4. Rebuild Multiplex Database & Interactive Web App
python src/setup_multiplex_db.py
python src/build_coverage_dictionary.py
python build_web_app.py

# 5. Run Unit Tests
python tests/test_archive_db.py
```

---

## GitHub Wiki & Online Documentation

Visit the official [GitHub Wiki](https://github.com/TriggerMinds/dutch-virology-network-analysis/wiki) for full-length Dutch language wiki articles:
- [Master-Unturned-Stones-Audit](https://github.com/TriggerMinds/dutch-virology-network-analysis/wiki/Master-Unturned-Stones-Audit)
- [Europese-Parlementaire-Onderzoeken](https://github.com/TriggerMinds/dutch-virology-network-analysis/wiki/Europese-Parlementaire-Onderzoeken)
- [Nederlandse-Anomalieen-en-Belangen](https://github.com/TriggerMinds/dutch-virology-network-analysis/wiki/Nederlandse-Anomalieen-en-Belangen)
- [Global-FOIA-Proximal-Origin](https://github.com/TriggerMinds/dutch-virology-network-analysis/wiki/Global-FOIA-Proximal-Origin)

---

## License

MIT — see `LICENSE`. Source documents are U.S. Congressional releases, European parliamentary records, and public FOIA disclosures.
