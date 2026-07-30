"""
auto_downloader.py — Haalt externe data op voor waarheidsvinding:
A. NIH RePORTER API → NIH grants met Nederlandse connecties
B. OpenAlex API → Publicaties/co-auteurs: Fouchier, Koopmans, Fauci, Farrar
C. FOIA / openbare documenten (directe links)

Output: downloads/nih_funding_netherlands.json, downloads/openalex_coauthorships.json
"""
import json, os, time, urllib.request, urllib.error, ssl

# Bypass SSL verification for corporate proxy environments
ssl_ctx = ssl._create_unverified_context()

OUTDIR = r"C:\Users\gewoo\Desktop\New folder (4)\downloads"
os.makedirs(OUTDIR, exist_ok=True)

def fetch_json(url, retries=3, data=None):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": "Kilo-OSINT/1.0",
                "Content-Type": "application/json", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=45, context=ssl_ctx) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"  [WARN] Attempt {attempt+1}/{retries} failed: {e}")
            time.sleep(2)
    return None

# ─── A. NIH REPORTER API ────────────────────────────────────────────────
print("=== A. NIH RePORTER: Netherlands-linked grants ===")
NIH_URL = "https://api.reporter.nih.gov/v2/projects/search"
# We search for projects mentioning Dutch investigators/institutions
# The RePORTER API v2 uses POST with JSON body
# For simplicity, we use the public search endpoint
payload = json.dumps({
    "criteria": {
        "advancedTextSearch": {
            "searchField": "projectterms",
            "searchText": "Netherlands OR Erasmus OR RIVM OR Koopmans OR Fouchier"
        },
        "includeFields": [
            "appl_id", "project_title", "abstract_text", "principal_investigators",
            "organization", "fy", "funding_ics", "award_amount"
        ]
    },
    "limit": 50,
    "offset": 0,
    "sortField": "fy",
    "sortOrder": "desc"
}).encode()

nih_results = []
nih_response = fetch_json(NIH_URL, data=payload)
if nih_response:
    nih_results = nih_response.get("results", nih_response.get("items", []))
    print(f"  Found {len(nih_results)} NIH projects matching Netherlands terms")
else:
    print(f"  NIH API returned no results")

# Fallback: NIH ExPORTER text dump search if API fails
if not nih_results:
    print("  Attempting NIH RePORTER fallback (Erasmus org search)...")
    payload2 = json.dumps({
        "criteria": {
            "orgNames": ["ERASMUS"],
            "includeFields": ["appl_id", "project_title", "org_name", "fy", "award_amount"]
        },
        "limit": 20,
        "offset": 0
    }).encode()
    fallback = fetch_json("https://api.reporter.nih.gov/v2/projects/search", data=payload2)
    if fallback:
        nih_results = fallback.get("results", fallback.get("items", []))
        print(f"  Fallback: found {len(nih_results)} Erasmus-linked grants")
    else:
        print("  NIH fallback also failed")

nih_path = os.path.join(OUTDIR, "nih_funding_netherlands.json")
with open(nih_path, "w", encoding="utf-8") as f:
    json.dump(nih_results, f, ensure_ascii=False, indent=1)
print(f"  Saved {len(nih_results)} grants to {nih_path}")

# ─── B. OpenAlex API — Co-authorships ───────────────────────────────────
print("\n=== B. OpenAlex: Co-authorship networks ===")
TARGET_AUTHORS = [
    ("Ron Fouchier", "https://api.openalex.org/authors?search=Ron+Fouchier&per_page=5"),
    ("Marion Koopmans", "https://api.openalex.org/authors?search=Marion+Koopmans&per_page=5"),
    ("Anthony Fauci", "https://api.openalex.org/authors?search=Anthony+Fauci&per_page=5"),
    ("Jeremy Farrar", "https://api.openalex.org/authors?search=Jeremy+Farrar&per_page=5"),
]

openalex_data = {}
for name, url in TARGET_AUTHORS:
    print(f"  Searching {name}...")
    result = fetch_json(url)
    if result and result.get("results"):
        author = result["results"][0]  # Best match
        author_id = author.get("id")
        openalex_data[name] = {
            "id": author_id,
            "display_name": author.get("display_name"),
            "works_count": author.get("works_count"),
            "cited_by_count": author.get("cited_by_count"),
            "last_known_institution": author.get("last_known_institutions", [{}])[0].get("display_name")
        }
        # Fetch most cited works for co-author network
        author_uuid = author_id.split('/')[-1]
        works_url = f"https://api.openalex.org/works?filter=authorships.author.id:{author_uuid}&sort=cited_by_count:desc&per_page=10"
        works_result = fetch_json(works_url)
        if works_result and works_result.get("results"):
            openalex_data[name]["works"] = []
            for w in works_result["results"]:
                authorships = [au["author"]["display_name"] for au in w.get("authorships", [])]
                openalex_data[name]["works"].append({
                    "title": w.get("title"),
                    "doi": w.get("doi"),
                    "publication_year": w.get("publication_year"),
                    "cited_by_count": w.get("cited_by_count"),
                    "coauthors": authorships
                })
        print(f"    ID: {author_id}  |  Works: {author.get('works_count')}  |  Cited: {author.get('cited_by_count')}")
    else:
        print(f"    No results found for {name}")
    time.sleep(1)  # Rate limiting

openalex_path = os.path.join(OUTDIR, "openalex_coauthorships.json")
with open(openalex_path, "w", encoding="utf-8") as f:
    json.dump(openalex_data, f, ensure_ascii=False, indent=1)
print(f"  Saved co-authorship data to {openalex_path}")

# ─── C. FOIA / Public Reports ───────────────────────────────────────────
print("\n=== C. FOIA / Open Documents ===")
FOIA_SOURCES = [
    # Washington Post Fauci emails archive
    ("Fauci Emails (Washington Post archive)", "https://www.washingtonpost.com/context/fauci-emails/"),
    # Proximal Origin paper DOI
    ("Proximal Origin paper DOI", "https://doi.org/10.1038/s41591-022-01791-8"),
]

foia_data = []
for label, url in FOIA_SOURCES:
    print(f"  {label}: {url}")
    foia_data.append({"label": label, "url": url, "note": "Reference collected; full content requires interactive access"})

foia_path = os.path.join(OUTDIR, "foia_references.json")
with open(foia_path, "w", encoding="utf-8") as f:
    json.dump(foia_data, f, ensure_ascii=False, indent=1)
print(f"  Saved {len(foia_data)} references to {foia_path}")

print("\n=== AUTO-DOWNLOADER COMPLETE ===")
