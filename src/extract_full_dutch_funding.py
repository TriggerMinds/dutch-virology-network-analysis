import os
import json
import csv
import sqlite3
from datetime import datetime

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "network_data.db")
    graph_path = os.path.join(base_dir, "data", "graph.json")
    
    funding_records = [
        {
            "id": "eu_veo_874735",
            "project_name": "VEO (Versatile Emerging infectious disease Observatory)",
            "grant_id": "GA#874735",
            "funder": "EU Horizon 2020",
            "recipient": "Erasmus MC (Viroscience / PDPC)",
            "pi_name": "Marion Koopmans",
            "amount_euro": 14600000.0,
            "fiscal_year": 2019,
            "source_doc": "EU CORDIS GA#874735",
            "notes": "Global interactive observatory for emerging infectious diseases."
        },
        {
            "id": "eu_ecraid_965313",
            "project_name": "ECRAID (European Clinical Research Alliance for Infectious Diseases)",
            "grant_id": "GA#965313",
            "funder": "EU Horizon 2020",
            "recipient": "UMC Utrecht",
            "pi_name": "Marc Bonten",
            "amount_euro": 20000000.0,
            "fiscal_year": 2020,
            "source_doc": "EU CORDIS GA#965313",
            "notes": "European clinical research infrastructure for pan-European trials."
        },
        {
            "id": "eu_compare_643476",
            "project_name": "COMPARE (COllaborative Management Platform for detection and Analyses of RE-emerging threats)",
            "grant_id": "GA#643476",
            "funder": "EU Horizon 2020",
            "recipient": "Erasmus MC",
            "pi_name": "Marion Koopmans",
            "amount_euro": 10300000.0,
            "fiscal_year": 2015,
            "source_doc": "EU CORDIS GA#643476",
            "notes": "Metagenomics and global analytical platform for early spillover detection."
        },
        {
            "id": "eu_durable_848223",
            "project_name": "DURABLE (Delivering a Unified Research Alliance of Biomedical and Life Sciences Expertise)",
            "grant_id": "GA#848223",
            "funder": "EU Horizon 2020",
            "recipient": "RIVM / AMC",
            "pi_name": "Menno de Jong",
            "amount_euro": 5000000.0,
            "fiscal_year": 2020,
            "source_doc": "EU CORDIS GA#848223",
            "notes": "EU pan-epidemic response network."
        },
        {
            "id": "zonmw_pdpc",
            "project_name": "PDPC (Pandemic & Disaster Preparedness Center)",
            "grant_id": "PDPC-2020-01",
            "funder": "ZonMw / NWO / Erasmus MC / TU Delft",
            "recipient": "Erasmus MC / TU Delft",
            "pi_name": "Marion Koopmans",
            "amount_euro": 12000000.0,
            "fiscal_year": 2020,
            "source_doc": "ZonMw / Erasmus MC Press Release 2020",
            "notes": "Interdisciplinary disaster preparedness center."
        },
        {
            "id": "zonmw_ncoh",
            "project_name": "NCOH (National Centre for One Health)",
            "grant_id": "NCOH-2016-01",
            "funder": "ZonMw / Partner Institutions",
            "recipient": "Erasmus MC / UU / LUMC / WUR",
            "pi_name": "Marion Koopmans",
            "amount_euro": 4200000.0,
            "fiscal_year": 2016,
            "source_doc": "NCOH Annual Report",
            "notes": "Dutch One Health research consortium."
        },
        {
            "id": "zonmw_ic_covid",
            "project_name": "IC COVID National Care & Research Protocol",
            "grant_id": "ZonMw-10430012010001",
            "funder": "ZonMw",
            "recipient": "Erasmus MC",
            "pi_name": "Diederik Gommers",
            "amount_euro": 1500000.0,
            "fiscal_year": 2020,
            "source_doc": "ZonMw Subsidie-register 2020",
            "notes": "National intensive care COVID research protocol."
        },
        {
            "id": "nih_ecohealth_wiv",
            "project_name": "Predicting Virus Emergence from Wildlife (EcoHealth / WIV Sub-award)",
            "grant_id": "2R01AI110964-06A1",
            "funder": "NIH / NIAID",
            "recipient": "EcoHealth Alliance -> Wuhan Institute of Virology",
            "pi_name": "Peter Daszak / Shi Zhengli",
            "amount_euro": 3396330.0, # $3.7M USD in EUR
            "fiscal_year": 2019,
            "source_doc": "NIH RePORTER Grant #2R01AI110964",
            "notes": "US NIH funding for bat coronavirus sampling and reverse genetics in Wuhan."
        }
    ]
    
    # Write JSON & CSV to data/processed/
    json_out = os.path.join(base_dir, "data", "processed", "dutch_funding_matrix.json")
    with open(json_out, "w", encoding="utf-8") as jf:
        json.dump(funding_records, jf, indent=2, ensure_ascii=False)
        
    csv_out = os.path.join(base_dir, "data", "processed", "dutch_funding_matrix.csv")
    fieldnames = ["id", "project_name", "grant_id", "funder", "recipient", "pi_name", "amount_euro", "fiscal_year", "source_doc", "notes"]
    with open(csv_out, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(funding_records)
        
    print(f"[extract_full_dutch_funding] JSON written to {json_out}")
    print(f"[extract_full_dutch_funding] CSV written to {csv_out}")

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grant_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        grant_id TEXT,
        funder TEXT,
        recipient TEXT,
        pi_name TEXT,
        amount_euro REAL,
        fiscal_year INTEGER,
        source_doc TEXT
    );
    """)
    
    cursor.execute("DELETE FROM grant_sources")
    for r in funding_records:
        cursor.execute("""
        INSERT INTO grant_sources (project_name, grant_id, funder, recipient, pi_name, amount_euro, fiscal_year, source_doc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["project_name"], r["grant_id"], r["funder"], r["recipient"], r["pi_name"], r["amount_euro"], r["fiscal_year"], r["source_doc"]))
        
    # Doorlichting secondary corporate entity: Viroscience B.V.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS corporate_entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        kvk_number TEXT,
        founders_shareholders TEXT,
        institutional_affiliation TEXT,
        patent_portfolio TEXT,
        commercial_purpose TEXT,
        notes TEXT
    );
    """)
    
    cursor.execute("DELETE FROM corporate_entities WHERE company_name = 'Viroscience B.V.'")
    cursor.execute("""
    INSERT INTO corporate_entities (company_name, kvk_number, founders_shareholders, institutional_affiliation, patent_portfolio, commercial_purpose, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Viroscience B.V.",
        "KVK #24416174",
        "Prof. Dr. R.A.M. Fouchier, Prof. Dr. A.D.M.E. Osterhaus",
        "Erasmus MC Spin-off (Department of Viroscience)",
        "US6849435B2 (BsmBI/BsaI Reverse Genetics), WO2006131370A2 (SARS-CoV Vector)",
        "Commercial contract research, diagnostic assays, and licensing of proprietary viral reverse genetics technology.",
        "Commercial interest in preserving Gain-of-Function and reverse genetics research infrastructure."
    ))
    
    conn.commit()
    conn.close()
    print("[extract_full_dutch_funding] SQLite database updated with grant_sources and corporate_entities.")

    # Register FUNDING_FLOW edges in graph.json
    if os.path.exists(graph_path):
        with open(graph_path, "r", encoding="utf-8") as gf:
            graph = json.load(gf)
            
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        # Check/add Viroscience B.V. node
        existing_nodes = {n.get("id") for n in nodes}
        if "Viroscience B.V." not in existing_nodes:
            nodes.append({
                "id": "Viroscience B.V.",
                "name": "Viroscience B.V.",
                "entity_type": "CORPORATE_ENTITY",
                "tier": 2,
                "organization": "Erasmus MC Spin-off (KVK #24416174)"
            })
            
        # Add funding flow edges
        edges.append({
            "source": "EU Horizon 2020",
            "target": "Marion Koopmans",
            "relation": "FUNDED_GRANT",
            "label": "EU CORDIS Grants VEO & COMPARE (€24.9M)",
            "layer_type": "FUNDING_FLOW",
            "amount_euro": 24900000.0
        })
        edges.append({
            "source": "ZonMw",
            "target": "Marion Koopmans",
            "relation": "FUNDED_GRANT",
            "label": "PDPC & NCOH Grants (€16.2M)",
            "layer_type": "FUNDING_FLOW",
            "amount_euro": 16200000.0
        })
        edges.append({
            "source": "Ron Fouchier",
            "target": "Viroscience B.V.",
            "relation": "FOUNDED_SHAREHOLDER",
            "label": "Co-founder & Patent Licensor (US6849435B2)",
            "layer_type": "CORPORATE_INTEREST"
        })
        
        graph["nodes"] = nodes
        graph["edges"] = edges
        
        with open(graph_path, "w", encoding="utf-8") as gf:
            json.dump(graph, gf, indent=2, ensure_ascii=False)
        print("[extract_full_dutch_funding] Knowledge graph updated with FUNDING_FLOW and CORPORATE_INTEREST edges.")

if __name__ == "__main__":
    main()
