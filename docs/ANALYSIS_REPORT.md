# ANALYSIS REPORT — "Tony's Diary Package"

**Datum:** 2026-07-30
**Bronbestand:** `2026.07.24_Tonys-Diary-Package.pdf` (69 MB, 1141 pagina's)
**Status:** Volledig geëxtraheerd, gestructureerd en opgeslagen in Knowledge Graph

---

## 1. Executive Summary

Het document is een vrijgave van **Chairman Rand Paul** (U.S. Senate) van het gepersonaliseerde dagboek van **Dr. Anthony Fauci**, getiteld *"Tony's Diary"*. Het beslaat de periode **januari 2020 t/m medio 2021** en beschrijft Fauci's perspectief op de COVID-19-pandemie, inclusief dagelijkse interacties met het Witte Huis, CDC, NIH, WHO, pers en farmaceuten.

**Belangrijkste vastgestelde feiten:**

| Feit | Pagina('s) |
|------|------------|
| Fauci was als NIAID-directeur nauw betrokken bij dagelijkse COVID-19 taskforce-overleggen | 3-80+ |
| Fauci's salaris ($400.000/jaar) overschreed dat van de VP en Chief Justice | p42 |
| NIAID-budget 2020: $4.75 miljard | p42 |
| Congress passeerde $8.3B supplement voor coronavirus (maart 2020) | p37 |
| POTUS tekende $2.2T (tot $6.2T) relief package (CARES Act) | p74 |
| EcoHealth Alliance / WIV wordt genoemd in context van gain-of-function en lab leak debat | multiple pages |
| Fauci had intensieve contacten met Collins, Birx, Redfield, Azar, Trump | passim |
| Operation Warp Speed, Moderna, Pfizer vaccinontwikkeling gedetailleerd | p210+ |

---

## 2. Overzicht van Entiteiten

### 2.1 Sleutelpersonen (top 30 op mention-frequency)

| Naam | Functie | Organisatie | Mentions |
|------|---------|-------------|----------|
| Chairman Rand / Rand Paul | U.S. Senator (vrijgever document) | U.S. Senate | 1127 |
| Fauci / Anthony Fauci | Director | NIAID/NIH | 663 |
| Trump / Donald Trump | President (2020) | White House | 308 |
| Chris / Christine Grady | Bioethicist, NIH | NIH | 159 |
| Biden / Joe Biden | President (2021) | White House | 148 |
| Birx / Deborah Birx | COVID-19 Response Coordinator | White House | 87 |
| Collins / Francis Collins | NIH Director | NIH | 82 |
| Meadows / Mark Meadows | Chief of Staff | White House | 70 |
| Redfield / Robert Redfield | CDC Director | CDC | 65 |
| Azar / Alex Azar | HHS Secretary | HHS | 61 |
| Pence / Mike Pence | Vice President | White House | 47 |
| Hahn / Stephen Hahn | FDA Commissioner | FDA | 38 |
| Walensky / Rochelle Walensky | CDC Director (2021) | CDC | 37 |

### 2.2 Sleutelorganisaties

| Organisatie | Type | Mentions |
|-------------|------|----------|
| WHO | Internationale organisatie | 495 |
| CIA | Inlichtingendienst | 344 |
| White House | Overheid (uitvoerend) | 252 |
| CNN | Media | 216 |
| CDC | Overheid (gezondheid) | 187 |
| NIH | Overheid (onderzoek) | 174 |
| Washington Post | Media | 143 |
| FDA | Overheid (regulering) | 121 |
| NIAID | Overheid (onderzoek-infectieziekten) | 113 |
| Congress | Overheid (wetgevend) | 99 |
| HHS | Overheid (gezondheid) | 91 |
| Fox News | Media | 60 |
| Nature | Wetenschappelijk tijdschrift | 29 |

### 2.3 Financiële stromen

| Bedrag | Context | Pagina |
|--------|---------|--------|
| $145M | NIAID-budgetaanvraag | p30 |
| $8.3B | Congressional COVID-19 supplement | p37 |
| $4.75B | NIAID 2020 budget | p42 |
| $2.2T – $6.2T | CARES Act relief package | p74 |
| $1T – $3T | Trillion-dollar stimulus discussions | p199-200 |
| $100/dose | Pfizer vaccine pricing (non-starter) | p210 |

### 2.4 Gedetecteerde relaties

| Relatietype | Aantal |
|-------------|--------|
| CONNECTED_TO (persoon ↔ organisatie) | 1169 |
| CO_MENTIONED_WITH (persoon ↔ persoon) | 803 |
| CO_AUTHOR_WITH | 29 (bevat ruis) |
| FUNDED_BY | 1 |

**Centrale hubpersonen in het netwerk:**
- **Fauci** (97 directe connecties) — centrale knooppunt tussen WH, CDC, NIH, media
- **Trump** (84 connections) — politieke context
- **Biden** (68 connections) — politieke context
- **Collins** (66 connections) — NIH-brug naar alle gezondheidsinstanties
- **Chris Grady** (69 connections) — opvallend centrale positie voor een niet-publieke figuur

---

## 3. Kwetsbaarheden & Blinde Vlekken

### 3.1 Beperkingen van de extractie

1. **Geen contextuele NER** — De huidige NER is gebaseerd op keyword-matching, geen ML/NLP. Dit levert ruis op (bv. "Infectious Diseases" wordt als persoon aangemerkt).
2. **Co-auteurschapsdetectie** — De regex-based aanpak produceert false positives bij meerledige zinnen met line breaks.
3. **Geen OCR** — Pagina's 1-2 bevatten geen tekst (mogelijk grafieken/titels). Indien er gescande bijlagen in latere pagina's zitten, zijn deze gemist.
4. **Financiële extractie** — Alleen dollarbedragen met een eenheid worden gevangen. Indirecte geldstromen (subsidies, grants via derde partijen) worden niet automatisch gelinkt.

### 3.2 Externe registers die geraadpleegd moeten worden

| Register | Doel |
|----------|------|
| **KvK / Netherlands Chamber of Commerce** | Nederlandse entiteiten checken (stichtingen, EcoHealth-connecties) |
| **PubMed / Crossref** | Co-auteurschapsnetwerken valideren van genoemde publicaties |
| **ZonMw** | Nederlandse COVID-19 subsidiebesluiten |
| **Woo-besluiten (NL)** | Openbaargemaakte documenten over COVID-19-beleid |
| **USASpending.gov** | Amerikaanse federale contracten en subsidies (BARDA, NIH) |
| **Open Payments (CMS)** | Farmaceutische betalingen aan artsen/onderzoekers |
| **Senate Lobbying Disclosure** | Lobbycontacten farma-Witte Huis |
| **NIH RePORTER** | NIAID grants en projecten |
| **Federal Register** | Regelgevingsdocumenten FDA/HHS |

### 3.3 Open vragen uit het document

1. Wat is de exacte rol van **EcoHealth Alliance** en **Peter Daszak** in de gain-of-function discussie?
2. Welke **Wuhan Institute of Virology**-connecties worden genoemd en door wie?
3. Welke interne **evaluaties/klokkenluiders** zijn er met betrekking tot CDC's testing failure (feb 2020)?
4. Wat was de aard van Fauci's interacties met **Gates Foundation** — niet prominent in de first-pass extraction
5. Hoe verhouden de in het dagboek genoemde bedragen (NIAID budget, CARES Act) zich tot **NIH-subsidies** aan individuele labs?

---

## 4. Aanbevolen Vervolgstappen

| Stap | Actie | Prioriteit |
|------|-------|------------|
| 1 | **Verbeter NER** met SpaCy of een klein getraind model voor betere persoon/org-discriminatie | Hoog |
| 2 | **Cross-reference PubMed** — zoek naar publicaties van genoemde co-auteurs (Fauci, Morens, Daszak, etc.) en bouw een citation network | Hoog |
| 3 | **USASpending query** — download alle NIH/BARDA COVID-contracten en match met entiteiten in de KG | Hoog |
| 4 | **Media-monitoring** — extraheer journalisten die Fauci bevroegen (George Stephanopoulos, Chris Wallace, etc.) voor bias-analyse | Medium |
| 5 | **Tijdlijn reconstructie** — bouw een chronologische tijdlijn van events uit de diary entries met datumpatronen | Hoog |
| 6 | **Open Payments download** — check farma-betalingen aan Fauci, Collins, Birx, Redfield | Medium |
| 7 | **Woo-verzoek Nederland** — onderzoek of Nederlandse instanties (RIVM, VWS) corresponderen met genoemde Amerikaanse actoren | Laag |

---

## 5. Outputbestanden

| Bestand | Beschrijving |
|---------|-------------|
| `raw_data.json` | Pagina-voor-pagina geëxtraheerde tekst (1141 entries) |
| `network_data.db` | SQLite database met entiteiten, relaties en audittrail |
| `graph.json` | NetworkX-graph export (node-link formaat) |
| `extract_pdf.py` | Stage 1 extraction script |
| `build_kg.py` | Stage 2 KG building script |
| `ANALYSIS_REPORT.md` | Dit rapport |

---

*Einde analyse. Voor verdere verfijning: voer NLP-verbeterde NER uit op raw_data.json of integreer externe registers via de bovenstaande aanbevelingen.*
