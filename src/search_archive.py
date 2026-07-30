"""
Multi-Lingual Search & Filter Module for data/archive.db (FTS5 + Taxonomy + Hash Provenance)
"""

import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "archive.db")


def search_by_keyword(query, language_code=None, jurisdiction=None, db_path=DB_PATH):
    """
    Search full-text document content using SQLite FTS5 index.
    Supports optional filters on ISO language_code and jurisdiction (NL, DE, FR, ES, IT, EU, US).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = """
        SELECT d.id, d.title, d.original_filename, d.jurisdiction, d.language_code,
               d.publication_date, d.sha256_hash, snippet(fts_document_texts, 1, '<b>', '</b>', '...', 30) AS snippet
        FROM fts_document_texts fts
        JOIN documents d ON fts.document_id = d.id
        WHERE fts_document_texts MATCH ?
    """
    params = [query]

    if language_code:
        sql += " AND d.language_code = ?"
        params.append(language_code)

    if jurisdiction:
        sql += " AND d.jurisdiction = ?"
        params.append(jurisdiction)

    sql += " ORDER BY rank LIMIT 50;"

    cursor.execute(sql, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def search_by_topic(topic_code, date_from=None, date_to=None, db_path=DB_PATH):
    """
    Retrieve documents mapped to a specific multi-lingual taxonomy topic.
    Supports optional publication_date filtering (date_from, date_to).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = """
        SELECT d.id, d.title, d.jurisdiction, d.language_code, d.publication_date, d.sha256_hash,
               t.label_nl, t.label_de, t.label_fr, t.label_en
        FROM documents d
        JOIN document_topics dt ON d.id = dt.document_id
        JOIN taxonomy_topics t ON dt.topic_code = t.topic_code
        WHERE dt.topic_code = ?
    """
    params = [topic_code]

    if date_from:
        sql += " AND d.publication_date >= ?"
        params.append(date_from)

    if date_to:
        sql += " AND d.publication_date <= ?"
        params.append(date_to)

    sql += " ORDER BY d.publication_date DESC;"

    cursor.execute(sql, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_document_history(document_id, db_path=DB_PATH):
    """
    Retrieve full version history, timestamps, and SHA-256 hashes for a specific document.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.version_id, v.document_id, v.version_number, v.release_date, v.sha256_hash, v.changes_description,
               d.title, d.original_filename
        FROM document_versions v
        JOIN documents d ON v.document_id = d.id
        WHERE v.document_id = ?
        ORDER BY v.version_number ASC;
    """, (document_id,))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


if __name__ == "__main__":
    print("[INFO] Running demo search on data/archive.db...")
    res = search_by_keyword("Fauci OR Koopmans OR Fouchier")
    print(f"Keyword search results: {len(res)} matches found.")
    for r in res[:5]:
        print(f" - [{r['jurisdiction']}] {r['title']} (Hash: {r['sha256_hash'][:10]}...)")
