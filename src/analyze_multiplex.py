"""
analyze_multiplex.py -- STAP 4 (audit-fixed): Netwerkanalyse met virologie-topic filtering.
Centraliteit wordt berekend:
  (a) over ALLE nodes (algemeen)
  (b) over VIROLOGY-FILTERED nodes (alleen personen/orgs met infectieziekte-relevantie)
  (c) per laag (CO_AUTHOR, POLICY_ADVISORY, MEDIA_NARRATIVE) -- gesplitst.
"""
import json, sqlite3, networkx as nx
from collections import defaultdict

DB_PATH = r"C:\Users\gewoo\Desktop\New folder (4)\data\network_data.db"
OUT_STATS = r"C:\Users\gewoo\Desktop\New folder (4)\data\centrality_results.json"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# ── Virology-relevant persons (Tier 1-3 + international virologists) ────
VIROLOGY_NAMES = set()
for r in c.execute("SELECT name FROM nodes WHERE tier IN (1,2,3)"):
    VIROLOGY_NAMES.add(r["name"])
# Add Feb 1 call participants and key policy nodes
for name in ["Anthony Fauci", "Francis Collins", "Jeremy Farrar", "Kristian Andersen",
             "Edward Holmes", "Andrew Rambaut", "Christian Drosten", "Robert Garry",
             "Patrick Vallance", "Mike Ferguson", "Shi Zhengli", "Yoshi Kawaoka",
             "Peter Daszak", "Feb 1 Conference Call", "Deliberate Insertion Hypothesis",
             "Natural Origin Hypothesis", "Proximal Origin Paper"]:
    VIROLOGY_NAMES.add(name)

# ── Build graphs ─────────────────────────────────────────────────────────
layers = ["CO_AUTHOR", "POLICY_ADVISORY", "MEDIA_NARRATIVE", "CONSORTIUM_FUNDING"]

def build_graph(layer=None):
    G = nx.Graph()
    query = """SELECT n1.name AS s, n2.name AS t, e.layer_type, e.date, e.description
               FROM edges e JOIN nodes n1 ON e.source_id=n1.id JOIN nodes n2 ON e.target_id=n2.id"""
    if layer:
        query += f" WHERE e.layer_type='{layer}'"
    for r in conn.execute(query):
        G.add_edge(r["s"], r["t"], layer=r["layer_type"], date=r["date"], desc=r["description"])
    return G

all_G = build_graph()
layer_graphs = {l: build_graph(l) for l in layers}

# ── Virology-filtered graph ──────────────────────────────────────────────
def filter_virology(G):
    """Keep only virology-core nodes: Tier 1-3 persons + their direct policy/event context.
    This removes general medical researchers (e.g., Arfan Ikram's non-virology co-authors)."""
    tier_nodes = set()
    for r in conn.execute("SELECT name FROM nodes WHERE tier IN (1,2,3)"):
        tier_nodes.add(r["name"])
    # Also include key policy/event/position nodes
    for name in ["Anthony Fauci", "Francis Collins", "Jeremy Farrar", "Kristian Andersen",
                 "Edward Holmes", "Andrew Rambaut", "Christian Drosten", "Robert Garry",
                 "Patrick Vallance", "Mike Ferguson", "Shi Zhengli", "Yoshi Kawaoka",
                 "Peter Daszak", "Feb 1 Conference Call", "Deliberate Insertion Hypothesis",
                 "Natural Origin Hypothesis", "Proximal Origin Paper", "EcoHealth Alliance",
                 "Wuhan Institute of Virology", "Wellcome Trust", "NIAID", "NIH", "WHO"]:
        tier_nodes.add(name)
    # Keep: Tier nodes + their direct co-authors who are also virology-linked
    # (connected via CO_AUTHOR to at least 2 different Tier 1-2 nodes)
    existing_tier = [n for n in tier_nodes if G.has_node(n)]
    keep = set(existing_tier)
    for n in existing_tier:
        for neighbor in G.neighbors(n):
            # Always keep policy/event nodes
            e_data = G.get_edge_data(n, neighbor)
            if e_data and e_data.get("layer") in ("POLICY_ADVISORY", "MEDIA_NARRATIVE", "CONSORTIUM_FUNDING"):
                keep.add(neighbor)
            # Keep co-authors linked to multiple Tier nodes
            elif e_data and e_data.get("layer") == "CO_AUTHOR":
                # Count links to different Tier nodes
                t_count = sum(1 for tn in existing_tier if tn != n and G.has_edge(tn, neighbor))
                if t_count >= 2:
                    keep.add(neighbor)
    H = G.subgraph(keep).copy()
    return H

