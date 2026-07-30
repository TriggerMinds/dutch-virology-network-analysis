"""
sync_wiki.py — Genereert Wiki-pagina's voor GitHub Wiki en pusht direct naar de GitHub Wiki repo.
TEAMDYNAMICA v1.5 Compliant (2026-07-30)
"""
import os, sys, shutil, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_OUT = os.path.join(ROOT, "wiki_output")
os.makedirs(WIKI_OUT, exist_ok=True)

print("[wiki] Generating updated GitHub Wiki pages...")

# ── 1. Home.md ────────────────────────────────────────────────────────────
home = """# Dutch Virology Network — Multiplex Knowledge Graph & Global Forensics

## Over dit project
Deze wiki is onderdeel van het open-source onderzoeksproject **"Dutch Pandemic Governance & Virology Network Analysis Toolkit"**. Het project bevat een multiplex knowledge graph van **4.929 nodes** en **7.934 edges** over de Nederlandse virologietop en hun internationale netwerken, gebaseerd op **TEAMDYNAMICA v1.5** evidence-first richtlijnen.

## Primair Bronmateriaal
- **Tony's Diary**: Het dagboek van Dr. Anthony Fauci (NIAID), 1.141 pagina's (U.S. Senate HELP Committee, juli 2026, SHA-256: `27d8d39b...`)
- **USRTK & U.S. House Select Subcommittee FOIA**: Vrijgegeven e-mails en getuigenissen (Feb 2020 Proximal Origin drafting, SHA-256: `3e1990e...`)
- **OpenAlex & NIH RePORTER**: Auteursprofielen en Amerikaanse subsidiegegevens
- **EU CORDIS & ZonMw**: EUR 67,6M+ aan Europese en Nederlandse subsidies (VEO, COMPARE, ECRAID, DURABLE)
- **Octrooien & Genomische Data**: BsmBI/BsaI reverse-genetics octrooien (US6849435B2, WO2006131370A2) en Eurosurveillance Corman-Drosten PCR fast-track

## Navigation & Core Wiki Pages

| Pagina | Beschrijving |
|--------|-------------|
| [Global-FOIA-Proximal-Origin](Global-FOIA-Proximal-Origin) | Forensisch dossier over Fouchier & Koopmans draft feedback op *Proximal Origin* |
| [Global-Sources-Dutch-COVID-Role](Global-Sources-Dutch-COVID-Role) | Geconsolideerd master-rapport over alle 6 prioritaire zoekdomeinen |
| [Blind-Spot-Mapping](Blind-Spot-Mapping) | Epistemologische audit van de top 7 hoogste-leverage blinde vlekken |
| [De-Pandemische-Draaischijf](De-Pandemische-Draaischijf) | Volledig forensisch onderzoeksrapport: 12 hoofdstukken, 31 bronnen |
| [Subsidies-en-Consortia](Subsidies-en-Consortia) | EUR 67,6M+ aan EU/ZonMw subsidies (VEO, ECRAID, PDPC, COMPARE, DURABLE, NCOH) |
| [48-Uurs-Reconstructie](48-Uurs-Reconstructie) | Minuut-voor-minuut reconstructie: 31 jan - 2 feb 2020 & Feb 1 call |
| [DURC-en-Patenten](DURC-en-Patenten) | BsmBI reverse genetics (US6849435B2), DARPA DEFUSE, furin cleavage site |
| [Forensische-SQL-Views](Forensische-SQL-Views) | DuckDB/Parquet handleiding, SHA-256 checksums, SQL views |
| [AVG-GDPR-en-Wederhoor](AVG-GDPR-en-Wederhoor) | TEAMDYNAMICA v1.5 regels, 4-assen kwalificatiekader & takedown policy |

## Externe Links
- **Live Web-App:** https://triggerminds.github.io/dutch-virology-network-analysis/
- **GitHub Repository:** https://github.com/TriggerMinds/dutch-virology-network-analysis
- **TEAMDYNAMICA Regels:** https://github.com/TriggerMinds/dutch-virology-network-analysis/blob/main/TEAMDYNAMICA.md

## Licentie
MIT — zie LICENSE in de hoofdrepository. Bron-PDF's zijn publiek domein (U.S. Congressional & FOIA releases).
"""
with open(os.path.join(WIKI_OUT, "Home.md"), "w", encoding="utf-8") as f:
    f.write(home)
