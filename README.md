# Tony's Diary — Dutch Connections & Lab-Origin Knowledge Graph

> **Automated entity extraction, network analysis, and blind-spot mapping** from Dr. Anthony Fauci's personal diary (1,141 pages, Jan 2020–Dec 2022), released by Chairman Rand Paul, U.S. Senate.  
> Focus: **Dutch institutional involvement** (Erasmus MC / Fouchier / Koopmans) and **lab-origin discussions** (Feb 1 conference call, furin cleavage site, gain-of-function).

---

## Repository Structure

```
├── src/                       # Python pipeline (stage-by-stage)
│   ├── extract_pdf.py         # Stage 1: PDF → raw_data.json (pdfplumber)
│   ├── build_kg.py            # Stage 2 (legacy): NER → SQLite + NetworkX
│   ├── build_final_dataset.py # Stage 2 (refined): Dutch/lab-origin search
│   ├── parse_all_docs.py      # Stage 3: Clean DB with target entities only
│   ├── auto_downloader.py     # External data: NIH RePORTER + OpenAlex + FOIA
│   └── export_graph.py        # Stage 4: NetworkX export + dossier generation
├── data/                      # Generated artifacts (gitignored)
│   ├── raw_data.json          # 1,141 page-wise text extractions
│   ├── network_data.db        # SQLite: nodes, edges, evidence, grants, timeline
│   ├── graph.json             # NetworkX export (node-link format)
│   ├── downloads/             # External data (NIH, OpenAlex, FOIA refs)
│   └── nl_*.json              # Intermediate extraction outputs
├── docs/                      # Reports and analysis
│   ├── DUTCH_CONNECTIONS_DOSSIER.md  # Master dossier (living document)
│   ├── BLIND_SPOT_MAPPING.md        # Epistemological audit & unknown unknowns
│   ├── ANALYSIS_REPORT.md           # Full corpus analysis
│   └── NL_EXTRACTIE_RAPPORT.md      # Dutch-specific extraction report (NL)
├── CLAUDE.md                  # AI assistant context
├── requirements.txt
├── LICENSE                    # MIT
└── README.md
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place PDF at: data/2026.07.24_Tonys-Diary-Package.pdf

# 3. Run full pipeline
python src/extract_pdf.py          # → data/raw_data.json
python src/auto_downloader.py      # → data/downloads/*.json
python src/parse_all_docs.py       # → data/network_data.db
python src/export_graph.py         # → data/graph.json + docs/dossier
```

## Key Finding

On **February 1, 2020**, Anthony Fauci convened 12 international scientists to discuss the furin cleavage site in the SARS-CoV-2 spike protein. Two Dutch virologists from Erasmus MC (Rotterdam) participated:

| Name | Position | Role on Call |
|------|----------|-------------|
| **Ron Fouchier** | Deputy Head, Dept of Viroscience | Argued furin cleavage site could occur naturally |
| **Marion Koopmans** | Head of Dept of Viroscience | Present — position **not recorded** by Fauci |

**Outcome:** No consensus. Fouchier + Drosten favored natural origin; Fauci, Collins, Andersen, Holmes, Rambaut, and others considered deliberate insertion possible given Shi Zhengli's GOF work at Wuhan Institute of Virology.

## Methodology & Philosophy

This project applies **forensic data engineering** principles:

1. **Truth-seeking, not advocacy.** No conclusions about guilt or innocence. Structured recording of facts traceable to source pages.
2. **Evidence traceability.** Every claim in the database has a `page` field linking to the PDF source. Every quote in `evidence_quotes` includes page, category, and source document.
3. **Explicit uncertainty.** Blind spots are documented in `BLIND_SPOT_MAPPING.md`. Positions that are *not* recorded (e.g., Koopmans' stance) are flagged, not fabricated.
4. **No ML hallucination.** Named entity recognition uses curated regex patterns, not LLM/NER — minimizing fabrication risk.

## Known Limitations

- The diary is Fauci's **personal narrative**, not an email archive. References to external emails (e.g., "Koopmans' Feb 9 email") come from FOIA releases, not this document.
- **Only 2 Dutch persons** found in 1,141 pages (Fouchier, Koopmans). Ab Osterhaus, RIVM, VWS are absent.
- NIH RePORTER API queries are limited to grants *mentioning* Netherlands terms, not grants *awarded to* Dutch institutions.
- OpenAlex data is limited to top-10 most-cited works per author (~15% of Fouchier's total output).

## External Data Sources

| Source | Data | Query |
|--------|------|-------|
| [NIH RePORTER](https://reporter.nih.gov/) | 50 grants mentioning Netherlands/Erasmus/RIVM | `searchText: "Netherlands OR Erasmus OR RIVM OR Koopmans OR Fouchier"` |
| [OpenAlex](https://openalex.org/) | 4 author profiles (Fouchier, Koopmans, Fauci, Farrar) + top-10 works each | `authors?search=Ron+Fouchier` |
| Washington Post FOIA | Fauci's email correspondence (separate from diary) | https://www.washingtonpost.com/context/fauci-emails/ |

## Citation

If you use this dataset or methodology in published research, please cite:

```bibtex
@software{tonys_diary_kg_2026,
  title = {Tony's Diary — Dutch Connections and Lab-Origin Knowledge Graph},
  author = {Kilo OSINT Pipeline},
  year = {2026},
  url = {https://github.com/example/tonys-diary-kg}
}
```

## License

MIT — see `LICENSE`. The source PDF is public domain (Congressional release). Extracted data and analysis scripts are freely reusable with attribution.

---

**For questions, corrections, or collaboration:** open an issue or submit a PR. This is a living document — contributions that improve accuracy, add sources, or identify blind spots are actively sought.
