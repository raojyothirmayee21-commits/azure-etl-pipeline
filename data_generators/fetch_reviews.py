
import requests
import json

# All product IDs we generated
product_ids = [f"PROD-{i:03d}" for i in range(1, 51)]

all_reviews = []

for product_id in product_ids:
    page = 1
    while True:
        response = requests.get(
            f"http://localhost:8000/reviews",
            params={"product_id": product_id, "page": page, "page_size": 10}
        )
        data = response.json()
        all_reviews.extend(data["reviews"])

        # Check if we've fetched all pages
        if page * 10 >= data["total"]:
            break
        page += 1

    print(f"Fetched {product_id} — total so far: {len(all_reviews)}")

# Save to landing zone
with open("sample_data/reviews.json", "w") as f:
    json.dump(all_reviews, f, indent=2)

print(f"Done! Total reviews: {len(all_reviews)}")