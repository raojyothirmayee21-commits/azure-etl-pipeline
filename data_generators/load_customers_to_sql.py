import sqlite3
import pyodbc

# Azure SQL connection
conn_str = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:etl-sqlserver-jy.database.windows.net,1433;Database=customers-db;Uid=sqladmin;Pwd=Etl@12345;Encrypt=yes;TrustServerCertificate=no;"

# Read from SQLite
sqlite_conn = sqlite3.connect("sample_data/customers.db")
cursor = sqlite_conn.cursor()
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()
sqlite_conn.close()

print(f"Read {len(customers)} customers from SQLite")

# Connect to Azure SQL
azure_conn = pyodbc.connect(conn_str)
azure_cursor = azure_conn.cursor()

# Create table in Azure SQL
azure_cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='customers' AND xtype='U')
    CREATE TABLE customers (
        customer_id  VARCHAR(20) PRIMARY KEY,
        name         VARCHAR(100),
        email        VARCHAR(100),
        country      VARCHAR(100),
        city         VARCHAR(100),
        tier         VARCHAR(20),
        joined_date  VARCHAR(20)
    )
""")

# Insert customers
for customer in customers:
    azure_cursor.execute("""
        INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?)
    """, customer)

azure_conn.commit()
azure_conn.close()

print("Customers loaded into Azure SQL successfully!")
