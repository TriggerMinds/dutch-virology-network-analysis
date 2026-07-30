# Forensische SQL Views — DuckDB/Parquet Handleiding

## Database locatie
De centrale SQLite database staat in `data/network_data.db`. Parquet exports staan in `data/parquet/`.

## Beschikbare SQL Views

| View | Rijen | Beschrijving |
|------|-------|-------------|
| vw_forensic_grants | 9 | CORDIS + ZonMw + NIH subsidies met coordinator en bedrag |
| vw_woo_citations | 3 | Bewijscitaten gekoppeld aan Woo-dossiernummers |
| vw_conflict_of_interest | 16 | Belangenmatrix: academisch, beleid, subsidie, media per Tier 1-3 |
| vw_virology_betweenness | 195 | Virologie-gefilterde betweenness centrality per node |
| vw_woo_redaction_deltas | 8 | Zwartlakkingsverschillen tussen Woo-vrijgaven 2021 vs 2024 |
| vw_silent_contributors | 4 | SCI-anomalieen (Robertson SCI=1.0, Farrar SCI=1.0) |

## DuckDB Voorbeelden

```sql
-- Top virology bridges
SELECT name, org, virology_betweenness
FROM vw_virology_betweenness
WHERE virology_betweenness > 0.1
ORDER BY virology_betweenness DESC;

-- Conflicterende belangen
SELECT name, tier, academic_role, policy_role, grant_review_role
FROM vw_conflict_of_interest
WHERE tier <= 2;

-- Alle EU-subsidies
SELECT project_name, grant_id, amount_euro
FROM grant_sources
WHERE funder LIKE '%EU%' OR funder LIKE '%ZonMw%'
ORDER BY amount_euro DESC;
```

## SHA-256 Verificatie
```bash
sha256sum -c data/checksums.sha256
```

## Parquet Exports
Bestanden in `data/parquet/`:
- `centrality_flat.parquet` — 33.584 rijen met centrality scores per node per laag
- `vw_forensic_grants.parquet` — 4 consortium grants
- `vw_conflict_of_interest.parquet` — 16 entries
- `vw_virology_betweenness.parquet` — 195 entries
- `vw_woo_citations.parquet` — 3 entries
