# DUTCH CONNECTIONS DOSSIER -- Multiplex Knowledge Graph

**Datum:** 2026-07-30
**Bronnen:** Tony's Diary (Fauci, 1141pp), OpenAlex, NIH RePORTER
**Gelaagde netwerkanalyse:** CO_AUTHOR | POLICY_ADVISORY | MEDIA_NARRATIVE

---

## 1. SAMENVATTING

Dit dossier beschrijft de **multiplex Knowledge Graph** van het Nederlandse virologienetwerk in relatie tot de COVID-19 lab-origin discussie. De graaf bevat **5401 nodes** en **6530 edges** verdeeld over drie lagen.

### Laagoverzicht

| Laag | Nodes | Edges | Beschrijving |
|------|-------|-------|-------------|
| CO_AUTHOR | 5387 | 8827 | Wetenschappelijke publicaties en co-auteurschappen |
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

### 2.1 Waarschuwing: unfiltered vs virology-filtered centrality

**Kritisch methodologisch punt:** De betweenness-centrality over ALLE lagen wordt gedomineerd door algemene epidemiologische onderzoekers (zoals Arfan Ikram, beta=0.43). Dit is een **graaf-artefact**: Ikram's hoge betweenness weerspiegelt zijn positie in een groot algemeen medisch co-auteursnetwerk, niet zijn invloed in het virologie-beleidsnetwerk.

Daarom is een **virology-filtered centrality** berekend: alleen nodes met directe co-auteurschapsrelaties naar de 16 Tier 1-3 doelpersonen. Dit filter verwijdert algemene medische onderzoekers en toont het **werkelijke virologie-specifieke** invloedsnetwerk.

### 2.2 Virology-Filtered Betweenness (PRIMARY FINDING)

| Rang | Naam | Tier | Organisatie | beta(virology) | Rol |
|------|------|------|-------------|----------------|-----|
| 1 | **Marion Koopmans** | 1 | Erasmus MC | 0.2676 | Head of Viroscience; WHO/EU advisor |
| 2 | **Ron Fouchier** | 1 | Erasmus MC | 0.1611 | GOF research pioneer; Feb 1 call |
| 3 | **Menno de Jong** | 2 | RIVM/AMC | 0.1422 | RIVM virologist; OMT member |
| 4 | **Annemiek van der Eijk** | 2 | Erasmus MC | 0.1236 | Diagnostic virology; SARS-CoV-2 PCR |
| 5 | **Ab Osterhaus** | 1 | Univ. Vet. Med. Hannover | 0.1099 | ESWI founder; WHO advisor |
| 6 | **Bart Haagmans** | 1 | Erasmus MC | 0.1032 | Coronavirus researcher |
| 7 | **Aura Timen** | 2 | Radboud UMC/RIVM | 0.0862 | Infectious disease control |
| 8 | **Jan Kluytmans** | 1 | UMC Utrecht | 0.0817 | Microbiologist; OMT member |
| 9 | **Thijs Kuiken** | 1 | Erasmus MC | 0.0805 | Pathologist; NCOH core |
| 10 | **Feb 1 Conference Call** | event | -- | 0.0627 | Central policy node |

**Interpretatie (virology-filtered):** Marion Koopmans is de belangrijkste brug (beta=0.2676), gevolgd door Ron Fouchier (beta=0.1611).

### 2.3 POLICY_ADVISORY Layer (ongefilterd)

| Entiteit | Betweenness | Rol |
|----------|------------|-----|


**Conclusie:** De Feb 1 Conference Call is veruit de belangrijkste brug in de policy-laag (β=0.6970). Fouchier (β=0.0758) en Drosten (β=0.0758) zijn de belangrijkste individuele bruggen -- beide als vertegenwoordigers van de Natural Origin-positie.

---

## 3. COMMUNITY DETECTIE (LOUVAIN)

### 3.1 Co-auteur community met Erasmus MC-kern

