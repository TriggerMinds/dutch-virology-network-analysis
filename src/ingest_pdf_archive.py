"""
Automated PDF Ingestion Script for data/archive.db
Extracts text, computes SHA-256 hashes, prevents duplicates, and populates FTS5 search index.
"""

import hashlib
import os
import sqlite3
import uuid

import pdfplumber
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "archive.db")
PDF_DIR = os.path.join(ROOT, "downloads", "pdf_documents")


def compute_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def extract_pdf_text(file_path):
    full_text = ""
    page_count = 0
    try:
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                txt = page.extract_text()
                if txt:
                    full_text += txt + "\n\n"
    except Exception:
        # Fallback to pypdf
        try:
            reader = PdfReader(file_path)
            page_count = len(reader.pages)
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    full_text += txt + "\n\n"
        except Exception as e:
            print(f"[WARN] Could not extract text from {file_path}: {e}")

    return full_text.strip(), page_count


def ingest_pdf_file(
    file_path,
    db_path=DB_PATH,
    jurisdiction="NL",
    language_code="nl",
    topic_code=None,
):
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return None

    file_hash = compute_sha256(file_path)
    filename = os.path.basename(file_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check for duplicate SHA-256 hash
    cursor.execute(
        "SELECT id, title FROM documents WHERE sha256_hash = ?", (file_hash,)
    )
    existing = cursor.fetchone()
    if existing:
        print(
            f"[SKIP DUPLICATE] {filename} already ingested as ID: {existing[0]} ({file_hash[:12]}...)"
        )
        conn.close()
        return existing[0]

    doc_id = f"doc_{uuid.uuid4().hex[:12]}"
    title = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ")
    text_content, page_count = extract_pdf_text(file_path)

    # Insert metadata into documents
    cursor.execute(
        """
        INSERT INTO documents (
            id, title, original_filename, jurisdiction, issuing_agency,
            document_type, publication_date, language_code, sha256_hash
        ) VALUES (?, ?, ?, ?, ?, ?, CURRENT_DATE, ?, ?)
    """,
        (
            doc_id,
            title,
            filename,
            jurisdiction,
            "Archive Pipeline",
            "PDF Document",
            language_code,
            file_hash,
        ),
    )

    # Insert text into document_texts (triggers FTS5 auto-sync)
    cursor.execute(
        """
        INSERT INTO document_texts (document_id, full_text, page_count, has_ocr)
        VALUES (?, ?, ?, 1)
    """,
        (doc_id, text_content, page_count),
    )

    # Insert topic mapping if provided
    if topic_code:
        cursor.execute(
            """
            INSERT OR IGNORE INTO document_topics (document_id, topic_code)
            VALUES (?, ?)
        """,
            (doc_id, topic_code),
        )

    # Insert version 1 entry
    cursor.execute(
        """
        INSERT INTO document_versions (version_id, document_id, version_number, release_date, sha256_hash, changes_description)
        VALUES (?, ?, 1, CURRENT_DATE, ?, 'Initial document ingestion')
    """,
        (f"ver_{uuid.uuid4().hex[:8]}", doc_id, file_hash),
    )

    conn.commit()
    conn.close()

    print(
        f"[INGESTED] {filename} -> ID: {doc_id} ({page_count} pages, {len(text_content)} bytes text, Hash: {file_hash[:12]}...)"
    )
    return doc_id


def ingest_directory(pdf_dir=PDF_DIR, db_path=DB_PATH):
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]

    # Check root for specific PDFs if pdf_dir is empty
    root_pdfs = [
        os.path.join(ROOT, f)
        for f in os.listdir(ROOT)
        if f.lower().endswith(".pdf")
    ]
    for rpdf in root_pdfs:
        dest = os.path.join(pdf_dir, os.path.basename(rpdf))
        if not os.path.exists(dest):
            with open(rpdf, "rb") as rf, open(dest, "wb") as df:
                df.write(rf.read())
            print(f"[COPIED] {os.path.basename(rpdf)} to downloads/pdf_documents/")

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    print(
        f"[INFO] Found {len(pdf_files)} PDF files to process in {pdf_dir}..."
    )

    ingested_ids = []
    for pdf_file in pdf_files:
        full_path = os.path.join(pdf_dir, pdf_file)
        doc_id = ingest_pdf_file(full_path, db_path=db_path)
        if doc_id:
            ingested_ids.append(doc_id)

    return ingested_ids


if __name__ == "__main__":
    from init_archive_db import init_db

    init_db()
    ingest_directory()
