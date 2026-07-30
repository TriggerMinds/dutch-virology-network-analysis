# OPERATIONAL INVESTIGATIVE MANUAL & HANDS-ON PROMPTBOOK

**Document Titel:** Operationele Handleiding, Terminal Opdrachten & LLM Prompts voor Forensisch Onderzoek en Waarheidsvinding  
**Datum:** 30 juli 2026  
**Versie:** 1.6 (TEAMDYNAMICA Compliant — Diepte-Audit Prompts Vrijgegeven)  
**Doel:** Een praktische, direct bruikbare gids met werkende terminal-opdrachten, Python-scripts, SQL-queries en gespecialiseerde LLM-onderzoeksprompts om de **verzwegen Nederlandse dossiers** boven te krijgen die buiten het zicht van de mainstream media zijn gebleven.

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

## 2. KANT-EN-KLARE AI / LLM PROMPTS VOOR HET BLOOTLEGGEN VAN VERZWEGEN DOSSIERS IN NEDERLAND

Deze prompts zijn specifiek ontworpen om AI-assistenten en subagenten op te dragen diepgaand forensisch onderzoek te doen naar **feiten over Nederland die niet door de mainstream media (NOS, Volkskrant, NRC, RTL) zijn behandeld**:

---

### PROMPT 1: Formuleer een Gericht Woo-Bezwaarschrift tegen Zwartlakking onder Art. 5.2
```text
Opdracht voor AI Onderzoeker:
Gebruik de documenten in docs/MASTER_UNTURNED_STONES_AUDIT.md en docs/DUTCH_ANOMALIES_FORENSIC_AUDIT.md.
Stel een formeel juridisch Woo-bezwaarschrift op aan het Ministerie van VWS gericht tegen de zwartlakking onder Art. 5.2 Woo op dossier Woo/VWS-2023-0042 (Februari 2020 OMT-notulen en e-mailwisselingen met Erasmus MC).
Onderbouw met jurisprudentie van de Raad van State waarom "persoonlijke beleidsopvattingen" niet mogen worden ingeroepen bij feitelijke wetenschappelijke onderbouwing, adviesstructuren en internationale netwerkafstemming.
Hanteer strikt de TEAMDYNAMICA v1.5 standaarden.
```

---

### PROMPT 2: Cross-Border EU Vergelijking (Duitse RKI-Protokolle vs. RIVM/OMT Narratief)
```text
Opdracht voor AI Onderzoeker:
Analyseer de bevindingen in docs/EU_MEMBER_STATES_FORENSIC_DOSSIER.md.
Vergelijk de RKI-Protokolle (Duitsland, mei/juli 2024 unredacted release) met de Nederlandse OMT-adviezen uit maart 2020 inzake mondkapjesverplichtingen en risico-escalatie.
Identificeer exact welke wetenschappelijke twijfels die intern bij het RKI speelden (bijv. effectiviteit FFP2-maskers voor de bevolking, avondklok) door het RIVM/OMT publiekelijk werden verzwegen ter bescherming van de beleidslijn.
Noem namen, datums, documentnummers en HTTP 200 OK geverifieerde bron-links.
```

---

### PROMPT 3: Forensische Audit op de Viroscience B.V. Exploitatielus & Octrooi US6849435B2
```text
Opdracht voor AI Onderzoeker:
Onderzoek de private/publieke verstrengeling rond de afdeling Viroscience (Erasmus MC) en de Besloten Vennootschap Viroscience B.V. (KvK #24416174).
Mappeer hoe octrooi US6849435B2 (BsmBI/BsaI IIS restrictie-enzym reverse genetics door Fouchier/Osterhaus) en gerelateerde coronavirus-patenten (WO2006131370A2) commercieel worden geëxploiteerd.
Analyseer de juridische en ethische belangenverstrengeling: OMT-leden die de overheid adviseren over virus-surveillance en testprotocollen, terwijl hun private entiteiten en universitaire afdelingen patenthouder en licentieverlener zijn.
Stel een gedetailleerd verhoor-dossier op voor de Parlementaire Enquêtecommissie Corona.
```

---

### PROMPT 4: Reconstructie van de 48-Uurs Corman-Drosten PCR Snelkoppeling & ECDC Belangen
```text
Opdracht voor AI Onderzoeker:
Reconstrueer de tijdslijn van de indiening, peer-review en publicatie van de Corman-Drosten PCR-paper in Eurosurveillance (21-23 januari 2020; DOI: 10.2807/1560-7917.ES.2020.25.3.2000045).
Co-auteurs: Chantal Reusken (RIVM/Erasmus MC), Marion Koopmans (Erasmus MC), Christian Drosten (Charité), Olfert Landt (TIB Molbiol).
Geef antwoord op de vragen die de Nederlandse media lieten liggen:
1. Hoe kon een peer-review in <24 uur plaatsvinden zonder dat het team beschikte over een viraal geïsoleerd Wuhan-sample?
2. Wat was de redactionele rol van Koopmans en Drosten bij Eurosurveillance (uitgegeven door het ECDC te Stockholm)?
3. Wat waren de commerciële belangen van co-auteur Olfert Landt (TIB Molbiol), die direct miljoenen testkits verkocht na publicatie?
Formuleer een uitputtend WOO/FOIA-verzoek aan het ECDC te Stockholm voor de openbaarmaking van de redactionele review-logboeken.
```

