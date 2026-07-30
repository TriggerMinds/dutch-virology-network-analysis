"""
export_multiplex.py — STAP 5: Export multiplex graph + generate master dossier.
"""
import json, os, sqlite3, networkx as nx
from collections import defaultdict

DB_PATH = r"C:\Users\gewoo\Desktop\New folder (4)\data\network_data.db"
GRAPH_PATH = r"C:\Users\gewoo\Desktop\New folder (4)\data\graph.json"
DOSSIER_PATH = r"C:\Users\gewoo\Desktop\New folder (4)\docs\DUTCH_CONNECTIONS_DOSSIER.md"
CENTRALITY_PATH = r"C:\Users\gewoo\Desktop\New folder (4)\data\centrality_results.json"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# ── Build complete NetworkX graph ────────────────────────────────────────
G = nx.Graph()
for r in c.execute("SELECT name, entity_type, tier, organization, primary_role FROM nodes"):
    G.add_node(r["name"], type=r["entity_type"], tier=r["tier"],
               org=r["organization"], role=r["primary_role"])

for r in c.execute("""SELECT n1.name AS s, n2.name AS t, e.layer_type, e.date, e.description
                      FROM edges e JOIN nodes n1 ON e.source_id=n1.id
                      JOIN nodes n2 ON e.target_id=n2.id"""):
    G.add_edge(r["s"], r["t"], layer=r["layer_type"], date=r["date"], desc=r["description"])

data = nx.node_link_data(G)
with open(GRAPH_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print(f"[graph] {G.number_of_nodes()} nodes, {G.number_of_edges()} edges -> {GRAPH_PATH}")

# ── Load centrality results ──────────────────────────────────────────────
centrality = {}
if os.path.exists(CENTRALITY_PATH):
    with open(CENTRALITY_PATH, "r") as f:
        centrality = json.load(f)

# ── Gather statistics ────────────────────────────────────────────────────
n_nodes = G.number_of_nodes()
n_edges = G.number_of_edges()
tier1_nodes = [r["name"] for r in c.execute("SELECT name FROM nodes WHERE tier=1 ORDER BY name")]
tier2_nodes = [r["name"] for r in c.execute("SELECT name FROM nodes WHERE tier=2 ORDER BY name")]
tier3_nodes = [r["name"] for r in c.execute("SELECT name FROM nodes WHERE tier=3 ORDER BY name")]
consortia = [r["name"] for r in c.execute("SELECT name FROM nodes WHERE entity_type='consortium' ORDER BY name")]
coauthor_edges = c.execute("SELECT COUNT(*) FROM edges WHERE layer_type='CO_AUTHOR'").fetchone()[0]
policy_edges = c.execute("SELECT COUNT(*) FROM edges WHERE layer_type='POLICY_ADVISORY'").fetchone()[0]
media_edges = c.execute("SELECT COUNT(*) FROM edges WHERE layer_type='MEDIA_NARRATIVE'").fetchone()[0]
n_timeline = c.execute("SELECT COUNT(*) FROM timeline").fetchone()[0]
timeline_entries = [dict(r) for r in c.execute("SELECT * FROM timeline ORDER BY date LIMIT 20")]

# Extract top betweenness
all_between = []
if "ALL" in centrality:
    for node in centrality["ALL"]["betweenness_top"]:
        r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (node["node"],)).fetchone()
        all_between.append({
            "name": node["node"],
            "score": node["score"],
            "tier": r["tier"] if r else 0,
            "org": r["organization"] if r else ""
        })

coauthor_between = []
if "CO_AUTHOR" in centrality:
    for node in centrality["CO_AUTHOR"]["betweenness_top"]:
        r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (node["node"],)).fetchone()
        coauthor_between.append({
            "name": node["node"],
            "score": node["score"],
            "tier": r["tier"] if r else 0,
            "org": r["organization"] if r else ""
        })

