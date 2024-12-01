import pymongo

class MongoDao:
    def __init__(self, uri="mongodb://localhost:27017/", database="auction_site"):
        self.client = pymongo.MongoClient(uri)

        self.db = self.client[database]

        # Explicitly check and create collections if they don't exist
        self.orders = self.db['orders'] if 'orders' in self.db.list_collection_names() else self.db.create_collection('orders')
        self.watchlist = self.db['watchlist'] if 'watchlist' in self.db.list_collection_names() else self.db.create_collection('watchlist')
        self.cart = self.db['cart'] if 'cart' in self.db.list_collection_names() else self.db.create_collection('cart')

    def add_to_watchlist(self, user_id, item_id, keyword, category):
        watchlist_item = {
            "user_id": user_id,
            "item_id": item_id,
            "keyword": keyword,
            "category": category
        }

        self.watchlist.insert_one(watchlist_item)

    def get_watchlist(self, user_id):
        watchlist_items_cursor = self.watchlist.find({"user_id": user_id})
        return list(watchlist_items_cursor)  

    def remove_from_watchlist(self, user_id, item_id):
        result = self.watchlist.delete_one({"user_id": user_id, "item_id": item_id})
        return result.deleted_count > 0  

    def add_to_cart(self, user_id, item_id, item_data, quantity):
        cart_item = {
            "user_id": user_id,
            "item_id": item_id,
            "shipping_cost": item_data.get('shipping_cost'),
            "description": item_data.get('description'),
            "flagged": item_data.get('flagged'),
            "category": item_data.get('category'),
            "keywords": item_data.get('keywords'),
            "starting_price": item_data.get('starting_price'),
            "quantity": quantity
        }

        self.cart.insert_one(cart_item)

    def get_cart(self, user_id):
        cart_items_cursor = self.cart.find({"user_id": user_id})
        return list(cart_items_cursor)  

    def get_cart_item(self, user_id, item_id):
        return self.cart.find_one({"user_id": user_id, "item_id": item_id})
    
    def update_cart_item_quantity(self, user_id, item_id, quantity):
        self.cart.update_one(
            {"user_id": user_id, "item_id": item_id},
            {"$inc": {"quantity": quantity}}
        )
    def remove_from_cart(self, user_id, item_id):
        result = self.cart.delete_one({"user_id": user_id, "item_id": item_id})
        return result.deleted_count > 0  
    
    def remove_all_cart(self, user_id):
        return self.cart.delete_many({"user_id": user_id})
    
    def add_to_orders(self, user_id, total_amount, items, status, created_at):
        return self.orders.insert_one(user_id, total_amount, items, status, created_at )