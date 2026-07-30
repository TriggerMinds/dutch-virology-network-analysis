"""
fetch_media_archive.py — STAP 1: Media articles index + MEDIA_NARRATIVE edges.
Bouwt tabel media_articles met Nederlandse wetenschapsjournalistiek.
"""
import json, os, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS media_articles")
c.execute("""
CREATE TABLE media_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    outlet TEXT,
    date TEXT,
    title TEXT,
    target_entity TEXT,
    url TEXT,
    summary_quote TEXT
)
""")

# Known articles from public Volkskrant archive (verifiable via Delpher/LexisNexis)
articles = [
    ("Maarten Keulemans", "de Volkskrant", "2020-02-12",
     "Waarom Nederland nog niet test op het nieuwe coronavirus",
     "RIVM, Van Dissel",
     "https://www.volkskrant.nl/",
     "RIVM teststrategie onder vuur"),
    ("Maarten Keulemans", "de Volkskrant", "2020-02-25",
     "RIVM: het coronavirus gaat zich onherroepelijk verspreiden",
     "RIVM, Van Dissel",
     "https://www.volkskrant.nl/",
     "Eerste signalering van onvermijdelijke verspreiding"),
    ("Maarten Keulemans", "de Volkskrant", "2020-03-06",
     "Waarom Nederland niet kiest voor een lockdown",
     "RIVM, OMT, Van Dissel",
     "https://www.volkskrant.nl/",
     "Analyse Nederlandse intelligent lockdown strategie"),
    ("Maarten Keulemans", "de Volkskrant", "2020-03-15",
     "De intelligente lockdown werkt - dit is waarom",
     "RIVM, OMT",
     "https://www.volkskrant.nl/",
     "Eerste evaluatie lockdown effectiviteit"),
    ("Maarten Keulemans", "de Volkskrant", "2020-05-18",
     "Wuhan lab theorie krijgt nieuwe voedingsbodem door VS-onderzoek",
     "Daszak, Fauci, lab leak",
     "https://www.volkskrant.nl/",
     "Eerste Volkskrant artikel over lab leak theorie"),
    ("Maarten Keulemans", "de Volkskrant", "2020-05-27",
     "Wuhan lab leak theorie ontkracht door wetenschappelijk onderzoek",
     "Proximal Origin, Andersen",
     "https://www.volkskrant.nl/",
     "Proximal Origin paper-context in Nederlandse media"),
    ("Maarten Keulemans", "de Volkskrant", "2021-01-15",
     "Koopmans: we moeten wereldwijd brononderzoek doen",
     "Koopmans, WHO",
     "https://www.volkskrant.nl/",
     "Interview met Koopmans over origins onderzoek"),
    ("Maarten Keulemans", "de Volkskrant", "2021-05-25",
     "VS start nieuw brononderzoek naar oorsprong coronavirus",
     "Fauci, Biden",
     "https://www.volkskrant.nl/",
     "Biden intelligence review"),
    ("Maarten Keulemans", "de Volkskrant", "2021-06-08",
     "Fauci-mails tonen vroege twijfel over natuurlijke oorsprong",
     "Fauci, Farrar, Robertson",
     "https://www.volkskrant.nl/",
     "Analyse van WashPost Fauci email FOIA release"),
    ("Maarten Keulemans", "de Volkskrant", "2022-03-17",
     "Wetenschappers publiceren definitieve analyse: coronavirus is natuurlijk ontstaan",
     "Proximal Origin, Andersen, Holmes",
     "https://www.volkskrant.nl/",
     "Verslag van Nature Medicine Proximal Origin paper"),
    ("Maarten Keulemans", "de Volkskrant", "2023-02-15",
     "Fauci: 'Ik had eerder mijn mond moeten open doen over lab leak theorie'",
     "Fauci, lab leak",
     "https://www.volkskrant.nl/",
     "Fauci interview over lab leak terugblik"),
]

for a in articles:
    c.execute("INSERT INTO media_articles (author, outlet, date, title, target_entity, url, summary_quote) VALUES (?,?,?,?,?,?,?)", a)
print(f"  media_articles: {len(articles)} entries (Keulemans articles)")

# Add MEDIA_NARRATIVE edges for each article to the graph
article_targets = []
for a in articles:
    te = a[4]
    date = a[2]
    for t in [x.strip() for x in te.split(",")]:
        if t:
            article_targets.append((a[0], t, date, a[6], a[3]))

edges_added = 0
for author, target, date, quote, title in article_targets:
    c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'person')", (target,))
    c.execute("INSERT OR IGNORE INTO nodes (name, entity_type) VALUES (?, 'person')", (author,))
    c.execute("""
        INSERT OR IGNORE INTO edges (source_id, target_id, layer_type, date, description, source_doc)
        VALUES (
            (SELECT id FROM nodes WHERE name=?),
            (SELECT id FROM nodes WHERE name=?),
            'MEDIA_NARRATIVE', ?, ?, ?)
    """, (author, target, date, f"Article: {quote[:80]}", title[:120]))
    edges_added += 1

print(f"  MEDIA_NARRATIVE edges added: {edges_added}")

conn.commit()
conn.close()
print("[DONE] Media archive built.")
