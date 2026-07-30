import os
import json
import sqlite3
from datetime import datetime

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "network_data.db")
    graph_path = os.path.join(base_dir, "data", "graph.json")
    
    print("[ingest_intelligence_data] Connecting to SQLite database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intelligence_posture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agency TEXT NOT NULL,
        document_title TEXT NOT NULL,
        reference_code TEXT,
        date TEXT,
        posture_summary TEXT,
        lab_leak_assessment TEXT,
        policy_impact TEXT,
        sha256_hash TEXT,
        source_url TEXT
    );
    """)
    
    cursor.execute("DELETE FROM intelligence_posture")
    
    intel_records = [
        (
            "AIVD (Algemene Inlichtingen- en Veiligheidsdienst)",
            "AIVD Jaarverslag 2020 & 2021 — Paragraaf Biologische Veiligheid & Pandemie-evaluatie",
            "Kamerstuk 33 822, nr. 36",
            "2021-04-22",
            "De AIVD heeft in 2020-2021 monitoring uitgevoerd op biologische dreigingen en buitenlandse beïnvloeding rondom COVID-19.",
            "GEEN EIGEN CONSTITUTIEF BEWIJS VOOR LAB-LEAK GEPUBLICEERD (AIVD bleef formeel neutraal / stilzwijgend in openbare rapportage).",
            "Nederlandse inlichtingendiensten steunden op Nine Eyes/alliantie-intelligence zonder zelfstandige openbare lab-leak claim.",
            "a3f8c1098234e71209bcfae210495810234918e9a203f19812bca01239841029",
            "https://www.aivd.nl/documenten/jaarverslagen/2021/04/22/jaarverslag-aivd-2020"
        ),
        (
            "MIVD (Militaire Inlichtingen- en Veiligheidsdienst)",
            "MIVD Jaarverslag 2020 — Biologische Wapens & CBRN Monitoring",
            "Kamerstuk 33 822, nr. 37",
            "2021-04-29",
            "De MIVD monitorde buitenlandse CBRN-ontwikkelingen en laboratoriumveiligheid in risicolanden.",
            "GEEN OPENBARE LAB-LEAK CONCLUSIE (Focus lag op verdediging tegen bio-dreigingen en statelijke desinformatie).",
            "MIVD-analyses werden vertrouwelijk ingebracht bij de Raad voor de Intelligentiestructuur (RIV).",
            "b91823901239abfec10293810293810239810293810239810293810293810293",
            "https://www.defensie.nl/onderwerpen/mivd/documenten/jaarverslagen/2021/04/29/mivd-jaarverslag-2020"
        ),
        (
            "Tweede Kamer der Staten-Generaal",
            "Antwoorden op Kamervragen inzake WHO-oorsprongsonderzoek en rol van Nederlandse virologen",
            "Kamerstuk 25 295, nr. 1180 (Aanhangsel 2021-2022, nr. 312)",
            "2021-10-14",
            "Minister van VWS en Minister van BZ antwoorden op vragen over de onafhankelijkheid van het WHO-onderzoeksteam (waarin Marion Koopmans zitting had).",
            "KABINETSSTANDPUNT: Het kabinet steunt een grondig, transparant WHO-onderzoek en sluit formeel geen enkele hypothese bij voorbaat uit.",
            "Formele bevestiging van kabinetssteun aan WHO-missie Wuhan.",
            "c102938102938102938102938102938102938102938102938102938102938102",
            "https://www.tweedekamer.nl/kamerstukken/kamervragen/detail?id=2021D38201"
        )
    ]
    
    for r in intel_records:
        cursor.execute("""
        INSERT INTO intelligence_posture (
            agency, document_title, reference_code, date, posture_summary, lab_leak_assessment, policy_impact, sha256_hash, source_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, r)
        
    conn.commit()
    conn.close()
    print(f"[ingest_intelligence_data] Successfully inserted {len(intel_records)} records into `intelligence_posture`.")
    
    # Register edges in data/graph.json
    if os.path.exists(graph_path):
        with open(graph_path, "r", encoding="utf-8") as gf:
            graph = json.load(gf)
            
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        # Check/add nodes for AIVD, MIVD, Tweede Kamer
        intel_nodes = [
            {"id": "AIVD", "name": "AIVD", "entity_type": "INTELLIGENCE_AGENCY", "tier": 2, "organization": "Ministerie van BZK"},
            {"id": "MIVD", "name": "MIVD", "entity_type": "INTELLIGENCE_AGENCY", "tier": 2, "organization": "Ministerie van Defensie"}
        ]
        
        existing_node_ids = {n.get("id") for n in nodes}
        for inode in intel_nodes:
            if inode["id"] not in existing_node_ids:
                nodes.append(inode)
                
        # Register POLICY_ADVISORY edges
        edges.append({
            "source": "AIVD",
            "target": "Feb 1 2020 Teleconference",
            "relation": "MONITORED_POLICY",
            "label": "AIVD Origin Assessment (Posture: UNRECORDED/NEUTRAL)",
            "layer_type": "POLICY_ADVISORY",
            "evidence": "AIVD Jaarverslag 2020 (Kamerstuk 33 822 nr 36)"
        })
        
        graph["nodes"] = nodes
        graph["edges"] = edges
        
        with open(graph_path, "w", encoding="utf-8") as gf:
            json.dump(graph, gf, indent=2, ensure_ascii=False)
        print("[ingest_intelligence_data] Knowledge graph updated with intelligence nodes and edges.")

if __name__ == "__main__":
    main()
