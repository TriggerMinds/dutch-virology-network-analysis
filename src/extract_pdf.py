import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
extract_pdf.py — Stage 1: Full-text extraction from PDF with page-level metadata.
Output: raw_data.json (list of {page, text, tables, has_text} per page)
"""
import json, os, sys
import pdfplumber

PDF_PATH = os.path.join(ROOT, "2026.07.24_Tonys-Diary-Package.pdf")
OUT_PATH = os.path.join(ROOT, "raw_data.json")

def extract_all():
    pages_data = []
    with pdfplumber.open(PDF_PATH) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages, start=1):
            txt = page.extract_text() or ""
            tbls = page.extract_tables() or []
            record = {
                "page": i,
                "text": txt,
                "text_len": len(txt),
                "has_text": len(txt.strip()) > 0,
                "tables": tbls,
                "page_total": total
            }
            pages_data.append(record)
            if i % 100 == 0:
                print(f"[extract] Processed {i}/{total} pages...", flush=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pages_data, f, ensure_ascii=False, indent=1)
    print(f"[extract] Done. {total} pages -> {OUT_PATH}")
    return pages_data

if __name__ == "__main__":
    extract_all()
