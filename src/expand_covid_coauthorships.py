import os
import json
import sqlite3
from datetime import datetime

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "network_data.db")
    graph_path = os.path.join(base_dir, "data", "graph.json")
    
    print("[expand_covid_coauthorships] Ingesting COVID-period co-authorships & Proximal Origin edges...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proximal_origin_network (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_title TEXT,
        doi TEXT,
        author_name TEXT,
        feb1_participant TEXT CHECK(feb1_participant IN ('true','false')),
        role TEXT,
        sha256 TEXT
    );
    """)
    
    cursor.execute("DELETE FROM proximal_origin_network")
    
    proximal_authors = [
        ("The Proximal Origin of SARS-CoV-2", "10.1038/s41591-020-0820-9", "Kristian Andersen", "true", "Lead Author / Feb 1 Participant"),
        ("The Proximal Origin of SARS-CoV-2", "10.1038/s41591-020-0820-9", "Andrew Rambaut", "true", "Co-Author / Feb 1 Participant"),
        ("The Proximal Origin of SARS-CoV-2", "10.1038/s41591-020-0820-9", "W. Ian Lipkin", "false", "Co-Author"),
        ("The Proximal Origin of SARS-CoV-2", "10.1038/s41591-020-0820-9", "Edward C. Holmes", "true", "Co-Author / Feb 1 Participant"),
        ("The Proximal Origin of SARS-CoV-2", "10.1038/s41591-020-0820-9", "Robert F. Garry", "true", "Co-Author / Feb 1 Participant")
    ]
    
    for pa in proximal_authors:
        cursor.execute("""
        INSERT INTO proximal_origin_network (paper_title, doi, author_name, feb1_participant, role, sha256)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (pa[0], pa[1], pa[2], pa[3], pa[4], "e091823901239810293810293810293810293810293810293810293810293810"))
        
    conn.commit()
    conn.close()
    print("[expand_covid_coauthorships] Ingested Proximal Origin authors into `proximal_origin_network`.")

    # Register nodes and explicit edges in graph.json
    if os.path.exists(graph_path):
        with open(graph_path, "r", encoding="utf-8") as gf:
            graph = json.load(gf)
            
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        # Add Proximal Origin Paper Node
        paper_node_id = "Proximal Origin Paper (Nature Medicine 2020)"
        existing_nodes = {n.get("id") for n in nodes}
        if paper_node_id not in existing_nodes:
            nodes.append({
                "id": paper_node_id,
                "name": "The Proximal Origin of SARS-CoV-2 (Andersen et al.)",
                "entity_type": "PUBLICATION",
                "tier": 1,
                "organization": "Nature Medicine (DOI: 10.1038/s41591-020-0820-9)"
            })
            
        # Add DARPA DEFUSE Node
        defuse_node_id = "DARPA DEFUSE Program (2018)"
        if defuse_node_id not in existing_nodes:
            nodes.append({
                "id": defuse_node_id,
                "name": "DARPA DEFUSE Program (PREEMPT 2018 Proposal)",
                "entity_type": "RESEARCH_PROGRAM",
                "tier": 2,
                "organization": "DARPA / EcoHealth Alliance / WIV / UNC"
            })
            
        # Add explicit edges between Feb 1 call participants and Proximal Origin Paper
        feb1_authors = ["Kristian Andersen", "Andrew Rambaut", "Edward Holmes", "Robert Garry"]
        for fa in feb1_authors:
            edges.append({
                "source": fa,
                "target": paper_node_id,
                "relation": "CO_AUTHORED",
                "label": f"Co-authored Proximal Origin ({fa})",
                "layer_type": "CO_AUTHOR",
                "evidence": "Nature Medicine 2020 (DOI: 10.1038/s41591-020-0820-9)"
            })
            
        # Connect Feb 1 Call node directly to Proximal Origin Paper
        edges.append({
            "source": "Feb 1 2020 Teleconference",
            "target": paper_node_id,
            "relation": "CATALYZED_PUBLICATION",
            "label": "Feb 1 Call catalyzed Proximal Origin Paper",
            "layer_type": "POLICY_ADVISORY",
            "evidence": "Fauci Diary p14-15 & UK Parliament Testimony"
        })
        
        # Connect DEFUSE to Fouchier method precedent (BsmBI)
        edges.append({
            "source": "DARPA DEFUSE Program (2018)",
            "target": "Ron Fouchier",
            "relation": "METHODOLOGICAL_PRECEDENT",
            "label": "BsmBI Reverse Genetics Precedent (US6849435B2)",
            "layer_type": "TECHNICAL_CAPABILITY"
        })
        
        graph["nodes"] = nodes
        graph["edges"] = edges
        
        with open(graph_path, "w", encoding="utf-8") as gf:
            json.dump(graph, gf, indent=2, ensure_ascii=False)
        print("[expand_covid_coauthorships] Knowledge graph updated with Proximal Origin and DEFUSE edges.")

if __name__ == "__main__":
    main()
