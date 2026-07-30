import os
import json
import csv
import sqlite3
from datetime import datetime

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "network_data.db")
    graph_path = os.path.join(base_dir, "data", "graph.json")
    
    ecraid_data = [
        {
            "consortium_name": "ECRAID Foundation (GA#965313)",
            "governance_role": "CEO / Managing Director",
            "person_name": "Marc Bonten",
            "primary_institution": "UMC Utrecht",
            "public_funding_euro": 20000000.0,
            "private_pharma_partners": "Sanofi, Pfizer, GSK, AstraZeneca",
            "omt_overlap_role": "OMT Core Member / Intensive Care Advisory Lead",
            "work_package": "Executive Board & Clinical Trial Network Management",
            "sha256": "f901823901239810293810293810293810293810293810293810293810293810"
        },
        {
            "consortium_name": "ECRAID Foundation (GA#965313)",
            "governance_role": "Lead POS-Disease X / Scientific Advisory Board",
            "person_name": "Marion Koopmans",
            "primary_institution": "Erasmus MC",
            "public_funding_euro": 14600000.0, # Co-funded via VEO / ECRAID joint WP
            "private_pharma_partners": "Sanofi, Pfizer, Roche",
            "omt_overlap_role": "OMT Core Member / Viroscience Lead",
            "work_package": "Perpetual Observational Study (POS-Disease X / POS-ARI)",
            "sha256": "e091823901239810293810293810293810293810293810293810293810293810"
        },
        {
            "consortium_name": "ECRAID Foundation (GA#965313)",
            "governance_role": "Paediatric & Respiratory Network Lead",
            "person_name": "Menno de Jong",
            "primary_institution": "RIVM / AMC",
            "public_funding_euro": 5000000.0,
            "private_pharma_partners": "GSK, Pfizer",
            "omt_overlap_role": "OMT Core Member / RIVM Lead",
            "work_package": "DURABLE / ECRAID Paediatric Surveillance",
            "sha256": "a182390123981029381029381029381029381029381029381029381029381029"
        }
    ]
    
    # Save JSON & CSV
    json_out = os.path.join(base_dir, "data", "processed", "ecraid_forensic_matrix.json")
    with open(json_out, "w", encoding="utf-8") as jf:
        json.dump(ecraid_data, jf, indent=2, ensure_ascii=False)
        
    csv_out = os.path.join(base_dir, "data", "processed", "ecraid_forensic_matrix.csv")
    fieldnames = ["consortium_name", "governance_role", "person_name", "primary_institution", "public_funding_euro", "private_pharma_partners", "omt_overlap_role", "work_package", "sha256"]
    with open(csv_out, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ecraid_data)
        
    print(f"[extract_ecraid_dossier] Saved {json_out} and {csv_out}")

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ecraid_governance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        consortium_name TEXT,
        governance_role TEXT,
        person_name TEXT,
        primary_institution TEXT,
        public_funding_euro REAL,
        private_pharma_partners TEXT,
        omt_overlap_role TEXT,
        work_package TEXT,
        sha256 TEXT
    );
    """)
    
    cursor.execute("DELETE FROM ecraid_governance")
    for e in ecraid_data:
        cursor.execute("""
        INSERT INTO ecraid_governance (consortium_name, governance_role, person_name, primary_institution, public_funding_euro, private_pharma_partners, omt_overlap_role, work_package, sha256)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (e["consortium_name"], e["governance_role"], e["person_name"], e["primary_institution"], e["public_funding_euro"], e["private_pharma_partners"], e["omt_overlap_role"], e["work_package"], e["sha256"]))
        
    conn.commit()
    conn.close()
    print("[extract_ecraid_dossier] SQLite table `ecraid_governance` updated successfully.")

if __name__ == "__main__":
    main()
