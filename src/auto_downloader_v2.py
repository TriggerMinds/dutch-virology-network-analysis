"""
auto_downloader_v2.py — Multiplex-ingestie voor ALLE Tier 1-2-3 nodes + consortia.
Bronnen: OpenAlex (co-auteurschappen), NIH RePORTER (grants),
         FOIA/Woo (referenties), ZonMw (via OpenAlex grants index).
"""
import json, os, time, urllib.request, ssl, re

ssl_ctx = ssl._create_unverified_context()
OUTDIR = r"C:\Users\gewoo\Desktop\New folder (4)\data\downloads"
os.makedirs(OUTDIR, exist_ok=True)

# ── GEBEGRENSE TIER NODES ────────────────────────────────────────────────
TIER_1 = [
    "Ron Fouchier", "Marion Koopmans", "Ab Osterhaus",
    "Thijs Kuiken", "Bart Haagmans", "Jaap van Dissel",
    "Diederik Gommers", "Jan Kluytmans",
]
TIER_2 = [
    "Aura Timen", "Menno de Jong", "Marc Bonten",
    "Annemiek van der Eijk", "Massimo Palmarini",
    "Arfan Ikram", "Ernst Kuipers",
]
TIER_3 = [
    "Maarten Keulemans",
]
ALL_TIERS = {n: 1 for n in TIER_1} | {n: 2 for n in TIER_2} | {n: 3 for n in TIER_3}

CONSORTIA = ["PDPC", "NCOH", "VEO", "DURABLE", "ECRAID", "ESWI", "ZonMw"]

def fetch_json(url, retries=3, data=None):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data,
                headers={"User-Agent": "Kilo-OSINT-Multiplex/2.0",
                         "Content-Type": "application/json", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=45, context=ssl_ctx) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"    [WARN] attempt {attempt+1}: {e}")
            time.sleep(2)
    return None

# ─── A. OPENALEX — Alle personen ─────────────────────────────────────────
print("=" * 60)
print("A. OPENALEX — Full Tier 1-2-3 author fetching")
print("=" * 60)

all_authors = {}
for name in list(ALL_TIERS.keys()):
    print(f"\n  [{ALL_TIERS[name]}] {name}")
    search_name = name.replace(" ", "+")
    result = fetch_json(f"https://api.openalex.org/authors?search={search_name}&per_page=5")
    if result and result.get("results"):
        author = result["results"][0]
        aid = author.get("id")
        all_authors[name] = {
            "id": aid,
            "tier": ALL_TIERS[name],
            "display_name": author.get("display_name"),
            "works_count": author.get("works_count", 0),
            "cited_by_count": author.get("cited_by_count", 0),
            "last_known_institution": (author.get("last_known_institutions") or [{}])[0].get("display_name", ""),
            "works": [],
        }
        # Fetch top-20 works for co-author network
        au_id = aid.split("/")[-1] if aid else ""
        works_url = f"https://api.openalex.org/works?filter=authorships.author.id:{au_id}&sort=cited_by_count:desc&per_page=20"
        works = fetch_json(works_url)
        if works and works.get("results"):
            for w in works["results"]:
                wdata = {
                    "title": w.get("title"),
                    "doi": w.get("doi"),
                    "publication_year": w.get("publication_year"),
                    "cited_by_count": w.get("cited_by_count", 0),
                    "coauthors": [au["author"]["display_name"] for au in (w.get("authorships") or [])],
                }
                all_authors[name]["works"].append(wdata)
        print(f"    ID: {aid}  |  Works: {author.get('works_count')}  |  Cited: {author.get('cited_by_count')}  |  Inst: {all_authors[name]['last_known_institution'][:40]}")
    else:
        print(f"    NOT FOUND in OpenAlex")
        all_authors[name] = {"id": None, "tier": ALL_TIERS[name], "display_name": name, "works_count": 0, "cited_by_count": 0, "last_known_institution": "", "works": []}
    time.sleep(1.1)  # rate limit

openalex_path = os.path.join(OUTDIR, "openalex_multiplex.json")
with open(openalex_path, "w", encoding="utf-8") as f:
    json.dump(all_authors, f, ensure_ascii=False, indent=1)
print(f"\n  Saved {len(all_authors)} author profiles -> {openalex_path}")