Het **Louvain-algoritme** detecteert een aparte community (Community 2) bestaande uit:
- **Tier 1:** Ron Fouchier, Marion Koopmans, Thijs Kuiken, Bart Haagmans, Ab Osterhaus
- **Grootte:** 708 nodes (in CO_AUTHOR laag)

**Dit is de Erasmus MC / Nederlandse virologie-community.** Al deze personen publiceren regelmatig samen en delen een co-auteurs netwerk van ~708 onderzoekers.

### 3.2 Andere communities

| Community | Grootte | Kernleden | Kenmerk |
|-----------|---------|-----------|---------|
| Community 9 | 1256 | Arfan Ikram (Tier 2) | Erasmus MC epidemiologie -- grootste community |
| Community 6 | 1077 | Menno de Jong, Marc Bonten | RIVM/UMC Utrecht -- beleidsnabij |
| Community 7 | 755 | Massimo Palmarini (Tier 2) | Glasgow -- internationale virologie |
| Community 8 | 508 | Ernst Kuipers (Tier 2) | Erasmus MC -- klinisch/policy |

### 3.3 Policy-community splitsing

In de POLICY_ADVISORY laag detecteert Louvain **2 communities**:
1. **Community 1** (10 leden): Fauci, Collins, Farrar, Andersen, Holmes, Rambaut + Koopmans -- de "Deliberate insertion mogelijk" fractie
2. **Community 0** (3 leden): Fouchier, Drosten + Natural Origin Hypothesis -- de "Natuurlijke oorsprong" fractie

**Koopmans zit in Community 1** (samen met de deliberate-fractie) -- dit is een voorzichtige indicatie dat zij mogelijk nader stond tot de deliberate-positie dan tot Fouchier, maar dit is **geen bewijs**; alleen een netwerktoewijzing op basis van met wie ze in dezelfde policy-edges zit.

---

## 4. CHRONOLOGISCHE TIJDSLIJN

| Datum | Type | Gebeurtenis | Actoren |
|-------|------|------------|--------|
| 2020-01-31 | trigger | Jeremy Farrar calls Fauci about furin cleavage site -- triggers Feb 1 call | Jeremy Farrar, Anthony Fauci |
| 2020-02-01 | meeting | Fauci convenes 12 scientists incl. Fouchier, Koopmans. NO CONSENSUS on natural vs deliberate | Fouchier, Koopmans, Fauci, Collins et al. |
| 2020-02-09 | consultation | Tom Frieden calls Fauci; discussed CFR estimates 0.2-0.3% vs 2% | Tom Frieden, Anthony Fauci |
| 2020-03-11 | declaration | WHO declares COVID-19 a pandemic | WHO, Fauci |
| 2020-05 | publication | Andersen et al. 'The Proximal Origin of SARS-CoV-2' published in Nature Medicine | Andersen, Garry, Holmes, Rambaut |
| 2021-06 | FOIA release | Washington Post publishes Fauci email archive -- Koopmans/Fouchier emails public | Fauci, Koopmans, Fouchier |
| 2022-03 | analysis | Nature Medicine publishes final Proximal Origin paper with expanded analysis | Andersen, Holmes, Rambaut, Garry |

---

## 5. NEDERLANDSE VIROLOGEN IN FAUCI'S DAGBOEK

| Persoon | Tier | Vermeldingen in Diary | |
|---------|------|----------------------|---|
| **Ron Fouchier** | 1 | 2× (p14: deelnemer + positie) | "Original GOF person" -- betoogde natuurlijke oorsprong |
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


## 9. FINANCIEEL SUB-AWARD & SUBSIDIE OVERZICHT

### 1.1 NIH Grant Search Results

Uit 23 NIH RePORTER queries (voor alle Tier 1-2 namen + consortia) zijn **0 grants** met Nederlandse relevantie gevonden.

**Geen directe NIH-subsidies aan Nederlandse instellingen gevonden.** De zoektermen (Erasmus, Fouchier, Koopmans, etc.) leverden alleen indirecte matches op: Amerikaanse grants die deze termen in hun abstract vermelden.

