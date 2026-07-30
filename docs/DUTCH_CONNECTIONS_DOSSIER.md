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

### 3.3 Policy-community splitsing & Koopmans Audit

In de POLICY_ADVISORY laag detecteert Louvain de volgende communities:
1. **Community 1** (10 leden): Andrew Rambaut, Anthony Fauci, Deliberate Insertion Hypothesis, Edward Holmes, Feb 1 Conference Call, Francis Collins, Jeremy Farrar, Kristian Andersen, Marion Koopmans, Robert Garry
2. **Community 0** (3 leden): Christian Drosten, Natural Origin Hypothesis, Ron Fouchier

> **Forensische Audit Update (juli 2026):** De plaatsing van Koopmans in Community 1 is puur een netwerk-topologische toewijzing door deling van de Feb 1 call-node. Uit de directe textuele extractie van *Tony's Diary* (p. 14-15) blijkt dat haar individuele standpunt of bijdrage op de teleconferentie van 1 februari 2020 **niet is vastgelegd** in het contemporaine verslag. Haar formele status is derhalve geclassificeerd als **`UNKNOWN` (Blind Spot)**.

---

## 4. CHRONOLOGISCHE TIJDSLIJN

| Datum | Type | Gebeurtenis | Actoren |
|-------|------|------------|--------|
| 2020-01-31 | trigger | Jeremy Farrar calls Fauci about furin cleavage site — triggers Feb 1 call | Jeremy Farrar, Anthony Fauci |
| 2020-02-01 | meeting | Fauci convenes 12 scientists incl. Fouchier, Koopmans. NO CONSENSUS. Fouchier/Drosten defend natural origin. Koopmans position UNRECORDED (UNKNOWN). | Fouchier, Koopmans, Fauci, Collins et al. |
| 2020-02-09 | consultation | Tom Frieden calls Fauci; discussed CFR estimates 0.2-0.3% vs 2% | Tom Frieden, Anthony Fauci |
| 2020-03-11 | declaration | WHO declares COVID-19 a pandemic | WHO, Fauci |
| 2020-05 | publication | Andersen et al. 'The Proximal Origin of SARS-CoV-2' published in Nature Medicine | Andersen, Garry, Holmes, Rambaut |
| 2021-06 | FOIA release | Washington Post publishes Fauci email archive — Koopmans/Fouchier emails public | Fauci, Koopmans, Fouchier |
| 2022-03 | analysis | Nature Medicine publishes final Proximal Origin paper with expanded analysis | Andersen, Holmes, Rambaut, Garry |

---

## 5. NEDERLANDSE VIROLOGEN IN FAUCI'S DAGBOEK

| Persoon | Tier | Vermeldingen in Diary | Details / Standpunt Status |
|---------|------|----------------------|---------------------------|
| **Ron Fouchier** | 1 | 2× (p14: deelnemer + positie) | "Original GOF person" — betoogde natuurlijke oorsprong |
| **Marion Koopmans** | 1 | 1× (p14: deelnemer) | **Aanwezigheid bevestigd; Standpunt UNRECORDED (`UNKNOWN`)** |
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

## 16. ONDERZOEKSTEAM-DYNAMICA & MATRIX VAN EXPERTISE VS. ONDERZOEKSOBJECT

### 16.1 Fauci Diary Mentions per Team Dynamica Lid

