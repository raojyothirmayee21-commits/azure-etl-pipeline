from faker import Faker
import json
import random

fake = Faker()
random.seed(42)
Faker.seed(42)
def generate_products(n=50):
    categories = ["Electronics", "Clothing", "Food", "Books", "Sports", "Home", "Beauty"]
    products = []
    for i in range(n):
        products.append({
            "product_id":   f"PROD-{i+1:03d}",
            "name":         fake.catch_phrase(),
            "category":     random.choice(categories),
            "unit_cost":    round(random.uniform(2.0, 300.0), 2),
            "stock":        random.randint(0, 500),
            "is_active":    random.choice([True, True, True, False]),
        })
    return products

def save_products():
    print("starting...")
    products = generate_products(50)
    print(f"products generated: {len(products)}")
    
    with open("sample_data/products.json", "w") as f:
        json.dump(products, f, indent=2, default=str)
    
    print("done")
save_products()