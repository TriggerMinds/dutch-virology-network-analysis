# OPERATIONAL INVESTIGATIVE MANUAL & HANDS-ON PROMPTBOOK

**Document Titel:** Operationele Handleiding, Terminal Opdrachten & LLM Prompts voor Forensisch Onderzoek en Waarheidsvinding  
**Datum:** 30 juli 2026  
**Versie:** 1.5 (TEAMDYNAMICA Compliant)  
**Doel:** Een praktische, direct bruikbare gids met werkende terminal-opdrachten, Python-scripts, SQL-queries en LLM-onderzoeksprompts om álle onopgelichte stenen in het COVID-19 dossier boven te krijgen.

---

## 1. SNELSTART & VOLLEDIGE PIJPLIJN UITVOERING

Voer de volgende opdrachten uit in de terminal (`pwsh`, `bash` of `cmd`) om het volledige systeem te initialiseren, datasets op te halen, FTS5-zoekindexen te bouwen en de interactieve visualisatie te genereren:

```bash
# 1. Omgeving installeren & afhankelijkheden controleren
pip install -r requirements.txt

# 2. Meertalig Documentenarchief Initialiseren & PDF's Inlezen
python src/init_archive_db.py
python src/ingest_pdf_archive.py

# 3. Data Engineering Modules Uitvoeren (Deltas, Open Macro-Data, Academic & CORDIS)
python src/track_redaction_deltas.py
python src/fetch_open_macro_data.py
python src/fetch_open_academic_data.py
python src/sync_cordis_open_data.py
python src/verify_open_documents.py

# 4. Multiplex Knowledge Graph & Coverage Status Dictionary Herbouwen
python src/setup_multiplex_db.py
python src/build_coverage_dictionary.py
python build_web_app.py

# 5. Unit Tests Uitvoeren
python tests/test_archive_db.py
```

---

## 2. WAT KAN JE HIER ALLEMAAL MEE DOEN? (TOEPASSINGEN)

Met deze toolkit beschik je over een **onafhankelijk, verifieerbaar forensisch instrumentarium**. Hiermee kun je:

1. **Onweerlegbare Woo- & FOIA-Verzoeken Formuleren:**  
   Gebruik de `redaction_deltas` module en de *Top 7 Unturned Stones Matrix* om haarscherp te specificeren welke exacte e-mail bijlagen (bijv. Farrar-Fouchier/Koopmans Feb 2020) of OMT-notulen gevraagd worden.

2. **Parlementaire Enquête & Verhoor-Voorbereiding:**  
   Genereer tijdslijnen en netwerkkaarten van actoren met dubbelrollen (zoals OMT-leden die subsidies ontvingen van ZonMw/EU voor door hen geadviseerde consortia).

3. **Zwartlak-Analyse (Redaction Deltas):**  
   Vergelijk eerdere en latere Woo-vrijgaven pagina-voor-pagina om automatisch te zien welke zinnen de overheid aanvankelijk weglakte op Art. 5.2 Woo.

4. **Internationale Vergelijkende Analyse (EU Cross-Border):**  
   Koppel Nederlandse OMT-besluiten aan de Duitse *RKI-Protokolle*, de Italiaanse *Bergamo Inchiesta* en de Franse Senaatsrapporten om gesynchroniseerde narratiefsturing aan te tonen.

---

## 3. KANT-EN-KLARE TERMINAL OPDRACHTEN & PYTHON SCRIPTS

### A. Full-Text Zoeken via SQLite FTS5 in Python

```python
# Zoek direct in alle ingelezen PDF-documenten en Woo-dossiers
from src.search_archive import search_by_keyword

# Voorbeeld 1: Zoek naar discussies over de furin cleavage site
results = search_by_keyword("furin OR cleavage", language_code="nl")
for r in results:
    print(f"[{r['jurisdiction']}] {r['title']} (Hash: {r['sha256_hash'][:12]}...)")
    print(f"Snippet: {r['snippet']}\n")

# Voorbeeld 2: Zoek op actoren
fauci_docs = search_by_keyword('"Proximal Origin" AND (Fouchier OR Koopmans)')
print(f"Aantal gevonden documenten: {len(fauci_docs)}")
```

### B. Zwartlak Verschillen Opvragen (Redaction Deltas)

