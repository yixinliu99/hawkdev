import pymongo
from datetime import datetime, timedelta
from consts.consts import *


class MongoDAO:
    def __init__(self, uri=MONGO_LINK, database=MONGO_DATABASE, client=None):
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

    def get_active_auctions(self, sort_by='end_time'):
        print("Mongo get active auctions")
        return list(
            self.db.auctions.find(
                {"status": "active"},
                {"_id": 0, "title": 1, "description": 1, "starting_price": 1, "current_price": 1, "start_time": 1, "end_time": 1, "category": 1}
            ).sort(sort_by, 1)
        )
    
    def get_closed_auctions(self, start_date):
        return list(self.auctions.find(
            {"status": "stopped", "end_time": {"$gte": start_date}},
            {"_id": 0, "title": 1, "description": 1, "starting_price": 1, "current_price": 1, "start_time": 1, "end_time": 1, "category": 1}
        ))

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
        return list(
            self.db.items.find(
                {"flagged": True},  # Query for flagged items
                {"_id": 0, "name": 1, "description": 1, "category": 1, "flag_reason": 1, "flagged_date": 1}
            )
        )

    # Emails
    def respond_to_email(self, email_id, response_text):
        return self.emails.update_one(
            {"_id": email_id},
            {"$set": {"response": response_text, "responded": True}},
        )
    
    def get_unresponded_emails(self):
        return list(
            self.emails.find(
                {"responded": False},  # Fetch only unresponded emails
                {"_id": 1, "user_email": 1, "message": 1}  # Include relevant fields
            )
        )


    def close(self):
        self.client.close()
