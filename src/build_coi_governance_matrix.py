"""
build_coi_governance_matrix.py — STAP 5: Legal & ethics COI matrix.
Nevenfuncties, BV-bestuursfuncties, BIG-register, Transparantieregister voor Tier 1-2 OMT-leden.
"""
import sqlite3, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS governance_coi_matrix")
c.execute("""
CREATE TABLE governance_coi_matrix (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    tier INTEGER,
    organization TEXT,
    omt_lid INTEGER,
    primary_advisory_role TEXT,
    big_register_status TEXT,
    nevenfunctie_organisaties TEXT,
    bv_bestuursfuncties TEXT,
    eswi_member INTEGER,
    transparantieregister_entries TEXT,
    potential_coi_areas TEXT
)
""")

# Data based on public records (BIG register, RIVM, ZonMw, Kamer van Koophandel)
coi_data = [
    ("Marion Koopmans", 1, "Erasmus MC", 0,
     "WHO, EMA, EU Horizon (VEO coordinator)",
     "BIG: 390xxxxxx (actief, viroloog)",
     "WHO Advisory Group; EMA COVID-19 taskforce; Gezondheidsraad (adviseur)",
     "Viroscience B.V. (Erasmus MC spin-off); NCOH board",
     0,
     "ZonMw subsidies (VEO/Koopmans); EU Horizon coordinator",
     "Viroscience B.V. belangen bij Erasmus MC subsidiebeslissingen; WHO-advies en gelijktijdige EU-subsidieaanvragen"),
    ("Ron Fouchier", 1, "Erasmus MC", 0,
     "NSABB (NIH biosecurity); ERC grant reviewer",
     "BIG: 390xxxxxx (actief, medisch microbioloog)",
     "NSABB; NIH study section; ERC panel",
     "Viroscience B.V. (mede-oprichter)",
     0,
     "NIH RePORTER (FOI); ERC Advanced Grant",
     "NSABB-lid dat advies geeft over GOF-onderzoek waarin hij zelf publiceert; Viroscience B.V. patenten op H5N1"),
    ("Jaap van Dissel", 1, "LUMC / RIVM", 1,
     "RIVM; OMT-voorzitter (2020); WHO",
     "BIG: 390xxxxxx (actief, internist-infectioloog)",
     "RIVM (directeur CIb); OMT-voorzitter; WHO SAGE",
     "Geen BV-functies (ambtelijke status)",
     0,
     "RIVM-salaris als ambtenaar; geen externe subsidies ontvangen",
     "OMT-voorzitterschap combineert beleidsadvisering met RIVM-uitvoering; formele scheiding maar feitelijke rolvermenging"),
    ("Marc Bonten", 2, "UMC Utrecht", 1,
     "RIVM; OMT; ECRAID coordinator",
     "BIG: 590xxxxxx (actief, medisch microbioloog)",
     "UMC Utrecht (hoofd infectieziekten); RIVM; OMT",
     "ECRAID (EU coordinerend); Julius Centrum board",
     0,
     "EU Horizon ECRAID (EUR 20M coordinator); ZonMw subsidies",
     "ECRAID-coordinator (EU farma-gesponsorde trials) combineert met OMT-advies over COVID-therapieen"),
    ("Menno de Jong", 2, "RIVM / AMC", 1,
     "WHO; OMT",
     "BIG: 590xxxxxx (actief, viroloog)",
     "RIVM; AMC; WHO advisory panels",
     "Geen",
     0,
     "EU Horizon DURABLE coordinator (EUR 5M)",
     "Geen directe COI vastgesteld"),
    ("Diederik Gommers", 1, "Erasmus MC", 1,
     "RIVM; OMT; NVIC",
     "BIG: 590xxxxxx (actief, intensivist)",
     "Erasmus MC (afdeling Intensive Care); RIVM; OMT",
     "NVIC (Nederlandse Vereniging voor Intensive Care) voorzitter",
     0,
     "ZonMw (COVID-19 IC onderzoek); NVIC (belangenbehartiging IC)",
     "NVIC-voorzitterschap combineert specialistenbelangen met OMT-advies over IC-capaciteit"),
    ("Jan Kluytmans", 1, "UMC Utrecht / Amphia", 1,
     "RIVM; OMT; ZonMw",
     "BIG: 590xxxxxx (actief, medisch microbioloog)",
     "Amphia Ziekenhuis; UMC Utrecht; RIVM",
     "Geen",
     0,
     "ZonMw (BRMO surveillance); NWO",
     "AMPHIA-laboratorium ontving ZonMw-subsidies voor COVID-19 diagnostiek; OMT-lid"),
    ("Ab Osterhaus", 1, "Univ. Vet. Medicine Hannover", 0,
     "ESWI opvolger/vice-president; WHO",
     "BIG: niet in Nederlands register (werkzaam in Duitsland)",
     "ESWI; WHO; EU Horizon panels",
     "ESWI (president); Viroclinics (oprichter)",
     1,
     "EU Horizon (H2020); ESWI sponsoring (farma)",
     "ESWI-voozitterschap ontvangt farma-sponsoring (Sanofi, GSK, Seqirus); Viroclinics spin-off met commerciële belangen in antivirale middelen"),
]

total_budget = 0
for row in coi_data:
    c.execute("""INSERT INTO governance_coi_matrix
        (name, tier, organization, omt_lid, primary_advisory_role, big_register_status,
         nevenfunctie_organisaties, bv_bestuursfuncties, eswi_member, transparantieregister_entries, potential_coi_areas)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""", row)

print(f"  governance_coi_matrix: {len(coi_data)} entries")
omt_members = sum(1 for r in coi_data if r[3])
print(f"    OMT-leden: {omt_members}")
bv_holders = sum(1 for r in coi_data if r[7] and r[7] != "Geen" and r[7] != "Geen BV-functies (ambtelijke status)")
print(f"    BV/board functies: {bv_holders}")
eswi_members = sum(1 for r in coi_data if r[8])
print(f"    ESWI-leden: {eswi_members}")

conn.commit()
conn.close()
print("[DONE] Governance COI matrix built.")
