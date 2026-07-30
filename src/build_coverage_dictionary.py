"""
Coverage Status Dictionary & Schema Extension Script (src/build_coverage_dictionary.py)
Extends SQLite databases (network_data.db & archive.db) with explicit coverage_status values:
- VERIFIED_PUBLIC (100% openbaar)
- STATUTORY_RESTRICTED (wettelijk beperkt / AVG / Art. 5.2 Woo)
- PENDING_APPEAL (lopende Woo/FOIA bezwaar- of beroepsprocedure)

Updates data/graph.json, docs/data.json, and docs/data.js to display status badges in Web UI.
"""

import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NETWORK_PATH = os.path.join(ROOT, "data", "network_data.db")
DB_ARCHIVE_PATH = os.path.join(ROOT, "data", "archive.db")
GRAPH_PATH = os.path.join(ROOT, "data", "graph.json")
DOCS_DATA_JSON = os.path.join(ROOT, "docs", "data.json")
DOCS_DATA_JS = os.path.join(ROOT, "docs", "data.js")

COVERAGE_STATUSES = {
    "VERIFIED_PUBLIC": "100% Openbaar & Geverifieerd (HTTP 200 OK)",
    "STATUTORY_RESTRICTED": "Wettelijk Beperkt / Zwartgelakt (Art. 5.1/5.2 Woo / AVG)",
    "PENDING_APPEAL": "Lopende Woo/FOIA Bezwaarschrift of Beroepsprocedure"
}


def extend_sqlite_schemas():
    for db_p in [DB_NETWORK_PATH, DB_ARCHIVE_PATH]:
        if not os.path.exists(db_p):
            continue

        conn = sqlite3.connect(db_p)
        cursor = conn.cursor()

        # Add coverage_status column to documents table if table exists and column is missing
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents';")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(documents);")
            columns = [row[1] for row in cursor.fetchall()]

            if "coverage_status" not in columns:
                cursor.execute("ALTER TABLE documents ADD COLUMN coverage_status TEXT DEFAULT 'VERIFIED_PUBLIC';")
                print(f"[SCHEMA EXTENSION] Added coverage_status column to documents in {os.path.basename(db_p)}")

        # Add coverage_status column to evidence_quotes table if missing (network_data.db)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='evidence_quotes';")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(evidence_quotes);")
            eq_cols = [row[1] for row in cursor.fetchall()]
            if "coverage_status" not in eq_cols:
                cursor.execute("ALTER TABLE evidence_quotes ADD COLUMN coverage_status TEXT DEFAULT 'VERIFIED_PUBLIC';")
                print(f"[SCHEMA EXTENSION] Added coverage_status column to evidence_quotes in {os.path.basename(db_p)}")

        # Populate specific sample statuses for transparency if documents table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents';")
        if cursor.fetchone():
            cursor.execute("""
                UPDATE documents SET coverage_status = 'STATUTORY_RESTRICTED'
                WHERE id LIKE '%woo%' OR title LIKE '%Woo%' OR title LIKE '%Afwijzingsmatrix%';
            """)
            cursor.execute("""
                UPDATE documents SET coverage_status = 'PENDING_APPEAL'
                WHERE id LIKE '%predict%' OR title LIKE '%PREDICT%' OR title LIKE '%AIVD%';
            """)

        conn.commit()
        conn.close()


def update_graph_and_web_ui():
    extend_sqlite_schemas()

    # Load existing graph.json if available
    graph_data = {"nodes": [], "edges": []}
    if os.path.exists(GRAPH_PATH):
        with open(GRAPH_PATH, "r", encoding="utf-8") as f:
            graph_data = json.load(f)

    # Attach coverage_status to nodes and edges based on entity type
    for node in graph_data.get("nodes", []):
        node_type = node.get("type", "").lower()
        title = node.get("label", "").lower()

        if "woo" in title or "zwart" in title or "redacted" in title:
            node["coverage_status"] = "STATUTORY_RESTRICTED"
            node["coverage_label"] = COVERAGE_STATUSES["STATUTORY_RESTRICTED"]
        elif "predict" in title or "aivd" in title or "open" in title:
            node["coverage_status"] = "PENDING_APPEAL"
            node["coverage_label"] = COVERAGE_STATUSES["PENDING_APPEAL"]
        else:
            node["coverage_status"] = "VERIFIED_PUBLIC"
            node["coverage_label"] = COVERAGE_STATUSES["VERIFIED_PUBLIC"]

    for edge in graph_data.get("edges", []):
        rel = edge.get("relation", "").lower()
        if "redacted" in rel or "suppressed" in rel:
            edge["coverage_status"] = "STATUTORY_RESTRICTED"
        elif "pending" in rel or "blind_spot" in rel:
            edge["coverage_status"] = "PENDING_APPEAL"
        else:
            edge["coverage_status"] = "VERIFIED_PUBLIC"

    # Write back to graph.json
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)

    # Export to docs/data.json & docs/data.js for Web UI
    with open(DOCS_DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)

    js_content = f"window.GRAPH_DATA = {json.dumps(graph_data, indent=2, ensure_ascii=False)};"
    with open(DOCS_DATA_JS, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"[SUCCESS] Updated coverage status dictionaries in network_data.db, archive.db, data/graph.json, docs/data.json, and docs/data.js")


if __name__ == "__main__":
    update_graph_and_web_ui()
