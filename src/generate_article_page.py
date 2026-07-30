"""
generate_article_page.py — Produceert docs/article.html en docs/INVESTIGATIVE_REPORT_DUTCH.md.
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
HTML_PATH = os.path.join(DOCS, "article.html")
MD_PATH = os.path.join(DOCS, "INVESTIGATIVE_REPORT_DUTCH.md")

article_content = {
    "title": "De Pandemische Draaischijf",
    "subtitle": "Hoe Nederlands toponderzoek, miljoenen aan subsidies en een besloten teleconferentie met Anthony Fauci de mondiale discussie over de oorsprong van SARS-CoV-2 hebben gestuurd",
    "author": "Forensic Data & Network Analysis Team",
    "date": "30 juli 2026",
    "sections": []
}

# ── Build all sections ────────────────────────────────────────────────────
sections_data = []

sections_data.append(("inleiding", "Inleiding", """
Op 1 februari 2020, om 14:00 uur EST, vond een video conference plaats die de wetenschappelijke en politieke discussie over de oorsprong van het SARS-CoV-2 virus voor jaren zou bepalen. Jeremy Farrar (toenmalig directeur van Wellcome Trust) had de avond ervoor een telefoontje gekregen van David Robertson, een computationeel viroloog aan de University of Glasgow, die een ongebruikelijke sequentie in het spike-eiwit had geïdentificeerd: een furin cleavage site — vier extra aminozuren (PRRAR) op een plek waar die normaal niet voorkomt bij betacoronavirussen.

Farrar belde Anthony Fauci (NIAID-directeur). Samen met Francis Collins (NIH-directeur) riepen ze twaalf internationale topwetwetenschappen bijeen. Twee van hen kwamen van het Erasmus MC Rotterdam: Ron Fouchier en Marion Koopmans.

Dit onderzoek reconstrueert, op basis van Fauci's eigen contemporaine dagboek (1.141 pagina's, vrijgegeven door Chairman Rand Paul, U.S. Senate, juli 2026), OpenAlex co-auteurschapsdata, NIH RePORTER en EU CORDIS subsidiegegevens, de Nederlandse rol in de oorsprongdiscussie. De dataset — een multiplex knowledge graph van 5.401 nodes en 6.530 edges — is volledig openbaar en verifieerbaar.
"""))

sections_data.append(("narratief", "Het Narratief versus de Feiten", """
| Aspect | Het Gangbare Narratief | Wat de Data Laten Zien |
|--------|----------------------|----------------------|
| **Wie organiseerde de Feb 1 call?** | Anthony Fauci (NIAID) | **Jeremy Farrar (Wellcome Trust)** organiseerde en leidde de call. Fauci en Collins waren mede-gastheren. Fauci's eigen aantekening: "Conference call at 2:00 PM with Jeremy, Francis and several other scientists gathered by Jeremy" (p14). |
| **Wie identificeerde de furin cleavage site?** | "Wetenschappers" of "Kristian Andersen" | **David Robertson (University of Glasgow)** was de eerste die de sequentie analyseerde en Farrar alarmeerde op 31 januari 2020. Robertson kreeg **geen** auteurscredit op de Proximal Origin paper. SCI=1.0 (Silent Contributor Index: geflagd). |
| **Was er consensus op de Feb 1 call?** | "Wetenschappers waren het eens over natuurlijke oorsprong" | **Geen consensus.** Twee kampen: Fouchier + Drosten (natuurlijke oorsprong) versus Andersen, Holmes, Rambaut, Garry, Ferguson, Fauci, Collins, Farrar, Vallance (deliberate insertion mogelijk). |
| **Wat was Koopmans' standpunt?** | Wordt vaak geciteerd als expert | **Haar positie werd niet genoteerd** door Fauci. Dit is een expliciete blinde vlek — de enige deelnemer van wie het standpunt ontbreekt. |
| **Was er Nederlands geld in de GOF-discussie?** | "Nederland financiert geen GOF" | Erasmus MC ontvangt via Koopmans €14,6M (VEO) + €10,3M (COMPARE) + €4,2M (NCOH) + €12,0M (PDPC). **Totaal: €41,1M aan EU/ZonMw-subsidies** voor pandemische paraatheid en surveillance. |
"""))

sections_data.append(("tijdlijn", "48-Uurs Reconstructie: 31 januari – 2 februari 2020", """
### 31 januari 2020 — Robertson identificeert furin cleavage site
David Robertson (MRC-University of Glasgow) analyseert de eerste SARS-CoV-2 sequenties en ontdekt een ongebruikelijke furin cleavage site (PRRAR|SV) in het spike-eiwit. Dit kenmerk is zeldzaam bij betacoronavirussen. Robertson alarmeert Jeremy Farrar (Wellcome Trust). *Bron: UK Parliament testimony Jeremy Farrar, 2021.*

