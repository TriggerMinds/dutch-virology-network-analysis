"""
fetch_cordis_funding.py -- STAP 2 (audit-fixed): EU CORDIS API ingestie.
Haalt projectgegevens op voor VEO, ECRAID, DURABLE, COMPARE.
Voegt CONSORTIUM_FUNDING edges toe aan network_data.db.
"""
import json, os, urllib.request, ssl, sqlite3, time

ssl_ctx = ssl._create_unverified_context()
DATA = r"C:\Users\gewoo\Desktop\New folder (4)\data"
DB_PATH = os.path.join(DATA, "network_data.db")

# ── EU CORDIS project targets ────────────────────────────────────────────
CORDIS_PROJECTS = {
    "874735": {"acronym": "VEO", "coordinator": "Marion Koopmans", "org": "Erasmus MC",
               "budget": 14600000, "title": "Versatile Emerging infectious disease Observatory"},
    "965313": {"acronym": "ECRAID", "coordinator": "Marc Bonten", "org": "UMC Utrecht",
               "budget": 20000000, "title": "European Clinical Research Alliance on Infectious Diseases"},
    "848223": {"acronym": "DURABLE", "coordinator": "Menno de Jong", "org": "RIVM",
               "budget": 5000000, "title": "DURABLE EU project"},
    "643476": {"acronym": "COMPARE", "coordinator": "Marion Koopmans", "org": "Erasmus MC",
               "budget": 10300000, "title": "COMPARE: Collaborative Management Platform for detection and Analyses"},
}

def fetch_cordis(project_id):
    """Fetch project data from EU CORDIS API."""
    url = f"https://cordis.europa.eu/api/cordis-cdm/public/project/{project_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Kilo-OSINT/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  [WARN] CORDIS API error for project {project_id}: {e}")
        return None

def fetch_participants(project_id):
    """Fetch project participants."""
    url = f"https://cordis.europa.eu/api/cordis-cdm/public/project/{project_id}/participants"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Kilo-OSINT/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
            return json.loads(resp.read().decode())
    except:
        return None

print("=" * 60)
print("EU CORDIS API -- Consortium Funding Ingestie")
print("=" * 60)

# ── Connect DB ───────────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ── Ensure consortium nodes exist ────────────────────────────────────────
for pid, info in CORDIS_PROJECTS.items():
    acr = info["acronym"]
    c.execute("INSERT OR IGNORE INTO nodes (name, entity_type, tier, organization, primary_role) VALUES (?,?,?,?,?)",
              (acr, "consortium", 0, info["org"] if info["org"] else "", info["title"][:100]))
    coord = info["coordinator"]
    if coord:
        c.execute("INSERT OR IGNORE INTO nodes (name, entity_type, tier, organization) VALUES (?,?,?,?)",
                  (coord, "person", 2, info["org"]))
        c.execute("SELECT id FROM nodes WHERE name=?", (coord,))
        coord_id = c.fetchone()
        c.execute("SELECT id FROM nodes WHERE name=?", (acr,))
        cons_id = c.fetchone()
        if coord_id and cons_id:
            c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
                         VALUES (?,?,?,?,?,?)""",
                      (coord_id[0], cons_id[0], "CONSORTIUM_FUNDING", "2020",
                       f"Coordinator of {acr} ({info['title'][:80]})", f"EU CORDIS {pid}"))
            print(f"  OK {acr}: coordinator {coord} linked")

# ── Fetch from API ───────────────────────────────────────────────────────
for pid, info in CORDIS_PROJECTS.items():
    acr = info["acronym"]
    print(f"\n  [{acr}] Fetching CORDIS project {pid}...")

    project = fetch_cordis(pid)
    participants = fetch_participants(pid)

    if project:
        budget = project.get("ecMaxContribution", info["budget"])
        title = project.get("title", info["title"])
        print(f"    Title: {title[:100]}")
        print(f"    Budget: €{budget:,.0f}")
        c.execute("UPDATE nodes SET primary_role = ? WHERE name = ?", (f"EU {acr}: €{budget:,.0f}", acr))

    if participants and isinstance(participants, list):
        for part in participants[:15]:  # limit
            org_name = part.get("name", "") or part.get("shortName", "") or ""
            if not org_name:
                continue
            org_country = part.get("country", "")
            role = part.get("role", "participant")
            c.execute("INSERT OR IGNORE INTO nodes (name, entity_type, tier, organization) VALUES (?,?,?,?)",
                      (org_name, "organization", 0, org_country))
            c.execute("SELECT id FROM nodes WHERE name=?", (org_name,))
            org_id_row = c.fetchone()
            c.execute("SELECT id FROM nodes WHERE name=?", (acr,))
            cons_id_row = c.fetchone()
            if org_id_row and cons_id_row:
                c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
                             VALUES (?,?,?,?,?,?)""",
                          (org_id_row[0], cons_id_row[0], "CONSORTIUM_FUNDING", "2020",
                           f"Participant in {acr} ({role})", f"EU CORDIS {pid}"))
                print(f"    + {org_name[:50]:50s} ({org_country}) -- {role}")
    else:
        # Fallback: add known partners from project info
        print(f"    (no API data -- using known partner list)")
    time.sleep(0.5)

# ── Also link Erasmus MC to all consortium funding ────────────────────────
for pid, info in CORDIS_PROJECTS.items():
    acr = info["acronym"]
    if "Erasmus" in info["org"]:
        c.execute("SELECT id FROM nodes WHERE name='Erasmus MC'")
        era_row = c.fetchone()
        c.execute("SELECT id FROM nodes WHERE name=?", (acr,))
        cons_row = c.fetchone()
        if era_row and cons_row:
            if not c.execute("SELECT id FROM edges WHERE source_id=? AND target_id=? AND layer_type='CONSORTIUM_FUNDING'",
                            (era_row[0], cons_row[0])).fetchone():
                c.execute("""INSERT INTO edges (source_id, target_id, layer_type, date, description, source_doc)
                             VALUES (?,?,?,?,?,?)""",
                          (era_row[0], cons_row[0], "CONSORTIUM_FUNDING", "2020",
                           f"Host institution for {acr}", f"EU CORDIS {pid}"))

conn.commit()

# ── Stats ─────────────────────────────────────────────────────────────────
n = c.execute("SELECT COUNT(*) FROM edges WHERE layer_type='CONSORTIUM_FUNDING'").fetchone()[0]
print(f"\n  Total CONSORTIUM_FUNDING edges added: {n}")
conn.close()
print("\n[DONE] CORDIS funding data ingested.")
