import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
build_final_dataset.py — Compileert de complete Nederlandse/lab-origin dataset
uit alle ruwe pagina's. Produceert schone JSON en een leesbaar eindrapport.
"""
import json, re, os

RAW_PATH = os.path.join(ROOT, "raw_data.json")
OUT_JSON = os.path.join(ROOT, "nl_connections_dataset_v2.json")
OUT_TXT  = os.path.join(ROOT, "NL_EXTRACTIE_RAPPORT.md")

with open(RAW_PATH, "r", encoding="utf-8") as f:
    pages = json.load(f)

# ── Target terms and page identification ─────────────────────────────────
DUTCH_TERMS = re.compile(
    r"Koopmans|Fouchier|Erasmus|Viroscience|Netherlands|Dutch|"
    r"NRC Handelsbad|RIVM|VWS|LUMC|Utrecht|Osterhaus", re.I)
LAB_CORE_TERMS = re.compile(
    r"lab[- ]?(?:leak|escape|origin)|gain[- ]?of[- ]?function|GOF|"
    r"furin[- ]?cleavage|deliberate\s*(?:insert|engineer|manipulat)|"
    r"natural\s*origin|Shi\s*Zhengli|Zheng[- ]?Li\s*Shi|"
    r"Wuhan\s*(?:Institute\s*of\s*Virology|lab|WIV|Lab)|"
    r"Yoshi\s*Kawaoka|Kawaoka|Kristian\s*Anders[enon]|"
    r"Edward\s*Holmes|Peter\s*Daszak|EcoHealth|"
    r"Proximal\s*Origin|RaTG13|conference\s*call.*Feb|"
    r"Feb.*conference\s*call|Participants.*Feb", re.I)

# ── Collect all relevant pages ───────────────────────────────────────────
dutch_pages = []
lab_pages = []
hlab_pages = []

for p in pages:
    txt = p["text"] or ""
    if not txt.strip(): continue
    has_dutch = DUTCH_TERMS.search(txt)
    has_lab = LAB_CORE_TERMS.search(txt)
    if has_dutch:
        dutch_pages.append(p["page"])
    if has_lab:
        lab_pages.append(p["page"])
    if "lab leak" in txt.lower() or "lab-leak" in txt.lower():
        hlab_pages.append(p["page"])

# Combine unique pages of interest
all_relevant = sorted(set(dutch_pages + lab_pages + hlab_pages))

# ── Build structured dataset ─────────────────────────────────────────────
def extract_context(txt, term_list, window=120):
    """Extract context windows for first occurrence of each term."""
    results = []
    tl = txt.lower()
    for term in term_list:
        if term.lower() in tl:
            idx = tl.index(term.lower())
            start = max(0, idx - window)
            end = min(len(txt), idx + len(term) + window)
            ctx = re.sub(r'\s+', ' ', txt[start:end]).strip()
            results.append({"term": term, "context": ctx})
    return results

# ── Output structure ─────────────────────────────────────────────────────
dataset = {
    "meta": {
        "source": "2026.07.24_Tonys-Diary-Package.pdf (Fauci Diary, Rand Paul release)",
        "extraction_date": "2026-07-30",
        "total_pages": 1141,
        "dutch_relevant_pages": sorted(dutch_pages),
        "lab_origin_pages": sorted(lab_pages),
        "lab_leak_mention_pages": sorted(hlab_pages),
        "unique_relevant_pages": all_relevant,
    },
    "critical_pages": {},
    "feb1_conference_call": {
        "date": "1 February 2020",
        "convened_by": "Anthony Fauci (NIAID)",
        "trigger": "Furin cleavage site analysis — Fauci called together scientists after receiving sequence data",
        "participants": [],
        "outcome": "No consensus. Fouchier argued natural origin; Andersen/Holmes/Rambaut faction favored deliberate insertion as possible.",
        "source_page": 14,
        "context": "This call is Fauci's contemporaneous diary record. It documents the earliest known high-level discussion among international virologists about the furin cleavage site."
    },
    "pages": {},
    "dutch_entities": {
        "persons": [
            {"name": "Ron Fouchier", "role": "Deputy Head, Dept of Viroscience, Erasmus MC", "pages": [14], "position_on_origin": "Argued furin cleavage site could occur naturally (page 14)"},
            {"name": "Marion Koopmans (M.P.G. Koopmans)", "role": "Head of Dept of Viroscience, Erasmus MC", "pages": [14], "position_on_origin": "Not explicitly stated in Fauci's account (page 14)"},
            {"name": "Bas Blokker", "role": "Journalist, NRC Handelsblad", "pages": [768], "position_on_origin": "Interviewed Fauci for Dutch newspaper"},
        ],
        "organizations": [
            {"name": "Erasmus MC / Erasmus Medical Center", "type": "academic medical center", "pages": [14], "dept": "Viroscience"},
            {"name": "Viroscience", "type": "research department", "pages": [14], "parent": "Erasmus MC"},
            {"name": "NRC Handelsblad", "type": "newspaper", "pages": [768], "note": "Dutch newspaper; Fauci interview reported as NRC Handelsbad (typo in PDF)"},
        ]
    },
    "network": {
        "nodes": [],
        "edges": []
    }
}

# Extract critical pages verbatim
CRITICAL_DESC = {
    13: "Jan 31/Feb 1 lead-up — GOF conspiracy theories mentioned",
    14: "Feb 1 Conference Call — FULL participant list + disagreement",
    767: "Fauci reviews Jan 31/Feb 1 notes re: furin cleavage site",
    805: "Kristian Andersen et al. preprint arguing natural emergence vs lab leak",
}
for pg in [13, 14, 767, 805]:
    for p in pages:
        if p["page"] == pg:
            dataset["critical_pages"][str(pg)] = {
                "page": pg,
                "description": CRITICAL_DESC.get(pg, ""),
                "full_text": p["text"] or ""
            }
            break

# Page 14: full participant list parsing
p14 = dataset["critical_pages"].get("14", {}).get("full_text", "")
part_match = re.search(r"Conference call at 2:00 PM with Jeremy(.*?)(?=There was not total agreement)", p14, re.DOTALL)
if part_match:
    block = part_match.group(1)
    entries = re.findall(r"[•\-\*]\s*(.+?)(?=(?:\n\s*[•\-\*])|\Z)", block, re.DOTALL)
    for ent in entries:
        ent = ent.strip().replace('\n', ' ')
        if not ent:
            continue
        name_match = re.match(r"((?:[A-Z]\.?\s*)+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", ent)
        name = name_match.group(1).strip() if name_match else ent.split(",")[0].strip()
        is_dutch = "Erasmus" in ent or "NL" in ent.upper() or "Koopmans" in ent or "Fouchier" in ent
        dataset["feb1_conference_call"]["participants"].append({
            "name": re.sub(r'\s+', ' ', name),
            "full_entry": ent,
            "is_dutch": is_dutch,
            "org": "Erasmus MC" if is_dutch else ""
        })

# Disagreement text
disag = re.search(r"(There was not total agreement[^.]+\.)", p14, re.DOTALL)
if disag:
    dataset["feb1_conference_call"]["disagreement_verbatim"] = disag.group(1).strip()
disc2 = re.search(r"(Ron Fouchier said[^.]+\.)", p14, re.DOTALL)
if disc2:
    dataset["feb1_conference_call"]["fouchier_position_verbatim"] = disc2.group(1).strip()

# Extract every relevant page
for p in pages:
    pg = p["page"]
    txt = p["text"] or ""
    if pg not in all_relevant:
        continue
    pdata = {
        "page": pg,
        "is_dutch": pg in dutch_pages,
        "is_lab_origin": pg in lab_pages,
        "is_lab_leak_mention": pg in hlab_pages,
        "contexts": {},
    }
    # Extract term-specific contexts
    for term_list, cat in [
        (["Koopmans", "Fouchier", "Erasmus", "Viroscience", "Netherlands", "NRC Handelsbad"], "dutch"),
        (["GOF", "gain of function", "furin cleavage", "lab leak", "lab-leak",
          "Shi Zhengli", "Wuhan", "Kawaoka", "Daszak", "EcoHealth",
          "natural origin", "deliberate insertion"], "lab"),
        (["conference call", "January 31", "February 1", "31 January", "1 February"], "timeline"),
    ]:
        contexts = extract_context(txt, term_list)
        if contexts:
            pdata["contexts"][cat] = contexts
    dataset["pages"][str(pg)] = pdata

# ── Build network ────────────────────────────────────────────────────────
PERSONS_KNOWN = {
    "Anthony Fauci": ("person", False),
    "Ron Fouchier": ("person", True),
    "Marion Koopmans": ("person", True),
    "Bas Blokker": ("person", True),
    "Francis Collins": ("person", False),
    "Jeremy Farrar": ("person", False),
    "Kristian Andersen": ("person", False),
    "Edward Holmes": ("person", False),
    "Andrew Rambaut": ("person", False),
    "Christian Drosten": ("person", False),
    "Robert Garry": ("person", False),
    "Patrick Vallance": ("person", False),
    "Mike Ferguson": ("person", False),
    "Shi Zhengli": ("person", False),
    "Yoshi Kawaoka": ("person", False),
    "Peter Daszak": ("person", False),
    "Bob Redfield": ("person", False),
    "Alex Azar": ("person", False),
    "Donald Trump": ("person", False),
    "Rand Paul": ("person", False),
}

ORGS_KNOWN = {
    "Erasmus MC": ("organization", True),
    "Viroscience": ("organization", True),
    "NRC Handelsblad": ("organization", True),
    "NIH": ("organization", False),
    "NIAID": ("organization", False),
    "CDC": ("organization", False),
    "WHO": ("organization", False),
    "Wellcome Trust": ("organization", False),
    "Scripps Research": ("organization", False),
    "EcoHealth Alliance": ("organization", False),
}

nodes = []
edges = []
seen_nodes = set()

def ensure_node(name, ntype="person", is_dutch=False):
    if name not in seen_nodes:
        seen_nodes.add(name)
        nodes.append({"id": name, "label": name, "type": ntype, "is_dutch": is_dutch})

def add_edge(src, tgt, rel, page, context=""):
    edges.append({"source": src, "target": tgt, "relation": rel, "page": page, "context": context[:200]})

# Add all known entities
for name, (ntype, dutch) in {**PERSONS_KNOWN, **ORGS_KNOWN}.items():
    ensure_node(name, ntype, dutch)

# Structure: Feb 1 call
ensure_node("Feb 1 Conference Call", "event", False)
add_edge("Anthony Fauci", "Feb 1 Conference Call", "CONVENED", 14, "")
for p in dataset["feb1_conference_call"]["participants"]:
    n = p["name"]
    ensure_node(n)
    if p["org"]:
        ensure_node(p["org"], "organization", "Erasmus" in p["org"])
        add_edge(n, p["org"], "MEMBER_OF", 14, p["full_entry"])
    add_edge(n, "Feb 1 Conference Call", "PARTICIPATED_IN", 14, p["full_entry"])

# Factions
ensure_node("Natural Origin Position", "position", False)
ensure_node("Deliberate Insertion Position", "position", False)
for natural_name in ["Ron Fouchier", "Christian Drosten"]:
    if natural_name in PERSONS_KNOWN:
        add_edge(natural_name, "Natural Origin Position", "SUPPORTED", 14,
                 "Fouchier: 'sure this could occur naturally'; Drosten agreed")
for deliberate_name in ["Kristian Andersen", "Edward Holmes", "Andrew Rambaut",
                         "Robert Garry", "Mike Ferguson", "Anthony Fauci",
                         "Francis Collins", "Jeremy Farrar", "Patrick Vallance"]:
    if deliberate_name in PERSONS_KNOWN:
        add_edge(deliberate_name, "Deliberate Insertion Position", "SUPPORTED", 14,
                 "'rest felt that deliberate insertion was possible' given Shi Zhengli's GOF work")
# Shi Zhengli linked to the discussion
ensure_node("Shi Zhengli")
add_edge("Shi Zhengli", "Deliberate Insertion Position", "IMPLICATED_BY", 14,
         "Shi Zhengli working for years in GOF in coronaviruses to allow adaptation of spike protein")

# Page 768: NRC interview
ensure_node("Bas Blokker")
add_edge("Bas Blokker", "NRC Handelsblad", "EMPLOYED_BY", 768, "")
add_edge("Anthony Fauci", "Bas Blokker", "INTERVIEWED_BY", 768, "NRC Handelsblad interview")

dataset["network"]["nodes"] = nodes
dataset["network"]["edges"] = edges

# ── Write JSON ────────────────────────────────────────────────────────────
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=1)
print(f"[output] {OUT_JSON}")

# ── Write text report ────────────────────────────────────────────────────
report = f"""# Extractierapport: Nederlandse connecties & Lab-origin discussie in Tony's Diary (Fauci)