all_viro_G = filter_virology(all_G)
layer_viro_G = {}
for l, G in layer_graphs.items():
    if G.number_of_nodes() > 0:
        layer_viro_G[l] = filter_virology(G)
    else:
        layer_viro_G[l] = G

print("=" * 60)
print("MULTIPLEX NETWERKANALYSE (AUDIT-FIXED)")
print("=" * 60)

print(f"\n  Full graph:               {all_G.number_of_nodes():6d} nodes, {all_G.number_of_edges():6d} edges")
print(f"  Virology-filtered:        {all_viro_G.number_of_nodes():6d} nodes, {all_viro_G.number_of_edges():6d} edges")
for l in layers:
    print(f"  {l:25s}: full={layer_graphs[l].number_of_nodes():5d}n/{layer_graphs[l].number_of_edges():5d}e  "
          f"viro={layer_viro_G[l].number_of_nodes():5d}n/{layer_viro_G[l].number_of_edges():5d}e")

# ── Centrality computation ────────────────────────────────────────────────
def compute_centrality(G_label, G):
    if G.number_of_nodes() < 3:
        return {}
    bc = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
    dc = nx.degree_centrality(G)
    ec = {}
    try:
        comps = [G.subgraph(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
        if comps and comps[0].number_of_nodes() > 1:
            ec = nx.eigenvector_centrality_numpy(comps[0], max_iter=1000)
    except:
        pass
    return {"betweenness": bc, "degree": dc, "eigenvector": ec}

results = {}
for label, G in [("ALL_full", all_G), ("ALL_virology", all_viro_G)]:
    results[label] = compute_centrality(label, G)
    bc = results[label].get("betweenness", {})
    if bc:
        print(f"\n  [{label}] Top-10 Betweenness:")
        for n, s in sorted(bc.items(), key=lambda x: -x[1])[:10]:
            r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (n,)).fetchone()
            tier = r["tier"] if r else "?"
            org = (r["organization"] or "?")[:30] if r else "?"
            print(f"    between={s:.4f}  T{tier} {n:35s} {org}")

# Per-layer centrality
for l in layers:
    for variant, G_l in [("full", layer_graphs[l]), ("virology", layer_viro_G[l])]:
        label = f"{l}_{variant}"
        results[label] = compute_centrality(label, G_l)

# ── Save ─────────────────────────────────────────────────────────────────
with open(OUT_STATS, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"\n  Saved to {OUT_STATS}")

# ── Viro-specific summary ────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"VIROLOGY-FILTERED TOP-10 (PRIMARY FINDING)")
print(f"{'='*50}")
bc_v = results.get("ALL_virology", {}).get("betweenness", {})
if bc_v:
    print(f"\n  (Filtered: alleen nodes met connectie naar Tier 1-3 virologen)")
    for i, (n, s) in enumerate(sorted(bc_v.items(), key=lambda x: -x[1])[:10], 1):
        r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (n,)).fetchone()
        tier = r["tier"] if r else "?"
        org = (r["organization"] or "?")[:30] if r else "?"
        print(f"  {i:2d}. between={s:.4f}  T{tier} {n:35s} {org}")

print("\n[DONE]")
conn.close()
