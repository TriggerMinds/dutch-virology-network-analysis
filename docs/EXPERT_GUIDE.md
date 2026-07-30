# Expert Guide: Multi-Language Document Archive (data/archive.db) & Data Engineering Modules

> **Version:** 1.5  
> **Databases:** `data/archive.db` & `data/network_data.db`  
> **Features:** FTS5 Full-Text Search, SHA-256 Provenance Hashing, EuroVoc Taxonomy, Redaction Deltas, Open Macro-Data Harvesting, Coverage Status Dictionary  

---

## 1. Architecture & Schema Overview

The database ecosystem is structured to store multi-language pandemic records (WOO, FOIA, RKI-Protokolle, Corman-Drosten protocols, Senate reports) with cryptographic provenance guarantees.

### Table Schema Summary

- `documents`: Primary metadata record (SHA-256 hash, jurisdiction, language_code, publication_date, `coverage_status`).
- `document_texts`: Extracted page-by-page full text content linked via foreign key.
- `redaction_deltas`: Page-by-page diff tracking between redacted (Version A) and unredacted (Version B) releases (`diff_snippet`, `unredacted_text`).
- `taxonomy_topics`: EuroVoc-aligned topic categories (`TOPIC_ADVISORY_MINUTES`, `TOPIC_DIAGNOSTICS`, `TOPIC_EMERGENCY_PROCUREMENT`, `TOPIC_POLICY_DIRECTIVES`, `TOPIC_FINANCIAL_GRANTS`).
- `document_topics`: Many-to-many relationship mapping documents to topics.
- `document_versions`: Version history and release hash tracking.
- `fts_document_texts`: SQLite FTS5 virtual table for high-speed full-text queries.

---

## 2. Python API & Data Engineering Modules

### A. Initializing the Archive Database

```python
from src.init_archive_db import init_db

init_db()  # Creates data/archive.db with all 5 tables and FTS5 triggers
```

### B. Redaction Delta Tracking (`src/track_redaction_deltas.py`)

```python
from src.track_redaction_deltas import compare_documents

deltas = compare_documents(
    doc_id="doc_woo_vws_2023_0042",
    doc_title="Woo/VWS-2023-0042 Notulen Feb 1 Call",
    pdf_path_a="downloads/pdf_documents/vws_2021_redacted.pdf",
    pdf_path_b="downloads/pdf_documents/vws_2024_unredacted.pdf"
)

for d in deltas:
    print(f"Page {d['page_num']}: Newly unredacted -> {d['unredacted_text']}")
```

### C. Open Macro-Data Harvester (`src/fetch_open_macro_data.py`)

```python
from src.fetch_open_macro_data import run_harvest

data = run_harvest()
print("CBS Table ID:", data["cbs_statline"]["table_id"])
print("Tweede Kamer Documents:", data["tweede_kamer_odata"]["count"])
```

### D. Coverage Dictionary & Web UI Status (`src/build_coverage_dictionary.py`)

```python
from src.build_coverage_dictionary import update_graph_and_web_ui

update_graph_and_web_ui()
# Extends schemas and updates coverage_status values:
# - VERIFIED_PUBLIC (100% openbaar)
# - STATUTORY_RESTRICTED (wettelijk beperkt/AVG)
# - PENDING_APPEAL (lopende Woo-procedure)
```

---

## 3. SQL Query Examples

### Querying Newly Unredacted Text Deltas

```sql
SELECT document_title, page_num, release_date, unredacted_text, diff_snippet
FROM redaction_deltas
WHERE unredacted_text LIKE '%furin%' OR unredacted_text LIKE '%Koopmans%'
ORDER BY release_date DESC;
```

### Executing FTS5 Full-Text Search with Coverage Status

```sql
SELECT d.title, d.jurisdiction, d.coverage_status, d.sha256_hash,
       snippet(fts_document_texts, 1, '<b>', '</b>', '...', 30) AS snippet
FROM fts_document_texts fts
JOIN documents d ON fts.document_id = d.id
WHERE fts_document_texts MATCH 'Fauci AND "Proximal Origin"'
ORDER BY rank
LIMIT 10;
```

### Verifying SHA-256 Hash Provenance

```sql
SELECT d.id, d.title, d.sha256_hash, d.coverage_status, v.version_number, v.release_date
FROM documents d
JOIN document_versions v ON d.id = v.document_id
WHERE d.sha256_hash = '27d8d39b118638e4c0a4a0ece7fda8e7e6772ea70a920aacfdcca70f198cd57e';
```
