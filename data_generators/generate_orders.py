from faker import Faker
import pandas as pd
import random
fake = Faker()
random.seed(42)
Faker.seed(42)
def generate_orders(n=1000):
    orders = []
    for i in range(n):
        orders.append({
            "order_id":    f"ORD-{i+1:04d}",
            "customer_id": f"CUST-{random.randint(1, 100):03d}",
            "product_id":  f"PROD-{random.randint(1, 50):03d}",
            "quantity":    random.randint(1, 10),
            "unit_price":  round(random.uniform(5.0, 500.0), 2),
            "order_date":  fake.date_between(start_date="-1y", end_date="today"),
            "status":      random.choice(["completed", "cancelled", "pending", "refunded"]),
        })
    return orders
def add_dirty_data(orders):
    for i in random.sample(range(len(orders)), 10):
        orders[i]["order_id"] = None
    for i in random.sample(range(len(orders)), 5):
        orders[i]["unit_price"] = -99
    return orders

def save_orders():
    orders = generate_orders(1000)
    orders = add_dirty_data(orders)
    df = pd.DataFrame(orders)
    df.to_csv("sample_data/orders.csv", index=False)
    print(f"Generated {len(df)} orders -> sample_data/orders.csv")

save_orders()