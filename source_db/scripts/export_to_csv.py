import os
import pandas as pd
import psycopg2
from datetime import date

OUTPUT_DATE = str(date.today())
BASE_DIR = os.path.join("data_exports", f"load_date={OUTPUT_DATE}")

os.makedirs(BASE_DIR, exist_ok=True)

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="legacy_insurance",
    user="postgres",
    password="postgres"
)

tables = ["customers", "agents", "policies", "claims", "payments"]

for table in tables:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)

    table_dir = os.path.join(BASE_DIR, table)
    os.makedirs(table_dir, exist_ok=True)

    output_path = os.path.join(table_dir, f"{table}.csv")
    df.to_csv(output_path, index=False)
    print(f"Exported {table} -> {output_path}")

conn.close()
print("Done.")
