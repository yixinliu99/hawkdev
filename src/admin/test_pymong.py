import pymongo
from datetime import datetime, timedelta
from admin.consts.consts import *

import random

def generate_dummy_auction_data():
    """Generate a list of dummy auction documents."""
    categories = ["Electronics", "Furniture", "Books", "Clothing", "Sports"]
    # statuses = ["active", "closed", "stopped"]
    data = []

    for i in range(10, 12):  # Generate 20 dummy auctions
        auction = {
            "_id": f"auction{i}",
            "title": f"Item {i}",
            "description": f"Description for item {i}",
            "starting_price": round(random.uniform(10, 500), 2),
            "current_price": round(random.uniform(10, 500), 2),
            "start_time": datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            "end_time": datetime.utcnow() - timedelta(days=random.randint(1, 10)),
            "category": random.choice(categories),
            "status": "stopped",
            "user_id": f"user{random.randint(1, 10)}",
            "flagged": random.choice([True, False]),
        }
        data.append(auction)
    return data

client = pymongo.MongoClient(MONGO_LINK)

db = client[MONGO_DATABASE]

dummy_data = {}

dummy_data['auctions'] = generate_dummy_auction_data()

dummy_data['users'] = [
        {"_id": f"user{i}", "name": f"User {i}", "email": f"user{i}@example.com", "blocked": False}
        for i in range(1, 11)
    ]

dummy_data['categories'] = [
        {"_id": f"cat{i}", "name": category}
        for i, category in enumerate(["Electronics", "Furniture", "Books", "Clothing", "Sports"], start=1)
    ]

dummy_data['items'] = [
        {"_id": f"item{i}", "name": f"Item {i}", "flagged": random.choice([True, False])}
        for i in range(1, 11)
    ]

dummy_data['emails'] = [
        {
            "_id": f"email{i}",
            "user_email": 'lihaowen@uchicago.edu',
            "message": f"Email {i} from jayce.",
            "response": None,
            "responded": False,
        }
        for i in range(1, 6)
    ]

# collections = ['users', 'categories', 'items', 'emails']
# collections = ['emails']
# for collection_name in collections:
#     collection = db[collection_name]
#     collection.delete_many({})  # Clear existing data
#     collection.insert_many(dummy_data[collection_name])  # Insert new data
#     print(f"Inserted {len(dummy_data[collection_name])} documents into '{collection_name}' collection.")

auctions  = db['auctions']

start_date = datetime.isoformat(datetime.utcnow() - timedelta(days=10))
print(start_date)
result = auctions.find({"active": False, "ending_time": {"$gte": start_date}})

for r in result:
    print(r)

    