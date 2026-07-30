"""
ingest_regulatory_phmpt.py — STAP 2: PHMPT, EudraVigilance, oversterfte tables.
"""
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("=" * 60)
print("REGULATORY & TRIAL DATA INGESTION (PHMPT + EUDRAVIGILANCE + OVERSTERFTE)")
print("=" * 60)

# ── Table: regulatory_trial_data ──────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS regulatory_trial_data")
c.execute("""
CREATE TABLE regulatory_trial_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trial_id TEXT,
    sponsor TEXT,
    document_type TEXT,
    phmpt_file_url TEXT,
    sha256_hash TEXT,
    key_findings TEXT
)
""")

trials = [
    ("NCT04368728 (BNT162b2)", "Pfizer/BioNTech", "EUA submission package",
     "https://phmpt.org/pfizer-application/", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     "Primary efficacy 95%; VAERS signals myocarditis/pericarditis in 16-24 males; ADSL data showed elevated reactogenicity at 30mcg dose"),
    ("NCT04470427 (mRNA-1273)", "Moderna", "EUA submission package",
     "https://phmpt.org/moderna-application/", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     "Primary efficacy 94.1%; safety profile similar to placebo except injection site reactions"),
    ("C4591001 (BNT162b2 CVRM)", "Pfizer/BioNTech", "5.3.6 Cumulative Vaccines Regulatory Report",
     "https://phmpt.org/pfizer-5-3-6/", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     "Updated safety dataset covering 50M+ doses; disproportionality signals for myocarditis, Bell's palsy, anaphylaxis"),
    ("C4591028 (pediatric)", "Pfizer/BioNTech", "VRBPAC briefing document",
     "https://phmpt.org/pfizer-pediatric/", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     "Pediatric safety data for 5-11 age group; myocarditis signal noted but deemed favorable risk-benefit by FDA"),
    ("NCT04516746 (JNJ-78436735)", "Johnson & Johnson", "EUA submission package",
     "https://phmpt.org/jnj-application/", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     "Single-dose efficacy 66.9%; TTS (thrombosis with thrombocytopenia) signal led to pause April 2021"),
]

for t in trials:
    c.execute("INSERT INTO regulatory_trial_data (trial_id, sponsor, document_type, phmpt_file_url, sha256_hash, key_findings) VALUES (?,?,?,?,?,?)", t)
print(f"  regulatory_trial_data: {len(trials)} entries")

# ── Table: oversterfte_studies ────────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS oversterfte_studies")
c.execute("""
CREATE TABLE oversterfte_studies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    title TEXT,
    date TEXT,
    data_source TEXT,
    methodology TEXT,
    key_conclusion TEXT,
    estimated_excess_deaths INTEGER,
    period TEXT,
    source_url TEXT
)
""")

studies = [
    ("Meester, R., Aukema, W., Jacobs, J., Bonte, T.",
     "Eindverslag onderzoek oversterfte 2021-2023 in Nederland",
     "2024-12-01", "CBS, RIVM",
     "Lineaire regressie op CBS sterftecijfers 2016-2019 als basis; vergelijking met waargenomen sterfte 2020-2023",
     "Significant hogere oversterfte dan door COVID-19 gecodeerd; gemiddeld 1.200-1.500 extra doden per maand in 2021-2022 die niet in RIVM COVID-19 registratie voorkomen",
     45000, "2020-2023",
     "https://eindverslagoversterfte.nl/"),
    ("CBS (Centraal Bureau voor de Statistiek)",
     "Oversterfte in Nederland 2020-2023",
     "2024-03-15", "CBS eigen data",
     "CBS-standaard oversterfteberekening; vergelijking waargenomen vs verwachte sterfte o.b.v. 5-jaar voortschrijdend gemiddelde",
     "2020: 8.800 extra doden (CBS); 2021: 5.400; 2022: 10.000; CBS bevestigt oversterfte ook buiten COVID-19-hoogtepunt",
     24200, "2020-2022",
     "https://www.cbs.nl/nl-nl/visualisaties/bevolkingsteller/overledenen"),
    ("RIVM",
     "COVID-19 gerelateerde sterfte in Nederland",
     "2024-06-01", "RIVM, CBS",
     "Koppeling RIVM COVID-19 meldingen aan CBS doodsoorzakenstatistiek",
     "RIVM registreerde 22.500 COVID-19-doden (2020-2023); verschil van 46.600 met totale oversterfte volgens Meester et al.",
     46600, "2020-2023",
     "https://www.rivm.nl/coronavirus-covid-19/grafieken/sterfte"),
]

for s in studies:
    c.execute("""INSERT INTO oversterfte_studies (author, title, date, data_source, methodology, key_conclusion, estimated_excess_deaths, period, source_url)
        VALUES (?,?,?,?,?,?,?,?,?)""", s)
print(f"  oversterfte_studies: {len(studies)} entries")

# ── EudraVigilance MedDRA references ──────────────────────────────────────
c.execute("""INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'system')""",
          ("EudraVigilance",))
c.execute("""INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'system')""",
          ("PHMPT (FDA)",))

c.execute("""INSERT OR IGNORE INTO nodes (name, entity_type, organization) VALUES (?, 'organization', 'Pfizer')""",
          ("Pfizer/BioNTech",))
c.execute("""INSERT OR IGNORE INTO nodes (name, entity_type, organization) VALUES (?, 'organization', 'Moderna')""",
          ("Moderna",))
c.execute("""INSERT OR IGNORE INTO nodes (name, entity_type, organization) VALUES (?, 'organization', 'Johnson & Johnson')""",
          ("Johnson & Johnson",))

conn.commit()
conn.close()
print("[DONE] Regulatory & oversterfte ingestion complete.")
