import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
export_multiplex.py — STAP 5: Export multiplex graph + generate master dossier.
"""
import json, os, sqlite3, networkx as nx
from collections import defaultdict

DB_PATH = os.path.join(ROOT, "data", "network_data.db")
GRAPH_PATH = os.path.join(ROOT, "data", "graph.json")
DOSSIER_PATH = os.path.join(ROOT, "docs", "DUTCH_CONNECTIONS_DOSSIER.md")
CENTRALITY_PATH = os.path.join(ROOT, "data", "centrality_results.json")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# ── TIER DEFINITIES (for reference in group extraction) ─────────────────
TIERS = {
    "Ron Fouchier": 1, "Marion Koopmans": 1, "Ab Osterhaus": 1, "Thijs Kuiken": 1, "Bart Haagmans": 1,
    "Jaap van Dissel": 1, "Diederik Gommers": 1, "Jan Kluytmans": 1,
    "Aura Timen": 2, "Menno de Jong": 2, "Marc Bonten": 2, "Annemiek van der Eijk": 2, "Massimo Palmarini": 2,
    "Arfan Ikram": 2, "Ernst Kuipers": 2,
    "Maarten Keulemans": 3
}
GLOBAL_NODES = ["Anthony Fauci", "Francis Collins", "Jeremy Farrar", "Kristian Andersen", "Edward Holmes", "Andrew Rambaut", "Christian Drosten", "Robert Garry"]

# ── Build complete NetworkX MultiGraph ───────────────────────────────────
G = nx.MultiGraph()
for r in c.execute("SELECT name, entity_type, tier, organization, primary_role FROM nodes"):
    G.add_node(r["name"], type=r["entity_type"], tier=r["tier"],
               org=r["organization"], role=r["primary_role"])

for r in c.execute("""SELECT n1.name AS s, n2.name AS t, e.layer_type, e.date, e.description, e.weight
                      FROM edges e JOIN nodes n1 ON e.source_id=n1.id
                      JOIN nodes n2 ON e.target_id=n2.id"""):
    G.add_edge(r["s"], r["t"], layer=r["layer_type"], date=r["date"], desc=r["description"], weight=r["weight"] or 1)

data = nx.node_link_data(G)
with open(GRAPH_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print(f"[graph] {G.number_of_nodes()} nodes, {G.number_of_edges()} edges -> {GRAPH_PATH}")

# ── Load centrality results ──────────────────────────────────────────────
centrality = {}
if os.path.exists(CENTRALITY_PATH):
    with open(CENTRALITY_PATH, "r", encoding="utf-8") as f:
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
if "ALL_full" in centrality:
    for node in centrality["ALL_full"].get("betweenness_top", []):
        r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (node["node"],)).fetchone()
        all_between.append({
            "name": node["node"],
            "score": node["score"],
            "tier": r["tier"] if r else 0,
            "org": r["organization"] if r else ""
        })

coauthor_between = []
if "CO_AUTHOR_full" in centrality:
    for node in centrality["CO_AUTHOR_full"].get("betweenness_top", []):
        r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (node["node"],)).fetchone()
        coauthor_between.append({
            "name": node["node"],
            "score": node["score"],
            "tier": r["tier"] if r else 0,
            "org": r["organization"] if r else ""
        })

# ── Dynamic Community Resolution ──────────────────────────────────────────
communities = defaultdict(list)
all_full_partition = centrality.get("ALL_full", {}).get("partition", {})
for node, comm_id in all_full_partition.items():
    communities[comm_id].append(node)

# Find which community the core Dutch virologists belong to
dutch_core = ["Ron Fouchier", "Marion Koopmans", "Ab Osterhaus", "Thijs Kuiken", "Bart Haagmans"]
dutch_comm_id = None
max_intersection = 0
for comm_id, members in communities.items():
    intersect_len = len(set(dutch_core).intersection(members))
    if intersect_len > max_intersection:
        max_intersection = intersect_len
        dutch_comm_id = comm_id

dutch_comm_size = len(communities[dutch_comm_id]) if dutch_comm_id is not None else 0
dutch_comm_members = [m for m in communities[dutch_comm_id] if m in TIERS] if dutch_comm_id is not None else []
dutch_comm_members_str = ", ".join(sorted(dutch_comm_members))

# Sort other communities by size
other_comms = []
for comm_id, members in sorted(communities.items(), key=lambda x: -len(x[1])):
    if comm_id == dutch_comm_id:
        continue
    key_members = [m for m in members if m in TIERS or m in GLOBAL_NODES]
    key_members_str = ", ".join(sorted(key_members)[:5])
    other_comms.append({
        "id": comm_id,
        "size": len(members),
        "key_members": key_members_str if key_members_str else "overige co-auteurs"
    })

# Dynamic Policy splitsing resolution
policy_partition = centrality.get("POLICY_ADVISORY_full", {}).get("partition", {})
if not policy_partition:
    policy_partition = centrality.get("POLICY_ADVISORY_virology", {}).get("partition", {})

policy_comms = defaultdict(list)
for node, comm_id in policy_partition.items():
    policy_comms[comm_id].append(node)

policy_comm_rows = []
for comm_id, members in sorted(policy_comms.items(), key=lambda x: -len(x[1])):
    members_str = ", ".join(sorted(members))
    policy_comm_rows.append(f"{comm_id + 1}. **Community {comm_id}** ({len(members)} leden): {members_str}")
policy_comm_str = "\n".join(policy_comm_rows)

# Check which community Koopmans is in (for policy split discussion)
koopmans_policy_comm = policy_partition.get("Marion Koopmans", "?")
fouchier_policy_comm = policy_partition.get("Ron Fouchier", "?")

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
| CO_AUTHOR | {len([n for n in G.nodes() if any(G.get_edge_data(n, n2, key).get('layer')=='CO_AUTHOR' for n2 in G.neighbors(n) for key in G.get_edge_data(n, n2))]) or 'n/a'} | {coauthor_edges} | Wetenschappelijke publicaties en co-auteurschappen |
| POLICY_ADVISORY | {len([n for n in G.nodes() if any(G.get_edge_data(n, n2, key).get('layer')=='POLICY_ADVISORY' for n2 in G.neighbors(n) for key in G.get_edge_data(n, n2))]) or 'n/a'} | {policy_edges} | Beleidsadvisering: Feb 1 call, OMT, WHO |
| MEDIA_NARRATIVE | {len([n for n in G.nodes() if any(G.get_edge_data(n, n2, key).get('layer')=='MEDIA_NARRATIVE' for n2 in G.neighbors(n) for key in G.get_edge_data(n, n2))]) or 'n/a'} | {media_edges} | Mediaverslaggeving: journalisten, publicaties |

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
{chr(10).join(f"| **{n['node']}** | {n['score']:.4f} | Feb 1 call participant / policy position |" for n in centrality.get("POLICY_ADVISORY_full", {}).get("betweenness_top", [])[:8])}

**Conclusie:** De Feb 1 Conference Call is veruit de belangrijkste brug in de policy-laag. Fouchier en Drosten zijn belangrijke individuele bruggen — beide als vertegenwoordigers van de Natural Origin-positie.

---

## 3. COMMUNITY DETECTIE (LOUVAIN)

### 3.1 Co-auteur community met Erasmus MC-kern

Het **Leiden/Louvain-algoritme** detecteert een aparte community (Community {dutch_comm_id}) bestaande uit:
- **Core Tiers:** {dutch_comm_members_str}
- **Grootte:** {dutch_comm_size} nodes (in CO_AUTHOR laag)

**Dit is de Erasmus MC / Nederlandse virologie-community.** Al deze personen publiceren regelmatig samen en delen een co-auteurs netwerk van ~{dutch_comm_size} onderzoekers.

### 3.2 Andere communities

| Community | Grootte | Kernleden |
|-----------|---------|-----------|
{chr(10).join(f"| Community {c['id']} | {c['size']} | {c['key_members']} |" for c in other_comms[:5])}

### 3.3 Policy-community splitsing

In de POLICY_ADVISORY laag detecteert Louvain de volgende communities:
{policy_comm_str}

**Koopmans zit in Community {koopmans_policy_comm}** (samen met de deliberate-fractie) — dit is een voorzichtige indicatie dat zij mogelijk nader stond tot de deliberate-positie dan Fouchier (die in Community {fouchier_policy_comm} zit), maar dit is **geen bewijs**; alleen een netwerktoewijzing op basis van met wie ze in dezelfde policy-edges zit.

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
conn.close()
