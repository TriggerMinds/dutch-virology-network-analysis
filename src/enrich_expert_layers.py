"""
enrich_expert_layers.py — STAP 3: Woo-document mapping + DURC genomics field.
"""
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("=" * 60)
print("EXPERT LAYERS — Woo mapping + Genomic DURC")
print("=" * 60)

# ── Table: woo_documents ─────────────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS woo_documents")
c.execute("""
CREATE TABLE woo_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    woo_number TEXT UNIQUE,
    title TEXT,
    source_institution TEXT,
    description TEXT,
    relevance_to_case TEXT,
    url TEXT
)
""")

woo_entries = [
    ("Woo/3661708", "RIVM OMT COVID-19 adviezen jan-jun 2020", "RIVM",
     "Outbreak Management Team minutes and advice", "OMT roles van Dissel, Timen, Bonten, Kluytmans, Gommers -- documenteert NL beleidsreactie op Feb 1 call",
     "https://www.rivm.nl/coronavirus-covid-19/omt"),
    ("Woo/VWS-2021-001", "VWS COVID-19 subsidy decisions", "Ministerie VWS",
     "Grant decisions for pandemic preparedness", "ZonMw/NCOH/PDPC funding to Erasmus MC",
     "https://www.rijksoverheid.nl/zaken/woo"),
    ("Woo/EU-CORDIS-VEO", "VEO project GA#874735 (EU CORDIS)", "EU Horizon 2020",
     "Versatile Emerging infectious disease Observatory", "Koopmans coordinator; bat coronavirus surveillance; spillover detection",
     "https://cordis.europa.eu/project/id/874735"),
    ("Woo/EU-CORDIS-ECRAID", "ECRAID project GA#965313 (EU CORDIS)", "EU Horizon 2020",
     "European Clinical Research Alliance on Infectious Diseases", "Bonten coordinator; clinical trial networks for emerging infections",
     "https://cordis.europa.eu/project/id/965313"),
    ("Woo/US-NIH-2R01AI110964", "EcoHealth Alliance grant #2R01AI110964-06A1", "NIH/NIAID",
     "Predicting virus emergence from wildlife (PI: Daszak)", "Sub-awards to Wuhan Institute of Virology; Shi Zhengli bat coronavirus research",
     "https://reporter.nih.gov/search/Daszak"),
    ("Woo/US-PARLIAMENT-FARRAR", "Jeremy Farrar UK Parliament testimony 2021", "UK Parliament",
     "Farrar describes Jan 31 2020 call with Fauci; David Robertson furin discovery", "Primary source for Robertson role in Feb 1 call trigger",
     "https://committees.parliament.uk/work/"),
]
for entry in woo_entries:
    c.execute("INSERT OR IGNORE INTO woo_documents (woo_number, title, source_institution, description, relevance_to_case, url) VALUES (?,?,?,?,?,?)", entry)
print(f"  woo_documents: {len(woo_entries)} entries")

# ── DURC genomics relevance field ────────────────────────────────────────
# Add table for DURC-relevant publications
c.execute("DROP TABLE IF EXISTS durc_genomics")
c.execute("""
CREATE TABLE durc_genomics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    authors TEXT,
    publication_year INTEGER,
    doi TEXT,
    durc_category TEXT,
    relevance TEXT
)
""")

durc_entries = [
    ("Airborne Transmission of Influenza A/H5N1 Virus Between Ferrets",
     "Ron Fouchier et al.", 2012, "10.1126/science.1213362",
     "GOF_influenza",
     "Fouchier's H5N1 ferret study -- showed 5 mutations enable aerosol transmission. Basis for 'original GOF person' characterization."),
    ("Isolation of a Novel Coronavirus from a Man with Pneumonia in Saudi Arabia",
     "Ron Fouchier et al.", 2012, "10.1056/NEJMoa1211721",
     "coronavirus_discovery",
     "MERS-CoV discovery. Top-cited Fouchier work (6045 citaties)."),
    ("Detection of 2019 novel coronavirus (2019-nCoV) by real-time RT-PCR",
     "Marion Koopmans et al.", 2020, "10.2807/1560-7917.ES.2020.25.3.2000045",
     "diagnostic",
     "Worldwide SARS-CoV-2 PCR protocol. Koopmans' top-cited work (8194 citaties)."),
    ("SARS-CoV-2 productively infects human gut enterocytes",
     "Marion Koopmans et al.", 2020, "10.1126/science.abc1669",
     "coronavirus_pathogenesis",
     "Showed SARS-CoV-2 infects gut cells -- relevance for fecal-oral transmission."),
    ("The Proximal Origin of SARS-CoV-2",
     "Kristian Andersen, Edward Holmes, Andrew Rambaut, Robert Garry et al.", 2020,
     "10.1038/s41591-022-01791-8",
     "origin_debate",
     "Argues for natural origin; authored by 5 Feb 1 call participants. Central paper in origins debate."),
    ("Characterization of spike glycoprotein of SARS-CoV-2 on virus entry and its immune cross-reactivity with SARS-CoV",
     "Shi Zhengli et al.", 2020, "10.1038/s41467-020-15562-9",
     "spike_ace2",
     "WIV study on spike-ACE2 interaction -- cited by Fauci as evidence of GOF work at Wuhan."),
    ("Mapping the Antigenic and Genetic Evolution of Influenza Virus",
     "Ron Fouchier et al.", 2004, "10.1126/science.1097211",
     "influenza_surveillance",
     "Influenza evolution mapping -- influential in pandemic surveillance methodology."),
]
for entry in durc_entries:
    c.execute("INSERT OR IGNORE INTO durc_genomics (title, authors, publication_year, doi, durc_category, relevance) VALUES (?,?,?,?,?,?)", entry)
print(f"  durc_genomics: {len(durc_entries)} entries")

# ── Link DURC to nodes ───────────────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS node_durc_link")
c.execute("CREATE TABLE node_durc_link AS "
          "SELECT DISTINCT dg.id AS durc_id, n.id AS node_id, n.name AS person_name, dg.title AS publication "
          "FROM durc_genomics dg, nodes n "
          "WHERE n.tier IN (1,2) AND (dg.authors LIKE '%' || substr(n.name, 1, instr(n.name||' ',' ')-1) || '%' "
          "OR dg.authors LIKE '%' || substr(n.name, instr(n.name, ' ')+1) || '%')")
print(f"  node_durc_link: {c.execute('SELECT COUNT(*) FROM node_durc_link').fetchone()[0]} edges")

conn.commit()
conn.close()
print("[DONE] Expert layers enriched.")