**Bron:** `2026.07.24_Tonys-Diary-Package.pdf` (1141 pp, ~69 MB)
**Vrijgave:** Chairman Rand Paul, U.S. Senate
**Extractiedatum:** 2026-07-30

---

## 1. Samenvatting

In het dagboek van Dr. Anthony Fauci (NIAID-directeur) zijn **{len(all_relevant)} pagina's** geïdentificeerd die relevant zijn voor Nederlandse connecties en de lab-origin discussie. Het centrale document is de **conference call van 1 februari 2020** (p14), waarin Fauci 12 internationale wetenschappers bijeenriep om de **furin cleavage site** en de mogelijkheid van **deliberate insertion** te bespreken.

### Nederlandse actoren

| Naam | Functie | Pagina |
|------|---------|--------|
| **Ron Fouchier** | Deputy Head, Dept of Viroscience, Erasmus MC | p14 |
| **Marion Koopmans (M.P.G. Koopmans)** | Head of Dept of Viroscience, Erasmus MC | p14 |
| **Bas Blokker** | Journalist, NRC Handelsblad | p768 |

### Sleutelvondst: Feb 1 Conference Call (p14)

Fauci beschrijft hoe hij op **31 januari 2020** een telefoontje kreeg van Jeremy Farrar (Wellcome Trust), waarna hij op **1 februari 2020 om 14:00** een videoconference belegde met:

{chr(10).join(f'- **{p["name"]}** ({p["full_entry"][:80]}...)' + (' 🇳🇱' if p["is_dutch"] else '') for p in dataset["feb1_conference_call"]["participants"])}

**Geen consensus.** Twee kampen:
- **Natuurlijke oorsprong:** Ron Fouchier (Erasmus MC) + Christian Drosten (Charité). Fouchier als "original GOF person with Yoshi Kawaoka" stelde dat furin cleavage site natuurlijk kon ontstaan.
- **Deliberate insertion mogelijk:** Fauci, Collins, Andersen, Holmes, Rambaut, Garry, Ferguson, Farrar, Vallance — vanwege Shi Zhengli's GOF-werk aan spike-eiwit-ACE2-receptor-adaptatie in Wuhan.

**Koopmans' positie wordt NIET expliciet genoemd** in Fauci's aantekeningen.

---

## 2. Chronologisch overzicht relevante pagina's

| Pagina | Datum (entry) | Relevantie | Nederlandse termen |
|--------|--------------|------------|-------------------|
| 13 | jan 2020 | Pre-call context: GOF conspiracy theories, "Indian investigators HIV sequences inserted" | - |
| **14** | **1 feb 2020** | **Conference call participant list + disagreement** | **Fouchier, Koopmans, Erasmus MC, Viroscience** |
| 39 | apr 2020 | GOF mention | - |
| 118 | jul 2020 | GOF mention | - |
| 720 | mei 2021 | Lab leak theory article (Foreign Policy) | - |
| 740 | jun 2021 | "Fringe press scaling up GOF rhetoric" | - |
| 750-754 | jun 2021 | Lab leak discussion, FOX News attacks | - |
| 765-768 | jun 2021 | **Fauci's terugblik op jan31/feb1 call** + **NRC interview** | **NRC Handelsbad** |
| 776 | jun 2021 | Politico: Trump officials pushed lab leak theory | - |
| 784 | jun 2021 | Lab leak, Chinese cover-up allegation | - |
| 788 | jun 2021 | NYT Sway interview: Fauci on lab leak | - |
| 792 | jun 2021 | Scientists raised lab leak possibility Feb 2020 | - |
| 802-805 | jul 2021 | **Andersen et al. preprint: natural emergence vs lab leak** | - |
| 813 | jul 2021 | Senator Marshall questions furin cleavage site | - |
| 833 | aug 2021 | GOP report lab leak cause; NIH role | - |
| 863 | sep 2021 | Intelligence community: natural vs lab leak | - |
| 888-893 | sep 2021 | Molecular analysis shows lab leak impossible; Jesse Bloom | - |
| 911 | okt 2021 | GOF: Rand Paul 2 Pinocchios | - |
| 922-927 | nov 2021 | Worobey Science paper, Alina Chan critique | - |
| 935 | dec 2021 | Furin cleavage site mutations (Delta/Omicron) | - |
| 944-958 | jun 2022 | Fauci-endorsed Chinese donation; lab leak hearing | - |
| 980-995 | jul 2022 | Biden tests positive; Worobey/Andersen paper | - |
| 1064 | sep 2022 | Jeffrey Sachs equates lab leak vs natural | - |
| 1085 | okt 2022 | GOF experiment discussion; IDSA meeting | - |
| 1103 | nov 2022 | ProPublica/Vanity Fair lab leak theory critique | - |
| 1138 | dec 2022 | Elon Musk tweets; GOF research funding claims | - |

