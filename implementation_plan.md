# Forensic Upgrade Phase 4 — Implementation Plan

Following user approval ("akkoord"), this implementation plan outlines the technical execution steps to upgrade the Dutch Virology Network Analysis repository into an unfiltered forensic intelligence workstation.

## Proposed Changes

### Component 1: CORDIS & ZonMw European Funding Ingestor
#### [NEW] [src/ingest_cordis.py](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/src/ingest_cordis.py)
- Fetch EU Horizon 2020 CORDIS funding metadata for VEO (€14.6M, GA#874735), COMPARE (€10.3M, GA#643476), ECRAID (€20.0M, GA#965313), DURABLE (€5.0M, GA#848223).
- Fetch ZonMw NCOH (€4.2M) and PDPC (€12.0M) grant allocations for Erasmus MC and UMC Utrecht.
- Write funding entries to `data/downloads/cordis_zonmw_funding.json`.

### Component 2: Multi-Layer Database Schema & Engine Upgrades
#### [MODIFY] [src/setup_multiplex_db.py](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/src/setup_multiplex_db.py)
- Create `informal_interactions` table to log draft reviews and uncredited advisory contributions.
- Create `narrative_drift` table to store chronological stance shifts (`PRIVATE_STANCE` vs `PUBLIC_STATEMENT`).
- Create `technical_capabilities` table mapping genetic techniques (e.g. `Furin Cleavage Site`, `BsmBI/BsaI Reverse Genetics`, `Ferret GOF Transmission`).
- Ingest `cordis_zonmw_funding.json` into SQLite as `FUNDING_FLOW` edges.

### Component 3: Forensic Anomaly & Drift Analytics
#### [MODIFY] [src/analyze_multiplex.py](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/src/analyze_multiplex.py)
- Calculate the **Silent Contributor Index (SCI)**:
  $$\text{SCI} = \frac{\text{Informal Draft Reviews}}{\text{Official Author Credit}}$$
- Calculate the **Narrative Drift Score** per key researcher (Jan 31 - March 2020).
- Save anomaly scores to `data/centrality_results.json`.

### Component 4: Forensic Views & Parquet Export
#### [MODIFY] [src/setup_sql_views.py](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/src/setup_sql_views.py)
- Create `vw_silent_contributors` view.
- Create `vw_narrative_drift` view.
- Create `vw_technical_capabilities` view.

#### [MODIFY] [src/export_forensic_data.py](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/src/export_forensic_data.py)
- Export new views to CSV, Parquet, and compute SHA-256 checksums in `data/checksums.sha256`.

### Component 5: Web Application & Dossier Export
#### [MODIFY] [build_web_app.py](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/build_web_app.py)
- Export `silent_contributors`, `narrative_drift`, and `technical_capabilities` to `docs/data.json`.

#### [MODIFY] [src/export_multiplex.py](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/src/export_multiplex.py)
- Add Section 3.4 (Silent Contributor Index), Section 3.5 (Narrative Drift Matrix), and Section 6.3 (EU CORDIS & ZonMw Funding Flow) to `docs/DUTCH_CONNECTIONS_DOSSIER.md`.

---

## Verification Plan

### Automated Tests & Pipeline Execution
- Execute full pipeline: `ingest_cordis.py` -> `setup_multiplex_db.py` -> `analyze_multiplex.py` -> `setup_sql_views.py` -> `export_forensic_data.py` -> `build_web_app.py` -> `export_multiplex.py`.
- Verify SQLite table counts and view queries.
- Verify SHA-256 checksum generation for exported datasets.
- Execute git commit and push to main.
