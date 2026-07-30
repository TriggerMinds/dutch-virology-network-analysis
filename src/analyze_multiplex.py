"""
analyze_multiplex.py -- STAP 4 (audit-fixed): Netwerkanalyse met virologie-topic filtering en dynamische Louvain clustering.
"""
import os
import json
import sqlite3
import networkx as nx
import community as community_louvain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")
OUT_STATS = os.path.join(ROOT, "data", "centrality_results.json")

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
    G = nx.MultiGraph()  # MultiGraph to preserve parallel edges
    query = """SELECT n1.name AS s, n2.name AS t, e.layer_type, e.date, e.description, e.weight
               FROM edges e JOIN nodes n1 ON e.source_id=n1.id JOIN nodes n2 ON e.target_id=n2.id"""
    if layer:
        query += f" WHERE e.layer_type='{layer}'"
    for r in conn.execute(query):
        w = r["weight"]
        if isinstance(w, str): w = 1
        try: w = int(w)
        except: w = 1
        G.add_edge(r["s"], r["t"], layer=r["layer_type"], date=r["date"], desc=r["description"], weight=w)
    return G

all_G = build_graph()
layer_graphs = {l: build_graph(l) for l in layers}

# Helper to project MultiGraph to simple weighted Graph
def to_weighted_simple_graph(MG):
    G = nx.Graph()
    for u, v, data in MG.edges(data=True):
        weight = data.get("weight", 1)
        if isinstance(weight, str): weight = 1
        try: weight = int(weight)
        except: weight = 1
        if G.has_edge(u, v):
            G[u][v]['weight'] += weight
        else:
            G.add_edge(u, v, weight=weight, layer=data.get("layer"), date=data.get("date"), desc=data.get("desc") or data.get("description"))
    for node, attrs in MG.nodes(data=True):
        G.add_node(node, **attrs)
    return G

# ── Virology-filtered graph ──────────────────────────────────────────────
def filter_virology(G):
    """Keep only virology-core nodes: Tier 1-3 persons + their direct policy/event context."""
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
    
    existing_tier = [n for n in tier_nodes if G.has_node(n)]
    keep = set(existing_tier)
    for n in existing_tier:
        for neighbor in G.neighbors(n):
            if isinstance(G, nx.MultiGraph):
                edges_dict = G.get_edge_data(n, neighbor) or {}
                edges_list = list(edges_dict.values())
            else:
                edges_list = [G.get_edge_data(n, neighbor)]
            
            has_policy = False
            has_coauthor = False
            for e_data in edges_list:
                if e_data:
                    if e_data.get("layer") in ("POLICY_ADVISORY", "MEDIA_NARRATIVE", "CONSORTIUM_FUNDING"):
                        has_policy = True
                    elif e_data.get("layer") == "CO_AUTHOR":
                        has_coauthor = True
            
            if has_policy:
                keep.add(neighbor)
            elif has_coauthor:
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
print("MULTIPLEX NETWERKANALYSE (MultiGraph & dynamic Louvain)")
print("=" * 60)

print(f"\n  Full graph:               {all_G.number_of_nodes():6d} nodes, {all_G.number_of_edges():6d} edges")
print(f"  Virology-filtered:        {all_viro_G.number_of_nodes():6d} nodes, {all_viro_G.number_of_edges():6d} edges")

# ── Centrality and Community computation ──────────────────────────────────
def compute_centrality_and_communities(G):
    if G.number_of_nodes() < 3:
        return {}
    # Convert MultiGraph to simple weighted graph for algorithms
    simple_G = to_weighted_simple_graph(G)
    
    bc = nx.betweenness_centrality(simple_G, k=min(100, simple_G.number_of_nodes()), weight='weight')
    dc = nx.degree_centrality(simple_G)
    ec = {}
    try:
        comps = [simple_G.subgraph(c) for c in sorted(nx.connected_components(simple_G), key=len, reverse=True)]
        if comps and comps[0].number_of_nodes() > 1:
            ec = nx.eigenvector_centrality_numpy(comps[0], max_iter=1000, weight='weight')
    except:
        pass
        
    partition = {}
    try:
        partition = community_louvain.best_partition(simple_G, weight='weight', random_state=42)
    except Exception as e:
        print(f"Louvain partitioning failed: {e}")
        
    # Format top betweenness nodes for the export script
    bc_top = [{"node": n, "score": s} for n, s in sorted(bc.items(), key=lambda x: -x[1])[:30]]
        
    return {
        "betweenness": bc,
        "betweenness_top": bc_top,
        "degree": dc,
        "eigenvector": ec,
        "partition": partition
    }

results = {}
for label, G in [("ALL_full", all_G), ("ALL_virology", all_viro_G)]:
    results[label] = compute_centrality_and_communities(G)
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
        results[label] = compute_centrality_and_communities(G_l)

# ── Save ─────────────────────────────────────────────────────────────────
with open(OUT_STATS, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"\n  Saved to {OUT_STATS}")

print("\n[DONE]")
conn.close()
