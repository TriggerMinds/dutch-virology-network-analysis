import os
import json
import csv
import re
import hashlib
from datetime import datetime
import pypdf

KEYWORDS = [
    "koopmans", "marion", "erasmus", "fouchier", "furin", "cleavage",
    "february 1", "1 february", "feb 1", "feb. 1", "teleconference",
    "conference call", "lab", "laboratory", "engineered", "insertion",
    "deliberate", "natural origin", "farrar", "drosten", "andersen", "holmes"
]

def check_redaction(text):
    if not text or len(text.strip()) < 30:
        return "illegible_or_heavy"
    redaction_markers = ["(b)(4)", "(b)(6)", "(b)(7)", "[redacted]", "redacted", "foia exemption"]
    count = sum(1 for m in redaction_markers if m in text.lower())
    if count > 3:
        return "heavy"
    elif count > 0:
        return "partial"
    return "none"

def evaluate_koopmans_position(text):
    text_lower = text.lower()
    if "koopmans" not in text_lower and "marion" not in text_lower:
        return "unknown", "Koopmans not mentioned on this page."
    
    # Look for explicit statements about her position
    position_keywords = [
        "koopmans argued", "koopmans stated", "koopmans believed",
        "koopmans thought", "marion argued", "marion stated",
        "marion position", "koopmans position", "koopmans position was",
        "marion believed", "marion agreed", "marion disagreed"
    ]
    for pk in position_keywords:
        if pk in text_lower:
            return "indicated", f"Explicit mention of position found via '{pk}'."
            
    return "unknown", "Koopmans is mentioned (e.g. participant list or reference), but her explicit stance/position on the furin site/origin is NOT recorded."

def calculate_relevance(text, page_num):
    text_l = text.lower()
    score = 0.0
    if "koopmans" in text_l or "marion" in text_l:
        score += 0.4
    if "february 1" in text_l or "1 february" in text_l or "feb 1" in text_l or "feb. 1" in text_l or "teleconference" in text_l:
        score += 0.3
    if "furin" in text_l or "cleavage" in text_l:
        score += 0.2
    if "fouchier" in text_l or "erasmus" in text_l:
        score += 0.1
    return min(1.0, round(score, 2))

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(base_dir, "data", "raw", "manifest.json")
    
    if not os.path.exists(manifest_path):
        print("Manifest not found. Run acquire_and_hash_raw_data.py first.")
        return

    with open(manifest_path, "r", encoding="utf-8") as mf:
        manifest = json.load(mf)
        
    all_mentions = []
    
    for entry in manifest:
        rel_path = entry["relative_path"]
        full_path = os.path.join(base_dir, rel_path.replace("/", os.sep))
        sha256 = entry["sha256"]
        
        if not os.path.exists(full_path) or not full_path.endswith(".pdf"):
            continue
            
        print(f"Extracting mentions from {rel_path}...")
        reader = pypdf.PdfReader(full_path)
        
        for idx, page in enumerate(reader.pages):
            page_num = idx + 1
            text = page.extract_text() or ""
            text_lower = text.lower()
            
            # Check if page matches any keyword
            matched_kw = [kw for kw in KEYWORDS if kw in text_lower]
            
            if matched_kw:
                rel_score = calculate_relevance(text, page_num)
                
                # We save all pages with relevance >= 0.3 OR explicit mentions of Koopmans/Fouchier/Feb 1
                if rel_score >= 0.3 or "koopmans" in text_lower or "marion" in text_lower or ("feb" in text_lower and "1" in text_lower and "furin" in text_lower):
                    pos_flag, pos_notes = evaluate_koopmans_position(text)
                    redaction = check_redaction(text)
                    
                    # Clean quote / snippet
                    snippet = text.replace("\r", " ").replace("\n", " ")
                    snippet = re.sub(r'\s+', ' ', snippet).strip()
                    
                    # Identify speaker / context if possible
                    speaker = "Anthony Fauci (Diary author)"
                    if "farrar" in snippet.lower():
                        speaker = "Jeremy Farrar / Anthony Fauci"
                    
                    all_mentions.append({
                        "source": entry["relative_path"],
                        "page": page_num,
                        "quote": snippet[:1000] + ("..." if len(snippet) > 1000 else ""),
                        "speaker": speaker,
                        "matched_keywords": matched_kw,
                        "relevance_score": rel_score,
                        "position_indicated": "true" if pos_flag == "indicated" else "unknown",
                        "position_notes": pos_notes,
                        "redaction_flag": redaction,
                        "sha256_source": sha256,
                        "extracted_at": datetime.now().isoformat()
                    })

    # Save JSON
    json_path = os.path.join(base_dir, "data", "processed", "koopmans_feb1_mentions.json")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(all_mentions, jf, indent=2, ensure_ascii=False)
        
    # Save CSV
    csv_path = os.path.join(base_dir, "data", "processed", "koopmans_feb1_mentions.csv")
    fieldnames = ["source", "page", "relevance_score", "position_indicated", "redaction_flag", "speaker", "matched_keywords", "position_notes", "sha256_source", "extracted_at", "quote"]
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        for m in all_mentions:
            row = dict(m)
            row["matched_keywords"] = "|".join(row["matched_keywords"])
            writer.writerow(row)
            
    print(f"Extraction complete. Found {len(all_mentions)} relevant mention pages.")
    print(f"JSON written to {json_path}")
    print(f"CSV written to {csv_path}")

if __name__ == "__main__":
    main()
