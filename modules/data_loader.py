import json

def load_data():
    with open("data/vinfast_specs.json", "r", encoding="utf-8") as f:
        specs = json.load(f)

    with open("data/vinfast_reviews.json", "r", encoding="utf-8") as f:
        reviews = json.load(f)

    return specs, reviews