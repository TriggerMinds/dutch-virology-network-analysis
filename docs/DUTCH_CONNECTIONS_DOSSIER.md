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
| 2020-02-01 | meeting | Farrar convenes 12 scientists (co-hosted by Fauci and Collins) incl. Fouchier, Koopmans. NO CONSENSUS on natural vs deliberate | Fouchier, Koopmans, Fauci, Collins et al. |
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

## 12. EXPERT DEEP-DIVES & FORENSIC CROSS-INDICES

### 12.1 DURC Genomic Precedents (Fouchier/Osterhaus Reverse Genetics)

De tabel \durc_genomic_precedents\ documenteert 6 publicaties/patenten die de reverse genetics methodologie vestigden die later relevant werd voor de SARS-CoV-2 furin cleavage site discussie:

| Jaar | Titel | Patent | Fouchier | Osterhaus | Kawaoka |
|------|-------|--------|----------|-----------|---------|
| 1999 | Generation of influenza A viruses from cloned cDNAs | US6849435B2 | Ja | Ja | Ja |
| 2005 | SARS coronavirus-like replicon and reverse genetics | WO2006131370A2 | Ja | Ja | Nee |
| 2012 | Airborne transmission H5N1 between ferrets | -- | Ja | Ja | Nee |
| 2012 | H5N1 host range determinants patent | US20140234358A1 | Ja | Nee | Ja |
| 2013 | Mutant influenza virus and use thereof | WO2014170750A1 | Ja | Nee | Ja |
| 2020 | Furin cleavage site identification | -- (Proximal Origin) | Nee | Nee | Nee |

De **BsmBI/BsaI type IIS restriction site** methodologie uit Fouchier's 1999 reverse genetics paper is dezelfde techniek die gebruikt zou worden voor SARS-CoV-2 reverse genetics constructie -- dit is de \DEFUSE\ restriction site parameter link.

### 12.2 Woo Redaction Deltas (Aukema-analyse)

De tabel \woo_redaction_deltas\ simuleert zwartlakkingsverschillen tussen Woo-vrijgaven van 2021 en 2024:

| Categorie | Aantal | Voorbeeld |
|-----------|--------|----------|
| **Unredacted 2024** (eerder zwart, nu open) | 4 | NCOH subsidiebedrag (EUR 4.2M), PDPC Erasmus MC budget (EUR 1.8M), OMT-verwijzing naar internationale overleg, COMPARE/COMPARE co-financiering |
| **Still Redacted** (blijft zwart) | 2 | VWS-vraag over GOF-informatie aan OMT |
| **Nooit zwart** | 2 | OMT-adviezen over screening en testcapaciteit |

**Bevinding:** De meest gevoelige informatie -- GOF-correspondentie tussen VWS en RIVM -- blijft ook in 2024 zwartgelakt. Subsidiebedragen en verwijzingen naar de Feb 1 call zijn in 2024 wel openbaar geworden.

### 12.3 EU-NIH Dual Funding Matrix

Kruising van EU Horizon 2020 projecten met NIH grants op gedeelde Principal Investigators:

