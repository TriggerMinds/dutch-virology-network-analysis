"""
analyze_narrative_lag.py — STAP 4: Narrative time-lag correlation.
Berekent vertraging tussen OMT-notulen, beleidsbeslissingen en media-verslaggeving.
"""
import json, os
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_STATS = os.path.join(ROOT, "data", "narrative_lag_stats.json")

# Reconstructed timeline of key events
timeline = [
    # (date, event_type, description, media_mention_date_if_applicable)
    ("2020-01-31", "internal_call", "Farrar calls Fauci about furin cleavage site", None),
    ("2020-02-01", "meeting", "Feb 1 Conference Call (12 scientists)", None),
    ("2020-02-03", "policy", "OMT-advies: screenen reizigers Hubei (RIVM)", None),
    ("2020-02-05", "omt", "OMT-1: eerste formele OMT over COVID-19 (RIVM)", None),
    ("2020-02-07", "omt", "OMT-2: teststrategie en isolatieadvies", None),
    ("2020-02-12", "media", "Eerste Volkskrant artikel over 'nieuw coronavirus'", "2020-02-12"),
    ("2020-02-17", "omt", "OMT-3: opschaling testcapaciteit", None),
    ("2020-02-19", "media", "Keulemans (Volkskrant): 'Waarom Nederland nog niet test'", "2020-02-19"),
    ("2020-02-24", "policy", "RIVM adviseert risicogroepen te ontzien", None),
    ("2020-02-25", "media", "Keulemans: 'RIVM: coronavirus gaat zich verspreiden'", "2020-02-25"),
    ("2020-02-27", "policy", "Eerste Nederlandse COVID-19 patient bevestigd (Tilburg)", None),
    ("2020-02-28", "media", "Landelijke media-aandacht piekt (alle kranten)", "2020-02-28"),
    ("2020-03-02", "omt", "OMT-4: brononderzoek en contactonderzoek prioriteit", None),
    ("2020-03-06", "media", "Keulemans: 'Waarom Nederland niet lockdown kiest'", "2020-03-06"),
    ("2020-03-09", "policy", "Kabinet adviseert thuiswerken en sociale afstand", None),
    ("2020-03-12", "policy", "RIVM adviseert 'intelligente lockdown' (OMT-6)", None),
    ("2020-03-12", "media", "Eerste grote persconferentie Rutte/de Jonge", "2020-03-12"),
    ("2020-03-15", "media", "Keulemans analyse over intelligent lockdown", "2020-03-15"),
    ("2020-03-16", "policy", "Kabinet kondigt 'intelligente lockdown' aan", None),
    ("2020-03-17", "media", "Keulemans: 'Lockdown werkt - dit is waarom'", "2020-03-17"),
    ("2020-05-18", "media", "First public mention of lab leak theory in NL media", "2020-05-18"),
    ("2020-05-20", "policy", "WHO says SARS-CoV-2 'most likely natural origin'", None),
    ("2020-05-27", "media", "Keulemans: 'Wuhan lab leak theorie ontkracht'", "2020-05-27"),
    ("2021-01-15", "media", "Keulemans: 'Koopmans: we moeten wereldwijd brononderzoek doen'", "2021-01-15"),
    ("2021-05-23", "policy", "Biden orders intelligence review of COVID origins", None),
    ("2021-05-25", "media", "Keulemans: 'VS start nieuw brononderzoek naar coronavirus'", "2021-05-25"),
    ("2021-06-04", "media", "Washington Post publishes Fauci emails", "2021-06-04"),
    ("2021-06-08", "media", "Keulemans: 'Fauci-mails tonen vroege twijfel over natuurlijke oorsprong'", "2021-06-08"),
]

# Calculate lags
narrative_lags = []
for t in timeline:
    event_date = datetime.strptime(t[0], "%Y-%m-%d")
    if t[3]:  # media_mention_date
        media_date = datetime.strptime(t[3], "%Y-%m-%d")
        lag_days = (media_date - event_date).days
        narrative_lags.append({
            "event_date": t[0],
            "media_date": t[3],
            "event_type": t[1],
            "description": t[2],
            "lag_days": lag_days
        })

# Calculate by event type
lags_by_type = {}
for nl in narrative_lags:
    t = nl["event_type"]
    if t not in lags_by_type:
        lags_by_type[t] = []
    lags_by_type[t].append(nl["lag_days"])

stats = {
    "total_events": len(timeline),
    "total_with_media_mention": len(narrative_lags),
    "narrative_lags": narrative_lags,
    "avg_lag_by_type": {}
}
for t, lags in lags_by_type.items():
    avg = sum(lags) / len(lags) if lags else 0
    stats["avg_lag_by_type"][t] = {
        "count": len(lags),
        "avg_lag_days": round(avg, 1),
        "min_lag": min(lags),
        "max_lag": max(lags)
    }

# Key findings
all_lags = [nl["lag_days"] for nl in narrative_lags]
stats["overall_avg_lag_days"] = round(sum(all_lags) / len(all_lags), 1) if all_lags else 0
stats["overall_median_lag_days"] = sorted(all_lags)[len(all_lags)//2] if all_lags else 0

# Key: OMT-beleid -> media lag
omt_lags = [nl for nl in narrative_lags if nl["event_type"] in ("omt", "policy")]
if omt_lags:
    stats["avg_omt_to_media_lag_days"] = round(sum(nl["lag_days"] for nl in omt_lags) / len(omt_lags), 1)
else:
    stats["avg_omt_to_media_lag_days"] = 0

# Feb 1 call to first NL media mention of lab leak
feb1_to_leak_lag = None
for nl in narrative_lags:
    if "lab leak" in nl["description"].lower() and nl["event_date"] >= "2020-05-01":
        feb1_to_leak_lag = {
            "from_date": "2020-02-01",
            "to_date": nl["media_date"],
            "lag_days": (datetime.strptime(nl["media_date"], "%Y-%m-%d") - datetime.strptime("2020-02-01", "%Y-%m-%d")).days,
            "description": nl["description"]
        }
        break

if feb1_to_leak_lag:
    stats["feb1_call_to_first_NL_media_lab_leak_days"] = feb1_to_leak_lag

with open(OUT_STATS, "w") as f:
    json.dump(stats, f, ensure_ascii=False, indent=1)

print(f"  narrative_lag_stats -> {OUT_STATS}")
print(f"  Events analyzed: {len(timeline)}")
print(f"  With media mention: {len(narrative_lags)}")
print(f"  Overall avg lag: {stats['overall_avg_lag_days']} days")
print(f"  OMT/Policy -> Media avg: {stats['avg_omt_to_media_lag_days']} days")
if feb1_to_leak_lag:
    print(f"  Feb 1 call -> first NL media lab leak mention: {feb1_to_leak_lag['lag_days']} days")
print("[DONE] Narrative lag analysis complete.")
