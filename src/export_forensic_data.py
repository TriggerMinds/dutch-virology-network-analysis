"""
export_forensic_data.py — STAP 2: Parquet/CSV exports + SHA-256 checksums.
"""
import sqlite3, os, json, hashlib
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "network_data.db")
CENTRALITY_PATH = os.path.join(ROOT, "data", "centrality_results.json")
PARQUET_DIR = os.path.join(ROOT, "data", "parquet")
CSV_DIR = os.path.join(ROOT, "data", "csv")
os.makedirs(PARQUET_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("FORENSIC DATA EXPORT — Parquet + CSV + SHA-256")
print("=" * 60)

# ── Export tables ────────────────────────────────────────────────────────
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_%'")]
views = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='view' AND name LIKE 'vw_%'")]

exported_files = []

for tbl in tables + views:
    try:
        df = pd.read_sql_query(f"SELECT * FROM [{tbl}]", conn)
        if df.empty and not views:
            print(f"  [SKIP] {tbl} — empty")
            continue

        # Parquet
        pq_path = os.path.join(PARQUET_DIR, f"{tbl}.parquet")
        df.to_parquet(pq_path, index=False)
        exported_files.append(pq_path)

        # CSV
        csv_path = os.path.join(CSV_DIR, f"{tbl}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8")
        exported_files.append(csv_path)

        print(f"  [OK]  {tbl:30s} -> {len(df):6d} rows")
    except Exception as e:
        print(f"  [ERR] {tbl}: {e}")

conn.close()

# Also export centrality JSON
if os.path.exists(CENTRALITY_PATH):
    with open(CENTRALITY_PATH, "r", encoding="utf-8") as f:
        cent = json.load(f)
    df_cent = pd.json_normalize(cent, sep="_")
    # Flatten for analysis
    rows = []
    for layer, metrics in cent.items():
        for metric_name, scores in metrics.items():
            if isinstance(scores, dict):
                for node, score in scores.items():
                    rows.append({"layer": layer, "metric": metric_name, "node": node, "score": score})
    df_cent_flat = pd.DataFrame(rows)
    pq_cent = os.path.join(PARQUET_DIR, "centrality_flat.parquet")
    df_cent_flat.to_parquet(pq_cent, index=False)
    csv_cent = os.path.join(CSV_DIR, "centrality_flat.csv")
    df_cent_flat.to_csv(csv_cent, index=False, encoding="utf-8")
    exported_files.extend([pq_cent, csv_cent])
    print(f"  [OK]  centrality_flat{'':20s} -> {len(df_cent_flat):6d} rows")

# ── SHA-256 checksums ────────────────────────────────────────────────────
checksums = {}
for fp in sorted(exported_files):
    with open(fp, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
        rel = os.path.relpath(fp, ROOT)
        checksums[rel] = sha

sha_path = os.path.join(ROOT, "data", "checksums.sha256")
with open(sha_path, "w") as f:
    for rel, sha in sorted(checksums.items()):
        f.write(f"{sha}  {rel}\n")
exported_files.append(sha_path)

print(f"\n{'='*60}")
print(f"EXPORT SUMMARY")
print(f"{'='*60}")
print(f"  Total files: {len(exported_files)}")
print(f"  Parquet:     {len([f for f in exported_files if f.endswith('.parquet')])}")
print(f"  CSV:         {len([f for f in exported_files if f.endswith('.csv')])}")
print(f"  SHA-256:     {sha_path}")
print(f"\n  SHA-256 hashes:")
for rel, sha in sorted(checksums.items())[:8]:
    print(f"    {sha[:16]}...  {rel}")
if len(checksums) > 8:
    print(f"    ... and {len(checksums)-8} more files")
print(f"\n[DONE] Export complete.")
