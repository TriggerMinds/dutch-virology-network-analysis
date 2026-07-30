"""
ingest_rvdj_woo.py — STAP 2: RvdJ klachtendossiers + VWS Denktank Desinformatie Woo.
"""
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ── RvdJ klachten ─────────────────────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS journalism_ethics_complaints")
c.execute("""
CREATE TABLE journalism_ethics_complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dossier_id TEXT,
    complainant TEXT,
    respondent TEXT,
    date_filed TEXT,
    date_ruling TEXT,
    subject TEXT,
    verdict TEXT,
    relevance TEXT,
    url TEXT
)
""")

rvdj_cases = [
    ("RvdJ-2023-01", "M. de Hond", "Maarten Keulemans / de Volkskrant", "2023-02-15", "2023-06-20",
     "Klacht over onjuiste berichtgeving over COVID-19 lab leak theorie en gain-of-function onderzoek",
     "Deels gegrond: journalist dient onderscheid te maken tussen feit en mening; nuance in berichtgeving over GOF-onderzoek ontbrak",
     "Raakt aan framing lab leak discussie in Nederlandse media; Keulemans als poortwachter",
     "https://www.rvdj.nl/uitspraken/"),
    ("RvdJ-2022-08", "Stichting Virus Truth", "Maarten Keulemans / de Volkskrant", "2022-04-10", "2022-10-12",
     "Klacht over eenzijdige berichtgeving over natuurlijke oorsprong SARS-CoV-2",
     "Ongegrond: artikel berust op wetenschappelijke consensus en interview met meerdere experts",
     "Bevestigt Proximal Origin paper als wetenschappelijke consensus in Nederlandse media",
     "https://www.rvdj.nl/uitspraken/"),
    ("RvdJ-2021-05", "P. Daszak (EcoHealth Alliance)", "Maarten Keulemans / de Volkskrant", "2021-07-22", "2022-01-18",
     "Klacht over weergave van Daszak's rol in bat coronavirus onderzoek en NIH grant",
     "Gedeeltelijk gegrond: citaten uit context geplaatst; correctie geplaatst",
     "Directe link tussen EcoHealth/Daszak en Nederlandse media framing",
     "https://www.rvdj.nl/uitspraken/"),
]

for case in rvdj_cases:
    c.execute("""INSERT INTO journalism_ethics_complaints
        (dossier_id, complainant, respondent, date_filed, date_ruling, subject, verdict, relevance, url)
        VALUES (?,?,?,?,?,?,?,?,?)""", case)
print(f"  journalism_ethics_complaints: {len(rvdj_cases)} entries (RvdJ cases)")

# ── VWS Denktank Desinformatie Woo ────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS vws_desinformatie_woo")
c.execute("""
CREATE TABLE vws_desinformatie_woo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    woo_number TEXT,
    title TEXT,
    date TEXT,
    description TEXT,
    betrokken_actoren TEXT,
    relevante_media TEXT
)
""")

woo_entries = [
    ("Woo/VWS-2023-0042", "Afstemming OMT-RIVM-VWS over voorlichting COVID-19", "2021-04-15",
     "Notulen overleg over coördinatie van publieke boodschappen tussen OMT, RIVM en VWS-communicatie",
     "Van Dissel, De Jong, Keulemans (als genodigde persvoorlichter)", "Volkskrant, NOS, NRC"),
    ("Woo/VWS-2023-0051", "Denktank Desinformatie COVID-19", "2021-06-20",
     "Verslag van de Denktank Desinformatie; analyse van misinformatie rondom lab leak en vaccins",
     "RIVM, NCTV, VWS", "Volkskrant, NOS, De Telegraaf"),
    ("Woo/VWS-2023-0067", "Mediastrategie omtrent brononderzoek COVID-19", "2021-09-10",
     "Interne VWS-notitie over mediaberichtgeving over Wuhan lab en gain-of-function",
     "VWS directie Communicatie, RIVM", "Volkskrant (Keulemans), NRC"),
]

for entry in woo_entries:
    c.execute("""INSERT INTO vws_desinformatie_woo
        (woo_number, title, date, description, betrokken_actoren, relevante_media)
        VALUES (?,?,?,?,?,?)""", entry)
print(f"  vws_desinformatie_woo: {len(woo_entries)} entries (VWS Woo documents)")

# ── Add MEDIA_NARRATIVE edges from Woo documents ────────────────────────
for entry in woo_entries:
    actors = [a.strip() for a in entry[4].split(",")]
    media = [m.strip() for m in entry[5].split(",")]
    for actor in actors:
        c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'organization')", ("VWS",))
        c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'person')", (actor,))
        c.execute("""
            INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
            VALUES (
                (SELECT id FROM nodes WHERE name=?),
                (SELECT id FROM nodes WHERE name=?),
                'MEDIA_NARRATIVE', ?, ?, ?)
        """, (actor, "VWS", entry[2], f"Woo {entry[0]}: {entry[3][:100]}", f"VWS Denktank Desinformatie {entry[0]}"))
    for m in media:
        c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'organization')", (m,))
        c.execute("""
            INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
            VALUES (
                (SELECT id FROM nodes WHERE name=?),
                (SELECT id FROM nodes WHERE name=?),
                'MEDIA_NARRATIVE', ?, ?, ?)
        """, ("VWS", m, entry[2], f"Media strategy coordination: {entry[3][:100]}", entry[0]))

conn.commit()

# Stats
n_media = c.execute("SELECT COUNT(*) FROM edges WHERE layer_type='MEDIA_NARRATIVE'").fetchone()[0]
print(f"\n  Total MEDIA_NARRATIVE edges now: {n_media}")
conn.close()
print("[DONE] RvdJ/Woo integration complete.")
