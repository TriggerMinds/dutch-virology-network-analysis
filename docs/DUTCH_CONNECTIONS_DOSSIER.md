# DUTCH CONNECTIONS DOSSIER — Multiplex Knowledge Graph

**Datum:** 2026-07-30
**Bronnen:** Tony's Diary (Fauci, 1141pp), OpenAlex, NIH RePORTER
**Gelaagde netwerkanalyse:** CO_AUTHOR | POLICY_ADVISORY | MEDIA_NARRATIVE

---

## 1. SAMENVATTING

Dit dossier beschrijft de **multiplex Knowledge Graph** van het Nederlandse virologienetwerk in relatie tot de COVID-19 lab-origin discussie. De graaf bevat **4921 nodes** en **7907 edges** verdeeld over drie lagen.

### Laagoverzicht

| Laag | Nodes | Edges | Beschrijving |
|------|-------|-------|-------------|
| CO_AUTHOR | 4906 | 7882 | Wetenschappelijke publicaties en co-auteurschappen |
| POLICY_ADVISORY | 13 | 19 | Beleidsadvisering: Feb 1 call, OMT, WHO |
| MEDIA_NARRATIVE | 3 | 2 | Mediaverslaggeving: journalisten, publicaties |

### Tier-indeling

| Tier | Type | Aantal | Personen |
|------|------|--------|---------|
| 1 | Directe kern (virologen) | 8 | Ab Osterhaus, Bart Haagmans, Diederik Gommers, Jaap van Dissel, Jan Kluytmans, Marion Koopmans, Ron Fouchier, Thijs Kuiken |
| 2 | Institutionele bruggen | 7 | Annemiek van der Eijk, Arfan Ikram, Aura Timen, Ernst Kuipers, Marc Bonten, Massimo Palmarini, Menno de Jong |
| 3 | Media & narrative | 1 | Maarten Keulemans |

### Consortia in de graaf
- **DURABLE**
- **ECRAID**
- **ESWI**
- **NCOH**
- **PDPC**
- **VEO**
- **ZonMw**

---

## 2. CENTRALITEITSANALYSE

### 2.1 Betweenness Centrality (ALLE lagen) — "Verborgen bruggen"

1. **Arfan Ikram** (Tier 2, Erasmus MC) — betweenness = 0.4344
2. **Menno de Jong** (Tier 2, RIVM / AMC) — betweenness = 0.3994
3. **Massimo Palmarini** (Tier 2, MRC-University of Glasgow) — betweenness = 0.3139
4. **Annemiek van der Eijk** (Tier 2, Erasmus MC) — betweenness = 0.1667
5. **Diederik Gommers** (Tier 1, Erasmus MC) — betweenness = 0.1462
6. **Marc Bonten** (Tier 2, UMC Utrecht) — betweenness = 0.1314
7. **Bart Haagmans** (Tier 1, Erasmus MC) — betweenness = 0.1054
8. **Efthimios Dardiotis** (Tier 0, ) — betweenness = 0.1043
9. **Jan Kluytmans** (Tier 1, UMC Utrecht / Amphia) — betweenness = 0.1030
10. **Jaap van Dissel** (Tier 1, LUMC / RIVM) — betweenness = 0.0837

**Interpretatie:** Hoge betweenness = entiteit die als brug fungeert tussen anders gescheiden delen van het netwerk.

### 2.2 Betweenness Centrality — CO_AUTHOR laag

1. **Arfan Ikram** (Tier 2, Erasmus MC) — betweenness = 0.4596
2. **Menno de Jong** (Tier 2, RIVM / AMC) — betweenness = 0.3858
3. **Massimo Palmarini** (Tier 2, MRC-University of Glasgow) — betweenness = 0.2905
4. **Annemiek van der Eijk** (Tier 2, Erasmus MC) — betweenness = 0.1817
5. **Marc Bonten** (Tier 2, UMC Utrecht) — betweenness = 0.1588
6. **Jan Kluytmans** (Tier 1, UMC Utrecht / Amphia) — betweenness = 0.1115
7. **Efthimios Dardiotis** (Tier 0, ) — betweenness = 0.1108
8. **Diederik Gommers** (Tier 1, Erasmus MC) — betweenness = 0.1062
9. **Marion Koopmans** (Tier 1, Erasmus MC) — betweenness = 0.0759
10. **Bart Haagmans** (Tier 1, Erasmus MC) — betweenness = 0.0708

### 2.3 Betweenness Centrality — POLICY_ADVISORY laag

| Entiteit | Betweenness | Rol |
|----------|------------|-----|
| **Feb 1 Conference Call** | 0.6970 | Feb 1 call participant / policy position |
| **Deliberate Insertion Hypothesis** | 0.1591 | Feb 1 call participant / policy position |
| **Ron Fouchier** | 0.0758 | Feb 1 call participant / policy position |
| **Christian Drosten** | 0.0758 | Feb 1 call participant / policy position |
| **Anthony Fauci** | 0.0108 | Feb 1 call participant / policy position |
| **Francis Collins** | 0.0108 | Feb 1 call participant / policy position |
| **Jeremy Farrar** | 0.0108 | Feb 1 call participant / policy position |
| **Kristian Andersen** | 0.0108 | Feb 1 call participant / policy position |

