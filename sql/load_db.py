"""
Loads the 4 generated CSVs into marketplace.db (SQLite).
Blank cells become real NULL values (not empty string).
Run: python sql/load_db.py
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "marketplace.db"
DATA_DIR = "data"

tables = ["seekers", "employers", "jobs", "funnel"]

con = sqlite3.connect(DB_PATH)
for t in tables:
    path = os.path.join(DATA_DIR, f"{t}.csv")
    df = pd.read_csv(path)
    df.to_sql(t, con, if_exists="replace", index=False)
    print(f"  Loaded {t:12s}: {len(df):,} rows -> {DB_PATH}")

# Quick reconciliation check
cur = con.cursor()
cur.execute("""
    SELECT
        COUNT(*)              AS views,
        SUM(applied)          AS applies,
        SUM(recruiter_viewed) AS recruiter_views,
        SUM(responded)        AS responses,
        SUM(interviewed)      AS interviews,
        SUM(hired)            AS hires
    FROM funnel
""")
row = cur.fetchone()
cols = ["views", "applies", "recruiter_views", "responses", "interviews", "hires"]

print("\nReconciliation numbers (copy these into README.md):")
print(f"{'Metric':<20} {'Count':>8}")
print("-" * 30)
for col, val in zip(cols, row):
    print(f"{col:<20} {int(val):>8,}")

con.close()
print(f"\nDatabase ready: {DB_PATH}")
print("Open in DB Browser for SQLite or run: sqlite3 marketplace.db")
