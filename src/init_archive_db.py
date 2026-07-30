"""
Database Schema Initialization Script for Multi-Language Document Archive (data/archive.db)
Equipped with FTS5 Full-Text Search, SHA-256 Provenance Tracking, and EuroVoc Taxonomy.
"""

import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "archive.db")


def init_db(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        original_filename TEXT NOT NULL,
        jurisdiction TEXT NOT NULL,
        issuing_agency TEXT,
        document_type TEXT,
        event_date TEXT,
        publication_date TEXT,
        language_code TEXT NOT NULL DEFAULT 'nl',
        sha256_hash TEXT UNIQUE NOT NULL,
        source_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. document_texts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_texts (
        document_id TEXT PRIMARY KEY,
        full_text TEXT NOT NULL,
        page_count INTEGER DEFAULT 0,
        has_ocr BOOLEAN DEFAULT 0,
        FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
    );
    """)

    # 3. taxonomy_topics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS taxonomy_topics (
        topic_code TEXT PRIMARY KEY,
        label_nl TEXT NOT NULL,
        label_de TEXT NOT NULL,
        label_fr TEXT NOT NULL,
        label_en TEXT NOT NULL
    );
    """)

    # 4. document_topics mapping table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_topics (
        document_id TEXT NOT NULL,
        topic_code TEXT NOT NULL,
        PRIMARY KEY (document_id, topic_code),
        FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
        FOREIGN KEY (topic_code) REFERENCES taxonomy_topics(topic_code) ON DELETE CASCADE
    );
    """)

    # 5. document_versions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_versions (
        version_id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        version_number INTEGER NOT NULL,
        release_date TEXT,
        sha256_hash TEXT NOT NULL,
        changes_description TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
    );
    """)

    # 6. FTS5 Virtual Table for document_texts
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS fts_document_texts USING fts5(
        document_id UNINDEXED,
        full_text,
        content='document_texts',
        content_rowid='rowid'
    );
    """)

    # FTS5 Triggers to maintain sync with document_texts
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS document_texts_ai AFTER INSERT ON document_texts BEGIN
        INSERT INTO fts_document_texts(rowid, document_id, full_text)
        VALUES (new.rowid, new.document_id, new.full_text);
    END;
    """)

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS document_texts_ad AFTER DELETE ON document_texts BEGIN
        INSERT INTO fts_document_texts(fts_document_texts, rowid, document_id, full_text)
        VALUES('delete', old.rowid, old.document_id, old.full_text);
    END;
    """)

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS document_texts_au AFTER UPDATE ON document_texts BEGIN
        INSERT INTO fts_document_texts(fts_document_texts, rowid, document_id, full_text)
        VALUES('delete', old.rowid, old.document_id, old.full_text);
        INSERT INTO fts_document_texts(rowid, document_id, full_text)
        VALUES (new.rowid, new.document_id, new.full_text);
    END;
    """)

    # Standard set of neutral taxonomy topics
    default_topics = [
        (
            "TOPIC_ADVISORY_MINUTES",
            "Notulen & Adviezen",
            "Beraterprotokolle & Empfehlungen",
            "Procès-verbaux & Avis",
            "Advisory Minutes & Guidance",
        ),
        (
            "TOPIC_DIAGNOSTICS",
            "Diagnostiek & Testprotocollen",
            "Diagnostik & Testprotokolle",
            "Diagnostics & Protocoles de test",
            "Diagnostics & Test Protocols",
        ),
        (
            "TOPIC_EMERGENCY_PROCUREMENT",
            "Nood-inkoop & Contracten",
            "Notfallbeschaffung & Verträge",
            "Marchés d'urgence & Contrats",
            "Emergency Procurement & Contracts",
        ),
        (
            "TOPIC_POLICY_DIRECTIVES",
            "Beleidsrichtlijnen",
            "Politikrichtlinien",
            "Directives politiques",
            "Policy Directives",
        ),
        (
            "TOPIC_FINANCIAL_GRANTS",
            "Subsidies & Toekenningen",
            "Zuschüsse & Fördermittel",
            "Subventions & Allocations",
            "Financial Grants & Allocations",
        ),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO taxonomy_topics (topic_code, label_nl, label_de, label_fr, label_en)
        VALUES (?, ?, ?, ?, ?);
    """,
        default_topics,
    )

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Database schema initialized at {db_path}")


if __name__ == "__main__":
    init_db()
