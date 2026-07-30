# Critical Blind-Spot Mapping & Methodological Audit

> **Document status:** Living document — updates expected as new sources are integrated.
> **Scope:** Epistemological audit of findings derived from *Tony's Diary (Fauci)*, NIH RePORTER, and OpenAlex, focused on Dutch institutional involvement in early COVID-19 origins discourse (Jan–Mar 2020).

---

## 1. Feitelijke correcties op de dataset

### 1.1 Koopmans' "9 February 2020 email" bestaat niet in deze bron

**Foutieve aanname in vroege extractie:** De timeline bevatte een entry "Koopmans co-authors paper or communication re: early origin analysis (9 Feb 2020, referenced in Fauci diary context)."

**Correctie:** Deze entry is **gefabriceerd** — hij staat niet in Fauci's dagboek. Koopmans wordt **één keer** genoemd (p14, participant list). De verwarring ontstaat doordat de Washington Post FOIA-release van Fauci's e-mails wél correspondentie met Koopmans bevat (zie https://www.washingtonpost.com/context/fauci-emails/). Het dagboek is een **persoonlijk narratief**, geen e-mailarchief. De entry is verwijderd.

**Les:** Scheid strikt tussen *diary entries* (subjectief, contemporain narratief) en *email releases* (objectievere communicatie, andere FOIA-bron).

### 1.2 NIH grants — geen directe Nederlandse financiering gevonden

**Aanname:** NIH RePORTER bevat Nederlandse instellingen als grant-ontvangers.

**Correctie:** De zoekterm "Netherlands" in NIH RePORTER vindt projecten die *Nederland in de abstract noemen* (vergelijkingsstudies, etc.), niet aan NL-instellingen toegekende grants. Alle 50 gevonden grants zijn Amerikaans. Voor de vraag of Erasmus MC / Fouchier / Koopmans NIH-subsidie ontvingen is een **org-filter "ERASMUS"** nodig in de NIH RePORTER webinterface (API limiteert buitenlandse org-query's).

### 1.3 OpenAlex co-auteurs netwerk — beperkte steekproef

**Aanname:** De 10 top-geciteerde werken per auteur geven een representatief co-auteursbeeld.

**Correctie:** De OpenAlex fetch haalde alleen de **top-10 meest geciteerde werken** per auteur (±157 unieke co-auteurs voor Fouchier). Dit is een selectiebias naar oudere, veel-geciteerde publicaties (vooral MERS/Influenza). Het netwerk van **COVID-19-specifieke co-auteurschappen** (2020) is hiermee **ondervertegenwoordigd**. Fouchier heeft 636 totale werken — de overige 626 zijn niet meegenomen.

### 1.4 Status Koopmans' positie op de teleconferentie van 1 februari 2020 (GEAUDITEERD)

**Foutieve aanname/onduidelijkheid vooraf:** Was Marion Koopmans aanwezig op de teleconferentie van 1 februari 2020 en wat was haar standpunt over de furin cleavage site en de lab-origin hypothese?

**Auditresultaat (juli 2026):**
- **Aanwezigheid:** Bevestigd op pagina 14 van *Tony's Diary* (`M.P.G. Koopmans, Head of Department of ViroScience, Erasmus Medical Center, NL`).
- **Standpunt/Citaat:** **Niet genoteerd.** Fauci vat de standpunten op de call expliciet samen voor Ron Fouchier ("sure that this could occur naturally"), Christian Drosten ("was with Ron"), en "the rest" (voorstanders van verder onderzoek naar deliberate insertion). Koopmans wordt in de lopende tekst niet geciteerd of genoemd als spreker.
- **Formele status:** Overeenkomstig TEAMDYNAMICA-regels is haar positie op de call geclassificeerd als **`UNKNOWN`** in de database (`koopmans_feb1_audit`) en de multiplex graph (`data/graph.json`).

---

## 2. Ontbrekende perspectieven & argumenten

### 2.1 Het "proximal origin" paper (maart 2022)

De paper *"The Proximal Origin of SARS-CoV-2"* (Andersen et al., Nature Medicine, DOI: 10.1038/s41591-020-0820-9) wordt in het dagboek genoemd op p805 (juli 2021, als preprint). Deze paper wordt algemeen beschouwd als het belangrijkste wetenschappelijke argument voor natuurlijke oorsprong. **Maar:** de paper is geschreven door *Kristian Andersen*, *Robert Garry* en anderen — allen deelnemers aan de Feb 1 call of nauw daaraan gelieerd. Dit roept de vraag op: was de Feb 1 call het startpunt voor wat later de "natural origin consensus" zou worden?

De dataset bevat deze link **niet** als edge — een gemiste relatie tussen "Feb 1 Conference Call" en "Proximal Origin paper".

### 2.2 De rol van EcoHealth Alliance — onderschat

Peter Daszak (EcoHealth Alliance) wordt niet genoemd in de Feb 1 call maar komt 7× voor in lab-leak context (p792, 805, 833, 888, 893, 947, 1064). EcoHealth's NIH-subsidie (grant #2R01AI110964-06A1, "Predicting virus emergence from wildlife") was direct aan Daszak in New York, met sub-awards naar het Wuhan Institute of Virology. Dit is **cruciaal** voor de financieringsvraag in het lab-leak debat, maar deze grant **ontbreekt** in de NIH RePORTER query (omdat de query "Netherlands" zocht, niet "EcoHealth").

### 2.3 DEFUSE-programma

Het DARPA DEFUSE (Detecting Emerging Pandemic Threats) programma wordt **0 keer** genoemd in het dagboek. Dit programma financierde early-warning systemen voor pandemieën, inclusief werk met bat coronavirussen. DEFUSE wordt in congresonderzoeken (House Select Subcommittee on the Coronavirus Pandemic, 2023) genoemd als relevant voor de WIV-samenwerking. De afwezigheid in Fauci's dagboek betekent **niet** dat het niet relevant is — het betekent alleen dat Fauci het niet in zijn persoonlijke notities besprak.

---

## 3. "Unknown Unknowns" — wat ik waarschijnlijk over het hoofd zie

> Dit zijn domeinen, concepten of verbanden waarvan ik het bestaan ken maar de relevantie voor deze specifieke casus niet kan beoordelen. Ze zijn geordend van hoogste naar laagste impactkans.

### 3.1 De 31 Januari 2020 e-mail van Jeremy Farrar (HOOGSTE IMPACT)

**Wat ik weet:** Fauci schrijft op p767: *"on January 31st, 2020 I received a call from Jeremy Farrar who conference called me"*.

**Wat ik niet weet:** Farrar heeft later (2021, in getuigenis voor het Britse parlement) gezegd dat hij Fauci belde *omdat een van zijn Wellcome Trust-onderzoekers de sequentieanalyse had gedaan*. Die onderzoeker was **David Robertson** (University of Glasgow), die de furin cleavage site identificeerde en Farrar alarmeerde. Robertson is **niet** genoemd in het dagboek. Heeft Robertson directe of indirecte banden met Nederlandse GOF-onderzoekers? Robertson's werk op het gebied van virale evolutie overlapt met Fouchier's netwerk.

**Hoe te verifiëren:** PubMed search op "Robertson furin cleavage site January 2020" + check of Robertson co-auteur is met Fouchier/Koopmans.

### 3.2 De virologische evidentie voor natuurlijke oorsprong (GEMIDDELDE IMPACT)

**Wat ik weet:** Fouchier en Drosten betoogden op de Feb 1 call dat de furin cleavage site natuurlijk kon ontstaan. De rest vond deliberate insertion mogelijk.

**Wat ik niet weet:** De **moleculaire argumenten** die Fouchier en Drosten op die call presenteerde. Zonder de transcriptie van de Feb 1 call (die waarschijnlijk niet bestaat) kunnen we alleen afgaan op Fauci's samenvatting. De meerderheid van virologen (in 2020-2021) accepteerde uiteindelijk de "natural origin" hypothese — maar was dat door de wetenschappelijke argumenten of door politieke/mediadruk?

**Hoe te verifiëren:** Vergelijk Fouchier's argument (zoals door Fauci weergegeven) met zijn gepubliceerde positie in *"The proximal origin of SARS-CoV-2"* (Andersen et al., 2020). Fouchier is **geen** co-auteur van die paper — terwijl Andersen, Holmes, Garry (allen "deliberate"-faction) dat wel zijn. Betekent dit dat Fouchier's positie (natuurlijk) verloren heeft in de wetenschappelijke arena? Of dat hij simpelweg niet is uitgenodigd als co-auteur?

### 3.3 De rol van de Amerikaanse inlichtingengemeenschap (GEMIDDELDE IMPACT)

**Wat ik weet:** p863 beschrijft dat de IC een split had: *"most elements felt natural occurrence ... except FBI who felt strongly lab leak"*.

**Wat ik niet weet:** De intelligence die ten grondslag lag aan dit oordeel is niet openbaar. Het FBI-standpunt kan gebaseerd zijn op HUMINT uit China, SIGNINT, of open-source analyse. **Nederlandse inlichtingendiensten** (AIVD, MIVD) hebben mogelijk eigen analyses gemaakt — Nederland heeft nauwe intelligence-sharing relaties met de VS (Nine Eyes). De AIVD heeft in 2021 verklaard geen bewijs van lab leak te hebben, maar de *onderbouwing* van die conclusie is niet openbaar.

**Hoe te verifiëren:** Woo-verzoek bij AIVD naar eventuele betrokkenheid bij COVID-19 origins intelligence. Check Kamerstukken 2021-2022 over COVID-origins.

### 3.4 De "Koopmans-Münster" spiering-as (LAGE IMPACT, HOGE CONCEPTUELE RELEVANTIE)

**Wat ik weet:** Marion Koopmans is **Head of Viroscience** aan Erasmus MC, gespecialiseerd in **veterinaire virologie, zoönosen en voedseloverdraagbare virussen**.

**Wat ik niet weet:** Koopmans' expertise is **niet** lab-origin of gain-of-function — haar specialisme is **surveillance, diagnostiek, en natuurlijke spillover**. Dit is consistent met de Feb 1 call: zij was uitgenodigd voor haar expertise in natuurlijke spillover detectie, **niet** voor GOF-discussie. Dit verklaart waarom Fauci **haar positie niet noteerde** — zij sprak misschien niet over de GOF-kwestie maar over surveillance en diagnostische protocollen.

**Concept:** Er is een **tweedeling in de virologische gemeenschap** tussen "surveillance virologists" (Koopmans-type: natuurlijke spillover detectie) en "GOF virologists" (Fouchier-type: functionele karakterisering in labs). Deze tweedeling is zichtbaar in de Feb 1 call maar wordt in de literatuur zelden expliciet gemaakt.

### 3.5 Proximal Origin paper — Co-auteurs netwerk (LAGE IMPACT, HOGE VERIFICATIE)

**Wat ik doe:** Ik heb OpenAlex top-10 werken van Fouchier, Koopmans, Fauci en Farrar gedownload.

**Wat ik niet doe:** Ik heb **niet** de co-auteurs van de Proximal Origin paper (Andersen, Garry, Monie, Rambaut, Holmes) in de dataset opgenomen — terwijl **Andersen, Holmes en Rambaut wél** op de Feb 1 call zaten. Dit betekent dat er een directe lijn is: Feb 1 call → Proximal Origin paper (2020) → Nature Medicine paper (2022). De dataset mist alle edges tussen deze paper en de call-deelnemers.

---

## 4. Aanbevolen externe bronnen per blind spot

| # | Blind spot | Bron | Prioriteit |
|---|-----------|------|-----------|
| 3.1 | Robertson (Farrar's adviser) | PubMed: Robertson DL, University of Glasgow | Hoog |
| 3.2 | Transcript Feb 1 call | Vraag bij deelnemers op (Fouchier, Koopmans, Farrar) — bestaat waarschijnlijk niet | Hoog |
| 3.2 | Proximal Origin co-authors | https://doi.org/10.1038/s41591-020-0820-9 | Hoog |
| 3.3 | AIVD COVID-origins | Woo-verzoek | Medium |
| 3.4 | Koopmans' expertise profiel | https://www.erasmusmc.nl/nl/research/onderzoekers/koopmans-mpg-marion | Medium |
| 3.5 | Proximal Origin ↔ Feb 1 call | Edge-analyse in graph.json — moet worden toegevoegd | Medium |
| 2.2 | EcoHealth NIH grant #2R01AI110964-06A1 | NIH RePORTER: zoek op appl_id van deze grant | Medium |
| 2.1 | Robertson-Fouchier co-auteurs | OpenAlex: Robertson co-authorship with Fouchier | Laag |

---

## 5. Epistemologische kwalificaties bij de dataset

Elk datapunt in `network_data.db` en `graph.json` moet worden gelezen met de volgende kwalificaties:

1. **Contemporain ≠ objectief:** Fauci's dagboek is contemporain (geschreven op de dag zelf), wat het waardevoller maakt dan retrospectieve memoires — maar het is nog steeds Fauci's subjectieve weergave.
2. **Geen correspondentie:** Het dagboek bevat **geen e-mails**. Citaten over wat iemand "zei" of "schreef" zijn tweedehands.
3. **Selectieve notitie:** Fauci noteerde niet alles. Koopmans' positie ontbreekt — niét omdat ze die niet had, maar omdat Fauci het niet opschreef.
4. **OpenAlex steekproef:** Alleen top-10 werken per auteur — geen volledig co-auteurs netwerk.
5. **NIH RePORTER:** Alleen Amerikaanse grants. Europese (ERC, NWO, ZonMw) financiering is niet meegenomen.

---

## 6. Geïntegreerde Forensische Dossiers & Datasets (Juli 2026 Audit)

De volgende aanvullende dossiers en datasets zijn formeel verankerd in de repository:

- **WOO-Afwijzingen & Zwartlakking Analyse:** [WOO_REFUSAL_ANALYSIS.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/WOO_REFUSAL_ANALYSIS.md)  
  *Dataset:* `data/processed/woo_refusal_matrix.json` & CSV (Art. 5.2 beleidsopvattingen 68.5%, Art. 5.1 sub c bedrijfsvertrouwelijkheid 42.0%).
- **ECRAID Foundation & OMT Dubbelrollen:** [ECRAID_FORENSIC_DOSSIER.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/ECRAID_FORENSIC_DOSSIER.md)  
  *Dataset:* `data/processed/ecraid_forensic_matrix.json` & CSV (Marc Bonten CEO €20M GA#965313, Koopmans POS-Disease X lead).
- **Nederlandse Inlichtingenpositie (AIVD/MIVD):** [NL_INTELLIGENCE_ORIGINS.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/NL_INTELLIGENCE_ORIGINS.md)  
  *Status:* `UNRECORDED_NEUTRAL` (Kamerstuk 25 295 nr 1180, AIVD Jaarverslag 2020).
- **Media-Narratief & 107-Dagen Lag:** [MEDIA_NARRATIVE_NL.md](file:///c:/Users/gewoo/Desktop/New%20folder%20(4)/docs/MEDIA_NARRATIVE_NL.md)  
  *Status:* 25+ geëncodeerde artikelen (Volkskrant, NRC, NOS, Nieuwsuur).
- **Volledige Geldstromen Matrix:** `data/processed/dutch_funding_matrix.json` & CSV  
  *Totaal:* €49,9M EU Horizon 2020 + €17,7M ZonMw + $3,7M NIH + Viroscience B.V. KVK #24416174 audit.

---

*Mapping generated 2026-07-30. Dit is een living document — voeg nieuwe blind spots toe zodra ze worden geïdentificeerd.*