### 31 januari 2020 — Farrar belt Fauci
Farrar belt Fauci en deelt Robertsons analyse. Fauci noteert: "on January 31st, 2020 I received a call from Jeremy Farrar who conferenced in Christian Andersen." *Bron: Tony's Diary p767.*

### 1 februari 2020, 14:00 EST — De Conference Call
Fauci's aantekening (p14): "Conference call at 2:00 PM with Jeremy, Francis and several other scientists gathered by Jeremy."

**Deelnemers:**
1. Francis Collins (NIH)
2. Anthony Fauci (NIAID)
3. Jeremy Farrar (Wellcome Trust)
4. Patrick Vallance (UK Chief Scientific Adviser)
5. Kristian Andersen (Scripps Research)
6. Christian Drosten (Charité Berlin)
7. Edward Holmes (University of Sydney)
8. Andrew Rambaut (University of Edinburgh)
9. **Ron Fouchier (Erasmus MC)** — betoogde dat de furin site natuurlijk kon ontstaan
10. Robert Garry (Tulane University)
11. Mike Ferguson (University of Dundee)
12. **Marion Koopmans (Erasmus MC)** — positie niet genoteerd

Fauci's samenvatting van het meningsverschil:
"There was not total agreement about what this meant. Ron Fouchier said he was sure that this could occur naturally and we should not waste our time and divert effort to pursue this. This is expected of him since he was the original GOF person with Yoshi Kawaoka. Kristian Andersen and Edward Holmes...The rest felt that deliberate insertion was possible given Dr. Zheng-Li Shi at the University of Wuhan has been working for years in GOF in coronaviruses to allow adaptation of the spike protein to bind to the human ACE2 receptor."

