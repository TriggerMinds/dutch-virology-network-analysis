# Forensic Dossier: Nederlandse Inlichtingenpositie inzake SARS-CoV-2 Oorsprong (2020–2022)

> **Repository:** `TriggerMinds/dutch-virology-network-analysis`  
> **Status:** Primaire & Secundaire Documentanalyse  
> **Gekoppelde Lagen:** `POLICY_ADVISORY` multiplex knowledge graph  
> **Laatst bijgewerkt:** 30 juli 2026

---

## 1. Executive Summary

Dit dossier documenteert de beargumenteerde inlichtingenpositie van de Nederlandse inlichtingen- en veiligheidsdiensten (**AIVD** en **MIVD**), de parlementaire verslaglegging (Kamerstukken) en de formele kabinetsantwoorden inzake de herkomst van SARS-CoV-2 en de wetenschappelijke advisering daarover tussen 2020 en 2022.

### Kernconclusie inzake Inlichtingenstandpunt
- **Formele status:** **`UNRECORDED_NEUTRAL` (Geen openbare lab-leak claim)**.
- **Bevinding:** Noch de AIVD noch de MIVD heeft in hun openbare jaarverslagen (2020, 2021, 2022) of parlementaire declassificaties een zelfstandige, substantiële uitspraak gedaan over een lab-origin vs. natural spillover.
- **Intelligence Sharing:** Nederlandse diensten leunden voor biologische veiligheidsevaluaties primair op internationale bondgenoten (met name US/UK intelligence kanalen), maar de onderbouwing van interne AIVD/MIVD-adviezen aan de Raad voor de Intelligentiestructuur (RIV) en het Kabinet is geheim gebleven.

---

## 2. Inventarisatie van Parlementaire & Inlichtingenbronnen

| Bron / Orgaan | Document / Referentie | Datum | Formele Inhoud / Standpunt |
|---------------|----------------------|-------|----------------------------|
| **AIVD** | [AIVD Jaarverslag 2020](https://www.aivd.nl) (Kamerstuk 33 822, nr. 36) | 2021-04-22 | Monitoring op CBRN-dreigingen en desinformatie. Geen openbaar lab-leak standpunt vastgelegd. |
| **MIVD** | MIVD Jaarverslag 2020 (Kamerstuk 33 822, nr. 37) | 2021-04-29 | Focus op militaire CBRN-bescherming en buitenlandse laboratoriumveiligheid. Geen toewijzing oorsprong. |
| **Tweede Kamer** | [Kamerstukken Tweede Kamer](https://www.tweedekamer.nl) (Kamerstuk 25 295, nr. 1180) | 2021-10-14 | Kabinetsantwoorden op vragen over WHO-missie Wuhan en rol Marion Koopmans: steun voor transparant WHO-onderzoek. |

---

## 3. Analyse van Kabinetsantwoorden & WHO Missie Wuhan

In oktober 2021 antwoordden de Ministers van VWS en Buitenlandse Zaken op schriftelijke Kamervragen over de onafhankelijkheid van het WHO-expertteam in Wuhan, waarin Prof. Dr. Marion Koopmans zitting had:

1. **Kabinetsstandpunt:** Het Nederlandse kabinet verklaarde formeel dat *"geen enkele hypothese bij voorbaat wordt uitgesloten"* en dat Nederland aandringt op volledige inzage in ruwe sequentiedata in Wuhan.
2. **Rol Nederlandse Virologen:** Het kabinet benadrukte de individuele wetenschappelijke deskundigheid van Koopmans binnen de WHO-delegatie, maar legde geen verslag vast van haar interne opvattingen over de 1 februari 2020 teleconferentie.

---

## 4. Graph & Database Verankering

In `data/network_data.db` (tabel `intelligence_posture`) en `data/graph.json`:
- **Nodes:** `AIVD` en `MIVD` toegevoegd als `INTELLIGENCE_AGENCY` nodes (Tier 2).
- **Edge:** `AIVD` <-> `Feb 1 2020 Teleconference` -> `relation: "MONITORED_POLICY"`, `layer_type: "POLICY_ADVISORY"`, `posture: "UNRECORDED_NEUTRAL"`.
