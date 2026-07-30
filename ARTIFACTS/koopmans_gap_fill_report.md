# Forensisch Eindrapport: Filling the Koopmans Feb 1 2020 Position Gap

> **Opdracht:** Systematische data-acquisitie, forensische extractie, WOO-drafting en graph-integratie voor de positie van Prof. Dr. Marion Koopmans op de teleconferentie van 1 februari 2020 over de furin cleavage site.  
> **Auteur:** Kilo OSINT Research Team (Google Antigravity Workstation)  
> **Datum:** 30 juli 2026  
> **Repository:** `TriggerMinds/dutch-virology-network-analysis`  
> **Compliance:** TEAMDYNAMICA-regels (Geen aannames; Default = `UNKNOWN`; Harde URL-verificatie HTTP 200 OK).

---

## 1. Executive Summary & Harde Conclusie

### Status van de Blind Spot: `UNKNOWN` (Unrecorded / Niet-gepubliceerd)

1. **Aanwezigheid op Teleconferentie (1 Feb 2020):** **BEVESTIGD.**  
   Op pagina 14 van het contemporaine dagboek van Anthony Fauci (*Tony's Diary*, Rand Paul Release juli 2026) wordt **M.P.G. Koopmans** (Head of Department of ViroScience, Erasmus Medical Center, NL) expliciet vermeld als deelnemer aan de internationale teleconferentie van 1 februari 2020 om 14:00 EST (20:00 CET).
2. **Inhoudelijke Bijdrage / Standpunt:** **NIET VASTGELEGD.**  
   Fauci beschrijft in de lopende tekst van het dagboek (pp. 14–15) wel expliciet het standpunt van **Prof. Dr. Ron Fouchier** (die stelde dat de furin cleavage site naturally kon zijn ontstaan en waarschuwde geen tijd te verspillen aan GOF/lab-origin hypotheses) en **Dr. Christian Drosten** ("was with Ron"), evenals "the rest" (Collins, Farrar, Andersen, Holmes, Rambaut, Garry, etc.). **Er is geen enkel citaat, specifieke argumentatie of stemgedrag van Marion Koopmans vastgelegd in dit primaire document.**
3. **Evaluatie van Secundaire Claims:**  
   De in sommige media geciteerde "9 februari 2020 e-mail van Koopmans" **bestaat niet** in deze primaire bron. Dit betreft een verwarring met latere FOIA-releases van de Washington Post.
4. **Formele Inrichting in Pipeline:**  
   De status `UNKNOWN` is verankerd in de SQLite database (`data/network_data.db` -> `koopmans_feb1_audit`), de multiplex knowledge graph (`data/graph.json` -> `BLIND_SPOT`), de chronologische dossiers en de WOO-verzoekteksten.

---

## 2. Bronnenlijst & Hash Manifest

| Document ID | Titel / Beschrijving | Relatief Pad | SHA-256 Hash | Status / Datum |
|-------------|----------------------|--------------|--------------|----------------|
| `fauci_diary_2026_07_24` | Tony's Diary Package (Fauci Diary Release, 1141 pp) | `data/raw/fauci_diary/2026.07.24_Tonys-Diary-Package.pdf` | `27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e` | Local / 2026-07-30 |
| `manifest_json` | Data Acquisition & Provenance Manifest | `data/raw/manifest.json` | `5c7390df732785d03ec5c4fa7c8651c6c0ca8e7cfaadceac9378c2e64ca62a8e` | Generated / 2026-07-30 |
| `koopmans_mentions_json` | Processed Keyword Extraction Dataset | `data/processed/koopmans_feb1_mentions.json` | `f312bd9a2e6fca783f9abf3a5e1eb3288b5774a382e737cbeec15632a764d262` | Generated / 2026-07-30 |
| `koopmans_mentions_csv` | Processed Keyword Extraction CSV | `data/processed/koopmans_feb1_mentions.csv` | `0ea9010df0fa71a25dbdbedb879ec3dfb768e1fa990ee48b94dfbfa3ca5ddc86` | Generated / 2026-07-30 |

---

## 3. Extractietabel Mentions & Deelnemers (Fauci Diary)

Onderstaande tabel vat alle treffers van de teleconferentie van 1 februari 2020 samen uit `data/processed/koopmans_feb1_mentions.json`:

| Bron & Pagina | Deelnemer / Entiteit | Exact Citaat / Passage | Positie Gewezen | Redaction Status |
|---------------|----------------------|------------------------|-----------------|------------------|
| `fauci_diary` p. 14 | **M.P.G. Koopmans** (Erasmus MC) | `• M.P.G. Koopmans, Head of Department of ViroScience, Erasmus Medical Center, NL.` | `unknown` | None |
| `fauci_diary` p. 14 | **Ron Fouchier** (Erasmus MC) | `Ron Fouchier said he was sure that this could occur naturally and we should not waste our time and divert effort to pursue this. This is expected of him since he was the original GOF person...` | `indicated` (Natural) | None |
| `fauci_diary` p. 14 | **Christian Drosten** (Charité) | `Also, Christian Drosten was with Ron;` | `indicated` (Natural) | None |
| `fauci_diary` p. 14 | **The Rest** (Andersen, Holmes, Garry, etc.) | `the rest felt that deliberate insertion was possible and given the fact that Dr. Zheng-Li Shi at the University of Wuhan has been working for years in GOF in coronaviruses...` | `indicated` (Deliberate Possible) | None |
| `fauci_diary` p. 864 | Marion Koopmans (Media ref) | Transcriptie / persreferentie d.d. 30 augustus 2021 | `unknown` | None |

---

## 4. Klaarliggende WOO-verzoeken (Ready-to-Submit)

Om de `UNKNOWN` status om te zetten in contemporaine bewijslast zijn concrete WOO-verzoeken (Wet open overheid) opgesteld in `docs/WOO_REQUESTS_FEB2020.md`:

1. **Erasmus MC (Viroscience / PDPC):**  
   *Doel:* E-mails, agenda's, gespreksverslagen en WhatsApp/Teams-berichten van Marion Koopmans en Ron Fouchier over de 1 februari 2020 call en furin cleavage site (periode 28 jan – 15 feb 2020).
2. **RIVM:**  
   *Doel:* OMT-afstemming en interne RIVM-memo's over de genomische kenmerken van SARS-CoV-2 en de overlegstructuur met Farrar/Fauci.
3. **Ministerie van VWS:**  
   *Doel:* Ambtelijke en bewindslieden-terugkoppeling van Nederlandse virologen na de 1 februari 2020 teleconferentie.

---

## 5. Database & Graph Integratie

### 5.1 SQLite Schema (`data/network_data.db`)
Een dedicated tabel `koopmans_feb1_audit` is aangemaakt en gevuld met 29 geëxtraheerde pagina's:
```sql
CREATE TABLE koopmans_feb1_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    page INTEGER,
    quote TEXT,
    speaker TEXT,
    position_indicated TEXT CHECK(position_indicated IN ('true','false','unknown')),
    redaction_flag TEXT,
    sha256_source TEXT,
    extracted_at TEXT,
    notes TEXT
);
```

Tevens is de tabel `informal_interactions` bijgewerkt met het expliciete auditrecord:
- `entity_name`: `Marion Koopmans`
- `paper_title`: `Feb 1 2020 Teleconference (Farrar/Fauci Call)`
- `interaction_type`: `UNRECORDED_PARTICIPATION (BLIND_SPOT)`
- `date`: `2020-02-01`
- `source_doc`: `data/raw/fauci_diary/2026.07.24_Tonys-Diary-Package.pdf`
- `page_num`: `14`

### 5.2 Knowledge Graph (`data/graph.json`)
- **Node `Marion Koopmans`:**  
  `feb1_2020_position_status`: `"UNKNOWN"`, `feb1_2020_attendance`: `"CONFIRMED_FAUCI_DIARY_P14"`, `blind_spot_flag`: `true`.
- **Edge `Feb 1 2020 Teleconference`:**  
  `relation`: `"PARTICIPATED_IN"`, `label`: `"Feb 1 Teleconference (Stance: UNKNOWN)"`, `status`: `"BLIND_SPOT"`.

---

## 6. Reproduceerbare Commando's & Scripts

Het volledige onderzoek is reproduceerbaar via de volgende commando's vanuit de repository root:

```bash
# 1. Acquisitie, verplaatsing en hashing van raw data
python src/acquire_and_hash_raw_data.py

# 2. Geautomatiseerde extractie & redaction audit uit PDF's
python src/extract_koopmans_feb1.py

# 3. Integratie in SQLite netwerkdatabase & JSON knowledge graph
python src/integrate_koopmans_gap.py
```

---

## 7. Geverifieerde Referentie-URL's (HTTP 200 OK Check)

In overeenstemming met het **URL Verificatie Protocol** zijn alle onderstaande links technisch gecontroleerd op een actieve HTTP 200 OK status:
- [Erasmus MC Researcher Profile - Prof. Dr. Marion Koopmans](https://www.erasmusmc.nl/en/research/researchers/koopmans-marion) (HTTP 200 OK)
- [Andersen et al., The Proximal Origin of SARS-CoV-2 (Nature Medicine DOI)](https://doi.org/10.1038/s41591-020-0820-9) (HTTP 200 OK)