---

### PROMPT 5: De Circulaire AIVD Inlichtingen-Lus (Kamerstuk 25 295 nr 1180 Audit)
```text
Opdracht voor AI Onderzoeker:
Onderzoek Kamerstuk 25 295 nr 1180 en het AIVD Jaarverslag 2020 waarin de Nederlandse inlichtingen- en veiligheidsdienst concludeerde dat er "geen aanwijzingen waren voor een laboratorium-oorsprong van SARS-CoV-2".
Toon de circulaire redenering aan: de AIVD beschikte niet over eigen virologische wet-lab capaciteit en raadpleegde voor haar analyse de experts van RIVM en Erasmus MC (Marion Koopmans & Ron Fouchier).
Leg uit hoe de AIVD fungeerde als echoput van de exacte onderzoekers die op de Feb 1 conference call zaten en direct belang hadden bij het beveiligen van hun Gain-of-Function onderzoeksagenda.
Schrijf een parlementaire vraagstelling voor de Commissie voor de Inlichtingen- en Veiligheidsdiensten (CIVD).
```

---

### PROMPT 6: Subsidie-Accumulatie & Belangenverstrengeling bij ZonMw & ECRAID (€67,6M+)
```text
Opdracht voor AI Onderzoeker:
Raadpleeg data/network_data.db en docs/DUTCH_ANOMALIES_FORENSIC_AUDIT.md.
Mappeer de financiële stromen en bestuursfuncties tussen adviesorganen (OMT) en subsidieverstrekkers (ZonMw / EU CORDIS):
1. Arfan Ikram: Voorzitter ZonMw én bestuurder bij het Pandemic Disaster Preparedness Center (PDPC). Toon de schending van Art. 2:4 Algemene Wet Bestuursrecht (AWB) aan bij het toewijzen van €12M publiek geld aan zijn eigen consortium.
2. Marc Bonten: Kernlid OMT én CEO van de ECRAID Foundation (EU GA#965313: €20,0M).
3. Marion Koopmans: Adviseur OMT én coördinator van VEO (€14,6M), COMPARE (€10,3M), PDPC (€12,0M), NCOH (€4,2M) en DURABLE (€5,0M).
Stel een kwantitatief diagram op van de €67,6M+ subsidie-accumulatie gecommitteerd in 2019-2020.
```

---

### PROMPT 7: Oversterfte Microdata Audit & Het Gat van 20.800+ Doden
```text
Opdracht voor AI Onderzoeker:
Raadpleeg data/downloads/open_macro_data.json en docs/DUTCH_ANOMALIES_FORENSIC_AUDIT.md.
Stel een vergelijkende audit op tussen de officiële RIVM/CBS oversterftecijfers (22.500 tot 24.200 geregistreerde COVID-doden) en het forensische epidemiologische model van Meester, Aukema, Jacobs & Bonte (45.000+ oversterfte).
Analyseer waarom het RIVM 20.800+ niet-uitgelegde doden toeschrijft aan "ongediagnosticeerde COVID" terwijl de temporele clustering sterk gecorreleerd is met vaccinatie-uitrolgolven en zorgmijding.
Formuleer een juridisch afdwingbaar verzoek onder Artikel 89 van de AVG (GDPR) om gekoppelde, gepseudonimiseerde individuele microdata (sterftedatum + doodsoorzaak + vaccinatiestatus + ziekenhuisopname) beschikbaar te stellen voor onafhankelijk wetenschappelijk onderzoek.
```

---

### PROMPT 8: De 107-Dagen Narrative Lag & Media-Coördinatie Audit
```text
Opdracht voor AI Onderzoeker:
Analyseer de temporele vertraging (narrative lag) van 107 dagen tussen de interne paniek over de furin cleavage site (31 januari 2020, ontdekt door David Robertson) en de eerste serieuze bespreking in de Nederlandse pers (mei/juni 2020).
Onderzoek de communicatielijnen tussen het Ministerie van VWS (Directie Communicatie / Denktank Desinformatie) en wetenschapsjournalisten (zoals Maarten Keulemans, de Volkskrant).
Toon aan hoe kritische geluiden en lab-leak scenario's stelselmatig werden geframed als "gevaarlijke complottheorieën" conform de schriftelijke waarschuwing van Marion Koopmans aan Jeremy Farrar (8 februari 2020: "highlighting FCS will generate conspiracy theories").
```

---

## 3. COMPLIANCE & VERIFICATIE CHECKLIST

- [x] **Strikte URL-verificatie:** Alle geciteerde links retourneren HTTP 200 OK.
- [x] **SHA-256 Provenance:** Alle PDF's hebben geregistreerde controlesommen in `data/checksums.sha256`.
- [x] **11 Biases Uiteschakeld:** Geen verzachtende taal, geen schijnbalans.
- [x] **4-Assen Kwalificatie:** Elk resultaat gelabeld op *Intentie*, *Causaliteit*, *Verantwoordelijkheid* en *Timing*.
- [x] **Coverage Status Dictionary:** Elke entiteit gelabeld met `VERIFIED_PUBLIC`, `STATUTORY_RESTRICTED` of `PENDING_APPEAL`.

---

*Handleiding verankerd in de repository conform TEAMDYNAMICA v1.5 richtlijnen.*
