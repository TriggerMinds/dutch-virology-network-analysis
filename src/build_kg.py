import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
build_kg.py — Stage 2: Entity & Relationship extraction, SQLite DB, network graph.
Input:  raw_data.json
Output: network_data.db (SQLite), graph.json (networkx export)
"""
import json, re, os, sqlite3
from collections import defaultdict
import networkx as nx

RAW_PATH = os.path.join(ROOT, "raw_data.json")
DB_PATH  = os.path.join(ROOT, "network_data.db")
GRAPH_PATH = os.path.join(ROOT, "graph.json")

# ── Load extracted text ──────────────────────────────────────────────────
with open(RAW_PATH, "r", encoding="utf-8") as f:
    pages = json.load(f)

# ── Pattern libraries ────────────────────────────────────────────────────

# Known persons (surname-first mentions likely)
KNOWN_PERSONS = [
    "Fauci", "Tony Fauci", "Anthony Fauci",
    "Rand Paul", "Paul",
    "Chris", "Christine Grady",
    "Redfield", "Robert Redfield",
    "Birx", "Deborah Birx",
    "Hahn", "Stephen Hahn",
    "Giroir", "Brett Giroir",
    "Azar", "Alex Azar",
    "Kushner", "Jared Kushner",
    "Meadows", "Mark Meadows",
    "McEnany", "Kayleigh McEnany",
    "Cncl Manc", "Manc",
    "Mnuchin", "Steve Mnuchin",
    "Pence", "Mike Pence",
    "Trump", "Donald Trump",
    "Biden", "Joe Biden",
    "Walensky", "Rochelle Walensky",
    "Collins", "Francis Collins",
    "Larry Brilliant",
    "Peter Daszak",
    "Kristian Andersen",
    "Edward Holmes",
    "Shi Zhengli",
    "Bob Redfield",
    "Rick Bright",
    "Scott Atlas",
    "Paul Offit",
    "Moncef Slaoui",
    "David Morens",
    "John Mascola",
    "Barney Graham",
    "Kizzmekia Corbett",
    "Peter Marks",
    "Luciana Borio",
    "Jeremy Farrar",
    "Rick Bright",
    "Carter",
    "Zeke Emanuel",
    "Eric Topol",
    "Tom Frieden",
    "Julie Gerberding",
    "Mark Zuckerberg",
    "Priscilla Chan",
    "Bill Gates",
    "Melinda Gates",
    "David Heymann",
    "Mike Ryan",
    "Tedros", "Tedros Adhanom",
    "Nilsen",
    "Zecca",
    "Kamp",
    "Hotez", "Peter Hotez",
    "Osterholm", "Michael Osterholm",
    "Gottlieb", "Scott Gottlieb",
]

KNOWN_ORGS = [
    "NIH", "National Institutes of Health",
    "NIAID", "National Institute of Allergy and Infectious Diseases",
    "CDC", "Centers for Disease Control",
    "FDA", "Food and Drug Administration",
    "WHO", "World Health Organization",
    "HHS", "Department of Health and Human Services",
    "BARDA", "Biomedical Advanced Research and Development Authority",
    "DSTL", "Defence Science and Technology Laboratory",
    "EcoHealth Alliance",
    "Wuhan Institute of Virology", "WIV",
    "Wuhan Laboratory",
    "USAID", "Defense Department", "DoD",
    "Congress",
    "White House",
    "State Department",
    "NIH Fogarty",
    "Fauci Emails",
    "Lancet", "NEJM", "New England Journal of Medicine",
    "Science", "Nature", "Cell",
    "Washington Post", "NYT", "New York Times",
    "Fox News", "CNN", "CNBC",
    "COVID-19 Response Team", "Coronavirus Task Force",
    "Operation Warp Speed",
    "DOD", "Department of Defense",
    "FBI",
    "CIA",
    "NSA",
    "NPIs",
    "ICTV",
    "ECOHEALTH",
    "Chatham House",
    "Wellcome Trust",
    "Gates Foundation", "Bill & Melinda Gates Foundation",
    "Clinton Foundation",
    "Rockefeller Foundation",
    "NIHCE",
    "NPCB",
    "NSABB",
    "NIHCM",
    "DSMB",
    "VRBPAC",
]

# ── Entity extraction functions ──────────────────────────────────────────

def extract_persons(text):
    found = set()
    # Known persons
    for name in KNOWN_PERSONS:
        if name.lower() in text.lower():
            found.add(name)
    # Generic patterns: "Dr. <First> <Last>", "Mr. <Last>", "Sen. <Last>"
    generic = re.findall(r'(?:Dr\.|Mr\.|Mrs\.|Ms\.|Sen\.|Rep\.|Prof\.|Secretary|Director)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
    for g in generic:
        if g not in ("None",) and len(g) > 2:
            found.add(g.strip())
    # Uppercase name patterns nearby keywords
    name_kw = re.findall(r'(?:said|according to|by|with|and|from)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', text)
    for nk in name_kw:
        found.add(nk.strip())
    return sorted(found)

def extract_orgs(text):
    found = set()
    for org in KNOWN_ORGS:
        if org.lower() in text.lower():
            found.add(org)
    # Acronym pattern (2-5 uppercase letters in parens, grab preceding word)
    acro = re.findall(r'\(([A-Z]{2,5})\)', text)
    for a in acro:
        # simple mapping
        if a not in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "AM", "PM"):
            found.add(a)
    return sorted(found)

def extract_financial(text, page):
    """Extract financial flows: grants, subsidies, contracts."""
    results = []
    # Dollar amounts
    amounts = re.finditer(r'\$[\d,]+(?:\.\d+)?\s*(?:million|billion|thousand|trillion)?(?:USD?)?', text, re.I)
    for m in amounts:
        val = m.group()
        ctx_start = max(0, m.start()-120)
        ctx_end = min(len(text), m.end()+120)
        context = text[ctx_start:ctx_end].strip().replace('\n', ' ')
        results.append({
            "value": val,
            "page": page,
            "context": context
        })
    return results

def extract_documents(text, page):
    """Extract referenced publications, reports, policies."""
    results = []
    # DOI pattern
    dois = re.finditer(r'10\.\d{4,}/[^\s,;)]+', text)
    for d in dois:
        ctx_start = max(0, d.start()-80)
        ctx_end = min(len(text), d.end()+80)
        context = text[ctx_start:ctx_end].strip().replace('\n', ' ')
        results.append({"doi": d.group(), "page": page, "context": context})
    # Quoted document titles
    titles = re.finditer(r'["""]([A-Z][A-Za-z0-9\s\-:;,!?]{10,})["""]', text)
    for t in titles:
        ctx_start = max(0, t.start()-40)
        ctx_end = min(len(text), t.end()+40)
        context = text[ctx_start:ctx_end].strip().replace('\n', ' ')
        results.append({"title": t.group(1), "page": page, "context": context})
    return results

# ── Build database ───────────────────────────────────────────────────────

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            title TEXT,
            org TEXT,
            first_seen_page INTEGER,
            mention_count INTEGER DEFAULT 1
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            org_type TEXT,
            first_seen_page INTEGER,
            mention_count INTEGER DEFAULT 1
        );
        CREATE TABLE financial_flows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT,
            context TEXT,
            page INTEGER,
            source_entity TEXT,
            target_entity TEXT
        );
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT UNIQUE,
            title TEXT,
            context TEXT,
            page INTEGER
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT,
            source_name TEXT,
            relation_type TEXT,
            target_type TEXT,
            target_name TEXT,
            context TEXT,
            page INTEGER,
            UNIQUE(source_name, relation_type, target_name)
        );
        CREATE TABLE page_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT,
            entity_type TEXT,
            page INTEGER,
            context TEXT
        );
    """)
    conn.commit()
    return conn

