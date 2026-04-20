from fastapi import FastAPI
from faker import Faker
import random

fake = Faker()
random.seed(42)
Faker.seed(42)

app = FastAPI()
@app.get("/reviews")
def get_reviews(product_id: str, page: int = 1, page_size: int = 10):
    random.seed(hash(product_id))
    
    total_reviews = random.randint(20, 200)
    reviews = []
    
    for i in range(page_size):
        reviews.append({
            "review_id":  f"REV-{product_id}-{page}-{i+1}",
            "product_id": product_id,
            "rating":     random.choice([1, 2, 3, 4, 4, 5, 5, 5, None]),
            "text":       fake.sentence(nb_words=12),
            "reviewer":   fake.name(),
            "date":       str(fake.date_between(start_date="-1y", end_date="today")),
        })
    
    return {
        "product_id":   product_id,
        "page":         page,
        "page_size":    page_size,
        "total":        total_reviews,
        "reviews":      reviews
    }

@app.get("/")
def root():
    return {"message": "Reviews API is running!"}