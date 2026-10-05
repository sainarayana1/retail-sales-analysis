"""Run every query in sql/queries.sql and save each result as a CSV in outputs/."""
import sqlite3, re, pandas as pd

con = sqlite3.connect("data/superstore.db")
sql = open("sql/queries.sql").read()
for block in [b.strip() for b in sql.split(";") if re.search(r"--\s*Q\d+", b)]:
    m = re.search(r"--\s*(Q\d+)\.\s*(.+)", block)
    df = pd.read_sql_query(block, con)
    df.to_csv(f"outputs/{m.group(1)}.csv", index=False)
    print(f"\n=== {m.group(1)}: {m.group(2).strip()} ===")
    print(df.head(12).to_string(index=False))
con.close()