**Conclusie:** De Feb 1 Conference Call is veruit de belangrijkste brug in de policy-laag. Fouchier en Drosten zijn belangrijke individuele bruggen — beide als vertegenwoordigers van de Natural Origin-positie.

---

## 3. COMMUNITY DETECTIE (LOUVAIN)

### 3.1 Co-auteur community met Erasmus MC-kern

Het **Leiden/Louvain-algoritme** detecteert een aparte community (Community 0) bestaande uit:
- **Core Tiers:** Ab Osterhaus, Bart Haagmans, Marion Koopmans, Ron Fouchier, Thijs Kuiken
- **Grootte:** 715 nodes (in CO_AUTHOR laag)

**Dit is de Erasmus MC / Nederlandse virologie-community.** Al deze personen publiceren regelmatig samen en delen een co-auteurs netwerk van ~715 onderzoekers.

### 3.2 Andere communities

| Community | Grootte | Kernleden |
|-----------|---------|-----------|
| Community 9 | 1265 | Arfan Ikram |
| Community 5 | 1107 | Jeremy Farrar, Marc Bonten, Menno de Jong |
| Community 4 | 733 | Massimo Palmarini |
| Community 3 | 369 | Annemiek van der Eijk, Aura Timen |
| Community 7 | 298 | Jan Kluytmans |

### 3.3 Policy-community splitsing

In de POLICY_ADVISORY laag detecteert Louvain de volgende communities:
2. **Community 1** (10 leden): Andrew Rambaut, Anthony Fauci, Deliberate Insertion Hypothesis, Edward Holmes, Feb 1 Conference Call, Francis Collins, Jeremy Farrar, Kristian Andersen, Marion Koopmans, Robert Garry
1. **Community 0** (3 leden): Christian Drosten, Natural Origin Hypothesis, Ron Fouchier

**Koopmans zit in Community 1** (samen met de deliberate-fractie) — dit is een voorzichtige indicatie dat zij mogelijk nader stond tot de deliberate-positie dan Fouchier (die in Community 0 zit), maar dit is **geen bewijs**; alleen een netwerktoewijzing op basis van met wie ze in dezelfde policy-edges zit.

---

## 4. CHRONOLOGISCHE TIJDSLIJN

| Datum | Type | Gebeurtenis | Actoren |
|-------|------|------------|--------|
| 2020-01-31 | trigger | Jeremy Farrar calls Fauci about furin cleavage site — triggers Feb 1 call | Jeremy Farrar, Anthony Fauci |
| 2020-02-01 | meeting | Fauci convenes 12 scientists incl. Fouchier, Koopmans. NO CONSENSUS on natural vs deliberate | Fouchier, Koopmans, Fauci, Collins et al. |
| 2020-02-09 | consultation | Tom Frieden calls Fauci; discussed CFR estimates 0.2-0.3% vs 2% | Tom Frieden, Anthony Fauci |
| 2020-03-11 | declaration | WHO declares COVID-19 a pandemic | WHO, Fauci |
| 2020-05 | publication | Andersen et al. 'The Proximal Origin of SARS-CoV-2' published in Nature Medicine | Andersen, Garry, Holmes, Rambaut |
| 2021-06 | FOIA release | Washington Post publishes Fauci email archive — Koopmans/Fouchier emails public | Fauci, Koopmans, Fouchier |
| 2022-03 | analysis | Nature Medicine publishes final Proximal Origin paper with expanded analysis | Andersen, Holmes, Rambaut, Garry |

---

## 5. NEDERLANDSE VIROLOGEN IN FAUCI'S DAGBOEK

| Persoon | Tier | Vermeldingen in Diary | |
|---------|------|----------------------|---|
| **Ron Fouchier** | 1 | 2× (p14: deelnemer + positie) | "Original GOF person" — betoogde natuurlijke oorsprong |
| **Marion Koopmans** | 1 | 1× (p14: deelnemer) | **Positie NIET genoteerd** |
| **Ab Osterhaus** | 1 | **0** | Afwezig in 1141 pagina's |
| **Thijs Kuiken** | 1 | **0** | Afwezig |
| **Bart Haagmans** | 1 | **0** | Afwezig |
| **Jaap van Dissel** | 1 | **0** | Afwezig |
| **Diederik Gommers** | 1 | **0** | Afwezig |
| **Jan Kluytmans** | 1 | **0** | Afwezig |

---

## 6. FINANCIERING & CONSORTIA

### 6.1 NIH Grants
Uit 23 NIH RePORTER queries (voor alle Tier 1-2 namen + consortia) zijn **0 grants** met directe Nederlandse link gevonden. Alle matches zijn indirect (Nederlandse namen in abstract van Amerikaanse grants).