def extract_relationships(text, page, persons, orgs, db_conn):
    """Extract relationships between entities."""
    c = db_conn.cursor()
    # Co-location relationships — persons/orgs mentioned in same paragraph
    paragraphs = text.split('\n\n')
    for para in paragraphs:
        para_persons = [p for p in persons if p.lower() in para.lower()]
        para_orgs = [o for o in orgs if o.lower() in para.lower()]
        # Employment/membership: "X of/at Y"
        for p_name in para_persons:
            for o_name in para_orgs:
                if p_name.lower() in para.lower() and o_name.lower() in para.lower():
                    idx_p = para.lower().index(p_name.lower())
                    idx_o = para.lower().index(o_name.lower())
                    if abs(idx_p - idx_o) < 200:
                        ctx = para[:300].replace('\n', ' ')
                        try:
                            c.execute("""INSERT OR IGNORE INTO relationships
                                (source_type, source_name, relation_type, target_type, target_name, context, page)
                                VALUES (?,?,?,?,?,?,?)""",
                                ("person", p_name, "CONNECTED_TO", "organization", o_name, ctx, page))
                        except: pass
        # Person-person co-mention
        for i, p1 in enumerate(para_persons):
            for p2 in para_persons[i+1:]:
                idx1 = para.lower().index(p1.lower())
                idx2 = para.lower().index(p2.lower())
                if abs(idx1 - idx2) < 250:
                    ctx = para[:300].replace('\n', ' ')
                    try:
                        c.execute("""INSERT OR IGNORE INTO relationships
                            (source_type, source_name, relation_type, target_type, target_name, context, page)
                            VALUES (?,?,?,?,?,?,?)""",
                            ("person", p1, "CO_MENTIONED_WITH", "person", p2, ctx, page))
                    except: pass
    # Co-authorship: known persons co-mentioned near "published/co-authored/et al."
    known_set = set(p.lower() for p in KNOWN_PERSONS)
    for m in re.finditer(r'(?:published|co.?authored|et\s+al\.|co.?author|paper|study|report)', text, re.I):
        window = text[max(0,m.start()-150):min(len(text),m.end()+50)].lower()
        found = [p for p in known_set if p.lower() in window and len(p) > 3]
        found = list(set(found))
        for i in range(len(found)):
            for j in range(i+1, len(found)):
                ctx = window[:200].replace('\n', ' ')
                try:
                    c.execute("""INSERT OR IGNORE INTO relationships
                        (source_type, source_name, relation_type, target_type, target_name, context, page)
                        VALUES (?,?,?,?,?,?,?)""",
                        ("person", found[i], "CO_AUTHOR_WITH", found[j], ctx, page))
                except: pass
    # Funding relationships
    funding = re.finditer(r'(?:fund|grant|award|donation|gift|contract)\s+(?:from|to|by)\s+([A-Z][a-zA-Z\s]{2,40}?)\s+(?:to|from)\s+([A-Z][a-zA-Z\s]{2,40}?)', text, re.I)
    for m in funding:
        a, b = m.group(1).strip(), m.group(2).strip()
        ctx = text[max(0,m.start()-20):m.end()+80].replace('\n', ' ')
        try:
            c.execute("""INSERT OR IGNORE INTO relationships
                (source_type, source_name, relation_type, target_type, target_name, context, page)
                VALUES (?,?,?,?,?,?,?)""",
                ("organization", a, "FUNDED", "organization", b, ctx, page))
        except: pass
    db_conn.commit()

