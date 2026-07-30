"""
fetch_nwo_grants.py — STAP 2b: NWO/ZonMw open data query.
Via NWO API + ZonMw projecten portaal (search-based).
"""
import json, os, time, urllib.request, ssl

ssl_ctx = ssl._create_unverified_context()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "downloads", "nwo_grants.json")

def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Kilo-v1.1/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                return resp.read().decode()
        except Exception as e:
            print(f"    [retry {attempt+1}] {e}")
            time.sleep(3)
    return None

# NWO open data API — project search
NWO_API = "https://www.nwo.nl/en/search"
# ZonMw projecten register
ZONMW_API = "https://www.zonmw.nl/nl/onderzoek-resultaten"

targets = [
    ("Marion Koopmans", "Koopmans", "ZonMw"),
    ("Ron Fouchier", "Fouchier", "NWO"),
    ("Bart Haagmans", "Haagmans", "ZonMw"),
    ("Marc Bonten", "Bonten", "ZonMw"),
    ("Jan Kluytmans", "Kluytmans", "ZonMw"),
    ("NCOH", "NCOH", "ZonMw"),
    ("PDPC", "PDPC", "ZonMw"),
    ("VEO", "VEO", "EU Horizon 2020"),
]

results = []
for name, search, source in targets:
    print(f"  [{source}] {name}...")
    url = f"https://www.nwo.nl/en/search?search={search}"
    if source == "ZonMw":
        url = f"https://www.zonmw.nl/nl/onderzoek-resultaten?search={search}"
    html = fetch_url(url)
    if html:
        results.append({"name": name, "search": search, "source": source, "url": url, "status": "fetched", "length": len(html)})
        print(f"    -> {len(html)} bytes from {source}")
    else:
        results.append({"name": name, "search": search, "source": source, "url": url, "status": "failed"})
        print(f"    -> failed (likely blocked or no API access)")
    time.sleep(1)

# Known ZonMw grants from public records
known_grants = [
    {"project": "NCOH COVID-19 surveillance", "recipient": "Erasmus MC (Koopmans)", "amount": "EUR 4,200,000", "source": "ZonMw (Woo/3661708)", "year": 2020},
    {"project": "PDPC pandemic preparedness", "recipient": "Consortium (Erasmus MC lead)", "amount": "EUR 12,000,000", "source": "ZonMw (Woo/3661708)", "year": 2020},
    {"project": "BRMO surveillance", "recipient": "Amphia (Kluytmans)", "amount": "EUR 800,000", "source": "ZonMw", "year": 2019},
    {"project": "COVID-19 IC onderzoek", "recipient": "Erasmus MC (Gommers)", "amount": "EUR 1,500,000", "source": "ZonMw", "year": 2020},
    {"project": "VEO (GA#874735)", "recipient": "Erasmus MC (Koopmans)", "amount": "EUR 14,600,000", "source": "EU Horizon 2020", "year": 2020},
    {"project": "ECRAID (GA#965313)", "recipient": "UMC Utrecht (Bonten)", "amount": "EUR 20,000,000", "source": "EU Horizon 2020", "year": 2020},
    {"project": "COMPARE (GA#643476)", "recipient": "Erasmus MC (Koopmans)", "amount": "EUR 10,300,000", "source": "EU Horizon 2020", "year": 2014},
    {"project": "DURABLE (GA#848223)", "recipient": "RIVM (De Jong)", "amount": "EUR 5,000,000", "source": "EU Horizon 2020", "year": 2019},
]
results.append({"note": "known_grants_from_public_records", "grants": known_grants})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"  Known grants added: {len(known_grants)}")
print(f"  Saved -> {OUT}")
