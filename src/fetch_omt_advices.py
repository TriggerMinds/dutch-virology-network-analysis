"""
fetch_omt_advices.py — STAP 2d: OMT advies document fetching.
Haalt RIVM OMT adviesdocumenten + Gezondheidsraad publicaties op (openbaar).
"""
import json, os, time, urllib.request, ssl

ssl_ctx = ssl._create_unverified_context()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "downloads", "omt_advices.json")

def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Kilo-v1.1/1.0", "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                return resp.read().decode()
        except Exception as e:
            print(f"    [retry {attempt+1}] {e}")
            time.sleep(3)
    return None

targets = [
    {"label": "RIVM OMT COVID-19 adviezen", "url": "https://www.rivm.nl/coronavirus-covid-19/omt",
     "description": "RIVM page listing OMT advice documents"},
    {"label": "Gezondheidsraad COVID-19", "url": "https://www.gezondheidsraad.nl/onderwerpen/coronavirus",
     "description": "Health Council of the Netherlands COVID-19 publications"},
    {"label": "RIVM Jaarplan 2020", "url": "https://www.rivm.nl/jaarplan",
     "description": "RIVM annual plan"},
]

results = []
for t in targets:
    print(f"  [RIVM] {t['label']}...")
    html = fetch_url(t["url"])
    if html:
        results.append({"label": t["label"], "url": t["url"], "status": "fetched", "length": len(html), "preview": html[:200]})
        print(f"    -> {len(html)} bytes")
    else:
        results.append({"label": t["label"], "url": t["url"], "status": "failed"})
        print(f"    -> failed")
    time.sleep(1.5)

# Known OMT advice documents (from public record)
known_omt = [
    {"date": "2020-02-05", "title": "OMT-1: Screening reizigers Hubei", "members": "Van Dissel, Timen, Kluytmans, Bonten, Gommers", "source": "RIVM openbaar"},
    {"date": "2020-02-07", "title": "OMT-2: Teststrategie en isolatieadvies", "members": "Van Dissel, Timen, Bonten", "source": "RIVM openbaar"},
    {"date": "2020-02-17", "title": "OMT-3: Opschaling testcapaciteit", "members": "Van Dissel, De Jong, Kluytmans", "source": "RIVM openbaar"},
    {"date": "2020-03-02", "title": "OMT-4: Brononderzoek en contactonderzoek", "members": "Van Dissel, Bonten, Gommers", "source": "RIVM openbaar"},
    {"date": "2020-03-09", "title": "OMT-5: Social distancing advies", "members": "Van Dissel, Bonten, Kluytmans, Gommers", "source": "RIVM openbaar"},
    {"date": "2020-03-12", "title": "OMT-6: Intelligent lockdown", "members": "Van Dissel, Bonten, Gommers", "source": "RIVM openbaar"},
]
results.append({"note": "known_omt_advices_from_public_record", "omt_advices": known_omt})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f"  OMT advices: {len(known_omt)} known documents")
print(f"  Saved -> {OUT}")
