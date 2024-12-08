from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['127.0.0.1:27017']
items_collection = db['items']

# Sample items to add
items = [
    {
        "description": "Item 1",
        "starting_price": 100,
        "category": "Electronics"
    },
    {
        "description": "Item 2",
        "starting_price": 200,
        "category": "Books"
    },
    {
        "description": "Item 3",
        "starting_price": 300,
        "category": "Clothing"
    }
]

# Insert items into the collection
items_collection.insert_many(items)
print("Items added successfully!")