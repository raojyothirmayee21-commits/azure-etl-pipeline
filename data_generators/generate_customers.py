from faker import Faker
import sqlite3
import random

fake = Faker()
random.seed(42)
Faker.seed(42)
def generate_customers(n=100):
    customers = []
    for i in range(n):
        customers.append({
            "customer_id": f"CUST-{i+1:03d}",
            "name":        fake.name(),
            "email":       fake.email(),
            "country":     fake.country(),
            "city":        fake.city(),
            "tier":        random.choice(["bronze", "silver", "gold"]),
            "joined_date": fake.date_between(start_date="-3y", end_date="today"),
        })
    return customers
def save_customers():
    print("starting...")
    customers = generate_customers(100)
    print(f"customers generated: {len(customers)}")
    
    conn = sqlite3.connect("sample_data/customers.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id  TEXT PRIMARY KEY,
            name         TEXT,
            email        TEXT,
            country      TEXT,
            city         TEXT,
            tier         TEXT,
            joined_date  TEXT
        )
    """)
    
    for c in customers:
        cursor.execute("""
            INSERT OR REPLACE INTO customers VALUES
            (?, ?, ?, ?, ?, ?, ?)
        """, (c["customer_id"], c["name"], c["email"],
              c["country"], c["city"], c["tier"], str(c["joined_date"])))
    
    conn.commit()
    conn.close()
    print("done")

save_customers()