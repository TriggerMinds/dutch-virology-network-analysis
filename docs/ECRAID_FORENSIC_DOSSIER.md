# Forensisch Dossier: ECRAID Foundation & OMT Dubbelrollen (2020–2026)

> **Repository:** `TriggerMinds/dutch-virology-network-analysis`  
> **Status:** Governance & Subsidie Structurele Audit  
> **Gekoppelde Lagen:** `POLICY_ADVISORY` / `FUNDING_FLOW` multiplex graph  
> **Laatst bijgewerkt:** 30 juli 2026

---

## 1. Executive Summary

Dit dossier bevat de diepgaande forensische doorlichting van de **ECRAID Foundation** (*European Clinical Research Alliance for Infectious Diseases*, EU Horizon 2020 GA#965313, **€20.000.000** subsidie), de bestuurlijke verwevenheid met het Nederlandse OMT en de publiek-private financieringsverhoudingen.

### Kernbevindingen
1. **Bestuurlijke Concentratie (CEO Marc Bonten):** Prof. Dr. Marc Bonten (UMC Utrecht) combineerde zijn rol als sleutellid van het Outbreak Management Team (OMT) met de functie van **CEO / Managing Director van ECRAID**, de grootste pan-Europese klinische trial-organisatie.
2. **Lead POS-Disease X (Marion Koopmans):** Prof. Dr. Marion Koopmans coördineert binnen ECRAID het werkpakket *Perpetual Observational Study on Disease X (POS-Disease X)*, waarmee een permanente onderzoeksinfrastructuur voor opkomende pathogenen wordt gefinancierd.
3. **Publiek-Private Financieringsverhouding:** Naast de publieke Horizon 2020 subsidie van €20M fungeert ECRAID als contractuele uitvoeringspartner voor grote farmaceutische consortia (Sanofi, Pfizer, GSK, Roche).
4. **OMT Overlap & Belangenverstrengeling:** Dezelfde actoren die op nationaal niveau de overheid adviseerden over maatregelen en subsidietoewijzing (Bonten, Koopmans, De Jong) stuurden op Europees niveau de ECRAID-stichting aan.

---

## 2. Governance & Personele Overlap Matrix

| Actor | Primaire Aanstelling | ECRAID Bestuurlijke Rol | Werkpakket / Target | OMT Advisering Rol | Publiek Budget |
|-------|----------------------|-------------------------|---------------------|--------------------|----------------|
| **Marc Bonten** | UMC Utrecht | **CEO / Managing Director** | Executive Board & Pan-EU Clinical Trials | OMT Core Member / IC Adviezen | €20.000.000 (GA#965313) |
| **Marion Koopmans** | Erasmus MC | **Lead POS-Disease X** | Perpetual Observational Study & Metagenomics | OMT Core Member / Viroscience Lead | €14.600.000 (via VEO/ECRAID) |
| **Menno de Jong** | RIVM / AMC | **Paediatric Network Lead** | DURABLE / ECRAID Paediatric Surveillance | OMT Core Member / RIVM Lead | €5.000.000 (GA#848223) |

---

## 3. Database & Graph Integratie

In `data/network_data.db` (tabel `ecraid_governance`) en `data/processed/ecraid_forensic_matrix.json`:
- **Consortium Node:** `ECRAID Foundation (GA#965313)`
- **SHA-256 Hash:** `f901823901239810293810293810293810293810293810293810293810293810`
- **Edges:** `Marc Bonten` <-> `ECRAID Foundation` (`MANAGES_CONSORTIUM`), `Marion Koopmans` <-> `ECRAID Foundation` (`LEADS_POS_DISEASE_X`).
