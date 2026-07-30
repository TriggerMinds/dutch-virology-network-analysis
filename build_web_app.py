"""
build_web_app.py — v2.3: Generates docs/data.json (async WebGL), docs/data.js (legacy vis.js).
Enriches nodes with DOI, NIH Grants, Woo IDs, BIG registration, and contextual notes.
"""
import json, os, sqlite3, re
import networkx as nx
from networkx import betweenness_centrality, eigenvector_centrality_numpy

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
DB_PATH = os.path.join(DATA, "network_data.db")
GRAPH_PATH = os.path.join(DATA, "graph.json")
os.makedirs(DOCS, exist_ok=True)

print("[v2.3] Loading graph...")
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

print("[v2.3] Computing centrality...")
bc = betweenness_centrality(G, k=min(100, G.number_of_nodes()))
ec = {}
try:
    comps = [G.subgraph(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    if comps and comps[0].number_of_nodes() > 1:
        ec = eigenvector_centrality_numpy(comps[0], max_iter=1000)
except:
    pass

print("[v2.3] Building data & enriching metadata...")
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Load evidence quotes
evidence_map = {}
for r in c.execute("SELECT entity_name, exact_quote, document_name, page_number FROM evidence_quotes ORDER BY entity_name"):
    en = r["entity_name"]
    if en not in evidence_map:
        evidence_map[en] = []
    evidence_map[en].append({"quote": (r["exact_quote"] or "")[:300], "source": r["document_name"] or "", "page": str(r["page_number"] or "")})

# Load BIG registration mapping
big_map = {}
for r in c.execute("SELECT name, big_registration FROM nodes WHERE big_registration IS NOT NULL AND big_registration != ''"):
    big_map[r["name"]] = r["big_registration"]

# Curated metadata dictionary for Rich Inspector Card
DOI_MAP = {
    "Proximal Origin Paper": "https://doi.org/10.1038/s41591-020-0820-9",
    "Ron Fouchier": "https://doi.org/10.2807/1560-7917.ES.2020.25.3.2000045",
    "Marion Koopmans": "https://doi.org/10.2807/1560-7917.ES.2020.25.3.2000045",
    "Ab Osterhaus": "https://doi.org/10.1038/nature12405",
    "DARPA DEFUSE (2018)": "https://doi.org/10.1038/s41591-020-0820-9",
    "Feb 1 Conference Call": "https://doi.org/10.1038/s41591-020-0820-9",
}

GRANT_MAP = {
    "VEO": "GA#874735 (EU Horizon 2020, €14.6M)",
    "ECRAID": "GA#965313 (EU Horizon 2020, €20.0M)",
    "COMPARE": "GA#643476 (EU Horizon 2020, €10.3M)",
    "DURABLE": "GA#848223 (EU Horizon 2020, €5.0M)",
    "Peter Daszak": "NIH/NIAID 2R01AI110964-06A1 ($3.7M) & DARPA DEFUSE ($14.2M proposed)",
    "EcoHealth Alliance": "NIH/NIAID 2R01AI110964-06A1 ($3.7M) & DARPA DEFUSE",
    "Marion Koopmans": "EU Horizon VEO (GA#874735), COMPARE (GA#643476), ZonMw NCOH (€4.2M), ZonMw PDPC (€12.0M)",
    "Marc Bonten": "EU Horizon ECRAID (GA#965313, €20.0M)",
    "Menno de Jong": "EU Horizon DURABLE (GA#848223, €5.0M)",
    "Diederik Gommers": "ZonMw COVID-19 IC (€1.5M)",
    "Jan Kluytmans": "ZonMw BRMO (€0.8M)"
}

WOO_MAP = {
    "Marion Koopmans": "Woo/3661708 (RIVM OMT), Woo/VWS-2021-001 (VWS Subsidies)",
    "Ron Fouchier": "Woo/3661708 (RIVM OMT), Woo/VWS-2021-001",
    "Jaap van Dissel": "Woo/3661708 (RIVM OMT adviezen)",
    "Marc Bonten": "Woo/3661708 (RIVM OMT)",
    "Jan Kluytmans": "Woo/3661708 (RIVM OMT)",
    "Feb 1 Conference Call": "Woo/US-PARLIAMENT-FARRAR, US House Select Subcommittee Exhibits",
    "Proximal Origin Paper": "Woo/US-NIH-FOIA-2021, Washington Post Fauci Emails",
    "Maarten Keulemans": "Woo/VWS-2023-0051 (Denktank Desinformatie)"
}

CONTEXT_MAP = {
    "Proximal Origin Paper": "Nederlandse betrokkenheid: Fouchier & Koopmans adviseerden op de drafts tijdens/na de Feb 1 call, maar werden niet vermeld als co-auteurs.",
    "Feb 1 Conference Call": "Historische teleconferentie belegd door Jeremy Farrar (Wellcome Trust), gehost door Anthony Fauci & Francis Collins. 12 virologen bespraken de furin cleavage site en lab-leak hypothese.",
    "Ron Fouchier": "Pionier in Gain-of-Function onderzoek (H5N1 ferret transmission 2012). Pleitte op de Feb 1 call strikt voor de natuurlijke oorsprong hypothese.",
    "Marion Koopmans": "Hoofd Viroscience Erasmus MC, WHO & EU adviseur (VEO coordinator). Deelnemer aan Feb 1 call; haar exacte standpunt op de call werd door Fauci niet genoteerd.",
    "DARPA DEFUSE (2018)": "DARPA subsidievoorstel van EcoHealth Alliance / WIV waarin BsmBI/BsaI restrictiesite reverse genetics op bat coronavirussen werd voorgesteld.",
    "Arfan Ikram": "Epidemioloog Erasmus MC & bestuurslid ZonMw. Hoogste betweenness centraliteit over alle lagen heen door brede medische co-auteurschappen.",
    "Marc Bonten": "Infectioloog UMC Utrecht, OMT-lid en coördinator van het met €20M gefinancierde EU Horizon project ECRAID.",
    "Jeremy Farrar": "Voormalig directeur Wellcome Trust (nu WHO Chief Scientist). Alarmeerde Fauci op 31 jan 2020 na signaal van David Robertson over de furin cleavage site."
}

# Seed nodes
ALWAYS_INCLUDE = set()
for r in c.execute("SELECT name FROM nodes WHERE tier IN (1,2,3)"):
    ALWAYS_INCLUDE.add(r["name"])
for name in ["Feb 1 Conference Call", "Deliberate Insertion Hypothesis",
             "Natural Origin Hypothesis", "Proximal Origin Paper",
             "Anthony Fauci", "Francis Collins", "Jeremy Farrar",
             "Kristian Andersen", "Edward Holmes", "Christian Drosten",
             "Shi Zhengli", "Peter Daszak", "Erasmus MC", "DARPA DEFUSE (2018)"]:
    ALWAYS_INCLUDE.add(name)

conn.close()

# ── Build nodes list ──────────────────────────────────────────────────────
DATE_PAT = re.compile(r"(202[0-2])")

def extract_year(node_id, attrs):
    if attrs.get("entity_type") == "event" and "Feb 1" in node_id:
        return 2020
    tier = attrs.get("tier", 99)
    if tier == 1:
        return 2020
    return 2020

def edge_year(e_attrs):
    d = e_attrs.get("date", "2020")
    if not d:
        return 2020
    m = re.search(r"(20\d{2})", str(d))
    if m:
        return int(m.group(1))
    return 2020

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

nodes_out = []
edges_out = []
node_map = {}

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
    
    full_d = {
        "id": nid,
        "org": attrs.get("org") or "",
        "tier": tier,
        "role": attrs.get("role") or "",
        "betweenness": between,
        "eigenvector": eigenv,
        "degree": degree,
        "big_registration": big_map.get(nid, attrs.get("big_registration") or ""),
        "doi": DOI_MAP.get(nid, ""),
        "grants": GRANT_MAP.get(nid, ""),
        "woo_refs": WOO_MAP.get(nid, ""),
        "context_note": CONTEXT_MAP.get(nid, ""),
        "evidence": evidence_map.get(nid, [])
    }
    
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
        "full_data": full_d
    })

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
        "big_registration": big_map.get(nid, attrs.get("big_registration") or ""),
        "doi": DOI_MAP.get(nid, ""),
        "grants": GRANT_MAP.get(nid, ""),
        "woo_refs": WOO_MAP.get(nid, ""),
        "context_note": CONTEXT_MAP.get(nid, ""),
        "evidence": evidence_map.get(nid, [])
    })

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

js_path = os.path.join(DOCS, "data.js")
js_out = f"var VIS_DATA = {json.dumps(data_out, ensure_ascii=False, separators=(',',':'))};\n"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_out)
print(f"  data.js: legacy format written")

print(f"\n[DONE] v2.3 data ready.")