# ── Main ─────────────────────────────────────────────────────────────────

def main():
    conn = init_db()
    c = conn.cursor()
    all_persons = defaultdict(int)
    all_orgs = defaultdict(int)
    all_financial = []
    all_docs = []

    print("[kg] Processing pages...")
    for p in pages:
        pg = p["page"]
        text = p["text"]
        if not text.strip():
            continue

        # Persons
        for name in extract_persons(text):
            all_persons[name] += 1
            ctx = text[:200].replace('\n', ' ')
            try:
                c.execute("INSERT OR IGNORE INTO persons (name, first_seen_page) VALUES (?,?)", (name, pg))
                c.execute("UPDATE persons SET mention_count = mention_count + 1 WHERE name = ?", (name,))
                # Special: if name has a known title/org pattern
                if "Fauci" in name:
                    c.execute("UPDATE persons SET title = 'Director, NIAID', org = 'NIAID/NIH' WHERE name = ?", (name,))
                if "Redfield" in name:
                    c.execute("UPDATE persons SET title = 'Director, CDC', org = 'CDC' WHERE name = ?", (name,))
                if "Birx" in name:
                    c.execute("UPDATE persons SET title = 'White House COVID-19 Response Coordinator', org = 'White House' WHERE name = ?", (name,))
            except: pass
            c.execute("INSERT INTO page_audit (entity_name, entity_type, page, context) VALUES (?,?,?,?)",
                      (name, "person", pg, ctx[:300]))

        # Organizations
        for org in extract_orgs(text):
            all_orgs[org] += 1
            ctx = text[:200].replace('\n', ' ')
            try:
                c.execute("INSERT OR IGNORE INTO organizations (name, first_seen_page) VALUES (?,?)", (org, pg))
                c.execute("UPDATE organizations SET mention_count = mention_count + 1 WHERE name = ?", (org,))
            except: pass
            c.execute("INSERT INTO page_audit (entity_name, entity_type, page, context) VALUES (?,?,?,?)",
                      (org, "organization", pg, ctx[:300]))

        # Financial flows
        for f in extract_financial(text, pg):
            all_financial.append(f)

        # Documents
        for d in extract_documents(text, pg):
            all_docs.append(d)

        # Relationships — batch every 50 pages
        if pg % 50 == 0:
            p_names = [n for n, _ in sorted(all_persons.items(), key=lambda x: -x[1])[:40]]
            o_names = [n for n, _ in sorted(all_orgs.items(), key=lambda x: -x[1])[:30]]
            extract_relationships(text, pg, p_names, o_names, conn)
            print(f"[kg] Processed page {pg}/{p['page_total']}...", flush=True)

    # Final relationship pass
    p_names = [n for n, _ in sorted(all_persons.items(), key=lambda x: -x[1])[:60]]
    o_names = [n for n, _ in sorted(all_orgs.items(), key=lambda x: -x[1])[:50]]
    for p in pages:
        if p["has_text"]:
            extract_relationships(p["text"], p["page"], p_names, o_names, conn)
    print("[kg] Relationship extraction complete.")

    # Store financial flows
    for f in all_financial:
        c.execute("INSERT INTO financial_flows (value, context, page) VALUES (?,?,?)",
                  (f["value"], f["context"], f["page"]))

    # Store documents
    for d in all_docs:
        ref = d.get("doi", d.get("title", "unknown"))
        c.execute("INSERT OR IGNORE INTO documents (reference, title, context, page) VALUES (?,?,?,?)",
                  (ref, d.get("title",""), d["context"], d["page"]))

    conn.commit()
    print(f"[kg] DB written to {DB_PATH}")

    # ── Build NetworkX graph ─────────────────────────────────────────
    G = nx.Graph()
    # Add nodes
    c.execute("SELECT name, title, org FROM persons")
    for row in c.fetchall():
        G.add_node(row[0], type="person", title=row[1], org=row[2])

    c.execute("SELECT name FROM organizations")
    for row in c.fetchall():
        G.add_node(row[0], type="organization")

    # Add edges
    c.execute("SELECT source_name, relation_type, target_name, context, page FROM relationships")
    for row in c.fetchall():
        src, rel, tgt, ctx, page = row
        G.add_edge(src, tgt, relation=rel, context=ctx, page=page)

    # Export
    data = nx.node_link_data(G)
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"[kg] Graph exported to {GRAPH_PATH}")

    # Summary stats
    print(f"\n{'='*50}")
    print(f"SUMMARY")
    print(f"{'='*50}")
    print(f"Pages processed: {len(pages)}")
    print(f"Unique persons:  {len(all_persons)}")
    print(f"Unique orgs:     {len(all_orgs)}")
    print(f"Financial flows: {len(all_financial)}")
    print(f"Documents refs:  {len(all_docs)}")
    print(f"Relationships:   {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    print(f"\nTop 20 persons:")
    for n, c_ in sorted(all_persons.items(), key=lambda x: -x[1])[:20]:
        print(f"  {n}: {c_} mentions")
    print(f"\nTop 20 organizations:")
    for n, c_ in sorted(all_orgs.items(), key=lambda x: -x[1])[:20]:
        print(f"  {n}: {c_} mentions")

    conn.close()

if __name__ == "__main__":
    main()