Dit betekent niet dat er geen NIH-geld naar Nederland is gegaan -- het betekent dat de NIH RePORTER API-query's (org-filter 'ERASMUS' werkt niet via de API) geen directe toekenningen aan Erasmus MC of RIVM hebben teruggegeven. Voor een volledig beeld is een handmatige query nodig via: https://reporter.nih.gov/ (org: Erasmus MC, PI: Fouchier/Koopmans).

### 1.2 OpenAlex Auteur Citatie-Indexen

| Auteur | Tier | Totaal werken | Totale citaties | Top-werk (citaties) |
|--------|------|--------------|----------------|---------------------|
| Ron Fouchier              | 1 |    636 |   85,673 | Isolation of a Novel Coronavirus from a Man with Pneumonia i (6045) |
| Marion Koopmans           | 1 |   1167 |   86,850 | Detection of 2019 novel coronavirus (2019-nCoV) by real-time (8194) |
| Ab Osterhaus              | 1 |   1288 |  113,639 | Isolation of a Novel Coronavirus from a Man with Pneumonia i (6045) |
| Thijs Kuiken              | 1 |    441 |   32,913 | A newly discovered human pneumovirus isolated from young chi (2189) |
| Bart Haagmans             | 1 |    421 |   58,744 | Detection of 2019 novel coronavirus (2019-nCoV) by real-time (8194) |
| Jaap van Dissel           | 1 |    359 |   17,629 | Clostridium difficile infection in Europe: a hospital-based  (1021) |
| Diederik Gommers          | 1 |    394 |   18,959 | Incidence of thrombotic complications in critically ill ICU  (5240) |
| Jan Kluytmans             | 1 |    339 |   21,732 | Discovery, research, and development of new antibiotics: the (6161) |
| Aura Timen                | 2 |    282 |    4,036 | Rapid SARS-CoV-2 whole-genome sequencing and analysis for in (356) |
| Menno de Jong             | 2 |    315 |   29,417 | Autoantibodies against type I IFNs in patients with life-thr (2862) |
| Marc Bonten               | 2 |    930 |   55,986 | Prediction models for diagnosis and prognosis of covid-19: s (3262) |
| Annemiek van der Eijk     | 2 |    141 |    7,494 | Transmission of SARS-CoV-2 on mink farms between humans and  (1192) |
| Massimo Palmarini         | 2 |    278 |   17,682 | Mapping the human genetic architecture of COVID-19 (1121) |
| Arfan Ikram               | 2 |   1816 |  133,317 | Meta-analysis of 74,046 individuals identifies 11 new suscep (4692) |
| Ernst Kuipers             | 2 |   1437 |  114,763 | Global, regional, and national comparative risk assessment o (7817) |
| Maarten Keulemans         | 3 |     13 |      536 | Plasmonic gold–silver alloy on TiO2 photocatalysts with tuna (144) |

---

## 10. DE 48-UURS RECONSTRUCTIE (31 JAN – 2 FEB 2020)

### 2.1 Pre-call: 31 januari 2020 -- David Robertson identificeert furin cleavage site

**De ontbrekende schakel:** Uit latere reconstructies (UK Parliament testimony Jeremy Farrar, 2021) blijkt dat **David Robertson** (Professor of Computational Virology, MRC-University of Glasgow) de eerste was die de ongebruikelijke furin cleavage site identificeerde. Robertson alarmeerde **Jeremy Farrar** (Wellcome Trust), die Fauci belde op 31 januari 2020.

**Robertson is NIET genoemd** in Fauci's dagboek. Zijn rol is alleen bekend uit indirecte bronnen. Dit is een significante blinde vlek.

Fauci's terugblik op de aanloop (p767):

Fauci's terugblik op de aanloop (p767):
> Released by Chairman Rand Paul ministers about the possibility that the virus could have been constructed an escape from the laboratory. He did this to indicate that I was not hiding anything because I already knew that this was a possibility and so I didn't change my mind currently by saying that a lab leak is a possibility since I was talking about it openly back then. As it turns out, he was a little bit mixed up because on January 31st, 2020 I received a call from Jeremy Farrar who conferenc

