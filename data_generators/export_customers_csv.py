import sqlite3
import pandas as pd

# Read from SQLite
conn = sqlite3.connect("sample_data/customers.db")
df = pd.read_sql("SELECT * FROM customers", conn)
conn.close()

# Save as CSV
df.to_csv("sample_data/customers.csv", index=False)
print(f"Exported {len(df)} customers -> sample_data/customers.csv")