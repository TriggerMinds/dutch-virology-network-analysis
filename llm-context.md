# LLM Context: Dutch Virology Multiplex Knowledge Graph

## Database Architecture (`network_data.db`)

### Tables

#### `nodes`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| name | TEXT UNIQUE | Entity name (person, org, event, publication) |
| entity_type | TEXT | person / organization / consortium / event / position / publication |
| tier | INTEGER | 0=global, 1=Dutch core, 2=institutional bridge, 3=media |
| organization | TEXT | Primary institutional affiliation |
| primary_role | TEXT | Scientific role / specialty |

#### `edges`
| Column | Type | Description |
|--------|------|-------------|
| source_id | INTEGER FK → nodes.id | Source node |
| target_id | INTEGER FK → nodes.id | Target node |
| layer_type | TEXT | CO_AUTHOR / POLICY_ADVISORY / CONSORTIUM_FUNDING / MEDIA_NARRATIVE |
| date | TEXT | Date or year of relationship |
| description | TEXT | Contextual evidence (up to 300 chars) |
| source_doc | TEXT | Document reference (page or DOI) |
| weight | INTEGER | Edge weight (default 1) |

#### `evidence_quotes`
| Column | Description |
|--------|-------------|
| entity_name | Person or org mentioned |
| exact_quote | Verbatim quote from source |
| page_number | PDF page number |
| document_name | Source document |

#### `timeline`
| Column | Description |
|--------|-------------|
| date | Event date |
| event_type | trigger / meeting / publication / declaration / FOIA release |
| description | Event summary |
| actors_involved | Key participants |
| source_ref | Document reference |

## Layer Definitions

| Layer | Type | Description | Example edges |
|-------|------|-------------|---------------|
| CO_AUTHOR | Scientific | Co-authorship on publications | Fouchier ↔ Drosten (via MERS-CoV paper) |
| POLICY_ADVISORY | Governance | Meeting participation, advisory positions | Fouchier → Feb 1 Conference Call (participant) |
| CONSORTIUM_FUNDING | Financial | Grant funding to consortia | (currently 0 edges — requires ZonMw/EU CORDIS import) |
| MEDIA_NARRATIVE | Media | Journalist coverage, public narrative | Keulemans ↔ Proximal Origin Paper |

## Key Computational Results

### Betweenness Centrality (ALL layers)
- Arfan Ikram: 0.4836 (top bridge — Erasmus MC epidemiology)
- Menno de Jong: 0.3191 (RIVM policy-science bridge)
- Massimo Palmarini: 0.3184 (Glasgow — international connector)
- Annemiek van der Eijk: 0.2095 (Erasmus MC virology)
- Ernst Kuipers: 0.2017 (Erasmus MC — clinical/policy bridge)

### Policy Layer Betweenness
- Feb 1 Conference Call: 0.6970 (dominant node)
- Ron Fouchier: 0.0758 (tying with Christian Drosten)
- Deliberate Insertion Hypothesis: 0.1591

### Louvain Communities (CO_AUTHOR)
- **Community 2** (708 nodes): Erasmus MC core — Fouchier, Koopmans, Osterhaus, Kuiken, Haagmans
- **Community 6** (1,077 nodes): RIVM/UMCU — De Jong, Bonten
- **Community 9** (1,256 nodes): Epidemiology — Ikram
- **Community 7** (755 nodes): International virology — Palmarini

## Critical Source Data

- **Tony's Diary**: Only 2 of 16 Tier-1/2 Dutch virologists appear (Fouchier 2×, Koopmans 1×, both on p14)
- **OpenAlex**: 16 author profiles with top-20 works each (~8,800 co-author edges)
- **NIH RePORTER**: 23 queries, 0 direct grants to Dutch institutions found
- **Consortium edges**: Currently 0 (requires ZonMw / EU CORDIS data)

## Methodological Limitations
1. Diary is Fauci's personal narrative — not an email archive
2. OpenAlex limited to top-20 works per author
3. No ML-based NER (intentional — regex-only to avoid hallucination)
4. Koopmans' position on deliberate-vs-natural origin not recorded by Fauci
5. Consortium funding layer empty — no ZonMw or EU Horizon data ingested yet
