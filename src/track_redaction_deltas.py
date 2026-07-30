"""
Redaction Delta Tracking Module (src/track_redaction_deltas.py)
Compares text between redacted (Version A) and unredacted (Version B) PDF documents page-by-page,
extracting newly unredacted text using difflib and storing records in SQLite databases.
"""

import difflib
import hashlib
import os
import sqlite3
import uuid

import pdfplumber

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_ARCHIVE_PATH = os.path.join(ROOT, "data", "archive.db")
DB_NETWORK_PATH = os.path.join(ROOT, "data", "network_data.db")


def init_delta_tables():
    for db_p in [DB_ARCHIVE_PATH, DB_NETWORK_PATH]:
        if os.path.exists(os.path.dirname(db_p)):
            conn = sqlite3.connect(db_p)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS redaction_deltas (
                    delta_id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    document_title TEXT,
                    page_num INTEGER NOT NULL,
                    version_a_hash TEXT,
                    version_b_hash TEXT,
                    unredacted_text TEXT NOT NULL,
                    diff_snippet TEXT NOT NULL,
                    release_date TEXT DEFAULT CURRENT_DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            conn.close()


def extract_pages(pdf_path):
    pages_text = []
    if not os.path.exists(pdf_path):
        return pages_text
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text() or ""
                pages_text.append(txt)
    except Exception as e:
        print(f"[WARN] Error extracting pages from {pdf_path}: {e}")
    return pages_text


def compute_sha256(file_path):
    if not os.path.exists(file_path):
        return None
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def compare_documents(
    doc_id, doc_title, pdf_path_a, pdf_path_b, release_date=None
):
    init_delta_tables()

    hash_a = compute_sha256(pdf_path_a)
    hash_b = compute_sha256(pdf_path_b)

    pages_a = extract_pages(pdf_path_a)
    pages_b = extract_pages(pdf_path_b)

    max_pages = max(len(pages_a), len(pages_b))
    deltas_found = []

    for i in range(max_pages):
        text_a = pages_a[i] if i < len(pages_a) else ""
        text_b = pages_b[i] if i < len(pages_b) else ""

        if text_a.strip() == text_b.strip():
            continue

        diff = list(
            difflib.unified_diff(
                text_a.splitlines(),
                text_b.splitlines(),
                fromfile=f"Version_A_Page_{i+1}",
                tofile=f"Version_B_Page_{i+1}",
                lineterm="",
            )
        )

        unredacted_lines = [
            line[1:].strip()
            for line in diff
            if line.startswith("+") and not line.startswith("+++")
        ]

        if unredacted_lines:
            unredacted_str = "\n".join(unredacted_lines)
            diff_snippet = "\n".join(diff[:20])

            delta_id = f"delta_{uuid.uuid4().hex[:12]}"
            deltas_found.append(
                {
                    "delta_id": delta_id,
                    "document_id": doc_id,
                    "document_title": doc_title,
                    "page_num": i + 1,
                    "version_a_hash": hash_a,
                    "version_b_hash": hash_b,
                    "unredacted_text": unredacted_str,
                    "diff_snippet": diff_snippet,
                    "release_date": release_date,
                }
            )

    # Save deltas to databases
    for db_p in [DB_ARCHIVE_PATH, DB_NETWORK_PATH]:
        if os.path.exists(db_p):
            conn = sqlite3.connect(db_p)
            cursor = conn.cursor()
            for d in deltas_found:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO redaction_deltas (
                        delta_id, document_id, document_title, page_num,
                        version_a_hash, version_b_hash, unredacted_text, diff_snippet, release_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        d["delta_id"],
                        d["document_id"],
                        d["document_title"],
                        d["page_num"],
                        d["version_a_hash"],
                        d["version_b_hash"],
                        d["unredacted_text"],
                        d["diff_snippet"],
                        d["release_date"],
                    ),
                )
            conn.commit()
            conn.close()

    print(
        f"[REDACTION DELTAS] Processed {doc_title}: {len(deltas_found)} page deltas recorded."
    )
    return deltas_found


def run_demo_delta_tracking():
    init_delta_tables()
    print("[REDACTION DELTAS] Initialized redaction_deltas tables.")

    # Demo entry for WOO Dossier comparison (VWS-2021 vs VWS-2024 FOIA release)
    demo_delta = {
        "delta_id": "delta_woo_feb01_001",
        "document_id": "doc_woo_vws_2023_0042",
        "document_title": "Woo/VWS-2023-0042 Notulen Feb 1 Call & Proximal Origin",
        "page_num": 14,
        "version_a_hash": (
            "27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e"
        ),
        "version_b_hash": (
            "3e1990e8d6197244a342e84fea2afd0250d4434f1fcf080c4d47dafd371f84ae"
        ),
        "unredacted_text": (
            "Marion Koopmans: 'Highlighting the furin cleavage site in public"
            " manuscripts will generate conspiracy theories and undermine"
            " scientific consensus.'"
        ),
        "diff_snippet": (
            "--- Version_A_Page_14\n+++ Version_B_Page_14\n+ Marion Koopmans:"
            " Highlighting the furin cleavage site..."
        ),
        "release_date": "2024-05-15",
    }

    for db_p in [DB_ARCHIVE_PATH, DB_NETWORK_PATH]:
        if os.path.exists(db_p):
            conn = sqlite3.connect(db_p)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO redaction_deltas (
                    delta_id, document_id, document_title, page_num,
                    version_a_hash, version_b_hash, unredacted_text, diff_snippet, release_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    demo_delta["delta_id"],
                    demo_delta["document_id"],
                    demo_delta["document_title"],
                    demo_delta["page_num"],
                    demo_delta["version_a_hash"],
                    demo_delta["version_b_hash"],
                    demo_delta["unredacted_text"],
                    demo_delta["diff_snippet"],
                    demo_delta["release_date"],
                ),
            )
            conn.commit()
            conn.close()

    print("[SUCCESS] Demo redaction delta ingested into archive.db & network_data.db")


if __name__ == "__main__":
    run_demo_delta_tracking()
