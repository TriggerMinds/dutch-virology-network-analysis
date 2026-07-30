import os
import json
import sqlite3
from datetime import datetime

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "network_data.db")
    json_mentions_path = os.path.join(base_dir, "data", "processed", "koopmans_feb1_mentions.json")
    graph_path = os.path.join(base_dir, "data", "graph.json")
    
    if not os.path.exists(json_mentions_path):
        print(f"Mentions JSON not found at {json_mentions_path}. Run extraction first.")
        return

    with open(json_mentions_path, "r", encoding="utf-8") as f:
        mentions = json.load(f)
        
    print(f"Connecting to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Ensure table koopmans_feb1_audit exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS koopmans_feb1_audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_file TEXT NOT NULL,
        page INTEGER,
        quote TEXT,
        speaker TEXT,
        position_indicated TEXT CHECK(position_indicated IN ('true','false','unknown')),
        redaction_flag TEXT,
        sha256_source TEXT,
        extracted_at TEXT,
        notes TEXT
    );
    """)
    
    # Clear previous audit entries to avoid duplicates on re-runs
    cursor.execute("DELETE FROM koopmans_feb1_audit")
    
    for m in mentions:
        cursor.execute("""
        INSERT INTO koopmans_feb1_audit (
            source_file, page, quote, speaker, position_indicated, redaction_flag, sha256_source, extracted_at, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m["source"],
            m["page"],
            m["quote"],
            m["speaker"],
            m["position_indicated"],
            m["redaction_flag"],
            m["sha256_source"],
            m["extracted_at"],
            m["position_notes"]
        ))
        
    # 2. Update informal_interactions table
    cursor.execute("DELETE FROM informal_interactions WHERE entity_name = 'Marion Koopmans' AND paper_title LIKE '%Feb 1 2020%'")
    cursor.execute("""
    INSERT INTO informal_interactions (
        entity_name, paper_title, interaction_type, date, source_doc, page_num
    ) VALUES (
        'Marion Koopmans', 'Feb 1 2020 Teleconference (Farrar/Fauci Call)', 'UNRECORDED_PARTICIPATION (BLIND_SPOT)', '2020-02-01',
        'data/raw/fauci_diary/2026.07.24_Tonys-Diary-Package.pdf', '14'
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"Successfully inserted {len(mentions)} records into SQLite `koopmans_feb1_audit` and updated `informal_interactions`.")
    
    # 3. Update data/graph.json
    if os.path.exists(graph_path):
        print(f"Updating knowledge graph at {graph_path}...")
        with open(graph_path, "r", encoding="utf-8") as gf:
            graph = json.load(gf)
            
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        koopmans_node = None
        for n in nodes:
            if n.get("id") == "Marion Koopmans" or n.get("name") == "Marion Koopmans" or "Koopmans" in n.get("id", ""):
                koopmans_node = n
                break
                
        if koopmans_node:
            koopmans_node["feb1_2020_position_status"] = "UNKNOWN"
            koopmans_node["feb1_2020_attendance"] = "CONFIRMED_FAUCI_DIARY_P14"
            koopmans_node["blind_spot_flag"] = True
            
        edge_exists = False
        for e in edges:
            if (e.get("source") == "Marion Koopmans" or e.get("target") == "Marion Koopmans") and "Feb 1" in str(e.get("label", "")):
                e["stance"] = "UNKNOWN"
                e["status"] = "BLIND_SPOT"
                edge_exists = True
                break
                
        if not edge_exists:
            edges.append({
                "source": "Marion Koopmans",
                "target": "Feb 1 2020 Teleconference",
                "relation": "PARTICIPATED_IN",
                "label": "Feb 1 Teleconference (Stance: UNKNOWN)",
                "stance": "UNKNOWN",
                "status": "BLIND_SPOT",
                "evidence": "Fauci Diary Release 2026, p14"
            })
            
        graph["nodes"] = nodes
        graph["edges"] = edges
        
        with open(graph_path, "w", encoding="utf-8") as gf:
            json.dump(graph, gf, indent=2, ensure_ascii=False)
        print("Knowledge graph successfully updated with explicit BLIND_SPOT status.")

if __name__ == "__main__":
    main()
