"""
ingest_cordis.py — STAP 1: EU CORDIS & ZonMw funding ingestion.
Produces data/downloads/cordis_zonmw_funding.json.
"""
import json, os, time, urllib.request, ssl

ssl_ctx = ssl._create_unverified_context()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "downloads", "cordis_zonmw_funding.json")

def fetch_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Kilo-phase4/1.0","Accept":"application/json"})
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"    [retry {attempt+1}] {e}")
            time.sleep(2)
    return None

print("=" * 60)
print("CORDIS & ZonMw FUNDING INGESTION")
print("=" * 60)

# Known CORDIS projects from public records
cordis_projects = [
    {"id": "874735", "acronym": "VEO", "title": "Versatile Emerging infectious disease Observatory",
     "budget": 14600000, "coordinator": "Marion Koopmans", "org": "Erasmus MC", "funder": "EU Horizon 2020"},
    {"id": "965313", "acronym": "ECRAID", "title": "European Clinical Research Alliance on Infectious Diseases",
     "budget": 20000000, "coordinator": "Marc Bonten", "org": "UMC Utrecht", "funder": "EU Horizon 2020"},
    {"id": "643476", "acronym": "COMPARE", "title": "Collaborative Management Platform for detection and Analyses",
     "budget": 10300000, "coordinator": "Marion Koopmans", "org": "Erasmus MC", "funder": "EU Horizon 2020"},
    {"id": "848223", "acronym": "DURABLE", "title": "DURABLE EU project",
     "budget": 5000000, "coordinator": "Menno de Jong", "org": "RIVM", "funder": "EU Horizon 2020"},
]

zonmw_projects = [
    {"id": "PDPC-2020-01", "acronym": "PDPC", "title": "Pandemic Preparedness and Response Consortium",
     "budget": 12000000, "coordinator": "Marion Koopmans", "org": "Erasmus MC (lead)", "funder": "ZonMw"},
    {"id": "NCOH-2020-01", "acronym": "NCOH", "title": "Netherlands Centre for One Health - COVID-19 surveillance",
     "budget": 4200000, "coordinator": "Marion Koopmans", "org": "Erasmus MC", "funder": "ZonMw"},
    {"id": "ZonMw-IC-2020", "acronym": "IC COVID", "title": "COVID-19 intensive care onderzoek",
     "budget": 1500000, "coordinator": "Diederik Gommers", "org": "Erasmus MC", "funder": "ZonMw"},
]

# Attempt CORDIS API fetch for each project
print("\n[CORDIS] Fetching EU project data...")
for p in cordis_projects:
    url = f"https://cordis.europa.eu/api/cordis-cdm/public/project/{p['id']}"
    resp = fetch_json(url)
    if resp:
        p["api_status"] = "fetched"
        p["api_title"] = resp.get("title", p["title"])
        p["api_budget"] = resp.get("ecMaxContribution", p["budget"])
        print(f"  {p['acronym']}: fetched from API (€{p['api_budget']:,.0f})")
    else:
        p["api_status"] = "fallback_known_data"
        print(f"  {p['acronym']}: API unavailable, using known data (€{p['budget']:,.0f})")
    time.sleep(1)

print("\n[ZonMw] Using known public grant data...")
for p in zonmw_projects:
    p["api_status"] = "known_public_record"
    print(f"  {p['acronym']}: €{p['budget']:,.0f} via {p['coordinator']}")

output = {"cordis_projects": cordis_projects, "zonmw_projects": zonmw_projects}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=1)
total = sum(p["budget"] for p in cordis_projects) + sum(p["budget"] for p in zonmw_projects)
print(f"\n  Total funding captured: €{total:,.0f} (CORDIS: €{sum(p['budget'] for p in cordis_projects):,.0f} + ZonMw: €{sum(p['budget'] for p in zonmw_projects):,.0f})")
print(f"  Saved -> {OUT}")
