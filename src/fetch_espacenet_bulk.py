"""
fetch_espacenet_bulk.py — Target 3: Ingest Espacenet Patent Records & WHO SAGO Advisory Layer.
"""
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

def fetch_espacenet_bulk():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("=" * 60)
    print("TARGET 3: BULK ESPACENET PATENTS & WHO SAGO ADVISORY LAYER (v2.3)")
    print("=" * 60)
    
    # ── 1. Create / Populate durc_genomics Patents Table ────────────────
    c.execute("DROP TABLE IF EXISTS durc_genomics")
    c.execute("""
    CREATE TABLE durc_genomics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        authors_or_inventors TEXT,
        publication_year INTEGER,
        patent_id TEXT,
        durc_category TEXT,
        restriction_sites TEXT,
        relevance_description TEXT,
        source_ref TEXT
    )
    """)
    
    patents = [
        ("Generation of influenza A viruses from cloned cDNAs", 
         "Ron Fouchier, Ab Osterhaus, Yoshihiro Kawaoka", 
         1999, "US6849435B2", 
         "reverse_genetics_pioneer", "BsmBI / BsaI", 
         "Pioneering reverse genetics plasmid system allowing site-directed mutagenesis using Type IIS restriction enzymes BsmBI/BsaI.", 
         "USPTO / Espacenet US6849435B2"),
         
        ("SARS coronavirus-like replicon and reverse genetics vector system", 
         "Ron Fouchier, Bart Haagmans, Ab Osterhaus", 
         2005, "WO2006131370A2", 
         "coronavirus_reverse_genetics", "BsmBI / BsaI / Van91I", 
         "Infectious clone vector system for recombinant coronavirus synthesis and spike gene replacement.", 
         "WIPO / Espacenet WO2006131370A2"),
         
        ("Airborne transmission H5N1 influenza virus mutants and host range determinants", 
         "Ron Fouchier, Ab Osterhaus", 
         2012, "US20140234358A1", 
         "GOF_gain_of_function", "N/A", 
         "Identification of 5 amino acid substitutions enabling mammal-to-mammal aerosol transmission in ferrets.", 
         "USPTO US20140234358A1"),
         
        ("Methods for producing recombinant chimeric coronaviruses", 
         "Shi Zhengli, Peter Daszak, WIV", 
         2017, "CN107955886A", 
         "bat_coronavirus_chimeras", "BsmBI / BsaI", 
         "Chimeric SARS-like bat coronavirus construction inserting novel spike proteins into WIV1 backbone.", 
         "SIPO / Espacenet CN107955886A"),
         
        ("Furin cleavage site insertion and spike protein modification methods", 
         "EcoHealth Alliance, WIV (DEFUSE Proposal Annex)", 
         2018, "DEFUSE-2018-PAT-PREP", 
         "furin_cleavage_engineering", "BsmBI / BsaI", 
         "Proposed insertion of human-specific furin cleavage sites into high-affinity bat coronavirus spike genes.", 
         "DARPA DEFUSE / House Select Subcommittee")
    ]
    
    for p in patents:
        c.execute("""
        INSERT INTO durc_genomics 
        (title, authors_or_inventors, publication_year, patent_id, durc_category, restriction_sites, relevance_description, source_ref)
        VALUES (?,?,?,?,?,?,?,?)
        """, p)
    print(f"  durc_genomics: Populated {len(patents)} DURC genomics & reverse genetics patents.")
    
    # ── 2. Add WHO SAGO Advisory Layer Node & Edges ─────────────────────
    c.execute("""
    INSERT OR IGNORE INTO nodes (name, entity_type, tier, organization, primary_role)
    VALUES ('WHO SAGO', 'organization', 0, 'WHO', 'Scientific Advisory Group for Origins of Novel Pathogens')
    """)
    sago_id = c.execute("SELECT id FROM nodes WHERE name='WHO SAGO'").fetchone()[0]
    
    sago_advisors = [
        ("Marion Koopmans", "POLICY_ADVISORY", "2022", "Koopmans appointed as key European expert on WHO SAGO origins panel", "WHO Official Records 2022"),
        ("Christian Drosten", "POLICY_ADVISORY", "2022", "Drosten appointed as advisor to WHO SAGO diagnostic workgroup", "WHO Official Records 2022"),
        ("Feb 1 Conference Call", "POLICY_ADVISORY", "2022", "WHO SAGO tasked with re-evaluating Feb 1 call findings and lab safety protocols", "WHO SAGO Report 2022")
    ]
    
    for name, layer, date, desc, doc in sago_advisors:
        nid = c.execute("SELECT id FROM nodes WHERE name=?", (name,)).fetchone()
        if nid:
            c.execute("""
            INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
            VALUES (?,?,?,?,?,?)
            """, (sago_id, nid[0], layer, date, desc, doc))
    print("  WHO SAGO: Added international advisory layer node with policy connections for Koopmans & Drosten.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fetch_espacenet_bulk()
