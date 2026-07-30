"""
build_woo_delta_views.py — STAP 2: Woo redaction delta simulation.
Analyseert gesimuleerde zwartlakkingsverschillen tussen Woo-vrijgaven (2021 vs 2024).
"""
import sqlite3, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")
OUT_PQ = os.path.join(ROOT, "data", "parquet", "woo_deltas.parquet")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS woo_redaction_deltas")
c.execute("""
CREATE TABLE woo_redaction_deltas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_name TEXT,
    woo_release_round TEXT,
    page_reference TEXT,
    content_segment TEXT,
    redacted_2021 INTEGER,
    redacted_2024 INTEGER,
    redaction_delta TEXT,
    relevance TEXT
)
""")

# Simulated redaction deltas based on known patterns in NL Woo releases
deltas = [
    ("RIVM OMT-advies 2020-02-05", "woo_2021_round1", "p12",
     "Advies om reizigers uit Hubei te screenen op symptomen", 0, 0,
     "None", "Open in both releases"),
    ("RIVM OMT-advies 2020-02-12", "woo_2021_round1", "p18",
     "Overweging om GGD-testcapaciteit op te schalen naar 500/dag", 0, 0,
     "None", "Open in both releases"),
    ("VWS subsidie NCOH 2020-03", "woo_2021_round1", "p34",
     "Subsidiebedrag: EUR 4.200.000 naar NCOH voor surveillance COVID-19 in vleermuizen", 1, 0,
     "Unredacted_2024",
     "Original Woo 2021 had bedrag zwartgelakt; Woo 2024 toont exacte bedrag"),
    ("VWS subsidie PDPC 2020-06", "woo_2021_round1", "p41",
     "PDPC programmabudget EUR 12.000.000 waarvan EUR 1.800.000 naar Erasmus MC (Viroscience)", 1, 0,
     "Unredacted_2024",
     "Erasmus MC Viroscience budget zichtbaar in 2024 release"),
    ("E-mailwisseling VWS-RIVM 2020-04-15", "woo_2021_round1", "p52",
     "Vraag van VWS aan RIVM: was OMT geinformeerd over internationale discussie over gain-of-function?", 1, 1,
     "Still_Redacted",
     "GOF-vraag blijft zwartgelakt in beide rondes -- niet openbaar"),
    ("E-mailwisseling VWS-RIVM 2020-04-15", "woo_2024_round2", "p52",
     "[zelfde passage] -- blijft onleesbaar", 1, 1,
     "Still_Redacted",
     "Hardnekkige blackling op GOF-correspondentie"),
    ("OMT-notulen 2020-02-17", "woo_2021_round1", "p28",
     "Van Dissel: 'Internationale wetenschappers hebben vorige week overleg gehad over sequentie' (verwijzing Feb 1 call zonder expliciete namen)", 1, 0,
     "Unredacted_2024",
     "Verwijzing naar Feb 1 call zichtbaar in 2024 — naam van deelnemers nog steeds zwart"),
    ("ZonMw subsidie Erasmus MC COMPARE 2020", "woo_2021_round1", "p61",
     "COMPARE EU Horizon 2020 subsidie EUR 10.300.000 (Koopmans coordinator) -- NL co-financiering EUR 1.200.000", 1, 0,
     "Unredacted_2024",
     "Koopmans COMPARE co-financiering zichtbaar in 2024"),
]

for d in deltas:
    c.execute("""INSERT INTO woo_redaction_deltas
        (document_name, woo_release_round, page_reference, content_segment, redacted_2021, redacted_2024, redaction_delta, relevance)
        VALUES (?,?,?,?,?,?,?,?)""", d)

print(f"  woo_redaction_deltas: {len(deltas)} entries")
stats = {}
for r in c.execute("SELECT redaction_delta, COUNT(*) as cnt FROM woo_redaction_deltas GROUP BY redaction_delta"):
    stats[r[0]] = r[1]
    print(f"    {r[0]}: {r[1]} entries")

# Create view
c.execute("DROP VIEW IF EXISTS vw_woo_redaction_deltas")
c.execute("""CREATE VIEW vw_woo_redaction_deltas AS
    SELECT document_name, woo_release_round, page_reference, content_segment,
           redacted_2021, redacted_2024, redaction_delta, relevance
    FROM woo_redaction_deltas
    ORDER BY document_name, woo_release_round
""")
print(f"  vw_woo_redaction_deltas created")

conn.commit()
conn.close()

# Write stats
stats_path = os.path.join(ROOT, "data", "woo_delta_stats.json")
with open(stats_path, "w") as f:
    json.dump(stats, f, indent=1)
print(f"  Stats -> {stats_path}")
print("[DONE] Woo redaction delta views built.")
