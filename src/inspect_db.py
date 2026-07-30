import sqlite3

conn = sqlite3.connect('data/network_data.db')
c = conn.cursor()
tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables:")
for t in tables:
    tbl = t[0]
    info = c.execute(f"PRAGMA table_info({tbl});").fetchall()
    cols = [f"{col[1]} ({col[2]})" for col in info]
    print(f"  {tbl}: {', '.join(cols)}")
conn.close()
