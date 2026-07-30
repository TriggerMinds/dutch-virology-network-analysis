import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
setup_multiplex_db.py — STAP 3: Multiplex SQLite database.
Layers: CO_AUTHOR, POLICY_ADVISORY, CONSORTIUM_FUNDING, MEDIA_NARRATIVE.
"""
import json, re, os, sqlite3
from collections import defaultdict

DB_PATH = os.path.join(ROOT, "data", "network_data.db")
RAW_PATH = os.path.join(ROOT, "data", "raw_data.json")
OA_PATH = os.path.join(ROOT, "data", "downloads", "openalex_multiplex.json")
NIH_PATH = os.path.join(ROOT, "data", "downloads", "nih_grants_multiplex.json")
FOIA_PATH = os.path.join(ROOT, "data", "downloads", "foia_references.json")

# ── TIER DEFINITIES ───────────────────────────────────────────────────────
TIERS = {
    "Ron Fouchier": (1, "Erasmus MC", "virologist"),
    "Marion Koopmans": (1, "Erasmus MC", "virologist"),
    "Ab Osterhaus": (1, "Univ. Veterinary Medicine Hannover", "virologist"),
    "Thijs Kuiken": (1, "Erasmus MC", "pathologist"),
    "Bart Haagmans": (1, "Erasmus MC", "virologist"),
    "Jaap van Dissel": (1, "LUMC / RIVM", "infectious disease control"),
    "Diederik Gommers": (1, "Erasmus MC", "intensivist"),
    "Jan Kluytmans": (1, "UMC Utrecht / Amphia", "microbiologist"),
    "Aura Timen": (2, "Radboud UMC / RIVM", "infectious disease control"),
    "Menno de Jong": (2, "RIVM / AMC", "virologist"),
    "Marc Bonten": (2, "UMC Utrecht", "infectious disease control"),
    "Annemiek van der Eijk": (2, "Erasmus MC", "virologist"),
    "Massimo Palmarini": (2, "MRC-University of Glasgow", "virologist"),
    "Arfan Ikram": (2, "Erasmus MC", "epidemiologist"),
    "Ernst Kuipers": (2, "Erasmus MC", "gastroenterologist / policy"),
    "Maarten Keulemans": (3, "de Volkskrant", "science journalist"),
}
CONSORTIA_INFO = {
    "PDPC": "Pandemic Preparedness and Response Consortium",
    "NCOH": "Netherlands Centre for One Health",
    "VEO": "Versatile Emerging infectious disease Observatory",
    "DURABLE": "DURABLE EU project",
    "ECRAID": "European Clinical Research Alliance on Infectious Diseases",
    "ESWI": "European Scientific Working Group on Influenza",
    "ZonMw": "Netherlands Organisation for Health Research and Development",
}
GLOBAL_NODES = {
    "Anthony Fauci": ("person", 0, "NIAID", "virologist/policy"),
    "Francis Collins": ("person", 0, "NIH", "geneticist/policy"),
    "Jeremy Farrar": ("person", 0, "Wellcome Trust", "tropical medicine/policy"),
    "Kristian Andersen": ("person", 0, "Scripps Research", "viral evolution"),
    "Edward Holmes": ("person", 0, "University of Sydney", "viral evolution"),
    "Andrew Rambaut": ("person", 0, "University of Edinburgh", "viral evolution"),
    "Christian Drosten": ("person", 0, "Charité Berlin", "virologist"),
    "Robert Garry": ("person", 0, "Tulane University", "virologist"),
    "Shi Zhengli": ("person", 0, "WIV", "bat coronavirus"),
    "Peter Daszak": ("person", 0, "EcoHealth Alliance", "ecohealth"),
    "Feb 1 Conference Call": ("event", 0, "", "meeting"),
    "Deliberate Insertion Hypothesis": ("position", 0, "", "scientific position"),
    "Natural Origin Hypothesis": ("position", 0, "", "scientific position"),
    "Proximal Origin Paper": ("publication", 0, "", "scientific paper"),
}

# ── DATABASE SETUP ────────────────────────────────────────────────────────
def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            entity_type TEXT,
            tier INTEGER DEFAULT 0,
            organization TEXT,
            primary_role TEXT
        );
        CREATE TABLE edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            target_id INTEGER,
            layer_type TEXT,
            date TEXT,
            description TEXT,
            source_doc TEXT,
            weight INTEGER DEFAULT 1
        );
        CREATE TABLE evidence_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT,
            date TEXT,
            exact_quote TEXT,
            document_name TEXT,
            page_number TEXT
        );
        CREATE TABLE timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            event_type TEXT,
            description TEXT,
            actors_involved TEXT,
            source_ref TEXT
        );
        CREATE INDEX idx_edges_source ON edges(source_id);
        CREATE INDEX idx_edges_layer ON edges(layer_type);
    """)
    return conn

