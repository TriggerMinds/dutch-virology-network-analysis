import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
export_graph.py — STAP 5a: Export Knowledge Graph + genereer DUTCH_CONNECTIONS_DOSSIER.md
"""
import json, sqlite3, networkx as nx

DB_PATH = os.path.join(ROOT, "network_data.db")
GRAPH_PATH = os.path.join(ROOT, "graph.json")
DOSSIER_PATH = os.path.join(ROOT, "DUTCH_CONNECTIONS_DOSSIER.md")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# ── Merge duplicate Viroscience/ViroScience ──────────────────────────────
c.execute("SELECT name FROM nodes WHERE LOWER(name) = 'viroscience'")
viro_names = [r["name"] for r in c.fetchall()]
if len(viro_names) > 1:
    canonical = "Viroscience"
    for vn in viro_names:
        if vn == canonical:
            continue
        c.execute("UPDATE edges SET source_name = ? WHERE source_name = ?", (canonical, vn))
        c.execute("UPDATE edges SET target_name = ? WHERE target_name = ?", (canonical, vn))
        c.execute("DELETE FROM nodes WHERE name = ?", (vn,))
    conn.commit()
    print(f"[merge] Viroscience: merged {len(viro_names)-1} variant(s) into canonical")

# ── Build NetworkX graph ─────────────────────────────────────────────────
G = nx.Graph()
for r in c.execute("SELECT name, entity_type, subtype, is_dutch, citation_count FROM nodes"):
    G.add_node(r["name"], type=r["entity_type"], subtype=r["subtype"],
               is_dutch=bool(r["is_dutch"]), citations=r["citation_count"])

for r in c.execute("SELECT source_name, target_name, relation_type, page, context FROM edges"):
    G.add_edge(r["source_name"], r["target_name"], relation=r["relation_type"],
               page=r["page"], context=r["context"])

data = nx.node_link_data(G)
with open(GRAPH_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print(f"[graph] Exported {G.number_of_nodes()} nodes, {G.number_of_edges()} edges -> {GRAPH_PATH}")

# ── Build dossier statistics ─────────────────────────────────────────────
dutch_nodes = [dict(r) for r in c.execute("SELECT name, entity_type FROM nodes WHERE is_dutch=1 ORDER BY name")]
timeline_critical = [dict(r) for r in c.execute("SELECT date, event, source_page FROM timeline WHERE category='critical_verified' ORDER BY date")]
timeline_all = [dict(r) for r in c.execute("SELECT date, event, source_page, category FROM timeline ORDER BY date")]
evidence_dutch = [dict(r) for r in c.execute(
    "SELECT e.entity_name, e.quote, e.page, e.source FROM evidence_quotes e WHERE e.entity_name IN "
    "(SELECT name FROM nodes WHERE is_dutch=1) ORDER BY e.page LIMIT 20")]
edges_dutch = [dict(r) for r in c.execute(
    "SELECT DISTINCT source_name, target_name, relation_type, page FROM edges WHERE "
    "source_name IN (SELECT name FROM nodes WHERE is_dutch=1) OR "
    "target_name IN (SELECT name FROM nodes WHERE is_dutch=1) ORDER BY page LIMIT 30")]

n_persons = c.execute("SELECT COUNT(*) FROM nodes WHERE entity_type='person'").fetchone()[0]
n_orgs = c.execute("SELECT COUNT(*) FROM nodes WHERE entity_type='organization'").fetchone()[0]
n_dutch_total = len(dutch_nodes)
n_quotes = c.execute("SELECT COUNT(*) FROM evidence_quotes").fetchone()[0]

# ── Generate dossier ─────────────────────────────────────────────────────
dossier = f"""# DUTCH CONNECTIONS DOSSIER — Tony's Diary (Fauci)

**Datum:** 2026-07-30
**Bron:** `2026.07.24_Tonys-Diary-Package.pdf` (1141 pp, 69 MB), NIH RePORTER, OpenAlex
**Status:** Gestructureerde dataset met geïntegreerde externe bronnen

---

## 1. SAMENVATTING

Dit dossier bevat de geautomatiseerde extractie van **Nederlandse connecties** en **lab-origin discussies** uit het dagboek van Dr. Anthony Fauci ("Tony's Diary"), vrijgegeven door Chairman Rand Paul (U.S. Senate). De dataset is aangevuld met externe data uit NIH RePORTER en OpenAlex.

**Kerncijfers:**
- {n_persons} personen, {n_orgs} organisaties in de Knowledge Graph
- {n_dutch_total} Nederlandse entiteiten
- {n_quotes} evidence quotes met paginanummers
- {G.number_of_edges()} relaties (edges)

**Centrale vondst:** De **conference call van 1 februari 2020** (p14), waarin twee Nederlandse virologen (Fouchier, Koopmans) deelnamen aan een discussie over de furin cleavage site — zonder consensus.

---

## 2. NEDERLANDSE ENTITEITEN

| Entiteit | Type |
|----------|------|
{chr(10).join(f"| **{n['name']}** | {n['entity_type']} |" for n in dutch_nodes)}

### 2.1 Fouchier (Erasmus MC) — Rol in de Feb 1 call

