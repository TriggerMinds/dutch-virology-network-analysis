[![Pipeline](https://img.shields.io/badge/Pipeline-Passing-brightgreen)](https://github.com/TriggerMinds/dutch-virology-network-analysis/actions)
[![Nodes](https://img.shields.io/badge/Nodes-4929-blue)](https://triggerminds.github.io/dutch-virology-network-analysis/)
[![Edges](https://img.shields.io/badge/Edges-7934-blue)](https://triggerminds.github.io/dutch-virology-network-analysis/)
[![SHA-256](https://img.shields.io/badge/SHA--256-Verified-success)](https://github.com/TriggerMinds/dutch-virology-network-analysis/blob/main/data/checksums.sha256)
[![TEAMDYNAMICA](https://img.shields.io/badge/TEAMDYNAMICA-v1.5--Compliant-success)](TEAMDYNAMICA.md)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/TriggerMinds/dutch-virology-network-analysis/blob/main/LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://triggerminds.github.io/dutch-virology-network-analysis/)

# Dutch Pandemic Governance & Virology Network Analysis Toolkit (Knowledge Graph)

> **Automated entity extraction, multiplex network analysis, global FOIA forensics, and blind-spot mapping**  
> Tracing Dutch institutional involvement (Erasmus MC, Fouchier, Koopmans, Osterhaus, RIVM, OMT) and the COVID-19 lab-origin discourse (Feb 1 2020 conference call, Proximal Origin paper, Corman-Drosten PCR fast-track) from Dr. Anthony Fauci's personal diary, USRTK FOIA disclosures, U.S. House Select Subcommittee records, OpenAlex, NIH RePORTER, and patent databases.

---

## Executive Summary & Core Dossiers

This repository contains a **multiplex knowledge graph** and forensic analysis suite built strictly under **TEAMDYNAMICA v1.5** evidence-first rules.

### Major Forensic Dossiers & Reports

| Document | Description & Key Findings |
|----------|----------------------------|
| **[BLIND_SPOT_MAPPING.md](docs/BLIND_SPOT_MAPPING.md)** | **Critical Blind-Spot Mapping & Audit**: Evaluates the top 7 highest-leverage blind spots (Fouchier/Koopmans *Proximal Origin* draft feedback, USAID PREDICT sub-awards open blind spot, Corman-Drosten PCR fast-track, BsmBI/BsaI patent overlap). |
| **[GLOBAL_FOIA_PROXIMAL_ORIGIN_DOSSIER.md](docs/GLOBAL_FOIA_PROXIMAL_ORIGIN_DOSSIER.md)** | **Proximal Origin Draft Feedback Dossier**: Analyzes USRTK FOIA & Congressional emails (Feb 2020) detailing Fouchier and Koopmans' substantive draft feedback and pushback against lab-origin phrasing via Jeremy Farrar. |
| **[GLOBAL_SOURCES_DUTCH_COVID_ROLE.md](docs/GLOBAL_SOURCES_DUTCH_COVID_ROLE.md)** | **Consolidated Master Forensic Report**: Comprehensive analysis across 6 priority search domains, cross-referencing Dutch actors with international counterparts (Fauci, Farrar, Collins, Baric, Daszak, Drosten). |
| **[DUTCH_CONNECTIONS_DOSSIER.md](docs/DUTCH_CONNECTIONS_DOSSIER.md)** | **Multiplex Network Dossier**: Centrality, betweenness, and community structure across `CO_AUTHOR`, `POLICY_ADVISORY`, `CONSORTIUM_FUNDING`, and `MEDIA_NARRATIVE` layers. |
| **[TEAMDYNAMICA.md](TEAMDYNAMICA.md)** | **Independent COVID Truth-Finding Rules (v1.5)**: Bias deactivation protocol and the 4-Axis Forensic Qualification Framework (**Intentie, Causaliteit, Verantwoordelijkheid, Timing**). |

---

## Knowledge Graph Layers & Architecture

| Layer | What it captures |
|-------|-----------------|
| **CO_AUTHOR** | Scientific co-authorship networks (OpenAlex publications & peer-reviewed papers) |
| **POLICY_ADVISORY** | Meeting participation, FOIA draft reviews, advisory positions (Feb 1 2020 call, Proximal Origin feedback) |
| **CONSORTIUM_FUNDING** | EU Horizon 2020 (VEO, COMPARE, DURABLE, ECRAID) & ZonMw grant flows |
| **MEDIA_NARRATIVE** | Science journalist coverage and narrative lag tracking (Volkskrant, NOS) |

---

## TEAMDYNAMICA v1.5 Standard & 4-Axis Qualification

All claims in this repository are strictly qualified under the 4-Axis Forensic Qualification Framework:

1. **Intentie (Intent):** Premeditated intent vs. institutional self-preservation vs. scientific reflex.
2. **Causaliteit (Causality):** Direct control/steering vs. substantive expert feedback that contributed to text.
3. **Verantwoordelijkheid (Responsibility):** Executive decision-maker vs. formal co-author vs. external consultant.
4. **Timing (Chronology):** Contemporaneous knowledge (Feb 2020) vs. retrospective reconstruction.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run ingestion & database setup
python src/ingest_international_foia.py
python src/setup_multiplex_db.py
python src/analyze_multiplex.py

# 3. Export web app & graph visualizations
python build_web_app.py
python src/export_multiplex.py
```

---

## License

MIT — see `LICENSE`. Source documents are U.S. Congressional and public FOIA releases.