### 6.2 Consortium edges
De consortia (PDPC, NCOH, VEO, DURABLE, ECRAID, ESWI, ZonMw) zijn opgenomen als nodes maar **hebben 0 edges** in de huidige graaf. Dit komt doordat:
- De NIH RePORTER query vond geen grants die consortiumnamen in de titel/abstract droegen
- ZonMw-gegevens zijn niet openbaar via NIH RePORTER
- EU Horizon 2020 data (VEO, DURABLE, ECRAID) zijn niet via NIH toegankelijk

**Aanbevolen:** Handmatige ZonMw-query + EU CORDIS-import.

---

## 7. NARRATIEVE MEDIA-LAAG

De MEDIA_NARRATIVE laag is klein (3 nodes, 2 edges) maar toont:
- **Maarten Keulemans** (Volkskrant) verbindt Proximal Origin Paper ↔ Fauci via media-verslaggeving
- Keulemans is de enige Nederlandse wetenschapsjournalist in de dataset
- Geen edges naar Tier 1-2 virologen via media-laag (alleen via CO_AUTHOR)

---

## 8. NETWERKVISUALISATIE

De volledige multiplex graaf is geexporteerd naar `data/graph.json` (node-link format, compatible met Gephi, Cytoscape, networkx).

### Aanbevolen visualisatie-instellingen:
- **Layout:** Force Atlas 2 (Gephi) of Spring (NetworkX)
- **Node kleur:** Tier 1 (rood), Tier 2 (blauw), Tier 3 (groen), overig (grijs)
- **Edge kleur:** CO_AUTHOR (blauw), POLICY_ADVISORY (rood), MEDIA_NARRATIVE (groen)
- **Node grootte:** Betweenness centrality

---

## 9. BLINDE VLEKKEN

1. **Koopmans' positie blijft onbekend** — Staat in de policy-community van de deliberate-fractie op basis van 1× vermelding; dit is géén bewijs van haar standpunt
2. **Alle Tier 1-personen behalve Fouchier/Koopmans zijn afwezig** in Fauci's dagboek — hun rol in de origins-discussie moet uit andere bronnen komen (OMT-notulen, ZonMw, EU-projecten)
3. **Consortium edges = 0** — De graaf heeft de consortia als nodes maar geen financieringsedges. NIH-data + ZonMw + EU CORDIS moeten handmatig worden toegevoegd
4. **Media-laag onderontwikkeld** — Alleen Keulemans; mist NRC, Trouw, Nieuwsuur, Pointer-journalisten
5. **Tijdlijn eindigt in 2022** — De Diary loopt tot dec 2022 maar de origins-discussie ging door (Worobey 2022, Senate hearings 2023)

---


## 11. DUAL-PILLAR INTELLIGENCE: USRTK 2026 & REGULATORY TRIALS

### 11.1 Pijler 1: Origins Intelligence

**DIA March 2020 Memo:** Gedeclassificeerd via USRTK v. DIA FOIA. Concludeerde WIV had reverse genetics capability. Lab-leak kon niet worden uitgesloten.

**CIA Whistleblower James Erdman III:** Senaatsgetuigenis mei 2026. Stelde dat lab-leak conclusie onderdrukt werd.

**Ralph Baric / UNC FOIA:** Baric (UNC) deelde reverse genetics materialen met Shi Zhengli (WIV). DEFUSE performer.

### 11.2 Pijler 2: Regulatory & Trial Data

**PHMPT datasets (5 trials):** Pfizer/BioNTech NCT04368728, Moderna NCT04470427, J&J NCT04516746, pediatric C4591028. Myocarditis/TTS signals.

**Oversterfte:** Meester/Aukema/Jacobs/Bonte (45.000 excess deaths 2020-2023) vs CBS (24.200) vs RIVM (22.500 COVID coded). Discrepantie: 46.700.

**Dual-pillar UI tabs toegevoegd aan web-app:** P1 Origins / P2 Regulering.

---
## 12. OUTPUTBESTANDEN

| Bestand | Grootte | Beschrijving |
|---------|---------|-------------|
| `data/network_data.db` | SQLite | Multiplex database (nodes, edges, timeline) |
| `data/graph.json` | Node-link | Complete graaf voor Gephi/Cytoscape |
| `data/centrality_results.json` | JSON | Betweenness, eigenvector, degree per laag |
| `data/downloads/openalex_multiplex.json` | JSON | 16 auteurprofielen met co-auteurs |
| `data/downloads/nih_grants_multiplex.json` | JSON | 23 NIH queries |
| `docs/DUTCH_CONNECTIONS_DOSSIER.md` | MD | Dit dossier |

---

*Multiplex Knowledge Graph gegenereerd 2026-07-30. Geen conclusies over schuld of onschuld — alleen gestructureerde vastlegging van feiten uit het brondocument.*
