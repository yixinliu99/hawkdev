import pymongo
from datetime import datetime, timedelta
from admin.consts.consts import *


class MongoDAO:
    def __init__(self, uri="mongodb://localhost:27017/", database="auction_db", client=None):
        if client:
            # Only for tests
            self.client = client
        else:
            self.client = pymongo.MongoClient(uri)

        self.db = self.client[database]
        self.auctions = self.db[AUCTIONS_COLLECTION]
        self.users = self.db[USERS_COLLECTION]
        self.categories = self.db[CATEGORIES_COLLECTION]
        self.items = self.db[ITEMS_COLLECTION]
        self.emails = self.db[EMAILS_COLLECTION]

    # Auction Operations
    def stop_auction_early(self, auction_id):
        return self.auctions.update_one({"_id": auction_id}, {"$set": {"status": "stopped"}})

    def get_active_auctions(self, sort_by):
        return self.auctions.find({"status": "active"}).sort(sort_by, pymongo.ASCENDING)

    def get_closed_auctions_count(self, timeframe):
        timeframes = {"day": 1, "week": 7, "month": 30}
        start_date = datetime.utcnow() - timedelta(days=timeframes[timeframe])
        return self.auctions.count_documents({"status": "closed", "end_time": {"$gte": start_date}})

    # User Operations
    def block_user_and_remove_auctions(self, user_id):
        user_result = self.users.update_one({"_id": user_id}, {"$set": {"blocked": True}})
        auction_result = self.auctions.delete_many({"user_id": user_id})
        return user_result.modified_count, auction_result.deleted_count

    # Category Operations
    def add_category(self, category_id, category_name):
        self.categories.insert_one({"_id": category_id, "name": category_name})

    def modify_category(self, category_id, category_name):
        return self.categories.update_one({"_id": category_id}, {"$set": {"name": category_name}})

    def remove_category(self, category_id):
        return self.categories.delete_one({"_id": category_id})

    # Flagged Items
    def get_flagged_items(self):
        return self.items.find({"flagged": True})

    # Emails
    def respond_to_email(self, email_id, response_text):
        return self.emails.update_one(
            {"_id": email_id},
            {"$set": {"response": response_text, "responded": True}},
        )

    def close(self):
        self.client.close()
