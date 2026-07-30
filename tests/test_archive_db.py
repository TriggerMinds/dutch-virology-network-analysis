"""
Unit Tests for Multi-Language Document Archive Database (data/archive.db)
Validates Schema Creation, SHA-256 Deduplication, FTS5 Search Queries, Topic Filtering, and Version Tracking.
"""

import os
import sqlite3
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from init_archive_db import init_db
from ingest_pdf_archive import ingest_pdf_file
from search_archive import get_document_history, search_by_keyword, search_by_topic

TEST_DB_PATH = os.path.join(ROOT, "data", "test_archive.db")


class TestArchiveDB(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        init_db(db_path=TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_schema_initialization(self):
        conn = sqlite3.connect(TEST_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("documents", tables)
        self.assertIn("document_texts", tables)
        self.assertIn("taxonomy_topics", tables)
        self.assertIn("document_topics", tables)
        self.assertIn("document_versions", tables)
        self.assertIn("fts_document_texts", tables)

    def test_taxonomy_topics_default_data(self):
        conn = sqlite3.connect(TEST_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT topic_code FROM taxonomy_topics;")
        topics = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("TOPIC_ADVISORY_MINUTES", topics)
        self.assertIn("TOPIC_DIAGNOSTICS", topics)
        self.assertIn("TOPIC_EMERGENCY_PROCUREMENT", topics)
        self.assertIn("TOPIC_POLICY_DIRECTIVES", topics)
        self.assertIn("TOPIC_FINANCIAL_GRANTS", topics)

    def test_fts5_search_and_deduplication(self):
        conn = sqlite3.connect(TEST_DB_PATH)
        cursor = conn.cursor()

        # Insert test document 1
        doc_id = "doc_test01"
        cursor.execute("""
            INSERT INTO documents (id, title, original_filename, jurisdiction, language_code, sha256_hash)
            VALUES ('doc_test01', 'Test COVID Protocol', 'test_protocol.pdf', 'NL', 'nl', 'hash1234567890abcdef');
        """)
        cursor.execute("""
            INSERT INTO document_texts (document_id, full_text, page_count, has_ocr)
            VALUES ('doc_test01', 'Het Outbreak Management Team en Marion Koopmans adviseerden de minister.', 5, 1);
        """)
        cursor.execute("""
            INSERT INTO document_topics (document_id, topic_code)
            VALUES ('doc_test01', 'TOPIC_ADVISORY_MINUTES');
        """)
        cursor.execute("""
            INSERT INTO document_versions (version_id, document_id, version_number, sha256_hash, changes_description)
            VALUES ('ver_01', 'doc_test01', 1, 'hash1234567890abcdef', 'Initial creation');
        """)
        conn.commit()
        conn.close()

        # Test FTS5 Search
        res = search_by_keyword("Koopmans", db_path=TEST_DB_PATH)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], "doc_test01")

        # Test Topic Filter
        res_topic = search_by_topic("TOPIC_ADVISORY_MINUTES", db_path=TEST_DB_PATH)
        self.assertEqual(len(res_topic), 1)
        self.assertEqual(res_topic[0]["id"], "doc_test01")

        # Test History
        history = get_document_history("doc_test01", db_path=TEST_DB_PATH)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["version_number"], 1)

        # Test Unique SHA-256 Constraint
        conn = sqlite3.connect(TEST_DB_PATH)
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO documents (id, title, original_filename, jurisdiction, language_code, sha256_hash)
                VALUES ('doc_test02', 'Duplicate Protocol', 'dup.pdf', 'NL', 'nl', 'hash1234567890abcdef');
            """)
        conn.close()


if __name__ == "__main__":
    unittest.main()
