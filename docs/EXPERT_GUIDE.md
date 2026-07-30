# Expert Guide — Dutch Virology Network Analysis Toolkit

> **Doelgroep:** Forensische data-analisten, OSINT-onderzoekers, moleculair biologen.
> **Datasets:** SQLite (`network_data.db`), Parquet (`data/parquet/`), CSV (`data/csv/`), SHA-256 (`data/checksums.sha256`).

---

## 1. SQLite Forensische Views

De volgende views zijn pre-compiled in `network_data.db`:

| View | Rijen | Beschrijving |
|------|-------|-------------|
| `vw_forensic_grants` | 4 | EU consortium grants (VEO, ECRAID, DURABLE, COMPARE) met bedragen en coördinatoren |
| `vw_woo_citations` | 3 | Bewijscitaten gekoppeld aan Woo-dossiernummers en openbare bronnen |
| `vw_conflict_of_interest` | 16 | Belangenmatrix: academische rol, beleidsrol, subsidie-beoordelingsrol, media-rol per Tier 1-3 persoon |
| `vw_virology_betweenness` | 195 | Virologie-gefilterde betweenness centrality per node (exclusief algemene epidemiologie) |

### SQL-voorbeelden voor DuckDB / SQLite

```sql
-- Top virology bridges
SELECT name, org, virology_betweenness
FROM vw_virology_betweenness
WHERE virology_betweenness > 0.1
ORDER BY virology_betweenness DESC;

-- Full conflict-of-interest matrix
SELECT name, tier, academic_role, policy_role, grant_review_role, media_role
FROM vw_conflict_of_interest
WHERE tier <= 2;

-- Grants funded to specific consortium
SELECT * FROM vw_forensic_grants
WHERE grant_or_consortium IN ('VEO', 'ECRAID');

-- Woo citations for a specific entity
SELECT * FROM vw_woo_citations
WHERE entity_name LIKE '%Koopmans%';
```

## 2. SHA-256 Checksum Verificatie

Alle gegenereerde data-bestanden zijn voorzien van SHA-256 hashes voor forensische verifieerbaarheid.

### Verifiëren op Linux/macOS

```bash
cd data
sha256sum -c checksums.sha256
```

### Verifiëren op Windows (PowerShell)

```powershell
Get-Content data\checksums.sha256 | ForEach-Object {
    $hash, $file = $_ -split '  ', 2
    $computed = (Get-FileHash $file -Algorithm SHA256).Hash.ToLower()
    if ($hash -eq $computed) { Write-Host "$file: OK" -ForegroundColor Green }
    else { Write-Host "$file: FAILED" -ForegroundColor Red }
}
```

### Verifiëren in Python

```python
import hashlib, os
with open("data/checksums.sha256") as f:
    for line in f:
        expected_hash, filepath = line.strip().split("  ", 1)
        actual_hash = hashlib.sha256(open(filepath, "rb").read()).hexdigest()
        assert expected_hash == actual_hash, f"{filepath} hash mismatch"
print("All files verified.")
```

## 3. Parquet & CSV Exports

Bestanden in `data/parquet/` en `data/csv/`:

| Bestand | Formaat | Rijen | Inhoud |
|---------|---------|-------|--------|
| `centrality_flat` | Parquet/CSV | 33.584 | Betweenness, degree, eigenvector scores per node per laag (genormaliseerd) |
| `vw_forensic_grants` | Parquet/CSV | 4 | Consortium grants |
| `vw_woo_citations` | Parquet/CSV | 3 | Woo-referenties |
| `vw_conflict_of_interest` | Parquet/CSV | 16 | Belangenmatrix |
| `vw_virology_betweenness` | Parquet/CSV | 195 | Virologie-gefilterde centraliteit |

### Verwerken met DuckDB

```sql
-- Analyseer centraliteit per laag
SELECT layer, COUNT(*) as nodes, AVG(score) as avg_score
FROM 'data/parquet/centrality_flat.parquet'
WHERE metric = 'betweenness'
GROUP BY layer
ORDER BY avg_score DESC;

-- Join tussenness met conflict-of-interest
SELECT b.name, b.virology_betweenness, c.policy_role, c.grant_review_role
FROM 'data/parquet/vw_virology_betweenness.parquet' b
JOIN 'data/parquet/vw_conflict_of_interest.parquet' c ON b.name = c.name
ORDER BY b.virology_betweenness DESC;
```

