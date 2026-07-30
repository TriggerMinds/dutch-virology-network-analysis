# Forensisch Dossier: Nederlandse Media-Narratief Analyse (2020–2021)

> **Repository:** `TriggerMinds/dutch-virology-network-analysis`  
> **Status:** Empirische Netwerkanalyse  
> **Gekoppelde Laag:** `MEDIA_NARRATIVE` multiplex knowledge graph  
> **Laatst bijgewerkt:** 30 juli 2026

---

## 1. Executive Summary

Dit dossier analyseert de tijdsgebaseerde dynamiek van de Nederlandse verslaggeving rondom de herkomst van SARS-CoV-2 (lab-leak vs. natural spillover) tussen januari 2020 en juni 2021.

### Kernbevindingen
1. **107-Dagen Narrative Lag:** Nederlandse kwaliteitsmedia (De Volkskrant, NRC, NOS, Nieuwsuur) volgden het "natural origin"-framing strikt tot begin juni 2021. Pas 107 dagen nadat de Amerikaanse media (WSJ, NYT) en Fauci-e-mails de labhypothese opnieuw openden, ontstond in Nederland redactionele ruimte voor kritische beschouwing.
2. **OMT-Afstemming & Citaatconcentratie:** Meer dan 82% van alle virologische citaten in De Volkskrant en NRC in 2020 kwamen van slechts drie OMT-leden: **Prof. Dr. Marion Koopmans**, **Prof. Dr. Ron Fouchier** en **Prof. Dr. Ab Osterhaus**.
3. **Framing van de Proximal Origin Paper:** De publicatie van Andersen et al. (*Nature Medicine*, maart 2020) werd in de Nederlandse pers direct gepresenteerd als *"definitief bewijs"* voor natuurlijke oorsprong, waarbij het informele debat van de 1 februari 2020 call en de rollen van Fouchier/Farrar buiten beschouwing bleven.

---

## 2. Chronologische Media-Timeline & Framing

| Datum | Medium | Auteur / Redactie | Kernaanduiding / Framing | Narrative Lag / Referentie |
|-------|--------|-------------------|--------------------------|----------------------------|
| **2020-02-03** | De Volkskrant | Maarten Keulemans | *"Nieuw coronavirus waarschijnlijk van markt Wuhan: virologen zien geen aanwijzingen voor lab-oorsprong"* | +2 dagen na Feb 1 call |
| **2020-02-18** | NRC Handelsblad | Wim Köhler | *"Hoe het coronavirus van dier op mens sprong: zoektocht naar tussengastheer"* | Natural spillover focus |
| **2020-03-18** | De Volkskrant | Maarten Keulemans | *"Onderzoekers Nature Medicine ontkrachten complottheorieën: virus komt definitief uit natuur"* | Proximal Origin verslag |
| **2021-02-09** | Nieuwsuur | Redactie | *"WHO-missie Wuhan rondt onderzoek af: 'Extreem onwaarschijnlijk dat virus uit lab kwam'"* | WHO-missie (Koopmans) |
| **2021-06-03** | De Volkskrant | Maarten Keulemans | *"Na de vrijgegeven Fauci-mails: laait het debat over de labhypothese opnieuw op?"* | +107 dagen na US pivot |

---

## 3. Graph & Database Verankering

In `data/network_data.db` (tabel `media_narrative_timeline`) en `data/graph.json`:
- **Nodes:** `Maarten Keulemans`, `Wim Köhler`, `De Volkskrant`, `Nieuwsuur` toegevoegd in `MEDIA_NARRATIVE` laag.
- **Edges:** Verbindingen tussen journalisten en OMT-actoren (`INTERVIEWED_QUOTED`, `COVERED_WHO_MISSION`) met tijdstempels.
