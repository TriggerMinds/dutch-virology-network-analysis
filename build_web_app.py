"""
build_web_app.py — v2.0: Generates docs/data.json (async WebGL), docs/data.js (legacy vis.js).
Each edge gets a year attribute for timeline filtering.
"""
import json, os, sqlite3, re
import networkx as nx
from networkx import betweenness_centrality, eigenvector_centrality_numpy
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
DB_PATH = os.path.join(DATA, "network_data.db")
GRAPH_PATH = os.path.join(DATA, "graph.json")
os.makedirs(DOCS, exist_ok=True)

print("[v2] Loading graph...")
with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    graph_data = json.load(f)

G = nx.Graph()
for n in graph_data["nodes"]:
    nid = n.pop("id")
    G.add_node(nid, **n)
for e in graph_data["edges"]:
    src = e.pop("source")
    tgt = e.pop("target")
    G.add_edge(src, tgt, **e)

print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

print("[v2] Computing centrality...")
bc = betweenness_centrality(G, k=min(100, G.number_of_nodes()))
ec = {}
try:
    comps = [G.subgraph(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    if comps and comps[0].number_of_nodes() > 1:
        ec = eigenvector_centrality_numpy(comps[0], max_iter=1000)
except:
    pass

print("[v2] Building data...")
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Load evidence
evidence_map = {}
for r in c.execute("SELECT entity_name, exact_quote, document_name, page_number FROM evidence_quotes ORDER BY entity_name"):
    en = r["entity_name"]
    if en not in evidence_map:
        evidence_map[en] = []
    evidence_map[en].append({"quote": (r["exact_quote"] or "")[:300], "source": r["document_name"] or "", "page": str(r["page_number"] or "")})

# Tier 1-3 seed nodes
ALWAYS_INCLUDE = set()
for r in c.execute("SELECT name FROM nodes WHERE tier IN (1,2,3)"):
    ALWAYS_INCLUDE.add(r["name"])
for name in ["Feb 1 Conference Call", "Deliberate Insertion Hypothesis",
             "Natural Origin Hypothesis", "Proximal Origin Paper",
             "Anthony Fauci", "Francis Collins", "Jeremy Farrar",
             "Kristian Andersen", "Edward Holmes", "Christian Drosten",
             "Shi Zhengli", "Peter Daszak", "Erasmus MC"]:
    ALWAYS_INCLUDE.add(name)

conn.close()

# ── Build nodes list ──────────────────────────────────────────────────────
DATE_PAT = re.compile(r"(202[0-2])")

def extract_year(node_id, attrs):
    """Best guess year for a node based on entity."""
    if attrs.get("entity_type") == "event" and "Feb 1" in node_id:
        return 2020
    tier = attrs.get("tier", 99)
    if tier == 1:
        return 2020  # active during pandemic
    return 2020  # default

def edge_year(e_attrs):
    """Extract numeric year from edge date attribute."""
    d = e_attrs.get("date", "2020")
    if not d:
        return 2020
    m = re.search(r"(20\d{2})", str(d))
    if m:
        return int(m.group(1))
    return 2020

# Build prioritised node list
all_nodes = list(G.nodes(data=True))
priority = []
for nid, attrs in all_nodes:
    if nid in ALWAYS_INCLUDE:
        priority.append((nid, attrs, 999))
        continue
    deg = G.degree(nid)
    b = bc.get(nid, 0)
    score = b * 10 + deg * 0.01
    priority.append((nid, attrs, score))

priority.sort(key=lambda x: -x[2])

# Build output data
nodes_out = []
edges_out = []
node_map = {}  # id -> index in nodes_out

# Add all Tier 1-3 + key nodes + top 600 total
MAX_VISIBLE = 600
for nid, attrs, scr in priority[:MAX_VISIBLE]:
    tier = attrs.get("tier", 0)
    if tier == 0:
        color = "#f39c12" if bc.get(nid, 0) > 0.01 else "#95a5a6"
        group_name = "global"
    else:
        cmap = {1: "#e74c3c", 2: "#3498db", 3: "#2ecc71"}
        color = cmap.get(tier, "#95a5a6")
        group_name = f"tier{tier}"
    
    idx = len(nodes_out)
    node_map[nid] = idx
    between = round(bc.get(nid, 0), 4)
    eigenv = round(ec.get(nid, 0), 4)
    degree = G.degree(nid)
    nodes_out.append({
        "id": nid,
        "label": (attrs.get("label") or nid)[:30],
        "org": attrs.get("org") or "",
        "tier": tier,
        "role": attrs.get("role") or "",
        "group": group_name,
        "color": color,
        "year": extract_year(nid, attrs),
        "centrality": {"betweenness": between, "eigenvector": eigenv, "degree": degree},
        "full_data": {
            "id": nid, "org": attrs.get("org") or "", "tier": tier, "role": attrs.get("role") or "",
            "betweenness": between, "eigenvector": eigenv, "degree": degree,
            "evidence": evidence_map.get(nid, [])
        }
    })

# Build edges between visible nodes
visible_ids = set(n["id"] for n in nodes_out)
seen_pairs = set()
for u, v, e_attrs in G.edges(data=True):
    if u in visible_ids and v in visible_ids:
        pair = tuple(sorted([node_map[u], node_map[v]]))
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            layer = e_attrs.get("layer", "unknown")
            lc = {"CO_AUTHOR": "#5dade2", "POLICY_ADVISORY": "#e74c3c",
                  "MEDIA_NARRATIVE": "#2ecc71", "CONSORTIUM_FUNDING": "#f39c12"}
            weight = e_attrs.get("weight") or 1
            if isinstance(weight, str): weight = 1
            try: weight = int(weight)
            except: weight = 1
            edges_out.append({
                "source": node_map[u],
                "target": node_map[v],
                "layer": layer,
                "color": lc.get(layer, "#95a5a6"),
                "year": edge_year(e_attrs),
                "desc": (e_attrs.get("desc") or e_attrs.get("description") or "")[:100],
                "weight": min(weight, 10)
            })

# Build full search index (all 5401 nodes)
full_index = []
for nid, attrs in all_nodes:
    between = round(bc.get(nid, 0), 4)
    full_index.append({
        "id": nid,
        "label": (attrs.get("label") or nid)[:50],
        "org": attrs.get("org") or "",
        "tier": attrs.get("tier") or 0,
        "role": attrs.get("role") or "",
        "centrality": between,
        "betweenness": between,
        "degree": G.degree(nid),
        "evidence": evidence_map.get(nid, [])
    })

# ── Write async data.json ────────────────────────────────────────────────
data_out = {
    "visible": {"nodes": nodes_out, "edges": edges_out},
    "fullIndex": full_index,
    "meta": {
        "totalNodes": G.number_of_nodes(),
        "totalEdges": G.number_of_edges(),
        "visibleNodes": len(nodes_out),
        "visibleEdges": len(edges_out),
        "searchable": len(full_index),
        "years": sorted(set(ey["year"] for ey in edges_out) | set(ny["year"] for ny in nodes_out))
    }
}

json_path = os.path.join(DOCS, "data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data_out, f, ensure_ascii=False, separators=(",", ":"))
print(f"  data.json: {len(nodes_out)} nodes, {len(edges_out)} edges ({os.path.getsize(json_path)/1024:.0f} KB)")

# ── Legacy data.js for vis.js fallback ────────────────────────────────────
# (Keep generating for backward compatibility)
js_path = os.path.join(DOCS, "data.js")
js_out = f"var VIS_DATA = {json.dumps(data_out, ensure_ascii=False, separators=(',',':'))};\n"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_out)
print(f"  data.js: legacy format written")

print(f"\n[DONE] v2.0 data ready.")
