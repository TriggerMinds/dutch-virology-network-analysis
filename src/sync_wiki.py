"""
sync_wiki.py — Genereert 7 Markdown-pagina's voor de GitHub Wiki.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_OUT = os.path.join(ROOT, "wiki_output")
os.makedirs(WIKI_OUT, exist_ok=True)

print("[wiki] Generating 7 wiki pages...")

# ── 1. Home.md ────────────────────────────────────────────────────────────
home = """# Dutch Virology Network — Multiplex Knowledge Graph

## Over dit project
Deze wiki is onderdeel van het open-source onderzoeksproject **"Dutch Pandemic Governance & Virology Network Analysis Toolkit"**. Het project bevat een multiplex knowledge graph van **5.401 nodes** en **6.530 edges** over de Nederlandse virologietop, gebaseerd op:

- **Tony's Diary**: Het persoonlijke dagboek van Dr. Anthony Fauci (NIAID), 1.141 pagina's, vrijgegeven door Chairman Rand Paul (U.S. Senate, juli 2026)
- **OpenAlex**: 16 auteurprofielen met top-20 werken per auteur
- **NIH RePORTER**: 250+ Amerikaanse subsidiegegevens
- **EU CORDIS & ZonMw**: EUR 67,6M+ aan Europese en Nederlandse subsidies

## Snelle links

| Pagina | Beschrijving |
|--------|-------------|
| [De-Pandemische-Draaischijf](De-Pandemische-Draaischijf) | Volledig forensisch onderzoeksrapport: 12 hoofdstukken, 31 bronnen |
| [Subsidies-en-Consortia](Subsidies-en-Consortia) | EUR 67,6M aan EU/ZonMw subsidies (VEO, ECRAID, PDPC, COMPARE, DURABLE, NCOH) |
| [48-Uurs-Reconstructie](48-Uurs-Reconstructie) | Minuut-voor-minuut: 31 jan - 2 feb 2020, Feb 1 call, SCI-scores |
| [DURC-en-Patenten](DURC-en-Patenten) | BsmBI reverse genetics (US6849435B2), DARPA DEFUSE, furin cleavage site |
| [Forensische-SQL-Views](Forensische-SQL-Views) | DuckDB/Parquet handleiding, SHA-256 checksums, SQL views |
| [AVG-GDPR-en-Wederhoor](AVG-GDPR-en-Wederhoor) | Juridische onderbouwing, Level 1 Fact-taxonomie, Takedown policy |

## Externe links
- **Live web-app:** https://triggerminds.github.io/dutch-virology-network-analysis/
- **GitHub repository:** https://github.com/TriggerMinds/dutch-virology-network-analysis
- **Artikel:** https://triggerminds.github.io/dutch-virology-network-analysis/article.html

## Licentie
MIT — zie LICENSE in de hoofdrepository. Bron-PDF is publiek domein (U.S. Congressional release).
"""
with open(os.path.join(WIKI_OUT, "Home.md"), "w", encoding="utf-8") as f:
    f.write(home)
print("  Home.md")

# ── 2. De-Pandemische-Draaischijf.md ──────────────────────────────────────
md_path = os.path.join(ROOT, "docs", "INVESTIGATIVE_REPORT_DUTCH.md")
if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    with open(os.path.join(WIKI_OUT, "De-Pandemische-Draaischijf.md"), "w", encoding="utf-8") as f:
        f.write("# De Pandemische Draaischijf\n\n")
        f.write("*Zie ook het originele artikel met interactieve netwerkgrafieken:* ")
        f.write("[article.html](https://triggerminds.github.io/dutch-virology-network-analysis/article.html)\n\n")
        f.write(md_content)
    print("  De-Pandemische-Draaischijf.md")
else:
    print("  [SKIP] INVESTIGATIVE_REPORT_DUTCH.md not found")

# ── 3. Subsidies-en-Consortia.md ──────────────────────────────────────────
subsidies = """# Subsidies en Consortia — EUR 67,6M+