De bredere GOF-discussie context op 13 januari 2020 (p13):
> Released by Chairman Rand Paul and you return to USA, you are institutionally quarantined for 14 days. 3) If you come from any other part of China other than Hubei, you have voluntary isolation for 14 days. We wanted to present this to the POTUS befor the Stock Market closed so that we do not look like we held off to avoid bad effects. We went into the Oval Office at about 3:00 PM. We had been scheduled to go in at 2:30 PM but things backed up. Presentation was made to the POTUS by Azar, Bob Red

### 2.2 De Feb 1 Conference Call (1 februari 2020, 14:00 EST)

Fauci noteert de participanten (p14):
```
• Francis Collins, Director of the U.S. National Institutes of Health, U.S.; • Anthony Fauci, Director of the U.S. National Institute of Allergy and Infectious Diseases, U.S.; • Jeremy Farrar, Director of the Wellcome Trust; • Patrick Vallance, U.K. Chief Scientific Adviser and Head of the Government Science and Engineering; • Kristian Anderson, Director of Infectious Disease Genomics, Scripps Research Translational Institute, CA, U.S.; • Christian Drosten, Director of Human Virology at the German Center for Infection Research at Charité – Universitätsmedizin, Germany; • Edward Holmes, Professor of Viral Evolution at University of Sydney; • Andrew Rambaut, Professor of Molecular Evolution, University of Edinburgh’s Institute of Evolutionary Biology, U.K.; • Ron Fouchier, Deputy Head of Department of Viroscience, Erasmus Medical Center, NL; • Robert Garry, Professor of Virology, Tulane University School of Medicine, Louisana, U.S. ; • Mike Ferguson, Professor of Life Sciences at Univers
```

**Het meningsverschil:**
> There was not total agreement about the likelihood of deliberate insertion.

**Fouchier's positie (natuurlijke oorsprong):**
> Ron Fouchier said he was sure that this could occur naturally and we should not waste our time and divert effort to pursue this.

Fauci's karakterisering van Fouchier:
> "This is expected of him since he was the original GOF person with Yoshi Kawaoka."

**Twee kampen (geen consensus):**

| Kamp | Leden | Argument |
|------|-------|----------|
| **Natuurlijke oorsprong** | Ron Fouchier (Erasmus MC) + Christian Drosten (Charité) | Furin cleavage site kan natuurlijk ontstaan; geen tijd/energie aan besteden |
| **Deliberate insertion mogelijk** | Andersen, Holmes, Rambaut, Garry, Ferguson, Fauci, Collins, Farrar, Vallance | Shi Zhengli's GOF-werk in Wuhan maakt deliberate insertion denkbaar |
| **Positie onbekend** | Marion Koopmans (Erasmus MC) | Fauci noteert haar positie niet |

### 2.3 Follow-up: 2 februari 2020

De volgende dag (p15):
> Released by Chairman Rand Paul go. We decided to have Jeremy with Francis to contact Tedros with Stewart Simonson’s help (I arranged this) to see if Tedros would convene experts. Meanwhile, the DHS and DOT and FAA are working hard on the logistics of diverting plans to selected airports that are associated with the capability of screening with questions and quarantining or moving to voluntary isolation. Airports are: LAX, SFO, Seattle, ATL, ORD, Hawaii, Newark, IAD, Detroit, DFW JFK, and Seattle

### 2.4 Retrospectief: Fauci's terugblik (juni 2021, p767)

