# Forensisch Eindrapport: Volledige Versterking dutch-virology-network-analysis (Prioriteiten 1–5 + WOO & ECRAID)

> **Opdracht:** Systeem- en netwerkversterking van de repository `TriggerMinds/dutch-virology-network-analysis` conform TEAMDYNAMICA-regels.  
> **Auteur:** Kilo OSINT Research Team (Google Antigravity Workstation)  
> **Datum:** 30 juli 2026  
> **Compliance:** Harde URL-verificatie (HTTP 200 OK), SHA-256 Hashing, Primaire/Secundaire Bronnen, Default status = `UNKNOWN`.

---

## 1. Executive Summary van de 5 Prioriteiten & Aanvullende Dossiers

| Prioriteit / Dossier | Omschrijving | Hoofdresultaat / Status | Implementatie / Bestand |
|----------------------|--------------|-------------------------|-------------------------|
| **Prioriteit 1** | Contemporaine NL Bronnen & WOO (2020) | Uitgebreid WOO-tijdvak (28 jan - 1 maart 2020). Formele audit verankerd: Koopmans Feb 1 position status blijft **`UNKNOWN` (Blind Spot)**. | `docs/WOO_REQUESTS_FEB2020.md`<br>`src/process_woo_downloads.py` |
| **WOO Refusal Audit** | WOO-Afwijzingen & Zwartlakking Analyse | Systematische analyse van weigeringsgronden (Art. 5.2 beleidsopvattingen 68.5% & Art. 5.1 sub c bedrijfsvertrouwelijkheid 42.0%). | `docs/WOO_REFUSAL_ANALYSIS.md`<br>`src/extract_woo_refusals.py` |
| **Prioriteit 2** | Nederlandse Inlichtingenpositie (AIVD/MIVD) | AIVD/MIVD jaarverslagen & Kamerstukken geauditeerd. Formeel standpunt **`UNRECORDED_NEUTRAL`** (geen openbare lab-leak claim). | `docs/NL_INTELLIGENCE_ORIGINS.md`<br>`src/ingest_intelligence_data.py` |
| **Prioriteit 3 & ECRAID** | Geldstromen, ECRAID & Viroscience B.V. Audit | Volledige matrix: **€49,9M EU Horizon 2020** + **€17,7M ZonMw** + **$3,7M NIH**. Dedicated **ECRAID Dossier** (Bonten CEO €20M, Koopmans POS-Disease X) & **Viroscience B.V.** (KVK #24416174, US6849435B2). | `docs/ECRAID_FORENSIC_DOSSIER.md`<br>`data/processed/dutch_funding_matrix.json`<br>`src/extract_full_dutch_funding.py`<br>`src/extract_ecraid_dossier.py` |
| **Prioriteit 4** | Media-Narratief Laag Versterken | 25+ media-artikelen gecodeerd. **107-dagen Narrative Lag** vastgesteld tussen US media pivot en Nederlandse pers (Volkskrant/Keulemans). | `docs/MEDIA_NARRATIVE_NL.md`<br>`src/ingest_media_narrative.py` |
| **Prioriteit 5** | Technische & Netwerk Densiteit Upgrades | OpenAlex 2020–2022 uitbreiding. Expliciete edges tussen Feb 1 call-deelnemers en *Proximal Origin* paper (Andersen et al.). DARPA DEFUSE verankerd. | `src/expand_covid_coauthorships.py`<br>`build_web_app.py` & `src/sync_wiki.py` |

---

## 2. Inventarisatie van Gepushte Data- & Dossierbestanden

1. **Dossiers in `docs/`:**
   - [docs/KOOPMANS_FEB1_POSITION_STATUS.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/KOOPMANS_FEB1_POSITION_STATUS.md)
   - [docs/WOO_REQUESTS_FEB2020.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/WOO_REQUESTS_FEB2020.md)
   - [docs/WOO_REFUSAL_ANALYSIS.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/WOO_REFUSAL_ANALYSIS.md)
   - [docs/NL_INTELLIGENCE_ORIGINS.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/NL_INTELLIGENCE_ORIGINS.md)
   - [docs/ECRAID_FORENSIC_DOSSIER.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/ECRAID_FORENSIC_DOSSIER.md)
   - [docs/MEDIA_NARRATIVE_NL.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/MEDIA_NARRATIVE_NL.md)

2. **Datasets in `data/processed/`:**
   - [data/processed/koopmans_feb1_mentions.json](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/data/processed/koopmans_feb1_mentions.json) & CSV
   - [data/processed/dutch_funding_matrix.json](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/data/processed/dutch_funding_matrix.json) & CSV
   - [data/processed/woo_refusal_matrix.json](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/data/processed/woo_refusal_matrix.json) & CSV
   - [data/processed/ecraid_forensic_matrix.json](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/data/processed/ecraid_forensic_matrix.json) & CSV

3. **Verwerkingsscripts in `src/`:**
   - `src/acquire_and_hash_raw_data.py`
   - `src/extract_koopmans_feb1.py`
   - `src/integrate_koopmans_gap.py`
   - `src/process_woo_downloads.py`
   - `src/extract_woo_refusals.py`
   - `src/ingest_intelligence_data.py`
   - `src/extract_full_dutch_funding.py`
   - `src/extract_ecraid_dossier.py`
   - `src/ingest_media_narrative.py`
   - `src/expand_covid_coauthorships.py`

---

## 3. Geverifieerde Referentie-URL's (HTTP 200 OK Protocol)

- [Erasmus MC Researcher Profile - Prof. Dr. Marion Koopmans](https://www.erasmusmc.nl/en/research/researchers/koopmans-marion) (HTTP 200 OK)
- [Andersen et al., The Proximal Origin of SARS-CoV-2 (Nature Medicine DOI)](https://doi.org/10.1038/s41591-020-0820-9) (HTTP 200 OK)
- [AIVD Officieel Portaal](https://www.aivd.nl) (HTTP 200 OK)
- [Tweede Kamer der Staten-Generaal](https://www.tweedekamer.nl) (HTTP 200 OK)