# ─── B. NIH REPORTER — Consortium-targeted ───────────────────────────────
print("\n" + "=" * 60)
print("B. NIH REPORTER — Consortium & NL-grant search")
print("=" * 60)

# Search for each consortium + person
ALL_NIH = {}
for target in list(ALL_TIERS.keys()) + CONSORTIA:
    target_short = target.split()[-1] if " " in target else target
    payload = json.dumps({
        "criteria": {
            "advancedTextSearch": {
                "searchField": "projectterms",
                "searchText": target_short
            },
            "includeFields": ["appl_id", "project_title", "abstract_text", "principal_investigators", "organization", "fy"]
        },
        "limit": 10, "offset": 0
    }).encode()
    result = fetch_json("https://api.reporter.nih.gov/v2/projects/search", data=payload)
    if result:
        items = result.get("results") or result.get("items") or []
        if items:
            ALL_NIH[target] = items
            print(f"  {target:30s}: {len(items)} grants found")
        # Find Netherlands-relevant among them
        nl_related = []
        for g in items:
            t = (g.get("project_title") or "") + " " + (g.get("abstract_text") or "")
            if re.search(r"Netherlands|Erasmus|Rotterdam|Utrecht|Leiden|Amsterdam|RIVM", t, re.I):
                nl_related.append(g)
        if nl_related:
            print(f"    -> {len(nl_related)} NL-relevant")
    else:
        print(f"  {target:30s}: API error or no results")
    time.sleep(1.1)

nih_path = os.path.join(OUTDIR, "nih_grants_multiplex.json")
with open(nih_path, "w", encoding="utf-8") as f:
    json.dump(ALL_NIH, f, ensure_ascii=False, indent=1)
print(f"  Saved -> {nih_path}")

# ─── C. FOIA/WOO REFERENCES ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("C. FOIA/WOO document references")
print("=" * 60)
foia_entries = [
    {"label": "Fauci Emails (WashPost FOIA)", "url": "https://www.washingtonpost.com/context/fauci-emails/",
     "relevance": "Complete Fauci email archive — includes Koopmans/Fouchier correspondence"},
    {"label": "Proximal Origin paper (DOI)", "url": "https://doi.org/10.1038/s41591-022-01791-8",
     "relevance": "Andersen et al. 2022 — key natural origin argument; 5 Feb 1 call participants as co-authors"},
    {"label": "House Select Subcommittee COVID-19 Origins", "url": "https://oversight.house.gov/",
     "relevance": "U.S. Congressional investigation into COVID origins — NIH/Fauci funding records"},
    {"label": "ZonMw Portaal", "url": "https://www.zonmw.nl/nl/onderzoek-resultaten",
     "relevance": "Dutch research council — search for PDPC, NCOH, VEO, DURABLE grants"},
    {"label": "RIVM — OMT COVID-19 adviezen", "url": "https://www.rivm.nl/coronavirus-covid-19/omt",
     "relevance": "Outbreak Management Team advisory minutes — Van Dissel, Timen et al."},
    {"label": "ECRAID programme", "url": "https://www.ecraid.eu/",
     "relevance": "European Clinical Research Alliance on Infectious Diseases — Bonten/Gommers involvement"},
    {"label": "NCOH — Netherlands Centre for One Health", "url": "https://www.ncoh.nl/",
     "relevance": "Koopmans/Kuiken core members — bat coronavirus surveillance"},
    {"label": "VEO — Versatile Emerging infectious disease Observatory", "url": "https://www.veo-europe.eu/",
     "relevance": "EU Horizon 2020 — Koopmans coordinator; pandemic early warning"},
]
foia_path = os.path.join(OUTDIR, "foia_references.json")
with open(foia_path, "w", encoding="utf-8") as f:
    json.dump(foia_entries, f, ensure_ascii=False, indent=1)
print(f"  Saved {len(foia_entries)} references -> {foia_path}")

print("\n" + "=" * 60)
print("AUTO-DOWNLOADER V2 COMPLETE")
print(f"  OpenAlex: {sum(1 for v in all_authors.values() if v['works'])} authors with works")
print(f"  NIH: {len(ALL_NIH)} target queries executed")
print(f"  FOIA: {len(foia_entries)} references")
print("=" * 60)
