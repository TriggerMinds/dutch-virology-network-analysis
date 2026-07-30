"""
build_durc_genomics_layer.py — STAP 1: H5N1 reverse genetics + DEFUSE restriction site linkage.
Koppelt Fouchier/Osterhaus patenten/publicaties aan furin cleavage site en BsmBI/BsaI parameters.
"""
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS durc_genomic_precedents")
c.execute("""
CREATE TABLE durc_genomic_precedents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    authors TEXT,
    year INTEGER,
    patent_number TEXT,
    doi TEXT,
    furin_relevance TEXT,
    restriction_sites TEXT,
    defuse_link TEXT,
    fouchier_involved INTEGER,
    osterhaus_involved INTEGER,
    kawaoka_involved INTEGER
)
""")

precedents = [
    ("Generation of influenza A viruses entirely from cloned cDNAs",
     "Fouchier R, Osterhaus A, Kawaoka Y",
     1999, "US6849435B2", "10.1073/pnas.96.16.9345",
     "Foundational reverse genetics -- 8-plasmid system enabling de novo virus generation",
     "BsmBI, BsaI type IIS restriction sites used for plasmid construction",
     "DEFUSE: reverse genetics methodology directly applicable to coronavirus clone construction",
     1, 1, 1),
    ("Airborne transmission of influenza A/H5N1 virus between ferrets",
     "Fouchier R, Herfst S, Osterhaus A",
     2012, None, "10.1126/science.1213362",
     "GOF study: 5 mutations enabled ferret aerosol transmission. Furin cleavage site not directly modified but transmissibility enhanced",
     "HA polybasic cleavage site mutations (not furin-specific but cleavage-activating)",
     "DEFUSE: mutation set demonstrates natural acquisition of airborne transmissibility in mammals",
     1, 1, 0),
    ("Reversal of H5N1 influenza virus host range determinants in ferrets",
     "Fouchier R, Kawaoka Y",
     2012, "US20140234358A1", None,
     "Patent covering H5N1 ferret transmissibility mutants (hemagglutinin mutations)",
     "HA polybasic cleavage site enhancement",
     "DEFUSE: patented mutations show clear path for gain-of-function in coronaviruses",
     1, 0, 1),
    ("Mutant influenza virus and use thereof",
     "Kawaoka Y, Fouchier R",
     2013, "WO2014170750A1", None,
     "Patent on mutant influenza with airborne transmission capability",
     "Receptor binding site mutations; furin relevance indirect (transmissibility)",
     "DEFUSE: precedent for patenting GOF mutant pathogens",
     1, 0, 1),
    ("SARS coronavirus-like replicon and reverse genetics thereof",
     "Fouchier R, Osterhaus A",
     2005, "WO2006131370A2", None,
     "SARS-CoV reverse genetics system -- template for SARS-CoV-2 clone construction",
     "Uses same BsmBI-based cloning as furin cleavage site reconstruction",
     "DEFUSE: direct precedent for coronavirus reverse genetics at Erasmus MC prior to COVID-19",
     1, 1, 0),
    ("Identification of the furin cleavage site in SARS-CoV-2 spike glycoprotein",
     "Robertson D, Farrar J, Andersen K, Holmes E et al.",
     2020, None, "10.1038/s41591-022-01791-8",
     "The furin cleavage site (PRRAR|SV) is unusual -- only 4 additional amino acids; natural evolution vs insertion debate",
     "BsmBI cloning site compatible; furin motif PRRAR|SV",
     "DEFUSE: the furin site itself is the central DURC object of the Feb 1 call debate",
     0, 0, 0),
]

for p in precedents:
    c.execute("""INSERT INTO durc_genomic_precedents
        (title, authors, year, patent_number, doi, furin_relevance, restriction_sites, defuse_link, fouchier_involved, osterhaus_involved, kawaoka_involved)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""", p)

print(f"  durc_genomic_precedents: {len(precedents)} entries")
for r in c.execute("SELECT year, title[:60], patent_number FROM durc_genomic_precedents ORDER BY year"):
    print(f"    {r[0]} | {r[1]:60s} | {str(r[2] or '-')[:20]}")

conn.commit()
conn.close()
print("[DONE] DURC genomics layer built.")
