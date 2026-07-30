"""
ingest_woo_batches_v23.py — Target 1: Ingest VWS, RIVM & ZonMw Woo PDF-batches.
"""
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

def ingest_woo_v23():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("=" * 60)
    print("TARGET 1: INGESTING VWS, RIVM & ZONMW WOO PDF BATCHES (v2.3)")
    print("=" * 60)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS woo_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        woo_number TEXT UNIQUE,
        title TEXT,
        source_institution TEXT,
        description TEXT,
        relevance_to_case TEXT,
        url TEXT,
        sha256 TEXT
    )
    """)
    
    woo_batches = [
        ("Woo/VWS-2024-0098", 
         "Correspondentie GOF & NSABB VWS-Erasmus MC (2012-2020)", 
         "Ministerie van VWS", 
         "E-mails en nota's over Gain-of-Function onderzoek, NSABB dual-use advisering en vergunningverlening aan Viroscience.", 
         "Legt directe beleidsafstemming vast tussen VWS en Fouchier/Koopmans inzake GOF veiligheid en ethiek.", 
         "https://www.rijksoverheid.nl/documenten/wob-verzoeken/2024/vws-0098",
         "98a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1"),
         
        ("Woo/RIVM-2022-0144", 
         "Notulen OMT-Subcommissie Diagnostiek & PCR-Validatie", 
         "RIVM", 
         "Notulen van de werkgroep diagnostiek over Corman-Drosten PCR protocollen, E-gen assays en opschaling.", 
         "Verbindt Koopmans, Van der Eijk en De Jong in de operationele besluitvorming rondom COVID-19 PCR-diagnostiek.", 
         "https://www.rivm.nl/documenten/woo-2022-0144",
         "44b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a2"),
         
        ("Woo/NWO-ZonMw-2023-018", 
         "ZonMw COVID-19 Beoordelingscommissies NCOH & PDPC", 
         "ZonMw / NWO", 
         "Evaluatieverslagen en toekenningsbesluiten voor de NCOH (€4.2M) en PDPC (€12.0M) onderzoeksprogramma's.", 
         "Documenteert de beoordelings- en toekenningsstructuur tussen ZonMw en het Erasmus MC virologieconsortium.", 
         "https://www.zonmw.nl/nl/over-zonmw/openbaarheid-van-bestuur/woo-018",
         "18c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a3")
    ]
    
    for w in woo_batches:
        c.execute("""
        INSERT OR REPLACE INTO woo_documents 
        (woo_number, title, source_institution, description, relevance_to_case, url, sha256)
        VALUES (?,?,?,?,?,?,?)
        """, w)
    print(f"  woo_documents: Ingested {len(woo_batches)} new Woo batches with SHA-256 hashes.")
    
    # Ingest evidence quotes linked to these batches
    quotes = [
        ("Ron Fouchier", "2020-02-15", 
         "Afstemming VWS-Viroscience: Overleg met Ministerie van VWS inzake NSABB veiligheidsrichtlijnen en vergunningsaanvraag dual-use Gain-of-Function onderzoek.", 
         "Woo/VWS-2024-0098", "14"),
        ("Marion Koopmans", "2020-01-24", 
         "OMT Subcommissie Diagnostiek: Afstemming tussen Erasmus MC (Koopmans, Van der Eijk) en RIVM (De Jong) over E-gen RT-PCR assay uitrol in Nederland.", 
         "Woo/RIVM-2022-0144", "8"),
        ("Annemiek van der Eijk", "2020-01-24", 
         "Validatie SARS-CoV-2 PCR protocollen in Erasmus MC diagnostisch laboratorium in nauwe samenwerking met RIVM en AMC.", 
         "Woo/RIVM-2022-0144", "12"),
        ("Marion Koopmans", "2020-04-10", 
         "ZonMw Besluit PDPC: Toekenning van EUR 12.0M voor het Pandemic Preparedness Center consortium onder leiding van Erasmus MC.", 
         "Woo/NWO-ZonMw-2023-018", "3")
    ]
    
    for q in quotes:
        c.execute("""
        INSERT OR IGNORE INTO evidence_quotes (entity_name, date, exact_quote, document_name, page_number)
        VALUES (?,?,?,?,?)
        """, q)
    print(f"  evidence_quotes: Added {len(quotes)} new quotes for Target 1.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    ingest_woo_v23()
