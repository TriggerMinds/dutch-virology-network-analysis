import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
analyze_multiplex.py — STAP 4: Netwerkanalyse van de multiplex graaf.
Centraliteitsmaten: Betweenness, Eigenvector, Degree.
Community Detection: Louvain-algoritme per laag + over alle lagen.
"""
import json, sqlite3, networkx as nx
import community as community_louvain
from collections import defaultdict

DB_PATH = os.path.join(ROOT, "data", "network_data.db")
OUT_STATS = os.path.join(ROOT, "data", "centrality_results.json")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

print("=" * 60)
print("MULTIPLEX NETWERKANALYSE")
print("=" * 60)

# ── Bouw laag-specifieke grafen ──────────────────────────────────────────
layers = ["CO_AUTHOR", "POLICY_ADVISORY", "CONSORTIUM_FUNDING", "MEDIA_NARRATIVE"]
graphs = {}
all_G = nx.Graph()

for layer in layers:
    G = nx.Graph()
    edges = c.execute("""
        SELECT n1.name AS sname, n2.name AS tname, e.layer_type, e.date, e.description
        FROM edges e
        JOIN nodes n1 ON e.source_id = n1.id
        JOIN nodes n2 ON e.target_id = n2.id
        WHERE e.layer_type = ?
    """, (layer,)).fetchall()
    for e in edges:
        G.add_edge(e["sname"], e["tname"], layer=layer)
        all_G.add_edge(e["sname"], e["tname"], layer=layer)
    graphs[layer] = G
    print(f"\n  {layer:25s}: {G.number_of_nodes():5d} nodes, {G.number_of_edges():5d} edges")

print(f"\n  {'ALL LAYERS':25s}: {all_G.number_of_nodes():5d} nodes, {all_G.number_of_edges():5d} edges")

# ── 1. CENTRALITY METRICS ────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"1. CENTRALITEITSANALYSE")
print(f"{'='*50}")

results = {}

for label, G in list(graphs.items()) + [("ALL", all_G)]:
    if G.number_of_nodes() < 3:
        continue
    # Betweenness centrality
    betweenness = nx.betweenness_centrality(G, k=min(50, G.number_of_nodes()))
    # Degree centrality
    degree = nx.degree_centrality(G)
    # Eigenvector centrality (only for largest connected component)
    components = list(nx.connected_components(G))
    if components:
        largest = G.subgraph(max(components, key=len))
        eigenvector = nx.eigenvector_centrality_numpy(largest, max_iter=1000) if largest.number_of_nodes() > 1 else {}
    else:
        eigenvector = {}

    # Top results per metric
    top_between = sorted(betweenness.items(), key=lambda x: -x[1])[:10]
    top_degree = sorted(degree.items(), key=lambda x: -x[1])[:10]
    top_eigen = sorted(eigenvector.items(), key=lambda x: -x[1])[:10]

    results[label] = {
        "betweenness_top": [{"node": n, "score": round(s, 4)} for n, s in top_between],
        "degree_top": [{"node": n, "score": round(s, 4)} for n, s in top_degree],
        "eigenvector_top": [{"node": n, "score": round(s, 4)} for n, s in top_eigen],
    }

    print(f"\n  [{label}] Top-10 Betweenness Centrality:")
    for n, s in top_between[:5]:
        tier_info = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (n,)).fetchone()
        org = (tier_info["organization"] or "?") if tier_info else "?"
        print(f"    {n:30s} | between={s:.4f} | {org[:30]}")

# ── 2. LOUVAIN COMMUNITY DETECTION ──────────────────────────────────────
print(f"\n{'='*50}")
print(f"2. COMMUNITY DETECTION (LOUVAIN)")
print(f"{'='*50}")

for label, G in list(graphs.items()) + [("ALL", all_G)]:
    if G.number_of_nodes() < 5:
        continue
    partition = community_louvain.best_partition(G)
    communities = defaultdict(list)
    for node, comm_id in partition.items():
        communities[comm_id].append(node)
    print(f"\n  [{label}] {len(communities)} communities detected:")
    for comm_id, members in sorted(communities.items(), key=lambda x: -len(x[1]))[:5]:
        # Identify Tier 1-2 members in this community
        tier_nodes = []
        for m in members:
            r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (m,)).fetchone()
            if r and r["tier"] in (1, 2):
                tier_nodes.append((m, r["tier"], r["organization"] or ""))
        print(f"    Community {comm_id}: {len(members)} members")
        for tn in tier_nodes[:5]:
            print(f"      T{tn[1]} {tn[0]:30s} | {tn[2][:30]}")

# ── 3. MEDIA LAYER SPECIFIC ──────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"3. MEDIA NARRATIVE LAYER")
print(f"{'='*50}")
media_G = graphs.get("MEDIA_NARRATIVE")
if media_G and media_G.number_of_nodes() > 0:
    print(f"  Nodes: {media_G.number_of_nodes()}, Edges: {media_G.number_of_edges()}")
    between_m = nx.betweenness_centrality(media_G)
    for n, s in sorted(between_m.items(), key=lambda x: -x[1])[:10]:
        print(f"    {n:30s} | between={s:.4f}")

# ── WRITE RESULTS ─────────────────────────────────────────────────────────
with open(OUT_STATS, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"\n  Results written to {OUT_STATS}")

# ── SUMMARY ──────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"NETWERKANALYSE SAMENVATTING")
print(f"{'='*50}")
all_G = graphs.get("ALL", all_G)
if all_G.number_of_nodes() > 0:
    ab = nx.betweenness_centrality(all_G, k=min(50, all_G.number_of_nodes()))
    print(f"\n  Top-5 tussenpersonen (betweenness — 'verborgen bruggen'):")
    for n, s in sorted(ab.items(), key=lambda x: -x[1])[:5]:
        r = c.execute("SELECT tier, organization FROM nodes WHERE name=?", (n,)).fetchone()
        org = r["organization"] if r else ""
        tier = r["tier"] if r else 0
        print(f"    T{tier} {n:35s} | β={s:.4f} | {org[:30]}")

print(f"\n[DONE]")
conn.close()
