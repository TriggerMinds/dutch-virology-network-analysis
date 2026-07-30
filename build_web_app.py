"""
build_web_app.py — Generate interactive web visualization from knowledge graph.
Output: docs/data.js (graph data) + docs/index.html (web app)
"""
import json, os, sqlite3
import networkx as nx
from networkx import betweenness_centrality, eigenvector_centrality_numpy

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
DB_PATH = os.path.join(DATA, "network_data.db")
GRAPH_PATH = os.path.join(DATA, "graph.json")
os.makedirs(DOCS, exist_ok=True)

# Load graph
print("[load] Loading graph.json...")
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph_data = json.load(f)

G = nx.Graph()
for n in graph_data["nodes"]:
    node_id = n.pop("id")
    G.add_node(node_id, **n)
for e in graph_data["edges"]:
    src = e.pop("source")
    tgt = e.pop("target")
    G.add_edge(src, tgt, **e)

print(f"  Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# Compute centrality
print("[centrality] Computing betweenness & eigenvector...")
bc = betweenness_centrality(G, k=min(100, G.number_of_nodes()))
ec = {}
try:
    comps = [G.subgraph(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    if comps and comps[0].number_of_nodes() > 1:
        ec = eigenvector_centrality_numpy(comps[0], max_iter=1000)
except Exception as e:
    print(f"  Eigenvector skipped: {e}")

# Load DB
print("[db] Loading network_data.db...")
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# evidence
evidence_map = {}
for r in c.execute("SELECT entity_name, exact_quote, document_name, page_number FROM evidence_quotes ORDER BY entity_name"):
    en = r["entity_name"]
    if en not in evidence_map:
        evidence_map[en] = []
    evidence_map[en].append({
        "quote": r["exact_quote"][:300] if r["exact_quote"] else "",
        "source": r["document_name"] or "",
        "page": str(r["page_number"] or "")
    })

# timeline
timeline = []
for r in c.execute("SELECT date, event_type, description, actors_involved FROM timeline ORDER BY date"):
    timeline.append({
        "date": r["date"] or "",
        "type": r["event_type"] or "",
        "desc": (r["description"] or "")[:200],
        "actors": (r["actors_involved"] or "")[:100]
    })

conn.close()

# Build vis.js data
print("[build] Preparing vis.js data...")
MAX_NODES = 100  # initial visible nodes

# Sort by combined centrality for priority
all_nodes = list(G.nodes(data=True))
node_priority = []
for nid, attrs in all_nodes:
    deg = G.degree(nid)
    b = bc.get(nid, 0)
    e = ec.get(nid, 0)
    tier = attrs.get("tier", 99)
    score = b * 10 + e * 5 + deg * 0.01
    # Boost tier 1-3 nodes
    if tier in (1, 2, 3):
        score += 10
    node_priority.append((nid, attrs, score, b, e, deg))

node_priority.sort(key=lambda x: -x[2])

# Gather seed + high-priority nodes
seen = set()
vis_nodes = []
vis_edges = []
node_map = {}  # id → index

for nid, attrs, score, b, e, deg in node_priority[:MAX_NODES]:
    tier = attrs.get("tier", 0)
    color_map = {1: "#e74c3c", 2: "#3498db", 3: "#2ecc71", 0: "#95a5a6"}
    if tier == 0:
        # Check if this is a key node
        if b > 0.01 or nid in ["Feb 1 Conference Call", "Deliberate Insertion Hypothesis",
                                "Natural Origin Hypothesis", "Proximal Origin Paper",
                                "Anthony Fauci", "Francis Collins", "Jeremy Farrar",
                                "Kristian Andersen", "Edward Holmes", "Christian Drosten"]:
            color = "#f39c12"  # gold for global key nodes
            tier_label = "Key"
        else:
            color = "#95a5a6"
            tier_label = "Other"
    else:
        color = color_map.get(tier, "#95a5a6")
        tier_label = f"Tier {tier}"

    label = attrs.get("label", nid) or nid
    title = attrs.get("org", "") or ""

    idx = len(vis_nodes)
    node_map[nid] = idx
    vis_nodes.append({
        "id": idx,
        "label": label[:30],
        "title": f"{label}\n{title}\n{tier_label}\nβ={b:.4f}" if b else f"{label}\n{title}\n{tier_label}",
        "group": tier_label,
        "value": max(5, min(50, 10 + b * 100)),
        "color": color,
        "physics": True,
        "full_data": {
            "id": nid,
            "org": title,
            "tier": tier,
            "role": attrs.get("role", ""),
            "betweenness": round(b, 4),
            "eigenvector": round(e, 4),
            "degree": deg,
            "evidence": evidence_map.get(nid, [])
        }
    })

# Edges between visible nodes
visible_ids = set(n["full_data"]["id"] for n in vis_nodes)
for u, v, attrs in G.edges(data=True):
    if u in visible_ids and v in visible_ids:
        layer = attrs.get("layer", "unknown")
        layer_colors = {
            "CO_AUTHOR": {"color": "#5dade2", "dashes": False},
            "POLICY_ADVISORY": {"color": "#e74c3c", "dashes": False},
            "MEDIA_NARRATIVE": {"color": "#2ecc71", "dashes": True},
            "CONSORTIUM_FUNDING": {"color": "#f39c12", "dashes": True},
        }
        lc = layer_colors.get(layer, {"color": "#95a5a6", "dashes": False})
        vis_edges.append({
            "from": node_map[u],
            "to": node_map[v],
            "color": lc["color"],
            "dashes": lc["dashes"],
            "title": f"{layer}: {attrs.get('desc','')[:80]}",
            "layer": layer
        })

# Build full node index for search
print("[search] Building full node index...")
all_node_index = []
for nid, attrs in all_nodes:
    label = attrs.get("label", nid) or nid
    all_node_index.append({
        "id": nid,
        "label": label,
        "org": attrs.get("org", ""),
        "tier": attrs.get("tier", 0),
        "role": attrs.get("role", ""),
        "betweenness": round(bc.get(nid, 0), 4),
        "evidence": evidence_map.get(nid, [])
    })

# Write data.js
print("[write] Writing docs/data.js...")
js_data = f"""
var VIS_DATA = {{
    "nodes": {json.dumps(vis_nodes, ensure_ascii=False)},
    "edges": {json.dumps(vis_edges, ensure_ascii=False)},
    "fullIndex": {json.dumps(all_node_index, ensure_ascii=False)},
    "timeline": {json.dumps(timeline, ensure_ascii=False)}
}};
"""

with open(os.path.join(DOCS, "data.js"), "w", encoding="utf-8") as f:
    f.write(js_data)
print(f"  data.js: {len(vis_nodes)} visible nodes, {len(vis_edges)} visible edges")
print(f"  fullIndex: {len(all_node_index)} total nodes searchable")

print("\nDone. docs/data.js ready.")