```python
# Bekijk nieuw vrijgekomen zinnen tussen Woo-versies
import sqlite3

conn = sqlite3.connect("data/archive.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT document_title, page_num, release_date, unredacted_text
    FROM redaction_deltas
    ORDER BY release_date DESC;
""")
for row in cursor.fetchall():
    print(f"Document: {row[0]} | Pagina: {row[1]} | Datum: {row[2]}")
    print(f"Vrijgekomen tekst: {row[3]}\n")
conn.close()
```

### C. Subsidie- en Financiële Stromen Analyseren (€67,6M+)

```python
# Haal alle EU CORDIS & NIH grants op voor Erasmus MC en ECRAID
import sqlite3

conn = sqlite3.connect("data/network_data.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT grant_id, project_title, amount_eur_usd, recipient_org, principal_investigator
    FROM financial_grants
    ORDER BY amount_eur_usd DESC;
""")
for row in cursor.fetchall():
    print(f"[{row[0]}] {row[1]}")
    print(f"Bedrag: €/{row[2]:,.2f} | Ontvanger: {row[3]} | PI: {row[4]}\n")
conn.close()
```

---

## 4. GEMACHTIGDE AI & SUBAGENT INVESTIGATIVE PROMPTS

Kopieer en plak de onderstaande prompts in je AI-assistent (of subagenten) om specifieke waarheidsvindings-opdrachten te laten uitvoeren:

### Prompt 1: Genereren van een Gericht Woo-Bezwaarschrift (Art. 5.2 Bestrijding)
```text
Opdracht voor AI Onderzoeker:
Gebruik de documenten in docs/MASTER_UNTURNED_STONES_AUDIT.md en docs/DUTCH_ANOMALIES_FORENSIC_AUDIT.md.
Stel een formeel juridisch Woo-bezwaarschrift op aan het Ministerie van VWS gericht tegen de zwartlakking onder Art. 5.2 Woo op het dossier Woo/VWS-2023-0042 (Februari 2020 OMT-notulen en e-mailwisselingen met Erasmus MC).
Onderbouw met jurisprudentie van de Raad van State waarom "persoonlijke beleidsopvattingen" niet mogen worden ingeroepen bij feitelijke wetenschappelijke onderbouwing en internationale advisering.
Hanteer strikt de TEAMDYNAMICA v1.5 standaarden.
```

### Prompt 2: Cross-Border EU Vergelijking (RKI vs. RIVM)
```text
Opdracht voor AI Onderzoeker:
Analyseer de bevindingen in docs/EU_MEMBER_STATES_FORENSIC_DOSSIER.md.
Vergelijk de RKI-Protokolle (Duitsland, mei/juli 2024 unredacted release) met de Nederlandse OMT-adviezen uit maart 2020 inzake mondkapjesverplichtingen en risico-escalatie.
Identificeer exact welke wetenschappelijke twijfels die intern bij het RKI speelden (bijv. effectiviteit FFP2-maskers) door het RIVM/OMT publiekelijk werden verzwegen.
Noem namen, datums, documentnummers en HTTP 200 OK geverifieerde bron-links.
```

### Prompt 3: Oversterfte Statistisch Forensisch Audit
```text
Opdracht voor AI Onderzoeker:
Raadpleeg data/downloads/open_macro_data.json en docs/DUTCH_ANOMALIES_FORENSIC_AUDIT.md.
Stel een vergelijkende analyse op tussen het officiële RIVM/CBS oversterfterapport (22.500 tot 24.200 COVID-doden) en het forensische model van Meester, Aukema, Jacobs & Bonte (45.000+ oversterfte).
Mappeer exact welke data-elementen ontbreken (het gat van 20.800+ doden) en schrijf een specificatie voor een AVG Art. 89 wetenschappelijk microdata-verzoek bij het CBS.
```

---

## 5. VOLLEDIGE COMPLIANCE CHECKLIST

- [x] **Strikte URL-verificatie:** Alle geciteerde links retourneren HTTP 200 OK.
- [x] **SHA-256 Provenance:** Alle PDF's hebben geregistreerde controlesommen in `data/checksums.sha256`.
- [x] **11 Biases Uiteschakeld:** Geen verzachtende taal, geen schijnbalans.
- [x] **4-Assen Kwalificatie:** Elk resultaat gelabeld op *Intentie*, *Causaliteit*, *Verantwoordelijkheid* en *Timing*.
- [x] **Coverage Status Dictionary:** Elke entiteit gelabeld met `VERIFIED_PUBLIC`, `STATUTORY_RESTRICTED` of `PENDING_APPEAL`.

---

*Handleiding verankerd in de repository conform TEAMDYNAMICA v1.5 richtlijnen.*
