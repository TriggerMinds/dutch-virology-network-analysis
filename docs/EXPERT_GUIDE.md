# Expert Guide: Multi-Language Document Archive (data/archive.db) & FTS5 Search

> **Version:** 1.0  
> **Database:** `data/archive.db`  
> **Features:** FTS5 Full-Text Search, SHA-256 Provenance Hashing, EuroVoc Taxonomy, Multi-Lingual Metadata  

---

## 1. Architecture & Schema Overview

The `data/archive.db` database is structured to store multi-language pandemic records (WOO, FOIA, RKI-Protokolle, Corman-Drosten protocols, Senate reports) with cryptographic provenance guarantees.

### Table Schema

- `documents`: Primary metadata record (SHA-256 hash, jurisdiction, language_code, publication_date).
- `document_texts`: Extracted page-by-page full text content linked via foreign key.
- `taxonomy_topics`: EuroVoc-aligned topic categories (`TOPIC_ADVISORY_MINUTES`, `TOPIC_DIAGNOSTICS`, `TOPIC_EMERGENCY_PROCUREMENT`, `TOPIC_POLICY_DIRECTIVES`, `TOPIC_FINANCIAL_GRANTS`).
- `document_topics`: Many-to-many relationship mapping documents to topics.
- `document_versions`: Version history and hash release tracking.
- `fts_document_texts`: SQLite FTS5 virtual table for high-speed full-text queries.

---

## 2. Python API Usage

### Initializing the Database

```python
from src.init_archive_db import init_db

init_db()  # Creates data/archive.db with all 5 tables and FTS5 triggers
```

### Ingesting PDF Files

```python
from src.ingest_pdf_archive import ingest_pdf_file

doc_id = ingest_pdf_file(
    "downloads/pdf_documents/2026.07.24_Tonys-Diary-Package.pdf",
    jurisdiction="US",
    language_code="en",
    topic_code="TOPIC_ADVISORY_MINUTES"
)
```

### Searching Full-Text Content via FTS5

```python
from src.search_archive import search_by_keyword

# Search across all documents for specific terms
results = search_by_keyword("Fouchier OR Koopmans OR Drosten", language_code="nl", jurisdiction="NL")

for r in results:
    print(f"[{r['jurisdiction']}] {r['title']}")
    print(f"Snippet: {r['snippet']}")
    print(f"SHA-256 Hash: {r['sha256_hash']}\n")
```

### Searching by Taxonomy Topic

```python
from src.search_archive import search_by_topic

# Retrieve all diagnostic protocol documents
docs = search_by_topic("TOPIC_DIAGNOSTICS", date_from="2020-01-01")
for d in docs:
    print(d["title"], d["publication_date"])
```

---

## 3. SQL Query Examples

### Executing FTS5 Full-Text Search in SQLite CLI

```sql
SELECT d.title, d.jurisdiction, d.sha256_hash,
       snippet(fts_document_texts, 1, '<b>', '</b>', '...', 30) AS snippet
FROM fts_document_texts fts
JOIN documents d ON fts.document_id = d.id
WHERE fts_document_texts MATCH 'Fauci AND "Proximal Origin"'
ORDER BY rank
LIMIT 10;
```

### Verifying SHA-256 Hash Provenance

```sql
SELECT d.id, d.title, d.sha256_hash, v.version_number, v.release_date
FROM documents d
JOIN document_versions v ON d.id = v.document_id
WHERE d.sha256_hash = '27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e';
```
