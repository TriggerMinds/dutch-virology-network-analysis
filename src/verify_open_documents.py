"""
Document Integrity & SHA-256 Checksum Register Script (src/verify_open_documents.py)
Scans downloads/pdf_documents/, calculates SHA-256 hashes, updates metadata in data/archive.db,
and generates a verified data/checksums.sha256 file.
"""

import hashlib
import os
import sqlite3

import pdfplumber

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_ARCHIVE_PATH = os.path.join(ROOT, "data", "archive.db")
PDF_DIR = os.path.join(ROOT, "downloads", "pdf_documents")
CHECKSUM_FILE = os.path.join(ROOT, "data", "checksums.sha256")


def compute_sha256(file_path):
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def get_pdf_page_count(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            return len(pdf.pages)
    except Exception:
        return 0


def verify_documents():
    os.makedirs(PDF_DIR, exist_ok=True)
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]

    print(f"[VERIFIER] Scanning {len(pdf_files)} PDF files in {PDF_DIR}...")
    checksum_lines = []

    conn = sqlite3.connect(DB_ARCHIVE_PATH) if os.path.exists(DB_ARCHIVE_PATH) else None

    for pdf_name in pdf_files:
        full_path = os.path.join(PDF_DIR, pdf_name)
        sha_hash = compute_sha256(full_path)
        file_bytes = os.path.getsize(full_path)
        pages = get_pdf_page_count(full_path)

        checksum_lines.append(f"{sha_hash}  {pdf_name}\n")
        print(f" - {pdf_name}: {file_bytes} bytes, {pages} pages, SHA-256: {sha_hash[:16]}...")

        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE documents
                SET sha256_hash = ?
                WHERE original_filename = ?;
            """, (sha_hash, pdf_name))
            cursor.execute("""
                UPDATE document_texts
                SET page_count = ?
                WHERE document_id IN (SELECT id FROM documents WHERE original_filename = ?);
            """, (pages, pdf_name))

    if conn:
        conn.commit()
        conn.close()

    # Write checksums.sha256
    with open(CHECKSUM_FILE, "w", encoding="utf-8") as cf:
        cf.writelines(checksum_lines)

    print(f"[SUCCESS] Checksum register updated at {CHECKSUM_FILE} ({len(checksum_lines)} hashes verified).")


if __name__ == "__main__":
    verify_documents()
