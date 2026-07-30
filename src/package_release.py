"""
package_release.py — STAP 3a: Creates release ZIP with forensic data exports.
"""
import zipfile, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def collect_files():
    files = []
    # Core data
    for f in ["data/network_data.db", "data/graph.json", "data/checksums.sha256",
              "docs/DUTCH_CONNECTIONS_DOSSIER.md", "docs/INVESTIGATIVE_REPORT_DUTCH.md"]:
        fp = os.path.join(ROOT, f)
        if os.path.exists(fp):
            files.append((f, fp))
    # Parquet
    pq_dir = os.path.join(ROOT, "data", "parquet")
    if os.path.isdir(pq_dir):
        for fn in sorted(os.listdir(pq_dir)):
            files.append((f"data/parquet/{fn}", os.path.join(pq_dir, fn)))
    return files

files = collect_files()
zip_path = os.path.join(ROOT, "release_v4.0.zip")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for arcname, fullpath in files:
        zf.write(fullpath, arcname)
    # Add SHA-256 of the zip itself
    zf.close()

# Generate release checksum
sha = hashlib.sha256(open(zip_path, "rb").read()).hexdigest()

print("=" * 60)
print("RELEASE PACKAGING v4.0")
print("=" * 60)
for arcname, _ in files:
    print(f"  + {arcname}")
print(f"\n  --> release_v4.0.zip ({os.path.getsize(zip_path)/1024:.0f} KB)")
print(f"  SHA-256: {sha}")

# Write checksum to file
with open(os.path.join(ROOT, "release_v4.0.sha256"), "w") as f:
    f.write(f"{sha}  release_v4.0.zip\n")
print(f"  Checksum: release_v4.0.sha256")