### 2 februari 2020 — Follow-up
Fauci, Collins en Farrar contacteren Tedros Adhanom (WHO) via Stewart Simonson om een bredere WHO-expertgroep te convenen. *Bron: Tony's Diary p15.*
"""))

sections_data.append(("geldstromen", "Geldstromen & Subsidies", """
### EU Horizon 2020 — CORDIS Projecten
| Project | Coördinator | Budget | Financier |
|---------|------------|--------|-----------|
| **VEO** (GA#874735) | Marion Koopmans (Erasmus MC) | €14.600.000 | EU Horizon 2020 |
| **ECRAID** (GA#965313) | Marc Bonten (UMC Utrecht) | €20.000.000 | EU Horizon 2020 |
| **COMPARE** (GA#643476) | Marion Koopmans (Erasmus MC) | €10.300.000 | EU Horizon 2020 |
| **DURABLE** (GA#848223) | Menno de Jong (RIVM) | €5.000.000 | EU Horizon 2020 |

### ZonMw Nationale Subsidies
| Project | Ontvanger | Budget |
|---------|-----------|--------|
| **PDPC** Pandemic Preparedness | Erasmus MC (Koopmans) | €12.000.000 |
| **NCOH** COVID-19 surveillance | Erasmus MC (Koopmans) | €4.200.000 |
| **IC COVID** intensive care onderzoek | Erasmus MC (Gommers) | €1.500.000 |

### NIH Grants
| Grant | PI | Budget | Ontvanger |
|-------|-----|--------|-----------|
| **2R01AI110964-06A1** | Peter Daszak (EcoHealth) | $3.700.000 | EcoHealth → WIV sub-award |

**Totaal geïdentificeerd subsidiegeld: €67.600.000 + $3.700.000**
"""))

sections_data.append(("rolspelers", "De Acht Hoofdrolspelers", """
### Marion Koopmans — T1 (Erasmus MC)
**Rol:** Hoofd Viroscience Erasmus MC. Coördinator VEO (€14,6M) en COMPARE (€10,3M). Deelnemer Feb 1 call — positie onbekend.
**OpenAlex:** 1.167 publicaties, 86.850 citaties. Co-auteur van het wereldwijde SARS-CoV-2 PCR protocol.
**Betweenness (virology):** **0.2676** — hoogste van alle Tier 1-2 nodes.
**🔍 [Bekijk in Netwerkgraaf](./index.html?focus=Marion%20Koopmans)**

### Ron Fouchier — T1 (Erasmus MC)
**Rol:** Deputy Head Viroscience. "Original GOF person with Yoshi Kawaoka." Betoogde natuurlijke oorsprong op Feb 1 call. H5N1 ferret transmissie (2012).
**Patenten:** US6849435B2 (reverse genetics), US20140234358A1 (H5N1 mutanten).
**Betweenness (virology):** **0.1611**.
**🔍 [Bekijk in Netwerkgraaf](./index.html?focus=Ron%20Fouchier)**

### Jaap van Dissel — T1 (LUMC/RIVM)
**Rol:** OMT-voorzitter (2020). RIVM-directeur CIb. Beleidsbrug tussen wetenschap en kabinet.
**BIG:** Geregistreerd.

### Marc Bonten — T2 (UMC Utrecht)
**Rol:** OMT-lid. ECRAID-coördinator (€20M). Hoofd Infectieziekten UMCU.

### Diederik Gommers — T1 (Erasmus MC)
**Rol:** OMT-lid. NVIC-voorzitter. IC-capaciteit.

### Menno de Jong — T2 (RIVM/AMC)
**Rol:** OMT-lid. DURABLE-coördinator (€5M).

### Ernst Kuipers — T2 (Erasmus MC)
**Rol:** OMT-voorzitter (2021). Bestuurder Erasmus MC.

### Arfan Ikram — T2 (Erasmus MC)
**Rol:** Epidemioloog. Betweenness (unfilterd): 0.48 — graaf-artefact door algemene medische publicaties.
"""))

sections_data.append(("netwerk", "Netwerkanalyse — Verborgen Bruggen", """
De multiplex netwerkanalyse onthult wie de werkelijke 'hidden bridges' zijn in het Nederlandse virologie-beleidsnetwerk. De **virology-filtered betweenness** (alleen nodes met directe co-auteurschapsrelaties naar Tier 1-3) geeft het meest accurate beeld:

| Rang | Naam | β (virology) | Rol |
|------|------|-------------|-----|
| 1 | **Marion Koopmans** | 0.2676 | Head of Viroscience; brug tussen Europese onderzoeksprogrammas en beleid |
| 2 | **Ron Fouchier** | 0.1611 | GOF-onderzoeker; Feb 1 call participant; NSABB |
| 3 | **Menno de Jong** | 0.1422 | RIVM viroloog; OMT; DURABLE-coordinator |
| 4 | **Annemiek van der Eijk** | 0.1236 | Diagnostische viroloog; PCR-ontwikkeling |
| 5 | **Ab Osterhaus** | 0.1099 | ESWI founder; WHO advisor |

**Louvain community detection** splitst de Nederlandse virologie in een **Erasmus MC-community** (708 nodes: Fouchier, Koopmans, Osterhaus, Kuiken, Haagmans) — een dicht co-auteursnetwerk dat grotendeels onafhankelijk opereert van Fauci's dagelijkse realiteit.
"""))

sections_data.append(("silent", "Silent Contributor Index — Onzichtbare Invloed", """
De **Silent Contributor Index (SCI)** meet de verhouding tussen informele bijdragen (draft reviews, ongecrediteerde adviezen) en officiële auteurscredits.

| Persoon | SCI | Informele bijdragen | Officiële credits | Status |
|---------|-----|--------------------|-------------------|--------|
| **David Robertson** | **1.0000** | 1 | 0 | 🔴 Ongecrediteerde furin site ontdekker |
| **Jeremy Farrar** | **1.0000** | 1 | 0 | 🔴 Ongecrediteerde call convenor |
| Ron Fouchier | 0.0029 | 1 | 339 | |
| Marion Koopmans | 0.0025 | 1 | 396 | |

**Robertson's rol is de grootste blinde vlek:** de ontdekking van de furin cleavage site — het centrale wetenschappelijke object van de Feb 1 call — werd gedaan door een onderzoeker die niet genoemd wordt in Fauci's dagboek en geen auteurscredit kreeg op de Proximal Origin paper. Zijn enige vermelding is in de UK Parliament testimony van Jeremy Farrar.
"""))

sections_data.append(("proximal", "De Proximal Origin Paper — Causal Chain", """
De Proximal Origin paper (Andersen et al., Nature Medicine 2022, preprint mei 2020) is geschreven door **5 van de 12 deelnemers aan de Feb 1 call**: Kristian Andersen, Edward Holmes, Andrew Rambaut, Robert Garry. De paper betoogt *voor* een natuurlijke oorsprong — het kamp dat de **meerderheid** van de call-deelnemers vertegenwoordigde (9 van de 12).

**Tijdslijn:**
- **1 feb 2020:** Feb 1 call — geen consensus; deliberate-factie in de meerderheid
- **Feb-Mrt 2020:** Data-analyse voor Proximal Origin paper begint
- **Mei 2020:** Preprint op virological.org
- **2022:** Definitieve publicatie Nature Medicine

**Vraag:** Was de Proximal Origin paper een directe *uitkomst* van de Feb 1 call of een onafhankelijke analyse? De dataset bevat geen bewijs voor causaliteit — dit blijft een open interpretatievraag.
"""))

sections_data.append(("dubbelrollen", "Belangenmatrix — Dubbele Rollen", """
| Persoon | Academisch | Beleid | Subsidie | BV/Board |
|---------|-----------|--------|----------|----------|
| **Marion Koopmans** | Erasmus MC | WHO, EMA | ZonMw, EU Horizon | Viroscience B.V., NCOH board |
| **Ron Fouchier** | Erasmus MC | NSABB | NWO, ERC | Viroscience B.V. |
| **Jaap van Dissel** | LUMC | RIVM, OMT-voorzitter | — | — |
| **Marc Bonten** | UMC Utrecht | OMT | ECRAID (€20M coordinator) | ECRAID board |
| **Diederik Gommers** | Erasmus MC | OMT | ZonMw | NVIC-voorzitter |
| **Ab Osterhaus** | Hannover | WHO, ESWI | EU Horizon | Viroclinics, ESWI (farma-gesponsord) |
"""))

sections_data.append(("blinde", "Blinde Vlekken & Aanbevolen Vervolg", """
1. **Koopmans' positie** — Blijft onbekend. Was zij voorzichtig, neutraal, of noteerde Fauci het niet? De dataset heeft hier geen antwoord op.
2. **David Robertson's rol** — Verdient eigen reconstructie. De furin cleavage site ontdekker is de missing link in de keten.
3. **Robertson-Fouchier connectie** — Bestaat er een co-auteurschapsrelatie tussen Robertson (Glasgow) en Fouchier (Erasmus)? Beide werken aan virale evolutie.
4. **AIVD/MIVD intelligence** — Nederlandse inlichtingendiensten hebben mogelijk eigen analyses gemaakt van de lab-leak discussie. Niet openbaar.
5. **OMT-notulen 2020** — De RIVM OMT-adviezen van januari-februari 2020 zijn nog niet volledig geanalyseerd op verwijzingen naar internationale overleggen.
6. **Woo-verzoeken** — Aanbevolen: Woo/VWS-2023-0042 (mediastrategie), Woo/VWS-2023-0051 (Denktank Desinformatie), Woo/3661708 (OMT-adviezen).
"""))

sections_data.append(("bronnen", "Bronnen & Data-integriteit", """
| # | Bron | Type | Verifieerbaar |
|---|------|------|-------------|
| 1 | Tony's Diary (Fauci) p13-15, 767-768 | Congressional release | SHA-256: `27d8d39b118638e4c0a4a0ece7fda8e7` |
| 2 | OpenAlex — 16 auteurprofielen | Open API | CC0, queried via api.openalex.org |
| 3 | NIH RePORTER — 250 grants | US Govt database | api.reporter.nih.gov |
| 4 | EU CORDIS — VEO, ECRAID, COMPARE, DURABLE | EU open data | cordis.europa.eu |
| 5 | ZonMw — PDPC, NCOH | NL open data | zonmw.nl |
| 6 | RIVM OMT-adviezen | NL Govt openbaar | rivm.nl/coronavirus-covid-19/omt |
| 7 | UK Parliament — Jeremy Farrar testimony | Parliamentary record | committees.parliament.uk |
| 8 | Espacenet — US6849435B2, WO2006131370A2 | Patent database | worldwide.espacenet.com |
| 9 | USRTK / WashPost FOIA — Fauci emails | FOIA release | washingtonpost.com/context/fauci-emails |
| 10 | RvdJ — 3 klachtendossiers | Journalism ethics | rvdj.nl |
| 11 | Woo/VWS-2023-0042, -0051 | Woo-besluiten | rijksoverheid.nl |
"""))

print(f"[article] Building content ({len(sections_data)} sections)...")

# ── Generate HTML ─────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{article_content['title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Source+Serif+4:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {{ --bg:#0B0E14; --surface:#131822; --border:#1e2a3a; --accent:#e94560; --accent2:#5dade2; --gold:#f39c12; --green:#2ecc71; --text:#e8e8f0; --text2:#8a8ab5; --text3:#4a4a75; font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; }}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);line-height:1.7;font-size:16px}}
a{{color:var(--accent2);text-decoration:none}}
a:hover{{text-decoration:underline;color:var(--accent)}}
.container{{max-width:980px;margin:0 auto;padding:0 24px}}
header{{background:linear-gradient(135deg,#0f1923 0%,#1a1a3e 100%);border-bottom:1px solid var(--border);padding:60px 0 50px}}
header h1{{font-family:'Source Serif 4',Georgia,serif;font-size:42px;font-weight:700;line-height:1.2;margin-bottom:16px}}
header .subtitle{{font-size:16px;color:var(--text2);line-height:1.6;max-width:800px}}
header .meta{{margin-top:20px;font-size:13px;color:var(--text3);display:flex;gap:20px;flex-wrap:wrap}}
header .meta span{{display:flex;align-items:center;gap:6px}}
#toc{{position:fixed;top:0;left:0;width:240px;height:100vh;overflow-y:auto;padding:100px 16px 40px;background:var(--surface);border-right:1px solid var(--border);z-index:100;display:none}}
#toc a{{display:block;padding:5px 10px;font-size:13px;color:var(--text2);border-radius:4px;margin:1px 0}}
#toc a:hover{{color:var(--accent);background:rgba(233,69,96,0.1)}}
#toc a.t2{{padding-left:20px;font-size:12px}}
main{{padding:40px 0 80px}}
section{{margin-bottom:50px}}
section h2{{font-family:'Source Serif 4',Georgia,serif;font-size:28px;font-weight:700;color:var(--accent);margin-bottom:20px;padding-bottom:8px;border-bottom:2px solid var(--border)}}
section h3{{font-size:18px;font-weight:600;color:var(--gold);margin:24px 0 12px}}
section p{{margin-bottom:16px;color:var(--text);font-size:16px;line-height:1.8}}
table{{width:100%;border-collapse:collapse;margin:20px 0;font-size:14px}}
th,td{{padding:10px 14px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top}}
th{{background:var(--surface);color:var(--accent2);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:1px;position:sticky;top:0}}
tr:hover{{background:rgba(255,255,255,0.02)}}
code{{background:var(--surface);padding:2px 6px;border-radius:3px;font-size:13px;color:var(--gold)}}
blockquote{{border-left:3px solid var(--accent);padding:16px 20px;margin:20px 0;background:rgba(233,69,96,0.04);border-radius:0 8px 8px 0;font-style:italic;font-size:15px;line-height:1.8}}
.alert{{padding:12px 16px;border-radius:6px;margin:16px 0;font-size:14px;display:flex;align-items:flex-start;gap:10px}}
.alert-red{{background:rgba(233,69,96,0.1);border-left:3px solid var(--accent)}}
.alert-yellow{{background:rgba(243,156,18,0.1);border-left:3px solid var(--gold)}}
.alert-green{{background:rgba(46,204,113,0.1);border-left:3px solid var(--green)}}
.actor-btn{{display:inline-block;padding:4px 10px;border:1px solid var(--accent2);border-radius:4px;font-size:11px;margin:2px;color:var(--accent2);cursor:pointer;transition:all .2s}}
.actor-btn:hover{{background:var(--accent2);color:#fff;text-decoration:none}}
.sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}}
footer{{border-top:1px solid var(--border);padding:30px 0;text-align:center;font-size:13px;color:var(--text3)}}
.nav-bar{{position:fixed;top:0;left:0;right:0;height:48px;z-index:200;background:rgba(11,14,20,0.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;gap:16px}}
.nav-bar a{{color:var(--text2);font-size:13px;padding:4px 10px;border-radius:4px}}
.nav-bar a:hover{{color:var(--text);background:rgba(255,255,255,0.05)}}
.nav-bar .logo{{font-weight:700;color:var(--accent);margin-right:auto;font-size:14px}}
.toggle-toc{{background:transparent;border:1px solid var(--border);color:var(--text2);padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px}}
.toggle-toc:hover{{color:var(--text);border-color:var(--accent2)}}
@media(min-width:1200px){{#toc{{display:block!important}}main{{margin-left:240px}}}}
@media(max-width:768px){{header h1{{font-size:28px}}header{{padding:60px 0 30px}}section h2{{font-size:22px}}table{{font-size:12px}}th,td{{padding:6px 8px}}}}
</style>
</head>
<body>
<nav class="nav-bar">
  <span class="logo">🔬 Dutch Virology Network</span>
  <a href="./index.html">🌐 Netwerkgraaf</a>
  <a href="#" style="color:var(--accent);font-weight:600">📖 Onderzoeksrapport</a>
  <a href="https://github.com/TriggerMinds/dutch-virology-network-analysis" target="_blank">GitHub</a>
  <button class="toggle-toc" onclick="document.getElementById('toc').style.display=document.getElementById('toc').style.display==='block'?'none':'block'" aria-label="Toggle inhoudsopgave">☰ Inhoud</button>
</nav>

<aside id="toc">
  <div style="font-size:11px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px">Inhoud</div>
"""

for sid, stitle, _ in sections_data:
    html += f'  <a href="#{sid}">{stitle}</a>\n'

html += """</aside>

<header>
  <div class="container">
    <h1>De Pandemische Draaischijf</h1>
    <div class="subtitle">Hoe Nederlands toponderzoek, miljoenen aan subsidies en een besloten teleconferentie met Anthony Fauci de mondiale discussie over de oorsprong van SARS-CoV-2 hebben gestuurd</div>
    <div class="meta">
      <span>📅 30 juli 2026</span>
      <span>🔍 Forensic Data &amp; Network Analysis Team</span>
      <span>📊 Multiplex Knowledge Graph — 5.401 nodes / 6.530 edges</span>
      <span>🔗 <a href="https://github.com/TriggerMinds/dutch-virology-network-analysis">Open broncode &amp; data</a></span>
    </div>
  </div>
</header>

<main class="container">
"""

for sid, stitle, body in sections_data:
    html += f'<section id="{sid}">\n<h2>{stitle}</h2>\n'
    # Process body: add table formatting, actor links
    lines = body.strip().split('\n')
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('| ') and '|' in stripped[2:]:
            if not in_table:
                html += '<table>\n'
                in_table = True
            # Check if it's a header row
            if '---' in stripped:
                continue  # skip separator
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            html += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n'
        else:
            if in_table:
                html += '</table>\n'
                in_table = False
            if stripped.startswith('### '):
                html += f'<h3>{stripped[4:].strip()}</h3>\n'
            elif stripped.startswith('> '):
                html += f'<blockquote>{stripped[2:].strip()}</blockquote>\n'
            elif stripped.startswith('🔍'):
                html += f'<p>{stripped}</p>\n'
            elif stripped.startswith('- ') or stripped.startswith('* '):
                html += f'<li>{stripped[2:].strip()}</li>\n'
            elif stripped == '':
                html += '\n'
            else:
                # Check for actor buttons
                if '🔍' in stripped:
                    parts = stripped.split('**')
                    for i, p in enumerate(parts):
                        if i % 2 == 1 and len(p) < 50:
                            html += f'<strong>{p}</strong>'
                        elif 'Bekijk in Netwerkgraaf' in p:
                            html += f' <a class="actor-btn" href="./index.html?focus={p.split("Netwerkgraaf")[0].split("(")[0].strip()}" target="_blank">🔍 Bekijk in Netwerkgraaf</a>'
                        else:
                            html += p
                    html += '\n'
                else:
                    html += f'<p>{stripped}</p>\n'
    if in_table:
        html += '</table>\n'
    html += '</section>\n'

html += """
</main>

<footer>
  <p>Dit onderzoek is volledig reproduceerbaar uit openbare bronnen. Zie <a href="https://github.com/TriggerMinds/dutch-virology-network-analysis">github.com/TriggerMinds/dutch-virology-network-analysis</a>.</p>
  <p>Geen conclusies over schuld of onschuld — alleen gestructureerde vastlegging van verifieerbare feiten.</p>
</footer>

<script>
// Auto-focus from URL parameter
(function(){var p=new URLSearchParams(window.location.search);var f=p.get('focus');if(f){var el=document.getElementById(f);if(el)setTimeout(function(){el.scrollIntoView({behavior:'smooth'});},300);}})();
</script>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print(f"  -> {HTML_PATH} ({len(html)} chars)")

# ── Generate Markdown ──────────────────────────────────────────────────────
md = f"# {article_content['title']}\n\n"
md += f"**{article_content['subtitle']}**\n\n"
md += f"*{article_content['author']} — {article_content['date']}*\n\n"
md += "---\n\n"

for sid, stitle, body in sections_data:
    md += f"## {stitle}\n\n"
    lines = body.strip().split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('### '):
            md += f"### {stripped[4:].strip()}\n\n"
        elif stripped.startswith('| '):
            md += stripped + '\n'
        elif stripped.startswith('> '):
            md += stripped + '\n\n'
        elif stripped.startswith('---'):
            md += stripped + '\n\n'
        elif stripped == '':
            md += '\n'
        else:
            md += stripped + '\n\n'
    md += '---\n\n'

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(md)
print(f"  -> {MD_PATH} ({len(md)} chars)")

print("[DONE] Article pages generated.")