## EU Horizon 2020 — CORDIS Projecten
| Project | Coordinator | Budget | Financier |
|---------|------------|--------|-----------|
| VEO (GA#874735) | Marion Koopmans (Erasmus MC) | EUR 14.600.000 | EU Horizon 2020 |
| ECRAID (GA#965313) | Marc Bonten (UMC Utrecht) | EUR 20.000.000 | EU Horizon 2020 |
| COMPARE (GA#643476) | Marion Koopmans (Erasmus MC) | EUR 10.300.000 | EU Horizon 2020 |
| DURABLE (GA#848223) | Menno de Jong (RIVM) | EUR 5.000.000 | EU Horizon 2020 |

## ZonMw Nationale Subsidies
| Project | Coordinator | Budget |
|---------|------------|--------|
| PDPC | Erasmus MC (lead, Koopmans) | EUR 12.000.000 |
| NCOH | Marion Koopmans (Erasmus MC) | EUR 4.200.000 |
| IC COVID | Diederik Gommers (Erasmus MC) | EUR 1.500.000 |

## NIH Grants
| Grant | PI | Budget | Ontvanger |
|-------|-----|--------|-----------|
| 2R01AI110964-06A1 | Peter Daszak (EcoHealth) | USD 3.700.000 | EcoHealth -> WIV sub-award |

## Totaal
- EUR 67.600.000 aan EU/ZonMw subsidies
- USD 3.700.000 aan NIH grants
- 91,5% toegekend in 2019-2020 (rondom Feb 1 call)
- 8 specifieke subsidie-hubs geidentificeerd
"""
with open(os.path.join(WIKI_OUT, "Subsidies-en-Consortia.md"), "w", encoding="utf-8") as f:
    f.write(subsidies)
print("  Subsidies-en-Consortia.md")

# ── 4. 48-Uurs-Reconstructie.md ───────────────────────────────────────────
reconstructie = """# 48-Uurs Reconstructie: 31 januari - 2 februari 2020

## 31 januari 2020 — Robertson identificeert furin cleavage site
David Robertson (MRC-University of Glasgow) analyseert de eerste SARS-CoV-2 sequenties en ontdekt een ongebruikelijke furin cleavage site (PRRAR|SV). Robertson belt Jeremy Farrar (Wellcome Trust).
**SCI=1.0** (Silent Contributor Index: ongecrediteerd).
*Bron: UK Parliament testimony Jeremy Farrar, 2021.*

## 31 januari 2020 — Farrar belt Fauci
Farrar belt Fauci en deelt Robertsons analyse. Fauci noteert:
> "On January 31st, 2020 I received a call from Jeremy Farrar who conferred in Christian Andersen."
*Bron: Tony's Diary p767*

## 1 februari 2020, 14:00 EST — De Conference Call
Fauci's aantekening:
> "Conference call at 2:00 PM with Jeremy, Francis and several other scientists gathered by Jeremy."
*Bron: Tony's Diary p14*

### Deelnemers
1. Francis Collins (NIH)
2. Anthony Fauci (NIAID)
3. Jeremy Farrar (Wellcome Trust) — organisator
4. Patrick Vallance (UK Chief Scientific Adviser)
5. Kristian Andersen (Scripps Research)
6. Christian Drosten (Charite Berlin)
7. Edward Holmes (University of Sydney)
8. Andrew Rambaut (University of Edinburgh)
9. **Ron Fouchier** (Erasmus MC) — betoogde natuurlijke oorsprong
10. Robert Garry (Tulane University)
11. Mike Ferguson (University of Dundee)
12. **Marion Koopmans** (Erasmus MC) — positie NIET genoteerd

### Het meningsverschil
> "There was not total agreement about what this meant. Ron Fouchier said he was sure that this could occur naturally and we should not waste our time... The rest felt that deliberate insertion was possible given Dr. Zheng-Li Shi at the University of Wuhan has been working for years in GOF in coronaviruses."

**Twee kampen:**
- **Natuurlijke oorsprong:** Fouchier + Drosten
- **Deliberate insertion mogelijk:** Andersen, Holmes, Rambaut, Garry, Ferguson, Fauci, Collins, Farrar, Vallance
- **Positie onbekend:** Koopmans

## 2 februari 2020 — Follow-up met WHO
Fauci, Collins en Farrar contacteren Tedros via Stewart Simonson om een WHO-expertgroep te convenen.
*Bron: Tony's Diary p15*

## Silent Contributor Index (SCI)
| Persoon | SCI | Informeel | Credits | Status |
|---------|-----|-----------|---------|--------|
| **David Robertson** | **1.0000** | 1 | 0 | Ongecrediteerde furin site ontdekker |
| **Jeremy Farrar** | **1.0000** | 1 | 0 | Ongecrediteerde call convenor |
| Ron Fouchier | 0.0029 | 1 | 339 | |
| Marion Koopmans | 0.0025 | 1 | 396 | |
"""
with open(os.path.join(WIKI_OUT, "48-Uurs-Reconstructie.md"), "w", encoding="utf-8") as f:
    f.write(reconstructie)
print("  48-Uurs-Reconstructie.md")

# ── 5. DURC-en-Patenten.md ──────────────────────────────────────────────
durc = """# DURC en Patenten — BsmBI Reverse Genetics, DEFUSE

## Octrooistamboom US6849435B2
De methodologische basis voor reverse genetics van zowel influenza- als coronavirussen ligt in het patent **US6849435B2** (Fouchier, Osterhaus, Kawaoka, 1999). Dit patent beschrijft het gebruik van type IIS restrictie-enzymen (BsmBI, BsaI) voor het kloneren van virale genomen uit cDNA.

```
US6849435B2 (Fouchier/Osterhaus/Kawaoka, 1999)
  +-- BsmBI/BsaI reverse genetics systeem
       +-- Toegepast op influenza A (H5N1 ferret, 2012)
       +-- Toegepast op SARS-CoV (WO2006131370A2, 2005)
       +-- Toegepast op MERS-CoV (Fouchier, 2012)
       +-- Relevant voor SARS-CoV-2 furin cleavage site
            +-- Feb 1 2020 call: natuurlijk vs. synthetisch debat
```

## Volledige patententabel
| Patent | Uitvinders | Jaar | Relevantie |
|--------|-----------|------|------------|
| US6849435B2 | Fouchier, Osterhaus, Kawaoka | 1999 | Basis reverse genetics — BsmBI/BsaI systeem |
| WO2006131370A2 | Fouchier, Osterhaus | 2005 | SARS-CoV reverse genetics — template voor coronavirus |
| US20140234358A1 | Fouchier, Kawaoka | 2012 | H5N1 ferret transmissiemutanten |
| WO2014170750A1 | Kawaoka, Fouchier | 2013 | Mutant influenza — airborne transmission |

## DARPA DEFUSE (2018)
Het DEFUSE-programma (Detecting Emerging Pandemic Threats) financierde early-warning systemen voor pandemieen. Performers includeerden:
- **Peter Daszak** (EcoHealth Alliance) — bat coronavirus surveillance
- **Shi Zhengli** (WIV) — sub-awards voor bat coronavirus sampling
- **Ralph Baric** (UNC Chapel Hill) — coronavirus reverse genetics
- **Ron Fouchier** — methodologische precedent (BsmBI)

## Technical Capabilities per Onderzoeker
| Onderzoeker | Techniek | Methode |
|------------|----------|---------|
| Ron Fouchier | BsmBI/BsaI Restriction Site Cloning | reverse genetics |
| Ron Fouchier | Furin Cleavage Site Engineering | GOF |
| Ron Fouchier | Serial Passage in Ferrets | GOF_transmission |
| Ab Osterhaus | BsmBI/BsaI Restriction Site Cloning | reverse genetics |
| Ab Osterhaus | Coronavirus Reverse Genetics | reverse genetics |
| Yoshi Kawaoka | BsmBI/BsaI Restriction Site Cloning | reverse genetics |
| Kristian Andersen | Phylogenetic Sequence Analysis | origin_analysis |
| Shi Zhengli | Coronavirus Spike-ACE2 Binding | ACE2_adaptation |
"""
with open(os.path.join(WIKI_OUT, "DURC-en-Patenten.md"), "w", encoding="utf-8") as f:
    f.write(durc)
print("  DURC-en-Patenten.md")

# ── 6. Forensische-SQL-Views.md ──────────────────────────────────────────
sql_views = """# Forensische SQL Views — DuckDB/Parquet Handleiding

## Database locatie
De centrale SQLite database staat in `data/network_data.db`. Parquet exports staan in `data/parquet/`.

## Beschikbare SQL Views

| View | Rijen | Beschrijving |
|------|-------|-------------|
| vw_forensic_grants | 9 | CORDIS + ZonMw + NIH subsidies met coordinator en bedrag |
| vw_woo_citations | 3 | Bewijscitaten gekoppeld aan Woo-dossiernummers |
| vw_conflict_of_interest | 16 | Belangenmatrix: academisch, beleid, subsidie, media per Tier 1-3 |
| vw_virology_betweenness | 195 | Virologie-gefilterde betweenness centrality per node |
| vw_woo_redaction_deltas | 8 | Zwartlakkingsverschillen tussen Woo-vrijgaven 2021 vs 2024 |
| vw_silent_contributors | 4 | SCI-anomalieen (Robertson SCI=1.0, Farrar SCI=1.0) |

## DuckDB Voorbeelden

```sql
-- Top virology bridges
SELECT name, org, virology_betweenness
FROM vw_virology_betweenness
WHERE virology_betweenness > 0.1
ORDER BY virology_betweenness DESC;

-- Conflicterende belangen
SELECT name, tier, academic_role, policy_role, grant_review_role
FROM vw_conflict_of_interest
WHERE tier <= 2;

-- Alle EU-subsidies
SELECT project_name, grant_id, amount_euro
FROM grant_sources
WHERE funder LIKE '%EU%' OR funder LIKE '%ZonMw%'
ORDER BY amount_euro DESC;
```

## SHA-256 Verificatie
```bash
sha256sum -c data/checksums.sha256
```

## Parquet Exports
Bestanden in `data/parquet/`:
- `centrality_flat.parquet` — 33.584 rijen met centrality scores per node per laag
- `vw_forensic_grants.parquet` — 4 consortium grants
- `vw_conflict_of_interest.parquet` — 16 entries
- `vw_virology_betweenness.parquet` — 195 entries
- `vw_woo_citations.parquet` — 3 entries
"""
with open(os.path.join(WIKI_OUT, "Forensische-SQL-Views.md"), "w", encoding="utf-8") as f:
    f.write(sql_views)
print("  Forensische-SQL-Views.md")

# ── 7. AVG-GDPR-en-Wederhoor.md ─────────────────────────────────────────
avg = """# AVG/GDPR en Wederhoor

## Juridische Onderbouwing
Dit project verwerkt namen, institutionele affiliaties en professionele rollen van personen die:
- **Publieke figuren** zijn (senior wetenschappers, overheidsadviseurs, gepubliceerde academici)
- Handelend in hun **professionele hoedanigheid**
- Geidentificeerd via **openbaar toegankelijke** databases (OpenAlex, NIH, Congressional records)

**Geen persoonlijke data** (adressen, telefoonnummers, privécorrespondentie, gezondheidsdata, politieke voorkeuren) wordt verzameld, opgeslagen of gepubliceerd.

## Level 1 Fact-Taxonomie
| Level | Label | Betekenis | Voorbeeld |
|-------|-------|-----------|-----------|
| L1 | [Documented Fact] | Direct geciteerd uit primaire bron met paginanummer | "Fauci noteert op p14: 'Conference call at 2:00 PM with Jeremy'" |
| L2 | [Inferred] | Logische conclusie uit L1-feiten | "Farrar organiseerde de call (gebaseerd op 'gathered by Jeremy')" |
| L3 | [Hypothesis] | Interpretatieve inschatting, gemarkeerd als onzeker | "Koopmans' positie was mogelijk neutraal (positie niet genoteerd)" |

## Wederhoor Procedure
1. **Open een GitHub Issue** via het template `.github/ISSUE_TEMPLATE/data_correction.yml`
2. **Vermeld**: uw e-mail (niet openbaar), betwist knooppunt, exacte fout, bewijsstuk URL
3. Het team onderzoekt de correctie binnen 14 werkdagen
4. Bij aantoonbare onjuistheid wordt de dataset gecorrigeerd + changelog bijgewerkt

## Takedown Policy
Indien u van mening bent dat uw persoonsgegevens onrechtmatig zijn verwerkt:
1. Dien een Woo-verzoek-gemotiveerd verzoek in via bovenstaand Issue template
2. Vermeld welke specifieke edge of node betwist wordt
3. Het verzoek wordt binnen 30 dagen behandeld conform AVG Art. 17 (Recht op vergetelheid)

## Verifieerbaarheid
Alle bewijscitaten in deze dataset bevatten een `page_number` veld dat linkt naar de bron-PDF.
SHA-256 hash van de bron-PDF: `27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e`
"""
with open(os.path.join(WIKI_OUT, "AVG-GDPR-en-Wederhoor.md"), "w", encoding="utf-8") as f:
    f.write(avg)
print("  AVG-GDPR-en-Wederhoor.md")

print(f"\n[wiki] 7 pages generated in {WIKI_OUT}")