---

## 3. Extractie van de Feb 1 call (p14 — letterlijk)

### Deelnemerslijst (12 personen + Fauci):
{chr(10).join(f'- **{p["name"]}**' + (' 🇳🇱' if p["is_dutch"] else '') + f' — {p["full_entry"]}' for p in dataset["feb1_conference_call"]["participants"])}

### Fauci's beschrijving van het meningsverschil:
> "{dataset['feb1_conference_call'].get('disagreement_verbatim', 'N/A')}"

> "{dataset['feb1_conference_call'].get('fouchier_position_verbatim', 'N/A')}"

### Fauci's noot over Shi Zhengli:
> "...Dr. Zheng-Li Shi at the University of Wuhan has been working for years in GOF in coronaviruses to allow adaptation of the spike protein to bind to the human ACE2 receptor"

---

## 4. Terugblik Fauci op Jan 31/Feb 1 call (p767 — letterlijk)

> "...since I am not an evolutionary biologist I called together by phone a group of prominent evolutionary biologists and virologists on January 31st and February 1st , 2020... this was a possibility and so I didn't change my mind currently by saying that a lab leak is a possibility since I was talking about it openly back then."

---

## 5. Pagina 768 — NRC Handelsblad interview

> "PRESS: Interview with Dutch newspaper NRC Handelsbad — Bas Blokker interviewer; Smithsonian Channel TV Documentary (Israel) — 'Vaxxed Nation'... Blinken casts doubt on methodology of coronavirus lab-leak report Reuters... Lawrence Livermore Lab report... lab leak hypothesis"

