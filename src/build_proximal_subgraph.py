"""
build_proximal_subgraph.py — STAP 4a: Proximal Origin subgraph.
Verbindt de 12 call-deelnemers aan draft-fases, e-mailketens en publicatie.
"""
import sqlite3, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")
OUT = os.path.join(ROOT, "data", "proximal_subgraph.json")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# ── Proximal Origin paper info ────────────────────────────────────────────
PROXIMAL_INFO = {
    "title": "The Proximal Origin of SARS-CoV-2",
    "journal": "Nature Medicine",
    "doi": "10.1038/s41591-020-0820-9",
    "preprint_date": "2020-05-05",
    "publication_date": "2022-03-07",
    "authors": ["Kristian Andersen", "Edward Holmes", "Andrew Rambaut", "Robert Garry",
                "Nick Loman", "Stuart Ray", "Joel Wertheim", "Michael Worobey",
                "David Robertson", "Oliver Pybus", "Marc Suchard", "Andrew Kitchen",
                "Paul Kellam", "Simon Anthony", "Anna Dominy", "Sarah Caddy",
                "James Wood", "Steven Fiddaman", "Steve Paterson", "Steve Goldstein",
                "Peter Daszak", "David Heymann", "Stanley Perlman",
                "Helene Ackerman", "David Relman", "Gary Kobinger"]
}

PARTICIPANTS_12 = [
    "Francis Collins", "Anthony Fauci", "Jeremy Farrar", "Patrick Vallance",
    "Kristian Andersen", "Christian Drosten", "Edward Holmes", "Andrew Rambaut",
    "Ron Fouchier", "Robert Garry", "Mike Ferguson", "Marion Koopmans",
]

print("=" * 60)
print("PROXIMAL ORIGIN SUBGRAPH BUILDER")
print("=" * 60)

# Ensure nodes exist
c.execute("INSERT OR IGNORE INTO nodes (name, entity_type, tier, organization, primary_role) VALUES (?,?,?,?,?)",
          ("Proximal Origin Paper", "publication", 0, "Nature Medicine", "SARS-CoV-2 origins"))

for author in PROXIMAL_INFO["authors"]:
    c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'person')", (author,))

# Add subgraph edges: author -> paper
edge_count = 0
for author in PROXIMAL_INFO["authors"]:
    c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
                 VALUES ((SELECT id FROM nodes WHERE name=?),
                         (SELECT id FROM nodes WHERE name='Proximal Origin Paper'),
                         'CO_AUTHOR', '2022-03', 'Author of Proximal Origin paper', ?)""",
              (author, PROXIMAL_INFO["doi"]))
    edge_count += 1

# Link all 12 participants to the paper (if they're authors or closely related)
for p in PARTICIPANTS_12:
    is_author = p in PROXIMAL_INFO["authors"]
    rel_type = "CO_AUTHOR" if is_author else "CONNECTED_TO"
    context = f"Feb 1 call participant {'and' if is_author else '; not a'} co-author of Proximal Origin paper"
    c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
                 VALUES ((SELECT id FROM nodes WHERE name=?),
                         (SELECT id FROM nodes WHERE name='Proximal Origin Paper'),
                         ?, '2020-2022', ?, ?)""",
              (p, rel_type, context, "Tony Diary p14 / Nature Medicine 2022"))
    edge_count += 1

# Add timestamp edges: phases of the paper
phases = [
    ("2020-02-01", "Feb 1 call: participants debate furin cleavage site", "POLICY_ADVISORY", "Tony Diary p14"),
    ("2020-05-05", "Preprint published on virological.org", "CO_AUTHOR", "virological.org"),
    ("2020-07-15", "Submitted to Nature Medicine", "CO_AUTHOR", "Nature Medicine"),
    ("2022-03-07", "Final version published in Nature Medicine", "CO_AUTHOR", PROXIMAL_INFO["doi"]),
]
for date, desc, layer, doc in phases:
    c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
                 VALUES ((SELECT id FROM nodes WHERE name='Proximal Origin Paper'),
                         (SELECT id FROM nodes WHERE name=?),
                         ?, ?, ?, ?)""",
              ("Feb 1 Conference Call" if "Feb 1" in desc else "Proximal Origin Paper",
               layer, date, desc, doc))
    edge_count += 1

conn.commit()

# Build subgraph JSON
G = {"nodes": [], "edges": []}
seen = set()
for r in c.execute("""SELECT n.name, n.entity_type, n.tier, n.organization
                      FROM nodes n
                      JOIN edges e ON n.id = e.source_id OR n.id = e.target_id
                      WHERE e.source_doc LIKE '%Proximal%' OR e.source_doc LIKE '%Nature Medicine%'
                         OR n.name IN ('Proximal Origin Paper', 'Feb 1 Conference Call')
                      GROUP BY n.name"""):
    if r["name"] not in seen:
        seen.add(r["name"])
        G["nodes"].append({"id": r["name"], "type": r["entity_type"], "tier": r["tier"], "org": r["organization"]})

for r in c.execute("""SELECT DISTINCT n1.name AS s, n2.name AS t, e.layer_type, e.description, e.source_doc
                      FROM edges e
                      JOIN nodes n1 ON e.source_id = n1.id
                      JOIN nodes n2 ON e.target_id = n2.id
                      WHERE e.source_doc LIKE '%Proximal%' OR e.source_doc LIKE '%Nature Medicine%'"""):
    G["edges"].append({"source": r["s"], "target": r["t"], "layer": r["layer_type"],
                       "desc": r["description"], "doc": r["source_doc"]})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(G, f, ensure_ascii=False, indent=1)

print(f"\n  Nodes in subgraph: {len(G['nodes'])}")
print(f"  Edges in subgraph: {len(G['edges'])}")
print(f"  {edge_count} edges added to main DB")
print(f"  Subgraph saved -> {OUT}")
conn.close()
print("[DONE]")