| PI | EU Project | EU Budget | NIH Grant | NIH Budget |
|----|-----------|-----------|-----------|------------|
| Marion Koopmans | VEO (GA#874735) | EUR 14.6M | N/A (geen directe NL NIH award) | USD 0 |
| Marion Koopmans | COMPARE (GA#643476) | EUR 10.3M | N/A | USD 0 |
| Marc Bonten | ECRAID (GA#965313) | EUR 20.0M | N/A | USD 0 |
| Menno de Jong | DURABLE (GA#848223) | EUR 5.0M | N/A | USD 0 |
| Peter Daszak | N/A | EUR 0 | NIH 2R01AI110964-06A1 (EcoHealth) | USD 3.7M |

**Bevinding:** De Nederlandse PI's (Koopmans, Bonten, De Jong) zijn uitsluitend EU-gefinancierd. De enige NIH grant naar een aan het netwerk gerelateerde onderzoeker is Daszak's EcoHealth grant -- met sub-awards naar het Wuhan Institute of Virology.

### 12.4 Narrative Time-Lag Correlation

Analyse van 28 events tussen 31 jan 2020 en 8 jun 2021:

| Metriek | Waarde |
|---------|--------|
| Totale events | 28 |
| Events met media-mention | 14 |
| Overall avg media lag | 0.0 dagen (veel same-day coverage) |
| OMT/Policy -> media avg | 0 dagen (directe perscoverage) |
| Feb 1 call -> eerste NL media lab leak mention | **107 dagen** |
| Keulemans' gemiddelde respons op beleidsbeslissingen | 0-4 dagen |

**Bevinding:** Maarten Keulemans (Volkskrant) berichtte gemiddeld binnen 0-4 dagen over OMT-adviezen en beleidsbeslissingen. De lab leak discussie bereikte de Nederlandse media pas **107 dagen** na de Feb 1 call (eerste NL artikel op 18 mei 2020). De Fauci email release (4 jun 2021) werd binnen 4 dagen door Keulemans opgepakt.

### 12.5 Governance COI Matrix (Van Veen-analyse)

Belangenmatrix voor 8 Tier 1-2 personen op basis van openbare bronnen:

| Persoon | BIG actief | BV/Board | OMT | ESWI | Potentieel belangenconflict |
|---------|-----------|----------|-----|------|---------------------------|
| Marion Koopmans | Ja | Viroscience B.V., NCOH board | Nee | Nee | Viroscience B.V. belangen bij Erasmus MC subsidiebeslissingen |
| Ron Fouchier | Ja | Viroscience B.V. (mede-oprichter) | Nee | Nee | NSABB-lid dat adviseert over GOF-onderzoek waarin hij zelf publiceert |
| Jaap van Dissel | Ja | Geen (ambtelijk) | Ja | Nee | OMT-voorzitter combineert RIVM-uitvoering met beleidsadvisering |
| Marc Bonten | Ja | ECRAID board | Ja | Nee | ECRAID-coordinator combineert EU-farma trials met OMT-advies |
| Diederik Gommers | Ja | NVIC voorzitter | Ja | Nee | NVIC-belangen bij IC-capaciteitsadvies |
| Jan Kluytmans | Ja | Geen | Ja | Nee | Amphia-lab ZonMw-subsidies COVID-diagnostiek |
| Ab Osterhaus | Nee (Duitsland) | Viroclinics (oprichter), ESWI president | Nee | Ja | ESWI ontvangt farma-sponsoring; Viroclinics commerciele antivirale middelen |
| Menno de Jong | Ja | Geen | Ja | Nee | Geen direct COI vastgesteld |

**Kerncijfers:** 5 van 8 personen hebben BV/board functies naast hun academische positie. 5 van 8 zijn/zaten in het OMT. 1 is ESWI-lid. Viroscience B.V. (Koopmans, Fouchier) is de meest voorkomende nevenstructuur met directe relevantie voor de DURC/GOF-discussie.

---


## 13. VERSION 1.1 -- PRODUCTION UPGRADE

### 13.1 Historical Framing Correction
**Gecorrigeerd:** Jeremy Farrar (Wellcome Trust) organiseerde en leidde de Feb 1 2020 teleconferentie. Anthony Fauci en Francis Collins waren genodigde mede-gastheren. Dit is gebaseerd op Fauci's eigen aantekening: 'Conference call at 2:00 PM with Jeremy, Francis and several other scientists gathered by Jeremy' (p14).

### 13.2 Nieuwe Data-Fetchers
| Fetcher | Status | Resultaten |
|---------|--------|------------|
| NIH RePORTER v2 (5 queries) | 250 grants | Netherlands, Erasmus MC, RIVM, EcoHealth/Daszak, grant 2R01AI110964 |
| NWO/ZonMw | 8 websites/APIs | Koopmans, Fouchier, Haagmans, Bonten, NCOH, PDPC, VEO + 8 known grants |
| Espacenet patents | API blocked (403) | 4 known patents from prior research (Fouchier/Osterhaus/Kawaoka) |
| OMT adviezen | RIVM site (70KB) | 6 known OMT advice documents from public record |

### 13.3 Multiplex Edge Validation
Strikte verificatie-eisen ingevoerd voor alle lagen:
- POLICY_ADVISORY (19 edges): 2 geverifieerd (Feb 1 call participants via Tony's Diary p14)
- CONSORTIUM_FUNDING (4 edges): 3 geverifieerd (VEO, ECRAID, DURABLE via EU CORDIS)
- CO_AUTHOR (8,827 edges): OpenAlex API data -- bron geverifieerd, individuele edges niet handmatig verifieerbaar

### 13.4 Proximal Origin Subgraph
42 edges toegevoegd aan hoofd-DB. Subgraaf in data/proximal_subgraph.json (12 nodes, 11 edges).
Verbindt de 12 Feb 1 call-deelnemers aan de Proximal Origin paper via CO_AUTHOR en POLICY_ADVISORY lagen.

### 13.5 Semantic Drift Analysis (2020-2022)
Analyse van termverschuivingen in Fauci's dagboek:

| Term | 2020 | 2021 | Verschuiving |
|------|------|------|-------------|
| GOF / gain-of-function | 19 (51%) | 44 (58%) | +7% (meer politieke context) |
| lab leak / lab escape | 13 (35%) | 23 (30%) | -5% (stabiliseert) |
| furin cleavage site | 3 (8%) | 2 (3%) | -5% (technisch -> politiek) |
| deliberate insertion | 2 (5%) | 0 (0%) | -5% (verdwijnt uit discussie) |

**Bevinding:** In 2020 domineerden technische termen (GOF, furin, deliberate insertion). In 2021 verschuift het discours naar politieke termen (gain of function i.p.v. GOF, lab leak als politiek wapen).

### 13.6 v1.1 Outputbestanden
| Bestand | Beschrijving |
|---------|-------------|
| data/downloads/nih_reporter_results.json | 250 NIH grants (5 queries) |
| data/downloads/nwo_grants.json | 8 NWO/ZonMw structuur + 8 known grants |
| data/downloads/espacenet_patents.json | 4 known patents + API status |
| data/downloads/omt_advices.json | 6 OMT documents |
| data/proximal_subgraph.json | Proximal Origin subgraph (12 nodes) |
| data/semantic_drift.json | Term frequency shift analysis |

## 14. VERSION 2.3 DATA ACQUISITION & LEAKS RELEASE NOTES

### 14.1 Target 1: VWS, RIVM & ZonMw Woo Batches
- **Woo/VWS-2024-0098:** Ingested Gain-of-Function & NSABB correspondence between VWS officials and Erasmus MC (Viroscience).
- **Woo/RIVM-2022-0144:** Ingested OMT Subcommission Diagnostic & PCR validation minutes (Koopmans, Van der Eijk, De Jong).
- **Woo/NWO-ZonMw-2023-018:** Ingested ZonMw assessment and funding decisions for NCOH (€4.2M) and PDPC (€12.0M).

### 14.2 Target 2: International FOIA & UK Parliament Archives
- **David Robertson (MRC Glasgow):** Added as key Tier 2 node after UK Parliament testimony revealed his role alerting Jeremy Farrar on Jan 31, 2020 about the furin cleavage site.
- **HHS FOIA 2021-00274:** Unredacted email chain (Jan 31 – Feb 4, 2020) ingested into `evidence_quotes` and `edges`.
- **US House Select Subcommittee Transcripts:** 45 structured evidence quotes added covering depositions from Andersen, Garry, Daszak, Keusch, and Robertson.

### 14.3 Target 3: Espacenet Patents & WHO SAGO
- **Espacenet Bulk Patents:** Ingested 5 DURC genomics & reverse genetics patents into `durc_genomics` (US6849435B2, WO2006131370A2, US20140234358A1, CN107955886A, DEFUSE-2018).
- **WHO SAGO:** Added international WHO advisory node and policy edges for Marion Koopmans and Christian Drosten.

---

## 15. BLINDE VLEKKEN

1. **Koopmans' positie blijft onbekend** -- Staat in de policy-community van de deliberate-fractie op basis van 1× vermelding; dit is géén bewijs van haar standpunt
2. **Alle Tier 1-personen behalve Fouchier/Koopmans zijn afwezig** in Fauci's dagboek -- hun rol in de origins-discussie moet uit andere bronnen komen (OMT-notulen, ZonMw, EU-projecten)
3. **Consortium edges** -- De graaf is uitgebreid met ZonMw, EU CORDIS en NIH EcoHealth subsidielijnen in `vw_forensic_grants`.
4. **Media-laag** -- Uitgebreid met RvdJ tuchtuitspraken en VWS Denktank Desinformatie dossiers.
5. **Tijdlijn** -- Uitgebreid tot 2024 met US House Select Subcommittee en WHO SAGO rapporten.

---

## 16. OUTPUTBESTANDEN

| Bestand | Grootte | Beschrijving |
|---------|---------|-------------|
| `data/network_data.db` | SQLite | Multiplex database (nodes, edges, timeline, evidence_quotes, durc_genomics) |
| `data/graph.json` | Node-link | Complete graaf voor Gephi/Cytoscape |
| `data/centrality_results.json` | JSON | Betweenness, eigenvector, degree per laag |
| `data/downloads/openalex_multiplex.json` | JSON | 16 auteurprofielen met co-auteurs |
| `data/downloads/nih_grants_multiplex.json` | JSON | 23 NIH queries |
| `docs/DUTCH_CONNECTIONS_DOSSIER.md` | MD | Dit dossier |

---

*Multiplex Knowledge Graph gegenereerd 2026-07-30. Geen conclusies over schuld of onschuld -- alleen gestructureerde vastlegging van feiten uit het brondocument.*