## 4. Genomische DURC-Relevante Publicaties

Tabel `durc_genomics` identificeert publicaties met **Dual-Use Research of Concern** (DURC) relevantie.

| Categorie | Aantal | Voorbeelden |
|-----------|--------|-------------|
| GOF_influenza | 1 | Fouchier H5N1 ferret (2012) — 5 mutations enable aerosol transmission |
| coronavirus_discovery | 1 | Fouchier MERS-CoV discovery (2012) |
| diagnostic | 1 | Koopmans nCoV real-time RT-PCR (2020) |
| coronavirus_pathogenesis | 1 | Koopmans SARS-CoV-2 gut enterocytes (2020) |
| origin_debate | 1 | Proximal Origin paper (Andersen et al. 2020/2022) |
| spike_ace2 | 1 | Shi Zhengli spike-ACE2 characterization (2020) |
| influenza_surveillance | 1 | Fouchier influenza evolution mapping (2004) |

### DURC-criteria (WHO/NSABB gedefinieerd):

1. **Enhances pathogen virulence** — Fouchier H5N1
2. **Disrupts immunity** — N.v.t.
3. **Confers resistance** — N.v.t.
4. **Enhances transmissibility** — Fouchier H5N1
5. **Alters host range** — Shi Zhengli ACE2 adaptation
6. **Evades detection** — N.v.t.
7. **Enables weaponization** — N.v.t.

### Volledige lijst:

```sql
SELECT title, authors, publication_year, durc_category
FROM durc_genomics
ORDER BY publication_year;
```

## 5. Woo-document Register

Tabel `woo_documents` bevat verifieerbare Woo-dossiernummers en openbare bronnen:

| Woo-nummer | Bron | Relevantie |
|-----------|------|-----------|
| Woo/3661708 | RIVM OMT adviezen | NL beleidsreactie COVID-19 |
| Woo/VWS-2021-001 | VWS subsidiebesluiten | ZonMw/NCOH/PDPC financiering |
| Woo/EU-CORDIS-VEO | EU Horizon 2020 | Koopmans VEO coordinator |
| Woo/EU-CORDIS-ECRAID | EU Horizon 2020 | Bonten ECRAID coordinator |
| Woo/US-NIH-2R01AI110964 | NIH RePORTER | EcoHealth/Daszak grant naar WIV |
| Woo/US-PARLIAMENT-FARRAR | UK Parliament | Farrar testimony over Jan 31 call |

## 6. Pipeline Reproductie

```bash
# Volledige data-pipeline (vereist PDF in data/)
pip install -r requirements.txt
python src/auto_downloader_v2.py     # OpenAlex + NIH
python src/setup_multiplex_db.py     # Bouw SQLite
python src/analyze_multiplex.py      # Centraliteit + communities
python src/setup_sql_views.py        # Forensische views
python src/export_forensic_data.py   # Parquet/CSV/SHA-256
python src/enrich_expert_layers.py   # Woo + DURC
python build_web_app.py              # Web visualisatie
python src/export_multiplex.py       # Graph + dossier export
```

## 7. Bestandsstructuur (forensisch relevant)

```
data/
├── network_data.db          SQLite (centrale database)
├── graph.json               NetworkX export
├── checksums.sha256         SHA-256 hashes (alle exports)
├── parquet/                 Parquet exports (5 bestanden)
├── csv/                     CSV exports (5 bestanden)
├── downloads/               Ruwe API-data (OpenAlex, NIH, FOIA)
docs/
├── DUTCH_CONNECTIONS_DOSSIER.md   Master rapport
├── BLIND_SPOT_MAPPING.md          Epistemologische audit
├── EXPERT_GUIDE.md                Deze handleiding
src/
├── setup_sql_views.py             View creatie
├── export_forensic_data.py        Parquet/CSV/SHA export
├── enrich_expert_layers.py        Woo + DURC
└── analyze_multiplex.py           Centraliteit + communities
```

---

*Laatste update: 2026-07-30. Voor vragen of correcties: open een GitHub Issue.*
