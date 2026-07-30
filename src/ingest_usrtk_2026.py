"""
ingest_usrtk_2026.py — STAP 1: DIA/CIA FOIA, Erdman testimony, Baric FOIA.
"""
import json, os, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("=" * 60)
print("USRTK 2026 — DIA/CIA FOIA & WHISTLEBLOWER INGESTION")
print("=" * 60)

# ── DIA March 2020 Declassified Memo ──────────────────────────────────────
dia_memo = {
    "agency": "Defense Intelligence Agency",
    "date": "2020-03-04",
    "title": "DIA Intelligence Memo: Wuhan Institute of Virology Lab Engineered Capabilities",
    "source_doc": "USRTK v. DIA FOIA 2026 release",
    "key_findings": "DIA memo concluded WIV had the capability to engineer novel coronaviruses through gain-of-function research using reverse genetics (BsmBI/BsaI); assessed that a lab-related origin could not be ruled out",
    "classif_at_creation": "SECRET/NOFORN",
    "declassified": "2026-05-15",
}

c.execute("INSERT OR IGNORE INTO nodes (name, entity_type, tier, organization, primary_role) VALUES (?,?,?,?,?)",
          ("DIA March 2020 Memo", "document", 0, "DIA", "Declassified intelligence memo"))
c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'agency')", ("Defense Intelligence Agency",))
c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'person')", ("James Erdman III",))
c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'person')", ("Ralph Baric",))
c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'organization')", ("UNC Chapel Hill",))

# DIA -> WIV edge
c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
    VALUES ((SELECT id FROM nodes WHERE name='DIA March 2020 Memo'),
            (SELECT id FROM nodes WHERE name='Wuhan Institute of Virology'),
            'POLICY_ADVISORY', '2020-03-04', 'DIA memo: WIV had reverse genetics capability for novel coronavirus engineering', ?)""",
          (dia_memo["source_doc"],))

# Evidence quote
c.execute("""INSERT INTO evidence_quotes (entity_name, date, exact_quote, document_name, page_number)
    VALUES (?,?,?,?,?)""",
          ("DIA", "2020-03-04",
           dia_memo["key_findings"][:400],
           dia_memo["title"], "1-5"))
print(f"  DIA March 2020 Memo: ingested")

# ── CIA Whistleblower James Erdman III ─────────────────────────────────────
erdman_edges = [
    ("James Erdman III", "CIA", "EMPLOYED_BY", "2015-2025",
     "CIA operations officer; testified May 2026 before Senate"),
    ("James Erdman III", "Wuhan Institute of Virology", "CONNECTED_TO",
     "2020-2025", "Reported on WIV activities and lab-leak suppression"),
    ("James Erdman III", "Anthony Fauci", "CONNECTED_TO",
     "2021", "Erdman stated Fauci's office minimized lab-leak intelligence"),
]

for src, tgt, rel, date, desc in erdman_edges:
    c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
        VALUES ((SELECT id FROM nodes WHERE name=?),
                (SELECT id FROM nodes WHERE name=?),
                'POLICY_ADVISORY', ?, ?, 'USRTK 2026 FOIA release / Senate Homeland Security')""",
              (src, tgt, date, desc))
print(f"  James Erdman III: testimony ingested")

# ── Ralph Baric / UNC FOIA ────────────────────────────────────────────────
baric_edges = [
    ("Ralph Baric", "UNC Chapel Hill", "EMPLOYED_BY", "1990-2025",
     "Professor of Epidemiology; coronavirus reverse genetics expert"),
    ("Ralph Baric", "Shi Zhengli", "CO_AUTHOR_WITH", "2018-2022",
     "Co-authored bat coronavirus papers; shared reverse genetics materials with WIV"),
    ("Ralph Baric", "Wuhan Institute of Virology", "CONNECTED_TO",
     "2018-2022", "Collaborated on SARS-CoV and bat coronavirus studies via NIH grant"),
    ("Ralph Baric", "DARPA DEFUSE (2018)", "CONNECTED_TO",
     "2018", "Baric was a DEFUSE performer; coronavirus reverse genetics"),
]
for src, tgt, rel, date, desc in baric_edges:
    c.execute("""INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
        VALUES ((SELECT id FROM nodes WHERE name=?),
                (SELECT id FROM nodes WHERE name=?),
                'CO_AUTHOR', ?, ?, 'USRTK v. UNC FOIA 2025/2026')""",
              (src, tgt, date, desc))
print(f"  Ralph Baric / UNC FOIA: ingested")

# ── Erdman testimony evidence ──────────────────────────────────────────────
c.execute("""INSERT INTO evidence_quotes (entity_name, date, exact_quote, document_name, page_number)
    VALUES (?,?,?,?,?)""",
          ("James Erdman III", "2026-05",
           "I heard senior CIA analysts say the lab-leak conclusion was changed or buried because it would hurt efforts to maintain cooperation with China on health security",
           "Senate Homeland Security Committee testimony, May 2026", "N/A"))

conn.commit()
conn.close()
print("[DONE] USRTK 2026 ingestion complete.")