def ensure_node(conn, name, etype="person", tier=0, org="", role=""):
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO nodes (name,entity_type,tier,organization,primary_role) VALUES (?,?,?,?,?)",
                  (name, etype, tier, org, role))
    except: pass

def add_edge(conn, sname, tname, layer, date="", desc="", doc=""):
    c = conn.cursor()
    c.execute("SELECT id FROM nodes WHERE name=?", (sname,))
    sr = c.fetchone()
    c.execute("SELECT id FROM nodes WHERE name=?", (tname,))
    tr = c.fetchone()
    if sr and tr:
        try:
            c.execute("INSERT INTO edges (source_id,target_id,layer_type,date,description,source_doc) VALUES (?,?,?,?,?,?)",
                      (sr[0], tr[0], layer, date, desc[:300], doc))
        except: pass

def add_evidence(conn, entity, quote, date="", doc="", page=""):
    c = conn.cursor()
    c.execute("INSERT INTO evidence_quotes (entity_name,date,exact_quote,document_name,page_number) VALUES (?,?,?,?,?)",
              (entity, date, quote[:500], doc, str(page)))

def add_timeline(conn, date, etype, desc, actors, ref):
    c = conn.cursor()
    c.execute("INSERT INTO timeline (date,event_type,description,actors_involved,source_ref) VALUES (?,?,?,?,?)",
              (date, etype, desc[:500], actors[:300], ref))

