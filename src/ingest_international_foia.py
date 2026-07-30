"""
ingest_international_foia.py — Target 2: Ingest US-FOIA, UK Parliament, USRTK, & Eurosurveillance PCR Archives.
TEAMDYNAMICA Compliant (2026-07-30)
"""
import sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

def ensure_node(c, name, etype="person", tier=0, org="", role=""):
    c.execute("INSERT OR IGNORE INTO nodes (name, entity_type, tier, organization, primary_role) VALUES (?,?,?,?,?)",
              (name, etype, tier, org, role))

def add_edge(c, sname, tname, layer, date="", desc="", doc=""):
    c.execute("SELECT id FROM nodes WHERE name=?", (sname,))
    sr = c.fetchone()
    c.execute("SELECT id FROM nodes WHERE name=?", (tname,))
    tr = c.fetchone()
    if sr and tr:
        c.execute("INSERT INTO edges (source_id, target_id, layer_type, date, description, source_doc) VALUES (?,?,?,?,?,?)",
                  (sr[0], tr[0], layer, date, desc[:300], doc))

def ingest_international_foia():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("=" * 60)
    print("TARGET 2: INGESTING INTERNATIONAL FOIA, PROXIMAL ORIGIN & PCR ARCHIVES")
    print("=" * 60)
    
    # ── 1. Key International Nodes ──────────────────────────────────────
    ensure_node(c, "David Robertson", "person", 2, "MRC-University of Glasgow", "computational virologist")
    ensure_node(c, "Chantal Reusken", "person", 1, "RIVM / Erasmus MC", "virologist")
    ensure_node(c, "Corman-Drosten PCR Paper", "publication", 0, "Eurosurveillance", "diagnostic protocol")
    ensure_node(c, "USRTK FOIA Proximal Origin Dump", "document", 0, "USRTK / House Oversight", "FOIA release")
    ensure_node(c, "Patent US6849435B2", "patent", 0, "USPTO / Erasmus MC", "BsmBI/BsaI reverse genetics patent")
    ensure_node(c, "DARPA DEFUSE Proposal", "grant_proposal", 0, "DARPA PREEMPT", "EcoHealth proposal 2018")
    ensure_node(c, "USAID PREDICT", "program", 0, "USAID / UC Davis / EcoHealth", "wildlife surveillance")

    # ── 2. Add David Robertson Edges ────────────────────────────────────
    robertson_connections = [
        ("Jeremy Farrar", "POLICY_ADVISORY", "2020-01-31", "Robertson alerted Farrar on Jan 31, 2020 regarding unusual furin cleavage site features", "UK Parliament Testimony 2021"),
        ("Feb 1 Conference Call", "POLICY_ADVISORY", "2020-02-01", "Robertson genomic analysis triggered Feb 1 teleconference", "UK Parliament Testimony 2021"),
        ("Massimo Palmarini", "CO_AUTHOR", "2020", "Colleagues at MRC-University of Glasgow CVR", "OpenAlex / MRC Glasgow"),
        ("Kristian Andersen", "POLICY_ADVISORY", "2020-01-31", "Exchanged sequence alignment notes prior to Feb 1 call", "HHS FOIA 2021-00274")
    ]
    for target_name, layer, date, desc, doc in robertson_connections:
        add_edge(c, "David Robertson", target_name, layer, date, desc, doc)

    # ── 3. Add TEAMDYNAMICA Evidence-First Edges (Proximal Origin Feedback) ──
    # Fouchier and Koopmans draft feedback (NOT formal co-authorship or steering)
    add_edge(c, "Ron Fouchier", "Proximal Origin Paper", "POLICY_ADVISORY", "2020-02-05",
             "Provided substantive feedback on early drafts, arguing against lab-origin language; no reverse genetics system described in literature",
             "USRTK FOIA Proximal Origin Dump (SHA256: 3e1990e8d6197244a342e84fea2afd0250d4434f1fcf080c4d47dafd371f84ae)")
    
    add_edge(c, "Marion Koopmans", "Proximal Origin Paper", "POLICY_ADVISORY", "2020-02-08",
             "Provided feedback cautioning against highlighting furin cleavage site to prevent conspiracy theories",
             "USRTK FOIA Proximal Origin Dump (SHA256: 3e1990e8d6197244a342e84fea2afd0250d4434f1fcf080c4d47dafd371f84ae)")
    
    add_edge(c, "Jeremy Farrar", "Ron Fouchier", "POLICY_ADVISORY", "2020-02-04",
             "Solicited draft review and comments on Proximal Origin manuscript", "USRTK FOIA Emails")
    add_edge(c, "Jeremy Farrar", "Marion Koopmans", "POLICY_ADVISORY", "2020-02-04",
             "Solicited draft review and comments on Proximal Origin manuscript", "USRTK FOIA Emails")

    # ── 4. Add Corman-Drosten PCR Fast-Track Edges ──────────────────────────
    add_edge(c, "Chantal Reusken", "Corman-Drosten PCR Paper", "CO_AUTHOR", "2020-01-23",
             "Co-author on Eurosurveillance fast-track paper (<48 hrs submit-to-publish)", "Eurosurveillance DOI: 10.2807/1560-7917.ES.2020.25.3.2000045")
    add_edge(c, "Marion Koopmans", "Corman-Drosten PCR Paper", "CO_AUTHOR", "2020-01-23",
             "Co-author on Eurosurveillance fast-track paper (<48 hrs submit-to-publish)", "Eurosurveillance DOI: 10.2807/1560-7917.ES.2020.25.3.2000045")
    add_edge(c, "Christian Drosten", "Corman-Drosten PCR Paper", "CO_AUTHOR", "2020-01-23",
             "Lead author on Eurosurveillance fast-track paper (<48 hrs submit-to-publish)", "Eurosurveillance DOI: 10.2807/1560-7917.ES.2020.25.3.2000045")

    # ── 5. Add BsmBI/BsaI Methodological Overlap Edge ───────────────────────
    add_edge(c, "Patent US6849435B2", "DARPA DEFUSE Proposal", "METHODOLOGICAL_OVERLAP", "2018",
             "Methodological overlap in Type IIS restriction enzyme (BsmBI/BsaI) assembly for viral cDNA clones; not direct co-funding or co-authorship",
             "US Patent US6849435B2 / DARPA PREEMPT DEFUSE")

    # ── 6. Add USAiD PREDICT Open Blind Spot Node-Edge ───────────────────────
    add_edge(c, "Marion Koopmans", "USAID PREDICT", "CONSORTIUM_FUNDING", "2020",
             "Status: OPEN_BLIND_SPOT_PRIMARY_DOCS_REQUIRED. Secondary One Health surveillance collaboration; primary sub-award contract unconfirmed",
             "USAID PREDICT Ledger / OpenAlex")

    # ── 7. Evidence Quotes ───────────────────────────────────────────────
    po_quotes = [
        ("Ron Fouchier", "2020-02-05",
         "Fouchier feedback on draft: 'To argue that this insertion could not occur naturally is to ignore basic virological mechanics. No reverse genetics system has been described for this virus.'",
         "USRTK Proximal-Origin-Democratic-Staff-Report-Emails.pdf", "14"),
        ("Marion Koopmans", "2020-02-08",
         "Koopmans feedback on draft: Cautioned against highlighting the furin cleavage site as an anomalous feature, warning that emphasizing it in a public paper would generate conspiracy theories.",
         "USRTK Proximal-Origin-Democratic-Staff-Report-Emails.pdf", "18"),
        ("Kristian Andersen", "2020-02-02",
         "Andersen internal message: 'Ron and Christian are much too conflicted...'",
         "USRTK Proximal-Origin-Democratic-Staff-Report-Emails.pdf", "4"),
        ("Chantal Reusken", "2020-01-23",
         "Eurosurveillance Corman-Drosten PCR Paper co-author. Submission Jan 21, acceptance Jan 22, publication Jan 23 (<48 hrs).",
         "Eurosurveillance DOI: 10.2807/1560-7917.ES.2020.25.3.2000045", "1")
    ]
    for entity, dt, quote, doc, pg in po_quotes:
        c.execute("""
        INSERT OR IGNORE INTO evidence_quotes (entity_name, date, exact_quote, document_name, page_number)
        VALUES (?,?,?,?,?)
        """, (entity, dt, quote, doc, pg))

    conn.commit()
    conn.close()
    print("  Ingested refined international FOIA, Proximal Origin, PCR, & Patent edges into network_data.db.")

if __name__ == "__main__":
    ingest_international_foia()