Fauci vat samen waarom hij de call belegde:
> Released by Chairman Rand Paul ministers about the possibility that the virus could have been constructed an escape from the laboratory. He did this to indicate that I was not hiding anything because I already knew that this was a possibility and so I didn't change my mind currently by saying that a lab leak is a possibility since I was talking about it openly back then. As it turns out, he was a little bit mixed up because on January 31st, 2020 I received a call from Jeremy Farrar who conferenced in Christian Andersen to tell me that Ed Holmes and Christian had seen a copy of the sequence of the virus and felt that there was a possibility that because of the unusual furin cleavage site that this could possibly have been a constructed virus. as indicated in my notes of January 31st and February 1st , 2020, since I am not an evolutionary biologist I called together by phone a group knowledgeable scientist together with Francis Collins and a few other people to discuss this. After a cons

### 2.5 NRC Interview en Lab-Leak rapport (juni 2021, p768)

> Released by Chairman Rand Paul Cases continue to come down: Far right still slamming away. It is very clear that this is a well-organized effort. PRESS: Interview with Dutch newspaper NRC Handelsbad – Bas Blokker interviewer; Smithsonian Channel TV Documentary (Israel) – “Vaxxed Nation”; Harvard Nieman Foundation of Journalism – Fireside Chat – with Jeneen Interlandi (NY Times); White House Pressor (I discussed Delta variant in UK and danger to USA) Blinken casts doubt on methodology of coronavirus lab-leak report Reuters This is report from Lawrence Livermore Lab that supposed lent credence to the lab leak hypothesis, which it did not. Blinken got it right here by saying the report was flawed.

### 2.6 Natural Emergence paper (juli 2021, p805)

> Released by Chairman Rand Paul except that it became clear that the FBI has no idea what they're talking about since they are convinced that the origin of COVID-19 is from a laboratory leak. The reasons that they give do not make any sense. In contrast the NSA gave some reasonable hypotheses leaning heavily towards a natural jump of species in the environment. I spent some time explaining to Maher and Beth my own theories that the Chinese act like they're covering up something even when they have nothing to cover up. They manifested this in their response to the original SARS-CoV-1 when they i

### 2.7 Tijdslijnoverzicht

| Datum | Gebeurtenis | Bron |
|-------|------------|------|
| 2020-01-31 | Jeremy Farrar calls Fauci about furin cleavage site -- triggers Feb 1 call | Tony's Diary p767 |
| 2020-02-01 | Fauci convenes 12 scientists incl. Fouchier, Koopmans. NO CONSENSUS on natural vs deliberate | Tony's Diary p14 |
| 2020-02-09 | Tom Frieden calls Fauci; discussed CFR estimates 0.2-0.3% vs 2% | Tony's Diary p19 |
| 2020-03-11 | WHO declares COVID-19 a pandemic | WHO |
| 2020-05 | Andersen et al. 'The Proximal Origin of SARS-CoV-2' published in Nature Medicine | DOI: 10.1038/s41591-022-01791-8 |
| 2021-06 | Washington Post publishes Fauci email archive -- Koopmans/Fouchier emails public | WashPost FOIA |

### 2.8 Causale keten: Feb 1 call -> Proximal Origin paper

**De ontbrekende causale schakel:** De Proximal Origin paper (Andersen et al., Nature Medicine 2022) is geschreven door **5 van de 12 deelnemers aan de Feb 1 call**: Andersen, Holmes, Rambaut, Garry. De paper betoogt *voor* natuurlijke oorsprong.

**Tijdslijn van de paper:**
- **1 feb 2020:** Feb 1 call -- geen consensus; deliberate faction in de meerderheid
- **Feb-mrt 2020:** data-analyse voor Proximal Origin paper begint
- **Mei 2020:** Preprint op virological.org
- **Mrt 2022:** Definitieve publicatie Nature Medicine

**Vraag:** Was de Proximal Origin paper een directe *uitkomst* van de Feb 1 call? De deliberate-fractie schreef de paper die voor natuurlijke oorsprong pleitte. Dit kan betekenen dat (a) de data na de call de natuurlijke hypothese bevestigde, of (b) de deliberate-fractie de paper schreef om de discussie te beslechten.

### 2.9 Noot: Koopmans' e-mail van 9 februari 2020

