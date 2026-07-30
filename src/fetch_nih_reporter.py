"""
fetch_nih_reporter.py — STAP 2a: NIH RePORTER v2 API fetcher.
Targets: Netherlands/Erasmus/RIVM + EcoHealth WIV grant #2R01AI110964.
"""
import json, os, time, urllib.request, ssl

ssl_ctx = ssl._create_unverified_context()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "downloads", "nih_reporter_results.json")

def fetch_json(url, data, retries=4):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data.encode(),
                headers={"User-Agent": "Kilo-v1.1/1.0", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=45, context=ssl_ctx) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"    [retry {attempt+1}] {e}")
            time.sleep(3)
    return None

BASE = "https://api.reporter.nih.gov/v2/projects/search"
all_results = []

queries = {
    "Netherlands_virology": "Netherlands AND (virus OR corona OR influenza OR GOF)",
    "Erasmus_MC": "Erasmus AND (virus OR vaccine OR corona)",
    "RIVM": "RIVM AND (virus OR corona OR influenza)",
    "EcoHealth_Daszak": "EcoHealth AND Daszak AND corona",
    "2R01AI110964": "2R01AI110964",
}

for label, query in queries.items():
    print(f"  [NIH] {label}...")
    payload = json.dumps({
        "criteria": {"advancedTextSearch": {"searchField": "projectterms", "searchText": query}},
        "includeFields": ["appl_id", "project_title", "abstract_text", "principal_investigators", "organization", "fy", "award_amount"],
        "limit": 50, "offset": 0
    })
    resp = fetch_json(BASE, payload)
    if resp:
        items = resp.get("results") or resp.get("items") or []
        all_results.append({"query": label, "query_text": query, "results": items})
        print(f"    -> {len(items)} results")
    time.sleep(1.2)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=1)
print(f"  Saved {len(all_results)} query sets -> {OUT}")
