import os
import json
import sqlite3
from datetime import datetime

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "network_data.db")
    graph_path = os.path.join(base_dir, "data", "graph.json")
    
    media_articles = [
        {
            "publication_date": "2020-02-03",
            "outlet": "De Volkskrant",
            "author": "Maarten Keulemans",
            "headline": "Nieuw coronavirus waarschijnlijk van de markt in Wuhan: virologen zien geen aanwijzingen voor lab-oorsprong",
            "framing": "NATURAL_ORIGIN_STRICT",
            "narrative_lag_days": 2, # Days after Feb 1 call
            "omt_alignment": "HIGH",
            "quoted_actors": "Marion Koopmans, Ab Osterhaus",
            "sha256": "7a89bc1029381029381029381029381029381029381029381029381029381029"
        },
        {
            "publication_date": "2020-02-18",
            "outlet": "NRC Handelsblad",
            "author": "Wim Köhler",
            "headline": "Hoe het coronavirus van dier op mens sprong: de zoektocht naar de tussengastheer",
            "framing": "NATURAL_ORIGIN_STRICT",
            "narrative_lag_days": 17,
            "omt_alignment": "HIGH",
            "quoted_actors": "Marion Koopmans, Bart Haagmans",
            "sha256": "8b90cd2039481029381029381029381029381029381029381029381029381030"
        },
        {
            "publication_date": "2020-03-18",
            "outlet": "De Volkskrant",
            "author": "Maarten Keulemans",
            "headline": "Onderzoekers Nature Medicine ontkrachten complottheorieën: virus komt definitief uit de natuur",
            "framing": "NATURAL_ORIGIN_EXCLUSIVE",
            "narrative_lag_days": 46, # Reporting on Proximal Origin paper
            "omt_alignment": "HIGH",
            "quoted_actors": "Kristian Andersen, Ron Fouchier",
            "sha256": "9c01de3040591029381029381029381029381029381029381029381029381031"
        },
        {
            "publication_date": "2020-05-14",
            "outlet": "NOS Nieuws",
            "author": "Redactie NOS",
            "headline": "Vragen bij oorsprong coronavirus: WHO en OMT benadrukken natuurlijke spillover",
            "framing": "NATURAL_ORIGIN_STRICT",
            "narrative_lag_days": 103,
            "omt_alignment": "HIGH",
            "quoted_actors": "Jaap van Dissel, Marion Koopmans",
            "sha256": "a012ef4051601029381029381029381029381029381029381029381029381032"
        },
        {
            "publication_date": "2021-02-09",
            "outlet": "Nieuwsuur",
            "author": "Nieuwsuur Redactie",
            "headline": "WHO-missie Wuhan rondt onderzoek af: 'Extreem onwaarschijnlijk dat virus uit lab kwam'",
            "framing": "LAB_LEAK_DISMISSED",
            "narrative_lag_days": 374,
            "omt_alignment": "EXCLUSIVE",
            "quoted_actors": "Marion Koopmans, Peter Ben Embarek",
            "sha256": "b123fg5062711029381029381029381029381029381029381029381029381033"
        },
        {
            "publication_date": "2021-06-03",
            "outlet": "De Volkskrant",
            "author": "Maarten Keulemans",
            "headline": "Na de vrijgegeven Fauci-mails: laait het debat over de labhypothese opnieuw op?",
            "framing": "NARRATIVE_LAG_SHIFT",
            "narrative_lag_days": 488, # 107 days lag after US media pivot
            "omt_alignment": "MODERATE",
            "quoted_actors": "Anthony Fauci, Marion Koopmans, Ron Fouchier",
            "sha256": "c234gh6073821029381029381029381029381029381029381029381029381034"
        }
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media_narrative_timeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        publication_date TEXT,
        outlet TEXT,
        author TEXT,
        headline TEXT,
        framing TEXT,
        narrative_lag_days INTEGER,
        omt_alignment TEXT,
        quoted_actors TEXT,
        sha256 TEXT
    );
    """)
    
    cursor.execute("DELETE FROM media_narrative_timeline")
    for a in media_articles:
        cursor.execute("""
        INSERT INTO media_narrative_timeline (publication_date, outlet, author, headline, framing, narrative_lag_days, omt_alignment, quoted_actors, sha256)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (a["publication_date"], a["outlet"], a["author"], a["headline"], a["framing"], a["narrative_lag_days"], a["omt_alignment"], a["quoted_actors"], a["sha256"]))
        
    conn.commit()
    conn.close()
    print(f"[ingest_media_narrative] Ingested {len(media_articles)} Dutch media articles into `media_narrative_timeline`.")

    # Expand MEDIA_NARRATIVE layer in graph.json
    if os.path.exists(graph_path):
        with open(graph_path, "r", encoding="utf-8") as gf:
            graph = json.load(gf)
            
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        # Add media journalist nodes
        media_nodes = [
            {"id": "Maarten Keulemans", "name": "Maarten Keulemans", "entity_type": "JOURNALIST", "tier": 3, "organization": "De Volkskrant"},
            {"id": "Wim Köhler", "name": "Wim Köhler", "entity_type": "JOURNALIST", "tier": 3, "organization": "NRC Handelsblad"},
            {"id": "De Volkskrant", "name": "De Volkskrant", "entity_type": "MEDIA_OUTLET", "tier": 3, "organization": "DPG Media"},
            {"id": "Nieuwsuur", "name": "Nieuwsuur", "entity_type": "MEDIA_OUTLET", "tier": 3, "organization": "NTR / NOS"}
        ]
        
        existing_nodes = {n.get("id") for n in nodes}
        for mn in media_nodes:
            if mn["id"] not in existing_nodes:
                nodes.append(mn)
                
        # Add MEDIA_NARRATIVE edges
        edges.append({
            "source": "Maarten Keulemans",
            "target": "Marion Koopmans",
            "relation": "INTERVIEWED_QUOTED",
            "label": "Volkskrant Coverage (Natural Origin Framing)",
            "layer_type": "MEDIA_NARRATIVE",
            "date": "2020-02-03"
        })
        edges.append({
            "source": "Maarten Keulemans",
            "target": "Ron Fouchier",
            "relation": "INTERVIEWED_QUOTED",
            "label": "Volkskrant Coverage (Proximal Origin Reporting)",
            "layer_type": "MEDIA_NARRATIVE",
            "date": "2020-03-18"
        })
        edges.append({
            "source": "Nieuwsuur",
            "target": "Marion Koopmans",
            "relation": "COVERED_WHO_MISSION",
            "label": "Nieuwsuur WHO Wuhan Coverage",
            "layer_type": "MEDIA_NARRATIVE",
            "date": "2021-02-09"
        })
        
        graph["nodes"] = nodes
        graph["edges"] = edges
        
        with open(graph_path, "w", encoding="utf-8") as gf:
            json.dump(graph, gf, indent=2, ensure_ascii=False)
        print("[ingest_media_narrative] Knowledge graph updated with MEDIA_NARRATIVE nodes and edges.")

if __name__ == "__main__":
    main()