De volgende tabel toont welke van de 15 TEAMDYNAMICA-leden genoemd worden in Fauci's
contemporaine dagboek (1.141 pagina's) — de enige directe contemporaine bron over de
Feb 1 2020 teleconferentie en de daaraan voorafgaande gebeurtenissen.

| Teamlid | Diary mentions | Pagina('s) | Context |
|---------|---------------|------------|---------|
| **Steven Quay** | **2** | p792, p1012 | Geciteerd als GOF-expert en lab-origin voorstander; CEO Atossa Therapeutics |
| **Ralph Baric** | **1** | p786 | GOF-onderzoek met coronaviruses aan UNC Chapel Hill |
| Robert Malone | 0 | — | — |
| Kevin McKernan | 0 | — | — |
| Aseem Malhotra | 0 | — | — |
| Theo Schetters | 0 | — | — |
| Yuri Deigin | 0 | — | — |
| Sonia Elijah | 0 | — | — |
| Aaron Siri | 0 | — | — |
| Jan Hommel | 0 | — | — |
| Els van Veen | 0 | — | — |
| Wouter Aukema | 0 | — | — |
| Ronald Meester | 0 | — | — |
| Marc Jacobs | 0 | — | — |
| Maurice de Hond | 0 | — | — |

**Bevinding:** Van de 15 teamleden worden alleen Steven Quay en Ralph Baric genoemd.
Quay (2x) vanwege zijn GOF/lab-origin stellingname. Baric (1x) vanwege zijn
coronavirus reverse genetics publicaties. De overige 13 analisten — inclusief de
mRNA-contaminatie-, oversterfte- en EudraVigilance-experts — worden niet genoemd.

### 16.2 De Asymmetrie: Onderzoekers vs. Onderzoeksobjecten

Een cruciaal methodologisch inzicht is het onderscheid tussen twee groepen:

**Groep A — De Onderzoekers (TEAMDYNAMICA-leden):**
Document- en data-analisten, clinici, journalisten. Geen hands-on wet-lab
reverse genetics ervaring met BsmBI/BsaI of furin cleavage site constructie.
Het team constateert dit zelf: "Het team heeft nog steeds geen lid met
hands-on laboratoriumervaring in het daadwerkelijk uitvoeren van reverse
genetics of gain-of-function experimenten met coronavirussen."

**Groep B — De Onderzoeksobjecten (Knowledge Graph nodes):**
Wet-lab wetenschappers met bewezen BsmBI/BsaI reverse genetics patenten:

| Naam | Patent(en) | Techniek | Jaar |
|------|-----------|----------|------|
| **Ron Fouchier** | US6849435B2, US20140234358A1 | BsmBI/BsaI reverse genetics; H5N1 ferret GOF | 1999, 2012 |
| **Ab Osterhaus** | WO2006131370A2 | SARS-CoV reverse genetics | 2005 |
| **Yoshi Kawaoka** | WO2014170750A1, US6849435B2 | Mutant influenza; ferret transmission | 2013 |
| **Ralph Baric** | — (peer-reviewed) | Coronavirus reverse genetics; DEFUSE | 2018+ |

**Kernpunt:** De personen met de daadwerkelijke laboratoriumexpertise om te
beoordelen of de furin cleavage site synthetisch of natuurlijk is (Fouchier,
Osterhaus, Kawaoka, Baric) zijn objecten van onderzoek, geen leden van het
onderzoeksteam. Zij worden geanalyseerd via documenten en data — maar hun
eigen technische oordeel (Fouchier: natuurlijk, Baric: via NIH-samenwerking
met WIV) is niet als primaire bron in het team aanwezig.

### 16.3 De BsmBI/BsaI Octrooistamboom (US6849435B2)

De methodologische basis voor reverse genetics van zowel influenza- als
coronavirussen ligt in het patent US6849435B2 (Fouchier, Osterhaus, Kawaoka,
1999). Dit patent beschrijft het gebruik van type IIS restrictie-enzymen
(BsmBI, BsaI) voor het kloneren van virale genomen uit cDNA. De techniek
is later toegepast op SARS-CoV (WO2006131370A2, 2005) en vormt de
methodologische basis voor de discussie over de furin cleavage site in
SARS-CoV-2.

De stamboom:
```
US6849435B2 (Fouchier/Osterhaus/Kawaoka, 1999)
  └── BsmBI/BsaI reverse genetics systeem
       ├── Toegepast op influenza A (H5N1 ferret, 2012)
       ├── Toegepast op SARS-CoV (WO2006131370A2, 2005)
       ├── Toegepast op MERS-CoV (Fouchier, 2012)
       └── Relevant voor SARS-CoV-2 furin cleavage site
            └── Feb 1 2020 call: natuurlijk vs. synthetisch debat
```

De octrooihouders (Fouchier, Osterhaus, Kawaoka) hebben direct of indirect
commercieel belang (Viroscience B.V.) bij de instandhouding van de reverse
genetics infrastructuur. Dit is geen aantijging van kwade opzet, maar een
constatering van belangen die in een volledige forensische analyse moeten
worden meegewogen.

## 17. OUTPUTBESTANDEN

| Bestand | Grootte | Beschrijving |
|---------|---------|-------------|
| `data/network_data.db` | SQLite | Multiplex database (nodes, edges, timeline) |
| `data/graph.json` | Node-link | Complete graaf voor Gephi/Cytoscape |
| `data/centrality_results.json` | JSON | Betweenness, eigenvector, degree per laag |
| `data/downloads/openalex_multiplex.json` | JSON | 16 auteurprofielen met co-auteurs |
| `data/downloads/nih_grants_multiplex.json` | JSON | 23 NIH queries |
| `docs/DUTCH_CONNECTIONS_DOSSIER.md` | MD | Dit dossier |

---

## 18. GEÏNTEGREERDE FORENSISCHE DOSSIERS (JULI 2026 REINFORCEMENT)

- [WOO-Afwijzingen & Zwartlakking Analyse](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/WOO_REFUSAL_ANALYSIS.md) — Systematische audit van weigeringsgronden (Art. 5.2 beleidsopvattingen 68.5%, Art. 5.1 sub c bedrijfsgegevens 42.0%).
- [ECRAID Foundation & OMT Dubbelrollen](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/ECRAID_FORENSIC_DOSSIER.md) — Governance doorlichting Marc Bonten (CEO €20M GA#965313) & Marion Koopmans (POS-Disease X).
- [Nederlandse Inlichtingenpositie (AIVD/MIVD)](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/NL_INTELLIGENCE_ORIGINS.md) — Audit van AIVD/MIVD-jaarverslagen en Kamerstuk 25 295 nr 1180.
- [Nederlandse Media-Narratief Analyse](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/MEDIA_NARRATIVE_NL.md) — Coderingsanalyse van 25+ media-artikelen & 107-dagen Narrative Lag.

---

*Multiplex Knowledge Graph gegenereerd 2026-07-30. Geen conclusies over schuld of onschuld — alleen gestructureerde vastlegging van feiten uit het brondocument.*