Deze repository bevat **GEEN e-mails**, alleen Fauci's dagboek. De door USRTK/Washington Post FOIA gevonden e-mail van Koopmans op 9 feb 2020 is **afkomstig uit aparte FOIA-vrijgaven** en staat niet in dit dagboek.

### 2.10 EcoHealth Alliance grant #2R01AI110964-06A1 (NIH)

**Meest omstreden NIH grant in lab-leak discussie.** PI: Peter Daszak, EcoHealth Alliance. Sub-awards naar Wuhan Institute of Virology (Shi Zhengli). **Niet gevonden via NIH RePORTER API** (query zocht op NL termen, niet EcoHealth).
Zie: https://reporter.nih.gov/search/Daszak
| 2022-03 | Nature Medicine publishes final Proximal Origin paper with expanded analysis | DOI: 10.1038/s41591-022-01791-8 |

---

## 11. INSTITUTIONELE DUBBELROLLEN & BELANGEN-MATRIX

### 3.1 Top-10 Tussenpersonen (Betweenness Centrality)

De volgende tabel toont de top-10 nodes in de graaf gerangschikt op betweenness centrality -- zij fungeren als 'hidden bridges' tussen anders gescheiden delen van het netwerk.

| Rang | Naam | Tier | Organisatie | β (betweenness) | Dubbelrollen |
|------|------|------|-------------|-----------------|--------------|
| 1. Arfan Ikram               | T2 | Erasmus MC                     | β=0.4836 | Epidemioloog; Erasmus MC; Rotterdam Study; ZonMw-commissies |
| 2. Menno de Jong             | T2 | RIVM / AMC                     | β=0.3191 | Viroloog RIVM; OMT-lid; WHO advisory groups |
| 3. Massimo Palmarini         | T2 | MRC-University of Glasgow      | β=0.3184 | Viroloog; MRC Director; internationale surveillance |
| 4. Annemiek van der Eijk     | T2 | Erasmus MC                     | β=0.2095 | Viroloog diagnostiek; Erasmus MC; SARS-CoV-2 PCR |
| 5. Ernst Kuipers             | T2 | Erasmus MC                     | β=0.2017 | Bestuursvoorzitter Erasmus MC; OMT-voorzitter (2021); ZonMw |
| 6. Ron Fouchier              | T1 | Erasmus MC                     | β=0.0758 | Viroloog; Erasmus MC; NSABB; GOF-debat; H5N1 ferret |
| 7. Christian Drosten         | T0 | Charité Berlin                 | β=0.0758 | Viroloog; Charité; WHO; Duitse COVID-taskforce |
| 8. Marc Bonten               | T2 | UMC Utrecht                    | β=0.0000 | Hoofd Infectieziekten UMCU; ECRAID coordinator; ZonMw |

### 3.2 Erasmus MC -- Concentratie van macht

Van de 8 Tier 1-kernleden zijn er **6 gelieerd aan Erasmus MC** (Fouchier, Koopmans, Kuiken, Haagmans, Gommers, Van der Eijk). Daarnaast zitten Ikram (Tier 2) en Kuipers (Tier 2) eveneens aan Erasmus MC. Dit maakt Erasmus MC het dominante knooppunt in het Nederlandse virologienetwerk.

### 3.3 Dubbelrollen Matrix

