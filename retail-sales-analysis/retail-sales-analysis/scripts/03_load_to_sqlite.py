"""Load the clean CSV into a SQLite database (no installation needed - SQLite ships with Python)."""
import sqlite3, pandas as pd

df = pd.read_csv("data/superstore_clean.csv", parse_dates=["Order Date", "Ship Date"])
df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d")
df["Ship Date"] = df["Ship Date"].dt.strftime("%Y-%m-%d")
df.columns = [c.replace(" ", "_").replace("-", "_").replace("%", "pct") for c in df.columns]

con = sqlite3.connect("data/superstore.db")
df.to_sql("orders", con, if_exists="replace", index=False)
con.close()
print(f"Loaded {len(df):,} rows into table 'orders' in data/superstore.db")
