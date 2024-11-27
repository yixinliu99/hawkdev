from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["notification_db"]  

users_collection = db["users"]
watchlist_collection = db["watchlist"]

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    @classmethod
    def get_by_id(cls, user_id):
        user_data = users_collection.find_one({"user_id": user_id})
        if user_data:
            return cls(user_data["user_id"], user_data["name"], user_data["email"])
        return None

class Watchlist:
    def __init__(self, watchlist_id, user_id, item_id, max_price):
        self.watchlist_id = watchlist_id
        self.user_id = user_id
        self.item_id = item_id
        self.max_price = max_price

    @classmethod
    def add_to_watchlist(cls, user_id, item_id, max_price):
        watchlist_data = {
            "user_id": user_id,
            "item_id": item_id,
            "max_price": max_price
        }
        result = watchlist_collection.insert_one(watchlist_data)
        return result.inserted_id

    @classmethod
    def get_by_user_id(cls, user_id):
        watchlist_items = watchlist_collection.find({"user_id": user_id})
        return [cls(wl["_id"], wl["user_id"], wl["item_id"], wl["max_price"]) for wl in watchlist_items]