---

## 6. Netwerkoverzicht ({len(nodes)} nodes, {len(edges)} edges)

| Entiteit | Type | Nederlands |
|----------|------|-----------|
{chr(10).join(f"| {n['id']:40s} | {n['type']:15s} | {'🇳🇱' if n['is_dutch'] else ''} |" for n in nodes)}

### Kanttekening bij data-kwaliteit:
- **Fouchier en Koopmans** worden alleen op p14 genoemd. Koopmans' positie in het natural-vs-deliberate debat wordt **niet** vermeld door Fauci.
- Fouchier wordt gekarakteriseerd als "original GOF person" — dit is Fauci's karakterisering.
- De Feb 1 call vond plaats op basis van een telefoontje van Jeremy Farrar op **31 januari 2020**, zoals beschreven op **p767**.
- Het dagboek is een **contemporaine bron** (geen retrospectief), maar wel geschreven door Fauci zelf (subjectiviteit mogelijk).

---

## 7. Blinde vlekken & aanbevolen verificatie

1. **Wat was Koopmans' positie?** — Fauci noteert haar niet in de voor/nadelen.
2. **Wat was Farrar's rol in het beleggen van de call?** — Fauci: "Jeremy Farrar who conference called me on January 31st" (p767).
3. **EcoHealth / Daszak connectie** — Worden met name genoemd in latere lab-leak discussies (zie pages 792, 805, 833, 888) maar niet in de Feb 1 call.
4. **Verificatie externe bronnen:** Vraag op bij Erasmus MC (Viroscience) of Fouchier/Koopmans eigen aantekeningen van deze call hebben. Check PubMed voor publicaties van de deelnemers in de week voor 1 feb 2020.
5. **Open vragen:** Waarom was Koopmans uitgenodigd maar wordt haar positie niet genoteerd? Was zij als viroloog/veterinair patholoog aanwezig voor de zoönotische (dier-mens) expertise?

---

## 8. Outputbestanden

| Bestand | Beschrijving |
|---------|-------------|
| `nl_connections_dataset_v2.json` | Volledige gestructureerde dataset (API/networkx-klare JSON) |
| `nl_lab_extraction_v2.json` | Eerdere extractie (v1) met alle passages per pagina |
| `NL_EXTRACTIE_RAPPORT.md` | Dit rapport |

---

*Einde extractierapport. Geëxtraheerd uit 2026.07.24_Tonys-Diary-Package.pdf. Geen conclusies over schuld of onschuld — alleen gestructureerde vastlegging van feiten uit het brondocument.*
"""

with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write(report)
print(f"[output] {OUT_TXT}")
print(f"\nStats: {len(all_relevant)} relevant pages | {len(nodes)} nodes | {len(edges)} edges")
print(f"Dutch pages: {len(dutch_pages)} | Lab-origin pages: {len(lab_pages)} | Lab-leak pages: {len(hlab_pages)}")
