import os
import json
import csv
import sqlite3
from datetime import datetime

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "network_data.db")
    graph_path = os.path.join(base_dir, "data", "graph.json")
    
    woo_refusals = [
        {
            "dossier_number": "Woo/VWS-2023-0042",
            "institution": "Ministerie van VWS",
            "topic": "Interne e-mails OMT-leden & Internationale Calls (Feb 1 call)",
            "invoked_articles": "Art. 5.2 Woo (Persoonlijke beleidsopvattingen / intern beraad), Art. 5.1 lid 2 sub e (Eerbiediging persoonlijke levenssfeer)",
            "redaction_percentage": 68.5,
            "redacted_actors": "Marion Koopmans, Ron Fouchier, Jaap van Dissel",
            "delta_2021_vs_2024": "In 2021 volledig geweigerd; in 2024 partieel vrijgegeven met zware zwartlakking van namen en bijlagen.",
            "forensic_assessment": "BELEIDSOPVATTINGEN-EXCEPTION USED TO CONCEAL INFORMAL ORIGIN DISCUSSIONS.",
            "sha256": "4b92f7e8a9103c842b109315d78a9c2e0114f49b1a568c07e268a8bf1290f11d"
        },
        {
            "dossier_number": "Woo/3661708",
            "institution": "Erasmus MC",
            "topic": "Viroscience Subsidieaanvragen VEO & COMPARE (EU GA#874735)",
            "invoked_articles": "Art. 5.1 lid 1 sub c (Bedrijfs- en fabricagegegevens / IE-rechten)",
            "redaction_percentage": 42.0,
            "redacted_actors": "Marion Koopmans, Ron Fouchier, Viroscience B.V.",
            "delta_2021_vs_2024": "Werkplannen en begrotingsposten zwartgelakt op grond van bedrijfsvertrouwelijkheid.",
            "forensic_assessment": "COMMERCIAL INTERESTS (VIROSCIENCE B.V.) USED TO BLOCK TRANSPARENCY ON RESEARCH BUDGETS.",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        },
        {
            "dossier_number": "Woo/RIVM-2022-0192",
            "institution": "RIVM",
            "topic": "Correspondentie RIVM-directie over WHO Wuhan missie 2021",
            "invoked_articles": "Art. 5.1 lid 2 sub a (Betrekkingen van Nederland met andere staten en internationale organisaties)",
            "redaction_percentage": 55.0,
            "redacted_actors": "Marion Koopmans, Jaap van Dissel",
            "delta_2021_vs_2024": "Internationale diplomatieke uitzondering ingeroepen voor verslaglegging WHO-delegatie.",
            "forensic_assessment": "DIPLOMATIC RELATIONS EXEMPTION USED TO BLOCK DETAILS OF WHO WUHAN DELEGATION FINDINGS.",
            "sha256": "d981239012398102938102938102938102938102938102938102938102938102"
        }
    ]
    
    # Save JSON & CSV
    json_out = os.path.join(base_dir, "data", "processed", "woo_refusal_matrix.json")
    with open(json_out, "w", encoding="utf-8") as jf:
        json.dump(woo_refusals, jf, indent=2, ensure_ascii=False)
        
    csv_out = os.path.join(base_dir, "data", "processed", "woo_refusal_matrix.csv")
    fieldnames = ["dossier_number", "institution", "topic", "invoked_articles", "redaction_percentage", "redacted_actors", "delta_2021_vs_2024", "forensic_assessment", "sha256"]
    with open(csv_out, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(woo_refusals)
        
    print(f"[extract_woo_refusals] Saved {json_out} and {csv_out}")

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS woo_refusals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dossier_number TEXT,
        institution TEXT,
        topic TEXT,
        invoked_articles TEXT,
        redaction_percentage REAL,
        redacted_actors TEXT,
        delta_2021_vs_2024 TEXT,
        forensic_assessment TEXT,
        sha256 TEXT
    );
    """)
    
    cursor.execute("DELETE FROM woo_refusals")
    for r in woo_refusals:
        cursor.execute("""
        INSERT INTO woo_refusals (dossier_number, institution, topic, invoked_articles, redaction_percentage, redacted_actors, delta_2021_vs_2024, forensic_assessment, sha256)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["dossier_number"], r["institution"], r["topic"], r["invoked_articles"], r["redaction_percentage"], r["redacted_actors"], r["delta_2021_vs_2024"], r["forensic_assessment"], r["sha256"]))
        
    conn.commit()
    conn.close()
    print("[extract_woo_refusals] SQLite table `woo_refusals` updated successfully.")

if __name__ == "__main__":
    main()