# ── MAIN ──────────────────────────────────────────────────────────────────
def main():
    conn = setup_db()
    c = conn.cursor()
    print("[db] Schema created.")

    # 1. Seed all nodes ─────────────────────────────────────────────────
    for name, (tier, org, role) in TIERS.items():
        ensure_node(conn, name, "person", tier, org, role)
    for cname, clabel in CONSORTIA_INFO.items():
        ensure_node(conn, cname, "consortium", 0, "", clabel)
    for gname, (gtype, g_tier, gorg, grole) in GLOBAL_NODES.items():
        ensure_node(conn, gname, gtype, g_tier, gorg, grole)

    # 2. Diary evidence (Fouchier, Koopmans only) ─────────────────────────
    print("[diary] Loading raw_data.json...")
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        pages = json.load(f)
    p14_text = ""
    for p in pages:
        if p["page"] == 14:
            p14_text = p["text"] or ""
        for person in ["Ron Fouchier", "Marion Koopmans"]:
            if person.lower() in (p["text"] or "").lower():
                ensure_node(conn, person, "person", TIERS.get(person, (0,"",""))[0])
                ctx = re.sub(r'\s+', ' ', (p["text"] or "")[:500]).strip()
                add_evidence(conn, person, ctx, "2020-02-01", "Tony's Diary", str(p["page"]))
                break

    # Feb 1 call edges
    ensure_node(conn, "Feb 1 Conference Call", "event")
    for name in TIERS:
        if name in ["Ron Fouchier", "Marion Koopmans"]:
            add_edge(conn, name, "Feb 1 Conference Call", "POLICY_ADVISORY",
                     "2020-02-01", f"Participated in Feb 1 call", "Tony's Diary p14")
    for gname in ["Anthony Fauci", "Francis Collins", "Jeremy Farrar", "Kristian Andersen",
                  "Edward Holmes", "Andrew Rambaut", "Christian Drosten", "Robert Garry"]:
        ensure_node(conn, gname)
        add_edge(conn, gname, "Feb 1 Conference Call", "POLICY_ADVISORY", "2020-02-01", "", "Tony's Diary p14")

    # Faction edges
    add_edge(conn, "Ron Fouchier", "Natural Origin Hypothesis", "POLICY_ADVISORY", "2020-02-01",
             "argued furin cleavage site could occur naturally", "Tony's Diary p14")
    add_edge(conn, "Christian Drosten", "Natural Origin Hypothesis", "POLICY_ADVISORY", "2020-02-01",
             "Drosten was with Ron", "Tony's Diary p14")
    for delib_name in ["Kristian Andersen", "Edward Holmes", "Andrew Rambaut",
                       "Robert Garry", "Anthony Fauci", "Francis Collins",
                       "Jeremy Farrar"]:
        add_edge(conn, delib_name, "Deliberate Insertion Hypothesis", "POLICY_ADVISORY", "2020-02-01",
                 "felt deliberate insertion was possible", "Tony's Diary p14")

    # 3. OpenAlex co-authorship edges ────────────────────────────────────
    print("[openalex] Loading co-authorship data...")
    with open(OA_PATH, "r", encoding="utf-8") as f:
        oa = json.load(f)
    n_coauthor_edges = 0
    for name, data in oa.items():
        if name not in TIERS:
            continue
        ensure_node(conn, name, "person", TIERS[name][0], TIERS[name][1], TIERS[name][2])
        for w in data.get("works", []):
            coauthors = w.get("coauthors", [])
            for ca in coauthors:
                ca_clean = ca.strip()
                if ca_clean and ca_clean != name and len(ca_clean) > 3:
                    ensure_node(conn, ca_clean, "person")
                    add_edge(conn, name, ca_clean, "CO_AUTHOR", str(w.get("publication_year","")),
                             f"via {w.get('title','')[:100]}", f"OpenAlex work: {w.get('doi','no-doi')}")
                    n_coauthor_edges += 1
                    if n_coauthor_edges % 1000 == 0:
                        print(f"  ... {n_coauthor_edges} co-author edges")
    print(f"  Total co-author edges: {n_coauthor_edges}")

    # 4. Consortium edges from NIH data ──────────────────────────────────
    print("[nih] Grant edges...")
    with open(NIH_PATH, "r", encoding="utf-8") as f:
        nih = json.load(f)
    n_grant_edges = 0
    for target, grants in nih.items():
        if isinstance(grants, list):
            for g in grants[:5]:
                title = g.get("project_title", "") or ""
                org = g.get("organization", {})
                org_name = org.get("org_name", "") if isinstance(org, dict) else str(org)
                appl_id = g.get("appl_id", "")
                txt = title + " " + org_name
                # Link consortium name → grant
                for cname in CONSORTIA_INFO:
                    if cname.lower() in txt.lower():
                        ensure_node(conn, cname, "consortium")
                        ensure_node(conn, org_name, "organization")
                        add_edge(conn, cname, org_name, "CONSORTIUM_FUNDING",
                                 str(g.get("fy", "")), title[:200], f"NIH grant {appl_id}")
                        n_grant_edges += 1
    print(f"  Consortium-grant edges: {n_grant_edges}")

    # 5. Media narrative edges ───────────────────────────────────────────
    ensure_node(conn, "Maarten Keulemans", "person", 3, "de Volkskrant", "science journalist")
    # Keulemans wrote about Proximal Origin, lab-leak, Fauci emails
    ensure_node(conn, "Proximal Origin Paper", "publication")
    add_edge(conn, "Maarten Keulemans", "Proximal Origin Paper", "MEDIA_NARRATIVE",
             "2022-03", "Keulemans reported on Proximal Origin publication", "Volkskrant")
    add_edge(conn, "Maarten Keulemans", "Anthony Fauci", "MEDIA_NARRATIVE",
             "2021-06", "Reported on Fauci email release / lab leak debate", "Volkskrant")
    add_edge(conn, "Kristian Andersen", "Proximal Origin Paper", "CO_AUTHOR",
             "2022-03", "Lead author of Proximal Origin paper", "DOI: 10.1038/s41591-022-01791-8")
    # Link all Feb 1 call participants who co-authored Proximal Origin
    for author, paper_role in [("Kristian Andersen", "lead"), ("Edward Holmes", "author"),
                                ("Andrew Rambaut", "author"), ("Robert Garry", "author")]:
        add_edge(conn, author, "Proximal Origin Paper", "CO_AUTHOR", "2022-03",
                 f"{paper_role} on Proximal Origin", "DOI: 10.1038/s41591-022-01791-8")

    # 6. Timeline entries ────────────────────────────────────────────────
    timeline_data = [
        ("2020-01-31", "trigger", "Jeremy Farrar calls Fauci about furin cleavage site — triggers Feb 1 call", "Jeremy Farrar, Anthony Fauci", "Tony's Diary p767"),
        ("2020-02-01", "meeting", "Fauci convenes 12 scientists incl. Fouchier, Koopmans. NO CONSENSUS on natural vs deliberate", "Fouchier, Koopmans, Fauci, Collins et al.", "Tony's Diary p14"),
        ("2020-02-09", "consultation", "Tom Frieden calls Fauci; discussed CFR estimates 0.2-0.3% vs 2%", "Tom Frieden, Anthony Fauci", "Tony's Diary p19"),
        ("2020-03-11", "declaration", "WHO declares COVID-19 a pandemic", "WHO, Fauci", "WHO"),
        ("2020-05", "publication", "Andersen et al. 'The Proximal Origin of SARS-CoV-2' published in Nature Medicine", "Andersen, Garry, Holmes, Rambaut", "DOI: 10.1038/s41591-022-01791-8"),
        ("2021-06", "FOIA release", "Washington Post publishes Fauci email archive — Koopmans/Fouchier emails public", "Fauci, Koopmans, Fouchier", "WashPost FOIA"),
        ("2022-03", "analysis", "Nature Medicine publishes final Proximal Origin paper with expanded analysis", "Andersen, Holmes, Rambaut, Garry", "DOI: 10.1038/s41591-022-01791-8"),
    ]
    for dt, etype, desc, actors, ref in timeline_data:
        add_timeline(conn, dt, etype, desc, actors, ref)

    conn.commit()
    # Stats
    n_nodes = c.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    n_edges = c.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    layers = c.execute("SELECT layer_type, COUNT(*) FROM edges GROUP BY layer_type ORDER BY COUNT(*) DESC").fetchall()
    n_evidence = c.execute("SELECT COUNT(*) FROM evidence_quotes").fetchone()[0]
    n_timeline = c.execute("SELECT COUNT(*) FROM timeline").fetchone()[0]
    print(f"\n{'='*50}")
    print(f"MULTIPLEX DB — EXTRACTIE VOLTOOID")
    print(f"{'='*50}")
    print(f"  Nodes:   {n_nodes}")
    print(f"  Edges:   {n_edges}")
    print(f"    Layer breakdown:")
    for l, cnt in layers:
        print(f"      {l:25s}: {cnt}")
    print(f"  Evidence quotes: {n_evidence}")
    print(f"  Timeline entries: {n_timeline}")
    print(f"\n  Tier 1 nodes in DB:")
    for r in c.execute("SELECT name, organization, primary_role FROM nodes WHERE tier=1 ORDER BY name"):
        print(f"    {r[0]:30s} | {str(r[1] or ''):30s} | {str(r[2] or '')}")
    print(f"  Consortia in DB:")
    for r in c.execute("SELECT name FROM nodes WHERE entity_type='consortium' ORDER BY name"):
        print(f"    {r[0]}")
    print(f"\n[db] Written to {DB_PATH}")
    conn.close()

if __name__ == "__main__":
    main()