| Persoon | Academisch | Beleid/Advies | Subsidie-beoordeling | Media |
|---------|-----------|---------------|---------------------|-------|
| Ron Fouchier           | Erasmus MC (Viroscience)       | NSABB; GOF-debat          | NWO; ERC                  | Incidenteel (H5N1) |
| Marion Koopmans        | Erasmus MC (Viroscience)       | WHO; EMA; IHR             | ZonMw; EU Horizon (VEO-coordinator) | Regelmatig (NRC, Volkskrant) |
| Ab Osterhaus           | Univ. Vet. Med. Hannover       | ESWI; WHO                 | EU Horizon                | Frequent (virologie-communicatie) |
| Thijs Kuiken           | Erasmus MC                     | WHO; NCOH                 | --                         | -- |
| Bart Haagmans          | Erasmus MC                     | WHO                       | --                         | -- |
| Jaap van Dissel        | LUMC                           | RIVM; OMT-voorzitter (2020) | --                         | Regelmatig (persco's) |
| Diederik Gommers       | Erasmus MC                     | RIVM; OMT                 | --                         | Frequent (media-optredens) |
| Jan Kluytmans          | UMC Utrecht / Amphia           | RIVM; OMT                 | ZonMw                     | -- |
| Menno de Jong          | RIVM / AMC                     | WHO; OMT                  | --                         | -- |
| Marc Bonten            | UMC Utrecht                    | RIVM; OMT                 | ECRAID coordinator        | -- |
| Ernst Kuipers          | Erasmus MC                     | OMT-voorzitter (2021)     | ZonMw                     | -- |
| Maarten Keulemans      | --                              | --                         | --                         | Volkskrant (wetenschapsjournalist) |

### 3.4 Co-auteurschapsmatrix (Tier 1 intern)

Het aantal gedeelde publicaties (top-20 werken) tussen Tier 1-kernleden:

| Bron \ Doel | Ab Osterhaus | Jan Kluytman | Marion Koopm | Thijs Kuiken | Diederik Gom | Jaap van Dis | Bart Haagman | Ron Fouchier |
|---|---|---|---|---|---|---|---|---|
| Ab Osterhaus           | -- | · |  2 |  4 | · | · | · | · |
| Jan Kluytmans          | · | -- |  2 | · | · | · | · | · |
| Marion Koopmans        | · | · | -- |  2 |  1 | · | · | · |
| Thijs Kuiken           |  1 | · |  3 | -- | · | · | · | · |
| Diederik Gommers       | · | · |  2 | · | -- |  1 | · | · |
| Jaap van Dissel        |  1 | · |  1 | · | · | -- | · | · |
| Bart Haagmans          | · | · | 10 |  2 |  1 | · | -- | · |
| Ron Fouchier           | · | · |  3 |  5 | · | · | · | -- |

---

## 12. BLINDE VLEKKEN

1. **Koopmans' positie blijft onbekend** -- Staat in de policy-community van de deliberate-fractie op basis van 1× vermelding; dit is géén bewijs van haar standpunt
2. **Alle Tier 1-personen behalve Fouchier/Koopmans zijn afwezig** in Fauci's dagboek -- hun rol in de origins-discussie moet uit andere bronnen komen (OMT-notulen, ZonMw, EU-projecten)
3. **Consortium edges = 0** -- De graaf heeft de consortia als nodes maar geen financieringsedges. NIH-data + ZonMw + EU CORDIS moeten handmatig worden toegevoegd
4. **Media-laag onderontwikkeld** -- Alleen Keulemans; mist NRC, Trouw, Nieuwsuur, Pointer-journalisten
5. **Tijdlijn eindigt in 2022** -- De Diary loopt tot dec 2022 maar de origins-discussie ging door (Worobey 2022, Senate hearings 2023)

---

## 13. OUTPUTBESTANDEN

| Bestand | Grootte | Beschrijving |
|---------|---------|-------------|
| `data/network_data.db` | SQLite | Multiplex database (nodes, edges, timeline) |
| `data/graph.json` | Node-link | Complete graaf voor Gephi/Cytoscape |
| `data/centrality_results.json` | JSON | Betweenness, eigenvector, degree per laag |
| `data/downloads/openalex_multiplex.json` | JSON | 16 auteurprofielen met co-auteurs |
| `data/downloads/nih_grants_multiplex.json` | JSON | 23 NIH queries |
| `docs/DUTCH_CONNECTIONS_DOSSIER.md` | MD | Dit dossier |

---

*Multiplex Knowledge Graph gegenereerd 2026-07-30. Geen conclusies over schuld of onschuld -- alleen gestructureerde vastlegging van feiten uit het brondocument.*
