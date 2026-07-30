import os
import shutil
import hashlib
from datetime import datetime
import json
import pypdf

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_page_count(filepath):
    try:
        reader = pypdf.PdfReader(filepath)
        return len(reader.pages)
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
        return None

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    raw_subdirs = [
        "fauci_diary",
        "foia_house",
        "parlementaire_enquete",
        "emails_feb2020",
        "woo_erasmus"
    ]
    
    for sd in raw_subdirs:
        os.makedirs(os.path.join(base_dir, "data", "raw", sd), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "data", "processed"), exist_ok=True)
    
    diary_src = os.path.join(base_dir, "2026.07.24_Tonys-Diary-Package.pdf")
    diary_dst = os.path.join(base_dir, "data", "raw", "fauci_diary", "2026.07.24_Tonys-Diary-Package.pdf")
    
    manifest_entries = []
    
    if os.path.exists(diary_src):
        if not os.path.exists(diary_dst):
            print(f"Copying {diary_src} to {diary_dst}")
            shutil.copy2(diary_src, diary_dst)
        else:
            print(f"Diary already exists at {diary_dst}")
            
        sha256_hash = get_sha256(diary_dst)
        pages = get_page_count(diary_dst)
        file_size = os.path.getsize(diary_dst)
        
        manifest_entries.append({
            "id": "fauci_diary_2026_07_24",
            "title": "Tony's Diary Package (Fauci Diary Release)",
            "relative_path": "data/raw/fauci_diary/2026.07.24_Tonys-Diary-Package.pdf",
            "source_origin": "Rand Paul Release / U.S. Senate Release July 2026 (local raw package)",
            "acquisition_date": datetime.now().isoformat(),
            "sha256": sha256_hash,
            "size_bytes": file_size,
            "page_count": pages,
            "status": "local",
            "notes": "Primary contemporary diary document for Anthony Fauci, covering Jan 2020 onwards."
        })
    else:
        print(f"Warning: {diary_src} not found in root workspace.")

    raw_base = os.path.join(base_dir, "data", "raw")
    for root, dirs, files in os.walk(raw_base):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), base_dir)
            norm_rel = rel_path.replace("\\", "/")
            if norm_rel == "data/raw/fauci_diary/2026.07.24_Tonys-Diary-Package.pdf" or f == "manifest.json":
                continue
            
            full_p = os.path.join(root, f)
            h = get_sha256(full_p)
            pc = get_page_count(full_p) if f.endswith(".pdf") else None
            manifest_entries.append({
                "id": f"raw_{f.replace('.', '_')}",
                "title": f,
                "relative_path": norm_rel,
                "source_origin": "Local Raw File",
                "acquisition_date": datetime.now().isoformat(),
                "sha256": h,
                "size_bytes": os.path.getsize(full_p),
                "page_count": pc,
                "status": "local",
                "notes": "Supplementary raw file in dataset"
            })

    manifest_path = os.path.join(raw_base, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as mf:
        json.dump(manifest_entries, mf, indent=2, ensure_ascii=False)
    
    print(f"Manifest created at {manifest_path} with {len(manifest_entries)} entries.")

if __name__ == "__main__":
    main()