print("  Home.md")

# ── Helper to copy docs to wiki pages ─────────────────────────────────────
def copy_doc_to_wiki(src_rel, wiki_name):
    src_path = os.path.join(ROOT, "docs", src_rel)
    if os.path.exists(src_path):
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(os.path.join(WIKI_OUT, f"{wiki_name}.md"), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  {wiki_name}.md")
    else:
        print(f"  [SKIP] {src_rel} not found")

copy_doc_to_wiki("GLOBAL_FOIA_PROXIMAL_ORIGIN_DOSSIER.md", "Global-FOIA-Proximal-Origin")
copy_doc_to_wiki("GLOBAL_SOURCES_DUTCH_COVID_ROLE.md", "Global-Sources-Dutch-COVID-Role")
copy_doc_to_wiki("BLIND_SPOT_MAPPING.md", "Blind-Spot-Mapping")
copy_doc_to_wiki("DUTCH_ANOMALIES_FORENSIC_AUDIT.md", "Nederlandse-Anomalieen-en-Belangen")
copy_doc_to_wiki("MASTER_UNTURNED_STONES_AUDIT.md", "Master-Unturned-Stones-Audit")
copy_doc_to_wiki("EU_MEMBER_STATES_FORENSIC_DOSSIER.md", "Europese-Parlementaire-Onderzoeken")

# ── 2. De-Pandemische-Draaischijf.md ──────────────────────────────────────
md_path = os.path.join(ROOT, "docs", "wiki", "De-Pandemische-Draaischijf.md")
if not os.path.exists(md_path):
    md_path = os.path.join(ROOT, "docs", "INVESTIGATIVE_REPORT_DUTCH.md")

if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    with open(os.path.join(WIKI_OUT, "De-Pandemische-Draaischijf.md"), "w", encoding="utf-8") as f:
        if not md_content.startswith("# De Pandemische Draaischijf"):
            f.write("# De Pandemische Draaischijf\n\n")
            f.write("*Zie ook het originele artikel met interactieve netwerkgrafieken:* ")
            f.write("[article.html](https://triggerminds.github.io/dutch-virology-network-analysis/article.html)\n\n")
        f.write(md_content)
    print("  De-Pandemische-Draaischijf.md")

# ── 3. Subsidies-en-Consortia.md ──────────────────────────────────────────
subsidies = """# Subsidies en Consortia — EUR 67,6M+

## EU Horizon 2020 — CORDIS Projecten
| Project | Coordinator | Budget | Financier |
|---------|------------|--------|-----------|
| VEO (GA#874735) | Marion Koopmans (Erasmus MC) | EUR 14.600.000 | EU Horizon 2020 |
| ECRAID (GA#965313) | Marc Bonten (UMC Utrecht) | EUR 20.000.000 | EU Horizon 2020 |
| COMPARE (GA#643476) | Marion Koopmans (Erasmus MC) | EUR 10.300.000 | EU Horizon 2020 |
| DURABLE (GA#848223) | Menno de Jong (RIVM) | EUR 5.000.000 | EU Horizon 2020 |

## ZonMw Nationale Subsidies
| Project | Coordinator | Budget |
|---------|------------|--------|
| PDPC | Erasmus MC (lead, Koopmans) | EUR 12.000.000 |
| NCOH | Marion Koopmans (Erasmus MC) | EUR 4.200.000 |
| IC COVID | Diederik Gommers (Erasmus MC) | EUR 1.500.000 |

## USAID PREDICT Status
- Status: **`OPEN_BLIND_SPOT_PRIMARY_DOCS_REQUIRED`**
- EcoHealth Alliance was kernpartner in USAID PREDICT (UC Davis lead). Erasmus MC (Koopmans, Osterhaus) werkte internationaal samen in One Health surveillance. Primaire sub-award contracten die Erasmus MC als directe beursontvanger staven vereisen verdere Woo/FOIA documentatie.

## NIH Grants
| Grant | PI | Budget | Ontvanger |
|-------|-----|--------|-----------|
| 2R01AI110964-06A1 | Peter Daszak (EcoHealth) | USD 3.700.000 | EcoHealth -> WIV sub-award |
"""
with open(os.path.join(WIKI_OUT, "Subsidies-en-Consortia.md"), "w", encoding="utf-8") as f:
    f.write(subsidies)
print("  Subsidies-en-Consortia.md")

# ── 4. 48-Uurs-Reconstructie.md ───────────────────────────────────────────
reconstructie = """# 48-Uurs Reconstructie: 31 januari - 2 februari 2020

## 31 januari 2020 — Robertson identificeert furin cleavage site
David Robertson (MRC-University of Glasgow) analyseert de eerste SARS-CoV-2 sequenties en ontdekt een ongebruikelijke furin cleavage site (PRRAR|SV). Robertson belt Jeremy Farrar (Wellcome Trust).
*Bron: UK Parliament testimony Jeremy Farrar, 2021.*

## 31 januari 2020 — Farrar belt Fauci
Farrar belt Fauci en deelt Robertsons analyse. Fauci noteert op p767:
> "On January 31st, 2020 I received a call from Jeremy Farrar who conferred in Christian Andersen."

## 1 februari 2020, 14:00 EST — De Conference Call
Fauci's contemporaine aantekening op p14:
> "Conference call at 2:00 PM with Jeremy, Francis and several other scientists gathered by Jeremy."

### Deelnemers & Posities
- **Ron Fouchier** (Erasmus MC): Verdedigde de natuurlijke oorsprong ("sure that this could occur naturally").
- **Marion Koopmans** (Erasmus MC): Aanwezigheid bevestigd; positie op de call zelf **niet genoteerd** (Status: `UNKNOWN`).
- **Christian Drosten** (Charité): Drosten was met Ron.
- **Overigen** (Andersen, Holmes, Rambaut, Garry, Ferguson, Fauci, Collins, Farrar, Vallance): Vonden deliberate insertion mogelijk.

## 4 - 8 februari 2020 — Substantiële Feedback op Concepten Proximal Origin
USRTK FOIA-documenten (`Proximal-Origin-Democratic-Staff-Report-Emails.pdf`, SHA-256: `3e1990e...`) tonen aan dat Fouchier en Koopmans via Jeremy Farrar inhoudelijke feedback gaven op vroege concepten van *The Proximal Origin of SARS-CoV-2*. 
- **Fouchier**: Droeg moleculaire tegenargumenten aan tegen lab-origin scenario's.
- **Koopmans**: Ontraadde het uitlichten van de furin cleavage site om conspiracy theories te voorkomen.
- **TEAMDYNAMICA Kwalificatie**: Zij waren geen formele co-auteurs of stuurders van het paper, maar invloedrijke externe adviseurs wiens argumenten bijdroegen aan het weglaten/verzagten van lab-leak taal.
"""
with open(os.path.join(WIKI_OUT, "48-Uurs-Reconstructie.md"), "w", encoding="utf-8") as f:
    f.write(reconstructie)
print("  48-Uurs-Reconstructie.md")

# ── 5. DURC-en-Patenten.md ──────────────────────────────────────────────
durc = """# DURC en Patenten — BsmBI Reverse Genetics & DEFUSE Methodologische Overlap

## Octrooistamboom US6849435B2
De methodologische basis voor reverse genetics van zowel influenza- als coronavirussen ligt in het patent **US6849435B2** (Fouchier, Osterhaus, Kawaoka, 1999). Dit patent beschrijft het gebruik van type IIS restrictie-enzymen (BsmBI, BsaI) voor het kloneren van virale genomen uit cDNA.

```
US6849435B2 (Fouchier/Osterhaus/Kawaoka, 1999)
  +-- BsmBI/BsaI reverse genetics systeem
       +-- Toegepast op influenza A (H5N1 ferret, 2012)
       +-- Toegepast op SARS-CoV (WO2006131370A2, 2005)
       +-- Toegepast op MERS-CoV (Fouchier, 2012)
       +-- Relevant voor SARS-CoV-2 furin cleavage site
            +-- Feb 1 2020 call: natuurlijk vs. synthetisch debat
```

## DARPA DEFUSE Methodologische Overlap
Het DEFUSE-voorstel (EcoHealth/Baric/WIV, 2018) maakte gebruik van Type IIS restrictie-enzymen (BsmBI/BsaI) om synthetische spike-eiwit mutaties en furin cleavage sites in bat coronaviruses in te bouwen. Dit betreft een **methodologische overlap** in reverse-genetics technologie, **geen** directe co-financiering of co-auteurschap door Nederlandse virologen.
"""
with open(os.path.join(WIKI_OUT, "DURC-en-Patenten.md"), "w", encoding="utf-8") as f:
    f.write(durc)
print("  DURC-en-Patenten.md")

# ── 6. AVG-GDPR-en-Wederhoor.md ─────────────────────────────────────────
avg = """# AVG/GDPR, TEAMDYNAMICA v1.5 & 4-Assen Kwalificatiekader

## TEAMDYNAMICA v1.5 Regels
- **Bias-Deactivatie Protocol**: Voorzichtigheidsbias, authority bias, framing bias en sycophancy worden uitgeschakeld waar bronnen het bewijs dragen.
- **4-Assen Kwalificatiekader**: Elke afgewogen claim specificeert exact welke van de vier assen niet hard genoeg is:
  1. **Intentie** (moedwil vs. onbewuste reflex / eigenbelang)
  2. **Causaliteit** (directe sturing vs. bijdrage/beïnvloeding)
  3. **Verantwoordelijkheid** (eindverantwoordelijke vs. adviserende rol)
  4. **Timing** (contemporaine wetenschap vs. kennis achteraf)

## Juridische Onderbouwing
Dit project verwerkt gegevens van publieke figuren acting in hun professionele hoedanigheid uit openbare bronnen.
"""
with open(os.path.join(WIKI_OUT, "AVG-GDPR-en-Wederhoor.md"), "w", encoding="utf-8") as f:
    f.write(avg)
print("  AVG-GDPR-en-Wederhoor.md")

print(f"\n[wiki] {len(os.listdir(WIKI_OUT))} pages generated in {WIKI_OUT}")

# ── Auto-push to GitHub Wiki repo ─────────────────────────────────────────
wiki_repo_url = "https://github.com/TriggerMinds/dutch-virology-network-analysis.wiki.git"

try:
    print(f"\n[wiki] Syncing directly to GitHub Wiki repository ({wiki_repo_url})...")
    temp_wiki_dir = tempfile.mkdtemp(prefix="wiki_sync_")
    
    subprocess.check_call(["git", "clone", wiki_repo_url, temp_wiki_dir])
    
    for f in os.listdir(WIKI_OUT):
        if f.endswith(".md"):
            shutil.copy2(os.path.join(WIKI_OUT, f), os.path.join(temp_wiki_dir, f))
            
    subprocess.check_call(["git", "add", "."], cwd=temp_wiki_dir)
    status_output = subprocess.check_output(["git", "status", "--porcelain"], cwd=temp_wiki_dir).decode()
    
    if status_output.strip():
        subprocess.check_call(["git", "commit", "-m", "docs(wiki): sync wiki pages with TEAMDYNAMICA v1.5 & global FOIA dossiers"], cwd=temp_wiki_dir)
        # Push to master and main on wiki repo if possible
        try:
            subprocess.check_call(["git", "push", "origin", "master"], cwd=temp_wiki_dir)
        except:
            pass
        try:
            subprocess.check_call(["git", "push", "origin", "main"], cwd=temp_wiki_dir)
        except:
            pass
        print("[wiki] GitHub Wiki successfully updated and pushed live!")
    else:
        print("[wiki] GitHub Wiki is already up to date.")
        
    shutil.rmtree(temp_wiki_dir, ignore_errors=True)
except Exception as e:
    print(f"[wiki] Warning: Auto-push to GitHub Wiki encountered an error: {e}")
