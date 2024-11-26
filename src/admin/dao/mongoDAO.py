import pymongo
from datetime import datetime, timedelta


class MongoDAO:
    def __init__(self, uri="mongodb://localhost:27017/", database="auction_db"):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[database]

    # Auction Operations
    def stop_auction_early(self, auction_id):
        return self.db.auctions.update_one({"_id": auction_id}, {"$set": {"status": "stopped"}})

    def get_active_auctions(self, sort_by):
        return self.db.auctions.find({"status": "active"}).sort(sort_by, pymongo.ASCENDING)

    def get_closed_auctions_count(self, timeframe):
        timeframes = {"day": 1, "week": 7, "month": 30}
        start_date = datetime.utcnow() - timedelta(days=timeframes[timeframe])
        return self.db.auctions.count_documents({"status": "closed", "end_time": {"$gte": start_date}})

    # User Operations
    def block_user_and_remove_auctions(self, user_id):
        user_result = self.db.users.update_one({"_id": user_id}, {"$set": {"blocked": True}})
        auction_result = self.db.auctions.delete_many({"user_id": user_id})
        return user_result.modified_count, auction_result.deleted_count

    # Category Operations
    def add_category(self, category_id, category_name):
        self.db.categories.insert_one({"_id": category_id, "name": category_name})

    def modify_category(self, category_id, category_name):
        return self.db.categories.update_one({"_id": category_id}, {"$set": {"name": category_name}})

    def remove_category(self, category_id):
        return self.db.categories.delete_one({"_id": category_id})

    # Flagged Items
    def get_flagged_items(self):
        return self.db.items.find({"flagged": True})

    # Emails
    def respond_to_email(self, email_id, response_text):
        return self.db.support_emails.update_one(
            {"_id": email_id},
            {"$set": {"response": response_text, "responded": True}},
        )

    def close(self):
        self.client.close()
