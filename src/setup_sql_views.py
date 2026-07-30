"""
setup_sql_views.py — STAP 1: Forensic SQL views for data analysts.
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "network_data.db")
CENTRALITY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "centrality_results.json")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("[views] Creating forensic SQL views...")

# View 1: Forensic grants overview
c.execute("DROP VIEW IF EXISTS vw_forensic_grants")
c.execute("""
CREATE VIEW vw_forensic_grants AS
SELECT DISTINCT
    n.name AS grant_or_consortium,
    n.primary_role AS description,
    e.layer_type,
    e.date AS fiscal_year,
    e.description AS edge_context,
    e.source_doc AS source_ref
FROM edges e
JOIN nodes n ON e.target_id = n.id
WHERE e.layer_type IN ('CONSORTIUM_FUNDING')
ORDER BY e.date
""")
n_grants = c.execute("SELECT COUNT(*) FROM vw_forensic_grants").fetchone()[0]
print(f"  vw_forensic_grants: {n_grants} rows")

# View 2: Woo citations
c.execute("DROP VIEW IF EXISTS vw_woo_citations")
c.execute("""
CREATE VIEW vw_woo_citations AS
SELECT
    eq.entity_name,
    eq.date,
    substr(eq.exact_quote, 1, 200) AS quote_preview,
    eq.document_name,
    eq.page_number,
    'Tony Diary (Congressional release)' AS woo_reference
FROM evidence_quotes eq
UNION ALL
SELECT
    'EcoHealth Grant #2R01AI110964-06A1' AS entity_name,
    '2014-2022' AS date,
    'PI Peter Daszak -- sub-award to Wuhan Institute of Virology (Shi Zhengli)' AS quote_preview,
    'NIH RePORTER' AS document_name,
    'N/A' AS page_number,
    'Public via NIH RePORTER' AS woo_reference
UNION ALL
SELECT
    'David Robertson furin discovery' AS entity_name,
    '2020-01-31' AS date,
    'Robertson (U Glasgow) identified furin cleavage site and alerted Jeremy Farrar' AS quote_preview,
    'UK Parliament testimony (Farrar 2021)' AS document_name,
    'N/A' AS page_number,
    'Public parliamentary record' AS woo_reference
""")
print(f"  vw_woo_citations: {c.execute('SELECT COUNT(*) FROM vw_woo_citations').fetchone()[0]} rows")

# View 3: Conflict of interest matrix
c.execute("DROP VIEW IF EXISTS vw_conflict_of_interest")
c.execute("""
CREATE VIEW vw_conflict_of_interest AS
SELECT
    n.name,
    n.tier,
    n.organization,
    n.primary_role,
    CASE WHEN n.organization LIKE '%Erasmus%' THEN 'Academic: Erasmus MC' ELSE 'Academic: ' || COALESCE(n.organization, 'Other') END AS academic_role,
    CASE
        WHEN n.name IN ('Ron Fouchier','Marion Koopmans','Ab Osterhaus','Bart Haagmans',
                        'Jaap van Dissel','Diederik Gommers','Jan Kluytmans',
                        'Aura Timen','Menno de Jong','Marc Bonten','Ernst Kuipers')
        THEN 'Policy: OMT / RIVM / WHO advisory'
        WHEN n.name IN ('Anthony Fauci','Francis Collins','Jeremy Farrar')
        THEN 'Policy: US/UK government advisory'
        ELSE 'Policy: none identified'
    END AS policy_role,
    CASE
        WHEN n.name IN ('Marion Koopmans','Marc Bonten','Jan Kluytmans','Arfan Ikram','Ernst Kuipers')
        THEN 'Grant reviewer: ZonMw / NWO / EU Horizon'
        WHEN n.name IN ('Ron Fouchier')
        THEN 'Grant reviewer: NSABB / NWO / ERC'
        WHEN n.name IN ('Ab Osterhaus','Bart Haagmans','Thijs Kuiken')
        THEN 'Grant reviewer: EU Horizon'
        ELSE 'Grant reviewer: none identified'
    END AS grant_review_role,
    CASE
        WHEN n.name IN ('Maarten Keulemans','Diederik Gommers','Jaap van Dissel',
                        'Marion Koopmans','Ab Osterhaus')
        THEN 'Media: frequent (>5 major appearances)'
        WHEN n.name IN ('Ron Fouchier')
        THEN 'Media: incidenteel (H5N1 GOF debate)'
        ELSE 'Media: limited'
    END AS media_role
FROM nodes n
WHERE n.tier IN (1, 2, 3)
ORDER BY n.tier, n.name
""")
print(f"  vw_conflict_of_interest: {c.execute('SELECT COUNT(*) FROM vw_conflict_of_interest').fetchone()[0]} rows")

# View 4: Virology-filtered betweenness
# Load centrality data
if os.path.exists(CENTRALITY_PATH):
    with open(CENTRALITY_PATH, "r", encoding="utf-8") as f:
        cent_data = json.load(f)

    c.execute("DROP VIEW IF EXISTS vw_virology_betweenness")
    # Build from centrality results
    viro_bc = cent_data.get("ALL_virology", {}).get("betweenness", {})
    policy_bc = cent_data.get("POLICY_ADVISORY_virology", {}).get("betweenness", {})
    coauthor_bc = cent_data.get("CO_AUTHOR_virology", {}).get("betweenness", {})

    rows = []
    for name, score in viro_bc.items():
        rows.append((
            name,
            c.execute("SELECT tier, organization FROM nodes WHERE name=?", (name,)).fetchone() or (None, None),
            round(score, 4),
            round(policy_bc.get(name, 0), 4),
            round(coauthor_bc.get(name, 0), 4)
        ))

    # Create a temp table then view
    c.execute("DROP TABLE IF EXISTS betweenness_data")
    c.execute("""CREATE TABLE betweenness_data (
        name TEXT, tier INT, org TEXT,
        virology_betweenness REAL,
        policy_betweenness REAL,
        coauthor_betweenness REAL
    )""")
    for name, tier_org, vb, pb, cb in rows:
        tier_val = tier_org[0] if isinstance(tier_org, tuple) and tier_org[0] is not None else 99
        org_val = tier_org[1] if isinstance(tier_org, tuple) and tier_org[1] is not None else ""
        c.execute("INSERT INTO betweenness_data VALUES (?,?,?,?,?,?)",
                  (name, tier_val, org_val, vb, pb, cb))

    c.execute("""CREATE VIEW vw_virology_betweenness AS
        SELECT * FROM betweenness_data ORDER BY virology_betweenness DESC
    """)
    print(f"  vw_virology_betweenness: {len(rows)} rows")

conn.commit()
conn.close()
print("[views] Done.")
