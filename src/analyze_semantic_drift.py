"""
analyze_semantic_drift.py — STAP 4b: Semantic drift analysis.
Analyseert verschuivingen in termgebruik (GOF, Dual Use, Lab Escape) over 2020-2022.
"""
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(ROOT, "data", "raw_data.json")
OUT = os.path.join(ROOT, "data", "semantic_drift.json")

with open(RAW_PATH, "r", encoding="utf-8") as f:
    pages = json.load(f)

# Define tracking terms
TRACK_TERMS = [
    "gain-of-function", "gain of function", "GOF",
    "dual use", "dual-use",
    "lab leak", "lab-leak", "laboratory escape",
    "natural origin", "natural emergence",
    "deliberate insertion", "engineered",
    "furin cleavage site", "furin",
]

# Categorize pages by date
def extract_date(text):
    for pat in [
        r"(Jan(?:uary)?\.?\s+\d{1,2},?\s+2020)",
        r"(Feb(?:ruary)?\.?\s+\d{1,2},?\s+2020)",
        r"(Mar(?:ch)?\.?\s+\d{1,2},?\s+2020)",
        r"(Apr(?:il)?\.?\s+\d{1,2},?\s+2020)",
        r"(Jun(?:e)?\.?\s+\d{1,2},?\s+2020)",
        r"(Jul(?:y)?\.?\s+\d{1,2},?\s+2020)",
        r"(Aug(?:ust)?\.?\s+\d{1,2},?\s+2020)",
        r"(Sep(?:tember)?\.?\s+\d{1,2},?\s+2020)",
        r"(Oct(?:ober)?\.?\s+\d{1,2},?\s+2020)",
        r"(Nov(?:ember)?\.?\s+\d{1,2},?\s+2020)",
        r"(Dec(?:ember)?\.?\s+\d{1,2},?\s+2020)",
        r"(Jan(?:uary)?\.?\s+\d{1,2},?\s+2021)",
        r"(Feb(?:ruary)?\.?\s+\d{1,2},?\s+2021)",
        r"(Mar(?:ch)?\.?\s+\d{1,2},?\s+2021)",
        r"(Jun(?:e)?\.?\s+\d{1,2},?\s+2021)",
        r"(Jul(?:y)?\.?\s+\d{1,2},?\s+2021)",
        r"\b(\d{4})\b",
    ]:
        m = re.search(pat, text)
        if m:
            return m.group(1)
    return "unknown"

# Track term frequency by period
periods = {"Q1_2020": (0, 90), "Q2_2020": (91, 181), "Q3_2020": (182, 273),
           "Q4_2020": (274, 365), "H1_2021": (366, 546), "H2_2021": (547, 730),
           "2022": (731, 1096)}

# Approximate page-level date mapping from diary entries
date_map = {}
current_date = "unknown"
page_dates = {}

for p in pages:
    pg = p["page"]
    txt = p["text"] or ""
    detected = extract_date(txt)
    if detected != "unknown" and len(detected) > 4:
        current_date = detected
    page_dates[pg] = current_date

# Count term occurrences by period
term_counts = defaultdict(lambda: defaultdict(int))
term_contexts = defaultdict(lambda: defaultdict(list))

for p in pages:
    pg = p["page"]
    txt = p["text"] or ""
    d = page_dates.get(pg, "unknown")
    
    # Assign to period (simplified)
    year = "unknown"
    m = re.search(r"20(\d{2})", d)
    if m:
        year = f"20{m.group(1)}"
    
    for term in TRACK_TERMS:
        count = len(re.findall(re.escape(term), txt, re.IGNORECASE))
        if count > 0:
            period_key = "unknown"
            if "2020" in d:
                period_key = "2020"
            elif "2021" in d:
                period_key = "2021"
            elif "2022" in d:
                period_key = "2022"
            else:
                period_key = year
            term_counts[period_key][term] += count
            # Store first few contexts
            for m2 in re.finditer(re.escape(term), txt, re.IGNORECASE):
                ctx = txt[max(0,m2.start()-80):min(len(txt),m2.end()+80)].replace("\n", " ")
                if len(term_contexts[period_key][term]) < 3:
                    term_contexts[period_key][term].append(ctx)

# Build output
drift_data = {
    "meta": {
        "description": "Semantic drift analysis of key terms across Fauci diary 2020-2022",
        "limitations": "Date assignment is approximate (based on first date mention in page text)"
    },
    "term_frequencies": {k: dict(v) for k, v in sorted(term_counts.items())},
    "term_contexts": {k: dict(v) for k, v in sorted(term_contexts.items())},
    "drift_summary": {}
}

# Calculate drift: what % of total references per year is each term
for year in ["2020", "2021", "2022"]:
    if year in term_counts:
        total = sum(term_counts[year].values())
        drift_data["drift_summary"][year] = {}
        for term in TRACK_TERMS:
            cnt = term_counts[year].get(term, 0)
            if total > 0:
                pct = round(cnt / total * 100, 1)
                drift_data["drift_summary"][year][term] = {"count": cnt, "pct": pct}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(drift_data, f, ensure_ascii=False, indent=1)

print("=" * 60)
print("SEMANTIC DRIFT ANALYSIS")
print("=" * 60)
for year in ["2020", "2021", "2022"]:
    if year in drift_data["drift_summary"]:
        print(f"\n  {year}:")
        for term, info in sorted(drift_data["drift_summary"][year].items(), key=lambda x: -x[1]["count"])[:8]:
            print(f"    {term:30s}: {info['count']:3d} mentions ({info['pct']:.1f}%)")
        total = sum(v["count"] for v in drift_data["drift_summary"][year].values())
        print(f"    {'TOTAL':30s}: {total:3d}")

print(f"\n  Saved -> {OUT}")
print("[DONE]")