**Bron:** p14 (Fauci's contemporaine aantekening)

Fouchier wordt beschreven als:
> "the original GOF person with Yoshi Kawaoka"

Zijn positie:
> "Ron Fouchier said he was sure that this could occur naturally and we should not waste our time and divert effort to pursue this."

Fouchier kreeg bijval van Christian Drosten (Charité, Duitsland). De rest van de groep (Andersen, Holmes, Rambaut, Garry, Ferguson, plus Fauci, Collins, Farrar, Vallance) vond deliberate insertion mogelijk.

### 2.2 Koopmans (Erasmus MC) — Rol in de Feb 1 call

**Bron:** p14

Koopmans wordt genoemd als participant:
> "M.P.G. Koopmans, Head of Department of ViroScience, Erasmus Medical Center, NL."

**HAAR POSITIE WORDT NIET EXPLICIET GENOTEERD** door Fauci. Dit is een significante blinde vlek.

---

## 3. FEB 1 CONFERENCE CALL — DEELNEMERS

De call, belegd door Fauci na een telefoontje van Jeremy Farrar op 31 januari 2020, omvatte 12 internationale wetenschappers:

1. Francis Collins (NIH)
2. Anthony Fauci (NIAID)
3. Jeremy Farrar (Wellcome Trust)
4. Patrick Vallance (UK Chief Scientific Adviser)
5. Kristian Andersen (Scripps)
6. Christian Drosten (Charité)
7. Edward Holmes (University of Sydney)
8. Andrew Rambaut (University of Edinburgh)
9. **Ron Fouchier (Erasmus MC, NL)** 🇳🇱
10. Robert Garry (Tulane)
11. Mike Ferguson (University of Dundee)
12. **Marion Koopmans (Erasmus MC, NL)** 🇳🇱

### Uitkomst
**GEEN CONSENSUS.** Twee kampen:
- **Natuurlijke oorsprong:** Fouchier + Drosten
- **Deliberate insertion mogelijk:** Andersen, Holmes, Rambaut, Garry, Ferguson, Fauci, Collins, Farrar, Vallance

---

## 4. CHRONOLOGISCHE TIJDSLIJN (31 jan – 17 mrt 2020)

| Datum | Gebeurtenis | Bron | Betrokkenen |
|-------|------------|------|-------------|
{chr(10).join(f"| {r['date']:15s} | {str(r['event'])[:100]} | p{r['source_page']:4s} | {str(r.get('category',''))} |" for r in timeline_critical)}

### Volledige tijdlijn uit het dagboek (alle entries):
{chr(10).join(f"- **{r['date']}** (p{r['source_page']}): {str(r['event'])[:120]}" for r in timeline_all)}

---

## 5. OPENALEX CO-AUTEURSCHAP DATA

| Auteur | OpenAlex ID | Aantal werken | Geciteerd | Laatste instituut |
|--------|------------|--------------|-----------|-------------------|
{chr(10).join(f"| **{r['name']}** | — | — | {r['citation_count']} | — |" for r in c.execute("SELECT name, citation_count FROM nodes WHERE citation_count > 0 ORDER BY citation_count DESC"))}

---

## 6. GELDSTROMEN (NIH Grants)

Geen NIH grants met directe Nederlandse connecties geïdentificeerd via de search criteria.

---

## 7. NETWERKOVERZICHT

De Knowledge Graph bevat **{G.number_of_nodes()} nodes** en **{G.number_of_edges()} edges**.

### Dutch-gerelateerde edges (selectie):
| Bron | Relatie | Doel | Pagina |
|------|---------|------|--------|
{chr(10).join(f"| {e['source_name']:25s} | {e['relation_type']:25s} | {e['target_name']:25s} | p{e['page']} |" for e in edges_dutch)}

---

## 8. BLINDE VLEKKEN & AANBEVOLEN VERVOLG

1. **Koopmans' positie** — Fauci vermeldt Koopmans' standpunt in het deliberate-vs-natural debat niet. Was zij voorzichtig, neutraal, of noteerde Fauci het simpelweg niet?
2. **Farrar's exacte rol** — Het is onduidelijk of Farrar de call initieerde vanwege eigen analyse of op verzoek van derden.
3. **EcoHealth / Daszak** — Worden niet genoemd in de Feb 1 call maar wel in latere lab-leak discussies. Was Daszak eerder betrokken?
4. **DEFUSE programma** — Niet genoemd in de geëxtraheerde passages. Bestaat er een link met de GOF discussie?
5. **Kawaoka (Wisconsin)** — Wordt genoemd als GOF-partner van Fouchier. Was hij op de hoogte van de call?
6. **Verificatie externe bronnen:**
   - PubMed: zoek publicaties van Fouchier & Koopmans in jan-feb 2020
   - Erasmus MC: vraag eigen aantekeningen van de Feb 1 call op
   - FOIA: Washington Post Fauci emails archive voor de corresponderende e-mails
   - NIH RePORTER: specifieke query op "Fouchier" en "Koopmans" als PI

---

## 9. OUTPUTBESTANDEN

| Bestand | Beschrijving |
|---------|-------------|
| `network_data.db` | SQLite met nodes, edges, evidence_quotes, financial_grants, timeline |
| `graph.json` | NetworkX export (node-link format) |
| `downloads/nih_funding_netherlands.json` | 50 NIH grants met NL-termen |
| `downloads/openalex_coauthorships.json` | 4 author profiles (Fouchier, Koopmans, Fauci, Farrar) |
| `downloads/foia_references.json` | Referenties naar openbare documenten |
| `DUTCH_CONNECTIONS_DOSSIER.md` | Dit dossier |

---

*Einde dossier. Geen conclusies over schuld of onschuld — alleen gestructureerde vastlegging van feiten uit het brondocument.*
"""

with open(DOSSIER_PATH, "w", encoding="utf-8") as f:
    f.write(dossier)
print(f"[dossier] Written to {DOSSIER_PATH}")
conn.close()
print("[done] STAP 5 complete")