# ── Generate dossier ─────────────────────────────────────────────────────
dossier = f"""# DUTCH CONNECTIONS DOSSIER — Multiplex Knowledge Graph

**Datum:** 2026-07-30
**Bronnen:** Tony's Diary (Fauci, 1141pp), OpenAlex, NIH RePORTER
**Gelaagde netwerkanalyse:** CO_AUTHOR | POLICY_ADVISORY | MEDIA_NARRATIVE

---

## 1. SAMENVATTING

Dit dossier beschrijft de **multiplex Knowledge Graph** van het Nederlandse virologienetwerk in relatie tot de COVID-19 lab-origin discussie. De graaf bevat **{n_nodes} nodes** en **{n_edges} edges** verdeeld over drie lagen.

### Laagoverzicht

| Laag | Nodes | Edges | Beschrijving |
|------|-------|-------|-------------|
| CO_AUTHOR | {len([n for n in G.nodes() if any(e[2].get('layer')=='CO_AUTHOR' for e in G.edges(n, data=True))]) or 'n/a'} | {coauthor_edges} | Wetenschappelijke publicaties en co-auteurschappen |
| POLICY_ADVISORY | {len([n for n in G.nodes() if any(e[2].get('layer')=='POLICY_ADVISORY' for e in G.edges(n, data=True))]) or 'n/a'} | {policy_edges} | Beleidsadvisering: Feb 1 call, OMT, WHO |
| MEDIA_NARRATIVE | {len([n for n in G.nodes() if any(e[2].get('layer')=='MEDIA_NARRATIVE' for e in G.edges(n, data=True))]) or 'n/a'} | {media_edges} | Mediaverslaggeving: journalisten, publicaties |

### Tier-indeling

| Tier | Type | Aantal | Personen |
|------|------|--------|---------|
| 1 | Directe kern (virologen) | {len(tier1_nodes)} | {', '.join(tier1_nodes)} |
| 2 | Institutionele bruggen | {len(tier2_nodes)} | {', '.join(tier2_nodes)} |
| 3 | Media & narrative | {len(tier3_nodes)} | {', '.join(tier3_nodes)} |

### Consortia in de graaf
{chr(10).join(f'- **{c}**' for c in consortia)}

---

## 2. CENTRALITEITSANALYSE

### 2.1 Betweenness Centrality (ALLE lagen) — "Verborgen bruggen"

{chr(10).join(f"{i+1}. **{b['name']}** (Tier {b['tier']}, {b['org']}) — betweenness = {b['score']:.4f}" for i, b in enumerate(all_between[:10]))}

**Interpretatie:** Hoge betweenness = entiteit die als brug fungeert tussen anders gescheiden delen van het netwerk.

### 2.2 Betweenness Centrality — CO_AUTHOR laag

{chr(10).join(f"{i+1}. **{b['name']}** (Tier {b['tier']}, {b['org']}) — betweenness = {b['score']:.4f}" for i, b in enumerate(coauthor_between[:10]))}

### 2.3 Betweenness Centrality — POLICY_ADVISORY laag

| Entiteit | Betweenness | Rol |
|----------|------------|-----|
{chr(10).join(f"| **{n['name']}** | {n['score']:.4f} | Feb 1 call participant / policy position |" for n in centrality.get("POLICY_ADVISORY", {}).get("betweenness_top", [])[:8])}

**Conclusie:** De Feb 1 Conference Call is veruit de belangrijkste brug in de policy-laag (β=0.6970). Fouchier (β=0.0758) en Drosten (β=0.0758) zijn de belangrijkste individuele bruggen — beide als vertegenwoordigers van de Natural Origin-positie.

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
| Community 9 | 1256 | Arfan Ikram (Tier 2) | Erasmus MC epidemiologie — grootste community |
| Community 6 | 1077 | Menno de Jong, Marc Bonten | RIVM/UMC Utrecht — beleidsnabij |
| Community 7 | 755 | Massimo Palmarini (Tier 2) | Glasgow — internationale virologie |
| Community 8 | 508 | Ernst Kuipers (Tier 2) | Erasmus MC — klinisch/policy |

### 3.3 Policy-community splitsing

In de POLICY_ADVISORY laag detecteert Louvain **2 communities**:
1. **Community 1** (10 leden): Fauci, Collins, Farrar, Andersen, Holmes, Rambaut + Koopmans — de "Deliberate insertion mogelijk" fractie
2. **Community 0** (3 leden): Fouchier, Drosten + Natural Origin Hypothesis — de "Natuurlijke oorsprong" fractie

**Koopmans zit in Community 1** (samen met de deliberate-fractie) — dit is een voorzichtige indicatie dat zij mogelijk nader stond tot de deliberate-positie dan tot Fouchier, maar dit is **geen bewijs**; alleen een netwerktoewijzing op basis van met wie ze in dezelfde policy-edges zit.

---

## 4. CHRONOLOGISCHE TIJDSLIJN

| Datum | Type | Gebeurtenis | Actoren |
|-------|------|------------|--------|
{chr(10).join(f"| {t.get('date','')} | {t.get('event_type','')} | {str(t.get('description',''))[:100]} | {str(t.get('actors_involved',''))[:80]} |" for t in timeline_entries)}

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

## 10. OUTPUTBESTANDEN

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
"""

with open(DOSSIER_PATH, "w", encoding="utf-8") as f:
    f.write(dossier)
print(f"[dossier] Written to {DOSSIER_PATH}")
print("[done] STAP 5 complete")
